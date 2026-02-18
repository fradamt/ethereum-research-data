---
source: magicians
topic_id: 7234
title: "EIP 4353: Viewing Staked Tokens in NFT"
author: aug2uag
date: "2021-10-09"
category: EIPs
tags: [nft, token, eip, interfaces]
url: https://ethereum-magicians.org/t/eip-4353-viewing-staked-tokens-in-nft/7234
views: 2828
likes: 2
posts_count: 10
---

# EIP 4353: Viewing Staked Tokens in NFT

I’m staking tokens on NFTs and would like an interface to get the amount of tokens staked by tokenId.

The proof-of-concept / prototype NFT did hold value / amount of tokens that were successfully transferred. Within the smart contract, an amount is mapped to tokenId, so I can get the value from an individual token in a custom manner.

However, I’m wanting the ability to see if other tokens on other contracts are staked for my UI/UX. For my purposes, value is only added at mint, and the token amount does not change-- this could vary on other implementations where proof-of-stake or post-mint deposits occur.

Any thoughts how retrieving token deposit / amount / staked could be accessed from web3? Does this already exist or could it become an EIP?

## Replies

**aug2uag** (2021-10-09):

EIP issue was opened at:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/4353)












####



        opened 04:57AM - 09 Oct 21 UTC



          closed 04:05AM - 23 May 22 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/5/5cd305daac7d094900daa39255f8f5572eac8a93.jpeg)
          aug2uag](https://github.com/aug2uag)










```yaml
---
eip: <to be assigned>
title: Interface for Staked Tokens in NFTs
[…]()
description: This interface enables access to publicly viewable staking data of an NFT.
author: <Rex Creed (@aug2uag), Dane Scarborough <dane@nftapps.us>>
status: Draft
type: Standards Track
category: ERC
created: 2021-10-08
---
```

## Abstract
ERC721s can be staked with tokens, but there's no means of retrieving the amount of tokens staked and/or bound to an NFT. This proposal outlines a standard that may be implemented by all wallets and marketplaces easily to correctly retrive the staked token amount of an NFT.

## Motivation
The absence of staked tokens data limits the ability of the token owner to convey to another, for any purpose including to transact, the true amount of staked tokens as may be viewable in a wallet, marketplace, or explorer. The ability to identify and verify an exogenous value derived from the staking process may be critical to the aims of an NFT holder.

## Specification
```js
// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

/**
 * @dev Interface of the ERC165 standard, as defined in the
 * https://eips.ethereum.org/EIPS/eip-165[EIP].
 *
 * Implementers can declare support of contract interfaces, which can then be
 * queried by others ({ERC165Checker}).
 *
 * For an implementation, see {ERC165}.
 */
interface IERC721Staked {

    /**
     * @dev Returns true if this contract implements the interface defined by
     * `interfaceId`. See the corresponding
     * https://eips.ethereum.org/EIPS/eip-165#how-interfaces-are-identified[EIP section]
     * to learn more about how these ids are created.
     *
     * This function call must use less than 30 000 gas.
     */
    function supportsInterface(bytes4 interfaceId) external view returns (bool);

     /**
     * @dev Returns uint256 of the amount of on-chain ERC20 or like tokens staked and/or bound to the NFT.
     *
     * @dev Wallets and marketplaces would need to call this for displaying the amount of tokens staked and/or bound to the NFT.
     */
    function stakedAmount() external view returns (uint256);

}
```

### Suggested flow:

#### Constructor/deployment
* Creator - the owner of an NFT with its own rules for depositing tokens at and/or after the minting of a token.
* Token Amount - the current amount of on-chain ERC20 or derived tokens bound to an NFT from one or more deposits.

#### NFT displayed in wallet or marketplace
Wallet or marketplace checks if an NFT has publicly staked tokens available for view - if so, call stakedAmount() to get the current amount of tokens staked and/or bound to the NFT.

The logical code looks something like this and inspired by [William Entriken](https://ethereum.stackexchange.com/a/70116/70167):

```js
abstract contract StakedNFT {

    /// @dev mapping tokenId to staked amount
    mapping (uint256 => uint256) private stakedTokens;

    /// @dev mints a new NFT
    /// @param _to address that will own the minted NFT
    /// @param _tokenId (timestamp) id the NFT
    function mint(
        address payable _to,
        uint256 _tokenId
    )
        external
        payable
        onlyOwner
    {
        _safeMint(_to, _tokenId);
        stakedTokens[_tokenId] = msg.value;
    }

    /// @dev if interface is supported
    /// @param interfaceId interface to check
    function supportsInterface
    (
        bytes4 interfaceId
    )
        public
        view
        virtual
        override
        (
            ERC165,
            IERC165
        )
        returns
        (
            bool
        )
    {
        return
            super.supportsInterface(interfaceId);
    }

    /// @dev returns the current amount of tokens staked
    /// @param _tokenId target NFT
    function stakedAmount
    (
        uint256 _tokenId
    )
        public
        view
        returns
        (
            uint256
        )
    {
        return stakedTokens[_tokenId];
    }

}
```

## Rationale
This standard is completely agnostic to how tokens are deposited or handled by the NFT. It is, therefore, the choice and responsibility of the author to encode and communicate the encoding of their tokenomics to purchasees of their token and/or to make their contracts viewable by purchasees.

For example, tokens may be deposited at any time with any method. Also, tokens may be transferred at any time with any method. This method will identify whether the NFT has publicly vieweable staked tokens.

However, even if there are no tokens at any given time, the views should treat a supporting interface without any staked tokens assuming tokens may be added in the future. The contract logic should determine whether a possibility exists for additional tokens to be added, i.e., a `depositingType` boolean. For example, if all tokens are withdrawn and no additional tokens will be deposited, it would be desired for a non-supporting interface response to be returned. There may be additional identifiers whether the NFT is a one-time deposit and if the NFT disallows withdraw actions. These may help the interface to provide additional insight and standardizations across staking operations.

## Copyright
Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

---

**fulldecent** (2021-10-12):

Before going ahead and standardizing something, please launch your own product and then after that build the case for why other people need to do this the exact same way you did it.

---

**aug2uag** (2021-10-12):

The product is available on the Apple AppStore under “Iconic Apps”, there are two apps in production beta undergoing finalization. The tokens are bound to NFTs at mint and in my use case the tokens are never able to be disassociated from commodity NFTs. In this way, we can ensure NFTs will remain with their assigned token amounts.

The primary impetus for my request is the need to display token values on an explorer and elsewhere including wallets and marketplaces. Although my app is not in its intended final state (it will be undergoing improvements to its tokenomics in the coming weeks), I encourage others to try and view staked token balances on NFTs to encounter the issue I am facing.

---

**pizzarob** (2022-05-28):

Hi. I think any kind of NFT staking is interesting and have implemented different variations in several products I’ve built over the last few years.

I guess my question is why does this need to be a standard and why now? It seems like you can definitely implement this interface and provide documentation for marketplaces and wallets to support but right now it seems very specific to your product. If there seemed to be interest in this standard I think it makes sense. But permanently staked ERC20 tokens tied to NFTs seems very one off, no?

---

**loretta_gould** (2022-12-07):

Hi I’m new to NFT market and i was scammed once. so I’m being smart about this before I proceed. This is not the Site that Scammed me but i wanted to check if it was a legit marketplace. how do I check if a market place is legit. [www.metartes.com](http://www.metartes.com) its a NFT marketplace. Thank You

---

**aug2uag** (2023-01-28):

[@fulldecent](/u/fulldecent) the app is now available on iOS, Iconic Apps: IconicQuotes, IconicJokes, soon to be released IconicMedia

The inspiration here was for content creators, enabling them to create transactables from their works with their audience, in a manner they can receive royalties

The issue became that of assurance, staking was used to allow the creator to receive the staked funds in case their token (i.e., expected future royalties) were to be burned

---

**aug2uag** (2023-01-28):

Currently, explorers do not display staked token amounts-- this becomes difficult if the contract is not available for view and if the transfer of staked tokens is arbitrary

The ideal condition is to enforce staking until it is burned, this logically eliminates the variability from transfers, and becomes a more standardized format for auditing and building community trust, such as displaying token amounts on the blockchain explorer

What would be great is if we can form a consensus around the idea of staking an NFT and the utility it would provide the community: specifically allowing someone to claim they own a staked token and knowing, with certainty, the amount that is staked.

Therefore, what I’m proposing is to enforce a no-transfer rule for tokens intended to be utilized in this manner: of publicly displaying staked amount, and to limit any transfer activity to the `burn` event/method. Furthermore, that the associated contract is validated and transparent against this feature, thus, allowing an explorer to safely determine whether a staked amount exists

An alternate strategy would need to trace blocks, for example a blockchain that serves to keep track of tokens who claim a staked status, and tracking all their transfer events to keep an up-to-date log of the actual amount staked-- the bottom line is that it’s in everyone’s best interest for the amount claimed to be staked is the actual amount that is staked, since these may have real consequences as mentioned above

I personally think the tracking/tracing is a little too much for a first step, and it’s beyond my personal use case. Therefore, my proposition is to limit transfers to `burn`, expose a method that returns the staked value, and have the contract code available for auditing, transparency, and assurance-- all so that an explorer may display the staked amount of a token

---

**aug2uag** (2023-01-28):

[@pizzarob](/u/pizzarob) the staking wouldn’t be ERC20, it would be native token at the time of mint – this raises the point of adding additional value, which could be safely implemented. My app is made for blockchain novices and does not have the feature to add more native tokens to an already minted NFT

---

**aug2uag** (2025-04-11):

I’d like to re-visit this and thank the earlier responses. I wasn’t thinking of utility beyond a standard for setting a token type as staked. But I can see now that utility is what the original was missing.

I’d like to propose a design pattern that enables configurable access to staked tokens. The core concept is simple: a contract holds staked tokens, and NFT ownership represents the right to designate who can access or utilize those tokens under configurable conditions.

```js
// Simplified example of the core pattern
contract StakedTokenAccessNFT is ERC721 {
    address public owner;
    // NFT ID -> accessor address -> permission
    mapping(uint256 => mapping(address => bool)) public tokenAccessors;
    // NFT ID -> max number of accessors
    mapping(uint256 => uint256) public accessorLimits;
    // NFT ID -> current number of accessors
    mapping(uint256 => uint256) public currentAccessorCounts;

    // Staking related state variables
    mapping(uint256 => uint256) public stakedAmounts; // NFT ID -> amount of tokens staked
    IERC20 public stakingToken;

    constructor(string memory name, string memory symbol, address _stakingToken) ERC721(name, symbol) {
        owner = msg.sender;
        stakingToken = IERC20(_stakingToken);
    }

    // Mint NFT and stake tokens in one transaction
    function mintWithStake(address to, uint256 tokenId, uint256 stakeAmount, uint256 _accessorLimit) external {
        require(stakingToken.transferFrom(msg.sender, address(this), stakeAmount), "Stake transfer failed");

        _mint(to, tokenId);
        stakedAmounts[tokenId] = stakeAmount;
        accessorLimits[tokenId] = _accessorLimit;
    }

    // NFT owner can manage accessors
    function addAccessor(uint256 tokenId, address accessor) external {
        require(ownerOf(tokenId) == msg.sender, "Not the NFT owner");
        require(currentAccessorCounts[tokenId] < accessorLimits[tokenId], "Accessor limit reached");
        require(!tokenAccessors[tokenId][accessor], "Already an accessor");

        tokenAccessors[tokenId][accessor] = true;
        currentAccessorCounts[tokenId]++;
    }

    function removeAccessor(uint256 tokenId, address accessor) external {
        require(ownerOf(tokenId) == msg.sender, "Not the NFT owner");
        require(tokenAccessors[tokenId][accessor], "Not an accessor");

        tokenAccessors[tokenId][accessor] = false;
        currentAccessorCounts[tokenId]--;
    }

    // Accessor can use the staked tokens as defined by implementation
    function useStakedTokens(uint256 tokenId, uint256 amount, address recipient, bytes calldata data) external {
        require(tokenAccessors[tokenId][msg.sender], "Not an authorized accessor");
        require(amount <= stakedAmounts[tokenId], "Insufficient staked amount");

        // Implementation would depend on specific use case
        // Examples:
        // - Transfer a portion of staked tokens to recipient
        // - Use tokens as collateral for a loan
        // - Execute a custom action defined by the data parameter

        // This is where application-specific logic would be implemented
        _executeTokenUtilization(tokenId, amount, recipient, data);
    }

    // Private function that defines how tokens can actually be used
    function _executeTokenUtilization(uint256 tokenId, uint256 amount, address recipient, bytes calldata data) private {
        // Application-specific implementation
    }
}
```

The specification combines:

- standard interface for identification of staking
- utility benefits

I am not aware of this, if it exists.

It’s foreseeable to have uses, an example use case:

A child in Nethers is raised by his mother in impoverished conditions. The child performs well at school and gets a reward. Company X pools staked assets and deposits rewards accessible to the child.

I can think of many more and want to hear your thoughts on this. I welcome your feedback and hope this is interesting to you.

