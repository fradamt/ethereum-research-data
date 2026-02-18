---
source: ethresearch
topic_id: 1239
title: Incentives for running full Ethereum nodes
author: jpitts
date: "2018-02-27"
category: Economics
tags: []
url: https://ethresear.ch/t/incentives-for-running-full-ethereum-nodes/1239
views: 22919
likes: 68
posts_count: 42
---

# Incentives for running full Ethereum nodes

This has to do with a concern voiced by Micah Zoltu that the community’s node implementations are not creating an optimal “node running experience”, potentially lowering the number of full nodes and leading to centralization risks.

He indicates that this may be the result of incentive mis-alignment for those developing implementations, leading to the sub-optimal prioritization.

Copied from a series of comments made by Micah Zoltu in the [ethereum/research](https://gitter.im/ethereum/research) gitter channel:

> ETH incentives to run the user agent
>
>
> I’m concerned that Ethereum node build quality is becoming more and more of a problem that is going to lead to centralization. As a user, I have tried using both Geth and Parity, but both of them have their own set of problems that result in me spending an increasing amount of time dealing with them. I, in general, can’t just “run a node in the background” on my desktop, I have to constantly be doing operations works to keep the thing on. While this is personal experience, in speaking with other developers and users, the sentiment is generally the same. Running a full node is a bunch of headache. I am very rapidly finding myself considering switching away from running a full node to just using a centralized node provider like QuikNode or Infura.
>
>
> I worry that this is going to lead to centralization risks over time as running a node is not about just having some free computing resources, but also being willing to dedicate time to operations work (along with knowing how to do that operations work.
>
>
> I, unfortunately, don’t have a great solution for this problem though I do think the fact that there is no clear business model for client developers is certainly a big part of the problem. While the various clients do have funding, that funding isn’t predicated on building a competitive product that attracts users. Thus, similar to government work, there isn’t a strong incentive to build something that actively incites people to use it, you just have to build something that is “good enough to pass muster with the people funding you”.
>
>
> Now don’t get me wrong, I do think that everyone working on clients right now cares greatly about Ethereum and wants the platform to succeed and they are trying to build something good.
>
>
> However, due to the incentive mis-alignment I don’t believe any of the clients have, for example, a product manager that is doing user-research to find out what features users want (not just the dev team) and then prioritizing those features along with others. Instead, I believe both teams are run more like open source shops where the dev team fixes/builds what they want or think is most important, which may not align with what end-users actually want.
>
>
> For example, as an end user what I want is to not have to do operations work. I care significantly less about getting a 3% CPU reduction or 100% disk utilization reduction (even though these things are useful to me, they don’t have as much impact as the thing “just working”).
>
>
> I suspect (I could be wrong) that if there was a product manager doing user research, user testing, data analytics, etc. we would see that I’m not the only one that wants their Ethereum node to “just work”.
>
>
> A number of developers and end-users I know have stopped running full nodes of their own for this reason (too much operational headache) and this trend worries me as currently (Proof of Work) Ethereum’s security model is dependent on decentralization of full nodes (as well as miners, but that is a separate topic).
>
>
> License: CC0

## Replies

**MicahZoltu** (2018-02-27):

After typing that rant up, I thought more about the problem and I have since become even more concerned that there is an incentive misalignment here, which leads to an unstable equilibrium long term.  Rather than focusing on the specific concerns about operational overhead of running a client, I would prefer to focus on the concern of lack of incentives to building a client.

I’m curious what people’s thoughts are on user-agent incentivization?  I recognize that it isn’t game theoretically fool proof, though I somewhat suspect that in the real world it may be “good enough” and think it is “notably better than the current situation with no incentives”.

---

**jamesray1** (2018-02-27):

[Here](https://gitter.im/ethereum/research?at=5a90e70ba2194eb80da6fc4a) is a permalink for the comment.

Regarding incentives for clients and their business model, [I spoke to Afri Schoeden and found out that Parity is funded via VCs and isn’t charging any fees](https://gitter.im/paritytech/parity?at=5a5cbda01dcb91f1775211e0). I guess that one reason VCs (or anyone) might invest in a client, even if the client doesn’t generate any revenue (except for maybe conferences and donations), is that the client is an enabler for the Ethereum ecosystem, thus allowing investors to gain access to new portfolio opportunities.

Re user incentives, if the client is free to use, that is a start, but I agree that since full nodes are providing value to the network, there should be incentives to run a full node. Hopefully with PoS it will be easier to join a staking pool, provided that one can run a full node, but that is a big proviso.

---

**MicahZoltu** (2018-02-27):

One thought (that would need more research) would be to make it so that when a client signs a transaction, it (optionally?) attaches a user agent to the signature. This would result in some sort of reward going to the author of that user agent when the transaction was processed (similar to mining rewards). I recognize that there are a bunch of economic caveats/gotchas with this idea, but I wanted to throw it out there as a starting point for “how can we incentivize people building Ethereum clients and running things as a business?”

The first most obvious caveat is that end-users would be incentivized to put an address of their own down as the user agent. My initial thinking on this is that there are few enough users advanced enough to run a custom client so the losses there would be minimal, and client developers are incentivized to not make the user agent string configurable because it is how they get paid. Also, presumably the per-transaction user-agent fee would be small enough such that the average user probably won’t care enough to hack their client to change it (or even switch clients to one that lets the user customize the user agent), usability and simplicity matter more to most. There is a concern that most transactions are coming in through third party Ethereum nodes like Infura or QuikNode and they have incentive and capability to change the user agent.

I’m tempted to suggest “lets wait and see if user-agent spoofing becomes a meaningful problem before trying to fix it”, since the worst it can do is put is right back where we are now with no incentives for client development.

Something to consider is that the user agent fee could be used to bribe miners by putting the miner address in instead. Once again, I’m tempted to try it out first (unless someone has better ideas) and see how things go because it is a very high coordination cost to actually bribe miners via user agent (since you don’t know who will mine the block your transaction ends up in), and there is no common infrastructure/protocol for broadcasting different transactions to different miners.

---

**MicahZoltu** (2018-02-27):

My concern with the “people wanting to make the ecosystem better to improve the ETH value proposition this driving eth prices up” doesn’t scale particularly well IMO, nor does it foster competition for customers which I think is critical to product development.  I’m worried that it will be very easy to reach a local maxima, and there is little incentive for new competitors to enter the market.

As a personal example, I have considered building as Ethereum client but decided against it because there was no profit incentive for me to enter the market.

---

**vbuterin** (2018-02-27):

> One thought (that would need more research) would be to make it so that when a client signs a transaction, it (optionally?) attaches a user agent to the signature. This would result in some sort of reward going to the author of that user agent when the transaction was processed (similar to mining rewards). I recognize that there are a bunch of economic caveats/gotchas with this idea, but I wanted to throw it out there as a starting point for “how can we incentivize people building Ethereum clients and running things as a business?”
> The first most obvious caveat is that end-users would be incentivized to put an address of their own down as the user agent. My initial thinking on this is that there are few enough users advanced enough to run a custom client so the losses there would be minimal, and client developers are incentivized to not make the user agent string configurable because it is how they get paid. Also, presumably the per-transaction user-agent fee would be small enough such that the average user probably won’t care enough to hack their client to change it (or even switch clients to one that lets the user customize the user agent), usability and simplicity matter more to most. There is a concern that most transactions are coming in through third party Ethereum nodes like Infura or QuikNode and they have incentive and capability to change the user agent.

This seems like you’re just suggesting the idea of creating a client that charges users for every transactions they send with it, and hoping that most users don’t change the default (they quite possibly won’t if the fee is significantly less than the miner fee). That seems reasonable to me if users are willing to accept it. Another approach would be for the developers of the client to run their own light client servers, and have a light client protocol that uses channel payments to these servers to get information (eg. receipts) faster. There are plenty of microscopic goodies that you can provide and charge for of this form.

---

**jamesray1** (2018-02-27):

Grid+ uses agents, so I think they would be interested in this topic. [@alex-miller-0](/u/alex-miller-0).

It would be good to get opinions from client developers, e.g. Afri Schoeden, Péter Szilágyi (their tags don’t come up on this site), [@axic](/u/axic) and [@gumbo](/u/gumbo).

---

**jamesray1** (2018-02-27):

As someone whose learning and planning on developing a stateless sharding implementation for Parity, I would be interested to know ways to generate revenue and profit for making not just maintenance changes, performance improvements, feature enhancements, UX improvements, and more development and operational tasks, but also implementing what comes out of Ethereum research. Of course there is the grant program but that is not intended to fully support a business. Having a token isn’t sufficient, you need an incentive for people to buy the token and for it to increase in price, e.g. fees or rewards for different things like as mentioned with fees for transactions, channel payments to light client servers, and rewards for full nodes verifying transactions.

---

**jamesray1** (2018-02-27):

Additionally if clients generate a profit then some of it could be used to fund research, as has been discussed here: [Using ICOs to fund science](https://ethresear.ch/t/using-icos-to-fund-science/920).

---

**FrankSzendzielarz** (2018-02-27):

For what it is worth, I have started down the path of implementing my own light client in .NET and the biggest hurdle I have faced so far is documentation.

To be clear, I am a software engineer who until now has only really been a user of pre-built crypto libraries. Entering the crypto space obviously meant I had to realign my skills and learn something. (That is part of the incentive actually for me personally to dive in head first. ) However a lot of what needs to be learnt is very obscure. For example, it took me an eternity just to work out what ‘v’ meant in an r,s,v format signature, and how exactly to implement it. Another example was trying to work out the significance of the Kademlia implementation and to what extent it was important, how it all fits in. Yet another example is the Discovery v5 roadmap and if/when to focus on that. Etc.

I guess a Steve Ballmer style “Developers!Developers!Developers!” call to action and the supporting material could bring new talent and new approaches that help address some of the hurdles. Maybe even new dedicated hardware, such as Merkle-trie friendly hardware storage etc. (Just guessing) Making this stuff more accessible could bring more fresh creativity into the whole thing.

Me personally, developing and maintaining a [proprietary, maybe] client is just a personal challenge with the resulting opportunity of realising some business plans I have in mind, when I get it done. So far that challenge has been pretty tough!

---

**kladkogex** (2018-02-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/jpitts/48/877_2.png) jpitts:

> ETH incentives to run the user agent
>
>
> I’m concerned that Ethereum node build quality is becoming more and more of a problem that is going to lead to centralization.

I think the core of the problem is PoW definition - miners get paid huge amounts of money for doing useless computations, and people that do useful computations such as verificaton of smart contracts get zero.

IMHO in a perfect network smart contract verification would be the POW itself.

A network like this  would be totally symmetric - there would be no miners and non-miners, everyone would be creating blocks and making money. People would get paid for doing useful work, namely, verifying blocks and smart contracts.

A node would receive a block, perform computations to verify it, and then create some kind of a PoVC (proof of verification computation).

Then the node would be entitled to propose the next block and claim block creation bounty, if the hash h = SHA3(PoVC || NODE_PUBLIC_KEY)  is smaller than a certain number C). In case of a fork, a block with smaller h would win.

The system described above would work perfectly in a sense that every node would be paid fairly and there would be no miners and no electricity waste.

The real issue cryptographically is how to design a secure PoVC algorithm, namely how to prove that verification computations were done by the node and not just copied from another node. There is probably a way to do it …

One simple way would be to require the node that proposes a block to send out intentionally modified blocks from time to time to particular nodes to test that they perform verification computations and not just copy others. More advanced solutions could probably use homomorphic encryption, SNARK etc …

When Ethereum switches to pure PoS, it may be that implementing this PoVC system could make sense in some hybrid way, for instance some of the bounties can go into staking and some into PoVC

---

**AlexeyAkhunov** (2018-02-27):

> @kladkogex
> IMHO in a perfect network smart contract verification would be the POW itself.

That is a very interesting idea indeed. One approach to explore could be that PoW could be a gradual compression of the blockchain using something like STARKs (it is very resource intensive computation to produce a STARK proof, but not very intensive to verify it). Perhaps there is a huge number of ways to compress the computation embedded in the past blocks, and most of them could be applied independently, so that rewards can be distributed more evenly across the network.

---

**kladkogex** (2018-02-27):

Interesting - this is a great idea !

You could compile from source code to EVM code to logical gates (like they do for chip design).

At the logical gates (STARK) level there at many ways to optimize in a unique way as Alexei suggets …

---

**rphmeier** (2018-02-27):

[@vbuterin](/u/vbuterin)

> have a light client protocol that uses channel payments to these servers to get information

So this is definitely the end-game for the light client protocols under development, but the problem so far has been that it’s very difficult to prove to a light client that you have collateral locked in a state channel without the light client having synced – but it would be a lot better if servers didn’t have to give out headers for free so clients can sync.

There are are a few tricks like having servers lock up funds for a long time in a special contract and using blind signatures to allow a light client to safely open a state channel at the head of the chain as soon as it has seen that block in the history. It still requires headers to be given out up to that point, but ideally with hardcoded light-client checkpoints, a finalizing consensus engine, and long-lived bonds we can minimize that.

---

**jamesray1** (2018-02-27):

Another potential revenue stream under stateless clients is to have an archive service with archival data servers, however Swarm would compete with this, although the client could somehow integrate Swarm so that anyone can provide the service and if there was a token for the client the service could be transacted with this token, however I haven’t looked into how Swarm works in detail and whether there are any revenue streams there.

---

**jamesray1** (2018-02-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/frankszendzielarz/48/878_2.png) FrankSzendzielarz:

> the biggest hurdle I have faced so far is documentation.

Hi Frank, if you see a way to improve something in documentation, feel free to make an edit (e.g. for a wiki), pull request, or raise an issue with the maintainers/author. That may help you to reinforce your understanding of the content in question, and help future readers.

---

**jamesray1** (2018-02-27):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> IMHO in a perfect network smart contract verification would be the POW itself.

This idea has been thought of and raised elsewhere, but a problem is that miners/validators could do a long range attack by creating a few contracts that they know a fast way of validating (or they’ve cached it), then validating them.

---

**Lars** (2018-02-28):

There is the [Beige Paper](https://github.com/chronaeon/beigepaper/) initiative that may help.

---

**kladkogex** (2018-02-28):

I see … Great point!

In the scheme proposed though it seems that a block proposer will have less incentive to include fake-self-made-easy-to-validate transaction because she will not get paid transaction fees. It seems to be a tradeoff - if you include a fake transaction, than it is easy to validate but you will not get paid transaction fees, only the block reward, because you are essentially paying transaction fees to yourself.

---

**roninkaizen** (2018-02-28):

as written also in the ethereum-research channel

as i understood it right, any of us could propose with an

eip to incentivise node-runners more active,

as somebody is worried about the quality of diversity in nodes

he would invest into a smart contract

dealing exactly this question-

something like “as you want to be rewarded for running your node,

subscribe your node here, with an ethereum-account for your reward”-

then the contract could “look” over all active nodes,

like

node is alive since (14-7-2days), score1

connections acceptance rate (10-20-100),score2

peering speed (kb, MB, GB), score3

reliance (just 4 hours per day, 8 hours, 24/7, 99,99%),score4

as there is no real time monitor for the “distribution level” of the chain,

we could work it out with dedicated submission to a certain “reward”-contract (s.a.) first,

and if it works like intended

to “scaled-up” this certain idea,

which is possible and easier to realize with code-

why overfreighting the etherum-protocoll itself, when information about

the peering node is continouusly given to peering “partners” by standards.

The ethereum protocoll standard defines some of the above mentioned “measure mechanisms”-

why not working with existing structures and information using the smartest techniques with smart contracts-

because if there is such a need like most of us describe, that we like fast peering,

fast “delivering” nodes- the smart contract will be subscribed (and paid) -

to avoid “fraud” in any way there could “put” be a kind of “randomization” into

payout-mechanism-

whereas i am not a coder but very experienced in running “sync” nodes with parity

as proven sometime with posting a picture to some people or into https://github.com/roninkaizen/recipes

there is a strong “wish” for transparency on rewarding, if there is a “real” need for it.

To be honest, it would be fine to get sort of “rewarded” for what people like me do-

the idea behind decentralization and scalability with ethereum is to

spread and interact with a certain “system”.

as we concentrate ourselfes in understanding decentralized networks it is about us to find

stable solutions to be defined by smart people.

---

**3esmit** (2018-02-28):

Maybe we could use a payment channel for buying state reads from full nodes, just like we need to pay gas for writing in ethereum state, full nodes could earn gas for providing the response to nodeless clients. We could have some judge system, like iExec is doing for offchain computation, so if one node sends invalid (signed) response, other could protest and information could be checked inchain (or through judges), if it was indeed a bad response than signer of bad response is penalized somehow (maybe a stake is required for participating).


*(21 more replies not shown)*
