---
source: magicians
topic_id: 27312
title: "ERC-8114: NFT Transfer With Signature"
author: wenzhenxiang
date: "2025-12-25"
category: ERCs
tags: [erc, nft, wallet, erc-721]
url: https://ethereum-magicians.org/t/erc-8114-nft-transfer-with-signature/27312
views: 74
likes: 3
posts_count: 2
---

# ERC-8114: NFT Transfer With Signature

This proposal extends [ERC-7564](https://github.com/mossdapp/ERCs/blob/feat/nfttransfer-sig/eip-7564.md) compliant smart contract wallets with an off-chain signature flow for NFT transfers, allowing wallet owners to delegate transfers via typed-data signatures presented by any relayer. The extension defines a canonical [EIP-712](https://github.com/mossdapp/ERCs/blob/feat/nfttransfer-sig/eip-712.md) schema, nonce accounting, and execution requirements for compliant implementations. Unlike nft-native standards, this extension operates at the wallet level, enabling gasless transfers for any [ERC-721](https://github.com/mossdapp/ERCs/blob/feat/nfttransfer-sig/eip-721.md) nft without requiring nft contract modifications.

## Motivation

ERC-7564 enables programmable asset management directly in smart contract wallets but requires on-chain transactions for every NFT transfer. This creates friction for gasless use cases such as gifting, claimable drops, custodial listings, and relayer-sponsored transfers.

By implementing authorization at the ERC-7564 compliant wallet level, this extension enables gasless transfers for *all* ERC-721 nfts managed by the wallet, significantly expanding the reach of gasless NFT applications.

A standardized off-chain transfer signature reduces bespoke integrations and paves the way for widespread adoption of NFT-based interactions in Web3.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

Compliant ERC-7564 implementations that support this extension MUST include the following functions and behavior.

### Interface

interface IERC8189 { function nftTransferNonce(address asset, address to) external view returns (uint256); function nftTransferWithSig( address asset, uint256 tokenId, address to, uint256 deadline, bytes calldata signature ) external returns (bool success); }

- nftTransferNonce MUST return a monotonically increasing nonce scoped to (asset, to).
- nftTransferWithSig MUST verify the signature via isValidSignature, reject expired signatures (unless deadline == 0), increment the nonce before performing the transfer, and execute the same logic as nftTransfer in ERC-7564.

Implementations MUST support wallets that validate signatures through [ERC-1271](https://github.com/mossdapp/ERCs/blob/feat/nfttransfer-sig/eip-1271.md). Wallets MAY wrap signatures but the module MUST unwrap them prior to verification.

### Typed Data

Compliant implementations MUST use the following EIP-712 typed data structure. The `wallet` field identifies the smart contract wallet that will execute the transfer.

| Function | Primary Type | Fields |
| --- | --- | --- |
| nftTransferWithSig | NFTTransferWithSig | wallet, asset, to, tokenId, nonce, deadline |

Every permit MUST use the EIP-712 domain:

- name = "NFTManage Transfer"
- version = "1"
- chainId equal to the executing chain
- verifyingContract = address(this)

### Nonce Semantics

- nftTransferNonce MUST be scoped per (asset, to).

Each `WithSig` function MUST increment its nonce immediately before state changes and MUST revert on signature reuse.

### Execution Requirements

Implementations MUST:

1. Treat deadline = 0 as non-expiring; otherwise enforce block.timestamp <= deadline.
2. Recover the signer from the EIP-712 digest. Validate the digest using ERC-1271 on the wallet address. The recovered/validated signer MUST be authorized to act on behalf of the wallet (typically its owner).
3. Verify the provided nonce matches the current stored nonce for the corresponding scope.
4. Increment the scoped nonce before invoking the underlying ERC-7564 function.
5. Emit the same events as the underlying ERC-7564 functions.
6. Revert if signature validation fails, inputs mismatch, or deadlines are exceeded.

Wallets MAY offer helper wrappers, but they MUST NOT alter the semantics described above.

## Rationale

- Reusing the existing ERC-7564 entry points keeps events and accounting compatible with current deployments.
- This wallet-level approach supports gasless transfers for all ERC-721 NFTs, including those without native off-chain authorization mechanisms.

## Backwards Compatibility

Existing ERC-7564 implementations remain valid. Clients SHOULD feature-detect permit support by checking for `IERC8189` via [ERC-165](https://github.com/mossdapp/ERCs/blob/feat/nfttransfer-sig/eip-165.md) or probing the new function selectors.

## Replies

**Ankita.eth** (2025-12-25):

I like the direction of this proposal. Handling NFT transfer authorization at the **wallet level** instead of the NFT contract itself feels like the right abstraction, especially if the goal is to make gasless NFT interactions broadly usable without fragmenting standards.

A few points and questions from an implementation perspective:

**Why this approach makes sense**

- Wallet-level authorization scales better than NFT-level permits
By extending ERC-7564 wallets instead of touching ERC-721 contracts, this works for all NFTs, including legacy collections. That’s a big practical win.
- Relayer-friendly without compromising security
Using EIP-712 + ERC-1271 keeps the trust model clean. The wallet owner authorizes intent, anyone can relay, and the wallet remains the final enforcer.
- Good UX foundation for gasless flows
Gifting, claimable drops, and custodial or mobile-first wallets all benefit from this without forcing users to hold ETH.

**Questions / considerations**

- Nonce scoping (asset, to)
What was the reasoning behind scoping nonces per (asset, to) instead of (asset, tokenId) or a global wallet nonce?
From an integrator’s view, this choice impacts how parallel authorizations and batching are handled.
- Partial replay risk across destinations
Since the nonce is destination-scoped, signing the same NFT for different to addresses would require separate signatures. This seems intentional, but it might be worth clarifying as a UX trade-off in the spec.
- Multisig / modular wallet flows
For wallets with delayed or aggregated ERC-1271 validation (e.g. multisig thresholds or session keys), are there any known edge cases around deadline enforcement or nonce invalidation that implementers should watch for?

This feels like a pragmatic and composable extension to ERC-7564 rather than a competing NFT transfer standard. If standardized cleanly, it could remove a lot of bespoke “gasless NFT” logic currently being reimplemented at the app layer.

