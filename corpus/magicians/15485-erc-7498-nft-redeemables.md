---
source: magicians
topic_id: 15485
title: "ERC-7498: NFT Redeemables"
author: ryanio
date: "2023-08-18"
category: EIPs
tags: [erc, nft]
url: https://ethereum-magicians.org/t/erc-7498-nft-redeemables/15485
views: 2659
likes: 2
posts_count: 10
---

# ERC-7498: NFT Redeemables

Discussion thread for [ERC-7498: NFT Redeemables](https://eips.ethereum.org/EIPS/eip-7498).

> Abstract
> This specification introduces a new interface that extends ERC-721 and ERC-1155 to enable the discovery and use of onchain and offchain redeemables for NFTs.
>
>
> Motivation
> Creators frequently use NFTs to create redeemable entitlements for digital and physical goods. However, without a standard interface, it is challenging for users and apps to discover and interact with these NFTs in a predictable and standard way. This standard aims to encompass enabling broad functionality for:
>
>
> discovery: events and getters that provide information about the requirements of a redemption campaign
> onchain: token mints with context of items spent
> offchain: the ability to associate with offchain ecommerce orders (through redemptionHash)
> trait redemptions: improving the burn-to-redeem experience with ERC-7496 Dynamic Traits

## Replies

**randyanto** (2023-08-29):

Hi [@ryanio](/u/ryanio), is there a possibility that we could collaborate on this proposal? Previously, we proposed [ERC-6672](https://eips.ethereum.org/EIPS/eip-6672), which is now in the Final status. I believe our combined effort could greatly benefit the phygital vertical.

---

**wwhchung** (2023-09-06):

[@ryanio](/u/ryanio) and [@randyanto](/u/randyanto)

For both these EIP’s, it’s unclear to me whether or not the extension to the 721/1155 spec need to be part of the underlying 721/1155 contract.

If so, wouldn’t it be better if the spec were around the ability to add a redemption to a 721 or 1155 in general?

i.e. ANYONE could deploy a new Redemption contract for any existing 721/1155 and the ecosystem would understand it.

Redemptions or providing incentives for an existing token holder group doesn’t have to be made exclusively by the initial token creator.

---

**wwhchung** (2023-09-06):

IMO, redemptions, or the concept of redemptions, shouldn’t be extensions of 721/1155.  Rather, they should be new primitives which take in 721/1155/erc20’s as input, and can result in an output as well (could be an output to the root token if natively supported, or could be an output to it’s own construct data).

---

**randyanto** (2023-09-11):

Thanks for your comment.

> Redemptions or providing incentives for an existing token holder group doesn’t have to be made exclusively by the initial token creator.

This is exactly what we have in our mind when we designed ERC-6672. That’s why if you look closely to ERC-6672, you can find that we mentioned about the `operator`. These operators are redemption platforms (operators). Note that we try to design the standard so that it can fit as many use-cases as possible. In the implementation of ERC-6672, it’s also possible for initial token creator to give permission (or you can say whitelist) the operators that can provide redemption service for the NFT holders.

> i.e. ANYONE could deploy a new Redemption contract for any existing 721/1155 and the ecosystem would understand it.

I believe it’s important to save the redemption status in the NFT smart contract instead of putting the redemption status in the Redemption contract so that secondary marketplace can immediately show the status of the redemption (e.g. `isRedeemed()` → `TRUE` or `FALSE`).

We can discuss more in ERC-6672 post if you’re interested.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/randyanto/48/8782_2.png)

      [EIP-6672: Multi-redeemable NFTs](https://ethereum-magicians.org/t/eip-6672-multi-redeemable-nfts/13276) [EIPs](/c/eips/5)




> This EIP proposes an extension to the ERC-721 standard for Non-Fungible Tokens (NFTs) to enable multi-redeemable NFTs. This extension would allow an NFT to be redeemed in multiple scenarios for either physical or digital objects and maintain a record of its redemption status on the blockchain.
> Motivation
> ERC-5560 enables only one-time redemption of an NFT, which means the same NFT cannot be re-used for another redemption from different campaigns or events.
> Proposed Improvement
>
> Utilize the com…

---

**wwhchung** (2023-09-11):

I can post there, but that aspect is what I don’t agree with (that redemption status needs to be stored with the nft). Decoupling it allows for the ability to create new redemption rules and behaviors in the future (Eg can redeem X times if you have some set of nft’s, etc).

I also don’t think it’s necessary to do this as long as there are well defined event types that indexers recognize which identify where to look/who to interact with for specific redemptions.  Decoupling also allows for backwards compatibility with existing nft’s.

Note that redemptions don’t have to be limited to a single usage or single type.

Also I believe permissionless redemptions are highly valuable (ie being able to offer redemptions for a specific nft community).

---

**0xWizardOf0z.eth** (2023-09-11):

This is how we handle redemptions with InfinityMint.eth.



      [twitter.com](https://twitter.com/im_not_art/status/1694855447105167752?s=20)





####

[@im_not_art](https://twitter.com/im_not_art/status/1694855447105167752?s=20)

  🛠️🚢🚀

  https://twitter.com/im_not_art/status/1694855447105167752?s=20

---

**ryanio** (2023-09-11):

> For both these EIP’s, it’s unclear to me whether or not the extension to the 721/1155 spec need to be part of the underlying 721/1155 contract.

The purpose of this EIP is to create a standard that can be built into the token contract itself, keeping gas costs lower by having fewer external contracts involved.

> If so, wouldn’t it be better if the spec were around the ability to add a redemption to a 721 or 1155 in general?

Yes we definitely want to support redemptions across tokens already deployed. This is why we developed a registry-like version of this EIP as [SIP-14: Redeemable Contract Offerer](https://github.com/ProjectOpenSea/SIPs/blob/main/SIPS/sip-14.md) that contains both ERC-7496 Dynamic Traits and ERC-7498 NFT Redeemables together. This means that anyone (including non-token owners) who wants to set up a redemption campaign does not need to deploy a new contract, only register the campaign with the Redeemable Contract Offerer which will emit the same events as the EIPs for external apps to pick up and understand.

---

**ryanio** (2023-09-11):

[@randyanto](/u/randyanto) thanks for jumping into the discussion! ERC-6672 is very cool, however it misses some functionality we are looking for:

- We wanted to allow for complex multi-redemption scenarios like, redeem a token plus another ERC721 or ERC1155 or ERC20 (or eth!) for the redemption. I believe this would work with ERC-6672, however it is nontrivial to “discover” these campaigns and what their requirements are. This is why we have a getCampaign getter and CampaignUpdated event to understand what is necessary for the redemption.
- We didn’t want to provide a way to “cancel” a redemption as an onchain token may have been minted or offchain order completed. This is why we have a “signer” for the redemption, that can provide a signature to guarantee the redemption has been validated, so there should be no reason to backtrack on a state change of a redemption, as that can cause cascading problems depending on the type of redemption.
- We wanted to provide this EIP to be accessible in a registry format for tokens already deployed who wanted to augment with Dynamic Traits or Redeemable functionality. (see SIP-14: Redeemable Contract Offerer)
- We wanted to provide a standard interface (mintRedemption in our spec) that tokens can implement to mint new tokens based on a redemption.

For simple redemption scenarios, I do think ERC-6672 is designed nicely, although I think there is some problematic scenarios with the “cancel” function.

---

**chuboyu** (2023-09-13):

Hi [@ryanio](/u/ryanio) for the discussion. However I do think you some important consideration on the design of ERC6672. As one of the authors I would like to elaborate more on the benefits of extending existing standards with small blocks of functionality rather than rebuilding a bundle of complete logic into a pack.

As a standard to be adopted by the community, we believe it should be simple yet extensible, rather than complex but specific. Complex mechanisms may build on top and we should make it generally re-usable to most business logic if possible.

First of all, ERC6672 intend to solve only the redemption tracking part, and we have received many feedbacks to polish the interface for it to be adoptable towards many businesses including distributors and suppliers. As simple it may seem, it is able to support complex logic, and we believe it should be supported with future implementations or standards.

Secondly, the redemption part of 7498 is extremely similar to 6672, with 6672 able to support more complex business structures with the operator management (which also can be freely implemented) As for the cancel part it is highly demanded from all sorts of providers, suppliers and creators for their “real world operation and business models”. The redemption record is still immutable, only that the aggregated final status is modified.

Thirdly, We should try to reuse interfaces so that we can build in consensus, rather than having a different standard for each problem. Linking it with dynamic trait is a great plus and I believe we can discuss the implementing to make it work. However for interfaces (like the cancel mentioned), we should still think more generally, and if unwanted in certain scenarios, simply deactivate it during implementation. For example, many builders of Soul Bound Tokens still uses 721 and follows Opensea’s metadata standard. They simply block the transfer part which they no longer needed.

To sum up, I believe it is beneficial to extend 7498 from 6672, so that the existing and growing mass network of real life scenarios, IOTs, hardwares and brands can be connected to the novel mechanisms that you and us are building.

Final touches, we also feel it quite good to have on chain campaign specifications. However we proposed 6672 to focus on the redemption handling because there are existing privilege specifying standards that we think is quite general and extensible. Have you looked at any of those and what’s your thoughts on the major differences ?

