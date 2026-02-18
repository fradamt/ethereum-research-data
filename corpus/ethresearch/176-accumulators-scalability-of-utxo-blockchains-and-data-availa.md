---
source: ethresearch
topic_id: 176
title: Accumulators, scalability of UTXO blockchains, and data availability
author: JustinDrake
date: "2017-10-25"
category: Sharding
tags: [data-availability, accumulators]
url: https://ethresear.ch/t/accumulators-scalability-of-utxo-blockchains-and-data-availability/176
views: 14407
likes: 21
posts_count: 28
---

# Accumulators, scalability of UTXO blockchains, and data availability

This post gives a high level and informal construction of a UTXO blockchain where node resources scale sublinearly in all respects (storage, disk IO, computation, and bandwidth). The scheme can be applied more generally to an Ethereum-style blockchain but bandwidth would remain a bottleneck for full scalability (bandwidth scales linearly with public state diffs). A key ingredient are (non Merkle-) cryptographic accumulators. These accumulators are promising for the blockchain space as a whole because of their applicability at both the consensus layer and the application layer.

I need to post a disclaimer that I am not a cryptography expert and that everything below should be taken with a huge grain of salt. Having said that, it does seem like the approach below is a possible path towards finding the blockchain scalability holy grail. Thanks to Vitalik for challenging my ideas and encouraging me to make this write-up.

**Background on accumulators**

Merkle trees fit in a wider class of cryptographic accumulators that are space and time efficient data structures to test for set membership. Non-Merkle accumulators tend to fall into two classes: RSA accumulators and elliptic curve accumulators. There has been a fair amount of academic study of non-Merkle accumulators and they are used in several practical applications outside of the blockchain space. The discussion below focuses on RSA accumulators to give a bit of intuition, but an elliptic curve accumulator may well be more appropriate.

RSA accumulators are based on the one-way RSA function `a -> g^a mod N` for a suitably chosen `N`. The set `{a_1, ..., a_n}` is compactly represented by the accumulator `A = g^(a_1 * ... * a_n)`. The witness `w` for an element `a_i` is built like `A` but skipping the `a_i` exponent, and checking the witness is done by checking that `w^a_i` equals `A`. Adding elements `b_1, ..., b_m` to the accumulator is done by exponentiating `A` by the “update” `b_1 * ... * b_m`, and likewise for the witness `w`.

Notice that RSA accumulators are constant size (a single group element) and witness updates are cleanly “segregated” from the other set elements. Compare this to Merkle trees which are linear in size to the number of leaves, and where an update to one element will modify internal tree nodes which will “corrupt” Merkle paths (witnesses) for other elements. Notice also that updates to RSA accumulators are batchable, whereas Merkle tree updates are not batchable and take logarithmic time for each element, impeding sublinearity.

Non-Merkle accumulators can have all sorts of nice properties. They can be “dynamic”, meaning they accept both additions and deletions to the tracked set, which is something we need. They can be “universal”, where nonmembership can be proved in addition to membership. They can have optimal space/time complexities. They can be zero-knowledge. Having said that, it’s not all rosy and every scheme has its own trade-offs. For example, some constructions require a trap-door (like Zcash). The perfect accumulator for our needs may not be readily available in the literature (where the decentralised and fully open context is rarely assumed). The nitty-gritty detail is beyond the scope of this post ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

**Construction**

The UTXO set is kept track of using a non-Merkle constant-sized dynamic accumulator with segregated, efficient and batchable updates for both the accumulator and witnesses. In terms of maintaining state, fully validating nodes and mining nodes only have to keep track of the header chain (which contains batched and constant-sized accumulator updates). Everything else (UTXO set, transactions, blocks) is prunable. We are in the [stateless client paradigm](https://ethresear.ch/t/the-stateless-client-concept/172) where transactions provide state and witnesses on a need-to-have basis, thereby relieving nodes of storing state (in our case, the UTXO set). Neither users nor nodes have to do the costly work of maintaining a Merkle tree. At this point we have sublinear storage and disk IO.

We next make use of SNARKs/STARKs to achieve sublinearity of computation and bandwidth. Instead of explicitly disclosing transaction data (UTXOs, amounts, signatures, witnesses) we allow for transactions to contain only the final accumulator update (batched across UTXOs), as well as a succinct proof that the accumulator is valid. Here validity includes:

- Knowledge of witnesses for the UTXOs to spend
- Knowledge of valid signatures for the UTXOs to spend
- Money conservation (the sum of the amounts in the UTXOs to spend is less than the sum in the new UTXOs)

Notice that a single transaction can spend an arbitrary number of UTXOs (from different signers/owners) and create an arbitrary number of new UTXOs without explicitly communicating them to nodes. Instead, all the UTXOs are subsumed in the accumulator and the updates, and size (for bandwidth) and computation are both sublinear. Indeed, the transaction consists of the accumulator update and a SNARK/STARK, both of which sublinear (generally constant or close-to-constant) in size and in time (for the SNARK verification and accumulator update).

**Data availability**

The ideas above came as I was attempting to solve [data availability](https://github.com/ethereum/research/wiki/A-note-on-data-availability-and-erasure-coding). The above scheme doesn’t solve data availability, but side-steps significant chunks of it. In particular:

- Private state (e.g. Bitcoin UTXOs or Ethereum accounts) that only ever needs to be known by a single party does not need to be publicly available. My guess is that a large portion (90%?) of Ethereum’s current ~10GB state falls in this category, or can be made to fall under this category by slightly tweaking the state management of individual contracts.
- Transaction data does not need to be publicly available because we use SNARKs/STARKs instead of fraud proofs.

In the context of an Ethereum-style blockchain, the only data that needs to be publicly available is state that at least two (non trusting) parties may require to make transactions. Think for example of a public order book where updates to the order book need to be known to the wider public to make trades. For such applications, the transaction (including the SNARK/STARK) needs to be extended to include the state diff. Notice that the state diff can be gossiped to the validator nodes and then immediately dropped after being checked against the SNARK/STARK. This leaves bandwidth as the final piece of the puzzle for full Ethereum scalability.

I am cautiously optimistic that bandwidth scalability can be solved convincingly. But even if not, in practical terms bandwidth is possibly the least pressing bottleneck. The capacity of a single node today is enough to support applications with significant amounts (think tens of gigabytes per day) of public state diffs, and Nielsen’s law (50% bandwidth capacity increase per year) is showing no sign of stopping.

## Replies

**vbuterin** (2017-10-25):

Thanks a lot for making the writeup!

One specific question: how would the N be chosen? I can only think of two schemes. The first is an N-party trusted setup, where each party provides a large prime p_i, and p_1 * … * p_n = N becomes the value. The other is much more inefficient, and is basically to create a really really big random number, “grind” out as many small factors as you can and use the result, hoping that it has enough large primes in it.

To calculate the required size of such a huge value, we can use a heuristic. We have a number N, and want to get the expected number of prime factors above P that it contains (we then can use a Poisson distribution to find the probability of it having at least two). This is equivalent to iterating over primes Q between P and N, and for each prime there’s a 1/Q chance that N is a factor. For every *value* Q between P and N, there is a 1/ln(Q) chance that Q is prime. Hence, the expected number of prime factors is sum[x = N…P] 1 / (x * ln(x)). The integral of 1 / (x * ln(x)) is ln(ln(x)), so this gives a result of: ln(ln(N)) - ln(ln( P)). So for example an 80-KB number (ie. near 2^640000) will have in expectation ln(ln(2^640000)) - ln(ln(2048)) >= 2048 bit prime factors, or ~5.74. So if we want to *really* guarantee a good modulus without a trusted setup it really does need to be extra-large.

---

**vbuterin** (2017-10-25):

Also, it’s important to note for the sake of this discussion that RSA accumulators support deletion (source here: https://eprint.iacr.org/2015/087.pdf)

Suppose you have an accumulator A that contains p, with witness W§. You can simply set `A' = W(p)` to make the new accumulator. To calculate a new witness W(q) for `q != p`, you find a, b such that `ap + bq = 1` (I believe `b = q^-1 mod p` and `a = p^-1 mod q` suffice to give this), then compute `W'(q) = W(q)^a * W(p)^b`. Notice that:

```
W'(q)^q
= W(q)^aq * W(p)^bq
= A^(1/q)^aq * A^(1/p)^bq
= A^(1/qp)^(aqp + bq^2)
= A^(1/p)^(ap+bq)
= A^(1/p)
= A'
```

So the witness is correct, and note also that for p=q it’s not possible to find suitable a,b values. That’s good to know, as this is crucial for being able to prevent double-spends.

---

**JustinDrake** (2017-10-26):

> One specific question: how would the N be chosen?

The multiparty computation is an attractive option. We’d probably want each party to prove primality somehow, and I think the primes `p_1, ..., p_n` may actually need to be *safe*, where a prime `p` is safe if `(p-1)/2` is also a prime.

Going down the random number route, [this paper](https://drive.google.com/open?id=0B9lwQ01C7V_fcmtRRW5mM19RTUk) (see page 262) improves upon your suggestion by picking several smaller random numbers instead of a single huge one. The paper is from 1999, and back then the construction was not practical. Maybe there’s been some theoretical improvements in the last 18 years.

(Half joke idea.) Let’s assume we can find a random number construction today that is practical only if we spend $X million in computation resources to filter out small primes and get a workable bit length. Then we can setup a massively distributed computing (similar to SETI@home) alongside an Ethereum contract that trustlessly dispenses bounties proportional to the size of the prime factors found. If $X million is too large for the Ethereum Foundation to cover, one can setup an Ethereum 2.0 ICO where some the proceeds go towards the bounties.

Another option of course is to investigate non-RSA accumulator schemes. I found [this scheme using Euclidian rings](http://kodu.ut.ee/~lipmaa/papers/lip12b/cl-accum.pdf) that does not require a trusted setup.

> Also, it’s important to note for the sake of this discussion that RSA accumulators support deletion

Thank you for pointing out this neat trick!

---

**JustinDrake** (2017-10-28):

Turns out I was wrong regarding batching for the RSA accumulator. The reason is that when batch adding elements b_1, ..., b_m, the bit size of the update exponent b_1 * ... * b_m grows linearly with m. (The exponent can be reduced modulo the trapdoor ϕ(N) — Euler’s totient — but that’s of no use to us.) Using an RSA accumulator may still be significantly more appropriate than a Merkle accumulator, especially in the stateless client paradigm, but without batching for witness updates I cannot see how to achieve sub-linearity of bandwidth and computation.

On this note, [this paper](https://eprint.iacr.org/2009/612.pdf) places an (obvious) lower bound on the bit size of batch deletions. The data needed to communicate m deletions within a set of n elements to update *all* witnesses is of size at least \log{n \choose m} bits, and this data needs to be publicly available. The worst case occurs when m = n/2, in which case O\big(\log{n \choose n/2}\big) = O(n).

The dream of finding the scalability holy grail is not lost but we know that the data that needs to be made available by the transaction sender for batch deletions of *all* witnesses in the worst case is at least O(n). This means we need to solve data availability, even in the simple UTXO model, for bandwidth scalability.

---

**JustinDrake** (2017-11-16):

I have good news. I think the [batched accumulator impossibility result](https://eprint.iacr.org/2009/612.pdf) referenced above can be worked around in our context of batched transactions. In short, we can setup batched transactions so that the \log{n \choose m} bits can be derived from communication that occurs during the construction of the batched transactions, bypassing data availability concerns raised by Camacho’s proof.

Camacho’s proof distinguishes the “manager” and the “user”. Instead I distinguish three entities and use blockchain terminology:

1. The “senders”: users making accumulator deletions as part of a given batched transaction.
2. The “hodlers”: users not making accumulator deletions as part of a given batched transaction. (So Camacho’s “user” is the union of senders and hodlers.)
3. The “batcher”: the entity that prepares the batched transaction and the witness update data. This is Camacho’s “manager”. It can be a concrete entity (e.g. a third party helper) or an abstract entity (e.g. the senders performing a multi-party computation among themselves).

The key idea is to build the batched transaction so that the senders know which of their UTXOs are being spent. (This is something we’d probably want anyway, for sanity.) To guarantee that, the SNARK/STARK in my original post can be extended to prove that the spenders know they are spenders. If the batcher is a third party, this can be done by proving ownership of digital signatures from the senders giving their blessing for a given “template” batched transaction. Similarly if batching is done with an MPC, then the MPC needs to produce such a proof somehow.

Now let’s go back to Camacho’s proof. Given a batched transaction (which is very sublinear in size) it is now possible for the senders and hodlers to reconstruct the set of deletions, even before the batched transaction is confirmed onchain. Indeed, by construction senders know that their UTXOs were spent in the batched transaction, and this information was communicated offchain. And hodlers know that their UTXOs were not spent, because they know they didn’t participate in building the batched transaction in the first place.

Another way to think of this is that the witness update data can be split into two parts. One part is private and offchain, for the spenders, without public data availability requirements. The other part requires public data availability, for the hodlers. Camacho’s proof applies to both parts in aggregate, and so breaks down for us purposes.

It seems hope is restored that a fancy accumulator scheme may yield sublinear data availability after all. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**vbuterin** (2017-11-17):

And there’s already an existential proof that this is possible in one very very specific case: when you are using a Merkle tree as the accumulator, and all of the senders happen to be within one particular subtree. The rest of the network only needs to know about the subtree root change, and everything within the subtree can be communicated between the senders.

---

**aniemerg** (2017-11-17):

So does this require all spenders to be online and interact with the batcher until the batched transaction is complete? That is, a sender submits a transaction, waits for a “template” batched transaction, then must sign the batch?

That seems quite challenging. Wouldn’t a template batch become invalid if even one sender drops off the network between submission and the signing of the template batched transaction?

---

**asdf_deprecated** (2017-11-18):

Related Stack Exchange question: https://crypto.stackexchange.com/questions/53213/accumulators-with-batch-additions (maybe one of you posted it)

---

**JustinDrake** (2017-12-05):

You make a good point [@aniemerg](/u/aniemerg). (Apologies for the late reply; I’ve been mulling over this in search of a convincing solution ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)  )

I have a few ideas to address the problem. The first three ideas can be combined for varying sophistication and effectiveness.

1. Identifiable aborts: Basically the batcher can take whoever seems online right now and attempt to organise a corresponding batched transaction. So long as aborts are identifiable (this is trivial for a third party batcher; not so clear in the MPC case) then simply retry without those who aborted.
2. Dropout tolerance: Consider the following slightly more general template scheme, which allows for a small number of dropouts. Instead of containing transactions that must all confirm together, the template contains “candidate” transactions for which the corresponding candidate spender can drop out. The template is shared with auxiliary information so that the spenders can compute the witnesses for the transaction recipients if given the subset of transactions that eventually confirmed. The batcher makes a best effort attempt to gather signatures (asynchronously) until the dropout rate is reasonable, then builds the new accumulator value, and also includes \log{{a}\choose{b}} bits of information to the final transaction, where a is the total number of candidate transactions and b is the number of confirmed transactions. Note that this scheme is workable if b is close to a. For example, if a=250 and b=240 (dropout rate of 4%), then that’s only 58 additional bits.
3. Sub-batches: If several transactions are controlled by the same spender then those transactions can form an atomic “sub-batch”. (That is, either all corresponding transactions are dropped off, or none.) This allows to replace a in the above idea from the number of candidate transactions to the number of candidate spenders.
4. Delayed witnesses: The following idea might work well for micro-transactions. The batcher is a third-party that does batching-as-a-service with a scheduled batch, say, every 5 minutes. Spenders that want a transaction in the next batch send it to the batcher and get a signed receipt for inclusion in the next batch. Now the batcher is making the promise that 1) the transaction will get included in the next batch, and that 2) he will deliver the corresponding recipient witnesses once the batched transaction has gone through. (If the spender can’t guarantee delivery of the recipient witnesses to the recipient, the transaction would be simultaneously spent and “uncashable”, hence why I suggest limiting this to micro-transactions.) These two promises can be backed with a collaterised contract that would heavily penalise the batcher in case of bad behaviour, or at least guarantee witness data availability with onchain challenges. Over time the batcher may be able to use his reputation as a trustworthy service provider as additional collateral.

---

**kladkogex** (2017-12-13):

Another data  structure that can be used for accumulators are Bloom filters. Although Bloom filters are probabilistic data structures, parameters of a filter can be selected to force false  positive rate to be exponentially low.

Arguably RSA accumulators are also probabilistic, since they use probabilistic primes. Good things about bloom filters is they have fixed time additions and removals.

[Here is a Wiki page on bloom filters](https://en.wikipedia.org/wiki/Bloom_filter)

If you use a counting Bloom filter, then it will support removal, and the hash of the Bloom filter can be included in the header. The Bloom filter itself will then become the witness.  Bloom filters can be compressed for storage or network communication ([for example as explained here (http://www.eecs.harvard.edu/~michaelm/NEWWORK/postscripts/cbf2.pdf). So another option is to include a compressed Bloom filter in the header, and then the element itself becomes the witness.

An approximate formula for false positives is

![image](https://ethresear.ch/uploads/default/original/1X/1e4363584ab3eb3dad174a982d52c4ec3e9681ca.png)

k is the number of hashes in the filter, m is the number of elements, and n is the size of the filter in bins

It is a tradeoff of computation vs witness size.  The more hashes you are willing to do during the witness verification, the smaller is the filter size.

It is interesting to understand how a bloom filter would perform vs Merkle tree vs RSA accumulator …

Bloom filters are widely used in routing tables of network routers, arguably if RSA accumulators would be faster Cisco guys would use them.

I think what we can do is agree on a particular realistic real-life benchmark such as number of elements, insertions, deletions etc. and then benchmark different approaches.

---

**vbuterin** (2017-12-14):

I looked at bloom filters before. The problem is that for the false positive rate to be low enough to be cryptographically secure, the size of the bloom filter basically needs to be almost the same as the size of a plain concatenated list of the hashes of the elements.

You can prove this info-theoretically. Informally: suppose that there is a list of 2^64 elements of which you are including N. From a bloom filter with 160 bit security, it’s possible to recover which N elements you’ve included with probability ~1 - 2^32. Hence, that bloom filter basically contains the info, and the size of the info is roughly 64 * N bits; and so the bloom filter must contain at least 64 * N bits.

---

**vbuterin** (2017-12-14):

Actual accumulators get around this by requiring witness data.

---

**kladkogex** (2017-12-14):

Interesting …

I found a paper that discusses [using bloom filters as crypto accelerators](https://www.jstage.jst.go.jp/article/transinf/E91.D/5/E91.D_5_1489/_pdf)

---

**vbuterin** (2017-12-14):

> If you try determining which elements are in the set by brute forcing over 2^64 candidate elements you will recover the true elements of the set, but also recover lots of false positives, and there will be no way for you to distinguish good guys from bad guys

False. The bloom filter has 160-bit security, meaning the false positive rate is 1 in 2^160. Hence, the chance that *any* of the 2^64 elements that are not part of the N will show up as a positive is 1 in 2^96 (oh wow, it’s even less probable than I thought, I guess I double-counted somewhere).

---

**kladkogex** (2017-12-14):

Now I understand that your argument is totally correct - sorry …

I think the mistake I made is relying on the formula for the false positives from Wikipedia, it is only true when m is much larger than kn, essentially for filters which are underloaded …

It looks like the paper referred to above is doing a bit more then just using a bloom filter, they are citing Nyberg accumulator, I need to understand how it works …

---

**kladkogex** (2017-12-14):

Here some rephrasing of the batched impossibility result for deletions, additions, and updates to make it a bit simpler to understand. I am using an argument similar to what Vitalik has used above.

Let A be the value of the accumulator, Let the size of accumulator in bits be L_{acc}. Let the size of a typical witness in bits be L_{wit}. Let N be the number of elements in the set, and let W[i] be a set of all witnesses, where 0 \le i < N.

Let us suppose that the accumulator is cryptographically secure to prove both participation and non-participation.

Then, it is clear that for large N one has

L_{wit} \sim O({log_2 N})

This comes from the fact that for a fixed accumulator value A, W[i]  encode all N elements of the set, and the dimension of the encoding space needs to be at least N.

Now consider the case where m distinct elements are added to the accumulator.  Then the new set W' can be described as the set W plus the delta layer w. Using the same argument as above, the size of w in bits L_{delta} should be at least

L_{delta} \sim O(m * log_2 N)

This comes again from the fact that with everything else fixed, the delta layer w can be used to encode the entire batch set of m distinct elements. Computing the delta layer is equivalent to computing the updated set  W' from W.

Since the delta layer is linear in m, the amount of computation  needed to derive the delta layer must also be at least linear in m.  This is essentially Camacho proof.

For large N it does not really matter whether one is talking about additions or deletions.  It is also true for unique updates (if each update in a set of m updates is touching a different element).

---

**Silur** (2017-12-17):

regarding delegated solutions for data availability: http://arxiv.org/abs/1712.04417v2

question: why force the N-party trusted setup for the RSA modulus?

is there some theoretical or philosophical argument against the trustless setup I proposed earlier and it got deleted?

---

**vbuterin** (2017-12-17):

> is there some theoretical or philosophical argument against the trustless setup I proposed earlier and it got deleted?

Sorry, which trustless setup was this?

I’m not aware of a trustless setup for RSA that doesn’t generate numbers hundreds of times larger than what a trusted setup can do.

---

**Silur** (2017-12-18):

let `n` be the size of the modulus, we have A and B with respective private inputs `iA = (pa, qa); iB = (pb, qb)`; trying to compute

f(i_a, i_b) = (p_a + p_b) \times (q_a + q_b) = N

let M' be the product of the first pimes such that M' = 2^\frac{n}{2-1} (just an efficiency improvement)

we first help coordinating the selection of a reasonable p_b without leaking p_a

- A choose random p'_a \in \mathbb{Z}^*_{M'} , p_a \in \mathbb{Z}_M'
- B choose random p'_b \in \mathbb{Z}^*_{M'} , \alpha_b \in \mathbb{Z}_M'
- A and B perform a two-way ANDOS buy-sell with A selling (p'_a, p_a) and B selling (p'_b, \alpha_b) and f being f((p'_a, p_a), (p'_b, \alpha_b)) = p'_a \times p'_b - p_a - \alpha_b \mod M'
- B gets \beta and computes p_b =  \beta + \alpha_b \mod M'

With knowledge of p_b = p'_a \times p'_b - p_a - \alpha_b \mod M' one can only obtain that (p_a + p_b) is in \mathbb{Z}^*_{M'}

Trivially perform B&F division test, then repeat for q and test the output N.

ANDOS protocols scale to N-parties so no worries about PKCS compatible moduli

---

**JustinDrake** (2017-12-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/silur/48/199_2.png) Silur:

> and it got deleted

I didn’t get an email notification for your post. It probably wasn’t successfully posted (as opposed to getting deleted).

I’m a little bit confused by the trustless setup you are proposing. Would you mind editing your post to add details and cleanup the exposition? (I think there are several typos that makes things hard for me to follow.) Below are specific questions.

Is this actually a trustless setup, or are you proposing an N-party trusted setup?

![](https://ethresear.ch/user_avatar/ethresear.ch/silur/48/199_2.png) Silur:

> let M' be the product of the first pimes such that M'=2^\frac{n}{2-1}

What do you mean by “first primes”? Also, do you really mean M'=2^\frac{n}{2-1}=2^n?

![](https://ethresear.ch/user_avatar/ethresear.ch/silur/48/199_2.png) Silur:

> two-way ANDOS buy-sell

Would you mind pointing to a specific construction/paper? I’m new to All-or-Nothing Disclosure of Secrets protocols.

![](https://ethresear.ch/user_avatar/ethresear.ch/silur/48/199_2.png) Silur:

> f being f((p'_a, p_a), (p'_b, \alpha_b)) = p'_a \times p'_b - p_a - \alpha_b \mod M'

Is this the same f as defined above, i.e. f(i_a, i_b) = (p_a + p_b) \times (q_a + q_b)?

![](https://ethresear.ch/user_avatar/ethresear.ch/silur/48/199_2.png) Silur:

> B gets \beta

What is \beta?

![](https://ethresear.ch/user_avatar/ethresear.ch/silur/48/199_2.png) Silur:

> perform B&F division test

What is the B&F division test?


*(7 more replies not shown)*
