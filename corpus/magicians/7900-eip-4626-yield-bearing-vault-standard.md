---
source: magicians
topic_id: 7900
title: "EIP-4626: Yield Bearing Vault Standard"
author: joeysantoro
date: "2022-01-05"
category: EIPs
tags: [vaults]
url: https://ethereum-magicians.org/t/eip-4626-yield-bearing-vault-standard/7900
views: 22142
likes: 46
posts_count: 109
---

# EIP-4626: Yield Bearing Vault Standard

---

## eip: 4626
title: Yield Bearing Vault Standard
description: A standard for yield bearing vaults.
author: Joey Santoro (), t11s (@transmissions11), Jet Jadeja (@JetJadeja)
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2021-12-22

# Yield Bearing Vault Standard

## Simple Summary

A standard for yield bearing vaults.

## Abstract

The following standard allows for the implementation of a standard API for yield bearing vaults within smart contracts. This standard provides basic functionality for depositing and withdrawing tokens and reading balances with an optional extension for tokenized vaults using ERC-20.

## Motivation

Yield bearing vaults have a lack of standardization leading to diverse implementation details. Some various examples include lending markets (Compound, Aave, Fuse), aggregators (Yearn, Rari Vaults, Idle), and intrinsically interest bearing tokens (xSushi). This makes integration difficult at the aggregator or plugin layer for protocols which need to conform to many standards. This forces each protocol to implement their own adapters which are error prone and waste development resources.

A standard for yield bearing vaults will allow for a similar cambrian explosion to ERC-20, unlocking access to yield in a variety of applications with little specialized effort from developers.

## Specification

### Methods

#### deposit

`function deposit(address _to, uint256 _value) public returns (uint256 _shares)`

Deposits `_value` tokens into the vault and grants ownership of them to `_to`.

MAY return a pro-rata ownership `_shares` value corresponding `_value`, if not MUST return `0`.

MAY represent `_shares` using internal accounting or an ERC-20 token.

If pro-rata shares ownership is implemented, the vault SHOULD implement `balanceOf`, `redeem`, `totalSupply` and `exchangeRate`.

#### withdraw

`function withdraw(address _to, uint256 _value) public returns (uint256 _shares)`

Withdraws `_value` tokens from the vault and transfers them to `_to`.

MAY return a pro-rata ownership `_shares` value corresponding to `_value`,  if not MUST return `0`.

#### totalHoldings

`function totalHoldings() public view returns (uint256)`

Returns the total amount of underlying tokens held/managed by the vault.

#### balanceOfUnderlying

`function balanceOfUnderlying(address _owner) public view returns (uint256)`

Returns the total amount underlying tokens held in the vault for `_owner`.

#### underlying

`function underlying() public view returns (address)`

Returns the address of the token the vault uses for accounting, depositing, and withdrawing.

SHOULD return a token implementing the ERC-20 standard.

#### totalSupply

`function totalSupply() public view returns (uint256)`

Returns the total number of unredeemed vault shares in circulation.

OPTIONAL - This method is only needed for vaults that implement a pro-rata share mechanism for deposits.

#### balanceOf

`function balanceOf(address _owner) public view returns (uint256)`

Returns the total amount of vault shares the `_owner` currently has.

OPTIONAL - This method is only needed for vaults that implement a pro-rata share mechanism for deposits.

#### redeem

`function redeem(address _to, uint256 _shares) public returns (uint256 _value)`

Redeems a specific number of `_shares` for underlying tokens and transfers them to `_to`.

MAY return a pro-rata ownership `_shares` value corresponding `_value`, if not MUST return `0`.

OPTIONAL - This method is only needed for vaults that implement a pro-rata share mechanism for deposits.

#### exchangeRate

`function exchangeRate() public view returns (uint256)`

The amount of underlying tokens one `baseUnit` of vault shares is redeemable for.

e.g. `_shares * exchangeRate() / baseUnit() = _value`.

`exchangeRate() * totalSupply()` MUST equal `totalHoldings()`.

OPTIONAL - This method is only needed for vaults that implement a pro-rata share mechanism for deposits.

#### baseUnit

`function baseUnit() public view returns(uint256)`

The decimal scalar for vault shares and operations involving `exchangeRate()`.

OPTIONAL - This method is only needed for vaults that implement a pro-rata share mechanism for deposits.

### Events

#### Deposit

MUST be emitted when tokens are deposited into the vault.

`event Deposit(address indexed _from, addres indexed _to, uint256 _value)`

Where `_from` is the user who triggered the deposit and approved `_value` underlying tokens to the vault, and `_to` is the user who is able to withdraw the deposited tokens.

#### Withdraw

MUST be emitted when tokens are withdrawn from the vault by a depositor.

`event Withdraw(address indexed _owner, addres indexed _to, uint256 _value)`

Where `_from` is the user who triggered the withdrawal and held `_value` underlying tokens in the vault, and `_to` is the user who received the withdrawn tokens.

## Rationale

The vault interface is designed to be optimized for minimal implementation and integration logic while maintaining flexibility for both parties. Details such as accounting and allocation of deposited tokens are intentionally not specified, as vaults are expected to be treated as black boxes on-chain and inspected off-chain before use.

## Reference Implementation

[Solmate Minimal Implementation](https://github.com/Rari-Capital/solmate/pull/88) - a tokenized vault using the ERC-20 extension with hooks for developers to add logic in deposit and withdraw.

[Rari Vaults](https://github.com/Rari-Capital/vaults/blob/main/src/Vault.sol) are an implementation that is nearly ready for production release. Any discrepancies between the vaults abi and this ERC will be adapted to conform to the ERC before mainnet deployment.

## Security Considerations

This specification has similar security considerations to the ERC-20 interface. Fully permissionless yield aggregators, for example, could fall prey to malicious implementations which only conform to the interface but not the specification.

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## Replies

**aallamaa** (2022-01-07):

Hello,

EnreachDAO is looking at using your standard for our upcoming vaults.

Would it be possible to add a deposit with permit function “depositWithPermit” in the standard (ERC2612 permit)?

---

**albertocuestacanada** (2022-01-10):

Hi, the logic to execute ERC2612 permits in `deposit` doesn’t belong in the ERC4626 vault itself, but in an external contract that would interact with the vault.

Example: [ERC4626/ERC4626Router.sol at 7a947f2507b760ae470578cfb106f71ff5b1a14b · fei-protocol/ERC4626 · GitHub](https://github.com/fei-protocol/ERC4626/blob/7a947f2507b760ae470578cfb106f71ff5b1a14b/src/ERC4626Router.sol#L139)

---

**albertocuestacanada** (2022-01-10):

The ERC4626 states that `calculateShares(calculateUnderlying(sharesAmount))` MUST equal `sharesAmount`. That would prevent vaults to implement deposit or withdraw fees.

Same for `calculateUnderlying(calculateShares(underlyingAmount))` MUST equal `underlyingAmount`.

I suggest those two requirements are dropped.

---

**aallamaa** (2022-01-10):

Thanks for the pointer, the only issue here is that this implies 2 transfers, one from sender to router, then from router to vault, instead of a single transfer from sender to vault, having a deposit with permit would allow to reduce gas cost by having a single transfer, and for tokens with taxes this would reduce the amount of taxes on transfer.

---

**joeysantoro** (2022-01-12):

In favor, lets adjust the language to be more flexible to different use cases

---

**joeysantoro** (2022-01-12):

[Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-4626)





###



A standard for tokenized vaults with a single underlying ERC-20 token.










^ this is the up-to-date proposed standard

Thread explaining the changes: https://twitter.com/joey__santoro/status/1478489634300588032

---

**frangio** (2022-01-12):

> calculateShares(calculateUnderlying(shareAmount)) MUST equal shareAmount
> calculateUnderlying(calculateShares(underlyingAmount)) MUST equal underlyingAmount

Aren’t there cases where due to integer division this can’t be guaranteed?

---

**AlexTheEntreprenerd** (2022-01-12):

The reference implementation from Rari Vaults doesn’t handle tokens with feeOnTransfer, using one of those tokens will break accounting.

Despite the comments implying that the transfer will transfer the exact amount of tokens:



      [github.com](https://github.com/Rari-Capital/vaults/blob/ebf83010c1e326569465443927300ae7a2cbbd7b/src/Vault.sol#L282)





####



```sol


1. // We don't allow depositing 0 to prevent emitting a useless event.
2. require(underlyingAmount != 0, "AMOUNT_CANNOT_BE_ZERO");
3.
4. // Determine the equivalent amount of rvTokens and mint them.
5. _mint(msg.sender, underlyingAmount.fdiv(exchangeRate(), BASE_UNIT));
6.
7. emit Deposit(msg.sender, underlyingAmount);
8.
9. // Transfer in underlying tokens from the user.
10. // This will revert if the user does not have the amount specified.
11. UNDERLYING.safeTransferFrom(msg.sender, address(this), underlyingAmount);
12. }
13.
14. /// @notice Withdraw a specific amount of underlying tokens.
15. /// @param underlyingAmount The amount of underlying tokens to withdraw.
16. function withdraw(uint256 underlyingAmount) external {
17. // We don't allow withdrawing 0 to prevent emitting a useless event.
18. require(underlyingAmount != 0, "AMOUNT_CANNOT_BE_ZERO");
19.
20. // Determine the equivalent amount of rvTokens and burn them.
21. // This will revert if the user does not have enough rvTokens.


```










The check in safeTransferFrom is checking for the token optionally returning True, and is not a guarantee that you received the amount specified:



      [github.com](https://github.com/Rari-Capital/solmate/blob/dd13c61b5f9cb5c539a7e356ba94a6c2979e9eb9/src/utils/SafeTransferLib.sol#L53)





####



```sol


1. mstore(freeMemoryPointer, 0x23b872dd00000000000000000000000000000000000000000000000000000000) // Begin with the function selector.
2. mstore(add(freeMemoryPointer, 4), and(from, 0xffffffffffffffffffffffffffffffffffffffff)) // Mask and append the "from" argument.
3. mstore(add(freeMemoryPointer, 36), and(to, 0xffffffffffffffffffffffffffffffffffffffff)) // Mask and append the "to" argument.
4. mstore(add(freeMemoryPointer, 68), amount) // Finally append the "amount" argument. No mask as it's a full 32 byte value.
5.
6. // Call the token and store if it succeeded or not.
7. // We use 100 because the calldata length is 4 + 32 * 3.
8. callStatus := call(gas(), token, 0, freeMemoryPointer, 100, 0, 0)
9. }
10.
11. require(didLastOptionalReturnCallSucceed(callStatus), "TRANSFER_FROM_FAILED");
12. }
13.
14. function safeTransfer(
15. ERC20 token,
16. address to,
17. uint256 amount
18. ) internal {
19. bool callStatus;
20.
21. assembly {


```

---

**AlexTheEntreprenerd** (2022-01-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joeysantoro/48/5147_2.png) joeysantoro:

> #### withdraw
>
>
>
> function withdraw(address _to, uint256 _value) public returns (uint256 _shares)
>
>
> Withdraws _value tokens from the vault and transfers them to _to.
>
>
> MAY return a pro-rata ownership _shares value corresponding to _value, if not MUST return 0.

My criticism of the standard is very simple:

The majority of already existing vault systems use:

`withdraw(uint256 shares)`

That’s because shares become the unit of measure for the vault once you have deposited.

This is used because:

1. The token takes it’s own meaning and life (bBADGER, yveCRV)
2. The user interface is simpler: “You are going to burn X shares and receive underlying back”
3. The _value math is provenly more complicated, can break (especially if you add fees (e.g. withdrawal fees), and tends to leave dust. This is a known issue by all protocols that use the interface you are recommending.
To prove this I’ll just search for “Dust” on the Rari Capital Discord:
Screenshot 2022-01-12 at 23.32.48818×1464 280 KB

Practically this interface causes more issues than necessary, offer sub-par DX and UX and implicitly makes the majority of already existing Vault Systems non-compliant

---

**AlexTheEntreprenerd** (2022-01-12):

A separate criticism which I’ll leave for the developers considering this standard is that the reference implementation (Rari Vaults), while audited, has not been battle tested nor used in any meaningful capacity.

At first scrutiny, I can tell that the system offers very strong `admin privileges` which can put user deposits at risk. (Replacing withdrawal queue with a list of fake strategies being the first example I found, at the very least a DOS exploit, at worst a rug vector)

[![Screenshot 2022-01-12 at 23.38.21](https://ethereum-magicians.org/uploads/default/optimized/2X/0/0672fbeba782876eaabd7c54f0ae229f2244794a_2_690x224.png)Screenshot 2022-01-12 at 23.38.211372×446 102 KB](https://ethereum-magicians.org/uploads/default/0672fbeba782876eaabd7c54f0ae229f2244794a)

It also is a system with multiple strategies, which from my experience is a lot more complicated than one with single strategies.

So while I won’t speak about it’s security, I highly recommend you dive deep into the code to understand what you’re actually getting into as well as show a little skepticism for something that hasn’t been used in production.

---

**TransmissionsDev** (2022-01-13):

> My criticism of the standard is very simple:
> The majority of already existing vault systems use:
> withdraw(uint256 shares)

Yes, we provide this functionality as well via `redeem` which is standard in the Compound system.

Having a withdraw function that takes a fixed amount is useful for users who treat their accounts like bank accounts, withdrawing amounts they need for specific payments.

> To prove this I’ll just search for “Dust” on the Rari Capital Discord

This is petty and pretty uncool man. That message is referring to the old yield aggregator which was legacy code written months before I even joined the company as a frontend engineer. I agree with you that providing only a mechanism to withdraw a fixed amount of underlying is not a good idea because it leaves dust, which is why we provide a `redeem` method! The only argument here is about the naming, and considering this standard is already not backwards compatible we want to move in a more logical direction.

> makes the majority of already existing Vault Systems non-compliant

There is an incredible amount of diversity in vault interfaces, there’s no way we could make a standard backwards compatible with even a tiny fraction of them. We want to develop a standard for the next generation of vaults, working towards that goal will allows us to achieve a better interface, and not blow up trying to shim our interface into a bunch of existing designs.

---

**TransmissionsDev** (2022-01-13):

As the comment in your screenshot states, the queue is validated at withdrawal time, which prevents it from being used as a rug vector. In terms of DOS the queue will be capped after we push the changes from our latest audit. You’re correct the Vaults intentionally don’t handle fee on transfer tokens, but that has nothing to do with the standard or its viability as a reference implementation. Find the criticism about centralization odd because this is a pretty standard yield aggregator, we don’t have much more control over the system than any governed system like Yearn or Idle does, and again irrelevant to the discussion here. It’s provided as a reference impl to show how a complex system could implement this standard, not as a minimal base for other contracts, that’s the purpose of the Solmate impl. I’d be happy to side with its removal if you and others think it’s important.

I think there’s plenty of room for skepticism about the robustness of the Rari Vaults contract, which is why they’re not in production and one of the reasons why we made this standard (to reach community consensus on an optimal interface)! Would love to field more of your feedback but would request we do it outside of this forum if it’s about implementation details and not pertaining to the ERC4626 interface.

---

**joeysantoro** (2022-01-13):

Correct! I believe [@albertocuestacanada](/u/albertocuestacanada) updated the language in favor of a better invariant related to it returning the same value as a mint/deposit call in the same transaction

---

**albertocuestacanada** (2022-01-13):

`mint` and `withdraw`, but yes, it’s fixed now. The issue was not on rounding, but on the fact that some vaults might have fees.

---

**albertocuestacanada** (2022-01-13):

Approving the vault to pull underlying from users, with `permit` or any other method, would open the door for griefing attacks.

If you want to have single-transfer deposits or mints I suggest you check how we do it at yield. You can implement an ERC4626 vault that allows the router to use a single `transferFrom` from the user to the vault, then kick `deposit` in the same tx, and have the vault find the underlying that was transferred.

Example (not yet 4626) [vault-v2/Join.sol at 72a441a69e692b57050d0d9282db7eb3e7535519 · yieldprotocol/vault-v2 · GitHub](https://github.com/yieldprotocol/vault-v2/blob/72a441a69e692b57050d0d9282db7eb3e7535519/contracts/Join.sol#L52)

---

**furchill** (2022-01-13):

I would like to add, that a fair share of vaults implement a minimum lock in period, and with deposit to, won’t that make it a target of grief attack where people use it and deposit to some address and lock for `to` address would updated, thus locking funds in the address for that lock duration.

---

**jparklev** (2022-01-13):

Without `exchangeRate`, what’s the idiomatic way to query the exchange rate for one share?  Is it

`vault.calculateUnderlying(baseUnit)`?

Or I see that `baseUnit` isn’t in the spec, so maybe it’s

`vault.calculateUnderlying(10**vault.decimals())`?

Also could you expand on this [@albertocuestacanada](/u/albertocuestacanada)

> Approving the vault to pull underlying from users, with permit or any other method, would open the door for griefing attacks.

I was going to see if there’d been any discussion about having `from` in `mint` & `deposit`, but it seems like you’d have a concern?

---

**joeysantoro** (2022-01-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jparklev/48/5223_2.png) jparklev:

> Without exchangeRate, what’s the idiomatic way to query the exchange rate for one share? Is it

This is a great point and we may need to keep exchangeRate for oracles etc

> I was going to see if there’d been any discussion about having from in mint & deposit, but it seems like you’d have a concern?

I’m open to it if and only if `from` and `msg.sender` BOTH have ERC20 approval, otherwise this presents a major risk when approving the vault as anyone can force your tokens into the vault. However the extra approval would need to be checked asynchronously and be left dangling. None of these improve developer experience or save gas, so we left it out

---

**jparklev** (2022-01-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joeysantoro/48/5147_2.png) joeysantoro:

> I’m open to it if and only if from and msg.sender BOTH have ERC20 approval, otherwise this presents a major risk when approving the vault as anyone can force your tokens into the vault. However the extra approval would need to be checked asynchronously and be left dangling. None of these improve developer experience or save gas, so we left it out

Yea, good shout. I can’t think of many benefits if there’s a double approval like that, and I see the justification for it now

---

**albertocuestacanada** (2022-01-14):

> maybe it’s
> vault.calculateUnderlying(10**vault.decimals()) ?

That’s correct, and that’s intentional.

A function such as `exchangeRate` returns a factor, and there is no standard as to which how many decimals a factor should have. Compound notoriously defines this as *an unsigned integer, scaled by 1 * 10^(18 - 8 + Underlying Token Decimals).*

If you want to know how much underlying you need to pay for one share, you ask for that, and that’s what you get with no further guessing.

Note that if the vault would have no decimals, the query would still work fine.

Also, in multi-hop oracle conversions, as we do for Yield, you don’t need to worry about decimals at all, it just works.

https://github.com/yieldprotocol/vault-v2/blob/master/contracts/oracles/composite/CompositeMultiOracle.sol


*(88 more replies not shown)*
