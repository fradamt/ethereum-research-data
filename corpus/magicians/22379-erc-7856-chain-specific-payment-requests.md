---
source: magicians
topic_id: 22379
title: "ERC-7856: Chain-Specific Payment Requests"
author: jackchuma
date: "2025-01-01"
category: ERCs
tags: [erc, interop, payments]
url: https://ethereum-magicians.org/t/erc-7856-chain-specific-payment-requests/22379
views: 166
likes: 0
posts_count: 5
---

# ERC-7856: Chain-Specific Payment Requests

This EIP proposes a URI scheme for chain-specific payment requests, enabling users to specify transactions in the form “send me X tokens of type Y on chain Z”. The URI format includes essential components such as the recipient’s blockchain account, the amount of tokens, the token contract address, and optional success and error callback URLs. This standard aims to eliminate ambiguity in multi-chain payment requests, ensuring clarity and accuracy in peer-to-peer transactions and vendor or dApp requests across different blockchain networks.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/823)














####


      `ethereum:master` ← `jackchuma:jack/payment-requests`




          opened 05:43PM - 01 Jan 25 UTC



          [![jackchuma](https://avatars.githubusercontent.com/u/75458431?v=4)
            jackchuma](https://github.com/jackchuma)



          [+105
            -0](https://github.com/ethereum/ERCs/pull/823/files)







This EIP proposes a URI scheme for chain-specific payment requests, enabling use[…](https://github.com/ethereum/ERCs/pull/823)rs to specify transactions in the form "send me X tokens of type Y on chain Z". The URI format includes essential components such as the recipient's blockchain account, the amount of tokens, the token contract address, and optional success and error callback URLs. This standard aims to eliminate ambiguity in multi-chain payment requests, ensuring clarity and accuracy in peer-to-peer transactions and vendor or dApp requests across different blockchain networks.

## Replies

**elkornacio** (2025-01-15):

Cool proposal, good job!

I can see `success-callback-url` and `error-callback-url` params in the ERC you’ve proposed.

Can you please clarify a little bit: how these callbacks should work in detail?

Like:

1. I scan some QR–invoice, my device will identify “cspr://” url scheme
2. It opens my default wallet with deep-link support for this scheme
3. I see UI to send X tokens of Y type to Z address. I confirm the tx
4. [Here callback should be called, I guess. How? By my wallet, exposing my IP address? By some third-party? Which one? I’ll be redirected automatically or I can decline redirection request?]

I see a lot of pitfalls and potential problems directly related to callbacks - both from the security side and from the implementation point of view.

It would be great if you could describe in much more detail how exactly they are supposed to be arranged.

---

**jackchuma** (2025-01-21):

Your concern is totally understandable. I was intending to leave the standard open to allowing a vendor to customize their checkout experience by supplying the wallet with a destination URL for a success or error page. However, this may be unnecessary as it opens up a handful of potential issues like you mentioned. I’d be open to removing that and allowing the host dApp to be in control of post-transaction handling.

Maybe it makes sense to define a response that the wallet should return to the requester to indicate success / failure?

---

**1etsp1ay** (2025-01-23):

how will it support privacy? The IRS, wife and gas toll collector would be keen on knowing X, Y, Z

---

**jackchuma** (2025-01-23):

I’d argue that privacy concerns are out of scope for what this ERC seeks to accomplish. The main goal here is to define a URI scheme so any wallet implementation can receive a request of this manner and understand exactly what the desired outcome is. The formulation & execution of the transaction(s) required to achieve that outcome is up to the wallet and I’d think that’s where privacy considerations come into play

