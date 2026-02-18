---
source: ethresearch
topic_id: 21084
title: In-Protocol Transaction Ordering
author: matthewkeil
date: "2024-11-25"
category: Proof-of-Stake > Block proposer
tags: [mev]
url: https://ethresear.ch/t/in-protocol-transaction-ordering/21084
views: 525
likes: 5
posts_count: 1
---

# In-Protocol Transaction Ordering

## Preface

This idea is an extension to the FOCIL design proposal. This was initially created concurrently/independently to FOCIL, and started as a way to funnel and order transactions with intention to fully remove the builder workflow from the protocol design. In speaking with several people it was brought to light that FOCIL was progressing, and after going through it, the timing put forth in that design was much better (required 1 less slot and used a larger committee) for transaction selection than this idea proposed.

This idea was whittled down to build on top of FOCIL instead of being a competitor as they achieved the same goal.  It’s possible that some of the idea contained here can be integrated with FOCIL but it is provided separately to facilitate targeted discussion and to not muddy the waters of that ongoing design.

Special thanks to Phil Ngo, Nico Flaig, Cayman Nava, Guillaume Ballet, Greg Markou, Gajinder, NC and many many others for taking the time to help hone this idea.

## Abstract

Where this proposal focusses is the ordering of transactions.  It also addresses rewards and penalties to coincide with the new inclusion committees and updated proposer duties.

There are two main duties, with regards to builders, of the proposal process that need to be addressed to facilitate exclusion of centralized forces through crypto economic means.

- Selection of transactions for inclusion
- Ordering of transactions

FOCIL is an excellent solution to address the heart of the first of those two topics, but it can be further refined by restricting transactions included in blocks to ONLY those on the inclusion list.  This removes economic incentives, through loss of agency, to add transactions to a block that would negatively affect ordering to capture MEV.

Ordering will become a deterministic process using the Aggregated Inclusion List, put forth via FOCIL, and an Inclusion Seed.  The Inclusion Seed is entropy generated on a slot-wise basis, specifically to prevent collusive and extractive behaviors during transaction ordering.

Because the bulk of the work during block building (inclusion and ordering of transactions in a block that is proposed on the current head) is removed from the proposer the rewards mechanisms should be updated proportionally to compensate the parties providing the value to the protocol.

## Design

There are three things that need to be accounted for to provision deterministic, non-gameable ordering. In particular ordering that is probabilistically infeasible to predict such that sandwich attacks and multi-block mev are economically disincentivized.

1. The cutoff time in which transactions can no longer be included in a block for slot N
2. The time in which the Inclusion Seed is selected for slot N
3. The verifiability of the randomization of transactions within slot N

The key to the ordering heuristic is such that the first two items happen in that order. If the seed is not known until after the window for inclusion closes, the heuristic can be built such that “mining an ordered transaction”, to be executed at a certain position in the transaction list, is infeasible.

The third item ensures that once the seed is known, any node on the network can calculate the same order of the transactions to prove compliance with the protocol. It also allows rewards and penalties to be assessed for (non)compliance.

### Timing Considerations

***Slot N-1***

t0: Proposer of slot N selects a random nonce, prepares and gossips it for use by the Inclusion Committee

t9: Cutoff for FOCIL IL committee to select IL from local mempool and gossip individual IL based on consensus head of slot N-1, IL includes the hashed nonce produced by the producer in slot N

***Slot N***

t0: Inclusion nonce, gossiped in N-1 is un-blinded and used to create Inclusion Seed. Inclusion Seed is sent to EL for use as an argument to an idempotent ordering function. An ordered list is produced that represents a full blocks worth of gas, and that list of transactions is executed. Block is produced jointly by EL/CL and CL adds un-blinded nonce to block before releasing to the network.

t4: Attesters must verify blinded/revealed nonce, inclusion seed and transaction ordering during block validity checks. Attesters vote on valid block at slot N.

### Inclusion Seed

The purpose of the Inclusion Seed is to provide the entropy to the transaction order.  It should be similar to RANDAO such that it uses on-chain data that is provable and knowable by everyone that follows the chain. However, RANDAO is too infrequently refreshed as it is epoch based and not slot based. For slot-wise ordering the entropy would also need to be slot-wise. The key to minimizing extractive behavior is that the seed needs to be selected after the window for transaction inclusion has closed in slot N-1, but prior to the end of slot N-1, so that it is available to the proposer of slot N.

When using the assumption that this proposal builds on top of FOCIL then the ideal source for entropy selection would be the aggregated Inclusion Lists which would be hard to mine against.

#### Timing-Based Seed Attack Solution

A likely attack vector to this scheme though would be waiting to be the last committee member to submit an IL which will open the opportunity to include content that affects the seed, and thus the final ordering. It would also incentivize timing games with the knock-on effect of detracting from network propagation of the un-aggregated lists.

A workaround would be to have the IL aggregation process include some additional entropy in the final list, such as the signature or a nonce.

#### Aggregator-Collusion Seed Attack Solution

Signing the list or using a simple nonce is insufficient though, as it would open attack surface for the final committee member to collude with the next proposer. For the collusion to work the collusive committee member could either have access to the next proposers key or simply coordinate with the next proposer to mine a transaction (and IL with its inclusion) for slot N.

To prevent against this attack a reveal process should be used. The first duty a proposer would do is gossip a signed hash in the slot prior to proposal.  The gossiped message would need to be announced very early, within 0-2 sec into the slot, ideally before the block is published (realistically just needs to be before the un-aggregated inclusion lists are gossiped as they need to include the nonce in the IL for validation purposes).

The announcement of the blinded nonce before gossip of the un-aggregated lists, with revealed afterwards, makes it impossible to collude in mining a transaction unless the entire inclusion committee participates in the scheme.

#### Nonce Generation and Reveal Mechanism

To ensure adequate entropy the proposer would select some random bytes, perhaps in the range of 8-32 bytes to prevent brute force guessing within the alloted time, and then mix in some stateful randomness from RANDAO.  The randomness would then be hashed to blind the true value and the hash would be signed by the proposer of slot and, but critically it would be gossiped in slot N-1 so it could be appended to the IL’s to prove that it was received prior to IL creation.

In slot N the proposer, the only participant that should know the true un-blinded value thus far, would pass the nonce to the EL to the EL can order the transactions to protocol specifications.  The un-blinded value would be appended to the block so it can be revealed to the attestors for block validation and voting.

#### Inclusion Seed Verification

The Inclusion Seed used to shuffle the transactions could then be verified by attestors by checking the hashed nonce in the Inclusion Lists matches the hash of the un-blinded nonce value included in the block once the stateful randomness (from RANDAO) was mixed in.

### Deterministic and Verifiable Ordering

The only two pieces that are needed for ordering to be both deterministic and verifiable are known inputs and and a well-known, idempotent ordering function such that:

Torderd, Tremaining = f(ILagg, IS)

where:

ILagg - Aggregated Inclusion List

IS - Inclusion Seed

Tordered - Ordered list of transactions

Tremaining - Left-Over transactions that roll over to next block

### Ordering Algorithm

Ordering could be easily achieved by multiplying the transaction hash by the Inclusion Seed, letting values that overflow wrap around, and then putting the transactions in numeric order. This is overly simplistic and may not provide resistance to mining transactions that could game the system.

Another option is ordering the transactions in the Aggregated Inclusion List numerically, by hash, and then running an algorithm similar to swap-or-not over the set utilizing the Inclusion Seed instead of RANDAO. This may be more cpu intensive, but for a small set (1000± transactions) it should be relatively performant.

The sender address can alternately be used instead of the transaction hash as the root value that gets ordered but preference currently is to the transaction hash.

### Ordering Heuristic

There are some user considerations that need to be addressed when implementing deterministic, non-gameable ordering. There is a balance that needs to be achieved between the crypto economic incentives of priority fees and rigor for prevention of sandwich attacks and monitoring the mempool for value extraction through transaction copies.

#### Pseudo-Random Ordering

Everyone will have the same fair shot at the order within a block.  While the most egalitarian solution this ignores the crypto economics of paying a higher priority fee.  The most important instance where ignoring this makes sense is for reducing the potential for someone to monitor the transaction pool, for transactions that are profitable to front-run.  The illegitimate actor can simply submit a transaction that with a higher priority fee.

Randomized ordering takes away much of the economic incentive to copy transactions but does not address undesirable spamming of several conditional-execution transactions to increase probability of being executed ahead of the legitimate actor.

#### Priority-Fee Aware Pseudo-Random Ordering

To address the spamming of conditional-execution transactions to try to ensure one randomly executes first, a heuristic that crafts tranches of transactions, bundled by fees, such that higher fees go towards the beginning of the block could be used. For transactions with relatively high priority fee (likely profitable arbitrage) it would be very expensive to match the fee for a large number of transactions. Keeping pseudo-randomness within the tranches will make that gamble, or single transaction out bidding expensive and without guarantee of success. It would also be possible to craft the tranches dynamically so that if there are transactions, with fees that are outliers, the bounds of the tranches can be structured to promote fairer execution.

```txt
As an example for a given block, the transaction priority fees in gwei:
`[ 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 4, 100 ]`

The tranches could be crafted like:
`[ 1, 1, 1, 1, 1, 1, 1, 1, 1 ]`
`[ 2, 2, 2, 2, 2, 2, 2 ]`
`[ 4, 100 ]`
```

#### Priority-Fee Based Ordering (Non-Pseudo-Random)

Once encrypted mem-pools are fully implemented it would be possible to move to a fully priority-fee based ordering heuristic. This would be the ideal situation that solely relies on market dynamics to set pricing for execution order.

### Rewards and Penalties

In this paradigm, the searchers adding transactions to the Inclusion Lists are the ones that would receive a bulk of the reward.  The block proposer would now be strictly following the protocol and have reduced agency. With the reduction of duty a majority of the proposal rewards should get shifted to searchers to avoid inflation. This will also have the added benefit of smoothing rewards from a single proposer to the whole IL committee. It could be argued that the proposer generating and gossiping the Inclusion Nonce at N-1 is now a critical point of failure though because the proposal process would hinge upon them.  Thus the block reward that is earned in slot N should be requisite of the nonce gossip at slot N-1.

The rewards mechanism of FOCIL would also need to be extended to accommodate the moving of partial block rewards to the searchers for including novel transactions.  This idea is referenced by the FOCIL team but is not finalized yet and thus needs to be updated here once that proposal progresses.

Because the IL Committee now hold the critical piece to transaction selection the task is now of high importance. Thusly, equivocation by a committee member should be slashable similar to creating conflicting attestations or blocks.

### Left-Over Transactions

The implication of having multiple un-aggregated inclusion lists and all transactions for a block being sourced through combining them into a single list is the potential for more transactions being submitted than can fit into a single block. This means that the Inclusion Pool (transactions submitted by IL committee members) might need to be inserted into the subsequent block. How this happens is still an area of research but some suggestions proposed so far are:

- Do not guarantee IL transactions MUST be included. More like Inclusion Suggestions Lists and a heuristic will be used to include transactions in the block that is reproducible. All transactions that are not included may be added to subsequent block lists
- Limiting IL size to prevent overflow
- Adding a time weighting such that transactions that have waited for inclusion get higher precedence in the next block. This could be added to the priority fee for instance.  If a large collection of high fee transactions are submitted which prevent inclusion the time weighting could be increased for subsequent blocks to help push the transaction through eventually
- Setting a threshold for sequencing.  If the transaction has a very low priority fee, and does not make it into several blocks it gets removed from the overflow

Of the suggestions the first is easiest, and most pragmatic to implement. The only thing that would be needed is to develop the heuristic for block inclusion for transactions on a list.

## Interactions with Other EIP’s and Existing Roadmap

### Account Abstractions

It would be possible to have the EL’s include AA generated transactions to the IL when a list is generated. There are some nuances to fees for prioritization with this though.

### ePBS

This proposal would remove the need for ePBS and the complexity that it adds to the protocol

### Proposer-Attester Separation

The chance for Execution Tickets, and other slot auction style proposals, to create further vertical integration by the builders is a real concern. If ordering was done in protocol it reduces this risk substantially. This would be a boon to all suggestions that separate the proposer duty from attester duties which would greatly increase the successful implementation of protocol developments that allow for very light attestation-only clients

## Discussion

### Protocol Simplification

The more complex systems become, the more difficult game theory is when planning and implementing protocols within the system. I argue that building widgets on top of widgets to solve problems creates more attacks surface within the system the widgets are designed to protect. In the case of building protocols to inhibit MEV/builders/relays without doing away with builder flow creates more nooks for exploitation to live in. We must address the existing system design and attack the root cause, selection and ordering of transactions without the help of “out of protocol” opaque solutions.

### Preserving Cypherpunk and Egalitarian Principles in the Protocol

Make Ethereum Cypherpunk Again. This is a call to action on our pilgrimage to MECA. To preserve the ethos that brought us all here.  Builders and the ecosystem that has built up around them must not be allowed to usurp L1. Allowing actors to extract value from honest participants is not only antithetical to the ideals of blockchain but it dissuades adoption by traditional industries. Blockchain brings Rule of Law to the digital space. The idea that single participant is above the protocol. Restoring and preserving that will entice experimentation with blockchain as the root of trust for inter-system interactions.

### Layered Settlement

The traditional financial system is built upon layers of infrastructure. It is important to highlight this because there may be significant push-back to the trade-offs this proposal introduces. Settlement time will potentially increase for some participants. Some transactions may fail because builders provide some level of transaction coordination (at the expense of the MEV). Transaction fees might go up.  L1 is not, and should not be designed for instantaneous settlement.  Consensus takes time and the tradeoff for that speed is decentralization and the security it imbues.  Builders will be upset and if incentives are tuned correctly because value extraction will be converted into priority fees. Transaction volume will move to L2.  But these are healthy things for an L2 centric scaling roadmap.

Being able to facilitate liquidity pool price discovery, ie very large buys/sells between LPs, across L2s and other application chains like the Uniswap rollup will benefit from surety of price discovery and honest auctions.  The trade off is small transactions will be too expensive to run on L1. This is similar to how our existing financial system works today.  Shares are held by DTCC on behalf of brokers for the benefit of the broker’s clients.  It is costly and difficult for individuals to transact small positions because order books at that level are for very very large quantities.  Brokers facilitate this by providing localized liquidity and pay for the service through transaction sequencing (and in some instances sandwich trades).  The end consumers, however, get to create trades for no fee (other than the slippage that is introduced by the broker).

The bottom line is consensus takes time and the trade-off between decentralization and throughput is real. For the benefit of the protocol over the long term, preserving the decentralization at all costs is the secret sauce of what will preserve Ethereum far into the future.
