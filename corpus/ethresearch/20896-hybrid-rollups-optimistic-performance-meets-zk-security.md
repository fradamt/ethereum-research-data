---
source: ethresearch
topic_id: 20896
title: "Hybrid Rollups: Optimistic Performance meets ZK Security"
author: 14mp4rd
date: "2024-10-30"
category: Layer 2 > ZK Rollup
tags: [zkop-rollup]
url: https://ethresear.ch/t/hybrid-rollups-optimistic-performance-meets-zk-security/20896
views: 724
likes: 4
posts_count: 1
---

# Hybrid Rollups: Optimistic Performance meets ZK Security

*Special thanks to [Sam Battenally](https://x.com/sam_battenally), [Hai Nguyen](https://ethresear.ch/u/hai-rise/summary), [Succinct Labs](https://www.succinct.xyz/), and [Norswap](https://norswap.com/) for feedbacks and reviews.*

# Motivation

Many high-performance rollups adopted an optimistic design in the first place. This was primarily driven by the simplicity of the optimistic approach and the limitations of zero-knowledge (ZK) proving technology. At that time, simulating an EVM machine with ZK was not feasible, and ZK proving was unable to meet the desired throughput demands. Optimistic rollups, on the other hand, offered a simpler and more scalable solution.

However, the optimistic approach has its drawbacks. To maintain security, it must rely on fraud challenges. The current fraud challenge process can be complex and time-consuming, requiring significant interactions or unfriendly to challengers.

With recent advancements in the ZK ecosystem, we are now able to prove an EVM block in an order of minutes. This article explores the possibility of transitioning to a hybrid rollup model that combines the best aspects of both optimistic and ZK rollups to address the limitations of each.

## Summary

Here’s a comprehensive overview of the key properties.

- Optimistic Foundation with ZK Security. At its core, a hybrid rollup operates like an optimistic rollup, but incorporates ZK validity proofs for enhanced security. This unique combination allows for high throughput while maintaining robust security measures.

- Efficient Challenge Mechanism. In the event of a disputed transaction, the system employs ZK validity proofs. The hybrid design is more straightforward and has been shown to be robust in various ZK rollup implementations, offering a higher degree of reliability compared to complex fraud proof systems.
- Cost-Effective. The hybrid model maintains the cost-effectiveness of optimistic rollups for end-users. Under normal circumstances, users do not bear the cost of generating validity proofs, keeping transaction fees competitive. Furthermore, operational costs also stay low in the case of low-to-no traffic.
- Balancing Performance and Security. By leveraging the high throughput capabilities of optimistic rollups and the security assurances of ZK proofs, the hybrid design achieves a balance that caters to both performance needs and security requirements.
- Flexible Proving Strategy. The system only generates ZK proofs when challenges occur, reducing the computational overhead associated with constant proof generation in full ZK rollups.
- Transitional Technology. The hybrid design serves as a stepping stone towards a full ZK rollup implementation. It allows rollups to gradually adapt to advancements in ZK technology while maintaining current operational efficiency.

## Optimistic vs ZK Rollups

Anyone can examine the data on a rollup and spot any mistakes. If even one person finds a problem, they can alert everyone else. This means the system is secure as long as at least one person is honest. In their simplest form, rollups work by

1. Having all input data published, allowing anyone to read it.
2. Allowing anyone to challenge against invalid behaviors.

The latter makes rollups secure and robust even if they are operated by centralized sequencers. Rollups are divided into two categories based on how they handle the second component.

### Optimistic Rollup

An optimistic rollup (ORU) assumes off-chain transactions are valid when publishing a new state transition on chain. While an ORU significantly improves transaction throughput by using the same state machine as the L1, it relies on a mechanism known as **fraud proofs** to ensure the integrity of the system. A fraud proof is essentially a mechanism that allows users to challenge the validity of a state transition on the rollup chain.

After a new state is published, there is a long challenge window (usually 7 days) for anyone to attest its validity. If a user believes that a transaction has been processed incorrectly, they can submit a fraud challenge to the main Ethereum chain. Otherwise, after the challenge window, this state is considered to be finalized.

The design choice of fraud proofs can also divide rollups into two categories.

- Non-interactive (or Re-executing) Fraud Proofs. In case of a dispute, the L1 contract would emulate the execution of all transactions in the relevant state, to see whether the outcome matches the given claim.

This incurs significant gas costs because there are potentially a lot of transactions. Furthermore, these transactions might be complicated and can exceed the gas limit given by the L1.
- In addition, the might be some slightly differences between the rollup and the L1, making re-execution not possible, or hard to realize.

> Optimism chose to use this approach in the first place but later abandoned this implementation.

**Interactive Fraud Proofs**. Related parties (i.e, challenger vs sequencer) engage in a back-and-forth protocol to resolve dispute with minimal work required from any L1 contract.

- The key principle behind interactive proving parties in a dispute should do as much off-chain work as possible needed to resolve their dispute, rather than putting that work onto the L1 contract.

Transaction execution can be broken down to multiple instructions, therefore, specifying which instruction was invalid is enough.
- Parties communicate off-the-L1 to identity this erroneous instruction via multiple rounds of interaction.
- Only the final step of the interactive dispute protocol involves L1 contract’s effort.

This approach addresses the expensive gas costs incurred by the non-interactive approach, significantly reducing computational complexity.
However, this comes with several drawbacks.

- Doubling the challenge period.

Apart from the regular challenge period, there is an additional challenge period for the interactive communication when a fraud challenge is invoked.
- In the worst case, the total window time can be doubled as usual (i.e, 14 days).

The rollup itself becomes more complex.

- At the moment, Arbitrum is the only optimistic rollup having the interactive mechanism on mainnet.
- Beside implementing the core protocol itself, a rollup must have an interface for parties to jump in for fraud challenges. This interactive mechanism introduces a new level of complexity in the protocol, and can be harder to design safely.

Next, we analyze a few properties of an ORU.

- Cost. Transaction costs on an ORU include an L2 cost (execution and data) and an L1 cost (state transition) and a DA cost.

The L2 execution and data cost is extremely cheap.
- The state transition cost is amortized over transactions and is fixed.
- If an ORU uses L1 as the DA, then the dominating cost should be DA cost.

For an ORU, full transaction data must be published to DA. Therefore, the DA cost is considered higher than that of a zk rollup (see below).

**Finality**. ORUs have slow finality because of the challenge window for fraud attestation.

- Today, most ORUs have 7-day finality.
- With interactive fraud proofs, an extended challenge window is created whenever a new challenge is invoked. As a result, users might have to wait for at most 14 days to withdraw their tokens from the rollups.

**Throughput**.  Throughput on an ORU is mainly limited by the L2 execution performance and DA bandwidth.

- Regarding DA, fortunately, EigenDA is doing 15+MB/s while Celestia has a roadmap to 1-gigabyte blocks (i.e, 1 GB over 12 seconds => 80+ MB/s).

**Simplicity**. ORUs are much simpler than ZRUs.

### ZK Rollups

A zkRollup (ZRU) relies on validity proofs to ensure the correctness of a state transition. It is able to verify a very complex operation (i.e, ~10k transactions) with very little information and a fixed cost. When submitting a rollup batch to L1, the sequencer must send along a validity proof proving that the off-chain computations are correct. ZRUs only need to provide validity proofs to finalize transactions on L1 instead of posting all transaction data on-chain like Optimistic Rollups.

Validity proofs are succinct and have fixed (*verifying*) cost. That is, no matter how many transactions there are, the final proof is fixed in length and verifying cost. This cost is amortized over all transactions included in the proofs. As the result, more transactions will result in less average cost per transaction.

We also analyze a few properties of a ZRU.

- Cost. Users on a ZRU must pay an additional cost for validity proof beside L1, and L2 fees.

For a ZRU, the data published to DA is usually more compact than for an ORU. Therefore, users on a ZRU pay less DA fee than users on an ORU.

This is because a ZRU only needs to publish the differences (i.e, state-diff) between two continuous states while an ORU must publish whole transactional data for the sake of re-execution.

Thanks to new advancements in ZK proving marketplace and new proving algorithms, proving cost now is cheaper and cheaper.
Today, proving cost per transaction is between half a cent to one cent. This additional cent balances out the reduced cost of DA mentioned above.

**Finality**. ZRUs allow fast finality. After a validity proof is submitted and verified on chain, the corresponding state is consider valid and finalized, no other challenge window is needed.

- Today, most ZRUs have 24-hour (or less) finality.
- Again, thanks to new advancements in ZK proving marketplace and new proving algorithms, 1-hour (or less) finality is possible.

Succinct’s SP1 and RISC-0 show potentials to generate a validity proof in an order of minutes.

**Throughput**. ZK proving performance is around tens of thousands of gas per second at the moment. This is expected to increase with further optimization and by adding more proving machines/GPUs.
**Simplicity**. While developing a new ZK proving infrastructure is considered complex, integrating an ORU with ZK proving is now much simpler.

- For example, SP1 and RISC-0 only require deploying a few additional services while keeping the Optimism codebase the same.

# Hybrid Rollups

The progress of ZK proving shows promising potentials. As a result, many rollups are considered to transition to a fully ZK mode. For high-performance rollups, this transition requires a stop. While doing a fully ZKU is expensive, we can definitely take a hybrid approach.

- Re-executing fraud proofs are not possible because it is impossible for L1 to re-execute these transactions.

Additionally, we might use external DA as a replacement for the L1 DA.

Interactive fraud proofs are complicated and buggy, and they might double the (*already long*) finality time.
Validity proofs offer fast finality but the proving performance might not keep up with our execution client on real-time proving.

We recognize that generating validity proofs is not always ideal. [Arbitrum has its fraud proof on mainnet for a few years but it has never been triggered](https://cointelegraph.com/news/arbitrums-fraud-proofs-havent-been-used-since-it-launched). This is to say that, **as long as the sequencer behaves honestly**, we will never need to use fraud proofs or validity proofs. We only need fraud proofs or validity proofs once a challenge is invoked. That is, if anyone spots an invalid state transition, he can initiate a challenge request and the remaining responsibility is at the sequencer side. The sequencer must (or ask external provers to) generate a validity proof for the required state transition and submit it to L1 attestation. Failure to generate this validity proof on time will get the sequencer slashed, and thus losing his stake.

[![image](https://ethresear.ch/uploads/default/optimized/3X/f/1/f139fca0c5794dafdcf7196770da727403692b4f_2_690x347.png)image2326×1170 211 KB](https://ethresear.ch/uploads/default/f139fca0c5794dafdcf7196770da727403692b4f)

***Figure**. A simplified version of a hybrid rollup.*

In its simplest form, our approach is an optimistic rollup but with validity proofs. This offers several advantages.

- Shorter challenge period (hence faster finality). Validity proofs are only required once we have a challenge.

The extended challenge period can be reduced from 7 days to as little as just few hours, or 1-2 days if being conservative.
- Most of the time (99.9999%), we do not need to generate validity proofs.
- If a challenge is invoked, the sequencer than has an additional window to submit the required validity proof. The additional window time should be on an order of the maximum proving time for the sake of security.

For example, if proving time is one hour, we can have this extended window to be 24 hours.

In the interactive fraud proof setting, the malicious sequencer will attempt to prevent 1) the state being challenged; and 2) the challenger finalizing the challenge. In the hybrid setting, (2) is not considered as if (1) is triggered, the sequencer has no other choice than submitting a valid proof.

**Simple and robust fraud mechanism**. ZK validity proofs appear to be more robust than fraud proofs.

- Several ZK rollups have been running on the mainnet.
- Arbitrum’s fraud proofs are the only permisisonless fraud proofs on mainnet that is running for years[1] while Optimism’s fraud proofs have just been live for a few months.

Optimism also had to disable its permissionless fraud proofs following security audits.

With this approach, a challenger can just focus on keeping up with the chain progress and identifying the incorrect state transition (same as the re-executing fraud proofs), no other interaction is required.

- Furthermore, no re-execution is required, therefore, challenging a state is cheaper than non-interactive fraud proofs.

**Cost saving**. The cost for users is the same as in an ORU and operational costs are lower than a ZRU.

- This is because users do not have to bare the cost of validity proof generation.

Notice that the cost of generating proofs are compensated by either the sequencer or the challenger.

ZRUs have to bear the cost of generating validity proofs for every state transition, even if there is no transaction. This is not required in a hybrid mode.

# Conclusion

The hybrid rollup approach represents a significant advancement in blockchain scaling solutions. By combining the best aspects of optimistic and ZK rollups, it offers a more efficient, secure, and user-friendly experience. This innovative model not only addresses current scalability challenges but also pays the way for future improvements and adaptations as the ecosystem continues to develop.

We give a quick comparison between different approaches in the following table.

| Property | Optimistic Rollups | ZK Rollups | Hybrid Rollups |
| --- | --- | --- | --- |
| Extended Finality | 7 days | N/A | 1-24 hours, depending on the ZK solution |
| Transaction Cost | Dominated by DA cost | Dominated by ZK proving | Dominated by DA cost |
| Operation Cost | Lower | Higher | Lower |
| Throughput | Limited by DA (for full transaction data) | Limited by DA (for state-diff[2]) and ZK proving | Limited by DA (for full transaction data[3]) and ZK proving |
| Simplicity | Simple | Considered more complex, depending on the solution | Considered more complex, depending on the ZK solution |
| Fraud Proofs | - Non-interactive: less battle-tested, limited in performance, less customizable - Interactive: complicated, time-consuming | Robust validity proofs | Robust validity proofs |

***Table**. A quick comparison of different rollup designs.*

1. As Arbitrum’s fraud proofs never got invoked on mainnet, we do not know whether they are robust when they are actually challenged. ↩︎
2. Some ZRUs (e.g, Polygon) still publish full transaction data rather than state diff. ↩︎
3. One question naturally arises is whether we can apply state-diff to a hybrid rollup instead of publishing full transaction data without sacrificing security. ↩︎
