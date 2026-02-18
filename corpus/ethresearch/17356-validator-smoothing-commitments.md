---
source: ethresearch
topic_id: 17356
title: Validator Smoothing Commitments
author: jvranek
date: "2023-11-08"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/validator-smoothing-commitments/17356
views: 3697
likes: 9
posts_count: 7
---

# Validator Smoothing Commitments

*Many thanks to [Justin](https://twitter.com/drakefjustin) for inspiration and [Drew](https://twitter.com/DrewVdW), [Domothy](https://twitter.com/domothy), [Barnabe](https://twitter.com/barnabemonnot), and [Amir](https://twitter.com/AmirOnchain) for feedback.*

**TLDR:** Requiring node operators to pay upfront to run validators can improve permissionless liquid staking protocols.

**Context:**

Permissionless Liquid Staking Protocols (LSPs) like Rocketpool require node operators (NoOps) to put up capital to run validators whereas permissioned LSPs like Lido do not and instead rely on governance to whitelist professional NoOps. While the former is better for Ethereum’s economic security and decentralization, the latter’s capital efficiency allows it to out-scale others to the point where it is close to surpassing a major consensus threshold and threatens to eventually become Ethereum’s governance.

[EIP-7514](https://eips.ethereum.org/EIPS/eip-7514) helps to slow this problem with minimal changes but an enshrined solution is still being researched e.g., [Dankrad’s article](https://notes.ethereum.org/bW2PeHdwRWmeYjCgCJJdVA) and [Mike’s article.](https://notes.ethereum.org/@mikeneuder/goldilocks)  In the meantime, improving the competitiveness of permissionless LSPs is a another way to slow Lido’s growth. We propose “Smoothing Commitments” as an out-of-protocol solution for the following problems permissionless LSPs face:

- Rug-Pooling as coined by Justin Drake where NoOps steal MEV from stakers.
- NoOps with poor validator performance will produce less LST rewards.
- A tendency towards cartelization via profitability standards.
- Long validator queues and low churn rates stunt the growth of new LSPs.

**Construction:**

Assume node operators lock C ETH collateral which can serve as [tier 1 capital](https://notes.ethereum.org/bW2PeHdwRWmeYjCgCJJdVA) in enshrined designs or be combined with 32 - C ETH with today’s specs.

The NoOps pay the LSP a non-refundable *Smoothing Commitment* (SC) to borrow ETH to run a validator for a minimum duration, e.g., M=1 months. If the NoOp’s SC expires before being renewed, their validator is exited from the beacon chain and C is returned, adjusted for penalties.

In exchange, the NoOp receives 100\% of the consensus and execution rewards earned by their validator. The SC can be priced via an auction, where a NoOp’s bid expresses “I am willing to pay this much to work for M months.”

**Example:** If a NoOp expects a 10\% profit margin and bids 0.90 ETH then they are expecting their validator to earn 1 ETH over the next M months. The NoOp locks C ETH collateral and pays LST holders 0.90 ETH of rewards upfront to borrow 32 ETH to launch a validator. Assuming the NoOp does not extend their commitment duration by rebidding, their validator is ejected after M months and they get back C - P ETH, where P is the penalties they’ve accrued.

**Advantages:**

- Good NoOp incentives: NoOps who paid SCs cannot recoup their initial payment unless they perform as well as the average expected validator, incentivizing for excellent long-term performance.
- MEV-autonomy: NoOps retain 100\% of their MEV, eliminating the need to police rug-pooling or enforce an MEV strategy.
- Decoupled rewards: The LST’s rewards depend on how many SCs are paid rather than validator performance, i.e., LST holders earn whenever a validator joins or renews their SC.
- Resists Cartelization: SCs help address a concern where profitability standards automatically cartelize permissionless LSPs. By allowing MEV-autonomy and decoupling validator performance from LST rewards, nodes can choose non-profit-maximizing MEV strategies without being ejected for underperforming.
- Fast growth: Since SCs can constitute months of rewards upfront, new permissionless LSPs can quickly grow and compete, even during extended validator queues.
- Simple: SCs are straightforward and do not require changes to consensus to implement.
- Compatible: SCs can be incorporated into LSPs that leverage DVT / anti-slashers, incorporated into future enshrined solutions, and is compatible with MEV-burn.
- Restaking: LSPs that engage in restaking can price restaking rewards into their SCs.

**Disadvantages:**

- New: Despite their similarity to T-Bills, SCs are new and require education.
- Less Forgiving: NoOps that need to exit early must forfeit their SC.
- Growth risk: SC dynamics could cause an LSP to grow too quickly.

**Open Questions:**

- Which auction format is most desirable?
- Does this introduce new centralization vectors?
- Can this mechanism also improve permissioned LSPs?

## Replies

**BirdPrince** (2023-11-09):

Thanks very much for the contribution

Lido recently announced its cooperation with Obol. Based on your assumption, does every validator of the Obol network need to pay SC?

Is obol by itself enough to solve this problem?

---

**jaspertheETHghost** (2023-11-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/jvranek/48/11434_2.png) jvranek:

> By allowing MEV-autonomy and decoupling validator performance from LST rewards, nodes can choose non-profit-maximizing MEV strategies without being ejected for underperforming.

Can you elaborate on this? It seems like the proposal constructs a system that favors nodes who are willing to pay the largest SCs to borrow ETH. This favors node operators that can rely on tail-end MEV lottery blocks to make up before a below avg. baseline rate. The proposed frxETH v2 system is similar to this. The LST protocol will tend towards centralization if it accepts the highest bidding operators.

Further, trying to get retail node operators to figure out what an appropriate SC is will be hard. There is a tendency for this to get bid up by opportunistic existing large node operators who want to maximize MEV exposure.

---

**Valdorff** (2023-11-09):

Hoping I’m missing something. If not, this is extremely anti-small-staker.

Essentially, the auction ensures that (a) only high performers should play and (b) the end users need to self-insure against volatility. This is great for large stakers! They can reasonably spend on HA systems to achieve (a) and having many validators will achieve (b) (note – it’s a *lot* of validators if we want to smooth MEV lottery effects).

I’ve written about this before in `https://github.com/Valdorff/rp-thoughts/tree/main/leb_safety` (which I’m not linking cuz apparently new users only get 2 links a post). I would direct you at:

- the first plot in  the value loss section, which shows that a ton of value is in the top few blocks, which means (b) is only achieved by very large stakers
- the conclusion, which talks about what size NOs can benefit from this methodology. Having unpredictable (and indeed potentially negative) rewards would push out small folks.

---

**knoshua** (2023-11-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/jvranek/48/11434_2.png) jvranek:

> Does this introduce new centralization vectors?

Yes, node operators are paying a fixed amount for an uncertain and highly volatile future payment. Large operators can smooth out this volatility by buying many “lottery tickets” and are able to bid close to expected value. If small operators try to compete, the median outcome is that they are losing money.

---

**jvranek** (2023-11-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/jaspertheethghost/48/13897_2.png) jaspertheETHghost:

> Can you elaborate on this? It seems like the proposal constructs a system that favors nodes who are willing to pay the largest SCs to borrow ETH. This favors node operators that can rely on tail-end MEV lottery blocks to make up before a below avg. baseline rate. The proposed frxETH v2 system is similar to this. The LST protocol will tend towards centralization if it accepts the highest bidding operators.

Following Danny Ryan’s reasoning, even in permissionless pools, the NoOps that do not rely on profit-maximizing MEV behavior will underperform relative to the ones that do. Given that there’s finite supply of ETH to allocate to NoOps, the protocol will need to filter according to some performance criteria, which can result in cartel-like behavior.

If you accept this premise, then any LSP will tend towards centralization. While SCs are certainly not a silver bullet, in the end game, they give NoOps an opportunity to choose an alternative MEV strategy without being ejected for underperforming.

> Further, trying to get retail node operators to figure out what an appropriate SC is will be hard. There is a tendency for this to get bid up by opportunistic existing large node operators who want to maximize MEV exposure.

Agreed. Pricing SCs is non-trivial mainly due to the volatility of MEV which is why an auction mechanism is favorable, but this can be daunting for retail NoOps. I suspect secondary markets could emerge to trade SCs. The design space is very large!

---

**vshvsh** (2023-11-11):

This would be extremely centralizing.

1. Reducing the block proposer selection system to a simple, purely monetary market of right to make blocks will make so the winners are the guys best at reducing expenses and extracting value. Best way to reduce expenses in node operation is centralization, the way to squeeze more money is probably vertically integrated MEV.

The node operator market should be multiparametric to actually deliver a secure validator set, and performance should be just one of the factors.

1. Even discarding 1), moving operational complexity and risk to the node operators (in this case, they take the risk of mispredicting MEV) means more sophisticated operators win, which again increases centralization. Operating a node (including in LSTs) should be maximally simple to have a chance of decentralization on beacon chain layer.
2. Have you considered that it’s essentially selling censorship rights for money? And not that much money as well, bc you only need to outbid best non-censoring MEV extractor by the slightest amount.

