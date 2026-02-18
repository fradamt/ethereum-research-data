---
source: ethresearch
topic_id: 19988
title: Reputation-Centric Light Client Framework for Optimistic Rollups
author: marcellobardus
date: "2024-07-05"
category: Layer 2 > Optimisitic Rollup
tags: []
url: https://ethresear.ch/t/reputation-centric-light-client-framework-for-optimistic-rollups/19988
views: 2701
likes: 1
posts_count: 3
---

# Reputation-Centric Light Client Framework for Optimistic Rollups

Authors: [Marcello Bardus](https://x.com/0xmarcello) ([Herodotus](https://x.com/HerodotusDev)), [Kacper Koziol](https://x.com/kacperkozi) ([Herodotus](https://x.com/HerodotusDev))

Thanks for early feedback: [bonustrack87](https://x.com/bonustrack87) ([Snapshot Labs](https://x.com/SnapshotLabs)), [Larry Sukernik](https://x.com/lsukernik) ([Reverie](https://x.com/hi_reverie)), [Pia Park](https://x.com/piapark_eth) ([Herodotus](https://x.com/HerodotusDev)), [Wojtek](https://x.com/wojtekwtf) ([Supercast](https://www.supercast.xyz/)),

# Summary:

This post introduces a conceptual framework for a reputation-centric light client system designed to address critical challenges in Optimistic Rollups (ORUs), with a primary focus on enabling fast finality for accessing ORU data from Ethereum, ORUs and other Ethereum layers. At its core, the system leverages the Herodotus Data Processor to compute sequencer reputation scores based on the sequencer’s historical behavior, including their track record of submitting valid output roots and avoiding successful challenges. This allows light clients to trust output roots only from sequencers with an impeccable track record without waiting for the full dispute period. This approach significantly reduces finality time while maintaining security. The framework includes a punitive measure that resets a sequencer’s reputation upon successful challenges, ensuring system integrity. Additionally, a fallback mechanism reverts to the standard seven-day dispute period in cases of unresolved conflicts or detected irregularities.

### Reputation-Centric Light Client Framework for Optimistic Rollups

Optimistic Rollups have seen significant adoption, however, they encounter several challenges, particularly in terms of finality time and data verification. This post introduces a conceptual framework for a reputation-centric light client system that aims to address these issues, enabling fast finality for accessing ORU data from Ethereum, and from other Ethereum layers.

OP Stack and other Optimistic Rollups (ORUs) have a security model based on fraud proofs. In this model, anyone can act as a sequencer, also known as a proposer. The sequencer first proposes the rollup state to Layer 1 (L1), after which a seven-day window is opened. During this period, anyone can challenge the correctness of the proposed state.

In ORU implementations such as OP Stack, proposers periodically submit output roots to L1. These output roots are a hash of certain L2 state information, including the state root, block number, and timestamp of the latest L2 block. OP Stack incorporates a specification for a fault proof system with bonding, which creates incentives for proposers to submit correct output roots.

This mechanism imposes a long finality time for ORUs, which is problematic for Storage Proofs, a secure on-chain data access solution that Herodotus has previously developed for Optimism and several other ORU ecosystems. This is especially problematic following recent upgrades that introduced permissionless fraud proofs on Optimism. With these upgrades, no assumptions can be made about where a valid state root can be found.

## Secure Data Access and Processing

The framework incorporates two crucial components:

### Storage Proofs

Storage Proofs are a secure on-chain data access primitive utilized by the Herodotus Data Processor that enables the cryptographic proving of the provenance of on-chain data. They allow for the verification of any data available on Ethereum, including current and historical balances, transactions, user interactions, liquidations, and more. Storage Proofs also enable the trustless and secure reading of data from arbitrary Ethereum Layers.

By utilizing Storage Proofs, the Herodotus Data Processor can ensure the integrity and authenticity of the on-chain data it processes, providing a foundation of trust for its computations.

### Data Processing Component

This would leverage the Herodotus Data Processor (HDP) to compute sequencer reputation scores efficiently. HDP can be thought of as a zk-coprocessor, capable of performing computations on verified data. Storage Proofs guarantee the integrity of the input data to HDP. Custom computations can be defined using HDP Modules, which can later process the verified historical data and update reputation scores based on the defined criteria, such as the consistency of avoiding challenges and the validity of proposed output roots over time.

## Reputation based light client

In our design, a sequencer, identified by an Ethereum address, would be assumed to be the most trustworthy based on the following criteria:

- The sequencer consistently avoids challenges, or any initiated challenges against them are unsuccessful.
- The validity of the sequencer’s proposed output roots over time, as proven by the lack of successful fault proofs against their outputs.

In OP Stack implementations like Bedrock, and potentially in other ORUs, output roots represent a compact summary of the L2 state at a specific block. These output roots are not Merkle roots of the entire canonical L2 chain, but rather a hash of certain L2 state information. Bonded proposers periodically submit these output roots to L1.

The output root typically includes a hash of the following information:

1. The state root of the L2 block
2. The L2 block number
3. The timestamp of the L2 block
4. The hash of the L2 block itself

This structure allows for efficient verification of specific L2 state information without requiring the entire L2 chain data on L1.

Once a highly reputable sequencer posts a claimed output root to L1, a Light Client contract would assume the claim is valid and treat it as final. This approach ensures that only sequencers with an impeccable track record are trusted, significantly reducing the finality time while relying on the cryptographically proven historical reliability of the sequencer rather than waiting for the full dispute period.

The Light Client contract would store the full output roots proposed by reputable sequencers, not just the block hash, enabling trustless proof of claims like withdrawals against the output roots directly.

The reputation of the sequencer can be periodically updated using the Herodotus Data Processor. This involves assessing historical data to ensure the sequencer continues to meet the criteria of reliability and activity. By continuously evaluating the sequencer’s performance and updating their reputation at fixed intervals, the Light Client can maintain a high level of trust and accuracy in the state roots it accepts.

## System Architecture

##

The proposed system would operate as follows:

1. Proposers submit output root proposals to the appropriate ORU contracts on L1, based on the state of the ORU L2 chain.
2. The ORU L1 contracts handle both output root proposals and challenges/fault proofs against these proposals.
3. The Herodotus Data Processor retrieves and processes data from the ORU L1 contracts, including output root proposals and challenges/fault proofs.
4. The reputation-based light client contract uses the processed data from the Herodotus Data Processor to track sequencer reputation scores and store trusted output roots. A custom reputation calculation formula can be implemented, allowing for flexible and adaptable assessment of sequencer reliability based on various factors and weighting systems as deemed appropriate for the specific ORU implementation.
5. The light client interface allows other contracts to query the state root of the L2 chain based on the most reputable sequencer’s output roots.

## Handling Successful Challenges

In the event that any challenge against a sequencer is successful, the reputation of the sequencer would immediately reset to zero in the light client. This punitive measure ensures that only sequencers with an impeccable track record maintain trusted status.

With fault proof systems like those in OP Stack’s Bedrock, the Light Client contract would automatically reset a sequencer’s reputation to zero if a fault proof is successfully submitted and verified, showing an invalid output root proposed by that sequencer. This automated process ensures swift and consistent enforcement of the reputation system.

The permissionless output proposal mechanism provides an objective way to track sequencer reputation over time and identify potentially malicious outputs. Simultaneously, the output roots proposed by sequencers enable the verification of Storage Proofs against these proposed L2 state roots when using the Light Client. Ultimately, this approach creates a self-regulating system that not only incentivizes honest behavior but also ensures quick penalization of any attempts at fraud, thereby maintaining the overall reliability and security of the network.

### Fallback Mechanism

In cases of unresolved conflicts or when the system detects any irregularities, it would automatically fall back to the conservative seven-day dispute period. This would ensure that the system remains secure and trustworthy, even in the face of unexpected challenges or disagreements among reputable sequencers.

## Potential Impact and Future Directions

We believe that this reputation-based light client framework has the potential to significantly decrease duration to finality for ORUs. By reducing finality times while maintaining security, it could substantially improve the user experience and enable new use cases in L2 ecosystems.

As we continue to explore and refine this concept, we welcome input from the community. The next steps would involve further theoretical analysis, simulations, and potentially, prototype implementations.

# References

Optimism Bedrock Documentation: [Optimism Documentation](https://community.optimism.io/docs/developers/bedrock)

L2 Output Root Proposals Specification: [optimism/specs/proposals.md at 65ec61dde94ffa93342728d324fecf474d228e1f · ethereum-optimism/optimism · GitHub](https://github.com/ethereum-optimism/optimism/blob/65ec61dde94ffa93342728d324fecf474d228e1f/specs/proposals.md)

## Replies

**donnoh** (2024-07-14):

> This approach significantly reduces finality time while maintaining security.

This is false as the attack is trivial: behave honestly up to the hardcoded criteria and then misbehave to steal funds. Applications are economically secured up to the bond size minus the profit from stolen funds.

Proposers reputation is subjective and offchain monitoring systems can present the data and let users decide whether to take the risk or not, which IMO would be mainly based on offchain reputation (e.g. known entity). Moreover, no “irregular behavior” detection mechanism exists that is shorter than a complete fraud proof and that can’t be used against honest proposers.

---

**maniou-T** (2024-07-18):

The article mentions that if a challenge is successful, the sequencer’s reputation will be reset immediately. Could this reset mechanism itself be abused or become a target for attackers?

