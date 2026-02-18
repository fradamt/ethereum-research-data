---
source: magicians
topic_id: 19471
title: "ERC-7746: Composable Security Middleware Hooks"
author: peersky
date: "2024-04-01"
category: ERCs
tags: [solidity, proxies]
url: https://ethereum-magicians.org/t/erc-7746-composable-security-middleware-hooks/19471
views: 888
likes: 2
posts_count: 4
---

# ERC-7746: Composable Security Middleware Hooks

This EIP proposes a standard interface, `ILayer`, for implementing composable security layers in smart contracts. These layers act as middleware, enabling runtime validation of function calls before and after execution, independent of the protected contract’s logic. This approach facilitates modular security, allowing independent providers to manage and upgrade security layers across multiple contracts.

The Security Layers Standard introduces a modular approach, enabling:

- Independent Security Providers: Specialized security providers can focus on developing and maintaining specific security checks.
- Composable Security: Layers can be combined to create comprehensive security profiles tailored to individual contract needs.
- Upgradability: Security layers can be updated without requiring changes to the protected contract.
- Flexibility: Layers can perform a wide range of validation checks, including access control, input sanitization, output verification, and more.

Practical need for such generic solution is fact that we must find some mean of generic, industry-wide solution to coupe with incidents on-chain.

Proposed solution is O(1) way to  disable vulnerabilities for the large ecosystems, while it also generalizes needs such as Pre/Post validation of paymasters in ERC4337, which could be well generalized under this case.

https://github.com/ethereum/ERCs/pull/543

Use cases for such technology arises from experience working with off-chain monitoring and incident management, as well as work on Ethereum Distribution System: [GitHub - peeramid-labs/eds: Ethereum Distribution System](https://github.com/peersky/eds)

## Replies

**peersky** (2024-04-17):

# Layered philosophy - security is an onion

Below you can find image, illustrating what a traditional security onion might look like on-chain, formalising the fact we have needs to understand questions like “Who sends transaction”, “What are permissions of sender”, “Is this behaviour undesired”.

[![Screenshot 2024-07-18 at 10.01.02](https://ethereum-magicians.org/uploads/default/optimized/2X/e/e691ac2be732955d5a0c04d567113da8e8b631c6_2_690x292.png)Screenshot 2024-07-18 at 10.01.021216×516 23.3 KB](https://ethereum-magicians.org/uploads/default/e691ac2be732955d5a0c04d567113da8e8b631c6)

In this philosophy, the great thing is that smart contract developer life could become much easier, by enabling developers to take care of functional requirements of smart contracts, while access and permissioning of such can be managed by wrappers performing specific tasks.

For example, in the proof of concept repository [GitHub - peersky/smart-contract-layers: layered security approach for securing and improving ux](https://github.com/peersky/smart-contract-layers/)

introduced is a simple layer that demonstrates protection against smart contract drainage by vulnerability that requires multiple calls to fully dilute the treasury.

Simple rate limiter acts on per-customer basis, assessing rate for on-chain calls to the contract and disabling drainers.

Simply saying, such system would allow to make security checks, some of which might be sanity-ones, i.e. “Revert if transaction result is decreasing treasury”.

---

**SamWilsn** (2024-07-23):

What makes this approach better than using calls to implement layers?

The “protected contract” could have an “authorized address” that is allowed to access the protected methods, and the “layers” would simply chain calls into the protected contract.

I’m sure there *are* benefits to doing it the way you’re proposing, but it might be nice to have that comparison in the proposal.

---

**peersky** (2024-08-03):

There are few important reasons in my view:

1. Specification Encapsulation: Security Specs vs Functional Specs can be written down and implemented by different groups more easily.
2. Better horizontal scaling: Instead of having each contract to host own security stack, we refer to a separate location which may serve numerous protected contracts. The configuration parameter in the call is intended to act as header that allows client to personalize server logic.
3. Generic interface: This allows to generalise needs for calling 3rd party for an approval. The bright use case would be paymaster validation in ERC4337. This ERC could offload some of complexity there by moving Paymaster and User Operation Validation Interfaces definitions to this.
4. It is not prohibitive: Contract MAY implement ILayer for himself, resulting your proposed approach.
5. Way to manage vulnerabilities: Using this enables security oracles, who may be managed autonomously from protected contract.

