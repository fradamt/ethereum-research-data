---
source: magicians
topic_id: 22559
title: "EIP-7862: Delayed Execution Layer State Root"
author: Nerolation
date: "2025-01-16"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7862-delayed-execution-layer-state-root/22559
views: 187
likes: 4
posts_count: 3
---

# EIP-7862: Delayed Execution Layer State Root

EIP-7862 proposes delaying the ExecutionPayload’s `state_root` by one block. Instead of referencing the post-state of the current block, the `state_root` in block `n` would point to the post-state of block `n-1`.

Find additional context here:


      ![image](https://ethresear.ch/uploads/default/optimized/2X/b/b5d7a1aa2f70490e3de763bef97271864784994f_2_32x32.png)

      [Ethereum Research – 25 Sep 24](https://ethresear.ch/t/proposal-delay-stateroot-reference-to-increase-throughput-and-reduce-latency/20490)



    ![image](https://ethresear.ch/uploads/default/optimized/3X/a/9/a94d0412f9a5ba4edd2674fa0c9e7227711a7d65_2_1024x537.png)



###



Proposal: Delay stateRoot Reference to Increase Throughput and Reduce Latency By: Charlie Noyes, Max Resnick  Introduction Right now, each block header includes a stateRoot that represents the state after executing all transactions within that...



    Reading time: 5 mins 🕑
      Likes: 39 ❤

## Replies

**sbacha** (2025-03-28):

There any work or updates on this? Would like to see if relays can adopt this too

---

**Nerolation** (2025-04-23):

Yeah, currently exploring the design space.

Since yesterday, there’s also a [discord channel](https://discord.com/channels/595666850260713488/1364000536738664470/1364175577216716831) to discuss it further:

