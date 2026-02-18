---
source: ethresearch
topic_id: 14957
title: Latency arms race concerns in blockspace markets
author: dcrapis
date: "2023-03-03"
category: Economics
tags: [mev]
url: https://ethresear.ch/t/latency-arms-race-concerns-in-blockspace-markets/14957
views: 4790
likes: 23
posts_count: 12
---

# Latency arms race concerns in blockspace markets

*Thanks to Akaki Mamageishvili and participants at the “Make MEV, not (latency) wars” event for helpful feedback. A related presentation of the main idea and more “pictorial” view is available [here](https://docs.google.com/presentation/d/1Yz9R6mWVWzLHp1m3yXOnZoRYN90wwCJ-hpsIWqjlUew/edit?usp=sharing).*

There is a justified attention on designing the market for blockspace in a way that it does not replicate traditional financial markets distortions. In particular, the now well-known latency arms race in which hundred millions of dollars have already been spent on network infrastructure to gain smaller and smaller advantages.

Will the **blockspace market** suffer from a similar trap? One where lots of wealth accrues to infrastructure & operations that have low/zero real utility, and that concentrates the market around a few big players that have capital & technology to compete in the arms race?

The answer is, it depends. On the market design and in particular on transaction ordering mechanisms. We provide two example designs, one time-based like traditional finance and the other bid-based like Ethereum L1. We show that the resulting **incentives to invest in latency advantage are very different**: constant in the former case and decreasing/finite in the latter. Then we present some **open questions** and we discuss the **design space and fundamental trade-offs of hybrid designs**.

## FCFS designs for transaction ordering (vanilla FCFS)

The risk of falling into the trap is **high**.

This design makes block ordering similar to ordering in tradfi exchanges where there is *continuous-time trading* and FCFS ordering of transactions.

Consider a generic 12s interval and suppose that there are 12 mev opportunities in the interval that arrive at random times. The searcher that has the fastest network will win every single opportunity. The slightest latency advantage gives the searcher uniform monopoly power over the entire interval.

## Auction designs for transaction ordering

The risk of falling into the trap is **low**.

In this design the transactions are ordered by the willingness-to-pay of the searcher, submitted in the form of a bid. Suppose there is a fast searcher with a latency of *f* milliseconds vs a slow searcher with a latency of *g > f*. It takes the fast searcher *f* ms to detect a new mev transaction and *f* ms to relay it to the block proposer. This means that the fast searcher will be able to extract up to *2f* ms before the end of the slot and the slow searcher up to *2g* ms. Call the advantage *x* ms.

Consider a 12s batch/slot interval. In this design the fast searcher has monopoly power over roughly x/12000. As an example, if x is 10ms this gives monopoly power to unilaterally extract only 0.08% of the time.

The same advantage gives the fast searcher unilateral extraction power 100% of the time in the other design, so the incentive to invest in fast network infra is reduced by a factor of >1000 in the 10ms advantage example.

**Assuming a convex cost to acquire more advantage we can easily see that, since the gain grows linearly, it quickly becomes uneconomical to invest more. After initial inefficiency is competed away the incentive to invest more in latency improvements stops.**

[![Screen Shot 2023-03-03 at 8.42.22 AM](https://ethresear.ch/uploads/default/optimized/2X/b/b124b593aa1ea7497b2d68162e9c17d7382bceea_2_690x157.png)Screen Shot 2023-03-03 at 8.42.22 AM1878×430 65.6 KB](https://ethresear.ch/uploads/default/b124b593aa1ea7497b2d68162e9c17d7382bceea)

This is in contrast with the FCFS design in which any small advantage grants uniform dominance. **Under the same reasonable cost structure we can easily see that the incentives to gain a latency advantage never goes away.**

[![Screen Shot 2023-03-03 at 8.43.03 AM](https://ethresear.ch/uploads/default/optimized/2X/a/a99fd6c90a113a7b2e821e6424394e4e4d16e920_2_690x151.png)Screen Shot 2023-03-03 at 8.43.03 AM1878×412 61.5 KB](https://ethresear.ch/uploads/default/a99fd6c90a113a7b2e821e6424394e4e4d16e920)

### What about incentives to invest in latency for other participants?

- proposers: NA, they are already monopolists
- relays: since connecting is free we can assume that builders will connect to the faster relay, however since relays don’t have revenue the economic incentive to invest in network infra seems low. For a malicious party that wants to subsidize this to monopolize the market the same argument as in the main section applies
- builders: low, again same incentives as the main argument, linear returns and convex costs, it quickly becomes more profitable to invest in other dimension of advantage (eg, aquiring private orders, devise more complex search strategies that extract closer to theoretical mev)

### What about geographical distribution of mev opportunity origin-set (user wallets, CEXs) and destination-set (validators)?

There are arguments on whether geographical distribution of users and validators is a centralizing or decentralizing force for other participants in the supply chain. We only note that users and validators are themselves participants in the location game. A searcher can invest to operate vertically integrated validators or subsidize them to relocate, same for user wallet providers (CEXs are harder to move).

The higher the level of geographical distribution of the network the higher the cost to aquire an average advantage of *x* milliseconds for a searcher. One can argue that now the searcher can first invest in centralizing the network (e.g., moving wallet providers and/or validators) and then invest in latency advantage at a lower unit cost. But other searchers can follow at a much lower cost by adjusting their location to the new geographical distribution.

This game is more complex than the previous one, so we need to be careful with our simplifications and the full analysis should consider key factors like (1) geographical distribution of MEV sources that are hard to move (i.e., CEXs) and their relative weight (2) intrinsic incentive to relocate closer to sources for other participants (3) opportunity cost of investing in latency and (4) the dynamics of repeated moves. **Intuitively, it again seems that since gains from latency advantage are linear, for any reasonable convex cost strucutre, the incentive to invest in latency are significantly smaller in this design vs designs with continuous-time trading.** However, a more thorough analysis of the relocation game is needed to say whether the resulting equilibrium network configuration is sufficiently decentralized.

**Open questions**

How does a geographically distributed demand/supply network change incentives?

How centralized is the equilibrium location of service providers (wallets/…/validators)? What is a reasonable measure of decentralization in this case?

In practice, in blockchain-based discrete-time auction designs, at what latency level (ms/…/ns) becomes uneconomical to invest more?

## Hybrid designs

We have seen how two extremely different designs for transaction ordering lead to very different incentives for participants. The designs we have analyzed actually differ on two important dimensions:

- processing policy: continous-time (streaming) vs discrete-time (batch)
- ordering policy: time-ordering vs bid-ordering

The FCFS is on one corner of spectrum, continous-time processing and time-ordering, and the auction design is in the opposite corner.

Choosing a **discrete-time batch processing** policy opens up a wide ordering policy design space, **virtually any combination of time-ordering and bid-ordering can be implemented**. But the system has higher latency of settlement, equal to the length of the batch interval.

In the other case of **continuous-time streaming**, time-ordering is most natural and has no additional latency. Mechanisms that also allow to bid for inclusion can be introduced at the cost of some latency (such as the [time-boost proposal that arbitrum is working on](https://research.arbitrum.io/t/time-boost-a-new-transaction-ordering-policy-proposal/8173)). However, **the design space is more constrained**.

In both cases above, a design with more latency in settlement introduces delay to user transactions and state updates which is *welfare decreasing*, but allows for more sophisticated bid-ordering mechanisms that can improve security, robustness, and mitigate the losses from MEV extraction which are *welfare increasing*. These are fundamental trade-offs to keep in mind while exploring this wide design space.

## Replies

**pmcgoohan** (2023-03-04):

Interesting and well put together research- thank you.

What do you make of the proposed Arbitrum solution of a priority fee within global network latency? It seems strong to me in that it makes latency investment finite for FCFS (similar to your auction charts) and in a very simple way compared to a complex auction model.

I’d also say that looking only at the negative externalities of latency wars without considering the (IMO) more significant negative externalities of frontrunning / toxic MEV which are harmful to users and price discovery is too narrow (frontrunning / toxic MEV are hugely reduced by FCFS ordering vs 12sec block MEV Auctions).

EDIT: “incentives to gain a latency advantage never goes away” isn’t quite true. Spend on latency advantages is capped at total profit, it isn’t infinite. You won’t spend $20m on colocation if you’re only making $19m. This is why the Arbitrum idea is strong, because it effectively lowers this existing cap to sensible levels.

---

**dcrapis** (2023-03-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> What do you make of the proposed Arbitrum solution of a priority fee within global network latency? It seems strong to me in that it makes latency investment finite for FCFS (similar to your auction charts) and in a very simple way compared to a complex auction model.

I think it is a nice experiment in the hybrid design space. Definitely helps partially with latency race and also helps partially with the recent “spam attacks” they have experienced: MEV searchers making thousands of websocket connections to increase the likelihood to be included first by their sequencer.

But note that the auction limits bid-competition to a narrow 500ms window in which time-competition is still important. So, yeah, it’s in between the two cases but the table may still be tilted to much in favor of lower latencies.

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> I’d also say that looking only at the negative externalities of latency wars without considering the (IMO) more significant negative externalities of frontrunning / toxic MEV which are harmful to users and price discovery is too narrow (frontrunning / toxic MEV are hugely reduced by FCFS ordering vs 12sec block MEV Auctions).

yes, this is only a partial analysis focused on latency incentives. a full analysis of welfare effects of the two system should include both looking at different types of opportunities of MEV extraction (perhaps using empirical data on their frequency & distribution) and also including geographical distribution.

---

**dcrapis** (2023-03-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> EDIT: “incentives to gain a latency advantage never goes away” isn’t quite true. Spend on latency advantages is capped at total profit, it isn’t infinite. You won’t spend $20m on colocation if you’re only making $19m. This is why the Arbitrum idea is strong, because it effectively lowers this existing cap to sensible levels.

right, but you can spend up to $18,999m. and it is enough to be slightly closer than your competitor to grab the entire $19m.

---

**quintuskilbourn** (2023-03-07):

One dynamic that isn’t really reflected here is that the latency advantage gives an advantage over all information-sensitive opportunities over the last 12s window.

Consider opportunities which consist of arbitrage against a CEX (or any other domain really). The latency advantage the fastest player has means that they are able to bid for the last 12s of opportunities with the most updated prices in mind, subjecting themselves to less risk than their competitors, which allows them to bid higher.

From another angle:

- If the price moves to make the opportunity more valuable, the fastest player is more likely to outbid competing players.
- If the price moves to make the opportunity less valuable, the fastest player shades their bid down. If a bidder from earlier in the slot wins the opportunity, they are more likely to have overpaid. Hence other bidders now face more adverse selection which they need to price in.

I haven’t thought the probabilities through enough to know what the value of the latency advantage is, but it’s not obviously linear and certainly only adds to the advantage you already described.

---

**dcrapis** (2023-03-08):

Here is a simple (the simplest?) setup that considers both cases you highlight.

Consider a simple model in which *orders* o_i arrive with a constant rate of \lambda and *signals* s_i arrive with a constant rate of \eta. There is a batch-auction design, similar to Ethereum L1, with a *slot length* of l. Searchers compete strategically for transaction inclusion and MEV-gains, WLOG we look at the simple case of two searchers and define the *latency advantage* of the fast-searcher A vs slow-searcher B as x. Each order represents a MEV opportunity and searchers can submit one or more transactions t_i=(t_{i1}, ..., t_{ik}) with associated inclusion bids b_i=(b_{i1}, ..., b_{ik}) to take advantage of it. For now, we consider the simplest case in which MEV is extracted with only one blockchain transaction (k=1).

**Gains**

Searchers compete for orders that come in the initial interval of length l-x, while in the last x milliseconds only A can respond to orders and signals. Note that in this design searchers can also change their bids for previously submitted transactions, so in the last x milliseconds A is the only one that can **send new transactions to take advantage of new orders** (write monopoly) and **change past bids to take advantage of new signals** (rewrite monopoly). Note that this also entails canceling transaction by setting a bid of 0 for example.

Searcher A gain-advantage depends critically on batch-length and latency advantage

g_A(x,l) - g_B(x,l) = \underbrace{x\lambda v}_\text{write gain} + \underbrace{x\eta(l-x)\lambda |v-b_B|}_\text{rewrite gain}

Note that we have assumed for simplicity that: (i) the opportunities are copies of the same order, (ii) all the signals received give a proportional informational advantage over order being rewritten. So it is really the best case for A, but as you can see it is still at most linear in x (the rewrite term is actually sublinear).

Some directions that would be interesting to explore: quantify informational advantage and valuation update rule instead of using true value & do a more realistic model with different types of MEV-opportunities and different information structure of signals.

---

**ankitchiplunkar** (2023-03-21):

Can you share the derivation for the last formula?

---

**ankitchiplunkar** (2023-03-21):

I want to bring another point into the latency debate.

We cannot treat L1/L2’s in a vacuum and need to consider competing trading venues in the model. Let’s only consider trading as a use-case (71% of [validator payments](https://frontier.tech/the-orderflow-auction-design-space#8307da28ed2340c9ade6c914fc5aa7e7) come from trades)

- Latency means slower price discovery
- i.e. Other venues will determine the price and have higher volume (due to how MMers work)
- LPs in the slower venue will leak value to toxic traders (maybe innovations like McAMM might reduce the leak)
- LPs prefer to go to higher volume venues because they have more fees and lesser value leak reducing the liquidity in slower venue.

L1/L2 designers will prefer to have more trading volume since it increases the value of their network. More transaction fees and more MEV to be captured and distributed.

---

**quintuskilbourn** (2023-05-07):

> Some directions that would be interesting to explore: quantify informational advantage and valuation update rule instead of using true value & do a more realistic model with different types of MEV-opportunities and different information structure of signals.

You might be hinting at it here^, but I don’t think your model takes into account the fact that the disadvantaged bidder has to shade down their bids compared to A as they take on more risk (and face adverse selection due to A’s acting with additional information).

Small advantages can have a large effect. I think the Klemperer paper could be quite relevant: https://www.nuff.ox.ac.uk/economics/papers/1998/w3/wallwebb.pdf

---

**raddy** (2023-05-22):

You’ll spend to where the risk adjusted predicted IRR is at the hurdle the respective player needs. From the protocol and user’s perspective though, this is deadweight loss. Economic value transfer to network providers, fancy low latency systems etc.

Can end up potentially in situations where builders could overpay for latency advantage to where its internally anti competitive – have seen this for periods in tradfi where big players are willing to operate a losing business for years to discourage long term competition.

---

**gutterberg** (2023-05-27):

The advantage may be linear, but isn’t the problem rather that the fast player in some sense strictly dominates the slow player because of these points?

---

**mariuszoican** (2023-08-04):

We were thinking of these ideas in the context of traditional markets a few years back, when there was talk of switching exchanges to frequent batch auctions: https://doi.org/10.1016/j.finmar.2020.100583. One issue is that the more you want to speed up the blockchain beyond the 12-second slot (say, for scalability), the more likely you are to trigger latency wars.

