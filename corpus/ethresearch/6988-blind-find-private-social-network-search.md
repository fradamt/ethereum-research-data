---
source: ethresearch
topic_id: 6988
title: "Blind Find: Private social network search"
author: barryWhiteHat
date: "2020-02-19"
category: Cryptography > Multiparty Computation
tags: []
url: https://ethresear.ch/t/blind-find-private-social-network-search/6988
views: 7165
likes: 19
posts_count: 17
---

# Blind Find: Private social network search

Barry Whitehat , Kobi Gurkan

## Intro

zkps are fun. They let us privately make statements about information that a single user holds.

They cannot let us talk about information that is not held by a single party. We would like to be able to make proofs about the relationships between multiple people. For example in a social network.

Here we use ZKP + MPC (socialist millionaire problem) to make proofs of connectivity in a social graph.

These proofs can be valuable for

1. Private routing in payment channels
2. Trust graph based crypto currencies / reputation systems
3. Decentralised social networks
4. p2p networks

Here we describe a network of nodes where a member of the network can

Search for a peer without

1. Revealing who they are searching for
2. Finding out who has them as a peer

The parties who were queried do not find out if

1. If the search was result was positive or negative.
2. Where the request came from, only that it came from one of their peers or was forwarded from one of their peers.

The searching party can construct a proof that will convince anyone that such a path exists.

We describe how to make proofs of this that hide any information about the connection.

## The Setup

We have a bunch of people who each have a private list of their “Peers”

This list is committed to on chain.

Each party only knows their own peers.

Each party commits to their peers on chain. The commitment also includes a zero knowledge proof that a connection was authorised by both peers. IE a proof of signature.

The commitment on chain are blinded by salting so no one knows who’s peers anyone has.

Finally all the peer list are aggregated together into a single accumulator so that proofs can say they come from this set.

## The scenario

Alice wants to find a path to Bob.

For ease of explanation here are the social graphs of Alice, Bob , Carroll.

Alice = {Bob, Frank}

Bob = {Alice, Erica, David}

David = {Carroll}

Carroll = {David}

Erica = {Bob, Carroll}

Frank = {Alice}

## Socialist millionaires protocol (SMP)

We use the protocol defined [here](https://en.wikipedia.org/wiki/Socialist_millionaires#Off-the-Record_Messaging_protocol) to find the peer. The search does not return any information other than true or false.

## Full protocol

Here we define the full protocol and then dig deeper into it later.

1. Alice creates a zkp that she is bobs peer. She sends it to bob. She also sends it to her other peers who respond by running the same protocol. She does not know which of her peers is which when responding. She does not know she is talking to Bob.
2. Bob performs the SMP to search for the peer Alice is looking for.
3. Alice completes the protocol.
4. The search fails, because Bob is not connected to Carroll.
5. Bob provides a proof he is connected to a hidden-peer (Erica) connects Alice with Erica to continue the search. Bob essentially acts as a proxy so that Alice doesn’t doesn’t discover she’s connected to Erica.
6. Erica performs the search with Alice.
7. The search works out, since Erica is connected to Carroll.
8. Alice now wants to construct a proof so she can convince someone else that she is connected to Carroll through some other peers.
9. Bob proves he is connected to a salted peer (Erica).
10. Erica proves that she is salted peer that Bob is connected to.
11. Erica proves she ran the SMP correctly for each peer.
12. Alice completes SMP correctly for the search term Carroll.
13. Alice aggregates the proofs together to create a single proof of connection that hides the SMP which could allow Erica to identify the proof.

[![](https://ethresear.ch/uploads/default/original/2X/3/39bedad092661609fa46801c18b44400486f23f6.jpeg)1058×794 37 KB](https://ethresear.ch/uploads/default/39bedad092661609fa46801c18b44400486f23f6)

## Who knows what

1. Alice knows that she is connected by two hops to Carroll.
2. Bob knows that one of his peers was trying to search for someone
3. Erica knows that one of her peer was searching for someone

In order to prevent people from seeing if a search attempt succeeded its important to create proofs for every search attempt.

We also need to continue the search to a certain depth in the social tree even if we have created the proof.

This might be prohibitively expensive but we can make a trade off here.

## Attacks

1. An attacker can brute force the network looking for peers

We can use a ZKP in order to rate limit all requests. [GitHub - semaphore-protocol/semaphore: A zero-knowledge protocol for anonymous interactions.](http://github.com/kobigurk/semaphore), [Semaphore RLN, rate limiting nullifier for spam prevention in anonymous p2p setting](https://ethresear.ch/t/semaphore-rln-rate-limiting-nullifier-for-spam-prevention-in-anonymous-p2p-setting/5009)

1. Loop attack: An attacker creates a loop of peers and when someone is searching for a peer they end up follow this loop forever

Limit the depth to 6 degrees of separation.

## Conclusion

We can privately search peer networks without revealing who is being searched for and who is doing the searching.

This is really exciting for privately finding routes in lightning networks, private social networks and

Adding the proofs allow us to expand this to trust networks, proofs of individuality and reputation systems.

## Replies

**Dumi2000** (2020-02-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> Alice wants to find a path to Bob.

Bob is Alice’s peer, right? so Alice wants to find a path to Carroll is what I understand from below

---

**Dumi2000** (2020-02-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> She does not know which of her peers is which when responding. She does not know she is talking to Bob.

Is this necessary? Like how does she not know that? On which layer are you going to exchange those messages? Are IPs hidden?

---

**Dumi2000** (2020-02-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> Alice doesn’t doesn’t discover she’s connected to Erica.

Alice doesn’t discover he (Bob) is connected to Erica, right?

---

**barryWhiteHat** (2020-02-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/dumi2000/48/5239_2.png) Dumi2000:

> Bob is Alice’s peer, right? so Alice wants to find a path to Carroll is what I understand from below

Yes

![](https://ethresear.ch/user_avatar/ethresear.ch/dumi2000/48/5239_2.png) Dumi2000:

> Is this necessary? Like how does she not know that? On which layer are you going to exchange those messages? Are IPs hidden?

Its not necessary. They autheniticate with IP and communicate using Bob as an intermediary to pass messages.

![](https://ethresear.ch/user_avatar/ethresear.ch/dumi2000/48/5239_2.png) Dumi2000:

> Alice doesn’t discover he (Bob) is connected to Erica, right?

Yes she does not know she is talking to Erica.

A lot of these pieces can be removed if you don’t need them. We build the most private system we could Perhaps you don’t even need ZKPs if you are just searching.

---

**kobigurk** (2020-02-22):

Well, both are true ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

This is prevented by the fact that Bob just proves he’s connected to one of his peers, and by the fact the Bob is acting is a proxy in the communication between Alice and Erica.

---

**Dumi2000** (2020-02-27):

Thank you again, now I understand the protocol much better. I will share it with the team here and then we will see how to go on.

Some more questions came to Dong-Ha’s and my mind. But it is more like note, not that we expect you to answer this

- To route in Raiden, we need information about channel balances and fees in a certain channel. The suggested search would provide any user with the information that there is a path but no more. So our first question would be how can the zero knowledge of having a connection to someone (binary) be used?
- Is the found path always the shortest? I.e. can the searcher choose between different paths? Is it a fundamental problem that privacy and optimality cannot go hand in hand?
- What kind of zkp variant can be used here? i.e. how efficient / scalable is the protocol in terms of proof generations for finding a path?

---

**barryWhiteHat** (2020-02-28):

> To route in Raiden, we need information about channel balances and fees in a certain channel. The suggested search would provide any user with the information that there is a path but no more. So our first question would be how can the zero knowledge of having a connection to someone (binary) be used?

You can find protocols to find if a > b [Yao's Millionaires' problem - Wikipedia](https://en.wikipedia.org/wiki/Yao's_Millionaires'_Problem) which may work better for finding paths with various volumes.

> Is the found path always the shortest? I.e. can the searcher choose between different paths? Is it a fundamental problem that privacy and optimality cannot go hand in hand?

no and it could have cycles through malicious notes pass the path through themselves multiple times.

> What kind of zkp variant can be used here? i.e. how efficient / scalable is the protocol in terms of proof generations for finding a path?

I am not sure you need to create the zkp for payment channels. I thought you would just route the payment once you have found the path.

---

**rumkin** (2020-03-01):

Can you explain it like I’m five? What is searching here a route to user I already know or a user I think I know? Does attacker can build a network of fake accounts with ends connected to the real users to know who you try to connect to?

---

**barryWhiteHat** (2020-03-02):

> Can you explain it like I’m five?

Find a a connection to a user throught your friends. But you ask your friends in a way that they don’t know who you are looking for. If your friends don’t know them you ask their friends.

> What is searching here a route to user I already know or a user I think I know?

You know their public id. But you don’t know how to connect to them.

> Does attacker can build a network of fake accounts with ends connected to the real users to know who you try to connect to?

In order to connect to a user you need to have their permission. You must possess a signatures in order to connect with them. So this attack will only work if you search target helps the attacker.

---

**lsankar4033** (2020-06-09):

In step 2 of the protocol, what is the piece of information Bob and Alice are comparing with SMP?

---

**SebastianElvis** (2020-06-09):

> We would like to be able to make proofs about the relationships between multiple people. For example in a social network.

Do you mean: in a network without any trusted third party, a node can make proofs that he directly connects to some nodes?

This is different from social network. The relationship in your scenario is not recorded in public (e.g., the network of channel capacity of Lightning Network) or a trusted party (e.g., Social network like Facebook). All relationships are maintained by pairs of nodes privately (e.g., the network of channels’ real-time balance of Lightning Network). In this way, nodes can forge proofs arbitrarily. Here you implicitly assume all nodes behave honestly.

For example, in a multi-hop payment in Lightning Network, you should assume all nodes report their real-time balances honestly in order to make your protocol work.

For networks where connections are recorded, there have been lots of research. Mainstream approaches are based on Symmetric Searchable Encryption and some Privacy-Preserving Graph Search techniques.

> Search for a peer without
>
>
> Revealing who they are searching for
> Finding out who has them as a peer

How do you define “searching for a peer”? Do you mean routing, i.e., given a node, find a viable route between the requester and this node, or peer look up, i.e., given a node, find all peers of it? According to your following description I guess you mean routing.

The first requirement basically requires to anonymise who sends the request (i.e., zero knowledge of the requester). This is not easy, and the main challenge is not at the protocol level, which is trivial by omitting identity of the requester. Instead, the underlying communication channel can be a side channel leaking the identity of the requester, inevitably.

What do you mean by the second requirement? I don’t find any security argument you make on this one. If you mean the requester cannot know any peer of nodes in the routing path, this is also trivial by only returning the routing path to the requester.

> The parties who were queried do not find out if
>
>
> If the search was result was positive or negative.
> Where the request came from, only that it came from one of their peers or was forwarded from one of their peers.

For the first requirement, the last and the second last nodes can always learn the routing result. Existing routing protocols (like Onion routing) have already achieved that other intermediate nodes cannot learn about the routing result. This seems to be a basic requirement of privacy-preserving routing protocols.

The second requirement is also achieved in existing privacy-preserving routing protocols.

Also, do you have any comparisons between this protocol with other privacy-preserving routing protocols? This one seems to suffer from non-negligible overhead on MPC and ZK techniques, and does not achieve stronger privacy than Onion routing.

I also believe Onion is not optimal for this scenario. For example, there have been routing protocols using Puncturable Encryption for fewer roundtrips, which might be useful for this scenario. https://petsymposium.org/2020/files/papers/issue2/popets-2020-0030.pdf

---

**mhchia** (2020-07-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> Erica performs the search with Alice.

Should it be “Alice performs the search with Erica”?

![](https://ethresear.ch/user_avatar/ethresear.ch/lsankar4033/48/10215_2.png) lsankar4033:

> In step 2 of the protocol, what is the piece of information Bob and Alice are comparing with SMP?

Is the public ID of the peer to-be-searched compared in SMP, in the example, Carrol’s public ID?

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> 1058×794 37 KB
>
>
> 1058×794 37 KB

Is the diagram out of order?

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> Alice = {Bob, Frank}
> Bob = {Alice, Erica, David}
> David = {Carroll}
> Carroll = {David}
> Erica = {Bob, Carroll}
> Frank = {Alice}

Not a big problem, but it seems the graph is directed. I thought it should be undirected instead?

Other questions:

1. If A wants to connect B, is it correct that they should 1) establish a connection(e.g. TCP/IP connection), 2) add each other in their peer list, 3) create a proof with both signatures(i.e. “proof that a connection was authorised by both peers”), and 4) submit the proof on chain as the commitment? And then the aggregated list should be updated since a new connection is established?

---

**barryWhiteHat** (2020-07-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/mhchia/48/643_2.png) mhchia:

> Should it be “Alice performs the search with Erica”?

Its the same.

![](https://ethresear.ch/user_avatar/ethresear.ch/mhchia/48/643_2.png) mhchia:

> Is the public ID of the peer to-be-searched compared in SMP, in the example, Carrol’s public ID?

![](https://ethresear.ch/user_avatar/ethresear.ch/mhchia/48/643_2.png) mhchia:

> If A wants to connect B, is it correct that they should 1) establish a connection(e.g. TCP/IP connection), 2) add each other in their peer list, 3) create a proof with both signatures(i.e. “proof that a connection was authorised by both peers”), and 4) submit the proof on chain as the commitment? And then the aggregated list should be updated since a new connection is established?

Yes

Its possible to simplify this protocol a bit to reduce the ZKPs proving that i am peer with users when i am searching for someone else. The current version is highly optimized to hide all info. We can reveal some to make it easier to build.

---

**barryWhiteHat** (2020-07-22):

Appologies i did not respond sooner ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/sebastianelvis/48/7342_2.png) SebastianElvis:

> Do you mean: in a network without any trusted third party, a node can make proofs that he directly connects to some nodes?

Yes

![](https://ethresear.ch/user_avatar/ethresear.ch/sebastianelvis/48/7342_2.png) SebastianElvis:

> This is different from social network. The relationship in your scenario is not recorded in public (e.g., the network of channel capacity of Lightning Network) or a trusted party (e.g., Social network like Facebook). All relationships are maintained by pairs of nodes privately (e.g., the network of channels’ real-time balance of Lightning Network). In this way, nodes can forge proofs arbitrarily. Here you implicitly assume all nodes behave honestly.

You commit to connections on chain + include signature that both sides of the connection consent to it.

![](https://ethresear.ch/user_avatar/ethresear.ch/sebastianelvis/48/7342_2.png) SebastianElvis:

> How do you define “searching for a peer”? Do you mean routing, i.e., given a node, find a viable route between the requester and this node, or peer look up, i.e., given a node, find all peers of it? According to your following description I guess you mean routing.

From me find a connection to specifically one other node. Tho we can use a similar sheme to find other peers.

![](https://ethresear.ch/user_avatar/ethresear.ch/sebastianelvis/48/7342_2.png) SebastianElvis:

> The first requirement basically requires to anonymise who sends the request (i.e., zero knowledge of the requester). This is not easy, and the main challenge is not at the protocol level, which is trivial by omitting identity of the requester. Instead, the underlying communication channel can be a side channel leaking the identity of the requester, inevitably.

You can use [GitHub - semaphore-protocol/semaphore: A zero-knowledge protocol for anonymous interactions.](http://github.com/kobigurk/semaphore) for this.

![](https://ethresear.ch/user_avatar/ethresear.ch/sebastianelvis/48/7342_2.png) SebastianElvis:

> What do you mean by the second requirement? I don’t find any security argument you make on this one. If you mean the requester cannot know any peer of nodes in the routing path, this is also trivial by only returning the routing path to the requester.

I mean who is searching for peer X. you don’t know who the request is coming from.

![](https://ethresear.ch/user_avatar/ethresear.ch/sebastianelvis/48/7342_2.png) SebastianElvis:

> The second requirement is also achieved in existing privacy-preserving routing protocols.

Its probably not routeing more like path finding. I am not aware of a solution to this, could you share?

![](https://ethresear.ch/user_avatar/ethresear.ch/sebastianelvis/48/7342_2.png) SebastianElvis:

> I also believe Onion is not optimal for this scenario. For example, there have been routing protocols using Puncturable Encryption for fewer roundtrips, which might be useful for this scenario. https://petsymposium.org/2020/files/papers/issue2/popets-2020-0030.pdf

Here you reveal where you are searching for in the last step, you reveal what website you want to get in the tor example. This cannot be linked to you. Which is a problem in trust networks and things like that.

---

**barryWhiteHat** (2020-07-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/lsankar4033/48/10215_2.png) lsankar4033:

> In step 2 of the protocol, what is the piece of information Bob and Alice are comparing with SMP?

Public key of the peer Alice is searching for.

---

**mhchia** (2020-07-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> mhchia:
>
>
> Is the public ID of the peer to-be-searched compared in SMP, in the example, Carrol’s public ID?

Thanks for the explanation.

Is it correct if we remove all ZKPs, it’s a DFS on the graph with SMP run with all visited peers? Besides, is every SMP run with an indirect peer(i.e. the initiator and responder are not neighbors on the graph) is proxied through the intermediate peers?

