---
source: ethresearch
topic_id: 19676
title: Practical, Trustless, Bitcoin Bridge
author: cryptskii
date: "2024-05-29"
category: Cryptography
tags: []
url: https://ethresear.ch/t/practical-trustless-bitcoin-bridge/19676
views: 3984
likes: 1
posts_count: 4
---

# Practical, Trustless, Bitcoin Bridge

## TL;DR

This proposal presents a practical trustless Bitcoin bridge using Nillion’s NMC (Nil Message Compute) protocol. The bridge leverages secure encryption, secret sharing, and cross-chain witness validation to enable the secure and decentralized transfer of Bitcoin to other blockchains.

## Background

Interoperability between different blockchains is crucial for the growing decentralized ecosystem. Trustless bridges allow secure transfers of assets and information across blockchain networks without relying on a central trusted authority. Nillion’s NMC protocol provides a framework for creating such trustless bridges.

## Proposal

The proposed trustless Bitcoin bridge consists of the following steps:

1. Initial Encryption:

 The Bitcoin secret key ( K ) is encrypted using a symmetric encryption scheme ( E = (\text{Enc}, \text{Dec}) ) with a condition-based ciphertext ( C ) dependent on a predefined condition ( \Phi ) on a separate blockchain, such as Ethereum:
 C = \text{Enc}(K, \Phi)
2. Generating Particles:

 A One-Time Mask (OTM) is applied to the ciphertext ( C ) to generate masked particles \{p_i\}_{i=1}^n:
 p_i = C \oplus b_i \quad \forall i \in [1, n]
 where \{b_i\}_{i=1}^n are random blinding factors.
3. Blinding Factor Sharing:

 Linear Secret Sharing (LSS) is used to distribute the blinding factors \{b_i\}_{i=1}^n among a decentralized network of nodes \{N_i\}_{i=1}^n.
4. Polynomials f_i(x) of degree t are constructed for each blinding factor b_i:
 f_i(x) = b_i + a_1 x + a_2 x^2 + \cdots + a_t x^t
5. n shares \{s_{i,j}\}_{j=1}^n are generated for each blinding factor b_i by evaluating f_i(x) at distinct points x_j \in \mathbb{F}_p:
 s_{i,j} = f_i(x_j) \quad \forall j \in [1, n]
6. The shares are distributed to the corresponding nodes N_j.
7. Particle Distribution:

The masked particles \{p_i\}_{i=1}^n are distributed across the decentralized network of nodes \{N_i\}_{i=1}^n.
8. Each node N_i holds a single particle p_i.
9. Witness Condition Validation:

Upon fulfillment of the predefined condition \Phi on the Ethereum blockchain, a witness proof \pi is generated.
10. Nodes validate the witness proof \pi to initiate the reconstruction process.
11. Reconstruction and Decryption:

 Nodes collaborate to reconstruct the blinding factors \{b_i\}_{i=1}^n using the LSS shares:
 b_i = \sum_{j \in I} s_{i,j} \prod_{k \in I \setminus \{j\}} \frac{x_k}{x_k - x_j}
 where I \subseteq [1, n] and |I| = t + 1.
12. With the reconstructed blinding factors \{b_i\}_{i=1}^n, nodes unmask their particles p_i to recover the original ciphertext C:
 C = p_i \oplus b_i \quad \forall i \in [1, n]
13. The recovered ciphertext C is decrypted using \text{Dec} and the condition \Phi to obtain the Bitcoin secret key K:
 K = \text{Dec}(C, \Phi)

## Advantages

The proposed trustless Bitcoin bridge has several advantages:

- Decentralization: The use of a decentralized network of nodes eliminates the need for a central trusted authority.
- Security: The encryption and secret sharing techniques ensure the confidentiality and integrity of the Bitcoin secret key.
- Cross-chain interoperability: The bridge enables the secure transfer of Bitcoin to other blockchains, such as Ethereum, based on predefined conditions.
- Fault tolerance: The use of Linear Secret Sharing provides fault tolerance, as the secret can be reconstructed even if some nodes are unavailable or malicious.

## Applications

The trustless Bitcoin bridge has various applications, including:

- Cross-chain asset transfers: Enabling the seamless transfer of Bitcoin to other blockchains for use in decentralized applications (DApps) and decentralized finance (DeFi) protocols.
- Atomic swaps: Facilitating atomic swaps between Bitcoin and other cryptocurrencies without the need for a trusted intermediary.
- Conditional payments: Allowing for conditional Bitcoin payments based on events or conditions on other blockchains.

## Conclusion

The proposed trustless Bitcoin bridge using Nillion’s NMC protocol provides a secure, decentralized, and interoperable solution for transferring Bitcoin across different blockchain networks. By leveraging cryptographic techniques such as encryption, secret sharing, and cross-chain witness validation, the bridge ensures the integrity and confidentiality of the transferred assets. This proposal opens up new possibilities for cross-chain asset transfers, atomic swaps, and conditional payments, further enhancing the interoperability and composability of the decentralized ecosystem.

[Nillion Whitepaper](https://cognizium.io/uploads/resources/Nillion%20-%20A%20Secure%20Processing%20Layer%20for%20Web3%20-%202022%20Feb.pdf)

## Replies

**cryptskii** (2024-05-29):

## Step-by-Step Example with Trustless Mechanisms Using HTLC

#### Initial Encryption

1. Bob creates a Bitcoin secret key (K).
2. Bob encrypts (K) using a symmetric encryption scheme (\text{Enc}, \text{Dec}) with a condition-based ciphertext (C) dependent on a predefined condition (\Phi) on the Ethereum blockchain:
C = \text{Enc}(K, \Phi)

#### Generating Particles

1. Bob applies a One-Time Mask (OTM) to the ciphertext (C) to generate masked particles \{ p_i \}_{i=1}^n:
p_i = C \oplus b_i \quad \forall \, i \in [1, n]

where \{ b_i \}_{i=1}^n are random blinding factors.

#### Blinding Factor Sharing

1. Bob uses Linear Secret Sharing (LSS) to distribute the blinding factors \{ b_i \}_{i=1}^n among a decentralized network of nodes \{ N_i \}_{i=1}^n.
2. Polynomials f_i(x) of degree t are constructed for each blinding factor b_i:
f_i(x) = b_i + a_1 x + a_2 x^2 + \cdots + a_t x^t
3. n shares \{ s_{i,j} \}_{j=1}^n are generated for each blinding factor b_i by evaluating f_i(x) at distinct points x_j \in F_p:
s_{i,j} = f_i(x_j) \quad \forall \, j \in [1, n]
4. The shares are distributed to the corresponding nodes (N_j).

#### Bitcoin Locking with HTLC

1. Bob locks the Bitcoin in a hashed time-locked contract (HTLC) on the Bitcoin blockchain. The HTLC specifies that the Bitcoin can only be spent if a cryptographic hash (h(K)) is revealed or after a time period (T) expires.

Bob generates a hash (h(K)) of the Bitcoin secret key (K) and creates an HTLC with the following conditions:
\text{HTLC: Spendable if } K \text{ is revealed (where } h(K) \text{ matches) or after time } T \text{ expires.}

#### Particle Distribution

1. The masked particles \{ p_i \}_{i=1}^n are distributed across the decentralized network of nodes \{ N_i \}_{i=1}^n.
2. Each node (N_i) holds a single particle (p_i).

#### Witness Condition Validation

1. Upon fulfillment of the predefined condition (\Phi) on the Ethereum blockchain (e.g., an Ethereum smart contract confirms an event), a witness proof (\pi) is generated.
2. Nodes validate the witness proof (\pi) to initiate the reconstruction process.

#### Reconstruction and Decryption

1. Nodes collaborate to reconstruct the blinding factors \{ b_i \}_{i=1}^n using the LSS shares:
b_i = \sum_{j \in I} s_{i,j} \prod_{k \in I \setminus \{j\}} \frac{x_k}{x_k - x_j}

where I \subseteq [1, n] and |I| = t + 1.
2. With the reconstructed blinding factors \{ b_i \}_{i=1}^n, nodes unmask their particles (p_i) to recover the original ciphertext (C):
C = p_i \oplus b_i \quad \forall \, i \in [1, n]
3. The recovered ciphertext (C) is decrypted using (\text{Dec}) and the condition (\Phi) to obtain the Bitcoin secret key (K):
K = \text{Dec}(C, \Phi)

#### Final Result

1. Alice now has the Bitcoin secret key (K) that Bob initially encrypted.
2. Alice can reveal the secret key (K) to claim the Bitcoin from the HTLC on the Bitcoin blockchain.

When Alice reveals (K), Bob (or anyone) can see the revealed (K), which matches (h(K)), allowing Alice to spend the Bitcoin locked in the HTLC.

### Ensuring Trustlessness

- HTLCs: Using HTLCs ensures that the conditions for spending Bitcoin are enforced by cryptographic means rather than relying on trust.
- Decentralized Validation: The decentralized network of nodes validates the witness proof (\pi) and collaborates to reconstruct the secret, maintaining a trustless environment.
- Automated Processes: The entire process is automated through cryptographic protocols, minimizing the need for trust in individual participants.

---

**Ethan** (2024-06-03):

I don’t think decentralize means trustless. You still need a network of trusted nodes.

---

**cryptskii** (2024-06-03):

Hey Ethan, thanks for your interest and feedback!

So you aren’t wrong in your comment here.

![](https://ethresear.ch/user_avatar/ethresear.ch/ethan/48/13959_2.png) Ethan:

> I don’t think decentralize means trustless. You still need a network of trusted nodes.

At least when taken out of context that is. My proposed method is in fact considered to be pretty ideal as far as trustless goes.

Let me provide more examples, and comparisons for a better understanding:

---

### Trustless Bitcoin Bridges: A Comparative Analysis

In the context of blockchain technology, especially Bitcoin bridges, the term “trustless” refers to the ability to operate without relying on a trusted third party, such as a federation or centralized entity. Let’s explore how Nillion’s NMC protocol achieves this and compare it with Wrapped Bitcoin (WBTC) and Stacks’ Nakamoto Upgrade.

### Nillion’s NMC Protocol

**Trust Model**: Fully Trustless

#### Mechanism

- Encryption and Secret Sharing: The Bitcoin secret key is encrypted and divided into shares using Linear Secret Sharing (LSS). These shares are then distributed across a decentralized network of nodes.
- Cross-Chain Condition Validation: A condition on another blockchain (e.g., Ethereum) must be met to initiate the reconstruction of the secret key.
- Reconstruction: Nodes collaborate to reconstruct the secret key without any single node having control, ensuring both decentralization and security.
- Cryptographic Security: The entire process relies on advanced cryptographic techniques, eliminating the need for any trusted third party.

#### Advantages

- Decentralization: No central authority; nodes work together independently.
- High Security: Uses strong cryptographic methods to protect the secret key.
- Interoperability: Facilitates secure transfers across different blockchains.

---

### Wrapped Bitcoin (WBTC)

**Trust Model**: Federated

#### Mechanism

- Custodian-Based System: Bitcoin is held by a centralized custodian (e.g., BitGo) and WBTC tokens are minted on Ethereum, representing the locked Bitcoin.
- Redemption: Users can redeem WBTC for Bitcoin through the custodian.

#### Advantages

- Liquidity: Provides access to Bitcoin liquidity on Ethereum for decentralized finance (DeFi) applications.
- Convenience: Easy integration with Ethereum’s DeFi ecosystem.

#### Disadvantages

- Centralization: Relies on a trusted third party (custodian).
- Security Risk: The custodian is a single point of failure and a potential target for attacks.

---

### Stacks’ Nakamoto Upgrade

**Trust Model**: Decentralized, but not Fully Trustless

#### Mechanism

- Proof of Transfer (PoX): Miners transfer Bitcoin to participate in securing the Stacks blockchain.
- Smart Contracts: Enables smart contracts that can interact with Bitcoin, adding functionality without moving Bitcoin itself.
- Nakamoto Consensus: Anchors Stacks’ transactions in Bitcoin’s security.

#### Advantages

- Security: Leverages Bitcoin’s security to protect Stacks’ operations.
- Decentralization: Uses a network of miners and validators.
- Enhanced Functionality: Allows for smart contracts and advanced interactions with Bitcoin.

#### Disadvantages

- Complexity: More complex than direct tokenization methods.
- Trust in Protocol: Users must trust the Stacks protocol and its security model.

---

# Decentralization vs. Cryptographic Security

**Nillion’s NMC Protocol**:

- Decentralization: Achieved by distributing the encrypted secret shares across multiple nodes.
- Cryptographic Security: Nodes use secret sharing and encryption to process data blindly. They cannot censor or exploit the transaction because they lack sufficient control or knowledge. The security of the system relies more on cryptographic techniques than on decentralization alone.

**Wrapped Bitcoin (WBTC)**:

- Centralized: Relies on a trusted custodian.
- Security: Dependent on the integrity and security of the custodian.

**Stacks’ Nakamoto Upgrade**:

- Decentralization: Utilizes a decentralized network of miners.
- Security: Enhanced by Bitcoin’s underlying security but still requires trust in the protocol.

**Summary Appendix**:

- Decentralization: Spreads out control and decision-making across many nodes, reducing reliance on any single entity.
- Cryptographic Security: Ensures data is processed securely without any node having complete control, thanks to techniques like encryption and secret sharing.
- Nillion’s NMC: Nodes process data blindly, meaning they cannot censor or exploit the transaction, ensuring true trustlessness.
- WBTC: Relies on a centralized custodian, making it less decentralized and trustless.
- Stacks: Decentralized and secure but requires trust in the protocol’s implementation.

[@Ethan](/u/ethan) I would say Stack’s method stands out as the type of implementation where the concern from your comment might hold some weight. Though in the context of this implementation I’m proposing these concerns are removed by the fact that the nodes on Nilion are basically just service nodes, where their functionality is mostly to divide the workload for efficiency and to add redundancy to avoid any single POFs. Their ability to censor or exploit the operations is next to Nil.

Nillion’s crypto primitive (NMC) is quite novel, and offers some new methods that weren’t before possible. Not in the current state of things.

So, similar to something like a “witness encryption Bitcoin bridge” | **see: [Trustless Bitcoin Bridge Creation with Witness Encryption](https://ethresear.ch/t/trustless-bitcoin-bridge-creation-with-witness-encryption/11953) |** would be. My BTC bridge proposal uses advanced cryptography in this case Nillion’s new primitive to provide a fully trustless bridge. The bridging method here is also great in the sense the its heterogenous, and so could be used with Eth, Sol, Dot etc also could be used to bridge LTC or DOGE as well.

Also. Nilion, claims that the computations can be processed at near PlainText speeds. Making this method viable as well as practical to implement.

Hope this helps to clarify!

