---
source: ethresearch
topic_id: 7754
title: Why you can't build a private uniswap with ZKPs
author: barryWhiteHat
date: "2020-07-24"
category: Privacy
tags: []
url: https://ethresear.ch/t/why-you-cant-build-a-private-uniswap-with-zkps/7754
views: 12840
likes: 39
posts_count: 23
---

# Why you can't build a private uniswap with ZKPs

## Intro

There has been a lot of interest lately in private smart contracts. The thinking that we have the EVM which is good. So it would also be good if we have a private version of the EVM. Where no one knows what anyone else is doing.

The EVM has two components the execution which takes a mix of input from users and the global state. Global state is any variable that a user is able to update during their transactions. For example the contracts balance `this.balance`  can be updated by sending 1 eth to the contract. Or the contracts internal variables such as that contracts balance of an erc20 token.

ZKPs allow you to prove the state of some data that you know. They do not let you prove about things that you do not know.

So ZKPs solve the first part they let you have a private execution. But they don’t let you have private global state.

Here we discuss an example smart contract that is impossible. We hope that this will help others reason about what is and is not possible with zkp based private smart contracts.

## Lack of global state

Uniswap is a constant product exchange. It is a very simple ethereum smart contract that allows people to trade. The contract holds balance of two tokens, token a and token b. It lets you deposit token a and withdraw some amount of token b defined by the ratio in the pools between `bal(token_a)` and `bal(token_b)`

Find more info on constant product exchanges in the original post by [Alen Lu](https://blog.gnosis.pm/building-a-decentralized-exchange-in-ethereum-eea4e7452d6e).

In order to build a private uniswap users need to deposit tokens A and withdraw token B. In order to prove that they have correctly withdrawn they need to know what the current balance of token A and token B are.

If you tell users what the current state they will be able to observe other users interactions see the state before and the state after someone else has used the contract. Using this they can infer what these users have done.

For example say the pool has 1 eth and 1 dai. I know the state but I don’t see users actions. Lets say a user does something. I don’t know what but the new state of the system is 2 eth and 0.5 dai. I know that they deposited 1 eth and removed 0.5 dai.

## Conclusion

So anyone who is able to update the system must have this state info in order to create the zkp that they updated correctly. If they have the state info they can monitor as the state changes. If they can monitor as the state changes they can see what others are doing.

So with ZKPs you end up building private things using only user specific state. So everything is like an atomic swap. If there is global state then this breaks privacy as it needs to be shared for others to make proofs about this state.

https://en.wikipedia.org/wiki/Indistinguishability_obfuscation can allow us to make global private state but that tech is a long way from production IMO.

## Replies

**Recmo** (2020-07-24):

This generalizes to other kinds of exchanges like order book exchanges, where now the global state is the fill state of the top of the orderbook.

Exchange and hence DeFi is hard to do with privacy (and for the same reasons, in an UTXO model and in an Asynchronous model).

---

**adlerjohn** (2020-07-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/recmo/48/3666_2.png) Recmo:

> Exchange and hence DeFi is hard to do in an UTXO model

That’s completely incorrect. UTXOs are equivalent to accounts with strict access lists, [and in fact that’s exactly what’s being done in Serenity](https://twitter.com/_prestwich/status/1284174491967348737). With covenants it’s trivial to define a UTXO that has no “owner.”

---

**Recmo** (2020-07-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> That’s completely incorrect.

I said it was hard, not (necessarily) impossible. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) I’m not sure if I would call that approach trivial compared to Eth1’s account based one, but I haven’t played with it so you could be right.

Is there a more detailed write-up of this approach? I’d like to learn how a Uniswap equivalent would work, especially with multiple concurrent users. Or the sort of funny composition transactions people do in DeFi arbs.

---

**runnerelectrode** (2020-07-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> With covenants it’s trivial to define a UTXO that has no “owner.”

With covenants you can define a spending condition on an UTXO. How would that work for a pool?

---

**adlerjohn** (2020-07-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/runnerelectrode/48/5048_2.png) runnerelectrode:

> How would that work for a pool?

The UTXO is anyone-can-spend, under the condition that the transaction that spends it produces an output that transitions the UTXO’s state based on some data in the transaction (an implementation detail). Now replace “UTXO” with “contract account” and you see that it’s trivial to define open contracts in the UTXO data model. Just make UTXOs able to hold state and contract code! Which is exactly how contracts on Ethereum differ from EOAs.

This should come as no surprise because UTXOs are almost exactly the same as accounts with mandatory strict access lists (there are some minor differences, but they’re outside the scope of your question).

---

**barryWhiteHat** (2020-07-27):

Can two people deposit into the same UTXO and a third spend it without the first two revealing to the third how much they deposited ?

---

**adlerjohn** (2020-07-27):

I don’t see how that would be possible without leaking *any* information. You could probably make sending funds to the contract private, but you’d always need everyone (since it’s anyone-can-spend) to know the current balance. At best you’d be able to obfuscate the source of the funds, not the amount. Kind of like Tornado Cash.

---

**runnerelectrode** (2020-07-28):

ZkVM enables two party shared UTXO to be committed in a contractID to be spent according to the constraint, without revealing to the third party the amount in the commitment.

---

**barryWhiteHat** (2020-07-28):

Who makes the spend proof ?

---

**runnerelectrode** (2020-07-28):

if the constraints are public, then the taker would generate the proof.

---

**barryWhiteHat** (2020-07-28):

So in the example above you said two party shared UTXO. This is a maker taker atomic swap?

Assuming so then party 1 the maker shares the balance of the UTXO with party 2 the taker who then creates a ZKP to consume that UTXO. In this case the maker needs to share their private information with the taker in order to have the atomic swap processed.

Now if you expand this from 1 party the taker being able to execute. To many parties being able to execute them you the taker needs to share their private information with everyone. Thus you lose privacy when you gain the ability for anyone to execute.

---

**Boogaav** (2020-07-29):

Hey [@barryWhiteHat](/u/barrywhitehat) if a user triggers the execution of uniswap’s contract from outside of the chain he/she remains incognito, while the contract executed publicly. I’ve published this work recently [pEthereum - privacy mode for smart contracts & integration with DeFi](https://ethresear.ch/t/pethereum-privacy-mode-for-smart-contracts-integration-with-defi/7336).

What do you think about such implementation? I am quite open to critique, feel free  ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=14)

---

**barryWhiteHat** (2020-07-30):

So basically you have a private erc20 tokens. Where you don’t know who owns which tokens and then you trade these tokens on uniswap or compond ?

So the ownership of the tokens is private but what you do with them trade on uniswap or compound is completely public. This post is claiming that you cannot make a uniswap which is not public. So your approach does not discount that.

> What do you think about such implementation? I am quite open to critique, feel free

I left some comments on the other post as I feel its a more natural place to discuss.

---

**Pratyush** (2020-08-01):

This isn’t quite true; you have to choose what kind of information you reveal. For example in ZEXE we show how to construct private DEXs that offer varying levels of privacy for the maker and the taker. In one construction, the only thing onlookers learn is that a party was interested in performing a trade for A to B (not even amounts are revealed)

---

**Mikerah** (2020-09-06):

I’m working on a similar project where we take a different approach. One thing that was noted by my collaborators is that your reasoning on seems to hold if you use non-malleable ZKPs. Thus, malleable ZKPs could *possibly* help get around the lack of a shared global state.

---

**PlyTools** (2021-01-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/mikerah/48/1616_2.png) Mikerah:

> malleable ZKPs

Hey, is there any paper about malleable ZKPs, it’s really cool

---

**nickgeoca** (2021-02-06):

Is it possible to do account-based privacy using something like erasure encoding? For example, rather than having one storage slot correspond to one person’s balance, have maybe four storage slots corresponding to four people’s balances. Idk if erasure coding is the way to do this, but the idea being several people share the same storage slots. So when they are accessed/written, you can only identify that it is one of those four people. I’m not an expert. Is this possible or make sense?

---

**barryWhiteHat** (2021-02-08):

Oh cool so the person who produced that proof would have to have the private info. For example all the data about the uniswap pool. Its an interesting idea but i think that a fully functional version of this would be obfuscation. Which I think is still pretty hard.

---

**barryWhiteHat** (2021-02-08):

The problem with private account model. Is that I can send x amount of coins to your account. Then refuse to tell you how x is and then you are unable to make a proof of your balance because you don’t know what it is. There are some approaches to solve this but they kind of degrade to input output. So i am not so excited about account model in private systems.

> Is it possible to do account-based privacy using something like erasure encoding? For example, rather than having one storage slot correspond to one person’s balance, have maybe four storage slots corresponding to four people’s balances. Idk if erasure coding is the way to do this, but the idea being several people share the same storage slots. So when they are accessed/written, you can only identify that it is one of those four people. I’m not an expert. Is this possible or make sense?

This does makes but I think this 1 of 4 would reduce your anonimity alot. Also you have to ensure that you know the amount of every inbound transaction in order to avoid the problem descibed above.

---

**tchitra** (2021-02-27):

Thanks for writing this; we ended up [writing a bit to formalize this as an attack for generic constant function market makers](https://stanford.edu/~guillean/papers/cfmm-privacy.pdf). The idea is basically to take advantage of the convexity of the invariant functions used and use that to iteratively approximate what the true trade size executed was. The convexity of these invariants (e.g. constant product, constant geometric mean, convex sum of the two) effectively makes it possible to infer the true and unique (this is the main theorem) trade size involved.


*(2 more replies not shown)*
