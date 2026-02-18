---
source: ethresearch
topic_id: 7211
title: Multi-layer hashmaps for state storage
author: dankrad
date: "2020-03-28"
category: Sharding
tags: []
url: https://ethresear.ch/t/multi-layer-hashmaps-for-state-storage/7211
views: 5483
likes: 8
posts_count: 11
---

# Multi-layer hashmaps for state storage

*TL;DR:* An improved hashmap construction to store state that does not depend on a combination with Merkle trees to resolve collisions, and therefore gets rid of DOS attacks described in the previous construction. The construction is efficient as long as the number of stored elements is not much larger than the degree of the polynomials used for storage.

# Background

Please refer to

- Hashmap-based polynomial commitments for state for an introduction on Kate commitments and multi-reveals
- Using polynomial commitments to replace state roots for more motivation, and also how to open several polynomials using just one opening

# Construction

As in my previous construction ([Using polynomial commitments to replace state roots](https://ethresear.ch/t/using-polynomial-commitments-to-replace-state-roots/7095/6)), we will use polynomials in the Lagrange basis to store values (which will be hashes of key-value pairs) at point evaluations of the polynomial. In a polynomial p(x) = \sum_{i=0}^{n-1} a_i x^i of degree n, we can store n different values, for example at the positions 0, 1, \ldots, n-1. In practice, this will be on a subgroup rather than integers for efficiency, but we don’t need to worry about this for the description of this construction.

Here is how we will use polynomial commitments to store a key-value map: Let p_i(X) \in \mathbb{F}[X], i=0, 1, 2, \ldots be an infinite sequence of polynomials of degree n. We say that the key-value pair (k, v) is stored at x in polynomial p_i if p_i(x) = \mathrm{hash}(k,v). We say nothing is stored at x in p_i if p_i(x)=0. If all p_i(x)=0 for x\in\{0, \ldots, n-1\} then p_i is “empty” and its commitment value doesn’t have to be stored.

We start with all p_i empty. Iteratively, for each key-value pair (k,v) to be stored, we will

- Check x=\mathrm{hash}(k, 0)\% n in p_0
- Check x=\mathrm{hash}(k, 1)\% n in p_1
- Check x=\mathrm{hash}(k, 2)\% n in p_2
- …

until we either encounter k has been stored or an empty position in p_i. We then store \mathrm{hash}(k,v) at p_i(x) for x=\mathrm{hash}(k, i)\% n.

# Performance

- To prove membership/an existing key, only a single value has to be decommitted (as by construction, the same key cannot be added twice). The total witness size is only the data plus one group element for the proof, for all data in aggregate (amortized it is just the data that has to be provided, as the group element is negligible)
- To prove non-membership (and adding a new key), a number of values will have to be provided. Below I will show that the number amount of data that has to be provided to prove non-membership is about m/n, where m is the total number of keys stored.

As a note, by separating keys and values into two separate polynomial sequences, only the keys have to be provided and not the values for proofs of non-membership.

## Number of non-empty polynomials

To estimate how many polynomial commitments we have to store in this construction, we can compute the expected number of “overflows” if we want to store m elements in a layer of size n (i.e., in a polynomial of degree n).

A position (“bucket”) in a polynomial overflows if more than one key-value pair would be stored at it. In other words, we can get the expected number of overflows per bucket by computing for each position x, how many elements in excess of 1 (since it can hold 0 or 1 elements) it is expected to store, which is

- The expected number of elements stored at x minus one
- Plus the probability that 0 elements will be stored at x; i.e.

E_x(m) = \frac{m}{n} - 1 + \left( 1-\frac{1}{n}\right) ^ m

The expected total number of overflows E can be computed via linearity of expectation:

E = \sum_{x=0}^{n-1} E_x(m) = m + n \left( \left( 1-\frac{1}{n}\right) ^ m - 1\right) \approx m + n (\mathrm{e}^{-\frac{m}{n}} - 1)

This also lets us easily compute the number of elements that are stored at this layer, i.e. do not overflow

F = E - m \approx n (\mathrm{e}^{-\frac{m}{n}} - 1)

Lets look at two possible regimes: If m \gg n

E \approx m + n (\mathrm{e}^{-\frac{m}{n}} - 1) \approx m - n

If m \ll n:

E \approx m + n (\mathrm{e}^{-\frac{m}{n}} - 1) \approx m + n\left(1 - \frac{m}{n} + \frac{1}{2} \left(\frac{m}{n}\right)^2 \mp \ldots - 1\right) \approx \frac{1}{2}\frac{m^2}{n}

Estimating the last layer as the one at which an expected 0.5 elements are stored, the second to last layer has \frac{1}{2}\frac{m_{-1}^2}{n} = \frac{1}{2} \Rightarrow m_{-1}= \sqrt{n} elements stored (Sanity check: This is exacty what we would expect from the birthday paradox, so we’re on the right track). Layer last but two would have \frac{1}{2}\frac{m_{-2}^2}{n} = m_{-1} = \sqrt{n} \rightarrow m_{-2} = \sqrt{2n\sqrt{n}} = \sqrt{2} n^{\frac{3}{4}}. We can iterate this until we get to a “relatively full” layer, at which point th m \gg n regime takes over.

From this we see that what will happen is that

- We will have m/n almost full layers
- Then we will have a number \delta of layers which will get gradually more empty

The total number of layers is thus m/n+\delta. \delta depends weakly on n, and my numerical estimate is \delta(n=2^{24})\approx 4 and \delta(n=2^{32}) \approx 5.

Since the layers at the end get empty very quickly, the number of reveals necessary to prove non-membership does not contain \delta in the average case, and thus only ca. m/n+1 reveals are necessary to prove non-membership.

## DOS attack

We will consider the following DOS attack:

- How many extra layers \epsilon can an attacker add to the expected m/n+\delta layers (effectively forcing the storage of m/n+\delta+\epsilon layers by grinding)

Note that this also puts a limit on any attack to an individual key: An attacker cannot add more than \delta+\epsilon elements to the (expected) non-membership proof of length m/n. The real limit is smaller than this.

### Attack

Let’s assume that the store is currently empty. This is roughly equivalent to having m/n+\delta layers (partially) filled and trying to fill up the layers after these layers, so we should arrive at the same result modulo a small constant (It is very easy to create a collision in almost full layers).

I assume that the best strategy for the attacker will probably be to fill every layer up to level \sqrt{n} [^1]. Assuming layers 0, \ldots, {\ell-1} are each filled with \sqrt{n} elements, inserting a new element into p_\ell means trying to create a key that collides in each of these layers, needing \sqrt n^\ell computational power. Most of the computation will be required to insert the last element.

At n=2^{24} \Leftrightarrow \sqrt{n}=2^{12} will become infeasible at around \ell=7. This means a total number of \delta=8 layers could be added by an attacker at a computational cost of 2^{84} and the economic cost of inserting 7\cdot 2^{12} \approx 28{,}000 keys.

At n=2^{30} this becomes \delta=7 at a computation cost of 2^{90} and the economic cost of inserting 6 \cdot 2^{15} \approx 200{,}000 keys.

[^1]: It would be interesting to try and improve this attack; the attacker can maybe do slightly better by filling up lower layers a bit more and higher layers a bit less. Attacks should be compared on the basis of inserting the same number of keys, as we assume that inserting order of n keys would be prohibitively expensive.

## Replies

**vbuterin** (2020-03-28):

I really like this! It outperforms my own schemes because:

1. It does not require complicated sorting arguments, so it’s light on constraints-per-value
2. Both a read and a write are simply a small set of in-place reads and writes of a single evaluation, so you can use a bunch of standard schemes for batch reading, batch writing, updating witnesses, etc. It potentially even allows the block proposer (or whoever the final witness generator is) to be stateless.

The removal of any need for a Merkle tree at layers below is also great.

---

**alinush** (2020-04-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> To prove membership/an existing key, only a single value has to be decommitted (as by construction, the same key cannot be added twice). The total witness size is only the data plus one group element for the proof, for all data in aggregate (amortized it is just the data that has to be provided, as the group element is negligible)

Are you saying that, *for membership*, you only need to prove \exists i such that p_i(\mathsf{hash}(k,i)) = \mathsf{hash}(k,v)? In other words, just reveal i and a KZG evaluation proof for p_i(\mathsf{hash}(k,i))?

Don’t you also have to prove v is the *only* value of key k? After all, the authenticated data structure can be constructed maliciously and the same key can be added twice, no?

i.e., Don’t you have to prove that no other values for k exist in the other polynomials p_{i'}(X)?

i.e., \forall i' \ne i:

p_{i'}(\mathsf{hash}(k,i')) = \left\{\begin{array}{ll}\mathsf{hash}(k', v'),\ \text{for any v' and any}\ k'\ne k\\ 0\end{array}\right.

Otherwise, it seems I could pick two different indices i,j and store (k,v) at p_i(\mathsf{hash}(k, i)) while storing a *different* (k,v') at p_j(\mathsf{hash}(k, j)).

Then, I could equivocate about the value of k: I can convince you k has value v with a proof against p_i or it has value v' with a proof against p_j.

Maybe this can be worked around by splitting up the p_i's into two polynomials (as mentioned in your post): one for keys (e.g., \alpha_i(\mathsf{hash(k,i)}) = k) and one for values (e.g., p(\mathsf{hash(k,i)}) = v). Then, you’d have to show that all the \alpha_i's don’t share any k's.

---

**dankrad** (2020-04-08):

I see. It seems indeed possible that this does not fit the definition of an authenticated data structure. It will still work for our use case, as long as you know that the data structure is always manipulated in the way I described here. So basically, whenever you insert a key, you have to include a proof of non-membership. As long as the data structure is consistently manipulated in this way, it is safe. It is true that you cannot trust it if someone just gives you the root for which you don’t know the history.

---

**alinush** (2020-04-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> So basically, whenever you insert a key, you have to include a proof of non-membership. As long as the data structure is consistently manipulated in this way, it is safe

But, in the stateless Ethereum setting, a stateless verifier can be tricked by a malicious miner who constructs the authenticated data incorrectly, no?

I don’t think I fully understand the setting and its assumptions.

I thought it was very important for a stateless verifier to be able to verify the blockchain from block 0 to n by relying on membership proofs to data accessed by contracts (and on somehow having the contracts themselves, possibly also via membership proofs).

---

**dankrad** (2020-04-08):

But that would be in resolved by assuring validity of state transitions: A stateless verifier knows that the data structure was correct at block n. They check the state transition from block n to n+1. If that state transition was correct, the data structure at n+1 was correctly constructed, because all accesses go through all the proofs as described.

---

**alinush** (2020-04-08):

I see. So, at block n, I have:

1. the previous digest d_{n-1} and the new digest d_n,
2. proofs (\pi_i)_{i\in R} w.r.t. d_{n-1} for all the |R| reads and,

ideally, there’s a single aggregated proof \pi_R for all the reads
3. the set of all writes W (perhaps with some auxiliary information (\mathsf{aux}_i)_{i\in W} to help me compute or verify the new digest d_n).

ideally, there’s some constant-sized auxiliary info \mathsf{aux}_W

Then, as a stateless verifier:

1. I know d_{n-1} is valid (either because I previously validated block n-1, or because I trust so).
2. I check all reads against d_{n-1} via the \pi_i's (or the aggregated \pi_R)
3. I check the transition from d_{n-1} to d_n is valid via the writes W (and possible the auxiliary information)

AFAICT, the stateless verifier can easily check that d_n has been updated correctly for all w\in W \cap R, since for those, you know exactly the index i of the polynomial p_i they are in and you can check the new polynomial commitment is computed correctly (especially if in Lagrange basis).

But for writes w\in W - R (i.e., writes for key-value pairs that have not been read by block n), the verifier has no clue which p_i to update. The auxiliary information could point him to the right p_i, but it could also be malicious. This means for each such w, say with key k and value v, the auxiliary information needs to have non-membership proofs w.r.t. d_{n-1} for k not being in all other p_j, j\ne i (as described in my earlier comment).

Is my understanding correct?

Also, who in the Ethereum ecosystem would be responsible for computing and updating proofs as the data structure is updated?

---

**dankrad** (2020-04-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/alinush/48/10069_2.png) alinush:

> This means for each such ww , say with key kk and value vv , the auxiliary information needs to have non-membership proofs w.r.t. dn−1d_{n-1} for kk not being in all other pj,j≠ip_j, j\ne i (as described in my earlier comment).
>
>
> Is my understanding correct?

Yes.

![](https://ethresear.ch/user_avatar/ethresear.ch/alinush/48/10069_2.png) alinush:

> Also, who in the Ethereum ecosystem would be responsible for computing and updating proofs as the data structure is updated?

This is a good question. It would likely be a “state provider” role that needs to be established. The state provider could be queried by individuals when making transactions and will give them the witnesses. Using the multireveal scheme in [Hashmap-based polynomial commitments for state](https://ethresear.ch/t/hashmap-based-polynomial-commitments-for-state/7186/1) would allow constructing the multireveal from the individual proofs.

Another possibility would be to require block proposers to hold state, so that they are able to construct proofs. This avoids problems with constantly updating witnesses.

---

**alinush** (2020-04-08):

Thank you Dankrad! I hope it is relevant to clarify here (below your post) the setting in which these polycommit-based authenticated data structures need to operate in. If not, we can move this conversation somewhere else.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> This is a good question. It would likely be a “state provide” role that needs to be established. The state provide could be queried by individuals when making transactions and will give them the witnesses.

This should work for simple transactions that just transfer ETH from A to B, but what about transactions that trigger smart contract (SC) executions?

Seems like the *user* making the transaction must know the “reads” of the SC in order to ask the *state provider* for proofs. This implies the user must execute the contract locally himself to get those “reads”, which might defeat the point of Ethereum to some extent.

I presume what happens instead is the user sends the transaction without the reads to a *block proposer* who is either stateful or can contact the state provider to get state and proofs. However, since I assume block proposers should be fast (e.g., non-interactive), it might be too slow to have to ask state providers over the network for state + proofs, no?

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Using the multireveal scheme in Hashmap-based polynomial commitments for state would allow constructing the multireveal from the individual proofs.

Right, but this takes O(n\log{n}) time to compute “on the fly,” given a set of m evaluation points for a polynomial \phi(X) of degree-bound n.

I assume you’d want instead to aggregate multiple, **precomputed** constant-sized proofs on \phi(X) into a constant-sized multi-reveal proof, as [Vitalik proposed](https://ethresear.ch/t/using-polynomial-commitments-to-replace-state-roots/7095).

You can use aggregation to lower bandwidth for the writes w\in W-R mentioned before. e.g., given two writes w_1 and w_2 you can aggregate their proofs on p_i. You still need as many proofs as the # of polynomials, I think. But this is better than |W|\times number of polynomials. There’s still an overhead for sending the evaluations of the polynomials (e.g., 0 or \mathsf{hash}(k',v')), I think.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Another possibility would be to require block proposers to hold state, so that they are able to construct proofs. This avoids problems with constantly updating witnesses.

But this is not ideal for sharding, where nodes switch to different shards and would need to re-download that shard’s state before being able to propose?

---

**dankrad** (2020-04-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/alinush/48/10069_2.png) alinush:

> Seems like the user making the transaction must know the “reads” of the SC in order to ask the state provider for proofs. This implies the user must execute the contract locally himself to get those “reads”, which might defeat the point of Ethereum to some extent.

There is a substantial discussion around this problem at the moment on DSA (dynamic state access) vs. SSA (static or predictable state access) (see here: [A Short History and a Way Forward for Phase 2](https://ethresear.ch/t/a-short-history-and-a-way-forward-for-phase-2/6982)). In the SSA paradigm, it would actually be completely predictable which storage locations need to be read, and therefore it would be possible that the user only needs one query to get all the data as well as proofs. In the DSA world, that would become a bit more complex. However, it turns out that the SSA world is probably universal and all contracts can be mapped into it. So we probably aren’t losing that much.

![](https://ethresear.ch/user_avatar/ethresear.ch/alinush/48/10069_2.png) alinush:

> Right, but this takes O(nlogn)O(n\log{n}) time to compute “on the fly,” given a set of mm evaluation points for a polynomial ϕ(X)\phi(X) of degree-bound nn .
>
>
> I assume you’d want instead to aggregate multiple, precomputed constant-sized proofs on ϕ(X)\phi(X) into a constant-sized multi-reveal proof, as Vitalik proposed.
>
>
> You can use aggregation to lower bandwidth for the writes w∈W−Rw\in W-R mentioned before. e.g., given two writes w1w_1 and w2w_2 you can aggregate their proofs on pip_i . You still need as many proofs as the # of polynomials, I think. But this is better than |W|×|W|\times number of polynomials. There’s still an overhead for sending the evaluations of the polynomials (e.g., 0 or hash(k′,v′)\mathsf{hash}(k’,v’) ), I think.

I am a bit confused on what your point is here. The idea would be that at any given block height, one state provider computes the proofs for *all* storage locations (this can be done in O(n \log n) group operations using this scheme: [GitHub - khovratovich/Kate](https://github.com/khovratovich/Kate)). Then any user can query the locations relevant for their transactions and get the data+proofs from the state provider.

![](https://ethresear.ch/user_avatar/ethresear.ch/alinush/48/10069_2.png) alinush:

> But this is not ideal for sharding, where nodes switch to different shards and would need to re-download that shard’s state before being able to propose?

It is important that *attesters* can quickly switch between shards for security and load reasons. The same isn’t necessarily true for proposers: It would be ok to select a small number of proposers who stay on one shard for a long time, e.g. one day. This does not compromise security.

---

**rawfalafel** (2020-05-04):

I tried my hand at prototyping a generic hashmap here: https://github.com/rawfalafel/layered-poly-commit

I think this layering idea is clever! From an engineering perspective, there’s a lot of opportunities for concurrency since the objects are stored in distinct layers. But as n approaches 2^30, the time to generate witnesses is still high. I’d be interested in finding a path that’ll bring down the time to something that’s reasonable.

