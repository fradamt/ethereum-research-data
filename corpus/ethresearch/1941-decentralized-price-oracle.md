---
source: ethresearch
topic_id: 1941
title: Decentralized price oracle
author: whgeorge
date: "2018-05-08"
category: Economics
tags: []
url: https://ethresear.ch/t/decentralized-price-oracle/1941
views: 2969
likes: 7
posts_count: 10
---

# Decentralized price oracle

[kleroslinearoracledraft7mai2018.pdf](https://ethresear.ch/uploads/default/original/2X/2/2944526f5c63f3adf2ebc4e158f43e8ac12c9463.pdf) (341.5 KB)

I’ve been working on a decentralized oracle to estimate real-number values, to be built on the (decentralized) dispute resolution platform [Kleros](https://kleros.io/assets/whitepaper.pdf) (disclaimer: I work for Kleros). In Kleros, crowdsourced, randomly-selected jurors are chosen to rule on disputes, where they are incentivized to be coherent which we use as a proxy for honesty in the style of [Schellingcoin](https://blog.ethereum.org/2014/03/28/schellingcoin-a-minimal-trust-universal-data-feed/) and [Truthcoin](http://www.truthcoin.info/papers/truthcoin-whitepaper.pdf). Then this is already a sort of oracle, where jurors are bringing some real-world knowledge (the correct ruling of a dispute) onto the blockchain. We leverage this into an oracle on real-values (so particularly useful for prices) by allowing anyone to submit an interval they think the value is in (we then call this person a respondent), and to the degree that these intervals are incoherent, that is converted into a (series of)  disputes. Specifically, you find points where someone’s upper bound is lower than someone else’s lower bound and you ask the jurors whether the true value is higher or lower than the median of the set of these points of incoherence.

This proposal has the advantage that how precise the ultimate answer is is tuned to how large the intervals of the respondents are. Particularly, if someone has an interest in the oracle outputting a very precise result, they can submit a very small interval, and the output will be in that interval as long as the jurors don’t rule that they were wrong. Respondents place a deposit, so they have to calculate to themselves how large an interval they want to submit in terms of whether they have a financial interest in the oracle outputting a precise value, the higher risk of losing a deposit if their interval is very small, and the fact that if they submit a small interval and are ruled right, they get a higher reward drawn from lost deposits from respondents who were ruled wrong.

Also, the number of times Kleros must be called scales with the \log(\text{Resources of wrong respondents})^2. So even if there are many responses, that only meaningfully delays the result to the degree that they disagree with each other, and we could reasonably expect the execution time to be good enough to be useful for many applications.

If anyone wants to check out the attached draft paper and/or if you have any thoughts or comments, that would be really appreciated.

## Replies

**jamesray1** (2018-10-17):

Interesting, I like that it is subjective but in a statistical way, like a confidence interval, as it seems that any oracle has to be trusted, thus making the results of that oracle explicitly subjective.

Generally, decentralized oracles on blockchains do require very careful design, as they are prone to manipulation.

Haven’t read the draft paper yet.

---

**mikedeshazer** (2019-12-02):

I’m working on a similar problem. [@jamesray1](/u/jamesray1) made a good point about the subjective nature of oracles. I think the best way is to aggregate data from multiple sources and eliminate outliers + mostly accept data from sources with skin in the game to provide accurate information.

[OrFeed.org](http://OrFeed.org) is a project I’m currently working on that is pursuing these ideas. It’s pretty early at the moment, but obviously open-source and there might be some ideas in there that might help with what you’re doing.

---

**Econymous** (2019-12-02):

It sounds like if there’s a strong universal oracle solution then that could be a major disruptor for blockchain

---

**jamesray1** (2019-12-02):

If you can make the oracle fully distributed, rather than just decentralized, for example by building a happ on Holochain, that would be advantageous. However, I would scrutinise whether oracles are needed for happs, as if they used currencies, then they would use mutual currencies, rather than tokens. Tokens and blockchains depend on universal consensus to prevent double spending, which isn’t how nature works and is fundamentally limiting.

https://twitter.com/holochain/status/1200319766940069888?s=19

---

**whwgeorge** (2019-12-03):

> I think the best way is to aggregate data from multiple sources and eliminate outliers + mostly accept data from sources with skin in the game to provide accurate information.

I think this depends on your application, your needs, and the trust model you are willing to accept. This is sort of parallel to the different trust models of different consensus protocols. If you have a fixed list of sources being aggregated, that has a similar trust model to PBFT style consensus, if you have a pool of token holders that can vote in or out a committee of aggregators, that is a similar trust model to DPoS. In the above work, our goal was to have something closer to the trust model of Proof-of-Work, namely open for anyone to enter the system and submit information, with economic incentives for people to participate “honestly”, i.e. here to come in and provide correct answers, particularly if other have already submitted incorrect answers. (Beyond greater resistance to abuse and errors from sources, this model is particularly relevant for the property we were going for that the precision of the answer should be tunable to user needs.) That said, the price of a stronger trust model is less flexibility in what kinds of oracle questions can be answered compared to the “aggregator of a panel of sources” models.

By the way, a more polished/peer-reviewed version of this work is now available [here](http://drops.dagstuhl.de/opus/volltexte/2019/11396/).

---

**mikedeshazer** (2019-12-03):

To piggyback off of that and regarding the “Big Picture”: https://medium.com/proof-of-fintech/the-reality-stone-on-the-blockchain-accessible-to-all-1654a3ec71a7

---

**mikedeshazer** (2019-12-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/whwgeorge/48/4271_2.png) whwgeorge:

> In the above work, our goal was to have something closer to the trust model of Proof-of-Work, namely open for anyone to enter the system and submit information

This is the way to go. Let the consumer of the oracle decide who they want information from/trust. Let the consumer of information also decide whether they want an aggregated response that removes outliers, or… a trusted source’s response that’s completely centralized. From there, when people who consume a smart contract that uses oracles data (like a future’s contract that settles based on an oracle-provided price) they just need to be made aware of who or what they are trusting. In the case of the CBOE, the settlement price for the VIX and other indexes is based purely on them… and as people have entrusted them with trillions, I don’t think that model of trust based on reputation will go away anytime soon. However, they have been sued regarding being a malicious actor (https://www.reuters.com/article/us-cboe-vix-explainer/vix-wall-street-fear-gauge-manipulated-or-maligned-idUSKCN1M00I1). And those people who don’t trusted centralized sources like CBOE will probably seek an alternative when they have been wronged.

But choice for the smart contract, and being able to make that choice in a simple parameter or two of a method call, versus an entirely different implementation, is needed.

---

**mikedeshazer** (2019-12-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/whwgeorge/48/4271_2.png) whwgeorge:

> By the way, a more polished/peer-reviewed version of this work is now available here

I have added a reference to this work in the [OrFeed Readme](https://github.com/ProofSuite/OrFeedSmartContracts). Your paper is amazing work!

---

**jamesray1** (2019-12-09):

There would still be use cases for oracles in happs. Here is an example that has just started to be implemented: https://github.com/redgridone/Internet-of-Energy/blob/03c531080dba0e650830bbc513ed7210bb33a207/device%20node%20libraries/signalzome_lib.rs. I was just thinking that there may be less need for, or dependence on, token- and blockchain-based cryptocurrencies and fiat currencies. However, there would certainly be use cases where oracles for existing currencies would be desirable.

However, I suppose it will be easier to integrate oracles with happs, as one can build fully distributed apps with Holochain, and not just smart contracts running on a decentralized blockchain like Ethereum.

My point about distributing oracles, data storage, and validation/computation, network transfer and I/O is still valid, however. We need to distribute information, currency/current-see control, value flows, power, and computational resources, in order to operate as part of a more equitable, fair, democratic, just society.

It’s important to keep the bigger picture in mind, and think carefully about how problems and solutions are framed and designs are made, before getting bogged down in implementation details and technical debt.

Requiring universal consensus in order to prevent double spending does not harmonize with biomimetic software design or how nature works. Assuming this requirement results in tunnel vision for how problems are addressed, and precludes consideration of more distributed, agent-centric, scalable solutions, a la Holochain. For example, when electrons are donated or shared in ionic or covalent bonds (respectively), an atom doesn’t check with a universal electron ledger whether that electron is double spent. Here’s the source of that example: https://medium.com/holochain/beyond-blockchain-simple-scalable-cryptocurrencies-1eb7aebac6ae.

I’m happy to discuss or point to resources that discuss Holochain vs blockchain, but I will stop as I don’t want to hijack threads or talk when the words may not be received with an open, considerative mind.

Blockchains still have more potential than the centralised client-server web model, but I assert that Holochain seems to have more potential than blockchains, and others who are not working for Holo make the same assertion:


      ![](https://ethresear.ch/uploads/default/original/3X/6/4/64c131477d033e0b260a75eaedd4f97ce831b710.png)

      [sail-the-net.com](https://www.sail-the-net.com/translate/translation_of_nautical_terms.html)



    ![](https://ethresear.ch/uploads/default/original/3X/b/7/b7a7a926548c489fd2871b3d01d49ced939745d6.png)

###



Untung hadir sebagai situs slot online resmi yang sudah berlisesnsi situs slot terpercaya dari bandar slot gacor nomor 1 di dunia



    Price: USD 5.20

