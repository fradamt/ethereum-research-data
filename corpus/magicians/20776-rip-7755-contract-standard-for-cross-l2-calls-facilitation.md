---
source: magicians
topic_id: 20776
title: "RIP-7755: Contract standard for cross-L2 calls facilitation"
author: wilsoncusack
date: "2024-08-12"
category: RIPs
tags: []
url: https://ethereum-magicians.org/t/rip-7755-contract-standard-for-cross-l2-calls-facilitation/20776
views: 2958
likes: 16
posts_count: 9
---

# RIP-7755: Contract standard for cross-L2 calls facilitation

Hi! I’ve been wishing for a lower-level ERC for cross-chain calls. In thinking on this, I often got stuck trying to find a opinionated and secure system for proving a call happened on some other chain. In talking to others, I realized that for cross L2 calls we should be able to leverage our ability to do state proofs about the other chain using (1) the L1 block hash (2) the L2 state that gets posted to L1.

I’ve written up a [pull request](https://github.com/ethereum/RIPs/pull/31) here to start discussion on this and welcome feedback!

## Replies

**srao** (2024-08-30):

Hey everyone!

Our team at Eco Inc. just open-sourced our contribution to RIP-7755.  We’ve already been talking with [@wilsoncusack](/u/wilsoncusack) about it but wanted to share it here as well.

You can find all the details on Cross-L2 Actions here:

— [Repository](https://github.com/ecoinc/Cross-L2-Actions) / [Twitter Announcement](https://x.com/eco_incorp/status/1829210253390733741)

Outside the open source repo, we’ve also been working on a vision for expanding this into a fully fledged protocol, which you can check out here: [Eco Docs](https://eco.com/docs)

We’re excited to hear any feedback!

---

**ylv-io** (2024-09-05):

I like the idea of storing everything on-chain, but I must point out that storing the entire calldata in a contract’s storage is expensive and counterintuitive in terms of EVM design.

---

**cjcobb23** (2025-03-19):

What stops a filler from supplying the wrong data for the cross chain call? Obviously they would not be able to claim the reward on the origin chain, but I am worried this could cause an invalid state transition on the receiving app, since the app doesn’t know at the time of execution that the data is wrong.

---

**jackchuma** (2025-03-19):

Curious if you can come up with an example of an unauthenticated invalid state transition?

You’re right to be concerned with this detail - the architecture is optimistic by nature and from the context of the destination chain, it assumes the request being submitted exists on a source chain to prevent having to wait for source chain finality.

For transactions involving token bridging or swapping, a fulfiller is not incentivized to submit invalid data because it involves giving up currency and getting nothing in return on the source chain. If the target contract involves some sort of sensitive state update and is callable by the 7755 `Inbox` contract, I’d argue that’s a security issue for the target contract

---

**cjcobb23** (2025-03-19):

One example could be some sort of cross chain governance. It would not be safe to pass votes as cross chain messages with optimistic execution, since the vote the filler passes is not necessarily the actual vote. Or imagine some sort of cross chain dex, where orders can be created on one chain but filled from another. If the filler delivers a message saying an order was created (or filled), the dApp can’t actually trust the message and could end up invalidly updating its state.

Optimistic execution works well for token bridging or swapping, but is not necessarily safe for arbitrary contract calls. It depends on the logic being executed, and dApp developers need to be careful.

---

**jackchuma** (2025-03-20):

For sure, dApp developers need to be careful. Generally, no special privileges should be granted to the Inbox contract. I think for casting votes, perhaps the smart account support can address that? It does require a signature from the account owner in that case. If the voter is an EOA, the protocol receiving votes would likely need to use ECDSA signatures or something of that nature. For extremely sensitive state updates, a middleware contract could be deployed as the target on destination chain that receives the request and holds it in escrow until the source chain state finalizes on L1. At that point, a proof of the existence of the source chain request could be submitted to finalize the destination chain transaction.

---

**cjcobb23** (2025-03-21):

I think for this to truly be an interface for cross chain calls, there would need to be a way for the dApp to opt out of optimistic execution, and only receive fully verified calls. I think this should be supported out of the box by the protocol itself, instead of something dApps need to implement on top of the protocol.

---

**SanLeo461** (2025-03-26):

What about the case of ERC1271 smart accounts which validate signatures via contract calls? There would be no way to verify them.

In a more general case, there would be no secure way for any possible contract to initiate a cross-chain call which the receiving contract could verify came from said contract.

I think the optimistic fulfillment case is useful for some usecases, but not all of them. I agree with [@cjcobb23](/u/cjcobb23) that there should be an option to only use finalized state to ensure source call verification.

I think this is especially important given that the future roadmap of Ethereum is trying to unify the properties of EOAs and contracts in a way. (e.g. 4337, 7702, EOF, etc.)

It would be counterproductive to have 2 separate protocols or to require dApp developers build their own call verification middleware for cross-chain calls that are from EOAs vs Contracts.

Better to just unify the standard, even if it means adding some extra config options regarding security/optimisticness.

Besides, long term finalization (1+ week) probably isn’t going to be the norm forever. When we get SSF and more chains transition to ZKPs for instant finalization, the UX for this standard will get an instant boost, and cross chain calls will be minutes, not weeks.

