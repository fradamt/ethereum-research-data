---
source: ethresearch
topic_id: 8373
title: Prover time comparison of GKR+Groth16 vs. Groth16 for proving MiMC hashes
author: AlexandreBelling
date: "2020-12-15"
category: zk-s[nt]arks
tags: [zk-roll-up]
url: https://ethresear.ch/t/prover-time-comparison-of-gkr-groth16-vs-groth16-for-proving-mimc-hashes/8373
views: 7330
likes: 27
posts_count: 19
---

# Prover time comparison of GKR+Groth16 vs. Groth16 for proving MiMC hashes

Olivier Begassat, Alexandre Belling, Gautam Botrel, Nicolas Liochon, Thomas Piellard

# Prover time comparison of GKR+Groth16 vs. Groth16 for proving MiMC hashes

Following our proposal [here](https://ethresear.ch/t/using-gkr-inside-a-snark-to-reduce-the-cost-of-hash-verification-down-to-3-constraints/7550) we present the results of our implementation of GKR+Groth16 for MiMC7. This post contains a comparison of proving times for 2^23 (~8M) MiMC hashes using two approaches:

1. straightforward hash circuit in Groth16 using Gnark (extrapolated from the proving time for 2^17 hashes)
2. our GKR+Groth16 approach: generate a GRK proof, feed it to a GKR verifier  embedded a in a Groth16 SNARK circuit and generate the associated SNARK proof with Gnark.

The latter is 27 times faster than the former, i.e. 3 minutes for GKR+Groth16 vs. 1 hour and 24 minutes for Groth16 only.

## The circuit

The GKR circuit performs a check on the MiMC permutation BN256 scalar field (as opposed to our initial proposition to do it with gMiMC7). It consists of 91 layers with an identical structure but using layer specific round constants. Every layer is made up of gates of the following types:

- Copy gates that output the values of their left entry (ignoring the value on the right entry). \text{copy}(v_l, v_r) = v_l.
- Nonlinear gate \text{nonlin}(v_l, v_r) = v_l + (v_r + c)^7
- Final round nonlinear gates \text{fnonlin}(v_l, v_r) = (v_r + c)^7

(To be precise: every layer except the last contains copy and nonlinear gates while the last layer contains only final round nonlinear gates.)

The *base*-circuit is made up of 91 layers, each of which has two inputs, let’s say v = [v_0, v_1], and produces two outputs (except for the final layer, producing only one). There are 2^{b_N} (e.g. 2^{23}) parallel copies of the base-circuit. At every intermediary layer the outputs of the base-circuit are [\text{nonlin}(v_1, v_0), \text{copy}(v_1, v_0)]. In the final (output) layer the base-circuit outputs [\text{fnonlin}(v_l, v_r)] only. Notice that the MiMC round function as described in the paper is of the form x \rightarrow (x + c + k)^7. Pipelining the operations x \rightarrow x^7, x \rightarrow x + c and x \rightarrow x + k results in \text{nonlin} being of degree 1 in v_r. This saves a lot of time in the prover. It is, however, important to pre-add v_0 = v_0 + v_1, in the first layer and to use the final round nonlinear gate in the last layer.

## The results

We benchmarked our implementation on a 32 core AWS c5.24xlarge instance. Our benchmarks include the time needed to generate the GKR proof and the time needed to build the SNARK proof of a circuit verifying the GKR proof. It also includes the assignment time for both of those steps. For the benchmark we set bN = 23 (ie: we prove 8M hashes)

For the baseline, we benchmark the running time for the assignment and the prover time of a gnark circuit which verifies MIMC. Since SNARK circuits verifying 8M hashes are impractical over the curve bn256, we extrapolated results obtained with fewer hashes. We benchmarked 2^17 hashes and scaled the results up to 2^23.

We implemented the [following circuit](https://github.com/ConsenSys/gkr-mimc/blob/c1d9e73b275640d0b8924b179d4681e5dba4180f/snark/hash/mimc_test.go#L17) to measure Gnark’s performance.

| Op | Runtime (sec) |
| --- | --- |
| Groth16 Prover - 2^15 hashes | 20.2 |
| Groth16 Prover - 2^17 hashes | 78.2 |
| Extrapolation to 2^22 hashes | 2587.0 |
| Extrapolation to 2^23 hashes | 5006.3 |

We [implemented](https://github.com/ConsenSys/gkr-mimc) the GKR prover and the Groth16 circuit of proof of the proof verification.

With 2^22 (~4M) hashes:

| Op | Runtime (sec) for 2^22 hashes | Runtime (sec) for 2^23 hashes |
| --- | --- | --- |
| GKR Prover assignment | 6.0 | 8.4 |
| GKR Prover | 50.0 | 95.7 |
| SNARK Assignment | 0.3 | 0.66 |
| SNARK Prover | 48.2 | 76.5 |
| Total | 104.6 | 181.2 |
| Baseline | 2587.0 | 5006.3 |

Which is a 27-fold improvement compared to the baseline for 8M hashes.

## Observations and possible improvements

### Constraints per second

Gnark performances for MiMC hashes are far better than the ones for the GKR proof checker when we look at the metric “number of constraints per second”. The table below shows that there are many more wires in the GKR proof verification circuit than in the circuit verifying the MiMC hashes. In other words, the number of constraints is an imperfect indicator for performance to be expected.

| Circuit | Number of constraints | Number of coefficients | Number of wires |
| --- | --- | --- | --- |
| SNARK MiMC - 2^17 hashes | 47841280 | 93 | 47972353 |
| SNARK GKR - 2^23 hashes | 32516244 | 95 | 49311227 |

### Impact on the number of hashes on the proving time

With a simple Groth16 prover proving time grows linearly with the number of hashes. Groth16 + GKR has a sublinear (logarithmic) overhead, subsequently the more hashes to verify the more interesting this approach is.

### Future work

It is possible to apply this approach to other types of hash functions (e.g. Poseidon) and altogether different purposes (e.g. signature verification). The GKR path is not fully optimized. Specializing the implementation, plus various optimizations should lead to a >30\times improvement.

## Replies

**vbuterin** (2020-12-16):

This is amazing work!

How difficult would it be to retool this for the use case of making a SNARK proof of a Merkle witness? It seems like this could completely solve our stateless client issues even with greatly expanded blocks.

---

**AlexandreBelling** (2020-12-16):

Thanks Vitalik!

The only thing we miss before we can do that is a feature to interact more nicely with the gnark solver. This is on our todo-list already.

---

**kladkogex** (2020-12-16):

Really nice !

Can this be verified in solidity ?) Does it use  the same curve that is implemented as a precompiled smartcontract?)

Another question : why did you have to extrapolate? Couldnt you just run it for 2500 seconds?

And also, could you describe what type of a machine you used (CPU, RAM)?)

---

**AlexandreBelling** (2020-12-16):

Thanks [@kladkogex](/u/kladkogex)

> Can this be verified in solidity ?) Does it use the same curve that is implemented as a precompiled smartcontract?)

It can be verified in a smart-contract depending on the curve that you use for the Groth16 part. In our case the GKR verifier is embedded in an R1CS and the Groth16 proof is built on the Bn256 curve so you could verify that. From a practical point of view, as I replied we just miss a few features to make it usable on a smart-contract, but this is not a matter of protocol.

> Another question : why did you have to extrapolate? Couldnt you just run it for 2500 seconds?

The reason we had to extrapolate, is that 4-8M hashes takes up to 1.5-3B constraints in a circuit. And you can’t make proofs for circuits that are this big with Bn256 (although it would have been possible to do so with BLS12-381 if not mistaken). The reason is that the FFT would not be as efficient and the proving time would explode.

> And also, could you describe what type of a machine you used (CPU, RAM)?)

For the machine, it’s an AWS c5a.24xlarge and we used 32 cores (our implems works better with powers of 2 cores). You can find the spec here: [Amazon EC2 C5 Instances — Amazon Web Services (AWS)](https://aws.amazon.com/ec2/instance-types/c5/)

It has 48 phyiscal cores (96 virtuals) and 192 GB of RAM, but we ran the benchmarks with the hyperthreading disabled

---

**kladkogex** (2020-12-16):

Alexandre -  thank you! Another question that I have been asking many people, and did not get an answer so far.

Lets say, I have a Merkle tree of 1000 signed transactions.

Lets assume it used MiMC for hash, and the signatures are ZKSNARK friendly (I do not know which is the friendliest signature).

Lets assume I have the public key for every transaction (for simplicity we can even assume that all transaction is signed by the same ZK-friendly public-private key pair.

Suppose, one wants a ZK proof that all transactions have valid signatures, and that the Merkle root of the tree is correct.

Very roughly, what would be you gut feeling for the time it will take to compute this proof?

We can assume the same type of AWS machine ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**AlexandreBelling** (2020-12-16):

[@kladkogex](/u/kladkogex)

For this use-case, I assume you would not benefit from the GKR approach. The most efficient way (I think…) to do it is to use 5-ary Merkle-Tree with Poseidon. You would need 5 levels to fit all your transactions. In fact, you could fit 3125 transactions like this. From [this post](https://ethresear.ch/t/gas-and-circuit-constraint-benchmarks-of-binary-and-quinary-incremental-merkle-trees-using-the-poseidon-hash-function/7446) it would cost 2182 constraints per path verification.

The signature would be EDDSA with baby jubjub and would takes 4000 constraints. Each transaction would fit in 5 fields elements (possibly less), we can reuse Poseidon here again. So 217 (not sure about the exact number but probably this +/- 1 constraint) extra constraints.

To sum up, you would have ~6300 constraints for each signature verification. With our machine and with 32 threads you would be able to prove in ~11-12 seconds.

Edit: I also assumed you would do it with gnark

---

**kladkogex** (2020-12-16):

Thank you Alexandre! Thats very informative!

---

**ValarDragon** (2020-12-29):

Its cool to see efficiency of GKR’s arithmetization getting worked out for circuits of interest.

How is the non-native arithmetic for the GKR verifier being handled on AltBn256? Are you using non-native arithmetic in R1CS?

One point re asymptotics:

> With a simple Groth16 prover proving time grows linearly with the number of hashes. Groth16 + GKR has a sublinear (logarithmic) overhead, subsequently the more hashes to verify the more interesting this approach is.

Groth16’s prover is nlog(n) with the circuit size (and therefore number of hashes). You’re GKR prover is also at least linear in the number of hashes. (All SNARK provers *must* be linear in the witness size) Even with recursion, the proving time cannot be sublinear in the number of hashes.

I’d frame why this is faster as stemming from two factors:

- Its using GKR’s tailored arithmetization
- With one layer of recursion, you can do tricks to reduce the logarithmic overhead from FFTs / allow for worse verifiers in your first SNARK

The interesting comparison point imo would be to compare this across GKR’s arithmetization as your inner snark, and an AIR / PLONK arithmetization. (In addition to relative to plain groth16. Its pretty clear that tailored arithmetizations for a particular problem should have provers that outperform a snark for pure r1cs) Its not at all clear to me why GKR’s arithmetization is inherently better for this than an AIR-style / Plonk-style approach.

---

**AlexandreBelling** (2021-01-05):

> How is the non-native arithmetic for the GKR verifier being handled on AltBn256? Are you using non-native arithmetic in R1CS?

We use native arithmetic only. The only cryptographic primitive we use is a hash function (Mimc7 even though we don’t need to reuse the same hash function than the one encoded in the GKR circuit). Since GKR does not use elliptic curves crypto in itself, we don’t need to resort to non-native arithmetic.

However, if you meant using a GKR circuit to handle non-native arithmetic. I don’t really know, how to do that efficiently. There would be likely a ton of layers, and the inputs/output would be very large. So we don’t know if it would be profitable in the end.

> Groth16’s prover is nlog(n) with the circuit size (and therefore number of hashes). You’re GKR prover is also at least linear in the number lof hashes. (All SNARK provers  must  be linear in the witness size) Even with recursion, the proving time cannot be sublinear in the number of hashes.

By logarithmic overhead, we meant the “sumcheck verification” part of GKR (ie: the “layer by layer” claim delegation). To clarify, we wanted to emphasize that the GKR approach works only if you have enough hashes to check. Also, yes in theory Groth16 prover is loglinear but in practice the FFT never really outweights the multiexponentation part (5%-10% of the runtime depending on the circuit size). That’s why we used a linear model for the extrapolation. But that’s worth clarifying as well.

> The interesting comparison point imo would be to compare this across GKR’s arithmetization as your inner snark, and an AIR / PLONK arithmetization. (In addition to relative to plain groth16. Its pretty clear that tailored arithmetizations for a particular problem should have provers that outperform a snark for pure r1cs) Its not at all clear to me why GKR’s arithmetization is inherently better for this than an AIR-style / Plonk-style approach.

The way I see it, is that layered arithmetic circuits are less expressive, than R1CS/Plonk and AIR. This means (obviously) that less computation can be properly modeled like that. You mentionned “recursion” but I don’t think you could implement a recursion for GKR or for a GKR-like protocol inside another one. However, their “feed-forward” and “data-parallel” properties can, on another hand, be leveraged to build more efficient (specialized?) proof systems.

For instance, GKR is a protocol in which the prover does not build any “form of commitment to the intermediate values of the computation” and the verifier does not need to know the “intermediate values” as well.

---

**dlubarov** (2021-01-06):

Very cool!

The writeup mentions that you evaluate MLEs of the 2n inputs and n outputs using 3n multiplications. Could you explain how that’s done? I know it can be done in linear time, as in [Vu et al](https://www.ieee-security.org/TC/SP2013/papers/4977a223.pdf) 5.1, but it seems their method involves 3n multiplications for n inputs (assuming n is a power of two).

---

**AlexandreBelling** (2021-01-07):

Assume you want to evaluate a multilinear whose values are stored in a vector **x** of length 2^n on a vector **d** of size n.

for i in 0…n {

- for b = 0…2^{n-i-1} {

x[b] = x[b] + (x[b+2^{n-i-1}] - x[b]) \times d[i]

}

}

return x[0]

---

**dlubarov** (2021-01-17):

Thanks for explaining; that’s a nice approach.

It seems like this uses 91 rounds of MiMC-2p/p – could you explain how you arrived at that? It seems like the [MiMC](https://eprint.iacr.org/2016/492) paper would suggest 2 \left\lceil \frac{\log_2 p}{\log_2 7} \right\rceil = 182 rounds, assuming that we can generalize their formulas for larger \alpha besides 3, which I’m not certain about. (It seems logical for interpolation, but I don’t know about other attacks.) I saw that the [GMiMC](https://eprint.iacr.org/2019/397) paper gives some more general formulas, but I’m not sure they help in this case.

---

**AlexandreBelling** (2021-01-17):

If I am correct, the one we implemented uses MiMC-p/p as opposed to the one we described in the initial post that uses MiMC-2p/p. We choosed to switch because of recents attacks founds on gMiMC which in the end made the approach less practical.

---

**David** (2024-02-05):

Sorry for necroposting, but I’m wondering what is the state of the Consensys/gkr-mimc repo seeing that it hasn’t been updated in a really long time + gnark now has an implementation of GKR in its stdlib

---

**AlexandreBelling** (2024-02-06):

Hey, yes the go-to implementation is the one in gnark. `Consensys/gkr-mimc` has been abandoned

---

**liochon** (2024-02-08):

btw, the paper corresponding to the original post was presented at CCS 2023 (3+ years after the first post…) : [Recursion over Public-Coin Interactive Proof Systems; Faster Hash Verification | Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security](https://dl.acm.org/doi/10.1145/3576915.3623078)

---

**AlexandreBelling** (2024-10-28):

I don’t get the point here. If you care about how many hashes you can do with our technique, the main driver is the maximal number of constraint your particular parameters (elliptic curves, proving scheme) allow. And anyway, with more recent techniques used for EVM/VM execution proving we can prove the equivalent of a hundred time more computation than what is possible with a single Groth16 circuit.

I believe 1B hashes at once is possible if it was not done before (I vaguely recall an announcement that somebody achieved this, but I am not sure where it came from nor if it actually happened).

---

**AlexandreBelling** (2024-10-28):

You mean, how to get from 27x to 30x? We haven’t planned to specifically spend time on this as we are happy with the perfs on the GKR side.

