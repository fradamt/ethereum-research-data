---
source: magicians
topic_id: 14639
title: "ERC-7515: NFT Alternative Text in Metadata"
author: mrprotocol
date: "2023-06-10"
category: ERCs
tags: [nft, informational-eips, eips, accessibility]
url: https://ethereum-magicians.org/t/erc-7515-nft-alternative-text-in-metadata/14639
views: 1008
likes: 4
posts_count: 3
---

# ERC-7515: NFT Alternative Text in Metadata

Hi All,

This is a proposal that is very simple. The significance, however, lies in contributing to making the space more inclusive with regards to accessibility.

I am drafting an “**information**” level EIP with regards to alternative text for NFTs.

It would be classified as informational, as per EIP levels, it seems to align most as a strong recommendation or best practice. Additionally, the change is proposed at a metadata level and not a protocol change for ERC 721 or 1155 standards.

Would greatly appreciate feedback, please kindly share your thoughts on the proposal below:

**Background**

Alternative text assists different users who leverage assistive technology. Users who leverage screen readers for instance, benefit from an accurate, concise description of the image.

Given that NFTs are portable between marketplaces, website, and dapps, it is more efficient to create a suitable description upon creation of the NFT. In this way, the description can be attached to the image and ported between interfaces.

**Simple Proposal**

In short, I would like to propose that in the metadata of each NFT, creator(s) should include a field designated as “alt”. “alt” will contain only the accurate description of the image used in the NFT. Any user interface, dapp, or marketplace can then simply display the NFT details from the chain with the “alt” field in the front-end image tag pointing to this metadata field. This field should be placed at the topmost level of the metadata for ease of access.

Responsibility of an accurate or revisable alternative text falls to the creator(s). They may consult with an expert or follow best practices in describing the image. It is not practical to require exchanges to sort and describe thousands of collections.

For generative collections it is possible to accurately describe the base image, and then dynamically set the additional fields in the description as the script is run. For example, “side profile of a girl with {hair_color} hair wearing {shirt_color} etc.

**Why not use “description” in the metadata?**

Description exists as a field in different collections currently. Since it can be more general, “alt” would designate a specific purpose of solely describing the image accurately for others.

**Best Practices**

Following accessibility standards, I have drafted a numbered list of guidelines to be included in the EIP. These guidelines are derived from existing general best practices but have been contextualized to NFT images where applicable. For instance, as mentioned above, it is better to have a clean separation between “description” and “alt” in the metadata as they can convey different information.

**Benefits**

Beyond NFT marketplaces, this simple straightforward EIP can provide a way of aiding in reducing barriers. Alternative text was cited as a continued barrier for individuals according to a recent report by WebAIM: [WebAIM: The WebAIM Million - The 2024 report on the accessibility of the top 1,000,000 home pages](https://webaim.org/projects/million/#alttext) . Alternative text is among the top 5-6 issues that can be easily addressed.

> “Addressing just these few types of issues would significantly improve accessibility across the web” (~WebAIM report linked above).

Going beyond marketplaces, any website or dapp that sourced an image from an NFT minted on-chain would also benefit. Corporate logos minted as NFTs could carry their descriptions between websites in another instance.

**Conclusion**

Although this is a simple EIP, the potential it carries to contribute to a greater accessibility is evident. If each collection creator, developer, and marketplace were willing to spend only a little extra time it could easily contribute to a better experience.

Thank you for your time!

~MR

## Replies

**mrprotocol** (2023-09-13):

PR has been raised!

ERC-7515

https://github.com/ethereum/EIPs/pull/7678

---

**mrprotocol** (2024-01-08):

PR Migration to ERC repo: [Add EIP: NFT Alternative Text in Metadata by DecoratedWings · Pull Request #191 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/191)

