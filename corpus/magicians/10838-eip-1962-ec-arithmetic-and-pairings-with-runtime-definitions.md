---
source: magicians
topic_id: 10838
title: "EIP-1962: EC arithmetic and pairings with runtime definitions for Shanghai-candidate"
author: weikengchen
date: "2022-09-13"
category: EIPs
tags: [evm, opcodes, zkp, shanghai-candidate]
url: https://ethereum-magicians.org/t/eip-1962-ec-arithmetic-and-pairings-with-runtime-definitions-for-shanghai-candidate/10838
views: 1615
likes: 0
posts_count: 2
---

# EIP-1962: EC arithmetic and pairings with runtime definitions for Shanghai-candidate

EIP-1962 is to add general EC arithmetics support for SNARK proof verification. Compared with EIP-2537, it is not limited to the BLS12-381 curve, but also other curves.

EIP-1962 is certainly a complicated one, but there is something that EIP-1962 can do, but EIP-2537 alone is insufficient. Here, let me cite three examples from the work from our teams.

- verification of ed25519 signatures in SNARK: when we do such verification on BLS12-381 or BN254, we have to resort to nonnative field arithmetics, which is very costly. If we use some application-specific curves, such as Yafa-108/146 in the following note, then the cost of scalar multiplication on ed25519 drops significantly.

https://eprint.iacr.org/2022/1145.pdf
- See page 2 and 3 for some key experiment results, and see Section 1 for a classification of different solutions for such signature verification.

verification of secp256k1 signatures in SNARK: as it is observed before, secq256k1 (“q”) can verify secp256k1 efficiently, and secp256k1 (“p”) can verify secq256k1 efficiently, which forms a cycle for proof systems based on inner-product arguments to work

- https://eprint.iacr.org/2022/1079.pdf
- See Section 1.4 for a technical design as well as some “personal opinions” on why secp256k1 is important

computation over SNARK-friendly twisted Edwards curves of BN254 and BLS12-381, such as Jubjub, Baby Jubjub, and others, which may be useful for interoperability with other systems, here, between SNARK-based L2 and L1 as well as zkBridges

- Same link above
- See page 17 for some discussion about these SNARK-friendly primitives

In other words, the necessity about EIP-1962 (instead of EIP-2537) is now materially different from the use cases cited in EIP-1962.

Since this EIP was previously tentatively approved, and we know EIP-2537, which is for BLS12-381 is “likely going to be merged” since it already stays in the codebase, and EIP-1962 shares a lot of code with EIP-2537, maybe, it is a good idea to expand EIP-2537 to the scope of EIP-1962.

Even if this is unlikely going to be included in the Shanghai candidate due to its complexity, I feel it useful to bring this one up “every” one or two years to revisit.

## Replies

**weikengchen** (2022-09-13):

Related: EIP-2537 seems to move forward a lot:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/peterccliu/48/6165_2.png)
    [EIP-2537 (BLS12 precompile) discussion thread](https://ethereum-magicians.org/t/eip-2537-bls12-precompile-discussion-thread/4187/21) [EIPs](/c/eips/5)



> Quick update in May 2022:
> Summary: The implementation of EIP-2537 has been completed and is now in go-ethereum codebase— it is only pending activation of this functionality.
> Next steps: Enable the precompiles by editing /core/vm/contracts.go, similar to what is done for Byzantine/Istanbul/Berlin:
>
> Create a new default set of pre-compiled Ethereum contracts used in the next release, including the new precompiles of EIP-2537.
> Modify init() and ActivePrecompiles() functions to activate the new p…

