---
source: ethresearch
topic_id: 5632
title: Clients with pluggable proof-of-work (consensus) algorithms
author: miohtama
date: "2019-06-19"
category: Architecture
tags: []
url: https://ethresear.ch/t/clients-with-pluggable-proof-of-work-consensus-algorithms/5632
views: 1724
likes: 0
posts_count: 4
---

# Clients with pluggable proof-of-work (consensus) algorithms

Hi,

I have a friend who is working in high-performance computing space. They have some workloads that they claim could be an ideal source for useful proof-of-work. Putting the discussion aside if the computations are suitable or not, she would like to test out plugging it in to a running blockchain.

Do any of Ethereum clients currently support pluggable proof-of-work algorithms e.g. assuming Bysantine Fault Tolerance consensus? What could be a starting point for such a research?

## Replies

**adlerjohn** (2019-06-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/miohtama/48/885_2.png) miohtama:

> useful proof-of-work

The work used in Proof-of-Work needs to be useless. If it’s useful, 1) who decides how it’s useful? and 2) it can be re-used (because it’s useful).

That said, it looks like [Py-EVM can be modified pretty easily to use a different PoW algorithm](https://github.com/ethereum/py-evm/blob/f205ed099c5534892c3afbbd1b14a2fa7f597673/eth/consensus/pow.py).

---

**miohtama** (2019-06-19):

Thanks! I think this is a good place to start hacking.

---

**q** (2020-03-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> who decides how it’s useful?

Not a complete answer, but Primecoin tried to provide useful p-o-w by letting miners search for primes of a certain size which is mathematically provable useful (here: number of digits).

I’m not sure what happened to the project though.

