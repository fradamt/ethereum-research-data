---
source: ethresearch
topic_id: 22510
title: "Subcommitments: Off-Chain Finality — Fast, Secure, and Cheap"
author: ranchalp
date: "2025-06-01"
category: Layer 2 > ZK Rollup
tags: [zk-roll-up, data-availability, rollup]
url: https://ethresear.ch/t/subcommitments-off-chain-finality-fast-secure-and-cheap/22510
views: 268
likes: 3
posts_count: 2
---

# Subcommitments: Off-Chain Finality — Fast, Secure, and Cheap

*written by [Alejandro Ranchal-Pedrosa](https://x.com/alranpe).*

*We would like to thank [Luca Donno](https://x.com/donnoh_eth) and [Jonas Theis](https://x.com/jonastheis_) for his thoughtful reviews and comments on an initial draft of this post.*

Rollups achieve incredible scalability by processing transactions off-chain and periodically submitting succinct proofs of correctness to Layer 1 (L1). While this guarantees **fast on-chain finality**—finality verifiable by L1 smart contracts, users increasingly demand **fast off-chain finality**—the confidence that transactions confirmed by the rollup sequencer will not be reverted, even before the data is fully committed and proven on the L1.

## The Challenge of Fast Off-chain Finality

Providing users with fast off-chain finality presents inherent challenges:

- Security concerns: Users relying on rapid confirmations risk double-spend attacks if trusting the sequencer before an irreversible commitment of transaction data is available on L1.
- High data availability (DA) costs: Immediate commitment of transaction data to L1 ensures off-chain finality but significantly increases operational costs.

Thus, current designs couple off-chain finality directly to immediate DA publication, forcing a **trade-off between latency, security, and cost**: security comes at either a high DA cost or high latency.

[![image](https://ethresear.ch/uploads/default/optimized/3X/6/2/62b47a0e17aeb10c42407d3d210c54ac9842c2ea_2_675x500.png)image1424×1054 34.2 KB](https://ethresear.ch/uploads/default/62b47a0e17aeb10c42407d3d210c54ac9842c2ea)

Demand for blobs has been steadily increasing over time, as exemplified in the following chart of number of blobs per day (the recent spike has been motivated by the new 6 blobs target from the pectra upgrade).

[![image](https://ethresear.ch/uploads/default/optimized/3X/d/0/d0f86b9426477a19695695e33a97f795118289a9_2_690x278.png)image1110×448 27.7 KB](https://ethresear.ch/uploads/default/d0f86b9426477a19695695e33a97f795118289a9)

Over time, along with greater demand for throughput in the Ethereum ecosystem, demand for blobs from multiple rollups will continue steadily increasing, and along with them, the price for blobs due to congestion, aggravating the trade-off between DA costs and off-chain finality.

## Introducing Subcommitments

**Subcommitments break this trade-off** by providing fast off-chain finality without having to publish the DA on-chain. Subcommitments are posted additionally to regular, less frequent commitments (which do publish the DA on-chain). Subcommitments carry succinct representations of the L2 ledger, such that users who hold the data locally corresponding to L2 state transition can independently verify them, achieving rapid and secure off-chain finality.

[![image](https://ethresear.ch/uploads/default/optimized/3X/0/a/0aa36922c416f26d15024954df71c2b6f23599ae_2_675x500.png)image1424×1054 61.5 KB](https://ethresear.ch/uploads/default/0aa36922c416f26d15024954df71c2b6f23599ae)

There are **two main benefits** derived from subcommitments thanks to eliminating the trade-off between DA costs, security and latency:

**1. Cheaper transaction fees:**

- Thanks to being able to obtain immediate off-chain finality without having to pay for blobs, DA is now only necessary for on-chain finality. As a result, the sequencer can have flexibility to decide when to commit full data at optimal times, leveraging cheaper blob prices and better data compression (i.e. more transactions in one blob at a time where blob fees are cheaper means cheaper fees per L2 transaction and/or greater margins for the rollup).
- Compression efficiency over several minutes/hours is expected to grow superlinearly in the number of L2 transactions for full transaction data, even more so for most cases if the DA consists of submitting the State Diff.
- This feature is important for zk rollups, as optimistic rollups are under pressure to commit full tx data as soon as possible to start the challenge period as soon as possible and not to further delay on-chain finality, a requirement that does not exist in zk rollups. Subcommitments are thus a new weapon that zk rollups can use to compete in terms of prices with optimistic rollups while obtaining the same latency for off-chain finality and significantly lower for on-chain finality.

**2. Greater security:**

- Users can independently anchor verified states onto L1 (by submitting subcommitments themselves), mitigating reliance on the sequencer or being bound by the default’s off-chain finality frequency of the L2 system. Though this can be done with the appropriate design by users submitting the DA directly, it is unreasonable to ask for this much extra cost on users interested in greater security at lower latency. Subcommitments effectively enable this feature at a reasonable, constant cost, irrespective of the associated DA size of the state transition being anchored.

## How Subcommitments Work

Subcommitments are succinct metadata (typically a cryptographic hash) that uniquely represents an L2 state transition (e.g. the hash of a sequence of L2 blocks). The sequencer submits these subcommitments periodically (e.g., every 30 minutes), significantly more frequently than full DA commitments (e.g. every 12 hours).

Alternatively, the sequencer can also offer subcommitments-as-a-service: by signing to the metadata of a subcommitment and distributing the metadata and signature off-chain, users are free to submit subcommitments signed by the sequencer themselves and obtain even lower latency off-chain finality than offered by default by the system (e.g. an app moving a lot of funds and not trusting the sequencer, wanting to offer their users level of safety and latency they are used to, can decide to subcommit 10 minutes after the previous subcommitments, or 3x faster than the default subcommitment submitted by the sequencer).

**Good case.** As such, the protocol for subcommitments in the good case where the sequencer is honest is the following:

1. Sequencer submits subcommitments periodically, or users submit signed subcommitments distributed and signed off-chain by sequencer.
2. Users observing a subcommitment on L1 and verifying it against their local data can confidently trust the associated off-chain state.
3. Full transaction data commitments and proofs come later, optimized for lower blob fees and better compression.

[![image](https://ethresear.ch/uploads/default/original/3X/5/a/5aacd9c4c24c4c2a71bc5076125a1579b4752df6.png)image915×721 20.1 KB](https://ethresear.ch/uploads/default/5aacd9c4c24c4c2a71bc5076125a1579b4752df6)

**Sequencer’s misbehavior.** Commitments can be used for off-chain finality because they provide guarantees of security even if the sequencer is faulty. As such, for subcommitments to provide off-chain finality, we need to account for the misbehavior of the sequencer. If **the sequencer is faulty, it can corrupt the good case** by either (i) not submitting subcommitments or (ii) submitting incorrect subcommitments (whose data is not available to anyone, or is only available to the sequencer)

If the sequencer does **not submit subcommitments**, then the rollup simply operates at its **usual frequency for commitments**. Similarly, the same mechanisms that are already known to prevent this misbehavior from the sequencer (enforced batches, decentralized commitments, etc.) can be used for subcommitments too.

**If the sequencer submits incorrect subcommitments**, the rollup faces a problem: these faulty subcommitments do not correspond to any transaction data known to anyone other than the sequencer. Because commitments and proofs must match the subcommitments, the rollup cannot proceed until the issue is resolved. This scenario leads to the critical edge case where **subcommitments may need to be reverted**.

**Reverting subcommitments:** To handle incorrect subcommitments, the protocol must define a clear timeout period. If the sequencer fails to commit and prove the state transition within this timeout, the problematic subcommitment can be safely reverted. Under normal conditions, this timeout isn’t reached because proper commitments and proofs are provided promptly.

[![image](https://ethresear.ch/uploads/default/original/3X/a/b/abfa3cf3945a381f49f168e15d3ecc0f89fb27fa.png)image783×459 11.9 KB](https://ethresear.ch/uploads/default/abfa3cf3945a381f49f168e15d3ecc0f89fb27fa)

**Preventing sequencer misuse:** Allowing subcommitments to revert introduces a new risk—malicious sequencers (coordinating with malicious provers) could intentionally revert valid transactions, causing double-spending issues. To address this, the protocol includes a shorter timeout period within which anyone can submit valid commitments and/or proofs. This mechanism ensures that even if the sequencer misbehaves, the network remains secure, and transactions can still reach finality, if the subcommitment was correct. The sequencer may also get slashed an amount of stake if he fails to commit before the decentralized commitment period kicks in, which can be used to subsidize and even reward decentralized committers. Instead of decentralized commitment and proving, enforced mode can also serve as a protection against this attack.

[![image](https://ethresear.ch/uploads/default/original/3X/d/7/d70428b73fc349ca5aab29bc93aa00bbd551aac7.png)image879×629 17.6 KB](https://ethresear.ch/uploads/default/d70428b73fc349ca5aab29bc93aa00bbd551aac7)

This two-tier timeout structure—shorter timeouts for decentralized intervention and longer timeouts for reverting subcommitments—balances security and operational robustness.

## Conclusion

Subcommitments represent a significant improvement in rollup technology by providing zk-rollups with a crucial competitive advantage: the decoupling of DA costs from fast off-chain finality. This innovation enables lower costs, enhanced security, and flexibility, positioning zk-rollups favorably against optimistic alternatives. Ultimately, subcommitments allow users and applications to safely and efficiently leverage the full potential of Ethereum scaling.

## Replies

**bxue-l2** (2025-11-21):

Nice read. I think it is a nice idea that work, it is just reverting subcommitments is a bit messy

