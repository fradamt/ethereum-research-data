---
source: ethresearch
topic_id: 3391
title: Plasma snapp - fully verified plasma chain
author: josojo
date: "2018-09-15"
category: Layer 2 > Plasma
tags: [new-extension]
url: https://ethresear.ch/t/plasma-snapp-fully-verified-plasma-chain/3391
views: 16001
likes: 41
posts_count: 47
---

# Plasma snapp - fully verified plasma chain

Special thanks to the [roll_up team](https://github.com/barryWhiteHat/roll_up) for their hard work on building a first PoC for verifiable snapps (snark-dapps) and special thanks to Felix and Ben for their invaluable contribution to this idea.

# Plasma snapp:

## TL;DR

The following specification outlines a new plasma version which utilizes snarks to prove its integrity and validity. Via an interlinking between exit requests and deposits with the correctness proof of a block - the snark -, we are able to specify an implementation without any need for exit challenge games and confirmation signatures. Unfortunately, the concept of exit queues is still needed and users need to be online to receive payments.

Removing the exit games and confirmation signatures allow us to remove much of the complexity of plasma, which is currently hindering the implementation of more sophisticated protocols beyond simple token-transfers. This proposed version will facilitate to integrate more protocols into plasma by making the snarks itself handling these protocol advancements.

## Introduction:

Over the last half a year, there has been made tremendous advancements regarding fully verifiable plasma chains. New signature mechanism and hashing mechanism were found, helping to reduce proving times significantly.

These advancements enable the following with reasonable timings:

- storing the complete state of a plasma chain encoded as a StateRootHash on ethereum
- this StateRootHash can be updated by a central operator by providing a snark proving a valid state transition
- A valid state transition is proven within the snark by opening one or several leaves of the merkle tree describing the current state, checking the user’s signatures, doing predefined operations, updating the leaf and finally recalculate the stateRootHash.

How this can be in done in detail, you can find over here: https://github.com/barryWhiteHat/roll_up

However, snarks do not solve the problems associated with data unavailability. Also, the snarks need to be aware of any incoming deposit request to the plasma chain and outgoing withdrawal requests. This post will describe a solution for these two remaining issues.

## Proving valid state transactions

In this model, the state is described by leaves of the StateMerkleTree. Each leaf is a list of a

` [public key, amount of token, block height of last transfer].`

The plasma contract is aware of the current state, as we store it as the variable `StateRootHash` in the contract. it also stores the verification keys of the snarks of 3 different programs: P_transfer, P_deposit, and P_exits for 3 different kinds of state changes. These verification keys allow the plasma contract verifying that the state changes for a new block are actually valid ones.

Let’s call the program checking the correctness of a state transition based on transfer P_transfer:

`P_transfer(StateRootHash_i, [witness transactions data]) = (StateRootHash_(i+1))`

A transaction is a value transfer from one leaf to another leaf. P_transfers checks the following:

- Leaf of sending account exists
- Leaf of sending account has the needed balance for transfer
- The transfer transaction is signed by the private key associated with the public key stored in the sending leaf.
- Subtracts balance from sending leaf, update block height of last transfer, updates the StateRootHash
- Leaf of receiving account exists
- Updates balance and block height of last transfer of receiving account

The witness transaction data will be used by the snark proof, but they will never touch the rootchain. It is only needed to create once the witness of the snark.

This is pretty straightforward. But how do we make the plasma chain aware of deposits and withdrawal? We think the following trick will do the job:

The information of several deposits, which are sent to the plasma contract, can be hashed together to a `depositHash` by the plasma contract. By requiring the snark proof to take the `depositHash` as a public variable, we can enforce the snark proof to process all deposits.

The program P_deposit checking the correctness of deposits would look like this

`P_deposit(StateRootHash_i, DepositHash_i, [witness deposit data]) = (StateRootHash_(i+1))`

A deposit is a value transfer into an empty leaf. Whether a leaf is empty, we will store on the ethereum mainchain in a mapping: leafOccupation. P_deposit does the following:

- Insert public key and deposit amount into the leaf
- Updates the StateRootHash

The same can be done for exits: All exit requests can be collected by the plasma contract. The operator submits for each exit request the currently withdrawable balance from the plasma chain. Then these information are hashed together in an `exitRequestHash` and by making it a public input the snark, we can enforce the snark to process this exit request.

`P_exit(StateRootHash_i, ExitRequestHash_i, [witness exit data]) = (StateRootHash_(i+1))`

A withdrawal tries to exit all balance out of a leaf. The snark checks the following:

- Leaf has not sent or received a transaction within the last 7 days. (If this would be the case, the operator would have to set the predefined withdraw balance to 0, and the snark would be exited.)
- Leaf currently stores exactly the predefined balance
- Deletes the complete leaf, updates StateRootHash

Unfortunately, exits with a fraction of the balance are not supported by this protocol.

Note that the operator needs to set the withdrawal balance, as only he knows for sure the current balance. Still, the snark enforces the operator to set the correct balance, as otherwise he will not be able to find a proof. If someone makes an exit request, which is not valid, the operator will set the balance in the exit to 0. Exit request against non-occupied leaves are prevented by the plasma smart contract.

These three different programs allow the operator to append the plasma chain with 3 different block types (deposits, transfers and exits) by sending over the respective snark prover key. The plasma smart contract would enforce that registered pending exits would be processes at first, forcing the operator to submit exit blocks, before deposit or blocking transfer blocks. Likewise, if there are deposits pending since several blocks, then the plasma contract would force the plasma operator to include deposit blocks, before any transfer blocks are accepted. Only if there are no pending deposits or withdrawals, then the plasma chain allows appending transfers blocks.

## Roll back of the tip of unavailable chains

This above construction interlinks very well deposits and exits with the snark proofs. Unfortunately, it can not prevent the data unavailability case. It could always happen that the operator would publish a StateRootHash and nobody knows the content of this new state. Using priority queues for exits and an unwinding mechanism, we can solve the problem:

If the chain operator stops publishing new valid blocks for 3 days, then the plasma root chain contract would allow swapping the operators. Then anyone else can extend the plasma snapp chain provided that the new operator hands in valid snark for his new blocks.

If no one can build on the tip of the plasma chain, then the last block of the plasma chain will be removed and we wait for people building on the second-highest block. We will continue this removal process of the plasma chain tip, until it is extended again by another operator. If clients are storing all the data of the plasma chain, then they could always become the operator themselves in such a situation. Thus, if they do not agree with the reversal of a block of the chain tip, they need to become the operator. This is a fair mechanism, as everyone can stop the roll back of the history.

Payment receivers should only acknowledge their payment as accepted, once they have the complete new state of the plasma chain. Then they could theoretically always prevent the roll back of their received transaction by becoming the plasma operator themselves.

Becoming a plasma operator is a heavy task, but on the other side, we could also incentivise this heavily by slashing the original operator and rewarding the new operator with these slashed funds: During the plasma chain creation, the operator has to make a deposit of x ether. If the plasma chain was stopped and the operator swapped, then the new operator would receive a fraction of this ether per submitted valid block. This ensures that the plasma chain is continued for quite some time after the original operator was switched and everyone has the chance to leave the chain.

But there is one hook, unwinding transactions might be fine, but unwinding withdrawals is not possible. However, there is a workaround: We require that

- exit requests are only included in the ExitRequestHasH of the plasma block at least 40320 blocks (7 days) later after their account was sending the last transaction.
- users initiate their exit request at the latest 40320 blocks (7 days) after they see the unavailability of the data

If a users wants to withdraw, he sends a request to the plasma root-contract with the blocknr: blocknr of last touch. The plasma contract then requires the snark to process this exit exactly at min(blocknr + 40320, current block + 1). Especially the plasma smart contract will make sure that the transfer block: blocknr + 40320 is not accepted before the exit is processed.

Using this delayed mechanism, users funds are safe:

Imagine the block n is the first unavailable block.

1. If the operator keeps on building blocks, but stops building new blocks before the block n+40320, then all exits processed must be “old” transaction, which are anyways were not touched since the data unavailability. Even when blocks are unrolled until n, we require the new blocks to include the same exits, but without paying for the exits again. Thus no funds are lost.
2. If the operator keeps on building blocks and goes beyond the block n+40320, then every user should have already registered their exit and it should be withdrawn.

Note: In order to make this mechanism work, everyone needs to know when their transaction might have been included into the plasma chain. Especially, the scenario needs to be prevented where the operator produces unavailable blocks and includes in these blocks old transactions of somebody and thereby prevents this person to withdraw. Hence, every transaction submitted by a customer should be valid only for a specific block height.

Note2: A malicious operator could top up the balance of other users to touch their leaves in the unavailable block, and thereby give regular users a bad priority in the exit queue. This attack vector can be migrated by requiring the operator to hand over to the snark as witness a message signed from the receiving party: " I have seen block x and I am okay with receiving funds in block x+1".

If someone could come up with a better solution, which does not require the receiver to submit this message, this would be great

Note3: This specification has the nice property that we can use any hash function for the state merkle tree within the snarks, as these hash functions do not need to be executed in the evm at all. This is a huge benefit. Only the deposits and exits need to be done with kecca, as here the evm will need to execute them as well.

## Replies

**MihailoBjelic** (2018-09-15):

This is awesome! ![:star_struck:](https://ethresear.ch/images/emoji/facebook_messenger/star_struck.png?v=12) Kudos to the entire team and to Barry WhiteHat especially (I’ve been following his work, he’s a true zk Jedi)! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

A few questions off the top of my head:

1. Which type of tree is used for the state? I’m asking because you’re mentioning empty leafs in the text, and we often tie this to SMTs.
2. The structure of a leaf is: [public key, amount of token, block height of last transfer]. Can we imagine Ethereum state-like leafs: [pubKey, nonce, balance, codeHash, storageRoot]?  Perhaps with some different type of tree?
3. A deposit can be done into empty leafs only, and withdrawals cannot be partial. Can this be fixed/improved?
4. Transfer blocks can only be appended if there are no pending deposits or withdrawals. Isn’t this opening a trivial attack vector for a malicious user (they just need to constantly submit deposits and exits, recycling the same value and only paying for Tx fees)?
5. I like the idea of allowing anyone to extend the chain if the operator is inactive for 3 days, but how do you solve concurrency problem and prevent replaying of old Txs (especially if we have block unwinding before chain is extended) in that case?
6. Can you elaborate on this paragraph (especially the “blocknr: blocknr of last touch” part):

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> If a users wants to withdraw, he sends a request to the plasma root-contract with the blocknr: blocknr of last touch. The plasma contract then requires the snark to process this exit exactly at min(blocknr + 40320, current block + 1). Especially the plasma smart contract will make sure that the transfer block: blocknr + 40320 is not accepted before the exit is processed.

Thanks! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**PhABC** (2018-09-15):

Awesome work! Few questions / comments :

- I know a single operator is common in the plasma world, but why not using a PoS framework instead? Invalid state transitions are not possible, hence you don’t really need slashing conditions or challenges. I believe that now the only thing the set of operators need to worry about is choosing who can commit the next root updates. Using PoS seem to significantly reduce the risk of both censorship and data availability, which could lead to disastrous transaction reversion.
- Why the 7 day period? (this has probably been answered many times for other Plasma constructions)
- Doesn’t the fact that all transactions can be reverted significantly injure finality? This can be quite problematic for certain applications.

---

**josojo** (2018-09-15):

thanks, we are also very excited about this idea ![:laughing:](https://ethresear.ch/images/emoji/facebook_messenger/laughing.png?v=12) Although it still needs to be improved to be really practical.

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> Which type of tree is used for the state? I’m asking because you’re mentioning empty leafs in the text, and we often tie this to SMTs.
> The structure of a leaf is: [public key, amount of token, block height of last transfer] . Can we imagine Ethereum state-like leafs: [pubKey, nonce, balance, codeHash, storageRoot] ?  Perhaps with some different type of tree?

In this thread, I tried to focus the discussion on the interlinking of the chain deposits, the withdrawals and the data availability, that is why I left out the detailed description of many parts.

Probably, some tree variances are possible, but I would implement it with a very simple Merkle tree of a constant depth. This should be the easiest for the snarks.

Also making the leaves more sophisticated will work for sure, but then the snark will also take much more time to prove. Everything is currently limited by the complexity ( nr of constraints) a snark can handle.

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> Transfer blocks can only be appended if there are no pending deposits or withdrawals. Isn’t this opening a trivial attack vector for a malicious user (they just need to constantly submit deposits and exits, recycling the same value and only paying for Tx fees)?

We thought about this as well. The fee structure needs to be set in such a way that depositing into empty leaves is quite costly (maybe 5 dollar).

Also, withdrawals would be needed to be pre-registered, so that they can easily be processed in one block.

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> I like the idea of allowing anyone to extend the chain if the operator is inactive for 3 days, but how do you solve concurrency problem and prevent replaying of old Txs (especially if we have block unwinding before chain is extended) in that case?

The model as described does not prevent the replay of old txs. I am not sure, whether this is needed. People should not send transactions if the chain is unavailable. Also, if the transactions of the first unavailable block are replayed, this should not cause any big problems, as people intended to make this payment.

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> Can you elaborate on this paragraph (especially the “blocknr: blocknr of last touch” part):
>
>
>  josojo:
>
>
>
> If a users wants to withdraw, he sends a request to the plasma root-contract with the blocknr: blocknr of last touch. The plasma contract then requires the snark to process this exit exactly at min(blocknr + 40320, current block + 1). Especially the plasma smart contract will make sure that the transfer block: blocknr + 40320 is not accepted before the exit is processed.

We can not allow people to withdraw very recently received funds. If we would allow them to do it, then we are running into the trouble of potentially paying a withdrawal twice.

This is why we are recording in the leaf when the last payment was received. This recorded number in the leaf is the “blocknr of the last touch”

---

**josojo** (2018-09-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/phabc/48/35_2.png) PhABC:

> I know a single operator is common in the plasma world, but why not using a PoS framework instead? Invalid state transitions are not possible, hence you don’t really need slashing conditions or challenges. I believe that now the only thing the set of operators need to worry about is choosing who can commit the next root updates. Using PoS seem to significantly reduce the risk of both censorship and data availability, which could lead to disastrous transaction reversion.
> Why the 7 day period? (this has probably been answered many times for other Plasma constructions)

Single operators are just simpler to code and to reason about.

7 days is a usual plasma period, which gives everyone the chance to notice malicious events and gives them time to act up these.  In this construction, the user would need to register their exit within 7 days, if the blocks are unavailable.

![](https://ethresear.ch/user_avatar/ethresear.ch/phabc/48/35_2.png) PhABC:

> Doesn’t the fact that all transactions can be reverted significantly injure finality? This can be quite problematic for certain applications.

Everyone can stop the reverting of the transaction by becoming the operator. Hence, if you received some funds in a block n and have all data of this block n, then you will be able to stop the reversal process before it reverts your payment of block n.

It only changes finality, if you have unavailable blocks. But it is good to have non-finality if blocks are unavailable.![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12)

---

**MihailoBjelic** (2018-09-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> Also making the leaves more sophisticated will work for sure, but then the snark will also take much more time to prove.

Cool, got it. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> We thought about this as well. The fee structure needs to be set in such a way that depositing into empty leaves is quite costly (maybe 5 dollar).

IMHO, this is extremely hard to set right. Let’s say the deposit fee is $5 indeed, and let’s take a popular trading platform as an example. Users are frequently depositing funds, so the $5 is probably too much to ask (centralized services offer lower fees). On the other hand, if the platform is popular, $5 could be totally acceptable for a malicious competitor - she needs to invest only ~$29k to completely halt the transfers on the platform for the whole day ($5 every 15 seconds). It might help if these fees can be chain-specific (operators and/or users can define what suites their use case best).

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> The model as described does not prevent the replay of old txs. I am not sure, whether this is needed.

Yep, I guess this needs to be thought through. Seems to me like some messy situations could happen, but I might be wrong, of course. And what about the concurrency problem (everyone tries be an operator)?

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> This recorded number in the leaf is the “blocknr of the last touch”

Oh, I see. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) Now that you you’ve explained this to me, I wonder:

1. Why the exits are processed exactly at min(blocknr + 40320, current block + 1)? What if the current block = blocknr + 4 (this will be the min and the exit will be processed 60 seconds after it was submitted)?
2. Why we need to be sure that blocknr + 40320 is not accepted?

Please keep working on this, it’s really exciting and important! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**PhABC** (2018-09-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> which gives everyone the chance to notice malicious events and gives them time to act up thes

Sure, but in this construction, there are no malicious events possible that can be included in the new root. I’m still not sure I understand the need for the 7 days in this construction.

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> Everyone can stop the reverting of the transaction by becoming the operator. Hence, if you received some funds in a block n and have all data of this block n, then you will be able to stop the reversal process before it reverts your payment of block n.

So the incentive is for a user to pull all the data for the blocks on which they want finality, that makes sense. I wonder in practice how frequently this would happen. Each client could do checkpoints though, so that should be fine.

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> It only changes finality, if you have unavailable blocks. But it is good to have non-finality if blocks are unavailable

Why is it good? Even if a given block is unavailable, users still know that no faulty transition was included. So long as a future block becomes available again, users funds are fine.

---

**josojo** (2018-09-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> The model as described does not prevent the replay of old txs. I am not sure, whether this is needed.

Yep, I guess this needs to be thought through. Seems to me like some messy situations could happen, but I might be wrong, of course. And what about the concurrency problem (everyone tries be an operator)?

![](//ethresear.ch/user_avatar/ethresear.ch/josojo/40/1454_1.png) josojo:

The plasma smart contract will only allow one party to be the operator. I can think of several methods on how to choose the next operator via the smart contract.

I think the situation would not really be messy. If everyone stops using the unavailable chain immediately, then we will get a reorg of only depth 1. And this is also happening in ethereum regularly these days.

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> This recorded number in the leaf is the “blocknr of the last touch”

Oh, I see. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) Now that you you’ve explained this to me, I wonder:

1. Why the exits are processed exactly at min(blocknr + 40320, current block + 1)? What if the current block = blocknr + 4 (this will be the min and the exit will be processed 60 seconds after it was submitted)?
2. Why we need to be sure that blocknr + 40320 is not accepted?

1. We need to process the exit after the block: blocknr + 40320, so that funds can not be withdrawn to early in the following attack: operator makes a payment to himself in an unavailable block, withdraws these funds and then reverts the transaction later.
And we need to process the exit exactly in the block: blocknr + 40320 or earlier, so that any transaction included in the first unavailable block has also the chance to get withdrawn together with any transaction of a malicious operator. If we would only withdraw it in blocknr + 40321, then the operator could stop operating at block blocknr+ 40320 and revert his transaction, but not withdraw funds for the others.

---

**josojo** (2018-09-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/phabc/48/35_2.png) PhABC:

> which gives everyone the chance to notice malicious events and gives them time to act up thes

Sure, but in this construction, there are no malicious events possible that can be included in the new root. I’m still not sure I understand the need for the 7 days in this construction.

The malicious event is the following: The operator creates unavailable blocks, does some transactions tx1,…tx10, withdraws outputs of these transaction, starts the rollback of the chain and especially reverts tx1…tx10. In this case the other plasma chain participants needs to leave the plasma chain, before the operator can withdraw the outputs of the transactions tx1…tx10.

![](https://ethresear.ch/user_avatar/ethresear.ch/phabc/48/35_2.png) PhABC:

> It only changes finality, if you have unavailable blocks. But it is good to have non-finality if blocks are unavailable

Why is it good? Even if a given block is unavailable, users still know that no faulty transition was included. So long as a future block becomes available again, users funds are fine.

It’s because of the attack mentioned earlier in this block. The construction needs to rollback non-available blocks, to make sure that the plasma chain can be extended at some point in time. Otherwise, all funds would get stuck in the plasma contract

---

**PhABC** (2018-09-15):

I see the problem [@josojo](/u/josojo), thanks for explaining. It seems to me that reverting all txs is not a desirable feature however, it’s only currently a necessity because of block withholding.

I mentioned it above, but can’t you somewhat “solve” for this with using a PoS scheme instead? The easiest implementation I can think of is a central operator with a set of validator, a la Casper FFG. Validators can then sign a block `X` attesting they have all the data for `X`. 2/3 validators could be required for each new root, or have this mechanism on top at every Y new block. Then at least you have a economic finality like with Casper, potentially for every new block submitted, with very small risk of reverts. In case of necessity to reverse (no more checkpoints because operator doesn’t sign), then validators need to prove they can reconstruct previous root. If they can’t they get slashed.

---

**therne** (2018-09-15):

Very Interesting approach! ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=9) I have a question for expanding this model to more general use:

Seems like the current approach can accommodate the Account Model (and it’s really huge advance from UTXOs and coins) and a scenario that every state has an owner (e.g. Account Balances). However, State Transition on smart contract executable platforms is usually complex, and not able to have a certain owner of a state.

Suppose the scenario that Alice and Bob each deposit 10 PETH to a gambling game contract in Plasma Chain. Oracle reports that Alice is won, and Alice gets 20 PETH from the contract. In this “Reporting” transaction, transaction signer is Oracle but sending account is the contract and the beneficiary is Alice. So `P_transfer` would fail.

So not just the account transfer needs to be verified, but the computation needs to be verified if we premise the use of smart contract on plasma chain.

Can we expand the use of SNARKs to the computational verification? and will it costly?

---

**PhABC** (2018-09-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/therne/48/2207_2.png) therne:

> Can we expand the use of SNARKs to the computational verification? and will it costly?

Yes we can expand snarks to add more complex logic, but it will be significantly more expensive, especially in terms of time to create the proof. It’s also not trivial to build a SNARK circuit at the moment, much more difficult and constrained than writing smart contracts.

---

**kladkogex** (2018-09-17):

Can you explain what is the purpose of the transaction aggregation?

I am trying to understand what is the value of this.

ECDSA signature verification can be done at 10,000+ signatures per sec on a regular PC. What is currently the bottlleneck for ETH is network speed, it is the p2p network gossip that makes ETH run at < 20TPS. ECDSA verification part seems to be pretty OK and not requiring much of further optimization. I am not sure what value will SNARKS provide if one replaces regular signature verification with SNARKS.

---

**PhABC** (2018-09-17):

Calling `ECRECOVER` costs 3000 gas. If you did nothing else than verifying signatures, you could fit ~2200 `ECRECOVER` in a single block (8m gas). With SNARK, you can theoretically verify as many signatures as you want in a fix amount of gas, hence are not limited to the block limit.

In addition, sending signed messages to a single operator is more efficient than using a P2P messaging network.

---

**kladkogex** (2018-09-17):

very interesting - so if want to create SNARK for verification of 2200 signatures - how much computational time does take to create a SNARK proof for this ? And what is the size of SNARK?

And what is the aggregation proof creation time for 1000 signatures - it should be seconds otherwise the prover will fall behind …

---

**PhABC** (2018-09-17):

Based on a https://github.com/barryWhiteHat/roll_up/tree/master/src, I calculated that generating a proof for 1000 signatures with a merkle tree of depth 32 would take about 5-10 hours to generate the proof (~3947112000 contraints) using 256 machines on AWS. If we optimize the circuit (using Pedersen commitment, no hash full-rounds, less checks, more efficient signature scheme, etc.) we could maybe bring this down to ~30 minutes.

Now, if we have optimized hardware, bigger clusters and *maybe* better tools for distributed proof generation, it might be possible we could get the proof generation time to be under a minute for a few thousands txs, which I think is fine. We don’t need to commit every block per say anyway.

---

**kladkogex** (2018-09-17):

Have you considered using multisignatures


      [eprint.iacr.org](https://eprint.iacr.org/2018/483.pdf)


    https://eprint.iacr.org/2018/483.pdf

###

550.70 KB

---

**PhABC** (2018-09-17):

It’s definitely doable, but would increase the circuit size.

---

**josojo** (2018-09-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/phabc/48/35_2.png) PhABC:

> I mentioned it above, but can’t you somewhat “solve” for this with using a PoS scheme instead? The easiest implementation I can think of is a central operator with a set of validator, a la Casper FFG. Validators can then sign a block X attesting they have all the data for X . 2/3 validators could be required for each new root, or have this mechanism on top at every Y new block. Then at least you have a economic finality like with Casper, potentially for every new block submitted, with very small risk of reverts. In case of necessity to reverse (no more checkpoints because operator doesn’t sign), then validators need to prove they can reconstruct previous root. If they can’t they get slashed.

I think that a POS sheme will improve the situation a little, but the gains are not fundamental. I mean the incentives do not change much: a single operator can be slashed as well. Bigger companies might even be able to put a bigger bond, as the sum of single validators.

The finality is also given in the single operator model: If you have all the data belonging to a block and its root hash has been published to the plasma contract, then you can prevent any roll-back or make others to prevent the roll-back and hence, the blocks are final.

However, POS changes the network topology and split responsibilities, which is for sure good. It’s just questionable whether the benefits justify the new complexity.

---

**bharathrao** (2018-09-18):

ELI5 please: Does this need some sort of trusted setup? How is lambda handled/disposed of?

---

**kladkogex** (2018-09-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/phabc/48/35_2.png) PhABC:

> It’s definitely doable, but would increase the circuit size.

I meant a little different thing. You are using SNARKs to aggregate signatures essentially into a single signature, but you could use the multi-signature scheme cited to aggregate - it seems that using the multisignature scheme could be more efficient.  The miner would simply aggregate multisignatures into one …


*(26 more replies not shown)*
