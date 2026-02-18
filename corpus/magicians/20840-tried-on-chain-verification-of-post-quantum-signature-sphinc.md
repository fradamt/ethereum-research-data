---
source: magicians
topic_id: 20840
title: Tried on-chain verification of post-quantum signature(SPHINCS+)
author: srarcharles
date: "2024-08-20"
category: Magicians > Primordial Soup
tags: [signatures, postquantum, sphincs]
url: https://ethereum-magicians.org/t/tried-on-chain-verification-of-post-quantum-signature-sphincs/20840
views: 191
likes: 0
posts_count: 1
---

# Tried on-chain verification of post-quantum signature(SPHINCS+)

# Background

- using PQC in the Blockchain mitigates risk of Quantum Computers’ attacks.
- signature verification should be happened on on-chain code(solidity)
- Clarify its possibility is a problem of realizability.

# What I did

- used SPHINCS+ as a post-quantum signature scheme

This is selected because NIST selected SPHINCS+ as a final candidate of PQC scheme

FIPS 205, Stateless Hash-Based Digital Signature Standard | CSRC

# Result

- I couldn’t realize verification on-chain, because it needs massive gas costs over block gas limit. (30,000,000gas)
- So, it is impossible to use SPHINCS+ as a verification method.

# Working Code

- Abount SPHINCS+

https://sphincs.org/

[GitHub - kasperdi/SPHINCSPLUS-golang: Implementation of the SPHINCS+ signature framework.](https://github.com/kasperdi/SPHINCSPLUS-golang)
migrated from Golang code to solidity code

[GitHub - blocq-inc/sphincsplus-verify-sol: solidity code for verify sphincs+ signature](https://github.com/blocq-inc/sphincsplus-verify-sol)
