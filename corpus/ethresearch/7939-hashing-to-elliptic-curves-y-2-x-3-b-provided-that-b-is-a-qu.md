---
source: ethresearch
topic_id: 7939
title: Hashing to elliptic curves $y^2 = x^3 + b$ provided that $b$ is a quadratic residue
author: dishport
date: "2020-09-04"
category: Cryptography
tags: []
url: https://ethresear.ch/t/hashing-to-elliptic-curves-y-2-x-3-b-provided-that-b-is-a-quadratic-residue/7939
views: 3432
likes: 2
posts_count: 11
---

# Hashing to elliptic curves $y^2 = x^3 + b$ provided that $b$ is a quadratic residue

Hi guys,

I wrote [a new article](https://www.researchgate.net/publication/344077207_Efficient_constant-time_hashing_to_elliptic_curves_y2_x3_b_provided_that_b_is_a_quadratic_residue)

[Hashing to elliptic curves y^2 = x^3 + b provided that b is a quadratic residue.pdf](/uploads/short-url/f3SrTaEMR7jrRskswQKCivPWXPE.pdf) (244.9 KB)

In my opinion, this is the most useful result for applied cryptography I have ever obtained. Please read its abstract:

> Let \mathbb{F}_{\!q} be a finite field and E_b\!: y_0^2 = x_0^3 + b be an ordinary elliptic \mathbb{F}_{\!q}-curve of j-invariant 0 such that \sqrt{b} \in \mathbb{F}_{\!q}. In particular, this condition is fulfilled for the curve BLS12-381 and for one of sextic twists of the curve BW6-761 (in both cases b=4). These curves are very popular in pairing-based cryptography. The article provides an efficient constant-time hashing h\!: \mathbb{F}_{\!q} \to E_b(\mathbb{F}_{\!q}) of an absolutely new type for which at worst \#\mathrm{Im}(h) \approx q/6. The main idea of our hashing consists in extracting in \mathbb{F}_{\!q} a cubic root instead of a square root as in the well known (universal) SWU hashing and in its simplified analogue. Besides, the new hashing can be implemented without quadratic and cubic residuosity tests (as well as without inversions) in \mathbb{F}_{\!q}. Thus in addition to the protection against timing attacks, h is much more efficient than the SWU hashing, which generally requires to perform two quadratic residuosity tests in \mathbb{F}_{\!q}. For instance, in the case of BW6-761 this allows to avoid at least approximately 2 \!\cdot\! 761 \approx 1500 field multiplications.

In your opinion, is this a useful result ? Please let me know in order to collaborate if any of companies or startups wants to use my hashing in its products. In this case I can implement it in one of programming languages.

Best regards.

## Replies

**vbuterin** (2020-09-04):

Interesting!

Quick question: does this apply to the altbn-128 curve as well, or no?

---

**dishport** (2020-09-04):

Unfortunately no, because for the altbn-128 curve the coefficient b = 3. It is a quadratic non-residue in the finite field. I will try to generalize my approach to this curve, but the task is very non-trivial, in my opinion.

---

**JustinDrake** (2020-09-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/dishport/48/4198_2.png) dishport:

> h is much more efficient than the SWU hashing

Oh, that’s great! I’m pleased to see you changed [your opinion](https://ethresear.ch/t/a-new-efficient-constant-time-hashing-to-some-barreto-naehrig-curves-including-bn256-and-bn512/7640/3) from earlier this year:

![](https://ethresear.ch/user_avatar/ethresear.ch/dishport/48/4198_2.png)[A new efficient constant-time hashing to some Barreto-Naehrig curves (including BN256 and BN512)](https://ethresear.ch/t/a-new-efficient-constant-time-hashing-to-some-barreto-naehrig-curves-including-bn256-and-bn512/7640/3)

> I think the hashing of Wahby-Boneh is quite optimal. I don’t see how to improve it.

A few questions:

1. How much faster is the hashing compared to Wahby-Boneh?
2. Have you tried implementing the function?

![](https://ethresear.ch/user_avatar/ethresear.ch/dishport/48/4198_2.png) dishport:

> for which at worst \#\mathrm{Im}(h) \approx q/6

Can you expand on this? Does this imply that your hash function does not behave like a random oracle (unlike Wahby-Boneh)?

---

**dishport** (2020-09-04):

> How much faster is the hashing compared to Wahby-Boneh?

My hashing is not much faster, because the Wahby-Boneh hashing uses an \mathbb{F}_{\!q}-isogeny \varphi of degree 11. This is a quite small degree. If [Horner’s method](https://en.wikipedia.org/wiki/Horner%27s_method) is applied for the image computation of \varphi, then it is sufficient approximately 50 field multiplications. However, in my opinion, the new hashing is more elegant)

My hashing is much faster if an elliptic curve does not have \mathbb{F}_{\!q}-isogenies of small degree.

> Have you tried implementing the function?

Not yet. I can try this if you are potentially interested in putting my hashing into practice. What programming languages do you use ?

> Can you expand on this? Does this imply that your hash function does not behave like a random oracle (unlike Wahby-Boneh)?

Sorry, I have no experience with random oracles, so I’m not sure I understand your question. I just estimated the image cardinality of the new hashing as a usual set map.

If I am not mistaken, the cardinality of the Wahby-Boneh hashing equals {\approx} 3q/(8 \!\cdot\! 11). Indeed, the image cardinality of the simplified SWU hashing is equal to {\approx} 3q/8 according to Propositon 4 of [Article](https://eprint.iacr.org/2010/037.pdf). However, the isogeny \varphi maps 11 points to one. Thus since 88/3 \approx 29.3, the image of my hashing has the cardinality at least 5 times more.

---

**JustinDrake** (2020-09-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/dishport/48/4198_2.png) dishport:

> My hashing is not much faster

Understood. The Boneh-Wahby hash function is being standardised by IETF for use across various blockchain projects. At this point in time a significant speedup is probably required to displace Boneh-Wahby.

![](https://ethresear.ch/user_avatar/ethresear.ch/dishport/48/4198_2.png) dishport:

> in my opinion, the new hashing is more elegant

That’s great. BTW, have you considered publishing on ePrint? ePrint tends to get much visibility within the cryptography and blockchain space than ResearchGate.

![](https://ethresear.ch/user_avatar/ethresear.ch/dishport/48/4198_2.png) dishport:

> Sorry, I have no experience with random oracles, so I’m not sure I understand your question.

On page 3 of [the Boneh-Wahby paper](https://eprint.iacr.org/2019/403.pdf) there is a section titled “Hash functions to curves as random oracles”. By “behaving like a random oracle” I mean that the hash function is indifferentiable from a random oracle.

---

**dishport** (2020-09-04):

> BTW, have you considered publishing on ePrint?

Yes, I also submitted the text to ePrint. It should be published in several days.

---

**kobigurk** (2020-09-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/dishport/48/4198_2.png) dishport:

> if an elliptic curve does not have Fq\mathbb{F}_{!q} -isogenies of small degree.

What do you consider a small degree?

---

**dishport** (2020-09-06):

Since \sqrt[3]{b} \not\in \mathbb{F}_{\!q} (i.e., there are no \mathbb{F}_{\!q}-points of order 2) for all curves used in practice, we can suppose that the degree d of an \mathbb{F}_{\!q}-isogeny \varphi\!: E \to E_b is odd, where j(E) \neq 0. In this case, according to Vélu’s formulae we obtain

\varphi = \left( \dfrac{\varphi_0(x)}{\varphi_1(x)}, y\dfrac{\varphi_2(x)}{\varphi_3(x)} \right),

where \varphi_i are \mathbb{F}_{\!q}-polynomials such that

\deg(\varphi_0) = d, \qquad \deg(\varphi_1) = d-1, \qquad
\deg(\varphi_2) = \deg(\varphi_3) = 3(d-1)/2

if I am not mistaken. Thus in general Horner’s method requires \approx 5d field multiplications in order to compute the image of \varphi. You decide for yourself whether it’s a lot or not.

---

**dishport** (2020-12-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> On page 3 of the Boneh-Wahby paper  there is a section titled “Hash functions to curves as random oracles”. By “behaving like a random oracle” I mean that the hash function is indifferentiable from a random oracle.

For any map h\!: \mathbb{F}_{\!q} \to E_b(\mathbb{F}_{\!q}) consider its tensor square

h^{\otimes 2}\!: \mathbb{F}_{\!q}^2 \to E_b(\mathbb{F}_{\!q}), \qquad h^{\otimes 2}(u,v) = h(u) + h(v).

In practice h^{\otimes 2} is taken in the place of h, because the scientific society does not know hashings of the form h\!: \mathbb{F}_{\!q} \to E_b(\mathbb{F}_{\!q}) indifferentiable from a random oracle if E_b is non-supersingular.

I proved that h_{new}^{\otimes 2} for my map h_{new} is indifferentiable from a random oracle at least for q \equiv 4, 7 (mod 9). I will update my text in the near future.

However h_{BW}^{\otimes 2} for the Boneh–Wahby map h_{BW} is not even surjective, hence it is not indifferentiable from a random oracle. Indeed, as I have already said earlier, Boneh and Wahby use the simplified SWU map h_{SSWU}\!: \mathbb{F}_{\!q}\to E(\mathbb{F}_{\!q}) and an \mathbb{F}_{\!q}-isogeny \varphi\!: E \to E_b such that \ker(\varphi) \subset E(\mathbb{F}_{\!q}). More precisely,

h_{BW}^{\otimes 2} = \varphi \circ h_{SSWU}^{\otimes 2} = (\varphi \circ h_{SSWU})^{\otimes 2}.

Since \{0\} \neq \ker(\varphi) \subset E(\mathbb{F}_{\!q}) and \#E(\mathbb{F}_{\!q}) = \#E_b(\mathbb{F}_{\!q}), the map \varphi\!: E(\mathbb{F}_{\!q}) \to E_b(\mathbb{F}_{\!q}) is not surjective. Therefore h_{BW}^{\otimes 2} cannot be surjective, namely \#\mathrm{Im}(h_{BW}^{\otimes 2}) = \#E_b(\mathbb{F}_{\!q})/\mathrm{deg}(\varphi). In particular, for BLS12-381 the degree \mathrm{deg}(\varphi) = 11.

However h_{BW}^{\otimes 2} is indifferentiable from a random oracle in its image \mathrm{Im}(h_{BW}^{\otimes 2}) and this is sufficient in practice, because only prime cyclic subgroups are considered for the discrete logarithm problem.

---

**dishport** (2020-12-18):

Good day.

I rewrote my article, providing a proof of the indifferentiability from a random oracle (at least for q \equiv 4 (mod 9)) for the new hashing H\!: \{0,1\}^* \to E_b(\mathbb{F}_{\!q}). [The latest version](https://eprint.iacr.org/2020/1070) posted on ePrint IACR.

The new abstract:

> Let \mathbb{F}_{\!q} be a finite field and E_b\!: y^2 = x^3 + b be an ordinary elliptic \mathbb{F}_{\!q}-curve of j-invariant 0 such that \sqrt{b} \in \mathbb{F}_{\!q}. In particular, this condition is fulfilled for the curve BLS12-381 and for one of sextic twists of the curve BW6-761 (in both cases b=4). These curves are very popular in pairing-based cryptography. The article provides an efficient constant-time encoding h\!: \mathbb{F}_{\!q} \to E_b(\mathbb{F}_{\!q}) of an absolutely new type for which q/6 \leqslant \#\mathrm{Im}(h). We prove that at least for q \equiv 4 \ (\mathrm{mod} \ 9) the hash function H\!: \{0,1\}^* \to E_b(\mathbb{F}_{\!q}) induced by h is indifferentiable from a random oracle. The main idea of our encoding consists in extracting in \mathbb{F}_{\!q} (for q \equiv 1 \ (\mathrm{mod} \ 3)) a cubic root instead of a square root as in the well known (universal) SWU encoding and in its simplified analogue. Besides, the new hashing can be implemented without quadratic and cubic residuosity tests (as well as without inversions) in \mathbb{F}_{\!q}. Thus in addition to the protection against timing attacks, H is much more efficient than the SWU hash function, which generally requires to perform 4 quadratic residuosity tests in \mathbb{F}_{\!q}. For instance, in the case of BW6-761 this allows to avoid approximately 4 \!\cdot\! 761 \approx 3000 field multiplications.

The condition q \equiv 4 (mod 9) is fulfilled for the curve BW6-761. Does anyone use this curve among you? I would be very grateful if you could inform your friends who use this curve about the new hash function. I could help them to implement it.

Best regards, Dimitri.

