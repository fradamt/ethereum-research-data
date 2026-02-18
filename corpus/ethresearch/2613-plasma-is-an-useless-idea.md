---
source: ethresearch
topic_id: 2613
title: Plasma is an useless idea
author: superdcc
date: "2018-07-19"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-is-an-useless-idea/2613
views: 3482
likes: 1
posts_count: 6
---

# Plasma is an useless idea

Plasma is built on the condition that everyone is very compliant, but it is virtually impossible to achieve this.

And when there is wrong information in Root Hash, everyone has to quit, it is a strange behavior…

I have studied plasma for a while, and I just made a simple plasma contract for decentralized games using token. I have following questions:

1. What consensus algorithms are possible to use in plasma chains? For a small company, it’s hard to use POS, and POA can’t convince people. How can I use an unconvincing chain support a convincing chain?
2. How high is its TPS? Is there any online application using plasma?  you know if you want to challenge someone, you need to upload all Merkle tree key node. so it is impossible to achieve 100,000 TPS.

Below is my smart contract URL:


      [github.com](https://github.com/tsai50702/solidity/blob/master/plasma_for_token.sol)




####

```sol
pragma solidity ^0.4.19;

// Pig World Chain (aka PWC is a Plasma solution)
// We are under heavy development, and use ether for test environment.
// using the PICO (ERC-20 Token) for production Environment.

// PWC let the pig world platform is totally decentralized & p2p game.
// PWC preliminary estimate TPS: 10,000

//--------

//Roles in PWC
//verifier, player, dealer, challengeWithdrawal

//--------

//Main function in PWC
//submit header, deposite, withdraw, challenge, prove a challenge

//--------
```

  This file has been truncated. [show original](https://github.com/tsai50702/solidity/blob/master/plasma_for_token.sol)








I add some function like: Punishment mechanism

And a new role in the plasma ecosystem: verifier

1. To become a verifier, someone need to pay a guarantee fund.
2. The verifier can agree to the withdrawal before it can takeout.
3. So when someone challenges, the verifier will be punished if the challenge is successful.

Welcome to comment on my smart contract.

(At the top of the contract is a simple token transfer function. You can change to ERC20 Token Standard if you want.)

## Replies

**zack-bitcoin** (2018-07-19):

The way to overcome these limitations in off-chain smart contracts is this:

- Each off chain contract should only have 2 participants.
- To make a big dapp with more than 2 participants, use hashlocking to connect smaller contracts together.

I wrote a market this way. It matches trades in single-price batches.

---

**ldct** (2018-07-19):

State channel networks like this come with their own downsides that plasma does not come with.

---

**haydenadams** (2018-07-19):

> Plasma is built on the condition that everyone is very compliant, but it is virtually impossible to achieve this.

Forcing the Plasma operator to put up a large bond can discourage bad behavior.

> when there is wrong information in Root Hash, everyone has to quit

This is only true for the original plasma spec referred to as Plasma MVP. In Plasma Cash and Plasma Debit, there is no need for mass exits.

Plasma Cash: [Plasma Cash: Plasma with much less per-user data checking](https://ethresear.ch/t/plasma-cash-plasma-with-much-less-per-user-data-checking/1298)

Plasma Debit: [Plasma Debit: Arbitrary-denomination payments in Plasma Cash](https://ethresear.ch/t/plasma-debit-arbitrary-denomination-payments-in-plasma-cash/2198)

---

**lucusfly** (2018-07-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/superdcc/48/1737_2.png) superdcc:

> What consensus algorithms are possible to use in plasma chains? For a small company, it’s hard to use POS, and POA can’t convince people. How can I use an unconvincing chain support a convincing chain?

In my opinion, plasma chains don’t need to be decentralize, as the decentralization and security are guaranteed by ethereum chain. So we could use even one single node to generate block.

---

**haydenadams** (2018-07-20):

Agreed that POA plasma chains are totally reasonable designs, but they are subject to some level of censorship. Personally, I like the idea of DPOS plasma chains to add a little more censorship resistance at the cost of some scalability.

