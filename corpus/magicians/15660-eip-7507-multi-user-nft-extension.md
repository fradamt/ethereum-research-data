---
source: magicians
topic_id: 15660
title: "EIP-7507: Multi-User NFT Extension"
author: minkyn
date: "2023-09-05"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-7507-multi-user-nft-extension/15660
views: 1669
likes: 2
posts_count: 4
---

# EIP-7507: Multi-User NFT Extension

Hi Magicians,

I’d like to introduce a new extension to ERC-721 standards. It proposes a new role `user` in addition to `owner` for a token. A token can have multiple users under separate expiration time. It allows the subscription model where an NFT can be subscribed non-exclusively by different users.

Existing ERC-4907 has a similar feature, but does not allow for more than one user. It is more suitable in the rental scenario where a user gains an exclusive right of use to an NFT before the next user. However for shareable IP assets, we need the subscription model where multiple users can subscribe to an NFT to obtain access.

For details, please see the submitted pull request:

https://github.com/ethereum/EIPs/pull/7634

Looking forward to the feedback from the community!

## Replies

**kevin** (2023-09-06):

It’s an interesting twist, allowing multiple users to interact with a single NFT under different expiration times. Could be a game-changer for things like digital subscriptions.

Anyone else read it? Thoughts?

---

**minkyn** (2023-09-13):

Quoted a comment from the PR:

> You might find this project interesting - it tries to provide similar functionality. It Some major differences is that 1) ability to access a given NFT is done through ownership of a token representing that specific access type 2) existing NFTs can “plug-in”, inheriting functionality is unnecessary 3) revenues generated from selling access to a given NFT can be distributed to multiple accounts based on ownership share of the NFT

The idea from the commenter’s project is to create new ERC-1155 contracts attaching to the original NFT, one such contract representing one type of relation. This allows for the flexibility of extending arbitrary relations on demand, e.g., an NFT can have a user, a renter, a licensee, an auditor, and so forth.

However, its limitation also comes from its flexibility. It requires another config contract to record the mapping among all these access contracts and the original NFT, and it’s not easy or authoritative for the original NFT holder to find that out. In addition, it requires the token ID to be maintained identical among all the contracts, which can be a hassle when synchronization is needed for minted or burned tokens, not to mention the access control issue when things are out of sync.

To summarize, it is an interesting idea and has its place, but for our project and many other developers, we just need a simple way to record the role of user besides owner from our new ERC-721 contract where we have power to add new extra metadata.

---

**xinbenlv** (2023-09-21):

In addition to ERC-4907, have you considered the following ERCs:



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5334)





###



Add a time-limited role with restricted permissions to EIP-721 tokens.












      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5006)





###



Add a user role with restricted permissions to ERC-1155 tokens

