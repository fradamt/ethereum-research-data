---
source: magicians
topic_id: 10282
title: Enable Interactions among NFTs across virtual worlds
author: Hectorzh
date: "2022-08-08"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/enable-interactions-among-nfts-across-virtual-worlds/10282
views: 641
likes: 0
posts_count: 1
---

# Enable Interactions among NFTs across virtual worlds

## Abstract

This standard applies to the outcome of interactions among NFTs with predefined metadata. By applying this standard, NFTs across games can be interacted, emulating how things are interacted in real world. The interactive properties of NFTs are transferable among games/metaverse. When the interaction property is developed once, the NFTs can be interacted across games. This will encourage NFT play and thus enhance user experiences in games/metaverses in Ethereum ecosystem.

For example, in a virtual world of game or metaverse, if an avatar uses a sword to slash a tree, the later should be cut down. This use case can be done by interaction properties, when the sword has predefined property of “cut” and the tree has predefined property of “slashable”. When the sword and the tree meet, the property of “cut” of sword will trigger the property of “slashable” of tree, which then is slashed down. The scene will show the tree is cut down. Taking an example of Decentraland and Roblox, a sword with “cut” property can originally exist in Decentraland and be brought to Rolox by an avatar, where there is a tree with “slashable” property. The sword from Decentralzand can cut the tree in Roblox down.

With the use of NFTs across game flourishing, NFT designers are expected to manage the interactions of NFTs simpler and more efficient, while NFTs should be interacted across multiple games or metaverses.

## Motivation

This proposal is for interaction usage of NFTs in virtual worlds. Now users are expected to play with NFTs instead of just investing. Like in real world, one thing should have effects on another. You reach out your hands to your friend, and your friend reach out hands as well for a shake. You throw a ball to the television and it is broken. You put mud into kiln to make brick…So do things simulate in game or metaverse. With the increasing demand of play with NFTs, the properties of these NFTs need to be transferable across games or metaverses.

Without this standard, the interactions among NFTs will be managed by developers instead of as NFT property. Thus, the NFT interactions in one game cannot reappear in another even these NFTs have been transferred to the same game.

With this standard, the interaction property of an NFT can be defined and exposed externally, while interaction outcome is from the list of URIs in metadata. The interaction from one NFT will trigger these NFTs’ reactions from the metadata, which can give rise to predefined rendering or displaying result.

Metadata Schema

{

“title”: “Asset Metadata”,

“type”: “object”,

“properties”: {

“name”: {

“type”: “string”,

“description”: “Identifies the asset type to which this NFT belongs”

},

“description”: {

“type”: “string”,

“description”: “Describes the asset to which this NFT belongs”

},

“owner”: {

“type”: “string”,

“description”: “Address of the current NFT owner. Default to solidity’s address(0).”

},

“Action”: {

“ActionName”: {

“type”: “string”.

“description”: “Describes the action name;”

},

“ActionId”: {

“type”: “number”.

“description”: “the numeric number of the action;”

},

“ImageUri”: "A URI pointing to a resource of 2D/3D file of scene or model; "

}

```
      "Action": {
              "ActionName": {
                     “type”: “string”
                     “description”: “Describes the action name;”
                      },
              "ActionId": {
                     "type": “number”.
                     “description”: “the numeric number of the action;”
                      },
      "ImageUri": "A URI pointing to a resource of 2D/3D file of scene or model; "
         }
      …
      "Action": {
              "ActionName": {
                     “type”: “string”
                     “description”: “Describes the action name;”
                      },
              "ActionId": {
                     "type": “number”.
                     “description”: “the numeric number of the action;”
                      },
      "imageUri": "A URI pointing to a resource of 2D/3D file of scene or model; "
        },
```

It is conceivable that with the further expansion of NFT application, the more common the problem of NFT interaction will have. Thus, there is a necessity to establish a standard to enable interaction among all NFTs, including those across metaverses.

## Specification

//interaction

struct interactive {

bool exist;                          //to see if the NFT exists

uint256 Id;

…

string imageUri;

}

```
//NFT
struct NFT {
    bool exist;                          //to see if the NFT exists
    uint256 tokenId;
    ...
    mapping (uint256 => interactive) interactiveBook;
}

//NFTList
struct NFTs {
    bool exist;                         //to see if the NFT exists
    ...
    mapping (uint256 => NFT) NFTBook;
}
mapping (address => NFTs) public NFTsBook;
address[] public NFTsList;

//Action List
struct NFTAction {
    bool exist;                         //To see if the action exist
    ...
    string imageUri;
}
mapping (bytes32 => NFTAction) public actionsBook;
```

function NFTInteractive(address _first, uint256 _firstId, address _second, uint256 _secondId, uint256 _Id1, uint256 _Id2) public returns (bool, string){

```
    //To detect Address
    require(_first != address(0), "first address is 0!");
    require(_second != address(0), "second address is 0!");

    NFTs storage firstNFT = NFTsBook[_first];
    if (!n.exist) {
        return (false, "");
    }

    NFT storage firstToken = firstNFT.NFTBook[_firstId];
    if (!firstToken.exist) {
        return (false, "");
    }

    NFTs storage secondNFT = NFTsBook[_second];
    if (!n.exist) {
        return (false, "");
    }

    NFT storage secondToken = secondNFT.NFTBook[_secondId];
    if (!firstToken.exist) {
        return (false, "");
    }

    interactive storage firstId = firstToken.interactiveBook[_Id1];
    if(!firstId.exist){
        return (false, "");
    }

    interactive storage secondId = secondToken.interactiveBook[_Id1];
    if(!secondId.exist){
        return (false, "");
    }

    //To Calculate Actionid
    bytes32 actionId = keccak256(firstId, secondId);
    NFTAction storage action = actionsBook[actionId];
    if(!action.exist) {
        return (false, "")
    }
    return （true, action.imageUri);
}
```

## Rationale

Many developers are trying to develop in-game NFT utility and some have already had interactions between NFTs, but there are some key problems need to be solved before the NFT interactions are managed simpler and more efficient. The advantages of this standard are below.

Simple and Efficient in NFT interaction

The interaction property can be exposed to user for editing. For example, interaction property of ‘slashable’ tree can be open to NFT designers.

Here is a simple example of a tree with its metadata for an interaction property of ‘slashable:

Example of the tree:

{

“name”: “A Slashable Tree”,

“description”: " A tree belongs to plant category and can be slashed down ",

“owner”: “…”,

///The space that owns the tree,

“Normal”: {

“NormalTree”: {

“Description”: “A normal tree;”,

“ActionID”: “1”

“ImageUri”: “ipfs://…”

}

}

“Slashed”: {

“SlashedTree”: {

“Description”: “A tree is slashed down;”,

“ActionID”: “2”

“ImageUri”: “ipfs://…”

}

}

Across game NFT play to enhance user experience

The NFTs with this standard can be played across games/metaverses. A player in one game has an NFT which can be used in another game/metaverse, and has interaction with another NFT with pre-defined property. This will enhance user experiences and encourage NFT play in Ethereum ecosystem, giving a real-life experience in virtual world.

## Backwards Compatibility

All EIPs that introduce backwards incompatibilities must include a section describing these incompatibilities and their severity. The EIP must explain how the author proposes to deal with these incompatibilities. EIP submissions without a sufficient backwards compatibility treatise may be rejected outright.

The proposal is fully compatible with both EIP-721 and EIP-1155. Third-party applications that don’t support this proposal will still be able to use the original metadata for each NFT.

## Test Cases

Test cases for an implementation are mandatory for EIPs that are affecting consensus changes.  If the test suite is too large to reasonably be included inline, then consider adding it as one or more files in `../assets/eip-####/`.

//An Interaction Example of Sword Slashing a Tree

//tree belongs to space; sword belongs to avatar;

struct interactive {

bool exist;                          //to see if the NFT exists

uint256 id;

…

string imageUri;

}

```
//NFT action mapping
struct NFT {
    bool exist;                          //to see if the NFT exists
    uint256 tokenId;
    ...
    mapping (uint256 => interactive) interactiveBook;
}

//NFTList
struct NFTs {
    bool exist;                         //To see if the NFT exists
    ...
    mapping (uint256 => NFT) NFTBook;
}
mapping (address => NFTs) public NFTsBook;
address[] public nftsList;

//ActionList
struct NFTAction {
    bool exist;                         //To see if the action exists
    ...
    string imageUri;
}
mapping (bytes32 => NFTAction) public actionsBook;
```

function NFTInteractive(address _first, uint256 _firstId, address _second, uint256 _secondId, uint256 _Id1, uint256 _Id2) public returns (bool, string){

```
    //to detect address
    require(_first != address(0), "first address is 0!");
    require(_second != address(0), "second address is 0!");

    NFTs storage firstNFT = nftsBook[_first];
    if (!n.exist) {
        return (false, "");
    }

    NFT storage firstToken = firstNFT.NFTBook[_firstId];
    if (!firstToken.exist) {
        return (false, "");
    }

    NFTs storage secondNFT = NFTsBook[_second];
    if (!n.exist) {
        return (false, "");
    }

    NFT storage secondToken = secondNFT.NFTBook[_secondId];
    if (!firstToken.exist) {
        return (false, "");
    }

    interactive storage firstId = firstToken.interactiveBook[_id1];
    if(!firstId.exist){
        return (false, "");
    }

    interactive storage secondId = secondToken.interactiveBook[_Id2];
    if(!secondId.exist){
        return (false, "");
    }

    //Calculating actionId
    bytes32 actionId = keccak256(firstId, secondId);
    NFTAction storage action = actionsBook[actionId];
    if(!action.exist) {
        return (false, "")
    }
    return （true, action.imageUri);
}
```

//Sword Slashing Tree;

//tree belongs to space; sword belongs to avatar;

function NFTInteractive(address of the avatar , uint256 sword Id, address of space, uint256 tree Id, uint256 sword actionId, uint256 tree actionId) public returns (bool, string){

```
    //To detect sword and tree address
    require(avatar address != address(0), "avatar address is 0!");
    require(space address != address(0), "space address is 0!");

    //To detect if the sword address and tree address own the NFT
    NFTs storage firstNft = nftsBook[avatar address];
    if (!n.exist) {
        return (false, "");
    }

    NFT storage firstToken = firstNFT.nftBook[swordid];
    if (!firstToken.exist) {
        return (false, "");
    }

    NFTs storage secondNFT = NFTsBook[spaceid];
    if (!n.exist) {
        return (false, "");
    }

    NFT storage secondToken = secondNFT.NFTBook[treeid];
    if (!firstToken.exist) {
        return (false, "");
    }

    //To acquire sword and tree actionId
    interactive storage firstId = firstToken.interactiveBook[sword actionId];
    if(!firstId.exist){
        return (false, "");
    }

    interactive storage secondId = secondToken.interactiveBook[tree actionId];
    if(!secondId.exist){
        return (false, "");
    }

    //To calculate sword slashing tree actionId
    bytes32 actionid = keccak256(firstId, secondId);

    //To determine sword slashing tree actionId
    NFTAction storage action = actionsBook[actionId];
    if(!action.exist) {
        return (false, "")
    }
    return （true, action.imageUri);
}
```

## Security Considerations

For some functions such as ‘destroy’ or ‘destruct’, this proposal should be used carefully. If the interactions between NFTs result in NFT destruction, the security issue should be taken seriously into consideration. One solution can be the ‘destroy’ function needs signature, and those with correct signatures can lead to destruction. There could be another form of security, such as data encryption, for example, RSA or AES.

## Copyright

Copyright and related rights waived via CC0.
