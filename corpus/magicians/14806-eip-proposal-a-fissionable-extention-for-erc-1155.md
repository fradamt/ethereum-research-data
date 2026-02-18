---
source: magicians
topic_id: 14806
title: "EIP Proposal: A fissionable extention for ERC-1155"
author: CoffeeKing001
date: "2023-06-23"
category: EIPs
tags: [erc, nft, eip, erc1155]
url: https://ethereum-magicians.org/t/eip-proposal-a-fissionable-extention-for-erc-1155/14806
views: 733
likes: 0
posts_count: 4
---

# EIP Proposal: A fissionable extention for ERC-1155

#### Why need ERC-1155F

When I create VIP membership cards NFT with equity attribute, I encounter the need to increase the amount of ERC-1155 tokens.

However, in ERC-1155, each ID corresponds to either a fixed quantity of tokens or allows for token minting.

If a fixed quantity approach is used, it will result in insufficient liquidity when there are many participating users.

If token minting is allowed, the question arises of how to carry out the minting:

1. Issuing tokens directly to the project’s owner would severely harm the interests of early participants and would be too centralized.
2. Airdropping tokens proportionally to early holders, requiring users to manually claim them, would incur significant gas fees and rely on centralized distribution rules.

None of these options are ideal. Therefore, we propose a fissionable ERC-1155 extension that can perfectly solve the liquidity issue while protecting the rights of early participants.

#### What is ERC-1155F

This is the ERC-1155F extention in github: https://github.com/ghking1/ERC-1155F

This is our ERC-1155F NFT collection in opensea: [TalentCard - Collection | OpenSea](https://opensea.io/collection/talentcard)

#### Overview of ERC-1155F

The ERC-1155F interface declared as following, more details can be found in github link above:

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/c/c97bc5c5122d21e31be66fa966a72f7c92bd8123_2_529x499.jpeg)image852×805 110 KB](https://ethereum-magicians.org/uploads/default/c97bc5c5122d21e31be66fa966a72f7c92bd8123)

#### Next step of ERC-1155F

Though it compatible with ERC-1155, but it added some new interface and event too. So may I need propose a new EIP to the ethereum official?

## Replies

**abcoathup** (2023-06-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/coffeeking001/48/9840_2.png) CoffeeKing001:

> Though it compatible with ERC-1155, but it added some new interface and event too. So may I need propose a new EIP to the ethereum official?

I suggest using ERC1155F in a couple of other projects (your own and other people) before thinking if it is worth standardizing.

See: [Comprehensive guide on writing and submitting an EIP | by Anett | The Fellowship of Ethereum Magicians | Medium](https://medium.com/ethereum-magicians/comprehensive-guide-on-writing-and-submitting-an-eip-9474163771f0)

---

**CoffeeKing001** (2023-06-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> I suggest using ERC1155F in a couple of other projects (your own and other people) before thinking if it is worth standardizing.

Thanks for your suggestion ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)

For the moment, we have used it in our “TalenTale” product, who allows KOL issue VIP card and provide knowledge sharing. We use ERC-1155F protocol achieved the fissionable ability. And it works well.

This is our Dapp link: [https://dapp.talentale.io](https://dapp.talentale.io/)

This is our ERC-1155F NFT collection in opensea: https://opensea.io/collection/talentcard

In the future it can be used in many scene like VIP card, business card, virtual art, virtual land, and so on. ERC-1155F can help them solve the liquidity issue while protecting the rights of early participants.

---

**CoffeeKing001** (2023-07-01):

If some one want to use ERC-1155F in your project, please contact me, we can help you freely. [coffeeking001@outlook.com](mailto:coffeeking001@outlook.com)

