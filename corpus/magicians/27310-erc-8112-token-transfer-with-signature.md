---
source: magicians
topic_id: 27310
title: "ERC-8112: Token Transfer With Signature"
author: wenzhenxiang
date: "2025-12-25"
category: ERCs
tags: [erc, token, wallet]
url: https://ethereum-magicians.org/t/erc-8112-token-transfer-with-signature/27310
views: 84
likes: 2
posts_count: 2
---

# ERC-8112: Token Transfer With Signature

This proposal extends ERC-7204 compliant smart contract wallets with an off-chain signature flow for token transfers, allowing wallet owners to delegate transfers via typed-data signatures presented by any relayer. The extension defines a canonical EIP-712 schema, nonce accounting, and execution requirements for compliant implementations.

Unlike token-native standards, this extension operates at the wallet level, enabling gasless transfers for any ERC-20 token without requiring token contract modifications.

## Motivation

ERC-7204 enables programmable token management directly in smart contract wallets but requires on-chain transactions for every transfer. This creates friction for gasless use cases such as red packets, claimable airdrops, and relayer-sponsored transfers.

Traditional off-chain authorization standards like EIP-3009 require support from the token contract itself. Many legacy and new tokens do not implement these, limiting gasless usability.

By implementing authorization at the ERC-7204 compliant wallet level, this extension enables gasless transfers for *all* ERC-20 tokens managed by the wallet, significantly expanding the reach of gasless applications.

A standardized off-chain transfer signature reduces bespoke integrations and paves the way for widespread adoption of token-based payments in Web3.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

Compliant ERC-7204 implementations that support this extension MUST include the following functions and behavior.

### Interface

```solidity
interface IERC8188 {
    function tokenTransferNonce(address asset, address to) external view returns (uint256);

    function tokenTransferWithSig(
        address asset,
        address to,
        uint256 value,
        uint256 deadline,
        bytes calldata signature
    ) external returns (bool success);

```

- tokenTransferNonce MUST return a monotonically increasing nonce scoped to (asset, to).
- tokenTransferWithSig MUST verify the signature via isValidSignature, reject expired signatures (unless deadline == 0), increment the nonce before performing the transfer, and execute the same logic as tokenTransfer in ERC-7204.

Implementations MUST support wallets that validate signatures through ERC-1271. Wallets MAY wrap signatures but the module MUST unwrap them prior to verification.

### Typed Data

Compliant implementations MUST use the following EIP-712 typed data structure. The `wallet` field identifies the smart contract wallet that will execute the transfer.

| Function | Primary Type | Fields |
| --- | --- | --- |
| tokenTransferWithSig | TokenTransferWithSig | wallet, asset, to, value, nonce, deadline |

Every permit MUST use the EIP-712 domain:

- name = "TokenManage Transfer"
- version = "1"
- chainId equal to the executing chain
- verifyingContract = address(this)

### Nonce Semantics

- tokenTransferNonce MUST be scoped per (asset, to).

Each `WithSig` function MUST increment its nonce immediately before state changes and MUST revert on signature reuse.

### Execution Requirements

Implementations MUST:

1. Treat deadline = 0 as non-expiring; otherwise enforce block.timestamp ERC-165 or probing the new function selectors.

## Replies

**wjmelements** (2025-12-31):

> tokenTransferNonce MUST return a monotonically increasing nonce scoped to (asset, to).

This follows the pattern of ERC-2612 instead of the pattern of ERC-3009. Have you read the rationale behind ERC-3009? If you allow the nonce to be a random number, it allows [using the nonce to encode intent information](https://ethereum-magicians.org/t/using-the-erc-3009-permit-nonce-for-intent-witness-data/25216), which is quite useful.

> Traditional off-chain authorization standards like EIP-3009 require support from the token contract itself. Many legacy and new tokens do not implement these, limiting gasless usability.

This is a good point. But it is easier to get users to use your token than to get them to use your wallet.

> uint256 value

This field can be reused for ERC-721 support. You don’t need to have a separate standard for NFTs.

> bytes calldata signature

In the Solidity ABI this signature parameter uses 5 words (offset, size, v, r, s). If you changed this to `uint8 v, bytes32 r, bytes32 s` then it would be 3 words. If you use ERC-2098 or ERC-8111 it would be 2 words. Perhaps you want to allow for non-ECDSA signatures. If so, you can explain this in your Rationale.

