---
source: ethresearch
topic_id: 5873
title: "Hurdle Funding: A value enhancement over pure buy and burn token models"
author: bgits
date: "2019-07-25"
category: Economics
tags: []
url: https://ethresear.ch/t/hurdle-funding-a-value-enhancement-over-pure-buy-and-burn-token-models/5873
views: 3075
likes: 3
posts_count: 9
---

# Hurdle Funding: A value enhancement over pure buy and burn token models

We propose an alternative to token models where token burning is the default value capture mechanism. We aim to show that networks in their growth phases do not need to choose between capturing value and further developing the network. These two seemingly opposing choices can be brought into alignment.

In the token burning model fees that are received are used to remove the token from supply usually by sending the token to an irretrievable address (burn address). If the fees are received in another token the native token would be acquired first then sent to the burn address. Both variants are methods of returning capital to token holders, leaving the onus of how to deploy that capital to the individual token holder.

Hurdle funding at a high level adds a filter prior to burning. If there are projects that could deliver value back to the network above their cost those projects are funded. In the case there are no such projects then the best path is to return capital and allow the individual token holders to find a better use for it.

[![hurdleVsBurn](https://ethresear.ch/uploads/default/optimized/2X/6/6f1d841cd4d985512c1f4a62fbd31d276e04ba0b_2_666x500.png)hurdleVsBurn800×600 25.9 KB](https://ethresear.ch/uploads/default/6f1d841cd4d985512c1f4a62fbd31d276e04ba0b)

While burning tokens does accrue value to the underlying protocol we believe this being the default action will accrue less value to underlying protocols in their development and growth phases. Below we will show how networks that invest in positive expected value projects will accrue more value than burning by default. Conversely, networks that are approaching the end of their useful lives and have few or no positive expected value projects would be better off burning.

# Example

Let’s start with a protocol that receives $100 equivalent in fees per year for 5 years. The protocol uses the fees to burn it’s token the same year as the received fees. In year five this leads to a net present value accrual of $379 equivalent to the protocol.

[![standardburn](https://ethresear.ch/uploads/default/original/2X/f/f79c9ef8237129a362b4a2410ee24cdac047b765.png)standardburn600×371 13.8 KB](https://ethresear.ch/uploads/default/f79c9ef8237129a362b4a2410ee24cdac047b765)

In the hurdle fund model we first check to see if there are any projects that have discounted value accruals which are greater than the initial investment. We find a project which requires an outlay of $100 equivalent for the first 3 years giving us a discounted cost of $249. The project produces its own value flows of $300 per year for two years starting in year 4. Giving the new project fees of $391 for a net present value of $142 which is the additional value contributed over the burn model.

[![hurdle_model](https://ethresear.ch/uploads/default/original/2X/6/6f65d6f9241811030ffc20abe2fd7b14ed002107.png)hurdle_model600×371 14.6 KB](https://ethresear.ch/uploads/default/6f65d6f9241811030ffc20abe2fd7b14ed002107)

[![hurdleburnnpvs](https://ethresear.ch/uploads/default/original/2X/d/db4d8e95fd7a4690262404f7ae2185c99ae3ec99.png)hurdleburnnpvs600×371 3.89 KB](https://ethresear.ch/uploads/default/db4d8e95fd7a4690262404f7ae2185c99ae3ec99)

# Tying up Loose Ends

Hurdle funding does add the additional risk of funding projects which contribute less value then their initial investment. If our project only returns $175 per year in the last two years we will have a Net Present Value (NPV) of -$20 giving us a final value accrual of $359, which is less than if we had just burned.

Knowing that each project could fail to deliver a positive NPV, we should account for this in project selection. In order to do this we can take a project’s probability of failure and multiply the expected value flow by its complement, the probability of success, which we then subtract from our initial investment to see if the risk adjusted returns are positive.

Let us add in the probability of failure for each project. For simplicity let us assume we have 10 projects to select from and they all have a 90% probability of failure. We also assume they all require the same initial investment and have the same expected value flows. In this example we make 10 investments and only one produces any kind of value flows. If we allocated $30 to each in the first 3 years we would have allocated the full $300 in fees. In order to get back to the same expected value contribution each project is now expected to produce the value flows as the original project but with only an investment of $30, however we are not factoring in a 90% probability of failure so the expected NPV of each project is `($391 * (1 - .90)) - $24.9 = $14.2`. Given that we have 10 projects the expected total accretive NPV is $142 over what a pure token burn model would produce.

# Simulation

We created a simulation in which a project receiving $100 in fees for 10 years invests in positive expected value projects. Running this experiment 500 times we found that the mean hurdle fund NPV was $2,323 while the burn approach was $675. Only 3 observations (~1%) had NPVs below the burn approach with a mean of $447 or ~34% below the burn approach. In other words, **hurdle funding produced higher NPVs 99% of the time**.

[![vfsByYear](https://ethresear.ch/uploads/default/original/2X/1/1d2501b60eaf69fac4a1c72225bed5598c7e874b.jpeg)vfsByYear782×313 119 KB](https://ethresear.ch/uploads/default/1d2501b60eaf69fac4a1c72225bed5598c7e874b)

**Simulation notebook: [Hurdle Funding simulation / Barry G | Observable](https://observablehq.com/@bgits/hurdle-funding-simulation)**

# Further Exploration

While it’s beyond our immediate focus here to propose robust ways of estimating the value flows of projects, we would like to propose areas that look promising. There are studies showing that crowdsourced estimates do provide useful information in markets1. Protocols like Numerai have found that adding staking to crowdsourced estimates further improves the estimates2. Doing project selection and valuation in a decentralized manner is likely a much harder problem but a skin in the game approach such as futarchy might enable sufficiently good project selection to still be an improvement over burning.

---

1 Jame, Russell and Johnston, Rick M. and Markov, Stanimir and Wolfe, Michael, The Value of Crowdsourced Earnings Forecasts (March 23, 2016). Available at SSRN: https://ssrn.com/abstract=2333671 or [http://dx.doi.org/10.2139/ssrn.2333671](https://dx.doi.org/10.2139/ssrn.2333671)

2 “We analyzed the [Sharpe ratio](https://en.wikipedia.org/wiki/Sharpe_ratio) of the unstaked models vs the staked models based on the backtest of the test set. Here is the performance:

Sharpe ratio of unstaked models: 1.66

Sharpe ratio of models staked with NMR: 2.09 “ - https://medium.com/numerai/numeraire-the-cryptocurrency-powering-the-world-hedge-fund-5674b7dd73fe

## Replies

**vbuterin** (2019-07-25):

So this is basically saying that if there’s a project that could deliver more value to the coin than burning the funds then burned funds should be directed to that project instead?

Two questions:

1. Why tie it to burning? If there’s a project where if you give them N coins they provide more than N coins of value, why not just print those coins and give them to the project? Why set a limit equal to the quantity of burned funds? Schelling-fence reasons, something else?
2. What mechanism decides what projects are valuable?

---

**bgits** (2019-07-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Why tie it to burning? If there’s a project where if you give them N coins they provide more than N coins of value, why not just print those coins and give them to the project? Why set a limit equal to the quantity of burned funds? Schelling-fence reasons, something else?

You could do this, especially if there are no funds available from economic activity. If you are just burning and then minting to fund projects, they are netting each other out, you are effectively hurdle funding.

Minting also limits to using only your own token which could have periods of time where market perception makes the cost of capital in said token more expensive over using an external token.

A protocol that can accept multiple tokens of value should have a lower cost of capital as it’s treasury volatility will be a function of the covariances of the return streams and risk factors of multiple tokens.

There is also a lurking argument for higher expected fees from the better UX of allowing users to pay in their token of choice.

---

**bgits** (2019-07-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> What mechanism decides what projects are valuable?

In this context we are only considering value from an economic perspective. So if a project’s discounted future value flows are greater than it’s cost, it’s valuable.

To do this requires estimating with a reasonable degree of accuracy the future value flows. How this can be done reliably in a decentralized way is one of the questions left open. I put my initial thoughts in the “further exploration” section but I don’t have a concrete approach here. Open to ideas ![:slightly_smiling_face:](https://ethresear.ch/images/emoji/facebook_messenger/slightly_smiling_face.png?v=12)

---

**3esmit** (2019-07-29):

Burning tokens might be required for some dapps, where a fee is necessary to provide safety to the smart contract, however is some cases the fee don’t have a rightful beneficiary. Reducing the supply makes all holders happy, and perhaps there is another mechanism increasing the supply.

Originally the idea was “Fee Recycling”, which take “burned tokens” and convert them back to normal currency under a public interest project that the end user selects.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Why tie it to burning?

This was proposed in case a token that don’t have any mechanism increasing the supply, so instead of putting the token in a forever deflationary system, it would prevent (or delay) this by recycling the burned fees.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> What mechanism decides what projects are valuable?

Would be a public governance and individual choice, and the advantage of Fee Recycle is exactly democracy, it allows lower quorum for approving a funding, while keeping the safety of individual user decisions. The quorum needs to be only high enough for people not funding themselves back.

So instead of having a very difficult project to be approved to get immediate funding, it could be approved to receiving funding from end users that have burned tokens. The approved projects would need to keep asking users to recycle their tokens in to fund them, instead of funding other approved projects.

The individual choice could also choose to forever accumulate this burned tokens, and then effectively reducing the circulating supply, or the smart contract could enforce them to be used within some period or any approved project could claim them.

---

**thegostep** (2019-07-29):

Stephane from Numerai. Thanks for sharing this research.

This is closely tied to inflation based grant funding which is what we are using to fund Erasure Grants. We decided to place an upper bound on inflation by minting a specific amount to be held in reserve.

The question quickly becomes how to identify positive NPV projects and, most importantly, how to incentivise them to deliver on their proposal once they receive the funding.

Any thoughts?

---

**corpetty** (2019-07-29):

Re: identifying positive NPV, this is something we’re actively interested in.  I’ll say a bit at the cost of shilling a project.

The Token Economics Research swarm within Status is trying to come up with models to do this.  While our initial efforts [1-3] are starts to building the models, they need hardening with data and peer-review.

We think a correct model depends on the real differences in the mechanism of the project in question (burning, staking, exchange, etc).  Eventually, we hope to have better models/frameworks of evaluating  projects based on their proposed mechanism, and then a better way to quantify whether or not to fund them with a given set of resources.  Our context is within how a given feature affects the whole of SNT, but they could definitely be extrapolated to whole projects themselves.

PS, if I’ve broken some social rules on posting here, please let me know and I’ll change my behavior accordingly.

1.) [Status article 1 - ENS usernames](https://our.status.im/token-economics-ens-usernames/)

2.) [Status article 2 - Sticker Market](https://our.status.im/token-economics-research-sticker-market/)

3.) Status article 3 - Dapp Discovery - link limit on my account (go search Dapp Discovery on our [dot] status [dot] im)

---

**corpetty** (2019-07-29):

I’d argue (without basis) that recycling a scarcity vs changing its supply is easier to reason about, especially if that minting is done based on subjective viewpoints.

If arbitrary minting is done, it is very difficult to see what the future looks like in terms of potential supply, or anything derived from it.  The further “down the stack” this scarcity is the more this is exacerbated.

---

**bgits** (2019-07-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/thegostep/48/7751_2.png) thegostep:

> The question quickly becomes how to identify positive NPV projects and, most importantly, how to incentivise them to deliver on their proposal once they receive the funding.

Hey Stephane,

I think Numerai has done some great real world research and validation (footnote 2) that could be tried with project selection as well.

Here is an idea that I think could make for a real world test.

I think decision making based on `vote + stake` could work, because future value flows can be measured once received.

example: Someone estimates that a project will get 100 DAI in year 1 and 500 DAI in year 2, so when year 1 and year 2 pass it’s possible to measure how accurate they are.

For them they can stake as much as they like so when they stake a lot that indicates a high degree of confidence, because if they are wrong they loose the stake.

Each project can have their own vaults into which funds are received with some percentage allocated to rewarding accurate stakers.

There could also be a percentage of fees received carved out for the project itself in order to incentivize completion.

