---
source: magicians
topic_id: 2203
title: "CANTO: A Scalable Blockchain System Interconnect Model"
author: atoulme
date: "2018-12-12"
category: Magicians > Primordial Soup
tags: [ethereum-roadmap, interop, canto]
url: https://ethereum-magicians.org/t/canto-a-scalable-blockchain-system-interconnect-model/2203
views: 6201
likes: 29
posts_count: 23
---

# CANTO: A Scalable Blockchain System Interconnect Model

Hi everyone,

We as a team between ConsenSys ([@atoulme](/u/atoulme), [@willmeister](/u/willmeister))  Whiteblock ([@zscole](/u/zscole), [@araskachoi](/u/araskachoi))  and a few other outfits are looking to help Ethereum scale.

We have started working on what we hope is an intriguing solution with a relatively quick implementation time that we think will benefit all participants in the Ethereum network.

It will help miners as we will reward them to host chains.

It will help developers control the chain, its rules and its governance.

It will help users participate directly in chains that are smaller and can be downloaded to a phone.

We have been working on formalizing our full thinking in this [specification](https://github.com/canto-ethereum/spec/blob/master/canto.md).

We are also working on a [POC](https://github.com/canto-ethereum/spec/blob/master/poc.md) to demonstrate how this can be practically implemented.

Your thoughts and reviews are very appreciated.

## Replies

**boris** (2018-12-13):

Hey [@atoulme](/u/atoulme) – awesome to see you decloaking and starting to share this more widely.

I find the Overview to be an easier starting point:

https://github.com/canto-ethereum/spec/blob/master/canto.md

Especially this picture / diagram:

[![](https://ethereum-magicians.org/uploads/default/optimized/2X/d/d7b7825917c44578ade122d641ab9fd4fd2c6922_2_549x500.jpeg)1551×1411 289 KB](https://ethereum-magicians.org/uploads/default/d7b7825917c44578ade122d641ab9fd4fd2c6922)

To put it into a more explainable way, is this a correct way of explaining it?

---

CANTO modifies the network layer of existing Ethereum clients to allow for the creation of subnets – by defining a new subprotocol. Each subnet is effectively a sidechain, and sidechains can make their own choices around consensus algorithm, gas, or a wide variety of other parameters. The Ethereum mainchain with PoW secured by miners as it is today is the highly secure base layer that all the sidechains connect into, with gateway contracts defining the interactions and trust of state on the sidechain.

---

I went back and read the overview and answered some other questions I had ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

I’m actually unclear if my attempted summary here is helpful – “Read the Overview” and [Read the FAQ](https://github.com/canto-ethereum/spec/blob/master/canto.md#faq) are likely the best ways to make sense of this.

---

**zscole** (2018-12-13):

Yeah, that’s a good summary, but it’s also important to note that the subprotocol itself allows the nodes to essentially operate on more than one network/subnet/networkID simultaneously.

---

**boris** (2018-12-13):

Yes, definitely key! Maybe that should be in big letters somewhere – this whole system is designed to be able to use existing Geth, Parity Ethereum, etc. etc. client software to run nodes, and “just” add the subprotocol.

---

**zscole** (2018-12-13):

Another point is that subnets can be rapidly created and destroyed. Think of the it as Docker containers inside the EVM where the gateway contracts can be likened to Dockerfiles. This can be done quickly and allows subnet creators and participants to configure the parameters of how their subnet operates.

---

**lrettig** (2018-12-13):

At a high level the design sounds quite similar to Polkadot, in that each subnet is self-sovereign, handles its own consensus and security, etc. The main differences seem to be that it uses existing Ethereum/EVM as the base, connector layer, and that it doesn’t contain any on-chain governance/upgradability mechanism like Polkadot. Is this assessment fair?

If so – cool!

---

**zscole** (2018-12-13):

Yes, you are correct. It’s similar in principle, however, there are some fundamental differences between the two. First of all, the Polkadot model is PoS based and also implies a certain degree of inherent connectivity and necessary cooperation between individual sidechains. While Canto presents a similar approach from a high-level, the intent is to provide a practical solution that can be easily implemented in a manner that requires very little additional re-architecture or development of the existing Ethereum protocol.

The Canto model is still POW based, but the subnets are logically isolated from one another and responsible for their own security and function. Assuming that a subnet is stable and consistent, we can also assume that its own transactional processing would be retained within that particular environment, thereby reducing the computational overhead required by POW on layer 1. To further expand on this notion, transactional activity on layer 1 would be limited to the result of very few actions, including subnet creation, subnet destruction, participant entry, and participant exit. This optimization could dramatically reduce the total amount of POW transactions, allowing anyone to participate as a miner without the need for commodity hardware.

The next point of difference would be that Canto’s design principles place an emphasis on consent, choice, and sovereignity, so long as the integrity of the primary layer is preserved. Each subnets has the ability to dictate its own terms of engagement. Interoperability between subnets is a choice. Consensus mechanisms are a choice. The act of joining a particular subnet, multiple subnets, or any subnet at all is a choice. The staking mechanics provide an insurance layer between the subnets and the primary EVM and also help contol liquidity.

For example, if some sort of experimental system chose to build out on a subnet, they can choose to implement whichever consensus algorithm or protocol they choose. Since the ephemeral nature of the subnets allows them to be rapidly constructed and deconstructed, the participants would still be able to experiment in a safe environment. If some sort of security issue were to present, the existing subnet could simply choose to rebuild itself as a separate subnet, similar to a forking event, however, the users would only have to change the network ID in the subprotocol to make the switch. From a more practical perspective, if an ICO were to choose to build on a subnet, they would be able to very quickly provide utility or at least an MVP.

While the microeconomics of the subnet itself could be affected, the results wouldn’t be nearly as adverse as they would be within the present system, but most importantly, because of the staking mechanics, the effects would be limited to the subnet and its participants and preserve the integrity of the primary EVM. Since the subnets are logically independent, the operations of each have no impact on any other, unless they choose to interoperate via cross-chain bridge.

There’s a lot of additional details we’ve discussed and are eager to share, but I’ll spare this post of further elaboration for the sake of brevity. Your feedback and critique is much appreciated.

---

**atoulme** (2018-12-19):

In our latest instalment, we now have a working PoC that showcases Canto in action.

We have used the new Canto subprotocol to show that it was possible to communicate with several subnets over one RLPx connection. In our test, 3 clients are created and connect to each other over RLPx.

Each client then connects to a remote server over a WebSocket.

Those remote servers run their own protocol - a simple ping/pong request reply in this case. We show that servers can independently communicate.

For more details, refer to the [code](https://github.com/canto-ethereum/canto-java/blob/master/client/src/test/java/org/ethereum/canto/client/ClientTest.java#L139) here.

---

**tvanepps** (2018-12-20):

this is very interesting stuff! a few questions:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zscole/48/9401_2.png) zscole:

> unless they choose to interoperate via cross-chain bridge.

1. Does a cross-chain bridge refer to the ETH base chain or is this more analogous to cross-shard tx communication

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zscole/48/9401_2.png) zscole:

> This optimization could dramatically reduce the total amount of POW transactions, allowing anyone to participate as a miner without the need for commodity hardware.

1. wouldn’t ASICs just absorb this new revenue source? or, for example, could ProgPow be implemented on a subnet?
2. Could an account send ether to a subnet have a sub-address created and then that ether (in the form of sub-net tokens) be deposited in a single transaction? and then actions signed from that previous address? This might be out your scope for now, I’m reminded of @austingriffith’s work on meta-txs

Your use of ‘ephemeral’ in the spec really helped illustrate what subnets can be (blooming in and out of existence). could something like ‘session-chain’ also work? Although ‘chain’ does have some permanence associated with it. I understand why you went with subnet. Canto seems more versatile than a simple sidechain as well - In theory it could be a long lived sidechain. Loom / POA / Skale are recruiting validators based on their community standing / reputation which signals that they are meant for the long-term.

This is great, looking forward to learning more!

---

**zscole** (2018-12-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tvanepps/48/3406_2.png) tvanepps:

> Does a cross-chain bridge refer to the ETH base chain or is this more analogous to cross-shard tx communication

Technically, they’re all ETH-based chains, so functionally, they would be able to communicate using a typical cross-chain bridge. It wouldn’t require much additional development on the protocol layer. Based on my experience, cross-shard tx communications rely on more complex pub/sub epidemic broadcast trees. I think these decisions can be made at the subnet level so long as they don’t effect the mEVM.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tvanepps/48/3406_2.png) tvanepps:

> wouldn’t ASICs just absorb this new revenue source? or, for example, could ProgPow be implemented on a subnet?

Sure, this is a possibility, but it shouldn’t make much of a difference because the real value should come from POS incentive mechanisms, which anyone can participate in. Since the miners would be further incentivized to stake their rewards, it would create a more robust insurance layer. Subnets, on the other hand, can choose to implement any consensus mechanism they see fit. There’s certainly more to think about on this subject though, but the idea is to get a scalable solution out the door quickly without the need to rearchitect the existing system.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tvanepps/48/3406_2.png) tvanepps:

> Could an account send ether to a subnet have a sub-address created and then that ether (in the form of sub-net tokens) be deposited in a single transaction? and then actions signed from that previous address? This might be out your scope for now, I’m reminded of @austingriffith’s work on meta-txs

I’m not quite sure what you mean by this. Would you mind elaborating?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tvanepps/48/3406_2.png) tvanepps:

> Could something like ‘session-chain’ also work?

Yeah, that would work as well. We decided to go with the term subnet because it was easier to understand in relation to existing networking terminology. I don’t think any of us were necessarily fans of the whole subnet/plasma/sidechain terms because they seemed to convolute any practical understanding for the system function.

Thanks for the feedback!

---

**tvanepps** (2018-12-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zscole/48/9401_2.png) zscole:

> Sure, this is a possibility, but it shouldn’t make much of a difference because the real value should come from POS incentive mechanisms, which anyone can participate in.

understood, but it would apply when PoW subnets are used.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zscole/48/9401_2.png) zscole:

> I’m not quite sure what you mean by this. Would you mind elaborating?

I’m now remembering in the spec that this requires an oracle to trigger the transfer function from the subnet contract to the subnet address. meta-txs basically allow you to signal from an empty account that you need tokens in order to transact and then a separate contract fulfills that. Austin would have a more accurate description. I guess these mechanisms would be papered over for someone just looking to play a quick game or something. they won’t really know that their ether is being held in a separate contract and that they are actually using a subnet with subnet tokens… etc etc

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zscole/48/9401_2.png) zscole:

> We decided to go with the term subnet because it was easier to understand in relation to existing networking terminology.

I think subnet as a term works well (given what it actually does and how it relates to the larger network of nodes), it just takes a little longer to click vs. a term like ‘sidechains’ >> chains on the side, easy. If there were a way to emphasise the temporal flexibility that might help.

What’s next now that the PoC is released, [@atoulme](/u/atoulme) / [@zscole](/u/zscole) ? I’m sure there are plenty of ideas…

---

**atoulme** (2018-12-20):

Thanks for the peer pressure. I am busy with other things just at the moment (Christmas shopping for example), but mean to publish a roadmap ~~tomorrow~~ really soon.

---

**zscole** (2018-12-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tvanepps/48/3406_2.png) tvanepps:

> PoW subnets

PoW subnets would be operating independently of the L1 mEVM, so their PoW implementation would be isolated to the subnet. There should’t be any merge mining, so they’re not operating on the same chain.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tvanepps/48/3406_2.png) tvanepps:

> I’m now remembering in the spec that this requires an oracle to trigger the transfer function from the subnet contract to the subnet address. meta-txs basically allow you to signal from an empty account that you need tokens in order to transact and then a separate contract fulfills that. Austin would have a more accurate description. I guess these mechanisms would be papered over for someone just looking to play a quick game or something. they won’t really know that their ether is being held in a separate contract and that they are actually using a subnet with subnet tokens… etc etc

Oh! Yeah, this makes sense. We actually discussed a function similar to this, but didn’t really detail it in the paper because that’s something more complex that we wouldn’t necessarily be able to provide immediately.

---

**atoulme** (2018-12-20):

I’m very short on time, so here is a video of me explaining the problem, where the POC is at and a few next steps: https://consensys.zoom.us/recording/play/RGByv1dQfVNp9iQK4UZinYffnvjqQ9_nK_yzSTSls-ATMoYMu-JYCkQr4q8CwQON?continueMode=true

I’ll post issues on github tomorrow in collaboration with the complete team.

---

**tvanepps** (2018-12-20):

cool, that video was also helpful

I’d love to do a writeup to introduce Canto more broadly when your team thinks it’s appropriate

---

**atoulme** (2018-12-20):

Contribs are welcome anytime, this project is your project. Make beautiful things with it please.

---

**Ethernian** (2018-12-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/atoulme/48/1323_2.png) atoulme:

> We have used the new Canto subprotocol to show that it was possible to communicate with several subnets over one RLPx connection. In our test, 3 clients are created and connect to each other over RLPx

If I understood you correctly, you have extended devp2p/RLP in that way, so it becomes possible to route messages between nodes in different “subnets” whatever their particular implementation looks like: sidechains, plasma, etc.

I am wondering, there is no similar topic discussed on [ethresear.ch](https://ethresear.ch), although plasma and other “subnets” are heavily discussed there.

Would you probably publish your ideas and in particular the RLPx extension on [ethresear.ch](https://ethresear.ch)?

I would really appreciated to see plasma developers involved into CANTO discussion, because they will become naturally implementors and users of the protocol.

---

**atoulme** (2018-12-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> Would you probably publish your ideas and in particular the RLPx extension on ethresea.rh?

Yes, I think now is a better time to do so.

---

**tvanepps** (2018-12-20):

another question: follow the closure of the subnet, nodes cease being incentivised to hold the block history. this would be deleted (voluntarily)?

In theory, could this data persist even after the subnet dies if a node decided to keep it for some reason?

---

**atoulme** (2018-12-20):

I don’t think we cover data lifecycle once the network is deemed terminated. It’s up to the node to continue holding on to the data or recycling it. It doesn’t matter to me all that much.

---

**zscole** (2018-12-21):

yeah, i thought about this earlier too. the data could persist, but it would only be on one node, so what would it really matter?


*(2 more replies not shown)*
