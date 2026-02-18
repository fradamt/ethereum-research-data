---
source: magicians
topic_id: 5255
title: EIP-1057 "Break Glass Moment" is here
author: CryptoBlockchainTech
date: "2021-01-27"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-1057-break-glass-moment-is-here/5255
views: 2977
likes: 28
posts_count: 12
---

# EIP-1057 "Break Glass Moment" is here

[@gcolvin](/u/gcolvin) [@Anlan](/u/anlan) [@bitsbetrippin](/u/bitsbetrippin),

It is now quite apparent that ASICs will dominate the network within the next few months. The recent rise in hash rate can be contributed to the A11 Innosilicon miner that started shipping last year and now the Linzhi Phoenix Miner is shipping in January. These miners are over 46% more efficient than the latest 3000 series Nvidia GPUs and represents a major centralization security risk.

At the [ACD#82](https://youtu.be/MOZ7_0Tb95M?t=1350) meeting it was decided to roll out EIP-1057 to testnet and be ready for implementation if needed and keep it in the “back pocket if ASICs become a concern.” In light of the new extremely efficient ASICs being rolled out, we now need to take action immediately. The longer we wait the more ASIC miners get sold, the higher risk to network security, and the more people who will be hurt if they buy them and then there is an algo change.

I have requested EIP-1057 implementation discussion to be added to the next ACD #105 meeting agenda on 2/2/2021 here: [Ethereum Core Devs Meeting 105 Agenda · Issue #241 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/241)

Here are the hard facts on ASICs as of now compared to GPU mining

**Efficiency**

Best GPU miner - 3060TI 62MH@130W - **Efficiency = 0.47 GH/W**

Linzhi Phoenix ASIC miner 2600MH@3000W **Efficiency = 0.87 GH/W**

Innosilicon A11 8GB 2000MH@2300W **Efficiency = 0.87 GH/W**

**ASIC Power Efficiency Advantage = 46% more efficient**

**Cost**

42x3060TI@ 62MH = 2604MH

42x3060TI@ $550 = $23,000

42x3060TI@ 130W = 5,460W

Linzhi Phoenix ASIC $12,900 + 25% tariff if US

Innosilicon A11 ASIC $15,500 +25% tariff if US

A GPU miner would have buy 42x3060Tis at $10K more to achieve the same hash. However as captured above in efficiency, electricity costs would be double. Ethereum network is now on a ticking time bomb of when not if ASICs will take over.

My comparison does not take into account additional costs of running 42 GPUS, from MBs to PSUs, RAM, CPUs etc. Most of us are using 8-13 GPUs per rig so this would be at least 5 rigs. Then there is the work it takes to set them up and maintain them versus plugging in a single ASIC and PSU.

**ASIC Purchase Cost Advantage = 44% lower purchase cost**

When ProgPow was being discussed Linzhi published this paper against ProgPow all the while they were developing and probably already making next gen ETHash ASIC miners. Time has a way of revealing ones intentions. https://linzhi.io/docs/LWP15-Posts-Against-ProgPoW-05092019.pdf

[Linzhi Phoenix ASIC miner 2600MH@3000W](https://linzhi.cn.com/shop/linzhi-phoenix-2600mh-s/)

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/c/c94bcc5313bd5c67d5356d6603c2f00cfadc2d82_2_690x423.jpeg)image975×599 89.8 KB](https://ethereum-magicians.org/uploads/default/c94bcc5313bd5c67d5356d6603c2f00cfadc2d82)

[Innosilicon A11 8GB 2000MH@2300W](https://innosiliconmining.tech/product/innosilicon-a11-eth-king-2100mh-8gb-april-pre-order/)

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/1/1d2ba468429a7878a02b95ada481e20aa9db6f40_2_690x420.jpeg)image1380×840 168 KB](https://ethereum-magicians.org/uploads/default/1d2ba468429a7878a02b95ada481e20aa9db6f40)

## Replies

**Amxx** (2021-01-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cryptoblockchaintech/48/2579_2.png) CryptoBlockchainTech:

> and represents a major centralization security risk

I was always under the impression that ASICs owner have absolutely no incentive to attack the network. My understanding is that, if an attack was to be successful, it would be noticed very fast, and would likely cause the confidence in ETH (and the price of ETH) to crash. ASICs owner (like all miners) make money from ETH having a high value, and if the price of ETH was to drop to much, their hardware being specific could not be repurposed (unlike GPU which have a value outside of ETH minning).

Are there arguments that would point out of miss-alignment of incentives between ASICs miners and the rest of the community ?

(Disclaimer: I am not an asic owner, I am not a miner, I’m just a simple ethereum developper & user)

---

**kladkogex** (2021-01-28):

An interesting meet-in-the-middle compromise that I mentioned in the past, would be for the network to support both algorithms (ProgPOW and  ETHash).

And then adjust difficulty separately, to guarantee that on average  50% of blocks is mined using  ProgPoW and 50% using ETHash.

---

**HostileEncoding** (2021-01-28):

(If allowed?) I’ll copy part of my post from a different thread, because I think it is relevant for the incentives that [@Amxx](/u/amxx) asks for:

> I know some of the devs here do not look favorably towards GPU miners. But when the time comes to switch to PoS you’ll be better off with a network made up of GPU miners, than a network filled with these ASIC monstrosities.
>
>
> Since other Ethash-based currencies are worthless, these ASICs would become instant paperweights. As such, ASIC miners will have every incentive to delay, derail and prevent PoS. We saw the force of the ASIC propaganda machine when they essentially killed EIP-1057 (ProgPow).
>
>
> GPU miners, meanwhile, will have other options:
>
>
> Mining a different coin.
> Selling the GPUs to gamers / creators / researchers
> Giving back by doing Folding@Home or similar.
>
>
> Especially with current EIP-1559 pushing to reduce miner profits, weeding out the (least profitable) hobby GPU miners and promoting a network of centralized ASIC dominance.

Other concerns regarding ASICs can of course be found in the Ethereum Whitepaper by Vitalik Buterin [1]:

> [on Bitcoin:]
> First, the mining ecosystem has come to be dominated by ASICs (application-specific integrated circuits), computer chips designed for, and therefore thousands of times more efficient at, the specific task of Bitcoin mining. This means that Bitcoin mining is no longer a highly decentralized and egalitarian pursuit, requiring millions of dollars of capital to effectively participate in.

And the Ethereum Yellowpaper by Dr. Gavin Wood[2]:

> One plague of the Bitcoin world is ASICs.  These are specialized pieces of compute hardware that exist only todo a single task (Smith [1997]).  In Bitcoin’s case the task is the SHA256 hash function (Courtois et al. [2014]).  While ASICs exist for a proof-of-work function, both goals are placed in jeopardy.  Because of this, a proof-of-work func-tion that is ASIC-resistant (i.e.  difficult or economically inefficient to implement in specialised compute hardware)has been identified as the proverbial silver bullet.

Where Wood refers to ASICs jeopardizing the two design goals of Ethereum’s PoW:

> Firstly, it should be as accessible as possible to as many people as possible.  The requirement of, or reward from, specialized and uncommon hardware should be minimized.
>
>
> Secondly, it should not be possible to make super-linear profits, and especially not so with a high initial barrier.

Both of which are in danger since the above mentioned ASIC:

1. Is highly specialized, generally inaccessible
2. Provides super-linear profits over current GPUs with an enormous initial barrier: hard to obtain, and $15000.

[1] [Ethereum Whitepaper | ethereum.org](https://ethereum.org/en/whitepaper/)

[2] https://ethereum.github.io/yellowpaper/paper.pdf

---

**souptacular** (2021-01-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cryptoblockchaintech/48/2579_2.png) CryptoBlockchainTech:

> I have requested EIP-1057 implementation discussion to be added to the next ACD #105 meeting agenda on 2/2/2021 here: https://github.com/ethereum/pm/issues/241

I have responded here: [Ethereum Core Devs Meeting 105 Agenda · Issue #241 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/241#issuecomment-769444358)

---

**greerso** (2021-01-30):

Those are old arguments rented hash attacks are hardware agnostic and the attacks we’ve seen do not reduce the value of the attacked networks in a significant way.

The real problem here is that there are at least 5 efficient ethash ASIC’s been available to enterprise for a year or more now, not available retail.  The risk is centralization of hash.  An attack doesn’t have to look like a double spend against an exchange.

---

**CryptoBlockchainTech** (2021-02-02):

Here is some additional data showing ASICs are now actively ingaging in a network attack RIGHT NOW.

F2Pool is known for hosting the majority of ASICs. This is about the best proof we have that ASICs are a threat to the network. Unfortunately the devs still only think in terms of 51% attack instead of an attack like this that goes unnoticed.

[![Screenshot_20210202-104018_Brave](https://ethereum-magicians.org/uploads/default/optimized/2X/5/556c3e14ea604d851ef26609b7ee2f9c499f528f_2_690x450.jpeg)Screenshot_20210202-104018_Brave1275×833 98.2 KB](https://ethereum-magicians.org/uploads/default/556c3e14ea604d851ef26609b7ee2f9c499f528f)

https://t.co/pkuSnEnug2?amp=1

---

**lmaonade80** (2021-02-02):

Unfortunately, while I am optimistic, I think the best chance EIP1057 had of passing was before. Now, the argument will be “we are too close to phasing out PoW entirely.” I fear most devs lump ASIC and GPU miners into one basket, and don’t really see the difference.

From a development perspective, I think the difference is that GPU miners are happy to move with the ecosystem. We are generally disorganized and have accepted reduction in block rewards, ETH2 developments, and embraced the “Minimum Viable Issuance” strategy without much of a peep. We understand PoW on ETH is ending ™, but we can carry on elsewere and we would wish ETH the best in their new direction. However, specifically anti-ASIC proposals face organized opposition with EIP1057 and now EIP1559. I don’t believe this is a coincidence.

If there is no community will now to remove ASIC’s from Ethereum, the chances of removal dwindle by the day, as more ASIC’s are put forth until we find ourselves in a BCH-like schism like Bitcoin dealt with a few years back. This set Bitcoin back years and spawned many more alternative coins where that capital likely would’ve remained in BTC. I hope we don’t have to deal with something as similarly dramatic. Everyone is trying to be the ETH killer today.

---

**CryptoBlockchainTech** (2021-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lmaonade80/48/2816_2.png) lmaonade80:

> Now, the argument will be “we are too close to phasing out PoW entirely.”

This same argument can be made of 1559 that will make ASICs dominate Ethereum completely. We will use this against 1559 proponents and push to implement 1057 in the same fork.

---

**lmaonade80** (2021-02-03):

Well, I actually disagree that the same argument works considering mining and therefore progpow is moot after ETH 1.x and many mechanisms from 1559 will live on in ETH2 chain.

But I otherwise agree with your more overall assessment of the unintended consequences of EIP 1559 when coupled with unaddressed and growing ever more powerful ASIC’s on the network.

---

**CryptoBlockchainTech** (2021-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lmaonade80/48/2816_2.png) lmaonade80:

> Well, I actually disagree that the same argument works considering mining and therefore progpow is moot after ETH 1.x and many mechanisms from 1559 will live on in ETH2 chain.

The fact that the entire yellow paper that Ethereum was founded on explicitly calls out ASICs as a “plague” and the developers did NOTHING as POW sunsets while ASICs gain over 90% hash will have long lasting consequences. Consequences that show developers were unwilling to stand for something so simple as what they were founded on.

Yes 1559 will be carried into 2.0 but will be quickly changed when stakers pay developers to give validators the fees instead of burning them as this was only for miners, not stakers.

---

**CryptoBlockchainTech** (2021-04-26):

Yet another ASIC miner has been announced, this one from BitMain.

This will be the most efficient ever with 3GH @ 2556W, or **1.17 MH/W**. This is now 2.5x more efficient than the best GPUs @ 0.47MH/W

[Bitmain Antminer E9 Ethereum ASIC](https://videocardz.com/newz/bitmain-antminer-e9-ethereum-asic-is-as-powerful-as-32-geforce-rtx-3080-graphics-cards)

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/6/61836085b54fa4cfb3a0d6f416c8efd53d928bff_2_690x211.jpeg)image1101×337 88 KB](https://ethereum-magicians.org/uploads/default/61836085b54fa4cfb3a0d6f416c8efd53d928bff)

It is now safe to say that Ethereum will be 100% ASICs when the attempt to move to POS will be made. I am really not sure why so much effort is going to go into forcing a switch to POS by ASIC miners when the simplier solution is to just make an algo change ASAP and GPU miners will welcome POS as we have always stated we would.

