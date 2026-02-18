---
source: ethresearch
topic_id: 22922
title: "Ethereum Settlement Score (ESS): Revitalizing the Rollup-Centric Roadmap"
author: gitpusha
date: "2025-08-15"
category: Layer 2
tags: [zk-roll-up, rollup, based-sequencing]
url: https://ethresear.ch/t/ethereum-settlement-score-ess-revitalizing-the-rollup-centric-roadmap/22922
views: 869
likes: 11
posts_count: 3
---

# Ethereum Settlement Score (ESS): Revitalizing the Rollup-Centric Roadmap

[![](https://ethresear.ch/uploads/default/optimized/3X/1/e/1ea0c772c6e67a5fe3f4b78def864e2d89033f05_2_290x413.png)850×1208 30.5 KB](https://ethresear.ch/uploads/default/1ea0c772c6e67a5fe3f4b78def864e2d89033f05)[![](https://ethresear.ch/uploads/default/optimized/3X/a/1/a1dc9b24f0b4922712753f525f28f320507af85c_2_291x413.png)850×1208 30.8 KB](https://ethresear.ch/uploads/default/a1dc9b24f0b4922712753f525f28f320507af85c)

Arbitrum One and Base leveraged Ethereum security for only ~28% of its TVS for last month

**TL;DR**

- L2s aren’t using Ethereum settlement as intended - Most assets and transactions on L2s bypass Ethereum settlement through third-party bridges, external assets, and native tokens.
- Asset settlement defines true security - The real question about infrastructure-level security is who controls the underlying ledger: Ethereum (canonical assets), external bridges (CCTP USDC, LayerZero OFTs), or the L2 itself (native tokens like AERO, KAITO, ARB).
- Current metrics create a false sense of ecosystem maturity - L2Beat green slices focus on theoretical security properties, not actual usage patterns.
- Ethereum Settlement Score (ESS) measures how much an L2 actually leverages Ethereum security by tracking canonical asset ratio, canonical bridge usage, external/native token dependence, settlement latency, and force inclusion.
- Ethereum should be leveraged as a security exporter - Native rollups will make canonical bridges truly trustless (Ethereum secured). Even Stage 2 rollups retain security councils that prevent full Ethereum security inheritance. We need “Stage 3” Native Rollups where L2s eliminate all intermediate trust assumptions.
- Ethereum must be relied on as a censorship-resistance exporter - The ability for users to force transaction inclusion against sequencer censorship (as in Based Rollups) preserves the fundamental property that makes Ethereum valuable in the first place.
- Zero Knowledge (ZK) tech will remove the training wheels - Instead of the current 7-day withdrawal periods, ZK will enable instant verified withdrawals through canonical bridges, finally making them competitive with third-party solutions while maintaining Ethereum’s full security.
- Stage 4 sets the memetic north star - The ultimate vision is beyond what L2Beat currently accounts for. Stage 4 “UltraSound L2s” combine Native Rollups (Stage 3) with “Based” properties (real-time force inclusion) and an ESS of 1, to achieve perfect Ethereum-equivalent censorship resistance and settlement guarantees both in theory and in practice.

## Data Sources

For real-world data inputs to accompany this ESS scoring exercise, we’ve created public dashboards that analyze the two biggest current-day L2s, Arbitrum and Base:

- Arbitrum Dashboard
- Base Dashboard

These dashboards provide comprehensive data on the L2s’ canonical vs. external bridge usage, asset composition, and other settlement patterns that serve as the foundation for our ESS calculations.

## Introduction

In our work running 50+ Ethereum L2s in production through Gelato RaaS, we’ve observed patterns in asset flows and settlement behavior that have emerged through UX improvements which depart from Ethereum’s security guarantees. The implications of these usage patterns are a big deal. That’s why **we need a new measurement framework** that takes into account the extent to which L2s are aligned with the original vision for Ethereum.

This framework addresses the [two critical aspects](https://warpcast.com/vitalik.eth/0xad052076) that Vitalik Buterin recently emphasized as a priority for the ecosystem:

1. Usage of Ethereum where users actually benefit from its underlying properties: To fulfill this goal, we need to measure whether users of L2s are genuinely benefiting from Ethereum’s censorship resistance, decentralization, and security, or if they’re operating in adjacent ecosystems with different trust assumptions. If the latter is true, we’re paying the costs of Ethereum alignment without inheriting the benefits.
2. Resilience and decentralization viewed holistically: We should account for asset settlement risks imposed by security councils, multisigs, sequencers and bridge service providers. Some of these centralization vectors were introduced specifically because they brought much-needed UX improvement, and others were deemed “training wheels” meant to come off with ecosystem maturity.

With native rollups on the horizon promising to eliminate reliance on security councils and multisigs, the roadmap toward a unified Ethereum is clear. How do we make the most of the L2 ecosystem until that day comes? I believe we can defragment the Ethereum L2 rollup space and return to Ethereum-centricism by bringing better transparency to Ethereum’s role in the broader ecosystem.[![](https://ethresear.ch/uploads/default/original/3X/b/4/b47175510ffd01083f026526f7562484b00f4c8d.png)564×500 360 KB](https://ethresear.ch/uploads/default/b47175510ffd01083f026526f7562484b00f4c8d)

## Why We Need Data-Driven Clarity

The hard truth is that it is a common misconception that today’s Ethereum L2s are effectively leveraging Ethereum’s capabilities. In reality, many underutilize or misuse Ethereum and fail to fully inherit its security guarantees. This isn’t about pointing fingers at L2s. It’s about recognizing the current limitations in Ethereum itself so that we can better track how far along on the roadmap we really are.

Sunlight is the best disinfectant. By measuring what’s actually happening rather than what we hope is happening, we can diagnose the core issues that need to be solved to enable Ethereum to become the settlement layer it was meant to be. The goal isn’t to “assess” L2s in a judgmental way, but to clearly understand utilization patterns that reveal where Ethereum itself is falling short.

The solution isn’t to force L2s to conform to an idealized model that doesn’t serve users well today. Instead, Ethereum needs to evolve to become a better settlement layer that L2s and users naturally want to leverage.

## The Reality Gap in L2 Ethereum Utilization

**[![](https://ethresear.ch/uploads/default/optimized/3X/c/b/cb62a9ff76bef46238a17e655357574d5a2d65aa_2_602x211.png)1600×561 251 KB](https://ethresear.ch/uploads/default/cb62a9ff76bef46238a17e655357574d5a2d65aa)**

If we look at L2Beat today, the metrics appear encouraging – strong TVS numbers across multiple chains, “green” security ratings for major L2s. Yet there’s a noticeable disconnect between these confident indicators and the community sentiment, which is far more cautious. This disparity exists because current metrics focus on theoretical security properties rather than actual usage patterns, and it paints an overly positive picture. Even Stage 2 rollups, while significantly more decentralized, still don’t achieve the original vision of full Ethereum security due to persistent Security Council powers.

Meanwhile, the roadmap has evolved to emphasize Native Rollups as a crucial next step, which acknowledges that current implementations don’t fully deliver on the original vision. The Ethereum Settlement Score (ESS) helps explain this sentiment gap by measuring what users are actually doing versus what the architecture theoretically enables. It shows that many users bypass Ethereum’s settlement guarantees through third-party bridges and external assets—pinpointing the problem areas of current L2 implementations.

These new metrics measure Ethereum utilisation, understanding that effective utilisation of Ethereum should be a conscious decision made by projects who are best served by Ethereum’s value proposition. It is a common misconception that today’s Ethereum L2s are effectively leveraging Ethereum’s capabilities. In reality, many underutilize or misuse Ethereum and fail to fully inherit its security guarantees. This underutilization is typically driven by the limitations of optimistic fault proofs, as well as constraints in Ethereum’s data availability throughput and latency.

By measuring what users are actually choosing rather than what we wish they were choosing, we can be honest about the tradeoffs users are making for better UX through technologies with different trust assumptions, and we can better focus on the most important work that brings us closer to truly trustless infrastructure.

As a community, we must recognize how profit-driven marketing psyops have led us astray, and it’s time to align behind a clear goal. Being truthful about the current shortcomings of L2s will allow Ethereum to regain credibility and articulate a common goal that will boost sentiment and defragment the community, so that Ethereum can achieve its original vision of a secure, censorship-resistant settlement layer that truly scales via L2s without compromising on its fundamental values—which is the very same founding vision that first inspired the growing ecosystem of builders, users and investors in the first place.

## Introducing the Ethereum Settlement Score (ESS)

We propose the Ethereum Settlement Score (ESS) to quantify the extent to which an L2 utilizes Ethereum’s canonical settlement. L2Beat provides TVS and Stages, but fails to account for asset settlement, when actually we need to combine these factors.

Stages alone do not define settlement. It’s more like a prerequisite to have a high stage to be able to unlock true Ethereum settlement at all, but you could still have a zero ESS at Stage 3 (defined below), if all assets on your rollup are non-canonical.

### How ESS Relates to L2Beat Stages

While ESS is a valuable metric at all [stages](https://medium.com/l2beat/introducing-stages-a-framework-to-evaluate-rollups-maturity-d290bb22befe) of L2 rollup maturity, true Ethereum settlement can only be achieved at Stage 2 or beyond. Even if an L2 uses exclusively canonical assets and bridges, the presence of multisigs or security councils means it’s not definitively secured by Ethereum—otherwise, why the multisig council?

We should measure ESS at all stages, but with clear understanding of what it represents:

- Stage 0-1 rollups: ESS measures hypothetical Ethereum settlement - what the scores could be if the rollup achieved Stage 2 or higher.
- Stage 2 rollups: Partial Ethereum settlement with limited Security Council intervention
- Stage 3 (Native Rollups): Full Ethereum settlement with no intermediate trust assumptions
- Stage 4 (UltraSound L2s - Based + Native Rollups with ESS Score of 1): The gold standard, combining both Native Rollup status AND Based Rollup properties for maximum Ethereum settlement and censorship resistance. This combination achieves both the UltraSound rollup definition and perfect ESS scoring.

The gold standard will be achieving both a high ESS score AND approaching Stage 4 status. This combination indicates both actual usage of Ethereum’s settlement layer AND the security model to properly leverage it.

## Recommended Initial Weights

| Factor | Weight | Rationale |
| --- | --- | --- |
| Censorship-Resistance (Force Inclusion) | 30% | Ethereum real-time force inclusion (i.e., Based Rollup) maintains Ethereum’s censorship resistance guarantees. Full score for Based Rollups with immediate force inclusion, decreasing linearly to zero for a 24h window. This is a critical component as censorship-resistance and liveness guarantees are core to Ethereum settlement. |
| Settlement (Proving) Latency | 20% | Real-time ZK proving provides maximum Ethereum settlement guarantees with minimal delay. |
| Canonical Asset Ratio | 20% | Major indicator of using Ethereum as the asset issuance and settlement layer for L2s. |
| Canonical Bridge Volume Ratio | 10% | Major indicator of using L2 trustless bridges as intended for L2 users to inherit Ethereum’s security also whilst in transit to or from L2s. |
| Canonical Bridge Addresses Ratio | 10% | Major indicator of using L2 trustless bridges as intended for L2 users to inherit Ethereum’s security also whilst in transit to or from L2s. |
| L2-Native vs External Asset Ratio | 10% | Penalizes heavy reliance on L2 natively minted assets because it goes even more against the spirit of using Ethereum as the asset issuance layer than External Assets, which include stablecoin issuance like USDC, where it’s arguably feasible to not use Ethereum for asset issuance. |

| Censorship-Resistance | Score (of 30%) | Example |
| --- | --- | --- |
| Real-time (Ethereum parity) | 30% | Based Rollups with atomic inclusion on the L1 |
| ≤ 1 hour | 28.75% | Rollups with short-window L1 inclusion guarantees |
| ≤ 6 hours | 22.5% | Medium-window L1 inclusion guarantees |
| ≤ 12 hours | 15% | Extended-window L1 inclusion |
| ≤ 24 hours (1 day) | 0% | 24+ hour L1 inclusion window |

### Settlement (State Proving/Verification) Latency Scoring with Examples

*Note: We’re measuring speed only, not proving costs. The assumption is that proving costs will be reasonably economical.*

|  |  |  |
| --- | --- | --- |
| Settlement Latency | Score (of 20%) | Example Tech |
| Real-time (instant ZK) | 20% | Future ZK Provers |
| ≤ 1 hour | 16% | ZK Provers: Succinct SP1, RISC0 |
| ≤ 6 hours | 14% | ZK Fraud Proofs: OP Succinct, RISC0 Kailula (high liveness risk) |
| ≤ 12 hours | 12% | ZK Fraud Proofs: OP Succinct, RISC0 Kailula (medium liveness risk) |
| ≤ 24 hours (1 day) | 10% | ZK Fraud Proofs: OP Succinct, RISC0 Kailula (low liveness risk) |
| 1 day to ≤ 7 days | Linear decay: 10% (1 day) → 0% (7 days) | Standard optimistic proofs (OP Stack, Arbitrum) |

### Stage-based ESS Penalties

| Rollup Stage | Penalty Applied | Why |
| --- | --- | --- |
| Stage 0-1 | 100% penalty | Settlement entirely hypothetical; no real Ethereum security. |
| Stage 2 | 50% penalty | Partial Ethereum security (due to multisigs/security councils). |
| Stage 3 (Native Rollups) | 0% penalty | Full Ethereum security inheritance (+ Based censorship-resistance parity); no penalty. |

## Final ESS Calculation

- 0 if Stage 0-1
- ESS × 0.5 if Stage 2
- ESS if Stage 3

The ESS is a much-needed update to bring real-world data into the L2 evaluation framework. The L2Beat stages are a nice start but paint an incorrectly positive picture without actual usage data. ESS adds critical nuance by exposing how users are actually interacting with these systems in practice rather than theory.

We encourage ESS measurements at all stages as it provides valuable insight into settlement patterns and helps teams understand their path toward true Ethereum alignment. However, only Stage 2+ rollups can claim any degree of actual Ethereum security inheritance, with Stage 4 Rollups representing the ideal memetic end state.

## Where Extra Visibility Is Needed

The current L2Beat framework provides excellent insights into the theoretical security properties of rollups. However, we should also clearly portray how users are actually interacting with these systems:

- Asset composition reveals important information about security models. This specifically refers to what assets users hold on the L2 and who is backing/securing these assets:

Canonical assets (e.g., ETH) originate on Ethereum, which serves as their primary ledger. These assets are moved into L2s via the canonical Ethereum bridge, preserving Ethereum as the source of truth.
- L2-native assets (e.g., ARB, OP, AERO, KAITO) are issued directly on the L2, which acts as their primary ledger. They are not bridged from Ethereum and do not rely on the Ethereum-side canonical bridge.
- External assets (e.g., USDC via CCTP or LayerZero OFTs) are issued and managed by external bridge protocols, with their primary ledger maintained off-chain or across multiple chains by the bridge itself. While L2Beat classifies mint-and-burn assets like Circle’s CCTP USDC and LayerZero OFTs as “Native”, we consider them “External” because the L2 does not serve as the authoritative source of truth and underlying backing for these assets.

**Bridge usage varies dramatically across L2s**. We should also be measuring the real percentage of assets that flow through canonical bridges versus other paths to show who is securing the asset whilst in transit. Additionally, we should inspect how many users are actually using the canonical bridges, to gauge Ethereum’s security benefits to the current-day end user.

Current metrics don’t place weights on the asset composition behind an L2’s TVS. A more comprehensive metric would help users understand not just what security a L2 could provide, but what settlement guarantees their assets actually have.

1. #### Canonical vs. Non-Canonical Assets

[![](https://ethresear.ch/uploads/default/optimized/3X/b/c/bc1fcc457e850d2fd7bcdc6962aa7d93ee6565a6_2_289x411.png)850×1208 33.7 KB](https://ethresear.ch/uploads/default/bc1fcc457e850d2fd7bcdc6962aa7d93ee6565a6)[![](https://ethresear.ch/uploads/default/optimized/3X/2/b/2b4621ce21d2fa53e03b753b03855441fa744224_2_290x411.png)850×1208 33.1 KB](https://ethresear.ch/uploads/default/2b4621ce21d2fa53e03b753b03855441fa744224)

Arbitrum: The pie chart shows that 28.0% of Arbitrum’s Total Value Secured (TVS) consists of canonical assets, 49.0% are external assets, and 23.0% are L2-native assets.

Base: Base shows a similar pattern with 26.5% canonical assets, 42.0% external assets, and 31.5% L2-native assets.

This comparison reveals that both networks have less than 40% of their value secured by Ethereum’s canonical bridges, with the majority residing in external bridges or natively issued on the L2 itself. Is the high proportion of native issuance a success case for L2s, as sovereign chains, but a departure from the original Ethereum scaling roadmap?

#### 2. L2-Native Assets

[![](https://ethresear.ch/uploads/default/optimized/3X/5/9/596abae239a1db5ff6688f179373450a246bf283_2_281x262.png)850×792 30.7 KB](https://ethresear.ch/uploads/default/596abae239a1db5ff6688f179373450a246bf283)[![](https://ethresear.ch/uploads/default/optimized/3X/f/3/f300ea5508735769990fcefdaa063507e5b63dc9_2_282x263.png)850×792 48 KB](https://ethresear.ch/uploads/default/f300ea5508735769990fcefdaa063507e5b63dc9)

*Base has a lively ecosystem of L2-native assets; the caveat is that L2-native tokens inherit none of Ethereum’s settlement guarantees*

Arbitrum: L2-native assets on Arbitrum are dominated by a single asset ($ARB, representing 93.5% of L2-native assets).

Base: Base shows a more diversified L2-native asset distribution with the largest asset representing 38.1%.

This highlights Base’s more diverse ecosystem of L2-native tokens compared to Arbitrum’s concentration in its governance token ARB.

#### 3. Canonical Bridge Assets

[![](https://ethresear.ch/uploads/default/optimized/3X/a/7/a79a55847080b4eb42dc785e23e720e9b6dfddbb_2_279x259.png)850×792 32.9 KB](https://ethresear.ch/uploads/default/a79a55847080b4eb42dc785e23e720e9b6dfddbb)[![](https://ethresear.ch/uploads/default/optimized/3X/b/9/b960d484e3b537c0a17867ce82aeaed19791d509_2_280x260.png)850×792 32.2 KB](https://ethresear.ch/uploads/default/b960d484e3b537c0a17867ce82aeaed19791d509)

Arbitrum: The canonical bridge on Arbitrum primarily holds ETH (23.7%), followed by Other (38.5%) and WBTC (27.4%).

Base: Base’s canonical bridge is heavily dominated by ETH (71.0%), with VIRTUAL in second place (19.9%).

Beyond ETH, are more assets set to abandon the canonical bridge in favor of external providers? WBTC already supports [LayerZero](https://medium.com/layerzero-ecosystem/layerzero-selected-as-official-interoperability-protocol-by-bitgo-for-wbtc-5f01f9fa7c61) and may soon follow in the footsteps of USDC and USDT, which migrated to external bridging standards like CCTP and LayerZero’s OFT framework.

#### 4. Transaction Volume by Bridge

####

Arbitrum: Only 10.0% of transaction volume is ETH flowing through the canonical bridge, while 90.0% uses external bridges.

Base: Base shows higher canonical bridge usage with 18.0% of volume, while 82.0% goes through external bridges.

If most transfers bypass the canonical bridge, can we still treat L2 canonical assets as truly “secured by Ethereum”—or are we just assuming trust based on how they’re held, not how they move?

#### 5. Bridge Users by Distinct Addresses

[![](https://ethresear.ch/uploads/default/optimized/3X/a/1/a1e1c9df65b32fd4734de1d7e09a010abdf1c5e2_2_258x240.png)850×792 31.6 KB](https://ethresear.ch/uploads/default/a1e1c9df65b32fd4734de1d7e09a010abdf1c5e2)[![](https://ethresear.ch/uploads/default/optimized/3X/6/5/65abd9f314f305e41f6f240b218ee442d0e20f7c_2_259x241.png)850×792 29.4 KB](https://ethresear.ch/uploads/default/65abd9f314f305e41f6f240b218ee442d0e20f7c)

Arbitrum: An overwhelming 99.7% of distinct addresses use external bridges on Arbitrum. Base: Similarly, 98.9% of users on Base rely on external bridges.

Despite architectural intentions, the vast majority of end users (>98%) on both networks rely on external bridges rather than the canonical one. This highlights a growing disconnect between how protocol teams design for security and how users actually move assets. If most users bypass the canonical bridge, can we still claim these assets inherit Ethereum’s security—or are we mistaking design assumptions for real-world guarantees?

## Key Insights from the Dashboard Comparison

- User Behavior vs. Protocol Actions: While 26-28% of TVS on both networks consists of canonical assets, less than 1.2% of unique addresses users actually interact with canonical bridges. This suggests institutional or protocol-level usage of canonical bridges rather than individual users.
- External Bridge Dominance: Compare the volume majority of external assets like USDC against the flow of canonical ETH. External bridges like Stargate, Across, and others handle the vast majority of transaction volume on both networks.
- Bridge User Preferences: For Arbitrum, external bridges like Hyperliquid (70.2% of external bridge volume), Stargate, and Across dominate. Looking at Base, volumes are similarly dominated by external bridges, with Stargate showing dominance (59.1%), followed by Mayan Swift.
- Asset Composition Differences: Base shows a substantial TVS in L2-native assets, which positions it as a competitive asset issuer that is opposed to Ethereum rather than a scaling solution for Ethereum-based assets. Arbitrum’s L2-native assets are highly concentrated in its ARB token.

## Understanding True Settlement Security: Who Controls Your Assets?

Our guiding question is **whether the canonical bridge is being used for Ethereum settlement**. Additionally, the question should be asked as to whether the canonical bridge is the best choice for some asset types.

Consider stablecoins like USDC, which represent a significant portion of TVS across many L2s. Although these tokens are classified by L2Beat as “[Natively Minted](https://l2beat.com/scaling/tvs),” The security of these assets doesn’t actually follow the L2’s security model – it follows Circle’s security model. These tokens are in truth “External assets” because they’re freely mintable/burnable by an issuing bridge (CCTP) at any time. Therefore, even when you hold the asset on the L2, you have neither security from Ethereum, nor from the L2 Sequencer, and instead from an off-chain ledger.

[![](https://ethresear.ch/uploads/default/optimized/3X/a/6/a6dc08334e111969dbe7ff613de31c8e18627a7e_2_276x290.png)850×896 62.2 KB](https://ethresear.ch/uploads/default/a6dc08334e111969dbe7ff613de31c8e18627a7e)[![](https://ethresear.ch/uploads/default/optimized/3X/0/f/0fe0a690f880e2a9b1e99f91b0d319ac9364d21c_2_314x290.png)850×792 53.7 KB](https://ethresear.ch/uploads/default/0fe0a690f880e2a9b1e99f91b0d319ac9364d21c)

*Compare the volume majority of external assets like USDC against the flow of canonical ETH*

This is fundamentally different from a canonical asset like ETH that you might receive via Across (notice that I didn’t say “via the canonical bridge,” because although essential to L2 asset security, these are rarely used by end users). While Across ETH is not secured by Ethereum during transit, once held by the user on the L2, it technically is secured by Ethereum again through the canonical bridge backing mechanism (i.e. fraud/zk proofs) .

Institutions like Circle choose to use their own servers rather than canonical bridges because of what it provides them with, and the widespread success of CCTP USDC adoption shows that most users are fine with these trust assumptions for the time being. We need better visibility into these preferences so we can evaluate whether this trend is temporary or represents a longer-term direction for certain asset types.

These more sovereign design decisions can be seen as a positive evolution. By recognizing that certain asset types may be better served by specialized bridging mechanisms, we can have a more honest conversation about security tradeoffs. A high ESS score isn’t necessarily “better” for all use cases—what matters is transparency about where security is derived from rather than pretending all L2 assets share the same security properties when they clearly don’t. Arguably, the ESS score derives even more meaning when it is measured on a per-asset basis and not as an aggregate for all L2 assets. However, for the purposes of this initial analysis, we only measure an L2’s aggregate Ethereum Settlement Score.

The asset issuer question applies to all asset types:

- Canonically bridged tokens (e.g., ETH): These tokens are locked in the canonical bridge on Ethereum L1, with their representations minted on the L2. They can theoretically inherit Ethereum’s full security guarantees by design, as their ultimate settlement remains on L1.
- External assets (e.g., Circle’s CCTP USDC, LayerZero OFTs): These tokens have their own independent ledger maintained by the external bridge provider. When you hold these assets on an L2, the balances are controlled by the external bridge, not by Ethereum or the L2. If the external bridge is compromised, these assets can be arbitrarily minted, burned, withdrawn or frozen regardless of L2 security. They do not derive security from Ethereum.
- L2-native tokens (e.g., ARB, OP, KAITO, AERO): These are secured by the L2 Sequencer. Their security model is independent of Ethereum, despite operating in its ecosystem.

Crucially, for the purposes of the Ethereum Settlement Score (ESS), the analysis focuses exclusively on the L2 infrastructure’s adherence to L2 rollup principles, not the underlying asset’s own security properties. The ESS evaluates how effectively an L2 preserves Ethereum’s intended security, trust assumptions, and economic guarantees, while minimizing the introduction of new risks at the L2 level, without factoring in the inherent risk profile of the bridged assets themselves.

Current L2 metrics show the total volume of assets on a rollup, but we need to zoom in one layer further to understand the true security guarantees for each asset class. Even for canonical assets, how users move them matters. Bridging canonical ETH via third-party bridges like [Across](https://www.gelato.network/blog/intent-based-bridging-for-seamless-ux-with-across-on-gelato-raa-s) or [LayerZero](https://www.gelato.network/blog/layer-zero-on-gelato-raa-s-omnichain-interop) rather than the official canonical bridge means those assets often aren’t secured by Ethereum during transit, even if they’re secured by Ethereum while users hold them on the L2.

## Interpreting the Ethereum Settlement Score

When evaluating an L2, we should look at asset composition with a focus on ETH and other Ethereum-native tokens. If a rollup has a good chunk of its TVS based on ETH (e.g., 10% or more) and the absolute number is also high (multiple millions in USD), then even a relatively low ESS would indicate a positive score because users at least have access to ETH secured by Ethereum’s canonical bridge, and because ETH clearly constitutes a significant portion of the rollup’s activity.

Different L2s have different design goals. An ESS helps make these distinctions transparent.

## ESS Tiers: What Different Scores Tell Us

### ESS of 1 (Stage 4 - The “UltraSound” Ethereum L2 meme)

This represents the ultimate, idealized L2 that achieves perfect Ethereum utilization. It combines Native Rollup and Based Rollup status and achieves an ESS score of 1. Censorship resistance is critical because it’s how we ensure we are actually leveraging Ethereum’s fundamental property as a credibly neutral platform. This demands real-time force inclusion to Ethereum (≤1 hour). Other Stage 4 qualifiers are instant ZK proving with minimal settlement latency, and 100% canonical asset ratio, 100% canonical bridge volume usage, and zero reliance on L2-native assets or external bridges. While technology constraints make Stage 4 aspirational today, it represents the technical endgame where an L2 achieves complete Ethereum settlement guarantees both architecturally and in practical usage.

### High ESS (0.7 - 0.99)

Strong alignment with Ethereum’s security model; users are actively utilizing Ethereum for settlement. A Stage 3 Rollup approaching Stage 4.

- Strong performance on Censorship-Resistance (25-30% of possible 30%) (≤1 hour force inclusion)
- Near real-time settlement with minimal latency (18-20% of possible 20%) (≤1 hour proving time)
- High canonical asset ratio (16-20% of possible 20%) (70-100% canonical assets)
- Strong canonical bridge usage (8-10% of possible 10%) (70-100% canonical volume)
- Low reliance on L2-native assets (8-10% of possible 10%) (0% L2-native assets)
- Stage 3 status: No penalty applied

**Example**: A Stage 3 ZK L2 rollup with 80% of TVS in canonical assets, like ETH.

**Open question**: Will a high ESS also translate into a high TVS? Only a tiny fraction of ETH has been moved from the L1 to L2s today. Is a high ESS the cure?

### Medium ESS (0.3-0.7)

Typically a Stage 3 rollup with less approach to Stage 4, or a high-scoring Stage 2.

This rollup still maintains meaningful connection to Ethereum’s security while pragmatically addressing UX needs through faster external bridges.

- Moderate performance on Censorship-Resistance (15-25% of possible 30%) (≤6-12 hour force inclusion)
- Some settlement latency (10-16% of possible 20%) (moderate proving time)
- Medium canonical asset ratio (10-15% of possible 20%) (50-70% canonical assets)
- Modest canonical bridge usage (5-8% of possible 10%) (50-70% canonical volume)
- Increased reliance on external assets (5-8% of possible 10%)
- L2-Native Asset Ratio: 5-7/10 points (30-50% L2-native assets)
- No stage penalty: Full score retained

**Example**: A Stage 3 optimistic L2 with 50% of TVS in canonical ETH, with the remainder using external bridges like Circle’s CCTP

**Open question**: Will all L2s become ZK rollups eventually, or will some remain optimistic?

### Low ESS (0.05 - 0.3)

Stage 2 L2s with varying weights and penalties. Still better than most L2s today as it requires at least Stage 2 status.

This rollup primarily uses alternative security models despite being technically connected to Ethereum.

- Low performance on Censorship-Resistance (5-15% of possible 30%) (≤24 hour)
- High settlement latency (0-10% of possible 20%) (standard optimistic fraud proving times)
- Low canonical asset ratio (5-10% of possible 20%) (25-50% canonical assets)
- Limited canonical bridge usage (1-5% of possible 10%) (10-50% canonical volume)
- High reliance on external or L2-native assets (1-5% of possible 10%) (10-30% canonical addresses)
- L2-Native Asset Ratio: 1-5/10 points (50-90% L2-native assets)
- 50% stage penalty applied

**Example**: A Stage 2 optimistic L2 where 80% of assets arrive via external bridges like CCTP, with minimal canonical ETH

**Open Question**: What about L2s with low Ethereum Settlement Scores that rely heavily on external bridges and L2-native tokens? If these external bridges never adopt Ethereum-native issuance—or if the L2 primarily serves its own ecosystem assets—then we must ask: is the Ethereum L2 label still meaningful, or does the overhead of an Ethereum-based L2 rollup architecture outweigh its benefits?

### Zero ESS: No Ethereum settlement

**Example**: A rollup that exclusively uses external bridges and native minting with no canonical assets

- This rollup operates as an Ethereum L2 in name only, with security entirely dependent on external bridges

**Open Question**: If none of the assets are actually settled through Ethereum, why maintain the architectural overhead of an Ethereum L2 canonical bridge and proof mechanism?

## The Tech We Have vs. The Tech We Want

### The Cross-Chain Bridge Market Maker Dynamic

In our current ecosystem, cross-chain bridge market makers (“solvers”) play a crucial role in providing a better user experience for bridging:

- They front assets to users for faster withdrawals
- They manage inventory across multiple chains
- They assume settlement risk in exchange for fees

This creates a dynamic where the theoretical security model of an L2 might suggest one architecture, while the practical experience for users (who often use market makers to bypass long challenge periods) suggests another.

These solutions have vastly improved UX, but do they depict the maturation of Ethereum according to the original vision, or are they to be regarded as a current solution until ZK happens? ESS scoring of L2 maturity accounts for this aspect via its canonical versus non-canonical volume weighting.

ZK technology can bring significant improvements to current providers like Stargate and Across by improving rebalancing efficiency and upgrading their verification to use cryptographic proofs instead of relying on optimistic challenge periods or multi-party verification. This creates a path where market makers can continue providing incredibly fast bridging UX while progressively removing trust assumptions.

### The ZK Future

ZK will be the endgame for Ethereum that improves Ethereum settlement UX, and it will be especially powerful when paired with Native Rollups and removing security councils.

However, affordable and fast ZK is not here yet. Let’s consider how the state of ZK affects settlement preferences. Addressing these questions would help us better assess the ecosystem as it actually operates today and might evolve tomorrow.

**If zero-knowledge proofs become instant, affordable, and widely deployed**:

Would external mint/burn asset issuers like Circle adopt Ethereum-based settlement due to risk/liability reduction and permissionless scaling potential, or would they maintain their own systems for regulatory or operational reasons?

Would mint/burn approaches that are one step removed from the asset issuer like LayerZero’s OFTs adopt ZK on these pathways? The likely answer is yes. However, this still leaves a fundamental issue: contagion risk from non-ZK networks like Solana within their ecosystem. Even with ZK verification, LayerZero’s cross-chain fungibility model means that security is limited by the weakest link.

External bridge providers like Circle and LayerZero face a dilemma with ZK adoption. While they could adopt Ethereum-based settlement for their assets on L2s when ZK technology matures, this would create inconsistency in their cross-chain asset management. These providers benefit from their mesh network asset fungibility across all chains, not just Ethereum’s ecosystem. Fragmenting their approach specifically for Ethereum L2s would introduce new costs and complexities that might not align with their broader business strategy, even if it would reduce their liability on Ethereum networks. L2 projects may eventually force this choice by lobbying for their own ESS-aligned canonical asset standard settings, but whether they will be able to compete with external providers, who might not prioritize Ethereum’s security model over their existing operational efficiency, remains to be seen.

One potential solution is a hybrid approach where Ethereum-based ZK L2s form a high-security cluster with instant transfers between them, while interactions with external networks require liquidity providers as intermediaries. This creates a security boundary around the Ethereum ecosystem.

Is it fair to say that external asset issuers like Circle are unlikely to prioritize Ethereum settlement over their broader cross-chain strategy? They benefit from maintaining consistent mint/burn functionality across all supported chains and would resist architecture changes that fragment their asset management approach, even if it would enhance security on Ethereum L2s.

How would cross-chain bridge market makers operate in a world of instant ZK? Would they still be needed, or would their role fundamentally change?

**What if ZK technology doesn’t meet expectations or takes longer than anticipated**?

It’s undeniable that the current 7-day challenge window in optimistic rollups is impractical. For active traders needing to quickly unwind positions, a 7-day delay would be catastrophic if the L2 operator has faults. For L2s competing for liquidity, this constraint effectively reduces the potential market size to scenarios where time-sensitivity isn’t critical. In our ESS scoring, settlement latency carries a high weighting of 20% because ultimately an L2 needs to be as close to Ethereum settlement time as possible for the ESS to correctly be applied. Real-time ZK proving is the only way to accomplish this. Real Ethereum L2s must go all-in on ZK, to become Ethereum again.

**Why Censorship-Resistance Matters (30% of ESS)**

In a world where ZK technology increasingly solves verification, the core value of decentralized smart contract platforms like Ethereum shifts to censorship resistance. This is the foundation for credibly neutral, permissionless financial infrastructure—and the defining promise of blockchains. While ZK enables a verifiable internet, it does not guarantee censorship resistance by default. The Ethereum Settlement Score reflects this distinction by assigning a 30% weight to censorship resistance, captured through force inclusion or based sequencing mechanisms.

Based Rollups represent the gold standard by achieving Ethereum-level force inclusion guarantees, but teams don’t need to adopt this approach to score well. A rollup with a 1-hour inclusion would still score respectably, opening the door for application-specific sequencing approaches while maintaining reasonable censorship-resistance.

While Stage 4 serves as an aspirational meme, it’s important to recognize that many highly valuable L2 use cases can exist at Stage 3, and even at Stage 2.

## Using ESS to Advance Ethereum’s Original Vision

As ZK technology matures to enable efficient proof verification at scale, we anticipate several shifts that ESS will help track:

- Native rollups will eliminate the need for security councils, governance tokens, and complex fraud proof games that currently serve as centralization vectors and security risks even in Stage 2 rollups
- Canonical bridges will become fast and practical with instant ZK-verified withdrawals, finally making them competitive with third-party solutions
- The progression from Stage 2 to Native Rollups (Stage 3) will represent the penultimate step in L2 maturity, where canonical assets can theoretically be truly secured by Ethereum without any intermediate trust assumptions

**Ethereum’s role will shift from a general-purpose computation platform competing for all use cases to a specialized security provider and asset issuance layer that exports its unique properties to connected Layer 2 systems**. This clarity becomes increasingly valuable as the ecosystem fragments into solutions with vastly different security properties, all falsely claiming an equivalent connection to Ethereum.

The ESS metric embodies the cypherpunk ethos that inspired Ethereum: transparency, verification over trust, and user sovereignty.

Ultimately, the path to making Ethereum great requires first acknowledging where we truly stand today. The ESS gives us that clarity, and with clarity comes the ability to focus our efforts on the innovations that will truly matter: ZK technology, Native Rollups, and Based infrastructure that makes Ethereum’s unparalleled censorship-resistance practically accessible to the entire ecosystem of L2s.

## Stage 4: The Final Form of Ethereum Rollups

[![](https://ethresear.ch/uploads/default/optimized/3X/f/3/f3ab012cd9d073b3945b8cd0216e347a1eeee62a_2_602x436.jpeg)1190×862 228 KB](https://ethresear.ch/uploads/default/f3ab012cd9d073b3945b8cd0216e347a1eeee62a)

What’s that? Another stage? Stage 4 represents the ultimate realization of Ethereum’s rollup vision: a fully decentralized, based and Ethereum-native rollup that achieves perfect alignment with the base layer.

Stage 4 represents the ultimate realization of Ethereum’s rollup vision: UltraSound L2s that combine Based and Native properties with perfect Ethereum alignment. These rollups achieve UltraSound status while demonstrating real-world usage that maximizes Ethereum security. To achieve Stage 4, a rollup must fully meet these requirements:

- Native Rollup Status (Stage 3): Complete elimination of all intermediate trust assumptions, including:

No security councils or multisigs with override powers
- Full state validation through Ethereum’s consensus
- Trustless canonical bridges with no admin keys

**Perfect ESS Score** (1): Maximum utilization of Ethereum’s settlement, consensus & DA layer, demonstrated by:

- Based Rollup Sequencing: Identical censorship-resistance (tx inclusion) guarantees as Ethereum L1
- Real-time ZK proving: Instant settlement with zero latency
- 100% canonical asset ratio: All assets originate from and settle on Ethereum
- 100% canonical bridge usage: Users exclusively rely on trustless Ethereum bridges
- 0% external or L2-native assets: No reliance on third-party issuers or local minting. All assets are issued on Ethereum and moved into the L2 via the canonical bridge.

A Stage 4 rollup achieves the original Ethereum rollup vision: it truly “is Ethereum” from a security perspective. Users experience instant, low-cost transactions while maintaining the full security and censorship-resistance guarantees of the Ethereum mainnet. No trade-offs, no compromises—just pure Ethereum security and censorship-resistance at scale.

This represents the hypothetical endgame where L2s become true extensions of Ethereum rather than adjacent ecosystems with varying trust assumptions.

## Practical Implementation

We’ve developed a public Dune dashboard that has the required inputs for the ESS formula from Arbitrum and Base. We welcome collaboration with the community to refine the methodology, weighting, and presentation to ensure it complements the existing framework while adding meaningful insight for users.

https://dune.com/gelatocloud/gelato-base-canonical-external/417a891c-bf39-48a1-b58b-2ed34da4f02a

https://dune.com/gelatocloud/gelato-arbitrum-one-canonical-external/90be0ede-9b3b-4cf0-a3a6-8b82e72a8ab2

**Key insights from our Arbitrum and Base ESS dashboard data:**

- External bridge dominance: The overwhelming majority of transaction volume goes through external bridges rather than the canonical bridge.
- Overwhelming user preference: >98% of distinct addresses use external bridges instead of the canonical bridge.
- Third-party bridge popularity: External Bridges like Stargate and Across, dominate bridge volumes, showing users’ clear preference for these faster alternatives over the canonical bridge.
- Hyperliquid: Arbitrum One’s TVS and volumes are mostly tied to Hyperliquid, which used Arbitrum One as a Settlement layer for its USDC collateral, which ironically makes Arbitrum One appear as more of a Settlement Layer than Ethereum.
- Asset composition concerns: While both Arbitrum One and Base have roughly one third of their TVS in their canonical Ethereum L2 bridge, the combined sum of external and L2-native assets still represents the majority of value on both L2s.

## Invitation for Discussion

We invite the community to join us in exploring these questions.

Truly secure, decentralized scaling is the holy grail that Ethereum has pursued since its inception. Native and Based rollups with ZK verification represent the clearest path to that destination—a world where users can enjoy increased throughput and lower costs without sacrificing security and censorship-resistance.

By tracking how effectively L2s utilize Ethereum’s settlement layer today, we create accountability and transparency that will drive progress toward this vision.

## Replies

**RogerPodacter** (2025-08-15):

Great post! Questions:

1. Why is the goal for an L2 to have 0% natively-issued assets? Consider users who enjoy minting cheap NFTs on an immutable based rollup. They certainly are “benefiting from Ethereum’s underlying properties.” Why discourage this use-case? Users minting on L2s might violate the “spirit” of the L1 being the hub for asset issuance, but shouldn’t enabling real users to securely accomplish their goals take precedence?
2. Why should a Stage 2 rollup that has a security council or multisig of any kind receive any ESS credit? Typical Stage 2 rollups rely on a 30 day exit window to protect users, and yet the efficacy of such an exit window has never been rigorously defended. I’d suggest the ESS not uncritically accept the idea that exit windows provide meaningful protection for users. I’ve written more on the topic here.

---

**gitpusha** (2025-08-19):

Hi [@RogerPodacter](/u/rogerpodacter),

Thanks a lot for engaging with my post — great question.

> Why is the goal for an L2 to have 0% natively-issued assets?

A couple of clarifications here:

- A Based & Immutable rollup is already Stage 3 in the ESS framework and likely would score quite high already if it has some canonical assets on it from Ethereum.
- The ESS = 1 (Stage 4) scenario — where all assets are issued on Ethereum — is more of an idealized end-point or thought experiment. It’s not meant as a strict prescription for every L2.

The motivation is that **higher-value use cases** (e.g. stablecoins, RWAs, high-liquidity tokens) gain the most from Ethereum-grade issuance and canonical bridges. For lighter use cases like minting cheap NFTs, the security/settlement guarantees of L1 issuance are arguably overkill — those rollups can still thrive while “accepting” a lower ESS.

So in short: ESS doesn’t discourage those use cases. Context matters. We need to make a distinction between **what really needs Ethereum settlement assurances** versus what can happily exist without it.

However, you raise an interesting point about asset issuance on Native Rollups. Are you saying that issuing assets on Native Rollups equates to issuing them on the L1 because the rollup STF is verified and run by the L1 itself? Tbh I havent thought about asset issuance on Native Rollups in that way. I could see how this could be classified as similar to canonical bridge asset issuance in the normal L2 context. But there’s still a difference because the Native Rollup single-sequencer might block your asset movement still, if you dont have a good force-inclusion mechanism. I suppose in a Native and Based rollup, asset issuance on the rollup itself is very similar to issuing the asset on the Ethereum World Ledger. Happy to discuss this further!

> Why should a Stage 2 rollup that has a security council or multisig of any kind receive any ESS credit?

I agree with your premise. Whether Stage 2 should incur a full penalty (ESS = 0) is debatable. One could argue Stage 3 — Native Rollups with no councils or multisigs — is the first stage that meaningfully deserves ESS credit.

