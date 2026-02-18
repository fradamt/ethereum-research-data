---
source: ethresearch
topic_id: 5475
title: Would a market-priced risk-free rate be valuable data?
author: jnmclarty
date: "2019-05-18"
category: Economics
tags: []
url: https://ethresear.ch/t/would-a-market-priced-risk-free-rate-be-valuable-data/5475
views: 1623
likes: 7
posts_count: 7
---

# Would a market-priced risk-free rate be valuable data?

I’m seeking feedback on the merit of an idea which could reveal a new market-priced proxy for a risk-free rate (RFR).  I assert that several niches of finance-related development in the ecosystem could benefit from learning about a native and global RFR decoupled from any central planning or state-associated actor.

I shared one rough implementation idea in a [post](https://medium.com/@jeffrey.mclarty/could-we-use-programmable-capital-to-quantify-a-risk-free-rate-proxy-eee78e133d68), which could be summarised as:

The creation of a finite series of periodic smart contracts, which allow investors to bid on a donated-in-advance amount of ether, in exchange for locking up the winning bidders’ bids only to return it after a known-at-bid-time amount of time.

As example, lets say one of the contracts is launched with a donation phase of 6 months, a bidding phase of 1 month, then a lockup of 12 months, and assume 100 ETH was donated.  If a bidder bid 10000 ETH, we would learn the RFR proxy for ETH is 1%.

The contract would need to be a set-and-forget type instrument, with no governance after instantiation to truly be a RFR.  All actors involved in the setup of the experiment would likely have to be altruistic and operating pro-bono; since there can be no profit anywhere.

I believe I have the technical and domain skills to execute this experiment.

What I don’t have is:

1. Marketing channels/audience/network to raise donations for the “interest”.
2. Funds to pay to have the smart contracts audited.
3. Time beyond reasonable levels of hobby-like capacity.

Do you think this experiment has merit?  Do you think somebody might offer a pro-bono contract audit?  Do you think people would donate?

## Replies

**STAGHA** (2019-05-22):

I personally do’t think it’s possible to quantify such a proxy. The winning bider will be the one who requires the lowerst return. One person might require 0,5% but the vast majority might require above 3 %. Therefore using an auction mechanism does not reflect the market majority.  Also the main risk types you list like smart contract risk  cannot be decoupled from the main risk that is price volatility of Ether.

I don’t want to sound pessimistic but i think it’s quite impossible to quantify something like that in an experiment in a reliable way.

---

**jnmclarty** (2019-05-23):

Thanks for reading thoroughly, and taking time to reply.  You mention good points.  Unless somebody counters you, I suspect I will stand down on this.

---

**STAGHA** (2019-05-23):

I found something quite similiar that might be interesting for you to look at. On Polkdaot there will be a smart contract Parachain at Launch called Edgeware. The way they distribute their tokens is that you can lock your ETH into a smart contract on the Ethereum Mainnet and get compensated relative to your stake and your lockup period. After the lockup period you get your ETH + the respective Edgeware Token.

There is basically no risk aside from the (simple) smart contract risk of the lockup contract. The contract is audited. They have a maximum cap at 2,2 million ETH. I think that might replicate your expirement quite well at relatively large scale. It start at June 1. More information for you: https://blog.edgewa.re/important-updates-to-the-edgeware-lockdrop/

Thank you too!

---

**bgits** (2019-05-25):

Having a market determined risk free rate would absolutely be helpful as we can’t effectively discount future value flows without it.

It’s worth considering what makes the risk-free rate in established markets. It’s generally the longest duration interest rate of the most liquid credit market + a default spread. So for USD, it would be the 10-year treasury, which is generally used over the 30-year because of liquidity. For the Indian rupee one would use long-term government bonds + a credit default spread.

In order for the risk-free rate to be valuable as a data point in something like valuation, it would need to be a long term rate of at least 5 years duration.

It’s also worth noting the contract itself is not without risk and there should probably be a market on the failure of the contract with the true RFR being the yield + default premium.

---

**jnmclarty** (2019-05-25):

[@bgits](/u/bgits)

I think if we set out to design an experiment to measure the RFR, we might want to let the market annualize it for us,  by creating explicit maturities for an entire yield curve; even if it did end up being flat-ish. This ecosystem also doesn’t have the longer-term ALM type institutions working/demanding instruments with 10 to 30 yr horizons, so we can’t predict what term would be most liquid.  Nor could we even guarantee there would be a secondary market.

The contract failure- (what you called default-) risk would be a very nice-to-have measurement. I can’t think of how to fund that contract, let alone in a trustless way.  Like, how could the blockchain know if a contract failed to perform? Sure we could have humans vote - but now it’s getting complicated.  And who is going to sell the insurance for that, even if we could build the mechanism (decentralized or otherwise).  In the same way that government-based RFR-proxies have residual, possibly structural, risk included in what we end up calling “risk free”, the crypto ecosystem may simply have similar spreads.  However, as trust climbed in the contract code, that contract-failure-risk, however small, would likely drop with every trade lifecycle completed for the contract.  I’d wager, it would approach a very low but indeed non-zero number, which probably wouldn’t be material within 4 or 5 life cycles of the contract; especially if it was audited.

---

**bgits** (2019-05-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/jnmclarty/48/3540_2.png) jnmclarty:

> how could the blockchain know if a contract failed to perform?

I think futarchy type contracts could accomplish this. An Augur market on the failure of a certain contract would give a premium to add in.

I think we may also have an opportunity to create long term rate instruments in POS backed by future staking rewards.

