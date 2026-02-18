---
source: magicians
topic_id: 17557
title: Updating an already-finalized EIPs/ERCs
author: dror
date: "2023-12-21"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/updating-an-already-finalized-eips-ercs/17557
views: 954
likes: 7
posts_count: 4
---

# Updating an already-finalized EIPs/ERCs

In the current architecture of the EIP repository, once an EIP reaches a “final” status there is no way to modify it, not even if a security consideration is found.

My suggestion: add a mechanism that is available in the IETF’s RFC repository: an “Updated-by” or “Replaced-by”  tag.

This way, a reader of an EIP can clearly see there is further discussion after the current ERC was finalized.

Updated-by should be marked even if the updating EIP is in “draft” (its an “FYI” notice)

Replaced-by should only be marked once the referencing EIP is finalized, and thus the current one becomes completely obsolete.

(both tags are added to existing EIPs once a new document with “Updates” or “Replaces” header tags, respectively, is added to the repository)

## Replies

**ulerdogan** (2023-12-21):

Nice idea! I think this idea can be included in the [EIP-7577](https://ethereum-magicians.org/t/add-eip-versioning-scheme-for-eips/17295), Versioning Scheme for EIPs, which introduces a “Changelog” section for the proposals.

---

**dror** (2023-12-21):

thanks for the reference.

reposted there, as it is indeed a better place for it.

---

**bumblefudge** (2024-01-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dror/48/2438_2.png) dror:

> (both tags are added to existing EIPs once a new document with “Updates” or “Replaces” header tags, respectively, is added to the repository)

Great minds think alike! I opened [this EIPIP issue/RFC](https://github.com/ethcatherders/EIPIP/issues/306) and so far a few of the EIP editors seem to support the idea.  Please drop a plus-one on that thread please if you want this to get did! [@ulerdogan](/u/ulerdogan) you too!

