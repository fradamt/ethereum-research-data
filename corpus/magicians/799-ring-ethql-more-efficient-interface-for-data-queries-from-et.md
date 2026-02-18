---
source: magicians
topic_id: 799
title: "Ring: EthQL - more efficient interface for data queries from ethereum node"
author: Ethernian
date: "2018-07-18"
category: Working Groups
tags: []
url: https://ethereum-magicians.org/t/ring-ethql-more-efficient-interface-for-data-queries-from-ethereum-node/799
views: 900
likes: 1
posts_count: 9
---

# Ring: EthQL - more efficient interface for data queries from ethereum node

Here is some of my observations from various p2p talks:

[@tjayrush](/u/tjayrush) (Thomas Jay Rush from [quickblocks.io](https://quickblocks.io)) has called for better standards for data retrieval from ethereum node, which is a pain (completely agree!).

[@AlexeyAkhunov](/u/alexeyakhunov) (author of the turbogeth client) has mentioned current database layer is not good enough and he is looking for replacement.

[@evgenyponomarev](/u/evgenyponomarev) from [fluence](https://fluence.one) was interested to created an integration between ethereum node and fluence database layer.

looks like you have an interesting topic to discuss, guys!

**Links & Resources**

- Ideas on How to Make an Ethereum Node Easier to Run - by @tjayrush
- EthQL - a project by PegaSys/Consensys

## Replies

**tjayrush** (2018-07-18):

I started collecting together very rudimentary ideas here: [Ideas on How to Make an Ethereum Node Easier to Run](https://github.com/Great-Hill-Corporation/quickBlocks/blob/master/docs/OSBEN/possibleEIPs.md)

---

**tjayrush** (2018-07-18):

One of the things that has become clear to me is that ‘duplicating’ the data (which, to me, is what is implied by the ‘QL’ part of the ring’s name) has consequences related to how easy/hard it will be to keep the data decentralized.

Because my work concerns itself first of all with the size of the duplicated data, I’ve been forced to look for ways to make the node ‘release’ its data in a more usable way.

I think it would be good to clearly separate “retrieval of data” from “storage of retrieved data”. For example, one solution may wish to retrieve every single block/transaction/receipt/log/trace and store all of it in an easily queried database (which would be fast, but quite large). Another may wish to retrieve the same data, calculate certain things, and only store those calculated results (which would be much smaller, but slower on subsequent queries on one needed the raw data).

I think both approaches are valid and will lead to different suggested changes/improvements to the nodes.

The central idea to keep at the front of mind throughout the entire design process, however, should be how to keep the data 100% accessible and cheap if not free.

---

**Ethernian** (2018-07-18):

reworked initial posting to include [EthQL](https://github.com/ConsenSys/ethql).

[@tjayrush](/u/tjayrush), do you miss something in EthQL approach?

---

**tjayrush** (2018-07-19):

My work starts from a 100% decentralized stance. I haven’t compromise at all. This forces me to keep the data on the node and only extract very small pieces to improve the interaction with the node, but not duplicate so much data that I can no longer run on consumer-grade hardware. (My code currently works on a Mac laptop.)

To accomplish this, I had to give up on arbitrary queries across the entire chain, but I’ve convinced myself that this is what a decentralized world is like. That’s why I call what I’m working on an “Account Scraper” as opposed to a “Blockchain Scraper.” Duplicating all of the Ethereum data outside the node will force, I think, a system to move to larger and more expensive hardware which will push strongly toward centralized data. There may be ways to re-decentralize the data through some market mechanism, but I’m exploring what it would look like to never centralize in the first place.

I was trying to note that both approaches are worth exploring and that this group should keep both in mind. A 100% decentralized approach forces me to look to the node software to be better at releasing its data in a usable way. Improving the node would be beneficial to both approaches.

---

**Ethernian** (2018-07-19):

If talking about accounting, do you mean ethers only or tokens as well?

---

**tjayrush** (2018-07-20):

Ether accounting, token accounting, gas accounting. In general, accounting for everything an Ethereum account (regular and contract) does.

---

**Ethernian** (2018-07-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjayrush/48/23_2.png) tjayrush:

> Ether accounting, token accounting, gas accounting.

unclear how to implement `eth_getUniqueAddressesPerBlock` for tokens.

---

**tjayrush** (2018-07-20):

It produces a list of addresses per block. You can use that for whatever purpose you would want, including querying against token contracts for balances. You could even use it to look for token contracts by querying the addresses’s code and poking around for particular patterns.

The general point I’ve been trying to make is that if you want to remain decentralized, you probably don’t want to duplicate the entirety of the data (and in fact, grow it significantly by adding traces to a database).

Instead, I’ve been focused on trying to figure out ways to make the node more “giving” and more “nimble”. If we form a ring, I think at least three sub-subjects would be appropriate: gathering the data, delivering the data, improving the node.

