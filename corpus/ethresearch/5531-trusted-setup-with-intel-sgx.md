---
source: ethresearch
topic_id: 5531
title: Trusted setup with Intel SGX?
author: wanghs09
date: "2019-05-30"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/trusted-setup-with-intel-sgx/5531
views: 3330
likes: 0
posts_count: 6
---

# Trusted setup with Intel SGX?

There are a lot of work done for improving proof generation.  However, for use cases besides anonymous transactions(which we can use zcash sprout/sapling parameters), there seems no solution for trusted setup. Users have to perform their own trusted setup and let others to trust them, which is very inconvenient.

So here I propose to use Intel SGX to alleviate the problem, even though that it cannot completely solve the problem.

Steps:

1, Users use python/js/c/rust to describe their trusted setup procedure for specific use case, which includes procedures to remove all toxic waste. The program is open to everyone and can be audited.

2, SGX hardware takes the logic, uses embedded random source as seeds to generate proving key and verifying key, then delete the toxic waste, with a quote generated.

Alternatively, one can use the SGX secrets when manufactured but unknown to Intel, to deterministicly derive all random numbers for trusted setup.

3, The quote is transmitted to Intel Attestation Service (IAS), which verifies the report and produces a final report with Intel’s certificate chain.

4, Everybody can verify the final report and be conviced that the verifying key is rightly generated and all toxic waste is deleted.

Problems & possible solutions:

1, Intel may deny legal quotes. It can be made indistinguishable to Intel whether or not it’s a trusted setup program.

2, Intel may collude with some SGX users to store toxic waste or use fake SGX. It can be avoided by  allowing free participation and randomly selecting SGX providers.

3, Intel may manipulate randomness in SGX with some trapdoor. It can be alleviated with tricks in 2.

References:

1, Costan V, Devadas S. Intel SGX Explained[J]. IACR Cryptology ePrint Archive, 2016, 2016(086): 1-118.

## Replies

**adlerjohn** (2019-05-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/wanghs09/48/1398_2.png) wanghs09:

> there seems no solution

What about:

1. Sonic: Zero-Knowledge SNARKs from Linear-Size Universal and Updateable Structured Reference Strings
2. Spartan: Efficient and general-purpose zkSNARKs without trusted setup
3. Scalable, transparent, and post-quantum secure computational integrity

---

**wanghs09** (2019-05-30):

Yes, thanks for mentioning these work. these are very recent work which claim good property and no setup.

Here I only targeted groth16 work, which shows provable security and good performance over the last few years.

---

**Econymous** (2019-05-31):

Will encryption (FHE), zero knowledge proofs, and/or multi-party computing combined with a multi-chain scaling solution help a privacy protocol?

---

**wanghs09** (2019-05-31):

no idea what you are talking about and its relation with zkp

---

**weijiguo** (2022-10-18):

It seems pretty interesting for groth 16 uses. I guess we might need a neutral 3rd party to run the SGX instances. There is still an issue about how users or anybody can trust the enclave measurements.

I just stumble into similar situation, for which I have create another topic here: [Combining SGX and web3 for better security/privacy](https://ethresear.ch/t/combining-sgx-and-web3-for-better-security-privacy/13961)

