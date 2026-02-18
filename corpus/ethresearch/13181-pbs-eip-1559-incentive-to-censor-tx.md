---
source: ethresearch
topic_id: 13181
title: PBS + eip-1559 = incentive to censor Tx?
author: uri-bloXroute
date: "2022-07-29"
category: Proof-of-Stake > Economics
tags: [mev, fee-market]
url: https://ethresear.ch/t/pbs-eip-1559-incentive-to-censor-tx/13181
views: 3258
likes: 8
posts_count: 13
---

# PBS + eip-1559 = incentive to censor Tx?

**block-builders are incentivized to censor / ignore Tx to reduce BASEFEE, to make MEV bundles more profitable.**

*this post expands on the discussion with [@vbuterin](/u/vbuterin) during the MEV Salon

[![images (2)](https://ethresear.ch/uploads/default/original/2X/8/8dac9cdd2eb580440370bfd379e80ca224375198.jpeg)images (2)265×190 5.05 KB](https://ethresear.ch/uploads/default/8dac9cdd2eb580440370bfd379e80ca224375198)

In Vitalik’s [slides](https://hackmd.io/@vbuterin/in_protocol_PBS) ![:point_down:](https://ethresear.ch/images/emoji/facebook_messenger/point_down.png?v=14) from yesterday he points out that censoring is costly:

- if a censored Tx has a Priority Fee of P
- the censoring block-builder is always at a disadvantage of P compared to other block-builders who will attempt to include this Tx
- Censoring block-builder will pay P (or lose a revenue of P) in every block until the Tx confirms

[![Screen Shot 2022-07-28 at 2.53.39 PM](https://ethresear.ch/uploads/default/optimized/2X/1/165def0998005dc9b585dcafcf3d3dcc963ee4de_2_345x195.jpeg)Screen Shot 2022-07-28 at 2.53.39 PM2102×1192 117 KB](https://ethresear.ch/uploads/default/165def0998005dc9b585dcafcf3d3dcc963ee4de)

This sounds pretty straightforward, and that it would be too costly for block-builders to censor Tx.

I want to provide additional data on block-builders incentives, which paints a different picture:

1. Under PBS, validators “blindly” pick the block which pays them the most
2. Block-builders construct blocks aiming to maximize MEV, with either their own MEV Tx or MEV bundles received from MEV Searchers.
3. Looking at a few random bundles on zeroMEV you can see that MEV Searchers burn $10-$50 in BASEFEE in every bundle
4. If BASEFEE was somehow pushed down, these bundles will produce more valuable blocks.
5. While the BASEFEE is significant, the priority tip isn’t: ~$0.05
6. Key Insight: due to eip-1559, Tx cost >> Tx tip so block-builders profit is much more sensitive to their own cost Vs. the tips from other Tx

So, what should a cut-throat MEV-maximizing block-builder do?

probably one of two options:

1. Push BASEFEE down, by

- increasing the gas limit while constructing 15M gas blocks, or
- Ignoring (i.e. censor) 100 Tx, paying $5 to be comparable to other builders, and repeat for 20 blocks (total cost $1,000)

1. return to 15M gas blocks with 30M gas limit, increasing MEV revenue by ~$25/block, so effort pays itself within a few hours
2. fill blocks only up to 15M gas, delaying other Tx to times where there are less Tx, unless their tip makes up for the cost pushing the BASEFEE down again afterwards
3. Welcome back to First Price Auction (FPA)!

The problem is worsen by the fact that each block-builder knows that all the other block-builders are similarly incentivized.

For the record - I think there **are** ways to improve PBS, some of which we’ve been discussing and exploring ([here](https://twitter.com/uriklarman/status/1546971147018948609)). And we at bloXroute are running both a “regular” block-builder and a “good” block-builder which avoids front-running.

But I am very surprised that while eip-1559’s economics were [thoroughly](https://timroughgarden.org/papers/eip1559.pdf) considered, PBS is being released in the wild and I don’t think anyone knows how things will play out in terms of block-builder competition, economic effects, centralization of Tx flow.

[@vbuterin](/u/vbuterin) - is my argument clearer now?

Yes, you could obviously set the gas limit in-protocol, but block-builders could still take the 2nd approach. You could then introduce crLists, but if we’re counting on validators altruism, why not just use the crLists for “fair ordering” like Ari Jules is suggesting?

I don’t know, we probably need a spec before we can analyze the incentives and implications of crLists, but I don’t think we can just punt it as a solution.

## Replies

**MicahZoltu** (2022-07-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/uri-bloxroute/48/9412_2.png) uri-bloXroute:

> You could then introduce crLists, but if we’re counting on validators altruism, why not just use the crLists for “fair ordering” like Ari Jules is suggesting?

The key defense against what you propose is that it is profitable to defect from any sort of block builder censorship attack.  Imagine there are two block builders and for whatever reason they have managed to push the base fee down to epsilon.  Either of those block builders could build a more profitable block than the other by over-filling the block (driving the base fee up).  If the two block builders collude, then a third block builder can show up and out-compete them by filling 2x full blocks.  If that third proposer colludes, a fourth can join and overfill blocks.

Since becoming a block builder is permissionless, and defecting from the collusion strategy is profitable, it is unlikely that collusion will actually happen/hold because it just doesn’t make financial sense long term as you have to pay the difference between your under-full blocks and a 2x full block *forever* to maintain the artificially low base fee.  This means that as a builder, that whole base fee that you just drove to epsilon now has to be paid by you to the proposer forever, so you have no incentive to actually do this as you don’t actually benefit from it at all.

---

Regarding crLists, it doesn’t require all proposers be altruistic, it just requires that *some* proposers be altruistic so censored transactions can eventually be forced through by proposers.  Also, if clients come with baked in defaults it requires proposers be altruistic *or* lazy, and the combination of the two results in a pretty large percentage of people, especially when there isn’t some direct financial incentive to do otherwise.

---

**barnabe** (2022-07-29):

I agree with [@MicahZoltu](/u/micahzoltu) here, and to add two elements to the discussion:

- Suppose the current market price of gas is 50 Gwei, and basefee has been driven to zero by the attack you describe. The builder who keeps the attack going by filling only a 1x target block has an opportunity cost of ~15M gas x 50 Gwei = 0.75 ETH against a builder who fills up the block to 2x capacity, since users would eventually match the market price with their priority fees. So the lower basefee gets, the higher the incentive to deviate is, and the costlier the attack becomes to the cartel of colluding builders.
- There is also an imbalance between the attackers and the defenders. To make the most effective attack, attackers want to produce empty blocks so that they drive basefee down faster during the first phase. While they make empty blocks, they entirely forego all their revenue. If they decided to trade-off speed of the attack against some revenue, e.g., by filling blocks only up to 25%, then defenders need only make one full block to compensate the basefee bias from two adversial blocks. So again here the attack gets costlier as it is more severe.

These are two simple arguments, I believe more modelling could be done, e.g., writing down precisely the bounds of how much the attack costs during either phase, but it is also unclear to me how PBS changes much from the analysis that was done at the time of 1559 (see [Tim Roughgarden’s report](http://timroughgarden.org/papers/eip1559.pdf), section 7). In the proposer model, a proposer joining the cartel incurs an immediate opportunity cost C vs producing a non-cartel block (C varies depending on the phase etc). In the builder model, the builder could indeed make up that cost C along the way to keep overbidding everyone else, such that greedy proposers always pick this builder, but C increases as the attack goes on. The cartel could also censor blocks built with deviating, honest builders but then it reduces to a classic 51% attack.

Can you expand on the “crList fair ordering” solution? I’ve not heard about a combination of the two (I missed that salon where it was perhaps discussed)

---

**MicahZoltu** (2022-07-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/barnabe/48/4742_2.png) barnabe:

> it is also unclear to me how PBS changes much from the analysis that was done at the time of 1559

I think the difference is that builders are *expected* to centralize, while proposers/miners are *expected* to be somewhat distributed.  Arguably, mining pools are fairly centralized but there were still enough that anonymous defection was a reasonable strategy.  Builders on the other hand are expected to whittle down to probably a small handful where perhaps anonymous defection won’t be quite as easy.

I’m not convinced this changes things significantly, as 1559 was designed to work under pretty heavy collusion assumptions (you only need a very small number of honest/altruistic/defecting miners to break the cartel).

---

**barnabe** (2022-07-29):

True, you could make the case the other way around too, yes builders are centralised/centralising but it’s also much easier to spin up a new (defecting) builder than a new mining pool

---

**MicahZoltu** (2022-07-29):

While I can appreciate that argument, it isn’t obvious that the marketing/infrastructure difficulty of spinning up a mining pool are *higher* than authoring a builder that is MEV competitive enough to actually get successful blocks.  The fact that you would be getting up to 2x the fee revenue of cartel builders definitely helps make such a builder more competitive, but it *may* not be enough depending on the volume of MEV available.

---

**MicahZoltu** (2022-07-29):

Something else to consider, I *think* the idea is that all clients will build a local block and compare the revenue from it with builder proposed block and always prefer local over builder if the local block is more profitable.  This means that by default, the naive strategy (no MEV extraction) is the baseline that the builder cartel needs to compete with.  So if you are building empty blocks, you need to pay the proposer *at least* 2x full blocks worth of fees at the current fee rate (which increases as the base fee goes down), even if you have 100% builder cartel.

---

**wanify** (2022-08-03):

Should we assume zero entry cost in being a builder? Is it possible that a validator enters the builder market at block ***n*** and exit the market at block ***n+1*** with almost zero cost?

I first thought that being a builder requires very high system requirements with expensive setup cost, so that the builder market cannot be entirely open, unlike today’s MEV market.  Reading the discussions above, I am a bit confused about this assumption.

---

**uri-bloXroute** (2022-08-03):

Thanks [@barnabe](/u/barnabe) and [@MicahZoltu](/u/micahzoltu) - these are great points!

So great in fact, that I’ve been mulling over them for days, which is why I didn’t respond.

I’m not entirely convinced though…

I’m not imagining a BBs producing empty blocks, nor the need to actively collude and BBs needing to anonymously defect.

I’m more concerned about BBs quickly pushing gas limit down (5 minutes at 3am on a weekend) and then ignoring 1559’s flexibility and producing up to 15M gas blocks, and delaying low fee Tx until they have room for them. And if priority fees spike - great! build pressure, capture fees, rinse & repeat.

Let me continue thinking about for a few more days - I keep rephrasing the issue in mind, but I haven’t nailed it yet

[@wanify](/u/wanify) - running a competitive block-builder requires executing non-trivial simulations. If it wasn’t the case then every validator would have run their own BB as a backup, but unfortunately this isn’t the case.

---

**barnabe** (2022-08-03):

I’ll try with a table to formalise the argument, maybe this is helpful to the discussion ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) Let’s say there is some group of builders, and Alice the builder. In each cell, the payoff is (Alice, other builders), where other builders can be thought of as a single builder. If you don’t like the idea of a collusion, you can replace references to “collusion” by “drive the basefee down by under-filling blocks”.

|  | Builders don’t collude | Builders collude |
| --- | --- | --- |
| Alice doesn’t collude | V(0), V(0) | V(\Delta), V_c(\Delta) |
| Alice colludes | 0, V(0) | V_c(\Delta), V_c(\Delta) |

\Delta measures the difference between the basefee and the market price of gas. Typically, the difference is equal to the nominal “1 Gwei” miner compensation, but assume that it is zero. The longer builders under-fill their blocks, the larger \Delta gets.

By V I mean the value available to be captured by the builder. The larger \Delta is, the higher V is, as users bump up their priority fees to make up for the low basefee.

V_c is the value function for builders who collude, i.e., they are not allowed to make blocks beyond a certain amount of gas G < \text{tgt}. So we always have V_c(\Delta) \leq V(\Delta) (but usually this inequality is strict)

Two claims can be true at the same time:

- V(0) < V_c(\Delta), i.e., builders extract more value when they drive basefee to zero, even if they limit themselves to blocks maintaining low basefees.
- Alice always has the incentive to deviate from the coalition, for any \Delta.

---

**uri-bloXroute** (2022-08-03):

[@barnabe](/u/barnabe) my issue is the following (again, I haven’t nailed it myself):

including another 100 Tx at 1 gwei is $2 / block

since MEV pays $200M/yr, its ~$600K/day, or ~$100 / block

that means:

- this amount is very small, compared to deciding between bribing using 90% or 92% of the profit.
- If the builder can increase its MEV profit by a good margin, it’s better off accepting this loss
- It won’t pay it forever because this “advantage” of a “defecting” builder would be eroded anyway, when these Tx will be included eventually at the same avg rate of 15M gas / block, since Tx are not being censored, just delayed to a later, less full block
- maybe eventually priority fees go up so much so they are all included, and then the cycle begins again.
- so your table is right, it just might be missing external factors which are significantly greater

again, this is not well articulated, just the hunch I’m still struggling to fully grasp

---

**barnabe** (2022-08-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/uri-bloxroute/48/9412_2.png) uri-bloXroute:

> It won’t pay it forever because this “advantage” of a “defecting” builder would be eroded anyway, when these Tx will be included eventually at the same avg rate of 15M gas / block, since Tx are not being censored, just delayed to a later, less full block

So that’s where I think I disagree. You can think of 1559 as aiming for a given throughput over time. When you artificially clamp the throughput, which you do when you under-fill blocks, you are creating an imbalance, assuming there is always more demand to be served than the throughput can serve (which imo is a fair assumption, otherwise basefee = 0 in equilibrium anyways). Meaning if over 10 blocks you under-fill by 5M gas each, there is 50M gas that the system *wants* to fill. Of that 50M gas, colluding builders are only allowed to serve < 15M per block they produce, to keep the attack going. Meanwhile, Alice the deviating builder can always make blocks serving 30M gas of user demand.

You may be displacing some of the demand that would have been served at the equilibrium basefee (= market price) and serving it instead when basefee is made low, but along the way, the incentive to deviate is stronger and stronger (in other words the cost of collusion C(\Delta) = V(\Delta) - V_c(\Delta) increases as \Delta increases). The issue is that you as a builder may be willing to subsidise the attack by spending C(\Delta) as long as \Delta is low, as you say, it’s a couple dollars. But you don’t know when you might be able to take profits, if at all. A single deviating builder can rug you of the effort you have personally invested to make this attack work. And assuming the demand process is stationary + in an efficient market (users update their PFs along the way), there is as much money to be made on the way up, when someone deviates and resets basefee to its equilibrium market price, as there is cost to spend on the way down, clamping blocks to make basefee go to zero but expending a little extra to puff up your bid to the proposer. So it’s not even the case that you can “make back” the expense of the attack if someone deviates before you start exploiting the low basefees and taking profits.

---

**MicahZoltu** (2022-08-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/uri-bloxroute/48/9412_2.png) uri-bloXroute:

> including another 100 Tx at 1 gwei is $2 / block
> since MEV pays $200M/yr, its ~$600K/day, or ~$100 / block

Both the cartel members and defectors are making the MEV money (presumably) so it is a wash when comparing the two.  The defector makes more in fees while the cartel member makes less in fees, so on net the defector makes more money in all situations when all else is equal.

FWIW, MEV being worth significantly more than fees/attestation rewards is definitely a problem as it can lead to selfish mining becoming the optimal strategy (I haven’t checked if this still applies under PoS or not).  However, the presence of 1559 base fee actually *reduces* this because it reduces the value of transaction fees relative to attestation rewards.

