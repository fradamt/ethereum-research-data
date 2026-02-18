---
source: magicians
topic_id: 10605
title: Off-loading bigint multiplication from zk-SNARK using Pedersen commitment
author: DanTehrani
date: "2022-08-31"
category: Magicians
tags: [zkp, cryptography]
url: https://ethereum-magicians.org/t/off-loading-bigint-multiplication-from-zk-snark-using-pedersen-commitment/10605
views: 1024
likes: 2
posts_count: 2
---

# Off-loading bigint multiplication from zk-SNARK using Pedersen commitment

**Edit**:

**Please do not sped too much time trying to understand this. I haven’t done any benchmarks yet, and even this method leads to performance improvements, no drastic gains should be anticipated.**

### Background

- I’m working on a scheme that could “off-load” some computation from some zk-SNARK circuits. That is,

1. we do some computation publically without revealing the private values using partially homomorphic schemes (PHS).
2. we verify that the values used in computation actually originate from the private values using zk-SNARK.

Moreover, we will use PHS with elliptic curves so we can efficiently run verification inside a zk-SNARK.

### Epistemic status

- I’m hoping to determine if there are any obvious flaws in the scheme I describe in this post.
- I haven’t implemented the schcme yet; I wish to procede to implementation after I get feedback from the community.
- I haven’t done any benchmarks. Therefore it might be the case that even though it seems like this leads to off-loading some computation from a zk-SNARK circuit, such hypothesis might be disproved after proper implementation.
- I believe that this stack exchange post discusses a similar theme, but I couldn’t find further information regarding such an idea.

### Off-loading bigint multiplication

We are assuming the following setup:

I will describe a way to *off-load* **integer multiplication**, more precisely **bigint multiplication that requires complicated operations**. By off-loading bigint multiplication, we could reduce the number of constraints of a zk-SNARK circuit.

For details about bigint operations in a zk-SNARK, please refer to [this blog post](https://0xparc.org/blog/zk-ecdsa-2) by 0xPARC.

Given two private `n`-bit integers `a, b` and a public integer `c`, we want to prove that `a * b = c`, without revealing `a, b`.

### Proving

First, we represent a in two vectors k and l

- k = (2^0, 2^1,..., 2^n-1)
- l = (l_0, l_1,...,l_n-1)

where `l_i` is either 0 or 1

Such that `k・ l = a`

(i.e. the dot product of `k` and `l` equals to `a`)

Then we can represent `a * b` as

- (2^0 * b, 2^1 * b, ... , 2^n-1 * b) ・l
-> 2^0 * b * l_0 + 2^1 * b * l_1, ... , 2^n-1 * b * l_n-1

Now, we commit each item of the vector `(2^0 * b, 2^1 * b, ... , 2^n-1 * b)` using Pedersen commitment with secret `r` and get the vector `j`.

- j = (com(2^0 * b, r), com(2^1 * b, r), ... ,com(2^n-1 * b, r))

It is important to note that the Pedersen commitment we use here operates on 254bits. (e.g. [Baby Jubjub Elliptic Curve](https://eips.ethereum.org/EIPS/eip-2494)) Another thing to keep in mind is that, the values to be committed originates from 256bit operations, so in order to commit them using a 254bit curve, **we need to split them into two 128bit chunks first**. We can do point additions to committed chunks, with a carry `com(1, r)` if necessary.

### Verification

Since Pedersen commitments are additively homomorphic, if the values in `j` were properly committed we can get the following equality.

- (j_0, j_1,...,j_n-1)・l = com(c, r)

Another necessary step will be: checking that the commitments in `j` are not just some random values that sum up to `com(c, r)`. We need to check the linearity of the commitments. This can be done by checking

- j_i + j_i = j_i+1 -> com(2^i * b, r) + com(2^i * b, r) = com(2^i+1 * b, r)

for all  `0 <= i < n - 1`

Lastly, using zk-SNARK, we will check that all values in `j` are committed correctly. This can be done by **only checking the first commitment** is correct, since we have already checked the linearity of the values.

Existing similar ideas, critical flaws, any kind of feedback will be welcome!

## Replies

**llllvvuu** (2022-09-02):

Would recommend moving this to [ethresear.ch](https://ethresear.ch/)!

