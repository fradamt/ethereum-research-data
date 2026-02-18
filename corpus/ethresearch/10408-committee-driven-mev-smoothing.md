---
source: ethresearch
topic_id: 10408
title: Committee-driven MEV smoothing
author: fradamt
date: "2021-08-23"
category: Economics
tags: [mev]
url: https://ethresear.ch/t/committee-driven-mev-smoothing/10408
views: 20820
likes: 27
posts_count: 7
---

# Committee-driven MEV smoothing

# Committee-driven MEV smoothing

---

*Many thanks to Justin Drake, Barnabè Monnot, [Caspar](https://twitter.com/casparschwa) and others from the EF research team for helpful comments and discussions. Caspar also directly contributed to parts of the main write-up*

Smoothing MEV means reducing the variance in the MEV that is captured by each validator, with the ultimate goal of getting the distribution of rewards for each validator to be as close as possible to uniform: a staker would then get a share of rewards proportional to their stake, just like with issuance. This is in my opinion the single most impactful consensus-level MEV mitigation that is potentially available to us, and strictly more powerful than democratization. Details about why and explorations of many more aspects of this proposal are in this [longer write-up](https://notes.ethereum.org/cA3EzpNvRBStk1JFLzW8qg), to which I’ll refer interested readers a few times (if you want to start reading there directly go ahead, but keep in mind that I am still working on it).

In the following, I am going to propose a mechanism which attempts to achieve MEV smoothing by equally sharing a block’s MEV among the committe members and the proposer (meaning that the proposer is treated the same as any individual committee member, but this could of course be changed). Doing so requires two ingredients: a well-functioning block content market, as in [the builders/proposer separation proposal](https://ethresear.ch/t/proposer-block-builder-separation-friendly-fee-market-designs/9725), and some relatively mild consensus modifications.

### Attestations

Given the existence of a block content market, we assume that at attestation time each committee member has their own view of a block with maximal payment, received within the prescribed time window. In particular, consider committee member v_i, with validator index i, whose current view is that the payment-maximizing block is b_i, making a maximal payment p_i. v_i would then attest as follows:

- Attest to a newly proposed block if these conditions are all satisfied:
a) A block has been timely proposed, i.e. it has been received by v_i before a specified deadline (currently 4 seconds after the beginning of the slot)
b) The block extends what in v_i's view is the previous head of the chain
c) The block makes a payment p such that p \geq p_i
- Otherwise, attest to the previous head of the chain.

Conditions a) and b) are the same as now, but we add the maximality condition c). Nonetheless, we still have essentially the two options block present vs block absent, except that a proposed block is considered absent if its payment is sub-maximal. The actual attestation rules can be more complicated than this, as we’ll see shortly, but the main point is that we can always ensure maximality by adding condition c) and requiring that an absolute majority of published attestations deems it fulfilled. If the supporting attestations are outnumbered by attestations to the previous head of the chain, the slot should be skipped.

By attesting this way, the committee is essentially trying to coordinate the execution of a tit-for-tat strategy, punishing non-cooperating proposers to achieve a long-term cooperative equilibrium.

### Fork choice rule

The way the fork-choice rule currently operates does not allow for such a strategy. It operates on blocks, not on (block, slot) pairs: attestations to the absence of a block are actually just attestations to the previous head of the chain. This implies that a block that correctly extends the previous head of the chain always becomes the new canonical head of the chain, regardless of how the committee attests. The attestations are immediately relevant only if the proposer has forked the chain.

What we need is instead that a block becomes the new head of the chain only if it receives a majority of the published attestations. Basically, we need a proposed block to be in competition with the empty block. In the diagram below, B is proposed at slot 1 with predecessor A, but it gets fewer attestations than the ones against it, and the canonical chain becomes the one with an empty slot 1.

[![](https://ethresear.ch/uploads/default/original/2X/3/32b24c8e2d25e3b97876749226c788e0e1581aab.png)627×340 5.02 KB](https://ethresear.ch/uploads/default/32b24c8e2d25e3b97876749226c788e0e1581aab)

More formally, we can think about it with (block, slot) pairs as the competing attestation targets:

[![](https://ethresear.ch/uploads/default/original/2X/0/04d47c9d4cc6c95070f61b04d5c93bdb213d0217.png)526×342 6.36 KB](https://ethresear.ch/uploads/default/04d47c9d4cc6c95070f61b04d5c93bdb213d0217)

[(block, slot) attestations have been frequently discussed](https://github.com/ethereum/consensus-specs/pull/2197) and ultimately it has always been decided against them, because they create a hard latency costraint for liveness. With current parameters, they would cause any block which does not make it to 50% of attesters within 4 seconds (the attestation deadline) to be skipped, and so under bad network conditions liveness can be threatened. We can maybe mitigate this issue with an alternative design which avoids conflating late blocks and non-maximal blocks, but some tradeoffs remain (among which increased complexity). I am discussing this in some detail at the very end of the full write-up, but keep in my mind that it’s just ideas at this stage.

### A proposal’s lifecycle

To give a full picture of the how a block makes its way to the canonical chain, let’s focus on a specific version of the builders/proposer separation scheme, specifically Idea 1 from the post. The steps are almost the same, except we need to add a deadline for builders’ block headers to be considered by attesters in their assessment of the maximal payment. Without one, one could always publish block headers with high payments that are too late to be seen and chosen by the proposer, but still cause attesters to update their view of the maximal payment.

The process would look something like this, with some delay between each step and with attesters being asked to enforce the deadlines in their attestations:

- Block headers deadline: builders publish block headers before this time. Attesters accept block headers published after the deadline, but they don’t consider them in their view of the maximal payment. This deadline can overlap with the previous slot.
- Proposal deadline: the proposer publishes its choice of a block header before this time.
- Block body deadline: the chosen builder publishes the body corresponding to the chosen block header before this time
- Attestation deadline: at the latest, attesters publish their attestations at this time

Note that this specific version of builders/proposer separation requires its own consensus modifications, with three attestation options:

- Block proposal absent
- Block proposal present but bundle body absent
- Block proposal present and bundle body present

Nonetheless, as already anticipated, the changes we need for our smoothing scheme can be simply applied on top, by again equating “block proposal present” with the three conditions a,b,c we identified previously (i.e. by adding c to the second and third attestation options) and skipping the block if “block proposal absent” has an absolute majority over all published attestations.

## Security

One immediate worry when introducing another aspect to the attestation process is whether or not an adversary can attempt to manipulate attesters’ views to produce undesirable outcomes. In particular, let’s consider how a committee member’s view of the maximal payment can differ from the real one:

- View > Reality: without the block headers deadline it is definitely possible to execute an attack using ideas from this post, by releasing a block header with a high payment at a time such that more than 50% of the committee is going to see it in time but the proposer won’t, which would cause the block to be rejected.
 With a deadline for block headers which is sufficiently in advance of the proposal time, this attack vector is no longer feasible and the ability to delay messages to the proposer is required. There’s also a high cost of failure, because the proposer seeing the header in time would lead to having to make the very high promised payment.
 Finally, even an adversary that is able to target specific proposers and cause their incoming messages to be delayed would be unable to execute such an attack if the proposer were to be chosen through a single secret leader election
- View < Reality: attesters whose view of the maximal payment is lower than what it should be will anyway always attest correctly when the proposer is honest. The only mistake they can make is attesting to a sub-optimal block. For a block to be sub-optimal, by definition there has to be a block header which offers a higher payment, because we define optimality through the block content market. That also means that there is a builder who made this maximal block and wants to see it published, and is therefore interested in having as many committee members as possible receiving it in time, thereby preventing competing sub-optimal blocks from being viable choices. We rely on the self-interest of such builders to make sure that committee members don’t have a sub-optimal view of the payment, at least as long as the adversary does not have too much control over network delays.

### Incentive compatibility

The main concern we have is not about potential manipulations of the views of committee members, but about whether or not the mechanism is incentive-compatible. Crucially, is it incentive-compatible for committee members to vote against sub-optimal blocks, preventing malicious proposers from getting more than their fair share of MEV?

Here are some reasons why I think this scheme is indeed long-term incentive-compatible:

- The long-term result of correctly participating in this scheme is that MEV is more or less evenly distributed, much more so than currently. For sufficiently large staking pools, this is no different than the status quo, because in a short period of time they already achieve the mean of the distribution of rewards, because of how often they propose. For everyone else, this is better than the status quo, because they are likely to earn more than before, though they sacrifice some low-proability higher upside (check the full write-up for details about what a smoothed vs non-smoothed distribution of rewards looks like, and how it impacts various participants).
- Consider the single-block game between the proposer and the commitee, where the latter is seen as a single player and the proposer moves first. Defecting means not following the protocol. For the proposer, that is proposing a block which does not make a maximal payment, and instead gives them an undue portion of the MEV. For the committee, that is accepting such a non-maximal block, or failing to accept a maximal one. Here’s the payoff matrix for this game:

|  | Proposer is honest | Proposer defects |
| --- | --- | --- |
| Committee is honest | (1,1) | (0, 0) |
| Committee defects | (0,0) | (0.5,2) |

 In this single-block game, the dominant strategy for the proposer is to always defect, because the committee always prefers to get something rather than nothing, i.e. to cooperate. On the other hand, in the repeated form of the game the committee can employ a tit for tat strategy, which corresponds to voting honestly and punishing non-complying proposers. In the long term, this should ensure a cooperative equilibrium. Moreover, as you can read in a section “Short-term considerations” in the full write-up, committee members from large pools have a very different payoff matrix in which the payoff for defecting with the proposer is very low or even negative.
- This game is of course very simplified. In reality, the committee is not one entity, and actually some of its validators will often share interests with the proposer (at least anytime in which the proposer belongs to a sufficiently large staking pool, which happens proportionally to the stake that’s held in such pools). Moreover, a validator that’s a committee member for one block will later be a proposer for a different block, so players really play both sides.
 Nonetheless, playing a proposer-friendly long-term strategy is just an attempt to keep the status quo, which as already mentioned does not particularly benefit anyone in terms of rewards. Large pools do benefit from the status quo in that their ability to achieve average rewards gives them an edge in attracting stake, but on the other end fostering staking decentralization can be a net-positive for the whole Ethereum ecosystem and increase the total value of the stake that pools compete for. Moreover, there’s a clear reputational cost that comes from subverting the protocol in an easily attributable way, especially for large pools and especially when it comes to a mechanism that’s common good-oriented.

## Consensus stability

Both the current fork-choice rule and the one proposed for this scheme are vulnerable to 51% attacks, with the only difference being that in this scheme a 51% coalition can immediately vote down any minority block, whereas currently it takes some time to convince the minority to join the majority chain (which is necessary to eventually achieve finality). Therefore, we should only worry about consensus instability created by adaptive adversaries which do not have control of 51% of the stake but can try to achieve such control over specific committees.

Currently, a committee does not get value from the content of a block, but just from coordinating the consensus process. Thus, no one outside of the proposer (and whatever amount of stake they represent) has a reason to do anything to steal MEV by forking. Stealing MEV from the previous block requires the proposer’s coalition to bribe other attesters, and without network attacks the total adversarial percentage in the two committees (including bribed members) has to add up to 2/3 of them (so that votes are 1/3 + 1/3 by the honest attesters and 0 + 2/3 by the adversarially controlled ones). On the other end, in this scheme controlling 51% of both committees is enough, because the first block can now directly be skipped, and committee members can have their own incentives to try to fork to steal MEV, because they share the benefits. Nonetheless, the situation is still arguably much better:

- Crucially, proposers from large staking pools have no incentive to fork to steal MEV, because they control about the same percentage of every committee, and thus get about the same percentage of each block’s rewards (within fairly tight bounds, even for proposers controlling only a single-digit percentage of the stake). Since large pools are the most powerful actors, and are potentially able to coordinate, disincentivizing them from attacks is arguably the single most important defense.
- If the proposer is a solo validator or anyway a small staker, they might want to capture a share of the previous block’s rewards, because they didn’t receive any of it. On the other end, a staker that’s small enough to not have participated in the rewards meaningfully is very ill-equipped to successfully fork. They essentially have no committee power of their own, and would need to convince everyone else. Pools are especially hard to convince, for the same reason why they don’t have a reason to fork, and it’s hard to imagine forking without the support of any large concentration of stake. Lots of other solo validators might have incentives to fork, but it’s hard to imagine adaptively bribing such a large coalition of small stakers

## Censorship resistance

The block content market could be very centralized, and it seems likely it will be. Either way, we have no control over whether that is the case. Censorship resistance would then heavily rely on the assumption that altruistic proposers would step up and utilize their discretion in choosing block headers to combat censorship when needed, for example by making their own blocks. This is not possible with MEV smoothing, because MEV maximization is enforced, and we therefore need to explore other solutions. I have started doing so in the full write-up, in the section “Censorship resistance by decoupling transaction inclusion and ordering”. I decided to not add any details about that here to keep the post contained and because there might be issues with the idea, but the tldr is that we could have the proposer of slot n-1 select a set of transactions for inclusion at slot n, without this interfering with the smoothing mechanism.

## Replies

**samueldashadrach** (2021-08-26):

Interesting proposal but I think the 4 second liveness requirement needs to be more seriously considered. IMHO the first principles for any design need to be - does this proposal increase ethereum’s consensus stability and censorship resistance against wealthy and state-level actors.

If I summarise (please correct me if I’m wrong)

Pros:

- more consensus stability due to less reorgs
- fairer MEV distribution which leads to less centralisation of validator pools which leads to less coercive control on ethereum by nation states

Cons:

- easier for state level actors to disrupt the network with bad network conditions or incentivised DOS
- harder to run validators through private networks such as mixnets and Tor [1][2]

More exploration of cons may be helpful to show that the pros are indeed more significant.

---

**fradamt** (2021-08-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/samueldashadrach/48/6197_2.png) samueldashadrach:

> Pros:
>
>
> more consensus stability due to less reorgs
> fairer MEV distribution which leads to less centralisation of validator pools which leads to less coercive control on ethereum by nation states

Another potential pro is the ability to do MEV democratization, which I think most would agree is necessary, without giving up too much censorship-resistance. The latter really depends on altruism in the normal builders/proposer separation scheme, whereas I think with MEV smoothing we can do away with this requirement. I talked about it in the writeup, but definitely take this with a grain of salt because it’s an idea from a few days ago.

A more clear pro is the following: it should make MEV income management for staking pools and SSV solutions much easier. The question with all of these is, how is MEV distributed? How much does the pool get, how much the stakers? For SSV, if the internal consensus is leader-based, is the leader going to share the MEV? And how do we verify that the distribution is being done correctly? The reason why these questions are not trivially solved is that detection of MEV is not easy at all, and attribution is even harder: good luck trying to tell how much money a pool actually made on a block. Even with the builders/proposer separation scheme, the payment accepted by the proposer is not reliable in this sense: a block builder could bribe a pool to have them accept blocks with sub-optimal payments (which are the part that stakers can easily request a share of, even directly on-chain), effectively funneling MEV away from the stakers and to the pool.

With this scheme, and given a minimum of competition in the block content market, such deals should not be possible, because maximality is enforced (and all builders have an incentive to make sure that their block reaches everyone, if they produce a good one), so the amount of payments which are funneled away from the transparent payment mechanism should be minimal. Basically the accepted payments should work as a somewhat reliable MEV oracle. Distribution of rewards can then be even entirely on-chain, without  the need to have any complex monitoring system. Besides, if you really wanted to build a monitoring system that works, what you’d do is probably try to get a good view of the block content market and use that as a proxy for MEV. Now this view is accessible on-chain, and the builders are incentivized to make it reliable.

![](https://ethresear.ch/user_avatar/ethresear.ch/samueldashadrach/48/6197_2.png) samueldashadrach:

> I think the 4 second liveness requirement needs to be more seriously considered.

This is definitely a major concern, as far as I can tell the main one. I am working on an idea which wouldn’t have this requirement, because it avoids conflating late blocks with non-maximal blocks. It does have other tradeoffs and at this stage it could well be completely broken, but I think it at least shows that there’s a design space for solutions which don’t have this constraint, and compromise elsewhere.

Also the 4 seconds is a parameter. Of course it can’t be made super long, but it could be made longer if the tradeoffs were deemed to be favorable.

![](https://ethresear.ch/user_avatar/ethresear.ch/samueldashadrach/48/6197_2.png) samueldashadrach:

> harder to run validators through private networks such as mixnets and Tor [1][2]

I wasn’t aware of this problem, I’ll read up on it ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

I am not aware of a lot of things, as I am fairly new to Ethereum and cryptocurrencies in general, so thank you for the feedback and for pointing out where further exploration is needed!

---

**samueldashadrach** (2021-08-26):

Thanks for the response!

Better income management for staking pools does not seem a significant advantage when compared against censorship resistance of the base protocol imo.

Minimising off-band payments is good but imo it is good *only* because that prevents validator pool centralisation and kingmaking. Need to make sure that when we try to improve one form of censorship resistance (incentivise more diverse validator set), we are not trading away another important form of censorship resistance (latency and DOS protection requirements).

Hence think it’ll be useful to study latter that’s all ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**casparschwa** (2021-08-26):

Fantastic idea. Here is my personal tl;dr in case that’s useful to anyone:

- We are assuming a functioning proposer/block builder separation-friendly market.
- Block builders signal a payment that is shared between block proposer and committee members of that slot, if their block is proposed. The highest of of all such signaled payments is called the maximal-payment p
- Block proposer should propose a block with a payment that offers at least p
- Committee members will only attest to the block if the proposed block’s payment is greater or equal to the maximal-payment, i.e. p_i \geq p (in addition to the usual fork choice rules).
- This payment p_i is shared equally between the block proposer and all committee members of a given slot. This is the crucial idea. Instead of smoothing MEV across slots (as often discussed), here it is proposed to share it with committee members of the same slot.
- The intuition is simple: As a committee member I only attest to a block that is proposing to share at least the maximal-payment that is known to me locally.
- This requires (block, slot)-voting, because attestors need a way of expressing an opinion: whether the proposed block is good enough or if the proposed block’s payment is not maximal (read: “screw you, you’re not sharing enough payment with us, so we are not attesting to your block”).

Simply voting for the last head of the chain does not work, because the to-be-rejected-proposed-block is built on that block and would inherit all its weight and thus become canonical…

(block, slot)-voting is problematic, because it introduces latency constraints of `SECONDS_PER_SLOT / 3`, which is the amount of time after which an honest validator is supposed to attest even if it hasn’t heard about a block for the current slot. So if within 4 seconds a validator does not hear a block it will vote for an empty slot. As a consequence honest, but slightly late block proposals will be orphaned.
There are ideas for replicating (block, slot)-voting functionality without introducing latency constraints. Read more in the [long form note](https://notes.ethereum.org/cA3EzpNvRBStk1JFLzW8qg#Changing-the-fork-choice-rule-to-allow-MEV-smoothing-without-latency-constraints).

- tl;dr: Attestations in slot n not only vote for a source, target and head, but also attach their local view of the max-value p_{i,n}. This helps because blocks publish a payment value p_{n} (to be shared across committee and proposer), and so we can compare the attestation’s p_{i,n} value to the block’s p_{n} value. But then there are new, different issues…

imho finding a workaround for (block, slot)-voting is the heart of the matter to solve.

---

**pmcgoohan** (2021-08-29):

Unsurprisingly for you [@fradamt](/u/fradamt) there is some good data and analysis in here and I respect the time and effort you have put into this. You know I have no time for MEVA, especially in the base layer, but as well as that I don’t see that smoothing achieves much here.

“…with the ultimate goal of getting the distribution of rewards for each validator to be as close as possible to uniform: a staker would then get a share of rewards proportional to their stake”

The staker already gets a share of rewards proportional to their stake. Smoothing out returns makes no difference to their profits over time because the [expected value](https://en.wikipedia.org/wiki/Expected_value) does not change however much you smooth. I know first hand because my income over the last 19 years has literally been based on this fact. The ev of a staking pool will always be lower (and therefore less attractive to a rational actor) than the ev of running your own validator, and smoothing does not impact this.

If there was a risk element to validators extracting MEV (ie: if they could lose MEV as well as win it) then you would have some argument because there would be a risk of ruin from the variance. To mitigate this optimally requires the application of the [Kelly criterion](https://en.wikipedia.org/wiki/Kelly_criterion) which benefits those with a bigger bank.

But there is zero risk of loss with MEV extraction, so this is not a factor. MEV extraction is a “bet to nothing” which is one of the most prized outcomes for traders and professional bettors.

So while there is no rational basis for finding a smoothed return to be desirable, you could argue that psychologically stakers prefer smoother returns and a steady income- but that is a subjective opinion.

I could just as easily argue that validators who are already getting a steady income from block rewards and gas might find the lottery aspect of massive outlier wins from MEV extraction more exciting/attractive, especially when the odds are stacked in their favour. The popularity of the national lottery, premium bonds and Las Vegas supports my thesis. Degen culture suggests this is likely also true in the Ethereum community. Anyway, my point is that it is cultural not rational or mathematical.

At the end of the day (and from previous conversations with you I think you get this actually) the MEV problem is not one of how to distribute extracted value, the problem is that value can be extracted from users in the first place.

If we are going to address MEV in the base layer and modify attestations (and I absolutely think that we should) I’d like us to be reducing the MEV that can be extracted (like… ahem… in a content layer).

I would love to see you direct your obviously wrinkly brain away from MEV redistribution and towards mitigation.

---

**pmcgoohan** (2022-08-30):

A reminder that this proposal forces validators to select the builder with the highest bid block.

This means:

- validators in different legal jurisdictions to the dominant builder may be forced to power down rather than accept non-compliant blocks (same goes for crList)
- individual validators have little resistance if the dominant builder starts censoring
- makes cornering order flow, CaaS and unstaked hijacks etc harder to mitigate
- robs validators of their ability to choose altruistic forms of ordering that don’t frontrun or censor users (also making it likely that many will power down instead due to moral or legal concerns), which also represents a huge legal/regulatory risk to Ethereum
- if a dominant builder is also a large stake holder (eg: a pool), it prevents validators from choosing a different builder to mitigate further centralization

Some (but not all) of these problems go away if we first encrypt the mempool with [this](https://ethresear.ch/t/shutterized-beacon-chain/12249) or some similar scheme, as do many other problems associated with PBS.

