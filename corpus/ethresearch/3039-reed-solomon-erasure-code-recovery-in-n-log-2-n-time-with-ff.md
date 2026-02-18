---
source: ethresearch
topic_id: 3039
title: Reed-Solomon erasure code recovery in n*log^2(n) time with FFTs
author: vbuterin
date: "2018-08-21"
category: Sharding
tags: []
url: https://ethresear.ch/t/reed-solomon-erasure-code-recovery-in-n-log-2-n-time-with-ffts/3039
views: 8616
likes: 5
posts_count: 12
---

# Reed-Solomon erasure code recovery in n*log^2(n) time with FFTs

With Fast Fourier transforms it’s possible to convert a set of evaluations of a polynomial over a prime field at a set of specific points, P(1), P(r), P(r^2) … P(r^{{2^k}-1}) (where r^{2^k} = 1) into the polynomial’s coefficients in n * log(n) time. This is used extensively and is key to the efficiency of [STARKs](https://vitalik.ca/general/2018/07/21/starks_part_3.html) and most other general-purpose ZKP schemes. Polynomial interpolation (and its inverse, multi-point evaluation) is *also* used extensively in erasure coding, which is useful for [data recovery](https://blog.ethereum.org/2014/08/16/secret-sharing-erasure-coding-guide-aspiring-dropbox-decentralizer/) and in blockchains for [data availability checking](https://github.com/ethereum/research/wiki/A-note-on-data-availability-and-erasure-coding).

Unfortunately, the FFT interpolation algorithm works only if you have *all* evaluations at P(r^i) for 0 \le i \le 2^k - 1. However, it turns out that you can make a somewhat more complex algorithm to also achieve polylog complexity for interpolating a polynomial (ie. the operation needed to recover the original data from an erasure code) in those cases where some of these evaluations are missing. Here’s how you do it.

### Erasure code recovery in O(n*log^2(n)) time

Let d[0] ... d[2^k - 1] be your data, substituting all unknown points with 0. Let Z_{r, S} be the minimal polynomial that evaluates to 0 at all points r^k for k \in S. Let E(x) (think E = error) be the polynomial that evaluates to your data with erasures (ie. E(r^i) = d[i]), and let P(x) be the polynomial that evaluates to original data. Let I be the set of indices representing the missing points.

First of all, note that D * Z_{r,I} = E * Z_{r,I}. This is because D and E agree on all points outside of I, and Z_{r,I} forces the evaluation on points *inside* I to zero. Hence, by computing d[i] * Z_{r,I}(r^i) = (E * Z_{r,I})(r^i), and interpolating E * Z_{r,I}, we get D * Z_{r,I}.

Now, how do we extract D? Just evaluating pointwise and dividing won’t work, as we already know that at least for some points (in fact, the points we’re trying to recover!) (D * Z_{r,I})(x) = Z_{r,I}(x) = 0, and we won’t know what to put in place of 0 / 0. Instead, we do a trick: we generate a random k, and compute Q1(x) = (D * Z_{r,I})(k * x) (this can be done by multiplying the ith coefficient by k^{-i}). We also compute Q2(x) = Z_I(k * x) in the same way. Now, we compute Q3 = Q1 / Q2 (note: Q3(x) = D(k * x)), and then from there we multiply the ith coefficient by k^i to get back D(x), and evaluate D(x) to get the missing points.

Altogether, outside of the calculation of Z_{r,I} this requires six FFTs: one to calculate the evaluations of Z_{r,I}, one to interpolate E * Z_{r,I}, two to evaluate Q1 and Q2, one to interpolate Q3, and one to evaluate D. The bulk of the complexity, unfortunately, is in a seemingly comparatively easy task: calculating the Z_{r,I} polynomial.

### Calculating Z in O(n*log^2(n)) time

The one remaining hard part is: how do we generate Z_{r,S} in n*polylog(n) time? Here, we use a recursive algorithm modeled on the FFT itself. For a sufficiently small S, we can compute (x - r^{s_0}) * (x - r^{s_1}) ... explicitly. For anything larger, we do the following. Split up S into two sets:

S_{even} = {\frac{x}{2}\ for\ x \in S\ if\ S\ mod\ 2 = 0}

S_{odd} = {\frac{x-1}{2}\ for\ x \in S\ if\ S\ mod\ 2 = 1}

Now, recursively compute L = Z_{r^2, S_{even}} and R = Z_{r^2, S_{odd}}. Note that L evaluates to zero at all points (r^2)^{\frac{s}{2}} = r^s for any even s \in S, and R evaluates to zero at all points (r^2)^{\frac{s-1}{2}} = r^{s-1} for any odd s \in S. We compute R'(x) = R(x * r) using the method we already described above. We then use FFT multiplication (use two FFTs to evaluate both at 1, r, r^2 ... r^{-1}, multiply the evaluations at each point, and interpolate back the result) to compute L * R', which evaluates to zero at all the desired points.

In one special case (where S is the *entire* set of possible indices), FFT multiplication fails and returns zero; we watch for this special case and in that case return the known correct polynomial, P(x) = x^{2^k} - 1.

---

Here’s the code that implements this (tests [here](https://github.com/ethereum/research/blob/master/mimc_stark/test_recovery.py)):


      [github.com](https://github.com/ethereum/research/blob/master/mimc_stark/recovery.py)




####

```py
from fft import fft, mul_polys

# Calculates modular inverses [1/values[0], 1/values[1] ...]
def multi_inv(values, modulus):
    partials = [1]
    for i in range(len(values)):
        partials.append(partials[-1] * values[i] % modulus)
    inv = pow(partials[-1], modulus - 2, modulus)
    outputs = [0] * len(values)
    for i in range(len(values), 0, -1):
        outputs[i-1] = partials[i-1] * inv % modulus
        inv = inv * values[i-1] % modulus
    return outputs

# Generates q(x) = poly(k * x)
def p_of_kx(poly, modulus, k):
    o = []
    power_of_k = 1
    for x in poly:
        o.append(x * power_of_k % modulus)
```

  This file has been truncated. [show original](https://github.com/ethereum/research/blob/master/mimc_stark/recovery.py)








Questions:

- Can this be easily translated into binary fields?
- The above algorithm calculates Z_{r,S} in time O(n * log^2(n)). Is there a O(n * log(n)) time way to do it?
- If not, are there ways to achieve constant factor reductions by cutting down the number of FFTs per recursive step from 3 to 2 or even 1?
- Does this actually work correctly in 100% of cases?
- It’s very possible that all of this was already invented by some guy in the 1980s, and more efficiently. Was it?

## Replies

**sourabhniyogi** (2018-08-27):

Concerning efficient erasure coding, have you checked out [fountain codes](https://pdfs.semanticscholar.org/974b/c9900eee8be1de11ee0e900a48f63e135a2e.pdf)

– Luby codes and then Raptor codes?  Here is [Nick Johnson’s short tutorial](http://blog.notdot.net/2012/01/Damn-Cool-Algorithms-Fountain-Codes) on it.  They have O(n) coding complexity, so you can encode + decode 1MB in 0.2s on a garden variety machine running an implementation like [this one](https://github.com/google/gofountain) rather than the 21s encoding you reported from C++.  If you bring in RNG from { the hash of the data being erasure coded, your favorite replacement to RANDAO }, the erasure coding can be Merklized.  There are [patents](https://patents.google.com/patent/US6307487B1/en) on this owned by Qualcomm but at least some of the oldest are expiring.

For STARKs, will try the “Calculating Z” technique and report back.

---

**vbuterin** (2018-08-27):

For STARKs, you want the evaluation of Z to be very concise so that you can do it inside the verifier; you can often find mathematical structures that do this for you. For example, in the multiplicative subgroups that I used for the MIMC example, you’re taking the subgroup 1, g, g^2 … g^{2^k-2}, where Z = (x^{2^k} - 1) / (x - g^{2^k - 1}). For erasure coding it’s more difficult because you don’t have this option, since it’s assumed the adversary could be omitting a portion of the data that will make computing Z for it not so simple.

---

**dankrad** (2020-01-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Let E(x)E(x) (think E = error) be the polynomial that evaluates to your data with erasures (ie. E(ri)=d[i]E(r^i) = d[i] ), and let P(x)P(x) be the polynomial that evaluates to original data. Let II be the set of indices representing the missing points.

I understand this this as E being the polynomial that interpolates to the known evaluations. I think P(x) is later called D. Isn’t (due to the low-degreeness) actually E=D?

I would write it down in a slightly different way: Say F is the interpolation of the data d[i] where d[i] is availabile, and 0 where i\in I (i.e. d[i] is not available). Then F can be easily computed from the available data using FFT, by substituting 0 in all the positions where the data is available.

Now F = D \cdot Z_{r,I}. Afterwards, use the trick to described to recover D from this equation.

---

**vbuterin** (2020-01-09):

Aah I think the idea that I meant to say is that E evaluates to the data but putting 0 in place of all missing points, and D is the actual data.

---

**dankrad** (2020-12-18):

I was thinking about this problem today and I came across this interesting algorithm to compute Z_{r,S}. It is unfortunately less efficient (O(n^2)) except in some special cases, but maybe someone can think of a trick to make it efficient so want to document it here.

We can easily compute a polynomial multiple of Z_{r,S}, by taking the vector that is zero in the positions of S and has a random non-zero value in the other positions, and take its Fourier transform. Let’s do this for two different random assignments and call the resulting polynomials P(X) and Q(X). Then we know that with overwhelming probability that Z_{r,S}(X) = \mathrm{gcd}(P(X), Q(X)).

So we can easily get the desired polynomial by computing a gcd. The Euclidean algorithm can do this and will reduce the degree of the polynomials by 1 at each step, and each step involves O(n) field operations, so in the general case this algorithm uses O(n^2) steps. However, the Euclidean terminates once the degree of the gcd is reached, so should the number of zeroes be close to the total size of the domain, it can be much faster.

---

**alinush** (2020-12-18):

There are O(n\log^2{n})-time variants of the Euclidean algorithm, if this is what you need.

For example, see **Fast Euclidean Algorithm**, by von zur Gathen, Joachim and Gerhard, Jurgen, *in Modern Computer Algebra*, 2013.

**Later edit:** In the past, I’ve used [libntl](https://libntl.org/)’s fast EEA implementation. See [here](https://github.com/alinush/libaad-ccs2019/blob/2f31566bbdac4891df45eee2e9268bc4681533dd/libaad/include/aad/PolyOps.h#L85).

---

**dankrad** (2020-12-19):

That’s very cool, I found some info on the algorithm here: https://planetmath.org/fasteuclideanalgorithm

So this gives the algorithm the same asymptotic complexity as the one suggested by [@vbuterin](/u/vbuterin)  (module a \log(\log n) factor that I’m not sure applies for finite fields; if it does it would also apply to [@vbuterin](/u/vbuterin)’s algorithm as it would be for all polynomial multiplications via FFT.

So, interesting question is which one is concretely more efficient.

---

**alinush** (2020-12-19):

Yes, that article is incorrect about the extra \log\log n factor for polynomial multiplication.

The time to multiply two polynomials over a finite field is M(n) = n \log n field operations (via FFT).

(On a related note, the extra \log \log n factor does come up only for n-bit integer multiplication. However, a [recent breakthrough](https://hal.archives-ouvertes.fr/hal-02070778/document) showed an O(n\log{n}) algorithm for integer multiplication. But it is not concretely fast. In practice, one still uses [Schonhage-Strassen](https://en.wikipedia.org/wiki/Sch%C3%B6nhage%E2%80%93Strassen_algorithm), which takes O(n\log{n}\log{\log{n}}).)

---

**dankrad** (2020-12-30):

An update on this – I coded both ideas [here](https://github.com/ethereum/research/blob/f6ffca80aa33aa115b295cf88b8b83c16fdf5bc1/polynomial_reconstruction/polynomial_reconstruction.py) in python. In short, while both have the same asymptotics, Vitalik’s approach is ca. 30x faster when constants are factored in.

The quest for an O(n \log n) or better algorithm is still open.

---

**qizhou** (2022-10-12):

For danksharding, we could optimize the calculation of Z from n = 8192 to n = 8192/16 = 512 (16 is the sample size).

The basic idea is that we could use a vanishing polynomial to represent a missing sample as

f(x) = x^{16} - h_i^{16}

where h_i is the shifting parameter.  Since h_i^{16}, i = 0, ..., 511 form a root of unity of order 512, the same algorithm can be applied to recover the full Z with n = 512

An example code can be found here:



      [github.com/ethereum/research](https://github.com/ethereum/research/pull/131)














####


      `master` ← `qizhou:opt_zpoly`




          opened 04:54AM - 12 Oct 22 UTC



          [![](https://ethresear.ch/uploads/default/original/2X/e/ec489df73b8873547715c8a2f21986ca2b83d33c.jpeg)
            qizhou](https://github.com/qizhou)



          [+70
            -3](https://github.com/ethereum/research/pull/131/files)







This diff implements an optimized zpoly calculation based on danksharding.  The […](https://github.com/ethereum/research/pull/131)basic idea is that we could use vanishing polynomial to represent a missing sample (16 data points) so that the complexity size is reduced from 8192 to 512 in O(n log^2(n)).

Performance numbers on Mac Book:
Before: 1.28s
After: 0.60












And I have a side-by-side perf comparison for the whole recovery process with n = 8192

- Before: 1.2s
- After: 0.6s

---

**qizhou** (2022-10-24):

It seems that we could further optimize the recovery based on Danksharding encoding - especially based on reverse bit order and samples in a coset size 16.  The main conclusion is that we could reduce the problem size from 8192 to 16 sub-problems of size 512 (=8192/16) and thus the cost of Z(x) and Q2(x) can be amortized over 16 sub-problems.

Consider the following danksharding encoding: the data are encoded in a polynomial with degree 4095 and are evaluated at the roots of unity of order n = 8192.  The roots of unity are ordered by reverse bit order, i.e., \{ \omega_0, \omega_1, ..., \omega_{8191} \} = \{ 1, \omega^{4096}, \omega^{2048}, \omega^{6072}, …, \omega^{8191} \}.  Therefore, we define \Omega = \{ \omega_0, \omega_1, … , \omega_{15} \} is a subgroup of order 16, and for each sample 0\leq i < m, we have a shifting factor h_i = \omega_{16i} so that the coset H_i = h_i \Omega.

For each sample \{ d^{(i)}_j \}, i = \{0, 1, ..., 255\}, where i is the index of the sample, we have the equations:

\begin{bmatrix} \omega^0_{16i+0} & \omega_{16i+0}^1 & ... & \omega^{4095}_{16i+0} \\ \omega_{16i+1}^0 & \omega_{16i+1}^1 & ... & \omega_{16i+1}^{4095} \\ ... \\ \omega_{{16i+15}}^0 & \omega_{16i+15}^1 & ... & \omega_{16i+15}^{4095}  \end{bmatrix}_{16 \times 4096}\begin{bmatrix}  a_0 \\  a_1 \\ ... \\  a_{4095} \end{bmatrix} = \begin{bmatrix} d^{(i)}_0 \\ d^{(i)}_1 \\ ... \\ d^{(i)}_{15} \end{bmatrix}

Given h_i \omega_j = \omega_{16i+j}, \forall 0 \leq j \leq 15 , we have

\begin{bmatrix} h_i^0 \omega^0_{0} & h_i^1 \omega_{0}^1 & ... & h_i^{4095} \omega^{4095}_{0} \\ h_i^0 \omega_{1}^0 & h_i^1 \omega_{1}^1 & ... & h_i^{4095} \omega_{1}^{4095} \\ ... \\ h_i^0 \omega_{{15}}^0 & h_i^1 \omega_{15}^1 & ... &  h_i^{4095} \omega_{15}^{4095}  \end{bmatrix}_{16 \times 4096}\begin{bmatrix}  a_0 \\  a_1 \\ ... \\  a_{4095} \end{bmatrix} = \begin{bmatrix} d^{(i)}_0 \\ d^{(i)}_1 \\ ... \\ d^{(i)}_{15} \end{bmatrix}

\begin{bmatrix} \omega^0_{0} &  \omega_{0}^1 & ... & \omega^{4095}_{0} \\ \omega_{1}^0 &\omega_{1}^1 & ... &  \omega_{1}^{4095} \\ ... \\  \omega_{{15}}^0 & \omega_{15}^1 & ... &   \omega_{15}^{4095}  \end{bmatrix}_{16 \times 4096}\begin{bmatrix}  h_i^0 a_0 \\  h_i^1 a_1 \\ ... \\  h_i^{4095} a_{4095} \end{bmatrix} = \begin{bmatrix} d^{(i)}_0 \\ d^{(i)}_1 \\ ... \\ d^{(i)}_{15} \end{bmatrix}

Note that \omega_i^{16 + j} = \omega_i^{j}, \forall 0 \leq i\leq15, then we have

\begin{bmatrix} \mathcal{F}_{16\times 16} & \mathcal{F}_{16\times 16} & ... & \mathcal{F}_{16\times 16}  \end{bmatrix}_{16 \times 4096}\begin{bmatrix}  h_i^0 a_0 \\  h_i^1 a_1 \\ ... \\  h_i^{4095} a_{4095} \end{bmatrix} = \begin{bmatrix} d^{(i)}_0 \\ d^{(i)}_1 \\ ... \\ d^{(i)}_{15} \end{bmatrix}

where \mathcal{F}_{16\times 16} is the Fourier matrix (with proper reverse bit order).

Combining the matrices, we finally reach at

\mathcal{F}^{-1}_{16 \times 16}  \begin{bmatrix} d^{(i)}_{0} \\ d^{(i)}_{1} \\ ... \\ d^{(i)}_{15} \end{bmatrix} =\begin{bmatrix} h^0_i\sum_{j=0}^{255} h^{16j}_ia_{16j} \\  h^1_i\sum_{j=0}^{255} h^{16j}_ia_{16j+1}\\ ... \\  h^{15}_i\sum_{j=0}^{255} h^{16j}_i a_{16j+15} \end{bmatrix} = \begin{bmatrix} h^0_{i} y^{(i)}_0 \\ h^1_{i} y^{(i)}_1 \\ ... \\ h^{15}_{i}  y^{(i)}_{15}\end{bmatrix}

This means that we can recover all missing samples by:

1. Perform IFFT to all received samples (256 IFFTs of size 16x16)
2. Recover y^{(i)}_j of missing samples by using Vitalik’s algorithm that solves 16 sub-problems of size 512.  Note that Z(x) and Q2(x) (if k is the same) can be reused in solving each sub-problem.
3. Recover the missing samples of index i by FFTing \{ h_i^j y^{(i)}_j \}, \forall 0 \leq j \leq 15.

The example code of the algorithm can be found [Optimized Reed-Solomon code recovery based on danksharding by qizhou · Pull Request #132 · ethereum/research · GitHub](https://github.com/ethereum/research/pull/132)

Some performance numbers on my MacBook (recovery of size 8192):

- Original: 1.07s
- Optimized zpoly: 0.500s
- Optimized RS: 0.4019s

