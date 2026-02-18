---
source: magicians
topic_id: 2121
title: EIP-1637 - Adding chainId parameter to eth_sendTransaction
author: pedrouid
date: "2018-12-04"
category: EIPs
tags: [json-rpc, eip-1637]
url: https://ethereum-magicians.org/t/eip-1637-adding-chainid-parameter-to-eth-sendtransaction/2121
views: 1049
likes: 1
posts_count: 2
---

# EIP-1637 - Adding chainId parameter to eth_sendTransaction

Following the discussion from the Wallet ring regarding a new scope of JSON-RPC methods prefixed with `wallet_` to improve Wallet UX, I propose that existing signing methods such as `eth_sendTransaction`, `eth_sendRawTransaction` and `eth_signTransaction` would benefit a lot from a small change that would be backwards-compatible and easily changed by major JS libraries used as middleware between Dapps and Wallets



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/1637)












####



        opened 03:28PM - 04 Dec 18 UTC



          closed 05:10AM - 05 Dec 21 UTC



        [![](https://avatars.githubusercontent.com/u/10136079?v=4)
          pedrouid](https://github.com/pedrouid)





          stale







Currently we rely in non-standard middleware to handle the state of the active c[…]()hain of the Wallet. This state could be standarized in the current `eth_sendTransaction` JSON-RPC method by adding a second parameter to include the chainId.

EIP-155 already takes this into account to protect transactions from being replayed as this chainId is included in the signature `v` value however this is not communicated in a standard way between a Wallet and a Dapp

Dapps today would barely notice this change as the chainId could easily default to the middleware state already handled by libraries like web3.js, ethers.js, ledger.js and etc, but it would allow use to gain instant multi-chain compatibility for Dapps with a (IMO very small) change to the current method.

**BEFORE**
```js
{
  "id":1,
  "jsonrpc": "2.0",
  "method": "eth_sendTransaction",
  "params": [txn]
}
```

**AFTER**
```js
{
  "id":1,
  "jsonrpc": "2.0",
  "method": "eth_sendTransaction",
  "params": [txn, chainId]
}
```

This change would also target `eth_sendRawTransaction` and `eth_signTransaction`

## Replies

**pedrouid** (2019-05-18):

Let’s revisit this EIP cc [@danfinlay](/u/danfinlay)

