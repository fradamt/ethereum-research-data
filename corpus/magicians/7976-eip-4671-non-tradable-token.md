---
source: magicians
topic_id: 7976
title: "EIP-4671: Non-tradable Token"
author: omaraflak
date: "2022-01-13"
category: EIPs
tags: [erc, token, ntt]
url: https://ethereum-magicians.org/t/eip-4671-non-tradable-token/7976
views: 7768
likes: 34
posts_count: 43
---

# EIP-4671: Non-tradable Token

Discussion thread for: https://github.com/ethereum/EIPs/pull/4671

## Abstract

NTTs represent inherently personal possessions (material or immaterial), such as university diplomas, online training certificates, government issued documents (national id, driving licence, visa, wedding, etc.), badges, labels, and so on.

As the name implies, NTTs are not made to be traded or sold. They don’t have monetary value. They only serve as a **proof of possession**.

## Motivation

US, 2017, MIT published 111 diplomas on a blockchain. France, 2018, Carrefour multinational retail corporation used blockchain technology to certify the provenance of its chickens. South Korea, 2019, the state published 1 million driving licences on a blockchain-powered platform.

Each of them made their own smart contracts, with different implementations. We think diplomas, food labels, or driving licences are just a subset of a more general type of tokens: **non-tradable tokens**. Tokens that represent certificates or labels that were granted to you by some authority.

By providing a common interface for this type of tokens, we allow more applications to be developed and we position blockchain technology as a standard gateway for verification of personal possessions.

## Specification

A single NTT contract, is seen as representing one type of badge by one authority. For instance, one NTT contract for MIT diplomas, one NTT contract for the state driving licences, and so on…

- An address might possess multiple tokens, which are indexed.
- An authority who delivers a certificate should be in position to invalidate it. Think of driving licences or weddings. However, it cannot delete your token.
- The issuer of a token might be someone else than the contract creator.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/introspection/IERC165.sol";

interface INTT is IERC165 {
    /// @notice Count all tokens assigned to an owner
    /// @param owner Address for whom to query the balance
    /// @return Number of tokens owned by `owner`
    function balanceOf(address owner) external view returns (uint256);

    /// @notice Check if a token hasn't been invalidated
    /// @param owner Address for whom to check the token validity
    /// @param index Index of the token
    /// @return True if the token is valid, False otherwise
    function isValid(address owner, uint256 index) external view returns (bool);

    /// @notice Get the issuer of a token
    /// @param owner Address for whom to check the token issuer
    /// @param owner Index of the token
    /// @return Address of the issuer
    function issuerOf(address owner, uint256 index) external view returns (address);
}
```

### Extensions

#### Metadata

An interface allowing to add metadata linked to each token, as in ERC721.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface INTTMetadata {
    /// @return Descriptive name of the tokens in this contract
    function name() external view returns (string memory);

    /// @return An abbreviated name of the tokens in this contract
    function symbol() external view returns (string memory);

    /// @notice URI to query to get the token's metadata
    /// @param owner Address of the token's owner
    /// @param index Index of the token
    /// @return URI for the token
    function tokenURI(address owner, uint256 index) external view returns (string memory);
}
```

#### Delegation

An interface to standardize delegation rights of token minting.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface INTTDelegate {
    /// @notice Grant one-time minting right to `operator` for `owner`
    /// An allowed operator can call the function to transfer rights.
    /// @param operator Address allowed to mint a token
    /// @param owner Address for whom `operator` is allowed to mint a token
    function delegate(address operator, address owner) external;

    /// @notice Grant one-time minting right to a list of `operators` for a corresponding list of `owners`
    /// An allowed operator can call the function to transfer rights.
    /// @param operators Addresses allowed to mint
    /// @param owners Addresses for whom `operators` are allowed to mint a token
    function delegateBatch(address[] memory operators, address[] memory owners) external;

    /// @notice Mint a token. Caller must have the right to mint for the owner.
    /// @param owner Address for whom the token is minted
    function mint(address owner) external;

    /// @notice Mint tokens to multiple addresses. Caller must have the right to mint for all owners.
    /// @param owners Addresses for whom the tokens are minted
    function mintBatch(address[] memory owners) external;
}
```

## Implementation

The implementation is a bit long. You’ll find it in the PR.

## NTT for EIP ?

As a first NTT, why not create the **EIP Creator Badge** ? An NTT created by the Ethereum foundation, and attributed to EIP-standard creators ? ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=15)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./NTT.sol";

contract EIPCreatorBadge is NTT {
    constructor() NTT("EIP Creator Badge", "EIP") {}

    function giveThatManABadge(address owner) external {
        require(_isCreator(), "You must be the contract creator");
        _mint(owner);
    }

    function _baseURI() internal pure override returns (string memory) {
        return "https://eips.ethereum.org/ntt/";
    }
}
```

---

Any thoughts or comments are greatly appreciated!

## Replies

**maxareo** (2022-01-15):

In one sentence, an NTT is an NFT that can only be minted but not transferred, correct?

---

**a2468834** (2022-01-15):

> As a first NTT, why not create the EIP Creator Badge ? An NTT created by the Ethereum foundation, and attributed to EIP-standard creators ?

Curious about what does this sentence mean?

---

**paxthemax** (2022-01-15):

This is an interesting proposal, i think there are a lot of cases where tokens are informal and effectively non-transferable.

I assume that there is no need for a kind of **mandated transfer** in cases when a recipient address is compromised (private key inaccessible, stolen or lost)? Tokens have to be invalidated and re-issued? I assume implementations might want to combine this into one call to save on gas.

---

**omaraflak** (2022-01-15):

In terms of what you can do with them technically, yes. But the purpose is different.

I really like the fact that there’s no speculation involved for once. NTTs, at their core, are just a proof of possession. But that hits so many use cases! You can imagine NTTs for all sorts of achievements

(a bit like the playstation online). You can imagine a particular implementation where the tokens can be minted only if there is a consensus of a predefined set of addresses => that could be for scholarships for instance, or something less serious ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=10).

---

**omaraflak** (2022-01-15):

You can imagine that the Ethereum foundation would give a badge to all the people who contributed to create one of their standards. They would send them over mail, you would receive one, clip it on your jacket, and brag about it because only Ethereum contributors have that badge ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=10)

Since NTTs can be badges (or anything non-tradable that was given to you personally), you can make a NTT for that. If the Ethereum foundation deploys the contract I showed at the end of the post, they can do so. They’ll be able to give a badge by calling `giveThatManABadge()` (or `giveThatGirlABadge()` of course, there was a meme intended ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=10)). The address of their contract would be well-known and anyone can verify that you personally had a badge delivered by the foundation.

---

**omaraflak** (2022-01-15):

So, actually it would be nice to be able to transfer your token to another of your wallets, however it’s a bit hard to achieve since the whole point is to have non-transferable tokens ^^ Maybe if you can prove you own the other address by signing messages on something…

But then, I try to make the bridge with real world applications and it doesn’t necessarily make sense. When an authority delivers a certificate (say a diploma or driving licence) you can imagine that they wouldn’t want you to be able to change your name, or your address on the official paper.

That’s one of the reasons there are `isValid()`and `invalidate()` methods. In case:

1- Your certificate expires

2- The authority wants to take it back because of something you did

Implementations could vary a lot I guess. But the standard has minimal required methods to work (at least I tried to make it that way). I might add a `total()` method to get the total number of issued tokens.

---

**maxareo** (2022-01-15):

I suppose ERC721 can achieve the same effect by locking `transfer` and `transferFrom` functions.

---

**numtel** (2022-01-15):

How is this different than [EIP-1238](https://github.com/ethereum/EIPs/issues/1238)?

---

**omaraflak** (2022-01-18):

[@maxareo](/u/maxareo) Yes indeed it could if you modify a bit (NTT has an issuer for instance). But I don’t know if it makes sense to implement ERC721 and override transfer methods to do nothing… Seems weird.

[@numtel](/u/numtel) Thank you for pointing that to me! never saw that since I was searching for existing standards on https://eips.ethereum.org

It’s basically the same idea but it seems the author never made a proper implementation / PR. I wonder why.

---

**cyrus** (2022-01-20):

Vitalik just discussed Non-tradable tokens on the Cobie twitch stream. Talked about getting a certificate for climbing Mt. Everest.

---

**omaraflak** (2022-01-20):

Haha exactly !!

Thanks for posting this. Too bad I missed it, I hope the stream is recorded!

---

**tserg** (2022-01-21):

I tried implementing the same in Vyper, if anyone is interested: [vyper-contracts/contracts/EIP4671 at main · tserg/vyper-contracts · GitHub](https://github.com/tserg/vyper-contracts/tree/main/contracts/EIP4671)

---

**omaraflak** (2022-01-23):

Nice! Good initiative ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=10) Let’s hope a discussion starts at some point in the PR! Any of you guys know how much time it usually takes for them to review a proposal ?

---

**calvbore** (2022-01-24):

I like the idea of transfer function where the NTT must be pulled by the recipient. The recipient would have to provide a signed message from the current owner, the contract verifies the message and transfers the token to the recipient. Maybe an interface to standardize this called `INTTConsignable`?

---

**omaraflak** (2022-01-26):

That’s an interesting idea! Thank you!

I’m just afraid people would consider this as “transferable”, because you can always sign a message for someone else. But I mean, that would *almost* be the same as giving your keys away, just one time. So I think it’s a good idea! I’ll see think about how to standardise it!

---

**omaraflak** (2022-01-26):

[@tserg](/u/tserg) I’ve linked your implementation in the EIP ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=10)

---

**xzhang** (2022-01-27):

Like this idea. It is definitely useful for many use cases. As the main function of the token is to represent a transfer of trust — by minting and giving it to someone else — have you considered the name “Credential Token”?

---

**omaraflak** (2022-01-30):

I’ve updated the standard. Here’s how it is now:

```solidity
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/introspection/IERC165.sol";

interface INTT is IERC165 {
    /// Event emitted when a token `tokenId` is minted for `owner`
    event Minted(address owner, uint256 tokenId);

    /// Event emitted when token `tokenId` of `owner` is invalidated
    event Invalidated(address owner, uint256 tokenId);

    /// @notice Count all tokens assigned to an owner
    /// @param owner Address for whom to query the balance
    /// @return Number of tokens owned by `owner`
    function balanceOf(address owner) external view returns (uint256);

    /// @notice Get owner of a token
    /// @param tokenId Identifier of the token
    /// @return Address of the owner of `tokenId`
    function ownerOf(uint256 tokenId) external view returns (address);

    /// @notice Check if a token hasn't been invalidated
    /// @param tokenId Identifier of the token
    /// @return True if the token is valid, false otherwise
    function isValid(uint256 tokenId) external view returns (bool);

    /// @notice Check if an address owns a valid token in the contract
    /// @param owner Address for whom to check the ownership
    /// @return True if `owner` has a valid token, false otherwise
    function hasValid(address owner) external view returns (bool);
}
```

### Extensions

#### Metadata

An interface allowing to add metadata linked to each token, as in ERC721.

```solidity
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./INTT.sol";

interface INTTMetadata is INTT {
    /// @return Descriptive name of the tokens in this contract
    function name() external view returns (string memory);

    /// @return An abbreviated name of the tokens in this contract
    function symbol() external view returns (string memory);

    /// @notice URI to query to get the token's metadata
    /// @param tokenId Identifier of the token
    /// @return URI for the token
    function tokenURI(uint256 tokenId) external view returns (string memory);
}
```

#### Enumerable

An interface allowing to enumerate the tokens of an owner, as in ERC721.

```solidity
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./INTT.sol";

interface INTTEnumerable is INTT {
    /// @return Total number of tokens emitted by the contract
    function total() external view returns (uint256);

    /// @notice Get the tokenId of a token using its position in the owner's list
    /// @param owner Address for whom to get the token
    /// @param index Index of the token
    /// @return tokenId of the token
    function tokenOfOwnerByIndex(address owner, uint256 index) external view returns (uint256);
}
```

#### Delegation

An interface allowing delegation rights of token minting.

```solidity
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./INTT.sol";

interface INTTDelegate is INTT {
    /// @notice Grant one-time minting right to `operator` for `owner`
    /// An allowed operator can call the function to transfer rights.
    /// @param operator Address allowed to mint a token
    /// @param owner Address for whom `operator` is allowed to mint a token
    function delegate(address operator, address owner) external;

    /// @notice Grant one-time minting right to a list of `operators` for a corresponding list of `owners`
    /// An allowed operator can call the function to transfer rights.
    /// @param operators Addresses allowed to mint
    /// @param owners Addresses for whom `operators` are allowed to mint a token
    function delegateBatch(address[] memory operators, address[] memory owners) external;

    /// @notice Mint a token. Caller must have the right to mint for the owner.
    /// @param owner Address for whom the token is minted
    function mint(address owner) external;

    /// @notice Mint tokens to multiple addresses. Caller must have the right to mint for all owners.
    /// @param owners Addresses for whom the tokens are minted
    function mintBatch(address[] memory owners) external;

    /// @notice Get the issuer of a token
    /// @param tokenId Identifier of the token
    /// @return Address who minted `tokenId`
    function issuerOf(uint256 tokenId) external view returns (address);
}
```

#### Consensus

An interface allowing minting/invalidation of tokens based on a consensus of a predefined set of addresses.

```solidity
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./INTT.sol";

interface INTTConsensus is INTT {
    /// @notice Get voters addresses for this consensus contract
    /// @return Addresses of the voters
    function voters() external view returns (address[] memory);

    /// @notice Cast a vote to mint a token for a specific address
    /// @param owner Address for whom to mint the token
    function approveMint(address owner) external;

    /// @notice Cast a vote to invalidate a specific token
    /// @param tokenId Identifier of the token to invalidate
    function approveInvalidate(uint256 tokenId) external;
}
```

---

**omaraflak** (2022-01-31):

Vitalik himself wrote a post a few days ago talking about “soulbound NFTs”. Essentially NFTs that you cannot trade and that are assigned to you personally. He mentions POAP and Proof Of Humanity, which are great, but these are specific implementations of a more general concept that is Non-Tradable Tokens! I feel really confident about the fact that we need a standard for this now ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

https://vitalik.ca/general/2022/01/26/soulbound.html

---

**cyrus** (2022-02-01):

I do think NTTs are a major necessity. The list of applications is endless. A new one: mint a specific NTT to all the Genesis accounts. Any account holding the token can now be identified as genesis by smart contracts. Or mint a warning token to known hacker/scammer accounts.

Does the spec include a “mintTo” type function?

Also, could my idea of “NFT Entanglement” be woven into this EIP? (NTT whose ownership is atomically linked to some other transferrable token.)



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cyrus/48/10140_2.png)
    [Idea: NFT entanglement](https://ethereum-magicians.org/t/idea-nft-entanglement/8038) [EIPs](/c/eips/5)



> When you buy a car, you don’t buy the hood, and then the steering wheel and then the rear axle… you buy it all together as one piece.
> In Ethereum NFT land, there’s no option to bundle things together permanently. NFTs that should go together have to be transferred 1-by-1, which is messy, expensive and limiting.
> This idea is to create “NFT Entanglement” where a new NFT can be minted but instead of having normal transfer mechanisms, it is immediately and permanently wedded to some existing NFT, …


*(22 more replies not shown)*
