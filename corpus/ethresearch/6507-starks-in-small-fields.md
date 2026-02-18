---
source: ethresearch
topic_id: 6507
title: STARKs in small fields
author: bobbinth
date: "2019-11-26"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/starks-in-small-fields/6507
views: 1794
likes: 1
posts_count: 5
---

# STARKs in small fields

It seems to me that using small fields (e.g. 64 bits) for STARKs would have a number of advantages. Specifically:

1. Proof sizes would be smaller. For example, with 256-bit fields, every state register adds about 1KB to proof size. With 64-bit fields, every state register would contribute 1/4 of that.
2. Hash functions would be more efficient. For example, for such hash functions as Rescue/Poseidon, the number of rounds can be reduced by almost 50% if we use a large number of 64-bit registers vs. a small number of 256-bit registers.
3. Computations would run faster. With 64-bit fields we can do all modular math with just a few native instructions.

It seems to me that the main drawback of using small fields is that 256-bit modular arithmetic becomes way more complex. And this makes it more difficult to work with elliptic curves. Are there any other reasons to avoid small fields?

Also, maybe there is an efficient way to do 256-bit modular arithmetic with 64-bit registers?

## Replies

**Levalicious** (2020-07-19):

There is a semi-efficient way to do all this in 64 bit registers, however the downside is that it is hard to do comparisons and moduli with a specific modulus. Residue numeral systems allow carry-less multiplication, addition, and subtraction, but they don’t have a prime modulus for the overall field, and I’m not sure how that affects the security.

Any way I could reach out to you to discuss STARKs and RNS?

---

**bobbinth** (2020-07-19):

Since this post I’ve learned that there are some complications with STARKs in very small fields. Specifically, FRI needs to be done in a field which is over ~120 bits. So, if we do want to use a 64-bit field as our primary field, we need to do FRI in a quadratic extension of that field. This is totally doable, and in fact this is how [ethSTARK](https://github.com/starkware-libs/ethSTARK) works, but it does add some complications.

So, for the work I’ve been doing, I’ve been using primarily 128-bit fields. But happy to chat - I’ll PM you my email.

---

**vbuterin** (2020-07-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/bobbinth/48/2389_2.png) bobbinth:

> Specifically, FRI needs to be done in a field which is over ~120 bits

What is the reason for this? Is this just the fact that the soundness error from sampling is \frac{deg(p)}{|F|}? That could be fixed by just doing multiple challenges.

---

**bobbinth** (2020-07-20):

Yes - I believe that’s the reason. My understanding is that increasing number of challenges leads to larger proofs, and so this approach becomes less attractive as compared to using an extension field for FRI. Though, I haven’t done the math to confirm this myself.

