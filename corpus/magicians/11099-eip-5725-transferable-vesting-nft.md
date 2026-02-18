---
source: magicians
topic_id: 11099
title: EIP-5725 Transferable Vesting NFT
author: Apeguru
date: "2022-09-29"
category: EIPs
tags: [nft, token]
url: https://ethereum-magicians.org/t/eip-5725-transferable-vesting-nft/11099
views: 4488
likes: 11
posts_count: 29
---

# EIP-5725 Transferable Vesting NFT

# EIP-5725 Vesting NFT

## Table of Contents

- EIP-5725 Vesting NFT

Table of Contents
- Simple Summary
- Abstract
- Motivation

Use Cases

[Specification](#specification)
[Rationale](#rationale)
[Backwards Compatibility](#backwards-compatibility)
[Reference Implementation](#reference-implementation)
[Test Cases](#test-cases)
[Security Considerations](#security-considerations)
[Extensions](#extensions)
[References](#references)
[Copyright](#copyright)
[Citation](#citation)

## Simple Summary

A **Non-Fungible Token** (NFT) standard used to vest tokens (EIP-20 or otherwise) over a vesting release curve.

## Abstract

The following standard allows for the implementation of a standard API for NFT based contracts that hold and represent the vested and locked properties of any underlying token (EIP-20 or otherwise) that is emitted to the NFT holder. This standard is an extension of the EIP-721 token that provides basic functionality for creating vesting NFTs, claiming the tokens and reading vesting curve properties.

## Motivation

Vesting contracts, including timelock contracts, lack a standard and unified interface, which results in diverse implementations of such contracts. Standardizing such contracts into a single interface would allow for the creation of an ecosystem of on- and off-chain tooling around these contracts. In addition of this, liquid vesting in the form of non-fungible assets can prove to be a huge improvement over traditional **Simple Agreement for Future Tokens** (SAFTs) or **Externally Owned Account** (EOA)-based vesting as it enables transferability and the ability to attach metadata similar to the existing functionality offered by with traditional NFTs.

Such a standard will not only provide a much-needed EIP-20 token lock standard, but will also enable the creation of secondary marketplaces tailored for semi-liquid SAFTs.

This standard also allows for a variety of different vesting curves to be implement easily.

These curves could represent:

- linear vesting
- cliff vesting
- exponential vesting
- custom deterministic vesting

### Use Cases

1. A framework  to release tokens over a set period of time that can be used to build many kinds of NFT financial products such as bonds, treasury bills, and many others.
2. Replicating SAFT contracts in a standardized form of semi-liquid vesting NFT assets

SAFTs are generally off-chain, while today’s on-chain versions are mainly address-based, which makes distributing vesting shares to many representatives difficult. Standardization simplifies this convoluted process.
3. Providing a path for the standardization of vesting and token timelock contracts

There are many such contracts in the wild and most of them differ in both interface and implementation.
4. NFT marketplaces dedicated to vesting NFTs

Whole new sets of interfaces and analytics could be created from a common standard for token vesting NFTs.
5. Integrating vesting NFTs into services like Gnosis Safe

A standard would mean services like Gnosis Safe could more easily and uniformly support interactions with these types of contracts inside of a multisig contract.
6. Enable standardized fundraising implementations and general fundraising that sell vesting tokens (eg. SAFTs) in a more transparent manner.
7. Allows tools, front-end apps, aggregators, etc. to show a more holistic view of the vesting tokens and the properties available to users.

Currently, every project needs to write their own visualization of the vesting schedule of their vesting assets. If this is standardized, third-party tools could be developed aggregate all vesting NFTs from all projects for the user, display their schedules and allow the user to take aggregated vesting actions.
8. Such tooling can easily discover compliance through the EIP-165 supportsInterface(IVestingNFT) check.
9. Makes it easier for a single wrapping implementation to be used across all vesting standards that defines multiple recipients, periodic renting of vesting tokens etc.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";

/**
 * @title Non-Fungible Vesting Token Standard
 * @notice A non-fungible token standard used to vest tokens (EIP-20 or otherwise) over a vesting release curve
 *  scheduled using timestamps.
 * @dev Because this standard relies on timestamps for the vesting schedule, it's important to keep track of the
 *  tokens claimed per Vesting NFT so that a user cannot withdraw more tokens than alloted for a specific Vesting NFT.
 */
interface IVestingNFT is IERC721 {
    event PayoutClaimed(uint256 indexed tokenId, address indexed recipient, uint256 _claimAmount);

    /**
     * @notice Claim the pending payout for the NFT
     * @dev MUST grant the claimablePayout value at the time of claim being called
     * MUST revert if not called by the token owner or approved users
     * SHOULD revert if there is nothing to claim
     * @param tokenId The NFT token id
     * @return amountClaimed The amount of tokens claimed in this call
     */
    function claim(uint256 tokenId) external returns (uint256 amountClaimed);

    /**
     * @notice Total amount of tokens which have been vested at the current timestamp.
     *   This number also includes vested tokens which have been claimed.
     * @dev It is RECOMMENDED that this function calls `vestedPayoutAtTime` with
     *   `block.timestamp` as the `timestamp` parameter.
     * @param tokenId The NFT token id
     * @return payout Total amount of tokens which have been vested at the current timestamp.
     */
    function vestedPayout(uint256 tokenId) external view returns (uint256 payout);

    /**
     * @notice Total amount of vested tokens at the provided timestamp.
     *   This number also includes vested tokens which have been claimed.
     * @dev `timestamp` MAY be both in the future and in the past.
     * Zero MUST be returned if the timestamp is before the token was minted.
     * @param tokenId The NFT token id
     * @param timestamp The timestamp to check on, can be both in the past and the future
     * @return payout Total amount of tokens which have been vested at the provided timestamp
     */
    function vestedPayoutAtTime(uint256 tokenId, uint256 timestamp) external view returns (uint256 payout);

    /**
     * @notice Number of tokens for an NFT which are currently vesting (locked).
     * @dev The sum of vestedPayout and vestingPayout SHOULD always be the total payout.
     * @param tokenId The NFT token id
     * @return payout The number of tokens for the NFT which have not been claimed yet,
     *   regardless of whether they are ready to claim
     */
    function vestingPayout(uint256 tokenId) external view returns (uint256 payout);

    /**
     * @notice Number of tokens for the NFT which can be claimed at the current timestamp
     * @dev It is RECOMMENDED that this is calculated as the `vestedPayout()` value with the total
     * amount of tokens claimed subtracted.
     * @param tokenId The NFT token id
     * @return payout The number of vested tokens for the NFT which have not been claimed yet
     */
    function claimablePayout(uint256 tokenId) external view returns (uint256 payout);

    /**
     * @notice The start and end timestamps for the vesting of the provided NFT
     * MUST return the timestamp where no further increase in vestedPayout occurs for `vestingEnd`.
     * @param tokenId The NFT token id
     * @return vestingStart The beginning of the vesting as a unix timestamp
     * @return vestingEnd The ending of the vesting as a unix timestamp
     */
    function vestingPeriod(uint256 tokenId) external view returns (uint256 vestingStart, uint256 vestingEnd);

    /**
     * @notice Token which is used to pay out the vesting claims
     * @param tokenId The NFT token id
     * @return token The token which is used to pay out the vesting claims
     */
    function payoutToken(uint256 tokenId) external view returns (address token);
}
```

## Rationale

**vesting terms**

- vesting: Tokens which are locked until a future date
- vested: Tokens which have reached their unlock date. (The usage in this specification relates to the total vested tokens for a given Vesting NFT.)
- claimable: Amount of tokens which can be claimed at the current timestamp.
- timestamp: The unix timestamp (seconds) representation of dates used for vesting.

**vesting functions**

- vestingPayout() and vestedPayout() add up to the total number of tokens which can be claimed by the end of of the vesting schedule, which is also equal to vestedPayoutAtTime() with type(uint256).max as the timestamp.
- vestedPayout() will provide the total amount of tokens which are eligible for release (including claimed tokens), while claimablePayout() provides the amount of tokens which can be claimed at the current timestamp.
- vestedPayoutAtTime() provides functionality to iterate through the vestingPeriod() and provide a visual of the release curve. This allows for tools to iterate through a vesting schedule and create a visualization using on-chain data. It would be incredible to see integrations such as hot-chain-svg to be able to create SVG visuals of vesting curves directly on-chain.

**timestamps**

Generally in Solidity development it is advised against using `block.timestamp` as a state dependant variable as the timestamp of a block can be manipulated by a miner. The choice to use a `timestamp` over a `block` is to allow the interface to work across multiple **Ethereum Virtual Machine** (EVM) compatible networks which generally have different block times. Block proposal with a significantly fabricated timestamp will generally be dropped by all node implementations which makes the window for abuse negligible.

The `timestamp` makes cross chain integration easy, but internally, the reference implementation keeps track of the token payout per Vesting NFT to ensure that excess tokens alloted by the vesting terms cannot be claimed.

## Backwards Compatibility

- The Vesting NFT standard is meant to be fully backwards compatible with any current EIP-721 standard integrations and marketplaces.
- The Vesting NFT standard also supports EIP-165 standard interface detection for detecting EIP-721 compatibility, as well as Vesting NFT compatibility.

## Test Cases

The reference vesting NFT repository includes tests written in Hardhat.

## Reference Implementation

A reference implementation of this EIP can be found in [this repository](https://github.com/ApeSwapFinance/eip-5725-vesting-nft-implementation).

## Security Considerations

**timestamps**

- Vesting schedules are based on timestamps. As such, it’s important to keep track of the number of tokens which have been claimed and to not give out more tokens than alloted for a specific Vesting NFT.

vestedPayoutAtTime(tokenId, type(uint256).max), for example, must return the total payout for a given tokenId

**approvals**

- When an approval is made on a Vesting NFT, the operator would have the rights to transfer the Vesting NFT to themselves and then claim the vested tokens.

## Extensions

- Vesting Curves
- Rental
- Beneficiary

## References

Standards

- EIP-20 Token Standard.
- EIP-165 Standard Interface Detection.
- EIP-721 Token Standard.
- Timestamp Dependence The 15-second Rule.
- hot-chain-svg On-chain SVG generator. Could be used to generate vesting curves for Vesting NFTs on-chain.

## Copyright

Copyright and related rights waived via CC0.

## Citation

Please cite this document as:

Apeguru(@Apegurus), Marco, Mario, DeFiFoFum, “EIP-5725: Vesting NFT,” Ethereum Improvement Proposals, no. XXXX, September 2022. [Online serial]. Available: https://eips.ethereum.org/EIPS/eip-XXXX.

## Replies

**SamWilsn** (2022-10-04):

I’m a little worried that `vestedPayoutAtTime` might be difficult/expensive to compute. Is that a reasonable concern?

---

**Apeguru** (2022-10-05):

That is indeed a reasonable concern, nevertheless it will depend a lot on the business logic behind the vesting scheme. As you can see in the reference implementations:

`https://github.com/ethereum/EIPs/pull/5725/files#diff-a4572304a6a812f0520147259c19c757cc16801c1db9bced504544d54b6afa37R79`

`https://github.com/ethereum/EIPs/pull/5725/files#diff-a4572304a6a812f0520147259c19c757cc16801c1db9bced504544d54b6afa37R79`

The computation required to calculate them is trivial.

---

**pxrv** (2022-10-05):

Are there any current projects that could benefit from this standardisation or is this just a nice-to-have?

---

**OxMarco** (2022-10-16):

Basically any VC or community-backed protocol that needs to distribute vested tokens at the token generation event.

---

**DeFiFoFum** (2022-10-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/apeguru/48/7323_2.png) Apeguru:

> Add EIP-5725: Transferable Vesting NFT by Apegurus · Pull Request #5725 · ethereum/EIPs · GitHub

As far as gas is concerned, as long as `VestingNFT.vestedPayoutAtTime()` uses a direct formula to calculate the payout (as in the reference implementation) the gas estimation comes out to around 85k for `VestingNFT.claim()` which calls `vestedPayoutAtTime` within the function. The estimator is calculating 46k just for an ERC-20 approval.

Considering `VestingNFT.claim()` also includes a transfer, I would not consider the gas expensive. It’s comparable to calculating the value of a swap using a constant product function.

Of course, this depends on how the implementation is written. If it requires a `for` loop to calculate then I would start to get VERY concerned about gas.

[![vesting-nft-gas](https://ethereum-magicians.org/uploads/default/optimized/2X/e/e76ec3357737ad5203d6ee7de77b96efb2eb4702_2_690x321.jpeg)vesting-nft-gas1522×710 191 KB](https://ethereum-magicians.org/uploads/default/e76ec3357737ad5203d6ee7de77b96efb2eb4702)

---

**SamWilsn** (2022-10-18):

That sounds reasonable! I was just concerned that requiring the function in the interface might make it impractical for some vesting schemes because of gas. As long as you’re okay with that risk, I have no objections.

---

**SamWilsn** (2022-11-25):

We’re trying a new process where we get a volunteer peer reviewer to read through your proposal and post any feedback here. Your peer reviewer is [@drgorilla.eth](/u/drgorilla.eth)!

If any of this EIP’s authors would like to participate in the volunteer peer review process, [shoot me a message](https://ethereum-magicians.org/new-message?username=SamWilsn&title=Peer+Review+Volunteer)!

---

[@drgorilla.eth](/u/drgorilla.eth) please take a look through [EIP-5725](https://eips.ethereum.org/EIPS/eip-5725) and comment here with any feedback or questions. Thanks!

---

**drgorilla.eth** (2022-11-26):

Heya!

Will edit/add as I go, sorry if it’s a bit of a mess at first’![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

- Timestamp dependency: since the merge, ethereum uses the beaconchain slots which are 12 seconds long. Block.timestamp is constrained and doesn’t rely on a third-party/miner anymore (worst that can happen is a slot without a block, ie a 12 second delay).
consensus-specs/beacon-chain.md at v0.10.0 · ethereum/consensus-specs · GitHub
- What if a vesting should remain associated to a given eoa/non-transferability? I guess a mapping initialized in createVesting() (or similar function) is the easiest

Style/nit:

```auto
    event PayoutClaimed(uint256 indexed tokenId, address indexed recipient, uint256 _claimAmount);
```

why the underscore only in _claimAmount?

Iic, _ for the args and no underscore for the returned values (see EIP-20 for instance [EIP-20: Token Standard](https://eips.ethereum.org/EIPS/eip-20#specification))

---

**Apeguru** (2022-12-22):

Hey! Thanks a lot for reviewing and working with us to push this forward ![:grin:](https://ethereum-magicians.org/images/emoji/twitter/grin.png?v=12)

- Unsure if there is anything to address on your first comment regarding timestamp. Let me know if I am missing something
- Same on second comment

**Syle**

Good catch! We will address it as soon as the review is finalized. Is there anything else you think we should be looking for?

---

**Apeguru** (2022-12-22):

Thank you and [@drgorilla.eth](/u/drgorilla.eth)!

Please let us know what can we do to move this into the next stage

---

**SamWilsn** (2022-12-22):

Once you’re reasonably happy with your draft, you can make a PR to move it to `Review`. Once in review, try and get buy-in from relevant people/organizations. One of the best things you can do is get a third party interested enough to try and implement their own version of the standard.

After all that, you can open a PR to move the proposal into `Last Call`, and finally `Final`.

---

**Apeguru** (2023-01-09):

Thanks a lot for sharing this! We will keep it in mind.

I hope you are having a great start of 2023 ![:smiling_face_with_three_hearts:](https://ethereum-magicians.org/images/emoji/twitter/smiling_face_with_three_hearts.png?v=12)

---

**DeFiFoFum** (2023-01-13):

After messing around with the standard some more by integrating it into a Treasury Bills product, these would be my questions about updates to `IERC5725`.

Technically all of these can be derived, but I’m curious if others feel they should be included.

If they are not included, another approach would be to create `IERC5725` Extensions similar to `[IERC20Metadata](https://docs.openzeppelin.com/contracts/4.x/api/token/erc20#IERC20Metadata)`.

1. Should we add vestingPayoutAtTime?

```plaintext
/// @notice Amount of tokens vesting/locked in Bill at the timestamp provided.
function vestingPayoutAtTime(uint256 tokenId, uint256 timestamp) external view returns (uint256 payout);
```

OR refactor `vestedPayoutAtTime` →  `payoutsAtTime`

```plaintext
/// @notice Find the different payout amounts for a Bill a the timestamp provided.
function payoutsAtTime(uint256 tokenId, uint256 timestamp) external view returns (uint256 vestedPayout, uint256 vestingPayout, uint256 claimablePayout);
```

1. A function which shows how much time left until vesting ends could be helpful?

```plaintext
/// @notice Returns the remaining vesting in seconds of the `tokenId` until the `vestingEnd` timestamp.
function pendingVesting(uint256 tokenId) external view returns (uint256 pendingSeconds);
```

1. A function which shows the total tokens left to be claimed

```plaintext
/// @notice Returns the total payout held for the given Bill ID. i.e.: `vestingPayout` + `claimablePayout`
function pendingPayout(uint256 tokenId) external view returns (uint256 payout);
```

January 13, 2023

---

**boyuanx** (2023-01-29):

Hey, first of all this is a very cool EIP and we are interested in performing a prototype implementation in our upcoming product (EthSign TokenTable). I have a question: in the EIP, it’s mentioned that “this standard also allows for a variety of different vesting curves to be implement easily”. However, I see no mention of any curves in the actual interface functions, which makes this sentence a little confusing. ~~Do you think we should incorporate a generic quadratic formula and 1D cubic equation as a basis for all curves? Or is that a tad too specific? But I think the two formulas mentioned above pretty much covers all possible curves.~~

---

**boyuanx** (2023-01-29):

Also, not to be pedantic, but I believe there is a significant difference between vesting and unlocking, and what’s being described in this EIP is actually unlocking instead of vesting. Vesting is the act of releasing tokens into an unlocking pool for the recipient, and unlocking is the act of releasing tokens in said pool to the recipient, and they can happen at different rates (obviously vesting must happen first, otherwise there is nothing to unlock).

---

**Apeguru** (2023-02-02):

Hello good ape!

As no one has shared opinions so far I will share mine:

I am of a school of keeping everything as simple as possible. As you noted all of this information can be easily derived from already existing methods, hence why I would advice against adding this functionality into the core standard.

If needed it can be added as an extension as you mention.

---

**Apeguru** (2023-02-02):

Hey!

I am glad you are looking forward on working on this. Feel free to reach out to further discuss.

In terms of what you bring up in regards of the curves being present in the implementation:

This is meant to be a standard interface to create token-lock and vesting contracts that are represented with NFTs. The goal of it is to keep it as flexible and adaptable as possible, hence why there isn’t any specific vesting curve or approach included directly in the standard. The specific curves are purposely left out of the standard, so to allow maximum flexibility, as it is expected to be implemented by each specific use case or developer.

If you want to further see how different vesting curves interact and integrate with the standard I suggest you look into the example implemetation:



      [github.com](https://github.com/ethereum/EIPs/blob/master/assets/eip-5725/README.md)





####



```md
# EIP-5725: Transferrable Vesting NFT - Reference Implementation
This repository serves as a reference implementation for **EIP-5725 Transferrable Vesting NFT Standard**. A Non-Fungible Token (NFT) standard used to vest tokens (ERC-20 or otherwise) over a vesting release curve.

## Contents
- [EIP-5725 Specification](./contracts/IERC5725.sol): Interface and definitions for the EIP-5725 specification.
- [ERC-5725 Implementation (abstract)](./contracts/ERC5725.sol): ERC-5725 contract which can be extended to implement the specification.
- [VestingNFT Implementation](./contracts/reference/LinearVestingNFT.sol): Full ERC-5725 implementation using cliff vesting curve.
- [LinearVestingNFT Implementation](./contracts/reference/VestingNFT.sol): Full ERC-5725 implementation using linear vesting curve.
```










Here you can find a linear vesting curve and non-linear examples.

---

**Apeguru** (2023-02-02):

Thanks a lot for the lesson, appreciated!

We can say this standard helps for both. Releasing the tokens over time and unlocking them, though when I put it like this it even sounds like the same! ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12)

---

**boyuanx** (2023-02-06):

Apologies for the unclear explanation, differentiating vesting vs. unlocking is mainly important in the context of Restricted Stock Units. In the traditional world, unlocking is called distributing.

From [Fidelity](https://www.fidelity.com/webcontent/ap002390-mlo-content/19.09/help/learn_rsus.shtml#whenvest):

---

## When do RSUs vest?

Depending on your company’s plan rules, vesting requirements may be met by the passage of time, or by company or individual performance. If you do not meet the requirements set forth by your company prior to the end of the vesting period, your units are typically forfeited to the company. Vesting may occur prior to the vesting date shown, contingent upon your company’s satisfaction with your compliance with the company’s performance criteria set forth in your company’s plan rules.

## What is a distribution schedule?

A distribution schedule is the schedule for actual payment to you under your company’s plan.

## What happens to my restricted stock units once they vest?

Once your restricted stock units vest, your rights become non-forfeitable. You will receive actual payment according to the distribution schedule under your company’s plan. If you have not elected to defer distribution, the distribution date and the vesting date are the same.

---

From the above, we can clearly see how vested RSUs don’t immediately become available all at once to the employee, it just means the employer can no longer take them away. Instead, another distribution schedule must be followed for employees to actually receive those stock units. In the context of tokens, vested tokens don’t necessarily mean they are immediately claimable by the stakeholder. The act of tokens actually being claimed by the stakeholder is an act of distribution (unlocking), not vesting.

Hope this helped clarify things more! Very few web3 entities properly distinguish vesting and unlocking. I think we can include this differentiation in the standard.

---

**Apeguru** (2023-02-06):

Thanks a lot you really went a long way to make your point!

For this particular thread and the scope of the Ethereum improvement proposal, we refer to vesting using the general definition and understanding within the Web3 and crypto ecosystem.

Let me help you out with some context on how vesting is used in the industry that pertains us:

https://medium.com/coinmonks/token-vesting-the-complete-guide-to-creating-vesting-in-tokenomics-bf211b999f2f



      [Ekotek](https://ekotek.vn/vesting-can-be-confusing-here-is-a-thorough-explanation)



    ![](https://ethereum-magicians.org/uploads/default/original/2X/c/c8539b5825839f364fbbde0b36a01c73b102ada2.webp)

###



The building of each blockchain project requires fundraising to ensure that it survives buoyantly after it has been launched. On this note, token vesting is not only […]











      ![](https://eqvista.com/wp-content/favicons/favicon-96x96.png)

      [Eqvista](https://eqvista.com/company-valuation/valuation-crypto-assets/token-vesting/)



    ![](https://eqvista.com/wp-content/uploads/2022/09/Create-token-vesting-schedule-efficiently-with-vesting-platforms.png)

###



There are two approaches to implementing token vesting- automatically or manually. Learn more about each token vesting process here.



    Est. reading time: 10 minutes











These are some industry specific articles that refer to vesting as **the process of locking and distributing purchased tokens within a given timeframe** which is the same definition we are using here and pretty much the one whole industry uses.

Lucky for us this standard doesn’t intend to address Restricted Stock Units, neither it pertains the ‘traditional world’ of finance. I still appreciate the lesson, cheers!


*(8 more replies not shown)*
