---
source: magicians
topic_id: 9875
title: "IDEA: ChainId issuance and registry / storage on a Mainnet smart contract"
author: juanfranblanco
date: "2022-07-08"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/idea-chainid-issuance-and-registry-storage-on-a-mainnet-smart-contract/9875
views: 933
likes: 3
posts_count: 4
---

# IDEA: ChainId issuance and registry / storage on a Mainnet smart contract

We are seeing many chains created everyday, L2s, other public evm chains, consortiums, testnets, L3s in the future, and eventually this is going to be the cause of chainId collisions, and possible replay attacks.

A solution for this will be to have a registry smart contract that stores the chainIds (in Ethereum mainnet) and allows chains to claim a specific chainId (probably with a deposit to avoid gaming the system), or even claim a range for their private deployments (ie consortiums, testnets, etc).

What are your thoughts?

## Replies

**weijia31415** (2022-07-13):

EIP-3220 by Ethereum Enterprise Alliance (EEA) is drafted to enhance crosschain ids for L1, L2, sidechains. etc. A registration smart contract has be developed to register chainIds.  Please take a look and provide your feedback.

---

**juanfranblanco** (2022-07-15):

[@weijia31415](/u/weijia31415) I do love the idea of having more information of a chain, including extra information of common addresses etc, but there is still an issue on the duplicate of ChainIds (Native ChainIds), so the registry will require to enforce the uniqueness of chainIds to prevent replay attacks (which can happen in any chain).

More comments here [EIP-3220 crosschain id specification - #13 by juanfranblanco](https://ethereum-magicians.org/t/eip-3220-crosschain-id-specification/5446/13)

---

**weijia31415** (2022-07-15):

The EIP-3220 has first 16 bytes assigned as the first 16 bytes of hash for block 0 or the first forked block.  Therefore crosschainId can be an extension or replacement of native chainId and will never have collision issue.

