---
source: magicians
topic_id: 7923
title: "EIP-4635: Semi-fungible token standard"
author: linvictor88
date: "2022-01-07"
category: EIPs
tags: [nft, sft]
url: https://ethereum-magicians.org/t/eip-4635-semi-fungible-token-standard/7923
views: 2064
likes: 2
posts_count: 5
---

# EIP-4635: Semi-fungible token standard

Hi all,

I would like to collect your feedback on [EIP-4635](https://github.com/ethereum/EIPs/pull/4635) request. It suggests a new standard to manage semi-fungible tokens.

Semi-fungible token (SFT) can be both fungible and non-fungible during its lifecycle. For example, one software company issues multiple types of licenses for their different levels of software service use, each type of licenses are fungible (FT), while these licenses will turn to non-fungible token (NFT) after delivering them to customers with unique id and expired time.

semi-fungible token (SFT) is widely used in common life including nft/software/music/membership licensing, concert tickets and so on, so it’s important if we have one standard specially for SFT. semi-fungible token is cited in ERC-1155, but ERC-1155 maybe not appropriate for SFT as following reasons:

- ERC-1155 requires the smart contract to ensure the quantity as 1 to represent NFT which is not nature. Meanwhile, the ownership, which is one of the important attribute in NFT, is hard to track with ERC-1155.
- By checking semi-fungible token scenarios, generally, there are no requirements to have more than one types of NFT in the single smart contract, such as mixing concert tickets and software licenses. Even if there are such requirements, the type can be defined in NFT metadata.
- NFT usually has different values with fungible token in SFT, which needs separate approvals.

Meanwhile, none of present ERCs has the transition from fungible token to non-fungible token. It’s necessary to define a standard interface specially for SFT. SFT can manage multiple types of fungible tokens and the transition from FTs to NFTs. SFT also defines different approvals for FT and NFT. There are many scenarios which depend on SFT. For example, concert tickets can be fungible tokens which own the same right to watch a show, but it will turn to NFT once it is delivered to the audience with the unique seat number and owner name.

Details refers to the pull request and it’s very appreciated for your comments and suggestions.

## Replies

**julesl23** (2022-01-08):

I’m thinking that concert tickets is a good use case for ERC-1155 anyway.

Each token id (with quantity 1) of ERC-1155 is representative of a ticket. It can point to metadata that includes concert name, date, and seat number.

To the outside real world once date has passed then it can become purely a collectible, but that is also indicated from on-chain and immutable storage for the metadata anyway.

Also recipient name is not on the ticket usually anyway so its fine to batch mint the concert ticket supply. The fact that the ticket (nft token) is in your account and matches an off-line system the provider has, is enough.

---

For software licensing, I guess your name does usually form part of the license agreement. Probably then need to mint for every license issued.

---

I guess I’m not there with more NFT types being required for these purposes, it might get confusing. The concepts you describe I believe can be derived from on-chain and metadata.

---

**linvictor88** (2022-01-11):

First, thanks for your reply. we once also struggle with using ERC-1155 or defining a new ERC specially for SFT, we finally choose the later option due to following reason:

semi-fungible token is a new token type which starts at fungible token and ends at non-fungible token. Considering the concert tickets, as you said, yes, we can just assume them all NFTs with unique seat number. However, we can also assume it multiple types of fungible tokens and turns to NFT once delivered to the user. we only considered the later case and the first case can just be covered by ERC721 or ERC1155.

Take an example for the concert tickets, ticket provider have 3 types of tickets for selling: number 1-100 are the VIP tickets, 100-1000 are the level 2 tickets, 1000-10,000 are the level 3 tickets. Tickets provider first mint these 3 types of FTs and don’t want to sell them by themselves. Then two selling sites buy some types of tickets from provider and sell these FTs on SFT trading platform. Once one user ordered one ticket from level3 with number 1000, the selling site would burn one level 3 FT and then mint one NFT with number 1000 to the user.

It is usually said that there is no need to mint these types of tickets, and we can define all these things in our metadata process and directly mint one NFT from ticket provider to user. This actually hide the existence of FT nature of SFT and the user cannot get these types information from ERC721 and ERC1155. We think SFT standard would be one supplement here.

SFT abstracts the semi-fungible token and denote the FT nature to separate roles of token provider and token seller, as well as the NFT nature for end user’s ownership value.

IMO, ERC-1155 is used to manage multiple types of FTs. NFT is a special FT in which the quantity is limited to 1. ERC1155 weakened the ownership value of NFT and owner cannot directly get the ownership info until going through all the transfer events. That’s true that we can design SFT standard based on ERC-1155 and define the FT and NFT by using bits separators in uuid, benefit we get cannot override other disadvantages, also we still need upper logic process to identify such SFT type of token. Then we finally designed the SFT specially for semi-fungible use cases.

---

**julesl23** (2022-01-13):

Hi,

It might be that concert tickets are just not a good use case here.

If the ticket is seated then then it would be an NFT from the start as a particular ticket cannot be swapped for another as they are seat numbered.

if the concert ticket is standing only then that’s a good case for multi token of ERC-1155 where a token id would have a quantity>1.

In both cases ERC-1155 copes well with this.

Presumably you wouldn’t “mint” to user, you mint and then “transfer” to the user.

You can transfer from provider to seller to user, or transfer from provider to user directly. Doesn’t seem relevant case for a new type of NFT for this particular example, unless I am missing something?

I’m not understanding the “ownership info”. Presumably the user owns it because the NFT is in their account?

---

**behzadz1** (2024-05-24):

Defining a standard interface for the transition from fungible to non-fungible tokens is essential. This capability is not directly addressed in existing ERCs, and having a standardized approach would ensure interoperability and ease of integration across different platforms and use cases.

