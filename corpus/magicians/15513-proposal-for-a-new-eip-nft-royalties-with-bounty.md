---
source: magicians
topic_id: 15513
title: "Proposal for a New EIP: NFT Royalties with Bounty"
author: nathanglb
date: "2023-08-21"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/proposal-for-a-new-eip-nft-royalties-with-bounty/15513
views: 644
likes: 2
posts_count: 4
---

# Proposal for a New EIP: NFT Royalties with Bounty

This EIP would propose an extension to the existing EIP-2981 standard.  NFT royalties are on the verge of becoming widely enforceable at scale with the advent of Limit Break’s ERC-721C, Payment Processor marketplace protocol.  Interest in adoption has gained a lot of momentum since OpenSea announced they were permanently adopting a royalty-optional posture for all collections.

The motivation for this EIP is to foster alignment between NFT creators and NFT exchanges.  The premise of the EIP is to standardize a way for creators to offer a bounty paid out of their royalties to the exchanges that facilitate trading of their NFTs.  This is not the same as a marketplace/platform fee.  This is a bounty, paid out of the creator’s/royalty recipient’s own share of royalties.  However, is puts guardrails in place for creators to specify a maximum amount of bounty they are willing to pay on each trade/royalty-bearing transaction.

The proposed extension is similar to EIP-2981, but return additional information:

```auto
function royaltyInfoWithBounty(uint256 _tokenId, uint256 _salePrice) external view returns (address receiver, uint256 royaltyAmount, uint256 maxBountyAmount)
```

An alternative function that could be used to offer bounties to an exclusive partner may look something like this:

```auto
function royaltyInfoWithBounty(uint256 _tokenId, uint256 _salePrice) external view returns (address receiver, uint256 royaltyAmount, uint256 maxBountyAmount, address exclusiveBountyReceiver)
```

Note: Exclusive partnership bounties could be split via payment processors, but for simplicity and reduction in gas cost we do not recommend including an array of partners as it increases complexity/gas cost for a marketplace protocol integration.

We expect that the addition of royalty bounties will lead to interesting incentivization mechanisms where higher bounties are promoted/spotlighted on exchanges more frequently, creating synergistic relationship between creators and exchanges instead of adversarial relationships that exist today.

## Replies

**mitche50** (2023-08-28):

A great way to align creators and marketplaces - seems like a valid extension to the existing EIP.

---

**Mani-T** (2023-08-28):

A good thought to foster collaboration between NFT creators and exchanges, potentially creating a more harmonious ecosystem.

---

**nathanglb** (2023-09-08):

Doesn’t sound like there have been any objections to this - I’ll probably work on a draft of this EIP soon unless I hear a serious objection.

