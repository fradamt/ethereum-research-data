---
source: magicians
topic_id: 18053
title: "EIP-7592: Falcon signature verification pre-compile"
author: christam96
date: "2024-01-10"
category: EIPs
tags: [eip]
url: https://ethereum-magicians.org/t/eip-7592-falcon-signature-verification-pre-compile/18053
views: 1701
likes: 3
posts_count: 3
---

# EIP-7592: Falcon signature verification pre-compile

Hi Magicians ![:sparkles:](https://ethereum-magicians.org/images/emoji/twitter/sparkles.png?v=12)

This post is about a discussion proposing to add a pre-compile for Falcon signature verification, a post-quantum digital signature soon to be standardized by NIST.

Ethereum’s public key infrastructure heavily relies on the Elliptic Curve Digital Signature Algorithm (ECDSA), an algorithm whose security is rooted in the assumed complexity of the discrete logarithm problem. In 1994, Peter Shor introduced Shor’s algorithm, capable of solving the discrete logarithm problem in polylogarithmic time, implying that ECDSA will no longer be safe in the face of a quantum adversary. While it may be such that there is not a general purpose quantum computer capable of breaking ECC today, this will likely not be the case tomorrow. This urgency underscores the pressing need to explore alternative cryptographic solutions to safeguard Ethereum’s infrastructure. Falcon is a cryptographic signature algorithm submitted to the NIST Post-Quantum Cryptography Project and is set to be standardized in 2024. Of the digital signatures to be standardized by NIST, Falcon wields a signature size a full order of magnitude smaller than it’s contemporaries. The addition of a precompiled contract for Falcon signature verification would:

1. Open the door to quantum-safe wallets using signature abstraction to replace ECDSA with Falcon
2. Allow for efficient verification of Falcon transactions
3. Facilitate further research such as signature aggregation of Falcon signatures, and the adoption of quantum-safe cryptographic primitives across Ethereum

EIP Page: [Add EIP: Precompile for Falcon Signature Verification by christam96 · Pull Request #8103 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8103)

## Replies

**jdetychey** (2024-02-09):

I may be wrong here but regarding post quantum security on Ethereum, I think the plan was to migrate from BLS to STARK agregation see: [Pragmatic signature aggregation with BLS - Sharding - Ethereum Research](https://ethresear.ch/t/pragmatic-signature-aggregation-with-bls/2105)

Do you know the timeline of NIST for this standardisation?

If I remember correctly, the European Commission ran several academic working group on the topic which concluded in favor of NTRU as a post quantum standard candidate. Does NIST only push for Falcon?

---

**eum602** (2024-02-09):

Hi!!, this is a great initiative and demonstration the community is switching towards the benefits of using post quantum Falcon signatures. Since 2020/2021 we have been exploring the possibility to integrate Falcon in Ethereum. After a series of test, even implementing the feature in solidity we realized a good and feasible approach was to use a precompiled contract. Part of the work was published in Nature Science Journal [here](https://www.nature.com/articles/s41598-023-32701-6) and a consolidated core implementation  summarized in a [EIP](https://github.com/ethereum/EIPs/pull/8190/files) proposal we were preparing last year and recently launched. Since this is a similar proposal with a slightly different approach let’s see how we can collaborate so both efforts can converge and have Falcon signatures a reality in ethereum.

We have opened a thread explaining some detailed inputs [here](https://ethereum-magicians.org/t/eip-7619-falcon-512-precompiled-generic-signature-verifier/18569)

