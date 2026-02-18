---
source: ethresearch
topic_id: 5645
title: Coercion resistant quadratic voting
author: snjax
date: "2019-06-23"
category: Applications
tags: []
url: https://ethresear.ch/t/coercion-resistant-quadratic-voting/5645
views: 2897
likes: 0
posts_count: 7
---

# Coercion resistant quadratic voting

## Abstract

Here I describe the construction providing coercion resistance voting. Voters can hide their identities from anybody, and also they cannot be bribed. Also, nobody knows the intermediate result of voting before the final result is counted.

The voter can be bribed in cases:

- cooperation of \geq \frac{C}{3} counting systems, where C is the total number of counting systems and one voter
- cooperation of all voters and one counting center.

The system is fault tolerance in a case <\frac{C}{3} counting centers go down.

## Setup

The users’ personalized accounts have rights to create unique identifiers. For example `hash(secret+salt)` is published, where the the identifier is computed as `hash(address+entropy)`. After then the identifiers can be conducted to other addresses anonymously (in such case as in [anonymous transactions](https://ethresear.ch/t/transactions-with-improved-anonymity/5518)). So, we have a lot of addresses with rights to vote and the set of identifiers. And nobody knows which identifier belongs to which users. Counting centers can associate the identity with any ephemeral address that is used in voting, but this brings no information about a voter’s personality.

## Voting

The voters publish the messages to the blockchain. In each message, we keep \frac{2C}{3} nonzero encrypted rows for the corresponding subset of counting centers and \frac{C}{3} zeroes. Also, we keep the hash of the current voting vector.

The voting vector is something like `[0, 0, 0..., 1, 0, 0, 0]`. We can use fixed point arithmetic and check, that \vec{v}^2 \leq 1 to validate the vector.

Each nonzero row R_i is composite of the pointer to previous message (or to the identifier if this is the first vote) and vector \vec d_i We need to check via the snark, that all pointers are same and \sum \vec d_i = \vec v - \vec v^*, where \vec v^* is voting vector from the previous message (equals zero in the 1st message case).

## Counting

In case when only up to one message is pointed to any message this is simple to count all votes. \vec V = \sum \vec d_{ij}, where all counting centers sum their parts separately, and after that we get resulting vector onchain, counting the sum of all counting centers’ results.

But in real case, we have tree structure like blockchain with forks.

![voting tree](https://ethresear.ch/uploads/default/original/2X/b/b4ab90e1ce0ea288cb3f0d5f8a4954109cc955a0.svg).

In each branching point let’s consider the youngest message valid. So, here the valid branch is ACG.

When we compare any pair of nodes in one branching point (for example B and C), at least \frac{C}{3} counting centers will know enough information to select the youngest node (C in this case).

So, counting centers may review messages one by one. If at least one counting center proof that the node is banned, we set the flag onchain that it is banned, all counting centers update their states and do not use it and all nodes pointed to it.

After that, we can sum all remained vectors (via reduce on zkSNARK) and obtain the result.

## Coercion and collusion resistance

The counting center cannot prove that the current message is the last message from the current voter. Also, the voter cannot prove that his current message is the last. It is achieved because each counting center has \frac{1}{3} messages with unknown information for him.

## Fault tolerance

Let’s consider that \sum \vec d_i r_{ij} = \vec 0 for j = 1..\frac{C}{3}, and each square submatrix in r_{ij} has same range as one’s size. That means that if some d_i are abcent (the counting center send nothing), we can anyway compute total sum.

## Replies

**vbuterin** (2019-06-25):

Interesting! What would you say is the main benefit you are trying to achieve compared to [the simpler technique](https://ethresear.ch/t/minimal-anti-collusion-infrastructure/5413)? Achieving M-of-N security without the heavy crypto of SNARKs over MPC?

I’m having trouble understanding what a “message” is here. The phrase “in each message, we keep \frac{2C}{3} nonzero encrypted rows” seems to be to imply that each voter submits a thing which has multiple rows, so each voter submits a matrix?? Also, what is “the previous message”? The previous vote published to chain? Would this mean that voters can’t publish concurrently, and if so are there DoS attacks there?

---

**snjax** (2019-06-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Interesting! What would you say is the main benefit you are trying to achieve compared to the simpler technique ? Achieving M-of-N security without the heavy crypto of SNARKs over MPC?

The main benefit is achieving M-of-N security. Additional benefits are that nobody knows intermediate results of voting and support of quadratic voting.

The most complex problem is the way how to hide from the counting centers the fact, what message is the last (or the first). I solve this problem here, so, voter and counting center cannot create the proof of the final vote together.

Unfortunately, heavy cryptography like zkSNARK-driven accumulators is used here. We need to process zero knowledge reduce to obtain the result. Maybe some parts of the protocol may be replaced to lighter cryptography, like cryptographic accumulators and homomorphic encryption.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Also, what is “the previous message”?

Speaking about the previous message, I mean any previous message, sent by the current voter. So, no data racing is here.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I’m having trouble understanding what a “message” is here. The phrase “in each message, we keep 2C3\frac{2C}{3} nonzero encrypted rows” seems to be to imply that each voter submits a thing which has multiple rows, so each voter submits a matrix??

The message is a composite of the following parts:

- array of \frac{2C}{3} sub-messages, encrypted via public keys of counting centers. The voter selects the centers as his wish, but he must create sub-messages, addressed to \frac{2C}{3} unique counting centers.
- hash of current voting state vector \vec v of the voter
- messageId=hash(message_parts_1_2, salt) Salt is known only by the sender, so it may be used to prove ownership of the message. For first messages we can use a special form of messageId, corresponding to the user’s identity onchain.

Each sub-message is composed of the following things:

- messageId of any previous message, send by the voter (need be same in all sub-messages, also voter need to prove the ownership)
- vector \vec d_i

Also, the voter needs to prove, that all encryptions are correct, \vec v^2 \leq 1 and \sum \vec d_i = \vec v - \vec v^*, where \vec v^* is the voting state vector of the previous message, determined in the sub-messages.

All messages are published onchain in chronological order. For each voter, we have a tree of his messages, but all graph is known only by the voter. Counting centers know only fragments of the tree.

But for any 2 nodes, pointing to one node there are at least \frac{C}{3} counting centers, that know both 2 nodes. That’s why processing the messages one by one the counting centers can ban all branches excluding the one (with the youngest node in each branching in my model).  After that, the counting centers can sum all the remained data and get the result.

Also, the youngest node rule may be replaced via the oldest node rule. I have not decided, which one is better in all cases.

---

**vbuterin** (2019-06-26):

So the sub-messages need to be consistent with each other? What happens if I make a different vote to each counting center?

> For each voter, we have a tree of his messages, but all graph is known only by the votes

In all cases where the voter is honest, the tree is just a linked list, correct?

> But for any 2 nodes, pointing to one node there are at least \frac{C}{3} counting centers, that know both 2 nodes.

But the “pointing” happens within the sub-messages, not the message. So what does happen here if I make some sub-messages point to one parent and other sub-messages point to another parent?

Also, why does a voter address only \frac{2C}{3} counting centers? Why not address all of them?

---

**snjax** (2019-06-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> In all cases where the voter is honest, the tree is just a linked list, correct?

No, it is legal to link messages as a tree. But after message removing procedure only the linked list remains.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> But the “pointing” happens within the sub-messages, not the message. So what does happen here if I make some sub-messages point to one parent and other sub-messages point to another parent?

When the voter publishes the message, he needs to prove via the snark, that all pointers are the same.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> So the sub-messages need to be consistent with each other? What happens if I make a different vote to each counting center?

The submessages need to satisfy following equations:

- \frac{C}{3} fault tolerance equations \sum\limits_i \vec d_i r_{ij} = \vec 0, where j=1..\frac{C}{3}
- voting delta equation \sum \vec d_i = \vec v - \vec v^*

The user prove this via the snark, when he publish the message.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Also, why does a voter address only \frac{2C}{3} counting centers? Why not address all of them?

If the voter addresses the data to all counting centers, each counting center has all information about the tree of messages. In such a case, the malicious counting center can request data of all messages of the voter as proof of vote and bribe the voter.

---

**vbuterin** (2019-06-28):

I see. So the idea is to have a sort of mixnet, where any given counting center is likely to not see at least some of the links in the tree, and so can’t tell who made a particular vote?

---

**snjax** (2019-06-28):

Yes. One center does not know, who made a particular vote.

Also, in general case one center does not know, what is the final meaning of this particular vote.

