---
source: ethresearch
topic_id: 7161
title: Performance of Rescue and Poseidon hash functions
author: bobbinth
date: "2020-03-20"
category: zk-s[nt]arks
tags: [library]
url: https://ethresear.ch/t/performance-of-rescue-and-poseidon-hash-functions/7161
views: 7950
likes: 16
posts_count: 8
---

# Performance of Rescue and Poseidon hash functions

I wanted to get some sense of how fast the new hash functions (Rescue and Poseidon) are - so, I put together a fairly performant implementation of both in Rust ([here](https://github.com/GuildOfWeavers/distaff)). As far as I know, this is the fastest implementation of these hash functions - but if anyone knows any faster implementations, let me know.

### results

These results are from for Intel Core i5-7300U @ 2.60GHz (single thread):

- Rescue: ~12,000 hashes/second or ~80,000 ns / hash
- Poseidon: ~33,000 hashes/second or ~30,000 ns / hash

For comparison, on the same machine, I can do over 1M sha256 hashes/sec. So, Poseidon is almost 3x faster than Rescue, and both are significantly slower than sha256 (this was expected). Specifically, Poseidon is about 30x slower, and Rescue is about 80x slower than sha256.

### parameters

The parameters I used for hash functions are similar to the ones listed for S128d variant in StarkWare’s [hash challenge](https://starkware.co/hash-challenge-implementation-reference-code/). Specifically:

- Rescue: 10 rounds with state width of 12 64-bit field elements
- Poseidon: 48 rounds (8 full / 40 partial) with sate width of 12 64-bit field elements

The main difference between the parameters I used and the ones listed on the hash challenge site is the field. I’m using a 64-bit prime field, while StarkWare challenge uses a 62-bit prime field (64-bit field made things a bit faster for me).

The use of a 64-bit field probably means that this implementation cannot be used inside pairing-based SNARKs, but it should still be usable in STARKs.

### performance analysis

Performance of these functions can be improved further. Here is what’s taking the most time in each hash function:

- Rescue: 85% of the time is spent doing the inverse S-Box, and 14% of the time is spend on applying MDS matrix.
- Poseidon: 92% of the time in spent on applying MDS matrix, and 5% of time is spent in doing the S-Box.

In my implementation, exponentiation is not particularly optimized - so, optimizing it should improve performance of Rescue. For Poseidon, the improvements could come from reducing the number of rounds. This could potentially be done by increasing S-Box degree from 3 to 5 - though, I’m not sure how many rounds this would allow to shave off.

## Edit:

Additional results:

- GMiMC_erf: ~380,000 hashes/second or ~2,600 ns / hash

This makes GMiMC hash function by far the fastest one out of the 3. It is almost 12x faster than Poseidon, and only about 2.5x slower than sha256.

## Replies

**vbuterin** (2020-03-20):

Thanks for the stats! How do these compare to MiMC?

---

**bobbinth** (2020-03-21):

I don’t have this comparison - but it should be pretty easy to implement GMiMC for comparable parameters. I’ll add it to my benchmarks and will update the post with results a bit later.

---

**bobbinth** (2020-03-21):

Updated with GMiMC results - this seems to be the fastest one by far.

---

**vbuterin** (2020-03-21):

Right, that makes sense, as MiMC doesn’t involve inverses, which are cheap inside a SNARK but expensive to compute in a regular context. I do expect that this will cause MiMC to be more popular than the others, because in contexts where prover time matters, evaluating the hashes outside the prover is also going to take a significant amount of time so there will be pressure to optimize it.

---

**dignifiedquire** (2020-03-24):

Might be of interest, we have an implementation of Poseidon, quite heavily optimized but with different parameters, on the Bls12 381 curve here: https://github.com/filecoin-project/neptune.

It is currently being audited, so almost ready to use.

---

**liochon** (2020-05-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/bobbinth/48/2389_2.png) bobbinth:

> This makes GMiMC hash function by far the fastest one out of the 3. It is almost 12x faster than Poseidon, and only about 2.5x slower than sha256.

It’s a great bench. FWIW, I got slightly better performances on sha3: 5 times faster then gmimc (I sent you a pull request to get sha3 integrated in the benchmark). Blake3 is interesting as well…

```
Thousands of hashes per second:
rescue          16
poseidon        44
gmimc-erf      555
sha3          2747
blake3       20576
```

---

**bobbinth** (2022-07-15):

We’ve made significant progress in making both Rescue and Poseidon much faster over the last couple of years. The numbers I’m currently getting on an M1 Pro (single core) are like this:

- Rescue Prime which we use in Polygon Miden: ~195K hashes per second (pure Rust code).
- Poseidon implemented by Polygon Zero: ~770K hashes per second (and could be up to 2x faster when complied with vectorized instructions).

Both of these are over an order of magnitude faster than what I had originally shared in this thread. The improvements come from a variety of places, but to mention two most important ones:

- Using a fast small field (specifically, we use a field with p = 2^{64} - 2^{32} + 1).
- Selecting an MDS matrix of special form which dramatically decreases the number of modular reductions needed for MDS matrix multiplication.

