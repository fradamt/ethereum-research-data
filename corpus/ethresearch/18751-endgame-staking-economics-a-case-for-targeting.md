---
source: ethresearch
topic_id: 18751
title: "Endgame Staking Economics: A Case for Targeting"
author: casparschwa
date: "2024-02-22"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/endgame-staking-economics-a-case-for-targeting/18751
views: 15420
likes: 77
posts_count: 37
---

# Endgame Staking Economics: A Case for Targeting

# Endgame Staking Economics: A Case for Targeting

*by [@adietrichs](/u/adietrichs) and [@casparschwa](/u/casparschwa) .*

This post explores the status quo of staking economics, its drawbacks as we see them and what the endgame of staking economics could look like.

Read about our separate proposal for an immediate issuance policy update in Electra [here](https://ethereum-magicians.org/t/electra-issuance-curve-adjustment-proposal/18825).

---

*Many thanks to Anders, Barnabé, Francesco, Julian, Dankrad, Thomas, Vitalik, Mike, Justin, Jon, Nixo, and Sam for feedback and discussions.*

Reviews \neq endorsements. This post expresses opinions of the authors, which may not be shared by reviewers.

---

***tl;dr***

- Today, 30M ETH or 1/4 of all ETH, is staked, with the trend of increasing staking showing no signs of stopping.
- We argue that most of new stake will be driven by LSTs, which gain in money-ness with adoption and time.
- A world in which most of ETH is staked through LSTs has several implications that we consider negative: LSTs have winner-takes-most dynamics due to network effects of liquidity. Economies of scale increase competitive pressure for solo staking viability. Further, a LST replacing ETH as the de facto money of the network (apart from L1 tx fees) leads to Ethereum users being exposed to counterparty risk inherited by the LST by default. For true economic scalability the money of Ethereum should be maximally trustless.
- Today, the issuance yield does not ensure a limit to the amount that can be staked profitably. LSTs have significantly changed the cost structure of staking, making it possible that most ETH will be staked eventually.
- We argue that endgame staking economics should include an issuance policy that targets a range of staking ratios instead, e.g. around 1/4 of all ETH. The intention is to be secure enough but avoid overpaying for security and thereby enabling said negative externalities.
- Finally, we highlight some open research questions that need answering to make a targeting policy feasible.

---

The [figure below](https://dune.com/hildobby/eth2-staking) shows the amount of ETH staked over time. Historically, staking has known one direction: up only. In this post, we put forward arguments for why we think this trend will likely continue, what the negative externalities of it are, and make a case for a path forward to avoid this plausible future.

[![](https://ethresear.ch/uploads/default/optimized/2X/9/9793c373e0ccdd3e3153f61890c3ad4e32f54b7c_2_690x228.jpeg)2920×966 147 KB](https://ethresear.ch/uploads/default/9793c373e0ccdd3e3153f61890c3ad4e32f54b7c)

In short, the current issuance policy allows for all ETH to be eventually staked. This arguably over-secures the protocol and comes with negative externalities. We elaborate why the endgame of staking economics should target a staking ratio range instead. The intention is to provide enough security for the protocol, while limiting the negative externalities of too much stake in the system.

## Current Issuance Policy – where we are & where it’s going

To frame our argument, we reason about what long term equilibria of stake participation are viable under the current issuance policy.

The Ethereum protocol requires some stake participation to secure itself. The demand for stake is very clearly defined in the form of the issuance curve. Given some level of stake participation, the protocol issues some maximum amount of rewards. Instead, the willingness to supply stake varies across ETH holders and is not public knowledge. Hence, we are left to reason about it.

### Demand for Stake – take my ETH and give me security

Ethereum inherits its security from its validators, who stake ETH for the right to earn rewards. The protocol’s demand for security is expressed in its  willingness to issue ETH for validators correctly performing their assigned duties. How much security is sufficient and how much might be too much is discussed [here](https://notes.ethereum.org/@vbuterin/single_slot_finality#Idea-1-super-committees), [here](https://www.reddit.com/r/ethereum/comments/191kke6/comment/kh79gh1/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button) and [here](https://www.reddit.com/r/ethereum/comments/191kke6/comment/kh7do9k/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button) and otherwise beyond the scope of this post.

The Ethereum protocol issues new ETH to recruit ETH holders as stakers. It rewards correct validation according to a fixed issuance curve. Further, validators earn MEV rewards in their role as block proposers. Both sources of yield contribute to the incentive to stake.

[![](https://ethresear.ch/uploads/default/optimized/2X/9/9eef7d49ab13e59680a7b3701628d070f77d91de_2_690x410.png)990×589 39.4 KB](https://ethresear.ch/uploads/default/9eef7d49ab13e59680a7b3701628d070f77d91de)

**Issuance yield** (solid green line). The current issuance yield curve is defined as y=\frac{cF}{\sqrt{ETH\ Staked}} with c\approx 2.6 and F=64 and represents the [maximum issuance yield available](https://github.com/ethereum/annotated-spec/blob/98c63ebcdfee6435e8b2a76e1fca8549722f6336/phase0/beacon-chain.md#rewards-and-penalties-1) for an optimally performing validator [1]. The rewards decrease as staking participation increases – first quickly, then more slowly. The protocol tries to ensure some minimum level of security and thus rewards validators more generously at low levels of staking participation. As more stake secures Ethereum, the marginal value of validators decreases and hence staking rewards are reduced.

**Total staking yield** (dashed green line). It is the sum of (nominal) issuance yield and MEV yield and forms the **demand curve for stake** [2]. MEV yield is exclusively available to validators in their role as block proposers. It is calculated as the annual amount of MEV extracted (~300,000 ETH over last year) over the amount of ETH staked. As a constant amount of MEV is shared by more validators, MEV yield decreases more rapidly than issuance yield, because it does not change with staking levels. The amount of MEV has stayed [remarkably constant over time](https://mevboost.pics/). While this could clearly change, for simplicity we will refer to the demand curve as fixed.

The current issuance curve was chosen over a plethora of reasonable functions. This particular curve conveys two clear messages:

- It deliberately aims to avoid too low staking participation, by paying out very high rewards at low staking levels.
- It suggests diminishing marginal utility for each additional staker, with issuance yield decreasing as staking participation increases.

**However, the issuance curve is *not* intentional about the level of staking participation** it wants to achieve. Notably, there is no mechanism to prevent the staking ratio from exceeding some threshold. In fact, even if the entirety of ETH is staked, the incentive to stake still mounts up to ~2%, favoring those who stake over those who do not. While the issuance curve subtly suggests that the value of each additional staker diminishes, the protocol does not exert fine control over the eventual staking ratio reached. Essentially, beyond ensuring minimum security through initial high incentives, the protocol doesn’t encourage an optimal range of staking levels.

Note that the issuance yield depicted above is *nominal* yield. It does not account for the dilution that takes place as more ETH is issued. The relevance of this dilution effect increases as more ETH is staked. However, as it affects both staked and unstaked ETH equally, it does not affect the net incentive to stake (i.e. the yield gap between holding raw ETH and staking it). We can therefore ignore dilution in this analysis for now – we will get back to it at a later point in this article.

### Supply Side – give me ETH and have my stake

Having explored the demand for stake, we now turn our attention to the supply side. The supply curve represents the willingness of ETH holders to stake at different staking yields, indicating the necessary incentives for each stake participation level. This curve typically slopes upwards, suggesting that higher staking participation levels require greater incentives. However, since the willingness to stake cannot directly be observed or measured, the exact shape of the supply curve remains unknown, only allowing for qualitative assessments.

In addition, the supply curve is not fixed over time. In the following sections we will illustrate how staking costs change over time, and such changes naturally impact the level at which ETH holders need to be incentivized to stake – in other words, they shift the supply curve.

The only direct observations of the supply curve that we do have are the historical staking levels. These represent the intersection between demand and supply curve at any given moment in time, and with the demand curve known, this gives us certain knowledge of a single point of the supply curve for each historical moment of the beacon chain, up to and including today.

As the first graph illustrated, the total amount of staked ETH has continued to grow since the launch of the Beacon Chain. Given the demand curve has remained constant [3], it then follows that this growth in ETH staked is due to a downward shift of the supply curve. In other words, this indicates that the willingness among ETH holders to participate in staking has increased – even at today’s lower issuance yield levels. The following graph illustrates this trend by sketching out plausible shapes of historical short term supply curves:

[![](https://ethresear.ch/uploads/default/optimized/2X/2/27e427ad234d88918368a5a2e56389fc6f4ae653_2_690x416.jpeg)2706×1634 207 KB](https://ethresear.ch/uploads/default/27e427ad234d88918368a5a2e56389fc6f4ae653)

Just looking at this historical trend, it is clear that for the near-term future, a continued downward shift of the supply curve and thus a continued net inflow of stake is reasonable to expect. However, the more interesting questions are those about the potential long term staking equilibria. To be able to make informed assessments here, we need to have a closer look at the composition of the supply side.

The decision for any ETH holder to stake depends on two things: The incentives provided to stake (total staking yield = issuance yield + MEV yield) and the costs of staking. While the former is relatively homogenous across stakers [4], the cost structure fundamentally varies for different staker types. In the following we contrast solo stakers and staking service providers.

#### Solo Staking vs. Staking Service Providers (SSPs)

Staking Service Providers (SSPs) receive ETH from their users and stake it for them, charging a fee for their service. In most cases, they give users [liquid staking tokens](https://mirror.xyz/barnabe.eth/v7W2CsSVYW6I_9bbHFDqvqShQ6gTX3weAtwkaVAzAL4) (LSTs) as a receipt for their ETH. An LST is fungible and can be freely used and traded. The extent to which this liquidity is useful for it’s holder varies among LSTs and is a function of overall adoption and support by third-party protocols for a given LST. In the following we will only talk about LST-issuing SSPs - those that do not issue LSTs can be considered as a special case of LSTs with zero liquidity value.

**Solo staking is trustless, but illiquid and inconvenient; liquid staking requires varying degrees of trust but is very convenient and importantly liquid.**

|  | Solo Staking | SSPs |
| --- | --- | --- |
| Costs | High fixed costs: hardware + setup effort. additional variable costs (internet connection, electricity, etc.) | Variable costs: SSPs typically take a cut of validator rewards (e.g., 10%, 14%, 25%,…) |
| Risks / trust assumptions | Trust your own node operation | Node operator risk + smart contract / legal risks + governance risks [5] |
| Convenience | Requires technical skills for setup and ongoing maintenance. | Offers a simple, one-click solution to earn yield. |
| Liquidity | Limited (to restaking); ETH is locked in the deposit contract. | Varying, but potentially high; LSTs are widely integrated in various protocols, enabling liquidity and revenue streams. |

Comparing these two staking types suggests two main conclusions, relevant to the supply discussion:

1. The cost structure for solo staking is heterogeneous across  ETH holders. The technical skill required, the variation in local cost for hardware and ongoing resources, and the difference in confidence in successful safeguarding of the ETH at stake, all contribute to a relatively steep supply curve for solo stakers. Without major improvements in solo staking UX, the pool of possible solo stakers at anything close to current issuance levels is likely mostly depleted.
2. In contrast, the cost structure for SSPs is much more homogeneous across ETH holders, with variation mostly in the assessment of operator risk and the LST-vs-ETH liquidity penalty. As a result, the SSP supply curve is considerably flatter, meaning that the issuance required to recruit more ETH holders as liquid stakers, only increases slowly.

In addition, the cost of solo staking remains independent of the level of staking participation, whereas the cost of holding LSTs will likely go down over time and with increased adoption:

- Money-ness of LSTs increases. As one LST becomes more popular, it can be expected to be supported by more and more projects in addition to native ETH (e.g. more defi integrations, L2s starting to liquid-stake bridged ETH by default). With a sufficiently high staking ratio, the winning LST could eventually even surpass the remaining unstaked ETH in available volume, completely closing (and potentially even flipping) the gap in liquidity.
- Smart contract risk decreases: “battle tested”, formal verification,  etc.
- Governance systems improve their robustness, e.g. this proposal.
- Perceived tail risks of mass slashing might decrease. Any LST scaling to subsume a significant portion of the overall ETH in existence could reasonably create a too-big-to-fail impression, where users expect a protocol bailout in case of failure, effectively driving down their perceived operator risk to 0.
- SSPs can offer lower fees to break even at higher staking ratios.

In summary, this suggests that the supply curve is significantly flattened by SSPs and LSTs in particular, meaning the incentives required to attract additional staking do not need to increase substantially as the total amount of staked ETH grows. **A continued future increase of stake driven by liquid staking can be expected.** But just how much more ETH will be staked in the long run?

### Long term equilibria – are we gonna keep staking or what?

We now put together the demand and supply considerations to reason about possible long term staking equilibria.

We argued that the demand curve is very opinionated for low staking participation but otherwise leaves it relatively open what staking ratios might be reached in the long run.

We then explained the dynamic of downward shifting supply curves over time, as the costs and risks of staking continue to decrease. The resulting new net inflow of stake will mostly flow towards LSTs. In particular, it is unclear whether the supply curve would be steep enough to set practical limits to staking participation.

Thus, there is a broad range of possible equilibria for the overall staking ratio, with ratios close to one among the plausible outcomes. The following sketch illustrates how even relatively small differences in the (hypothetical) long term equilibrium supply curve can lead to very different outcomes:

[![](https://ethresear.ch/uploads/default/optimized/2X/5/5170aa5cfe0e427a1126d32e857d2bc9c016893b_2_690x412.jpeg)2724×1628 211 KB](https://ethresear.ch/uploads/default/5170aa5cfe0e427a1126d32e857d2bc9c016893b)

**The key take-away is not that staking participation levels will *necessarily* be high, but that such high levels are *plausible*.**

With this in mind, we now detail our concerns around high staking ratios, before presenting possible changes to the issuance policy preventing these.

## Staking Ratio – when is less stake more?

With ~30 million ETH staked from a total supply of ~120 million, the staking ratio s is defined as \frac{ETH\ Staked}{Total\ Supply\ of\ ETH} and stands at \frac{1}{4}.

Before diving into the concerns we see for high staking ratio regimes, we again point to [some references](https://notes.ethereum.org/@vbuterin/single_slot_finality#Idea-1-super-committees), discussing [what level of stake participation](https://www.reddit.com/r/ethereum/comments/191kke6/comment/kh79gh1/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button) might be [secure enough](https://www.reddit.com/r/ethereum/comments/191kke6/comment/kh7do9k/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button). In short, current staking levels are arguably sufficiently secure. This then raises the question - if we don’t need it for security, should we be okay with staking participation sufficiently higher than today?

We argue that high staking ratio regimes come with negative externalities that affect ETH holders, (solo) stakers, as well as the protocol itself.

### Network Effects of Money (LSTs) – no thanks to forced risk taking

- LSTs compete on money-ness with winner-takes-most if not all dynamics due to network effects. As a LST is more widely used, it becomes more useful driving further adoption. The money-ness of LSTs increases in aspects such as degree of integrations (on- and offchain), trading liquidity, resilience against governance/legal attacks, etc.
- In a high staking ratio regime in which one SSP controls most stake, the LST may be considered too-big-to-fail. Is it a credible threat to slash, if a majority of all ETH in existence would be affected? More generally, the governance of such a dominant SSP would de facto become a part of the protocol, without being accountable to all Ethereum users.
- In a world in which most existing ETH is liquid-staked, the de facto money of Ethereum for most use cases besides L1 transaction fees will be some LST(s). All LSTs, be they issued by an ETF, centralized exchange or onchain staking pool, come with different trust assumptions – some worse than others. But ultimately Ethereum users will end up holding LSTs, economically quasi-forced to expose themselves to those added risks (operator/governance/legal/smart contract/etc. risk). Is this desirable for Ethereum users? Further, such intermediated ETH is worse collateral. For true economic scalability, the money of Ethereum needs to be maximally trustless: ETH.

### Minimum Viable Issuance – in it for the UX

- Minimum viable issuance as a guiding principle suggests enough staking participation to be sufficiently secure, but not more. There comes a staking level beyond which the protocol is secure enough and the marginal utility of a staker turns negative (networking load increases, ETH holder dilution, etc.).
- Ethereum users should not have to concern themselves with the complexities of staking to prevent their ETH holdings from getting diluted. Staking is a service that the protocol requires and pays for, but it should not be economically quasi-forced upon all its users.
- More issuance implies more dilution for all ETH holders and stakers. However, SSPs are shielded from this downside. They don’t hold the ETH that underlies the staked position, but instead derive their revenue from SSP fees that they charge for their services, which naturally increase for higher staking ratios.
- At a hypothetical staking participation level of 90% with 2% yield, assuming a liquid staking share of 90% and an average SSP fee of 10%, 0.16% of Ethereum’s market cap, or ~200,000 ETH, or ~530 million USD at current prices, are paid in SSP fees every year – a de facto tax on all ETH holders.

### Real Yield – the real deal

As we discussed in the beginning of the article, the nominal yield for stakers from issuance is progressively diluted with higher staking participation. To adjust for this effect, it is useful to look at the real staking yield.

**Real yield is nominal yield adjusted for the dilution effects of ETH issuance [6].**

[![](https://ethresear.ch/uploads/default/optimized/2X/8/8689c311763db0aecdf7a231b6b0e7af3ebb48af_2_690x414.png)6000×3600 617 KB](https://ethresear.ch/uploads/default/8689c311763db0aecdf7a231b6b0e7af3ebb48af)

The graph depicts the impact of dilution on yield for both stakers and non-staking ETH holders. For ETH holders (red line) this implicit yield is of course negative, as their nominal balance remains unchanged, while they are exposed to the same dilution effect as stakers. To better characterize the impact of this effect, we can broadly distinguish between two different staking ratio (s) regimes:

- On the left, for low s, the real yield curves relatively closely resemble the nominal yield curves we previously examined. With few stakers the total amount of new ETH minted is respectively small, resulting in only a small dilution effect. The net incentive to stake is made up primarily by the positive yield available to stakers – or visually it’s mostly green.
- On the right, for high s, the real issuance yield diverges more strongly from the nominal yield curves. With an increased number of stakers earning validator rewards, total ETH issuance is higher, leading to this more noticeable dilution effect. Besides the diminished real yield, a significant portion of the net staking incentive now derives from “dilution protection”, essentially the avoidance of losses that would be incurred by passively holding ETH. In the extreme, as the staking ratio approaches 1, real total staking yield only consists of MEV yield.

The shifting composition of the net incentive to stake is a fundamental area of distinction between the two staking ratio regimes. At this point, we want to stress that this composition does not change the effectiveness of the incentive to stake. In other words, dilution protection incentivizes stakers just as much as real staking yields!

What does change though is the desirability of the outcome resulting from that incentive. For low s, staking is a profitable service paid for by the protocol. But for high s, staking loses its profitability and instead becomes an unpleasant necessity to avoid losses from passively holding ETH. Thus, by allowing the staking ratio to “slide to the right”, we risk ending up in the worst of all worlds: Staking becomes a necessary indirection layer, exposing minimal real yield, but threatening dilution for those opting out of accepting LST trust assumptions.

If you give a staker the choice between living in some equilibrium (a) or equilibrium (b) for different issuance policies, this staker, assuming they would stake in both equilibria, would prefer the equilibrium paying higher real staking yield. For obvious reasons a staker cannot “choose” an equilibrium, but the protocol issuance curve effectively determines which equilibrium is reached (given some fixed long term supply curve). Higher issuance is associated with more nominal yield, but importantly, **more nominal yield does not imply more real yield.**

### Solo Staking Viability – down bad

- SSPs with fixed costs naturally benefit from economies of scale, allowing them to operate more profitably (or charge lower fees) as they have more ETH under management. Successful SSPs might be viewed as too-big-to-fail, reducing their perceived tail risks and further contributing to such scale effects. In contrast, solo staking comes with per-staker costs that do not decrease (rather even slightly increasing with networking load!) as the total amount of stake grows. In fact, EIP-7514 was in part merged for this reason.
- As a larger share of issuance goes towards “dilution protection” and no longer contributes to real yield, stakers are left with more and more of their remaining real yield coming from MEV. This yield is by its nature highly variable, which leads to increased volatility of real total yield for solo stakers. For SSPs on the other hand this MEV income is smoothed over all validators they operate, removing staking yield volatility as a concern for them.
- The liquidity gap between solo staking and LSTs widens with increased adoption and moneyness of LSTs. Put differently, the competitive disadvantage of solo staking relative to liquid staking increases as the staking ratio increases.
- In many jurisdictions, the basis for government taxes on staking income is the nominal income, not the real income adjusted for dilution effects. LSTs can be structured in a way to shield holders from this effect, while for solo stakers this is usually not possible. This further increases the profitability gap as the difference between nominal yield and dilution-adjusted real yield widens.

### Discussion

The considerations above lead us to argue for the following:

1. Holding raw ETH should be economically feasible, to ensure user friendliness and preventing dilution beyond ensuring sufficient security.
2. For true economic scalability, Ethereum’s de facto money should be maximally trustless [7].
3. An outcome with most of the incentive to stake coming from dilution protection is undesirable for both stakers and ETH holders.
4. High staking participation worsens the competitive disadvantage of solo staking.

Ethereum’s future staking ratio is uncertain; however, the absence of control over maximum staking levels warrants a proactive approach in determining optimal levels. Even if high staking ratios may be preferable to some, it should then be a deliberate choice, not an accidental result of exogenous market dynamics.

The following sections are concerned with proposing alternative issuance policies.

## Stake Ratio Targeting – endgame staking economics

An endgame staking policy for Ethereum should target a staking *ratio*, rather than a fixed quantity of staked ETH. This approach ensures accounting for the variable supply of ETH, which changes over time due to EIP-1559 and issuance. In practice, the total supply of ETH currently changes so slowly ([-0.3% per year since the merge](https://ultrasound.money/)) that this distinction [does not matter in the medium term](https://x.com/weboftrees/status/1710725744651825281?s=20). However, the intention of an endgame policy is to not require adjustments, even over longer time horizons.

As discussed, while the current issuance curve is designed to ensure a minimum level of staking, it lacks a mechanism to cap staking at an upper bound, potentially resulting in high staking ratios. We argue that a robust endgame issuance policy should express desired staking participation levels by implementing controls on both the lower and upper bounds of staking ratio. Specifically, it should aim to maintain staking ratios within a defined optimal range that reflects the network’s security requirements without enabling negative externalities further.

The protocol can express strong opinions for “too-low” and “too-high” staking ratios alike, by issuing very high or low rewards (possibly also negative) respectively. By doing so the protocol regains control over its level of staking participation. To illustrate the existence of a curve with such properties consider the following plot, which is close to [Vitalik’s curve here](https://notes.ethereum.org/@vbuterin/single_slot_finality#Economic-capping-of-total-deposits).

[![](https://ethresear.ch/uploads/default/optimized/2X/9/98e71ac5ab43b5b226fcfe68475d435b8eb4cb62_2_690x414.png)6000×3600 475 KB](https://ethresear.ch/uploads/default/98e71ac5ab43b5b226fcfe68475d435b8eb4cb62)

In this plot we observe that for low amounts of staking participation the issuance curve rewards generously, similarly to today’s issuance policy. As stake levels increase, issuance yield tapers off and finally turns negative. That way, staking becomes increasingly disincentivized, until it even becomes more profitable to hold ETH than to stake it. In practice, this range of negative total staking yields would not be maintained, with staking participation finding a lower equilibrium. Thus, any curve of such shape would give strong guarantees for the range of viable staking ratios.

Practically it might not be necessary to choose a curve which turns negative so abruptly to achieve similar range targeting properties. In fact, curves that bring issuance rewards down to (or close to) zero beyond some point might even be sufficient for that purpose.

### Implications of Targeting

The main advantage of targeting is that it prevents all of the negative aspects of a high staking ratio regime enumerated in the section above. The notable exception to this is the [concern around reward variability for solo stakers](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448#h-14-consensus-incentives-6). Like in the high staking ratio regime, under targeting the share of real yield coming from MEV is also higher than today. A downside of a move to targeting is thus an  acceleration of this (already existing) dynamic. However, this increased variance can be mitigated through MEV capture mechanisms such as [Execution Tickets](https://ethresear.ch/t/execution-tickets/17944) or [MEV Burn](https://ethresear.ch/t/mev-burn-a-simple-design/15590), or instead by introducing a [staking fee](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448#h-3-consensus-incentives-11).

One criticism sometimes brought forward against targeting is that it reduces the overall equilibrium yield, thus worsening the existing competitive pressure between solo staking and SSPs, as well as across different types of SSPs. The idea here is that when there is more money to go around, slightly less competitive forms of staking that might be desirable for the protocol have an easier time staying profitable. To address this concern, the distinction between nominal and real yield is crucial. A move to targeting unquestionably reduces nominal yields when compared to the equilibrium that would otherwise be reached in the long run. However, the same is not generally true about real yield, which is what really matters, as the following sketches illustrate.

[![](https://ethresear.ch/uploads/default/optimized/2X/b/b7ad05197fc1fd9d3a8feaa68933e3ec0d46c9b6_2_690x210.jpeg)3533×1077 316 KB](https://ethresear.ch/uploads/default/b7ad05197fc1fd9d3a8feaa68933e3ec0d46c9b6)

The left graph depicts a plausible example for a long term equilibrium under targeting, the right graph similarly an example using today’s issuance curve. Crucially, both examples use the same hypothetical long term supply curve, allowing for a comparison of outcomes. As one can see, the chosen example would in the non-targeting case lead to a high staking participation of around 100M ETH. At that level, most of the staking incentive comes from dilution protection, with a real yield of only around 0.5%. Conversely, under targeting, the same example leads to an equilibrium with lower nominal yield, but little dilution and thus a real yield of around 1.4%.

This example illustrates how targeting can plausibly lead to significantly higher real yield levels than the equivalent outcome under the current system. To the extent that yield levels indeed matter for intensity of competition among different staking types, targeting can thus help prevent a near-zero outcome for real yield. It should be noted here that this is not only beneficial under the aspect of competitive pressure – keeping staking profitable is beneficial for stakers of all types. Moreover, it also benefits non-staking ETH holders, by minimizing the dilution they are exposed to.

### Open Questions

This article advocates for the general principle of stake participation targeting. To move to an actual specification that could then be implemented on Ethereum, there are still several open questions that need to be addressed. In closing, we want to briefly touch on each of these questions.

#### What is the desirable range for stake participation?

We have deliberately only talked about undesirable ranges, but never specified a precise and desirable range. This is because it is inherently hard to objectively reason about it and needs to be discussed more broadly in the community. The main tradeoff is that little stake participation leaves the protocol open to cheap attacks, while too much staking creates negative externalities as discussed in earlier sections. We once again link to some preliminary discussion on the topic by [Vitalik](https://notes.ethereum.org/@vbuterin/single_slot_finality#Idea-1-super-committees), [Vitalik](https://www.reddit.com/r/ethereum/comments/191kke6/comment/kh7do9k/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button), and [Justin](https://www.reddit.com/r/ethereum/comments/191kke6/comment/kh79gh1/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button). One helpful way to model the decision is by considering the utility of different staking ratios. One possible example for such a utility curve is sketched below.

[![](https://ethresear.ch/uploads/default/optimized/2X/6/65ce183d44af120fc475555bb02566bfef8ddbe2_2_690x371.jpeg)3017×1623 102 KB](https://ethresear.ch/uploads/default/65ce183d44af120fc475555bb02566bfef8ddbe2)

#### How to pick a suitable issuance curve, given some target range?

Once a target range is picked, there is still a wide design space of possible issuance curves, that could be chosen to achieve the specified goals. Further work is necessary to compare the possible choices and pick the best candidate. In addition, alternative targeting mechanisms, such as an EIP-1559-like feedback controller, should continue to be explored.

#### How to ensure incentive compatibility of consensus duties for close-to-zero or negative issuance?

The purpose of issuance is to reward the correct performance of validators fulfilling their consensus duties. However, under a targeting policy it might be possible for issuance yield to approach zero or even turn negative. A validator might still be incentivized to stake with issuance levels approaching zero or less, for the possibility to capture MEV. However, with no issuance it is rational for a validator to not fulfill all consensus duties. This goes to show that for low issuance levels consensus incentives risk breaking down. To mitigate this, the protocol could charge a fee for the right to validate (and again reward correct participation). This reestablishes incentive compatibility. However, this adds protocol and implementation complexity, of which the details need to be figured out.

#### How to remove the reward volatility introduced by MEV?

As mentioned before, the mitigation of increased reward volatility is important for solo staking viability and can be achieved through MEV capture mechanisms such as [Execution Tickets](https://ethresear.ch/t/execution-tickets/17944) or [MEV Burn](https://ethresear.ch/t/mev-burn-a-simple-design/15590), or instead by introducing a fee for validators, as per discussion above. While shipping targeting with one of these solutions already in place would be preferable, in principle this is not a strict dependency.

#### How to set the target in relative (staking ratio) instead of absolute (fixed ETH amount) terms?

A targeting policy could of course also target a fixed amount of ETH, e.g. 30M ETH. But for future-proofing the issuance policy it is preferable to directly target a staking ratio instead, e.g. \frac{1}{4}. For the issuance policy to target some staking *ratios* the consensus layer needs to be aware of the amount of stake and supply of ETH. The latter is currently not the case, but could be achieved in a simple two-fork process:

- Fork (1): Start tracking supply changes relative to the time of fork (1).
- Fork (2): Add total supply of ETH at time of fork (1). This together with the ongoing tracking of supply changes since fork (1), gives a running total supply of ETH.

#### How to transition to a targeting mechanism, when starting with  stake participation levels beyond the target range?

The simplest way to transition to a targeting policy is to of course start within the target staking range. However, in the likely scenario that the target range will be surpassed before the transition, this would necessitate a decrease in staking participation. Even with a gradual easing into the new curve, this would in practice entail a significant period, during which stakers would be insufficiently compensated, until the excess stake can exit. It remains an open question how to minimize the adverse impacts on stakers of such a transition.

## Conclusion

We discussed the current issuance policy, explained negative externalities as we see them, and elaborated what a path forward could look like. In particular, we suggest targeting a range of staking ratios. However, given the open questions, and in particular the lack of a validator fee mechanism and/or in-protocol MEV capture mechanism, moving to a targeting policy will take time. In the meantime we should update the issuance policy, a stepping stone towards targeting. We make a case for a proposal to update the issuance policy in the upcoming network upgrade Electra [here](https://ethereum-magicians.org/t/electra-issuance-curve-adjustment-proposal/18825).

---

## Footnotes

[1] [on aggregate the network operates at ~97% effectiveness](https://www.rated.network/?network=mainnet&view=pool&timeWindow=1d&page=1&poolType=all)

[2] Read more about why issuance yield and MEV yield together form the demand curve in section 2.1 [here](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448#h-2-equilibrium-staking-8).

[3] We want to reiterate that issuance yield and MEV yield together [form](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448#h-2-equilibrium-staking-8) the demand curve. Further, we make the simplifying assumption that MEV remains constant over time. While historically roughly true, this could of course change.

[4] The performance across validators varies, both in terms of earning issuance rewards (consensus duties) and MEV rewards. However, this [variability](https://www.rated.network/?network=mainnet&view=nodeOperator&timeWindow=1d&page=1) is relatively small and its discussion beyond the scope of this post.

[5] Read [this discussion](https://notes.ethereum.org/@mikeneuder/magnitude-and-direction#Explicit-attacks) for an analysis of risks for one such onchain SSP.

[6] We analyze these yields in isolation, in particular we do not consider the tx fee burn mechanism ([EIP 1559](https://notes.ethereum.org/@vbuterin/eip-1559-faq)). The underlying analysis would remain unchanged nonetheless, as *all* yield curves would be shifted up- or downwards by some constant amount, independent of the staking level. We simply wish to reason about an ETH holder’s decision to stake or not to stake and for that only the difference in yields is relevant.

[7] The asset ETH is more trustless than staked ETH for the slashing risk alone and then of course there is a spectrum of trust required across different SSPs.

## Replies

**PhABC** (2024-02-22):

Interesting proposal, thanks for the indepth post.

You argue that higher staking ratio is more favorable to LSTs, however I think you can say the same about low yields too. I worry that solo stakers will be the first to unstake if yields go to 0, since solo staking has significantly more costs. While we may very well be heading to 100% staking ratio due to LSTs, it seems like this proposal would accelerate the death of solo stakers. It is also possible that solo staking becomes more accessible over time, so there is a good argument to keep solo stakers “viable” for a longer period of time.

---

**fradamt** (2024-02-22):

Solo staking costs are mostly upfront, and current solo stakers have already paid them. It seems to me that one could reasonably expect many of them to stick around.

On the other end, can we really expect there to be many remaining “future solo stakers”, which haven’t staked yet but might stake at some point with no issuance reduction but not if the issuance is reduced? What do you think about this argument?

![](https://ethresear.ch/user_avatar/ethresear.ch/casparschwa/48/3001_2.png) casparschwa:

> The cost structure for solo staking is heterogeneous across ETH holders. The technical skill required, the variation in local cost for hardware and ongoing resources, and the difference in confidence in successful safeguarding of the ETH at stake, all contribute to a relatively steep supply curve for solo stakers. Without major improvements in solo staking UX, the pool of possible solo stakers at anything close to current issuance levels is likely mostly depleted.

---

**alonmuroch** (2024-02-22):

Feels like the jump from “this level is ok” to this level hurts ethereum and solo stakers to be not well explained.

Also, a world in which we have multi “winning” LSTs is definitely possible … we are seeing it now with some emerging LSTs/ LRTs and EigenLayer native restaking.

---

**nixorokish** (2024-02-22):

Solo stakers, maybe not. Home stakers, yes I do think so. For some color, EthStaker is running a DVT home staker program right now and we received a lot of applications from technically-inclined people working in the industry who just wanted to be walked through the process. The perception of difficulty around home staking seems to be much more than the actual difficulty.

And though the costs are mostly upfront, (for solo stakers) it’s still a lot of capital locked into a place where the entire point is generating yield. So if the issuance goes near zero or negative and they choose to move the capital elsewhere, they’ll likely shut down the machine. If it ever becomes profitable again, it requires doing all the same research, determining if they need upgraded hardware, restarting a process that they likely only did once and so it’s not much easier the second time around. I definitely could see a sudden shift downward permanently depleting the percentage of solo stakers on the network.

---

**PhABC** (2024-02-22):

Indeed. When I referred to cost I was not even thinking of hardware required or rental, but about the overhead of ensuring 24/7 uptime to avoid penalties. Most people aren’t devops engineers. At 5% yield you can afford a few mistakes, but not at 0.5%.

---

**theSamPadilla** (2024-02-22):

Very thoughtful post. Thanks for that.

This, however, strikes me as incentivizing the exact opposite of what this is trying to achieve. Asymptotically reducing staking incentives after a given staking ratio is likely to hurt solo stakers before it hurst LST stakers.

Set aside infra, capital requirements, and knowledge needed to run a solo validator. I think this boils down to (lack of) liquidity. The sacrifice solo stakers make when validating is lockng up their ETH in contract. LSTs don’t make this sacrifice, they still had their LST that they can use on DeFi, borrow against, lend, or immediately exit at any point in time. In a future where the value of holding your ETH excels the rewards, I don’t necessarily see it hurting LSTs, if you assume the 1:1 parity of :ETH will hold.

If anything, this would deincentivize existing solo stakers from continuing to stake. And the downsize in staking ratio will likely come from solo stakers. The incentive for multiple LST stakers to collectively withdraw their ETH does not seem obvious to me. They would not hurt, they are liquid.

---

**benaadams** (2024-02-22):

Won’t this push people away from accutally staking and towards LSTs so they can then restake to make up the missing yield?

---

**0xemperor** (2024-02-23):

Thanks for the great post.

Maybe this is from a place of naivete, but if the underlying worry is a single tbtf (too big to fail) LST, then a native staking approach might be a higher priority to explore right? The issuance ultimately is a value that reflects the networks’ willingness to pay for its own security, which coupled with the burn has actually resulted in a negative issuance since the merge overall. Is there not a risk of overtuning this, and underpaying?

Also, in a second-order effect, restaking should be considered when thinking of staking economics. This is the stake that secures ethereum that also secures an AVS, in essence, you could say this stake is “less secure” for the base layer. One, if we target a stake percentage, and most of it gets restaked isn’t that dangerous to the base layer? Two, if the issuance is reduced, isn’t it more likely that the targeted stake all get restaked so people retain the same staking return? In a world where we overload the security of the network with additional terms, is it really valid to say we are oversecuring the network? Today almost ~10% of all staked eth is already restaked in eigenlayer.

---

**MicahZoltu** (2024-02-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/thesampadilla/48/15356_2.png) theSamPadilla:

> The sacrifice solo stakers make when validating is lockng up their ETH in contract.

What is the current time required to withdraw staked ETH (given current withdraw queues and whatnot)?  Knowing this would help analyze the time-value-of-money cost to low-liquidity stakers.

---

**MicahZoltu** (2024-02-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/0xemperor/48/13285_2.png) 0xemperor:

> Also, in a second-order effect, restaking should be considered when thinking of staking economics. This is the stake that secures ethereum that also secures an AVS

Restaked ETH does *not* secure Ethereum, generally speaking.

For any given amount of stake to be *actually* securing Ethereum, the actor that is taking on the capital risk of staking failure/chain split **MUST** be the same actor that is making decisions about what algorithm (client) to run.  As soon as you either outsource algorithm choice to someone else or you sell the risk to someone else the game theory for staking falls apart and your “stake” needs to be treated as attacker controlled stake for mechanism design calculations.

![](https://ethresear.ch/user_avatar/ethresear.ch/0xemperor/48/13285_2.png) 0xemperor:

> if the underlying worry is a single tbtf (too big to fail) LST

The above game theory issue is the reason why solo staking is so important.  There is no such thing as “too big to fail”.  We can wipe out 99% of stake and everything will be fine as long as the wiped out stake is of people who chose the wrong algorithm (e.g., chose a super-majority client, or a censoring client).  There will be a long period (weeks) of no finality during recovery, but the system is designed to self heal from nearly all staked ETH defecting.

---

**barnabe** (2024-02-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Restaked ETH does not secure Ethereum, generally speaking.

I disagree here, it is much more nuanced and 10% ETH being re-staked does not mean Ethereum is 10% less secure. You may have principal-agent relationships (in fact you *will* have such relationships) between operators and delegators, and some of the capital at stake may also be burdened with other conditions, all of this is important to consider the security of Ethereum, not only the worst-case pessimistic view.

![](https://ethresear.ch/user_avatar/ethresear.ch/0xemperor/48/13285_2.png) 0xemperor:

> In a world where we overload the security of the network with additional terms, is it really valid to say we are oversecuring the network?

Something that could happen is a large EigenLayer slashing event, in which case the first-order consequence is a reduction of the “dollar-amount” security of Ethereum ([as long as EigenLayer slashings are properly surfaced to the protocol](https://ethresear.ch/t/unbundling-pbs-towards-protocol-enforced-proposer-commitments-pepc/13879#in-protocol-eigenlayer-ip-eigenlayer-1), which is the point of [EIP-7002](https://eips.ethereum.org/EIPS/eip-7002) for instance). Since lots of validators are exited, the consensus-offered yield will decrease, inciting more validators to join the staking set and recovering the equilibrium staking ratio.

A bit of weirdness may happen during the transition, but is in my opinion mitigated by the following. Let’s say an adversary wants to benefit from the temporary lower amount of stake after a large EigenLayer slashing event. There can be two cases. If the adversary is the one to trigger the large slashing event, then its own stake will be penalised and exited from Ethereum, largely preventing them from pursuing an attack on Ethereum (e.g., a safety fault). If the adversary is not the one, then it cannot really predict in advance that a large slashing event will happen, it needs to command a large enough amount of (non-EigenLayer-encumbered) stake to launch the attack as soon as the slashing event happens. At the end of the day, the bounds provided to us by the theory of consensus are binding: If we have an adversary with 1/3+ of the total *active* stake, a safety fault of FFG is possible in theory.

---

**MicahZoltu** (2024-02-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/barnabe/48/4742_2.png) barnabe:

> I disagree here, it is much more nuanced and 10% ETH being re-staked does not mean Ethereum is 10% less secure. You may have principal-agent relationships (in fact you will have such relationships) between operators and delegators, and some of the capital at stake may also be burdened with other conditions, all of this is important to consider the security of Ethereum, not only the worst-case pessimistic view.

One can certainly try to model the system with cow shaped cows rather than spherical cows, but things get *really* hard and *really* complicated *really* fast.  In general, I think when designing systems we should focus on designing a system that is resilient to the worst case scenario with rational actors rather than *hoping* that we get all of the numbers right for the fuzzy and hard to calculate things.

If I am accepting delegated stake and operating a node, and in return I earn say 1 ETH over 10 years for doing so, if an attacker offers me 1 ETH *today* in exchange for running their software instead of canonical software, the rational decision (with spherical cows) is to take it.  Of course, there are fuzzy things like threats of violence (legal risks) and reputational damage that I perhaps should think about, but we have no way of measuring those things accurately.  How much do the operators of some random delegate value their reputation?  What if their reputation is already in the gutter for unrelated reasons?  What if they operate anonymously?  What if they live in a country where bribing law enforcement is cheap and easy?

Even if you can accurately estimate (or at least put some bounds on) things like legal/reputational risks and reasonably convert those into ETH denominated numbers, adding complexity to the system can cause a complexity explosion that ends up with subtle bugs in the mechanism design.  Take Bitcoin for example, where the economic incentive system is stupidly simple.  Yet it wasn’t until sometime after its launch that people realized selfish mining attacks were profitable in a transaction-fee-only future.  This is a very subtle attack that was discovered years later despite the system being trivial to analyze.  The situation is far worse when your system is not trivial to analyze, which is the case when we start treating restaked ETH as anything other than “attacker ETH”.

---

**barnabe** (2024-02-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> In general, I think when designing systems we should focus on designing a system that is resilient to the worst case scenario with rational actors rather than hoping that we get all of the numbers right for the fuzzy and hard to calculate things.

Note that these proposals are not actually hoping to “get all of the numbers right”, they are quite agnostic to the ratio between “true operator stake” and “delegated stake” or “re-staked stake”, they simply reason out about the aggregate size of the staking set. Scaling the staking set size by 2x may mean that you get 2x the dollar amount of “true operator stake”, but also may not (e.g., larger staking set => more LST network effects => more incentives to delegate to LSPs). Either ways, there are indeed risks of misalignments between principals and agents, but these risks have more to do with staking UX (by which I mean broadly the set of mechanisms that are in place in- and out-of-protocol between stakers and the protocol) than with the current discussion. To be clear, these mechanisms are important and they help us improve the quality of our staking set, which is a necessary condition to me (see [recent post](https://ethresear.ch/t/unbundling-staking-towards-rainbow-staking/18683)), but not sufficient to achieve sustainable staking conditions.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> selfish mining attacks were profitable in a transaction-fee-only future

This is besides the point but selfish mining attacks are also profitable in a block-rewards-driven regime, though yes when you are in a transaction-fee-driven regime you need less hashpower to launch them with +EV. More generally, the proposals made for Electra or this curve with stronger targeting are not more opinionated to me than the current reward curve that we have, they just express different opinions, which appear to me to be broadly more in line with the goals of Ethereum. So it’s not really a problem of adding complexity to the system vs status quo, but deciding what best suits the needs of our network.

---

**Draco** (2024-02-23):

The article:

- does a great job at highlighting the advantages in terms of cost, convenience, and liquidity of SSPs vs solo stakers
- does not account for airdrop/points farming from protocols such as EigenLayer. Swell, Puffer, etc. which represents additional yield pressure to drive SSP adoption
- correctly suggests that as overall staking ratio grows, solo stakers will be disadvantaged even more, because of SSP’s structural advantages
- proposes a solution that tinkers with overall stake ratio rather than trying to address the problematic structural advantages of SSPs

The dominance of SSPs (and in turn, the staking ratio issue) is a result of average ETH holders making rational economic decisions. The threat posed by SSP dominance is not a new topic and yet we have make little progress solving it. And I’d argue the reason we found ourselves in this situation because we have not been willing to address the structural advantages of SSPs over solo stakers

In the end, it’s an incentive problem. And it is best (can only be) fixed with incentives

The real question here is: Are we willing to discriminate against a SSP validator? More specifically:

- Is a solo validator the same as a SSP validator? (I’d argue no. at this point an additional SSP validator is a net negative)
- If a solo validator and a SSP validator are different, is it wrong to discriminate one against the other? Does it violate principle of credible neutrality?
- If it does violate credible neutrality to a certain degree, is it acceptable?

I’d love to see what the community think re: those questions, the pros and cons

But now assuming we are willing to entertain the idea of validator discrimination, here’s a few unsophisticated thoughts on how we might fix the imbalance in structural incentives

First, thanks to community effort, we already have some ways to distinguish solo stakers from a SSP. Of course, the list is imperfect at the moment, but I’m sure we will get there over time. (also, as a zk-illerate, is there a way we can allow solo stakers to attest to their solo staking status while keeping privacy?)

**Proposal #1: Yield over Convenience with ePBS + MEV Redirect, a protocol-based approach**

- Instead of the proposed MEV burn, simply spread the MEVs evenly among solo validators only
- If the result of this comes to a 2+% higher yield to solo stakers over SSPs, I’m sure many of those who own more than 32 ETH will be motivated enough to unstake their LST and learn to spin up solo nodes

**Proposal #2: Solo Staking Loyalty Points (SSLP) farming, a community-based approach**

- solo stakers accrue loyalty points
- Points should measure how long a solo validator has been active and attestation effectiveness
- Points accrued on a monthly basis and non-transferable
- Points can be redeem for solo staking achievement NFT/SBT/POAP
- Retro-airdrop for SSLP or staking achievement
- We can try and persuade projects to pre-commits to an allocation to solo stakers. For example, they can make statement like “We don’t have a token, we might never have a token, but if we ever do, there will have an allocation to solo stakers and the amount will be based on SSLP”

---

**ComfyGummy** (2024-02-24):

Hi, fellow home staker here.

Thanks for the proposal. I appreciate the thoughtful analysis of the cost structures of home staking and I agree with all of them. However, I do not understand why stake ratio targeting solves them. It seems to me that no matter how you slice it, implementing targeting means that staking yield, both nominal and real, will go down compared to today’s levels.

This means the first stakers to become priced out of staking will be the home stakers, for the reasons you’ve already enumerated: they don’t have the economies of scale that large staking pool operators do, they don’t benefit from the value of having their stake liquid, they have higher reward variability, and so on.

I would add to this list: Home stakers will likely not be able to earn as high a yield as SSPs will due to restaking opportunities that require serious hardware.

**
There is also another dynamic that this post doesn't mention: LST liquidity wars *between each other* in a stake ratio targeting environment.**

So far, most new staking providers have been able to gain market share because they can attract new ETH to be staked. In a world of stake ratio targeting, especially one where the target is close to 1/4 which is already what the current ratio is, *the LST competition becomes zero-sum*. This accelerates the winner-takes-most dynamic the post already mentions, and it cements the position of existing LST operators as it makes entering the LST market increasingly difficult. You might argue that we are already effectively heading there anyway but that it’s just a matter of it happening when we reach 100% of stake vs whatever the targeted stake ratio is, but the argument remains that the world where the LST market is allowed to grow in a non-zero-sum way for a few more years vs the world where the only new ETH coming into LSTs has to come from existing stake are two different worlds. It may well be that giving more breathing room to the LST market brings a sufficient number of new entrants to ensure the a sufficient plurality of SSPs and delay winner-takes-most effects. But of course, all of this is speculation.

At the end of the day, home staking is already not an economically rational choice. LSTs are already more competitive, and the difference seems like it will only grow over time as per the above arguments. This is why I’ve proposed that [we should make staking operators legible to the protocol](https://ethresear.ch/t/how-optional-non-kyc-validator-metadata-can-improve-staking-decentralization/17032) so that we can actually reverse this effect.

![](https://ethresear.ch/user_avatar/ethresear.ch/draco/48/12292_2.png) Draco:

> First, thanks to community effort, we already have some ways to distinguish solo stakers from a SSP. Of course, the list is imperfect at the moment, but I’m sure we will get there over time. (also, as a zk-illerate, is there a way we can allow solo stakers to attest to their solo staking status while keeping privacy?)

See [this proposal to do just that](https://ethresear.ch/t/how-optional-non-kyc-validator-metadata-can-improve-staking-decentralization/17032).

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> What is the current time required to withdraw staked ETH (given current withdraw queues and whatnot)? Knowing this would help analyze the time-value-of-money cost to low-liquidity stakers.

It currently takes nearly no time; [only about 37% of the beacon chain’s exit capacity was used in the last 30 days](https://www.rated.network/overview?network=mainnet&timeWindow=30d&rewardsMetric=average&geoDistType=all&hostDistType=all&soloProDist=stake). As the OP notes, staking has been mostly up only. However, as a home staker, this is not really what makes my staked ETH illiquid. What actually makes it illiquid in practice is:

- Exiting the validator is an extremely manual process which I have not researched and, having a full-time job, it would likely be a weekend project to figure out how to do this safely. It requires re-learning a bunch of things I have likely forgotten around how my validator operates (something which I set up once and only need to worry about occasionally), as well as needing to research how to set up another validator later if I want to stake it again.
- I cannot use my home-staked ETH for anything other than ETH staking. Contrast this with LSTs, which can be used in DeFi to get a loan against them, or can be used to participate in vampire attacks in the SSP wars, etc. as noted above by @theSamPadilla. Essentially, LSTs have already attained a significant amount of money-ness. In the future, my home-staked ETH will probably also be forgoing more yield opportunities from restaked AVSs which be run on a residential connection. That’s OK with me; my goal with home staking is to secure Ethereum and ensures it keeps running first and foremost, and I would be home-staking even with negative yields. But I think the pool of home stakers for which this is sufficient motivation is vanishingly small as a fraction of staked ETH.

---

**MicahZoltu** (2024-02-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/comfygummy/48/13538_2.png) ComfyGummy:

> Exiting the validator is an extremely manual process which I have not researched and, having a full-time job, it would likely be a weekend project to figure out how to do this safely. It requires re-learning a bunch of things I have likely forgotten around how my validator operates (something which I set up once and only need to worry about occasionally), as well as needing to research how to set up another validator later if I want to stake it again.

Assuming your withdraw address is already set, exiting a validator is just running a single command with your validator client: https://launchpad.ethereum.org/en/withdrawals/#how-to-exit  I would estimate 5 minutes to read the docs for your validator client and run the command, maybe 10 minutes if you want to be thorough.  If you don’t have a withdraw address set, then you’ll need to do that first but it is a similarly easy process IIUC, and new stakers will not have to do this as it is set during staking setup process now.

![](https://ethresear.ch/user_avatar/ethresear.ch/comfygummy/48/13538_2.png) ComfyGummy:

> I cannot use my home-staked ETH for anything other than ETH staking. Contrast this with LSTs, which can be used in DeFi to get a loan against them, or can be used to participate in vampire attacks in the SSP wars, etc. as noted above by @theSamPadilla. Essentially, LSTs have already attained a significant amount of money-ness. In the future, my home-staked ETH will probably also be forgoing more yield opportunities from restaked AVSs which be run on a residential connection. That’s OK with me; my goal with home staking is to secure Ethereum and ensures it keeps running first and foremost, and I would be home-staking even with negative yields. But I think the pool of home stakers for which this is sufficient motivation is vanishingly small as a fraction of staked ETH.

If your goal is to secure Ethereum, then you should continue to solo stake and not participate in all of the crazy DeFi lego stuff with your stake as that stuff generally *weakens* Ethereum’s security.  Ethereum would be more secure if those people didn’t stake at all.  The problem is, we don’t have a way of stopping them from harming the network, so they continue to exist and do what they do and we hope that enough people don’t do those things.

---

**danw.eth** (2024-03-02):

Hi,

This is an interesting problem, thank you for the detailed writeup and acknowledging solo stakers might suffer more from targeting.

I’m a solo home staker, with several validators and rocketpool minipools (and intention for future DVT participation).

There’s just a few assumptions/comments I’d like to challenge:

![](https://ethresear.ch/user_avatar/ethresear.ch/casparschwa/48/3001_2.png) casparschwa:

> Holding raw ETH should be economically feasible, to ensure user friendliness and preventing dilution beyond ensuring sufficient security.

I think it’s a misconception that it’s not viable to hold ETH without a yield. Bitcoin is held without a mining yield, and the recent ETF flows have proven that people don’t need a yield to simply hold an asset. In addition, the issuance/inflation is higher for Bitcoin than it is for Ethereum after EIP 1559.

Even so I acknowledge humans will chase small amounts of yield wherever it is, as seen through 2021-2022 and all the problems it caused.

![](https://ethresear.ch/user_avatar/ethresear.ch/fradamt/48/6474_2.png) fradamt:

> Solo staking costs are mostly upfront, and current solo stakers have already paid them. It seems to me that one could reasonably expect many of them to stick around.

The initial cost of staking hardware really is not expensive compared to the ongoing monetary and non-monetary costs. In addition since it’s a sunk cost it wouldn’t really contribute to the decision about whether to keep operating based on the issuance - that would be more about the ongoing viability of staking and ones belief in Ethereum as a viable long term investment. The ongoing long term costs of staking I have for example are:

- Extra internet connectivity, a 2nd internet connection, higher speeds, higher data. Particularly required for multiple validators and/or splitting into DVT clusters or minipools like Rocketpool.
- Time cost for updates every 2 weeks, fixing problems with updates (e.g. today the MevBoost update caused timeouts), fixing outages (e.g. Nethermind bug).
- Capital requirement of holding all the ETH in the contract, while not technically an accounting cost it’s a major decision factor on whether to continue staking. Sure it’s easy to withdraw, but by deciding not to withdraw it’s a capital allocation that for some is an extremely large and non-diversified risk.
- Electricity, is minor in my opinion.
- Upgrades due to changes like EIP 4844

You could say these are more like ongoing commitments rather than just costs, but I’m just highlighting this because these are the factors that play into the constant decision to stay as a home staker. Not once do I think about my upfront cost paid 2+ years ago.

![](https://ethresear.ch/user_avatar/ethresear.ch/thesampadilla/48/15356_2.png) theSamPadilla:

> This, however, strikes me as incentivizing the exact opposite of what this is trying to achieve. Asymptotically reducing staking incentives after a given staking ratio is likely to hurt solo stakers before it hurst LST stakers.
>
>
> Set aside infra, capital requirements, and knowledge needed to run a solo validator. I think this boils down to (lack of) liquidity. The sacrifice solo stakers make when validating is lockng up their ETH in contract. LSTs don’t make this sacrifice, they still had their LST that they can use on DeFi, borrow against, lend, or immediately exit at any point in time. In a future where the value of holding your ETH excels the rewards, I don’t necessarily see it hurting LSTs, if you assume the 1:1 parity of :ETH will hold.

I agree and I think it’s useful to conceptually split the LST considerations into the two participants:

1. The LST node operator, whose costs are rather fixed and will earn a percentage of what depositors earn.
2. The person who swaps their ETH for an LST, or deposits it into an LST contract in exchange for an LST yield bearing token

Participant #1 would likely take steps to reduce costs and increase risk if there was less yield, e.g. for instead of running 20 nodes they may cut down to 3 nodes and increase the number of validators per node. It’s an extremely efficient business, to run many validators without much of your own capital deposited. Unfortunately I don’t see this proposal as targeting these participants in a stronger manner than it would target solo stakers, because due to economies of scale with potentially thousands of validators they would still be ahead of solo stakers even if only taking 5% of the earnings (which they can choose to vary if yield changes).

Participant #2 really has zero cost, and can deposit every ETH they own since they only pay for the LST operator out of the yield they earn. Even if yield was 0.1% and they paid 0.01% commission then economically they still don’t feel the cost like a solo staker would. In reality they would have to consider smart contract and slashing risk, and the usefulness of their LST receipt token in DEFI (even though most people ignore this and throw money around like crazy).

Both of these participants I see being much more resilient to the potential changes than the home/solo staker.

![](https://ethresear.ch/user_avatar/ethresear.ch/casparschwa/48/3001_2.png) casparschwa:

> At this point, we want to stress that this composition does not change the effectiveness of the incentive to stake. In other words, dilution protection incentivizes stakers just as much as real staking yields!

Dilution prevention is something that is great for all holders of Ethereum. However when observing participants of the Ethstaker reddit and other social media comments, the dilution prevention of other changes were not appreciated. EIP 1559 burning of gas to make Ethereum deflationary and benefit all ETH holders, was also seen as a redistribution from stakers to ETH holders. I fear that dilution prevention is not seen as an incentive to be a solo/home staker, as staking is not required to receive that benefit. Personally I can understand the logic, but the public has a history of misunderstanding the many Ethereum proposals and upgrades.

I agree with the problem that has been detailed, but I think the solution needs some more input.

The primary difference I see between LST operators and Home/Solo stakers is that an LST operator runs a large number of validators from a single beacon chain client (and a single node), whereas most home stakers have just 1 validator or very few.

If there was a way to have variable issuance based on how many validators are attached to an instance of a beacon chain client it could reduce the economy of scale benefits achieved by LST operators, encourage more unique nodes and incentivize the decentralization we want to encourage.

I suspect however there would be ways to work around such solutions, and some sort arms race between the spec and LST configurations. Unfortunately I don’t have a solution, I just believe there may be other solutions yet to explore.

---

**Jstar101** (2024-03-03):

I agree with the decision to re-evaluate staking economics given we now have staking data spanning multiple years. One of the main unknowns at this point in time is how restaking will impact the ecosystem, however I believe that we should design the optimal staking economics for Ethereum, irrelevant of restaking. Any deviations away from this ‘optimal’ due to restaking should be seen as restaking impacting the security of the network and should be avoided.

Whilst I agree that targeting a fixed staked supply solves issues associated with a super majority of staked ETH, it does not solve the winner takes all dynamic. Applying a yield curve that limits stake to say 30% of total ETH supply will lock in Lido as the winner of ETH staking. The only way in which smaller/newer staking protocols can realistically compete is to encourage capital away from Lido using incentives, something that Lido can easily combat with its own purchasing power. This entire ecosystem is already a Moloch trap where staking protocols are required to spend significant sums to attract capital and capping the total ETH stake will likely increase this problem. The worst part, however, is that real competition (outside of incentives) will likely be squashed, reducing innovation and technological advances that would otherwise lead to a safer staking ecosystem for both stakers and the network as a whole.

We know that yield is always going to be the primary driver of where/how stakers stake. The only way I can see us safely aligning yield with ecosystem security is introducing staking economics that fundamentally rewards stakers that take steps to improve network security, such as using minority clients, home staking, etc… Admittedly, this would get complicated very quickly and introduce technical challenges (i.e. how can you prove someone is a home staker or truly using X client), but I do not see how we can meaningfully take steps to improve the current dynamic with a simple shift in the yield curve.

One of the main arguments against solo staking at the moment is the lack of economic incentives to do so, mostly due to them missing access the benefits available to liquid stakers: A) being able to use staked capital in DeFi/CeFi, and B) economies of scale that large staking pools receive due to MEV. It is important to highlight here that this doesn’t have to be the case. Whilst it is not yet widely known, solo stakers are able to liquid stake against their own node via StakeWise V3. StakeWise DAO provides the liquidity and integrations for its LST, osETH, which solo stakers are permissionlessly allowed to utilise in DeFi. This opens up the door for solo stakers to borrow against their own nodes, leverage stake, and even restake by depositing osETH on Eigenlayer. I am of the opinion that native restaking will not be available to home stakers due to the expected competition across operators to be in the active set for AVSs (in the very least the most lucrative AVSs will not be available to solo stakers, further increasing the economic disparity). The ability to restake an LST minted from a home node goes some way to solving this. Alongside an LST, StakeWise V3 enables stakers to access a smoothing pool with zero costs and goes some way to solve economies of scale problem too.

When evaluating the economics between liquid staking and solo/home staking, it is vital to consider the ability for solo stakers to liquid stake in this manner as it fundamentally changes the dynamics. It is also vital to increase the awareness for solo/home stakers to liquid stake in this manner to further encourage the participation of home stakers.

---

**htimsk** (2024-03-07):

Thank you for the in depth post. One question that I have is how can the “Real ETH Yield” be negative? With the inclusion of the EIP-1556 and the burning of the base fee the amount of ETH has decreased since the merge. As modeled by https://ultrasound.money/. Hence a holder of ETH who does not stake is not being diluted. I don’t think the model can ignore the effects of 1556 and simply assume that unstaked ETH is being diluted by the Beacon chain issuance.

---

**barnabe** (2024-03-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/casparschwa/48/3001_2.png) casparschwa:

> [6] We analyze these yields in isolation, in particular we do not consider the tx fee burn mechanism (EIP 1559). The underlying analysis would remain unchanged nonetheless, as all yield curves would be shifted up- or downwards by some constant amount, independent of the staking level. We simply wish to reason about an ETH holder’s decision to stake or not to stake and for that only the difference in yields is relevant.

I believe this footnote addresses your question, indeed the burn may shift up the real yield, but that shift is constant across the whole real curves, so does not change the relative quantities and thus the arguments of the post.


*(16 more replies not shown)*
