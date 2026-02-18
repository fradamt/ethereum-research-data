---
source: magicians
topic_id: 6753
title: Who, what and why decides the gas limit?
author: uri
date: "2021-07-31"
category: Magicians > Process Improvement
tags: [gas, governance]
url: https://ethereum-magicians.org/t/who-what-and-why-decides-the-gas-limit/6753
views: 1786
likes: 8
posts_count: 8
---

# Who, what and why decides the gas limit?

During the PEEPandEIP discussion today on the gas limit, @vitalikbuterin suggested that moving to long-form might be valuable for more complete arguments.

Below is a short summary of the discussion (H/T [@poojaranjan](/u/poojaranjan)!), and what I see as the open-ended questions.

***Quick Summary***

Vitalik mostly covered the technical limitations for increasing the gas limit, as he previously articulated so well in his [post](https://vitalik.ca/general/2021/05/23/scaling.html).

The most interesting points Vitalik brought up, which are worth reiterating:

1. The gas limit is not binary “safe” or “unsafe” - it’s a spectrum, and it must balance safety and usability.
2. ETH design should make it easy for “many users” to run their own node, to protect users from the majority of hash or stake. Sync times should remain within the 12h-1d range.
3. the gas limit is very much a question of community values, and should be decided by the community. Technical arguments are critical, but we should be careful not to allow them to be used to sneak in personal opinions.

***Open-Ended Questions***

I think most would agree with Vitalik’s technical analysis (even if I think he slightly mischaracterizes the limitation at the network layer - propagation vs bandwidth - and I *think* [@AlexeyAkhunov](/u/alexeyakhunov) [@vorot93](/u/vorot93) and the Arigon team might disagree with his storage/memory numbers).

However, there were a few points which remained open-ended, which are the reason for this discussion. Specifically:

1. How the current gas limit is actually being set right now?
2. Who should set it?
3. How should it be set?

First, to the one point I think Vitalik was completely off (partially due to simplification, partially due to not being in close touch with the smaller mining pools).

Vitalik outlined how:

1. Miners adjust the gas limit with every new block they mine, pushing it up or down by up to 0.1%
2. Miners listen to core devs (see 2016 Shanghai DDoS)

**1. Miners adjust the gas limit**

This is *not* how the gas limit is set in practice. The gas limit is being set by those constructing the blocks - the mining *pools*.

Tomato Tomâtoe, right? well, no.

Mining pools are [much more concentrated](https://etherscan.io/stat/miner?range=7&blocktype=blocks), with the top-3 pools controlling 55% of the hashpower. Pools, especially the smaller ones, are mostly a DevOps operations, helping miners to reduce payout variance and remove their need to run nodes with great connectivity of their own. Pools all generally earn just 1% of the mining revenues, so they hold all the power but not the $.

The gas limit is effectively set by the top-3 pools, and the rest of the mining pools just follow their lead. When we asked some of the top-20 pools why are they setting the gas to a certain level, they were surprised to learn that they control this parameter.

Let that sink in.

Obviously, someone from their tech team knows and adjusts the gas limit parameter, but as an entity most don’t know nor care to learn what the gas limit should be.

It is controlled by the top-3, with some push from Pools 4-6, but 40% of the hashpower just follows their lead.

**Why is this so important that I’m draggin y’all thru the details?**

a. Because it means the gas limit is currently controlled by 3 actors. In fact, two are so big as to have veto power - without them the gas limit won’t change since 40% are just followers - and we have seen a pool singlehandedly preventing the move to 15M gas for months, and unfortunately their incentives are misaligned with the long term success of ETH

b. Pools hold immense power, but capture relatively little income, and can be “persuaded” relatively cheaply - about $1-2M.

Whenever I say this everyone jump and say “but if the pools push the gas limit to dangerous limits they will just get forked by the devs” which is obviously true.

But I’m not talking about raising the gas limit to 80M, I’m talking about moving from 12.5M to 15M gas. If tomorrow 5 pools push it to 17.5M gas, and in 3 months to 20M - would you know if I bribed them? Or Alameda, Wintermute, CMS, 3Arrows, Multicoin, Parafi or any of the other major DeFi trading firms for whom $1-2M is pocket change?

**2. Miners listen to core devs**

They don’t.

Sure, they will if there’s a catastrophe, an obvious malicious behavior, or an immediate danger. They are already walking on thin ice with the community and everyone knows it.

but do they follow the gas limit core devs tell them? no ![:point_down:](https://ethereum-magicians.org/images/emoji/twitter/point_down.png?v=15)

We shouldn’t blame them though - different core devs have different opinions, and it’s very hard for them to gage what the community actually wants.

[![Screen Shot 2021-07-31 at 12.26.06 AM](https://ethereum-magicians.org/uploads/default/optimized/2X/5/5c0a89919bc8ed75c004b4ecfb984d47669fe66c_2_690x329.png)Screen Shot 2021-07-31 at 12.26.06 AM1166×556 93.3 KB](https://ethereum-magicians.org/uploads/default/5c0a89919bc8ed75c004b4ecfb984d47669fe66c)

[![Screen Shot 2021-07-31 at 12.28.01 AM](https://ethereum-magicians.org/uploads/default/optimized/2X/b/b4b3ae2eb5bf26946b92a67911ce630c441723ae_2_690x345.png)Screen Shot 2021-07-31 at 12.28.01 AM1176×588 73.8 KB](https://ethereum-magicians.org/uploads/default/b4b3ae2eb5bf26946b92a67911ce630c441723ae)

[![Screen Shot 2021-07-31 at 12.26.46 AM](https://ethereum-magicians.org/uploads/default/optimized/2X/f/f73a9089335d159eacceab84b44434cd25cfcae5_2_690x343.png)Screen Shot 2021-07-31 at 12.26.46 AM1176×586 93.7 KB](https://ethereum-magicians.org/uploads/default/f73a9089335d159eacceab84b44434cd25cfcae5)

***Discussion***

So who should decide the gas limit? I think everyone (Vitalik and Peter included) believes it shouldn’t be the core devs - that it should be “the community”.

[![Screen Shot 2021-07-31 at 12.34.37 AM](https://ethereum-magicians.org/uploads/default/optimized/2X/6/6b955ea6ee77a9e9642e686f19a69b3838427eeb_2_690x149.png)Screen Shot 2021-07-31 at 12.34.37 AM1180×256 49.9 KB](https://ethereum-magicians.org/uploads/default/6b955ea6ee77a9e9642e686f19a69b3838427eeb)

But that doesn’t really say much… If I’m running my own ETH validator, what should I set the gas limit to be?

I don’t know what the different core devs think, using the defaults is the same as letting the core devs set it (which nobody wants). and how do we pass the decision from mining pools to the community?

I think that instead of hiding the question behind a giant “this is technical!” sign, the community should be presented with:

1. Insight to the different opinions among core devs.
2. explanations on budget implications: ETH can handle X if nodes run on $75 raspi, or Y if nodes run on $400 laptops, or Z if it requires $800 laptop to run a node. There will be disagreements on the assessment, and these will change over time due to improvements to HW and client implementations, but it would be a good starting point.
3. a way for the community to make its desires clear, and an incentive for pools to follow the community desires.

I know there are those who disagree with me, and I’d be glad to discuss where we diverge in our view of the current situation and the potential solution.

## Replies

**vbuterin** (2021-07-31):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/u/439d5e/48.png) uri:

> If tomorrow 5 pools push it to 17.5M gas, and in 3 months to 20M - would you know if I bribed them?

Historically, as far as I can tell, none of the gas limit increases were *initiated* by miners. They all followed some kind of movement with wide community support agitating for a gas limit increase. Sure, some core devs were often *not enthusiastic* about the increase, but they also did not violently oppose (there’s always a distribution of opinion, the extreme tail of the distribution does not reflect on the mean). Often, the increase happens after core devs’ concerns are satisfied (eg. the recent increase to 15M happened the week after Berlin included EIP 2929 that addressed DoS concerns).

So if tomorrow 5 pools push the limit to 17.5M, this definitely would raise eyebrows, and if they then push it further to 20M it would raise even more eyebrows and I fully expect “remove gas limit voting” EIPs to be proposed and discussed on ACD. People are sniffing not for positive evidence of collusion (which is hard to get), but for absence of evidence of a “normal” explanation.

> the community should be presented with:

I’ll also put into writing the suggestion I made in the call: we should just increase the gas limit on one of the testnets (Ropsten or Goerli or a new one but one that people actually use for applications) to 40M+, just so we can have an environment where the gas limit is higher and we can better understand what the consequences of that environment are. People are often better at understanding tradeoffs in the specific than in the abstract.

---

**uri** (2021-08-02):

> the extreme tail of the distribution does not reflect on the mean

But Peter is anything but the extreme, at least in the public eye. He is the loudest voice in the community when it comes to the gas limit, and to many he represents “what core devs think” (regardless if that’s true or not). Even your own [tweet](https://twitter.com/vitalikbuterin/status/1273941792707227648) says you told sparkpool you oppose increasing the gas limit because he opposes it. The fact nobody has any insight into what other core devs think, or what the community wants just doesn’t make sense in the world’s #1 transparent decentralized ecosystem.

But more importantly, if the pools would increase the gas limit to 17.5M today, Peter would object just like he did in the past - it won’t “feel” any different. And if they do it again, maybe not in 3 months but in 4-5 months, I don’t think anyone will be able to tell whether this is “organic” or not.

My point is not to say that Peter is wrong in opposing any increase - it is that’s the entire process is opaque:

- For pools, trying to understand what the community wants
- For the community, trying to reach a collective decisions
- For anyone, trying to gage whether the current gas limit is what the community wants

> we should just increase the gas limit on one of the testnets (Ropsten or Goerli or a new one but one that people actually use for applications) to 40M … People are often better at understanding tradeoffs in the specific than in the abstract.

I think that’s a great idea!

how to achieve this though? you need to communicate to everyone mining on it that this is what the community wants.

(well, you could just testnet-vote on the gas limit with EGL… ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12))

---

**poojaranjan** (2021-08-13):

Recording of the conversation on Block gas limit with [@vbuterin](/u/vbuterin)

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/0/040d8cd910abae47c3b611c4a69e32fae071dacd.jpeg)](https://www.youtube.com/watch?v=vJNO_UqcH6A)

---

**kladkogex** (2021-08-13):

I do not understand the general argument that Peter makes about the general health of the network being affected by block size.

Anything can run faster if computers become faster and networks become faster.

I personally think that fears of ETH becoming too centralized if higher block limit forces people to use more powerful computers and faster networks are grossly exaggerated. It may force out some people who run on AWS , but it is arguably better for decentralization.   People run ETH2 clients on AWS and store keys in plaintext.  Jeff Bezos can take over ETH2 anytime. If people are forced to run powerful hardware servers it is going to be much more secure.

Insecurity of ETH2 keys is a major problem that no one is talking about.

A vulnerability in an ETH2 client can take the entire network down in minutes if the vulnerability allows for BLS key extraction.

In addition, lots of performance problems come from geth quality not improving much. At SKALE we fight with geth bugs, slowness, instability and chaos every day. It is not able to reliably respond to basic API calls.  May be people need to switch to turbogeth or something else.

---

**shamatar** (2021-08-23):

I think that we encounter a usual twitter problem where there are a lot of opinions and heated argument, but without any material to support the case or help people to make an educated choice on a subject.

Let’s try to make some assumptions and analyze the current state of affairs. Some of these assumptions may be opinionated, but conclusions will follow only after facts that are global.

So, let’s start with some facts that readers should be aware:

- EVM opcodes are mispriced all over the place, but fixes only affect a storage (discussion of Geth vs Erigon is beyond this post or thread). One can run some Geth benchmarks on opcodes and see that

```auto
BenchmarkOpAdd256-12    	15743443	        75.0 ns/op	      32 B/op	       1 allocs/op
BenchmarkOpMul-12    	12864930	        83.4 ns/op	      32 B/op	       1 allocs/op
BenchmarkOpDiv256-12    	 6107662	       194 ns/op	      32 B/op	       1 allocs/op
```

Let’s ignore for a second an underlying reason why addition is as expensive as multiplication (I didn’t look for it, may be it’s overhead bound benchmark, but what it benchmarks then?), but it’s clear that division is few times slower than multiplication, while opcodes for them are priced the same (5 gas). Those benchmarks in Geth may be not benchmarks for the “worst execution time cases”, but the intuition is that divisions should be more expensive. On the machine that performed the benchmarks once can assume 30-35M gas/second for CPU bound tasks, so it’s around 2.5 gas for multiplication and 6 for division. Similar examples may be found for other opcodes.

- A number of empty blocks over ranges is the following:

```auto
from 12_000_000 to 12_010_000, around 12.5M gas limit: 179 empty blocks (with 0 transactions)
from 12_500_000 to 12_510_000, around 15M gas limit: 140 empty blocks
from 13_000_000 to 13_010_000, around 30M gas limit under EIP1559: 138 empty blocks
```

(yes, it’s a small statistics, but better than nothing)

Now comes an assumptions: if blocks on average represent a balanced load (so there is nothing special in those block like state read spam, and opcodes on average more-or-less ok-ish priced. Here we have a contradiction, but let’s assume at least something productive) then ratio of empty blocks to the number of all blocks is roughly proportional (with a factor of 2 most likely) to the ratio of the time that takes for a miner to process a block to the time between blocks. Why we can assume it: a reasonable behavior for a miner would be to start to mine on top of the newly received block (it it passes the PoW check) while the block is parsed, and then fill the block and start mining on a full one. Numbers above indicated that such ratio is roughly constant even though the block limit has increased, so performance of the miner’s hardware has increased roughly proportionally.

Another explanation may be also that that EVM is opcodes are so mispriced on average that large increase of the gas limit and number of executed opcodes per block only lead to a proportional increase of the execution time that of that opcodes that was negligible at the first place (e.g. that some execution time contribution was 1% and now is 2% on top of some other largely unchanged contributions). Alternatively that block size has increased proportionally to their part related to storage related opcodes cost.

Now one would ask a question whether “casual” mining exists on scale (reasonable mining decentralization beyond pools), is having a causal mining a target, should one assume that non-mining node hardware should be at some minimal decent performance level, etc. E.g. if average time to assemble a block by miner is roughly 2% of the time between block then one can naively assume that CPU/IO bound node would be able to keep up with a network even if it would have 50 times less performance than a mining node (50 is an upper bound, as a node should sync a history first).

I hope readers can make their choice more educated, but I would also appreciate if EGL would perform some more thorough analysis on a subject and assemble it in some place as it would help everyone. In any case I do not think that any hardcap on a gas limit is a solution as it builds a negative precedent for a network that wants to be decentralized, but arbitrary developers decisions can take declared protocol powers from a wider audience - that kind of negates that essence of PoS.

Regarding DoS attacks: if one claims that they exist in a current state of Ethereum 1.0 (e.g. storage access is too cheap, etc) such information (vector, etc) should be made public and not just claimed. If one would really want to DoS Ethereum it wouldn’t be hard for them to find such vector if it exists and if such DoS is in any sense rational, so hiding any such vectors only protects from lazy “hackers”. I’m not aware about the current state of performance bottlenecks between clients, but again, it’s not a thread for Geth vs Erigon discussion. My personal take it that clients’ competition should be supported as a healthy initiative to keep network in better state and remove inefficient legacy.

---

**norswap** (2021-08-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kladkogex/48/8349_2.png) kladkogex:

> I do not understand the general argument that Peter makes about the general health of the network being affected by block size.
>
>
> Anything can run faster if computers become faster and networks become faster.
>
>
> I personally think that fears of ETH becoming too centralized if higher block limit forces people to use more powerful computers and faster networks are grossly exaggerated. It may force out some people who run on AWS , but it is arguably better for decentralization.

It depends where we you want to be on the continuum of decentralization.

A geth node currently requires a 1TB SSD, and will soon be past that. It’s probably possible to diminish that by accepting that one does not need to keep full blocks for the whole history.

But still, it’s not hard to imagine a  medium-term future where you need 10TB in SSD. I can’t even buy that from Amazon, and buying 2x4TB drives will put me back ~12000+€.

And in fact, the the decentralization continuum goes the other way too - it would be better if we’re able to validate the network on our existing machine, wouldn’t it? What about a machine that isn’t always on (laptop), what about a smartphone?

I think there are a few “engagement cliffs” where you get less and less people that are able to validate the network. Right now you can with some difficulty validate the network on a dev laptop with a 1TB SSD. That might not hold for very long. The fear is that if you increase the throughput of the chain considerably, you might get to the point where the validation setup is the same cost as a second-hand car (a few 1000$) and you need to setup some kind of nerd cave to host it. **At that point there are very few “hobbyists” validating anymore and it’s all the more easy to dismiss them and move further in the direction of centralization.**

Even if we ignore storage (by far the biggest concern - that’s why nobody is overly looking at gas cost of multiplication vs division [@shamatar](/u/shamatar), it’s not even remotely on the critical path), increasing the throughput “because we can” is a slippery slope, because it’s always possible, but each time you increase it, it’s possible for less and less people.

I’m not saying we shouldn’t increase the limit, but I feel like people who want to increase it systematically fail to address the concern of people who don’t want to increase it, which is: how does that impact who validates the network (or just as importantly, who **can** validate the network)?

For sure, it would be good to have some better numbers on state growth + the projected hardware requirements in case of gas limit increase.

---

**shamatar** (2021-08-25):

[norswap](https://ethereum-magicians.org/u/norswap) may be I should have made it explicit, but div vs mul example there is to demonstrate that block gas limit is not anywhere close to an indication of validation complexity as a lot of gas may be just “wasted” for something that e.g. doesn’t take so much CPU cycles to execute. If one would really care about network health and if the storage is the most difficult problem then SSTORE pricing should have become dynamic consensus parameters like base fee in EIP1559, or may be even some deterministic function over statistics of non-empty storage slots in the state to avoid continuous repricing.

The last time I’ve checked for numbers the state (without archive) was quite well below 1TB and you do not need archive for mining (well, unless you mine then you do not strictly validate a network but just observe it’s state), and mining has other capital requirements contributions in a similar price range. It’s not cheap to have a machine that can efficiently follow the network, but it’s PoW and not PoS yet and a reason to have such machine should be separated from network requirements.

