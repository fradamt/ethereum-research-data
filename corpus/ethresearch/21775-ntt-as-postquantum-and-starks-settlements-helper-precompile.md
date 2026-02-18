---
source: ethresearch
topic_id: 21775
title: NTT as PostQuantum and Starks settlements helper precompile
author: rdubois-crypto
date: "2025-02-18"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/ntt-as-postquantum-and-starks-settlements-helper-precompile/21775
views: 271
likes: 8
posts_count: 1
---

# NTT as PostQuantum and Starks settlements helper precompile

**NTT-EIP as a building block for FALCON, DILITHIUM and Stark verifiers**

With the release of Willow cheap, the concern for quantum threat against Ethereum seems to accelerate. Posts by [Asanso](https://ethresear.ch/t/so-you-wanna-post-quantum-ethereum-transaction-signature/21291) and [PMiller](https://ethresear.ch/t/tidbits-of-post-quantum-eth/21296) summarize those stakes and possible solutions. Those solutions include use of lattice based signatures such as Dillithium or FALCON (the latter being more optimized for onchain constraints), STARKs and FHE. There is a consensus in the cryptographic research community around lattices as the future of asymmetric protocols, and STARKs won the race for ZKEVMs implementation (as used by Scroll, Starknet and ZKsync).

Those protocols have in common to require fast polynomial multiplication over prime fields, and use NTT (a special [FFT](https://vitalik.eth.limo/general/2019/05/12/fft.html) adapted to prime fields). While in the past Montgomery multipliers over elliptic curve fields were the critical target of optimizations (both hardware and software), NTT optimization is the key to a performant PQ implementation.

**Discussion**

In the past Ethereum chose specificity by picking secp256k1 as its sole candidate for signature. Later, after dedicated hardware and proving systems working on other hardwares were realeased, a zoo of EIP flourished to propose alternative curves. There where attempts to have higher level EIPs to enable all of those at once, such as EWASM, SIMD, EVMMAX, or RIP7696 (by decreasing order of genericity and complexity).

Picking NTT as EIP instead of a given scheme would provide massive gas cost reduction for all schemes relying on it.

- pros : massive reduction to all cited protocols, more agility for evolutions.
- cons: requires to be wrapped into implementations, not optimal for a given target compared to dedicated EIP, not stateless.

**Implementation results**

ZKNOX performed an optimized implementation of NTT, using top notch algorithm, Yul and memory hacks to reach a 1.9M NTT polynomial multiplication, 3.6M for a whole EVM-friendly falcon verification (shake being replaced by keccak). While this numbers provide a massive gains compared to previous implementation, it is still expensive. This is why pushing this primitive into nodes as a precompile is now proposed as EIP-9374.

**Link**



      [github.com](https://github.com/ZKNoxHQ/NTT)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/a/6/a65da9de24504c199f850400c7dfa8d0b1f96e71_2_690x344.png)



###



Generic implementation of the Number Theoretic Transform in the context of cryptography applications










**Acknowledgements**

We are grateful to Antonio Sanso for its valuable insights and discussions.
