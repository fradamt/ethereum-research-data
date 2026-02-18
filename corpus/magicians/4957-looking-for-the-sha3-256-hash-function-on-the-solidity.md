---
source: magicians
topic_id: 4957
title: Looking for the SHA3-256 hash function on the solidity
author: unamed12
date: "2020-11-23"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/looking-for-the-sha3-256-hash-function-on-the-solidity/4957
views: 1763
likes: 6
posts_count: 8
---

# Looking for the SHA3-256 hash function on the solidity

Hi community, I’ve been trying to find the answer to the below question on the ethereum forums, but haven’t found so I write this post.

Currently, I am looking for the SHA3-256 (SHA3 FIPS 202, https://en.wikipedia.org/wiki/SHA-3) hash function on the solidity to develop a new smart contract using this hash function. But, I haven’t found any related information regarding SHA3-256 on the solidity.

1.) SHA3-256 hash function exists on the solidity?

2.) If not, is there any plan to implement the SHA3-256 hash function on the solidity as a method?

3.) If not, anything I can do to use the SHA3-256 has function on the solidity?

It would be really helpful if you know the answer to the above questions. Thank you for reading this question.

## Replies

**matt** (2020-11-23):

1. SHA3-256 is not currently supported in Ethereum. Only Keccak256 is.
2. There is desire to support SHA3-256 in the future, either as a precompile or written natively in EVM384-like framework.
3. I’m not aware of one. I know Near has implemented SHA-512, but I’m not sure if it is FIPS 202 or Keccak family.

---

**benny_options** (2020-11-24):

Hi [@matt](/u/matt) thanks for the quick answer!

We are building a cross-chain bridge and a SHA3-256 hashing function is a necessary component of our bridge. Do you know the Ethereum update schedule?

As for next steps, do you have a recommended next step we can take to get this function added? Any advice you may have would be super helpful, as our bridge technology (as it’s currently designed) depends on having this function.

---

**matt** (2020-11-24):

The Berlin hard fork is scheduled for Q1 2020. It probably won’t be until after that when new EIPs are discussed.

---

**unamed12** (2020-11-24):

Is there any website that I can see the next upcoming update? Thank you for your answer!

---

**matt** (2020-11-24):

Network upgrades are roughly tracked here: https://github.com/ethereum/eth1.0-specs/projects/1

---

**k06a** (2020-11-28):

Efficient SHA3-512 Solidity implementation could be found here: https://gist.github.com/abacabadabacaba/9c395588c455ca1f7dccfa853d8fd56d

---

**unamed12** (2020-11-29):

Thank you guys! I’ll look into it

