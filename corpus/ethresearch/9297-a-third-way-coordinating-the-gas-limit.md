---
source: ethresearch
topic_id: 9297
title: "A Third Way: Coordinating the gas limit"
author: eleni
date: "2021-04-28"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/a-third-way-coordinating-the-gas-limit/9297
views: 5825
likes: 8
posts_count: 10
---

# A Third Way: Coordinating the gas limit

**TL;DR** - Setting the block size in the protocol (BTC) or by miners (ETH) isn’t working out well. We suggest the use of an on-chain coordination token which allows the ETH ecosystem to signal its collaborative desire, under the guidance of the core devs, and incentivizes pools to follow it.

In fact, Sparkpool literally just called for this on April 21, 2021.

**[![](https://ethresear.ch/uploads/default/optimized/2X/3/387e5b546ecf077ccfac23c15f0f2616eafdb62b_2_448x456.png)648×660 65.7 KB](https://ethresear.ch/uploads/default/387e5b546ecf077ccfac23c15f0f2616eafdb62b)**

**1. Overview**

The Ethereum community has been hyper focused lately on how to lower transaction fees. The problem is simple: more transactions want to be included in the block then available space. This causes fees to spike as users outbid each other to get their transactions inside the block. Different chains have taken different approaches to block space governance.

Bitcoin gave control over the block size to the protocol developers*. On the face of it, this makes a lot of sense. Those building the clients that run the system should have some technical decision making power. However, philosophical disagreements on what is the right block size led to internal fights among developers and a chain split: large block advocates left to form BCH and small blockers stayed with BTC.

Ethereum attempted a different paradigm—what if we gave control of the block size to miners? In Ethereum, each miner is allowed to change the subsequent block size up or down by 0.1%. Thus, over time, a majority of miners must mine blocks in a certain direction to achieve a new block size level. This solution sought to change a philosophical topic to an economic one—miners ought to act in their financial interest, or so it was posed, and the rationale was that their investment in mining equipment was a long-term commitment to the value of ETH.

**Where we are today**

This solution worked for a while, but the block size debate has resurfaced. Unfortunately, this time the community is arguing over long twitter threads on what the “right” answer is, while those with the actual power (miners) are notably absent from the conversation.

Instead, miners coordinate to increase the gas limit when they so choose. You can see from this chart of the historical gas limit that instead of miners independently voting on the optimal block size over time for Ethereum, they instead act like a cartel, agreeing in private on the optimal size and then all voting it into existence (shown below as jumps in gas limit). There have been no changes since July 2020 (the recent SparkPool announcement aside; it should be noted that it looks like again all the other miners have followed this decision acting in a coordinated effort).

See: etherscan. io/chart/gaslimit

Why haven’t the miners “listened to the community?” For one thing, it’s unclear what the community consensus is. Some Core Developers argue to reduce the gas limit, while others believe it should remain constant, while most fee-paying users believe it should be increased. Moreover, those with the loudest voice do not necessarily reflect the majority.

Another reason is miners are averse to increasing the gas limit because they may lose revenues in the short term. This is because miners may be at a local maximum where blocks are full and fees are high. However, if miners increase the block size, fees may come down in the short term but pent up demand that was initially priced out may start to flow in, increasing profits over the long term. EGL provides a buffer to unstick miners from this position.

Blocks are full today, and even though it seems intuitive increasing the gas limit may yield more value (more transactions at lower fees coupled with a higher ETH price), the economics are complex—and with ETH2.0 on the horizon, to most miners the answer is simply: why rock the boat? Sure, users are hurting and getting priced out of the chain, but this block size mechanism doesn’t take into account utility to users.

It’s time for another iteration in this experiment; I’d like to advocate for a third way.

Vitalik [has written](https://vitalik.ca/general/2020/09/11/coordination.html) about the role coordination plays in building an effective social system. He writes “building an effective social system is, in large part, determining the structure of coordination: which groups of people and in what configurations can come together to further their group goals, and which groups cannot?”

It is clear core devs should have a say, but they shouldn’t have the only voice. This is why people are excited about Proof of Stake—moving some of the power to those most invested in the protocol. The power should also probably not sit only with miners whose economic incentives may not align perfectly with the community. Our proposed solution is about creating a mechanism for anyone in the community to participate and influence the block size, using economic incentives (skin in the game and markets) to induce good behavior.

What if there was a way to financially incentivize miners to listen to the community? A third way that aligned incentives and allowed the market to determine which level is optimal?

We propose $EGL: a coordination token to allow holders to vote on what their individual desired Ethereum Gas Limit is, and reward miners for listening to the community and user preferences.

The design is simple: $EGL is a coordination token whereby holders vote on their designed adjustment to the existing gas limit. The collaborative choice is adjusted weekly based on a weighted-average tally, and when miners mine a block that follows the desired gas limit they can claim free EGLs.

**2. EGL Model High Level**

- Voting

EGL holders lock their EGLs (1-8 weeks) to vote on their desired gas limit, which must be within 4M gas from the chain’s actual gas limit.
- Votes are tallied and weight-averaged weekly, based on EGL amount and lockup duration.
- The desired gas limit is set to the weighted average, but no more than 1M gas above/below the chain’s current gas limit.

Miner Rewards

- Mining pools can include a transaction which sweeps “free” EGLs whenever they mine a block. Their reward depends on how closely the block’s gas limit matches the desired gas limit.

Ethereum Community Launch

- Pools will not be incentivized by a worthless token, so EGLs must be bootstrapped with value.
- Anyone with ETH can participate in the EGL Launch by locking up ETH to be matched with EGLs and deployed to an ETH-EGL pool. Participants will also receive additional EGLs to be used for voting. In this way, launch participants are both long ETH & EGL and users (voters) of the protocol.
- Resulting Pool Tokens and EGLs are released between 10 to 52 weeks based on time of participation (earlier participants release first)

DAO

- EGLs are to be distributed in the future to support further development, security audits, etc. Allocation of these funds is decided upon by the EGL voters as part of the voting process.

Core Devs

- While PoS usually refers to capital stake, it is obvious that the core devs are among the most important stakeholders (regardless of their capital). Furthermore, the Ethereum ecosystem would greatly benefit from the guidance of the Core Devs, and from insight into their individual preferences for the gas limit.
- Each and every Core Dev is entitled to receive EGLs, locked for a period of a year, to vote on the gas limit and guide the community.

**3. FAQs**

**Scammers and traders will just vote the gas limit to the moon! Isn’t that unsafe?**

In short, no.

First, the EGL protocol only allows for a slow and gradual change in the gas limit. Specifically, it can only adjust the gas limit by up to 1 million gas each week. That means it would take many weeks to drastically change the gas limit.

Second (and more importantly), EGL is designed to empower long-term actors over short-term opportunists, and incentivizes key stakeholders to participate. Have Coinbase, Pantera, Polychain, Consensys, a16z, USV, et al, each with billions of dollars at stake on Ethereum,take the time and effort to study the gas limit at depth, considering the different aspects, implications and opinions to help solve this issue? It’s unlikely.

And why would they?

It’s not something they can affect, and “it’s technical” somewhere between the Core Devs and miners. However, if the gas limit becomes something that anyone with ETH can vote on, you bet they would invite Core Devs to explain the different issues around it, they’ll reach out to the different client developers for their different perspectives, they’ll consult their internal engineers and experts, and eventually vote towards what they believe is best for ETH to succeed. In fact - many have already expressed their interest. The invested interests of these large actors are orders of magnitude larger than traders and scammers.

Decentralization (limiting state growth) matters, but it is something that must be balanced with user preferences and affordable access to the blockchain. Right now user preferences have no entry in the calculus at all. Users should have some say, after all Ethereum should answer the needs of a diverse collection of stakeholders, not only decentralization maximalists. In addition, all long term actors (be they the unorganized masses or large actors) who are betting on ETH’s long term success can easily increase their vote’s weight by locking up their EGLs for longer - a step which is almost unimaginable for short-term opportunists.

Third, pools would not follow the EGL vote if it leads them to substantially higher uncle-rate. Pools are not rewarded with EGLs for mining uncle-blocks. Thus, any gas level that increases their probability of mining an uncle block also decreases their utility function and is thus not profit maximizing.

For those math inclined, a miner’s utility function can be thought of as:

Upool=R+fee()+EGL(,)·ETH()

Where R represents the block reward, represents the gas limit, fee() represents fees earned as a function of , ETH() represents the value of ETH as a function of and its effect on the chain’s security, and EGL(,) where represents the collaborative desired gas limit, and EGL(,) represents the EGL reward pools capture as a function of and .

EGL thus allows users and core devs to express their collaborative desired gas limit and to affect the pools’ decision making, without compromising the pools’ incentive to maintain the network’s security and health.

**Doesn’t EIP-1559 make EGL irrelevant by solving the whole fees thing?**

No.

In fact, EIP-1559 (which we support) increases the need for EGL.

As most people know, EIP-1559 doesn’t solve this whole “fees are high” thing. It does make fees more predictable and works better than the first price auction (FPA). However, when many people try to send their Tx and the capacity is limited, the most valuable Tx will outbid the less valuable (i.e. pay a higher fee). EGL the ecosystem helps to collectively signal what capacity (gas limit) they think is right.

More importantly, EIP-1559 completely removes the incentive for pools to increase the gas limit, even if everyone agrees it is completely safe. Why should they? Producing larger blocks would only increase their risk of uncle blocks, but would hardly increase their revenues (since fees are burned). EGL actually provides a missing piece to EIP-1559 - an incentive for pools to adjust the gas limit as long as it’s safe.

We also realized that $EGL might be the perfect bridge to smooth the transition to EIP-1559. EGL aims to reward pools substantially, potentially similarly to their expected revenues from fees, thus it might allow for pools to maintain their expected revenues while benefitting users with EIP-1559 superior monetary policy and fee predictability. This is possible since the value created by EGL should suffice to compensate pools, alleviating the argument whether the value from fees should compensate pools or be burned.

**What about ETH2.0 and The Merge? What then?**

EGL is fully compatible with ETH 2.0 (well, to the extent we know what next phases look like), but more importantly aims to improve the functionality of ETH1.x in the immediate term, regardless whether it is merged into the beacon chain or not. The move from PoW to PoS does nothing to eliminate the need for the ecosystem to reach a collaborative decision on the right gas limit (block size), whether systematically or per-shard.

**The gas limit should be decided by core devs, and them alone. Stupid rich people shouldn’t have a say.**

The importance of the Core Devs cannot be overrated, but:

1. Not all core devs have the same opinion.
2. I don’t think we want ETH to follow the footsteps of BTC, especially since the need for its own chain originally started with the concern that BTC core devs are going to shrink op-return even further.
3. Those most familiar with the code don’t necessarily have the quickest grasp of the value of new use cases (see BTC above). On the other hand, some of the largest actors are managed by very bright people, who hire even brighter people, and their different perspectives are actually critical.

A mechanism which gives some influence to core devs, and also showcases their different opinions to the entire ecosystem, benefits from the best of both worlds (technocracy & PoS).

**OK, this might be a good idea, but why use a token? Why not just use ETH?**

We spent a lot of time trying to remove the token from the design, to no avail. It boils down to bundling (include the functionality in ETH) vs unbundling (a separate token).

If you bundle the functionality into ETH, participants invest time, money and effort, while the benefits are shared with all ETH holders and users equally. That’s both, a drop in a bucket and a classic Tragedy of the Commons, eroding the incentive to participate.

By unbundling the functionality, most of the benefit of finding the optimal safe gas limit is still being shared by all ETH holders and users, but some is accrued directly to the token holders. Specifically, those wishing to hold EGLs to ensure the gas limit continues in the “right direction” (whatever that direction is) create a demand for the token, increasing the value of EGL, and benefitting participants.

**What happens to EGL when everyone’s happy with the current gas limit? What’s the incentive to participate? Would everyone just sell?**

EGL has a built-in mechanism to begin rolling backwards if there’s not enough voting participation. That means that even if the gas limit reaches the level everyone is happy with, without continuous participation it will roll backwards. While the ETH community includes many different perspectives on the optimal gas limit at any given time, most members of the community support either maintaining the current gas limit, or increasing it, while those supporting reducing the current gas limit are a minority. As such, reducing the gas limit (which would increase the gas bidding competition among transactions) is a dissatisfying outcome for most ETH users and actors.

Leveraging this preference, EGL’s default outcome when failing to reach a vote is to reduce the gas limit, not keep it unchanged. This unconventional design choice means that lax actors would likely be dissatisfied with the outcome and are better off participating. For example, large actors and their customers are likely to be negatively affected if and when a large portion of them decide not to vote.

**Can EGL be used to make other decisions?**

Yes!

While EGL is initially designed to affect the gas limit, its use as a coordination tool can be extended to other on-chain aspects. For example, mitigating MEV, delegation of voting rights, discourage selfish mining, mining decentralization, or transparency of node diversity.

**4. What now?**

This post serves to start a conversation about EGL. In the coming weeks we will launch our Discord and Forum. In the meantime, to stay up to date, follow our Twitter handle [@ETH_EGL](https://twitter.com/ETH_EGL) or sign up at egl (dot) vote to our mailing list.

## Replies

**AlexeyAkhunov** (2021-04-29):

Interesting proposal. I am sure you put a lot of thought into it, probably much more than I will be able to. But, as promised, I will write down what I think about gas limit.

Currently, the discussion about gas limit usually touches on the question about what the “safe limit” is. It usually composes of 2 things:

1. What is the worst-case block execution given certain gas limit. We know that bottleneck in some specially crafted worst-case blocks is state access. Depending on how it is crafted, different state layouts (like Geth snapshotter, and turbo-geth plain state) and presence/absence of bloom (or similar) filters in front of state access, make significant difference there. However, it is still possible to craft a worst-case block that would, say specifically target turbo-geth, and still result in long processing time (though other implementations are likely to suffer much more on the same blocks). Also, as I realised recently, precompile pricing calibrations are performed under assumptions of 40Mgas/sec (or even 25Mgas/sec perhaps). It is clear that with such calibrations, precompiles will become bottleneck for the worst case performance sooner or later.
2. What is state growth given certain gas limit. Again, here we can easily sketch a worst case growth, which however is likely to be quite unrealistic.

So is it possible to increase the gas limit above the limitation dictated by worst case performance? It seems that the answer is “no”. But I think it is “yes”. I believe this can be done through decoupling of worst-case performance (what we are afraid may happen) and average-case performance (what actually happens most of the time). It requires some architectural changes though. Here is the idea. First, we decouple transaction pool (miner/block proposer will be located inside this transaction pool component). Sort of like shown on this diagram: https://github.com/ledgerwatch/interfaces/blob/4b95458a4f48aa11112c81e5af4c4107671dd368/turbo-geth-architecture.png?raw=true

This separation of transaction pool (it is not super hard, we should get it this year) allows a crucial improvement - the ability of running multiple instances of transaction pool per “Core”. Why is it crucial? Lets imagine that the worst-case transaction that executes really long time (but is still within the gas limit) is an “execution bomb”. Someone creates such a “bomb” and relays it over the network. Currently, because it passes simple checks like account having enough ETH to pay for gas, and no nonce gaps, it will be relayed all the way to the miners/block proposers, at which point it is likely to “explode” their “Core” engine that does the mining, delaying the composition of the block, therefore increasing probability of serious of empty blocks, and therefore reducing the capacity of Ethereum. Now lets imagine that some miner/block proposer managed to include such transaction into a block (perhaps it was intentional), and now this block propagates. It is quite likely that this block will be orphaned, because any miners/block proposers that are trying to import it to compose new blocks over it, will be delayed and lose the race to the new block. Therefore, it is not in miner/block proposer’s interest to even include such execution bombs, unless they possess clear majority  and want to squeeze everyone else’s revenue.

So, my conclusion from the above is that

1. There needs to be a mechanism for miners/block proposers to detect execution bombs when they come inside the block. This can be achieved by simply timing out the execution and orphaning the block if it exceeds certain reasonable time limit.
2. There needs to be a mechanism for network participants who relay transactions to detect and stop relaying transactions that carry execution bombs. This can be achieved by the practice of running multiple transaction pools per “Core”, and using this to pre-execute all transactions before relaying. Here again, transaction is thrown out after exceeding a time limit. And having multiple tx pools and randomly assigning transactions to them helps prevent clogging up the pools by just one bomb. In order to make repeated bomb production more costly, transaction pools may introduce ban on the replacement of the “bomb” transactions with the transaction from the same sender and nonce, for some time (several hours?). This will make sure that whatever is in the sender’s balance will effectively be temporarily locked.

These are pretty rough ideas, but I would like to try them out on a devnet/testnet

---

**uri-bloXroute** (2021-04-30):

That’s super interesting. A few thoughts:

1. thinking about it as “compartmentalization” and bomb exploding is very intuitive - I like the analogy
2. I think we should always consider the cost of an attack. For instance, if it costs $x to mine 1% empty blocks, using this attack is x2 more effective (you produce a valueless block and cause the next block to be empty). Is that major? maybe. maybe not. There is always a possibility to attack the network - I can try to DDoS the entire internet - and the question is how hard/costly it is.
3. Your outlines a proposal to make increasing the gas limit safe. But EGL is not about increasing the gas limit. Maybe the right choice is to keep it as it, or even decrease it. EGL allows:

- Each core dev to signal what she thinks (the twitter discussion includes like 4 core devs + Vitalik)
- The entire ETH ecosystem to reach a collaborative decision (with large stake holders with $Bs at stake obviously having more $ and more weight - PoS)
- Pools to get clarity on the community desired gas limit, and incentive to follow it

I *personally* think that the 12M gas limit was too conservative, but nobody cares or should care what I think. With EGL, everyone can try and engage core devs and the community at large, and try to affect the gas limit. Nowadays its not even an option - it’s a decision being made by the top-3 pools

---

**AlexeyAkhunov** (2021-04-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/uri-bloxroute/48/9412_2.png) uri-bloXroute:

> Your outlines a proposal to make increasing the gas limit safe. But EGL is not about increasing the gas limit

Yes, sorry, I am squatting in your topic, just because I said I would right what I think about block gas limit. But I am thinking about EGL too

---

**uri-bloXroute** (2021-04-30):

No worries - I like squatters and I **honestly** eager to hear how turbogeth are thinking about it. There’s literally no structured discussion about it (since there’s no point - top-3 pools are currently deciding it)

---

**tkstanczak** (2021-05-20):

1. would the vote happen on chain and people would have to issue transactions?
2. currently we have some meritocracy in the gas limits settings with maybe 20-100 people involved - if we add a token constructed in the suggested way i do not expect the number of decisive votes to be higher than that (and the vote will no longer be meritocratic but capital based?)
3. I feel like the justification of the mechanism is very soft and does not show entirely how it would lead to improvements in finding the best gas limit. How far is the current gas limit from optimal? What does it take into account - latency? storage? propagation? economical aspects? ← we would need to analyze all of these under both mechanism.
4. Currently the incentivization to set the gas limit right is very strong → reputation, network stability, security, ETH price. I believe that the token would not be stronger incentivization.
5. “Each and every Core Dev is entitled to receive EGLs, locked for a period of a year, to vote on the gas limit and guide the community.” ← you will never be able to provide a fair list of core devs so this part of the mechanism will not work
6. If you think about incentivization → suggested solutions practically takes away power from core devs and moves it entirely to miners but it does not take into account that the core devs have collectively power to reject or modify the solution.

My gut feeling is that this solution is flawed and unnecessary but I like the discussion and I read this. It may lead to something cool if researched further.

---

**tkstanczak** (2021-05-20):

Without EGL also anyone is able to engage with core devs and community at large. I would say with EGL, the holders would somehow be meant to have more to say? The actual power will remain in the hands of pools and core devs so the token will just have some negative impact of having financial incentive into something that has worked well for the last 5 years by having reputation + security incentive for people who care about the topic.

---

**rai** (2021-05-21):

Thanks for the writeup! I agree that the discussions can get messy around this topic but I’m not sure we have the tools to fix it without losing desirable properties.

If we try to make this in-flight system more legible and codified we’ll likely fail to correctly design a distribution mechanism that encapsulates the nuances going on in the discussion. The matter of core dev selection, as Tomasz mentioned, seems like enough to make this proposal as it stands untenable.

Either:

- We make core devs generate EGL for themselves
- We allot them some (as in the propsoal)

The second one fails for lack of credible neutrality. The first fails because the resulting distribution wouldn’t map onto the current community-implied distribution of expertise.

---

**eleni** (2021-05-24):

Thanks [@rai](/u/rai)! I agree with most of your argument, especially that credible neutrality is key for successful mechanisms.

The point where I disagree - which was also lost on [@tkstanczak](/u/tkstanczak) so we should probably make more clear - is the importance of the distribution to core devs, compared to the distribution to other ETH holders.

In most crypto projects the initial distribution is key, but not here. We intend to award EGLs to the core devs:

- because they deserve it
- for their vote to signal to the community what they think.

Core devs are awarded enough EGLs to be meaningful, but nowhere close to allow them to call the shots directly. Their individual votes however matter as a reference point for the larger community.

If Vitalik, Peter, Alexey, Micha and yourself all vote for 15-17M gas, it allows any ETH large stakeholder, whether businesses (Coinbase), investors (Polychain) or users (the unorganized masses of Uniswap LPs), to take that into consideration along their own inputs and experts, and make an informed vote.

If EGLs were just awarded to the core devs to vote and decide the gas limit, I would agree with you, but they are awarded EGLs to vote and **signal**, not vote and decide, which I believe makes the question of who exactly is a core dev and the initial distribution x100 less important.

If EGLs are awarded undeservedly to some rando, it doesn’t matter, since his signal won’t have the same effect as the voting of prominent core devs.

---

**rai** (2021-05-24):

Ah, that’s a good clarification. I didn’t realize that you intended for it to be more of a signaling mechanism. I’ll think about it some more then.

