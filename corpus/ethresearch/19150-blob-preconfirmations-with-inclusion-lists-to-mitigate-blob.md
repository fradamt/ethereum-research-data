---
source: ethresearch
topic_id: 19150
title: Blob Preconfirmations with Inclusion Lists to Mitigate Blob Contention and Censorship
author: chrmatt
date: "2024-03-29"
category: Proof-of-Stake > Economics
tags: [mev, layer-2, censorship-resistance]
url: https://ethresear.ch/t/blob-preconfirmations-with-inclusion-lists-to-mitigate-blob-contention-and-censorship/19150
views: 2842
likes: 24
posts_count: 15
---

# Blob Preconfirmations with Inclusion Lists to Mitigate Blob Contention and Censorship

Thanks to my collaborators [@murat](/u/murat), [@ckartik](/u/ckartik), [@Evan-Kim2028](/u/evan-kim2028), and [@bemagri](/u/bemagri). Further thanks to the ETHGlobal London community for early feedback and in particular Nethermind for awarding a prize at the hackathon for our credible preconfirmation leader auction.

# Introduction

In this post, we describe an out-of-protocol mechanism for blob inclusion preconfirmations. It allows preconfirmation providers to bid in an auction to become the leader for the subsequent slot. The auction winner can then accept bids on blob inclusions and issue preconfirmations to the bidders. The preconfirmed blobs then act as an inclusion list that needs to be respected by all participants. The goals of this design are to enable L2 sequencers and other entities relying on blob inclusion to gain certainty about their inclusion, prevent censorship, and possibly mitigate latency issues of blocks with many blobs in the future. Our out-of-protocol design can be implemented right now and serve as a starting point to measure and understand blob inclusion lists in practice until they are available natively in the Ethereum protocol.

Given recent issues with blob contention [1,2], we believe it is timely to implement an out-of-protocol solution as the one described here.

We next provide an overview of the entities involved in the protocol and then describe the protocol in more detail. We then provide more details on the payment and slashing mechanism. We conclude with discussions on the N+1 slot design, the leader auction, and how to handle premature blob inclusion.

# Actors

We assume there is a sidechain (with a faster block time than L1) that is used to settle payments among the protocol participants. This chain in the following is called *mev-commit chain*.

The following actors participate in the protocol:

- L1 proposers. We assume a subset of L1 validators opt-in to participate in the protocol and stake a collateral on the mev-commit chain.
- Relays. The opted-in proposers need to exclusively work with relays that participate in the protocol and only forward blocks from builders that also participate in the protocol.
- Preconfirmation providers. These are the actors bidding to become the blob preconfirmation leaders and issue the blob inclusion lists. They could be the proposers themselves, builders, or relays. For this write-up, we assume the relays play the role of preconfirmation providers.
- Preconfirmation bidders. The entities who want blobs to be included in a block, such as L2 sequencers.
- Builders. The builders need to be aware of the blob inclusion lists and include the corresponding blobs in their blocks.

# Protocol Description

We next describe the protocol execution in more detail. Let N be the current L1 slot and consider preconfirmation bidders want to include blobs in a block by slot N+1 (see below for a justification of the one-slot delay).

The protocol description is divided into three steps. The first is done during slot N, the second at the beginning of slot N+1, and the last one during the rest of slot N+1. See also the figures below for graphical overviews of the corresponding steps.

## Protocol Execution in Slot N

1. During L1‘s slot N, preconfirmation bidders send their bids to the providers. A bid contains the hash of the KZG commitment of the blob, the bid amount, and the target slot N+1, and is signed by the bidder.
2. Preconfirmation providers collect preconfirmation bids during L1 slot N.
3. The relays further submit leader bids for slot N+1 to the leader auction.

[![Fig. 1: Protocol overview for Slot N.](https://ethresear.ch/uploads/default/optimized/2X/7/78d6d4a75c61c8924502b41d72fa6adfa2853f0f_2_689x304.png)Fig. 1: Protocol overview for Slot N.1212×534 19.2 KB](https://ethresear.ch/uploads/default/78d6d4a75c61c8924502b41d72fa6adfa2853f0f)

## Protocol Execution at the Beginning of Slot N+1

1. At the beginning of slot N+1, the leader auction declares the provider with the highest bid as the leader for slot N+1 by publishing the leader together with the auction price on the mev-commit chain. The auction further settles the payment from the leader to the proposer.
2. The elected leader can now issue preconfirmations. Note that the leader has already received all preconfirmation bids for that slot and, therefore, can issue all preconfirmations immediately. They do so by publishing a blob inclusion list on the mev-commit chain. This list is final at this point and includes all bids including the blob KZG commitment hashes the leader commits to. To avoid timing issues in the next step, we can require the inclusion list to be published sufficiently early, e.g., within the first 6 seconds of the slot (and ignore lists published too late).

[![Fig. 2: Protocol overview for beginning of slot N+1.](https://ethresear.ch/uploads/default/optimized/2X/4/4ed8dfebb950c5c7877ade27b2d878d918a04cb0_2_690x486.png)Fig. 2: Protocol overview for beginning of slot N+1.849×599 45.9 KB](https://ethresear.ch/uploads/default/4ed8dfebb950c5c7877ade27b2d878d918a04cb0)

## Protocol Execution During Slot N+1

1. The builders receive from the mev-commit chain the inclusion list of blobs that are mandated to be in the block. Then, the builders build a block containing those blobs (in an order of their choice) and send it to the relays. Note that the builder can also include additional blobs if they choose to do so.
2. The relays only forward to the L1 proposer the blocks from builders that opted-in to the protocol. The relays can also optionally verify that the blocks respect the blob inclusion list (or simply trust the builders in case of optimistic relays).
3. The proposer signs a block header received from a relay (this can be done optimistically without checking for blob inclusion).

[![Fig. 3: Protocol overview for slot N+1.](https://ethresear.ch/uploads/default/optimized/2X/5/5498d249fa6e64846cf1c2a555e5b2c93a003873_2_690x330.png)Fig. 3: Protocol overview for slot N+1.1153×553 41.6 KB](https://ethresear.ch/uploads/default/5498d249fa6e64846cf1c2a555e5b2c93a003873)

## L1 Monitoring

1. An oracle monitors the L1 chain for blocks and reports to the mev-commit chain when a block is proposed by an opted-in proposer, who the proposer is, and whether this block (or a previous block) contained the blobs from the inclusion list. The oracle may want to wait for L1 finality to avoid reorg issues.
2. If the oracle reports a blob inclusion list violation, slashing is executed (see below for details).

## Payments and Slashing

We consider the following rules for payments and slashing.

The following two types of payments are always executed (even if blobs are not included, slots get missed, etc.):

1. The preconfirmation leader pays the amount for winning the leader auction to the L1 proposer (regardless of whether any preconfirmations are issued; this is because they participated in the auction and won the rights to become the leader).
2. For all blobs in the inclusion list, the preconfirmation bidders pay the corresponding amount to the preconfirmation providers (regardless of whether the blob actually gets included; bidders may get reimbursed via slashing of proposers as described below).

If the oracle reports that a blob from an inclusion list is not included in an L1 block in slot N+1 or earlier, we need to execute slashing. There are different scenarios that can lead to a blob from the inclusion list not being included on L1:

1. An opted-in relay sends a block not containing the blob.
2. The proposer includes a block from an external relay.
3. The proposer proposes their own block.
4. The proposer misses the slot.
5. The block gets proposed but then orphaned in a reorg.

In the first case, the relay or the builder violated the protocol, while in cases 2, 3, and 4, it is the proposer’s fault. Without additional mechanisms, the proposer cannot prove which relay has sent what block. We therefore always slash the proposer. If it was indeed the relay’s fault, the relay’s reputation with the proposer gets “slashed” in the same way as the relay sending invalid blocks. If in turn the relay has received that block from an opted-in builder, that builder’s reputation with the relay is “slashed” and they can settle the dispute out-of-protocol with existing mechanisms.

The last case is special since it may not be the fault of anyone involved and constitutes a general reorg risk the proposers need to consider. The slashing amount therefore needs to be set such that proposers still can make profit overall.

The slashed amount is distributed to the preconfirmation bidders proportionally to their bid amounts since they are the ones harmed by the protocol violation.

# Further Details and Discussions

## N+1 Slot Design

In our protocol, preconfirmation bidders bid in slot N for blob inclusion in slot N+1. This means that there is an expected one-slot delay between bidding and blob inclusion. While this would be unacceptable for time-sensitive transactions, e.g., for mev extraction, blob inclusion is substantially less time-sensitive.

We further note that this next-slot inclusion list design is also used in EIP-7547 [3]. The lack of an out-of-protocol next-slot design and consequently the lack of real-world data from such designs has recently been criticized in the context of L1 inclusion lists [4]. Hence, the availability of this via mev-commit can be used to gather data about the efficacy of next-slot inclusion lists and can serve the Ethereum Foundation to make an effective decision based on the obtained empirical data.

The purpose of the delay is to ensure that at the time the block builders want to build the block, the blob inclusion list is available to them. Furthermore, this allows the preconfirmation leader of slot N+1 to preconfirm blobs at the beginning of the slot. By doing so, all participants know which blobs are going to be included in the block of slot N+1 way ahead of the end time of that slot. In particular, the L1 validators could in the future use this information to pre-fetch the blob data at this time, thereby mitigating reorg risks due to long blob propagation (see, e.g., [5]). Having a predetermined leader also means that once the leader issues a preconfirmation, all participants can immediately rely on the blob inclusion, which allows for synchronous composability.

## Leader Auction

The auction to determine the preconfirmation leaders should ideally be credible, i.e., not require a trusted auctioneer. There are different ways to achieve this, and the precise implementation is orthogonal to our preconfirmation design. One option using SUAVE was explored by the Primev team, which has built a prototype auction at ETHGlobal London and was awarded a prize from Nethermind [6]. Another option is to use cryptographic tools such as timed commitments to realize the auction [7]. As an intermediate solution, the auction can also be run by a trusted actor.

## Premature Inclusion of Blobs

Leaders can issue preconfirmations for blobs to be included in slot N+1. However, before slot N+1, some builder (possibly outside of our protocol) may have already included this blob in a block that is now part of L1. In such a case, all payments are executed as described above and no slashing takes place. The preconfirmation bidders got their blobs included even earlier than expected and nobody else is harmed in this scenario.

# Conclusion

We have presented an out-of-protocol mechanism for blob inclusion lists. As long as inclusion lists are not available as part of the Ethereum protocol, we believe our solution offers a viable solution to the current issues with blob contention. Since it is a next-slot design, findings from this solution can further help to improve the understanding of such designs, which are also considered for L1 inclusion lists.

Currently, mev-commit for transaction preconfirmations is live on the Holesky testnet and we are excited to add an implementation of the design discussed here. We are looking forward to feedback to further refine and improve this system.

# References

[1] https://twitter.com/bertkellerman/status/1773031698222989623?s=46

[2] https://twitter.com/mcutler/status/1773033173573628009

[3] [EIPs/EIPS/eip-7547.md at 30fec793f3cb6769cb44d2d0daa5238451f67c48 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/blob/30fec793f3cb6769cb44d2d0daa5238451f67c48/EIPS/eip-7547.md)

[4] [The Case for ILECTRA - HackMD](https://notes.ethereum.org/@mikeneuder/the-case-for-ilectra)

[5] [Validator Timing Game Post EIP4844](https://ethresear.ch/t/validator-timing-game-post-eip4844/18129)

[6] https://ethglobal.com/showcase/blobpreconf-auction-qfdco

[7] [Riggs: Decentralized Sealed-Bid Auctions](https://eprint.iacr.org/2023/1336)

## Replies

**Julian** (2024-03-29):

Hi! Thanks for your post, it is very interesting! Although the demand for preconfirmations is clear, I would love some more clarity on how this design solves blob contention and censorship.

First, contention between blobs stems from too many blobs competing for a scarce protocol product. It is unclear to me how preconfirmations avoid contention since the protocol product is as scarce with this design as without, and bidding is also possible in-protocol.

Secondly, inclusion lists improve censorship resistance by tapping into the [entropy that a decentralized validator set](https://ethresear.ch/t/unbundling-staking-towards-rainbow-staking/18683) creates. Since proposers outsource their preconfirmation provider duties to a leader in this design, it is not clear to me that this design also taps into the entropy of the validator set. Wouldn’t the preconfirmation providers also become specialized entities, as in mev-boost?

In general, I think this design is very interesting but looks more like a parallel [slot auction](https://mirror.xyz/0x03c29504CEcCa30B93FF5774183a1358D41fbeB1/CPYI91s98cp9zKFkanKs_qotYzw09kWvouaAa9GXBrQ) in which the proposer sells its rights to the preconfirmation leader. Therefore it may be more appropriate to see this not as an inclusion list but as a specific proposer commitment that is realized via a [PEPC](https://ethresear.ch/t/unbundling-pbs-towards-protocol-enforced-proposer-commitments-pepc/13879)-like system. Parallel block auctions in PEPC may benefit censorship resistance, but that is because [multiple parties](https://ethresear.ch/t/concurrent-block-proposers-in-ethereum/18777/5) are involved with block construction.

---

**Evan-Kim2028** (2024-03-29):

Hey Julian thanks for your comments. I can address some of your comments:

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> First, contention between blobs stems from too many blobs competing for a scarce protocol product. It is unclear to me how preconfirmations avoid contention since the protocol product is as scarce with this design as without, and bidding is also possible in-protocol.

We see the current in-protocol bidding mechanisms as inadequate to bid effectively for the scarce blobspace. Although bidding is possible in-protocol via the EIP-1559 max priority fee, it does not apply to the EIP-4844 transaction blob base fee for example. Furthermore in times of high volatility, in order to update a bid, the entire transaction must be resubmitted, which is very costly and [not recommended](https://github.com/ethereum/go-ethereum/blob/66e1a6ef496e001abc7ae7433282251a557deb2c/core/txpool/blobpool/blobpool.go#L159C7-L163C42). In contrast, submitting a preconfirmation bid only requires the blob sender to update their bid amount without having to resubmit the entire blob transaction into the mempool.

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> Secondly, inclusion lists improve censorship resistance by tapping into the entropy that a decentralized validator set creates. Since proposers outsource their preconfirmation provider duties to a leader in this design, it is not clear to me that this design also taps into the entropy of the validator set. Wouldn’t the preconfirmation providers also become specialized entities, as in mev-boost?

The design has the same trust assumptions that currently exist with mev-boost today because it is an out-of-protocol design

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> In general, I think this design is very interesting but looks more like a parallel slot auction  in which the proposer sells its rights to the preconfirmation leader. Therefore it may be more appropriate to see this not as an inclusion list but as a specific proposer commitment that is realized via a PEPC-like system. Parallel block auctions in PEPC may benefit censorship resistance, but that is because multiple parties are involved with block construction.

Thank you for sharing, that was an interesting read! I think it is accurate to describe this as a slot auction. However, wouldn’t the current inclusion list design being discussed under EIP-7547 also be considered a slot auction as well?

---

**Julian** (2024-03-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/evan-kim2028/48/15875_2.png) Evan-Kim2028:

> Although bidding is possible in-protocol via the EIP-1559 max priority fee, it does not apply to the EIP-4844 transaction blob base fee for example.

Just to be clear, are you saying that bidding is impossible for blobs? It makes sense that bidding via base fee does not work, but can you not bid via EIP-4844 max priority fee?

![](https://ethresear.ch/user_avatar/ethresear.ch/evan-kim2028/48/15875_2.png) Evan-Kim2028:

> In contrast, submitting a preconfirmation bid only requires the blob sender to update their bid amount without having to resubmit the entire blob transaction into the mempool.

This makes sense, but I’m wondering if this is not already possible today or more easily realized as an add-on to mev-boost where bidding happens through a separate transfer transaction instead of via resubmitting the blob? This would only require an update from a builder

![](https://ethresear.ch/user_avatar/ethresear.ch/evan-kim2028/48/15875_2.png) Evan-Kim2028:

> The design has the same trust assumptions that currently exist with mev-boost today because it is an out-of-protocol design

I’m not sure if we can say both designs have the same trust assumptions simply because they are out-of-protocol. mev-boost only does the part of what you call here the Leader auction. Then, this design requires extra trust assumptions in, e.g., the oracle and the sidechain.

![](https://ethresear.ch/user_avatar/ethresear.ch/evan-kim2028/48/15875_2.png) Evan-Kim2028:

> However, wouldn’t the current inclusion list design being discussed under EIP-7547 also be considered a slot auction as well?

These terms are all definitely starting to blur as different ways of constructing a block start to emerge. However, I would say EIP-7547 ILs are not necessarily slot auctions susceptible because 1) there is no auction 2) if there were an auction the commitment still needs to be made in block N not block N + 1 as in your design. In principle, pretty much any product could be auctioned via a slot or block auction, though. The difference is in your design, you explicitly match the criteria for a slot auction: you decide the winner before the winner commits to the contents of their part of the block.

---

**murat** (2024-03-30):

Great points. I’ve suggested adding a feature to mev-boost in almost every single mev-boost stewards meeting, and found it very difficult to get consensus. Some folks have suggested an experimental mev-boost version to address this, which we would be willing to participate in if there is community interest or other further action on it. It may be worth exploring a grant avenue to get interested parties together for this.

My understanding is that the EIP-4844 maxFeeperblobgas isn’t sufficient as it too gets burned, and blob producers are looking at using direct transfers to address this, which doesn’t help for DA costs as you may imagine. [@Evan-Kim2028](/u/evan-kim2028) may be able to add additional detail here.

Agree RE: trust assumptions of the chain and oracle, but commitments are cryptographic so technically one could take them elsewhere to settle without relying on the chain or the oracle, although this isn’t supported in the current testnet version.

The design here seems to match the definition of a slot auction as you point out, do you see that this can be improved in a meaningful way, or simply that it’s a property of this design? [@Julian](/u/julian)

---

**Julian** (2024-03-30):

Hi [@murat](/u/murat), thanks for your reply!

![](https://ethresear.ch/user_avatar/ethresear.ch/murat/48/12986_2.png) murat:

> Great points. I’ve suggested adding a feature to mev-boost in almost every single mev-boost stewards meeting, and found it very difficult to get consensus.

I may have been unclear since this is not necessarily a feature to mev-boost, as it is not a problem with the fair exchange between a builder and a proposer, instead it could be an add-on from a single builder. This should be straight forward and doesn’t require consensus as it is purely opt-in.

![](https://ethresear.ch/user_avatar/ethresear.ch/murat/48/12986_2.png) murat:

> My understanding is that the EIP-4844 maxFeeperblobgas isn’t sufficient as it too gets burned

From the [EIP](https://eips.ethereum.org/EIPS/eip-4844) it seems to me that the max_priority_fee_per_gas is not burnt just as in EIP-1559, but your point of resubmitting being costly makes sense!

![](https://ethresear.ch/user_avatar/ethresear.ch/murat/48/12986_2.png) murat:

> The design here seems to match the definition of a slot auction as you point out, do you see that this can be improved in a meaningful way, or simply that it’s a property of this design? @Julian

I think it is important to see this as a parallel slot auction instead of an inclusion list because it clarifies that this proposal is not an out-of-protocol substitute for inclusion lists that improve the censorship resistance of Ethereum since if inclusion lists do not have the forward property (that proposer N constrains the block of proposer N + 1 not their own block), they rely on altruism. This property cannot be achieved out-of-protocol. On the flip side though, seeing this as a parallel slot auction places it in the design space of (a specific instance of) diet-PEPC. It could for example be achieved using something like [PEPC-Boost](https://hackmd.io/@bchain/BJkarrEWp). This is useful because this design could maybe be composed with the previous research done on PEPC and, when launched, the data would be very useful to PEPC research, of which slot auctions are also a specific instance.

---

**Evan-Kim2028** (2024-04-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> Just to be clear, are you saying that bidding is impossible for blobs? It makes sense that bidding via base fee does not work, but can you not bid via EIP-4844 max priority fee?

I am not saying that bidding is impossible - rather I am saying that the only way to “bid” for type 3 blob transactions is to use the type 2 priority fee mechanism, which only applies to the block base fee gas and not the blob base fee.

There does not exist a `max_priority_blob_fee` that lets one bid on the type 3 transaction contents, such as blob gas, directly.

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> I’m not sure if we can say both designs have the same trust assumptions simply because they are out-of-protocol. mev-boost only does the part of what you call here the Leader auction. Then, this design requires extra trust assumptions in, e.g., the oracle and the sidechain.

This is correct. My wording was very poor earlier my apologies.

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> This property cannot be achieved out-of-protocol. On the flip side though, seeing this as a parallel slot auction places it in the design space of (a specific instance of) diet-PEPC. It could for example be achieved using something like PEPC-Boost. This is useful because this design could maybe be composed with the previous research done on PEPC and, when launched, the data would be very useful to PEPC research, of which slot auctions are also a specific instance.

PEPC-Boost is interesting, thanks for sharing! Interestingly, since our design centers around blobs only, and blobs are independent of the rest of the Ethereum block state, we do not have the same state-conflict problem as PEPC-Boost.

---

**murat** (2024-04-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> I think it is important to see this as a parallel slot auction instead of an inclusion list because it clarifies that this proposal is not an out-of-protocol substitute for inclusion lists that improve the censorship resistance of Ethereum since if inclusion lists do not have the forward property (that proposer N constrains the block of proposer N + 1 not their own block), they rely on altruism. This property cannot be achieved out-of-protocol.

In this design the leader elected by the auction at block N constrains the block of proposer N + 1, which ends up in maximal profitability for blob preconfs for proposer N + 1, and notably, sets a minimum the proposer will make as they will receive auction proceeds right away. In this sense it is an Inclusion List for the mev-commit protocol, that acts as a de facto Inclusion List for Ethereum, achieved out of protocol. This design does not rely on altruism because actors are staked in the protocol and will suffer economic and reputational consequences if they do not adhere to the behavior they’ve opted in to.

If one of our goals is to increase the censorship resistance of Ethereum, this design achieves that even if the semantics are different. It sounds to me that this design has the forward property you mention but expands its definition to include other actors (relays, auction leader etc) to constrain the block at N + 1 rather than restricting it to the previous proposer only. The other consideration here is the preconfirmation UX, which no prior Inclusion List design addresses as far as I’ve seen. I would be curious to hear [@chrmatt](/u/chrmatt) 's thoughts on the forward property aspect

---

**chrmatt** (2024-04-02):

Thanks for the interesting discussion so far! Regarding censorship resistance of our protocol, the list of blobs that must be included by slot N+1 are determined by a provider that is (typically) not the builder or proposer of the block at slot N+1. These providers can in principle be any party, including other proposers. We thus believe that this design can improve censorship resistance. I don’t understand why the fact that the leader decides which blobs to include during slot N+1 should reduce censorship resistance since the leader is a separate entity from the builder and proposer. Maybe I misunderstood or you can clarify, [@Julian](/u/julian)? If this is an issue, it should be possible to mitigate this by a simple modification of our protocol: We can let the leader during slot N+1 decide on the blobs to include by slot N+2. The downside of this is that it delays blob inclusion by one additional slot.

I think a fair counterargument is that these providers need to actively participate in the auction to become the preconfirmation leader and therefore require some level of sophistication. They may therefore also be more susceptible to censoring than the set of proposers. Nevertheless, this design should be a step in the right direction.

---

**Julian** (2024-04-02):

Hi [@Evan-Kim2028](/u/evan-kim2028), [@murat](/u/murat) and [@chrmatt](/u/chrmatt). Thanks for the replies!

Maybe a problem in this discussion is the different terms for inclusion lists, slot auctions, PEPC, and preconfirmations, many of which are not super well-defined terms and may be interlinked. In this reply, I’ll try to stay away from these terms and use the terms in-protocol ILs for the inclusion lists that Ethereum may implement in-protocol and out-of-protocol ILs for the design that you propose here.  With in-protocol ILs, the protocol assigns the right to some party, say the IL proposer, to construct a list of transactions that constrains the builder of the slot to which the list applies, say to the slot that the Block proposer controls. Notably, it is important that the Block proposer has no control over the IL proposer since then, it may force or bribe the IL proposer to not constrain the Block proposer’s block. This is what I have been calling the “forward” property, as in current designs, the proposer of block N creates an in-protocol IL for the proposer of block N + 1. The important part is that the person who receives constraints has no power over the person constraining because otherwise, the person being constrained would not let itself be constrained. In implementing in-protocol ILs, the protocol makes an opinionated trade-off that it does not want to maximize the amount of MEV that a block can produce but wants to uphold censorship resistance. The in-protocol IL upholding censorship resistance leads to lower MEV for the Block proposer than if the in-protocol IL were empty.

This property—that the person who creates an IL is not controlled by the person who is constrained by the IL—is fundamentally impossible to get out of protocol, as far as I know. The intuition is that a proposer currently gets absolute control over their slot, and if it were to give away control, it may decide to whom, and it will never reduce the profit it can make. A rational proposer would not make the opinionated trade-off that it will not maximize MEV but will uphold censorship resistance. Therefore, it will not make an inclusion list for its own slot, if it would, it would be altruism because the proposer gives up its own profits for censorship resistance. Similarly, the proposer will not allow other parties to decrease their profits by creating an out-of-protocol IL. At best, the other parties need to pay the proposer for the right to constrain its block with censored transactions, which relies on altruism because, again, someone is giving up the maximum profitability of the opportunity to build a (part of the) block for censorship resistance. At worst, the out-of-protocol IL will not contain censored transactions as it maximizes MEV. Whatever actually ends up in the out-of-protocol IL, the mechanism does not contribute to censorship resistance because the person who is constrained by the out-of-protocol IL controls the person who creates the out-of-protocol IL.

![](https://ethresear.ch/user_avatar/ethresear.ch/murat/48/12986_2.png) murat:

> If one of our goals is to increase the censorship resistance of Ethereum, this design achieves that even if the semantics are different. It sounds to me that this design has the forward property you mention but expands its definition to include other actors (relays, auction leader etc) to constrain the block at N + 1 rather than restricting it to the previous proposer only.

In this sense, your mechanism does not expand the forward property to include other actors because the proposer of block N + 1 is still assigned full property rights over the slot, and the proposer of block N is not assigned any rights over the out-of-protocol IL by the protocol. Whether the proposer of block N + 1 then decides to sell its rights to another party is irrelevant.

![](https://ethresear.ch/user_avatar/ethresear.ch/murat/48/12986_2.png) murat:

> This design does not rely on altruism because actors are staked in the protocol and will suffer economic and reputational consequences if they do not adhere to the behavior they’ve opted in to.

Also note that this design relies on altruism in making a commitment that upholds censorship resistance instead of maximizing revenue for the proposer. I understand that, once this commitment is made, the system does not rely on altruism as there is slashing.

---

**chrmatt** (2024-04-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> This property—that the person who creates an IL is not controlled by the person who is constrained by the IL—is fundamentally impossible to get out of protocol, as far as I know. The intuition is that a proposer currently gets absolute control over their slot, and if it were to give away control, it may decide to whom, and it will never reduce the profit it can make.

Thanks for the clarifications! I think this is a crucial point. In our proposed protocol, the proposers who want to participate need to stake and agree to get slashed upfront, i.e., before knowing who will become leaders and which out-of-protocol ILs they will impose. So basically you are saying that proposers would not use our protocol. However, they will get paid from the leader auction, so it should be profitable for them to do so (and it should make sense for the leaders to pay for becoming the leader, because they get paid from those wanting to get blob preconfirmations). Of course the overall incentives are more complex, but as long as people are willing to pay for blob preconfirmations, this should be economically viable. Does that make sense?

---

**murat** (2024-04-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> the mechanism does not contribute to censorship resistance because the person who is constrained by the out-of-protocol IL controls the person who creates the out-of-protocol IL.

The person who is constrained = block builder

The person who creates out of protocol IL = relay

In this model the definition doesn’t hold, but if we say the constrained is proposer and creator is relay, it does as you point out. What’s economically different in our proposal is:

1. revenue from blob preconfirmations (net-new for relay)
2. revenue from leader auction right sale (net-new for proposer)

So perhaps the take home here is that the economical delta between these additions and the status quo needs to be positive for the proposal to be viably non-altruistic, as Christian points out. This remains to be seen, but our projections and validator talks both point to an eventuality where this is the case, hence why validators are opting in to the protocol. This may present cases where it’s not great enough, but given repeated games it’s most likely to average out in the positive.

The additional item not covered in this proposal is the mitigation of the timing game due to blob transfer times from the availability of the blob IL ahead of time, but we have not finalized the solution there yet. I would contend the economical gains as is will present a compelling story for this to be non-altruistic, but in the case of the addition of the timing game mitigation it will be undeniable. We remain optimistic for a solution for this space.

I guess the question this discussion brings up is why would rational validators opt in to the in protocol IL, as I presume it does require a node upgrade or some form of opting in through following the protocol and not forking? If the tradeoff is that it will reduce profits, it would follow in a reduction in economic security for Ethereum, which I’m not sure is a good tradeoff for soft censorship resistance.

---

**Julian** (2024-04-03):

Hi [@chrmatt](/u/chrmatt) and [@murat](/u/murat), I’m not saying proposers would not use your design. If the preconfirmations pay enough, I’m sure they will. However, the design will not be used for censorship resistance since the person who creates the out-of-protocol “IL” is the same person or commissioned by the person who is constrained by the out-of-protocol “IL,” and therefore, the person will not give up profits to achieve censorship resistance.

If you want to argue that this design leads to more censorship resistance, contention mitigation, or timing games mitigation, I would need to see further arguments to be convinced ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**chrmatt** (2024-04-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> However, the design will not be used for censorship resistance since the person who creates the out-of-protocol “IL” is the same person or commissioned by the person who is constrained by the out-of-protocol “IL,” and therefore, the person will not give up profits to achieve censorship resistance.

I don’t quite understand this argument. The person creating the IL is the one winning the leader auction. The people constrained by that IL are the builders and proposer for slot N+1. The latter do not run the auction and have no influence on who will win. The only option for them is to opt-out of our protocol. But, as argued above, they likely won’t do that if it’s profitable for them.

---

**murat** (2024-04-04):

I see what you’re saying if we consider the leader as being commissioned by the proposer (although indirectly), however they’re not being asked to give up profits but rather gaining more to achieve censorship resistance, so the design would be useful in this case. Basically our discussion converges around the fact that censorship resistance in this design relies on profits from preconfs, otherwise actors are incented to not follow / opt out.

I’d say profits from preconfs are a reasonable assumption however, and my opinion is that this is more economically viable than forcing actors to accept an IL through in protocol means purely for censorship resistance without addressing the economical downside.

