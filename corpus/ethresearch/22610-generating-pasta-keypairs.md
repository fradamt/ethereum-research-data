---
source: ethresearch
topic_id: 22610
title: Generating Pasta keypairs
author: "71104"
date: "2025-06-14"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/generating-pasta-keypairs/22610
views: 353
likes: 2
posts_count: 5
---

# Generating Pasta keypairs

Helloes,

I’m trying to build a brand new blockchain (feel free to ask me why, I’m happy to provide info about my project) and I’m prototyping the first node implementation in Rust.

This blockchain will be capable of executing smartcontracts compiled as WebAssembly modules, generating a zk-SNARK proof of their correct execution. I’m quite new to zk-SNARKs but after plenty of exploration I believe the best scheme to use is Halo2, which doesn’t need any trusted setup and also supports recursive proofs, allowing me to implement zk-rollups.

I understand that if I use Halo2 then:

- EdDSA,
- Pallas/Vesta (aka Pasta) elliptic curves,
- and the Poseidon hash function optimized for Pasta curves

are practically mandated choices, as using any other curves and hash functions would cause the size of all SNARK circuits to blow up.

All that being correct, I’m going to use crates like `halo2_proofs`, `halo2_gadgets`, `halo2_poseidon`, as well as `ff` and `pasta_curves`. My first question is: **where do I find a Rust example that generates an EdDSA keypair?** Are the `ff` and `pasta_curves` crates sufficient to generate a keypair?

Thanks in advance!

## Replies

**71104** (2025-06-15):

For anyone reading, I’ve gathered much more information about this. Here’s what I’ve learned.

## 1. Key Derivation

In elliptic curve cryptography, key derivation is pretty much always the same and independent of the signature scheme. It’s based on the **discrete logarithm problem**, and once the specific curve is defined, deriving the keys is pretty straightforward. The discrete logarithm problem says that given:

- a very large prime p that’s specific to the curve,
- a field F_p with arithmetic operations modulo p,
- an arbitrary value x \in F_p,
- a point P expressed as a pair of affine coordinates (or alternatively as a triple of projective coordinates) on F_p,
- a special sum operation between points that I’m not delving into here but it’s provided in the pasta_curves crate,
- and Q = x \cdot P (meaning that P is added up x times with the aforementioned sum operation),

**it’s infeasible to recover x from Q knowing only P**. So key generation in elliptic curve cryptography is pretty straightforward:

- come up with a random x and that’s the private key;
- the public key is P = x \cdot G, with G being a special point of the curve known as the generator;
- convert P to affine coordinates to reduce it to a pair of 256-bit numbers;
- use only the X coordinate to communicate the public key, as the Y coordinate is obtained by simply evaluating the elliptic curve in X; this way the public key is a single 256-bit number.

With all this, the answer to my original question is: **yes, the `ff` and `pasta_curves` crates are more than enough to derive Pasta keypairs** (if one is willing to take the risk of implementing a minor amount of cryptography).

## 2. Signature Scheme

I’ve learned that EdDSA is not even the best choice for SNARK-friendliness. Schnorr is better! (AIUI Schnorr is more general than EdDSA but don’t quote me on this.)

There are some crates to deal with Schnorr but then again, once you have things like `ff` the math behind it seems to be so straightforward that it’s actually worth taking the risk of implementing some amount of cryptography first-hand rather than the burden of an extra dependency (that may grow stale, may be no longer maintained, etc.).

I think it’s worth summarizing the Schnorr signature and verification algorithms here for anyone interested. **Should anyone notice mistakes please call them out and I’ll edit.**

### Definitions

- G = the generator point of the curve.
- p = a large prime specific to the curve.
- n = a secret random nonce in F_p.
- m = the message to sign (it should also contain its own nonce / timestamp / whatever to prevent replay attacks).
- x = the private key of the signer.
- P = the public key of the signer.
- H = a suitable hash function (Poseidon is recommended for zk-SNARK friendliness).

### Schnorr Signature

- Generate the nonce n (such that n \in F_p) with a cryptographic PRNG.
- Compute the nonce commitment point:

N = n \cdot G

- Compute the challenge hash:

c = H(N || P || m)

- Compute the response scalar:

s = n + c \cdot x \mod{p}

- The signature is the pair

(N, s)

Note: x remains secret and unrecoverable from (N, s) because:

- n is unrecoverable from N due to the discrete logarithmic problem;
- if you don’t know n you can’t solve the s equation for x.

**WARNING #1**: it’s important that n remains secret, otherwise anyone can get your private key by solving:

\begin{aligned}
s &= n + c \cdot x \mod{p} \\
x &= \frac{s - n}{c} \mod{p}
\end{aligned}

where the division over F_p is performed by multiplying by the inverse modulo-p of c.

**WARNING #2**: NEVER reuse the same random n to sign two different messages, otherwise full private key recovery becomes possible by solving:

\begin{aligned}
s_1 &= n + c_1 \cdot x \mod{p} \\
s_2 &= n + c_2 \cdot x \mod{p} \\
\end{aligned}

\frac{s_1 - s_2}{c_1 - c_2} = \frac{n + c_1 \cdot x - n - c_2 \cdot x}{c_1 - c_2} = x \cdot \frac{c_1 - c_2}{c_1 - c_2} = x

Note that doesn’t work if c_1 = c_2 because in that case s_1 = s_2 and you end up with

\frac{s_1 - s_2}{c_1 - c_2} = \frac00

which is an indeterminate form. So a single signature for a given c does not allow private key recovery.

So make sure n is fresh (and cryptographically secure) for every new signature.

Signing the same message with two different nonces is okay.

### Schnorr Verification

1. Compute the challenge hash:

c = H(N || P || m)

1. Check the equation:

s \cdot G \stackrel{?}{=} N + c \cdot P

## 3. Conclusions

With all this we have two fundamental cryptographic primitives (a hash and a signature scheme) that are highly efficient for zk-SNARK circuits, especially Halo2 since we’re using the same field. This probably makes Poseidon and Poseidon-Schnorr the best choices for starting a new blockchain project today since Halo2-friendliness buys us the ability to construct recursive proofs (and therefore zk-rollups). Moreover, Halo2 is significantly easier to use than other schemes because it doesn’t require any trusted setup.

---

**jonhubby** (2025-07-03):

Hey 71104, thanks for sharing all this really helpful breakdown, especially for folks just starting to explore zk-SNARKs and Halo2.

I’m also looking into using Halo2 for a similar purpose (WASM execution + zk proof of correctness), and your notes clarified a few things I was still fuzzy on, especially around the key derivation using Pasta curves and the benefits of Poseidon + Schnorr over EdDSA in this context.

Quick question have you found or written any concrete examples in Rust for doing the actual Schnorr signing and verification using pasta_curves and ff? I get the math side now, but having a minimal working example to start from would definitely help avoid mistakes when translating theory into code.

Thanks again for documenting your findings.

2/2

---

**71104** (2025-07-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/jonhubby/48/20094_2.png) jonhubby:

> I’m also looking into using Halo2 for a similar purpose (WASM execution + zk proof of correctness),

Interesting, this is precisely what I’m going to be doing for *my* project as well! I’m building a new L1 blockchain whose smartcontracts will be compiled to WASM and their execution will be proven in Halo2 (feel free to ask me my motivations etc., I’m happy to provide more info about my project.)

What are you working on?

![](https://ethresear.ch/user_avatar/ethresear.ch/jonhubby/48/20094_2.png) jonhubby:

> and your notes clarified a few things I was still fuzzy on, especially around the key derivation using Pasta curves and the benefits of Poseidon + Schnorr over EdDSA in this context.

Yep. And I’ve gathered even more information about the matter, I’ve now learned that Schnorr provides two more important advantages over EdDSA:

- EdDSA is vulnerable to malleability attacks if care is not taken on the verifier side (see here for details). Schnorr, on the other hand, is non-malleable.
- The Schnorr scheme makes signature aggregation possible, a feature that EdDSA doesn’t have.

Besides, EdDSA is pretty much always used with Curve25519 which is somewhat worse than Pallas & Vesta in terms of entropy of the scalars (such as the private key and secret nonces). The order of the scalar field of Curve25519 is a large prime multiple of 8, meaning that in order for the whole scheme to be secure you need to perform a specific clamping procedure whenever you generate a random scalar. This clamping procedure is defined by Ed25519 and implemented e.g. [here](https://docs.rs/curve25519-dalek/latest/src/curve25519_dalek/scalar.rs.html#1386-1391). As you can see, it zeroes the three least significant bits. Not a big deal, you still have 252 bits of entropy, but Pallas & Vesta don’t have that problem because the order of their respective scalar fields are large primes. So **the two Pasta curves allow for slightly more entropy than Curve25519**.

(Unfortunately I’m going to be unable to leverage this benefit in my project because I’m using mTLS for authentication which doesn’t support Schnorr or Pallas, so the private keys of my blockchain need to be usable on both curves, so my key derivation process actually performs Ed25519 clamping and loses 3 bits of entropy.)

![](https://ethresear.ch/user_avatar/ethresear.ch/jonhubby/48/20094_2.png) jonhubby:

> Quick question have you found or written any concrete examples in Rust for doing the actual Schnorr signing and verification using pasta_curves and ff?

… yes and no. I’m still working on the low-level protocol, things like authenticating the nodes, joining and leaving the network, etc. so the signatures I’m dealing with right now are not going to be verified in zero-knowledge proofs and therefore they don’t need to use the Poseidon hash. SHA3 is generally more secure and also much easier to use than Poseidon. The latter is a 128-bit hash, potentially vulnerable to post-quantum attacks, and it has different usage modes and APIs for different use cases, e.g. fixed-length messages vs. variable-length ones… I’ve tried using the `halo2_poseidon` crate and it was an absolute mess.

But I *am* using the Schnorr scheme! So far I’ve implemented two types of signatures:

- generic signatures for protobuf messages using Schnorr over Pallas with SHA3;
- the dual-Schnorr signature scheme that I use for authenticating the nodes of the network via mTLS certificates (I discussed it in this thread but there have been developments since then, I should update it).

Both implemented here: [node/src/keys.rs at 25e98380d4fe258c707f06298efc25059f858199 · dotakon-mirror/node · GitHub](https://github.com/dotakon-mirror/node/blob/25e98380d4fe258c707f06298efc25059f858199/src/keys.rs)

Notable parts:

- Generic Schnorr-Pallas-SHA3 signing: node/src/keys.rs at 25e98380d4fe258c707f06298efc25059f858199 · dotakon-mirror/node · GitHub
- Generic Schnorr-Pallas-SHA3 verification: node/src/keys.rs at 25e98380d4fe258c707f06298efc25059f858199 · dotakon-mirror/node · GitHub
- “Dual-Schnorr” signing scheme: node/src/keys.rs at 25e98380d4fe258c707f06298efc25059f858199 · dotakon-mirror/node · GitHub
- “Dual-Schnorr” signature verification: node/src/keys.rs at 25e98380d4fe258c707f06298efc25059f858199 · dotakon-mirror/node · GitHub
- If you’re curious about certificate generation: node/src/ssl.rs at 25e98380d4fe258c707f06298efc25059f858199 · dotakon-mirror/node · GitHub
- For key derivation, since I had to do Ed25519 clamping anyway as explained above, I made a hybrid process using the ed25519_dalek crate as well as my own Pallas point multiplication with the pasta_curves crate. The full process runs here: node/src/keys.rs at 25e98380d4fe258c707f06298efc25059f858199 · dotakon-mirror/node · GitHub (the Pallas point multiplication is at line 71).

This is probably not quite what you were looking for since I’m using SHA3 instead of Poseidon… (and I’m not making a Halo2 circuit out of it anyway, for now)

The lesson I’ve learned is that Poseidon is so complicated that it only makes sense inside Halo2 circuits, so the whole `halo2_poseidon` crate is not really the best in terms of usefulness. When I get to the point of running WASM programs in Halo2 I’ll actually use the Poseidon implementation provided in the `halo2_gadgets` crate (it’s a crate containing several reusable circuit components, such as Poseidon hashing: [halo2/halo2_gadgets/src/poseidon.rs at 8056703404299dd0a1e381ecfaa780f891dfc392 · zcash/halo2 · GitHub](https://github.com/zcash/halo2/blob/8056703404299dd0a1e381ecfaa780f891dfc392/halo2_gadgets/src/poseidon.rs)).

---

**71104** (2025-07-31):

Hey [@jonhubby](/u/jonhubby), I made some progress on my project and wanted to let you know that I’ve actually converted most of the code base to Poseidon hashing! It’s much more zk-SNARK-friendly this way, and since you were interested in the Poseidon-Schnorr signature scheme – here it is!

Signing: [node/src/keys.rs at 56daa66124187fda5387c475b79822a4ac66d67e · dotakon-mirror/node · GitHub](https://github.com/dotakon-mirror/node/blob/56daa66124187fda5387c475b79822a4ac66d67e/src/keys.rs#L353)

Verification: [node/src/keys.rs at 56daa66124187fda5387c475b79822a4ac66d67e · dotakon-mirror/node · GitHub](https://github.com/dotakon-mirror/node/blob/56daa66124187fda5387c475b79822a4ac66d67e/src/keys.rs#L368)

The big catch is that Poseidon is mostly tailored to hashing **fixed-length messages**, and Halo2’s crates actually don’t even provide the API to hash variable-length ones. That is because zk-SNARKs have fixed size (circuits can’t loop indefinitely, the execution trace encoded in the polynomials must be a fixed-size table). Interestingly, the [Poseidon paper](https://eprint.iacr.org/2019/458.pdf) did define an algorithm for variable-length hashing (section 4.2, “domain separation”) but the API was never implemented.

I’m now in the process of exploring Halo2 and making my first circuits. No smartcontracts for now, I’m just trying to prove/verify the correctness of a simple coin transfer transaction from address A to address B.

I definitely want to post a separate tutorial about Halo2 because on one hand it’s very complex and not easy to learn and on the other hand it’s so much more powerful than Circom and really deserves to be known more! Not to mention that people should probably ramp off Circom usage altogether seeing how its GitHub repo activity has gone flat over the last few months…

