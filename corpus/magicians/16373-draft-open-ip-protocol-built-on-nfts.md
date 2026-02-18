---
source: magicians
topic_id: 16373
title: Draft:Open IP Protocol built on NFTs
author: saitama2009
date: "2023-10-31"
category: EIPs
tags: [erc, nft, erc-721, erc1155]
url: https://ethereum-magicians.org/t/draft-open-ip-protocol-built-on-nfts/16373
views: 1917
likes: 1
posts_count: 4
---

# Draft:Open IP Protocol built on NFTs

A protocol that enables users to remix NFTs and generate new NFT derivative works, while their relationships can be traced on chain.

## Abstract

This proposal aims to establish a standardized method for creating new intellectual properties (IPs) by remixing multiple existing IPs in a decentralized manner.

The protocol is built on the foundation of NFTs (Non-Fungible Tokens). Within this protocol, each intellectual property is represented as an NFT. It extends the ERC-721 standard, enabling users to generate a new NFT by remixing multiple existing NFTs. To ensure transparency and traceability in the creation process, the relationships between the new NFT and the original NFTs are recorded on the blockchain and made publicly accessible.

Furthermore, to enhance the liquidity of IP, users not only have the ability to remix NFTs they own but can also grant permission to others to participate in the creation of new NFTs using their own NFTs.

## Motivation

The internet is flooded with fresh content every day, but with the traditional IP infrastructure, IP registration and licensing is a headache for digital creators. The rapid creation of content has eclipsed the slower pace of IP registration, leaving much of this content unprotected. This means digital creators can’t fairly earn from their work’s spread.

|  | Traditional IP Infrastructure | Open IP Infrastructure |
| --- | --- | --- |
| IP Registration | Long waits, heaps of paperwork, and tedious back-and-forths. | An NFT represents intellectual property; the owner of the NFT holds the rights to the IP. |
| IP Licensing | Lengthy discussions, legal jargon, and case-by-case agreements. | A one-stop global IP licensing market that supports various licensing agreements. |

With this backdrop, we’re passionate about building an Open IP ecosystem tailored for today’s digital creators. Here, with just a few clicks, creators can register, license, and monetize their content globally, without geographical or linguistic barriers.

## Specification

The keywords “MUST,” “MUST NOT,” “REQUIRED,” “SHALL,” “SHALL NOT,” “SHOULD,” “SHOULD NOT,” “RECOMMENDED,” “MAY,” and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

**Interface**

This protocol standardizes how to remix multiple existing NFTs and create a new NFT derivative work (known as a combo), while their relationships can be traced on the blockchain. It contains three core modules, remix module, network module, and license module.

### Remix Module

This module extends ERC-721 standard and enables users to create a new NFT by remixing multiple existing NFTs, whether they’re ERC-721 or ERC-1155.

```solidity
// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.10;

interface IERC721X {
    // Events

    /// @dev Emits when a combo is minted.
    /// @param owner The owner address of the newly minted combo
    /// @param comboId The newly minted combo identifier
    event ComboMinted(address indexed owner, uint256 indexed comboId);

    // Structs

    /// @param tokenAddress The NFT's collection address
    /// @param tokenId The NFT identifier
    struct Token {
        address tokenAddress;
        uint256 tokenId;
    }

    /// @param amount The number of NFTs used
    /// @param licenseId Which license to be used to verify this component
    struct Component {
        Token token;
        uint256 amount;
        uint256 licenseId;
    }

    // Functions

    /// @dev Mints a NFT by remixing multiple existing NFTs.
    /// @param components The NFTs remixed to mint a combo
    /// @param hash The hash representing the algorithm about how to generate the combo's metadata when remixing multiple existing NFTs.
    function mint(
        Component[] calldata components,
        string calldata hash
    ) external;

    /// @dev Retrieve a combo's components.
    function getComponents(
        uint256 comboId
    ) external view returns (Component[] memory);
}
```

### License Module

By default, users can only remix multiple NFTs they own to create new NFT derivative works. This module enables NFT holders to grant others permission to use their NFTs in the remixing process.

```solidity
// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.10;

import "./IERC721X.sol";

interface ILicense {
    /// @dev Verify the permission when minting a combo
    /// @param user The minter
    /// @param combo The new NFT to be minted by remixing multiple existing NFTs
    /// @return components The multiple existing NFTs used to mint the new combo
    function verify(
        address user,
        IERC721X.Token calldata combo,
        IERC721X.Component[] calldata components
    ) external returns (bool);
}
```

### Network Module

This module follows the singleton pattern and is used to track all relationships between the original NFTs and their NFT derivative works.

```solidity
// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.10;

import "./IERC721X.sol";

interface INFTNetIndexer {
    /// @dev Verify if the `child` was created by remixing the `parent` with other NFTs.
    /// @param parent Any NFT
    /// @param child Any NFT
    function isParent(
        IERC721X.Token calldata parent,
        IERC721X.Token calldata child
    ) external view returns (bool);

    /// @dev Verify if `a` and `b` have common `parent`s
    /// @param a Any NFT
    /// @param b Any NFT
    function isSibling(
        IERC721X.Token calldata a,
        IERC721X.Token calldata b
    ) external view returns (bool, IERC721X.Token[] memory commonParents);

    /// @dev Return all parents of a `token`
    /// @param token Any NFT
    /// @return parents All NFTs used to mint the `token`
    function getParents(
        IERC721X.Token calldata token
    ) external view returns (IERC721X.Token[] memory parents);
}
```

## Rationale

The Open IP Protocol is built on the “1 premise, 2 extensions, 1 constant” principle.

The “1 premise” means that for any IP in the Open IP ecosystem, an NFT stands for that IP. So, if you have the NFT, you own the IP. That’s why the Open IP Protocol is designed as an extended protocol compatible with ERC-721.

The “2 extensions” refer to the diversification of IP licensing and remixing.

- IP licensing methods are diverse. For example, delegating an NFT to someone else is one type of licensing, setting a price for the number of usage rights is another type of licensing, and even pricing based on auction, AMM, or other pricing mechanisms can develop different licensing methods. Therefore, the license module is designed allowing various custom licensing methods.
- IP remixing rules are also diverse. When remixing multiple existing NFTs, whether to support ERC-1155, whether to limit the range of NFT selection, and whether the NFT is consumed after remixing, there is no standard. So, the remix module is designed to support custom remixing rules.

The “1 constant” refers to the fact that the traceability information of IP licensing is always public and unchangeable. Regardless of how users license or remix IPs, the relationship between the original and new IPs remains consistent. Moreover, if all IP relationships are recorded in the same database, it would create a vast IP network. If other social or gaming dApps leverage this network, it can lead to entirely novel user experiences. Hence, this protocol’s network module is designed as a singleton.

## Backwards Compatibility

This proposal is fully backwards compatible with the existing ERC-721 standard, extending the standard with new functions that do not affect the core functionality.

## Reference Implementation

An implementation of this EIP will be provided upon acceptance of the proposal.

## Security Considerations

This standard highlights several security concerns that need attention:

- Ownership and Permissions: Only the NFT owner or those granted by them should be allowed to remix NFTs into NFT derivative works. It’s vital to have strict access controls to prevent unauthorized creations.
- Reentrancy Risks: Creating derivative works might require interacting with multiple external contracts, like the remix, license, and network modules. This could open the door to reentrancy attacks, so protective measures are necessary.
- Gas Usage: Remixing NFTs can be computation-heavy and involve many contract interactions, which might result in high gas fees. It’s important to optimize these processes to keep costs down and maintain user-friendliness.

## Copyright

Copyright and related rights waived via CC0.

Link to the PR:

https://github.com/ethereum/ERCs/pull/77

## Replies

**saitama2009** (2023-11-30):

[@SamWilsn](/u/samwilsn) please have a review of the updated proposal if it’s convenient, thanks

---

**SamWilsn** (2023-12-05):

A non-editorial comment:

> if you have the NFT, you own the IP

 This relies on a lot more than just some interfaces on the blockchain. You probably also need some kind of legal license from the creator for this, right? Should this standard have a function for getting a link to that license?

---

**drllau** (2024-01-09):

As someone who specialises in IP/IT/ID law, [@SamWilsn](/u/samwilsn) is correct … some legal nuances for those who don’t want to waste 4+ years in grad school

1. possession != copyright holder … Copyright Law (mickey-mouse extensions aside) is what we om legal profession call choses-in-action, or use-rights enforceable by court which in the case of copyright is the ability to modify, transfer, publish etc any fixed work … whereas an NFT is a little closer to choses-in-possession, if you control the secret key, you can at least VIEW the data. But only the copyright holder can issue and modify the work which is why Hollywood considers all the subcontractor as work4hire and not authors.
2. grant (of usage) != power (to sublicense) licensing is a very nuanced topic … the simplest approach is the CreativeCommons where you have to expressly designate your work as able to be derivative, but once you have other restrictions like co-authorship, sufficiently transformative (and mirror image of a bored ape doesn’t meet that threshold) and fair use/dealings/exemptions and relicenseable all add to the complexity (not to mention non-commercial as that is rather vague).
3. link != legal privilege NFts are basically pointers … whereas if you want a auto-bargaining platform to negotiate rights, then firstly you have to implement the metadata (see the creative commons example), then correctly implement the technology protective mechanisms (which could be a smart contract … see the book that accompanies the collectable art) and then a proper recordat system of indefeasible title creation/transfer/exclusion.

If you want to start … look at the first step of how to identify creative commons derviative works and enforce the share-alike trait in future works.

