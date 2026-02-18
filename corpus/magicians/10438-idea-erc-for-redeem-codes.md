---
source: magicians
topic_id: 10438
title: "Idea: ERC for redeem codes"
author: dohzya
date: "2022-08-18"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/idea-erc-for-redeem-codes/10438
views: 924
likes: 0
posts_count: 3
---

# Idea: ERC for redeem codes

Hello,

I plan to propose an EIP for creating contracts allowing redeeming offchain codes.

I didn’t see any existing EIP related to this problematic, maybe I missed it?

In case there is none, here what I have in mind:

# Context

I want to give tokens to some people although I don’t know their address yet (they might not have one yet) so I though of using a redeem code, like the infamous online stores’ cards.

Workflow:

1. ( offchain) The contract operator generates a code.
2. ( onchain) The contract operator stores the cryptographic hash of the code, along with some information about the related token (amount, NFT’s metadata, etc.).
3. ( offchain) The contract operator gives the code to some person.
4. ( onchain) The code’s owner redeems the code and obtains the token. The code is now unusable.

This workflow can be used in multiple applications, for instance to obtain a specific NFT, or a certain amount of ERC20 coins.

# Proposal

The idea of this EIP is to provide a generic way to redeem a code, while avoid adding limitations on what is redeemed.

```auto
pragma solidity ^0.8.0;

interface Redeemable /* is ERC165 */ {

    /** This emits when a code is redeemed */
    event Redeem(uint256 _tokenId, address indexed _owner, uint256 _amount);

    /** Retrieve the token and give it to the new owner */
    function redeem(string calldata _code, address _owner) external returns (uint256 _tokenId, uint256 _amount);

    /** Checks if the code whose hash is provided is redeemable */
    function isRedeemable(bytes32 _hash) external view returns (bool);

}
```

This interface is simple but makes Redeemable focused on tokens. We could replace the specific fields `_tokendId` & `_amount` by a customizable `bytes` field (`event Redeem(address indexed _to, bytes _customData);`). It would allow redeeming other things than tokens, or maybe more than one tokens. However this definition seems too cumbersome.

The `isRedeemable` function checks if a specific code is available without having to pay any fees, but the hashing algorithm used by the contract has to be used by the caller. However, the hashing being performed by the contract, the used algorithm should be considered public knowledge.

I suppose it’s secure enough to use `keccak256`, and I doubt that using a salt would improve security.

It is possible to mint the token before or during the redeeming. However minting it before the call to `redeem` would force to select an arbitrary owner and then to transfer tokens without being this arbitrary owner, which can make some people uncomfortable ![:person_shrugging:](https://ethereum-magicians.org/images/emoji/twitter/person_shrugging.png?v=15).

# Example

Here is a complete example of a OpenZeppelin based redeemable NFT contract which allows its owner to prepare new tokens that can be later redeemed by anyone (who has the code).

**
IRedeemable.sol**

```auto
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/introspection/IERC165.sol";

interface IRedeemable is IERC165 {

    /** This emits when a code is redeemed */
    event Redeem(uint256 _tokenId, address indexed _owner, uint256 _amount);

    /** Retrieve the token and give it to the new owner */
    function redeem(string calldata _code, address _owner) external returns (uint256 _tokenId, uint256 _amount);

    /** Checks if the code whose hash is provided is redeemable */
    function isRedeemable(bytes32 _hash) external view returns (bool);

}
```

**
Redeemable.sol**

```auto
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/introspection/ERC165.sol";

import "./IRedeemable.sol";

abstract contract Redeemable is ERC165, IRedeemable {

    function supportsInterface(bytes4 _interfaceId) public view virtual override(ERC165, IERC165) returns (bool) {
        return _interfaceId == type(IRedeemable).interfaceId || super.supportsInterface(_interfaceId);
    }

}
```

**
RedeemableNFT.sol**

```auto
pragma solidity 0.8.9;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

import "./Redeemable.sol";

contract RedeemableNFT is ERC721, Ownable, Redeemable {
    mapping(bytes32 => uint256) private redeemableHashes;
    mapping(uint256 => bool) private redeemabledTokenIds;

    constructor() ERC721("Redeemable NFT", "RNFT") {}

    /** Prepare a token to be redeemed */
    function prepare(uint256 _tokenId, bytes32 _hash) public onlyOwner {
        // this first test can be removed by using a custom struct in the redeemableHashes mapping
        require(_tokenId != 0, "Can't prepare token with id 0");
        require(!_exists(_tokenId), "Can't mint an existing token");
        require(!redeemabledTokenIds[_tokenId], "Can't mint an already prepared token");
        redeemabledTokenIds[_tokenId] = true;
        redeemableHashes[_hash] = _tokenId;
    }

    function redeem(string calldata _code, address _owner) public returns (uint256, uint256) {
        bytes32 hash = _computeHash(_code);
        uint256 tokenId = redeemableHashes[hash];
        delete redeemableHashes[hash];
        if (tokenId == 0) {
            revert("No available token found for this code");
        }
        _safeMint(_owner, tokenId);
        delete redeemabledTokenIds[tokenId];
        emit Redeem(_owner, tokenId, 1);

        return (tokenId, 1);
    }

    function isRedeemable(bytes32 _hash) public view returns (bool) {
        return redeemableHashes[_hash] != 0;
    }

    function supportsInterface(bytes4 _interfaceId) public view override(ERC721, Redeemable) returns (bool) {
        return super.supportsInterface(_interfaceId);
    }

    /** Computes the hash from a received code */
    function _computeRedeemableHash(string calldata _code) internal pure returns (bytes32) {
        return keccak256(abi.encode(_code));
    }

}
```

Example of Typescript code (using ethers) which computes the hash of a given code.

```auto
import { utils } from "ethers"
import { keccak256 } from "@ethersproject/keccak256"

function computeHash(code: string): string {
  return keccak256(utils.toUtf8Bytes(code))
}
```

# Incompatibility

##

This EIP already uses the word `redeem` for its own purpose.

```auto
// from the EIP-5095's reference Implementation
event Redeem(address indexed from, address indexed to, uint256 underlyingAmount);

function redeem(uint256 principalAmount, address from, address to) public virtual returns (uint256 underlyingAmount)
```

---

I’m open to any suggestion or advice ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=15)

Thank you!

## Replies

**dohzya** (2022-08-19):

I just realized the incompatibility with EIP-5095 comes from the generic word *redeem* for specific usages.

I think this ERC could be renamed into either `RedeemCode` or `RedeemToken`.

For instance:

```auto
pragma solidity ^0.8.0;

interface RedeemableToken /* is ERC165 */ {

    /** This emits when a code is redeemed */
    event RedeemToken(uint256 _tokenId, address indexed _owner, uint256 _amount);

    /** Retrieve the token and give it to the new owner */
    function redeemToken(string calldata _code, address _owner) external returns (uint256 _tokenId, uint256 _amount);

    /** Checks if the code whose hash is provided is redeemable */
    function isRedeemableToken(bytes32 _hash) external view returns (bool);

}
```

---

**julien** (2022-09-15):

Hi [@dohzya](/u/dohzya),

I like the idea!

What use cases do you have in mind?

I’m sure it can be useful for airdrops online (through messaging apps, social networks or email) and IRL (QR codes or NFC).

You’ll probably need:

- a tool to issue fresh codes
- a UI to setup (admin)
- a UI to redeem

I was thinking of airdroping some NFTs for [Āto](https://ato.network/) early community members. I remember I told myself it would be a pain to gather everyone’s addresses…

