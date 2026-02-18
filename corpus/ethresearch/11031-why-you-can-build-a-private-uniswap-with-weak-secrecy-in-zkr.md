---
source: ethresearch
topic_id: 11031
title: Why you can build a private Uniswap with weak secrecy in zkRollup
author: leohio
date: "2021-10-17"
category: Privacy
tags: [zk-roll-up]
url: https://ethresear.ch/t/why-you-can-build-a-private-uniswap-with-weak-secrecy-in-zkrollup/11031
views: 5414
likes: 1
posts_count: 9
---

# Why you can build a private Uniswap with weak secrecy in zkRollup

## Intro

[The previous post](https://ethresear.ch/t/a-zkrollup-with-no-transaction-history-data-to-enable-secret-smart-contract-execution-with-calldata-efficiency/10961/19) referred to the main idea of the private Uniswap or general private/secret smart contract execution.

This idea cannot be the denial of the post “[Why you can’t build a private Uniswap with ZKPs](https://ethresear.ch/t/why-you-cant-build-a-private-uniswap-with-zkps/7754),” but this can be the effective mitigation with some extension.

The previous post, titled “A zkRollup with no transaction history data,” was not appropriate to explain the effective secrecy since the scaling topic and the privacy topic were mixed and gave a vague explanation about the secrecy limitation.

## Approach

### 1) First, you adopt the “Option 2” in zkRollup in this post.

![](https://ethresear.ch/user_avatar/ethresear.ch/leohio/48/10414_2.png)[A zkRollup with no transaction history data to enable secret smart contract execution with calldata efficiency](https://ethresear.ch/t/a-zkrollup-with-no-transaction-history-data-to-enable-secret-smart-contract-execution-with-calldata-efficiency/10961/1)

> There are 2 two options of using txcalldata to restore the full states.
>
>
> Option 1 is recording all of transaction history data to txcalldata.
> Option 2 is recording the diff of the final state as a result of transactions in the block (batch).
>
>
> In option 2, millions of transactions with the same result of no transactions use 0 gas for the txcalldata use, since there is nothing to record in the txcalldata. The soundness of the Merkle root transition is guaranteed by zkp.

Then you can make a batch of zkRollup without tx history data.

Tx history data will be part of the private input of a zkp circuit (like Groth16 or Plonk) and prove that final state diffs are the correct result of that hidden tx history data.

The remarkable thing is that the final state diffs are the result of many transactions.

Here you find the result is mixed, and hard to distinguish them IF THE USER BALANCES / STATES ARE HIDDEN.

### 2) Second, zkp and the “user state” model hide the user’s balance.

If you define the data model that every asset is described as a leaf of the small Merkle Tree for each user, each user can prove her assets and these relevant transitions with zkp without revealing their balance/assets themselves.

The Merkle proof of the inclusion of the assets bind to the last Merkle root, and the Merkle proof of the inclusion of the changed balance/assets bind to the next Merkle root, can be in the private input of the zkp circuit, and the relevant change of global states can be the public input.

Here you find that the user balances/states are hidden if you combine the first step (result mixing) and this second step.

This is what zkp can do as was researched in the works by Barry Whitehat.

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png)[Why you can't build a private uniswap with ZKPs](https://ethresear.ch/t/why-you-cant-build-a-private-uniswap-with-zkps/7754/1)

> ZKPs allow you to prove the state of some data that you know. They do not let you prove about things that you do not know.

However, as he said, zkp cannot hide the changes of global states that reveal users’ activities.

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png)[Why you can't build a private uniswap with ZKPs](https://ethresear.ch/t/why-you-cant-build-a-private-uniswap-with-zkps/7754/1)

> So anyone who is able to update the system must have this state info in order to create the zkp that they updated correctly. If they have the state info they can monitor as the state changes. If they can monitor as the state changes they can see what others are doing.
>
>
> So with ZKPs you end up building private things using only user specific state. So everything is like an atomic swap. If there is global state then this breaks privacy as it needs to be shared for others to make proofs about this state.

If you are the operator, you can know each content of trades in the batch you aggregate. (The important thing here is that other operators cannot know that from the batch.)

In this situation, only the operator and a transactor know what the transactor is doing since all tx histories banish into the private input, and the result is mixed.

So, at the same time, the operators themselves have the “mixing-level” privacy for their transactions because only the operator and a transactor know the activity.

### 3) Third, combining transactions makes “weak secrecy.”

If the operator is the last person who has secrets of the others, let’s make all transactors operators.

The final operator (is the usual operator) combines all batches all small operators (just the users) make.

The transactor has or generates several dummy accounts and integrates the dummy transactions (or cheap transactions from those) to the main transaction as a batch like at the first step. Then the final operator( the usual operator) only knows that one of the addresses with dummies sent a Uniswap trade transaction.

Such a batch, which is actually a transaction, can be combined with others by applying recursive zkp repeatedly. The proof can be the private input to the next proof.

Finally, the usual operator finds a Uniswap transaction mixed with many activities among many addresses.

## Replies

**barryWhiteHat** (2021-10-19):

So the idea is basically

1. Maintain an access list of accounts that are updated
2. The coordinator knows the balances of everyone but this allows the coordinator to hide their own transactions in a block of other users transactions.
3. Make everyone the coordinator os everyone can have private transaction.

Is this a good summary of the idea ?

My worry is that with step 3 you need to share the state with the new coordinator so they can make zkps then you lose privacy.

---

**leohio** (2021-10-19):

If the coordinator is the operator,

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> The coordinator knows the balances of everyone

The coordinator (operator) does not know the balance.

With zkSNARKs, the user can prove the rightness of the relationship of these 3

1. the previous merkle root of all his assets
2. the new merkle root of all his assets after a transaction
3. the change of the storage which is commonly shared in a Ethereum type contract

The coordinator can verify only the root, not the balance itself.

And the coordinator could know the activity of user by the change of the storage, then this hole is patched by combined transaction and dummy address with zkSNARKs described above.

---

**barryWhiteHat** (2021-10-19):

Right so its like zcash and the mixing is used to make it difficult to see which user updates which state variable ?

---

**leohio** (2021-10-19):

Yes.

In ZCash, the assets are utxo, then I’m not sure it’s available to have the merkle root of all assets one has. But it can be difficult to see which user updates and which state variable in the user state from any  node in zkRollup as described.

---

**eigmax** (2022-03-04):

I am confused about how to make the sender’s account anoynomous.

---

**leohio** (2022-04-10):

Here.


      ![](https://ethresear.ch/uploads/default/original/2X/0/0e059a8feebbdf6b4348f5049c9408cfc998331c.png)

      [HackMD](https://hackmd.io/ZTImRSapRH-zADmY7cNJVA?view#5-5-Secret-Smart-Contract-on-zkRollup)



    ![](https://ethresear.ch/uploads/default/optimized/3X/c/d/cd231863ebeb783c60343a8e1e943178c5cb44c7_2_690x362.jpeg)

###










In short, doing an inclusion proof of only state data relevant to a transaction, without revealing an address.

You can hide an address by just hiding siblings of a Merkle proof by ZKP.

---

**eigmax** (2022-04-15):

I see. but the `msg.sender` is always public, right?  kind of relayer delivering `inclusion proof` will be involved in your approach, yes?

---

**leohio** (2022-04-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/eigmax/48/7720_2.png) eigmax:

> but the msg.sender is always public, right?

The msg.sender is always a one-time address generated with a private key and nonce.

Only the user can find the connection between the one-time addresses.

![](https://ethresear.ch/user_avatar/ethresear.ch/leohio/48/10414_2.png) leohio:

> Here.
> Intmax zkRollup [deprecated] - HackMD

