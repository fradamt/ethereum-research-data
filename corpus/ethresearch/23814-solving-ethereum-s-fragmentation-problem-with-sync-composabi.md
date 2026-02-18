---
source: ethresearch
topic_id: 23814
title: Solving Ethereum’s Fragmentation Problem With Sync Composability
author: alonmuroch
date: "2026-01-08"
category: Layer 2
tags: []
url: https://ethresear.ch/t/solving-ethereum-s-fragmentation-problem-with-sync-composability/23814
views: 442
likes: 4
posts_count: 3
---

# Solving Ethereum’s Fragmentation Problem With Sync Composability

*Special thanks to Jason Vranek, Josh Rudolf, Ellie Davidson, Drew Van der Werff, the **fabric team** and Friederike Ernst for helping in making this document*

The Ethereum community faces a critical choice: What is Ethereum? Is it merely the main chain (the L1), or is it the unified L1 plus all the dependent rollups and chains that rely on it for settlement? If it’s the latter, what do we need to do to reduce fragmentation and improve UX and DevX?

The answer to this question profoundly impacts our approach and ambition for true interoperability.

The [rollup-centric roadmap](https://ethereum-magicians.org/t/a-rollup-centric-ethereum-roadmap/4698) has successfully scaled Ethereum’s throughput at the cost of state fragmentation.

Today, transacting on Ethereum or its rollups feels similar, sharing wallets and developer tools largely due to common EVM compatibility. However, the experience of transacting *between* Ethereum and its rollups, or between the rollups themselves, is starkly fragmented.

**Current interoperability solutions focus narrowly on faster value transfer, a speed race that has already cut bridging times** from days (normal fraud proof exit times) to seconds (modern intent based solvers). While these solutions improve basic token transfers, the overall User Experience (UX) and Developer Experience (DevX) have suffered dramatically.

Three critical properties make EVM transactions powerful.

- Composability: A single transaction can execute multiple interactions or contract calls.
- Atomicity: All interactions within a transaction succeed or fail together—there is no partial execution.
- Synchronicity: All interactions occur within the scope of a single transaction and a single block.

These properties serve as the foundation that powered decentralized finance (DeFi), gave birth to decentralized stablecoins, launched the original DAO, and underpins modern rollup systems that build complex decentralized applications (dApps).

However, these properties do not hold in a cross-chain world. The fragmented Ethereum ecosystem has compromised the ability for developers to seamlessly make cross-chain composable transactions. We believe that unless this is solved, Ethereum will gradually lose its competitive edge and its powerful network effects.

We call for a unified Ethereum, and explain how **Synchronous Composability (SC)** is a viable path to achieve this.

# Current Interop Approaches

Multiple interoperability models have emerged in Ethereum’s multi-rollup environment. This comparison focuses on **intents**, **asynchronous message passing**, and the **Ethereum-Interop-Layer (EIL)**, evaluating them based on three key aspects: **execution mode**, **latency**, and **expressiveness**.

(see [previous](https://ethresear.ch/t/synchronous-composability-vs-intents-two-paths-to-ethereum-wide-interop/23426/7) discussions)

| Approach | Execution Mode | Latency | Composability |
| --- | --- | --- | --- |
| Intents | User specifies desired outcome; off‑chain solvers plan and execute steps; asynchronous. | Minimum one block plus solver confirmations; depends on network congestion and solver liquidity | Intents in of themselves are not composable, using AA we can pipe followup actions. Arbitrary contract-to-contract bi-direction calls are not supported, nor does atomicity. |
| Asynchronous message passing | Chains exchange messages via relayers/bridges; messages processed later; no shared execution. | Wait for source‑chain finality and for a relaying oracle; delays depend on each chain and can range from seconds to minutes. | Composability is possible but becomes impractical due to high latency and broken down steps; can deliver data or function calls, but no shared state; no atomic cross-chain state. |
| EIL | Account‑based interop; wallet signs once and sends direct calls to each chain; no intermediaries; supports multi chain transactions. | Similar to intent based interop | Supports multi‑call sequences at the account level; doesn’t support contract-to-contract bi-directional (stateful) calls. |

# True-Composability

Ethereum’s core strength lies in its ability to compose various dApps, which has fueled a decade of innovation. However, a significant gap exists between transactions that stay within a single EVM-compatible chain (intra-EVM) and those that span across different chains (inter-EVM). Currently, interoperability solutions function similarly whether they connect Ethereum and Base or Solana and Base.

To enhance the UX and DevX, and to secure a competitive edge for the broader Ethereum ecosystem against other chains, we urgently need an interoperability solution that minimizes this intra-EVM/inter-EVM disparity.

**True Composability Defined**

We define true composability as the capability to execute arbitrary, state-dependent, and bi-directional contract calls, all within a single transaction with guaranteed atomicity.

**The Crucial Importance of Composability**

Modern dApps are universally constructed from multiple interacting contracts. DeFi’s innovation hinges on the ability to combine protocols (like flash loans and trading) or optimize operations (like DEX routing). The current lack of cross-chain composability forces developers to repeatedly redeploy their dApps across different rollups.

Projects such as [Tempo](https://tempo.xyz/), [Arc](https://www.arc.network/), [Stablechain](https://www.stable.xyz/), and the [Canton network](https://www.canton.network/) serve as important cautionary examples. These projects opted to launch as Layer 1 (L1) solutions when they should have ideally been Layer 2 (L2)s. This choice was driven by two main factors: the necessary technical modifications (which were feasible as an L2) and the inherent difficulty of bootstrapping an L2, which is comparable to launching an L1 but without the benefit of composability.

This absence of true composability also hinders rollup innovation, making it exceptionally difficult to launch new rollups and effectively bootstrap a new ecosystem from scratch.

The lack of true composability stifles innovation, creates misaligned incentives, and gradually drains value away from the Ethereum ecosystem.

**The Existential Question for Ethereum**

What mechanism will prevent major rollups (such as Base, Arbitrum, or Robinhood) from eventually decoupling from Ethereum, or giants like Stripe and Circle from opting to become independent L1 chains ?

# Ethereum’s Single-Execution-Environment (eSEE)

[![Screenshot 2026-01-08 at 8.17.07](https://ethresear.ch/uploads/default/optimized/3X/0/2/023827fb9657a7e0481aa96b85668c1ee53b9118_2_467x499.png)Screenshot 2026-01-08 at 8.17.07854×914 34.8 KB](https://ethresear.ch/uploads/default/023827fb9657a7e0481aa96b85668c1ee53b9118)

**Ethereum Single Execution Environment (eSEE)**, builds on the idea of **Synchronous Composability (SC).** A model that has been actively researched over the last couple of years. Synchronous composability rethinks interoperability by allowing Ethereum and its connected rollups to behave as if they were part of one unified execution environment.

Unlike today’s cross-chain approaches, SC ensures that interactions across chains run as one atomic, deterministic, transaction-like flow. In other words, eSEE takes the guarantees we expect from a normal EVM transaction and extends them across multiple EVM environments, not just within a single chain.

SC has 3 main desired properties:

- Composability
Applications can interact across rollups as if they were on one chain. Developers can write cross-domain logic and DeFi strategies that feel no different from local contract calls
- Atomicity
Cross-chain interactions behave like a single transaction. All operations across L1, L2s, and appchains either succeed together or revert together, ensuring there are no partial or inconsistent outcomes.
- Synchronicity
Cross-chain calls are ordered and executed within the same transactional flow. A shared coordination layer keeps all domains in lockstep, allowing contracts to act on remote chains and immediately use the results.

Key R&D promoting SC:

- Espresso Systems (CIRC)
- Fabric (SCOPE)
- Compose (Shared-Publisher)
- Puffer (Unifi Signal Service)
- Spire (based L3 composability)
- Ultra transactions (Taiko)

### Benefits

Inspiring to reach eSEE through SC we improve significant parts of Ethereum’s UX, enabling developers to do more and innovate without borders. Users will feel as if they never left the L1, no matter on which chain they are on.

We believe this will create competitive advantage like no other, symbiotic with the [business model behind rollups](https://alonmuroch-65570.medium.com/ethereums-mcdonald-s-moment-how-rollups-became-the-franchise-model-of-web3-145fc8e0b359).

| Benefit | Today | With SC |
| --- | --- | --- |
| Instant UX State can be read from and written to a different chain (e.g., Chain B) synchronously within the same execution cycle of a call originating on Chain A | A user has funds on chain A, but wants to transact on chain B, is forced to bridge, then transact and then bridge back. This whole process feels fragmented, with significant latency and the UX is very different than the L1 | Funds on chain A are bridged (with no intermediaries), transacted on chain B and returned to chain A. All in a single (instant) transaction with a UX that “feels” like the L1 |
| Atomic Flows Execution is all-or-nothing, preventing partial transactions, race conditions, and frustrating “message pending” delays | With current interop approaches there is no guarantee of execution or atomicity. A User transacting across chains will break down each step individually, the next step is not guaranteed to execute. | All steps can be expressed in a single transaction, atomic execution is guaranteed. Either all steps execute correctly or none of them. |
| Singleton dApp deployments A decentralized application only needs a single deployment and can be utilized from any connected chain, avoiding 30 fragmented deployments | Developers are forced to deploy their dApps to every chain they want presence on, fragmenting their TVL and user base. | Contract-to-contract interactions are sync and atomic, exactly like on Ethereum. Any user on any connected chain can interact with the dApp, regardless of where their assets sit.  Devs can deploy their contract once, enabling all users to interact with (no bridging required) |
| Dev Composability Developers can use, compose and interact with dApps within their EVM and across chains in a similar manner. Without changing their contract architecture | Contracts are strictly built for sync composability (intra EVM). Current interop approaches support async calls at most, severely restricting what’s possible. | Complete bi-direction (and stateful) arbitrary read/ write calls between contracts (intra and inter EVM) |
| Unified Liquidity Capital can reside on one chain while the dApps operate on another, all without compromising the user experience | Liquidity is fragmented across different rollups for both dApps and users. | Users and dApps can consolidate their liquidity into a single chain as it doesn’t impact their ability to interact with other dApps/ users on connected chains |

### Reaching eSEE

We suggest focusing on those 3 pillars as a way to direct more resources (by the EF and the greater community) and attention to achieving eSEE through SC:

- Fast Finality: We must push for faster finality across the entire ecosystem. Faster finality reduces reorg windows and delivers a superior user experience (e.g., faster and more predictable L2-to-L1 withdrawals). It is also critical for synchronous composability (SC): rollups that compose synchronously must settle together, which means settlement must occur frequently to avoid inheriting long reorg and settlement delays. Waiting hours to settle two synchronously composable rollups effectively forces both to inherit that delay, making co-dependency less appealing. Achieving fast finality requires faster settlement on the rollup side (via ZK technology) and continued progress on Ethereum’s side through SSF (Single Slot Finality), 3SF (Three-Slot Finality), and shorter slot times.
- Research & Standardization: The incredible innovation from SC research must now transition to formal development. We must prioritize formal, EF-led research and standardize the core aspects of SC (message passing, coordination, atomicity, composability, and limitations). The goal is to move SC from a researched concept to a mature, engineered, and optimized solution.
- Adoption: The Community Mandate: As with any solution of this magnitude, adoption is the ultimate key. This phase is critical and follows the first two steps. Building community-wide consensus on the necessity of faster finality and SC standardization is the lever that will drive adoption at the highest levels—from developers and users to wallets and major infrastructure providers.

**The Ethereum Single Execution Environment is a movement to unify the fragmented rollup ecosystem by collectively pushing for synchronous composability.**

## Replies

**Citrullin** (2026-01-12):

Your comparison chart lacks of another, very important, metric for users. The fee structure.

The delay may be acceptable, if you benefit in terms of fees. It seems Intents profit at both fronts rn.

Haven’t tried it yet. Please correct me, if my intel is wrong.

From a physical business user perspective, I see a future where multiple options are to be desired. Especially when you have to work with L3s eventually. Where the delay might be something you want to bypass. Based and Native Rollups seem to me the only way to move forward in the long run. Especially Based Rollups are quite attractive for appchains.

Even with all these optimizations, there will always be a limit at some point.

Cutting off a specific economic environment, or industry, makes a lot of sense.

Not really a new idea to begin with. Cosmos failed at it, and so did many others.

There is no need to transact on main, when the whole industry transacts mostly between each other. The cocoa industry gets their own, so does the toy industry.

And the chemical company, the injection molding company, the supplier and the retailer all engage on this chain, mostly. Once in a while moving contracts/tokens/whatever around over ultra transactions or whatever it will be.

My personal bias at the moment goes heavily in favour of Taiko and in extension Surge(Nethermind). Spire Labs has yet to provide a solution like Surge does.

Not to mention ENS working on switching to Surge too.

There is, of course, the whole TEE and GPU topic.

Which is quite the bottleneck in terms of hardware, but that’s another topic for another day.

Observing and helping ENS here is probably going to be interesting.

Last time I checked Spire Labs, they were also heavily favouring L3 development on Base etc.

Which increases the risk of the attack scenario you mentioned.

I do understand it from a business perspective though. It’s still a risky mentality to have.

Coinbase Venture probably pressured them to use their Base chain.

The technology in the Ethereum ecosystem is pretty close to being usable in the real world.

Which is about time after a decade. With that in mind, we have to change culture here.

Away from this ponzi exploitation mentality towards actual economic use.

In order to not always keep repeating the mistakes Spire Labs is doing with Coinbase right now.

We REALLY have to also consider the sustainable business model here to finance it.

You can only sell hope and dreams for so long. At some point you have to deliver.

Or this whole thing will go under in smokes and mirrors.

That’s why I didn’t even consider Puffer at all. The are focusing on restaking after all.

It’s a temporary solution to the lack of deployment opportunities for capital in this industry.

So, from my physical economy perspective, I wouldn’t take their perspective into account at all. At the end of the day, it’s just a way to make number go up, nothing more.

---

**alonmuroch** (2026-01-14):

With SC you can have near zero fee for bridging … it’s literally just messages burning and minting tokens (atomicity is required)

