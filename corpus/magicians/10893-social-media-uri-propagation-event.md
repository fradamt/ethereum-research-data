---
source: magicians
topic_id: 10893
title: Social Media URI Propagation Event
author: TimDaub
date: "2022-09-15"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/social-media-uri-propagation-event/10893
views: 579
likes: 0
posts_count: 4
---

# Social Media URI Propagation Event

- PR: Add: Social Media URI Propagation Event by TimDaub · Pull Request #5659 · ethereum/EIPs · GitHub
- Heavily inspired by EIP-3722 of @auryn-macmillan

## Replies

**TimDaub** (2022-09-15):

A nice use case of preferring URIs over raw text content is where e.g., CAIP-19-style URIs for NFTs could be used to curate NFTs. E.g. someone could also release their latest music NFT tracks in a release club or post the latest crypto kitty using CAIP-19: `eip155:1/erc721:0x06012c8cf97BEaD5deAe237070F9587f8E7A266d/771769`

reference: [CAIPs/caip-19.md at master · ChainAgnostic/CAIPs · GitHub](https://github.com/ChainAgnostic/CAIPs/blob/master/CAIPs/caip-19.md)

---

**auryn** (2022-09-30):

Is there a reason contracts wouldn’t just call poster rather than implementing this function?

---

**TimDaub** (2022-09-30):

With regards to EIP-3722, I think I’m mostly confused about using JSON and its format in `string content`. So my idea was to distill it and give any implementer the chance to build their own emission contract business logic instead of having a single repository. Instead of posting content directly, rather I’d prefer if users posted a URI or even better a content ID from a network like IPFS.

