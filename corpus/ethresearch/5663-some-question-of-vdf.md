---
source: ethresearch
topic_id: 5663
title: Some question of vdf
author: yyyyyp
date: "2019-06-28"
category: Miscellaneous
tags: [verifiable-delay-functions]
url: https://ethresear.ch/t/some-question-of-vdf/5663
views: 1999
likes: 1
posts_count: 7
---

# Some question of vdf

I want to know how you satisfy the low order assumption of vdf，to be specific ，how can you generate two large prime numbers in the distributed environment？  Can anyone answer this question

## Replies

**yyyyyp** (2019-06-28):

anyone can answer this question？

---

**yyyyyp** (2019-06-28):

Is it going to be generated in a centralized way

---

**seresistvan** (2019-06-28):

Well, there are several papers on how to generate RSA-moduli in a distributed fashion.

[Boneh-Franklin](https://link.springer.com/content/pdf/10.1007/BFb0052253.pdf): Efficient Generation of Shared RSA Keys

[Damgard-Mikkelsen](https://www.iacr.org/archive/tcc2010/59780180/59780180.pdf):Efficient, Robust and Constant-Round

Distributed RSA Key Generation

[Federiksen-Osheter-Lindell-Pinkas](https://eprint.iacr.org/2018/577): Fast Distributed RSA Key Generation for Semi-Honest and Malicious Adversaries

And there are many more…

The main research line here is how to make the original Boneh-Franklin paper more robust, i.e. that it is safe against even large number of active adversaries.

However it is an open question, how we could generate RSA-moduli of special form in a distributed way. This would be beneficial in a VDF-setting, since for example the multiplicative group of an RSA-modulus which is the product of safe primes does not contain low order elements ***at all***. That is how Pietrzak proved the soundness of his VDF construction [in his paper](https://eprint.iacr.org/2018/627.pdf). Later Boneh, Bünz, Fisch realised that you do not need the modulus to be the product of two safe primes, rather you “only” need the low-order assumption. See paper [here](https://crypto.stanford.edu/~dabo/pubs/papers/VDFsurvey.pdf).

---

**yyyyyp** (2019-07-01):

Thanks for you reply. By the way，What is your preference for distributed production of large prime Numbers,as you provided many papers above. Do you think it’s a big safe problem to generate large prime numbers, Or do you think that’s not a problem.Thank you

---

**seresistvan** (2019-07-01):

Well, in all of the papers I referenced above, you do not generate ***prime numbers*** in a distributed fashion, but ***RSA-moduli***. The point is that noone should know the factors of the generated moduli, i.e. N is searched in the following form:

N=(p_1+p_2+\dots p_k)(q_1+q_2+\dots q_k),

where party i only knows p_i, q_i and obviously N and whether N is a product of two primes (so called biprime) or not, ***but*** no other information is revealed!!!

So all the above mentioned MPC protocols output biprimes (RSA-moduli) and not primes.

If you want to generate secret primes in a distributed fashion, then you might want to have a look at [this paper](https://www.brics.dk/RS/98/29/BRICS-RS-98-29.pdf). It allows one to execute the Miller-Rabin primality test in a distributed way.

---

**yyyyyp** (2019-07-02):

Thank you very much. I misunderstood before.I have another question that you mean N is a product of two primes (so called biprime) or not.If N is not a product of two primes ,is it safe? And as I know,

The MPC is being designed by Ligero, Is your development based on their unpublished papers on

RSA Modulus Generation. When can I see some progress in development?

