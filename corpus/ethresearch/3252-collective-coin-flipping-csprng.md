---
source: ethresearch
topic_id: 3252
title: "\"Collective Coin Flipping\" CSPRNG"
author: MihailoBjelic
date: "2018-09-06"
category: Sharding
tags: [random-number-generator]
url: https://ethresear.ch/t/collective-coin-flipping-csprng/3252
views: 9232
likes: 26
posts_count: 30
---

# "Collective Coin Flipping" CSPRNG

“Collective Coin Flipping” is a CSPRNG (cryptographically secure pseudo-random number generator) model, first described in an eponymous paper back in 1985. The goal of the paper was to come up with a method to perform collective coin flipping which is only slightly biased despite the presence of adversaries.

The authors first noted that this problem was considered before, mostly in the field of the Byzantine Generals Problem research, and that all past solutions were based on the assumption that information

may be communicated so that only some of the parties can read it (usually achieved by using cryptography). However, the authors’ idea was to completely avoid such assumptions, i.e. to deal only with games of complete information. They analyzed several Boolean functions on which every variable has only a small influence, as a way to achieve the goal in such an open environment.

Original paper: http://www.cs.huji.ac.il/~nati/PAPERS/coll_coin_fl.pdf

I’ve stumbled upon this work a few times already, and AFAIK Polkadot is considering using it, too. I wonder if anyone has looked into it? [@JustinDrake](/u/justindrake) or [@vbuterin](/u/vbuterin), maybe?

I’ve skimmed through several papers that iterate upon this work and these two might be worth mentioning:

1. “Random Selection with an Adversarial Majority” (link); describes the first protocols that solve the random selection problem in the presence of a dishonest majority in the full-information model (the model introduced by the original paper).
2. “Lower Bounds for Leader Election and Collective Coin-Flipping in the Perfect Information Model”
(link); defines lower bounds (in terms of number of rounds and number of bits per round) for any n-player coin-flipping protocol that is resilient against corrupt coalitions of linear size.

## Replies

**dlubarov** (2018-09-06):

Interesting, thanks for the links. Their construction is simple, but you have to get kind of far in the paper to see it, so here’s a summary. I just quickly skimmed the paper, so let me know if I missed anything important.

The idea is to divide the n boolean variables (think 1-bit validator VRF outputs) into blocks of size b. Then the “coin flip” function f is just

> 1 if and only if a whole block unanimously votes one and is 0 otherwise.

b must satisfy (2^b − 1)^{1/b} = 2^{1−1/n}. It’s roughly log(n), but we need that particular value in order to make f unbiased, i.e. to ensure that it outputs 0 and 1 with equal probability when the inputs are random.

The “influence” of a single variable (which I think is essentially probability of that variable deciding the result if all others are randomly assigned?) is \mathcal{O}(log(n)/n), which is better than the more obvious majority function, where influence is in \mathcal{\Theta}(1/\sqrt{n}).

---

**Mikerah** (2018-09-06):

Since Polkadot is considering using collective-coin flipping, I’m pretty sure [@vbuterin](/u/vbuterin) and [@JustinDrake](/u/justindrake) have gone into it.

After several discussions with [@JustinDrake](/u/justindrake), the current thought on what RNG Ethereum is going to use for sharding is a RANDAO+VDF scheme, where RANDAO is used as a source of weak/low entropy and the output of RANDAO is used as the input into some verifiable delay function (the main contender is based on RSA groups). Once the VDF is computed, the result is the random number.

---

**MihailoBjelic** (2018-09-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> thanks for the links

Thank you for taking time to look through them.

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> let me know if I missed anything important

I think you’ve summed it up well, although I didn’t go into the details of the paper, too.

I will ask someone from the Polkadot team/community to explain to me how do they intend to employ this. I think I’ve heard someone mentioning that the idea is to use one of those Boolean functions together with previous block hashes (I might be wrong, of course).

---

**MihailoBjelic** (2018-09-06):

[@Mikerah](/u/mikerah) I don’t know a lot about VDFs, but the term “specialized hardware” makes my skin crawl.

Wouldn’t it be better if we could get rid of those things once for all? What’s your opinion on this?

---

**Mikerah** (2018-09-06):

I understand the sentiment about specialized hardware. Note that this phase is currently in research and they are working on other ideas. The Ethereum Foundation is getting a report written about VDF ASICs and [@JustinDrake](/u/justindrake) organized a VDF day for practitioners to come together in order to share their ideas on VDFs.

There are also other alternatives that tend to have a lot of shortcomings. Among them are threshold cryptography (used in Dfinity) and verifiable random functions (used in Algorand and Ourobouros). Some of these are susceptible to 51% attacks, not quantum resistant, require large committee sizes, etc.

---

**MihailoBjelic** (2018-09-07):

Thanks for the answer [@Mikerah](/u/mikerah).

![](https://ethresear.ch/user_avatar/ethresear.ch/mikerah/48/1616_2.png) Mikerah:

> The Ethereum Foundation is getting a report written about VDF ASICs and @JustinDrake organized a VDF day for practitioners

Firstly, I truly admire [@JustinDrake](/u/justindrake)’s work and effort. Secondly, if I got it right, that report should estimate the viability of production of commodity VDF ASICs? I don’t want to be negative, but that’s “just” a report by a (group of) professional(s). If I’ not mistaken, that type of ASICs would be completely new (built to solve the VDF function), so there should be substantial room for improvement in the future (Bitcoin’s SHA-256 ASICs improved a lot since the beginning). There are no guarantees that at some moment, some other (group of) professional(s) will not come up with a much better tech/design and build ASICs much more efficient  than the “commodity” ones, and then we have a problem. I’m not a hardware expert, maybe I shouldn’t discuss this at all, but I’m just a bit concerned…

Also, Ethereum 2.0 is already an ambitious project, [@JustinDrake](/u/justindrake), [@vbuterin](/u/vbuterin) and everyone else are already neck-deep in work, can/should we involve ourselves even in hardware manufacturing on top of everything else?

If we could come up with a safe, software-only solution for RNG, that would be great.

---

**dlubarov** (2018-09-07):

I think you’re right that it would be hard to build a near-optimal ASIC right from that start, but that should be okay, as long as we can come up with a reasonable multiplier like 100x and be fairly sure that nobody will beat that.

Like if 100x is our multiplier, and the VDF is parameterized to take 100 hours on the commodity ASIC, then we assume the VDF will take attackers at least 1 hour. It seems hard for an attacker to do any manipulation with a 1 hour delay, since they would need to wait for their predecessors’ blocks before starting the computation, and the system would normally move on before 1 hour is up, skipping the attacker’s block.

So I figure for the attack to work, an attacker would need a way to pause the consensus mechanism while running their VDF. Like if the system uses Tendermint-style consensus, the attacker would need a 34% stake, or the ability to DOS 34% of validators for 1 hour.

The other thing to consider is that if someone does come up with a super-fast ASIC, the security just degrades to VRF security (assuming we require validators to submit VRF outputs, not arbitrarily-chosen numbers). I.e. an attacker who controls the last n blocks in an epoch could manipulate up to n bits of entropy by withholding blocks.

I’m working on some analysis of VRF blockchain security. I haven’t finished, but it’s becoming clear that manipulation would rarely be profitable, on the order of 1% or less depending on the epoch size, the largest attacker’s stake, etc.

---

**Mikerah** (2018-09-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> I think you’re right that it would be hard to build a near-optimal ASIC right from that start, but that should be okay, as long as we can come up with a reasonable multiplier like 100x and be fairly sure that nobody will beat that.

Also note that VDFs are sequential in nature and most improvements in ASICs are mainly with regards to parallelization of computation. Moreover, I think a current research problem in VDFs is determining upper bounds to how much these computations can be sped up. Once we have these bounds then we will know that an attacker can’t do much better than the rest.

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> Secondly, if I got it right, that report should estimate the viability of production of commodity VDF ASICs?

Yes. The goal is to build close to no-expense-spared attacker ASICs. Access to these commodity ASICs will counter a no-expense-spared attacker.

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> If we could come up with a safe, software-only solution for RNG, I would be a happy person.

This is an open problem in cryptography that has been on the books for 30+ years. I have been trying personal to come up with something but it is truly a hard problem.

---

**MihailoBjelic** (2018-09-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> The other thing to consider is that if someone does come up with a super-fast ASIC, the security just degrades to VRF security

This is a valid point.

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> I’m working on some analysis of VRF blockchain security.

Great, share if you can once it’s finished.

![](https://ethresear.ch/user_avatar/ethresear.ch/mikerah/48/1616_2.png) Mikerah:

> Also note that VDFs are sequential in nature and most improvements in ASICs are mainly with regards to parallelization of computation.

True.

![](https://ethresear.ch/user_avatar/ethresear.ch/mikerah/48/1616_2.png) Mikerah:

> This is an open problem in cryptography that has been on the books for 30+ years.

Exactly. I will definitely go deeper into this coin flipping, it’s also been around for 30+ years. Since you’ve been researching this topic, can you maybe explain what are the downsides of BLS signatures/threshold cryptography? Thanks.

---

**Mikerah** (2018-09-08):

The main issue with using a beacon based on threshold cryptography is that such a beacon is susceptible to a 51% attack. In addition to that, BLS signatures are not quantum resistant due to their reliance on elliptic curve pairings.

---

**MihailoBjelic** (2018-09-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/mikerah/48/1616_2.png) Mikerah:

> susceptible to a 51% attack

I thought that we have 1/2 (or even 2/3) honesty assumption in Ethereum anyway? Do you know what could happen in the case of the 51% attack, I guess it still wouldn’t be easy/possible to do things possible in 51% attacks on PoW chains?

![](https://ethresear.ch/user_avatar/ethresear.ch/mikerah/48/1616_2.png) Mikerah:

> not quantum resistant

I believe this will be a valid concern in 10-20 years from now?

---

**Mikerah** (2018-09-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> I thought that we have 1/2 (or even 2/3) honesty assumption in Ethereum anyway?

For a random beacon, we need an honest minority assumption. Otherwise, using threshold cryptography as a random beacon, an attacker can very easily influence the outcome of the beacon.

That is why in the current design that [@JustinDrake](/u/justindrake) is considering, we are using VDFs. There is also an alternate design called the leaderless k-of-n beacon by [@JustinDrake](/u/justindrake) ([Leaderless k-of-n random beacon](https://ethresear.ch/t/leaderless-k-of-n-random-beacon/2046)) that looks very similar to the Dfinity random beacon that uses threshold cryptography. The issue with this design is that it would need quantum resistant cryptography in order to have the same properties as the Dfinity beacon.

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> I believe this will be a valid concern in 10-20 years from now?

The goal is to a solution that would work in the long-term. We are currently seeing quantum computers (even though they can’t do much yet) come into existence. So, we would still need to design a beacon that can last more than 20 years.

---

**AgeManning** (2018-09-15):

Thanks for the great responses on this thread.

I’m confused about the statement “an attacker can very easily influence the outcome of the beacon”. As I understand (at least in Dfinity) the random number is a sequence, i.e you sign the last random number and the hash of the signature is the new random number. If an attacker owned all signatures, isn’t it true that they could only predict future randomness rather than influence the outcome? I guess, if the group signature could be changed by aggregating different single shares then it could be influenced, but I’ve not looked into if that is the case or not.

Have I understood this correctly?

---

**Mikerah** (2018-09-17):

I think you right.

In my head, the word *influence* has several meanings. I guess the meaning that I wrote in that post is not completely accurate.

However, if the attacker did own a significant portion of the signatures (>50%), I think they would indeed have the power to influence the beacon itself since they get to choose the random number and can obviously determine the hash of the next random number.

---

**kladkogex** (2018-09-17):

BLS-based threshold signatures provide a very efficient for a common coin. It is secure and fully asynchronous.

---

**Mikerah** (2018-09-18):

Note that you cannot just say that a particular cryptosystem is secure without a particular definition. BLS-based threshold signatures are efficient and are fully asynchronous but as explained above they are susceptible to 51% attacks. The fact that they are susceptible to 51% attacks is why [@vbuterin](/u/vbuterin) and [@JustinDrake](/u/justindrake) are not using them for the randomness beacon in Ethereum.

---

**kladkogex** (2018-09-18):

Can you explain how the algorithm above are not susceptible to 51% attacks ?)) I  thought if more than half of your network are bad guys you are always screwed and math does not help …

---

**Mikerah** (2018-09-20):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Can you explain how the algorithm above are not susceptible to 51% attacks ?

Do you mean the RANDAO+VDF scheme that is being considered? It turns out, only 1 person needs to properly compute the VDF on the generated value from RANDAO. So, a honest minority/single honest party assumption is used. Then, a malicious actor can only attempt to manipulate by refusing to reveal the output. But, I think there are issues before the VDF phase of the beacon, namely the RANDAO phase. A lot the issues that RANDAO has still are still present. I think an adversary can attempt to mess up the RANDAO phase before the VDF phase.

So, I think the Ethereum Foundation thinks that RANDAO+VDF has much better tradeoffs than beacons based on threshold cryptography.

In my humble opinion, the use of VDFs, even though there are bounds on how much you can speed the computation up with ASICs, feels like a step backwards. There has been so much innovation in getting PoS to where it is now, just for us to add a component that could potentially backfire. I think VDFs are this really cool and interesting cryptographic primitive but I wouldn’t want VDFs to be a part of the protocol.

---

**MihailoBjelic** (2018-09-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/mikerah/48/1616_2.png) Mikerah:

> So, a honest minority/single honest party assumption is used.

Are you sure RANDAO is safe with an honest minority assumption? If we have e.g. 1M nodes network with a malicious majority, they can refuse to reveal majority of “XORing inputs”, i.e. choose to reveal them one by one, trying to get the value that suits them best (they’ll have 500k+ tries)?

![](https://ethresear.ch/user_avatar/ethresear.ch/mikerah/48/1616_2.png) Mikerah:

> I think an adversary can attempt to mess up the RANDAO phase before the VDF phase.

Exactly.

![](https://ethresear.ch/user_avatar/ethresear.ch/mikerah/48/1616_2.png) Mikerah:

> In my humble opinion, the use of VDFs, even though there are bounds on how much you can speed the computation up with ASICs, feels like a step backwards. There has been so much innovation in getting PoS to where it is now, just for us to add a component that could potentially backfire.

Wrote about that above, glad you agree with me.

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> Do you know what could happen in the case of the 51% attack, I guess it still wouldn’t be easy/possible to do things possible in 51% attacks on PoW chains?

I would still really like to know how a 51% attack in Dfinity/threshold crypto-like random value generation process would look like/what would the consequences be? I looked online and couldn’t find anything. Anyone?

---

**JustinDrake** (2018-09-20):

The general idea in the “Collective Coin Flipping” paper is also known as “low-influence functions”. Another paper on the topic by [@iddo](/u/iddo) and others is [this one](https://arxiv.org/pdf/1406.5694.pdf). A downside of low-influence functions (e.g. see [this post by @cleasage](https://ethresear.ch/t/rng-exploitability-analysis-assuming-pure-randao-based-main-chain/1825/7)) is worsened collusion resistance.

Dfinity’s threshold scheme (which I understand Polkadot also intends to use) is quite cool. The main downside is liveness: if a significant portion of the network goes offline then the randomness beacon—and the whole blockchain!—stalls. (The more minor issues are quantum insecurity, a complex secret sharing setup, and adaptive attacks on infrequently-shuffled committees.) One of the design goals of Ethereum is to survive WW3. Even if 90% of nodes go offline we want the network to continue running.

From a consensus perspective, I think [@vbuterin](/u/vbuterin) is relatively confident that the Ethereum 2.0 protocol can be made robust enough to run on RANDAO despite it being a “weak” source of entropy. I think the best-case scenario of running on pure RANDAO is that the relevant design parameters—honesty assumptions, committee sizes, committee thresholds, etc.—are worsened to take into account the biasability of RANDAO.

A few remarks on the VDF approach:

1. It is the only known approach that is simultaneously un-biasable and un-stoppable (under a minority liveness assumption).
2. As pointed by @dlubarov the VDF strictly improves the RANDAO beacon. Even if the VDF is completely broken—i.e. outputs can be computed instantly—we fall back to the underlying RANDAO. As such, the potential for backfiring is limited.
3. Part of the value of a VDF-based randomness beacon is to expose strong randomness to dApps via an opcode. Replicating this critical piece of infrastructure at L2 without L1 support (such as VDF rewards and forced RANDAO participation) is hard/impossible.


*(9 more replies not shown)*
