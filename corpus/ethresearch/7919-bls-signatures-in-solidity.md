---
source: ethresearch
topic_id: 7919
title: BLS Signatures in Solidity
author: liangcc
date: "2020-08-31"
category: Tools
tags: [signature-aggregation]
url: https://ethresear.ch/t/bls-signatures-in-solidity/7919
views: 10411
likes: 29
posts_count: 7
---

# BLS Signatures in Solidity

*Thank [@kilic](/u/kilic), [@jannikluhn](/u/jannikluhn), and [@Mikerah](/u/mikerah) for the review and the advice*

This article targets developers who want to perform BLS signature verification in Eth1 contracts.

For readers interested in the BLS signature in Eth2, I highly recommend “BLS12-381 For The Rest Of Us”[[1]](#footnote-22446-1) by Ben Edgington, which provides long but not too long answers to common questions.

The article also assumes the readers heard of the terms like G_1, G_2, and pairings. “BLS12-381 For The Rest Of Us” is also a good source for understanding those.

## Introduction

When we talk about the BLS signature, we are talking about the signature aggregation technique. The BLS here is the name of three authors Boneh, Lynn, and Shacham. [[2]](#footnote-22446-2)

## Which curve should I use?

BLS signature aggregation works on pairing friendly curves. Ｗe have to choose which of the following curves to use.

- alt_bn128: Barreto-Naehrig curve. [3]
- BLS12-381: This BLS is Barreto, Lynn, and Scott. [4]

At the time of writing this document (2020-Aug), we can only use alt_bn128 curve in contracts. The alt_bn128 curve is specified in EIP-196[[5]](#footnote-22446-5) (curve point addition and multiplication) and EIP-197[[6]](#footnote-22446-6) (curve pairing) and introduced in Byzantium hardfork October 16, 2017[[7]](#footnote-22446-7).

The cost is further reduced in EIP-1108[[8]](#footnote-22446-8), and was live on mainnet in Istanbul-fork[[9]](#footnote-22446-9).

The BLS12-381 curve is specified in EIP-2537[[10]](#footnote-22446-10) and expected to go live in the Berlin hardfork[[11]](#footnote-22446-11).

The alt_bn128(BN256) is shown in 2016 to have less than 100-bits of security[[12]](#footnote-22446-12). To target 128-bits security use BLS12-381 whenever possible.

We use alt_bn128 in the examples hereafter.

### alt_bn128, bn256, bn254, why so many names and so confusing?

- Originally named alt_bn128 for targeting theoretic security at 128 bits.
- It then be shown to have security level less than 128 bits[12:1], so people call it bn254.
- Some also call it bn256 for unknown reason.

## Notes on size of the elements

|  | alt_bn128 | BLS12-381 | Note |
| --- | --- | --- | --- |
| F_q | 254 bits (32 bytes) | 381 bits  (48 bytes) | has leading zero bits |
| F_{q^2} | 64 bytes | 96 bytes |  |
| \Bbb G_1 Uncompressed | 64 bytes | 96 bytes | has x and y coordinates as F_q |
| \Bbb G_2 Uncompressed | 128 bytes | 192 bytes | has x and y coordinates as F_{q^2} |

A curve point’s y coordinate can be compressed to 1 bit and recovered by x.

|  | alt_bn128 | BLS12-381 |
| --- | --- | --- |
| \Bbb G_1 compressed | 32 bytes | 48 bytes |
| \Bbb G_2 compressed | 64 bytes | 96 bytes |

## Big Signatures or Big public keys?

This is a decision you’ll face in the project.

Choose either:

- Use \Bbb G_2 for signatures and messages, and \Bbb G_1 for public keys, or
- Use \Bbb G_2 for public keys, and \Bbb G_1 for signatures and messages.

\Bbb G_2 is 128 bytes (`uint256[4]` in Solidity) and \Bbb G_1 is 64 bytes  (`uint256[2]` in Solidity). Also field/curve operations on \Bbb G_2 are more expensive.

The option saves more gas in your project is better.

We’ll use the big public keys in the examples hereafter.

## BLS cheat sheet

We have a curve. The points on the curve can form a subgroup. We define \Bbb G_2 to be the subgroup of points where the curve’s x and y coordinates defined on F_{q^2}. And subgroup \Bbb G_1 with coordinates on F_q.

### Tips

- Field operations: We are talking about arithmetics of field elements F_q or F_{q^2}. F_q can be added, subtracted, multiplied, and divided by other F_q. Same applies for F_{q^2}.
- Curve operations: We are talking about operations of curve elements \Bbb G_1 or \Bbb G_2. An element in \Bbb G_1 can be added to another element in a geometrical way. An element can be added to itself multiple times, so we can define multiplications of an element in \Bbb G_1 with an integer in Z_q[13]. Same applies for \Bbb G_2.

### Pairing function

e:\Bbb G_1 \times \Bbb G_2 \to \Bbb G_T

G_1, G_2 are the generators of \Bbb G_1 and \Bbb G_2 respectively

Pairing function has bilinear property, which means for a, b \in Z_q, P \in \Bbb G_1, and Q \in \Bbb G_2, we have:

e( a \times P, b \times Q) = e( ab \times P, Q) = e( P, ab \times Q)

### Hash function

It maps the message to an element of \Bbb G_1

H_0: \mathcal{M} \to \Bbb G_1

### Key Generation

Secret key:

\alpha \gets \Bbb Z_q

Public key:

h \gets \alpha \times G_2 \in \Bbb G_2

### Signing

\sigma \gets \alpha \times H_0(m) \in \Bbb G_1

### Verification

e(\sigma, G_2)\stackrel{?}{=} e(H_0(m), h)

### Proof of why verification works

e(\sigma, G_2) \\
= e( \alpha \times H_0(m), G_2) \\
= e(  H_0(m), \alpha \times G_2) \\
= e(H_0(m), h)

## Contracts / Precompiles

Developers usually work with a wrapped contract that has clear function names and function signatures. However, the core of the implementation could be confusing. Here we provide a simple walkthrough.

### Verify Single

Below shows an example Solidity function that verifies a single signature. It is the small signature and big public key setup. A signature is a 64 bytes \Bbb G_1 group element, and its calldata is a length 2 array of uint256. On the other hand, a public key is a 128 bytes \Bbb G_2 group element, and its calldata is a length 4 array of uint256.

EIP 197 defined a pairing precompile contract at address `0x8` and requires input to a multiple of 192. This assembly code calls the precompile contract at address `0x8` with inputs.

```auto
function verifySingle(
    uint256[2] memory signature, \\ small signature
    uint256[4] memory pubkey, \\ big public key: 96 bytes
    uint256[2] memory message
) internal view returns (bool) {
    uint256[12] memory input = [
        signature[0],
        signature[1],
        nG2x1,
        nG2x0,
        nG2y1,
        nG2y0,
        message[0],
        message[1],
        pubkey[1],
        pubkey[0],
        pubkey[3],
        pubkey[2]
    ];
    uint256[1] memory out;
    bool success;
    // solium-disable-next-line security/no-inline-assembly
    assembly {
        success := staticcall(sub(gas(), 2000), 8, input, 384, out, 0x20)
        switch success
            case 0 {
                invalid()
            }
    }
    require(success, "");
    return out[0] != 0;
}
```

We translate the above code into math formula. Where the `nG2` is the negative “curve” operation of the G_2 group generator.

e(\text{signature}, neg(G_2)) e(\text{message}, \text{pubkey}) \stackrel{?}{=} 1

If the above formula is not straight forward, let’s derive from the pairing check we usually see. The message here is the raw message hashed to G_1.

e(\text{message}, \text{pubkey}) \\
= e(\text{message},  \text{privkey} \times G_2 ) \\
= e(\text{privkey} \times \text{message},  G_2 ) \\
= e(\text{signature}, G_2)

e(\text{message}, \text{pubkey}) \stackrel{?}{=} e(\text{signature}, G_2)

### Hash to curve

We can choose from Hash and pray approach or Fouque Tibouchi approach:

- Hash and pray approach is easy to implement, but since it is non-constant time to run it has a security issue[14]. Each iteration is expensive in solidity and attacker can grind a message that’s too expensive to check on chain.
- Fouque Tibouchi is constant time, but more difficult to implement.

The following discussion are for hash to G1. For the case of bn254 in G2, see musalbas’s [implementation](https://github.com/musalbas/solidity-BN256G2)

#### Attempts to fix hash and pray

Avg 30k gas for hash and pray https://github.com/thehubbleproject/RedditHubble/runs/1011657548#step:7:35

A sqrt iteration takes 14k gas due to the call to modexp precompile.

Attempt to replace modexp with a series of modmul. optimized cost is 6.7k



      [github.com](https://github.com/ChihChengLiang/modexp)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/5/9/59a07e42bfc92d68aeeefec604314da05c04e808_2_690x344.png)



###



Contribute to ChihChengLiang/modexp development by creating an account on GitHub.










Kobi has a proposal that user provides outputs of modexp and onchain we use 1 modmul to verify. [Created using remix-ide: Realtime Ethereum Contract Compiler and Runtime. Load this file by pasting this gists URL or ID at https://remix.ethereum.org/#version=soljson-v0.5.17+commit.d19bba13.js&optimize=false&gist= · GitHub](https://gist.github.com/kobigurk/b9142a4755691bb12df59fbe999c2a1f#file-bls_with_help-sol-L129-L154)

## Gas Consumption

Post EIP-1108, k pairings cost `34 000 * k + 45 000` gas.

So as the above example, to validate a single signature takes 2 pairings and thus 113000 gas.

Validating n different messages takes n + 1 pairings, which costs `80 000 + 34000*n` gas.

In comparison, ECDSA takes 3000 gas, see `ecrecover`[[15]](#footnote-22446-15).

Here are cases to consider the aggregate signature:

- When there’s only one message, but many signatures to verify. The aggregate signature takes 2 pairings (113000 gas), and it wins ECDSA when you have 38 more signatures to verify.
- When you need to store or log signatures on chain. Storing a word (32 bytes) costs 20000 or 5000 gas, and logging costs 8 gas per byte. The aggregate signature (48 bytes * 1 sig) wins ECDSA (65 bytes * n sigs) easily in this case.

In the Hubble project, we use BLS signature to achieve [3000 TPS on ropsten](https://ropsten.etherscan.io/tx/0x01c83dbce6894360a56dc6810106f47cbc699522a9844e126afc30f51abc0c2e)

## Packages to do BLS

### JavaScript/TypeScript



      [github.com](https://github.com/kilic/evmbls)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/b/9/b9eaaded47444a6dd3e246892c639924fc38bb99_2_690x344.png)



###



Contribute to kilic/evmbls development by creating an account on GitHub.










### Python



      [github.com](https://github.com/ChihChengLiang/bls_solidity_python)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/e/c/ec5ad29e360e93466270fe9252219340fe475572_2_690x344.png)



###



Contribute to ChihChengLiang/bls_solidity_python development by creating an account on GitHub.










## Cookbook

### Aggregations

TODO

- how to create private keys, public keys, and signatures (just listing the formulas should be enough, everyone can then use their favorite library to implement them).
- test data for one cycle (a private key, a public key, a message, and a signature)
- a note on encodings: The solidity code just uses the plain uints, but at least for BLS12-381 there are standardized encodings, aren’t there? Not sure if it makes sense to go into details, but just mentioning that they exist with maybe a link could be helpful
- public key aggregation (my problem basically): My understanding from our discussion yesterday is that it’s not easily possible on-chain with bn128 and public keys from G2. I looked into the EIP fro BLS12-381 and they have a precompile for G2 additions, so with that it should be easy.

1. BLS12-381 For The Rest Of Us - HackMD ↩︎
2. https://www.iacr.org/archive/asiacrypt2001/22480516.pdf ↩︎
3. Pairing-Friendly Elliptic Curves of Prime Order ↩︎
4. https://eprint.iacr.org/2002/088.pdf ↩︎
5. EIP-196: Precompiled contracts for addition and scalar multiplication on the elliptic curve alt_bn128 ↩︎
6. EIP-197: Precompiled contracts for optimal ate pairing check on the elliptic curve alt_bn128 ↩︎
7. Byzantium HF Announcement | Ethereum Foundation Blog ↩︎
8. EIP-1108: Reduce alt_bn128 precompile gas costs ↩︎
9. EIP-1679: Hardfork Meta: Istanbul ↩︎
10. EIP-2537: Precompile for BLS12-381 curve operations ↩︎
11. EIP-2070: Hardfork Meta: Berlin ↩︎
12. https://www.ietf.org/id/draft-irtf-cfrg-pairing-friendly-curves-07.html ↩︎ ↩︎
13. Elliptic curve point multiplication - Wikipedia ↩︎
14. Non-constant time hash to point attack vector · Issue #171 · thehubbleproject/hubble-contracts · GitHub ↩︎
15. https://ethgastable.info/ ↩︎

## Replies

**kobigurk** (2020-08-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/liangcc/48/39_2.png) liangcc:

> Kobi has a proposal that user provides outputs of modexp and onchain we use 1 modmul to verify. Created using remix-ide: Realtime Ethereum Contract Compiler and Runtime. Load this file by pasting this gists URL or ID at https://remix.ethereum.org/#version=soljson-v0.5.17+commit.d19bba13.js&optimize=false&gist= · GitHub

To expand on this a bit - a client library can generate witness values as to the expected result of a sqrt operation. If the sqrt for x exists - great, provide a witness w such that w^2 = x. If not, provide a witness w such that w^2=-x. This exists and works since -1 is not a quadratic residue (doesn’t have a square root) when the field has p  = 3 \pmod 4, and so if x is not a quadratic residue then -x is. p = 3 \pmod 4 is true for both BN254 and BLS12-381.

---

**ralexstokes** (2020-08-31):

i have an example for BLS signature verification (following the scheme used in eth2) here:


      [github.com](https://github.com/ralexstokes/deposit-verifier/blob/8da90a8f6fc686ab97506fd0d84568308b72f133/deposit_verifier.sol)




####

```sol
// SPDX-License-Identifier: The Unlicense
pragma solidity 0.6.8;
pragma experimental ABIEncoderV2;

import { IDepositContract } from "./eth2-deposit-contract/deposit_contract.sol";

contract DepositVerifier  {
    uint constant PUBLIC_KEY_LENGTH = 48;
    uint constant SIGNATURE_LENGTH = 96;
    uint constant WITHDRAWAL_CREDENTIALS_LENGTH = 32;
    uint constant WEI_PER_GWEI = 1e9;

    uint8 constant BLS12_381_PAIRING_PRECOMPILE_ADDRESS = 0x10;
    uint8 constant BLS12_381_MAP_FIELD_TO_CURVE_PRECOMPILE_ADDRESS = 0x12;
    uint8 constant BLS12_381_G2_ADD_ADDRESS = 0xD;
    string constant BLS_SIG_DST = "BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_POP_+";
    bytes1 constant BLS_BYTE_WITHOUT_FLAGS_MASK = bytes1(0x1f);

    uint8 constant MOD_EXP_PRECOMPILE_ADDRESS = 0x5;

```

  This file has been truncated. [show original](https://github.com/ralexstokes/deposit-verifier/blob/8da90a8f6fc686ab97506fd0d84568308b72f133/deposit_verifier.sol)








it uses the EIP-2537 precompiles (which are not *yet* deployed) but may be useful for anyone looking to play around with this stuff.

---

**alonmuroch** (2020-09-01):

I think the the groups where switched, G1 is over Fq and G2 is over Fq^2

Hash: H(m) ∈ G2

sk: a ∈ Zq

pk: a*G1 ∈ G1

sig: a*H(m) ∈ G2

verification: e(sig, G1) =? e(pk, H(m))

---

**mratsim** (2020-09-01):

My two cents:

![](https://ethresear.ch/user_avatar/ethresear.ch/liangcc/48/39_2.png) liangcc:

> Which curve should I use?

This strongly depends on:

- the security level we want.

We don’t protect private keys here so is ~100 bits of security acceptable?

the efficiency we want, as EVM is using 256-bit words, BN254 Fq elements fit in one EVM word while BLS12-381 wille requires 1.5 EVM words. The space wasted grows with curve point:

- On BN254, G1 Affine needs 2 words, G2 Affine needs 4
- On BLS12-381 G1 Affine would require 4 words (2 being half-empty), G2 Affine would requires 8 words (4 being half-empty). We can optimize long-term storage by packing the half empty words.

> BLS cheat sheet

The BLS signature standardized draft spec is there by the way: https://tools.ietf.org/html/draft-irtf-cfrg-bls-signature-02

> Big Signatures or Big public keys?

If that can help, in Eth2 we use small public key and big signature because each individual validator public key must be store in the state while signatures can be aggregated.

> Hash function

If we create something new, I think we should follow the hash-to-curve draft standard. Many blockchains agreed to follow it for BLS signature over BLS12-381 (Algorand, Chia, Dfinity, Eth2.0, Filecoin, Zcash at least and Tezos is exploring it), unless we need it for legacy purposes (Aztec protocol for example), I think all hashing going forward are better served by a standard. It would be easier for optimized software (and hardware?) implementations to emerge.


      ![](https://ethresear.ch/uploads/default/original/3X/a/3/a36eaf5ce9c4569f08c317d6e9adb3a1684222ae.png)

      [IETF Datatracker](https://datatracker.ietf.org/doc/html/draft-irtf-cfrg-hash-to-curve-09)



    ![](https://ethresear.ch/uploads/default/optimized/3X/9/6/96a9b3b540a3661b9506086665dfedad751f6571_2_690x362.png)

###



This document specifies a number of algorithms for encoding or hashing an arbitrary string to a point on an elliptic curve.










Also a hash-to-curve precompile might be necessary there are many costly operations namely:

- Generating an uniform random byte string. (Think something similar to HKDF that repeatedly call SHA256)
- Transforming that byte string into a modular integer in Fq or Fq2 (somewhat fast but still involves modulo)
- Mapping that to the G1 or G2 curves. This involves inversion and square root which are the slowest operations you can have on Fq:

inversion is about 40 to 100 times slower than modular multiplication if non-constant-time (or as slow as square root if constant-time but I don’t think this is needed or expected in the EVM)
- square root is 500 times slower than modular multiplication for BN254 and 620x for BLS12-381 from my measurements.

Last but not least we need to clear the cofactor. While BN curves have no cofactor on G1, BN on G2 and BLS on G1 G2 have a cofactor. Naively this involves a scalar multiplication and this is easily 2500x~5500x slower than a modular multiplication even though BN and BLS cofactors have low Hamming-Weight.

An optimized cofactor clearing can be made cheaper using endomorphism (Fuentes-Castaneda 2011 for BN G2 and Budroni-Pintore 2017 / Wahby-Boneh 2019), but since those are likely provided by all BN254 libraries used for the existing precompiles or BLS12-381 libraries, if we use library calls, we might as well just do a whole hash-to-curve call.

Lastly, I’ve skimmed through the Pixel signature scheme by Dfinity and Algorand and it seemed quite interesting in terms of state size:

- Write-up: https://medium.com/algorand/digital-signatures-for-blockchains-5820e15fbe95
- Paper: Pixel: Multi-signatures for Consensus
- PoC: GitHub - algorand/pixel: Algorand's implementation of pixel consensus signature

They claim 35% reduction of state size and 38% reduction in verification time.

---

Performance figures on Fp, those are from the pairing library I’m building at: [GitHub - mratsim/constantine: Constantine: modular, high-performance, zero-dependency cryptography stack for verifiable computation, proof systems and blockchain protocols.](https://github.com/mratsim/constantine) and should give you an idea of the gap between Solidity and an optimal native implementation. Unfortunately I didn’t implement pairing/verification yet.

The code on Fq / G1 is probably optimal (as in even if you write pure assembly you cannot get more than 3% faster). Note that variable-time inversion can be made 5x~10x faster than constant-time inversion.

[![image](https://ethresear.ch/uploads/default/optimized/2X/7/70f866e94d4ba820f61e0362df0c06740336efb1_2_690x351.png)image1184×604 100 KB](https://ethresear.ch/uploads/default/70f866e94d4ba820f61e0362df0c06740336efb1)

---

**kladkogex** (2020-09-03):

Well - we have them implemented at SKALE


      [github.com](https://github.com/skalenetwork/skale-manager/blob/e02aaa37c37a7d3f2f3214e784307b389b726c4b/contracts/SkaleVerifier.sol)




####

```sol
// SPDX-License-Identifier: AGPL-3.0-only

/*
    SkaleVerifier.sol - SKALE Manager
    Copyright (C) 2018-Present SKALE Labs
    @author Artem Payvin

    SKALE Manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    SKALE Manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with SKALE Manager.  If not, see .
*/
```

  This file has been truncated. [show original](https://github.com/skalenetwork/skale-manager/blob/e02aaa37c37a7d3f2f3214e784307b389b726c4b/contracts/SkaleVerifier.sol)

---

**chgormanMH** (2020-10-25):

I recently submitted an [EIP](https://github.com/ethereum/EIPs/pull/3068/commits) requesting a precompiled contract for the Fouque and Tibouchi hash-to-curve algorithm. I have implemented this both in Solidity and Go for geth. The estimates for gas cost in Solidity is ~140K, while the cost would be closer to 8500 if it were a precompiled contract. The cost is only slightly more expensive than G1 scalar multiplication. This hash-to-curve algorithm would reduce gas cost for verifying BLS signatures using BN256 in Ethereum.

Similar to [EIP-2537](https://eips.ethereum.org/EIPS/eip-2537), if the deterministic field-to-curve algorithm is the precompiled contract, then different users could have different mappings for hash-to-field. This would allow for greater flexibility.

