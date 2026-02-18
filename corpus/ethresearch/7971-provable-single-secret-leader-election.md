---
source: ethresearch
topic_id: 7971
title: Provable Single Secret Leader Election
author: mmaller
date: "2020-09-14"
category: zk-s[nt]arks
tags: [single-secret-leader-election]
url: https://ethresear.ch/t/provable-single-secret-leader-election/7971
views: 4787
likes: 20
posts_count: 2
---

# Provable Single Secret Leader Election

We suggest the use of an adaptation of the Bayer-Groth permutation argument [here](http://www0.cs.ucl.ac.uk/staff/J.Groth/MinimalShuffle.pdf) to obtain a secret single-leader election with low prover overhead. (Related post [here](https://ethresear.ch/t/low-overhead-secret-single-leader-election/5994).)

**Construction**

Let g be an elliptic curve generator. Let v_1, ...,v_k be a list of validators to secretly shuffle for block proposals. Every validator v_i has a permanent public key pk_i as part of their validator record where pk_i=g^{sk_i} for some secret key sk_i . To begin an ephemeral base is set to epk = g.

To shuffle a set of ciphertexts participate in the election a validator v broadcasts:

- a new ephemeral base epk' = epk^r
- shuffled public keys pk_1', ... , pk_k'
- a corresponding SNARK proof \pi with public inputs pk_1,...,pk_k, epk and private inputs (r, \sigma  ) such that pk_i'=pk_{\sigma(i)}^{r} and epk'=epk^r

A participant can identify their public key as the value pk_j' such that pk_j' = (epk')^{sk_i}.  If the shuffle is accepted, then the ephemeral base is updated to epk' = epk and the public keys are updated to (pk_1, ... , pk_k) = (pk_1', ... , pk_k').

To limit the damage of a dishonest shuffler, it will be necessary to commit to the shuffle \sigma in advance of knowing the current ordering of public keys.

**Motivation**

Justin Drake proposed a low overhead secret single leader election.  However, for security, his idea required the use of a private broadcast mechanism (e.g. Tor).  Recently Dan Boneh, Saba Eskandarian, Lucjan Hanzlik, and Nicola Greco proposed a means to remove the private broadcast mechanism by instead encrypting the shuffled ciphertexts [here](https://eprint.iacr.org/2020/025.pdf). In this proposal we specify a means to instantiate the zero-knowledge shuffle argument.

For more technical detail see [here](https://github.com/ethresearch/Shuffle_SSLE/blob/8b42397dcdb01e57bb5b804c896eab50430795a9/docs/shuffle_ssle.pdf)

## Replies

**JayWelsh** (2021-12-11):

How viable would it be to have this included with the initial release of the merge?

