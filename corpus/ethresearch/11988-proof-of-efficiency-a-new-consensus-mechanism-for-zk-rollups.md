---
source: ethresearch
topic_id: 11988
title: "Proof of Efficiency: A new consensus mechanism for zk-rollups"
author: davidsrz
date: "2022-02-10"
category: Layer 2
tags: [zk-roll-up]
url: https://ethresear.ch/t/proof-of-efficiency-a-new-consensus-mechanism-for-zk-rollups/11988
views: 21304
likes: 23
posts_count: 12
---

# Proof of Efficiency: A new consensus mechanism for zk-rollups

# Proof of Efficiency

David Schwartz and Jordi Baylina, Polygon Hermez

## A new consensus mechanism for zk-rollups

We at Polygon Hermez are currently working on the zkEVM implementation, and this challenge has required us to research and develop a new consensus mechanism for a decentralized L2 protocol.

It leverages the experience of the existing Proof-of-Donation in v1.0, designed to build the first decentralized zk-rollup and support the permissionless participation of multiple coordinators in order to produce batches in L2.

We are still considering several options and improving this protocol for v2.0 (zkEVM), but we are happy to share our ideas with the community and receive feedback.

## Background

In zk-rollups, the challenge of decentralizing is huge and it has been difficult to find a good solution so far. This happens because protocols such as PoS have some [issues](https://ethresear.ch/t/against-proof-of-stake-for-zk-op-rollup-leader-election/7698) on L2 and there’s a need to get production of zk validity proofs (which are very computation intensive for the prover) with high performance so the network can keep its service level. Assigning the right to produce a batch (L2 block) to any random validator does not guarantee that.

Proof of donation/Proof of Burn (PoD/PoB) is based on a decentralized auction model to get the right to produce batches in a specific timeframe. In this case, the economic incentives are set up so the validators need to be very efficient in order to be competitive, and it represents a big improvement.

One problem with this model is that for a specific time, the network is controlled by a single actor which could potentially be malicious and even if there are ways to mitigate the impact, it’s difficult to avoid zero impact on the service level, especially on the bootstrapping phases.

On the other hand, the auction protocol is very costly and complex for coordinators/ validators, while at the same time only the most effective will be rewarded. It’s difficult to automate for them and the complexity of the predictions is high, since the auction requires bidding some time in advance.

Another problem with the previous protocol is the effectiveness for selecting “the best” operator that converges to a “winner takes it all” model. This doesn’t allow operators with slightly less performance to compete. The consequence is that operators in control of the network became very centralized with the censorship resistance limitations that this situation produces.

## New requirements

The new protocol aims to cover the key properties that such a consensus model for a L2 zk-rollup requires:

- Permissionless access to produce L2 batches
- Efficiency as key to network performance
- Avoid control from any single party
- Protection from malicious attacks
- Total validation effort proportional to the value in the network

## Proof-of-Efficiency (PoE) model

The protocol of creation of batches consists of a two-step model that splits activities between different parties. The first party to participate is the Sequencer and the second one is the Aggregator.

### Sequencers

In this model, the sequencers are parties that collect L2 transactions from users and so they select and  pre-process a new L2 batch in the network by sending a L1 TX with the data of all selected L2 TXs. Anyone can be a sequencer, it’s a permissionless role consisting of a gateway to the network.

The interesting thing is that these proposed batches will be recorded in a L1 transaction for a zk-rollup model (or in a different data availability network in the case of a Validium).

This batch proposal happens when the sequencers decide to do so based on the incentives they have:

- one potential being the economic value of transactions in their pools.
- or the service level that they need to fulfill with their users (fees could vary accordingly since they will be requested by the sequencer).

[![PoE1](https://ethresear.ch/uploads/default/original/2X/1/1b54ce784c821f34b8d5d7218850095a84c9e054.png)PoE1602×359 15.3 KB](https://ethresear.ch/uploads/default/1b54ce784c821f34b8d5d7218850095a84c9e054)

To propose a new batch to the network, sequencers will need to pay the gas fees of L1 network to produce a TX with all the batch transactions data, and the protocol defines an additional fee in $MATIC token that will need to be deposited. This way, there is an incentive for sequencers to propose valid batches with valid transactions.

The batch fee will be variable depending on the network load, this will be calculated from a parameter called , automated from the protocol smart contract.

The batches, in the format of L1 transactions with information in the CALLDATA, will be used as the data availability for the L2 network and any new permissionless node will be able to synchronize the state, reconstructed also from this information.

Once mined, these data availability L1 transactions define the L2 TXs that will be executed and the specific order. This creates a deterministic new state, which can be computed as a virtual future state by network nodes.

Of course, this new state will be settled when the validity proof of a new state (the ZKP) is generated and mined in L1. This corresponds to the second part of the protocol.

### Aggregators

Of course one of the main advantages of the zk-rollups is the fast finality of transactions that validity proofs provide. This protocol tries to enhance the effectiveness of these proofs.

The aggregators are the parties that participate in a permissionless way in the consensus protocol of Proof-of-Efficiency.

In this mechanism, the right to create the validity proof of a new state of the L2 (and of course, collect part of the fees in the txs) is earned simply by being the first aggregator to do it.

It works in the following way: the batches proposed by the Sequencers in L1 are sorted by their appearing position in the L1 and contain the transaction data. The PoE smart contract will accept as valid the first validity proof that updates to a new valid state including one or more of the proposed batches.

[![PoE-Agg1.drawio](https://ethresear.ch/uploads/default/original/2X/6/6066873078dcd11f9ef93601eba9237c52cbf11a.png)PoE-Agg1.drawio536×321 13.9 KB](https://ethresear.ch/uploads/default/6066873078dcd11f9ef93601eba9237c52cbf11a)

The aggregators need to define their objectives to trigger proof generation and run the race based on their own strategy.

For example, if there are batches with few TXs included, some aggregators may find it not interesting to produce a proof until there is more value and produce a proof that includes the change of state of N proposed batches. Other aggregators may have a different strategy.

For the aggregators that are late to the race, the smart contract will execute with a Revert if the proof sent is not proposing a new state, checked with the merkle tree hash of the overall state database. So, not being the first comes at the cost of proof generation but most of the gas fees are recovered.

Of course, the proof will exist only if the aggregator has processed the proposed batches correctly, meaning they have an order and *all* of them need to be processed. It’s a mechanism similar to the “Force tx” implemented in Polygon Hermez v1.0, in that case useful to avoid censorship.

This mechanism avoids control of a single party and many of the potential attacks, since any Sequencer can propose a batch, but there is a cost on it.

And the Aggregators have the option to participate in a permissionless manner too, but if they don’t do it, there will be a moment when the economic value will be interesting for someone to do it.

In our case, the Polygon Hermez network would launch a Boot Aggregator backing up that there is a new validity proof at a specific frequency during the bootstrapping phase.

Fees will be distributed in the following way:

- Fees from L2 TXs will be processed and distributed  by the same aggregator that creates the validity proofs.
- All TXs fees will be sent to the corresponding Sequencer of each batch.
- The deposited fees from Sequencers to create a batch will be sent to the Aggregator that included this batch into a validity proof.

## Conclusions

The PoE consensus mechanism is ideated to solve some of the challenges of decentralized and permissionless validators in L2 for zk-rollups.

It defines a two-step model where it enables:

- Permissionless Sequencers as benefited participants in the protocol, also as a source of scalability of the network.
- A data availability model perfectly compatible with Volition (zk-rollup and Validium) schemas which could enable different tiers of service for users.
- The calculation of a “virtual” state from the data availability and a “final” state based on the validity proofs. This architecture can save a lot of cost for decentralized zk-rollups by settling validity proofs frequency based on different criteria, but not as the only solution to confirm transactions.
- Space for permissionless Aggregators as the agents to perform the specialized task of cryptographic proof generation, expected to be costly for zkEVM protocols. It provides a very simple and straightforward model for them to manage their incentives and returns.
- Native protection against L2 network problems such as attacks from malicious actors or technical problems of selected validators.
- Incentives model to maximise the performance of the network finality.

## Replies

**tudor-malene** (2022-02-11):

Hi David. Nice protocol.

All rollups should have a way to decentralise sequencing.

Here are a few questions and suggestions after a quick read.

1. Do sequencers coordinate?

Since anyone can be a sequencer, it means there must either be a gossip protocol, or a way for users to discover where to publish transactions. A normal user would probably publish the transaction to multiple sequencers to make sure it gets included quickly.

The reason why it is important to consider coordination is that publishing batches to the L1 is quite expensive. If the same L2 transactions get included in multiple batches, it might raise the costs.

If there is a gossip protocol, then it’s even worse since all transactions might end up included multiple times.

1. Do aggregators coordinate?

Similar question.

If all aggregators are watching the L1 for published batches and have similar incentives, they will attempt to submit the proof at the same time. Which can be relatively expensive. One could think of various attacks where a competing aggregator front-runs adversaries to push them out of business.

1. Fee distribution.

It’s not clear why an aggregator would distribute the fee to the sequencers. Is that behaviour somehow verified by the next proof?

---

**davidsrz** (2022-02-11):

Thanks for your comments, I’ll try to answer them.

1. Do sequencers coordinate?
The protocol does not limit that, but it’s not the main approach. In our vision, a sequencer could be a wallet app, an exchange or a game for example… in general, applications that have a use case or transactions brokers.
In any case, the model does not limit some party to setup an open sequencer or a network of coordinated sequencers, but this is out of the scope of our protocol.
2. Do aggregators coordinate?
The idea is that Aggregators compete.
But if they decide to coordinate (out of the scope of the protocol) that’s not a problem for the network, because by depositing some incentives in each batch the network is outsourcing the ZK proof calculation to the most efficient participant or participants in benefit of the network throughput.
It’s kind of a reverse auction where each permissionless Aggregator decides when it’s profitable to trigger the calculation of a proof according to the available incentives in the zk-rollup smart contract.
3. Fee distribution
Aggregators are permissionless participants and the only thing that they can do is running the enforced ZKP calculation. If they want to get a valid proof, they need to meet all the requirements including fees distribution (or the actions that have been encoded as required).

---

**CryptoWhite** (2022-02-13):

The consensus is similar to the idea of [PBS](https://notes.ethereum.org/@vbuterin/pbs_censorship_resistance) (Proposer/Builder Separation), where Sequencer == Proposer and Aggregator == Builder.

I think the Aggregator mechanism can be further improved to avoid the race between Aggregators. The race may result in a waste of both computation power for generating the proof and the gas fee for validating the proof. Besides, the batches cannot be settled+finalized because of the existence of Revert.

---

**tudor-malene** (2022-02-14):

Thanks David,

it makes sense.

![](https://ethresear.ch/user_avatar/ethresear.ch/davidsrz/48/5107_2.png) davidsrz:

> The protocol does not limit that, but it’s not the main approach. In our vision, a sequencer could be a wallet app, an exchange or a game for example… in general, applications that have a use case or transactions brokers.

I have a feeling the “Sequencer per app” approach without any coordination is quite vulnerable to someone submitting “double-spend” transactions to different sequencers, thus making them waste gas.

I struggled with these questions myself when working on the design of the [POBI](https://whitepaper.obscu.ro/obscuro-whitepaper/consensus.html) protocol. In my experience, it’s not an easy task to come up with a coordination mechanism that doesn’t transform the rollups into a sidechain.

![](https://ethresear.ch/user_avatar/ethresear.ch/davidsrz/48/5107_2.png) davidsrz:

> It’s kind of a reverse auction where each permissionless Aggregator decides when it’s profitable to trigger the calculation of a proof according to the available incentives in the zk-rollup smart contract.

My feeling here is that profitability will be the same for everyone, given the same inputs ( ethereum gas price, accumulated fees, etc). Is there another factor that might add some randomness?

![](https://ethresear.ch/user_avatar/ethresear.ch/davidsrz/48/5107_2.png) davidsrz:

> Aggregators are permissionless participants and the only thing that they can do is run the enforced ZKP calculation. If they want to get valid proofs, they need to meet all the requirements including fees distribution (or the actions that have been encoded as required).

Does this mean there is some more logic on the ethereum smart contract level besides the zkp verification logic?

Hope this is helpful.

---

**davidsrz** (2022-02-14):

Thanks CryptoWhite,

![](https://ethresear.ch/user_avatar/ethresear.ch/cryptowhite/48/8625_2.png) CryptoWhite:

> The consensus is similar to the idea of PBS (Proposer/Builder Separation), where Sequencer == Proposer and Aggregator == Builder.

Yes, both models have two separated roles, but the scope and the implementation of PBS are very different.

PBS is focusing on mitigating MEV centralization risks on L1 validators while in PoE the objective is to provide a permissionless model to enable decentralization on zk-rollups while solving issues like managing the gap between network confirmation and ZKP finality, which today is only achieved through a centralized operator.

![](https://ethresear.ch/user_avatar/ethresear.ch/cryptowhite/48/8625_2.png) CryptoWhite:

> I think the Aggregator mechanism can be further improved to avoid the race between Aggregators. The race may result in a waste of both computation power for generating the proof and the gas fee for validating the proof.

Yes, the Aggregator mechanism for sure can be improved. As you describe there is a waste of computation since only the most efficient will get the reward, but this probably will lead to a reduced number of competing Aggregators and it would not be a lot of total computation.

We are also considering the option to introduce some randomness in the ZKP acceptance or even to distribute the reward between close proofs in time. Ideas are very welcome here…

![](https://ethresear.ch/user_avatar/ethresear.ch/cryptowhite/48/8625_2.png) CryptoWhite:

> Besides, the batches cannot be settled+finalized because of the existence of Revert.

I think I don’t understand what you mean here, the Revert will be the result for late ZKP for the same set of batches (virtual states). The idea is that finality proofs validate a set of batches and not a single one, so we can optimize the L1 gas for the costly ZK proofs.

---

**StarLI-Trapdoor** (2022-04-01):

Hi, David, the protocol is clear and creative to seperate the “block” proposer and “block” committer, which are “sequencer” and “Aggregators” in the protocol.

By checking the replies from others, I have another one question about the size of “block” submitted by “sequencer”. For the current zk-Rollup solution, the “block” is submitted by the same operator, who tries to submit proof for the block. For that case, the “block” data can be minimal - only the raw data of Txs is needed, which is used for proof verification and data availability. The Tx signature checking logic is checked by offline circuits.

But if the Sequencer and Aggregator is seperated, more information should be included in the submitted block by sequencers. For example, the “signature” of one Tx should be included to keep Tx intact. And more than that, it seems that L1 should check the validity of Tx. If that’s true,  more data size and more gas are needed by L1.

Could you please share your idea about that? Thanks a lot ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=10)

---

**jbaylina** (2022-04-18):

We are planning two types of sequencer submissions transactions. Ones with the full signgatute that will be just included in the data availability, (The way you describe)

Other submission tx type will go with a zero knowlege proof that validates the signature and some formating. In this case the signature will not be necessary to be included.

For small small batches or for user “forced” TXs the first case will be used. But from certain break-even number of tx, we expect sequencers to include the proof to replace all the signatures of the block.

---

**StarLI-Trapdoor** (2022-04-18):

Cool.  Thanks a lot for your response.

The 2nd way to use ZKP proof to prove that all TXs in the batch are legal is brilliant. However, for that case, if only signature of one Tx is checked, the validality of one Tx is NOT checked, right? That’s to say, it’s possible that one sequencers can prove one proof of its batch, which contains “invalid” Txs (for example, balances are not enough or wrong target address, and so on).

If my understanding is correct, Aggregators have to prove one “rubbish” tx to be wrong. But from my experience, it seems not easy.

---

**jbaylina** (2022-04-18):

Exactly. You need to proof it any way in the batch. But you can skip the signature verification…

---

**bet3lgeuse** (2022-06-26):

[quote=“davidsrz, post:1, topic:11988”]

In this mechanism, the right to create the validity proof of a new state of the L2 (and of course, collect part of the fees in the txs) is earned simply by being the first aggregator to do it. [/quote]

[quote=“davidsrz, post:1, topic:11988”]

So, not being the first comes at the cost of proof generation but most of the gas fees are recovered. [/quote]

![](https://ethresear.ch/user_avatar/ethresear.ch/davidsrz/48/5107_2.png) davidsrz:

> by depositing some incentives in each batch the network is outsourcing the ZK proof calculation to the most efficient participant or participants in benefit of the network throughput

Hi, I am a Polygon fan and complete zkrollup newbie. I’m an architect doing a deep dive and trying to determine if Hermez is a good fit for my project relative to the MATIC side chain. The architecture makes sense for the most part on the Hermez 2.0 docs site, but the PoE algorithm gives me a lot of pause about the role of aggregators.

RealTimeBidding (RTB) protocols for advertising require fast bandwidth and sub 100ms latencies to ensure homogeneous UX to app users, or the central market operator kicks the auction participant. The prize for the auction is to sell inventory. By creating a “race” it seems to me that the PoE protocol is directly sponsoring an auction based market where the “winner” has an incentive to win the auction for some reason other than just being the winner (e.g. the fee) … just like a trading orderbook on a dark pool. As we’ve had to contend in non-blockchain systems for decades, performance games end up being highly centralized with FPGA hardware and highly centralized software. How does PoE not lead to aggregator centralization among a few players on the fastest interconnects with their own racks?

If I have a large B2C application and am running my own sequencers on AWS, my incentive is to run also my own validator to ensure higher than average probability that my blocks are processed as a hedge against being front-run or rejected with a higher than average probability by a competitor with the same strategy. The asymmetric loads from high volume applications and low volume applications would seem to lead to centralization with PoE, where only low-traffic sequencers would remain risk neutral, benefitting from the competition. The design problem as I see it is that high volume apps vs long-tail apps follow a power law among active traffic. The fastest aggregators can’t be gauranteed to remain benevolent, potentially turning byzantine with an opportunistic attack on the network.

I could be completely misunderstanding the nature of the “race” as too literal, and perhaps the lattitude in aggregator code to define its own strategies is severely limited by the amount of meta-data available to the strategy. But I am curious:  did the team consider using a VRF for the aggregators to select a round in a performance independent way, permitting a higher degree of decentralization with bandwidth and compute power agnostic interconnects? The risk of heavy fee losses during traffic spikes seems also like it could be weaponized to punish a larger actor on the network.

Thanks for all the work the team is doing on this project. I recognize that this is a colossal effort and I see a lot of great engineering going into it, and I think zkEVM is the most promising L2 solution.

---

**the-blocktopian** (2022-07-29):

Hi David,

I have a few questions I was hoping you could answer:

1. Is it correct to consider the profit in the zkEVM network to be a function of the user fee (for L2 transactions) - cost of publishing data to Ethereum? If yes, does this or a portion of the profit accrued by the network get distributed to MATIC stakers?
2. With Polygon Avail, can we expect the new data availability layer to become Avail, and then the only data cost is the cost of the final zk proof?
3. I understand that sequencers must deposit MATIC for the right to create transaction batches. Is there anything you can point me to that would help me determine what this deposit would be relative to the value of the transaction pool?

Thanks!

