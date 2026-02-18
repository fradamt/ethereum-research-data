---
source: magicians
topic_id: 27627
title: "ERC Proposal: Vault Whitelister Interface for Permissioned ERC-20 Vaults"
author: MiguelSchneider
date: "2026-01-30"
category: ERCs
tags: [erc, token, evm]
url: https://ethereum-magicians.org/t/erc-proposal-vault-whitelister-interface-for-permissioned-erc-20-vaults/27627
views: 65
likes: 6
posts_count: 3
---

# ERC Proposal: Vault Whitelister Interface for Permissioned ERC-20 Vaults

## Summary

This proposal introduces a **standard companion contract interface** (“Vault Whitelister”) for **permissioned ERC-20 ecosystems**.

The interface enables third-party protocols to **atomically authorize investor-bound vault contracts** during protocol flows such as deposits, while preserving investor-level ownership attribution required by many regulated or permissioned tokens.

The ERC is **additive to ERC-20**, does not modify the ERC-20 interface, and intentionally leaves identity and compliance logic implementation-defined.

## Problem Statement

Many permissioned ERC-20 tokens (e.g. regulated RWAs) must maintain **investor-level ownership attribution** for regulatory compliance, lifecycle events, and corporate actions.

However, common DeFi patterns—such as pooled contracts—aggregate balances across investors and obscure beneficial ownership.

A widely adopted alternative is **investor-bound vaults**:

- protocols deploy a dedicated vault contract per investor
- the vault holds and manages the permissioned token on the investor’s behalf
- ownership attribution remains tied to the investor

Today, authorizing such vaults requires **bespoke, issuer-specific flows**, forcing protocols to implement custom integrations for each permissioned token ecosystem.

## Proposed Solution

This ERC defines a **standardized companion contract interface** (“Vault Whitelister”) that permissioned ERC-20 ecosystems MAY expose.

High-level flow:

1. A protocol deploys a vault contract for an investor
2. During the same transaction, the protocol calls the Vault Whitelister
3. The whitelister verifies eligibility according to issuer-defined rules
4. If successful, the vault is authorized under the investor’s permissions

The interface standardizes **only the integration surface** between protocols and permissioned-token ecosystems.

**Note:** While this proposal involves vault contracts, it is orthogonal to ERC-4626 / ERC-7575. This ERC does not define vault accounting or asset semantics, and focuses exclusively on standardizing authorization of investor-bound vault addresses in permissioned ERC-20 ecosystems.

## Design Goals

- Enable atomic vault deployment + authorization
- Preserve investor-level beneficial ownership attribution
- Minimize integration friction for protocols
- Support multiple permissioning models without standardizing identity
- Avoid modifications to ERC-20 or existing permissioned token standards

## Non-Goals

This proposal explicitly does **not** attempt to:

- Standardize identity models, KYC, or accreditation logic
- Define how investor identities are represented or stored
- Replace or subsume ERC-3643, ERC-1400, or other permissioned token standards
- Mandate specific compliance checks or policies

All compliance semantics remain **implementation-defined**.

## Interface Overview (Simplified)

```auto
interface IERC_VaultWhitelister {
    event VaultWhitelisted(
        address indexed investor,
        address indexed vault,
        address indexed token,
        string investorId
    );

    function whitelist(
        address vaultAddress,
        address investorWalletAddress
    ) external;

    function token() external view returns (address);
}
```

The whitelist function is intended to be called by authorized protocol contracts as part of an atomic transaction. Implementations MUST revert if authorization cannot be completed.

## Why a Standalone Companion Interface

This ERC is intentionally designed as a **standalone contract interface**, rather than an ERC-20 extension:

- Many permissioned tokens cannot be upgraded to add new methods
- Compliance logic is often externalized for regulatory or operational reasons
- Protocols prefer a predictable “call this contract during the flow” pattern
- The design avoids imposing identity semantics on token contracts

The whitelister acts as an **adapter** between protocols and permissioned ERC-20 ecosystems.

## Compatibility

- Fully compatible with ERC-20
- Compatible with permissioned token standards such as ERC-3643, ERC-1400, and custom issuer implementations
- Tokens may adopt this pattern without changing their ERC-20 interface

## Security Considerations (High Level)

- Implementations should restrict which callers may invoke whitelist
- Vault authorization should be treated as equivalent to investor authorization
- Implementations should be safe to call within complex protocol flows
- Reentrancy and denial-of-service considerations apply

## Status and Next Steps

This proposal is shared for **early community feedback**, particularly on:

- Scope and abstraction level
- Single-token vs multi-token whitelister designs
- Naming conventions
- General usefulness across permissioned ERC-20 ecosystems

If there is alignment, the next step will be to submit this as a Draft ERC to the ethereum/ERCs repository.

## Discussion

Feedback and discussion are welcome in this thread.

## Replies

**dacian** (2026-02-03):

There are some who would object to the terms “whitelist” and “blacklist” instead preferring “allowlist” and “denylist”; it may be easier to get a standard approved using these more “neutral” terms.

Should the standard interface also contain a function to check current authorization status:

```auto
    event VaultAllowed(
        address indexed investor,
        address indexed vault,
        address indexed token,
        string investorId
    );

    function allow(
        address vaultAddress,
        address investorWalletAddress
    ) external;

    function isAllowed(
        address vaultAddress,
        address investorWalletAddress
    ) external view returns (bool);
```

Also should it contain a function to revoke permission with a corresponding event?

```auto
    event VaultDenied(
        address indexed investor,
        address indexed vault,
        address indexed token,
        string investorId
    );

    function deny(
        address vaultAddress,
        address investorWalletAddress
    ) external;
```

---

**sullof** (2026-02-04):

My recently finalized proposal, [ERC7656](https://eips.ethereum.org/EIPS/eip-7656), enables the creator of an ERC-20 token to deploy an owned service linked directly to that token. Its core purpose is to allow tokens, NFTs, or wallets to be extended seamlessly with new functionalities, without requiring modifications to the original contract. Your proposal strikes me as an excellent and clear use case for this standard.

More info at https://erc7656.github.io/

