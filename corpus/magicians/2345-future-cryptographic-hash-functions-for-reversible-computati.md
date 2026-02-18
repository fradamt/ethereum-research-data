---
source: magicians
topic_id: 2345
title: Future cryptographic hash functions for reversible computation
author: jvanname
date: "2019-01-06"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/future-cryptographic-hash-functions-for-reversible-computation/2345
views: 511
likes: 0
posts_count: 1
---

# Future cryptographic hash functions for reversible computation

Today, the top limiting factor in the performance of our integrated circuits is the energy usage and the heat production of these integrated circuits. Furthermore, Landauer’s limit states that every bit of information deleted must cost at least k T ln(2) energy where k is Boltzmann’s constant (k=1.38 times 10^(-23) Joules/Kelvin) and T is the temperature. In practice, one will need to spend much more that k*T energy per bit deleted in order to obtain reliable conventional computation since thermal noise becomes a problem well before k T ln(2). This means that the only possible way to make computation energy efficient in the long run is to make computers that delete as little information as possible. These computers that perform calculations without deleting much information are known as reversible computers.

As you might guess, it generally takes more operations and space to perform a computation reversibly than to perform the corresponding computation using a conventional computer. Fortunately, the space and time overhead incurred from reversible computation is surprisingly slow growing [(See Theorem 2.12 in this paper)](https://arxiv.org/pdf/math/9508218.pdf), and this space and time overhead can be further managed by using partially reversible computation instead of fully reversible computation. In the future, reversible computers will become efficient enough to perform any calculation more cost effectively than conventional computers would.

Certain types algorithms such as symmetric encryption and decryption functions are nearly perfectly suited for reversible computation; a symmetric encryption function designed to be used by a reversible computer would run nearly as well on a conventional computer as a symmetric encryption function designed to be used by a conventional computer. The notion of a cryptographic hash function is also quite suited for reversible computation since the security properties of cryptographic hash functions such as collision resistance and second pre-image resistance are themselves weak versions of reversibility.

Oddly enough, I have not seen much of any research on any cryptographic functions designed for reversible computers. Since algorithms such as AES and SHA-256, SHA-3, etc are not designed with reversible computation in mind, we will need to develop, evaluate, standardize, and finally implement new reversible cryptographic hash functions and other functions.

Might Ethereum be interested in the development of reversible symmetric cryptographic algorithms and similar algorithms like reversible hash-based signatures in order to maximize its efficiency?

I personally would be able (if funded) to develop functions f with f^n is the identity function that may be used in the key schedules for reversible encryption functions and in a similar role in reversible cryptographic hash functions (It looks like reversible linear cellular automata of characteristic 2 over the torus could serve this purpose https://mathoverflow.net/a/320240/22277). I will also be able to design hash-based signature algorithms for reversibility along with optimizing Merkle trees for reversibility.

-Joseph Van Name Ph.D.
