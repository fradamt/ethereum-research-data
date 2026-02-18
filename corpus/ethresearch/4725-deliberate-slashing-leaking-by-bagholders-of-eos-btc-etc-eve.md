---
source: ethresearch
topic_id: 4725
title: Deliberate slashing/leaking by bagholders of EOS, BTC, ETC, even ETH
author: projectoblio
date: "2019-01-02"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/deliberate-slashing-leaking-by-bagholders-of-eos-btc-etc-even-eth/4725
views: 2095
likes: 7
posts_count: 7
---

# Deliberate slashing/leaking by bagholders of EOS, BTC, ETC, even ETH

Slashing/leaking in POS opens up the network to an attack vector that I can’t wrap my head around. This attack is basic and common, but it’s only possible in production and can’t be tested for in development.

- Cryptocurrency holders of EOS, BTC, BCH, and ETC will DDOS Eth staking pools and nodes. They achieve short-term results in these attacks. These attacks are already common in cryptocurrency, but with the added benefit of slashing/leaking having an effect on people’s coins, they will be a lot more common in ETH POS.
- Bagholders of ETH will want to maximize their ETH interest rate. They’ll quietly DDOS a small percentage of nodes over a time period. As these nodes lose confidence in POS, they’ll quit and won’t stake again, leading to more returns for the bagholders in the long-term. This is especially true because the number of staking nodes is likely to rise up to a point where staking is unprofitable, so now if average users are also are being randomly DDOS’d and losing coins, they’ll be even less likely to stake.

This second bullet is basically the equivalent of Starbucks buying up 1,000 of cafes over these 10 years and cutting their prices. When no more cafes exist in an area (they’ve gone out of business), Starbucks raises their prices up to higher than what they were before they moved in.

More technically, imagine the following attack vector:

One of the many people with incentives to deliberately slash goes to a popular staking pool. They locate the ~25 IP addresses which stakers are supposed to connect to. They then run a prolonged, 7 day DDOS on these IP addresses. This causes a pretty large impact on the Ethereum network.

**What worries me most** about this attack is [1] how cheap it is to repeatedly DDOS (e.g. versus printing ASICS), [2] how other POS/POW coins don’t have this problem because they don’t use slashing/leaking (these coins are already DDOSed often, without the benefit to the attacker that comes with slashing/leaking), and  [3] how many wealthy and powerful people have the incentives to perform them. This attack really can be done in a lot of different ways other than DDOS, in the linked stackexchange post you’ll find more. These types of attacks are only possible due to inactivity leaking in Eth’s POS algorithm.

The attached post goes into more details on the long-term effects of slashing/leaking, specifically how over time, the structure incentivizes a single corporation to run the entire process protected by a propietary anti-DDOS structure.



      [ethereum.stackexchange.com](https://ethereum.stackexchange.com/questions/64871/deliberate-slashing-dont-slashing-and-leaking-incentivize-ddos-attacks-on-smal)



      [![nick carraway](https://ethresear.ch/uploads/default/original/3X/0/0/00a8180c0539d12e14b9188ca716fa557c3d4d96.jpeg)](https://ethereum.stackexchange.com/users/3172/nick-carraway)

####

  **proof-of-stake, network, casper, proof-of-work**

  asked by

  [nick carraway](https://ethereum.stackexchange.com/users/3172/nick-carraway)
  on [04:21PM - 01 Jan 19 UTC](https://ethereum.stackexchange.com/questions/64871/deliberate-slashing-dont-slashing-and-leaking-incentivize-ddos-attacks-on-smal)

## Replies

**haokaiwu** (2019-01-02):

[discouragement.pdf](https://raw.githubusercontent.com/ethereum/research/master/papers/discouragement/discouragement.pdf)

Linked from the thread about ETH incentives. This paper was written by Vitalik about “epsilon attacks.” The gist is basically what you describe in your post.

The already-implemented mitigation is to reduce the reward for taking stakers offline. This is why we don’t use a flat issuance rate for the network (e.g. 1% inflation) in the current spec, rather one dictated by the inverse square root of the amount staked. It reduces the rewards for taking a portion of the network offline.

Beyond that, I don’t believe staking changes the fundamental risk dynamics. Availability issue already costs money for PoW miners (electricity costs, depreciation of hardware, etc.). Theoretically, the same type of attack is possible, yet we haven’t seen it happen between miners. Yes, slashing may increase the potential losses for losing availability, but it solves other issues such as the “nothing-at-stake” problem, which make PoS unviable otherwise. Given that things like sharding would be next-to-impossible without Proof-of-Stake, it’s a tradeoff that protocol designers seem happy to live with.

Also, the attack you describe above also assumes that the IP addresses of stakers can readily be identified. As far as I know, the hacker would have to track these down one by one and then coordinate an attack on a sufficient proportion. Given that validator clients can be run from anywhere on cheap consumer hardware, tracking down small fish may not be so easy. Also, given that DDOS attacks are already a feature of the existing market, centralized entities should already have experience with developing countermeasures.

Here, we see a classic centralization tradeoff. You can trust your ETH to a pool or entity like Coinbase, but you have to also trust their security protocols against this class of attack. As you point out, these pools are high-value targets, and hackers could conceivably find out how much each pool is “worth” from a staking standpoint.

Separately, you can stake the ETH yourself and not expose how much your ETH you stake. Hackers targeting small fish would have to track down a very large number of IP addresses to make a noticeable impact. However, once your IP address gets marked as a staker,  it’s unlikely you’ll be able to weather a DDOS on your own. You can take steps like changing your IP address though or using a service which masks it.

Of course, I’m not an expert hacker, so it might be easier to find IP addresses than I’m imagining. It just seems that we’re assuming away a critical part of what makes this attack viable.

---

**lookfirst** (2019-01-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/haokaiwu/48/2969_2.png) haokaiwu:

> Availability issue already costs money for PoW miners (electricity costs, depreciation of hardware, etc.). Theoretically, the same type of attack is possible, yet we haven’t seen it happen between miners.

In PoW, it is more like one pool attacking another pool. If you can force miners off of a competitors pool and onto your pool, you gain hashrate and thus rewards. Booting miners off a pool is pretty easy (simply enact the competitors pool anti-DDoS measures for specific accounts), but knowing what the accounts failover configuration is, is much harder.

---

**jochem-brouwer** (2019-01-03):

I have a weird, random idea which I’m sure has been proposed in the past to mitigate DDOS attacks.

What if we let people who request ANYTHING from a node do proof of work? Letting someone solve a hash challenge which requires 100 attempts on average will lower the DDOS volume by a factor 100? I haven’t thought of the implementation though since I guess the node can still be attacked by just sending random solutions…

---

**LRonHubs** (2019-01-03):

If you read early Satoshi’s emails, this is actually the first use case he proposes for Bitcoin, outside the double spend problem. Albeit, he talks primarily of using it to mitigate email spam.

---

**MihailoBjelic** (2019-01-05):

I think [@haokaiwu](/u/haokaiwu)’s answer covered pretty much everything.

This is particularly interesting IMHO:

![](https://ethresear.ch/user_avatar/ethresear.ch/haokaiwu/48/2969_2.png) haokaiwu:

> Here, we see a classic centralization tradeoff. You can trust your ETH to a pool or entity like Coinbase, but you have to also trust their security protocols against this class of attack. As you point out, these pools are high-value targets, and hackers could conceivably find out how much each pool is “worth” from a staking standpoint.
>
>
> Separately, you can stake the ETH yourself and not expose how much your ETH you stake. Hackers targeting small fish would have to track down a very large number of IP addresses to make a noticeable impact.

What’s interesting is that now you have a choice - you can “join the pool” (i.e. delegate your tokens to a large validator) or you can run your own validator (in this case your rewards/revenue will even be slightly higher since there’s no large validator’s rent). In PoW, 99% of miners effectively/practically don’t have a choice - they simply need to join a pool (if they decide to mine on their own it’ll take them hundreds of years to get lucky and mine a block ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)).

I believe this is an important thing, both for mitigating this particular attack and for keeping the mining decentralization level high (important for mitigating a number of other attacks).

---

**projectoblio** (2019-02-04):

I have been thinking about this alleged “nothing-at-stake” problem. I think it would be great if we could identify the best chain in a decentralized way as fast as possible. But taking people’s coins away is only going to speed-up the process of centralization.

