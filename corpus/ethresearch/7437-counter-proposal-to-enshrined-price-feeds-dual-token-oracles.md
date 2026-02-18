---
source: ethresearch
topic_id: 7437
title: "Counter-proposal to enshrined price feeds: dual-token oracles"
author: vbuterin
date: "2020-05-16"
category: Economics
tags: []
url: https://ethresear.ch/t/counter-proposal-to-enshrined-price-feeds-dual-token-oracles/7437
views: 6099
likes: 4
posts_count: 13
---

# Counter-proposal to enshrined price feeds: dual-token oracles

The following is a largely application-layer counter-proposal to [Enshrined Eth2 price feeds](https://ethresear.ch/t/enshrined-eth2-price-feeds/7391), though there are some protocol-layer features (eg. larger graffiti, in-VM accessibility of the validator set) that could help make it easier to implement.

A lot of existing and proposed oracles (Augur, Kleros, UMA) work in roughly the same way:

- [Initial reporting] Suppose a result on some event E needs to be reported. First, anyone (or at least one of many actors) can make a report R by putting down a deposit. The deposit is only returned if the oracle ends up returning R.
- If the report is unchallenged, the oracle returns R.
- [Escalation] One of many actors can challenge the report, and there is some escalating challenge process where the deposits required to challenge challenges keep increasing. If there are enough challenges with high enough deposits, the system starts a global coin vote.
- [Global coin vote] In a global coin vote, everyone who holds some coin can vote on the report. The oracle reports the winning result, and everyone who agreed with the winning result sees their coin balance greatly increase and everyone who disagreed sees their balance greatly decrease.
- [Market backstop] In the event of a 51% attack on the system, anyone can fork the system and create a “parallel universe” where the minority report won and the minority coinholders see their balances greatly increase and the majority coinholders see their balances greatly decrease. If the minority answer was actually correct, the theory is that the market will value the forked system more highly because its coinholders have a track record of honesty even under high risk, and the original system will be less important than the fork.

There are two ways to measure security of such oracles:

- Budget: how much money do you need to attack the system?
- Cost: how much does attacking the system cost you?

These oracles have a budget requirement *and* cost of attack roughly equal to the market cap of the oracle token (eg. REP, MKR, PNK). The unincentivized coin vote oracle proposed in the [enshrined feed proposal](https://ethresear.ch/t/enshrined-eth2-price-feeds/7391) has a higher budget requirement, because ETH has a higher value than tokens, but zero cost because there is no penalty to voting incorrectly.

**The goal of this proposal is to combine these two systems, creating a system with a budget requirement consisting of a substantial portion of all staked ETH *plus* an oracle token, and a cost of attack based on the oracle token.**

### The proposal

An oracle where to participate in the global coinvote, you need to have *both* 32 ETH worth of oracle tokens *and* an active validator slot. That is, one unit of participation requires both signing a message with a key that controls oracle tokens and signing a message with a key that is connected to a validator slot.

### How to verify?

There are a few goals here:

- Prevent validators from easily selling off their oracle participation rights as a separate token (as that would break the security of the scheme)
- Avoid adding centralization/pooling pressure to validating itself
- Avoid imposing excessive risk on validators

One option is to require signing a message with the signing key of a validator (this could even be done by checking the graffiti of the last beacon or shard block that they created). This goes pretty far in preventing selling participation rights, because giving someone else your signing key lets them (profitably) slash you. However, it does increase the complexity of validation itself.

A second option is to have some kind of signature scheme where instead of the key *being* the signing key, the key is a pair of signatures of conflicting block headers (so the key could be used to slash, but not to commit any other mischief to the chain). This would not increase people’s willingness to delegate participation rights, but in the event that people do so anyway, it would decrease risks, as they would only be giving out a self-slashing key, not a key that could be used to attack the blockchain.

## Replies

**JustinDrake** (2020-05-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> protocol-layer features (eg. larger graffiti, in-VM accessibility of the validator set) that could help make it easier to implement

+1 for these two specific protocol-layer features. In-VM accessibility of the validator set should be easy by exposing `state.historical_roots` via an opcode. Another interesting feature to think about is “application-layer slashing” where a validator can specify logic (e.g. via a piece of code, similar to account abstraction) to opt-in to being slashed under specific circumstances.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> staked ETH plus an oracle token

I’d say the following heuristics apply for (X, Y)=(pure ETH, an application-specific token) in a similar way that they apply for (X, Y)=(pure cryptography, cryptoeconomics).

- If you can’t make X work, try Y.
- If you can make X work, avoid Y.
- With sufficient cleverness and effort X will usually work.
- When X fundamentally does not work, Y will be a huge success.

Application-specific tokens can be convenient stopgaps. Are they fundamentally required and desired longer term for oracles specifically (and most dApps in general)?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Budget : how much money do you need to attack the system?
> Cost : how much does attacking the system cost you?

Agreed that we want both high budget and high cost for attackers ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) I think our two proposals explore different points in a 2D budget-cost grid:

**Enshrined oracles**—Attacking the system is high budget and low/medium expected cost. You need a huge budget to overcome honest and lazy validators. On the other hand the “social backstop” (social shaming, slashing, orphaning) is harder to execute and not guaranteed to kick in, so the expected cost is relatively low.

**Dual-token oracles**—Attacking the system is low/medium budget and high expected cost. You need a relatively small budget to corrupt the set of validators (say, 10% of validators) that opted in to participate in the oracle token scheme. On the other hand the “enshrined punishments” make the expected cost high.

Open problem: Design a scheme where both the budget and expected cost are high. Bonus points for a pure ETH solution ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**vbuterin** (2020-05-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Application-specific tokens can be convenient stopgaps. Are they fundamentally required and desired longer term for oracles specifically (and most dApps in general)?

I think fundamentally yes (for oracles, not for most dapps), precisely because tokens are the only robust way to provide incentives for correct reporting.

---

**JustinDrake** (2020-05-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> tokens are the only robust way to provide incentives for correct reporting

Why? All we need are ETH-only penalty and reward mechanisms. Below are two such mechanisms. (Note that I’m not necessarily advocating for these. I’m merely pointing out that they exist for the sake of argument.)

**penalties**—As mentioned above, consider “application-layer slashing” where a validator can specify logic (e.g. via a piece of code, similar to account abstraction) to opt in to being slashed under specific circumstances. Such slashing could be part of the registration process for a validator to become an oracle voter. The slashing would get triggered, for example, by some global coin vote mechanism in case of bad behaviour.

**rewards**—Consider a design which allows participating validators to manipulate the oracle prices by ±1% in a plausibly deniable way. (Implementation details are not super important, but imagine something like quadratic voting which bypasses a linearly weighted median to apply the ±1% bias. Fancy cryptography would provide full privacy to prevent reverse-engineering the bias.) Such oracle manipulation on the margin would not be a systemic risk for dApps like fully decentralised stablecoins, yet would provide validator extractable value (VEV).

And voilà, you have an ETH-only incentivisation mechanism. The heuristic “With sufficient cleverness and effort X will usually work.” has proven surprisingly true for X=“pure cryptography”. My gut feel is that it’s also true for X=“pure ETH” ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**vbuterin** (2020-05-16):

1. The problem is that you need to have incentives that are directly tied to whether or not some report about a price was correct, ie. whether or not some real fact about the world is true.
2. The ethereum base system does not know about such things.
3. I claim we don’t want to make its exceptional-case governance worry about such things, as that imposes political risk on the platform.
4. Hence, you need a system other than ethereum with value to impose such incentives.
5. This entails a token other than ETH.

What step in the reasoning do you disagree with?

---

**JustinDrake** (2020-05-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The ethereum base system does not know about such things.

I claim that this is not necessary. More specifically, it is sufficient for L2 to know about such things. Consider the following system:

- registration—Validators are invited to become “oracle voters” by placing 1 ETH of collateral attached to their validator pubkey into a smart contract. The smart contract, which has access to historical_roots, will only release the 1 ETH when the validator’s status is withdrawable. Moreover, it will slash the 1 ETH collateral if a global vote deems that the validator misbehaved.
- global vote—This is your suggestion. After an escalation process a global vote is triggered among the oracle voters (1 oracle voter = 1 vote). This is how the Ethereum chain “knows about such things” as the price of ETH.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The ethereum base system does not know about such things.

I now claim this statement is false if we assume the “application-layer slashing” protocol-layer feature.

Application-layer slashing allows a validator to specify logic (e.g. via a piece of code, similar to account abstraction) to opt in to being slashed (i.e. having the function [slash_validator](https://github.com/ethereum/eth2.0-specs/blob/73031537bc5b470e576385e3d417fa69ee2ee4aa/specs/phase0/beacon-chain.md#slash_validator) called on itself) under programmatically-defined circumstances. This has several consequences:

- base system awareness—The base system (by which I assume you mean Ethereum L1) can be aware of the result of global votes through application-layer slashing.
- capital efficiency—The above design can be redesigned to avoid the extra 1 ETH collateral above. Instead, the oracle incentivisation system reuses the native state.balances of validators without the external 1 ETH, leading to a more capital-efficient system.

---

**alonmuroch** (2020-05-17):

Is there any particular importance to have oracles an an in-protocol feature? and if so, is that the most important in-protocol add-on to have?

---

**JustinDrake** (2020-05-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/alonmuroch/48/4817_2.png) alonmuroch:

> Is there any particular importance to have oracles an an in-protocol feature?

The goal is to have fully decentralised oracles, ideally as L2 infrastructure. Such oracles can be used for all sorts of DeFi applications. As a concrete example consider tBTC which launched two days ago. They are using the ETH/BTC oracle from Maker. This is not ideal:

1. tBTC had to get permission from Maker. This goes against permissionlessness.
2. tBTC has to trust the Maker governance to keep tBTC in the oracle whitelist. This goes against trustlessness and dependency minimisation.
3. The Maker oracle is a federation of 17 opaque sources. This goes against full decentralisation and transparency.

There are a few important primitives that are hard for a deterministic VM to provide out of the box. These include time, randomness, price. It can take significant sophistication to address these properly (e.g. use VDFs to do unbiasable randomness). We haven’t fully cracked price yet, i.e. we are still looking for a robust mechanism for Ethereum to be aware of its own price in a fully decentralised way.

---

**vbuterin** (2020-05-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Moreover, it will slash the 1 ETH collateral if a global vote deems that the validator misbehaved.
> global vote —This is your suggestion. After an escalation process a global vote is triggered among the oracle voters (1 oracle voter = 1 vote). This is how the Ethereum chain “knows about such things” as the price of ETH.

Right, so this is not robust against 51% attacks. If there’s a 51% attack against the system, then it’s cost-free for the attackers, and furthermore, it’s costly for everyone who doesn’t join the attackers. This is quite a dangerous equilibrium, and potentially could even incentivize the centralization of staking at the base layer (do *you* want to be sure you won’t get slashed for disagreeing? Then join the binance pool that already has 37% of all ETH in the oracle and has a direct phone line to the bitfinex pool that has another 15%!) The lack of “[subjectivocracy](https://blog.ethereum.org/2015/02/14/subjectivity-exploitability-tradeoff/)” backstop makes this issue unavoidable.

---

**alonmuroch** (2020-05-18):

But both of the proposals would add protocol specific features for that? That is adding more responsibilities for the validators on L1? (using graffiti or an dedicated metadata storage)

---

**JustinDrake** (2020-05-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The lack of “subjectivocracy ” backstop makes this issue unavoidable.

The section titled “rational operators” of the enshrined Eth2 price feeds proposal is all about subjective backstops, including what I called “social slashing” to combat 51% attacks. Are you claiming that ETH-based schemes have no subjective backstops to combat 51% attacks?

- Definition—Surely yes-The-DAO-fork (Ethereum) vs no-The-DAO-fork (Ethereum Classic) satisfies your own definition of subjectivocracy:

> Pure subjectivocracy is defined quite simply:
>
>
> If everyone agrees, go with the unanimous decision.
> If there is a disagreement, say between decision A and decision B, split the blockchain/DAO into two forks, where one fork implements decision A and the other implements decision B.
>
>
> All forks are allowed to exist; it’s left up to the surrounding community to decide which forks they care about.

- Historical examples—Can you point to historical examples of non-ETH L2 subjectivocracy? As far as I can tell the prime example of subjectivocracy is ETH-based, and I’m not aware of non-ETH-based historical examples.
- Practicality—How would non-ETH-based L2 subjectivocracy work in practice for fully decentralised dApps, say tBTC? Imagine tBTC uses a L2 price feed coming from some contract C. A 51% attack on C is performed and the community subjectively forks to contract C’. Now what? How does tBTC, which is fully decentralised, benefit from C’? L1 subjectivocracy can perform surgery to change the definition of contract C whereas L2 subjectivocracy seems fundamentally limited to address this “pointer remapping” issue.

---

**0xNimrod** (2024-04-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> There are two ways to measure security of such oracles:
>
>
> Budget: how much money do you need to attack the system?
> Cost: how much does attacking the system cost you?

Can I find some deep analysis about “budget”? I wonder why it’s so unused in crypto-economic discussions? Maybe we need some additional parameters that emphasize the complexity to gain the amount of power that could manipulate the system - this has to do with capital and the number of diverse players in the system.

---

**themandalore** (2024-05-03):

Some people have talked about it (see UMA or even new EIGEN paper on cost of corruption or cost of attack).  The basic issue though is that in forkable systems, it doesn’t mean much.  Additionally the bigger issue with any of these analysis is that “Cost” is basically unobservable.  If you have ETH in a smart contract to attack, the problem is a) will they fork to save it? b) Will I be detectable on the exit / will I be able to exit? c) What if you’re a competitor who gains by this project failing…what do I get from an attack now?  d). What do I lose if I fail at the attack? e) can I hedge my failing attack with a derivative?  Can I multiply my earning of a successful attack with a derivative (e.g. a 100x contract on bitmex)?  e) Can I socially attack it with no capital…(e.g. say there’s a bug in the oracle contract and get stake to exit)

The simple model of budget < cost are rarely measurable and practically useless for actually security discussions unfortunately

