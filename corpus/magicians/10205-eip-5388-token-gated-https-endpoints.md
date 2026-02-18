---
source: magicians
topic_id: 10205
title: "EIP-5388: Token-Gated HTTPS Endpoints"
author: TimDaub
date: "2022-08-01"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-5388-token-gated-https-endpoints/10205
views: 686
likes: 0
posts_count: 2
---

# EIP-5388: Token-Gated HTTPS Endpoints

Launch tweet:



      [twitter.com](https://twitter.com/timdaub/status/1554116824006103040)





####

[@](https://twitter.com/timdaub/status/1554116824006103040)

  🐣 Another day, another EIP submission! 🆕

"EIP-5388: Token-Gated HTTPS Endpoints" implements a paywall that can be overcome by invoking a Solidity function at a contract address. @oceanprotocol V3 was an inspiration.

Feedback is welcome! DRAFT PR: https://t.co/zcfohM7q6N

  https://twitter.com/timdaub/status/1554116824006103040










- Description: Composable RESTful and Solidity interface to implement token-gated HTTPS endpoints using data tokens.
- Draft PR: Initial draft for EIP-5388 by TimDaub · Pull Request #5388 · ethereum/EIPs · GitHub

## Replies

**Pandapip1** (2022-08-01):

> The resulting hexadecimal-encoded signature must be included in a user’s request to the endpoint as the Bearer value of the Authorization header. An example:

I personally would recommend defining a new scheme for this. How about `Paid 0xabc`, `Signed 0xabc`, or `Paid5388 0xabc`?

