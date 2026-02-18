---
source: ethresearch
topic_id: 4157
title: The economic incentives of staking in Serenity
author: econoar
date: "2018-11-07"
category: Economics
tags: [staking-parameters]
url: https://ethresear.ch/t/the-economic-incentives-of-staking-in-serenity/4157
views: 17385
likes: 77
posts_count: 78
---

# The economic incentives of staking in Serenity

For an initial reference, I put together a [twitter thread](https://twitter.com/econoar/status/1053311930885197825) on this subject a few weeks back but I’d like to formalize the discussion here.

I used the latest spec to calculate the sliding scale of staking payouts versus total network at stake and it looks as follows:

[![DnabodbUcAAAmyV](https://ethresear.ch/uploads/default/original/2X/4/4c8bc400776e5349da33dcc4364a03dd58ae710b.jpeg)DnabodbUcAAAmyV492×450 59.4 KB](https://ethresear.ch/uploads/default/4c8bc400776e5349da33dcc4364a03dd58ae710b)

I’d like to open up the discussion around these numbers. There are many complexities involved that I think should be considered:

1. What return is the average user looking for considering 32eth of capital?
2. What returns will “competitors” built on Ethereum be able to offer for returns on ETH investment. This will impact the attractiveness to current ETH holders.
3. What returns will “competitors” not built on Ethereum be able to offer for returns on capital. This will impact the attractiveness to people who may have entered ETH to stake otherwise.
4. What will the cost of running a single validator be, cutting into this return?
5. How many holders will stake no matter what the return, just like running a node at a loss today?
6. How much do we want staked in the network to feel minimally secure?
7. Staking rewards are taxable, how will this cut into incentives?

Here are some of my initial thoughts on the above:

1. Somewhere around 4% return.
2. This will fluctuate wildly on DeFi apps. Relatively risk free interest will be around 0.25%-1% and riskier loans with counter-party risk will be around 5-10%.
3. There are 2% savings accounts today but one must also consider inflation. Over a period of say 15-20 years it’s not all that difficulty to average 4-5% returns post-inflation in the US stock market.
4. Gathered some VERY preliminary data here and seems a single validator will require: 1-5gb storage and 256kbit/s of internet connection.
5. There are 13,000 nodes today but it’s hard to answer this one.
6. If I’m reading the spec right then we need 128 validators for a minimum committee size. So 1024*128=137,072 validators, or ~4.2mn total staked ETH.
7. Would be somewhat similar to other investment vehicles.

What does this mean? Well, I’m not really sure yet and that’s why I wanted to start this discussion. I personally don’t really see a scenario where the network gains many validators under the 3% return rate (~15mn staked). If that is acceptable for the network to run efficiently, the perhaps it’s fine, but if not should we consider increasing these initial numbers with the downside of slightly higher inflation?

## Replies

**jannikluhn** (2018-11-07):

I wouldn’t spend too much effort on tweaking parameters right now and rather say let’s just try it out. When the first phase of Serenity will launch, the value to be secured will be quite low, so as long as we don’t start with something completely off we’re probably vastly overpaying for security anyways. Then we have some hard numbers on what validators will do and we can adjust accordingly in the next fork.

Of course I don’t want to discourage any discussion, the more we know now the better. But I have my doubts that those kind of predictions can be very accurate (I’m not an economist though).

---

**econoar** (2018-11-07):

I’m not too sure I agree with that. As Ethereum ages, it becomes harder and harder to coordinate hard forks, which would be required to tweak parameters. It’s best to attempt to get it right up front and not rely on the need for constant tweaking. IMO, the need for constant tweaking of the block reward has been less than ideal.

Also, what do you mean by “the value to be secured will be quite low”? There is immense value secured by the network today.

Finally, my research above would say we are potentially underpaying, not overpaying.

---

**jannikluhn** (2018-11-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/econoar/48/2248_2.png) econoar:

> As Ethereum ages, it becomes harder and harder to coordinate hard forks

As Eth2.0 is supposed to be rolled out in several phases each of which requires a hard fork anyway, this shouldn’t be too much of an issue I hope (note that the forks mostly do not affect the PoW chain, only the beacon chain and the shards). Look [here](https://github.com/ethereum/wiki/wiki/Sharding-roadmap) for a preliminary roadmap.

![](https://ethresear.ch/user_avatar/ethresear.ch/econoar/48/2248_2.png) econoar:

> Also, what do you mean by “the value to be secured will be quite low”? There is immense value secured by the network today.

That’s true, but that value will stay on the PoW chain in the beginning, it will not move immediately to the shards (because in phase 0 they don’t exist, and because in phase 1 they only store data, there’s no state execution on which most contracts depend on right now).

---

**MihailoBjelic** (2018-11-07):

[@econoar](/u/econoar) thanks for the post. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/econoar/48/2248_2.png) econoar:

> What return is the average user looking for considering 32eth of capital?

IMHO we should agree on a fixed global ETH inflation (e.g. 1%) and distribute it to the current validator set, no matter how big/small the set is. I have high hopes for such a model when it comes to onboarding validators, because it provides really high rewards for the validators in the beginning (we’re rewarding early entrants for the high risk they’re taking, see bellow), and later on (when Eth 2.0 matures) it reaches some equilibrium. One nice thing here is that we don’t need to care where the equilibrium is, as long as we have the critical number of validators (137,072).

![](https://ethresear.ch/user_avatar/ethresear.ch/econoar/48/2248_2.png) econoar:

> There are 13,000 nodes today but it’s hard to answer this one.
> If I’m reading the spec right then we need 128 validators for a minimum committee size. So 1024*128=137,072 validators, or ~4.2mn total staked ETH.

From this it’s obvious that we will need way more validators than we have miners now (quick note: this current number of nodes is not equal to the number of actual miners, but it can certainly serve as a reference).

On the other hand, future validators will face a few disincentives compared to current miners:

a) they risk their stake/capital by applying for this risky new job (PoW is very well known/proven and PoW miners don’t risk losing their capital),

b) the rewards are generally lower than in PoW (AFAIK, payback period in PoW mining is usually around 6 months and after that you usually make some decent profit for at least 6 months after that, then you buy new GPUs and start all over again - my rough estimate is that you can make at least 30-50% per year, but you have to continue investing to stay at that level),

c) they’re making a more serious commitment than in PoW mining (you have to be online 24/7, in PoW you can plug/unplug anytime you want),

d) higher entry-level investment (you can get a small PoW rig for ~$2,500, and PoS validator will have to invest ~$6,000, plus I believe this price is unrealistically low and it will go up in future).

There are more disincentives, but IMHO these would be the main ones (there are also a few advantages, of course).

This being said, I think we should have very high rewards in the beginning to attract as many validators as possible (to reach that threshold), and just let the system reach equilibrium later.

One last note: I’m not a big fan of a super-low/close-to-zero ETH inflation. What’s the point of it, do we really need ETH to moon? I mean, who cares expect the speculators? ![:stuck_out_tongue_closed_eyes:](https://ethresear.ch/images/emoji/facebook_messenger/stuck_out_tongue_closed_eyes.png?v=12)

---

**MihailoBjelic** (2018-11-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> we’re probably vastly overpaying for security anyways

Can you elaborate on this, please? To be specific, how will we be paying validators in Phases 0 and 1, is that already decided? Thanks! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**econoar** (2018-11-07):

Thanks for the response!

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> IMHO we should agree on a fixed global ETH inflation (e.g. 1%) and distribute it to the current validator set, no matter how big/small the set is. I have high hopes for such a model when it comes to onboarding validators, because it provides really high rewards for the validators in the beginning (we’re rewarding early entrants for the high risk they’re taking, see bellow), and later on (when Eth 2.0 matures) it reaches some equilibrium. One nice thing here is that we don’t need to care where the equilibrium is, as long as we have the critical number of validators (137,072).

This is definitely a possibility. A fixed inflation rate takes out the complexity of the sliding scale and could be an easier way to find the proper target.

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> One last not: I’m not a big fan of super-low/close-to-zero ETH inflation. What’s the point of it, do we really need ETH to moon? I mean, who cares expect the speculators?

This I don’t agree with. It’s well beyond just “ETH to the moon”. We’re talking about a platform that hopefully some day secures Trillions in value (already is securing Billions). It’s a necessity that ETH’s value continues to appreciate as it keep the network a lot more secure, incentivizes staking through valuable returns, and makes it more costly to attack the network.

No one is going to trust valuable assets on the network if we’re killing investment value through rampant inflation.

---

**MihailoBjelic** (2018-11-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/econoar/48/2248_2.png) econoar:

> Trillions in value (already is securing Billions). It’s a necessity that ETH’s value continues to appreciate as it keep the network a lot more secure, incentivizes staking through valuable returns, and makes it more costly to attack the network.

This is true, you’re right, I completely lost that perspective. ![:blush:](https://ethresear.ch/images/emoji/facebook_messenger/blush.png?v=12)

---

**jannikluhn** (2018-11-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> Can you elaborate on this, please? To be specific, how will we be paying validators in Phases 0 and 1, is that decided upon? Thanks!

Well, it’s not decided until the community starts running the chain ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12). I’m not sure how final the numbers in the spec are, I wouldn’t be surprised if they end up being changed according to the outcome of this discussion.

But according to [@econoar](/u/econoar)’s calculations above, for the smallest staked amount of 1M ETH we get a yearly interest rate of 12% or in absolute numbers 120k ETH or $25M.

---

**MihailoBjelic** (2018-11-09):

Thanks for the answer. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> for the smallest staked amount of 1M ETH we get a yearly interest rate of 12% or in absolute numbers 120k ETH or $25M

I guess this would definitely be a nice incentive to onboard early, while at the same time global inflation remains almost the same. ![:ok_hand:](https://ethresear.ch/images/emoji/facebook_messenger/ok_hand.png?v=12) This has nothing to do with economics, but I would also be extremely careful with slashing in the beginning (I spoke with a lot of people who are considering becoming validators and they’re all so scared of it ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)).

---

**thatguy1466** (2018-11-15):

How long is the proposed staking period? That’s obviously and important consideration to many. Do you foresee secondary markets for people looking to buy-out early from their staking obligations?

---

**vbuterin** (2018-11-15):

A max withdrawal rate of 8 validator slots per cycle, with a minimum withdrawal waiting time of 24 hours. So in normal circumstances when few others are withdrawing, you can withdraw within a day. In the case of an attack or other situation where everyone tries to leave at the same time, the waiting time can go up to months, but that’s an exceptional case.

---

**econoar** (2018-12-06):

It would appear that with some recent changes to the base reward quotient and switching from cycles to epochs, the rewards have shifted down some. [@vbuterin](/u/vbuterin) I noticed on github most of those changes were from you so figure you may be the best to comment on this.

I’m interested in how the base reward quotient is being determined since that number seems to directly impact the scale of rewards. Is it purely technically driven right now to fit other areas of the spec? I just want to make sure that we get the incentives right.

[![12%20AM](https://ethresear.ch/uploads/default/optimized/2X/8/812012bf767c82d203125ad64228201e558a4f26_2_290x300.png)12%20AM716×730 141 KB](https://ethresear.ch/uploads/default/812012bf767c82d203125ad64228201e558a4f26)

---

**econoar** (2018-12-07):

I’ve started a [GitHub page](https://github.com/ethhub-io/ethhub/blob/3ca7115bffd861ab85e1df644e7172f291e6b250/ethereum-101/monetary-policy/eth-2.0-economics.md) for this topic. It can add to the discussion here or if people want to just contribute directly on the page that’d be great.

---

**jpitts** (2018-12-07):

I am grateful that you have brought this important topic up [@econoar](/u/econoar)!

Even though we are clearly dealing with an nascent and abnormal economy, I believe that staking incentives is partly in the realm of macro-economics. As such, I believe that people with academic research and actual experience in these matters should be brought in to comment (of course after being thoroughly educated in crypto-economics). Experience can even be in game-world economies.

This is a related discussion on the topic of ether supply rate / miner rewards in the current Ethereum mainnet, ahead of a decision made by the All Core Devs:

[Possible outcomes from altering the ether supply growth rate](https://ethresear.ch/t/possible-outcomes-from-altering-the-ether-supply-growth-rate/1647)

---

**jpitts** (2018-12-07):

And to sum up my thinking:

![](https://ethresear.ch/user_avatar/ethresear.ch/jpitts/48/877_2.png)[Possible outcomes from altering the ether supply growth rate](https://ethresear.ch/t/possible-outcomes-from-altering-the-ether-supply-growth-rate/1647/3)

> One additional consequence that may be considered as very significant is the effect of ether supply and expectations about ether supply on capital formation.
>
>
> Through the lens of Mankiw’s 2nd principle , it can be understood that an economy with a less inflationary currency reduces the opportunity cost of holding that currency. The same applies to the rates of bonds. This opportunity cost of capital can help us understand how seemingly abstract factors such as inflation and bond rates relate to investment in business expansion and, by extension, the entire rate of growth of an economy.

Are we allocating enough thinking toward macro-econ basics as we balance staking incentives with security considerations?

---

**jvluso** (2018-12-07):

Is the deflationary pressure of storage fees significant enough to incorporate into the inflation calculations? Unlike gas fees which are kept in the system and passed to the block creator, storage fees are burned forever.

---

**jpitts** (2018-12-08):

I think that [@MihailoBjelic](/u/mihailobjelic) makes a good point about targeting certain metrics.

To maintain such targets would require far more econometric measurement than is happening now in Ethereum. Additionally, an articulation of the desired outcomes would have to be made by key stakeholders. And, above all, there would have to be the will and capacity to periodically make changes in order to reach the desired outcomes.

That validators need to be incentivized is clear. But to decide on the rewards so far in advance seems unrealistic. How can we know now what competing investment options will be available when the time comes to potentially stake?

**Perhaps it is better to focus on the design of “how to decide” on matters like this, and what considerations and stakeholder groups are important to the process.**

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> One last note: I’m not a big fan of a super-low/close-to-zero ETH inflation. What’s the point of it, do we really need ETH to moon? I mean, who cares expect the speculators?

This commonly-cited connection between reduced ether issuance and an improvement in the price of ether to fiat is unproven.

Ether is not exactly allegorical to corporate shares, which would increase in value in the eyes of investors should the firm perform buybacks. Ether is perhaps more similar to the currency of a small economy, featuring limited types of firms. Perhaps its value is more rooted in the growth of the underlying economy and in the subsequent demand for gas.

![](https://ethresear.ch/user_avatar/ethresear.ch/econoar/48/2248_2.png) econoar:

> No one is going to trust valuable assets on the network if we’re killing investment value through rampant inflation.

Rampant inflation may not be a factor in evaluating ethereum as a viable network. It may have actually been driving the miners to participate in ICOs and direct investment in projects. IMO we need to measure and prove what inflation is actually doing to the behavior of individuals and firms.

---

**haokaiwu** (2018-12-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/jpitts/48/877_2.png) jpitts:

> Ether is perhaps more similar to the currency of a small economy, featuring limited types of firms. Perhaps its value is more rooted in the growth of the underlying economy and in the subsequent demand for gas.

It’s not exactly a currency either. It’s a currency asset whereby staking it allows you to own a greater percentage of the total amount of the currency.

I agree though that the effects of inflation aren’t proven. It’s also less of an operating factor for currency that increases and decreases in value by 5% daily.

A few additional points based on [@econoar](/u/econoar) 's opening questions :

1. If we want to compare ETH against asset classes outside of crypto, it’s not necessarily fair to use checking accounts or other nominally safe investments. We should treat it as the market would likely treat it: as a risky asset. This means using a large discount rate that prices in a risk of failure, similar to how people value cash flows in a start-up. We’re talking 30%+. We may have unshakeable convictions on the future of ETH, but it’s unrealistic to expect the market to see it the same way.
2. However, just because we want to use a realistic discount rate 30%+ doesn’t mean we also have to target inflation accordingly. We have to remember that we’re talking about ETH-on-ETH return, not Cash-on-ETH return. If transaction counts and total gas paid has an astronomical growth rate post-sharding, we may not need to pay stakers with much inflation.
3. I agree with keeping the inflation and staker return simple before we get data on sharding. Target a simple and low percentage like 1% or 2% and let the market determine how much ETH-on-ETH return is justified by staking. Without data on the growth rate of transaction fees post-sharding, we’re essentially trying to make policy with one hand proverbially tied behind our backs. As a future staker, I know I’d want to see transaction growth rates before committing to stake long-term. Until that data is available, I’d stake or not stake according to how many people are currently staking.

Granted, point 3 is entirely based on ease of investment decision-making to stake. If there are technical reasons why the current reward schedule is the way it is, that obviously take priority.

---

**MihailoBjelic** (2018-12-13):

I generally agree withe everything [@jpitts](/u/jpitts) wrote.

Few remarks:

![](https://ethresear.ch/user_avatar/ethresear.ch/jpitts/48/877_2.png) jpitts:

> This commonly-cited connection between reduced ether issuance and an improvement in the price of ether to fiat is unproven.

I think this is pretty important to note and understand.

Of course, basic economic logic says that e.g. zero inflation can have only positive impact on the price (certainly not negative and probably not even neutral).

But, I would say that the Ethereum “KPIs” (state of the tech, app usage etc) and the overall state of the crypto ecosystem impact the price at least an order of magnitude more.

![](https://ethresear.ch/user_avatar/ethresear.ch/jpitts/48/877_2.png) jpitts:

> That validators need to be incentivized is clear. But to decide on the rewards so far in advance seems unrealistic. How can we know now what competing investment options will be available when the time comes to potentially stake?

We need to decide on the specific inflation/rewards, sooner or later. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) I think it’s hardly possible to take into consideration all current alternative investment opportunities for validators/stakers, and it’s definitely impossible to account for the future opportunities, which implies that there is no scientific method to determine the optimal inflation. That said, I guess what remains is public discussion and gut feeling (public agreement to try with X% inflation and change it to Y% at a later point of time if needed). As I’ve said, it’s impossible to foresee future investment opportunities for stakers, so we might have to repeatedly adjust the inflation in future anyways, e.g. every few years (no. of validators can not be adjusted bellow a certain threshold if we want a secure system, so adjusting the inflation is the only variable to tune here).

---

**lookfirst** (2018-12-14):

Any thoughts on capping the total number of ether? Doesn’t solve the inflation issue, but does give people a sense of scarcity, like bitcoin. Just seems like it is part of the economic landscape. I know this has been a hot topic in the past, although I haven’t paid too much attention to it, so I’m not pushing it… feel free to dismiss this comment.


*(57 more replies not shown)*
