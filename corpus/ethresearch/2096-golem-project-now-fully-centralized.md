---
source: ethresearch
topic_id: 2096
title: Golem project - now fully centralized?
author: kladkogex
date: "2018-05-30"
category: Cryptography > Multiparty Computation
tags: []
url: https://ethresear.ch/t/golem-project-now-fully-centralized/2096
views: 2249
likes: 1
posts_count: 3
---

# Golem project - now fully centralized?

Golem is  apparently releasing a beta on Ethereum main net

The source code of Golem smart contracts is here

[source code](https://github.com/golemfactory/golem-contracts/blob/master/contracts/GNTDeposit.sol)

What is interesting is that every smart contract includes …  [a centralized approving party!](https://www.youtube.com/watch?v=L_VQEP_ceIM)

A bit ironic, having that the first line of the Golem whitepaper reads

“Golem is the first truly decentralized supercomputer, creating a global market for

computing power”

![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=9)![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=9)![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=9)

## Replies

**ardakesim** (2018-10-23):

contract cant check computation, but project could allow selecting confirmatory

---

**musalbas** (2018-10-23):

We released [a paper](https://arxiv.org/abs/1805.06411) a few months ago describing how to do fair exchange payment for outsourced TEE computations. If they use that they wouldn’t need a centralised party to guarantee fairness. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Airtnt: Fair Exchange Payment for Outsourced Secure Enclave Computations


      ![image](https://static.arxiv.org/static/browse/0.2.7/images/icons/favicon.ico)
      [arXiv.org](https://arxiv.org/abs/1805.06411)


    ![image]()

###

We present Airtnt, a novel scheme that enables users with CPUs that support
Trusted Execution Environments (TEEs) and remote attestation to rent out
computing time on secure enclaves to untrusted users. Airtnt makes use of the
attestation...

