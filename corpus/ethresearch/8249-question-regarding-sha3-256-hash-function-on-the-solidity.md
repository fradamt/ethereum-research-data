---
source: ethresearch
topic_id: 8249
title: Question regarding SHA3-256 hash function on the solidity
author: unamed12
date: "2020-11-23"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/question-regarding-sha3-256-hash-function-on-the-solidity/8249
views: 1408
likes: 1
posts_count: 3
---

# Question regarding SHA3-256 hash function on the solidity

Hi community, I’ve been trying to find the answer to the below question on the ethereum forums, but haven’t found so I write this post.

Currently, I am looking for the SHA3-256 (SHA3 FIPS 202, https://en.wikipedia.org/wiki/SHA-3) hash function on the solidity to develop a new smart contract using this hash function. But, I haven’t found any related information regarding SHA3-256 on the solidity.

1.) SHA3-256 hash function exists on the solidity?

2.) If not, is there any plan to implement the SHA3-256 hash function on the solidity as a method?

3.) If not, anything I can do to use the SHA3-256 has function on the solidity?

It would be really helpful if you know the answer to the above questions. Thank you for reading this question.

## Replies

**barryWhiteHat** (2020-11-23):

** Disclaimer i am not 100% sure here please someone correct me if i am wrong **

![](https://ethresear.ch/user_avatar/ethresear.ch/unamed12/48/5320_2.png) unamed12:

> 1.) SHA3-256 hash function exists on the solidity?

Iiuc sha3-256 was added to ethereum before the standard was finalized. Which means that the sha3 that you can call from solidity is actually a older version of the finalized sha3 which we call `keccak256`.

So tldr SHA3 FIPS 202 is not available.

![](https://ethresear.ch/user_avatar/ethresear.ch/unamed12/48/5320_2.png) unamed12:

> 2.) If not, is there any plan to implement the SHA3-256 hash function on the solidity as a method?

I am not aware of any plan and would be surprised if it did happen.

![](https://ethresear.ch/user_avatar/ethresear.ch/unamed12/48/5320_2.png) unamed12:

> 3.) If not, anything I can do to use the SHA3-256 has function on the solidity?

Why do you need to us this exact hash function why not sha2 256 ?

---

**unamed12** (2020-11-24):

Hey, thank you for answering my questions. Very appreciate! We are building a cross-chain bridge and a SHA3-256 hashing function is a necessary component of our bridge.

For now, I am trying to find a way to implement the Sha3-256 on the Ethereum. I think I can submit an EIP on the forum, but I am not really familar with this process so want to ask a few things.

1.) Do you know how long time will take to get an EIP approved? I do expect it will take very long time but want to know the average expectation about this.

2.) Do you know the next Ethereum’s update schedule? Can I find any place that can see the next upcoming update schedule? It would be helpful if I can expect when my EIP will be approved and implemented on the next release.

Thank you so much!

