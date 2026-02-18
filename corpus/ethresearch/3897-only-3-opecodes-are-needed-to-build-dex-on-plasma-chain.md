---
source: ethresearch
topic_id: 3897
title: Only 3 opecodes are needed to build DEX on Plasma Chain
author: leohio
date: "2018-10-23"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/only-3-opecodes-are-needed-to-build-dex-on-plasma-chain/3897
views: 3468
likes: 2
posts_count: 8
---

# Only 3 opecodes are needed to build DEX on Plasma Chain

Only 3 opecodes are needed to build DEX on Plasma Chain.

Leona Hioki ([leona.hioki@laurus-school.com](mailto:leona.hioki@laurus-school.com))

Soichi Kawai (skawai@math.kyoto-u.ac.jp)

Let us think about a fraud proof of general computings with a merkle tree ,and we think about an actual use case for instance.

Most of contract codes like EVM byte-codes are thought to be difficult to execute on Plasma chain. This hardness derives from the limitation that we cannot use Root Hash of state because only an operator has all value data which is the result of transactions.

This can be solve to a certain extent by recording all of execution process in a Merkle Tree. By this, we can prove which part of a process is precisely wrong at law cost, and minimize any fraud proof of general computings.

# ====Fraud Proof of General Computing====

Let us have a problem 1+1+1 and an evil executor returns "1+1+1=3+1=4".

We introduce opecode "ADD" which adds up left term.

And have a tree which leaves are,

(1,1,1,ADD),(2,1,ADD),(3,JUNK),(JUNK,JUNK)

This order means process of execution.

Even if the evil executor returns,

(1,1,1,ADD),(3,1,ADD),(4,JUNK),(JUNK,JUNK)

We can prove that the executor broadcasted tree includes

(1,1,1,ADD),(3,1,ADD) by hash values in the tree,

and also can prove that this part is wrong in the function of Plasma Contract.

This proof size scales at O(log(n)),so it can be used in any big contract execution.

NOTE: "JUNK" is just used to make a tree with 2^n leaves.

# ===Making DEX with this tree with some opecodes===

A merkle tree which includes opecodes can be set as a program, and can record the whole process of the execution of the program when input comes.

We will have the special merkle tree as an extension of that tree above.

The leftost branch just below the root hash is the hash of argument leaves (x1,x2,xn).

These arguments are not set when users of DEX send this to the operator with a transaction to make bid or ask.

The middle branch just below the root hash is a hash of memory leaves (m1,m2,…,mj),which record the value used in the process of the execution.

In other branches, opecodes, arguments leaves(like x1) and memory leaves (like m1) are set as leaves like (m2 x1 SUB).

The result of execution of branch will be inherited to the next right branch.

So, in a program branch "(9,3,SUB,m1),(m1,4,SUB,m2),(m2,1,SUB,m3)", m1 will be 9-3=6

and m2 will be 6-4=2, and m3 will be 1.

Like first case "1+1+1",this process and result can be proven with hash values in the tree by this structure either.

We need only 3 opecodes SUB, MUL,TX to make a DEX.

TX code branch is like (amount,from,to,currency,TX)

For example, we send 300 ETH to the operator with a tree of [300 ETH at rate 10 ETH/ETC] to get 3000 ETC. And one person can deal with amount smaller than 300 at rate higher that 10 ETH/ETC after he/she sends ETH. Operator sends the change to us.

The tree of this deal is described with leaves below,

(x1,x2,x3) //this means (amount,rate,address) arguments

(m1,m2,m3) // memory

(owner_address,operator_address)// our address

// program start

(300,x1,SUB,m1)

(10,x2,SUB,m2)

(x1,x2,MUL,m3)

(m3,operator_address,owner_address,"ETC",TX)//we get ETC

(m1,operator_address,owner_address,"ETH",TX)//this is change

(x1,operator_address,x3,"ETH",TX) // the other get ETH we set

Then, if any underflow in (m1,m2,m3), it’s a fraud transaction which can be easily proven with hash values in the tree.

Anyway, an operator executes and proves it with a tree, so he/she chose and match the transactions not to make wrong one.

if we or the operator want a condition like [transaction fee is 1ETH or 10 ETC for the DEX operator], we just add

(m1,1,SUB,m4),

(x1,10,SUB,m5)

We can extend DEX transactions in many ways by this tree.

# ===PROCESS===

(1) Alice set (price, amount, transaction fee) ,and make a exchange program with the merkle tree

(2) Alice sends a tx with UTXO (to Operator) and the exchange program tree.

(3) OP accepts it and broadcast this with OP’s sign.

(4) Bob react this, and sends a tx with UTXO (to OP)

(5) OP completes the exchange program tree and make UTXO to both of Alice and Bob as the result of the exchange.

# ===SECURITY REQUIREMENT===

Anyone can prove any fraud in this chain, but need to accuse one by one in the plasma contract on main chain. And every node needs to simulate the set transaction program written by tree structure before sending a real transaction.

## Replies

**bharathrao** (2018-10-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/leohio/48/10414_2.png) leohio:

> we send 300 ETH to the operator with a tree of [300 ETH at rate 10 ETH/ETC]

What if the operator pockets the 300 ETH and ignores your order?

![](https://ethresear.ch/user_avatar/ethresear.ch/leohio/48/10414_2.png) leohio:

> an operator executes and proves it with a tree

What if the operator gives himself (using a proxy) all the 300 ETH and gives you no ETC? Its on a different chain?

---

**leohio** (2018-10-25):

> we send 300 ETH to the operator with a tree of [300 ETH at rate 10 ETH/ETC]

This ETH is UTXO format pETH and bound to an exchange tree and signed in the tx.

So op has only two choices

(1) Accept a tx with both of UTXO and the tree

(2)Do not accept the tx

So, following situation does not happen.

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> What if the operator pockets the 300 ETH and ignores your order?

Next,

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> What if the operator gives himself (using a proxy) all the 300 ETH and gives you no ETC?

All UTXOs are bound to a tree. Returned UTXOs as results of an exchanges are also described in the tree which is completed by OP. So It’s hard to take only UTXO from tx and exit it.

Every UTXO without a merkle proof cannot be used to exchange or exit.

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Its on a different chain?

It’s not cross chain.

I was wrong that I took ETC (pETC) for example because this does not exist on the ETH main chain, so one cannot exit this pETC. It was totally nonsense. pls replace word “ETC” to any ERC20 token.

---

**bharathrao** (2018-10-25):

Im wondering if this can be incorporated into [gluon plasma](https://ethresear.ch/t/gluon-plasma-full-spec-for-non-custodial-exchanges/3931) to eliminate data unavailability.

For this to work, we would also need the following:

1. A user signature on [300 ETH at rate 10 ETH/ERC20]. Otherwise operator can take everyone’s pETH by fake orders.
2. A price-time priority fraud proof to prevent front-running.
3. Im unsure how the 300 ETH exists. Is it a single account or is it a bunch of UTXOs that add up to 300? If its the latter, then you have to deal with dust piles where 300M outputs of 0.000001 pETH orders are created.

There are many practical issues that we had to face to create our version of plasma for exchanges that you would need to address.

---

**bharathrao** (2018-10-26):

Who can prove fraud? only the victim or any observer?

If its only the victim, then the operator can create two fake users owner_1 and owner_2 and make tham have a fake transaction where one of them gets lots of fake pETH?

---

**leohio** (2018-10-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Im unsure how the 300 ETH exists. Is it a single account or is it a bunch of UTXOs that add up to 300? If its the latter, then you have to deal with dust piles where 300M outputs of 0.000001 pETH orders are created.

This problem make me think that we should introduce not UTXO but slot like Plasma Cash.

I just proposed this with UTXO simply because many of us know UTXO.

The problem is amount of data and traffic where all UTXO/slots have each trees as the exchange history. Is this what you referred as “data unavailability”?

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Who can prove fraud? only the victim or any observer?

It seems that this needs observers, because all of exchange txs are signed and broadcasted with a tree by OP, and only this can prove the right to exit.

Only 2 facts prevent malicious behaviors

(1)only UTXOs which occurred from a tree signed by 3 (from, to,OP) can be used to new exchange tx, or exit on contract.

(2)every node can prove the right to exit if he/she has the proved tree, and every node can prove the fraud of the others when they don’t have proof or they faked a tx-tree.

---

**KanaGold** (2018-11-05):

If we only think about a situation for creating a DEX on Plasma cash, I think I would simply create a new UTXO that spend UTXOs for my NFTs that can be spent by either:

1 withdwaral requirement by the owner of the NFTs  to normal form of UTXOs

2 matching order by another person that is willing to get the NFTs in exchange for some other NFTs that are defined by the UTXO

1 occurs when the original person wants to cancel the order, and 2 occurs when someone decides to settle the order.

with this approach, by placing the UTXO onto the correspontding merkle leafs(ie. the same txid is located on multiple leafs), i think we would be able to maintain the situation of original plasma cash.

---

**leohio** (2018-11-07):

Yes, I proposing that method with UTXO and tx with a merkle tree, but it’s only because it’s simple. NFT is more easy to code when we tag some data like merkle trees to assets.

![](https://ethresear.ch/user_avatar/ethresear.ch/kanagold/48/3410_2.png) KanaGold:

> 1 occurs when the original person wants to cancel the order, and 2 occurs when someone decides to settle the order.

Exactly, we cannnot cancel an order by the method I proposed.

But we can fix that by adding new OPECODE of CANCEL which disable the program tree.

I mean a merkle tree and its “proof of process” is extensible by thinking about a new OPECODE i think.

