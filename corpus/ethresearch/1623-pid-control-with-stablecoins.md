---
source: ethresearch
topic_id: 1623
title: PID control with stablecoins
author: k26dr
date: "2018-04-05"
category: Economics
tags: []
url: https://ethresear.ch/t/pid-control-with-stablecoins/1623
views: 8304
likes: 13
posts_count: 53
---

# PID control with stablecoins

I’m coding up a Solidity implementation of Robert Sams’ [Seignorage Shares](https://bravenewcoin.com/assets/Whitepapers/A-Note-on-Cryptocurrency-Stabilisation-Seigniorage-Shares.pdf). One issue I have with the paper is the formula for determining the number of coins to print/remove based on price.

![image](https://ethresear.ch/uploads/default/original/2X/4/414de50bbece6a23569397ceef4525f8633649c4.png)

If the price of the coin goes down by 1%, this formula would remove 1% of the supply. This seems overly simplistic to me. It’s essentially a P-controller with a P-gain of 1. Using PID control seems like a better option, but tuning the gains would be difficult in the absence of an effective test environment.

Anybody have any thoughts/advise on using PID control with stablecoins?

## Replies

**MicahZoltu** (2018-04-06):

IMO, simple is better.  Can you explain in more detail the problem with simple in this case?  What problem does it lead to?

---

**k26dr** (2018-04-06):

I was worried the printing rate is too fast and supply changes would cause price oscillations.

You’re right though, simple is likely best. I’ve put a gain term in front of the price ratio and set it to 0.1, so the formula looks like this now with alpha = 0.1:

[![image](https://ethresear.ch/uploads/default/original/2X/5/549336d03eede9f6060270395099124bb5a0af30.jpg)image318×114 7.85 KB](https://ethresear.ch/uploads/default/549336d03eede9f6060270395099124bb5a0af30)

The cycle repeats every 1000 blocks, so ~5x per day.

---

**fubuloubu** (2018-04-06):

Working on a test environment, basically a Python framework that’ll let you simulate a smart contract with a pool of user agents with predefined behavior (that can be randomized). What else do you think would be necessary in order to get enough data to tune the PID controller smart contract?

---

**yazzaoui** (2018-04-06):

Had the same idea [here](https://github.com/yazzaoui/Smart-Contracts#stabletoksol) but then I gave up knowing that in practice most of the demand is purely speculative and not transactional, so I’m not confident on the effectiveness of the formula …

---

**k26dr** (2018-04-06):

I doubt the real world response of a price to supply change is linear or consistent, it’s probably chaotic. Maybe simulating chaotic behavior is what is needed here.  Your framework definitely sounds like it will be useful for gathering test data to do a preliminary gain tuning, but with prices and markets real world data is always best. I don’t know if a test environment can properly capture the emotional swings of a market.

---

**k26dr** (2018-04-06):

I’ve actually got a working implementation complete that seems fairly usable. I’ll post it in a couple days once I’ve had time to run it thru a few iterations on the testnet.

It’s a simple proportional supply change in response to a pricing error repeated over many cycles to slowly move the price back to the target. I’ve set it for now so that a 1% movement in price leads to a 0.1% change in supply per cycle (P-gain of 0.1). Cycles are 1000 blocks long.

If you have some math that can provide a more rigorous gain calculation, I’d love to see it.

---

**fubuloubu** (2018-04-06):

Only one way to find out. It seems a lot better than the current best practice more generally of divinating these parameters out of thin air (“how much total supply do I have?”)

---

**vbuterin** (2018-04-06):

Why not just have large active sell orders at $1.01 equivalent and buy orders at $0.99 equivalent and adjust based on fiat price movements? There are designs other than fixed quantity auctions that could make sense here.

---

**fubuloubu** (2018-04-06):

How much control authority do you need to maintain that threshold over time? (e.g. what is the size of those large buy/sell orders)

---

**vbuterin** (2018-04-06):

Why not basically infinite?

I suppose that would be unstable and potentially arbitrageable in case the price feed ever got it wrong; in that case, it could make sense to make the sell price go up as more units get bought (and buy price go down as more units are sold). There’s probably some mathematical formalism that can get you pretty good bounds on loss from arbitrage if the attacker has a more up-to-date view of the price than the blockchain feed. That’s the main thing I would be worried about.

---

**fubuloubu** (2018-04-06):

An infinite-sized sell order of a finite quantity item? I’d imagine there’d be a particular quantity of the stable coin at any given time (that could get minted as demand grew *cough* US Mint) so that the manager of the stable coin retained a certain dominance to the buy/sell orders to maintain that stability. But that dominance can’t be infinite, if there was unlimited supply it would be basically worthless, and you would only have a limited amount of buy power in whatever collotoral you were using to conduct the sale that you had stockpiled.

---

**vbuterin** (2018-04-06):

I was assuming that the PID controller is run by the stablecoin, so of course it would have access to the ability to mint arbitrarily large amounts. Is that assumption mistaken?

---

**fubuloubu** (2018-04-06):

Nope, on the sell side you’re right that basically makes it infinite (although you wouldn’t just continuously mint coins, and probably batch them for efficiency). On the buy side you wouldn’t have infinite authority however, eventually you’d run out of collotoral.

---

**vbuterin** (2018-04-06):

Right, but on the buy side eventually everyone will have sold all of their coins to you. Also, in Seignorage Shares, the buy order is buying coins for shares, and shares are also something that the system has the right to print an unlimited quantity of.

---

**fubuloubu** (2018-04-06):

Hmm, yeah. I think broader Controls Theory isn’t really useful to apply here because it’s full authority as you said, and the dynamic response is pretty minimal as long as cycles are tight enough and enough authority is exhibited.

---

**vbuterin** (2018-04-06):

The theory that I *do* think is useful is insights from mechanism design about making mechanisms with bounded loss. I do worry that a badly designed seignorage shares system could get money-pumped to hell during periods of high price volatility. Maybe Augur or Gnosis people could come share their insights?

---

**k26dr** (2018-04-06):

The nice part about the current design is that the price feed doesn’t have to be very accurate because it’s only required once every 1000 blocks and a mis-pricing doesn’t create arbitrage opportunities. Additionally, the only price feed that needs to be maintained is the one between the stablecoins and USD (I’m assuming we’re pegging to USD for simplicity’s sake), which shouldn’t be very volatile.

If the contract is acting as a market maker, an additional price feed would have to be maintained between the shares and the stablecoins for the contract to keep orders at $0.99 and $1.01, and this price feed would be volatile, making it easy to arbitrage. It worries me that the contract could be attacked too easily.

The best method I’ve seen for price discovery so far is the reverse Dutch auction used by the EOS crowdsale. A fixed number of assets are auctioned off. Bidders contribute to a common pool, raising the price of the asset until it meets the market price. At the end of the cycle, bidders can claim the asset proportional to their percentage of the total bid. The code is simple and I’ve seen it work for the past 8 months so I’m pretty confident in it. Mis-pricings are uncommon and don’t affect the financial health of the contract. This is what I’ve used in the current implementation.

The downside to reverse Dutch auction cycles is that the supply can’t respond to price changes as quickly as in the market-maker method.

---

**k26dr** (2018-04-06):

If the market maker could be implemented securely it does seem like it would be a better control system than the auction. But I’m worried about arbitrageurs causing havoc.

---

**rmsams** (2018-04-06):

So there’s the (1) coin/shares price and the (2) coin/index price (coin/$ for simplicity). Are you suggesting an oracle for (1) as well as (2), and then stablecoin contract mkt maker biases the bid/ask spread around the mid-price feed from (1) on the basis of the feed from (2)?

The simplicity of this LMSR-esq approach seems to invite complicated strategic behaviour, I would guess.

---

**k26dr** (2018-04-07):

I was wrong about only needing one price feed using the reverse Dutch system. In order to determine how many shares to print when contracting the supply, a price feed for the shares is required as well. However, the price feeds still do not directly determine the buy/sell prices, so mis-pricings do not lead to damaging arbitrage opportunities. They lead to bad supply changes, but those can be corrected in the next cycle.


*(32 more replies not shown)*
