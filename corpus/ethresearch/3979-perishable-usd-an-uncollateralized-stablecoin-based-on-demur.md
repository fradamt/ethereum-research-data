---
source: ethresearch
topic_id: 3979
title: "Perishable USD: an uncollateralized \"stablecoin\" based on demurrage?"
author: nullchinchilla
date: "2018-10-28"
category: Economics
tags: []
url: https://ethresear.ch/t/perishable-usd-an-uncollateralized-stablecoin-based-on-demurrage/3979
views: 5774
likes: 13
posts_count: 30
---

# Perishable USD: an uncollateralized "stablecoin" based on demurrage?

(Note: this is a repost of something I’ve once posted onto r/cryptocurrency but got no useful replies. I only recently discovered ethresear.ch, so please tell me if such a post is off-topic)

It seems like stablecoins aiming to peg themselves to, say, USD essentially fall into three approaches:

1. Centralized currency board maintaining 1:1 link with fiat, like in TrueUSD or Tether. This obviously works as long as you trust the centralized party, and is the most reliable way to peg real world currencies like the HKD to the USD.
2. Collateralized debt with reserves denominated in virtual assets, like Dai
3. Algorithmic central bank, like Basis, with no concept of reserves. Basically tries to be the Fed except implemented as a smart contract.

It’s often claimed that algorithmic central banks are the most flexible since black swan crashes in asset backings do not cause issues, and they can theoretically target any exchange rate with anything, including things like baskets of goods. (Aside: I find this highly suspect. Taken to the logical extreme Basis can target a perfectly oscillating sine wave of prices so that everybody can buy low and sell high and get free money, which is obviously false. I am not really knowledgeable enough to know where exactly the argument that anything can be targeted fails though)

The main problem with algorithmic central banks seems to be that without reserves, it’s hard to defend a peg when the market price of the coin drops. When the price is higher than the peg the smart contract can simply give everybody helicopter money to drop the price, but if the price is too low there’s little that can be done. Basis claims that selling discounted bonds payable only if the peg is restored somehow fixes this, but I remain skeptical — it seems to imply Venezuela can somehow borrow its way out of hyperinflation using cleverly designed bonds, which seems absurd.

However, I wonder whether or not there’s an obviously robust solution to fixing algorithmic-central-bank stablecoins — *demurrage*, basically a negative interest rate. Imagine I make a stablecoin called PUSD, for Perishable USD, as a token with an algorithmic central bank running on an Ethereum smart contract. Like with any other algorithmic central bank, we print helicopter money if the price (based on some median of oracles) is too high.

However, every year 5% of every PUSD account balance disappears into thin air. Essentially, this means there will always be demand for *freshly printed* PUSD. Even if everybody dumps PUSD and the price tanks, eventually the dumped pile will get exponentially small, so that eventually PUSD becomes scarce and the tiny number of “survivors” still wanting to get PUSD must pay 1 USD again. This creates a market expectation that PUSD will always go back to 1 USD, which should prevent price crashes in the first place. PUSD will behave sorta like a fixed production cost perishable good like milk: milk prices won’t ever crash significantly under the cost of production.

Clearly, due to the demurrage nobody would prefer to hold PUSD rather than USD, but for applications like hedging risk in crypto-only exchanges, or having a reasonable store-of-value for people living in places like Venezuela, 5% a year might not be too big of a negative interest rate to bear. Perhaps this percentage can be made much smaller and we’d still have a stable currency.

Is there any idea like PUSD floating out there? It seems like quite an obvious way of fixing the problems with algorithmic central banks, at the cost of course of imposing this carrying cost that makes it strictly worse than fiat for people who can use fiat conveniently. Is there some “duh!” gotcha I am missing here?

## Replies

**BenMahalaD** (2018-10-29):

To answer this directly, the problem is the time until the supply drops low enough to hit demand at $1 can be arbitrarily long, so there is no guarantee that someone buying at the current price will make profit even if the price does eventually return to $1. If you buy at, say, $0.5, but it then takes 15 years to return to $1, then at 5% demurrage you’ve still lost money. The lower it goes, the longer you can hold before you lose, but the longer you will have to hold for the supply to go down enough to reach parity. I don’t see how this helps you get buyers when you need it in a panic.

Ultimately, if you have $X worth of stablecoins in existence, and there is a panic that is big enough, you need ~$X with of real dollars to maintain the peg. You can either have those dollars (1), having something that you can trade for those dollars (2), or try and get people to give you those dollars (3). (1) is uninteresting.

Of the remaining two, I think 3 is the weakest. At least with DAI, you have some assets on hand to attempt to hold the peg. I simplify don’t see how you can entice enough buyers to invest in your stablecoin in a panic. The only way to make profit is for the peg to break considerably and then return to $1, but the harder the peg breaks, the more people will want out and the more buyer’s you need. I don’t see how you can get stability with these mechanisms.

I do think these central bank style mechanisms might be useful in order to reduce volatility of a true cryptocurrency, instead of trying to maintain the peg of a stablecoin. I don’t know if anyone is building something like that though.

---

**MaverickChow** (2018-10-29):

No stablecoin can last regardless of the algorithm unless it is issued by the central bank with promise to back the stablecoin with unlimited fiat. A stablecoin issuer is just another counterparty to the market and thus has counterparty risk.

---

**nullchinchilla** (2018-10-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/benmahalad/48/76_2.png) BenMahalaD:

> The lower it goes, the longer you can hold before you lose, but the longer you will have to hold for the supply to go down enough to reach parity.

I’m not sure whether the second half of that sentence necessarily holds exactly in proportion to the first half. *Ceteris paribus* demand usually rebounds at least somewhat after a panic, meaning the supply probably does not need to go down as much for the price to go back to $1. Your argument certainly holds if, say, the demand for PUSD suddenly drops by a factor of 2 and then stays there forever though.

---

**MihailoBjelic** (2018-10-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/nullchinchilla/48/2606_2.png) nullchinchilla:

> Is there any idea like PUSD floating out there?

The idea of increasing/decreasing holders’ balances in order to stabilize the price is definitely not new. You might want to check [Hayek Money paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2425270) (published in 2014). Also, famous Albert Wenger from USV proposed the same concept in his [blog post](https://continuations.com/post/168330457810/the-quest-for-a-stable-coin) (and sparked an interesting discussion in the comments).

However, I’ve never heard someone proposing an automatic, fixed balances decrease. Interesting idea, but as [@BenMahalaD](/u/benmahalad) said, I’m not sure it’s sufficient/effective when a big price drop happens.

Also, I think the main problem with this idea is that it appears “awkward”, i.e. it requires a complete paradigm shift (users have to get used to their coins occasionally disappearing ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)). However, that might be less of a problem for institutional holders.

Hope this helped. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**BenMahalaD** (2018-10-29):

> I’m not sure whether the second half of that sentence necessarily holds exactly in proportion to the first half.

My point isn’t that the two terms are equal, I have no idea which half would win out in practice. It would probably be highly market dependent. Just that there are two forces at play here, so it’s not a given that it will always recover.

---

**nullchinchilla** (2018-10-29):

That makes sense. I still think demurrage is probably going to work better than something like Basis, though, since the mechanism to recover the peg isn’t itself going to exacerbate a panic as it’s always there (in Basis on the other hand selling those discounted bonds can easily push market sentiment down even more, leading to a death spiral).

I also do suspect that stablecoins that aren’t backed by any assets are unlikely to work in general, and even those backed by cryptoassets are fairly risky. I wouldn’t be surprised if at some fundamental level pegging to USD securely without some way of holding USD is impossible.

I’m actually working on a “low volatility true cryptocurrency” (the main idea being that the real-world cost of minting a new coin is roughly constant, dashing any speculative hopes of prices going “to the moon” since increased adoption would just mean increased currency issuance) and I believe that such systems will probably be a better – and perhaps stabler! — currency than a cryptocurrency whose value proposition rests entirely on maintaining a peg. True cryptocurrencies also don’t need any sort of centralized/gameable price feed to have much lower volatility than Bitcoin etc.

---

**nullchinchilla** (2018-10-30):

I’ve been fairly skeptical of Radix in general since their distributed ledger uses stuff like vector clocks all over the place and doesn’t actually seem to be Byzantine fault-tolerant, which I think is absolutely crucial for security and true decentralization. Their idea of a relatively stable coin is certainly interesting though; most coins out there seem to either be fixed-supply or stablecoins.

---

**MihailoBjelic** (2018-10-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/benmahalad/48/76_2.png) BenMahalaD:

> Of the remaining two, I think 3 is the weakest. At least with DAI, you have some assets on hand to attempt to hold the peg. I simplify don’t see how you can entice enough buyers to invest in your stablecoin in a panic.

I think this is critical, completely agree.

![](https://ethresear.ch/user_avatar/ethresear.ch/benmahalad/48/76_2.png) BenMahalaD:

> I do think these central bank style mechanisms might be useful in order to reduce volatility of a true cryptocurrency, instead of trying to maintain the peg of a stablecoin. I don’t know if anyone is building something like that though.

I had the exact same thought some time ago. Did a quick research, and all I found was [Saga](https://www.saga.org/currency) (scroll down to the “Price Simulator” graph). If I got it right (I only skimmed through their website), their algorithm works similar to a central bank - it defends the peg (the blue curve) but only up to a point when the available reserve in the treasury matches the minimal reserve ratio (the yellow curve).

---

**nullchinchilla** (2018-10-30):

Perhaps the lack of interest in a low-volatility cryptocurrency is because cryptocurrencies that allow speculative bubbles to form generally attract more interest? The amount of interest in a cryptocurrency is pretty much directly related to crazy-high prices and volatility — thus being low-volatility could paradoxically prevent any adoption of the currency since nobody would ever hear of it.

---

**bharathrao** (2018-10-30):

A primary issue with all “stablecoins” is that they are actually “peggedcoins”. The unstated assumption is that the USD is the ultimate metric of stability. However, we know this is only partially true because of the current economic realities where USD is the primary base currency for the forex market and the currency of choice for trading various global commodities.

The value of USD can and does fluctuate based on the strength of the US economy and the demand/supply of global commodities.

A true metric of stability would be what everyone has in nearly equal amounts and is unlikely to change with global economic shifts. This would be time. In particular, a stable metric of value can be modeled as *a single hour of unskilled labor*. Lets call it “Hour of unskilled labor credit” or *hulc*. One hour of a doctor’s time would be worth say, 300 *hulcs*.

The economics is straight-forward: if it takes you much longer to do as good a job than the *hulcs* someone charges you, then their service/good is a value.

Hulcs can be mined by someone putting in one hour of useful work on a blockchain or smart contract. Could be something that is fairly easy for humans but almost impossible for machines. (this needs some work). Another option is to have specialized work that starts at 50 hulcs and keeps getting halved like a block reward.

This currency reflects true stability rather than a peg. Note the Ithaca “hour” is similar to this idea but they had to peg it to $10 to align with minimum wage laws.

---

**nullchinchilla** (2018-10-30):

The problem with your approach is that it’s really hard to come up with a problem that is 1. roughly equally easy for humans to solve across time and space 2. infeasibly hard for computers to solve 3. easy for computers to verify. In practice hulcs in your system would have a volatile price way less than the value of an hour of unskilled labor, since there’s always the chance that an AI advance will make hulcs essentially free, and the market will price it in.

Also, in your system putting in an hour of work gives you a hulc, but there isn’t any guarantee that a hulc can hire you an hour of work, without some centralized entity (like a totalitarian state!) forcing people to work for 1 hulc/hour. So if hulcs crash there isn’t any mechanism for raising the price of hulcs.

My current project’s idea is actually sorta similar, but instead of using humans, “one hour of sequential work on the fastest CPU currenly available” gives you a coin. This can be measured in a decentralized, incentive-compatible way with VDFs.

---

**MihailoBjelic** (2018-10-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> The unstated assumption is that the USD is the ultimate metric of stability…
>
>
> The value of USD can and does fluctuate based on the strength of the US economy and the demand/supply of global commodities.

I think everyone’s more or less aware of this. Most stablecoins use USD because: 1) it’s “popular” (world’s reserve currency), 2) it’s easy to agree on its value. You can think of using USD as basically blackboxing the actual value of a stablecoin (you can easily replace it with any other value).

That said, a number of researchers around the world are working on their definition/formula of “stable value”, but this is **far from trivial**. For example, famous John Nash spent half of his life working on it (google “ideal money”). ![:slightly_smiling_face:](https://ethresear.ch/images/emoji/facebook_messenger/slightly_smiling_face.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> A true metric of stability would be what everyone has in nearly equal amounts and is unlikely to change with global economic shifts. This would be time. In particular, a stable metric of value can be modeled as a single hour of unskilled labor . Lets call it “Hour of unskilled labor credit” or hulc . One hour of a doctor’s time would be worth say, 300 hulcs .

How would this be easily determined on a global scale? ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**bharathrao** (2018-10-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/nullchinchilla/48/2606_2.png) nullchinchilla:

> roughly equally easy for humans to solve across time and space 2. infeasibly hard for computers to solve 3. easy for computers to verify.

1. and 3. are fulfilled by any NP-complete problem Some NP-complete problems are relatively easy for humans, such as graph-coloring problem or Minesweeper.

> In practice hulcs in your system would have a volatile price way less than the value of an hour of unskilled labor, since there’s always the chance that an AI advance will make hulcs essentially free, and the market will price it in.

If AI solves an np-complete problem, I think P=NP and we have bigger problems.

> without some centralized entity (like a totalitarian state!)

There are plenty of currencies that work without a centralized entity. Ithaca hours ran for decades without a centralized entity. [Anything can be money](https://en.wikipedia.org/wiki/Local_currency#List_of_local_currencies) if there is sufficient belief that it has the same value tomorrow.

> forcing people to work for 1 hulc/hour.

Nobody forces anybody since everything is negotiated locally. 1 hulc/hr is just a reference of value. Every person is free to charge a rate and anyone else is free to take it or refuse it.

> My current project’s idea is actually sorta similar,

Link?

---

**bharathrao** (2018-10-30):

> How would this be easily determined on a global scale?

Its all determined between individual interactions. One doctor may charge 300, another may charge 200. You trade off their skills and experience to your needs. Perhaps today you are poor (bear market) and take a chance with the cheaper doctor, but in Jan, you would have paid 300 for the specialist.

> far from trivial

Yes, Im getting that. Doesnt have to be ideal. Just has to have a sense of stability, ie bread costs 0.5 hulc today, it should likely cost the same 10 years from now, assuming wheat etc doesnt suffer from crop failure.

---

**nullchinchilla** (2018-10-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> and 3. are fulfilled by any NP-complete problem Some NP-complete problems are relatively easy for humans, such as graph-coloring problem or Minesweeper.

There isn’t any evidence humans can solve NP-complete problems quickly in the general case; humans simply use the same kind of heuristics as computers do, like greedy algorithms. I bet you that there is no *single* instance of Minesweeper that can be solved faster by a human than a computer with a reasonable algorithm. NP-complete problems aren’t that hard, for humans or computers, in small problem sizes.

In fact if you can show that humans can asymptotically solve a certain mathematical problem faster than computers, it would be extremely surprising, as it would probably violate the Church-Turing thesis.

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Ithaca hours ran for decades without a centralized entity

That’s because it never intended to be pegged completely to labor, but rather to 10 dollars, which was chosen only to roughly approximate an hour of labor. You can’t peg a currency to labor without *two-way* convertibility - one hour of labor guarantees you a hulc, and one hulc guarantees you one hour of labor. If nobody is willing to work for one hulc an hour, say, mowing your lawn, you must have a way to *force* them to to maintain the peg, otherwise the hulc will devalue. Otherwise known as a government, and not a particularly benevolent one.

On the other hand if hulcs were to freely trade for labor, there is no real peg mechanism anyway. In a 100 years I bet you that the price of an hour of unskilled labor would be nowhere *near* 1 hulc, and hulcs would just be another random commodity currency.

Also, the value of unskilled labor is not by any means a good way of measuring value across time, since unskilled labor might not be a particularly important factor of production, and might have an illiquid, niche market. In the Middle Ages land was far more important than unskilled labor, and markets for unskilled labor were extremely illiquid. In a few decades things like non-fungible intellectual labor or renting out robots would be the way the vast majority of people make money, and unskilled labor would again be useless.

There are all sorts of value-stable things that are easier to measure and more value-stable than labor time. Sequential CPU time on the best computing device available is probably value-stable over long periods of time: one second of facebook now is probably approximately the same value as one second of usenet 30 years ago, despite the vast disparity in raw resource consumption, since both consume roughly the same CPU time on CPUs of their era.

---

**bharathrao** (2018-10-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/nullchinchilla/48/2606_2.png) nullchinchilla:

> I bet you that there is no single instance of Minesweeper that can be solved faster by a human than a computer with a reasonable algorithm.

My understanding was that the minesweeper consistency problem is equivalent to SAT and therefore [np-complete and solving it by a machine means P=NP](https://web.archive.org/web/20121018141147/http://www.claymath.org/Popular_Lectures/Minesweeper/)

---

**nullchinchilla** (2018-10-30):

Yes, it is indeed NP-complete, but that doesn’t mean “computers can’t solve it otherwise P=NP”. That is a common misconception of what NP-complete means.

NP complete just means that “if a worst-case polynomial-time general algorithm exists for Minesweeper than P=NP”. Computers can solve specific instances just as well as humans using heuristics, NP-complete just means the difficulty goes up really fast as the size of the problem goes up — and for minesweeper there’s no evidence difficulty for humans doesn’t go up as fast. SAT solvers are in fact widely used in all sorts of software, they totally work as long as the problem size is not large.

A simple google search for “minesweeper AI” should give quite a few programs that can outperform most humans.

---

**BenMahalaD** (2018-10-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/nullchinchilla/48/2606_2.png) nullchinchilla:

> Perhaps the lack of interest in a low-volatility cryptocurrency is because cryptocurrencies that allow speculative bubbles to form generally attract more interest? The amount of interest in a cryptocurrency is pretty much directly related to crazy-high prices and volatility — thus being low-volatility could paradoxically prevent any adoption of the currency since nobody would ever hear of it.

I wonder if an opposite effect also happens. Cryptocurrencies seem to shift between high volatility and low volatility regimes (see, BTC in 2015 vs 2017 vs today). I suspect this is due to new people getting interested, and this causing a positive feedback loop that causes volatility and gets more people interested, until a bubble and crash.

This means that most people first hear about a cryptocurrency exactly when it is the worst time to buy at the height of a bubble, so their first experience is being burned, and they then leave.

I wonder if it would be possible for a cryptocurrency to get interest without causing ruinous volatility. Such that the average person could buy when they hear about it and not lose money,

This could generate interest that sustains for much longer.

---

**nullchinchilla** (2018-10-31):

An elastic supply coin like what I’m currently working on will make sure that spikes in interest don’t cause unsustainable bubbles, so the average  person won’t be buying an overvalued coin. Perhaps without bubbles most people won’t ever hear of a currency though. Every time I mention my coin project to somebody they usually express disappointment when I get to “hodling will never net you money, by design”

---

**BenMahalaD** (2018-10-31):

> Every time I mention my coin project to somebody they usually express disappointment when I get to “hodling will never net you money, by design”

You might not be talking to the right people ![:stuck_out_tongue:](https://ethresear.ch/images/emoji/facebook_messenger/stuck_out_tongue.png?v=12)

It also might be possible to reward coin holders in ways that are not purely speculative. You could redistribute transaction fees (although this does come from users, it’s a lot more ‘fair’ then a bubble), or have some other use case for the coin so they people have a value case that isn’t just selling at the top.


*(9 more replies not shown)*
