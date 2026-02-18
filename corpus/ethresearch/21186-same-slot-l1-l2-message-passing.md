---
source: ethresearch
topic_id: 21186
title: Same-Slot L1→L2 Message Passing
author: linoscope
date: "2024-12-06"
category: Layer 2
tags: [rollup, based-sequencing]
url: https://ethresear.ch/t/same-slot-l1-l2-message-passing/21186
views: 1437
likes: 18
posts_count: 13
---

# Same-Slot L1→L2 Message Passing

[![image](https://ethresear.ch/uploads/default/optimized/3X/e/d/ed16c6fd28ca34ceace9f2109953769c94f80cd3_2_690x394.jpeg)image1792×1024 183 KB](https://ethresear.ch/uploads/default/ed16c6fd28ca34ceace9f2109953769c94f80cd3)

*Co-authored by [Lin Oshitani](https://x.com/linoscope), [Conor McMenamin](https://x.com/ConorMcMenamin9), [Anshu Jalan](https://x.com/AJ_Jalan), and [Ahmad Bitar](https://x.com/Smartprogrammer), all [Nethermind](https://www.nethermind.io/). Thanks to [Brecht Davos](https://x.com/Brechtpd), [Jeff Walsh](https://x.com/cyberhorsey), and [Daniel Wang](https://twitter.com/daniel_taikoxyz) from [Taiko](https://taiko.xyz/) for their feedback. Feedback is not necessarily an endorsement.*

# Summary

Rollups can import the L1 state root into L2 to facilitate message passing between the two layers, such as user deposits and cross-chain contract calls. However, because the EVM cannot access the state root of the current block, rollups can only pull in state roots from past blocks. This restriction makes it impossible for rollups to process L1→L2 messages within the same slot using the state root alone.

To overcome this limitation, this post introduces a protocol that enables the L2 proposer to selectively inject L1 messages emitted in the same slot directly into L2, bypassing the need to wait for a state root import. By combining this protocol with the L2→L1 withdrawal mechanism discussed in our [previous post](https://ethresear.ch/t/fast-and-slow-l2-l1-withdrawals/21161), users can execute composable L1<>L2 bundles, such as depositing ETH from L1, swapping it for USDC on L2, and withdrawing back to L1—all within a single slot.

# Terminology

We use the terminology from the [Taiko](https://taiko.xyz/) protocol, on which this research is based.

- Messages (a.k.a, Signals): Units of data exchanged between chains to facilitate interoperability, such as transferring tokens or executing cross-chain contract calls. Messages are emitted on the source chain and consumed on the destination chain.
- Same-Slot Messages: Messages emitted in the same slot as the L2 block proposal.
- Message Service Contract: A contract deployed on both L1 and L2 to facilitate message passing between the two layers. Users emit messages in the L1 message service contract and consume them in the L2 message service contract (and vice versa).
- Anchor block: The anchor block is the historical L1 block referenced by an L2 block to import the L1 state root into the L2 environment, effectively “anchoring” the L2 execution to a specific L1 state root. Note that the anchor block must be one slot or more in the past as the EVM does not have access to the current block header.

# The Protocol

Below is a high-level diagram of the protocol:

[![image](https://ethresear.ch/uploads/default/optimized/3X/f/f/ff73da430203794507bc503ea65db6170069075e_2_446x500.png)image1001×1122 100 KB](https://ethresear.ch/uploads/default/ff73da430203794507bc503ea65db6170069075e)

The flow is explained below, with **bolded text highlighting the components newly introduced by this proposal for enabling same-slot message passing**. The non-bolded text follows what is implemented in the current Taiko protocol.

- (A) Users invoke the L1 message service contract to initiate the L1→L2 message transfer.

The messages are hashed and stored in the L1 message service contract.

The L2 proposer:

- (B) Selects which same-slot messages to import into L2.
- (C) Selects the anchor block ID, which is the L1 block ID of the anchor block. This determines which historical L1 block’s state root will be imported into L2.
- (D) Submits the selected same-slot message hashes to the batch inbox contract, the L1 anchor block ID, and the L2 batch to the batch inbox contract.

The batch inbox contract:

- (E) Verify with the L1 message service that the message hashes have been recorded. If the verification fails, the L2 batch proposal is reverted. The messages
- (F) Fetch the L1 anchor state root (block header incorporating the state root to be accurate) of the given L1 anchor block ID via the BLOCKHASH opcode. The anchor block must be at least one slot in the past, as the EVM cannot access the current block header.
- (G) Emit an event containing the message hashes, the L2 batch, and the anchor state root, allowing the L2 execution to access and process them.

The L2 execution will:

- (H) Import the message hashes and the L1 anchor state root into the L2 message contract.
- (I) The batch is executed. L2 transactions in the batch can:

(J-1) Consume the imported same-slot messages by calling the L2 message contract. Note that no Merkle proof is needed in this case, as the message hashes can be stored in a more easily retrievable way in the L2 message contract.
- (J-2) Consume messages emitted in blocks at or before the anchor block ID. Users (or relays acting on their behalf) achieve this by submitting the original message and Merkle proof to the L2 message contract. This proof verifies that the message was emitted on L1 using the anchor state root.

Note that the message service contracts do not provide native replay detection, and it delegates this responsibility to the applications that consume the messages

Next, we will explore the key features of this protocol that shape its design decisions.

## Selective Message Imports

An important feature of this protocol is that L2 proposers can choose which same-slot L1→L2 messages to import into their L2 blocks. This ensures:

- State Determinism: Proposers maintain full control over the post-execution L2 state root of their L2 batch by avoiding unexpected state changes due to unanticipated inbound messages from L1. This is especially important for enabling same-slot message passing even when the L2 proposer is not the L1 proposer/builder.
- Cost Management: Proposers can choose to import only same-slot messages that compensate for the additional L1 gas cost required to process them. Additionally, block proposals will have no gas cost overhead when no same-slot messages are imported.

## Conditioning

Furthermore, note that the batch proposal transaction reverts if the specified same-slot messages were not emitted in L1 (see (C) in the protocol description). This lets the L2 proposer trustlessly condition their L2 batch on the dependent same-slot messages.

# Tying a Loop: L1→L2→L1

Suppose an L1 user wants to deposit ETH from L1, swap it into USDC on L2, and withdraw back to L1—all within the same slot. This can be achieved by combining this proposal with a same-slot L2→L1 withdrawal mechanism we introduced in [Fast (and Slow) L2→L1 Withdrawals](https://ethresear.ch/t/fast-and-slow-l2-l1-withdrawals/21161). Specifically, the L2 proposer can submit an L1 bundle containing the following three transactions:

- An L1 transaction by the user that emits the message for depositing ETH into the L2.
- An L2 batch proposal transaction by the L2 proposer that imports the above deposit message and includes:

The DEX trade by the user that swaps the ETH into USDC.
- The withdrawal transaction by the user that sends the USDC back to L1.

An L1 [solution transaction](https://ethresear.ch/t/fast-and-slow-l2-l1-withdrawals/21161#:~:text=conditions%20of%20Requests.-,Solution,-%3A%20An%20L1%20transaction) by a solver that conducts the withdrawal.

## Are Shared Sequencers/Builders Needed Here?

It’s important to note that the L2 proposer does *not* have to be the L1 builder in the above L1→L2→L1 scenario. That is, a shared sequencer/builder is not needed. What matters is that the bundle is executed atomically—either all transactions in the bundle succeed or the bundle is not included at all. This atomicity can be achieved through builder RPCs like [eth_sendBundle](https://docs.flashbots.net/flashbots-auction/advanced/rpc-endpoint#eth_sendbundle) or via [EIP-7702](https://github.com/ethereum/EIPs/blob/9b44c0d41fd714ccca411d3a7ab7705284fddaa3/EIPS/eip-7702.md) (once implemented), ensuring that the L1→L2→L1 bundle will execute atomically within the same slot. In other words, the L2 proposer does not need to know exactly the L1 state in which the L2 batch is executed. Instead, the L2 proposer just needs to know “enough” L1 state—specifically, the imported same-slot messages—to execute the L2 batch.

This means that there isn’t necessarily a need for the rollup to be “based” in the sense of having a shared sequencer between L1 and L2, which is [one of the value propositions](https://www.reddit.com/r/ethereum/comments/191kke6/comment/kh78s3m/) of based rollups. However, relying on same-slot L1 messages for L2 execution creates a tight coupling between L1 and L2. As a result, the L2 would need to “reorg together” with the L1 during reorganization events. In practice, only based rollups would accept such reorgs.

# Future Directions

## Incentivization

The current protocol does not introduce mechanisms to incentivize the L2 proposers to include and consume same-slot messages. These incentives can be implemented on the L2 execution side. We can introduce features like L2 transactions conditioned on inclusion in specific L2 blocks or those with a “decaying” priority fee. Note that such a feature will also be important to solve the [fair exchange problem](https://ethresear.ch/t/strawmanning-based-preconfirmations/19695#problem-4-fair-exchange-7) for preconfirmations, as both preconfirmations and same-slot message passing aim to incentivize proposers to include transactions early.

## Towards Arbitrary Reads: Taiko Gwyneth

One limitation of this protocol is that the L2 can only read the L1 state of the messaging service contract within the same slot. Can we get reads for *arbitrary* L1 state, not just the message service contract state, to enable more seamless composability between the L1 and L2?

[Gwyneth](https://twitter.com/gwyneth_taiko), a new exciting protocol being developed by the Taiko team, aims to enable such arbitrary same-slot L1 state reads from the L2. An interesting approach under consideration involves introducing a new “introspection precompile” ([EIP-7814](https://github.com/ethereum/EIPs/blob/1676c9451a75fd0740c65e7d1d5f18296d68a9a0/EIPS/eip-7814.md)) that exposes the current transaction trie and opcode counter to the EVM. With this information available, the batch inbox contract can fetch the transaction trie and opcode counter and pass them to the L2 execution. This would enable the L2 to simulate the entire L1 execution up to the batch proposal and compute the middle-of-the-slot L1 state root at the exact opcode counter of the batch proposal.

Read more about Gwyneth’s design [here](https://mirror.xyz/0xeac5Bc2abB5141c1510c18a9637437D49cE71e3F/L2E14JX1wXTytIvMEdmNkX5N4vJpNV-1jCDUyxy5KPg).

# Appendix: Gas Cost

A rough estimate of L1 gas per each same-slot message import is as follows:

- 32 bytes * 16 gas/bytes = 512 gas for the message hash in call data.
- 2600 gas for a function call from inbox to L1 message service. We can batch-call the message service for all messages to share this cost.
- 1 SLOAD = 2100 gas for reading the message hash in the message service

Hence 512 + 2100 = 2612 gas, plus the 2600 gas cost for calling message service shared among the messages. Furthermore, if we enable L2 proposers to free EVM slots of messages they consumed for same-slot inclusion, they can receive a gas refund, compensating for the additional gas cost.

## Replies

**frangio** (2024-12-06):

What is the role of the anchor in this protocol? Does it matter if the latest or an older L1 block is used as anchor?

---

**linoscope** (2024-12-06):

Good question! The anchor is indeed not directly used in the proposed protocol; it’s mainly mentioned to highlight how L1->L2 message passing is currently handled. However, note that the “slow path” L1->L2 message passing, achieved through the anchor state root, serves as a fallback mechanism for the same-slot protocol proposed here. Since anchor blocks are not allowed to lag too much behind the latest L1 block, even if your L1->L2 message isn’t picked up by the L2 proposer in the same slot, it will still eventually be passed to L2 via the anchor state root.

---

**CeciliaZ030** (2024-12-06):

> Gwyneth, a new exciting protocol being developed by the Taiko team, aims to enable such arbitrary same-slot L1 state reads from the L2. An interesting approach under consideration involves introducing a new “introspection precompile” (EIP-7814) that exposes the current transaction trie and opcode counter to the EVM. With this information available, the batch inbox contract can fetch the transaction trie and opcode counter and pass them to the L2 execution.

As a side note to the reader, Gwyneth will probably not use a  ***Message Service Contract*** because we directly access the L1 state root upon introspction, which means **all L1 transactions are equivalently messages** w.r.t the current Taiko design. It also imply that all intermediate L1 states can be “anchored” against. We aim to maximize interoperability to the whole state space / blockspace.

[EIP-7814](https://github.com/ethereum/EIPs/blob/1676c9451a75fd0740c65e7d1d5f18296d68a9a0/EIPS/eip-7814.md) is an elegant solution because it doesn’t involve computing the MPT, instead just exposes the current processed […Tx] to L2. Given that the L2 compute budget is relatively big, the L2 application can compute the desired state (e.g. same-slot deposit) on the fly within the L2 EVM.

---

**otrsk** (2025-01-16):

Interesting.

![](https://ethresear.ch/user_avatar/ethresear.ch/linoscope/48/13681_2.png) linoscope:

> However, relying on same-slot L1 messages for L2 execution creates a tight coupling between L1 and L2. As a result, the L2 would need to “reorg together” with the L1 during reorganization events. In practice, only based rollups would accept such reorgs.

Why would a non-based rollup *not* reorg together with the L1?

---

**linoscope** (2025-01-16):

For non-based rollups with centralized sequencers, the sequencer usually ensures that the L2 state does NOT reorg with the L1. This is done in two ways:

1. If the L1 reorgs and some L2 batches are reorged out, the sequencer ensures that the L2 batches are re-submitted in the exact same order to the L1.
2. The sequencer only picks up L1->L2 messages (deposits, etc) that are in finalized L1 blocks.

On the other hand, based rollups don’t have a centralized sequencer to ensure 1. so their state does reorg together with L1. And since they reorg together with the L1 anyway, they are also willing to pick up non-finalized L1->L2 messages from L1 too.

---

**otrsk** (2025-01-17):

Ok, I see what you mean. However, I want to assume this status quo to be temporary only. **Assuming** that non-based rollups decentralise their sequencers, is there a reason why such rollups would NOT be reorging together with L1 and therefore NOT be compatible with your approach?

(I also acknowledge that it’s a very valuable property not to have to make this assumption with based rollups, BTW).

---

**linoscope** (2025-01-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/otrsk/48/11580_2.png) otrsk:

> Assuming that non-based rollups decentralise their sequencers, is there a reason why such rollups would NOT be reorging together with L1 and therefore NOT be compatible with your approach?

The reason rollups might **choose not to** reorg together with L1 is to ensure a better UX. Once an L2 sequencer (decentralized or not) provides preconfirmations for an L2 transaction (e.g., “Your L2 DEX trade resulted in this amount of tokens”), users expect that preconfirmation to remain valid even if the L1 chain experiences a reorg.

That said, you’re absolutely correct that non-based rollups *can* reorg with L1 if they choose to. However, most non-based rollups avoid this to maintain a good UX, while based rollups inherently must reorg with L1 due to their design.

In summary, there’s a tradeoff:

- Rollups providing L1 reorg resistance cannot import same-slot messages.
- Rollups that do not provide L1 reorg resistance (and are willing to reorg with L1) can import same-slot messages.

---

**alau1218** (2025-01-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/linoscope/48/13681_2.png) linoscope:

> Verify with the L1 message service that the message hashes have been recorded. If the verification fails, the L2 batch proposal is reverted. The messages

Does that mean the ordering is important here? The order of the two transactions has to be first L1 message being recorded into the message service contract, and then the L2 batch proposal.

In order to keep the ordering, we need either the L2 proposer is also the L1 proposer (Based rollup) or we can use eth_sendBundle RPC to batch both L1 messge and L2 batch proposal together to keep the ordering correct.

---

**linoscope** (2025-01-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/alau1218/48/16422_2.png) alau1218:

> Does that mean the ordering is important here?

Yes!

![](https://ethresear.ch/user_avatar/ethresear.ch/alau1218/48/16422_2.png) alau1218:

> In order to keep the ordering, we need either the L2 proposer is also the L1 proposer (Based rollup) or we can use eth_sendBundle RPC to batch both L1 messge and L2 batch proposal together to keep the ordering correct.

And yes to this, too! It’s interesting that, even without a shared sequencer/builder, you can get pretty good composability with simple bundling RPC.

---

**otrsk** (2025-01-27):

Thanks for confirming, this makes sense. Our plan is to be reorging together with the L1 in order to allow for the tight coupling, in spite of starting out with a centralised sequencer. However, I’d expect most of regular user L2 transactions (incl. deposits from L1) to be able to be replayed onto such new `post-L1-reorg-L2-state`, so that the impact on UX under regular conditions should be minimal. Would you agree with this gut feeling?

---

**linoscope** (2025-01-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/otrsk/48/11580_2.png) otrsk:

> However, I’d expect most of regular user L2 transactions (incl. deposits from L1) to be able to be replayed onto such new post-L1-reorg-L2-state, so that the impact on UX under regular conditions should be minimal.

I agree. It’s important to note the large difference between ‘100% final if you trust the sequencer’ and ‘only 99% final even if you trust the sequencer,’ especially for solvers, arbitragers, and similar participants. That said, centralized sequenced L2s willing to reorg with the L1 seem significantly underexplored (and probably underrated) in the design space, especially considering it offers nice UX benefits, such as fast deposits and delayed inboxes with shorter delays. So it’s cool to hear that you’re exploring this approach!

---

**otrsk** (2025-01-28):

Gotcha, and agreed on the 99% caveat. Which might almost be a feature if you’re cynical ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12) But which can also be further mitigated with cryptoeconomics etc. Plus, L1 finality delay improvements would directly benefit such an L2.

