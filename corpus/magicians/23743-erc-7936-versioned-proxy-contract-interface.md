---
source: magicians
topic_id: 23743
title: "ERC-7936: Versioned Proxy Contract Interface"
author: mokita-j
date: "2025-04-22"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7936-versioned-proxy-contract-interface/23743
views: 240
likes: 3
posts_count: 7
---

# ERC-7936: Versioned Proxy Contract Interface

Discussion Topic for [ERC: Versioned Proxy Contract Interface](https://eips.ethereum.org/EIPS/eip-7936)

## Simple Summary

This ERC standardizes a proxy interface that lets users call specific contract versions, enabling backward compatibility and opt-in upgrades.

## Abstract

This EIP standardizes an interface for proxy contracts that allows callers to explicitly select which version of an implementation contract they want to interact with. Unlike traditional proxy patterns that only expose the latest implementation, this standard enables backward compatibility by maintaining access to previous implementations while supporting upgrades. The versioned proxy maintains a registry of implementation addresses mapped to version identifiers, allowing callers to specify their desired version at call time.

## Motivation

Smart contract upgrades are essential for fixing bugs and adding features. Current proxy patterns typically force all callers to use the latest implementation, which can break existing integrations when interfaces change.

Furthermore, traditional proxy patterns expose all users to risk if an upgrade is malicious, as they have no choice but to use the latest implementation. This standard allows users to remain on verified versions they trust, mitigating the risk of a compromised admin key or governance process deploying harmful code.

This EIP addresses several key problems:

1. Breaking Changes: Interface changes in new implementations can break existing integrations.
2. Gradual Adoption: There is no standard way to allow gradual adoption of new contract versions.
3. Malicious Upgrades: Users today must trust proxy admins indefinitely, as they can’t opt out of potentially harmful upgrades without ceasing use of the contract entirely.
4. Trust Assumptions: Contract users must maintain perpetual trust in governance or admin keys, with no ability to selectively trust specific, audited implementations.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

### Interface

```solidity
interface IVersionedProxy {
    /// @notice Emitted when a new implementation version is registered
    /// @param version The version identifier
    /// @param implementation The address of the implementation contract
    event VersionRegistered(bytes32 version, address implementation);

    /// @notice Emitted when the default version is changed
    /// @param oldVersion The previous default version
    /// @param newVersion The new default version
    event DefaultVersionChanged(bytes32 oldVersion, bytes32 newVersion);

    /// @notice Registers a new implementation version
    /// @param version The version identifier (e.g., "1.0.0")
    /// @param implementation The address of the implementation contract
    function registerVersion(bytes32 version, address implementation) external;

    /// @notice Removes a version from the registry
    /// @param version The version identifier to remove
    function removeVersion(bytes32 version) external;

    /// @notice Sets the default version to use when no version is specified
    /// @param version The version identifier to set as default
    function setDefaultVersion(bytes32 version) external;

    /// @notice Gets the implementation address for a specific version
    /// @param version The version identifier
    /// @return The implementation address for the specified version
    function getImplementation(bytes32 version) external view returns (address);

    /// @notice Gets the current default version
    /// @return The current default version identifier
    function getDefaultVersion() external view returns (bytes32);

    /// @notice Gets all registered versions
    /// @return An array of all registered version identifiers
    function getVersions() external view returns (bytes32[] memory);

    /// @notice Executes a call to a specific implementation version
    /// @param version The version identifier of the implementation to call
    /// @param data The calldata to forward to the implementation
    /// @return The return data from the implementation call
    function executeAtVersion(bytes32 version, bytes calldata data) external payable returns (bytes memory);
}
```

### Behavior Requirements

1. The proxy contract MUST maintain a mapping of version identifiers to implementation addresses.
2. The proxy contract MUST maintain a default version that is used when no version is specified.
3. When executeAtVersion is called, the proxy MUST:

Verify the specified version exists
4. Forward the call to the corresponding implementation
5. Return any data returned by the implementation
6. The proxy contract MUST emit appropriate events when versions are registered, or when the default version changes.
7. The proxy contract SHOULD implement access control for administrative functions (registering versions, setting default).
8. The proxy contract MAY implement EIP-1967 storage slots for compatibility with existing tools.

### Fallback Function

The proxy contract SHOULD implement a fallback function that forwards calls to the default implementation version when no version is specified. This maintains compatibility with traditional proxy patterns.

## Rationale

### Version Identifiers as bytes32

Version identifiers are specified as `bytes32` rather than semantic versioning strings to:

1. Provide flexibility in versioning schemes
2. Reduce gas costs for storage and comparison
3. Allow for both string-based versions (converted to bytes32) and numeric versions
4. Allow for storing a Git commit identifier in SHA-1 or SHA-256

### Explicit Version Selection

The standard requires callers to explicitly select a version through `executeAtVersion` rather than encoding version information in the call data to:

1. Maintain a clean separation between version selection and function calls
2. Avoid modifying existing function signatures
3. Make version selection explicit and auditable

### Registry Pattern

The registry pattern was chosen over alternatives like:

1. Multiple Proxies: Having separate proxies for each version would increase deployment costs and complexity
2. Version in Storage: Storing a single “current version” would not allow different callers to use different versions simultaneously

### Default Version

The default version mechanism allows the proxy to maintain compatibility with traditional proxy patterns and supports callers that don’t need to specify a version.

## Backwards Compatibility

This EIP is designed to enhance backward compatibility for smart contracts. It does not introduce any backward incompatibilities with existing Ethereum standards or implementations.

Existing contracts that interact with proxy contracts can continue to do so without modification, as the fallback function will route calls to the default implementation.

## Security Considerations

This EIP is meant to significantly improve the security of the widely used proxy pattern.

## Replies

**MASDXI** (2025-06-17):

If `registerVersion` emits `VersionRegistered`, then `removeVersion` should emit something like ` VersionUnregistered`?

or change `VersionRegistered` and `VersionUnregistered` event style into `VersionUpdated` if version change to default address (zero address) mean `remove`

```auto
event VersionUpdated(bytes32 version, address indexed implementation);
```

So the indexer can index which version has been removed by filter implementation set to zero address, and the developer can avoid reusing old version identifiers.

---

**mokita-j** (2025-06-17):

Nice catch, emitting the `VersionUnregistered` event would be useful to track versions that are not safe to use anymore. Thanks for the suggestion.

---

**mudgen** (2025-10-15):

Hello,

I reviewed this EIP, and I think it provides useful functionality for proxy contracts.

I agree the EIP solves or mitigates these issues mentioned in the EIP:

> Breaking Changes: Interface changes in new implementations can break existing integrations.
> Gradual Adoption: There is no standard way to allow gradual adoption of new contract versions.
> Trust Assumptions: Contract users must maintain perpetual trust in governance or admin keys, with no ability to selectively trust specific, audited implementations.

I do not agree that this EIP prevents or mitigates the following problem which is mentioned in the EIP:

> Malicious Upgrades: Users today must trust proxy admins indefinitely, as they can’t opt out of potentially harmful upgrades without ceasing use of the contract entirely.

This is **Why**: An implementation contract has full access to the contract storage data of a proxy contract. A malicious implementation contract does not require any action by a user to do any damage that a proxy can do. So if a malicious implementation is added to a proxy, it doesn’t matter what version users of the proxy use. The attackers can add their own functions to an implementation that can access whatever the proxy can access, including stealing user funds or changing any of the contract storage data.

I reviewed the Specification and the other sections and they seem good to me.

---

**mokita-j** (2025-12-10):

Thanks for the review and the clarification! You’re absolutely right that an implementation contract executed via `delegatecall` has full write access to the **storage** of the proxy. That is the core security risk of any upgradeable architecture.

One important distinction, though, is that while the implementation can freely modify the proxy’s **storage**, it does **not** have access to the proxy’s **memory**. This allows the proxy to enforce certain invariants even when executing untrusted implementation code.

In particular, we can still prevent a malicious implementation from altering critical storage fields (such as past implementation addresses). The proxy can:

1. Snapshot the relevant storage values into memory before the delegatecall.
2. Execute the implementation logic via delegatecall.
3. Read the storage again after the call returns.
4. Revert the transaction if the values in storage do not match those stored in memory.

Because a revert undoes *all* effects of the delegatecall, including any attempted storage mutation, this mechanism prevents a malicious implementation from successfully rewriting the proxy’s implementation pointers (or any other protected fields we choose to validate).

This ERC defines **only the interface** for versioned proxy selection. We are currently building a reference implementation that includes these safeguards and are happy to share it as a **POC**.

---

**mudgen** (2025-12-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mokita-j/48/14866_2.png) mokita-j:

> You’re absolutely right that an implementation contract executed via delegatecall has full write access to the storage of the proxy. That is the core security risk of any upgradeable architecture.

Yes, that’s correct.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mokita-j/48/14866_2.png) mokita-j:

> One important distinction, though, is that while the implementation can freely modify the proxy’s storage, it does not have access to the proxy’s memory. This allows the proxy to enforce certain invariants even when executing untrusted implementation code.
>
>
> In particular, we can still prevent a malicious implementation from altering critical storage fields (such as past implementation addresses). The proxy can:
>
>
> Snapshot the relevant storage values into memory before the delegatecall.
> Execute the implementation logic via delegatecall.
> Read the storage again after the call returns.
> Revert the transaction if the values in storage do not match those stored in memory.
>
>
> Because a revert undoes all effects of the delegatecall, including any attempted storage mutation, this mechanism prevents a malicious implementation from successfully rewriting the proxy’s implementation pointers (or any other protected fields we choose to validate).

Yes, I see this approach can work. I like it.

If a proxy has 5 different implementation contracts,  will the proxy load 5 different implementation addresses from storage into memory?  Loading 5 storage slots costs 10,500 gas.  So will every `delegatecall` to any function then cost an additional 10,500 gas?

I am interested to see a proof of concept implemenation.

---

**mudgen** (2025-12-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mokita-j/48/14866_2.png) mokita-j:

> One important distinction, though, is that while the implementation can freely modify the proxy’s storage, it does not have access to the proxy’s memory. This allows the proxy to enforce certain invariants even when executing untrusted implementation code.
>
>
> In particular, we can still prevent a malicious implementation from altering critical storage fields (such as past implementation addresses). The proxy can:
>
>
> Snapshot the relevant storage values into memory before the delegatecall.
> Execute the implementation logic via delegatecall.
> Read the storage again after the call returns.
> Revert the transaction if the values in storage do not match those stored in memory.
>
>
> Because a revert undoes all effects of the delegatecall, including any attempted storage mutation, this mechanism prevents a malicious implementation from successfully rewriting the proxy’s implementation pointers (or any other protected fields we choose to validate).

How does this security technique prevent malicious alteration of implementation specific critical storage?

For example let’s say that an implementation implements an ERC20 token and many people use it and there are now 1000 user balances.  How can all 1000 storage locations be protected?  Or what stops an attacker from adding his own malicious implementation to the proxy that adds 100 million tokens to his/her balance which he then sells?

