---
source: ethresearch
topic_id: 21225
title: "On Increasing the Block Gas Limit: Technical Considerations & Path Forward"
author: Nero_eth
date: "2024-12-09"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/on-increasing-the-block-gas-limit-technical-considerations-path-forward/21225
views: 2492
likes: 50
posts_count: 8
---

# On Increasing the Block Gas Limit: Technical Considerations & Path Forward

# On Increasing the Block Gas Limit: Technical Considerations & Path Forward

*Authored by: [Toni](https://x.com/nero_eth), [Marek](https://x.com/M25Marek), [Pari](https://x.com/parithosh_j), [Jacek](https://x.com/jcksie), [Paul](https://x.com/paulhauner), [Tim](https://x.com/timbeiko) and [Alex](https://x.com/ralexstokes).*

**Authors’ Note:**

The core development community is committed to continuous improvement of the network’s scalability and user experience. With recent community-driven initiatives, such as [pumpthegas.org](https://pumpthegas.org), there has been a growing call to increase Ethereum’s block gas limit with some proposals approaching 60 million. While this enthusiasm reflects the shared goal of expanding Ethereum’s capacity, it is important to proceed deliberately and in harmony with the technical realities of the protocol and its clients. Before encouraging the community to actively signal for limits beyond 36 million, we may want to deepen our understanding of the potential consequences—conducting more analysis, collecting empirical data, and examining results of upcoming protocol changes in the greatest detail possible—so that adjustments are made with both confidence and caution.

---

## Context

The consensus-layer (CL) clients currently implement certain constraints, as specified by the [formal specifications](https://github.com/ethereum/consensus-specs). These constraints include a maximum acceptable uncompressed block size for gossip propagation, currently set to **10 MiB**. In practice, this indirectly influences the maximum feasible block gas limit. Today, raising the gas limit to **60 million** gas, as proposed by some community members, would generate blocks that exceed this gossip constraint—leading to missed slots and overall network instability.

Until these client-level assumptions can be revisited and improved, the network should move forward with caution when considering increases beyond certain thresholds.

> #### Rationale for Limits (Security Considerations):
>
>
>
> These constraints are not arbitrary; they are in place to safeguard the network. Extremely large blocks can facilitate potential DoS vectors by forcing nodes to handle unwieldy amounts of data. Without practical use cases for such large blocks—and with the risk of malicious actors exploiting them—the core developers have designed limits to mitigate negative effects and protect the network’s health.

---

## What This Means in Practice

- Functionality up to ~40M gas:
Blocks at or below this level remain within the acceptable size range, allowing clients to propagate them and maintain consensus stability. This ensures that validators do not see unexpected missed slots due to overly large blocks which would be prevented from being propagated because of gossip limits.
- Beyond ~40M gas:
Valid blocks larger than 10 MiB could fail to propagate as expected. This results in some validators missing their slots despite producing otherwise valid blocks. The gossip limits, which cannot be easily circumvented today, create a bottleneck. In addition, without further empirical data, the initial analyses guiding the blob count increases may not fully reflect the increased complexities of operating under a significantly higher gas limit.

---

## Why Wait for Pectra?

The core developers have been planning the [Pectra](https://eips.ethereum.org/EIPS/eip-7600) network upgrade that reduces worst-case block sizes and create the headroom needed to safely increase capacity. Two notable upcoming changes are:

- EIP-7623 (Included in Pectra):
This proposal aims to reduce worst-case block sizes. By increasing the cost of calldata for calldata-heavy transactions, it opens pathways to safely handle more capacity—be that additional blobs or a higher gas limit. Reducing worst-case scenarios mitigates potential DoS vectors and helps ensure that the network remains stable and resilient under heavier loads.
- EIP-7691 (Included in Pectra):
This proposal will increase the target/maximum number of blobs per block from 4/6 to 6/9. By observing the network’s performance under increased blob counts, we can gather data on propagation behavior, storage demands, and client resource usage. This empirical evidence will guide safer adjustments in block composition and size.

By first deploying the [Pectra](https://eips.ethereum.org/EIPS/eip-7600) hardfork and analyzing the outcomes of [EIP-7623](https://github.com/ethereum/EIPs/blob/7fbdc5d77b40b6d6d2e0214e202d2917c9a429ea/EIPS/eip-7623.md) and [EIP-7691](https://github.com/ethereum/EIPs/blob/7fbdc5d77b40b6d6d2e0214e202d2917c9a429ea/EIPS/eip-7691.md) in a production environment, we stand to gain critical empirical evidence. This data will inform both core developers and the broader Ethereum community on how the network responds to changes in block composition and size. Armed with this understanding, the community can make more informed decisions on how to increase the gas limit while maintaining Ethereum’s robustness and security.

Future upgrades, such as [PeerDAS](https://eips.ethereum.org/EIPS/eip-7594), will build on these insights, further refining parameters and scaling capabilities as the network evolves.

---

## A Call for Patience and Collaboration

The Ethereum community’s proactive approach and passion for scaling solutions is commendable. Core developers are keenly aware of this momentum and, in general, are supportive of finding a responsible path to increasing the gas limit. However, moving too quickly—especially beyond 36M gas—risks unintended consequences and network instability.

We encourage all stakeholders—users, validators, researchers, and client developers—to remain patient and work together through this transition.

By deferring significant capacity increases until after the [Pectra](https://eips.ethereum.org/EIPS/eip-7600) hardfork, monitoring the real-world effects of [EIP-7623](https://github.com/ethereum/EIPs/blob/7fbdc5d77b40b6d6d2e0214e202d2917c9a429ea/EIPS/eip-7623.md) and [EIP-7691](https://github.com/ethereum/EIPs/blob/7fbdc5d77b40b6d6d2e0214e202d2917c9a429ea/EIPS/eip-7691.md), and carefully reviewing the results, we can ensure that these increases are implemented responsibly and sustainably.

While many sympathize with the desire to see Ethereum’s gas limit significantly increase over a short period, a more incremental approach might be sounder. For instance, starting with a moderate increase to around 36M gas would allow us to carefully monitor the network’s response, assess client performance, and ensure that no unforeseen issues arise. If the data supports further increases, we could then proceed more confidently to higher limits while maintaining the network’s stability and security.

Finally, we may also anticipate further updates and guidance from core developers in the coming days/weeks as they work towards resolving these issues.

---

## In Summary

- The current CL client constraints make immediately raising the gas limit to 60M gas impractical due to block size and gossip propagation issues.
- Increasing the gas limit beyond 36M requires careful, data-driven planning and consideration of DoS resilience.
- The upcoming Pectra hardfork, which includes EIP-7623 and EIP-7691, will provide the groundwork and data needed for safe throughput increases.
- Core developers support scaling the network, but emphasize a measured, evidence-based approach. This is in alignment with the motivation of the pumpthegas.org.

## Replies

**MicahZoltu** (2024-12-09):

I’m sure I sound like a broken record to many, but I’ll once again repeat what I say in all of these gas limit threads:

Storage space required by **users** running nodes is incredibly important and we need to solve the ever-growing state problem before we increase the gas limit, even if we can resolve any DoS vectors that **validators** may face.

There is work (e.g., Portal Network) being undertaken to alleviate some of the end user storage requirements, but IIUC this work is not implemented/integrated in the majority of clients so users still need full state and some amount of history in order to use Ethereum clients today.  While we should address the DoS limitations as outlined here, that alone isn’t sufficient to increase the gas limit.

---

**benaadams** (2024-12-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Storage space required by users running nodes is incredibly important and we need to solve the ever-growing state problem before we increase the gas limit

Dropping pre-merge history has been agreed to happen on 1st May 2025 (with clients commiting to various fallbacks including Portal Network)

Do you think a increase to 36M (+20%) is going to cause any real storage issues by then?

---

**storm** (2024-12-09):

[![image](https://ethresear.ch/uploads/default/optimized/3X/7/7/7778558ced95e8e1b9444cbf3ade55fa93869198_2_690x403.png)image1592×931 71.6 KB](https://ethresear.ch/uploads/default/7778558ced95e8e1b9444cbf3ade55fa93869198)

(from [here](https://www.paradigm.xyz/2024/05/how-to-raise-the-gas-limit-2))

storage size is less of a bottleneck than bandwidth or storage IO. state is relatively small. and history is growing at a smaller rate post 4844 (graph is outdated). full-4444 would still be extremely beneficial but the pre-merge-4444 in pectra will still give a huge amount of runway

from the perspective of hardware constraints, 36M seems like a non issue. delay 60M until post pectra. I think Toni’s analysis is spot on here

---

**markodayan** (2024-12-09):

Of all the activity we need to analyze to be a bit more proactive about these decisions, do you think    the findings around propagation behavior will always be the most urgent thing to be sure of compared to the other effects? Seems like its largely the burst factor that threatens consensus stability (at least according to the current thresholds), other stuff seems more like long-term sustained effects.

Would also be keen to know what exactly is the agreed upon way to profile block propagation. Would it be similar to something like done done in this paper (Page 4): [[2405.03183] Impact of EIP-4844 on Ethereum: Consensus Security, Ethereum Usage, Rollup Transaction Dynamics, and Blob Gas Fee Markets](https://arxiv.org/abs/2405.03183)

---

**MicahZoltu** (2024-12-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/benaadams/48/14892_2.png) benaadams:

> Dropping pre-merge history has been agreed to happen on 1st May 2025 (with clients commiting to various fallbacks including Portal Network)

Dropping ancient history is definitely a positive step, though it comes with downsides like a range of applications ceasing to work in a decentralized way because they depend on ancient historic events (I mostly blame the apps for this design, not the clients for dropping receipt history).

![](https://ethresear.ch/user_avatar/ethresear.ch/benaadams/48/14892_2.png) benaadams:

> Do you think a increase to 36M (+20%) is going to cause any real storage issues by then?

I am of the opinion that we are already way over reasonable state requirements for end-users, and small gains like dropping pre-merge history just help mitigate some of the damage we have already done.  Part of the problem here is that there is no consensus on what the target end-user machine looks like, and there isn’t even consensus (sadly) that end-users should be able to run an Ethereum client at all.

The first step to making informed decisions on this topic is to come to an agreement (among who?) about what the target demographic is for running trustless RPC clients.  Once we have that we can have more interesting discussions around whether a given change will cause us to exceed that target or not.

---

**arnetheduck** (2024-12-12):

Here’s some more background information on the technical aspects of the limit:

[GOSSIP_MAX_SIZE](https://github.com/ethereum/consensus-specs/blob/dev/specs/phase0/p2p-interface.md#constants) is the relevant constant and is currently set to 10MB for the *uncompressed* payload of the block message.

The [contents](https://github.com/ethereum/consensus-specs/blob/dev/specs/phase0/p2p-interface.md#topics-and-messages) of this payload is an SSZ-encoded consensus message. The consensus message has information about consensus matters and also carries the execution payload, which is the the part of the message received from the execution layer. All fields in the consensus layer have fixed bounds on how much space they can possibly use - [in Deneb](https://github.com/ethereum/consensus-specs/blob/dev/specs/deneb/beacon-chain.md#beaconblockbody), this “consensus overhead” amounts to `357288` bytes.

The execution payload is made up of several fields, all of which have constant upper bounds on their length except for the transactions (in the consensus layer, we have a *theoretical* limit of 1024TB of transaction data, for the curious). The constant-size portion of the execution payload is another `1264` bytes.

As such, we can reframe the problem of a maximum gossip size effectively as a limit on the size of the transactions that we can fit in a block - `10127208` bytes.

The advantage of framing it as a limit on transactions is that this field is entirely controlled by the block producer and / or execution clients - they know, as they are constructing the block, what size transactions have and what the sum of the transaction sizes are.

Edit: fixed sizes, thanks [@tbenr](/u/tbenr) for crosschecking with Teku!

---

**arnetheduck** (2024-12-18):

There is now an issue open that describes some of the [long-term solutions](https://github.com/ethereum/consensus-specs/issues/4064) to this conundrum.

