---
source: magicians
topic_id: 13856
title: "RFC: ERC721 token metadata update notification"
author: vrypan
date: "2023-04-17"
category: ERCs
tags: [nft, token, erc-721]
url: https://ethereum-magicians.org/t/rfc-erc721-token-metadata-update-notification/13856
views: 592
likes: 2
posts_count: 2
---

# RFC: ERC721 token metadata update notification

More and more NFT tokens use metadata that change over time: traits, name, staking status, artwork.

Some marketplaces allow users to manually refresh metadata, but this is problematic: For example, a potential buyer may not be aware that the metadata of the token they are about to purchase have changed. Also, this is a market-specific solution, which often leads to marketplaces having a different representation of the token metadata depending on when they updated them.

I think that if ERC-721 was put together today, there would have been an even emission to indicate that metadata have changed.

The simplest approach would be something like `event MetadataUpdated(uint tokenId);` and the NFT smart contract could emit this event to notify that the metadata of tokenId has been updated.

I intend to submit an ERC proposal, but I would like to hear some feedback first.

I can see for example, how this could be abused. Should there be some kind of TTL? How are marketplaces (and other apps) treat very frequent MetadataUpdated() event emissions? Should there be a way to signal that **all** token metadata must be refreshed (typical case is artwork reveal, but there are many more similar ones)?

## Replies

**abcoathup** (2023-04-24):

There is already an ERC for this:



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-4906)





###



Add a MetadataUpdate event to EIP-721.

