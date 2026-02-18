---
source: ethresearch
topic_id: 7909
title: Rebutting Flare and Tarun Chitra on Proof of Stake
author: MaverickChow
date: "2020-08-28"
category: Economics
tags: []
url: https://ethresear.ch/t/rebutting-flare-and-tarun-chitra-on-proof-of-stake/7909
views: 1771
likes: 0
posts_count: 7
---

# Rebutting Flare and Tarun Chitra on Proof of Stake

Not sure if it is appropriate for me to post this here, but…

Referring to [Domain error](https://flare.ghost.io/theflarenetwork/) and [[2001.00919] Competitive equilibria between staking and on-chain lending](https://arxiv.org/abs/2001.00919) on how Proof of Stake security can be impaired/cannibalized by higher returns from DeFi lending, I wish to present my rebuttal here.

Tarun Chitra’s argument is if return from DeFi lending is higher than return from staking, then capital would flow to such DeFi lending, causing reduced network security.

Flare shares the same argument while undermining the critically important relation of price = security.

My rebuttal:

1. Higher DeFi lending does not impair network security simply because capital flow between staking and lending will eventually reach a balance. As more capital switches from staking to lending, existing capital that continue to stake will earn a larger share of the staking pie. Eventually the return from staking will be equal to the return from lending, after risk-adjusted. Over the long term, I believe all DeFi lending return (and staking return) will normalize to around 7% average, disregarding over 100% annual return currently offered by DeFi lending that is simply fundamentally unsustainable.
2. The remaining leftover capital that continue to stake may still fully secure the network without any compromise, if the price of ETH is equivalent to (the total economic value of all assets tokenized on Ethereum) / (the number of ETH staked). In this case, it does not matter how much capital leaves staking in favor of lending, network security would still be preserved.

To quote Flare:

> Taken to the logical endpoint, if smart contract networks using proof of stake were to become the ubiquitous method of doing business, the scale of diversion of capital required from other endeavors, just to secure the value built on these networks, would make the cost of commerce unfeasibly high. For this reason it is extremely unlikely to happen.

In my opinion, as long as a network (whatever the network it is) is used to secure the value built above it, the security in place must at least be worth as much as the value. Otherwise, imagine a network is used to secure some assets worth $1 trillion, but the instrument (be it coin, token, stablecoin, etc) used to secure the network is just worth $100 (as an extreme example to explain my point), then an arbitrage value of around $0.9999 trillion would be available for exploitation. Thus, for Flare to favor an instrument (Spark) which price is detached from security would be unwise.

> Flare is at its core a new way of scaling smart contract platforms that does not link safety with the value of its token.

This is unwise. Something has to give. If it is not Spark, then it needs to be something else. Otherwise, arbitrage would exist. And such arbitrage would compromise the network security.

Question: What defect do you see from my rebuttal?

## Replies

**kladkogex** (2020-08-28):

A legitimate reason to lend a token is shorting.

For shorting if a  PoS token is a ponzi scheme (many of them are ) sane investors will want to short it so short interest will be high.

It a token is legit short interest will be low.

Which kind of proves that the result will be healthy.  Good tokens will have low short interest and therefore little competition to staking. Bad tokens will have high short interest and high competition to staking

---

**wnuelle** (2020-09-02):

I think the argument against your point would be that the process of stabilization between lending and staking represents a loss of security in PoS models. If capital is flowing out of PoS to lending for those rates to stabilize, then PoS is losing security.

To your second point, though, security as a function of capital in PoS may be a logistic function where first derivative of security with respect to capital is very small, meaning you don’t actually lose much security as capital flows out.

---

**MaverickChow** (2020-09-02):

Capital flowing out of PoS’ staking will cause a decline in security, but if the price of ETH is adjusted upward whereby its price is always (the total economic value of all assets tokenized on Ethereum) / (the number of ETH staked), i.e. at par, then there will be no loss of security.

The rates stabilize themselves economically. Capital does not deliberately flow out in order to stabilize the rates.

Whether you will lose any security as capital flows out from staking to lending (or to any other economic / commercial use other than lending) depends on what is used to secure the network, i.e. ETH. Thus the less ETH is being staked, the less security it gets. Capital is ETH, and vice versa. They are not mutually exclusive.

Edit: Welcome. And thank you for your first post.

---

**kladkogex** (2020-09-03):

If you token is locked in PoS, nothing prevents using this token in DeFi.

You can have a derivative token, that represents the staked token.

---

**denett** (2020-09-03):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> If you token is locked in PoS, nothing prevents using this token in DeFi.

If you can use the token you have staked as collateral in DeFi to borrow, the actual value at stake is reduced, because you can keep the tokens you have borrowed after you have been slashed. So allowing staked tokens to be used in DeFi will reduce the security of the blockchain.

---

**MaverickChow** (2020-09-04):

Another thing I wish to elaborate regarding Proof of Stake being the superior choice of blockchain protocol is because the price is attached to the security. If a malicious actor wants to hijack an asset base with the value of, say, $1 billion, he/she must first have the same $1 billion at stake to do the hijacking. This renders his arbitrage opportunity to be zero.

On the other hand, Proof of Work is far less secure as the price is detached from the network’s security. Let’s say an asset base with value of $1 billion is utilized on such blockchain. And if the majority of hashing power, say 51%, costs just $1 million for whatever the reason such as technological advancement that makes processing power far cheaper, to be acquired, then the arbitrage opportunity in hijacking such network would be $999 million, which is also 999x ROI as an example. This is possible because security is tied to the hashing power, which in turn is tied to technological advancements. And as technology continues to advance, the cost of acquiring hashing power declines, which also means the cost to hijack the network declines, regardless of the price of the native coin. The variation of the native coin’s price merely dictates the arbitrage opportunity that arises, and this certainly does not thwart any intent, nor attempt, to hijack.

I have no idea why the appeal to Proof of Work persists in some sector of the crypto space, but it is really not hard to see why Proof of Work is a very inferior protocol, security-wise.

