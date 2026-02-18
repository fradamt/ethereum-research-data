---
source: magicians
topic_id: 25985
title: "ERC-8064: Contract wallet management token Permit Extensions"
author: wenzhenxiang
date: "2025-10-27"
category: ERCs
tags: [token]
url: https://ethereum-magicians.org/t/erc-8064-contract-wallet-management-token-permit-extensions/25985
views: 72
likes: 0
posts_count: 4
---

# ERC-8064: Contract wallet management token Permit Extensions

## Abstract

This proposal extends [ERC-7204](https://eips.ethereum.org/ERCS/erc-7204) smart-wallet token managers with an off-chain authorization flow similar to `permit`. It introduces nonce-tracked `tokenTransferWithSig`, `tokenApproveWithSig`, and `tokenSetApprovalForAllWithSig` functions so that transfers, individual allowances, and global operators can all be delegated after a typed-data signature is presented by the wallet owner. The extension defines the canonical EIP-712 schemas, nonce accounting, and expected behaviour for compliant implementations.

## Motivation

ERC-7204 describes a token management module for smart contract wallets, but stops short of standardising an off-chain signing workflow. Systems that wish to provide “red packet”-style transfers or account delegation flows must currently implement bespoke message encodings and nonce tracking, reducing interoperability. A shared permit definition enables wallets, relayers, and user interfaces to exchange signed transfer authorisations without bespoke integrations.

Goals:

- Allow wallets to hand out single-use, replay-protected transfer rights and operator approvals without on-chain transactions.
- Produce predictable EIP-712 schemas so that wallet UIs, SDKs, and relayers can sign and validate authorisations in a uniform manner.
- Maintain backwards compatibility with existing ERC-7204 deployments that do not implement permit extensions.

## Specification

The following additions are REQUIRED for an ERC-7204 compliant module that implements this extension.

### Interface

```solidity
interface IERC7204Permit {
    function tokenTransferNonce(address owner, address asset, address caller) external view returns (uint256);

    function tokenTransferWithSig(
        address owner,
        address asset,
        address to,
        uint256 value,
        uint256 deadline,
        bytes calldata signature
    ) external returns (bool success);

    function tokenApproveNonce(address owner, address asset, address operator, address caller)
        external
        view
        returns (uint256);

    function tokenApproveWithSig(
        address owner,
        address asset,
        address operator,
        uint256 value,
        uint256 deadline,
        bytes calldata signature
    ) external returns (bool success);

    function tokenApprovalForAllNonce(address owner, address caller) external view returns (uint256);

    function tokenSetApprovalForAllWithSig(
        address owner,
        address operator,
        bool approved,
        uint256 deadline,
        bytes calldata signature
    ) external returns (bool success);
}
```

- tokenTransferNonce MUST return a monotonically increasing nonce scoped to the tuple (owner, asset, caller).
- tokenTransferWithSig MUST:

Verify the signature using ERC-1271 at the smart wallet address.
- Require the caller of the module to equal the caller encoded in the signed message.
- Reject signatures whose deadline is in the past unless the deadline is 0.
- Increment the nonce returned by tokenTransferNonce immediately before performing the transfer.
- Perform the token transfer exactly as described in ERC-7204.

### Typed Data

Compliant implementations MUST hash the following payload and pass it to the wallet’s `isValidSignature` function:

- EIP-712 domain separator fields:

name = "TokenManager Permit"
- version = "1"
- chainId as observed by the module
- verifyingContract = address(this) (the wallet executing the module)

Primary type `TokenTransferWithSig` with the fields:

| Field | Type | Description |
| --- | --- | --- |
| wallet | address | The smart wallet address invoking the module. |
| owner | address | Wallet owner index that approved the transfer. |
| caller | address | The account expected to submit the transaction on-chain. |
| asset | address | ERC-20 asset to transfer. |
| to | address | Recipient of the assets. |
| value | uint256 | Amount of token units to transfer. |
| nonce | uint256 | Value returned by tokenTransferNonce(owner, asset, caller) |
| deadline | uint256 | Expiry timestamp; 0 represents no expiry. |

For approvals the primary types mirror the on-chain behaviour:

| Function | Primary Type | Fields |
| --- | --- | --- |
| tokenTransferWithSig | TokenTransferWithSig (wallet, owner, caller, asset, to, value, nonce, deadline) |  |
| tokenApproveWithSig | TokenApproveWithSig (wallet, owner, caller, asset, operator, value, nonce, deadline) |  |
| tokenSetApprovalForAllWithSig | TokenApprovalForAllWithSig (wallet, owner, caller, operator, approved, nonce, deadline) |  |

The module MUST wrap the owner signature in a format understood by the wallet (`ERC-1271` allows arbitrary encoding). Wallets using packed owner bytes (such as `SignatureWrapper{ ownerIndex, signatureData }`) MUST ensure the module forwards the wrapper unchanged.

### Nonce Semantics

- tokenTransferNonce MUST be scoped per (owner, asset, caller).
- tokenApproveNonce MUST be scoped per (owner, asset, operator, caller) so that multiple relayers can manage allowances independently.
- tokenApprovalForAllNonce MUST be scoped per (owner, caller).

## Rationale

- Caller binding prevents relayers from reusing signatures intended for other executors and mirrors the semantics of native ERC-20 permits as used in multicall payments.
- Per-function nonce scoping ensures transfers, per-operator approvals, and global approvals cannot replay one another.
- Domain name is intentionally generic (“TokenManager Permit”) so different implementations can interoperate. Wallets MAY expose additional domain separation through custom prefixes but MUST continue to accept the standard name.

## Backwards Compatibility

Existing ERC-7204 modules remain valid. Wallets SHOULD feature-detect permit support by checking whether the module implements `IERC7204Permit` via `supportsInterface` or by probing the function selectors.

## Security Considerations

- Wallets MUST guarantee that the nonce increments even if downstream transfers revert. Failing to do so could enable signature replay.
- Signers SHOULD evaluate deadline and refuse to sign if the value is too distant in the future.
- Integrators MUST validate caller to avoid inadvertently relaying authorisations intended for other contexts.

## Copyright

Copyright and related rights waived via [CC0-1.0](https://creativecommons.org/publicdomain/zero/1.0/).

## Replies

**SamWilsn** (2026-01-16):

I’m a bit of a proponent for using `validBefore` or `invalidAfter` instead of `deadline`, because they avoid any ambiguity between `<` and `<=` (respectively).

---

**SamWilsn** (2026-01-16):

> If the recovered address is a contract, validate the digest using ERC-1271 on the wallet address. The recovered/validated signer MUST equal the wallet owner.

This is not how ERC-1271 is supposed to work. You can’t “recover” a contract address, it has to be provided separately.

You’ll note that Uniswap’s [Permit2](https://github.com/Uniswap/permit2/blob/cc56ad0f3439c502c246fc5cfcc3db92bb8b7219/src/SignatureTransfer.sol#L25) requires an `owner` argument, and its [verify](https://github.com/Uniswap/permit2/blob/cc56ad0f3439c502c246fc5cfcc3db92bb8b7219/src/libraries/SignatureVerification.sol#L21-L46) implementation does a bunch of work to figure out if it should use `ecrecover` or ERC-1271.

---

**docbot** (2026-01-23):

This looks like a solid extension for ERC-7204. Standardizing the permit flow for smart account modules is definitely needed.

I have a question about the `tokenTransferNonce` scoping. You mention it must be scoped to the tuple `(owner, asset, caller)`.

While this offers granular replay protection, doesn’t it create a significant state bloat issue? If a user interacts with 50 different assets across 3 different relayers (callers), the contract has to initialize and store 150 separate storage slots.

Have you considered a simpler nonce model (like a single nonce per `owner` or per `owner + caller`)? It might sacrifice some concurrency but would be much cheaper gas-wise for the module to track.

