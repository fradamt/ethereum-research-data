---
source: ethresearch
topic_id: 7450
title: When do we need cryptography in blockchain space?
author: Rbchi1
date: "2020-05-21"
category: Cryptography
tags: []
url: https://ethresear.ch/t/when-do-we-need-cryptography-in-blockchain-space/7450
views: 3307
likes: 6
posts_count: 6
---

# When do we need cryptography in blockchain space?

I want to check when will we need cryptography in blockchain field.I list all I know here:

1. Consensus algorithm
2.Signing transaction (including different kinds on digital signature )
3.Layer2’s verification on Layer1
4.Verifying the cross chain tx
5.Rollup with different digital signature
6.Cross-shard

Is there anything I miss ?

## Replies

**vbuterin** (2020-05-21):

### Consensus-layer:

- Hashes for Merkle trees
- Signatures for transactions
- Signatures for blocks in PoS
- Possibly, polynomial commitments as a replacement for Merkle trees
- ZK-SNARKs/STARKs to enable more efficient client-side verification
- Private information retrieval for privacy-preserving light clients

### Application-layer

- ZK-SNARKs for scaling (eg. ZK rollup)
- ZK-SNARKs for privacy (eg. Tornado Cash)
- Other forms of cryptography for privacy (confidential transactions, bulletproofs, ring signatures…)
- Group homomorphisms for stealth addresses and deterministic wallets
- Multi-party computation for privacy (in some situations ZK-SNARKs are not sufficient, particularly when you want to maintain state that no one can decrypt)
- In the future, obfuscation: How obfuscation can help Ethereum

---

**Rbchi1** (2020-05-22):

Thanks Vitalik

it seems that the most cryptography in Consensus layer is hard code. Could Ewasm help ?

And could application layer get more flexibility for programming ? For example,zk rollup is hard to interact with general smart contract on Eth so they need to invent new lang like Zinc.

---

**vbuterin** (2020-05-22):

Ewasm could certainly be used to write cryptography more efficiently, though in many cases it’s not needed; rather, what’s needed is for EVM to get better support for big-integer operations, as that’s where the bulk of the cost of a lot of cryptographic operations comes in.

> For example,zk rollup is hard to interact with general smart contract on Eth so they need to invent new lang like Zinc.

Yeah, this is a problem. The EVM is not very friendly to living *inside of* cryptographic systems like ZK-SNARKs (or STARKs, or MPC, or FHE). Ewasm is a little better, but the best would be a VM specifically designed for ZK-friendliness.

---

**Rbchi1** (2020-05-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> big-integer operations,

Gotcha,thanks. What is the big-integer operations? I would take more study about that .

A VM especially for Zk is a solution but it is possible that a VM could read different kinds of cryptography in specific code format ?

---

**vbuterin** (2020-05-24):

Basically arithmetic (add, multiply, modulo, divide) with very big numbers, usually 80-2000 digits.

> A VM especially for Zk is a solution but it is possible that a VM could read different kinds of cryptography in specific code format ?

VMs that specifically support certain cryptographic operations are definitely possible.

