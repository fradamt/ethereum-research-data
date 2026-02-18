---
source: magicians
topic_id: 8572
title: "EIP4907: ERC-721 User And Expires Extension"
author: LanceSnow
date: "2022-03-11"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip4907-erc-721-user-and-expires-extension/8572
views: 12970
likes: 35
posts_count: 41
---

# EIP4907: ERC-721 User And Expires Extension

---

## eip:
title: ERC-721 User And Expires Extension
description: Standard interface extension for ERC-721 user and expires.
author: EmojiDAO ()
discussions-to:
status: Final
type:
category (*only required for Standards Track):
created: 2022-03-11
requires (*optional): <EIP 165 721>

This standard proposes an extension to ERC721 Non-Fungible Tokens (NFTs) to separate NFT usage rights.

## Abstract

This standard is an extension of ERC721. It proposes an additional role **user** and a valid duration indicator **expires**. It allows users and developers manage the use right more simple and efficient.

## Motivation

Some NFTs have certain utilities. In-game NFTs can be used to play, virtual land can be used to build scenes, music NFT can be used to enjoy , etc. But in some cases, the owner and user may not be the same person. People may invest in an NFT with utility, but they may not have time or ability to use it. So separating use right from ownership makes a lot of sense.

Nowadays, many NFTs are managed by adding the role of **controller/operator** . People in  these roles can perform specific usage actions but can’t approve or transfer the NFT like an owner. If owner plans to set someone as **controller/operator** for a certain period of time, owner needs to submit two on-chain transactions, at the start time and the end time.

It is conceivable that with the further expansion of NFT application, the problem of usage rights management will become more common, so it is necessary to establish a unified standard to facilitate collaboration among all applications.

By adding **user**, it enables multiple protocols to integrate and build on top of usage rights, while **expires** facilitates automatic ending of each usage without second transaction on chain.

## Specification

This standard proposes two user roles: the **Owner**, and the **User**.Their rights are as follows:

- An Owner has the right to:

Transfer the Owner role
- Transfer the User role
- A User has the right to:

use NFT

## Interface

```solidity
// Logged when the user of a token assigns a new user or updates expires
event UpdateUser(uint256 indexed tokenId, address indexed user, uint64 expires);

// set the user role and expires of a token
function setUser(uint256 tokenId, address user, uint64 expires) external ;

// get the user of a token
function userOf(uint256 tokenId) external view returns(address);

// get the user expires of a token
function userExpires(uint256 tokenId) external view returns(uint256);
```

## Rationale

Many developers are trying to develop based on the NFT utility, and some of them have added roles already, but there are some key problems need to be solved.  The advantages of this standard are below.

### Clear Permissions Management

Usage rights are part of ownership, so **owner** can modify **user** at any time, while **user** is only granted some specific permissions, such as **user** usually does not have permission to make permanent changes to NFT’s Metadata.

NFTs may be used in multiple applications, and adding the user role to  NFTs  makes it easier for the application to make special grants of rights.

### Simple On-chain Time Management

Most NFTs do not take into account the expiration time even though the role of the user is added, resulting in the need for the owner to manually submit on-chain transaction to cancel the user rights, which does not allow accurate on-chain management of the use time and will waste gas.

The usage right often corresponds to a specific time, such as deploying scenes on land, renting game props, etc. Therefore, it can reduce the on-chain transactions and save gas with **expires**.

### Easy Third-Party Integration

The standard makes it easier for third-party protocols to manage NFT usage rights without permission from the NFT issuer or the NFT application.

## Backwards Compatibility

As mentioned in the specifications section, this standard can be fully ERC721 compatible by adding an extension function set.

In addition, new functions introduced in this standard have many similarities with the existing functions in ERC721. This allows developers to easily adopt the standard quickly.

## Test Cases

When running the tests, you need to create a test network :

```auto
truffle develop
nft = await ERC_DualRoles.new("ERC_DualRoles","ERC_DualRoles")
nft.mint(1,accounts[0])
nft.ownerOf(1)
nft.setUser(1,accounts[1],33203038769)
nft.userOf(1)
```

Powered by Truffle and Openzeppelin test helper.

## Reference Implementation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "./IERC_DualRoles.sol";

contract ERC_DualRoles is ERC721, IERC_DualRoles {
    struct UserInfo
    {
        address user;   // address of user role
        uint64 expires; // unix timestamp
    }

    mapping (uint256  => UserInfo) internal _users;

    constructor(string memory name_, string memory symbol_)
     ERC721(name_,symbol_)
     {
     }

    function setUser(uint256 tokenId, address user, uint64 expires) public virtual{
        require(_isApprovedOrOwner(msg.sender, tokenId),"ERC721: transfer caller is not owner nor approved");
        UserInfo storage info =  _users[tokenId];
        info.user = user;
        info.expires = expires;
        emit UpdateUser(tokenId,user,expires);
    }

    /**
    * get the user expires of a token.
    * if there is no user role of a token , it will return 0
    */
    function userExpires(uint256 tokenId) public view virtual returns(uint256){
        return _users[tokenId].expires;
    }

    /**  get the user role of a token */
    function userOf(uint256 tokenId)public view virtual returns(address){
        if( uint256(_users[tokenId].expires) >=  block.timestamp){
            return  _users[tokenId].user;
        }
        else{
            return address(0);
        }
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId
    ) internal virtual override{
        super._beforeTokenTransfer(from, to, tokenId);

        if (from != to) {
            _users[tokenId].user = address(0);
            _users[tokenId].expires = 0;
            emit UpdateUser(tokenId,address(0),0);
        }
    }

    // for test
    function mint(uint256 tokenId, address to) public {
        _mint(to, tokenId);
    }
}
```

## Security Considerations

This EIP standard can completely protect the rights of the owner, the owner can change the NFT user and use period at any time.

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## Replies

**0xanders** (2022-03-11):

## Example for rental

The following diagram demonstrates an example for the rental functionality.

[![eip](https://ethereum-magicians.org/uploads/default/optimized/2X/a/a0f102412c9f1feecbb76b841cfb72a5bf0fdf66_2_370x500.png)eip1239×1671 43.1 KB](https://ethereum-magicians.org/uploads/default/a0f102412c9f1feecbb76b841cfb72a5bf0fdf66)

Suppose Alice owns NFTs and wants to rent out a NFT, and Bob wants to lease a NFT.

1. Alice approves rental contract could transfer the NFT Alice owns.
2. Alice sends a rental listing to the rental contract.
3. Bob select a lease time, the rent is calculated according to the lease time and rental price. Bob transfer tokens as rent, rental contract transfer NTT from Alice to rental contract and set the user of the NFT to Bob, set the expires by the lease time.
4. When the lease expires, Alice can redeem the NFT from rental contract.

---

**Daniel-K-Ivanov** (2022-03-16):

Hi [@LanceSnow](/u/lancesnow)

The proposal that you’ve done makes sense, especially the `expiration` feature. I had a similar idea when working on the [EIP-4400: ERC-721 Consumable Extension](https://eips.ethereum.org/EIPS/eip-4400).

---

**Daniel-K-Ivanov** (2022-03-21):

Hi [@LanceSnow](/u/lancesnow)

Since your proposed EIP is very similar to the already approved and in draft state [EIP-4400: ERC-721 Consumable Extension](https://eips.ethereum.org/EIPS/eip-4400), do you want to collaborate and update EIP4400 with your expiry suggestion?

---

**ShrugNewton** (2022-04-18):

Hey Daniel, glad to buidl the NFT rental market together.

Just checked EIP-4400, it doesn’t have `expires` function, which brings the problem of multi-submitting on-chain transactions and wasting of gas.

Would love to collaborate, let’s discuss it!

Shrug

Double Protocol

---

**miltonwg** (2022-05-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lancesnow/48/5600_2.png) LanceSnow:

> This EIP standard can completely protect the rights of the owner, the owner can change the NFT user and use period at any time.

Hey! Good proposal.

One concern I have is related to this Security Consideration.

If the owner has the right to change the user at any time, wouldn’t that be a threat for, let’s day, rental contracts? (or similar).

Shouldn’t there be the expiration time the one that allows/disallows that right?

I understand that if the expiration time is mistakenly set you could never get your NFT user right back. Is that your rationale for this decision?

Thanks!

---

**ShrugNewton** (2022-05-06):

Hey, thx for the question.

In fact, the owner can always change the user and expires to prevent the situation you described.

When leasing, the owner needs to transfer the NFT to the rental contract, and then the rental contract will become the owner to set the renter and the expires.

---

**miltonwg** (2022-05-06):

Thanks for the answer!

Wouldn’t it be better and safer for users to avoid transferring the NFT to the rental contract?

And just approving the rental contract to change “user” role when rented?

thx

---

**ShrugNewton** (2022-05-09):

But if so, the owner sets the renter to one of his own addresses and also sets the expiration to 100 years later. At this point the owner sells the NFT to someone else, and the buyer will suffer a loss without paying attention to it.

If we do not allow the owner to be transferred in the case of the user is valid, it will be different from the common transfer logic and easy to cause confusion.

THX

---

**miltonwg** (2022-05-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shrugnewton/48/5884_2.png) ShrugNewton:

> But if so, the owner sets the renter to one of his own addresses and also sets the expiration to 100 years later. At this point the owner sells the NFT to someone else, and the buyer will suffer a loss without paying attention to it.

I think this is prevented with your implementation here, right?

https://github.com/ethereum/EIPs/blob/master/assets/eip-4907/contracts/ERC4907.sol#L67

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shrugnewton/48/5884_2.png) ShrugNewton:

> If we do not allow the owner to be transferred in the case of the user is valid, it will be different from the common transfer logic and easy to cause confusion.

Anyway, I get this point. It may be something to work out in another way.

Thanks.

---

**MissieBish** (2022-05-17):

Great idea, I had a similar one recently in an effort to develop a rental protocol. There is 2 things I’d like to mention:

1. Maybe the scope can include erc1155, which would benefit from this proposal just as much as erc721.
2. The security issues regarding the end date until which a user is set can be handled at the lease contract level, which has the added benefit of making a lease more trustless.

Can’t wait to see this standard broadly accepted, it will open a whole new segment of decentralised finance.

---

**0xG** (2022-06-11):

Hi there!

Early this year I built a proof of concept for a lendable/rentable token and the core idea is close to what is being discussed in this EIP. You can find the source code on [etherscan](https://etherscan.io/address/0x39fc977438febfac1d8fbb96599881712adf40dc)

I just wanted to chime in and share some suggestions.

I would rename `user` to `holder` - it is more self descriptive. I would also rename `userExpire` to `expiresOf` for consistency (since they both take a `tokenId`).

`expires` could be `0` for lending and `> 0` for rentals etc - this way you can check against `block.timestamp` and use that as a way to allow the owner to update the `holder`. Specifically when `expires` is `0` they can update the `holder` at any time. Otherwise `block.timestamp` must be `> expires`.

It would be great to think of a mechanism that would enable sub-lending etc. (holder lends to another holder within `expires` timeframe). There are plenty of real life applications for this behavior.

Finally it would be great if we could figure out:

1. A way to have the ownership check in the token contract - transferring the NFT to the marketplace is sub optimal
2. A method to lookup the ownership status of a token i.e. a method that returns (address owner, address holder, uint expires) - this is not super important as you can call holderOf and expiresOf

---

**mipicdev** (2022-06-13):

Hey,

Great EIP! Like [0xG](https://ethereum-magicians.org/u/0xG), I have a similar suggestion regarding the `user`.

In my opinion `user` is too general, because the `owner` may use an NFT and then he is also the `user`. Therefore I’d suggest to rename it to `possessor`.

Here’s a good explanation: “For example, an owner of a car could lend it to someone else to drive. That driver would then possess the car. However, the owner does not give up ownership simply by lending the car to someone else.” (source: [Possession versus Ownership legal definition of Possession versus Ownership](https://legal-dictionary.thefreedictionary.com/Possession+versus+Ownership))

---

**CarlosTM** (2022-06-28):

Hi Team,

I liked the proposal, but I have a suggestion:

Add a new function to renew the loan (NewExpiresOf) and keep the ExpiresOf to check how long the first date lasted for the new date, this could be a new condition to allow interest in the future.

---

**TimDaub** (2022-07-09):

This standard caught my attention as separating users and owners could help me make progress on implementing Harberger taxes and self-assessed pricing for NFTs. I’ve started implementing it for libharberger here: [Attempt ERC4907 integration by TimDaub · Pull Request #38 · rugpullindex/libharberger · GitHub](https://github.com/rugpullindex/libharberger/pull/38) any help integrating or feedback is welcome!

---

**TimDaub** (2022-07-09):

It’s a shame that the authors of this standard didn’t wait a bit longer before flagging it as final as I’m noticing slight inconsistencies with the surrounding ecosystem.

E.g. EIP-721 which this contract aspires to be compatible with has a similar function to `function userOf(uint256 tokenId)` but in case the `tokenId` doesn’t exist, it throws. See OZ’s implementation. So it is inconsistent.

[![Screenshot 2022-07-09 at 19.10.03](https://ethereum-magicians.org/uploads/default/optimized/2X/c/c37fc699f23891087880964a567c2557791c3539_2_690x131.png)Screenshot 2022-07-09 at 19.10.031988×378 136 KB](https://ethereum-magicians.org/uploads/default/c37fc699f23891087880964a567c2557791c3539)

EIP-4907, however, made the odd choice of returning the zero address as a signal, which I judge as a bad decision given that I conceptually see `function ownerOf` to be very similar to `function userOf`.

[![Screenshot 2022-07-09 at 19.12.18](https://ethereum-magicians.org/uploads/default/optimized/2X/3/3e978a2ed037a841bab514fd399df418e23f8963_2_690x198.jpeg)Screenshot 2022-07-09 at 19.12.181942×560 172 KB](https://ethereum-magicians.org/uploads/default/3e978a2ed037a841bab514fd399df418e23f8963)

And before someone misunderstands: 4907 mandates returning the zero address in the standard and 721 mandates throwing so these are NOT implementation details, they are interface inconsistencies!

eip-721.md

```auto
    /// @notice Find the owner of an NFT
    /// @dev NFTs assigned to zero address are considered invalid, and queries
    ///  about them do throw.
    /// @param _tokenId The identifier for an NFT
    /// @return The address of the owner of the NFT
    function ownerOf(uint256 _tokenId) external view returns (address);
```

eip-4907.md

```auto
    /// @notice Get the user address of an NFT
    /// @dev The zero address indicates that there is no user or the user is expired
    /// @param tokenId The NFT to get the user address for
    /// @return The user address for this NFT
    function userOf(uint256 tokenId) external view returns(address);
```

---

**TimDaub** (2022-07-09):

Cleaned up trailing white space, formatting and repackaged ERC4907 as a foundry package here: [GitHub - rugpullindex/ERC4907: Reference Implementation of EIP-4907 "Rental NFT, ERC-721 User And Expires Extension"](https://github.com/rugpullindex/ERC4907)

---

**0xanders** (2022-07-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/carlostm/48/6450_2.png) CarlosTM:

> Add a new function to renew the loan (NewExpiresOf) and keep the ExpiresOf to check how long the first date lasted for the new date, this could be a new condition to allow interest in the future.

Thanks for your feedback. Because the status of ERC-4907 is Final, you could propose a new EIP as  extension of  ERC-4907 to add this new function.

---

**wighawag** (2022-07-17):

Hi, thanks for your work on this EIP to allow the rental of NFT while keeping ownership flexibility

This is something I have been working on in the past and I actually got my own proposal which in my opinion offers significant benefits over the one proposed here. I already have a repo exploring the idea in great detail, see here: [GitHub - wighawag/erc721-lease: A contract to manage lease of NFT](https://github.com/wighawag/erc721-lease)

I do not want to hijack the discussion here and so I also created a topic to discuss the proposal on its own here: [ERC721 Lease: allowing owner to rent NFT to other](https://ethereum-magicians.org/t/erc721-lease-allowing-owner-to-rent-nft-to-other/9965)

To recapitulate, the main difference with EIP-4907 is that my proposal

- work with all ERC721, past, present and future
- does not need to get implemented in the token contract
- is completely generic: can implement any kind of contract between the user and owner.
- 's rental representation is itself an ERC721, so no extra work to get it working with existing infrastructure or tooling
- puts users (lease owners) and NFT owners on the same footing. EIP-4907 on the other end does not protect the “users” in any way as the owner can reclaim at any time and thus does not establish a fair ground for owner/user agreement

The main pain point I see for EIP-4907 is that “usership” expiry is not enforced in any way and NFT owner has full power. This takes a political stance on the matter of ownership vs rental rights while such a system should be as fair as possible to allow user and owner to set their own term.

---

**MaestroKongrio** (2022-07-19):

From a business and legal point of view, handling the ownership of any asset is a problem solved by ancient romans lawyers. Basically, you need to handle 3 properties:

- Who is the owner of an assets, basically who is able to transfer the ownership of the asset, and by default setting is also the owner of any other rigths.
- Who can use the asset. For instance, the one who lives on a rented house
- Who can take the benefits from the asset (romans call this ius fruendi). Using the same rented house example, the landlord of the house is the one who owns this right.
This way of modeling this has worked over 2.000 years… honestly I doubt any one in the crypto world can make something better.

---

**DOBBYl1** (2022-08-23):

I will be happy to chat more. Please check this out: → [EIP-tbd Rental & Delegation NFT - ERC-721 Extension](https://ethereum-magicians.org/t/eip-tbd-rental-delegation-nft-erc-721-extension/10441)


*(20 more replies not shown)*
