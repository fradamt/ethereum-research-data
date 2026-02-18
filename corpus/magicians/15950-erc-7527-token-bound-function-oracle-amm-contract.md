---
source: magicians
topic_id: 15950
title: "ERC-7527: Token Bound Function Oracle AMM Contract"
author: lanyinzly
date: "2023-09-30"
category: ERCs
tags: [erc, nft, erc-721, erc-20]
url: https://ethereum-magicians.org/t/erc-7527-token-bound-function-oracle-amm-contract/15950
views: 3379
likes: 5
posts_count: 13
---

# ERC-7527: Token Bound Function Oracle AMM Contract

This proposal defines a system which embeds a Function Oracle that can wrap fungible tokens to non-fungible token and unwrap the non-fungible back to fungible tokens. The preset Function Oracle provides its own Automated Market Maker(AMM) so that it standardize the process of a creating pool for the issuer of vouchers.

Under current framework of pool, it is hard for user to define how to manage the pool without coding. However, we believe it should be more accessible for users to define and create their own pools to energize the market. Through employing FTs as premium for NFTs under a customizable framework, such an approach standardize the process of creating a pool and allows users to gain the ability to “do it yourself.”

We want to propose an infrastructure for decentralized platforms and prompt the development of the decentralized voucher system.

https://github.com/ethereum/ERCs/pull/70

## Replies

**matt_2929** (2023-10-03):

Very good idea, can you expand on it?

---

**kaliwdsn** (2023-10-06):

Where can I view the code? I want to develop the core components of a full-chain game based on this.

---

**lanyinzly** (2023-10-06):

You can click the GitHub link and find the most updated version under “commits.”

The current version is: [Add EIP: Token Bound Function Oracle AMM Contract by lanyinzly · Pull Request #7797 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/7797/commits/1e0f42a4105fe49b83231613b24e98b24e397987#diff-3b593a281c5e8ce316f0e0b2fb8eab8c9cadaa1534ff7904ee3f8a64b1c9c1ed)

Keep clicking the blue “Expand Down” Button at left bottom corner if you cannot see the full script.

---

**lanyinzly** (2023-10-06):

Yes, we will continue post our updates for rationale and more general ideas behind the design. And we will provide some examples on how to implement it and possibilities for future application.

---

**likeaixi** (2023-10-07):

Looking forward to approval！

---

**amandafanny** (2023-10-07):

Very good idea,Looking forward to approval！

---

**Mani-T** (2023-10-08):

This is awesome. By standardizing the process of creating a pool for voucher issuers, this system provides liquidity to credit assets. This liquidity can make credit assets more accessible and tradable in various scenarios.

---

**Peter.G** (2023-10-08):

The EIP7797 is very cool. This will be a disruptive asset issuance protocol. I think there are at least two things that are subversive:

Asset issuance rights are controlled by users, not the so-called project parties

Asset issuance has sufficient liquidity.

The project party only formulates the rules for asset issuance. Both project parties and users need to mint assets according to the rules, and these assets will automatically enter the Pool. Any asset holder can redeem their assets at any time. Not only NFT artists, but also games, social media, and even any influential organization or individual can use this standard to issue assets without worrying about unfair asset issuance and insufficient asset liquidity. Very good, looking forward to further development.

---

**DanceChange** (2023-10-10):

Perhaps, EIP-7797 will become the infrastructure for decentralized credit in the crypto world

---

**xsstc** (2023-10-16):

看了eip7527示例合约代码，我想问下，eip7527是怎样在amm提供流动性的。如果封装和解封装的fee是给流动性提供者，那么应该怎样成为流动性提供者

---

**SamWilsn** (2024-01-12):

These two requirements seem weird together:

> Accounts MUST implement a receive function.
> Accounts MAY perform arbitrary logic to restrict conditions under which Ether can be received.

So it’s perfectly valid for an implementation to reject all ether, but it still has to define a `receive` function?

---

**lanyinzly** (2024-02-07):

If `Factory` is implemented, it does not distinguish what kind of `currency` would be received by the `Agency`. For conciseness, we require `Agency` to implement a receive function.

We can change it to be when `Factory` is implemented and able to accept ETH as `Asset`, `accounts` in `Agency` MUST implement a `receive` function.

> So it’s perfectly valid for an implementation to reject all ether, but it still has to define a receive function?

This case can happen if `Agency` only accepts ERC20.

