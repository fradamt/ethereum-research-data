---
source: magicians
topic_id: 26505
title: "EIP-8077: eth/XX - announce transactions with nonce"
author: cskiraly
date: "2025-11-10"
category: EIPs > EIPs networking
tags: [networking, devp2p, mempool]
url: https://ethereum-magicians.org/t/eip-8077-eth-xx-announce-transactions-with-nonce/26505
views: 89
likes: 1
posts_count: 3
---

# EIP-8077: eth/XX - announce transactions with nonce

Discussion for [Add EIP: eth/XX - announce transactions with nonce by cskiraly · Pull Request #10745 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/10745)

This EIP improves mempool propagation, extending the devp2p ‘eth’ protocol’s `NewPooledTransactionHashes` message to also announce each transaction’s source address and nonce together with the already announced hash, type, and size.

By making this change, EL clients will be able to:

- filter by source,
- fill nonce gaps more efficiently,
- avoid some useless transaction fetches.

## Replies

**cskiraly** (2025-12-05):

[@etan-status](/u/etan-status) [@raul](/u/raul) I’ve discussed with both of you the option of including fees besides the source and nonce in the announcement. I’ve now added some text about it in the rationale, but not (yet) in the selected solution. Let’s discuss whether to change the proposed version to one that includes fees as well.

---

**cskiraly** (2026-01-23):

I’m changing the EIP to have the version announcing fees as well discussed more and selected as the main proposed solution. So what’s announced are: txhash, type, size, source, nonce, fees

