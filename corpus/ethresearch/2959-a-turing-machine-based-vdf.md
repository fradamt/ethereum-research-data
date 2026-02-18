---
source: ethresearch
topic_id: 2959
title: A Turing-machine based VDF
author: krzhang
date: "2018-08-16"
category: Cryptography
tags: [verifiable-delay-functions]
url: https://ethresear.ch/t/a-turing-machine-based-vdf/2959
views: 2335
likes: 1
posts_count: 3
---

# A Turing-machine based VDF

Here’s a weird VDF that came up as an idea when I was discussing VDFs with Ofer Grossman:

1. Fix some reasonable Turing Machine implementation.
2. Run some reasonably complicated f(x) (in the language of the TM) for 2^n time steps on the Turing machine. (we can e.g. get x from a RANDAO?)
3. Hash the 2^n machine states with some H(x) and Merklelize. The output of your computation is the Merkle root.
4. You verify by giving a Merkle branch to any node.

A few comments:

1. You already have a Turing Machine in Ethereum, so you can just use the specs for that for this TM, which makes this both amusing (from a meta point of view) and good (from a reusability point of view).
2. This is very similar to TrueBit, which itself seems to kind of require some sort of TM. Might as well use the same implementation for engineering practices.

What are the tradeoffs of something like this in context of what Ethereum wants, compared to other solutions? Also, am I missing something obviously bad?

Good meeting many of you over the weekend!

## Replies

**krzhang** (2018-08-16):

Note that we have a classic problem that comes up with PCPs (as Ofer reminded me) which is that adversaries can change a single machine state in a way that’s hard to detect.

However, I think we’re armed with cryptoecon for that part, because we can e.g. make a challenge game.

Now this is just becoming more and more like TrueBit. Maybe in some sense they (TrueBit and TM-based VDF) are the same problem…

---

**dlubarov** (2018-08-17):

Hm, what would be the advantage of a TM over computing f(x) directly? A TM would let us make f dynamic, but it doesn’t seem like your scheme requires that.

For verification, you’d probably end up with an interactive protocol along the lines of what [@clesaege](/u/clesaege)  discussed [here](https://ethresear.ch/t/multiparty-interactive-verification/1221), right? See also [Bunz et al.](http://www.jbonneau.com/doc/BGB17-IEEESB-proof_of_delay_ethereum.pdf)

