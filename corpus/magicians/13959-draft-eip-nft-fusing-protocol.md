---
source: magicians
topic_id: 13959
title: "Draft EIP: NFT Fusing Protocol"
author: saitama2009
date: "2023-04-24"
category: EIPs
tags: [erc, nft, erc-721, erc1155]
url: https://ethereum-magicians.org/t/draft-eip-nft-fusing-protocol/13959
views: 1647
likes: 11
posts_count: 9
---

# Draft EIP: NFT Fusing Protocol

## Abstract

This standard extends the [ERC-721](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-721.md) standard, enabling users to fuse two or more NFTs to create a new NFT with customized combination rules. This proposal aims to provide a more interactive and dynamic approach to NFT creation, unlocking new possibilities for NFT use cases and increasing their utility within the Ethereum ecosystem.

## Motivation

The current NFT ecosystem lacks a standardized approach to combine multiple NFTs into a new one. While some projects have implemented custom solutions, these are often ad hoc and project-specific, limiting their interoperability with other NFTs and platforms. This standard aims to create a standardized method for fusing NFTs, enabling users to create new NFTs by combining existing ones according to customizable combination rules. This will foster more incredible innovation and creativity within the NFT space and create new possibilities for NFT use cases.

## Specification

The keywords “MUST,” “MUST NOT,” “REQUIRED,” “SHALL,” “SHALL NOT,” “SHOULD,” “SHOULD NOT,” “RECOMMENDED,” “MAY,” and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

**Interface**

The following interface extends the existing ERC-721 standard:

```solidity
// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.10;

interface IERC6927 {
    // Events

    /// @dev Emits when a combo is minted.
    /// @param owner The owner address of the newly minted combo
    /// @param comboId The newly minted combo identifier
    event ComboMinted(address indexed owner, uint256 indexed comboId);

    /// @dev Emits when a combo is dismantled.
    /// @param owner The owner address of the combo
    /// @param comboId The dismantled combo identifier
    event ComboDismantled(address indexed owner, uint256 indexed comboId);

    /// @dev Emits when an owner approves another address
    /// @param spender The approved address
    /// @param tokenOwner tokenOwner The NFT's owner
    /// @param tokenAddresses The NFT's collection addresses
    /// @param tokenIds The NFT identifiers
    /// @param allowances The allowed number of uses
    event ComboApproval(
        address indexed spender,
        address indexed tokenOwner,
        address[] tokenAddresses,
        uint256[] tokenIds,
        uint256[] allowances
    );

    // Structs

    /// @dev A ComboFactor defines the requirements for NFTs from a specific collection
    /// to participate in the combo and the rules that apply.
    /// A customized combination rule consists of several ComboFactors.
    /// @param collectionAddress The NFT collection address
    /// @param minRequired Minimum number of NFTs required from the collection
    /// @param maxAllowed Maximum number of NFTs allowed from the collection
    /// @param lockTokens Indicates if tokens from the collection will be locked when minting a combo
    /// @param maxReuseCount Maximum total reuse count of a token from the collection in
    /// this combo collection (only applicable for ERC-721 and when lockTokens is false)
    struct ComboFactor {
        address collectionAddress;
        uint64 minRequired;
        uint64 maxAllowed;
        bool lockTokens;
        uint64 maxReuseCount;
    }

    /// @param tokenAddress The NFT's collection address
    /// @param tokenId The NFT identifier
    /// @param amount The number of NFTs with `tokenId` used
    struct Ingredient {
        address tokenAddress;
        uint256 tokenId;
        uint256 amount;
    }

    // Functions

    /// @dev Mints a combo using the provided NFTs as ingredients.
    /// If a combo rule specifies an NFT to be locked, it will be locked within the combo.
    /// For unlocked NFTs, their reuse count will be reduced accordingly.
    /// @param ingredients The NFTs used to mint a combo
    /// @param hash The hash representing user-specific adjustments or
    /// operations applied to the final NFT's visual appearance when fusing NFTs. This
    /// value provides additional information about the unique combination of NFTs.
    function mint(
        Ingredient[] calldata ingredients,
        string calldata hash
    ) external;

    /// @dev Dismantles a combo, returning locked NFTs to the current owner of the combo,
    /// and restoring the reuse count of the participating but unlocked NFTs.
    function dismantle(uint256 comboId) external;

    /// @dev Retrieve the combo rule.
    function getComboRule() external view returns (ComboFactor[] memory);

    /// @dev Retrieve a combo's ingredients.
    function getIngredients(
        uint256 comboId
    ) external view returns (Ingredient[] memory);

    /// @dev Approves `spender` to use `msg.sender`'s NFTs when minting a combo.
    /// The approval allows the spender to use the specified NFTs within their allowance limits.
    /// Only ERC-721 NFTs are approvable.
    /// @param tokenAddresses The NFT's collection addresses
    /// @param tokenIds The NFT identifiers
    /// @param allowances The maximum number of uses
    function approveCombo(
        address spender,
        address[] calldata tokenAddresses,
        uint256[] calldata tokenIds,
        uint256[] calldata allowances
    ) external;
}
```

## Rationale

Firstly, the process of fusing existing NFTs to create new ones is highly diverse. The current NFT trading market uses a price discovery mechanism dominated by collection floor prices. To facilitate price discovery, it is essential to assign new NFTs created with different combination rules to separate collections. Therefore, we have extended the ERC-721 to support various combination rules.

Secondly, the potential for customizable combination rules is immense, and maintaining simplicity and flexibility is a fundamental principle. Given the current NFT trading market’s price discovery mechanism, which is dominated by collection floor prices, we have positioned the collection as the basic unit of combination factors. Both ERC-721 and [ERC-1155](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1155.md) are supported as combination factors. To avoid over-design, we have added only the most necessary parameters for each combination factor, such as upper and lower bounds and lock settings. Moreover, to prevent users from repeatedly creating combos using the same NFT without locking and destroying the scarcity of new assets, we have added usage limits for NFTs that do not require locking in the combination.

Lastly, fusing NFTs results in an internal structure within combos. These ingredients are distinct from metadata that cannot be read by smart contracts. They can be read by other smart contracts and used in more native on-chain application scenarios, such as smart airdrops and raffles based on different ingredients of combos.

## Backwards Compatibility

This proposal is fully backwards compatible with the existing ERC-721 standard, extending the standard with new functions that do not affect the core functionality.

## Test Cases

Test cases should be developed to cover the following scenarios:

- Minting a valid combo with ERC-721 and/or ERC-1155 NFTs.
- Dismantling a combo and returning locked NFTs to their owners.
- Setting combo rules and ensuring compliance during the minting - - process.
- Approving ERC-721 NFTs for use in combos.
- Querying combo rules and ingredients.

## Reference Implementation

An implementation of this EIP will be provided upon acceptance of the proposal.

## Security Considerations

This standard introduces some potential security considerations that must be addressed. These include:

- Ownership and permissions: It is crucial to ensure that only the rightful owner of the NFTs can initiate the fusing process. Proper access control and authentication mechanisms must be in place to prevent unauthorized users from fusing tokens they do not own.
- Reentrancy attacks: The fusing process may involve multiple calls to external contracts, potentially leading to reentrancy attacks. Proper security measures, such as reentrancy guards or the Checks-Effects-Interactions pattern, can help mitigate this risk.
- Gas consumption: The fusing process may involve complex computations and multiple contract interactions, leading to potentially high gas costs. Optimizing the fusing process to minimize gas consumption will be essential for ensuring usability and cost-effectiveness.

## Copyright

Copyright and related rights waived via [CC0](https://github.com/ethereum/EIPs/blob/master/LICENSE.md).

Link to the EIP:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/6927)














####


      `master` ← `saitama2009:draft_nft_fusing_standard`




          opened 04:57PM - 24 Apr 23 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/7/7ad5c8981125264d9145cda3929a862d168f561f.png)
            saitama2009](https://github.com/saitama2009)



          [+166
            -0](https://github.com/ethereum/EIPs/pull/6927/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/EIPs/pull/6927)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

## Replies

**stoicdev0** (2023-05-03):

I feel this can be done with [ERC-6220: Composable NFTs utilizing Equippable Parts](https://eips.ethereum.org/EIPS/eip-6220).

We used an equipping approach so these are some equivalents:

- instead of mint / dismantle we have equip / unequip
- instead of getIngredients we have getEquipment
- Rules (ComboFactor and Ingredient) are specified in a Catalog contract as Parts, so they can be reused across different collections. We do not include amount however, and it’s actually weird for me that you specify them on the Ingridient, together with tokenAddress and tokenId, since there can only be 1 of each.
- Approvals are simply the same as in 721s, they work from the parent token.

Some advantages of our approach:

- Reusable rules across collections. They are also very flexible.
- Each equipment is independent, in this proposal it seems like it’s all or nothing. Although it might be a desired feature for you.
- Parent tokens can continue to be used they just have more value/functionality on them.
- On the catalog, besides parts that can be equipped we also define reusable parts. This is very useful for collections which reuse traits among NFTs with different combinations.

Let me know if it helps!

---

**ComboWizard** (2023-05-04):

Hey [@stoicdev0](/u/stoicdev0), as fellow builders of NFT 2.0, we are delighted to see your question, which will inspire us to think more deeply about NFT composability.

From our current understanding of EIP-6220, we believe the biggest difference between our EIP-6927 and EIP-6220 in terms of design is that the target scenario for EIP-6220 is more like character upgrades, where a core NFT is gradually assembled by equipping and unequipping other NFTs over time, constantly changing. In contrast, our goal with EIP-6927 is more like a collectible challenge, where users select NFTs that meet the requirements of a combination rule and combine them in one go.

The NFT combination in EIP-6220 mainly happens after the creation of new NFTs. However, the NFT combination in EIP-6927 mainly occurs during the creation of new NFTs. For example, in StepN, the combination gameplay of embedding gems into sneakers is more suitable for EIP-6220, while the combination gameplay of fusing two sneakers to create a new sneaker is more suitable for EIP-6927.

Due to the differences in target scenarios, we have different design directions. In EIP-6927, not all NFTs participating in the combination need to be embedded into the new NFT. For example, in the scenario where a BAYC and a Mutant Serum are combined to create a MAYC, BAYC holders only need to prove they own a BAYC without embedding it into the final MAYC. Therefore, we do not rely on EIP-6059.

The scenarios for NFT 2.0 are diverse, and we believe we all want to create a highly extensible protocol. We are more than willing to collaborate with you to bring such a protocol to life and look forward to further communication.

---

**SamWilsn** (2023-09-20):

Hey! I have a couple non-editorial related comments. Please note that these should be answered in the EIP itself (though feel free to discuss here too.)

- Is comboId also a valid ERC-721 tokenId?
- Who is meant to implement IERC6927? Is it the token contract that wants to support fusing? Can you fuse tokens from arbitrary smart contracts?
- Does the fuse contract need to take ownership of the ingredient tokens?
- I find using mint to fuse tokens somewhat confusing. Would it make sense to use fuse as the function name instead?
- I think approveCombo deserves a bit more explanation.
- Would it make sense to reserve zero maxAllowed as unlimited?

---

**Mani-T** (2023-09-21):

This has the potential to bring more dynamism and innovation to the NFT space. It ensures interoperability with existing NFTs and platforms.  This is essential for the broader adoption of such features.

---

**saitama2009** (2023-11-01):

Sorry for the delay!

- The comboId is actually an ERC-721 tokenId, no difference.
- The token contract need to implement IERC6927! The current design supports fusing all tokens from ERC-721 and ERC-1155.
- It’s not necessary, we can create an escrow contract to do that.
- We’ll take that suggestion under advisement.
- Okay, more detailed explanations will be added.
- Yes!

---

**joeysantoro** (2023-11-13):

I love the direction of this EIP. My main suggestion is to remove the concept of a comboRule entirely in favor of leaving that logic fully up to the implementers to add the most flexibility and composability. In summary I would:

- renaming mint to fuse as Sam suggested above
- having the Ingredient struct use arrays for tokenId and amount to save potentially needing to iterate over the same collection multiple times.
- adding the desired comboId as a parameter to fuse
- inverting the relationship of getIngredients (which could have an arbitrary output set and conflict errors) and instead have canFuse(uint outputComboId, Ingredient[] memory) returns (bool) which would effectively introspect whether the corresponding fuse call would succeed or not. This could even be dual purpose and work for unfuse as well
- rename dismantle to unfuse or defuse also take a desired ingredient output list
- removing combo rule and comboFactor entirely

This approach has advantages of composability and flexibility by not requiring any special relationships of the source nfts and letting the fuse nft use any logic it wants

You could have the ComboFactor be an out of the box implementation or extended standard as well.

---

**ComboWizard** (2023-11-14):

[@SamWilsn](/u/samwilsn) what do you think about [@joeysantoro](/u/joeysantoro)’s idea?

---

**SamWilsn** (2023-11-16):

I can only say that Joey’s suggestions *sound* reasonable. I don’t really have a deep understanding of the problem space, so I can’t offer more in-depth critique ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)

