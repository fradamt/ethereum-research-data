---
source: magicians
topic_id: 941
title: "EIP-1285: Increase Gcallstipend gas in the CALL OPCODE"
author: ben-kaufman
date: "2018-08-03"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-1285-increase-gcallstipend-gas-in-the-call-opcode/941
views: 3251
likes: 0
posts_count: 1
---

# EIP-1285: Increase Gcallstipend gas in the CALL OPCODE

Hey fellows ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=12)

I’ve created [EIP-1285](https://github.com/ethereum/EIPs/pull/1286) which propose to increase the gas stipend given by the `CALL` OPCODE for a call to another contract for non zero value transfers.

This proposal main motivation is to allow decent fallback logic for Proxy contracts. On average, a call to a Proxy costs about 800 to 1,000 gas units for the `DELEGATECALL` and `SLOAD` OPCODES (loading the address of the logic contract and forwarding the call. This is a severe issue when another contract calls the Proxy’s logic contract fallback function. Currently, the EVM gives a stipend of 2,300 gas units to the contract to allow execution of its `fallback` function. This stipend is intentionally low in order to prevent the called contract from spending a lot of gas or attacking the caller contract (for example re-entrancy). This limitation shall allow some basic logic to be executed like using `LOG`. However, when using the proxy pattern, there are only about 1,300 gas units left for the actual logic execution. This is barely enough for a simple `LOG`, and from my own experience, it was enough for one `LOG` with a single, non-indexed parameter (it might allow a bit more in some cases, but still not enough for proper logic).

[EIP-1285](https://github.com/ethereum/EIPs/pull/1286) proposes to increase the given stipend from 2,300 to 3,500 gas units.

You’re welcome to share your thoughts and join that discussion here or on the issue linked below.

https://github.com/ethereum/EIPs/issues/1285

Please find the PR for the EIP here: [EIP 1285: Increase Gcallstipend gas in the CALL OPCODE by ben-kaufman · Pull Request #1286 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/1286)
