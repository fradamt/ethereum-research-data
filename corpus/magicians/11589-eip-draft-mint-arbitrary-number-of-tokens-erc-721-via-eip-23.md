---
source: magicians
topic_id: 11589
title: "EIP Draft : mint arbitrary number of tokens(ERC-721) via EIP-2309"
author: sciNFTist.eth
date: "2022-11-03"
category: EIPs
tags: [nft, erc-721, gas, eip-2309]
url: https://ethereum-magicians.org/t/eip-draft-mint-arbitrary-number-of-tokens-erc-721-via-eip-2309/11589
views: 1464
likes: 4
posts_count: 6
---

# EIP Draft : mint arbitrary number of tokens(ERC-721) via EIP-2309

**EIP Draft :  ERC721FancyMint**

**eip: eip-draft_ERC721FancyMint**

**title: ERC721FancyMint**

**author: scinftist.eth  ([shypink@protonmail.com](mailto:shypink@protonmail.com))**

**status: draft not submitted**

**type: ERC**

**created: 2022-11-3**

requires (*optional): <EIP 165 721 2309>

# Abstract

This standard proposes another implementation to `IERC721` Non-Fungible Tokens (NFTs) to eliminate minting fee of fixed length collection.

# Motivation

As of today there is 3 way to create a collection.

1. Minting the tokens ahead so people can see it and find it trough market places. this includes minting fee for creators!
2. create a contract and people mint the tokens, with first come first served strategy.  people cant see the Tokens before hand. and users don’t know what they get.
3. using just in time minting or Lazy minting. that is only accessible trough one platform. this limits the creators to one platform.

this implementation is like creator minted arbitrary number of tokens before hand without using gas fee on minting process.

**benefits**:

1. no minting fee, any number of token mint in constructor with O(1) execution.
2. user can view the tokens before purchasing.
3. tokens are accessible trough all Ethereum platforms.

**caveat**

1. any number of tokens should be minted at deployment time, an there is no further _mint() or _safeMint() function available.
2. this token does not support _burn() function.

# Specification

1. maxSupply is desired number of token that we want to mint
2. preOwner is the address that all tokens will be transferred to

## Interface

- this interface is needed for Enumerable extension (IERC721Enumerable) of this contract.

```auto
// get the preOwner of a tokens
function preOwner() public view returns(address);

// get the maxSupply of a token
function maxSupply() public view returns(uint256);

```

The `maxSupply_` MUST NOT be 0.

The `preOwnwer_` MUST NOT be 0x0 (i.e. zero address).

## Implementation

proposed changes to

// OpenZeppelin Contracts (last updated v4.7.0) (token/ERC721/ERC721.sol)

for full Implementation see Reference Implementation.

```auto
//proposed changes

contract ERC721FancyMint is
    Context,
    ERC165,
    IERC721,
    IERC721Metadata,
    IERC2309
{
     *@dev my proposal
     */

    //max
    uint256 private _maxSupply;
    //NFT owner
    address private _preOwner;


    constructor(
        string memory name_,
        string memory symbol_,
        uint256 maxSupply_,
        address preOwner_
    ) {

        require(preOwner_ != address(0), "preOwner can NOT be address(0)");
        require(0  “Batch token creation: emit ConsecutiveTransfer(1, 100000, address(0), to Address);”

[Test Case 2 on goerli testnet with 6000 tokens](https://goerli.etherscan.io/address/0x39095ebb95f3576f522a16fba4a21c2c109f4e98)

[Test case 2 on OpenSea with 6000 tokens](https://testnets.opensea.io/collection/fancy-second-try)

# Reference Implementation

Test cases where Implemented in PR:

[../assets/eip-draft_ERC721FancyMint/ERC721FancyMint.sol](https://github.com/shypink/EIP-draft_ERC721FancyMint/tree/master/assets/eip-draft_FancyMint/ERC721FancyMint.sol)

# Security Considerations

This EIP standard can completely protect the rights of the owner, the owner can change the NFT user and use period at any time.

but if some how user burns a token, the owner of token will be set to `0x0` (i.e. address(0) ) the token won’t be destroyed and it will assigned to preOwner. I don’t know if it occurs or not, since the `_burn()` function is removed and `_trandfer()` function has require that prevent transfer `_to` address(0) `0x0`. I wish to hear from you if you can assure me on this.

```auto
require(to != address(0), "ERC721: transfer to the zero address");
```

# Copyright

Copyright and related rights waived via CC0.

## Replies

**xinbenlv** (2023-01-04):

Thanks for the draft. Congrats on your first drat.

Some technical feedback

I’ve not figure out a strong rationale why an extra `function preOwner` is necessary when you could just do

```auto
contract FancyMint {
  mapping (uint256 => address) _owners;
  address _preOwner; // initalize in the constructor or set somewhere, or just use the owner from IOwnable
  function ownerOf(uint256 tokenId) view return(address) {
    if (tokenId < _maxSupply {
      return _owners[tokenId] ? _owners[tokenId] : _preOwner;
    }
  }
}
```

---

**sciNFTist.eth** (2023-01-04):

Thank you for your time and the energy that you gave me.

also thanks for the code it’s elegant.

originally I was thinking about of Enumerable batch minting

```auto
ERC721Enumerable /* is ERC721 */ {
    function totalSupply() external view returns (uint256);
    function tokenByIndex(uint256 _index) external view returns (uint256);
    function tokenOfOwnerByIndex(address _owner, uint256 _index) external view returns (uint256);
}
```

and there was few more steps needed to make this IERC721Enumerable compatible.

```auto
function totalSupply() public view virtual override returns (uint256) {
        return ERC721FancyMint.maxSupply();
    }
```

```auto
/**
     * @dev handling tokens index virtualy
     */
    function tokenByIndex(uint256 index)
        public
        view
        virtual
        override
        returns (uint256)
    {
        require(
            index < ERC721FancyMintEnum.totalSupply(),
            "ERC721Enumerable: global index out of bounds"
        );
        return index;
    }
```

---

```auto
function tokenOfOwnerByIndex(address owner, uint256 index)
        public
        view
        virtual
        override
        returns (uint256)
    {

        address _preOwner = ERC721FancyMint.preOwner();

        require(
            index < ERC721FancyMint.balanceOf(owner),
            "ERC721Enumerable: owner index out of bounds"
        );
        if (_preOwner == owner) {
            return preIndex(index);
        } else {
            return _ownedTokens[owner][index];
        }
    }
```

`function _beforeTokenTransfer(         address from,         address to,         uint256 tokenId     ) ` needed some more tweaks with some new functions _addTokenToPreOwner() , _removeTokenFromPreOwner()

the [file on the github ERC721FancyMintEnumRef.sol](https://github.com/shypink/Fancy_Project_Premium/blob/main/ERC721FancyMintEnumRef.sol)

If you find the time to check this too, I’ll be grateful.

---

**nathanglb** (2023-08-21):

I put out an article on this with some sample code in 2022.  Feel free to have a look.

https://medium.com/nifty-gateway/how-to-mint-nfts-at-a-fixed-gas-cost-4a040f9792d6

I invented this at Nifty Gateway and they do this at scale (since April 2022).  Feel free to check out their official implementation at:

https://etherscan.io/address/0xee2c03ced8b6755e8d76ab144677f5f350203cab#code

---

**sciNFTist.eth** (2023-08-23):

I read your article it was great and I really liked this part

```auto
struct CollectionStatus {
    bool isMinted;
    uint88 amountCreated;
    address defaultOwner;
}
```

It’s great to find a likeminded friend

---

**nathanglb** (2023-09-08):

Thanks!  Good luck with this!

