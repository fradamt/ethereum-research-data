---
source: magicians
topic_id: 3044
title: "Forming a new Ring: ETH2.0 Validator Ring"
author: jrhea
date: "2019-03-31"
category: Working Groups
tags: [consensus-layer]
url: https://ethereum-magicians.org/t/forming-a-new-ring-eth2-0-validator-ring/3044
views: 924
likes: 6
posts_count: 4
---

# Forming a new Ring: ETH2.0 Validator Ring

## Motivation

We need to think about how to encourage more stakers with consumer grade hardware/connectivity to participate by allowing them to easily form staking pools that will offset risk, make staking more accessible and provide a more decentralized network of stakers to secure the network.

Serenity needs a staking client to balance the effect of the penalties validators are subjected to for being offline.  The health of the network will require stakers.  The health of the ecosystem demands that staking be accessible.  This staking client will help ensure the success of both.

## Solution

Stakers will have to be in contact with the beacon chain in order to perform their validator duties.  The beacon chain will associate stakers to keypairs and a p2p staking pool will collectively control a **single validator’s keypair**.  Staking pool clients should be able to subscribe to a live-streamed public API of validator assignments and perform their duties automatically.  This design will allow us to select a Beacon Chain running locally or even hosted by Infura.

## Benefits

### Encourage more stakers

Individuals with commodity hardware and consumer grade internet connectivity will be exposed to less risk by using this client to participate in staking.

### Help decentralization

Excessive reliance on centralized cloud services represent an existential threat to decentralization.  This client will promote a more heterogeneous decentralized network that is performant and accessible to a much broader user base than staking in Serenity alone.

## Technical Requirements

- P2P - A central server should not be needed for clients to communicate

client discovery
- message delivery

Client Verification - There should be a robust way for each staking pool to agree on if a client meets the performance and protocol requirements. Need a verification ceremony for:

- forming a new pool
- replacing a member of a pool
- secret ballot voting

Consensus Mechanism - the pool should be able to come to agreement on its validator duties

- fast enough to avoid penalties
- scale to the target staking pool size
- pluggable*

Optional failover Infura - only perform the duties of the pool when it is unresponsive

> * Staker’s might favor different consensus mechanisms given their level of trust, network conditions, etc

## Hardware Requirements

For a full beacon node + validator:

- Processor: 64-bit Intel® or AMD® multi-core processor*
- RAM: 4 GB of RAM minimum (8 GB or more recommended)*
- Disk space: 6 GB of free disk space*
- Network: 1.2Mbps / 1.2Mbps**

> *  Min requirements for 3DStudio Max 2018
> ** Min requirements for Skype Video calling (HD)

> note: a validator should be able to run on a raspberry pi

## Infura with Ethereum Serenity

There are multiple ways that Infura could participate in the staking pools:

1. As an optional failover
2. Provide a gateway/proxy that would allow the staking pool to masquerade as a Node Operator in other staking pools such as Rocket Pool.  This would allow Infura to offer competitive pricing to clients that want to participate in Infura backed staking pools.

## FAQ

### How does this compare to Rocket Pool?

The two ideas are simpatico.  From the Rocket Pool whitepaper:

> Node operator uptime is a crucial requirement for reliable staking infrastructure. Rocket Pool requires all its node operators to stake as much ether themselves as they receive from us, so they have just as much to lose if
> they provide sub-par service or are actively malicious. Our smart contracts will also detect when a server becomes unresponsive or is misbehaving, then stop
> sending new user deposits to the node. This helps to minimise any penalties the network may incur due to server reliability.

a couple of things to point out:

1. RocketPool relies on the TrustedNode operator to have ~100% uptime; whereas, this idea is to form a private network among ‘unreliable’ nodes that, in aggregate, will be reliable.  This is advantageous bc we don’t have to struggle to find (and incentivize) trust node operators.
2. Infura could offer to join networks of ‘unreliable’ nodes for extra backup, or they could BE a trusted node for RocketPool (using the staked ETH from our customers) and collect profits from RocketPool.

### How do we combat the centralization concerns?

This staking client will be p2p and lower the barrier to entry for staking.  The end result is a more diverse group of stakers that can participate with commodity hardware/connectivity.  This gives stakers a viable alternative to AWS, Azure and GCP - which could be the defacto home of most stakers if we don’t provide another solution.

# Ethereum Serenity Background

You can skip this section if you don’t want to know the details of why Serenity penalizes validators for being offline.

## Liveness

One of Serenity’s main goals is to guarantee liveness (i.e. continue to finalize blocks) in the event of a major internet partition.  This liveness guarantee comes at a steep cost which makes it important to understand the predicament and possible tradeoffs.

## The CAP Theorem

The [CAP Theorem](https://en.wikipedia.org/wiki/CAP_theorem) for distributed systems, tells us that:

> You can’t simultaneously guarantee more than two of the following:
>
>
> Consistency: Every read receives the most recent write or an error
> Availability: Every request receives a (non-error) response – without the guarantee that it contains the most recent write
> Partition Tolerance: The system continues to operate despite an arbitrary number of messages being dropped (or delayed) by the network

## The Assumption

By viewing the argument through the lens of the **CAP Theorem**, we can deduce the rationale for the **inactivity leak** by accepting the following assumption:

> No network can guarantee message delivery because the network itself is not safe from failures (e.g. client disconnects, data center outages, connection loss).

## Partition Tolerance

Since message delivery cannot be guaranteed, the logical thing to do is to tolerate prolonged message loss.  This is equivalent to **Partition Tolerance**.

> Sidenote: Think of the World War 3 scenario as a dysphemism for prolonged message loss between groups of validators.

With **Partition Tolerance** as a hard requirement, we are now limited to tradeoffs between **Consistency** and **Availability**.

## World War 3

In the **World War 3** scenario, where the network is severed, the validators are split into two partitions. From Casper FFG, we know that in order for both partitions to continue finalizing blocks, we need two-thirds majority of validators to be online in both partitions.  This is obviously not possible; however, we can prevent the chain from stalling forever if we are willing explore a compromise between our **Availability** and **Consistency** guarantees.

## The Compromise

This is accomplished by introducing an **inactivity leak** that drains the deposit of unresponsive validators each time a slot is missed until the remaining validators in each partition become the supermajority.

At this point, blocks in both network partitions can begin to finalize; however, if the network partition is healed we are left with two valid and separate networks.

# Appendix

The following terminology and constants are taken directly from the [Serenity](https://github.com/ethereum/eth2.0-specs/blob/master/specs/beacon-chain.md) specification and represent the minimum subset required to define the staking pool.

## Terminology

**Validator** - a participant in the Casper/sharding consensus system. You can become one by depositing 32 ETH into the Casper mechanism.

**Proposer** - the validator that creates a beacon chain block

**Attester** - a validator that is part of a committee that needs to sign off on a beacon chain block while simultaneously creating a link (crosslink) to a recent shard block on a particular shard chain.

**Slot** - a period of 6 seconds, during which one proposer has the ability to create a beacon chain block and some attesters have the ability to make attestations

**Epoch** - a span of 64 slots during which all validators get exactly one chance to make an attestation

cc: [@mikerah](/u/mikerah), [@terence](/u/terence)

## Replies

**mikerah** (2019-03-31):

Great!

I do have some concerns with this proposal, namely the lack of penalties and reliance on Infura. This means that potential stakers would have to trust your client and that the client is implemented correctly. As we already know, software is hard to do correctly. Perhaps, having potential stakers take on a bit of risk might not be too bad. You also need to take into account that staking can be thought of as another form of investment with a different risk level. With this in mind, having no penalties doesn’t seem like a good idea. Moreover, it doesn’t seem to actually increase decentralization (Note that I’m taking a definition of decentralized informally presented in this article: https://media.consensys.net/scaling-series-part-1-what-is-decentralized-scaling-69cb858f954), it just makes everything more distributed. Also, the reliance on Infura adds another centralized component to this proposal.

---

**jrhea** (2019-03-31):

> With this in mind, having no penalties doesn’t seem like a good idea.

Agreed.  I’ll change it.

> Also, the reliance on Infura adds another centralized component to this proposal

The infura component is just a thought.  Like an optional failover in case your quorum of validators (acting as a single validator) lose connectivity.  Just a thought.

---

**jrhea** (2019-03-31):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/e9c0ed/48.png) mikerah:

> Moreover, it doesn’t seem to actually increase decentralization

This was my rationale:

> Excessive reliance on centralized cloud services represent an existential threat to decentralization. This client will promote a more heterogeneous decentralized network that is performant and accessible to a much broader user base than staking in Serenity alone.

In other words, the idea is to make it possible for regular people with commodity hardware to stake. Hopefully, this will balance out the centralizing force that super nodes and exchanges that stake will eventually bring.

