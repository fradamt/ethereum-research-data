---
source: ethresearch
topic_id: 5402
title: Fixed-modulus timelock puzzles
author: JustinDrake
date: "2019-05-02"
category: Sharding
tags: [random-number-generator]
url: https://ethresear.ch/t/fixed-modulus-timelock-puzzles/5402
views: 5065
likes: 7
posts_count: 11
---

# Fixed-modulus timelock puzzles

**TLDR**: We show how to create timelock puzzles targetting RSA VDF ASICs with a hardcoded modulus.

**Context**

A key design decision for RSA VDF ASICs is whether or not the modulus should be hardcoded or programmable. There are reasons to have it hardcoded. These include reduced latency, power consumption, cooling, die area, complexity, and cost.

The main argument for a programmable modulus is that [Rivest-Shamir-Wagner timelock puzzles](https://people.csail.mit.edu/rivest/pubs/RSW96.pdf) require a programmable modulus (to be chosen by the puzzle creator). In this post we present a modified timelock scheme which works with a fixed modulus.

**Construction**

Let N be a fixed modulus of unknown factorisation. Let t be a time parameter. Assume that 2^{2^t} \mod N (i.e. the VDF output for the input 2) is known as a public parameter (see next section for construction). A puzzle creator can now uniformly sample a large enough (e.g. 128-bit) secret s and propose 2^s \mod N as a puzzle input.

Notice that the corresponding output \big(2^s\big)^{2^t} = \big(2^{2^t}\big)^s can easily be computed knowing s. Without knowledge of s the input 2^s \mod N is indistinguishable from random, and therefore the corresponding output must be evaluated the “slow” way with repeated squarings.

**Public parameters**

It remains to show how to compute the public parameter 2^{2^t} \mod N. For small t it suffices for anyone to run the computation and share the output. For large t, if an MPC generated N, the MPC can be extended to also generate 2^{2^{2^i}} \mod N for a few i. For example, if the RSA VDF ASIC runs at 1ns per modular squaring then choosing i = 52, ..., 60 would allow for decade-long timelock puzzles.

**Edit**: Notice that the construction also allows to do timelock puzzles with class groups.

## Replies

**marckr** (2019-05-12):

This is great! Thank you for sharing.

I have several thoughts about VDF ASICs however drawing from graph theory instead.

One thing I would like to mention for consideration with respect to hard coded ASIC modulus is Moti Yung’s paper [Cliptography: Clipping the Power of Kleptographic Attacks](https://eprint.iacr.org/2015/695.pdf).

Will look this over as time permits.

**Edit:** Does this get around [Tonelli-Shanks](https://en.wikipedia.org/wiki/Tonelli%E2%80%93Shanks_algorithm)? I haven’t looked at this in a while.

Rock on Justin.

---

**thor314** (2019-05-12):

Apologies for the basic question, I’m trying to understand what the key insight here is. I understand solving s in 2^s \mod N is just RSA. Is the insight that for large t, MPC may generate 2^{2^{2^i}} as a solution to (2^s)^{2^t}, resulting in a very slow puzzle?

---

**marckr** (2019-05-12):

Justin:

If and when you have a chance, would be curious if this pertains: [The GHS Attack Revisited](https://iacr.org/archive/eurocrypt2003/26560374/26560374.ps)

Although, given that you are posting wrt RSA it’s likely unsuited. Had been looking into this area in specific, but rather mystified at the end. It is hard to constraint insight into class groups away from elliptic curve cryptography.

Had been looking into this however. Perhaps this is better to post elsewhere?

As a friend once told me: always look into complex analysis, as you can reframe many a problem through it.

---

**marckr** (2019-05-12):

[![vdf](https://ethresear.ch/uploads/default/optimized/2X/f/f83b5712a0d47365734727d7a0a7aa2309265d05_2_690x479.png)vdf1760×1222 268 KB](https://ethresear.ch/uploads/default/f83b5712a0d47365734727d7a0a7aa2309265d05)

From [A Survey of Two Verifiable Delay Functions](https://eprint.iacr.org/2018/712.pdf). So the additional exponentiation allows the indexing, like a scatter gather? It’s actually been a bit since I looked at VDF per se.

Related is the [Phi-hiding assumption](https://en.wikipedia.org/wiki/Phi-hiding_assumption) for RSA. I sort of cut short after going down this line, but very interested in VDF research.

I have a good time lock cryptography paper I printed over a year ago somewhere around here… [How to build good Time Lock Encryption](https://eprint.iacr.org/2015/482.pdf). Boy did I spend a lot of time thinking about this space for no result yet.

---

**JustinDrake** (2019-05-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/thor314/48/11146_2.png) thor314:

> I’m trying to understand what the key insight here is

In the traditional timelock scheme (RSW96) the timelock puzzle creator can skip the time-consuming sequential computation (namely, repeated modular squaring) by choosing a modulus `N` for which he knows the factorisation. You can think of the timelock puzzle creator as hiding a secret in the modulus `N`.

With VDF ASICs where the modulus `N` is hardcoded (and of unknown factorisation to everyone) we don’t have the freedom to embed secrets in the modulus. The “key idea” is for the timelock creators to instead embed secrets in the input. It turns out the construction is quite elegant and straightforward.

![](https://ethresear.ch/user_avatar/ethresear.ch/marckr/48/1636_2.png) marckr:

> rather mystified at the end. It is hard to constraint insight into class groups

The traditional timelock scheme (RSW96) works because of the particular algebra of RSA groups. Specifically, by knowing the factorisation of the modulus `N`, the timelock puzzle creator can construct a group which is of known order to him (and hence is able to reduce the exponent 2^t by the Euler totient \phi(N)), but of unknown order to the rest of the world.

On the other hand, class groups (as used by Chia in the context of VDFs without a trusted setup) are groups of unknown order to everyone, without the special algebra that RSA groups have. The goods news is that the modified timelock scheme only requires a group of unknown order, so works for both RSA groups and class groups.

---

**marckr** (2019-05-12):

Thanks for the clear analysis, Justin!

If we have groups of unknown order, would Phi-sampling be an issue then or are these without quadratic residue in the base exponent? You were quite clear, but a “scatter gather” sampling from a trusted oracle is how I’d been thinking of the intractability of distinguishing higher-order residue from non-residues. As far as I know that is where the security of RSA comes from.

If each puzzle creator is separate, however, and on a common homomorphic strip, it really comes down to the algebra and becomes then a boolean search vs decision problem with logic synthesis.

Very interested to see how this research evolves.

---

**JustinDrake** (2019-05-13):

Sorry Mark I don’t understand the following concepts, especially in the context of timelock puzzles ![:flushed_face:](https://ethresear.ch/images/emoji/facebook_messenger/flushed_face.png?v=14)

“Phi-sampling”, “quadratic residue in the base exponent”, “scatter gather sampling”, “trusted oracle”, “higher-order residue”, “common homomorphic strip”, “boolean search”, “logic synthesis”.

---

**marckr** (2019-05-15):

I have a response, and I may edit this post later, but I had to tend myself elsewhere. Don’t want to just leave a bunch of jargon that we are all trying to figure out anyway as it is what is under the hood after all.

My understanding, and this may be quite flawed:

The RSA problem is based on intractability of solving integer factorization via congruences. This can equally be framed in sampling for Phi or the totient by finding co-prime congruences. This then gives the prospect of higher order residue that could factor through the Phi component by iteration.

Was thinking aloud of the prospect to have a trusted oracle to place the orders of the exponents, possibly via an MPC, but that defeats much of the purpose of privacy in a key. Thought this could be conceptually similar to scatter gather as in I/O vectorization, but that is rather vague, especially if I am missing with these concepts. Simply don’t have the time to refine presently.

From what I can see, in the VDF form you basically are generating a homomorphic sequence, that is a Turing tape with commit-reveal schemes as encoded “lock boxes”. Remember, TrueBit is rather basic ultimately and fully outsources the need for any developer to look seriously at the functionality of commit-reveal schemes. You can see it is often the magic box in quite a few leading projects with of course solid documentation. Regardless, taking this to an ASIC and hardware level would then bring up logic synthesis and the difference between search vs decision problems. I don’t have the time to clarify on this, but maybe the opportunity will arise.

Actually if you want to know something wild, bit-by-bit composition:

[![bitbybit](https://ethresear.ch/uploads/default/optimized/2X/1/14b7fa6b6b77423b4de4aea56ff782e397412fee_2_690x471.png)bitbybit2004×1368 403 KB](https://ethresear.ch/uploads/default/14b7fa6b6b77423b4de4aea56ff782e397412fee)

From [Commitment Reveal Schemes, Lecture 14, NYU](https://cs.nyu.edu/courses/fall08/G22.3210-001/lect/lecture14.pdf). And now I see it was Victor Shoup’s graduate class. What have I been doing in crypto this year? I have to chuckle at the irony (Where is the commitment of Ethereum into it’s community?)

Sometimes feeling your way toward a solution draws all kinds of lateral thinking. Communicating it however is a process of iteration and I am sitting here writing while market prices are exploding, cannot attend Consensus, or get any sort of financial traction from the Ethereum community. You guys are cool and I am onboard, but well these problems have a life of their own and perhaps many of you are in a similar conundrum and it should be left there.

Keep it up. Coming to the researcher workshop in NYC tomorrow Justin?

---

**jdbertron** (2021-04-20):

You’re not making any sense.

---

**jdbertron** (2021-09-01):

Wow, Justin, you were right in time with this one: https://eprint.iacr.org/2019/635.pdf

