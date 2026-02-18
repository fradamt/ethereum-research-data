---
source: ethresearch
topic_id: 4055
title: Nothing-up-my-sleeve computations
author: jvanname
date: "2018-11-01"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/nothing-up-my-sleeve-computations/4055
views: 1468
likes: 0
posts_count: 4
---

# Nothing-up-my-sleeve computations

So [here](https://crypto.stackexchange.com/questions/58465/can-nothing-up-my-sleeve-computations-be-obtained-from-other-cryptosystems), I proposed the idea of a nothing-up-my-sleeve cryptosystem.

A nothing-up-my-sleeve computation essentially is a cryptographic algorithm that allows one to prove without any trusted setup that he has obtained some output f(x) of the function f without knowing anything about the input x other than its existence. These nothing-up-my-sleeve computations could be used to remove the need of a trusted setup in a zk-SNARK.

A nothing-up-my-sleeve computation generator is a function D produced without a trusted setup where for each circuit C and string x, there is some input c to the circuit C such that D(C)(x)=C(c) but where little to no information about c other than what can be deduced from C and C(c) can be obtained.

I do not have any idea about the mathematics needed to construct nothing-up-my-sleeve computations. I suspect the mathematics needed to construct these nothing-up-my-sleeve computations is beyond any mathematics that we have today since nothing-up-my-sleeve computations do not seem to be producible even with a cryptographic program obfuscator and since cryptographic program obfuscators (once mathematicians come up with some that are efficient enough to use in practice) could be used to easily construct nearly any kind of proposed cryptosystem.

Nevertheless, even though I suspect that nothing-up-my-sleeve computations are probably extremely difficult to produce in practice, this notion may be worthwhile to investigate since it only takes one instance of a nothing-up-my-sleeve computation in order to remove any worry about any ‘toxic waste’ produced in any cryptosystem such as zk-SNARKs requiring a trusted setup.

## Replies

**vbuterin** (2018-11-03):

This seems at first glance to be similar to homomorphic encryption. Specifically, D(C)(x) can be defined as “homomorphically compute C using x, which we expect to be a homomorphically encrypted version of some c, as an input, then decrypt it”.

However, we can easily show that you cannot make a generic D that is secure. Otherwise you can set C to the identity function C(n) = n and then D(C)(x) = C(c) = c so you can recover c from C and x, which violates your assumption. Homomorphic encryption fails because the decryption key that lets you dectypt the output also lets you decrypt the input.

---

**bharathrao** (2018-11-03):

If you want to address the toxic waste issue, you have the following options:

- Bulletproofs
- Zk-starks
- Zk-snarks without trusted setup

---

**jvanname** (2018-11-07):

In order to exclude the case where C computes the identity function or any other easily invertible function, I gave the exception for the case when c can be easily computed from C and C(c). The function D should satisfy the following security requirements:

1. (Conditional pre-image resistance) It will be no easier to find a c' with C(c')=D(C)(x) when one knows D,C,x than it will be if one only knows the output C(c) and the function D but not x. In particular, if C computes a cryptographic hash function or a function for a trusted setup, then one in general will not know the inputs for the cryptographic hash function nor the trusted setup.
2. Suppose that D,C are known. Suppose that P is an efficiently computable function that returns either 0 or 1. Then the problem of finding an input y such that P(D(C)(x),y)=1 should not be any easier if one knows the input x. Property 1 follows from property 2 when we define P(r,y)=1 precisely when C(y)=r.

I wonder if there is some sort of impossibility result for this sort of cryptosystem as there is with virtual black-box obfuscation.

