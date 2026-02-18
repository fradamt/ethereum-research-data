---
source: ethresearch
topic_id: 21953
title: Separation Gap, Trusted Advantage, and APS
author: daniel5713
date: "2025-03-13"
category: Economics
tags: [mev, consensus]
url: https://ethresear.ch/t/separation-gap-trusted-advantage-and-aps/21953
views: 272
likes: 2
posts_count: 1
---

# Separation Gap, Trusted Advantage, and APS

By [Tong CAO](https://x.com/0xCaotongtong) and [Julian MA](https://x.com/_julianma). This blog post presents the outcomes of [ROP-13](https://efdn.notion.site/RIG-Open-Problems-ROPs-c11382c213f949a4b89927ef4e962adf?p=107d9895554180eeb352d12ccef5a325&pm=s).

# Background

Modern consensus protocols allow the participants to include the heavy execution payload into the blocks to support various functionalities. In each round, an elected participant as the leader verifies the global state of blockchain, constructs execution payload, and proposes a new block. The block is then verified by other participants gradually, and disseminated in the peer-to-peer network. As the need for execution payload increases, relying on one leader to construct execution payload and propose block has shown some shortcomings: 1, entities that are often elected as the leader can be easily discovered and be forced to censor transactions; 2, entities that are often elected as the leader would be able to use more resources to extract values from transaction ordering, which would lead to reward disbalance among the participants; 3, the leader would become the bottleneck of system throughput in each round. There has been an obvious trend to separate the task of constructing execution payload from the consensus protocol (i.e., block proposer is responsible for consensus block, and execution payload proposer is responsible for execution block. Please find more details about the concept of consensus execution separation in [ethereum.org](https://ethereum.org/en/developers/docs/nodes-and-clients/), [cryptofrens.info](https://www.cryptofrens.info/p/modular-design-and-the-two-blockchains)). For instance, [PBS](https://ethereum.org/en/roadmap/pbs/) allows block proposers to take the execution payload from builders relying on some trusted entities. [EPBS](https://ethresear.ch/t/why-enshrine-proposer-builder-separation-a-viable-path-to-epbs/15710) aims at achieving “Separates the ethereum block in consensus and execution parts, adds a mechanism for the consensus proposer to choose the execution proposer.”

# What’s new?

In this article, we define Separation Gap to categorize and analyze existing Ethereum’s separation protocols. We show that a non-zero separation gap would be generated when one wants to guarantee [Honest Builder Payload Safety and Honest Builder Payment Safety](https://ethresear.ch/t/equivocation-attacks-in-mev-boost-and-epbs/15338) without relying on any trusted entity. Within the separation gap, both [block auction and slot auction](https://efdn.notion.site/Arguments-in-Favor-and-Against-Slot-Auctions-in-ePBS-c7acde3ff21b4a22a3d41ac4cf4c75d6) would be feasible (currently, slot auction has more benefits). We simulate slot auction in three scenarios to evaluate whether “No Trusted Advantage” (was first defined in [here](https://ethresear.ch/t/epbs-design-constraints/18728#35-no-trusted-advantage), and then explored in [here](https://ethresear.ch/t/trusted-advantage-in-slot-auction-epbs/20456)) can be satisfied. Our findings are:

- the fundamental reason of whether “No Trusted Advantage” can be satisfied is whether the execution proposer can get the highest bid (all slot time high) at the beginning of the slot. If affirmative, the execution proposer would lack incentive to delegate payload construction task to third-party builders in the secondary market during the remaining time window of the slot;
- the key factors in getting the highest bid at the beginning of the slot are builders’ historical performance and builders’ prediction ability;
- when every builder submits the bid with a predicted value depending on the expected value, the execution proposer is willing to outsource the construction task to the secondary market, and accept the highest bid at the end of bid window, and take the risk in a more decentralized builder network (i.e., the deviation is small). In this case, “No Trusted Advantage” can not be satisfied, and trusted entities in the secondary market would help the execution proposer earn more revenue;
- when every builder submits the bid with a predicted value depending on the expected value, the execution proposer is willing to accept the highest bid at the beginning of the slot, and let the builders take the risk when the builder network is relatively centralized. In this case, “No Trusted Advantage” can be satisfied, and we do not escape from the centralized builder network.
- the complete separation protocol (i.e., Attester-Proposer Separation) can essentially eliminate the negative impact of slot auction on consensus protocol.

# Separation and Separation Gap

## Definition

**Semi Separation.** The block proposers can select either to construct execution payloads by themself or take the execution payload from others.

**Complete Separation.** The block proposers can only propose consensus blocks, while the execution payload construction rights belong to other entities.

**≈0 Separation Gap.** The consensus block and execution payload approximately arrive in the peer-to-peer network at the same time.

**≈½ Slot Separation Gap.** The execution payload approximately arrives in the peer to peer network ½ slot time later than the consensus block.

For brevity. In the following figures, consensus blocks are presented by the same square, which does not mean consensus blocks are the same in different slots.

## Semi Separation and ≈0 Separation Gap

[![MEV-Boost](https://ethresear.ch/uploads/default/original/3X/8/4/849ee84bd13d7a9c0637088041df10bd6b244149.png)MEV-Boost648×260 19.7 KB](https://ethresear.ch/uploads/default/849ee84bd13d7a9c0637088041df10bd6b244149)

## Semi Separation and ≈½ slot Separation Gap

[![EPBS + Block Auction](https://ethresear.ch/uploads/default/original/3X/5/3/5372ee7e52e3d8ccb37077598d61f2e9ea6ee18c.png)EPBS + Block Auction648×260 22.4 KB](https://ethresear.ch/uploads/default/5372ee7e52e3d8ccb37077598d61f2e9ea6ee18c)

[![EPBS + Slot Auction](https://ethresear.ch/uploads/default/original/3X/2/3/2345a5a7ea5120c5120d9c19135b0e2886397162.png)EPBS + Slot Auction638×260 22.1 KB](https://ethresear.ch/uploads/default/2345a5a7ea5120c5120d9c19135b0e2886397162)

## Complete Separation and ≈½ slot Separation Gap

[![APS](https://ethresear.ch/uploads/default/optimized/3X/2/6/266d3bce298ad7ce61e3f0f4db3c45b22ff9f95b_2_517x320.png)APS772×478 37.8 KB](https://ethresear.ch/uploads/default/266d3bce298ad7ce61e3f0f4db3c45b22ff9f95b)

# No Trusted Advantage in Slot Auction

## Definition

It was defined [here](https://ethresear.ch/t/trusted-advantage-in-slot-auction-epbs/20456): “(Definition) No Trusted Advantage: The beacon proposer is incentivized to use the in-protocol commitment to commit to the block producer whose in-protocol bid value maximizes the beacon proposer’s utility.”

We redefine it as follows:

**No Trusted Advantage.** The entity who has the execution payload construction right would not be able to gain an advantage (i.e., earn more revenue) by outsourcing the construction task to the trusted entities in the block building market.

## Simulation

In a network consisting of 100 builders, we simulated slot auctions in three different settings: 1, Builders’ historical performances follow a Power Law distribution; 2, Builders’ historical performances follow a random distribution; 3, Builders’ historical performances based on MEV-boost data.

### Assumptions

- Anyone can observe all builders’ historical performance, and calculate the expected bid value of each builder;
- Builders use a vanilla slot auction bidding strategy. Around the beginning of the slot, each builder submits the bid depending on the expected bid value;
- The elected entity that has the execution payload construction right (e.g., block proposer in EPBS, execution block proposer in APS) is profit-driven, who will outsource the construction task to a secondary market if doing so is more profitable.
- The MEV opportunity arrivals for each builder follow the Poisson process.

### Methodology

In different settings, we let each builder submit: 1, a bid according to the expected bid value at the beginning of the slot; 2 a bid based on the real captured value at the end of the bid window.

If the highest expected bid value Max(v_{eb}) is larger than the highest captured bid value Max(v_{cb}), we say that the construction task should not be outsourced, vice versa. We run the simulation to estimate the probability (denoted by P) of that Max(v_{cb}) > Max(v_{eb}).

### Result

#### Case 1: Power Law distribution. P≈0.48

**Analysis:** Power Law distribution indicates a centralized builder network. Like today’s builder network, the [top 3 builders](https://www.relayscan.io/overview?t=7d) constructed more than 95% blocks. In this network, if the top builders submit a bid at the beginning of the slot based on their past performances, the block proposer should follow them in order to optimize their revenue. Sometimes, though the block proposer can get more from the secondary market, there is a risk by outsourcing the construction.

#### Case 2: Random distribution within a small range. P is dependent on the range of the random data sample. When the range is from 50 to 75 (number of arrived MEV opportunities), we have 0.75 < P <0.9. When the range is from 65 to 75, P≈0.95.

**Analysis:** Random distribution within a small range indicates a desired builder network, where builders are likely homogeneous and have similar ability to obtain MEV opportunities and extract values. In this network, P is decided by the range of the random distribution. In the extreme case, when the range is equal to 0, meaning, all builders have exactly the same expected bid value, P1. As the range increases, P decreases slightly. In this simulation, we do not consider random distribution with a large range since it does not reflect a desired or possible builder network. This result demonstrates that the block proposer has a high driving force to outsource the construction task to the secondary market in a desired homogeneous builder network.

#### Case 3: MEV-boost data. P≈0.0187. We use one-day MEV data from Flashbots (), where we get more than 12,000,000 bids from 115 public keys.

**Analysis:** We use one day MEV-boost data to calculate the real expected bid value for each builder (identified by public key). It is then easy to calculate the highest expected bid value Max(v_{eb}). We use the next day’s MEV-boost data to evaluate if there is a Trusted Advantage in the slot auction. The highest captured bid value Max(v_{cb}) can be easily found in the slots of next day. Surprisingly, we find that P≈0.0187 by using MEV-boost data as the input of the simulation. As shown in the following Figure, in most slots, we have Max(v_{eb})>Max({v_cb}). Given that today’s builder network is highly centralized, the value of P in this case is vastly lower than the simulation result by using power law distribution. Please be aware that the builder with the best historical performance might not submit the bid frequently. In this simulation, we assume that all builders submit a bid depending on their historical performances in each slot, which is actually too strong. We aim to relax this assumption in future work. Due to the limitations of the simulation, we only can observe that: 1, if the builder network of MEV-boost is transitioned to a slot auction based separation protocol, the block proposer would not be incentivized to outsource the execution payload construction task to the secondary market when every builder uses the vanilla slot auction bidding strategy (i.e., depending on the expected bid value); 2, when builders submit bids depending on other methods (i.e., mean of all builders’ expected bids), the block proposer would have a relatively high driving force to outsource the construction task.

[![Expected-vs-Captured](https://ethresear.ch/uploads/default/optimized/3X/e/d/eda70e47e1437982e0d0a968aa3ea13744d79d37_2_499x375.png)Expected-vs-Captured800×600 30.5 KB](https://ethresear.ch/uploads/default/eda70e47e1437982e0d0a968aa3ea13744d79d37)

## Limitations

- Lack of various bidding strategies in slot auctions. In this post, we only consider a vanilla bidding strategy in slot auction, which is, the builder uses the expected bid value to compete with others at the beginning of the slot. However, this strategy is obviously not the best strategy for builders.
- Lack of real world data for slot auctions. In this post, we use MEV-boost data as an input to simulate slot auction, which has two drawbacks: a, we do not know how builders actually submit bids with a predication at the beginning of the slot; b, different bid windows might lead to different behaviors.
- Lack of profitability analysis. P is only used to estimate the possibility of that max(v_{eb})>max(v_{cb}). Lower value of P does not mean that the beacon proposer can not be profitable from outsourcing the construction task to the secondary market. As long as the revenue is big enough, even if P is relatively small, the rational block proposer would like to outsource the construction task to the secondary market.
- We assume that builders’ MEV opportunity arrivals follow the Poisson process.

## Relationship to APS

The above analysis preliminarily verifies that Trusted Advantage exists in slot auctions, where the proposer would outsource the execution payload construction task to the secondary market and gain more revenue from the trusted entities. To enhance the separation of consensus and execution withouting relying on trusted entities, it is necessary to mitigate the impact of Trusted Advantage in slot auctions.

[Attester-Proposer Separation](https://efdn.notion.site/Attester-Proposer-Separation-Tracker-15bd9895554180c2ac75cb40878ecd33) (APS) is a potential future upgrade to Ethereum that would introduce slot auctions. APS mitigates the impact of Trusted Advantage problem by completely separating the execution proposing rights from block proposer. Even if the builder chooses to connect with a trusted entity, the unconditional payment from the builder to the protocol would not affect consensus protocol because the block proposer does not need to trust any third party. We emphasize here, in APS, the consensus protocol no longer needs tight coupling with some centralized and trusted entities.

This work shows the importance of a secondary market. Even in APS, the secondary market remains important. A failing secondary market may lead to intermediaries buying a large share of execution proposing rights in the primary market because they could perhaps sell them at a higher price in the secondary market compared to builders. This is very similar to the setting of a beacon proposer choosing to “buy” the execution proposing rights from themselves in the primary market of ePBS and selling them when the block needs to be delivered.

Heavy involvement of intermediaries in the primary market of APS is undesirable because it deteriorates the potential market structure the primary market of APS could implement. APS may forgo some protocol revenue in favor of a more decentralized builder market. It would do so by implementing a Tullock contest – a market structure with the key characteristics that all participants pay their bid and gain a proportional probability of winning – in the primary market, instead of a revenue-maximizing auction. If not builders but intermediaries participate in the primary market, however, this decentralizing force misses its point as it will not actually lead to more decentralized builders, but to more decentralized intermediaries, which serves no role to the protocol.
