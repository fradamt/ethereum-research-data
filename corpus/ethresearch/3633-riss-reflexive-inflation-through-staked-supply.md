---
source: ethresearch
topic_id: 3633
title: RISS - Reflexive Inflation through Staked Supply
author: johba
date: "2018-09-30"
category: Economics
tags: []
url: https://ethresear.ch/t/riss-reflexive-inflation-through-staked-supply/3633
views: 1769
likes: 7
posts_count: 4
---

# RISS - Reflexive Inflation through Staked Supply

A discussion about PoS chains at [Blockchain Embassy Berlin](https://twitter.com/embassy_berlin) with [Elad Verbin](https://twitter.com/verbine), Vincent Danos, [Florian Glatz](https://twitter.com/heckerhut) and others put some attention on this block reward function. While being super trivial, it gives some nice properties that I would like to discuss here.

## Introduction:

- A token is used to bond validators into PoS.
- The tokens is also used for economic activity.
- The headers of new blocks are recorded in a contract on Ethereum.
- The token is continuously minted to pay block rewards.

When inflating the token supply to pay validators, value is redistributed from all participants to the validators. How can this redistribution be minimized while still paying enough to keep the chain secure?

## Definitions:

r = reward payed for block by minting of tokens.

s = staked supply of tokens.

a = active supply of tokens.

Total supply is active supply + staked supply: t = a + s

n = number of block-rewards payed per year.

i = yearly inflation rate - a value between 0 and 1.

Comparing the sum of minted tokens over a year with total supply gives us the yearly inflation rate:

i = {r n \over t}

Using a simple quadratic function of the form y=ax^2+bx+c we can define the inflation rate as follows:

s < {t \over 2} \quad \quad  i = 0.5  \quad \quad \quad \\
s \geq {t \over 2} \quad \quad i = -2 {s^2 \over t^2} + 2{s \over t}

Combining the two definitions we can define reward as follows:

s < {t \over 2} \quad \quad  r = {t i \over n} \quad  \quad \quad \quad \\
s \geq {t \over 2} \quad \quad r = -2 {s^2 \over t n} + 2{s \over n}

The *RISS* curve looks like this:

[![15%20PM](https://ethresear.ch/uploads/default/optimized/2X/2/21ae8b231203ac0a9a3275e80e313ea24df07822_2_690x426.png)15%20PM1902×1176 128 KB](https://ethresear.ch/uploads/default/21ae8b231203ac0a9a3275e80e313ea24df07822)

## Discussion

Assuming a constant token price, validators are incentivised to stake more tokens when inflation is high. Once the total amount of tokens staked exceeds 50% of supply, the block-rewards start decreasing. Block-rewards continue decreasing until first validators are finding the validation not worth their while and unstake from the chain. Somewhere in the right half of the graph a market equilibrium is found where only the efficient validators can make a profit.

**=> Validators enter into competition and market equilibrium is established.**

Furthermore we can pick a point on the graph, let’s say 80% and discuss the effects of token price on the validator market.

**Token price increases -** Validators are making more profits and more tokens are staked to participate in validation. This continues until some validators loose their profit margins and have to unbond. The equilibrium moves to the right. By using a quadratic function, the curve gets ever steeper, preventing that all tokens move into staking - leaving non for the real economy.

**Token price decreases -** Least effective validators go out of business, and have to unbond, decreasing the  supply staked and thus driving up inflation. The equilibrium moves to the left.

## Conclusion

Paying the right amount for the security of a chain is hard. Both, the effort of validators as well as the current token price are unknowns. Using the % of staked supply as an indicator of token value allows to create a reflexive rate of token issuance.

## Replies

**burrrata** (2018-12-27):

This is cool ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) Do you know if there is any more work in this direction and/or if attacks/bugs have been found in the cryptoeconomics of the model?

---

**johba** (2019-01-02):

haven’t received much feedback. but we are planning to launch this at [leapdao.org](http://leapdao.org) asap ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**burrrata** (2019-01-03):

That’s cool. I really how you guys have bounties clearly posted for everyone to see what’s going on and participate if they want to help out. The community page is dope too with the map and links to get engaged. Reading through the front page though, I’m still not exactly sure what LeapDAO does or is. I understand enough about Ethereum scaling, plasma, and decentralized governance to have an idea of the problems you’re pointing at, but I didn’t get a clear idea of how LeapDAO addresses them and why that’s good for me. Is there a high level blog post somewhere that addresses the “what”, “how”, and [“why”](https://www.youtube.com/watch?v=u4ZoJKF_VuA) questions?

