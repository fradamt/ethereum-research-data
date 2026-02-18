---
source: ethresearch
topic_id: 22909
title: Integrating 3SF with ePBS, FOCIL, and PeerDAS
author: luca_zanolini
date: "2025-08-12"
category: Proof-of-Stake
tags: [consensus]
url: https://ethresear.ch/t/integrating-3sf-with-epbs-focil-and-peerdas/22909
views: 557
likes: 5
posts_count: 1
---

# Integrating 3SF with ePBS, FOCIL, and PeerDAS

# Integrating 3SF with ePBS, FOCIL, and PeerDAS

**Authors**: [Luca Zanolini](https://x.com/luca_zanolini), [Roberto Saltini](https://x.com/robsaltini)

Thank you to [Francesco](https://x.com/fradamt), [Julian](https://x.com/_julianma), and [Thomas](https://x.com/soispoke) for the insightful and constructive feedback.

In the following, we explore how [3SF](https://arxiv.org/abs/2411.00558) can be integrated with [ePBS](https://ethresear.ch/t/why-enshrine-proposer-builder-separation-a-viable-path-to-epbs/15710), [FOCIL](https://eips.ethereum.org/EIPS/eip-7805), and [PeerDAS](https://eprint.iacr.org/2024/1362).

The original 3SF protocol does not account for newer proposals around PeerDAS, inclusion lists, or proposer-builder separation. We build on the [existing analysis by Francesco](https://hackmd.io/@fradamt/all-in-one-fc) and extend it to fully support 3SF.

**Note**: This is a preliminary exploration of how the proposal in the paper interacts with the current designs of ePBS, FOCIL, and PeerDAS. Our goal is to assess whether combining these components introduces any challenges or incompatibilities when adapting 3SF to this context.

## Overview

The protocol follows an *ebb-and-flow* model: it combines a dynamically available (synchronous) protocol — [RLMD-GHOST](https://arxiv.org/abs/2302.11326) — with a partially synchronous finality gadget. It operates in slots, removing the need for epochs or committees. For now, all validators vote every slot, although [lightweight validator rotation](https://ethresear.ch/t/orbit-ssf-solo-staking-friendly-validator-set-management-for-ssf/19928) is being explored.

### Actors in Play

- Validators (n total):

Proposer — randomly sampled at the beginning of each slot t to propose a new block.
- Voters (Attesters) — cast vote messages (attestations) for the proposed block.
- Inclusion List (IL) Committee (16 members) — randomly sampled at each slot, tasked with creating and gossiping inclusion lists (part of FOCIL).
- Availability Committee (AC) (512 members) — also known as the Payload Timeliness Committee (PTC); randomly sampled each slot. Members vote during slot t to signal timely observation of the payload and blobs released by builders (part of ePBS).

**Builders** — entities that construct full execution payloads. They compete in an auction to have their payload selected by the proposer (part of **ePBS**).

### Slot Structure of the Vanilla 3SF

Current 3SF slot structure:

[![](https://ethresear.ch/uploads/default/original/3X/f/6/f6a1591cc9481317bc60d01bc501a2f5e9fa3f4a.png)749×194 3.6 KB](https://ethresear.ch/uploads/default/f6a1591cc9481317bc60d01bc501a2f5e9fa3f4a)

- Each slot has a duration of 4\Delta, where \Delta is the assumed network delay under the synchronous model (currently 4 seconds in Ethereum). A slot t is divided into four sequential phases:

Propose phase: begins at time 4\Delta t
- Vote phase: begins at 4\Delta t + \Delta
- Fast confirm phase: begins at 4\Delta t + 2\Delta
- Freeze phase: begins at 4\Delta t + 3\Delta

Note that 4\Delta t + 4\Delta = 4\Delta (t + 1) which marks the beginning of the propose phase for slot t + 1.

- Each slot starts with a randomly chosen proposer.
- The proposer builds on top of the fork-choice head and gossips the block.
- After a delay \Delta, validators vote for the block — but only if it extends their fork-choice head.
- If more than 2/3 vote for it, the block becomes fast confirmed.
- If fast confirmation fails, the \kappa-deep prefix of the output chain of fork-choice is selected instead. Specifically, the \kappa-deep prefix is the portion of the chain you get by taking the fork-choice tip and trimming off its most recent \kappa blocks, leaving the chain as it looked \kappa slots ago. Here \kappa represents the number of slots that are required in order to be certain, except for a negligible probability, that at least one of the proposers in these slots is honest.
- The Freeze phase enables the view-merge mechanism, addressing known attack vectors.

Validators freeze their views at the end of the slot.
- The next proposer continues receiving messages.
- Under synchrony, the proposer’s view is guaranteed to be a superset, preventing reorgs caused by asymmetric visibility.

### Voting and Finality

Votes include two components:

1. Head vote: vote for the output of the fork-choice function.
2. Finality/FFG vote: links the latest justified block (source) to a candidate block (target).
3. If ≥ 2/3 agree on a target: it’s justified.
4. If ≥ 2/3 agree on a source and the gap is one slot: it’s finalized.

Under ideal conditions (synchrony, full participation, honest proposer):

- Slot t: propose B and fast confirm it.
- Slot t+1: justify B.
- Slot t+2: finalize B.

### Fork-Choice Inclusion Lists (FOCIL)

[FOCIL (EIP-7805)](https://ethresear.ch/t/fork-choice-enforced-inclusion-lists-focil-a-simple-committee-based-inclusion-list-proposal/19870) protects against censorship by enforcing inclusion of transactions that should not be arbitrarily excluded by proposers:

- A small committee of randomly selected validators is responsible for publishing Inclusion Lists (ILs), which consist of transactions from the mempool that need to be included.
- Each validator in the committee selects transactions according to some rules (e.g., by fee or timestamp) and publishes their ILs ahead of time.
- The block proposer is then required to include the union of all transactions across all ILs into its block, provided the block isn’t full.
- A block must include all IL transactions, provided there is space, or an attester who saw an IL that was not included in the block does not vote for the block.
- This mechanism ensures that validators only vote for blocks that honor the inclusion requirements, thus preventing censorship even in MEV-driven builder environments.

---

### Enshrined Proposer-Builder Separation (ePBS)

[ePBS](https://ethresear.ch/t/why-enshrine-proposer-builder-separation-a-viable-path-to-epbs/15710) formalizes the separation between block construction and block proposal within the protocol itself:

- Builders assemble the block body (including transactions, blobs, and ILs) and submit a blinded header along with a fee bid to the proposer.
- The proposer selects the highest bidder and includes only the blinded header in the beacon block. This header cryptographically commits to the full block contents without revealing them.
- After the beacon block is published, the builder reveals the full payload. A Payload Timeliness Committee (PTC) of randomly selected validators checks whether the payload was revealed promptly and matches the commitment. They cast a vote that will be used by the attesters of slot t+1.
- This architecture enables block pipelining, and enshrines the role of builders in the protocol, getting rid of the necessity to trust relays to facilitate interactions between builders and proposers.

---

### PeerDAS and Data Availability

[PeerDAS](https://ethresear.ch/t/peerdas-a-simpler-das-approach-using-battle-tested-p2p-components/16541) introduces a scalable way to verify **data availability** using peer-to-peer sampling:

- Instead of downloading the full data (e.g., all blobs), validators perform data availability sampling by requesting random small samples from different peers.
- This allows the network to statistically verify whether the data is actually available, without any validator needing to download everything.
- PeerDAS uses KZG commitments and erasure coding to allow light clients to prove that samples are correctly encoded.
- It scales data throughput without sacrificing trust assumptions or requiring centralized data sources.
- This mechanism enable blob-based scaling for rollups and L2s.

## Required Properties

We outline the key properties that must hold for the various entities participating in the protocol:

- All properties already satisfied by 3SF – both those inherited from RLMD-GHOST (e.g., reorg-resilience of proposals by honest proposers under synchrony) and those resulting from its integration with FFG Casper – must continue to hold after composing 3SF with FOCIL, ePBS, and PeerDAS.

Under synchrony, any transaction observed by honest validators in the IL committee will be included in the next block – assuming an honest proposer - unless the block is full or the transaction is invalid.
- Under synchrony, honest proposals are not reorged. That is, if a proposer includes a block, it will remain on the canonical chain and eventually be finalized, assuming full validator participation. This property is inherited from the underlying RLMD-GHOST protocol.

**Builder protection (if payload is revealed)**: If an honest builder chooses to reveal the payload, then the block containing the builder’s payload commitment is guaranteed to remain on the canonical chain, i.e., it will not be reorged.
**Builder neutrality (if payload is withheld)**: If the builder honestly withholds the payload, they are not penalized.

- In this case, the proposer should also not receive a payment. Specifically, if there are insufficient votes to make the block canonical and trigger the payment to the proposer, the builder may honestly withhold their block. Even if the entire set of Byzantine validators votes in favor, the protocol design must ensure the voting threshold is not met without honest participation, thus preventing payment.

**Builder payment safety**: If the proposer receives payment (i.e., the payload is revealed and the required vote threshold is met), then the block will remain in the canonical chain and will eventually be finalized upon full validator participation.

### Challenge

The open challenge is: **How can we adapt 3SF’s slot timeline to accommodate FOCIL, ePBS, and PeerDAS, while ensuring the above properties are satisfied?**

This is the focus of the next section. But first, let’s state all the assumptions used from here on.

### Assumptions

1. Reduced Adversarial Resilience: We assume n \geq 5f + 1, meaning the adversary controls less than 20\% of the total stake.
2. Synchrony: The protocol operates under a synchronous network model, where validators have access to synchronized clocks and message delivery is guaranteed within a bounded delay of \Delta rounds.

In practice, periods of asynchrony or network partitions may occur. However, the presence of the partially synchronous finality gadget guarantees asynchronous safety for the portion of the chain that has already been finalized.
3. Full Participation: All honest validators are assumed to be online and actively participating during the relevant protocol phases.
4. Payload Visibility: If an honest builder reveals the payload, it is observed by the Attestation Committee, and all honest attesters in the subsequent slot agree with the AC.
5. Fast Attestation Visibility for Builders: Builders are assumed to observe individual attestations more quickly than validators – an assumption justified by the fact that aggregated attestations typically incur higher latency due to the aggregation and propagation steps (not required for the builders).

## New slot proposal

[![](https://ethresear.ch/uploads/default/optimized/3X/d/2/d20d295747c5fdc7d4d2cc7217f9f08dcfa4e71d_2_690x243.jpeg)1331×470 71.8 KB](https://ethresear.ch/uploads/default/d20d295747c5fdc7d4d2cc7217f9f08dcfa4e71d)

### Slot Timeline Restructuring in 3SF

We can restructure the slot timeline in 3SF by leveraging the fact that, under ePBS, the proposer initially sends only a beacon block with a blinded execution payload header. This separation allows us to anticipate the Vote phase: for example, validators could begin attesting as early as 2 seconds into the slot. At that point, the payload is not yet available, and the block may still be reorged in subsequent slots.

Before diving into validator behavior during the Vote phase, we need to understand the broader slot structure, since validator actions are influenced by events and actors from slot t-1.

For now, assume validators proceed to vote for the beacon block.

### Builder Behavior and Payload Release

The role of the builders is to construct full execution payloads. They compete in an auction to have their payload selected by the proposer of slot t. [By combining FOCIL with ePBS](https://ethereum-magicians.org/t/epbs-focil-compatibility/24777), builders also include an **IL bitfield** specifying from which of the IL committee members (from slot t-1) the builder has received an IL. The bitfield establishes a set of ILs that the payload commits to satisfying.

Once a builder sees that its payload has been selected (i.e., the proposer included its signed header) and it observes sufficient attestations and no conflicting beacon block from the proposer, it proceeds to release the payload and it propagates the blob data.

If the builder observes at least 60\% votes for the block it constructed, it must release the payload. However, if the builder fails to reveal the payload and validators still cast more than 80\% votes in support of the block, the builder is penalized and must compensate the proposer regardless.

To understand why 60% provides builder protection, let B be the proposed block that receives 60% of the votes. Consider the worst-case scenario: this 60% includes all malicious validators, while the remaining 40% – composed entirely of honest validators – votes for a different block B’. In this case, the best the malicious validators can do to attempt a reorg of B is to cast conflicting votes for B’. However, since this constitutes equivocation, their votes would be disqualified from contributing to either B or B’. Given that the adversary controls less than 20% of the stake, the weight of B remains above 40%, and thus still exceeds the weight of B’.

Likewise, if the builder observes fewer than 60% of votes and chooses to withhold, the 80% voting threshold that would force the builder to pay cannot be reached, assuming less than 20% of the stake is adversarial.

For a more detailed analysis – which also shows that the 20% adversarial threshold is the best we can tolerate – see [this analysis](https://notes.ethereum.org/@tgj5dxinR6mR9Go4BN9ytg/rko1BEkOex) originally presented by Roberto.

### Inclusion List Handling and the Freeze Phase

Once the IL committee for slot t begins receiving the full payload, each member constructs an inclusion list. This triggers the FOCIL mechanism, which runs until the Freeze deadline, the point when validators stop adding ILs to their view.

The Freeze phase ensures that (under synchrony):

- The next proposer has time to see all ILs.
- Voters in slot t+1 do not see more ILs than the proposer does.

In other words, towards the end of the slot, voters of slot t freeze their views and stop storing new ILs. Some time later, the proposer of slot t+1 also stops storing new ILs.

As noted in [this post](https://ethereum-magicians.org/t/epbs-focil-compatibility/24777), it’s important to understand that the **precise timing between FOCIL and ePBS actions isn’t critical to correctness**. This is because the enforceability of inclusion lists does not depend on them being constructed from the latest canonical head of the chain. Even if an IL is created based on an outdated or non-canonical view of the chain, its transactions must still be honored by the builder – provided there’s block space and the transactions are valid. This means some redundancy is acceptable: if IL transactions have already been processed in previous blocks, they may simply be skipped.

### Fast Confirmation and Availability Committee

At 7 seconds into the slot, the Fast Confirmation phase is executed. If full participation, synchrony, and an honest proposer are present, fast confirmations can proceed (even if the full payload hasn’t yet been revealed.)

If full validator participation isn’t achieved, a \kappa-deep prefix of the chain output by the fork-choice function is chosen (to be precise, the longest between the \kappa-deep prefix and the chain with head the block associated to the greatest justified checkpoint) to ensure beacon chain growth.

During this phase, we introduce a new voting mechanism modeled on the ePBS Payload Timeliness Committee (PTC). This Availability Committee (AC) performs three core tasks:

1. Verifies whether the payload was revealed in time.
2. Checks blob data availability (critical for the next proposer, who may not subscribe to all column subnets).
3. Perform the IL bitlist inclusivity check.

Each AC member locks onto the first beacon block it observes in the slot. This lock ensures it evaluates that block (and payload), even if a conflicting block appears later. This prevents equivocation risk: if the builder sees its block included and releases the payload, the AC still votes on the locked-in view.

An AC member casts its vote during Fast Confirmation if:

1. All its assigned blob custody columns are available.
2. The IL bitfield in the payload marks all relevant IL committees (seen before Freeze of slot t–1) as satisfied.

Note that, in theory, fast confirmation and the AC vote are logically distinct steps in the protocol and do not need to occur simultaneously. In practice, however, it is reasonable to align them, since both should take place roughly one \Delta before the Freeze phase. Importantly, there are no separate “fast-confirmation votes”: a block is fast-confirmed by the attestations already cast during the vote phase.

### Views and the Freeze Deadline

The Freeze deadline now serves three roles:

- FOCIL cutoff.
- AC vote cutoff.
- General view-merge point as in the vanilla 3SF.

### Fork Choice and the Role of RLMD-GHOST

After all mechanisms above, we return to the core of the protocol: the fork-choice function. A fork-choice function is a deterministic algorithm executed locally by each validator. Given the validator’s current view, it outputs the chain that is considered valid at that moment. Both the proposer and voters evaluate the fork-choice function before proposing and voting, respectively. The proposer extends the resulting head, and validators vote accordingly.

3SF uses a refined fork-choice function based on RLMD-GHOST.

#### Vanilla RLMD-GHOST

[![](https://ethresear.ch/uploads/default/original/3X/b/d/bd646814e2c646ce71431c37578bb66e688a8f88.png)948×488 31.1 KB](https://ethresear.ch/uploads/default/bd646814e2c646ce71431c37578bb66e688a8f88)

The RLMD-GHOST function processes the view V by applying filters to:

- Remove equivocating votes (\text{FIL}_{\text{eq}}),
- Discard expired messages (\text{FIL}_{\eta-\text{exp}}),
- Retain only the latest vote per validator (\text{FIL}_{\text{lmd}}).

From the filtered set, the algorithm walks from B_{start} (usually the latest justified checkpoint) by repeatedly choosing the child with the highest weight, defined by votes for that block and its descendants. The walk stops at a block with no children.

#### RLMD-GHOST with Payload Awareness

We now refine this algorithm to account for [payload availability under proposer-builder separation](https://github.com/fradamt/consensus-specs/blob/epbs-payload-bit/specs/_features/eip7732/fork-choice.md). Observe that the specification of ePBS included in this section very closes matches the *current* proposal of ePBS.

Observe a key difference in the VOTE message compared to the original RLMD-GHOST paper. In the original proposal, validators cast VOTE messages for the head of the canonical chain along with the FFG component. The head is identified directly by the block, and a vote takes the form: [\text{VOTE}, B, \mathcal{C}_1 \to \mathcal{C}_2, t, v_i], where B is a pair (b, p), with b denoting the block root and p the slot in which the block was proposed. Here instead, the VOTE message is slighly modified. Specifically, a VOTE message is now of the form [\text{VOTE}, (B,a), \mathcal{C}_1 \to \mathcal{C}_2, t, v_i], where a represents the *status* of the block as seen by the validator while casting the vote, as we discuss in details below.

In our setting, we denote a block by B, with B.\text{slot} indicating its slot and B.\text{parent} its parent. We represent B.\text{parent} as the pair (B', s'), where B' is the parent block of B and s' is the availability status of $B’$’s payload: FULL if the payload is available and has been released (e.g., by the builder), or EMPTY if it is unavailable, such as when it has not been released. Equivalently, B = B'.\text{parent}.\text{block} and s' = B'.\text{parent}.\text{status}. A block cannot certify its own availability – it can only assess its parent’s label. Availability statuses (FULL/EMPTY) are relevant for execution and censorship-resistance, and blocks contain only a hash commitment to the payload rather than the payload itself. For the fork-choice function, we instead work with block-tree nodes (or simply nodes) N = (B, \text{status}), where B is a block and \text{status} is one of COMMITTED, FULL, or EMPTY. Here, COMMITTED represents the block independently of its payload and is particularly relevant for the finality mechanism, which operates solely on the chain’s structure. Blocks are initially treated as COMMITTED and may later acquire a FULL or EMPTY status depending on whether the payload becomes available during execution.

[![](https://ethresear.ch/uploads/default/optimized/3X/9/a/9a19a0737f294e23d67c7665dd99a6422ef5bd28_2_427x500.png)1128×1318 103 KB](https://ethresear.ch/uploads/default/9a19a0737f294e23d67c7665dd99a6422ef5bd28)

Initially, B_{start} is treated as COMMITTED. Its FULL and EMPTY interpretations are then explored as child options.

If B is COMMITTED, the algorithm splits it into two artificial children: one interpreting the block as if its payload was available (FULL) and one as if it was not (EMPTY). These are not real blocks but logical branches used to evaluate both possible payload interpretations. The fork-choice then proceeds along the heavier of the two.

If B is not COMMITTED (i.e., it is either FULL or EMPTY), then its children are actual blocks in the view \mathcal{V} that:

- extend B,
- were proposed no later than slot t, and
- preserve the same payload interpretation, meaning their status equals N.\text{status}.

This constraint ensures that once the walk commits to an interpretation of the payload (available or not), it consistently follows that interpretation through the subtree – preventing ambiguous transitions between FULL and EMPTY views.

Weight is computed using w(N, \mathcal{V}, t). If the block associated with the node N was proposed at slot t-1, the function uses AC votes to determine payload availability through \text{ac_payload_present}. Specifically, \text{ac_payload_present} return whether the payload was voted as present by the AC during slot t-1, and was locally determined to be available.

- If availability is confirmed and B is FULL → return weight 1.
- If not confirmed and B is EMPTY → return weight 1.
- Otherwise → return 0.

In all other cases, weight is defined as the sum of effective balances of validators whose latest, non-equivocating and unexpired vote supports block B as the head of the chain.

A vote supports B if either:

- It directly targets N.\text{block} and indicates a payload status matching N.\text{status} (i.e., votes for the FULL version contribute only to the FULL node, and similarly for EMPTY), or
- It targets a descendant of B that sees B as its ancestor at slot B.\text{slot}, and either B is committed or the descendant assigns B the same payload status.

Ties between candidate children are broken deterministically in the following order:

1.	Prefer the block with higher weight,

2.	Then prefer lexicographically greater block root,

3.	Then prefer FULL over EMPTY.

This version handles ambiguity around payload availability cleanly, with no need for proposer boost, relying solely on vote weight and message availability.

**tl;dr.**

We start from the latest justified checkpoint and treat it as COMMITTED. Then we split it into two versions: FULL and EMPTY.

For each, we walk down the chain by always selecting the heaviest child that matches the current payload status.

Weight is computed from votes that either directly target the node or descend from it and observe it with the same status.

Once both FULL and EMPTY branches are exhausted, we return the heavier of the two as the final head.

### Proposer Logic

Finally, the proposer of slot t runs the fork-choice function. If the head is not from slot t, it simply builds on top of it. If it is from slot t, the proposer checks the AC votes. If a majority affirms availability and the IL checks pass, it extends the FULL version; otherwise, the EMPTY version.

To protect this decision, the proposer includes all AC votes it knows. Attesters consider both pre-Freeze votes and those included in the beacon block, guarding against late adversarial votes.

## Final Observations

A careful reader may notice that we have not formally proven that the integration of 3SF with FOCIL, ePBS, and PeerDAS preserves all of 3SF’s original properties. We intentionally omit a full proof here to maintain a high-level focus in this blog post. However, we strongly believe that, under appropriate assumptions, the addition of these mechanisms does not compromise the security or liveness guarantees of 3SF.

At a high level, both FOCIL and ePBS rely on the same core technique used in 3SF to mitigate adversarial behavior – namely, the [view-merge mechanism](https://ethresear.ch/t/view-merge-as-a-replacement-for-proposer-boost/13739). Specifically, during the Freeze phase, both FOCIL and ePBS impose deadlines after which validators stop processing local inclusion lists, votes, or messages from the Attestation Committee. This ensures that adversarial behavior specific to FOCIL and ePBS is mitigated using the same techniques that protect the vanilla 3SF protocol against liveness and safety attacks.

One critical property inherited from RLMD-GHOST and preserved in 3SF is reorg resilience: under synchrony, once an honest proposer proposes a block, that block will not be reorged and will remain permanently in the canonical chain. Our aim is to ensure that this property remains intact after the integration of mechanisms like FOCIL.

A potential risk introduced by FOCIL is that, due to the local construction and dissemination of inclusion lists during slot t, validators in slot t+1 might end up voting for a different head – possibly leading to a reorg of the block proposed at slot t. However, this scenario is prevented by

1. the Freeze-phase deadline, which bounds the time during which validators process locally built ILs, and
2. the fact that FOCIL requires honest validators to reject a valid block B only if it does not contain at least one transaction tx that is part of the ILs for which  \text{invalid}(B,tx)=\text{FALSE}, where \text{invalid}(B,tx) is a function such that, taken any list of transaction txs, then it is possible to build a valid block B such that, for any tx in txs, either tx \in B, or \text{invalid}(B,tx) = \text{TRUE}.

Due to (1) validators voting in slot t+1 will stop accepting ILs before the next builder constructs their block, ensuring that the proposer’s view of ILs is a superset of any individual validator’s view. As a result, the proposer will impose (by design of the 3SF protocol) its view on the voters when proposing the block, guaranteeing that the voters’ views converge with the proposer’s. Then, given that (2) ensures that an honest proposer can always create a block that is not going to be rejected by honest validators, the block proposed at slot t is not reorged, preserving reorg resilience even in the presence of FOCIL.

This is precisely the same reasoning used in RLMD-GHOST to argue resistance against reorgs and attacks such as balancing attacks.

Another crucial property we want to have is that under synchrony, any transaction observed by honest validators in the IL committee will be included in the next block unless the block is full or the transaction is invalid. This property is guaranteed because, as mentioned above, validators do not vote for a block B if tx \notin B \land \text{invalid}(B,tx)=\text{FALSE}.

A more rigorous analysis is ongoing and will be shared in a forthcoming posts.

### Future Works

The overview presented in this post offers an informal discussion on why ePBS, FOCIL, and PeerDAS do not interfere with the core properties of 3SF – under the right assumptions. In addition to synchrony, a crucial assumption we make is full validator participation. However, in practice, 3SF builds on RLMD-GHOST, which is a dynamically available consensus protocol – that is, it tolerates temporary validator inactivity without halting the chain.

This introduces an important challenge: the current mechanism assumes that builders release the payload once they observe 60\% of the validator set attesting to the block. But if only, say, 30\% of validators are online in a given slot, this threshold may never be reached, even in the absence of adversarial behavior.

A necessary future direction is to design fallback mechanisms that allow builders to safely release payloads even when participation is low, while preserving the protocol’s incentive alignment and safety guarantees. We leave this exploration for future work and further discussion.
