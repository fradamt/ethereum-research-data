---
source: ethresearch
topic_id: 19954
title: Fork Choice compliance test suites & test generator
author: ericsson49
date: "2024-07-02"
category: Consensus
tags: []
url: https://ethresear.ch/t/fork-choice-compliance-test-suites-test-generator/19954
views: 2273
likes: 3
posts_count: 1
---

# Fork Choice compliance test suites & test generator

This is a preliminary announcement, we’ll officially announce during the next All Core Devs call.

We (TxRx team, ConsenSys) have implemented a Fork Choice compliance test generator as well as have generated Fork Choice compliance test suites.

Overall F/C compliance testing methodology is described [here](https://hackmd.io/@ericsson49/fork-choice-implementation-vs-spec-testing).

In this report we briefly describe the results of the initial implementation phase (i.e. the F/C test generator and F/C test suites).  A more detailed description of the work is TBD.

This work was supported by a grant from the Ethereum Foundation.

# Implementation status

## Test generator

The initial version of the Fork Choice tests generator is implemented and currently available as a draft [consensus-specs PR](https://github.com/ethereum/consensus-specs/pull/3831). We have been focusing on minimizing efforts for client implementer teams to adopt the generated tests. The only a small change to the existing [FC test format](https://github.com/ethereum/consensus-specs/tree/dev/tests/formats/fork_choice) is the addition of a [new check](https://github.com/ericsson49/eth2.0-specs/tree/fc-compliance2/tests/formats/fork_choice#checks-step), which is safe to ignore initially.

## Test suites

We have developed test generation parameters for three suites at the moment.

| Test suite | size | Purpose | Status | Link |
| --- | --- | --- | --- | --- |
| Tiny | 135 tests | Demonstration, smoke testing | Done | link |
| Small | 1472 tests | Initial adoption, smoke testing | Done | link |
| Standard | 13240 tests | Main testing | Done | link |
| Extended | about 100K tests | Extended testing | TBD |  |

**Note**: We are able to generate the Extended test suite. However, it will take significant time (about a week), therefore, we have delayed actual test suite generation until it will be demanded.

It should be possible to generate test suites for any fork (Altair, Capella, Deneb) and preset (mainnet or minimal). However, test generation for mainnet is very slow. We have tested minimal/altair and minimal/deneb.

Test generation currently is slow (about 10-15 seconds per test on average). However, a multiprocessing mode is supported (about 2 seconds per test on Apple M1). Generation of the Standard test suite takes about 8 hours (multiprocessing mode) or two days (single process mode).

The reasons of slow performance are known and are to be alleviated in future. Currently, our top priority is to simplify adoption of the new test suites.

## Testing the tests

We have run the generated tests against [Teku](https://github.com/Consensys/teku), using Teku test runner and against the official executable Fork Choice spec (minimal/deneb), using a simple Python [test runner](https://github.com/ericsson49/eth2.0-specs/blob/4a0745bd7c0ec6d6a216a8baf81bcb80c30ccaa3/tests/generators/fork_choice_generated/test_run.py).

# Test generation approach

The test generation approach is a mix of model-based and fuzz testing.

Principles:

- the Fork Choice spec is virtually “decomposed” into two parts: topological sorting of events and actual event processing
- tests are generated for the event processing part, the topological sorting part is addressed via event shuffling (time shift plus drop/duplication)
- models are used to describe the spec aspects that we want to cover. There are two flavors: trees of various shapes (for block trees and super-majority link trees) and predicates to be covered (filter_block_tree)
- for each model there can be multiple solutions, each solution can be seen as a template (e.g. SM link tree + block tree) which can be instantiated in multiple ways (varying validator actions)
- each test case can be mutated multiple times

Tests are generated with four steps:

1. Models (implemented using MiniZinc), describing abstract coverage aspects that we want to cover. Currently there are three models: SM link (super-majority link) tree model, Block tree model and Block cover model.
2. For each model a set of solutions is produced. The models are parameterized, which affects the size of solution set generated.

SM link and block tree solutions are combined into a single block tree.
3. Each solution is instantiated using two test instantiators (block tree and block cover). The instantiation is randomized, i.e. a coin is flipped on each decision point. This results in a complete Fork Choice test case (i.e. anchor state plus a sequence of tick | block | attestation | attester_slashing events).
4. Each test case is mutated via mutation (shuffling) operators. Currently, there are thee mutation operator: time shift, drop and duplicate (with consequent shifting).

The models are developed manually.

Solutions to the models are produced with a special [generator](https://github.com/ericsson49/eth2.0-specs/blob/4a0745bd7c0ec6d6a216a8baf81bcb80c30ccaa3/tests/generators/fork_choice_generated/generate_test_instances.py).

Test instantiators and mutations are performed with [test_gen.py](https://github.com/ericsson49/eth2.0-specs/blob/4a0745bd7c0ec6d6a216a8baf81bcb80c30ccaa3/tests/generators/fork_choice_generated/test_gen.py).

After tests are generated, one can validate the produced test steps using [test_run.py](https://github.com/ericsson49/eth2.0-specs/blob/4a0745bd7c0ec6d6a216a8baf81bcb80c30ccaa3/tests/generators/fork_choice_generated/test_run.py) script, which executes the steps using the pyspecs, performing prescribed checks.

# Test structure

| Test group | size (standard suite) | parameters (solutions + variations + mutations) | description |
| --- | --- | --- | --- |
| Block tree | 4096 tests | 1024*2*(1+1) | focus on trees of varying shapes |
| Block weight | 2048 tests | 8*64*(1+3) | focus on producing block trees with varying weights |
| Shuffling | 2048 tests | 8*4*(1+63) | focus on shuffling/mutation operators |
| Attester slashing | 1024 tests | 8*16*(1+7) | focus on attester slashing |
| Invalid messages | 1024 tests | 8*32*(1+3) | focus on invalid messages |
| Block cover | 3000 tests | 60*5*(1+9) | cover various combinations of predicates from the filter_block_tree method |

# Future steps

- improve performance. Performance is adequate right now (for the initial adoption phase). But is the main blocker otherwise.
- more flexible test generation. More and better models, better instantiators, better mutation operators.
- coverage-guided fuzzing
- new test vector format (don’t need full test cases for fuzz testing, as need to compare against the FC spec anyway)
