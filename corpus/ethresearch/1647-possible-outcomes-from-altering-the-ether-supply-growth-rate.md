---
source: ethresearch
topic_id: 1647
title: Possible outcomes from altering the ether supply growth rate
author: jpitts
date: "2018-04-07"
category: Economics
tags: []
url: https://ethresear.ch/t/possible-outcomes-from-altering-the-ether-supply-growth-rate/1647
views: 4621
likes: 30
posts_count: 24
---

# Possible outcomes from altering the ether supply growth rate

Background:

- the White Paper describes a linear currency issuance rate.
- EIP 960 proposes a cap to the total ether supply, ending the linear issuance rate.
- EIP 186 proposes to reduce the ether issuance rate before Casper / PoS
- reddit discussion: “Let’s talk about the projected coin supply over the coming years”

What are the goals that drive maintaining a certain supply level or growth rate of a cryptocurrency?

What possible outcomes might occur from altering the ether supply growth rate?

## Replies

**vbuterin** (2018-04-07):

In general, increased issuance has a few consequences:

1. More funding that could be used to pay for security
2. More inflation of ETH, leading to the potential for lower ETH prices, which in turn mean that the total USD amount of security deposits drops
3. If issuance goes to a concentrated elite (eg. ASIC miners, concentrated wealthy PoS validators), then it makes the ecosystem more oligarchic over time.

(2) is especially hard to analyze because it’s very nonlinear; increasing annual issuance from 2% to 4% could lead to ETH prices falling by much more than 2% (and possibly even more than half) over the very long run, depending on the competitiveness of the cryptoasset market and other factors.

With PoS, the amount of funding that needs to go into security will be lower than it is in PoW, so you can argue that if bitcoin (and derivatives) can survive with a fixed supply on transaction fees only in a PoW regime, then so can ethereum in a PoS regime. There are concerns that PoW and PoS block production is insecure without issuance for micro-game-theoretic reasons (eg. fee-stealing attacks), but this is not a big deal if your proposed way of going without issuance is to have a regular block reward that is subsidized by *burned* fees, which is the kind of scheme that I generally favor.

Another concern is that if we promote a hard norm about a supply cap (supply will never go up above 121 million! If it does then by definition it’s not even ethereum!!!1!1!!), then we lose the ability to later increase issuance, either because we later decide that that *is* the best way to get security, or because we want to use issuance for other reasons (eg. an on-chain-governed decentralized bounty fund, or an airdrop of N coins per person to as many people as possible).

---

**jpitts** (2018-04-08):

These consequences described in the first section all make sense. #3 stands out in particular because this sector of the ecosystem is where the supply first lands, and because relates to a long-standing goal of reducing wealth concentration described in the White Paper and elsewhere.

One additional consequence that may be considered as very significant is the effect of ether supply and expectations about ether supply on capital formation.

Through the lens of [Mankiw’s 2nd principle](https://en.wikiversity.org/wiki/10_Principles_of_Economics), it can be understood that an economy with a less inflationary currency reduces the opportunity cost of holding that currency. The same applies to the rates of bonds. This opportunity cost of capital can help us understand how seemingly abstract factors such as inflation and bond rates relate to investment in business expansion and, by extension, the entire rate of growth of an economy.

But this economy is not normal. The extreme price increases experienced by all major investment opportunities in the Ethereum ecosystem – including ether itself as denominated in fiat – has likely clouded the effect of ether supply on capital formation. But PoS may help us see this far more clearly. The very reliable opportunity posed to investors by staking may mean that they not only consider the return on staking vs. other opportunities, but also consider the ether supply growth rate, or lack thereof.

> With PoS, the amount of funding that needs to go into security will be lower than it is in PoW, so you can argue that if bitcoin (and derivatives) can survive with a fixed supply on transaction fees only in a PoW regime, then so can ethereum in a PoS regime.

Are there measures of the effect of miner rewards in the economy, either direct via investments made, or indirect via the transfer of their ether to other investors via exchange? It would be very instructive to understand how similar to the banking system and its extension of credit this has become.

> Another concern is that if we promote a hard norm about a supply cap… then we lose the ability to later increase issuance

This is an interesting effect which certain central banks appear to be concerned about, but not so much for psychological expectation reason. For example, much has been made of [BoJ’s loss of monetary firepower](https://www.reuters.com/article/us-japan-economy-boj/bank-of-japan-may-shift-policy-focus-to-rates-as-monetary-firepower-wanes-idUSKCN11P08M) at different times.

---

**vbuterin** (2018-04-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/jpitts/48/877_2.png) jpitts:

> But this economy is not normal

Agree that’s the case now, but it’s worth pointing out that eventually the economy *will* become normal (unless it hits zero first). And we have to start planning for that future now, not a decade from now when there are multibillion-dollar interests tugging at the governance process and it’s much more difficult to accomplish anything.

---

**kladkogex** (2018-04-08):

Imho one can prove that any PoS solution is fundamentally less secure than PoW.

The argument is very simple : consider a virus that compromises ALL nodes except one.

With PoS an attacker  can regenerate/resign transactions from the beginning of time to create  a totally fake chain indistinguishable from the  real chain.

With PoW an attacker that compromised all nodes except one, still can not create a fake chain.

So PoW is infinitely more secure long term. Any PoS chain has a 100% probability  to be destroyed some time in the future

What this means for Ethereum is that the  best future  is to keep the main chain PoW and let the side chains be PoS. Then you have a nice hierarchy, where the top chain is super slow and  secure, and side chains are fast and less secure.

If Ethereum goes PoS, then 10 years from now  virus that compromises Linux kernel can infect all or substantially all Ethereum node and destroy the main chain.  With PoW the main chain is undestroyable.

For PoW  imho the best  money issuance rate is to fix mining complexity forever .T

Fixing complexity lead to an equilibrium where long term ETH would be basically pegged to electricity/ASIC costs.  As a result,  ETH would have much less price volatility.  Imho,  mining complexity adjustments are a bad thing that leads to ETH price fluctuations.

If Ethereum decides to go PoS for the main chain, a very likely scenario will be that miners will disagree. and there will be a fork that will surpass in value the PoS solution, because the PoS solution for the main chain is inherently less secure.

Another important argument is that PoS will not help much for the main schain.  Even if the main chain goes PoS it will still not able to go above 100 transactions per second, due to EVM execution, so whats the point making it PoS then …

---

**ldct** (2018-04-08):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Imho one can prove that any PoS solution is fundamentally less secure than PoW.

First of all security of these systems are multidimensional, containing at least the distinct dimensions of (for e.g.) fault tolerance thresholds, incentive compatability, and actual realistic monetary cost of attack. But let’s look at security from the point of view of your proposed attack.

> With PoS an attacker can regenerate/resign transactions from the beginning of time to create a totally fake chain indistinguishable from the real chain.

Sounds like this is basically the long-range attack problem, which is indeed a weakness of PoS over PoW. But IMO this is solved by relying on weak subjectivity ([Proof of Stake: How I Learned to Love Weak Subjectivity | Ethereum Foundation Blog](https://blog.ethereum.org/2014/11/25/proof-stake-learned-love-weak-subjectivity/)). In particular, if my node does log on at least once every four months (and has logged on once from from before the virus appears) my node *can* distinguish the attack chain from the real chain, since the Casper-FFG papers specifies a fork choice rule that clients do not revert blocks once they see them finalized.

> If Ethereum goes PoS, then 10 years from now virus that compromises Linux kernel can infect all or substantially all Ethereum node and destroy the main chain. With PoW the main chain is undestroyable.

What does “destroy” mean? For instance, here’s one (extremely expensive) way to recover from what I think of as a virus-infects-lots-of-computers attack: get most full nodes to install the Linux kernel patch that fixes the virus, then coordinate to hard-fork the chain from before the virus appears. Super expensive, probably not the best way, but it works. Is the claim that there is an attack that can be done on PoS systems for which the above recovery fails, and that this attack can’t be done on PoW chains? If so what is the attack in more detail?

> so whats the point making it PoS then …

For me at least, economic finality, see https://github.com/ethereum/wiki/wiki/Proof-of-Stake-FAQ#what-is-economic-finality-in-general. In PoW you don’t have this property, you only have some sort of probabilistic finality (with certain assumptions, blocks get exponentially more unlikely to be reverted the more confirmations they have).

This concretely means it’s more expensive to revert finalized/confirmed blocks; in PoS the cost to do this is to cost to destroy about 1/3 of the stake, while in PoW the cost is just to outmine the main chain for a while. In PoW an equivocating validator (builds on two chains) can only be punished by reducing rewards (and rewards are capped by issuance), in PoS an equivocating validator can be punished by slashing deposits. See https://medium.com/@VitalikButerin/a-proof-of-stake-design-philosophy-506585978d51 for more.

---

**MicahZoltu** (2018-04-08):

[@kladkogex](/u/kladkogex) In your example, why would a client accept a block that has no path to the most recent block the client has seen finalized?

That feels like saying a PoW client will throw away it’s recent blocks and accept a new block built on genesis proposed by the one remaining miner (no reasonable client would do this).

---

**jpitts** (2018-04-08):

Regarding the concern of “interests tugging”: stakeholders tugging at the process can be seen as user feedback and common to any human-dependent system. It must be guided through appropriately-configured communications channels and well-designed and fair governance processes.

And I agree wholeheartedly that the planning has to occur now, informed by history and guided by well-established theory.

Regarding theory, it is important for us all to avoid understanding the macro-economic situation through a single lens, even if it has worked well in other cases or is comfortable. There are many schools of thought – in and even outside of economics – that can be helpfully employed in understanding the situation we see, understanding the future situation which we desire, and in guiding decisions.

I do not believe that macro-economic theory is being applied enough to this problem domain. Is there a reason why, or concerns driven by well-known failures in the application of various economic theories in normal economies?

---

**vbuterin** (2018-04-09):

> I do not believe that macro-economic theory is being applied enough to this problem domain.

Most traditional macro-econ has to do with a mostly stable currency whose price with respect to the CPI adjusts at most a few percent a year in either direction in most cases, *and* which is used as a unit of account for both immediate services and long-term agreements. Cryptocurrency is not remotely the same situation.

---

**jpitts** (2018-04-09):

Thanks [@vbuterin](/u/vbuterin), this clarifies why you believe that traditional macro-economic theories do not apply to a cryptocurrency like Ethereum.

---

**kladkogex** (2018-04-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> Is the claim that there is an attack that can be done on PoS systems for which the above recovery fails, and that this attack can’t be done on PoW chains? If so what is the attack in more detail?

Yes, The attack goes as follows:

1. An unknown  kernel virus infects all computers in the world and stays silent.
2. At a particular moment (time X) all computers modify/resign the chains they way they want.  The will cause a total havoc, literally Ethereum turning into a Skynet from the Terminator movies.

There are already example of things like that. For instance NSA installed a backdoor in ALL Samsung TVs in the world.

Linux Kernel is an extremely vulnerable thing. Kernel viruses are untraceable by definition.  Intel CPUs are extremely vulnerable, virtual machine hypervisors are extremely vulnerable, gcc compiler is extremely vulnerable.  Bootloaders are extremely vulnerable. BIOSes are extremely vulnerable. NSA has backdoors to all of this stuff.

If Ethereum switches to PoS, it will be trivial for NSA to shut down at anytime, and not only for NSA, but for also for bad guys like totalitarian governments around the world.

With PoW even NSA can not destroy Ethereum, this is a big achievement imho, so one has to think really hard before abandoning PoW.

---

**jpitts** (2018-04-10):

Is there any analysis work done to trace how miner rewards are being used in the network? Has it been determined if rewards are primarily exchanged for fiat or BTC vs. invested in tokenized firms vs. held?

---

**ldct** (2018-04-10):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> At a particular moment (time X) all computers modify/resign the chains they way they want.  The will cause a total havoc, literally Ethereum turning into a Skynet from the Terminator movies.

You’d have to be more specific wrt what “cause total havoc” means - why can’t my proposed hard-fork recovery work?

---

**kladkogex** (2018-04-19):

If you have a POS chain and all computers except one are infected, you can use a hard fork to reset back to to the correct state.  The problem though is that how do you differentiate two computers with slightly different chains?

In other words,  lets say all computers except two are infected. Then the two guys come to you and and say they have un-infected chains. But the chains are slightly different.  It then becomes impossible to differentiate the true good guy from the fake good guy.

Or is this too paranoid? ![:smiling_imp:](https://ethresear.ch/images/emoji/facebook_messenger/smiling_imp.png?v=9)

---

**MicahZoltu** (2018-04-19):

I argue that at that point it doesn’t matter.  You effectively have a global catastrophic failure on your hands, the economic participants can take a beat and figure out what chain they want to use via traditional (non-automated) human communication like Reddit, Twitter, blogs, etc.  While I think it is valuable to recognize/acknowledge this potentiality when analyzing the soundness of Proof of Stake, I think its risk (`liklihood * impact`) ends up being pretty small in the end when you realize that the problem *can* be solved off-chain.

---

**ldct** (2018-04-20):

You can of course privately differentiate them, if this really happened I would check the addresses I have private keys for and see if I still have the same amount of ether, etc on both chains. If the state of all my accounts is the same on both chains then honestly I really don’t personally need to care which one was the “good guy”. If many people do this then the split would end up being resolved by social consensus (presumably the two chains have different state, and someone would notice they lost something on one chain, or that one chain has an inflated supply of some token they care about).

I don’t think PoW helps you resolve this kind of split - if there were 2 competing chain heads after a virus attacks I’m not going to choose the one wherein I lose all my money just because it has slightly more PoW on it; in your scenario under PoW the attacker can easily take the real chain tip, add a block that deletes some random UTXOs and creates some under his control, and now you have 2 tips with the same PoW.

---

**manfr3d** (2018-04-23):

I think you can also use a issuance dynamic adjustment per block to reduce volatility, if there is an automated concensus on the previous (or previous sliding window) gas consumed, you can estimate present change in price related to stable fiat, and then adjust the block issuance. You can smooth with moving average. There is a recent article on correlation between many-day (or month) crypteconomy activity and price change:

https://medium.com/cryptolab/https-medium-com-kalichkin-rethinking-nvt-ratio-2cf810df0ab0

---

**fubuloubu** (2018-04-23):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> For instance NSA installed a backdoor in ALL Samsung TVs in the world.

It would be very difficult to coordinate an attack like this and perpetuate the malicious chain without a portion of the network recovering from it. The Linux kernel is used by many different operating systems built many different ways with many different versions of the code. I would give a conservative estimate that at any given time 100+ variations of the Linux kernel are being run in the real world (it’s probably closer to 1000’s if you consider all the people running custom kernels because they’re masochists). This is on top of being in an environment where many non-Linux systems are in common use (Windows, Apple, etc.). And all those computers run on top of various networks of differing security and connectivity. The number of permutations here is roughly on the order of millions.

This is not to say that the NSA couldn’t hack any given computer in very little time if they put their considerable resources to it, but the heterogeneity of the computing systems this software can run on inherently makes a massively coordinated attack very difficult.

I would be way more concerned about malicious PRs into client repositories, that’s a much easier way to attack the network, and the reason why it’s so important to have many different implementations being managed by strongly technical teams.

But this is WAY off topic now lol

---

**d10r** (2018-04-26):

> More inflation of ETH, leading to the potential for lower ETH prices, which in turn mean that the total USD amount of security deposits drops

Ether inflation will lower its value only if supply growth exceeds the growth of *network value*.

Assuming typical network growth rates (something between S-curve and exponential) and assuming that Ethereum is far from having reached its growth limit, that shouldn’t be an issue for a long time - especially if you assume Metcalfe’s Law applying here (I don’t see why not).

It’s true that in the long term inflation becomes a risk, because network value can’t grow forever (or maybe it can, just like the economy).

But as long as network growth is to be expected, I consider too little inflation more of a risk, because it has already started to turn Ether into another digital gold.

It was supposed to be *fuel* for decentralized applications.

---

**swapman** (2018-04-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> More funding that could be used to pay for security

Can you clarify this point?

Higher supply rate/quantity, ceteris paribus and without context, is the same as government printing money. So  it increases quantity which reduces the purchasing power (as modeled in basic quantity theory of money in Friedman 1987)

When the government does this they justify the “gain” by [seignorage](https://en.wikipedia.org/wiki/Seigniorage), which is basically “I printed $100 bill for $0.75 marginal cost and pocket the difference” and “I spent the money before the inflation was recognised and reacted to by the broader economy”, a first mover advantage of sorts.

Economists in traditional economy justify it by saying sticky prices induces demand on the margin, and higher inflation can induce people to invest in more which adds stimulus to the economy. (see [Mankiw & Reiss 2002](https://dash.harvard.edu/bitstream/handle/1/3415324/mankiw_stickyinformationversus.pdf?sequence=2))

If I understand you correctly, the increased supply in the context of extended PoW makes the additional supply “backed” by the real resources of having to mine to receive them. So the additional quantity is not “helicopter money” state-style, but it is additional quantity that is only disbursed when real resources are expended to “earn” it, which attracts hashing power to secure the network.

I think this is an important distinction when people get nervous about supply increases leading to direct negative impact on value a la Venezuelan inflation style.

---

**ldct** (2018-04-27):

increased issuance to validators in PoS makes it more attractive to become a validator, thereby increasing the amount of eth staked, thereby making “economic finality” be stronger in that a larger amount of eth will get slashed in a history with a reversion of a finalized block.


*(3 more replies not shown)*
