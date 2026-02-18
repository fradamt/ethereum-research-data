---
source: ethresearch
topic_id: 22011
title: "Nexus: A Based Sequencing Layer for L2s"
author: irfanshaik11
date: "2025-03-27"
category: Layer 2
tags: []
url: https://ethresear.ch/t/nexus-a-based-sequencing-layer-for-l2s/22011
views: 437
likes: 8
posts_count: 1
---

# Nexus: A Based Sequencing Layer for L2s

# Nexus: A Based Sequencing Layer for L2s

Authored by [Sattvik](https://x.com/sattvikkansal) & [Anil](https://x.com/anilkumarRome) from [Rome](https://x.com/RomeProtocol), review from [Domothy](https://x.com/domothy) & [Irfan](https://x.com/i_shaix) from [Interstate](https://x.com/interstatefdn).

## Summary

We introduce [Rome’s Nexus](https://docs.rome.builders/nexus-romes-based-sequencer): Using an alt-L1 (Solana) with faster block times as a based sequencing layer that settles to Ethereum

We present an implementation of Ethereum L2s using the validators of a different Layer 1 blockchain (Solana) as the sequencer, while otherwise using Ethereum L1 for everything else: settlement, data availability, deposits/withdrawals, and later forced inclusion.

## Context

As per the [seminary ethresearch post](https://ethresear.ch/t/based-rollups-superpowers-from-l1-sequencing/15016) on based rollups, a rollup is said to be based if it employs Ethereum L1 proposers (and indirectly searchers and block builders) for the task of sequencing L2 transactions. The benefits and drawbacks are discussed in [the initial based rollup research post](https://ethresear.ch/t/based-rollups-superpowers-from-l1-sequencing/15016) on the subject.

The main drawback of based sequencing addressed here is that the based rollup’s blocktime becomes coupled with the L1’s, which in the case of Ethereum is currently 12 seconds per slot. The consequences of this constraint can be remedied by some preconfirmation mechanism, which comes with more engineering effort and design choices.

We argue that a simpler solution for permissionless, decentralized *and* fast mechanism is to use the validators of a different blockchain that optimizes for fast blocks (e.g. Solana) as sequencers for L2 transactions.

## Pros and cons

**Advantages:**

- All of the advantages of based sequencing listed here
- Inherits Solana’s high speed, throughput, low cost, security ($52B staked SOL as of Mar 26, 2025), decentralization (1300 validators), and well-tested infrastructure
- Atomic composability between Based L2s and Solana. Async composability between Ethereum and Solana transactions
- Dual DA on Solana and Ethereum. Eth L2s and contracts can access Solana state on Ethereum chain, and Solana L2s and contracts can access Eth state on Solana chain
- It is effectively a shared sequencer infrastructure “for free” – contingent on the L1’s security properties

**Disadvantages:**

- Sequencer weakest link: Reliance on an external blockchain’s validators for sequencer liveness
- MEV leaks to the altL1 rather than Ethereum (note that this is neutral from the perspective of the L2, as employing based sequencing means foregoing MEV revenue anyway)

## Proposed Workflow & Implementation

Using components like op-node, rhea, hercules, op-proposer, op-batcher, and rome-evm, we can achieve an Ethereum L2 which uses Solana for sequencing but Ethereum for everything else.

The transaction flow is outlined below:

[![Nexus](https://ethresear.ch/uploads/default/optimized/3X/1/9/190ceb45ff42d8a271192c050c319425519f5255_2_690x255.jpeg)Nexus5440×2017 506 KB](https://ethresear.ch/uploads/default/190ceb45ff42d8a271192c050c319425519f5255)

### Depositing Funds

1. User submits a deposit transaction to Ethereum to bridge ETH to L2.
2. op-node reads the finalized deposit transaction from Ethereum and executes it on the L2 Rome EVM contract to make ETH available to the user.

### L2 Transaction Submission

1. User submits L2 transaction to op-geth.
2. Rhea reads L2 transactions from op-geth mempool.
3. Rhea submits L2 transactions to Solana for sequencing.

### Solana Sequencing

1. Hercules reads Solana blocks relevant to the Rome EVM contract.
2. Hercules creates op-node compatible L2 sequencer batches (blocks) from Solana blocks and stores them into Postgres.
3. op-node queries Hercules for L2 sequencer batches and appends them to op-geth.

### Monitoring Ethereum Finality

1. op-node reads finalized Ethereum blocks.
2. op-node confirms L2 blocks based on finalized Ethereum blocks, marking them first as safe and then as finalized.

### Posting tx batches to Ethereum via Interstate preconfirmation

1. op-batcher periodically gets sync status from op-node.
2. op-batcher gets unsafe L2 blocks from op-geth.
3. op-batcher writes these L2 sequencer batches to Ethereum Batch Inbox address. Submits tx to Interstate for preconfirmation.

### State commit to Ethereum via Interstate preconfirmation

1. op-proposer periodically queries op-node for output root. op-node in turn queries op-geth for state root.
2. op-proposer posts output root to the Ethereum L2OutputOracle contract.

Submits transaction to Interstate for preconfirmation. The batches & state root written to Ethereum are preconfirmed when available. Else written as normal transactions to L1.

### Withdrawal Flow

[![Withdrawals](https://ethresear.ch/uploads/default/optimized/3X/4/a/4a08710e7ea4fa4fc938fb6fc2029313feca3724_2_690x288.jpeg)Withdrawals4754×1990 456 KB](https://ethresear.ch/uploads/default/4a08710e7ea4fa4fc938fb6fc2029313feca3724)

Note: Relying on preconfirmation for withdrawal requires sufficient collateral by the preconfer to compensate for funds loss. This design indicates ideal end state with the understanding that preconfirmations must have sufficient collateral before being relied on for bridging. We can even use a ‘fast-withdrawal’ for lower value transactions and enforce that higher value transactions go through slower withdrawal queue.

## Open questions

- How to minimize state divergence due to different EVMs (Rome EVM v/s OP Geth EVM) and block-production logic? Compare hash of impacted accounts on OP Geth and Rome EVM for each tx. Timestamp and blockhash are also part of the state. Also, how to have the correct state root? OP Geth state root different is from Rome EVM root.
- How to deal with the same timestamp for different L2 blocks? Does it impact proofs?

## Conclusion

We have presented a novel approach to L2 sequencing that leverages the fast block times of alternative L1s such as Solana while maintaining settlement security on Ethereum. This hybrid architecture offers the benefits of based sequencing without requiring complex preconfirmation mechanisms, effectively providing shared sequencer infrastructure at no additional cost.

While this approach introduces some tradeoffs – particularly around sequencer dependency – our working implementation demonstrates its technical feasibility. Several open questions remain around fast finality, state consistency, and technical implementation details that need to be resolved before production deployment.

This architecture represents an interesting exploration of cross-chain collaboration that could enable faster, more efficient L2 solutions while maintaining the security guarantees that make Ethereum valuable as a settlement layer.
