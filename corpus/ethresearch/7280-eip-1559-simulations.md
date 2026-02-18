---
source: ethresearch
topic_id: 7280
title: EIP 1559 simulations
author: barnabe
date: "2020-04-15"
category: Economics
tags: [fee-market, eip-1559]
url: https://ethresear.ch/t/eip-1559-simulations/7280
views: 8610
likes: 23
posts_count: 8
---

# EIP 1559 simulations

Hi all!

I wrote a notebook introducing simple simulations of EIP 1559, the anticipated fee market proposal by [@vbuterin](/u/vbuterin), [@econoar](/u/econoar) and now many others. The notebook is [here](https://github.com/ethereum/rig/blob/9de2ecbba130fba13011eca2b229979b0adcba52/eip1559/eip1559.ipynb).

EIP 1559 was discussed quite a lot on other forums (see links section below). I wouldn’t want to add to the noise and start yet another thread, so I will focus this post on the approach of the notebook above, the next steps and some literature I am looking at. The notebook also prompted discussion on Twitter that would fit better here it seems.

## The notebook

The simulations assume some demand comes in between two blocks, is either included in the block or not, sometimes stays in the mempool and sometimes not. I increasingly add complexity to the simulation but stop short of having “smart users” who act based on the current market or “smart producers” who strategically try to improve their payoffs.

## Next steps

1. Real demand is not that simple. Users look at the current market conditions before deciding how to set their fees, so we need to model this behaviour (there was an interesting post a few years ago by Vitalik). If clients set the parameters for them, this is also something we want to model. Looking at historical prices may help identify the processes at play. We want to be able to express time-preferences.
2. Block producers may (will?) have more sophisticated behaviour than just include anything. More importantly, we need to make sure the mechanism is incentive-compatible (producers behave honestly, in a timely fashion). Formal analysis is probably more helpful here than simulations.
3. Integrating the simulation with Hive (suggested by @AFDudley). More generally, there is work to do on matching real conditions (down to the client implementation) with the simulations. There was chatter about an EIP 1559 testnet too over at the EthR&D Discord.
4. Mechanism tuning. EIP 1559 is “simple” (though I would argue, not that simple either) in that it looks like a fairly standard control mechanism: number go up, resistance go up; number go down, resistance go down. Variants exist, e.g., the escalator algorithm (suggested by @danfinlay).
5. I still have many unknowns and blind sides. The notebook was my attempt to build some intuition for myself and others, but many of the hard questions remain ahead. I’ll be looking into the modelling a bit deeper over the next weeks too.

## Some links

- Blockchain resource pricing, by Vitalik
- EIP 1559 proposal
- Ethereum Magicians thread
- Formation of a working group and amendment
- The escalator algorithm + EIP

## Replies

**danfinlay** (2020-04-16):

This analysis is very interesting, I’m still making my way through it, but I’d like to comment on one observation that occurred to me:

The current analysis uses the `fee_cap` parameter to represent both the highest price a person is willing to pay, *and* their sense of urgency, what I might suggest is a missing parameter: `time_preference`.

To illustrate why this is an valid distinction to consider, we need examples of exceptions to these two parameters being correlated. Here are two, on different ends of the spectrum:

- A user who has a high-priced auction reveal coming up is willing to pay a high price as the block approaches the reveal time.
- When blocks are not full, and transactions are cheap, there may be small opportunities of arbitrage available. These would be situations where the max_price is very low, but the time_preference for those transactions is urgent.

Even without having good estimates of the frequency, we can still ask questions like:

Does a user with `fee_cap=X` and `time_preference=Y` achieve a satisfactory outcome given the block conditions and gas payment algorithm?

That’s one of the types of questions I tried considering in [the Escalator algorithm EIP](https://github.com/ethereum/EIPs/pull/2593). I’m not sure how much it would benefit from numeric quantification, since we would be guessing the frequency of many scenarios, but I would like to highlight these considerations.

Anyways, thanks again for such an interesting analysis. It’s been very fun to read this, I hope more protocol proposals get cadCad analyses like these.

---

**barnabe** (2020-04-21):

Thanks Dan!

![](https://ethresear.ch/user_avatar/ethresear.ch/danfinlay/48/1084_2.png) danfinlay:

> A user who has a high-priced auction reveal coming up is willing to pay a high price as the block approaches the reveal time.
> When blocks are not full, and transactions are cheap, there may be small opportunities of arbitrage available. These would be situations where the max_price is very low, but the time_preference for those transactions is urgent.

I really like all the cases you have isolated, here but also in your EIP. This is very helpful. I agree that getting a sense of what normal conditions are, or what is the “usual” mix of transactions would be sensible. I am hoping to collect data on this and try that analysis.

![](https://ethresear.ch/user_avatar/ethresear.ch/danfinlay/48/1084_2.png) danfinlay:

> Does a user with fee_cap=X and time_preference=Y achieve a satisfactory outcome given the block conditions and gas payment algorithm?
>
>
> That’s one of the types of questions I tried considering in the Escalator algorithm EIP. I’m not sure how much it would benefit from numeric quantification, since we would be guessing the frequency of many scenarios, but I would like to highlight these considerations.

I’d like to be clearer what the transaction parameters are in the escalator. As I understand it currently, there is some price level `p`. For now say I only set two parameters, `feecap` and `time_preference`.

- I submit my transaction at t=0, with fee p and a hash of the block at t.
- If it is not included, at t=1, my transaction fee increases by (feecap - p) * t / time_preference. Meaning, if I really want to be included at least 1 block from now, I set time_preference to 1 and my bid jumps to my fee_cap in the next slot.

Is there a need for something like the `initial_bid` of the Agoric papers? In your own [ethresear.ch thread](https://ethresear.ch/t/another-simple-gas-fee-model-the-escalator-algorithm-from-the-agoric-papers/6399) you let users decide on the `initial_bid`. Using some kind of ambient price `p` (sort of like the `basefee`) this is one less parameter to specify (if we expect users to specify both `feecap` and `time_preference`). Of course it opens more question on how the dynamics of `p` affect the algorithm.

---

Segueing to a more formal model that could help compare the alternatives on hand. The presentation is more EIP 1559-specific but the representation of users and producers, metrics like social welfare etc. can be taken as is for a different mechanism – the only thing that changes would be strategies of users and producers.

In the last section I also give a result to show that under certain conditions, producer behaviour can be individually rational but not socially optimal. This is not unexpected however, these are the kind of things that were discussed on other threads. I haven’t necessarily seen it written up though.

#### EIP 1559 System dynamics

Given

- b(0): the basefee at t=0,
- c: a target gas per block,
- G: the max gas limit per block, and
- d: the basefee max change denominator d,

we observe two dynamical processes:

- b(t) is the basefee at time t \in \mathbb{N}.
- g(t) is the total gas used by the block at time t, g(t) \in [0, G].

This yields the following state dynamics:

b(t+1) = b(t) + b(t) \frac{g(t) - c}{cd} = b(t) \Big(1 + \frac{g(t) - c}{cd} \Big)

#### Users

- Probably WLOG, we can assume that one user = one transaction[^1]. k runs over a countable (possibly infinite) set of users K, t denotes time steps, which we can assume discrete since “events” happen one block at a time. For some k, v_k: t \mapsto v_k(t) is the value function of the user, mapping time indices to the value. For all k, there exists t_k such that v_k(t) = 0, \, \forall t  0 and v_k(t_k + 1) = 0.
- User k places their transaction a_k in the mempool at time t_k (i.e., earliest possible inclusion is in block at height t_k) and sets the transaction premium (\texttt{premium}(a_k)) and fee cap (\texttt{feecap}(a_k)).
- Users observe the basefee b(t) at time t-1, i.e., know about b(t_k) once the block at height t_k - 1 is produced. The basefee is Markovian, i.e., only depends on its value at the previous block height. This makes it easier to reason about strategies for users and producers alike, as either can simply base their strategies on the value of b(t) alone (producers need to consider also the set of transactions in the mempool at t). The strategy space of user k is thus the set of mappings from the basefee and their utility function to their transaction attributes,

S_k = \Big\{ (v_k, b(t_k)) \mapsto (\texttt{premium}(a_k), \texttt{feecap}(a_k) \Big\}

- Given some basefee b(t) at time t, the fee paid by user k whose transaction is included at time t is

\texttt{fee}(a_k, t) = \texttt{gasused}(a_k) \times \texttt{gasprice}(a_k, t)

where

\texttt{gasprice}(a_k, t) = \min(\texttt{feecap}(a_k), b(t) + \texttt{premium}(a_k))

- Let i : K \times \mathbb{N} \to \{ 0, 1 \} be the inclusion function, with i(k, t) equal to 1 if and only if the transaction of user k was included at time t. Note that i(k, t) = 1 \Rightarrow b(t) \leq \texttt{feecap}(a_k).
- The payoff function of user k is

\sum_{t \in \mathbb{N}} i(k, t) (v_k(t) - \texttt{fee}(a_k, t))

#### Producers

- We have N block producers, commanding respectively fraction \alpha_n of the mining/staking power. The probability producer n is selected to create a block is \alpha_n.
- Producers learn whether they will produce the block at height t right after the block at height t-1 is produced. The producer at time t selects from the mempool at time t a set of transactions respecting the block limit. We can get the state of the mempool at time t with:

M(t) = \{ a_k, k \in K: t_k \leq t; \; \forall s < t, \, i(k, s) = 0 \}

i.e., transactions from users who are awake and who weren’t previously included. Given M(t) and b(t), the producer for time t chooses a set of transactions A(t) \subseteq M(t) to include in their block.

- The producer function is p : N \times \mathbb{N}  \to \{ 0, 1 \}, with p(n, t) equal to 1 if and only if producer n produced the block at time t in the canonical version of the chain. The long-term payoff of block producer n is given by:

\sum_{t \in \mathbb{N}} (1-\delta)^t p(n, t) \Big( \sum_{k \in K} i(k, t) \cdot \texttt{gasused}(a_k) \times (\texttt{gasprice}(a_k) - b(t)) \Big)

with \delta giving a discount rate for payoff now vs. payoff later. We can assume

\frac{1}{T} \sum_{t = 1}^T p(n, t) \rightarrow_{T \to \infty} \alpha_n

#### Social welfare

- The fee is paid from the user to the producer and is thus a simple transfer. The social welfare of the system is obtained by

SW(v, \alpha, b(0)) = \sum_{t \in \mathbb{N}} \sum_{k \in K} i(k,t) (v_k(t) - \texttt{gasused}(a_k) \cdot b(t))

All else being equal, the social welfare is optimised whenever transactions get in as early as possible and when basefee is lower.

The concern that producers can “manipulate” the fee has been expressed a few times, so we now give a simple example, showing that if a producer is chosen to produce two successive blocks, they can artificially delay inclusion to maximise their payoff. This is a prototype deviation, clearly a bit contrived.

#### A single producer

We have two time steps, 0 and 1. Let’s normalise the gas target to 1. The basefee is set at b for the first block and moves to b' for the second block. Transactions W(0) awaken at time t=0, with \mu(W(0)) = \sum_{a \in W(0)} \texttt{gasused}(a). Assume

- All transactions are identical (this is a strong assumption, but the example works as long as there is money on the table).
- \mu  f - b (the producer cannot get the whole premium at time step 0, since it is larger than the difference between the feecap and the basefee).
- A single producer creates the blocks at time t=0 and t=1. For PoW chains, you could try to selfish mine, leaving the first block empty and stuffing the second one to reap higher fees. In eth2, at the start of a new epoch, validators can look up the slots in that epoch where they will be proposers.
- Producer discount rate is \delta = 0 (also WLOG).

The payoff of the block producer who includes all transactions from W(0) at time step 0 is \mu \cdot (f - b).

If the producer does not include anything, the basefee drops to b' = b - \frac{1}{d}b = \frac{d-1}{d}b. Assume that b' + \epsilon < f, i.e., the basefee has dropped enough that the producer would get the whole premium instead of the difference between the feecap and the basefee. Including the transactions at time step 1 now yields payoff \mu \cdot \epsilon > \mu \cdot (f - b). In other words, it is more profitable for the producer to wait out another step. This is individually rational, but not socially optimal.

This holds true as long as the opportunity cost of not including transactions at t = 0 is lower than the profit from delaying them, and decreasing the basefee.

---

![](https://ethresear.ch/user_avatar/ethresear.ch/danfinlay/48/1084_2.png) danfinlay:

> Anyways, thanks again for such an interesting analysis. It’s been very fun to read this, I hope more protocol proposals get cadCad analyses like these.

There is a [cadCAD notebook](https://github.com/ethereum/rig/blob/b7eab114509eac9c8219cd1bb195dcfbeae6e76a/eth2economics/code/beaconrunner/beacon_runner.ipynb) on eth2 specs!

---

**tkstanczak** (2020-05-28):

Hi guys,

I have spent some time analyzing various sources about EIP-1559. This may help you with defining the simulations. Give me a shout if Nethermind team can help in any other way.

Best,

Tomasz

[EIP1559-Nethermind.pdf](/uploads/short-url/jxCghxljHrvP6cWDwji7JQHYRRr.pdf) (1.8 MB)

---

**barnabe** (2020-05-29):

It’s amazing, I was looking at the PDF after the call yesterday. Your experience on the client-side is invaluable! For instance, transaction pool dynamics seem to matter more than I anticipated (it was also pointed out by [@veox](/u/veox) [in an issue in our repo](https://github.com/ethereum/rig/issues/4)).

I cannot click on the links though, specifically I was curious to check out “Measuring Eth1 network metrics” if it is public, I couldn’t find it.

---

**tkstanczak** (2020-05-29):

[Discord Channel](https://discord.com/channels/595666850260713488/692078615269212180)

[RIG team analysis](https://github.com/ethereum/rig/blob/069087787a683654dc263529ada2d2c83646e574/eip1559/eip1559.ipynb)

[Measuring Eth1 network metrics](https://docs.google.com/document/d/1eFdWN9g2wMycEZF-YNvMFE2yS5_IuFP5eRNB17Dw4NE/edit#heading=h.85qzouiqi92e)

[EIP-1559 Implementers Call #1](https://notes.ethereum.org/@afhGjrKfTKmksTOtqhB9RQ/HJlq2GYFU)

[Moloch DAO statement of work - economics](https://docs.google.com/document/d/1JDaElsMEJlmi4uc7axZ7JAw3EjkYczdP6PAsuEZz4rk/edit#heading=h.o8btuiu1a5g)

[EthResearch Escalator and EIP-1559 discussion](https://ethresear.ch/t/another-simple-gas-fee-model-the-escalator-algorithm-from-the-agoric-papers/6399/36)

[Vulcanize Implementation in Geth](https://docs.google.com/document/d/1yqvvfrQ_He0fN1SsUcvZNBdyhv__d8-1QPyteCbNT6Q/edit)

[EIP-1559 Draft](https://github.com/ethereum/EIPs/blob/4cc3816b9567090b2b4118392631ef8546103723/EIPS/eip-1559.md)

[EIP-1559 Update](https://eipupdate.substack.com/p/eip-update-issue-1-eip-1559)

[EIP-1559 PR](https://github.com/ethereum/EIPs/pull/2505/files)

[Ethereum Magicians discussion](https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783)

[Resource Pricing](https://ethresear.ch/t/draft-position-paper-on-resource-pricing/2838/16)

[First and Second Price Auctions](https://ethresear.ch/t/first-and-second-price-auctions-and-improved-transaction-fee-markets/2410)

---

**tkstanczak** (2020-08-17):

Please let me know where is the fault in my thinking:

- if a minority miner (20% of the network) decides to always fill the blocks with useless transactions to the level of Maximum gas limit (2 * TARGET_BLOCKGASLIMIT) then the only strategy preventing this from entirely disrupting the network forever would be to mine empty blocks in response which is counterproductive because it serves the attacking miner too. The attacking miner still collects the block rewards and is only affected by the fee burning cost but they will always fill as much as they can with legit transactions so part of the attack cost is covered.

Would it not render the entire EIP-1559 design incorrect?

In the past we kept discussing miners trying to decrease the BASEFEE but we did not discuss the idea of a malicious miner trying to make the network useless?

---

**barnabe** (2020-08-19):

The attacking miner would need to spend an increasing amount in basefee block after block, while filling blocks to capacity would entail an exponential increase of basefee. The attack is very costly to sustain for long periods of time. [@timbeiko](/u/timbeiko) posted one of his slides [here (Eth R&D discord)](https://discordapp.com/channels/595666850260713488/692078615269212180/745113045344321597) giving back-of-the-envelope estimations: after a few blocks the cost of the attack is already higher than the block reward itself.

