---
source: magicians
topic_id: 3968
title: "EIP-2494: Baby Jubjub Elliptic Curve"
author: bellesmarta
date: "2020-01-29"
category: EIPs
tags: [zkp, eip-2494]
url: https://ethereum-magicians.org/t/eip-2494-baby-jubjub-elliptic-curve/3968
views: 4361
likes: 7
posts_count: 3
---

# EIP-2494: Baby Jubjub Elliptic Curve

This is the discussions-to thread for the [EIP-2494](https://github.com/ethereum/EIPs/pull/2494) proposing Baby Jubjub, a twisted Edwards elliptic curve that allows elliptic curve cryptography inside zk-SNARK circuits.

**Abstract**

Two of the main issues behind why blockchain technology is not broadly used by individuals and industry are scalability and privacy guarantees. With a set of cryptographic tools called zero-knowledge proofs (ZKP) it is possible to address both of these problems. More specifically, the most suitable protocols for blockchain are called zk-SNARKs (zero-knowledge Succint Non-interactive ARguments of Knowledge), as they are non-interactive, have succint proof size and sublinear verification time. These types of protocols allow proving generic computational statements that can be modelled with arithmetic circuits defined over a finite field (also called zk-SNARK circuits).

To verify a zk-SNARK proof, it is necessary to use an elliptic curve. In Ethereum, the curve is alt_bn128 (also referred as BN254), which has primer order `r` . With this curve, it is possible to generate and validate proofs of any `F_r` -arithmetic circuit. This EIP describes *Baby Jubjub* , an elliptic curve defined over the finite field `F_r` which can be used inside any zk-SNARK circuit, allowing for the implementation of cryptographic primitives that make use of elliptic curves, such as the Pedersen Hash or the Edwards Digital Signature Algorithm (EdDSA).

## Replies

**otto-mora** (2024-11-15):

Hello!  I would like “relive” the discussion around this EIP which is used for Digital Identity in the Iden3 open source protocol and which would greatly benefit the larger Ethereum ecosystem as a whole.  We have been using this for a few years now, and it efficiently produces zk proofs in both browsers and mobile devices. I think it is worth re-visiting this and evaluating it with the larger Eth community.

https://docs.iden3.io/getting-started/babyjubjub/



      [docs.iden3.io](https://docs.iden3.io/publications/pdfs/Baby-Jubjub.pdf)



    https://docs.iden3.io/publications/pdfs/Baby-Jubjub.pdf

###



256.98 KB










Appreciate if this could be evaluated for discussion and potential approval.

---

**rdubois-crypto** (2024-11-20):

Hi there !

Having Baby-jujub and jujub would be great. There is also Bandersnatch, palla, vesta.

In this regard RIP7696 would allow to use efficiently any of those, requiring a little wrapping for edwards curves (some linear computations),



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rdubois-crypto/48/6815_2.png)
    [RIP-7696 : generic Double Scalar Multiplication (DSM) for all curves](https://ethereum-magicians.org/t/rip-7696-generic-double-scalar-multiplication-dsm-for-all-curves/19798) [RIPs](/c/rips/58)



> This proposal creates two precompiled contracts that perform a double point multiplication (DSM) and sum then over any elliptic curve  given p, a,b curve parameters.
> This operation consists in computing the value uP+vQ, u and v being scalars, P and Q being points.
> We managed to implement generic DSM in full solidity with a lower cost than previous implementations (FCL, Daimo, p256-verifier-huff). Such genericity will enable curves such as Ed25519 and Babyjujub (with the use of isogeny we will …

