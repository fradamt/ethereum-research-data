---
source: magicians
topic_id: 9362
title: Name-bound tokens
author: TimDaub
date: "2022-05-24"
category: Magicians > Primordial Soup
tags: [token, ntt]
url: https://ethereum-magicians.org/t/name-bound-tokens/9362
views: 899
likes: 3
posts_count: 2
---

# Name-bound tokens

Keywords: Non-Tradable, non-separable, Non-transferrable, non-fungible tokens, NFTs, Soulbound tokens, SBTs, badges, ENS-bound tokens, Name-bound tokens

- EIP-XXXX DRAFT: Add initial draft for Name-bound tokens by TimDaub · Pull Request #5107 · ethereum/EIPs · GitHub

Feedback, discussions, and comments are welcome.

## Replies

**tomcohen.eth** (2022-05-24):

Just to kick off the discussion here - there are two paths forward here I’d be interested in getting input on:

1. The ERC as it stands, with binding to ENS nodes specifically.
2. A broader ERC for binding ALL ERC721 token, with an interface similar to what @MicahZoltu suggest in the ERC4973 discussion - returning (address erc721Contract, uint256 erc721TokenId)

Tim’s position is that binding to ERC721 is too broadly general with unclear advantages, whereas binding to ENS has a clear motivation behind it. Basically a standard should have the clearest possible purpose and the tightest definition that serves that need. [@TimDaub](/u/timdaub) am I characterising your position here accurately?

Personally, I don’t see the harm in providing a general standard as long as it satisfies the ENS subset to the same degree. My current position is that standards should allow for the broadest possible room for use that can still provide the same guarantees as a tighter standard. Relatively strong position, but will try to have it loosely held. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

