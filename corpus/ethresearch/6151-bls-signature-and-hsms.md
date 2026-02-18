---
source: ethresearch
topic_id: 6151
title: BLS Signature and HSMs
author: hermanjunge
date: "2019-09-16"
category: Cryptography
tags: []
url: https://ethresear.ch/t/bls-signature-and-hsms/6151
views: 3714
likes: 2
posts_count: 6
---

# BLS Signature and HSMs

Dear All,

My team has been working on designing a set of tools to deploy and monitor validator clients in any cloud.

A key element in this kind of deployment is the HSM component. To date (2019.09.16), there are not known support for the BLS12-381 curve and the BLS signature. Then a great task is start evangelizing cloud and hardware providers on this requirement.

Anybody in this forum is familiar with the steps it takes for both the curve and the signature scheme to be NIST / FIPS compliant? (any of them, either or both). Any pointer to cover this subject will be extemely appreciated.

**Herman**

PS: I plan to use that article’s url and this thread as the main redirection links for the subject of HSM support.

## Replies

**hermanjunge** (2019-09-17):

This is a quick “BLS for busy people” guide. With a summary, some discussion and the links I’ve visited the most during my little information gathering.


      [gist.github.com](https://gist.github.com/hermanjunge/3308fbd3627033fc8d8ca0dd50809844)




####

##### BLS_Signature.md

```
# BLS Signature for Busy People

## Summary

* BLS stands for
  * Barreto-Lynn-Scott: BLS12, a Pairing Friendly Elliptic Curve.
  * Boneh-Lynn-Shacham: A Signature Scheme.

* **Signature Aggregation**
  * It is possible to verify `n` aggregate signatures on the same message with just `2` pairings instead of `n+1`.
```

This file has been truncated. [show original](https://gist.github.com/hermanjunge/3308fbd3627033fc8d8ca0dd50809844)

---

**kladkogex** (2019-09-18):

BLS signatures can not be FIPS validated since BLS has not been validated as FIPS compliant by the US government.

At SKALE we are developing SGX based crypto wallet, which can be used to protect BLS. We are planning to opensource it soon.

---

**hermanjunge** (2019-09-18):

Stan, thank you for your answer.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> At SKALE we are developing SGX based crypto wallet

I have to gain further understanding on the topic of SGX. For now, It is correct to assume that I can build a secure enclave in a cloud (e.g. AWS), leveraging SGX?

---

**kladkogex** (2019-09-19):

You can use Microsoft Azure, AWS does not support it yet

It is basically a programmable HSM inside of Intel CPU

---

**deejvince** (2020-04-24):

SGX has many downsides and security issues exposed recently. AWS has developed their own Enclave technology called: Nitro Enclave

