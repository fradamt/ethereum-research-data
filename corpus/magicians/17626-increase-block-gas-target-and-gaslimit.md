---
source: magicians
topic_id: 17626
title: Increase block gas target and gaslimit
author: benaadams
date: "2023-12-24"
category: EIPs
tags: [gas]
url: https://ethereum-magicians.org/t/increase-block-gas-target-and-gaslimit/17626
views: 1625
likes: 11
posts_count: 11
---

# Increase block gas target and gaslimit

Increase block gas target by 50% from 15M to 22.5M and block gaslimit from 30M to 45M

https://github.com/ethereum/EIPs/pull/8058

## Replies

**Tudmotu** (2023-12-24):

Would love to see this happen ![:clap:t3:](https://ethereum-magicians.org/images/emoji/twitter/clap/3.png?v=12)

---

**LukaszRozmej** (2023-12-24):

I am against at this moment. Doing EIP-4844 and gas limit changes in same time window can have unexpected consequences as both can increase network latency. Secondly without EIP-4444 or similar mechanism it might put too much storage usage on users.

---

**MicahZoltu** (2023-12-25):

1. Gas limit defaults are not part of consensus, so this isn’t a Core EIP and really probably shouldn’t be an EIP at all.  You could lobby each client team independently to change their defaults, or try to lobby the core devs as a group, but no EIP is needed.
2. The motivation of this is severely lacking at the moment.  “We haven’t increased it in a while” isn’t a motivation, it is just a statement of fact.  What are the perceived benefits of increasing the gas limit?  What do you hope doing so will achieve?  What evidence do you have that increasing the gas limit will achieve the target goals?
3. The security considerations section should include a detailed analysis of the centralization risks associated with increasing the operational costs of running nodes that comes with an increased gas limit.  Every increase in operational costs to running a node are paired with a decrease in the number of users that can run their own node.
Without having an explicit target demographic that we want to be able to run a node, there is no way to mount an argument against increasing the block gas limit.  A good proposal should clearly describe the constraints on both sides (what is hurt by lowering the gas limit, what is hurt by raising the gas limit, and how do we weigh these competing constraints).

---

**Tudmotu** (2023-12-25):

As there is no better way to coordinate client teams other than EIPs, I suggest we keep it an EIP in the absence of more appropriate options. Opening 7 different discussions on 7 different github repos would be detrimental to coordination and counterproductive. At the very least, even if not as EIP the discussion should be held here on Eth Magicians where client teams can discuss jointly.

Regarding motivations:

Competition by other L1s is eating up Ethereum revenue. While there are plans to combat this i  the long run, we must form a short-term strategy otherwise devs would leave by the time the long-term solutions arrive

Regarding centralization risks:

1. By any measurement, the bottleneck for Ethereum execution is IOPS, not compute. Outside of fresh syncs, nodes rarely utilize 100% of the cpu even on relatively weak machines. This can clearly be seen via Grafana or AWS dashboards. Therefore this proposal should have little to no effect on centralization.
2. PBS will completely eliminate any risk here since validators are not required to execute the payload, only sign it

---

**benaadams** (2023-12-25):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Gas limit defaults are not part of consensus, so this isn’t a Core EIP and really probably shouldn’t be an EIP at all.

In theory nothing to do with devs, as is validator choice/setting, in practice people don’t change defaults.

In theory is to do with that setting (so stakers choice); in practice is the block builders since stakers like the mev too much.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> You could lobby each client team independently to change their defaults, or try to lobby the core devs as a group, but no EIP is needed.

So really should be lobbying the blockbuilders as they build most of the blocks. However if the blockbuilders unilaterally increase blocksize without some consensus from the community; and direction from the devs to frame the discussion (in terms of what the network will support), then we will be in a bad place.

To achieve some kinda consensus the discussion needs to take place in public in a common forum rather than individual discussion with individual groups. While technically there doesn’t need to be any consensus (each validator chooses their own setting); is better that there is a single point where people can express their views and we can come to a coordinated consensus ; which then acts as a signal to what the recommended blocksizes should be.

Ofc then the validators and blockbuilders can choose whatever size they want individually; since Ethereum is decentralized.

However decentralization does not imply without leadership; and if never properly discussed, it will never change; what is a better way to discuss than via EIP as while in theory everyone can choose their own setting, but in practice:

- if a node used a higher limit will other nodes attest to those blocks or will they get slashed?
- how is a consensus of a different limit communicated to blockbuilders to build higher gas blocks?
- It’s specified in the official docs that 15M/30M are the block limits Blocks
- Etherscan et al. even display block size vs target

So while at the surface it isn’t a consensus issue; in practice it really is but of a wider community consenus level than pure protocol.

I don’t how to be coordinate that outside of this forum and EIPs; but am open to suggestions if there is a better way? (Clearly running a poll on twitter is not the way ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12))

---

**domothy** (2023-12-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tudmotu/48/9144_2.png) Tudmotu:

> PBS will completely eliminate any risk here since validators are not required to execute the payload, only sign it

Well, not really. The proposer does blindly sign the payload header without knowledge of payload, but the rest of the validators still have to execute it (which requires knowing the whole state, hence state growth is still a bottleneck) before deciding that it’s a valid payload they can attest to (needless to say, optimistically attesting to potentially invalid payload would be terrible!)

PBS+Statelessness would be the combination that alleviates this, as validators could then execute and verify payloads without needing to know the state, since they could quickly verify a block witness provided by the builder. Now the gas limit could be increased without adding a state growth burden on nodes (with the tradeoff that fewer nodes now hold the entire state)

---

**Tudmotu** (2023-12-25):

Thank you for the correction.

Anyone remembers the arguments for not integrating this mechanism into the consensus itself?

If this was a proper EIP we could force proposers/builders to increase the target. This was part of 1559, correct? Was this decision documented somewhere as part of that EIP?

---

**benaadams** (2023-12-25):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> The motivation of this is severely lacking at the moment. “We haven’t increased it in a while” isn’t a motivation, it is just a statement of fact. What are the perceived benefits of increasing the gas limit?

Is about user experience (obviously should be properly evaluated post 4844 to see how that effects things).

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> What do you hope doing so will achieve?

Reduce regular user pain by including more of their transactions; potentially at a lower price, but the increased gas will compensate validators for the slightly higher load.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> What evidence do you have that increasing the gas limit will achieve the target goals?

On Xmas day there are currently 155,728 pending txns; most blocks are at target or above; when a lot of the world is on holiday and not doing blockchain things so is demand for the transactions:

[![image](https://ethereum-magicians.org/uploads/default/original/2X/2/29aea625366634f995fe13d1cc8c05d3993ea302.png)](https://etherscan.io/chart/pendingtx)

Even if there is a narrative that L1 is a settlement layer for L2s it does ignore that L1 is also the liquidity layer for L2s its where the largest liquidity resides and related txns will happen on L1 for that; as well as the fact some people just like Ethereum and don’t want to use an L2. Ethereum is not one thing and we should embrace and support its many facets and how users want to use it.

Regardless of L2s, TSTORE etc go live in the next fork with [EIP-1153](https://eips.ethereum.org/EIPS/eip-1153) enabling the exciting improvements in Uniswap v4; and judging by L2 adoption of PUSH0 will be a long time before that moves up the layers. So there is certainly a lot of time left with Ethereum as a primary execution layer as its significant use case.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> The security considerations section should include a detailed analysis of the centralization risks associated with increasing the operational costs of running nodes that comes with an increased gas limit. Every increase in operational costs to running a node are paired with a decrease in the number of users that can run their own node.

While state growth and storage costs are a serious concern and is being looked at via other initiatives e.g. [EIP-4444](https://eips.ethereum.org/EIPS/eip-4444) as part of a longer term strategy; in the shorter term, it doesn’t take into account the technological innovations in the hardware space.

When [EIP-1559](https://eips.ethereum.org/EIPS/eip-1559) went live a 2TB NVMe drive was the recommended size; and Ethereum EL has remained under 1TB.

Looking at the hardware side of things; at that time a 2TB SAMSUNG 980 PRO SSD 2TB NVMe Gen 4 cost $429; it now costs $139; and you can now buy a 4TB SAMSUNG 990 PRO SSD for $319; which is double the space for 25% less than the price of a recommended drive at the time of EIP-1559

[![image](https://ethereum-magicians.org/uploads/default/original/2X/1/1ca5a150a56c1be5fd22e9d454d2d84ad041c048.png)](https://camelcamelcamel.com/product/B08RK2SR23?context=search)

On the compute size as Ethereum on Arm demonstrates you can run both maintnet and an L2 on the same $189 Rocks ARM machine:

[![image](https://ethereum-magicians.org/uploads/default/original/2X/8/85847b707f35715316f8449f2893a765b276afc9.jpeg)](https://twitter.com/EthereumOnARM/status/1737409687358718304)

So its currently a $328 hardware outlay to validate Ethereum. (plus $18k in ETH (rocketpool) to $72k in ETH); and then validators stakes stack on the same EL node so it doesn’t incrementally increase (and [EIP-7251](https://eips.ethereum.org/EIPS/eip-7251) works to acknowledge this and reduce consensus load)

So I don’t see that it will particularly increase in operational costs for running a node in a way that would decrease in the number of users that can run their own node. It’s cheaper now to run a node with double the recommend disk space than it was when EIP-1559 went live.

As for state growth there is a risk that state growth is not addressed in the time it takes Ethereum to triple in size; which will happen slightly faster with a 50% bump in blocksize. However if that is the case then there are priority issues that are outside the scope of this proposal.

---

**benaadams** (2023-12-26):

**tl;dr** so the overall concern of state increase remains valid; however we should also accept that cheap fast storage has doubled in the last 2 years, so only going up by 50% is only half that increase

---

**MicahZoltu** (2023-12-26):

I recommend formalizing your above statements and adding them to the EIP.  I also recommend fleshing them out more.

Things to think/talk about when drafting security considerations section:

- What is the target demographic of people who you (the EIP author) think should be able to run an Ethereum node?
- Why did you choose that target demographic?
- How many node operators will we lose by increasing operational costs (e.g., by doubling state growth) and over what time (CPU/bandwidth costs are immediate, state growth is costs accrue over time)?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/benaadams/48/9199_2.png) benaadams:

> most blocks are at target or above

As a point of clarification: this is literally impossible over any appreciable length of time.  The system is self adjusting, and blocks will always be (on average) right around the target.  You can only have very short bursts of bigger before the system auto-corrects.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/benaadams/48/9199_2.png) benaadams:

> On Xmas day there are currently 155,728 pending txns

Having lots of pending transactions doesn’t necessarily correlate with the gas limit.  You could have a gas limit of 10B and still have lots of pending transactions.  Pending transactions are usually either people making a mistake when setting their gas pricing manually, or people hoping to get a deal on gas price by waiting until a low point (and people will deal hunt no matter how cheap gas is).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/benaadams/48/9199_2.png) benaadams:

> While state growth and storage costs are a serious concern and is being looked at via other initiatives e.g. EIP-4444 as part of a longer term strategy

We must not count our chickens before they hatch.  While one can be hopeful that things like 4444 or state expiry go live eventually, we need to be careful to not go into debt in anticipation of them.  Once these things are live we can *then* discuss the possibility of increasing the gas limit.  Note: I don’t think 4444 is sufficient to get us out of the disk-space-debt we are currently in.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/benaadams/48/9199_2.png) benaadams:

> So I don’t see that it will particularly increase in operational costs for running a node in a way that would decrease in the number of users that can run their own node.

IMO, the meaningful metric is “can a middle class westerner run an Ethereum client **in the background** of their home PC that they already have and use for other things”.  Normal consumers generally get 512GB-1TB drives these days, and those drives are shared with other uses like games, videos, music, photos, operating system, browser caches, etc.  These people also use their computer on a day to day basis, and many will shut it down at night (meaning they need to catch-up sync in the morning).

If people need to buy hardware just to run an Ethereum node, they simply won’t run an Ethereum node.  We should be targeting operation on what people already have, not on what some subset of people could afford to buy if they chose to do so.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/benaadams/48/9199_2.png) benaadams:

> Looking at the hardware side of things; at that time a 2TB SAMSUNG 980 PRO SSD 2TB NVMe Gen 4 cost $429; it now costs $139; and you can now buy a 4TB SAMSUNG 990 PRO SSD for $319; which is double the space for 25% less than the price of a recommended drive at the time of EIP-1559

In that time the state size of Ethereum has grown significantly.  While I think looking at price of drive is not the right metric, if you are going to do that you must consider the state growth over that time period as well as the price of hardware.  e.g., “cost to run an Ethereum client in 2021” vs “cost to run an Ethereum client in 2023”.  Things are further complicated by state growth resulting in hardware needing to be upgraded more frequently, since we don’t have a mechanism to cap disk usage like some chains have.

