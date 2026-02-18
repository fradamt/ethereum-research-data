---
source: ethresearch
topic_id: 8271
title: Executable beacon chain
author: mkalinin
date: "2020-11-26"
category: The Merge
tags: []
url: https://ethresear.ch/t/executable-beacon-chain/8271
views: 25127
likes: 43
posts_count: 39
---

# Executable beacon chain

*Special thanks to [@vbuterin](/u/vbuterin) for the original idea, [@djrtwo](/u/djrtwo), [@zilm](/u/zilm) and others for review and useful inputs.*

**TL; DR** an eth2 execution model alternative to executable shards with support of single execution thread enshrined in the beacon chain.

Recently published [rollup-centric roadmap](https://ethereum-magicians.org/t/a-rollup-centric-ethereum-roadmap/4698) announces data shards as the main scaling factor of execution in eth2 allowing scalability upon a single execution shard and simplifying the overall design.

Eth1 Shard design supposes communication with data shards through the beacon chain. This approach would make sense if Phase 2 with multiple execution shards were going to be rolled out afterwards. With the main focus on rollup-centric roadmap, placing Eth1 on a dedicated shard (that is, independent from and frequently “crosslinked” the beacon chain) puts unnecessary complexity to the consensus layer and increases delays between publishing data on shards and accessing them in eth1.

We propose to get rid of this complexity by embedding eth1 data (transactions, state root, etc) into beacon blocks and obligating beacon proposers to produce executable eth1 data. This enshrines eth1 execution and validity as a first class citizen at the core of the consensus.

## Proposal overview

- Eth1-engine is maintained by each validator in the system.
- When validator is meant to propose a beacon block it asks  eth1-engine to create eth1 data. Eth1 data are then embedded into body of the beacon block that is being produced.
- If eth1 data is invalid, it also invalidates the beacon block carrying it.

## Eth1 engine modifications

According to the previous, Eth1 Shard centric, design, eth1-engine and eth2-client are loosely coupled and communicate via RPC protocol (check [eth1+eth2 client relationship](https://ethresear.ch/t/eth1-eth2-client-relationship/7248) for more details). Eth1-engine keeps maintaining transaction pool and state downloader which requires own network stack. It also should keep storage of eth1 blocks.

Current proposal removes the notion of eht1 block and there are two potentials ways of eth1-engine to handle this change:

- synthetically create eth1 block out of eth1 data carried by beacon block
- modify the engine in a way that eth1 block is not needed for transaction processing and eth1 data is used instead

beacon block roots may be used to keep a notion of the chain which is currently required by state management

The former option looks more short term than the latter one. It allows for faster turn of eth1 clients into eth1-engines and has been proved already by [eth1 shard PoC](http://github.com/txrx-research/eth1-shard-demo).

We use term *executable data* to denote data that includes eth1 state root, list of transactions (including receipts root and bloom filter), coinbase, timestamp, block hashes and all other bits of data required by eth1 state transition function. In the eth2 spec notation it may look as follows:

```python
class ExecutableData(Container):
    coinbase: bytes20  # Eth1 address that collects txs fees
    state_root: bytes32
    gas_limit: uint64
    gas_used: uint64
    transactions: [Transaction, MAX_TRANSACTIONS]
    receipts_root: bytes32
    logs_bloom: ByteList[LOGS_BLOOM_SIZE]
```

A list of eth1-engine responsibilities looks similar to what we used to have for Eth1 Shard. Main observed items of it are:

- Transaction execution. Eth2-client sends an executable data to the eth1-engine. Eth1-engine updates it inner state by processing the data and returns true if consensus checks have been passed and false otherwise. Advanced use cases, like instant deposit processing, may require full transaction receipts in the result as well.
- Transaction pool maintainance. Eth1-engine uses ETH network protocol to propagate and keep track of transactions in the wire. Pending transactions are kept in the mempool and used to create new executable data.
- Executable data creation. Eth2-client sends previous block hash and eth1 state root, coinbase, timestamp and all other information (apart of transaction list) that is required to create executable data. Eth1-engine returns an instance of ExcecutableData.
- State management. Eth1-engine maintains state storage to be able to run eth1 state execution function.

It involves state trie pruning mechanism triggered upon finality which requires state trie versioning based on the chain of beacon blocks.
Note: Long periods of no finality can result in tons of garbage in the storage hence extra disk space consumption.
- When stateless execution and “block creation” is in place eth1 engine may optionally be run as pure state transition function with a bit of responsibility on top of that, i.e. state storage could be disabled reducing requirements to the disk space.

**JSON-RPC support.** It is very important to preserve Ethereum JSON-RPC support for the sake of usability and adoption. This responsibility is going to be shared between eth2-client and eth1-engine as eth1-engine *may* loose the ability to handle a subset of JSON-RPC endpoints on its own, e.g. those calls that are based on block numbers and hashes. This separation is to be figured out later.

## Beacon block processing

`ExecutableData` structure replaces `Eth1Data` in the beacon block body. Also, synchronous processing of the beacon chain and eth1 allows for instant depositing. Therefore, deposits may be removed from beacon block body.

An updated beacon block body:

```python
class ExecutableBeaconBlockBody(Container):
    randao_reveal: BLSSignature
    executable_data: ExecutableData  # Eth1 executable data
    graffiti: Bytes32  # Arbitrary data
    # Operations
    proposer_slashings: List[ProposerSlashing, MAX_PROPOSER_SLASHINGS]
    attester_slashings: List[AttesterSlashing, MAX_ATTESTER_SLASHINGS]
    attestations: List[Attestation, MAX_ATTESTATIONS]
    voluntary_exits: List[SignedVoluntaryExit, MAX_VOLUNTARY_EXITS]
```

We modify `process_block` function in the following way:

```auto
def process_block(state: BeaconState, block: BeaconBlock) -> None:
    process_block_header(state, block)
    process_randao(state, block.body)
    # process_eth1_data(state, block.body) used to be here
    process_operations(state, block.body)
    process_executable_data(state, block.body)
```

It is reasonable to process executable data *after* `process_operations` has been completed as there are many places where operation processing may invalidate entire block. Although, this approach may be suboptimal and leaves a room for client optimizations.

### Accessing beacon state in EVM

We change semantics of `BLOCKHASH` opcode that used to return eth1 block hashes. Instead, it returns beacon block roots. This allows for checking proofs for those data that were included into either beacon state or block starting from `256` slots ago up to the previous slot inclusive.

Asynchronous state read has a major drawback. A client has to wait for a block before it can create a transaction with the proof linked to that block or the state root it produces. Simply speaking, asynchronous state accesses are delayed by a slot at minimum.

#### Direct state access

Suppose, eth1-engine has access to the merkle tree representing entire beacon state. Then EVM may be featured with opcode `READBEACONSTATEDATA(gindex)` providing direct access to any piece of the beacon state. This opcode has a couple of nice properties. First, the complexity of such read depends on `gindex` value and easily computable and hence allows for easy reasoning about the gas price. Second, the size of returned data is 32 bytes which perfectly fits in EVM’s 32-byte word.

With this opcode one may create a higher level library of beacon state accessors providing convenient API for smart contracts. For example:

```auto
v = create_validator_accessor(index) # creates an accessor
v.get_balance() # returns balance of the validator
v.is_slashed()  # returns the value of slashed flag
```

This model gets rid of state access delay. Therefore, with proper ordering of beacon chain operations and eth1 execution (the latter follows the former), crosslinks to slot `N-1` shard data becomes accessible in slot `N`, allowing rollups to prove data inclusion in the fastest possible way.

Also, this approach reduces data and computation complexity of beacon state reads by avoiding the need of proofs that are sent over the wire and further validated by contracts.

*Note:* it might worth making the semantics of `READBEACONSTATEDATA` opcode independent from particular commitment scheme (that is, merkle tree) at the very beginning allowing for easy upgradability.

The cost of direct access increases eth1-engine complexity. Capability of reading beacon state may be implemented in different ways:

- Pass state along with executable data. The main problem of this approach is handling state copies of a big size. It could work if direct access would be restricted to a subset of state data requiring small portion of state to be passed to the execution.
- Duplex communication channel. Having a duplex channel, eth1-engine would be able to ask beacon node for pieces of the state requested by EVM synchronously. Depending on the way the channel is setup, the delays may become a bottleneck for execution of those transactions that have beacon state reads.
- Embedded eth1-engine. If eth1-engine would be embedded into beacon node (e.g. as a shared library) it could read the state from the same memory space via a host function provided by the node.

## Analysis

### Network bandwidth

Current proposal enlarges beacon block by the size of executable data. Though, it potentially removes `Deposit` operation as the proposal allows for advanced depositing schemes.

Depending on the block utilization, expected increase is between [10 and 20](https://docs.google.com/spreadsheets/d/19Tz4wkPmdseBh023Wq2hBYv8Zk6Nrme6d2JkTkRawLE/edit?usp=sharing) percents according to [average eth1 block size](https://etherscan.io/chart/blocksize)  which slightly affects network interface requirements.

It worth noting that if `CALLDATA` is [utilized by rollups](https://medium.com/plasma-group/ethereum-smart-contracts-in-l2-optimistic-rollup-2c1cef2ec537#f432) then eth1 block size may grow up to `200kb` in the worst case (with `12M` gas limit) giving executable beacon block size around `300kb` with `60%` increase.

### Block processing time

Average processing times look as follows:

| Operation | Avg Time*, ms |
| --- | --- |
| Beacon block | 12 |
| Epoch | 64 |
| Ethereum Mainnet Block | 200 |

* *Lighthouse on Toledo with 16K validators and Go-ethereum on Mainnet with 12M gas limit.*

It is difficult to reason about beacon chain processing times, especially, in the case with relatively large validator set and crosslink processing (since shards are rolled out). Perhaps, at some point epoch processing will take near the same time as eth1 execution.

Potential approach of reducing processing times at epoch boundary is to process epoch in advance without waiting for the beginning of the next slot in case when the last block of the epoch arrives in time.

Asynchronous state access model allows for yet another optimization. In this case `process_executable_data` may be run in parallel with the main `process_block` and even `process_epoch` payloads.

### Solidifying the design

One may say that current proposal sets execution model in stone and reduces the ability of introducing more executable shards once we need them.

On the other hand, several executable shards introduces problems like cross shard communication, sharing account space and some others that are not less important and difficult to solve than the expected shift in the execution model.

## Replies

**matt** (2020-11-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkalinin/48/4799_2.png) mkalinin:

> We change semantics of BLOCKHASH opcode that used to return eth1 block hashes.

One concern here is that any contract relying on `BLOCKHASH` will now be broken. Would it be possible to assemble an eth1 block on the fly to return via `BLOCKHASH` and add a new opcode `BEACONBLOCKHASH`?

---

**timbeiko** (2020-11-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkalinin/48/4799_2.png) mkalinin:

> It worth noting that if CALLDATA is utilized by rollups then eth1 block size may grow up to 200kb in the worst case (with 12M gas limit) giving executable beacon block size around 300kb with 60% increase.

Also worth noting that if 1559 ships on mainnet (![:crossed_fingers:](https://ethresear.ch/images/emoji/facebook_messenger/crossed_fingers.png?v=12)), then the maximum would be 2x this.

---

**kladkogex** (2020-11-26):

Interesting proposal!

Some questions:

**Question 1.** Can you explain how to reconcile ETH1 PoW fork choice rule and ETH2 PoS fork choice rule?

![](https://ethresear.ch/user_avatar/ethresear.ch/mkalinin/48/4799_2.png) mkalinin:

> When validator is meant to propose a beacon block it asks eth1-engine to create eth1 data. Eth1 data are then embedded into body of the beacon block that is being produced.

What is exactly meant by " asks eth1-engine to create eth1 data."

If there is later a re-org on ETH1, the data on the ETH2 chain will become invalid.

Or are you going to wait for a very long time to make sure there is no re-org on ETH1?

Also, what are two ETH2 clients supposed to do if they see different winning branches on ETH1?

If there is fork of ETH1

**Question 2:** If there is a fork on ETH1 similar to the one that happened last month,  what is going to happen to the beacon chain then?

---

**mkalinin** (2020-11-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/matt/48/4560_2.png) matt:

> One concern here is that any contract relying on BLOCKHASH will now be broken. Would it be possible to assemble an eth1 block on the fly to return via BLOCKHASH and add a new opcode BEACONBLOCKHASH ?

This is worth checking. But I assumed that swapping one hash with another won’t change the semantics in a way that it breaks existing smart contracts. Is there any particular cases that you have in mind?

---

**dabasov** (2020-11-26):

seems like we won’t have separate shard for ETH1 anymore, it will be merged with beacon chain and no separate consensus mechanism for it will exist.

![](https://ethresear.ch/user_avatar/ethresear.ch/mkalinin/48/4799_2.png) mkalinin:

> We propose to get rid of this complexity by embedding eth1 data (transactions, state root, etc) into beacon blocks and obligating beacon proposers to produce executable eth1 data. This enshrines eth1 execution and validity as a first class citizen at the core of the consensus.

---

**JustinDrake** (2020-11-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkalinin/48/4799_2.png) mkalinin:

> if Phase 2 with multiple execution shards were going to be rolled out afterwards

Phase 2 is still on the table. The “rollup-centric roadmap” is a short- and medium-term roadmap (say, for 2021 and 2022). It is not a long-term roadmap.

![](https://ethresear.ch/user_avatar/ethresear.ch/mkalinin/48/4799_2.png) mkalinin:

> If eth1 data is invalid, it also invalidates the beacon block carrying it

This would require validators to run an Eth1 full node to validate. This goes against the design goal of allowing validators to run on cheap hardware (e.g. entry-level laptops, NUCs, Raspberry Pis, phones, etc.). This is especially relevant for validators that are staking a small amount of ETH through an m-of-n pooled validator.

![](https://ethresear.ch/user_avatar/ethresear.ch/mkalinin/48/4799_2.png) mkalinin:

> We change semantics of BLOCKHASH opcode that used to return eth1 block hashes. Instead, it returns beacon block roots.

The beacon block roots are extremely malleable making them unusable as a source of randomness, hence unusable for Eth1 dApps (and other infrastructure) that use the `BLOCKHASH` as a source of randomness. A possible fix for this use case is to make `BLOCKHASH` return the relevant RANDAO mix.

However, as mentioned by [@matt](/u/matt), we also need to cater for Eth1 dApps (and other infrastructure) that use `BLOCKHASH` to authenticate Eth1 headers and bodies. I’m not sure how to modify `BLOCKHASH` to reconcile both use cases (randomness and authentication).

---

**dankrad** (2020-11-26):

Excellent proposal. This gives us a way to merge Eth1 and Eth2 even before statelessness has been achieved (though it would be better with statelessness).

![](https://ethresear.ch/user_avatar/ethresear.ch/mkalinin/48/4799_2.png) mkalinin:

> Suppose, eth1-engine has access to the merkle tree representing entire beacon state. Then EVM may be featured with opcode READBEACONSTATEDATA(gindex) providing direct access to any piece of the beacon state. This opcode has a couple of nice properties. First, the complexity of such read depends on gindex value and easily computable and hence allows for easy reasoning about the gas price. Second, the size of returned data is 32 bytes which perfectly fits in EVM’s 32-byte word.

I think we should provide access through a more semantic data structure rather than using a generalized index. The generalized index would severely limit upgradability of beacon chain data structures.

---

**zilm** (2020-11-26):

Excellent proposal! I have 2 questions:

1. Making a sync BeaconState access API today could we support it tomorrow when/if we have several execution shards? Async looks safer for me even if it’s possible to make it sync in the near term.
2. As noted above, we want to go stateless in the middle-long term. How could eth1 engine be incentivized and verified as a separate actor in the future?

---

**vbuterin** (2020-11-26):

Great work!

I am definitely worried about the idea of synchronous interaction between eth1 execution and the beacon chain. The reason is that using synchronous interaction, while simpler, permanently enshrines the requirement that verifying an eth2 block requires running the corresponding eth1 execution. It excludes alternatives like allowing eth2 nodes to be stateless clients of eth1 and only verify the eth1 side if they are part of an assigned committee, for example (and it would also exclude the possibility of migrating eth1 to a shard further down the road).

So even if executable data is directly inside beacon blocks I’d be inclined to favor keeping the communication between the executable data and the beacon chain logic fully asynchronous.

---

**edmundedgar** (2020-11-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkalinin/48/4799_2.png) mkalinin:

> This is worth checking. But I assumed that swapping one hash with another won’t change the semantics in a way that it breaks existing smart contracts. Is there any particular cases that you have in mind?

Previously people have discussed using the block hash in contracts to prove the existence of previous event logs, see this discussion:



      [ethereum.stackexchange.com](https://ethereum.stackexchange.com/questions/16117/proving-the-existence-of-logs-to-the-blockchain)



      [![Nate Rush](https://ethresear.ch/uploads/default/original/3X/9/9/992d19c82812f7a4c405ff4806dee5fe27022699.png)](https://ethereum.stackexchange.com/users/5635/nate-rush)

####

  **events, logs, merkle-patricia-tries, receipts**

  asked by

  [Nate Rush](https://ethereum.stackexchange.com/users/5635/nate-rush)
  on [09:41PM - 12 May 17 UTC](https://ethereum.stackexchange.com/questions/16117/proving-the-existence-of-logs-to-the-blockchain)










…which includes a couple of people’s POC implementations:



      [github.com](https://github.com/PISAresearch/event-proofs)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/0/c/0cb00818b957c8243c0e3ec35d63c3dafd51bce7_2_690x344.png)



###



Solidity proofs that a historical event occurred












      [github.com/figs999/Ethereum](https://github.com/figs999/Ethereum/blob/1eeb246d02067bf356a59ffeff2298aca9874b79/EventStorage.sol)





####

  [1eeb246d0](https://github.com/figs999/Ethereum/blob/1eeb246d02067bf356a59ffeff2298aca9874b79/EventStorage.sol)



```sol
pragma solidity ^0.4.19;

contract EventStorage {

/*
Author: Chance Santana-Wees
Contact Email: figs999@gmail.com

This contract code has not been fully audited. DO NOT CONSIDER THIS PRODUCTION READY CODE!!!

This is a proof of concept for reduced gas cost verifiable data storage which uses event logs to store data on chain.
By having a client pass a block header along with the event payload into the ValidateEventStorage method, the contract
can decode and validate the block header, then search the block header's bloom filter for the event payload. This allows
the contract to verify the existence of the logged data.

In theory, this can allow for a significant reduction in gas cost when storing large byte arrays on chain while still
allowing a contract to work with the stored data. Via this method, it should be possible to store and validate the existence of
data blobs several kilobytes in size, far beyond what is possible with SSTORE due to block gas limits.

Below is comparative theoretical gas costs of various storage operations. "HashedEventStorage" refers to using the same method as
```

  This file has been truncated. [show original](https://github.com/figs999/Ethereum/blob/1eeb246d02067bf356a59ffeff2298aca9874b79/EventStorage.sol)










This obviously relies on whatever is returned by `BLOCKHASH` hashing a header with the same structure as currently, but certain parts of it could be replaced - for instance, you might want to replace the nonce with a random number from Randao.

I don’t know whether anything like this was ever used in production, beyond proving that it could be done, or whether it’s still expected to work. “Eth1 block headers will never change” doesn’t really feel like a reasonable thing to assume, but maybe somebody assumed it.

---

**kladkogex** (2020-11-27):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/d/8baadc/48.png) dabasov:

> seems like we won’t have separate shard for ETH1 anymore, it will be merged with beacon chain and no separate consensus mechanism for it will exist.

Well, I think **if this is a direction**, the beacon chain needs to run for a while **to prove stability**, and I am not sure this can be done in 2021, because some people may need more time. Most complex software products take years to polish and fix bugs.

Weakly coupling ETH1 & ETH2 in 2021 is realistic in IMO.

On the other hand forcefully killing ETH1 PoW consensus in 2021 would be scary for many people.

People in general like to have an option to do something and not be forced to do something.  Giving people an option to move ETH1 tokens to ETH2 is better than telling them that the old thing stops and everyone needs to move to the new one.

If I were an investor keeping my money on PoW and someone would tell me that the PoW chain is going to be terminated, say on June 1, 2021,  and I would be moved to the PoS chain, I would start worrying, because I do not know how stable the new thing is.

I would like it much more if the old one keeps running and I am given an option to move my funds to the new one.

To summarize, the optimal solution imo is to somehow embed ETH1 merkle roots into ETH2 blocks and ETH2 merkle roots into ETH1 so the funds can go back in forth.

The simplest way to do it is probably to introduce a long delay to make sure the state is finalized on the source chain before funds are moved to the destination chain.

Then, in particular, ETH2 can flow back into ETH1 slowly but surely.

---

**mkalinin** (2020-11-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Phase 2 is still on the table.

Perhaps, the wording regarding Phase2 is confusing. The assumption is that rollup-centric roadmap makes eth1 as the only execution thread for a longer period than it was previously planned with Phase2. The option of scaling the execution on L1 is not excluded by this proposal.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> This would require validators to run an Eth1 full node to validate.

Right, but what if there is eth1 nodes market that provides access to eth1 state transition and block production for Tx fees? We may think of centralisation risk here but eth1 Tx fees could be enough for relatively high number of independent parties to run their own nodes and provide such a service mitigating the risk.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> The beacon block roots are extremely malleable making them unusable as a source of randomness, hence unusable for Eth1 dApps (and other infrastructure) that use the BLOCKHASH as a source of randomness. A possible fix for this use case is to make BLOCKHASH return the relevant RANDAO mix.

This is a good point! I agree with you and [@matt](/u/matt) that we *can’t* change the semantics of `BLOCKHASH` and rather introduce a `BEACONBLOCKROOT` opcode for proofs verification. Preserving `BLOCKHASH` semantics addressing both, randomness and blocks identity, is an open question.

---

**mkalinin** (2020-11-27):

It definitely need to prove stability. And executable beacon chain will highly likely not happen in 2021. Technically with eth2 light client contract on eth1 some of the use cases that require bi-directional communication becomes possible.

---

**kladkogex** (2020-11-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> This would require validators to run an Eth1 full node to validate

Well I am a bit confused now …

Why does one need to run a full PoW node if the PoW consensus is no longer valid?

My understanding that you would need to either add EVM and the historic ETH1 state to ETH2 clients, or run and ETH1 node in parallel to ETH2  node, but only the part of it that does EVM, not  PoW consensus …

---

**mkalinin** (2020-11-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> I think we should provide access through a more semantic data structure rather than using a generalized index. The generalized index would severely limit upgradability of beacon chain data structures.

Good point! This restriction is addressed by the following note:

![](https://ethresear.ch/user_avatar/ethresear.ch/mkalinin/48/4799_2.png) mkalinin:

> Note: it might worth making the semantics of READBEACONSTATEDATA opcode independent from particular commitment scheme (that is, merkle tree) at the very beginning allowing for easy upgradability.

---

**mkalinin** (2020-11-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/zilm/48/4876_2.png) zilm:

> Making a sync BeaconState access API today could we support it tomorrow when/if we have several execution shards?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> It excludes alternatives like allowing eth2 nodes to be stateless clients of eth1 and only verify the eth1 side if they are part of an assigned committee, for example (and it would also exclude the possibility of migrating eth1 to a shard further down the road).

I totally agree with these points! Tight coupling eth1 and eth2 by synchronous state accesses puts a big restrictions on upgradability. Making such a change requires a clear path towards execution scalability and we definitely should use less restrictive asynchronous model, at least at the beginning.

---

**mkalinin** (2020-11-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/edmundedgar/48/2287_2.png) edmundedgar:

> for instance, you might want to replace the nonce with a random number from Randao.

This is probably a good path to follow. RANDAO mix is embedded into eth1 block header (into extra data field or whatever else) by eth1-engine. Eth1 block execution takes `200ms` in average which restricts the number of potential re-rolling the dice attempts by introducing a risk of loosing proposer reward and hence transaction fees if block is not propagated in time.

---

**edmundedgar** (2020-11-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkalinin/48/4799_2.png) mkalinin:

> RANDAO mix is embedded into eth1 block header (into extra data field or whatever else) by eth1-engine. Eth1 block execution takes 200ms in average which restricts the number of potential re-rolling the dice attempts by introducing a risk of loosing proposer reward and hence transaction fees if block is not propagated in time.

Come to think of it I’m not sure this works - Couldn’t a validator bias the randomness of the block hash after getting the randao number by grinding any other part of the header that isn’t part of the block execution? (Or do something at the end of the block after the 200ms?)

If so then it seems like you have to choose between just replacing the block hash with a random number, which preserves the use of the block hash for contracts that use it as a ghetto (moderately expensive-to-bias) random number generator, and preserving its use for already-deployed existing contracts that want to prove things about the block.

---

**mkalinin** (2020-11-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/edmundedgar/48/2287_2.png) edmundedgar:

> Come to think of it I’m not sure this works - Couldn’t a validator bias the randomness of the block hash after getting the randao number by grinding any other part of the header that isn’t part of the block execution? (Or do something at the end of the block after the 200ms?)

We can avoid this by including eth1 block hash onchain and validating that unused fields are e.g. filled with zeros.  Though, `coinbase` can be manipulated in any case.

---

**djrtwo** (2020-11-27):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Why does one need to run a full PoW node if the PoW consensus is no longer valid?

He means run eth1 state and tx verification, but with the the consensus driven by the beacon chain.

The software architecture of this might very well look like an eth2 client and portions of an eth1 client (often called an eth1-engine) running adjunct on the same system, where the eth2-client drives consensus and the eth1-engine handles user layer validity (state, txs, etc).

See this post for a high level on the division of concerns – [Eth1+eth2 client relationship](https://ethresear.ch/t/eth1-eth2-client-relationship/7248)


*(18 more replies not shown)*
