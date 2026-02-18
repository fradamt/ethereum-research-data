---
source: ethresearch
topic_id: 4808
title: "Whisper-v2 : Request for requirements for ETH2 unified messaging protocol"
author: Ethernian
date: "2019-01-14"
category: Networking
tags: [messaging-protocol, whisper]
url: https://ethresear.ch/t/whisper-v2-request-for-requirements-for-eth2-unified-messaging-protocol/4808
views: 5954
likes: 29
posts_count: 21
---

# Whisper-v2 : Request for requirements for ETH2 unified messaging protocol

I have started to evaluate what is going on with whisper and with secure messaging in ethereum in general.

I found out, that whisper is barely used. Some projects propose to use 3rd party messaging like rabbitMQ, others try develop an own messaging protocol like PSS in Swarm to fit their particular needs. I thought, this is because of missing whisper specification, but the real reason is that whisper does not meet requirements of those projects.

I know six groups working on next generation of ethereum messaging: [Status](https://discuss.status.im/t/protocol-anonymous-communication-requirements-and-brief-update/792), [EF](https://github.com/ethereum/wiki/wiki/Whisper-PoC-2-Protocol-Spec), [W3F](https://github.com/w3f/messaging/), [Swarm/PSS](https://swarm-guide.readthedocs.io/en/latest/pss.html), [Validity Labs](https://www.validitylabs.org) and [CANTO Project (extending RLPx)](https://ethereum-magicians.org/t/canto-a-scalable-blockchain-system-interconnect-model/2203) . They make amazing work, but developing of an universal secure messaging system is not easy because there are many trade offs to be solved differently depending on requirements. If you would like to see wide spectrum of messaging protocols and trade-offs to be solved, please have a look into this [classic paper](http://cacr.uwaterloo.ca/techreports/2015/cacr2015-02.pdf).

Ethereum become more and more heterogeneous ecosystem: sharding, plasma, state channels, swarm, Tx Relays, oracles, side chains - a lot of different nodes that should be able to communicate to each other.

If we would like to develop an unified secure messaging protocol for ETH2, we must start with collecting requirements. [Ethresear.ch](https://ethresear.ch) is a great place for that, because almost any subsystem for ETH2 get discussed and specified here. Unfortunately I don’t see here any discussion about requirements for messaging. All specification efforts are currently going in dev groups internally and probably quite disconnected from demand of projects discussed here. It is not good and I would like to change it.

I would ask all developers working on projects with secure messaging (almost all of them?) to specify requirements for messaging explicitly and make it available here to messaging protocol developers.

Any thoughts?

UPD: [mainframe](https://mainframe.com), [uport](https://github.com/uport-project/uport-transports), [NuCypher](https://ethresear.ch/t/whisper-v2-request-for-requirements-for-eth2-unified-messaging-protocol/4808/15) are building own messaging solutions too.

It is not healthy. We need some unified secure messaging service in ethereum ecosystem.

UPD 2: one project more needs secure messaging: [WalletConnect.org](https://walletconnect.org) aims to replace their bridge-servers routing transactions to be signed from Dapp to Wallet.

## Replies

**Ethernian** (2019-01-22):

Guys, I would like to submit for topic “Whisper v2: Unified Ethereum Secure Messaging” on [Magicians Council in Paris 2019](https://ethereum-magicians.org/t/council-of-paris-2019-announcement/2438).

I would like to discuss …

- What do Ethereum Projects expect from Secure Messaging and why they are re-implementing it?
- What should be improved on whisper in order to make it convenient to use for most ethereum projects?
- //open for other aspects

In order to get a time slot we need to present enough people interested in the discussion.

Please ![:hearts:](https://ethresear.ch/images/emoji/facebook_messenger/hearts.png?v=9) the post to signal your interest.

---

**oskarth** (2019-01-23):

Hi! Oskar from Status here. Thanks for this thread.

Regarding requirements for a Whisper alternative, I just wanted to plug that we (Status, Web3 Foundation, Validity Labs and some others) have started to gather and discuss this here: https://github.com/w3f/messaging

We are also going to have a workshop in Brussels 31/1-1/2, just before Fosdem where we’ll discuss these in more detail. Would love to see more people join this initiative. https://www.meetup.com/Pre-FOSDEM-Messaging-Workshop/events/257926909/?isFirstPublish=true

We also have a Riot channel that’s open, you can join it here: https://riot.im/app/#/room/#web3-messaging:matrix.org

---

**kladkogex** (2019-01-23):

Ideally messaging spec is very simple. There is a smart contract where a messaging provider registers its information, and through which it is paid for its services. There is a JSON api that all messaging providers satisfy.

Take analogy with Linux Kernel device drivers. Linus Torvalds does not develop device drivers. There is a simple spec API that everyone knows

---

**vbuterin** (2019-01-24):

Great initiative!

Some form of robust anti-DoS solution is imo esential; the section in the doc seems underspecified, and I’m worried about institutionalizing reputation-based solutions because those exclude anyone who doesn’t have a friend nearby who’s already using the platform.

Are there thoughts on using either PoW or PoS deposits as solutions here?

---

**Ethernian** (2019-01-24):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Ideally messaging spec is very simple. There is a smart contract where a messaging provider registers its information,

what you actually describe is a registry for messaging providers. We have no re-usable messaging providers actually. This is the problem I would like to target.

---

**Ethernian** (2019-01-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/oskarth/48/1489_2.png) oskarth:

> Regarding requirements for a Whisper alternative, I just wanted to plug that we (Status, Web3 Foundation, Validity Labs and some others) have started to gather and discuss this here https://github.com/w3f/messaging

I fear anyone is too focused on his own project.

Most projects are probably unaware of messaging-as-service idea at all. The rest will face difficulties to collect requirements because it needs some special knowledge about secure messaging protocols. We need to go to other projects actively and collect their requirements on their side. It will be the best promotion for the messaging forum you have mentioned.

---

**burdges** (2019-01-24):

We’re primarily discussing metadata privacy while the SoK paper by Nik Unger, et al. deals more with authentication, an entirely separate question.  We should avoid that derail here, but I’d caution against focusing on deniability between users, like Nik’s PhD work does, although deniability arises naturally below that.

Anyways..

There are numerous academic proposals for messaging that provide metadata privacy in one respect or another, but many lack real scalability.   Source-routed mixnet salability is limited by the PKI for nodes.  True DC-nets cannot scale.  At best DC-nets are only a transport for a mixnet, but an extremely complex one.  You obviously cannot scale up broadcast schemes like Whipser or Secure Scuttlebutt, but worse they do not protect senders.  PIR has cool blockchain applications, but actually doing decentralize PIR requires a massive research effort, and they serve only highly specialized use cases.  Almost all these PIR issues apply to the hybrid mixnet-to-PIR schemes from the MIT CSAIL group, so if you manage then you have a system with like twice the complexity of a mixnet and fewer applications.  In short, mixnets are the only scalable option for metadata privacy.

We want a source-routed mixnet work with a sphinx-like packet format and loopix-like mixing and cover traffic.  If however you literally follow the loopix paper then their “providers” scheme break receiver anonymity, which creates ethical problems and breaks many financial applications, and cannot be considered decentralized.

Instead, we need a sphinx-like packet format that supports chaining single-use reply blocks (SURBs), which requires adding a “SURB log” field to the packet header.  I’ve some notes on the engineering decisions around this in


      ![](https://ethresear.ch/uploads/default/original/2X/b/bad3e5f9ad67c1ddf145107ce7032ac1d7b22563.svg)

      [github.com](https://github.com/burdges/lake/tree/master/Xolotl/papers)





###



Sphinx based mixnet with hybrid forward secrecy (NOTHING HERE YET) - burdges/lake










At the theory level, we should update the security proofs for sphinx to formalize how you use this SURB log field for more complex or group protocols of the sort Status IM does.

I believe the hardest open question is improving the scalability of the mixnet PKI, primarily by understanding the sampling better, but one might explore radical ideas like MPC and pairing-based tricks, like punctured encryption, what I call index-based encryption, or maybe even non-source-routed schemes.  At present, almost all non-source-routed schemes only work for highly specilized cases, like voting.

At W3F, we also now have sensible crypto-economic designs for measuring/rewarding relays that avoid per hop payments.  Any per hop payment design sounds much too slow and worse creates a crypto-economic scenario that quickly breaks cover traffic.  I’ll do a write up in the near future, but I spent the last couple months side tracked by nit-picky signature scheme concerns for polkadot.

---

**SCBuergel** (2019-01-24):

We’re experimenting with a kind of PoS approach here:

[github.com/validitylabs/messagingProtocol](http://github.com/validitylabs/messagingProtocol)

The idea is a TOR-like messaging layer and a payment layer to incentivize relay operators to forward a message. By using staking funds in payment channels (e.g. sender sends 3 Szabo to relayer 1, relayer 1 passes on 2 Szabo to relayer 2, etc) that are closed only after many transactions we aim to preserve privacy. A relay node needs cooperation of the next downstream node to update their incoming payment channel, thereby providing incentive to actually relay the message.

---

**kladkogex** (2019-01-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/oskarth/48/1489_2.png) oskarth:

> I just wanted to plug that we (Status, Web3 Foundation, Validity Labs and some others) have started to gather and discuss this here: https://github.com/w3f/messaging

Imho the best Ethereum can do at the moment is to have many alternatives as the one above and let the innovation flourish.  Lets be frank, the previous iteration of Swarm failed.

Imho the fundamental reason why it failed is because Swarm was not a startup, it was a fun project by people who already made money.  There was no much of an attempt to ship a high quality MVP product and find a product market fit.

Letting other people make money and innovate is the fundamental issue for success of Ethereum project.  Just look at Linux vs BSD.   Would Linux be successful if Linus Torvalds would want to control everything including the graphics UI?  The entire idea of Linux is that everyone becomes an expert  in something, and then a Linux distribution is a collection of independent innovations.

Thats why imho the entire spec for Whisper needs to be one page - basically you need to state that you want to send a message from account A to account B. and then one needs to list security assumptions such as anonymity, encryption, untraceability etc.  And then Ethereum foundation needs to have a call for alternative specs, like NIST did for encryption algorithms.

One needs to have a committee to review the specs.  As a result, several specs may be adopted, serving different purposes.  And then one needs to let startups implement the specs, innovate, compete and make lots of money.

The ideal situation is when Whisper becomes used by billions of people and people who implemented it become rich and happy.  And this is not only true for Whisper. The entire Ethereum ecosystem can become successful only if it becomes a loosely coupled decentralized ecosystem of  projects and  tokens.

The year of 2019  will be very important for ETH, especially since Telegram releases its network, and Telegram guys know how to execute and deliver things.   They are smart and lean startup guys that care about their customers. I think everyone in the ETH ecosystem needs to think about improving execution, which includes doing a retrospective on things that went wrong.   There were lots of projects that raised  too much money and failed to apply the basics of lean startup methodology and customer driven development.

The best imho is for everyone in the ecosystem to draw a fresh line and learn from mistakes.

Taking the example of Whisper, did everyone ever do customer interviews to understand what do customers actually want? For example many people told me that the fact that whisper does not store message make it pretty much unusable for real applications …

---

**Ethernian** (2019-01-25):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> The entire idea of Linux is that everyone becomes an expert in something, and then a Linux distribution is a collection of independent innovations.
> …
> The entire Ethereum ecosystem can become successful only if it becomes a loosely coupled decentralized ecosystem of projects and tokens.

I am completely with you, but I think the discussion about the best way for ethereum to manage projects and innovations is worth of own topic. Could you start one? It would be great! I would answer there.

---

**Ethernian** (2019-01-25):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Taking the example of Whisper, did everyone ever do customer interviews to understand what do customers actually want?

This is exactly what I was missing.

I see the most projects here as future adopters (customers) of secure messaging and that is why I had started this topic here.

---

**burdges** (2019-01-25):

I’d consider competing with telegram, whatsapp, etc. to be mostly off topic for an initially technical conversation, but I’ll share my thoughts since it came up.

Am I correct that telegram’s messaging layer crypto remains highly suspect?  It’s true they’ve many users, due to delivering a nice UI, but if they never quite delivered secure messaging right, then there is zero chance they’ll deliver metadata privacy.  And minimal chance they’ll decentralize anything.

It’s just incredibly rare that “lean startup guys” deliver anything secure because security is fundamentally a cost center that gets cut in being lean.  WhatsApp bought their security from Open Whipser Systems, which worked only because their basic designs matched Signal.  We’re doing this to provide security for everyone though, so we do need to deliver interfaces that make users happy migrating from Telegram and WhatsApp.

We expect like a minute of latency from our system, while those systems have seconds or less, so we automatically loose if latency factors into the competition.  I want to believe that latency could be factored out of the competition by “making the interface more relaxing”.  We know humans do not multi-task well, but all the “start up guys” focusing on “engagement” make this worse.  We should push interfaces towards effectiveness, efficiency, and disengagement, especially making interactions more asynchronous.

In other words, we should write the messenger that productive people want to use to improve their productivity, not the messenger that maximizes how much kids spend on icons.  If such messengers can be built then we’re still at a disadvantage because people start their lives as kids using the engaging messengers, but we believe engagement and productivity to be mutually contradictory, so attracting the productive people becomes a straightforward sales and marketing problem.

Also, I expect the W3F crypto-economic design I mentioned up thread to be vastly more favorable to users than anything Telegram launches.  All crypto-currencies have impossibly shitty gini coefficients, and proof-of-stake launches like polkadot make this worse.  We should actually make money from a messenger, not by charging users for service, but by printing money for relays and users based on them correctly sending cover traffic.  It requires the cover packet creator be staked however, so only staked users could earn money for their cover traffic.  I think even owning a phone number could act as sufficient “stake” for some sub-currency, but not for the one that controls the PKIs security.  I’ll have write ups on these schemes coming along next month.

---

**Ethernian** (2019-01-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/burdges/48/1997_2.png) burdges:

> In other words, we should write the messenger that productive people want to use to improve their productivity, not the messenger that maximizes how much kids spend on icons.

I started this topic not because of messenger use case. Status already works hard on it.

I have started it mostly because of M2M communication. Ethereum becomes highly heterogeneous system with different kind of nodes like shards, plasma, tx-relays, truebit, swarm and many others species.  There will be definitely necessary to send messages between these networks and may be between two particular nodes in these different networks.

This is what I would like to research requirements for.

---

**michwill** (2019-02-02):

Michael from NuCypher here.

I am not sure if Whisper is the right thing or not, but we need some way for nodes in our network to communicate. I think, the most important properties are:

- To minimize the time from connecting to the network and communicating with any node over there;
- The speed of response;
- Python support.

Whisper v1 seemed a little bit heavy-weighted with sending messages to everyone. Perhaps, one way would’ve been do use devp2p or to wrap libp2p, but we went our own way, summarized here: https://blog.nucypher.com/why-were-rolling-our-own-intra-planetary-node-discovery-at-nucypher-beeb53018b0

---

**leonprou** (2019-02-08):

One drawback of Whisper is that the keys (both pubkey and symmetric key) stored in the Ethereum node. Users that does not run their own node had to trust the node provider for key management. User-centric tools like Metamask did a great service for the popularity of Ethereum, and I guess they will continue to be popular with ETH 2.0.

For Dapps, Whisper can be used as a notification channel. As a Dapp developer I think it would be pretty cool if I could just send a message to all the users simply by their addresses, or simply by topic (when I asked them before to subscribe to that topic via the Dapp). So we need to think a notion of “Whisper Provider” (similar to “Ethereum Provider” of web3).

> Am I correct that telegram’s messaging layer crypto remains highly suspect? It’s true they’ve many users, due to delivering a nice UI, but if they never quite delivered secure messaging right, then there is zero chance they’ll deliver metadata privacy. And minimal chance they’ll decentralize anything.

The Telegram client messaging library is open sourced, but the backend infrastructure is closed. About the security, seems like the protocol has number of flaws.



      [security.stackexchange.com](https://security.stackexchange.com/questions/49782/is-telegram-secure)



      [![ilazgo](https://ethresear.ch/uploads/default/original/3X/c/1/c183a99eb75cd32807dd5d95b6871a030916b769.png)](https://security.stackexchange.com/users/35564/ilazgo)

####

  **encryption, cryptography, smartphone, instant-messaging**

  asked by

  [ilazgo](https://security.stackexchange.com/users/35564/ilazgo)
  on [06:17PM - 02 Feb 14 UTC](https://security.stackexchange.com/questions/49782/is-telegram-secure)

---

**cryptogoth** (2019-04-26):

Thanks for starting this thread [@Ethernian](/u/ethernian) sounds like you are looking for something like a standards body that is between academic research and individual (business) use cases.

I know I’m late to the party, but I’m investigating the use of Whisper to coordinate private trading of securities for a current client, and I’d like to pitch it to future clients in creating a decentralized exchange of encrypted assets (using AZTEC Protocol) or coordinate voting on DAOs such as https://alchemy.daostack.io/daos. These tx’s would otherwise be expensive / prohibitive to new users.

For private trading, these messages require encryption to conceal the price of the trade, but are ephemeral (expire after a few days / weeks). The client wishes to use a conventional database to store these trades, as metadata concealing is not important for this particular use case.

From a dapp developer / business perspective, here are some improvements and concerns from me and my client, that would help me recommend Whisper with fewer reservations:

- Most importantly: storage of keys on nodes gives node operators an ability to eavesdrop and forge, so each user would have to run their own server (like Secure Scuttlebutt), and it’s important to support browser-first implementations (like Status’s murmur or ethereumjs-client)
- Unclear incentives to mix routing with other whisper nodes at the moment. Running our own private node will allow our own users to coordinate their on-chain trades.
- Map of Whisper nodes and key performance indicators (KPI in business speak) like uptime, dropped messages, etc. using Grafana graphs, to see the community’s support of the infrastructure, like ethstats.net
- Better documentation, specs, and education, on a single website. Status has made great progress on user-friendly tutorials (that’s how I first got started a few months ago), but more different perspectives and companies collaborating together yield better ideas. As a much simpler example, RadarRelay has made a great resource available at weth dot io and EF about Rinkeby at rinkeby dot io

If anyone is interested in collaborating on the above in an open source-like / standards body way, please reply here, or DM me, or find me on ethereum/whisper Gitter  (I’m [@cryptogoth](/u/cryptogoth) everywhere).

I could use some help in proposing a grant from Web3 Foundation, as it’s most closely aligned to their mandates

https://medium.com/web3foundation/web3-foundation-grants-wave-one-winners-2a9cd39f1fbc

Cheers, looking forward to the future.

---

**Ethernian** (2019-04-27):

Thank you for your reply!

Yes, I know this BusinessCase.

Please give me few days more to reach out related people and prepare more detailed answer.

---

**Ethernian** (2019-04-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/cryptogoth/48/2624_2.png) cryptogoth:

> but I’m investigating the use of Whisper to coordinate private trading of securities for a current client, and I’d like to pitch it to future clients in creating a decentralized exchange of encrypted assets (using AZTEC Protocol) or coordinate voting on DAOs such as Notion – The all-in-one workspace for your notes, tasks, wikis, and databases..

I have asked [@pitkevich](/u/pitkevich) for ideas. She should know more details about similar BusinessCase. Let us wait a bit for her reply.

---

**pitkevich** (2019-05-06):

[@Ethernian](/u/ethernian) [@cryptogoth](/u/cryptogoth)  thank you very much for the intro… At my company we were looking at the case with our potential client to implement ECN (https://en.m.wikipedia.org/wiki/Electronic_communication_network) and were exploring (not really deep) to use Wisper for it.

Because of the legal reasons we were stopped in our exploration (as my company cannot effectively work with Ethereum community due to legal requirements etc). I still believe if we will fix the performance the wispier might be a good choice. If you’d like I can prepare for the discussion over the requirements&use case client had.

---

**fubuloubu** (2019-05-06):

py-libp2p is a work in progress. Check it out here: https://github.com/libp2p/py-libp2p

