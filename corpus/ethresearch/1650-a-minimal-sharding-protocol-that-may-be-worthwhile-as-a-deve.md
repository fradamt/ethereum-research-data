---
source: ethresearch
topic_id: 1650
title: A minimal sharding protocol that may be worthwhile as a development target now
author: vbuterin
date: "2018-04-07"
category: Sharding
tags: []
url: https://ethresear.ch/t/a-minimal-sharding-protocol-that-may-be-worthwhile-as-a-development-target-now/1650
views: 14325
likes: 33
posts_count: 25
---

# A minimal sharding protocol that may be worthwhile as a development target now

Given the possibility of yet more changes to the sharding 1.1 spec, and developers’ concerns that they are building something that could get changed again, I wanted to offer something that is worthwhile as a development target to shoot for *right now*, and will be on the path toward implementing the final protocol:

1. Anyone can call addHeader(period_id, shard_id, chunks_root) at any time. The first header to get included for a given shard in a given period gets in, all others don’t. This function just emits a log.
2. For every combination of shard and period, N collators (now called “notaries”) are sampled. They try to download the collation body corresponding to any header that was submitted. They can call a function submitVote(period_id, shard_id, chunks_root). This function just emits a log.
3. Clients read logs. If a client sees that in some shard, for some period, a chunk has been included and >= 2N/3 notaries voted for it, it accepts it as part of the canonical chain.

Notice that this protocol is extremely simple, and lacks “notary skin in the game” (slashing conditions that make it risky to vote for collations unless you actually downloaded the full data at that time) but it is under some assumptions a complete protocol, and offers an opportunity to build and test all of the base infrastructure, including:

- The capability of having 100 separate shard p2p networks, and building and sending collations across those networks
- The ability to read logs emitted by an SMC
- The ability to send transactions that call functions of the SMC
- The ability for a client to maintain a database of which collation roots it has downloaded the full body for
- The ability of a validator to (i) log in, (ii) detect that it has been randomly sampled, switch to the right p2p network, and start doing stuff, (iii) log out

## Replies

**terence** (2018-04-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Given the possibility of yet more changes to the sharding 1.1 spec

Is there a write up for the 1.1 spec?

---

**JustinDrake** (2018-04-08):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/aca169/48.png) terence:

> Is there a write up for the 1.1 spec?

I think Vitalik is referring to the [currently written up phase 1 spec](https://ethresear.ch/t/sharding-phase-1-spec/1407).

We’ve made progress on the research side recently which points towards a revamping of the protocol. We have a cleaner proposer-notary separation, an [alternative to windback](https://ethresear.ch/t/a-general-framework-of-overhead-and-finality-time-in-sharding-and-a-proposal/1638), a [stronger availability challenge](https://ethresear.ch/t/extending-skin-in-the-game-of-notarization-with-proofs-of-custody/1639). Some other ideas we are exploring:

- Decoupling collation headers from the main chain, or only explicitly exposing fully notarised collations or checkpoints, maybe using ideas from Dfinity and Bitcoin-NG
- Fork-free proposal chains, and rollback mechanisms
- Variable-size and variable-threshold notarisation
- A new form of signature aggregation
- Strengthened shard finality in case of main chain reorg
- Sidechaining parts of the SMC into a manager shard

In short, the research side of things is in flux. It will probably take a few weeks for ideas to surface on ethresear.ch and for the dust to settle. A new spec (hopefully all round better) may come out in a couple months or so.

The above minimal sharding protocol is a good starting point for implementers. Agreeing on the p2p networking stack (transport layer based on libp2p or otherwise, plus a gossip layer with a channel per shard) seems like a valuable thing to do irrespective of the higher level protocol details.

---

**hwwhww** (2018-04-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> addHeader(period_id, shard_id, chunks_root)

Request for renaming and ordering for consistency:

- addHeader(shard_id, chunk_root, period)

period_id → period
- chunks_root → chunk_root



      [github.com/ethereum/sharding](https://github.com/ethereum/sharding/issues/76)












####



        opened 04:49AM - 08 Apr 18 UTC



          closed 03:27AM - 27 Jul 18 UTC



        [![](https://ethresear.ch/uploads/default/original/3X/d/f/df1ab50a98a1315b77c55c8e7c7c6b37bb91700e.png)
          hwwhww](https://github.com/hwwhww)





          suspended







### What is wrong?
[**Old** sharding spec](https://ethresear.ch/t/sharding-phas[…]()e-1-spec/1407) + [A minimal sharding protocol](https://ethresear.ch/t/a-minimal-sharding-protocol-that-may-be-worthwhile-as-a-development-target-now/1650)

### How can it be fixed
- [x]  "collator" -> "notary"
    * e.g., `COLLATOR_DEPOSIT` -> `NOTARY_DEPOSIT`
- [x] Add constant
	* `COMMITTEE_SIZE` := 135
	* `QUORUM_SIZE` := 90
* Implement notary pool and notary registry:
    - [ ] `register_notary() returns bool`: Adds an entry to `notary_registry`, updates the notary pool (`notary_pool`, `notary_pool_len`, etc.), locks a deposit of size `NOTARY_DEPOSIT`, and returns `True` on success. Checks:
        * Deposit size: `msg.value >= NOTARY_DEPOSIT`
        * Uniqueness: `notary_registry[msg.sender]` does not exist
    - [ ] `deregister_notary() returns bool`: Sets the deregistered period in the `notary_registry` entry, updates the notary pool (`notary_pool`, `notary_pool_len`, etc.), and returns `True` on success. Checks:
        * Authentication: `notary_registry[msg.sender]` exists
    - [ ] `release_natory() returns bool`: Removes an entry from `notary_registry`, releases the notary deposit, and returns `True` on success. Checks:
        * Authentication: `notary_registry[msg.sender]` exists
        * Deregistered: `notary_registry[msg.sender].deregistered != 0`
         * Lockup: `floor(block.number / PERIOD_LENGTH) > notary_registry[msg.sender].deregistered + NOTARY_LOCKUP_LENGTH`
- [x] `add_header(shard_id, chunk_root, period) returns bool`: anyone can call this function at anytime. The first header to get included for a given shard in a given period gets in, all others don’t. Returns `True` on success. This function just emits a log.
    * `HeaderAdded` log (emitted from SMC `add_header` function)
        * v1
        ```python
        shard_id uint256  # pointer to shard
        chunk_root bytes32  # pointer to collation body
        period int128  # (current block number / PERIOD_LENGTH)
        proposer_address address  # the address of proposer
        ```
        * v2 compressed
        ```python
        shard_id bytes1  # pointer to shard
        chunk_root bytes32  # pointer to collation body
        period bytes3  # (current block number / PERIOD_LENGTH)
        proposer_address address  # the address of proposer
        ```

- [x] `get_committee(shard_id, period) returns a list of addresses`:  use the last block hash `h` before this period as the seed. Selecting `notary_pool[sha3(h) % notary_pool_size], notary_pool[sha3(h + 1) % notary_pool_size], .... notary_pool[sha3(h + (COMMITTEE_SIZE - 1)) % notary_pool_size]` notaries from `notary_pool`.
- [ ] `submit_vote(shard_id, chunk_root, period) returns bool`: Sampled notaries call this function to submit vote, returns `True` on success.  This function just emits a log.
    * `Vote` log (emitted from SMC `submit_vote` function)
        * v1
        ```python
        shard_id uint256  # pointer to shard
        chunk_root bytes32 # pointer to collation body
        period int128  # (current block number / PERIOD_LENGTH)
        notary_address address  # the address of notary
        ```
       *  v2 compressed
        ```python
        shard_id bytes1  # pointer to shard
        chunk_root bytes32  # pointer to collation body
        period bytes3  # (current block number / PERIOD_LENGTH)
        notary_address address  # the address of notary
        ```

---

**mhchia** (2018-04-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> For every combination of shard and period, N collators (now called “notaries”) are sampled. They try to download the collation body corresponding to any header that was submitted. They can call a function submitVote(period_id, shard_id, chunks_root). This function just emits a log.

Does this mean we can reuse the `get_eligible_collator` and `collator_pool` in the sharding phase1 spec here?

---

**efynn** (2018-04-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Anyone can call addHeader(period_id, shard_id, chunks_root) at any time. The first header to get included for a given shard in a given period gets in, all others don’t. This function just emits a log.

What’s the purpose of this function? Why can’t `submitVote` be called without it?

For every shard and for every notary member there shoud be a `submitVote` called?

What happens when there are less than N*(2/3) notaries voting for a shard collation?

---

**ChosunOne** (2018-04-08):

It seems like it would be better if there was some intermediary staging before clients tried decoding what the canonical chain is.  Otherwise it might be difficult to read.  Maybe have a canonical headers section of finalized blocks that receive 2N/3 votes?  That way clients don’t need to deal with computing what the canonical chain is.

---

**vbuterin** (2018-04-09):

> What’s the purpose of this function? Why can’t submitVote be called without it?

`addHeader` is there to *propose* headers. `submitVote` is there to submit a vote *approving* a header. The two are different.

> What happens when there are less than N*(2/3) notaries voting for a shard collation?

Then no collation gets accepted in that period.

---

**vbuterin** (2018-04-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/chosunone/48/732_2.png) ChosunOne:

> Maybe have a canonical headers section of finalized blocks that receive 2N/3 votes?  That way clients don’t need to deal with computing what the canonical chain is.

We could move the computation into the SMC itself, and have it emit finalized headers as logs, which would simplify the work of light clients at the cost of requiring more gas.

---

**jannikluhn** (2018-04-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> If a client sees that in some shard, for some period, a chunk has been included and >= 2N/3 notaries voted for it, it accepts it as part of the canonical chain.

I think this should be extended to

> If a client sees that in some shard, for some period, a chunk has been included, >= 2N/3 notaries voted for it and all other accepted headers have a lower period number, it accepts it as part of the canonical chain.

Otherwise it’s possible that a very old chunk that’s been missing just a single vote gets accepted, leading to a huge reorg at the execution layer (or whatever interprets the chunks).

Also, this prevents two chunks being accepted for the same period.

(Unless this is really just supposed to be a placeholder SMC in which case it doesn’t really matter of course.)

---

**stri8ed** (2018-04-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Anyone can call addHeader(period_id, shard_id, chunks_root) at any time

What is the incentive for doing do?

---

**vbuterin** (2018-04-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> Otherwise it’s possible that a very old chunk that’s been missing just a single vote gets accepted, leading to a huge reorg at the execution layer (or whatever interprets the chunks).

Ah, sorry I failed to mention that there’s a time limit for notaries to notarize collations; notarizations for one period have to be submitted before the start of the next period.

---

**nisdas** (2018-04-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Anyone can call addHeader(period_id, shard_id, chunks_root) at any time.

What is the rationale for allowing anyone to call `addHeader` ? Someone could just spam a shard by continuously calling the function and submitting invalid collation headers, thus not allowing any new collations to be added to the canonical shard chain

---

**vbuterin** (2018-04-09):

> What is the rationale for allowing anyone to call addHeader ?

It will almost certainly be replaced, we just don’t know by what yet. Hence why I said “minimal sharding protocol”. It’s there as a stub.

---

**yhirai** (2018-04-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> N collators (now called “notaries”) are sampled.

Can this sampling return different N notaries on different branches of a shard?

---

**yhirai** (2018-04-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> If a client sees that in some shard, for some period, a chunk has been included

What does “included” mean here?  `addHeader()` has been called on the chunk?

---

**yhirai** (2018-04-11):

Now I guess the sampling happens not on the managed shard but somewhere else, so the sampling is not affected by forks and branches of shards.

---

**yhirai** (2018-04-11):

But it sometimes sounds like voting happens in the shard, not somewhere else

> in some shard, … >= 2N/3 notaries voted for it

so, it might be the case, notaries are chosen in the shard, and voting is recorded in the shard.  Different votes are counted on different branches, pointing to different canonical chains.

---

**yhirai** (2018-04-11):

I’m guessing

- it’s never mentioned but there is the main chain
- SMC is deployed on the main chain
- addHeader and sutmitVote are interfaces of SMC (shard management contract?)

---

**hwwhww** (2018-04-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/yhirai/48/153_2.png) yhirai:

> it’s never mentioned but there is the main chain
> SMC is deployed on the main chain
> addHeader and sutmitVote are interfaces of SMC (shard management contract?)

Yes, yes, and yes. ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=12)

---

**vbuterin** (2018-04-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/yhirai/48/153_2.png) yhirai:

> Can this sampling return different N notaries on different branches of a shard?

What’s a “branch of a shard”? There’s no concept of in-shard forking here anymore.

> What does “included” mean here? addHeader() has been called on the chunk?

Yes.

> Now I guess the sampling happens not on the managed shard but somewhere else, so the sampling is not affected by forks and branches of shards.

Yeah, all votes are put on the main chain.


*(4 more replies not shown)*
