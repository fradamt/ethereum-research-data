---
source: ethresearch
topic_id: 20059
title: Staking Rights Auctions
author: felipeargento
date: "2024-07-13"
category: Economics
tags: []
url: https://ethresear.ch/t/staking-rights-auctions/20059
views: 2318
likes: 4
posts_count: 2
---

# Staking Rights Auctions

This post was written by [@pedroargento](/u/pedroargento) but his account seems unable to post it, so he asked me to do it. I’m not too aware of the necessities/constraints of the ether issuance debate - but this seems quite interesting for defi protocols as well. Anyway, here it goes:

---

Hey everyone,

A friend of mine just watched the “What’s the Issue with Issuance?” talk by Christine Kim, Caspar Schwarz-Schilling, and Ansgar Dietrichs at EthCC. They said that the key points discussed around Ethereum’s issuance reminded them of a proposal I wrote in the past for Cartesi and CTSI.

The significant issues mentioned were the high (and growing) percentage of ether staked, how having too much ether staked isn’t necessarily beneficial for the network, how LST providers might be in a "winner take all ‘’ situation and etc. Both Ansgar and Justin Drake suggested aiming for around 20-25% staked ether (ball park estimates).

It seems to me that the auction mechanism I proposed for the CTSI staking economy could really help to address these issues, by making the staking system much more expressive. The idea also allows participants to pay negative issuance for the right to earn MEV, which not only tackles the problem of excessive ether staking, but might also helps to balance MEV discrepancies.

I’m not an expert in this research area, but based on the feedback from the EthCC talk, it seems like my proposal aligns well with the direction Ethereum is aiming to take. I’m sharing this here on the Ethereum Research forum in hopes that it can contribute to the ongoing conversation and possibly offer a viable solution to the current challenges with Ethereum’s issuance models.

Looking forward to your thoughts and feedback!

# Staking Rights Auctions

A popular solution to reward users for staking is to mint new tokens and distribute them among stakers. Besides the obvious incentive to gain extra tokens, the inflation created penalizes those who choose not to participate. The challenge is how to measure the opportunity costs of users and how to choose the appropriate issuance amount to achieve a target participation rate, while avoiding exceedingly high inflation rates.

Some projects have a fixed emission rate while others have a dynamic inflation function, which is higher when the participation is below desired and lower otherwise. There are three key problems with these methods:

- You need strong assumptions about users’ risk preferences to tailor the parameters of the function;
- Users have little information about the mining income they will get as it depends on the number of total staked funds.
- The methods don’t allow for differentiation between players with different risk preferences;
- It is hard to determine a balanced inflation target.

As a countermeasure to these three issues, I’m proposing a staking system based on a novel mechanism called staking rights, detailed in the sections below.

## The Mechanism of Staking Rights

Staking rights give node operators the right to participate in staking. Without the rights, operators cannot be selected in the lottery that chooses the node that will generate the next block.

Rights are transitory. At the end of each staking cycle, a set of rights expires and ceases to exist. Conversely, new rights are created and made available for purchase through an auction.

Staking rights always have a final value of 1 token, which is delivered to the account that purchased it at the precise time of their expiry. When users buy a staking right for a price of less than 1 token, the difference between the price paid and the unit value is proportional to their perceived opportunity of the staking right. In that case, the difference is minted and locked in staking together with the price paid, totaling 1 token staked per right sold.

Here is an example. Suppose that the desired staking participation rate is 50% of the circulating supply of 1 thousand tokens. In this case, the system creates and auctions 500 staking rights, each scheduled to pay 1 token at the end of the cycle.

> Circulating supply: 1000
> Target participation: 500 (50%)
> Staking rights issued: 500
> Auction price = 0.97

Assume that each staking right is sold for 0.97 in the auction, thereby generating 0.03 new tokens. The staking rights buyer at the end of the staking cycle would be rewarded 1 token obtaining a 3.09\% return (0.03/0.97). The total inflation generated for the network would be 15 tokens (0.03 per right * 500 rights) or 1.5\%.

With this system, the user knows exactly how much return they will get for their staked tokens, independent of how many rights are sold or how many other stakers exist. There are also no assumptions about risk preferences, buyers will state them through bidding. This method also allows for bigger differentiation between users: instead of asking for a binary decision (stake or not to stake), we allow users to signal at what price they would be willing to stake.

The system can offer staking rights with different staking cycle periods: 2 weeks, 1 month, 3 months, etc. This achieves two objectives (1) differentiate between users who are willing to stake long term from short term players and, mainly, (2) decrease volatility in token emission. After all, if all staking cycles end at the same time, all new staking rights will be subjected to the same market conditions that may not represent the average behavior of stakers.

With different staking periods, in each cycle only a small number of staking rights will need to be created to replace the expired ones. This is because in each cycle there is going to be a mix of active staking rights bought at different points in time.

User risk preferences can be stated in the form of a discount rate, the rate used to convert future values (promises of payouts) to the present. The discount rate is the income that makes one indifferent between gaining money in the present or in the future. For example, with a discount rate of 10% a year, one would be indifferent between receiving 100 dollars today or 110 dollars a year from now.

The discount rate of a user can be translated to a staking right value using it to compute the present value of all incentives that can be paid by staking the right.

Staking rights give the owner three sources of incentives, provided that the owner remained active within the network:

- Staking right’s unit value (paid at the end of the cycle)
- Block producer’s tips
- Mine extractable Value

Below is an example of staking rights holder cash flows for a six month locked period.

[![](https://ethresear.ch/uploads/default/optimized/3X/2/8/28063c3ac2b9e1cd18ed0e7aa69be283c8125261_2_624x385.png)Chart1200×742 21.3 KB](https://ethresear.ch/uploads/default/28063c3ac2b9e1cd18ed0e7aa69be283c8125261)

The price to be paid for the staking can be easily calculate based on the return demanded by the staker

> Given:
> a staking right in a staking cycle of 12 weeks that pays rewards every 2 weeks
> MEV_t the expected mine reward for time t
> NF_t the expected network fees for time t
> UV the staking right unit value
> i the 2-week return expected by the user
> The price P will be calculated as:
>
>
> P= \frac {UV} {(1+i)^6} + \sum_ {t=1}^{6} \frac {MEV_t + NF_t} {(1+i)^t}

The staking rights can be sold through a closed price auction of Nth price, which means that the higher bid wins the token but will pay the price of the highest loser bid. For example, If 500 tokens are sold and the 501st highest bid was 0.98, all 500 tokens will cost 0.98. This type of auction, also known as a Vickrey auction (or Dutch auction), ensures all players bid their true valuation of the staking right, revealing their true risk preferences.

> Proof
> Its not 100% applicable to this specific auction, but a classical proof from Game Theory can give the intuition why the paid price being the lowest winning bid incentivizes truthfully reporting:
>
>
> Given user i has a valuation B_i for a staking right. They can bid B_+ >B_i or B_-
>
> If they bids B_+ there are two possibilities:
>
>
>
>
> B_n
>
>
>
> B_+ > B_n > B_i
>
>
>
>
> In (1) they would get (B_i - B_n) independent of bidding B_+ or B_i and in (2) they would lose (B_i — B_+) that would be larger than (B_n — B_i). In neither case they have incentive to bid B_+.
>
>
> If they bids B_- there are two possibilities:
>
>
>
>
> B_n
>
>
>
> B_-
>
>
>
> In (3) they would get (B_i — B_n) independent of bidding B_- or B_i and in (4) they would not get the token, making it better to bid Bi and have the chance to win.
>
>
> In all possible cases there is no incentive to bid B_+ or B_-, making B_i the dominant Nash-Bayesian equilibrium.

This system also allows for deflation, if the value of the auction ends up above 1 unit. This would make sense if people are expecting such a high reward from the fees and MEV that they are willing to burn a certain amount of tokens in order to participate.

## Inflation Control Mechanisms

Besides the burning possibility, its possible to add parameters in the auction to help manage inflation. Although its unclear to me at this time how those parameters could be decided by the Ethereum ecosystem, I’m presenting them anyway. Contributions are welcomed as always.

**First**. Auction reserve prices: In the worst-case scenario, where all rights are sold in the auction with a price close to zero, the inflation will be the number of rights sold, divided by the total supply (50% in our previous example).

A reserve price means that only bids above a certain value will be considered valid. If we choose a reserve price of 0.7, the worst-case scenario in our example would be an inflation of 15%.

With a reserve price, it is possible to choose an acceptable inflation range and guarantee it will be complied with at all times.

**Second**. The number of issued tokens: The number of tokens directly affects the inflation. If only 100 tokens are issued (out of a total supply of one thousand), the worst-case scenario for inflation would be 10%.

These two variables need to be controlled dynamically in order to make sure the inflation is never higher than a previously determined ceiling. The number of tokens issued will depend not only on the target participation rate but also on the value of bids from the auction. This number will be capped so that the total newly minted tokens are limited to the maximum inflation. The total newly minted tokens can be calculated as the difference between the face value and the highest bid not honored (the Dutch auction price) times the number of tokens issued.

> Let CAP be the maximum number of minted ETH desired
>
>
> Let N_ {max} be the maximum number of staking rights necessary to achieve the target participation rate
>
>
> Let B(i) be the i-th largest bid from the auction results
>
>
> Let N be the number of staking rights issued
>
>
> N will be chosen as the result of the optimization problem:
>
>
> \begin{aligned}
> \max_{} \quad & N\\
> \textrm{s.t.} \quad & N * (1-B(N+1)) \le CAP\\
> \quad & N \le N_ {max} \\
> \end{aligned}

More precisely, suppose that we sort all the bids made during the auction in decreasing order and plot them as in the figure below.

[![m1](https://ethresear.ch/uploads/default/original/3X/f/4/f4dd92342507c13ba5e872d205c15c90bf308b60.png)m1477×318 6.3 KB](https://ethresear.ch/uploads/default/f4dd92342507c13ba5e872d205c15c90bf308b60)

Then N staking rights will be issued in order to preserve the maximum number of ETH issued (CAP). Therefore, we can dynamically choose the minimum value B(N+1) such that the inflation is within the predetermined bounds.

The deflation case is depicted in the figure below:

[![m2](https://ethresear.ch/uploads/default/original/3X/7/3/736de5fac6d3efefd1b613297221521da4f9d64b.png)m2459×318 5.9 KB](https://ethresear.ch/uploads/default/736de5fac6d3efefd1b613297221521da4f9d64b)

It is important to note that there is no way around the tradeoff between participation rate and inflation, to control the later there is the need to sacrifice the former. The advantage brought by the system of staking rights auction is that we maximize participation, while limiting the inflation and allowing workers to express their economic preferences.

## Replies

**felipeargento** (2024-07-15):

Again, don’t have too much knowledge about this (very long) debate.

But, one thing came to mind:

It’s be pretty cool if during an auction like this we’d have a way to favor uncorrelated bidders. If we could ensure that the winners are, for instance, in different geographical locations we could be a bit more confident in the decentralized nature of stakers.

Of course it’s a very hard problem to solve. But maybe timing games? Or past correlated behavior?

