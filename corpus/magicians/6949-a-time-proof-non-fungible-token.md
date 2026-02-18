---
source: magicians
topic_id: 6949
title: A time proof Non-fungible Token
author: CyberForker
date: "2021-08-25"
category: Magicians > Primordial Soup
tags: [nft, token]
url: https://ethereum-magicians.org/t/a-time-proof-non-fungible-token/6949
views: 797
likes: 0
posts_count: 2
---

# A time proof Non-fungible Token

author: Cyberforker

## Simple Summary

This is a standard for time-stamp provable NFTs, which extends ERC-721.

It is called Time proof Non-fungible Token, and is referred to as tpNFT in the subsequent descriptions.

## Abstract

On the basis of the tokenURI parameter of ERC721, the plain text parameter and the encryption parameter are added, and the timestamp proof is set for the update of these three parameters.

Based on these improvements, we can provide new possibilities for NFT, enabling NFT to map and capture time-level value.

Here are some brand new applications that can be achieved by tpNFT based on this extension. I believe you can find more and more interesting applications to bring more functions to the blockchain.

1. Governance: as a proof of time stamp for governance voting, it is used to verify the validity of the vote and obtain governance incentives.

2. Invention and creation: the idea is stored on the chain to prove that the idea existed before a certain point in time. And you can temporarily hide the specific technical implementation details through Hash encryption.

3. Open source projects：similarly to previous one to used to prove the originality of their products and leave a proof of their own open source.

4. Oracle: Make predictions about the future and cast it into tpNFT with time proof ability, as a proof of personal ability, or as a certificate for receiving bonuses.

5. Identity: Participating in a series of on-chain behaviors through tpNFT, including the prophecy mentioned in the previous point, revolves around tpNFT’s timestamp proof, which has become a natural proof of identity.

6. Legacy: Binding assets to a tpNFT, others can receive part or all of the assets by submitting the preimage of HashTree. We have another EIP to solve the front running attacks.

7. Dynamic NFT: Based on the timestamp proof, we can get the interactive on-chain state that exists on the chain and the 0 Gas fee automatically changes and does not require an off-chain oracle to provide. Dynamic parameters are the internal state and attributes of tpNFT. Such features can open up new areas for games, installation art, option contracts, and so on.

8. Promise: Cast the tpNFT promise and send it to Lover, reveal the hash value on the wedding day to express your promise and love when you first met.

Summarize: The NFT of the ERC721 standard is mainly used to anchor and map things related to space, while tpNFT is used for time proof and time value.

## Replies

**CyberForker** (2021-08-29):

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/3777)














####


      `master` ← `CyberFork:master`




          opened 04:43AM - 29 Aug 21 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/9/97cbef7218101d96f78f6c58a18ba165d1ab993e.jpeg)
            CyberFork](https://github.com/CyberFork)



          [+304
            -0](https://github.com/ethereum/EIPs/pull/3777/files)







This is a standard for time-stamp provable NFTs, which extends [ERC-721](./eip-7[…](https://github.com/ethereum/EIPs/pull/3777)21.md).
Enables NFT to mapping and anchor things that have time features.
And also the time-stamp proof of NFTs can be the condition of interaction with smart contracts.
It is called Time proof Non-fungible Token and is referred to as tpNFT in the subsequent descriptions.

When opening a pull request to submit a new EIP, please use the suggested template: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

