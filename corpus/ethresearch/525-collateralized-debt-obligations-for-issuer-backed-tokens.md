---
source: ethresearch
topic_id: 525
title: Collateralized Debt Obligations for Issuer-Backed Tokens
author: vbuterin
date: "2018-01-08"
category: Applications
tags: []
url: https://ethresear.ch/t/collateralized-debt-obligations-for-issuer-backed-tokens/525
views: 21930
likes: 25
posts_count: 36
---

# Collateralized Debt Obligations for Issuer-Backed Tokens

*Special thanks to some discussions from Dominic Williams from 2015 that brought up the idea of multi-issuer collateral-risk-reduced stablecoins.*

One major type of “stablecoin” that already exists, and will likely continue to become more popular, on public blockchains is the issuer-backed token (eg. [Tether](https://tether.to/?p=7889), and likely soon Digix Gold). In this model some centralized issuer maintains a reserve (likely a bank or brokerage account or vault depending on context) of some underlying backing asset, and issues a quantity of tokens on the blockchains equal to the quantity of the backing asset. They promise that each unit of the blockchain token will be redeemable for a unit of the backing asset.

This kind of token is attractive because it avoids the [financial “black swan” risk](https://prestonbyrne.com/2017/12/10/stablecoins-are-doomed-to-fail/) of stablecoins like DAI that are purely backed by crypto, but it comes with its own set of problems, chief among which is that it brings back the spectre of counterparty risk. Issuers of backed tokens are often met with suspicion, and the tokens are often avoided as a result.

The following is a proposal for how to mitigate this risk, effectively creating 1-of-N issuer-backed stablecoins that only fail if most or all of the issuers fail.

---

Suppose that we have N issuers of USD on the blockchain, `I[1] ... I[n]`, and there exists a DAO into which M coins from each issuer have been deposited. The DAO releases N new assets, which we call “slice 1” … “slice N”, effectively ordered low risk to high risk. The goal is as follows: buyers of slice 1 will be able to redeem a dollar if at least one, any one, of the issuers continues to be solvent. Buyers of slice 2 will be able to redeem a dollar as long as at least two issuers are solvent. And so on and so forth until slice N, which will be able to redeem a dollar only if all issuers are solvent.

The expected loss component of counterparty risk can never be reduced or removed - if the issuers collectively lose $X, that loss of $X has to be paid by *someone*. But what this does let us do is channel the risk toward those who are most willing to bear it, and give those who are not an asset that is highly robust, losing value only if a very large number of issuers fail.

To compensate those who are willing to bear risk (or those with insider knowledge that allows them to trust the issuers more than the general public does), the holders of slices closer to N would be paid interest rates, which would come out of the pockets of the holders of slices closer to 1.

---

Now, on to implementation. The coins are issued at time T, and have a pre-determined duration D. Before T, anyone is allowed to specify a bid, of the form “I want to buy a unit of slice `i`, and I am willing to pay `x / N` units of *every* coin in the basket to purchase it”. The system then keeps track of the bids in highest-to-lowest sorted order for each slice, and once the bidding period ends it starts processing the bids. It looks at the top bid for each slice, and sees if the top bids sum to at least 1. If they do, then it accepts the bids, and if they do not then it terminates.

At the end of the process, everyone who bid for slice `i` pays the same price as the last (ie. lowest) accepted bid for slice `i`. This mechanism ensures that, for every set of bids the system accepts, the system issues one coin for each slice and receives at least one coin from each issuer as backing, so it will be able to meet all obligations.

At time T + D, comes the claiming phase, which is split into N periods. In the first period, everyone who has a coin of slice 1 can redeem it in exchange for a coin from any issuer of their choosing. In the second period, everyone who has a coin of slice 2 can do the same, though if there is some issuer whose coins have already been fully drained by the redeeming process they can naturally no longer be claimed. This continues for all N slices.

This mechanism removes the need to have any kind of fancy dynamically adjusted/controlled interest rate, or an oracle to tell which issuers are insolvent. If `k` of the N issuers are insolvent, then holders of coins in slices 1…N-k would redeem all of the solvent coins first, leaving the holders of coins in slices N-k+1…N with worthless coins; the need for an oracle is substituted with market-based preference revelation.

To create an infinite-duration coin on top of this, one can simply imagine a DAO that creates rounds of this game with duration 2D every D (ie. there are always two overlapping games) and another DAO which buys tokens of some specific slice on the open market a quarter of the way through their period and sells them three quarters of the way through to buy the coins from the next game.

### Variations

- Have one of the “issuers” be a contract that holds ETH and has a redemption process that allows holders of a coin to claim an amount of ETH equivalent to 1 USD. The contract’s USD liabilities would be half the value of its ETH holdings at the start, and if the contract becomes insolvent it would simply give each token holder an equal share of its entire quantity of ETH. Any undistributed ETH would be given to a second class of token holder, who would thus be holding “ETH at 2x leverage”
- Come up with more complex combinatorial mechanisms that allow people to express through the market opinions like “I think issuers 1, 4 and 11 are solvent but have no idea about any of the others”
- Have one of the “issuers” be DAI

## Replies

**FBrinkkemper** (2018-01-08):

Great concept.

I am working on a concept of asset backed tokens, and was thinking about improvements in regards to decentralization. I don’t quite understand yet the reason for the pre-determined duration D, but I presume it is to check solvency every so often?

A few general questions:

1. Do you think it would be possible, and productive, to merge this Issuer-backed token model with a DAICO, or can this be viewed as a DAICO with a set selfdestruct every D?

> … and receives at least one coin from each issuer as backing, so it will be able to meet all obligations.

1. In the case of Digix Gold, the issuer needs the coins they receive to buy the gold. How would they be able to meet this at least one issuer-backed coin requirement?

Thanks Vitalik for being such a vocal researcher.

---

**adamluc** (2018-01-18):

[@vbuterin](/u/vbuterin)

Really interesting proposal around a stablecoin alternative.

I am curious, why would the more complex structure that replicates bond tranches to price risk and derive a market-driven interest rate be superior to utilizing ERC-20 backed Tether (USD and/or Euro), Digix Gold, and other crypto assets to back the stablecoin DAI? Counter-party risk would be minimized through the backing of assets from outside of crypto such as USD and Euro as well as Gold. Additionally, as a backstop to Tether and Digix Gold, MKR could be sold to recapitalize the CDP’s that back DAI if a significant swing in crypto prices and/or black swan event were to occur.

Thanks Vitalik!

Adam

---

**EazyC** (2018-01-18):

Hey Vitalik,

Great ideas as usual. I like the fact that this setup makes oracles obsolete/less vital for these asset backed tokens. That is truly the most innovative aspect of the proposal imo. But while we are on the topic of stablecoins and oracles, what do you think of the idea of non-asset/non-collateral backed stablecoins which make use of expansion and retraction of supply instead of 1:1 exchange promises? Such as basecoin. Do you still see the issuer-backed tokens as the main stablecoin of choice in the ETH ecosystem? I ask this because those types of stable tokens also have a lesser requirement for oracles if the expansion and retraction signals are given as schelling point schemes.

---

**vbuterin** (2018-01-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/adamluc/48/555_2.png) adamluc:

> why would the more complex structure that replicates bond tranches to price risk and derive a market-driven interest rate be superior to utilizing ERC-20 backed Tether (USD and/or Euro), Digix Gold, and other crypto assets to back the stablecoin DAI?

Doesn’t this depend on having price feeds for the various ERC20s so that you know when to trigger liquidation calls for CDPs? My scheme does not depend at all on price feeds; it instead gets the same effect through incentivized preference revelation (ie. people participate in the “implied price feed” by choosing which asset they withdraw).

> Such as basecoin.

Personally I’m not sold on basecoin specifically; it’s coins/bonds/shares model seems a bit iffy and unnecessarily complex. Particularly, there’s the instability that if the basecoin price goes down, then the mechanism pushing the price back up is to get people to buy basebonds, but basebonds basically just lock you into holding basecoin, and it’s not clear why people would want to do that; it seems too close to the old bitusd model (“we just say that the price of this token should be $1, and therefore people will buy if it’s under $1 and sell if it’s over $1 because they expect the self-fulfilling prophecy to be true”) for comfort. I am more of a proponent of seignorage shares: [GitHub - rmsams/stablecoins](https://github.com/rmsams/stablecoins)

Another thing I have thought about is that in an economic model where you do not assume altruistic honesty or non-coordination, it’s not clear that makerdao has a higher security level, or even that it’s possible to achieve a higher security level, than seignorage shares. If the total discounted expected future profits of the scheme are lower than the amount of capital inside it, then the shareholders have the incentive to manipulate the price feed in order to siphon everyone’s money out. I’d be interested in seeing more detailed analysis on this.

---

**bradleat** (2018-01-20):

From my understanding of MakerDao the incentive to use a good price feed comes from the holders of MKR. As you noted, if total discounted expected future profits are lower than some current accessible value, then shareholders have an incentive to manipulate something to take money out. I might need some help here, because I can’t figure out how this would happen…

To siphon money out of the system (when price feed inclusions are votable), you’d have to manipulate the price feed and have coordination amongst the majority of MKR holders to do that. (The incentives of the operators of the price feed deserve their own analysis)

Furthermore to siphon money out of the system by setting the price feed incorrectly, it is not clear to me that MKR holders are the beneficiaries.

If the price feeds get set low, so people are getting margin called then people (not just MKR holders) have access to cheap collateral through the auction mechanism. In another scenario (the “bravo” scenario), MKR itself would be diluted to raise DAI to recapitalize the failed CDPs. At the same time, the collateral of the CDPs would be sold to remove MKR from the circulating supply.

If the price feed were manipulated to make bravo scenario likely, MKR is being auctioned for DAI a rate set by the market. It’s hard to know what this rate would be in the scenario given the open manipulation that is going on, in the best case scenario for the attack you are asking about, the rate would be favorable for MKR and DAI would still have some lasting value despite the manipulation of the system. At the same time, collateral would be available cheaply (in DAI terms) and the proceeds would be used to remove MKR from the market. This low rate used to create the attack negatively impacts the amount of value that can be transferred to MKR.

---

The other way around would be manipulate the price feed so that the price for the collateral is higher than in reality. By doing this the system’s collateralization rate would increase. At low prices increases this would help CDP holders and possibly MKR holders by increasing the stability fees paid into the system. However, if the true collaterlization rate came into danger DAI would likely lose market value.

This manipulation seems like an effective lowering of the collaterlization rate needed to create CDPs. It’s not clear to me that the amount of accessible value this creates for MKR holders can ever be significant. If the true collaterlization is 150% then MKR holders could see up to 33% bumps in fees paid into MKR for a stability fee in the short term, however if this impacts the solvency of their DAI product it would destroys the future value of MKR in the process.

---

I agree that there is an incentive for MKR holders to mess around with this collaterlization rate to siphon money out of the system. I think the plain mechanism of adjusting the collaterlization rate is better than manipulating a price feed higher. However this siphoning is at the risk of the MKR holder as collaterlization rate decreases (or price feed that increases the value of collateral) risks the future value of the entire system.

---

**MicahZoltu** (2018-01-20):

[@bradleat](/u/bradleat) I’m hesitant to make any assertions on this, but I’m reasonably confident that in DAI (the eventual implementation, not current implementation), when CDPs are liquidated collateral is sold off for DAI, not MKR.  The only time MKR is bought & burned is when fees are assessed.  Since fees on the short term are somewhat insignificant relative to the value of MKR (just as dividends for stocks are a very small percentage of the value of the stock) causing the system to fail to do its job in order to get more fees isn’t worth it, because it is very likely that the decreased system confidence will decrease the value of MKR far more than the minuscule fees you’ll get.

MKR is minted when a lender of last resort is needed to get the system out from under water, and MKR holders are strongly incentivized to have this never happen because it is a pure loss scenario for all MKR holders when it occurs.

In short, MKR holders manipulating the oracles would not benefit much.  CDP holders on the other hand may.  Now if MKR holders == CDP holders then perhaps there is reason to manipulate?  e.g., set oracle price feeds such that 1 ETH == 10000000 DAI, then CDP holders can all exit their CDPs effectively for free (getting out their capital).  I believe the Maker team has discussed including a limit on how fast the oracles can change the price (of course, this then leads to the inverse problem where the oracles are unable to keep up with the real price).

---

**vbuterin** (2018-01-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/bradleat/48/527_2.png) bradleat:

> it is not clear to me that MKR holders are the beneficiaries.

What if the MKR holders are also CDP holders? Then they can manipulate the price feed to make it look like the price of ETH is infinity, and do a global settlement. Without the global settlement, they could withdraw an arbitrarily large amount of DAI and sell it, though revenue from this would be limited as it would quickly crash the market. Alternatively, if the MKR holders were also DAI holders, they could manipulate the price feed down, at which point all of the ETH in the CDPs could be distributed to them.

Though you are right that both attacks are fairly messy, and would not get anywhere close to stealing all of the collateral in the system.

---

**bradleat** (2018-01-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I’m hesitant to make any assertions on this, but I’m reasonably confident that in DAI (the eventual implementation, not current implementation), when CDPs are liquidated collateral is sold off for DAI, not MKR.

I was referring to MKR being minted as the lender of last resort.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Though you are right that both attacks are fairly messy, and would not get anywhere close to stealing all of the collateral in the system.

I guess the detailed analysis then would be:

> What is the concentration of MKR holders in CDPs or DAI where there is an incentive to perform an attack (through global settlement, otherwise)?

I need to read up on the global settlement mechanism (current implementation, planned implementation)…

---

**denett** (2018-01-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Have one of the “issuers” be a contract that holds ETH and has a redemption process that allows holders of a coin to claim an amount of ETH equivalent to 1 USD. The contract’s USD liabilities would be half the value of its ETH holdings at the start, and if the contract becomes insolvent it would simply give each token holder an equal share of its entire quantity of ETH. Any undistributed ETH would be given to a second class of token holder, who would thus be holding “ETH at 2x leverage”

Interesting contact!

In this contract the second class token holder will actually hold a call option with ether as the underlying. This option has a strike price of half the price of ether in USD at the start of the contract.

The first class token holder will have an equivalent of 2 USD worth of ETH and a short call option.

The time value of the call option (current price of the call minus the price of the call if would expire now) depends strongly on the volatility of the underlying. Cryptocurrencies are notorious for their volatility, so at the start of the contract the second class token will be worth significantly more than 1 USD and the first class token significantly less.

Although you can use the first class token as a coin in the proposed CDO, it is quite risky and not stable at all.

The risk can be lowered for the first class token holder by adding more ether in the initial contract. For example if you add N ether in the contract you can create N classes of tokens constructed in a similar way as the CDO.

---

**EazyC** (2018-01-22):

Good insights about basecoin. I agree that their 3 token system is unnecessarily complex - at most it should just be a 2 token system. But just a quick question:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> basebonds basically just lock you into holding basecoin, and it’s not clear why people would want to do that

Is the main different between seignorage shares and basebonds in that the shares allow for holding of the abstracted volatility of the stablecoin while basebonds are simply a future IOU of a basecoin? That’s the only main difference I can see, is there any other differences between the basebond and the seignorage share?

Also, just as an aside, I don’t think anyone has implemented a seignorage share based stablecoin, which is a shame. I definitely agree with you it’s the simplest and most elegant system. Perhaps someone can develop one on ethereum to compete/compare to the collateralized issuer-backed gen1 stablecoins.

---

**vbuterin** (2018-01-23):

I definitely think seignorage shares should be tried. I’m actually surprised that no one has yet just taken the paper verbatim and ICO’d it…

---

**denett** (2018-01-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/eazyc/48/5266_2.png) EazyC:

> Is the main different between seignorage shares and basebonds in that the shares allow for holding of the abstracted volatility of the stablecoin while basebonds are simply a future IOU of a basecoin?

One big disadvantage with the basecoin proposal is that the basebonds are not a commodity. Every bond has his own position in the queue, so they are all valued differently. This makes them harder to sell.

---

**EazyC** (2018-01-25):

It’s funny you say that because while I 100% agree with you, the basecoin whitepaper actually criticizes seignorage shares because “shares are too difficult to price individually.” So it’s interesting that they see it as an advantage rather than a disadvantage. Like Vitalik said above, I really think seignorage shares should be tried out in the wild, perhaps inside ETH itself or its own chain using Casper or PoS as the consensus method. More stablecoin competition is a good thing.

---

**bradleat** (2018-01-26):

The problem I see with seignorage shares is that the system relies on its future popularity to achieve a stable coin. As far as I can tell, there is no collateral that can bootstrap the system and provide participants with a concrete reason that the coin should be transacted at a price point set by the contract.

Absent this claim on collateral, the system may need a permanent participant willing to accept the coin a price. For instance, it would make sense to me if a block chain such as Ethereum worked with a seignorage share model to dampen volatility. (Not that I’m proposing this)

---

**EazyC** (2018-01-26):

Even the US Dollar (the role model of all shitcoins jk jk), started out pegged to gold and then ended up floating their currency so you might have a point about initially not being backed by anything. However, I personally don’t think that would be an issue given sufficiently large enough size of the stablecoin/seignorage share pool and market cap. For example, I can’t see a seignorage share system being too unstable (assuming the entire premises work out in practice and it’s not just a faulty idea) if the entire market cap of the stablecoin is 20B+ then it can resist a lot of market manipulation and exchange/whale pressures and slowly increase adoption and the circulating supply. However, if the entire circulating supply is just a few billion market cap USD then the peg can very easily break since it’s just a floating point currency in its early days.

---

**denett** (2018-01-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/eazyc/48/5266_2.png) EazyC:

> It’s funny you say that because while I 100% agree with you, the basecoin whitepaper actually criticizes seignorage shares because “shares are too difficult to price individually.”

This is indeed funny, because as soon as you create a market for shares, a price is the result.

For the bonds there is no liquid market, so pricing them is much harder.

![](https://ethresear.ch/user_avatar/ethresear.ch/bradleat/48/527_2.png) bradleat:

> The problem I see with seignorage shares is that the system relies on its future popularity to achieve a stable coin. As far as I can tell, there is no collateral that can bootstrap the system and provide participants with a concrete reason that the coin should be transacted at a price point set by the contract.

I think you only need collateral for bootstrapping the coin, as soon as the usage is big enough to create a liquid market for the both the coin and the share, it will be quite stable.

You could bootstrap it, by auctioning of N million coin/share pairs and keep that in the contract. After a year people can trade x% of outstanding coins/shares for x% of the ether in the contract.

![](https://ethresear.ch/user_avatar/ethresear.ch/bradleat/48/527_2.png) bradleat:

> For instance, it would make sense to me if a block chain such as Ethereum worked with a seignorage share model to dampen volatility.

I agree with you, the goal price of eth could be the average price of eth in USD of the last X month.

Even when the price is not completely stable, it will be a huge improvement over the current price swings.

---

**SRALee** (2018-01-28):

> This is indeed funny, because as soon as you create a market for shares, a price is the result. For the bonds there is no liquid market, so pricing them is much harder.

You make a very good point in that bonds are not fungible. But perhaps that was the basecoin team’s main goal? I definitely like the fungibility of seignorage shares though.

> I think you only need collateral for bootstrapping the coin, as soon as the usage is big enough to create a liquid market for the both the coin and the share, it will be quite stable.
> You could bootstrap it, by auctioning of N million coin/share pairs and keep that in the contract. After a year people can trade x% of outstanding coins/shares for x% of the ether in the contract.

Can you expand on this? What do you envision the bootstrapping/ether pool doing? I think it is an interesting idea but essentially it is just propping up the system until the “training wheels come off” right? What would a system like this entail if further thought out? The beginning of the system is collateralize and then it moves off after a year?

---

**denett** (2018-01-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/sralee/48/1134_2.png) SRALee:

> What do you envision the bootstrapping/ether pool doing? I think it is an interesting idea but essentially it is just propping up the system until the “training wheels come off” right?

The bootstrapping using the ether pool has 2 purposes, marketing and collateral. You want as many people involved in the project. Selling coins/shares will do that. Second, you want the first users to trust the coin. You basically put in a lower bound so the initial coin/share market will not go south.

The team now has a year to proof two things:

1. It can create a liquid market for the coin/share pair.
2. The coin is being used. For example accepted in shops and traded on exchanges.

If you can convince people you can pull this off before you launch the coin, you will not need an ether pool.

---

**SRALee** (2018-01-28):

You’re technically right and it is a rather clever setup, but my main fear in this situation is that the transition between the tokens becoming collateral backed and floating after 1 year could potentially be very rocky if the market has priced in the lower bound as part of the intrinsic worth of the tokens. For example, if the collateral puts a lower bound at 30 cents to a stablecoin pegged at $1, then it is difficult to know how much of the $1 price is propped up by the collateral. As the one year mark approaches and the ETH pool is set to be removed from the system, it is difficult to know if the price of the stablecoin will adjust to 70 cents since there is no way to check if the $1 price was the sum of collateral + coin or just coin. Otherwise, I like your bootstrapping method.

---

**denett** (2018-01-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/sralee/48/1134_2.png) SRALee:

> For example, if the collateral puts a lower bound at 30 cents to a stablecoin pegged at $1

The collateral does not put a lower bound on the stable coin but it is a put option that users can use when the total market-cap of shares and coins is lower than the value of the collateral.

If the coin is a success, the total market cap will rise in the first year and the put option will be far out of the money. Options that are “far out of the money”, have their price go to zero when they are about to expire, because the chance that the option can be used is low. In this case, the collateral can be removed easily.

If the total market cap of the shares and coins is close the value of the collateral, when the option is about to expire, the project probably has failed. But at least the investors will get their money back.


*(15 more replies not shown)*
