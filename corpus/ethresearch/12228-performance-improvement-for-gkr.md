---
source: ethresearch
topic_id: 12228
title: Performance improvement for GKR
author: AlexandreBelling
date: "2022-03-18"
category: zk-s[nt]arks
tags: [zk-roll-up]
url: https://ethresear.ch/t/performance-improvement-for-gkr/12228
views: 3200
likes: 10
posts_count: 5
---

# Performance improvement for GKR

# Updates on the performances of GKR

(Work with Olivier Bégassat, Nicolas Liochon and Azam Soleimanian)

This post is follow-up to [this post](https://ethresear.ch/t/using-gkr-inside-a-snark-to-reduce-the-cost-of-hash-verification-down-to-3-constraints/7550) and [this post](https://ethresear.ch/t/prover-time-comparison-of-gkr-groth16-vs-groth16-for-proving-mimc-hashes/8373).

Since the previous posts, we have been working on GKR to assess its security and improve its performances. The updates includes (non-exhaustively): algorithmic optimizations of GKR drawn from [Zhang et al](https://eprint.iacr.org/2020/1247), implementation/parallelization improvements, updates of the techniques to update GKR inside a Groth16 circuit, fix for the initial randomness technique. We thank Dan Boneh for helpful discussions, for pointing out mistakes in an earlier version of the protocol and helping us fix it.

The full description of the protocol will be out in a paper soon (including security analysis). For now, we share results for our implementation.

### Update 08/21/2022

The paper is out on eprint,

https://eprint.iacr.org/2022/1072

# Benchmarks

The new benchmarks have been made on a different machine than the first one : an AWS hpc6a (96 physical core + 384 Gb of memory). This machine is cheaper than the one before despite having largely superior computing power. We compare the runtime of our prover and the baseline for parallel MiMC permutations of random values. Our prover consists in proving the hashes using GKR, and using *our construction* to embed it inside a Groth16 circuit. As in the previous post, the results for the baseline are extrapoled and for the same reason : cannot go beyond a certain number of constraints due to the 2-adicity of the bn254 scalar field. Since, the machine has more memory, we have been able to run the benchmark for 2^{24} hashes (as opposed to a maximum of 2^{23} previously).

The implementation can be found [here](https://github.com/ConsenSys/gkr-mimc).

| Nb Hashes | Initial Randomness | Gkr Prover | Groth16 Proof | Total | Baseline (extrapoled) | Hash Per second |
| --- | --- | --- | --- | --- | --- | --- |
| 524288 | 120 (ms) | 3.4(s) | 4.0 (s) | 7.6 (s) | 76 (s) | 68 463 |
| 1048576 | 196 (ms) | 5.4 (s) | 6.4 (s) | 12.0 (s) | 153 (s) | 86 795 |
| 2097152 | 412 (ms) | 13.1 (s) | 7.1 (s) | 20.7 (s) | 306 (s) | 101 214 |
| 4194304 | 756 (ms) | 19.7 (s) | 12.5 (s) | 33.0 (s) | 612 (s) | 126 892 |
| 8388608 | 1293 (ms) | 29.1 (s) | 21.3 (s) | 51.7 (s) | 1224 (s) | 162 149 |
| 16777216 | 2504 (ms) | 51.8 (s) | 24.5 (s) | 78.9 (s) | 2449 (s) | 212 572 |

In other words, we have a ~x31 speed-up in using GKR over directly Groth16 for the 2^{24} instance, achieving a proving speed of 212 572 hashes per second.

## Replies

**dlubarov** (2022-03-22):

Regarding the methods you described for generating initial randomness, would it be fair to say that these are ideas whose security is conjectured, not proven?

For the sumcheck randomness method, the doc says

> The intermediate hashes thus generated (O(b_G+b_N) many) serve as binding commitments to x and y.

It seems this could be viewed as implicitly defining a hash function, H(x, y) \rightarrow \mathbb{F}^{O(b_G+b_N)}, whose output is essentially (part of) the transcript of a sumcheck protocol, where the polynomial being checked involves MLEs x(\cdot) and y(\cdot).

This seems like a novel hash function, and I’m having trouble seeing how it could have collision resistance. Let’s consider just the first round of sumcheck, where u_1(\cdot) is “compressed” to u_2(\cdot) = u_1(r_1, \cdot) using some challenge r_1.

If I understand the idea right, r_1 is derived only from a constant r^\text{sep}, so it’s independent of u_1(\cdot). Given some u_2(\cdot), it seems straightforward to invert the “compression map”, enumerating the many u_1(\cdot) that are mapped to that u_2(\cdot). It seems like these would be collisions, since the rest of the protocol depends on u_2(\cdot) only.

I hope I don’t sound too critical, since it’s a neat idea, and even if we did have to hash x and y entirely, we could do so using a cheaper hash function (to reduce e.g. Keccak to Rescue).

---

**AlexandreBelling** (2022-03-22):

> Regarding the methods you described for generating initial randomness, would it be fair to say that these are ideas whose security is conjectured, not proven?

Thanks for your feedbacks,

I believe you are referring to one of the two “initial randomness” ideas developed in the initial post. Those two ideas are broken. 1) The first one: “using a preemptive sumcheck as a hash function”, is broken because (as you say) it is not collision resistant and direct attack can be built as a consequence. 2) The second approach “sending a commitment of the GKR inputs” is also broken per se, because it allows the prover to forge proofs for arbitrary public inputs.

For clarity, the retained method for the initial randomness, **the fix** (which is also the one we benchmark here) is a variant of the second one. It can be briefly described as follows:

- All inputs/outputs of GKR are passed as public inputs of the outer-SNARK’s circuit
- The prover sends a precomputation of the public input part of the outer-SNARK’s verifier w.r.t. the GKR inputs/outputs elements (instead of sending them directly). K_G.
- Alongside this, the prover sends a proof of knowledge of the exponents (it prevents the attack of initial solution (2)). \pi_G
- The verifier checks \pi_G
- The initial randomness is the hash of what the prover has seen so far \rho.
- The verifier completes the public input part of the outer-SNARK’s verifier with \rho and the other public inputs (e.g. those we would have had we not used GKR at all).
- The verifier runs the remaining parts of the outer-SNARK’s verifier.

By “public input part of the verifier”, we mean for instance:

- For Plonk : reconstructing the public input polynomial commitment \mathsf{PI}
- For groth16 : the multi-exponentiation of the public inputs by a subset of the verification key.

A more detailed version of the protocol is to be published later. The paper is unfinished yet, but the proof of what is described above is complete.

The reason for us, why this “initial randomness” business was critical is because without it, we would end sending more data (a lot more data) than what should be necessary. And for rollups/scalability use-cases, it’s an issue.

---

**dlubarov** (2022-03-22):

Thanks for the clarifications, and glad to hear that a proof has been written now. I didn’t fully follow the updated method, but looking forward to reading about it when the paper is published.

---

**AlexandreBelling** (2022-08-21):

Update:

The aforementioned paper is out on eprint now. It can be found here,

https://eprint.iacr.org/2022/1072

