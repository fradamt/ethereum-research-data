---
source: ethresearch
topic_id: 23090
title: Trustless Consensus Manipulation Through Bribing Contracts
author: 0xSooki
date: "2025-09-23"
category: Proof-of-Stake
tags: [security]
url: https://ethresear.ch/t/trustless-consensus-manipulation-through-bribing-contracts/23090
views: 230
likes: 3
posts_count: 1
---

# Trustless Consensus Manipulation Through Bribing Contracts

**TL;DR**: In our latest research, we designed, implemented, and evaluated three bribery attacks. They aim to violate three fundamental properties of consensus protocols.

- PayToAttest: Tramples safety by enabling vote buying (attestations).
- PayToExit: Incentivizes validators to cease participating in the consensus, thereby threatening liveness.
- PayToBias: RANDAO bribery market impacting fairness.

Our results show that these attacks are surprisingly cheap and practical, with bribes as low as 0.09 ETH (\approx 334 USD) to reorganize blocks ex-post (assuming rational validators accept the bribe whenever the bribe amount is slightly larger than the protocol rewards).

Paper link: https://eprint.iacr.org/2025/1719.pdf

Github link: [GitHub - 0xSooki/bribery-zoo: Trustless consensus manipulation through bribing contracts](https://github.com/0xSooki/bribery-zoo)

## Motivation

A common misconception is that the provided economic security “security budget” is proportional to the value of staked ETH (\approx115B USD). However, if validators act rationally, this threshold becomes much smaller in the short term, since a briber only needs to outpay protocol rewards marginally. Transparent, on-chain bribery contracts allow trustless, atomic, and cheap participation in our attacks. In this post, I aim to provide a brief overview of our key results; for further details, please refer to the [paper](https://eprint.iacr.org/2025/1719.pdf).

## The Bribery system model

Fair exchange is impossible without a trusted third party. Thus, we apply an on-chain bribery contract.

At its core, bribery entails a simple smart contract interaction.

- Step 1. Briber posts instructions along with some money.
- Step 2. Validator provides proof of deviation (e.g., signature, (zk) proofs).
- Step 3. The contract verifies the proof and pays the bribee.

[![Bribery system model](https://ethresear.ch/uploads/default/optimized/3X/5/b/5b5767756f7b9114f58cd836e99f40d2c1a1227a_2_517x154.png)Bribery system model864×258 23.6 KB](https://ethresear.ch/uploads/default/5b5767756f7b9114f58cd836e99f40d2c1a1227a)

The bribery contract makes the bribery atomic, without requiring any *additional* trust assumptions between the two parties.

## Preliminaries

After the Pectra upgrade with the inclusion of [EIP-2537: Precompile for BLS12-381 curve operations](https://eips.ethereum.org/EIPS/eip-2537) the cost of verifying BLS (aggregate) signatures on-chain in the EVM became not only feasible but relatively cheap. As the (current) consensus protocol heavily relies on BLS signatures, it provides trustless verification between the consensus and execution layers, making our work practical.

[![BLS verification gas costs](https://ethresear.ch/uploads/default/original/3X/9/6/9698808ebf77326d53a30a6e8d70d6ea2c987c8b.png)BLS verification gas costs508×444 23.5 KB](https://ethresear.ch/uploads/default/9698808ebf77326d53a30a6e8d70d6ea2c987c8b)

## Bribery contracts

We designed, implemented, and evaluated the following three types of bribery contracts targeting Ethereum validators.

1. PayToAttest - Enables vote buying

 Briber buys votes for the adversarial fork
2. Enables ex-post reorgs without majority stake
3. Cost of attacks:

**PayToExit** - Market for validator exits

1. Validators are paid to voluntarily exit the protocol
2. Increase adversaries’ relative staking power, thus threatening liveness
3. By our initial game-theoretical analyses for an entity with a 23% stake, to increase it to 33%, the optimal bribe amount would be 9.23 ETH

**PayToBias** - Auctioning RANDAO randomness contribution

1. Validators in the tail slots can bias Ethereum’s randomness beacon by withholding their block.
2. To our best of our knowledge, we built the first on-chain RANDAO bribery market.

## Performance evaluation (gas costs)

The following table shows the most important functions’ gas costs of our proposed bribing contracts. USD costs were computed using the ETH/USD exchange price and gas prices (3,708 USD/ETH and 1.63 Gwei gas price) on July 25th, 2025.

[![Gas costs](https://ethresear.ch/uploads/default/optimized/3X/9/b/9bbda8feb5c5b93aa3e690cbd9c8d9a28146d2bb_2_517x105.png)Gas costs1060×216 21.8 KB](https://ethresear.ch/uploads/default/9bbda8feb5c5b93aa3e690cbd9c8d9a28146d2bb)

### Sequence of an ex-post reorg

To further illustrate the potential harm that can be caused by such contracts, the next figure walks through how a briber can leverage the **PayToAttest** contract to buy attestations causing the honest votes to be outweighed by the bribed ones until the adversarial fork becomes the canonical chain. An adversary might be motivated to perform such a reorg to steal MEV from honest blocks, or the manipulate the RANDAO.

### Cost of an ex-post reorg

The next figure shows the cost of an ex-post reorg using our **PayToAttest** contract. Where the adversary seeks to fork out the block in slot n+1 with an alpha stake amount, the attack fails in the white region.

[![Ex-post reorg timeline](https://ethresear.ch/uploads/default/optimized/3X/8/1/813f5542e4d3f7fce1a957c39e0fdb4ead67c8d0_2_517x201.png)Ex-post reorg timeline1418×554 88.2 KB](https://ethresear.ch/uploads/default/813f5542e4d3f7fce1a957c39e0fdb4ead67c8d0)

## PayToExit bribery markets

A more in-depth analysis was done on the incentives in the **PayToExit** bribery market, to derive the optimal bribe amount. The market was modelled as a single-leader multiple-follower market exit game, in which a briber offers bribe b to n rational validators to exit the active validator set. A briber may want rational validators to stop being Ethereum validators to a) increase its relative staking power or b) to divert scarce capital from the deposit contract to another decentralized application (think of a DeFi protocol, e.g, liquidity provision in a DEX, or lending pool, etc.) of the adversary’s choosing.

Rational validators have two choices: a) Accept the bribe and leave the consensus protocol b) Deny the bribe and stay validating in the Ethereum consensus.

[![Single-leader multiple-follower market exit game](https://ethresear.ch/uploads/default/optimized/3X/3/a/3a61e7a5782ccc314c8578a6a41da0bab0011baf_2_517x223.png)Single-leader multiple-follower market exit game1018×440 22.7 KB](https://ethresear.ch/uploads/default/3a61e7a5782ccc314c8578a6a41da0bab0011baf)

Solving the game, we derived a range for calculating the optimal bribe amount that is

R(n-k+1) \cdot \mathrm{PV}(r,Y)\leq b^* \leq R(n-k) \cdot \mathrm{PV}(r,Y).

where

    R(n) = {\underbrace{32}_{stake} \cdot \bigg(\underbrace{\frac{2940.21}{\sqrt{n}}}_{\text{protocol rewards}} + \underbrace{\frac{1078543.3}{n}}_{\text{estimated MEV}}\bigg)} \quad \mathrm{and} \quad \mathrm{PV}(r,Y) = \frac{1.08^{-9}}{0.08\cdot100}

Using the optimal bribe range, there exists an equilibrium in which exactly enough validators exit to raise the adversary’s stake from \alpha to \alpha^*, but no validator has an incentive to unilaterally change their strategy.

The next figures show the bribe costs (in USD) and the attack duration (in days), when an adversary would like to increase their relative staking power from \alpha to  \alpha^* (\alpha \le \alpha^*).

[![PayToExit attack cost and duration](https://ethresear.ch/uploads/default/optimized/3X/1/0/1062f78be8c97bf788fdcdf8dc4c2e27620380e9_2_517x181.jpeg)PayToExit attack cost and duration1422×500 119 KB](https://ethresear.ch/uploads/default/1062f78be8c97bf788fdcdf8dc4c2e27620380e9)

There are many more discussions and results in our [paper](https://eprint.iacr.org/2025/1719.pdf).

## Countermeasures

How could Ethereum defend against these bribery attacks? What shall/could Ethereum protocol designers do to make the protocol more robust?

- Increasing honest participation rewards: maybe unwanted because it dilutes the Ethereum supply if done carelessly?
- Adding whistleblowing incentives: huge design space
- Single-slot finality (preventing PayToAttest forks)
- Unbiasable randomness beacon (mitigation for PayToBias)

## Future research directions

- Anonymity and Privacy: it would be interesting to hide the details of our bribery contracts. That would make our bribery markets more practical as participants would be less reluctant to join.
- Additional Bribery Contracts: using our framework, it is conceivable that new bribery contracts can be easily implemented. For instance, PayToInclude or PayToCensor, where a certain transaction is requested to be {in/ex}cluded in/from the blockchain.
- Game-theoretic analyses: numerous game-theoretic open questions. In particular, we did not analyse our PayToAttest or the PayToBias bribery markets from a game-theoretic point of view.
- Attack Robustness vs. Inflation An interesting trade-off could be studied between protocol robustness against bribery attacks vs. increased inflation. What is the sweet spot here?

Feel free to reach out, leave comments, questions, feedback, and criticism!

Happy Bribing! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)
