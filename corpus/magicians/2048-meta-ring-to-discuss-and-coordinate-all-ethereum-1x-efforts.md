---
source: magicians
topic_id: 2048
title: Meta-Ring to discuss and coordinate all "Ethereum 1x" efforts
author: 5chdn
date: "2018-11-28"
category: Working Groups > Ethereum 1.x Ring
tags: [eth1x, ethereum-roadmap, ethereum-1x, meta-ring]
url: https://ethereum-magicians.org/t/meta-ring-to-discuss-and-coordinate-all-ethereum-1x-efforts/2048
views: 1760
likes: 10
posts_count: 3
---

# Meta-Ring to discuss and coordinate all "Ethereum 1x" efforts

This thread is a proposal to create a meta-working-group for Ethereum 1x, ETH 1x, or “1x”-related discussions and coordination.

The initial discussions started in Prague around Devcon4, the following two previous threads pretty much sum up the what has been proposed so far:

- Kicking off the debate Thread to begin discussing "Ethereum 1.0" proposals
- Not suggesting a roadmap yet Ethereum 1 dot X: a half-baked roadmap for mainnet improvements

To summarise, we see the strong need to bridging the gap between the “legacy” Ethereum (1.0) and the “future” Ethereum (2.0, aka Serenity) with something unspecific we call 1x (a.k.a 1.x).

Participants of the various discussions and working groups agreed to have a joint call on Nov-30, 2018: https://github.com/ethereum/pm/issues/65

The current 1x working groups are:

- State Rent Ethereum State rent for Eth 1.x pre-EIP document
- eWasm Ewasm working group proposal for Eth 1.x
- eWasm (duplicate) Ethereum 1.x - Ewasm Working Group proposal
- Simulation of changes/data to inform motivation (Shahan from Pantheon to lead)
- Reducing storage via archiving logs and blocks (Peter from go-ethereum to lead)
- your proposal here …

However, there are some open questions:

- How to transition from a rent-less system to a state-rent system?
- How to deal with “legacy” contracts?
- Is it sufficient to introduce concepts like rent in mid-2019 or shall we think further?
- How to transition from EVM 1.0 to an EVM 1.5 or eWasm environment?
- Does it make sense to talk about block pruning?
- Does it make sense to reset the state at some point?
- Is it worth to consider 1x to be launched as a new, clean, bridged mainnet?

I don’t seek immediate answers to these questions, especially not technical solutions, but would instead encourage people to contribute to a working group that tries to keep an eye on the meta-issues related to 1x, to potentially map out different scenarios for a transition, and finally to propose realistic roadmaps.

## Replies

**boris** (2018-11-28):

Thanks [@5chdn](/u/5chdn). I initially have reacted quite negatively to new chain — like, just as a gut reaction.

As I think about it, and a chain of chains future, and possibilities to tune it for dapp usage, I think this is a very interesting direction.

Another thought I had is adding MORE features to the 1x roadmap — like zkSNARKs / similar privacy features.

A question is still what the path from 1x to 2 is. How can we plan for forward compatibility which leads to a transition / migration / upgrade plan?

Also I would say our [#evm-evolution](https://ethereum-magicians.org/tags/evm-evolution) work fits alongside WASM questions. It’s not a counter proposal — we’re still digging into the current WASM proposal — but think in the spirit of 1x that we can do more evolution, sooner.

---

**jpitts** (2018-11-28):

Looking forward to seeing this meta Ring form!

I would prefer that the Ring be called “Ethereum-1x Ring” instead of “Eth-1.x”. Over time we can work out how this and other meta rings generally function, this is worthy of a topic!

Thank you [@5chdn](/u/5chdn)  for keeping it open to proposals!

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/4/498943cb4f4b99ce905e0ef05a4d90f917d3780f_2_690x209.png)image990×300 40.9 KB](https://ethereum-magicians.org/uploads/default/498943cb4f4b99ce905e0ef05a4d90f917d3780f)

There are two additional projects not posted elsewhere in this Forum that may be relevant here. These are described in [notes](https://docs.google.com/document/d/1IB3oKuH5mryyhmVHE9r3aR6bK2pJCoJgAtiCYTEieh4/edit) from the “private, ad-hoc Ethereum 1.x gatherings in Prague”:

- Simulation of changes/data to inform motivation (Shahan from Pantheon to lead)
- Reducing storage via archiving logs and blocks (Peter from go-ethereum to lead)

