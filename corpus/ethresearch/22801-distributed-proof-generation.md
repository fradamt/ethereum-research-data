---
source: ethresearch
topic_id: 22801
title: Distributed Proof Generation
author: jbaylina
date: "2025-07-23"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/distributed-proof-generation/22801
views: 290
likes: 4
posts_count: 1
---

# Distributed Proof Generation

# Distributed Proof Generation Specification on top of a consensus protocol like Ethereum

## Overview

This specification defines a distributed proof generation protocol integrated with Ethereum (or any consensus protocol), introducing two distinct roles:

- Validators: Existing Ethereum validators who participate in block consensus and verify submitted zk-proofs.
- Provers: A new role, separate from validators, responsible for generating zk-proofs using GPUs. Provers are required to stake separately from Ethereum validators.

The system is designed to ensure timely, redundant, and verifiable proof generation through an incentivized multi-phase protocol (T1–T5).

## Variables

```auto
// Numbers needs to be adjusted, they are just some initial ideas.

PROVERS_PER_PROOF = 200
PROVERS_PER_AGGPROOF = 5

REWARD_FULL_PROOF_PROVER_T1 = 9000 // Reward received by each selected prover in T1 if a valid FullProof is submitted.
REWARD_FULL_PROOF_SENDER_T1 = 50 // Reward received by the prover who sends a valid FullProof in T1.
REWARD_FULL_PROOF_VALIDATOR_T1 = 1000
REWARD_T1_VALIDATOR = 3
PENALTY_T1_PROVER = -1

REWARD_FULL_PROOF_PROVER_T2 = 8000
REWARD_FULL_PROOF_SENDER_T2 = 40
REWARD_FULL_PROOF_VALIDATOR_T2 = 900
REWARD_T2_VALIDATOR = 3
PENALTY_T2_PROVER = -3

REWARD_PROVER_REUSING_T3 = 40
REWARD_PROVER_REUSED_T3 = 40
REWARD_PROVER_T3 = 50
REWARD_VALIDATOR_T3 = 1
PENALTY_PROVER_T3 = -1
PENALTY_PROVER_NOTREUSED_T3 = -1

REWARD_PROVER_REUSING_T4 = 30
REWARD_PROVER_REUSED_T4 = 30
REWARD_PROVER_T4 = 40
REWARD_VALIDATOR_T4 = 1
PENALTY_PROVER_T4 = -2
PENALTY_PROVER_NOTREUSED_T4 = -1

REWARD_PROVER_REUSING_T5 = 20
REWARD_PROVER_REUSED_T5 = 20
REWARD_PROVER_T5 = 40
REWARD_VALIDATOR_T5 = 1
PENALTY_PROVER_T5 = -4
PENALTY_PROVER_NOTREUSED_T5 = -1

REWARD_AGG_PROOF_PROVER = 50
REWARD_AGG_PROOF_VALIDATOR = 3
```

## Prover Selection and Assignment

- For each new block, a deterministically random subset of provers is selected using a mechanism such as RANDAO.
- The number of selected provers depends on the block’s gas usage:

```auto
num_provers_selected = Min(PROVERS_PER_PROOF, availableProvers / 2)
```

- Each selected prover is randomly assigned a set of partial proofs (sub-tasks) to generate, distributed with a redundancy factor:

```auto
num_airs_assigned = (num_of_partial_proofs / num_provers_selected) * redundancy_factor
```

- The assigned partial_proofs of each selected prover are determined random-deterministically after the count & plan phase.
- Provers with a strong history of valid submissions may have an increased (but bounded) probability of being selected in future rounds.
- A prover may only be assigned to one proof at a time.

## Multi-phase Proof Generation

### T1: Challenge Commitment Phase

- All selected provers must:

Commit to the signed challenge (e.g., a polynomial commitment of the sub-AIRs they are responsible for constructing).
- Optionally submit a full proof.

Only **one transaction per prover** is allowed. The proof must include the prover’s **public key** as a public output to prevent proof stealing.

#### Incentives:

- If a valid full proof is submitted in T1:

REWARD_FULL_PROOF_PROVER_T1 for each selected prover.
- REWARD_FULL_PROOF_VALIDATOR_T1 for the validator.
- REWARD_FULL_PROOF_SENDER_T1 extra for the prover submitting it.

Otherwise:

- REWARD_T1_VALIDATOR × valid commitments for validators.
- PENALTY_T1_PROVER for provers who fail to commit.

### T2: Partial Proof Submission Phase

- All selected provers must:

Submit their partial proof, referencing the challenges from T1.
- Optionally submit a full proof.

#### Incentives:

- If a valid full proof is submitted:

REWARD_FULL_PROOF_PROVER_T2 for each selected prover.
- REWARD_FULL_PROOF_VALIDATOR_T2 for validators.
- REWARD_FULL_PROOF_SENDER_T2 extra for the submitting prover.

Otherwise:

- REWARD_T2_PROVER for provers submitting valid partial proofs.
- PENALTY_T2_PROVER for failed submissions.
- REWARD_T2_VALIDATOR × valid partials for validators.

### T3: Full Proof Aggregation Phase

- Any prover may submit a full proof, including a BloomHash summarizing reused partial proofs.

#### Rewards:

- REWARD_PROVER_REUSING_T3 × reused partials
- REWARD_PROVER_REUSED_T3 × times reused by others
- PENALTY_PROVER_NOTREUSED_T3 × times not reused by others
- If many valid full proofs are submitted, the above rewards are averaged among them.
- REWARD_PROVER_T3 for the submitting prover.
- REWARD_VALIDATOR_T3 × valid full proofs
- PENALTY_PROVER_T3 for non-participation.

### T4 / T5: Fallback Aggregation Phases

- If T3 fails to finalize a valid proof:

Enter T4, then T5 if needed.
- Retry with the same or new prover set (if T5 fails).
- Rewards/Penalties are as in T3 but adjusted (decreased/increased) by a defined percentage.

## Extension for Multiple Sub-blocks (Gigagas)

- The number of sub-blocks is limited by system caps and prover availability.
- One prover set is assigned per sub-block. The protocol above applies independently per sub-block.
- A group of PROVERS_PER_AGGPROOF provers is also selected to aggregate sub-blocks into a full block.

### In T1:

- Selected provers may submit an AggProof for the block.

#### Incentives:

- REWARD_AGG_PROOF_PROVER per aggregator prover.
- REWARD_AGG_PROOF_VALIDATOR per validator including an AggProof.
