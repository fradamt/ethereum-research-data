---
source: ethresearch
topic_id: 4605
title: Client-Side Solidity/EVM
author: kladkogex
date: "2018-12-17"
category: EVM
tags: []
url: https://ethresear.ch/t/client-side-solidity-evm/4605
views: 1899
likes: 6
posts_count: 5
---

# Client-Side Solidity/EVM

What we realized recently at Skale Labs, is that if your app requires validators (a random group of nodes  that need interact with the blockchain and the outside world), then validators need to be written in Solidity.  Coding smart contracts in Solidity and validators in python does not make much sense.

Ideally  it has to be the same code base, and a generic framework which would operate in terms of messages sent both ways.

Essentially one needs a Client-side Solidity/EVM version similar to NodeJS for Javascript.

I wonder if anyone else here had similar ideas …

## Replies

**hjorthjort** (2018-12-20):

I’ve been thinking in exactly the same terms recently, mostly to be able to bootstrap and write a Solidity compiler in Solidity. I think it should be technically possible today, but require a lot of libraries and hacking.

Are you thinking in terms of making some sort of NodeJS-like clientside interpreter, with extra capabilities/libs to simplify stuff like IO? Or are you thinking about extending Solidity to make it more general purpose? In the latter case, it would be ideal to have some clean separation between “contract Solidity”, with extra restrictions and/or optimizations, and “general-purpose Solidity”, I think.

---

**DZack** (2018-12-20):

“generic framework which would operate in terms of messages sent both ways”

For some cases, this is enough to circumvent having to write client side logic that’s duplicative with the solidity code; i.e., Counterfactual’s generalized state machines. But I don’t know enough about Skale’s specific needs — can you give an example of what you have in mind with an “app that requires validators”?

---

**kladkogex** (2018-12-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/hjorthjort/48/3007_2.png) hjorthjort:

> Are you thinking in terms of making some sort of NodeJS-like clientside interpreter, with extra capabilities/libs to simplify stuff like IO? Or are you thinking about extending Solidity to make it more general purpose?

Initially I was thinking about a NodeJS-like interpreter, with extended capabilities like IO and internet access.  But I think your idea about making Solidity more of a general purpose language also makes lots of sense. It could be two versions of solidity one general purpose / client side and another one for blockchain.

![](https://ethresear.ch/user_avatar/ethresear.ch/dzack/48/2562_2.png) DZack:

> can you give an example of what you have in mind with an “app that requires validators”?

Ideally, you would be able to easily write Casper validators in this framework.

Another example is an oracles, or Truebit like system.

IMHO this can be done without modifications to the EVM through pre-compiled smart contracts. You would need pre-compiled smart contracts for file/network IO. Also you would need to add a trigger facility to run client-side EVM periodically or on events from the blockchain

---

**hjorthjort** (2018-12-21):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Initially I was thinking about a NodeJS-like interpreter, with extended capabilities like IO and internet access. But I think your idea about making Solidity more of a general purpose language also makes lots of sense. It could be two versions of solidity one general purpose / client side and another one for blockchain.

I think it sounds interesting and could be on board to be part if there is some real interest in a concept like this. Do you know any other groups or companies that have shown interest? I’m just gearing up to re-learning Solidity, to see what idioms could be used.

