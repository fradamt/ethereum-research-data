---
source: ethresearch
topic_id: 22313
title: "Fenwick + Bitmap: constant-time matching for on-chain order books"
author: dev-clober
date: "2025-05-12"
category: Decentralized exchanges
tags: []
url: https://ethresear.ch/t/fenwick-bitmap-constant-time-matching-for-on-chain-order-books/22313
views: 285
likes: 2
posts_count: 1
---

# Fenwick + Bitmap: constant-time matching for on-chain order books

### 1. Why DeFi needs a limit-order book that runs on-chain

In traditional markets, liquidity emerges naturally through limit orders placed by diverse participants, each serving a distinct purpose. Professional market makers rely on limit orders to manage their exposure precisely, dynamically adjusting their bid-ask quotes to supply efficient liquidity under changing market conditions. At the same time, directional participants, such as institutional hedgers, asset managers, and retail traders, use limit orders to express their market views explicitly, embedding their directional bets into the order book. Collectively, these varied limit orders aggregate into liquidity, providing depth and efficiency that no single liquidity provider could match alone. This multifaceted liquidity, formed by limit orders from both sophisticated market makers and directional traders, ultimately enhances the resilience and transparency of the overall trading ecosystem.

DeFi automated-market-maker pools emerged as a practical solution tailored specifically for environments with high computational costs, prioritizing gas efficiency over capital efficiency. While effective as a minimum viable mechanism for low-throughput liquidity provision, AMMs are fundamentally limited in their ability to accommodate directional liquidity. Because AMMs cannot handle explicit limit orders, they fail to capture directional market views from participants who would otherwise post limit orders to express their trading intent. Additionally, the rigidity of AMM algorithms prevents sophisticated market-making strategies, restricting liquidity providers to simple, passive two-sided quoting mechanisms. These inherent limitations make AMMs insufficient to reflect the nuanced directional bets and dynamic liquidity adjustments central to traditional, limit-order-driven market structures.

A native on-chain order book can overcome these fundamental limitations by fully capturing the depth, transparency, and dynamic price discovery provided by traditional limit-order-driven markets. By directly enabling participants, including professional market makers deploying sophisticated quoting strategies and directional traders embedding explicit market views, to submit and manage limit orders fully on-chain, this model facilitates efficient and expressive liquidity formation. Achieving this within the constraints of decentralized networks requires a matching engine designed to operate efficiently under strict gas and latency constraints, performing critical functions with minimal computational overhead while preserving the deterministic price-time priority essential for fair execution.

---

### 2. Complexity targets

| Task | Required complexity | Why the bound matters |
| --- | --- | --- |
| Locate the best executable price | O(1) | Search cost must remain fixed even when most ticks are empty. |
| Place or cancel at one price level | O(log m) where m is the number of quotes at that level | Cancels are as common as placements. |
| Execute a market order that crosses levels | O(t) where t is the number of price levels the order touches | Gas should scale with depth consumed, not with maker count. |

With a practical cap of thirty thousand quotes per price level log m stays below fifteen, so maker actions behave like a constant.

---

### 3. Two compact structures that meet those bounds

| Layer | Structure | What it does | Cost profile |
| --- | --- | --- | --- |
| Price directory | Three-tier bitmap | L0 stores one bit per price tick, L1 stores one bit for every block of 256 L0 bits, and L2 stores one bit for every 256 L1 bits. Setting or clearing a price level touches at most three bits. Finding the best price reads one word from each tier and counts trailing zeros. | Exactly three storage reads, constant time. |
| Inside one price level | Fenwick tree | Quotes receive increasing sequence numbers. The tree stores live sizes as overlapping partial sums. Adding or cancelling updates log m cells, and computing volume ahead of a sequence reads the same log m cells. | At most fifteen reads and two writes under the depth cap. |

The bitmap keeps taker cost tied to the number of price levels crossed, and the Fenwick tree keeps maker cost limited to a few cells inside the chosen level.

---

### 4. Core engine operations

**Placing a limit order**

The engine assigns a sequence number at the chosen price, adds the size to the level’s Fenwick tree, raises the depth counter, and, if this is the first quote in the tick, sets the corresponding bits in all three bitmap tiers.

**Canceling an order**

The contract reads a prefix sum to see how many units have filled, removes the remainder from both the tree and the depth counter, refunds the maker, and, if depth falls to zero, clears the bitmap bits for that tick.

**Submitting a market order**

The engine iterates through three constant-cost steps:

1. Read the best price through the bitmap
2. Match as much volume as possible at that price by advancing the filled cursor
3. Continue if volume remains

Because the loop runs once per price level gas depends on ticks crossed, not maker count.

**Claiming proceeds**

A maker compares the filled cursor with a prefix sum just before the order’s sequence, withdraws the difference, and records the claim.

---

### 5. Gas outline

| Path | Typical reads | Typical writes | Gas estimate |
| --- | --- | --- | --- |
| Best-price lookup | 3 | 0 | a few thousand |
| Place quote | up to 18 | 1–4 | ~40 k |
| Cancel quote | up to 17 | 2–3 | ~50 k |
| Sweep one price level | 3 | 2 | ~20 k |

Even in the busiest tick a taker never touches individual maker slots.

---

### 6. Safety and storage notes

- Matching logic finishes before any external transfer, preventing re-entrancy from reordering fills.
- Depth counters increase monotonically, blocking over-claims and double refunds.
- After proceeds are claimed the tree entry resets to zero, allowing sequence numbers to wrap and keeping storage bounded.

---

### 7. Position among other engines

| Aspect | Fenwick + Bitmap | Segmented-segment tree with heap | Radix-tree heap |
| --- | --- | --- | --- |
| Price lookup | constant three reads | bitmap read plus optional heap read | walk branch |
| Depth cap per level | none | 32,768 quotes | none |
| Maker edit cost | log m, small constant | log m, four fixed writes | log N, can reach sixty writes |
| Market sweep cost | one pass per level | similar | one step if subtree detaches |
| Tick spacing | fixed grid | fixed grid | arbitrary spacing |

- The Segmented-Segment Tree with Heap performs best in very sparse order books because its heap structure efficiently skips empty ticks, reducing read overhead in sparse conditions. It also imposes a strict depth cap per price level, inherently limiting spam but requiring heap management and introducing complexity.
- The Radix-Tree model handles large market orders extremely efficiently when entire branches of price levels vanish, effectively deleting multiple prices simultaneously in near-constant time. However, during volatile conditions with frequent cancellations at deep levels, it may incur substantial gas spikes due to extensive updates across nodes.
- The Fenwick + Bitmap approach described here offers predictable gas costs and simpler maintenance by avoiding heap management. It achieves constant-time price lookup regardless of market density, and each maker’s interaction is confined to a small, predictable set of storage operations. This makes it particularly suitable for environments with high maker activity and frequent cancellations, ensuring consistent gas performance without abrupt spikes.

When choosing an on-chain matching engine, projects should consider expected market density, volatility patterns, tolerance for complexity, and requirements for consistent gas consumption.

---

### 8. Conclusion

The three-tier bitmap locates the next price level in constant time, and the per-level Fenwick tree keeps maker edits within tiny logarithmic cost, reproducing price-time priority on-chain without external helpers and staying within realistic gas limits. This design makes proactive quoting, deep visible liquidity, and deterministic execution possible in DeFi. Feedback, stress tests, and formal proofs are welcome.
