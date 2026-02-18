---
source: ethresearch
topic_id: 22066
title: Introduction to Optimistic V3 Relays
author: gd-0
date: "2025-04-01"
category: Proof-of-Stake
tags: [mev, proposer-builder-separation]
url: https://ethresear.ch/t/introduction-to-optimistic-v3-relays/22066
views: 866
likes: 12
posts_count: 5
---

# Introduction to Optimistic V3 Relays

*Co-authored by [George](https://x.com/gd_gattaca) and [Vlad](https://github.com/vladimir-ea) from [Gattaca](https://x.com/gattacahq). Special thanks to [Alex](https://x.com/alextes) and [Niclas](https://x.com/AlphaMonad) from [Ultrasound](https://x.com/ultrasoundrelay), [Auston](https://x.com/austonst) and [Max](https://x.com/0xKuDeTa) from [Aestus](https://x.com/AestusRelay) and [Colin](https://x.com/colink14110476) and Eric from [bloXroute](https://x.com/bloxroute).*

## Overview

In earlier relay architectures (Optimistic V1 and V2), builders had to transmit full block payloads to the relay upfront for verification. This meant significant data overhead: every block submission included all transactions and blob data, which could be on the order of megabytes per submission. This resulted in huge amounts of redundant network traffic, as all but one submitted payload would ever be returned, burdening the relay with heavy data transfer, processing and costs.

Optimistic V3 is designed to eliminate this overhead by avoiding the transmission of full block data unless absolutely necessary. The key insight is to send only the essential data for auction purposes, namely, the block header, bid trace and signature, while deferring the heavy payload until the block is actually chosen. This design substantially reduces bandwidth usage and reduces block submission latency. With the continued growth in block size, particularly from the increase in the blob limit, this approach becomes increasingly vital to ensure relays can handle rising throughput demands.

### Recap Of The Evolution From Optimistic V1 to V3

- Optimistic V1: Introduced deferred block validation, where the relay optimistically considers a bid without immediately verifying the full block.
- Optimistic V2: Decoupled header from payload, allowing a small header to be processed immediately while the heavier block data arrived asynchronously. Despite latency gains for the header submission, builders were still forced to send full block payloads to the relay in parallel, resulting in duplicate header data and even more bandwidth usage.
- Optimistic V3: Builders submit only the block header and include an address for retrieving the payload from the builder on demand. Full block data is fetched on-demand by the relay, eliminating almost all redundant data transfer.

## Architectural Changes in V3

The protocol between builders and the relay is redesigned as follows:

1. Header-Only Submissions: Builders no longer send full block bodies to the relay up-front. Instead, a builder submits a block header bundle containing the essential data needed for the relay to serve the get_header call: execution payload header, bid trace and signature. In addition, they include an address where the relay can retrieve the full block if the proposal wins.
2. Relay Auction: The relay applies the same auction logic as before. It stores the headers, ranks them, and designates a top bid. Full payloads remain unsent until the header is committed to by the proposer.
3. Deferred Payload Fetching: When a proposer calls get_payload, the relay fetches the full block by following the previously provided address. The builder’s endpoint verifies the request, matches the block hash to its cache, and returns the full payload to the relay.
4. Validation and Block Publishing: After obtaining the full block, the relay performs the standard fast-path validations and verification steps found in the normal submit_block flow. It then sends off for the full block simulation to be processed async. Assuming the block passes all fast-path checks, the relay then runs the standard get_payload flow.

### Discretionary Payload Fetching

While the primary idea of Optimistic V3 is to fetch a block only when a proposer commits to its header, relays may benefit from allowing earlier or discretionary block retrievals. For example:

- Pre-fetching: If the relay can determine which headers are likely to win or know which get_header call was made specifically by the proposer they can pre-fetch the full payload from the builder so it is ready before the get_payload call.
- Bid Adjustments: If the relay is doing bid adjustments they will need to fetch the full payload before responding to the get_header call to run the adjustment logic.

Allowing the relay to decide when and how to request payload data, beyond the strict rule of “only after a proposer’s commitment”, can improve robustness. This approach does carry potential trade-offs, such as revealing partial selection information to builders or incurring extra bandwidth, but given the improvements to reliability seems worthwhile.

### Why Relays Remain Essential Under V3

With Optimistic V3, the relay primarily acts as a stripped-down forwarder for the builder api: it receives header-only submissions and, fetches and forwards the full payload from the builder on demand. Despite this shift, relays remain critical to the broader health and trust assumptions of the Ethereum ecosystem. Specifically:

1. Decentralised Market Access: A relay provides a single integration point for validators to access multiple builders. Instead of each builder having to set up deals with every validator, builders can simply register with the relay. This makes it easier for new entrants to participate in PBS without requiring extensive business development and time, lowering barriers to entry and fostering a more competitive builder market.
2. Fair Exchange and Trust Minimisation: One of the relay’s fundamental tasks remains solving the fair exchange problem. Validators rely on the relay to ensure they receive the promised payment for including a builder’s block. If a block is invalid or fails to pay the proposer, the relay immediately penalises that builder—demoting them for future slots and drawing on collateral to compensate the proposer. This lets validators avoid having to trust or vet every builder themselves, relying instead on the relay’s simulation checks and collateral enforcement.

# Data Size and Network Efficiency Comparison

Optimistic V3’s chief advantage is the substantial reduction in data transmitted between builders and the relay. A single block with six blobs can easily approach 1 MB in total size, around 200 kB for the execution payload plus 6 × 144 kB for blobs. V3 avoids this problem by sending only small headers (~900 bytes, enough to fit into the standard MTU) for the majority of proposals. The full block data, is only transferred once, for the winning proposal.

To highlight this advantage lets look at some submission data from Titan builder. Here are the different percentiles for the number of submissions the builder makes from a single cluster across a 3 second submission period.

|  | p50 | p90 | p95 |
| --- | --- | --- | --- |
|  | 2649 | 3290.9 | 3531.2 |

At P99 that’s 1.25 GB/s of data. Since many relays, including Titan and Ultrasound, operate multiple geographically distributed clusters and receive submissions from multiple builders, overall bandwidth consumption can multiply even further. By contrast, under Optimistic V3, the relay would receive ~1 MB/s of headers, plus a single 1 MB payload for the final selected block.

**Importance for Future Blob Scaling**

This efficiency gain becomes increasingly critical as Ethereum continues to boost its blob limits in upcoming upgrades. Moving from 6 blobs to 9 (Pectra), and potentially up to 96 (Peer-DAS), poses a major challenge for any relay still reliant on full data uploads. The growing blob capacity massively increases the per-block data size, and thus the latency cost for builders to transmit full blocks to the relay on every submission. This may result in builders excluding lower-value blobs to avoid the bandwidth and latency penalties, ultimately weakening Ethereum’s scaling objectives.

This concern is already apparent even under the current 6-blob limit. Blobs often yield minimal additional revenue while incurring a significant latency cost to transmit. As a result, there are many situations in which builders may omit these lower-value blobs or transactions. For example:

1. High Volatility, CEX/DEX Blocks: In blocks dominated by CEX/DEX replacements, speed to include the replacement is critical. If replacements are delayed, the searchers risk adverse selection. Minimising block size can drastically shorten submission time, so lower-value blobs are often the first to be dropped.
2. Late, High Value Transactions: When a high value transaction arrives near the block cut-off, builders may choose to incorporate that single high-paying transaction, and exclude almost everything else, to reduce the time-to-relay.

It is worth noting that some alternative strategies have been proposed to address rising blob data and larger block sizes. One such approach is caching both blobs and transaction data on the relay, so that if a builder reuses the same data in multiple bids, they can simply reference the cached data via hash pointers, reducing redundant uploads. However, we prefer Optimistic V3 for two key reasons:

1. Transfer Timing Near Slot End: Even with caching, a large transfer is still needed the first time that data appears. If this occurs close to the slot boundary or during a spike in submissions, it can still overwhelm the network. Builders would also need to replicate that data across all relays, which under a 96-blob scenario could represent a massive data burst.
2. Geographically Distributed Clusters: Most relay operators run multiple relay instances in a cluster behind a load balancer and others also run multiple clusters worldwide behind a latency routing URL like AWS Route53. Syncing caches across all data centres in real time adds substantial complexity and introduces new overhead to maintain a globally consistent state. If one instance misses some blobs due to routing variance, it cannot serve them properly on a subsequent reference.

# Trade-Offs and Risks

- Dependency on Builder Uptime and Responsiveness: Because the relay only fetches the full block when it’s needed, this design depends on the builder being online and fast when the relay requires the payload. If the builder is down or fails to respond in time, the relay cannot deliver a valid block for the proposer, resulting in a missed slot. This risk is mitigated by the fact that builders already operate redundant, highly-available endpoints and that failure to return results in slashed collateral. However, there is still a large amount of work to be done here to figure out how to fairly detect “slow” builder responses.
- Additional latency in the get_payload call: Retrieving the block on demand adds a small overhead to the relay’s processing time in the get_payload call. If the proposer calls get_payload late, this delay could result in a missed slot. In practice, with co-located builders and current submission latencies, the overhead is generally under 5 ms, which is likely acceptable. Builders that consistently respond slowly can be demoted from V3 optimistic. Relays will also be able to pre-fetch payloads for headers that they think might be selected.

# Technical Specification

Paths

1. /relay/v3/builder/headers

Endpoint for submitting v3 header-only blocks to the relay.

1. /get_payload_v3

New endpoint on the builder’s server, where the relay requests the full block payload if needed.

**Encoding:**

The standard `SSZ` and `JSON` encoding used in relay communication is supported for both messages.

### Header Submission (Relay Endpoint)

**Path:** `POST /relay/v3/builder/headers`

`HeaderSubmissionV3` is sent from the builder to the relay in order to submit a new block header. The header submission payload is a `HeaderSubmissionv3` structure that wraps the standard `SignedHeaderSubmission` (as used in Optimistic v2):

```rust
struct HeaderSubmissionV3 {
    /// URL pointing to the builder's server endpoint for retrieving
    /// the full block payload if this header is selected.
    pub url: Vec,

    /// The signed header data. This is the same structure used by
    /// the Optimistic V2 'SignedHeaderSubmission', carrying:
    ///   - ExecutionHeader
    ///   - BidTrace
    ///   - Signature
    pub submission: SignedHeaderSubmission,
}
```

URL must be a network address (e.g., [https://builder.example.com](https://builder.example.com/get_payload_v3)) that serves the `get_payload_v3` path where the relay can retrieve the full block.

### Payload Retrieval (Builder Endpoint)

**Path:** `POST /get_payload_v3`

If / when the relay wants to retrieve the block payload for a `HeaderSubmissionV3` it will make a POST to the provided URL on the `get_payload_v3` path.

```rust
struct GetPayloadV3 {
    /// Hash of the block header from the `SignedHeaderSubmission`.
    pub block_hash: B256,
    /// Timestamp (in milliseconds) when the relay made this request.
    pub request_ts: u64,
    /// Bls public key of the signing key that was used to create
    /// the `signature` field in `SignedGetPayloadV3`.
    pub relay_public_key: BlsPublicKey,
}

struct SignedGetPayloadV3 {
    pub message: GetPayloadV3,
    /// Signature from the relay's key that it uses to sign the `get_header`
    /// responses.
    pub signature: BlsSignature,
}
```

The `block_hash` field is the hash of the requested block. `request_ts` is a millisecond UTC timestamp set to the time the relay made this request.

**Response Body**

The builder must return the full block payload in the same `SignedBuilderBid` type as the standard builder submissions.

## Replies

**antonydenyer** (2025-04-03):

One concern I have is around **incentive alignment**. Further entrenching the reputation-based nature of relays seems problematic — it risks centralizing trust and creating barriers to entry.

Have you considered a mechanism where block builders also submit a **commitment block** alongside their bid? This commitment block would contain only the builder’s payment to the proposer — effectively acting as **collateral**. The data overhead remains low, though not as minimal as in the proposed case.

If the relay fails to fetch the block, it could fall back to sending the commitment block. This guarantees that the proposer still receives payment, even if the full block is unavailable. The relay could perform basic validation, moving slightly away from a purely optimistic model.

This approach could help further align incentives: block builders are economically motivated to remain available and deliver the block, while proposers are protected from failed deliveries. It also reduces reliance on reputation by introducing a **trust-minimized fallback**.

---

**gd-0** (2025-04-03):

Agree that v3 does give relays a bigger role because of the extra conditions around demoting builders. I don’t see how that necessarily increases the barrier for new entrants, though, could you clarify why you think it does?

As for the commitment block proposal, it would require the proposer to sign two separate headers. One for the main block, then if the builder fails to deliver the main block, the relay would have to ask for another signature on the fallback header. That second round of signing adds a significant amount of risk to the proposer as a malicious/ buggy relay could broadcast both headers, causing the proposer to equivocate and get slashed. It would also require significant changes to the beacon/ validator clients to support double signing. It also requires similar trust in the relay to the current collateral implementation, as the relay must release the commitment block for the proposer to be paid.

---

**antonydenyer** (2025-04-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/gd-0/48/12254_2.png) gd-0:

> don’t see how that necessarily increases the barrier for new entrants, though, could you clarify why you think it does?

Because it’s reputation-based, a new entrant will never be able to compete on level terms immediately. However, if it’s solely based on economic terms, it’s a more level playing field.

![](https://ethresear.ch/user_avatar/ethresear.ch/gd-0/48/12254_2.png) gd-0:

> That second round of signing adds a significant amount of risk to the proposer as a malicious/ buggy relay could broadcast both headers, causing the proposer to equivocate and get slashed

Many such trust problems with PBS ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/gd-0/48/12254_2.png) gd-0:

> It would also require significant changes to the beacon/ validator clients to support double signing. It also requires similar trust in the relay to the current collateral implementation, as the relay must release the commitment block for the proposer to be paid.

That’s fair. Maybe it could be down to the relay to decide if they have the block builders’ payment transaction. Then, if something fails, the relay can still build a block with payment for the proposer.

---

**gd-0** (2025-04-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/antonydenyer/48/20160_2.png) antonydenyer:

> Because it’s reputation-based, a new entrant will never be able to compete on level terms immediately. However, if it’s solely based on economic terms, it’s a more level playing field.

Right, gotcha. Similar to optimistic v1/v2, access is purely based on collateral. If the builder posts collateral, then for all blocks with a value lower than that collateral, they’ll have access to v3 submissions.

![](https://ethresear.ch/user_avatar/ethresear.ch/antonydenyer/48/20160_2.png) antonydenyer:

> That’s fair. Maybe it could be down to the relay to decide if they have the block builders’ payment transaction. Then, if something fails, the relay can still build a block with payment for the proposer.

I think this has similar issues as the initial proposal. e.g., I don’t think there is a significant difference between the relay holding collateral from the builder vs holding a payment transaction from the builder.

