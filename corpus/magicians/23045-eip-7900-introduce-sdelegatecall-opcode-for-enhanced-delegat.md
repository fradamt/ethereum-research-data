---
source: magicians
topic_id: 23045
title: "EIP-7900: Introduce SDELEGATECALL opcode for enhanced delegatecall security"
author: NolanWang
date: "2025-03-03"
category: EIPs > EIPs core
tags: [evm]
url: https://ethereum-magicians.org/t/eip-7900-introduce-sdelegatecall-opcode-for-enhanced-delegatecall-security/23045
views: 152
likes: 0
posts_count: 4
---

# EIP-7900: Introduce SDELEGATECALL opcode for enhanced delegatecall security

This draft EIP introduces a new EVM opcode `SDELEGATECALL` (secure delegatecall) that enhances security when executing external contract code. It functions similarly to the existing `DELEGATECALL` opcode but additionally returns the deployer’s address of the target contract, allowing the caller to verify the authenticity of the contract being called.

https://github.com/ethereum/EIPs/pull/9440

#### Update Log

2025-03-03: First Time Drafted.

#### External Reviews

None as of 2025-03-03.

#### Outstanding Issues

None as of 2025-03-03.

## Replies

**Arvolear** (2025-03-03):

Generally speaking, there are three existing use cases for a `delegatecall`:

1. Proxy/Diamond contracts.
2. Self multicall/Solidity libraries.
3. Some weird governance upgrade patterns.

In all these use cases, smart contract addresses are known beforehand. Everything else is probably an anti-pattern that shouldn’t be used. To me, this proposal promotes such anti-patterns without clear benefits. Though please correct me if I am wrong.

---

**NolanWang** (2025-03-04):

Let me address why SDELEGATECALL provides value even in scenarios where contract addresses are known:

### Security Benefits for Established Patterns

1. For Proxy/Diamond contracts:

SDELEGATECALL lets contracts verify that implementations were deployed by trusted entities, not just that they exist at expected addresses
2. Permits proxy contracts to reject execution if implementation deployer isn’t whitelisted
3. Example: Even if an admin key is compromised and implementation address changed, the proxy can still verify the deployer is authorized
4. For Libraries/Multicalls:

We can allow deployers to configure their own whitelist to verify if the return value from SDELEGATECALL matches the whitelist
5. If configuring a whitelist seems troublesome, developers can continue using delegatecall
6. The two opcodes don’t conflict with each other - it depends on the specific use case
7. For Governance Upgrades:

Adds an additional verification layer beyond address-based checks
8. Ensures new implementations come from authorized deployers, preventing governance attacks that replace implementations

### Not Promoting Anti-Patterns

Rather than encouraging delegatecall to random contracts, SDELEGATECALL actually makes established patterns more secure. It addresses the specific attack vector demonstrated in the Bybit hack, where the vulnerability wasn’t calling unknown addresses but rather compromised code at known addresses.

The core security insight: knowing an address isn’t enough when the code at that address can be maliciously replaced. SDELEGATECALL provides origin verification as an additional security layer.

---

**shemnon** (2025-03-04):

From an EVM implementation perspective there are two high level problems:

The first and lesser concern is that currently no operation results in a net add of more than one item to the operand stack. Basually all existing operations return zero or one items (modulo DUP/SWAP that may have a strange definitions, but the net is 1).  Adding an operation that adds two items will be a first for the opcodes so the level of scrutiny will be higher.

The second one is more problematic.  Clients do not track who deployed a contract and retroactively adding that info will be very expensive, requiring a re-evaluation of the entire chain. This would impact verkle/stateless work as well as the deployer address would need to be tracked, and that would require a significant spec and implementation revisions.

This would be an relatively large effort for a single opcode. That makes me skeptical we will ever reach consensus to ship this as specified.

