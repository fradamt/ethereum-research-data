---
source: magicians
topic_id: 6634
title: Limiting dark pools and MEV in Ethereum
author: karim
date: "2021-07-12"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/limiting-dark-pools-and-mev-in-ethereum/6634
views: 918
likes: 3
posts_count: 4
---

# Limiting dark pools and MEV in Ethereum

# Motivation

I’m thinking about ways to limit the existence of dark pools and information asymmetry between miners and the rest of the ecosystem and I would like to get your feedback on a possible future EIP that could severely hinder MEV. I consider this idea to be quite controversial because it sort of reverses some of the 1559 changes and requires more processing power from the nodes.

# Proposal

1. Let’s consider that we are already in the PoS world, there we have the process of “attestation”. At least 128 validators are required to attest to each shard block – this is known as a “committee.”
2. The committee is chosen randomly so there is little chance that they all will come from the same organization/actor.
3. Each transaction goes through two phases: First it is submitted to the public txpool, then a member of the committee will pick up that transaction, and dry-run it on the state that reflects the latest block (as if it was the only transaction in the newly simulated block). The result of this attestation is:
a. A signature of the attester, proving that they “saw” the transaction.
b. An access list of storage addresses they observed during their dry-run (EIP-2930).
c. an estimate of the gas used during the transaction execution.
d. Transactions that run out of gas will not be attested.
4. Repeat step 3 for the same transaction and accumulate N attestations that confirm the exact same outcomes from N different members of the committee for that validation time-slot. For now I’m arbitrary proposing N to be something like 3-5 attestations.
5. Only transactions that has collected enough attestations/witnesses will be eligible for inclusion in the next block.
6. On top of that, apply the idea proposed in EIP-3378 (EIP-3378: Ordered Blocks - HackMD) to randomize the order of those transactions within a block.
I believe that this direction could eliminate:

dark pools to a large extend
7. MEV sandwich, frontrunning and backrunning attacks (because you can’t insert arbitrary txs before or after that are not attested by N other nodes, and you can’t predict the order at all [because out of gas txs also don’t get attestations, and they are randomized -3378]).

To incentivise the attesting committee to spend time witnessing and attesting mempool transactions, the base fee would be in part transfered to those attesters instead of being burned. 1st attester gets 50% of the base fee, second attester 20%, third 10%, forth 10% and fifth 10%. For each given transaction.

# Request For Feedback

This proposal is early and quite rough. Constructive feedback would be very much appreciated. Have at it!

## Replies

**norswap** (2021-07-13):

I’ve been thinking a little bit about this as well.

One criticism I have seen levered against proposals for ordering the transactions is that it causes searchers to flood the network with transactions to maximize their chances to be picked (for a liquidation for instance). At first glance it looks like this proposal suffers from the same issue, or am I wrong here?

Another question I have is what the benefits of letting members of the commitee pick transactions if you are going to shuffle them anyway? One potential reason I see is that if you just shuffle (and the shuffle has enough “avalanche” that you can craft your transactions to insert them strategically – which doesn’t seem to be the case in EIP-3378?), you can still sandwich by (1) emitting very little transactions and (2) adapting your transactions until the order is what you want. You can even bypass (1) by stuffing with a lot of no-op transactions. Is that what you had in mind?

In general, I don’t think it’s a good plan to try to eliminate MEV entirely. For profitable liquidations, for instance, it’s only fair to have a bidding contest (in fact, in the long term it wouldn’t be surprising if the miners are the ones that always liquidate).

I wonder if  (1) shuffling most transactions pseudo-randomly and (2) introducing a new typed transaction for “prioritized transactions” that are not shuffled and are executed first (essentially they work like transactions do currently) is not a better idea. It prevents most sandwiches, unless it’s so damn profitable that it’s worth not including any other transactions in the block. Front-running is still possible, but not back-running. This seems fine, front-running is generally about racing for some public opportunity anyway (at least as far as I know - and I don’t pretend to know a lot, so I’d love counter-examples).

---

**karim** (2021-07-13):

> Another question I have is what the benefits of letting members of the commitee pick transactions if you are going to shuffle them anyway?

This is to eliminate dark pools and the information asymmetry between miners and the rest of the ecosystem. A transaction cannot be eligible for inclusion unless it is seen and signed by few random validator nodes.

That also prevents miners from crafting transactions and inserting them into a block without having them being seen and signed by “the public”.

---

**axic** (2021-07-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/karim/48/4265_2.png) karim:

> On top of that, apply the idea proposed in EIP-3378 (EIP-3378: Ordered Blocks - HackMD ) to randomize the order of those transactions within a block.

The number 3378 seems to be used by another pull request on the EIP repository. I would suggest not using that here to avoid confusion, perhaps you also want to submit that EIP as a pull request to secure a number for it.

