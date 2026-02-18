---
source: ethresearch
topic_id: 21296
title: Tasklist for post-quantum ETH
author: p_m
date: "2024-12-19"
category: Architecture
tags: [signature-aggregation, post-quantum]
url: https://ethresear.ch/t/tasklist-for-post-quantum-eth/21296
views: 2036
likes: 28
posts_count: 14
---

# Tasklist for post-quantum ETH

## Background

Cryptographically relevant quantum computer, if built, could enable Shor’s algorithm and Grover’s algorithm. These completely break ECDSA / ECDH, and reduce hash function (& cipher) strength from 2^n to 2^\frac{n}{2}

There are some non-obvious parts of ETH which would need to be upgraded.

## What is still OK

- bip39 (pbkdf2-sha512) seems just fine
- eip2333 validator withdrawal keys are also fine!

## What needs upgrading

- bip32 hdkey derivation

Should be replaced by something post-quantum and better (no “non-hardened” keys)
- New scheme could be based on HKDF (like EIP-2333), but not HKDF-SHA256
- Alternative KDF is Blake3 in context mode (pq security is unclear)
- The proposed scheme should support both ECC and new pq mode

Transaction signing

- Should be replaced by lattice-based Falcon (FN-DSA / FIPS-206),
or hash-based Sphincs-plus (SLH-DSA / FIPS-205)
- New keys and signatures will consume more space
- Falcon-1024 has 1.75KB keys and 1.25KB sigs
- SLH-DSA-256 has 48-128B keys and 17-51KB sigs

Sender address recovery

- It was feature of ECDSA (not available in Schnorr, for example)
- Perhaps txs (and not sigs) should encode sender addresses

Address format

- Currently it’s 40 hex characters, keccak256(pubkey)
- keccak256 should be replaced by keccak512 / sha3-512 / sha512 / blake3-512
- How does Grover algo affect brute-forcing of addresses? Should 40 characters be upped to 80-128?
- Longer address formats should probably use something like bech32 for checksumming & human-friendliness
- How would new addresses interop with old addresses / EVM?

Encrypted wallets

- Should upgrade from AES-128 to AES-256 or chacha20
- hmac-sha256 should upgrade to hmac-sha512 / kmac / blake3-512 (keyed mode)

KZG EIP-4844 verification

- Should be replaced by a post-quantum scheme
- Algorithms are unclear for now, any suggestions?

EVM 0x20 opcode (KECCAK256)

- Should be replaced by keccak512 / sha3-512 / sha512 / blake3-512 (new opcode)

EVM precompile for ECRECOVER

- See address recovery above

EVM precompiles for BN / BLS / KZG

- Should be replaced by newer schemes (unclear which ones?)
- No more Groth16, vanilla PLONK, Marlin, BulletProof

Consensus layer signature aggregation

- Currently aggregates signatures of all validators once per epoch (6 mins)
- More than 1M signatures right now?
- Algorithms are unclear for now, any suggestions?

ZK-rollups (non STARK)
Anything else?

## Final thoughts

I’m confident all of these problems can be solved even in limited time. Let’s start solving them.

If such computer appears soon, it’s possible to do Vitalik’s trick ([How to hard-fork to save most users’ funds in a quantum emergency](/t/how-to-hard-fork-to-save-most-users-funds-in-a-quantum-emergency/18901)): freeze all accounts and leverage BIP39 with ZK-proofs to recover funds into new pq scheme.

## Replies

**WizardOfMenlo** (2024-12-19):

I might point out that while Grover gives an asymptotic sqrt advantage, currently the consensus is that the attack concrete costs are large enough that it is not much better than classical methods.

See (I can’t link) csrc nist gov/csrc/media/Events/2024/fifth-pqc-standardization-conference/documents/papers/on-practical-cost-of-grover.pdf for example.

This is why the NIST-PQC standard still recommends AES-128 as the symmetric component in most of these ciphers.

---

**p_m** (2024-12-19):

That’s NIST opinion. They also don’t like hybrids (ecc + pq), which others prefer.

Australian ASD, on the other hand, prohibits SHA256, AES-128, etc after 2030: https://www.cyber.gov.au/resources-business-and-government/essential-cyber-security/ism/cyber-security-guidelines/guidelines-cryptography

---

**pcaversaccio** (2024-12-19):

Some additional points:

- Some chains (e.g. Polygon or ZKsync) have already implemented RIP-7212, i.e. the P256VERIFY precompile at address 0x100 for the non-Ethereum-native NIST P-256 elliptic curve (also known as secp256r1). Other chains will follow in the near future and even Ethereum mainnet will eventually ship it probably.
- Node discovery (DevP2P): The current Kademlia DHT employs secp256k1 for node identity, which would require quantum-resistant replacements to ensure security. Handshake protocols and all p2p encryption mechanisms must be upgraded to post-quantum schemes. Additionally, Ethereum Node Records (ENR) would need new identity schemes, and - if I’m not completely wrong - the Discovery v5 protocol would require significant modifications to support these changes. Ethereum relies on the Node Discovery v5 protocol for bootstrap and peer discovery. Furthermore, IMHO (also not 100% sure) the boot node infrastructure needs a comprehensive security reassessment to address vulnerabilities in a post-quantum environment.
- Light client sync protocols need quantum-resistant proofs.

---

**rdubois-crypto** (2024-12-19):

Some additional thoughts:

- if the hash function property we need is collision resistance, difficulty is n/2, quantum computing reduces it to n/3, so 384 bits might be enough (while 512 could still be a conservative choice).
- the end game being ZK, while replacing keccak, a ZK-friendly (ie NTT friendly) hash function might be pushed instead of larger keccak sizes.
- RIP7212 has been pushed because of Passkey/FIDO, for sure one standard will be pushed as a replacement when the threat is considered high enough.
- there is a potential key recovery mechanism in FALCON.
- instead of pushing a precise lattice candidate, which might change, the efforts could focus on NTT, both a building block for ZK schemes and PQ-sig schemes. This precompile could provide  large speed-ups for STARKS (potential replacement for KZG).
- While there is a sudden FUD around quantum threat, which shall be taken seriously, ciphering is considered from today because of Forward secrecy. The transition must be prepared, but authentication is less threatened. (looking at GAFAM, ciphering like in e-message already migrates, not auth.). There is a lot to do and we shall prepare those rn, sustainability of solutions shall be preferred.

---

**frangio** (2024-12-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/p_m/48/18530_2.png) p_m:

> EVM 0x20 opcode (KECCAK256)
>
>
> Should be replaced by keccak512 / sha3-512 / sha512 / blake3-512

I’m not sure if this is what you were suggesting but replacing the opcode in place is not a good idea, it’s better to have lower security contracts than completely broken ones (in the sense that they can’t even run because the hash function was rug pulled). We should add a new opcode for a higher security hash function and let developers and users migrate. The same applies to other opcodes and precompiles.

---

**p_m** (2024-12-19):

No replacement. Just introducing new ones. I agree.

---

**vbuterin** (2024-12-19):

> bip32 hdkey derivation

Probably just say “hardened keys only” because it’s not clear how to do non-hardened derivation as that depends on having a homomorphism. Something lattice-based eventually?

> Transaction signing

User chooses what sig algo they want, using account abstraction. See [EIP-7701: Native Account Abstraction with EOF](https://eips.ethereum.org/EIPS/eip-7701) for a reasonably simple way to do this.

> Sender address recovery

Agree we should dump this and just include sender address in the tx. The AA standards (eg. EIP-7701) already do this.

> Address format

Grover reduces brute-force cost from 2^160 to 2^80, still extremely high esp if you take into account quantum computers realistically being much slower per computation step. So, not worried here.

> Encrypted wallets

Agree it’s worth looking into.

> KZG EIP-4844 verification

STARKed Merkelized erasure coded blobs.

> EVM 0x20 opcode (KECCAK256)

I don’t think 256-bit hashes will be a problem, same reason as why addresses are ok

> EVM precompile for ECRECOVER
> EVM precompiles for BN / BLS / KZG

Yeah we will phase ECDSA out entirely, so at some point just replace this with EVM code for backwards compatibility and dump the precompile.

> ZK-rollups (non STARK)

Replace with STARKs, and consider adding in-protocol aggregation to make it more cost-friendly in the protocol.

---

**p_m** (2024-12-19):

For bip32 i’ve meant that if wallets would be switching to pq sigs, there would be no need in bip32, which even in hardened version rejects keys over curve order. If we modify bip32 to remove this check, it would no longer be bip32. And pqc may need keys larger than amount of bytes bip32 can produce.

Better to just invent a completely new scheme which plays nicely with both ECC and PQC. EIP2333 is a great starting point.

Non hardened version of course belongs to trash bin. Never liked it much bc of address associativity. In pq setting it’s particularly bad.

---

**guorong009** (2025-02-21):

What could be tasklist for Ethereum networking?

Ethereum networking depends on **devp2p** and **libp2p**.

They depend on non-PQ cryptography, like ECC.

Maybe, networking stuff does not belong here?

Or, should they be considered after the PQ transition of tasklist above?

---

**p_m** (2025-02-21):

[@pcaversaccio](/u/pcaversaccio) mentioned it above

---

**rdubois-crypto** (2025-02-23):

For the recovery part, we implemented the falcon recovery version in solidity, here:

[ETHFALCON/src/ZKNOX_falconrec.sol at fa358d808952ee6b35fb9239f5761a0b53b705f8 · ZKNoxHQ/ETHFALCON · GitHub](https://github.com/ZKNoxHQ/ETHFALCON/blob/fa358d808952ee6b35fb9239f5761a0b53b705f8/src/ZKNOX_falconrec.sol).

This would require to modify the way to hash a public key of course. For performances the value of the hash of public key in the ntt domain is chosen here. (avoiding a NTTinv operation).

---

**Perun** (2025-02-27):

> Probably just say “hardened keys only” because it’s not clear how to do non-hardened derivation as that depends on having a homomorphism. Something lattice-based eventually?

We had a paper that shows how to do this with lattices: [Deterministic Wallets in a Quantum World](https://eprint.iacr.org/2020/1149). And there was also some work solving this with Isogenies: https://dl.acm.org/doi/10.1145/3634737.3657008

---

**Quamtum** (2025-07-27):

Hi everyone, as I was reviewing this post including reply and propositions from folks, unfortunately most encryption synopsis that use a randon value as bigInt to reach eventually a stance satisfying the total space,  variable and features to use from that protocole in relation with elliptic curves, actually offer a framework to precisely offer path in order to break the algorithm as EDCSA-384, 256, those aren’t bulletproof and can be challenged…

To reduce potential exposition to risk, using a scheme as color pixBits val to distribute a shared patterns across the network and so by using this methodology, you can attribute and tag subsequent cells_groups(units)_extension_unknown(slots) and so on with a chained link. This setup is still using zero-trust as each layers (clusters) are isolated and only a X amount as validator or processor have such privileges as to produce trust similar as AURA from brightID, and partially the ENS metaphore that encapsulate or wrap your address.

It’s important to note, that this system is using a no-competition clause as no-race condition can be set or happen, as the curriculum is a val with variable shared dependencies where this can either form a singular link as one United under the core system, where multimodal and adjacent cells are working in 3D, or true parallel and serial path reduced to bare minimal so sharing the overall risk and increasing the level of security.

