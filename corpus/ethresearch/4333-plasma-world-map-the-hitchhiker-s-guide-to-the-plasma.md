---
source: ethresearch
topic_id: 4333
title: Plasma World Map - the hitchhiker’s guide to the plasma
author: Dapploper
date: "2018-11-22"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-world-map-the-hitchhiker-s-guide-to-the-plasma/4333
views: 19616
likes: 50
posts_count: 22
---

# Plasma World Map - the hitchhiker’s guide to the plasma

[![image](https://ethresear.ch/uploads/default/optimized/2X/f/fe51381218e40a2d6b38ee4de91e94ef280976ec_2_690x397.png)image1386×799 138 KB](https://ethresear.ch/uploads/default/fe51381218e40a2d6b38ee4de91e94ef280976ec)

*You can read this post on [here](https://medium.com/onther-tech/plasma-world-map-ba8810276bf2) too.*

## Intro

**The Plasma World Map**  is designed to guide anyone traveling on a long journey to plasma safely to their desired destination without getting lost on the way.

It allows new plasma travelers to draw large pictures of numerous studies and provides existing plasma researchers with a good cheat sheet for doing one’s research efficiently.

***Note : The Plasma World Map is not perfect.***  *Please let me know if you find something wrong in this article and the map itself.*

### Classification

Two major categories of the World Map are  **Simple Transfer**  and  **General States & Computation** . Each plasma model was classified to each category, considering the purpose it is trying to achieve. You are always welcome if you have an idea of better classification.

## Index

### 1.Simple Transfer

This category includes plasma models which implement simple transfer feature like Bitcoin.

#### UTXO based

- Plasma MVP
- With ZKP
- Plasma Cash

#### Account based

- General
- With ZKP

### 2.General States & Computation

This category includes plasma models which implement general states & computation features like smart contract in Ethereum.

#### UTXO based

#### Account based

# 1. Simple Transfer

### 1) UTXO based : Plasma MVP

This category is for a plasma model which implements the Simple Transfer feature based on UTXO data structures. It is based on the Minimal Viable Plasma(Plasma MVP).

####

Authors : Vitalik Buterin

Plasma MVP is the first plasma model presented after the plasma white paper was released. It used binary Merkle tree based on UTXO for its data structures. In addition, a challenge system was set up to prevent an invalid exit, and Confirmation and Exit Priority were set up to resolve the data unavailability issue.

Although there was the issue of poor UX caused by the Confirmation phase which requires 2 steps of signature in sending transaction, it was a good starting point for presenting various future researches.

####

Authors : Dan Robinson

In this model, the client-side validation method was applied to Plasma MVP, and the structure of UTXO was transformed to include only signatures and destination. Clients in Plasma chain can verify the UTXO which they received. It also suggested a way of tumbling transaction through pruning.

####

Authors : Kelvin Fichter

This article designed a method of implementing Fast Withdrawal which is presented in the white paper. The key idea in here is we can build it only by smart contract on the root chain.

####

Authors : Ben Jones, Kelvin Fichter

This research proved that we can build the existing valid exit game schema excluding the Confirmation step by changing the exit priority rule from the age of output of UTXO to age of the youngest input.

####

Authors : Kelvin Fichter

This research suggested enabling the Simple Fast Withdrawal even on faulty plasma chains by making the operator deposit on the user’s Fast Withdrawal in return for some fees.

####

Authors : Vitalik Buterin

This article discussed about enabling single exit for multiple UTXOs or coins by submitting not a Merkle proof for each UTXO or coin but the block number and indices of each UTXO or coin.

####

Authors : Kelvin Fichter

It showed how mass exit can be executed through the Sum Merkle Tree, which represents the sum of UTXO aggregation and the aggregated value of each UTXO.

####

Authors : Eva Beylin

This is a discussion of ways to liquidate for collateral like deposits for Exit in several Layer2 solutions such as Plasma.

####

Authors : Bing Yang

This article presents a way to reduce transaction-to-transaction latency. It is making transactions contained in blocks but not committed to the root chain available as input to other transactions.

### 2) UTXO based : With ZKP

This category is for a Plasma model that adds verification methods with ZK Proof to the simple transfer feature based on the UTXO data structure.

####

Authors : josojo

This article is about how to configure a kind of light-client on a Plasma chain by introducing a verification method using zk-snark in the model of Plasma MVP, More Viable Plasma.

### 3) UTXO based : Plasma Cash

This category is for a Plasma model which implements the Simple Transfer feature based on UTXO data structures. It is based on the research of Plasma Cash.

*(Plasma Cash is based on the Plasma MVP, but is classified separately because many researches were conducted based on Plasma Cash.)*

####

Authors : Vitalik Buterin

Plasma Cash is a newly proposed model to improve the problems of Plasma MVP. Each coin was given a unique ID and denomination in this model. It used the Sparse Merkle Tree(SMT) to place the index of each leaf node as a coin ID. And the value contains relevant transaction information when the coin is used. If the coin is not used in that block, the value is null because there is no transaction information for that coin as well. This means that the proof of inclusion and non-inclusion in SMT allows clear verification of the use history of coins.

However, it was pointed out that it is hard to pay partially due to non-fungibility, and the verification of history for each coin could be a very heavy work.

####

Authors : Karl Floersch

To improve the shortcomings of the single operator model in [Plasma Cash Simple Spec](https://karl.tech/plasma-cash-simple-spec/), it suggested PoS consensus to resolve the Transaction Censorship and the issue that all users should exit when the data is withheld.

####

Authors : Kelvin Fichter

As the title suggests, the burden of verification of the coin history in Plasma Cash was alleviated through secure checkpointing with [Cryptoeconomic signature aggregation](https://ethresear.ch/t/cryptoeconomic-signature-aggregation/1659) in Plasma XT.

####

Authors : Sourabh Niyogi

In this model, Bloom filters were introduced for efficient non-spent verification, and probabilistic transfers were introduced for partial payment.

####

Authors : Georgios Konstantopoulos

Plasma Cash Implementation specialized for use of ERC721.

####

Authors : Dan Robinson

Plasma Debit is a model that improves the problem of non-fungibility, which was pointed out as a disadvantage of Plasma Cash. To do so, it made each coin to be used as a form of payment channel between users and operators or other users.

####

Authors : Vitalik Buterin

Atomic Swap protocol for Plasma Cash. In this protocol, most of the actions required for the Atomic swap are executed on the plasma chain. Only the sharing keys is executed on the main chain so that the Atomic swap could be carried out efficiently.

####

Authors : Vitalik Buterin

Plasma Cash Defragmentation is about the Defragmentation method to improve the indivisibility of the coin in Plasma Cash. The key idea is to allow the users to put those coins scattered on single Merkle branch through kind of Atomic swap when they send coins.

####

Authors : Vitalik Buterin

This research suggested how the operator can execute defragmentation by sending a permutation transaction. This special transaction consists of swaps of each coin to defragment them.

####

Authors : Vitalik Buterin

It showed how defragmentation can be performed by minimizing the generation of fragment when users send transaction each other.

####

Authors : Hayden Adams

Plasma Cashflow is a Plasma Cash Implementation that is based on the ideas of Plasma Debit and Plasma Defragmentation.

####

Authors : Vitalik Buterin

This research showed how to reduce the verification burden for the history of each coin in Plasma Cash using RSA Accumulators. This idea was the basis for the Plasma Prime.

####

Authors : Vitalik Buterin

This research proved that we can execute the inclusion and non-inclusion proof of the coin in Plasma Cash with O(log n) using RSA accumulators.

####

Authors : Sourabh Niyogi

This is a summary of what Vitalik Butterin explained about the specific spec of Plasma Prime in the Plasma Implementers Call.

####

Authors : Bankex team

This is the Plasma Prime Implementation designed by the Bankex team. It is based on Plasma Cashflow.

### 4) Account based : General

This category is for a plasma model which implements the simple transfer feature based on Account-balance data structures.

####

Authors : Paul Berg, Mark Milton

Plasma implementation that used kind of payment channel.

####

Authors : Bharath Rao

It explained why it is difficult to build the decentralized exchange(DEX) in Plasma MVP and Plasma Cash. It suggested a different way to build the DEX in Plasma. More details can be found at Gluon Plasma.

####

Authors : Bharath Rao

Gluon Plasma suggested a plasma model that focuses on improving UX and Scaling. However, due to the lack of solutions to the Data unavailability issue, it is hard to say that it was well constructed.

####

Authors : Jieyi Long

It suggested a way to force only the valid state transition through probabilistic verification of account balance in the plasma chain.

### 5) Account based : With ZKP

This category is for a plasma model that adds verification methods with ZK Proof to the simple transfer feature based on the Account-balance data structures.

####

Authors : Alex Vlasov

Quark-gluon Plasma is a plasma chain based on account-balance data structures which can be verified its valid state transition with zkSNARKs. However, the solution to the data unavailability was insufficient.

####

Authors : Barry White Hat, Alex Gluchowski, HarryR 33, Yondon Fu, Philippe Castonguay

It is research about the side chain with zkSNARKs. It suggested operator replacement auction mechanism when the operator stops the operation for a specific period. And roll-back mechanism was suggested to enable new operator to keep making the blocks.

####

Authors : josojo

Plasma Snapp is a plasma chain that can verify the state transition including deposit and withdrawal with zkSNARKs. Like the [Roll_up / roll_back snark side chain](https://ethresear.ch/t/roll-up-roll-back-snark-side-chain-17000-tps/3675), it also allowed anyone to become an operator when the operator was absent for a long period of time. And the roll back mechanism was used to return the chain to its previous state for the new operator. And users can keep safe one’s fund through higher priority in exits. Although the data is withheld by the operator, priority of user’s exit is always higher than operator’s if the users did not send transaction after the withholding.

# 2. General States & Computation

### 1) UTXO based

This category is for a plasma model which implements general states & computation features using the advantages of limited features that UTXO has.

####

Authors : Johann Barbie

This is discussion about why it is difficult to implement Smart Contract in Plasma. It was briefly stated that it is not possible to force a valid state transition with existing Exit game in the data unavailability. It was also the theoretical basis for Plasma leap.

####

Authors : Johann Barbie

Plasma Leap implemented general computation feature with a small program called Spending Condition which is similar to Pay-to-Script-Hash (P2SH) in Bitcoin. And it also implemented general states feature with nun-fungible storage token(NST) which is kind of ERC721 token with storage root hash. It resolved the data availability issue using exit model of More Viable Plasma.

### 2) Account based

This category is for a plasma model which implements general states & computation features similar or equal to Ethereum.

####

Authors : Esteban Ordano

Plasmabits is a plasma implementation proposal that can use EVM-based smart contract. It suggested PASITO contract (Plasma Arbitration Stepping Instruction Test Operator) borrowing the Truebit-like verification game as a way to verify valid state transition. And it also suggested query and respond system for availability of blocks data. But anyone can attack the operator by making query to the operator for all blocks. That means, every plasma block should be included on the root chain and that is not so good.

####

Authors : Carl Park , Aiden Park, Kevin Jeong

Plasma EVM is a new version of Plasma that can execute EVM in plasma chain. It used Truebit-like verification game as a way to verify valid state transition in plasma chain. It also suggested concept of Requestable Contract to resolve exit authority problem in Contract Account. And User Activated Fork model was introduced to deal with the data unavailability.

### Comment

*Plasma World has been growing rapidly since its birth in August 2017. As many researchers keep working to expand Plasma’s territory, Plasma World Map will also be updated periodically to quickly reflect the newly pioneered areas.*

## Replies

**bharathrao** (2018-11-22):

This is great. I had no idea there were more flavors of plasma than Ben and Jerry’s ice cream.

Maybe we highlight flavors that are in testnet and mainnet?

---

**bharathrao** (2018-11-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/dapploper/48/2003_2.png) Dapploper:

> due to the lack of solutions to the Data unavailability issue

Data unavailability is addressed the same way as MVP/plasma classic. There is a mass exit. This is made practical by halting the chain first to avoid gas pressure/network congestion.

---

**Dev43** (2018-11-22):

Thank you very much for this. Great breakdown of the different plasma proposals it’d be great to add in which ones are actuvely being worked on too as I would imagine some of them reached POC and moved on.

---

**Dapploper** (2018-11-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Maybe we highlight flavors that are in testnet and mainnet?

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/d/b19c9b/48.png) Dev43:

> it’d be great to add in which ones are actuvely being worked on too as I would imagine some of them reached POC and moved on.

Originally, I designed this as a map of numerous theoretical researches so that anyone can draw a big picture of them. This is the reason why I focused on connecting related researches and wrote short summary about theoretical implication of each. For this reason, I think it is unnecessary to discuss about status of development in here. It would be more proper to make another post about the status of development for each plasma model.

---

**Dapploper** (2018-11-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Data unavailability is addressed the same way as MVP/plasma classic. There is a mass exit. This is made practical by halting the chain first to avoid gas pressure/network congestion.

By [the full paper](https://leverj.io/GluonPlasma.pdf), if the data is withheld by the operator and is unavailable, then users vote to halt the chain or not, based on the governance token. But the voting mechanism assumes security based on honest majority and the token distribution. Let’s say a minimum percentage of number of votes needed to halt the chain is N%. If an attacker has N% of governance token or more, then one can always rob those users very easily using data unavailability.

The key point in Plasma is that only valid state transition is enforced in plasma chain by the root chain. If you can’t, at least you should ensure that users can safely exit from that chain. But in your model, if an attacker has those tokens equal or more than N%, invalid state transition can be done and users cannot safely exit anymore.

So the voting mechanism in your model is not a solid solution for data unavailability.

---

**bharathrao** (2018-11-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/dapploper/48/2003_2.png) Dapploper:

> N%. If an attacker has N% of governance token or more

This would be true if N > 50. The recommended value for N is 10. This would require the attacker to control more than 90% of the entire supply to perform the attack you suggest. It would require a huge amount of money to obtain these many tokens from the market (assuming that 90% would even sell). The price would pump so high that it may not even be possible to buy them all. The tokens would be immediately worthless after a successful attack.

This balances the cost of the attack to the theft incentive and makes such an attack impractical. Compare with getting a supermajority hashrate on a POW coin.

---

**Dapploper** (2018-11-24):

Let me explain more precisely. Let’s say total number of tokens is **N**, and for halting the chain, **M** tokens should be voted for **yes**. Then for preventing honest users from halting the chain in the data unavailability, an attacker must have at least **N-M+1** tokens **(DA attack)**. And if an attacker has number of tokens equal or more than **M**, one can always halt the chain forever **(DoS attack)**.

What is interesting in here is, **If you set the M low** to prevent the data unavailability, the probability of DA attack would be low, but on the contrary, it becomes vulnerable to DoS attack.

Let’s take a look at the table below.

| Total(N) | M(cost of DoS) | N-M+1(cost of DA) |
| --- | --- | --- |
| 100 | 10 | 91 |
| 100 | 30 | 71 |
| 100 | 50 | 51 |
| 100 | 70 | 31 |
| 100 | 90 | 11 |

As you can see, when you set **M** lower to protect the chain from DA attack, the chain becomes **more vulnerable to DoS attack**. And the opposite is same as well.

You said that the recommended value of **M is 10**. Then the chain will be very vulnerable to DoS attack, because an attacker needs only 10% of total tokens. There’s a dilemma here. How can you set the M? And **how can you assure that it is not vulnerable to both attacks?**

The problem is that this is not the end. There is one more thing you should consider for setting M. The thing is when the benefits of the attack outweigh the costs, there is always an incentive to attack. Let’s say M is 10 and the cost for buying N-M+1 tokens is 100000ETH. Then if the total deposit amount of the chain is bigger than this cost, the attacker would be glad to attack.

Therefore, the amount of total deposit must always be less than the cost of acquiring this N-M+1 tokens to be safe from DA attack. And that is not so good.

If the price of the token crashed like the cryptocurrency market right now, well… you can easily expect what will happen.

---

**bharathrao** (2018-11-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/dapploper/48/2003_2.png) Dapploper:

> Let’s say M is 10 and the cost for buying N-M+1 tokens is 100000ETH.

The cost of buying even 10% of the supply will be extremely prohibitive. As supply dries up, price would skyrocket. Even if someone did manage to capture 10% and halt the chain, they would have to sacrifice a portion of their tokens as part of voting to halt. The disruption would be a few hours to a couple of days but they cannot steal any funds.

The cost of being a nuisance for a few hours is still very high and not attractive.

Regardless, POS with tendermint consensus is an attractive alternative that eliminates issues with token voting. Your analysis on that piece would also be most appreciated.

---

**Dapploper** (2018-11-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> they would have to sacrifice a portion of their tokens as part of voting to halt.

Does that mean someone who voted for halting the chain will lose one’s tokens after voting?

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Regardless, POS with tendermint consensus is an attractive alternative that eliminates issues with token voting. Your analysis on that piece would also be most appreciated.

There seems to be a misunderstanding among some plasma researchers(like what I did at first). A plasma model should not be dependent on the consensus algorithm(ex. Tendermint, Casper or whatever else). Because that is what the plasma is. Plasma is dependent on the root chain(Ethereum), not the consensus of child chain. Plasma model must ensure that only valid state transition is enforced by the root chain, even if the child chain is byzantine.

In plasma white paper, the authors did recommend to use PoS based consensus in child chain. But it is just recommendation. A solid plasma model should work in even PoA which only has a single node. With repeated emphasis, it doesn’t matter which consensus algorithm is used in the plasma model.

You can definitely build your chain with PoS like Tendermint. But if you did not solve these problems like DA attack, you cannot say that you did design plasma model. It would be more proper to call it a sidechain.

---

**bharathrao** (2018-11-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/dapploper/48/2003_2.png) Dapploper:

> Does that mean someone who voted for halting the chain will lose one’s tokens after voting?

Yes. This disincentives careless or malicious voting to halt

---

**4000D** (2018-11-25):

You cannot judge whether a vote is malicious or not in a decentralized way unless you use the slashing conditions like casper. But it means that the security is dependent on the consensus in plasma, not root chain.

BTW, also you cannot use high quorum ratio like 90% because attacker can prevent the halt by occupying 10% of tokens. and the lowest quorum ratio you can use would be 50%.

---

**bharathrao** (2018-11-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/4000d/48/1214_2.png) 4000D:

> unless you use the slashing conditions like casper

The root contract slashes some percent of voters tokens. Root contract does not care if the vote is malicious or not, you get slashed if you vote. The idea is that you are willing to sacrifice a portion of tokens whose worth is going to drop in case of a real attack.

![](https://ethresear.ch/user_avatar/ethresear.ch/4000d/48/1214_2.png) 4000D:

> attacker can prevent the halt

Also correct. 10% is recommended but it is counterproductive to go above 50%. The actual parameters depend on the supply, price and distribution characteristics.

---

**bharathrao** (2018-11-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/dapploper/48/2003_2.png) Dapploper:

> Plasma is dependent on the root chain(Ethereum),

Even with a POS consensus on the child chain, slashing bad validators or halting bad exchanges would be enforced by the root chain.

![](https://ethresear.ch/user_avatar/ethresear.ch/dapploper/48/2003_2.png) Dapploper:

> With repeated emphasis, it doesn’t matter which consensus algorithm is used in the plasma model.

Can you describe why this should be so? My understanding is that the only requirement is that users are able to withdraw funds if the consensus system’s operators/validators fail. The plasma chain itself could have any rules it wants, including POW, POS, POA or any combination thereof.

---

**Dapploper** (2018-11-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Can you describe why this should be so? My understanding is that the only requirement is that users are able to withdraw funds if the consensus system’s operators/validators fail. The plasma chain itself could have any rules it wants, including POW, POS, POA or any combination thereof.

That is exactly what I mean. This is the reason why the POS with tendermint consensus is not an attractive alternative. You need another way to ensure user’s exit when the consensus system fails like more than 2/3 nodes are byzantine. And the voting mechanism that you mentioned is not a solid solution for this as I said before.

---

**bharathrao** (2018-11-26):

You are suggesting that POS is ok for root chains such as Ethereum or Cosmos but not ok for plasma chains. Do you have any technical reasons or quantitative measures as to why this is so?

I also don’t understand why you think token voting POS is an unsuitable fallback. For the purposes of the Gluon Plasma chain – trading exchanges, it is very effective due to the Pareto distribution of assets.

Your point regarding resistance to both DoS and DA attack have been addressed: The economic cost of mounting such an attack is likely to be higher than any benefits. Just like POW, all consensus mechanisms dissuade the rational attacker.

---

**Dapploper** (2018-11-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> You are suggesting that POS is ok for root chains such as Ethereum or Cosmos but not ok for plasma chains. Do you have any technical reasons or quantitative measures as to why this is so?

No, What I said is that you can use POS or whatever consensus in your plasma chains, but you should have additional mechanism for safety like exit-game in Plasma-MVP. That is the reason why I told you using Tendermint is not an attractive alternative.

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Your point regarding resistance to both DoS and DA attack have been addressed: The economic cost of mounting such an attack is likely to be higher than any benefits.

I can’t understand how you can assure for this. If the total deposit amount of plasma chain that an attacker can take is bigger than the cost, the attacker will always gladly do DA attack. This model will definitely be vulnerable when the total deposit grows or the price of governance token crashed. Do you have any mathematical model or analysis for these cases?

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Even if someone did manage to capture 10% and halt the chain, they would have to sacrifice a portion of their tokens as part of voting to halt.

I think this is not so good idea. You can prevent DOS attack definitely, but the operator can withhold data and attack users so that one can make them burn their tokens.

And there is also an issue of the tragedy of the commons. Users have no reason to be active in voting because all the tokens voted to halting the chain in data unavailability. They will always want other users to vote. This is because, if the quorum is filled, they can escape without spending any money. That is why I call it the tragedy of the commons.

Also, users with few assets in the plasma chain are likely not to vote, even if they have the tokens. That is because the cost of voting is likely to be higher than the assets that they can be exit with. I think a more accurate analysis of these various cases is necessary if you want to prove that your solution is solid.

---

**bharathrao** (2018-11-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/dapploper/48/2003_2.png) Dapploper:

> but you should have additional mechanism for safety like exit-game in Plasma-MVP.

Since you havent described *why* there needs to be an additional mechanism, let me try to guess: The safety exit mechanism exists to ensure that the security level of the plasma chain is equal to the security level of the rootchain.

The ethereum level security equivalence of mass exits is an illusion. The MVP/Cash (and others) exit constructions are of lower security since they can be spammed with millions of dust deposits and/or fake exits that need to be challenged. Sufficient amount of spam will render many users unable to exit. Every mass exit mechanism right now is of lower security than ethereum. The only exceptions are ZKP and other chains that do not have DA issues. I haven’t yet created a quantification model for the mass exit, but my current guess is Gluon is as secure or more than MVP/Cash.

![](https://ethresear.ch/user_avatar/ethresear.ch/dapploper/48/2003_2.png) Dapploper:

> I can’t understand how you can assure for this

The cost of the governance tokens will rise as the value locked in the plasma contract increases. This is due to several reasons:

1. The people who move tokens to plasma will buy governance tokens to subsidize their trading since higher asset values are followed by higher activity, resulting in higher staking rewards.
2. An attacker buying 10% or 90% is similar to a hostile takeover. When a large hard percentage limit of the assets needs to be acquired, the price paid will be the marginal price that any user is willing to pay. An increase in price will bring in even more buyers competing with the attacker. This is a well-known effect in markets.
3. Due to the fact that it takes time for books to fill, you have a window of a few days before the crowd rushes in. You can try this yourself by trying to acquire a large percentage of any asset. Try buying 10% of the entire supply of even the cheapest shitcoin and you’ll see how expensive it gets even in a terrible bear market. At 90% it becomes improbable. The only requirement is that the coins are not held by a small ( but the operator can withhold data and attack users so that one can make them burn their tokens.

Once the operator withholds the data, the chain will halt and the operator is effectively terminated. This is a serious disincentive for forced loss of users tokens at no gain to operator.

![](https://ethresear.ch/user_avatar/ethresear.ch/dapploper/48/2003_2.png) Dapploper:

> And there is also an issue of the tragedy of the commons. Users have no reason to be active in voting

Users want to protect their assets on the plasma chain. This is a good reason to vote. Filling the quorum or not is irrelevant. There is no economic incentive to withhold voting since if the operator is compromised, governance tokens are likely to be worthless.

![](https://ethresear.ch/user_avatar/ethresear.ch/dapploper/48/2003_2.png) Dapploper:

> the cost of voting is likely to be higher than the assets that they can be exit with

This is only true when the voter is malicious (or plain careless). In the event of a real compromise, all parties detect it simultaneously and everyone knows that tokens will be worthless in a few minutes.

The nature of the tokens to **retain value when the operator is honest but lose value when compromised** is a key aspect that you may have overlooked.

![](https://ethresear.ch/user_avatar/ethresear.ch/dapploper/48/2003_2.png) Dapploper:

> using Tendermint is not an attractive alternative.

Tendermint consensus removes the need to halt the chain and associated bad effects. It allows multiple validators instead of a single operator. If a validator is compromised, only that operator’s deposit needs to be slashed. The rest of the system continues to run unaffected

---

**ldct** (2018-11-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> The MVP/Cash (and others) exit constructions are of lower security since they can be spammed with millions of dust deposits and/or fake exits that need to be challenged.

This is not true in general. Assuming a plasma cash chain which only supports single-input transactions as well as single-beneficiary exits, it is possible to require exits to put up a bond. We can analyze the possible attacks against someone in this design and the only one that shows its security level to be below that of the root chain is a direct attack on root chain liveness.

> my current guess is Gluon is as secure or more than MVP/Cash.

I think you already understand this from your analysis, but it is worth pointing out that comparison of security of these systems is multidimensional, e.g. one way of breaking it down is to consider

1. assuming the child chain mechanism does not get compromised, how can users be attacked?
2. assuming the child chain mechanism is compromised, how can users be attacked?
3. how likely is it that the child chain mechanism is compromised?

It seems like the answer to (2) is that in the case that the child chain mechanism is compromised, i.e. the PoS block producers withhold data and the 10% token vote threshold is not reached, you do not attempt to provide any guarantees for users?

---

**bharathrao** (2018-11-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> Assuming a plasma cash chain which only supports single-input transactions as well as single-beneficiary exits, it is possible to require exits to put up a bond.

This is trivial to spam attack with a modest budget:

1. Create a few coins.
2. Send them around to other addresses that you own creating a long history
3. Exit intermediate states simultaneously and fill the gas limit. ie, say 80 exits / eth block assuming 100K gas per exit.
4. Keep exiting for the next 10,000 blocks. Some challenges will block exits but many wont.

The original Plasma Cash spec does not specify who deposits bonds, Im guessing its both the exiter and the challenger, in which case challengers can run out of money fast tied up in challenges, while the exiter can re-funnel the money he stole back into the attack.

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> these systems is multidimensional

Ultimately, the cost of the attack should be much higher than the profits. Gluon Plasma is far from perfect, but tries to accomplish this by creating a voting token that needs to be acquired at high cost but loses value on successful attack.

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> assuming the child chain mechanism does not get compromised, how can users be attacked?
> assuming the child chain mechanism is compromised, how can users be attacked?
> how likely is it that the child chain mechanism is compromised?

1. Ideally, #1 shouldn’t even be possible. Yet, most plasma constructions can be easily spam attacked, overloaded with large proof histories that need to be verified, challenge wallets can be depleted. This is why we dont rely on challenges or allow creation of entry blocks from plasma contract and use compact proofs of validity instead of long tx histories.
2. If the child chain is compromised, the chain should halt immediately in a POA model This is the safest way to protect user funds. In a POS model, the bad validator can be eliminated. Many plasma constructions are POA and rely on the individual users to be responsible to exit by themselves. This is a very high bar for people who can barely manage their own private keys. Many people WILL lose a lot of money if such a chain ever attracts people with expertise level below that of members of this forum.
3. A POA model is like a centralized exchange. It’s a matter of when, not if it will get compromised. Obviously POS makes it a lot more decentralized and safer because the bad actors will now have to compromise (say) more than 2/3 of the validators.

---

**ldct** (2018-12-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> This is trivial to spam attack with a modest budget:
>
>
> Create a few coins.
> Send them around to other addresses that you own creating a long history
> Exit intermediate states simultaneously and fill the gas limit. ie, say 80 exits / eth block assuming 100K gas per exit.
> Keep exiting for the next 10,000 blocks. Some challenges will block exits but many wont.

Why would the plasma contract allow the same coin / range of coins to be successfully withdraw multiple times? The whole point of the plasma cash design is to segregate deposits in such a way that this cannot happen.

> in which case challengers can run out of money fast tied up in challenges

If the plasma chain is functioning correctly (only valid and available blocks are committed), there is no need to make challenges that do not immediately succeed (proof: the only invalid exits possible are exits of spent coins, and those can be challenged and cancelled by showing the spend of the coin). Hence

1. assuming the child chain mechanism does not get compromised, there are no serious attacks possible against users (the “tie money up in challenges” attack is not possible) in plasma cash; this is no worse than in gluon
2. assuming the child chain mechanism does get compromised, a “tie up money in challenges” attack is possible, but this is no worse than in gluon, wherein users will lose money

> If the child chain is compromised, the chain should halt immediately in a POA model

When I say the “child chain mechanism” I mean all things not enforced by the plasma contract, including the blocks committed and the outcome of the token vote. Hence the hypothesis of this case analysis is that the PoS block producers maliciously commit invalid/unavailable blocks *and also that the token vote to stop them does not happen or does not pass the 10% threshold*.


*(1 more replies not shown)*
