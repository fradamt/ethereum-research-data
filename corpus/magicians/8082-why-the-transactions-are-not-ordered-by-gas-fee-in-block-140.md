---
source: magicians
topic_id: 8082
title: Why the transactions are not ordered by gas fee in block 14020984?
author: Richard
date: "2022-01-23"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/why-the-transactions-are-not-ordered-by-gas-fee-in-block-14020984/8082
views: 664
likes: 0
posts_count: 2
---

# Why the transactions are not ordered by gas fee in block 14020984?

please see the block 14020984 from beginning:

[etherscan.io/txs?block=14020984&p=10](http://etherscan.io/txs?block=14020984&p=10)

I write the transaction batch below:

1. the first transaction(I am now sure, I guess) in the block
Txn Hash: 0x6583965a16987b36a0c5b16908717205f32125a31905954bd049e6301ae110fc
method:
contract call of setStatus()
gas fees from the caller: Base: 131.296607397 Gwei |Max: 172.69338682 Gwei |Max Priority: 2 Gwei
Gas Price:
0.000000133296607397 Ether (133.296607397 Gwei) – please note that there is only 133.296607397 Gwei for the first transaction
2. the second transaction in the block:
Txn Hash:0xc4ba57dff7f6402557209b96f625e529bc2746b5ee4f568878751f1a1a71dec6
method: contract call of mint()
gas fees from the caller: Base: 131.296607397 Gwei |Max: 7,000 Gwei |Max Priority: 7,000 Gwei
Gas Price:
0.000007 Ether (7,000 Gwei) – please note that 7000Gwei is much larger than 133.296607397 Gwei of the first transaction, but this transaction is submitted directly to the miners
3. the third transaction in the block:
Txn Hash:0xc4231ace9b74409092b4a774771ae5a62eab3f98e86ae719eec332646d207c5d
method: contract call of mint()
gas fees from the caller: Base: 131.296607397 Gwei |Max: 7,000 Gwei |Max Priority: 7,000 Gwei
Gas Price:
0.000007 Ether (7,000 Gwei) – please note that 7000Gwei is much larger than 133.296607397 Gwei of the first transaction, and also this transaction is submitted directly to the miners(flashbots?)
4. and the next seris of 9 transactions is the same: they were all submitted directly to the miner with Gas Price of 7000Gwei:
Txn Hash: 0xf0c16d2837c87e10880231d32a6cf7a1930fd79fda3272d6bf4d61c79dcafa25
Txn Hash: 0x087d15d2096827f1859f91c0d2036763f25a5ff7f1ce22601bee64342c4875ee
Txn Hash: 0x34c847169867fe1445a7bc99081c022adad2a225c4846de7e488a28697e29188
Txn Hash: 0x8e03da5e0109851ab0fdc4cb6fb6017520b72a79801f4b489412d142b4903628
Txn Hash: 0x497d97d3add26aaace969141f9d01b18e3838ea34c5f90e071372627bc366f6f
Txn Hash: 0x64414f65e67ff77005d235061837e72730f3cc2d39f7fabb666fc7ac02ff94d9
Txn Hash: 0x8c3e1366fbd8d111707cc229ba86d4209ef981691482f96579fc149830fd2b09
Txn Hash: 0xf10c071262c44d95b4ba5231025f4c72c9262e364e734f210808a6b041755e67
Txn Hash: 0x078dac5c362c1c48c0e7b3efbfbc8891c57919c4e15f9bae82b7bdfcc890a4b9
actually, I guess these transactions from the second to the 11th are from the one guy(maybe a bot?)
5. OK, next transaction is like this:
Txn Hash: 0x0b957b5f94befe2575f53214d7a5938862cec7473a394c854c5d2b3f5b716dcf
Gas Fees: Base: 131.296607397 Gwei |Max: 10,001 Gwei |Max Priority: 10,001 Gwei
Gas Price:
0.000010001 Ether (10,001 Gwei)
and the subsequent transactions are also high gas fees…
So, I am confused of:
I know that in ethereum(I read the source code of go-ethereum), the miner order the transactions with gas price, but why the transaction of 0x6583965a16987b36a0c5b16908717205f32125a31905954bd049e6301ae110fc with only gas fee of 131.296607397 Gwei is queued before so many higher gas fee transactions? I am really confused, anyone could help me to explain this? Thank you so much.

## Replies

**cyrus** (2022-01-23):

My understanding is, in Ethereum, transactions are never guaranteed in any order. The miner can choose any set of txs (or none?) and then sort them any way they choose.

