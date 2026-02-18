---
source: magicians
topic_id: 20388
title: "RIP-7728: L1SLOAD precompile"
author: icemelon
date: "2024-06-26"
category: RIPs
tags: []
url: https://ethereum-magicians.org/t/rip-7728-l1sload-precompile/20388
views: 2787
likes: 52
posts_count: 35
---

# RIP-7728: L1SLOAD precompile

This proposal introduces a new precompiled contract `L1SLOAD` to L2s that can load storage slots from L1 given a contract address and storage keys. The motivation is to provide a convenient and trustless way for smart contracts deployed on an L2 chain to read storage values from L1. With the `L1SLOAD` precompile, the developers don’t need to generate and submit MPT proofs themselves.



      [github.com/ethereum/RIPs](https://github.com/ethereum/RIPs/pull/27)














####


      `master` ← `icemelon:l1sload`




          opened 08:22AM - 24 Jun 24 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/d/df16d063d1181adc51cf1c8713dc87448fc6e447.jpeg)
            icemelon](https://github.com/icemelon)



          [+121
            -0](https://github.com/ethereum/RIPs/pull/27/files)







This proposal introduces a new precompiled contract `L1SLOAD` to L2s that can lo[…](https://github.com/ethereum/RIPs/pull/27)ad storage slots from L1 given a contract address and storage keys.

## Replies

**FilosofiaCodigo** (2024-07-02):

Being able to query L1 blocks from a precompile is great from the DevEx perspective and also from the end user perspective since it can bring new use cases with fast and cheap transactions.

I noticed that earlier versions of this proposal included the L1 block number as a parameter, but it has now been fixed to the latest block. While this precompile was primarily designed with keystores in mind, reintroducing the block number parameter could unlock additional use cases such as:

1. Snapshots for token governance, whitelists and airdrops. For example: only if you were a holder in a specific time in the past you will be able to vote on a proposal or claim an airdrop
2. ZK merkle inclusion proofs for cross-chain privacy applications. Proving that you have been part of an historic merkle tree can help saving gas because right now we have to store all historic roots in the contracts. So for example this can help saving gas if for example, you are building a L2 voting mechanism for L1 tokens holder, or a mixer where tokens are deposited in L1 and retrieved in L2.
3. 100% on-chain DeFi data to feed financial algorithms. Access to historical block data can feed financial algorithms for DeFi applications. For instance, algorithms could be designed to react to specific market conditions, such as “sell if volatility decreases and price drops.” Projects like Maker and Aave are exploring stuff like this, for example the new Aave V4 proposal expressed the need to include different data points to their fuzzy interest rates.

I like the idea of reintroducing the block number and inviting new ways of saving gas fees. Any thoughts?

---

**toml** (2024-08-13):

[@FilosofiaCodigo](/u/filosofiacodigo) great points! Was thinking the same about providing an optional L1 block number, and you brought up solid usecases.

Should be possible, assuming:

- as per RIP, you will need an archive L1 node for L2 node catch-up,
- the L1SLOAD precompile can receive an optional block number, if none was provided -  fallback to default (i.e. take the latest L1 block known to the L2 sequencer),
- a given L2 can choose to ignore a block height parameter if this is not an important feature to them and they want to avoid having to hold an archive node at all times,
- alternatively, have two different precompiles, e.g. L1SLOAD and L1SLOAD_at_block with the second one being optional (or something similar).

For us it would be an important aspect of `L1SLOAD`. This would make it more generic and would unlock more use cases, without compromising on much.

Happy to hear thoughts!

---

**mralj** (2024-09-24):

Hello everyone!

I’ve been reading through the RIP, and I have couple questions.

In the RIP it is stated:

> Prerequisite 1: The L2 sequencer has access to an L1 node. Given that the sequencer needs to monitor deposit transactions from L1, it already embeds an L1 node inside (preferred) or has access to an L1 PRC endpoint.

> The overhead to L2 sequencers from additional RPC latency
> The L1SLOAD precompile introduces risks of additional RPC latency and intermittent RPC errors. Both risks can be mitigated by running a L1 node in the same cluster as the L2 sequencer. It is preferrable for a L2 operator to run their own L1 node instead of using third party to get better security and reliability. We will perform more benchmarks to quantify the latency overhead in such setting.

**Q1**

I could be missing something, but this prerequisite/overhead is not just for sequencers, it’s for any L2 node. Am I correct? (if so, IMHO, the RIP description should be updated so that mentions of “sequencer” is replaced with eg. “L2 node”).

Which ties to my next question/observation:

**Q2**

Assuming that I was correct, by making `L1SLOAD` accept *any* block number, we would impose requirement of running full archive L1 node on any node which wants to participate in L2 (not just sequencers). Am I correct?

**Q3**

I’m not sure if this is actual problem in practice, ie. was it observed that indeed, most L2 nodes *do* run archive nodes either way, making this issue “non-issue”?

---

**thegaram33** (2024-09-24):

Hi [@mralj](/u/mralj), both your observations are correct. These were briefly discussed during RollCall #6 (slides: [L1SLOAD @ RollCall #6 - Google Slides](https://bit.ly/l1sload-rollcall-6)).

Currently for most rollups it’s possible to run an L2 node without connecting to an L1 node. In this case the node would need to trust the sequencer for any L1-derived info (most importantly deposit transactions), which is not ideal, but possible.

This is in contrast with this RIP. With L1SLOAD follower nodes **must** connect to an L1 node, since the sequencer has no standard way to relay the result of the L1 state reads to other nodes.

I think requiring L2 nodes to connect to an L1 full node is acceptable. But requiring them to connect to an L1 archive node (necessary during initial sync) might make it much more challenging to run a node.

---

**koloz193** (2024-11-18):

could we make this opcode settlement layer agnostic and save it be something like SLSLOAD (settlement layer SLOAD)? i can see some benefits of having this available for L3s on the L2 and then the naming doesn’t make much sense

---

**icemelon** (2024-11-23):

It makes sense. We will take it into consideration and open to better naming. I feel `SLSLOAD` may be confusing to people who don’t have much context.

---

**thegaram33** (2024-12-04):

Here is a wip reference implementation of the current draft spec in rollup-geth: [Implements RIP-7728 by mralj · Pull Request #2 · NethermindEth/rollup-geth · GitHub](https://github.com/NethermindEth/rollup-geth/pull/2) by [@mralj](/u/mralj).

---

**swp0x0** (2024-12-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/thegaram33/48/13347_2.png) thegaram33:

> iring L2 nodes to connect to an L1 full node is acceptable. But requiring them to connect to an L1 archive node (necessary during initial sync) might make it much more challenging to run a node.

Hi sorry, I am bit to late to the party.

Has there been any discussion about generalising this from just a storage read opcode to producing the Base layer’s block hash, which can be used to verify storage reads and other fields in the block header, like the base fee, timestamp and other things?

Also echoing [@koloz193](/u/koloz193)’s sentiment of changing the name to imply the the settlement layer read, maybe `BASE_SLOAD` might be confusing with the base chain tho.

---

**mralj** (2024-12-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/thegaram33/48/13347_2.png) thegaram33:

> I think requiring L2 nodes to connect to an L1 full node is acceptable. But requiring them to connect to an L1 archive node (necessary during initial sync) might make it much more challenging to run a node.

Hey quick question about this, since it was also mentioned during roll-call.

I understand needing archive node during the initial “full sync”.

But what I’m missing is: why is archive node needed during `snap sync`? Or is it issue that L2 nodes are always doing `full sync` (and it indeed wouldn’t be requirement for `snap`)?

---

**thegaram33** (2024-12-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/swp0x0/48/13901_2.png) swp0x0:

> Has there been any discussion about generalising this from just a storage read opcode to producing the Base layer’s block hash, which can be used to verify storage reads and other fields in the block header, like the base fee, timestamp and other things?

Actually that feature is a prerequisite of L1SLOAD.

The L2 needs to have a notion of the latest known L1 block height. The way we implemented this in the [L1SLOAD devnet](https://l1sload.scroll.systems) is that the sequencer relays all L1 block headers to a system contract that verifies that they are chained correctly and stores the L1 block hash in L2 state. (The correctness of this step is later verified as part of the zk proof.)

So yes, this definitely can be used to access other L1 block header fields. But strictly speaking this is not in scope for RIP-7728.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mralj/48/13295_2.png) mralj:

> But what I’m missing is: why is archive node needed during snap sync? Or is it issue that L2 nodes are always doing full sync (and it indeed wouldn’t be requirement for snap)?

No, you are right, it is not needed for snap sync (assuming you can sync up to a very recent block), only for full sync. As an example, Scroll currently does not support snap sync, but it might support it in the future, there is nothing inherent in L2 nodes that would make this impossible.

Edit: But rollups (at least ones that post transaction data to Ethereum) need to be able to reproduce the state root by replaying the posted data, and for this kind of sync (“L1 follower node”) snap sync is not an option.

---

**mralj** (2024-12-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/thegaram33/48/13347_2.png) thegaram33:

> No, you are right, it is not needed for snap sync (assuming you can sync up to a very recent block), only for full sync. As an example, Scroll currently does not support snap sync, but it might support it in the future, there is nothing inherent in L2 nodes that would make this impossible.
>
>
> Edit: But rollups (at least ones that post transaction data to Ethereum) need to be able to reproduce the state root by replaying the posted data, and for this kind of sync (“L1 follower node”) snap sync is not an option.

Thank you very much for explaining this to me!

---

**PatrickAlphaC** (2025-01-24):

Wow, the more I think about this, the more excited I get. As of today, it’s rough how many users/apps need to have a “home base” of some kind. If we could do an `L1SLOAD`, we could have the home base be a one-time L1 cost and then do everything on any L2 without having to “transfer” all the data from the L1 to the L2.

On drawbacks/risks, the main drawbacks outlined in the google slides are around latency, which makes sense. A chain re-org is definitely a bit spooky too.

I’m sort of thinking out loud here, and maybe this is beyond my current knowledge, but would this make decentralizing the sequencer harder? Since a cluster of sequencers could all get different blocks based on latency, and that’s going to become more important with this RIP?

---

**sbacha** (2025-01-26):

How were the gas costs determined? How does this vary per difference in rollup implementation? Based from our assessment from the L1STATICCALL proposal that was under priced in terms of L2 Gas costs, so seeking some evidence to substantiate the values defined in this proposal.

---

**thegaram33** (2025-01-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/patrickalphac/48/7343_2.png) PatrickAlphaC:

> would this make decentralizing the sequencer harder? Since a cluster of sequencers could all get different blocks based on latency, and that’s going to become more important with this RIP?

Yeah, since L1SLOAD is part of the replicated state machine, it is assumed that the L2 has a notion of “latest seen L1 block”. This is not part of this RIP but rather a prerequisite to it.

In our L1SLOAD devnet it is simply the centralized sequencer who relays the L1 headers to L2. This can be done in a fully verifiable manner: We verify the chaining of blocks on L2, and we connect this with the L1 block hash when we submit the validity proof (it is part of the public input).

But you’re right, this relaying of L1 block headers becomes challenging with multiple sequencers, in multiple cases:

- Sequencer relays an incorrect L1 block header
- Sequencer relays a correct L1 block header but with insufficient confirmations
- Local node has a delayed view of L1
- etc.

---

**thegaram33** (2025-01-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sbacha/48/4661_2.png) sbacha:

> How were the gas costs determined? How does this vary per difference in rollup implementation? Based from our assessment from the L1STATICCALL proposal that was under priced in terms of L2 Gas costs, so seeking some evidence to substantiate the values defined in this proposal.

The gas costs in the current draft are placeholders. Would love to hear your input and learnings from L1STATICCALL!

The actual execution cost on the L2 node side is not substantial. These are the operations that we need to factor in:

1. Cost of producing Merkle proofs on the L1 node.
2. Cost of verifying Merkle proofs as part of the rollup validity proof.
3. Latency of querying L1 RPC. It is unclear how we should price in latency. One approach is to estimate the opportunity cost of the sequencer not processing other transactions in the meantime.

---

**sbacha** (2025-01-28):

Scenarios for testing could include:

- simulating a request such that the request is sent in order to reach the maximum possible stack depth, triggering an overflow for the entire block
- Try to reach a stack level where we can perform the maximum number of SLOADs in order to force a state cache data structure to query linearly over caches created at each depth, consuming all gas of block
- observing how requests are handled by forwarded transactions (where the originator of the transaction is sponsored by a relayer/forwarding agent (e.g. GSN)).

Regarding latency, this can be calculated by calculating a transaction fee overhead due to the additional latency in the critical path (we can assume a constant value) and the marginal latency incurred for the call (as you stated) based for unit gas consumed. Then we can derive a p90/p95 probability for inclusion within the next block. This calculated amount is just added to the bribe as additional payment to the builder.

My telegram username is @sambacha if you would like to discuss more very welcome to chat!

---

**wminshew** (2025-01-28):

Is this still an issue w based rollups? [sorry if naive question … still learning]

---

**SanLeo461** (2025-01-29):

There was some discussion earlier in the thread about making L1SLOAD agnostic over exactly which layer it was on, instead just querying 1 layer below; e.g. an L3 querying state of an L2.

Do you think there’s enough value in this idea to also apply it to L1STATICCALL? With static calling, an L3 could call to the L1 via a contract chain. L3 static calls the L2, L2 static calls the L1.

Any ideas on the technical challenges that would be involved with trying to build something like this versus just L1STATICCALL for L2s? My guess is that it wouldn’t be *too* difficult, but I’d love to hear your thoughts or ideas on technical hurdles and any ideas for usecases you might have.

---

**dror** (2025-01-30):

L1SLOAD requires an rpc call into an external L1 node.

The gas cost attempts to reflect that, with a relatively high base fee, and additional marginal cost for extra fetched slots.

But what if the implementation can’t “batch” these calls ?

Consider a bundle of multiple SCA requests that are sent over ERC-4337 call: Each SCA is unaware of the others, and thus each will require a separate L1SLOAD call with one (or few) slots, which on extreme cases would cause the transaction to timeout, and fail inclusion.

**My suggestion**: Extend the `accessList` (EIP-2930) transaction field, to pre-fetch not only EVM state slots but also L1 slots.

The caller of the transaction (a bundler in ERC-4337 model) can collect those slot addresses and add them to the accessList

This requires to redefine the “address” member of the accessList as `{20|21 bytes}`: a 21-byte address (with a prefix “1”) is an L1 address, and a 20-byte normal address is an L2 (current evm state) address.

This format makes it backward compatible to the existing transaction type (at the RLP level)

Note that the L2 node/sequencer could even batch and pre-fetch those L1SLOADs for multiple transactions before evm-executing them.

---

**thegaram33** (2025-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wminshew/48/4658_2.png) wminshew:

> Is this still an issue w based rollups? [sorry if naive question … still learning]

A based rollup could automatically (implicitly) use the previous L1 block hash as the latest known L1 block hash. If the L1 and L2 block proposers are identical, then the previous L1 block hash is known to the block builder, and L2 block inclusion is guaranteed.

My concern would be in these two cases:

1. Permissionless fallback: L1 proposer did not opt in to propose the next L2 block so someone else needs to propose it, inclusion in the next L1 block is not guaranteed.
2. L1 reorgs automatically lead to L2 reorgs.

In these cases, the “latest known L1 block hash” is either not known in advance or might change, which can invalidate preconfs.


*(14 more replies not shown)*
