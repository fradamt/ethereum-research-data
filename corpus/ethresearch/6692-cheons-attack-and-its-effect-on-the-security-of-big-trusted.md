---
source: ethresearch
topic_id: 6692
title: Cheon's attack and its effect on the security of big trusted setups
author: kobigurk
date: "2019-12-26"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/cheons-attack-and-its-effect-on-the-security-of-big-trusted-setups/6692
views: 8903
likes: 64
posts_count: 31
---

# Cheon's attack and its effect on the security of big trusted setups

Thanks to Ariel Gabizon and Zac Williamson for collaborating on the post, and the authors of [Marlin](https://eprint.iacr.org/2019/1047.pdf) for highlighting the attack and its importance.

## The attack

[Cheon](http://www.math.snu.ac.kr/~jhcheon/publications/2010/StrongDH_JoC_Final2.pdf) shows that if you’re given g, g^\alpha and g^{\alpha^d}, where g is an element of a group of order p and d | p -1, then it’s possible to find \alpha in 2\left(\left\lceil\sqrt{\frac{p - 1}{d}}\right\rceil + \left\lceil\sqrt{d}\right\rceil\right)\cdot \left(\mathsf{Exp}_{\mathbb{G}}(p) + \log{p} \cdot \mathsf{Comp}_{\mathbb{G}}\right) operations, where \mathsf{Exp}_{\mathbb{G}}(n) means the cost of one exponentiation of an element in \mathbb{G} by a positive integer less than n amd \mathsf{Comp}_{\mathbb{G}} means the cost to determine if two elements of \mathbb{G} are identical. By assuming that \mathsf{Exp}_{\mathbb{G}}(p) dominates \mathsf{Comp}_{\mathbb{G}} and that the \log{p} factor can be ignored when using a hash table, the cost formula can be simplified to be approximately 2\left(\left\lceil\sqrt{\frac{p - 1}{d}}\right\rceil + \left\lceil\sqrt{d}\right\rceil\right)\cdot \mathsf{Exp}_{\mathbb{G}}(p). The storage cost is \max\left\{{\left\lceil\sqrt{\frac{p-1}{d}}\right\rceil}, \left\lceil\sqrt{d}\right\rceil\right\} elements of \mathbb{G}.

For more intuition on how the attack works, check out [Ariel’s write-up](https://hackmd.io/2oUhPtzWSRulLQ83Ctoy_g).

Cheon uses Baby-step Giant-step as the main part of the attack, and it’s possible to use Pollard’s Rho instead.

When using Pollard’s Rho algorithm, we can either use a large memory or a constant memory version, as mentioned in [3]. For the large memory version, i.e. which requires saving around 1.25\left(\sqrt{\frac{p-1}{d}} + \sqrt{d}\right) elements of \mathbb{G}, the expected number of evaluations (which roughly mean exponentiations) is 1.25\left(\sqrt{\frac{p-1}{d}} + \sqrt{d}\right). For the constant memory version, the expected number of evaluations is 3.09\left(\sqrt{\frac{p-1}{d}} + \sqrt{d}\right) and 1.03\left(\sqrt{\frac{p-1}{d}} + \sqrt{d}\right) comparisons.

The Marlin authors also noticed that if you’re given g, g^\alpha and g^{\alpha^d} and h, h^\alpha and h^{\alpha^d} where g is a generator of \mathbb{G}_1 and h is a generator of \mathbb{G}_2, it’s also possible to use the pairing to transfer the problem into \mathbb{G}_T: e(g^{\alpha^m}, h^{\alpha^n}) = e(g,h)^{\alpha^{m+n}}.

## The impact

This is particularly relevant for trusted setups that have been performed in the past and are being performed at the moment. Solving for \tau allows for the possibilty of breaking soundness.

1. Zcash Powers of Tau - Sapling - BLS12-381 - we have up until g^{\tau^{2^{22} - 1}} in \mathbb{G}_1 and g^{\tau^{2^{21}}} in \mathbb{G}_2
2. AZTEC PLONK setup - BN254 - we have g^{\tau^{3 \cdot 2^{25}}}  in \mathbb{G}_1
3. Perpetual Powers of Tau - BN254 - we have up until g^{\tau^{2^{29} - 1}} in \mathbb{G}_1 and g^{\tau^{2^{28}}} in \mathbb{G}_2
4. Filecoin Powers of Tau - BLS12-381 - we have up until g^{\tau^{2^{28} - 1}} in \mathbb{G}_1 and g^{\tau^{2^{27}}} in \mathbb{G}_2

Let’s take the biggest one to show the potential impact - Perpetual Powers of Tau. By the Cheon method with Pollard’s Rho, we can solve DLP in \mathbb{G}_1 for \tau in 1.25\left(\sqrt{\frac{2^{254}}{2^{28}}} + \sqrt{2^{28}}\right) \approx 2^{114}, so at most 2^{114} exponentiations, or 114-bit security. For BN254, the impact is not severe, since there are other NFS-based attacks that lower the security to around [110-bit security](https://github.com/zcash/zcash/issues/714#issuecomment-290959691). You could also transfer the method to \mathbb{G}_T, and get 1.25\left(\sqrt{\frac{2^{254}}{2^{29}}} + \sqrt{2^{29}}\right)  \approx 2^{114}, but the operations in \mathbb{G}_T are significantly more expensive.

For BLS12-381 setups, the impact might be more meaningful. The goal was to design a curve with 128-bit security, and the trusted setup lowers is. In the Filecoin parameters, this translate to 1.25\left(\sqrt{\frac{2^{255}}{2^{27}}} + \sqrt{2^{27}}\right) \approx 2^{114}, so at most 2^{114} exponentiations.

This is also relevant to other projects which will perform a trusted setup:

1. Projects that are using curves mentioned in Zexe, such as Celo and possibly EYBlockchain
2. Coda that uses MNT4753 and MNT6753
3. Projects that are using curves mentioned in DIZK

## Conclusion

Future projects that target 128-bit security should also consider this attack, which has become relevant because of the growing size of circuits.

This might also be a benefit of updatable setups, such as can be done for PLONK, Marlin and Sonic - you can estimate the amount of time it would take to solve for \tau and make sure the SRS is updated before that.

## References

[1] Cheon, Jung Hee. “Discrete logarithm problems with auxiliary inputs.” Journal of Cryptology 23.3 (2010): 457-476.

[2] Kozaki, Shunji, Taketeru Kutsuma, and Kazuto Matsuo. “Remarks on Cheon’s algorithms for pairing-related problems.” International Conference on Pairing-Based Cryptography. Springer, Berlin, Heidelberg, 2007.

[3] Bai, Shi, and Richard P. Brent. “On the efficiency of Pollard’s rho method for discrete logarithms.” Proceedings of the fourteenth symposium on Computing: the Australasian theory-Volume 77. Australian Computer Society, Inc., 2008.

[4] Chiesa, Alessandro, Yuncong Hu, Mary Maller, Pratyush Mishra, Noah Vesely, and Nicholas Ward. Marlin: Preprocessing zkSNARKs with Universal and Updatable SRS. Cryptology ePrint Archive, Report 2019/1047, 2019.

[5] Gabizon, Ariel, Zachary J. Williamson, and Oana Ciobotaru. PLONK: Permutations over Lagrange-bases for Oecumenical Noninteractive arguments of Knowledge. Cryptology ePrint Archive, Report 2019/953, 2019.

## Replies

**vbuterin** (2019-12-27):

To me, this sounds like this attack negates the advantage that BLS-12-381 has over alt-bn128. In which case, the main practical consequence is that projects that aren’t already committed to BLS-12-381 should not worry so much about upgrading because the benefit is lower?

---

**kobigurk** (2019-12-27):

That’s a good point. I’d say this also depends on the application. For Zcash-sized circuits (\approx 2^{21}), the effect is not that big and leaves a big margin of security over BN.

Another avenue that we discussed (Ariel, Zac, me) is searching for a curve with a bigger group size (e.g., + 40 bits) to negate the effect.

---

**Mikerah** (2019-12-27):

Is it safe to say that a takeaway from this is to stick with the well-used and audited curves and use updateable SNARK schemes?

---

**Recmo** (2019-12-28):

For each doubling of d you loose half a bit of security. For realistic upper bounds for d, say 2^{30}, you would need only +15 bits in the order to compensate.

But what about the d \vert p - 1 requirement? If I look at the factorization of p-1 for the BN254 curve (please check that I got the order right, it’s strangely hard to find concrete parameters for BN254 online):

2^3 \cdot 3 \cdot 1279341515037335760923230309485547607615095952161030647804445804731813728599

The final factor is > 2^{249}, so can not appear in d, that leaves the highest choice for d as 24, which gives an attack complexity of 2^{127.32}, i.e. we only loose negligible 0.7 bits of security.

Edit: Looks like a variant mention in the paper works for d \vert p + 1, which factors as:

2 \cdot 31 \cdot 485115557 \cdot 1020847438134909471455349635706891684178805671318695707584770673967

 2^{28} < 485115557 < 2^{29} so only Perpetual Powers of Tau should be worried?

---

**kobigurk** (2019-12-28):

The p - 1 is of the group order p = 21888242871839275222246405745257275088548364400416034343698204186575808495617, which has a 2^{28} factor in it. Since we’re talking about the curve prime subgroup order, this affects all of the curves that we mentioned.

And yeah, the +40 bits is just an example of something that definitely negates this attack, we can probably use something smaller if we care more about efficiency than a higher safety margin.

---

**Recmo** (2019-12-28):

Ah, yes, that makes p-1 and p+1 pretty smooth numbers.

As an alternative mitigation strategy (for sake of curiosity, bumping the size is probably the way to go), how realistic would it be to look for a curve where p-1 and p+1 have mostly large factors?

---

**kobigurk** (2019-12-28):

p+1 doesn’t necessarily have to be pretty smooth. For example, if p-1 has a large 2^n factor, p+1 won’t.

The problem with having p-1 with mostly large factors is that FFTs won’t be as efficient. It’s common today to use a radix-2 FFT (or multi-radix in the case of Coda), where you use the small factor in each step of the recursion

---

**ebfull** (2019-12-28):

This doesn’t seem right. “alt-bn128” has less than 100 bits of security (not 110, as the OP linked) against NFS.


      [eprint.iacr.org](https://eprint.iacr.org/2017/334.pdf)


    https://eprint.iacr.org/2017/334.pdf

###

482.23 KB








BLS12-381 has about 117-120 bits of security under the same attack – which seems pretty close to the effect that Cheon’s attack has with Sapling’s setup.

---

**JustinDrake** (2019-12-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/recmo/48/3666_2.png) Recmo:

> For realistic upper bounds for d , say 2^{30}

As a side note I expect we’ll be able to easily go beyond d=2^{30} with hardware acceleration, and that there will be demand for these larger circuits. My very rough guesstimate based on preliminary VDF ASIC numbers is that one could build a 1 Watt core that does elliptic curve addition in ~1ns. So given a rig with 256 such cores one could do about 2^{30} multiexponentiations per second.

The other computational (and memory) bottleneck is FFTs but I believe we can tradeoff FFTs for multiexponentiations for SNARKs such as PLONK and SLONK (writeup to be published soon). As such, I’d set d=2^{40} as a more realistic upper bound ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**daira** (2019-12-28):

Note that we did consider this attack during the design of Sapling / BLS12-381. I seem to remember we came to similar conclusions then to what [@ebfull](/u/ebfull) says [above](https://ethresear.ch/t/cheons-attack-and-its-effect-on-the-security-of-big-trusted-setups/6692/9), i.e. that it’s not a significantly better attack than TNFS against Sapling. Of course it does have a greater effect for larger d.

[Edited 2021-09-03: according to the security estimates for STNFS at [Pairing-friendly curves – Aurore GUILLEVIC](https://members.loria.fr/AGuillevic/pairing-friendly-curves/) and the code at [tnfs-alpha / alpha · GitLab](https://gitlab.inria.fr/tnfs-alpha/alpha), the security of BLS12-381 against STFNS is ~126 bits. So the Cheon attack for trusted setups using BLS12-381, e.g. Sapling’s setup, does give a security level lower by a few bits (see [below](https://ethresear.ch/t/cheons-attack-and-its-effect-on-the-security-of-big-trusted-setups/6692/16)) than STNFS, although it is not lower than we previously conservatively estimated for STNFS.]

---

**arielgabizon** (2019-12-28):

I think it popped out of our heads, at least mine, for a little while, otherwise we wouldn’t have claimed bls-381 has 128 bits security here https://electriccoin.co/blog/new-snark-curve/.

I think it’s hard to really estimate the best nfs attack. Generally speaking

you’re moving to a field of ~4000 bits instead of 3000 bits in bls vs bn254; so it should give you *something*

---

**ebfull** (2019-12-28):

I think quite a bit of time elapsed between when we first settled on BLS12-381 (the blog post) and when we actually finished designing Sapling, which was roughly when we started looking closer at NFS and e.g. the NCC audit finished. We concluded that there wasn’t another curve for us to move to that gave a sufficient security boost without significant performance loss.

---

**kobigurk** (2019-12-28):

Thanks for the correction on the security of “alt-bn128”, I was looking at old results.

The focus of the post is indeed larger setups than Sapling’s Powers of Tau (like I mentioned in another reply) - there are pretty large setups in the wild at the moment.

---

**daira** (2019-12-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/kobigurk/48/13100_2.png) kobigurk:

> This is also relevant to other projects which will perform a trusted setup:
>
>
> […]
> 2. Coda  that uses MNT4753 and MNT6753

Don’t the Coda curves have much larger groups, so that this attack is not significant?

---

**daira** (2019-12-29):

For BLS12-381 in Sapling, d = 2^{21}, so we have 2^{117.2} *exponentiations* in the subgroup of d'th powers in \mathbb{F}_p^* which should have the same cost as roughly 255 \cdot 2^{117.2} \approx 2^{125.2} \mathbb{F}_p^* multiplications. Sapling had a design strength of \sim\!125 bits (limited by the 251-bit hash \mathsf{CRH^{ivk}} and the subgroup size of Jubjub). Yes the blog post and/or the protocol spec should mention the Cheon attack, even if only to say that it isn’t a problem for Sapling. I’ve [opened a ticket](https://github.com/zcash/zips/issues/310).

(It’s reasonable to measure the cost in multiplications, because the cost of square-root DL attacks is normally measured in group operations which are comparable, to within a small constant factor, to multiplications in \mathbb{F}_p^*. More precisely a group operation takes about [9 to 14 \mathbb{F}_p multiplications](https://www.hyperelliptic.org/EFD/g1p/auto-shortw-projective.html), so [for comparison with Pollard rho or Pollard kangaroo] the 2^{125.2} \mathbb{F}_p^* multiplications above correspond to at least 2^{122} group operations.)

[Edited 2021-09-03 to give a more precise estimate accounting for d = 2^{21} for the Sapling setup, not 2^{27} as in the Filecoin setup.]

For historical interest, let’s also compute this for BN-254 in Sprout. Again d = 2^{21}, but the group order is slightly smaller, so we have 2^{116.6} exponentiations in the subgroup of d'th powers in \mathbb{F}_p^* which should have the same cost as roughly 254 \cdot 2^{116.6} \approx 2^{124.6} \mathbb{F}_p^* multiplications. For comparison with Pollard rho or Pollard kangaroo, this would correspond to at least 2^{121.4} group operations.

---

**kobigurk** (2019-12-29):

Oh, you’re right, they do, about 750 bit groups. Definitely not relevant there ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

---

**daira** (2019-12-30):

Just to clarify, the smoothness of other factors of p-1 and p+1 doesn’t matter. The Cheon algorithm can only compute the \tau for which \{g, g^\tau, g^{\tau^d}\} is given [corrected], and in the zk-SNARK context, that is only given up to the d determined by the setup. There is indeed a variant of the algorithm that works with p+1, but only if g^{\tau^{0..2d}} is given for d a factor of p+1. In the zk-SNARK context that variant doesn’t help because p+1 will not be highly 2-adic, and even if it were we don’t have any extra g^{\tau^i} available.

---

**kobigurk** (2019-12-30):

Small note - for the p-1 variant, we only need g, g^\tau g^{\tau^d}, and not the elements in between. In the zk-SNARK context we indeed have them though.

---

**arielgabizon** (2019-12-31):

though there’s no concrete attack for now using smoothness of other factors, intuitively it feels safest to me to have a p-1 that just has  a large prime factor besides the power of 2 used for the FFT. So I wonder if we could construct a curve like that.

---

**daira** (2019-12-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/arielgabizon/48/4002_2.png) arielgabizon:

> intuitively it feels safest to me to have a p-1 that just has a large prime factor besides the power of 2 used for the FFT

Can you explain the intuition? I haven’t before seen anyone suggesting we need to care about factors of p-1 for security reasons, either in pairing or non-pairing curves.

(An extreme case for example is NIST P224:

> sage: factor((2^224 - 2^96 + 1)-1)
> 2^96 * 3 * 5 * 17 * 257 * 641 * 65537 * 274177 * 6700417 * 67280421310721

)


*(10 more replies not shown)*
