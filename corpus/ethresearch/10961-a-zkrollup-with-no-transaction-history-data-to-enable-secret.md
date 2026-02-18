---
source: ethresearch
topic_id: 10961
title: A zkRollup with no transaction history data to enable secret smart contract execution with calldata efficiency
author: leohio
date: "2021-10-08"
category: Layer 2
tags: [zk-roll-up]
url: https://ethresear.ch/t/a-zkrollup-with-no-transaction-history-data-to-enable-secret-smart-contract-execution-with-calldata-efficiency/10961
views: 11610
likes: 10
posts_count: 24
---

# A zkRollup with no transaction history data to enable secret smart contract execution with calldata efficiency

Thanks to Alex Gluchowski from zkSync and Barry Whitehat for your insights.

## 1) TL;DR

A zkRollup that does not require tx-history-data from an operator. This has an efficiency of gas use of txcalldata on L1 and also has the privacy of smart contract executions and assets. Only an account list of owners of changed states needs to be recorded in txcalldata for each batch.

The demerit is a need for zkp calculation of client-side for each user when she makes funds exit to L1. Another demerit is the difficulty of EVM compatibility.

## 2) Background & Motivation

Rollups still cost operators and transactors for their txcalldata use. This restriction is simply because of a need to restore states which are the result of transactions not to make users unavailable to generate the Merkle proofs of their funds. The most of specifications of Rollups require operators to dump all transaction history data to txcalldata on L1.

This transparency of transaction history data is not only increasing gas costs of txcalldata but also disabling the privacy of transactions.

It’s conjectured that an accumulator of transaction history data solves both the efficiency problem and the privacy problem.

## 3) Approach

In short,

In the first step, we construct a zkRollup that operator writes final states diff directly to txcalldata. Transaction history data will be in private inputs of a circuit of zkp.

In the second step, we remove the final states diff from txcalldata by separating commonly used storage and user state storage. This enables a user’s exit with non-inclusion proof like a state version of Plasma Prime. A user keeps her user storage and exposes only its Merkle Root. The user can prove the root transition with zkp and can update a commonly used storage of a smart contract.

The details are below.

### 3.1) First Step, options of txcalldata usage in zkRollup

There are 2 two options of using txcalldata to restore the full states.

Option 1 is recording all of transaction history data to txcalldata.

Option 2 is recording the diff of the final state as a result of transactions in the block (batch).

In option 2, millions of transactions with the same result of no transactions use 0 gas for the txcalldata use, since there is nothing to record in the txcalldata. The soundness of the Merkle root transition is guaranteed by zkp.

Adopting “option 2” is the first step.

### 3.2) The second step, optimizing “option 2”

Option 2 described above costs less gas when the transactions in a batch/block change the same storage value in a contract. Such commonly shared and changed values are like a total supply of ERC20, a total pooled amount of a swap protocol, etc.

And also this kind of storage value affects all asset holders, and the loss of this kind of data leads to the loss of liveness of zkRollup. On the other hand, the other data which is not commonly shared and changed are mostly individual asset data. The loss of this kind of data directly means the loss of funds of the owner. This risk is separated and does not affect the other’s funds.

Then separating users’ states and giving a user data of her states and its proof as a receipt of her transaction by an operator makes mass gas cost cut.

```auto
(1) A transactor send a transaction to the operator

(2) The operator make the merle proof of her user state as a receipt of the transaction

(3) The transactor sign the receipt

(4) Only transaction data with the signed receipt is accepted in the circuit
```

If one user makes a transaction and several users have their balances changed and they know their states including those balances and Merkle proofs, any of them can exit her funds at any time by zkp which proves that it’s the last state.

This proves that it’s the last state of her balance can be made by non-inclusion proof of each account list of owners of changed states for each batch. Sparse Merkle Tree of account list of owners of changed states can be used to have efficient proof. This is like Plasma Prime with states, SMT, and zkp. There is no exit game.

There are 2 ways to let the owners of changed states know their last changes.

If they are online, the operator sends the last diff, receives the signed that diff, and puts it into the input of the zkp circuit. This has the cheapest gas cost.

If they are not online, the operator posts it to txcalldata or off-chain decentralized storage.

With this separation of states, an operator no longer needs to put even any diff of the final states to txcalldata, because users have their account states safe enough for the exit, and losing commonly shared data is just meaning that the operators can not update the Merkle Root of the zkRollup and they will simply stop the service. Then both commonly shared storage and user storage can be distributed off-chain. Only an account list of owners of changed states needs to be recorded in txcalldata for each batch.

### 3.3) The third step, private smart contract execution

Users’ transactions are not on-chain, but operators still can see and need to see the user states including balances to make zkp proofs.

If a user makes zkp by her side to prove the transition of her Merkle root of her user state and the commonly shared storage, the operator can just change that root and storage. The secret of the balance remains.

```auto
(1) The user sends a transaction to the operator.

(2) The operator returns the diff of balance and the updated common shared storage.

(3) The user makes zkp proof of the updated Merkle root of her user state and common shared storage.
```

An operator who makes each batch can know the balance diff by the changes of commonly shared storage in the batch, but she can not know the balance diffs in other batches since only the final diff is shared among operators. This has mixing-level privacy.

This mechanism requires recursive-zk.

## 4) More detailed discussion

### 4.1) Communication to off-line state changers at off-chain.

This is just an option. This protocol can be constructed without this part.

Even in the worst case, state changers are off-line, data availability risks for this case are very limited.

An offline user can get data to be safe to exit when she is online. She can set agents instead of receiving the data by herself.

And we can construct the exit method so that the last state update does not make the previous state dangerous due to a data availability problem.

Typical decentralized storage can be constructed as bellow,

```auto
(1) commit hash(storage)

(2) prove preimage(hash(storage)) = preimage(hash(storage, last-Ethereum-block-header)) -  last-Ethereum-block-header

(3) keep watching how many nodes can do (2)
```

### 4.2) Account listing gas cost on chain

Each account can get an ID that is much shorter than an address itself.

Only an account list is needed for each batch, then this can omit duplicates, and this is much more efficient than transaction history in txcalldata uses.

### 4.3) Further optimization of common shared storage

On Ethereum L1, you can not erase txcalldata.

We can modify this since common shared storage needs not to be on-chain.

Unlike transaction history data, we need only last state data, not any state before.

Then operators can abandon the previous “final states data” shared in the network.

Operators can know the data which can be abandoned with the zkp logic.

## 5) Conclusion

Separating user states makes both efficiency and privacy in zkRollup smart contract execution. Almost all of txcalldata cost is removed from zkRollup.

ps: Please read this also.



    ![](https://ethresear.ch/user_avatar/ethresear.ch/leohio/48/10414_2.png)
    [A zkRollup with no transaction history data to enable secret smart contract execution with calldata efficiency](https://ethresear.ch/t/a-zkrollup-with-no-transaction-history-data-to-enable-secret-smart-contract-execution-with-calldata-efficiency/10961/15) [Layer 2](/c/layer-2/32)



> It is easy to misunderstand the point of data availability in this protocol.
> First, this protocol does not rely on off-chain decentralized storages. This is just an option.
>
> I edited the document and added this.
> Second, this is important that operators don’t need to write the commonly shared storage to calldata.
> Let’s talk about the Uniswap V2 on this protocol spec, and let’s start with all LPs are online for the simplest case.
> It’s  essentially a transaction between a transactor and severa…

## Replies

**adompeldorius** (2021-10-08):

Hi, I am working on very similar ideas. I have started with a version that only does transfers, but I have also an idea of how to support contracts. I am working on a specification [here](https://hackmd.io/-Uj7YPjYTkmIhuG7-FVmNQ).

---

**leohio** (2021-10-08):

Thank you for your good document, I’m glad to see the pioneer.

The biggest difference is here.

> All changes to the published state must be included as calldata

This mechanism does not provide state data to calldata.

Focusing on deviding states is the common feature, I think.

And I think this approach is also oriented to the privacy of smart contracts.

---

**adompeldorius** (2021-10-08):

By “changes” I mean the diff from the previous batch ![:blush:](https://ethresear.ch/images/emoji/facebook_messenger/blush.png?v=9)

---

**adompeldorius** (2021-10-08):

Could you clarify what would happen if the operator disappeared after publishing a batch without providing any state? How would users be able to withdraw their funds? In particular, what about liquidity providers that would need access to the latest state of token balances, which is part of the common state, in order to exit?

---

**leohio** (2021-10-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/adompeldorius/48/6325_2.png) adompeldorius:

> How would users be able to withdraw their funds?

Here is the way to exit their fund.

![](https://ethresear.ch/user_avatar/ethresear.ch/leohio/48/10414_2.png) leohio:

> This proves that it’s the last state of her balance can be made by non-inclusion proof of each account list of owners of changed states for each batch. Sparse Merkle Tree of account list of owners of changed states can be used to have efficient proof.

This is the reason why only this account/ID lists could not be removed from txcalldata.

---

**adompeldorius** (2021-10-08):

I see, but I’m more worried about losing the common state, since e.g. liquidity providers would need it in order to withdraw.

---

**leohio** (2021-10-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/adompeldorius/48/6325_2.png) adompeldorius:

> liquidity providers would need it in order to withdraw.

It won’t be a problem.

I’m sorry for the previous insufficient explanation. It’s different from the typical smart contract.

The transactor makes a transaction, and both the transactor and relevant LPs sign otherwise the diff will be on txcalldata.

Bacially, being online makes both the efficiency and the privacy.

ps: Offline user can have the privacy. I realized that the calldata messages of diff of offline user states can be  encrypted for each of them with her public key, and off course this can be merged to her user state to exit with zkp.

---

**adompeldorius** (2021-10-08):

Aha, I see. Would that mean that if even one LP, is offline, state diffs would need to be provided in calldata? I would suppose that would be the case most of the time in practice. Even so, it would still be an improvement, since the amount of diffs to common state is O(number of common contracts), which would be much smaller than O(number of users).

---

**leohio** (2021-10-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/adompeldorius/48/6325_2.png) adompeldorius:

> Would that mean that if even one LP, is offline, state diffs would need to be provided in calldata?

It’s up to how to code swap contract on this zkRollup.

One thing I can assure you is an offline LP with secret balance can not exist (edit: this was found to be possible, see the comment above), since the LP needs to make a zkp proof with her user state to keep it secret and this needs to be online available.

In one implementation, the diff of **his** state will be in calldata.

On Uniswap, especially V3, a swap transactor is having deals with LPs.

An LP locks their token on the contract and it’ll be added to the contracts’ balance on Ethereum L1,

the LP have their balance in his state with an allowance/flag controll for Uniswap contract on this zkRollup spec. These are same.

Another implementation is what you said, the final state of contract (commonly shared storage) will be in calldata. This would be safe as well.

I think online/offline requirements, secret/public, and usage of calldata will be programmable in this kind of network and VM. That’s why it’s up to how to implement contracts.

---

**adompeldorius** (2021-10-08):

Also, have you seen [this proposal](https://ethresear.ch/t/adamantium-power-users/9600)? It seems relevant.

---

**leohio** (2021-10-08):

Yes, I did. And l think this seems a very good idea.

But it was different from my main focus, a **secret smart contract execution with zkp** and minimizing txcalldata of zkRollup with the same security assumption of zkRollup.

---

**adompeldorius** (2021-10-08):

I believe the power users in Adamantium also enjoy the same security assumptions as a zk-rollup. The idea is the same; that you can avoid using calldata for online users.

Another question, if you don’t mind, because it is still not entirely clear to me:

Focusing on simple transfers, my proposal has the property that you can send funds to an offline recipient, without having to post the transfer data as calldata. When the recipient comes online, even in the worst case where they find out that their account state is unavailable, they can still exit by providing a witness to the latest balance they have, together with the receipt of the additional received funds (given to them by the sender).

How does your proposal handle this scenario? Do you require recievers to be online to avoid having to post the transfer in calldata?

---

**leohio** (2021-10-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/adompeldorius/48/6325_2.png) adompeldorius:

> the same security assumptions as a zk-rollup

I could not judge that, then I could not refer to Adamantium clearly.

![](https://ethresear.ch/user_avatar/ethresear.ch/adompeldorius/48/6325_2.png) adompeldorius:

> The idea is the same; that you can avoid using calldata for online users.

If you cut out this part, you can say it’s the same about this part. Yes.

![](https://ethresear.ch/user_avatar/ethresear.ch/adompeldorius/48/6325_2.png) adompeldorius:

> When the recipient comes online, even in the worst case where they find out that their account state is unavailable, they can still exit by providing a witness to the latest balance they have, together with the receipt of the additional received funds

This does not simply occur.

---

**leohio** (2021-10-10):

It is easy to misunderstand the point of data availability in this protocol.

First, this protocol does not rely on off-chain decentralized storages. This is just an option.

![](https://ethresear.ch/user_avatar/ethresear.ch/leohio/48/10414_2.png) leohio:

> This is just an option. This protocol can be constructed without this part.

I edited the document and added this.

Second, this is important that operators don’t need to write the commonly shared storage to calldata.

Let’s talk about the Uniswap V2 on this protocol spec, and let’s start with all LPs are online for the simplest case.

It’s  essentially a transaction between a transactor and several LPs.

The secret smart contract execution of this Uniswap goes as below.

1. The transactor send a transaction to the operator
2. The operator send the diff of the commonly shared storage (like pooled amounts of ERC20 tokens and k-value) to the transactor and the LPs
3. All of them make a zkp proof of the transitions of the Merkle roots of their user states caused by balance changes from that transaction. These can be receipts as well.
4. The operator includes the proofs as the transactions in the next batch.

Then do you think it is dangerous that all nodes lose the commonly shared storage?

If it’s lost, the operators can not make a new transaction, then liveness will die. But anyone can exit her fund to L1 with the latest receipt. The service will end, but no fund will be compromised.

The commonly shared storage is **needed for liveness, not safety.**

---

**StarLI-Trapdoor** (2021-10-13):

Thanks a lot for the idea to reduce the calldata size of zkRollup. I tried to understand the idea: instead of save transactions onchain, the state difference (the “commonly used” storage) is saved onchain only. Even the operator is crashed, he/she can recover the “common” state from onchain data. However, I have several questions in mind:

1/ Logically, if many transactions uses the same “commonly used” storage, the calldata size can be reduced. However, if each transaction affects different “commonly used” storage, the calldata size may NOT be reduced.

2/ Due to the fact, the “commonly used” storage for one batch of transactions is NOT fixed. To reduce the onchain size, extra circuit logic should be used. Whether the circuit complexity is increased?

3/ Because the “user used” storage is saved in user side, if the user lost his/her data, he can NOT send transaction anymore and the worst case is that he can NOT exit because he can NOT generate the according merkle proof.

Am I right about those understanding? Thanks a lot ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**leohio** (2021-10-14):

Thank you

![](https://ethresear.ch/user_avatar/ethresear.ch/starli-trapdoor/48/8900_2.png) StarLI-Trapdoor:

> the state difference (the “commonly used” storage) is saved onchain only.

Actually, we can remove the common state difference from calldata without losing safety.

This is in the second step.

![](https://ethresear.ch/user_avatar/ethresear.ch/leohio/48/10414_2.png) leohio:

> Then do you think it is dangerous that all nodes lose the commonly shared storage?
>
>
> If it’s lost, the operators can not make a new transaction, then liveness will die. But anyone can exit her fund to L1 with the latest receipt. The service will end, but no fund will be compromised.
>
>
> The commonly shared storage is needed for liveness, not safety.

The common state diff can be shared off-chain, the circuit requires the operator to prove she shared the common state diff to other operators. Then one operator can not kill the liveness, and there will be no fund loss if it happens.

So only the account/ID list is needed to be in calldata, basically.

Almost all of txcalldata cost is removed from zkRollup if you allow the possibility of the end of the service and the relevant safe exit.

![](https://ethresear.ch/user_avatar/ethresear.ch/starli-trapdoor/48/8900_2.png) StarLI-Trapdoor:

> 1/ Logically, if many transactions uses the same “commonly used” storage, the calldata size can be reduced. However, if each transaction affects different “commonly used” storage, the calldata size may NOT be reduced.

So here won’t be the problem. But you are right about the storage cost estimations of these cases when it’s discussed about off-chain data.

![](https://ethresear.ch/user_avatar/ethresear.ch/starli-trapdoor/48/8900_2.png) StarLI-Trapdoor:

> he can NOT send transaction anymore and the worst case is that he can NOT exit because he can NOT generate the according merkle proof.

If he (and all other people) loses his user state data completely, he can not send any transaction anymore. You are right.

The best effort we can make for this is preventing the last user state update destroys the exit of the irrelevant assets in the user state.

---

**StarLI-Trapdoor** (2021-10-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/leohio/48/10414_2.png) leohio:

> StarLI-Trapdoor:
>
>
> the state difference (the “commonly used” storage) is saved onchain only.

Actually, we can remove the common state difference from calldata without losing safety.

This is in the second step.

![](https://ethresear.ch/user_avatar/ethresear.ch/leohio/48/10414_2.png) leohio:

> Then do you think it is dangerous that all nodes lose the commonly shared storage?
>
>
>
> If it’s lost, the operators can not make a new transaction, then liveness will die. But anyone can exit her fund to L1 with the latest receipt. The service will end, but no fund will be compromised.
>
>
> The commonly shared storage is needed for liveness, not safety.

The common state diff can be shared off-chain, the circuit requires the operator to prove she shared the common state diff to other operators. Then one operator can not kill the liveness, and there will be no fund loss if it happens.

So only the account/ID list is needed to be in calldata, basically.

Almost all of txcalldata cost is removed from zkRollup if you allow the possibility of the end of the service and the relevant safe exit.

Thanks a lot for your clarification. My understanding is that for best optimization, only changed account IDs are published on chain. And operators help to maintain commonly shared storage and users are on duty to save his/her user storage. For that case, the safety is NOT same as original zkRollup solution. For original zkRollup solution, the safety is exactly same as L1. However, your idea’s safety is NOT same as L1. Actually, the safety depends on operators’ safety. If all operators lost the “commonly shared storage”, the system has to enter exit mode and can NOT be recovered.

---

**leohio** (2021-10-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/starli-trapdoor/48/8900_2.png) StarLI-Trapdoor:

> For that case, the safety is NOT same as original zkRollup solution. For original zkRollup solution, the safety is exactly same as L1.

For this spec, safety is exactly same as L1 if users are online.

Liveness is not same as L1. That’s the difference.

Users don’t lose their money, and users don’t have double spend as far as L1 is not 51% attacked.

This is safety.

![](https://ethresear.ch/user_avatar/ethresear.ch/starli-trapdoor/48/8900_2.png) StarLI-Trapdoor:

> Actually, the safety depends on operators’ safety. If all operators lost the “commonly shared storage”, the system has to enter exit mode and can NOT be recovered.

All assets can be exit since all of them are in “user state”.

Commonly shared storage should not describe the assets, and that’s why this spec separates these.

So, when “commonly shared storage” can not be recovered, safety will be fine. Liveness dies.

---

**barryWhiteHat** (2021-10-19):

So the idea here is you allow users to withdraw from a previous state if a transaction for that address has not already been included ?

My concern here is that after a user has withdraw from an older state what stops that user from continuing to transfer funds that are already inside their rollup ? So the attack is that i withdraw from old state, transfer my funds on rollup to a new address withdraw again. I just doubled my money.

[@adompeldorius](/u/adompeldorius) this may also be applicable to your design ?

---

**adompeldorius** (2021-10-19):

This is not an issue in my design, I replied [here.](https://ethresear.ch/t/springrollup-a-zk-rollup-that-allows-a-sender-to-batch-an-unlimited-number-of-transfers-with-only-6-bytes-of-calldata-per-batch/11033/10)


*(3 more replies not shown)*
