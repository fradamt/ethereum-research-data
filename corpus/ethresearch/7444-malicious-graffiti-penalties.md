---
source: ethresearch
topic_id: 7444
title: Malicious Graffiti penalties
author: alonmuroch
date: "2020-05-19"
category: Proof-of-Stake > Block proposer
tags: []
url: https://ethresear.ch/t/malicious-graffiti-penalties/7444
views: 2356
likes: 4
posts_count: 3
---

# Malicious Graffiti penalties

Potentially the graffiti (and other data bits from slots) might end up available in the EVM for various purposes, it might be interesting exploring ways to penalise block proposers that include malicious code as graffiti.

We could argue that it’s every devs’ job to escape and validate anything before usage, but it might also be good to enforce it on the protocol level.

The idea being, attesters will not vote for a block proposed with a graffiti the fails validation (validation parameters could be added and improved via EIP)

[![Screen Shot 2020-05-19 at 10.53.23](https://ethresear.ch/uploads/default/optimized/2X/c/c0d97de696f528daec24d780635a8bc8440059cb_2_690x63.png)Screen Shot 2020-05-19 at 10.53.231303×120 9.85 KB](https://ethresear.ch/uploads/default/c0d97de696f528daec24d780635a8bc8440059cb)

https://beacon.etherscan.io/slot/225533

## Replies

**dankrad** (2020-05-19):

Since currently, Graffiti is not intended to be interpreted as code, there is by definition no such thing as malicious code. If you are suggesting that we implement a mechanism to stop people from adding code that could attack *external* users of the blockchain, then you would actually need something more like a virus scanner to do heuristic on what could be malicious (as there are tons of possible languages and databases that this could affect), and it would be insane to enforce something like that as part of consensus (the attack surface that is introduced would be much larger than the existing one).

---

**alonmuroch** (2020-05-19):

There are discussions of making graffiti more useful and potentially usable not just as a random string…

Question is, if that happens does the protocol have responsibility to enforce some security measure around it.

I agree that if it never makes it to the evm or no substantial use is made from it than no penalties should apply

