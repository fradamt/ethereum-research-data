---
source: magicians
topic_id: 10977
title: "Discussion EIP-3668: Use of CCIP read for transactions (CCIP write)"
author: dev
date: "2022-09-22"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/discussion-eip-3668-use-of-ccip-read-for-transactions-ccip-write/10977
views: 756
likes: 0
posts_count: 1
---

# Discussion EIP-3668: Use of CCIP read for transactions (CCIP write)

Earlier this year [ethers.js](https://github.com/ethers-io/ethers.js/issues/2478) added support for EIP-3668. A few [other clients](https://github.com/ensdomains/pm/issues?q=is%3Aissue+is%3Aclosed) followed.

It appears to be the case that most clients decided to only support `eth_call` even though EIP-3368 mentions the “use of CCIP read for transactions”:

> While the specification above is for read-only contract calls (eg, eth_call ), it is simple to use this method for sending transactions (eg, eth_sendTransaction or eth_sendRawTransaction ) that require offchain data. While ‘preflighting’ a transaction using eth_estimateGas or eth_call , a client that receives an OffchainLookup revert can follow the procedure described above in Client lookup protocol, substituting a transaction for the call in the last step. This functionality is ideal for applications such as making onchain claims supported by offchain proof data.

We think using EIP-3668 for “write” transactions is powerful, especially when combined with EIP-712 for offchain signing of payloads returned by the `Gateway`.

What could be done to emphasize the support for `eth_sendTransaction`? Would it be helpful to create a new “EIP - CCIP Write” or is the existing EIP good enough?
