---
source: magicians
topic_id: 19022
title: "ERC-7644: ERC-721 Name Registry Extension"
author: bizliaoyuan
date: "2024-03-02"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7644-erc-721-name-registry-extension/19022
views: 1113
likes: 0
posts_count: 3
---

# ERC-7644: ERC-721 Name Registry Extension

[github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/292)














####


      `master` ← `chenly:erc-name`




          opened 04:53PM - 01 Mar 24 UTC



          [![](https://avatars.githubusercontent.com/u/13716?v=4)
            chenly](https://github.com/chenly)



          [+197
            -0](https://github.com/ethereum/ERCs/pull/292/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/ERCs/pull/292)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.












## Abstract

This standard enhances ERC-721 by giving each token a unique name and an expiry date, allowing other token holders to claim the name once it expires.

## Rationale

Here are a few design decisions and why they were made:

#### Intuitive Token IDs

Current token IDs are predominantly numeric, lacking intuitiveness. The extension of the ERC-721standard to support Named Tokens aims to facilitate the acceptance and use of this standard within the NFT marketplace. By moving beyond mere numbers to include distinctive names, token IDs can more directly reflect the unique identity or value they represent.

#### Expanding NFT Use Cases

By allowing each token to possess a unique name, we unlock new application scenarios in ecosystems built around scarce username resources, such as domain name registration systems. In such scenarios, domain owners can demonstrate ownership directly by holding the corresponding token, thereby broadening the application spectrum and enhancing the value of NFTs.

## Replies

**Kureev** (2024-03-05):

I wonder which exact problem would that solve? Right now you can set an asset name in the metadata, isn’t it enough?

As for the proposed solution for the domain names, I don’t see why they can’t be attached to the account directly through your registration system. In the proposed solution you add an extra layer: registry → nft → account and suggest to determine registration based on the token if I understand it correctly. However, you also suggest to “expire” the name attached to the token. In the case of the expiration, what would token indicate/what would be the value of the token?

On the other hand, you can write a domain name registry contract and create a simple `mapping(address => Registration)` where `Registraction` is a struct with params like expiration date etc. This way you don’t need tokens to prove ownership, don’t have a problem giving meaning to the tokens that are expired and there is no need to extend the standard.

However, if you’d like to use token as collateral or transfer ownership rights through the NFT transfer I think you can set an expiration date on the token itself by checking block time upon transferring attempt and again, map token id to the domain name in another smart contract. This way you achieve the same goals without extending the contract.

I think this is similar (in a way) to [my Metadata Manager ERC](https://ethereum-magicians.org/t/erc-7646-metadata-management-for-nfts/19027): you can build an abstraction that works on top of existing standard instead of extending the standard itself. The only difference in your use-case is adding logic for the expiration and duplication checks unless I misunderstood the idea.

---

**SamWilsn** (2024-03-05):

`TokenMintedWithName` would be emitted alongside the `Transfer` event from ERC-721? Seems redundant.

