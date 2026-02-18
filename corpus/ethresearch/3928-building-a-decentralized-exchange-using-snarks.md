---
source: ethresearch
topic_id: 3928
title: Building a decentralized exchange using snarks
author: josojo
date: "2018-10-25"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/building-a-decentralized-exchange-using-snarks/3928
views: 8904
likes: 22
posts_count: 11
---

# Building a decentralized exchange using snarks

Hey,

we, from Gnosis, developed a new specification for a decentralized exchange using on chain scaling with snarks. The exchange is developed as a snark-app (snapp). The scalability is achieved by outsourcing all computations into snarks and using ethereum only as a data availability insurance and execution engine for the snarks. The approach is quite similar to [Roll_up](https://ethresear.ch/t/roll-up-roll-back-snark-side-chain-17000-tps/3675/) project, [plasma snapp](https://ethresear.ch/t/plasma-snapp-fully-verified-plasma-chain/3391/) and especially [onchain scaling](https://ethresear.ch/t/on-chain-scaling-to-potentially-500-tx-sec-through-mass-tx-validation/3477/).

Here is the [specification](https://github.com/gnosis/dex-research/blob/cc9cdb9ebed2d27732aa512bc649ebbffd5fed91/dFusion/dFusionSpec.md)

And here is a high-level [presentation](https://docs.google.com/presentation/d/1RH07nlptBuZQWsZ6h365ZEhN7AGuILyw3GUHc-jE3Bg/edit?usp=sharing):

One remarkable feature of this specification is that it is the first exchange, which scales well and has a decentralized matching engine. With the batch auction approach, anyone has the chance to provide the best prices and thereby determine how orders are matched.

Since we need to deal with huge snarks, up to 2**28~0.26 billion constraints, calculating the snarks will be quite expensive. Our estimate for the costs is roughly 1200$ using AWS and DIZK. In order to cut costs, we are introducing a proposal-challenge game: Snarks are not provided immediately, only the new state of the snapp needs to be provided by a significantly bonded party. Then, anyone can check the proposed state of the snapp and can challenge it, in case it is not correct. Of course, the challenger also needs to bond himself. If a state transition is challenged, then the challenged person needs to deliver the snark proof its correctness.

In the longterm, he hope that we can gain more scalability by merging these snapp approaches with plasma.

We are very interested in your opinion. What do you think about the snapp architecture? Do you see any improvements for the protocol?

## Replies

**sg** (2018-10-25):

I’m glad to see the more complex 2nd layer app from snapp researchers. This area is certainly next bg thing ![:heart_eyes:](https://ethresear.ch/images/emoji/facebook_messenger/heart_eyes.png?v=9)

The important construction for now, is proof computation feasibility, until we get better zkp implementation. And in this case, challenge DoS vector analysis would be prefered to be seen. Maybe challenger also needs bunch of bond?

---

**jannikluhn** (2018-10-26):

Nice work!

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> Our estimate for the costs is roughly 1200$ using AWS and DIZK.

How long does it take to compute it? Can it be parallelized?

---

**josojo** (2018-10-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/sg/48/14420_2.png) sg:

> proof computation feasibility

Yes exactly. This is our focus currently. Mainly we are investigating into DIZK for now. But for sure, we will also look into other technologies.

![](https://ethresear.ch/user_avatar/ethresear.ch/sg/48/14420_2.png) sg:

> Maybe challenger also needs bunch of bond?

Yes, exactly. The challenger also need to be bonded. The bonds should be at least the costs for computing a snark.

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> How long does it take to compute it? Can it be parallelized?

Yes, the DIZK paper has developed a good approach for parallelization. Take a look into it. It’s worth it.

The time depends for sure on many parameters. In the DIZK paper, it is mentioned that they calculate 1 Billion constraint snarks in ~30 mins with a lot of AWS power.

We will post our numbers, once we have them well tested.

---

**bharathrao** (2018-10-30):

Congrats! You guys are definitely one of the most advanced teams in this space.

**Top 3 issues:**

1. any significantly bonded party. I think this needs some elucidation. How big should the challenger bond be? If the bond is too large, many challengers will be priced out and if its too small you risk being spam attacked. There’s also the chance of unintended DDOS. If your network contains 2000 possible challengers and they all submit a challenge, your exchange/network should not be brought to its knees. How big should the prover bond be? If they have to place a smaller bond that what they can steal, but the challenger bond is so large that no one wants to challenge, you will run into a problem. You need to prove that for any combination of on-exchange balance, prover bond, challenger bond, all parties are incentivized to act correctly
2. I seem to have missed the incentive to spend $1200 to solve and submit the solution. Does the submitter get compensated?
3. How is the trusted setup handled? If its integrity cannot be verified, there will the concern that Gnosis team can hypothetically forge any proof.

**Other Issues:**

1. Operators bundle orders and send it on-chain. Can orders be cancelled? How does this work? Does the operator have to resubmit the hashed orders?
2. Function challengeTransitionInformation( bytes32 oldstate, bytes32 newstate)
Can someone challenge a very old state or does the challenge window expire due to checkpointing?
3. Once orders are final, everyone can try to find the best uniform clearing price. What makes an order final?
4. Everyone can check whether the  stateRH  …  can be challenge by providing a bond. Trying to understand the finality of a trade. Is it after the challenge window has passed?

Comments:

1. Ring Trades This may not be worth putting heavy emphasis on. Most of your volume will be from specialists who trade certain pairs. Any internal optimization of liquidity is minor.
2. we allow orders, which might not be covered by any balance of the order sender. Spam attack vector.
3. We do have only 2^6 different tokens in our exchange This may not be as bad as it sounds like. You can replicate the exchange for different token sets in a kind of sharding approach by providing a common base currency to trade against.

---

**josojo** (2018-11-03):

Hey, [@bharathrao](/u/bharathrao)

thanks for taking the time to look through our spec proposal.

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Top 3 issues:
>
>
> any significantly bonded party . I think this needs some elucidation. How big should the challenger bond be? If the bond is too large, many challengers will be priced out and if its too small you risk being spam attacked. There’s also the chance of unintended DDOS. If your network contains 2000 possible challengers and they all submit a challenge, your exchange/network should not be brought to its knees. How big should the prover bond be? If they have to place a smaller bond that what they can steal, but the challenger bond is so large that no one wants to challenge, you will run into a problem. You need to prove that for any combination of on-exchange balance, prover bond, challenger bond, all parties are incentivized to act correctly
> I seem to have missed the incentive to spend $1200 to solve and submit the solution. Does the submitter get compensated?
> How is the trusted setup handled? If its integrity cannot be verified, there will the concern that Gnosis team can hypothetically forge any proof.

1. This is really still subject to research.
2. Yes trading fees. I left these things out, in order to keep the spec short.
3. This is also still research. But probably, we would do it similar to zcash

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Other Issues:
>
>
> Operators bundle orders and send it on-chain . Can orders be cancelled? How does this work? Does the operator have to resubmit the hashed orders?
> Function challengeTransitionInformation( bytes32 oldstate, bytes32 newstate)
> Can someone challenge a very old state or does the challenge window expire due to checkpointing?
> Once orders are final, everyone can try to find the best uniform clearing price . What makes an order final?
> Everyone can check whether the stateRH … can be challenge by providing a bond. Trying to understand the finality of a trade. Is it after the challenge window has passed?

1. We have different models in mind.
2. Yes, we would only allow the challenging of transitions in a certain time frame. Maybe 1 day
3. We will collect orders for some time period. Maybe 3 minutes. After this time, the orders are final
4. After the solution submission phase, the best valid solution is final immediately. I still might be challenged, but anyone could provide the snark to oppose the challenge and keep the state

---

**bharathrao** (2018-11-03):

From a product point of view, batch auctions are perfect for the (rather large) crypto-to-crypto OTC market. The risks of having orders locked in for 3 minutes without knowing if they may be filled is something that affects retail traders but not OTC traders. You could even have trades settle once in a few hours instead of once in 3 minutes, this may reduce cost for the Prover.

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> we would do it similar to zcash

Any chance you could use bulletproofs instead? This would eliminate trusted setup.

---

**khovratovich** (2018-11-14):

For so large a constraint system, you might want to use some more SNARK-friendly hash function than Pedersen hash. For example, one of our inversion-based designs (DevCon4).

---

**josojo** (2018-11-15):

[@khovratovich](/u/khovratovich)

Yes, we are definitively looking into this.  We also watched your talk at devcon ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=9)

Better hash functions would help sooo much!

---

**HarryR** (2018-11-15):

While the whitepaper hasn’t been released (yet?) I have been trying to specify Jarvis and Friday with the details available, and I’m already using the Miyaguchi–Preneel one-way construct in combination with MiMC, but using an inversion reduces the number of constraints *significantly*

I put together the details I have at: https://github.com/HarryR/ethsnarks/issues/73

Do you have any additional references or material?

---

**fraserbrownirl** (2019-03-29):

Is there a video accompanying the Web3 dFusion slides? I’ve a few questions

