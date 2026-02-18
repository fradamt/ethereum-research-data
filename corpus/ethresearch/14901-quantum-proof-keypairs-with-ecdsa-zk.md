---
source: ethresearch
topic_id: 14901
title: Quantum Proof Keypairs with ECDSA + ZK
author: yush_g
date: "2023-02-25"
category: zk-s[nt]arks
tags: [post-quantum]
url: https://ethresear.ch/t/quantum-proof-keypairs-with-ecdsa-zk/14901
views: 3656
likes: 14
posts_count: 5
---

# Quantum Proof Keypairs with ECDSA + ZK

So far, I’ve only seen solutions on ethresearch to quantum proof Ethereum via new keypair types. However, I think there’s a more robust solution to migrate Ethereum than hardforking to a quantum resistant keypair, as this would break every single wallet and piece of key-related infra. I think there’s a way to quantum-proof Ethereum on the existing ECDSA on secp256k1. The reason Ethereum is not currently quantum proof is that after sending a tx, an account’s public key is revealed (i.e. the hash preimage of your address), so an adversary can take the discrete log efficiently with a quantum computer, and get someone’s secret key. If there was a way to send txs that didn’t reveal the public key, this would allow existing keypairs to remain quantum secure. If you want a brief refresher on what exactly quantum computers can do cryptography wise, you can refer to [this blog post](https://blog.aayushg.com/posts/quantumcrypto)/[zkresearch post](https://zkresear.ch/t/how-quantum-computers-affect-zk-and-blockchains-how-to-quantum-proof-ethereum/59/8).

So a post-quantum Ethereum account could keep their public key hidden, and only make their addresses public. Then, to send a tx, instead of signing it, they publish a zk proof of knowing a valid signature that corresponds to their address, and that would authorize the transfer, so no one would ever even know their public key! With account abstraction-type solutions, this type of thing could even be possible as soon as that is available on any L2 or L1. It wouldn’t work on accounts that have already sent any tx’s today (since those reveal public keys), but such accounts could easily send all their assets to a new keypair, and vow to not reveal their public key in those cases. It would quantum proof Ethereum in the long term as well (similarly to how unused utxos in btc are safe right now).

You’d have to use a STARK, since SNARKs right now don’t have post-quantum soundness, and the ECDSA proof would have to be fast to generate and verify.

One issue is that smart contracts need to be special-cased, since we know the pre-image of the address via create2. One easy solution is to hard-code that once a contract has been made by create/create2, transactions that utilize their secret key are disallowed (i.e. no signatures or eoa-style txs will be validated).

Perhaps, for future smart contracts, if we don’t want to special case them, we could standardize around a new opcode (say create3, or create2 with an optional arg), that, say, just swaps the last bit in the create2 output. This keeps the address determination deterministic, but does not reveal the pre-image of the hash.

This also probably requires some renaming of terminology; for instance, public keys shouldn’t be public, so renaming them to be like, quantum insecure keys, hidden keys, or private addresses or something might be useful. It also requires hardware wallets to be able to calculate proofs, which doesn’t seem feasible right now – hopefully this usecase drives research for stark computation in low resource environments though. It can also be punted to software for now, as long as the user trusts that the software won’t reveal their public key to anyone.

## Replies

**Hugo0** (2023-07-26):

This is pretty neat, thanks [@yush_g](/u/yush_g) . Expect this thread to get way more popular now ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

It’s a bit jarring to imagine traditionally public keys to eventually become confidential information ^^

Hopefully by 2030, or whenever this becomes a problem, enough work has been done on AA that just deriving a single keypair doesn’t immediately compromise an entire account.

---

**yush_g** (2024-02-17):

Aditya Bisht implemented this scheme with a FRI proof directly settled on Ethereum, which you can see here: [GitHub - Bisht13/post-quantum-eth-security](https://github.com/Bisht13/post-quantum-eth-security)

Because it was not wrapped in KZG, it was plausibly post-quantum safe. However, due to transaction gas limits, it took 10 transactions to do the proof. (The paymaster signing the tx of course is not quantum-proof, but a simple EIP enabling post-quantum signers on the L1 would resolve that).

---

**yush_g** (2024-02-24):

Thanks to Or Sattath for mentioning this idea on [Episode 288 of ZK Podcast](https://www.youtube.com/watch?v=g-Y4PT8va94)!

---

**AndreevPetr** (2024-04-13):

Thank you for the wonderful article and splendid links. The link 2quantumcrypto doesn’t work, but it nonetheless leads to the marvelous blog Aayush’s Thoughts. I am very interested in the following newbie questions regarding quantum technologies, though I’m not sure how relevant and correct they are in the context of discussing security and the use of quantum technologies. Please consider each of them separately:

***Question 1***: Lately, quantum random number generators have become significantly **cheaper**. Can their use protect and enhance the security of Ethereum storages through quantum random number generators?

Quantum Random Number Generators (QRNGs) utilize quantum properties of particles, such as superposition and entanglement, to generate truly random numbers. These numbers can be used to enhance the security of cryptographic systems, including blockchains like Ethereum. The true randomness of quantum generators makes predicting or reproducing the generated keys extremely difficult, if not impossible, making cryptosystems more resilient to attacks.

For instance, the use of QRNGs in Ethereum storages can enhance security in the following ways:

- Key Generation: QRNGs can be used to create more secure private keys, reducing the risk of them being guessed or cracked by algorithms.
- Protocol Strengthening: QRNGs can be integrated into consensus protocols, improving their randomness and fairness.
- Smart Contracts Improvement: Smart contracts that utilize randomness (for example, for games or lotteries) can benefit from the unpredictability of truly random numbers generated by quantum generators.

*Question 2*: From a futurism perspective or in terms of actual protection for **large** storages, can **quantum entanglement** provide protection against “man-in-the-middle” attacks?

Quantum entanglement is a phenomenon where the state of one particle instantly influences the state of another, regardless of the distance between them. This property is fundamental to quantum cryptography and Quantum Key Distribution (QKD), which can offer a fundamentally new level of protection against “man-in-the-middle” attacks.

QKD uses quantum entanglement for the secure exchange of cryptographic keys between two parties. Any attempt to intercept or measure the quantum state of the keys during transmission would result in a change in their state and would be immediately noticeable, providing a high level of protection against eavesdropping.

The use of quantum entanglement for protection against “man-in-the-middle” attacks includes:

- Eavesdropping Detection: Any attempt to interact with quantum-entangled particles leads to changes that can be detected as an eavesdropping attempt.
- Unconditional Security: Theoretically, QKD methods can provide unconditional security by using fundamental properties of physics, unlike traditional cryptography, which relies on computational complexity.

*Question 3*: Are you aware of any companies that reliably destroy equipment on which they generate keys for their cold wallets, so the user can be 100% sure that their wallet cannot be obtained through the recovery of hard drives?

I understand that the practical application of these technologies is still in the development stage, and there are many technical and organizational obstacles in the way of their widespread adoption. Nevertheless, I would be very pleased if quantum technologies offered significant opportunities for improving security in the field of cryptography and data protection, including protection against “man-in-the-middle” attacks

Thank you for any answer or links!

