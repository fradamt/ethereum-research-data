---
source: ethresearch
topic_id: 1901
title: Reliable Exits of Withheld In-flight Transactions ("Limbo Exits")
author: kfichter
date: "2018-05-03"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/reliable-exits-of-withheld-in-flight-transactions-limbo-exits/1901
views: 4606
likes: 11
posts_count: 8
---

# Reliable Exits of Withheld In-flight Transactions ("Limbo Exits")

# Reliable Exits of Withheld In-flight Transactions (“Limbo Exits”)

This post is a more long-winded version of ideas that came out of conversations with Piotr Dobaczewski, [@danrobinson](/u/danrobinson), [@DavidKnott](/u/davidknott), and [@jcp](/u/jcp). Credit of the original concept goes to Piotr, who astutely noticed that we can settle withheld in-flight transactions on the root chain. Some modifications are made to Piotr’s original concept.

## Edit

Since publishing this post, I’ve realized that the scheme only works if the outputs are cooperating. When we’re talking about a single output, that’s probably reasonable. If we have multiple unrelated outputs, that’s less reasonable. The [More Viable Plasma](https://ethresear.ch/t/more-viable-plasma/2160/22) construction doesn’t have this problem (assumes non-cooperation), but I still think limbo cancels are a very important because they make things easier when there is cooperation.

## Problem Background & Motivation

Both Plasma Cash and David Knott’s no-conf version of Plasma MVP suffer from the problem of “transactions in limbo.” In a nutshell, this problem arises when a transaction is in-flight but part (or all) of the Plasma chain is unavailable. Neither party to the transaction knows where (or if) the transaction is included in a block, so the sending party must attempt an exit on their possibly spent coin.

If the transaction has already been included in a block, then the operator can submit a challenge and claim the sending party’s bond. In the Plasma Cash case, the operator could even choose to create a new block that includes the transaction after the fact specifically to claim the bond. This action gives the receiving party enough information to exit from the now-included transaction.

I’m of the opinion that this isn’t a particularly satisfying solution. There’s some sense of uncertainty about who will actually receive the exit, and the grieving factor against the sender is possibly non-negligible. This is, of course, up for debate. If users and implementers are generally OK with this attack vector, then the mechanism described in this post is unnecessary.

## Limbo Exits

“Limbo Exits” (as coined by Piotr possibly? not sure) are a special type of exit that attempts to solve the above problem. The general idea of the construction is that the sender will allow the receiver to “force” the transaction to complete on the root chain. This effectively becomes a confirmation signature that’s only necessary in the very specific case of withheld in-flight transactions. It’s possible to extend this construction so that the receiver may force the transaction *not* to complete, but the first use case seems generally more useful.

We’ll detail how this scheme would work in the context of Plasma Cash. First, let’s set up a scenario where the limbo exit will become necessary:

1. A broadcasts a transaction sending a coin to B while the Plasma chain height is at N.
2. The operator begins withholding blocks at Plasma block N + 1.
3. Neither party knows if the transaction from A to B is included in block N + 1.

Without limbo exits, `A` is forced to attempt an exit first. If the operator has included the transaction from `A` to `B`, then the operator will challenge the exit started by `A`, giving `B` the required information to exit.

Limbo exits instead allow the two parties to agree to complete the transaction on the root chain and exit simultaneously. Limbo exits are started as follows:

1. A sends B a signature on the hash of the in-flight transaction plus some special constant. This minimizes the size of the signature and makes the signature is different than the signature A has already provided on the transaction hash. The special constant can probably just be a single bit.
2. B starts a limbo exit by submitting all data A would submit if A were exiting from the coin, as well as the signature received in (1) and the in-flight transaction. “All data A would submit” is effectively the entire tx giving A control of the coin, the block in which that tx was included, and an inclusion proof. Note that no Merkle proof-of-inclusion is required for the in-flight transaction because this transaction may or may not actually be included. B places a bond on the exit as normal.

The limbo exit can then be blocked if the challenger provides either:

1. Any signed transaction from B spending the coin that appears in a block after the one given in (2) or
2. Any signed transaction from A spending the coin (except the one given in (2)!) that appears in a block after the one given in (2)

These challenge conditions guarantee (I think?) that the exit can only be challenged if `A` or `B` genuinely double spent the coin.

## Caveats

Note that this mechanism only works when `A` and `B` are cooperating. We assume that if the two are cooperating, they will want to complete the transaction as planned. As stated before, it’s possible to adapt this design to allow `B` to “reject” the transaction by effectively running the signature scheme in reverse.

The reliance on cooperation is probably not an issue. If `A` and `B` are not cooperating, then the transaction may or may not complete depending on if the operator has included it or not. This situation would probably require extra-protocol resolution anyway and is similar to the case where a customer pays for a product but the merchant fails to send it.

## Optimizations

- We can reduce the amount of data B is required to submit by allowing B to simply assert that the transaction giving A control was included in the given block. This means we need to allow another challenge type where the challenger proves the transaction for that coin in the stated block did not give A control or some equivalent interactive game.

## Notes/Changelog/Etc.

So I *think* this works. I may be entirely wrong, we may need more challenge conditions, it may not work at all. Feedback/criticism/review is always more than welcome!

Again, a special thanks to Piotr Dobaczewski, Dan Robinson, David Knott, and Joseph Poon for useful conversations about this idea.

## Replies

**ldct** (2018-05-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> David Knott’s no-conf version of Plasma MVP

is this written down anywhere? my guess would be that it is an adaptation of this comment [Plasma Cash: Plasma with much less per-user data checking - #18 by MaxC](https://ethresear.ch/t/plasma-cash-plasma-with-much-less-per-user-data-checking/1298/18) to MVP, but I’d rather prefer to encourage more stuff to be written down.

I agree with the need for this limbo exit mechanism, but there’s some stuff in the “problem and motivation” section that concerns me, in particular, the use of bonds. IMO it should never be OK for an honest user to end up in a situation where his funds are on a plasma chain and exiting could result in him losing a large bond. a trivial way to enforce this property is to not require bonds for any exits, but this means that anyone can grief anyone else (unbounded amount, but bounded griefing factor). if we accept this, then the user-might-have-to-exit-twice problem is actually acceptable. of course, we probably don’t want to accept this. I think the general principle should be that users post bonds to exit but the bond is only taken away in cases where the exiter is provably cheating.

---

**kfichter** (2018-05-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> is this written down anywhere?

Yep, a version of the spec is maintained [here](https://github.com/omisego/research/blob/master/plasma/plasma-mvp/specifications/no-confirmations.md).

I agree with the problem around bonds, but it seems to be the best way to motivate challenges on exits (currently necessary). Ideally users would be able to absolutely prove that some coin/UTXO is unspent, possibly via some zk scheme.

---

**ldct** (2018-05-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> to be the best way to motivate challenges on exits

nitpick: in plasma cash the motivation is that if the legitimate coinholder does not challenge the exit, they lose their eth

---

**kfichter** (2018-05-03):

Yeah - I need to make some edits here so it’s Plasma Cash specific. I keep flipping between no-conf MVP and Plasma Cash.

---

**AlexXiong97** (2018-07-05):

May I ask why not just adding a `maxPlasmaBlockHeight` field in every tx to avoid this limbo exit? As [suggested here](https://ethresear.ch/t/plasma-cash-plasma-with-much-less-per-user-data-checking/1298/18).

---

**kfichter** (2018-07-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexxiong97/48/10228_2.png) AlexXiong97:

> May I ask why not just adding a maxPlasmaBlockHeight field in every tx to avoid this limbo exit?

Still have the same problem if blocks are withheld within the `maxPlasmaBlockHeight` (although I still use it as a mitigation for most cases).

---

**vbuterin** (2018-07-05):

If a user sets `maxPlasmaBlockHeight` to equal the height of the next Plasma block, then you can reduce the limbo issues, as there is no way for the transaction to get included in the chain after some other transaction in the same slot.

