---
source: ethresearch
topic_id: 4578
title: Let's assign prime numbers to transactions instead of coins
author: keyvank
date: "2018-12-13"
category: Layer 2 > Plasma
tags: [accumulators]
url: https://ethresear.ch/t/lets-assign-prime-numbers-to-transactions-instead-of-coins/4578
views: 5485
likes: 17
posts_count: 13
---

# Let's assign prime numbers to transactions instead of coins

(WARNING: This design seems to be broken, see [here](https://ethresear.ch/t/lets-assign-prime-numbers-to-transactions-instead-of-coins/4578/12))

(Previous knowledge of [Plasma Cashflow](https://hackmd.io/DgzmJIRjSzCYvl4lUjZXNQ?view#), [Merkle Sum Trees](https://ethresear.ch/t/plasma-cash-was-a-transaction-format/4261), and [RSA accumulators](https://ethresear.ch/t/rsa-accumulators-for-plasma-cash-history-reduction/3739) is assumed)

Current thoughts on RSA accumulators are all trying to assign prime numbers to non-fungible coins as in Plasma Cash, and use some creative approaches [to batch a large number of coins in log(coins) sized proofs](https://ethresear.ch/t/log-coins-sized-proofs-of-inclusion-and-exclusion-for-rsa-accumulators/3839). [@benj0702](/u/benj0702) came up with the great idea of assigning primes to transactions, by adding a `prime` property to our transactions, which is chosen by the clients. This post tries to further explain this idea. Read the original post [here](https://ethresear.ch/t/plasma-cash-was-a-transaction-format/4261).

A regular Plasma Cash transaction is like this:

```auto
struct Transaction {
    uint256 coinId;
    address recipient;
    uint256 prevBlock;
}
```

Plasma Cashflow transactions (With RSA accumulators) are probably like this:

```auto
struct Transaction {
    uint256 coinStart;
    uint256 coinEnd;
    address recipient;
    uint256[] prevBlocks;
    uint256 prime;
}
```

Notes:

- Instead of a single coinId, we have a range of coins, specified with coinStart and coinEnd. (Read Plasma Cashflow spec)
- We may want to merge contiguous ranges of coins from multiple transactions, so we should provide an array of prevBlocks.
- We also assign a prime number to our transactions.

The rule is: **If you want to spend some range of coins, you should say in which block(s) did you get those coins (`prevBlocks`) and the accumulator of the current block should include the corresponding primes of the parent transactions.**

E.g. if I assign prime 7 to my transaction (which is submitted in block 18) and I get a batched exclusion proof of prime 7 in blocks [A_{18}...A_{100}], I can be completely sure that there isn’t any ***valid*** transaction in blocks (19, 100) that could spend part/all of my coins.

You might ask what happens if someone tried to spend a transaction that is also labeled with prime 7 in block 46? (In other words, what should we do if 7 is accumulated in [A_{45}...A_{46}]?)

Nothing bad happens! It is very important to understand that the ***actual security comes from our Merkle-Sum-Trees***, so here is what the prover should do to convince me that my coins are not spent in blocks (19, 100), he gives me:

- RSA exclusion proof of prime 7 in blocks [A_{18}...A_{45}]
- Merkle-Sum-Tree exclusion proof of my coins in block 46
- RSA exclusion proof of prime 7 in blocks [A_{46}...A_{100}]

Now the question is, how can we synchronize the clients with each other, and prevent them from using each other’s prime for their transactions? (So that their coin history size is reduced as much as possible) Through the operator! The operator may have some kind of **prime pool**, that contains all of the available primes in it. Clients can ask the operator for free primes through some API call, and the operator doesn’t accept transactions with primes that are not free. (Even if he does, nothing bad happens, as previously explained)

Whenever an UTXO is completely spent, its prime can get back into the prime pool and be used again by other transactions.

## Example

Say Alice sent Bob coins (500,1500) through the following tx which is submitted in block 14:

```auto
coinStart: 500
coinEnd: 1500
recipient: Bob
prevBlocks: [...]
prime: 19

(Submitted in block 14)
```

Now Bob owns coins (500,1500), he wants to send coins (500,1000) to Charlie and coins (1000,1500) to David. He simply creates two transactions:

```auto
coinStart: 500
coinEnd: 1000
recipient: Charlie
prevBlocks: [14]
prime: 23

(Submitted in block 18)
```

(Accumulator of block 18 should include prime 19 as the parent transaction is labeled with prime 19, or the transaction is invalid)

```auto
coinStart: 1000
coinEnd: 1500
recipient: David
prevBlocks: [14]
prime: 29

(Submitted in block 20)
```

(Accumulator of block 20 should include prime 19 as the parent transaction is labeled with prime 19, or the transaction is invalid)

Now let’s say Charlie was the owner of coins (0, 500) through some transaction in block 3 with prime 7, and he wants to send coins (250,1000) to Edward

```auto
coinStart: 250
coinEnd: 1000
recipient: Edward
prevBlocks: [18,3]
prime: 31

```

(Accumulator of block 20 should include prime numbers 7 and 23 as the parent transactions are labeled with primes 7 and 23, or the transaction is invalid)

## Replies

**nginnever** (2018-12-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/keyvank/48/15523_2.png) keyvank:

> You might ask what happens if someone tried to spend a transaction that is also labeled with prime 7 in block 46?
> Nothing bad happens! It is very important to understand that the actual security comes from our Merkle-Sum-Trees , so here is what the prover should do to convince me that my coins are not spent in blocks (19,100), he gives me:
>
>
> RSA exclusion proof of prime 7 in blocks (19, 45)
> Merkle-Sum-Tree exclusion proof of my coins in block 46
> RSA exclusion proof of prime 7 in blocks (47,100)

I think you would now need merkle exclusion proofs for all blocks (47-100)  after the spend at block 46 that accumulates your exclusion proof 7.

This assumes your design has no method of stateless deletion.

---

**boolafish** (2018-12-14):

What happens if a bad operator provide client with prime numbers already in use?

Like your example, if 7 is used in some block, the transaction owner need to specify that block with merkle proof instead of accumulation proof. For client to be able to provide the merkle proof instead of accumulative proof, client still need to store all the merkle-tree exclusion proofs in case of misbehaving operator, doesn’t it?

If so, then does this still have the benefit of using accumulative proof?

---

**keyvank** (2018-12-14):

We can check for inclusion of some prime number ***in a range of blocks***. So although 7 is in [A(45)…A(46)], but I can generate a proof that 7 is not in [A(0)…A(45)] and [A(46)…A(100)]

---

**keyvank** (2018-12-14):

The operator can do this. But notice that:

- By doing so, the operator can’t steal my money.
- If I’m not convinced that my coin is not spent in a range of blocks using RSA exclusion proofs, then I ask for merkle-branches. This results in more bandwidth usage for the operator, which is not good for him.
- I can easily exit from the plasma chain, if the operator is messing with the accumulators. By doing so, he is just making the coin histories longer and users don’t want that. Why should he do that? The operator is getting fees from the users.

---

**snjax** (2018-12-15):

This design is broken. You may see more information at [Short S[NT]ARK exclusion proofs for Plasma](https://ethresear.ch/t/short-s-nt-ark-exclusion-proofs-for-plasma/4438/5) and at 18th plasma call.

---

**denett** (2018-12-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/keyvank/48/15523_2.png) keyvank:

> E.g. if I assign prime 7 to my transaction (which is submitted in block 18) and I get a batched exclusion proof of prime 7 in blocks (19,100), I can be completely sure that there isn’t any valid transaction in blocks (19,100) that could spend part/all of my coins.

For this to be the case I think the clients also need to check whether the operator is only doing additions to the accumulator. The operator could add prime 7 in block 20 and remove it again in block 21. In this case there could be a transaction in block 20 that will go unnoticed.

A fix for this could be that the operator provides a Wesolowski proof for every accumulator transition. This proof could be checked on chain, or should be send to every client off chain.

---

**keyvank** (2018-12-15):

Exactly, so in this proposal we require the operator to provide a Wesolowski proof of exponentiation for each block submission on-chain.

---

**nginnever** (2018-12-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> For this to be the case I think the clients also need to check whether the operator is only doing additions to the accumulator. The operator could add prime 7 in block 20 and remove it again in block 21. In this case there could be a transaction in block 20 that will go unnoticed.
> A fix for this could be that the operator provides a Wesolowski proof for every accumulator transition. This proof could be checked on chain, or should be send to every client off chain.

What would the target be for these Wesoloski PoKE that enforces that only transactions can be added? If A_t is transitioning to A_{t+1} I think you would need n (where n is the number of spent txs in A_t) [Wes18] proofs onchain to verify A_{t+1} does not remove anything. This also seems to imply that a UTXO holder would now need t [Wes18] proofs for each block that we want to know a spend hasn’t been removed.

You could potentially batch proofs but I’m not sure if this accumulator works with batching [Wes18] proofs.

---

**denett** (2018-12-15):

Source of below formula’s can be found here: [Compact RSA inclusion/exclusion proofs](https://ethresear.ch/t/compact-rsa-inclusion-exclusion-proofs/4372)

We have to show that:

A_{t+1} \equiv A_{t}^x \mod N

where x is the product of the primes the operator wants to add.

We substitute for x:

x = B\lfloor \frac x B \rfloor + x \mod B

We use the following witnesses:

b=A_{t}^{\lfloor \frac x B \rfloor} \mod N

r=x \mod B

Now the verifier has to check:

b^B.A_{t}^r \equiv A_{t}^x \equiv A_{t+1} \mod N

If this verification is done on chain, all clients can be sure no prime has ever been removed.

---

**keyvank** (2018-12-16):

Didn’t quite understand the problem. How can the operator forge a chain? He can’t hide **valid** transactions from the clients. A transaction is only valid if the primes of its parent transactions are accumulated in the current block. So if there is a suspiciously-valid  transaction (Invalid transactions can be challenged) in a range of blocks that is trying to spend my range of coin, I will get aware of that, as the operator can’t give me a valid RSA exclusion proof of my prime in the given range of blocks. So I ask for a Merkle-Sum-Tree exclusion proof for my coins on that block.

---

**snjax** (2018-12-16):

Let’s consider following UX:

- You are honest user and you own any interval in Plasma Prime.
- You  watch at blocks where something occurs with your money and watch at RSA exclusion proofs, proving that nothing occurs with your money at other blocks
- Only plasma operator knows what inside excluded blocks at your interval. And he can put there anything. Nobody will check him, because you have the RSA exclusion proof and other users watch at their intervals.
- Plasma owner can forge any coins affecting your interval in such block and do a huge number of transactions at blocks excluded for you.
- When the time to exit come, we have two chains: your valid chain and operator’s queer chain. And only the operator knows all details of his chain. These chains are equal for the plasma contract until you find the first transaction where the operator forge his queer money. You may do it with binary search (the exit game with \log_2 N rounds, where N is the number of your transactions). But for a big N we can reach up to 15 exit game rounds. This is not useful.

---

**keyvank** (2018-12-16):

You are right. That’s definitely a bug.

