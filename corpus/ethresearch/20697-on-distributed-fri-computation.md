---
source: ethresearch
topic_id: 20697
title: On Distributed FRI Computation
author: curb-dancer
date: "2024-10-18"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/on-distributed-fri-computation/20697
views: 329
likes: 8
posts_count: 1
---

# On Distributed FRI Computation

In this note we discuss the distributed computation of the FRI protocol. In practice, we often need to distribute the prover’s work across many servers. In the case of using a FRI-based proof system, this leads to the expensive recursive aggregation of the obtained proofs or exchanging data, the size of which is comparable to the size of the circuit. Below, we describe a technical trick that allows us to optimize obtaining a single final proof.

### Batched FRI

The **batched** version of the \mathtt{FRI} protocol allows one to estimate the closeness of each of the functions f_1, \dots, f_L to the \mathsf{RS} code. To do this, the \mathtt{Verifier} samples and sends a random \theta \in \mathbb{F}_p to the \mathtt{Prover}. The latter calculates a linear combination

F = \theta^1 \cdot f_1 + \theta^2 \cdot f_2 + \dots + \theta^L \cdot f_L

Then the \mathtt{Prover} and \mathtt{Verifier} execute the regular version of the \mathtt{FRI} protocol for testing F. The only difference is that each time F is queried at point x, the \mathtt{Verifier} also performs a consistency check:

F(x) = \theta^1 \cdot f_1(x) + \theta^2 \cdot f_2(x) + \dots + \theta^L \cdot f_L(x).

If the \mathtt{Verifier} accepted in the end of the protocol, then all f_i are close to \mathsf{RS}.

### Distributed FRI

Let us now consider a distributed setting in which n=L \cdot M polynomials of degree at most d are divided among M \mathtt{Provers}. The output of the protocol should be a proof that all the polynomials f_1, \dots, f_n are close enough to the \mathsf{RS} code. A naive approach would be to send all polynomials in plaintext to one of the provers, who in turn would execute the batched \mathtt{FRI} protocol. Let us consider how this problem can be solved more efficiently.

\mathtt{Provers} generate \mathsf{Merkle~ Tree} commitments to their polynomials and send them to the \mathtt{Master~Prover} (this function can be performed by one of the provers, for simplicity we will assume that this is a separate entity). The \mathtt{Master~Prover} gets a random challenge \theta from the \mathtt{Verifier} and broadcasts it among all \mathtt{Provers}. Now each \mathtt{Prover} P_i, knowing its number i, can generate its “part of the linear combination” and send it to the \mathtt{Master~Prover}.

F_i = \sum_{j=1}^{L}\theta^{(i-1) \cdot L + j}f_{(i-1) \cdot L + j}.

\mathtt{Master~Prover} runs a regular version of \mathtt{FRI} for the polynomial \sum_{i=1}^{M}F_i. However, it cannot provide polynomial evaluations and Merkle auth paths for  consistency checks in the query phase of the protocol for individual polynomials, so it asks the corresponding \mathtt{Prover} for each of them.

\mathtt{Master~prover} can easily detect malicious behavior of individual \mathtt{Provers}. This is achieved due to the fact that the partial linear combinations F_i belong to \mathsf{RS} code. This property is especially useful in a distributed SNARK generation process, as it allows for the implementation of economic measures to penalize participants for misbehaving.

It is easy to see that the time complexity of the \mathtt{Provers} is O(d\log d). The communication cost (this is communication between provers and master prover) is dominated by sending a partial linear combination, whose size is O(d) elements from \mathbb{F}_p. Moreover, the number of hash invocations required to verify the final proof is significantly less than that needed to verify M independent proofs.

You can find a more detailed description [here](https://hackmd.io/@nil-research/rJ_NVyiRA). Feel free to share your comments!
