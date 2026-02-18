---
source: magicians
topic_id: 24850
title: "EIP-7990: RUNCODE Opcode – Execute arbitrary bytecode from memory within the same execution context"
author: camax
date: "2025-07-19"
category: EIPs > EIPs core
tags: [evm, opcodes]
url: https://ethereum-magicians.org/t/eip-7990-runcode-opcode-execute-arbitrary-bytecode-from-memory-within-the-same-execution-context/24850
views: 181
likes: 5
posts_count: 3
---

# EIP-7990: RUNCODE Opcode – Execute arbitrary bytecode from memory within the same execution context

## Summary

This EIP proposes a new `RUNCODE` opcode that enables execution of arbitrary bytecode from memory within the same execution context. This complements `DELEGATECALL` by providing an alternative for scenarios where dynamic code doesn’t need to be permanently stored on-chain, offering significant gas savings.

[EIP-7990](https://github.com/ethereum/EIPs/pull/10036)

## Key Benefits

- Alternative to DELEGATECALL: Provides option for temporary/generated code that doesn’t require permanent on-chain storage
- Gas Optimization: Saves up to 2,600 gas per execution by eliminating cold address access costs
- Reduced Blockchain Bloat: Avoids deploying temporary bytecode as contracts, reducing state growth
- Deployment Savings: Eliminates need to deploy ephemeral code as contracts (~32,000+ gas savings per deployment)
- Context Preservation: Maintains identical execution context as DELEGATECALL while operating from memory

## Use Cases

- Runtime code generation and execution without permanent deployment
- One-time complex calculations that don’t justify permanent contract storage
- Temporary computational libraries that change frequently
- Meta-programming patterns where bytecode is generated dynamically
- Mathematical computation libraries that generate optimized bytecode on-demand

## Discussion Goals

Prior to opening a pull request to the EIPs repository, this proposal seeks community feedback on:

- Real-world use cases where RUNCODE provides significant value
- Any overlooked security implications compared to DELEGATECALL
- Whether any opcode restrictions should be applied within RUNCODE
- The appropriateness of the proposed 100 gas base cost

Comments, concerns, and alternative perspectives are highly encouraged.

— **Alan Bojorquez** ([@camax](https://x.com/keccamaxk256))

## Replies

**Shkedo** (2025-07-23):

This can be useful but security-wise, I think this is a big risk.

Right now code exists on chain which:

a. Allows users to see the contract’s code that they sign on.

b. Maintain control over execution of arbitrary code. The only code that can be run is the code that the developer deployed (even if he uses DELEGATECALL it’s still explicitly intended by the smart contract). By emitting this, you will subject yourself to all sorts of new issues and vulnerability potential.

---

**camax** (2025-07-23):

I fully agree that the security implications are significant.

Introducing an opcode that allows arbitrary bytecode execution definitely expands the attack surface, so any benefit must clearly outweigh this new risk.

One potential way to reduce the risk would be to **limit the execution context**, similar to how `STATICCALL` prevents state modifications:

- No state writes (SSTORE, SELFDESTRUCT, etc.)
- No value transfers
- Purely read-only execution that just returns a result

With such a sandboxed approach, we still get some interesting possibilities without exposing the full danger of arbitrary execution.

---

While exploring possible use cases, I thought about something *inspired by* how Bitcoin scripts work.

A **sandboxed, read-only version** of this opcode could enable things like:

- One-off, lightweight validation logic included in a transaction
- Custom signature checks (e.g. Schnorr/BLS) without deploying a verifier contract
- Simple hashlocks or timelocks directly in the spending transaction

It wouldn’t be a 1:1 replication of Bitcoin scripts, but it could bring some of that **ephemeral validation flexibility** without leaving a permanent footprint on-chain.

