---
source: magicians
topic_id: 7885
title: Delegator Extension That Enables ERC721 to be loaned
author: AFKDAO
date: "2022-01-04"
category: ERCs
tags: [erc, nft, erc-721]
url: https://ethereum-magicians.org/t/delegator-extension-that-enables-erc721-to-be-loaned/7885
views: 977
likes: 1
posts_count: 2
---

# Delegator Extension That Enables ERC721 to be loaned

Hi there.

ERC721 is widely used in blockchain games. I think it’s good to NFTized game accounts and game equipment so that users can own their own assets. However, I don’t think it’s a good experience for every player to buy an NFT before playing the game. Sometimes we just want to try the game. Under such circumstances, if we can borrow NFT to play the game in a safe and convenient way, the experience will be much better.

In order to solve this problem, I thought of a method, that is, add a delegator extension to ERC721. Specifically, like the following code.

`mapping(uint256 => address) private _delegators;`

`function setDelegator(address delegator, uint256 tokenId)`

If I want to borrow an NFT from you, you just set me as the `delegator` of your NFT. It’s safe for you to do it, cause I don’t have any permission to transfer or approve your NFT.

What a delegator can do is defined by the game developers, or the utility NFT developers. If developers are willing to adopt this extension, they need to add the identification and processing of the delegator in the code.

I will develop specific implementations and examples in the next. I would also like to get feedback from everyone ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

## Replies

**Daniel-K-Ivanov** (2022-02-07):

Hi AFKDAO,

I am glad that you have noticed the same need for explicit role for NFTs to address renting of ERC721s. Your proposal seems very similar to what I have described and has been merged as EIP4400.

You can add your comments/thoughts in the Discussion section here and lets see whether the proposed EIP4400 fulfils your needs:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/daniel-k-ivanov/48/4799_2.png)

      [ERC-4400: ERC-721 Consumer Extension](https://ethereum-magicians.org/t/erc-4400-erc-721-consumer-extension/7371) [ERCs](/c/ercs/57)




> Abstract
> This specification defines standard functions outlining a consumer role for instance(s)
> of ERC-721. An implementation allows reading the current consumer for a
> given NFT (tokenId) along with a standardized event for when an consumer has changed. The proposal depends on and
> extends the existing ERC-721.
> Motivation
> Many ERC-721 contracts introduce their own custom role that grants permissions
> for utilising/consuming a given NFT instance. The need for that role stems from the fact tha…

I will update the EIP in the coming days with the new feedback that we have received from the community.

