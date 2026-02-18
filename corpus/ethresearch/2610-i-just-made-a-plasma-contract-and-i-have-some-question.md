---
source: ethresearch
topic_id: 2610
title: I just made a plasma contract, and I have some question
author: tsai50702
date: "2018-07-19"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/i-just-made-a-plasma-contract-and-i-have-some-question/2610
views: 1763
likes: 1
posts_count: 3
---

# I just made a plasma contract, and I have some question

I have studied plasma for a while, and I just made a simple plasma contract for decentralized games using token.

I have following questions:

1. What consensus algorithms are possible to use in plasma chains? For a small company, it’s hard to use POS, and POA can’t convince people. How can I use an unconvincing chain support a convincing chain?
2. How high is its efficiency rate? Is there any online application using plasma?

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

Welcome to comment on my smart contract.

(At the top of the contract is a simple token transfer function. You can change to ERC20 Token Standard if you want.)

## Replies

**superdcc** (2018-07-19):

I review your Plasma contract, and you add a new function: the verifier

1. To become a verifier, someone need to pay a guarantee fund.
2. The verifier can agree to the withdrawal before it can takeout.
3. So when someone challenges, the verifier will be punished if the challenge is successful.

So, why someone want to be a verifier?

---

**LucasAschenbach** (2018-07-24):

I have just published a [design for Plasma MVP](https://ethresear.ch/t/plasma-mvp-design-lower-maintainance-cost-scalable-trustless/2663/1) which offers some solutions for reducing operating costs, need for trust, etc.

However, if you are looking to create a blockchain game, perhaps you should check out the loom network. They have specialized in blockchain based games and social media applications and offer a development kid for creating your own sidechains.

I hope it helps!

