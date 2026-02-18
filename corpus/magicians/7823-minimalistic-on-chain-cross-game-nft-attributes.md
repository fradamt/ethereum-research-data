---
source: magicians
topic_id: 7823
title: Minimalistic on-chain cross-game NFT attributes
author: sullof
date: "2021-12-22"
category: EIPs
tags: [erc-721]
url: https://ethereum-magicians.org/t/minimalistic-on-chain-cross-game-nft-attributes/7823
views: 2397
likes: 1
posts_count: 10
---

# Minimalistic on-chain cross-game NFT attributes

A proposal to extend the ERC721 standard to save generic attributes on chain.

**UPDATE May 2023**

**Since the proposal changed completed from when this post was published, I am replacing here the initial test with a description of the most recent proposal, used in production in Mobland and other projects.**

# ERC721Attributable

A proposal for a standard approach to manage attributes on chain for NFTs

## Premise

In 2021, I proposed a standard for on-chain attributes for NFT at [GitHub - ndujaLabs/erc721playable: A implementation of MCIP-1: Multi-player On-chain NFT Attributes proposal](https://github.com/ndujaLabs/erc721playable)

It was using an array of uint8 to store generic attributes.

After a few iterations and attempts to implement it, I realized that it is unlikely that a player, for example, a game, can be okay with just storing uint8 values. It will most likely need multiple types that defy the advantages of that approach.

Investigating the possible alternatives, I concluded that the best way to have generic values is to encode them in an array of uint256, asking the player to translate them into parameters that can be understood, for example, by a marketplace.

Let’s say you have an NFT that starts in a game at level 2 but later can level up. Where do you store the info about the level? If you put it in the JSON metadata, you break one of the rules of the NFT, the immutability of the attributes (essential for collectors). The solution is to split the attributes into two categories: mutable and immutable attributes.

There are a few proposals to extend the metadata provided by JSON files (like [ERC-4906: EIP-721 Metadata Update Extension](https://eips.ethereum.org/EIPS/eip-4906)). The problem is that smart contracts can’t read dynamic parameters off-chain, which is the problem I am trying to solve here.

## Why do we need a common standard for on-chain metadata?

People talks every day about having NFTs that can be moved around games. The problem is that, despite the good intention, that is not possible in most cases. A standard NFT is not intended for it. What it misses is the flexibility necessary to allow any player out there (a game, a metaverse, whatever) to use the NFT inside a game, in total transparency, and in a shared way. The idea behind ERC721Attributable is that your NFT:

1. can be used by any game, i.e., any game access the data in the same format, encoding/decoding them for its purposes
2. only the NFT owner can authorize the game
3. only the game can modify its attributes

Point 2 is necessary because you don’t want any player adds data to your NFT. For example, a porn game can add you PfP. Maybe you don’t like it. For sure, you don’t want it if the player is involved in some criminal activity.

Point 3 is necessary because you can cheat after you authorize a game if you alter the data that the game sets. For example, in Mobland, a character can be wounded and go into a coma. If that character is not cured in the maximum allowed time, the character will die. On the market, a dead character will probably have a much lower value than a character in good health. But, right now, there is no way to get it. If the character is ERC721Attributable, that value can be stored in the NFT and be visible to anyone.

How? A marketplace like OpenSea can listen to the emitted event and record any new authorization. Then, it can query the authorized game to get the on-chain attributes of that NFT. (Of course, the game can also set off-chain dynamic attributes to make its data more broadly available.)

Point 1 is essential. The data must be stored most generically to allow cross-game maneuverability. The choice then is between uint256 and bytes32. My preference is for using big integers because it looks to be easier to play with.

When you have big integers that encode information, you just need a map based on tokenId and game address. A basic approach would be setting the data as:

```solidity
mapping(uint256 => mapping(address => uint256)) internal _tokenAttributes;
```

The problem is that a single integer may not be enough. A better solution is to have an “array” of big integers. My preferred variable would be

```solidity
mapping(uint256 => mapping(address => mapping(uint256 => uint256))) internal _tokenAttributes;
```

Regardless, the optimal data format is not central, and the choice of what to use is left to the implementation of the NFT. What is more important here is to define how the NFT (or any other asset with an ID) interfaces with the player.

## The interfaces

### IERC721Attributable - the NFT should extend it

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

/**
   @title IERC721Attributable Cross-player On-chain Attributes
    Version: 0.0.4
   ERC165 interfaceId is 0xc79cd306
   */
interface IERC721Attributable {
  /**
     @dev Emitted when the attributes for an id and a player is set.
          The function must be called by the owner of the asset to authorize a player to set
          attributes on it. The rules for that are left to the asset.

          This event is important because allows a marketplace to know that there are
          dynamic attributes set on the NFT by a specific contract (the player) so that
          the marketplace can query the player to get the attributes of the NFT in within
          the game.
   */
  event AttributesInitializedFor(uint256 indexed _id, address indexed _player);

  /**
   @dev Emitted when the attributes for an id are updated.
   */
  event AttributesUpdated(uint256 indexed _id, address indexed _player);

  /**
     @dev It returns the on-chain attributes of a specific id
       This function is called by the player, which is able to decode the uint and
       transform them in whatever is necessary for the game.
     @param _id The id of the token for whom to query the on-chain attributes
     @param _player The address of the player's contract
     @param _index The index in the array of attributes
     @return The encoded attributes of the token
   */
  function attributesOf(
    uint256 _id,
    address _player,
    uint256 _index
  ) external view returns (uint256);

  /**
     @notice Authorize a player initializing the attributes of a token to a non zero value
     @dev It must be called by the owner of the nft

       To avoid that nft owners give themselves arbitrary values, they must not
       be able to set up the values, but only to create the array that later
       will be filled by the player.

       Since by default the value in the array would be zero, the initial value
       must be a non-zero value. This way the player can see if the data are initialized
       checking that the attributesOf a certain id is != 0.

       The function must emit the AttributesInitializedFor event

     @param _id The id of the token for whom to authorize the player
     @param _player The address of the player contract
   */
  function initializeAttributesFor(uint256 _id, address _player) external;

  /**
     @notice Sets the attributes of a token after the initialization
     @dev It modifies attributes by id for a specific player. It must
       be called by the player's contract, after an NFT has been initialized.

       The owner of the NFT must not be able to update the attributes.

       It must revert if the asset is not initialized for that player (the msg.sender).

       The function must emit the AttributesUpdated event

     @param _id The id of the token for whom to change the attributes
     @param _index The index of the array where the attribute is updated
     @param _attributes The encoded attributes
   */
  function updateAttributes(
    uint256 _id,
    uint256 _index,
    uint256 _attributes
  ) external;
}

```

### IERC721AttributablePlayer - the player should extend it

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

// Author:
// Francesco Sullo

/**
   @title IERC721AttributablePlayer Player of an attributable asset
    Version: 0.0.1
   ERC165 interfaceId is 0x72261e7d
   */
interface IERC721AttributablePlayer {
  /**
    @dev returns the attributes in a readable way
    @param _asset The address of the asset played by the game
    @param _id The id of the asset
    @return A string with type of the attribute, name and value
  */
  function attributesOf(address _asset, uint256 _id) external view returns (string memory);
}

```

## Examples

In `/contracts/examples` there is an example of a token and a player.

Let’s show here just the function attributesOf in the player:

```solidity
function attributesOf(address _nft, uint256 tokenId) external override view returns (string memory) {
    uint256 _attributes = IERC721Attributable(_nft).attributesOf(tokenId, address(this), 0);
    if (_attributes != 0) {
      return
        string(
          abi.encodePacked(
            "uint8 version:",
            Strings.toString(uint8(_attributes)),
            ";uint8 level:",
            Strings.toString(uint16(_attributes >> 8)),
            ";uint32 stamina:",
            Strings.toString(uint32(_attributes >> 16)),
            ";address winner:",
            Strings.toHexString(uint160(_attributes >> 48), 20)
          )
        );
    } else {
      return "";
    }
  }
```

Calling it, a marketplace can get something like:

```auto
uint8 version:1;uint8 level:2;uint32 stamina:2436233;address winner:0x426eb88af949cd5bd8a272031badc2f80330e766
```

that can be easily transformed in a JSON like:

```JSON
{
  "version": {
    "type": "uint8",
    "value": 1
  },
  "level": {
    "type": "uint8",
    "value": 2
  },
  "stamina": {
    "type": "uint32",
    "value": 2436233
  },
  "winner": {
    "type": "address",
    "value": "0x426eb88af949cd5bd8a272031badc2f80330e766"
  }
}
```

of something like:

```JSON
{
  "attributes": [
    {
      "trait_type": "version",
      "value": 1
    },
    {
      "trait_type": "level",
      "value": 2
    },
    {
      "trait_type": "stamina",
      "value": 2436233
    },
    {
      "trait_type": "winner",
      "value": "0x426eb88af949cd5bd8a272031badc2f80330e766"
    }
  ]
}
```

Notice that the NFT does not encode anything, it is the player who knows what the data means, and encodes the data. Look at the following function in MyPlayer.sol:

```solidity
  function updateAttributesOf(
    address _nft,
    uint256 tokenId,
    TokenData memory data
  ) external {

    require(_operator != address(0) && _operator == _msgSender(),
            "Not the operator");

    uint256 attributes = uint256(data.version) |
                         (uint256(data.level) << 8) |
                         (uint256(data.stamina) << 16) |
                         (uint256(uint160(data.winner)) << 48);

    IERC721Attributable(_nft).updateAttributes(tokenId, 0, attributes);
  }
```

## Implementations

1. MOBLAND In-game Assets in-game-assets/contracts/SuperpowerNFTBase.sol at main · superpowerlabs/in-game-assets · GitHub

## Replies

**dylanetaft** (2021-12-22):

I think having an NFT token format standard for games is a neat idea as a concept.

I do not think you should be enforcing as much as you are - like a version. The version could just be an attribute described in the external JSON format if it is needed.  Could be byte 0 inside the a uint256/bytes32.

Perhaps attributes can be packed outside of Solidity, described in the JSON format, into a single uint256 or bytes32 in alignment with EVM word size.

Not sure why setting or getting attributes needs more than the token ID - like a player id.



      [github.com](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol)





####



```sol
// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts v4.4.1 (token/ERC721/ERC721.sol)

pragma solidity ^0.8.0;

import "./IERC721.sol";
import "./IERC721Receiver.sol";
import "./extensions/IERC721Metadata.sol";
import "../../utils/Address.sol";
import "../../utils/Context.sol";
import "../../utils/Strings.sol";
import "../../utils/introspection/ERC165.sol";

/**
 * @dev Implementation of https://eips.ethereum.org/EIPS/eip-721[ERC721] Non-Fungible Token Standard, including
 * the Metadata extension, but not including the Enumerable extension, which is available separately as
 * {ERC721Enumerable}.
 */
contract ERC721 is Context, ERC165, IERC721, IERC721Metadata {
    using Address for address;
```

  This file has been truncated. [show original](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol)










ERC721 tokens usually have a map of token ID to Address, given an ID you can find the owner.

Also, ERC721 implements a tokenURI method.  You might want a method dedicated to replying back with the JSON URL to describe your attributes, similar methodology?

---

**sullof** (2021-12-26):

Thanks for your comment.

There is no need for a new standard if we put data in the metadata.json since, despite the fields required by OpenSea, Enjin, etc., in that JSON file, you can already put whatever you like.

But that would not solve the issue we are trying to solve, because a purely decentralized game cannot access off-chain files. That is why we propose a uint8[31] array that can be managed with maximum freedom by games.

The version is unnecessary, and it could just be the first element of the uint8[]. Still, it is here because if a marketplace needs to understand what every field represents, they must find the information somewhere.

The idea is that any player/game could expose an API that describes what every field is. And since that can change, specifying the version of the data can be helpful. Thus said, I do not have a strong opinion about it. In Syn City, it makes sense to have info about the data version; maybe it does not make sense in other games.

About packing the info in a single bytes32 or uin256, yes, that is possible. But using a struct with an array of uint8 (or bytes1) offers the advantage that you can modify a single element of the array, spending around 1000 gas. While updating a bytes32 would cost more that 20,000 gas.

---

**dylanetaft** (2021-12-27):

An array of bytes1 actually gets padded with blank space in EVM and cosumes a lot more gas than bytes32

Correct me if I am wrong but updating one element will consume a full 32 bytes of gas when using storage due to EVM word size.

The version thing seems use case specific.  If you needed it, and another project didn’t, whatever API is used to provide definitions of properties could pull the version from your array.  Gas is so expensive on L1 and every byte is precious, that’s why I am bringing it up.  Maybe another project doesn’t maintain rolling versions for NFTs on layer 2, maybe they do rolling upgrades on them.

Gotcha - for completely on chain games.  What about a contract with a view function that returns metadata about properties, and setting the property definition contract on the game NFT?

I am interested in this just because I am also looking at making a game that uses NFTs.  If everyone starts following a convention then interopability becomes possible.

---

**sullof** (2022-01-09):

Since the array is in the struct, it will update only the specified value.

I tested it, and if you change only a single uint8, you spent a bit more that 1000 gas.

Of course, there is the cost of the standard transaction, but if you update many parameters at the same time, you end up spending much less than updating a single bytes32.

---

**sullof** (2022-01-09):

The proposal talks about an info contract that explains what any property is in [the chapter about integration with NFT marketplaces](https://github.com/ndujaLabs/erc721playable#interaction-with-nft-marketplaces) but that part is not defined yet, because it makes sense only after than this first step is supported by the community.

---

**sullof** (2022-07-02):

NOTICE: this proposal has been abandoned after trying to use it in a couple of projects because in almost every scenario uint8 values are not enough for what it is needed and when working with conversions, the cost to save the changes becomes higher because of the calculation compared with using custom struct in the contract. This kills the advantage coming for using a common structure amongst games.

---

**Christophe** (2022-07-04):

Your use case may be answered partially by [EIP-5185: NFT Updatable Metadata Extension](https://ethereum-magicians.org/t/eip-5185-nft-updatable-metadata-extension/9077) if you want to have a look.

In this case you would be able to store offchain lot’s of variable data that would be shared between chains.

---

**sullof** (2022-07-24):

I know that proposal. The problem there is that a contract cannot access the attributes, which was the primary goal of my proposal.

BTW, I am working on a different format — [GitHub - ndujaLabs/attributable: A proposal for standard attributes on chain](https://github.com/ndujalabs/attributable) — which is not incompatible with EIP-5185, since that works off-chain, while my proposal focuses on on-chain data.

---

**sullof** (2023-05-08):

Since I need to use this for a new project, I updated the initial post to hope revive the conversation.

A reason for it is that I realized that the event `AttributesUpdated(_id)` is not enough, and it should be replaced with

```auto
event AttributesUpdated(uint256 indexed _id, address indexed _player);
```

In fact, knowing that some attribute has changed without knowing the actor you made the change is not useful for whoever is listening to it.

