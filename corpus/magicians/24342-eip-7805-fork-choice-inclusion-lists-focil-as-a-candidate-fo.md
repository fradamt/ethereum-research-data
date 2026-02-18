---
source: magicians
topic_id: 24342
title: EIP-7805 Fork-Choice Inclusion Lists (FOCIL) as a candidate for Glamsterdam
author: soispoke
date: "2025-05-26"
category: EIPs
tags: [glamsterdam]
url: https://ethereum-magicians.org/t/eip-7805-fork-choice-inclusion-lists-focil-as-a-candidate-for-glamsterdam/24342
views: 514
likes: 14
posts_count: 3
---

# EIP-7805 Fork-Choice Inclusion Lists (FOCIL) as a candidate for Glamsterdam

*Thanks to [Jihoon Song](https://x.com/jih2nn), [Caspar Schwarz-Schilling](https://x.com/casparschwa) ,[Terence Tsao](https://x.com/terencechain), [Jacob Kaufmann](https://x.com/jacobykaufmann) and [Francesco D’Amato](https://x.com/fradamt) for feedback and comments on this note.*

This document follows a template designed by [@timbeiko](/u/timbeiko) to propose a headliner for a fork inclusion.

**Summary (ELI5):**

**Fo**rk-**C**hoice **I**nclusion **L**ists (FOCIL, [EIP-7805](https://eips.ethereum.org/EIPS/eip-7805)) improve Ethereum’s censorship resistance by enabling multiple validators to ensure that any transaction valid under protocol rules is included in blocks.

**Why it matters:**

Censorship resistance, permissionlessness, and credible neutrality are core Ethereum values. Today, >80% of all blocks are produced by two builders who can unilaterally decide whether to include or exclude transactions (clearly illustrated by data from [censorship.pics](https://www.censorship.pics/), where the level of builder censorship fluctuates significantly over time). FOCIL fixes this by empowering the decentralized set of validators to enforce inclusion constraints on builders’ blocks, restoring fairness and ensuring Ethereum remains decentralized and neutral.

**Who directly benefits:**

This directly benefits all users by ensuring their transactions are included on-chain in a timely manner as long as the network is not congested, without having to rely on two centralized entities to not censor them.

**Why now?**

A solution to mitigate the censorship risks arising from the centralization of the builder market is long overdue. The builder market is inherently prone to centralization due to MEV and [private order flow](https://dune.com/dataalways/private-order-flow), and we have observed increasing vertical integration across builders, relays, and searchers over time. Ethereum must enforce protocol-level guarantees to users that their transactions will land on-chain, [as long as they are valid according to protocol rules, not subject to external preferences](https://ethresear.ch/t/uncrowdable-inclusion-lists-the-tension-between-chain-neutrality-preconfirmations-and-proposer-commitments/19372). FOCIL should be implemented now, before more significant censorship behavior emerges and makes protocol-level changes that improve censorship resistance more difficult to coordinate and adopt.

**Detailed Justification:**

**Primary benefits:**

- Improving censorship resistance of Ethereum: Ethereum’s current block production is heavily centralized, with two builders constructing more than >80% of all blocks. FOCIL significantly reduces this centralization risk by empowering multiple decentralized validators to enforce transaction inclusion, preventing any single entity from arbitrarily censoring transactions.
- Scaling Ethereum without imposing constraints on local block builders: By allowing validators to independently enforce transaction inclusion, FOCIL represents the first step toward scaling Ethereum throughput without depending on local block builders to preserve censorship resistance at the cost of performance or incentives (Decoupling throughput from local building - Economics - Ethereum Research).
- Improved user experience by reducing transaction inclusion time: With today’s centralized block-building process, if the two dominant builders choose to exclude specific transactions, users would experience delays averaging around 7 blocks (approximately 84 seconds). FOCIL ensures prompt and reliable transaction inclusion unless the block is full, significantly enhancing overall user experience.

**Technical Readiness:**

FOCIL demonstrates a high level of technical maturity. It has already been implemented by six client teams and successfully runs on a [local devnet](https://github.com/jihoonsong/local-devnet-focil/blob/30c32101bf84a9938854542c8c800280a0c4a0af/kurtosis/kurtosis.config.registry.interop.yaml) with Prysm, Lodestar, Teku, and Geth interoperability. It is currently undergoing spec testing, with additional local devnet testing using [Assertoor](https://github.com/ethpandaops/assertoor) scheduled to begin in the next few weeks. The consensus-layer specification has undergone preliminary review by CL client teams, and the execution-layer specification is now under review by EL client teams.

- Consensus Specification: EIP-7805 -- The Beacon Chain - Ethereum Consensus Specs
- Execution Specification: feat: add initial EIP-7805 by jacobkaufmann · Pull Request #1214 · ethereum/execution-specs · GitHub
- Execution APIs: Add initial FOCIL spec by jihoonsong · Pull Request #609 · ethereum/execution-apis · GitHub
- Consensus Layer

Prysm: Implement EIP7805: Fork-choice enforced Inclusion Lists by terencechain · Pull Request #14754 · OffchainLabs/prysm · GitHub
- Lodestar: GitHub - ChainSafe/lodestar at focil
- Teku: GitHub - Consensys/teku at focil
- Lighthouse: GitHub - sigp/lighthouse at electra-focil

Execution Layer

- Geth: https://github.com/ethereum/go-ethereum/pull/30914
- Nethermind: GitHub - NethermindEth/nethermind at feature/eip-7805

**Security & Open Questions:**

FOCIL ([EIP-7805](https://eips.ethereum.org/EIPS/eip-7805)) includes clear mitigation strategies for key security risks such as consensus liveness, IL equivocation, and fork-choice related changes, all detailed in the EIP. The design is also compatible with [EIP-7702](https://eips.ethereum.org/EIPS/eip-7702) and other proposals like Delayed Execution ([EIP-7886](https://eips.ethereum.org/EIPS/eip-7886)), BALs ([EIP-7928](https://ethereum-magicians.org/t/eip-7928-block-level-access-lists/23337)), or ePBS ([EIP-7732](https://eips.ethereum.org/EIPS/eip-7732)).

**Resources:**

Implementation progress, research posts, and talks about FOCIL can all be found at https://meetfocil.eth.limo/

## Replies

**Pmatt328** (2025-05-26):

If ready this is a must do for Glamsterdam! Thanks for the work!

---

**tim-clancy.eth** (2025-07-03):

Thank you for being our champion. This is easily the most important EIP we could add to Ethereum. We have witnessed builder censorship after the Tornado Cash sanctions and, while it was not catastrophic, we did not have a neutral mechanism to address it. We need this.

