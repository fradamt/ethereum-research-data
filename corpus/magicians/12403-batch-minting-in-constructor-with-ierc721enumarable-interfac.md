---
source: magicians
topic_id: 12403
title: Batch minting in constructor with IERC721Enumarable interface
author: sciNFTist.eth
date: "2023-01-03"
category: ERCs
tags: [erc, nft, token, erc-721, gas]
url: https://ethereum-magicians.org/t/batch-minting-in-constructor-with-ierc721enumarable-interface/12403
views: 2213
likes: 25
posts_count: 19
---

# Batch minting in constructor with IERC721Enumarable interface

# new Implementation of ERC721 that removes minting fee or no transaction fee minting.(ERC721FancyMint.sol)

As of today there is two way to mint ERC721 NFTs:

1. lazy minting or just in time minting.
2. pay the minting fees your self and list them.

I created a way to mint arbitrary number of NFT with **no minting fee**.

## how other ERC721 works?

at the heart of any ERC721 there is data storage that hold what token(token Id number) belongs to which Ethereum address.

[![owner](https://ethereum-magicians.org/uploads/default/original/2X/4/4bdc0eb7e22cc5755c7de17e6eb72478857bcef9.png)owner672×376 11.7 KB](https://ethereum-magicians.org/uploads/default/4bdc0eb7e22cc5755c7de17e6eb72478857bcef9)

this is a “Mapping”, Mapping is like a kind of magical table/record, it has a default value for every possible entry.

the default value for addresses are address(0).

[![map-1](https://ethereum-magicians.org/uploads/default/original/2X/d/d73eb3860ab38b2024037bfd9a4a4b01caddc977.png)map-1683×763 15.3 KB](https://ethereum-magicians.org/uploads/default/d73eb3860ab38b2024037bfd9a4a4b01caddc977)

as people **mint** tokens, contract populates the mapping with user address.

[![map-3](https://ethereum-magicians.org/uploads/default/original/2X/0/0d8da409ae8fa7b54bc336a7f577d4f3a69e211a.png)map-3700×782 20.1 KB](https://ethereum-magicians.org/uploads/default/0d8da409ae8fa7b54bc336a7f577d4f3a69e211a)

An ERC721 contract have to determine which tokens exist.

- for example in ERC721 Implemented by OpenZeppelin the Rationale behind token existence is if a token owner address is 0x000…0000 (also called address(0)) this token does not exist, if anything else the token is exist and owned by that address.

in the image above only the tokenID **0, 1, 2** are exist.

## my Implementation:

This implementation I need to introduce you to 2 new parameter.

1. MaxSupply: total number of token that we want to mint(it can be any number without increasing transaction fee)
2. preOwner: the address that we want to mint maxSupply of token to.(maybe the creator)

This Implementation uses a new abstraction for token existence, instead of checking **token owner** not being address(0) to exist, it check if a **token Id** is less than **MaxSupply** it exists, and if the token owner is any **address** beside address(0) it belong to that *address*, if the owner was address(0) it belongs to **preOwner**.

also at deployment make the balance of the user equal to MaxSupply.

In this way **preOwner** have **MaxSupply** number of token in their wallet.

Example: If we create a collection with this implementation with the MaxSupply of 999, token 0 to 998 would be exist.

[![GroupMap](https://ethereum-magicians.org/uploads/default/optimized/2X/1/1b52f142827c0ccdf9d205a2cf4ba667fe08917d_2_458x499.png)GroupMap682×743 41.6 KB](https://ethereum-magicians.org/uploads/default/1b52f142827c0ccdf9d205a2cf4ba667fe08917d)

If you want to know more about the Implementation please look at the following links:

1. Ethereum Magicians:Idea : minting one billion NFTs or 2^256
2. Ethereum Magicians: EIP Draft : mint arbitrary number of tokens(ERC-721) via EIP-2309
3. GitHub: EIP-draft_ERC721FancyMint.sol

# benefits

1. no minting fee for any number of token.
2. tokens are accessible trough all Ethereum platforms at the same time.(like market places, block explorer,…)
3. users can view the tokens before owning them.

# Deployed on the mainnet.

**Fancy Project : Premeium**

I created a collection around this. it has 999 item and the art is on-chain SVG.

and I list them in different market places. something that you can’t do with marketplaces lazy minting contract.

[OpenSea Link](https://opensea.io/collection/fancy-project-premeium)

[![m1](https://ethereum-magicians.org/uploads/default/optimized/2X/8/8c44a223ce1718340d8f7b3f268b1b3b92673b3c_2_690x361.png)m11821×954 171 KB](https://ethereum-magicians.org/uploads/default/8c44a223ce1718340d8f7b3f268b1b3b92673b3c)

[LooksRare Link](https://looksrare.org/collections/0xE0321AF68eAE73960261DA5bbdCDD47E26741894?queryID=a1f6036c41bd80431848b472ab0281be)

[![m2](https://ethereum-magicians.org/uploads/default/optimized/2X/9/9404ac2273807897d4896b0488d6f53149340efc_2_690x353.png)m21851×947 186 KB](https://ethereum-magicians.org/uploads/default/9404ac2273807897d4896b0488d6f53149340efc)

---

and as I promised they all minted with no transaction.

[etherscan](https://etherscan.io/address/0xe0321af68eae73960261da5bbdcdd47e26741894)

[![etherscan](https://ethereum-magicians.org/uploads/default/original/2X/b/b81e34034c05099e9ed7ec107663f0c1f35cecac.png)etherscan858×739 36.3 KB](https://ethereum-magicians.org/uploads/default/b81e34034c05099e9ed7ec107663f0c1f35cecac)

[![Screenshot 2023-01-01 004744](https://ethereum-magicians.org/uploads/default/optimized/2X/f/fb3b2609a12971038770ef461149bd4478413a1b_2_627x500.png)Screenshot 2023-01-01 0047441039×828 40.4 KB](https://ethereum-magicians.org/uploads/default/fb3b2609a12971038770ef461149bd4478413a1b)

## manifold example:

they have one of the best implementation of batch minting but because of max gas limit of 12 million or 200 token per transaction.

[![manifold](https://ethereum-magicians.org/uploads/default/optimized/2X/1/13fe46d9da8434e27f90b3681fb8a11e21761fe6_2_690x471.png)manifold1395×954 114 KB](https://ethereum-magicians.org/uploads/default/13fe46d9da8434e27f90b3681fb8a11e21761fe6)

but this way you can bring down the gas usage to **zero** for any number of token.

[![Screenshot 2023-01-02 224053](https://ethereum-magicians.org/uploads/default/optimized/2X/7/7826dc4b37d8186bcd79271086ff619971685424_2_596x500.png)Screenshot 2023-01-02 2240531142×957 48.2 KB](https://ethereum-magicians.org/uploads/default/7826dc4b37d8186bcd79271086ff619971685424)

the magic happens all with the help of **EIP-2309** the consecutiveTransfer event(event is a thing that notify other application that there is something to check for) instead of simple one by one transfer.

consecutiveTransfer of token 0 - 998, are in the transaction log

PS:

**Fancy Project : Premeium** is fully compatible with IERC721 and IERC721Enumerable by using ERC721FancyMint and ERC721FancyMintEnumerable (ERC721FancyMIntEnumerable is a bit too long to explain here)

code: [Github-Fancy_project_premium](https://github.com/shypink/Fancy_Project_Premium)

## Replies

**Pandapip1** (2023-01-03):

As someone that frequently uses lazy evaluation, I am somewhat shocked that this technique wasn’t already standard practice. Kudos!

---

**sciNFTist.eth** (2023-01-03):

Thank you for taking the time to read the article and  for your good energy.

I proposed this technique back in November but it seems nobody notices it(you are the first)

If you have any recommendations, from who might be interested to see this, or where should present it. I be glad.

---

**abcoathup** (2023-01-04):

OpenZeppelin added `ERC721Consecutive` extension to OpenZeppelin Contracts which uses [ERC2309](https://eips.ethereum.org/EIPS/eip-2309)



      [github.com](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/extensions/ERC721Consecutive.sol)





####



```sol
// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v4.8.0) (token/ERC721/extensions/ERC721Consecutive.sol)

pragma solidity ^0.8.0;

import "../ERC721.sol";
import "../../../interfaces/IERC2309.sol";
import "../../../utils/Checkpoints.sol";
import "../../../utils/structs/BitMaps.sol";

/**
 * @dev Implementation of the ERC2309 "Consecutive Transfer Extension" as defined in
 * https://eips.ethereum.org/EIPS/eip-2309[EIP-2309].
 *
 * This extension allows the minting of large batches of tokens, during contract construction only. For upgradeable
 * contracts this implies that batch minting is only available during proxy deployment, and not in subsequent upgrades.
 * These batches are limited to 5000 tokens at a time by default to accommodate off-chain indexers.
 *
 * Using this extension removes the ability to mint single tokens during contract construction. This ability is
 * regained after construction. During construction, only batch minting is allowed.
```

  This file has been truncated. [show original](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/extensions/ERC721Consecutive.sol)

---

**xinbenlv** (2023-01-04):

Emm,. it still cost gas to change the MaxSupply, right?

---

**Pandapip1** (2023-01-04):

The technique used above, compared to other methods, costs practically nothing. The gas cost is ~3000 to mint any number of NFTs (even after contract construction).

---

**sciNFTist.eth** (2023-01-04):

In the **ERC721Consecutive.sol** there is`_mintConsecutive(address to, uint96 batchSize)` for minting, since it uses batch minting, it has O(n) time complexity. I propose we fully omit minting functions.

### ERC721Consecutive.sol:

```auto
function _ownerOf(uint256 tokenId) internal view virtual override returns (address) {
        address owner = super._ownerOf(tokenId);

        // If token is owned by the core, or beyond consecutive range, return base value
        if (owner != address(0) || tokenId > type(uint96).max) {
            return owner;
        }

        // Otherwise, check the token was not burned, and fetch ownership from the anchors
        // Note: no need for safe cast, we know that tokenId <= type(uint96).max
        return _sequentialBurn.get(tokenId) ? address(0) : address(_sequentialOwnership.lowerLookup(uint96(tokenId)));
    }
```

### ERC721FancyMint(my proposal):

```auto
function _ownerOf(uint256 tokenId) internal view virtual returns (address) {
        address owner = _owners[tokenId];
        if (owner == address(0) && (tokenId < _maxSupply)) {
            return _preOwner;
        }
        return owner;
    }
```

this way we do not need any operation.

---

Also this abstraction is extendable to IERC721Enumerable with [ERC721FancyMintEnumarable.sol](https://github.com/shypink/Fancy_Project_Premium/blob/main/ERC721FancyMintEnumRef.sol) that ERC721Consecutive.sol in current implementation can’t be.

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
            return preIndex(index);\\  a view function that handles preOwner index
        } else {
            return _ownedTokens[owner][index];
        }
    }
```

```auto
function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId
    ) internal virtual override {
        super._beforeTokenTransfer(from, to, tokenId);
        address _preOwner = ERC721FancyMint.preOwner();

        if (from == address(0)) {
            //does not support minting
            revert("fromm == zero, does not support minting");
        } else if (from != to) {
            if (from == _preOwner) {
                _removeTokenFromPreOwner(tokenId);
            } else {
                _removeTokenFromOwnerEnumeration(from, tokenId);
            }
        }
        if (to == address(0)) {
            //does not support burning
            revert("to == zero, does not support burning");
        } else if (to != from) {
            if (to == _preOwner) {
                _addTokenToPreOwner(tokenId);
            } else {
                _addTokenToOwnerEnumeration(to, tokenId);
            }
        }
    }
```

---

**sciNFTist.eth** (2023-01-04):

I rather don’t change the maxSupply , and preOwner.

and this implementation is more fit toward fixed length collections.

```auto
constructor(
        string memory name_,
        string memory symbol_,
        uint256 maxSupply_,
        address preOwner_
    ) {

        require(preOwner_ != address(0), "preOwner can NOT be address(0)");
        require(0 < maxSupply_, "maxSupply_ should not be zero!");
        _name = name_;
        _symbol = symbol_;

        //@dev my proposal

        _maxSupply = maxSupply_;
        _preOwner = preOwner_;
        // blance of preOwner
        _balances[preOwner_] = maxSupply_;

        // see eip-2309 examples for batch creation
        emit ConsecutiveTransfer(0, maxSupply_ - 1, address(0), preOwner_);
    }
```

---

**xinbenlv** (2023-01-04):

Can you share with us a TX link on etherscan that actually yields zero gas cost?

---

**sciNFTist.eth** (2023-01-04):

the zero gas cost is because there is no minting function.

if you look at [EIP-721](https://eips.ethereum.org/EIPS/eip-721) there is no mint function there:

> Creation of NFTs (“minting”) and destruction of NFTs (“burning”) is not included in the specification. Your contract may implement these by other means. Please see the event documentation for your responsibilities when creating or destroying NFTs.

and “event” is:

```auto
/// @dev This emits when ownership of any NFT changes by any mechanism.
   ///  This event emits when NFTs are created (`from` == 0) and destroyed
   ///  (`to` == 0). Exception: during contract creation, any number of NFTs
   ///  may be created and assigned without emitting Transfer. At the time of
   ///  any transfer, the approved address for that NFT (if any) is reset to none.
   event Transfer(address indexed _from, address indexed _to, uint256 indexed _tokenId);
```

and [EIP-2309](https://eips.ethereum.org/EIPS/eip-2309) introduced a new event that make batch token creation more efficiently.

> Batch token creation
> emit ConsecutiveTransfer(1, 100000, address(0), toAddress);

In my implementation, I simply use no operation or state change. I only notify applications, with an consecutiveTransfer event:

`emit ConsecutiveTransfer(0, maxSupply_ - 1, address(0), preOwner_);`

and it’s done in the constructor at deployment.

please see the transaction log.

deployment tx:

https://etherscan.io/tx/0x59537f3f817a7e621462afe16e6435032e9c63a66169a031e559af671363a6f2#eventlog

---

**xinbenlv** (2023-01-04):

If what you propose is “mint during contract creation and using 2309 to do it ‘cheaper’ for large amount or use a fallback owner, and outside of constructor I don’t do minting so I don’t pay for TX I didn’t incur” then ok by but that’s very limited in usebility for any real use case I am afraid. It doesn’t create any benefit avoiding gas cost IMHO

There title of this thread might better update to “mint only during constructor plus a default owner saves some gas if you don’t mint at all after contract creation.”, I guess?

Mint by its definition involves creation of token and can happen in any stage of a contract. Combining the minting process with constructor  doesn’t actually make the cost zero, it only bundles them together. Reading the title I was anticipating some other magic moves like gas banking or return of gas from existing balance of a contract.

---

**sciNFTist.eth** (2023-01-04):

about the title you are right, I have posted this idea with different titles but they couldn’t spark the conversation. hence “0 gwei”

the thing that I’m trying to address here is aimed for collections that has maxSupply and their minting function become deactivated after minting period. In my observation respectable portion of NFT ecosystem are these collection.

I think the part that this implementation become useful is:

1. when people want to lazy mint NFT their collection is only available in one market place.
2. If they decided to use ERC721Consecutive.sol they loose the lack of IERC721Enumarable compatibility.

I really enjoyed the new abstraction of _ownerOf in **ERC721Consecutive.sol** and I changed it a little.

since some Dapps are dependent on `tokenOfOwnerByIndex(address owner, uint256 index)`,It’s possible to use ERC721FancyMintEnumerable extension,` I think this Implementation would be useful in some cases

---

**xinbenlv** (2023-01-04):

> but they couldn’t spark the conversation. hence “0 gwei”

I couldn’t believe, *click-bating*, this evil thing, is now in the sacred land of Ethereum-Magician, how dare you, my friend! [@sciNFTist.eth](/u/scinftist.eth)

(just kidding. well-played)

---

**Pandapip1** (2023-01-04):

Actually, they’re not wrong in saying that it’s gasless minting. The *marginal* cost of minting an NFT is exactly zero. The fixed cost is (roughly from my estimates) 3000.

---

**cybertelx** (2023-01-04):

seems similar to https://erc721a.org

---

**sciNFTist.eth** (2023-01-05):

there is a pros and cons between these two implementation:

1. after deployment ECR721A maintain the mint & batch minting functionality that ERC721FancyMint does not.
2. ERC721FancyMint has an extension ERC721FancyMintEnumarabe  that give the contract full compatibility with IERC721Enumarable interface, but ERC721A does not have IERC721Enumerable interface.

PS: ERC721A has an [ERC721AQueryable.sol](https://github.com/chiru-labs/ERC721A/blob/main/contracts/extensions/ERC721AQueryable.sol) extension that  has an interface like this:

```auto
 /**
     * @dev Returns an array of token IDs owned by `owner`.
     *
     * This function scans the ownership mapping and is O(`totalSupply`) in complexity.
     * It is meant to be called off-chain.
     *
     * See {ERC721AQueryable-tokensOfOwnerIn} for splitting the scan into
     * multiple smaller scans if the collection is large enough to cause
     * an out-of-gas error (10K collections should be fine).
     */
    function tokensOfOwner(address owner) external view virtual override returns (uint256[] memory) {}
```

and another interface:

```auto
/**
     * @dev Returns an array of token IDs owned by `owner`,
     * in the range [`start`, `stop`)
     * (i.e. `start <= tokenId < stop`).
     *
     * This function allows for tokens to be queried if the collection
     * grows too big for a single call of {ERC721AQueryable-tokensOfOwner}.
     *
     * Requirements:
     *
     * - `start < stop`
     */
    function tokensOfOwnerIn(
        address owner,
        uint256 start,
        uint256 stop
    ) external view virtual override returns (uint256[] memory) {}
```

and it has time complexity of `O(totalSupply)` but tokenOfOwnerByIndex(address owner, uint256 index) in ERC721FancyMintEnumarable has `O(1)` time complexity.

---

**karmacoma** (2023-01-09):

> and as I promised they all minted with no transaction

this is of course nonsense, but for anyone else who might be confused the minting happens in the [deploy transaction](https://etherscan.io/tx/0x59537f3f817a7e621462afe16e6435032e9c63a66169a031e559af671363a6f2#eventlog)

---

**sciNFTist.eth** (2023-01-10):

yeah your right, the title was confusing so I’ve changed it,

thank you for pointing that out.

but the main focus of this implementation. is batch minting and while maintaining **enumerability** with complexity of O(1). mainly `tokenOfOwnerByIndex(address owner, uint256 index)` from ERC721Enumerable.

a quick comparison:

openZeppelin :[ERC721Consecutive.sol](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/extensions/ERC721Consecutive.sol)

```auto
abstract contract ERC721Consecutive is IERC2309, ERC721
```

chiru-lab: [ERC721AQueryable.sol](https://github.com/chiru-labs/ERC721A/blob/main/contracts/extensions/ERC721AQueryable.sol)

```auto
abstract contract ERC721AQueryable is ERC721A, IERC721AQueryable
```

[ERC721FancyMintEnumerable](https://github.com/shypink/EIP-draft_ERC721FancyMint/tree/master/assets/eip-draft_FancyMint/FancyEnumerable_extension)

```auto
contract ERC721FancyMintEnum is ERC721FancyMint, IERC721Enumerable
```

If you could provide your feedback on ERC721FancyMintEnumerable, I’ll be glad.

PS: ERC721AQueryable has an interface like `function tokensOfOwner(address owner)` this that has O(collectionSize) time complexity.

```auto
 /**
     * @dev Returns an array of token IDs owned by `owner`.
     *
     * This function scans the ownership mapping and is O(`totalSupply`) in complexity.
     * It is meant to be called off-chain.
     *
     * See {ERC721AQueryable-tokensOfOwnerIn} for splitting the scan into
     * multiple smaller scans if the collection is large enough to cause
     * an out-of-gas error (10K collections should be fine).
     */
    function tokensOfOwner(address owner) external view returns (uint256[] memory);
}

```

thank you for reading this.

---

**karmacoma** (2023-01-10):

thanks for updating the title of your post, it’s more factual now

