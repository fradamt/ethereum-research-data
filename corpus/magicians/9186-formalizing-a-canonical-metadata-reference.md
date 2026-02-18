---
source: magicians
topic_id: 9186
title: Formalizing a canonical metadata reference
author: rebeccajae
date: "2022-05-07"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/formalizing-a-canonical-metadata-reference/9186
views: 615
likes: 0
posts_count: 2
---

# Formalizing a canonical metadata reference

Hi all,

There does not currently exist, as far as I know, a canonical reference for a contract’s ABI/Metadata. There are projects/repositories that try to catalog them (the [ethereum-lists/contracts](https://github.com/ethereum-lists/contracts) repository is one that comes to mind), but it stores metadata on a centralized platform. Providing a canonical reference to IPFS or some other alternative storage platform could resolve this.

In my experiments, I’ve been implementing an `abiURI() public view returns (string memory)` function that provides a URI to this metadata which is configured as part of the constructor, but could be configured by way of another function call.

I’ve been trying to create something around this because I feel that attaching it to the contract itself would be the best place to look.

Let me know if this is something worth working towards or if I missed something in trying to find a solution.

Thank you!

- rebeccajae

## Replies

**abcoathup** (2022-05-11):

Have a look at Sourcify: https://sourcify.dev/

