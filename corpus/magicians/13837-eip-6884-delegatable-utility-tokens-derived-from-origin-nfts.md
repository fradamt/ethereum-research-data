---
source: magicians
topic_id: 13837
title: "EIP-6884: Delegatable Utility Tokens Derived from Origin NFTs"
author: JB_theRedDuck
date: "2023-04-16"
category: EIPs
tags: [erc, nft, erc-721, utility, deligate]
url: https://ethereum-magicians.org/t/eip-6884-delegatable-utility-tokens-derived-from-origin-nfts/13837
views: 3511
likes: 5
posts_count: 7
---

# EIP-6884: Delegatable Utility Tokens Derived from Origin NFTs

---

## title: Delegatable Utility Tokens Derived from Origin NFTs
description: Structure and interface to increase the utility of Origin NFTs without transferring Origin NFTs
author: JB Won (), Geonwoo Shin (), Jennifer Lee (@Purplee), Bora Lee (@Violet-Bora-Lee), Taehyeong Noh ()
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2023-04-16

# EIP-6884: Delegatable Utility Tokens Derived from Origin NFTs

*Structure and interface for Delegatable Utility Tokens (DUT) for enhancing the utility of NFTs*

## Abstract

This EIP introduces the Delegatable Utility Tokens (DUT) standard, designed to enhance the utility and increase usage frequency of NFTs. The standard enables anyone to freely associate arbitrary utilities with existing NFTs. The current owner of the NFT retains ownership of each assigned utility, while also having the ability to delegate individual usage rights to others for a specified duration.

## Motivation

Most ERC-721 NFTs offer limited utility, and even those with additional utilities are often underutilized.

This limitation can be attributed to the following reasons:

1. The entity providing utility to an NFT is typically the small team that created the project or, at best, a tiny subset of the NFT holders.
2. The owner of an NFT cannot fully exploit the potential of all utilities, even if the NFT has a sufficient number of them.

A single NFT user can only utilize it for a maximum of 24 hours per day, regardless of whether it has 10 or 1000 utilities.

EIP-6884 addresses these issues by proposing Delegatable Utility Tokens (DUT) standard with the following characteristics:

1. Anyone can permissionlessly link a DUT to an existing ERC-721 NFT (Origin NFT) and grant that NFT an on-chain, certifiable utility.
2. The DUT standard separates the owner (Origin NFT owner) from the user. The owner of the Origin NFT can delegate the usage rights of each DUTs to different users for an arbitrary period of time, if desired.
3. Ownership of each DUT token is always tied to the current owner of the Origin NFT. As a result, if the owner of the Origin NFT changes, all DUTs will automatically be transferred to the new owner without incurring any gas fees.

How this standard(DUT) can achieve these are examined in code and Rationale below.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

**Every ERC-6884 compliant contract must implement the `ERC6884` and `ERC165` interfaces**:

```auto
pragma solidity ^0.8.0;

interface IERC6884 /* is IERC165 */ {
    /// Event emitted when a token usage right has been changed.
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);

    /// Event emitted when the approved address for a token usage right is
    /// changed or reaffirmed. The zero address indicates that there is no
    /// approved address. When a Transfer event is emitted, this also
    /// signifies that the approved address for that token usage right
    /// (if any) is reset to none.
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);

    /// Event emitted when an operator is enabled or disabled. The operator
    /// has the authority to delegate or restore the token usage rights.
    event ApprovalForAll(address indexed owner, address indexed operator, bool approved);

    /// Event emitted when the owner delegates a token usage right to a user
    /// for a specific period of time. At the end of the delegation period,
    /// the owner can regain the token usage right, or the user can restore
    /// it to the owner before the delegation period ends.
    event Delegated(address indexed owner, address indexed user, uint256 indexed tokenId, uint256 duration);

    /// Event emitted when the owner regains a token usage right that was
    /// delegated to a user.
    event Regained(uint256 indexed tokenId);

    /// Event emitted when the user restores a token usage right that was
    /// delegated.
    event Restored(uint256 indexed tokenId);

    /// @notice Returns the address of the ERC-721 contract that this contract
    ///  is based on.
    /// @return The address of the ERC-721 contract.
    function origin() external view returns (address);

    /// @notice Returns the expiration date of a token usage right.
    /// @dev The token id matches the id of the origin token.
    /// @param tokenId The identifier for a token usage right.
    /// @return The expiration date of the token usage right.
    function expiration(uint256 tokenId) external view returns (uint256);

    /// @notice Returns the number of token usage rights owned by `owner`.
    /// @dev Returns the balance of the origin token. Whether the token usage
    ///  right is delegated or not does not affect the balance at all.
    /// @param owner The address of the owner.
    /// @return The number of token usage rights that can be delegated, owned
    ///  by `owner`.
    function balanceOf(address owner) external view returns (uint256);

    /// @notice Returns the address of the owner of the token usage right.
    /// @dev Always the same as the owner of the origin token.
    /// @param tokenId The identifier for a token usage right.
    /// @return The address of the owner of the token usage right.
    function ownerOf(uint256 tokenId) external view returns (address);

    /// @notice Returns the address of the user of the token usage right.
    /// @dev The usage rights are non-transferable and can only be delegated.
    /// @param tokenId The identifier for a token usage right.
    /// @return The address of the user of the token usage right.
    function userOf(uint256 tokenId) external view returns (address);

    /// @notice Returns the address of the approved user for this token
    ///  usage right.
    /// @param tokenId The identifier for a token usage right.
    /// @return The address of the approved user for this token usage right.
    function getApproved(uint256 tokenId) external view returns (address);

    /// @notice Returns true if the operator is approved by the owner.
    /// @param owner The address of the owner.
    /// @param operator The address of the operator.
    /// @return True if the operator is approved by the owner.
    function isApprovedForAll(address owner, address operator) external view returns (bool);

    /// @notice Approves another address to use the token usage right
    ///  on behalf of the caller.
    /// @param spender The address to be approved.
    /// @param tokenId The identifier for a token usage right.
    function approve(address spender, uint256 tokenId) external;

    /// @notice Approves or disapproves the operator.
    /// @param operator The address of the operator.
    /// @param approved True if the operator is approved, false to revoke
    ///  approval.
    function setApprovalForAll(address operator, bool approved) external;

    /// @notice Delegates a token usage right from owner to new user.
    /// @dev Only the owner of the token usage right can delegate it.
    /// @param user The address of the new user.
    /// @param tokenId The identifier for a token usage right.
    /// @param duration The duration of the delegation in seconds.
    function delegate(address user, uint256 tokenId, uint256 duration) external;

    /// @notice Regains a token usage right from user to owner.
    /// @dev The token usage right can only be regained if the delegation
    ///  period has ended.
    /// @param tokenId The identifier for a token usage right.
    function regain(uint256 tokenId) external;

    /// @notice Restores a token usage right from user to owner.
    /// @dev User can restore the token usage right before the delegation
    ///  period ends.
    /// @param tokenId The identifier for a token usage right.
    function restore(uint256 tokenId) external;
}

interface ERC165 {
    /// @notice Query if a contract implements an interface
    /// @param interfaceID The interface identifier, as specified in ERC-165
    /// @dev Interface identification is specified in ERC-165. This function
    ///  uses less than 30,000 gas.
    /// @return `true` if the contract implements `interfaceID` and
    ///  `interfaceID` is not 0xffffffff, `false` otherwise
    function supportsInterface(bytes4 interfaceID) external view returns (bool);
}
```

### Metadata

The **metadata extension** is OPTIONAL for ERC-6884 smart contracts. This allows your smart contract to be interrogated for its name and for details about the assets which your utility represent.

```auto
interface ERC6884Metadata /* is ECR6884 */ {
    /// @notice A descriptive name for a collection of Tokens in this contract
    function name() external view returns (string _name);

    /// @notice An abbreviated name for Tokens in this contract
    function symbol() external view returns (string _symbol);

    /// @notice A distinct Uniform Resource Identifier (URI) for a given asset.
    /// @dev Throws if `_tokenId` is not a valid NFT. URIs are defined in RFC
    ///  3986. The URI may point to a JSON file that conforms to the "ERC-721
    ///  Metadata JSON Schema".
    function tokenURI(uint256 _tokenId) external view returns (string);
}

```

The EIP-6884 Metadata JSON schema follows the same specifications as the metadata schema used in ERC-721.

```auto
{
    "title": "Asset Metadata",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Identifies the asset to which this Token represents"
        },
        "description": {
            "type": "string",
            "description": "Describes the asset to which this Token represents"
        },
        "image": {
            "type": "string",
            "description": "A URI pointing to a resource with mime type image/* representing the asset to which this NFT represents. Consider making any images at a width between 320 and 1080 pixels and aspect ratio between 1.91:1 and 4:5 inclusive."
        }
    }
}
```

## Rationale

NFTs are valuable assets, and moving them can be very risky. It’s also risky to try to increase their utility by locking them to a specific contract. We’ve come up with a simple way to enhance utility without moving NFTs.

The utility of an NFT influences its value. If the utility can be sold, the NFT’s value might become diluted. As a result, we have designed the utility to be temporarily delegated only, ensuring that the NFT’s value remains undiluted. Our standard enables the creation of a wide variety of utilities, allowing many users to enjoy them through delegation without having to buy the Origin ERC-721 NFT itself.

**Why didn’t this standard inherit the ERC-721 contract?**

This is not a token standard that extends ERC-721, but rather a standard for tokens that grant utility to existing NFTs.

ERC-721 has transfer functions, which allow owners to sell their NFTs. However, tokens in this standard cannot be sold, only delegated. Instead of inheriting the ERC-721 contract and reverting all transfer functions, we believe that proposing a new standard is a cleaner approach.

**Owners and Users**

In this standard, there are owners and users. The owner is the account that owns the Delegatable Utility Token (DUT), and the user is the account that has usage rights to the DUT.

The `ownerOf` function always returns the holder of the origin token, eliminating the need for a minting process (see **no minting process**). The `userOf` function has two cases:

1. If the usage right is not delegated: the owner is returned.
2. If the usage right is delegated: the delegated user is returned.

**Balance**

The balance represents ownership (unrelated to usage rights), so the balance of the original token is always returned. As a result, this contract does not require a state variable associated with the balance.

**No minting process**

Since the `ownerOf` function always returns the current owner of the origin NFT, owners can delegate usage rights to a new user without any minting.

**Delegation process**

The delegation process is accomplished through three functions:

1. delegate: Allows the owner to delegate the token’s usage rights to a new user for a specific period of time.
2. regain: At the end of the delegation period, the owner can regain the usage rights.
3. restore: Delegated users have an option to restore the delegated usage rights to owner before its expiration.

**Approval**

There might be dApps build based on supply and demand for usage rights, facilitated by this delegation process.

## Test Cases

Test cases are included in [test.js](https://eips.ethereum.org/assets/eip-6884/test/test.js).

Run:

```auto
➜ cd assets/eip-6884
➜ yarn instsall
➜ yarn hardhat test test/test.js
```

## Reference Implementation

See [ERC6884.sol](https://eips.ethereum.org/assets/eip-6884/contracts/ERC6884.sol).

## Security Considerations

A buyer of an origin NFT may encounter the following malicious scenario:

Bob (0x222) places a bid to purchase Alice’s (0x111) origin NFT (0xaaa). Before accepting the bid for the origin NFT, Alice delegates a Delegatable Utility Token (DUT, 0xbbb) to a new account (0x333) for the maximum allowable duration.

As a result, Bob gains ownership of the original NFT and the DUT, but does not gain usage rights to the DUT.

This problem can be addressed in the following ways:

- Use a short duration when delegating usage rights for DUTs. This does not solve the underlying problem but allows for the restoration of usage rights more quickly.
- Utilize a validation process for the origin of NFTs during trades. For example, on platforms like OpenSea, you can use a solution like Zone to add validation checks, ensuring the integrity of usage rights.

## Copyright

Copyright and related rights waived via [CC0](https://eips.ethereum.org/LICENSE).

## Replies

**tbergmueller** (2023-04-17):

Stumbled across this while researching for an EIP we’re currently drafting (where I don’t want to solve for renting, but I want to enable it);

“Utility” for NFTs is in many dApps implemented through a low-level native token-gating approach, i.e. “Does account 0x123 possess at least one token of smart contract 0x456”. This extends to Metaverses and other virtual worlds, where renting property such as metaverse-land is a thing or at least the community wants it to become a thing.

I see the following scenario for a dApp-developer:

- Assume you have an original mother NFT contract 0xaaa and the proposed ChildERC721 contract 0xbbb.
- In mother contract 0xaaa: Assume token 1 is owned by account 0x111 and token 2 is owned by account 0x222.
- In child contract 0xbbb: Assume token 2 is rented to account 0x333
- I would argue right of usage is with account 0x111 (via original token 1) and account 0x333 (via rented token 2)

I do not see how in a dApp I’d verify on-chain which account has right of usage *from a single contract*.

- Checking for tokens in mother contract 0xaaa just provides me with ownership (implicit right of utility, as long as not rented).
- Checking for tokens in child contract 0xbbb just gives me a view on rented tokens only, but not on non-rented tokens.

I’d always need to check both and implement the rental-logic off-chain, which may then be implemented differently across “multiverses” as you put it.

Can you please elaborate how you would solve the above scenario in a dApp?

---

**sullof** (2023-04-18):

This is basically what I implemented in [GitHub - ndujaLabs/erc721subordinate: An NFT which is subordinate to a primary NFT](https://github.com/ndujaLabs/erc721subordinate)

Discussed at [ERC-721 Subordinate - #11 by sullof](https://ethereum-magicians.org/t/erc-721-subordinate/12479/11)

---

**0xdagarn** (2023-04-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tbergmueller/48/9196_2.png) tbergmueller:

> I do not see how in a dApp I’d verify on-chain which account has right of usage from a single contract.
>
>
> Checking for tokens in mother contract 0xaaa just provides me with ownership (implicit right of utility, as long as not rented).
> Checking for tokens in child contract 0xbbb just gives me a view on rented tokens only, but not on non-rented tokens.

[![KakaoTalk_Photo_2023-04-19-14-42-39](https://ethereum-magicians.org/uploads/default/optimized/2X/5/599ae2007962ffa5662860e5097bc2440b31330d_2_524x500.jpeg)KakaoTalk_Photo_2023-04-19-14-42-39960×916 102 KB](https://ethereum-magicians.org/uploads/default/599ae2007962ffa5662860e5097bc2440b31330d)

If you call the `ownerOf` function on the child token contract(`0xbbb`), we know who the ownership has, because when the child token is rented, the ownership changes.

If the question is about how to tell if it’s being rented or not, we can consider two ways:

1. make expiration a zero value when claim/giveBack. expiration == 0 → not rented, expiration > 0, → rented
2. compare the owner of the mother token and the child token. same → not rented, not same → rented

---

**tbergmueller** (2023-04-19):

Thank you that clarifies. So in any software application, I’d always call `ChildContract.ownerOf(tokenId)`, so always call the 0xbbb contract. I will never interact with the MotherContract.

I may be missing this from the code, but how is it ensured that ChildContract claims/mints each and every token from MotherContract?

In any case and suitable to use ChildContract.ownerOf only;

Why not overwrite `ChildContract.ownerOf(tokenId)`;

- Only mint/claim tokens in ChildContract, which are rented
- IF the tokenId is “available” in the ChildContract, check ownership via the ChildContract.
- OTHERWISE  return MotherContract.ownerOf(tokenId).

This would save a ton of gas, since non-rented tokens (which may be the majority?) do not need to be minted by the ChildContract.

---

**royo** (2023-04-20):

This is very close to what I had in mind with this: [ERC-5553: Representing IP and its Royalty Structure](https://eips.ethereum.org/EIPS/eip-5553)

thoughts?

---

**JB_theRedDuck** (2023-04-26):

[@tbergmueller](/u/tbergmueller) [@sullof](/u/sullof) [@royo](/u/royo)

I just updated this EIP-6884 standard (DUT) for a more detailed and intuitive explanation! I’m sure it will clear up a lot of questions after you read it again. If you have any questions after reading it, please ask them by replying. I’ll do my best to answer them ASAP!

