---
source: magicians
topic_id: 27402
title: "ERC-8118: Agent Authorization"
author: 0xvimer
date: "2026-01-09"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-8118-agent-authorization/27402
views: 228
likes: 3
posts_count: 9
---

# ERC-8118: Agent Authorization

## Abstract

ERC-8118 defines a standard interface for authorizing autonomous agents (bots, AI systems, or automated accounts) to perform specific on-chain actions on behalf of users (principals).

**Pull Request**:



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1450)














####


      `master` ← `WORLD3-ai:erc-agent-authorization`




          opened 12:24AM - 06 Jan 26 UTC



          [![](https://avatars.githubusercontent.com/u/191608781?v=4)
            0xvimer](https://github.com/0xvimer)



          [+558
            -0](https://github.com/ethereum/ERCs/pull/1450/files)







## Abstract

  This ERC defines a standard interface for authorizing autonomou[…](https://github.com/ethereum/ERCs/pull/1450)s agents (bots, AI systems, or automated accounts) to perform specific on-chain actions on behalf of users (principals).

  ## Motivation

  As autonomous AI agents become more prevalent in blockchain ecosystems, a standardized interface for delegation is needed. Existing delegation mechanisms (like token approvals) are either too broad or too narrow. This standard provides a balanced approach suitable for autonomous agent scenarios.

  ## Key Features

  - **Time-bound authorizations**: Optional start and end timestamps
  - **Usage-limited authorizations**: Maximum call count with automatic revocation
  - **Function-level granularity**: Permissions scoped to specific function selectors
  - **Cryptographic consent**: Agents must sign consent via EIP-712
  - **Single-principal constraint**: Each agent serves only one principal at a time

  ## Use Cases

  - Automated trading agents
  - Gaming NPCs
  - DeFi position management
  - DAO proposal execution
  - Subscription services
  - Cross-chain relayers

  ## Production Validation

 This standard has been validated through production deployment:
  - 1M+ unique wallets
  - 5.7M+ transactions without custody violations
  - Peer-reviewed at 7th Conference on Blockchain Research & Applications for Innovative Networks and Services (BRAINS 2025), Zurich, Switzerland

  ## Dependencies

  - EIP-165 (Interface Detection)
  - EIP-712 (Typed Structured Data Signing)
  - EIP-1271 (Contract Signature Validation)

  ## Checklist

  - [x] Specification follows ERC format
  - [x] CC0-1.0 license
  - [x] RFC 2119/8174 keywords
  - [x] EIP-165 interface IDs computed
  - [x] Reference implementation available












## Key Features

- Time-bound authorizations: Optional start and end timestamps
- Usage-limited authorizations: Maximum call count with automatic revocation
- Function-level granularity: Permissions scoped to specific function selectors
- Cryptographic consent: Agents must sign consent via EIP-712
- Single-principal constraint: Each agent serves only one principal at a time

## Motivation

As autonomous AI agents become more prevalent in blockchain ecosystems, a standardized interface for delegation is needed. Existing mechanisms are either too broad (unlimited token approvals) or too narrow (single-use signatures). This standard provides a balanced approach for autonomous agent scenarios.

### Use Cases

- Automated trading agents
- Gaming NPCs
- DeFi position management
- DAO proposal execution
- Subscription services
- Cross-chain relayers

## Production Validation

This standard has been validated through production deployment:

- 1M+ unique wallets
- 5.7M+ transactions without custody violations
- Peer-reviewed at 7th Conference on Blockchain Research & Applications for Innovative Networks and Services (BRAINS 2025), Zurich, Switzerland

We welcome feedback and discussion on the specification.

---

Authors: WORLD3 Team (@world3-ai)

## Replies

**blackalbino01** (2026-01-09):

interesting to see such features, thinking about error handling and if there is any restrictions to amount of retries.

---

**0xvimer** (2026-01-12):

Thanks for raising this ,and we  think it’s a good point to clarify.

Error handling

The specification defines explicit custom errors for all failure conditions:

- InvalidAgentAddress, InvalidSelector, ZeroCallsNotAllowed, ValueExceedsBounds (input validation)
- SignatureExpired, InvalidSignature (signature verification)
- AgentAlreadyBound, NoAuthorizationExists, NotAuthorized (state validation)

Per EVM semantics, if a protected call reverts, the entire transaction reverts and any state changes (including a remainingCalls decrement) are rolled back. The remainingCalls counter is only consumed on successful execution.

Retry restrictions

The allowedCalls parameter sets the initial value of remainingCalls. Per the specification:

- Each successful call through a protected function MUST decrement remainingCalls by one
- When remainingCalls reaches 0, the authorization MUST be automatically revoked
- Failed calls (reverts) do not consume this allowance

An agent can therefore retry until:

1. A call succeeds (consuming one unit)
2. The validity window ends (endTime)
3. The principal explicitly revokes the authorization

This is an intentional design choice: principals limit successful completions, not attempted executions.

Thank you again, and we welcome any further feedback.

---

**blackalbino01** (2026-01-12):

thank you for taking your time to clarify. [@0xvimer](/u/0xvimer)

---

**SamWilsn** (2026-01-23):

I haven’t read your entire proposal yet, but from the abstract and motivation, it sounds vaguely similar to [ERC-7291: Purpose bound money](https://eips.ethereum.org/EIPS/eip-7291). Have you looked into it and its descendants?

---

**SamWilsn** (2026-01-23):

Looking at your EIP-1271 flow, how do you pass in the authorizing address? Unlike with `ecrecover`, you need to provide the address to validate against.

Edit: wait, what? Why is the principal `msg.sender` when you also provide a `signature`? `msg.sender` should always be authorized to take an action without a signature—it’s the account making the call! You only need a signature when a third party is relaying a call. Unless I’m missing something significant?

---

**0xvimer** (2026-01-26):

Thank you for the reference. We’ve reviewed [ERC-7291 (Purpose Bound Money)](https://github.com/ethereum/ERCs/blob/master/ERCS/erc-7291.md) and while both standards involve authorization constraints, they address fundamentally different problems:

**ERC-7291 (Purpose Bound Money):**

- An ERC-1155 wrapper around a store-of-value token (e.g., stablecoin)
- Defines how/where the underlying value can be redeemed or unwrapped (merchant allowlists, compliance conditions)
- The constraint is on spending/redemption conditions of the wrapped asset
- PBM tokens themselves can be bearer/transferable; restrictions apply at unwrapping time

**ERC-8118 (Agent Authorization):**

- Authorizes who can act on behalf of a principal on a specific contract
- Controls what functions an agent can call (by selector), for how long, and how many times
- The constraint is on delegated execution permissions, scoped per-contract

The key distinction: ERC-7291 encodes spending conditions into a token wrapper, while ERC-8118 grants bounded execution rights to approved agents. They’re complementary rather than overlapping, and a contract could implement both to have purpose-bound assets managed by authorized agents.

Regarding descendants: we’ve reviewed ERC-7291 and haven’t found a PBM-related standard that overlaps with agent delegation. If there are specific follow-on proposals you’d like us to compare against, we’d be happy to take a look.

---

**0xvimer** (2026-01-26):

In ERC-8118, the signer is the **agent** (not the principal), so the agent address is already known from the function call—it’s passed explicitly as a parameter to `authorizeAgent(address agent, ...)`.

The key line in the reference implementation is:

```solidity
SignatureChecker.isValidSignatureNow(agent, hash, signature)
```

This OpenZeppelin utility handles both signature types:

- EOA agents: Attempts ECDSA recovery and compares the recovered address against agent
- Contract agents: Calls IERC1271(agent).isValidSignature(hash, signature) on the agent contract

Importantly, `principal = msg.sender` is baked into the EIP-712 signed digest (as part of `AgentConsent`), so a third party cannot reuse the agent’s signature with a different principal. The signature is also domain-separated by `verifyingContract` and `chainId` to prevent cross-contract and cross-chain replay.

Also here, the signature is from the **agent**, not the principal.

The principal (`msg.sender`) is already authenticated by making the call. Hence, no signature needed there. The agent, however, must sign an `AgentConsent` message to confirm they agree to be authorized. This creates a mutual consent model.

Why do we need agent consent? ERC-8118 has a single-principal constraint: each agent can only serve one principal per contract at a time. Without requiring the agent’s signature, anyone could “claim” an address as their agent and block it from serving its intended principal—essentially a DoS vector. The Rationale section covers this under “Agent Consent Requirement.”

Note that this signature is only needed when creating or escalating an authorization. Once authorized, the agent executes actions normally as `msg.sender`, and no signature required for each call.

If you’re thinking about relayed or gasless authorization, that would be a meta-transaction or account abstraction concern, which is outside the scope here. The signature in ERC-8118 is purely for agent opt-in.

I hope this response addresses your concern, and I am more than happy to clarify further if I misunderstood your question or missed any part.

---

**SamWilsn** (2026-01-28):

Ahhhh, that makes a lot more sense. Thank you!

