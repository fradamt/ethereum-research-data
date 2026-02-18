---
source: ethresearch
topic_id: 2128
title: Simple Fast Withdrawals
author: kfichter
date: "2018-06-03"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/simple-fast-withdrawals/2128
views: 16551
likes: 24
posts_count: 28
---

# Simple Fast Withdrawals

Design from conversation with vi, David Knott, Ben Jones, and Eva Beylin. Thanks to Eva Beylin & Kelsie Nabben for review/edits.

---

## TL;DR

We can enable fast withdrawals without Plasma contracts by taking advantage of root chain smart contracts. Withdrawals can then be handled as tokenized debt, and we can build a marketplace from there.

## Background

Fast withdrawals are a construction in Plasma that effectively boil down to an atomic swap between the Plasma chain and the root chain. They’re useful because Plasma withdrawals are slow (2 weeks, in our implementation), and people usually want their money quite quickly. The Plasma paper discusses one such construction that relies on outputs being locked to contracts:

> Funds are locked to a contract on a particular output in the Plasma chain. This occurs in a manner similar to a normal transfer, in that both parties broadcast a transaction, and then later commit that they have seen the transaction in a Plasma block. The terms of this contract is that if a contract is broadcast on the root blockchain and has been finalized, then the payment will go through in the Plasma chain.

However, we currently don’t support funds locked to contracts in Plasma. This post describes a simple fast withdrawal mechanism that ensures the liquidity provider will be paid after the full withdrawal time without the need of Plasma contracts. Like the original fast withdrawal design, this design relies on Plasma data availability.

## Pay-to-Smart-Contract

We take advantage of the fact that Ethereum smart contracts cannot produce signatures, and therefore cannot spend funds on the Plasma chain. However, Ethereum contracts *can* initiate an exit by calling the Plasma contract. This makes it possible for a user to send child chain funds to the address of an Ethereum contract, where these funds can no longer be spent but can be withdrawn.

In the case that a user doesn’t want to wait for the Plasma exit, we can enable fast withdrawals by deploying a special contract to Ethereum - let’s call this a “liquidity contract”. Any user may force the contract to trigger a slow Plasma exit of any utxo where the user is the sender. This action creates an ERC721 token for the user that represents the right to receive the value of the exit once it processes. The user can then quickly and simply receive value of their utxo (minus a fee in the form of a discount) by transferring or selling this token to any other user.

For clarity, here’s a quick user flow:

1. Alice has 10 ETH on the child chain and wishes to quickly withdraw to the Plasma chain instead of waiting two weeks.
2. Bob is okay waiting two weeks for the exit to process, so he’s willing to front Alice the money now in exchange for a discount.
3. Alice and Bob will use an Ethereum liquidity contract.
4. Alice sends her 10 (child chain) ETH to the address of the liquidity contract. This a Plasma transaction, not an Ethereum transaction.
5. Alice sees that her transaction to the contract has been included in the Plasma chain. The contract now owns a utxo received from Alice.
6. Alice calls a function in the smart contract that triggers an exit from this utxo. The contract credits Alice with a token representing the future funds from this exit.
7. Bob is willing to pay 9 ETH for a 10 ETH token that will “mature” (to take some bond terminology) in two weeks.
8. Bob has data availability, checks the Plasma chain, and sees that Alice’s exit is not invalid. Bob tells Alice that he’s willing to purchase her exit token.
9. Alice sells her 10 ETH token to Bob for 9 ETH. Alice receives 9 ETH now, and Bob will receive 10 ETH once the exit processes. Bob has “earned” 1 ETH (in the form of a discount) for providing a liquidity service to Alice.

## Markets

To ensure that Alice is able to receive funds from the Plasma chain quickly, there must be a marketplace for her tokens. It’s possible to create any number of schemes that give users the best possible price. For example, each user could hold a short auction for their token or could arrange a sale out-of-band.

It’s also possible to reintroduce the concept of rating agencies to create more liquid markets. These agencies would attest to the validity of the exit. Liquidity providers could then give a market price for each token (based on value & time to process). This means that users can quickly sell their tokens and receive their funds without having to spend time finding a liquidity provider or waiting for an auction to complete.

Furthermore, it’s probably also possible to sell parts of a token, but gas costs make this more infeasible for low-value tokens.

An auction seems like the simplest mechanism in the short-term.

## Notes

As always, feedback and comments are more than welcome. Please feel free to challenge any part of this, there very well may be issues.

## Replies

**sg** (2018-06-03):

Revised: Regarding procedure #5, UTXO has been owned by contract, and it is already psuedo-burned. My concern was pointless.

---

We should prohibit further spending of submitted UTXO on child chain because malicious user is able to use that UTXO after recieving fast withdrawal fund.

Correct me if I am missing that Plasma popular spec has involved UTXO locking logic. Unless we’d better to define it. There might be many corner cases which is about lock handling after challenge succeeded, or about when an user re-enter to that child chain. In the both cases we must handle lock state consistently.

Additionally, the lock handler must not rely on child chain Tx/Contract. This is because of block withholding on child chain. The virtue of Mass Exit security model is being independent from child chain Tx, hence everyone can flee from malicious block halting. If we want to make Tx locking logic for all exits, this restriction is quiet headachy.

---

**y-matsuwitter** (2018-06-03):

From my understanding, this withdrawal spec can be used for Plasma Cash too. Is this correct?

---

**sg** (2018-06-03):

In the #5 procedure, Alice is able to find her UTXO in receipt of Plasma chain.

Then before #6 - exit procedure - the malicious validator withholding Plasma block.

Now, Alice’s UTXO has been burn-ed in contract address, but she cannot execute exit anymore because #6 exit might be written as Plasma chain’s contract(CMIIW).

Then, now it’s time to Mass Exit from this Plasma chain because of the “Plasma enforcement” but her UTXO is already possessed by contract.

---

Maybe this can be a corner case which we need to solve.

---

P.S.

> Now, Alice’s UTXO has been burn-ed in contract address, but she cannot execute exit anymore because #6 exit might be written as Plasma chain’s contract(CMIIW).

I noted this is a Rootchain contract, and argument of this contract is UTXO_ID which is recorded on receipt of Plasma chain, and this UTXO is exactly the same thing with what owned by Plasma chain’s contract. If this understanding is correct, withholding is not a big deal.

---

**sg** (2018-06-03):

> Bob will receive 10 ETH once the exit processes.

At procedure #6, Rootchain’s fast-exit contract stored an exit and output ERC-721 debt, then, `finalizeExit()` processes matured exits. Now the ERC-721 backed exit has been finalized. Then what’s happen to the debt owner?

I guesstimate that ERC-721 debt gonna be expired state, and owner of that debt token directly gains withdrawn fund.

In this case, `finalizeExit()` function must contain a detector for “ERC-721 backed exit” in order to transfer tied fund to debt owner.

---

**kfichter** (2018-06-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/sg/48/14420_2.png) sg:

> In this case, finalizeExit() function must contain a detector for “ERC-721 backed exit” in order to transfer tied fund to debt owner.

We would add some functionality to finalizeExit() to pass information (UTXO ID) along with the send. Smart contract would get the $$ + UTXO ID and update balances internally. We wouldn’t want to handle this logic in the Plasma contract.

![](https://ethresear.ch/user_avatar/ethresear.ch/sg/48/14420_2.png) sg:

> Then, now it’s time to Mass Exit from this Plasma chain because of the “Plasma enforcement” but her UTXO is already possessed by contract.

I left this out of the original post, but withholding isn’t an issue with some scheme like confirmation sigs (or whatever alternative to them). Alice does provide the UTXO ID and tx data so that the exit is always tied to her.

---

**kfichter** (2018-06-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/y-matsuwitter/48/1188_2.png) y-matsuwitter:

> From my understanding, this withdrawal spec can be used for Plasma Cash too. Is this correct?

I haven’t checked for edge-cases, but I believe so.

---

**vbuterin** (2018-06-04):

I’ve had similar ideas; the conclusion I had is that the optimal buyer for coins in exit slots will generally be the plasma chain operator itself. So this becomes isomorphic to saying that the plasma chain can, in the normal case, have instant withdrawals, provided the contract is up to 2x over-collateralized (and much less over-collateral will be needed if the frequency of withdrawal requests is somewhat predictable).

---

**kfichter** (2018-06-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> the conclusion I had is that the optimal buyer for coins in exit slots will generally be the plasma chain operator itself.

Is this generally because the operator won’t include a double spend if they’re the one who’d lose out by including it?

---

**vbuterin** (2018-06-04):

Because the operator is both (i) the best party to internalize gains from increasing usability of the plasma chain, and (ii) the party that most easily and quickly knows that some exit-in-progress is valid and not challengeable.

---

**kfichter** (2018-06-04):

Got it, both make sense.

---

**bharathrao** (2018-06-04):

While this could work technically, I wouldn’t characterize this as simple economically.

This scheme could be simply seen as a hefty withdrawal fee if the plasma operator is the one most likely to accept the offer. The plasma operator can run out of funds and therefore an auction market as you suggested is necessary.

The exit fee needs to be balanced such that its attractive to the bond purchaser but affordable for the exiter. In my experience anything other than a flat, nominal fee would be a disincentive to use this plasma chain. Just imagine Binance charging 10% for withdrawals. Nobody would go there anymore. However, the operator would need to charge a percentage fee since locking large amounts of money for small fixed amounts does not make sense. In general, the charges have to reflect the borrowing cost for a 2-week period. Bitfinex borrowing rate for ether is around 0.0416%. Compounded over two weeks is about 1.77%

This may be *acceptable cost* for a lot of parties who trade occasionally for plasma speed and security. There would be many who would simply be priced out of the system who need to get in and out often (market makers, arbitrageurs, frequent traders). Think about it this way, if I move my money out 28 times, the 1.77% cost would cut my bankroll in half.

The real issue here is the two week delay on the main chain. This amplifies all costs and UX issues with plasma. If plasma could reduce this to say one day, the cost would be 0.04%, which may be acceptable to most people.

In Gluon Plasma we enable the UTXO owner to mark an output as retired, which prevents all operations on it except withdrawal to main chain. This enables withdrawal once the retirement is included in a plasma block. This enables withdrawals in a few minutes (except in Byzantine cases when the longer bonded exit can be used.)

---

**kfichter** (2018-06-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> In Gluon Plasma we enable the UTXO owner to mark an output as retired, which prevents all operations on it except withdrawal to main chain. This enables withdrawal once the retirement is included in a plasma block. This enables withdrawals in a few minutes (except in Byzantine cases when the longer bonded exit can be used.)

How do you handle the case where an operator creates an invalid (“out of nowhere”) utxo, marks it as retired, and withdraws it? You can prioritize slow bonded exits, but a user could then make many (continuous) slow bonded exits to grief the fast exits.

---

**bharathrao** (2018-06-04):

> operator creates an invalid

Good question.

I guess our scheme only works for an account model. An account begins with zero balance and every change to it (deposit, withdrawal, trade) are made from signature proofs and the prior state. There are fraud proofs for every transition any attempt to create an invalid transition can be proven.

Withdrawals cannot simply come from nowhere, since they need to point to a valid previous balance.

---

**kfichter** (2018-06-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Withdrawals cannot simply come from nowhere, since they need to point to a valid previous balance.

Do you have details on how this account model works?

---

**sg** (2018-06-05):

Basically, Nth Plasma has both economical bottle-neck and computational bottle-neck. And more strict condition might rate-limit the “depth N” of Plasma nest.

Then, regarding this fast withdrawal’s discount rate, N=27 is the economical bottle-neck of Plasma. Because the exitee(= the person who accepts the other’s exit) expects 10%~ profit per year and N=27 means he need to wait 1yr(54weeks) until he can unlock exiting fund. And this “27 times nested fast exit” costs exiter 10%+ discount. This is the economical bottle-neck of Plasma and this topic enlighten me. (There were no discussion regarding maximum depth of Plasma nest)

P.S. This fast withdrawal enables Plasma-fans to think about “Plasma MapReduce”. I’m quiet exciting about that.

---

**bharathrao** (2018-06-06):

Im finishing up the details including economic and game theory reasons for our model. Will post it here in a few days. Meanwhile, we have this bit online: https://docs.google.com/presentation/d/1OHarNOefkU39uch0s3IhyKAbtiyOisvqxOttP91k1Qo/edit#slide=id.g38e9606432_0_49

---

**kfichter** (2018-06-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> finishing up the details including economic and game theory reasons for our model.

Also, how are accounts credited when someone deposits into the chain?

---

**jdkanani** (2018-06-06):

Working on the same thing. The difference is - the stakeholders vote on checkpoints. Once votes exceed the threshold level, you propose checkpoint on the main chain. If checkpoints won’t happen in a certain amount of time, the chain goes into “withdraw the only mode” (same as chain halting) and people can withdraw their tokens using the last checkpoint without any urgency.

You can also restart the chain with different authorities. That would be better I guess.

[@kfichter](/u/kfichter)

> Also, how are accounts credited when someone deposits into the chain?

It’s special kind of transaction where operator inputs senders’ balance (latest UTXO) and deposit amount (with deposit id - tracked on mainchain), and generates total amount as output. That way anyone can challenge if operator uses same deposit id in multiple transactions. Apart from that, proof of existence in required from operator if sender challenges on main chain regarding deposit transaction.

---

**kladkogex** (2018-06-06):

I think this is a good proposal, but it may be imho rephrased even simpler.

1 Since it takes long time time to exit a Plasma, the value of ETH on Plasma is always less than the value of ETH on the main chain.

In other words, these are two different currencies. Lets call Plasma token PETH.

Then at particular moment of time you have something like

1 PETH = 0.98 ETH where the difference is risk of the Plasma operator becoming bad, plus decrease in value coming from a two-week lock.

So in my opinion what Kelvin is designing is an automic-swap-based market of PETH vs ETH.

These markets will exist for sure immediately once Plasma chains run, and once they exist then in my opinion, no one will use plasma default way of moving ETH into PETH for a very interesting reason - if you use the atomic swap market that Kelvin is proposing, you will get more PETH.   Very interesting!

---

**kfichter** (2018-06-06):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/j/4bbf92/48.png) jdkanani:

> It’s special kind of transaction where operator inputs senders’ balance (latest UTXO) and deposit amount (with deposit id - tracked on mainchain), and generates total amount as output.

Right, but an operator can update the balance with a fake deposit amount, send it to themselves a few times (masking the initial fake deposit), and then do a fast exit, all within a single withheld block. So you can prove that a single state transition is invalid if the block is available, but you can’t prove it if blocks are withheld. You also can’t efficiently prove that a chain of TXs is invalid.


*(7 more replies not shown)*
