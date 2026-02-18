---
source: ethresearch
topic_id: 20129
title: Builder Bidding Behaviors in ePBS
author: terence
date: "2024-07-23"
category: Economics
tags: []
url: https://ethresear.ch/t/builder-bidding-behaviors-in-epbs/20129
views: 5107
likes: 27
posts_count: 17
---

# Builder Bidding Behaviors in ePBS

Special thanks to [@soispoke](/u/soispoke) for the review

# Background

Builder bidding strategies in the MEV-Boost world have been studied extensively over some time. Numerous [excellent resources](https://arxiv.org/html/2312.14510v3), [literature](https://arxiv.org/abs/2407.13931), [game-theoretic models](https://ethresear.ch/t/game-theoretic-model-for-MEV-Boost-auctions-mma/16206), and [archives](https://collective.flashbots.net/t/MEV-Boost-builder-bids-archive/3561) capture the current builder bidding behaviors on how to win block building right for an Ethereum slot. Today, builder bidding war for MEV-Boost is a complex interplay between latencies, relays, and strategy effectiveness. In this post, we argue that builder bidding strategies become simpler in ePBS world and we highlight the key differences in how bidding strategies change under the new ePBS market space rules, strategy limitations, and reduced latency benefits in ePBS.

# Market Spaces

Here, we summarize three types of market spaces. The first one is MEV-Boost. The second and third ones are ePBS. MEV-Boost is push + pull based market space, meaning the builders push the bids to the relays, and the proposer pulls the bids from the relays. ePBS contains two types of market spaces: the P2P Bid Gossip Netwok, which is push-based, and the Builder RPC Endpoint, which is pull-based.

- MEV-Boost market space

Push + pull-based: The builders push bids to the relay, and the proposer pulls the bids from the relay.

**ePBS market spaces**

- P2P market space

Push-based. The builder pushes the bid to the p2p network.

**Builder RPC market space**

- Pull-based. The proposer pulls the bids from the builder RPC end points.

We define the following market space characteristics given how the consensus [spec](https://github.com/ethereum/consensus-specs/pull/3828) is written today. Builder-API is still **TBD** for ePBS.

## MEV-Boost Market Space

- Open auction: Builders that subscribe to the relay’s feed can see the every builder’s latest bid.
- Continuous auction: Builders can bid multiple times and cancel previous bids.
- Auction termination: The auction terminates when the proposer calls getHeader and when the relay returns the header to the proposer to sign. The relay may delay the header response for a timing game. This means the relayer has the final control over when the auction terminates.
- Profit sharing: Some relays take the difference between the winning bid and the second-highest bid received from builders. This difference goes to the relay, with a portion potentially refunded to the builder. This transforms the auction dynamic into a second-price auction. However, not all relays adopt this approach, and complete trust in the relay is mandatory.
- We assume the market space doesn’t verify block contents from the builder, hence it is an optimistic market space. The only delay is when the builder sends the block to the relay.

## ePBS P2P Market Space

- Open auction: Anyone can subscribe and listen to the P2P network for gossiped builder bids.
- Single bid auction: To prevent DOS attacks on the P2P network, the current spec only allows builders to submit a single bid and above a certain minimum value. Any subsequent bid will be dropped by the nodes. There is no cancellation support over the P2P network.
- Auction termination: The auction terminates when the proposer proposes the block which includes the builder’s bid. The proposer could play a timing game here and has the final control over when the auction terminates.
- Profit sharing: The bid specifies the value, and the proposer gets the full value on the consensus layer as long as the consensus block that includes the bid remains canonical. There’s no profit sharing with 3rd parties.
- The market space is still optimistic and doesn’t need to verify the execution contents at inclusion time. If the execution block later becomes invalid or fails to reveal, the proposer still gets unconditional payment. The only delay here is the builder sending the bid to the P2P network. This delay is argubly longer than using a relay in MEV-Boost market space.

## ePBS Builder RPC Market Space

Note: The [Builder API](https://github.com/ethereum/builder-specs) is undefined at this moment. This section is based on what we think the ePBS Builder API might look like, but it’s highly subjective to change and open for feedback. Below outlines one version of Builder API which we have been thinking.

- Private auction: Only the proposer can request a bid from the builder. The proposer will sign the getHeader request using the builder’s public key. The builder’s bid remains private until requested by the proposer. Builders can’t sniff other builders’ bids unless the builder API allows this or the builder voluntarily opens their bids to the public.
- Single (maybe multiple?) bid auction: Builders allow proposers to request a bid once, and any subsequent requests will result in an error. Builders may also allow proposers to request bids multiple times without error; this specific detail is undefined, and it’s unclear what the Nash outcome is here. If builders allow multiple requests, then the builder must ensure previous bids are canceled.
- Auction termination: The auction terminates when the proposer requests the header and the proposer receives the header. The builder can play a timing game, but this may backfire and lead to the proposer using another builder’s bid. Builder timing game will not work here, but proposer timing games are still relevant.
- Profit sharing: Same as the P2P market space.
- The market space is still optimistic, and the delay here is the builder returning the bid to the proposer. This delay is shorter than the P2P market space and likely the same as MEV-Boost if the builder is well co-located.

# Builder Bidding Profiles under ePBS

In the [Strategic Bidding Wars in On-chain Auctions](https://arxiv.org/abs/2312.14510), four profiles of builder behavior are listed in MEV-Boost auction:

- Naive Behavior: Aggressively updates bids based on their valuation as long as the aggregated signal surpasses their profit margin.
- Adaptive Behavior: Monitors the current highest bid and places a bid if able to outbid by a small constant. Defaults to the naive strategy if unable to outbid.
- Last Minute Behavior: Reveals valuation at the final possible moment before auction termination to minimize the reaction window for other players.
- Bluff Behavior: Initially places high bids (bluff) and later reverts to actual valuation, leveraging bid cancellation to compel other players to disclose their valuations.

Given the new market space in ePBS, we will examine which strategies are viable under the auction rules.

### P2P Market Space

- Naive, Adaptive, and Bluff Behaviors: These strategies are harder to execute since bids can only be sent once. The builder might use different staked addresses, each sending one bid. However, this requires staking on the consensus layer for each address, assuming payment is handled on the consensus layer. Additionally, bluffing is not possible because bids cannot be canceled.
- Last Minute Behavior: This is the only possible strategy. Builders will reveal their valuation at the final moment before auction termination to minimize the reaction window for other players.

### Builder RPC Market Space

- Naive, Adaptive, Bluff, and Last Minute Behavior: For similar reasons to the P2P market space, these strategies are not possible. Additionally, the auction is private, meaning builders cannot see each other’s bids. Most importantly, the auction has shifted from push-based to pull-based, so the builder no longer has control over when to submit bids. The only way for builders to get their bids to the proposer is through the proposer’s request.

We conclude that builders’ bidding strategies are heavily limited under ePBS. For P2P, only last-minute bidding is possible. For Builder RPC, builders can only respond to the proposer as it is a pull-based model.

# Market Space Considerations

We add a few more concerns in this section that was emphasized in the MEV-Boost market space but may no longer be relevant in ePBS market space.

## Latency and DOS Concerns

Different market spaces impose varying latency constraints. In the P2P market space, builders push bids to the proposers, and the market operates as a large P2P gossip network constrained by anti-DOS measures. With 1 million validators, the worst-case scenario could mean 1 million bids. Due to these concerns, rules like disallowing multiple bids and ensuring bids are above certain values are necessary. The P2P network is inherently slow, so we don’t foresee serious bidders using it to win bids. However, the P2P market space is valuable for maintaining a good **baseline for competitive bids** that isn’t latency-sensitive. If builders using RPC collude to drive bid prices low, an **altruistic builder** over P2P can ensure the bid value baseline remains healthy and competitive with minimal effort. The baseline P2P bid value may also be used for burning in future iterations, as it only requires a 1/n honest assumption.

In the builder RPC market space, which is pull-based, latency matters significantly. Instead of two latencies (global and individual) defined in the MEV-Boost market space, there’s only one individual delay to consider: how fast the builder can return the bids to the proposer. Delaying the return of `getHeader` may result in proposer missing builder’s bid.

## Auction Interval Uncertainty

The auction interval uncertainty becomes clearer in ePBS because MEV-Boost middleware and relays no longer control the timing of when the block gets returned to the proposer or released to the network. The proposer either uses the pushed bids from the P2P network or pulls bids from the builders RPC. The proposer has the final say on the auction interval cut-off. From the builder RPC market space perspective, it will keep updating its bids until the proposer requests them.

### New: Bluff Behavior under ePBS

In ePBS, proposers or builders may attempt to bluff other builders. This may not be scalable given the nature of the single bid auction over P2P and the fact that every builder is a validator and needs to have a stake on the beacon chain. One bluff strategy is for the proposer of next slot to reveal a high value P2P bid, intentionally stating that this is the bid it will include for the next slot unless others can beat it. This helps set the base price and forces everyone else to beat it. However, the proposer doesn’t have to include its bid.

Although it’s obvious that anyone can see that the bid comes from the proposer and just ignore it, the proposer may use sybil validators to perform the same bluff. However, it’s still unclear how scalable this strategy is, given that one bid equals one validator.

# Open questions

The current ePBS market space design and requirements leave some open questions. We will summarize the open questions here for feedback:

- P2P Market Space Conditions:

Every builder can only submit one bid, and the subsequent bids get dropped. Are there any advantages to allowing multiple bids here? If yes, then how many?
- Every builder’s bid needs to be above a certain value to deter DOS attacks. What should the value be?

We can look at current or past empirical data here.

There’s a tradeoff between the number of bids allowed and the minimal values. If we set the values high, we may allow multiple bids.
Is there a strong argument for requiring bid cancellation?

**Builder RPC Market Space’s Builder API Interface**:

- What does the Builder API interface look like?

We want to leverage the existing Builder API and aim for minimal changes.
- When the proposer makes a header request to the builder, what should the request look like? Can we use the current get header request with a signature, or should we modify it?
- Do we allow multiple getHeader requests, such as continuous polling from the proposer, or do we enforce a common standard?

What kind of auction is most ideal?

- Sealed second-price auction may be most ideal.
- How to design this over Builder API?

**Comparing MEV-Boost Market Space to ePBS Market Space**:

- Do we lose anything in the ePBS market space that is important to maintain from the MEV-Boost market space?

**Implications of staking pools also bidding:**

- Pools that hold a significant chunk of validators could be in a privileged position for submitting bids and manipulating the market extensively compared to a builder that doesn’t hold as many keys.

Is there an advantage to this asymmetry?
- Will we see staking pools and builders teaming up, and how will this dynamic play out?

## Replies

**M1kuW1ll** (2024-07-23):

Interesting post! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

Several thoughts:

1. P2P Market Place - Single-bid vs. Multiple-bid.
I wonder if an open-bid ascending (multiple bids) auction is more collusion-resistant than an open-bid one-shot (single bid) auction. If a open-bid one-shot auction, it seems easier for builders to engage in off-chain/out-of-protocol agreements (collusion). For example, all the builders bid the minimal value (the DOS attack value) with some tiebreaker mechanism rendering equal chance of winning, or the builders agree and take turns to bid the minimal value. This may be the equilibrium for builders to maximize their profits.
In an open-bid ascending auction, maintaining collusion is more difficult (but not impossible) because of the need for continuous coordination in multiple bidding rounds.
Also it brings up the question of what is the tiebreaker when builders have the same bid, for both p2p and RPC market place. In the current mev-boost, some relays (ultrasound) only allow outbidding, which means a later bid of the same value as the current highest one will not be forwarded to proposer when calling getHeader. Then mev-boost uses the hash as a tiebreaker for bids of the same value from different relays. One option for ePBS would be the protocol enforces outbidding, a later bid of the same value as the current highest one will be dropped.
If multiple-bid auction, cancellation is needed. But if you are simply asking if builders need such a feature to replace their bids with a lower one, I dont think cancellation is used very often currently in MEV-Boost, 1 or 2 times per auction on average, compared to 30 bids placed. [Cite “Who Wins Ethereum Block Building Auctions and Why”].
2. Do we lose anything in the ePBS market space that is important to maintain from the MEV-Boost market space?
Low latency? A lower latency for builders potentially indicates a higher bid value, as low latency enables builders to include late transactions and update their bids faster. Does it mean that, under the same conditions, the proposers are more incentivized to listen to bids from mev-boost rather than ePBS for potentially a higher bid?

---

**terence** (2024-07-24):

Thanks for the read! I think serious builders may not participate in the P2P market space as much as in the RPC market space. The RPC market space is low-latency, similar to MEV-Boost today. The proposer requests bids from the builder the same way as from the relayer. For RPC, the builder itself may decide whether to host a one-shot auction or a continuous auction. If it’s a one-shot auction, subsequent proposer requests will be met with an error. I generally believe that the P2P market space doesn’t need to be fancy or have many features but should have strong DOS resistance. Its sole purpose is to ensure good liveness and collusion resistance, meaning that if all builders collude at the RPC endpoint, the proposer can still use the P2P endpoint to get a decent bid.

---

**r4f4ss** (2024-07-26):

Thanks for the post.

The researcher entity, that sends bundles to the builder, was not mentioned anywhere and is very important in MEV-boost since they decentralized the exploration of MEV opportunities mitigating negative effects of MEV. Who will be the actor that finds and explores MEV opportunities in ePBS P2P Market Space and ePBS Builder RPC Market Space? Are the buider those who will search MEV opportunities? I just reasoning and asking this question because I have concerns about the centralization of MEV opportunities exploration.

---

**terence** (2024-07-26):

Thanks for reading! epbs doesn’t change the relationship between builders and searchers. Epbs like EIP7732, it only affect the relationship between builders and validators.

---

**boz1** (2024-07-26):

Thanks for the post!

1. In the pull-based RPC market space design, the agency regarding keeping track of the best builders (or, simply, the availability of any builder) shifts to the proposer, who was, in MEV-Boost, only registering with some relays which were then already acting as a multiplexer of builder bids. Isn’t this conflicting with PBS goals?
2. The bluff behavior under the ePBS discussion is interesting. The absence of relays or any governing entity holding the builder responsible for providing the highest available bid could lead to scenarios, as you described, where the colluding validators/builders place inflated bids to invoke others, and the proposer leaves the bluff bids out on purpose. I would guess this could be especially relevant for staking pools that can employ this strategy through their sybils.

---

**syang-ng** (2024-07-27):

Interesting post! A sealed second-price auction in the builder RPC market looks like an ideal mechanism with many good properties. However, given the concerns about proposers’ bluff behaviors, it seems that we need to enforce a common standard here. For example, a proposer must simultaneously request `getHeader` and choose a bid immediately after requesting. Otherwise, a rational proposer will always request `getHeader` to get the current best bid `v` and create a new builder who bids `v-ε`.

The builders may not bid truthfully without a good guarantee provided by the standard; then the mechanism will actually be a first-price auction.

---

**terence** (2024-07-28):

Thanks for reading!

> in MEV-Boost, only registering with some relays which were then already acting as a multiplexer of builder bids. Isn’t this conflicting with PBS goals?

I’m not entirely sure what the goals of PBS are, but it’s important to note that PBS does not necessarily remove the relayer feature. For example, ePBS (EIP-7732) removes the need for trust between the builder and proposer. Currently, they must use a relayer to trust each other, but in ePBS, they may use a relayer. This change moves from a requirement to an option, along with benefits like delayed execution and more. Also, having the proposer track the builder instead of the relayer tracking the builder is much more advantageous. The proposer can easily bypass a poorly performing builder, whereas today, with the relayer in the middle, the proposer can’t bypass a builder directly—only the relayer can, which isn’t ideal. This can lead to missed blocks, similar to the withdrawal root issue we’ve seen recently.

> The absence of relays or any governing entity holding the builder responsible for providing the highest available bid could lead to scenarios,

I think you can use the same bluff strategy today. As a proposer for slot `n+1`, at slot `n`, I could run an anonymous builder and submit a really high bid, hoping others will try to beat it. If my bid wins, I simply don’t use it and instead propose a local block. I don’t think relayers simulate bids.

---

**terence** (2024-07-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/syang-ng/48/16292_2.png) syang-ng:

> A sealed second-price auction in the builder RPC market looks like an ideal mechanism with many good properties

It’s not clear how to implement a sealed second-price auction for builder RPC, given that it’s outside the protocol. The protocol cannot see the second-price bid through RPC, and we need attesters to be able to verify these bids. Here are some strawman ideas:

1. Use the highest price bids from the P2P market: This approach relies on P2P market data for the highest bid. However, it may not always reflect the true market value due to potential discrepancies between P2P and RPC bids. Additionally, it assumes a high level of trust in builders to act competitively and honestly in the P2P environment.
2. Proposer shares the highest price bid with the protocol: The proposer could disclose the highest price bid they received. However, this method risks collusion between the proposer and the builder, which could compromise the fairness of the auction process.
3. Attesters also poll for bids from the RPC market: Attesters could independently verify bids by polling the RPC market. This strategy could deter dishonesty from builders, but it may expose the identity of proposers and attesters, as builders could track the IP addresses involved in these transactions.

---

**syang-ng** (2024-07-28):

I think one goal of PBS is to eliminate the inequality of proposers. But sophisticated proposers in the pull-based RPC market may be good at keeping track of the best builders, giving them higher MEV than home stakers.

There seems to be a tradeoff: If we want to diminish inequality, then it is good to have a relay to achieve this functionality for all proposers. If proposers can do more on their own rather than relying on a centralized relay, it will require the abilities of proposers, which may vary.

---

**terence** (2024-07-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/syang-ng/48/16292_2.png) syang-ng:

> I think one goal of PBS is to eliminate the inequality of proposers. But sophisticated proposers in the pull-based RPC market may be good at keeping track of the best builders, giving them higher MEV than home stakers.

This is no different from MEV-boost today. Proposers are able to discover the best relayers, and in epbs, proposers should be able to discover the best builders or non-censoring builders in the same way. The builder API should be more or less the same

---

**Julian** (2024-07-30):

Thanks for the post! It looks like the post asks two important general questions:

1. To what extent does the protocol need to interfere in the market between the proposer and the builder
2. What is the auction mechanism the protocol should enforce between the proposer and the builder, and

The first question reminds me of [@barnabe](/u/barnabe)’s classic [Seeing like a protocol](https://barnabe.substack.com/p/seeing-like-a-protocol). I think it is clear that the protocol cannot facilitate the optimal market mechanism. First, no one knows what it would be, and innovations like optimistic relaying can greatly change the ecosystem’s view of what is optimal. Secondly, even if the optimal market mechanism were known, it may be hard to implement, or relays could always be incentivized to reduce latency and thereby improve upon the protocol’s market mechanism.

In my view, ePBS moves us in the right direction regarding what kind of market the protocol would want to facilitate, and it relieves some of the relay funding pressure. However, I’m less sure that the specific auction mechanism the current EIP implements will be the final one the protocol adopts. Therefore, I think it’s important not to be too opinionated about the auction design and to be aware that the ecosystem might crowd out the intended auction mechanism and use any gadgets that the protocol facilitates for other use cases.

That said, designing an auction mechanism that allows the builder more freedom makes bidding for the builder easier and less risky, but it is harder for the protocol. Restricting the builder’s bidding strategy space means it is easier for the protocol, but it may also mean that builders are less willing to use the in-protocol market. To me, it makes sense to make this trade-off with potential future market mechanisms in mind. A goal of APS is to prevent timing games so potentially it is more suited to a static (single-bid) auction or it is more suited to a market without cancellations.

Finally, a proposer bluff bidding in its own auction and setting a minimum price for bids to prevent DOS attacks is very similar to setting a reserve price. Min-bid in MEV-Boost attempts to set a reserve price, but the min-bid parameter is private. It could be beneficial to set a public reserve price, as I argue in [this post](https://mirror.xyz/0x03c29504CEcCa30B93FF5774183a1358D41fbeB1/8aCbi_a-Gh5DWnkJWstm8zA5fvtoQB-QR5we7C8XC90).

---

**terence** (2024-07-30):

I agree with everything you’ve said. The way I see this problem, there will always be two market spaces: one is P2P and the other is RPC. RPC is for more serious builders who are expected to win bids most of the time. P2P caters more to long-tail, enthusiastic, and altruistic builders. If I run a validator, I might also run a home builder for fun and try to win bids. This keeps the RPC builders honest and prevents collusion among them. If P2P builders ever become as competitive as RPC builders, there could be a case for getting attesters to come to a consensus on P2P bid values and potentially burn them

---

**Julian** (2024-07-30):

So, is the idea that the protocol would want a P2P market because it prevents collusion amongst builders? Is this not also possible by solely having permissionless access to be a supplier in the RPC market or by setting strategic reserve prices? If we were to move to a form of attester proposer separation (APS), do you think the P2P market will still be necessary in the PBS market? It might not be because you could choose to buy the execution proposing right in the APS market and not sell it.

---

**terence** (2024-07-31):

> the protocol would want a P2P market because it prevents collusion among builders

Correct. Another smaller reason is liveness. If all the RPC builders go away tomorrow proposers could still use p2p bids other than self-build

> permissionless access to be a supplier in the RPC market or by setting strategic reserve prices

I may be wrong here but I think that’s more expensive to boot strap. Gossip a bid to the p2p is nothing comparing to operating a RPC server. It’s a more expensive 1/n trust model assumption

> If we were to move to a form of attester proposer separation (APS), do you think the P2P market will still be necessary in the PBS market?

I don’t think so, at least in the context of execution tickets. It depends on how the bids are being auctioned. If proposers only ask 2-3 builders for bids, it becomes easy for those builders to collude and drive the price down. For ET, if anyone can buy a ticket and the protocol is aware of all tickets in circulation, then it shouldn’t become a problem.

---

**M1kuW1ll** (2024-08-02):

So for the RPC market, I guess we can say the auction starts AFTER the proposer’s request? and only lasts until the proposer selects the winning bid. Because before the request the builders cannot bid for their blocks in RPC market (but can bid in P2P market). Once they receive the request, builders can decide whether to bid one single time (seal-bid auction) or update their bids multiple times (ascending auction) until the proposer selects the winning bid. But ofc during the latency of updating their bids, the proposer might already choose another bid. Under this setting, it seems that the proposer doesn’t have to wait until the beginning of the slot to call a request. They can simply call a request very early, let the builders update their bids, and ultimately choose the highest one around the beginning of the slot, which

sounds like the proposer optimal strategy in RPC market?

Also a bit confused about how to ensure the proposer gets unconditional payment if the execution block is invalid or fails to reveal for both p2p and RPC market.

---

**terence** (2024-08-05):

> Once they receive the request, builders can decide whether to bid one single time (seal-bid auction) or update their bids multiple times (ascending auction) until the proposer selects the winning bid.

This assumes the proposer will continuously poll for builder’s bids and builders will keep returning bids. Builders could, and probably should, refuse any subsequent requests except the first one, or else the proposer could still make builders pay for highest bid. There’s no support for cancellations. The payment is on the consensus layer, not on the execution layer.

> Also a bit confused about how to ensure the proposer gets unconditional payment if the execution block is invalid or fails to reveal for both p2p and RPC market.

Builders are staked on the beacon chain. When a consensus block includes a builder’s bid, the bid amount gets transferred during the processing of the consensus block as part of the state transition function.

