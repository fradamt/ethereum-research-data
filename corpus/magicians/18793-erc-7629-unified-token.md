---
source: magicians
topic_id: 18793
title: "ERC-7629: Unified Token"
author: 0xZeus1111
date: "2024-02-20"
category: ERCs
tags: [erc, nft]
url: https://ethereum-magicians.org/t/erc-7629-unified-token/18793
views: 1728
likes: 17
posts_count: 9
---

# ERC-7629: Unified Token

## Abstract

ERC-7629, known as the Unified Token Protocol, introduces a comprehensive protocol unifying the characteristics of ERC-721 and ERC-20 tokens within the Ethereum ecosystem. This standard seamlessly integrates the liquidity features of ERC-20 with the non-fungible nature of ERC-721, enabling frictionless conversion between these asset types. ERC-7629 offers a multifunctional solution, providing developers and users with the flexibility to leverage both liquidity and non-fungibility in a unified token framework.

## Motivation

The motivation behind ERC-7629 stems from the inherent need within the blockchain community for assets that possess both the liquidity of ERC-20 tokens and the non-fungibility of ERC-721 tokens. Current standards present a dichotomy, necessitating users to choose between these features. ERC-7629 addresses this limitation by providing a unified token standard, empowering users to seamlessly transition between ERC-20 and ERC-721 characteristics, catering to diverse blockchain applications.

## Specification

- ERC-7629 standardizes a token contract that encompasses features from both ERC-20 and ERC-721.
- The token contract supports state transitions between ERC-20 and ERC-721 modes, ensuring smooth conversion and utilization of both liquidity and non-fungibility.
- Defines essential functions and events to support token interactions, conversions, and queries.
- Implements a low gas consumption ERC-20 mode to maintain gas efficiency comparable to typical ERC-20 token transfers.

Compliant contracts MUST implement the following Solidity interface:

```solidity
pragma solidity ^0.8.0;
/**
 * @title ERC-7629 Unify Token Interface
 * @dev This interface defines the ERC-7629 Unify Token, which unifies ERC-721 and ERC-20 assets.
 */
interface IERC7629  is IERC165 {
    // ERC-20 Transfer event
    event ERC20Transfer(
        address indexed from,
        address indexed to,
        uint256 amount
    );

    // ERC-721 Transfer event
    event ERC721Transfer(
        address indexed from,
        address indexed to,
        uint256 indexed tokenId
    );

    // ERC-721 Transfer event
    event Transfer(
        address indexed from,
        address indexed to,
        uint256 indexed tokenId
    );

    // Approval event for ERC-20 and ERC-721
    event Approval(
        address indexed owner,
        address indexed approved,
        uint256 indexed tokenId
    );

    // Approval event for ERC-20 and ERC-721
    event Approval(
        address indexed owner,
        address indexed approved,
        uint256 indexed tokenId
    );

    // Approval event for ERC-20
    event ERC20Approval(
        address indexed owner,
        address indexed approved,
        uint256 indexed tokenId
    );

    // ApprovalForAll event for ERC-721
    event ApprovalForAll(
        address indexed owner,
        address indexed operator,
        bool approved
    );

    // ERC-20 to ERC-721 Conversion event
    event ERC20ToERC721(address indexed to, uint256 amount, uint256 tokenId);

    // ERC-721 to ERC-20 Conversion event
    event ERC20ToERC721(address indexed to, uint256 amount, uint256[] tokenIds);

    /**
     * @dev Returns the name of the token.
     */
    function name() external view returns (string memory);

    /**
     * @dev Returns the symbol of the token.
     */
    function symbol() external view returns (string memory);

    /**
     * @dev Returns the number of decimals used in the token.
     */
    function decimals() external view returns (uint8);

    /**
     * @dev Returns the total supply of the ERC-20 tokens.
     */
    function totalSupply() external view returns (uint256);

    /**
     * @dev Returns the balance of an address for ERC-20 tokens.
     * @param owner The address to query the balance of.
     */
    function balanceOf(address owner) external view returns (uint256);

    /**
     * @dev Returns the total supply of ERC-20 tokens.
     */
    function erc20TotalSupply() external view returns (uint256);

    /**
     * @dev Returns the balance of an address for ERC-20 tokens.
     * @param owner The address to query the balance of.
     */
    function erc20BalanceOf(address owner) external view returns (uint256);

    /**
     * @dev Returns the total supply of ERC-721 tokens.
     */
    function erc721TotalSupply() external view returns (uint256);

    /**
     * @dev Returns the balance of an address for ERC-721 tokens.
     * @param owner The address to query the balance of.
     */
    function erc721BalanceOf(address owner) external view returns (uint256);

    /**
     * @notice Get the approved address for a single NFT
     * @dev Throws if `tokenId` is not a valid NFT.
     * @param tokenId The NFT to find the approved address for
     * @return The approved address for this NFT, or the zero address if there is none
     */
    function getApproved(uint256 tokenId) external view returns (address);

    /**
     * @dev Checks if an operator is approved for all tokens of a given owner.
     * @param owner The address of the token owner.
     * @param operator The address of the operator to check.
     */
    function isApprovedForAll(
        address owner,
        address operator
    ) external view returns (bool);

    /**
     * @dev Returns the remaining number of tokens that spender will be allowed to spend on behalf of owner.
     * @param owner The address of the token owner.
     * @param spender The address of the spender.
     */
    function allowance(
        address owner,
        address spender
    ) external view returns (uint256);

    /**
     * @dev Returns the array of ERC-721 token IDs owned by a specific address.
     * @param owner The address to query the tokens of.
     */
    function owned(address owner) external view returns (uint256[] memory);

    /**
     * @dev Returns the address that owns a specific ERC-721 token.
     * @param tokenId The token ID.
     */
    function ownerOf(uint256 tokenId) external view returns (address erc721Owner);

    /**
     * @dev Returns the URI for a specific ERC-721 token.
     * @param tokenId The token ID.
     */
    function tokenURI(uint256 tokenId) external view returns (string memory);

    /**
     * @dev Approve or disapprove the operator to spend or transfer all of the sender's tokens.
     * @param spender The address of the spender.
     * @param amountOrId The amount of ERC-20 tokens or ID of ERC-721 tokens.
     */
    function approve(
        address spender,
        uint256 amountOrId
    ) external returns (bool);

    /**
     * @dev Set or unset the approval of an operator for all tokens.
     * @param operator The address of the operator.
     * @param approved The approval status.
     */
    function setApprovalForAll(address operator, bool approved) external;

    /**
     * @dev Transfer ERC-20 tokens or ERC-721 token from one address to another.
     * @param from The address to transfer ERC-20 tokens or ERC-721 token from.
     * @param to The address to transfer ERC-20 tokens or ERC-721 token to.
     * @param amountOrId The amount of ERC-20 tokens or ID of ERC-721 tokens to transfer.
     */
    function transferFrom(
        address from,
        address to,
        uint256 amountOrId
    ) external returns (bool);

    /**
     * @notice Transfers the ownership of an NFT from one address to another address
     * @dev Throws unless `msg.sender` is the current owner, an authorized
     *  operator, or the approved address for this NFT. Throws if `_rom` is
     *  not the current owner. Throws if `_to` is the zero address. Throws if
     *  `tokenId` is not a valid NFT. When transfer is complete, this function
     *  checks if `to` is a smart contract (code size > 0). If so, it calls
     *  `onERC721Received` on `to` and throws if the return value is not
     *  `bytes4(keccak256("onERC721Received(address,address,uint256,bytes)"))`.
     * @param from The current owner of the NFT
     * @param to The new owner
     * @param tokenId The NFT to transfer
     * @param data Additional data with no specified format, sent in call to `to`
     */
    function safeTransferFrom(address from, address to, uint256 tokenId, bytes calldata data) external payable;

    /**
     * @notice Transfers the ownership of an NFT from one address to another address
     * @dev This works identically to the other function with an extra data parameter,
     *  except this function just sets data to "".
     * @param from The current owner of the NFT
     * @param to The new owner
     * @param tokenId The NFT to transfer
     */
    function safeTransferFrom(address from, address to, uint256 tokenId) external payable;

    /**
     * @dev Transfer ERC-20 tokens to an address.
     * @param to The address to transfer ERC-20 tokens to.
     * @param amount The amount of ERC-20 tokens to transfer.
     */
    function transfer(address to, uint256 amount) external returns (bool);

    /**
     * @dev Retrieves the unit value associated with the token.
     * @return The unit value.
     */
    function getUnit() external view returns (uint256);

    /**
     * @dev Converts ERC-721 token to ERC-20 tokens.
     * @param tokenId The unique identifier of the ERC-721 token.
     */
    function erc721ToERC20(uint256 tokenId) external;

    /**
     * @dev Converts ERC-20 tokens to an ERC-721 token.
     * @param amount The amount of ERC-20 tokens to convert.
     */
    function erc20ToERC721(uint256 amount) external;
}

```

## Rationale

The rationale for ERC-7629 lies in its ability to harmonize liquidity and non-fungibility, filling a crucial gap in the existing token standards. By unifying ERC-20 and ERC-721 features, ERC-7629 enhances user flexibility, allowing for efficient conversion between these asset types. The protocol is designed to provide a standardized and versatile solution for developers, promoting a more streamlined development process. With smooth transitions and low gas consumption, ERC-7629 aims to be a robust standard that not only simplifies token interactions but also fosters broader adoption within the Ethereum ecosystem.

## Backwards Compatibility

The proposed ERC-7629 introduces a challenge in terms of backward compatibility due to the distinct balance query mechanisms utilized by ERC-20 and ERC-721 standards. ERC-20 employs balanceOf to check an account’s token balance, while ERC-721 uses balanceOf to inquire about the quantity of tokens owned by an account. To reconcile these differences, the ERC must consider providing either two separate functions catering to each standard or adopting a more generalized approach.

### Compatibility Points

The primary compatibility point lies in the discrepancy between ERC-20’s balanceOf and ERC-721’s balanceOf functionalities. Developers accustomed to the specific balance query methods in each standard may face challenges when transitioning to ERC-7629.

### Proposed Solutions

Dual Balance Query Functions:

Introduce two distinct functions, erc20BalanceOf and erc721TotalSupply, to align with the conventions of ERC-20 and ERC-721, respectively. Developers can choose the function based on the token type they are working with.

## Test Cases

## Reference Implementation

- ERC-7629 standard undergoes thorough testing to ensure consistent and accurate behavior in both ERC-20 and ERC-721 modes.
- Detailed documentation and sample code are provided to assist developers in understanding and implementing the ERC-7629 standard.



      [github.com](https://github.com/ColorfuLabs/ERC7629)




  ![image](https://opengraph.githubassets.com/76956403cb528e54d50df6fa72e5a3ed/ColorfuLabs/ERC7629)



###



Unifying ERC-721 and ERC-20 for seamless asset conversion.










## Security Considerations

- Due to the dual nature of ERC-7629, potential differences in protocol interpretation may arise, necessitating careful consideration during development.
- Comprehensive security audits are recommended, especially during mode transitions by users, to ensure the safety of user assets.

## Replies

**mk124690** (2024-02-20):

awesome！the innovation made by combining the characteristics of erc20 and erc721 is indeed superb and improves liquidity. It can be said that it fills the gap between erc standards and looks forward to opening up a new situation in web3.

---

**sennett-lau** (2024-02-20):

I’d like to engage in a deeper conversation regarding four specific aspects:

1. Should the functions safeTransferFrom(address from, address to, uint256 tokenId) and safeTransferFrom(address from, address to, uint256 tokenId, bytes calldata data) be incorporated as standard functionalities within the ERC721 specification?
2. It appears there is a redundancy in the functions related to total supply within ERC20, specifically the presence of both totalSupply() and erc20TotalSupply() . This seems to duplicate functionality unnecessarily.
3. For the sake of clarity and to avoid ambiguity, all instances of id referring to a token’s identification number in the context of ERC721 should consistently be labeled as tokenId .
4. Additionally, should there be consideration for inheriting from IERC165 and IERC20 to ensure backward compatibility? This could potentially streamline integration and interoperability with existing contracts and standards.

---

**abcoathup** (2024-02-20):

How is this different from **ERC7616: Hybrid fungible token**?

https://github.com/ethereum/ERCs/pull/244

I asked the people behind **DN404 (Solidity contract): hybrid ERC20 & ERC721, mints/burns NFTs based on ERC20 balance** if they wanted to create an ERC.

https://github.com/Vectorized/dn404#readme

---

As an aside, EIP/ERC/RIP numbering changed to sequential from 7500.  Numbers are issued by editors/associates.  Authors don’t get to pick their own numbers.

---

**sennett-lau** (2024-02-21):

For `ERC7616`:

`ERC7616` is designed to associate `ERC20` tokens with individual `ERC721` tokens, enabling the transfer of balances through each unique NFT. While the proposed unified token standard, `ERC7629`, extends this functionality by incorporating a built-in swap mechanism. A direct trading between NFTs and / or fungible tokens (FTs) can be executed easily with NFT_A/FT_A ⇄ FT_B/NFT_B, provided there’s a liquidity pool for FT_A and FT_B.

This seems to enable more flexible trading options directly within NFT itself.

For `DN404`:

`DN404` focuses on a unique approach where an entity can simultaneously own `ERC20` and `ERC721` tokens. This mechanism allows for the minting / burning of `ERC721` tokens based on the amount of ERC20 tokens held, rather than enabling direct swapping between token types.

---

**0xZeus1111** (2024-02-21):

ERC-7616 is built upon ERC-3525, both being SFT tokens. In 7616, the TokenID of the NFT holds FT, and the transfer of FT occurs between the TokenIDs of the NFT. When transferring the NFT, FT is simultaneously transferred. ERC-7616 is not compatible with ERC-721 but is compatible with ERC-20. On the other hand, ERC-7629 is compatible with both ERC-721 and ERC-20, allowing seamless switching between the two asset types.

---

**0xZeus1111** (2024-02-21):

Thank you for your suggestions.

I will include `safeTransferFrom` in ERC-7629.

Both `totalSupply()` and `erc20TotalSupply()` are used to query ERC-20 balances. I am still inclined to retain `erc20TotalSupply` in ERC-7629. In ERC-7629, by default, `totalSupply` and `balanceOf` methods are allocated to ERC-20. This is primarily to ensure that ERC-7629 can seamlessly integrate with existing DeFi infrastructure without creating an impression that it is solely ERC-20.

Additionally, I’ll include IERC-165 in ERC-7629.

---

**abcoathup** (2024-02-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sennett-lau/48/11749_2.png) sennett-lau:

> For DN404:
> DN404 focuses on a unique approach where an entity can simultaneously own ERC20 and ERC721 tokens. This mechanism allows for the minting / burning of ERC721 tokens based on the amount of ERC20 tokens held, rather than enabling direct swapping between token types.

Now it is a proposed ERC:

ERC-7631: Dual Nature Token Pair

https://github.com/ethereum/ERCs/pull/271/files

---

**fomo-protocol** (2024-03-02):

As the author of ERC7616, my initial vision was inspired by the approach taken by ERC-3525, where each NFT carries an attached value, allowing for the transfer of value between NFTs.

However, recognizing that this feature might not align with the broader community’s desires, I’ve since relegated it to an optional component of the standard.

ERC7616 is designed to facilitate the coexistence of ERC20 and ERC721 standards within a single contract framework. Upon reflection, I believe that your proposal does not substantially diverge from what ERC7616 already offers.

Importantly, ERC7616 does not mandate that NFTs must be convertible into fungible tokens (FTs), or vice versa. Instead, it grants developers the flexibility to define the nature of the relationship between FTs and NFTs according to their specific project needs.

Consequently, functionalities such as `ERC20ToERC721` conversion are not inherent to the ERC7616 standard.

In my view, ERC7616 offers a more versatile and standardized framework, adeptly accommodating a wide range of applications and use cases within the digital asset domain.

