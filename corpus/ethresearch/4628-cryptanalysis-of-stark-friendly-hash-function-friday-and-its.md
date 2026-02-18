---
source: ethresearch
topic_id: 4628
title: Cryptanalysis of STARK-friendly hash function Friday and its cipher Jarvis
author: khovratovich
date: "2018-12-19"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/cryptanalysis-of-stark-friendly-hash-function-friday-and-its-cipher-jarvis/4628
views: 1803
likes: 10
posts_count: 2
---

# Cryptanalysis of STARK-friendly hash function Friday and its cipher Jarvis

An international group of researchers discovered an algebraic vulnerability in the recently proposed Friday hash function.  It turns out that SNARK/STARK-friendly designs can be vulnerable to Groebner basis attacks for exactly the same reason: few low degree equations. All versions of Jarvis and Friday have much lower security level than expected.

Some slides [here](https://drive.google.com/open?id=16NOFiKxoBqe3zeRAr7quUgRbcGQTitsL) .

## Replies

**HarryR** (2018-12-24):

The slides present the complexity of interpolating the cipher using some kind of interpolation using Gröbner basis and the Hilber series. Lagrange interpolation is more easily understood IMO, but does this new work provide a lower-complexity solution using a different algorithm? If so, how realistic is it to implement and how much memory is required.

For Lagrange interpolation there is a multiplicative cost of at least O(d\log d) for a polynomial of degree d, and all terms need to be in memory for the computation? With 12 rounds of cubing the degree is about 2^{32}, requiring 128gb of memory to compute. Given a naïve implementation in C: https://justcode.me/c/c-program-implementing-lagrange-interpolation-formula/ - would these new findings make it easier to find pre-images of perform key recovery with MiMC?

What is a realistic way to target a specific security level, as in a desired number of years at the current pace of innovation? And what relation does that have to a given number of rounds of either algorithm.

The following are some interesting references, but I’m still having a hard time understanding it:

- http://linux.math.tifr.res.in/manuals/html/magma/text630.html
- https://everipedia.org/wiki/lang_en/Gr%C3%B6bner_basis/
- https://en.wikipedia.org/wiki/Gröbner_basis
- https://en.wikipedia.org/wiki/Hilbert_series_and_Hilbert_polynomial

