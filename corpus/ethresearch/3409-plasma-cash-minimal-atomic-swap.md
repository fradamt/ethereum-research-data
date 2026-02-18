---
source: ethresearch
topic_id: 3409
title: Plasma Cash Minimal Atomic Swap
author: vbuterin
date: "2018-09-17"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-cash-minimal-atomic-swap/3409
views: 7628
likes: 8
posts_count: 13
---

# Plasma Cash Minimal Atomic Swap

The following is my attempt at a two-round atomic swap protocol for Plasma Cash. Suppose an atomic swap of X going from A -> B and Y going from B -> A.

1. A generates a random key S_A and a value h_A = hash(S_A). B similarly generates S_B and h_B = hash(S_B). They share h_A and h_B.
2. A and B sign an “intent-to-transfer” message containing (i) their coin ID, (ii) the counterparty coin ID, (iii) h_A and h_B
3. The intent-to-transfer messages get included into the Plasma Cash chain in their respective slots (that is, the “new owner” of each coin is the respective intent-to-transfer message). The Plasma Cash chain makes sure to include them in the same block.
4. A and B publish S_A and S_B
5. A “secret publication record” containing S_A and S_B gets committed to the main chain in a Merkle tree (ie. the tree could contain many such records from many exchange events)

When the “current owner” of a coin is an intent to transfer message, a special exit challenge rule is added: a “secret publication event” containing S_A and S_B that is committed to on-chain in the block *immediately after* the block containing the intent to transfer message can be used to challenge the exit to transfer the owner from the sender to the recipient, as long as this challenge is made within 7 days. If a challenge is made within 7 days on one exit, the deadline is extended to 14 days for the other exit.

These rules also apply if an intent-to-transfer owner is part of a coin’s ownership history, eg. if the ownership chain is A -> (A->B) -> C -> D, then D’s right to exit the coin would be dependent on whether or not it’s true that either (i) the (A->B) -> C transaction was **signed by A** and there **is no** secret publication event for (S_A, S_B) or (ii) the (A->B) -> C transaction was **signed by B** and there **is** a secret publication event for (S_A, S_B).

At all stages of the above, if A or B or the chain fail to fulfill their duties the other parties have an emergency action they can undertake to ensure a safe outcome:

- If either A or B do not publish an h value, the process simply terminates and fails.
- If either A or B do not publish an intent-to-transfer message, the chain can make sure the other message does not get included. If the chain misbehaves and includes only one of the two messages, or includes them in different blocks, then the honest party can exit; because they did not publish their S value, they are safe.
- If either A or B do not publish their S value, the counterparty can by default wait for the next Plasma Cash block, and if nothing has happened, send a transaction to transfer their coin back to themselves; after 2 blocks it can legally get included in the Plasma chain.
- If the Plasma Cash chain withholds part of the next block, then A and B can both exit their (originally owned) coins. If either one of the exits is challenged with the (S_A, S_B) pair, then the counterparty has the ability to do the same to the other exit within 7 days (due to the deadline lengthening rule)

Performance properties:

- A malicious party can only lock up their counterparty’s coins for 2 blocks
- An honest party can only be forced to exit by a malicious operator, not a malicious counterparty
- In the simplest scheme, participants are required to watch O(N) data (the secrets) only during the one block when they are transacting their coins, and otherwise they are required to watch O(C * log(N)) if they hold C coins.
- The process for completing a transaction involves a round of data exchange for exchanging hashes, a Plasma confirmation for the intent to transfer, and one further round of data exchange and Plasma confirmation for the secrets, so two rounds of data exchange and Plasma confirmation in total.

The need to download the whole block containing the secrets after a transaction can be reduced further by making a 2D Merkle tree (ie. a Merkle quad tree) where (S_A, S_B) must be included at position (A, B); this reduces the data requirements to O(C * log(N)) in all cases.

## Replies

**danrobinson** (2018-09-18):

What is added by the extra preimage step, relative to just having the validity of one part of the transaction be directly dependent on the inclusion of the same transaction in the other coin’s slot in the same block?

---

**vbuterin** (2018-09-18):

Now that I think about it, the preimage may not actually be necessary and I may have needlessly created something overcomplicated. Need to think about this more…

If you’re right, then atomic swaps are *super* easy, and so Plasma Cash defragmentation is actually not bad at all, making Plasma Cash *extremely* viable even today…

---

**danrobinson** (2018-09-18):

Yep, if we’re lucky I think all you need to support this are atomic transactions (txes that must be included in all of the involved coins’ merkle slots in the same block to be valid) and maxtimes (to prevent your counterparty from hoarding your signature on a transaction without giving you theirs). If the operator is providing you data, then you will know for certain by the transaction’s maxtime whether it will ever be included.

If the operator is withholding data, they can force you to attempt to exit the previous coin (possibly invalidly and thus losing an exit bond), but as you mention, that’s true of your scheme as well. I think this is insurmountable (as do [@karl](/u/karl) and [@kfichter](/u/kfichter) I think)—in any multi-coin atomic transaction scheme where multiple parties are involved, the operator can, by strategic data withholding and cooperation with one party, cause the other party to lose an exit bond. That is not the case in single-coin-transaction Plasma Cash (or single-coin-transaction Plasma MVP) with limbo exits, but I think it is probably endemic to anything that supports atomic transactions with multiple coins. And it’s a capped, relatively small cost, that can only be imposed once, by an operator whose Plasma Cash chain you’ve explicitly decided to join, so as griefing attacks go, it is extremely modest.

---

**vbuterin** (2018-09-18):

The operator can always cause participants to have to exit; hasn’t that been part of the security model all along?

---

**danrobinson** (2018-09-18):

In these cases they can force you to attempt an *invalid* exit, thus having to pay to reward a challenger. In Plasma Cash without atomic transactions, it’s possible to construct a limbo exit (or “force confirmation”) scheme that keeps you safe from ever having to attempt an invalid exit, even when the operator goes rogue while you have a transaction in flight.

(I’ve generally given up on Plasma Cash limbo exits anyway, since their complexity isn’t worth the minor griefing problem they solve.)

---

**gakonst** (2018-09-18):

Just reiterating your post with some comments, to see if I understood this correctly

With this, the ownership of a token becomes more abstract. The “intent-to-transfer” message being the new owner of a coin can be thought of as a new account type (I’ll call this the *escrow account*)

All the preimages for each coin that would be swapped get merkleized and committed, per block. The operator must also make all data available. If they don’t there is a constant griefing factor of 1 bond during exits.

Here are my questions:

1. How will you generate this account’s address? Maybe deterministically from its arguments as Hash(coin Id, counterparty coin Id, h_a, h_b)?
2. How does one exit a coin that is being owned by this sort of “escrow account”? I do not see how it’s possible to exit only one of the 2 coins held by the escrow while leaving the other in the Plasma chain.
3. My guess is that this generalizes to more than 2 coins, just increasing the data availability requirements along with coordination overhead by the participants?
4. Doesn’t this construction make it increasingly complex to check a coin’s history if a user receives a coin which had multiple atomic swaps in its history?

This may be a good building block for multisigs on top of a coin, towards making state channels work on Plasma, given that this is like a state deposit in an account where funds are unlocked under specific rules.

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> What is added by the extra preimage step, relative to just having the validity of one part of the transaction be directly dependent on the inclusion of the same transaction in the other coin’s slot in the same block?

We’ve talked about this in Plasma Debit context where the receiver does not care that the sender’s coin changes ownership, however in this context we need circular dependencies ie. txA requires txB to be included, and txB requires txA to be included. How would it work?

---

**danrobinson** (2018-09-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> We’ve talked about this in Plasma Debit context where the receiver does not care that the sender’s coin changes ownership, however in this context we need circular dependencies ie. txA requires txB to be included, and txB requires txA to be included. How would it work?

I think it should work fine—you just have a single compound tx, txAB, with a list of multiple operations involving multiple coins, and when anyone reveals a Merkle proof of it as part of an exit, challenge, or response on one of those coins, they also have to reveal that it was included in the other path(s) for it to count. It’s a slightly different kind of dependency from what we’ve talked about in Debit but if anything this fits a more traditional concept of a transaction.

---

**kfichter** (2018-09-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> they also have to reveal that it was included in the other path(s) for it to count.

I guess this does increase proof size, but the impact depends on the frequency of atomic swaps in practice.

---

**kfichter** (2018-09-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> Doesn’t this construction make it increasingly complex to check a coin’s history if a user receives a coin which had multiple atomic swaps in its history?

At least with what Dan’s saying, the history check doesn’t become much more complex. If there’s ever an Atomic swap (A<=>B), you just need to provide both sides of the atomic swap transaction. As I said above, this does increase proof size but probably not significantly.

---

**augustoteixeira** (2018-09-20):

A suggestion for this to go hand in hand with plasma cash defragmentation: allow swaps of a whole subtree of coins belonging to the same owner.

The only modification necessary is that the signature in the “intent-to-transfer” could include (instead of the coin ID) an identification of a sub-branch containing the said coin.

This would make the proofs much more compact, as the exact same transaction would be repeated for a large and contiguous batch of coin slots in a block.

---

**vbuterin** (2018-09-24):

Here’s another defragmentation solution that does not require atomic swaps: [Plasma Cash defragmentation, take 2](https://ethresear.ch/t/plasma-cash-defragmentation-take-2/3515)

---

**benj0702** (2018-10-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> I think this is insurmountable (as do @karl and @kfichter I think)—in any multi-coin atomic transaction scheme where multiple parties are involved, the operator can, by strategic data withholding and cooperation with one party, cause the other party to lose an exit bond.

This feels true up to the swap amount, but I think the potential loss might be less than an exit bond.  What do you think of the following scheme?

Instead of the above, we execute swaps Interledger-style, via payment channels (requiring that once opened, swap channels cannot be closed by the operator unless fully swapped).  By exchanging \epsilon of value at a time, counterparties only risk not knowing where \epsilon of their funds are.  This value can be smaller than an exit bond.

