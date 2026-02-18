---
source: ethresearch
topic_id: 1081
title: A signaling theory model of cryptocurrency issuance and value
author: vbuterin
date: "2018-02-14"
category: Economics
tags: []
url: https://ethresear.ch/t/a-signaling-theory-model-of-cryptocurrency-issuance-and-value/1081
views: 33281
likes: 71
posts_count: 43
---

# A signaling theory model of cryptocurrency issuance and value

[Updated and cleaned up 2018.10.09]

One argument often brought up by single-cryptocurrency maximalists is that if creating new cryptocurrencies becomes legitimate, then it will be possible to print new cryptocurrencies into existence at near-zero cost, causing cryptocurrency as a whole to hyperinflate and lose value. To prevent this possibility, the argument goes, we must establish a very strong norm that the currently dominant cryptocurrency is the only legitimate cryptocurrency, putting it in a fundamentally different reference class from all others - “there is bitcoin, and there are shitcoins”. However, there are now thousands of cryptocurrencies, and it is clear that cryptocurrency as a whole has not lost all value. But why not?

Theoretically, there is an infinite number of possible equilibria of which cryptocurrencies maintain a nonzero value: just Bitcoin maintains value, just Bitcoin Cash maintains value, just Bitcoin and Ethereum, just IOTA, just those in the current top 1000 on coinmarketcap where the sha256 of the listed name is a prime number, etc. But there are also equilibria where the set of cryptocurrencies with nonzero value is not fixed, and new cryptocurrencies can join. However, if just about any cryptocurrency can join the club, then everyone will be able to issue new cryptocurrencies, driving the price of all of them to zero. Is there some equilbrium in the middle, one that comes closer to explaining our present situation?

---

The answer is yes. Consider a scenario where there is a set of “entrepreneurs” (ie. coin creators), and entrepreneurs can expend capital to create a “signal” associated with their coin. Expending $M of capital creates a signal of strength M * R(), where R() is a random distribution with mean 1. The equilibrium is simple: a cryptocurrency with signal strength M is valued at an initial market cap of M * k, where k decreases as the total market cap of all cryptocurrencies as a portion of global wealth increases (additionally, we need k > 1 where there are no cryptocurrencies, and k < 1 where cryptocurrencies make up 100% of all global wealth).

The total market cap of all cryptocurrencies at any point in time is at the point where k is slightly above 1, so being an entrepreneur is in expectation slightly profitable. If world GDP increases, say, 3% per year, then one could imagine that existing cryptocurrencies on average increase 2% per year and every year some new cryptocurrencies appear with total initial value on average equal to 1% of the value of the existing cryptocurrencies. This is a totally long-term-stable situation; the market share of cryptocurrencies as assets remains long-run constant.

Now we can ask, what is the signaling that entrepreneurs are expending capital on? Theoretically, it could be anything. Even if each cryptocurrency developer signals by building sand pyramids in Egypt, and people want to purchase the cryptocurrency with the most impressive-looking pyramids, the model still works. However, in practice human beings want at least the pretense of not doing something completely ridiculous, and there are informational obstacles to people learning about cryptocurrencies, so the signaling activity comes in two primary forms: (i) technical development, and (ii) marketing, with marketing taking up an increasing share (including social media marketing, public billboards, as well as expenses such as paying up to $1-15 million dollar listing fees to major exchanges). In order to enter the club of cryptocurrencies that benefit from the “store of value” position, an entrepreneur need only do enough tech development and do enough marketing to build up a community to be seen as worthy.

This shows how even a free-entry market of issuance of intrinsically useless digital assets does not *necessarily* need to lead to all of the assets dropping to zero in the long run, if a separating equilibrium based on signaling expenditure emerges (and I would claim there’s a good chance that this is in part what’s happening now). **Issuing new currencies is nearly free, but issuing new currencies *that people care about* requires an increasing amount of “marketing as proof of work”**.

---

The alternative story for cryptocurrency valuation, and one that feels less spooky to friends of classical economics, is the one I describe [here](https://vitalik.ca/general/2017/10/17/moe.html): cryptocurrencies are like corporations, where their valuations represent the expected future discounted sum of coins burned from transaction fees. Currently, very few blockchains satisfy this property; although Bitcoin’s fees [have at one point reached $20 million per day](https://blockchain.info/charts/transaction-fees-usd), corresponding to a quite reasonable-looking “[P/E ratio](https://www.investopedia.com/university/peratio/peratio1.asp)” of ~30, and Ethereum has reached about [a fifth of that](https://etherscan.io/chart/transactionfee) (though fees on both chains have dropped now, to ~$200k/day for BTC and ETH), fees can only be viewed as *revenue*; the fees are paid directly to miners, which to the blockchain are *security expenditure*;  there is no *profit* left over.

In pure proof of stake, even if no coins are burned, a weaker version of the model still exists: a coin is a *tool* that you can use, with some further effort, to get a share of transaction fees; it is like a virtual mining pick. As long as the effort is less than the reward, the tool takes its share of the difference as its value.

Theoretically, a cryptocurrency world where cryptocurrencies are primarily valued as shares of future burned transaction fees, or as tools that can be used to access transaction fee revenues, is a much healthier one; putting aside outright scamming or tricking people, the only way to earn money is to build (or, by holding tokens, financially support) a blockchain that people actually use.

Given that P/E ratios less than 100 are demonstrably within reach (compare: in 2009 the S&P had a ratio of over 120), getting to this state is quite possible. And in fact, even in the current environment it should be the case that coins that get a large amount of actual usage get an advantage over coins that do not. The reason is simple: suppose that all cryptocurrencies are going up an average of 2% annually, but then one of these cryptocurrencies burns 0.5% of its coins annually from transaction fees. That cryptocurrency will go up an average of 2.5% annually, and so in a portfolio theory model it will be more attractive to hold larger quantities of it. Hence, **in the long run we do expect the best stores of value to be things that are useful for other reasons first, and stores of value second**.

That said, it is worth noting that in the current market, where cryptocurrencies rise and fall by over 10x annually, the difference between 2% and 2.5% expected annual growth is virtually impossible to see; hence, it may take some time for an equilibrium different from the current signaling equilibrium to emerge.

## Replies

**EazyC** (2018-02-14):

Great examples/illustrations as usual. I wanted to propose something I’ve been thinking about that could possibly be an interesting way to also measure coin value in addition to the above.

What if we take your argument of “a blockchain as being like a security company which keeps gold safe” example farther and contend that a blockchain is a security company which keeps gold safe and allows you to trade and speculate on its value free from traditional brokerage/middleman services. And then in addition to the blockchain “charges some percentage fee per annum that makes up its revenue and from which is derived its market cap” there is a separate network fee (a sink) for the “brokerage fee” for speculating on the gold.

This essentially becomes monetization of speculators and day traders (a monetization method that is currently how stock brokers earn their revenue).

This would be similar to Snapchat demanding a penny per transaction for movement of its stock on the NYSE (or instead of a penny, 1/100th of their own share - unfortunately shares aren’t as divisible as crypto…). Traditionally, the company which issues the security does not demand this fee, instead it is done at the broker/exchange level. However, with the advent of DEXes and smart contracts, the ledger itself essentially takes over the job of brokers and exchanges so it is not unreasonable to incorporate a broker’s monetization model in one’s conception of a blockchain’s provided value.

So perhaps one can think of a crypto asset’s future expected value as a combination of various concepts you discussed plus the idea above. Specifically, a coin’s value, V, is the sum of:

1. Expected future discounted sum of coins burned from transaction fees (in the narrow featureset of the coin)
2. Integral of all entrepreneurial signals (M * k)
3. Expected future discounted sum of coins taxed/burned from speculative activity (aka broker monetization model)

---

**ihlec** (2018-02-14):

Active and passive staking

1. Transaction fees: benefit only active-stakers
2. Buring fees: benefit also passiv-stakers

To strengthen Ethereum as a platform we want is accumulated value, as high as possible.

We want to incentivize staking of value and can do so, by rewarding all kind of token staking. (active and passive). The high entry barrier for active staking could, in a worst-case scenario, reduce the popularity of active staking to a point, where the availability reduction rate of coins cannot keep up with the expected average of 2.5% annually.

In my opinion the outstanding development effort inside Ethereum will guarantee a continuously growing adoption and protect its value. On the other hand, passive-staking (burning fee) allows everyone who holds ETH to be rewarded for his financial support. Passive stakes are also resulting in the value protection of ETH and need to be incentivized.

In the end, the gains active stakers will make, were made possible by the strong community behind ETH and therefore are a group effort, where every member of the group should be rewarded. Implementing a burning fee seems like the right thing to do.

I do support that active staking needs to be more profitable, due to higher risk, expenses and greater value for the Ethereum infrastructure, but passiv stakes are not useless and should be rewarded. Having a burning fee will strengthen the community.

This is a post-crypto-hype issue we could create early vaccines against.

---

**metabol** (2018-02-16):

One could observe that cryptocurrency is swaying torwards financial markets and is generally abandoning the original idea of replacing fiat money.

More like a modern tool for wallstreet and exchange operators to make quick money than a system of storing value.

The argument about steady price might not hold water given the fact that markets are composed of self-interested actors whose ultimate goal is to make profit.

The aforementioned profits can only be maximized in highly volatile setups like  pump and dump events.

As for the 1001 new coins created daily its pretty obvious that greed is the major factor driving a good number of them.

Government regulation might eventually be the principal force to calm the waters in the long run.

---

**clesaege** (2018-02-16):

I would disagree on passive staking. Passive stakers do not provide security to the network as the 51% attack is the 51% attack of the staked ETH. Passive stakers take advantage of the security produced by actives ones. Therefore it is fair to charge then (through inflation) in order to reward active stakers.

---

**SRALee** (2018-02-16):

The reason for this is that crypto has very little in common with fiat currency and that’s becoming more and more apparent by the day. Fiat currency has a mechanism for price stability through expansion and retraction policies (although the monetary policy is heavily centralized and set by the fed/central banks). It’s becoming very clear that the reason crypto can’t replace fiat money/cash/greenbacks is because there is no way for a crypto asset to keep its purchasing power/value stable relative to some fixed point of reference. When that isn’t possible, crypto assets look more and more like normal real-world assets than digital forms of fiat money. To put it another way, the crypto asset becomes its own asset class and less a medium of exchange. BTC rebranding as digital gold than p2p cash etc. is indicators of this trend.

---

**divraj** (2018-02-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Hence, in the long run we do expect the best stores of value to be things that are useful for other reasons first, and stores of value second.

I’d just like to add that many diverse developers with different visions & projects building on said useful protocol ( as well designed tokens allow incentives to build ) also contribute to improving , scaling & security through fundamental & tooling contributions making the protocol a better store of value than  one with a singular application of store of value

---

**Lalaland** (2018-02-18):

I think there are a lot of issues with this “store of value” argument.

In the original post, vbuterin basically argues that a “store of value” can sustainably grow if it doesn’t grow in value faster than the general economy and there is enough “belief” that the token will retain its value. vbuterin then provides an example model where the price of a coin is based on the capital investment and then shows that this model can work sustainably as it can grow slower than the general economy.

The big issue with this argument is that it is simply saying that it is possible for a “store of value” coin to retain its value in certain circumstances. A lot of things are possible, but that doesn’t necessary make them probable. For instance, it is possible that a randomly shuffled deck of cards will turn out to be sorted by suit and number. It’s just incredibly unlikely that any random shuffle will happen to be sorted.

There are a lot of other, potentially more likely possibilities for what would happen with “store of value” coins. For instance, a “store of value” coin could rapidly drop to zero for almost no reason. Or drop to 50 cents and then stay there. Etc, etc. The signaling theory is an interesting idea and is certainly “possible”, but I highly doubt it’s a good model of what’s going on.

---

**CallMeGwei** (2018-02-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> … even a free-entry market of issuance of intrinsically useless digital assets does not necessarily need to lead to all of the assets dropping to zero in the long run, if a separating equilibrium based on signalling expenditure emerges …

This sorta makes the whole space sound like those websites selling pamphlets about how to make money (selling pamphlets)…

Honestly, this signaling idea just doesn’t seem realistically sustainable to me. Where would all of this capital for endless ‘signaling’ (shilling?) ultimately come from? Even after building up an entire community of people *donating/investing* human capital - the community that spends the greater part of its collective time **marketing** is losing serious ground to their competition actually ***developing***. Spreading awareness seems like it can give a short-term boost - but long-term failure to deliver *something other than marketing* isn’t suddenly going to be a non-issue. If anything, I think signaling too far ahead of tech delivery can be net negative - the hype cycle is only so long-lived, imho.

Deliverable utility matters. Which I why I think this point is absolutely true:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Hence, in the long run we do expect the best stores of value to be things that are useful for other reasons first, and stores of value second.

Empirically, I’m not so sure that has actually been the case. Gold and Diamonds have been fine stores of value, after all. I think the difference is that people generally prefer technology with more features over technology with fewer features. Now that the store of value concept has been technologized - I expect that preference will ultimately play out in this space…

Unfortunately, I don’t have an equation for that.

---

**vbuterin** (2018-02-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/callmegwei/48/773_2.png) CallMeGwei:

> Where would all of this capital for endless ‘signaling’ (shilling?) ultimately come from?

It’ll come from the outside economy. World economy grows at 3% per year, existing cryptocurrencies grow at 2% per year, so every year an amount of resources equal to ~1% of existing cryptocurrency value can get burned on signaling, keeping the total percentage of the economy in cryptocurrencies constant.

Though note that I’m not saying this will necessarily happen; I’m just saying that something like this happening to at least part of the space is totally possible and even compatible with rational actor models.

> the community that spends the greater part of its collective time marketing is losing serious ground to their competition actually developing

As I mention lower down, that actually is true; whoever makes a blockchain that’s actually worth paying transaction fees for will ultimately have a leg up in the store of value competition. But if no one does, then it seems like the equilibrium I describe could dominate.

---

**hansz** (2018-02-18):

is it possible that in the end:

only bitcoin is valued as ‘store of value’, and other tokens used more as “medium of exchange” (e.g. ether) are valued with [MV = PT](https://vitalik.ca/general/2017/10/17/moe.html)?

I do not find it’s a bad world if above is true. Why do we need to introduce things like ‘burning’ to make ether be valued in a different way?

---

**vbuterin** (2018-02-18):

Possible. But that does not seem likely; people are increasingly realizing that there’s nothing special about bitcoin, so I think the signaling equilibrium is already asserting itself. And if other useful tokens start getting valued as shares of future burned fees, then as I describe above, that will actually make them *better* stores of value than pure stores of value, so “thing X is a store of value, and things Y[1] … Y[n] are backed by profit streams but don’t get any store of value premium” seems like an unstable situation.

Personally, I want the “expected discounted future transaction fees” scenario to win, because I think that it creates the best possible incentives for developers. The MV = PT and store of value arguments are both multi-equilibrium games, which are highly vulnerable to signaling, manipulation and other wasteful behavior.

---

**Lalaland** (2018-02-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/hansz/48/776_2.png) hansz:

> is it possible that in the end:
>
>
> only bitcoin is valued as ‘store of value’, and other tokens used more as “medium of exchange” (e.g. ether) are valued with MV = PT?
>
>
> I do not find it’s a bad world if above is true. Why do we need to introduce things like ‘burning’ to make ether be valued in a different way?

MV = PT is not really a valid and stable way to value a cryptocurrency because the velocity of money can be arbitrarily increased or decreased. The system will probably converge to people holding the coin only as long as necessary in order to complete their transaction. That would result in an almost infinite velocity of money and a corresponding almost zero value of the coin.

---

**hansz** (2018-02-18):

right, I think this is exactly the point of vitalik’ medium of exchange valuation blog. For pure medium of exchange token, with the help of highly efficient exchange, I do not see any problem of having the value of each token drop to nearly zero and still be able to do its job as “medium of exchange”.

---

**CallMeGwei** (2018-02-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> It’ll come from the outside economy.

Apologies if I’m just not keeping up - I’ll admit that my UofC econ classes are years behind me now. I’m reticent to reply (and risk exposing my ignorance), but will do so… just in case anyone else out there who stumbles on this feels a little underwhelmed or puzzled trying to follow along here.

If the entire space were filled with ‘signaling’ only, why, again, would cryptocurrencies necessarily need to grow in sync with the world economy? If a hundred years of zero development ensued - WHO, exactly, would keep shoveling capital into the ideas? It seems individuals would be disillusioned and **divesting** well before then. In such a world, I **couldn’t** “imagine that existing cryptocurrencies on average increase 2% per year” - but you imagine they *could*?

From a pure thought experiment point of view - I suppose I must cede that it COULD happen and it COULD remain in this signaling equilibrium as you propose. The pragmatist in me just doesn’t think it would actually ever pan out that way in the real world.

I guess I’m more inclined to agree with this person:

![](https://ethresear.ch/user_avatar/ethresear.ch/lalaland/48/772_2.png) Lalaland:

> There are a lot of other, potentially more likely possibilities for what would happen…

I’m missing that argument that bridges COULD happen from WOULD happen, I guess.

---

**phillip** (2018-02-19):

With potential apologies for the, um, *mixed* ⁰ notation between [Jensen](https://www.investopedia.com/terms/j/jensensmeasure.asp) and [Simons-Sullivan](https://arxiv.org/pdf/math/0701077.pdf) for α, and between CAPM and Holmström for ε,¹ here is a sketch of a view pending further empirical study,² with models and controllers - *floating* for the moment?

tl;dr: a correspondence between “store of value” and [“prestige of the institution”](https://en.wikipedia.org/wiki/The_Concept_of_Law)

[Praeton.pdf](https://ethresear.ch/uploads/default/original/1X/e39a9d3a68398d96e22fa3cad134e5218ba46f47.pdf) (375.8 KB)

δ₃: I have not made it clear enough why the above is relevant in this context. Note the three top categories by what might be crassly called engagement value. Whether this is a suitable proxy for stickiness of authority, cultural rent, metacommunitarian values, or simply speculative interest in price metadata dominating substantive “conent” on a media platform is a much longer discussion than a sassy introduction of the construct of “eye dominance” with glib reference to the network effects, and implicitly the ACID properties, of the Roman praetorian system. *See* note 2.

⁰ Strategy space language is a hell of a drug. *Va. Pharmacy Bd. v. Va. Consumer Council*, 425 U.S. 748 (1976).

¹ Perhaps resolved by reconciling Holmström and Nash for E with respect to e and ε in the proper framework. *See*, e.g., [Holmström 1999](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=162270) at “6.” *See also* [Kandel & Lazear 1992](https://doi-org/10.1086/261840) (on signaling problems in lossy analog proof of work systems).

² A found abstract may follow, contingent on coauthor permission to [SPLAT](http://www.professorbainbridge.com/professorbainbridgecom/2005/11/self-plagiarism-or-splat-a-problem.html).

---

**awaliaus** (2018-02-19):

“Hence, in the long run we do expect the best stores of value to be things that are useful for other reasons first, and stores of value second.”

If it is not useful for other reasons it cannot be a store of value.  “Crypto currency” should be replaced by “crypto assets” as this is causing misleading comparisons with fiat currencies.

Only a valuation based on quantification(PV) of future fees/utility is sustainable and would be “fundamental bottoms up analysis”.  Whether a sink is a good idea - I am not smart enough to be sure

Every other top down way of measuring value will have varying levels of directional relevance.

---

**phillip** (2018-02-19):

[Desan 2013] Money as a legal institution (h/t [@lanalana](http://twitter.com/lanalana))

**ABSTRACT** This chapter summarizes the case for considering money as a legal institution. The Western liberal tradition, represented here by John Locke’s iconic account of money, describes money as an item that emerged from barter before the state existed. Considered as an historical practice, money is instead a method of representing and moving resources within a group. It is a way of entailing or fixing material value in a standard that gains currency because of the unique cash services it provides. The evidence to that end comes from coin itself, the practice of free-minting, judicial commentary, and academic theorizing. As the second half of the chapter details, the relationships that make money work are matters of governance carried out in law. Thus law defines public debt, allocates authority to create money, and determines what counts as a ‘commodity’. Comparing medieval, early American, and modern money law on money demonstrates the dramatic importance of that legal engineering.

https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2321313

---

**awaliaus** (2018-02-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/callmegwei/48/773_2.png) CallMeGwei:

> vbuterin:
>
>
> Hence, in the long run we do expect the best stores of value to be things that are useful for other reasons first, and stores of value second.

Empirically, I’m not so sure that has actually been the case. Gold and Diamonds have been fine stores of value, after all. I think the difference is that people generally prefer technology with more features over technology with fewer features. Now that the store of value concept has been technologized - I expect that preference will ultimately play out in this space…

Unfortunately, I don’t have an equation for that.

Gold and Diamond etc started out and continue to be used for jewelry.  That was their first use.  The barter system made them good stores of value.

---

**CallMeGwei** (2018-02-20):

Sure, the jewelry use case is *something* - but that is clearly not where most of the value locked up in gold comes from. If we expect useful things to be better stores of value, gold isn’t particularly useful give its share of the “store of value” market. Today, clearly, bartering with gold is uncommon - it’s a massive store of value probably just because *it has been a store of value* for so long. I think this is what OP was talking about in the first section, right?

Time is working against anything new in this store of value model. If time and utility were the critical variables for stores of value, then dethroning gold would require massive utility multipliers. I doubt signaling (esp marketing) would be enough - that was my primary point of contention. If utility simply stagnated - what reason would there be to prefer the new stores of value over the old ones? If anything the old ones seem “safer” by virtue of their age… and safety used to be important for stores of value. I may be getting a little tangential though…

---

**awaliaus** (2018-02-20):

Not sure if this was the intent of the signaling approach but I can see how in the case of Gold the signals from the early kings/emperors/chiefs were strong in terms of resources expended to accumulate.  Over time these signals have diminished and today are close to zero.

The only time a similar signal occurs with cryptos is at launch.  Where is the 2% ongoing signal coming from


*(22 more replies not shown)*
