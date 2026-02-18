---
source: ethresearch
topic_id: 2634
title: Payment Channels with central hub
author: adamskrodzki
date: "2018-07-21"
category: Layer 2 > State channels
tags: []
url: https://ethresear.ch/t/payment-channels-with-central-hub/2634
views: 5121
likes: 22
posts_count: 26
---

# Payment Channels with central hub

Hello,

for some time I’m trying to find working implementation

of Ethereum payment channels with central hub (

all participants except hub have only one channel opened - to hub) but was suprised that there is none in production.

I’ve found only solutions which are far away from being user friendly and still in tests (eg. Raiden) .

Are there any particular reason why ?

My idea is to implement payment channel smartcontract which can verify signatures of human readable messages (like eg.  “000000000000000003.You have 000000000000000003.123000000000000000 ETH if you know the secret 0x…”) and control payment channels that way.

Central hub would not be able to steal any funds so it would be still trustless (thanks to hashlocks). Worst it could do is to censor some user from sending eth to anyone. I’m aware that to make it work substantial deposit on hub side is required, but it does not sounds like a dealbreaker. Also hacking central hub would not put users funds in danger (only hubs).

From user perspective that would be ordinary website integrated with MetaMask which pop up human readable messages to sign from time to time

If I’m correct that kind of solution will be sufficient for micropayment and could be used in practice by things like online services.

My question is

1. Is there solution like that already
2. Is there any reason why that kind of solution is not as useful as I think
3. Is there any reason why that kind of solution is harder to implement than I think

Thank You in advance for answer.

## Replies

**jfdelgad** (2018-08-07):

Having a Hub is something people are complaining about a lot (see lightning network). The issue that things become centralized.

---

**eolszewski** (2018-08-07):

Can you link to the relevant literature and gripes that you’re talking about, please? ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**adamskrodzki** (2018-08-08):

Yes,

I’m aware of, but not every channel need to serve same purpose.

Imagine service like ‘eBay’ using payment channels with central hub (managed by him)

You can enjoy fast cheap transactions and You do not mind that ebay knows what and when and from who You where buying. Actually You might even prefer it since that gives ‘eBay’ opportunity to build some insurance for buyers system on top.

---

**adamskrodzki** (2018-08-08):

Could not find any which describes payment channels with central hub,

here is great resource about virtual hubs idea


      [eprint.iacr.org](https://eprint.iacr.org/2017/635.pdf)


    https://eprint.iacr.org/2017/635.pdf

###

469.04 KB

---

**jfdelgad** (2018-08-08):

I agree with this, but notice that the channel can be opened by any one, for payments to ebay and any other provider such that it becomes a bank-like system, which takes away the whole purpose of the decentralization. Do not take me wrong, I like the idea and I have been implementing custom versions of payment channels, but when it comes to scaling those, a hub have the risk of make the whole system centralized which usually leads to abuse and corruption. Maybe we can come up with address this issue?.

---

**adamskrodzki** (2018-08-08):

It not exacly takes away whole purpose of decentralisation. Bank can zero Your account and say ‘because we can’ (theoretically) and You will not be able to recover those funds or even able to prove to third parties that it was not zero. In payment channel with central hub Hub cannot zero your account. You can always withdraw. You do not give up safety, only privacy and possibly availability - which (privacy) btw is added value of other payment channels, since ethereum as is has no privacy (or very little at best).

So tradeofs comparable to on-chain transactions are:

(+) faster

(+) cheaper

(-) lower availability

Tradeofs in comparition to things like Raiden are:

(+) much easier to use for end user (no instalation, just browser and web3 provider)

(-) no privacy if hub misbehave

---

**eolszewski** (2018-08-08):

[@adamskrodzki](/u/adamskrodzki) - here’s your hub and spoke payment channels https://finalitylabs.io/static/media/SetPaymentChannels.8a29d449.pdf

These are being implemented on spankchain right now

[@jfdelgad](/u/jfdelgad) Re: “Having a Hub is something people are complaining about a lot (see lightning network). The issue that things become centralized.” - Please provide some evidence of this - otherwise you’re just adding noise ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**jfdelgad** (2018-08-08):

I wish the conversations could go along in good terms, but seems like this is not possible. Yet before going I will leave you with several sources that support my comment, if you agree or not with it is irrelevant:

This comes from different sources from mainstream news to people making valid, sustentable points:


      ![](https://ethresear.ch/uploads/default/original/3X/e/f/ef60601f359b90de6d3e2e5c46a4f80e9333ca31.png)

      [Cointelegraph](https://cointelegraph.com/news/lightning-network-will-be-highly-centralized-gavin-andresen)



    ![](https://ethresear.ch/uploads/default/original/3X/1/3/137032a8b04a85c92b9be54f873c07a3301533a0.jpeg)

###



The Lightning Network will be “highly centralized,” developer Gavin Andresen has said.











      ![](https://ethresear.ch/uploads/default/original/3X/9/4/94d18ac406ebd1273caf396b6c9a89ee5af0103e.png)

      [Bitcoin News – 9 Oct 17](https://news.bitcoin.com/lightning-network-centralization-leads-economic-censorship/)



    ![](https://ethresear.ch/uploads/default/optimized/3X/f/0/f05e30e0bb2d3336e2f5334a12f58fadfaf437d6_2_500x500.jpeg)

###



A few months ago, I wrote an article called “Mathematical Proof That the Lightning Network Cannot Be a Decentralized Bitcoin Scaling Solution”



    Est. reading time: 5 minutes











https://medium.com/@jonaldfyookball/mathematical-proof-that-the-lightning-network-cannot-be-a-decentralized-bitcoin-scaling-solution-1b8147650800

This one is just entertainig

  [![image](https://ethresear.ch/uploads/default/original/3X/c/7/c70b8e912d91709ef09e8087d59fa1b6137ece3a.jpeg)](https://www.youtube.com/watch?v=UYHFrf5ci_g)

That said I agree with @ [adamskrodzki](https://ethresear.ch/u/adamskrodzki) The problem is not if the system is centralized, the real problem is that this centralization leads to corruption and abuses. If this can be avoided by imposing rules using smart contracts I think this will work just well.

---

**nginnever** (2018-08-17):

A payment channel with a hub-and-spoke model as in the OP does not equal Lightning Network or Raiden in their requirements or what they are trying to achieve. It’s an interesting debate of whether a decentralized network is desirable over a verified provider.

Routing was a problem that we decided to avoid by choosing an application that can work with a simple hub-and-spoke model. It could be interesting to see how many applications could fit such a model. As Gavin Andresen states, a centralized Lightning Network (which really isn’t a network) may not be a bad thing.

You in a way see this pattern in Plasma as well, where more emphasis is placed on verifying that the operator (central bank) can’t act out of your interest. As you say a good set of rules and protocol to be sure you can’t be cheated is the way to go.

---

**jfdelgad** (2018-11-05):

When you said:

![](https://ethresear.ch/user_avatar/ethresear.ch/nginnever/48/1936_2.png) nginnever:

> we decided to avoid by choosing an application that can work with a simple hub-and-spoke model.

You mean that you have an implementation of payment channels with a central hub? If not, do you know about any working applications? Also, there is no need for a central hub, one may think that the hubs can be run by anyone.

---

**adamskrodzki** (2018-11-05):

> one may think that the hubs can be run by anyone.

It is certainly possible but it introduces routing problems again if person You want to interact with is not in the same hub

---

**nginnever** (2018-11-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/jfdelgad/48/1295_2.png) jfdelgad:

> You mean that you have an implementation of payment channels with a central hub? If not, do you know about any working applications?

I worked with SpankChain and helped them write the first version of their non-custodial hub.

![](https://ethresear.ch/user_avatar/ethresear.ch/jfdelgad/48/1295_2.png) jfdelgad:

> Also, there is no need for a central hub, one may think that the hubs can be run by anyone.

Finding a path is an issue and I would argue that not anyone can be a hop in a payment path since it requires capital lockup. Centralized hubs may be necessary or at least desired in the absence of good routing algos over payment networks, depends maybe on your use case for payments.

---

**adamskrodzki** (2018-11-06):

Hi [@nginnever](/u/nginnever) which spankChain project You have in mind? Is it on github?

---

**nginnever** (2018-11-06):

https://github.com/SpankChain/virtual-channels

It’s a perun / L4 (meta) style payment hub. You’ll notice that it is still a bit of a work in progress. There are a lot of small considerations that go into actually putting a hub into a working system.

i.e. with spankchain you have a bunch of viewers opening virtual channels with performers who may more than likely close their laptops and never come back before they sign an update with the hub to close their VC. This could lead the hub needing to on-chain close “dust” channels that is costly. So we have to build slight alterations to the theory that seem to make these systems usable in practice. It’s not perfect and you’ll see some wobble around the edges from this type of monkey wrenching theory to actually work in practice. It’s still really neat and will work eventually when the kinks iron out.

---

**jfdelgad** (2018-11-06):

I can see this working with a central hub that is not different in terms of functionality than any other party in the system. There is a bidirectional channel between two users (the central hub is just another user that has connections to everyone). On this view the system looks rather simple and if this attracts a lot of attention there is little reason to ever close a channel with the central hub. Notice that this will work with ether, tokens and any kind of countable units that can be locked in a contract.

Finally, I think there would be space for several hubs and users can select to connect to the hub they prefer. The concern that I have is with fees, a single provider will have a tendency to abuse if it is realized that people need the service. We may think in collective, open initiatives where people fund a hub and they participate of the benefits of the fees, all this to allow for competition that may keep the fees under control.

In the system, none of this prevent people from creating their own channels and send ether or tokens with or without fees.

---

**rhlsthrm** (2019-01-04):

Hey [@adamskrodzki](/u/adamskrodzki), we at Connext have been working on a generalized implementation of exactly what you are describing. We collaborated closely with Spankchain to build their current payment channel hub (non-custodial version is live at [beta.spankchain.com](http://beta.spankchain.com)). We just open-sourced our code and are ready to start helping people integrate into their platforms.

We’d love to help you learn more and answer any questions you have.

https://github.com/ConnextProject/indra

---

**jtremback** (2019-01-07):

The benefits of a payment channel system that relies on a central hub are minor vs a traditional centralized payment processor. Just to be clear, I am speaking only about single-hub-based payment channels in this post, not multi-hub, or non-hub systems.

There are two real benefits, and one imagined benefit:

1. It is not possible for the hub to simply steal your money. However, the hub can still censor you indefinitely. Since the hub is “the only game in town”, its ability to censor you is equal to that of a completely centralized payment processor.
2. Payments are faster (this applies only to “virtual channel” systems). Payments between nodes do not need to go through the database of the hub. However, massively scalable centralized databases are a solved problem. Best to wait until you have those billion users before solving problems you don’t have.
3. (Imaginary benefit): The hub does not need to legally register as a payment processor. This benefit is probably imaginary, as the centralized hub is easily identifiable to the government and will need to comply with currency control laws, or anti money laundering, or whatever a given government likes to call it. An exception to this is perhaps any law around preventing theft of assets held by a payment processor, IF you can explain this to the regulators.

---

**nginnever** (2019-01-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/jtremback/48/2634_2.png) jtremback:

> It is not possible for the hub to simply steal your money.

From my understanding this has been the only benefit sought after by current implementers of centralized hubs.

![](https://ethresear.ch/user_avatar/ethresear.ch/jtremback/48/2634_2.png) jtremback:

> the hub can still censor you indefinitely.

This is why hub code is open source, a larger problem is the liquidity needed to make it easier for a competitor to stand up a hub in the event that one is censoring an application.

![](https://ethresear.ch/user_avatar/ethresear.ch/jtremback/48/2634_2.png) jtremback:

> IF you can explain this to the regulators.

Coincenter has been doing this already, I think it is a fairly easy argument for regulators to understand.

---

**adamskrodzki** (2019-01-08):

> censor you indefinitely … hub is “the only game in town”

It is not there will be many concurrent competetitors in with different network hubs, as today is VISA and MASTERCARD

and not indefiniteli since You can get Your money back on-chain and get Your funds back

> Payments are faster (this applies only to “virtual channel” systems). Payments between nodes do not need to go through the database of the hub.

Payments are faster since they do not need to go over blockchain the fact if they need to go over central hub database or not are irrelevant,

> (Imaginary benefit):

Can not recall anyone giving that argument before,

it is false mainly because capital requirements. Hub will need to stand loud in order to collect capital required for the solution.

In central hub payment channel the reuirement of capital lock on hub side is monopholy building force - Bigger hubs are better for every single user because of network effects. But to build big hub You need a lot of capital, so only few can exist

---

**jfdelgad** (2019-01-08):

The point about censorship is an important one. If the system is build focused on a central hub this can be prevented directly in the smart contract. If the system is more general and everyone could potentially be a central hub (note that any store could what to have a node to receive payments, or small communities would also be interested in having small central hubs, etc) then it would be difficult to control censorship.

All the other points described by jtremback are a bit forced. In particular I do not understand the payment processor part, the central hub do not receive funds from anyone, these will be in the smart contract of the main system.People are just storing funds in a contract, those funds are realesed when the users show a signed agreement between them, is there something I am missing?


*(5 more replies not shown)*
