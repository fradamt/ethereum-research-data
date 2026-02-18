---
source: magicians
topic_id: 10431
title: EIP-5489 - NFT Hyperlink Extension
author: IronMan_CH
date: "2022-08-18"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-5489-nft-hyperlink-extension/10431
views: 2304
likes: 2
posts_count: 7
---

# EIP-5489 - NFT Hyperlink Extension

[Add EIP-5489 by Ironman_CH · Pull Request #5489 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5489)

NFT Hyperlink extension.

Give an use case, such as in advertisement industry, they can take NFTs as the medium of promotion, and put advertisement as an attachment on NFTs. It has that potential to impact if it grows as a standard.

If anyone else would like to add their thoughts, please reply in the post. Let’s get this moving forward.

## Replies

**SamWilsn** (2022-08-23):

Hey! Since your EIP involves URI/URL and a new scheme, I’d recommend coming out to the [AllWalletDevs](https://discord.gg/nS8geQ5M) discord and joining the URI/URI Working Group discussion.

---

**IronMan_CH** (2022-08-24):

I see, will join that URI/URI Working Group.

---

**IronMan_CH** (2022-08-24):

The invitation is invalid now. I got the following toast.

[![image](https://ethereum-magicians.org/uploads/default/original/2X/c/c471f0c719b88d5e0dac94631a4370b25ffbc98f.png)image476×366 12.6 KB](https://ethereum-magicians.org/uploads/default/c471f0c719b88d5e0dac94631a4370b25ffbc98f)

---

**bfondevila** (2023-03-06):

Thanks [@IronMan_CH](/u/ironman_ch) - this is a great initiative that also allows intraoperability within the same blockchain, allowing 3rd parties to add their own metadata to the NFT.

I have a question however - what’s the rationale behind making authorization a MUST by including it as part of the standard? Since I don’t see the risk of the usual DDoS due to data growing out of control, because the way to access that data is also providing the address of the slot setter.

In the interest of decentralization I see this as an opportunity for web3 projects to immortalize NFTs from dead projects by giving them a second wind, in the form of metadata updates specific to 3rd party players.

This is a revised simplified reference implementation based on that: [simplified-IERC5489/ERC5489.sol at main · bfondevila/simplified-IERC5489 · GitHub](https://github.com/bfondevila/simplified-IERC5489/blob/main/ERC5489.sol)

Such a pity that I saw this EIP so late! But potentially could submit a simplified proposal as another EIP.

---

**IronMan_CH** (2023-03-06):

> I have a question however - what’s the rationale behind making authorization a MUST by including it as part of the standard? Since I don’t see the risk of the usual DDoS due to data growing out of control, because the way to access that data is also providing the address of the slot setter.

Because, there exits ownership problem. It’s the answer for “If the slot’s trade makes profit, who should that profit belongs?”. If we extend this question, there will be a slot DEX on chain for EIP-5489.

---

**bfondevila** (2023-03-06):

I see. It certainly has a need for that specific use case of using an NFT as a billboard, but the foundation of it could still be permissionless (if we talk exclusively about NFT hyperlink extension).

Based on your answer I do see the need for two standards - a permissionless one that allows for fully decentralized NFT hyperlinking, and a permission based one that could be used by external operators such as an exchange.

I’ll join the discord and discuss it further with the team, thanks for your response!

