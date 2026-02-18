---
source: ethresearch
topic_id: 23635
title: Trustless payments
author: BrunoMazorra
date: "2025-12-10"
category: Consensus
tags: [mev]
url: https://ethresear.ch/t/trustless-payments/23635
views: 502
likes: 27
posts_count: 5
---

# Trustless payments

# Trustless payments

> TL;DR
> We are in favour of keeping the trustless payments component of EIP-7732. While the design can be improved, the limitations are not damning, can be improved upon, and do not outweigh the importance of permissionlessness.

Joint work with [@jcschlegel](/u/jcschlegel) ,[@quintuskilbourn](/u/quintuskilbourn), [@boz1](/u/boz1), and [@LuisVCorreia](/u/luisvcorreia). Thank you [@tripoli](/u/tripoli) for extensive feedback. And finally, all members of the ePBS thinkboi Association.

[![](https://ethresear.ch/uploads/default/optimized/3X/d/6/d6a78237d6e454977a3258ed2253052988758d12_2_690x368.jpeg)1650×881 92.4 KB](https://ethresear.ch/uploads/default/d6a78237d6e454977a3258ed2253052988758d12)

In this post, we provide an overview of the implications of trustless payments introduced by [EIP-7732](https://eips.ethereum.org/EIPS/eip-7732) and justify our support for the EIP. We only reflect our views and do not provide a stance for the whole Flashbots organization.

Let us start with what we believe is self-evident: proposer-builder separation will remain the block-building architecture of Ethereum for the foreseeable future. The efficent way to organize the proposer-builder interaction is through a just-in-time (JIT) block auction. Even if we would want to enshrine a different market structure (e.g., through APS), efficiency dictates that a JIT market out-of-protocol will emerge to achieve efficiency. The core question is how the Ethereum network should interact with this market.

Currently, validators maintain lists of trusted “relays” who are external to the protocol and provide blocks. Distinctions between relays and builders here are not inherent (and clearly fading) - *what ultimately matters is who has access to the proposer*. Securing access to the proposer currently involves doing business development and building trust with node operators. This is exactly the kind of high-friction coordination which Ethereum aims to avoid. To have a protocol that is robust and resilient throughout the stack, we shouldn’t leave major parts that are core to its effective functionality to run purely on trust. The only viable long-term choice is to enshrine the builder role in protocol and offer a way for builders and proposers to contract in-protocol trustlessly.

What follows from the previous is that we should either implement enshrined builders and trustless payments now with EIP-7732 and the proposal available to us or wait and implement them later. The only reason to wait in our opinion would be if 1) the current proposal has a major flaw or 2) there is a viable and sufficiently detailed alternative design that we can implement soon. Minor flaws shouldn’t be a reason to halt the process and can be iterated on or improved in future protocol updates. Delaying a trustless payments mechanism further into the future will only make it harder to introduce since the surrounding out-of-protocol ecosystem will become further established. Option 2) is not available to us, hence we need to determine whether there is any major flaw and on the way check whether minor flaws can be mitigated or removed.

So let us go through potential problems with trustless payments as proposed and see whether any of them would be a major flaw:

### Capital cost for builders

In-protocol bidding requires builders to stake which introduces additional cost. Specifically, they need to run a validator and become a critical infrastructure for the network, which requires locking 32 ETH to the protocol. Moreover, they need to additionally collateralize bids, similar to what they already do with optimistic relays. This combination of cost could eliminate a long-tail of builders bidding in-protocol who don’t want to or can’t afford to lock money for an unknown period of time.

These costs are non-negligible, however validator duties generate yield on the whole 0x03 builder balance, so that cost are effectively only the opportunity cost, operational costs and costs of sourcing the capital. Most blocks’ bids are not very large (<0.02ETH) (99% of block bids are < 0.46ETH). These costs can also be partly avoided, as relaying services are likely to continue to exist (through staked and unstaked variants), providing access to the proposer for the unstaked actors. Collateralization of bids is in any case necessary for any permisionless bidding system that doesn’t rely on reputation or use of additional DA services.

Furthermore, a lot of the capital costs can be mitigated by improving on technical inefficiencies, either in the current EIP or in future. For example, forcing builders to run a validator and stake 32ETH doesn’t make sense if we were to design a system from scratch. It is there because of path-dependance and tech debt, and is ideally removed in the future (e.g., through future protocol upgrades to [lower validator stake requirements](https://vitalik.eth.limo/general/2024/10/14/futures1.html)).

[![Captura de pantalla 2025-12-10 a las 16.21.03](https://ethresear.ch/uploads/default/optimized/3X/7/1/71ff06b4cd1389ed348fe15ab84160243ac758ab_2_690x345.png)Captura de pantalla 2025-12-10 a las 16.21.031808×904 72.6 KB](https://ethresear.ch/uploads/default/71ff06b4cd1389ed348fe15ab84160243ac758ab)

Figure: MEV rewards (<1 ETH) between blocks 20000000 and 23984511.

### Tech cost and operational complexity

Introduction of trustless payments will require work from builders and relays to adapt to the change and introduces more state for the consensus clients to track.

In-protocol bidding goes through a slower flow using the deposit and partial withdrawal features of the Ethereum consensus layer. This removes the flexibility of JIT bid funding and settlement, as builders need to initially register with the protocol and fund their account for bids. This is an artifact of implementing the builder logic entirely on the consensus layer which wasn’t built for inter-validator payments. It makes the feature more cumbersome to use, but not unusable, and subject to future improvements.

Additional improvements like programmatic builder endpoint discovery and management for validators should also be considered.

While all of these do represent additional effort, we do not believe that this cost is not justified, especially since any form of trustless outsourcing of block production will require some of this work. It’s also worth noting that trustless payments remove the need to manage node operator relationships that is required for relays to gain and maintain market share. So it removes this overhead.

### Market structure

The Ethereum block-building market is [already highly concentrated today](https://www.relayscan.io/), raising concerns for the chain’s long-term [neutrality](https://ethresear.ch/t/uncrowdable-inclusion-lists-the-tension-between-chain-neutrality-preconfirmations-and-proposer-commitments/19372). A reasonable concern to address is whether EIP-7732 may increase concentration due to capital costs and risk management.

As we have mentioned in the section on capital costs, we believe that these concerns are likely not as severe as anticipated. More fundamentally, we believe that it is better to push risk & complexity on to external market participants instead of proposers. Without EIP7732 proposer risk management manifests as managing allow-lists. With EIP7732 proposers do not need to trust relays at all. Importantly, EIP-7732 does not prevent blocks being sourced from unstaked builders.

In either case, we believe the neutrality challenge should be further addressed at the protocol level, through mechanisms such as [FOCIL](https://eips.ethereum.org/EIPS/eip-7805) that strengthen censorship resistance.

### Implications to the Free Option Problem

Pipelining introduced the [“Free Option Problem”](https://arxiv.org/abs/2509.24849) and the problem does *not* disappear if we remove trustless payments. Practically, the free option problem might play out differently though: if we force bids through relays, then relays can help policing the free option problem. Mitigation mechanisms on the relay level could be measures such as deposit requirements for builders to police payload delivery failures, only allowing bids from a permissioned set of builders (or block-listing builders that have failed to deliver payloads in the past) or to allow “optimistic” bids only for a permissioned set of builders.

Such mitigation mechanisms are, in principle, also possible in protocol, for example via builder deposit requirements which could be used for punishments in the event of failed payloads. We have advocated for and spec-ed this out in [this post](https://ethresear.ch/t/dynamic-penalties-for-epbs/23472). In this context, allow-listing or block-listing are trickier, as proposers generally don’t have an incentive to use them. However, we shouldn’t rely on them long-term on the relay level, as either this leads effectively to a permissioned set of or discrimination between builders (on which services they can access) managed by out-of-protocol actors or to new (or existing) relays offering what is lucrative to proposers - access to builders using the “free option” together with an unconditional payment mechanism mediated by the relay.

### Sealed-bids

If direct communication is employed and relays are bypassed, the auction format effectively shifts from the status quo—an open auction with a random deadline—to a sealed-bid auction.

While some argue that sealed-bid auctions under ePBS negatively impacts the builder market structure, we think that the effects are net neutral or more likely positive. Specifically, the current open-bid auction favors builders with latency advantages, allowing them to outbid competitors moments before the deadline. This asymmetry [promotes market concentration](https://arxiv.org/pdf/2311.09083). Conversely, a sealed-bid auction levels the playing field by neutralizing these latency advantages, resulting in a fairer mechanism. Sealed bidding leads to less bids to process per builder and is therefore more bandwidth-friendly.

While one could argue the mechanism lacks credibility—specifically, that validators might have incentives to leak bids to boost revenue, unless the auction has a significant *and* unknown common value component, validators generally have no incentive to disclose information in a sealed bid first-price auction. Notably, this leads to a more efficient auction outcome, increases revenue in equilibrium and is more fair to all market participants.

### Nobody will use them?

As we have argued so-far, the additional cost of using trustless payments seems to be small and there are also potential efficiency gains. Optimistic relays can give us some intuition on what we might expect: currently, a majority of blocks are proposed through the optimistic path and builders are happy to deposit with optimistic relays, but for high value blocks they might go through the pessimistic path. We might expect similar things to happen with trustless payments: parallel usage of both paths depending on the situation.

The difference in value for in-protocol and out-of-protocol bidding for builders seems marginal, which brings us to the arguably biggest blocker: *switching cost*. In other words, it requires engineering effort for builders to integrate the in-protocol path. So let us point out the obvious: this relies largely on the good will of ecosystem participants (builders and relays mostly) to want to make it work. We are very optimistic on this point, as historically people have stepped in to make Ethereum work and prioritize the long-run over short term cost-savings. As probably haven’t missed your attention, we are close to one of the major builders and we would obviously lobby them to embrace the in-protocol path and allocate engineering capacity to make it work.

## Replies

**terence** (2025-12-10):

Re: Capital cost for builders

It’s worth raising that design could be updated to such builders could be allowed to participate in protocol bidding without meeting the `MIN_ACTIVATION_BALANCE` (32 ETH) requirement and instead just have a 1 ETH minimum balance. They wouldn’t act as active validators or earn yield on that 1 ETH but it lowers the capital needed. From spec’s perspective, it’s not a difficult change, but we do want to study its implications

---

**alextes** (2025-12-11):

first, appreciate the contribution to the discussion. i’d be remiss not to point out the following:

![](https://ethresear.ch/user_avatar/ethresear.ch/brunomazorra/48/10029_2.png) BrunoMazorra:

> The only reason to wait in our opinion would be if 1) the current proposal has a major flaw or 2) there is a viable and sufficiently detailed alternative design that we can implement soon.

this seems like a v low bar to get something in, and a v high bar to stop it from getting in. not to mention the enormous amount of resistance to splitting, which preserves most of the currently detailed design, even much of its implementation.

![](https://ethresear.ch/user_avatar/ethresear.ch/brunomazorra/48/10029_2.png) BrunoMazorra:

> what ultimately matters is who has access to the proposer

yes. and today, if you tried to get a block on chain, you’d notice it has nothing to do with relays gatekeeping. in fact, they make it much easier than trustless which requires min 32 ETH, a single bid, sent over p2p (or BD or CL updates needed), sealed bid first price, miss risk 100% for builder.

![](https://ethresear.ch/user_avatar/ethresear.ch/brunomazorra/48/10029_2.png) BrunoMazorra:

> It’s also worth noting that trustless payments remove the need to manage node operator relationships that is required for relays to gain and maintain market share. So it removes this overhead.

this i don’t follow. i feel like multiple times the biggest builder in the market today has explained this overhead is and remains a sensible investment because one can give out higher bids.

![](https://ethresear.ch/user_avatar/ethresear.ch/brunomazorra/48/10029_2.png) BrunoMazorra:

> we believe that it is better to push risk & complexity on to external market participants instead of proposers.

we again agree in principle but seem to estimate the opposing impact. i don’t quite understand why.

![](https://ethresear.ch/user_avatar/ethresear.ch/brunomazorra/48/10029_2.png) BrunoMazorra:

> the current open-bid auction favors builders with latency advantages, allowing them to outbid competitors moments before the deadline. This asymmetry promotes market concentration. Conversely, a sealed-bid auction levels the playing field by neutralizing these latency advantages

bidding heats up late in the slot but most builders seem to drop from the race long before that point. if you have analysis that suggest that type of toxic behavior is happening i’d love to see it. we could easily counter-act. on the latter point, neutralizing latency advantages, i really don’t see how this is true. later is still better. it allows builders to build more valuable blocks. latency still matters. i don’t see how this changes with a sealed bid auction. it seems to me those who focus on latency across the pipeline will still win out.

on permissionlessness. permissionlessness is huge, but we have local block building. shouldn’t the benefit of any adopted change beyond that be significant?

ok, more to say but i’m out of time. again thank you for this extensive piece. i do remain a bit confused why people prefer to push ahead despite so many points remaining contentious.

---

**BrunoMazorra** (2025-12-11):

Maybe I’m stretching what can be done for Glamsterdam, but wouldn’t it make sense to have both options? i.e. either become a ‘builder-validator’ with `min_balance = 32 ETH` or just a builder with `min_balance = 1 ETH`.

---

**ltitanb** (2025-12-11):

I don’t think reducing the minimum deposit helps much for capital costs. With optimistic relaying a builder only needs to have collateral for a single block, as was mentioned 0.5ETH could be enough for most blocks. With staked builders one has to deposit in advance a lot more and it depends on the length of the deposit queue (potentially weeks). If for whatever reason the builder runs out of balance it will be locked out of bidding until it can deposit again

