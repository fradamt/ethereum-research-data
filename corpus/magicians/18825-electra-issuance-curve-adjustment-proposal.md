---
source: magicians
topic_id: 18825
title: "Electra: Issuance Curve Adjustment Proposal"
author: caspar
date: "2024-02-22"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/electra-issuance-curve-adjustment-proposal/18825
views: 10052
likes: 71
posts_count: 24
---

# Electra: Issuance Curve Adjustment Proposal

*by [@adietrichs](/u/adietrichs) and [@caspar](/u/caspar)*

In this document we argue for a change of the issuance curve in the upcoming network upgrade Electra.

For a more detailed account of the current issuance policy, its drawbacks as we see them, and an endgame vision for staking economics, read our writing on [stake participation targeting](https://ethresear.ch/t/endgame-staking-economics-a-case-for-targeting/18751).

---

*Many thanks to Anders, Barnabé, Francesco, Mike, and Dom for feedback and discussion.*

Reviews ≠ endorsements. This post expresses opinions of the authors, which may not be shared by reviewers.

The work presented here is based on Anders’ suggested issuance curve, linked below.

---

***Relevant resources***

- Endgame Staking Economics: A Case for Targeting
- Properties of issuance level: consensus incentives and variability across potential reward curves
- Minimum Viable Issuance

***Terminology***

staking ratio - fraction of ETH that is staked

SSP - staking service provider

LST - liquid staking token

***tl;dr***

- We argue why under the current issuance policy, in the long run most ETH will plausibly be staked via LSTs.
- High staking ratios have negative externalities:

LSTs are a winner-takes-most market due to network effects of money. This LST could replace ETH as the de facto money of Ethereum. But for true economic scalability, the money of Ethereum should be maximally trustless: raw ETH.
- Economies of scale and network effects induce more demand for LSTs as the staking ratio increases, making solo stakers relatively less competitive.
- ETH holders are diluted beyond what is necessary for security.

We briefly introduce the endgame vision for staking economics: [a stake targeting policy](#what-is-the-tldr-on-the-stake-participation-targeting-policy-7). However, we also highlight remaining open questions which make it not viable for Electra.
We thus suggest adjusting the issuance curve in Electra as per [Anders’ proposal](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448). It is trivial to implement, but significantly reduces the incentive for new stake inflow and helps to mitigate many of the issues outlined above.

---

## Why adjust the issuance policy

*< This section is a shorter and less complete version of our writeup [here](https://ethresear.ch/t/endgame-staking-economics-a-case-for-targeting/18751). >*

**1. The current issuance policy makes it economically viable for all ETH to be staked [1].** For low stake participation, a minimum staking level is achieved by issuing very high rewards. However, those rewards do not drop off conclusively enough to ensure an upper bound to staking levels.

**2. It is plausible most ETH will be staked in the long run – via LSTs.** With time and adoption, the **moneyness of LSTs continues to increase** (more integrations and liquidity + lower governance and smart contract risk), further lowering the cost of staking due to increased economies of scale of SSPs. In short, network effects of money imply that higher adoption of some LST induces more adoption of that LST.

**3. A high staking ratio is undesirable.** As negative externalities [outweigh benefits from increased security](#what-level-of-stake-participation-is-optimal-or-sufficiently-secure-5), the marginal utility of delegated [2] staking turns negative.

- LSTs come with added trust assumptions relative to ETH: node operator risk, governance risk, legal or smart contract risk.

A too high issuance policy economically quasi-forces Ethereum users to expose themselves to those added LST risks.

**LSTs are a winner-takes-most market due to the network effects of money**. Increased liquidity, adoption, etc., all increase the demand for a LST.

- A mass slashing of the leading SSP might not be credible and considered “too-big-to-fail”. The governance of such a dominant SSP would de facto become a part of the protocol, without being accountable to all Ethereum users.

The winning LST could replace *raw* ETH as the de facto money of Ethereum. **But for true economic scalability, the money of Ethereum should be maximally trustless.**
**Solo stakers are relatively less competitive** due to the network effects and economies of scale that LSTs benefit from.
**A too high issuance policy dilutes ETH holders beyond what is necessary for security.**

- It economically constrains Ethereum users to concern themselves with the complexities of staking to prevent this dilution.
- SSPs profits, however, are proportional to amount of stake delegated with them, without suffering the dilution effects of ETH holders.

**Increased p2p networking load.**
**Real staking yields plausibly higher in long run equilibrium of lower issuance policies**. This would be beneficial to all stakers, but not for SSPs.

**4. Our endgame vision for staking economics is a stake targeting policy, but it will take time to get there.** Targeting would entail moving to an issuance curve that economically guarantees an upper bound to stake participation, mitigating all of the above concerns. However, some remaining questions and technical dependencies prevent this from being implemented in the near term. More details can be found in the [FAQ section below](#what-is-the-tldr-on-the-stake-participation-targeting-policy-7).

We argue that leaving the issuance curve unchanged, until transitioning to a targeting policy, entails numerous disadvantages. This will become apparent as we look at hard fork timelines next.

## Why in Electra?

- Changing the issuance curve requires a consensus layer hard fork.
- The current plan of upcoming hard forks (EL/CL) roughly looks like:

Cancun/Deneb (3 weeks) - EIPs were finalized many months ago
- Prague/Electra (9-12 months) - EIPs discussed right now, final decisions soon
- Osaka/? (18-24 months) - EIPs will be decided once Pectra goes live

Thus, Ethereum will remain under current issuance policy for at least 9-12 months, and without a change included in Electra, it will be ~2 years.
We argue that a lack of action for two years unnecessarily risks sliding into a regime of high staking ratios. Even with the stricter limit to the deposit queue introduced by [EIP-7514](https://eips.ethereum.org/EIPS/eip-7514), that would allow for a new inflow of >40,000,000 ETH over the span of two years (max. 8 validators per epoch). This would more than double the current validator set size, with ~60% of all ETH staked. While this represents the worst case scenario, it is plausible to get close to those levels for reasons outlined above. Further, the fact that it could happen is enough cause for concern in our opinion.
If the long term goal is to target some staking ratio, [say around 1/4 of all ETH](#what-level-of-stake-participation-is-optimal-or-sufficiently-secure-5) (current staking levels), then it is advisable to avoid exceeding that range significantly in the interim.

- Surpassing the stake participation target range before implementing such a policy, would necessitate a decrease in staking.
- Even with a gradual easing into the new curve, this would in practice entail a significant period, during which stakers would be insufficiently compensated until the excess stake can exit.

Thus, we see a strong case for an adjustment of the issuance policy in Electra. In the next section, we present a proposal for such an adjustment. In our view, it satisfies two important design criteria:

- CL changes are trivial to implement, making it feasible for Electra.
- It significantly reduces the incentive for new stake inflow and helps to mitigate many of the issues outlined above.

## Proposal for Electra: Issuance curve adjustment

**We suggest to strongly consider the adoption of a new issuance curve, [as proposed by Anders](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448#h-55-potential-candidate-for-a-new-reward-curve-23), in the Electra upgrade.** This change would update the issuance curve from `y=cF/sqrt(D)` to `cF/(sqrt(D)(1+kD)` [3]. Let’s consider this visually, before enumerating some properties of the new issuance curve.

[![](https://ethereum-magicians.org/uploads/default/optimized/2X/8/83f675fa6efb8589af52630df7f9bbe1e44b147d_2_690x220.jpeg)5783×1846 596 KB](https://ethereum-magicians.org/uploads/default/83f675fa6efb8589af52630df7f9bbe1e44b147d)

*^ this figure shows the current issuance curve on the left and new issuance curve on the right. The real issuance yield (green line) is the maximum amount of rewards issued by the protocol for correct validation, while accounting for dilution. Dilution (red line) is the (negative) yield of ETH holders who are diluted by the issuance of new ETH. Real total staking yield (green dotted line) is real issuance yield plus MEV yield [4]. Nominal total staking yield (grey) is the maximum amount of rewards issued by the protocol for correct validation, but not accounted for dilution unlike green dotted line. For more detail on the differences between nominal and real yields, please refer to our discussion [here](https://ethresear.ch/t/endgame-staking-economics-a-case-for-targeting/18751#real-yield-the-real-deal-10).*

- It visibly removes many concerns around dilution for ETH holders, as  dilution is capped at ~0.4% with the new issuance policy. With the current curve, on the other hand, dilution approaches ~1.5% in the limit.
- It keeps reward variability concerns for solo stakers in check and maintains correct incentives for consensus duties.
- It is trivial to implement this proposal, ensuring it will not be blocked by technical complexity or client team resources.
- The new issuance curve does not economically guarantee an upper bound for staking participation, unlike a targeting policy. However, it significantly reduces the net incentive to stake, primarily by reducing dilution.
- At current staking levels (30M ETH, or a staking ratio of 0.25), real total staking yield is reduced by ~30%.
- However, lower nominal yields of new issuance curve need not imply lower real yields in the long run equilibrium. Consider the figure below, which shows higher real yields in equilibrium under the new issuance policy, given some hypothetical but plausible longer term supply curve. This would be a preferable outcome to all stakers than the hypothetical equilibrium achieved under the current issuance policy.

[![](https://ethereum-magicians.org/uploads/default/optimized/2X/2/224aa8a563f776c511b15e260bd802f242de9980_2_690x221.jpeg)5755×1850 739 KB](https://ethereum-magicians.org/uploads/default/224aa8a563f776c511b15e260bd802f242de9980)

*^ this figure is identical to the above, except for the addition of an identical hypothetical* long term supply curve for both issuance curve plots. Nominal total staking yield (grey line) represents the the protocol’s demand for stake. The equilibrium level of stake is then established at the intersection between the demand and supply curve. The same hypothetical supply curve that would lead to 100M ETH or ≥ 80% of all ETH staked under the current issuance policy, would lead to less than half the amount of ETH staked under the new issuance curve. Further, we can see that real total staking yield under the current issuance policy would only be around ~0.5%, while under the new issuance curve we would obtain ~1.2% of real staking yield in equilibrium. **Given this plausible example of a long term supply curve, the new issuance curve would be preferable to *all* stakers, due to higher real yields in the long term equilibrium, and despite exhibiting lower nominal yields.**

---

## FAQ

#### What level of stake participation is optimal or sufficiently secure?

- In short, current staking levels are arguably sufficiently, if not exceedingly secure.
- But ultimately there is no objectively optimal level of staking. Instead, one needs to weigh up cost of attacks (both in ETH and USD denomination) with the negative externalities of staking mentioned above.
- We point to some references, discussing what level of stake participation might be optimal or secure enough.

#### What about viability of solo staking?

We argue that the proposed issuance change can help keep solo staking viable. In particular, if we do nothing, a continued increase in stake participation would negatively impact solo staking viability in several ways:

- SSPs with fixed costs naturally benefit from economies of scale, allowing them to operate more profitably (or charge lower fees) as they have more ETH under management. Successful SSPs might be viewed as too-big-to-fail, reducing their perceived tail risks and further contributing to such scale effects. In contrast, solo staking comes with per-staker costs that do not decrease (rather even slightly increase with networking load!) as the total amount of stake grows. In fact, EIP-7514 was in part merged for this reason.
- As a larger share of issuance goes towards “dilution protection” and no longer contributes to real yield, stakers are left with more and more of their remaining real yield coming from MEV. This yield is by its nature highly variable, which leads to increased volatility of real total yield for solo stakers. For SSPs on the other hand this MEV income is smoothed over all validators they operate, removing staking yield volatility as a concern for them.
- The liquidity gap between solo staking and LSTs widens with increased adoption and moneyness of LSTs. Put differently, the competitive disadvantage of solo staking relative to liquid staking increases, as the staking ratio increases.
- In many jurisdictions, the basis for government taxes on staking income is the nominal income, not the real income adjusted for dilution effects. LSTs can be structured in a way to shield holders from this effect, while for solo stakers this is usually not possible. This further increases the profitability gap as the difference between nominal yield and dilution-adjusted real yield widens.

#### What is the tldr on the stake participation targeting policy?

[We argue extensively for targeting as the endgame issuance policy here](https://ethresear.ch/t/endgame-staking-economics-a-case-for-targeting/18751). In short:

- Today, the issuance yield does not ensure a limit to the amount that can be staked profitably. LSTs have significantly changed the cost structure of staking, making it possible that most ETH will be staked eventually.
- We argue that endgame staking economics should include an issuance policy that targets a range of staking ratios instead, e.g. around 1/4 of all ETH. The intention is to be secure enough but avoid overpaying for security and thereby enabling said negative externalities.
- In particular, this approach is future-proof as it ensures sustainability with respect to the changing supply of ETH.
- The easiest mechanism for achieving targeting is an issuance curve designed  to go towards negative infinity beyond some staking level, as in this figure. This practically guarantees stake participation will not grow beyond some specified range.
6000×3600 475 KB

#### Why not ship targeting immediately?

- Ideally we would be in a position to propose a targeting policy for Electra already.
- However, currently there is no mechanism to capture MEV in-protocol, which means some validator staking fee logic would be required to ensure incentive compatibility of consensus duties.
- But importantly, the added complexity of a staking fee is not desirable in itself, because it would become unnecessary with future MEV capture mechanism, such as Execution Tickets or MEV Burn.
- We argue that the negative externalities of high staking levels far outweigh waiting for at least ~2 years to change the issuance curve.
- This is especially true given the proposed curve has been well studied, is trivial to implement, and in our opinion a move in the right direction, if not sufficient in the long run.

#### What about removing slashability of delegated stake to make LSTs more trustless?

Read more about what a more explicit separation of labor and capital could look like in [Barnabé’s post on rainbow staking](https://ethresear.ch/t/unbundling-staking-towards-rainbow-staking/18683). But it is not in competition with our proposal, instead both could be implemented.

- While reducing trust assumptions for LSTs, it does not mitigate all concerns at all.
- Beyond slashing, LSTs still require trust assumptions: governance/legal risk and smart contract risk. Should the money of Ethereum depend on governance decisions by some liquid staking protocol, or worse, some CEX or ETF?
- Further, there are many other negative externalities such as SSP staking fees diluting ETH holders, solo stakers being relatively less competitive, increased networking load, Ethereum users having to concern themselves with the complexities of staking if unwilling to make trust assumptions, …
- To summarize, even without slashability, a LST is intermediated by some entity or protocol with certain trust assumptions and tradeoffs. Instead, raw ETH is maximally trustless.

---

## Footnotes

[1] Modulo some ETH required for L1 txs fees…

[2] The marginal utility of solo staking also turns negative, but for much higher staking ratios. This removes all of the concerns expressed in previous section. However, if done naively it This is because many of the negative externalities are specific to delegated staking.

[3] `D` is the amount of ETH staked, and `c≈2.6`, `F=64`, and `k=2^(-25)`.

[4] MEV yield is exclusively available to validators in their role as block proposers. It is calculated as the annual amount of MEV extracted (~300,000 ETH over last year) over the amount of ETH staked. As a constant amount of MEV is shared by more validators, MEV yield decreases more rapidly than issuance yield, because it does not change with staking levels. The amount of MEV has stayed [remarkably constant over time](https://mevboost.pics/). While this could clearly change, for simplicity we will refer to the demand curve as fixed.

## Replies

**vshvsh** (2024-02-22):

Reduction is staking rewards (imminent with this proposal and staking dynamics we have now) will tighten up margins for staking which will:

- incentivize margin cutting - reducing number of node operators protocol can support comfortably, and making their setups cheaper
- incentivize vertical integration, such as restaking, exchange staking, or even MEV-based integrations to increase margins

I don’t think it’s in question if this will happen or not, the question is how impactful this will be. Which hasn’t been really analyzed in the whole string of research leading to that proposal. I think the research on how this impacts Ethereum’s valdator set should be done before the community signals if it wants this particular change or not. My intuition is the results of this will be quite gruesome for decentralization on staking level.

---

**artofkot** (2024-02-22):

The decision to reduce issuance / implement stake capping should be accompanied with a well-analyzed model for economic security. As is presented now, the current thinking is that we should be okay with 1/4 staking ratio, and presented arguments are [1], [2], [3].

With the current stake distribution these arguments may seem reasonable. However, a severe change in the institutional adoption is happening right now, with the advent of ETFs:

1. Bitcoin ETFs are rapidily growing, currently custoding 3.7% of BTC [4]
2. 8 out of 11 ETF issuers use Coinbase as BTC custodian [5]
3. As of Q4’23 Coinbase custodies 17.5m ETH, of which 4.4m ETH is staked. So now Coinbase custodies ~14.5% of all ETH in circulation [6]
4. ETH ETFs are expected to launch as soon as in May, and there is little doubt they will attract lots of institutional flows. Coinbase will likely service most of ETF issuers.
5. Given (1-4), it is quite likely that Coinbase’s share of ETH custodied will grow significantly, up to 30m ETH.
6. The market forces imply that all the ETH in Coinbase Custody, Coinbase Prime and future Coinbase ETF Custody will be long-term staked.
7. This means that of the future 30m ETH custodied by Coinbase, easily half of that – 15m ETH – will be staked, if not more.
8. If the staking ratio 1/4 is targeted (~30m ETH), we arrive at the very much possible scenario of Coinbase controlling 51% of staked ETH.

I understand that the proposed curve doesn’t strictly cap the issuance and doesn’t target the 1/4 level. However, it is a move in this direction, and I think the premise of this direction is under-analyzed. In particular, this proposed lowering of issuance has the repercussions discussed by VS above.

Bottom line:

A. I think that the premise of the staking endgame (capping and targeting 1/4 level) is dangerous and may allow 51% attacks in the future, in the view of very strong institutional flows into staking market.

B. Most importantly, partially in the view of A, I think the proposal lacks analysis from all the relevant viewpoints, and requires significantly more scrutiny.

I think it makes most sense to not add this into Electra fork, and wait for more analysis and clarity on these issues. We should push for more external research on issuance change impact on stake distribution. From our end, we have recently launched a [grant](https://cyber.fund/content/mvi) specifically dedicated to this.

---

**artofkot** (2024-02-22):

Links:

[1] [Paths toward single-slot finality - HackMD](https://notes.ethereum.org/@vbuterin/single_slot_finality#Idea-1-super-committees)

[2] https://www.reddit.com/r/ethereum/comments/191kke6/comment/kh79gh1/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button

---

**artofkot** (2024-02-22):

[3] https://www.reddit.com/r/ethereum/comments/191kke6/comment/kh7do9k/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button

[4] https://dune.com/hildobby/btc-etfs

---

**ryanberckmans** (2024-02-22):

Changing our monetary policy represents a significant hit to credible neutrality.

Why not wait and see

- How LST competition continues evolving
- Whether or not restaking delivers yield at scale, and
- How 7251’s max effective balance change plays out?

I’m not a researcher and have only a welcome appreciation for the depth of research here, but I can’t at this time see the community supporting this change.

---

**alonmuroch** (2024-02-22):

Those are good points.

It seems setting limits to 1/4 is somewhat lacking good proofing.

Moreover, if we are at 1/4 today and the limit is set to 1/4 … it will create turmoil in the market. Any limitation needs to be into the future

---

**sharp** (2024-02-22):

ETH holders will always seek yield, adjusting Ethereum’s issuance curve with the intent of decreasing the % of staked ETH will likely push ETH holders further up the risk curve leading to higher restaking concentration on Eigenlayer. This is irresponsible and will lead to new concentration risks. Any DeFi user knows this, LSTs were also obvious to predict, capital efficiency dictates the rules. Changing monetary policy arbitrarily seems very credibly neutral lol

---

**dgusakov** (2024-02-23):

From my experience working with solo stakers and the staking market, I believe that if applied, this proposal will result in the following:

- Institutional ETH will end up staked anyway
- Staking APR will reduce to the values that are even less appealing for the solo stakers
- Even if the ETH price goes up significantly, the entry barrier for the new solo stakers will get even higher
- As a result, we will see almost no net new solo stakers
- The staking market will be dominated by the vertically integrated parties who can afford to run validators at a loss by funding it from other revenue sources like selling blockspace, offering other services, etc.

The research behind the proposal is incomplete and based on assumptions that do not include incoming institutional capital.

---

**OisinKyne** (2024-02-23):

I’m firmly opposed to MVI as a direction, and think the impact of this change would be very negative for the health of the Ethereum network. This would:

- Favour enterprise staking operations
- Favour non-contributing speculators
- Harm marginal staking service providers
- Make home stakers non-viable

As a counterproposal, if the problem to be solved is LSTs becoming the base asset for the network, I think we should fix the primary downside of native staking, by allowing a mechanism for someone to exit their stake at finality for an escalating basefee. There is [a large amount](https://x.com/proofofjk/status/1761021089290006920?s=20) of risk-averse delegators that currently hold >32 eth worth of LSTs and do nothing with it, purely so they have the optionality to exit promptly if they so choose. The idea that the exit queue could become months long is unacceptable to this group, and so they hold derivatives.

[Modifying EIP7002](https://ethereum-magicians.org/t/eip-7002-execution-layer-triggerable-exits/14195/6) to process forced-exits independently from the free queue would make native staking a viable option for this risk averse part of the market. They would no longer be exposed to smart contract upgrade risk, nor the oracle risk of LSPs. This could become the safest way to delegate stake. LSTs would then be primarily needed for fractional stake (<32 eth), and for those that legitimately want to put their collateral to use, e.g. in DeFi. (LSPs can benefit from this feature too for that matter). I think this modification should be adopted for Electra/Pectra as opposed to the 7002 design as currently specified. Happy to work with the original authors on getting this proposal to technically complete to make that happen. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**barnabe** (2024-02-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/artofkot/48/11817_2.png) artofkot:

> If the staking ratio 1/4 is targeted (~30m ETH), we arrive at the very much possible scenario of Coinbase controlling 51% of staked ETH.

If a target was to be set, the nominal yield at this point (let’s say 1/4, though this number is still very much to be discussed) would be quite different from what it is today, meaning that Coinbase depositors would be faced with a new decision of whether to stake or not, and Coinbase itself would need to decide what to do with custodied ETF ETH, so I am questioning here the assumption “The market forces imply that all the ETH in Coinbase Custody, Coinbase Prime and future Coinbase ETF Custody will be long-term staked”.

A new equilibrium would be found, where the share of Coinbase in the staking set would likely not simply be their custodied amount at stake under the previous configuration with non-targeting issuance curve (so 15m staked, say) divided by the target (30m). I would expect the net effect to be a reduction of Coinbase’s nominal amount of ETH at stake. This demands of course more analysis to understand the magnitude of the effect, but is in my opinion a more reasonable hypothesis than the nominal amount at stake remaining constant.

edit: Reminding myself that this post is actually not about targeting, better discussed [there](https://ethresear.ch/t/endgame-staking-economics-a-case-for-targeting/18751?u=barnabe), but the argument also stands for a reduction in yield with this new moderate curve.

---

**IntrinsicVector** (2024-02-24):

I believe that modifying the issuance curve could potentially lead to issues with Ethereum’s trustworthiness and neutrality. Furthermore, if modifications are made, there is no guarantee that it will be a one-time adjustment.

Large corporate staking has a higher chance of proposing blocks, and they are more likely to gain MEV benefits compared to solo stakers. Therefore, I think that solo stakers are the ones who would be disadvantaged and in the event of a reduction in profits, it is anticipated that the solo stakers would be the ones to go extinct.

While there is an urgent need for updates, in order to approach this carefully, I believe that a simple and certain way to limit this would be to temporarily adjust the maximum staking amount dynamically according to the total supply quantity, and to establish a queue for entry stability.

---

**zengjiajun** (2024-02-24):

Good proposal.

My biggest critique on the insurance curve tweaking analysis is that maybe we should use the intersection of “real total staking yield” with the “hypothetical supply curve” to get the equilibrium rate.

assuming in the long run the market is rational, not acting based on face value.

In this case, it seems it actually will lower the real yield for all stakers (which is fine). Just wanted to point out.

---

**zilm13** (2024-02-25):

While the current curve is definitely bad and staking ratio is already that big that it should be addressed, decreasing ROI together with issuance (making staking less attractive at all) will hurt solo stakers more than LSTs. Applying alone at the fork it will axe solo-stakers completely which will mean lower security for the protocol.

We need some measures along with this to benefit solo-stakers. It could be:

a. Spread rewards according to the validator ordinal number. If we should have 2.5% reward, it will mean #1 validator receives 4% and #1,000,000 1% (ordinal is not current id, it doesn’t count gaps). This change cannot be applied together with validator indexes reuse. It benefits not only solo-stakers but at least it benefits them more and enough to stay. And it’s deterministic. Until we have a way to change existing validator private key, selling existing validators is not an issue. It is also close to the concept  “reward rate is fixed forever at the time of joining”.

b. Every attestation includes voluntary reward decrement with number of validators on this node. Honest nodes count unique validator ids per node and if decrement is lower than the real number of validators, such nodes are banned.

c. anything else benefiting solo-stakers

While I dislike both example measures, at least they directly address solo-stakers’ importance. One curve for all will always benefit LSTs more than solo-stakers whatever it looks like. There was no way found in the real world to tax bigger parties and small subjects with the same rate, while benefitting smaller subjects more.

---

**Kody** (2024-02-28):

Hey all, I’ll throw in my two cents:

In regards to institutional stakers, they have a structural advantage in the staking ecosystem due to their ability to spread costs at scale, making even minimal yields economically viable for them. IMO, as long as yields remain greater than zero, institutions will continue to stake, independent of the rewards’ size. This can lead to an increased concentration of staking power among these entities.

Solo stakers, who are critical to Ethereum’s decentralization, face disproportionate impacts from the reduced issuance. The viability of solo staking is crucial for preventing centralization and ensuring the network remains resilient and censorship-resistant. However, with reduced yields, the economic rationale for solo staking weakens, removing the incentives for new solo operators to come online. No matter the outcome (with or without reducing issuance), addressing this issue may require innovative solutions from the social layer, where community support and initiatives can provide alternative incentives for solo stakers. This should be the last resort, as there is no guarantee these initiatives will take hold.

Given the complexity of the staking ecosystem and the potential long-term implications of the reduced issuance proposal, there’s a clear need for further analysis from third-party researchers and economists. These studies should aim to understand the nuanced impacts of the proposal on both the macro and micro levels of Ethereum’s staking dynamics. This would give us more assurances that any adjustments to the issuance policy are made with a full understanding of their potential consequences. Additionally, any changes to Ethereum’s monetary policy should be done in a way that minimizes the impact on its credible neutrality. In my opinion, this means these decisions should be made over years, not months.

I’m glad we’re getting the conversation started now, and that the community has stepped up and shared their thoughts!

---

**artofkot** (2024-02-29):

**Current proposal VS capping stake low (1/4).**

One of the main motivations for the current proposal is a conjunction of two statements: “capping stake low is desirable” AND “reverting staking ratio back might be too hard”. This implies that any argument for/against capping stake low is also an argument for/against the current proposal.

**Staked ETH concentration.**

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> I am questioning here the assumption “The market forces imply that all the ETH in Coinbase Custody, Coinbase Prime and future Coinbase ETF Custody will be long-term staked”

Claim is that all the ETH stored long-term with exchanges & custodians will be eventually staked, and the reasons are the specifics of their client base and market structure:

1. Long-term ETH-depositors don’t have much opportunity costs in terms of yield – they are not willing to go onchain, custodian is their safe place.
2. There will be ETF competition on the basis of zero VS non-zero yield.
3. Decision to stake or not to stake may actually end being made not by depositors.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> I would expect the net effect to be a reduction of Coinbase’s nominal amount of ETH at stake.

Agree that decreasing issuance should decrease custodians’ nominal amount of ETH at stake, considering all other external conditions are the same. However:

1. The external conditions (ETF flows) position custodians to grow their nominal ETH at stake significantly.
2. Centralized custodians will have much lower supply curve than dec pools & solo stakers, due to lower costs and different client base. This implies that custodian’s nominal ETH at stake will not be significantly affected by the issuance decrease, at least relative to dec pools & solo stakers.
3. Combination of 1 & 2 lead to the possibility of one custodian controlling 51% of staked ETH, as was described in my first reply.

The scenario I described is meant to showcase that 3 is a real possibility, which means that we need to analyze it or wait and see how the situation plays out.

**Aside: meta framework.**

In addition to analyzing specific arguments, such an important & contentious proposal warrants a framework for how to reconcile and account for all the variables at play. I have sketched a map of arguments below. One starting point for a wholistic meta framework is to understand arguments’ relative importance, and focus first on those that matter most.

[![arguments_map](https://ethereum-magicians.org/uploads/default/optimized/2X/6/6edb6e25ed68226d4c0310b5b0090d4f2c740c77_2_548x500.jpeg)arguments_map1920×1749 126 KB](https://ethereum-magicians.org/uploads/default/6edb6e25ed68226d4c0310b5b0090d4f2c740c77)

---

**barnabe** (2024-02-29):

Thank you for the meta framework, this is a useful starting point. There will be much more to say about individual items, so I am not intending to reply fully to each of them right now. Here are questions currently on my mind, with some notes on potential approaches:

- Assumption of “long-term staked participants” given any PoS reward curve design: Model cost structure of various types of participants (solo stakers/operators, node operators, LST holders, ETF depositors) as well as type-specific reward curves (e.g., solo staker PnL, solo operator part of fractional/DVT pool, node operator in LSP, custodial services). Combining cost structure and reward curves, we obtain type-specific supply curves. Move on to understanding the distribution effects (relative share of each type) across classes of issuance curves, as well as aggregate size of the staking set as determined by type-specific supply curves and issuance curves under consideration.
Leading question: Is there a “macro effect” to the size of the staking set? (i.e., analyse further folk arguments that more issuance loosens everyone’s constraints and increases the relative share of certain types)
- PoS mechanism improvements: How far can we go with changes to slashing weights/parameters of the mechanism? What else can we consider to improve internal market competitiveness, i.e., “micro effects”, “make the staking set the best it can be”? (see e.g., proposals contained in rainbow staking framework, and @OisinKyne’s earlier answer)
Link back to “macro”: What are the impacts of such changes on the supply curve of each type of participant? Is there any reason to think these effects apply differentially given the prevailing staking ratio, i.e., is there still a “macro effect”, or are the two effects separable?
- ETH derivatives: What are fundamental differences between “ETH on L2-derivatives” and “ETH in PoS-derivatives (LST)”? What are fundamental differences between “Re-staked ETH derivatives” and “Re-staked staking ETH derivatives”? (possible starting point for a typology of derivatives)

---

**Wander** (2024-02-29):

This is a bit tangential, but I’d like to address one of your core assumptions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/caspar/48/1313_2.png) caspar:

> LSTs are a winner-takes-most market due to network effects of money.

This is an unpopular opinion in the age of Lido dominance, but I disagree, especially in the long run. Today’s short-term market issues are the result of distortion introduced from immaturity of the existing PoS technology which will be mostly resolved with Dencun and Prague/Electra.

**Ultimately, PoS simply needs more technological maturity to enable more dynamic market competition, which obviates the need for trade-offs like this proposal which present serious risks to Ethereum’s inclusive ideals.**

To compliment the prior technological arguments from [@OisinKyne](/u/oisinkyne), here’s an economic argument:

Although they share properties of both, LSTs are more likely to take on the market conditions of commodities rather than money (if staking parameters are ossified – otherwise, the market will continue to be distorted). That is, they will act more as inputs into a complex manufacturing system of financial products built on top, more similar to crude oil or raw ore, than a standard means of exchange. Many LST designs exist, each with different characteristics like risk-return metrics or blended product offerings. These commodities must be produced through an industry which will increasingly have larger barriers to entry due to declining margins, but the even if the cost of node operation continuously declines, that cost will always present a floor for cost of goods sold (LST fees).

Under this environment, competition naturally ensues, with perhaps one or a few dominant players per sub-category of LST but no single actor becoming dominant overall. An analysis of the LST market which doesn’t recognize the unique nature of different systems and their specialized use-cases can easily over-simplify and assume all LSTs are basically the same, but that ignores the reality of differences between osETH and stETH and rETH and frax and mETH and… Not to mention all the new 0-liquidity LST designs popping up with protocols like StakeWise v3. This market is dynamic, with Lido dominance currently problematic but decreasing slowly even as newer LSTs gain traction quickly.

–

For full disclosure, I’m part of a team which is working on a [new and unique type of unblended/pure LST which is heavily decentralized and has no commission](https://nodeset.medium.com/project-hyperdrive-4819f22391dc).

---

**mattstam** (2024-03-04):

This is a really interesting proposal, but I think we should be cautious about changing the curve before it’s clear what the endgame distribution of staking looks like.

I suspect what we’ll get if we continue down the current path is more LST dominance, but that is inevitable no matter how you adjust the curve. The interesting thing is that LSTs are adding [permissionless options](https://research.lido.fi/t/staking-router-module-proposal-simple-dvt/5625) to themselves, which preserves:

- solo staking viability
- greater potential for enforcing client diversity
- low-risk LST token holding

In a world in which there is no actual game theoretical reason for solo stakers to exist and minimal reason for client diversity, this seems like a pretty good endgame.

And if it is the how things will continue to pan out, how do these curve adjustments fit in with that world? Are they still necassary?

---

**Valdorff** (2024-03-05):

I think a proposal like this, if implemented, would essentially end solo staking (with the exception of some very large solo stakers, and some altruists willing to lose money for ethos). We have already seen a number of ways where solo stakers are underperforming (see, eg https://timing.pics/). They have more missed proposals, they cannot play timing games effectively, etc. Making staking profits marginal will ensure that the only validators left are those that are most effective at extracting value – this is extremely different from those that are most effective at securing the chain (I would argue there’s a negative correlation).

I wanted to highlight two comments from above that I think really hit the nail on the head:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dgusakov/48/11037_2.png) dgusakov:

> Institutional ETH will end up staked anyway
> Staking APR will reduce to the values that are even less appealing for the solo stakers
> …
> As a result, we will see almost no net new solo stakers

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/k/6bbea6/48.png) Kody:

> In regards to institutional stakers, they have a structural advantage in the staking ecosystem due to their ability to spread costs at scale, making even minimal yields economically viable for them. IMO, as long as yields remain greater than zero, institutions will continue to stake, independent of the rewards’ size. This can lead to an increased concentration of staking power among these entities.

---

**Guest20444** (2024-03-06):

I have only one thing to say. Solostakers are extremely important for Ethereum. Any proposal that harms them harms Ethereum credibility and makes the network more fragile. Think about a solution how solo staking is being incentivized. At the very least do not harm solo staking incentives compared to what they currently are.


*(3 more replies not shown)*
