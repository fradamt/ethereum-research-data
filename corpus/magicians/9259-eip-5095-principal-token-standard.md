---
source: magicians
topic_id: 9259
title: "EIP-5095: Principal Token Standard"
author: JulianT
date: "2022-05-15"
category: EIPs
tags: [token]
url: https://ethereum-magicians.org/t/eip-5095-principal-token-standard/9259
views: 3349
likes: 0
posts_count: 8
---

# EIP-5095: Principal Token Standard

---

eip: 5089

title: Principal Token Standard

description: A standard for principal tokens (zero-coupon tokens) that are redeemable for a single underlying ERC-20 token at a future timestamp.

author: Julian Traversa (@JTraversa), Robert Robbins (@ robrobbins), Alberto Cuesta Cañada (@alcueca)

discussions-to: https://github.com/ethereum/EIPs/pull/5089

status: Draft

type: Standards Track

category: ERC

created: 2022-05-01

requires: 20, 2612

---

## Abstract

Principal tokens represent ownership of an underlying [EIP-20] token at a future timestamp.

This specification is an extension on the [EIP-20] token that provides basic functionality for depositing

and withdrawing tokens and reading balances and the EIP-2612 specification that provides

[EIP-712] signature based approvals.

## Motivation

Principal tokens lack standardization which has led to a difficult to navigate development space and diverse implementation

schemes.

The primary examples include yield tokenization platforms which strip future yield leaving a principal

token behind, as well as fixed-rate money-markets which utilize principal tokens as a medium

to lend/borrow.

This inconsistency in implementation makes integration difficult at the application layer as well as

wallet layer which are key catalysts for the space’s growth.

Developers are currently expected to implement individual adapters for each principal token, as well as adapters for

their pool contracts, and many times adapters for their custodial contracts as well, wasting significant developer resources.

## Specification

All Principal Tokens (PTs) MUST implement [EIP-20] to represent ownership of future underlying redemption.

If a PT is to be non-transferrable, it MAY revert on calls to `transfer` or `transferFrom`.

The [EIP-20] operations `balanceOf`, `transfer`, `totalSupply`, etc. operate on the Principal Token balance.

All Principal Tokens MUST implement [EIP-20]  optional metadata extensions.

The `name` and `symbol` functions SHOULD reflect the underlying token’s `name` and `symbol` in some way, as well as the origination protocol, and in the case of yield tokenization protocols, the origination money-market.

All Principal Tokens MAY implement [EIP-2612] to improve the UX of approving PTs on various integrations.

### Definitions:

- underlying: The token that Principal Tokens are redeemable for at maturity.
Has units defined by the corresponding [EIP-20] contract.
- maturity: The timestamp (unix) at which a Principal Token matures. Principal Tokens become redeemable for underlying at or after this timestamp.
- fee: An amount of underlying or Principal Token charged to the user by the Principal Token. Fees can exist on redemption or post-maturity yield.
- slippage: Any difference between advertised redemption value and economic realities of PT redemption, which is not accounted by fees.

### Methods

#### underlying

The address of the underlying token used by the Principal Token for accounting, and redeeming.

MUST be an EIP-20 token contract.

MUST *NOT* revert.

- name: underlying type: function stateMutability: view inputs:  outputs: - name: underlyingAddress type: address

#### maturity

The unix timestamp (uint256) at or after which Principal Tokens can be redeemed for their underlying deposit.

MUST *NOT* revert.

- name: maturity type: function stateMutability: view inputs:  outputs: - name: timestamp type: uint256

#### convertToUnderlying

The amount of underlying that would be exchanged for the amount of PTs provided, in an ideal scenario where all the conditions are met.

Before maturity, the amount of underlying returned is as if the PTs would be at maturity.

MUST NOT be inclusive of any fees that are charged against redemptions.

MUST NOT show any variations depending on the caller.

MUST NOT reflect slippage or other on-chain conditions, when performing the actual redemption.

MUST NOT revert unless due to integer overflow caused by an unreasonably large input.

MUST round down towards 0.

This calculation MAY NOT reflect the “per-user” price-per-principal-token, and instead should reflect the “average-user’s” price-per-principal-token, meaning what the average user should expect to see when exchanging to and from.

- name: convertToUnderlying type: function stateMutability: view inputs: - name: principalAmount type: uint256 outputs: - name: underlyingAmount type: uint256

#### convertToPrincipal

The amount of principal tokens that the principal token contract would request for redemption in order to provide the amount of underlying specified, in an ideal scenario where all the conditions are met.

MUST NOT be inclusive of any fees.

MUST NOT show any variations depending on the caller.

MUST NOT reflect slippage or other on-chain conditions, when performing the actual exchange.

MUST NOT revert unless due to integer overflow caused by an unreasonably large input.

MUST round down towards 0.

This calculation MAY NOT reflect the “per-user” price-per-principal-token, and instead should reflect the “average-user’s” price-per-principal-token, meaning what the average user should expect to see when redeeming.

- name: convertToPrincipal type: function stateMutability: view inputs: - name: underlyingAmount type: uint256 outputs: - name: principalAmount type: uint256

#### maxRedeem

Maximum amount of principal tokens that can be redeemed from the `owner` balance, through a `redeem` call.

MUST return the maximum amount of principal tokens that could be transferred from `owner` through `redeem` and not cause a revert, which MUST NOT be higher than the actual maximum that would be accepted (it should underestimate if necessary).

MUST factor in both global and user-specific limits, like if redemption is entirely disabled (even temporarily) it MUST return 0.

MUST NOT revert.

- name: maxRedeem type: function stateMutability: view inputs: - name: owner type: address outputs: - name: maxPrincipalAmount type: uint256

#### previewRedeem

Allows an on-chain or off-chain user to simulate the effects of their redeemption at the current block, given current on-chain conditions.

MUST return as close to and no more than the exact amount of underliyng that would be obtained in a `redeem` call in the same transaction. I.e. `redeem` should return the same or more `underlyingAmount` as `previewRedeem` if called in the same transaction.

MUST NOT account for redemption limits like those returned from maxRedeem and should always act as though the redemption would be accepted, regardless if the user has enough principal tokens, etc.

MUST be inclusive of redemption fees. Integrators should be aware of the existence of redemption fees.

MUST NOT revert due to principal token contract specific user/global limits. MAY revert due to other conditions that would also cause `redeem` to revert.

Note that any unfavorable discrepancy between `convertToUnderlying` and `previewRedeem` SHOULD be considered slippage in price-per-principal-token or some other type of condition.

- name: previewRedeem type: function stateMutability: view inputs: - name: principalAmount type: uint256 outputs: - name: underlyingAmount type: uint256

#### redeem

At or after maturity, burns exactly `principalAmount` of Principal Tokens from `from` and sends `underlyingAmount` of underlying tokens to `to`.

Interfaces and other contracts MUST NOT expect fund custody to be present. While custodial redemption of Principal Tokens through the Principal Token contract is extremely useful for integrators, some protocols may find giving the Principal Token itself custody breaks their backwards compatibility.

MUST emit the `Redeem` event.

MUST support a redeem flow where the Principal Tokens are burned from `owner` directly where `owner` is `msg.sender` or `msg.sender` has EIP-20 approval over the principal tokens of `owner`.

MAY support an additional flow in which the principal tokens are transferred to the Principal Token contract before the `redeem` execution, and are accounted for during `redeem`.

MUST revert if all of `principalAmount` cannot be redeemed (due to withdrawal limit being reached, slippage, the owner not having enough Principal Tokens, etc).

Note that some implementations will require pre-requesting to the Principal Token before a withdrawal may be performed. Those methods should be performed separately.

- name: redeem type: function stateMutability: nonpayable inputs: - name: principalAmount type: uint256 - name: to type: address - name: from type: address outputs: - name: underlyingAmount type: uint256

#### maxWithdraw

Maximum amount of the underlying asset that can be redeemed from the `owner` principal token balance, through a `withdraw` call.

MUST return the maximum amount of underlying tokens that could be redeemed from `owner` through `withdraw` and not cause a revert, which MUST NOT be higher than the actual maximum that would be accepted (it should underestimate if necessary).

MUST factor in both global and user-specific limits, like if withdrawals are entirely disabled (even temporarily) it MUST return 0.

MUST NOT revert.

- name: maxWithdraw type: function stateMutability: view inputs: - name: owner type: address outputs: - name: maxUnderlyingAmount type: uint256

#### previewWithdraw

Allows an on-chain or off-chain user to simulate the effects of their withdrawal at the current block, given current on-chain conditions.

MUST return as close to and no fewer than the exact amount of principal tokens that would be burned in a `withdraw` call in the same transaction. I.e. `withdraw` should return the same or fewer `principalAmount` as `previewWithdraw` if called in the same transaction.

MUST NOT account for withdrawal limits like those returned from maxWithdraw and should always act as though the withdrawal would be accepted, regardless if the user has enough principal tokens, etc.

MUST be inclusive of withdrawal fees. Integrators should be aware of the existence of withdrawal fees.

MUST NOT revert due to principal token contract specific user/global limits. MAY revert due to other conditions that would also cause `withdraw` to revert.

Note that any unfavorable discrepancy between `convertToPrincipal` and `previewWithdraw` SHOULD be considered slippage in price-per-principal-token or some other type of condition.

- name: previewWithdraw type: function stateMutability: view inputs: - name: underlyingAmount type: uint256 outputs: - name: principalAmount type: uint256

#### withdraw

Burns `principalAmount` from `owner` and sends exactly `underlyingAmount` of underlying tokens to `receiver`.

MUST emit the `Redeem` event.

MUST support a withdraw flow where the principal tokens are burned from `owner` directly where `owner` is `msg.sender` or `msg.sender` has [EIP-20] approval over the principal tokens of `owner`.

MAY support an additional flow in which the principal tokens are transferred to the principal token contract before the `withdraw` execution, and are accounted for during `withdraw`.

MUST revert if all of `underlyingAmount` cannot be withdrawn (due to withdrawal limit being reached, slippage, the owner not having enough principal tokens, etc).

Note that some implementations will require pre-requesting to the principal token contract before a withdrawal may be performed. Those methods should be performed separately.

- name: withdraw type: function stateMutability: nonpayable inputs: - name: underlyingAmount type: uint256 - name: receiver type: address - name: owner type: address outputs: - name: principalAmount type: uint256

### Events

#### Redeem

`from` has exchanged `principalAmount` of Principal Tokens for `underlyingAmount` of underlying, and transferred that underlying to `to`.

MUST be emitted when Principal Tokens are burnt and underlying is withdrawn from the contract in the `EIP5089.redeem` method.

- name: Redeem type: event inputs: - name: from indexed: true type: address - name: to indexed: true type: address - name: amount indexed: false type: uint256

#### Mature

The Principal Token has hit maturity, and a a state change has been recorded on the Principal Token contract for the first time post-maturity.

- name: Mature type: event inputs: - name: timestamp indexed: true type: uint256

## Rationale

The Principal Token interface is designed to be optimized for integrators with a core minimal interface alongside optional interfaces to enable backwards compatibility. Details such as accounting and management of underlying are intentionally not specified, as Principal Tokens are expected to be treated as black boxes on-chain and inspected off-chain before use.

[EIP-20] is enforced as implementation details such as token approval and balance calculation directly carry over. This standardization makes Principal Tokens immediately compatible with all [EIP-20] use cases in addition to EIP-5089.

All principal tokens are redeemable upon maturity, with the only variance being whether further yield is generated post-maturity. Given the ubiquity of redemption, the presence of `redeem` allows integrators to purchase Principal Tokens on an open market, and them later redeem them for a fixed-yield solely knowing the address of the Principal Token itself.

This EIP draws heavily on the design of [EIP-4626] because technically Principal Tokens could be described as a subset of Yield Bearing Vaults, extended with a `maturity` variable and restrictions on the implementation. However, extending [EIP-4626] would force PT implementations to include methods (namely, `mint` and `deposit`) that are not necessary to the business case that PTs solve. It can also be argued that partial redemptions (implemented via `withdraw`) are rare for PTs.

## Backwards Compatibility

This EIP is fully backward compatible with the [EIP-20] specification and has no known compatibility issues with other standards.

For production implementations of Principal Tokens which do not use EIP-5089, wrapper adapters can be developed and used, or wrapped tokens can be implemented.

## Reference Implementations

TBA

## Security Considerations

Fully permissionless use cases could fall prey to malicious implementations which only conform to the interface in this EIP but not the specification, failing to implement proper custodial functionality but offering the ability to purchase Principal Tokens through secondary markets.

It is recommended that all integrators review each implementation for potential ways of losing user deposits before integrating.

The `convertToUnderlying` method is an estimate useful for display purposes,

and do *not* have to confer the *exact* amount of underlying assets their context suggests.

As is common across many standards, it is strongly recommended to mirror the underlying token’s `decimals` if at all possible, to eliminate possible sources of confusion and simplify integration across front-ends and for other off-chain users.

## Copyright

Copyright and related rights waived via [CC0]

## Replies

**JulianT** (2022-06-06):

At this point we’ve gathered the input of ~10 teams and so far ended up with the edits above as of 06/06.

I’ve also implemented some test integrations across two products of ours with no issues, some suggested examples available if anyone would like! I’ll be open-sourcing all of that in the next couple days.

---

**devtooligan** (2022-06-12):

I’m going to move some of the conversation from the draft pr to here.

Starting with

> All principal tokens are redeemable upon maturity, with the only variance being whether further yield is generated post-maturity. Given the ubiquity of redemption, the presence of redeem allows integrators to purchase Principal Tokens on an open market, and them later redeem them for a fixed-yield solely knowing the address of the Principal Token itself.

[axic](https://github.com/axic)

This assumption only allows this standard to work in the case principal tokens are redeemable for the principal + yield. There are some systems where it has to be redeemed in tandem with the yield tokens.

Do you have any suggestion for covering that?

ContributorAuthor

[alcueca](https://github.com/alcueca)

I’ve been asking around and I haven’t found a system like the one that you describe that would be relevant, would you have any more detail?

---

**devtooligan** (2022-06-12):

> All principal tokens are redeemable upon maturity, with the only variance being whether further yield is generated post-maturity. Given the ubiquity of redemption, the presence of redeem allows integrators to purchase Principal Tokens on an open market, and them later redeem them for a fixed-yield solely knowing the address of the Principal Token itself.

**jparklev**

Another vote for removing `withdraw`!

**devtooligan**

For simplicity’s sake, i tend to agree with removing withdraw. There are enough helper functions for an external contract to easily calculate the how many tokens should be redeemed for a given amount of underlying.

**alcueca**

How would you do that, without knowing the internal implementation of a given 5089, and taking into account that `convert*` functions are not necessarily exact?

---

**devtooligan** (2022-06-12):

> alcueca
> How would you do that, without knowing the internal implementation of a given 5089, and taking into account that convert* functions are not necessarily exact?

Well technically there would be an off-chain iterative solution that could accomplish this.

It still seems more like an edge case to me.  I’m guessing most users just want to redeem shares, they don’t view their ptoken shares like a piggy bank to be withdrawn from (whereas they might look at a 4626 vault like that).

I still like removing for the sake of simplicity.

---

**JulianT** (2022-06-18):

So I believe that APWine requires the user redeem PTs+YTs in tandem?

Once their maturity hits, they provide PT holders and equivalent balance of YTs for the next maturity period. That said, I dont think this impacts the standard’s redeem because whatever PT balance would also be automatically matched by YTs post maturity.

Another possible interpretation of the comment might be about pre-maturity redemption though?

It could be that pre-maturity you have the option to redeem PTs assuming you have equivalent YT balance, though I dont know if this really fits into a standard (The intended use case here is to extend a simple interface for fixed-rate lending integration)

---

**JulianT** (2022-06-18):

I personally had withdraw in my implementations given our PTs accrue yield post maturity @ Swivel, and I think they make sense in context of that sort of implementation.

That saaaiid, we’ve generally removed a few optional methods/vars (e.g. uint256 public view maturityRate) that serve a similar purpose and are more related to the exact calculation of accrued yield.

So I’m pretty ambivalent here, I can see how `withdraw` might not be necessary in context of other removals.

---

**devtooligan** (2022-06-30):

I was initially against `withdraw()` (for reasons of simplicity) but after some additional thought (and a recent experience on another project) I have changed my mind.

While the average user may generally just be looking to redeem their principal tokens upon maturity, other protocols/integrators may have different needs.  Some sort of `redeem(convertToPrincipal...` or iterative solution incurs additional gas and may not provide the appropriate precision.

