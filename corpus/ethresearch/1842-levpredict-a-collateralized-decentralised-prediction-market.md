---
source: ethresearch
topic_id: 1842
title: "LevPredict: A collateralized decentralised prediction market token model on Ethereum"
author: swapman
date: "2018-04-26"
category: Applications
tags: []
url: https://ethresear.ch/t/levpredict-a-collateralized-decentralised-prediction-market-token-model-on-ethereum/1842
views: 3131
likes: 3
posts_count: 16
---

# LevPredict: A collateralized decentralised prediction market token model on Ethereum

This post outlines LevPredict, a model that represents a collateralized approach to facilitating a parimutuel betting market for binary (and multi category) real-world event outcomes. It focuses on financial engineering aspects of market structure and smart contract UX design.

This is not an ICO or project seeking funding it is just an outline anyone can follow. The model does not require any special token, but it does posit a Smart Contract that creates its own ERC20 tokens to serve as vehicles for the outcome values. See the latest version of the paper in PDF here: http://leverj.io/levpredict.pdf

LevPredict requires a trusted event outcome determination, so a trustless resolution mechanism is beyond the scope of this paper. As a result, this is not at truly trustless prediction market model because the trigger to payout to winners is centrally determined.

To our knowledge this style of parimutuel betting facility model has not been applied to Ethereum (or any other crypto blockchain) for decentralised prediction market tokens. Technically the LevPredict model would apply to any Smart Contract capable blockchains not just Ethereum.

**Background**

The most efficient facilitation of price discovery in prediction markets is to allow free trading of a raw asset representing the probability of a certain event. You can wrap up risk exposure into all kinds of exotic products: options, futures, insurance products, etc., but these are all just middlemen repackaging the price of risk.

If you use X ETH at price δ to buy Y=X/δ  tokens to take a position on an outcome of interest, you should have the flexibility to sell or buy more of the exposure just like any other asset, fully collateralized. As the price oscillates up to the event resolution date, the market absorbs the information in the world to reveal determinants of the outcomes. Just like stock shares and ICO assets are traded openly on the market, so too is there a market price δ reflecting the some probability of the outcome of an event. As long as there are sellers available to pay the buyers (and vice versa), then a market is made.

This model uses a Smart Contract implementation that uses ETH as the collateral and creates ERC20 token assets that take on a market value representing the effective probability between outcomes of a binary event. This paper focuses on binary events, but the model can trivially be expanded to multi-category events (and this is suggested to handle tail event outcomes).

In contrast to a futures model approach, there is no margining or risk management required as the mechanism is fully collateralized. And unlike a bookie, the Smart Contract won’t go bankrupt, because it holds the ETH put into the system and pays directly to one outcome.

Throughout this post I’ll be illustrating by example using, the event of the 2016 United States election had two outcomes: Trump or Not Trump (effectively Hillary). These outcomes are represented by two ERC20 tokens TUP and NUP.

[![Selection_999(665)](https://ethresear.ch/uploads/default/original/2X/b/b9dd9f296697cbe481b71b6be032133db07470a8.png)Selection_999(665)617×287 36.1 KB](https://ethresear.ch/uploads/default/b9dd9f296697cbe481b71b6be032133db07470a8)

**Figure 1:** How event is birthed and matures

**Smart Contract Specs**

Primarily you have to specify the resolution date, the number of outcomes (tokens), the ETH price of the token pairs (or groups for n>2), and the mechanism to resolve which triggers the payout to winning outcome (this is a big decision, the trigger is in the contract, but someone/something has to pull it). Decimals should be 1 to avoid dust payouts.

People send ETH to the Contract, receive ERC20 tokens representing different event outcomes, and if people send the tokens back (in proportion) to the Contract, it sends ETH back. Then at resolution date an outcome is chosen as winner. The token holders of the winning outcome then get sent back to the Contract, which disburses the ETH pro rata.

Let’s say you create: LevPredict Trump-2016 Event Contract which goes through three periods:

- t0=contract creation, months ahead ideally to get market in price discovery mode early
- t1=outcome category tokens generating and being redeemed and trading on secondary market in period (TUP and NUP)
- t2=resolution date (in blockheight), e.g, January 20. 2017 (Inauguration)
Supply creation mechanism

When you send ETH to the contract, the contract issues two ERC20 tokens back to you:

- TUP: Trump United States President 16
- NUP: No Trump United States President 16

So given rate r (in ETH) for token creation, the Contract has received at any given time a net total of Y ETH:

TUP supply Q_TUP=Y/r

NUP supply Q_NUP=Y/r

TUP and NUP supply are always equal. In our example we take r=1.

[![Selection_999(666)](https://ethresear.ch/uploads/default/original/2X/e/e012a86a1fdd3647cd58500fc14f30483b044e87.png)Selection_999(666)623×218 23.3 KB](https://ethresear.ch/uploads/default/e012a86a1fdd3647cd58500fc14f30483b044e87)

**Figure 2**: Separation of assets in Smart Contract from the secondary market for TUP & NUP

**Convertibility window for arbitrage**

Since 1 ETH in results in 1 TUP and 1 NUP, the Contract also will return 1 ETH in exchange for 1 TUP and 1 NUP sent together. This forces the market to trade rationally since people could arbitrage any deviation from the sum of the market value of the two tokens by sending ETH to create new tokens and sell down the market.

[![Selection_999(667)](https://ethresear.ch/uploads/default/original/2X/1/1e5b38fda1ce8b120351f97df0044606fedd0e01.png)Selection_999(667)485×232 10.1 KB](https://ethresear.ch/uploads/default/1e5b38fda1ce8b120351f97df0044606fedd0e01)

**Figure 3**: Smart contract as a convertibility window at fixed rate TUP and NUP for ETH.

*Low  prices*

Take the case of TUP trading at 0.40 ETH and NUP trading at 0.50 ETH.

One could buy TUP and NUP together for 0.90 and redeem from the smart contract at face value to earn 1.0 ETH.

*High prices*

Take the case now of TUP trading at 0.55 ETH and NUP trading at 0.54 ETH.

One could send 1 ETH to the Contract, create 1 TUP and 1 NUP, and sell for 1.09, earning 0.09 ETH arbitrage per token.

This keeps the system fundamentally in balance with respect to ETH flows and token pricing on the market.

**Pre-Settlement Market Expectations**

Since NUP and TUP are ERC20 tokens, they can be traded anywhere: on DEXes or centralised markets that accept Ethereum assets. They rationally should trade between: (0, r] ETH since nobody would buy TUP or NUP for more than the price r that you can get from the Contract.

At price r=1, the market value takes on a reflection of the decimal probability of the outcome occurring. With enough economic/insurable risk/speculation interest associated with the event then it will attract liquidity.

Market participants who did not generate their own tokens may enter the secondary market and speculate and participate in the token market as a prediction market. One can continuously receive market signals of the token value indicating the outcome risk of occurring.

As the world moves closer in time to the event from the present time, the value of the tokens will gravitate toward the true probability at any given time of the event having a particular outcome. The smart contract will programmatically disburse to the winning outcome so there is cryptographic certainty (to the extent the resolution mechanism is trustless) that no matter what price you pay to obtain TUP or NUP, you will receive the face value of 1 ETH if the outcome occurs. This solidifies the credibility of the value of the tokens and reduces uncertainty on the valutaion.

**Settlement**

Upon resolution date **t2:**:

- Smart contract will pay out (or be redeemable for) all ETH to TUP holders if Trump is United States president on Jan 20, 2017, nothing if not.
- Smart contract will pay out (or be redeemable for) all ETH to NUP will if Trump is NOT United States president on Jan 20, 2017, nothing if he is.

In general when determining outcomes, assume only one or the other can happen (i.e., mutually exclusive), and that there is no ambiguity in event outcome. Design of the event is outside of the scope of this paper, but for simplicity, could focus only on events that are very popular among the global bookmakers such that it is relatively easy to determine consensus of outcome.

This creates a market where people use ETH and ERC20 assets to make unlevered bets on binary event outcomes. The contract can be coded open ended such that a group of trusted parties gather to verify the event outcome after it has occurred.

Once the resolution is verified in the Contract, holders of the winning event get full payout and NUP gets nothing. Any further ETH sent to the Contract is rejected.

Upon settlement block being reached, Contract has Y_end ETH that is distributed pro rata to all TUP holders at price of TUP/ETH = 1 (either via redemption or snapshot airdrop).

Payout can be done in many ways but two main approaches would be suggested:

1. The winning token is chosen in the Smart Contract, and users must send their tokens back to the Smart
Contract to redeem their ETH.
2. A “snapshot” is taken at the resolution date, at which time the Smart Contract disburses the ETH to all account holders at the specific block.

The first model is preferable because it is more practical in making the user pay for the gas, and then the LevPredict contract is more of a utility people choose to interact with to generate tokens and disburse.

Throughout the period, many ETH may have gone in (when people create TUP and NUP) and out (when people destroy TUP and NUP), but Y_end remains at t2 as no further generation would be allowed. In the second model, Y_end goes out of the contract to distribute to TUP. Gas could be user paid or pre-funded through a pool “rake”.

**User journey for betting on outcome**

*Inception Route*

The way a user would make a simple bet on Trump winning would be to send ETH to the Contract, receive 1 TUP and 1 NUP, and sell their NUP tokens to other people who believe Hillary will win. Those who believe Hillary will win will provide the Supply sell pressure on TUP market.

For example say TUP is trading at P_TUP= 0.40 and P_NUP is trading at 0.60 on different exchanges like Leverj, IDEX, Binance, and EtherDelta.

User starts with 1 ETH.

User sends 1 ETH to get 1 TUP and 1 NUP. You sell your 1 NUP for 0.60 ETH, and you use your 0.60 ETH to buy 1.5 TUP (0.6/P_TUP).

After election day the “good news” comes that Trump won. Even though the resolution date is months away,

If the user chooses to hold until settlement, then the contract pays out at the resolution date block where a “snapshot” of sorts is taken to see what addresses are holding TUP and NUP in a given block.

The contract then sends 1.5 ETH in proportion to the 1.5 TUP tokens held in the user’s Ethereum address.

User makes 0.5 ETH on the bet.

*Purely Secondary Market Trader*

Another user maybe has a lot of ETH and just wants to make a bet on Trump winning. He would not interact with the smart contract, but would just go to an exchange that trades ERC20 tokens and buy what he considers to be a fair price for a return in case Trump wins.

Say market is trading at the above prices, P_TUP=0.40.

User sends 1 ETH to bet on Trump at this price. It buys 2.5 TUP

(which pay out 2.5 ETH if Trump wins).

An effort would need to be made to avoid people scamming so that the TUP and NUP tokens can’t be sent around and duping people into thinking there is value even after the settlement payout has occurred.

**Decentralised exchange trading of LevPredict**

It bears repeating that LevPredict tokens are fully collateralized. The model poses no system risk to exchanges that list, for example, TUP/ETH and NUP/ETH pairs. They would be free to list them for trading and just earn execution fees in ETH with no exposure to the underlying volatility.

Additionally, because they are ERC20 tokens they could be trustlessly handled in your favourite trustless exchange or protocol. It is truly decentralised in that anybody can create the tokens if they send ETH to the Smart Contract and trade it wherever they want.

**Beyond Binary: Multiple Categories**

This is a bit trickier in terms of event design, if there is surely only 3 types of outcomes it can be a functioning market, but if there is ambiguity it can be hard to facilitate a liquid market.

However, in financial engineering terms, one can easily create n > 2 categories with the same convertibility window and settlement to single outcome. Multiple tokens would make it a bit more difficult to arbitrage. The smart contract would require all three, or all n tokens to be submitted to redeem equal amount in ETH (in time t1).

**Issues**

*Liquidity issues*

Although the Contract convertibility window does provide arbitrage for summed values deviating, there is no easy way for marketmakers to manage exposure on prediction market outcomes. In my years working with crypto exchanges the number one issue after proper tech is having liquidity. For financial assets with a liquid spot market, market makers can create short and long position adjustments in response to trading activity.

This exposure is more difficult in prediction markets. As a result, liquidity would be an ongoing issue. There is , however, for many events, a global bookmaking market where casinos are offering odds on events, which one could view as a financial asset with a payoff that can adjust exposure.

If this is not obvious at first, think about it in purely mathematical terms: say you want to bet at a bookie 1 ETH that Trump wins, he offers you odds payout of 2.4x. You would earn 2.4 ETH from it if Trump wins and end up with 3.4 ETH.

This is identical to buying 3.4 TUP at TUP/ETH = 0.30 for 1 ETH. This is the market value of gaining exposure to the possibility of this event.

If the event has widespread appeal, then quants can provide liquidity and exploit differentials between different bookmaking markets around the world.  LevPredict tokens would be the freest and most secure market for an event because you are guaranteed to have bookie solvency in the Smart Contract.

*Event Definition*

When defining a particular event, care must be taken to ensure mutual exclusivity. For most practical applications (politics, sports events with clear rules) there is reasonable certainty and minimal ambiguity regarding resolution.

*Anomalous / Unaccounted Outcomes*

In practice events can be shocking and not result in any of the predicted outcomes. There is no obvious way to refund token holders because they would be traded around and switching hands so much where people took different exposure. Thus, it is not clear how it would disburse fairly. A 50/50 split would benefit speculators of the cheaper outcome on the market. Potentially could disburse to all those who have overlap of TUP and NUP for ETH, and then split the rest to the people.

Cheekier way would be to create a third token, lets call it 00P, which would be issued in addition to NUP and TUP,. and be paid out fully in anomalous unaccounted outcomes. We treat it as “00” in Roulette.

## Replies

**MicahZoltu** (2018-04-27):

I recommend checking out Augur.  If I’m reading this right, it is exactly the trading system Augur has implemented, though Augur also sizes too solve the problem of trustees reporting (which is what most of the Augur white paper is about).

---

**swapman** (2018-04-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> If I’m reading this right, it is exactly the trading system Augur has implemented

No, but like all prediction market models there are similarities. In this case, it is only similar to the Augur concept mentions “trading event shares” (something Augur did not pioneer at all by the way, Intrade and others have used this model for years before).  On their whitepaper page 2 section B you can see how they describe it: http://www.augur.net/whitepaper.pdf

> consider a market that has two possible outcomes, A and B. Alice is willing to pay 0.7 ETH for a share of A and Bob is willing to pay 0.3 ETH for a share of B. 5 First, Augur matches these orders and collects a total of 1 ETH from Alice and Bob.6 Then Augur creates a complete set of shares, giving Alice the share of A and Bob the share of B. This is how shares of outcomes come into existence

Notice the unnecessary lengths of matching and platformising when the contract could just create the outcomes and automatically disburse and let the market manifest freely in ERC20 assets anywhere.

They continue on page 3:

> The Augur trading contracts maintain an order book for every market created on the platform. Anybody can create a new order or fill an existing order at any time

This is where things go off the rails. Order matching and marketmaking on chain is a mess, and theres no reason to go that far. With LevPredict you just create the outcome assets, establish a direct collateralised settlement mechanism, and then leave the asset trading to the dozens of protocols and exchanges that are out there handling ERC20 tokens.

So at the current point Augur implementation reveals no such specifics outlining the system in a purely decentralised share as representing in an ERC20 token (which is described in detail in OP). I also am not convinced they have solved trustless out resolution with REP. IMO they overengineer the problem trying to be a “platform” when the system is pretty easy to set up fully decentralised, with the only (but very important) issue remaining being how to resolve outcome in a proper way.

---

**MicahZoltu** (2018-04-27):

Fundamentally, Augur’s trading system and LevPredict both (if I understand LevPredict correctly) provide the same system for creating complete sets (1 share of every outcome) and then allowing trading of each of the shares as ERC20 tokens.  The reason Augur does the complex matching stuff is because of a desire to limit capital requirements to value at risk.  This means that if a user has 1 ETH and wants to bet it all on Trump winning the election and another user has 1 ETH and wants to bet it all on Trump losing the election and the current market price is 0.5 ETH, then we want to enable matching of these two parties *without* either of them first needing to put up 2 ETH to buy a complete set and then sell one of the shares to the other party.  You are correct that if you drop this requirement, the trading system gets significantly easier.

Augur went with on-chain trading first because it is “easier” for an MVP when you want to minimize capital requirements to value at risk.  If that isn’t a requirement then the whole system can be written in one smart contract pretty easily.  There is certainly merit to just letting market makers solve the problem of providing capital.  The Forecast Foundation (team building Augur) plans to move to off-chain trading in the future, but it is non-trivial (though it is possible) when you want to minimize capital requirements to value at risk.

Also note that Augur is a pure superset of LevPredict.  With Augur you can buy a complete set yourself without finding a counter party, as you have described in LevPredict (again, if I understand correctly).  Once you do this, you will have two ERC20 tokens that you can then freely trade on any exchange platform such as a 0x exchange, centralized exchange, EtherDelta, etc.  So I would argue that Augur has already implemented what you have described, they just have a bunch of *other* stuff on top of it like minimizing capital requirements to value at risk, on-chain order books, a default UI, and a trustless oracle.

![](https://ethresear.ch/user_avatar/ethresear.ch/swapman/48/1243_2.png) swapman:

> with the only (but very important) issue remaining being how to resolve outcome in a proper way.

This is by far (many orders of magnitude) the hardest problem in the prediction market space.  I have argued many times in the past that if you are willing to accept a centralized oracle, building a prediction market is actually pretty easy.  While I do believe there may be value in a prediction market that doesn’t have a trustless oracle, that is the opposite of Augur’s goals which is specifically to build a trustless oracle.  The prediction market part of Augur is more-or-less a first-use-case for the trustless oracle platform, because the prediction market part is effectively the “easy” part it made sense at the time to tack it on to the oracle as a proof of usefulness of sorts.

---

**swapman** (2018-04-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Fundamentally, Augur’s trading system and LevPredict both (if I understand LevPredict correctly) provide the same system for creating complete sets (1 share of every outcome) and then allowing trading of each of the shares as ERC20 tokens

Generally yes you create complete set, but you lose me when you say…

> The reason Augur does the complex matching stuff is because of a desire to limit capital requirements to value at risk.

Why is there even a discussion of capital requirements when the representation of the value should be fully collateralised as I outline in the convertability window section of OP. Theres no “risk” in the sense of one leg not being able to pay the other leg. It’s a pure parimutuel model with no system risk possible under any circumstances.

> Augur went with on-chain trading first because it is “easier” for an MVP when you want to minimize capital requirements to value at risk. If that isn’t a requirement then the whole system can be written in one smart contract pretty easily.

I tihnk what you are alluding to here is what I address in LIquidity Issues section. The obstacle, once the fully collateralised outcome tokens are created, is to make sure theres a healthy market of buyers and sellers for the different outcomes so that traders who create the tokens have a market to take their preferred position.

That’s the beauty of LevPredict though: it is simple, one smart contract, that will let outcomes be purely decentralised.

> Once you do this, you will have two ERC20 tokens that you can then freely trade on any exchange platform such as a 0x exchange, centralized exchange, EtherDelta, etc

I have not seen it presented as shares in ERC20 tokens outside of the Augur “platform”. If it goes live in that form I guess we will see, but this is not described in white paper or revealed in the beta as far as I have seen. They got so focused on trying to create utility for REP and solving the unsolvable trustless oracle issue that they did not bother to make the simple fully decentralised implementation that LevPredict outlines clearly.

> So I would argue that Augur has already implemented what you have described, they just have a bunch of other stuff on top of it like minimizing capital requirements to value at risk, on-chain order books, a default UI, and a trustless oracle.

I have not seen it implemented and would argue they missed the bigger picture by trying to create a trustless oracle (which is also yet to be seen as working really trustlessly) and missed out on a very elegant simple fully decentralised model that could have been done instead of delaying year after year a platform release that overpromised on the model. Why is a UI needed in a fully decentralised Smart Contract system? Send ETH, receive outcome tokens, trade the tokens WHEREVER you want. Why are we talking about all these unnecessary bells and whistles when the system does not even solve the problem they set out to do: truly trustless event resoltuion.

> This is by far (many orders of magnitude) the hardest problem in the prediction market space

Agree 100%! I spend years trying to solve it, and supported Augur and other projects, until I realised none of them solve the issue. So it is better to focus on creating robust markets and the financial engineering structure to have the assets created and traded ANYWHERE.

If the resolution is gonna be trusted anyway, may as well just make a simple trigger in the Smart Contract to pick the winner and allow redemptions.

---

**MicahZoltu** (2018-04-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/swapman/48/1243_2.png) swapman:

> Why is there even a discussion of capital requirements when the representation of the value should be fully collateralised as I outline in the convertability window section of OP.

Value at Risk is a term of art in finance/investing that means the amount of capital that is at risk in any given position.  It is also sometimes called Worst Case Loss, which means the amount of capital that I can possibly lose in the worst case scenario.  In the example I gave (market price 0.5 ETH for Trump winning presidency) the most that someone holding this position can lose is 0.5 ETH, which means their VAR or WCL is 0.5 ETH.  The goal with Augur’s trading system is to make it so someone who wants to enter into such a position can do so with *only* 0.5  ETH of available capital.  They do not need to first acquire 1 ETH of capital to buy a complete set and then sell one of the shares for 0.5 ETH just so they can obtain their 0.5 ETH VAR position.  As I mentioned, if you are willing to accept that liquidity providers/market makers are a *required* part of the platform this can all go away.

![](https://ethresear.ch/user_avatar/ethresear.ch/swapman/48/1243_2.png) swapman:

> I have not seen it presented as shares in ERC20 tokens outside of the Augur “platform”.

I can assure you, shares are just ERC20 tokens, you can see that here: [augur-core/source/contracts/trading/ShareToken.sol at master · AugurProject/augur-core · GitHub](https://github.com/AugurProject/augur-core/blob/master/source/contracts/trading/ShareToken.sol)

While the built-in UI doesn’t expose shares as tokens anywhere I don’t believe, under the hood they are which means you can view them in any wallet that supports ERC20 tokens and you can trade them on any exchange that supports arbitrary ERC20 tokens.  At the moment the “name” and “symbol” of the share are super generic though, so you’ll want an exchange that supports custom labeling of tokens being traded.

![](https://ethresear.ch/user_avatar/ethresear.ch/swapman/48/1243_2.png) swapman:

> They got so focused on trying to create utility for REP and solving the unsolvable trustless oracle issue

I think you misunderstand the goals of Augur.  This is the *primary* goal of Augur, the prediction market is a secondary goal that was an easy add-on and proof of usefulness to the primary goal.

![](https://ethresear.ch/user_avatar/ethresear.ch/swapman/48/1243_2.png) swapman:

> they did not bother to make the simple fully decentralised implementation that LevPredict outlines clearly.

As mentioned above, their trading system is a full superset of LevPredict I believe.  With Augur you can do the following:

1. Create a market. (this defines the description, end date, outcome labels, reporting source, etc.)
2. Escrow ETH to create one or more complete sets. (this will give you one or more shares of each outcome)
3. Trade the ERC20 tokens wherever you want (on chain, off-chain, etc.)
4. If you end up with one of each outcome (a complete set), you can trade that back to the market in exchange for the escrowed ETH.
5. Once the market resolves, winning shares can be redeemed with the market for the ETH escrowed.

If I understand LevPredict correctly, this is exactly what it proposes.  Augur has a bunch of other stuff like fallbacks for when the reporting source lies, since the oracle is its primary goal, but the trading system at its core is an implementation of what LevPredict proposes.

![](https://ethresear.ch/user_avatar/ethresear.ch/swapman/48/1243_2.png) swapman:

> the system does not even solve the problem they set out to do: truly trustless event resoltuion.

I would love to hear your arguments as to why Augur fails to solve this problem within the bounds described by the paper.  However, that is unrelated to the current discussion of whether or not Augur has already implemented a superset of the design described by LevPredict.

---

I’m willing to make the relatively bold claim that I could build the LevPredict contracts in under a week, maybe even a weekend if I ignored testing and deployment infrastructure.  The problem is that smart contracts alone are not particularly useful.  In order for a product to succeed you need to provide a full solution, not just a component of a solution.  This means you need a UI, at the least, for interacting with the system and you need to solve the problem of oracle trust.  Even if you go with a trusted oracle, you need to then have an actual trusted oracle (e.g., an actor that people believe will be honest in the future when given the opportunity to rob everyone).  You also need to solve the problem of the oracle being attacked by a state actor (e.g., the US went after InTrade despite InTrade operating out of EU).

Fun side fact: I built a smart wallet some time ago that has a mechanism for recovery built-in that allows for securing assets in a hot wallet without having to worry about losing access to physical backup keys.  No one but me uses it because it doesn’t have a UI (I have to interface with it manually using Parity/MEW).

Augur attempts to build a full solution, which is why it is so much more complex than LevPredict alone.  Gnosis was going to go with the “trusted oracle” prediction market but they have since pivoted.  I believe the issue they foresaw was that creating liquidity for an unbounded number of tokens was going to be really hard, which is why they pivoted to building a new type of exchange first, so they could put their unbounded number of otherwise illiquid tokens on that exchange without needing to figure out how to create a useful amount of liquidity for *every* market.

---

**swapman** (2018-04-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Value at Risk is a term of art in finance/investing that means the amount of capital that is at risk in any given position…
> …The goal with Augur’s trading system is to make it so someone who wants to enter into such a position can do so with only 0.5  ETH of available capital.

Ah, sure. I come from the derivatives world where we have to deal with margining and marking of position values to determine collateral suitability, and risk management systems for liquidating and handling system imbalances. So “capital requirement” is used as a initial or maintenance margin for handling PnL harmoney.

Re: minimal capital requirement, LevPredict achieves the same in a slightly diferent way: just by letting you send 0.5 ETH to create both (or all) outcomes and then trading them on any markets to allocate your preferred risk exposure.  Also by altering the token price you can do it quite granularly.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I can assure you, shares are just ERC20 tokens

Cool, it is quite “under the hood” as you say. This means there might be hope for it being properly decentralised without other requirements (like being forced into Augurs platform), as long as the settlement mechanism should be as simple as sending the ERC20 tokens to Contract if you have the winning outcome, and redeeming face value ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) (or snapshop+airdrop approach)

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> This is the primary goal of Augur, the prediction market is a secondary goal that was an easy add-on and proof of usefulness to the primary goal.

Fair enough. We can save the discussion about trustless oracle viability and whether REP model truly achieves this for a different thread because this post was presented with that being outside the scope.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I’m willing to make the relatively bold claim that I could build the LevPredict contracts in under a week, maybe even a weekend if I ignored testing and deployment infrastructure

Excellent! Please do. I think it is crazy this does not exist as it is simple and elegant and allows others to then focus on how the trigger is selected in a trustless way (just plug that event resolution mechanism into the trigger of the LevPredict Contract).

We had the same thought, that we would sit down and bang the simple code out in a hackathon. Currently at Leverj we are focused on a plasma flavour for hybrid DEX for ERC20 spot and for ETH margined futures, so our priorities are just elsewhere. However, with proper implementation, LevPredict prediction market tokens are easily implemented as any other spot ERC20 asset in an exchange so eventually envision a “Prediction” section for the exchange dedicated to ERC20s launched with popular event outcomes.

Nevertheless, we hope the OP serves as a sufficient outline of how this component would work if someone else wants to push it out!

---

**MicahZoltu** (2018-04-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/swapman/48/1243_2.png) swapman:

> Excellent! Please do. I think it is crazy this does not exist as it is simple and elegant and allows others to then focus on how the trigger is selected in a trustless way (just plug that event resolution mechanism into the trigger of the LevPredict Contract).

The reason I haven’t done this, and I suspect no one else has done this, is because there is no money in doing it.  So I could spend a week of my time (which is very valuable to me) building something that will not (IMO) do more than prove a point on the internet.  I have *also* considered building a full product, but that is 6-12 months of work which means it competes actively with other opportunities I have.

---

**swapman** (2018-04-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> The reason I haven’t done this, and I suspect no one else has done this, is because there is no money in doing it.  So I could spend a week of my time (which is very valuable to me) building something that will not (IMO) do more than prove a point on the internet

It does more than prove a point on the internet, it creates a clear and truly decentralised direct model for prediction market that nobody has clearly specified (and to emphasize: it is definitely not in the Augur whitepaper). LevPredict works 100% as outlined and just requires a trusted trigger to determine outcome and does not require anyone’s special platforms to interact with, just Ethereum. How that trigger ends up getting tripped is up to others who can make it as trusted or trustless as they want. The component model of LevPredict is ironclad as a system and by forcing user to pay gas to create the outcome tokens and redeem, it is simple and robust the way decentralised apps should be.

Although I think you are getting to a good point: LevPredict as a model does not require anyone’s ICO token in order to use, it is purely on Ethereum, and purely independent of anyones pet projects. So maybe thats why nobody has specified or coded this even though you and I both know it shouldnt take more than a week to produce. That’s why we lay this model out to the community to build without the perverse incentive of jamming an ICO token use case into prediction markets.

---

**vbuterin** (2018-04-27):

> An effort would need to be made to avoid people scamming so that the TUP and NUP tokens can’t be sent around and duping people into thinking there is value even after the settlement payout has occurred.

I would say make it simpler: when Trump wins, allow TUP tokens to be *exchanged* for ETH at 1:1. This way the TUP token balances would get cleaned out and there’s no risk of tricking people by offering them outdated TUP tokens.

---

**bharathrao** (2018-04-27):

Augur was certainly groundbreaking in its time.

I see the following differences:

**Creation**

Augur: Creator posts validity, noshow gas and noshow REP bonds to create a market. The bonds exist to insure that the participants are not stuck with useless tokens after event resolution. This imposes a financial limit on how many simultaneous bets can run concurrently.

LevPredict: No need to post bonds since the smart contract can convert tokens back into ETH. This allows for automated creation of contracts from sports/tournament schedules.

**Participation**

Augur: Platform matches two outcomes (Buy A at 0.7 and buy B for 0.3) and creates tokens. This means that two participants need to come together at specific prices to participate. Its quite unclear how this would work when there are 15 outcomes (say Presidential primary). There is good chance 90% of the participants only want to bet on the top 3 candidates. But unless there are buyers for the remainder, there is no match. The net result is low liquidity because outcome share generation is cumbersome.

LevPredict: A single participant can simply send eth and is ready to participate. There is no liquidity penalty for larger outcome sets. Result is high liquidity

**Trading**

Augur: Trading on augur platform. Platform needs to cancel unfilled and partially filled orders.

LevPredict: Trading is free on existing token exchange platforms.

**Resolution**

Augur: Designated reporter. On failure public reports with staked bonds, Dispute round, fork. Extensive work on trustless resolution.

LevPredict: Designated reporter only.

**Invalid Outcome**

Augur: Proportional refund

LevPredict: Invalid is an outcome like 00 in roulette

**Fees**

Augur: Creation, Trading?, Settlement

LevPredict: None

---

**bharathrao** (2018-04-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> when Trump wins, allow TUP tokens to be exchanged for ETH at 1:1.

Makes sense. Only the TUP token be exchanged for ETH. The NUP tokens can be destroyed to save storage space.

---

**swapman** (2018-04-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I would say make it simpler: when Trump wins, allow TUP tokens to be exchanged for ETH at 1:1.

Bingo. This is how it would work in the Payment option #2 (snapshot+airdrop), what you describe it the Payment #1 where the TUP have to be sent to the Contract, with gas to pay for the ETH being redeemed. (Actually [@bharathrao](/u/bharathrao) suggested this in the paper)

This option in the model dominates the snapshot+airdrop model for that reason

---

**MicahZoltu** (2018-04-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Creation

There is no limit on how many simultaneous bets can be run concurrently.  Perhaps what you mean is that there is more capital lockup required to create new markets, thus one can imagine that there will be fewer markets than LevPredict?

I would personally argue that the benefits of guaranteeing that markets eventually resolve is well worth the increased capital lockup requirements for creating new markets.  Personally, I would rather have fewer markets that are guaranteed to finalize than more markets where some may never finalize.

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Participation

The mechanism you described for LevPredict exists in Augur, so that isn’t a LevPredict advantage.  As for the issue of how do you deal with many-outcome markets, the answer is allowing short positions.  A user can go short on Trump, which under the hood means “own one of every share *except* Trump”.  When presented to the user they see, “Short on Trump”.  This means that the top 3 of the 8 (Augur MVP has a limit of 8 outcomes per market) possible candidates will just be pairs of people “long on candidate” and people “short on candidate”.  Arbitrageurs can make a little money moving individual shares around if things ever get weird.

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Trading

Similar to what I mentioned above, Augur supports trading shares as ERC20 tokens, which means on any exchange you want (on or off chain).  The default UI is on-chain trading, but since LevPredict has no UI it doesn’t seem fair to count that against Augur.  ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Invalid Outcome

To be clear, Augur’s refund is just “everyone splits the pot evenly”, meaning in a two-outcome market, each share gets half of a share’s worth of winnings.

---

**swapman** (2018-04-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> To be clear, Augur’s refund is just “everyone splits the pot evenly”, meaning in a two-outcome market, each share gets half of a share’s worth of winnings.

Yea this is really not an elegant solution. This obviously wildly benefits those who bet on low-odds outcomes and suddenly get an even split payout with the other outcomes. But this comes back to the importance of event design.

In LevPredict, as mentioned in the end of post, there is just no direct equitable way to disburse since the outcome tokens change hands and people pull money out of the system and you cant roll that back. So ultimately what makes most sense to either use a wildcard / 00 token to represent no resolution (and its intended that event design should cover outcomes sufficiently enough that the odds of no resolution are truly order of magnitude of 00), or to allow people to submit TUP + NUP to redeem the base cost (if they have it) and then begrudgingly disburse evently between outcome tokne holders.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> since LevPredict has no UI it doesn’t seem fair to count that against Augur

Here’s the UI if you need inspiration:

**LevPredict Contract Creation**

Enter resolution description:

Describe the outcome tokens:

Enter resolution date:

Specify an Ethereum address that the Contract accepts as only whitelist to call the resolution command

[ Send TX ] with gas to get on network

**LevPredict Contract Participation**

To participant in the event, please send ETH to LevPredict contract address: 0xfoobar

The addresses for the outcome tokens to add to your wallet are: 0xOutcome1, 0xOutcome2

Add these tokens to your wallet and send them like any ERC20 token

The end.

As for the convertibility window of the token outcomes back to ETH, the user could just send 100 TUP in one tx, and 100 NUP in another, and the contract will know they have matched amount and then send ETH back. So, UI can just instruct this.

The real UI issue comes with making the ERC20 tokens userfriendly and tradeable in a nice fast trustless environment. And actually, that’s what Leverj is focused on, which is why we don’t have time to bang this out right now. But it seems natural that once our ERC20 spot and ETH futures platform is done, that we add some Prediction market section dedicated to trading ERC20 tokens that represent popular outcomes. Maybe even Augur ERC20 event shares would be suitable but we would have to see what you end up doing for the redemption since it is not specified in whitepaper and not clear from the code even.

---

**MicahZoltu** (2018-04-28):

I like the idea of invalid being its own outcome.  In Augur it has some effects on scalar markets depending how they are implemented and it means that short on YES is now different from long on NO in a binary market.  Both of these result in some UX complexities that would need to be solved for a full solution.

If you are curious about Augur or integrating with it, I recommend popping into the Augur Discord server (http://augur.net/invite/).  I’m not clear on what you are asking regarding Augur redemption, and I already feel bad derailing this thread as much as I have explaining how LevPredict is a subset of Augur’s current implementation (though Augur doesn’t do the invalid as a separate share thing), so I don’t want to continue discussing Augur here unless it is directly related to LevPredict.

