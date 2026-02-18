---
source: ethresearch
topic_id: 5315
title: "Elasticoin: low-volatility cryptocurrency with proofs of sequential work"
author: nullchinchilla
date: "2019-04-16"
category: Economics
tags: [proofs-of-sequential-work]
url: https://ethresear.ch/t/elasticoin-low-volatility-cryptocurrency-with-proofs-of-sequential-work/5315
views: 4110
likes: 10
posts_count: 14
---

# Elasticoin: low-volatility cryptocurrency with proofs of sequential work

[elasticoin-icbc.pdf](https://ethresear.ch/uploads/default/original/2X/0/01ed80d5d42dbfc951beddee9e048efad540a1d7.pdf) (151.1 KB)

I want to solicit some discussion on **Elasticoin**, which I’m going to present as a short paper at [IEEE ICBC 2019](http://icbc2019.ieee-icbc.org/), which is a rather weird cryptocurrency issuance scheme I’m using in my blockchain project Themelio.

The goal of Elasticoin is to have a cryptocurrency that has much lower price volatility than coins like Bitcoin, Ethereum, etc, while having an entirely endogenous and trustless algorithm that’s resilient to external economic shocks (so no pegs to USD, no price oracles).

The general idea is ridiculously simple: we fix the real cost of minting a coin. If creating 1 coin costs you $1, obviously the price of the coin is capped at $1. Naively you might think this leads to a coin that fluctuates in price just as much as Bitcoin does, except capped at $1, but that’s not actually true. Most of the volatility in cryptocurrency prices is based on speculation on the slight chance the price is going to the moon — since traditional cryptocurrencies have fixed supplies, “mainstream adoption” means mooning prices. Thus, every piece of news, or every random investor panic, is going to cause massive price swings due to “chance of Bitcoin worth >$1M in 2030” changing several times in different directions.

The hard problem is fixing the cost without oracles. The naive solution would be to basically use PoW without adjusting the difficulty; this is not going to work because sudden technological advances will cause massive hyperinflation.

Instead, we make it so that **one day of sequential computation on the fastest processor available *right now*** mints you a coin. This can be done trustlessly by leveraging proofs-of-sequential-work that essentially prove that you computed an iterated Argon2 hash a zillion times. Completing a protocol-given sequential puzzle gives you a fixed reward, while difficulties and rewards adjust so that the fastest solver the blockchain has seen solves the puzzle in exactly 24 hours. We also penalize solvers that are slower than the fastest solver, making using GPUs or ASICs where each core is slower but ops per watt are lower, or “free” spare compute cycles on web servers, uneconomical. The exact algorithm is pretty simple and can be seen in the attached paper (read: I’m too lazy to retype a bunch of LaTeX formulas)

(Note that Themelio is a PoS blockchain, so rewards from the Elasticoin minting have nothing to do with incentivizing consensus. Think of the coin as an ERC20 minted by a smart contract verifying people’s puzzles)

This is a rather weird metric to use, but empirically the cost of “up-to-date” sequential processing time is actually pretty stable. The price of renting single cores hasn’t really changed ever since processors were fully mass-produced. Physically you also don’t see massive improvements in sequential processing speed in the future, and it’s likely to be really hard to make ASICs dedicated to sequentially computing Argon2 that are much cheaper and faster than CPUs.

What we get is a coin that’s basically pointless to HODL in hopes of it mooning, because it’s guaranteed that it won’t. The trading market would look a lot more like trading fiat currency pairs, and a lot less like the Bitcoin market. Coin prices won’t be completely stable (gluts from demand declines will still cause price declines, price shocks in electricity and silicon will affect the coin), but they will almost certainly be much more money-like than Bitcoin. I think that for users wanting a good medium of exchange or gas-paying token, this is a big positive, and could attract the “right” kind of attention and adoption that doesn’t correlate strongly with price bubbles.

## Replies

**adlerjohn** (2019-04-16):

Interesting first attempt at what I’ve been calling an “arbitrage oracle.”

Unless I’m mistaken, your design has two stable equilibria: one at $0 and one at $1 (normalized wlog).

1. If the price of a stablecoin goes above $1, more is issued—in this case by more minters joining in a decentralized manner. This prevents a price of $infinity being an equilibrium.
2. In the case a stablecoin goes below $1, then some coins need to be burned/re-bought. This prevents a price of $0 being an equilibrium.

Your algorithm covers case 1 but not case 2, so your stablecoin will have two equilibria. Unfortunately, the equilibrium at $1 is less stable than the one at $0, so the coin will end up being truly stable at a price of zero.

I shouldn’t have declined being a reviewer for this conference when asked back in December, if I knew I was going to be reviewing submissions anyways!

---

**nullchinchilla** (2019-04-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> I shouldn’t have declined being a reviewer for this conference when asked back in December, if I knew I was going to be reviewing submissions anyways!

Haha…

To reply to your comment, Elasticoin explicitly doesn’t want to be a “stablecoin” in the sense of holding a peg to a target price with an equilibrium mechanism. If the cost of minting is $1, you can easily imagine the coin bouncing back and forth between $0.2 and $0.3. The *threat* of minting at $1 is enough to cut off speculation about “how many millions is the coin gonna be worth in a century”. Note that $1 in this case is a slowly varying, not-obvious number that depends on things like the price of electricity, so we wouldn’t expect any sort of Schelling-point that “fakes” a peg until a panic happens.

With stablecoins, you implicitly promise a fixed price at $1, and its entire value proposition is based on holding the peg, so you do need a very stable and unique equilibrium. Otherwise, a minor deviation can totally destroy the coin as everybody panic-sells. My goal is a lot more modest — it’s a true cryptocurrency used for payments and gas payments, but one that you are pretty much guaranteed to lose money by HODLing, and can be used as a reasonable unit of account.

I do concede that over a long period of time the coin might inflate quite a bit more than US dollars. The USD/coin exchange rate might look like that of a currency of a third-world country. But even those currencies are much less volatile than Bitcoin, and in an efficient market inflation can easily be hedged by holding bonds/stocks issued by DAOs anyway — money is neutral in the long run. Despite Bitcoin etc, I don’t think “no inflation ever” is a necessary condition for a successful cryptocurrency, just “no arbitrary inflation by a sovereign issuer for its own benefit”.

---

**marckr** (2019-04-17):

You’re on an intriguing direction. Eager to see how this works going forward!

---

**dankrad** (2019-04-20):

Very interesting. However, I wonder how you are going to create demand for it in the first place. A large part of the value proposition of all current cryptocurrencies and tokens comes from the promise of being worth millions down the line. If there is no chance whatsoever that is going to be the case, then why should I invest anything now into a volatile asset?

So you are going to have a hell of a chicken and egg problem here, you basically need to create a demand for this token without having an economy based on it.

---

**marckr** (2019-04-20):

What was the demand for a cryptocurrency in the first place? I would argue that aside from the [Economic Majority](https://en.bitcoin.it/wiki/Economic_majority), a la BTC, it came down to something different. A hedge against the turmoil of the period? A safe store for assets? Perhaps this entire space is simply a demand for stability that now wrests with the powers that be.

We have a grave chicken and egg problem, but we are going to get past it. Demand is on understanding the utility needs of holders, and so proposes a model more toward [Intertemporal Consumption](https://en.wikipedia.org/wiki/Intertemporal_consumption).

---

**marckr** (2019-04-20):

I stated privately about the prospect of some quasi-enlightened class of cryptocurrency holders around 2011. Many went on to help build this network. A new set of money, fungible in exchange, demands then the funding and furtherance of that core mission. These are no static concepts.

---

**lebed2045** (2019-04-21):

Thanks for sharing your ideas here! It’s definitely an interesting concept to adjust PoW complexity based on the speed of sequential work rather than prove of total work.

About price stability, I think it’s not going to work. The stability proposition is basically based on the assumption that **cost of mining** is influencing the **price minted coin**.

I might be wrong but looks like the price is fundamentally determined **only by demand/supply equilibrium**. In other words, the cost of producing the goods/services don’t directly influence the price. What does is the amount of these goods/services available on the market and the demand for these goods/services.

In case of minting coins if the number of coins going to be “produces” is predetermined,

![](https://ethresear.ch/user_avatar/ethresear.ch/nullchinchilla/48/2606_2.png) nullchinchilla:

> Completing a protocol-given sequential puzzle gives you a fixed reward, while difficulties and rewards adjust so that the fastest solver the blockchain has seen solves the puzzle in exactly 24 hours.

the only factor which is going to influence the price is the current demand. Since demand is driven by people who are exchanging money for these coins for some sort of utility, unless utility is connected with production cost - the main proposition is wrong.

---

**nullchinchilla** (2019-04-21):

In Themelio, there are actually two tokens, named the **mel** and **vol** (abbreviated TMEL and TVOL; I might change the names to something catchier).

TMEL is the main currency, used for all transaction fees and other in-protocol fees, and intended to be used in an economy. It’s minted through the Elasticoin algorithm and won’t have a really volatile price.

TVOL are “shares” in Themelio; they have a fixed supply of 1 million TVOL and are the only token usable for staking in PoS. TVOL essentially is a share of the transaction fees generated by TMEL users, and will have a volatile price driven by speculation on the discounted future revenues from fees.

So people wanting to invest/speculate in something that might “moon” will buy TVOL, and people participating in the Themelio ecosystem would use TMEL. I think that TVOL has enough draw as an investment asset to garner interest in Themelio without an economy existing yet.

---

**nullchinchilla** (2019-04-21):

The reward is not literally fixed, but rather adjusted downwards as processors become faster such that one day of sequential processing mints you a coin.

Any coin’s price is driven by demand and supply; Elasticoin’s difference is to make supply respond to changes in price (supply elasticity, hence the name). In Bitcoin etc no matter what the market conditions are, BTC is minted at a fixed rate. With Elasticoin, minters will mint coins when coin price is above the cost of one day of sequential computation, and stop minting coins when it’s not. This should reduce volatility.

The scheme also ends up giving a ceiling to speculation about future coin value, which should reduce swings due to panics/hypes about possible future adoption.

---

**xiaohanzhu** (2020-06-27):

Just heard about this thread from a fellow researcher.  I suggested you to take a look at https://meter.io  We create a new economic game and consensus model to address all the concerns mentioned in this thread.

Meter has a dual token economy.  The low volatility currency token MTR has a fixed production cost of 10kwh/token with SHA256 in main stream BTC miners.   Competitive electricity price has been more stable in purchasing power than any fiat currencies in the world during the last 70 years.   The governance token MTRG is the staking token for maintaining the ledger.  We use HotStuff consensus so the system doesn’t require strong synchrony and can be highly decentralized.   The only way to obtain newly created MTRG is to use MTR to participate in the daily onchain competitive bidding.  The proceed of the auction will partly be put into a system reserve and partly distributed as block rewards to PoS validators.  Essentially MTRG is the “BTC” in the system.  In BTC, miners use hashing power to directly compete for newly created BTC.  In Meter, miners first convert their hashing power into mining credit MTR and use the credit to compete for the newly created “BTC” (MTRG).

The project started in early 2018 and we are launching mainnet next week.  We will see the actions in the real world.

---

**SebastianElvis** (2020-06-27):

Interesting idea and initiative. If I understand correctly, this scheme is only for “minting”, i.e., how coins are issued, rather than consensus, i.e., who mines the next block. If so, this minting scheme should rely on a separate consensus protocol (say Thermelio as you mentioned). Then, you price coins using the cost of solving PoSW in order to stabilise coin prices.

I’m wondering whether the following issues exist.

1. The computational cost is not the only variable that influences the price. For example, the consensus also influences the coin price, e.g., when the consensus is proven flawed, the coin price will become zero. In other words, this scheme assumes all other factors affecting the coin price are fairly stable.
2. Should the register process be sybil-resistant? What if someone generates a huge number of register transactions? Maybe transaction fee applies here? If there is transaction fee, then it should be much less than the reward of solving the PoSW puzzle. Not sure if this always holds when transaction fee is fluctuating.
3. Not sure if this scheme will reduce the security of consensus. In blockchains, minting is not only for issuing coins, but also for incentivising nodes to participate in consensus. With more nodes (mining power) in the system, the consensus will be more secure. In this scheme, nodes with more processors can get more reward. If the underlying consensus uses another resource to measure the advantage of nodes, then nodes may not have incentive to invest such resource to consensus. For example, if using deposit-based PoS-based consensus, then nodes will not choose to deposit much coins. Instead, nodes will buy more processors and solve lots of puzzles concurrently for more reward. When this happens, the amount of deposit for consensus is small, and the adversary may break the consensus (e.g., 51% attack) by using a small amount of deposit.

---

**cangurel90** (2020-10-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/nullchinchilla/48/2606_2.png) nullchinchilla:

> The hard problem is fixing the cost without oracles. The naive solution would be to basically use PoW without adjusting the difficulty; this is not going to work because sudden technological advances will cause massive hyperinflation.

a solution to this is addresed by dynamic block rewards that take into account moorse law for effeciency improvements [Meter Tokenomics. Currency pegged to 10 kWh electricity… | by Can Gurel | Medium](https://1yousef-yousef7.medium.com/meter-tokenomics-2a3a29c108fe)

---

**IShyshatskyi** (2021-01-15):

A very interesting thread. I’ll use it as an opportunity to give some exposure to our project JaxNetwork. We utilize a very similar idea. We believe we have gone much further than anybody else here. I believe our project might be interesting to people who already think in this direction and conduct experiments with block reward functions.

The main goal of our project is not to create a coin which has a low volatility. We build a scalable blockchain network based on sharding and merged mining. We have found that the reward scheme in which block reward is proportional to block difficulty is the only way to go. Apparently, it’s the only way to set a proper tokenomics in sharded blockchain network.

Obviously, technological progress and new more power efficient mining equipment poses a thread to the coin price stability. Therefore we use adjustment coefficient based on Koomey’s law. Yes, it’s Koomey’s law, not Moor’s law. It’s a more accurate name for this consistent pattern.

This block reward scheme was reinvented many times since the early days of Bitcoin. You can find some old threads at bitcointalk forum. However, it’s true that many people find this approach rather weird.

