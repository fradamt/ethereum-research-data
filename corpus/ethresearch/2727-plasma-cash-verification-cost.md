---
source: ethresearch
topic_id: 2727
title: Plasma Cash verification cost
author: kladkogex
date: "2018-07-27"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-cash-verification-cost/2727
views: 3785
likes: 9
posts_count: 10
---

# Plasma Cash verification cost

If there is a Plasma block every minute, then if one holds a coin for a year the size of the non-spend proof for a payment is

60 * 24 * 365 * 100 * 10 * 256 = 17 Gbyte

This assumes that an  average payment transfers 10 coins and that the depth of the Merkle tree is 100

This needs to be multiplied by 2 because the receiver needs to send the change back. So it is 34 GByte total traffic

How feasible is the entire payment then?  How long will it take for sender to upload and for receiver to download and verify 17 GB of data and then pay the change back and then for the sender to verify the proof for the change?   Uploading 17 GB of data will mean days for many people that have asymmetric DSL.

## Replies

**ldct** (2018-07-27):

There are two proposals to alleviate this, what do you think of them?

## Compression

Most of the coin validity proofs are exclusion proofs, and those can be compressed using SNARKs/STARKs. For e.g. if we use constant-sized proofs this means that a coin validity proof will only increase in size when a coin is spent.

Back-of-the-envelope calculation: if a coin is spent once per day, the proof size becomes 1.2 MB per coin.



    ![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png)
    [Plasma Cash: Plasma with much less per-user data checking](https://ethresear.ch/t/plasma-cash-plasma-with-much-less-per-user-data-checking/1298/4) [Plasma](/c/layer-2/plasma/7)



> I’m not sure it would work to use a ZK-snark for the non-existence proofs, unless the parent chain is willing to accept ZK-snarks for the exit transactions. Otherwise, you don’t have enough information to respond to a challenger, right?
>
> Now that I think about it, you are right. In order to be able to respond to type (iii) challenges you have the proofs for every transfer in the coin’s actual history. If there are t blocks and h transfers (history length), then this already reduces required da…



    ![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png)
    [Plasma Cash: Plasma with much less per-user data checking](https://ethresear.ch/t/plasma-cash-plasma-with-much-less-per-user-data-checking/1298/101) [Plasma](/c/layer-2/plasma/7)



> An alternative way to accomplish this might be for the operator to construct a merkle tree T committing to the number of times every coinid has been spent since the genesis plasma block, and to use snarks to verify the integrity of the root hash of the tree. Then a client checking the validity of a coin can download the witness for the branch of this tree that tells him that his coin has been spent h times, and then download h inclusion proofs.
> For clarity, an example of this is shown below fo…

## Checkpointing

We know that withdrawing and re-depositing a coin will “reset” the length of the coin validitiy proof; this construction allows you to do this at an amortized cost of 1 bit of storage (`SSTORE`) per coin.

Back-of-the-envelope calculation: if we do this every 3 months would make the proof size is upper-bounded at 0.4 GB per coin at the cost of a few cents per year.



    ![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png)
    [Plasma XT: Plasma Cash with much less per-user data checking](https://ethresear.ch/t/plasma-xt-plasma-cash-with-much-less-per-user-data-checking/1926) [Plasma](/c/layer-2/plasma/7)



> Plasma XT embraces Plasma Cash’s original vision of simple, reliable, low-cost transactions for everyone in the world.*
> Special thanks to Dan Robinson for discussion and coming up with much of this, as well as David Knott, Joseph Poon, Karl Floersch, and Vitalik Buterin for ideas and feedback that led to this design. Another special thanks to Justin Drake for the gorgeous construction of cryptoeconomic aggregate signatures and to Sunny Aggarwal for the Plasma XT name.
> (enough memes now)
> Reall…

## Combinations Thereof

We can combine these two techniques by doing a checkpoint when even the compressed proofs get too big. Analysis: with checkpoints, we can have the coin validity proof grow as O(f(n)) and the per-unit-time cost of owning a coin grow as O(g(n)) with the constraint that fg \in O(n) where n is the total number of plasma blocks (i.e. increases by 1 per minute).

Three points on this tradeoff space are

1. Bounded proof sizes, constant rent (e.g. 1 cent/year/coin)
2. Constant cost to own a coin, but proof size grows linearly (e.g. 1.7gb /year)
3. Both cost and proof size are O(\sqrt n)

By combining them we relax the constraint to fg \in O(s) where s is the number of spends of the coin (i.e. increases by 1 every time the coin is spent).

---

**kladkogex** (2018-07-27):

You will pay several USD of ethereum costs when you withdraw/redeposit.

And then you have to wait each time you withdraw/redeposit.  I do not think this is a solution people will use.

For SNARKS - what are the computational costs of SNARK calculation - I understand it makes things smaller but how does it influence computational costs? How much time does it take to compute/verify SNARKS?

---

**ldct** (2018-07-27):

> You will pay several USD of ethereum costs when you withdraw/redeposit

Please reread what I wrote more carefully; I am not suggesting a withdrawal and redeposit. The cost with today’s gas fees should be one cent or less.

---

**ldct** (2018-07-28):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> How much time does it take to compute/verify SNARKS?

For succint/scalable verification technology in general, this depends on the exact construction and there are trade-offs, eg STARKs have lower prover cost and longer proof sizes (hundreds of kilobytes vs hundreds of bytes). The trade-offs come into play because depending on exactly how you want to compress the proofs, maybe the verification must be doable on-chain, or maybe it is sufficient to do them client-side.

For the specific zk-SNARK construction I *believe* that the verification costs is low (dominated by two elliptic curve pairings) but the costs of the trusted setup as well as prover cost are quite high ([@kfichter](/u/kfichter) estimated hours per plasma block to produce a proof of the validity of an entire block). For asymptotic costs I have the following table in my notes (note: I don’t understand everything in this table!) for the cost of doing various things for an arithmetic circuit of with N wires, l of which are public:

|  | Proof Size | Prover Cost | Verifier Cost | Setup |
| --- | --- | --- | --- | --- |
| discrete-log based | O(\log N) | O(N) exponentiations | O(N) multiplications | public-coin |
| STARKs | O(\sqrt N) | O(N) multiplications | O(N) additions | public-coin |
| pairing-based SNARKs | O(1) | O(N) exponentiations | O(l) exponentiations + O(1) pairings | structured setup |

Thanks to Jens Groth for the table, but all mistakes are mine.

---

**kfichter** (2018-07-28):

Yeah the ~hours figure came from discussion with vitalik and then spending ~10 mins generating a height 4 merkle tree on my laptop.

---

**kladkogex** (2018-07-30):

[@ldct](/u/ldct) Great table!! Thank you!

Do you know how does the number of wires N depend on the number of transactions ? Is it linear in the number of transactions?

If I have a coin which is one year old, then for the non-spend proof , will the number of wires be linear in time?

Also, what is public coin setup and structured setup?

[@kfichter](/u/kfichter) - I watched Eli Ben Sasson lecture

[https://www.youtube.com/watch?v=VUN35BC11Qw](http://lecture)

The lecture pretty much says that zk-SNARKS with trusted setup are not practical because the setup essentially requires trusted parties. He says during the lecture that STARKS is pretty much the only practical thing.

Why did you guys decide to use SNARKS and not STARKS, and how are you going to do the setup if you will be using SNARKS? I think ZCash had setup that involved 6 people.

Also if  the prover creation takes hours, then since typically the receiver will have to confirm payment and send change back to the the payee, the entire payment may take hours or a day …

How is this going to work for ecommerce ? Plasma is supposed to be for micropayments.

---

**kfichter** (2018-07-30):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Why did you guys decide to use SNARKS and not STARKS, and how are you going to do the setup if you will be using SNARKS? I think ZCash had setup that involved 6 people.
>
>
> Also if the prover creation takes hours, then since typically the receiver will have to confirm payment and send change back to the the payee, the entire payment may take hours or a day …
> How is this going to work for ecommerce ? Plasma is supposed to be for micropayments.

We haven’t decided to use anything, we’re just exploring what’s possible. I agree that hours to create a proof us unreasonable.

---

**ldct** (2018-08-03):

which library did you use?

---

**ldct** (2018-08-03):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Also if the prover creation takes hours, then since typically the receiver will have to confirm payment and send change back to the the payee, the entire payment may take hours or a day …

One thing I think you can do is to use the normal exclusion proof in “real time” and then compress old portions of the coin validity proofs. I am not sure how much this reduces the prover burden, but it shows we can just care about raw throughput instead of latency.

