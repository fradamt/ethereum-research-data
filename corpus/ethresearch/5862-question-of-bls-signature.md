---
source: ethresearch
topic_id: 5862
title: Question of bls signature
author: yyyyyp
date: "2019-07-23"
category: Miscellaneous
tags: [signature-aggregation]
url: https://ethresear.ch/t/question-of-bls-signature/5862
views: 2617
likes: 0
posts_count: 11
---

# Question of bls signature

Can you tell me the progress of BLS signature.Such as the specifics of the BLS’s integration with consensus, the efficiency of the validation of signature aggregation.

As far as I know, using the BLS signature also requires additional public key transfers，will this influence the efficiency？

## Replies

**yyyyyp** (2019-07-25):

can anyone answer it？

---

**yyyyyp** (2019-08-06):

bls is a big problem

---

**kladkogex** (2019-08-13):

At SKALE we are developing a BLS library for general use.

It also includes threshold encryption.  It is in process of getting improved and documented.

Your are welcome to use it. It is licensed under  AGPL 3.0



      [github.com](https://github.com/skalenetwork/libBLS)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/f/7/f749de1f54c26e4bcbc370a71c0f1c5eb61dfd5f_2_690x344.png)



###



If you like this project, please ⭐⭐⭐ it on GitHub!! Solidity-compatible BLS signatures, threshold encryption, distributed key generation library in modern C++. Actively maintained and used by SKALE for consensus, distributed random number gen, inter-chain communication and protection of transactions. BLS threshold signatures can be verified in

---

**yyyyyp** (2019-08-14):

thanks for your reply,Can you provide some benchmark data，and do your library support the go language

---

**kladkogex** (2019-08-14):

It does around a 1000 signings per sec on my PC.

We will be adding a command line for it soon. Then you will be able to call this from go easily.

---

**yyyyyp** (2019-08-15):

1000signings means 1000 individual signatures or aggregate signatures ？

---

**kladkogex** (2019-08-15):

1000 individual signings for a BLS share.  Actually a signing involves a single exponentiation in a field, so it is not so expensive …

---

**yyyyyp** (2019-08-16):

Validation time may be more important than signature time because it involves pairing. How long does it take you to verify the signature? One more thing, I find that you are using a bn128 curve, but as far as I know it can only achieve 110bit security. What do you think about this? Have you considered bls12-381

---

**kladkogex** (2019-08-16):

yyyyp - I am going to ETH Berlin but I will have Sveta Rogova who is our BLS tsar get measure this and get back to you

---

**p_m** (2019-08-29):

Check out our pure JS implementation: https://github.com/paulmillr/noble-bls12-381

Works in node and browsers.

