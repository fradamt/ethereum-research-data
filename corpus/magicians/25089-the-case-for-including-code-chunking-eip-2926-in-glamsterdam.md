---
source: magicians
topic_id: 25089
title: The case for including code chunking (EIP-2926) in Glamsterdam
author: gballet
date: "2025-08-13"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/the-case-for-including-code-chunking-eip-2926-in-glamsterdam/25089
views: 98
likes: 3
posts_count: 1
---

# The case for including code chunking (EIP-2926) in Glamsterdam

# Summary (ELI5)

Introduces code chunking in the MPT, and adds a gas cost each time execution/code copy accesses a new chunk. This is useful for preventing a nasty “prover killer attack” in zkvms that it’s not currently possible to defend against. It is also useful for removing the code size limit. Last but not least, it’s preparing the way for stateless Ethereum by reducing witness size.

## Detailed Justification

### Benefits

As part of the “scaling L1” roadmap of Ethereum, this EIP delivers:

- removing the code size limit, as code accesses / writes are now paid for, which means
- solves the EXTCODESIZE prover killer attack, which (besides performance) is a major roadblock towards the adoption of zkvms and zk stateless clients
- reduces the witness size as only the code chunks that are accessed need to be present in the witness. A study showcasing the benefits is available here.

### Why now?

This fixes very difficult blockers for efforts at scaling L1, which are planned for the next 2 years. By reducing the witness size, it also helps improving the UX.

### Alternative solutions

There are two alternative with this proposal:

- Introducing binary trees (eip-7864) / verkle trees (eip-6800): this is the more complete solution, which will take more time to implement as the question of the hash function is still an ongoing research and security topic.
- eip-7907, which is another attempt at raising the code limit and also introduce some gas changes to account for the increase in resource use. EIP-2926 has the same benefits as eip-7907, with the benefits of a consistent gas model, future proofiness, and addressing the prover killer issue on top of that.

## Stakeholder Impact

| stateholder | impact | description |
| --- | --- | --- |
| end users | Low | End users are unaffected as code transition occur at protocol layer. |
| app devs | Medium | Developers need to adapt to the new gas costs model. |
| wallet devs | Low | Wallet functionality remains unchanged. |
| tooling infra | Medium | Infrastructure tools need updates to handle chunk-based proofs and codeRoot fields. |
| L2s | Low | Layer 2s remain unaffected. |
| stakers | Medium | A transition period has to happen, during which  resource consumption increases slightly. |
| CL clients | Low | Core consensus rules remain unchanged. |
| EL clients | High | Requires the implementation of code transition and the new storage format for accounts. |

## Technical Readiness

This is an extract from the verkle/binary code, which is already implemented in many clients. We are at the proposal stage, so no code specific for this EIP has been written yet, but adapting existing code is a matter of a couple of weeks. Here is a table to keep track of implementation in clients:

| client | eip-4762 | eip-6800 | eip-2926 | eip-7612 |
| --- | --- | --- | --- | --- |
| besu |  |  |  |  |
| erigon |  |  |  |  |
| geth |  |  |  |  |
| nethermind |  |  |  |  |
| reth |  |  |  |  |

## Open Questions

- EIP-7703 seemed to have a much smaller gas cost than the one proposed in eip-4762. Deciding what the gas cost would be is still an open question, although the existence of eip-4762 means that there is something ready to ship in the worst case.
