---
source: ethresearch
topic_id: 23669
title: An Observation on Ethereum’s Blockspace Market
author: kubimens
date: "2025-12-16"
category: Proof-of-Stake > Block proposer
tags: [mev, proposer-builder-separation, censorship-resistance]
url: https://ethresear.ch/t/an-observation-on-ethereum-s-blockspace-market/23669
views: 1117
likes: 21
posts_count: 5
---

# An Observation on Ethereum’s Blockspace Market

# An Observation on Ethereum’s Blockspace Market

Co-authored by [Kubi M.](https://x.com/kubimensah)([Gattaca](https://x.com/gattacahq) / [Titan Builder](https://x.com/titanbuilderxyz)), [Alex T.](https://x.com/alextes) ([Ultrasound Relay](https://x.com/ultrasoundrelay)),  [Kevin L.](https://x.com/lepsoe) ([ETHGas](https://x.com/ethgasofficial)), and [Justin D.](https://x.com/drakefjustin) ([Ethereum Foundation](https://x.com/ethereumfndn)).

Special thanks to [Drew V.](https://x.com/DrewVdW) ([Commit-Boost](https://x.com/Commit_Boost)), [Michael M](https://x.com/mostlyblocks), [Thomas T.](https://x.com/soispoke) ([EF)](https://x.com/ethereumfndn), [Ladislaus v D.](https://x.com/ladislaus0x) ([EF](https://x.com/ethereumfndn)), [Jason V.](https://x.com/jasnoodle) ([Fabric](https://x.com/Fabric_ethereum)), [Ben H.](https://x.com/philosowrapter)([BTCS](https://x.com/NasdaqBTCS)), [Quasar Builder](https://x.com/QuasarBuilder), [Sebastien R.](https://x.com/aimxhaisse) ([Kiln](https://x.com/Kiln_finance)), [Ben T.](https://x.com/builder_benny) ([Figment](https://x.com/Figment_io)), [Murat](https://x.com/MuratLite) ([Primev](https://x.com/primev_xyz)), [0xprincess](https://x.com/0x9212ce55) ([Nuconstruct](https://x.com/nuconstruct)), [Sam J.](https://x.com/macrosam) (EMF) and [Matt C.](https://x.com/mcutler) ([Blocknative](https://x.com/Blocknative)) for the comments and review.

Ethereum’s core business is the production and sale of blockspace: the scarce commodity of verifiable compute and data storage. Through economic security, geographic decentralisation, and client diversity, **Ethereum produces the highest-grade blockspace available today**. How that blockspace is priced, allocated, exchanged, and consumed directly determines user experience and impacts the overall utility the protocol provides.

Consumers of blockspace span a wide range of users, including those who utilize smart contracts powering applications such as exchanges and lending markets, rollups that settle batched transactions and rely on data availability, and stablecoin issuers enabling global payments. While there are countless other use cases, each has heterogeneous demands that must be optimally serviced to maximise the utility Ethereum provides.

By staking capital and performing core protocol duties (attesting and proposing), validators earn fees and collectively produce blockspace (supply); users originate transactions and pay fees (demand); and various infrastructure providers enable price discovery, allocation, and exchange of blockspace. The interaction among these three classes of stakeholders constitutes the microstructure of Ethereum’s blockspace market.

Over the last decade, Ethereum’s blockspace market has undergone substantial evolution, shaped by hard forks and ongoing developments. Today, over 90% of blockspace is sold through this microstructure, which is broadly referred to as Proposer-Builder Separation (PBS). PBS has successfully preserved the decentralisation of Ethereum’s validators by allowing the **Proposer (**proposer and validator are used interchangeably below) to outsource block construction, the computationally intensive allocation of blockspace, to specialised **Builders**, with wholesale auctions coordinated by **Relays**.

While PBS is robust, challenges remain with today’s blockspace market structure.

There are several ongoing efforts to improve the current market structure: [BuilderNet](https://buildernet.org/) uses TEEs to reduce trust assumptions and enable shared order flow; [ETHGas](https://www.ethgas.com/) explores crypto-economically backed preconfirmations and futures to price inclusion risk and smooth fees; [mev-commit](https://docs.primev.xyz/v1.1.0/concepts/what-is-mev-commit)  develops preconfirmations and block positioning bids for inclusion; [TOOL](https://docs.nuconstruct.xyz/s/212d8a9e-66f5-41cf-bfb8-dff38edd691f) targets subslot-driven early execution confirmations with an open collaborative environment; and other experiments are underway.

**This post is a call for continued community engagement to push boundaries, evolve the current market structure, and address emerging challenges.** It focuses on today’s issues, but is merely a starting point. Follow-ups and working sessions will prioritise the problems across *economics*, *robustness*, *performance*, and *services,* and begin delivering solutions. We conclude by outlining a set of principles to guide and evaluate solutions. To keep scope clear, the focus is the out-of-protocol market for blockspace: how it is priced, allocated, exchanged, and consumed, and how these choices impact the protocol’s overall utility. In-protocol production of blockspace and consensus mechanics are treated as assumed context rather than subjects of analysis.

## Unpacking the State of Today’s Blockspace Market

The out-of-protocol PBS implementation [MEV-Boost](https://ethresear.ch/t/mev-boost-merge-ready-flashbots-architecture/11177) successfully alleviated some centralisation pressures on the core protocol. Despite that progress, existing challenges persist, and new ones are emerging. We categorise these challenges across four core areas: Economics, Robustness, Performance, and Services.

### Economics

Key challenges in the current market structure revolve around incentives for transaction originators, relays, and builders.

#### Price Discovery and Misaligned Incentives

One key challenge is fair price discovery for blockspace access and the inherent tension between producers and consumers: producers want to maximise revenue from selling blockspace, while consumers want to minimise what they pay. Today, price discovery occurs via a sequence of auctions. Users send transactions to order flow auctions (“OFAs”) and builders with fee payments to express priority access to specific state. Builders, after allocating blockspace based on desired state access and fee payments, participate in a whole-block auction hosted by the relay to wholesale buy blockspace (the entire block per slot). Because state access cannot be precisely priced, originators tend to overpay to guarantee inclusion and priority. They are further incentivised to send their order flow to a single builder: if they send to multiple builders, the aggregated priority fees are competed away during the relay auction. By sending exclusively, the builder can retain some of the priority fees instead of passing all of it to the validator and can refund a portion of the retained fees to the originator. Overall, exclusive transactions may account for up to 84% of the total fees paid in winning blocks (see [Andrea](https://arxiv.org/abs/2509.16052) (COW) and [Thomas](https://ethresear.ch/t/empirical-analysis-of-builders-behavioral-profiles-bbps/16327) (EF)). The originator’s effective fee is therefore the total priority fees paid minus any refund received. This is an inefficient price discovery process with multiple negative second-order effects, some of which will be discussed in the following sections.

#### Reduced Blockspace Revenue and Inefficient Blockspace Allocation

A second-order effect of the aforementioned inefficient price discovery process is fragmented access to transactions across builders. Not all transactions can be included in a given block, so the winning builder allocates blockspace from a partial view. Unobserved transactions will spill into later slots, [increasing time-to-inclusion and raising inclusion cost](https://arxiv.org/abs/2506.04940). Further, due to the builder not being aware of the transaction, there is suboptimal blockspace utilisation that leaves priority fees and execution surplus uncollected, reducing the realised blockspace revenue for the slot and, in aggregate, lowering overall revenue. In summary, users experience inclusion degradation and validators receive lower block rewards.

#### The Wrong Participants May Bear Volatility and Uncertainty Risk

In-slot auctions excel at capturing last-minute and state-dependent value, while forward markets may be better suited for managing risk within the pipeline–expressing sustained demand, hedging volatility, or predictable latency. A robust market design may require both components working together rather than relying solely on the in-slot mechanism.

Further, current designs push risk to the end-users. An open question is whether part of this risk should instead be transferred to specialized actors, blockspace wholesalers, or liquidity providers who actively manage demand through standardized blockspace futures. Such financial instruments could allow users and applications to hedge execution risk more efficiently, reducing volatility shocks. These [mechanisms](https://frontier.tech/ethereums-blockspace-future) are common across most markets and have been studied for decades as effective tools.

#### Lack of Economic Incentives for Key Actors

In the current PBS design, there is a fair exchange challenge between the builders and validators. For this reason, Relays were introduced to perform critical functions: they solve the fair-exchange problem between builders and validators by acting as a trusted counterparty, lower the barrier to entry for builders, and run the computationally heavy whole-block auction so validators can remain lightweight and unsophisticated.

Relays, however, have no established incentives. The protocol does not compensate relay operations, requiring them to effectively function as public goods sustained by donations or by looking to extract value elsewhere (see below). The result is economic fragility and a degraded Ethereum, examples include: relay shutdowns *that reduce* the active set to only a handful of operators, underinvestment in performance and robustness, increased concentration risk and correlated failures, weaker geographic and network coverage with higher latency variance, and slower iterations on monitoring and transparency.

In response, some relays have introduced monetisation to remain viable, for example, by adding a subscription fee or by adding a fee on transactions (e.g., bid-adjustments). These tactics prioritise relay revenue over maximal blockspace utilisation, further complicate price discovery, and erode robustness (e.g., the fee charging relay optimizes its fee relative to the bid, not the true block value).

Last, we note there are some proposals, such as ePBS, that remove the trust function of the relay. However, when the current relay market is observed, trust is a given requirement, not what drives the adoption of relays. Trust relationships can enhance efficiency, but must be grounded in a competitive market that rewards performance. Relays with adoption now offer highly functional services such as delaying and canceling bids, or aiding in price discovery.

### Robustness

Ethereum’s core protocol has unmatched liveness guarantees, producing high-grade blockspace. That robustness only holds end-to-end if out-of-protocol consumption paths (currently the PBS transaction pipeline) uphold comparable guarantees. A more diverse and decentralised operator set would mitigate many issues; however, these roles are resource-intensive and exhibit winner-take-most economics. In our view, the best path forward is to embrace this fundamental dynamic whilst preserving decentralised properties. Novel approaches are required. We focus on three properties: liveness, fair access (to inclusion guarantees), and proposer agency.

#### Liveness

Robustness here is intended as continuous consumption of blockspace with service continuity comparable to in-protocol production. Winner-take-most dynamics and the per-slot validator monopoly concentrate blockspace allocation and auctioning in a small operator set. Further, fragile relay economics shrink participation. Notwithstanding, technical efforts and order flow network effects increase barriers to entry. This concentration raises correlated-failure risk, including: client and implementation monocultures (e.g., around Reth or Intel TDX), shared infrastructure and data-center outages, network incidents, and jurisdictional (regulatory pressures, forced shutdowns, or otherwise). Last, when a dominant operator loses the block auction, order flow tied to that operator faces delayed inclusion and disruption. Key characteristics of any designs we believe must still preserve scale advantages while reducing single-operator criticality and making broad, diverse participation feasible.

#### Fair Access

Robustness also depends on non-discriminatory, censorship-resistant access to blockspace. High uptime is insufficient if access is gated or transactions are censored (in the wake of the merge, up to [78%](https://www.mevwatch.info/) of blocks were censored for a period of time).  [Inclusion lists](https://eips.ethereum.org/EIPS/eip-7805) and related mechanisms improve guarantees for public-mempool transactions without privacy needs. Gaps remain for originators with privacy requirements, such as DeFi users, who cannot use the public mempool, and for transactions that execute against contended state. Without finding a path for fair-access guarantees for private transactions (e.g., transactions that do not fit neatly within inclusion lists via mechanisms such as [block merging](https://ethresear.ch/t/relay-block-merging-boosting-value-censorship-resistance/22592)), availability becomes conditional and impacts user experience, and more importantly, the overall robustness of Ethereum is degraded.

### Trustlessness

The blockspace market should follow transparent rules that can be enforced without placing trust in any particular party. While discretionary trust can increase efficiency, it should not be necessary or assumed as the default state. Specifically, the inclusion of transactions must verifiably comply with fair access principles, and transactions must not be exposed to undue information leakage in-flight. Today, enforcement is largely reputational, and while builder and relay misbehavior can carry penalties (i.e., a reduction in transaction flow), this dynamic favours established participants and can therefore lead to centralization.

Mechanisms and technologies that can minimize trust such as economic and consensus based systems or TEE’s, MPC and FHE should be leveraged where appropriate.

#### Proposer Agency

One of Ethereum’s greatest features supporting robustness is its diverse validator set. As part of this, it is critical that blockspace proposers remain lightweight while retaining effective control over how blockspace is allocated and accessed. Resource-intensive tasks can be outsourced to specialised entities, but proposers must keep agency: the ability to select and rotate providers, enforce allocation and sequencing policies, monitor censorship, and recover safely when delegates fail.

Without this control, out-of-protocol consumption can diverge from the protocol’s neutrality and reliability, embedding dependencies that overtime increase switching costs. This results in slower recoveries if or when something does go wrong. Proposed Ethereum protocol upgrades like FOCIL address censorship and give proposers more control, while [Attester-Proposer Separation (“APS”)](https://www.youtube.com/watch?v=IrJz4GZW-VM)  cleanly decouple validators from the transaction pipeline, but timelines are unclear.

### Performance

Performance should be a first-order requirement of Ethereum’s blockspace market. It determines whether latency-sensitive applications can exist, sets the ceiling on how much can be processed in a given time constraint, and drives the user cost of certainty: when inclusion is slow or volatile, users overpay to hedge uncertainty, blockspace goes underutilised, and overall economic value decreases.

We should aim to embrace high-performance specialisation whilst preserving decentralised properties; mechanisms must bound proximity rents (e.g., colocation edge must be capped), keep providers replaceable, and avoid degrading overall protocol utility.

#### Hot Path Latency

The hot path is transaction originator → block construction and allocation → whole block auction → validator signature (commitment to the block) → network propagation to the attestation committee.

Today, queuing and scheduling on this path are implicit. Order flow waits in venue-specific backlogs before being allocated; builders keep accepting and reshuffling transactions until the slot deadline, with no public cut-off time or priority rules, so late arrivals are unpredictably dropped or pushed to the next slot; signature dispatch (e.g., committing to the header and signing) competes with other validator duties; propagation then inherits network jitter as does communication at every hop of this communication chain. The result is long-tail latency and unstable time-to-inclusion that users price in with higher fees.

Further, to evaluate improvements in sequencing infrastructure, there should be more explicit Service-Level Objectives - for example, p95 and p99 time-to-inclusion, maximum tolerable backlog under burst load, or guaranteed latency windows for preconfirmed transactions. Establishing measurable goals would allow protocol designers and market participants to understand and compare performance tradeoffs.

#### Capacity Management

Throughput must remain stable under bursty demand, including rollup data-availability spikes. Without explicit intake policies for transactions and data blobs, bursts propagate through block construction, the relay auction, proposer signature dispatch, and block propagation, turning short spikes into multi-slot delays.

Improving capacity management requires explicit slot budgets: for example, accept new bundles only until t_slot − δ and publish intake queue depth, drain rate, and the next eligible slot so wallets and rollups can pace. Explicit, observable intake budgets prevent burst cascades, stabilise tail latency, and preserve broad inclusion.

#### Portability Without Proximity Lock-In

High performance cannot require permanent colocation at a few facilities. Designs should bound persistent proximity advantage (e.g., with timing windows and rotation), make routing and measurement portable across venues, and keep operators substitutable without bespoke integrations. Competitive edge should come from measurable service quality, not geography.

### Services

Services are a core layer of the blockspace market. A market structure that preserves core properties, aligns incentives, and delivers performance must also foster permissionless innovation, allowing new teams to improve how blockspace is consumed through features such as preconfirmations and inclusion guarantees backed by economics. Today, out-of-protocol intermediaries gate service creation, stifling innovation, degrading user experience, and decreasing network value. The goal is an open, programmable, and verifiable services layer that remains compatible with the economic, robustness, and performance constraints outlined above.

#### Openness and Programmability

In the current out-of-protocol design, builders and relays act as gatekeepers. Teams must persuade these intermediaries to support any new service, rather than exposing a formal interface where services can be expressed directly. This concentrates decision power, raises integration costs, and lengthens feedback cycles. A healthier market exposes standard, neutral interfaces for defining and discovering services, so originators, wallets, and applications can request specific behaviours and providers can compete to fulfil them. Examples include preconfirmations, priority inclusion guarantees, fixed-fee lanes, and intent execution policies. Formalising these primitives at the market edge, rather than negotiating them bilaterally with a single allocation or auction venue, increases experimentation without sacrificing safety.

Further, when PBS first started, there was not a robust L2 community. Now that this is flourishing and helping scale Ethereum, this pipeline must find ways to offer services to provide things like composability (both synchronous and asynchronous) and work to provide services that specifically meet their needs and pain points (i.e., faster L1 confirmation times). Last, as services become broadly adopted, we should work to improve and standardize these services (similar to the broader transaction flow).

#### Verifiable Guarantees and User Experience

Like any service, the offering and product features must be credible. With ad hoc arrangements amongst validators, relays or builders, the network is left with unenforceable guarantees around censorship resistance, inclusion priority, latency classes, or cost predictability. Services need portable semantics and more measurable or ideally verifiable outcomes. For example, economically backed preconfirmations with clear fault handling and refunds or inclusion guarantees with measurable deadlines. Another example is pricing instruments such as forwards or futures that help hedge gas costs across time. With shared definitions and proofs of delivery, wallets and applications can rely on these services across providers.

#### Portability and Competition

Service quality should be determined by performance and accountability, not by exclusive relationships. Today, vendor lock-in and bespoke integrations with specific block construction or wholesale auction venues limit portability and entrench intermediaries. A services layer that is discoverable across venues, with open and consistent interfaces, lets originators switch providers with low integration costs, and lets blockspace producers adopt or sunset offerings without hard coupling. Competition then shifts to measurable metrics such as latency and refund accuracy, improving allocation efficiency and time to inclusion.

The target is a services market that lowers barriers to entry, encourages rapid iteration, and allows blockspace producers to credibly offer specialised properties while preserving neutrality. By making services open, programmable, verifiable, and portable, the blockspace market can evolve without sacrificing decentralization.

## Principles to Improve Ethereum’s Blockspace Market

This section aims to outline principles that can guide the evolution of Ethereum’s blockspace market. Proposals should enhance price discovery and blockspace allocation efficiency, and make incentives for key out‑of‑protocol infrastructure providers explicit and sustainable; strengthen robustness and liveness, preserve client and geographic diversity, and keep validators lightweight while retaining oversight and safe failover paths; deliver predictable performance without proximity lock‑in; and support an open, verifiable, portable services layer. Changes must be incrementally deployable, reversible, and observable with clear accountability. The objective is to increase the utility of Ethereum’s blockspace while preserving the protocol’s credible neutrality and decentralization.

1. Transparent price discovery and efficient allocation
Blockspace pricing maps to specified state access; overpayment is minimised. Allocation raises utilisation and improves time‑to‑inclusion, increasing realised revenue.
2. End‑to‑end robustness and liveness parity
Blockspace consumption paths meet production‑level continuity; correlated‑failure risk is reduced; client and geographic diversity are preserved; failures are isolated, and recovery is fast.
3. Fair access, censorship resistance and privacy
Access must be non‑discriminatory across public and private order flow, including contentious state, with inclusion guarantees portable across venues. Designs should minimise information leakage and asymmetric visibility by favouring privacy-preserving order flow and execution.
4. Sustainable incentives for key actors
Key market infrastructure providers have explicit, durable economics that do not distort neutrality or price discovery and do not depend on public‑good funding.
5. Proposer agency with lightweight validation
Validators remain lightweight while retaining policy control, provider rotation, and safe failover, avoiding hard dependencies on any single intermediary.
6. Hot‑path latency and capacity discipline
Queuing, admission, and deadlines along the transaction pipeline are explicit. Intake is a bounded resource with published capacity signals; overload is handled predictably and fairly to prevent multi-slot cascades, and inclusion timing is stable.
7. Portability without proximity lock‑in
Persistent proximity rents are bounded; multi‑client, multi‑region participation remains viable.
8. Open, programmable, portable services with verifiable guarantees
Neutral interfaces expose services; semantics are standard and auditable; switching costs are low, so competition centers on measurable QoS rather than exclusive relationships; and clear data pipelines to measure metrics are established.
9. Observability, accountability, and incremental deployment
Operators publish metrics and proofs sufficient for independent verification and attribution. Changes are staged, reversible, and measurable, with clear responsibility for faults. Observability may help inform Ethereum protocol upgrades.
10. Governance of critical infrastructure
Governance must be explicit, accountable, and capture-resistant. Define roles and upgrade paths across critical infrastructure, with features such as no single-institution veto.

## Conclusion

Ethereum produces high-grade blockspace; the out-of-protocol market now determines how much of that value is realised. PBS preserved validator neutrality but left structural gaps in pricing, incentives, concentration, latency, and service openness. This post mapped those gaps across economics, robustness, performance, and services, and set principles for addressing them.

The path forward are mechanisms that embrace high-performance specialisation while preserving decentralised properties, align incentives end-to-end, make guarantees portable and verifiable, and iterate with incremental, observable changes. We look forward to further discussions and working towards solutions. These principles have the potential to increase realised blockspace value without compromising Ethereum’s credible neutrality.

## Replies

**DrewVanderWerff** (2025-12-16):

Looking forward to finding solutions for these challenges.

---

**antonydenyer** (2025-12-16):

Is it time to admit that, as a mechanism, 1559 does NOT facilitate price discovery of block space?

---

**unbalancedparenthese** (2025-12-16):

Great article. Looking forward to see what’s next.

---

**nuel-ikwuoma** (2025-12-22):

this is the right model on which every credible ‘blockspace offering’ solutions like ethereum should hinged.

