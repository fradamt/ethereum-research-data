---
source: magicians
topic_id: 23309
title: A simple L2 security and finalization roadmap
author: vbuterin
date: "2025-03-28"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/a-simple-l2-security-and-finalization-roadmap/23309
views: 8350
likes: 34
posts_count: 22
---

# A simple L2 security and finalization roadmap

*Special thanks to various EF, Optimism, Taiko, Flashbots, Surge and other researchers who helped form my thoughts on this.*

Today, the state of L2 security and L2 finality guarantees is improving: we now have three rollups at Stage 1, we are on the cusp of rollups getting more blob space with Pectra and then [even more with Fusaka](https://x.com/tkstanczak/status/1895864644587471141), and we have more and more [high-quality ZK-EVM options](https://ethproofs.org/) that would allow much shorter finality times. Where can we go from here?

## 1. More blobs

This has already been discussed in other places; a target of 6 for Pectra, and 72 for Fusaka in Q4 (or, alternatively, 12-24 in Fusaka in Q3, if it is followed up with rapid further increases) feels like it is adequate to L2s’ needs.

## 2. Pragmatic fast finality via 2-of-3 OP + ZK + TEE

I argue that the best short-term proof system architecture for EVM rollups to get to stage 2 is a 2-of-3 between optimistic, ZK and TEE-based provers. Specifically:

- If a state root is approved by both a ZK prover and a TEE prover, then it is finalized immediately.
- If a state root is approved by either the ZK prover or the TEE prover but not both, then it is finalized after 7 days only if the optimistic proof game also unambiguously favors the state root.
- There is (optionally) a security council, which has the right to update the TEE prover logic with zero delay, and the ZK or optimistic prover logic after 30 days of delay.
- Potentially, we can give the security council upgrade rights in other specific contexts, eg. if a proof system provably disagrees with itself, we could allow the security council to upgrade it instantly.

This specific architecture is designed to simultaneously satisfy three goals:

1. Provide instant finality in the normal case
2. Satisfy the core stage 2 criteria, particularly (i) the requirement that if the “trustless” proof systems work, then nothing “semi-trusted” (either TEE or security council) is able to override them, (ii) the 30-day upgrade delay
3. Avoid short-term over-reliance on ZK. Today, ZK proof systems still have a high enough rate of bugs, and shared code, that it is very plausible that either (i) there is a bug in shared code that affects multiple proof systems, or (ii) an attacker finds and holds on to a bug in one proof system for long enough that they discover a bug in the other.

In fact, the above architecture is arguably the *only* way to do this. Specifically, if for simplicity, you want a 2-of-3 proof system architecture, and ZK, OP, TEE and SC (security council) are the four “proof system” options, then:

- (1) implies zk + tee >= 2 (OP and SC are both too slow)
- (2) implies tee + sc < 2 (non-trustless things cannot finalize on their own)
- (3) implies zk < 2

`zk = 1`, `tee = 1`, `op = 1` is the only solution to this system of constraints.

The risk that a ZK system and an OP system will both have bugs (that are found by the same party) is much lower than the same risk for two ZK systems, because ZK and OP are so fundamentally different. In fact, it’s acceptable for the OP system to be ZK-OP (ie. one-round fraud proof via a different ZK-EVM), because the risk that one ZK-EVM has a soundness failure while the other ZK-EVM has a completeness (ie. liveness failure) is much lower than the risk of two soundness failures.

This gets us to a pragmatic higher level of fast finality and security while getting us to the key stage 2 milestone of full trustlessness in the case where proof systems (OP and ZK) work correctly. This will reduce round-trip times for market makers to 1 hour or even much lower, allowing fees for intent-based cross-L2 bridging to be very low.

## 3. Work on aggregation layers

Realistically, we are already on a trajectory to get ZK-EVMs generating proofs in one slot. This is because this is necessary for L1 use of ZK-EVMs. In fact, a very strong version of this, where we get single-slot proofs *even in the worst case*, is necessary for L1 use. This also creates a pressure for the rapid discovery and removal for the main class of *completeness* bugs in ZK-EVM: situations where a block has too many instances of some particular type of ZK-unfriendly computation. The [verified ZK-EVM effort](https://verified-zkevm.org/) will also work to reduce soundness bugs, allowing us to hopefully phase out TEEs and go full-trustless in a few years.

The thing where we are currently relatively behind is Ethereum-ecosystem-wide standardized *proof aggregation layers*. There should be a neutral ecosystem-wide mechanism by which a prover in any application that uses zero knowledge proof systems (L2s, privacy protocols and zkemail-like wallet recoveries are the most natural initial use cases) can submit their proof, and have one aggregator combine the proofs into a single aggregate proof. This allows N applications to pay the ~500,000 gas cost of proving *once*, instead of N times.

## Replies

**TimDaub** (2025-03-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> This has already been discussed in other places; a target of 6 for Pectra, and 72 for Fusaka in Q4 (or, alternatively, 12-24 in Fusaka in Q3, if it is followed up with rapid further increases) feels like it is adequate to L2s’ needs.

Can we please properly motivate this publicly?

The public motivations I have read so far follow a “we’ll increase the blob limit because we can” argument.

I’ve seen cases where people say that we have to keep blobs cheap because at their current price point they don’t have a moat. This was only said to me privately.

A lot of “increase the blob limit” motivations were also written in different periods (vibe wise). I feel like many of the motivations were written in anticipation of a major bull market where more DA capacity would have been necessary. But this has, so far, not turned out to be an accurate prediction.

Can we please create transparency around increasing the blob limit and officially post the data and our thinking here on why we’re increasing the blob count? E.g. Base has motivated the blob count increase by arguing that their users’ transaction costs are too high, which is just really unreasonable as their txs costs are consistently below 0.01 USD. Besides, Ethereum captures so little value from Base that they can probably even subsidize their users’ gas costs while still being profitable, can’t they?

Blobs do have a moat [from what I know](https://hackmd.io/4u6eL7NOSE2_a1wHzffqoA), but they may have more of a moat further down the line? What is the thinking here? What can you share the ideas with us? Or is this giving away too much strategic advantage? I’m almost feeling like some information is strategically retained by decision makers.

Consider, I’m not an ETH researcher with deep insights into the mechanisms and I also don’t talk to one every day. It took me many days to get up to speed on why some people here want to increase the blob count. In my naive logic more blob supply means again less fee accrual, which again makes me worried for the Ether that I hold and its price.

---

**Tobi** (2025-03-31):

Please trust your intuition [@vbuterin](/u/vbuterin). After now roughly a decade in the blockchain space I learned that people think very differently and many (even technically capable people) just don’t have intuition for greater / more broad things.

But in the complex and chaotic world of social interaction / economics / game theory there are often no hard facts to proof that intuition. Other projects are free to explore different paths… and people are free to sell their ETH if they think ethereum is going towards a wrong direction and follows a misguided path.

But still let me try to put that intuition into words (even though after all that time I’m not very optimistic that people who don’t get it will do so because of it):

Internet native software - and especially open source software based blockchains born and bred there - live in a highly competitive environment. Network effects provide some stickiness but in the long run only those will survive and thrive that offer the maximum utility to their users (and thereby maybe at some point to the whole world). This is because everything can be copied. It’s all public. Code is just information and can travel from A to B by the speed of light. So to maintain a leading position you cannot rely on your first-mover advantage for long. Others will catch up, and improve what you didn’t improve or offer users what you don’t offer. So ethereum must use its momentum and resources to stay ahead. Keep offering the maximum utility among all available alternatives.

This maximum utility - in the context of blockchains - translates to the absulute minium possible transaction fees while maintaining additional crucial blockchain properties that offer utility - and set blockchains apart from just servers. These other utility properties are immuntability and censorship resistance.

With blockchains it is like every software developer now has a magic tool in their toolbox to just upload code to a chain and thereby making it practially immortal - available for everyone, everywhere. This is incredably powerful and ethereum is correct in making sure that these properties must be maintained. Still to maximize the usefulness of this - transaction fees must go down further. Lots of applications that are easiliy to imagine are still too expensive to run on a blockchain, even with current fee-levels. Now one can ask - which applications are these? There’s no evidence of them. Well I do see evidence but you have to look close. People questioning the need or usefulness of any decentralized mass scale application have an easy position (until now) because we do not see them yet… But of course don’t do yet. This is because a platform for them that has low enough fees and still immutability and censorship resistance is not available yet. There are certain ideas that only now slowly make sense to start working on as L2s are on the verge of getting cheaper and fully trustless.

Regarding the point of L2s being parasitic… that will sooner or later go away when some L2s will emerge that simply use ETH (e.g. via restaking) to run validators and sequencers.

So…

1. L2s being ETH-friendly (or even run with ETH as their sole token) will have a competitive advantage as the base of ETH holders is bigger (and more enthusiastic and idealistic about using the tech) than any other token (especially still non-existant ones). It is not easy to widely distribute a token among believers (note that this will change if ethereum doesn’t compete strongly enough)
2. Even if 1. weren’t true… there’s simply no alternative to keep maximizing utility by non-stop working on decreasing transation fees while maintaining immutability and censorship resistance because blockchains live in a highly competitive environment. Even if L2s would take 95% of the cake, these 5% a highly competitive ethereum will maintain will be more significant than an outdated and comparatively expensive ethereum that lost its network effect in a few decades from now.

---

**kladkogex** (2025-04-01):

Below are the fees that rollups currently pay to the ETH mainnet

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/8/8bf555e47605cf72205302c144fbf985b25db0ff_2_690x212.png)image1625×500 132 KB](https://ethereum-magicians.org/uploads/default/8bf555e47605cf72205302c144fbf985b25db0ff)

These are already tiny amounts

And here is a typical Base transaction - it shows that Base pays a tiny propotion of total user fee to ETH mainnet

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/b/b9dc2b2b5ee9f5c7c5b0fead892efcef4a0be09f_2_690x161.png)image1365×319 59.9 KB](https://ethereum-magicians.org/uploads/default/b9dc2b2b5ee9f5c7c5b0fead892efcef4a0be09f)

And here is the current dominance of Base

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/0/041092f2dbf252657a63fbcf9f83b0d8ec47acfc_2_655x500.png)image815×622 101 KB](https://ethereum-magicians.org/uploads/default/041092f2dbf252657a63fbcf9f83b0d8ec47acfc)

It is easy to predict evolution if blob space grows 10 times - essentially L1 fees which are already miniscule will drop to zero, and there will be a single rollup surviving, which is Base

It is already estimated that Base shaved 50B USD of Eth market cap.

Moreover, Base has no plans to decentralize, and there is no economic model for anyone even provide Base fraud proofs, since running a fraud-detecting system in parallel to Base will cost lots of computational power.

---

**vbuterin** (2025-04-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> Can we please properly motivate this publicly?

The motivation for 10x’ing blobs is simple. We know for a fact that there are lots of L2s, both currently live and in the works, that are ready to bring thousands of TPS online. This TPS can either come online in a format which is trustless (which requires both sufficient blob count and adoption of a practical stage 2 roadmap like what I wrote above), or it can come online in a format which is basically a separate L1 barely connected to Ethereum.

It’s far better for us to have the former.

If the concern is that L2s are not paying enough gas, then we should fix that by setting a minimum blob gasprice. That way L1 can get paid and at the same time L2s get certainty that a sufficient level of capacity exists to handle their needs, even if their application sees an unexpectedly high level of success.

Additionally, if we decide to greatly increase the ethereum L1 gas limit itself, at some point we will need to rely on ZK proofs and rely on blobs to store execution data, because nodes would not be able to fully download the entire execution data directly. So blob count increases are a necessary waypoint among any realistic ethereum scaling plan that goes above ~1k TPS.

---

**TimDaub** (2025-04-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> If the concern is that L2s are not paying enough gas, then we should fix that by setting a minimum blob gasprice. That way L1 can get paid and at the same time L2s get certainty that a sufficient level of capacity exists to handle their needs, even if their application sees an unexpectedly high level of success.

You say EIP 7762 addresses both that

1. L2s will pay their fair share for using Ethereum; and that
2. L1 will get paid?

This is an extra ordinary claim that is very hard to evaluate as someone who’s not an Ethereum researcher. I do see the Dune charts in EIP 7762 and they look promising. But as an Ethereum investor, I’m anchored to the expectation that Ethereum’s fee accrual is roughly 100x less of what its market cap is. So if in 2024 2B USD in fees were accrued to ETH investors then a 200B USD market cap seems fair. As an Ethereum investor, I’m also anchored to the idea that there’s a mechanical connection between the protocol’s ability to accrue fees and its market cap and that arbitrage will keep these connected.

- EIP 7762 discussions focus on the 1 wei blobgas minimum parameter having been set wrongly and needing too many blocks to scale up blob price => not a fundamental proof that this will get the L1 paid, it lacks a projection calculation IMO. EIP 7762 discussions don’t center around “getting the L1 paid” IMO.
- The EIP 7762 charts, which show that more blobs will be priced with the minimum blob gasprice are encouraging but they don’t project that we’ll earn 10x more either.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> at the same time L2s get certainty that a sufficient level of capacity exists to handle their needs, even if their application sees an unexpectedly high level of success.

I personally have zero doubts about you and others’ ability to scale Ethereum. I frankly don’t understand the L2s’ logic here. Why do we as Ethereum have to prove to them that we can scale? Do they know something about Ethereum scaling that others don’t? E.g. that there’ll be difficulties down the road? A tangential question is: Where else could they go for the same level of security if they had unexpected high levels of success but Ethereum doesn’t scale?

Personally, I’m actually more worried about the short to mid term pain of having to hold Ether while we capture DA market share. My understanding is that the L2+DA breakthrough is deflationary to the price of transacting on secure blockchains like Ethereum and that my anchoring in past fee accrual statistics has become unreasonable since EIP 4844 shipped. Still, I don’t think we can argue away that there are many in my painful position who have been locked into ETH price at around 2000 USD. How do we motivate to them that despite their bad entry price we have to keep capture DA market share instead of focusing on fee accrual?

Frankly most of my concerns center around Ethereum pricing blobs with a mechanism that triggers only on congestion, and at the same time the Ethereum researchers are constantly working to improve congestion with technical breakthroughs. Perspective wise this doesn’t inspire optimism for more fee accrual in the future. Maybe then we must not price blobs through a congestion mechanism anymore, but differently?

---

**kladkogex** (2025-04-01):

Hey Vitalik,

I think it is really good that you’ve started communicating with people, which includes responding to their thoughts.

Ethereum needs to respond to reality, which means having an economic model and also **having meaningful governance and democracy**. It is understandable that initially the more effective thing was you controlling it personally. But now it is actually more effective to release the power; otherwise, people will leave. They are leaving Ethereum because they do not see transparency in decision-making or balance. Things are controlled to the point now that it is impossible to meaningfully express disagreement. People who have opposing views are literally banned from Devcon. Even the Ethereum conference does not have any democracy — I am not even talking about transparently deciding how the Ethereum Foundation spends its money.

I understand that you made a decision to prioritize L2 vs L1, but there are opposing views. Unfortunately, in the past, you have chosen not to respond to questions that are important to the community.

1. The current official view that you have about L2s simply does not correspond to reality. You say there are many L2s — this is simply not true. There is only one L2, Base, which is doing well, and all others are dying, basically waiting until their token price goes to zero.
2. There is no technology in Base L2; it is simply a single-node EVM. They have no intention to decentralize. You have chosen to be silent on this elephant in the room. They will not be able to decentralize since they now pocket all the fees, and a decentralized system will not run fast enough even to match their current speed.
3. Base is uncontrolled because there are no fraud proofs, and there is no economic model for anyone to run an economically viable system producing the fraud proofs, because the only entity that can pay the fraud proof creator is Base itself. Essentially, this all becomes a joke — Base will have to run two corporate departments controlling each other.
4. No one has ever produced an economic model for a decentralized rollup. You have been talking about rollups for years, Vitalik — please provide a reference to a paper describing this thing. All currently running rollups are centralized. What was the entire point then?
5. Over the years you,Vitalik was very specific that all blockchains in the Ethereum community had to post all data to Ethereum mainnet.  To the point that Ethereum foundation specifically attacked people that did not post to the main net. I never understood what was the entire idea about  that.  Now we have Base posting data to Eth mainnet. Are we happy about it ? They are totally centralized, they do not have fraud proofs, they pocket the fees, essentially they are a centralized bank that posts transactions on blockchain. People that use Base could not care about this bv the way, if something goes wrong they will not use fraud proofs, they will simply sue Coinbase. I love Coinbase, they are a great company, but this has nothing to do with blockchain.
6. Sometime ago, you said that you see yourself as a “high priest”. Do you still think it is a good description of the way you want to interact with the community?  I personally do not like it, I think priests per say do not accept any criticism and do not listen to opinions of other people, they only listen to “God” which is basically self-reference to themselves.

As far as blob fees go, I think the right thing to do is to **destroy the boundary * between blob fees and L1 fees. There has to be a competition between blobs and L1.   Computation is cheap and EVM can easily run way faster.  Writing to the state is expensive, although with parallel state databases it can be done way faster too.  If people want use blobs thats fine, but artficially making blobs price low is not good.

---

**Tobi** (2025-04-02):

> As far as blob fees go, I think the right thing to do is to **destroy the boundary * between blob fees and L1 fees. There has to be a competition between blobs and L1. Computation is cheap and EVM can easily run way faster.

[@kladkogex](/u/kladkogex) The boundary is not arbitrary. It is not a subsidy. The reason it is priced differently is because that data is actually much less of a burden to the ethereum network because the data can be forgotten. It is dropped after a certain period. In contrast to that writing state is so expensive because - before some clever not yet clear state expiry is implemented - has to be maintained forever.

---

**kladkogex** (2025-04-03):

Hey Toby

Writing to the state is expensive, but adding data to the blockchain is not expensive.  Most nodes do not keep blocks starting from time zero. Therefore, call data could be as inexpensive as blobs, may be a little more expensive but by not much.

Having blob price essentially zero compared to call data creates unfair disadvantage to L1 as compared to L2. It can not be justified economically. And now there is a proposal to increase call data price even more, which again makes no sense economically, it is a political thing to make usage of Layer 1 even harder.

---

**vbuterin** (2025-04-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> Frankly most of my concerns center around Ethereum pricing blobs with a mechanism that triggers only on congestion, and at the same time the Ethereum researchers are constantly working to improve congestion with technical breakthroughs. Perspective wise this doesn’t inspire optimism for more fee accrual in the future. Maybe then we must not price blobs through a congestion mechanism anymore, but differently?

Isn’t EIP-7762 a solution to this exact problem? It ensures that blobs have a price which is substantial, and is always active regardless of congestion conditions. This also aligns incentives, as it means that people who want scale and people who want value accrual have the same goal (increasing blob count). If EIP-7762 as-is is not enough, then wouldn’t a simple solution be: EIP-7762, but with a higher minimum fee?

> Having blob price essentially zero compared to call data creates unfair disadvantage to L1 as compared to L2. It can not be justified economically.

There is a big difference between calldata and blobs: calldata is data that all ethereum nodes must have access to in order to be able to verify a block. Blobs are not, because EVM is not allowed to access blob contents. This makes blobs friendly to peerdas and other tech, in a way that calldata fundamentally is not.

---

**kladkogex** (2025-04-11):

Hey Vitalik,

Respectfully disagree. Most Ethereum nodes store only 128 blocks. There is very little reason for anyone to store the entire history of blocks from the beginning of time, except for a company like Etherscan.

In fact, it is in most users’ interest that Ethereum blocks are lost, because keeping all blocks from the beginning of time creates an Orwellian violation of privacy—essentially, anyone can be held accountable forever for anything they did in life.

So there is no major difference between CALLDATA and blobs. Even if you believe that CALLDATA is more expensive, one could set the blob fee per byte to be, say, 10 times less than CALLDATA.

There was no reason to separate the markets. Would you agree that the current situation—where **blobs are infinitely cheaper** than CALLDATA—is suboptimal?

The Ethereum Foundation should not prescribe how people should do things, just as Linus Torvalds does not tell people how to use the kernel. People use it however they want. When the Ethereum Foundation expresses opinions on everything under the sun, and then the network is forcefully modified to reflect a particular point of view, it becomes a recipe for disaster. The unfortunate reality is that people want money, which creates an absolutely toxic environment where the opinion of a “high priest” becomes idolized.   I have seen many people that learn these opinions by heart without having any understanding, and then very effectively attack those who express even a tiny divergence from the party line.

It’s gotten to the point where people are actually afraid to speak. I’ve had incredibly funny moments at conferences when I tried to discuss interesting security questions around Ethereum consensus with some ETH client developers receiving grants from the Ethereum Foundation. They would literally freeze. From that, I concluded that many of them had little understanding of why consensus works the way it does. And I also suspect they thought I was crazy for publicly questioning the gods. I must say, the last time I experienced something like this was in the Soviet Union.

So the problem goes far deeper than the CALLDATA price vs. blob price. **All the arguments above may be absolutely wrong**, just a misinformed opinion from a random person. The direction the Ethereum Foundation is taking might be absolutely perfect, a genius contribution to computer science. The real issue is the toxic environment that doesn’t allow for open discussion and self-selects people who are willing to accept anything as truth and immediately change their opinions. *If people don’t discuss things, how can anyone differentiate between what’s true and what’s false?*

Like with rollups, it just seems like a random set of things coming from the top. First, Plasma was the solution, then Rollups were great, followed by ZK Rollups being better than Optimistic Rollups. All of these rollups have never  decentralized, never implemented fraud proofs; they’re essentially centralized single-computer systems.

Now, we have Base Rollups and Native Rollups as the latest “new thing.”

In all these cases, people have instantly changed their minds, forgotten the old solutions, and started worshipping the new ones without understanding them—just like they did with the old ones. It’s incredibly amusing to an outside observer to see how many times this has happened. Wouldn’t it make sense to have a retrospective to discuss the mistakes of the past? After all, if there were no issues with the old solutions, we wouldn’t need the new ones. Can we at least add some humor and irony to the entire process?

So, it’s not really about Plasma or this rollup or that rollup. They may all be fantastic under certain conditions. What’s troubling is the constant flipping of worships without any real understanding, and the toxic system that enables and encourages this behavior. And the endpoint of this evolution may be an incredibly slippery slope. Just look at Elon Musk. First, he was the electric car genius. Then, he decided he needed to widen his horizons, so he started expressing planet-scale opinions about relocating to Mars. Now, he’s a political genius. In each case, there was an echo chamber of people who truly worshipped him and others who made money pretending to worship him.

People buy Bitcoin because it is essentially unmodifiable, which makes it a fantastic store of value despite its imperfections. If someone buys Bitcoin for retirement savings, they can reasonably expect to have their money when they need it. Ethereum, understandably, is not Bitcoin because it wants to innovate and push the boundaries of science. But there has to be a balance of transparent governance and conflicting points of view. Open conflicts are valuable because they can lead to reasonable compromises.

![image](https://ethereum-magicians.org/uploads/default/optimized/2X/8/87bb69ef790d821a12eefedc9454b63267f4e813_2_690x62.png)

---

**Tobi** (2025-04-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kladkogex/48/8349_2.png) kladkogex:

> The real issue is the toxic environment that doesn’t allow for open discussion and self-selects people who are willing to accept anything as truth and immediately change their opinions. If people don’t discuss things, how can anyone differentiate between what’s true and what’s false?

Aren’t you discussing right now, noone is stopping you from writing here. I don’t see the problem. Not sure what experiences you made, but challenging ideas seems good to me (if it’s not just done in a trolling manner).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kladkogex/48/8349_2.png) kladkogex:

> because keeping all blocks from the beginning of time creates an Orwellian violation of privacy

I don’t see how throwing away blocks helps with this one bit. The data was still published, everyone was able to see it, so nodes throwing it away won’t help with privacy (people can keep private copies).

But apart from that I actually totally agree with you on this point… most nodes shouldn’t need to keep the history. I don’t think this is in misalignment with what most people in ethereum think.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kladkogex/48/8349_2.png) kladkogex:

> First, Plasma was the solution, then Rollups were great, followed by ZK Rollups being better than Optimistic Rollups

Looks to me like progress being made, in a still very novel branch of computer science.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kladkogex/48/8349_2.png) kladkogex:

> So there is no major difference between CALLDATA and blobs.

So calldata can result in state being written (expensive, cannot be deleted) - blobs cannot. But apart from that, even if calldata is not stored in the state, every single node needs it for its EVM state transition. How’s that not a big difference to blob data which is - in the hopefully not so distant future - only needed by a fraction of the nodes. So each node only needs a fraction of the blob data. Again, not even talking about storing here - no node needs to store it forever. I’m talking about nodes not even needing to receive it.

---

**Tobi** (2025-04-13):

[@vbuterin](/u/vbuterin) I’m actually really curious to get a response by you or someone else from the EF here about this point I also kind of made in this thread and on other occasions but never got an answer for. Would really appreciate a response:

It seems to me that many of the big challenges right now are more economically/incentive based. Wouldn’t it maybe be helpful - to lead by example … and even to heat up competition a bit - have a big player like the EF spearhead an L2 rollup that is everything we want to see from other projects? I understand that it is a major task to implement a rollup… but as I said earlier… we’re in an open source environment. There’s no shame in copying open source code - that’s the whole idea of open sourcing something: To allow others to copy it and further develop something based on it.

And as a follow-up question to this: wouldn’t it make sense to use re-staking for such an initiative? I’m not affiliated with eigenlayer and I don’t think it would be necessary to use any eigenlayer contracts to accomplish this (but it might make sense). But the general idea of running other stuff than the ethereum execution and consensus clients via eth-staking seems very powerful to me - even without the possiblity of printing ETH that restaking L2 clients would not have.

---

**amiller** (2025-04-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> I argue that the best short-term proof system architecture for EVM rollups to get to stage 2 is a 2-of-3 between optimistic, ZK and TEE-based provers. Specifically

While this post is motivated by fast finality, what do you think about OP + TEE + SC, in other words using TEE proofs to reduce reliance on the Security Council?

For example, a TEE proof could be used to create a “proof of software bug” which would justify the security council to make a faster than 30-day upgrade.

---

**Samuel.Ranellucci** (2025-04-16):

Hi Vitalik,

We are engineers and cryptographer working at Base.

Thank you for sharing your proposal on leveraging Trusted Execution Environments (TEEs) and Zero-Knowledge proofs for achieving stage 2 decentralization. We find the approach compelling and would appreciate clarification on two specific aspects:

First, could you elaborate on the TEE prover concept that was mentioned but not fully fleshed out? We’re particularly interested in understanding its operational framework within stage 2 decentralization—specifically, whether TEE proving capabilities will be restricted to a centralized authority (such as the chain itself), or if the architecture allows for permissionless TEE proof generation by any participant with the appropriate secure hardware.

Second, we’d value your insights regarding the governance time constraints—namely, why can the security council modify the TEE logic without a waiting period, while updates to the ZK logic require a minimum 30-day delay. The reasoning behind this asymmetric approach isn’t immediately apparent to us.

---

**changeschung** (2025-04-17):

It’s not dropped they used a lot of codes on that address and make it dead ![:no_entry_sign:](https://ethereum-magicians.org/images/emoji/twitter/no_entry_sign.png?v=12) unfortunately that address is me and they stole it in the first place duuh enough…!

---

**kladkogex** (2025-04-17):

Hey Tobi,

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tobi/48/10955_2.png) Tobi:

> Aren’t you discussing right now, noone is stopping you from writing here.

Well, I am discussing it here, but this message board is not managed by Ethereum Foundation.  Try applying to devcon with anything not fitting.  Twitter is full of messages from pissed people like this

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/0/08d0632c0f132700d0c7767313fe524ca5a566ad_2_690x392.png)image924×525 93.4 KB](https://ethereum-magicians.org/uploads/default/08d0632c0f132700d0c7767313fe524ca5a566ad)

Who TF are the reviewers, anyway? No one knows. It’s a joke. Nearly every scientific conference has a public list of reviewers, and you receive feedback from them. People get absolutely nothing back. Do you find this effective ?

And whats the problem accepting more submissions?  Does Ethereum Foundation have issues renting a venue with lots of rooms?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tobi/48/10955_2.png) Tobi:

> in a still very novel branch of computer science.

Computer science is great, of course. I’m talking about the hype—how things are promoted in a completely random order. But what’s the point? What would the Linux community say if Linus Torvalds started doing this with Linux apps? Or telling people to use Ubuntu and not use Fedora?

Or rejecting Fedora submissions to Linux conferences?

Don’t you find it illogical that the Ethereum Foundation, while promoting decentralization, is itself completely centralized and non-transparent? Almost every other project has formal governance and voting mechanisms.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tobi/48/10955_2.png) Tobi:

> So calldata can result in state being written

There’s a separate fee for state storage. What we’re discussing here is the fee for blockspace. These two separate markets create a meaningless situation where the per-byte fee for CALLDATA is infinitely more expensive than the per-byte fee for blobs. Why would anyone build apps on Layer 1 if they’re being artificially discouraged from using it?

---

**Tobi** (2025-04-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kladkogex/48/8349_2.png) kladkogex:

> These two separate markets create a meaningless situation where the per-byte fee for CALLDATA is infinitely more expensive than the per-byte fee for blobs

Right, but you conveniently skipped over the part I wrote after the text you quoted. Can we acknowledge that there’s a good reason for pricing both differently? When we do that we can discuss whether the extend to how these are priced differently is fair. Here I have a less strong opinion. The difference might be too big. Maybe it’s not… I don’t know. I can understand that for the transition to L2s a little nudging the ecosystem into the right direction by strongly encouraging blob usage is seen as a smart strategy. I somewhat agree. But I can also see that we want to keep building on L1 as cheap as possible.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/b2d939/48.png) magicians:

> Let me be blunt Samuel; you, at base are doing a disservice to Ethereum by acting like a bunch of leeches!

Hey [@Samuel.Ranellucci](/u/samuel.ranellucci), I hope that you know that there are lots of crypto/ethereum enthusisasts like me who highly appreciate what you over at (Coin)Base are doing. Thanks for all the great work and bringing the ecosystem forward. Every community from a certain size on will contain people with a certain entitlement for other peoples work - often building nothing themselves - but complaining about how other people building things aren’t doing so to their complete satisfaciton.

---

**kladkogex** (2025-04-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tobi/48/10955_2.png) Tobi:

> Can we acknowledge that there’s a good reason for pricing both differently? When we do that we can discuss whether the extend to how these are priced differently is fair. Here I have a less strong opinion.

I think it is good that the community is at least starting to have open and honest discussions. I totally agree with you that the less time data is stored, the less one needs to be charged for it. Maybe blobs need to be charged 1 gas unit per byte, which would be way lower than call data.

By the way that was the idea Vitalik expressed and promoted originally.  Lower the call data price for blobs. Then there was behind-the-scenes pressure to change it to make things even more advantageous for rollups.  This is how we got to the current state where the price is zero, so L1  economic model is undermined, essentially L1 inflation is sponsoring Base.

Having a separate market for blobs looks, to a reasonable observer, not like something coming from economics but rather from pushing a particular point of view. The Ethereum Foundation needs to think about users as customers. Our project has one of the largest sets of smart contracts on L1. Over the years, we’ve paid hundreds of thousands of dollars to the Ethereum mainnet. We feel that there has to be a mechanism for customers to be heard.

It is no secret to anyone that Vitalik makes the vast majority of strategic decisions in the network. In addition, there is an ineffective notion of a core team where decisions are supposedly made by some kind of consensus. There is the Ethereum Foundation, which is supposed to be a nonprofit, but in reality doesn’t even have a publicly known set of people who steer the foundation.

There is Devcon—no one knows who organizes it, and no one knows who approves or rejects submissions.

All of these things create a false sense of consensus. In reality, conflict always exists. It is healthy to have open conflict and then reach compromise, compared to hiding things under the rug and silently making decisions based on money flowing to one group or another.

Right now, there’s an idea to raise L1 gas fees even higher and drive people to L2. Vitalik has said in the past that he views L1 as just the place where ZK proofs are settled. I can openly say that we do not like this. Maybe we are a 1% minority, maybe our point of view is incorrect, but there is absolutely no way to express this point of view. The same goes for the “transition to L2.” There is no discussion about why it is needed, to what extent, and how it will affect L1.

1. There is no transition to L2. There is a transition to Base. When Vitalik talks about rollups, he ignores the fact that most of them are irrelevant. Base has already won, and they have no intention to decentralize. I love Base and Coinbase, but these are just centralized companies making money—huge amounts of transaction fees, in fact.
2. ZK – I love ZK mathematics, but ultimately users decide what they want, and so far they have clearly decided they do not want ZK as a replacement for blockchain. Technology needs to solve a problem that users actually have. If you have a blockchain with truly 100 decentralized nodes, you get a high level of replication and achieve incredible security without ZK. Deprioritizing the blockchain in favor of rollups and ZK was a suboptimal decision. Users are simply voting no.
3. The current state of the network – There are basically three parties that control the Ethereum mainnet: Coinbase, Binance, and Lido. Liquid staking killed the community. People who buy Lido tokens have no involvement with the network. Then you have essentially Ponzi schemes like restaking, which have no economic foundation but are suddenly promoted as the next big thing. Talking about thousands of ETH nodes makes no sense if they are controlled by the same party—it’s just a giant waste of computational power.
4. Given point 3, why is it so important that everyone in the ETH ecosystem posts all data to the ETH mainnet? Do we really want Binance, Coinbase, and Lido controlling everything? It only creates a fake sense of security, because no one re-executes Base transactions. There are no fraud proofs, and no economic foundation for anyone to build them, since it requires someone to be paid.

To summarize — the absence of governance has created all of these problems. Now, with the token price down, it’s a good time to address this issue. The way to address it is very simple:

1. Vitalik needs to institute at least advisory governance voting, so that even if the system continues to function as a monarchy, it becomes a more modern monarchy.
2. Devcon needs to accept all reasonable submissions and transform into a true community conference. The review board should be openly selected, with no conflicts of interest.
All submissions must receive feedback along with the name of the reviewer. Submission criteria should be clearly published in advance.
3. Same is true for the Ethereum Foundation Grants.
4. “Core team” meetings need to be open so that community can participate and ask questions.

---

**Tobi** (2025-04-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kladkogex/48/8349_2.png) kladkogex:

> Vitalik needs to institute at least advisory governance voting

I woulnd’t want ethereum to be some kind of democracy where every holder/user can vote on the roadmap and on technical decisions. I want it to be a very open ecosystem, where everyone is welcome to start contributing and via that contribution gain respect and influence within the community. Via good arguments and this soft power everyone is welcome to shape the future of ethereum. It’s an informal process. But there’s beauty in this informality.

I know you’re not saying that everyone should vote, but you’re arguing for a formal board of voters (who picks them?). This formal process makes things rigit and carves the power given to certain people or institutions in stone. Again, the informality is chaotic and sometimes hard to grasp… but that doesn’t necessarily make it a bad thing. I think it’s a strength.

If ethereum was the only existing chain in the world and no other chain was allowed and capable of coming into existence, then that would maybe not be acceptable. But this is not the case. All possible directions can be explored at the same time by different projects/chains - that doen’t mean one particular chain must try all directions simultaneusly and cannot have a very particular path it tries to explore. That’s the beauty of free markets and open source technology.

This is also by the way why I like the focus on L2s… It will further enable that process. Progress on composability and more blobs will help us to get to that state where market forces will do the rest. A monolithic Base will not be able to compete with a varyiety of strongly composable competitor chains that are all compatible with another in the long run. I think we’re way too fast in jumping to conclusions when assuming Base has won.

---

**Tobi** (2025-04-21):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/b2d939/48.png) magicians:

> they give nothing back and cause inflation.

Why do you think they cause inflation? Seems to me they’re doing the exact opposite: Reduce the token supply by paying blob fees causing deflation. You probably think these fees aren’t enough but “not enough deflation” doesn’t equate to “inflation”.


*(1 more replies not shown)*
