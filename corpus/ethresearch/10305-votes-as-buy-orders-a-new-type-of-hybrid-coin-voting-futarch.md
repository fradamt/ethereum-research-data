---
source: ethresearch
topic_id: 10305
title: "Votes as buy orders: a new type of hybrid coin voting / futarchy"
author: vbuterin
date: "2021-08-11"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/votes-as-buy-orders-a-new-type-of-hybrid-coin-voting-futarchy/10305
views: 7562
likes: 17
posts_count: 22
---

# Votes as buy orders: a new type of hybrid coin voting / futarchy

*Special thanks to Dan Robinson for discussion*

This post proposes a form of coin voting that mitigates tragedy-of-the-commons issues in traditional coin voting that limit its ability to respond to (potentially obfuscated) vote-buying attacks.

# Problem

The core tragedy-of-the-commons problem in coin voting is that each voter only internalizes a small portion of the benefit of their voting decision. This can lead to nasty consequences when it hits against an attacker trying to buy votes: if the voter instead votes in the way that the *attacker* wants them do, they suffer only a small portion of the cost of the attacker’s decision being more likely to succeed, but they get the full personal benefit of the attacker’s bribe.

Suppose there is a decision that the attacker is attempting to push which, if successful, will give the attacker a 20000-point payout but hurt each of 1000 voters by 100 points. Each voter has a 1% chance that their vote will be decisive; hence, in expectation, from each voter’s point of view, a vote for the attacker hurts all voters by 1 point. The attacker offers a 5-point bribe to each voter who votes for their decision. The game chart looks as follows:

| Decision | Benefit to self | Benefit to 999 other voters |
| --- | --- | --- |
| Accept attacker’s bribe | +5 (bribe) - 1 (cost to self of bad decision) = +4 | -999 |
| Reject attacker’s bribe | 0 | 0 |

If the voters are rational, everyone accepts the bribe. The attacker pays out 5000 points as their bribe, gains the 20000 point payout, and causes 100000 points of harm to the voters. The attacker has executed a governance attack on this system.

Bribes do not need to be direct blatant offers; they can be obfuscated. Particularly, an exchange might offer interest rates on deposits of some governance token, where those interest rates are subsidized by the exchange using those tokens to vote in the governance in a way that satisfies its interests. Even more sneakily, an attacker might buy many tokens but at the same time short that token on a defi platform, so they retain zero net exposure to the token and do not suffer if the token suffers as a result of their governance attack. This is an obfuscated bribe, because what is happening behind the scenes is that users who would otherwise hold the token are instead being motivated (by defi lending interest rates) to hold a synthetic asset that carries the same economic interest as the token but without the governance rights. Meanwhile, the attacker has the governance rights without the economic interest.

**In all of these cases, the key reason for the failure is that while voters are collectively accountable for their votes, they are not *individually accountable*. If a vote leads to a bad outcome, there is no way in which someone who voted for that outcome suffers more than someone who voted against. This proposal aims to remedy this issue.**

# Solution: votes as buy orders

Consider a DAO where in order to vote on a proposal with `N` coins, the voter needs to put up a buy order: if the current price at the start of the vote is `P`, then they need to be willing to purchase an additional `N` coins at `0.8 * P` for a period of 1 week if the vote succeeds (denominated in ETH, as DAO tokens tend to have less natural volatility against ETH than they do against fiat). These orders can be claimed by anyone who votes against the decision.

To encourage votes, a reward for making a vote could be added. Alternatively, anyone who votes against could be required to put up a similar buy order if the against side succeeds, and anyone who votes in favor can claim those orders. Another option is that in each round, token holders can vote on any one of N options, including the “do nothing” option, and if a token holder gets the decision they want their buy order activates and if they do not they can claim other holders’ buy orders.

## Analysis

The intended effect of this design is to create a voting style which is a hybrid between voting and futarchy: voting for “normal” decisions that have low effect, and futarchy in extremis. **It solves the tragedy of the commons problem by introducing individual accountability into voting**: if you vote for a bad decision that passes, it’s *your* responsibility to buy out those who disagree if everything goes wrong, and if you did not vote for that bad decision, you do not have this burden.

Note also that the security of this design does not rely on strong efficient-market assumptions. Rather, it relies on a more direct argument: if you personally, as a holder of the system, believe that decision X is an attack on the chain, then you can vote against it, and if the decision passes then the attacker is required to compensate you with locked funds. In the extremes, if an attacker overpowers honest participants in a key decision, the attacker is essentially forced to buy out all honest participants.

## Replies

**Mister-Meeseeks** (2021-08-11):

The hardest part about this is that the buy order is essentially a free call option. It’s true it’s deep out of the money, but even deep out of the money options have some non-zero value. The way I’d go about exploiting this is repeatedly calling votes on proposals that have no chance of passing to mint myself a bunch of free options.

Let’s say every week, I call for a vote to transfer control of the project to North Korea. I repeatedly vote yes with 1% of the tokens, and the other 99% vote no. Now I have access to a huge bunch of options to sell my tokens at 0.8*P. Most times those options will expire worthless, but sometimes the market will go down, and eventually I’ll hit the jackpot. (Or even worse, most of the other participants will get tired of my free riding and vote “do nothing”, and Kim Jong Un eventually takes over the protocol.)

To make it work, I think you’d need some sort of mechanism so that the side being forced to mint options are being fairly compensated for the value of those options. It can certainly be done, but efficiently pricing options is definitely not a trivial problem.

---

**vbuterin** (2021-08-11):

Interesting… this seems like a version of the same problem that you see in all futarchy, which is that if some vote has a too-close-to-zero chance of passing, there’s no incentive to commit capital to voting against it, and so in equilibrium it has to succeed at least some of the time.

Possible mitigations include:

- Adding a “yes bias”: making the requirement that no votes have to provide a buy order weaker, or conditional on there being a sufficient number of yes votes
- Requiring a proposal to have a fee equal to 1% of the funds distributed, so only proposals that have at least some minimum probability of success actually get proposed
- Using a prediction market to filter proposals: anyone can make a bet that the proposal will fail with >95% probability, and bringing the proposal to a vote requires someone making counter-bets against all open bets

---

**kladkogex** (2021-08-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Suppose there is a decision that the attacker is attempting to push which, if successful, will give the attacker a 20000-point payout but hurt each of 1000 voters by 100 points. Each voter has a 1% chance that their vote will be decisive; hence, in expectation, from each voter’s point of view, a vote for the attacker hurts all voters by 1 point.

I am not sure that this line of reasoning is correct.  Probably it is not, since it does not take into account self-referential nature of things, which precludes definitions of the word probability and expectation.

In the extreme case where all voters are PhDs in game theory they will not be tricked by the attacker.  So the result depends on how smart the voters are (or on how well they can be influenced by bad guys and good guys)

You can probably do some social experiments to show this point.

---

**kelvin** (2021-08-13):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> I am not sure that this line of reasoning is correct. Probably it is not, since it does not take into account self-referential nature of things, which precludes definitions of the word probability and expectation.
>
>
> In the extreme case where all voters are PhDs in game theory they will not be tricked by the attacker. So the result depends on how smart the voters are (or on how well they can be influenced by bad guys and good guys)
>
>
> You can probably do some social experiments to show this point.

I’d say it is probably the other way around! If you do the social experiments, I totally expect the group of PhD professors to be the only group falling for the bribes (lol). I think the most counterintuitive idea is that it is rational to accept the bribe even if no one else does. Most people may seek conformity and/or intuitively expect to be punished in this scenario.

By the way I don’t think we run into self-referential problems here. If someone is bribing others to vote, and the bribes *are not* conditional on the attack succeeding, then I’m afraid the only rational equilibrium is everyone accepting the bribe.

Even if in real life people end up not falling for the blatant bribes, they will still be attracted to the obfuscated ones: staking rewards and synthetic exposure. It seems that majority voting is fundamentally broken, and can only survive governance attacks by threatening retaliation with project forks / slashing. So I think Vitalik is spot on trying to attack this problem.

At the same time I don’t think the simple solution of placing buy orders to vote will work. I agree with everything [@Mister-Meeseeks](/u/mister-meeseeks) said. Also, even if you have to put a buy order for `0.8 * P` to vote, you can still vote to steal up to 20% of the DAO’s money and no one can stop you, unless they sell their tokens for a discount, which is far from acceptable in my opinion.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Interesting… this seems like a version of the same problem that you see in all futarchy, which is that if some vote has a too-close-to-zero chance of passing, there’s no incentive to commit capital to voting against it, and so in equilibrium it has to succeed at least some of the time.

If we can solve that particular problem along with a few others, I think we can make futarchy a viable governance protocol for DAOs. I got some ideas about that, I’ll see if I can take some time to work out the details.

---

**MeLlamoPablo** (2021-08-15):

Hi! I’m new to this forum, and I find this discussion very interesting so I wanted to participate.

![](https://ethresear.ch/user_avatar/ethresear.ch/kelvin/48/6173_2.png) kelvin:

> It seems that majority voting is fundamentally broken, and can only survive governance attacks by threatening retaliation with project forks / slashing

I’d like to explore the concept of slashing within DAOs as it could be a powerful tool to build a robust governance system (not just “survive”).

Here’s what I have in mind: first, the governor contract is created with “a constitution” which is simply a string document containing the core values of the DAO. Users should only purchase the token if they agree with it. The constitution may be modified by governance, maybe requiring a higher quorum.

Next, inflation rewards are offered to honest actors who engage in governance. Anyone who delegates their votes, either to themselves or to others (thinking of Compound’s model), is elegible for earning inflation rewards.

The DAO constitutuon should define “human” rules regarding voting. While mathematical rules are expressed in the smart contract, human rules are expressed in the constitution.

It would define strict rules about “dishonest behaviour”, that is, attempting any kind of governance attack through bribes or token lending. It also would set rules about how tokens can be held on behalf of others. For example:

Any entity (including, but not limited to users, smart contract protocols, or centralised exchanges) may hold the DAO token in behalf of third parties with the sole condition that they do not engage in governance by not delegating their tokens. Any entity that delegates tokens held on behalf of third parties may be subject to slashing.

This explicitly forbids the “undercover bribe” by CEXes offering staking rewards. If they want to offer them, they can’t participate in governance or their tokens will be taken away.

The same rationale can be applied to forbid users lending their tokens to short sellers (to prevent Vitalik’s idea of attackers longing and shorting the token simultaneously to access voting power without exposure to the price).

Finally, a new kind of proposal is introduced: the “constitutional proposal” which is a proposal claiming to enforce the constitution. For example, slashing a CEX breaking the rules. This kind of proposal is different in that everyone is forced to participate. Here’s how it works:

1. The proposer opens a constitutional proposal slashing the dishonest CEX. If the proposal passes, the proposer may keep a percentage of the slashed tokens as an incentive for honest behaviour. The rest are burned in an attempt to offset inflation rewards.
2. If the proposal passes:
2.a. “Yes” voters keep getting inflation rewards.
2.b. Abstainers (either implicit or explicit) get their rewards and voting power suspended for 3 months.
2.c. “No” voters get slashed, plus get their rewards and voting power suspended for 6 months.
3. If the proposal doesn’t pass:
3.a. “No” voters keep getting inflation rewards.
3.b. Abstainers (either implicit or explicit) get their rewards and voting power suspended for 3 months.
3.c. “Yes” voters get slashed, plus get their rewards and voting power suspended for 6 months.

This incentives every participant to either vote or delegate to a trusted member of the community who will vote.

Constitutional proposals should be unambiguous and only enforce the constitution. If any ambiguity is included, voters should vote “No” (This should also be stated in the constitution).

I believe this system rewards honest behaviour and penalizes dishonest behaviour. Blatant bribing (such as paying for token delegation) or not-so-blatant-but-still-malicious (CEX staking rewards) is penalized. Undercover/off-chain bribing does not scale well with a sufficiently decentralized token distribution, and slashing rewards incentive honest actors to denounce undercover bribing operations and punish the bribers and the participants who accept bribes.

---

**kelvin** (2021-08-15):

Hi Pablo, welcome to the forum! I agree that “human rules” may sometimes be needed, and that it is better to write them down if possible. So I’d say a constitution defining written rules for hard forks and slashing would be a good idea.

However, I don’t think slashing based on whether you vote for the “winning” proposal is a good idea. It just gives a lot of leverage to the first voters, and people may end up voting for a bad proposal if it seems like that proposal is winning. So if bad actors can just create “momentum” in favor of a bad proposal no one can stop them.

Also prohibiting lending would not work. People can be long in synthetics, futures, and so on, and if the attacker is willing to pay a premium for the real token, at the same time shorting a synthetic, rational people will sell the asset to buy the synthetic and there is no one to be slashed.

---

**jannikluhn** (2021-08-16):

Interesting!

> Suppose there is a decision that the attacker is attempting to push which, if successful, will give the attacker a 20000-point payout but hurt each of 1000 voters by 100 points. Each voter has a 1% chance that their vote will be decisive;

Doesn’t the probability depend a lot on how an individual voter thinks the rest will vote? The closer the vote will be, the more decisive the individual vote is. If they don’t expect it to be close at all they can take the bribe no matter what since it won’t influence the result.

That said, I don’t think it matters for the argument. If one just takes the limit of individual voters having no influence at all, they should always take the bribe.

> Consider a DAO where in order to vote on a proposal with N coins, the voter needs to put up a buy order: if the current price at the start of the vote is P, then they need to be willing to purchase an additional N coins at 0.8 * P for a period of 1 week

I think the main practical problem with this is that it makes voting more costly and complex since voters would presumably have to lock `N * 0.8 * P` for a week and (in the “worst” case) dealing with someone actually taking them up on the call option. Voter apathy is already a big problem for many DAOs and this proposal would increase it, especially for non-institutional voters who don’t want to or can’t “support” their shares with additional funds for voting.

---

**BnWng** (2021-08-16):

Hi [@vbuterin](/u/vbuterin) and company, 1.5 years ago I came up with a very, very similar solution to the vote buying Vitalik is proposing so I have some thoughts on this topic.

IMO, [@Mister-Meeseeks](/u/mister-meeseeks) and kelvin are spot on with their initial points/criticism: the attacker is able to extract value if they are buying at `price < P`.

I.e. If buy order is at 0.8P then the attacker is free to choose a proposal that reduces market price to 0.8P with *zero* cost, right? (Buying the tokens is of zero cost when at the market price.)

Therefore, it would better if the buy order was greater than the current price P. After all, if the proposal is beneficial to the protocol, it should (even in the short term) result in price increases. We could also allow this increase to be very small. Therefore, the attacker has cost of `(buyPrice - P) * N` .

However, we are then left with the problem of the quorum necessary for a proposal to pass. We can derive this by calculating the Cost of Corruption (CoC) for the attacker, against the potential value being stolen or Profit from Corruption (PfC) by using the constraint:

`CoC > PfC`

This allows us to reduce the quorum if `buyPrice >> P` or have a high quorum but low price - `buyPrice ~ P`

I derive this for my project here: [Buidler_Governance/Equations_and_derivations.pdf at 7d81078df5ee5bef4febeccad023b75882d8bbcf · BnWng/Buidler_Governance · GitHub](https://github.com/BnWng/Buidler_Governance/blob/7d81078df5ee5bef4febeccad023b75882d8bbcf/P_min_derivation/Equations_and_derivations.pdf)

This means that the winning voters effectively ‘pay’ the PfC. That might seem like a hard thing to persuade voters but bear in mind that:

1. They choose the buy order price.
2. The market price will (on average) increase if  - or in expectation that - the proposal passes i.e. the value gained from the proposal should be greater than the cost to ‘fund’ it.
3. We can set the ‘current’ price at that of the previous proposal which gives some time for market prices to increase naturally in expectation of the next proposal.

And in fact, voters paying for proposals is exactly what we want - skin-in-the-game.

I hope this doesn’t come across as purely trying to ‘shill my own thing’. I think this kind of design of ‘vote buying at price greater than P’ is the natural evolution of what Vitalik has proposed.

EDIT: I should say that the idea above forces the for-voter to buy the token (rather than selling a put option as in Vitalik’s OP) so that they have a profit incentive if the current price buyPrice for the proposal is low.

---

**MeLlamoPablo** (2021-08-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/kelvin/48/6173_2.png) kelvin:

> Also prohibiting lending would not work. People can be long in synthetics, futures, and so on, and if the attacker is willing to pay a premium for the real token, at the same time shorting a synthetic, rational people will sell the asset to buy the synthetic and there is no one to be slashed.

I’m not sure if I understand correctly, but I see no reason that prohibiting lending can’t work. The “real” asset may also entitle holders to a share of the earnings, and in my proposed example, rewards for participating in governance. So holders do have an incentive for holding the real asset versus holding a synthetic.

Probably what can’t be prevented is an attacker buying the real token and shorting a synthetic (“synthetic” as in Synthetix or UMA, not a wrapper of the real asset) to get “governance rights without the economic interest”. But at the same time the president of a nation could bet against themselves in prediction markets to hedge against bad outcomes. I don’t think that’s something that can be prevented in the majority voting model, but at least “attackers” here are paying the rightful price of governance rights, instead of borrowing the asset or bidding for delegations. I don’t see anything wrong here.

![](https://ethresear.ch/user_avatar/ethresear.ch/kelvin/48/6173_2.png) kelvin:

> I don’t think slashing based on whether you vote for the “winning” proposal is a good idea. It just gives a lot of leverage to the first voters, and people may end up voting for a bad proposal if it seems like that proposal is winning

That’s a good point I hadn’t considered. I’m sure my model can be improved by a lot, but the basic gist is:

- Give governance an on-chain framework for slashing and punishing bad behaviour.
- Reward good behaviour.
- Explicitly forbid behaviour that could lead to a governance attack.

I believe that with those considerations the majority voting model should be fine.

---

**BnWng** (2021-08-16):

Hi Pablo,

Interesting idea. The main problem for me is that there is only a kind of social schelling point or convention that enforces the written constitution. Since the token holders will be aware of this, the attacker can just announce that they will slash all who do not vote for his proposal. So as [@kelvin](/u/kelvin) suggested, you just need some momentum to win the proposal and that momentum could even be a cheap social campaign before the proposal starts (with enough time to scare holders but not enough time to defend.)

IMO, futarchy designs often have this same problem - assume the schelling point will end up on the good side when it isn’t clear that’s the case, so you’re just raising the stakes.

And in addition to the above it would still be possible to bribe the holders cheaply - you simply need to convince them that you’re going win. I.e. attacks can be subtle. E.g. slightly bad proposal could bribe its way through since the cost for each individual holder is low. Bribes are much harder to police than lending.

---

**BnWng** (2021-08-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> I think the main practical problem with this is that it makes voting more costly and complex since voters would presumably have to lock N * 0.8 * P for a week and (in the “worst” case) dealing with someone actually taking them up on the call option. Voter apathy is already a big problem for many DAOs and this proposal would increase it, especially for non-institutional voters who don’t want to or can’t “support” their shares with additional funds for voting.

Re voter apathy: Yes, but you would get higher turnout for proposals since some (or all depending on design) voters would get free insurance through the options. Although that doesn’t mean any more voters would have researched what the proposals mean any more than usual.

---

**itzr** (2021-08-20):

Hi all, this is my first post here too. ![:wave:](https://ethresear.ch/images/emoji/facebook_messenger/wave.png?v=9)

[@BnWng](/u/bnwng), could you please tell me if I have correctly identified the core difference between your concept and [@vbuterin](/u/vbuterin)’s?

For example’s sake, let’s say the token is question is worth $1000.

In Vitalik’s idea, If you want to vote yes, you need to be willing to buy an additional N coins at 0.8*P. So:

- If I vote yes, I must be willing to buy tokens at $800 for 1 week. (mints option)
- If I vote no, I automatically hold the option minted by ‘vote-yes’.
- Thus, if the price goes to $600, ‘vote-no’ users can claim the option and earn $200.

In your model, if you vote no, you must be willing to sell coins at 1.2*P. So:

- If I vote no, I must be willing to sell tokens at $1200. (mints option)
- If I vote yes, I hold the ‘votes-no’ options,
- Thus, if the price goes to $1400, I can claim and earn $200.

Is this correct? If so, there are a few things I like about the idea. I like that it has a positive bias. It’s also similar to giving directors options in order to incentivize price growth. Though, it’s still not clear to me how this would disincentivize bribing…

More broadly, another consideration is time-horizons. Sometimes proposals are good in the long term and bad in the short term (e.g. proposals for oil & gas businesses to publish/implement transitional plans to a ‘sustainable’ future). And coupled with time-horizons is accountability. I read some interesting thinking around this [here](https://astralcodexten.substack.com/p/instead-of-pledging-to-change-the?utm_source=substack&utm_medium=email&utm_content=share&token=eyJ1c2VyX2lkIjozMDA5MTE0MSwicG9zdF9pZCI6MzczMTI1ODgsIl8iOiJJLzBLMyIsImlhdCI6MTYyOTQ1MjY5NiwiZXhwIjoxNjI5NDU2Mjk2LCJpc3MiOiJwdWItODkxMjAiLCJzdWIiOiJwb3N0LXJlYWN0aW9uIn0.xyBP321nowpQ3z4Xi2fX5Jv7W9VLt50hB6VL2203PRg).

---

**tehom** (2021-08-20):

> this seems like a version of the same problem that you see in all futarchy, which is that if some vote has a too-close-to-zero chance of passing, there’s no incentive to commit capital to voting against it,

It has come up before; Wei Dai called it “The Thin End Of The Market” and I’ve raised it as well.

I proposed a solution on the futarchy mailing list (now inactive for some years).  Basically I proposed using a ladder of yes/no markets with varying payout ratios appropriate to a set of increasing probabilities of passing, an auxiliary market that just estimated the probability of passing, and if the estimate reached the top of the ladder, passing it stochastically so it didn’t need to deal with a singularity at 100% probability.

---

**BnWng** (2021-08-21):

Hi [@itzr](/u/itzr), glad you find the ideas interesting.

![](https://ethresear.ch/user_avatar/ethresear.ch/itzr/48/6987_2.png) itzr:

> In your model, if you vote no, you must be willing to sell coins at 1.2*P. So:
>
>
> If I vote no, I must be willing to sell tokens at $1200. (mints option)

No, you **must/will** sell if you vote ‘no’ (rather than “be willing”). The only conditionality is whether the proposal passes or not.

# For clarity

To vote yes:

- You send your dai/eth to the voting contract.
- If the proposal wins, you get gov tokens in return (you bought).
- If the proposal loses, you get your DAI/ETH back (refund).

To vote no:

- You send your tokens to the voting contract.
- If the proposal wins, you get DAI/ETH in return (you sold).
- If the proposal loses, you get your tokens back (refund).

There is no option for anyone to exercise after the voting is concluded, the outcome is determined purely by the proposal winning or losing.

Or if you want to think about it in terms of options: each side is selling options to the governance contract and the contract *always* exercises those options in the case the proposal wins. And in the case that the proposal loses it always refunds all option exchanges.

However, the ‘no’ vote doesn’t affect the outcome of this proposal. In reality the sell side is just providing some liquidity for the buy side and those voters are ‘exiting’ their stake in the protocol by selling.

The main crucial difference between my design and V’s OP are:

1. In my design, the yes voter must buy the token if the proposal wins the vote. Whereas in the OP, they only end up buying the token if both: the proposal wins and another party wishes to sell to them in the week after.
This is crucial since if the yes voter knows they will definitely be buying after the vote is passed, they can profit. This incentivises voting through the pure profit motive.
2. They must buy at any price greater than a pre-set market price set from the previous proposal. Whereas in V’s design they buy at something below the current market price (TBD on how market price is measured there also).

# Example

Firstly, note that you can do governance for funding and governance for upgrades. In funding, you have explicit costs (funds from inflation) to compare against benefits whereas in upgrades, we have the potential cost in terms of protocol damage which therefore decreases token price.

## 1. Some significant amount of time before proposal

- Fair market price P starts at $1000 which is set as a variable in the smart contract.
- Market participants have no knowledge of the proposal below although they might speculate on hypothetical future proposals.

## 2. Proposal announcement:

- Propopser announces some new idea to improve the protocol.
- With this knowledge market participants will re-value the token price higher (on average and all-else being equal).
- So let’s say the new fair market price for the token is now $1200 (but P remains the same at $1000).

## 3. ‘Voting’

- In this governance model the ‘voters’ are actually purely profit motivated. I.e. when you vote ‘for’, you in fact simply consider the buy price to be profitable. Likewise, when you vote against you simply consider the sell price to be profitable.
- Buying and selling are conducted using dutch auctions to allow a market based price to be found.
- This results in a spread between the buy and sell price which is paid for through inflation. Importantly though, this inflation is taken into account when participants buy/sell. I.e. the benefit of the proposal must also pay for the cost of the proposal.
- Buyers and sellers are locked into buying/selling if the proposal wins.

### Buy side:

- The buy-side dutch auction will start off at some high price e.g. £3000 and slowly goes down.
- At some point it will reach some price below the market price at which point it becomes profitable for buyers. Let’s say $1100, so then buyers make a profit of $100 per token.
- The dutch auction only ends when either:

It reaches quorum to pass the proposal.
- It does not reach quorum and times out.

### Threshold for proposal being accepted:

- This is essentially determined by the buy-price and buy-volume (quorum).
- We can calculate the total cost for an attacker to manipulate and buy N amount of tokens. Therefore, we set N based on the point at which the cost for the attacker is equal to the profit they might gain.
- The naïve way to calculate this is: ‘(buyPrice - P) * N’. However, actually P must be measured in some way which means it’s also manipulatable which is why this derivation is used.
- However, assuming P is not manipulated we could say the potential profit - (either through damage or stealing funds) - that the attacker can get is $1000. Therefore, the proposal will win at a volume of 10 tokens.

### Sell-side

- The sell-side dutch auction starts off at some price below the market price and increases.
- At some point it reaches a price above market price at which point it becomes profitable for participants to sell into the auction.
- The total $ amount available in exchange for the tokens depends on the amount being bought on the buy side.
- The purpose of the sell side is primarily to use as a measure for the market price of the next proposal. I.e. we always compare buyPrice(n) with sellPrice(n-1).

> It’s also similar to giving directors options in order to incentivize price growth.

In one sense yes, but actually the relevant price growth has already occured and is necessary for proposal to win.

> it’s still not clear to me how this would disincentivize bribing…

‘Rational’ bribing is not possible in this design if the Profit from Corruption is calculated correctly.

E.g. let’s say the proposal is $1000 of funding so PfC = $1000. If the attacker wants to manipulate the mechanism it would cost them exactly $1000. They would just be paying themselves. So this is an irrational attack.

So bribing is completely removed.

> More broadly, another consideration is time-horizons.

For upgrades, there is a very short time-horizon since the upgrade would happen immediately after the proposal wins.

For funding, the proposals can be split up into smaller proposals with shorter sooner deadlines.

There will be some error but the idea is that, *on average*, over time the mechanism is value creating.

---

**itzr** (2021-08-24):

Interesting…thanks [@BnWng](/u/bnwng)! What you’re suggesting is a very novel idea! I think I understand better now…

We have two auctions, a buy-side auction for vote yes, and a sell-side auction for vote no. This is an opportunity to bid on the perceived value of the token in the event that proposal passes. If you support a proposal, that rationale is that you’ll want gov tokens. If you don’t support, you will want out so you aim to swap to dai/eth.

I have a few more thoughts that I’d like to share with you, though I am by no means a thought-leader in this space, so please take with a pinch of salt ![:slightly_smiling_face:](https://ethresear.ch/images/emoji/facebook_messenger/slightly_smiling_face.png?v=9):

- Delegation / Voting power:

In the broader context of DeGov, having to send eth/dai to vote yes, and send governance tokens to vote no may conflict with vote delegation. Surely it’s better to have a token that handles voting, whether you choose to vote yes or no? At least then you can start delegating to other addresses, or other proxies.

It’s also impossible to tally who has ‘voting power’ in the DAO. Anyone with considerable ETH/DAI can sway a yes vote at any moment in time. Compound offers nice functionality in this regard, also check out [Sybil](https://sybil.org/#/delegates/pool) & [withtally.com](http://withtally.com)

- Practicality question / Adoption:

Imagine you’re a core dev with 15% of total supply.

If I don’t support some proposal which I deem to be bad for the future of the DAO, in the best case scenario, I must vote no, then lose my tokens via the voting mechanism, and repurchase them back on the open market?

If I want to vote yes with my bags, I would need to sell my gov tokens on the open market for eth/dai, then vote. If it loses, I then have buy back the governance tokens in the event that I want to vote no in future. It’s quite a hassle! Not to mention potential liquidity issues…And also, creating an auction based mechanism creates a level of complexity for voting that I’m not sure would be conducive to protocol adoption.

- Is it an option?:

What’s the rational for an “option” that always exercises? It’s not really an option, if there is no option…Surely it’s better to see what the outcome of the proposal is before rewarding/punishing the voters?

…

On another note, it’s interesting to think about what kind of arbitrage opportunities could be created with your auction against the broader market…

Please forgive me if I have failed to understand the entirety of your model and/or have made some false assumptions. It’s a fairly complicated yet fascinating topic!

---

**norswap** (2021-08-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/mister-meeseeks/48/5638_2.png) Mister-Meeseeks:

> The hardest part about this is that the buy order is essentially a free call option. It’s true it’s deep out of the money, but even deep out of the money options have some non-zero value. The way I’d go about exploiting this is repeatedly calling votes on proposals that have no chance of passing to mint myself a bunch of free options.

Tell me if I’m misunderstanding, but I think the idea in the proposal is more similar to **selling a put option**, except you sell them for free! The buy order is pure liability. You can’t exercise anything, but people who voted against you can exercise them if it’s economically beneficial.

If the price drops (e.g. below 0.8 * P) (during the period until expiration, e.g. 1 week) then people can sell tokens to you at 0.8 * P. so you’re buying at a loss, since you could have bought them on the market for less.

---

**BnWng** (2021-08-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/norswap/48/6891_2.png) norswap:

> more similar to selling a put option, except you sell them for free!

Yep, I think you are right. You are selling (for free), the right for someone else to *sell* to you at 0.8P.

In [@Mister-Meeseeks](/u/mister-meeseeks)’s example, the attacker profits when the market price has gone **down**, I.e. the attacker is exercising a put option.

---

**BnWng** (2021-08-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/itzr/48/6987_2.png) itzr:

> We have two auctions, a buy-side auction for vote yes, and a sell-side auction for vote no. This is an opportunity to bid on the perceived value of the token in the event that proposal passes. If you support a proposal, that rationale is that you’ll want gov tokens. If you don’t support, you will want out so you aim to swap to dai/eth.

Yes, that’s a better summary than anything I’ve ever written haha.

![](https://ethresear.ch/user_avatar/ethresear.ch/itzr/48/6987_2.png) itzr:

> Delegation / Voting power:

There is no reason to do delegation anymore since that was partly solving for voter apathy whereas this model solves apathy by offering profit. The equivalent of delegation would be voting specialists who are essentially like short time-scale VC investors who take capital from others to vote on proposals they think are valuable.

E.g. if you’re interested in the protocol and wanted to invest in its development, you can invest ETH/DAI in a ‘delegate’ who will buy and sell the token depending on the proposal.

Important to note: in the long term, the buy and hold strategy will probably not work as well in this model because it’s likely that most value creation will go to new proposers and voters on those proposals (i.e. new innovations).

This is in complete contrast to current value creation model:

- Token holders are free-riders waiting for others to create value.
- Innovation stagnates as ownership decentralises.

![](https://ethresear.ch/user_avatar/ethresear.ch/itzr/48/6987_2.png) itzr:

> It’s also impossible to tally who has ‘voting power’ in the DAO. Anyone with considerable ETH/DAI can sway a yes vote at any moment in time.

Voting power isn’t as relevant in this model since there isn’t as much danger from sybil attacks:

Like previously mentioned, in the case of proposals for funding, the profit from corruption must be paid for through the attack. So any zero-sum attack enriches honest participants.

Similarly, in the case of proposals for upgrades, the attacker would have to pay for the cost of damage done by the upgrade. So although the cashflow value of the token would be damaged, other participants would again profit.

E.g. let’s say the upgrade changed the owner of a contract that held protocol deposits (which could be greater than the value of the governance token). The cost for the attacker would equal the total value of the deposits. So if the attack was carried out, the value of deposits would be transferred to governance token holders while the attacker has zero profit. So then there would be a governance inflation mechanism to redistribute this value back to depositors in such an event.

Also, tallying ‘voting power’ doesn’t actually tell you much because of the possibility of bribery or other secret deals. I.e. it doesn’t tell you the worst case scenario.

![](https://ethresear.ch/user_avatar/ethresear.ch/itzr/48/6987_2.png) itzr:

> Practicality question / Adoption:

Yes, you are right that the voting process is very complex and demanding on the voter compared to staking N amount of tokens in coin-voting.

However, bear in mind, voters are rewarded with profit which is paid for by the value creation of the proposal. I.e. the problem is not ‘how to create the incentive to vote’, the problem is the **cost** of that incentive.

And in reality we should reframe ‘voters’ as ‘traders/funds’ who would simply be arbitraging between the auction and the market price.

Furthermore, a lot of crypto is going to be abstracted away or become the domain of specialists.

So the more likely problem is the inefficiency of markets in pricing new proposals. But I think even that doesn’t matter so much because on average, good proposals will win out over bad ones.

![](https://ethresear.ch/user_avatar/ethresear.ch/itzr/48/6987_2.png) itzr:

> Imagine you’re a core dev with 15% of total supply.

The problem is that the example of the core dev is assuming the old coin-voting model where the core dev must hold some of the supply to profit from their work. In the this design, devs don’t need to do that. Instead, they request funding through a proposal (and get funded!). Dev’s wouldn’t be holding any tokens since that isn’t their domain of expertise - traders and funds would be actively buying/selling tokens based on proposals.

![](https://ethresear.ch/user_avatar/ethresear.ch/itzr/48/6987_2.png) itzr:

> What’s the rational for an “option” that always exercises? It’s not really an option, if there is no option…

I agree, it’s not really an option. I was just trying to describe it in terms of options to further clarify comparisons with the OP.

![](https://ethresear.ch/user_avatar/ethresear.ch/itzr/48/6987_2.png) itzr:

> Surely it’s better to see what the outcome of the proposal is before rewarding/punishing the voters?

By “outcome” you mean in the case that it takes some time to implement the proposal *after* the proposal wins the vote? I’m not totally clear on this question but I will answer anyway.

The idea is that, on average, the market responds correctly to good proposals. So, voters are rewarded for voting for value creating proposals *immediately*. And we need voters to be ‘locked-in’ to buying the token because that creates ‘skin in the game’ and allows us to model the cost of corruption in the case of an attacker.

![](https://ethresear.ch/user_avatar/ethresear.ch/itzr/48/6987_2.png) itzr:

> Please forgive me if I have failed to understand the entirety of your model and/or have made some false assumptions. It’s a fairly complicated yet fascinating topic!

No worries! “complicated yet fascinating” - yes, this is true for a lot of crypto haha. Thank you for the feedback and questions.

---

**Mister-Meeseeks** (2021-08-27):

Absolutely right. My phrasing wasn’t optional should have said “the buy order is essentially *providing* a free call option to the other side”

---

**bowaggoner** (2021-09-26):

I’m thinking that providing a free call option can be a feature, not a bug.

- Proposals are one-sided – change the status quo, or not. So there is a ‘burden of proof’ on supporters of the proposal.
- Presumably the supporters actually want the change to happen, i.e. they derive some benefit from this change happening. This benefit can outweigh the expected utility they lose from providing free options.
- On the other hand, if people aren’t willing to stake much money on the proposal, it can’t be that beneficial (as measured by $$).

It’s similar reasoning to my ethresearch post [Governance mixing auctions and futarchy](https://ethresear.ch/t/governance-mixing-auctions-and-futarchy/10772) . Mixing monetary mechanisms with voting has the advantage of letting people express the strength of their preference by putting their money where their mouth is.


*(1 more replies not shown)*
