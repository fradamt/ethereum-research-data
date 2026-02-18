---
source: magicians
topic_id: 7924
title: "Idea: Licensing token standard specially for \"licensing\" relationshp"
author: linvictor88
date: "2022-01-07"
category: EIPs
tags: [nft, sft, licensing]
url: https://ethereum-magicians.org/t/idea-licensing-token-standard-specially-for-licensing-relationshp/7924
views: 702
likes: 0
posts_count: 2
---

# Idea: Licensing token standard specially for "licensing" relationshp

Hi All,

It’s appreciated for your comments on our licensing token standard [" Create a new licensing non-fungible token standard"](https://github.com/ethereum/EIPs/pull/4636) request to managing “licensing” relationship.

NFT grants proof-of-owning to any asset owner and bring great potential to Ethereum. While apart from ownerhsip, there are more relationship referring to “licensing” in common life. For example, software company issues licenses for their software use. NFT owner sells licensing tokens for their NFT use permission. DApp provides types of VIPs licenses as incentives to their regular customers. Metaverse GameFi[5] producer creates licensing service contract so that players are able to rent their powerful game equipment.

We think licensing token is more like a semi-fungible token in which it starts out from multiple types of fungible token and finally ends at non-fungible token, so here we first proposes [semi-fungible token standard](https://github.com/ethereum/EIPs/pull/4635). Then we extended SFT to licensing token (LNFT) standard for variety of “licensing” relationship use.

LNFT grants proof-of-licensing to asset owner which is a supplement of  present NFT. Please refer details to the pull request and welcome for your replies and suggestions.

## Replies

**rayzhudev** (2022-04-19):

Hi Victor,

My opinion is that rather than making this a new token standard, we can create an interface such as in EIP-2981. The license can be represented as an ERC-721 belonging to the 0x0…0 address with the interface referencing the license contract. Here are my initial thoughts around what the standard should contain.

```auto
interface IERCLICENSE is IERC165 {
    function licenseInfo(
        uint256 _tokenId
    ) external view returns (
        address license
    );
}
```

