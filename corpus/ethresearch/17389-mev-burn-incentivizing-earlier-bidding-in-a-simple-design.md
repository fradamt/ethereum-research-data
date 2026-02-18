---
source: ethresearch
topic_id: 17389
title: "MEV burn: Incentivizing earlier bidding in \"a simple design\""
author: aelowsson
date: "2023-11-11"
category: Proof-of-Stake
tags: [mev]
url: https://ethresear.ch/t/mev-burn-incentivizing-earlier-bidding-in-a-simple-design/17389
views: 2479
likes: 12
posts_count: 14
---

# MEV burn: Incentivizing earlier bidding in "a simple design"

I have been thinking about the game theory of late bidding in “[MEV burn—a simple design](https://ethresear.ch/t/mev-burn-a-simple-design/15590)” and *I thank Justin Drake for giving feedback on the following thoughts*. It seems rather intuitive that bidding after the deadline may evolve as an equilibrium strategy, as previously suggested by, e.g., [jasalper](https://ethresear.ch/t/dr-changestuff-or-how-i-learned-to-stop-worrying-and-love-mev-burn/17384/3) and [cometshock](https://ethresear.ch/t/mev-burn-a-simple-design/15590/8) (also very relevant to this post: [ethdreamer](https://ethresear.ch/t/mev-burn-a-simple-design/15590/23)). The problem is that defecting from such an equilibrium strategy is not rewarded in any substantial way. What we need is a mechanism that rewards defecting builders for chiseling at the surplus of any emerging “late-bidding cartel”. A potential solution is to reward the builder who submits the winning bid (in a majority of the attesters’ view) at the observation deadline. A design could look like this:

At the observation deadline, attesters observe the highest bid and set their subjective payload base fee floor F_f at this level. Attesters also remember the identity of the builder that provided the highest bid. If the same builder submits the block selected by the proposer, attesters vote `TRUE` in a separate vote when they attest to timeliness. Otherwise they vote `FALSE`, but still attest to the validity of the block as long as it is above their subjective payload base fee floor (and fulfills all other criteria). If the majority of attesters in the slot vote `TRUE`, the winning builder receives a fraction x of the payload base fee F that would otherwise have been fully burned (e.g., x=0.05). They thus receive the reward xF in excess of any profit (or loss) they make from the payload. An attester who votes with the majority (either `TRUE` or `FALSE`) receives a small reward. The proposer’s rewards should presumably not be determined by if it selects a `TRUE` payload or not, to avoid incentivizing proposer sophistication. Its selection can be influenced via arbitrage by builders across the payload tip anyway.

The outcome of this additional vote is that builders race to win the preliminary auction at the observation deadline. The game-theoretical equilibrium strategy will depend on the size of x. It should be set high enough to favor competition and disincentivize collusion (but not higher). Collusion is disincentivized since defection from late bidding is rewarded. This applies regardless of whether a late-bidding strategy would arise through builders’ own accord or an oligopoly evolving into a cartel.

Note that builders will likely opt to bid slightly above the MEV at the observation deadline, the extent to which will depend on x. They are incentivized to do so to attain the surplus xF and because they can expect some additional opportunities for MEV to arise before the proposer will select a winning bid. The primary motive of this change to the MEV burn design is to reduce the risks of builder collusion by providing a lucrative way to defect. The fact that it pushes builders to estimate the block’s full MEV already at the observation deadline (and in some settings may even bid above it), is an additional feature, which on balance should be positive.

A drawback is added complexity. The proposal also introduces some game theory for attesters that we may wish to study closer and make adjustments for. They may, e.g., gain from voting `FALSE` even if they observed `TRUE` if they registered a flurry of competing bids at the deadline. One way to try to adjust for this would be to reduce the majority threshold for `TRUE`, but it feels safer to rely on a majority vote here. Finally, even if the design works with an honest majority when the winner is clear, we ultimately still need to be attentive to the risks of builder–attester or builder–attester–proposer collusion.

An example of a problematic issue to consider. Say that Builder A can control 15 % of the attesters of the slot. If the race to provide the highest bid at the observation deadline is very tight between Builder A and Builder B, the remaining 85 % of the validators may for example be distributed as A = 36 % vs B = 49 %. Then Builder A can achieve the vote `TRUE` by relying on its control over the remaining 15 %. While early bidding and a high burn is incentivized, it can become a probabilistic game where builders may seek to influence attestations, which of course would be negative.

Curious to hear your thoughts!

## Replies

**jasalper** (2023-11-12):

This is an interesting idea but it seems that its effect is just shifting consensus earlier, as you’re still forcing the attesters of the committee to agree to what builder won.

At that point, why do you even need a proposer? Just have builders propose blocks and attesters determine which one becomes canonical by a majority vote.

---

**Nero_eth** (2023-11-12):

The attesters don’t decide which builder wins but they just enforce that the proposed block burns at least the mev-burn basefee floor. If not, they make sure it doesn’t become part of the canonical chain. Even with mev-burn, it’s the proposers that decides which block to propose and only the selected bid/block has a chance of becoming canonical.

There are more, much more fundamental differences between builders and proposers (slashability, CL rewards, etc) and under ePBS you would already have the builder propose a block (the EL block) while the proposer would still propose the CL block.

Simply saying that builders should propose the block and attesters should then somehow come to a conclusion which block among all the builders blocks is “the best” to become canonical falls short for many reasons.

---

**aelowsson** (2023-11-12):

They only need to agree that the winning block is at or above the payload base fee floor (and attest to timeliness etc.), so this is the same as in “a simple design”. The majority vote `TRUE` is not a requirement and simply produces a kickback to the winning builder.

A winning builder at the 10-second mark may still want to make further bids up until the proposer has selected a winning block for numerous reasons. There may be additional MEV so new competitive bids from other builders that also meet the payload base fee floor may come in. If the builder is certain that it won the auction, it has an edge against other builders, a size which depends on x, and can use that edge to bump up the payload tip. At the 10-second mark they may not include any payload tip at all (this design is generally pretty harsh to proposers, I guess it could be tuned if this idea is something to think more about).

[@Nero_eth](/u/Nero_eth) already got to the question of proposers while I was answering. I’ll add that one of those reasons is that it is not straightforward for attesters to come to an agreement on which block that was proposed at a specific deadline under asynchronous settings. There is possibly an alternative for the kickback though, where attesters vote on the winning builder id instead, generating a kickback xF to that id only in the case where a majority voted for it. But I haven’t thought it through, it would require thresholding stray votes with some rather complex changes to the attestation aggregation procedure (if at all possible), and this research area is not really my expertise. The same caveats as mentioned in the post, of builders influencing attesters, then apply.

---

**soispoke** (2023-11-12):

I think incentivising earlier bidding to deter builders from colluding is a really good idea! I was trying to understand if it would be “enough” by writing down some scenarios, and **Scenario 3** might still be an issue.

**Scenario 1:**

We let D be the beginning of slot N, while bidding happens during slot N-1.

Builder 1 bids D - 2 =  `1 ETH`

Builder 2 bids at D - 2 = `0.9 ETH`

Base Fee floor set by Builder 1 = `1 ETH`

Builder 1 bids at D = `1.2 ETH`

Builder 2 bids at D = `1.1  ETH`

Builder 1 gets selected by Proposer, profits from the difference between his bid value (`1.2 ETH`) and EL rewards (e.g., `1.15 ETH`) = `0.05 ETH`

Proposer profits: (Builder 1 bid value at D) - (Builder 1 bid value at D-2) = `0.2 ETH`

If your idea is implemented: Builder 1 gets additional rewards, corresponding to a proportion of the Base Fee floor, e.g., `5%`, so `0.05` * `1` = `0.05 ETH`. Total profits for Builder 1 = `0.05 ETH` + `0.05 ETH` = `0.1 ETH`

**Scenario 2:**

Builder 1 bids D - 2 =  `1 ETH`

Builder 2 bids at D - 2 = `0.9 ETH`

Base Fee floor set by Builder 1 = `1 ETH`

Builder 1 bids at D =  `1.1 ETH`

Builder 2 bids at D =  `1.2 ETH`

Builder 2 gets selected by Proposer, profits from the difference between his bid value (`1.2 ETH`) and EL rewards (e.g., `1.15 ETH`) = `0.05 ETH`

Proposer profits stay the same: (Builder 2 bid value at D) - (Base Fee floor) = `0.2 ETH`

If your proposal is implemented, no additional rewards for Builder 1 or Builder 2. Builder 1 profits = `0 ETH`, Builder 2 profits = `0.05 ETH`

**Scenario 3** (Builders <> Proposer collusion scenario):

Builder 1 bids at D - 2 = `0 ETH`

Builder 2 bids at D - 2 = `0 ETH`

Base Fee floor = `0 ETH`

Builder 1 bids at D =  `1.2 ETH`

Builder 2 bids at D =  `1.1 ETH`

Builder 1 gets selected by Proposer, profits from the difference between his bid value (`1.2 ETH`) and EL rewards (e.g., 1.15 ETH) = `0.05 ETH`

Proposer profits: (Builder 1 bid value at D) - ( Base Fee floor) = `1.2 ETH` - `0 ETH` = `1.2 ETH`

If the proposer wants to keep a tip of `0.2 ETH`, this mean it can rebate up to `1 ETH` to builders, so let’s say `0.5 ETH` each

If builders had not colluded, with incentivised early bidding, builders could’ve made up to `0.1 ETH`, but it’s still (a lot) lower than `0.5 ETH`  But in the scenario we described there is no additional profits for builders (5% of base fee floor = 0)

Of course if you have 10 colluding builders, and the proposer wants to reward them all equally, then the rebated value per builder goes down a lot, and **Scenario 3** is assuming full blown collusion between all parties involved.

I wonder if an added “bid validity condition” would help, something like: To be valid, bid at D should not exceed the Base Fee floor by more than a certain percentage, say 15% of that floor for example. It’s adding even more complexity, but it ensures builders have to set “reasonable” block base fees relative to their final bid at D?

---

**jasalper** (2023-11-12):

How do the attesters come to a consensus on what the mev-burn basefee floor is?

Are they only attesting if the block has a greater burn than what they locally think the basefee floor should be? Or does Attester 1 need to be able to verify that Attester 2 voted correctly?

If its a local comparison, then how does the proposer then know how much MEV actually needs to be burned for the block to become canonical? Presumably the builder/proposer will want to cut it close and only burn as much as is required, but no more. This could lead to many blocks not making the threshold when there is uncertainty around what it actually is due to a flurry of bids at the threshold deadline.

---

**aelowsson** (2023-11-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/jasalper/48/13925_2.png) jasalper:

> How do the attesters come to a consensus on what the mev-burn basefee floor is?

There is never a consensus on the burn base fee floor (in any of the designs), and it is not necessary. Each attester simply rejects any block below their subjective floor.

![](https://ethresear.ch/user_avatar/ethresear.ch/jasalper/48/13925_2.png) jasalper:

> Are they only attesting if the block has a greater burn than what they locally think the base fee floor should be? Or does Attester 1 need to be able to verify that Attester 2 voted correctly?

No verification is needed.

![](https://ethresear.ch/user_avatar/ethresear.ch/jasalper/48/13925_2.png) jasalper:

> If its a local comparison, then how does the proposer then know how much MEV actually needs to be burned for the block to become canonical? Presumably the builder/proposer will want to cut it close and only burn as much as is required, but no more. This could lead to many blocks not making the threshold when there is uncertainty around what it actually is due to a flurry of bids at the threshold deadline.

The honest proposer selects the block with the highest burn base fee floor and has 2 seconds of safety margin. If there is a block with a higher floor that they may miss, just around the start of the new slot (D+2), then the majority of attesters will not enforce such a floor. This is the point of the original design and remains the same. Thus, no substantial uncertainty exists if proposers play it safe. It is correct that if proposers do not play it safe, then they may miss their block and all rewards. Let’s review the game mechanics.

Builders are incentivized to win the auction at the observation deadline by providing as a high payload base fee as possible (the part that will be burned). Before this change, no such incentive existed, which is why we suspected a lower base fee floor. A short time after the deadline, some builders may focus on raising the payload tip, if they believe that proposers will select based on the payload tip. This is true also in the vanilla design, but there builders may opt for this strategy also before the observation deadline (if they bid at all). A realistic outcome (in both versions) is thus that both proposers and builders focus on raised payload tips after the observation deadline. Since a higher payload base fee under competition will lead to a lower payload tip, both parties are incentive-aligned as such. Builders will likely keep track of any raise to the payload base fee also after the deadline and make a probabilistic judgment on whether they need to match it. The decision will depend on if the raise happens at D+0.05 (proposers may wish to play it safe and treat it as the floor) or D+1.9 (proposer may be more confident, and not treat it as a floor that will be enforced). The decision will thus evolve with proposers’ behavior.

Some builders may target unsophisticated proposers by raising the payload base fee after the deadline and some may target sophisticated proposers by raising the payload tip. Some may run both strategies in parallel. Note that it is not possible to remove the payload tip, as it prevents giving an edge to proposers and builders that settle out-of-band after the observation deadline.

If there is substantial MEV but the payload base fee floor is very low around the observation deadline, a builder that wishes to cause consensus instability may provide a bid just at the deadline that makes it impossible to match when providing any relevant payload tip, and hope that the proposer gambles by ignoring it. Thus it is not a flurry of bids per se that is the risk, but rather that the bids just at the deadline differ substantially from the bid before the deadline. The vanilla design will be susceptible to such an “attack”, but on the other hand it does not provide any incentives for bidding just around the deadline at all.

The change will give builders an incentive to provide bids that are within the deadline so that they win the auction. There would in that way be less possibility for an “attack” that seeks to cause consensus instability. However, there are scenarios where builders strategically wait to provide bids until just around the deadline. If this is a concern (**and it does seem pretty valid!**), the deadline for selecting the subjective winner could be shifted to be slightly before the deadline for selecting the subjective base fee floor. The proposer will then always select a bid that at least matches the winner of the auction and not gamble. It will then also not be possible for an attacking builder to subject the proposer to substantial opportunity costs by bidding when attesters set the base fee floor, without also taking on an expected loss.

---

**Nero_eth** (2023-11-13):

For scenario 2, I’d agree that builder 2 get selected, assuming that the latest bid of builder 2 also burns the payload basefee floor established at d.

In general, from the perspective of the proposer, it’s the safest to select the bid that maximizes the burn. This gurantees that every attester is fine with the burnt amount.

Though, it’s interesting to think of scenarions in which the final bids vary in the amount they burn:

Builder 1 bids D − 2 = 1 ETH

Builder 2 bids at D − 2 = 0.9 ETH

The true basefee floor (as determined by the attesters)  = 1 ETH

Builder 1 bids at D = 2 ETH, with the floor set to 1 ETH

Builder 2 bids at D = 2 ETH with the payload base fee set to 1.1 ETH

In this scenario, a tip-maximizing proposer would be like “ok, I’ll take the bid of builder 1 as it offers me a greater tip (1 ETH vs 0.9 ETH)”. On the other hand, a very cautious proposer might prefer to select the bid of builder 2 as it will more likely satisfy the payload basefee floor. As Anders pointed out in the comment above, the final outcome will likely depend on the exact timing of the bids. If you’re a very well connected validator and there is a bid that comes in exactly at D, increasing the payload basefee floor, then the proposer might ignore it, trusting that the attesters (that are not that well connected) might not have seen it before D. If you’re a badly connected validator, you might want to maximize the burn to to be on the safe side.

Scenario 3 assumes that all builders collude without any builder left setting the floor, although, as of Ander’s proposal, there is an incentive to do so. The proposer would have to set up the incentives to collude before knowing how much “bribe” is needed to convince every builder to not bid before the floor is set. This would then not only present a collusion between proposer and builders but also among the builders themselves which would already be possible today (builders extracting mev but not paying anything to the proposer).

---

**quantumtechniker** (2023-11-13):

(post deleted by author)

---

**jasalper** (2023-11-13):

> The honest proposer selects the block with the highest burn base fee floor and has 2 seconds of safety margin. If there is a block with a higher floor that they may miss, just around the start of the new slot (D+2), then the majority of attesters will not enforce such a floor. This is the point of the original design and remains the same. Thus, no substantial uncertainty exists if proposers play it safe.

The “honest” proposer in this case is not acting rationally - the rational action is to select the highest tip with the payload base fee high enough to be accepted by the required percentage of attesters. This is not particularly sophisticated behavior - I think it is safe to assume that a high percentage of validators would be running this strategy. Agree with your assessment in the next paragraph:

> A realistic outcome (in both versions) is thus that both proposers and builders focus on raised payload tips after the observation deadline. Since a higher payload base fee under competition will lead to a lower payload tip, both parties are incentive-aligned as such. Builders will likely keep track of any raise to the payload base fee also after the deadline and make a probabilistic judgment on whether they need to match it. The decision will depend on if the raise happens at D+0.05 (proposers may wish to play it safe and treat it as the floor) or D+1.9 (proposer may be more confident, and not treat it as a floor that will be enforced). The decision will thus evolve with proposers’ behavior.

> Thus it is not a flurry of bids per se that is the risk, but rather that the bids just at the deadline differ substantially from the bid before the deadline.

I’m not describing an intentional attack. If we look at bidding behavior with a fixed deadline and public information, bidders wait until they approach the deadline and in the last few moments submit a flurry of increasing bids in response to each other. As a result, in a relatively short amount of time, the MEV bid is likely to go from ~zero to potentially the full payload base fee floor. Given latency considerations, the observed winner of these bids may be pretty widely distributed across attesters.

Depending on the value of the MEV in that block vs the consensus rewards, rational proposers will take higher risks during high-MEV periods where they’ll select blocks with a comparatively lower base fee floor, but higher risk of not being confirmed by the attesters. (As the expected value of a x% lower basefee-floor will be worth more than the consensus rewards).

---

**aelowsson** (2023-11-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/jasalper/48/13925_2.png) jasalper:

> The “honest” proposer in this case is not acting rationally - the rational action is to select the highest tip with the payload base fee high enough to be accepted by the required percentage of attesters. This is not particularly sophisticated behavior - I think it is safe to assume that a high percentage of validators would be running this strategy. Agree with your assessment in the next paragraph:

Yes, this is well understood and we are in agreement. This [thread](https://x.com/casparschwa/status/1660931518791909376)  may interest you.

![](https://ethresear.ch/user_avatar/ethresear.ch/jasalper/48/13925_2.png) jasalper:

> I’m not describing an intentional attack.

Also well understood. But to determine the safety of a change to the spec, we must include in the analysis the outcome when someone “attacks” the consensus mechanism. In the vanilla design, the motivation for a builder to place a bid with a high payload fee exactly at the deadline would primarily be to cause disruption, and then gain from that through more complex avenues. I therefore noted that the presented change to the MEV burn implementation removes the opportunity for builders to execute such an attack without also taking on an expected loss.

![](https://ethresear.ch/user_avatar/ethresear.ch/jasalper/48/13925_2.png) jasalper:

> If we look at bidding behavior with a fixed deadline and public information, bidders wait until they approach the deadline and in the last few moments submit a flurry of increasing bids in response to each other. As a result, in a relatively short amount of time, the MEV bid is likely to go from ~zero to potentially the full payload base fee floor. Given latency considerations, the observed winner of these bids may be pretty widely distributed across attesters.

This auction will not have a fixed deadline in the classical sense, since some latency/asynchrony can be expected. Furthermore, the winning builder needs to be selected by a majority of attesters to reap rewards from the auction. Being a plurality winner of the initial auction is of little use to a builder, and this will substantially affect the bidding behavior. The expected outcome can only be modeled in light of the provided incentives (and given circumstances) for each individual agent. A few conclusions are immediately obvious. Under perfect competition, with some latency, and honest attesters:

1. Builders will try to estimate the expected full MEV of the entire block V_e before the observation deadline, and will at most bid slightly below \frac{V_e}{1-x}. Note thus that bids can be higher than V_e, due to the potential, in expectation, of profiting xV_e in the best-case scenario. This means that the mechanism can burn rather close to the entire MEV, subtracting builders’ aggregated costs (including capital costs), etc. We can assume that the variable x will influence the builder landscape.
2. Bids will not immediately be viewed by all attesters once placed. Builders that want all attesters to review their bid before each attester determines a subjective winner must provide a competitive bid early enough for full propagation. Not doing so will reduce their chance of becoming the majority winner of the auction (the only type of win that counts).
3. Builders will try to estimate the expected bids of other builders before placing their first bid, and update their estimate of forthcoming bids based on any observed bids. The goal is to become a majority winner by placing the last bid as low as possible, and always below \frac{V_e}{1-x} (unless when punishing some builder in an attempt to uphold a cartel, etc). Since the win may not stem from a single bid, but rather a series of increasing bids, the optimization game is rather complex.
4. The opportunity to extract MEV will vary between builders across blocks. Blocks allowing for greater specialization may be more likely to produce a majority winner.

![](https://ethresear.ch/user_avatar/ethresear.ch/jasalper/48/13925_2.png) jasalper:

> Depending on the value of the MEV in that block vs the consensus rewards, rational proposers will take higher risks during high-MEV periods where they’ll select blocks with a comparatively lower base fee floor, but higher risk of not being confirmed by the attesters. (As the expected value of a x% lower basefee-floor will be worth more than the consensus rewards).

Right, so to summarize the situation based on my current and previous comments:

**A.** Under competition, builders that wish to become majority winners will need to start making competitive bids early enough such that they are seen by a large majority of attesters before the deadline. These bids will determine the opportunity cost that a gambling proposer faces. Presumably, the difference between these early bids (that still must win in some attesters’ view), and any updated bids that not all attesters have time to see, may not be that great. Therefore, there will be no expected profit from gambling.

**B.** As mentioned in the previous comment, concerns may however still remain pertaining to, for example, certain phases of imperfect competition or degraded network conditions. Therefore:

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) Anders Elowsson:

> the deadline for selecting the subjective winner could be shifted to be slightly before the deadline for selecting the subjective base fee floor.

Such a shift would in that case alleviate concerns, because it minimizes the opportunity cost of selecting a block with a payload base fee above the payload base fee floor.

---

**soispoke** (2023-11-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> If you’re a very well connected validator and there is a bid that comes in exactly at D DD , increasing the payload basefee floor, then the proposer might ignore it, trusting that the attesters (that are not that well connected) might not have seen it before D DD .

Did you mean D -2 here? The bids coming at or around D don’t increase the payload basefee floor right?

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> Scenario 3 assumes that all builders collude without any builder left setting the floor, although, as of Ander’s proposal, there is an incentive to do so.

Yeah I agree, I was just saying the incentives to collude might be higher than `x` in some cases.

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> This would then not only present a collusion between proposer and builders but also among the builders themselves

Also agree that both builders and proposers would have to collude for Scenario 3 to play out (that’s what I meant when I wrote: “full blown collusion between all parties involved”), but I don’t think *not knowing how much bribe is needed* is enough to deter collusion in that case.

One last point, is you mention collusion between builders is possible today and it’s true, but I still don’t think it’s necessarily a good reason to be comfortable with enshrining it in the protocol, with validators having very few options to respond (won’t even be able to go back to local block building) if it happens.

---

**Nero_eth** (2023-11-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/soispoke/48/12076_2.png) soispoke:

> Did you mean D -2 D−2D -2 here? The bids coming at or around D DD don’t increase the payload basefee floor right?

Oh yeah, meant D-2 - thanks. And yeah, only what comes before D-2 can impact the basefee floor. As a badly connected validators, bids coming in exactly at D-2 could potentially still raise the floor, thus, for such validators it’d be beneficial to accout for them. For well connected validators, bids raising the floor at D-2 could be ignored under the assumption that not all validators are that well connected and might have seen the bid later.

This potentially introduces a source of centralization. Large pools can play with their setup and fine-tune it while solo-stakes are almost forced to maximize the burn in order to make sure that they get the CL rewards and not getting reored out. Also, solo-stakes who propose a few blocks per year cannot really fine-tune their setup as it’s just too risky. The outcome could be that staking pools achieve better APYs than solo stakers.

![](https://ethresear.ch/user_avatar/ethresear.ch/soispoke/48/12076_2.png) soispoke:

> One last point, is you mention collusion between builders is possible today and it’s true, but I still don’t think it’s necessarily a good reason to be comfortable with enshrining it in the protocol, with validators having very few options to respond (won’t even be able to go back to local block building) if it happens.

This is an important point yeah. With MEV-Burn inplace, local block builder might potentially not produce good-enough blocks to burn the agreed payload basefee floor. This would lead to vanilla building completely dying out.

---

**aelowsson** (2023-11-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> This potentially introduces a source of centralization. Large pools can play with their setup and fine-tune it while solo-stakes are almost forced to maximize the burn in order to make sure that they get the CL rewards and not getting reored out. Also, solo-stakes who propose a few blocks per year cannot really fine-tune their setup as it’s just too risky. The outcome could be that staking pools achieve better APYs than solo stakers.

This proposal is designed to burn almost all MEV income for proposers. The auction at the observation deadline is in a way a slot auction masquerading as a block auction. Builders have incentives to bid up to, and even above the expected value of the MEV for the entire slot, since they stand to receive a kickback if they win. A winning builder will update their payload after the observation deadline and provide a small tip so that the proposer includes the updated payload in the slot. Builders that do not win will presumably have worse opportunities to extract MEV and on top of that cannot receive the kickback. They therefore do not have incentives to raise the payload base fee after the observation deadline, because if they then win the proposer auction, they will take a loss.

Now, there will of course be many cases where builders hold back a little in the auction (perhaps to compensate for the prospect of not having a clear winner) or where some late burst of MEV comes in, etc. But it is still reasonable to expect a tempering of block proposals just after the auction, with rather small bumps to the payload base fee, if any, and then potentially some final bidding closer to the end of the proposal auction. Therefore, it seems to me that this effect, while existing, should overall not be that significant in turns of value (at least in the version with an auction design). Especially since the auction can be positioned slightly before the point where the base fee floor is set if necessary. If you can raise the base fee just after the auction, you could just have raised it before, or at least will not be able to raise it by that much without the prospective of taking on a loss.

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> With MEV-Burn inplace, local block builder might potentially not produce good-enough blocks to burn the agreed payload basefee floor. This would lead to vanilla building completely dying out.

MEV burn does not materially alter the situation, merely our perception of it. It is not possible today for vanilla builders to build good enough blocks to receive the available MEV value. This is what has led to vanilla building being rather uncommon. Implementing MEV burn does not remove the ability to build blocks for anyone, and does not substantially alter the real economic consequences of such a decision. As a comparison, if the subsidy is bumped for stakers to keep the yield the same before and after implementing MEV burn, then, over time, the outcome for vanilla builders will essentially be the same under the current situation and with MEV burn. The potential “donation” from the vanilla builder to transacting users is not altered in substance.

Of course, our perception of the two situations may be very different, but this is mainly a question of educating users. The current vanilla-builder situation is like an employee who donates the bonus that their employer randomly hands them once in a while. The MEV-burn situation would then be vanilla builders as an employee with a slightly higher salary who donates the difference whenever they once in a while see a poster for a charitable cause. Now if that charitable cause only accepts donations of one million dollars, then the employee may need to avoid donating this one time. We can certainly expect prospective vanilla builders to incorporate a check on the payload base fee floor relative to what they can extract themselves, to ensure that the decision to self-build will not affect them too negatively. Variability may in this way prevent vanilla builders from building their blocks in *some* cases, if a big MEV opportunity arises.  But we must then remember a big advantage of MEV burn—that variability for the more typical solo staker is removed, which is a big win. In many cases, we also specifically would like to burn that big MEV opportunity anyway, to prevent it from falling into the hands of the next proposer.

If the base reward factor is not bumped, such that the yield falls with MEV burn, then the required “donation” will be a larger proportion of rewards than before MEV burn. But that is an effect of an underlying change to the issuance policy, something which is a separate conversation. Reducing the base reward factor right now without MEV burn would have a similar effect on vanilla builders. They’d be forced to forego a larger proportion of their rewards.

I will provide a more extensive write-up on the proposal in a short while.

![](https://ethresear.ch/user_avatar/ethresear.ch/soispoke/48/12076_2.png) soispoke:

> you mention collusion between builders is possible today and it’s true, but I still don’t think it’s necessarily a good reason to be comfortable with enshrining it in the protocol, with validators having very few options to respond (won’t even be able to go back to local block building) if it happens.

If builders indeed collude, then vanilla building becomes very cheap. Not sure if I am missing something there.

