---
source: ethresearch
topic_id: 12740
title: Why I dread the Merge, and why you should too
author: Janeth
date: "2022-05-29"
category: The Merge
tags: []
url: https://ethresear.ch/t/why-i-dread-the-merge-and-why-you-should-too/12740
views: 8255
likes: 41
posts_count: 44
---

# Why I dread the Merge, and why you should too

When Ethereum debuted I was a fan. I put money in The DAO expecting to lose (after all, more things could fail than succeed!) and was fascinated to watch the unfolding hack and fork.

While that fork was low risk and only contentious on philosophical grounds, it sparked a schism in the community. We survived it and the ecosystem is flourishing. Now, as we near another serious fork that is not sparked by necessity, I am not excited. The upcoming fork is motivated with two assumptions: that PoW is inefficient, and that it is slow, and so must be replaced with something that provides cheaper security and is faster. You might say, “Surely, you don’t mean to say it’s an assumption? How can something so energy hungry and with 15s block times (not fast enough for payments) not be improved??”

Over the past few years I have convinced myself of two things:

1. That PoW is the most secure consensus protocol possible, because it introduces a measure of security that is fundamental to the concept of security itself. When the situation is considered in the context of reality, there is no simple mechanism in nature that would require less energy to defend than to attack, which suggests that any proposal that makes such a claim is not likely to be correct.
2. That PoW is the fastest consensus protocol possible, because it does not require voting or any form of chatter around the agreement. Any limitation on speed stems purely from physical limitations of latency and the community’s appetite for storing the transaction history.

For point 1 I have even asked Vitalik to weigh in, and he has. He proposed that hide and seek is a simple game where it costs less to defend than to attack. This is not true, since a hider must also be active and activity (communication or physical) reveals position. An inactive hider is a dead hider. To put it in more base terms, in the realm of security the map is the territory and no trickery or violence is off the table.

For point 2 I hope the argument is easier to understand. See point 2 below.

Both points are explained in two articles:

1. On security: https://medium.com/coinmonks/blockchain-myth-5-proof-of-work-wastes-energy-a848000aea9a
Read just the TLDR to get the picture.
2. On speed: https://medium.com/@brrabski/blockchain-myth-6-proof-of-work-is-slow-8f0a4e0bca2b

I was encouraged to post this by someone. I do not expect to be able to change the minds of everyone here… Most of you are probably staking, which puts you at a conflict of interest in taking an objective look. This post is to warn of the inevitable and perhaps help explain, when things inevitably will not turn out as expected.

Feel free to challenge the propositions on their merits. Many have tried.

## Replies

**NateMarrocco1** (2022-06-04):

Interesting points. I hope to hear some rebuttals. Do you think blockchains can scale to 500k tps with sharding and starks? If not why?

---

**Janeth** (2022-06-05):

Thanks for replying. It’s an uphill battle to get engagement on this, because so many people have effectively painted themselves into a corner by depositing large sums into the staking contract. This essentially guarantees that they puke if the merge doesn’t move forward.

Blockchains will scale via L2, because that’s the only possibility.

One aspect of ZK that is a dirty little secret that no one seems to like to mention is that it is computationally difficult to generate proofs, and so to do anything complex you’ll need a small cpu farm to construct the proof (transaction) in reasonable time.

Read myth 2 in the series on how blockchains complement (but not replace) other computing architectures.

---

**Killari** (2022-06-06):

Have you tried zk tech out and generated some proofs? You can for example try zcash or tornado cash to see how you can generate proofs with just your laptop. You can also write your own circuits with Circom to see how fast you can prove them. The runtimes are not insane.

---

**Janeth** (2022-06-09):

I have tried zcash at launch and I appreciate there are now faster implementations, but it’s not so much that they’re faster now, it’s that creating transactions (proofs) is slow in principle, and so if someone wants to run lots of them it will necessarily cost a lot in CPU power. Transactions will always fill all available space and applications need to be built with that in mind.

---

**goldnutter** (2022-06-09):

It will work fine. Two more testnets ? excellent. What is the stress about… on PoW

smh… cling on to it like Bitcoin maxis and see what happens. Bitcoin needs PoW but doesn’t need to send a lot on L1. Bitcoin will be fine.

ETH will get FSS from ChainLink later in the year and could stay PoW but traffic will simply follow the rule of free market capitalism. ETH1 is already obsolete by so far. Are you actually serious…

Blockchains can already scale infinitely wake tf up pls… its just the team have no options while stuck on POW at the mercy of angry miners.

I suspect you just want to keep mining now that I am about to say…

sayonara

---

**ulrych8** (2022-06-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/janeth/48/4524_2.png) Janeth:

> there is no simple mechanism in nature that would require less energy to defend than to attack

What about keeping a private key private? Once you’ve created your private key and announced the public key the cost of attack is vastly superior than the cost of defense, wouldn’t you say?

And if this doesn’t fall in the category of simple mechanism, I’d be interested in the arguments you make to say that PoS is a simple mechanism.

Otherwise, great points, always nice to confront ideas.

---

**ricacsa** (2022-06-10):

Thanks for posting this, it is always good to have all the point of views and discuss them openly. Honestly, I believe the merge will be absolutely amazing and POS and POW will coexist in the future, so either would be smhw fine. However, in a crowded market, where people don’t care about the chain, and only about the UX, they will be channeled towards more efficient, maybe less decentralized systems, AUTOMATICALLY!

I hate to see supporters of the merge post aggressive comments against your post, it kind of makes me affraid and doubt about the merge being a good thing ;)… But anyway, imagine the future “online banking” app, connected to all L1 and routing automatically all orders through the fastes, most efficient,  most stable and secure “network (eth, avax, cosmos, dot etc…)” - The algo won’t care about POW being the most secure etc… If POW doesn’t provide the best user experience…

So even with POW, ETH may stay competitive, for a certain tranche of the users, however without being selfish, ETH should go to the merge and increase their user experience for everyone, to continue in its original spirit of inclusion, decentralization and innovation.

All the best.

---

**Janeth** (2022-06-10):

Private keys are subject to the $5 wrench attack. Very low energy to get at it unless it’s guarded with substantial force (private or state-supplied).

The key insight is that actual security cannot be modelled, because it’s based in reality itself. A model assumes that no tricks can be played. Not so in reality, where no holds are barred.

---

**Janeth** (2022-06-10):

> I hate to see supporters of the merge post aggressive comments against your post, it kind of makes me affraid and doubt about the merge being a good thing

This is worth considering. If every pro-merge believer put their ETH in a smart contract that has no withdraw function, how could they be expected to objectively evaluate if the merge might be unnecessary or harmful? Wouldn’t they be incentivised to protect their “deposit,” even if it hurts the space as a whole?

---

**Option-Panda** (2022-06-22):

I would prefer the OP approach to prevail in the future. Theoretically it’s infeasible for ZK approach to scale for general purpose computation. However, Optimistic team itself might not be able to.

---

**alanorwick** (2022-06-25):

I agree with many of your points. Sort of disagree that scaling is only feasible via L2s. We’re building Quai Network (https://quai.network) via sharded merged mined chains and the research done in the BlockReduce paper https://arxiv.org/pdf/2112.11072.pdf

Ultimately many PoS systems will succumb to KYC and AML restrictions at the block production level which will hinder the true use cases of cryptocurrencies / a lot of the ethos it is meant to represent.

---

**nickmura** (2022-06-26):

Really? What has lead you to this conclusion that KYC will be inevitable?

---

**JamesVZ** (2022-06-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/janeth/48/4524_2.png) Janeth:

> This is not true, since a hider must also be active and activity (communication or physical) reveals position.

I don’t think this is correct – the attacker is also revealing their position while actively searching, this aspect of the game provides no benefit to either the attacker or the defender if one assumes no holds are barred, which just leaves the fact that the attacker must search all available hiding spaces (i.e. anything not in view) while the defender merely needs to find one new hiding space periodically.  If you want a real life example of this playing out, read about Carlos Hathcock sniping an NVA General: [Carlos Hathcock | Military Wiki | Fandom](https://military-history.fandom.com/wiki/Carlos_Hathcock#Assassination_of_an_NVA_Commanding_General)

![](https://ethresear.ch/user_avatar/ethresear.ch/janeth/48/4524_2.png) Janeth:

> That PoW is the fastest consensus protocol possible, because it does not require voting or any form of chatter around the agreement.

I think this needs to be clarified a little more, as the article cited later in your post posits that the block must be difficult enough to find that only a few competing blocks at most can be found per cycle which leads to multiple block confirmation times, i.e. delayed consensus of the state of the chain.  “Chatter” about block validity is certainly faster than waiting for multiple difficult to find blocks.

---

**alanorwick** (2022-07-10):

PoS systems make the progression of the network too closely tied to the monetary supply. Given that most PoS chains already require KYC for obtaining coins, I can foresee a future in which governments go after block producers to enforce AML rules as money transmitters.

---

**MicahZoltu** (2022-07-10):

Just because other people have designed PoS systems that require KYC doesn’t mean that all designs of PoS systems require KYC.  Contrary to popular belief, there is a good reason why it took Ethereum so long to switch to proof of stake: It is a really hard problem to solve in a permissionless and censorship resistant way.

---

**jureor** (2022-08-26):

But PoS is less energy consuming and anyway you can always mix PoS and PoW.

Also, PoW is not the only way to insure speed. What about the InstantSend algorithm? I’m researching many coins rn and WEI for example has PoS and PoW, and the speed is insured by the InstantSend algorithm. Isn’t that kind of mixture better?

---

**alanorwick** (2022-08-26):

It’s a hard solution because it’s the wrong solution to a permissionless and censorship resistant system. As we’ve seen more recently with OFAC sanctions and the threat of slashing, PoS seems to only add scrutiny to what is being done on chain.

---

**Janeth** (2022-08-28):

Even though PoS is less energy intensive, this does not mean it’s equally secure. Quite the contrary. If you take a look at the argument in the first article cited, it basically puts out a challenge: If you can’t think of a simple mechanism, where the energy of the most efficient attack is greater than the energy used to defend a system, then what basis do you have for supposing that a complex mechanism, like PoS, could be an effective low energy defence against a high energy (law enforcement, hacking budget, violence) attack?

---

**Janeth** (2022-08-28):

Apologies for the delay in answering. I just saw your response.

On your first challenge:

The attacker isn’t defending. Assuming the attacker has overwhelming force, they do not need to hide. The attacker would need to hide only if the defender presented a credible threat. Does the defender have the energy/force at hand to effectively counterattack? If so, they must have equal energy at their disposal If not, the attacker just needs to sniff or smoke out the defender; both of these are low energy strategies.

On the second challenge:

The optimum block time is the time it takes for light to travel across the diameter of the network. In such an optimum setup chatter would always take longer.

---

**Janeth** (2022-08-28):

The fundamental value proposition of blockchain is that there is only one history. That means that it must sync to a single truth. This is an exercise that necessarily has physical limitations relative to massively parallel systems.


*(23 more replies not shown)*
