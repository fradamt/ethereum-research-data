---
source: ethresearch
topic_id: 5945
title: "Galois: a JavaScript/WASM library for finite field arithmetic"
author: bobbinth
date: "2019-08-08"
category: Tools
tags: [library]
url: https://ethresear.ch/t/galois-a-javascript-wasm-library-for-finite-field-arithmetic/5945
views: 3357
likes: 5
posts_count: 3
---

# Galois: a JavaScript/WASM library for finite field arithmetic

I originally wrote this library for the [genSTARK](https://ethresear.ch/t/genstark-a-javascript-zk-stark-generation-framework/5538) project, but it evolved into a pretty nifty stand-alone module. The library is here:



      [github.com](https://github.com/GuildOfWeavers/galois)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/c/e/ce5a12ff2baf096e3517506c99f4a6ebd708be5f_2_690x344.png)



###



Arithmetic and polynomial operations in finite fields.










High-level features are:

- Basic modular arithmetic (addition, subtraction, multiplication, inversion, exponentiation).
- Bulk operations on vectors and matrixes.
- Basic polynomial operations (addition, subtraction, multiplication, division).
- Polynomial evaluation and interpolation (using Lagrange and FFT methods).

At this point, only prime fields are supported.

### WebAssembly optimization

One of the cool features of the library is a flexible optimization architecture. It is pretty simple to write optimization modules for different types of fields.

So far, I wrote an optimization module in WASM for 128-bit prime fields with modulus of the form 2^{128}-k, where k < 2^{64}.This resulted in the overall speed of up to **6x - 10x** as compared to native JavaScript implementation. Here are some high-level benchmarks run on Intel Core i5-7300U @ 2.60GHz (single thread):

| Operations/sec | JS BigInt (256-bit) | JS BigInt (128-bit) | WASM (128-bit) |
| --- | --- | --- | --- |
| Additions | 3,200,000 | 5,000,000 | 44,000,000 |
| Multiplications | 950,000 | 1,850,000 | 16,300,000 |
| Exponentiations | 3,200 | 10,500 | 97,000 |

WASM performance can be optimized further. Specifically, SIMD and multi-threaded evaluation is something that I’m planning to implement at some point in the future (once support for these in WASM becomes more mature). But even as is, I believe the numbers are within 2x - 4x of what can be achieved with a native C implementation.

The library is still very new, and there are a bunch of things to fix and improve (see the [issues](https://github.com/GuildOfWeavers/galois/issues) in the repo). So, would appreciate any feedback, help, and support.

## Replies

**cdetrio** (2019-08-12):

Cool! There is some overlap between the features here and what [websnark](https://github.com/iden3/websnark) does. I see this is written in Assemblyscript, it would be interesting to compare the benchmarks against websnark.

![](https://ethresear.ch/user_avatar/ethresear.ch/bobbinth/48/2389_2.png) bobbinth:

> At this point, only prime fields are supported.

I’m very interested in a binary field implementation, as it’s something we’d like to benchmark in wasm. We have lots of example applications using prime fields (elliptic curves and SNARKs/pairings etc.), including the STARK implementations using prime fields (genSTARK, and even the [starkDEX solidity code](https://ropsten.etherscan.io/address/0xdc3422c75a04e64c30b4cedac699239d48bfba35#code)), all of which can be ported/compiled to wasm (e.g. this [scout STARK example](https://github.com/ewasm/scout/pull/22)). But we can’t find a STARK implementation using binary fields, and so the performance of binary field arithmetic in wasm is an open question for us.

---

**bobbinth** (2019-08-14):

Thanks! Would love to benchmark this against other implementations - but not sure how to benchmark modular arithmetic ops with websnarks.

As for binary fields - I’ve stubbed it out [here](https://github.com/GuildOfWeavers/galois/blob/66e1bea9cadce7a5dc519c6ef4907b001de2bb7d/lib/BinaryField.ts), but a workable implementation is probably some time away. I’d like to first stabilize the overall architecture using the prime field implementation (that’s probably another 1 or 2 iterations away). But once the interfaces stabilize, it should be fairly straightforward to plug in a binary field implementation into the existing structure.

