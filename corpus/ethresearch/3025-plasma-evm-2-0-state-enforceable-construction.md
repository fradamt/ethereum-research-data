---
source: ethresearch
topic_id: 3025
title: "Plasma EVM 2.0: state-enforceable construction"
author: 4000D
date: "2018-08-21"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-evm-2-0-state-enforceable-construction/3025
views: 8683
likes: 29
posts_count: 19
---

# Plasma EVM 2.0: state-enforceable construction

Onther Inc. came up with how to use EVM in plasma chain. Please review the approach they took. If you want explained version, you can check [here](https://hackmd.io/s/HyZ2ms8EX).

**Abstract**

Plasma EVM is a new version of Plasma that can execute EVM in plasma chain. We propose state-enforceable Plasma construction to guarantee only valid state submitted to root chain, providing a way to enter and exit account storage between two chains because each chain has identical architecture.

**2 Types of Block**

There are 2 types of block in Plasma EVM. `requestBlock` applies enter(deposit ERC20 or account storage) and exit request that users make in the RootChain contract. `nonRequestBlock` is typical block we know, to transfer ETH or to incur message-call.

**Request Block**

If users deposit ERC20 to participate plasma, operator have to include those requests in the very next block, `requestBlock`, to apply it to plasma chain. It can be considered as root chain enforces how the state should change. Exit can be applied in a similar way as enter does. If operator submits invalid blocks with invalid request, the challenge on it reverts the block. This makes only valid state committed to root chain.

**Non-request Block**

it contains all transactions not related to the enter & exit requests.

**Enter & Exit**

Enter & Exit mean moving a account’s single storage variable in one chain onto a corresponding contract in another chain. A contract is *requestable* if it can accept storage change by enter and exit requests.

**Fraud Proof**

There are many types of challenges. But the most important one is a challenge on the computation of EVM. TrueBit-like verification game provides a way to resolve validity of the computation. The game uses [solevm](https://github.com/parsec-labs/solevm-truffle), by Andreas Olofsson and PARSEC labs ,to verify EVM computation.

**Block Withholding Attack**

We may use CAS to enforce operator to submit block that all transactions are confirmed, but this approach cannot completely resolve the attak.

## Replies

**ldct** (2018-08-21):

I do not think the CAS construction (described in the hackmd) is sufficient for safety. Consider the following attack: Alice owns 10 eth in the plasma chain. Bob and the operator collude to send Alice some amount of eth that is known to Bob and the operator but unknown to Alice. The transaction data for this transaction is withheld, however the CAS cannot be challenged. The end result seems to be that Alice cannot exit her 10 eth any more, since she no longer has the witness data necessary for an exit.

---

**4000D** (2018-08-21):

I agree with you. you are correct. the construction cannot solve the withholding attack. The suggested solution is quite naive and immature to solve completely withholding attack. More research is required on it.

---

**YunJungHwan** (2018-08-22):

I read your article and found an error although it is off the main topic. You describe that if plasma chain is PBFT-consensus, block-withholding attack can be mitigated. But I think it is false sentence. Even in PBFT-consensus, if byzantine occupies two-thirds or more of the operators, block-withhoding attack definitely can be occured. If byzantines are 2/3+ of operators, they can make block without PBFT-consensus, just make block that they want and sign 2/3+ by operator’s private key. Because plasma contract is a kind of light-client, it can not find fraud for itself.

---

**Dapploper** (2018-08-23):

There is no need to know the witness data for exit. Let 10 eth be some tokens which is located in a arbitrary storage variable in requestable contract account. If Alice want to exit for this variable, the only thing she needs to know is trieKey of that variable. And this is known to everyone because information about requestable contract is open to both root chain and child chain. Even if Bob sends some tokens to Alice and Alice cannot notice it, it doesn’t matter. If there is withholding problem, Alice will exit using by trieKey and value.

---

**fistline** (2018-08-28):

It’s a good idea and I think it’s a good way to verify EVM.

we know that the plasma-chain has no stateless and  only checks transactions with UTXO.

I wonder how smart contracts exist in the plasma-chain.

Despite some vulnerabilities, I think it is a very innovative idea.

If you can make a plasma-chain that adds various functions to the EVM, it will be a plasma-chain suitable for a specific purpose.

As a result, the block-chain will have greater functionality and scalability as a system.

---

**Honglei-Cong** (2018-08-29):

about the exit request and withhold attack,

in the child chain, there’ll child-chain transactions, tx_0, tx_1 … tx_100,

correspondingly, there’ll state transitions, state_0, state_1, … state_100

if any participant in child-chain can provide state transition proof for any state of child-chain, for example,

state_proof_50, which is proof of from state_0 to state_50, and if Bob and operation is hold-attacking state from state_81 to state_100, Alice can make her exit request with state_proof_80.

Of course, during the challenge time, Bob can make his challenge, then the state_81 to state_100 can not be held internally?

---

**philosopher** (2018-09-02):

2.0 paper will be shared in a few days, which solves the problem that you mentioned.

---

**MihailoBjelic** (2018-09-03):

1. What is the reason for using two types of blocks? Why not simply include enter/exit transactions as parts of “regular” (nonRequest) blocks?
2. How do you exit contracts which hold funds than no one owns (who will sign/authorize the transfer)?
3. How do you exit contracts that can be modified by anyone (every modification is a valid state transition and it can block an exit)?
4. In your design, an operator MUST include an enter transaction in the first Plasma block created after the funds were deposited in the root chain contract. If the main chain block in which that deposit transaction was included turns out to be an uncle, we then have a situation where funds are not deposited on the main chain (uncle transactions are not included in the chain), but the equivalent amount is generated on the Plasma chain?

---

**4000D** (2018-09-04):

[@MihailoBjelic](/u/mihailobjelic)

1: User can always validate request block unlike non-request block that can be withheld by operator because the prepare step specify what requests should be included. It makes user to challenge on it in any situation if request block is submitted.

2, 3: It can be defined when the request contract is developed, who can exit and how the exit should change contract storage in plasma chain and root chain. It depends on developers.

4: It is common problem of Plasma if the root chain runs on pow. I think possible practical solutions are 6-confirm of Bitcoin and tracking down the correct fork of root chain. However, casper + sharding can solve it by providing finality.

---

**MihailoBjelic** (2018-09-04):

Thanks for the answers [@4000D](/u/4000d)! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Regarding my question no.1, please take a look at the potential problem I described here: [A potential problem with two "types" of blocks in Plasma MVP?](https://ethresear.ch/t/a-potential-problem-with-two-types-of-blocks-in-plasma-mvp/3202) and share your opinion. Thanks!

---

**philosopher** (2018-10-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/dapploper/48/2003_2.png)
    [Data Availability Solution for Plasma EVM without Confirmation](https://ethresear.ch/t/data-availability-solution-for-plasma-evm-without-confirmation/3294) [Plasma](/c/layer-2/plasma/7)



> This is a solution for Data availability problem of Plasma EVM designed by Onther Inc. And I believe this can solve most of the problems. I’m looking forward to get lots of feedback from you.
> This is very simplified version. I highly recommend to read this full version.
> A proposal for Data availability Solution of Plasma EVM
> (Korean)A proposal for Data availability Solution of Plasma EVM
> Abstract
> This article proposes a model to address the most problematic Data Availability (DA) in Plasma E…

CAS construction eliminated, and URB(User Request Block) concept is introduced.

URB is kind of “user generated fork” of Plasma chain’s exit/enter block, which solves data availability problem completely.

---

**qbig** (2018-12-10):

Could I ask a rather naive question here?

In there paper, it mentions that computation challenge could be carried out in the following way.

Here, how do we recover preState and postState from preStateRoot and postStateRoot? My understanding is that stateRoot is store in the blockHeader. But how could we recover a previous world state?

> If operator submits wrong  stateRoot , it can be challenged with  txData ,  preStateRoot , and  postStateRoot , using TrueBit-like verification game.
> postState=STFtx(preState,TXi)

---

**4000D** (2018-12-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/qbig/48/2221_2.png) qbig:

> Here, how do we recover preState and postState from preStateRoot and postStateRoot? My understanding is that stateRoot is store in the blockHeader. But how could we recover a previous world state?

Sorry for the late document update. The below description will be added to the paper.

For the computational challenge, it uses the TrueBit-like verification game. During the game, challenger can query the PostTransactionState before he query the EVM execution step. So intermediateStatesRoot is now useless because of 2-step query.

---

**u2** (2019-02-13):

[@4000D](/u/4000d)

About the exit request.

if any participant in child-chain can provide state transition proof for any state of child-chain, for example, state_proof_50, which is proof of from state_0 to state_50, and if Bob exit with the historical state and transaction, how could to prevent this situation?

---

**Dapploper** (2019-02-14):

Thank you for your question [@u2](/u/u2).

First, you do not need to provide any proof to exit, except for target to exit which is storage trie key-value. If the exit request is included and applied validly in subsequent ORB(Operator Request Block), we can all know the exit request is valid and she is entitled to exit that state. So it is not possible to exit with the historical data that you mentioned.

This is our implementation for contract, and please check the `startExit()`

Note that the `_to` parameter means target requestable contract address.


      [github.com](https://github.com/Onther-Tech/plasma-evm-contracts/blob/a59d4a87f3c232255c7150a71be3846b1f5a175a/contracts/RootChain.sol#L534-L551)




####

```sol

1. function startExit(
2. address _to,
3. bytes32 _trieKey,
4. bytes32 _trieValue
5. )
6. public
7. payable
8. onlyValidCost(COST_ERO)
9. returns (bool success)
10. {
11. require(_trieValue != bytes32(0));
12.
13. uint requestId;
14. requestId = _storeRequest(EROs, ORBs, false, _to, 0, _trieKey, _trieValue, true, false);
15.
16. emit RequestCreated(requestId, msg.sender, _to, 0, _trieKey, _trieValue, false, true, false);
17. return true;
18. }

```

---

**u2** (2019-02-14):

Thanks.

At [Plasma EVM 2.1 : State-enforceable, turing-complete plasma - HackMD](https://hackmd.io/s/HyZ2ms8EX#Child-chain)

> If a asset holder wants to exit, he makes a request on root chain with proofs. The request is queued on  exitRequests  and operator (or NULL_ADDRESS)  MUST  generate a transaction to  burn  the asset in the next block.

The description is not accurate, the exit request does not need proofs.

---

**u2** (2019-02-14):

According to the https://hackmd.io/s/HyZ2ms8EX#Exit step 6, I could find a function named `finalizeExit` in the contract, but where is it?

It’s the `applyRequest`, get it.

---

**Dapploper** (2019-02-15):

I agree with you. It would be more accurate expression getting rid of ‘with proofs’ phrase. I will revise the docs, thank you.

