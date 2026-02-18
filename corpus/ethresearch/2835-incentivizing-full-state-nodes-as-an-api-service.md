---
source: ethresearch
topic_id: 2835
title: Incentivizing full state nodes as an API service
author: o_rourke
date: "2018-08-07"
category: Economics
tags: []
url: https://ethresear.ch/t/incentivizing-full-state-nodes-as-an-api-service/2835
views: 3056
likes: 4
posts_count: 7
---

# Incentivizing full state nodes as an API service

Hi all, we are posting this in hopes creating discussion and feedback of what we’re building. The following proposes a solution for incentivizing individuals to run full archival nodes for Ethereum and any other blockchain as well. First off we want to tip our hat to [@MicahZoltu](/u/micahzoltu), [@jamesray1](/u/jamesray1) and others for the thinking and research they have done in [EIP908](https://eips.ethereum.org/EIPS/eip-908), [this post](https://ethresear.ch/t/incentives-for-running-full-ethereum-nodes/1239), and [this post](https://ethresear.ch/t/incentivizing-full-state-nodes/1640). We hope this adds to the conversation in a meaningful manner.

### Background

The node incentivization problem is something we recognized about 18 months ago and have been planning a solution since then. For about 15 months we’ve assumed this was going to be a set of smart contracts on Ethereum, but realized that it was not going to be a viable solution due to the limitations and cost of saving state on a set of smart contracts. You can see the first version of these smart contracts in one of our [repositories](https://github.com/pokt-network/pocket-core).

We then dove deep into Plasma, hoping this could be a viable scaling solution for what we were building. We got really excited because all of a sudden we had this whole design space available to us, and we could use Ethereum as its security. We still think this can be built as a plasma chain.

Due to the flexibility of designing a system on Plasma, we started to spec out our own separate blockchain, and decided to completely remove it from there with the assumption of our project being its own blockchain. Our design has significant influence from the Dash protocol, as the original idea of masternodes was meant to combat the problem of incentivizing full state nodes.

We have a white paper that I’ve attached to this post that contains a detailed specification of the protocol itself. Below is a high level explanation of the pieces that go into it. I would also like to point out that we’ve built a lot of the high level tools explained in the paper that make it easy to access decentralized infrastructure on our [github](https://github.com/pokt-network) too.

### The Protocol

Pocket Network is a protocol that pays individuals to run full nodes for any blockchain. This is accomplished by enabling Service Nodes to easily spin up an API for blockchains to service reads and writes.

Each API request (reads or writes) is validated by a group of trusted Federated Nodes known as Validators. Validation is accomplished through a client and service node cryptographic signing scheme explained in greater detail in section 3.2 of the white paper. Anyone can run a Service Node in the Pocket Network with the goal of becoming a Validator. Service Nodes earn Karma for each successful API request, and when certain threshold requirements are met, can become a Validator. There is no limit to how many validators there can be in the Pocket Network. Pocket supports up to ⅓ malicious or replicated nodes using a modified version of PBFT. Thus, the more Validator nodes in the system, the more resilient it is.

At maturity, Pocket Network could be serving many quintillions of API requests a year. Recording each API request into the blockchain is infeasible. The Validators condense the results of the Session (section 3.2 of the white paper) into a single transaction and submit it to the Pocket Blockchain every epoch.

### Economics

Pocket Network is a developer-driven protocol - there can only be as many API requests served as there are applications using Pocket. Instead of paying fees to access service node API’s developers must stake the protocol token (POKT) in advance. The protocol does not deplete the developer’s stake as they use the API services. It throttles the number of API requests a developer can send to a service node in a given Epoch. Once a developer reaches ROI on their staked POKT, they can continue using service nodes at the throttled amount allowed. They can choose to unstake their POKT after an initial lockup period or stake more if their application grows in usage.

While Service Nodes earn Karma for providing an API service, federated nodes mint POKT for each API request validated. Similar to other master node protocols like Dash, service nodes and federated nodes must also stake POKT. This staking and minting mechanism is the basis for the economic model of the protocol. Various burning mechanisms are proposed in the economic paper for the economic sustainability of the protocol at maturity.

### Governance

Federated nodes provide an important governance layer as well. Inspired by the Dash protocol, 10% of each mint from a validated API request goes to a DAO (section 5). Participants must burn POKT to submit a proposal for some amount of POKT from the DAO. This ensures the long-term sustainability of the Pocket Network through native allocation of POKT for future protocol development.

[POCKET WHITEPAPER V0.1.0.pdf](https://ethresear.ch/uploads/default/original/2X/b/b662eec0f686f44f504eb49e69760fca42535682.pdf) (401.0 KB)

## Replies

**thegostep** (2018-08-08):

This infrastructure is something dApp developers will be infinitely thankful exists if something ever happens to Infura! Many are taking full nodes for granted. Looking forward to seeing how this project develops.

---

**jamesray1** (2018-08-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/o_rourke/48/1549_2.png) o_rourke:

> Pocket supports up to ⅓ malicious or replicated nodes using a modified version of PBFT.

Thanks for trying to solve this problem, I believe that the Ethereum community has underrecognized the importance of solving it.

Why not use Casper, which is able to explore the full [tradeoff triangle](https://github.com/ethereum/cbc-casper/wiki/FAQ#what-is-the-tradeoff-triangle), in a deterministic, asynchronous fashion with hybrid blockchain-based and traditional consensus?

What are the repercussions of your proposed protocol for users?

I think extra-protocol appproaches like VIP node and Rocket Pool are probably insufficient and that in-protocol incentives are necessary. I tried to raise EIP-908 at a few All Devs meetings, but gave up because it was given insufficient attention; I felt like I was flogging a dead horse; and have continued work on sharding and libp2p gossipsub development.

I don’t know if it’s just the way my computer is set up with Manjaro, Firefox and No PDF download, but I can’t copy and paste in your PDF.

If you are planning to have on-chain governance, you need to make sure that any voting has sybil resistant input from node operators, which is difficult to achieve, and I’m not sure if anyone has discovered a way of doing that. See also https://github.com/ethereum/wiki/wiki/Governance-compendium#against-on-chain-governance.

[![Screenshot%20from%202018-08-08%2013-56-14](https://ethresear.ch/uploads/default/original/2X/2/2c4349d8870815e7d9857d051623414610c22d07.png)Screenshot%20from%202018-08-08%2013-56-14514×463 15 KB](https://ethresear.ch/uploads/default/2c4349d8870815e7d9857d051623414610c22d07)

Yes, I thought of the same attack while reading the paper. You need to go beyond thinking of specific attacks, and also generalize to prove how security properties such as safety, liveness and censorship resistance are maintained, and under what assumptions.

[![Screenshot%20from%202018-08-08%2013-58-51](https://ethresear.ch/uploads/default/original/2X/d/d133504ab29e9f5a2bf6ad0700cc9f6a3ae355ea.png)Screenshot%20from%202018-08-08%2013-58-51484×294 8.34 KB](https://ethresear.ch/uploads/default/d133504ab29e9f5a2bf6ad0700cc9f6a3ae355ea)

It is better to be leaderless. On round robins, you need to use a better source of randomness, such as RANDAO. See https://vitalik.ca/files/randomness.html FMI.

---

**o_rourke** (2018-08-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> Why not use Casper, which is able to explore the full tradeoff triangle, in a deterministic, asynchronous fashion with hybrid blockchain-based and traditional consensus?

Casper provides an interesting economic and security tradeoff. It would need to be a hybrid model where federated validators for relays get rewarded and proof of stake validators get rewarded as well.

If you are running a full infrastructure service like Infura but as a federated node on Pocket costs can get expensive quickly if using a cloud service provider like AWS. We do believe Pocket will also incentivize people to run their own infrastructure locally to reduce costs and dependency on other services.

For example, if it’s a 45/45/10 model like Dash the staking economics would have to ensure that the value of the reward for federated nodes is greater than the costs of running one. We opted for the federated route and have 90% of the mint reward to go to the federated nodes. That being said, it seems like there are some possibilities to balance out the economics with PoS below the relay validation layer. This would broaden the base of stakers within the protocol and act as a protection layer from the federated validators taking over the network.

**On users and governance -**

The users of the protocol are primarily developers, service nodes and federated nodes. Developers stake POKT to access API services, service nodes earn karma, and federated nodes mint POKT then sell to developers and service nodes to cover their costs.

We believe in the “messy” style of governance that Ethereum is working through. This forum and the EIP process is a direct example of it, where there are conversations and then formal specifications for upgrades to the protocol. We would be setting a “social contract” for people who want to see Pocket grow, and are in line with the changes in the future for it as well.

We are toying around with the idea of voting on the DAO not being just coin holders, but developers who have actually used the protocol in some amount as well. The protocol can keep track of how much of a used stake you’ve had, and because developers have different incentives than federated nodes, it helps balance things out.

---

**jamesray1** (2018-08-09):

Best of luck with it, it will be interesting to see it live! I might have a look at the test network when I find some time.

---

**jamesray1** (2018-10-17):

Interesting that you have moved to incentivizing relays instead of storage. It would be interesting to try and  do both, but I suppose you could roll out one feature, then the other.

---

**jamesray1** (2018-10-17):

Nevermind, looking at the white paper yet again, it seems that you’re planning to do both.

