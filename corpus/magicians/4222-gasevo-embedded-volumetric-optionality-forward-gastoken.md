---
source: magicians
topic_id: 4222
title: "GasEVO: Embedded Volumetric Optionality Forward GasToken"
author: sbacha
date: "2020-04-27"
category: EIPs
tags: [eip-1559]
url: https://ethereum-magicians.org/t/gasevo-embedded-volumetric-optionality-forward-gastoken/4222
views: 1543
likes: 1
posts_count: 3
---

# GasEVO: Embedded Volumetric Optionality Forward GasToken

[GasEVO: Embedded Volumetric Optionality Forward GasToken](http://www.authorea.com/445804/Oz025FdbiKmaDC3SPE42Zg) contract; an exchange-traded instrument with GasToken as the underlying asset for hedging transaction price and settlement risk for Ethereum.

[Alpha Draft of Paper: www.authorea.com/445804/Oz025FdbiKmaDC3SPE42Zg](http://www.authorea.com/445804/Oz025FdbiKmaDC3SPE42Zg)

Basically making GasToken an exchange-traded token with a few adjustments to enable users to hedge. Long term growth for DEX’s will require some sort of product for professional trading firms to be able to price in this risk and allocate against it.

**Any feedback on math, design, methodology, specifications, additional use-cases, additional use-cases for abuse, are greatly appreciated. This is not a finished work, I just wanted to get additional input before proceeding further down (as it may not be viable in an economic sense)**

**Progress**

- I haven’t figured out the “optimal” pricing strategy
- I haven’t figured out the contract delivery dates
- I haven’t figured out any additional mechanisms or designs to the instrument (e.g. perpetual vs auction, auction design systems (reverse vs Vickrey, etc)

**Concerns**

- Derivatives math and pricing Asian-style options (strike is only at maturity) is difficult
- Speculative nature may not be enough to warrant such market?
- I think if you add the possibility of Gas Station Networks using this and Smart Contract wallets as well, the use case isn’t so much for speculation as it is for end users (i.e. smart contract wallet providers will use this product long run).

The values used to price the options on a 7/30 day monthly contract for delivery (i.e. the maturity of the contract, which would be released of the contract to the option exerciser) are a rough estimate, as some of the answers need a more refined and exacting approach. [Here is the google spreadsheet of them](https://docs.google.com/spreadsheets/d/13_6jlPka3zpeioBb7Ssd4juNuSU2OfIG2tw0UOxh3_c/edit?usp=sharing)

**Some Caveats:**

assuming  is the GasToken “strike price” is GasToken refund: 3575742

GasToken minting cost: 1191914

Period of Time is reflected on the calculation dates based off BitMax contracts for ETH70LD

I am sure my math is wrong, in fact it probably is. It is not meant to be used for an exact proposal: only as an initial starting point for an iterative process to optimize or if not to say that “well we know this wont work as an option because of (x, y, z, etc).”

Yes, the paper is disorganized, I am in the process of re-arranging it, this is purely a rough draft examining the solution.

**Thanks to**

I would like to thank the IC3 team from GasToken for coming up with the original concept of an in-protocol mechanism for hedging transaction settlement risk. EVO’s are nothing new in delivered commodities space, and my experience stems from my companies usage in our own application for physically delivered commodities (i.e. decentralized physical settlement).

**Paper layout**

Additional references are in the draft paper, would like some feedback. The paper is broken up into sections concerning:

- Order Book
- Matching Engines (time/priority, pro-rata, LMM, etc)
- Order Routing (not relevant directly, but can play a part in terms of how a client is submitting transactions to the network, e.g. using Infura vs. full node-local geth)
- Overview of GasEVO
- Overview of the derivatives math to calculate call and put
- Examination of past art and references
- Additional graphs littered along the way,

Additional sources



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)
    [EIP-1559: Fee market change for ETH 1.0 chain](https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783/75) [EIPs](/c/eips/5)



> Figured I should post this here: we are having a 1559 implementers’ call this week. https://github.com/ethereum/pm/issues/167

Sources (more in the paper link)

[GasEVO documentation repo on GitHub](https://github.com/sambacha/gasevo)



      [github.com](https://github.com/sambacha/orderbook-data-raw)




  ![image](https://opengraph.githubassets.com/5dbd29441832d8ce6209f7be0cfd697f/sambacha/orderbook-data-raw)



###



raw data of order book OHLCV for SPY on 4/21/22020 and additional products










[SPY Orderbook information](https://github.com/sambacha/orderbook-data-raw) (used in getting an understanding of market microstructure in legacy markets)

[SPY 4/21 Tick Data NASDAQ format (~500mbs)](https://www.dropbox.com/s/efduyary1lfy1kf/20200421_SPY.i40?dl=0)

[kdb+ joining tools and referenced whitepaper on transactional cost analysis of executed orders on exchange-traded products](https://github.com/sambacha/gasevo/tree/master/kdb)

## Replies

**sbacha** (2020-04-27):

additionally, tracking I am trying to find out the amount of transactions that get submitted, and then an incremented transaction is sent to “speed it up”. if anyone has that readily available I would appreciate it!

---

**sbacha** (2020-05-12):

Here is the draft paper

https://www.authorea.com/users/285079/articles/445181-embedded-volumetric-optionality-a-new-financial-instrument-primitive

