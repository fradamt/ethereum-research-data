---
source: magicians
topic_id: 1050
title: Final Request From the GPU Mining Community
author: CryptoBlockchainTech
date: "2018-08-14"
category: EIPs
tags: [core-devs, mining]
url: https://ethereum-magicians.org/t/final-request-from-the-gpu-mining-community/1050
views: 6472
likes: 27
posts_count: 32
---

# Final Request From the GPU Mining Community

I listened to the conference call a few days ago and would like to provide the input that you solicited during the call as a large Ethereum miner (+500 GPUs). I know you are trying to strike a balance to ensure the miner community accepts the mining reward changes and difficulty bomb. I have a solution that I think would make this a lot easier.

To be quite honest most GPU miners are now barely breaking even after electricity costs due to the current state of the market and increased ASIC mining pushing up difficulty. Any reduction in rewards without a likewise reduction in difficulty would leave only ASICs on your network. I think I can speak for the mining community by saying we would be extremely open to outright reductions in rewards with the difficulty bomb reward removal if you were to include an anti ASIC POW mining algorithm change simultaneously. We know once ASICs are off the network we will again be on equal footing with other fellow GPU miners and profits should resume to where we are not mining for a loss.

I realize Anti ASIC POW change was part of an EIP a few months back but you never finished the work but did agree it would need to be part of a fork with other EIPs. It seems this would be the best time to implement a POW algorithm change along side the reward reduction and difficulty bomb removal. I know you would hands down win over the mining community if you finally took serious the amount of profits ASICs are costing the community and forked them off.

One last thought. I participate in a lot of wall street conference calls and your hesitation and lack of urgency to roll out PoW/PoS with Casper FFG ahead of Devcon 4 curtailed a lot investment enthusiasm. It is at this moment in time that your team should double down and pour every last scrap of energy into ensuring Ethereum can complete the goals they have committed to this year. Since the 7/13 call when you talked about delaying until 2019, the ETH/BTC pair has lost 40%. It is now that the community needs to hear your enthusiasm and commitment to work day and night to accomplish your goals this year even if it means DEVCON 4 gets missed by your team.

## Replies

**jcyr** (2018-08-14):

At what point, given current market trends, does it become unprofitable to mine Eth? ASICs are not far behind. ASICs for Eth only provide a slight watt per hash advantage over GPUs.

---

**CryptoBlockchainTech** (2018-08-14):

Excellent question. It depends on the size of your mining farm from hobbyist to professional. The hobbyist are less efficient and become less profitable first, ETH was started to appeal to the hobbyist miners. The professionals have a longer term outlook and will mine for a period of time at a loss if there is continued progress in the community for the coin they are mining.

The question though about GPU miner profitability vs ASIC is difficult to answer without knowing the number of ASICs on the network. Most of us that have large operations feel the numbers could be as high as 30% of the hash rate are ASICs. If we are correct Ethereum should want to protect the GPU miners at 70% of the hash versus the minority at 30% of the hash. The GPU miners are at a tipping point and once they leave the project, ASIC miners will be impossible to get rid of as their economies of scale will never let GPUs back in at a profitable rate.

---

**BsDum** (2018-08-14):

Public announced Bitmain ASIC, the E3, is about 10% to 20% more efficient than an average GPU mining rig - 200mhs at 760w.

However, the pressing concern is the Innosilicon A10, fabricated using Samsung 10nm process with a spec of 485mhs at 850w - about 150% more efficient than even the best tuned GPU mining rig.

These ASICs are already in deployment, and would begin mass shipping first week of September.

The worst part is, these ASICs are priced competitively relative to GPU rigs - $3,000 USD.

Effectively, an A10 ASIC is equivalent to the performance of 2.6 best-tuned GPU rigs, at the price of 2 GPU rigs, and at 50% of the operating costs.

I may not speak for my fellow miners, but a reduction in issuance is an understood and welcomed development direction, provided that we also have a solution to the ASIC problem.

All we need is a stop-gap solution to bar ASICs out, even if temporarily, as long as the solution lasts long enough to propel us through the issuance reduction, into Shasper.

My greatest fear is that if we don’t have an answer to the ASIC problem, come issuance reduction time, we’ll lose a significant number of GPU miners, be left with a less secured (less overall hash rate) chain, and very centralized hash rate sources.

Coupled with deteriorating overall price sentiments, we might be opening doors to potentially hostile counterparty actions, such as 51% double spend attack on prominent exchanges, or worst, a direct 51% attack to topple everything we love and built atop of us.

I hope my doomsday scenario never come to be.

---

**jcyr** (2018-08-14):

With the market trending to 0, much of this is moot.

---

**BsDum** (2018-08-14):

Saddening, isn’t it?

---

**AtLeastSignificant** (2018-08-14):

There will always be miners.  If it becomes so unprofitable that 50% of miners leave, the difficulty will drop and the remaining 50% will be in profit again.  That’s just the way this works - there’s never a risk of the network going offline due to lack of miners because it will *always* be profitable at some point.

Additionally, development does not depend on the market. At all.  Changes to the protocol will happen when they are ready, no sooner, and you’re never going to convince core devs to work faster/harder than they already are by pointing at the price of Ether.

If you want to make a compelling argument to devs, you need to talk about the security of the blockchain and have actual data to back up your claims.  Is there a legitimate threat of 51% attack *right now*?  Will there be at some point in the future if we let ASICs continue to dominate mining?  There is a lot of historical evidence on the Bitcoin side of things, as well as a lot of economic/game theory, that would suggest that this is not an issue for anybody except you as a GPU miner.

---

Personally, I consider ASIC mining to be against the elusive “Ethereum Philosophy” because anti-ASIC efforts were part of the original spec of the protocol.  It still is, and it still works.  However, it would be naive to ignore the fact that better hardware is coming out and it is not as accessible as a GPU, which ultimately leads to the same effects as having ASICs on your network.

Here’s the real issue though, there are too many possible solutions. Do we:

• Work on the transition to PoS to eliminate ASIC *and* GPU miner problems

• Work on anti-ASIC mining protocols in conjunction to issuance/difficulty bomb changes

• Try to ignore “ASICs” because they aren’t actually ASICS, just better hardware than GPUs, in order to maintain that the current algorithm is indeed ASIC resistant

Each of these have about 3-5 sub-options to them, and there will never be a 100% consensus on which to do.  IMO, if the network isn’t under threat of immediate 51% attack, then efforts should be only towards scaling/PoS, not worrying about whether or not miners are making money. That really isn’t very important to the network.

---

**jcyr** (2018-08-14):

I think you miss the point. I was just pointing out the futility of it all if there is no value in the coin. It matters little how efficient you are, or the size of the block reward,

---

**CryptoBlockchainTech** (2018-08-14):

I agree with your point and maybe I can help clarify for others. There is both a perceived value and an actual value to a coin. One is factual (actual) and the other is based on future potential (perceived). As someone else pointed out, it is not the job of the development team to enhance the actual value of the coin. However their contributions and delivery on foundation milestones play key roles into shaping the perceived value of the coin. These perceptions can directly influence the value of the coin, whether they are real or imagined.

This is why I included the final thought above. We are at a crossroads in crypto where perceived value is out of flux with actual value in a lot of coins, most are wrong and too high and some are too low. Now is not the time to lose focus and fall back on commitments.

---

**AtLeastSignificant** (2018-08-15):

If you believe “there’s no point”, then why be here making a comment about it at all?

---

**AtLeastSignificant** (2018-08-15):

The “actual value” is completely intangible. It varies from person to person.  The “perceived value” is what is reflected in the market.

It is absolutely the job of developers to increase the “actual value”, because development on a project *should increase the stability, utility, function, scope, etc.* of the project.   That inherently increases the actual value of the platform/coin.

It is *not* the job of developers to increase the market value of a coin though, but they are free to do that if they want.

This means that developers have zero obligation to miners, whose costs are very much real and paid for in fiat currency.  Miners by definition liquidate their mined tokens to fiat immediately, and those who choose to hold the token are still miners, but they are now also investors/traders and it is their responsibility to remain profitable in that situation - just like every other investor/trader.

As long as the block reward * fiat value of coin is high enough for *enough* GPU miners to be profitable (not all, just enough to meet the minimum required to secure the network, it’s impossible to create a static inflation rate that always guarantees all miners are profitable because that is a function of difficulty too), then there is no need to increase the inflation rate.

There is also very little need to actually decrease the current inflation rate.  It’s very comparable to nearly every other crypto, but people forget that because they use the fiat dollar amount to talk about inflation, which is completely absurd.

---

**alberreman** (2018-08-17):

Where are you getting the $3k figure? I’m seeing the A10 for about $5,600, which would make it a much less competitive product. Or am I misunderstanding what you’re saying?

---

**BsDum** (2018-08-17):

That’s the quoted price I got from my local supplier inclusive of duty and shipping. I’m in Asia though, so there’s that.

Edit: you’re right. I checked the price again from the local supplier, it seems the price has been bumped up to around $5,500 for the 485mh model.

---

**CryptoBlockchainTech** (2018-08-17):

Yeah it is quite apparent from where I sit, being a long term Ethereum miner and investor, that the developers need to take action this year on something. In April they did not want to do a separate fork to remove ASICs due to Constantinople being released this year. If the developers delay Constantinople like they talked about then they will have no reason not to get this small fork done by December. Surely they can get this done with the pressure off the table to get Constantinople released.

---

**AtLeastSignificant** (2018-08-20):

Being a long term miner and investor does not make your opinion more valid.

The developers don’t “owe” you anything.

Many developers *do* support a fork to improve ASIC resistance, but wanting something and having a technically feasible solution that everyone agrees on are two very different things.

There are many reasons why a new ASIC resistance protocol change should not happen by December, or even at all.

I strongly urge you to research what ASIC resistance is, the currently available “ASICs” that are on the market, how they work, and then return with a protocol that you believe will be an upgrade that makes the desired changes you want.  If you can not or do not want to do this, then your opinion on the matter is the same as every other person who isn’t doing this.

---

**CryptoBlockchainTech** (2018-08-22):

Wow so hostile. Please review the Ethereum Devs Meeting where they said they were looking for the opinions of the mining community on the three competing EIPs to delay the difficulty bomb and/or reduce the block rewards. I never stated my opinion matters more than anyone else or that the developers owed me anything, they are reaching out to us. I am just giving my opinion and supplying background to support my perspective. I also put a post on Reddit and YouTube asking other miners to come here to give their feedback.

You might want to try taking long walks outside so you can step back, relax, and enjoy life more. Sorry you are always so upset, life is to short.

---

**AtLeastSignificant** (2018-08-23):

You’re confusing being logical and impartial with anger.  If it really comes off that way, perhaps it’s because it’s a truth you’re simply unwilling to acknowledge.

Regardless, you definitely *do* seem to think that being a miner and investor is somehow relevant to your opinion because you keep mentioning it.  It doesn’t matter.  That’s just a fact, and “facts don’t care about your feelings”.

All that matters is whether or not *you* are actually developing a solution, or if you can present substantiated arguments for or against specific decisions.  If you cannot, then you are noise.  There is already too much noise.

---

**jcyr** (2018-08-23):

Unless you are developing a solution it is noise? Much of what is said here then is noise!

---

**atlanticcrypto** (2018-08-23):

EIP-1295 presentation here:

[tinyurl.com/ycjec3no](http://tinyurl.com/ycjec3no)

---

**AtLeastSignificant** (2018-08-23):

Yes, you are a prime example of noise in this discussion.  If the signal to noise ratio degrades here as it has on reddit, i would expect nothing other than for these discussions (and ultimately decisions about the protocol) to be made more and more in private.

I would even consider this response I’m making right now to be noise because it contributes nothing to the topic at hand, but it is at least in an effort to cut down on future noise and be a net positive.  That’s all I’m going to say on this here.

---

[@atlanticcrypto](/u/atlanticcrypto) Maybe I’m the only one, but I really dislike URL shorteners. They just force me to go to [checkshorturl.com](http://checkshorturl.com) to see where the link is going to redirect to, which is much more of a hassle than dealing with a long url (which could’ve just been embedded in text to make it shorter).

[Here is the long link](https://drive.google.com/file/d/15n7Vur8wwlfDK6ZXwohUc95rXOUIXo7j/view).

The slides are a little noisy for me, particularly the background graphic.  I’m sure if somebody was presenting them it would be fine, but reading them on my own they are very congested.

It mentions that this proposal is “in line with Draft Casper FFG’s Year 1 Issuance”.  Is this a meaningful/valuable target?  I don’t think using a line out of a draft as your goal is particularly worthwhile if that’s the only support.

What is the motivation behind reducing issuance?  That may seem like a silly question, but the follow-up questions to the response tend to point out nuances that bring into question why reducing issuance really matters.

You mention “top line incentives” a few times, but never really define it.  Are you just talking about block rewards that aren’t ommer related?

The fact that the top 15 pools have 90% of the hashrate is irrelevant.  Those pools don’t *own* the hashpower.  Pools *are decentralized*.  Lines like “Uncle rates are driven by latency - a product of centralization” are patently false.  I find the motivation and “evidence” extremely suspect, but I’m not going to spend too much time breaking down every little thing in this when I haven’t seen it being referenced by anyone else.

---

**atlanticcrypto** (2018-08-23):

EIP-1295 will be discussed during tomorrow’s developer call. I will be presenting it.

I will address your claim that “Uncle rates are driven by latency - a product of centralization” is patently false.

Latency is the single driver of Uncles.

With centralization of work package distribution (mining pools), there is latency introduced that can be otherwise avoided when solo mining. Hence, latency is a product of centralization.

Mining nodes are hit with three levels of latency:

```
Latency with the Ethereum node network — the time it takes for the mining node to receive notification that a new pending block is available.
Latency with the miners — the time it takes for the mining pool to send new work packages to its miners + the time it takes for a miner to send a potential solution back to the mining pool.
Latency in propagating a “solved” block — the time it takes for a mining pool to distribute its valid block solution to 51pct of the Ethereum network.
```

There are some areas where a mining pool/node CAN minimize latency:

```
Invest in low-latency fiber connectivity.
Invest in best-in-class compute servers (including SSD storage).
Increase their exposure to the Ethereum network (connect to more peers).
Trim their transaction queue size to minimize computing requirements.
```

There are some areas where a mining pool/node CANNOT manage latency:

```
**The latency of its miners to the pool itself (think home internet latency).**
The latency of network peer connections.
The block propagation advantage larger pools have to their own miners.
```

Let’s quantify some of the latency:

```
Mining node block propagation — 200ms to 500ms
Block Import / Transaction Processing — 100ms to 150ms
Mining pool to miner latency — 100ms to 500ms
Miner to mining pool latency — 100ms to 500ms
```

This puts our aggregate range of latency from 400ms to 1650ms.

If a target block round is 15sec, it’s possible a valid block may not be propagated for 1.65sec!!! That’s an 11pct delay under normal operating conditions! That also defines the lower boundary of the network wide uncle rates.


*(11 more replies not shown)*
