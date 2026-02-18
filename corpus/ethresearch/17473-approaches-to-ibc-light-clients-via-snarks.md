---
source: ethresearch
topic_id: 17473
title: Approaches to IBC light clients via SNARKs
author: ZORK780
date: "2023-11-20"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/approaches-to-ibc-light-clients-via-snarks/17473
views: 1657
likes: 13
posts_count: 5
---

# Approaches to IBC light clients via SNARKs

Hey everyone,

We at Panther published our SNARK paper earlier this year (https://eprint.iacr.org/2023/1255.pdf), as well as a follow-up paper (https://eprint.iacr.org/2023/1264.pdf). This scheme circumvents the overhead of non-native field arithmetic arising from Ed25519 signatures.

Right now we survey some approaches to IBC light clients via Snarks. The implementation uses a 570-bit outer curve to Ed25519 constructed via the Cocks-Pinch algorithm.

The prover time for a million gate circuit on a 64 vCPU AWS machine’s 32 seconds for the version optimized for the proof size and verification time, and 20 seconds for the version optimized for the Prover time.

I am wondering if 100 blocks within ~ 90 seconds / 1 minute is efficient enough for the Snark to be useful within the given context outlined above, and if someone here has a use for this work.

We are currently working on a piece describing an IBC scheme related to our earlier work.

## Replies

**hoanngothanh** (2023-12-06):

In your experience, what are the key advantages and potential drawbacks of using the Cocks-Pinch algorithm for constructing the outer curve in the implementation?

---

**xyzq-dev** (2023-12-08):

In your SNARK paper, you’ve effectively reduced the overhead of non-native field arithmetic for Ed25519 signatures and optimized the prover time. Considering the specific use of a 570-bit outer curve and the prover times you’ve achieved, could you elaborate on how these optimizations impact the scalability and practical deployment of IBC light clients using SNARKs, especially in high-throughput blockchain environments?

---

**ZORK780** (2023-12-14):

We at Panther did look into other algorithms like Brezing-Weng for example however the curve won’t get much smaller with the more subtle techniques.

We intend to look into more subtle constructions in the future.

---

**H1GPBDC** (2023-12-15):

Great initiative and paper. Do you think your algorithm can handle such a large amount of blocks in a small amount of time (ie 100 blocks in 90 seconds/ 1 minute). I would suggest having a slightly larger block time and keep tapering it down based on the performance metrics and see how it affects the client being operational and without it falling into breaks. Another suggestion would be to run multiple iterations of client with different presets and parameters and gauge the performance and make incremental upgrades.

