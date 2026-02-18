---
source: ethresearch
topic_id: 4485
title: RSA Hash accumulator for arbitrary values
author: denett
date: "2018-12-05"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/rsa-hash-accumulator-for-arbitrary-values/4485
views: 5687
likes: 14
posts_count: 21
---

# RSA Hash accumulator for arbitrary values

RSA accumulators can efficiently store primes, but are (as far as I know) not efficient with non-prime numbers. My goal is to store arbitrary values, just like you can do in a Merkle tree, but having a shorter proof size. This can have multiple applications, such as in zk-starks, Plasma, etc.

I believe it is possible that we can proof that multiple values are contained in the accumulator with a single 2048 bit witness.

---

**Basic example for three values**

Let a, b and c be the values we like to store.

Let \textit{h} be a secure hash function.

Let N be a 2048 bit RSA modulus with unknown factorization and g be the generator.

Let p, q and r be three distinct large primes.

The accumulator A = g^{qr \textit{h}(a)+pr \textit{h}(b)+pq \textit{h}(c)} \mod N

To proof that a is stored in the first spot we need a witness W = g^{r \textit{h}(b)+q \textit{h}(c)} \mod N

The verifier has to check that g^{qr \textit{h}(a)}W^{p} \equiv A\mod N

To proof a fake value a' is in the accumulator, the forger needs to calculate the p-root of g^{qr (\textit{h}(a)-\textit{h}(a'))+pr \textit{h}(b)+pq \textit{h}(c)}\mod N. I believe this problem to be computationally infeasible when the RSA trapdoor is unknown.

It is also possible to make a single proof that the accumulator contains multiple values. For example when we want to proof a and b are both stored in the accumulator, we need the witness W = g^{\textit{h}(c)} \mod N

The verifier has to check that g^{qr \textit{h}(a)+pr \textit{h}(b)}W^{pq} \equiv A\mod N

---

**Hash accumulator with n primes**

We can generalize this to an accumulator for n values using n primes.

Let x_{1},..,x_{n} be the n values we like to store.

Let p_{1},..,p_{n} be n distinct large primes.

We define P_S to be g to the power of the product of all the primes not contained in the set S modulo N

P_S =  g^{\prod\limits_{\substack{k=1,k\not\in S}}^n p_{k}} \mod N

The accumulator A = \prod\limits_{k=1}^n P_{k}^{\textit{h}(x_k)} \mod N

To proof x_i is stored in spot i we need a witness W = \prod\limits_{k=1, k\neq i} ^n P_{i,k}^{\textit{h}(x_k)} \mod N

The verifier has to check that P_i^{\textit{h}(x_i)} W^{p_i} \equiv A \mod N

To proof that multiple values from set B are in the accumulator we need a single witness W = \prod\limits_{k=1, k\not\in B} ^n P_{B,k}^{\textit{h}(x_k)} \mod N

And the verifier has to check that \prod\limits_{k\in B}  P_{k}^{\textit{h}(x_k)}  W^{\prod\limits_{k\in B}p_k}  \equiv A \mod N

## Replies

**vbuterin** (2018-12-06):

Doesn’t this require quadratic overhead? If so, that’s a non-starter for most applications where prover time is already a bottleneck…

---

**Mikerah** (2018-12-06):

Since RSA accumulators can efficiently store primes, couldn’t you use this fact to efficiently store prime factorizations of non-prime numbers? Obviously, you would need a way to check the prime factorization and depending on the size of the number, this could have a lot of overhead.

---

**Silur** (2018-12-06):

why don’t just use a more advanced form of accumulator like the ajtai hash?

Randomly sample A from \mathbb{Z_p}^{n \times m} then do Ax\, mod\, p.

This is not only quasy-commutative but also quantumsafe, parallelizable and accumulations are trivially revocable by accumulating the inverse element.

Note that parameter selection for n and m are sensitive and limits your input size and security

---

**denett** (2018-12-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Doesn’t this require quadratic overhead?

You can build a witness in O(n) time.

Pseudo code:

```auto
function calculateWitness(pos,values) {
   var W=1;
   var P=g;
   for (var i=0;i<values.length;i++) {
      if (pos!=i) {
      	 W=(W^primes[i])%N;
      	 W=W*(P^hash(values[i]))%N;
         P=(P^primes[i])%N;
      }
   }
   return W;
}
```

---

**gakonst** (2018-12-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/silur/48/199_2.png) Silur:

> why don’t just use a more advanced form of accumulator like the ajtai hash?

Could you perhaps elaborate on how using the Ajtai hash would help in this case?

---

**ldct** (2018-12-07):

I have a similar question to [@gakonst](/u/gakonst) - the RSA accumulator scheme is defined using a function f : \mathbb{Z}_N \times \mathbb{N} \to \mathbb{Z}_N given by f(a, x) = a^x \pmod N; then the quasi-commutativity [1] property is f(f(a, x_1), x_2) = f(f(a, x_2), x_1).

From what I can find online [2] the Ajtai hash function is defined by g: \{0, 1\}^m \to \mathbb{Z}_q^n given by g(x) = A x \pmod p. What’s the quasi-commutativity property for g?

References

[1] https://eprint.iacr.org/2015/087.pdf

[2] https://www.math.u-bordeaux.fr/~ybilu/algant/documents/theses/BERGAMI.pdf

---

**denett** (2018-12-08):

A burden for the verifier is that it needs to store all the primes and all P_k constants, to verify the proof.

For a light verifier, we can save on storage space, when the prover supplies both P_k and p_k. The verifier can check P_k^{p_k} \equiv P_{\emptyset} \mod N, where  P_{\emptyset} = g^{\prod\limits_{k=0}^n p_{k}}. This way the light verifier only has to store P_{\emptyset}.

For a bulk proof the prover can provide P_B and all primes corresponding the the set B. The verifier can check the correctness of P_B, by checking P_B^{\prod\limits_{k\in B} p_{k}} \equiv P_{\emptyset} \mod N and calculate all needed P_k.

The disadvantage of this trick is that the verifier can only know that a value x is one of the n values in the accumulator, but not the specific spot.

For applications that do not need the specific spot, this light verifier trick can be used.

I was wondering whether zk-starks proofs (for which we can shrink the proof a lot by having a smaller merkle tree replacement) actually need the spot, or that putting the spot in the hashed data is sufficient. From what I understand of zk-stark proofs, it would not weaken the proof as long as the number of values in the accumulator is limited to n. A forger could try to put multiple values in the same spot to increase the chance to be able to give the correct answer for that spot. But now the forger increases the chance of not being able to answer when an empty spot is chosen.

---

**denett** (2018-12-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/mikerah/48/1616_2.png) Mikerah:

> Since RSA accumulators can efficiently store primes, couldn’t you use this fact to efficiently store prime factorizations of non-prime numbers?

Yes, I have thought of that, but it would require more primes and a larger proof.

To store a 256 bit hash value we could use 256 primes each representing one bit. Now we have to proof inclusion for on average 128 primes and exclusion for the other 128 primes. We can efficiently combine the inclusion proofs, but not the exclusion proofs, because we have a remainder the size of the product of 128 primes. For primes of 64 bit size, this results in a witness size of 2*2048 +128*64 =12288 bits.

A trick we could do is, instead of having one bit per prime, we could have 8 bits per prime, by including p^b where b is a byte. We have to prove p^b is included, but b^{n+1} is not.

Now we need only 32 primes for which we do 32 inclusion and 32 exclusion proofs. The witness size is now down to 2*2048 +32*64 =6144 bits for one value. For an extra value we need an extra 32*64=2048 bits, because we have a bigger remainder.

Unfortunately we cannot overstretch this trick, because calculating g^{p^{x}} \mod N is not trivial for large x.

My proposal is based on one inclusion proof, so is only 2048 bits for an unlimited number of values.

---

**Silur** (2018-12-10):

let X = {x_1, x_2, .... x_n}  arbitrary values. then your accumulator is \Sigma_{i=1}^{n}Ax_i \,(mod \,p). Witness is trivial, same as with RSA and revocation is just acc + x_i^{-1} where the inverse is by mod \, p

Security of the scheme is proven to be equivalent to solving the Shortest Integer Solution problem on ideal lattices.

references:


      [eprint.iacr.org](https://eprint.iacr.org/2014/1015.pdf)


    https://eprint.iacr.org/2014/1015.pdf

###

404.35 KB








http://elaineshi.com/docs/streaming.pdf

---

**Silur** (2018-12-10):

"ldct:

> What’s the quasi-commutativity property for g?

look up the properties of vector spaces ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**nginnever** (2018-12-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> We can efficiently combine the inclusion proofs, but not the exclusion proofs

Assume a plasma cash/flow design application. I wonder if it would be possible to have the operator commit to two accumulator values A_i and A_e where including a prime in A_i represents committing to the inclusion of a value i.e. a bit is 1 not a 0. And then A_e represents committing to exclusion of a value i.e. a bit is 0 not 1 at a given position i in vector x.

In plasma cash we might want a sparse vector that stores only the public key of the owner of the coin at a particular index. Assume a public key is only 8 bits i.e if we have two values v_1 = [01101110] and v_2 = [10100111] we could generate the two VC accumulators A_i and A_e like so.

Let v_1^p = [3,5,7,11,13,17,19,23]

Let v_2^p = [29,31,37,41,43,47,53, 59]

Let A_i = g^{[{3^0}*{5^1}*{7^1}*{11^0}*{13^1}*{17^1}*{19^1}*{23^0}]*[{29^1}*{31^0}*{37^1}*{41^0}*{43^0}*{47^1}*{53^1}*59^1]}

Let A_e = g^{[{3^1}*{5^0}*{7^0}*{11^1}*{13^0}*{17^0}*{19^0}*{23^1}]*[{29^0}*{31^1}*{37^0}*{41^1}*{43^1}*{47^0}*{53^0}*59^0]}

To prove that x_1 opens to v_1 we would ask for a batched inclusion proof for 5,7,13,17,19 to prove that x_1 position contains all of the correct bits with 1. To prove x_1 has all of the correct 0 bits committed we would ask for a batched inclusion proof for 3,11,23 which should result in just two times the batched proof size of one accumulator.

err… Not explicitly proving exclusion could mean that multiple values are stored in the same position since the operator could include more primes than the verifier is checking which will allow other values to pass. This makes me wonder if we could create a compact proof that A_i and A_e are disjoint if this would work.

---

**denett** (2018-12-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/nginnever/48/1936_2.png) nginnever:

> This makes me wonder if we could create a compact proof that A_i and A_e are disjoint

If the prover and verifier agree on which primes are used, the prover can show that A_i and A_e are constructed correctly.

Let x be the product of all included primes.

Let y be the product of all excluded primes.

Let z be the product of all primes.

Let A_i = g^x \mod N

Let A_e = g^y \mod N

Let A_T = g^{z} \mod N

A_T is the accumulator containing all primes. This value can be pre-calculated and stored on chain.

Now I want to use a double Wesolowski proof, to show that x*y=z.

We are substituting:

x = B\lfloor \frac x B \rfloor + x \mod B

We use the following witnesses:

b_1=g^{\lfloor \frac x B \rfloor} \mod N

b_2=A_e^{\lfloor \frac x B \rfloor} \mod N

r=x \mod B

The verifier should check:

b_1^B.g^r \equiv A_i \mod N

b_2^B.A_e^r \equiv A_T \mod N

---

**denett** (2018-12-19):

We can adjust the RSA Hash Accumulator to store a matrix of values. This way we can store more values using less primes.

The idea behind the accumulator is that every hashed value is multiplied with every prime except one. To proof a value is in the accumulator we can group all other values together, because they are all multiplied by the same prime that is missing from the value we like to proof.

To store a matrix instead of a vector, we will multiply all hashed values with every prime except two, this way we can store n*m values using only n+m primes. The downside of this approach is that we need two 2048 bit witnesses to proof inclusion of one value.

---

**Hash accumulator for a mxn matrix**

Let x_{i,j} be the values of the matrix we like to store.

Let p_{1},..,p_{n} and q_{1},..,q_{m} be the n+m distinct large primes.

We define P_S and Q_S to be the product of all their respective primes not contained in the set S (*not g raised to the power as above*)

P_S =  \prod\limits_{\substack{k=1,k\not\in S}}^n p_{k}

Q_S =  \prod\limits_{\substack{k=1,k\not\in S}}^m q_{k}

The accumulator A = g^{\sum\limits_{k=1}^m \sum\limits_{l=1}^n Q_{k}P_{l}\textit{h}(x_{k,l})} \mod N

To proof x_{i,j} is stored in spot i,j, we need two witnesses:

W_p = g^{\sum\limits_{l=1,l \neq j}^n Q_{i}P_{l,j}\textit{h}(x_{i,l})} \mod N

W_q = g^{\sum\limits_{k=1,k\neq i}^m \sum\limits_{l=1}^n Q_{k,i}P_{l}\textit{h}(x_{k,l})} \mod N

The verifier has to check: g^{Q_iP_j{\textit{h}(x_{i,j})}} W_q^{q_i}W_p^{p_j} \equiv A \mod N

If we select a set of columns and a set of rows we can proof in a similar manner, all values that are both in the row set as in the column set, using just two 2048 bit witnesses.

If we like, this can be extended to store n-dimensional matrices.

---

Edit: adding a small example to make it less abstract

**A small example for a 2x3 matrix**

We are using three p primes p_1, p_2 and p_3 for the columns and two q primes q_1 and q_2 for the rows.

We can store six values: x_{1,1}, x_{1,2}, x_{1,3}, x_{2,1}, x_{2,2}, x_{2,3}

The accumulator A=g^{q_2p_2p_3\textit{h}(x_{1,1}) + q_2p_1p_3\textit{h}(x_{1,2}) + q_2p_1p_2\textit{h}(x_{1,3}) + q_1p_2p_3\textit{h}(x_{2,1}) + q_1p_1p_3\textit{h}(x_{2,2}) + q_1p_1p_2\textit{h}(x_{2,3})}

To proof x_{2,2} is in the accumulator we need witnesses:

W_p = g^{q_1p_3\textit{h}(x_{2,1}) + q_1p_1\textit{h}(x_{2,3})}

W_q = g^{p_2p_3\textit{h}(x_{1,1}) + p_1p_3\textit{h}(x_{1,2}) + p_1p_2\textit{h}(x_{1,3})}

The verifier has to check: g^{q_1p_1p_3\textit{h}(x_{2,2})}W_q^{q_2}W_p^{p_2} \equiv A \mod N

---

**denett** (2018-12-20):

We can also build a hash accumulator using only two primes to store an arbitrary number of values.

To do this we will multiply the hashed values with both a power of prime p and a power of prime q. This is done is such a way that all other values will be multiplied by either a higher power of p or a higher power of  q. This way all other values can be separated via the p side or the q side.

We can proof the values on the tail or head with just one 2048 bit witness and any range in the middle with two 2048 bit witnesses.

---

**Hash accumulator using two primes**

Let x_1,..,x_n be the values we like to store.

Let p and q be two distinct large primes.

The accumulator A = g^{\sum\limits_{k=1}^n p^kq^{n-k}\textit{h}(x_{k})} \mod N

To proof x_i is stored in spot i, we need two witnesses:

W_q = g^{\sum\limits_{k=1}^{i-1} p^kq^{i-k-1}\textit{h}(x_{k})} \mod N

W_p = g^{\sum\limits_{k=i+1}^{n} p^{k-i-1}q^{n-k}\textit{h}(x_{k})} \mod N

The verifier has to check:

g^{p^iq^{n-i}{\textit{h}(x_{i})}} W_p^{p^{i+1}}W_q^{q^{n-i+1}} \equiv A \mod N

In a similar manner we can proof inclusion of a range of values using two 2048 bit witnesses.

---

**gakonst** (2018-12-30):

Just trying to go along with your math, I think the notation might be a little mistaken in some places (given that P_S and Q_S are scalars)? Please correct me if I’m wrong.

 A = g^{\sum\limits_{k=1}^m \sum\limits_{l=1}^n Q_{k}P_{l}\textit{h}(x_{k,l})} \mod N

should be  A = g^{\sum\limits_{k=1}^m \sum\limits_{l=1}^n q_{k}p_{l}\textit{h}(x_{k,l})} \mod N  ?

Also in the witnesses,

 W_p = g^{\sum\limits_{l=1,l \neq j}^n Q_{i}P_{l,j}\textit{h}(x_{i,l})} \mod N

you iterate over j in [1,n] excluding l, but j in x_{ij} is in [1,m].

This seems like a neat idea, along with your post where you consider MxN to be CoinIdxBlock, but could you please revisit this post, so that you check for any mistakes and perhaps provide an example with smth simple like a simple 2x3 array?

---

**gakonst** (2018-12-30):

Unfortunately the cited Latice-based accumulator paper does not propose a scheme for universal accumulators ie non-membership proofs, which is one of the biggest challenges in compressing UTXO history in Plasma.

---

**denett** (2018-12-30):

You are correct, P_S and Q_S are scalars. The subscript is a set of indices that should be excluded, so I understand it might be confusing. I don’t know if there is a better notation for that. I chose capital P and Q, because they are the products of respectively the p and q primes.

Without P and Q we can write the accumulator as:

A = g^{\sum\limits_{k=1}^m \sum\limits_{l=1}^n (\prod\limits_{\substack{t=1,t\neq k}}^m q_{t} ) (\prod\limits_{\substack{t=1,t\neq l}}^n p_{t})\textit{h}(x_{k,l})} \mod N

So \textit{h}(x_{k,l}) is multiplied by every p and q prime except p_l and q_k.

For witness W_p = g^{\sum\limits_{l=1,l \neq j}^n Q_{i}P_{l,j}\textit{h}(x_{i,l})} \mod N we are only using values of row i. We are iterating over all columns l in [1,n] except j. Every hashed value \textit{h}(x_{i,l}) is multiplied by every q prime except q_i, and multiplied by every p prime except p_l and p_j.

p.s. I have edited the post to include a 2x3 matrix example.

---

**kilan2018** (2019-01-03):

What  do you mean  by  qrh(a) …how can multiply by hash …h(a)

---

**denett** (2019-01-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/kilan2018/48/3121_2.png) kilan2018:

> What do you mean by qrh(a) …how can multiply by hash …h(a)

h(a) is the hash of value a, when using for example the keccak256 hash function the result is a 256 bit number.This number is multiplied by both q and r. These should be large prime numbers of similar size.

---

**denett** (2019-03-06):

So I have reinvented the wheel here. The original version of the Hash Accumulator is equivalent to Vector Commitment scheme as described  in paragraph 3.2 of the below paper from Catalano and Fiore.


      [eprint.iacr.org](https://eprint.iacr.org/2011/495.pdf)


    https://eprint.iacr.org/2011/495.pdf

###

474.15 KB








They describe a nice trick in paragraph 3.3 where the prime for an index is based on a random number generator. Per index they sample multiple random numbers, the first random number that is a prime, is the prime for the index. The verifier can do the same, so the verifier does not have to store all primes.

Downside is that the verifier has to check a lot of numbers for primality what could be burdensome. But we could combine this prime generation method with the trick described in this [post](https://ethresear.ch/t/rsa-hash-accumulator-for-arbitrary-values/4485/9) above. Now the verifier has to generate one random number and check whether the generated number is one of the pre-committed primes.

This way the verifier can efficiently verify that a prime corresponds with a given index without storing all the primes.

