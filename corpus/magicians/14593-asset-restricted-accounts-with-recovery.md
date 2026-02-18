---
source: magicians
topic_id: 14593
title: Asset-restricted accounts with recovery
author: dcposch
date: "2023-06-06"
category: EIPs > EIPs interfaces
tags: [erc, wallet, account-abstraction]
url: https://ethereum-magicians.org/t/asset-restricted-accounts-with-recovery/14593
views: 475
likes: 1
posts_count: 1
---

# Asset-restricted accounts with recovery

# TL;DR

**This is a rough sketch of an interface for contracts that want to support a subset of assets and/or a subset of chains.**

Primary use case is simplified contract wallets. An ERC-4337 contract wallet can implement this interface to specify that it supports, for example, only a single stablecoin on a specific L2.

It comes with an optional recovery mechanism. There’s no way to prevent a sender from accidentally transfering in an unsupported asset, or any asset on an unsupported chain. If this happens–say, someone sends their ape to a DAI-only payments wallet–the recovery mechanism lets them retrieve it.

## Interface pseudocode

```auto
interface AssetRestrictedAccount {
   /** Chain support. 1 for mainnet, 10 for Optimism, etc */
   function supportsChain(uint256 chainID) public view returns (boolean);
   /** Asset support, with a special value (say 0xeee...) for ether */
   function supportsAsset(address asset) public view returns (boolean);

   /** Recovery */
   function supportsRecover() public view returns (boolean);
   /** If supportsRecover() is false, reverts. Otherwise, validates the proof that `sender` sent `asset` in `txHash`, then returns the asset. Must support simple transfers; support for any other kind of transaction is optional. */
   function recover(address sender, address asset, bytes32 txHash, bytes proof);
}
```

Asset-restricted accounts are also required to implement ERC-165 `supportsInterface`.

## UX enabled by this standard

A wallet or exchange that supports this standard can clarify their send UI.

The user enters a destination address, as usual. Then, for example:

- If the destination is not an asset-restricted account, everything works unchanged.
- If the destination does not support the asset being sent, show error message and disable send.
- If the destination supports only a specific chain, preselect that chain (or show an error with a “Switch Chains” button, etc).
- If the destination does support the asset being sent and chain, can show a subtle affirmation such as a check mark.

This is friendly to incremental adoption.

Importantly, unlike the alternative Numbered Accounts proposal ([Numbered Accounts](https://ethereum-magicians.org/t/numbered-accounts/14551)), you can send to your account from any existing UI that’s unaware of Asset-Restricted Accounts. You just won’t have the UI validation protections described above.

Finally, when displaying the *contents* of an asset-restricted account, a simplified display can be used. UIs like block explorers and wallets can display just the supported assets on the supported chain.

## Recovery motivation

If you want a simplified wallet (say, for payments on a single L2), you run into the problem of what to do if someone accidentally sends in an unsupported asset.

One way is to make the wallet support sending *any asset on any chain*, but that complicates the UX significantly.

Another option would be to give the underlying contract a `recover()` function.

- Anyone can call recover, submitting a proof that address X sent unsupported asset Y. (Or any asset, on an unsupported chain.)
- Contract verifies the proof, then sends Y back to X.

TLDR; this lets you make a recovery tool that operates totally independently of the wallet. Wallet app stays clean & just does payments.

## Recovery implementation

Recovery is optional. A wallet can implement the standard and just have `supportsRecovery` return false, `recover` revert.

If supported, it takes a proof (either a validity proof made with a tool like Axiom, or a potentially-large Merkle proof) that `sender` sent `asset` in transaction `txHash`. It verifies the proof and sends the asset back to `sender`.

Note that `msg.sender` can be anyone. This means that even if the sender wallet interface doesn’t support arbitrary transactions (say, because it’s an exchange wallet), a separate recovery tool can let senders retrieve an unsupported asset sent to a restricted account.

Arbitrary transactions are not necessarily reversible, but the common case of (a basic transfer of asset X to address Y that’s not meant to receive X) could be mitigated this way.

## Usage outside AA contract wallets

The motivating use case for asset-restricted accounts is simplified wallets. However, any contract can implement this spec to signal that they don’t want to receive asset transfers, or only specific assets on specific chains.

For that purpose, it might be worth adding a blank `supportsReceive()` to the interface. Many contracts are designed such that users should never directly transfer ether or tokens to them. This would let those contracts indicate that explicitly.
