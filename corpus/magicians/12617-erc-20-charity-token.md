---
source: magicians
topic_id: 12617
title: ERC-20 Charity token
author: b_eab
date: "2023-01-18"
category: ERCs
tags: [erc, token, donations]
url: https://ethereum-magicians.org/t/erc-20-charity-token/12617
views: 2167
likes: 0
posts_count: 6
---

# ERC-20 Charity token

## Abstract

An extension to EIP-20 that can automatically send an additional percentage of each transfer to a third party, and that provides an interface for retrieving this information. This can allow token owners to make donations to a charity with every transfer. This can also be used to allow automated savings programs.

## Motivation

There are charity organizations with addresses on-chain, and there are token holders who want to make automated donations. Having a standardized way of collecting and managing these donations helps users and user interface developers. Users can make an impact with their token and can contribute to achieving sustainable blockchain development. Projects can easily retrieve charity donations addresses and rate for a given EIP-20 token, token holders can compare minimum rate donation offers allowed by token contract owners. This standard provides functionality that allows token holders to donate easily.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

Owner of the contract **MAY**, after review, register charity address in `whitelistedRate` and set globally a default rate of donation. To register the address, the rate **MUST** not be null.

Token holders **MAY** choose and specify a default charity address from `_defaultAddress`, this address **SHOULD** be different from the null address for the donation to be activated.

The donation is a percentage-based rate model, but the calculation can be done differently. Applications and individuals can implement this standard by retrieving information with `charityInfo()` , which specifies an assigned rate for a given address.

This standard provides functionality that allows token holders to donate easily. The donation when activated is done directly in the overridden `transfer`, `transferFrom`, and `approve` functions.

When `transfer`, `transferFrom` are called the sender’s balance is reduced by the initial amount and a donation amount is deduced. The initial transfered amount is transferred to the recipient’s balance and an additional donation amount is transfered to a third party (charity). The two transfer are done at the same time and emit two `Transfer` events.

Also, if the account has an insufficient balance to cover the transfer and the donation the whole transfer would revert.

```solidity
// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.4;

///
/// @dev Required interface of an ERC20 Charity compliant contract.
///
interface IERC20charity is IERC165 {
    /// The EIP-165 identifier for this interface is 0x557512b6


    /**
     * @dev Emitted when `toAdd` charity address is added to `whitelistedRate`.
     */
    event AddedToWhitelist (address toAdd);

    /**
     * @dev Emitted when `toRemove` charity address is deleted from `whitelistedRate`.
     */
    event RemovedFromWhitelist (address toRemove);

    /**
     * @dev Emitted when `_defaultAddress` charity address is modified and set to `whitelistedAddr`.
     */
    event DonnationAddressChanged (address whitelistedAddr);

    /**
     * @dev Emitted when `_defaultAddress` charity address is modified and set to `whitelistedAddr`
    * and _donation is set to `rate`.
     */
    event DonnationAddressAndRateChanged (address whitelistedAddr,uint256 rate);

    /**
     * @dev Emitted when `whitelistedRate` for `whitelistedAddr` is modified and set to `rate`.
     */
    event ModifiedCharityRate(address whitelistedAddr,uint256 rate);

    /**
    *@notice Called with the charity address to determine if the contract whitelisted the address
    *and if it is the rate assigned.
    *@param addr - the Charity address queried for donnation information.
    *@return whitelisted - true if the contract whitelisted the address to receive donnation
    *@return defaultRate - the rate defined by the contract owner by default , the minimum rate allowed different from 0
    */
    function charityInfo(
        address addr
    ) external view returns (
        bool whitelisted,
        uint256 defaultRate
    );

    /**
    *@notice Add address to whitelist and set rate to the default rate.
    * @dev Requirements:
     *
     * - `toAdd` cannot be the zero address.
     *
     * @param toAdd The address to whitelist.
     */
    function addToWhitelist(address toAdd) external;

    /**
    *@notice Remove the address from the whitelist and set rate to the default rate.
    * @dev Requirements:
     *
     * - `toRemove` cannot be the zero address.
     *
     * @param toRemove The address to remove from whitelist.
     */
    function deleteFromWhitelist(address toRemove) external;

    /**
    *@notice Get all registered charity addresses.
     */
    function getAllWhitelistedAddresses() external ;

    /**
    *@notice Display for a user the rate of the default charity address that will receive donation.
     */
    function getRate() external view returns (uint256);

    /**
    *@notice Set personlised rate for charity address in {whitelistedRate}.
    * @dev Requirements:
     *
     * - `whitelistedAddr` cannot be the zero address.
     * - `rate` cannot be inferior to the default rate.
     *
     * @param whitelistedAddr The address to set as default.
     * @param rate The personalised rate for donation.
     */
    function setSpecificRate(address whitelistedAddr , uint256 rate) external;

    /**
    *@notice Set for a user a default charity address that will receive donation.
    * The default rate specified in {whitelistedRate} will be applied.
    * @dev Requirements:
     *
     * - `whitelistedAddr` cannot be the zero address.
     *
     * @param whitelistedAddr The address to set as default.
     */
    function setSpecificDefaultAddress(address whitelistedAddr) external;

    /**
    *@notice Set for a user a default charity address that will receive donation.
    * The rate is specified by the user.
    * @dev Requirements:
     *
     * - `whitelistedAddr` cannot be the zero address.
     * - `rate` cannot be less than to the default rate
     * or to the rate specified by the owner of this contract in {whitelistedRate}.
     *
     * @param whitelistedAddr The address to set as default.
     * @param rate The personalised rate for donation.
     */
    function setSpecificDefaultAddressAndRate(address whitelistedAddr , uint256 rate) external;

    /**
    *@notice Display for a user the default charity address that will receive donation.
    * The default rate specified in {whitelistedRate} will be applied.
     */
    function specificDefaultAddress() external view returns (
        address defaultAddress
    );

    /**
    *@notice Delete The Default Address and so deactivate donnations .
     */
    function deleteDefaultAddress() external;
}

```

### Functions

#### addToWhitelist

Add address to whitelist and set the rate to the default rate.

| Parameter | Description |
| --- | --- |
| toAdd | The address to the whitelist. |

#### deleteFromWhitelist

Remove the address from the whitelist and set rate to the default rate.

| Parameter | Description |
| --- | --- |
| toRemove | The address to remove from whitelist. |

#### getAllWhitelistedAddresses

Get all registered charity addresses.

#### getRate

Display for a user the rate of the default charity address that will receive donation.

#### setSpecificRate

Set personalized rate for charity address in {whitelistedRate}.

| Parameter | Description |
| --- | --- |
| whitelistedAddr | The address to set as default. |
| rate | The personalised rate for donation. |

#### setSpecificDefaultAddress

Set for a user a default charity address that will receive donations. The default rate specified in {whitelistedRate} will be applied.

| Parameter | Description |
| --- | --- |
| whitelistedAddr | The address to set as default. |

#### setSpecificDefaultAddressAndRate

Set for a user a default charity address that will receive donations. The rate is specified by the user.

| Parameter | Description |
| --- | --- |
| whitelistedAddr | The address to set as default. |
| rate | The personalized rate for donation. |

#### specificDefaultAddress

Display for a user the default charity address that will receive donations. The default rate specified in {whitelistedRate} will be applied.

#### deleteDefaultAddress

Delete The Default Address and so deactivate donations.

#### charityInfo

Called with the charity address to determine if the contract whitelisted the address and if it is, the rate assigned.

| Parameter | Description |
| --- | --- |
| addr | The Charity address queried for donnation information. |

## Rationale

This EIP chooses to whitelist charity addresses by using an array and keeping track of the “active” status with a mapping `whitelistedRate` to allow multiple choice of recipient and for transparence. The donation address can also be a single address chosen by the owner of the contract and modified by period.

If the sender balance is insuficent i.e total amount of token (initial transfer + donation) is insuficent the transfer would revert. Donation are done in the `transfer` function to simplify the usage and to not add an additional function, but the implementation could be donne differently, and for exemple allow a transfer to go through without the donation amount when donation is activated. The token implementer can also choose to store the donation in the contract or in another one and add a withdrawal or claimable function, so the charity can claim the allocated amount of token themselves, the additional transfer will be triggered by the charity and not the token holder.

Also, donations amount are calculated here as a percentage of the amount of token transfered to allow different case scenario, but the token implementer can decide to opt for another approach instead like rounding up the transaction value.

## Backwards Compatibility

This implementation is an extension of the functionality of EIP-20, it introduces new functionality retaining the core interfaces and functionality of the EIP-20 standard. There is a small backwards compatibility issue, indeed if an account has insufficient balance, it’s possible for the transfer to fail.

## Security Considerations

There are no additional security considerations compared to EIP-20.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**b_eab** (2023-01-18):

Link to EIP PR: [EIP-6353: 6353: Charity token · Pull Request #6353 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6353)

---

**SamWilsn** (2023-01-23):

Some non-editing related comments (meaning you’re free to ignore them and they won’t affect your PR getting merged):

I would:

- Remove the whitelist management functions/events from the standard. Only the contract owner will use them, and specifying them makes the EIP less general purpose. Just specify that setSpecificRate may revert if the given rate or address isn’t allowed.
- Make the specification more general. Simplify it down to just:

setAdditionalRate(uint256 rate): set the function caller’s donation rate to rate.
- additionalRateOf(address addr): returns addr’s donation rate.
- setAdditionalRecipient(address addr): set the function caller’s donation destination to addr.
- additionalRecipientOf(address addr): returns addr’s donation recipient.

Remove the default rate stuff. The contract author can set one, and users can query it (by just querying their own address.)

---

**radek** (2023-01-25):

Working with charities myself, there is a common case of the micro transaction related to the rounding up the transaction value (instead of %rate). Example - rounding up to 5 USD for each tx → sending 83 will send 2 USD to charity.

Can you consider this approach as well?

---

**SamWilsn** (2023-02-05):

As part of our process to encourage peer review, we assign a volunteer peer reviewer to read through your proposal and post any feedback here. Your peer reviewer is [@arturo](/u/arturo)! Please note that this review **is NOT required** to move your EIP through the process. When you—the authors—feel ready, just open a pull request.

If any of this EIP’s authors would like to participate in the volunteer peer review process, [shoot me a message](https://ethereum-magicians.org/new-message?username=SamWilsn&title=Peer+Review+Volunteer)!

---

[@arturo](/u/arturo) please take a look through [EIP-6353](https://eips.ethereum.org/EIPS/eip-6353) and comment here with any feedback or questions. Thanks!

---

**b_eab** (2023-02-06):

Thanks, that’s a good idea, each implementation can calculate the donation amount differently, so I added the rounding-up method as an implementation option.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/b/ee59a6/48.png) b_eab:

> Also, donations amount are calculated here as a percentage of the amount of token transfered to allow different case scenario, but the token implementer can decide to opt for another approach instead like rounding up the transaction value.

