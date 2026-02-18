---
source: ethresearch
topic_id: 19760
title: Censorship Resistance Through Game Theory
author: antonydenyer
date: "2024-06-07"
category: Proof-of-Stake > Block proposer
tags: [proposer-builder-separation, censorship-resistance]
url: https://ethresear.ch/t/censorship-resistance-through-game-theory/19760
views: 2621
likes: 1
posts_count: 1
---

# Censorship Resistance Through Game Theory

> tldr; relays should divulge more metadata about the block so that validators can make more informed decisions that align with their preferences

> Thanks to @simbro @mmp for early feedback

Censorship resistance is a fundamental property that underpins the decentralised nature of blockchain networks and ensures the integrity and accessibility of transactions within the system. While the threat of “hard censorship” is well understood, the challenges faced by preventing “soft censorship” resistance are more nuanced.

“Soft censorship” involves delaying or slowing down the propagation and inclusion of valid transactions. It could be accidental or deliberate; either way, it disrupts the normal flow of transactions, negatively impacts execution quality and harms user experience.

“Hard censorship” means the complete and permanent prevention or blocking of valid transactions from landing on-chain (e.g., OFAC compliance). The majority of research on censorship resistance has focused on this topic.

Previous approaches to mitigating censorship have focused on inclusion lists and tend towards some form of unconditionality. A proposer must include a transaction, or it is a protocol violation.



    ![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png)

      [Unconditional inclusion lists](https://ethresear.ch/t/unconditional-inclusion-lists/18500) [Block proposer](/c/proof-of-stake/block-proposer/10)




> Unconditional inclusion lists
>  [upload_d8336517ff27bb713b162aea8e862611]
> ^lol
> \cdot
> by mike & toni based on discussions with potuz & terence
> \cdot
> tuesday – january 30, 2024
> \cdot
> tl;dr; Inclusion lists return agency to the proposer in a PBS world by allowing them to express preferences over the transactions included onchain, despite outsourcing their block production to the specialized builder market. This document discretizes the inclusion list design, advocates for a specific feature s…

By applying game theory principles to PBS, incentives can be leveraged to foster etherum aligned outcomes. Our goal is to create a scenario where including all valid transactions and resisting censorship attempts becomes the dominant strategy for block builders. This approach not only addresses the challenges of soft censorship but also mitigates the risks of hard censorship. It has the potential to improve the integrity of ethereum significantly.

This proposal is not meant to replace inclusion lists but should be considered a progressive move towards more robust forms of censorship resistance.

## What motivates validators

Under mev-boost, the most profitable block always wins; this assumes that all actors in the PBS auction are rational. However, it fails to account for the fact that some validators are motivated by factors other than profit. PBS has impacted censorship resistance and pushed the network towards centralisation. Many validators (over 8% at last count) refrain from using mev-boost, perhaps because of concerns around censorship and centralisation. Validators may perceive themselves as being more ethereum aligned if they are not running mev-boost because they accept transactions that block builders censor.



    ![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png)

      [Is it worth using MEV-Boost?](https://ethresear.ch/t/is-it-worth-using-mev-boost/19753) [Economics](/c/economics/16)




> Is it worth using MEV-Boost?
> To answer that question from an economic perspective, we will look into the APYs.
> > For simplicity, we assume a total of 1 million active validators and ignore sync-committee rewards.
> > The underlying data ranges from November 2023 - 6 June 2024 and includes all slots.
> First, let’s check the difference between local block building and using MEV-Boost.
> We can see that the block reward is higher for MEV-Boost users:
>  [reward_comparison (3)]
> The median block rewar…

## Block Builders

The current implementation of PBS is designed so that block builders will pay the maximum possible to validators, to the detriment of all other factors. One reason PBS was introduced was the idea that block builders would be better at building blocks than validators, especially solo validators. They would be better connected and have access to private order flow. The problem is that better was assumed to mean more profitable. The current optimum strategy is to be a vertically integrated searcher builder that can pay the most for a block. Anything that gets included in that block is secondary and only there to reduce the cost burden on the purchase of the block.

We need to change the game, so the optimum strategy is to fill the block with as many transactions and blobs as possible within the protocol’s constraints and pay the validator for the privilege. Put another way, block builders should be better at building blocks than validators. To achieve this new optimum strategy, they must be well connected to the far reaches of the network, accept transactions from any source, and include all valid transactions.

In short we need to force the transaction supply chain to be more representative of validators wishes.

[![chart showing 10% validators censor - 39% builders censor](https://ethresear.ch/uploads/default/original/3X/b/c/bce4e393de8cc20c5571269b8ac90ab767c26d3d.png)](https://www.antonydenyer.co.uk/assets/img/blog/block-proposer-inclusion-lists/censorship-pics.png)

Source: https://censorship.pics/

## How to introduce a dilemma

Currently, block proposers are missing out on priority fee rewards. Let’s assume an OFAC censored transaction is in the mempool tc, and a block builder creates a ‘censored’ block bc. The total amount of rewards available is bc + tc. However, the block proposer only gets bc. The block proposer is choosing to accept bc because the rewards are greater than what they could build themselves (see [builder_boost_factor](https://ethereum.github.io/beacon-APIs/#/Validator/produceBlockV3)). The block builder knows it can build a better block than the block proposer as they have more order flow. The only thing that keeps the block builder from bidding just above the fees in a block containing mempool transactions is healthy competition between block builders.

Previous works have explored the possibility of a multi-proposer system or partial block auctions requiring significant protocol and infrastructure changes.



    ![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png)

      [Concurrent Block Proposers in Ethereum](https://ethresear.ch/t/concurrent-block-proposers-in-ethereum/18777) [Block proposer](/c/proof-of-stake/block-proposer/10)




> Concurrent Block Proposers in Ethereum
>  [upload_9cfebe6c788a99112f6efb3a851deac0]
> ^look ma, we are trying to end the proposer monopoly
> \cdot
> by mike & max – friday; february 23, 2024.
> \cdot
> Abstract: The Ethereum protocol elects a single proposer to produce a block during each 12-second slot. That proposer has unilateral authority over the set of transactions included. As a result, time-sensitive transactions can be censored by a single party. We present an initial analysis of increasing th…



    ![](https://ethresear.ch/user_avatar/ethresear.ch/barnabe/48/4742_2.png)

      [Unbundling PBS: Towards protocol-enforced proposer commitments (PEPC)](https://ethresear.ch/t/unbundling-pbs-towards-protocol-enforced-proposer-commitments-pepc/13879) [Economics](/c/economics/16)




> Many thanks to @fradamt @casparschwa @vbuterin @ralexstokes @nikete for discussions and comments related to the following post. Personal opinions are expressed in the first-person-singular.
> Protecting the proposer and ensuring liveness of the chain are a big part of why PBS is considered to be moved into the Ethereum protocol. Ideally, when the proposer utilises the services of a builder, there is a contract between parties for the delivery of some goods (valuable blockspace), and the contract …

## Proposer inclusion lists

To introduce some form of dilemma for the block builder, the block proposer should have better visibility of what they are delegating. Currently, the relay only exposes information about fee rewards and gas used. We could [extend builder_boost_factor](https://github.com/ethereum/beacon-APIs/issues/450) to include an opinion about gas used that would only require changes on the consensus layer client. But let’s go much further; the relay should publish the transaction hashes of the winning bid. The consensus layer client can then check against its view of the mempool and decide if it wants to delegate block building to that relay.

To frame this in more formal game theoretical terms and notation, we can consider the interaction between the block proposer and the block builder as a strategic game. This game involves decisions on whether to include certain transactions (t1 and t2) in the block, based on the incentives (tips and MEV) associated with each transaction. The players in this game are the block proposer and the block builder, and their strategies involve deciding which transactions to include or censor.

## Game Setup

Players: Block Proposer (P) and Block Builder (B).

## Strategies:

For Block Proposer `(P)`: Accept `(A)` or Censor `(C)` transactions.

For Block Builder `(B)`: Accept `(A)` or Censor `(C)` transactions.

Payoffs: Defined in terms of gwei received from tips and MEV.

## Transactions

`t1`: A censored public mempool transaction paying `1` gwei in tips.

`t2`: A private transaction paying `2` gwei in tips and `2` gwei in MEV.

## Payoff Matrix

The outcomes of the game can be represented in a payoff matrix where the rows represent the Block Builder’s strategies, and the columns represent the Block Proposer’s strategies. The payoffs are represented as tuples, with the first element being the payoff for the Block Proposer and the second element being the payoff for the Block Builder.

| B \ P | Accept (A) | Censor (C) |
| --- | --- | --- |
| Accept (A) | (3, 2) | (3, 2) |
| Censor (C) | (1, 0) | (2, 2) |

## Analysis

Builder censors and proposer censors (C, C): The block contains `t2`. The proposer receives `2` gwei in tips, and the builder receives `2` gwei in MEV. This is a Win-Lose scenario in the original description, but in game-theoretical terms, it’s a Nash Equilibrium if the builder’s payoff for censoring is higher than accepting without proposer enforcement.

Builder censors and proposer accepts (C, A): The proposer chooses to build a block with `t1`, receiving `1` gwei in tips. The validator is “eth aligned” and wishes to forgo the additional rewards. It is a Lose-Lose scenario, indicating a misalignment of strategies leading to suboptimal payoffs for both players.

Builder accepts and proposer accepts (A, A): The block contains both `t1` and `t2`. The proposer receives `3` gwei in tips, and the builder receives `2` gwei in MEV. This is a Win-Win scenario, representing a Pareto optimal outcome where no player can be made better off without making the other player worse off.

Builder accepts and proposer censors/doesn’t enforce (A, C): The block contains both `t1` and `t2` because it is more profitable. The proposer receives `3` gwei in tips, and the builder receives `2` gwei in MEV. This is also a Win-Win scenario, similar to (A, A), indicating that the proposer’s decision to censor does not change the outcome due to the builder’s acceptance.

In this strategic game, the optimal outcomes for both players are when both accept the transactions, leading to a Win-Win situation. The game illustrates the importance of alignment in strategies between the block proposer and the block builder to maximize their respective payoffs.

## Summary

Some validators need to be irrational (10% already are) whilst using mev-boost. Solo Validators Can Stay Retarded Longer Than Block Builders Can Stay Solvent.

The threat of not accepting a block builder’s block should be enough incentive for them to choose not to censor transactions.

Which validators censor and which do not will become apparent over time. This may mean that block builders will change their tactics depending on who is proposing the next block.

Smaller transactions and participants are less likely to be sidelined by profit-maximising behaviour. This will lead to priority fees trending downwards.

Block builders will help strengthen the network rather than centralise it.

No hard fork required. The only changes needed are in the relay spec, the consensus layer client and some minor changes in the execution client.

The only downside I can foresee is that relays may be leaking some information to other block builders.

Minor changes to clients

Minor changes to relay infrastructure

# Conclusion

In summary, by leveraging game theory principles, this proposal aims to significantly reduce transaction censorship by block builders, fostering a more inclusive and decentralized network. In the best case, it will lead to the cessation of censorship practices among block builders, enhancing the network’s integrity. In the worst case, given the relatively minor changes required, it might represent a learning opportunity with minimal loss. At the very least, it promises to stimulate more competition and differentiation within the block builder market, contributing to the overall health and diversity of the ecosystem.
