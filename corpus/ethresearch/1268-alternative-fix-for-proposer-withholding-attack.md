---
source: ethresearch
topic_id: 1268
title: Alternative fix for proposer withholding attack
author: JustinDrake
date: "2018-03-01"
category: Sharding
tags: [proposal-commitment]
url: https://ethresear.ch/t/alternative-fix-for-proposer-withholding-attack/1268
views: 4078
likes: 0
posts_count: 7
---

# Alternative fix for proposer withholding attack

See [this post](https://ethresear.ch/t/proposal-confirmation-separation-a-bug-and-a-fix/1261) for a description of the attack and proposed fix. We propose an alternative fix below.

**Construction**

During his assigned period p the eligible validator gathers the proposals (i.e. signed collation headers) he has received from all proposers. He also prepares a proposal of his own, e.g. the proposal with an empty collation body. Those proposals are Merklelised to form a root r.

The validator prepares a commitment C by signing [p, r] and broadcasts C to all proposers. The commitment C bonds the validator to using a proposal authenticated against r. That is, when the validator pushes a proposal to the VMC, he also includes a Merkle path from the proposal to r.

If the validator shares a commitment C' for the same period p but with a different root r' then any whistleblower can have the validator slashed (and get a whistleblower’s bounty).

**Discussion**

The commitment and authentication of proposals combined with the slashing condition means that proposers that have received the commitment C can safely reveal the collation body for their proposal with the validator, without the risk of the validator “stealing” the transactions.

The VMC can be setup so that the eligible validator only receives the collation subsidy if the collation body is made available. With such a setup proposers would know that that the eligible validator has a financial preference for proposals for which he has access to the corresponding collation body. Therefore proposers are incentivised to share their collation body with the validator to increase the probability of having their proposal picked by the validator.

In an environment where collation subsidies represent a significant portion of proposer bids, or where withholding attacks are common, an honest and rational validator will likely push proposals to the VMC for which he has received the corresponding collation body, thereby addressing the withholding attack.

## Replies

**vbuterin** (2018-03-02):

Let’s suppose the commitment can only include two proposals, one of which is empty, to analyze the base case. The game now becomes:

1. Proposers all submit proposals
2. The validator chooses one, with txfees T and fee F
3. The proposer maybe publishes the body.
4. If the proposer publishes the body, the validator confirms that one; otherwise the validator confirms the empty one.

It seems to be that because the validator has the fee anyway, the validator has zero incentive to choose one over the other. In fact, validator’s dilemma effects in practice will steer the validator toward confirming the empty collation, as future validators can evaluate it faster. Another problem is that this allows validators to costlessly grief proposers.

I suppose we could have a small reward for choosing the nonempty collation, and dynamically adjust it to target some constant fraction of empty collations, but that is a point of complexity, and griefing proposers would still be cheap (though that’s not fatal by itself, as it just means that future proposers’ fees would decrease to compensate for the risk of griefing).

---

**JustinDrake** (2018-03-02):

Here is one way to design the incentives (sorry for not making this explicit!) so that incentives align:

- The validator can only include a single proposal (collation header signed by a proposer) in the VMC.
- A proposer loses the proposal fee F iff his proposal is included in the VMC by the validator.
- The validator gains F iff the selected proposal “wins”, i.e. gets included in the highest scoring proposal chain.
- The proposer is awarded T, the total transaction fees without collation subsidy, iff his proposal wins.
- The validator is awarded the collation subsidy S iff the selected proposal wins.

The scheme has the following phases:

1. Proposing: Proposers share proposals to the eligible validator without the collation bodies being published.
2. Commitment: The eligible validator commits to all the proposals he has seen, and broadcasts the commitment to all proposers.
3. Reveal: After seeing the commitment, some subset of proposers reveal their collation bodies. Proposers are incentivised to reveal collation bodies for two reasons:

The commitment guarantees the validator cannot steal the fees.
4. The validator has a preference for proposals for which he has seen the corresponding collation body. (See selection algorithm below.)
5. Selection: After the reveal phase the validator decides which proposal to include in the VMC. (See selection algorithm below.)

**Selection algorithm**

An honest and rational validator calculates the expected value for each proposal, and then selects the proposal with the highest expected value. Let’s assume the probability of the proposal winning after inclusion in the VMC is 0.99 if the collation body is properly made available.

For proposals for which the validator has the collation body the expected value for him is 0.99 * (F + S). The reason is that the validator will publish the collation body himself to guarantee availability.

For proposals for which he does *not* have the collation body the expected value is R * 0.99 * (F + S) where R is the probability that the corresponding proposer reveals the collation body.

In an adversarial context where withholding attacks are common with untrusted proposers, the validator will set a low value of R for untrusted proposers, i.e. R \ll 1. In the extreme case the validator will estimate R = 0 for proposals for which he does not have access to the collation body, thereby only selecting proposals for which he has access to the collation body.

---

**vbuterin** (2018-03-02):

> A proposer loses the proposal fee F iff his proposal is included in the VMC by the validator.
> The validator gains F iff the selected proposal “wins”, i.e. gets included in the highest scoring proposal chain.

This has the same issue as the voluntary 50% surrender approach: it creates a fee mechanism which is “inefficient”, in the sense that it has a built-in risk that fees paid through it disappear if the collation does not get included, and so creates an easy incentive for validators and proposers to circumvent the scheme and agree on payments through side channels.

---

**JustinDrake** (2018-03-02):

> incentive for validators and proposers to circumvent the scheme and agree on payments through side channels

Aha, good point! I think the side channel issue can be addressed with a trick ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

- We introduce a “virtual fee” F' (e.g. F' = \min\{10 * S, 1 \textrm{ ETH}\}) to be locked upfront by the proposer.
- The virtual fee F' is returned to the proposer iff the proposal wins.

A similar thing can be done with the subsidy for the validator:

- We introduce a “virtual subsidy” S' locked upfront by the validator upon inclusion of a proposal in the VMC.
- The virtual subsidy S' is returned to the validator iff the proposal wins.

---

**vbuterin** (2018-03-02):

You don’t want money to be returned to the proposer if the proposal *wins*, you want money returned if the proposal *loses*. That way the proposal pays F conditional on chain inclusion, and the validator gets F conditional on chain inclusion, so the gain and loss match out. This *does* give an incentive for validators to try to assign “credit scores” to proposers, so it’s still not perfect, but it does solve the imbalance.

---

**JustinDrake** (2018-03-02):

Having F, T and S all be conditional on the proposal winning makes sense (and is clean). The expected value for the validator is R * 0.99 * (S + F). As you write, it depends on R which acts as a credit score.

If we add the virtual subsidy then the expected value can be even more positively correlated with R:

R * 0.99 * (S + F) - (1 - R * 0.99) * S'

The larger S' is, the closer the validator will want R to be close to 1. There will be a point where any R < 1 will be rejected, i.e. credit scoring is ineffective and validators will only select proposals for which they have the collation body.

