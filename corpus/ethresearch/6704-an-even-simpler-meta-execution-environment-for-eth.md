---
source: ethresearch
topic_id: 6704
title: An even simpler meta-execution environment for ETH
author: vbuterin
date: "2019-12-30"
category: Sharding
tags: []
url: https://ethresear.ch/t/an-even-simpler-meta-execution-environment-for-eth/6704
views: 5529
likes: 9
posts_count: 8
---

# An even simpler meta-execution environment for ETH

See [Moving ETH between shards: the problem statement](https://ethresear.ch/t/moving-eth-between-shards-the-problem-statement/6597) for the problem statement and [A meta-execution environment for cross-shard ETH transfers](https://ethresear.ch/t/a-meta-execution-environment-for-cross-shard-eth-transfers/6656) for an earlier attempt.

### Solution

Every shard stores a map balances: (shard, EE) \rightarrow balance. The total “real balance” of some EE in some shard can be computed as:

real\_balance(shard, ee) = \sum_{i=0}^{shard\_count} shard[i].balances[s][x]

To perform any transfers of ETH between EEs in a block, the shard must contain a Merkle proof from the most recent state of every shard, showing `shard[i].balances[s][x]` for every shard `i` to prove the total balance of the EE. If a transfer between EEs is made on some shard `s`, transfering `xfer_amount` ETH from EE `ee_1` to `ee_2`, then we check that the `real_balance(s, ee_1) >= xfer_amount`, and then set `shard[s].balances[s][ee_1] -= xfer_amount` and `shard[s].balances[s][ee_2] += xfer_amount`.

To perform a cross-shard transfer from shard `s1` to shard `s2`, we set `shard[s1].balances[s1][ee] -= xfer_amount` and `shard[s1].balances[s2][ee] += xfer_amount`.

Note that invididual `shard[s].balances[s][ee]` values may sometimes be negative. For example, if the initial balances for some EE are `{A: [1, 0, 0], B: [0, 0, 0], C: [0, 0, 0]}` and then 1 ETH is transferred from shard A to shard B, and then soon transferred from shard B to shard C, the final balances would be `{A: [0, 1, 0], B: [0, -1, 1], C: [0, 0, 0]}`. However, the “real balance” \sum_{i=0}^{shard\_count} shard[i].balances[s][x] should always remain non-negative.

### Overhead

Under conditions of high usage, about the same overhead will be required as previous schemes (ie. ~20 kB per EE), though slightly lower because Merkle branches into bitfields will not be required. Also, if a block contains exclusively proofs within an EE, or if for every EE, ETH coming in equals ETH going out, proofs are not required. However, if there are unbalanced cross-EE transfers, then full proofs are required for any EE that has net-outgoing funds.

### Further improvements

EEs could have a “reserve” of funds saved on every shard (eg. 1 ETH per shard). If a particular EE has more outgoing than incoming transfers in a block, then that reserve would be reduced; full balance proofs would only be required when the reserve reaches zero. If an EE has more incoming than outgoing transfers, then the reserve would be increased.

A “zero capital overhead” alternative would be a system where `shard[i].balances[j][ee]` stores both the balance value and also the amount received minus amount spent in the most recent slot. A block in shard `j` spending amount X could avoid providing a full proof of all shards for some EE by providing *some* proofs from some other shards containing proofs of amounts available from the previous slot.

## Replies

**adiasg** (2020-01-07):

Whenever `shard[s].balances[s][ee] < xfer_amount`, validators must fetch data from other shards to check `real_balance(s, ee) >= xfer_amount`. With that data at hand, they can be forced to process all ETH transfers to `ee` that they see so that `shard[s].balances[s][ee]` always remains non-negative for all shards.

Ideally, validators would only keep fetching `shard[i].balances[s][ee]` until the summation in `real_balance(shard, ee)` becomes greater than `xfer_amount`. To force them to process whatever ETH transfers they saw that led to this, they must fetch `shard[i].balances[s][ee]` in exactly the same order (hopefully seeded by some common randomness).

---

**cdetrio** (2020-01-23):

Here’s a walk-through of the concept.

- we have three shards: A B C
- When an EE is deployed, it is exists on all shards. Same code, but a different balance and different stateroot on each shard. (Not all conceptions of “EE” are like this, sometimes the term “EE” is used to describe accounts with (code, stateroot, balance) that are deployed to a single shard).
- for each EE, each shard maintains a balance map like this: A: [1, 0, 0].
- we can visualize the global balance map for an EE as a matrix, but note that it is not maintained in whole anywhere. Rather, each shard maintains one row.

```auto
    A   B   C
 A [1,  0,  0]
 B [0,  0,  0]
 C [0,  0,  0]
```

- this is the map(s) for an EE with a starting balance = 1 ETH on shard A.

## same-EE/cross-shard transfers

Same-EE/cross-shard transfers are done by updating the map on the sending shard `shard[s1]`; the map on the receiving shard `shard[s2]` is not updated. In code: `shard[s1].balances[s1][ee] -= xfer_amount` and `shard[s1].balances[s2][ee] += xfer_amount`

- in a block on shard A there’s a txn that transfers 1 ETH to the same EE on shard B. Only the map stored on shard A is updated (Row A), shard B is not aware of this transfer.

```auto
    A   B   C
 A [0,  1,  0]
 B [0,  0,  0]
 C [0,  0,  0]
```

- in a block on shard B there’s a txn that transfers 1 ETH from B to C (in the same EE). only Row B is updated:

```auto
    A   B   C
 A [0,  1,  0]
 B [0, -1,  1]
 C [0,  0,  0]
```

Note that the text doesn’t mention any checks or proofs to do same-EE/cross-shard transfers, perhaps because the operation of adding -1 to the sending cell (row B, col B in the previous example) and +1 in the receiving cell (row B, col C) keeps the EE’s total balance constant. It does say that the “real balance should always remain non-negative”, but it doesn’t say how. If same-EE/cross-shard transfers are allowed without any proofs, then any particular column could become negative.

## cross-EE/same-shard transfers

For cross-EE transfers, the protocol requires proof of an EE’s balance across shards (“real balance”).

> To perform any transfers of ETH between EEs in a block, the shard must contain a Merkle proof from the most recent state of every shard, showing shard[i].balances[s][x] for every shard i to prove the total balance of the EE. … we check that real_balance(s, ee_1) >= xfer_amount.

Take the map from the previous section:

```auto
    A   B   C
 A [0,  1,  0]
 B [0, -1,  1]
 C [0,  0,  0]
```

- to calculate the “real balance” on a shard, you add up the column. The real balance on shard C is 1, A and B have 0.
- In the real_balance() formula, i corresponds to rows in the matrix and s to a column. So real_balance(shard_s, ee_x) is a proof for column s.

real\_balance(shard, ee) = \sum_{i=0}^{shard\_count} shard[i].balances[s][x]

- If same-EE/cross-shard transfers are allowed without any proofs, then checking real_balance(shard_s, ee_x) is not sufficient because any particular column might be negative. However, proof of all columns (i.e. the real_balance() proofs for all shards, not just shard s) could be used to show that the total EE balance is non-negative.

We thus have two versions:

- version A: same-EE/cross-shard transfers do not require any proofs. cross-EE/same-shard transfers require proof of total EE value, i.e. real_balance() proofs for all shards.
- version B: same-EE/cross-shard transfers require a real_balance() proof for the sending shard. cross-EE/same-shard also require a real_balance() proof for the sending shard.

I guess the text is describing version B.

Continuing on, here’s how the balance maps would look before and after a cross-EE/same-shard transfer.

```auto
             -before Txn-

     AliceEE               BobEE

    A   B   C            A   B   C
 A [0,  1,  0]        A [0,  0,  0]
 B [0, -1,  1]        B [0,  0,  0]
 C [0,  0,  0]        C [0,  0,  0]
```

Let’s send the 1 ETH we have in AliceEE on shard C, to BobEE on shard C. To perform the transfer, update two maps (AliceEE and BobEE) for the shard we’re on. In code: we check that `real_balance(s, ee_1) >= xfer_amount`, then set `shard[s].balances[s][ee_1] -= xfer_amount` and `shard[s].balances[s][ee_2] += xfer_amount`

```auto
             -after Txn-

     AliceEE              BobEE

    A   B   C            A   B   C
 A [0,  1,  0]        A [0,  0,  0]
 B [0, -1,  1]        B [0,  0,  0]
 C [0,  0, -1]        C [0,  0,  1]
```

---

**rjdrost** (2020-01-28):

Thanks for the clear walk through of VB’s scheme using a couple of example Eth transfers among shards and EEs!! Extremely helpful as this is a *very* clever scheme—and hence it takes a while to catch up with VB!

One point that I’d like to check is whether I’m correct in surmising that in your examples, the diagonal of your 3x3 shard Eth balance matrix is strictly a decreasing value in the case of cross-shard transfers within the same EE (e.g. transfers from AliceEE to AliceEE on another shard)

Transfers from AliceEE to BobEE do bump up the recipient EE right on the recipient matrix diagonal, but then transfers among BobEE on different shards, would again be strictly decreasing.

Vitalik stated that "Note that individual shard[s].balances[s][ee] values may sometimes be negative.”

But my (correct/incorrect?!) understanding above would indicate that all shard[s].balances[s][ee] would eventually become negative and remain increasingly so for all shards and EEs over time. Or, is there another rebalancing mechanism that I missed?

Thanks for your feedback as I’m not sure I’m reading this correctly.

But I think VB deliberately spec’d this so that transfers only originate from shard[s].balances[s][ee] (i.e. the balance of the EE in the current shard). This gives the important property you point out that ensures that the column sum can only increase in the current block being evaluated (i.e. we’d never expect an off-diagonal matrix entry to decrease from the previous block, hence the column sum at the start of evaluating a transaction block is a strict minimum and is safe to use as the max eth to transfer out of shard[s].balances[s][ee] during the current block)

---

**vbuterin** (2020-01-28):

Yep, on-diagonal entries would only decrease and off-diagonal entries would only increase, unless some extra rebalancing mechanic is added.

---

**drcode1** (2020-01-28):

So, I want to book a hotel using a contract on shard B for 100 dollars. I deposit $100 on shard A in the same EE, then transfer the $100 to shard B using the above “same EE/different shard” mechanism.

…so my impression is that this scheme doesn’t solve the problem of “how does the contract on shard B know I have enough money to pay for the hotel”, it only solves the “meta problem” of ensuring that the EE is not leaking currency. Is that correct? Also, why is it not preferable to just use Merkle proofs for cross-shard transfers directly, with single balances for the EE maintained on each shard? (instead of merkle proofs for inter-EE transfers)

Thanks for any answers to my novice questions.

---

**villanuevawill** (2020-02-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/drcode1/48/707_2.png) drcode1:

> …so my impression is that this scheme doesn’t solve the problem of “how does the contract on shard B know I have enough money to pay for the hotel”, it only solves the “meta problem” of ensuring that the EE is not leaking currency.

Correct.

![](https://ethresear.ch/user_avatar/ethresear.ch/drcode1/48/707_2.png) drcode1:

> Also, why is it not preferable to just use Merkle proofs for cross-shard transfers directly, with single balances for the EE maintained on each shard? (instead of merkle proofs for inter-EE transfers)

This requires either a bitfield mechanism (which essentially veers into another enshrined UTXO model with complexity on its growth), or a queue/nonce model to prevent replays. These discussions are found here:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png)
    [Implementing cross-shard transactions](https://ethresear.ch/t/implementing-cross-shard-transactions/6382) [Sharded Execution](/c/sharded-execution/35)



> One of the requirements of phase 2 is the ability to move ETH quickly from one shard into another shard. Though cross-shard transactions in general are possible through application of the usual receipt mechanism, with the protocol itself needing only to provide access to each shard’s state roots to each other shard, cross-shard ETH requires a little more enshrined in-protocol activity. The reason for this is that we need to keep track of how much ETH there is in each shard, and we need an enshri…



    ![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png)
    [Moving ETH between shards: the problem statement](https://ethresear.ch/t/moving-eth-between-shards-the-problem-statement/6597) [Sharding](/c/sharding/6)



> In general, the way that tokens are handled on a sharded blockchain is through accounts and receipts that exist inside of execution environments. That is, a token is something that exists inside of an EE, in the form of account balances on different shards that have units of that token. On shard A, Alice might have 50 ExampleCoin (EXC) and Ashley 70 EXC, on shard B, Bob might have 40 EXC, etc, and these are all represented as leaves in the EE’s state tree.
> [Untitled%20Diagram]
> Alice transferri…

---

**villanuevawill** (2020-02-05):

Here is a general writeup, https://hackmd.io/g-FvxXFoRDWYGPIEs82AAQ I worked on with [@SamWilsn](/u/samwilsn) and [@adietrichs](/u/adietrichs) that dives into the things mentioned by [@drcode1](/u/drcode1) and other issues/questions with this meta-ee approach. It also explains different scenarios (cross-shard, cross-ee) with examples.

The TLDR is that the meta-ee basically would enshrine a basic account model anyways to work. The scenarios of "how does the contract on shard B know I have enough money to pay for the hotel” are given in there and likely calls for a more enshrined format overall. There are some writeups coming on all of this and suggestions (but this doc will likely be helpful for anyone following along with this discussion). Apologies for the mixed python/rust syntax (these were general brainstorming docs).

