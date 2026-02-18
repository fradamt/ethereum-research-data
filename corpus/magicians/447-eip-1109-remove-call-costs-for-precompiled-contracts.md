---
source: magicians
topic_id: 447
title: "EIP-1109: Remove call costs for precompiled contracts"
author: jbaylina
date: "2018-05-22"
category: EIPs
tags: [opcodes, gas]
url: https://ethereum-magicians.org/t/eip-1109-remove-call-costs-for-precompiled-contracts/447
views: 7013
likes: 0
posts_count: 14
---

# EIP-1109: Remove call costs for precompiled contracts

This topic is intended be the discussion for EIP-1109.  Any comment or feedback is very much appreciated!


      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-1109)




###

Ethereum Improvement Proposals (EIPs) describe standards for the Ethereum platform, including core protocol specifications, client APIs, and contract standards.

## Replies

**maurelian** (2018-05-23):

(I deleted my previous comment asking for a link, maybe delete your response)

I like this proposal. A few questions:

1. Are there resources that explain how the cost per opcode was set initially? My guess is that much of the cost of CALL is based on the need to retrieve the callee from the disk, but I don’t know.
2. Is it possible that the existing precompile costs have already been reduced by 700?
3. I noticed the test cases don’t mention “precompiled” contracts at all.

---

**jbaylina** (2018-05-23):

1.- Yes, CALL gas cost was increased highly after Shanghai attacks to take in account disk access. For precompiled contracts this makes no sense.

2.- No, it has not been reduced. I tested again now.  If you check this TX: https://ropsten.etherscan.io/vmtrace?txhash=0x3d020fef1b87a4b4b4ff64206c1d1feb4c7e8def9b2d5086fdac3851b30e05d3  in the Line 60 of Geth trace you will see that the cost of the CALL is 872 ( 700 for the CALL, 60 for the SHA256 precompiled contract and 12 becouse there is 1 word as a parameter).

3.- Fixed.

---

**jbaylina** (2018-08-23):

Just Updated the EIP for introducing the new OPCODE PRECOMPILEDCALL.

Please, feedback…

---

**axic** (2018-08-24):

I think it is a bad idea to create a new call opcode.

For a long while I was meant to create an EIP to clarify the range of precompiles, but finally did it: https://github.com/ethereum/EIPs/pull/1352 (Also added a topic here: [EIP-1352: Specify restricted address range for precompiles/system contracts](https://ethereum-magicians.org/t/eip-1352-specify-restricted-address-range-for-precompiles-system-contracts/1151))

I think with having an accepted range specified, this cost reduction EIP would be much simpler to be specified. I would actually propose to only reduce the cost for `STATICCALL` since precompiles should be called with that, given they do not modify the state.

---

**jbaylina** (2018-09-03):

Reducing the cost for all STATICCALL is not a good idea.  There is a vector attack (exploited in Changai attacks) that allows to make multiple calls to multiple contracts forcing the client to search and load the code from the disk of the clients.  That is why this cost was incremented at that time.

According to the core devs meeting, it is more easy to define a new code that to touch the acutual call code of the clients.  That is why I refactor the full EIP and created a new opcode.

---

**axic** (2018-09-04):

Isn’t this issue only about reducing cost for calls targeting precompiles? What is to be loaded from disk in that case?

---

**axic** (2018-09-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> I would actually propose to only reduce the cost for STATICCALL since precompiles should be called with that, given they do not modify the state.

To clarify, this refers to “reduce the cost for STATICCALL when targeting precompiles”.

---

**jbaylina** (2019-06-21):

Static calls do not have to load the state, but they have to load the code. So going in that direction would implicate that the cost of STATICCALL should be higher than 2.

Also note, that this EIP was redesigned in order to not having to touch any thing from the current  CALxxx  code.

---

**axic** (2019-06-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> I would actually propose to only reduce the cost for STATICCALL since precompiles should be called with that, given they do not modify the state.

For reference, this has been proposed as [EIP-2046: Reduced gas cost for static calls made to precompiles - #3 by karalabe](https://ethereum-magicians.org/t/eip-2046-reduced-gas-cost-for-static-calls-made-to-precompiles/3291/3)

---

**axic** (2019-06-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jbaylina/48/261_2.png) jbaylina:

> Static calls do not have to load the state, but they have to load the code. So going in that direction would implicate that the cost of STATICCALL should be higher than 2.

The same requirement applies to `PRECOMPILEDCALL` and `STATICCALL`. Both need to check upfront, before loading any state, if the destination address is on the “list of precompiles”. I do not see any difference in complexity whether that is done in a new opcode or it is done amending an existing one.

However a new opcode seems to be an extra opcode without much benefit over augmenting the existing one. Additionally with a new opcode the cost reduction is only applied to newly deployed contracts. (There is some discussion [here](https://ethereum-magicians.org/t/eip-2045-particle-gas-costs/3311/8) why it may be a bad idea not applying these reductions to existing contracts.)

---

**jbaylina** (2019-06-21):

The number of precompiled smart contracts is going to be always limited. In the other hand the callable contracts from static are much higher.  So you probably will have to load it from disk. Or you can have an attack of just calling many different contracts from the same smart contract.

I saw that in EIP-2046 you already distinguish the 2 different types of calls.

Another reason is that a precompiled smart contract  should not change the context.  It just executes a specific code in the client. So the treatment can be different.

I understand this CALL not as an external call to a different smart contract but an extension of the opcodes in the EVM.  I’m thinking that this opcode should be very low gas.

Also, in the old the core devs call #44, implementers said that they prefer to have a new opcode.

You can check the notes here: https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2044.md

---

**axic** (2019-06-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jbaylina/48/261_2.png) jbaylina:

> The number of precompiled smart contracts is going to be always limited. In the other hand the callable contracts from static are much higher. So you probably will have to load it from disk.

I still don’t understand what difference it makes in which opcode the system checks whether the destination is a precompiled address.

---

**MrChico** (2019-10-18):

STATICCALL should have better performance than CALL in general since no snapshot of state needs to be stored, so it might make sense for STATICCALL to be cheaper in general.

If we knew the breakdown of the cost of a CALL in terms of `cost needed for new bytecode retrieval + cost needed to store current callframe + cost needed for state snapshot` we’d be able to give a motivated answer to the cost of `STATICCALL`, cost of `call-to-self` and call to precompiles.

For some reason geth still does a snapshot https://github.com/ethereum/go-ethereum/issues/20180 for STATICCALL though…

