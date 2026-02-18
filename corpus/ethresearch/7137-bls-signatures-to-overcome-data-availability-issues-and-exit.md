---
source: ethresearch
topic_id: 7137
title: BLS signatures to overcome data availability issues and exit games in Plasma
author: mharishankar
date: "2020-03-17"
category: Layer 2 > Plasma
tags: [zk-roll-up, signature-aggregation]
url: https://ethresear.ch/t/bls-signatures-to-overcome-data-availability-issues-and-exit-games-in-plasma/7137
views: 2869
likes: 1
posts_count: 3
---

# BLS signatures to overcome data availability issues and exit games in Plasma

Hi folks,

We have developed a mechanism based on BLS signature aggregation to enable Plasma-style smart-contracts, that overcome the data availability problem and avoid exit games. At a high-level, we achieve this by requiring participants’ signatures on a Merkle root before it is committed to the root chain. We design a protocol to allow for the L2 chain to securely move forward even when some participants are temporarily offline or withhold their signatures maliciously. This mechanism results in orders of magnitude lesser curve exponentiations and signature verifications for the operator and the smart-contract; on the other hand, gas costs are estimated to scale with the number of missing participants in each round (and O(1) in number of transactions). In ZK Rollup, for ex, gas costs (roughly) increase instead with the number of transactions.

Our preprint is available here: https://arxiv.org/abs/2003.06197 . The context and model we motivate in this work (that the side-chain is applied to) is a generic 2-sided marketplace.

Please let us know if you have any questions/comments or just interested in talking about it more.

Best regards,

Madhu & team

## Replies

**adlerjohn** (2020-03-18):

Reviewer number: 1

In section III-D, you describe a set of desirable properties for side chains. The first few are essentially identical to those in the framework developed by Adler et al. in [Building Scalable Decentralized Payment Systems](https://arxiv.org/abs/1904.06441) (see: definitions 2.4 and 3.4). You should actually be using that paper as a baseline metric for the quality of layer-2 systems. Pay close attention to the last paragraph on page 8, though. The latter few properties are more specific to your design, or follow from the rest.

One important point that arises from the above is that Plasma Go is permissioned, as opposed to rollups which are permissionless. This facet needs to be discussed, as it’s a property that rollups make a sacrifice to have.

Another important point is that rollups allow for arbitrary state transitions, so long as [validity proofs](https://ethresear.ch/t/on-chain-scaling-to-potentially-500-tx-sec-through-mass-tx-validation/3477) or [compact fraud proofs](https://ethresear.ch/t/minimal-viable-merged-consensus/5617) can be made. ZK rollups are constrained by the practicality of prover time, but there’s nothing stopping them in theory from allowing arbitrary state transitions. In addition to smart contracts, this means you can do atomic swaps to immediately withdraw funds. You can’t close a channel immediately, so consumers in your proposal *need* to wait a potentially long time to withdraw their funds. This is a downside that needs to be including when comparing to other proposals, such as ZK or optimistic rollups.

A few more issues I see:

1. Your proposal is custodial/vulnerable to griefing, or degenerates to a rollup. The operator can withhold a payment from a consumer to a provider. The only recourse would then be to force this transaction to be processed by posting it on-chain. You can’t penalize the operator or the provider in this case since data unavailability is a non-uniquely attributable fault, the system degenerates into a rollup with extra steps.
2. Exits are large. Each exit needs to be accompanied by a significant amount of data that must be posted on-chain.

Overall, your proposal is a simple modification on [Plasma Cash](https://ethresear.ch/t/plasma-cash-plasma-with-much-less-per-user-data-checking/1298): rather than having channels whose ownership is transferred and using a blockchain to prevent double-spending of ownership transfer, you set up channels and use the operator as an intermediary to route payments. This has the advantage over Plasma Cash that transaction *sends* are instant, though *receives* are not. Which isn’t much of an improvement over Plasma Cash, which you should have compared your system to rather than Plasma MVP. The disadvantage is that the operator can block payments, which causes degeneration to a rollup unless you want to allow griefing or make the operator a custodian.

[This recent paper](https://eprint.iacr.org/2020/175) by Dziembowski et al. proves some lower bounds on Plasma constructions, namely either mass exits (and therefore not trust-minimized) or large exits. Your proposal falls under the latter category, except for where it degenerates to a rollup.

Reviewer recommendation: reject.

---

**mharishankar** (2020-03-18):

[@adlerjohn](/u/adlerjohn) Thanks for reading the work and providing your feedback. Rebuttal:

- Good point about citing Building Scalable Decentralized Payment Systems. Our definitions, however, are specific to the marketplace scenario as we clearly state. That allows us to define properties which are more reasonable in a marketplace: e.g. Consumer Safety is defined such that I don’t care about consumers being able to withdraw funds they’ve deposited into the contract for use in this marketplace as long as their funds cannot be misappropriated. Also, our model, to the best of my knowledge, is the first formalization of a Plasma-style L2 chain with periodic Merkle root commitments, atleast for the marketplace.
- Indeed, makes sense to discuss the tradeoff between Plasma Go and ZK Rollup in terms of being permissioned. Confirmed funds are defined in the model only as those which have already been included in a committed Merkle root, in which case, Plasma Go ensures that there is zero chance of anyone cheating the provider out of those - hence no exit games. However, the operator may indeed cause griefing by excluding payments that providers are owed in the next commitment. We do not claim to solve griefing in this work, and I believe this is discussed somewhere in the text. Agree that it will help to highlight in a discussion section.
- I dont understand what you mean by being unable to close a channel immediately. (1) I don’t allow consumers to withdraw at all, by definition of Consumer Safety in the model. I expect them to deposit only what they wish to use in the marketplace. Allowing consumers to withdraw will necessarily introduce a wait-time where others must be given a chance to contest the exit. (2) Operators and Providers can withdraw anytime without any wait-time. That is one of the goals Plasma Go meets.
- An exit for most providers is a Merkle proof. In addition, for each consumer in whose channel the provider has been promised funds from by the operator, the provider must reveal the consumer’s latest-known micropayment made to the operator. The cost of this component scales with the number of consumers that interact with a given provider; also depends on how frequently the providers exit. So yes, exits can become large, but not always - depends.
- Why would I compare this with Plasma cash? The entire idea is that the operator does not maintain dedicated channels with each provider - it is trivial to have an operator intermediary where operator receives payments from consumers on dedicated channels, then forwards them on dedicated channels on the other end. But, as noted in the paper, this incurs significantly liquidity burden on the operator and does not allow them to straightforwardly transfer the off-chain incoming funds in an off-chain fashion providers. Plasma Go affords Liquidity Pooling, i.e., enables this. By using Plasma-MVP style Merkle root commitments of the outgoing off-chain promises, but with BLS signatures to ensure that exit games are avoided and data availability attacks are impossible on notarized funds. We design the commitment generation/notarization and withdrawal process to ensure that the L2 chain can proceed (providers can get paid subsequently generated income) even when a subset of providers are missing during signing time, while also ensuring that these missing providers’ funds are never misappropriated.
- Ofcourse, ZK Rollups can do arbitrary state transitions; for the marketplace scenario (which is a considerable one given how many widely used two-sided digital markets exist), the state transition captured in the paper are predominantly sufficient and hence ZK Rollup and Plasma Go are compared in this specific context. Then, we show that Plasma Go results in significantly reduced computational costs for operator + contract, and monetary costs for the operator. As I noted though, the costs for the operator scale in this case with the number of providers that fail to sign a Merkle root. If ZK Rollup is applied here, costs will scale with the number of transactions that happen in the marketplace.
- I will check out the recent work you’ve linked to. One thing to keep in mind (without me having read it yet) is that we do not compare  with ZK Rollup or other Plasma construction for arbitrary off-chain payments, which will involve broader claims and, in some cases, more stringent properties to be fulfiled.

