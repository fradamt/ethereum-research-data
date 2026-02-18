---
source: ethresearch
topic_id: 8802
title: Commit to pre-state instead of post-state on the executable beacon chain
author: dankrad
date: "2021-03-03"
category: The Merge
tags: []
url: https://ethresear.ch/t/commit-to-pre-state-instead-of-post-state-on-the-executable-beacon-chain/8802
views: 4306
likes: 7
posts_count: 10
---

# Commit to pre-state instead of post-state on the executable beacon chain

**TLDR**: By changing the state-root included in the ExecutableData in the [Executable beacon chain](https://ethresear.ch/t/executable-beacon-chain/8271) proposal to the pre-state rather than the post-state, we can get rid of the execution bottleneck in block verification/propagation. This means it is ok for the eth1 payload execution to take several seconds on average, which would degrade the beacon chain in the current (post-state) proposal. This means we can likely increase the block gas limit to 50-100M almost immediately post merge, without any security compromises.

# Introduction

In theory, a Proof of Stake based system should be able to accommodate a longer block execution time than a Proof of Work based system, because it does not need to account for “block jitter”: All blocks are exactly equally spaced in time, so it is ok to exploit that time for execution; whereas the jitter makes a Proof of Work system degrade somewhat already when block execution only requires a fraction of the average block time, because some blocks will arrive earlier.

However, the current [Executable beacon chain](https://ethresear.ch/t/executable-beacon-chain/8271) proposal does not really allow us to make use of this freedom: It requires full execution of the Eth1 payload before it can be decided whether a block is valid. Since validity is a precondition for attesting to a block, and attestations are supposed to be created 1/3 block time (4s) after a block is published, this really does not leave much time for Eth1 payload execution; much more than 0.5s-1s on average will be difficult because it will interfere with block propagation. At 20M gas per second target, this does not leave much room for a gas limit increase post-merge.

Committing to pre-state roots rather than post-state roots has been suggested in the past to improve scalability (e.g. see [Near Sharding Design](https://near.org/papers/nightshade/#state-validity-and-data-availability), section 3.5). It means that Eth1 payload validation will not be necessary at all to validate the current block; it is only necessary to validate the pre-state of the next block, which comes 12s later and thus leaves a lot of time for execution.

I argue that in the current context, we should max out what we can do on the single-sharded EVM and this proposal can, in my prediction, allow us to increase the gas limit 5-10x within weeks of the merge, so in around 12 months. Having this could easily make or break Ethereum, since it will probably be another year or two from then for the effect of full sharding to be felt in gas prices. The proposal also does not depend on any other scaling solutions being deployed and thus benefits even those applications that cannot make use of rollups in the near future.

# Proposal

The executable beacon chain proposal suggests adding the `ExecutableData` data structure to the beacon state:

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

We need to make one change to this data structure: We will remove the `coinbase` variable and just immediately use the proposer validator balance for it (*this is necessary as we will need to be able to charge it; It would be possible to charge to an Eth1 address as well, but would require that all validators maintain a well funded Eth1 address in order to be able to propose blocks (which is very capital inefficient if you only get to propose a block every few weeks). We would need to add a signature that proves that a validator is the owner of the Eth1 address in question*). Further, we will change all variables except for `transactions` to refer to the state at the end of the execution of the *previous* `ExecutableData` block, which we clarify by adding the `pre` keyword:

```python
class NewExecutableData(Container):
    pre_state_root: bytes32
    pre_gas_limit: uint64
    pre_gas_used: uint64
    pre_receipts_root: bytes32
    pre_logs_bloom: ByteList[LOGS_BLOOM_SIZE]
    transactions: [Transaction, MAX_TRANSACTIONS]
```

Validating the `NewExecutableData` means checking that all `pre_` variables have the proposed value after the *previous* block’s `NewExecutableData.transactions` have been executed.

All tips (non-basefee part of gas) are sent directly to the validator’s (Eth2) balance.

## Handling invalid transactions

There are a couple of reasons why a transaction can be invalid in Eth1, and this list may not be exhaustive:

- Invalid signature
- Invalid Nonce
- Not enough balance to pay for gas
- Block gas limit exceeded

Note that this is different from runtime errors, e.g. running out of gas: The latter do not make a transaction invalid, they just revert all state changes except for the gas charged. However, for invalid transactions, we cannot even necessarily charge the sender, since they may not have intended for it to be included or may not be responsible for its failure. So these transactions need to be charged to the proposer instead: The EIP1559 BASEFEE times basic transaction cost (21k gas plus charge per byte used).

This means that there is nothing in `transactions` that can make a block invalid, and thus there is no need to check it before propagating/attesting to a block. Only when building/checking the next block do we need to have executed all transactions.

*Note that, except for the block gas limit, all of these can be checked by the proposer quite cheaply without actually executing the transactions. This suggests that some proposers might get away with composing blocks without executing transactions, and just staying safely below the block gas limit will make sure they won’t be out of pocket*

# Maximum gas limit

There are three limits on how much execution time we can allow with this proposal:

1. The next proposer needs to be able to assemble their own block – they do need enough time for full execution even if they don’t commit to the post-state, as they don’t want to include any invalid transactions
2. We cannot use 100% of the available time between two blocks for execution, otherwise it is literally impossible to ever sync with a chain
3. DOS attacks. But it turns out they are probably more benign overall post-merge, because long execution time will only lead to orphaned beacon blocks, but can still have the same attestation rates; so only throughput will be decreased, but not security.

1 and 2 both lead to a (somewhat aggressive) maximum of targetting a little less than 50% slot time for Eth1 execution. For example, if we did target 5s at 20M gas/s, we could increase the gas limit to 100M gas (50M EIP1559-target), which is a lot more than is possible now. A major downside is that it will obviously make syncing much harder, so it would be essential that good sync protocols are implemented that can yield a state quite close to the tip.

## Replies

**adlerjohn** (2021-03-03):

Doesn’t seem new to me, Tendermint makes use of deferred execution from day 1. For exactly the reason of being able to pipeline block execution during the voting phase. There’s been a lot of discussion from the Tendermint / Cosmos community on this front and the ramifications (i.e. downsides) of deferred execution:



      [github.com/tendermint/tendermint](https://github.com/tendermint/tendermint/issues/7898)












####



        opened 01:57PM - 17 Jun 20 UTC



          closed 12:13AM - 26 Aug 23 UTC



        [![](https://ethresear.ch/uploads/default/original/2X/a/aff0fac7dff35288f32701e6cc0b67152a402bc3.jpeg)
          liamsi](https://github.com/liamsi)





          C:abci


          C:consensus


          S:proposal


          stale







This is a draft (will update shortly):

## Summary

Consider enabling immedi[…]()ate execution (either by default, or, somehow make it possible to chose or overwrite the current behaviour for tendermint users).

## Problem Definition

Currently, tendermint executes transactions one "block height off". Meaning that In the current execution model, blocks are executed against the app only after they are committed.
Full block verification (incl. state) always needs access to transactions of the previous block:

state(1) = InitialState
state(h+1) <- Execute(state(h), ABCIApp, block(h))

While that seem to be fine for most use-cases there are a few draw backs here:

1) First of all it's confusing *why* transactions do not simply get executed in the same block (this is mostly a documentation concern). There is no clear documentation why this decision was made in tendermint. There are a few issues where this was discussed but these discussions are difficult to find and they don't explain the decision well enough.
2) Dealing with one-offs is a classical source of bugs. That is a concern for app or rather SDK module developers. E.g., a dev who was instrumental in designing and implementing the PoS module in the SDK confirmed that "it actually being quite annoying to deal with the +1 offset". This is mostly about developer usability. It also (unnecessarily?) complicates the app centric point of view (ref: https://github.com/tendermint/tendermint/issues/2483).
3) In the context of IBC, for some zones it might be annoying to essentially "wait" an extra block for the state to actually be updated. Not sure if this is a real issue actually. But I can imagine for some projects that waiting a few extra seconds is at least non-optimal.
4) For certain fee models, deferred execution is a burden, or makes them hacky/impossible to implement: https://github.com/lazyledger/lazyledger-core/issues/3#issuecomment-644175000
and https://github.com/lazyledger/lazyledger-core/issues/3#issuecomment-644832152

## Proposal

First, the reasoning behind the current execution model needs to be documented (my understanding is that it is an optimization to reduce latency; s.t. validators can reach consensus on tx ordering quickly and then do the state transitions leisurely while timeout_commit didn't kick in yet). This should be done independent of the proposal to execute earlier.

TODO

### Related:
 - longish discussion over at LazyLedger: https://github.com/lazyledger/lazyledger-core/issues/3
 - https://github.com/tendermint/tendermint/issues/2384
 - app centric interpretation of concepts: https://github.com/tendermint/tendermint/issues/2483
 - invalid/spam tx in blocks (sdk): https://github.com/cosmos/cosmos-sdk/issues/4695
 - also a bit related (block pre-processing phase would happen before the block gets proposed in the immediate exec I guess): https://github.com/tendermint/tendermint/issues/2639
- kinda related discussions on CheckTx: https://github.com/tendermint/tendermint/issues/2384#issuecomment-423359994

____

#### For Admin Use

- [ ] Not duplicate issue
- [ ] Appropriate labels applied
- [ ] Appropriate contributors tagged
- [ ] Contributor assigned/self-assigned












https://github.com/lazyledger/lazyledger-core/issues/3#issuecomment-644175000

Notably, [deferred execution prevents gas refunds as they exist on Ethereum today](https://ethresear.ch/t/the-great-alaskan-transaction-pipeline/8472/11).

On the topic of increasing the block gas limit, block validation rate must be much higher than production rate not for Nakamoto Consensus, but so that users can full sync. [Therefore, changing the consensus protocol does not allow us to decrease this multiplier](https://ethresear.ch/t/increasing-eth-s-gas-limit-what-we-can-safely-do-today/8121/2).

---

**dankrad** (2021-03-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> Doesn’t seem new to me

Did I claim it was new? Quote: “Committing to pre-state roots rather than post-state roots has been suggested in the past to improve scalability (e.g. see [Near Sharding Design](https://near.org/papers/nightshade/#state-validity-and-data-availability), section 3.5).” I haven’t tracked down where this idea first came from.

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> Notably, deferred execution prevents gas refunds as they exist on Ethereum today

This is not true in the model I suggested, where the proposer does execute the transactions (they just don’t add the post state root).

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> On the topic of increasing the block gas limit, block validation rate must be much higher than production rate not for Nakamoto Consensus, but so that users can full sync.

Much higher? Why? If it is 50%, as suggested, then you can still sync. I think we should abandon syncing from genesis for most users. Let’s say you can get the current state and it takes 10h to download it, then you will need another 5h to catch up to the head for a total of 15h sync time. Seems fine.

In the stateless model, of course, syncing can be parallelized, so this is even less of a problem.

Anyway, thanks for the link – most of the arguments are irrelevant IMO (off by one errors can be minimized by very explicit naming, as I suggested above); but one that remains is that, since you don’t commit to the post-state, it won’t be available to other beacon blocks. I think that doesn’t matter in our case, actually:

1. It is (as far as I can think) of minimal or no consequence in the data shard model, where there is no execution on shards
2. When we have execution on (some) shards, we will most likely remove execution from the beacon chain in its own shard. In this case, we will most likely reconsider the execution model, and from what you say, it may be that post-state is the better model then.

---

**adlerjohn** (2021-03-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Did I claim it was new?

[I’m just shitposting for the lulz](https://twitter.com/dankrad/status/1307081652733177858).

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> This is not true in the model I suggested, where the proposer does execute the transactions (they just don’t add the post state root).

You still have the issue of how to meter the block gas limit. If the miner doesn’t make a claim on the amount of gas used per transaction, then you can only allow 12.5M blocks based on the sum of the transactions’ gas limits, *not* the gas used as it is currently. Of course, if you include extra metadata per tx on the amount of gas used…then that’s equivalent to just having a state root.

---

**dankrad** (2021-03-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> You still have the issue of how to meter the block gas limit. If the miner doesn’t make a claim on the amount of gas used per transaction, then you can only allow 12.5M blocks based on the sum of the transactions’ gas limits, not the gas used as it is currently. Of course, if you include extra metadata per tx on the amount of gas used…then that’s equivalent to just having a state root.

Actually we can do it as follows:

- We will first count all the bytes of all transactions in the block, which consume gas according to the number of bytes (currently 16/byte). We store this in GAS_CONSUMED
- Then we will start executing transactions from the top, counting each toward the GAS_CONSUMED. If at any point (also in the middle of executing a transaction), GAS_CONSUMED > BLOCK_GAS_LIMIT, then:

The last transaction is reverted, and the gas it has consumed before it reached the BLOCK_GAS_LIMIT is charged to the proposer
- All remaining transactions are not executed, and their gas according to bytes is charged to the proposer

---

**adlerjohn** (2021-03-04):

Interesting workaround, but it still has an issue: the check for Ethereum data validity must be `proposer_balance >= sum(tx_gas_limit) * base_fee`. This allows miners to prevent the inclusion of any Ethereum data into Serenity by simply making a block where the sum of the transaction gas limits times the base fee is more than 32 (or whatever). Which is trivial to do by making a bunch of txs with a gas limit of 12.5M but that revert immediately.

---

**djrtwo** (2021-03-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> All tips (non-basefee part of gas) are sent directly to the validator’s (Eth2) balance.

I think it’s still simplest to specify and use eth1 coinbase for the collection of such TX fees and not mix layers here. Even if the validator balance is used to pay for invalid TX payloads.

---

**dankrad** (2021-03-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> I think it’s still simplest to specify and use eth1 coinbase for the collection of such TX fees and not mix layers here. Even if the validator balance is used to pay for invalid TX payloads.

You also mix it by giving gains to coinbase and charging losses to the validator balance.

But yeah, there are different options. We can also charge coinbase, but then we have to make sure it’s funded and authenticated.

---

**alonmuroch** (2021-03-09):

Prysm (and I’m sure others) rolled out timely attestation where validators get notified immediately when a block is received.

It will be interesting to measure what is the actual avg time passed from slot start until X% of the committee received the block. That could make the max gas more accurate, e.g. blocks might be received on the 1st/ 2nd seconds of the slot rather than the 3rd/ 4th.

---

**mkalinin** (2021-09-02):

The proposer/builder separation, namely the Idea 1 outlined in this [post](https://ethresear.ch/t/proposer-block-builder-separation-friendly-fee-market-designs/9725) introduces a ternary fork choice rule which in addition has the following status *Block proposal present but bundle body absent*. IMO, this new status can be perfectly combined with this proposal as it helps to get rid of the complexity related to transaction verification. Malformed block body may be deemed *absent*.

Moreover, gossiping the block body *after* the beacon block has been gossiped and received by the builder introduces an additional delay which may affect attesters’ votes. Having additional time for executing the payload will help to mitigate this issue.

