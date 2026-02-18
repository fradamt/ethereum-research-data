---
source: ethresearch
topic_id: 7159
title: Who's working on what?
author: pipermerriam
date: "2020-03-20"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/whos-working-on-what/7159
views: 3228
likes: 34
posts_count: 13
---

# Who's working on what?

I’d like to get a sense for who’s working on what across both eth1.x and eth2.  My goal is to identify areas of work where we know things need to be done but that nobody is actively working on.

You might use V’s diagram from this post if you need a reference for what topics are out there: https://twitter.com/VitalikButerin/status/1240365047421054976

Things to consider including.

- what are you researching/thinking about
- what are you building
- what areas are you interested in pursuing (things that you haven’t been actively working on but that you’d like to)

## What is Piper working on

- I’m “owning” the overall effort to make sure “Stateless Ethereum” keeps making progress.
- I’m passively researching DHT networks for use in the “state network” for providing on-demand state data.
- I’m actively researching a new sync protocol as well as planning to play coordinator between the others who want to be involved in this effort.

## Replies

**q** (2020-03-21):

Hi, this is Afri from the Görli Testnet Initiative.

After following ETH 2.0 client development loosely, we noticed there might be some coordination wanted towards a multi-client phase-0 testnet in the coming months.

[![ETaj8ruWAAM1AdG](https://ethresear.ch/uploads/default/optimized/2X/4/4cd9aae2a51c337bcb5810425790cfc6c66b1583_2_690x401.jpeg)ETaj8ruWAAM1AdG792×461 99.1 KB](https://ethresear.ch/uploads/default/4cd9aae2a51c337bcb5810425790cfc6c66b1583)

We have resources available to support client teams in coordinating:

- Coming up with a testnet spec that would work across multiple clients
- Getting clients up to speed with networking, validating, synchronization, or anything else if necessary

We had a call previously with Danny and Hsiao-Wei two weeks ago, notes: `hackmd io Nx204wkTSgeGB0UzNXhz9g`

We explored the feasibility launching a beacon chain using the Lighthouse client this week, notes: `hackmd io GIwaFeGaQn6q7VYb_n94LA`

And published The-Practical-Dev article:


      ![](https://media2.dev.to/dynamic/image/width=32,height=,fit=scale-down,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F8j7kvp660rqzt99zui8e.png)

      [DEV Community](https://dev.to/q9/how-to-run-your-own-beacon-chain-e70)



    ![](https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fi%2Fwnxhxughx2dm7x63ofbh.jpg)

###



This article is for educational purposes only. A beacon chain is a future Ethereum 2.0 relay...










We’ve put multi-client testnet on the ETH-2.0-Call-36 agenda for next week and will eventually spin out dedicated calls for client teams to focus on joint testnet efforts in future: `github.com ethereum eth2.0-pm issues 135`

The overall goal would be, as opposed to previous *interop* efforts, to have a persistant state of interoperability across all clients, i.e., by not having a specially patched branch but rather having a baseline compatibility in the master/development code.

Please, hit me up if you want to discuss or coordinate. I’m `@q9f` on Discord and Github. *(Sorry, can’t post more than two links here.)*

---

**ericsson49** (2020-03-23):

I’m Alex Vlasov, from TX/RX team, ConsenSys/Pegasys.

I’m working on Clock Synchrronization Protocol for Eth2, right now.

Additionally, on fork choice tests.

More generally, I want to make sure that the subprotocols, that beacon chain relies on or requires (clock sync, node/topic discovery, libp2p) are BF tolerant and cannot be used to perform attacks on beacon chain protocol/Ethereum 2.

That includes (more detailed) Ethereum 2.0 security model.

---

**franck44** (2020-03-23):

Hi,

I am Franck from ConsenSys/PegaSys, Consensus Protocol team, Sydney, Australia.

We are working on a formal specification of the Eth2.0 specifications using the Dafny verification-aware programming language.

Our first aim is to provide a formal specification/correctness proof of Eth2.0 Phase 0.

This is work in progress and we have started with SSZ and Merkleisation.

More generally, we endeavour to foster the use of formal methods in the development Blockchain systems.

---

**ProfessionalKiwi** (2020-03-24):

Hello! I’m Ivan Martinez, an engineer for Prysmatic Labs.

I’ve been working mainly on the Slasher client lately, but I’m very familiar with our beacon chain and validator clients as well.

I’m extremely excited by EIP1559, and would like to help however I can. I would also like to help with the stateless effort but my cryptography knowledge still needs work. Particularly I’m interested in state providers but happy to help where I can.

---

**terence** (2020-03-24):

Terence from Prylabs. I thought I’d drop by and say hi. Had a brief chat with Danny last week about supporting phase 1 implementation on Prysm. In my spare time, I’m building a proof of concept phase 1 client on top of Prysm

https://github.com/terencechain/prysm-phase1

The goal of this proof of concept is to build 1-2 shard chains along side beacon chain to simulate what phase 1 will look like. Hopefully it serves to be useful to validate eth1.x core ideas and eth1.x → eth2 migration, Feel free to ping me on telegram @terencechain if there’s any questions

---

**gballet** (2020-03-27):

I’m Guillaume from the Geth team. I’m working on:

- Changing eth1 trie format from hexary to binary
- Turning geth into a shard 0 block producer

---

**hmijail** (2020-03-30):

Horacio from Team X (Enterprise, Cross Shard & Stateless - ECSS, pronounced X) in ConsenSys/PegaSys.

- Cross-Shard: We implemented a PoC for Atomic Cross-Chain Function Calls for sidechains on Eth1, and are working on applying our learnings to Cross-Shard transactions on Eth2. Currently with focus on how to transfer Eth as part of the function call, building on the netting proposal.
- Stateless: we are starting work on witness spec proposals, compression techniques, charging strategies and tiling; researching hexary-to-binary Merkle trie transition possibilities; and analysing the “three network” strategy and protocols.

---

**mandrigin** (2020-03-30):

Igor from Turbo-Geth here.

I’m working [on the witness spec](https://github.com/ethereum/stateless-ethereum-specs/blob/5ca1bcda54a5b2bdca27ab1d57cb0dcf2aad5e29/witness.md) primarily.

Also, I’m implementing/adjusting turbo-geth code to be compliant with the witness spec.

Also, I do quantitive experiments on witnesses on mainnet sometimes.

---

**alonmuroch** (2020-03-31):

Hi, I’m Alon from Blox.

We are researching trustless staking pools based on DKG and a consensus layer on top.

First post about it [here](https://ethresear.ch/t/trustless-staking-pools-with-a-consensus-layer-and-slashed-pool-participant-replacement/7198/2)

We develop infrastructure for eth 2.0 coupled with a hot-wallet for validators. Basically easy staking setup while you keep your keys.

---

**jrhea** (2020-04-28):

Hello, this is Jonny Rhea from the TX/RX team (Consensys).

I am working on network health monitoring and testing strategies.  A brief description of the plan:

> Deploy a swarm of semi-autonomous network agents masquerading as an Eth2 node that communicate with a command & control service. This service will collect, aggregate and analyze information from individual agents to evaluate network health. Additionally the command & control service can coordinate the agents to perform attacks to the network, evaluating the security and resilience of the protocol.

Here is a link to the project:



      [github.com](https://github.com/prrkl/docs/blob/master/README.md)





####



```md
# prrkl: 😈 Evil P2P Network Tooling 😈

Tools to monitor, test, and break p2p networks.

## Links

- Eth2 Network Monitor: [project overview](https://github.com/prrkl/docs/blob/master/project-overview.md)
- Eth2 Network Agent: [imp](https://github.com/prrkl/imp)
- Libp2p for Dummies: [mothra](https://github.com/prrkl/mothra)

```

---

**mkalinin** (2020-05-07):

Hello everyone!

This is Mikhail Kalinin from the TX/RX research team (ConsenSys).

I’ve been previously worked on Eth1-Eth2 two-way bridge, currently proceeding with Eth1-Eth2 merger.

---

**alonmuroch** (2020-05-09):

We are working on trustless pools as well

https://ethresear.ch/t/trustless-staking-pools-with-a-consensus-layer-and-slashed-pool-participant-replacement/7198/3

