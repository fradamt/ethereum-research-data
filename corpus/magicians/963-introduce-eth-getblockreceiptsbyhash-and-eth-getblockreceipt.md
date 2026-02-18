---
source: magicians
topic_id: 963
title: Introduce eth_getBlockReceiptsByHash and eth_getBlockReceiptsByNumber JSON RPC methods
author: JakubLipinski
date: "2018-08-06"
category: EIPs > EIPs interfaces
tags: [json-rpc]
url: https://ethereum-magicians.org/t/introduce-eth-getblockreceiptsbyhash-and-eth-getblockreceiptsbynumber-json-rpc-methods/963
views: 1082
likes: 1
posts_count: 4
---

# Introduce eth_getBlockReceiptsByHash and eth_getBlockReceiptsByNumber JSON RPC methods

Hi,

I’m looking for some feedback regarding [my first EIP draft](https://github.com/jakublipinski/EIPs/blob/eip-introduce-eth_getblockreceiptsbyhash-and-eth_getblockreceiptsbynumber-methods/EIPS/eip-introduce-eth_getblockreceiptsbyhash-and-eth_getblockreceiptsbynumber-methods.md) before I submit it. This EIP proposes to introduce a new JSON RPC methods called `eth_getBlockReceiptsByHash` and `eth_getBlockReceiptsByNumber` which return all the receipts from a particular block

Cheers,

Jakub

## Replies

**boris** (2018-08-06):

This feels like something [@tjayrush](/u/tjayrush) would have thoughts on.

---

**tjayrush** (2018-08-06):

Already talking to Jakub in the GitHub repo. There’s a related issue against Parity that accomplishes a similar (if not identical) task, here: https://github.com/paritytech/parity-ethereum/pull/9126. They’re questioning whether that should be an EIP as well.

I looked over Jakub’s EIP and it seems reasonable, but I think I prefer the solution suggested in the linked issue as it’s more compact, just as flexible, delivers the same data (unless I’m misunderstanding something), and doesn’t introduce another end point to the RPC.

---

**JakubLipinski** (2018-08-08):

Pull Request: https://github.com/ethereum/EIPs/pull/1300

