---
source: ethresearch
topic_id: 8867
title: Indifferentiable hashing to ordinary elliptic Fq-curves of j=0 with the cost of one exponentiation in Fq
author: dishport
date: "2021-03-09"
category: Cryptography
tags: [signature-aggregation]
url: https://ethresear.ch/t/indifferentiable-hashing-to-ordinary-elliptic-fq-curves-of-j-0-with-the-cost-of-one-exponentiation-in-fq/8867
views: 3133
likes: 6
posts_count: 7
---

# Indifferentiable hashing to ordinary elliptic Fq-curves of j=0 with the cost of one exponentiation in Fq

Hi guys,

I am very sorry for spamming. However I wrote [a new article](https://eprint.iacr.org/2021/301), which is a remarkable improvement of [my previous topic](https://ethresear.ch/t/hashing-to-elliptic-curves-y-2-x-3-b-provided-that-b-is-a-quadratic-residue/7939). In my opinion, this is the most useful result for blockchain I have ever obtained. Please read the abstract:

> Let \mathbb{F}_{\!q} be a finite field and E_b\!: y^2 = x^3 + b be an ordinary (i.e., non-supersingular) elliptic curve (of j-invariant 0) such that \sqrt{b} \in \mathbb{F}_{\!q} and q \not\equiv 1 \: (\mathrm{mod} \ 27). For example, these conditions are fulfilled for the group \mathbb{G}_1 of the curves BLS12-381 (b=4) and BLS12-377 (b=1) and for the group \mathbb{G}_2 of the curve BW6-761 (b=4). The curves mentioned are a de facto standard in the real world pairing-based cryptography at the moment. This article provides a new constant-time hash function H\!: \{0,1\}^* \to E_b(\mathbb{F}_{\!q}) indifferentiable from a random oracle. Its main advantage is the fact that H computes only one exponentiation in \mathbb{F}_{\!q}. In comparison, the previous fastest constant-time indifferentiable hash functions to E_b(\mathbb{F}_{\!q}) compute two exponentiations in \mathbb{F}_{\!q}. In particular, applying H to the widely used BLS multi-signature with m different messages, the verifier should perform only m exponentiations rather than 2m ones during the hashing phase.

For your taste, is this an important achievement ? Please let me know about a collaboration if one of companies or startups wants to use my hash function in its products. In the near future, I will also try to generalize this hash function to the more difficult case \sqrt{b} \not\in \mathbb{F}_{\!q} in order to be applicable to all pairing-friendly curves.

Best regards.

## Replies

**illuzen** (2021-10-12):

Looks like your paper was incorrectly published? When I download the PDF it only shows the first page.

In general, adoption of a new hash function is slow, since it is a central component to many cryptographic systems.

Your result is impressive, but still linear in m. Is it possible to make it logarithmic by assembling the messages into a tree?

Seems like you’re coming from pure math into computer science. Welcome, your contributions are appreciated.

---

**dishport** (2021-10-12):

> Looks like your paper was incorrectly published? When I download the PDF it only shows the first page.

When I download, the PDF shows all the paper. Do you open the link on eprint iacr ?

> In general, adoption of a new hash function is slow, since it is a central component to many cryptographic systems.

If the new hash function is slow, then previous ones are a fortiori.

> Is it possible to make it logarithmic by assembling the messages into a tree?

I don’t know how this is possible, because all the messages are arbitrary and independent of each other.

> Seems like you’re coming from pure math into computer science. Welcome, your contributions are appreciated.

Thanks.

---

**illuzen** (2021-10-14):

I was referring to the social layer, that the humans implementing cryptosystems aren’t quick to adopt a new hash  function, even if it’s faster, like yours.

---

**illuzen** (2021-10-14):

I read your paper. If you are serious about getting this accepted by a wider community, you will need an implementation in some common programming language, C, Python, Rust, JS. This resource might be helpful: [Hashing to Elliptic Curves](https://www.ietf.org/archive/id/draft-irtf-cfrg-hash-to-curve-10.html)

I’m not an expert in your field, but it seems like there should be a term for the relationship between the encodings e and h. It’s like you generalized e to a larger domain, so e = h on the diagonal. Could be good for you to coin the term if it doesn’t exist…

Also, a natural question is “is the epsilon small enough to be usable for critical security infrastructure?” You might supply some comparisons with existing solutions to make it easy to reason about.

Anyways thanks for sharing.

---

**dishport** (2021-10-14):

> Also, a natural question is “is the epsilon small enough to be usable for critical security infrastructure?” You might supply some comparisons with existing solutions to make it easy to reason about.

Yes, epsilon is negligible for q of a cryptographic size. I give an estimation in the end of my paper.

---

**dishport** (2022-02-02):

[SpringerLink](https://link.springer.com/article/10.1007/s10623-022-01012-8)



    ![](https://ethresear.ch/uploads/default/optimized/3X/7/a/7a166a4f981528feafd6aca4f308ec69db60f1cd_2_329x500.jpeg)

###



Let $${\mathbb {F}}_{\!q}$$ F q be a finite field and $$E_b\!: y^2 = x^3 + b$$ E b : y 2 = x 3 + b be an ordinary (i.e., non-supersingular) elliptic curve (of j-invariant 0) such that $$\sqrt{b} \in {\mathbb {F}}_{\!q}$$ b ∈ F q and $$q \not \equiv 1...










Hi. My article about hashing to the subgroup \mathbb{G}_1 is published since yesterday in Designs, Codes and Cryptography.

