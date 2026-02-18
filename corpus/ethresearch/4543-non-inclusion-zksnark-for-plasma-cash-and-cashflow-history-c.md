---
source: ethresearch
topic_id: 4543
title: Non-inclusion zkSNARK for Plasma Cash and Cashflow history compaction
author: shamatar
date: "2018-12-10"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/non-inclusion-zksnark-for-plasma-cash-and-cashflow-history-compaction/4543
views: 2395
likes: 6
posts_count: 4
---

# Non-inclusion zkSNARK for Plasma Cash and Cashflow history compaction

TL DR; We’ve made a demo snark for Plasma Cash and Cashflow history compaction, that reduces a proof size from `~700 bytes` per block to `~200 + 8*N` bytes for `N` blocks

## Details

The SNARK itself is located [here](https://github.com/matterinc/plasma_cash_history_snark). In it’s core it proves that a subtree in a block’s SMT is empty for each root hash in the public inputs. Peddersen hash is used as a tree hash, with leaf values being 256 bit strings.

### Inputs:

- Start of the continuous non-inclusion range
- Length of the continuous range. Currently there is no internal check that start of the interval is divisible by the length of the range, but it’s trivial to extend
- Set of N root hashes for the block’s SMTs for which non-inclusion is proved. Those are not compacted using the hash to reduce the number of inputs because a verification of such SNARK will be done off-chain only

### Workflow:

- Alice accumulated N non-inclusion proofs from operator and prepares a SNARK proof as mentioned above
- Upon the transfer Alice sends a proof along with a list of block number for which this proof is valid to Bob
- Bob queries the chain to obtain root hashes for these blocks and use them as public inputs in verification
- Bob accepts a non-inclusion proof for this range of block numbers if SNARK proof is valid

### Some numbers

- 4_270_718 constraints for 128 block of non-inclusion for 24 tree depth
- provable in ~30 seconds on my laptop with six core i9
- Proof size is 192 bytes (Groth16 for BN256) + N*8 bytes to encode block numbers to send to Bob (uint64 for block numbers) + 8 bytes for a start of the slice being proved + 8 bytes for a length of the slice

### Trade-offs

- Will require to use Peddersen hash for a tree, that is slower (~ 30 microseconds per round 2n -> n)
- Will require to use another zkSNARK to prove inclusion upon exits, that is more expensive, but can be batched. Batch size of 5 gives verification cost of 300k gas per proof

### Improvements

- May transpose a zkSNARK to prove not the fact of non-inclusion of some range for a set of blocks, but a non-inclusion of the set of slices in one or more blocks
- Can be trivially extended to sum-trees

## Replies

**PhABC** (2018-12-10):

Was the proof generation parallelized at all? 30s per 128 block is good, but after a full year with 1 block per 15 mins, we are looking at ~2h proof generation (assuming circuit size increases linearly).

![](https://ethresear.ch/user_avatar/ethresear.ch/shamatar/48/670_2.png) shamatar:

> Will require to use Peddersen hash for a tree, that is slower

Slower with respect to what? I thought the whole point of using Pedersen commitment was to reduce circuit size, hence decrease proving time.

---

**shamatar** (2018-12-11):

Proof generation is done with multiple threads, that’s why I’ve listed a number of cores. If blocks are made once every minute, then user compresses ~2 hours of history during 30 seconds. This computation is also outsourcable to watchtowers.

Peddersen hash is slower than standard keccak256/sha256, so implies an overhead for an operator

---

**HarryR** (2018-12-11):

4m constraints in 30s on 6 cores is impressive, that’s ~130k constraints/sec. Using libsnark with Groth16 I’m only able to manage around 35k-40k constraints/sec on 4 cores (relatively old xeons though).

After more analysis it seems the majority of the time (about 70%) is spend in the heavily optimised `libff::mul_reduce` (multiply over F_p). It would be interesting to see where the differences are, how much is down to newer processor, or if there’s an underlying efficiency that libsnark is missing out on.

