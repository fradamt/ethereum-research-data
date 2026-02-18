---
source: magicians
topic_id: 9660
title: "EIP-TBD: Contract Fees"
author: greg
date: "2022-06-17"
category: EIPs > EIPs core
tags: [evm, gas]
url: https://ethereum-magicians.org/t/eip-tbd-contract-fees/9660
views: 1026
likes: 7
posts_count: 3
---

# EIP-TBD: Contract Fees

**Note:** I haven’t created an EIP yet, planning to get more feedback before that.

Abstract:

This proposal specifies a mechanism for redistributing a portion of the gas fee’s burned, via eip1559, during a contract interaction to the contract creator.

Full spec can be found [here](https://hackmd.io/@gregthegreek/r11YEwqY9)

There are a few open questions that still remain wrt the actual implementation found under the `specifications` sections.

## Replies

**ralexstokes** (2022-06-17):

my concern with this class of thing is that it just becomes a way to abuse the protocol by a few actors at the expense of all users of it.

for example, I make a contract and construct it to pay you out of the burned fees for interacting with it. I add token mechanics on top which I use to vampire attack a popular DeFi protocol to juice the yield even more.

I use the remainder out of the aggregate flows to bribe proposers to prioritize transactions to this contract ahead of all others. I even give miners a bit more in the form of kickbacks to start raising the gas limit to include this “parasitic” transaction over all others.

Assuming this construction doesn’t collapse, you’d end up with pressure to raise the gas limit meaning fewer people can run full nodes harming network security.

If you follow this line of thinking to its limit, you see why we burn the base fee in the first place – it is the least capturable way to handle what are otherwise valuable flows.

---

**timbeiko** (2022-06-17):

Another way this kind of breaks things is that the equilibrium is for contracts to subsidize whatever part of the transaction fees they get back by offering a rebate of some sort to users. In that case, you haven’t really improved things, but simply made the fee market more opaque. The base fee will just end up higher by whatever % users get as a kickback.

For a fee redistribution mechanism to work, you want to “break the link” between the block proposer and the redistribution (e.g. by smoothing fees over the next N blocks), otherwise there is always a way to simply “recycle” the non-burnt fees as a kickback.

