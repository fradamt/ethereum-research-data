---
source: ethresearch
topic_id: 17176
title: Novel techniques for zkVM design
author: Victor
date: "2023-10-24"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/novel-techniques-for-zkvm-design/17176
views: 1839
likes: 4
posts_count: 7
---

# Novel techniques for zkVM design

Zero-Knowledge Virtual Machines (zkVMs) are specialized virtual machines designed to execute programs while preserving data privacy through zero-knowledge proofs.

A visual representation of zkVM’s main components and their interactions can be seen below.

[![image](https://ethresear.ch/uploads/default/optimized/2X/8/85426ea778d6cea1fbfb4f6989697a20a199bee7_2_690x299.jpeg)image1500×650 80.3 KB](https://ethresear.ch/uploads/default/85426ea778d6cea1fbfb4f6989697a20a199bee7)

Current zkVM designs prioritize SNARK compatibility, which in principle requires the minimization of the complexity of the circuit representation of their instructions.

Optimizing for SNARK compatibility does enhance the efficiency of the zero-knowledge proof process, but this often involves using a simplified instruction set. Such simplification inherently constrains the zkVM’s capabilities and expressiveness.

Yet, two recent innovations in zkVM optimization techniques are challenging the way we approach zkVM design; Jolt and Lasso.

- Jolt (Just One Lookup Table): Introduces a new front-end technique that can be applied to a variety of instruction set architectures. Instead of converting each instruction directly into corresponding arithmetic circuits, Jolt represents these instructions as lookups into pre-determined tables. This provides a considerable efficiency boost because fetching a precomputed value from a table is usually much faster than performing a complex computation.
- Lasso: Introduces a new lookup argument that uses a predefined table, enabling provers to commit to vectors and ensuring that each entry can be mapped back to this table. This provides an optimization for multiplications-based commitment schemes, creating a dramatically faster prover.

Jolt uses Lasso to offer a new framework for designing SNARKs for zkVMs, and **together they can improve performance, developer experience, and auditability for SNARKs**, thus expanding the horizon for zkVM design.

*Thank you to the [ZKM](https://www.zkm.io/) research team for valuable discussions.*

## Replies

**ghasshee** (2023-10-24):

I have just known the notion of zkVM here.

How do you construct the VM on EVM ?

Or do you have any introductions to zkVM?

---

**Victor** (2023-10-24):

Hi, a zkVM is just a zero-knowledge circuit that runs a Virtual Machine.

Here’s a nice explanation that might help:



      [cryptologie.net](https://www.cryptologie.net/article/564/what-are-zkvms-and-whats-the-difference-with-a-zkevm/)





###



I've been talking about zero-knowledge proofs (the "zk" part) for a while now, so I'm going to skip that and assume that you already know what "zk" is about.
The first thing we need to define is: what's a virtual machine (VM)? In brief, it's a...

---

**ghasshee** (2023-10-25):

I read the instruction but I did not understand why even zkEVM has the name EVM which is not running on ethereum.

Am I wrong ?

It sounds like  you are talking about JVM here for me.

How to embed zkVM into ethereum ?

Or is there any milestone that EVM is going to be zkVM ?

Or are you proposing that EVM should be extended to zkVM in the future ?

Or do you have some contract zkVM on ethereum blockchain already ?

I am not asking the converse, i.e. how to embed EVM into zkVM.

Point out what is the wrong part if my understanding is wrong!

I do not see your motivations, how to use it “on ethereum”.

---

**BirdPrince** (2023-10-26):

So in fact, zkvm is not a virtual machine, but a collective name for a series of virtual machines?

---

**ghasshee** (2023-10-27):

Yes, it’s a virtual machine. I just asked the mechanism how to use Ethereum with zkVM.

I found a motivative article of zkVM.

https://www.zkm.io/whitepaper

> To connect zkMIPS with L2, users need to implement an L2-specific Communication Manager and a validation program for state transition. This program is then compiled to MIPS and executed by a MIPS VM. zkMIPS executes the program and generates ZK proof of execution. The proof can be sent to an on-chain proof verifier, which can trigger a state transition or allow withdrawals if the proof is valid. The main components of the integrated system are illustrated in Figure 3.

section 3.2 of the whitepaper seems to say that

1. A user Alice makes some program that compile into MIPS
2. Alice compiles the program using zkMIPS.
3. Then, zkMIPS publishes a zk-proof of the Alice’s program on some Ethereum Contract

There’s another [good introduction](https://decrypt.co/resources/what-is-zkevm).

It says zkEVM is a kind of zkRollup.

1. A user Alice write a contract and want to execute on zkEVM not on EVM
2. zkEVM compiles the code and publish its execution proof on the main zkEVM’s ethereum contract.
3. Alice can assure that zkEVM definitely executed Alice’s contract.

So, zkEVM is a kind of DApp on ethereum, and it can execute smart contracts “on zkEVM”.

The Contract executions are assured by ethereum.

---

**maniou-T** (2023-10-27):

Congratulations to the ZKM 4 research team for their groundbreaking work in zkVM optimization.  The results speak volumes, not only in terms of advancing the efficiency of zero-knowledge proof processes but also in opening new horizons for zkVM design. The impact of this research is truly commendable. Well done!

