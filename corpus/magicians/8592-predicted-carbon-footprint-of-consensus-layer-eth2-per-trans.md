---
source: magicians
topic_id: 8592
title: Predicted Carbon Footprint of Consensus Layer (Eth2) per transaction
author: Seanyboy
date: "2022-03-13"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/predicted-carbon-footprint-of-consensus-layer-eth2-per-transaction/8592
views: 1195
likes: 9
posts_count: 9
---

# Predicted Carbon Footprint of Consensus Layer (Eth2) per transaction

We’re working on a project and it’s important for us to get a handle on the predicted carbon footprint (kgCO2) of an average consensus layer (Eth2) transaction - I would be grateful if anyone has any information up-to-date information on this?

Also, it would be really good to know the carbon footprint of a typical Layer 2 transaction when on the consensus layer. There doesn’t seem to be a lot of information on this either. The Layer 2 we are looking at is Arbitrum but happy to take some generic average values for a typical Layer 2 transaction if anyone can point me in the right direction.

Many thanks

## Replies

**Pandapip1** (2022-03-14):

This is completely theoretical, but my logic is as follows:

1. Everyone who validates blocks wants to make a profit
2. To make a profit, the energy cost of validating blocks must be less than the expected reward of validating those blocks.
3. According to Carbon Footprint Factsheet | Center for Sustainable Systems, each kWh generated in the U.S. results in an average of 0.889 pounds of CO2e.
4. According to Annual Electricity Price Comparison by State, Louisiana has the lowest energy cost, of 7.51 cents per kWh.
5. Fast gas fees on arbitium are about 2.71 cents per 20k gas right now. Therefore, 20k gas, from this analysis, releases a maximum of 0.32079760319 pounds of CO2e.

There’s almost certainly some problems with this analysis, but this is my rough estimate.

Here are more figures for other chains (for 20k gas):

PoW Ethereum: 22.4913448735 pounds of CO2e

Binance Chain: 0.48599334699 pounds

Polygon Chain: 0.01873114713 pounds

Gnosis Chain: 0.00098682669 pounds

EDIT: The lowest energy prices are found in Libya, at 0.7 cents per kWh (source: [Worldwide electricity pricing – energy cost per KWh in 230 countries | Cable.co.uk](https://www.cable.co.uk/energy/worldwide-pricing/)), with 0.55 pounds of CO2e per kWh (source: [Libya: CO2 Country Profile - Our World in Data](https://ourworldindata.org/co2/country/libya)). This gives these updated stats per 20k gas:

Arbitium: 2.12928571425 pounds (2236 visa transactions per transfer)

PoW Ethereum: 149.285714286 pounds (156750 visa transactions per transfer)

Binance Chain: 3.22576814999 pounds (3387 visa transactions per transfer)

Polygon Chain: 0.12432749995 pounds (131 visa transactions per transfer)

Gnosis Chain: 0.00655003638 pounds (7 visa transactions per transfer)

---

**Seanyboy** (2022-03-14):

Thanks [@Pandapip1](/u/pandapip1)

The rough numbers are a good starting point.

To be fair, I don’t fully understand Arbitrum but I’ve been tasked to do the numbers.

Do you know how many transactions on Arbitrum when rolled up would equate to 20k gas if we assume say an average of $10 per transaction (smart contract NFT type transactions)?

Or, can you point me in the direction of a formula?

I guess this depends on how many transactions are rolled up into the single transaction that is then sent to the mainnet. Don’t suppose you know anything about this?

My understanding is that Arbitrum can scale transactions such that we can choose how many times a day for example the rolled up transactions are written back to the mainnet. Assuming we can do this, it allows us to control the number of transactions per day, and therefore, predict our CO2 emissions (roughly).

Also, if we wanted to calculate the energy usage / carbon footprint to execute a mint of an NFT based on the number of computational calculations on Arbitrum Layer 2, I assume we need to know the following:

1. Number of transactions required to execute a mint inside Arbitrum
2. Number of transactions that can be rolled up on Arbitrum that have to be written back to the mainnet.

Sorry for asking so many questions.

---

**Pandapip1** (2022-03-14):

> Do you know how many transactions on Arbitrum when rolled up would equate to 20k gas if we assume say an average of $10 per transaction (smart contract NFT type transactions)?

A transaction of the built-in coin always costs 21k gas. It’s the gas price itself that varies.

> I guess this depends on how many transactions are rolled up into the single transaction that is then sent to the mainnet. Don’t suppose you know anything about this?

I’d recommend you look at [EIP-1559: Fee market change for ETH 1.0 chain](https://eips.ethereum.org/EIPS/eip-1559) for more information.

> My understanding is that Arbitrum can scale transactions such that we can choose how many times a day for example the rolled up transactions are written back to the mainnet. Assuming we can do this, it allows us to control the number of transactions per day, and therefore, predict our CO2 emissions (roughly).

I’m not really an arbitium expert, so I’m not entirely sure ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

> Also, if we wanted to calculate the energy usage / carbon footprint to execute a mint of an NFT based on the number of computational calculations on Arbitrum Layer 2, I assume we need to know the following:
>
>
> Number of transactions required to execute a mint inside Arbitrum?
> Number of transactions that can be rolled up on Arbitrum that have to be written back to the mainnet.

Close. You’d need to know how much gas would be consumed. Think of gas as a unit of computation – one gas could let you add two numbers X times, store Y bytes of data, etc…

---

**abcoathup** (2022-03-15):

A good place to start is:



      [ethereum.org](https://ethereum.org/en/energy-consumption/)



    ![image](https://ethereum.org/en/energy-consumption/images/home/hero.png)

###



The basic information you need to understand Ethereum's energy consumption.

---

**Seanyboy** (2022-03-15):

Thanks [@abcoathup](/u/abcoathup) for the link.

I now understand why [@Pandapip1](/u/pandapip1) set out some rough estimates, which I appreciate - thank you. It’s clearly notoriously difficult to establish a per transaction carbon footprint for any Ethereum based transactions. The following statement on [ethereum.org](http://ethereum.org) explains this:

“It’s not entirely accurate to compare based on number of transactions as Ethereum’s energy usage is time-based. The energy usage of Ethereum is the same in 1 minute regardless if it does 1 or 1,000 transactions.”

Herein lies the problem.

---

**Pandapip1** (2022-03-16):

I found this. These are probably the stats you are looking for: https://www.xdaichain.com/about-gc/news-and-information/xdai-energy-efficiency

---

**Anais** (2022-03-18):

The EEA has started working on this (internally). They recently started a blog series for the public, starting with a high level introduction : [Ethereum’s Environmental Footprint: Breaking Down the Misconceptions - Enterprise Ethereum Alliance](https://entethalliance.org/ethereums-environmental-footprint-breaking-down-the-misconceptions/) . Maybe you can reach out to them ?

---

**tynes** (2022-03-18):

Be sure to take into account every full node (ie Infrua, Alchemy, hobbyists, etc) as well as every consumer device that connects to the network to send transactions or display data when it comes to thinking about the “energy usage” of the network.

