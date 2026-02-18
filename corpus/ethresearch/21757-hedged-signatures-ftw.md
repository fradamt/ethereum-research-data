---
source: ethresearch
topic_id: 21757
title: Hedged Signatures FTW
author: pcaversaccio
date: "2025-02-16"
category: Cryptography
tags: [security]
url: https://ethresear.ch/t/hedged-signatures-ftw/21757
views: 417
likes: 10
posts_count: 3
---

# Hedged Signatures FTW

4 days ago [elliptic](https://github.com/indutny/elliptic) – a well-know JavaScript-based cryptography library – published the following security advisory: [GHSA-vjh7-7g9h-fjfh](https://github.com/advisories/GHSA-vjh7-7g9h-fjfh).

> ### Summary
>
>
>
> Private key can be extracted from ECDSA signature upon signing a malformed input (e.g. a string or a number), which could e.g. come from JSON network input.
>
>
> Note that elliptic by design accepts hex strings as one of the possible input types.

First the good thing: If wallets strictly follow [RFC 6979](https://datatracker.ietf.org/doc/html/rfc6979) (nonces are derived deterministically from the hashed message), their input-to-bytes conversion is not erroneous (but we never really know!), and doesn’t allow custom nonce injection, everything should be safe.

Well, sure one might dismiss this as merely an implementation error, but I truly believe this incident is far more nuanced and warrants deeper reflection on the actions we, as an ecosystem, must take. Cryptographic primitive libraries—not just the cryptographic theory—are the foundation of our security infrastructure. A single mistake can lead to devastating consequences, and we really cannot afford to take that risk lightly. **Human error is inevitable** tbh, and new vulnerabilities will continue to emerge.

That’s why I think we should start experimenting with **hedged signatures** in our ecosystem. [@p_m](/u/p_m) describes this well in his blog post [here](https://paulmillr.com/posts/deterministic-signatures). The TL;DR is:

> Hedged signatures generate k deterministically, then incorporate randomness into it.

He also shares important references about the current usage:

> RFC 6979 actually describes hedging in section 3.6! Libraries also do: for example, libsecp256k1 had it since 2015
> BIP 340 authors also made a wise decision, incorporating hedging by default
> RFC 8032 ed25519 does not support hedged signatures, however, Signal made an effort and created XEdDSA. Then Apple followed Signal and added hedged ed25519 to both CryptoKit and its Safari implementation of webcrypto. The idea was formalized in the mailing list from 2017.

With this post, I aim to spark a discussion on **how and where we should begin exploring the adoption of hedged signatures in our ecosystem**. There is no doubt that they represent a meaningful advancement in security, and it is crucial that we consider their implementation thoughtfully.

## Replies

**p_m** (2025-02-16):

- micro-eth-signer supports hedged signatures
- Viem also supports them since Nov, but it’s disabled by default. They indicate switching on by default in next major version.
- Ethers has an open issue. They’ve indicated interest if Geth/Clef added hedging
- Geth/Clef have an open issue.
- ethereumjs has an open issue and plan to switch it on by default.

---

**bbjubjub2494** (2025-02-16):

Putting this in preformat for now because my account is too fresh to post links ![:stuck_out_tongue_winking_eye:](https://ethresear.ch/images/emoji/facebook_messenger/stuck_out_tongue_winking_eye.png?v=12)

```auto
In Rust, [the `k256` crate implements RFC6979 with the `ad` parameter for fresh randomness,](https://docs.rs/k256/latest/k256/ecdsa/hazmat/trait.SignPrimitive.html#method.try_sign_prehashed_rfc6979) but [higher level abstractions currently leave it empty.](https://docs.rs/ecdsa/0.16.9/src/ecdsa/recovery.rs.html#184) As a result, things like `alloy` should currently produce deterministic signatures.
There is also a `secp256k1` crate that contains bindings to libsecp256k1. [parts of Reth](https://github.com/paradigmxyz/reth/blob/a96bc6110cc985c9b7004966426280aed1dd4729/crates/primitives-traits/src/lib.rs#L17) have an option to use it. I couldn't quickly figure out if it enables hedging and under which circumstances.
Empirically, we can determine that Foundry 1.0 produces deterministic signatures by running the following command multiple times:
```sh
$ cast wallet sign --private-key 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80 "hello"
```

```auto

```

