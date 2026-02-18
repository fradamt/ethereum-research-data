---
source: magicians
topic_id: 3813
title: Proposing New Function to Select Transactions
author: bitsanity
date: "2019-11-28"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/proposing-new-function-to-select-transactions/3813
views: 525
likes: 0
posts_count: 1
---

# Proposing New Function to Select Transactions

**Feature**

Select all blockchain transactions in block/index order based on a set of criteria. This is similar in concept to filtering events from a smart contract’s log.

**Current Approach**

Fetch each block and the full transaction data. Iterate and apply the filter on the client side. Each such fetch causes an ipc message exchange (node → geth → node) and may send more data than is needed.

**Proposal**

For efficiency, the web3 service providers (geth, parity, infura etc) should implement a server-side transaction query function callable via web3 api.

**Example** (running in node.js with web3 module)

> let txfilter =  { from: addressa, to: addressb };
> let colfilter = [ 'input', 'hash' ];
>
>
> web3.eth.getTransactions( 0, 'latest', txfilter, colfilter )
> .then( (txlist) => {
>
>
> for (let ii = 0; ii  let tx = txlist[ii].hash;
> let hexdata = txlists[ii].input; // .from and .to fields not present
> }
>
>
> } )
