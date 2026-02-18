---
source: magicians
topic_id: 9553
title: "EIP DRAFT: Extending ERC1155 with rentable usage rights"
author: Tech
date: "2022-06-09"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-draft-extending-erc1155-with-rentable-usage-rights/9553
views: 3113
likes: 1
posts_count: 14
---

# EIP DRAFT: Extending ERC1155 with rentable usage rights

The traditional ERC721 and ERC1155 focus more on ownership. However, NFTs as digital assets are more prominent in use than ownership. Taking artistic NFTs as an example, NFT artists may wish to rent out the use rights of their works to media companies in the allotted time, or NFT musicians may wish to make their music available to listeners as per playing duration.

Therefore, to better serve NFT developers to meet such needs and develop more sophisticated NFT products, we propose directly introducing rentable usage rights to complement the ERC standard.

There is similar accomplishment in eip-2615 which extended ERC721. But can’t reach the charactor of ERC1155.

## Replies

**cryptoERA** (2022-06-11):

good to see this. I am searching for rentable ERC1155 fulfilment, do you have definable rent rights ? In some cases , i want to rent out the NFT picture many times at the same time whereas others only once.

---

**Tech** (2022-06-12):

sure you need to assign the amount of rent rights, from 1 to any number you like.

the corresponding function as follows:

```auto
    /**
     * @notice Function to rent out usage rights
     * @param from The address to approve
     * @param to The address to rent the NFT usage rights
     * @param id The id of the current token
     * @param amount The amount of usage rights
     * @param expires The specified period of time to rent
     **/
    function safeRent(
        address from,
        address to,
        uint256 id,
        uint256 amount,
        uint256 expires
    ) external;
```

---

**simonyang2022** (2022-06-15):

So you have finished the contract code right? hope to have function list of the contract .

---

**Tech** (2022-07-01):

yeah, the proposal was abstracted from our products. Comprehensive documents and SDK will push to the market this month.

---

**taro2potato** (2022-08-03):

Is this eip compatible with ERC721?

---

**Tech** (2022-08-10):

Sure, it’s compativle with ERC-721 and ERC-1155. The first product is about to launch soon.

---

**wighawag** (2022-08-13):

Hey thanks for this proposal.

Did you consider using a registry approach like I mentioned here : [EIP4907: ERC-721 User And Expires Extension - #19 by 0xanders](https://ethereum-magicians.org/t/eip4907-erc-721-user-and-expires-extension/8572/19)

this would allow old NFT contract to be supported

Also I think we could probably support both ERC-1155 and ERC-721 in this proposal : [ERC721 Lease: allowing owner to rent NFT to other](https://ethereum-magicians.org/t/erc721-lease-allowing-owner-to-rent-nft-to-other/9965)

---

**Tech** (2022-08-15):

thanks for you proposal, and my point is : the NFT can be rented by more than one user and the number can be defined by the NFT creator.

EIP-4907 has only one usage right in different usage scenario.

---

**wighawag** (2022-08-15):

Oh of course, I was not suggesting to use 4907, nor even my own [proposal](https://ethereum-magicians.org/t/erc721-lease-allowing-owner-to-rent-nft-to-other/9965) without modification to support ERC-1155.

One big advantage of my proposal is the use of a registry that if applied to your EIP would allow it to support ERC-1155 that are already deployed. It would also not require any extra code to support renting.

---

**Tech** (2022-08-31):

Good  idea! Why not submit your proposal to ethereum? We have an ecological partner who is developing a new NFT marketplace and will support multiple NFT extentions like EIP-5187, EIP-4907, EIP-5006 and more.

---

**ivyattheoldmill** (2022-09-23):

I believe leasing will bring many use cases, whether in DeFi, Metaverse, or the real world.

What I am curious about is the circulation of rented NFTs. If users don’t want to rent anymore, is there a way they can return the NFT to the owner early, or “re-rent” the NFT to someone else? When the lease term set by the owner does not match the user’s needs, it may lead to the user’s reluctance to lease.

Have you ever wondered how to solve this problem?

---

**TehilaFavourite** (2022-09-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivyattheoldmill/48/7269_2.png) ivyattheoldmill:

> is there a way they can return the NFT to the owner early

Here, there should be a functionality to do that, where the user can revoke the NFTs rented back to the owner, with a check to ensure that the balance is not refunded, or else you have the

functionality to request the owner’s permission to refund the balance of days remaining.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivyattheoldmill/48/7269_2.png) ivyattheoldmill:

> Here, you will also need a separate function that can permit the user to rent it out possibly maybe with the owner’s permission or not.
> “re-rent” the NFT to someone else?

---

**ivyattheoldmill** (2022-09-29):

Thanks for helping me understand this. Yes, I think the rental market will become more prosperous if there is a way to do “early return” and “re-rent” by adding some simple functionalities. How to secure a refund is also an interesting topic, I can’t think of a viable way to do this…

