---
source: magicians
topic_id: 116
title: Ethereum Core Devs Meeting 36
author: jpitts
date: "2018-04-06"
category: Protocol Calls & happenings > Announcements
tags: []
url: https://ethereum-magicians.org/t/ethereum-core-devs-meeting-36/116
views: 1372
likes: 2
posts_count: 4
---

# Ethereum Core Devs Meeting 36

**Ethereum Core Devs Meeting 36**

*Friday 04/06/18 at 14:00 UTC*

[Agenda](https://github.com/ethereum/pm/issues/36):

1. Testing
2. EIP 712: Add eth_signTypedData as a standard for machine-verifiable and human-readable typed data signing with Ethereum keys.
3. EIP 665: Add precompiled contract for Ed25519 signature verification.
4. EIP 958: Modify block mining to be ASIC resistant.
5. EIP 960: Cap total ether supply at ~120 million.
6. EIP process updates.
7. Research Updates.
8. Metropolis.
9. Client updates.

[YouTube Live Stream Link](https://www.youtube.com/watch?v=SoPfoNpqG0k)

## Replies

**lrettig** (2018-04-07):

Notes are here: https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2036.md

---

**virgil** (2019-03-22):

Ping on EIP665.  Are there objections to passing this in the next fork?  This change would make a lot of ideas in making Ethereum interact with: DNS, HTTPS,

and email, vastly easier.

---

**boris** (2019-03-22):

Hey [@virgil](/u/virgil) if you or someone you’re working with wants to champion this, I would put list it in the wiki for starters https://en.ethereum.wiki/roadmap/istanbul

I’ve made a PR against EIP233 for Hardfork process that [@axic](/u/axic) wanted updated as well, where process will be making a PR to propose particular EIPs.

Do you want to present it at the CoreDev meeting in Berlin to talk more about it? Remco is proposing a precompile, and I think talking more broadly about precompiles would be helpful.

