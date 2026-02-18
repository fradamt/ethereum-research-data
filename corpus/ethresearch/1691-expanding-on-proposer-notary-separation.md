---
source: ethresearch
topic_id: 1691
title: Expanding on proposer/notary separation
author: JustinDrake
date: "2018-04-10"
category: Sharding
tags: []
url: https://ethresear.ch/t/expanding-on-proposer-notary-separation/1691
views: 5348
likes: 5
posts_count: 12
---

# Expanding on proposer/notary separation

**TLDR**: We expand on proposer/notary separation as introduced in [this post](https://ethresear.ch/t/a-general-framework-of-overhead-and-finality-time-in-sharding-and-a-proposal/1638). We suggest a simple proposer selection mechanism and compare the scheme with that of the [retired phase 1 spec](https://ethresear.ch/t/sharding-phase-1-spec-retired/1407).

**Construction**

The SMC in the main shard is endowed with a “proposer registry” per shard which keeps track of proposer deposits. At every period of a given shard, a proposer is pseudo-randomly sampled as the “eligible proposer” with probability proportional to the deposit size relative to the total deposit pool in the proposer registry for the shard.

Shards use main chain blockhashes delayed by 20 minutes (relative to some shards-and-main-chain synchronisation mechanism unspecified here) as the RNG, with a corresponding 20-minute lookahead. Similarly, shards sample from the main chain proposer registry delayed by 20 minutes. Should the main chain reorg by more than 20 minutes, shards must also reorg (both the data layer and the execution layer) and recalculate eligible proposers.

We allow notary deposits to be reused across proposer registries, incentivising notaries to be proposers on at least one shard.

**Discussion**

In the retired phase 1 spec collators had a dual purpose. When calling `addHeader` a collator would simultaneously cast an availability vote for collations in the windback, as well as make a proposal selection. In other words, collators played a role in both the data layer and the execution layer. This conflation of roles led to the proposal commitment mechanism and trapping game to address proposal withholding.

The idea with proposer-notary separation is to provide a cleaner separation between the data and execution layers. Notaries participate exclusively at the data layer without selecting a proposal and associated proposer. Instead the eligible proposer is selected autonomously by the main chain, and given monopoly rights to suggest a proposal for the corresponding period.

Beyond the removal of the proposal commitment game and the cleaner separation of concerns, this scheme comes with a number of advantages:

1. Reduced offchain overhead: The eligible proposer directly broadcasts his proposal (0.5 round trips), as opposed to many proposers simultaneously broadcasting proposal headers and bodies to the eligible collator, with a total of 2 round trips to make a proposal selection. The reduced offchain latency overhead allows for more time to construct proposals.
2. No balance maintenance: In the retired phase 1 proposers had a balance per shard from which would bids where deducted from. This meant that balances had to regularly be “topped up” by proposers, causing onchain overhead and introducing cashflow complexities for proposers.
3. Incentive alignment: In the retired phase 1 collators would get rewarded the bulk of the transaction fees despite proposer-executors doing the work of executing and selecting transactions (see also this post). With proposer/notary separation, notaries rightfully only get paid collation subsidies for their availability efforts, and proposers get paid transaction fees.
4. No forced cashflows: In the retired phase 1 there were forced cashflow cycles from main chain ETH to shard vETH and back. Indeed, bids were paid for in ETH by proposers who then received vETH which then needed to be exchanged back for ETH for balance maintenance. Even orphaned proposals were paid for in ETH with a refund in vETH.
5. Stronger ETH enshrining: In the retired phase 1 spec ETH was the default currency to pay bids, but nothing prevented proposers from privately paying bids in any number of other assets (e.g. ERC20s). With the new scheme the only option for getting selected as eligible proposer is to stake ETH.
6. Decoupled proposer lookahead: In the retired phase 1 spec the collator was effectively the “tier 1” proposer, and the proposers were “tier 2” proposers. The collator lookahead (required for windback) meant that the tier 1 proposer also suffered from lookahead. With the new scheme the tier 1 proposer lookahead is independent from the notary lookahead, and can be completely removed with a RNG-and-anchoring scheme such as this one.
7. No proposer censorship: Because the proposer is autonomously selected by the main chain, there is no opportunity for the main chain to be partial to a subjective proposer selection algorithm. This removes the possibility of proposer censorship by collators.
8. No collator bribing: Again, because the proposer is autonomously selected by the main chain, this is a significant mitigation against proposers bribing collators to not build on the head.
9. Capital reuse and guaranteed proposer pool: Allowing notaries to reuse deposits across proposer registries enables capital reuse and yields a baseline pool of proposers. For example, with 10,000 notaries and 1,000 shards we get an average of at least 10 proposers per shard from notaries alone.
10. Natural merging of proposers and executors: While proposers and executors both execute transactions, it made sense to separate proposers and executors in the retired phase 1 to not require proposers to make a deposit. With the new scheme both proposers and executors need to stake, so merging roles is natural. This allows for capital reuse and allows us to require proposals to also come with a state root claim as a further optimisation.
11. Tier 2 proposal markets: The new scheme does not enshrine infrastructure for the tier 1 proposers to interact with tier 2 proposers, but nothing precludes sub-proposal markets to reuse the proposal commitment game at the application layer. The local gas idea allows for trustless sub-proposal markets to emerge.

## Replies

**terence** (2018-04-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Shards use main chain blockhashes delayed by 20 minutes

Are we still keeping the terminology *periods*? If yes, how many *periods* is roughly 20 minutes?

---

**JustinDrake** (2018-04-10):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/aca169/48.png) terence:

> Are we still keeping the terminology periods?

Yes, the “period length” is the shard equivalent of the main chain “block time”.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/aca169/48.png) terence:

> If yes, how many periods is roughly 20 minutes?

The period length is a parameter which can be specified in absolute terms (e.g. 5 seconds, as in [this scheme](https://ethresear.ch/t/offchain-collation-headers/1679)) or specified as a multiple of block times (e.g. 5 block times, as in [the first version of this scheme](https://ethresear.ch/t/off-chain-intermediate-blocks/1680)). The number of periods in 20 minutes is dictated by the choice of parameter. My preference would be short low-variance periods, e.g. 5-second periods.

---

**terence** (2018-04-10):

Thanks for explaining. I see. A proposer lookahead is independent from the notary lookahead, which can be replaced by RNG scheme.

---

**vbuterin** (2018-04-11):

Thanks for writing this up! In principle I’m totally onboard with proposer/notary separation at this point.

I’d be interested to see any further thoughts on exactly how proposer/executor merging could work, keeping in mind the expected trust model (up to ~90-95% of proposer/executors in any shard are attackers but not more).

Points worth keeping in mind include:

- Are proposals in a chain or not? If not, that makes it harder to connect proposals to state roots directly, so this is an argument for proposals to actually be in a chain.
- If a proposal disagrees with the state root of a proposal N collations ago, what does the proposer do? Publish an alternate list of state roots, as well as witnesses for each state recalculation up until that point? That would probably best fit the spirit of the “fork-free” model.
- How do cross-shard dependencies work? It seems to be that the simplest thing would be to only allow cross-shard data reading where the data being read is behind whatever is the last checkpoint that got committed to the main chain (we need a name for this other than checkpoint… perhaps “merging point?”), so data-layer cross-dependency and execution-layer cross-dependency perfectly match up, and the recalculation algorithm is clear: the only case where you need to recalculate state is the case where the main chain gets reverted to beyond the most recent merging point, and in that case you’re throwing away all of the collations including and past that merging point anyway.
- Also adding onto cross-shard dependencies, what is the “windback length” that we are trusting for state root recalculation?  Having it be the same length as one merging point also seems nice and clear I suppose.

---

**vbuterin** (2018-04-11):

Also, it’s worth keeping one more thing in mind: if we have proposer/executors being shard-specific, then theoretically we could just always require them to provide witnesses for every collation that they create; after all, we *do* trust them to maintain the state. Then we could even require notaries to check the witnesses, so we’re basically going right back to the stateless client model, except that that proposers/executors become the enshrined state storage guarantors.

Not saying that this is optimal; it would certainly be far more efficient for notaries to just do data availability and rely on the interactive game for proposer/executors, but just pointing out that this option, and everything on the spectrum between the interactive game and this option, is on the table now.

---

**mhchia** (2018-04-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> The SMC in the main shard is endowed with a “proposer registry” per shard which keeps track of proposer deposits. At every period of a given shard, a proposer is pseudo-randomly sampled as the “eligible proposer” with probability proportional to the deposit size relative to the total deposit pool in the proposer registry for the shard.

Will it be easier for attackers make themselves the proposer in one shard? One just puts all of its deposit to the proposer registry for the shard. or am I understanding it wrong?

---

**vbuterin** (2018-04-11):

Yes, absolutely. But the point is that the system can still remain secure even if up to ~90-95% of proposers on any specific shard are attackers; the ~5-10% that are not can (i) ensure that any high-value transactions get through, and (ii) call out any fraudulent state root claims.

---

**jamesray1** (2018-04-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> We allow notary deposits to be reused across proposer registries, incentivising notaries to be proposers on at least one shard.

So notaries have an incentive to be proposers. So while there is a better incentive alignment as you outline, what’s preventing a similar scenario to [Exploring the proposer/collator split](https://ethresear.ch/t/exploring-the-proposer-collator-split/1632) happening to notary-proposer-executors becoming the dominant or only player compared to proposer-executors? Additionally if notaries are randomly shuffled per shard it seems that it would still be advantageous for notary-proposer-executors to act in all shards, favouring supercomputers.

Also it would be good to see more detail on the randomness function for proposer selection, however I understand that is another topic in itself.

---

**jamesray1** (2018-04-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Then we could even require notaries to check the witnesses, so we’re basically going right back to the stateless client model, except that that proposers/executors become the enshrined state storage guarantors.

Then notary-proposer-executors would not need to check their own witnesses, giving them an extra competitive advantage. And of course witnesses add overhead. There is a trade-off between more storage and disk reads/writes with witnesses and more latency with interactive verification. Perhaps an optimal approach is to find a middle way between these two kinds of approaches.

---

**vbuterin** (2018-04-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> We allow notary deposits to be reused across proposer registries, incentivising notaries to be proposers on at least one shard.

I would actually recommend NOT doing this. I know that it harms capital efficiency, but it has a number of benefits:

- You don’t have to think about things like “what if a proposer or notary gets slashed in one capacity but then they keep acting in another capacity?”
- Doesn’t introduce an incentive to be both, making it more likely that the two will be separate in practice
- Doesn’t introduce an incentive to be both, making it more likely that pooling and other infrastructure for the two node categories will evolve separately

> Perhaps an optimal approach is to find a middle way between these two kinds of approaches.

Allow not just proposers, but ANYONE, to submit a claim of fraud on any specific collation (with an on-main-chain deposit); the claim would be submitted to the main chain, and clients seeing the claim would know to check that particular collation’s correctness directly, and then reward the submitter in-shard if they are correct.

---

**jamesray1** (2018-04-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Allow not just proposers, but ANYONE, to submit a claim of fraud on any specific collation (with an on-main-chain deposit); the claim would be submitted to the main chain, and clients seeing the claim would know to check that particular collation’s correctness directly, and then reward the submitter in-shard if they are correct.

Yeah and you could have Golem Project using Truebit or similar dapps to verify collations.

