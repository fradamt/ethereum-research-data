---
source: magicians
topic_id: 5095
title: Out-of-order, asynchronous, eager evaluation of unambiguous state-operating EVM machine codes
author: u4ea
date: "2021-01-04"
category: Magicians > Primordial Soup
tags: [evm, opcodes, ooe]
url: https://ethereum-magicians.org/t/out-of-order-asynchronous-eager-evaluation-of-unambiguous-state-operating-evm-machine-codes/5095
views: 592
likes: 0
posts_count: 2
---

# Out-of-order, asynchronous, eager evaluation of unambiguous state-operating EVM machine codes

Hello! I am new here and to Ethereum development (though I am a professional software engineer). This is my first time posting here.

I’ve been wading in these waters since about the 10,000,000th block and I’ve had a burgeoning interest in finding ways to contribute materially to Ethereum’s growth and success. I was pointed here by someone else, and will warn you that my suggestion(s) may seem outlandish as I lack granular expertise over existing EVM implementations. *It’s possible this or something like it is already in the soup!*

With that out of the way, here’s an EVM improvement I’d like to propose and discuss:

> During EVM code execution “look ahead” as many opcodes as possible, until the next opcode is ambiguous such as a dynamic or conditional jump. Pay strict attention to state-operators such as SSTORE and SLOAD. As soon as the arguments to these codes are unambiguous, eagerly execute the codes in asynchronous out-of-order fashion. No apparent functional differences should be visible externally. The time-value of compute resources used should be approximately upper-bounded by those consumed using a serial approach.

**Some immediate notes:**

- As far as I know, there are no EVM implementations (neither old, nor current, nor in the works), which feature this type of optimization. I can’t imagine I’m the first to conceive of this… has this type of work already been looked at and panned for one reason or another? (not worth it, too niche, etc?)
- Outside of the challenge of achieving a “correct” implementation, there are some externality concerns here which may introduce subtle implementation complexities. Notably: ensuring that the time-value of compute resources consumed by this new implementation is strictly less than or equal to the previous implementation given a perfect attacker. This is meant to be an optimization: throwing money at a solution is not an optimization (a.k.a let’s not hazard spawning 3,000 threads).
- It seems obvious that this would, at least initially and perhaps forever, be locked behind a default-off flag. Node operators whose workloads are suitable for the optimization can then opt into it.
- Even with the flag, there shouldn’t be any circumstances in which a corner-case scenarios (malicious or not) may block up a node for unreasonable amounts of time.

**Real-world use-cases:**

- I imagined this as a step toward a much larger and more soup-y intrigue of mine: accelerating latency-insensitive, read-only, massively concurrent JSON-RPC workloads using the the many cores of a GPU. If the goal is raw machine-code throughput, the GPU is the undoubtedly place to do it. However, the hard-drive is “relatively on another planet” from the GPU. Therefore, state operations must also be made as concurrent as possible to start reaping the benefits of GPU acceleration. Much “hot state” can be simply kept in VRAM to help smooth things out, but the reality remains.
- The specific use-case that prompted this is the following function (for those looking to deep-drive) in the contract at 0x6cb2291A3c3794fcA0F5b6E34a8E6eA7933CA667:



      [gist.github.com](https://gist.github.com/elliottdehn/d6a0f485935c2d15503c3cb115efee47#file-0x6cb2291a3c3794fca0f5b6e34a8e6ea7933ca667-sol-L2382)





####



##### 0x6cb2291A3c3794fcA0F5b6E34a8E6eA7933CA667.sol



```
/**
 *Submitted for verification at Etherscan.io on 2020-08-10
*/

// File: @openzeppelin/contracts/token/ERC20/IERC20.sol

pragma solidity ^0.5.0;

/**
 * @dev Interface of the ERC20 standard as defined in the EIP. Does not include
```

   This file has been truncated. [show original](https://gist.github.com/elliottdehn/d6a0f485935c2d15503c3cb115efee47#file-0x6cb2291a3c3794fca0f5b6e34a8e6ea7933ca667-sol-L2382)










This is a loop over 34 exchange output estimators, used by a DEX aggregator for the purpose of finding an optimal swapping arrangement. In my analysis, there is no reason this loop (or a more static version of it) must be executed fully serially. The loop has a static size… the state reads involved are also static. On my NVMe drive this loop takes about 5-6ms to execute, a throughput of 200 req/s.

If one is offering a service based on off-chain work by this function (which indeed, the One Inch Exchange seems to do), this throughput can be crippling. It would demand a significant amount of expensive CPU resources either through a cloud provider or on-premises hardware. The most advanced consumer hardware I could find for this workload is the *AMD Ryzen Threadripper 3990X 64-Core* processor coming in at a whopping $5,000. This processor would give you ~2700 req/s running all 64 cores at 3.8ghz, which seems to be roughly its thermal limit.

- This state-operating bottleneck is prohibitively significant for those seeking to do data science, forensic analysis, institutional reporting, and so forth. While this may sound rather niche, it represents a barrier to adoption. How can we expect the world’s financial system to enter a compute environment in which any meaningful and timely analysis demands thousands of dollars worth of hardware and resources?
- There is an emerging technology trend regarding GPU-accelerated databases in general; clearly there is an appetite for reduced overhead when it comes to munging huge lakes of data.

**Conclusions:**

First: thanks for reading this, I know I’m still a novice and ill-informed on many things which I’m sure turn what I’m suggesting into Swiss cheese. I’d like to see this idea live or get analytically panned, rather than sit in the purgatory of brains and speculation.

While on-chain optimizations (i.e shards) are important for *scalability*, off-chain optimizations are important for *adoption*. Together, they’re greater than the sum of their parts. This is my motivating thesis.

Much of the work done by institutions (and researchers and developers) is out-of-band from their various executive functions. Case in point: DEX aggregators providing off-chain estimates to their users, and supplying historical pairing charts (so many pairs, so many blocks!). This feature should cost $tens, not $tens-of-thousands.

We can’t with a straight face argue that the world’s *financial system*, a system notoriously sensitive to new technology and jam-packed with out-of-band work, will acquiesce to the limitations imposed by data warehoused in the blockchain. It’d be reasonable (prudent even) for those in technical positions of authority to pan the Ethereum platform for many useful purposes, based on this alone. Solidity could perhaps be viewed as the most powerful database query language in existence, but it’s not *useful* in that regard - right now, it’s an hindrance verging on uselessness relative to things like SQL.

Solidity will never achieve the relative efficiency of SQL (please prove me wrong), but that doesn’t mean we can’t squeeze as much blood out of Solidity’s rock as possible.

What if Solidity *was* in-fact a powerful and efficient tool for interesting, important, and valuable chain database work? Thank you!

## Replies

**qizhou** (2021-01-08):

Looks like this will result in a complicated implementation.  Assuming most of the cost is in SLOAD/SSTORE, a simpler way could preload these data in memory via [optional access list](https://eips.ethereum.org/EIPS/eip-2930) in parallel with the normal transaction execution.

