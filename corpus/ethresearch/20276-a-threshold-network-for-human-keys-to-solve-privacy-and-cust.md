---
source: ethresearch
topic_id: 20276
title: A Threshold Network for “Human Keys” to solve privacy and custody issues
author: nanaknihal
date: "2024-08-14"
category: Cryptography
tags: [security, zk-id]
url: https://ethresear.ch/t/a-threshold-network-for-human-keys-to-solve-privacy-and-custody-issues/20276
views: 984
likes: 11
posts_count: 3
---

# A Threshold Network for “Human Keys” to solve privacy and custody issues

# Introduction

In blockchain and PKI more generally, people are represented by keys. A somewhat strange question to ask might be “why don’t keys represent people?” I will argue this is actually an important question and the crux of major privacy and onboarding challenges. We present a a threshold network design dubbed Mishti Network to derive keys from people rather than arbitrary randomness. This network solves a number of problems in ZK identity, compliance, and onboarding.

What does it mean for a key to be a representation of a person? There are two conditions that should be met:

- A person’s knowledge and/or attributes can always map to the private key
- This person is the sole controller of the key

In other words, it is a collision-resistant map of personal data and attributes to a high-entropy pseudorandom number. Without collision resistance, multiple people could have the same key. Without high entropy, the key is not secure. Keys can be both standard private keys or also a nullifier that’s useful for secure ZK credentials.

Human keys are not solely biometrics. They could be from human-friendly data such as security questions, passwords, or any unique knowledge belonging to an individual rather than arbitrary randomness.

# Solution: Oblivious Pseudorandom Function

This solution is based on a threshold verifiable oblivious pseudorandom function (tVOPRF) on private data. An oblivious pseudorandom function (OPRF) takes a private input and computes a pseudorandom function (PRF). PRFs take low-entropy input and create high-entropy output. Adding verifiability via a ZKP makes it into a VOPRF. Verifying individual node contributions is important to decentralizing the network.

# Why it is helpful to Ethereum + PKI

Some of the outstanding issues in Ethereum are onboarding and privacy. Onboarding requires not just simplicity but also self-custody, and recovery. Current onboarding solutions such as social logins and passkeys do not have self-custody (as they can be recovered by web2 accounts), while self-custodial solutions can’t have recovery without extra onboarding step like electing gaurdians.

A similar need is for ZK identity applications that need to derive nullifiers from their users’ identities, in a way nobody can trace back to the user. This is a common need in proof-of-personhood solutions to ensure that each person only has one corresponding nullifier without a central database or key that links users to their nullifiers.

Furthermore, the underlying cryptography and network can be repurposed to tackle another pressing challenge: that of satisfying compliance rules with ZK identity. The same underlying elliptic curve multiplication primitive that underlies this design can be used to construct threshold ElGamal decryption over ZK-friendly curves, which can allow ZK proofs to contain encrypted data with flexible access control.

# Oblivious Pseudorandom Function

To generate keys from identities, an oblivious pseudorandom function (OPRF) can be constructed with distributed EC scalar multiplication. This allows private user data such as security questions, biometrics, passwords, or social security numbers, etc. to deterministically generate secret keys. The resulting pseudorandom value is computationally impractical to reverse despite it being from low-entropy input. One can thereby create wallet or nullifier from any (or a combination) of these low-entropy “human” factors. In the 2HashDH OPRF [1], a server or network’s secret is used to give randomness to the client’s input. The oblivious property prevents any server or set of nodes from seeing see this input.

2HashDH is the following algorithm between a user with a private input x and a server (or network) with a private key s. For a subgroup G of an elliptic curve there are two hash functions:

hashToCurve: \{0,1\}^* \rightarrow G

hashToScalar: G \rightarrow F_q.

The 2HashDH OPRF proceeds as follows

1. User samples a random mask r and sends M = r * hashToCurve(x)
2. Server multiplies by its secret, returning s * M
3. User computes the output by unmasking the server’s response and hashing it: o = HashToScalar(r^{-1} * s * M)

o is uniformly pseudorandom in F_q, and the server is information-theoretically blinded from the user’s input.

## Decentralizing the server

To decentralize the OPRF server, only the step with a server must be decentralized:

> Server multiplies by its secret, returning s * M

For threshold elliptic curve multiplication, first a linear secret sharing, such as Shamir’s scheme, must be used. The secret key is generated through distributed key generation (DKG) such that each node with index i receives share f(i) for some secret polynomial f known to nobody. There is no node at the 0 index and f(0) is the secret key of the network. The secret key f(0) can be computed by a set Q of t nodes where t is one more than the degree of f.

f(0) = \sum_{i \in Q}{L_{0, Q}(i)*f(i)}

where L_{0,Q}(i) is the Lagrange basis for index i in set Q evaluated at zero.

Instead of reconstructing f(0), the nodes can collaborate to construct f(0) * M

f(0) * M = \sum_{i \in Q}{L_{0, Q}(i)*f(i) * M}

This is sufficient for step

> Server multiplies by its secret, returning s * M

if the nodes are honest. But if one lies, the result will be wrong and there will be no way of knowing who lied. Thus, each node should prove their individual multiplication using a lightweight zero-knowledge DLEQ proof.

# Other interesting use case: Provable encryption with programmable privacy

The same decentralized EC scalar primitive can be used not just for VOPRF but also for ElGamal decryption over ZK-friendly curves. This is helpful when identities must be revealed in certain conditions.

For example, many private DeFi protocols are interested in ensuring that bad actors do not get the benefits of anonymity, while the average user typically does. Governments are not satisfied with solely ZK because they need access to user data, but currently the only alternative is honeypots where all user data is stored to be turned over to authorities if needed.

Another use of revealing provably encrypted identities under certain conditions is undercollateralized lending – what if you want an identity or private key to be revealed if a DeFi loan is defaulted on? In this case, you need to prove the proper data is encrypted correctly, then have a smart contract control decryption rights.

To modify this threshold EC point multiplication to such use cases, little is needed.

### Encryption

ElGamal encryption is client-side:

1. Create an ephemeral keypair (a, A = aG)
2. Encode the message as an EC point P
3. Compute Diffie-Hellman shared secret with network public key: aB
4. Compute the ciphertext (A, aB+P)

### Decryption

Unlike encryption, decryption requires a server or decentralized network.

1. Server/network multiply ephemeral public key A by its secret key b to get bA = aB
2. Decryptor subtracts this value from aB+P to get P

The server/network’s step can be handled by the same threshold multiplication protocol as before!

# Network Setup and Collusion Protection

The team at Holonym has implemented this as as an AVS on Eigenlayer called Mishti Network. High reputation is common among Eigenlayer operators despite the permissionless nature, so it is ideal for threshold networks where collusion is a concern. To further mitigate collusion risk, there is the idea of parallel networks:

The asynchronous and homomorphic nature of the computations means users can permissionlessly add nodes outside of Mishti Network that they trust to not collude with Mishti Network. E.g. instead of splitting a secret between Mishti Network, half of the secret is between the Mishti Network and the other half in a semi-trusted node elected by the user. Since the whole network just does an EC multiplication, exactly what its individual does do, nodes and networks can be treated the same. A 2/2 scheme could be done between a semi-trusted node and Mishti network, simply by

- Adding their public keys to get the joint public key
- Adding their responses to get a joint response to the computation

Note this requires no consent from the network and is not limited to 2/2 schemes; it can be done with any combination of semi-trusted nodes and/or independent networks via threshold schemes.

# References

[1] S. Jarecki, A. Kiayias, and H. Krawczyk, “Round-optimal

password-protected secret sharing and T-PAKE in the password only model,” in International Conference on the Theory and Application of Cryptology and Information Security. Springer, 2014 pp. 233–253

# Concluding Notes

If you have any ideas on how to improve or elaborate on this network design for either ZK identity, self-custody, or any other relevant use cases, please reply or reach out.

## Replies

**turboblitz** (2024-08-16):

Linking private keys to users in a reliable way is definitely a hard problem, and I like how your solution just relies on one EC operation without additional fuss.

It seems like the challenge with this kind of design is that the threshold secret has to be persistent across long periods time. This is very different from most MPC/TSS systems in which an operation is performed once. In particular:

- No rotation is possible, as the threshold secret must be persistent for nullifiers/private keys to stay fixed. It’s possible to add nodes but not to remove them. This means that if a node wants to leave the network, either the threshold secret stops being recoverable, or new shares are issued and now a new share is in the wild, with no incentive to prevent its leakage.
- Secret share leakage is not detectable. This can be partially mitigated by letting someone obtaining the secret share of a node slash it and getting part of the stake, but that assumes that the stakes are high enough and the colluder is money-driven, i.e. not a state actor for instance.

I’m curious of possible mitigations because this is definitely something we’re looking for in the context of nullifiers for OpenPassport.

---

**nanaknihal** (2024-08-19):

Thanks, glad to hear this could be useful to your nullifier scheme at OpenPassport! To answer your questions:

![](https://ethresear.ch/user_avatar/ethresear.ch/turboblitz/48/10155_2.png) turboblitz:

> No rotation is possible, as the threshold secret must be persistent for nullifiers/private keys to stay fixed. It’s possible to add nodes but not to remove them. This means that if a node wants to leave the network, either the threshold secret stops being recoverable, or new shares are issued and now a new share is in the wild, with no incentive to prevent its leakage.

It is possible to add and remove nodes via a resharing protocol! We designed a resharing protocol to be run at each epoch, upon which active nodes and nodes waiting to join can form the new n. All old shares are invalidated at each epoch, and the new shares are shares of the same private key. In this protocol, similar to the DKG, new n and t values are chosen, and corresponding new shares (k_i, K_i) are chosen for the i nodes in a set Q, for a new epoch e+1.

[![image](https://ethresear.ch/uploads/default/optimized/3X/e/1/e142da11eae103a1d406c59ffffdfd87c007a362_2_401x500.jpeg)image1088×1354 208 KB](https://ethresear.ch/uploads/default/e142da11eae103a1d406c59ffffdfd87c007a362)

![](https://ethresear.ch/user_avatar/ethresear.ch/turboblitz/48/10155_2.png) turboblitz:

> Secret share leakage is not detectable. This can be partially mitigated by letting someone obtaining the secret share of a node slash it and getting part of the stake, but that assumes that the stakes are high enough and the colluder is money-driven, i.e. not a state actor for instance.

The bad news: the economic strategy actually doesn’t work because of resharing – for any secret sharing protocol where “standard” resharing exists, incl. Shamir’s, t nodes can just run a resharing protocol to get new shares which aren’t linked to a particular node. They can even frame nodes though, since by knowing the polynomial they can derive any node’s keyshare and thus “frame” innocent nodes for the collusion!

The good news: there are non-economic ways of protecting against collusion. My favorite is the idea of a semi-trusted node or a paranet. Say you have two parallel Mishti networks with keys k_1 and k_2 respectively. Recall their goal is just multiplying their key by an input point.

You request to both networks with input point P and recieve (k_1*P, k_2*P).

Even though the networks have not communicated, you can treat their output as if it came from a single network with public key K1+K2 by adding them to get

(k_1*P+k_2*P)

(k_1+k_2)*P

By treating both independent networks as a joint network, both must be corrupt and collude with each other. When one network is a single node, you have a case we are calling a “semi-trusted node.” It cannot see any secret but is trusted to not collude. Even if the decentralized network colludes, as long as this node doesn’t the collusion can’t do damage. Instead of a single node it could instead be a collection of credibly neutral organizations, like how [drand](https://drand.love) is set up.

Now there are other ways too of preventing collusion, like enclaves, but I like this more.

