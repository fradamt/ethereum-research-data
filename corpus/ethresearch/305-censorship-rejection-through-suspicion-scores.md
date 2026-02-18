---
source: ethresearch
topic_id: 305
title: Censorship rejection through "suspicion scores"
author: vbuterin
date: "2017-12-10"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/censorship-rejection-through-suspicion-scores/305
views: 8332
likes: 9
posts_count: 8
---

# Censorship rejection through "suspicion scores"

Each client maintains a “suspicion score” for each chain C, which works as follows:

score = \underset{v \in votes}{max} \left( TimeSeenIncluded(v, C) - TimeSeen(v) - \frac{now - TimeSeenIncluded(v, C)}{16} \right)

Where votes is the set of votes that were valid to be included in C at the time they were submitted, now is the current timestamp, TimeSeen(v) is the time that the node first saw that vote, and TimeSeenIncluded(v, C) has a three-part conditional definition:

- if v \in C (ie. v has been included in C), then it’s the time that the block in C that included v was received
- if v \not\in C but including v would no longer be valid (eg. because an epoch timed out), then it’s the time that the last block in C in which including v is still valid was received
- otherwise, it’s now

Basically, it’s the longest amount of time that the client has seen that a vote could have been included in the chain but was not included, with a “forgiveness factor” where old events are discounted by how old they are divided by 16.

It’s fairly easy to show that if there is a latency bound \delta between two clients, then the two clients’ suspicion scores will differ by at most 2 * \delta. It’s also easy to show that a chain cannot censor votes without racking up a suspicion score among all clients.

We can also add two modifications to the Casper FFG protocol:

1. If an epoch is not finalized, the next epoch is 25% longer. The lengths reset only if an epoch does get finalized.
2. A vote is allowed to include one transaction (in a stateless client model, it would need to have witnesses based on the state root of the block the vote is voting for). If a block includes the vote, it must process that transaction.

(1) does the double-duty of both (i) making Casper FFG a properly partially synchronous consensus algo, able to provably eventually get consensus with *any* latency bound \delta, and (ii) ensuring that if a chain continues censoring for a long time, it’s suspicion score will increase unboundedly. (2) ensures that full transaction censorship cannot happen without vote censorship.

The purpose of this scheme is to serve as a social coordination tool for users to reject censoring chains. Users are guaranteed to have suspicion scores that are reasonably similar, and this will make it easier to coordinate on whether or not to perform a minority fork to escape a censorship attack at any given time.

---

Addendum (2017.12.30):

In the current FFG spec, only ~20 minutes of latency is sufficient to make Casper never include certain blocks, transactions or votes, so this suspicion score would not work very well in that context. To solve this problem, we can add a rule that if an epoch does not finalize, the next epoch’s length doubles, and epoch lengths continue doubling until an epoch does finalize. If EpochLength = 50 * 2^{EpochsSinceFinality}, or any other formula, then we’d maintain the quadratic leak by simply setting LeakThisEpoch = k * EpochLength * BlocksSinceFinality; in this context, BlocksSinceFinality = EpochLength - 1, but in other contexts it could be different. This way, you would actually need to accrue a high suspicion score to fully censor votes.

This also makes Casper FFG secure in the “latency < \delta but we don’t know what \delta is” formulation of the partially synchronous network model.

## Replies

**kladkogex** (2017-12-10):

It does not say exactly how the suspicion score is used …  My understanding is that it is to be plugged into the consensus protocol as one of the factors for selecting the winning chain?  An otherwise winning chain can be thrown away if its suspicion score crosses a certain threshold?

.

I guess one also needs to define how much validators pay for votes.  Currently, miners include transactions that pay the most. I think a miner should be deemed suspicious if it keeps a vote out but includes a lower-paying transaction. I am assuming that Casper votes are just regular smart contract calls and validators pay for voting … Or we are talking about a Casper implementation where the core protocol is modified and votes are not regular smart contract calls?

---

**vbuterin** (2017-12-10):

It’s not something used automatically; it’s something that the client keeps track of and may use to *manually* collectively agree to reject a chain if it is not including legitimate votes.

The reason not to make it automatic is that doing that would require some specific suspicion threshold to overcome finality, and a 51% attacker could make a main chain that overcomes this threshold for 10% of users and not the other 90%, continually confusing users with very very little risk of the attacker losing funds from the leak.

---

**kladkogex** (2017-12-11):

I see  … so it is more of a last resort thing …

It looks like every node will be required to check every pending vote *not yet included in the chain* for  validitity (vote signed by a valid validator with enough deposit) …

What if a malicious network participant (not a validator) creates zillions of sybil ETH accounts that emit zillions of fake votes, that will never be included in the chain, but could cause lots of computational activity on each and every client?  Looks like for each incoming fake vote each client would need to do a check if this vote belongs to a valid validator - how much computationally intense will this be?  Would it be possible to mount a DoS attack based on that …?

---

**vbuterin** (2017-12-11):

> Looks like for each incoming fake vote each client would need to do a check if this vote belongs to a valid validator - how much computationally intense will this be? Would it be possible to mount a DoS attack based on that …?

This is not more difficult than the problem of a miner receiving transactions from clients and figuring out if those transactions are actually capable of paying for their gas, or the problem of a client receiving such transactions and figuring out whether or not to relay them, or a client receiving block headers, or…

---

**kladkogex** (2017-12-11):

How does a client check validity of a vote that has not yet been included in the blockchain yet?![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Lets take the following example -

- there is a slashing transaction for a validator and a vote that this validator is issuing
- both transactions happening approximately at the same time
- the miner receives the vote after it receives the slashing transaction, and then rightfully does not include the vote
- the client receives the vote first, and then receives the slashing transaction.

What algorithm should the client follow?![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**vbuterin** (2017-12-12):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Lets take the following example -
>
>
> there is a slashing transaction for a validator and a vote that this validator is issuing
> both transactions happening approximately at the same time
> the miner receives the vote after it receives the slashing transaction, and then rightfully does not include the vote
> the client receives the vote first, and then receives the slashing transaction.

See:

> if v \not\in C but including v would no longer be valid (eg. because an epoch timed out), then it’s the time that the last block in C in which including v is still valid was received

Just follow this rule mechanically and you’ll be fine. Basically, if at any point including v stops being valid, assume that v was included right there and then.

---

**vbuterin** (2017-12-30):

See addendum to original post.

