---
source: ethresearch
topic_id: 4566
title: Exploring Worst Case Scenarios in ETH 2
author: jrhea
date: "2018-12-12"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/exploring-worst-case-scenarios-in-eth-2/4566
views: 5838
likes: 23
posts_count: 13
---

# Exploring Worst Case Scenarios in ETH 2

The economics of staking has been a hot topic lately.  [@econoar](/u/econoar) has done a good job putting the incentives in concrete terms for everyone to digest.  See his post on [Economic Incentives for Validators](https://ethresear.ch/t/the-economic-incentives-of-staking-in-serenity/4157) and [@vbuterin](/u/vbuterin)’s post on [Average-case improvements to reduce validator costs](https://ethresear.ch/t/suggested-average-case-improvements-to-reduce-capital-costs-of-being-a-casper-validator/3844) for some background.  In this thread, I want to encourage people to explore the improbable worst case scenarios that could cause the protocol to fail.

## A plausible scenario

We all want to believe that Ethereum 2 will be wildly successful.  One certainty that comes with success is mainstream adoption, institutional investors, new financial products, etc.  This is great, but with it comes the very real possibility that entities that hold (or have access to) large sums of ETH will want to earn interest off of it.  We know that Coinbase, Binance, etc hold large sums of ETH in their dungeons.  It is logical that they will decide that they want to dedicate some percent of the ETH that they are holding to staking.  In fact, I am sure they are already talking about it.

That virtually guarantees that we will have a healthy amount of ETH to secure the chain.  This sounds great, right?

Not so fast.

## The problem

Entities controlling large sums of ETH represent a existential threat.

## Wait. Why is this an issue?

This demonstrates a plausible scenario that could compromise the security of the network if one entity controls more than 1/3 of the stake.

## Is there any hope?

Of course.

The point I am trying to make is that we should talk through these scenarios and simulate different ingress and egress distributions to see how the protocol is affected.

## Final Thoughts

There are a lot of brilliant people working on different aspects of these problems, but I am disturbed at people’s hesitation to share (even on this forum) until they have had their ideas peer reviewed and formally written up.  We need to get over this fear of being wrong and be more willing to receive constructive criticism.

On that note…if anyone has already worked out a solution, ( or if I am just flat out wrong ), then please let me know.  I am curious to hear the explanation.

## Replies

**cleanapp** (2018-12-12):

Absolutely correct line of thought. Another thing that our small crew of law people is working on are various legal attack vectors that can be used by and/or against validators to essentially lock up staked funds, or otherwise put a cloud on their title. This can have an opposite worst case effect to the one you describe here in that it essentially forces validators to keep their stake, which is sub-optimal from the perspective of the validator.

Relatedly, the same off-chain legal processes that can enjoin validators from removing funds can theoretically be used to force validators to remove staked ETH. The worst case scenario here is a legal removal order (injunction, seizure, forfeiture, choose your poison …) that conflicts with the protocol, which leads to an outright governance conflict. Off-chain governance norms require one thing; on-chain governance protocols require another thing.  That’s a disaster waiting to happen.  No way to anticipatorily code around it, so the only way to prepare for it is to … prepare for it.

Working on an analytical piece right now, *The Legal Structure of PoS Blockchains*. The intercourse between exchanges, validators, devs, and users is central to that story, in manifold ways. If there are issues that you think are priority areas that should be addressed, pls share what you think those are.

---

**jrhea** (2018-12-12):

> The worst case scenario here is a legal removal order (injunction, seizure, forfeiture, choose your poison …) that conflicts with the protocol, which leads to an outright governance conflict.

Thank you for sharing this.  Good to know that this is being looked at.

> Working on an analytical piece right now,  The Legal Structure of PoS Blockchains . The intercourse between exchanges, validators, devs, and users is central to that story, in manifold ways.

Brilliant.  I would love to read this when you are ready to share.

> If there are issues that you think are priority areas that should be addressed, pls share what you think those are.

I will (and hopefully others) think about other issues that need to be considered and post them here.  I have to admit that the legal aspect of this caught me off-guard.  It sounds obvious now that you mention it, but I just hadn’t entertained that line of reasoning.  I will think on this more.

---

**jrhea** (2018-12-12):

[@cleanapp](/u/cleanapp) did you happen to see this?


      [github.com](https://github.com/ethhub-io/ethhub/blob/1d9c3f6f280eab1fc78fbb84506f6c3e10971173/other/ethhub-cftc-response.md#17-how-would-the-introduction-of-derivative-contracts-on-ether-potentially-change-or-modify-the-incentive-structures-that-underlie-a-proof-of-stake-consensus-model)




####

```md
# EthHub CFTC Response

On December 11th, 2018 the CFTC [submitted a public "Request for Input"](https://www.cftc.gov/sites/default/files/2018-12/federalregister121118.pdf) which asks for clarity and answers around Ethereum. The following is a list of all questions asked in the RFI. The following answers were developed on EthHub, an open source, community run information hub for the Ethereum community.

_**From the CFTC: In providing your responses, please be as specific as possible, and offer concrete examples where appropriate. Please provide any relevant data to support your answers where appropriate. The Commission encourages all relevant comments on related items or issues; commenters need not address every question.**_

DEADLINE: February 9, 2020

## Purpose and Functionality

### 1. What was the impetus for developing Ether and the Ethereum Network, especially relative to Bitcoin?

It's first vitally important to distinguish between Ether and Ethereum. Ethereum is an open-source, blockchain-based computing system. Leveraging smart contract \(scripting\) technology, anyone is able to build and deploy decentralized applications on top of Ethereum. This is very attractive for development because you are able to create programs that run exactly as programmed, trustlessly and with no down time.

Ether is the fundamental cryptocurrency used on the Ethereum network. It is used to compensate miners \(and potentially staked validators upon completion of a planned transition to a Proof of Stake mechanism known as Casper\) for securing transactions on the network. Ether also has many other use cases such as money, store of value and value transfer.

The underlying impetus to develop Ethereum and consequently Ether, was to utilize aspects of the technology initially developed as part of the Bitcoin blockchain and combine it with the capabilities of smart contract technology. The idea was that this marriage would lead to a platform that could sustain not only the money or medium of exchange use case, but also to add programability to money, introducing conditional logic to the equation that would open up a world of possibilities with regards to decentralized financial applications and products, and additional decentralized applications. This is contrary to the singular purpose vision for Bitcoin as a simple store of value \(pivoting more recently from the original peer-to-peer electronic cash vision championed by Satoshi Nakomoto\) and ultimately made necessary by a lack of flexibility in the Bitcoin protocol's scripting language. This was in response to the aversion to adding new features by the core maintainers of the Bitcoin protocol, such as those required to enable Ethereum-like functionality on Bitcoin.

### 2. What are the current functionalities and capabilities of Ether and the Ethereum Network as compared to the functionalities and capabilities of Bitcoin?

```

  This file has been truncated. [show original](https://github.com/ethhub-io/ethhub/blob/1d9c3f6f280eab1fc78fbb84506f6c3e10971173/other/ethhub-cftc-response.md#17-how-would-the-introduction-of-derivative-contracts-on-ether-potentially-change-or-modify-the-incentive-structures-that-underlie-a-proof-of-stake-consensus-model)








You might have some good input

---

**cleanapp** (2018-12-12):

Thank you so much for sharing.  Yeah – saw this come across the [wire earlier](https://medium.com/cryptolawreview/ummmm-hate-to-break-it-to-you-but-cryptolovers-should-have-not-used-legacy-legal-concepts-and-fbb632c10b76). Will be preparing a response for sure on behalf of the CleanApp Foundation, given the enormity of the stakes. As it comes together, will definitely post drafts and welcome any and all suggestions for improvement.

---

**collinjmyers** (2018-12-19):

Would also love to read your work on the legal implications of POS.

---

**jrhea** (2018-12-20):

Another scenario to consider is the possibility of turning the beacon chain, pow chain into microservices.   This could become a serious centralization concern. These microservices would be a great value to validators that want a light weight setup. It is also very likely to be implemented by organizations with large amounts of ETH to stake. If they can connect N validators to a single beacon chain or to a reverse proxy that load balances connections to beacon chains, then we are arguably in the same boat we are today with mining pools

---

**MihailoBjelic** (2018-12-21):

Thanks for starting this discussion.

![](https://ethresear.ch/user_avatar/ethresear.ch/jrhea/48/1406_2.png) jrhea:

> In order to ensure the security of the network, 2/3 (or more) of the validators must have an uptime >= the weak subjectivity period. If I am not mistaken, this is why we impose a withdrawal delay on validators.

I thought the purpose of these delays is to enable us to slash the validator if any malicious activity from the past is detected after she decided to withdraw?

Speaking of the problem of mass validator exits:

If we have 1024 shards, then we need (I believe) ~150,000 validators to be sure the system is secure (under the honest majority model) and operates smoothly. What happens if this number drops to e.g. 50,000? Does the shards just have to wait more to cross-link (something kind of equivalent to PoW main chain clogging), or…?

---

**nisdas** (2018-12-21):

Hey [@jrhea](/u/jrhea), thanks for starting this discussion.

So currently with the parameters we have in the event of a mass exit, it would take ~3.3 months in the average case for a validator to successfully exit, this should solve any weak subjectivity concerns given that the last finalized checkpoint would most likely be before the validator exits.

The current spec elaborates on it here:

https://github.com/ethereum/eth2.0-specs/issues/91

[@MihailoBjelic](/u/mihailobjelic)

In that case the committee size would re-adjust to account for the drop in the number of validators. Although with 50,000 validators you would get an average committee size of 50. The minimum safe threshold for committee sizes is 111, so I would guess in an extreme case like this you would have multiple commitees attesting to the state of a shard which would lead to a longer finalization period for crosslinks. Although this case hasn’t been really elaborated elsewhere

---

**MihailoBjelic** (2018-12-21):

Thanks [@nisdas](/u/nisdas).

![](https://ethresear.ch/user_avatar/ethresear.ch/nisdas/48/250_2.png) nisdas:

> The minimum safe threshold for committee sizes is 111, so I would guess in an extreme case like this you would have multiple commitees attesting to the state of a shard which would lead to a longer finalization period for crosslinks.

I don’t think it makes sense to reduce the committee size below the 111 validators/shard threshold, because committees basically become “useless” then. Instead, I would lock the committees size once they reach the threshold and then start to assign the same committee to multiple shards. That could do the job unless the drop is really extreme (validators hardware requirements are relatively low so we can’t expect the same committee to validate 10 shards at the same moment). This deserves more formal and in-dept analysis IMHO.

---

**jrhea** (2018-12-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> I thought the purpose of these delays is to enable us to slash the validator if any malicious activity from the past is detected after she decided to withdraw?

Sorry for the delay. Ya, I believe that they are both true.  Here is a VB quote from another thread:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png)[Suggested average-case improvements to reduce capital costs of being a Casper validator](https://ethresear.ch/t/suggested-average-case-improvements-to-reduce-capital-costs-of-being-a-casper-validator/3844/4)

> the security of the system depends on the withdrawal time of the lowest 1/3

---

**MihailoBjelic** (2018-12-23):

Thanks [@jrhea](/u/jrhea), you’re right, both are definitely true.

---

**cleanapp** (2019-02-27):

Hi – it took much longer than anticipated (and still not done), but here is the first part. You’ll see that it’s laying the groundwork for the next part of the puzzle, which will be analysis of the legal status of bETH (as well as the contract-ish linkages between stakers and other network participants).  But hopefully it is constructive and helpful.

https://medium.com/cryptolawreview/legal-frameworks-for-pow-pos-79d57c8fbca9

