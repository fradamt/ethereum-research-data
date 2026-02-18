---
source: ethresearch
topic_id: 1685
title: "Perun: virtual payment and state channel networks"
author: Perun
date: "2018-04-09"
category: Layer 2 > State channels
tags: []
url: https://ethresear.ch/t/perun-virtual-payment-and-state-channel-networks/1685
views: 14729
likes: 31
posts_count: 30
---

# Perun: virtual payment and state channel networks

We would like to introduce Perun – a protocol system for building virtual payment and state channel networks.

Perun is currently described in two academic research papers. A short description of these research papers and links to the pre-print versions are given below.

1. Perun: Virtual Payment Hubs over Cryptographic Currencies (http://eprint.iacr.org/2017/635)
Introduces the concept of channel virtualization as an alternative for routing payments via intermediaries using the hash-locked based transactions. The main advantage of channel virtualization is that once the virtual channel is established, payments can be carried out without interaction with the intermediary. This reduces fees and latency, while at the same time improving availability.
2. Foundations of state channel networks (https://eprint.iacr.org/2018/320).
Develops formal protocol specification for building state channel networks that have two main features: (i) our protocols allow to run arbitrary smart contracts off-chain, and (ii) we can support channel networks of any complexity (i.e., any number of intermediaries can be involved). Our state channel network supports full concurrency and use channel virtualization to minimize the need for interaction with intermediaries.

All our protocols are given in pseudocode and are proven secure in the universal composability framework commonly used in cryptography for analyzing the security of protocols. We would be happy to further work together closely with the Ethereum research community and improve our models and constructions. For us it would be helpful to receive further feedback on our approach – in particular whether the Ethereum community views formal security models (such as our UC modeling) for off-chain protocols as an important criteria for massive deployment of these technologies.

Best regards,

The Perun research team

## Replies

**vbuterin** (2018-04-10):

Excellent work!

Do you know any teams that are actually trying to build implementations of this?

> in particular whether the Ethereum community views formal security models (such as our UC modeling) for off-chain protocols as an important criteria for massive deployment of these technologies.

I definitely do think that we need some kind of general-purpose machinery for formally verifying properties of layer-2 systems in general, including both channels and plasma. We definitely have the intention of putting plasma contracts through a top-to-bottom formal verification process which checks both the model and that the code correctly implements the model and the right kind of process makes sense for state channel mechanisms as well.

In principle, I personally am satisfied that it’s fundamentally possible to achieve all of the things that you claim in the way that you’re doing it; the risk of error that worries me is closer to the implementation side (both smart contract code and daemon logic).

---

**ldct** (2018-04-10):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/p/839c29/48.png) Perun:

> in particular whether the Ethereum community views formal security models (such as our UC modeling) for off-chain protocols as an important criteria for massive deployment of these technologies.

Are UC-style ideal functionality specifications amenable to be used as specifications in formal verification? Ideally I would want a machine-checked proof that this sequence of EVM bytecode implements some specification written in a high-level formal specification language (for e.g., according to my hazy understanding, [@yhirai](/u/yhirai)’s work on Casper proves some theorems using (and specified in) Isabelle, and some other team is using a formal model of EVM semantics to verify the actual Casper contract bytecode that will be deployed).

---

**Perun** (2018-04-10):

> Do you know any teams that are actually trying to build implementations of this?

We are currently in contact with some companies that are interested in developing off-chain protocols. Unfortunately, currently we do not have the resources to do a full-fledged implementation but we are happy to contribute to them by, e.g., writing formal specifications, proving security of protocols, etc. This is also where our main expertise lies. That said, for the basic virtual payment channels, we made a highly non-optimized prototype implementation of the contracts in Solidity. The main purpose of this implementation was to estimate gas costs. Here is the link: [GitHub - PerunEthereum/Perun: Implementation of the Perun protocol](https://github.com/PerunEthereum/Perun).

> In principle, I personally am satisfied that it’s fundamentally possible to achieve all of the things that you claim in the way that you’re doing it; the risk of error that worries me is closer to the implementation side (both smart contract code and daemon logic).

Our modeling currently is at the abstract specification level only. This means it deals with logic errors due to, e.g., concurrency (which can be very tricky to get right) and also the composition of complex protocols. In fact, one of the main features of our modeling approach is that it enables us to give a rather modular specification and not one monolithic protocol that simultaneously has to deal with the vast number of special cases.

Of course, as you said our long term vision is to have fully verified code (hopefully even machine-checked) and reference implementations of the smart contracts and daemon logic. Before we move to this step however we first need to get the underlying protocol specification right – which turned out to be quite complex for these protocols. Indeed during the design we figured out many technical subtleties that we would not have noticed without a proof-driven design approach.

Such a bottom-up approach where we start with abstract protocol specification and then move to low level implementation is quite common in (cryptographic) protocol design. For instance, currently a “hot topic” in protocol design is to get fully-verified implementations of TLS. Also, there part of the process is to get the abstract protocol specification right and to find a modular design such that fully automated verification can be applied. We believe that one approach to designing secure off-chain protocols (payment/state channel networks, plasma, etc.) is to follow a similar path as these attempts.

---

**modong** (2018-04-10):

Fellow state channel researcher here. Great work on the specification of generalized state channel! We are working on a whole tech stack for state channel network and our work at the channel layer is very similar to yours.

I do want to bring up the discussion about the narrative of virtual channel across intermediaries. I think this narrative should not be promoted and encouraged to the developers.

First, every multi-hop payment, including HTL ones, are constructing and tearing down “virtual channels”. For HTL payments, a transient “virtual channel” is established whose resolution depends on the reveal of certain secret before certain timeout. For more complex off-chain applications, the lock up time is usually longer as the payments are usually conditionally depending on some other states but those states has not been finalized yet. To optimize the routing performance of the state channel network, for every mediated conditional payment, we should strive to lock up fund for as little time as possible. The multi-hop lockup of fund, IMHO, should be considered as last resort, not a feature. For example, in this A – Network – C topology, A and C are frequently transferring simple payments (not further dependency on other states) via the Network, they should trust and rely on the routing algorithm to deliver those payments for them instead of locking up resource in the network upfront by essentially provisioning a circuit and hurting any routing algorithm running on top. In fact, the locking up time is actually a very big adversary consideration for a routing layer algorithm that we developed.

Historically, this was why Internet routing switched from circuit switching to packet switching. The same argument holds, if not stronger, for state channel network where a stateful link model dictates. Again, there is nothing wrong about slow-resolving mediated transfer depending on further states. After all, this is the fundamental model of off-chain state channel application. But I am hoping that we could together promote the narrative of “you can do this when you have to”.

---

**Perun** (2018-04-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> Are UC-style ideal functionality specifications amenable to be used as specifications in formal verification? Ideally I would want a machine-checked proof that this sequence of EVM bytecode implements some specification written in a high-level formal specification language (for e.g., according to my hazy understanding, @yhirai’s work on Casper proves some theorems using (and specified in) Isabelle, and some other team is using a formal model of EVM semantics to verify the actual Casper contract bytecode that will be deployed).

Yes, ideally this is where we want to move eventually. But before we move to verifying the bytecode, we would probably start to do machine verification of our hand-written proofs. Already this is non-trivial, and probably needed before we start to verify bytecode.

---

**tomclose** (2018-04-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/modong/48/11445_2.png) modong:

> I do want to bring up the discussion about the narrative of virtual channel across intermediaries. I think this narrative should not be promoted and encouraged to the developers.

I understand your arguments about why HTL payments are superior to virtual channels for *payment* channels. I’m not sure I fully understand how the argument applies to general *state* channels though.

It seems to me that the HTL approach might not be possible for general state channels. For example, imagine that A and B are playing chess in a state channel for a prize of 2ETH. In order for this to be trustless, A and B must each have locked 1ETH at the beginning of the game, and those funds must remain locked throughout. In order for this to be supported across an intermediary, C, they too need to have their funds locked for the entirety of the game - across many state exchanges. If you want a framework capable of supporting general state channels, it seems like the HTL-per-state-exchange model breaks down, and you inevitably end up needing some sort of virtual channel. At this point, it seems like the virtual channel becomes a useful tool for developers, allowing them to abstract away whether their game is running in a direct channel or a virtual channel and focus on the game itself.

It might just be that I don’t understand how you intend to extend the HTL approach to general state updates. Are you able to explain this further?

---

**modong** (2018-04-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/tomclose/48/3252_2.png) tomclose:

> I understand your arguments about why HTL payments are superior to virtual channels for payment channels.

Sorry for the confusion. That is exactly my argument. IMHO, there will be two big classes of use cases for state channel networks: 1. pay-per-use; 2. generalized state channel. What I was saying is exactly that for the first use case, HTL per payment is better than provisioning circuits and we should promote that. The above comment was a gentle suggestion to not use simple payment channel as an example of generalized state channels and also not promote channel layer to do the job of routing layer with provisioned circuits.

![](https://ethresear.ch/user_avatar/ethresear.ch/tomclose/48/3252_2.png) tomclose:

> It seems to me that the HTL approach might not be possible for general state channels.

HTL payment is also just a specialized virtual channel (with a simple and “pre-compiled” boolean state transition resolution logic). One could build the HTL payment just like a generic state channel with more general boolean circuit “precompiles” or even lose it all together and build it completely using conditional dependency between on-chain verifiable states. In the case of more complex applications, multi-hop lockup for a certain timeout, which is the intended deadline for dependent states in that application to become available, is not avoidable. In general, any multi-hop relayed payments need to be carefully optimized with carefully designed mechanisms. We will release some research result on that front soon.

[edit: typos]

---

**yhirai** (2018-04-12):

I’m more comfortable in Dolev-Yao model of course ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=9)  I don’t know if anybody has done universal composability in any theorem provers.  That would be fun, given some excuse to work on that.

---

**choeppler** (2018-04-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Do you know any teams that are actually trying to build implementations of this?

Bosch is collaborating with the Perun Research Team and is just starting to implement this. We aim to contribute an initial version to the Ethereum Open Source Community within the next few months.

---

**homakov** (2018-04-12):

Do you mind to explain a gist of why virtual channel is better than hashlock approach? Lower funds lockup, lower dispute time or?

You would have to connect few channels in a network anyway, so most of the time you are paying to new users, not the same user so the market for direct user to user connection is neglectable.

---

**Perun** (2018-04-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/modong/48/11445_2.png) modong:

> I do want to bring up the discussion about the narrative of virtual channel across intermediaries. I think this narrative should not be promoted and encouraged to the developers.

Thank you all for the interest in our work!

Let us comment a bit on the points raised by Modong.

We agree that the need of blocking money by the intermediaries can be viewed as a disadvantage for some applications. For other applications, however, a bigger problem is the need to contact the intermediary for each microtransaction.  As an example consider paying for a wifi access charged 1 gwei per every chunk of 100 KB. Suppose the payments are routed via one intermediary Ingrid (say: the “operator” of the whole system). The HTL approach would require contacting Ingrid for each chunk of data which introduces huge communication burden. Perun does not have this problem. Other applications where we envision Perun is for devices with only near field communication. In this setting these devices can carry out payments between each other even when the intermediary Ingrid is not available. Perun also has the advantage that balance updates can still be carried out when the intermediary is unavailable due to network off-time.

One way to look at it is that Perun simply gives the users an opportunity to have a smooth tradeoff between the “communication” and “deposits”. For instance, in the wifi example above: the users could register (in the ledger channel) the virtual channel once per each 10 micropayments. This would mean an interaction with Ingrid (but not with the blockchain) is needed once per each 1 MB transferred, and her deposit needs to be 10 gwei.

We believe that Perun will in general be used when there are very few intermediaries (frequently: just one intermediary). Then, the “deposit” (compared to the HLT approach) is rather limited. The true cost of blocking money is hard to estimate, but it seems reasonable to assume that it has to correspond to the inflation on ether, which Vitalik once predicted to be around 2% per year at most (note that blocking the money in Perun is risk-free, so there will be no premium for the credit risk). This would correspond to 0.005% per day, or in other words 0.05 cent for each 10 dollars blocked for one day.  It’s actually an interesting question for the economists to provide a more scientific analysis of this.

Finally let us say in some cases one can get rid of deposits from the intermediaries, by switching to a weaker security model, where the intermediary can steal the money, but it becomes evident to everyone that he did it (see p. 15 of https://eprint.iacr.org/2017/635.pdf). We believe that it can make sense in cases when small amounts of money are at stake, and the intermediary has some established reputation.

Best,

The Perun research team

---

**ldct** (2018-04-13):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/p/839c29/48.png) Perun:

> For other applications, however, a bigger problem is the need to contact the intermediary for each microtransaction.  As an example consider paying for a wifi access charged 1 gwei per every chunk of 100 KB.

Agree that this is how I personally see the tradeoff between HTL-style routing and “virtual channel” style routing (without considering for now the intermediate points on this spectrum that was brought up). Worth noting that the cost is not just communication, but that if you reuse an intermediary in HTL-style routing, there is the potential cost in terms of griefing / censorship. E.g., assuming the only available route for A to pay B is A-X-B then X can selectively route payments; in “virtual channel” style routing X can commit to locking up funds for 10 days and for that length of time, A and B can do whatever they want and X cannot stop them, but this seems impossible to do with HTL payments.

Also worth noting that the term “HTL per payment” covers more than one solution, eg Sprites also uses HTL but a different (IMO strictly superior) kind that Lightning-style HTL.

---

**homakov** (2018-04-13):

Maybe you can help to comprehend how virtual channels work and what’s the benefit over hashlocks? I have read the paper real quick and for what sounds like a simple concept it is exaggerated.

When can virtual channels be applied and why would I want to avoid an intermediary with hashlocks when the payment is already offchain, there’s no overhead to worry about going through someone?

---

**tomclose** (2018-04-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/homakov/48/1171_2.png) homakov:

> When can virtual channels be applied and why would I want to avoid an intermediary with hashlocks when the payment is already offchain, there’s no overhead to worry about going through someone?

One way of thinking about the difference here is to think about the compensation involved. Even though you’re not incurring on-chain transaction fees, off-chain transactions aren’t completely free: A’s payment to B through C requires C to have some money staked on-chain, and so C should be compensated for that (for an amount that’s less than the on-chain transaction fee, otherwise the state channel wouldn’t be beneficial…).

Hashlocks are a pay-per-message pricing model. Every message needs to be routed through the network, and each node it passes through will require a fee for that. In a telecoms analogy, hashlocks are like text messages, where you pay per text.

Virtual channels are a line-rental pricing model. You set up a connection to your counterparty and pay the intermediaries for the time they keep that connection open. While you have the connection open you can send as many messages down it as you want. In the telecoms analogy, virtual channels are like phone calls, where you pay per minute.

Virtual channels are exciting because they enable a different pricing model - one that will be more suited to some applications. They’re also exciting because they allow more general applications; to extend the analogy: if you have a modem, you can stream video over your phone call, but you’d have a tough time doing that by transmitting the data via text.

---

**homakov** (2018-04-14):

That’s a great answer, I now understand on a higher level the cases when virtual channel is better suited. Theoretically speaking a-b could exchange a ton of micropayments via virtual channel and pay less fee than doing that through c with hashlocks.

But what I still don’t get is the mechanics of this idea. How exactly virtual channel is started and used? The hashlock is an “amendment” of the balance proof, which can be enforced onchain, so I guess the channel is also a new amendment for balance proof? I tried to dig https://github.com/PerunEthereum/Perun but got lost in VC_LC_ namings

---

**Perun** (2018-04-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/homakov/48/1171_2.png) homakov:

> But what I still don’t get is the mechanics of this idea. How exactly virtual channel is started and used? The hashlock is an “amendment” of the balance proof, which can be enforced onchain, so I guess the channel is also a new amendment for balance proof? I tried to dig GitHub - PerunEthereum/Perun: Implementation of the Perun protocol but got lost in VC_LC_ namings

You may find further information on our web-page: https://perun.network. There you may also find a non-technical high-level summary of our results.

For a full description of our protocols we suggest to take a look into our whitepapers. They contain the most up-to-date description of Perun. The current version of the source codes are not intended for studying our construction but where only done to estimate the gas costs on Ethereum. We hope to improve the implementation in the future.

In case there are further questions, just let us know. We will try to clarify.

---

**modong** (2018-04-14):

> Virtual channels are a line-rental pricing model

I think the pricing model and the mechanisms of payment transfer can and should be completely decoupled. Even in HTL model, end user can subscribe to services with its payment service provider(s) with any sort of subscription model (monthly, capacity based and etc). Virtual Channel can also use subscription model and if we are thinking about analogy, virtual channel is like provisioned MPLS tunnels where HTL is like Internet users’ model.

---

**ldct** (2018-04-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/modong/48/11445_2.png) modong:

> Even in HTL model, end user can subscribe to services with its payment service provider(s) with any sort of subscription model (monthly, capacity based and etc).

Can this be done trustlessly but with the same capital efficiency characteristics as charging per-payment HTL?

---

**modong** (2018-04-16):

> Can this be done trustlessly but with the same capital efficiency characteristics as charging per-payment HTL?

I think it can. Imagine one can setup a SLA proof contract (virtual) with the service provider, with SLA proof decoding and verification logic written in that contract. SLA proof can be some compact proof regarding whether service provider has met promised SLA (e.g. the maximal amount of outgoing payment relayed, the speed of relay (x ETH / day)). SLA proof design itself can be an interesting question, but simple ones definitely should work. In the beginning of a service period, a conditional state transition (in this case payment) should be initiated from the client to the service provider with a conditional dependency on the SLA being fulfilled. During the service period, if everyone is cooperative, the SLA contract can resolve to true on state satisfaction query before condition timeout and therefore the conditional payment will be “unlocked” to unconditional. Of course, all of the above will happen off chain. However, if one party trying to be malicious, dispute can be carried out on chain regarding the state of the SLA proof contract. Often times, dispute on SLA will also couple with dispute or “disconnect” of the actual state channel with deposits. However, in the case of “honest mistake” (communication outage), business can carry with state recovery primitives.

---

**modong** (2018-04-16):

And wearing the hat of promoter for generalized state channels, pay-per-hop can also be viewed as “pre-compiled” SLA resolution, where per payment fee is depending on the SLA of “deliver my payment to destination”.


*(9 more replies not shown)*
