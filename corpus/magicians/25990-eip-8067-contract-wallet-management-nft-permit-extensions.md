---
source: magicians
topic_id: 25990
title: "EIP-8067: Contract wallet management NFT Permit Extensions"
author: wenzhenxiang
date: "2025-10-27"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/eip-8067-contract-wallet-management-nft-permit-extensions/25990
views: 34
likes: 0
posts_count: 1
---

# EIP-8067: Contract wallet management NFT Permit Extensions

## Abstract

This proposal extends [ERC-7564](https://eips.ethereum.org/ERCS/erc-7564) NFT manager modules with EIP-712 permit flows. It standardises message schemas, signature verification, and nonce handling so that smart wallets can delegate transfers and approvals of ERC-721 and ERC-1155 assets without sending on-chain transactions themselves.

## Motivation

ERC-7564 equips smart wallets with an on-chain permissions framework for NFTs, but every interaction still requires the wallet contract to submit its own transaction. Users must maintain gas balances, and dApps that want claimable drops or delegated marketplace access resort to bespoke signature formats that do not interoperate.

Introducing a standard permit flow allows the wallet owner to sign once off-chain while a dApp or relayer later submits the operation on-chain and pays gas for the user. This enables:

- gasless NFT interactions (listings, transfers, staking) without requiring the owner to hold native gas tokens;
- claimable “red packet” or reward drops where a signed nftTransferWithSig lets friends or community members redeem later;
- universal coverage for any ERC-721 or ERC-1155 asset managed by the wallet’s NFT module;
- interoperable tooling because wallets, marketplaces, and relayers share one EIP-712 schema and nonce model.

Taken together, the ERC-7564 permit extension allows NFT dApps to provide gasless, permissioned operations through a unified standard instead of fragmented, project-specific signatures.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

### Interfaces

Implementations MUST expose the following interface in addition to the baseline ERC-7564 API:

```solidity
interface IERC7564Permit {
    function nftTransferNonce(address owner, address asset, address caller) external view returns (uint256);

    function nftTransferWithSig(
        address owner,
        address asset,
        address to,
        uint256 tokenId,
        uint256 deadline,
        bytes calldata signature
    ) external returns (bool success);

    function nftApproveNonce(address owner, address asset, uint256 tokenId, address caller) external view returns (uint256);

    function nftApproveWithSig(
        address owner,
        address asset,
        address operator,
        uint256 tokenId,
        uint256 deadline,
        bytes calldata signature
    ) external returns (bool success);

    function nftApprovalForOneAllNonce(address owner, address asset, address caller) external view returns (uint256);

    function nftSetApprovalForOneAllWithSig(
        address owner,
        address operator,
        bool approved,
        uint256 deadline,
        bytes calldata signature
    ) external returns (bool success);

    function nftApprovalForAllAllNonce(address owner, address caller) external view returns (uint256);

    function nftSetApprovalForAllAllWithSig(
        address owner,
        address operator,
        bool approved,
        uint256 deadline,
        bytes calldata signature
    ) external returns (bool success);
}
```

All functions MUST mirror the behaviour of their on-chain ERC-7564 counterparts once the signature is accepted.

Implementations MUST support wallets that verify signatures through [ERC-1271](https://eips.ethereum.org/EIPS/eip-1271). If a wallet wraps signatures (for example to indicate owner index), the module MUST unwrap prior to verification.

### EIP-712 Domain

Every permit MUST use the following domain values:

- name = "NFTManager Permit"
- version = "1"
- chainId equal to the executing chain
- verifyingContract = address(this) (the smart wallet that owns the module)

If the wallet supports multiple chains, it MUST ensure that the observed `chainId` matches the signed value before executing a permit.

### Typed-Data Payloads

Each function MUST hash one of the following primary types before invoking the wallet’s signature validation logic. The `wallet` field identifies the smart wallet executing the module. In all payloads `nonce` is the value returned by the corresponding nonce view function.

| Function | Primary Type | Fields |
| --- | --- | --- |
| nftTransferWithSig | NFTTransferWithSig | wallet, owner, caller, asset, to, tokenId, nonce, deadline |
| nftApproveWithSig | NFTApproveWithSig | wallet, owner, caller, asset, operator, tokenId, nonce, deadline |
| nftSetApprovalForOneAllWithSig | NFTApprovalForOneAllWithSig | wallet, owner, caller, asset, operator, approved, nonce, deadline |
| nftSetApprovalForAllAllWithSig | NFTApprovalForAllAllWithSig | wallet, owner, caller, operator, approved, nonce, deadline |

The module MUST compare the signed `caller` with `msg.sender` and revert on mismatch.

### Nonce Strategy

- nftTransferNonce MUST derive a unique nonce per (owner, asset, caller) tuple.
- nftApproveNonce MUST derive a unique nonce per (owner, asset, tokenId, caller) tuple.
- nftApprovalForOneAllNonce MUST derive a unique nonce per (owner, asset, caller) tuple.
- nftApprovalForAllAllNonce MUST derive a unique nonce per (owner, caller) tuple.

A `WithSig` function MUST increment the relevant nonce immediately before state changes. Re-using a signature MUST revert.

### Execution Requirements

Implementations MUST follow these rules when processing a permit:

1. Treat deadline equal to 0 as non-expiring; otherwise enforce block.timestamp <= deadline.
2. Invoke nftTransfer, nftApprove, nftSetApprovalForOneAll, or nftSetApprovalForAllAll with the provided arguments once the signature is verified and the nonce is incremented.
3. Ensure allowances tracked inside the wallet are updated exactly as they would be for direct calls.
4. Emit the same events as the underlying ERC-7564 function.
5. Revert if validation fails at any stage (invalid signature, expired deadline, incorrect caller, or mismatched asset parameters).

Wallets MAY expose additional permit helpers, but they MUST NOT change the semantics defined above.

## Rationale

ERC-7564 already defines transfer and approval functions for NFT managers inside smart wallets. The permit extension mirrors those entry points so that wallets can capture the same behaviour with off-chain signatures:

- The domain name is shared across implementations to allow community tooling while remaining specific to NFT managers.
- The caller field binds a signature to the relayer authorised to execute it, reducing the chance of front-running and replay by unrelated addresses.
- Scoping nonces by caller, asset, and (where needed) tokenId prevents cross-operation replay while allowing users to delegate distinct relayers for different collections.
- Executing the existing ERC-7564 methods after signature verification keeps event streams and downstream integrations unchanged.

## Backwards Compatibility

Existing ERC-7564 modules remain valid. Clients SHOULD detect permit support via ERC-165 or by probing for the new function selectors. Wallets that do not implement this extension can ignore the added functions without changing behaviour.

## Reference Implementation

A reference implementation will be published after the draft is reviewed. It follows the pattern of validating the signature against the typed-data hash, incrementing the scoped nonce before any external calls, and then invoking the underlying ERC-7564 function so that events and storage updates stay consistent.

## Reference Test Cases

A public test suite will accompany the reference implementation. Implementers are encouraged to cover:

- successful transfers, approvals, and operator grants submitted by authorised relayers,
- rejection of expired permits, incorrect callers, or mismatched assets,
- nonce incrementing when downstream token logic reverts,
- replay protection across all nonce domains.

## Security Considerations

- Implementations MUST increment the nonce before calling external token contracts so that reverts cannot reopen a signature.
- Wallets SHOULD bound permit validity windows and monitor outstanding approved = true operator signatures to limit abuse.
- Relayers MUST ensure that the transaction sender matches the signed caller; otherwise execution will revert and gas will be wasted.

## Copyright

Copyright and related rights waived via [CC0-1.0](https://creativecommons.org/publicdomain/zero/1.0/).
