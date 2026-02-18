---
source: ethresearch
topic_id: 7902
title: SGX security for ETH2 keys
author: kladkogex
date: "2020-08-26"
category: Security
tags: []
url: https://ethresear.ch/t/sgx-security-for-eth2-keys/7902
views: 1352
likes: 1
posts_count: 2
---

# SGX security for ETH2 keys

Want to secure your #ETH2 validator keys so hackers do not steal them while they are stored in plaintext on your AWS machine?

SKALE has opensource sgxwallet hardware security module that can be EASILY improved to be used by ETH2 (1-2 weeks of work).



      [github.com](https://github.com/skalenetwork/sgxwallet)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/1/b/1b27c7264024b974bef7ace39e6a613f61cb75ce_2_690x344.png)



###



sgxwallet is the first-ever opensource high-performance hardware secure crypto wallet that is based on Intel SGX technology.  First opensource product on Intel SGX whitelist. Scales to 100,000+ transactions per second. Currently supports ETH and SKALE, and will support BTC in the future.  Sgxwallet is under heavy development and use by SKALE network.










We are looking for opensource developers interested to contribute to sgxwallet so it can be used for ETH2.

## Replies

**kobigurk** (2020-08-27):

Nice work!

Are the operations in libBLS constant-time? As far as I know, SGX doesn’t provide built-in protection against side-channels attacks.

