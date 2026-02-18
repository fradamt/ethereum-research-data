---
source: magicians
topic_id: 6101
title: JSON-RPC Changes for Type 0x2 EIP-1559 transactions
author: ryanschneider
date: "2021-04-26"
category: EIPs > EIPs interfaces
tags: [json-rpc, eip-1559, eip-1474]
url: https://ethereum-magicians.org/t/json-rpc-changes-for-type-0x2-eip-1559-transactions/6101
views: 3542
likes: 4
posts_count: 9
---

# JSON-RPC Changes for Type 0x2 EIP-1559 transactions

The goal of this thread is to come to a rough consensus on the JSONRPC changes required to support EIP-1559 type 0x2 transactions.  I’ve placed it here in Primordial Soup vs in the EIP section since as [@matt](/u/matt) has pointed out over on Discord the JSONRPC spec is moving out to https://github.com/ethereum/eth1.0-specs.

Anyways, before we get to deep into naming things (the hardest part of Computer Science ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=10) ) I think we need to agree on what JSONRPC changes are needed for type 0x2 transactions.

To recap, there are a couple places where transaction objects are serialized as JSONRPC results:

- In response to the eth_getTransactionByHash RPC
- In response to the various block-returning RPCs like eth_getBlockByNumber where the second argument to return full tx bodies is true.
- As part of the txpool_content RPC response.

At least in geth, all of these locations use the same tx marshalling code, I suspect most clients are probably similar (though I’m not sure if txpool_content is supported in all clients).

For the first two cases, I think it’s generally a good thing that a JSONRPC consumer is able to “recreate” the transaction hash from the returned JSONRPC result.  As such, I think all the new consensus-level fields in EIP-1559 should be available in the JSONRPC.

To recap, the consensus fields in 1559 txs are:

- The EIP-2718 type (always 0x2)
- The twelve fields in the RLP-encoded tx body chainId, nonce, maxPriorityFeePerGas, maxFeePerGas, gasLimit, to, value, data, access_list, signatureYParity, signatureR, signatureS
 Clients have already standardized on including type, chainId, and accessList for EIP-2718/-2930 txs in Berlin, so I think including these fields for 1559 txs is pretty non-controversial.  Likewise clients have continued to return the r, s, and v fields.

That leaves the following new consensus-level fields:

- maxPriorityFeePerGas
- maxFeePerGas

And importantly, the following existing fields no longer have obvious corresponding consenus-level 1-to1s:

- gasPrice

Digging into the details of EIP-1559, there are a couple new “intermediate” levels which, while not required for consensus per se, could be considered useful to JSONRPC tx consumers taken from the implementation pseudo-code.

```auto
# priority fee is capped because the base fee is filled first
priority_fee_per_gas = min(transaction.max_priority_fee_per_gas, transaction.max_fee_per_gas - block.base_fee_per_gas)
# signer pays both the priority fee and the base fee
effective_gas_price = priority_fee_per_gas + block.base_fee_per_gas
```

The intermediate values are

- priority_fee_per_gas
- effective_gas_price
- block.base_fee_per_gas

So, to summarize, there are 5 potentially new fields to include, and 1 field that is no longer relevant.

I’ll add my proposed changes in a reply to this initial message, to try to keep the top-level post in this thread as “objective” as possible.

## Replies

**ryanschneider** (2021-04-26):

With respect to the new fields, I propose the following changes (with rationale):

- We include the two consensus-level fields, with JSONRPC names to be determined.

The two consensus level fields are required to either (re-)compute the transactions hash or to convert the tx into RLP (for example to rebroadcast a tx via eth_sendRawTransaction).
- Let’s finalize the names after we agree that these fields should be included.

We include the `effective_gas_price` value *in place of* the previous `gasPrice` value.

- Many downstream JSONRPC result parsers may assume that the gasPrice field will always be present on a transaction.
- Un-updated consumers can still roughly interpret gasPrice as it’s original meaning.

Note, however, that unmined transactions still in a clients txpool can be returned via JSONRPC.  In this case, we have two options for “effective gas price”:

- don’t return it at all
- return an “estimated” effective gas price based on the current pending block’s baseFee.

My initial reaction is to not return it at all, but this does “break” un-updated consumers that expect the `gasPrice` field to exist, so I reluctantly lean towards re-calculating the effective gas price of unmined txs as the “pending” block baseFee is updated.

---

**MicahZoltu** (2021-04-27):

We could return the max gas price prior to mining.  This is similar to `gasLimit` vs `gasUsed`, where you have a cap prior to execution and once execution is completed you know the actual.

---

**MicahZoltu** (2021-04-27):

I think `effective_gas_price` should be included in the transaction receipt JSON-RPC endpoint.  It isn’t technically part of the consensus receipt, but we already return a number of non-receipt fields in the `eth_getTransactionReceipt` endpoint and I think this is a useful one to add to that set.

`priority_fee_per_gas` *may* also be useful in receipts as people will need to look at it historically to see what priority fee miners are demanding for inclusion, which will be very valuable for informing the priority fee set in future transactions.

---

**alita-moore** (2021-04-30):

What would be the most impactful ETH1 JSON RPC spec for me to write now? I can prioritize this and get rough drafts out asap. From this conversation I see the following as priorities:

`eth_getTransactionReceipt`

`eth_sendRawTransaction`

`eth_getTransactionByHash`

Are there any others that would be relevant here?

---

**yuga.cb** (2021-04-30):

Hi! One question for folks.

When a sender constructs a transaction, they will fill out the maxPriorityFeePerGas and maxFeePerGas fields. The actual gas fee the sender pays, however, may be lower than maxFeePerGas. For the APIs returning transaction information (e.g. getTransactionByHash), which field will contain the amount of gas the sender actually paid? Will it be effective_gas_price?

I understand we can get the base fee from the block APIs, so we can calculate the actual priority fee paid if we have the total price paid.

Thank you!

---

**yuga.cb** (2021-04-30):

I think those would be great to start with! getTransactionByHash is the most important IMO and would be great to have ASAP.

---

**ryanschneider** (2021-04-30):

[@alita-moore](/u/alita-moore) ya I think `eth_getTransactionByHash` and `eth_getTransactionReceipt` are the two most important.  `eth_sendRawTransaction` actually shouldn’t require any interface-level changes, implementers just need to handle the `0x2` tx type much like they did for `0x1` txs in Berlin/EIP-2930.

Also thinking about `eth_gasPrice`, when ordering the txs and deciding a percentile, should the 1559 txs be ordered by effective gas price?  Do we need an alternate RPC that returns more granular info about the base fee/inclusion fee breakdown?

I’m sure there are other RPCs we will think of that will require some changes as the clients start implementing these changes now that the bulk of the consensus work is (mostly) done for 1559.

---

**tvanepps** (2021-05-04):

Wanted to invite folks from this thread to the first London Readiness call, [announced here](https://twitter.com/trent_vanepps/status/1388153403432480769?s=20)! We’ll be using this to coordinate ecosystem dev tooling and infra ahead of the upcoming London Upgrade.

**Friday, May 7, 14:00 UTC**

[@MicahZoltu](/u/micahzoltu) [@yuga.cb](/u/yuga.cb) [@ryanschneider](/u/ryanschneider) [@alita-moore](/u/alita-moore) DM me via the ETH R&D Discord if you’d like to be added to the calendar event.

Read agenda [here](https://github.com/ethereum/pm/issues/308), add your discussion topics: one of the main ones will be **JSON RPC support for 1559**. Please join if you would like to have input on this.

Looking forward to you joining us on Friday.

