---
source: magicians
topic_id: 2581
title: Precompile for general elliptic curve linear combinations
author: Recmo
date: "2019-02-04"
category: EIPs
tags: [security, eip]
url: https://ethereum-magicians.org/t/precompile-for-general-elliptic-curve-linear-combinations/2581
views: 7219
likes: 21
posts_count: 24
---

# Precompile for general elliptic curve linear combinations

# Precompile for Elliptic Curve Linear Combinations

EIP here: https://github.com/ethereum/EIPs/blob/af94e5498b9db0ee32f96bdba199a76b138906bc/EIPS/eip-ecmul-precompile.md

PR here: https://github.com/ethereum/EIPs/pull/1829

I have removed redundant content posted here.

## Questions

**Q4.** Accepting points in compressed form adds extra overhead to every call, but allows caller to work with compressed coordinates. Is it worth it?

**Q5.** Cleverness allows you to use this precompile for modular square root. Is it possible to extract a modular inversion?

**Q6.** While a transaction has no assumption of privacy, this could be an issue when used in `eth_call`. A constant time implementation also allows more code-reuse with applications that require more side-channel protection such as wallets. Should we implement constant time algorithms?

**Q8.** Is it worth exploring some hash to a curve point function or a generic pairing function?

## References

- List of elliptic curve parameters.
https://safecurves.cr.yp.to/index.html
- Database of optimal addition formulas.
http://www.hyperelliptic.org/EFD/index.html
- Mater Inc. Rust Finite Field implementation.
https://github.com/matterinc/ff/blob/master/src/lib.rs
- And Elliptic Curve.
https://github.com/matterinc/pairing/blob/master/src/bn256/ec.rs
- Parity Finite Field Implementation.
https://github.com/paritytech/bigint/blob/master/src/uint.rs
- Standards for Efficient Cryptography 1 (SEC 1).
http://www.secg.org/sec1-v2.pdf
- Weierstrudel implementation of BN254.
https://medium.com/aztec-protocol/huffing-for-crypto-with-weierstrudel-9c9568c06901

## Replies

**axic** (2019-02-04):

Nice!

We do currently collect some precompile ideas under https://github.com/ewasm/ewasm-precompiles/issues, but since the above proposal doesn’t utilise any ewasm-specific behaviour (such as the potential to avoid using the current ABI encoding), I’d suggest the best would be proposing this as an EIP, which can be implemented and tested on ewasm. The other newly implemented precompiles in the ewasm repository all have a corresponding EIP.

What do you think?

---

**cdetrio** (2019-02-04):

This seems to be an outline, if fleshed out it would become an EIP.

A (the?) major use case for this precompile, if I understand correctly, is for doing Pedersen commitments inside contracts, cheaply. So it would supersede a [pedersen commitment precompile](https://github.com/ewasm/ewasm-precompiles/issues/25).

---

**Recmo** (2019-03-06):

I created a Draft EIP and made a [pull request](https://github.com/ethereum/EIPs/pull/1829). It links back here for discussion.

> @axic  since the above proposal doesn’t utilise any ewasm-specific behaviour (such as the potential to avoid using the current ABI encoding), I’d suggest the best would be proposing this as an EIP, which can be implemented and tested on ewasm

Yes, I realized this and I don’t want to add technical risk to this proposal by making it unnecessarily dependent on eWASM.

The current implementation strategy is to use the excellent Rust libraries developed by ZCash and have both native and ewasm as a compilation target. We can then test and compare. It is then up to Node developers to either use the Rust library, native library, webassembly library, or develop their own.

> @cdetrio  A (the?) major use case for this precompile, if I understand correctly, is for doing Pedersen commitments inside contracts, cheaply.

The goal of this EIP is to subsume a class of problems, including but not limited to

- EWASM issue 25: Pederson commitments for altbn128.
- EIP issue 603: ecadd/ecmul for SECP256k1.
- EIP665: Ed25519 signature verification. Edit: maybe not, requires Montgomery curve, not short Weierstrass.
- EIP196: altbn128 ecadd/ecmul which is inefficient for linear combinations.
- Existing 256-bit ECDSA signature schemes.
- New ECDSA Signature schemes used inside proof protocols like S[n/t]arks and.
- Pederson commitment schemes.
- BLS Signature aggregation.

All of these would benefit from either 1) allowing generic curves or 2) doing a linear combination.

`ECRECOVER` can also be reimplemented using this proposal, but I doubt that leads to an advantage.

---

**Recmo** (2019-03-06):

[@boris](/u/boris) What do I do next to get this on the HF agenda?

---

**AlexeyAkhunov** (2019-03-06):

Thank you very much for writing this down! I agree that perhaps dependency eWASM is too early to build in.

I think the next steps would be to build a proof of concept and generate test cases for this precompile.

---

**boris** (2019-03-06):

Add it to https://en.ethereum.wiki/roadmap/istanbul

I’m going to work with [@axic](/u/axic) on updating 233. I think we want to see a PR against 1679 to have a “proposed” section that includes your EIP. The wiki can be a placeholder for this or you can go ahead and do the PR now.

As we discussed, how you plan to implement — eg a single C or Rust or ??? implementation that can be linked into clients — might be good to hear. Client devs will have opinions ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

(Apologize for lack of links, mashing my phone)

---

**Recmo** (2019-03-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> The wiki can be a placeholder for this or you can go ahead and do the PR now.

I updated the wiki and submitted a PR on 1679.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> As we discussed, how you plan to implement — eg a single C or Rust or ??? implementation that can be linked into clients — might be good to hear. Client devs will have opinions

It’s described in the EIP section [Implementation](https://github.com/ethereum/EIPs/blob/af94e5498b9db0ee32f96bdba199a76b138906bc/EIPS/eip-1829.md#implementation):

> There will be a reference implementation in Rust based on the existing libraries (in particular those by ZCash and The Matter Inc.).
>
>
> The reference implementation will be production grade and compile to a native library with a C api and a webassembly version. Node developers are encouraged to use the reference implementation and can use either the rust library, the native C bindings or the webassembly module. Node developers can of course always decide to implement their own.

---

**cdetrio** (2019-03-06):

Great to see a draft EIP!

I want to highlight question 8:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recmo/48/2516_2.png) Recmo:

> Q8. Is it worth exploring some hash to a curve point function or a generic pairing function?

How much would it benefit Pedersen commitments for rollup, to do this computation inside the precompile?

---

**HarryR** (2019-03-11):

I started work on a simple implementation for EIP-1829:

https://github.com/HarryR/eip-1829

Hopefully I will generate some test cases which can verify the functionality and ensure that implementations match each other.

> How much would it benefit Pedersen commitments for rollup, to do this computation inside the precompile?

Hash To Curve would be good to add to this builtin, as while you can do Y coordinate recovery using the precompile it would `REVERT` if you gave it an invalid parameter X coordinate (something you may have to do in a loop several times) - so doing it in practice would be annoying / tedious from Solidity.

It isn’t possible to use this builtin for pairing operations, and I don’t think it should be extended for that use case…

---

**Recmo** (2019-03-12):

Idea: The largest prime less than $2^{256}$ is $2^{256} - 189$. This means the top 189 values can not be valid field elements and we could use them as flag values for the point at infinity, compressed points, or number of tries for try-and-increment value-to-point mapping.

---

**Recmo** (2019-03-12):

Modular square root only has efficient deterministic algorithms when $p = 3 mod 4$ or $p = 5 mod 8$, which applies to nearly all curves. The algorithms are simple and fail gracefully when $p$ is composite.

There are no simple algorithms for other values of $p$.

I suggest we disallow any form of point recovery when neither $p = 3 mod 4$ or $p = 5 mod 8$.

---

**Recmo** (2019-03-14):

Questions from eWASM call:

- Which practical application (ECDSA, Pederson, Bulletproofs, etc.) are there?
- How many points and scalars are required for each?
- Look at EVM-C for the C bindings, there’s also Rust bindings under development.

Questions to eWASM team:

- Benchmarking procedure and framework.

---

**Recmo** (2019-03-14):

> @vbuterin : The thing that has always stopped me from proposing a similar thing is, what happens if someone submits a non-prime modulus? There are different ways to implement elliptic curve addition and multiplication, and in general I don’t expect that the different libraries have been tested to ensure that they fail in the same cases when the modulus ends up being composite, and this seems like a large and deep potential source of consensus failures. Unfortunately primality tests that take into account weird edge cases like Carmichael numbers but are also clean and efficient don’t really exist.

So if the modulus is composite you end up with a Ring instead of a Field. The only difference being that inversion fails on more values than just zero.

Elliptic curve linear combinations, when implemented in the standard efficient way using Jacobi coordinates use only Ring operations (i.e. no inversion). So the whole computation is safe. What will go wrong is converting back to Affine coordinates, which requires a single inversion. If this inversion fails, this would normally indicate the point at infinity. No new control flow. No edge cases being hit harder than otherwise, except for the last one.

Garbage in, garbage out still applies of course. Throw in a composite modulus and the thing you are computing is not guaranteed to be an elliptic curve.

Existing libraries do not seem particularly useful here. Most are designed for a particular curve. The remaining ones are mostly for research purposes and are not security hardened. (They would rely on probabilistic algorithms like Miller-Rabin or Tonelli–Shanks).

The current implementation strategy is to develop a Rust library specific for this EIP which is generic and efficient, but only uses deterministic algorithms. This library will be available as Rust, C bindings and a eWASM module.

Currently the design allows you to use compressed coordinates as input. This gives developers some advantages, but requires us to compute modular square roots. Modular square root has similar issues as inversion. Simple deterministic procedures involving only Ring operations exist when `p = 3 mod 4` or `p = 5 mod 8` . Most field moduli used in practice satisfy this by design. My current thinking is to simply reject compressed coordinates when the field modulus does not satisfy and make compressed points optional.

Lastly, there’s a feature request to do a form of hash-to-curve point. I think this can be incorporated elegantly and safely as well. I’ll update the EIP soon to incorporate these ideas.

---

**axic** (2019-03-14):

The EVMC Rust bindings are here: [evmc/bindings/rust at master · ethereum/evmc · GitHub](https://github.com/ethereum/evmc/tree/master/bindings/rust)

The `evmc-vm` crate will provide an API for “VMs” to implement. [@chfast](/u/chfast) and I are considering to provide precompiles as EVMC modules to be used with aleth. If this works out, it would be possible to also provide EIP1829 as an EVMC module.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recmo/48/2516_2.png) Recmo:

> Benchmarking procedure and framework.

Some of that is available in [GitHub - ewasm/benchmarking: Instructions for benchmarking Ewasm precompiles. (And results.)](https://github.com/ewasm/benchmarking), but [@cdetrio](/u/cdetrio) will need to publish the framework he has been using.

For creating ewasm contracts, please have a look at [GitHub - ewasm/ewasm-rust-api: Ewasm API for Rust](https://github.com/ewasm/ewasm-rust-api).

---

**vbuterin** (2019-03-15):

Ah, I see. If the edge cases are that manageable, then I suppose it could work.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recmo/48/2516_2.png) Recmo:

> Existing libraries do not seem particularly useful here. Most are designed for a particular curve.

I think py_ecc might actually be generic enough to implement this fairly easily, or at least with a few tweaks. So there’s at least one other thing that the rust library could be checked against.

---

**shamatar** (2019-03-15):

[@Recmo](/u/recmo) Montgomery form (and implementations are likely to use it) is not defined in case of GCD != 1. But garbage in - garbage out should work.

---

**shamatar** (2019-04-12):

In addition to the separate Telegram chat I also post a link here, cause now this implementation is at the point where more help is needed with test vectors and pricing, then in actual implementation.

For the code here https://github.com/matter-labs/eip1829/tree/pairings the following works:

- runtime curve creation
- check on curve
- add two points
- multiply single point by a scalar (double-and-add or wnaf)
- multiexponentiation (trivial and peppinger)
- extension towers
- pairings for BLS12 family

There is a set of benchmarks, but only for quite limited set of curves. Can support fields of arbitrary size in principle.

Limitations:

- have to specify scalar field size for a curve (needed to try Ben-Coster algorithm, didn’t work out)
- field elements larger than a field are errors
- scalars larger than an order are errors
- only fields up to 319 bits are supported, but this only requires to extend a “switch” statement further

Plans:

- pairings for BN, MNT4 and MNT6. May be KSS too
- cleanup by removing a scalar fields
- check if pairings for Cocks-Pinch method generated curves can be easily implemented
- chose multiexp and multiplication methods based on benchmarks
- implement Twisted Edwards arithmetics (this one is trivial, but low priority)

---

**holiman** (2019-04-12):

Was just looking through the EIP. I couldn’t quite figure out what the gas cost calculation/specification is? Could you clarify that in the EIP – the eip should be a full specification, and it’s currently lacking that.

---

**virgil** (2019-04-27):

In the recent Core Devs Call, I said that ENS would like to have one of these precompiles:

- https://eips.ethereum.org/EIPS/eip-665
- https://eips.ethereum.org/EIPS/eip-1829

Where EIP1829 is a superset of EIP665.  Based on meeting feedback, my current understanding is that:

- EIP665 is ready-to-go but not obviously worth including.
- EIP1829 is not ready-to-go but is reasonably likely to be accepted at some future point.

Although it would obviously be welcome, ENS doesn’t *need* this to go into Istanbul.  Ergo, if it’s plausible that EIP1829 will go in at some point, we have no need for EIP665 and ENS will patiently wait for EIP1829.

---

**virgil** (2019-04-27):

An unrelated aside, given this is fairly complex crypto, I suggest writing this library in conjunction with Hyperledger Ursa.  https://www.hyperledger.org/projects/ursa

Although I am completely confident in our ability to do a bug-free implementation this EIP, Ursa is very interested in becoming a generic library for everyone (including Ethereum).  And given IBM/Hyperledger willingness to put substantial resources behind the Ursa project, it seems pro-social as well as financially sensible to avail ourselves to their generosity.


*(3 more replies not shown)*
