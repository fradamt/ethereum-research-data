---
source: magicians
topic_id: 27085
title: "EIP-8101: Payload Chunking"
author: Nerolation
date: "2025-12-11"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-8101-payload-chunking/27085
views: 75
likes: 2
posts_count: 2
---

# EIP-8101: Payload Chunking

The EIP:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/10900)














####


      `master` ← `nerolation:payload-chunking`




          opened 02:15PM - 11 Dec 25 UTC



          [![](https://avatars.githubusercontent.com/u/51536394?v=4)
            nerolation](https://github.com/nerolation)



          [+553
            -0](https://github.com/ethereum/EIPs/pull/10900/files)







This PR proposes payload chunking as a feature to streamline block download and […](https://github.com/ethereum/EIPs/pull/10900)execution.












Discussion topic for EIP-7928: [Add EIP: Payload Chunking with Chunk Access Lists by nerolation · Pull Request #10900 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/10900)

#### Update Log

- 2025-12-01: Initial Commit

#### External Reviews

TBD

#### Outstanding Issues

TBD

## Replies

**jochem-brouwer** (2025-12-16):

The current draft PR of the EIP encodes the Chunk Access Lists as RLP. I think for this new EIP we should use/start with SSZ. We can also explore there how we can create minimal packets such that we can verify that the provided CAL is part of the CAL root. With RLPs this data is much larger, because you need all data of the tree branches in order to verify that something is part of that hash (e.g. the RLP proof).

I’m not super deep in SSZ but as far as I understood these unlock smaller proof sizes, and this thus also gives a direct guarantee on the executing client that the CAL is the correct one. This would also lower the attack surface a bit if you can directly verify that the CAL is correct (provided that this does not require one to need all CALs to verify that one received CAL is part of the set).

