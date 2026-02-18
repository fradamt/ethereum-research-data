---
source: ethresearch
topic_id: 20490
title: "Proposal: Delay stateRoot Reference to Increase Throughput and Reduce Latency"
author: _charlienoyes
date: "2024-09-25"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/proposal-delay-stateroot-reference-to-increase-throughput-and-reduce-latency/20490
views: 2019
likes: 40
posts_count: 17
---

# Proposal: Delay stateRoot Reference to Increase Throughput and Reduce Latency

# Proposal: Delay stateRoot Reference to Increase Throughput and Reduce Latency

By: [Charlie Noyes](https://x.com/_charlienoyes), [Max Resnick](https://x.com/MaxResnick1)

## Introduction

Right now, each block header includes a `stateRoot` that represents the state after executing all transactions within that block. This design requires block builders and intermediaries (like MEV-Boost relays) to compute the `stateRoot`, which is computationally intensive and adds significant latency during block production.

This proposal suggests modifying the Ethereum block structure so that the `stateRoot` in block `n` references the state at the beginning of the block (i.e., after executing the transactions in block `n - 1`, rather than the state at the end of the block).

By delaying the `stateRoot` reference by one block, we aim to remove the `stateRoot` calculation from the critical path of block verification at the chain tip, thereby **reducing L1 latency and freeing up capacity to increase L1 throughput.**

## Technical Specification (High-Level)

When validating block `n`, nodes ensure that the `stateRoot` matches the state resulting from executing block `n-1` (i.e., the pre-state root of block `n`).

To be clear, there is no change to exeuction ordering. Transactions in block `n` are still applied to the state resulting from block `n-1`.

## Motivation

`stateRoot` calculation and verification is unnecessary work on the critical path of block production. A builder cannot propose a block on MEV boost without first calculating the `stateRoot` and the attestation committee cannot verify a block without computing the `stateRoot` to compare with the proposed `stateRoot`. `stateRoot` calculation itself accounts for approximately **half** of time spent by all consensus participants working at the tip. Moreover, whatever latency implications the `stateRoot` calculation imposes are paid twice on the critical path: once at the block building stage and then again during verification.

- When block builders submit blocks to relays, they are required to provide the calculated stateRoot. From surveying three of the four largest builders, each spends on average only 40%-50% of their time actually building each block, and the rest on stateRoot calculation.

- When MEV-Boost relays recieve blocks from builders, they are supposed to verify their correctness. In Flashbots’ relay, also approximately half of the ~100ms (p90) verification time is spent on the stateRoot calculation.

- When validators receive a new block, or when non-MEV-Boost validators (“home builders”) produce a block, they are also required to re-verify its execution and its stateRoot. Commodity hardware Reth nodes spend approximately 70% of its time in live-sync on the stateRoot (remainder on execution).

  [![RETH benchmarks](https://ethresear.ch/uploads/default/optimized/3X/a/9/a94d0412f9a5ba4edd2674fa0c9e7227711a7d65_2_690x362.png)RETH benchmarks2130×1118 161 KB](https://ethresear.ch/uploads/default/a94d0412f9a5ba4edd2674fa0c9e7227711a7d65)
  ~70% of RETH's block processing time is spent on `stateRoot` calculation.

These participants - builders, relays, and validators - are highly latency sensitive. They operate under tight timing constraints around slot boundaries (particularly with the [incresaing prevalence of timing games](https://ethresear.ch/t/on-attestations-block-propagation-and-timing-games/20272)).

The latency introduced by `stateRoot` verification at the tip is unnecessary and removing it could allow us to improve the health of the block production pipeline, and network stability.

### Benefits of Delaying the stateRoot

- Higher L1 throughput, because the time currently spent verifying the stateRoot can be re-allocated to execution. stateRoot verification would be pipelined to occur in parallel with the next slot (i.e. during time that nodes are currently idle). Bandwidth requirement increases and state growth would also need to be acceptable before activating a throughput increase.
- Time saved by pipelining the stateRoot could also be allocated towards lowering slot times - improving L1 Ethereum UX, and likely resulting in tighter spreads for users of decentralized exchanges.
- Builders and relays avoid an unnecessary latency speedbump. Both are highly latency-sensitive actors. We want to minimize the sophistication it takes to be a relay or validator. Removing stateRoot latency from the critical path of block verification means they will no longer have to worry about optimizing it, improving the health and efficiency of the block production pipeline.

## Potential Downsides and Concerns

### Impacted Applications

1. Light Clients and SPV Clients

- Impact: These clients rely on the latest stateRoot to verify transactions and account balances without downloading the entire blockchain. A one-block delay introduces a latency in accessing up-to-date state information. Cross-chain communication protocols (like bridges that utilize light clients) would also experience this delay.
- Consideration: We do not see an obvious issue with light clients being delayed by a single block.

1. Stateless Client Protocols

- Impact: Stateless clients rely on the latest stateRoot to verify transaction witnesses. A one-block delay could affect immediate transaction validation.
- Consideration: If these clients can tolerate a one-block delay, the impact may be minimal. This aligns with ongoing discussions in the statelessness roadmap.

## Rationale

### Why This Approach?

- Efficiency: Removing stateRoot computation from the critical path significantly reduces block verification time.
- Simplicity: The change is straightforward in terms of protocol modification, affecting only the placement of the stateRoot reference. This is backwards-compatible with the existing block production pipeline (i.e., native building and MEV-Boost). Other proposals which include execution pipelining, like ePBS, are significantly broader in scope and complexity. Delaying the stateRoot is a simpler change we can make with immediate benefit and little risk.
- Minimal Disruption: While some applications may be affected, we think most (all?) can tolerate a one-block delay without significant issues. We should collect feedback from application developers to validate this.

### Backwards Compatibility and Transition

- Hard Fork Requirement: This change is not backwards compatible and would require a network hard fork.
- Application Adaptations: Affected applications (light clients, Layer 2 solutions, stateless clients) may need to adjust their protocols or implementations.

## Request for Feedback

We invite the community to provide feedback on this proposal, particularly:

- Feasibility: Are there technical challenges that might impede the implementation of this change?
- Upside: How much throughput will we be able to eke out from pipelining stateRoot calculation, and reallocating the time to exeuction?
- Affected Applications: We don’t obviously see a class of widely used applications which would be affected. We hope any developers whose applications do depend on same-block stateRoot will let us know.

## Next Steps

We plan to formalize this proposal into an EIP for potential inclusion in Pectra B.

### Acknowledgements

Thanks to Dan Robinson, Frankie, Robert Miller, and Roman Krasiuk for feedback and input on this proposal.

## Replies

**hdevalence** (2024-09-25):

One thing I’d note is that this design is already used by ABCI/Tendermint, to great success.

Tendermint agrees on the block and hands it off to the application to be executed and committed; the `AppHash` (the Tendermint version of the `stateRoot`) is returned by the application to Tendermint in the `Commit` message and included in the header of the **next** block.

This allows the consensus engine to be cleanly separated from the execution of the application logic it executes, and also allows efficiency improvements. (For instance, in Penumbra, we defer all hashing to the end of the block and then do a single parallelized tree insertion).

I mention this not to have specific reference to Tendermint but just to highlight that this change seems like a conservative adjustment in line with other (technically) successful blockchains, rather than a radical new change.

---

**Bapi-Reddy** (2024-09-25):

Is `stateRoot` computation the major part of computation for block building on other clients as well. As we might be optimising for wrong component if its not similar in other clients for example on geth as well. Where we can find or read more about split of different steps involved in current block building flow ?.

---

**benedictbrady** (2024-09-25):

while we are at it why don’t we just delete the `stateRoot`

---

**potuz** (2024-09-25):

I believe this doesn’t really work without separating the block from the payload. Attesters attest to the block and this consensus information is kept on-chain. If the block is kept with an invalid execution (because attesters no longer attest to execution) then you get free DA on chain. The reason delayed execution works with proposals like EIP 7732 is that the block does not commit to the the stateroot and the payload is not attested at all, so that the payload is not needed to be kept. This way you can delay the validation of the execution until the next slot.

---

**_charlienoyes** (2024-09-25):

> I believe this doesn’t really work without separating the block from the payload. Attesters attest to the block and this consensus information is kept on-chain. If the block is kept with an invalid execution (because attesters no longer attest to execution) then you get free DA on chain. The reason delayed execution works with proposals like EIP 7732 is that the block does not commit to the the stateroot and the payload is not attested at all, so that the payload is not needed to be kept. This way you can delay the validation of the execution until the next slot.

I think that this is not true. Execution validity and state root computation are completely separable.

What happens here is that attesters receive block n, which includes transactions and the pre-stateroot of n (ie the post state root of n-1). If there is an invalid transaction (e.g. which doesn’t pay intrinsic gas), they should not attest to n. Similarly, if the prestate root is wrong, they shouldn’t attest. Either is dishonest behavior.

There is no need to “separate the block from the payload,” I think.

BTW sorry didn’t realize you could edit posts…

---

**potuz** (2024-09-25):

Yeah it seems I confused both optimizations we are proposing, you would still require attesters to validate execution, just not commit to the resulting state root. This does work, I believe it was considered pre-merge even.

---

**benaadams** (2024-09-25):

While I disagree that the state root calculation takes >50% of the block for validators (very much depends on the client); it is still a chunky part of block.

Builders are definitely overcalculating state roots as only one will be included in block and changing the execution payload from `state_root` => `prior_state_root` doesn’t look to decrease any security as consensus would still need to agree the root in the next block.

So while I feel this is mainly a direct benefit to builders than validators (especially with mainnet’s current slot times).

There doesn’t seem to be harm in making `state_root` async; and there is indeed an optionality benefit as faster data structures can be used for block validation that may be also more merkle unfriendly as the whole slot time will be open for merklization (i.e. not critical path).

---

**jacobkaufmann** (2024-09-25):

without a corresponding change to the slot time, proposal/attestation sub-slot time, and/or gas limit, the reduction in block verification time could exacerbate the pre-existing timing games mentioned. in other words, if the protocol does not take advantage of the additional “slack”, then we can reasonably expect other parties to do so.

as you mentioned, the concern with a gas limit increase is a faster rate of state growth.

one item that was not mentioned is the potential for more collaborative block building schemes, which are limited in the current regime because some entity must ultimately execute the aggregate state transition and compute the post-execution state root (e.g. [proposer suffix ILs](https://ethresear.ch/t/how-much-can-we-constrain-builders-without-bringing-back-heavy-burdens-to-proposers/13808#proposer-suffixes-2)).

---

**i-norden** (2024-09-25):

Filecoin also does this as part of their TipSet design that allows for multiple concurrent proposers.

Expect some confusion around whether e.g. a eth_getProofAt(blockHash) request returns a proof for the n-1 stateRoot committed in blockHash n or the n stateRoot proof committed in blockHash n+1.

If an L2 tries to derive from head this would cause problems for them, e.g. a op-stack rollup that has SequencerConfDpeth=0 won’t get a commitment to state in its L1BlockInfo. But that’s a silly thing to do anyways.

Question: is SSF still a long-term goal, and if it is do we still achieve what we want to achieve with it if that single slot doesn’t commit to the state?

---

**malik672** (2024-09-25):

maybe it’s me but the way I’m reading this, it just feels like added complexity that does not really achieve what it should do

my reasons:

1. you are always going to calculate the state root, all you are just doing is simply delaying it
2. overall, we are not making a really big increase in throughput, feels like you are delaying computation instead
3. Nodes aren’t truly “idle” between slots. They’re constantly processing transactions and preparing for the next block.
4. how does this help the ongoing statelessness stuff?

I support this though since builders will propose blocks faster

---

**Giulio2002** (2024-09-25):

I see why this brings benefits. but I do not see if they are worth it:

First of all, The statement that “most of the time is spent on state root” is only correct for Reth and Erigon 2 because they use the same design. In reality, in most clients (included Erigon 3), this will be much smaller.

Secondly, I am not sure what realistically this changes - it seems to me like this gives more time for block builders to build block - however, there is objectively plenty of it already. It is very rare that, unless you run Erigon 2 or Reth, to fall behind the tip of the chain on Ethereum mainnet (due to Erigon 2 not being designed to be efficient on chain tip) . Also, you are just postponing this computation so you are not scaling Ethereum significantly either.

Thirdly, This “Idle” time is not really spent doing nothing, as ELs needs to manage the txpool.

In conclusion, It seems to be a lot of complexity for little benefit.

Perhaps, it would make more sense to have this during in the Verkle hardfork as we will be touching the state root anyway there.

---

**potuz** (2024-09-26):

> While I disagree that the state root calculation takes >50% of the block for validators (very much depends on the client); it is still a chunky part of block.

I believe this optimization is mostly useful for builders, not so much for validators. Builders want to be simulating their blocks as much as possible as far as they can. They need to hash at the very last moment and submit their bids.

Validators on the other hand will not attest until they have completely synced the block, this means DB access, and a series of security measures that need to be committed to disk before attesting. For validators, the state root latency is a much less important optimization compared with the full delayed validation that they get if they **dont** need to validate the payload at all by the attestation deadline.

Having said so, both optimizations can (and most probably should) be applied in parallel. I would disagree that this one proposed here is *enough*, but I think it’s useful nonetheless.

---

**Inspector-Butters** (2024-09-26):

> We do not see an obvious issue with light clients being delayed by a single block.

The light client protocol is already delayed one block by design, since the sync committee signatures point to the previous block.

this proposal would increase that delay to two blocks.

---

**kimroniny** (2024-12-23):

we need external verifications like light client (SPV) or cross-chain, in which the state root is a key commitment to on-chain states

---

**banr1** (2025-01-28):

1. Is my understanding correct that the reason the stateRoot for slot n was included in slot n is because it was carried over from the design of the early PoW era?
2. Even after this is implemented, I understand that the proposer for slot n needs to calculate the stateRoot for slot n and pass it to the proposer for the next slot (n+1) via broadcast. Compared to the traditional approach, how much can the timing of the broadcast be delayed?
3. Thinking very naively, I feel that if shifting by one is possible, perhaps shifting by two might also be feasible. What are your thoughts on this?

---

**kladkogex** (2025-02-02):

Great work!

What troubles me is Denial Of Service security implications of this. If you do not execute a block, then it is not clear to me how you enforce block gas limit. Potentially I can add a transaction with huge gas limit so the block gas limit is crossed.

