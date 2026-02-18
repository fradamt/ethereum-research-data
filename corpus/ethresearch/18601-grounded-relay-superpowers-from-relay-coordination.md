---
source: ethresearch
topic_id: 18601
title: "Grounded Relay: Superpowers from Relay Coordination"
author: DrewVanderWerff
date: "2024-02-07"
category: Proof-of-Stake > Economics
tags: [mev]
url: https://ethresear.ch/t/grounded-relay-superpowers-from-relay-coordination/18601
views: 2086
likes: 6
posts_count: 1
---

# Grounded Relay: Superpowers from Relay Coordination

Thanks to [Alex](https://twitter.com/alextes), [Alex](https://twitter.com/ralexstokes), [Barnabe](https://twitter.com/barnabemonnot), [Dougie](https://twitter.com/DougieDeLuca), [Justin](https://twitter.com/drakefjustin), [Kydo](https://twitter.com/0xkydo), [Matt](https://twitter.com/mcutler), [Robin](https://twitter.com/robindoteth), and a few others for the thoughts and review.

Around The Merge, I started to think about leverage and market dynamics that would evolve in Ethereum’s transaction lifecycle. When speaking with researchers, builders, and MEV tourists, all but one pointed to block builders and validators as key parts to the puzzle—however, one standout highlighted the relay as the “watchtower” with the crucial role of coordination. Initially, I laughed, thinking that a relay could never make money… Fast forward and it became clear that both views were correct; relays are watchtowers and weren’t successfully monetizing. But, as we continued research around block builders and blockspace, we realized we could be missing something subtle about the power the relay wields.

Most of the conversation about relays has been in a negative light, even some pinning them as dead without much [hope of survival](https://mirror.xyz/0xE21b1e6f471EDeF18264e9BBe51b7fA7643EE6B5/0Sh7BDW7qgH_nadfqF8bpmnjxnfoYzPFvRdmoIoi9mg). However, we believe relays have a path forward to use their superpower of coordination to not only be additive to the Ethereum ecosystem, but also become sustainable. We call this middleware Relay Added Value-Boost or RAV-Boost. This middleware isn’t quite based, but it is grounded in ideas of how the relay could benefit the future of Ethereum.

[![Spider-Man](https://ethresear.ch/uploads/default/optimized/2X/4/4890382ef19c1df22bd2fcc8a8dfe3682e675c51_2_690x282.jpeg)Spider-Man1352×553 59.8 KB](https://ethresear.ch/uploads/default/4890382ef19c1df22bd2fcc8a8dfe3682e675c51)

**History**

Flashbots introduced the current-day relay software via their marque product, MEV-boost. This software is an out-of-protocol solution to allow validators to outsource building and equal the playing field for solo validators to still benefit from MEV. Until recently, “positive” literature on relay business [has been limited](https://mirror.xyz/0xE21b1e6f471EDeF18264e9BBe51b7fA7643EE6B5/0Sh7BDW7qgH_nadfqF8bpmnjxnfoYzPFvRdmoIoi9mg). However, there are plenty of resources about how awful it is to run a relay. Cited pain includes, but is not limited to [1]:

- Potential regulatory risks
- Cited lack of profitability / with reasonable overhead cost
- The need to use poor standards from a broadly adopted middleware that needs developer love
- A good chunk of Ethereum researchers / the community is trying to get rid of it, so why invest

Because of this pain and lack of monetization, only five relays currently have [90% market share](https://mevboost.pics/) (with two of those relays run by the same company). Further, the resource investment from Flashbots and their focus on MEV-boost has drastically reduced, resulting in product deterioration. Last, MEV-boost has, on multiple occasions, become a concern around upgrades for Ethereum[2] and caused [issues](https://collective.flashbots.net/t/disclosure-mitigation-of-block-equivocation-strategy-with-early-getpayload-calls-for-proposers/1705). Long-term, and in some cases [short-term](https://x.com/blocknative/status/1706685103286485364?s=46&t=ruG_HMQUodILQdpYNrhO9g), the dynamics are not sustainable.

[![Slot Share](https://ethresear.ch/uploads/default/optimized/2X/7/770c03e2165b7db450f2ebdc36e227e9f46e1da6_2_690x387.png)Slot Share947×532 110 KB](https://ethresear.ch/uploads/default/770c03e2165b7db450f2ebdc36e227e9f46e1da6)

Even with all the challenges and headaches outlined above, the relay is [thriving](https://mevboost.pics/) (since the merge, excluding some brief periods, 90%+ of blocks go through MEV-boost / relays) and single-handedly is coordinating 900,000+ validators with ~15+ block builders—a coordination feat unmatched by probably any other middleware in web3. Given this connectivity, is there an opportunity to use the relay’s superpower of coordination to offer products and services that benefit various stakeholders?

[![Mev -boost slot share](https://ethresear.ch/uploads/default/original/2X/6/6c458f7186c48b3a2d59431380550195dc692bb5.png)Mev -boost slot share850×464 34.6 KB](https://ethresear.ch/uploads/default/6c458f7186c48b3a2d59431380550195dc692bb5)

**Enter RAV-Boost**

Most current innovations around monetization / relay improvements are [latency](https://github.com/michaelneuder/optimistic-relay-documentation/blob/4fb032e92080383b7b5d8af5675ef2bf9855adc3/proposal.md) or capturing [spreads](https://gist.github.com/blombern/c2550a5245d8c2996b688d2db5fd160b). People have also debated whether the relay can capture value through [coordinated fee-fixing](https://hackmd.io/@KuDeTa/relay_guild_mvp) efforts. There has also been [research](https://hackmd.io/@bchain/BJkarrEWp) around PEPC-boost, which starts to encapsulate the power of the relay. While these approaches may work, we hope to extend these efforts highlighting potential products and services the relay could offer with a focus on the magic of the relay: coordination. Products and services this middleware could provide span three themes:

- Validator specific products
- Block builder-specific products
- Block builder to validator products

This list is not exhaustive but provides a few ideas we hope spurs others to build on and innovate around. We also note that with time, like how the builder market could evolve, we expect to see relays with specialized skills that optimize in one product but not the other. For instance, to run a blockspace futures market, the relay may need to be sophisticated in blockspace risk management but may not have the expertise to connect to new middleware. This specialization could help ensure healthy competition amongst at least a few relays. We also see the relay offering some of this functionality to builders OR validators. This separation is subtle, but this mental model is an essential departure from how most view today’s relay.

**Validator products:** These products are offered to validators by the relay. In some cases, the products may require most validators to opt in or provide a product that directly benefits the validator. The block builder may not “be aware” that the relay is offering the validator these products.

- Pre-confirms: This product is critical for both L2s and potentially Ethereum’s near-term success to being a based sequencer. Justin has written on potential designs of based pre-confirms. Within this construct, we see the relay as potentially acting as the facilitator for out-of-protocol pre-confirms to quickly come to market
- Integration to other middleware: One of the areas we see a relay focusing is allowing validators to integrate with other middleware seamlessly or be able to read / write to external middleware as part of the relay’s ability to offer products to / for validators
- Modularized product features: Each validator has its requirements and needs. Relays could provide more modularity to allow validators to seamlessly switch product features on and off or provide flexible product features. For example, this may not be the most Ethereum-aligned, but a low-hanging fruit is a compliance / non-compliance transaction flag, where a validator can easily specify if they want blocks with or without potentially “risky” transactions included (maybe even the validator could be more expressive on what they consider “risky”). Another potential feature could be the relay offering a varying degree of risk depending on the validator’s tolerance to missing a slot with the upside of maximizing the value packed in the block
- Validator flexibility: Similar to the feature above, the relay could potentially build a service that allows the validator to message the relay ahead of the block that the validator would like to receive (or not receive) certain features or services, and the relay would adapt their behavior based on this feedback across each block[3]

**Builder products:** These products are offered to block builders by the relay. In some cases, the products may require most block builders to opt in or provide a product that directly benefits the builder. The validator may not “be aware” that the relay is offering the block builder these products. Some of these products could also start to look like the relay offering decentralized / distributed block building as the relay pieces together the output of these products.

- Pre-confirms: Pre-confirms have mostly been researched as implemented by a validator. While we agree this is a potential promising path, we also see this product potentially being developed and offered directly to builders. This approach has multiple advantages, including the relay being able to run a pre-confirm auction market across builders to get the best pricing and the builders being able to optimize blocks around the pre-confirm
- Innovations around gas: Pre-confirms could be viewed as a block space structured product. However, countless variations of gas optimization could be structured and, most importantly, coordinated by the relay. For instance, a block builder could sell the future inclusion of a transaction and be part of the relay coordination service to ensure that even if the builder doesn’t stack the block where the future expires / is exercised, the relay ensures that the transaction is included in the block
- Partial block building: With time, builders may start to specialize in building various parts of the block. For instance, CEX / DEX arb builders may only care about optimization at the top of block, while another builder may specialize in packing the rest of the block. A relay could potentially start acting as an aggregation layer across builders to provide more granular auctions within blocks. Similarly, through conversations with Barnabe, it was also highlighted that the relay maybe able to help with PEPC-boost, by the relay not just aggregating partial blocks together, but also cleaning up reverted / transactions that are invalidated by something in the top of block
- Integration to other middleware: Similar to validators, there is a potential role in acting as a trusted party between someone who needs computing / optimization and the party providing it. For instance, as outlined in PBS for AVS, there is a potential need for computing for “Intensive AVSs” and a middleware required to connect the operator running the AVS with a party such as a builder
- Blob management: This product is less clear, but managing and organizing blobs will be important moving forward and likely will require some coordination across blocks and builders. A relay is in a great position to explore this

**Builder-to-validator products:** Instead of just coordinating passing payloads, the relay can coordinate other information between the builders and validators.

- Inclusion lists: While we wait for the devs to do something about inclusion lists, relays could implement this feature now. This would allow us to have the feature today, as well as provide a space for innovation to try different implementations to find the most optimal for enshrinement in Ethereum
- MEV burn / smoothening: Relays could test various ideas around MEV burn. One implementation could be to instead of burning the ETH, the relay keeps the “burnt” ETH as a fee. This might be harder to get buy-in from builders / validators and could be gamed, but it still warrants exploration. A relay could also potentially create a network using smoothening commitments to guarantee something about inclusion or ordering of transactions. Again, instead of the smoothening commitment payment going to the Ethereum network, it would go to relays

**The Future**

We know these ideas are not a silver bullet, and other issues may evolve if a relay starts to build these products. Some open questions worth considering:

- Does enshrined PBS remove the need for innovation by a relay
- As activity moves to an L2, how will this affect the importance of the relay / feasibility of these products
- If L2s implement PBS in one form or another, does the relay play a similar critical role and could relays at the L1 support relays at the L2? Do we need a “Super Relay”

We hope this inspires a different lens to the dire situation we currently are in for the sustainability of the relay market. With all this said, we are already engaging with and keen to meet teams researching and building products that could benefit from the coordination superpower the relay currently holds.

**Footnotes:**

[1] Some commentary / references to this include but are not limited to: https://x.com/mcutler/status/1650523821957578752?s=46&t=ruG_HMQUodILQdpYNrhO9g, https://x.com/blocknative/status/1706685103286485364?s=46&t=ruG_HMQUodILQdpYNrhO9g, https://www.youtube.com/watch?v=OsgjL17rvwA, and [Unbundling PBS: Towards protocol-enforced proposer commitments (PEPC)](https://ethresear.ch/t/unbundling-pbs-towards-protocol-enforced-proposer-commitments-pepc/13879)

[2] Situations like this might be avoided if full-time teams could focus on testing and working through upgrades with MEV-boost in mind, [Crypto & Blockchain Research Reports | Galaxy](https://www.galaxy.com/insights/research/ethereum-all-core-developers-call-143-writeup/)

[3] Idea originally created out of a conversation one of the reviewers had with Alex Stokes

***Important Legal Information & Disclaimer ***

*The commentary contained in this document represents the personal views of its authors and does not constitute the formal view of Brevan Howard. It does not constitute investment research and should not be viewed as independent from the trading interests of the Brevan Howard funds. The views expressed in the document are not intended to be and should not be viewed as investment advice. This document does not constitute an invitation, recommendation, solicitation, or offer to subscribe for or purchase any securities, investments, products or services, or any investment fund managed by Brevan Howard or any of its affiliates. Unless expressly stated otherwise, the opinions are expressed as at the date published and are subject to change. No obligation is undertaken to update any information, data or material contained herein.*
