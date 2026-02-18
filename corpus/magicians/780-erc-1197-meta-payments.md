---
source: magicians
topic_id: 780
title: ERC-1197 Meta Payments
author: kosecki123
date: "2018-07-18"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/erc-1197-meta-payments/780
views: 736
likes: 0
posts_count: 3
---

# ERC-1197 Meta Payments

This is the draft of the idea of meta payments (generalized payments aka pay-to-code). This is the outcome of the discussion with [@snario](/u/snario) at Off-the-chain workshop.

https://github.com/ethereum/EIPs/issues/1197

Feedback appreciated.

## Replies

**ask** (2018-07-22):

Thanks for getting this discussion started, have thought about this too. One concern I have with the ERC 1077 proposal to implement these kinds of payments is the increasing number of parameters. Solidity has a hard cap on the number of stack variables, and eventually that will limit will be reached by the function’s arity alone. Additionally, many of the parameters end up being 0 which seems like a code smell. A similar issue exists if you have to represent the union of all possible payment args in a struct.

A simple implementation of meta payments could be a bytes format that includes a payment type and a variable number of key/value bytes32 pairs. This could exist alongside a standardized set of keys that represent common payment fields/flags. Although the format is a workaround due to solidity’s lack of protobuf-style dense packing, it seems like a good future-proof way to implement meta payments.

---

**kosecki123** (2018-07-26):

Your are right, although my primary concern was to enable more future-proof payments. So given our protocol (Ethereum Alarm Clock), we are currently using simple ETH payments and in order to enable token payments or NFT payments, we need to upgrade code and re-deploy. Looking into the future, I’m pretty sure that we are yet to witness more asset types to be implemented on Ethereum, essentially forcing protocol updates on our side.

A more specific usage can be found here https://github.com/ethereum/EIPs/issues/1228

