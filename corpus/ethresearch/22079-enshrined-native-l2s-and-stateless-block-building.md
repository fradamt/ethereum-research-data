---
source: ethresearch
topic_id: 22079
title: Enshrined Native L2s and Stateless Block Building
author: keyneom
date: "2025-04-02"
category: Sharding
tags: [zk-roll-up, stateless]
url: https://ethresear.ch/t/enshrined-native-l2s-and-stateless-block-building/22079
views: 522
likes: 6
posts_count: 6
---

# Enshrined Native L2s and Stateless Block Building

# Scaling Ethereum with Enshrined Native L2s and Stateless Block Building

## Introduction

Ethereum’s scalability journey has long explored Layer 2 (L2) solutions to boost throughput while preserving decentralization. One promising direction—building on prior work like based rollups—is the concept of *enshrined native L2s*. In this post I argue we can scale Ethereum by creating L2 systems deeply integrated into Ethereum’s protocol, sharing its validator set to process transactions in parallel. This isn’t a novel invention but a refinement of existing ideas, leveraging validators not active in Layer 1 (L1) duties through concepts like Orbit to scale throughput horizontally. By cycling validators between L1 and multiple L2s, we can unlock additional truly native blockspace, increase transaction capacity, and introduce local fee markets—all without demanding ever-heavier node hardware. Each L2 would have the same gas limits and other configurations set as the L1. I do not believe these enshrined native L2s are likely to be highly competitive with non-enshrined L2s. Those are obviously more capable of scaling throughput vertically and creating communities that can tolerate varying degrees of censorship that the enshrined native rollups would not be able to do.

I don’t believe we can safely outsource block building without having a viable enshrined fallback that would result in drastically lower throughput. Outsourcing block building to sophisticated actors will inevitably create a dependency on them. As MEV reduces over time (applications are incentivized to capture it themselves) block builders earn less and less revenue. As throughput increases, the cost to build blocks becomes more and more expensive. Profitability therefore depends on sophisticated, proprietary knowledge significantly increasing the difficulty of new entrants to block building being competitive. When auctions are winner takes all non-competitive builders cannot survive and you end up high centralization (a duopoly or monopoly wouldn’t be surprising to me). You can navigate through some threads on my perspective here: [In Defense of Local Block Building](https://x.com/keyneom/status/1894523301999120501).

This post will touch on the available design space, focusing on trade-offs and the critical role of stateless block building to horizontal scaling that allows us to keep local block building and keeps Ethereum forkability practical.

## Core Concept: Enshrined Native L2s with Shared Validators

Enshrined native L2s extend Ethereum’s validator set beyond L1 duties. Currently 31/32 validators are not really actively useful for Ethereum. Ideally we want a system that can ensure as much of the network is productively leveraged as possible. We can take validators not proposing or attesting on L1 (e.g., due to rotation in systems like Orbit) and shift them to L2s, forming committees to handle transaction sequencing and block production. e.g. we could have committees of 96 validators per L2, with 16 validators assigned to FOCIL/proposing duties and the rest attesting. Just like the L1, we would expect a super majority of the L2s stake to attest to the new block for it to be accepted and finalized. Every slot we can rotate 4 validators (I’m speaking as if all validators are 32 eth of stake but I’m aware this is not the case, there’s some complexity here on validator selection, etc. but I think it is something we can solve and want to keep things simple for now) from the L2 they are currently on and transition them back to L1 or another L2, ensuring continuous productivity.

- Shared Security: These L2s inherit Ethereum’s security via zero-knowledge (zk) proofs, validated by the same consensus mechanism and pretty much equivalent censorship resistance guarantees (something basically no L2s currently have).
- Horizontal Scaling: Adding more L2s increases throughput without vertically scaling hardware, contrasting with traditional node upgrades.

This leverages the fact that, in systems like Orbit, ~80% of validator stake might be active on L1, leaving ~20% available for L2s, amplifying native blockspace.

## The Necessity of Stateless Block Building

For this to work, *stateless block building* is desirable. Validators can’t store the full state as storage requirements continue to grow even on L1 and much less including all L2s. Instead:

- How It Works: Users or state providers supply witnesses (state data + proofs) with transactions. Validators use Verkle trees to verify these compact proofs (~150 bytes) against the state root, building blocks without local state. You might be able to have certain optimizations that allow for zkEVM proofs of execution that don’t conflict with any other state changes to be submitted as a valid transaction as well at lower gas costs.
- Why It Matters: Statelessness keeps hardware requirements low, enabling fast transitions between L1 and L2 duties. It’s the backbone of horizontal scaling, ensuring validators can handle any L2 without syncing massive datasets.

Without statelessness, the benefits of enshrined L2s—flexibility, scalability, and broad participation—collapse under impractical storage and time-to-sync demands.

## Trade-offs in the Design Space

Here’s where the rubber meets the road: balancing validator roles, state management, and bandwidth to make this viable.

### 1. Validator Committee Size vs. Throughput

- Trade-off: Smaller committees (e.g., dozens of validators) simplify coordination and transitions but risk security. Larger ones (e.g., hundreds) enhance decentralization at the cost of overhead.
- Example Shift: With ~20% of validators free from L1, a committee of 100 might support many L2s, while 200 per L2 halves that number but bolsters resilience.
- Impact: More L2s mean higher throughput, but committee size dictates how many can run securely in parallel. Not only this but at a certain point L1 Gas limits limit how many L2s can actually be supported as well.

### 2. Verkle Tree (or equivalent) Levels Stored by Validators

We can set a requirement that validators store the root and all intermediate nodes of the Verkle tree up to a certain level, rather than just the root. This allows them to verify witnesses more efficiently without needing to store the entire state but also allows us to reduce the bandwidth overhead of transmitting large witnesses for every transaction. Storing the root and a diff of the previous slot’s tree can help with avoiding invalidating otherwise valid txs that referenced the prior slots state but were too late into the slot to be included and would be invalidated by other transactions modifying their proof paths.

- Trade-off: Storing upper Verkle tree levels (e.g., root to intermediates) reduces witness sizes but increases memory. Storing none keeps validators lean but bloats transaction data.
- Example Shift: For a branching factor of 256, storing Levels 0–3 would be I think ~1.7 GB with about 4 billion leaf nodes. At 512 branching, it’s ~13 GB but gives us ~69 billion leaf nodes (leaf nodes for L1 and each L2 with good interop I think this should be good enough for a while).
- Impact: More stored levels offset bandwidth increases, letting throughput scale without choking the network.

### 3. Bandwidth vs. Throughput Gains

- Trade-off: Statelessness increases bandwidth per transaction (witnesses), but enshrined L2s multiply native blockspace, potentially dwarfing this cost.
- Key Benefit: If switching to stateless block building increases bandwidth requirements by 5x but enables us to support 500 enshrined native L2s then it might be worth the tradeoff. This also creates local fee markets per L2, so if we allow for app migration we might see apps that interact often settle next to each other within L2s to avoid interop overhead and large apps move to L2s with lower use to avoid being impacted by demand for other apps driving up fees for users. All of which is to say that over the long term we might see close to optimal throughput achieved.

### 4. Validator Transition Speed

- Trade-off: Minimal state (root only) stored in memory for validators enables near-instant transitions but demands larger witnesses. Storing intermediate levels slows transitions for tx bandwidth savings. We could include other things like all smart contract code is expected to be stored by the validators and would need to be synced before they are able to participate in L2 duties besides attestation. i.e. contract storage slots or eoa accounts, etc would be expected to have witnesses provided by the user (a state provider could provide the user with that data of course as well and ideally we have the eLTS–see my eth research post for more details there–as a back up). This means that the user only needs to provide a few witnesses for storage slots or account balances and all validators would be able to execute all transactions at all times. There are alternatives to this where we only keep an active set of contracts in memory and the rest would need witnesses provided for them. This recent post discusses that in greater detail (A Protocol Design View on Statelessness).
- Example Shift: Root-only transitions take ~1 second, while ~1.7 GB syncing might take ~5 minutes, depending on network speed requirements for validators.
- Impact: Faster transitions maximize validator utility, but slower ones optimize transaction efficiency.

## Why This Matters: Throughput and Beyond

- Native Blockspace: Enshrined L2s create a massive increase in native blockspace, allowing Ethereum to scale horizontally. This is a key differentiator from other L2s that rely on external validators.
- Bandwidth Offset: Yes, stateless witnesses increase bandwidth, but ideally the increase in native blockspace via L2s can far outpace this.
- Local Fee Markets: With enshrined L2s, we can create local fee markets, preventing demand on one app from impacting simple payments from being practical elsewhere. Enshrined L2s could receive a free allotment of blobspace or have a variety of other fee mechanisms and/or issuance mechanisms to find a reasonable balance to how this works.

## Conclusion

There’s obviously a ton of work that would be necessary to carry out this vision with plenty of open questions on the balance to strike between certain trade-offs. I believe enshrined native L2s, powered by stateless block building, offer the best path to scale Ethereum horizontally and maintain its long-term censorship resistance. Controlling fork choice has serious ramifications. When we limit who is capable of building the chain from a practical perspective we give up fork choice and leave ourselves susceptible to the influence of powerful actors to the harm of everyone else. Approaches to SSF like orbit that enable anyone to participate in voting on forks are our best path forwards. It also enables us to tap validators that aren’t active in L1 duties for potentially massive throughput gains. We *can* enhance capacity while keeping nodes accessible and *without* losing Ethereum’s decentralized soul.

## Replies

**keyneom** (2025-04-02):

I threw this together pretty quickly so, if there’s something I’m missing or mistakes or just a general sense of abstractness, please let me know and I’d be happy to try to address it!

---

**barnabe** (2025-04-03):

Thank you for the post! It’s actually a very close design to what “eth2 phase 2” was proposing with sharding: Sample validator committees and assign them to shards which they validate (i.e., run the state transition function and attest to validity if everything checks out). There too it would have made sense to rely on as much statelessness as possible, given that validators were expected to rotate (infrequently) between shards. It’s also pretty close to the idea of [collators](https://wiki.polkadot.network/learn/learn-collator/) in Polkadot, I think.

There are differences of course, in your design, it looks more like assigning validators as decentralised sequencers of native rollups (in the sense of rollups using the `EXECUTE` opcode as described [here](https://ethresear.ch/t/native-rollups-superpowers-from-l1-execution/21517)). To some extent, getting validators involved with construction of L2 blocks also has a flavour of based rollups, but here you propose to go further and involve them e.g., in FOCIL committees too.

I still don’t think it’s an either/or when it comes to keeping throughput at local building limits. In your design, it’s still critical to use blobs to make the L2 data available. These blobs are provided by the L1 validator set as a whole, in that all are expected to participate in the dissemination of the blob, albeit maybe not in its sampling if they are not attesters for that slot. So it may still be desirable to push blob throughput beyond what some L1 validators as local builders can achieve. You also assume that L2s in your design are secured by zk proofs—these proofs need to be computed, and you may not want to be limited by the best proving capacity of the worst validator assigned to the L2.

---

**keyneom** (2025-04-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/keyneom/48/19968_2.png) keyneom:

> This isn’t a novel invention

I agree it is basically an existing concept. This is just how I would envision it.

![](https://ethresear.ch/user_avatar/ethresear.ch/barnabe/48/4742_2.png) barnabe:

> you may not want to be limited by the best proving capacity of the worst validator assigned to the L2.

Ideally we as a community determine minimum requirements that allow for home validators to build. In my opinion, those could be on the relatively high end of consumer hardware.

---

**hanniabu** (2025-05-12):

There’s existing specs for local block builders here [EIPs/EIPS/eip-7870.md at 1dd2558f9a68d9453aed71c803fdda09d83c6e37 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/blob/1dd2558f9a68d9453aed71c803fdda09d83c6e37/EIPS/eip-7870.md)

---

**keyneom** (2025-05-13):

I know, I’m mostly concerned about how those requirements evolve and how we can scale without increasing them beyond what I believe is truly safe.

You can find some background on what drives this post by scrolling up through this thread here: https://x.com/keyneom/status/1894535989265404233

