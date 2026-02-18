---
source: ethresearch
topic_id: 10339
title: Practical Futarchy Setup
author: kelvin
date: "2021-08-16"
category: Economics
tags: []
url: https://ethresear.ch/t/practical-futarchy-setup/10339
views: 2522
likes: 2
posts_count: 6
---

# Practical Futarchy Setup

The main problem with majority voting, as summarized by [@vbuterin](/u/vbuterin) [here](https://ethresear.ch/t/votes-as-buy-orders-a-new-type-of-hybrid-coin-voting-futarchy/10305), is that voters are not individually accountable: If a vote leads to a bad outcome, there is no way in which someone who voted for that outcome suffers more than someone who voted against.

Futarchy attempts to solve this problem, but most seem to consider that “pure” futarchy is impractical. We disagree with that assessment, and would like to share with the community a setup that we believe solves some known problems. We plan on implementing it as the governance proceduce for our future Tick Exchange DAO.

The DAO issues TICK tokens, while ETH is the base currency. We can only evaluate a single proposal at a time, in what is called a *decision round*. Each round can have several *decision turns*, which for instance may last for a day. For the duration of a full decision round one can:

- split ETH into ACCEPTED_ETH and DENIED_ETH
- split TICK into ACCEPTED_TICK and DENIED_TICK

At the end of the round a proposal will be either accepted or denied. If a proposal is accepted, ACCEPTED_ETH is converted into ETH and ACCEPTED_TICK being converted TICK. Otherwise, DENIED_ETH is converted into ETH and DENIED_TICK is converted into TICK.

We begin each round by auctioning off some number X of ACCEPTED_TICK for TICK, and the winner gets to decide what the proposal is for that round. Some proportion u of the TICK proceeds are then used alongside uX ACCEPTED_TICK to create a prediction liquidity pool.

This means that the proposal most likely to pass is expected to be decided upon first, and that if the proposal is approved, a total of (1+p)X TICK tokens will be minted.

Once a proposal has been selected for evaluation, the DAO removes some of the liquidity that it holds in a TICK/ETH pool, splits TICK and ETH as described above and adds liquidity to both ACCEPTED_TICK/ACCEPTED_ETH \text{(accepted price)} and DENIED_TICK/DENIED_ETH \text{(denied price)} pools.

At the end of each turn, if \text{(accepted price)} < (1 + \alpha)\text{(denied price)} on average over the turn, then the proposal has a chance p of being rejected. Otherwise a \text{counter} is increased, and if the \text{counter} >= N already, it has a chance q of being accepted. Once a turn ends with a proposal being either denied or accepted, the round ends.

This proposal is similar to one previously proposed here: [Possible Futarchy Setups](https://ethresear.ch/t/possible-futarchy-setups/1820). However, it solves an important problem out by [@vbuterin](/u/vbuterin):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png)[Votes as buy orders: a new type of hybrid coin voting / futarchy](https://ethresear.ch/t/votes-as-buy-orders-a-new-type-of-hybrid-coin-voting-futarchy/10305/3)

> if some vote has a too-close-to-zero chance of passing, there’s no incentive to commit capital to voting against it, and so in equilibrium it has to succeed at least some of the time.

By having probabilistic outcomes for each round, it is possible for an “underdog” proposal to not be denied immediately, giving time for its supporters to sway market opinion. That should prevent prediction markets from estimating approval probabilities that too extreme (very close to either 0 or 100%).

In particular, a proposal has to “pass” several turns to be approved. So when a proposal that was previously considered to be unlikely to pass manages to “pass” one or more rounds, the prediction markets will have time to reevaluate, and token holders that may not be paying attention to it will have time to do so.

**Problem #1 - Hostile Takeovers**

Someone can make a proposal that effecively steals all the assets from the DAO. If the previous market price of the TICK token is P, the attacker can bid P' > P in the \text{accepted price} market. Unless the market price of TICK rises after this attack, everyone has to sell their APPROVED_TICK tokens for P', in what is effectively a hostile takeover, otherwise their tokens will be worthless. If some significant fraction of tokenholders is expected not to sell, the attack can be very profitable even by paying a high price.

But even less ouright malicious proposals are still bad, for instance a hostile merge/acquisition by a larger competitor project that will stiffle competition.

One potential solution to that is making the \alpha in the \text{(accepted price)} < (1 + \alpha)\text{(denied price)} equation be variable and depend on the “open interest” of the contract. If there are simultaneously many people bidding APPROVED_ETH for APPROVED_TICK and TICK holders willing to sell conditional on approval, then the \alpha may increase significantly. This protects inactive tokenholders as controversial proposals become less likely to be approved.

One problem with that is that large TICK holders may effectively simulate a large open interest to bring down proposals, effectively giving them veto power. This could be curbed by adding a “settlement fee” that grows alongside \alpha, making such vetos costly.

**Problem #2 - Denial of service**

Someone can bid highly for a nonsense proposal as a way to prevent other proposals from being considered. To do so they will have to bid some number of TICK tokens every round.

Because a proportion (1-u) of the TICK proceeds are effectively profits for the DAO in case the proposal is denied, we can use some of these tokens to increase the value of X for the next round. As a result, we can make X increase exponentially if all proposals receive high bids but end up being rejected.

[@mkoeppelmann](/u/mkoeppelmann), [@danrobinson](/u/danrobinson), do you see any other problem with this idea? Would love to receive feedback from the community.

## Replies

**bowaggoner** (2021-09-06):

Hi! A few questions/comments, hope it helps!

1.

> We begin each round by auctioning off some number X of ACCEPTED_TICK for TICK, and the winner gets to decide what the proposal is for that round.

I wonder if you could incorporate value/importance of the proposal. I’m worried about not just denial of service with bad proposals, but denial of service from “good” (i.e. highly likely to be passed) but low-value proposals. In fact, it can be very profitable to do this if you win the auction by bidding say 0.7 and then submit some milquetoast proposal that’s sure to pass.

1.

> if \text{(accepted price)} < (1 + \alpha)\text{(denied price)}

This is minor, but this is a bit of a red flag: letting the second-highest bid influence the winner’s chance of succeeding. If I know in advance that Alice is bidding above 0.9, and I don’t like her proposal, I might put in a high bid of 0.8 just to make her life difficult. A first-price approach is probably more robust, unless I misunderstood.

1. Apologies if this is well-trodden ground, but something I’ve wanted to understand in general about blockchain uses of futarchy is how to get around manipulation of the prediction markets? To recap, the idea is that if I have a lot of capital, I can manipulate prediction market prices in order to get a proposal passed. If the proposal benefits me, e.g. deposits all the DAO’s money in my wallet, then I make more than I lose. In fact, I can sometimes manipulate risklessly by only manipulating the conditional “fail” market, which evaporates when the proposal is passed.

Thanks!

---

**kelvin** (2021-09-14):

Hi [@bowaggoner](/u/bowaggoner). In our proposal we have two different mechanisms:

1. Auction to determine what the proposal to be “voted upon” is
2. Market-based decision making in which the proposal is accepted or not whether the price conditional on acceptance is meaningfully higher than the price conditional on rejection.

Approving proposals in step (2) is based on the (\text{accepted price})>(1+\alpha)(\text{denied price}),

formula, so any accepted proposal meaningfully increases the value of the token. Milquetoast proposals will cause (\text{accepted price}) \approx (\text{denied price}) and so are unlikely to pass.

At the same time, the auction in step (1) is a traditional auction in which the highest bidder wins. So there is no way to influence the proposal selection by placing a losing bid.

Your last question is quite important. If you do have a lot of money, you can indeed manipulate the market and force the approval of your proposal, e.g. depositing the DAO’s money in your wallet. However, if all players are rational, holders of the token will just split and sell APPROVED_TICK, and then the manipulator has to buy everyone else’s tokens at above market price.

In practice, not everyone will be rational, and some players may not sell their conditional tokens in this case and will be expropriated by the manipulator.

To prevent that from happening, we increase the \alpha based on how “controversial” the proposal is. One way to “measure” that, for instance, is by how many of the TICK tokens have been split into APPROVED_TICK + DENIED_TICK. One simple logic would be \alpha = 1/(1-p), where p is the proportion of tokens that have been split. This way 50% of “alert” token holders would be enough to prevent a proposal from being approved unless (\text{accepted price})>2(\text{denied price}).

This basically means that, while market manipulation can still happen, the status quo is privileged, and it is much easier to manipulate markets to reject a proposal than to approve one.

---

**bowaggoner** (2021-09-15):

Thanks! I see that I misunderstood what “accepted price” and “denied price” mean. (I thought it was related to a second-price versus first-price auction, but nevermind.) I’ll rethink that and think about your responses!

---

**bowaggoner** (2021-09-17):

> However, if all players are rational, holders of the token will just split and sell APPROVED_TICK, and then the manipulator has to buy everyone else’s tokens at above market price.

Sorry for my naivety: Do you mean that members of the DAO will essentially fork and agree that “Deny” is the canonical version of the chain? If so, that sounds like a reasonable answer!

> Milquetoast proposals will cause (accepted price)≈(denied price) and so are unlikely to pass.

I understand this now. It sounds good, as long as we’re okay with only considering proposals that are strongly relevant to the price of the DAO’s token. (For example I guess donating a bunch of money to charity would be hard to pass even if many are strongly in favor of it.)

This is definitely a tangent, but it reminds me of what I’d call the books-and-bling problem[1]. Maybe your DAO starts out as an environmental advocacy group, but someone proposes pivoting to selling  plastic toys. Nobody in the DAO wants to do that but it would be way more profitable so it passes. Could that be a concern?

[1] Think of whatever the most profitable kind of new shop would be in a given city, say for the sake of argument it’s jewelry at the moment. Then look at any shop in that area, say a bookstore, and ask: if the optimal use of their space and location is to sell bling, then why they don’t just get rid of their books and pivot to selling bling instead? I’m sure there can be complicated economic reasons why not, but it’s a fun thought experiment. Please let me know if anyone knows a proper economic term for this.

---

**kelvin** (2021-09-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/bowaggoner/48/7119_2.png) bowaggoner:

> Sorry for my naivety: Do you mean that members of the DAO will essentially fork and agree that “Deny” is the canonical version of the chain? If so, that sounds like a reasonable answer!

What I mean is that, whenever a “bad” proposal (that decreases the expected value of the token) is being in the process of being approved due to market manipulation, the manipulator has to keep the price of APPROVED_TICK up. Any TICK holders can then split their tokens into APPROVED_TICK + DENIED_TICK and sell the APPROVED_TICK at above market price (for APPROVED_ETH).

The manipulator has to use a lot of APPROVED_ETH to manipulate the (\text{accepted price}) up, and most likely can only do so by splitting his own ETH into APPROVED_ETH + DENIED_ETH. If the proposal ends up being accepted, this is equivalent to the manipulator buying TICK holders at above market prices.

![](https://ethresear.ch/user_avatar/ethresear.ch/bowaggoner/48/7119_2.png) bowaggoner:

> I understand this now. It sounds good, as long as we’re okay with only considering proposals that are strongly relevant to the price of the DAO’s token. (For example I guess donating a bunch of money to charity would be hard to pass even if many are strongly in favor of it.)

Yes, the DAO is only expected to approve measures that increase the price of the token. So this is only intended as an organizational structure for profit seeking institutions. Other types of institutions (governments, charities, etc) would have to define a different type of value function in order to use futarchy as a decision procedure (e.g. stakeholders voting on values).

I do expect decisions to act more like the decision of a company board than like the decision of a CEO. As you mentioned, small decisions that affect the price only slightly are unlikely to pass. The way a futarchy DAO can still help such decisions happen is by voting on structural reforms, delegating power, etc. Instead of voting on each small decision, the market votes on how to allocate power most efficiently.

