---
source: ethresearch
topic_id: 2236
title: 1-bit aggregation-friendly custody bonds
author: JustinDrake
date: "2018-06-13"
category: Sharding
tags: [proofs-of-custody]
url: https://ethresear.ch/t/1-bit-aggregation-friendly-custody-bonds/2236
views: 13578
likes: 9
posts_count: 13
---

# 1-bit aggregation-friendly custody bonds

**TLDR**: We present a 1-bit custody bond scheme which is friendly to BLS aggregation.

**Construction**

Let V be a 32-ETH collateralised validator that has published H(s) onchain where s is a 32-byte secret. Given a piece of data D the validator V can compute the corresponding “custody bit” b as follows:

1. Partition D into 32-byte chunks
2. XOR every 32-byte chunk with s and H(D)
3. Merkleise the XORed chunks to get a root r
4. Let b be the least significant bit of r

The signed message [H(D), b] is a non-outsourceable 1-bit custody bond assuming the following constraints (enforced with slashing conditions):

1. Secrecy: The secret s must be kept secret for some time, e.g. at least 15 days after publishing the proof of custody.
2. Expiry: The secret s must be revealed eventually, e.g. within 30 days after publishing the proof of custody.
3. Consistency: The custody bit b must derive correctly from s and D (enforced with a TrueBit-like challenge game).

Notice that a 1-bit custody bond has 16 ETH of cryptoeconomic security. Indeed, choosing b better than at random requires custody of D (and of s, for non-outsourceability).

We now add custody bonds for [BLS aggregated votes](https://ethresear.ch/t/pragmatic-signature-aggregation-with-bls/2105). Let V_1, ..., V_{1024} be a committee of 1024 validators voting on H(D). Each validator is invited to make a “bonded vote” [H(D), b] which can either be a “0-vote” where b = 0 or a “1-vote” where b = 1. The 0-votes and 1-votes are aggregated into a single 96-byte signature, and the 1024-bit string is replaced with a 1024-trit string to account for the three possibilities per validator (no vote, 0-vote or 1-vote).

**Discussion**

The added costs of custody bonds in aggregated votes are marginal:

- Every validator consumes 1 trit (~1.58 bit) instead of 1 bit, adding 75 bytes of overhead per aggregated committee vote.
- Signature verification requires 3 pairings instead of 2, adding <2.7ms of verification time per aggregated committee vote.

Notice also that we can augment the cryptoeconomic security of custody bonds close to 32 ETH. The reason is that the same piece of data D can be included in several custody bonds for added security. (Having overlapping custody bonds works especially well for shard attestations when the committee of attesters is infrequently shuffled.)

For example, two 1-bit custody bonds [H(D_1), b_1] and [H(D_2), b_2] where D is contained in both D_1 and D_2 yields a 2-bit custody bond for D with security 24 ETH. (The reason we XOR chunks with H(D) in the construction above is to avoid validators caching the Merkleisation of D across custody bonds thanks to the unpredictability of H(D). We could also use beacon outputs instead of H(D).)

## Replies

**vbuterin** (2018-06-15):

Let me try to summarize the core principle in plain English.

Every month, each validator publishes the hash H(x) of some secret random value x that they choose. Every time the validator signs a cross-link, where that cross-link commits some large pile of data D to the main chain, the validator performs some big unholy magic (but deterministic) computation on D and x, and signs only the first bit of the output of this computation. At the end of the month, the validator is required to publish x. At that point, anyone else can repeat the computations that the validator made, and see if the first bit is the same as the first bit published by the validator.

If the value that they compute is not the same, then they can play a game, where they publish a series of challenge values to the chain, each representing some intermediate step in the computation, and the validator is required to respond to all challenges, and the responses are checked for compliance with the bit that they published. If the published bit is wrong, then there is a strategy that anyone can follow to zero in on the precise point in the computation where it went wrong, and prove to the chain that it actually was wrong, and by doing so steal that validator’s deposit.

---

**daniel** (2018-08-09):

This might be a stupid question, but why does *s* have to be kept secret at all? What is the downside of publishing it immediately and therefore letting everyone verify the custody bonds at arbitrary times?

And assuming the 15 day and 30 day limits from the first post: Does this imply that the validator generates a new secret after publishing the current one (after 15 days)?

---

**JustinDrake** (2018-08-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/daniel/48/146_2.png) daniel:

> why does s have to be kept secret at all? What is the downside of publishing it immediately and therefore letting everyone verify the custody bonds at arbitrary times?

The downside is that the custody bit would become outsourceable which would be a centralisation vector.

![](https://ethresear.ch/user_avatar/ethresear.ch/daniel/48/146_2.png) daniel:

> assuming the 15 day and 30 day limits from the first post: Does this imply that the validator generates a new secret after publishing the current one (after 15 days)?

Yes, a new secret is committed whenever a previous secret is revealed. This can be done in a single optimised step with a hash onion (aka hash chain). Secrets must be refreshed between 15 and 30 days, and it’s possible that multiple secrets run in parallel.

---

**DB** (2018-08-09):

Another stupid question: Can’t a cheating validator catch himself, thus cheating and not loosing the 32 ETH? Maybe add a burn for some of it?

---

**vbuterin** (2018-08-10):

Yeah, realistically you only need a fairly small incentive, even 10% might do it.

---

**daniel** (2018-08-10):

Okay, thanks, that makes sense.

So this basically forces validators to keep the data of all collations / main-chain blocks / cross-links that they voted on for at least 30 + x days (as long the maximum challenge period would be), right? Is there any estimation of how much that could be on average?

And: what happens to the data after the challenge period runs out? Is there any incentive for anyone to keep historic data that I missed?

---

**JustinDrake** (2018-08-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/daniel/48/146_2.png) daniel:

> Is there any estimation of how much that could be on average?

We can set the parameters appropriately. IMO something on the order of weeks (e.g. 2-6 weeks) would be reasonable.

![](https://ethresear.ch/user_avatar/ethresear.ch/daniel/48/146_2.png) daniel:

> what happens to the data after the challenge period runs out?

After the challenge period runs out validators can safely discard the data.

![](https://ethresear.ch/user_avatar/ethresear.ch/daniel/48/146_2.png) daniel:

> Is there any incentive for anyone to keep historic data that I missed?

The most important data is state, which is naturally incentivised.

For historical data (i.e. blocks and blobs/transactions) some ecosystem participants (e.g. block explorers, exchanges, [archive.org](http://archive.org), academics, the NSA, …) are incentivised to keep it. The raw storage costs shouldn’t be prohibitively high for a company (on the order of ~50 TB per year for all the shards).

Users and service providers may be incentivised to keep the data relevant to the applications they care about. Validators and other participants may be incentivised to keep the data for fancy stuff like alternative execution engines, historical data markets, witness auto-update for stateless clients, …

---

**daniel** (2018-08-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> We can set the parameters appropriately. IMO something on the order of weeks (e.g. 2-6 weeks) would be reasonable.

Ah, my concern was more about how much data (in GB, etc.) that would be on average per validator.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> The most important data is state, which is naturally incentivised.

How is it naturally incentivised? As far as I understand, validators only need the last x (currently 25?) collations / blocks to safely cast a vote. Who is incentivised to keep the entire state? And how are entities that keep the entire state (or part of it) incentivised to share that state with new participants?

Edit: Actually, how are state transitions happening? Is there a proof of data availability (custody bonds?) for the entire state?

---

**JustinDrake** (2018-08-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/daniel/48/146_2.png) daniel:

> how much data (in GB, etc.) that would be on average per validator

If we assume 1MB per minute of data per shard, and the data is stored for 30 days, that’s 43GB. A decent amount of data, but not unmanageable either.

![](https://ethresear.ch/user_avatar/ethresear.ch/daniel/48/146_2.png) daniel:

> How is it naturally incentivised?

It’s relatively likely that state execution will require executors to have the state (i.e. not stateless client model). If that’s the case then storage of state is incentivised because it allows for participation as an executor.

---

**daniel** (2018-11-01):

A (bit late) follow-up:

1. What happens if we discover weeks after the fact through the challenge game that a block is not available? Okay, a lot of deposits will be slashed, but how does the blockchain recover from this? We cannot revert more than until the last finalized block, right?
2. What’s the point of having the validators store (“cache”) the most recent blocks? If we have stateful executors on every shard that have to store the entire state anyway and we assume that history will be stored by actors with external motivation, what role is actually fulfilled by validators storing the data for so long? Is it just to prove that the data was available at the time when the validator attested to it (aka. it was not withheld)?

---

**JustinDrake** (2018-11-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/daniel/48/146_2.png) daniel:

> What happens if we discover weeks after the fact through the challenge game that a block is not available?

Until we have data availability proofs unavailable blocks must be manually hard forked away. I expect unavailable blocks to be detected fast, certainly in less than weeks.

![](https://ethresear.ch/user_avatar/ethresear.ch/daniel/48/146_2.png) daniel:

> What’s the point of having the validators store (“cache”) the most recent blocks?

Validators don’t have to store the most recent blocks, but they are liable to respond to challenges with block data. So if they rely on external storage providers they would be taking on some counterparty risk, something a rational actor with limited storage may do.

---

**daniel** (2018-11-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Until we have data availability proofs unavailable blocks must be manually hard forked away. I expect unavailable blocks to be detected fast, certainly in less than weeks.

Ah, I understand. So this would have a huge impact actually. My thought was more like: Since we can only challenge validators after let’s say 15 days, if the validators did not actually store the block it might be unavailable at that time. So I guess the security is that if we have to hardfork to remove the unavailable block (or that became unavailable because noone stored it) and accept the damage caused by it, at least a significant amount of validators will get slashed, right?

How transitive is the application of the custody bond requirement? Let’s say committee C1 attests to Shard block A and broadcasts the custody bonds for shard block A - if now committee C2 attests to the next beacon chain block (child of C1’s block), are they required to download and store shard block A too (since their attestation includes the CYCLE_LENGTH parents of the block they are responsible for? Even though their “main work” is to attest to a block on a different shard, let’s say shard block B?

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Validators don’t have to store the most recent blocks, but they are liable to respond to challenges with block data. So if they rely on external storage providers they would be taking on some counterparty risk, something a rational actor with limited storage may do.

I understand that, but my question is more like: Why? If executors need the block immediately and have to store it forever anyway - why bother burdening the validators with this? Just to make sure that it was available in the first place? Could we then not significantly reduce the duration of how long they have to store the blocks / can be challenged?

