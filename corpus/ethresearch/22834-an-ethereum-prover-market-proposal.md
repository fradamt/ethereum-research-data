---
source: ethresearch
topic_id: 22834
title: An Ethereum Prover Market Proposal
author: Julian
date: "2025-07-29"
category: Economics
tags: []
url: https://ethresear.ch/t/an-ethereum-prover-market-proposal/22834
views: 1197
likes: 18
posts_count: 9
---

# An Ethereum Prover Market Proposal

*Thanks to Kev, Maryam, Mike, Thomas Thiery, Thomas Coratger, Maria, Caspar, Ladislaus, Marios, George, Mary, and Dmitry for feedback and discussions that led to this post (feedback ≠ endorsement).*

When Ethereum implements a [zkEVM on the L1](https://blog.ethereum.org/2025/07/10/realtime-proving), it will be necessary to source proofs for blocks. This post proposes to implement a prover market on Ethereum: It allows builders to connect with a permissionless set of provers. Builders, with help from the Ethereum protocol, deposit a prize for proofs into a system contract while building the block. Anyone who submits a proof may collect a part of the prize in the next slot. Attesters enforce that payments are delivered.

This proposal solves the fair-exchange problem between builders and provers. The fair-exchange problem implies that builders only pay for proofs if proofs are delivered, and provers only proof if they can claim a prize. Moreover, this proposal removes the need for a relay to handle the potentially large amount of communication, sometimes called [safe multiplexing](https://collective.flashbots.net/t/tee-boost/3741), between a builder and provers. That is immediately one of the largest advantages of this proposal: there is no need for trusted, third-party relays. Instead, the Ethereum protocol manages the fair-exchange problem and the builder prover communication.

In this post we propose a prover market, however, Ethereum may not need a prover market if either:

1. There is at least one altruistic prover online at all times for all proving systems.
2. Builders are provers.

Whether the first assumption holds depends on the costs of proving. How high proving costs in the short- and long-term will be is still unclear. Justin [suggests](https://docs.google.com/presentation/d/1vDkFlUXJ6S94hOGjMkeIO-SP3ZB4ysKPNgu1mskf1No/edit?usp=sharing) long-term capital expenditures to be around 100,000 USD and the long-term operational expenditures  to be capped at what it costs to obtain 10kW power throughput. However, Dankrad [suggests](https://ethereum-magicians.org/t/relaxing-the-prover-hardware-requirements-for-the-next-few-years/24346/14) that in the short-term it may be acceptable if costs are higher. Costs should be quite low for Ethereum to rely on the first assumption, such that there will be many provers at all times.

Even if the top builders prove blocks themselves, in my opinion, it is still desirable to have an in-protocol prover market, because it decreases Ethereum’s dependence on builders. If the top builders go offline, local block builders may still connect to provers via a prover market. Moreover, access to a prover market decreases the barriers to entry of the builder market.

## Proposal: Ethereum Prover Market

- Block n:

The builder of slot n builds a block and measures the amount of prover gas used in the block, we call this amount g. Prover gas is a measure of how difficult a block is to prove due to the combination and types of transactions in the block.
- The protocol provides an indication of the market price, p, per unit of prover gas. For this post, we assume the protocol knows the market price.
- The builder deposits k separate prizes of size x_i = g * p_i * n_i into a system contract which provers may claim in the next slot if they provide a proof. k refers to the number of proofs from different proof systems necessary for a block to be considered valid (k may be 3), p_i is the market price per unit of prover gas for proving system i and n_i is the number of proofs targeted for proving system i.
- The builder propagates its block.

Slot `n`:

- Provers create proofs and include a recipient_address in their proof.
- Proofs must be submitted to the global topic before some proof deadline, say t = 9, as described in the Prover Killers Killer post.

Block `n+1`:

- The builder of slot n+1 is forced to reference all proofs available before the observation deadline. Additionally, the builder includes all recipient_address fields from these proofs in the system contract where the prize is deposited. Attesters enforce completeness.
- The prizes x_i are split equally among all provers for a particular proving system and their portions are sent to their recipient_address.

## Prize System Contract

The system contract must have two important functions to

1. Deposit prizes: Builders must be able to deposit prizes into the system contract. The contract should hold the prizes until the next block.
2. Pay out the prize: The contract should take as input a list of recipient_address values and pay out the prize in equal portions to each recipient_address. The size of the list could be larger than k if more proofs are delivered than strictly necessary. In that case all provers (more than k) receive an equal portion of the prize of their proving system.

If no proof is delivered, the prize should either be returned to the builder or burnt, depending on who exactly provides the prize money. More on this in the next section.

## The Prize

The prize needs to be set such that there is a very low probability that too few proofs are delivered. This section discusses:

1. How to set the prize.
2. Who pays for the prize.
3. What happens if too few proofs are delivered.

***How to set the prize.***

[Maryam](https://x.com/bahrani_maryam?s=21) and [Mike](https://x.com/mikeneuder?s=21) analyze how to set the prize optimally in [this post](https://ethresear.ch/t/on-incentivizing-anonymous-participation/22469#fn7). They find that if the protocol knows the proving costs, the proving costs are identical for every prover, and the welfare loss from a missed slot is known, there is an optimal prize to set that is independent of the number of potential provers in the asymptote.

[Ignacio](https://x.com/ignaciohagopian?s=21) and [Kev](https://x.com/kevaundray?s=21) are leading the work to benchmark how expensive to prove certain (combinations of) opcodes are relative to each other. These efforts allow us to assign “prover gas” to each opcode. The sum of prover gas in a block would then be `g` as mentioned in the proposal above.

Then, the protocol needs to know what the prevailing market price is per unit of prover gas. There is a large design space here that should be explored. We could take inspiration from EIP-1559 and target a certain number of proofs that is larger than the minimum necessary. If the number of proofs is higher than the target, the prover gas price decreases. If the number of proofs is lower than the target, the prover gas price increases. The protocol must be careful though: too few proofs lead to costly missed slots.

Ethereum will likely require proofs from `k` different proving systems. It could be that proving for one system may be significantly cheaper than for another. To target a certain number of proofs per proving system, it is needed to create a separate prize for each proving system.

Moreover, we need to know the welfare loss from a missed slot. Although potentially a good proxy, as suggested by Maryam [here](https://www.youtube.com/live/HnuYme5f8ho?si=1o_UWr7LKqUr6j2J), the MEV-Boost auction bid is not available to the protocol, hence it cannot be used. Previous discussions on missed slot penalties, like [this temperature check](https://ethresear.ch/t/missed-slot-penalties-temperature-check/18713) from [Max Resnick](https://x.com/maxresnick1?s=21), suggest a missed slot penalty of the `gas_target * base_fee`.  More research is needed to understand what penalty level ensures proposers are never incentivized to exclude proofs to capture more MEV.

***Who pays for the prize.***

Either the builder must pay for the prize entirely, or users must pay for the costs of proving their transactions and the prize is the sum of all transactions.

The simplest way to implement this is to not define who pays for the proofs, in which case it may be expected that the builder is the only entity that deposits a prize into the system contract. Presumably, the prize costs less than the MEV profits the builder makes from the block. A disadvantage of such a system is that the builder may put up a low prize if the costs of missing a slot for a builder are lower than for the network.

Alternatively, user transactions may be charged the market price for the prover gas they consume and these revenues may be put as the prize. An advantage of this system is that builders are immediately incentivized to use the Ethereum Prover Market because it does not cost them anything. If the builder is responsible for setting the prize, they may find it cheaper to make service-level agreements with provers out-of-protocol. If the Ethereum Prover Market is the main way proofs are sourced, it gives Ethereum more control over parameters like the probability of a missed slot and decreases barriers to entry for both builders and provers.

In either scenario, end-users eventually pay (part of) the price for proving. In the second proposal, users do so directly. In the first proposal, users do so indirectly through MEV, however, it could be builders also pay for a part of it. Importantly, the set of users carrying the heaviest burden of prover costs may be MEV searchers and traders in the first proposal.

***What happens if too few proofs are delivered.***

If too few proofs are delivered, the block does not become canonical. However, it could be that there are more than `0` but fewer than `k` proofs delivered. In that case, it may be ideal that the prize is payed out to the provers that did deliver a proof. If the builder is expected to pay for the proof, that would lead to a loss for the builder. If no proofs are delivered, the prize should be returned to the builder if the builder deposits the prize and returned to the users otherwise.

Note that returning the prize may be trivial in the case there are no proofs since the block does not become canonical and transactions aren’t processed. However, that also complicates the case in which there are more than `0` but fewer than `k` proofs. If it turns out to be costly to implement, the prize may also be returned in that case.

## Proof Recipient Address

The proofs need to include a `recipient_address` field in order to receive a portion of the prize. The proofs should satisfy the following two propeties:

1. Proofs should include the recipient_address in the context, metadata that does not describe the proof but the usage of the proof. If the context is changed it turns the proof invalid. That is, proofs should be non-malleable.
2. A prover should not be able to produce multiple proofs with different recipient_address fields at the cost of a single proof.

FRI-based proving systems are the most used ones for zkEVMs today and satisfy these two properties.

## Attester Enforcement

Attesters freeze their view of available proofs at the observation deadline. They make a `recipient_address` list from all proofs that they have observed. The proposer freezes its view later than the attesters and must include a list of all `recipient_address` fields it has seen in the beacon block. If an attester’s view of the `recipient_address` list contains values that are not contained in the beacon block, the attester does not vote for the block.

This system is based on [view-merge](https://ethresear.ch/t/view-merge-as-a-replacement-for-proposer-boost/13739), as described by [Francesco](https://x.com/fradamt?s=21), which is already used for the [same-slot proving architecture](https://ethresear.ch/t/prover-killers-killer-you-build-it-you-prove-it/22308) this proposal relies on. The added complexity here includes communication between the consensus and execution layer to use the `recipient_address` list from the beacon block in a system contract.

## Why the Ethereum Prover Market is simpler than PBS

Proposer-Builder Separation (PBS) has been discussed for years in the Ethereum community, yet there is no rough consensus on a satisfactory market implementation. There [have been concerns](https://ethresear.ch/t/relays-in-a-post-epbs-world/16278) about relays existing even with a version of enshrined PBS (ePBS). The current ePBS proposal, [EIP-7732](https://eips.ethereum.org/EIPS/eip-7732), deals with [some of these concerns cleverly](https://hackmd.io/@potuz/HyhN0Nt9A), yet builders and relays expect relays to continue operating even if 7732 were implemented.

However, I do not expect an Ethereum Prover Market to be as complicated as PBS for the following major reasons:

**Proofs are out of the critical path.** Because of some form of delayed execution, either through [EIP-7732](https://eips.ethereum.org/EIPS/eip-7732) or [EIP-7886](https://eips.ethereum.org/EIPS/eip-7886), proofs can be submitted in the next slot, instead of before the block is committed to. That has two important advantages for a prover market.

First, it means that the payment for proofs can happen in the next slot. There does not have to be a deal between the builder or the protocol and a prover before the block is committed to. In PBS, the proposer must make a deal with a builder in the critical path, which means Ethereum cannot be used as the trusted third-party that solves the fair-exchange problem and relays are necessary.

Secondly, it means that propagation speed is not an important determinant of whether a proof is on time. In MEV-Boost, relays heavily optimize propagation to play [timing games](https://arxiv.org/abs/2305.09032). If provers can prove blocks in real-time, perhaps such tiny latency races are not meaningful enough to become a vector of competition.

[**The cash flows are reversed](https://www.youtube.com/watch?v=HnuYme5f8ho&t=1203s).** In MEV-Boost, the builder pays the proposer for the right to propose a block. In the Ethereum Prover Market, potentially, the protocol uses transaction fees to pay provers to create a proof. If user transaction fees (not the builder) pays the provers, the market simplifies because it is immediately incentive compatible for the builder to participate, since it does not have to pay anything. If the builder does not offer external rewards, provers must also participate in the Ethereum Prover Market.

**No Unbundling.** Blocks in MEV-Boost need to be signed by the proposer before the proposer sees the block’s contents to prevent the proposer from stealing the MEV from the block. Unbundling is not a concern in the prover market. First, builders commit to their block and propagate it publicly before proofs are delivered, without risking MEV stealing. Secondly, provers can send proofs publicly before receiving funds because their payments are attester enforced and their proofs cannot be easily modified to hold a different `recipient_address` (proofs are non-malleable). Since there is no unbundling risk, both blocks and proofs can be propagated publicly without the need for a relay.

## Disadvantages of this Proposal

- Wastefulness. Potentially more proofs than strictly necessary should be gossiped on the network, which either increases bandwidth requirements for proof propagation or the necessary time allocated to proof propagation, which decreases proving time.
- Potential Missed Slots. If the prize is set too low, it could be that few provers are incentivized to prove causing missed slots. Ensuring that the prize is sufficiently high is therefore extremely important.

## Advantages of this Proposal

- Prover Liveness. This proposal creates an incentive for provers to create proofs, regardless of who the builder is.
- No relays. This proposal solves the fair-exchange problem and prover builder communication without the need for trusted third-party relays.
- Permissionless. All provers can receive prizes for proofs.
- 0-Stake-Provers and No Shirking. Provers do not need to deposit stake to cover potential penalties from being inactive because the system does not rely on a specific prover to provide a proof. From that, it follows that there is no risk a prover promises to deliver but shirks.
- No Randomness Required. The prize is paid out in equal portions to all provers instead of one randomly selected provers. This does not affect the prover’s decision on whether to prove, yet it removes the need for a good random oracle, as Maryam argues here.
- Ethereum Controlled. Ethereum can control the parameters of the market, such as the probability of too few proofs arising. There is no dependency on external governance.

## Alternative Proposal: Auction-based Prover Market

*This section was added later on the 25th of August based on the discussion in the comments below from [@jbaylina](/u/jbaylina) and private discussions.*

The above proposal depends on the assumption that proving costs are non-amortizable: creating a second proof with a different public input is as costly as creating the first proof. [@jbaylina](/u/jbaylina) points out that this assumption may not hold in general and private conversations suggest it is hard to ascertain what fraction of the proof is amortizable.

Here we propose a different prover market that does not depend on the non-amortizable property. It works as follows:

1. Provers specify their proving costs per unit of gas, total gas units they can prove, the amount of ETH they stake, and the minimum total fee they accept as the tuple (cost_per_gas, max_gas, stake, min_fee). Bids are recorded in a smart or system contract on-chain.
2. The block builder of slot n can pick a prover from those that specified bids in the smart contract as long as the gas_used is lower than the max_gas the prover can prove. The builder selects a prover by including a transaction in its block that calls the smart contract.
3. As soon as the block is propagated it is clear which prover is selected. The prover now must start proving the block before the proof deadline. If successful, the proof is included in the next block (for details see Prover Killers Killer design)
4. If the proof was included, the prover is paid max(min_fee, gas_used * cost_per_gas). If the proof was not included, the prover’s stake is transferred to the builder.

This mechanism selects one prover which removes the reliance on the non-amortizable assumption. The downside, however, is that the prover may not deliver the proof. The stake is there to incentivize the prover to deliver the proof and to compensate the builder for potential losses.

Since prover costs do not vary much within a short timespan, bids can be recorded and stored on-chain for some period of time. Bids in this sense are more like posted prices than bids we may see in the builder market which vary significantly during one slot. The proposer of slot `n` may pick a prover and the proposer of slot `n+1`, and slot `n+2`, etc, may choose provers from the same list of bids. This prevents the need for a relay.

Details like making the stake dependent on the amount of gas used could be implemented as well to make the market more suitable to specific arrangements.

In summary, this proposal removes the non-amortizable assumption but introduces shirking risk, which necessitates provers to have stake. The advantage of this proposal is that it is fully implementable via smart contracts and does not require consensus layer changes to Ethereum. Moreover, there is no need for trusted intermediaries like relays.

## Replies

**bout3fiddy** (2025-07-29):

Interesting proposal. The ‘builder-pays’ model seems like a much more sustainable path forward than involving protocol-level issuance, which seems to have a growing voice within the community too.

I’m trying to get a sense of how much a prover will charge per proof. My understanding is that the highest costs will be OpEx, and this is quite arbitrary here.

Assuming 12-second slots, and some inspiration on target specs taken from the Realtime-Proving blog post by the EF published recently by Sophia Gold on the 10th of July 2025, the costs are split as:

1. CapEx: I expect a cost of ~$0.011 per proof, based on a $100k rig with a 3-year lifespan.
2. Energy costs: ~$0.008 per proof, based on a 10kW rig running at a high energy cost of $0.30/kWh.
3. OpEx: Prover teams need a budget of approximately $2.0 million per year. Assuming 12 second slots, and ~3.15 million proofs per year, that comes down to ~$0.70 per proof.
4. Assuming a prover wins 10% of the times it generates proof, or it gets paid out for 1 proof per 10 proof it generates, a prover will probably charge 10x a proof’s cost.
5. I add a 25% profit margin because why not.

These very hand-wavey assumptions come down to $9.00 per proof that a builder has to pay, with most of the costs coming from OpEx (2 ZK cryptographers, 4 engineers, 1 operations) for a lean team.

Does this number ($9.00 per proof paid from builder to prover) make sense to you? Is it realistic?

---

**Julian** (2025-07-30):

Hi bout3fiddy, thanks for your response!

First, to clarify, I do not propose to use protocol-level issuance. Instead, I propose either the builder pays for it or users do so with transaction fees.

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> Either the builder must pay for the prize entirely, or users must pay for the costs of proving their transactions and the prize is the sum of all transactions.

Your analysis on prover costs mostly makes sense to me. The OpEx, however, may be lower depending on what types of provers we want to attract. The CapEx and Energy costs were set such that proving could be done from a home or an office which doesn’t seem to match the need for a team of cryptographers and engineers. Potentially we may see two different types of provers:

1. Home provers where the CapEx and Energy costs dominate.
2. Sophisticated provers who really want to squeeze out more performance to create bigger blocks where OpEx costs in terms of salaries dominate.

It is very interesting to continue work on this and perhaps looking at the types of provers that exist today is a good starting point.

---

**bout3fiddy** (2025-07-31):

> It is very interesting to continue work on this and perhaps looking at the types of provers that exist today is a good starting point.

I’ve created a Google sheet for doing these kinds of economic modelling: docs.google . com/spreadsheets/d/1SnwLecBwThcC2OScNie7TjZhvYzqwPIWo5rNddFrd9w

I hope you find it useful.

Question in addition here is: We expect that proofs are generated by builders themselves as they’d probably want to ensure nobody frontruns them, generates a proof for their payload and pawns it off as their own (can we say this is one way to describe proof stealing?). Do you then expect the same centralisation forces in play here that have emerged in the mev-sphere?

---

**Julian** (2025-07-31):

Cool!

Builders may be provers but I see fairly small synergies between the two roles. Builders do not have to worry about payloads or proofs being stolen.

1. Payloads cannot be stolen because they are committed to on-chain and no one else has the right to propose them.
2. Proofs cannot be stolen because proving systems satisfy the non-malleability property which means proofs cannot be unbundled basically.

Builders want to ensure there is at least a proof so if they are unconvinced of that perhaps they become provers themselves. Moreover, potentially if they build such big blocks such that communication time between sending a block and the prover receiving it becomes a problem they may build themselves.

There are few natural synergies as I understand it since builders do not rely on the hardware used for proving for other strategies.

---

**jbaylina** (2025-08-01):

For reference: [Distributed Proof Generation](https://ethresear.ch/t/distributed-proof-generation/22801)

Some points that are not clear to me:

1.

In general, when you are building a proof, you can reuse a huge percentage of the work to compute the proof, to generate a different proof with a different prover address. So, an obvious attack is to generate many proofs faking many provers, but reusing the work of generating one single proof.

1.

How the price is calculated and adjusted? This price needs to be calculated/commited before hand, but may variate.

1.

Generally speaking, for me, the bigest concern of a proving market is the danger that there is a single prover that ends up building all the proofs and geting all the fees, because it hase the more competitive advantage, and give no margin to the second one (the backup), that gets no fees, but need to maintain an infrastructure.  This model can bring important outages in caise of main prover failure, because backaps are not economically worthy, so they just not exist.

---

**asn** (2025-08-07):

> In general, when you are building a proof, you can reuse a huge percentage of the work to compute the proof, to generate a different proof with a different prover address. So, an obvious attack is to generate many proofs faking many provers, but reusing the work of generating one single proof.

Yep! That’s certainly the case for most proof systems, and [proving the opposite](https://eprint.iacr.org/2020/190) (i.e. amortization resistance) is an extremely challenging task.

Given that most proof systems out there are likely not [\epsilon-amortization resistant](https://eprint.iacr.org/2020/190) (for a tiny \epsilon), but they are likely also not super-super amortizable (e.g. can’t push out three proofs for the work of one), it’s worth thinking if there are plausible designs for this intermediate world:

1. Can you design an efficient proof system assuming a very amortizable proof system (e.g. can produce two proofs in the work it takes to produce one)? The problem is that all parties will be submitting superfluous proofs due to the amortization. Since everyone can amortize, the problem in this case might not be that some parties will get higher rewards than others, but it does cause lots of redundant P2P traffic and other logistics. How does this redundancy hurt us? How amortizable does a proof system need to be before the redundancy becomes a big problem? Is there a good prover market that can be created out of such a proof system?
2. In a similar vein to the above, let’s say we go through the motions and prove that our proof system is max 20% amortizable (i.e. Alice is able to produce max 1.2 proofs in the time it takes to produce 1). Is there a good prover market that can be created out of this?

If the answer to the above two questions is “no”, then it’s likely we will only ever be happy with \epsilon-amortization resistance which is a result that is both very hard to get and also very hard to maintain (as proof systems in our prover market get added, removed, and change over time).

---

**asn** (2025-08-12):

Thinking a bit about how an L1 prover market could accomodate amortizable proof systems. In such a setting, we expect to see more proofs than normal, and we would need to handle and reward them all appropriately. A good thing we have for us is that the proposer only needs a single valid proof to create a block.

So perhaps we can split the protocol in two phases. Here is a strawman proposal, assuming we have a  mempool of proofs that contains a bunch of amortizable proofs for slot n:

- In the block production phase, proposer picks her favorite proof and creates a valid block. Chain continues, people are happy.
- We then have a longer “aggregation” phase, where  k aggregators are tasked with collecting all amortizable proofs of slot n and creating a recursive superproof that they eventually post on chain to collect rewards based on the amount of proofs they aggregated. The provers of slot n also get rewarded appropriately at that point. This phase can last for an epoch or so, to give enough time to aggregators to do their job.

This proposal certainly has flaws (aggregators could grief provers, staggering rewards like this is not elegant, P2P redundancy is not alleviated etc.) but I just meant to provide a design that could potentially work around amortizable proofs.

---

**Julian** (2025-08-25):

Hi [@jbaylina](/u/jbaylina) , I still wanted to thank you for your comments! I adjusted the post above with a different proposal that does not rely on the assumption that proofs are non-amortizable.

To your second point, there is a large design space to set good prices for proofs. An EIP-1559 style market is possible but tricky to get right to prevent missed slots. More experimental options include mechanisms similar to [Aleo’s Coinbase Puzzles](https://developer.aleo.org/concepts/network/provers/#goals-of-the-puzzle) where Ethereum would create small puzzles every so often to get a price signal and price proof requests based on that. However, I think we should first decide whether we want to go down the route of an enshrined prover market before committing to specific price mechanisms.

Finally, I agree it is very important to prevent liveness failures do to provers. Ensuring there are multiple provers participating at all times is one way to do so, but it would likely have to be done via a market mechanism that does not always allocate proving rights to the cheapest prover as then there may only be one as you describe. However, such mechanisms are usually more expensive, which may mean they would have to be forced in-protocol to ensure the mechanism is used. Markets are just one way of supporting liveness though. Perhaps liveness concerns can also be decreased by creating software that allows people to spin up remote provers in many different uncorrelated places or by ensuring sufficiently many decentralized nodes have basic prover hardware.

