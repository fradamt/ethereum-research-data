---
source: magicians
topic_id: 18508
title: "RollCall Breakout #3: Precompiles and the RIP Process"
author: adietrichs
date: "2024-02-06"
category: Protocol Calls & happenings
tags: [rollcall]
url: https://ethereum-magicians.org/t/rollcall-breakout-3-precompiles-and-the-rip-process/18508
views: 1080
likes: 5
posts_count: 4
---

# RollCall Breakout #3: Precompiles and the RIP Process

As announced on [RollCall #2](https://github.com/ethereum/pm/issues/925), we are organizing a series of breakout calls each Wednesday. The third breakout call will be on RIP precompiles, using RIP-7212 as a concrete example. The intention is for these breakout calls to be optional additions to the monthly RollCalls, and aimed at bringing together the subset of teams interested in each particular topic.

## Meeting Info

- Wed Feb 07, 2024, 14:00-15:30 UTC
- Zoom link shared in the rollcall channel in the EthR&D Discord, which is bridged to the RollCall telegram channel, shortly before the call.

## Agenda

- current situation

RIP finalization
- precompile address range

RIP-7212: next steps
open questions

- RIP registry / L2 indication of support
- progressive precompiles & alternatives

open discussion

## Further discussion

Feel free to add comments here with further items of discussion

## Replies

**mratsim** (2024-02-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/adietrichs/48/14646_2.png) adietrichs:

> L2 indication of support

Taiko supports this RIP (and would love to see it on mainnet, it is critical for improving gas cost of our SGX proofs)

---

**abcoathup** (2024-02-08):

## Notes

**thegaram33** here’s a quick summary:

- RIP-7212: adopted by Polygon (live on testnet), zkSync (ready, rollout ETA April), Optimism, Kakarot
- Rollup registry wip: RIPs/registry at rips_registry · ethereum/RIPs · GitHub. Chains that support an RIP on mainnet can be added here. Which chains → inclusion by default, we don’t want to define what a rollup is.
- What if a rollup is not fully compliant with a RIP, e.g. changes gas schedule? Generally it would count as not implementing the RIP. Multi-dimensional fees might address this.
- How to check if an RIP is implemented correctly? We could set up something similar to execution-spec-tests and reuse some of the testing setup from L1.
- Devex issues around partial support for precompiles, devs need to ensure support on each L2 they deploy on. We could use progressive precompiles but that proposal is not compatible with the RIP address range. Suggestion by @yoavw: new precompile that would allow checking RIP support on-chain in a standard way

## Recording

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/3/3a8065ea9ccabc30a2ceeba2ab34d4b9cde0c607.jpeg)](https://www.youtube.com/watch?v=tg01COfxi_M)

---

**abcoathup** (2024-02-11):

## Notes by Scroll:



      [x.com](https://x.com/scroll_zkp/status/1756490663246610849)





####

[@](https://x.com/scroll_zkp/status/1756490663246610849)



  https://x.com/scroll_zkp/status/1756490663246610849

