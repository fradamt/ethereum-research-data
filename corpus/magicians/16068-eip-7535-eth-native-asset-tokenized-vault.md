---
source: magicians
topic_id: 16068
title: "EIP-7535: ETH (Native Asset) Tokenized Vault"
author: joeysantoro
date: "2023-10-12"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-7535-eth-native-asset-tokenized-vault/16068
views: 2059
likes: 3
posts_count: 5
---

# EIP-7535: ETH (Native Asset) Tokenized Vault

---

## eip: 7535
title: ETH (Native Asset) Tokenized Vault
description: ERC-4626 Tokenized Vaults with ETH as the underlying asset
author: Joey Santoro ()
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2023-10-12
requires: 4626, 7528

## Abstract

The following standard allows for the implementation of a standard API for Tokenized Vaults that use ETH as the underlying asset.

This standard is an extension of the ERC-4626 spec with an identical interface and behavioral overrides for handling ETH as the underlying.

## Motivation

A standard for tokenized ETH Vaults has the same benefits as ERC-4626, particularly in the case of Liquid Staking Tokens, (i.e. fungible ERC-20 wrappers around ETH staking).

Maintaining the same exact interface as ERC-4626 further amplifies the benefits as the standard will be maximally compatible with existing ERC-4626 tooling and protocols.

## Specification

All EIP-7535 tokenized Vaults MUST implement ERC-4626 with behavioral overrides for the methods `asset`, `deposit`, and `mint` specified below.

### Methods

#### asset

MUST return `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE ` per EIP-7528 (TODO add link once merged).

```yaml
- name: asset
  type: function
  stateMutability: view

  inputs: []

  outputs:
    - name: assetTokenAddress
      type: address
```

#### deposit

Mints `shares` Vault shares to `receiver` by depositing exactly `msg.value` of Ether.

MUST have state mutability of `payable`.

MUST use `msg.value` as the primary input parameter for calculating the `shares` output. MAY ignore `assets` parameter as an input.

MUST emit the `Deposit` event.

MUST revert if all of `msg.value` cannot be deposited (due to deposit limit being reached, slippage, etc).

```yaml
- name: deposit
  type: function
  stateMutability: payable

  inputs:
    - name: assets
      type: uint256
    - name: receiver
      type: address

  outputs:
    - name: shares
      type: uint256
```

#### mint

Mints exactly `shares` Vault shares to `receiver` by depositing `assets` of ETH.

MUST have state mutability of `payable`.

MUST emit the `Deposit` event.

MUST revert if all of `shares` cannot be minted (due to deposit limit being reached, slippage, the user not sending a large enough `msg.value` of Ether to the Vault contract, etc).

```yaml
- name: mint
  type: function
  stateMutability: payable

  inputs:
    - name: shares
      type: uint256
    - name: receiver
      type: address

  outputs:
    - name: assets
      type: uint256
```

### Events

The event usage MUST be identical to ERC-4626.

## Rationale

This standard was designed to maximize compatibility with ERC-4626 while minimizing additional opinionated details on the interface. Examples of this decision rationale are described below:

- maintaining the redundant assets input to the deposit function while making its usage optional
- not enforcing a relationship between msg.value and assets in a mint call
- not enforcing any behaviors or lack thereof for fallback/__default__ methods, payability on additional vault functions, or handling ETH forcibly sent to the contract

## Backwards Compatibility

EIP-X is fully backward compatible with ERC-4626 at the function interface level. Certain implementation behaviors are different due to the fact that ETH is not ERC-20 compliant, such as the priority of `msg.value` over `assets`.

It has no known compatibility issues with other standards.

## Reference Implementation

TODO / WIP

## Security Considerations

In addition to all security considerations of ERC-4626, there are security implications of having ETH as the Vault asset.

### call vs send

Contracts should take care when using `call` to transfer ETH, as this allows additional reentrancy vulnerabilities and arbitrary code execution beyond what is possible with trusted ERC-20 tokens.

It is safer to simply `send` ETH with a small gas stipend.

Implementers should take extra precautions when deciding how to transfer ETH.

### Forceful ETH transfers

ETH can be forced into any Vault through the `SELFDESTRUCT` opcode. Implementers should validate that this does not disrupt Vault accounting in any way.

Similarly, any additional `payable` methods should be checked to ensure they do not disrupt Vault accounting.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**albertocuestacanada** (2023-10-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joeysantoro/48/5147_2.png) joeysantoro:

> not enforcing a relationship between msg.value and assets in a mint call

Why are we not enforcing `msg.value == assets` in `mint` and `deposit`? It seems to me that it has zero cost for the caller to make them match. If you want to allow the caller to be lazy and not set `assets`, you can require that it must be zero. Personally, I would require that they match.

---

**joeysantoro** (2023-10-13):

for deposit, its purely for gas reasons to allow the parameter to be ignored. I could change it to should match or even must match but I don’t think this is necessary. Its most important that the interface matches

for mint, I want to allow the possibility that the user sends in some eth but not the exact amount and the difference is returned to the user for example

I’m open to the idea that we should be more opinionated on both of these cases but I think it only adds gas on deposit and more difficulty of integrating on mint

---

**albertocuestacanada** (2023-10-13):

I see, I think that you are right on one count, maybe not so much on the other.

On `mint` I think that you are right. We don’t have `transferFrom` for Ether, so users need to send an amount as they call `mint`. The on-chain way of knowing how much exactly would be to call `mintPreview` before `mint`, but some implementations might choose to calculate `assets` offchain and save the gas cost of `mintPreview`. If some implementations want to return unused Ether, there is no reason to stop them.

On `deposit`, my problem here is with MAY, which leads to undefined behaviour.

I think that the right approach is to take `assets` as the truth as to what the user wants to do, but then implementations need to ensure that `msg.value >= assets`, which has the same gas cost as ensuring that `msg.value == assets`.

That seems to leave us with asking that implementations MUST ignore `assets`, and act solely on `msg.value`. It is a bit weird, but as long as anyone reads the EIP is safe. Besides, if someone ignores that MUST, they will still be probably fine as most callers will use `assets = 0` to save on calldata gas.

---

**joeysantoro** (2023-10-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/albertocuestacanada/48/3057_2.png) albertocuestacanada:

> I think that the right approach is to take assets as the truth as to what the user wants to do, but then implementations need to ensure that msg.value >= assets, which has the same gas cost as ensuring that msg.value == assets.

I think this is more of a purist approach, however if a user is actually sending ETH via msg.value, it is hard to imagine why `assets` would ever be a truer value. `MAY` seems like undefined behavior, but it really does mean `MUST NOT` rely on `assets` only.

“MAY ignore assets parameter as an input” could be removed, but I think the spec benefits from having some extra clarification here.

Forcing everyone to require `msg.value >= assets` could just let people use assets=0 always anyway. I think the benefits of forcing any kind of relationship are negligible and having the explicit behavior of relying on msg.value is cleaner and has fewer footguns.

