---
source: ethresearch
topic_id: 18733
title: Unified Endgame Rollup Requirements
author: Perseverance
date: "2024-02-20"
category: Layer 2
tags: []
url: https://ethresear.ch/t/unified-endgame-rollup-requirements/18733
views: 1938
likes: 5
posts_count: 1
---

# Unified Endgame Rollup Requirements

*Proposer: [George Spasov](https://twitter.com/GSpasov) (LimeChain)*

*Special Thanks for the comments to [Daniel Ivanov](https://twitter.com/danielkivanov) (LimeChain), [Mohammad Jahanara](https://twitter.com/MMJahanara) (Scroll), [Péter Garamvölgyi](https://twitter.com/thegaram33) (Scroll), [Brecht Devos](https://twitter.com/Brechtpd) (Taiko)*

The growth of the rollup ecosystem calls for the unification of the terms used and requirements applied when judging the state of the various rollups. Currently, every team and researcher has a slightly different way of expressing requirements and a slightly different vision of what it means to be a decentralized rollup. This post is an attempt to start the discussion around a unified list of requirements that a rollup must satisfy to be considered “complete” in its endgame decentralized form. Such a list will be helpful to teams and researchers in terms of discussions, system analysis and backlog prioritization.

We assume that decentralization is a gradient and each rollup team can decide when, how, and if to satisfy the requirements listed below. The list is not ordered by the importance of the requirement and higher placed requirements must not be understood as more important. The list is created with the [proposed milestones for rollup decentralization](https://ethereum-magicians.org/t/proposed-milestones-for-rollups-taking-off-training-wheels/11571) in mind and is an invitation to propose changes, additions and/or removals to this list.

# Unified Endgame Rollup Requirements

1. L1 sufficiency - any actor monitoring the L1 and having access to L1 historical state should be able to reconstruct the latest committed state of the rollup.
2. Subjective finality - Given finality of the L1, any actor monitoring the L1 should be able to reason about the final state of the rollup, regardless of the finality mechanism and its state (i.e. whether or not the fraud proof submission window has passed).
3. Objective finality - The rollup via its actors should be able to convince the L1 of its finality.
4. Robust liveness - any valid transaction that is paying higher than current rate for fee, should be included in a sequence within time \texttt{T}_C
5. Robust finality -  any valid sequence gets finalized within time \texttt{T}_L
6. L1 leadership - any external (to L2) input required for the functioning of the system is inputted by the L1 and deterministically provable (i.e. source of randomness).
7. Economic viability - any actors assuming roles within the protocol block production and finalisation pipeline are reimbursed and paid for their duties. Altruism is not required for the system to operate securely. All security ensuring roles have their minimum APY ensured by the protocol.
8. Permissionless role access - any role within the protocol can be assumed by any actor meeting the criteria for this role (i.e. has enough stake provided), without requiring permission by an authoritative entity.
9. Actors diversity - through its mechanism rollup maintains a target of \texttt{N}_P  diverse non-colluding proposers and \texttt{M}_P diverse non-colluding block-provers, thus addressing systemic risk posed by economical, governmental, geographical and other factors.
10. Excellent user experience - the rollup offers the user an excellent experience closer to the web2 paradigm.

Cheap transactions - on average the gas price for transaction execution in the rollup costs \texttt{X}_C times less compared to L1
11. Fast Preconfirmations - users get preliminary confirmation of inclusion and/or post-state of the rollup within \texttt{T}_L
12. Synchronous composability enabled - the rollup enables synchronous composability with other rollups

**Open source** - the rollup has the necessary software needed to assume any of the roles and the on-chain artefacts (i.e. smart contracts) publicly available for download and use.

# Clarifying Notes

- L1 Sufficiency is needed so that the rollup is actually a rollup and satisfies the promise of the L1 being the only trust requiring party. This can be satisfied if there is a follower node implementation, that can retrieve historical rollup data from some source, check that it matches the L1 committed data, and use it to reconstruct the state
- Subjective finality allows for followers of the rollup state committed to L1 to know what is the latest committed state. It enables followers to know if/when a transaction, chunk or a batch is valid and if it will eventually be proven valid
- Objective finality allows for composability of the rollup with L1 and other L2s. With objective finality the L1 can now trust the L2 state as final and enable other parties to reason safely about this state.
- Robust liveness ensures the mitigation of attacks of any temporary SpoFs along the sequencing pipeline. Example of such temporary SpoFs might be the leader in proposer leader election type of sequencing. Attacks can be either censorship attacks (censoring a user) or liveness attacks (DoS of the rollup). So this requirement ensures both the short inclusion times, liveness and censorship resistance.
- Robust finality ensures that the rollup finalizes and becomes composable within an acceptable timeframe when the rollup is in its normal protocol operation.
- L1 leadership ensures that any external input required for the functioning of the rollup is passed by the L1 and is therefore provable by a follower. Examples of this could be randomness required for ticket generation, L1→L2 message passing, etc.
- Economic viability ensures that the various actors of the protocols are paid and the system requires no altruism.
- Permissionless role access - this requirement aims to ensure that no roles in the protocol are held for special entities and any actor can assume these roles as long as they meet the necessary criteria for this role.
- Actors diversity ensures a minimal and target number of participants for the various roles via the system mechanisms. Such a requirement adds to the robust liveness requirement and mitigates the monopoly of a few actors on the rollup for an extended period allowing them to exploit users. Furthermore, it adds security against possible malicious practices like toxic MEV and reduces risks posed by external factors - governmental intrusion, geographical outages and more.
- Excellent user experience ensures that the rollup fulfills the promise of being cheaper and does not add, but rather mitigates fragmentation. In this category, one can also add the ability to add early preconfirmations.
- Open source ensures that the code needed to assume any of the roles is not siloed and held for only special entities.
