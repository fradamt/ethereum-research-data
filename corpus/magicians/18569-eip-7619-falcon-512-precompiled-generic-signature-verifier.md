---
source: magicians
topic_id: 18569
title: EIP 7619 - Falcon-512 Precompiled - Generic Signature Verifier
author: eum602
date: "2024-02-09"
category: EIPs > EIPs core
tags: [precompile, signatures, postquantum]
url: https://ethereum-magicians.org/t/eip-7619-falcon-512-precompiled-generic-signature-verifier/18569
views: 1215
likes: 6
posts_count: 6
---

# EIP 7619 - Falcon-512 Precompiled - Generic Signature Verifier

What we propose?

In this topic we bring a proposal to introduce a precompile to verify a **generic** postquantum Falcon-512 signature.

Why Falcon Signatures?

- Falcon algorithm is a good postquantum candidate algorithm for ethereum because of the short size of the produced signature (~667 bytes) and public key (897 bytes).
- The way we propose it allows to handle such signatures at a contract level so encapsulating the feature at the execution layer.
- Additionally the benchmarks we performed (results are presented in the proposed EIP) shows the low consumption of gas (around 1465 as a base cost plus 6 gas per word in the message to sign. For instance to verify a message of 33 bytes the cost of verification in the precompile would cost  1663 units of gas).
- The method doesn’t replace secp256k1 elliptic curve but instead it is an option that can work together with such algorithm. For example a transaction is still signed following the ecdsa-secp256k1 signature algorithm while also embedding a falcon signature in a contract call for an additional authentication.
- Falcon-512 could be a good fit with account abstractions (EIP-4337)

Why a precompiled contract for Falcon is a good option?

- We implemented the falcon signature algorithm directly in solidity, which proved to be unfeasible due to the high consumption of gas (Implementation in solidity here)
- Implementing the same feature in two clients Hyperledger Besu and Geth turned to be way cheaper, even less than ecrecover.

Additional References:

- One of our initiatives using the proposed Falcon-512 precompiled Link

## Replies

**abcoathup** (2024-02-09):

How is this different from EIP7592: Precompile for Falcon signature verification?

https://github.com/ethereum/EIPs/pull/8103/files

---

**eum602** (2024-02-09):

Hi [@abcoathup](/u/abcoathup) the difference relies in the message size. Our proposed precompile doesn’t limit the size of the message (in the other proposal the message is limited to 256 bits). For our proposal, a particular case is just setting a message of 32 bytes (e.g. a digest) but in other cases it is up to the contract layer decide the size of the message, for example a digest of 384 bits. Since message is dynamic the gas cost is dynamic as well. It was calculated by using a [geth implementation](https://github.com/lacchain/go-ethereum/pull/2/files) and summarized results [here](https://github.com/lacchain/benchmarking/tree/falcon_precompiled) that the base cost of executing a generic verification of a falcon signature is 1465 units of gas plus 6 units of gas per word of message.

---

**rdubois-crypto** (2024-02-15):

Hi, this implementation is a straightforward translation of a C code, which doesn’t exploit at all the finite field operations avalaible in solidity. As such it cannot be concluded at all that it shows the infeasibility of FALCON in solidity.

For instance :

- ```
function mq_add(uint32 x, uint32 y)
```

can trivially be replaced by a single addmod instruction, it is an emulation over a 32 bit architecture of a modular addition, same for sub

- the use of a montgomery representation is totally useless as mulmod is only 3 gas cost, here it is several hundreds of gas per modular multiplication. Which is the critical part of the code (more than 90% is the computation overt the lattice).

Lattice computations require larger amount of space, but are faster than elliptic curve operations. (Look at bench here and there, falcon is faster than ECDSA). So it should be feasible to have implementation in the order of magnitude of emulated non native ecc (ed25519, secp256r1).

That being said, having a PQ precompile would be a good idea. We should wait for available implementations in devices (smartphones and PC), cause the process of standardization is still very wet.

---

**shemnon** (2025-09-10):

I’m interested in reviving this proposal and have some comments:

### (a) ABI encoding heading

No other mainnet precompiles utilize the 4 byte Solidity function selector, can it be removed?

### (b) Fixed-width encoding

The public key is fixed width, and there is a standardized fixed with signature format (limit size to 666 bytes and pad with zeros). Could we change the ABI to become a plain concatenation?

```auto
[pubkey:897 bytes][signature: 666 bytes][message: remainder]
```

The length of the input buffer will become a part of the calculations for the underlying calculations, but this matches how other hash algorithms.

Also, given what I know about the algorithm the input may be given a per-signature salt to the message, so providing the message instead of a hash of the message looks to be the correct.

### (c) Return Value

Can the return value be set to 32 byte padded 1 for success and 32 byte zero for failure? While those values match the underlying PQClean implementation (0 for success, -1 for any and all failure) this return doesn’t match with the P256 precompile return of 1 for success, matching a boolean “success.”

But we should not follow RIP-7212’s guide and make failure/rejection an empty string, contracts and RPC probing will use that to determine if the precompile is present or not.  The zero-success is also especially dangerous for code that will blindly copy the return value without considering the length, especially in the case where the precompile is not deployed and a contract accidentally calls. Because of this zero and empty responses should be reserved for failures.

---

**eum602** (2025-09-10):

Hi [@shemnon](/u/shemnon) , sure, I see it reasonable. Those changes can be applied.

