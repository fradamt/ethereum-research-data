---
source: ethresearch
topic_id: 13560
title: Low-Toxicity AMM
author: alexnezlobin
date: "2022-09-02"
category: Applications
tags: []
url: https://ethresear.ch/t/low-toxicity-amm/13560
views: 3467
likes: 5
posts_count: 4
---

# Low-Toxicity AMM

**SUMMARY**

We are designing an AMM to fight the problem of high order flow toxicity. The idea is to make it easy for non-arbitrage traders to execute large deals by gradually taking or making liquidity. The AMM is optimized for passive liquidity provision, with features such as: dynamic fees, automatic positioning and concentration of liquidity, fully internal price discovery, and options to contribute one-way or two-way liquidity in a single token of LP’s choice.

The main mechanism can be called a double-sided Dutch auction. In the absence of swaps, both sides of the liquidity distribution are moved closer to the mid-price, with liquidity getting more concentrated around that price. Each swap expands the bid-ask spread and flattens the distribution of liquidity.

**The protocol in three pictures**

Let’s say Alice wants to buy some ETH for USDT. The protocol initially positions all available liquidity as follows:

[![ltamm1](https://ethresear.ch/uploads/default/original/2X/e/e3e83f5b73b68ea74afea736c7f8651e48169132.png)ltamm1366×251 7.83 KB](https://ethresear.ch/uploads/default/e3e83f5b73b68ea74afea736c7f8651e48169132)

All prices in the picture above are after fees. Alice can buy the first unit of ETH at *askP* or sell at *bidP*. If she takes all liquidity between prices *askP* and *P’*, she will pay a weighted average of prices in this range (which will be closer to *askP* since the distribution of ETH liquidity is declining in price).

After Alice’s swap, the synthetic order book looks as follows:

[![ltamm2](https://ethresear.ch/uploads/default/original/2X/a/a3198852dca74373586035b296f9a5c3c270b4bd.png)ltamm2367×253 8.66 KB](https://ethresear.ch/uploads/default/a3198852dca74373586035b296f9a5c3c270b4bd)

Dashed red and green lines show the liquidity position before the swap, shaded areas show the liquidity position once the swap is executed.

According to the protocol:

(i) the ask price immediately moves to *P’*,

(ii) the mid-price, which is not always exactly in the middle between the bid and ask prices, immediately travels the same distance as *askP*,

(iii) the opposite side of the book is *flattened*, so that its height matches that of the ask side at the new ask price, and

(iv) the bid price stays the same.

Note that we flatten the USDT liquidity and do not move it right away in the direction of the new mid-price. Instead, we will do this gradually over time. This ensures that LPs make profits on quick roundtrip transactions, such as, say, an uninformed purchase of ETH followed by an arbitrage sale of ETH. Similarly, this approach prevents attacks in which a trader buys one asset to inflate its price and then buys the other asset cheaply. Since the opposite side of the book is flattened and only moves gradually over time, the attacker would have to bear the full cost of the attack but then compete for its benefits with arbitrageurs over multiple blocks.

The last figure shows the behavior of the protocol over time. Each block, the following two transformation are applied to the book:

[![ltamm3](https://ethresear.ch/uploads/default/original/2X/9/99bf7ffc822644458561f8022c535bd66cea2204.png)ltamm3367×253 12.1 KB](https://ethresear.ch/uploads/default/99bf7ffc822644458561f8022c535bd66cea2204)

Hatched areas show the positions of ETH and USDT liquidity at the end of the previous block, shaded areas show the positions at the beginning of the current block.

The bid-ask spread contracts at some rate (shrinkage), and the concentration of liquidity increases at some other rate (growth).

So spreads shrink and liquidity gets concentrated over time. Each swap expands the spread and flattens liquidity. In equilibrium, the two forces will be offsetting each other. For example, if trading volume is low, liquidity will get concentrated and the spread will shrink, attracting new traders. The new swaps will then flatten the liquidity distribution and expand the spread.

For more details and equilibrium analysis, see our Medium post: https://medium.com/@alexnezlobin/low-toxicity-amm-traders-perspective-a2509bcc5b7

**QUESTIONS:**

1. Did we miss anything? What attacks come to mind that the current iteration of the algorithm can be susceptible to?
2. Do the economics of algorithm make sense?
3. The list of main features is available at: https://medium.com/@alexnezlobin/designing-a-low-toxicity-automated-market-maker-c789d7f2aa. Did we miss anything important?
4. We are developing these ideas further, thinking through the LP incentives and applications to other markets, such as NFT and mean-reverting pairs. If you have ideas/questions/suggestions, please comment here or reach us at ltdex@pm.me.

## Replies

**llllvvuu** (2022-09-10):

Very cool! Paradigm has been pushing Dutch auctions as well: [Variable Rate GDAs - Paradigm](https://www.paradigm.xyz/2022/08/vrgda)

It makes a lot of sense for revenue maximization.

---

**alexnezlobin** (2022-09-12):

Yes, I think the main difference with Paradigm’s Dutch auctions is that we are designing a two-sided market.

So, for example, for NFTs, we want LTAMM to look like sudoswap with a GDA on each side of the book. The tricky part is to coordinate the Dutch auctions so that one side cannot be abused by manipulating the other side. That is, make it resistant to attacks like spoofing in TradFi but with blackjack and flash loans.

---

**0xValerius** (2023-07-20):

[@alexnezlobin](/u/alexnezlobin) very interesting concept. Kudos!

Did you manage to create a PoC for this kind of AMM?

