---
source: ethresearch
topic_id: 21070
title: Concerning Ethereum's Fee Issues
author: as1ndu
date: "2024-11-23"
category: Applications
tags: []
url: https://ethresear.ch/t/concerning-ethereums-fee-issues/21070
views: 217
likes: 3
posts_count: 2
---

# Concerning Ethereum's Fee Issues

I have been looking at the Ethereum prices for gas costs (transaction fees?).

Gas tracking resources  — https://etherscan.io/gastracker

I noticed that simply sending a transaction is actually decently cheap, about under $1.

What’s seems to be costly for making transactions is [smart contract calls](https://etherscan.io/gastracker#gasguzzler).

My assumption is that, the more operations a smart contract runs to execute its task the costlier it’s is in terms of fees.

It is said that swapping, costs about $16 per contract call.

I am assuming that this is expensive because the swap is probably made via an automated market maker like uniswap. (i.e lots of code to run)

Here is my idea.

What if I am to strip down the concept of swapping a coin in to a very simple smart contract.

By simple, I mean;

- No order books
- No market making
- Higher dimensional swaps (ability to swap any combination of assets)
- No Deposits
- No Withdraws

How the basic swap application would work. (Let’s say a PEPE/USDC swap application)

- Create a contract that only holds PEPE & USDC
- Periodically push exchange rates between PEPE/USD to contract from centralised exchange
- When users send USDC to swap contact it simply uses the stored exchange rate to send an equivalent amount of PEPE
- When users send an an amount of PEPE to the swap contract it also uses the stored exchange rate to send back a proportional amount of USDC to the sender.
- Has basic error handling (when not enough USDC or PEPE to swap, unsupported coins etc)

I am assuming that these stripped down smart contracts would cost way less since there would be less compute.

Why may this be useful.

1. Cheaper transaction costs for fee sensitive users.
2. Easier to implement
3. Lower surface of attack and hence, reduced contract risk (hacking risk)

My questions for this forum.

a) Has this minimalist approach to smart contracts been explored?

b) Can it help in solving fee issues?

c) If it can help, by how much can fees be reduced?

## Replies

**Ashy5000** (2024-11-26):

This method could reduce gas fees, but there’s a few things you might want to think about.

- Where are the funds in the smart contract coming from?
- What you’re describing has a vulnerability- if the price deviates even slightly from the market price, arbitrage can drain the entire pool, as it won’t affect the price directly.
- If funds are coming from LPs, the above vulnerability could cause significant losses on their part. This means they will only supply funds if they get a very high APY on it.
- If the LPs get a high APY, that means fees will have to be raised to provide that income. And the entire goal is to lower fees.
- Note that you’ll have to rely on oracles for this to work, which adds an additional attack vector.
- You won’t be able to trade any tokens that aren’t traded on CEXs/don’t have price feeds, as you won’t have anywhere to get the price data from.

Overall, I think the oracle idea still has potential, as long as you keep the price updates frequent. Maybe you could create an incentive for third parties to update the price?

Also, your idea solves an important issue- price impact. The price isn’t directly impacted by swaps, so larger trades won’t result in a much lower-valued output than input.

A ‘minimalist’ smart contract could also lower deployment costs and make it easier to create a new trading pair. My suggestion would be for you to write and optimize a version of what you’re describing, and write some unit tests to compare gas fees/price impact with a well-established DEX like Uniswap.

