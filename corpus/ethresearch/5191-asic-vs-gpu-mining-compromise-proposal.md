---
source: ethresearch
topic_id: 5191
title: ASIC vs GPU mining compromise proposal
author: kladkogex
date: "2019-03-21"
category: Mining
tags: []
url: https://ethresear.ch/t/asic-vs-gpu-mining-compromise-proposal/5191
views: 3900
likes: 8
posts_count: 11
---

# ASIC vs GPU mining compromise proposal

On the subject of ASIC vs GPU mining -  imho an optimal proposal should both allow GPU mining and help people that bought ASICs  in the past protect their investment.

So here is a compromise proposal which can make both parties happy

1. Allow both old(ASIC) and new (GPU) algorithms.
2. Have a dynamic rescaling coefficient which enforces 50% / 50% ratio of GPU-mined blocks vs ASIC-mined blocks.
3. One can then gradually phase out ASIC mining over, say, 10 years, by gradually shifting the ratio from 50%/50 to 100%/0.

## Replies

**adamskrodzki** (2019-03-24):

Why Ethereum should bother about protection of ASIC miners investment? I believe the whole point of ETHash was prevent ASIC on the first place.

Introduction of ASIC centralized mining which also was something Ethereum was against. If Ethereum change algorithm and make all ASIC useless immediately it will send clear signal that any next attempt will be threaten equally seriously so do not even try…

It is unfortune that it has not been done long time ago.

---

**kladkogex** (2019-03-25):

Well - many people who bought ASICs are totally innocent non-computer scientists who believe in ETH - unnecessarily harming them is bad IMHO.

In addition the more parties you have in the network the better.  Would not it help decentralization to have some people do ASICS and some  GPUs?

In addition,  not alienating ASIC owners will help to prevent ETH forking into to network. Otherwise, a fork into two tokens is almost guaranteed, since ASIC owners will for sure not throw their ASICs away.

---

**ekrenzke** (2019-03-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/adamskrodzki/48/1910_2.png) adamskrodzki:

> Why Ethereum should bother about protection of ASIC miners investment? I believe the whole point of ETHash was prevent ASIC on the first place.

Why should Ethereum bother protecting GPU miner’s investment? While resistance may have been the intention, absolute prohibition was never guaranteed. With money at stake, people will find ways to create custom hardware for the specific purpose of mining. Furthermore, the new design does not guarantee prohibition either, just resistance.

The use of scare tactics is not going to deter ASIC manufacturers. I am not claiming to be an expert when it comes to consensus algorithms, but I think it is generally unsafe to make hardware assumptions regarding Proof-of-Work. People will always find a way when there is money at stake, but if you take the development cost into account, I think the safer assumption to make is that these miners are incentivized to behave honestly for a few years. It is trivial to prove most attacks since the ledger is public, and displaying malicious behavior would cause massive price depreciation.

Currently, there isn’t an easy way to open a short position ETH, and the ways you could, often times suffer from liquidity issues. The prevalence of ASIC miners could prove to be an issue on longer timescales if their is no competition, but the mining industry has seen a boon in the last couple of years. One thing I would like to see is a more transparent effort for open-source ASIC design, but that is quite hard to do.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Well - many people who bought ASICs are totally innocent non-computer scientists who believe in ETH - unnecessarily harming them is bad IMHO.

Nobody should have special protections. Advocating for “remain” in this case should not imply any special privileges for ASIC mining. Optimization is inevitable on any proof-of-work blockchain.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> In addition, not alienating ASIC owners will help to prevent ETH forking into to network. Otherwise, a fork into two tokens is almost guaranteed, since ASIC owners will for sure not throw their ASICs away.

I think this is possible, but can’t they just mine ETC? That seems like a better fit than miners bootstrapping an entire network for something outside of their realm of expertise. Some supporting evidence of forking can be found in XMR, which forked into roughly six different networks upon the first hard-fork that imposed an algorithm change. I think we should examine the effects of XMR more closely before jumping to a conclusion on this one.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> In addition the more parties you have in the network the better. Would not it help decentralization to have some people do ASICS and some GPUs?

Prior art: DGB weighs five different proof-of-work algorithms to achieve consensus.

I have been advocating for this idea as a decent middle ground, since some smaller chains have successfully implemented it, but it stall has some cracks. I think one good counterargument is that it does introduce additional cost on something that should not have been greenlit in the first place.

I believe that this is an inelegant solution and sets a dangerous precedent for introducing new algorithms in the future. Since there is no formal governance mechanism for the modification of issuance – it could be less apealing to miners, and thus less secure overall.

---

**kladkogex** (2019-03-27):

From the security perspective ASIC mining has some advantages. Once ASICs are optimized it is hard to make something substantially faster.  IMHO one can hardly classify ASIC guys as evil.  After all, GPUs are ASICs too and produced pretty much by NVIDIA.  Just from the decentralization perspective it is better IMHO to have two players (NVIDIA) and ASICs vs one …

---

**ekrenzke** (2019-03-27):

There are also security arguments for ASIC mining over GPU mining that could be made regarding the definition of ASIC. If Ethereum mining loses significant profitability, or if the relative margins between two chains is thin enough, miners can easily defect to the chain that is most profitable. With application specific hardware, miners are further limited in what chains they can mine. I do not think this argument is strong enough to be the deciding factor, but it should be considered.

Additionally, the energy efficiency of ASIC mining greatly reduces the environmental impact of mining, but again, I do not think this is a strong argument. If I were to advocate for ASIC mining, I would also have to advocate for developing ways to incentivize open source designs, such that competition stems from minimal improvements over time, as well as the efficiency of supply chains.

---

**kladkogex** (2019-03-28):

Agree - another argument for having alternative algorithms is that each helps finance progress in a particular branch of computer science.

Actually, I would love an algorithm based on neural networks because it could finance improvement in AI

---

**gcolvin** (2019-03-29):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> On the subject of ASIC vs GPU mining - imho an optimal proposal should both allow GPU mining and help people that bought ASICs in the past protect their investment

It’s way too late for Istanbul, but a lot of the discussion here will be relevant down the line.

![](https://ethresear.ch/user_avatar/ethresear.ch/ekrenzke/48/3331_2.png) ekrenzke:

> kladkogex:
>
>
>
> In addition, not alienating ASIC owners will help to prevent ETH forking into to network. Otherwise, a fork into two tokens is almost guaranteed, since ASIC owners will for sure not throw their ASICs away.

I think this is possible, but can’t they just mine ETC? That seems like a better fit than miners bootstrapping an entire network for something outside of their realm of expertise.

Yes, they can.  There appear to be a small enough number of ASICs on the ETH network that they would fail to establish a viable fork of their own, so switching to ETC would seem to be the smart move.  But I’m not in that business, so I don’t really know.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> From the security perspective ASIC mining has some advantages. Once ASICs are optimized it is hard to make something substantially faster. IMHO one can hardly classify ASIC guys as evil…

![](https://ethresear.ch/user_avatar/ethresear.ch/ekrenzke/48/3331_2.png) ekrenzke:

> There are also security arguments for ASIC mining over GPU mining that could be made regarding the definition of ASIC…

I don’t recall any core devs calling them evil.   Unfortunately, the security arguments for ASICs didn’t get presented very well during the progPoW discussions, even by the ASIC manufacturers, but we were aware of them, and I doubt they would have carried the day.  We can always reconsider whether discouraging ASICs is best–I suspect that efficiency concerns will force us onto custom hardware, but I don’t when.  For the time being we have knowingly entered a war between the ASIC manufacturers, NVIDIA, AMD, and our algorithms.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> another argument for having alternative algorithms is that each helps finance progress in a particular branch of computer science.

Except that is not a goal of the core devs.  We can’t even finance ourselves.

---

**kladkogex** (2019-04-01):

Arguably a solution could be introducing a separate ETH2 token for ETH2 and using it to incentivize core devs.  10% could go to core devs, and 90% airdropped to ETH2 holders in proportion of ETH1 holding. After all, ETH2 is very much a startup  …

---

**lane** (2019-04-28):

If you’re interested in this topic, a lot of work has been done on it here, probably a better forum for discussing it: https://github.com/ethereum-funding/blockrewardsfunding/issues.

There are economic issues with having “a separate ETH2 token” that is one-way fungible with ETH, although at this stage it’s unclear exactly how Beacon chain ETH (BETH) and ETH will be exchangeable.

---

**kladkogex** (2020-02-27):

Well - is it time to come back to this ?

