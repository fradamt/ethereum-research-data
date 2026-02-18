---
source: ethresearch
topic_id: 2665
title: Default post-quantum signature scheme?
author: EricM
date: "2018-07-24"
category: Cryptography
tags: [post-quantum]
url: https://ethresear.ch/t/default-post-quantum-signature-scheme/2665
views: 6650
likes: 7
posts_count: 11
---

# Default post-quantum signature scheme?

Opinions differ about the possibility of practical quantum computers that can easily break elliptic curve cryptography.  However, if there is a breakthrough, it could be an existential threat.  Since it will take some time to transition, it seems prudent to put a high priority on alternatives.

Is there any momentum towards a particular default post-quantum signature scheme for Ethereum?

Is XMSS popular among the research team? ( https://tools.ietf.org/html/rfc8391 )

I realize account abstraction can make the choice of signature scheme flexible, but most users will still want a default that protects them as much as possible.

## Replies

**mathcrypto** (2019-08-30):

It is believed that Lamport signatures are Quantum secure. Unfortunately, each Lamport key can only be used to sign a single message. However, combined with [hash trees](https://en.wikipedia.org/wiki/Merkle_tree), a single key could be used for many messages, making this a fairly efficient digital signature scheme.

**Size issues:**

The size of Lamport public key and signature together is 231 times (106 bytes vs 24KB) more than the ECDSA public key and signature.

The public key and signature form part of each bitcoin transaction and are stored in blockchain. So use of Lamport Signature will need 231 times more storage than ECDSA.

---

**vbuterin** (2019-09-02):

Lamport is too large to be practical; you want Winternitz signatures (I much prefer Karl Gluck’s more descriptive name [“hash ladder signatures”](https://gist.github.com/karlgluck/8412807)). You can get those down to 1 KB or less (and then you can add a hash tree to make them multi-use).

If you want a “stateless” signature scheme then I believe the state of the art is [SPHINCS](https://sphincs.org/), where signature sizes come out to ~40 kB AFAIK, though you may be able to do better these days by adapting a STARK.

---

**mihasK** (2019-09-14):

SPHINCS is state of the art only among hash-based signatures.

While it’s simple and reliable, I would look into more powerful platforms,

the best option is lattice-based cryptography. You can implement almost any cryptographic constructions using lattices, e.g. if you want to support some privacy-preserving mechanisms, or group signatures, whatsoever. So probably it makes more sense to look into it.

In general, to compare the best options for post-quantum signatures, it’s better to look into results of NIST post-quantum competitions, which runs now. https://csrc.nist.gov/news/2019/pqc-standardization-process-2nd-round-candidates

---

**doctor-gonzo** (2019-09-25):

[The Quantum Resistant Ledger](https://theqrl.org/) project has implemented XMSS [@EricM](/u/ericm), it is the only implementation I know of.

I am no expert but it seems there may be attack vectors with current stateless post-qc methods. I know BLISS is vulnerable to side channel attack, and it seems like SPHINCS is also [vulnerable to attacks](https://eprint.iacr.org/2018/674) which XMSS is not.

---

**deryakarl** (2022-04-26):

Another interesting fact that needs attention:

A  k -bit number can be factored in time of order **O(k^3)** using a quantum computer of **5k+1 qubits** (using Shor’s algorithm).

- See http://www.theory.caltech.edu/~preskill/pubs/preskill-1996-networks.pdf

256-bit number (e.g. Bitcoin public key) can be factorized using 1281 qubits in 72*256^3 quantum operations.

- ~ 1.2 billion operations == ~ less than 1 second using good machine

ECDSA, DSA, RSA, ElGamal, DHKE, ECDH cryptosystems are all quantum-broken

Conclusion: publishing the signed transactions (like Ethereum does) is not quantum safe → avoid revealing the ECC public key

---

**Pratyush** (2022-04-28):

For elliptic curve operations, you’re not factoring anything; it’s a different problem (discrete log) which requires a different approach. See, e.g., here: [Quantum Resource Estimates for Computing Elliptic Curve Discrete Logarithms | SpringerLink](https://link.springer.com/chapter/10.1007/978-3-319-70697-9_9)

---

**deryakarl** (2022-05-09):

I hear you Pratyush , thanks for your reply. I’m aware of this information : In [[44](https://link.springer.com/chapter/10.1007/978-3-319-70697-9_9#ref-CR44)], Shor presented two polynomial time quantum algorithms, one for factoring integers, the other for computing discrete logarithms in finite fields. The second one can naturally be applied for computing discrete logarithms in the group of points on an elliptic curve defined over a finite field.

It is well known in computer science that **quantum computers will break some cryptographic algorithms** , especially the public-key crypto-systems like **RSA** , **ECC** and **ECDSA** that rely on the **IFP** (integer factorization problem), the **DLP** (discrete logarithms problem) and the **ECDLP** (elliptic-curve discrete logarithm problem). Quantum algorithms will not be the end of cryptography, actually can be a cure to current problems of security and scalability. There is dedicated work to build quantum-secure robust crypto-systems.

Appreciated your feedback.

---

**nufn** (2022-07-06):

Hi, here is our proposal about adding a new transaction type to the EVM to achieve a hybrid post quantum digital signature, in line with NIST latest PQ standardisation. Details in [this post](https://ethresear.ch/t/a-hybrid-post-quantum-digital-signature-scheme-for-the-evm/13008) and full proposal [here](https://bit.ly/FlarePQEVM).

---

**pldd** (2023-01-23):

At Pauli Group we created an EVM [smart contract wallet](https://anchorwallet.ca/) that requires a Lamport signature (with decentralized verification) to execute transactions. This is fully quantum resistant and can be used to protect digital assets over the long term. You can read our roadmap for more advanced quantum resistant smart contracts in our [whitepaper](https://anchorwallet.ca/whitepaper/).

The network will still have to upgrade to post-quantum signatures (like Falcon or Dilithium) but at least it’s now possible to start upgrading the quantum vulnerable ECDSA wallets now.

---

**gcsfred2** (2024-01-18):

On the subject:

Quantum-safe transactions on Ethereum - Aditya Bisht

A Signature Fit for a Post Quantum Era: Dilithium-Ed25519 - Prof Bill Buchanan

There’s still the need to ultimately replace ECDSA directly in the protocol.

