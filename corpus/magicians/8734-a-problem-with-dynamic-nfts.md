---
source: magicians
topic_id: 8734
title: A problem with Dynamic NFTs
author: Saarule
date: "2022-03-28"
category: EIPs
tags: [nft, token, dynamic]
url: https://ethereum-magicians.org/t/a-problem-with-dynamic-nfts/8734
views: 1067
likes: 1
posts_count: 3
---

# A problem with Dynamic NFTs

**TL;DR** There is an issue with the way opensea and other NFT marketplaces retrieve their metadata and present it to their users when it comes to Dynamic NFTs.

Recently I built a few projects that are focused on dynamic NFTs.

When I created my most recent NFT game (Aquatic Wars), I found an issue with how opensea retrieves and presents the data to its users.

Opensea’s main assumption is that all NFTs are static, which means they are retrieving data solely on the user’s request. That is a big problem for dynamic NFTs as their metadata and image might very often frequently change.

Let’s have a look at [Aquatic Wars](https://www.aquaticwars.com/), as it emphasizes the importance of the issue. This project has three levels of dynamicness to the player’s NFTs.

Some properties in the appearance of the NFT are changing every day (The number of days appears on the top side of the NFT’s image) some properties only change when there is an interaction with the smart contract (When you eat someone’s fish, their fish is disappearing from the NFT’s image) and some should change (at least in theory) every millisecond (The inner color of the fish should change with every call to the tokenURI function).

As you can see, by going to opensea, the data is not refreshing often enough in order to present all those changes to the user, and hence, making the game unplayable. In fact, the NFT’s metadata as it appears to the user is not changing at all, unless, of course, if the user is requesting that. That is far from optimal and doesn’t make sense from a developer and a user perspective.

What I propose, is a new protocol and EIP for dynamic NFTs that can extend the ERC721 standard so that NFT marketplaces will know when the collection is a collection of dynamic NFTs and will know to retrieve the metadata at a faster rate as predefined by the developer.

I would love to hear your thoughts on the topic.

I also think I know how to solve this issue elegantly for future developers through an EIP and a new standard for dynamic NFTs, and would love some help from someone who has already been through the process of creating a successful EIP as this is the first time I’m creating one.

## Replies

**JamesB** (2022-11-10):

Hi Saarule, we have also run into this issue which we have fixed locally in our wallet (AlphaWallet) however agree that we can push an update for this.

I would propose that we add a ‘MetadataUpdate’ event like this:

```auto
event MetadataUpdate(uint256 tokenId);
event ContractMetadataUpdate();
```

Both events are needed, for example an ‘NFT reveal’ style art exhibition where minters/receivers just receive a blank NFT until the artwork is revealed at a later data. Also, the contract art may update - this is something that Opensea doesn’t handle at all; if you update contract metadata it never refreshes on Opensea. Updating Token metadata can be refreshed manually, but to optimise this we should add the MetadataUpdate event.

---

**alenhorvat** (2022-11-10):

Hi.

What you’re describing is an issue with a platform, in this case, OpenSea.

The issue you present is directly linked to an issue I described here: [NFT minting standardisation - protecting authors, buyers, sellers](https://ethereum-magicians.org/t/nft-minting-standardisation-protecting-authors-buyers-sellers/11637/2)

Namely, if the NFT changes, how do you ensure the owner, and later owner/buyer/seller, that the content for which he/she bought the NFT did not change?

IMO, the problem is solvable by

a) assigning a unique id to the item that never changes and ensuring everyone that the id is linked to a specific item (within the game, for example)

b) using the image_uri or by adding a dynamic_image_uri attribute to the metadata, which would signal that the content might change

In my view, point a) is crucial to prevent stealing NFTs, misclaiming authorship, and other tricks on owners/buyers/sellers.

Edit:

Another, probably more proper, solution would be to create 1 NFT per unique attribute in the game and introduce an “aggregated NFT” – an NFT, that is composed of several other NFTs. This way you can ensure that the items linked to NFTs don’t change, yet you can build an NFT (aggregated NFT) that represents a character in the game.

