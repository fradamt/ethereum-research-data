---
source: magicians
topic_id: 8531
title: "EIP-4885: Subscription Token Standard"
author: julesl23
date: "2022-03-07"
category: EIPs
tags: [erc, nft, token]
url: https://ethereum-magicians.org/t/eip-4885-subscription-token-standard/8531
views: 3815
likes: 1
posts_count: 13
---

# EIP-4885: Subscription Token Standard

Hi,

I’ve written up an EIP proposal “Subscription Token Standard for NFTs and Multi Tokens”. Been busy lately but this proved very useful in my own dapp so thought I’d share.

One of the features that I really like about it (being as unbiased as possible) is the notion of subscriptions as a thing of value, which it has as it is exchanged for ERC-20 tokens. And if an implementer so desired, they are able to make them tradeable by implementing the remaining methods of ERC-20 that the specification does not cover.

I kept the spec minimal so that it can be as general purpose as possible. I also kept my mind open to future uses of NFTs and tried the best I could to ensure that this standard would cope with that.

It works by linearly reducing the balance of a subscriber’s subscription tokens held, until the balance is zero meaning that the subscription has expired. Whatever subscription service that was subscribed to can simply run the *balanceOf* method and disable when zero, or at least until more subscription tokens are bought to top the balance up again.

For example, an implementation mints an amount of subscription token that totals to one subscription token per day of the subscription period length paid for by the subscriber; for example a week would be for seven subscription tokens. The subscription token balance then decreases automatically at a rate of one token per day continuously and linearly over time until zero.

```auto
interface ISubscriptionToken {
    /**
        @dev This emits when the subscription token constructor or initialize method is
        executed.
        @param name The name of the subscription token
        @param symbol The symbol of the subscription token
        @param provider The provider of the subscription whom receives the deposits
        @param subscriptionToken The subscription token contract address
        @param baseToken The ERC-20 compatible token to use for the deposits.
        @param nft Address of the `nft` contract that the provider mints/transfers from.
        All tokenIds referred to in this interface MUST be token instances of this `nft` contract.
    */
    event InitializeSubscriptionToken(
        string name,
        string symbol,
        address provider,
        address indexed subscriptionToken,
        address indexed baseToken,
        address indexed nft,
        string uri
    );

    /**
        @dev This emits for every new subscriber to `nft` contract of token `tokenId`.
        `subscriber` MUST have received `nft` of token `tokenId` in their account.
        @param subscriber The subscriber account
        @param tokenId MUST be token id of `nft` sent to `subscriber`
        @param uri MUST be uri of the `nft` that was sent to `subscriber` or empty string
    */
    event SubscribeToNFT(
        address indexed subscriber,
        uint256 indexed tokenId,
        string uri
    );

    /**
        @dev Emits when `subscriber` deposits ERC-20 of token type `baseToken` via the `deposit method.
        This tops up `subscriber` balance of subscription tokens
        @param depositAmount The amount of ERC-20 of type `baseToken` deposited
        @param subscriptionTokenAmount The amount of subscription tokens sent in exchange to `subscriber`
        @param subscriptionPeriod Amount of additional time in seconds subscription is extended
    */
    event Deposit(
        address indexed subscriber,
        uint256 indexed tokenId,
        uint256 depositAmount,
        uint256 subscriptionTokenAmount,
        uint256 subscriptionPeriod
    );

    /**
        @return The name of the subscription token
    */
    function name() external view returns (string memory);

    /**
        @return The symbol of the subscription token
    */
    function symbol() external view returns (string memory);

    /**
        @notice Subscribes `subscriber` to `nft` of 'tokenId'. `subscriber` MUST receive `nft`
        of token `tokenId` in their account.
        @dev MUST revert if `subscriber` is already subscribed to `nft` of 'tokenId'
        MUST revert if 'nft' has not approved the `subscriptionToken` contract address as operator.
        @param subscriber The subscriber account. MUST revert if zero address.
        @param tokenId MUST be token id of `nft` contract sent to `subscriber`
        `tokenId` emitted from event `SubscribeToNFT` MUST be the same as tokenId except when
        tokenId is zero; allows OPTIONAL tokenid that is then set internally and minted by
        `nft` contract
        @param uri The OPTIONAL uri of the `nft`.
        `uri` emitted from event `SubscribeToNFT` MUST be the same as uri except when uri is empty.
    */
    function subscribeToNFT(
        address subscriber,
        uint256 tokenId,
        string memory uri
    ) external;

    /**
        @notice Top up balance of subscription tokens held by `subscriber`
        @dev MUST revert if `subscriber` is not subscribed to `nft` of 'tokenId'
        MUST revert if 'nft' has not approved the `subscriptionToken` contract address as operator.
        @param subscriber The subscriber account. MUST revert if zero address.
        @param tokenId The token id of `nft` contract to subscribe to
        @param depositAmount The amount of ERC-20 token of contract address `baseToken` to deposit
        in exchange for subscription tokens of contract address `subscriptionToken`
    */
    function deposit(
        address subscriber,
        uint256 tokenId,
        uint256 depositAmount
    ) external payable;

    /**
        @return The balance of subscription tokens held by `subscriber`.
        RECOMMENDED that the balance decreases linearly to zero for time limited subscriptions
        RECOMMENDED that the balance remains the same for life long subscriptions
        MUST return zero balance if the `subscriber` does not hold `nft` of 'tokenId'
        MUST revert if `subscriber` is not an approved operator of `nft`
        MUST revert if subscription has not yet started
        When the balance is zero, the use of `nft` of `tokenId` MUST NOT be allowed for `subscriber`
    */
    function balanceOf(address subscriber) external view returns (uint256);
}
```

This spec does create some implications on control of NFT lifetimes. This area is probably not as or yet to be fully developed by existing EIPs, and I don’t think it clashes with anything out there?

My particular use case for this proposal is numerous from:

Streaming services

Club memberships

Season tickets etc.

Other use cases I see are:

Renting of digital assets

Fixed rate to variable income in DeFi

etc.

My main motivation was to come up with a way to help loosen the stranglehold around content creators so they can administer their own subscription service eco system.

But let me know if you feel that this is something that could be useful? If there is anything that could be improved, or if there is an issue, or perhaps something that you don’t understand? etc.

Cheers

## Replies

**julesl23** (2022-03-07):

[![Subscription Tokens for NFT and Multi Tokens](https://ethereum-magicians.org/uploads/default/optimized/2X/5/5722a6de3fdfd60cffe8c3822372e7dc45d8999f_2_690x414.png)Subscription Tokens for NFT and Multi Tokens1200×721 43.6 KB](https://ethereum-magicians.org/uploads/default/5722a6de3fdfd60cffe8c3822372e7dc45d8999f)

I’m thinking that this diagram might help cement the idea of subscription tokens.

---

**julesl23** (2022-03-08):

The EIP proposal (not yet in draft) can be found here:

https://github.com/julesl23/EIPs/blob/master/EIPS/EIP-Subscription_Token_Standard.md

---

**julesl23** (2022-03-18):

**Workflow of EIP-4885 (with pseudo code)**

This is done once for each type of subscription service offered by provider:

1. Provider deploys an ERC1155 contract
2. Provider deploys a contract that implements ISubscriptionToken
3. Provider executes ERC1155.setApprovalForAll(address(SubscriptionToken), true)

Then for each subscriber:

4. Mint the ERC1155 NFT tokenId (increment tokenId each time) to and paid for by subscriber

5. Subscriber executes SubscriptionToken.subscribeToNFT(subscriber, tokenId, uri)

6. Subscriber buys an amount of SubscriptionToken

The rule is that once the linearly depreciating SubscriptionToken.balanceOf() falls to zero, then the subscriber’s subscription expires. Subscriber can buy more SubscriptionToken to top up the balance at any time.

The uri could be a link to NFT tokenId’s metadata for the legal agreement between provider and subscriber, or a digital asset etc.

If SubscriptionToken implements ERC-20 then it can be traded on secondary markets, or sent as gifts to others, or be refundable etc.

Hopefully this makes the steps clearer,

Cheers

---

**julesl23** (2022-03-23):

Proposal moved to draft: https://eips.ethereum.org/EIPS/eip-4885

---

**AntonioHoffert** (2022-07-10):

Hello Jules, I have been writing a subscription smart contract from scratch and just found your EIP.

I have some contributions, what is the best way to present them and discuss with you?

---

**julesl23** (2022-07-10):

You’re already in the right place ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**ricdikulous** (2022-07-27):

> The subscription token balance then decreases automatically at a rate of one token per day continuously and linearly over time until zero.

I’m curious how does this mechanism work under the hood? Do you suggest burning the tokens?

---

**julesl23** (2022-08-07):

Sorry for delay. I’ve been so busy with the launch of a Web3 platform.

Here’s some pseudo code:

```auto
    function balanceOf(address subscriber) public
        view
        returns (uint256 balance)
    {

       uint256 amountTokensBurnt = ((block.timestamp - _burnFromTimestamps[subscriber])
			* 10**18 * _price)
			/ _perPeriod;

       if (tokenBalance > amountTokensBurnt)
            balance = tokenBalance - amountTokensBurnt;
       else balance = 0;
	}
```

Hope that helps.

---

**Ivans1310** (2022-08-17):

Hi,

I have a few of questions:

1. Why SubscriptionToken contract must have approval as an operator of the nft when you subscribe or deposit? SubscriptionToken will perform any transfer action of the tokenId.
2. Does the burning of the SubscriptionTokens happen on the Deposit function?
3. On balanceOf, Isn’t It enough requering subcriber holds tokenId?, why does it require that subscriber be the operator of the token as well?
4. The subscritption is set as started  once the tokenId is subscribed using subscribeToNFT function? or when a deposit is done for that tokenId?

Thank you.

---

**julesl23** (2022-08-19):

> Why SubscriptionToken contract must have approval as an operator of the nft when you subscribe or deposit? SubscriptionToken will perform any transfer action of the tokenId.

Allows implementers to check that the subscription token contract has the approval from the NFT owner to subscribe to it.

> Does the burning of the SubscriptionTokens happen on the Deposit function?

In the `deposit` function, the balance of the subscription token for the subscriber increases to extend the length of the subscription period. There is no gas needed to actually burn tokens, instead can note the block timestamp of the last deposit in a `mapping` and the new balance as another `mapping` for the subscriber. Then `balanceOf` function returns the result of the balance decrease as a linear function between the stored block timestamp and the current block timestamp. So you need to also know the rate of balance decrease per time period.

> On balanceOf, Isn’t It enough requering subcriber holds tokenId?, why does it require that subscriber be the operator of the token as well?

The subscriber doesn’t need to be an NFT operator, just the subscription token contract. Thanks, I better remove that from the spec.

> The subscritption is set as started once the tokenId is subscribed using subscribeToNFT function? or when a deposit is done for that tokenId?

It is from the `deposit` function when the subscription token balance increases from zero to an amount greater than zero.

---

**Ivans1310** (2022-08-24):

Thank you for your replies. Everything was clear for me.

However, in your first reply,  I think it is necessary to give the approval to the SubscriptionToken Contract. Because in this case, as I understand,  subscribeToNFT function will store  subscribers and the tokenId in a mapping that relates subscribers to TokenIds. And to populate that mapping the approval is not necessary

---

**julesl23** (2022-08-28):

Depends on your implementation.

If for example you own the NFT service subscribed to that is an ERC-1155, then another implementation could be in the `subscribeToNFT` function, mint the subscriber an NFT token with uri that points to terms and conditions personalised for the subscriber.

