---
source: ethresearch
topic_id: 11033
title: "Springrollup: A zk-rollup that allows a sender to batch an unlimited number of transfers with only 6 bytes of calldata per batch"
author: adompeldorius
date: "2021-10-17"
category: zk-s[nt]arks
tags: [zk-roll-up, rollup, layer-2]
url: https://ethresear.ch/t/springrollup-a-zk-rollup-that-allows-a-sender-to-batch-an-unlimited-number-of-transfers-with-only-6-bytes-of-calldata-per-batch/11033
views: 7160
likes: 11
posts_count: 20
---

# Springrollup: A zk-rollup that allows a sender to batch an unlimited number of transfers with only 6 bytes of calldata per batch

(The newest version of this document can always be found on [hackmd](https://hackmd.io/@albus/BkMFnuNXK) or [GitHub](https://github.com/adompeldorius/springrollup))

We introduce Springrollup: a Layer 2 solution which has the same security assumptions as existing zk-rollups, but uses much less on-chain data. In this rollup, a sender can batch an arbitrary number of transfers to other accounts while only having to post their address as calldata, which is 6 bytes if we want to support up to 2^48 ~ 300 trillion accounts. As a by-product we also achieve increased privacy, since less user data is posted on-chain.

## General framework

We start by introducing the general framework that we will use to describe the rollup.

The rollup state is divided in two parts:

- On-chain available state: State with on-chain data availability. All changes to this state must be provided as calldata by the operator.
- Off-chain available state: State without on-chain data availability. This state will be provided by the operator off-chain.

The on-chain available state can always be reconstructed from the calldata, while the off-chain available state may be withheld by the operater in the worst case scenario (but we will show that our rollup design guarantees that users’ funds will still be safe).

The L1 contract stores

- a common merkle state root to both parts of the state.
- the rollup block number
- the inbox

The *inbox* is a list of deposit and withdrawal operations that users have added on L1. When posting a rollup block, the operator must process all operations in this list before processing the L2 operations included in the rollup block.

The rollup operator is allowed to make changes to the rollup state by posting a rollup block to the L1 contract, which must include the following as calldata:

1. The new merkle state root.
2. A diff between the old and the new on-chain available state.
3. A zk-proof that there exist a state having the old state root and a list of valid operations (defined below) that when applied to the old state, after processing all operations in the inbox, gives a new state having the new state root, and that the diff provided above is the correct diff.

If the above data is valid, the state root is updated and the inbox is emptied.

**Remark:** What we have described so far is a general description of several L2 solutions. For instance:

- If the whole rollup state is in the on-chain available part, and the off-chain available state is empty, we get existing zk-rollups.
- If the whole rollup state is in the off-chain available part and the on-chain available state is empty, we get validiums.
- If both parts of the state contain account state, we get volitions (e.g. zk-porter).

Our proposal is neither of the above, and is described below.

## Overview of the rollup design

#### Transfers

When a user sends L2 transfers to the operator, they are not processed immediately. Instead, they are added to a set of pending transactions in the off-chain available state. After the rollup state has been updated by the operator, the user recieves (off-chain) witnesses to both their balance and to all their pending transactions in the new rollup state from the operator. In order to process their pending transactions, the user signs and sends an operation `ProcessTransactions` to the operator. The operator then adds this operation in the next rollup block, which processes all the pending transactions of the sender, and sets a value `lastSeenBlockNum(sender) = blockNum` in the on-chain available state, where `blockNum` is the last block number. After a rollup block has been posted, the operator provides witnesses to all updated balances to the affected users.

#### Calldata usage

The only data that needs to be provided as calldata in each rollup block (ignoring deposits and withdrawals) is the set of accounts that have updated their `lastSeenBlockNum`, i.e. 6 bytes per address (supporting up to 2^48 ~ 300 trillion accounts). This is already less calldata than regular rollups if each user only added one pending transfer before calling `processTransactions`, and is much less per transfer when a user processes a large batch of transfers at once.

#### Frozen mode

Under normal circumstances, a user may withdraw their funds by sending an L2 transfer to an L1 address that they own. If the transfer is censored by the operator, the user may instead send a `ForceWithdrawal` operation to the inbox on L1, which the operator is forced to process in the next rollup block.

If the operator doesn’t post a new rollup block within 3 days, anyone can call a `Freeze` command in the L1 contract. When the rollup is frozen, users may withdraw the amount determined by

- their balance in a block b with blockNum >= lastSeenBlockNum(address),
- minus the total amount sent from the user in the pending transactions in the same block b (if blockNum == lastSeenBlockNum(address)),
- plus the total amount sent to them in a set of pending transfers in blocks at least as new as b, that have all been processed.

The user must provide witnesses to all the above data in order to withdraw their funds.

The security of the protocol is proven by showing that each user always has the necessary witnesses to withdraw their funds, which we will do in the detailed description below.

## Detailed description of the protocol

### Rollup state

Each L2 account’s balance is represented as the sum of a balance stored in the on-chain available state and a balance stored in the off-chain available state:

`balanceOf(address) = onChainBalanceOf(address) + offChainBalanceOf(address)`

The reason for this is to simplify deposits and withdrawals. When a user makes a deposit or a withdrawal on L1, only their on-chain balance is updated. On the other hand, when an L2 transfer is processed, only the off-chain balances of the sender and recipient are updated.

Note that either `onChainBalanceOf(address)` or `offChainBalanceOf(address)` may be negative, but their sum is always non-negative.

#### On-chain available state

```auto
OnChainAvailableState =
  { lastSeenBlockNum : Map(L2 Address -> Integer) # The block number of a block in which the owner of the address possess a witness to their balance and pending transactions.
  , onChainBalanceOf : Map(L2 Address -> Value) # On-chain part of the balance of an account.
  }
```

#### Off-chain available state

```auto
OffChainAvailableState =
  { offChainBalanceOf : Map(L2 Address -> Value) # Off-chain part of the balance of an account.
  , nonceOf : Map(L2 Address -> Integer) # The current nonce of an account.
  , pendingTransactions : Set(Transaction) # A set of transactions that have been added, but not processed yet.
  }
```

where `Transaction` is the type

```auto
Transaction =
  { sender : L2 Address
  , recipient : L2 address or L1 address
  , amount : Value
  , nonce : Integer
  }
```

### L2 operations

The operator is allowed to include the following operations in a rollup block.

#### AddTransaction

```auto
AddTransaction(
    transaction : Transaction
  , signature : Signature of the transaction by the sender
  )
```

Adds the transaction to the set `pendingTransactions` and increases `nonceOf(sender)` by one. It is required that the transaction’s nonce is equal to the current `nonceOf(sender)`.

#### ProcessTransactions

```auto
ProcessTransactions(
    sender : Address
  , blockNum : Integer
  , signature : Signature of the message "Process transactions in block blockNum" by the sender
  )
```

This operation processes all pending transactions *from* `sender` in the last published rollup block (i.e. not the currently in-process block), which is required to have block number `blockNum`, and sets `lastSeenBlockNum(sender)` to `blockNum`.

When a transaction is processed, it is removed from `pendingTransactions`, the amount is subtracted from `offChainBalanceOf(sender)` and added to `offChainBalanceOf(recipient)`. If the sender has insufficient funds for the transfer, meaning that `amount > balanceOf(sender)`, the transaction fails and is just removed from `pendingTransactions`.

The sender should make sure they possess the witnesses for their balance and all their `pendingTransactions` in block `blockNum` before sending this operation to the operator, since they would need this in order to withdraw in case the rollup is frozen.

### L1 operations

The following operations can be added by users to the inbox in the L1 contract.

#### Deposit

```auto
Deposit(
    toAddress : L2 Address
)
```

Adds the amount of included ETH to `onChainBalanceOf(toAddress)`.

#### ForceWithdrawal

```auto
ForceWithdrawal(
    sender : L2 Address
  , recipient : L1 Address
  , signature : Signature of the message "Withdraw all ETH to recipient" by the sender
  )
```

Withdraws `balanceOf(sender)` ETH to `recipient` on L1 and decreases `onChainBalanceOf(sender)` by the withdrawn amount (i.e. sets `onChainBalanceOf(sender)` to `-offChainBalanceOf(sender)`).

### Frozen mode

If the operator doesn’t publish a new block in 3 days, anyone can call a freeze command in the contract, making the rollup enter a *frozen mode*.

When the rollup is frozen, the users that have unprocessed deposits in the inbox can send a call to the L1 contract to claim the deposited ETH in the inbox.

In order to withdraw from an L2 account, a user Alice must provide to the L1 contract the witnesses to the following.

1. offChainBalanceOf(alice) in some rollup block b with blockNum >= lastSeenBlockNum(alice).
2. If blockNum == lastSeenBlockNum(alice), we also require witnesses to the set of pending transactions from Alice in block b. We denote the total sent amount as sentAmount.
3. A set of pending transfers to Alice. Each pending transfer must have been processed, meaning that it’s block cannot be newer than the sender’s lastSeenBlockNum. Also, each pending transfer’s block must be at least as new as b above (otherwise it would already be included in offChainBalanceOf(alice)). We denote the total recieved amount as recievedAmount.

When the L1 contract is given the above data, it sends to Alice the amount (if non-negative) given by

```auto
  offChainBalanceOf(alice)
+ onChainBalanceOf(alice)
+ recievedAmount
- sentAmount
```

and decreases `onChainBalanceOf(alice)` by the withdrawn amount. If the above amount is negative, the withdrawal request fails and nothing happens.

**Remark:** It may happen that Alice withdraws her funds, and then later is made aware of a transfer from Bob that she didn’t include in the withdrawal. She may then add a new withdrawal request where she include Bob’s transfer along with the same transfers as last time.

## Example 1: Single transfer from Alice to Bob

Alice wants to send 5 ETH to Bob. Her current nonce is 7, and her current `lastSeenBlockNum` is 67. The procedure is as follows:

1. Alice signs and sends transaction

```auto
transaction =
    ( sender = alice
    , recipient = bob
    , amount = 5 ETH
    , nonce = 7
    )
```

to the operator.
2. The operator includes the operation AddTransaction(transaction, signature) in the next rollup block (number 123), with the effect of adding the transaction to the set of pending transactions in the rollup state.
3. After rollup block 123 is published on-chain, the operator sends a witness of the newly added pending transaction to Alice.
4. Once Alice have the witness of her pending transaction in block 123, she signes the message “Process transactions in block 123” and sends this signed message to the operator.
5. The operator includes the operation

```auto
ProcessTransactions(
  address = alice
, blockNum = 123
, signature = Signature of the message "Process transactions in block 123" by Alice
)
```

in the next rollup block, which has block number 124. Alice’s lastSeenBlockNum is set to 123, and the transfer to Bob is processed.
6. The operator gives Alice and Bob the witnesses to their updated balances in block 124.

### Security argument

The operator may misbehave in several stages in the example above. If this happens, users can exit by sending a `ForceWithdrawal` operation to the L1 inbox. Then, either the operator will process the withdrawal requests in the next rollup block, or it will stop publishing new blocks. If the operator doesn’t add a new block in 3 days, anyone can call the freeze command on L1, and the rollup is frozen. For Alice and Bob, there are two scenarios:

- The transfer from Alice to Bob has not been processed (it is either pending or wasn’t included at all). Then Alice will use a witness of her balance in some block at least as new as 67 (which is her lastSeenBlockNum) to exit.
- The transfer was processed, but the operator didn’t provide the witnesses to the new balances of Alice and Bob. In this case, Alice have a witness of her balance in block 123 and of the pending transfer to Bob (otherwise she wouldn’t sign the ProcessTransactions operation). Alice can then withdraw using the witness of her balance in block 123, plus a witness to the pending transfer to Bob. Bob may withdraw with a witness to his balance in some block at least as new as his lastSeenBlockNum, plus a witness of the pending transfer from Alice, which he could get from Alice.

In all both cases, both Alice’s and Bob’s (and all other user’s) funds are safe.

## Example 2: Batch of transfers from Alice to 1000 recipients

Suppose Alice is a big employer and want to send salaries to 1000 people. She may then batch the transfers to save calldata. The procedure for this is the same as in Example 1 above, but she will add all 1000 transactions to `pendingTransactions` before sending the `ProcessTransactions` operation. Note that it is not necessary to add all 1000 transfers in the same rollup block, she may continue to add pending transactions in many rollup blocks before calling `ProcessTransactions`.

## Discussion

### Privacy

This design has increased privacy compared to existing rollups, since an honest operator will not make users balances or transactions public, but only give each user the witnesses to their updated balances.

### Token support

We described a MVP without token support, but it is trivial to add support for ERC-20 tokens and NFTs by adding separate balances for these.

### Smart contracts

Further research should be done to figure out how to support smart contracts in this design.

## Related ideas

- Minimal fully generalized S*ARK-based plasma
- Plasma snapp - fully verified plasma chain
- Plasma snapp-1-bit
- MVR - Minimally Viable Rollback
- Adamantium - Power Users
- A zkRollup with no transaction history data to enable secret smart contract execution with calldata efficiency - #19 by leohio

## Replies

**barryWhiteHat** (2021-10-18):

So basically you are saying

We can remove the on chain data to just addresses that were touched if we require a signature from the recipient of each payment. Because if they sign it ensures they know the new state and a data availability attack against them won’t happen. If a data availability attack happens against someone else they will just do a plasma type exit game to withdraw their funds ?

---

**adompeldorius** (2021-10-18):

Yes, I think that’s a nice summary, with the possible exception of that there is no exit game! Or at least not the Plasma kind of exit game of  where there is a challenge period. It is not possible to exit with other users’ funds in this design.

---

**barryWhiteHat** (2021-10-18):

Cool. So how do you handle a situation where user a , b and c exist in the system. User a and b updates their balance and refuses to share the new value with user c. How does user c generate a ZKP to move their funds beauces they don’t have the witness data ?

---

**adompeldorius** (2021-10-18):

Users don’t generate ZK-proofs, they just sign L2 transactions and send them to the operator which generates a ZK-proof which is included in a rollup block. In the current design, there is a designated rollup operator.

EDIT: Note that there is a possible scenario where the operator stops producing blocks, and Alice is missing the witnesses for the transfers sent to her in blocks that are newer than the one in which she has a witness of her balance. In this case, we assume that it is in the senders best interest to provide these witnesses to Alice.

---

**barryWhiteHat** (2021-10-18):

Ah right. That is a big assumption and a possible attack. So i would colude with the operator to send a random amount between (0.0000000000001 0.000099999999) tokens to each user. They need to know this number in order to withdraw or transfer and i can basically extort them.

Am i understanding correctly ?

---

**adompeldorius** (2021-10-18):

No no, in that case Alice can still withdraw with the witness to an earlier balance (in a block at least as new as the users lastSeenBlock), plus witnesses to the recieved funds she DOES have.

---

**barryWhiteHat** (2021-10-18):

What if an attacker waits until a transaction from Alice is in flgith. And then does data availbilty attack and mines that transaction in the same block. Do you allow Alice to withdraw from the older state even tho the lastSeenBlock is the current block ?

---

**adompeldorius** (2021-10-18):

lastSeenBlocNum is always the last published block (while the new block is in-process). If Alice have her data in the last published block (say block 123) she will sign and send “Process transactions in block 123” to the operator. Then either the operator includes this operation in block 124, or it can’t be included at all (not even in a later block).

---

**adompeldorius** (2021-10-19):

Reply to [this post.](https://ethresear.ch/t/a-zkrollup-with-no-transaction-history-data-to-enable-secret-smart-contract-execution-with-calldata-efficiency/10961/20)

> So the idea here is you allow users to withdraw from a previous state if a transaction for that address has not already been included ?
>
>
> My concern here is that after a user has withdraw from an older state what stops that user from continuing to transfer funds that are already inside their rollup ? So the attack is that i withdraw from old state, transfer my funds on rollup to a new address withdraw again. I just doubled my money.
>
>
> @adompeldorius this may also be applicable to your design ?

This is not an issue in my design, because the user’s balance is represented as a sum of a balance stored in the on-chain available state and a balance stored in the off-chain available state:

balanceOf(address) = onChainBalanceOf(address) + offChainBalanceOf(address)

So when you withdraw, your on-chain available balance decreases, and so the amount left for withdrawals (or transfers) is decreased.

---

**Killari** (2021-10-19):

What happens if Alice doesn’t sign the txt on step 4. Does the operator need to build a new block and ask everyone’s signatures again (except Alices)?

---

**adompeldorius** (2021-10-19):

If Alice doesn’t sign in step 4, her transaction would still be in the set of pending transactions. It is possible for Alice to wait for many blocks before sending the message to process her pending transactions.

Example: Alice doesn’t sign the message "Process transactions in block 123” in step 4.

Step 5: The operator publishes block 124 without the above message from Alice. Her transactions are still pending.

Step 6: The operator publishes blocks 125-137 while Alice is sleeping. Alice’s transactions are still in the set of pending transactions.

Step 7: Alice wakes up and sees that the current block is block number 137. She gets witnesses to her balance and pending transactions in block 137 from the operator.

Step 8: After recieving the witnesses, Alice signs and sends the message “Process transactions in block 137” to the operator.

Step 9: The operator includes Alice’s message in block 138, and Alice’s transactions are processed.

---

**invocamanman** (2021-10-19):

Thank you, it’s a very interesting approach!

I have a couple of questions, sorry if I misunderstood something:

- How the balance can go from onChain to offChain?
- Why in frozen mode the sentAmount is subtracted, since this amount is in pending state? If this sentAmount is substracted, does the reciever can claim it? if yes, how to ensure that Alice has enough balance to sent that amount since that check is done when processing the transaction?

---

**adompeldorius** (2021-10-20):

Hi, thanks!

![](https://ethresear.ch/user_avatar/ethresear.ch/invocamanman/48/7670_2.png) invocamanman:

> How the balance can go from onChain to offChain?

Not sure if I understand your question, but I will give it a try.

The on-chain available balance keeps track of the amount that is deposited to the account from L1 *minus* the amount withdrawn to L1 from the account.

The off-chain available balance, on the other hand, keeps track of the amount recieved by L2 transfers to the account *minus* the amount sent by L2 transfers from the account.

The balance does not move between these two, you just define the balance of an account to be the sum of these two balances. Does this clear things up? If not, please ask again.

![](https://ethresear.ch/user_avatar/ethresear.ch/invocamanman/48/7670_2.png) invocamanman:

> Why in frozen mode the sentAmount is subtracted, since this amount is in pending state? If this sentAmount is substracted, does the reciever can claim it? if yes, how to ensure that Alice has enough balance to sent that amount since that check is done when processing the transaction?

Keep in mind that the sent amount in the pending transfers is *only* subtracted in the edge case where Alice uses the `offChainBalance(Alice)` in the block `lastSeenBlockNum(Alice)`. The reason for this is that the pending transfers in `lastSeenBlockNum(Alice)` were actually processed in the next block `lastSeenBlockNum(Alice)+1`, but Alice’s balance in `lastSeenBlockNum(Alice)` doesn’t reflect that, so the sent amount must be subtracted.

---

**invocamanman** (2021-10-20):

Hi! thank you for answers, really appreciate it ^^

![](https://ethresear.ch/user_avatar/ethresear.ch/adompeldorius/48/6325_2.png) adompeldorius:

> The balance does not move between these two, you just define the balance of an account to be the sum of these two balances. Does this clear things up? If not, please ask again.

I’m sorry, I will ask this way: If Alice has 1 ether in ethereum, what is the flow to deposit into the rollup and then transfer that ether to Bob by an L2 transaction?.

![](https://ethresear.ch/user_avatar/ethresear.ch/adompeldorius/48/6325_2.png) adompeldorius:

> Keep in mind that the sent amount in the pending transfers is only subtracted in the edge case where Alice uses the offChainBalance(Alice) in the block lastSeenBlockNum(Alice). The reason for this is that the pending transfers in lastSeenBlockNum(Alice) were actually processed in the next block lastSeenBlockNum(Alice)+1, but Alice’s balance in lastSeenBlockNum(Alice) doesn’t reflect that, so the sent amount must be subtracted.

Now I get it! But I have a follow-up question to this.

Suppose this situation above:

![](https://ethresear.ch/user_avatar/ethresear.ch/adompeldorius/48/6325_2.png) adompeldorius:

> Alice can then withdraw using the witness of her balance in block 123, plus a witness to the pending transfer to Bob. Bob may withdraw with a witness to his balance in some block at least as new as his lastSeenBlockNum, plus a witness of the pending transfer from Alice, which he could get from Alice.

Where the transaction from Alice to Bob should fail when processed because Alice does not have enough balance `amount > balanceOf(Alice)`. Does Bob could withdraw that amount as in this example?

---

**adompeldorius** (2021-10-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/invocamanman/48/7670_2.png) invocamanman:

> If Alice has 1 ether in ethereum, what is the flow to deposit into the rollup and then transfer that ether to Bob by an L2 transaction?.

Ahh, I see. So the procedure would be this:

Step 1: Alice calls the function `Deposit(toAddress)` in the rollup L1 contract, where `toAddress` is her L2 address, with 1 ETH included in the call. I didn’t specify how L2 addresses are generated, but it would be similar to existing zk-rollups. It could be something like this: Each L2 address is associated to a L1 address in the rollup state. If Alice calls `Deposit()` without specifying an L2 address, it is sent to the L2 address associated to Alice’s L1 address, which is created if it doesn’t exist.

Step 2: The `Deposit` function above adds the deposit request to the *inbox*, and the operator is forced to process it in the next rollup block.

Step 3: After the operator has processed the deposit request in the next rollup block, Alice may create a transaction and sign it using the private key of the L1 address associated to her L2 address. The signed transaction is sent to the operator.

Step …: The rest is the same as in example 1.

![](https://ethresear.ch/user_avatar/ethresear.ch/invocamanman/48/7670_2.png) invocamanman:

> Where the transaction from Alice to Bob should fail when processed because Alice does not have enough balance amount > balanceOf(Alice). Does Bob could withdraw that amount as in this example?

Nice catch! We must make sure that Bob is not allowed to get the funds from the transfer if it failed.

One way to make sure of this is to make it illegal for the operator to add a pending transaction if this would cause the total amount sent in the pending transfers to be greater than the sender’s current balance. That way, we ensure that processing a pending transfer would always be valid.

---

**invocamanman** (2021-10-20):

Thank you very much for your answers again!

![](https://ethresear.ch/user_avatar/ethresear.ch/adompeldorius/48/6325_2.png) adompeldorius:

> Step 3: After the operator has processed the deposit request in the next rollup block, Alice may create a transaction and sign it using the private key of the L1 address associated to her L2 address. The signed transaction is sent to the operator.

But in this 3 steps, only the `onChainBalance` is updated and you need to have `offChainBalance` in order to process L2 transactions right?

![](https://ethresear.ch/user_avatar/ethresear.ch/adompeldorius/48/6325_2.png) adompeldorius:

> One way to make sure of this is to make it illegal for the operator to add a pending transaction if this would cause the total amount sent in the pending transfers to be greater than the sender’s current balance. That way, we ensure that processing a pending transfer would always be valid.

Thank you! ^^

I think might be more tricky than that because, could be some pending valid transactions, and then the user can put a `forceWithdrawal` in the inbox before processing that transactions and therefore invalidate them.

---

**adompeldorius** (2021-10-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/invocamanman/48/7670_2.png) invocamanman:

> ut in this 3 steps, only the onChainBalance is updated and you need to have offChainBalance in order to process L2 transactions right?

Yes, only the `onChainBalance` is increased to 1 ETH, while the `offChainBalance` is unchanged (0 if it’s a brand new L2 address). The thing is that we allow either `onChainBalance(address)` or `offChainBalance(address)` to be negative, as long as the sum of them is positive. So if Alice has deposited 1 ETH to a new L2 address, she has `onChainBalance(Alice)=1ETH` and `offChainBalance(Alice)=0 ETH`. If she then sends 1 ETH to Bob on L2, she will have `onChainBalance(Alice)=1 ETH` and `offChainBalance(Alice)=-1 ETH` after this transfer is processed, so her balance will be 1 ETH - 1ETH = 0 ETH.

![](https://ethresear.ch/user_avatar/ethresear.ch/invocamanman/48/7670_2.png) invocamanman:

> I think might be more tricky than that because, could be some pending valid transactions, and then the user can put a forceWithdrawal in the inbox before processing that transactions and therefore invalidate them.

Hmm, yeah you’re right. Perhaps a better way would be to make it illegal for the operator to add a `ProcessTransaction` for Alice if she doesn’t have enough funds for all of her pending transactions.

---

**invocamanman** (2021-10-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/adompeldorius/48/6325_2.png) adompeldorius:

> she has onChainBalance(Alice)=1ETH and offChainBalance(Alice)=0 ETH. If she then sends 1 ETH to Bob on L2, she will have onChainBalance(Alice)=1 ETH and offChainBalance(Alice)=-1 ETH after this transfer is processed, so her balance will be 1 ETH - 1ETH = 0 ETH.

I finally get it!!! thank you

![](https://ethresear.ch/user_avatar/ethresear.ch/adompeldorius/48/6325_2.png) adompeldorius:

> Hmm, yeah you’re right. Perhaps a better way would be to make it illegal for the operator to add a ProcessTransaction for Alice if she doesn’t have enough funds for all of her pending transactions.

Yes, I think this fix it ^^

---

**adompeldorius** (2021-10-20):

Cool! Thanks for your questions, I will update the document with clarifications/fixes for the things you brought up!

