---
source: magicians
topic_id: 3532
title: Resource constrained client incentivization
author: ligi
date: "2019-08-06"
category: Magicians > Primordial Soup
tags: [light-client]
url: https://ethereum-magicians.org/t/resource-constrained-client-incentivization/3532
views: 913
likes: 4
posts_count: 5
---

# Resource constrained client incentivization

Really worth a read for everyone working in this area:

https://in3.readthedocs.io/en/develop/incentivization.html

Would love to hear what others in the Constrained Resource Client Ring think about it.

## Replies

**shazow** (2019-08-06):

Some questions I have about in3’s architecture: (cc [@CJentzsch](/u/cjentzsch))

## Discovery

Participating full nodes are registered on-chain in a smart contract. When light nodes want to connect, how does the initial discovery happen, if you need chain state to get to the chain? Are we relying on a centralized point of failure here, and what are the attack vectors?

## Identity

There is a reputation-based system for colouring full nodes as good vs bad. As a light node, what kind of guarantee do you get from eclipse attacks? Is it just a matter of a full node spamming the registry smart contract with a bunch of slots (sybil attack) with some minimum deposit, to get a fairly decent probability that the target light nodes will connect to its subset of evil nodes?

## Payment

This is a big challenge I ran into with Vipnode as an economic incentive:

1. Is it profitable? Are there any models for the scale of payments that we’re aiming for and if they’re realistic? (Anecdotally, looking at the vipnode pool I’ve been running this past year, I don’t believe it’s anywhere near profitable to run a full node in the current ecosystem. This will likely change as there’s an influx of new users or maybe as staking becomes a thing.)
2. How do we disburse many-to-many micropayments efficiently? If you’re running a full node with a paid incentive, and you have a balance of say 20 cents each across 50 clients. How do you get your $10 without burning most of it in transaction fees?

---

**CJentzsch** (2019-08-13):

Good questions, here our current answers:

1. Discovery:
Here we do the same as most Ethereum clients. There are hard coded boot nodes, but you can also point  to your own over the CLI. Through that boot nodes (or those boot nodes) you can then retrieve the current list from the registry contract itself.
2. Identity:
Spamming is prevented by paying a deposit. Naturally, I would sort nodes according to the total amount of deposit. So spamming becomes very expensive. If you find some node not responding, you locally black list this node. Also, math is on our side here. Since you can get the validation of several nodes simultaneously, you need to have a very high percentage of nodes in order to cheat, since all of the nodes I am asking need to give the same response. So if I for example configure my client to get 5 validations. This means he chooses 5 nodes, most likely from those with higher deposits, and they all need to give the same signed blockhash. If I hit one honest node (and I could even set one node to be my own), then I could convict all the dishonest nodes.
Here our analysis about that: https://in3.readthedocs.io/en/develop/Threat-Model-for-Incubed.html#risc-calculation
3. Payment
We are currently experimenting with different state channel implementation. We are also looking at probabilistic micro payments. But this is not completed yet, so I will give more information once we are done with that.
As for profitability, it is an issue. But just as Infura how much they pay for their servers. They already started their paid subscriptions, so there is a real cost, which needs to be covered. The Ethereum community just has been spoiled with free Infura, I think we will have to get used to actually pay for what we use.

I hope this helps.

---

**egalano** (2019-08-15):

Thanks [@CJentzsch](/u/cjentzsch). I’ve been following Incubed since the beginning and I think it shows a lot of promise as a way for infrastructure providers to provide a service and accept payments in a decentralized manner. Thanks for all your work on it.

For identity and node reputation tracking, one thing we’ve seen is that nodes may return incorrect responses not out of malice but because they are occasionally lagging behind other nodes on the network maybe because of server performance profile, network issues, etc. Would these nodes be penalized the same as malicious nodes? What does the economic model for this look like? It might not be worth the risk to stake if the penalty for occasionally lagging is too high.

---

**dominic** (2019-08-18):

For [diode.io](http://diode.io) we have been following a somewhat different approach. Instead of making the constrained clients a feature supported by additional special server, we merge it into the core node functionality. This creates a couple of simplifications:

1. Discovery
Each blockchain node is a constrained client protocol serving node. By fetching blocks / knowing recent blocks the IoT devices also know the originating mining nodes. This requires a block header change to have miner a) sign each block cryptographically and b) leave some kind of address in it (e.g. ip address). The details are described in the BlockQuick paper https://eprint.iacr.org/2019/579
2. Identity and Payment
In Diode we’re introducing to for identity and payment the concept of “Fleet Contracts”. A fleet contract is a smart contract created by the Sponsor of a fleet of devices and has to follow a specific API that can be used by the miners to receive rewards for serving devices that are covered by the fleet contract. This means that also the fleet contracts are containing functions in their interface to decide whether an identity belongs to it’s fleet. At this stage we have defined “ConnectionTickets” accounting for devices to connect and validate the chain and “TrafficTickets” accounting for devices using the nodes to transmit/proxy data traffic. We have presented some of this during an Ethereum Meetup in Taipei in May (slides here https://docs.google.com/presentation/d/1qVgH8QnPMmV7yAVy4D_gLzJISawlgG7hcVpltqsacnQ/edit#slide=id.p29).
For any such solution the actual throughput of transactions / and the gas cost per transaction is a question to consider. To reduce the cost here, we went the route of a Layer 2 solution inspired by Plasma, but much simplified and specialized to the use case of accounting for resources usage of IoT devices.

As we’re moving forward we are very focused on our use case around IoT devices for certain consumer and industrial applications, but the concept of depositing an amount of value in our fleet contracts seems similar to what slock.it is proposing in the link [@ligi](/u/ligi) shared. I wonder whether there is a generalization possible in which Nodes supporting constrained clients are incentivized from “Fleet Sponsors” not only for predefined services such as in our use case but more generalized for any kind of service.

[@ligi](/u/ligi) what you shared in point 3.11 called client identification seems very similar to what we’ve defined as “Tickets” https://docs.google.com/presentation/d/1qVgH8QnPMmV7yAVy4D_gLzJISawlgG7hcVpltqsacnQ/edit#slide=id.p33

I’ll be in Berlin end of August, but if we won’t make it to chat then, we might also chat in Osaka.

