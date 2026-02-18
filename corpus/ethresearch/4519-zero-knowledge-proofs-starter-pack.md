---
source: ethresearch
topic_id: 4519
title: Zero-Knowledge Proofs Starter Pack
author: PaulRBerg
date: "2018-12-08"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/zero-knowledge-proofs-starter-pack/4519
views: 37035
likes: 55
posts_count: 8
---

# Zero-Knowledge Proofs Starter Pack

On my journey to join the [club of people](https://twitter.com/PaulRBerg/status/1044556551938363392) who possess a reasonable understanding of ZKP cryptography, I stumbled upon many invaluable resources that provided to be very helpful. The problem was that they were rather scattered on the web. The [awesome ZKP repo](https://github.com/gluk64/awesome-zero-knowledge-proofs) is indeed awesome but a bit verbose and lacks videos and podcasts.

The goal of this post is to serve as an entry point for anyone interested to make their baby steps towards understanding the core technical layers of zero-knowledge-whatever. It is important to note that this is definitely not an exhaustive list, but rather a set of supportive resources for ZKPs that have a connection to the blockchain ecosystem.

**Legend**

- ZKP = Zero-Knowledge Proof
- zkSNARK = Zero-Knowledge Succinct Non-Interactive ARgument of Knowledge
- zkSTARK = Zero-Knowledge Scalable Transparent ARgument of Knowledge
- AZTEC = Anonymous Zero-knowledge Transactions with Efficient Communication

**Induction**

- [Deck] Elena Nadolinski: Demystifying Zero-Knowledge Proofs
- [Article] Matthew Green: An illustrated primer
- [Podcast] Zero Knowledge FM: Intro to Zero-Knowledge Proofs with Anna Rose & Fredrik Harrysson
- [Video] What Are Zero-Knowledge Proofs
- [Video] Elad Verbin: Zero-Knowledge Proofs and Their Future Applications at Web3 Summit 2018
- [StackExchange] Comparison between SNARKs, STARKs and Bulletproofs

**zkSNARKs**

- [Article Series] Vitalik Buterin: zkSNARKs Under the Hood
- [Article] Zcash: What are zkSNARKs?
- [Podcast] Zero Knowledge FM: Intro to zkSNARKs with Howard Wu
- [Video] Howard Wu: Rise of the SNARKs

**zkSTARKs**

- [Video] Eli Ben Sasson: Introduction of zkSTARKs at Technion Cyber and Computer Security Summer School
- [Deck] State of the STARK at Devcon4
- [Article Series] By Vitalik Buterin

**Bulletproofs**

- [Podcast] Zero Knowledge FM: Benedikt Bünz on Bulletproofs and Verifiable Delay Functions
- [Video] Bulletproofs: Short Proofs for Confidential Transactions and More
- [Video] Benedikt Bünz at SF Bitcoin Devs

**AZTEC**

- [Article] Zachary Williamson: A dive into the AZTEC protocol
- [Podcast] The Smartest Contract: Confidential transactions on Ethereum via range proof

**MimbleWimble**

- [Video] Jackson Palmer: What is MimbleWimble
- [Video] Andreas Antonopoulos: Bitcoin Q&A: MimbleWimble and Schnorr signatures
- [Article] Conor O’Higgins: MimbleWimble explained like you’re 12

**Papers**

- Zerocash: Decentralized Anonymous Payments from Bitcoin
- Scalable, transparent, and post-quantum secure computational integrity
- Bulletproofs: Short Proofs for Confidential Transactions and More
- The AZTEC Protocol
- MimbleWimble

Hope this helps! Open to additions and other suggestions.

## Replies

**light** (2018-12-19):

This post about ZkDai might be a good addition to these resources:

https://medium.com/@atvanguard/zkdai-private-dai-transactions-on-ethereum-using-zk-snarks-9e3ef4676e22

---

**MihailoBjelic** (2018-12-20):

Here’s another super-awesome paper on SNARKs by Christian Reitwießner: https://chriseth.github.io/notes/articles/zksnarks/zksnarks.pdf.

This one will help you fully understand all the “moon math” that is the heart of SNARKs and that is almost never explained in tutorials/presentations. ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=9)

---

**GriffGreen** (2018-12-21):

This walk thru is a must try if you actually want to get your hands dirty:

https://iden3.io/blog/circom-and-snarkjs-tutorial2.html

---

**lebed2045** (2019-02-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/paulrberg/48/17405_2.png) PaulRBerg:

> zkS N ARK = Zero-Knowledge Succinct Non-Interactive ARgument of Knowledge

cool content compilation! Guys, if anyone wants to give a try and learn zkSnarks properly, please ping me [x.com](https://twitter.com/lebed2045). Would be nice to have a learning companion and to study together.

---

**cooganb** (2019-05-16):

Another good one is this overview of PCPs, which underpin SNARKs and STARKs


      ![](https://ethresear.ch/uploads/default/original/3X/7/6/761799b36b5fd945eba6b29ef9bd602e26fd4c55.png)

      [Consensys - Building the Era of Decentralized Finance](https://consensys.io/)



    ![](https://ethresear.ch/uploads/default/optimized/3X/3/2/32768be956c05ae27f520b4f2a0c2b09bc6b1012_2_690x361.png)

###



Consensys is a blockchain software company building the tools, infrastructure and research that power the new Era of Decentralized Finance, for a more secure and open economy

---

**Econymous** (2019-05-16):

zkp rivals enigma, correct?

---

**SamuelDare** (2019-06-30):

[@Econymous](/u/econymous) you can view Zero Knowledge Proofs as a family of functions that ensure honest computation. They can be used for privacy, scalability and annonymity .Enigma employs Multi Party Computation which is a subset of ZKP where multiple parties are used to provide the answer to to a problem without revealing it to everyone.

