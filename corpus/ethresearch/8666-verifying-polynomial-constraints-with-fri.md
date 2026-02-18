---
source: ethresearch
topic_id: 8666
title: Verifying polynomial constraints with FRI
author: dlubarov
date: "2021-02-13"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/verifying-polynomial-constraints-with-fri/8666
views: 3400
likes: 0
posts_count: 16
---

# Verifying polynomial constraints with FRI

In many argument systems, a valid witness is defined as a polynomial f such that C(f(x)) vanishes on some set H, where C is some constraint. (As an intuitive example, if we wanted to enforce that f\restriction_H contained only binary values, we could set C(x) = x (x - 1).) Equivalently, f is a valid witness iff C(f(x)) / Z_H(x) is a polynomial, where Z_H is the polynomial (of minimum degree) that vanishes on H.

If we’re using FRI, we could check the constraint by having the prover send (a low-degree extension of) f, then applying FRI to this quotient. Given a polynomial f that does not satisfy the instance, C(f(x)) / Z_H(x) will not be a polynomial, but it may still have up to \deg(C) \deg(f) points in common with a low-degree polynomial. To account for this, I think we would need \delta \le 1 - \deg(C) \rho (\delta is FRI’s proximity parameter, \rho is the code rate), which could make FRI rather expensive if C is high-degree.

Alternatively, we could have the prover send this quotient polynomial q(x) = C(f(x)) / Z_H(x), have the verifier sample a random point r, “open” f and q at r, and check that C(f(r)) = Z_H(r) q(r). Then by the Schwartz-Zippel lemma, invalid witnesses would be detected except with probability \deg(C) \deg(f) / |\mathbb{F}|. If we use a \delta within the decoding radius, (1 - \rho)/2, then the Merkle roots of f and q can be treated as binding commitments to their (unique) proximate polynomials, \tilde{f} and \tilde{q}, and we can verify openings of these proximate polynomials by running FRI on

\left\{ \frac{f(x) - f(r)}{x - r}, \frac{q(x) - q(r)}{x - r} \right\},

or sample a random \alpha and run FRI on

\frac{f(x) - f(r) + \alpha (q(x) - q(r))}{x - r}.

If \delta is outside the decoding radius, then we lose the binding property, but we can still use FRI as a sort of “weakly binding” polynomial commitment, since there are upper bounds on the number of polynomials within \delta of any f or q. Let L such an upper bound (e.g. from the Johnson bound, or the conjectured bound in the DEEP-FRI paper). Then in a sense, the Merkle root of f binds the prover to (at most) L proximate polynomials, and likewise for q.

So we can apply FRI in the same way as before, and argue that C(\tilde{f}(r)) = Z_H(r) \tilde{q}(r) is unlikely hold for any of the L^2 possible (\tilde{f}, \tilde{q}) pairs (if none of them are valid witnesses). However, this multiplies our soundness error by L^2, at least with a naive analysis (I think there may be ways to tighten this). In practice, most IOPs involve more than two prover polynomials, which would further increase the exponent on L.

So this error may greatly exceed our security parameter. I guess the obvious solution is to reduce soundness error by checking the polynomial identity at a bunch of points. We’re thinking about a recursive IOP with a small (64 bit) field and many (100+) witness polynomials, though, so the interpolations needed to open many points could get expensive.

One thing we could do is combine a set of 2^l polynomials (from the same prover message) into one higher-degree polynomial, which would increase L a bit but decrease its exponent. Constraints over the small polynomials would be compiled to constraints over the merged polynomial, with f_i(g^j)

mapped to f_\mathrm{merged}(g^{2^l j + i}). This seems a bit complex though, and it could end up being less efficient since it could increase the number of FRI rounds.

Are there better solutions? How do STARK implementations (or other FRI-based IOPs) handle this?

## Replies

**bobbinth** (2021-02-13):

This will probably not answer the question fully, but here are a few things I know:

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> we could have the prover send this quotient polynomial q(x) = C(f(x)) / Z_H(x) , have the verifier sample a random point r , “open” f and q at r, and check that C(f(r)) = Z_H(r) q(r)

This is the approach I’ve used it my implementations of STARK provers.

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> which could make FRI rather expensive if C is high-degree

You usually try to keep degree of C as low as possible. For example, I know that in Cairo VM, this degree is 2. In my Distaff VM, the degree is 8, but could be reduced to 4 with some optimizations.

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> We’re thinking about a recursive IOP with a small (64 bit) field and many (100+) witness polynomials

In STARKs, degrees of all polynomials are normalized to the same degree (high enough to accommodate the highest degree polynomial), and then they are all merged into a single polynomial using random linear combination. Then FRI is applied to this single polynomial.

Also, as far as I know, you don’t run FRI in a 64-bit field. If polynomial coefficients are in a 64-bit field, you run FRI in either a quadratic or a cubic extension of that field to get ~100 or ~128 bits of security respectively. I think that’s how StarkWare’s [ethSTARK](https://github.com/starkware-libs/ethSTARK) library works.

---

**dlubarov** (2021-02-15):

Thanks [@bobbinth](/u/bobbinth), this is helpful info!

![](https://ethresear.ch/user_avatar/ethresear.ch/bobbinth/48/2389_2.png) bobbinth:

> In STARKs, degrees of all polynomials are normalized to the same degree (high enough to accommodate the highest degree polynomial), and then they are all merged into a single polynomial using random linear combination. Then FRI is applied to this single polynomial.

I think there are a few options to handle this:

- As you said, we could pad polynomials to the same degree.
- We could split up higher-degree polynomials into components. For example Plonk splits up its quotient polynomial, and then queries it as t(X) = t_\mathrm{lo}(X) + X^n t_\mathrm{mid}(X) +  X^{2n} t_\mathrm{hi}(X).
- We could start FRI with a linear combination of the highest-degree polynomials, then “fold in” lower-degree polynomials mid-way though the commit phase.

Perhaps splitting up polynomials would be preferable in some cases, since it would mean fewer FRI rounds, but at the cost of more leaf data in the first round.

![](https://ethresear.ch/user_avatar/ethresear.ch/bobbinth/48/2389_2.png) bobbinth:

> Also, as far as I know, you don’t run FRI in a 64-bit field. If polynomial coefficients are in a 64-bit field, you run FRI in either a quadratic or a cubic extension of that field to get ~100 or ~128 bits of security respectively. I think that’s how StarkWare’s ethSTARK  library works.

Hm, would the concern with 64-bit FRI be that the commit phase introduces too much soundness error? I realize that will be an issue, but I think we could address it by executing the commit phase ~3 times with different randomness. We could execute them “in parallel”, i.e. with each batch of ~3 prover polynomials interleaved in a single oracle, to avoid increasing query complexity.

It would add some complexity, but I’m sort of determined to use 64-bit fields since certain hashes are much faster, particularly GMiMC.

---

**bobbinth** (2021-02-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> would the concern with 64-bit FRI be that the commit phase introduces too much soundness error?

I am probably not the best person to answer this question, but my understanding is that soundness of FRI is limited by the following expression: log(field\_size) - log(evaluation\_domain\_size) (point 3 from [here](https://github.com/starkware-libs/ethSTARK#7-measuring-security)). So, for example, if the field size is 128 bits and evaluation domain is 32 bits, the soundness could be at most 96 bits.

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> It would add some complexity, but I’m sort of determined to use 64-bit fields

Yes, this is possible and the way it is done in STARKs is that your computation can be in a 64 bit field, but then FRI is run in an extensions of this field (e.g. 128 bits in case of quadratic extension, or 192 bits in case of cubic extension). The way you move from the base field to extension field is during linear combination phase. So, basically, you start out with a set of polynomials with coefficients in a 64-bit field, but then you draw your coefficients for linear combination from the extension field. This way, you end up with a single polynomial with coefficients in the extension field. And then you run FRI on that polynomial.

One other point: from modular arithmetic standpoint, it might be more efficient to use a slightly smaller field (e.g. 62-bits). This way, you can enable extra optimizations by implementing branchless modular multiplication.

---

**dlubarov** (2021-02-22):

I also asked Eli Ben-Sasson about this, and he pointed me to the paper [Proximity Gaps for Reed-Solomon Codes](https://eprint.iacr.org/2020/654). I haven’t had a chance to read it yet, but it seems to have a better soundness argument which doesn’t result in an L^k term.

![](https://ethresear.ch/user_avatar/ethresear.ch/bobbinth/48/2389_2.png) bobbinth:

> I am probably not the best person to answer this question, but my understanding is that soundness of FRI is limited by the following expression: log(field_size)−log(evaluation_domain_size)log(field_size) - log(evaluation_domain_size) (point 3 from here ). So, for example, if the field size is 128 bits and evaluation domain is 32 bits, the soundness could be at most 96 bits.

Understood, but I think running the commit phase a few times would address this, no? E.g. if the probability of a “bad event” (c.f. FRI’s analysis) in each commit phase is bounded by 2^{40}, then with three runs, the probability of bad events occurring in all three reduction trees would be bounded by 2^{-120}. (We would use different randomness in each run so that the probabilities are independent.) Then in the query phase, we would apply consistency checks to all three reduction trees, so as long as one of them had no bad events, the analysis in FRI’s “bounding soundness when no bad event occurred” section would still hold. We should probably write out a more rigorous argument for this (and other FRI variations), but that would be the gist of the argument.

I know this probably sounds expensive, but I don’t expect it to increase costs that much if we do the runs “in parallel” as described above. Using extension fields is an interesting approach, but I’m not sure if we could use it with hashes like GMiMC, since the paper only considered prime and binary fields.

![](https://ethresear.ch/user_avatar/ethresear.ch/bobbinth/48/2389_2.png) bobbinth:

> One other point: from modular arithmetic standpoint, it might be more efficient to use a slightly smaller field (e.g. 62-bits). This way, you can enable extra optimizations by implementing branchless modular multiplication.

Yes, this is a good point. At the moment I’m using p = 2^{64} - 9 \cdot 2^{28} + 1, which has a simple and fast Crandall reduction, but doesn’t have space for any delayed reductions. Another member of our team is looking into other options for small fields.

---

**Pratyush** (2021-02-23):

Re the GMiMC issue, you can still run the hash only over the prime base field, no? Another approach would be to set the constraint field to be the prime base field, but perform the protocol (RS-IOPP + FRI) over the extension field.

---

**dlubarov** (2021-02-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/pratyush/48/4986_2.png) Pratyush:

> you can still run the hash only over the prime base field, no?

Ah yeah. I was imagining hashing in the extension field, but this makes more sense. Was that also what you were recommending [@bobbinth](/u/bobbinth)? Sorry if I misunderstood.

With that approach, I think the costs would be very similar to my plan of running three commit phases – in either case, the leaves of the commit phase oracles would consist of three 64-bit elements.

I guess using a field extension does feel like a cleaner approach though, since it feels closer to the FRI spec, so it’s more obvious that the paper’s soundness analysis still applies.

---

**bobbinth** (2021-02-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> Was that also what you were recommending @bobbinth

Yep, an element in an extension field is represented by either 2 or 3 elements from the base field, depending on whether it is a quadratic or cubic extension. So, you can still hash them with a hash function which works over the base field.

If you are going with the extension field route, there might be another thing to keep in mind: you might need to prove that original polynomials were in the base field (and not in the extension field). This can be done using a conjugate constraint as described in section 3.8.2 in [here](https://docs.google.com/viewer?url=https://github.com/starkware-libs/ethSTARK/raw/master/rescue_stark_documentation.pdf).

---

**bobbinth** (2021-02-25):

Btw, you might have seen this already, but some time ago I’ve implemented Rescue, Poseidon, GMiMC in a 64-bit field and wrote up a short analysis of it [here](https://ethresear.ch/t/performance-of-rescue-and-poseidon-hash-functions/7161). I’ve since updated the implementations to be in a 128-bit field - but you might find the comparison interesting (one note, with the latest release of Rescue Prime, Rescue would be about 2x faster than in my original implementation).

---

**dlubarov** (2021-02-25):

Oh cool, I hadn’t seen that. We’re seeing really high GMiMC throughput in our prototype – around 10 million (~512 bit to ~256 bit) hashes per second on my i7-9750H laptop (6 cores, 2.6 GHz). We’ll open source it when it’s more finished. Some more details –

- As mentioned I used a Crandall field, p = 2^{64} - 9 \cdot 2^{28} + 1, but I agree we could probably do even better with a 62-63 bit field.
- I used the accumulation technique mentioned in 4.2 here to save some additions compared to the obvious implementation of GMiMC.
- I unrolled the whole thing, and the round constants are in a const array so that (I assume) the compiler will make them immediate values.

For now our code is pure Rust, but I think AVX-512 has some instructions for widening 64-bit multiplication, so that would be interesting to look into also.

---

**bobbinth** (2021-03-01):

Wow - very cool! Is 10M on a single core? If so, that’s faster than sha2, no?

In terms of a small field, I think it’d be cool to have a field which has very efficient regular reduction, supports delayed reduction, and also has high order roots of unity (e.g. around 2^{40}). Not sure if some of these goals conflict with each other though.

---

**dlubarov** (2021-03-02):

Oh I was using all 6 of my cores. I think it’s a bit faster than a “plain” sha2 implementation, but implementations using `sha256rnds2` or SIMD might be a bit faster.

Agreed about those field properties. I think 2-adicity is somewhat at odds with reduction speed, at least if we’re using Crandall reductions, since a 2-adicity of k implies a distance of at least 2^k from a power of two. It might be interesting to search for 3-adic fields that are very close to a power of two, though I’m not sure how efficient ternary FFTs would be.

---

**bobbinth** (2021-04-01):

[@dlubarov](/u/dlubarov) - I am curious, what kind of speeds are you seeing for field multiplication in the 64-bit field you are using?

---

**dlubarov** (2021-04-02):

I’m seeing about 4ns per field mul (on a i7-9750H with Turbo Boost enabled). So around 18 cycles per mul, I think. I suspect it could be faster, but I haven’t looked at the asm yet. Our repo isn’t quite ready to be public, but here’s the [Crandall field code](https://gist.github.com/dlubarov/c35e67746bfc8b112a28ebc6513a80ce) if you’d like to see or time it.

Our teammate Hamish came up with several other interesting options for ~64 bit fields. One that seems promising to me is p = 2^{64} - 2^{32} + 1. Reductions should be really fast (just a few adds/subs), though the caveat is that the lowest-degree permutation monomial is x^7. Maybe that would work well with a hash like Poseidon.

---

**bobbinth** (2021-04-02):

Thanks! On my machine (Intel Core i9-9980KH @ 2.4 GHz) I’m seeing 1.3 ns / mul for your code.

I’ve also benchmarked a rudimentary implementation of Montgomery multiplication in a field with modulus 2^{61} + 1025 \cdot 2^{40} + 1, and I’m seeing about 1.3 ns / mul as well. For Montgomery multiplication I’m assuming the values are already in Montgomery form - so there will be an additional overhead of converting to/from Montgomery form, though, in practice, this overhead should be negligible.

However, since the field I’m using also supports delayed reduction, I’ve benchmarked that as well, and I’m getting about 0.9 ns / mul. So, it seems like Montgomery multiplication with delayed reduction outperforms both Crandall method and plain Montgomery method by about 30%.

---

**dlubarov** (2021-04-02):

Oh nice! Glad to hear that. That’s odd that we get such different numbers, but yours seem believable; there must be something fishy going on with my machine or compiler.

Makes sense that a Montgomery multiplication would be equally fast – I think both approaches involve 3 muls, two adds, and a conditional sub. But yeah maybe the Montgomery option is better since it gives more flexibility to pick any prime we’d like, depending on the desired permutation monomials, the desired room for delayed reductions, etc.

