---
source: ethresearch
topic_id: 20943
title: Orbit SSF in Practice
author: Giulio2002
date: "2024-11-07"
category: Proof-of-Stake
tags: [single-slot-finality]
url: https://ethresear.ch/t/orbit-ssf-in-practice/20943
views: 441
likes: 3
posts_count: 1
---

# Orbit SSF in Practice

I would like to thank [@fradamt](/u/fradamt) and [@potuz](/u/potuz) for their review and insights

We propose an approach for implementing the Orbit method for Single Slot Finality (SSF) with minimal adjustments to the base Ethereum protocol. This proposal simplifies committee formation by using a single control parameter, `ETH_CEIL`, for validator sampling.

## Introduction to Orbit SSF

Orbit SSF aims to achieve single-slot finality (SSF) in the Ethereum network by optimally selecting validators for committee formation. SSF allows Ethereum to finalize blocks within a single slot, significantly enhancing finality speed and network security. As the validator count and concentration of high-balance validators (e.g., from entities like Coinbase or Lido) increase, Orbit offers an efficient and balanced way to sample validators, reducing bandwidth requirements while maintaining economic security and robustness.

### Orbit SSF and MaxEB

The protocol operates under the assumption that MAXEB (Maximum Effective Balance) has been implemented, creating a predictable validator landscape. MAXEB establishes a balance cap of 2048 ETH per validator, concentrating economic weight among fewer, larger validators. By leveraging the security of high-balance validators, the protocol achieves robust finality without imposing high network overhead.

## Idea of a Specification

Our goal is to start thinking about a minimally invasive implementantion of Orbit SSF within the Ethereum 2.0’s consensus framework. Thus, We will focus on modifying:

- Committee Selection
- Attestation Format

Additionally, we explore how clients can perform an epoch transition every slot without falling out of sync.

### Changes in Committee Selection

Orbit’s committee selection method deviates from purely random sampling, employing a “weighted-by-balance” randomness approach. This method adjusts validator inclusion probability based on each validator’s balance, capped by `ETH_CEIL`.

| Constant | Description | Value/Unit |
| --- | --- | --- |
| ETH_CEIL | Balance ceiling used to calculate validator inclusion probability | 2048 ETH |

#### Committee Selection Process

1. Generate random numbers for each validator:
Generate a unique random number for each validator’s inclusion decision. This random number, limited to a 16-bit space, is based on the current epoch’s mix.

```python
def get_random_numbers_for_orbit_sampling(state: State) -> Sequence[uint64]:
    epoch = get_current_epoch(state)
    seed = get_seed(state, epoch, DOMAIN_ORBIT_COMMITTEE)
    expanded_seed = b''.join(
        hash(seed + to_bytes(i))
        for i in range((len(validators) + 15) // 16)
    )
    return [from_bytes(expanded_seed[i:i+2]) for i in range(0, len(validators)*2, 2)]
```
2. Calculate inclusion probability based on balance:
Using ETH_CEIL as the sole parameter, we calculate the probability for each validator to be included in the committee.
 By adjusting ETH_CEIL, we control the maximum inclusion probability. A higher ETH_CEIL decreases the probability of validators with balances near the MaxEBcap, whereas a lower ETH_CEIL increases the committee size by increasing the inclusion of validators.
3. Determine committee inclusion:
A validator’s inclusion is determined by the following inequality:

\frac{M_{i} \times \text{ETH}_{\text{ceil}}}{\min(\text{ETH}_{\text{ceil}}, \text{validator}_{\text{balance}})}  Set[ValidatorIndex]:
    assert epoch in (get_previous_epoch(state), get_current_epoch(state))
    epoch_participation = (
        state.current_epoch_participation if epoch == get_current_epoch(state) else state.previous_epoch_participation
    )
    active_validator_indices = get_active_validator_indices(state, epoch)
    participating_indices = [
        i for i in select_committee(state) if has_flag(epoch_participation[i], flag_index)
    ]
    return set(filter(lambda index: not state.validators[index].slashed, participating_indices))
```

With this change, only committee members are processed for inactivity scores, penalties, and rewards. Similarly, only committee members are considered in justification bits and related processes.

#### Finality Condition

Finality is achieved when `66%` of the Orbit committee attests to a slot. In case of non-finality, the protocol falls back to LMD-GHOST.

### Epoch Transition Every Slot

In a post-MAXEB world, where the active validator set is expected to decrease significantly, epoch transitions may have reduced overhead. However, generating fresh random numbers each slot remains essential to maintain committee integrity. To achieve this efficiently, clients can precompute random numbers for the next slot during idle periods within the current slot, ensuring they are ready for the transition.

### Potential Optimization with SSF

SSF allows for protocol simplifications depending on the post-MAXEB validator set structure. as a matter of fact, by sampling only a subset of validators, the protocol can reduce attestation-related traffic and get rid of the aggregation layer. This enables the potential removal of aggregators, streamlining the protocol and freeing up additional slot time for block verification.

**NOTE:** at this time this is quite unclear if this is a feasible path.

## Future Work:

As MAXEB concentrates validator balances, we will need to conduct an analysis to assess how these changes impact the robustness and resilience of the protocol. Such as how, as the validator set consolidates,  how effectively Orbit SSF can maintain economic security and robust finality guarantees. This includes examining any adjustments needed to preserve Ethereum’s security standards.
