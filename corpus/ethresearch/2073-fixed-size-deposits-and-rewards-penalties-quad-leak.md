---
source: ethresearch
topic_id: 2073
title: Fixed-size deposits and rewards/penalties/quad leak
author: vbuterin
date: "2018-05-27"
category: Sharding
tags: []
url: https://ethresear.ch/t/fixed-size-deposits-and-rewards-penalties-quad-leak/2073
views: 2304
likes: 0
posts_count: 7
---

# Fixed-size deposits and rewards/penalties/quad leak

One challenge I’m seeing in the current design is that we want to have fixed-size deposits (32 ETH), for two reasons (i) to make random selection convenient, (ii) to have a minimum deposit size so that slashing always destroys at least some minimum amount of money. But fixed-size deposits don’t really play well with rewards and penalties, which in the current Casper FFG approach simply directly go into deposits.

One possibility is to have rewards and penalties tracked in a separate variable, and then applied only at point of withdrawal. However, this has the issue that it ignores another important function of penalties in Casper FFG: to weed out and reduce the influence of validators that are offline, particularly so that if more than 1/3 of validators go offline at some point, those validators’ deposits start quickly dropping, until they can go online again.

Here is one proposed solution (from [@JustinDrake](/u/justindrake)). Validators have 32 ETH deposits, and have a separate variable that tracks rewards and penalties. If a validator’s penalties minus rewards exceed some critical threshold (eg. 8 ETH), then the validator can be kicked out of the validator set.

Does this achieve the intended objectives? It seems to, but the analysis is somewhat nontrivial:

- If some portion of validators go offline, then their penalties will start accruing, and eventually the online validators will be able to kick them out. That said, it may take longer than before, because we would have to wait until their deposits go all the way down to 24 ETH, instead of possibly exiting earlier.
- If an online majority want to censor a minority, they can do that, just as before. The need to make an active kick-out message is not an impediment to the majority, because they control the chain anyway. So in this regard, nothing is made worse. There’s no gain to a majority from censoring kick-out messages.

Does this scheme have any other issues? Are there any better alternatives?

## Replies

**JustinDrake** (2018-05-27):

I’ll call the variable that tracks penalties minus rewards the “margin”. I think we need a scheme to disincentivise positive margins otherwise the value at stake will be unbalanced across validators.

My suggestion is to levy “interest” (an additional penalty) on positive margins and allow users to “settle” their positive margins by topping up ETH. The interest could grow exponentially to kick out validators faster.

---

**djrtwo** (2018-05-27):

Are the rewards a function of the `32eth + reward_margin` or just fixed to the `32eth`?  In the case of the latter, the validator is effectively earning less and less on their capital while leaving more and more at risk. strange incentives. Especially in the context of the beacon chain being initially totally isolated from the main and shard chains. I see little incentive to join validation when rewards can neither be realized (in the short to medium term) nor compounded upon.

In the case where rewards are based upon the `32 eth + reward_margin` a validator can earn in excess of their responsibilities. A long term validator could easily have far more capital deposited than the 32 eth, but their contribution to security is equal to that of a fresh 32 eth depositor. It seems like in this case they would be being overpaid.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> I think we need a scheme to disincentivise positive margins otherwise the value at stake will be unbalanced across validators.

[some of the below comments might change depending on the answer to the above questions]

Isn’t the ejection mechanism and loss of stake already a disincentive? I don’t see much benefit or advantage that a validator gains by say operating with a 7 eth margin. They bought their 32 eth ticket to play the game. That said, I do like the potential accelerate kicking out validator’s that are accruing penalties, and the top-off is a cool solution.

On the flip, a validator with a huge negative penalty margin (or a positive reward margin) has “more at stake”. Is this too a problem? In the case where validator rewards are a function of `32eth + reward_margin` it does seem to be a problem because we overpay for security from that validator.

---

**JustinDrake** (2018-05-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> Are the rewards a function of the 32eth + reward_margin or just fixed to the 32eth ?

Fixed to the 32 eth.

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> while leaving more and more at risk.

We can design things so that there’s no additional risk to having a negative margin. Specifically,

- Cap the total loss from one continuous leak to 8 ETH (as opposed to waiting that the deposits go to 24 ETH)
- Cap the loss from slashing to 32 ETH (so the negative margin is shielded)

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> nor compounded upon

Rewards compounding is a pretty marginal second-order effect. The main reason for staking is to see rewards accrue (~5% per year) on the fixed-size deposit.

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> I don’t see much benefit or advantage that a validator gains by say operating with a 7 eth margin.

One problem I see is that an attacker can buy out validators for cheap slashing. For example, an attacker can set up a bribing contract offering 1 ETH above the validator’s total account value (e.g. 26 ETH in the case of a validator operating at a 7 ETH margin) to do something bad.

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> On the flip, a validator with a huge negative penalty margin (or a positive reward margin) has “more at stake”. Is this too a problem?

Other than the minimal compound interest a validator doesn’t really have more at stake. And when withdrawals are enabled (not too far in the future) any negative margin can simply be withdrawn and reinvested.

---

**djrtwo** (2018-05-27):

EDIT: In general I’m in favor of this approach.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Fixed to the 32 eth.

Good. Gets rid of the more urgent concerns coming to mind.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Cap the total loss from one continuous leak to 8 ETH (as opposed to waiting that the deposits go to 24 ETH)

Are you suggesting that a validator can be kicked out after an 8 eth leak regardless of end margin? Or that the leak just stops but they can’t be kicked out unless their margin brings them to 24 eth?

Both have some strange censorship attacks that bleed the validator close to 8 eth, let the validator get in some votes, then bleed close to 8 again.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> For example, an attacker can set up a bribing contract offering 1 ETH above the validator’s total account value (e.g. 26 ETH in the case of a validator operating at a 7 ETH margin) to do something bad.

Which is only about ~25% cheaper than a similar attack assuming there are enough high margin validators to bribe. The attack in practice would be between 0 and 25% cheaper depending on the typical margin validators were floating. It shifts the minimum theoretical cost of attack down 25%. The accelerated bleed with the option to top off is nice because it probabilistically keeps the cost of attack closer to the 32eth (times num validators).

---

**tim** (2018-05-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> unbalanced across validators

Why is this a bad thing? I saw that the intention was to make random selection convenient but do not understand the mechanics that makes it so.

---

**djrtwo** (2018-05-28):

If we assume each validator has exactly the same deposit size, we can pick each validator with exactly the same probability. Which is much simpler than having to pick by weight figure out what responsibilities are depending on the weight of the validator.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> One problem I see is that an attacker can buy out validators for cheap slashing. For example, an attacker can set up a bribing contract offering 1 ETH above the validator’s total account value (e.g. 26 ETH in the case of a validator operating at a 7 ETH margin) to do something bad.

One thing [@JustinDrake](/u/justindrake) mentioned is that having validators with a significant margin could make a theoretical  bribe attack cheaper by some amount.

