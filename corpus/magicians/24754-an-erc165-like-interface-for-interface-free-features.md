---
source: magicians
topic_id: 24754
title: An ERC165-like Interface for Interface-free Features
author: adraffy
date: "2025-07-07"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/an-erc165-like-interface-for-interface-free-features/24754
views: 89
likes: 1
posts_count: 1
---

# An ERC165-like Interface for Interface-free Features

[EIP-1](https://eips.ethereum.org/EIPS/eip-1#eip-work-flow) recommends floating an idea before writing an EIP so I would like to propose [IFeatureSupporter](https://github.com/ensdomains/ens-contracts/blob/staging/contracts/utils/IFeatureSupporter.sol) which is a cousin of [ERC-165](https://eips.ethereum.org/EIPS/eip-165) for exhibiting “features” which have no visible interface to identify.

```Solidity
/// @notice Interface for expressing contract features not visible from the ABI.
/// @dev Interface selector: `0x582de3e7`
interface IFeatureSupporter {
    /// @notice Check if a feature is supported.
    /// @param feature The feature.
    /// @return True if the feature is supported by the contract.
    function supportsFeature(bytes4 feature) external view returns (bool);
}
```

Features are `bytes4`, ideally derived from the following scheme: take leading four bytes of a hashed reverse domain:

```Solidity
library ResolverFeatures {
    /// @notice Implements `resolve(multicall([...]))`.
    /// @dev Feature: `0x96b62db8`
    bytes4 constant RESOLVE_MULTICALL =
        bytes4(keccak256("eth.ens.resolver.extended.multicall"));
}
```

IMO, contracts that implement `IFeatureSupporter` must implement `ERC165` and must return true for `supportsInterface(type(IFeatureSupporter).interfaceId)`.

I believe a separate interface is better than polluting the ERC165 space with synthetic feature-like interfaces.

---

For ENS, we’ve found (2) uses for features based on the core description above:

First, features help support backwards compatibility while maintaining efficiency for newer contracts.  Post-feature contracts can implement standard interfaces but express features which enable aware callers to optimize their calls.  For example, ENS operates an [UniversalResolver](https://github.com/ensdomains/ens-contracts/blob/staging/contracts/universalResolver/AbstractUniversalResolver.sol) (UR) which is a contract that performs the core parts of standard ENS resolution (that originally was handled by client libraries.)  One feature of the UR is that it enables multicall on resolver contracts that use an offchain gateway, but the implementation incurs one [ERC-3668](https://eips.ethereum.org/EIPS/eip-3668) request per call.  With features, before the UR calls a resolver contract, [it can probe it](https://github.com/ensdomains/ens-contracts/blob/staging/contracts/universalResolver/AbstractUniversalResolver.sol#L279-L304) for the new ENS feature `eth.ens.resolver.extended.multicall` which indicates that instead of externally performing the multicall as parallel single requests, the multicall can be passed to the resolver as a combo request.

Second, features can express functional properties of a contract.  For example, ENS has a resolver contract which returns the same record data regardless of the name queried, eg. `R.addr("vitalik.eth") = R.addr("made.up.name")`.  This enables the same onchain datastore to provide data for multiple names.  This type of resolver supports the `"eth.ens.resolver.singular"` feature which indicates [R.resolve(name, call)](https://github.com/ensdomains/namechain/blob/main/contracts/src/common/DedicatedResolver.sol#L268-L285) is independent of `name`.  Although this feature can’t be trusted, since the implementation could do something else, this information is useful for indexers and clients.
