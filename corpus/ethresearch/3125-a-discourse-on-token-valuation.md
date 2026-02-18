---
source: ethresearch
topic_id: 3125
title: A Discourse on Token Valuation
author: savant.specter
date: "2018-08-29"
category: Economics
tags: []
url: https://ethresear.ch/t/a-discourse-on-token-valuation/3125
views: 4603
likes: 5
posts_count: 15
---

# A Discourse on Token Valuation

Hopefully, I won’t get chewed out for talking about theoretical valuation methodology.

These concepts seem to be poorly understood and consequently code design decisions (for plasma/Dapps and around UX) are being made without consideration of the monetary policy consequences.

I would like to think this will help raise the quality of discourse surrounding valuation and token withholding. Happy to discuss more with anyone who is interested.

[A Discourse on Token Valuation](https://savantspecter.github.io/research/A_DISCOURSE_ON_TOKEN_VALUATION.pdf)

## Replies

**mkoeppelmann** (2018-08-29):

you can find my thoughts on this [here](https://twitter.com/koeppelmann/status/1033983197678379009) and [here](https://twitter.com/koeppelmann/status/1034770427627876352).

In summary:

In Ethereum today ETH is a payment token. And while ETH is scarce there would be likely no long term reason to hold ETH because Ethereum tx (which are valuable) are IMHO NOT priced in ETH. Other then using default software a miner has no good reason to price transactions in ETH or even accept ETH. The miner could just accept any token they like e.g. via a payment channel or accept Paypal. The miner has no costs in ETH to produce the block - so why would they accept ETH.

HOWEVER - this would change completely with POS. Now owning/staking ETH WOULD be a requirement to create blocks. I still think that payments to miner can happen in ANY currency but you can now use the DCF model and say that all transaction revenue will go to miner/staker. POS only is secure if ETH is valuable thus the network should reward staking and thus the tx costs for a user needs to be higher than the computation costs for the average staker.

This difference between costs could be seen as rent. The idea that forking is free is absurd as soon as you would have to coordinate thousands of independent actors. This is why I define independent actors doing connected transactions on Ethereum as the measure of success. ([increases forking costs](https://twitter.com/koeppelmann/status/1021865794429435904?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E1021865794429435904&ref_url=https%3A%2F%2Fblog.gnosis.pm%2Fmedia%2F6d943da28718da37a5aaed6810f04baf%3FpostId%3D9cb486b170ff))

So if any I would be concerned that Ethereum has TOO MUCH potential to turn into something rent extracting and I am more wondering about mechanisms that ensure that transaction fees will stay reasonably low.

---

**UHU1234** (2018-08-29):

You claim to have demonstrated a “supply and demand model”, so what is the equilibrium price of ETH?

Every asset in the world is priced based on supply and demand in a market place, ETH is no different. The challenge is that nobody knows what the supply is, what the demand is, how they affect each other and how either of them is going to change in the future.

On top of that, the ETH token isn’t even needed to pay for gas (as Martin has already pointed out). I can pay miners with Paypal if I want, which further reduces the need to hold ETH.

---

**savant.specter** (2018-08-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png) mkoeppelmann:

> Ethereum tx (which are valuable) are IMHO NOT priced in ETH.

I think we agree here. Hopefully, this terminology makes the idea clearer: “While # of transactions is a valid but imperfect metric of platform success, it is not a factor in deriving token valuation because transaction capacity is (theoretically, at scale) unlimited.”

![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png) mkoeppelmann:

> Other then using default software a miner has no good reason to price transactions in ETH or even accept ETH. The miner could just accept any token they like e.g. via a payment channel or accept Paypal. The miner has no costs in ETH to produce the block - so why would they accept ETH.

This is an interesting idea but, as mentioned above, I already agree that transactions (between token users and/or miners) don’t directly attribute value back to the token.

![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png) mkoeppelmann:

> I still think that payments to miner can happen in ANY currency but you can now use the DCF model and say that all transaction revenue will go to miner/staker.

PoS will cause Ether to become an interest bearing asset more similar to currency. While one could theoretically use this to perform a DCF, I suspect the output wouldn’t make much sense- as it wouldn’t for a DCF using interest rates on USD.

![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png) mkoeppelmann:

> So if any I would be concerned that Ethereum has TOO MUCH potential to turn into something rent extracting and I am more wondering about mechanisms that ensure that transaction fees will stay reasonably low.

Sorry I don’t quite follow the logic to get here. Regardless of the exact costs, the rent extraction associated with imperfectly matching fees must still be bounded by the coordination costs of a fork, right?

---

**savant.specter** (2018-08-30):

A key point here is that any protocol which requires Ethereum lockups affects the demand (bullishly). Casper staking, Plasma bounties (mainly from operators but also from individual actions of sufficient aggregate size), and Augur prediction market lockups are all examples [Read: layer 1, layer 2, and applications]. However as higher prices do not imply/cause platform success, it’s an open question as to whether or not high prices are good for forwarding Ethereum’s goals.

---

**Lars** (2018-08-30):

This is a topic that certainly needs more research.

The use of Discounted Cash Flow leads to the Market Cap being an important number. As DCF isn’t a good model, the Market Cap is almost meaningless, although it is frequently used today when comparing cryptocurrencies. Actually, because of continuous new issuance resulting in inflation, the situation is almost the opposite of dividends. Coin holders will effectively have to pay a kind of tax.

A key point of the valuation by Pfeffer is the Velocity, seemingly arbitrarily set to 7. This velocity depends a lot of whether you are a Coin Holder, or a user.

> At system maturity, there will be a fixed (scarce) number of tokens; it is written into the core code and
> agreed upon by the participants.

Even though it is written into the protocol, it is ultimately a thing up to social consensus. That is, an economic majority may decide to change it.

Defining the supply as the number of tokens in circulation is not the same thing as the total theoretical supply. A number of coins are lost forever. Also, when talking about the supply-demand relation, it usually refers to the current supply and demand at an exchange.

> At a specific point in time, the supply of ether is constant.

This is a crucial observation. It is a common misunderstanding that some cryptocurrencies are “unlimited”. Yes, they are unlimited with increasing time, but not at a specific point of time. Because of this misunderstanding, some people believe that the value should be zero.

> Besides the promise of future execution, there are a few additional reasons to withhold Ether.

This is also a crucial observation. If you only take this into account, the value of ether doesn’t have to be high at all. But ether also has another important role, and that is to pay for the security of the network.

> Because supply is fixed, price rises and falls with demand alone.

And this explains why there is a high volatility.

Personally, I think the Velocity Of Money is an important tool when analyzing cryptocurrencies.

There is also the interesting effect of the Network effect (or the lack of it), as you mentioned. This is important when analyzing fork effects. Notice that the network effect usually isn’t quadratic, but more like n*log(n). Notice also that the network effect fails if blocks are “full”.

I have collected my various thoughts and ideas at [Medium](https://medium.com/@lars.pensjo/price-of-a-cryptocurrency-and-the-market-cap-fc09897440b9)

---

**savant.specter** (2018-08-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/lars/48/14_2.png) Lars:

> Defining the supply as the number of tokens in circulation is not the same thing as the total theoretical supply. A number of coins are lost forever. Also, when talking about the supply-demand relation, it usually refers to the current supply and demand at an exchange.

Definitely agree that burn should be factored into the supply curve. It is a small additional factor that didn’t seem relevant when discussing just the basics of the model. Also, it’s a good point that daily price discovery happens on only a subset of total units. Longer term this should have a smaller impact.

> Velocity Of Money is an important tool when analyzing cryptocurrencies.

In theory, “MV = PQ” is a macro model as well and an evaluation informed by this framework provides some interesting insights. Unfortunately in practice, as the community has demonstrated time and again, it is deceptively difficult to apply the model in an intuitive way. The crypto space already has specifically defined concepts of “market cap,” “units,” “quantity,” and “price” which do not necessary line up with the required economic definitions of the model- leading to some distorted conclusions. From a *very* high level, “token”(?) lockups reduce “velocity”(?) and thus increase “market cap”(?) (- consistent with the analysis from the S&D model). But attempting to utilize this model at a more detailed level quickly reveals these terms are not well-defined/universally consistent.

---

**Lars** (2018-08-31):

There is much discussion of the Network Effect. Cryptocurrencies depend on the network effect. This behaves differently when we look at the use for transactions and the use as store of value. E.g. if the number of passive bitcoin holders is doubled, all other things equal, the price of bitcoin would need to double. Compare this with transactions. If the number of vendors doubles, it will become almost twice as useful for those that use bitcoin to pay for goods (supposing the block size limit isn’t reached). And the other way around, a web shop will equally benefit if the number of customers paying with bitcoin double.

So the value of Bitcoin from the point of view of transactions grows with O(n²), while the value from the point of view of coin holders grow with O(n).

What then happens when we apply this conclusion to Bitcoin? The use of Bitcoin has gradually changed from being Electronic Cash to Store of Value. That means it is gradually reducing its dependency on network effect from O(n²) to O(n). Improving scaling should increase the O(n²) factor more. A Network effect of O(n) isn’t really a network effect.

Also, if the blocks are “full”, it means that added users no longer provide a Network Effect.

---

**Lars** (2018-08-31):

Ethereum also have a lot of tokens, implemented by contracts. Should the market cap of these be included in the valuation of ether? The total value of the Ethereum blockchain should include all values on the blockchain, so it would seem reasonable. But then, it can be argued it already is included, but indirectly. If the number of high value tokens grow, the price of ether will probably grow indirectly as an effect.

But there is a counter example. Suppose a bank issues an internal token on the public Ethereum blockchain, but tells no one about it. The bank assigns the nominal value of $1 billion per token, and then use this token (or fractions of it) for transfers between sub businesses. The “market cap” of this token could easily be a trillion of dollars, much bigger than a market cap for Ethereum. But the total effect on Ethereum would be negligible.

Does the value of ether reflect the value of the Ethereum blockchain? Does the value of the Ethereum blockchain correspond to the market cap of ether?

---

**savant.specter** (2018-09-04):

The article from Jeremy Rubin on TechCrunch is getting a lot of media play. Considering it is closely associated with the topics discussed above, I thought a short response in the context of this conversation is relevant.

[@mkoeppelmann](/u/mkoeppelmann) tweets some good points [here](https://twitter.com/koeppelmann/status/1036537351290478592)

And Vitalik’s thoughts on the topic [here](https://www.reddit.com/r/ethtrader/comments/9ch5ls/the_collapse_of_eth_is_inevitable_techcrunch_can/e5av470)

Coincidentally, Martin pointed out days ago the idea of paying miners without Ether. Vitalik proposes that wallets are unlikely to implement the feature due to its complexity. Regardless, the value attributed to Ether directly from transactions is negligible as the required sender holding of “working capital” can be little to none already. On the miner’s side, they are incentived to sell mining rewards as quickly as possible (especially with the tax structure in the US). Neither side of a transaction incurs significant holding - assuming instantaneous transactions. Therefore, Rubin’s first 3 points seem largely irrelevant even in the most bearish scenario where Ether never achieves any sort of SoV properties.

His last point on staking is more concerning. I do not have the expertise to say whether or not it is technically possible. But it is clear that in the event it does get implemented, other coins would steal “withholding” demand from Ether.

As Vitalik stated that full economic abstraction is unlikely, this is less concerning for Casper/PoS. But the argument still applies to other applications like Augur & Dai. By moving away from requiring Ether towards allowing all tokens, theoretical demand for Ether is lost. The Multi-Collateral change for Dai, while making the stablecoin more accessible to all, is relatively bearish for the price of Ether. If PoS + all applications built on top of Ethereum followed this scheme, there wouldn’t be any (non-speculative/non-SoV) reason to hold Ether.

If (core/Dapp) developers want Ether to be valuable, their code must be designed to require users to constantly hold Ether.

---

**MaverickChow** (2018-09-09):

Assuming your logic is 100% true,

1. What other currency/token would possibly be accepted by miners?
2. How will miners be assured that the price level of such currency/token accepted as payment is fair, not manipulated?
3. How will anyone be incentivised to secure the Ethereum network?

On question #3 above, let’s assume the answer is the miners will be incentivised by some XYZ token. How can the miners be assured the price level of this XYZ is fair and not artificially inflated? Assuming a significant chunk of economic activity is built on top of the network through asset tokenization, say with a total worth of USD 1 trillion, are we putting our trusts on these many different variations of 3rd-party XYZ tokens (each with own different smart contract rules and terms) to secure the network? If so, how will governance on such XYZ tokens take place?

It is good to think 1 step ahead (by implying the network does not need ETH). But would be much better if we think 10 steps further, because very likely if we think 1 step ahead we may stumble on totally different challenges at step 2. What makes you think the road ahead from step 2 and onward will be smooth sailing?

---

**MaverickChow** (2018-09-09):

Assuming if there is no reason to hold Ether and the price of Ether falls to zero, then how will the network be secured?

If ETH market cap is USD 0, then anyone can take control of the entire network.

If all other tokens operating on top of Ethereum are used to secure the network instead, then how will this be done safely and securely? Bear in mind, each and every one of the tokens is different in term of smart contract programming and governance. What about if a dApp is so useful that its token is used for over 51% of Ethereum’s network transactions? How will security and governance turn out then? Ultimately, you might as well just leave the security and governance part to a native currency that is Ether, thus a reason for having non-0 value.

You need to think of ways things can be gamed by rogue agents. You should not assume everyone to be kind, generous, honest, fair, and holy.

Have you guys actually thought this out in great detail, or is the opinion that Ether has no use just a passing thought? And are you guys sure that those suggesting Ether to have a value of 0 is not actually having a selfish-vested interest? For example, JohnDoe minted XYZ token and he suggested ETH to have no value so that XYZ can be the dominant currency in play for all matters relating to security and governance and if this happens, then XYZ token price will skyrocket making JohnDoe an overnight multibillionaire so he can cash out his profits, f***up the network in the process and retire happily somewhere without a trace. The problem is, JohnDoe is not the only one with such selfish incentive. Tarzan that minted ABC token, Skywalker that minted CDE token, MaryJane that minted DEF token, and countless others with their own tokens have similar selfish-vested interest. How will you guys solve this? Very soon, JohnDoe will learn to collude with Tarzan, Skywalker, and MaryJane, in which internal politicking, conflicts, and backstabbing will result. Tarzan would find ways to betray JohnDoe and the rest. MaryJane would find ways to betray Tarzan and the rest. JohnDoe would find ways to betray MaryJane and the rest. Eventually, the whole network would collapse. By the time you figured out the best ways to solve all these dilemmas, you may realize you already have ETH in place to solve them. And the only reason why nobody wants to cooperate and collaborate with ETH is purely because of the hope to see Ethereum dies so that all its economic worth would flow to another person. And this person may very well turn out to be just another screwup. Suggesting such multi-currency system may lead to such outcome.

When a person suggests Ether to have zero value, is he/she being objective? Or does he/she have hidden motive undisclosed?

The Ethereum blockchain needs ETH and ETH only.

The future world of blockchain needs collaboration and cooperation, not senseless competition for selfish reasons. The mindset needs to change to have a better world.

---

**MaverickChow** (2018-09-09):

The true worth of the Ethereum blockchain is not based on any of the tokens operating on top of it. Assuming your logic is true, that the combined market cap of all the tokens is in trillions and let’s say ETH value is so negligible its total market cap is just USD 1, then anyone that wants to take control of the multi trillions worth of “wealth” can just spend USD 1 to do so.

Initially, the idea was never about having dApps slapped with ICOs on them, so valuing Ethereum (or ETH, for short) based on the market cap of the dApps’ tokens is false.

Even then, the total market cap of all these tokens combined (assuming their value is fair and not inflated) is actually just a subset of Ethereum’s market cap so whenever you see the total market cap of all the cryptocurrencies at coinmarketcap, you are actually staring at gross double counting. The same can be said of every other blockchains that build dApps with ICOs on top of them, including EOS and NEO.

The true worth of the Ethereum network (and the ETH that comes with it for security and governance) is based on something else far larger than all the dApps combined by multiple fold.

---

**savant.specter** (2018-09-09):

Focusing on the academic questions you propose. This seems to be a fundamental underlying premise of your thoughts:

> If ETH market cap is USD 0, then anyone can take control of the entire network.

But what does it mean to “take control of the entire network?” For most definitions, “Ether Market Cap = 0” does not imply “take control costs = 0.”

Do you mean “hijack block creation,” “control transaction inclusion,” “own a token majority,” or something else? All of these have very different interactions with the Ether token. So I’m not sure I understand your logical progression.

---

**MaverickChow** (2018-09-09):

Assuming ETH is not needed at all, then what will be used to secure the network?

And what assurance is there that this alternative to ETH will do a better job?

And if this alternative can do a better job than ETH, then why does it not start its own blockchain?

When a person suggests that use case of ETH is negligible and that other tokens can be used in place of ETH, what incentive does this person have in making such suggestion?

I have ETH and I don’t mind if ETH totally dies if there is a much better alternative out there in solving the problems of consensus, security and governance, but I don’t want ETH to die only to give way to an alternative that is just another form of money grab pretending to be superior.

I see too many people talking down another coin only because they want the economic worth of the coin to flow to them instead.

It is not really because they have a better alternative.

If the value of ETH can be made negligible, then the same be made on every other tokens too.

