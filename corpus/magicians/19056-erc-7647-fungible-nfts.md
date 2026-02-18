---
source: magicians
topic_id: 19056
title: "ERC-7647: Fungible NFTs"
author: LordJ
date: "2024-03-05"
category: ERCs
tags: [erc, nft, erc-721, erc-20]
url: https://ethereum-magicians.org/t/erc-7647-fungible-nfts/19056
views: 2021
likes: 5
posts_count: 9
---

# ERC-7647: Fungible NFTs

## E741 - Fungible NFTs

## Abstract

This proposal introduces a hybrid token standard that combines the features of ERC-20 and ERC-721 tokens. The E741 token standard allows for fungible and non-fungible assets to be represented within a single token contract, providing enhanced functionality for applications that require both types of tokens.

## Motivation

Currently, Ethereum supports two widely-used token standards: ERC-20 for fungible tokens and ERC-721 for non-fungible tokens. However, there are scenarios where applications require both fungible and non-fungible assets to be managed within the same system. For example, in decentralized games or collectibles platforms, users may hold both currency (fungible) and unique assets (non-fungible).

By combining ERC-20 and ERC-721 functionalities into a single token standard, developers can streamline their smart contract architecture and simplify interactions for users who hold both types of assets. This proposal aims to address this need by defining a unified standard for hybrid tokens on the Ethereum blockchain.

Furthermore, there are liquidity issues associated with the auction model of the ERC-721 standard and this proposal aims to address some of those limitations present in the NFT marketplace by allowing NFT’s to be sold in whole and in pieces through a Decentralized Exchange (DEX).

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

The E741 token standard MUST inherit all functions and events from both ERC-20 and ERC-721, with additional considerations for interoperability between the two types of tokens. It is RECOMMENDED to support both types of events through an internal library, however a token MAY use another interface if it achieves the same event structure.

It is RECOMMENDED to support optional metadata features from  ERC-20 and ERC-721.

The following rules MUST be followed to adhere to the E741 standard:

- 1.0 ERC-20 tokens represent 1 NFT.
- The decimals of the token combined with 1.0 represent the token id.
-i.e. 1.12345 would represent token id 12345
- The maximum total supply corresponds to the total number of NFTs sans decimal. It is OPTIONAL to either fix the total supply with the maximum NFT id, or to increase the total supply as new NFTs are minted.

i.e. If the largest NFT id is 123, the maximum total supply is 123.

The decimals of the token MUST accomodate the number of posisble NFTs.

- i.e. Four decimals allows for max NFT id of 9999

Specific ids can be transfered by using their ERC-20 representation

- i.e. transfer(to, 1.12345) would send token id 12345

Sending a specifc token id will only transfer `1.0` ERC-20 tokens along side the nft.

- i.e. transfer(to, 1.12345) would send token id 12345 + 1.0 ERC-20 tokens

NFT’s will be ‘broken’ during a transfer that forces a user’s balance to decrease in such a way as to cross a `1.0` ERC-20 threashold.
NFT’s will be ‘unbroken’ during a transfer that forces a user’s balance to increase in such a way as to cross a `1.0` ERC-20 threshold.
NFT’s that are ‘broken’ must be maintained in a ‘broken list’ temporarily.

### Interface

```solidity
// ERC-20 events
library libES20 {
    event Transfer(address indexed from, address indexed to, uint amount);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    function emitTransfer(address _from, address _to, uint _amount) internal { emit Transfer(_from, _to, _amount); }
    function emitApproval(address _owner, address _spender, uint _value) internal { emit Approval(_owner, _spender, _value); }
}

// ERC-721 events
library libES721 {
    event Transfer(address indexed _from, address indexed _to, uint indexed _tokenId);
    event Approval(address indexed _owner, address indexed _approved, uint indexed _tokenId);
    event ApprovalForAll(address indexed _owner, address indexed _operator, bool _approved);
    function emitTransfer(address _from, address _to, uint _tokenId) internal { emit Transfer(_from, _to, _tokenId); }
    function emitApproval(address _owner, address _approve, uint _tokenId) internal { emit Approval(_owner, _approve, _tokenId); }
    function emitApprovalForAll(address _owner, address _operator, bool _approved) internal { emit ApprovalForAll(_owner, _operator, _approved); }
}

interface IERC165 {
    function supportsInterface(bytes4 interfaceID) external view returns (bool);
}

interface IERC-20 {
    function balanceOf(address account) external view returns (uint256);
    function totalSupply() external view returns (uint256);
    function transfer(address to, uint256 value) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
    function decimals() external view returns (uint);
}

interface IERC-721 is IERC165 {
    function balanceOf(address account) external view returns (uint256);
    function ownerOf(uint256 _tokenId) external view returns (address);
    function safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes memory data) external payable;
    function safeTransferFrom(address _from, address _to, uint256 _tokenId) external payable;
    function setApprovalForAll(address _operator, bool _approved) external;
    function getApproved(uint256 _tokenId) external view returns (address);
    function isApprovedForAll(address _owner, address _operator) external view returns (bool);
    // payable removed for ERC-20 etherscan compatibility
    function approve(address spender, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
}

interface IE741 is IERC-20, IERC-721 {
    // supportsInterface 0x5a46575f
    // library transfers can not be included in the interface
    // incorporate them directly with library
    function balanceOf(address account) external override(IERC-20, IERC-721) view returns (uint256);
    function approve(address spender, uint256 value) external override(IERC-20, IERC-721) returns (bool);
    function transferFrom(address from, address to, uint256 value) external override(IERC-20, IERC-721) returns (bool);
}

interface IERC-721Metadata {
    function name() external view returns (string memory _name);
    function symbol() external view returns (string memory _symbol);
    function tokenURI(uint256 _tokenId) external view returns (string memory);
}

interface IERC-7572 {
    function contractURI() external view returns (string memory);
    event ContractURIUpdated();
}

interface IERC-20Metadata {
    function name() external view returns (string memory _name);
    function symbol() external view returns (string memory _symbol);
    function tokenURI(uint256 _tokenId) external view returns (string memory);
}
```

## Rationale

There are many limitations to the ERC-721 standard, namely the problem of liquidity. The majority of NFTs on the open market leave owners without the ability to liquidate assets despite a high floor price. In the worst case this leaves people with serious tax implications if they hold an NFT with a high floor price and no interested buyers in their particular NFT.

Besides the liquidity issue, partial ownership of NFT’s is not possible, and a range of possibilities opens with the paradigm of partial NFT ownersip. This not only gives someone the ability to slowly accumulate enough to cross the threshold into NFT ownership but it also allows someone to temporarilty liquidate a portion of their NFT asset for a short period of time.

With this proposal we hope to open the world to new possibilities with NFTs to bring them into the free market DEX environment.

## Backwards Compatibility

The creators of E741 worked hard to maintain backwards compatibility with the ERC-20 and ERC-721 standard, however one feature was not possible to adhere to.

The ERC-721 standard has the `payable` keyword on several functions that are `non payable` in ERC-20. In order to support both standards generally the `payable` keyword was removed from the incompatible functions.

In our experience it is rare for a protocol to force payment through `approve`, `transferFrom`, and `safeTransferFrom`. However, if a protocol does force payment, the transactions will fail with the E741 standard.  We found this to be an acceptible compromise compared to the benefits of the standard.

In order to bring the marketplace towards the E741 standard, the creators have also developed wrappers to bridge the gap from ERC-20 to E741, and from ERC-721 to E741. Any ERC-20 can be “nft-ized” and any ERC-721 can be “token-ized”.

## Test Cases

Comprehensive unit test cases were performed on the first implementation of E741, and the creators will strive to open source test cases for other’s to ensure their tokens meet the standards of this proposal.

## Security Considerations

Existing protocols may be succeptible to loss of funds if precautions are not taking when handling E741 tokens. Specifically when a value such as `1.12345` is used to transfer `1.0` ERC-20 worth of tokens along side an NFT with id 12345, the protocol may internally track a deposit/withdraw of `1.12345` resulting in mismanaged accounting.

## Implementations


      ![](https://etherscan.io/images/favicon3.ico)

      [Ethereum (ETH) Blockchain Explorer](https://etherscan.io/token/0x382EDfe4c6168858C81893fE00fCB7b68914d929#code)



    ![](https://etherscan.io/images/brandassets/og-preview-sm.jpg)

###



Token Rep: Unknown | Holders: 625 | As at Dec-29-2025 04:24:30 PM (UTC)

## Replies

**abcoathup** (2024-03-05):

ERC numbers are assigned by ERC editors/associates. they are now sequential, you don’t get to pick your own number.

There have been multiple hybrid token ERCs drafted recently.  Please review these to see if you could add/improve these rather than creating another hybrid token ERC.

---

**pyrobit** (2024-03-06):

Greetings! Sir, what are the current assigned hybrid token standards? Found this: ERC-6960 is still in draft mode.

---

**LordJ** (2024-03-06):

I have found



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xzeus1111/48/11726_2.png)

      [ERC-7629: Unified Token](https://ethereum-magicians.org/t/erc-7629-unified-token/18793) [ERCs](/c/ercs/57)




> Abstract
> ERC-7629, known as the Unified Token Protocol, introduces a comprehensive protocol unifying the characteristics of ERC-721 and ERC-20 tokens within the Ethereum ecosystem. This standard seamlessly integrates the liquidity features of ERC-20 with the non-fungible nature of ERC-721, enabling frictionless conversion between these asset types. ERC-7629 offers a multifunctional solution, providing developers and users with the flexibility to leverage both liquidity and non-fungibility in a u…

They utilize ERC-20 to ERC-721 conversion within their contract by assigning each id a value. Our approach doesn’t separate NFTs from tokens and instead couples the transactions together. Always using both token standards in a transaction (unless the user has more tokens than IDs, transfer less than 1.0 tokens, or don’t roll over or under a balance of 1.0 * n tokens). Each ID is equivalent to 1.000.. tokens making it so that any user whom collects 1.0 * n tokens will receive n NFTs with no need for further conversion.

and



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vectorized/48/7129_2.png)

      [ERC-7631: Dual Nature Token Pair](https://ethereum-magicians.org/t/erc-7631-dual-nature-token-pair/18796) [ERCs](/c/ercs/57)




> Dual Nature Token Pair
> requires: ERC-20, ERC-721
> Abstract
> A fungible ERC-20 token contract and non-fungible ERC-721 token contract can be interlinked, allowing actions performed on one contract to be reflected on the other. This proposal defines how the relationship between the two token contracts can be queried. It also enables accounts to configure if ERC-721 mints and transfers should be skipped during ERC-20 to ERC-721 synchronization.
> Motivation
> The ERC-20 fungible and ERC-721 non-fungibl…

DN404 is a separate, unique, approach which links 2 tokens together. This creates the requirement of handling 2 tokens addresses (one for ERC-20 and one for ERC-721). Our solution only requires one contract, making usage streamlined for users by them not needing to track 2 addresses. They also implement a way for users to skip minting and transfer of IDs. We offer a similar solution. However, we only allow the skip of minting to ensure parity between user balances and ID count.

It also may be worth noting that Emeralds predates all recent hybrid token implementations with our Emeralds v1 which was sadly a flawed implementation which we improved on after an exploit.

---

**ownerlessinc** (2024-04-25):

The solution seems confusing at the contract level and there is room for improvement.

My questions regarding compatibility:

If I mint the NFTs, will they show up on OpenSea, Rarible, and other marketplaces?

If I mint the ERC20s, can I use them to manage liquidity in Uniswap V2/V3? Will the NFTs affect the usage of the protocol?

We can always wrap NFTs and mint tokens as we can wrap tokens and mint NFTs. Using more gas to separate both in the same contract, isn’t it the same as simply wrapping them and providing new features using the existing standards?

---

**LordJ** (2024-04-26):

Yes minted NFTs have been showing up on all the platforms we’ve tested natively. including etherscan, nftscan, opensea, and other platforms.

We ensured 100% compatibility with ERC20 interactions so the token should operate normally in those contracts.

Our solution doesn’t involve any wrapping. Each NFT is intrinsically linked with 1.0 tokens. When a user makes an ERC721 transaction, an equivalent ERC20 transaction takes place and vice versa. There is no wrapping or unwrapping.

On contract initialisation, the owner is minted the ERC20 totalSupply but not the NFT ids as this would be too gassy. The owner is also exempt from minting NFTs during their transactions to further lower gas. This allows the owner to create uniswap pools or deposit the tokens in whichever contract they like. Once the owner has set up on those contracts, the further transactions from those platforms causes the NFT ids to mint as the users receive their tokens. Once there are ids minted and available for transfers, they are prioritised instead of minting.

The order of NFT id operations are as follows:

Does sender have an id to send?

yes:

send that id

no:

is there an id in the broken ids pool?

yes:

send the id from that pool

no:

mint a new id

To sum it up: there aren’t 2 tokens that you wrap/unwrap, only 1 token: the fractions NFTs

---

**zhuzhu** (2024-11-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> There have been multiple hybrid token ERCs drafted recently. Please review these to see if you could add/improve these rather than creating another hybrid token ERC.

thank you, thanks to your answers, information about ERC hybrid tokens has become more clear

---

**sullof** (2024-11-15):

An easy way to obtain the same is to mint an NFT and then create an ERC20 as an ERC7656Service, deployed using an ERC7656Registry. No need for a new standard, I think.

---

**Halva777** (2024-11-16):

In what ways does the E741 standard address the liquidity issues associated with NFTs, and how might this impact the NFT marketplace and user behavior?

