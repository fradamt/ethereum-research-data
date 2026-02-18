---
source: magicians
topic_id: 4478
title: "EIP: Vendor-specific opcodes"
author: qizhou
date: "2020-08-03"
category: EIPs
tags: [opcodes]
url: https://ethereum-magicians.org/t/eip-vendor-specific-opcodes/4478
views: 803
likes: 0
posts_count: 7
---

# EIP: Vendor-specific opcodes

Besides Ethereum, EVM has been widely used by multiple blockchain projects to support smart contracts (including EEA).  Different vendors may want to add new features where standard EVM does not have.  However, adding such features with compatibility with the standard EVM can be complicated - it is not recommended to use a new opcode as the opcode may be used by the standard EVM in the future. Instead, it generally requires to implement a precompile contracts, which needs careful gas calculation and can be error-prone.

The EIP aims to ease the work of adding non-standard EVM features (i.e., extensions in x86).  The EIP uses two opcodes OP_VENDOR and OP_VCALL:

- OP_VENDOR returns a uint256 indicating who is the vendor of the EVM.  The vendor list can be registered similar to coin_type in HD wallets.
- OP_VCALL calls a vendor-specific extension (similar to CPU instruction extensions such as SSE, AVX).  Which extension of the vendor and the arguments can be specified in the stack or data appended after OP_VCALL.

Note that this can be also used to tell which version of Ethereum the EVM is running on (such as Peterburg, Byzantine).

## Replies

**matt** (2020-08-04):

Are the gas calculations required to vet a precompile really more arduous than doing so for an opcode?

---

**qizhou** (2020-08-04):

Besides gas calculation and more complicated to implement, the gas cost of pre-compile contract can be also much higher than opcodes.  Taking the evolution of EVM as an example, the bitwise shifting instructions in EIP145 takes 3 gas, while implementing it using pre-compiled contract, the gas cost of STATICCALL takes 30 gas or more for CALL.

---

**matt** (2020-08-05):

I guess I’ll state my skepticism more clearly: I don’t agree that calculating the cost of an op code is any easier than a precompile. The effort should be roughly equivalent.

The biggest downside to the precompile is the additional cost. But I don’t think this is a good reason to introduce an EVM feature targeted for private chains on mainnet. A stronger argument for this sort of mechanism would be that it could help alleviate the inevitable exhaustion of op codes, since there are only 255.

---

**qizhou** (2020-08-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> But I don’t think this is a good reason to introduce an EVM feature targeted for private chains on mainnet.

Note that the EVM feature can be used not only in private chains but also consortium/permissioned chains (e.g., Enterprise Ethereum) or other public chains, who want to maintain compatibility with standard EVM while harvesting the benefits of new opcodes that are customized.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> A stronger argument for this sort of mechanism would be that it could help alleviate the inevitable exhaustion of op codes, since there are only 255.

Yes, by using like OP_VCALL, we could add another 255 opcodes.  In addition, OP_VENDOR can be combined together with OP_VCALL.

---

**matt** (2020-08-06):

Why not calculate the gas cost of a new addition, subtract 30 gas (for the `STATICCALL`), and ship it as a precompile? This will work for all new behaviors which cost more than 30 gas.

---

**qizhou** (2020-10-14):

This is another solution.  But I personally dislike the idea of having special gas calculation for precompiles - it may easily cause other corner cases that we never thought about.  Further, for some simple operations, such as how many bits in an integer, or the position of top 1 bit in an integer, implementing in precompiles is pretty tedious.

