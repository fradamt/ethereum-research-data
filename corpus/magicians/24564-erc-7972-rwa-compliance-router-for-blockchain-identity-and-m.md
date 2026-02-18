---
source: magicians
topic_id: 24564
title: "ERC-7972: RWA Compliance Router for Blockchain Identity and Modular Real-World Asset Compliance"
author: deepanshu179
date: "2025-06-16"
category: ERCs
tags: [erc7972]
url: https://ethereum-magicians.org/t/erc-7972-rwa-compliance-router-for-blockchain-identity-and-modular-real-world-asset-compliance/24564
views: 224
likes: 2
posts_count: 3
---

# ERC-7972: RWA Compliance Router for Blockchain Identity and Modular Real-World Asset Compliance

Discussion topic for ERC-7972, RWA’s: RWA compliance router for RWA’s(security tokens) ·  [Add ERC: Universal Compliance Router for RWA's by deepanshu179 · Pull Request #1087 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1087)

**Summary:**

The RWA Compliance Router (ERC-7972) is a smart contract middleware that enables modular compliance for tokenized Real-World Assets (RWAs). It integrates seamlessly with:

- DIDs (Decentralized Identifiers) for universal identity resolution
- OnchainID for verified, on-chain identity and compliance metadata
- Soulbound Tokens (SBTs) to represent non-transferable credentials like KYC, accreditation, or residency
- On-chain compliance modules (e.g., KYC/AML, investor limits, blacklists)

**Motivation:**

On-chain compliance for tokenized real-world assets (RWAs) such as money market funds, real estate, private equity, and fixed-income securities etc. is becoming essential as adoption increases. Regulatory frameworks (KYC, AML, accredited investor rules, jurisdiction-specific rules) are often complex, evolving, and differ across asset classes and countries.

Currently, developers hardcode compliance logic into token contracts or wrap tokens with enforcement proxies. These approaches are:

- Inflexible: They require contract redeployments to update rules.
- Siloed: Each protocol creates and audits its own compliance logic.
- Non-composable: Tokens, marketplaces, and identity services cannot easily interoperate.

This results in duplicated effort, increased audit surface, and fragmentation across ecosystems.

We need a **shared, modular, and extensible compliance layer** that:

- Allows for dynamic updates to compliance rules
- Enables jurisdiction-specific enforcement logic
- Promotes reuse and composability across protocols
- Encourages collaboration between identity providers, compliance services, and token issuers

The `RWAComplianceRouter` addresses these needs by serving as a pluggable registry and execution layer for compliance modules that can be applied across different asset types, jurisdictions, and lifecycle events.

**Rationale:**

The `RWAComplianceRouter` is designed with the following decisions:

- Modular Contract Registration: Compliance contracts are registered with their corresponding function selectors (bytes4) to allow for diverse validation logic without assuming fixed interfaces. This allows backwards-compatible upgrades and supports heterogeneous compliance frameworks.
- Staticcall: Compliance checks are invoked via staticcall, ensuring they are read-only and cannot modify state. This makes the router safe to integrate with other on-chain systems and supports off-chain simulation for auditability.
- Dual Registry Design: The router maintains separate lists for:

General compliance contracts: which apply globally,
- Jurisdiction-aware contracts: which are checked conditionally based on the user’s jurisdiction (passed as a bytes32 identifier).
Note: The router interface can extended to perform additional checks not limited to just above checks.

This split improves clarity and allows different enforcement strategies to coexist.

**Iterative Check Model**: The router returns `true` on the *first passing check*. This conservative model optimizes for gas efficiency while enabling compliance layering.

**Owner-controlled Registration**: To avoid misuse, only the deployer (or designated admin) can register or remove compliance modules. This can later be extended to role-based or DAO-based control models.

This architecture provides a **low-coupling**, **high-composability** mechanism for evolving compliance logic that can serve as shared infrastructure for the RWA ecosystem.

#### Update Log

- 2025-06-16: review
- 2025-06-16: ERC-7972 under review

#### External Reviews

2 as of 2025-07-21

#### Outstanding Issues

None as of 2025-06-16.

## Replies

**deepanshu179** (2025-06-16):

[![Universal compliance proxy (1)](https://ethereum-magicians.org/uploads/default/optimized/2X/d/dc1f6a93fbcd1fc5f8ba30618c32ae7e6ca5100f_2_587x500.png)Universal compliance proxy (1)749×637 69.2 KB](https://ethereum-magicians.org/uploads/default/dc1f6a93fbcd1fc5f8ba30618c32ae7e6ca5100f)

---

**deepanshu179** (2025-06-23):

Interface

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
/// @title IUniversalComplianceRouter
/// @notice Interface for a modular compliance router supporting general and jurisdiction-aware compliance contracts
interface IUniversalComplianceRouter {
    /// @notice Registers a general compliance contract
    /// @param contractAddress The address of the compliance contract
    /// @param selector The function selector (e.g., isCompliant(address))
    function registerGeneralComplianceContract(address contractAddress, bytes4 selector) external;
    /// @notice Removes a compliance contract from the registry
    /// @param contractAddress The address of the contract to remove
    function removeComplianceContract(address contractAddress) external;
    /// @notice Checks if a user is compliant with any general compliance contract
    /// @param user The address of the user to check
    /// @return True if compliant with any general contract, false otherwise
    function isCompliant(address user) external view returns (bool);
    /// @notice Checks if a user is compliant with any jurisdiction-aware compliance contract
    /// @param user The address of the user
    /// @param jurisdiction The jurisdiction identifier (e.g., country code)
    /// @return True if compliant with any jurisdiction-aware contract, false otherwise
    function isCompliant(address user, bytes32 jurisdiction) external view returns (bool);
}
```

```auto

```

