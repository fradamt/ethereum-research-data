---
source: ethresearch
topic_id: 6545
title: Using HoneyBadgerMPC for the multi-party Proof-of-Custody
author: amitgtx
date: "2019-12-01"
category: Cryptography > Multiparty Computation
tags: []
url: https://ethresear.ch/t/using-honeybadgermpc-for-the-multi-party-proof-of-custody/6545
views: 3852
likes: 8
posts_count: 3
---

# Using HoneyBadgerMPC for the multi-party Proof-of-Custody

## Background

This blog post describes our implementation of legendre PRF based “Proof of Custody” using [HoneyBadgerMPC](https://github.com/initc3/HoneyBadgerMPC) framework. The link to the codebase along with the instructions can be found [here](https://github.com/amitgtx/HoneyBadgerMPC/tree/legendreprf/apps/legendrePoC). In short, Proof of Custody is a way for nodes (called validators) to “prove” that they are really storing a file which they are obligated to store. Prior realizations of this scheme utilized a “mix” function based on SHA256. A future goal is to make use of primitives which allow: i)validator pools to be set up in a secure, trustless manner, (ii) allow one-party validators to spread their secret across several machines, reducing the risk of secrets getting compromised. In order to meet this goal, it is required that the primitive is MPC-friendly which, unfortunately, is not a property of SHA256. Fortunately, the “mix” function in the Proof of Custody scheme can be replaced with any PRF. Consequently, it was proposed that Legendre PRF, an MPC-friendly primitive, would be a good candidate for such replacement. See this post ([Using the Legendre symbol as a PRF for the Proof of Custody](https://ethresear.ch/t/using-the-legendre-symbol-as-a-prf-for-the-proof-of-custody/5169)) for a detailed backgound.

## Setting

There are n nodes out of which t might be malicious. Additionaly, there is a secret-key K which is secret-shared among the n nodes using a (t, n) threshold secret-sharing scheme. This means that atleast a group of t+1 nodes are required in-order to reconstruct the secret-key K. In order to “prove the custody” of a file represented as a set of B blocks - {X_1, X_2, .... X_B} - which is basically a public dataset of B field elements, the nodes compute the output of legendre PRF function using their secret key share [K] and the B field elements as input. This output is represented in the following equation:

F_{[k]}(X) = legendre_p(([K]+X_1) * ([K]+X_2) * ([K]+X_3)  .... ([K]+X_B))

where

legendre_p (a) = a^{\frac{p-1}{2}} (mod\;p)

Once each node has computed its share of the output, those outputs can be combined to reconstruct the actual output. In a setting where n > 3t, we can use a technique called robust interpolation for such reconstruction. This technique ensures that: i) reconstructed output always matches with the expected output, ii) nodes which did not submit or submitted incorrect shares of their PRF output are always identified. This identification of malicious behaviour (coupled with a scheme which provides rewards to nodes who submit correct output shares) incentivizes the nodes to perform the MPC computation honestly.

## Protocol

Below, we outline the protocol that each node follows:

Precompute:

- [K],[K^2],...[K^B] : powers of secret-share of key for each block

Online computation:

- Compute [y] where y = (K+X_1)(K+X_2)....(K+X_B) through local computations. This is a polynomial y = f(K) where the coefficients of f can be determined from constants X_1,...,X_B and we have powers of [K] precomputed
- Compute [F_K(X)] := [y]^{(p-1)/2} through log_2 p multiply/squarings
- Open [F_K(X)] and reconstruct to obtain F_K(X)

## Implementation

We have implemented the above scheme using [HoneyBadgerMPC](https://github.com/initc3/HoneyBadgerMPC) framework. HoneyBadgerMPC is unique in that it focuses on robustness. In a network of  n  server nodes, assuming at most  t<n/3  are compromised, then HoneyBadgerMPC provides confidentiality, integrity, and availability guarantees. In MPC terminology, it is asynchronous, provides active security, has linear communication overhead, and guarantees output delivery. Other MPC toolkits, such as SCALE-MAMBA, Viff, EMP, SPDZ, and others, do not provide guaranteed output delivery, and so if even a single node crashes they stop providing output at all.The link to the codebase along with the instructions can be found [here](https://github.com/amitgtx/HoneyBadgerMPC/tree/legendreprf/apps/legendrePoC). In our code, the above protocol is implemented inside the `prog()` in 2 different phases:

- Offline Phase : In this phase, each node obtains a (t,n) secret-sharing of key K, and then each node computes successive powers of their secret share ([K], [K^2], [K^3], etc) using the offline_powers_generation() function
- Online Phase : In this phase, nodes run a MPC protocol using the public file (represented as an array X of B elements) and the preprocessed powers of secret shared key as input. The logic for same is present in the eval() function. The output of this function is a secret-sharing fk_x of the desired output. After this, each node reconstructs the desired output FK_x using the open() function.

## Difference between our implementation and a real-world deployment

Our implementation differs from a real-world deployment in the following ways:

1.) The nodes in our implementation are “simulated” as async tasks which execute concurrently on the same system and communicate with each other using message passing. However, in the real-world, each node would correspond to a validator (a standalone system) and the communication would happen over network sockets.

2.) In our implementation, nodes obtain a share of the predetermined secret-key K which is computed by the HoneyBadgerMPC system. In the real world, the “one-party validator” node will be holding the secret-key K and will be responsible for distributing shares of it to each of the n nodes in the “validator pool”

## Acknowledgements

As already mentioned, our implementation makes use of HoneyBadgerMPC framework which has been developed under the supervision of [Andrew Miller](http://soc1024.ece.illinois.edu/) and others. I am a first year PhD student working under Andrew Miller at [Decentralized Systems Lab](https://decentralize.ece.illinois.edu/), UIUC. You can find out more about me [here](https://amitagarwal.gitbook.io/)

## Replies

**dankrad** (2019-12-02):

Nice! This is amazing, would you be able to post some statistics on this? Especially the total computation complexity would interest me!

Note that the construction had to change slightly as [@khovratovich](/u/khovratovich) found a bug in my first construction, see here: https://github.com/ethereum/eth2.0-specs/issues/1378

---

**amitgtx** (2019-12-16):

Hi Dankrad,

We have performed a theoretical and empirical analysis of the costs involved in our implementation of “Proof of Custody” scheme. While doing the complexity analysis, we realized that the part in online phase where we determine the coefficients of y = f(K) = (K + X_1)(K + X_2).....(K + X_B) takes O(B^2) time. Therefore, we have replaced the inefficient coefficient-generating algorithm with a new FFT based algorithm which can compute the coefficients in O(B \times log ^2 B) time. Below we outline the costs involved in our implementation:

**Offline phase**

- Computation cost:  O(n B \; log n + n \; log n \; log p)
Explanation: We require (B + 2 log p) precompute triples overall - B triples for computing all the B powers of secret-shared key K, and 2 log p triples for PRF evaluation. In addition to triple generation, we are performing B beaver multiplication for precomputing all B powers of secret-shared key. Each Beaver triple generation and beaver multiplication requires O(n log n) computation
- Communication cost : O(B + log p)
Explanation: Each triple generation and beaver multiplication require O(1) amortized communication cost. We are generating (B + 2 log p) triples and performing B beaver multiplications.

**Online phase**

- Computation cost : O (B \; log^2 B + n \;log n \; log p)
Explanation :  We perform B \; log^2 B local computations for computing the coefficients of polynomial y = f(K) + B local computations to evaluate the polynomial using pre-computed powers + 2 log p Beaver multiplications to compute the PRF on the result of polynomial evaluation. Each beaver multiplication requires O(n \; log n) computation
- Communication cost : O(log p)
Explanation : Beaver multiplications require communication, and we are performing maximum 2 log p such beaver multiplications for each PRF evaluation. The amortized communication cost of each multiplication is O(1)

We have also performed some empirical measurements by executing our code on different values of B (number of file blocks), for a fixed value of n (number of node) and t (number of corrupted nodes). Note that in all these experiments, all nodes were simulated on a single core. The offline cost itself did not include the cost of generating triples, so this estimate could be off by say 2x

[![Computation%20costs%20(in%20seconds)%20of%20offline_online%20phase%20as%20a%20function%20of%20B](https://ethresear.ch/uploads/default/original/2X/0/06b87b784922870e854842735b02ed158474441d.png)Computation%20costs%20(in%20seconds)%20of%20offline_online%20phase%20as%20a%20function%20of%20B629×388 15.9 KB](https://ethresear.ch/uploads/default/06b87b784922870e854842735b02ed158474441d)

