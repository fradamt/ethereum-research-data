---
source: magicians
topic_id: 25482
title: "ERC-8027: Recurring Subscription NFT"
author: ant
date: "2025-09-16"
category: ERCs
tags: [erc, nft, erc-721]
url: https://ethereum-magicians.org/t/erc-8027-recurring-subscription-nft/25482
views: 92
likes: 2
posts_count: 10
---

# ERC-8027: Recurring Subscription NFT

## Abstract

Recurring Subscription NFT is an extension of [ERC-721](https://file+.vscode-resource.vscode-cdn.net/Users/ant/Desktop/ERCs/ERCS/eip-721.md) token that enables recurring subscription feature by charging the NFT holder ERC-20 tokens via any token approval methods.

The interface suggests specifications that allow users to renew/extend subscriptions, service provider to charge users automatically for recurring subscription by their subscription data and [EIP-712](https://file+.vscode-resource.vscode-cdn.net/Users/ant/Desktop/ERCs/ERCS/eip-712.md) signature. Also an optional function for users to cancel their subscription by revoking the respective token approval.

## Motivation

NFTs are commonly used as ownership verification on decentralized apps or membership passes to communities, events, and more. However, these use cases often fall into either being a token of ownership that have no expiration dates, or a one-off ticket for verifying identity/reservation thus no recurring payments involved for both cases. However for many real-world applications with paid subscriptions, they would prefer a middle ground - to keep an account or membership valid until the user stops paying for the subscription.

Currently there exists no standard implementation for subscription service that allows:

1. service provider to easily configure a subscription
2. users to setup a seamless payment flow via gasless pre-approval for any ERC-20 with an expiry date
3. the above while restricting the service provider from only automatically charging by each cycle instead of a full amount to keep users’ subscriptions active

On the other hand a common interface will make it easier for future projects to develop subscription-based NFTs. In the current Web2 world, it’s hard for a user to see or manage all of their subscriptions in one place. With a common standard for subscriptions, it will be easy for a single application to determine the number of subscriptions a user has, see when they expire, and renew/cancel them as requested.

Overall this standard offers a more efficient approach for both users and the platform. Rather than forcing users to pay a huge lump sum to tie them into a long subscription plan, or having users locked a fixed amount of funds in advance waiting to be charged each month, users can just spend their funds as they please, and keep enough funds to be deducted by the service provider for the next cycle of subscription without going through a manual subscription process - basically like a debit card for recurring subscription, and more similar to how an auto subscription would work in web2.

## Specification

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

interface IERC8027 {
    /**
     * @param paymentToken Token to pay for the subscription, use address(0) for native token
     * @param serviceProvider The address of the service provider to receive the payment
     * @param billingInterval The interval of each subscription billing in seconds
     * @param planPrices Array of prices for different plans, the respective index of the price refers to `planIdx`,
     * length > 1 indicates multiple plans available
     */
    struct SubscriptionConfig {
        address paymentToken;
        address serviceProvider;
        uint64 billingInterval;
        uint256[] planPrices;
    }

    /**
     * @param planIdx The index of the subscription plan from `planPrices`
     * @param expiryTs The latest timestamp which the subscription is valid until
     */
    struct Subscription {
        uint128 planIdx;
        uint128 expiryTs;
    }

    struct RecurringSubscriptionData {
        uint256 tokenId;
        uint128 planIdx;
        uint64 numOfIntervals;
        bytes tokenApprovalData;
        bytes extraVerificationData;
    }

    /**
     * @notice Emitted when a subscription is extended
     * @dev When a subscription is extended, the expiration timestamp is extended for `billingInterval * numOfIntervals`
     * @param tokenId The NFT to extend the subscription for
     * @param planIdx The plan index to indicate which plan to extend the subscription for
     * @param oldExpiryTs The old expiration timestamp of the subscription
     * @param newExpiryTs The new expiration timestamp of the subscription
     */
    event SubscriptionExtended(uint256 indexed tokenId, uint128 planIdx, uint128 oldExpiryTs, uint128 newExpiryTs);

    /**
     * @notice Emitted when service provider charges a user for a recurring subscription
     * @dev When a recurring subscription is charged, the expiration timestamp is extended for ONE `billingInterval` only
     * @param tokenId The NFT to charge the recurring subscription for
     */
    event RecurringSubscriptionCharged(uint256 indexed tokenId);

    /// @notice Thrown when paymentToken is address(0) but not enough native token is sent as msg.value
    error InsufficientPayment();
    /// @notice Thrown when the subscription is not renewable for all tokens or a given tokenId
    error SubscriptionNotRenewable();
    /// @notice Thrown when the tokenId does not exist
    error InvalidTokenId();
    /// @notice Thrown when the number of intervals is not greater than 0
    error InvalidNumOfIntervals();
    /// @notice Thrown when the plan index exceeds the number of plans
    error InvalidPlanIdx();
    /// @notice Thrown when the payment of native token or ERC20 token failed
    error TransferFailed();

    /**
     * @notice Manually renews a subscription for an NFT by directly transferring native token or ERC20 token to the service provider
     * @param tokenId The NFT to renew the subscription for
     * @param planIdx The plan index to indicate which plan to subscribe to
     * @param numOfIntervals The number of `interval` to extend the subscription for
     */
    function renewSubscription(uint256 tokenId, uint128 planIdx, uint64 numOfIntervals) external payable;

    /**
     * @notice Charges the subscription for an NFT by transferring ERC20 payment token from user to the service provider,
     * usually called by the service provider automatically and recurringly for each `billingInterval`
     * after a subscription is signaled by a user via signing token approval off-chain
     * @param data A packed struct of subscription data
     */
    function chargeRecurringSubscription(RecurringSubscriptionData memory data) external;

    /**
     * @notice Determines whether a NFT's subscription can be renewed
     * @dev Returns false if `tokenId` does not exist
     * @param tokenId The NFT to check the renewability of
     * @return The renewability of a NFT's subscription
     */
    function isRenewable(uint256 tokenId) external view returns (bool);

    /**
     * @notice Gets the expiration date of a NFT's subscription
     * @dev Returns 0 if `tokenId` does not exist
     * @param tokenId The NFT to get the expiration date of
     * @return The `expiryTs` of the NFT's subscription
     */
    function expiresAt(uint256 tokenId) external view returns (uint128);

    /**
     * @notice Gets the price to renew a subscription for a number of `interval` for a given tokenId.
     * @dev Returns 0 if `numOfIntervals` is 0 or `planIdx` is not a valid plan index
     * @param planIdx The plan index to indicate which plan to subscribe to
     * @param numOfIntervals The number of `interval` to renew the subscription for
     * @return The price to renew the subscription
     */
    function getRenewalPrice(uint128 planIdx, uint64 numOfIntervals) external view returns (uint256);

    /**
     * @notice Gets the subscription details for a given tokenId
     * @dev Returns empty `Subscription` if `tokenId` does not exist
     * @param tokenId The NFT to get the subscription for
     * @return The packed struct of `Subscription`
     */
    function getSubscriptionDetails(uint256 tokenId) external view returns (Subscription memory);

    /**
     * @notice Gets the subscription config
     * @return The packed struct of `SubscriptionConfig`
     */
    function getSubscriptionConfig() external view returns (SubscriptionConfig memory);
}
```

## Rationale

This standard aims to make on-chain recurring subscriptions as generic and as easy to integrate with as possible by having minimal configurations. Here are few design choices being made to fulfill these purposes.

1. The SubscriptionConfig allows multiple plans to be configured - the standard supports multiple plans to enable tierd subscription plans and only using ERC-20 as payment token will enable recurring subscription due to its approval feature. The NFT itself represents ownership of a subscription and there is no facilitation of how the NFT should be minted or transferred.
2. RecurringSubscriptionData passed in chargeRecurringSubscription is designed to be generic in order to integrate with any ERC-20 approval methods:

```auto
struct RecurringSubscriptionData {
    uint256 tokenId;
    uint128 planIdx;
    uint64 numOfIntervals;
    bytes tokenApprovalData;
    bytes extraVerificationData;
}

```

 tokenid: Token id of the Subscription NFT
 planIdx: Index of the plan in planPrices array
 numOfIntervals: The number of billingInterval for verifying total pre-approval amount of the recurring subscription
 tokenApprovalData Encoded data to handle different token approval logic such as Permit/Permit2
 extraVerificationData Encoded data to handle extra verification logic for example a signed EIP-712 signature if more verifications are needed.
3. For actual implementation in ERC8027.sol, customizations on:

 verifying token approval and charging automatically should be done by overriding _verifyApprovalAndCharge to integrate with any common ERC-20 approval methods e.g. ERC-2612, ERC-3009 and Permit2
4. verifing inputs passed from the function caller should be done by overriding _verifyInputs
5. paying for manual subscription should be done by overriding _pay
6. extending subscription should be done by overriding _extendSubscription

### Considerations on token pre-approval via Account Abstraction(AA)

Even though we could somehow achieve something similar to gasless pre-approval with the help of [EIP-7702](https://file+.vscode-resource.vscode-cdn.net/Users/ant/Desktop/ERCs/ERCS/eip-7702.md), user’s EOA will need to delegate to an external contract to act as an smart account which would impose extra security vectors that integrators need to consider, and the subscription feature is still lacking nonetheless.

More importantly this interface is in fact compatitable with such smart accounts as long as they are able to receive NFT i.e. with `onERC721Received` implemented thus this interface provides a standardized framework while being AA-compatible for apps to offer subscription features in a more composable way.

### Subscription Management

- Manual subscription: Users should be able to renew their subscriptions by directly transferring either native or ERC-20 tokens to the service provider thus the renewSubscription function. Users will specify the index of subscription plan i.e. planIdx and the number of interval to subscribe for i.e. numOfIntervals.
- Recurring subscription: Normally users will start by signing a EIP-712 signature off-chain to pre-approve the Recurring Subscription NFT contract the total funds needed for their subscription, ideally on a platform where service provider can gather their signature and subscription data to be used to call chargeRecurringSubscription. The service provider will then be able to charge subscription fee automatically by billingInterval via chargeRecurringSubscription to start the subscription for users, no extra subscription fee should be sent to service provider as per the standard’s implementation. If the users don’t want to continue the subscription they can either call cancelAutoSubscription to revoke token approval if this is available in the approval implementation that integrates with this interface, or they can directly move the funds out from the wallet they initially signed the approval with.
- expiresAt function allows users and applications to directly confirm the validity of a Subscription NFT by checking its expiration date, and getSubscriptionDetails function will get both the expiration date and the subscription plan the Subscription NFT belongs to.
- getRenewalPrice helps users and applications to calculate the price of the subscription given the plan it belongs and the number of intervals the subscription will continue for.
- isRenewable function gives users and applications the information whether a subscription for a certain NFT or all NFTs could be renewed once expired.
- getSubscriptionConfig will give users and applications the information about the configuration of the subscription such as which payment token, which service provider will receive the subscription fee, how long is each interval is, and the price for each plan.
- Finally it’s important to know that only using ERC-20 as payment token can enable recurring subscription as we cannot directly transfer native token on behalf of users without introducing external dependencies.

## Backwards Compatibility

This standard can be fully [ERC-721](https://file+.vscode-resource.vscode-cdn.net/Users/ant/Desktop/ERCs/ERCS/erc-721.md) compatible by adding an extension function set, and payment can be integrated with any [ERC-20](https://file+.vscode-resource.vscode-cdn.net/Users/ant/Desktop/ERCs/ERCS/erc-20.md) out of the box.

This standard is also fully compatible with smart accounts that utilize Account Abstraction standards such as [EIP-4337](https://file+.vscode-resource.vscode-cdn.net/Users/ant/Desktop/ERCs/ERCS/erc-4337.md) and [EIP-7702](https://file+.vscode-resource.vscode-cdn.net/Users/ant/Desktop/ERCs/ERCS/erc-7702.md) as long as they are able to receive NFT i.e. with `onERC721Received` implemented or with `ERC721Holder.sol` from OpenZeppelin inherited.

## Reference Implementation

### ERC8027.sol

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import { IERC165 } from "@openzeppelin/contracts/interfaces/IERC165.sol";
import { IERC20 } from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import { ERC721 } from "@openzeppelin/contracts/token/ERC721/ERC721.sol";

import { IERC8027 } from "./IERC8027.sol";

abstract contract ERC8027 is IERC8027, ERC721 {
    mapping(uint256 tokenId => Subscription) internal _subscriptions;

    SubscriptionConfig internal _subscriptionConfig;

    constructor(
        string memory name_,
        string memory symbol_,
        SubscriptionConfig memory subscriptionConfig
    ) ERC721(name_, symbol_) {
        _subscriptionConfig = subscriptionConfig;
    }

    /* MANUAL SUBSCRIPTION RENEWAL BY USER */
    /// @inheritdoc IERC8027
    function renewSubscription(uint256 tokenId, uint128 planIdx, uint64 numOfIntervals) public payable {
        SubscriptionConfig memory config = _subscriptionConfig;

        _verifyInputs(tokenId, planIdx, config.planPrices.length, numOfIntervals);

        _pay(config, planIdx, numOfIntervals);
        _extendSubscription(tokenId, planIdx, config.billingInterval, numOfIntervals);
    }

    /* RECURRING SUBSCRIPTION RENEWAL BY SERVICE PROVIDER */
    /// @inheritdoc IERC8027
    function chargeRecurringSubscription(RecurringSubscriptionData calldata data) public {
        SubscriptionConfig memory config = _subscriptionConfig;

        _verifyInputs(data.tokenId, data.planIdx, config.planPrices.length, data.numOfIntervals);

        _verifyApprovalAndCharge(data);
        _extendSubscription(data.tokenId, data.planIdx, config.billingInterval, 1);
    }

    /* INTERNALS */
    /**
     * @dev Ensures the inputs are valid.
     * 1. the tokenId exists
     * 2. the planIdx is less than the number of plans
     * 3. the numOfIntervals is greater than 0
     */
    function _verifyInputs(
        uint256 tokenId,
        uint128 planIdx,
        uint256 numOfPlans,
        uint64 numOfIntervals
    ) internal virtual {
        require(_ownerOf(tokenId) != address(0), InvalidTokenId());
        require(planIdx  0, InvalidNumOfIntervals());
    }

    /**
     * @dev Internal function to pay for the subscription, supports both native token and ERC20 token payment.
     * If the payment token is address(0), the function will use msg.value to pay for the subscription.
     * If the payment token is not address(0), the function will transfer the payment token from the caller to the service provider.
     */
    function _pay(SubscriptionConfig memory config, uint128 planIdx, uint64 numOfIntervals) internal virtual {
        uint256 planPrice = _calcRenewalPrice(config.planPrices[planIdx], numOfIntervals);
        if (config.paymentToken == address(0)) {
            require(msg.value == planPrice, InsufficientPayment());
            (bool success,) = payable(config.serviceProvider).call{ value: planPrice }("");
            require(success, TransferFailed());
        } else {
            IERC20(config.paymentToken).transferFrom(msg.sender, config.serviceProvider, planPrice);
        }
    }

    /**
     * @dev Extends the subscription for `tokenId` for `duration` seconds.
     * If the `tokenId` does not exist, an error will be thrown.
     * If a token is not renewable, an error will be thrown.
     * Emits a {SubscriptionExtended} event after the subscription is extended.
     */
    function _extendSubscription(
        uint256 tokenId,
        uint128 planIdx,
        uint64 billingInterval,
        uint64 numOfIntervals
    ) internal virtual {
        uint128 expiryTs = _subscriptions[tokenId].expiryTs;
        uint128 newExpiryTs;
        if ((expiryTs == 0) || (expiryTs = _subscriptionConfig.planPrices.length) return 0;
        return _calcRenewalPrice(_subscriptionConfig.planPrices[planIdx], numOfIntervals);
    }

    /// @inheritdoc IERC8027
    function getSubscriptionDetails(uint256 tokenId) public view virtual returns (Subscription memory) {
        if (_ownerOf(tokenId) == address(0)) return Subscription({ planIdx: 0, expiryTs: 0 });
        return _subscriptions[tokenId];
    }

    /// @inheritdoc IERC8027
    function getSubscriptionConfig() public view virtual returns (SubscriptionConfig memory) {
        return _subscriptionConfig;
    }

    /// @inheritdoc IERC165
    function supportsInterface(bytes4 interfaceId) public view virtual override(ERC721) returns (bool) {
        return interfaceId == type(IERC8027).interfaceId || super.supportsInterface(interfaceId);
    }
}
```

### Example: ERC8027Permit2.sol - ERC8027.sol that integrates with Permit2

```auto
// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import { IERC165 } from "@openzeppelin/contracts/interfaces/IERC165.sol";
import { IERC20 } from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import { ERC721 } from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import { IAllowanceTransfer, IPermit2 } from "@permit2/interfaces/IPermit2.sol";

import { ERC8027 } from "./ERC8027.sol";
import { IERC8027 } from "./IERC8027.sol";

struct TokenApprovalData {
    IPermit2.PermitSingle permitSingle;
    bytes signature;
}

/// @notice Emitted when a user cancels the upcoming subscription by revoking permit2 allowance
/// @dev When a subscription is canceled, the subscription will last until the `expiryTs` timestamp
/// @param tokenId The NFT to cancel the auto subscription for
event RecurringSubscriptionCancelled(uint256 indexed tokenId);

/// @notice Thrown when the token specified in the permit is not same as the payment token
error PaymentTokenMismatch();
/// @notice Thrown when the expiration of the permit doesn't last until the current timestamp + `billingInterval * numOfIntervals`
error AllowanceExpireTooEarly();
/// @notice Thrown when the spender of the permit is not this contract
error InvalidSpender();
/// @notice Thrown when the service provider charges before the `expiryTs` of the subscriber's subscription
error ChargeTooEarly();
/// @notice Thrown when the service provider charges for subscription that uses native token as `paymentToken` in `SubscriptionConfig`
error OnlyERC20ForAutoRenewal();
/// @notice Thrown when the payment of native token or ERC20 token failed
error TransferFailed();

abstract contract ERC8027Permit2 is ERC8027 {
    IPermit2 public immutable PERMIT2;

    constructor(
        string memory name_,
        string memory symbol_,
        SubscriptionConfig memory subscriptionConfig,
        address permit2
    ) ERC8027(name_, symbol_, subscriptionConfig) {
        PERMIT2 = IPermit2(permit2);
    }

    /* OPTIONAL FUNCTIONS */
    function cancelAutoSubscription(uint256 tokenId) public virtual {
        require(_ownerOf(tokenId) != address(0), InvalidTokenId());
        SubscriptionConfig memory config = _subscriptionConfig;
        IPermit2.TokenSpenderPair[] memory approvals = new IPermit2.TokenSpenderPair[](1);
        approvals[0] = IAllowanceTransfer.TokenSpenderPair(config.paymentToken, config.serviceProvider);

        PERMIT2.lockdown(approvals);

        emit RecurringSubscriptionCancelled(tokenId);
    }

    /* INTERNALS */
    /**
     * @dev Ensures the permit is valid beforehand by making sure:
     * 1. this contract is the spender
     * 2. the payment token is the same as the allowed token
     * 3. the amount is the same as the price of the subscription plan times the number of intervals
     * 4. the expiration is greater or equal to the current timestamp + `interval * numOfIntervals`
     */
    function _verifyApprovalAndCharge(RecurringSubscriptionData memory data) internal override {
        // TODO: see if we need the extraVerificationData to verify the whole data as a eip712 signature
        TokenApprovalData memory tokenApprovalData = abi.decode(data.tokenApprovalData, (TokenApprovalData));
        IPermit2.PermitSingle memory permit = tokenApprovalData.permitSingle;
        SubscriptionConfig memory config = _subscriptionConfig;

        require(permit.details.token == config.paymentToken, PaymentTokenMismatch());
        require(
            permit.details.amount == _calcRenewalPrice(config.planPrices[data.planIdx], data.numOfIntervals),
            InsufficientPayment()
        );
        require(
            permit.details.expiration >= block.timestamp + config.billingInterval * data.numOfIntervals,
            AllowanceExpireTooEarly()
        );
        require(permit.spender == address(this), InvalidSpender());

        address nftOwner = _ownerOf(data.tokenId);
        PERMIT2.permit(nftOwner, tokenApprovalData.permitSingle, tokenApprovalData.signature);

        Subscription memory subscription = _subscriptions[data.tokenId];
        require(block.timestamp > subscription.expiryTs, ChargeTooEarly());
        require(config.paymentToken != address(0), OnlyERC20ForAutoRenewal());

        // NOTE: only charge for one interval to keep the subscription automatic
        try PERMIT2.transferFrom(
            nftOwner, config.serviceProvider, uint160(config.planPrices[subscription.planIdx]), config.paymentToken
        ) {
            _extendSubscription(data.tokenId, subscription.planIdx, config.billingInterval, 1);
            emit RecurringSubscriptionCharged(data.tokenId);
        } catch {
            revert TransferFailed();
        }
    }
}
```

## Security Considerations

- This EIP standard does not affect ownership of an NFT
- When integrating with Permit-like token approval, to ensure no extra subscription fee would be sent to the service provider, caution should be taken to make sure:

 the spender of the Permit is restricted to only the contract that applies this standard
- payment receiver is restricted to the service provider
- implementation in _verifyApprovalAndCharge should verify chargeRecurringSubscription can only be called by each cycle of interval

## Replies

**ant** (2025-09-16):

This standard is inspired by the foundation and direction of the [Subscription NFTs](https://ethereum-magicians.org/t/eip-5643-subscription-nfts/10802) proposed by [@cygaar](/u/cygaar) previously thus I have added cygaar as the co-author, unfortunately he isn’t actively working on that EIP currently so I am hoping to propose this SubNFTs standard instead for a better implementation of a real-world on-chain recurring subscription.

---

**vitali_grabovski** (2025-09-17):

Hello, could you provide one or two specific examples where an NFT-level subscription would be a perfect augmentation?

---

**ant** (2025-09-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vitali_grabovski/48/15798_2.png) vitali_grabovski:

> Hello, could you provide one or two specific examples where an NFT-level subscription would be a perfect augmentation?

Hey there! I think NFT-level subscriptions can be utilized in a number of real-world use cases - for  example accessing market analytics service like [Dexu](https://dexu.ai/narratives) or an advanced feature of a DeFi protocol, premium newsletters from creators, and even on-chain video-streaming platform to name a few.

Benefits of providing subscriptions in NFT(i.e. tokenizing subscription):

- easy management of subscriptions like transferring to another user or renewing with ease
- users can take true ownership of their subscription without fear of getting blocked/blacklisted by the service provider for any reasons(as the subscription logic is not as a blackbox as in web2 but of course it depends on the actual implementation)
- the NFT itself can be used as trustless verification to bring further benefits to users
- by supporting ERC20 recurring payments we can pretty much bring most of the web2 services on-chain

One prevalent example we have right now in web3 is the Ethereum Name Service (ENS) where each domain can be renewed for a certain period of time, and expires if payments are no longer made. With SubNFTs ENS could definitely make use of the recurring payment feature to make their subscription process more flexible and seamless for users!

---

**vitali_grabovski** (2025-09-17):

I’m thinking about smart wallets. Most of them have ERC-20/ETH subscription features, including recurring payments, pre-approved one-time payment options, and more.

Do you think wallet-level subscriptions are still unable to solve the problems and answer the questions you raised in the ‘Motivation’ section?

---

**ant** (2025-09-17):

Yes something like EIP7702 could indeed enable such feature but this is also the reason I think this standard can bring extra benefits with - since it doesn’t require the user’s EOA to delegate to an external contract which could impose extra security vectors that integrators need to consider(plus the delegated contract could contain more functions other than subscription) - while SubNFTs provide a non-wallet level standardized framework for apps to adopt subscription features in a more flexible way

---

**ant** (2025-09-18):

Here is the library for this EIP which contains the implementation, test cases and deploy script:



      [github.com](https://github.com/0xdevant/ERC8027)




  ![image](https://opengraph.githubassets.com/d6e77638fc68e36f9a376a43ced207ce/0xdevant/ERC8027)



###



ERC8027 provides a framework and interface of EIP8027 for NFTs - specifically ERC721 tokens to enable manual and recurring subscription service with auto expiration i.e. Subscription NFTs (SubNFTs)

---

**vitali_grabovski** (2025-09-18):

`Yes something like EIP7702 could indeed enable such feature but this is also the reason I think this standard can bring extra benefits with - since it doesn’t require the user’s EOA to delegate to an external contract which could impose extra security vectors that integrators need to consider(plus the delegated contract could contain more functions other than subscription) - while SubNFTs provide a non-wallet level standardized framework for apps to adopt subscription features in a more flexible way`

I suggest you should mention in the Motivation section that a wallet-level subscription does not solve the problem, and include possibly in the Rationale section a comparison explaining why the wallet approach fails

---

**ant** (2025-09-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vitali_grabovski/48/15798_2.png) vitali_grabovski:

> I suggest you should mention in the Motivation section that a wallet-level subscription does not solve the problem, and include possibly in the Rationale section a comparison explaining why the wallet approach fails

Yea 100%, thanks for the feedback!

---

**ant** (2026-01-28):

Hi guys I have given a second thought for this standard and I think it should be improved to be more generic so it is easier to integrate with all the common token approval methods more than just Permit2, and all of the approval methods supported by this standard should involve signing a [EIP712](https://eips.ethereum.org/EIPS/eip-712) message off-chain as token approval for example [ERC-2612](https://eips.ethereum.org/EIPS/eip-2612), [ERC-3009](https://eips.ethereum.org/EIPS/eip-3009), [Permit2](https://github.com/Uniswap/permit2), and other approval methods that could appear in the future.

TLDR: I revamped this standard for quite a bit. This interface is now more generic and easier to integrate with any token approval methods by introducing a new struct `RecurringSubscriptionData` and generalizing the whole implementation.

Any review would be greatly appreciated! Thank you!

