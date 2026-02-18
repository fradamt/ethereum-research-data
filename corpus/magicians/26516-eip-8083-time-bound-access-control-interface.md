---
source: magicians
topic_id: 26516
title: "EIP-8083: Time-Bound Access Control Interface"
author: dif
date: "2025-11-11"
category: ERCs
tags: [erc, authorization, access-control]
url: https://ethereum-magicians.org/t/eip-8083-time-bound-access-control-interface/26516
views: 140
likes: 7
posts_count: 7
---

# EIP-8083: Time-Bound Access Control Interface

This EIP standardizes secure time-bound roles with automatic expiration, eliminating manual revocation risks.

## Abstract

This EIP introduces a minimal interface for enforcing time-bound role permissions management in contracts.

Specifically, it provides interfaces for granting time-bound roles and verifying active permissions, enabling automatic deactivation of expired roles without requiring manual intervention.

## Motivation

The permission system of smart contracts is crucial for the operation and management. Role-based access control (RBAC) systems are widely adopted in smart contracts to manage permissions effectively.

However, the absence of a standardized mechanism for automatically revoking roles after predefined durations introduces significant security challenges, particularly in dynamic environments such as complex organizational structures and multi-party business scenarios. Permanent role assignments exacerbate these risks in common use cases, including:

1. Temporary access needs, such as third-party supplier or vendors integrations.
2. Project- or task-specific permissions that should not persist beyond their scope.
3. Employee offboarding or role changes.

In these cases, permanent roles create unnecessary attack surfaces. To address these systematic issues, this EIP introduced verifiable time constraints directly into permission management.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

Every contract compliant with this EIP **MUST** implement the EIP-XXXX interface. Contracts **SHOULD** also implement EIP-165 to support interface detection.

```solidity
pragma solidity ^0.8.13;

interface ERC165 {
    /// @notice Query if a contract implements an interface
    /// @param interfaceID The interface identifier, as specified in ERC-165
    /// @dev Interface identification is specified in ERC-165. This function
    ///  uses less than 30,000 gas.
    /// @return `true` if the contract implements `interfaceID` and
    ///  `interfaceID` is not 0xffffffff, `false` otherwise
    function supportsInterface(bytes4 interfaceID) external view returns (bool);
}

/// @title Time-Bound Access Control Interface
interface EIPXXXX /* is ERC165 */ {
    /// @dev Emitted when role expiration is changed
    event RoleExpirationChanged(
        bytes32 indexed role,
        address indexed account,
        uint256 previousExpiryTimestamp,
        uint256 expiryTimestamp
    );

    /// @dev set role expiration at specified timestamp
    function setRoleExpiration(
        bytes32 role,
        address account,
        uint256 expiryTimestamp
    ) external;

    /// @dev Query the expiry timestamp of the role
    function getRoleExpiration(bytes32 role, address account) external view returns (uint256);
    /// @dev Checks if role is active at current timestamp
    function hasActiveRole(bytes32 role, address account) external view returns (bool);
}
```

1. The setRoleExpiration(bytes role, address account, uint256 expiryTimestamp) MUST have reasonable access control.
2. The expiryTimestamp parameter MUST be represented as seconds, the role expiration time, using Unix timestamp format.
3. All operations involving changes in the role expiration MUST emit RoleExpiryChanged events.

## Rationale

- Timestamp-Only: A single timestamp parameter simplifies implementation while supporting calendar-based expiration that aligns with real-world use cases.
- Minimal surface: The design enforces a clear security boundary with the function hasActiveRole, avoids auxiliary functions to reduce the attack surface, and provides a fully self-contained specification.

## Backwards Compatibility

No backward compatibility issues are introduced. This proposal is fully backward-compatible with existing access control systems and supports EIP-165 interface detection.

## Reference Implementation

```solidity
pragma solidity 0.8.13;

import { EIPXXXX } from "./EIPXXXX.sol";

/**
 * @title EIPXXXX Implementation
 * @dev Implementation of the EIPXXXX Time-Bound Access Control Interface
 */
contract EIPXXXXImpl is EIPXXXX {

    mapping(bytes32 => bytes32) private _roleAdmin;
    mapping(bytes32 => mapping(address => uint256)) private _roleExpiryTimestamps;

    error NotActiveRole(bytes32 role, address account);
    event RoleAdminChanged(bytes32 indexed role, bytes32 indexed prevRole, bytes32 adminRole);

    /**
     * @dev Sets the admin role for a given role
     * @param role The role to set admin for
     * @param adminRole The admin role to set
     */
    function _setRoleAdmin(bytes32 role, bytes32 adminRole) internal virtual {
        bytes32 previousAdminRole = getRoleAdmin(role);
        _roleAdmin[role] = adminRole;
        emit RoleAdminChanged(role, previousAdminRole, adminRole);
    }

    /**
     * @dev Returns the admin role for a given role
     * @param role The role to query
     * @return The admin role
     */
    function getRoleAdmin(bytes32 role) public view returns(bytes32) {
        return _roleAdmin[role];
    }

    /**
     * @dev Modifier to check if an account has an active role
     * @param role The role to check
     * @param account The account to check
     */
    modifier onlyActiveRole(bytes32 role, address account) {
        if (!hasActiveRole(role, account)) {
            revert NotActiveRole(role, account);
        }
        _;
    }

    /**
     * @dev Sets the expiration timestamp for a role-account pair
     * @param role The role to set expiration for
     * @param account The account to set expiration for
     * @param expiryTimestamp The expiration timestamp
     */
    function setRoleExpiration(
        bytes32 role,
        address account,
        uint256 expiryTimestamp
    ) external onlyActiveRole(getRoleAdmin(role), msg.sender) {
        uint256 lastExpiryTimestamp = _roleExpiryTimestamps[role][account];

        _roleExpiryTimestamps[role][account] = expiryTimestamp;

        emit RoleExpirationChanged(role, account, lastExpiryTimestamp, expiryTimestamp);
    }

    /**
     * @dev Returns the expiration timestamp for a role-account pair
     * @param role The role to query
     * @param account The account to query
     * @return The expiration timestamp
     */
    function getRoleExpiration(bytes32 role, address account) external view returns(uint256) {
        return _roleExpiryTimestamps[role][account];
    }

    /**
     * @dev Checks if an account has an active role (not expired)
     * @param role The role to check
     * @param account The account to check
     * @return Whether the role is active
     */
    function hasActiveRole(bytes32 role, address account) public view returns (bool) {
        return block.timestamp CC0.

## Replies

**Ankita.eth** (2025-11-11):

This is a solid and very practical draft. Standardizing time-bound roles fills a clear gap in RBAC by enabling **automatic, verifiable expiry without relying on manual revocation.** The interface is lean, modular, and EIP-165 compatible, which makes it easy to compose with existing systems. High signal-to-noise ratio — exactly what good standards look like.

I particularly appreciate the minimal design of `setRoleExpiration`, `getRoleExpiration`, and `hasActiveRole` — it keeps the implementation straightforward while aligning with real-world temporal requirements. Integrating automatic expiry into role management helps prevent stale or permanent permissions from becoming attack vectors, which is especially important for DAOs, DeFi protocols, and multi-party systems.

A few targeted observations and suggestions for tightening the spec before EIP-IP submission:

### 1. Role Assignment vs. Expiration Scope

> setRoleExpiration assumes a role is already granted elsewhere (e.g., via AccessControl._grantRole). But getRoleExpiration returns a timestamp even if the role was never granted.

**Question**: Should the spec **require** that getRoleExpiration returns 0 *only* when the role has never been assigned? Currently, 0 is overloaded (never granted vs. explicitly set to epoch). This breaks UI/indexer logic.

**Recommendation**:

```auto
// Semantic clarity
0                  → role never granted
type(uint256).max  → permanent
else               → Unix expiry
```

---

### 2. Access Control on setRoleExpiration

> “MUST have reasonable access control” → too vague for a standard.

Your ref impl uses:

```auto
onlyActiveRole(getRoleAdmin(role), msg.sender)
```

**Question**: Should the spec **mandate** that only the *active admin* of a role can modify its expiry? This prevents privilege escalation and aligns with OpenZeppelin patterns.

---

### 3. Infinite Expiry Constant

No INFINITE constant defined.

**Recommendation**: Add to interface:

```auto
uint256 public constant INFINITE_EXPIRY = type(uint256).max;
```

Then update hasActiveRole:

```auto
function hasActiveRole(...) view returns (bool) {
    uint256 exp = _roleExpiryTimestamps[role][account];
    return exp != 0 && (exp == INFINITE_EXPIRY || block.timestamp < exp);
}
```

---

### 4. supportsInterface Bug in Ref Impl

solidity

```auto
interfaceID == this.supportsInterface.selector  // recursive, wrong
```

**Fix**:

```auto
return interfaceID == type(ERC165).interfaceId ||
       interfaceID == type(EIPXXXX).interfaceId;
```

---

### 5. MEV Mitigation (Optional but Critical)

You flag front-running — excellent.

**Question**: Should high-security deployments support a deadline param?

```auto
function setRoleExpiration(..., uint256 deadline) external;
```

Enables timelocks and commit-reveal. **Optional**, but spec should *allow* it.

**Additional Considerations:**

- Timestamp Variability: Miners can slightly manipulate block timestamps. Safety margins or buffer periods for short-lived roles are recommended.
- Admin Hierarchy Clarity: Guidance on chaining or limiting admin privileges could prevent accidental or malicious misuse.

Overall, this proposal is backward-compatible, gas-efficient, and addresses a top security concern in role-based systems. From a Web3 perspective, it provides a robust foundation for secure, auditable, and temporary role management, making it particularly relevant for DeFi protocols, DAOs, and other time-sensitive on-chain systems.

---

**RILTONKC** (2025-11-11):

Inclusivity adopts reliability

---

**Fra** (2025-11-11):

Nice EIP! I have a question about the first user calls `setRoleExpiration`. Since `_setRoleAdmin` only sets `_roleAdmin`, not the `_roleExpiryTimestamps`. Will the user with the admin role fail the `onlyActiveRole` check?

---

**dif** (2025-11-12):

Hi, Ankita. Thank you! Truly appreciate your kind words. Your suggestions are practical and valuable.

1. Role Assignment vs. Expiration Scope

In our current design, we treat an expiration time of `0` or `invalid value` as indicating an inactive role. You’re right – using `0` as default value is semantically inconsistent with the Unix timestamp definition, and may break UI/indexer logic. We agree this needs clarification. I’ll add a patch to the proposal to explicitly note this behavior and remind readers of the implication.

1. Access Control on setRoleExpiration

Your observation is correct. We recognize that different implementation approaches may be appropriate depending on specific business contexts. The reference implementation we provide is just one possible approach; alternatives — such as managing roles via a single “TimeAllocationRole” — are equally valid. For this reason, the specification intentionally avoids prescribing implementation details, and only requires that “some access control” mechanism must be in place for this function.

1. Infinite Expiry Constant

Great suggestion. We’ll introduce a named constant (e.g., `INFINITE_EXPIRY`) in the ref impl and recommend its use.

1. supportsInterface Bug in Reference Implementation

Our implementation follows the syntax in the [EIP-165](https://eips.ethereum.org/EIPS/eip-165) reference example. For compatibility reasons, we’ll retain this structure as-is. Could you share more details about the recursive issue you mentioned?

1. MEV Mitigation (Optional but Critical)

The `deadline` design you suggested is indeed excellent, and we will mention it in the relevant discussion. However, the likelihood of MEV-related issues arising in this specific context is extremely low. As OpenZeppelin’s `AccessControl` contract also omits provide such a feature. So, we’ve chosen not to include it in the interface.

Thanks again for your thoughtful feedback — it’s helping us improve the spec!

---

**dif** (2025-11-12):

Nice finding! Our ref impl didn’t consider this detail. Do you think it’s good to add an internal function `_setRoleExpiration` to handle such scenarios during contraction initialization?

---

**Ankita.eth** (2025-11-12):

Thanks for the thoughtful clarifications — I really appreciate the openness to discussion.

On **`getRoleExpiration` semantics**: great call adding that clarification. You might consider explicitly stating this in the spec, e.g.

*“A return value of `0` MUST indicate that the role has never been assigned; expired roles retain their timestamp for auditability.”*

That distinction helps indexers and off-chain analytics tools a lot.

Regarding **`supportsInterface`**, here’s what I meant — the current reference returns `interfaceID == this.supportsInterface.selector`, which causes a recursive call. The correct pattern is:

```auto
return interfaceID == type(IERC165).interfaceId ||
       interfaceID == type(ITimeBoundAccess).interfaceId;
```

I can submit a short PR if helpful.

Re **MEV mitigation**: agreed that the risk is low for most cases, but allowing a `deadline` param in the interface doesn’t impose implementation cost — it just gives downstream protocols optional protection (esp. for governance or off-chain signed role updates). Worth considering as an *optional extension*.

Finally, [@Fra](/u/fra) makes a good point — `_setRoleExpiration` as an internal helper for initialization would make the pattern cleaner, especially when roles are pre-assigned in constructors.

Overall, love how this spec is shaping up. Time-bound RBAC is something real protocols will actually use — not just theoretical.

