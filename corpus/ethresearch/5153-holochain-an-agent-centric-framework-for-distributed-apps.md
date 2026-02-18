---
source: ethresearch
topic_id: 5153
title: "Holochain: an agent-centric framework for distributed apps"
author: jamesray1
date: "2019-03-14"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/holochain-an-agent-centric-framework-for-distributed-apps/5153
views: 10765
likes: 44
posts_count: 43
---

# Holochain: an agent-centric framework for distributed apps

[Holochain](https://holochain.org/) is a framework for distributed apps that has an agent-centric approach. My initial impression of it after browsing its website, reading some of the white paper, some of the [FAQs](https://developer.holochain.org/guide/latest/faq.html), and [this blog post on mutual credit cryptocurrencies](https://medium.com/holochain/beyond-blockchain-simple-scalable-cryptocurrencies-1eb7aebac6ae), is that it looks better than Ethereum, providing a simpler, more intuitive approach to solving the scalability problem without compromising the scalability-decentralization-throughput trilemma, unless you really need universal consensus / data as an absolute truth, rather than data as a shared perspective, which corresponds to being able to use fiat currencies or tokens, including crypto fiat currencies like ETH and all other blockchain currencies, or tokens pegged to national fiat currencies or other assets.

I made a post about Holochain previously, but it was deleted due to being too spammy, so this is another one.

## Replies

**virgil** (2019-03-14):

Yeah.  The post was noise.  This post is noise too, but less so than your previous post.

---

**fubuloubu** (2019-03-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> unless you really need universal consensus / data as an absolute truth, rather than data as a shared perspective.

I think it’s a very interesting framework, but I wish they were more up front about this exact point.

You can’t build incentives on subjectivity. This framework doesn’t solve the double-spend problem without the addition of centralized coordinator nodes, which makes it a terrible solution for coordinating things like decentralized identifiers and currencies. In their “decentralized Twitter” example, this means you can build 99% of what Twitter does on their framework… *Except* for handles! (I mean, you could do it, but you risk splitting the network in extreme cases due to subjectivity)

If they took that out, it would actually be a really interesting alternative as a “p2p application framework”, leveraging things like Ethereum only for consensus-critical items like DIDs and tokens, etc. They could get rid of the ugly bits like the coordinator boxes they’re selling and the token, and stick to the truly innovative design model they’ve created. It actually solves some privacy things too!

Unfortunately, that’s not how you raise money in blockchain, hence the token ![:man_shrugging:](https://ethresear.ch/images/emoji/facebook_messenger/man_shrugging.png?v=12)

---

TL;DR: not an “Ethereum killer”, more Ethereum-complementary

---

**jamesray1** (2019-03-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/fubuloubu/48/2424_2.png) fubuloubu:

> This framework doesn’t solve the double-spend problem

Did you read about the mutual cryptocurrency design at [Beyond Blockchain: Simple Scalable Cryptocurrencies | by Arthur Brock | Holochain | Medium](https://medium.com/holochain/beyond-blockchain-simple-scalable-cryptocurrencies-1eb7aebac6ae)? What did you think of it?

---

**fubuloubu** (2019-03-15):

Quote from the author:

> We are not building a currency. We ARE building a platform for the decentralized evolution, deployment, and operation of many currencies and other distributed applications.

Where did HOT come from then?

---

The mutual credit concept is pretty fascinating, and that concept I believe may scale well for app-specific reputational currencies (something I didn’t think about before), as they already have problems with sybil attacks that I don’t believe this model solves in a satisfactory manner (other then “let the community decide”, which is fine for a reputational token).

Mutual credit doesn’t scale well. It relies on community trust models to work, which is a very difficult problem to solve without an anti-sybil mechanism. Holochain’s solution to this is to make central coordinator nodes available so as to corral the system and ensure that new HOT doesn’t get created out of thin air, which the author notes is a possibility. The system doesn’t work in an adversarial environment, which is fine for 99% of applications in the modern world, but I don’t believe a valuable currency is one of them. I would also tend to put other economically valuable items in this same bucket, such as a DNS names, centralized identifiers such as handles, stocks/bonds/etc.

I’ll make an effort to read through this again as it’s very dense, so I might be missing something. I like the fact that it was written before Holochain was a cryptocurrency on the market though, hopefully marketing didn’t affect the original text too much.

---

**fubuloubu** (2019-03-15):

I’d also like to note that it is important to discuss alternative frameworks in this research channel as it could give us good ideas to model changes to Ethereum. I don’t think this post is spammy as long as we discuss the true pros and cons of the frameworks, and figure out what are good ideas to incorporate and what are just alternatives that don’t add value to our particular design ideology (censorship-resistance, high security, adversarial env, etc.)

---

**jamesray1** (2019-03-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/fubuloubu/48/2424_2.png) fubuloubu:

> Holochain’s solution to this is to make central coordinator nodes available so as to corral the system and ensure that new HOT doesn’t get created out of thin air

I’m not sure if the hawaladars/coordinator nodes are more centralised than validators in Ethereum; I haven’t finish reading through docs like the Holochain white paper yet.

---

**Theybrooks** (2019-03-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/fubuloubu/48/2424_2.png) fubuloubu:

> This framework doesn’t solve the double-spend problem without the addition of centralized coordinator nodes

Are you referring to the “notaries” mentioned in the article [@jamesray1](/u/jamesray1) cited? I would just point out that this article is nearly 3 years old now and the approach has evolved since then.

The way holo fuel is designed now, all participants in the network act as notaries. There is no centralized coordinator. For every transaction, a random set of validator devices is recruited to perform validation, randomness being based on the similarity of their public key hashes to the hash of the data being shared.

The framework itself does not specify how each app should address potential collisions in the DHT. App developers will need to decide that for themselves. In the twitter example you gave, if a collision is detected, say, if two users choose the same handle at the same time (i.e., before either user’s choice has fully propagated in the DHT), you could code it so the name goes up for auction to the highest bidder, or a message is sent to both users with a release code and they can discuss who wants it more and activate the release code for the other, or if you have a reputation currency, you could give it to the one with higher reputation, or take the median timestamp from the network validations (kind of like how Hashgraph works) and give it to the “first” person to choose the handle by that metric, or etc. etc. Part of the point is to NOT dictate a one-size-fits all consensus mechanism for every situation, but to allow it to be flexible. (I got these examples from listening to [this interview with Arthur Brock](https://www.stitcher.com/podcast/crypto-radio/e/56696347))

![](https://ethresear.ch/user_avatar/ethresear.ch/fubuloubu/48/2424_2.png) fubuloubu:

> They could get rid of the ugly bits like the coordinator boxes they’re selling

Those boxes aren’t “coordinator” boxes. I think you’re (understandably) confusing Holochain and Holo, which are two different (but related) things.

![](https://ethresear.ch/user_avatar/ethresear.ch/fubuloubu/48/2424_2.png) fubuloubu:

> Where did HOT come from then?

Yeah, HOT is not Holochain’s “native” currency. Holochain itself is just a free, open-source framework for building distributed applications, which do not necessarily require any kind of currency to function. HOT was the fundraising token for Holo, the distributed web-hosting application built on Holochain, which will be redeemed 1:1 for the mutual credit currency, Holo fuel, when Holo launches.

Full disclosure, I’ve been volunteering in the Holo/Holochain community for about a year, and am new to this forum (just found this discussion trawling the web).

---

**fubuloubu** (2019-03-15):

You literally have to buy them from holochain, it’s not “trustless participation”

---

**fubuloubu** (2019-03-15):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/cdc98d/48.png) Theybrooks:

> The way holo fuel is designed now, all participants in the network act as notaries. There is no centralized coordinator.

This was my understanding from a few months ago when I met the creator in person.

---

**Theybrooks** (2019-03-15):

Are you still referring to the Holoports? They will be releasing the hosting app for anyone to download and run on any machine. You don’t need to buy anything from anyone, and again you are confusing Holochain with Holo. “Holochain” doesn’t sell anything.

---

**fubuloubu** (2019-03-15):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/cdc98d/48.png) Theybrooks:

> confusing Holochain with Holo

Weird distinction to make if they’re both the same people, but I guess if that’s true I have no issues with Holochain and only with Holo!

I still claim that Holochain and Ethereum solve fundamentally different problems (although the original crowdsale Ethereum’s promise of a “decentralized application platform” it makes more sense to compare them together)

I guess cryptocurrencies are just confusing and can’t make up their minds what they are! ![:rofl:](https://ethresear.ch/images/emoji/facebook_messenger/rofl.png?v=12)

---

**fubuloubu** (2019-03-15):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/cdc98d/48.png) Theybrooks:

> HOT was the fundraising token for Holo … will be redeemed 1:1 for the mutual credit currency,

I still claim that you can’t have a mutual credit currency without central coordinators to make sure double-spends don’t happen.

---

**Theybrooks** (2019-03-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/fubuloubu/48/2424_2.png) fubuloubu:

> Weird distinction to make if they’re both the same people, but I guess if that’s true I have no issues with Holochain and only with Holo!

Yes it’s certainly a common confusion, but the difference is that Holochain is the framework, and Holo is just one app. It’s sort of like the difference between blockchain and Ethereum, except if Vitalik et al. had also invented the concept of blockchain in the first place ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/fubuloubu/48/2424_2.png) fubuloubu:

> I still claim that you can’t have a mutual credit currency without central coordinators to make sure double-spends don’t happen.

Is your primary concern with sybil protection? Also I’m wondering how you are understanding what “mutual credit” is. I want to make sure we’re on the same page on that, because otherwise we might get confused.

Holo will indeed be relying on third-party KYC identity verification for hosts (who can create currency up to a credit limit determined by a demonstrated history of hosting services, as part of the elastic currency supply in the mutual credit design). Otherwise I’m curious what other kind of problem you could see with the validation model? If someone tried to double-spend, they would fork their own hash chain, which would be detected by peers in the validation process. A time delay of at most a couple minutes would be needed to ensure any previous transactions have been fully propogated in the DHT.

---

**fubuloubu** (2019-03-15):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/cdc98d/48.png) Theybrooks:

> Is your primary concern with sybil protection

Basically. I am deeply interested in reputation systems, and mutual credit (at least from my introduction to it in that article) seems to rely on reputation to function correctly. Not a bad system, but it’s fragile at scale as most human societies and the internet prove pretty sufficiently. I will definitely learn more about it, but there’s a reason why no major economy runs on mutual credit systems… we don’t trust each other when money is involved! (mostly because we do bad things to each other when profit is at stake)

---

**Theybrooks** (2019-03-15):

I think you’ll enjoy the Holochain/Metacurrency rabbit hole. It’s quite a deep one!

---

**jamesray1** (2019-03-15):

Welcome to ethresear.ch! I do intend to look more into Holochain but need to prioritize getting a job, which may include working on an ~~startup~~ idea to [incentivize waste reduction](https://iwr-wasteless.github.io/iwr/) along with a part-time job.

---

**jamesray1** (2019-03-27):

AIUI, Holochain and its mutual credit currency can’t be used for any economic activity, unlike Ethereum and Ether. Indeed, https://holochain.org lists apps that it helps. From https://developer.holochain.org/guide/latest/faq.html#what-kind-of-projects-is-holochain-good-for: “Fiat currencies where tokens are thought to exist independent of accountability by agents are more challenging to implement on holochains.”

---

Edited section May 14:

I’d edit the top post with this but I can’t:

Holochain pros:

- unlimited scalability
- doesn’t enforce universal consensus when every use case can do without it. Mutual and reputational credit can be used for transactions rather than fiat cryptocurrencies or tokens. You should be able to implement a blockchain as a Holochain happ, but again, this isn’t necessary. Fiat currencies (including cryptocurrencies) have inherent centralization with the stakeholders controlling the currency, e.g. developers, miners, stakers, validators; although this could be mitigated with a DAO, but then governance of the DAO can be complicated and there hasn’t been a secure demonstration yet.
- You can build a full (stack) happ on Holochain, rather than just a smart contract. This allows all of the code, state and data for the happ to be decentralized, rather than only hosting some code e.g. on GitHub servers, plus the developers, testers, and early-adopters who host it on their local machines. If there is a fork in a node in one line of code, that node gets rejected by validators and must fork to its own happ to continue operating independently, or sync with the existing happ.

Cons:

- rather than using consensus, mutual and reputational credit, if used to transact, hinges on KYC. But perhaps using KYC isn’t such a bad thing, and you could potentially have a web-of-trust like mechanism (a la KILT) to decentralise the KYC and trust, and also enable the ability to revoke trust from any entity at any time. Additionally, if you don’t need to transact currencies, and just transfer data, then Holochain, Secure Scuttlebutt, and Dat Protocol are more suitable than blockchains, with Holochain having the above advantages. Not enforcing universal consensus is what enables unlimited scalability.

As quoted above:

> I’m not going to create another account and get involved with another conversation. I would like to point out that I see a criticism about the centralized aspect of Holo that appears to show lack of understanding of Holochain. Unless I don’t have the full context of the conversation.
> Yes Holo is partially centralized. They admit that. That is the cost of creating mass adoption. Until people evolve to using pure Holochain. Don’t like KYC, they only run Holochain and require all your users to install it.
> Blockchainers live in this future where everyone wants to do anonymous transactions because they don’t trust the “powers that be.”
> Holochainers live in a future where they care about the people they transact with.
> —lifesmyth

Me:

> AIUI, to do mutual credit with Holo is one way, requiring KYC. But AFAIK there is no decentralized, sybil-resistant approach that does not involve consensus or a blockchain approach, in order to avoid invalid transactions such as double-spending.

pauldaoust:

> re:
>
>
>
> But AFAIK there is no decentralized, sybil-resistant approach that does not involve consensus or a blockchain approach

I’d further qualify your list of adjectives by adding ‘anonymous’ – because there is one very good decentralised, Sybil-resistant approach that doesn’t require PoW/PoS/etc, and that’s KYC – or at least some sort of human identification approach that all the participants in the system are comfortable with, which may in fact permit pseudonymity if you design it right. Connecting accounts with humans, whether those humans reveal their IRL identities or not, is by definition Sybil-resistant.

I’d further qualify your list of adjectives by adding ‘anonymous’ – because there is one very good decentralised, Sybil-resistant approach that doesn’t require PoW/PoS/etc, and that’s KYC – or at least some sort of human identification approach that all the participants in the system are comfortable with, which may in fact permit pseudonymity if you design it right. Connecting accounts with humans, whether those humans reveal their IRL identities or not, is by definition Sybil-resistant.

It’s also useful to talk about the consequences of Sybil attacks for a given distributed system. For a global ledger, the consequence is of course that the Sybils can control what goes into the ledger. (Hence the very clever but wasteful remedy, proof of work.)

For a Holochain network, the risks are different. You’ll never get enough Sybils in a given neighbourhood to completely push out the possibility of one honest neighbour who blows the whistle on them all. They can choose not to talk to that neighbour, but they can’t force the rest of the network to do the same. As far as I can tell, the only thing that Sybils can do in a Holochain network are:

- ‘ruin the party’ – that is, issue spurious warrants, fail to store or pass on data, etc, in order to make all the honest nodes work really hard to do the sort of data validation that should be done automatically.
- mount an ‘eclipse attack’ – this is when an honest node is completely surrounded by dishonest peers.
We’re thinking about both issues, of course.
—Holo

There’s more discussion on Sybil attack resistance at [Holo](https://chat.holochain.org/appsup/pl/nx56wg6amfgg8bmwj34pdhhwze) (it goes over two days to Apr 16).

---

**jamesray1** (2019-03-27):

~~Agreed, this is a major drawback that apparently makes it impractical for Holochain to integrate with the modern economy and scale. It is a very hard problem to proof against Sybil attacks in a reputation network and AFAIK no method has been proven to do so.~~ I’m not sure about this, more research and thought is needed.

---

**MightyAlex200** (2019-03-27):

Actually, it’s not the reputation of the people exchanging credit that matters, but the reputation of the notaries. Just a single notary acting in good faith can stop an invalid transaction from going through. A good reputation system or a very strong application membrane should be able to keep the majority of notaries signing any given transaction as an honest actor.

Even if there is an unreasonably high chance of choosing a dishonest notary by whichever metric the currency chooses (i.e. purely random or random but weighted by reputation) at 30%, it would still take less than 150 notaries per transaction to have a lower chance of accepting an invalid transaction than the chance of two 256-bit hashes colliding.

Here is my math:

b^n < 2^{-256}

Where b is the chance of picking a dishonest notary, n is the amount of notaries we are picking per transaction. (and 2^{-256} is the chance that some random 256-bit number is equal to some other random 256-bit number)

And even such a number as 10%, where only 78 notary entries are required for the same effect, may be a gross overestimation of the possibility of attacks, given that any effective reputation system would completely (or mostly) invalidate an agent’s reputation if they were to validate two competing notary entries (these entries are stored on a hashchain, keeping the chain linear would reveal the conflicting data, but splitting the chain is not allowed, and is protected by a very similar system to the one just described).

---

**jamesray1** (2019-04-12):

Here’s some thinking about Holochain mutual and reputational credit: https://medium.com/@james.ray/holochain-economics-671ef4a66974 with a brief comparison to alternatives.


*(22 more replies not shown)*
