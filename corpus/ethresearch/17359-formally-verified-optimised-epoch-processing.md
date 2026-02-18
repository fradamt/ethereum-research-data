---
source: ethresearch
topic_id: 17359
title: Formally-verified optimised epoch processing
author: michaelsproul
date: "2023-11-09"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/formally-verified-optimised-epoch-processing/17359
views: 2637
likes: 14
posts_count: 4
---

# Formally-verified optimised epoch processing

# Formally-verified optimised epoch processing

*By [Callum Bannister](https://github.com/onomatic) and [Michael Sproul](https://github.com/michaelsproul), Sigma Prime*.

Implementations of the Ethereum [consensus specification](https://github.com/ethereum/consensus-specs) typically make use of

algorithmic optimisations to achieve high performance. The correctness of these optimisations is

critical to Ethereum’s security, and so far they have been checked by manual review, testing and

fuzzing. To further increase assurance we are formally proving the correctness of an optimised

implementation.

This document describes the optimised implementation which we are in the process of verifying,

and includes a high-level argument for its correctness.

## Scope

We only consider the `process_epoch` function which is responsible for computing state changes at

the end of each 32-slot epoch. Block processing (`process_block`) is considered out of scope for now

but may be covered by future work.

Our goal is to verify an implementation of `process_epoch` containing the minimum number of O(n)

iterations over the validator set (n is the number of validators). We consider not only the

`state.validators` field, but also the other length n fields of the state including:

- .validators
- .balances
- .previous_epoch_participation
- .current_epoch_participation
- .inactivity_scores

The specification version targeted is v1.3.0, for the Capella hard fork. We anticipate that the

proofs will be able to be updated for Deneb quite easily because there are minimal changes to epoch

processing in the Deneb fork.

## Motivation

As the validator set grows the amount of computation required to process blocks and states

increases. If the algorithms from [consensus-specs](https://github.com/ethereum/consensus-specs) were to be used as-is, the running time of

`process_epoch` would be increasing quadratically (O(n^2)) as validators are added.

Another motivation for optimising epoch processing is that it grants implementations the freedom to

explore different state models. Some clients have already switched their `BeaconState`

representation from an array-based model to a tree-based model, which allows for better sharing of

data between states, and therefore better caching. The downside of the tree-based model is that it

tends to have substantially slower indexing (e.g. computing `state.validators[i]`), and

iteration is slightly slower (same time complexity with a larger constant).

| Operation | Array-based | Tree-based |
| --- | --- | --- |
| index | O(1) | O(\log n) |
| iterate | O(n) | O(c * n) |

Hence in the tree-based paradigm it becomes even more important to remove random-access indexing,

and to remove O(n^2) nested iterations which amplify the higher cost of tree-based iteration.

## Algorithm Description

For ease of keeping this post up-to-date, we link to the algorithm description in our main Git repository:

- Algorithm Description @ milestone1 tag; Nov 2023.
- Algorithm Description @ main branch; current.

## Informal Proof Sketch

- Informal Proof Sketch @ milestone1 tag; Nov 2023.
- Informal Proof Sketch @ main branch; current.

## Separation Logic Algebra

As part of this work we’ve developed an Isabelle/HOL theory for verifying the correctness of the optimised implementation (relative to the original).

It combines several layers in a novel way

- We use the Concurrent Refinement Algebra (CRA) developed by Hayes et al as the unifying language for the formal specification and refinement proof between the original and optimised implementation.
- We implement a concrete semantics of said algebra using an intermediate model of Order Ideals as bridge between CRA and a trace semantics.
- We denote programs using the Continuation Monad (roughly mimicking a Nondeterministic State Monad with failure) to provide a familiar Haskell-style syntax and simulate argument-passing in the CRA.
- We extend the notion of ordinary refinement in CRA to data refinement.
- Finally, we use Separation Logic as an assertion language, allowing reasoning about the spatial independence of operations as required for the optimised implementation to preserve the original semantics.

At the time of writing the framework is mostly complete but has a few proofs skipped (using Isabelle’s `sorry`) which we intend to revisit later.

**Links Below**

- Separation Logic Algebra @ milestone1 tag; Nov 2023.
- Separation Logic Algebra @ main branch; current.

## Implementation and Fuzzing

We have implemented the optimised algorithm on Lighthouse’s `tree-states` branch, which uses tree-based states and benefits significantly from the reduction in validator set iteration. The Lighthouse implementation closely follows the described algorithm, with some minor variations in the structure of caches, and some accommodations for Deneb which we argue are inconsequential.

The Lighthouse implementation is passing all spec tests as of v1.4.0-beta.2.

- single_pass.rs: bulk of the Lighthouse implementation; Rust.
- GitHub actions for ef-tests: Successful CI run for the Ethereum Foundation spec tests on the tree-states branch.

The Lighthouse implementation is also currently undergoing differential fuzzing against the other clients, as part of the `beaconfuzz` project. So far no bugs have been discovered.

## Next Steps

The next step is to formalise both the spec and our implementation in the separation logic framework within Isabelle/HOL, and then prove refinement following the proof sketches.

1. Port the partially-written spec code from the option monad to the new continuation monad.
2. Translate the optimised algorithm to Isabelle/HOL code following the Python algorithm description.
3. Prove refinement proceeding through the phases of epoch processing in order. Starting from process_justification_and_finalization_fast and building out supporting auxiliary lemmas as we go. The proof sketches provide high-level guidance for this step.

In parallel with the above we will also continue fleshing out the logical framework, and completing the proofs.

We plan to have this work completed by Q2 2024.

## Acknowledgements

We’d like to thank the Ethereum Foundation for a grant supporting this research, and Sigma Prime for facilitating the project.

## Replies

**saulius** (2023-11-22):

Thanks [@michaelsproul](/u/michaelsproul) for reaching us for a comment. Grandine uses parallelization, and it’s hard to prove parallel algorithms formally, so this is not something we are actively researching. But it’s really great to see this is moving forward.

Generally speaking, Grandine has similar optimizations. Some optimizations didn’t yield significant results (i.e. “Exit Cache”) so we removed it. Maybe it makes sense to roughly measure what is the impact of each optimization so that client teams can decide whether it’s worth implementing it.

A few random thoughts from the team:

# Can the exit cache be simplified?

Does `ExitCache` really need to store counts for past epochs?

Wouldn’t storing just the latest values of `exit_queue_epoch` and `exit_queue_churn` be enough?

```python
class ExitCache:
    exit_queue_epoch: Epoch
    exit_queue_churn: uint64
```

Are we missing something?

# Effective balances fit in a single byte

Effective balances are multiples of `EFFECTIVE_BALANCE_INCREMENT` with a maximum of `MAX_EFFECTIVE_BALANCE`.

The values of the two variables in mainnet and minimal presets are such that an effective balance can only have 33 distinct values.

Storing them as bytes would save memory and may speed up some operations, but the required conversions would add overhead.

We haven’t implemented this in Grandine yet, so we’re not sure if it’s worth it.

# Will increase_balance pose any problems?

Unlike `decrease_balance`, `increase_balance` does not saturate.

The letter of `consensus-specs` is that an overflow should make the entire state transition invalid.

This is not a big concern in practice[1], but we imagine it may get in the way of formal verification.

If the only goal is to prove equivalence with `consensus-specs`, this might not be a problem.

# Invalid test data may prevent optimizations

This is more of a grievance than feedback, but it may be relevant.

Some test cases in `consensus-spec-tests` contain data that is invalid or cannot be reached through state transitions[2].

For example, the `random` test cases[3] for Phase 0 contain pre-states with impossible inclusion delays, necessitating a check[4] that should not be needed in a real network.

Test cases like these restrict the optimizations possible in a compliant implementation.

[1]: There is not enough ETH in the mainnet, though a malicious testnet operator could exploit this by submitting a very large deposit.

[2]: Like a [Garden of Eden](https://en.wikipedia.org/wiki/Garden_of_Eden_(cellular_automaton)).

[3]: Only `randomized_0` as of v1.4.0-beta.2. `randomized_5` also appears to be invalid in some versions, including v1.3.0.

[4]: Albeit one with a negligible cost.

---

**michaelsproul** (2023-12-07):

Thanks for the input!

![](https://ethresear.ch/user_avatar/ethresear.ch/saulius/48/7673_2.png) saulius:

> Grandine uses parallelization, and it’s hard to prove parallel algorithms formally, so this is not something we are actively researching.

The proof framework that Callum has developed supports concurrency, but we thought we’d start with something simpler. Maybe we can sync up again in a few years if we get bored of proving sequential algorithms and want to prove something concurrent ![:stuck_out_tongue:](https://ethresear.ch/images/emoji/facebook_messenger/stuck_out_tongue.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/saulius/48/7673_2.png) saulius:

> Some optimizations didn’t yield significant results (i.e. “Exit Cache”) so we removed it.

Interesting, we’ve had an exit cache in Lighthouse for ages and it definitely provided some benefit when it was added, but I agree it would be good to re-check. I suspect it might be more beneficial for block processing than epoch processing, although with tree states it should almost always be beneficial to avoid an O(n) iteration.

![](https://ethresear.ch/user_avatar/ethresear.ch/saulius/48/7673_2.png) saulius:

> Does ExitCache really need to store counts for past epochs?
> Wouldn’t storing just the latest values of exit_queue_epoch and exit_queue_churn be enough?

You’re right! As I said this exit cache approach is a hangover from an early Lighthouse cache, where I think we were trying to keep it looking like the spec. Now that we’re proving it correct I agree it makes sense to simplify. Thanks!

![](https://ethresear.ch/user_avatar/ethresear.ch/saulius/48/7673_2.png) saulius:

> Effective balances fit in a single byte

![](https://ethresear.ch/user_avatar/ethresear.ch/saulius/48/7673_2.png) saulius:

> Storing them as bytes would save memory and may speed up some operations, but the required conversions would add overhead.

I think I tried this in LH with tree-states and it was slower than using `u64`s, but I’ll try it again and confirm. Might be a CPU <> memory trade off as you said.

![](https://ethresear.ch/user_avatar/ethresear.ch/saulius/48/7673_2.png) saulius:

> The letter of consensus-specs is that an overflow should make the entire state transition invalid.
> This is not a big concern in practice[1], but we imagine it may get in the way of formal verification.

In our Isabelle formalisation any arithmetic operation that overflows causes the entire state transition to abort, just like in consensus-specs. We’re hoping that the proofs for these cases end up not being too hard (i.e. show that the impl fails whenever the spec fails).

![](https://ethresear.ch/user_avatar/ethresear.ch/saulius/48/7673_2.png) saulius:

> Some test cases in consensus-spec-tests contain data that is invalid or cannot be reached through state transitions[2].

Part of the reason for this is that there’s no straight-forward predicate for a valid state, other than an inductive definition involving the entire state transition. With a formalisation of the state transition in hand we *may* (time permitting) be able to carve out a predicate for what a valid state looks like, which could then inform the spec tests. We’ll see.

---

**arnetheduck** (2024-03-04):

How much of this work would be reasonable to bring back to the spec itself, refactoring it along lines that make more sense for an at least reasonably optimized client?

