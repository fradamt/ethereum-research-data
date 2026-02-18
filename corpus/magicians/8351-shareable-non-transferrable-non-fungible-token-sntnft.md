---
source: magicians
topic_id: 8351
title: Shareable non-transferrable non-fungible token, sntNFT
author: yaruno
date: "2022-02-18"
category: EIPs
tags: [nft, shareable, sntnft]
url: https://ethereum-magicians.org/t/shareable-non-transferrable-non-fungible-token-sntnft/8351
views: 839
likes: 0
posts_count: 1
---

# Shareable non-transferrable non-fungible token, sntNFT

Greetings fellow Ethereum Magicians!

I’m working on an EU project where we are researching Accouting Technologies for Anti-Rival Coordination and Allocation. One of our goals is to find novel and innovative ways to capture, quantify and account value in sharing economies. If you’d like to know more you can check us at [atarca.eu](https://www.atarca.eu) and some of my initial thoughts from our project at [medium](https://medium.com/@jarno.marttila/about-anti-rival-goods-and-incentives-9946dbcc6bdb) .

In relation to the project and to the wider Ethereum ecosystem we’ve been concepting a new type of token that we believe could be the first step of capturing and allocating some anti-rival value in our pilot experiments. We are calling this token a shareable non-transferrable non-fungible token, shortly a sntNFT. As the name indicates this token cannot be transferred, or used in traditional way in an exchange economy as a tool to exchange goods and services. However it can be shared, or in technical terms re-minted to a new party. This new type of token may require extending existing token standards such as ERC-721 or ERC-1155 or developing a new kind of token standard for which we are considering on making a draft proposal for.

To give a bit of context to one of our use cases, Streamr Acknowledgment Token use case, we are building a pilot to target Streamr projects community to incentivize communitys code and non-code contributions. We believe that with this new type of shareable token the community members can be recognized for their contributions and they can further share the recognition of e.g. what has influenced their contribution to wider community.

In terms of sharing, we have though of two different sharing modalities, a push type of permissioned sharing and a pull type of permissionless sharing. A push type of sharing would be possible by the contract owner and a token holder. A contract owner can mint new shareable tokens. A token holder can remint new ‘versions’ of his or her token to a recipient. However tokens cannot be shared if they are not owned.

In the pull type of approach, tokens can be freely shared or re-minted by anyone to ones wallet. Like collecting pokemons, you choose which token you like and you mint a version of it for yourself.

These two modalities serve different purposes, to simplify, one indicating a contribution or a merit and another one the popularity of a contribution or a merit. These different sharing modalities may require different types of contracts and along the line maybe even different standards.

As the token is still on idea and conceptual stage we would like to know your initial thoughts about this type of token. Do you see it could be a new type of token standard or an extension to an existing standard? Can you think of other use cases for such token beyond what we briefly introduced? Or how about technical limitations for such token? All feedback is greatly appreciated.
