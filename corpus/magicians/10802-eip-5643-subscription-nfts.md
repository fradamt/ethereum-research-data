---
source: magicians
topic_id: 10802
title: EIP-5643 Subscription NFTs
author: cygaar
date: "2022-09-10"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-5643-subscription-nfts/10802
views: 12234
likes: 32
posts_count: 44
---

# EIP-5643 Subscription NFTs

## Abstract

This standard is an extension of ERC-721. It proposes an additional interface for NFTs to be used as recurring, expirable subscriptions. The interface includes functions to renew and cancel the subscription.

## Motivation

NFTs are commonly used as accounts on decentralized apps or membership passes to communities, events, and more. However, it is currently rare to see NFTs like these that have a finite expiration date. The “permanence” of the blockchain often leads to memberships that have no expiration dates and thus no required recurring payments. However, for many real-world applications, a paid subscription is needed to keep an account or membership valid.

The most prevalent on-chain application that makes use of the renewable subscription model is the Ethereum Name Service (ENS), which utilizes a similar interface to the one proposed below. Each domain can be renewed for a certain period of time, and expires if payments are no longer made. A common interface will make it easier for future projects to develop subscription-based NFTs. In the current Web2 world, it’s hard for a user to see or manage all of their subscriptions in one place. With a common standard for subscriptions, it will be easy for a single application to determine the number of subscriptions a user has, see when they expire, and renew/cancel them as requested.

Additionally, as the prevalence of secondary royalties from NFT trading disappears, creators will need new models for generating recurring income. For NFTs that act as membership or access passes, pivoting to a subscription-based model is one way to provide income and also force issuers to keep providing value.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

The technical specification should describe the syntax and semantics of any new feature. The specification should be detailed enough to allow competing, interoperable implementations for any of the current Ethereum platforms (go-ethereum, parity, cpp-ethereum, ethereumj, ethereumjs, and [others](https://github.com/ethereum/wiki/wiki/Clients)).

```solidity
interface IERC5643 {
    /// @notice Emitted when a subscription expiration changes
    /// @dev When a subscription is canceled, the expiration value should also be 0.
    event SubscriptionUpdate(uint256 indexed tokenId, uint64 expiration);

    /// @notice Renews the subscription to an NFT
    /// Throws if `tokenId` is not a valid NFT
    /// @param tokenId The NFT to renew the subscription for
    function renewSubscription(uint256 tokenId, uint64 expiration) external payable;

    /// @notice Cancels the subscription of an NFT
    /// @dev Throws if `tokenId` is not a valid NFT
    /// @param tokenId The NFT to cancel the subscription for
    function cancelSubscription(uint256 tokenId) external payable;

    /// @notice Gets the expiration date of a subscription
    /// @dev Throws if `tokenId` is not a valid NFT
    /// @param tokenId The NFT to get the expiration date of
    /// @return The expiration date of the subscription
    function expiresAt(uint256 tokenId) external view returns(uint64);

    /// @notice Determines whether a subscription can be renewed
    /// @dev Throws if `tokenId` is not a valid NFT
    /// @param tokenId The NFT to get the expiration date of
    /// @return The renewability of a the subscription
    function isRenewable(uint256 tokenId) external view returns(bool);
}
```

The `expiresAt(uint256 tokenId)` function MAY be implemented as `pure` or `view`.

The `isRenewable(uint256 tokenId)` function MAY be implemented as `pure` or `view`.

The `renewSubscription(uint256 tokenId)` function MAY be implemented as `external` or `public`.

The `cancelSubscription(uint256 tokenId)` function MAY be implemented as `external` or `public`.

The `SubscriptionUpdate` event MUST be emitted whenever the expiration date of a subscription is changed.

The `supportsInterface` method MUST return `true` when called with `0x8c65f84d`.

## Rationale

This standard aims to make on-chain subscriptions as simple as possible by adding the minimal required functions and events for implementing on-chain subscriptions. It is important to note that in this interface, the NFT itself represents ownership of a subscription, there is no facilitation of any other fungible or non-fungible tokens.

### Subscription Management

Subscriptions represent agreements to make advanced payments in order to receive or participate in something. In order to facilitate these agreements, a user must be able to renew or cancel their subscriptions hence the `renewSubscription` and `cancelSubscription` functions. It also important to know when a subscription expires - users will need this information to know when to renew, and applications need this information to determine the validity of a subscription NFT. The `expiresAt` function provides this functionality. Finally, it is possible that a subscription may not be renewed once expired. The `isRenewable` function gives users and applications that information.

### Easy Integration

Because this standard is fully EIP-721 compliant, existing protocols will be able to faciliate the transfer of subscription NFTs out of the box. With only a few functions to add, protocols will be able to fully manage a subscription’s expiration, determine whether a subscription is expired, and see whether it can be renewed.

## Backwards Compatibility

This standard can be fully EIP-721 compatible by adding an extension function set.

The new functions introduced in this standard add minimal overhead to the existing EIP-721 interface, which should make adoption straightforward and quick for developers.

## Test Cases

The following tests require Foundry.

```solidity
// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.13;

import "forge-std/Test.sol";
import "../src/ERC5643.sol";

contract ERC5643Mock is ERC5643 {
    constructor(string memory name_, string memory symbol_) ERC5643(name_, symbol_) {}

    function mint(address to, uint256 tokenId) public {
        _mint(to, tokenId);
    }
}

contract ContractTest is Test {
    event SubscriptionUpdate(uint256 indexed tokenId, uint64 expiration);

    address user1;
    uint256 tokenId;
    ERC5643Mock erc5643;

    function setUp() public {
        tokenId = 1;
        user1 = address(0x1);

        erc5643 = new ERC5643Mock("erc5369", "ERC5643");
        erc5643.mint(user1, tokenId);
    }

    function testRenewalValid() public {
        vm.prank(user1);
        vm.expectEmit(true, true, false, true);
        emit SubscriptionUpdate(tokenId, 2000);
        erc5643.renewSubscription(tokenId, 2000);
    }

    function testRenewalNotOwner() public {
        vm.expectRevert("Caller is not owner nor approved");
        erc5643.renewSubscription(tokenId, 2000);
    }

    function testCancelValid() public {
        vm.prank(user1);
        vm.expectEmit(true, true, false, true);
        emit SubscriptionUpdate(tokenId, 0);
        erc5643.cancelSubscription(tokenId);
    }

    function testCancelNotOwner() public {
        vm.expectRevert("Caller is not owner nor approved");
        erc5643.cancelSubscription(tokenId);
    }

    function testExpiresAt() public {
        assertEq(erc5643.expiresAt(tokenId), 0);
        vm.startPrank(user1);
        erc5643.renewSubscription(tokenId, 2000);
        assertEq(erc5643.expiresAt(tokenId), 2000);

        erc5643.cancelSubscription(tokenId);
        assertEq(erc5643.expiresAt(tokenId), 0);
    }
}
```

## Reference Implementation

Implementation: ERC5643.sol

```solidity
// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.13;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "./IERC5643.sol";

contract ERC5643 is ERC721, IERC5643 {
    mapping(uint256 => uint64) private _subscriptions;

    constructor(string memory name_, string memory symbol_) ERC721(name_, symbol_) {}

    function renewSubscription(uint256 tokenId, uint64 expiration) external payable {
        require(_isApprovedOrOwner(msg.sender, tokenId), "Caller is not owner nor approved");
        _subscriptions[tokenId] = expiration;
        emit SubscriptionUpdate(tokenId, expiration);
    }

    function cancelSubscription(uint256 tokenId) external payable {
        require(_isApprovedOrOwner(msg.sender, tokenId), "Caller is not owner nor approved");
        delete _subscriptions[tokenId];
        emit SubscriptionUpdate(tokenId, 0);
    }

    function expiresAt(uint256 tokenId) external view returns(uint64) {
        return _subscriptions[tokenId];
    }

    function isRenewable(uint256 tokenId) external pure returns(bool) {
        return true;
    }

    function supportsInterface(bytes4 interfaceId) public view virtual override returns (bool) {
        return interfaceId == type(IERC5643).interfaceId || super.supportsInterface(interfaceId);
    }
}
```

## Security Considerations

This EIP standard does not affect ownership of an NFT and thus can be considered secure.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**cygaar** (2022-09-10):

I’ve read through some of the other proposed subscription-related posts: [EIP-4885: Subscription Token Standard](https://ethereum-magicians.org/t/eip-4885-subscription-token-standard/8531), [EIP-5029: Subscription Tokens](https://ethereum-magicians.org/t/eip-5029-subscription-tokens/9013), but I wanted to create an interface that used the NFT itself to represent the subscription in order to be simple and easily compatible with ERC721. Rather than pay (via an ERC20 token) and receive some sort of balance, I propose that users pay (via ETH) and have a set expiration time of their subscription. This model is simple, requires only one extra on-chain mapping, and makes it easier for users to know when their subscription expire.

---

**darcys22** (2022-09-10):

Awesome work, like the idea.

What would the benefit be over minting a new nft every time your subscription period ends though?

---

**cygaar** (2022-09-11):

A service might want to reward long time subscribers, and in that case you’d want to keep your subscription NFT as long as possible rather than burning one every time it ends. It’s also *probably* less gas, but I’d have to run some tests.

---

**julien51** (2022-09-12):

This is very exciting. And something we’re happy to support at Unlock where we built [renewable NFT subscriptions](https://unlock-protocol.com/blog/recurring-subscription-nft) a while back!

One issue that i can see here is that the subscriptions has to be manually renewed by the owner of the NFT everytime it expires which is not ideal. (Imagine if your have to give the Netflix once a month to extend your account).

The approach we took at Unlock it’s to enable “pricing” using ERC20 where the user can then approve a large amount corresponding to multiple renewals that can then be triggered by anyone.

We’d love to contribute!

---

**zlace** (2022-09-12):

Love the simplicity of this!

Can tie in well with



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xanders/48/5635_2.png)

      [EIP-5007: EIP-721 Time Extension](https://ethereum-magicians.org/t/eip-5007-eip-721-time-extension/8924) [EIPs](/c/eips/5)




> eip:
> title: ERC-721 Time Extension
> description: Add start time and end time to ERC-721 tokens.
> author: Anders (@0xanders), Lance (@LanceSnow), Shrug shrug@emojidao.org
> discussions-to:
> status: Draft
> type: Standards Track
> category: ERC
> created: 2022-04-13
> requires: 165, 721
>
> Abstract
> This standard is an extension of ERC-721. It proposes some additional property( startTime, endTime,originalTokenId) to help with the on-chain time management.
>
> Motivation
> Some NFTs have a defined usage per…

---

**cygaar** (2022-09-12):

What changes to the interface would you make? I’d imagine something related to allowing auto-renewals?

---

**gregfromstl** (2022-09-13):

I agree the most common use case will involve auto-renewals but think that should be left to the implementation rather than requiring it for the standard. That way the standard only requires the base level implementation.

---

**shobhit** (2022-09-14):

Why is `cancelSubscription` payable?

Also, I think `updateSubscription` will be a better name than `renewSubscription`.

---

**MrLine** (2022-09-15):

This is awesome, we are thinking of integrating this into our NFT project/app. NFT 2.0

---

**cygaar** (2022-09-15):

That’s how I was approaching this problem, however if someone can provide a clean interface for auto-renewals I’d be happy to consider it

---

**cygaar** (2022-09-15):

Someone may have a reason to make cancellations payable, I want this to be as open as possible. Take EIP721 for example, transfer and approve are both payable but it’s not used most of the time.

---

**julien51** (2022-09-16):

First of all, thanks a lot for your patience here.

I would preface by saying that I am really happy that the space is thinking about recurring revenues. I deeply believe that the “sell once, provide value forever” model is not going to work for lots of creators… Additionally time limits on NFTs do bring lots of opportunities for artistic work even! You can make on NFT that render differently based on whether they are expired or, or how close to expiration they are… etc! (People have used Unlock for that and it’s pretty cool!).

Now, when it comes to feedback about the spec, I think it is a good start, but also falls short to be practically usable as is.

For example, and unless I missed something there is currently no way to *start* a subscription.

Well, first I think you would need to have a way for the user to “start” a subscription. Right now it is unclear how as a user, when I own an NFT, I can “start a subscription”.

Then, as I wrote earlier, I deeply believe that a prerequisite to this would be to allow users to pay for the NFT with an ERC20 (vs the native currency via the payable approach). The reason for this is that with ERC20 users can “approve” the contract to spend from them… rather than have them come back over and over to (re)purchase next month’s subscription. However, if ERC20 “approvals” are supported it is critical to make sure they are not abused by either making the price/duration “unchangeable”, or by keeping track in the contract of what each user has “allowed” in terms of pricing (combination of duration and amount).

---

**cygaar** (2022-09-16):

Regarding the “no way to start a subscription”, I was imagining it would be part of the mint process for the token - when you mint a token to someone, the subscription would start. However, we could in theory change `renewSubscription` to `updateSubscription` like mentioned above and kick off the subscription then.

For autorenewals, I do agree that having this feature is nice to have, however if you look at ENS, they’ve been able to create a very successful subscription NFT without needing it. I can see a popular library having an autorenewal feature built-in (similar to how OpenZeppelin’s library has mint functions for 721), but I don’t think the standard requires it. At the end of the day, a subscription only really needs to be renewable and cancelable to be considered a “subscription”.

---

**cosmosys** (2022-09-22):

This has a great use case for e-commerce NFTs. I’d be down to do some hypothesis test with [www.shopx.co](http://www.shopx.co) → might be interesting to open up that subscriptions could be paid in erc-20s too.

---

**cygaar** (2022-09-24):

Happy to work with you on implementing this EIP!

---

**aram** (2022-10-12):

Thanks [@cygaar](/u/cygaar) for the proposal, very good work ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12)

To keep it simpler would it be beneficial to leave our the “renew” functions out of this EIP, and only keep the view functions (and maybe cancel) included?

Main reason for that is similar to mint function there would be various ways people want to implement a “start”/“renew” for example choosing a specific Plan, not just a direct payment, or being able to “upgrade”/“downgrade”, etc.

Since the signature for renew (and potentially upgrade/downgrade) cannot be generalized, the wallet implementations for example cannot create a “Generic Renewal” interface and take advantage of a standard.

Another way to generalize “renew” (or “update”) is to extend the EIP further (which I personally suggest to be a separate eip maybe), is to provide an additional “bytes data” argument. But still since there won’t be a generalized solution, and each dApp will end up creating their own renewal methods/interfaces.

People could still use same method name (e.g. updateSubscription) but the rest of signature might be different per use-case.

What are you thoughts?

---

**mpeyfuss** (2022-10-18):

[@cygaar](/u/cygaar) this is an awesome proposal that I’d love to contribute to. Timing works out as I am currently developing a subscription NFT ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

[@aram](/u/aram) makes a good point on the update functions potentially being limiting based on the desired implementation. Limiting this standard to only view functions and the required events would greatly increase usability for various implementations. This would also help solve the questions about auto-renewals and how to start subscriptions.

I do have two additional comments as feedback.

1. I think adding in a function called isCancelable would make a lot of sense, as there can definitely be implementations that don’t want to allow canceled subscriptions. It would operate similar to isRenewable.
2. Typically subscriptions have tiers. The way you buy tiers is hard to generalize properly, but adding the idea of tiers should be easy to implement into this standard. Basically, the SubscriptionUpdate event would have to include a tier variable (maybe uint8 so enums can be used - 255 tiers should be plenty in basically all applications) and adding a getTier view function would be simple. It may also make sense to add view functions for seeing if a token is upgradeable/downgradeable – isUpgradeable and isDowngradeable.

---

**admlj** (2022-10-19):

edit: ahhh i see this has been implemented already, nice

i’m wondering if, rather than having to manually set the `expiration` for `renewSubscription`, it might be better to have that function take a `duration` instead that would then be added to the existing `_subscription`.

like “renew for 30 days” and it would check if 30 days * cost was paid then add time.~

---

**cygaar** (2022-10-24):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/a/b782af/48.png) admlj:

> renewSubscription

Yes, I actually made that change in the EIP as well as the implementation: [ERC5643/src/IERC5643.sol at main · cygaar/ERC5643 · GitHub](https://github.com/cygaar/ERC5643/blob/main/src/IERC5643.sol#L14). Thanks for the callout!

---

**cygaar** (2022-10-24):

Let me think on the renew function - I think it makes sense to require a function of this nature since it’s a core part of being a subscription. I would be open to having a second renew function that takes in a `data` bytes parameter (similar to 721 having multiple safeTransferFrom functions).

1. This is a bit tricky because if a user doesn’t pay for their subscription then it’s by definition canceled. Even if you say a subscription can’t be canceled, you can’t force a user to pay.
2. I think this would be a good idea for an implementation, but I don’t think it’s necessary for a standard interface. I’ll think about it some more.


*(23 more replies not shown)*
