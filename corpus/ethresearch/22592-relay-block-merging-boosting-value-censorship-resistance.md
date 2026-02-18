---
source: ethresearch
topic_id: 22592
title: "Relay Block Merging: Boosting Value & Censorship Resistance"
author: remosm
date: "2025-06-12"
category: Proof-of-Stake > Block proposer
tags: [mev, proposer-builder-separation, censorship-resistance]
url: https://ethresear.ch/t/relay-block-merging-boosting-value-censorship-resistance/22592
views: 910
likes: 5
posts_count: 3
---

# Relay Block Merging: Boosting Value & Censorship Resistance

Co-authored by [Michael](https://x.com/mostlyblocks) and [Kubi](https://x.com/kubimensah) ([Gattaca](https://x.com/gattacahq)). Special thanks to [Thomas](https://x.com/soispoke), [Julian](https://x.com/_julianma), [Anders](https://x.com/weboftrees), [Max](https://x.com/0xKuDeTa) and [Niclas](https://github.com/blombern) for their feedback and suggestions. Feedback is not necessarily an endorsement.

### Overview

This post introduces relay block merging, a way of immediately increasing block value by offsetting two systemic inefficiencies: exclusive order flow on the builder level, and timing games on the relay level. This unlocks transparent revenue for relays, increases Ethereum’s censorship resistance, and provides an income uplift for proposers and builders.

In practical terms, relay block merging allows relays to append transactions from competing blocks into the bottom of the winning PBS auction block without changing its execution guarantees. The idle time a relay normally incurs due to timing games is repurposed to optimize block value.

The design creates a net surplus by enabling transactions from opted-in builders that lost the PBS auction to still find timely inclusion, capturing value that would otherwise be inaccessible due to exclusive flow. The merged block’s value equals or exceeds the original PBS block value, eliminating financial downside risk. This additional revenue is shared between builders, relays, and the proposer.

Relay block merging enhances Ethereum’s censorship resistance. Currently, a builder can enforce censorship over the slots it wins. With relay block merging, non-censoring relays can merge filtered transactions back into the blocks, limiting inclusion delays, while increasing block value.

The value add of relay block merging positively scales with decentralization. The more fragmented flow is among builders, the less encompassing the execution guarantees an individual builder can provide, the higher the surplus unlocked by the design.

The system is permissionless and easily auditable. Anyone can operate a relay, with trust relationships evolving naturally among participants. Both transaction inclusion and value distribution models can be fully verified by builders against their local records.

An adjacent design is [PEPC-Boost](https://hackmd.io/@bchain/r1eZd51g3n), which modifies relays to allow for top-of-block (TOB) and rest-of-block bidding (ROB); relay block merging parallels this by enabling appends to the bottom of the block.

The following table summarizes the key benefits of relay block merging versus the status quo:

| Aspect | Status Quo | Relay Block Merging |
| --- | --- | --- |
| Block Value | Capped by the flow of the winning builder, at the winning PBS bid. | Strictly enhanced by incorporating transactions from other builders. Greater or equal to the winning PBS bid. |
| Revenue Distribution | Between proposer and winning builder. | An additional surplus accrues to the relay, proposer, and multiple builders. |
| Censorship Resistance | Can be censored by the winning builders. | Strictly enhanced as non-censoring relays can merge back filtered transactions. |
| Decentralization | Builder diversity capped by private flow. | New builders can contribute without winning the auction. Surplus scales with flow fragmentation. |

### Implementation and Value Flow

Relay block merging unfolds in two parallelized stages: the auction stage, which is equivalent to the current PBS auction, and the block merging stage, which unlocks an additional surplus via relays merging transactions into the PBS block.

Relays may sort non-overlapping transactions into a priority queue during the auction stage from which transactions can be drawn in the merging stage without another full pass over the transaction set.

Finally, relays proceed to a delivery stage, sanity checking the surplus of the block merging stage and returning the header of the most valuable block to the proposer.

**Before the slot**

Builders opt into Relay Block Merging. For each block, builders must define:

- Bundle labeling: Specify which transactions are part of a bundle. Mislabeling that triggers accidental unbundling requires builder compensation to the originator.
- Exclusions: Specify transactions that should be excluded from the merging stage.

**Auction Stage**

1. The standard slot auction commences with relays receiving builder bids.
2. The proposer calls getHeader.
3. The relay designates the winning block B_{PBS} and proceeds to the merging stage. The relay may bid-adjust as per its policy.

The result of the auction stage is the PBS block B_{PBS}.

**Merging Stage**

1. For the best block B of each opted-in builder i, the relay identifies all transactions absent in the PBS block B_{PBS}:

\text{Txns}_{i/\text{PBS}} = \{ \text{tx} \in B_i \mid \text{tx} \notin B_{\text{PBS}}\}

1. The relay appends transactions from Txns_{i/PBS} to the bottom of B_{PBS}, filtering out any reverts.

The result of the merging stage is the relay merged block B_{RM}.

**Delivery Stage**

1. The relay checks for the presently most valuable PBS block \hat{B}_{PBS}.
2. The relay sanity checks the value of B_{RM} against the maximum value of B_{PBS} and \hat{B}_{PBS}:

\Delta V = val(B_{RM})-max(val(B_{PBS}), val(\hat{B}_{PBS}))

1. If \Delta V \geq 0 the relay returns the header of B_{RM} to the proposer and splits the surplus as per the merging surplus distribution rule; otherwise, it falls back to the most valuable PBS block B_{PBS} or \hat{B}_{PBS}.

The end result of the delivery stage is the provision of the header of the most valuable block to the proposer.

### Value distribution

The surplus unlocked by relay block merging simply corresponds to the difference between the value of the merged block B_{RM} and the value of the PBS block B_{PBS}:

V_{merging}=val(B_{RM}) - val(B_{PBS})

Therefore, relays compete on maximizing the value delta between the merged block B_{RM} and the PBS block B_{PBS}. This competition centers on three dimensions:

- The set of transactions available to a relay for merging \text{Txns}_{i/\text{PBS}}.
- The efficiency with which the relay can merge \text{Txns}_{i/\text{PBS}} into B_{PBS}.
- The latency of the relay to the attestation committee (i.e. max. size of the block).

As transactions are sourced from different builders, the surplus must be calculated per transaction. When multiple builders contribute the same transaction, it is attributed to the builder with the higher PBS auction bid, incentivizing competitive bidding.

As builders, relays, and the proposer all contribute to the merging stage, the revenue should be distributed among them. The distribution rule should reflect the value-add of each party, and facilitate competitive price discovery.

An initial rule could first linearly compensate the relay for the excess value of B_{RM} versus B_{PBS} and retain the proposer-builder split from the PBS auction for the remainder. Compensation could also take the form of fixed percentage allocations for the relay, winning builder, contributing builders, and the proposer respectively. We invite contributions from researchers, validators, relays, and builders.

**Constraints**

Relays must commit to improving the block that has won the PBS auction, even if a combination of multiple losing blocks could be more valuable. Otherwise, builders are incentivized to spam blocks containing subsets of the best block to improve their chances of inclusion during the block merging stage. Visually speaking, they would try to build a maximum of legos, at the cost of efficiency, which would reflect in reduced overall block value.

### Future Directions

In the future, relays may elect to share blocks with each other after the end of the auction stage, at the commencement of the merging stage. This way, the net surplus that can be unlocked by any individual relay during the merging stage increases without incurring a competitive disadvantage. This incentive holds for any relay that does not have visibility of all blocks; relays that fail to comply can be excluded from the system by social consensus.

## Replies

**austonst** (2025-06-19):

Sorry for not getting this feedback out earlier. I’m trying to figure out the builder incentives and dynamics a little more. A few angles on this:

Under what circumstances will builders find it more profitable to get transactions included via appending rather than winning the main auction? For example, if two builders each have private order flow such that their blocks are each worth ~1 ETH, then the usual mev-boost auction incentives should push the builder bids up to 1-ε ETH, delivering nearly the full value to the proposer while the winning builder keeps very little. If the losing builder could get their transactions appended to the block, and then receive a kickback of some percentage of the surplus value, they may end up making more in profit than the “winning” builder.

If builders become aware of this, would they *try* to lose the auction? Could this lead to less competition in the auction, such that the proposer gets paid less?

As a separate question, how would per-tx surplus be calculated? Buildernet claims that for each tx it rebuilds the most valuable block possible–with that tx missing–to compute surplus, but relays won’t have that capability. Is it feasible for relays to analyze a bundle in isolation to determine its contribution, or would builders be expected to provide some numbers? Are there ways this system could be gamed by a builder to make a tx look more valuable than it is?

---

**remosm** (2025-06-25):

Hey Auston, great questions.

Typically, builders will find it most profitable to win the main auction as the winning builder has first access to contentious state (i.e. top-of-block).

If a builder loses the auction, it can only derive benefit from the subset of its private flow that successfully executes when appended to the bottom of the block.

In the example, if both builders have private order flow worth ~1 ETH, then only the disjoint set of this flow would be available for merging.

From this remaining set, only the transactions that do not compete for contentious state that has already been allocated to the winning builder can find inclusion. Lastly of these, the contributing builder captures an initial 25% of their value.

Therefore, losing is profitable if a 25% value share on the remaining flow exceeds the proposer/builder split for the main auction.

This is self-remedying, as if builders were to lose the auction on purpose, the value share of the winning builder would grow proportionally to the degree to which the losing builder underbids, which would correspondingly increase the opportunity cost of underbidding. Separately, the incentive to lose would additionally be weakest when demand is typically highest, as the value of top-of-block scales with volatility.

Regarding the surplus, we currently define it simply as each transaction’s priority fee. This is because the merging stage is append-only, and thereofore, isolated from the larger block provided by the winning builder. A goal is keep the value distribution calculation simple and fast, and barriers to entry for relays low.

