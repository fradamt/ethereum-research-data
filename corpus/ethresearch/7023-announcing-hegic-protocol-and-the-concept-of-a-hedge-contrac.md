---
source: ethresearch
topic_id: 7023
title: Announcing Hegic Protocol and the Concept of a Hedge Contract
author: 0mllwntrmt3
date: "2020-02-25"
category: Applications
tags: []
url: https://ethresear.ch/t/announcing-hegic-protocol-and-the-concept-of-a-hedge-contract/7023
views: 3636
likes: 1
posts_count: 12
---

# Announcing Hegic Protocol and the Concept of a Hedge Contract

**Hegic is an on-chain options trading protocol on Ethereum powered by hedge contracts and liquidity pools. Protocol can be used for trustless creating, maintaining and settling of hedge contracts.**

Whitepaper: https://ipfs.io/ipfs/QmWy8x6vEunH4gD2gWT4Bt4bBwWX2KAEUov46tCLvMRcME

Hedge contract is an options-like on-chain contract that gives the holder (buyer) a right to buy or to sell an asset at a certain price (strike) as well as imposes the obligation on the writer (seller) to buy or to sell  an  asset during  a  certain  period. Hedge contracts can be considered as a non-custodial, trustless and  censorship-resistant  alternative  to  options contracts. Exercising  of  hedge  contracts  is  guaranteed  by  the liquidity  allocated  and locked on them, timestamps and Ethereum Virtual Machine (EVM) that executes the code.

On Hegic, liquidity providers’ (writers’) funds can be distributed between many hedge contracts simultaneously.  It diversifies the  liquidity  allocation  and  makes capital  work  in  an  efficient  way.  The assumption is that in the long-run, liquidity providers’ returns could beat the returns of a solo options writer.

The initial implementations of Hegic will enable holders to buy put hedge contracts that will give them a right to swap ETH to DAI stablecoin at a certain price (strike) at any given moment until the expiration. Hegic uses a dynamic strike price determination approach, which influences the rate and the premium of hedge contracts. Maintenance and execution of hedge contracts do not depend on the external price feeds.

Liquidity pools are non-custodial.  In the initial implementations of Hegic, the rate for holding a hedge contract varies from 0.5% up to 2.0% per week. Theoretical yearly returns for hedge contracts writers (sellers) are in between from +27% up to +108% APR on DAI, USDC or USDT. While allocating DAI token in the pool on Hegic, liquidity providers will be simultaneously earning DSR (DAI Savings Rate) with the help of CHAI (ERC20 wrapper over the DSR). Allocating DAI in the liquidity pool provides writers with the returns on DAI paid by MakerDAO’s DSR plus the premiums that are paid by hedge contracts holders.

HEGIC an ERC20 token that is used for distribution of 100% of the settlement fees between all the token   holders   and   in   the   protocol   on-chain   governance   purposes.   HEGIC   token   combines the collective  fractional  ownership,  utility  and  governance  functions.HEGIC  has  a  fixed  supply  of 3012009 HEGIC tokens, which will be unlocked with the time after the particular goals are reached by the Hegic protocol.

Code of the deployed ETH put hedge contract:

[![index](https://ethresear.ch/uploads/default/original/2X/9/9514f7f8765d61a9b1ea33aea321919f7af93c41.jpeg)index757×590 88.2 KB](https://ethresear.ch/uploads/default/9514f7f8765d61a9b1ea33aea321919f7af93c41)

Hegic protocol is live on Ethereum mainnet: https://www.hegic.co

Open source code of the Hegic protocol: /hegic on Github

Hegic ETH Put Hedge Contract (Ethereum mainnet): 0x27b6125328ca57d5d96baaa4f9ca8c5edbafe016

Hegic DAI Liquidity Pool Contract (Ethereum mainnet): 0x009c216b7e86e5c38af14fcd8c07aab3a2e7888e

**Feedback is very much appreciated.**

## Replies

**monteluna** (2020-02-25):

Glancing through the WP I have some thoughts which maybe I didn’t see?

I’m seeing the HEGIC token has a few interesting properties with governance and faster writeDAI widthdrawal, but why not include a stake and burn model if the contract is released? I mean, I see the WP has a staking model for the entire market, but it would be interesting if every paid out contract burned a little bit of HEGIC. There could be a way to programatically set this burn rate to set targets for certain system parameters too. Maybe something like a function to set burn rate to target 1% token value increase for the current year could work.

Also, how are premiums calculated? I’m a bit of an Augur maximalist so I think making this open and well known to allow for comparisons with contracts on Augur would be helpful. I just see that as a possible arb opportunity if Augur starts kicking off and premiums are different on both sites.

---

**0mllwntrmt3** (2020-02-25):

answerin’ z 1st q:

in z current concept of Hegic all z settlement fees r distributed between z HEGIC token holders every quarter. dan elitzer from mitbitcoinclub has suggested me 2 think abt z burn model as it works in makerdao. i thought that it might b a gr8 gas-efficient way 2 distribute z settlement fees: buying back HEGIC tokens from z market every quarter & ?burn? what do u think of it?

answerin’ z 2nd q:

pls read z ‘pricing model’ section of z whitepaper 1more time. z rate on Hegic is a predefined percent of z asset’s value that depends on z period of a hedge contract. u can find them in z Table 4: Rates of put hedge contracts with different strike prices and periods on Hegic.

citin’ whitepaper: HEGIC  token  is  used  in  HIPs  (Hegic  Improvement  Proposal)  for  governance  purposes. HEGIC  token holders  can  vote  for  changing  hedge  contracts rates,  settlement  fee  size,  strike  price  multipliers, assets supported by hedge contracts and more.

---

**monteluna** (2020-02-25):

So I don’t know of any protocol that does a full buy back and burn, and I do know Augur turned away from it for v2 to a burn model “when things are ok”. [@MicahZoltu](/u/micahzoltu) what was the whole reason for switching off buy back and burn? Was it just because it was less efficient than just burning on smaller transactions?

Maybe you just do buy back and burn quarterly though. Augur is weekly but I imagine weekly BBB auctions are too gas intensive, where doing one every 3 months is ok. That could be an option.

Another consideration is whether it would be an issue for governance. I’m not sure if you want to lock tokens in a contract that can’t be used for governance votes. There could be some weird situation where an attacker can just buy a lot of the HEGIC during a BBB auction.

To give some insight into Augur’s way AFAIK, there’s a weekly staking period and separate burn everytime a market ends. MKR just dumps MKR fees into a contract that anyone can burn at any point.

Honestly, I would probably just do a burn when hedge contracts end, and allow a stake/vote where staking locks into the earned fees directly and users can still vote with their tokens. Or just do a “as long as you stake before this day you can access the pool”.

---

**MicahZoltu** (2020-02-25):

I’m not the right person to ask about the reasoning for doing dividends instead of buy & burn.  I lobbied hard for buy & burn and think the dividend model is silly.

The argument I have heard *other* people make is that with the dividend model the weekly rewards are distributed only to people who show up to claim them.  In theory, this means that parked/idle/loaned REP doesn’t consume dividends and thus people who *do* show up get more.  I believe that in a world of spherical cows this doesn’t actually make a difference in terms of pricing/valuation/return but when it comes to human behavior all sorts of things that shouldn’t work do so maybe it will?  ![:man_shrugging:](https://ethresear.ch/images/emoji/facebook_messenger/man_shrugging.png?v=14)

There are also tax benefits to buy & burn in that you will be taxed when you exit which in many countries means long term capital gains which tend to be taxed lower or not at all, while dividends tend to be taxed higher (as income).

---

**monteluna** (2020-02-26):

Ok. So buy and burn is good. In that case, was the plan to do an auction since the smart contract can’t really know the price?

---

**MicahZoltu** (2020-02-26):

There are two common ways I have seen to handle the situation.

1. Auction.
2. Orderbook (really just an auction in advance).

Maker originally build Oasis DEX so they would have an on-chain place for the contract to buy/sell assets to burn.  When it comes time to sell an asset (so you can burn the proceeds), you just sell it to the best offer on the books at the time of the burn.  Users are incentivized to keep reasonably good offers on the books so they can catch the sale.

The one problem with the orderbook is that the trigger transaction can be frontrun which can lead to only bots actually filling orders, which can (in theory) lead to the book drying up as no one is getting the purchased asset at a discount over market price and maintaining positions on an on-chain DEX is hard.  If the book does dry up, you can end up getting bad pricing.

The auction is the best solution IMO.  It can be short, I think the Maker auction is 10 minutes.  Arbitrage bots will be the participants in the auction and it just needs to be long enough to make block stuffing an unprofitable attack.

---

**MicahZoltu** (2020-02-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/0mllwntrmt3/48/4600_2.png) 0mllwntrmt3:

> Liquidity pools are non-custodial.

Since you have a centralized price feed provider, I would argue that liquidity pools are in fact custodial (as is any asset that depends on a centralized price feed).

The nice thing about traditional options is that you don’t need a price feed.  What is the reason you decided to go this route instead (which appears to require a price feed) rather than traditional options (which don’t)?

---

**MicahZoltu** (2020-02-26):

> Note that this is the only part of  the  Hegic  system  that  uses  oracles  to  work  with  the  external  price  feeds. Maintenance  and execution of hedge contracts do not depend on the external price feeds. Such an approach is used for guaranteeing  the  security  of  active  hedge  contracts  and  for  preventing  attacks  and  exploits of oracles from price attacks. Thus, active hedge contracts are safe from the oracles’ manipulations.

If the oracle were compromised, couldn’t it report the price of ETH being 0, thus allowing people to create hedged positions for free?  I suppose that isn’t too bad if that is all an attacker can do with a compromised price feed as it just means that liquidity providers don’t make any money, but they also shouldn’t lose any money.

---

The whitepaper says it converts DAI to CHAI, but I don’t see that actually happening in the contracts.  Am I missing something?

---

**0mllwntrmt3** (2020-02-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> The nice thing about traditional options is that you don’t need a price feed. What is the reason you decided to go this route instead (which appears to require a price feed) rather than traditional options (which don’t)?

price feed is **only** required in 1 part of z hedge contract: **pricing**. if u visit [hegic.co](http://hegic.co) website, u’ll see z currenct price of ETH. chainlink’s ETH/USD price reference contract (with 21 independent data providers) is used 4 calculatin’ z price of hedge contracts based on z current price of ETH. after a contract is activated, z liquidity is locked on z hedge contract (+ it’s timestamp’d). price feeds are **not** used for maintainin’ / executin’ / settlin’ hedge contracts

---

**0mllwntrmt3** (2020-02-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> If the oracle were compromised, couldn’t it report the price of ETH being 0, thus allowing people to create hedged positions for free?

to compromise z oracle one should attack 21 independent data providers. as z price feed is used only for pricing z hedge contracts, z data received from an oracle that z price of ETH is 0 will lead 2 a sutuation wen a hedge contract will be priced as a free one, but z liquidity locked on z contract will also be zero due to z 0 price of ETH

---

**0mllwntrmt3** (2020-02-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> The whitepaper says it converts DAI to CHAI, but I don’t see that actually happening in the contracts. Am I missing something?

wip. i’m chattin’ with martin lundfall in order 2 properly integr8 chai 4 distrubitin’ z interest between individual liquidity providers coz z interest (DSR) shouldn’t b pooled

