---
source: magicians
topic_id: 18744
title: ERC-7628：ERC-721 Ownership Shares Extension
author: bizliaoyuan
date: "2024-02-17"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7628-erc-721-ownership-shares-extension/18744
views: 1458
likes: 7
posts_count: 7
---

# ERC-7628：ERC-721 Ownership Shares Extension

[github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/266)














####


      `master` ← `chenly:erc-7626`




          opened 02:37PM - 17 Feb 24 UTC



          [![](https://avatars.githubusercontent.com/u/13716?v=4)
            chenly](https://github.com/chenly)



          [+195
            -0](https://github.com/ethereum/ERCs/pull/266/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/ERCs/pull/266)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.












## Abstract

This extension defines an interface that adds balance functionalities to ERC-721 tokens, enabling functions and events for balance querying, transfer, and approval akin to ERC-20 tokens.

## Motivation

Some NFTs require defining shares of a corresponding right for each token, such as ownership stakes in a company. Each token holder can be considered a shareholder of this right and they wish to be able to conveniently query and trade these shares. However, the current ERC-721 standard lacks built-in support for token balances, leading to difficulties and limitations in managing and trading these rights. By introducing balance functionalities akin to ERC-20, we can provide a universal solution for ERC-721 tokens, enabling holders to easily query and trade their corresponding shares of rights, thereby fostering broader adoption and circulation of NFTs.

## Replies

**Mani-T** (2024-02-19):

Impressive. Implementing access control through smart contracts on the blockchain ensures decentralized and tamper-resistant authorization, reducing reliance on centralized entities and mitigating single points of failure.

---

**Swader** (2024-03-02):

Why is this needed when 1155, 6551, and 7590 already exist? What problem does it solve that those do not?

---

**bizliaoyuan** (2024-03-06):

I have renamed the proposal to ‘ERC-721 Ownership Shares Extension’, which better aligns with the motivation.

The proposal aims to find a middle ground between ERC-721 and ERC-1155. While ERC-1155 can represent the share of an asset held by a particular address, tokens lack uniqueness. On the other hand, ERC-721 provides uniqueness for each token, but they lack attributes to represent the share of an asset.

Both 6551 and 7590 are mapped to other token assets. I think it would be more straightforward to simply add an additional attribute.

---

**SamWilsn** (2025-02-04):

Couple of non-editorial points I want to address before moving this into last call. First, [@Swader](/u/swader) 's comment needs some more discussion. Why introduce an entire new standard when you can encode the exact same information in ERC-1155 and have better wallet support?

You say ERC-1155 tokens lack uniqueness, but you can represent an NFT as a token-id with a total supply of one, and its shares as a separate token-id with multiple shares.

ERC-7628 is less general purpose than ERC-1155 and requires even more work in wallets to properly support. Instead of building a new token system from scratch, I’d recommend a much simpler extension to ERC-1155:

```solidity
interface ERC1155OwnershipShares /* is ERC1155 */ {
    function sharesOf(uint256 tokenId) public view returns (uint256 nftTokenId);
}
```

Given a fungible token id, `sharesOf` would return the token id of the NFT that is fractionally owned.

---

The other question I’d like to ask is why `totalShares` returns the total number of shares across all NFTs? That doesn’t seem like a particularly useful number. Wouldn’t it make more sense to return the total number of shares for a particular NFT?

---

**SamWilsn** (2025-02-04):

https://github.com/ethereum/ERCs/pull/793 seems vaguely similar to this proposal. Might be a potential area for collaboration?

---

**parseb** (2025-02-19):

The id space of *ERC-3525: Semi-Fungible Token* can be used to achieve that behavior.

Good idea, best today as an OZ/solmate extension.

