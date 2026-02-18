---
source: ethresearch
topic_id: 5962
title: Can anyone recommend cipher for Solidity encryption?
author: kladkogex
date: "2019-08-13"
category: Cryptography
tags: []
url: https://ethresear.ch/t/can-anyone-recommend-cipher-for-solidity-encryption/5962
views: 3008
likes: 0
posts_count: 4
---

# Can anyone recommend cipher for Solidity encryption?

At SKALE we need to implement a Hash(Keccack) based-cipher - the reason is we need  to be able to decrypt in Solidity smart contract as a part of a fraud claim.

t the moment we are using an ad-hock counter-based CIPHER that I cooked up - essentially XORING plaintext with consequitive hashes of COUNTER | KEY

Can anyone point to a spec on a simple HASH-based cipher that is cheap and easy to do in Solidity?

## Replies

**laurentyzhang** (2019-09-15):

Just implement one outside EVM and wrap it as a solidty smart contract, deploy it at a special address, intercept and redirect calls made to the smart contract to the hasher outside EVM.

It worked well for us and it is very simple, 2 weeks, 1 guy enough

---

**kladkogex** (2019-09-18):

Well …  We need to do it on main net

---

**solidblu1992** (2019-09-18):

Could you use something like [RC4](https://en.wikipedia.org/wiki/RC4)?  Not sure how much stuff your are decrypting, but using my [hacked together contract](https://goerli.etherscan.io/address/0xa16005f8f56eeb781d2d46f449db2e3d77a05ac2#code) with a 32 byte key, 32 bytes of ciphertext takes about 200,000 gas, while 1KB of text takes about 1 million.

Edit: Published new version of contract that *actually* passes the test vectors on Wikipedia.  Also, I realize that RC4 is rather old, but maybe it is still useful for your purposes.

