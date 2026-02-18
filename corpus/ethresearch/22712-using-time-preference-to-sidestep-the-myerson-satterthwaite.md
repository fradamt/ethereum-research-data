---
source: ethresearch
topic_id: 22712
title: Using Time Preference to sidestep the Myerson–Satterthwaite Theorem?
author: trevelyan
date: "2025-07-08"
category: Economics
tags: [consensus-incentives]
url: https://ethresear.ch/t/using-time-preference-to-sidestep-the-myerson-satterthwaite-theorem/22712
views: 159
likes: 0
posts_count: 3
---

# Using Time Preference to sidestep the Myerson–Satterthwaite Theorem?

This is a cross-post from a Reddit. It is not directly relevant to ETH so mods please feel welcome to remove it, but it is about something fundamental to mechanism design in distributed systems so it is indirectly relevant and important – the question whether “indirect mechanisms” that include time-preference can achieve incentive compatibility in situations where “direct mechanisms” have been proven to be incapable of it.

Specifically, I’ve been wondering lately how or why routing work mechanisms avoid the well-known **Myerson–Satterthwaite impossibility theorem** – the claim that no mechanism can be simultaneously efficient, incentive compatible, individually rational, and budget-balanced. The theorem limits the efficiency of ETH designs and generalizes to most multilateral trade mechanisms and double auctions, but it doesn’t seem to limit routing mechanisms, which are:

- Efficient
- Incentive compatible (though not DSIC)
- Individually rational
- Budget-balanced

This should be impossible. So why isn’t it?

I would be curious if anyone knows or has run into anyone in the space working on this. The closest problem-space I’m aware of is basically auction mechanisms on public goods, where Clarke-Groves, etc.

Anyway, I suspect the answer is that the Myerson–Satterthwaite theorem only applies to mechanisms that can be reduced to direct revelation mechanisms via the Revelation Principle. And while we assume that this reduction is theoretically possible for every incentive compatible indirect mechanism as per Maskin, in this specific case such a reduction doesn’t seem *informationally* possible in mechanisms that create a combinatorial auction over three goods. Specifically in the case of routing mechanisms:

- blockspace (on-chain bytes)
- speed of settlement (time-sensitive utility)
- collusion goods (off-chain benefits, e.g., MEV-protection, API-access)

Almost all of the academic papers studying ETH model blockchain as if there is only the first form of utility in place, which is clearly wrong but also a simplification. Which is where it gets interesting, because the curious thing about having three forms of utility explicitly in play in these mechanisms is that if the user holds any two of these fixed, then their fee is monotonic in the third. But the fee is not monotonic overall. You can see this in action in the following example, which shows how two users might pay different fees at different time-points based on whether or not they are also negotiating for provision of the third good.

USER 1

at 20s — bids 50 for blockspace with 0 collusion goods

at 40s — bids 30 for blockspace with 0 collusion goods

at 60s — bids 60 for blockspace with 1 collusion good

at 80s — bids 20 for blockspace with 1 collusion good

USER 2

at 20s — bids 40 for blockspace with 0 collusion goods

at 40s — bids 35 for blockspace with 0 collusion goods

at 60s — bids 50 for blockspace with 1 collusion good

at 80s — bids 30 for blockspace with 1 collusion good

The discontinuities created by the existence of these three forms of potentially-bundled utility imply **jagged, non-monotonic indifference curves** that violate both the requirements of **single-crossing** and **increasing differences** in implementation theory and particularly Maskin. The existence of non-smooth curves means that truthful preference revelation needs to be high-dimensional as users have to share their rank ordered preferences over all possible combinations. This is obviously impractical (see Hurwicz’s comments on Hayek), but since high-dimensional isn’t strictly-speaking *impossible* the issue can’t just be this problem…

But given this, **I suspect the real issue is that time is infinitely granular.** And because speed-of-settlement is a form of utility that declines continuously rather than discretely, in theory users can have distinct preferences for every infinitesimally small time increment. And since our indifference curves are non-monotonic and cross multiple times — we cannot ignore any subset of the time-curve. So we need full preference revelation, but how can agents disclose preferences at every single point along an infinitely granular curve?

The reason this matters is that it suggests that if we have combinatorial mechanisms in play that include granular time-preferences and 3-way trade-offs, moving from indirect to direct mechanisms seems to **require infinite preference revelation.** And that doesn’t seem to be theoretically possible even if we assume no informational limits on the size of the messaging channel. So it is actually an impossibility condition.

Curious if anyone has any thoughts or feedback. I know people have looked at multidimensional mechanism design, and identified *practical* limits to information-sharing at scale, but I don’t know if anyone has written about *informational* problems like this that seem to make it impossible to shift from indirect to direct mechanisms when one of our goods is infinitely granular. This questino is likely outside the ken of anyone working on blockchain, but would be curious if anyone by chance has tried to model these kind of informational problems theoretically.

## Replies

**BrunoMazorra** (2025-07-08):

Not sure that I got the problem, but seems interesting. Can you clarify what do you understand as routing mechanism? Also, can you write down a simple valuation function of an agent in this set up?

Also, just to clarify **Myerson–Satterthwaite** shows that there is no efficient mechanism with such properties, but there are direct mechanism that are very close to efficient.

---

**trevelyan** (2025-07-09):

Yes, that is the theorem. ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=12)

Myerson-Satterthwaite technically limits direct bilateral trade (one buyer, one seller), but generalizes to mechanisms with multiple buyers and sellers. The claims of universal applicability (“no efficient mechanism”) exist because the proof also generalizes to all *indirect* mechanisms that can be converted to *direct* mechanisms via the Revelation Principle.

The solution involves an indirect mechanism that is incentive compatible with an “efficient production and allocation equilibrium” but is theoretically incapable of conversion to a direct mechanism via the Revelation Principle because doing so would require infinite preference revelation. So the solution does not “debunk” the proof so much as it shows the existence of an efficient mechanism that lives outside its scope.

There is a description of what Hurwicz (1960) called the formula for routing mechanisms on the first page of this paper. Mechanisms use routing signatures to restrict who can put transactions into blocks and produce the next block. Broadcast strategy affects who produces the next block (leader selection) and who gets paid when it is produced. The fact that the node-paid is not necessarily the leader selected is one way the mechanism imposes cost-of-attack on adversarial nodes (reduced probability of payout if you use your own funds to attack the mechanism). Saito Consensus is one possible implementation of this mechanism:



      [github.com](https://github.com/SaitoTech/papers/blob/e32c51db6aae071a41b7e481d0f5ba6cd75ec12d/sybil/A_Simple_Proof_of_Sybil_Proof_Lancashire-Parris_2023.pdf)



    https://github.com/SaitoTech/papers/blob/e32c51db6aae071a41b7e481d0f5ba6cd75ec12d/sybil/A_Simple_Proof_of_Sybil_Proof_Lancashire-Parris_2023.pdf

###










---

ETH research papers traditionally model valuation as transaction inclusion (vt) and assume a fixed supply of utility. In this case supply is not invariant (blocks can be produced faster or slower and producers will rationally include their own transactions in blocks in some situations, which reduces the supply available).

So how you write the valuation equation depends on the problem you’re modelling.

The price paid by user j is the sum of their public and private fees.

p_j = p_{pub}^j + p_{priv}^j

The user valuation \theta_j is the sum of their public and private valuation functions:

\theta_j = U_{pub}^j + U_{priv}^j

We can introduce time by wrapping both functions in time-sensitive functions, but it is challenging as time-preference is specific to the type of collusion good in play. The amount I am willing to pay you not to MEV my transaction will depend on what I am trying to buy on-chain and how quickly I want it. The amount you might be willing to spend to MEV me can also be modelled as a collusion good, but time preference will be different and possibly even non-continuous.

