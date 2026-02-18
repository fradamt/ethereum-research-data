---
source: ethresearch
topic_id: 2337
title: Hash-based VDFs, MIMC and STARKs
author: vbuterin
date: "2018-06-24"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/hash-based-vdfs-mimc-and-starks/2337
views: 12870
likes: 20
posts_count: 29
---

# Hash-based VDFs, MIMC and STARKs

**Edit:** turns out this idea is already out there, on page 20 of https://eprint.iacr.org/2018/601.pdf. Congrats to Dan Boneh, Benedict Bunz, Joseph Bonnneau and Ben Fisch.

MIMC is a hash function “core” that Zcash is evaluating as a possibility to switch to in the mid-term future pending much more security analysis: https://github.com/zcash/zcash/issues/2233

The goal of MIMC is to be maximally SNARK and STARK-friendly, and it does so by building its core primitive to be made up entirely out of simple operations within some finite field. Specifically, MIMC’s permutation function looks as follows:

```auto
                         k_1                     k_2
                          |                       |
                          v                       v
input -----(x->x³)------(xor)------(x->x³)------(xor)---- ..... ----> output
```

The core is made up of a few hundred rounds of this, and each round only adds a very small number of constraints or arithmetic steps into the SNARK/STARK process because it literally is just a single xor/addition and cubing. In fact, one should be able to literally take the techniques in my [STARK](https://vitalik.ca/general/2017/11/09/starks_part_1.html) [tutorial](https://vitalik.ca/general/2017/11/22/starks_part_2.html), as written (see the Fibonacci example), make some minor modifications, and make a STARK out of it fairly easily.

Furthermore, one might notice that this primitive can be calculated in the reverse direction, due to Fermat’s Little Theorem or its prime-power-field analogue, but this would take up to a few hundred times longer. However, making a STARK out of the reversed output is still just as easy (you just calculate the STARK of the reverse computation trace). It seems plausible that with some engineering (and perhaps GPU parallelism), the time taken to compute the STARK could be *lower* than the time taken to run the computation in reverse order, and a possible holy grail would be doing the two *in parallel*.

What this gives us is a verifiable delay function (ie. a function `f(x)=y` where `y` takes some time to calculate that cannot be parallelized away, but `(x, y)` can be easily verified to be an input/output pair of `f`) that *happens to exactly align* with a primitive that is being evaluated for use in hashes, and which hence fulfills the goal of a VDF that only assumes properties of a single cryptographic primitive.

---

*Special thanks to researchers from Stanford, and Zooko Wilcox from Zcash, for pointers and conversations that led to this post.*

## Replies

**sourabhniyogi** (2018-07-31):

Thank you for your *super* accessible [STARKs, Part 3: Into the Weeds](https://vitalik.ca/general/2018/07/21/starks_part_3.html) tutorial and 100% working python implementation.

I did a port of your `mimc_stark` to Go and posted it here

https://github.com/wolkdb/deepblockchains/tree/master/stark

for more of us to really get in the weeds and incorporate STARKs into deployable blockchain designs.

---

**vbuterin** (2018-07-31):

Great job!

Also good to see that the STARK overhead is ~300x in another language implementation ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

I noticed that the verifier is not significantly faster in go vs python. I guess that’s because STARK verification is mostly just hash calculation?

---

**sourabhniyogi** (2018-08-01):

Thank you – there are tons of parallelizations of verify branch part that are easy to add in go, will explore that this month and report back –

---

**vbuterin** (2018-08-01):

You can parallelize the prover very heavily as well; FFTs, Merkle tree generation and FRI are all highly parallelizable.

---

**sourabhniyogi** (2018-08-13):

I streamlined the [Go STARK implementation](https://github.com/wolkdb/deepblockchains/tree/master/stark) with goroutines, channels + big.Int optimizations and on an ordinary laptop (2014 MacBook Pro 2.2 GHz Intel Core i7 with 8 “logical” cores) got to this basic level of temporal performance:

| NUM_CORES | STARK Proof Generation | STARK Verification |
| --- | --- | --- |
| 1 | 3.12s | 46.11ms |
| 2 | 2.01s | 24.70ms |
| 4 | 1.49s | 15.64ms |
| 8 | 1.42s | 16.58ms |
| 16 | 1.49s | 18.30ms |
| 32 | 1.48s | 20.18ms |
| ethereum/research python | 3.78s | 52.10ms |

---

**vbuterin** (2018-08-14):

Wow! So python actually is not all that suboptimal for this stuff.

Can you also give the numbers for MIMC calculation, and reverse MIMC calculation (replace `x := x**3+p` with `x:= (x-p)**((2*p-1)//3)` mod p)?

Also, any idea why adding more cores doesn’t improve things beyond 1.4s? Is there some part of the computation you’re not parallelizing? Merkle tree calculation, FFTs, and FRI computation should all be quite parallelizable.

---

**sourabhniyogi** (2018-08-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Can you also give the numbers for MIMC calculation, and reverse MIMC calculation (replace x := x**3+p with x:= (x-p)**((2*p-1)//3) mod p)?

Yes - will report back on this shortly.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Also, any idea why adding more cores doesn’t improve things beyond 1.4s? Is there some part of the computation you’re not parallelizing? Merkle tree calculation, FFTs, and FRI computation should all be quite parallelizable.

The program flow has to actually use the cores available to it to get improvements, with goroutines/channels/waitgroups/… structured in a pipeline matching the cores nicely – so if you have a machine with 64 cores with only 3 go routines running computation (1), (2) and (3) in parallel, you aren’t going to do much better than with just 3 cores.  On the other hand, if you have a machine with 8 cores, having 128 goroutines running through 128 pieces of a for loop will have worse performance than if you just have 8 goroutines.  To minimize the time of STARK proof generation, its essential to take the computational dependency graph, break it into stages, and focus on the key bottlenecks of the longest route.  This is what the pipelined version of your STARK looks like in my Go re-implementation, with sample times attached:

[![proof-goroutine-flow](https://ethresear.ch/uploads/default/optimized/2X/5/53446611200756e1f284a7d4c927483cbd8eca0a_2_271x500.png)proof-goroutine-flow1148×2118 470 KB](https://ethresear.ch/uploads/default/53446611200756e1f284a7d4c927483cbd8eca0a)

The longest route is currently (2a+b+c) => (4a+b) =>(7) => (8) => (9) => (11) => (12) (shown in red).   Inside the longest route are the time consuming FFTs + inverse FFTs (in step (2b)+(2c)], multi_interp_4 (in step (11)) –  I did make a first pass at parallelizing these internal operations, but I’m certain we can do a lot more.

Here is the verification part, much easier to reason about:

[![verify-goroutine-flow](https://ethresear.ch/uploads/default/optimized/2X/8/858fa1e1e5c5be02a6c8b25981dece0be16ffe3d_2_690x395.png)verify-goroutine-flow1844×1056 110 KB](https://ethresear.ch/uploads/default/858fa1e1e5c5be02a6c8b25981dece0be16ffe3d)

Most of the time, breaking up a for loop into N goroutines [as in (v4)] is totally worth it (for some N, but less worth it for 2N), but sometimes its not (because the overhead of the goroutine is just too high) – so it makes for a lot of empirical engineering.  With gradient descent in the parameter space, we can have confidence there is another 25-40% speedup to be squeezed out of the proof timing.  We’ll try out beefy machines with 24-32 cores for comparison this month and report back.

---

**vbuterin** (2018-08-15):

Why can’t the FFT be massively parallelized? There’s no reason for parallelization to be between functions and not within one function.

---

**sourabhniyogi** (2018-08-16):

No debate that FFTs should be parallelized.  Here are the basic stats on Forward + Reverse MiMC in C, Go, Python, JS [(code here)](https://github.com/wolkdb/deepblockchains/tree/master/vdf/mimc):

| Implementation | Forward MiMC | Reverse MiMC |
| --- | --- | --- |
| C - mimc.c | 1.85ms | 122.7ms |
| Go - mimc_test.go | 6.11ms | 278.8ms |
| Python - mimc.py | 13.40ms | 1,291.4ms |
| Node.js - mimc.js | 108.29ms | 13,910.1ms |

[Stats taken from an 2015 iMac 3.2 GHz Intel Core i5]

---

**vbuterin** (2018-08-16):

Is the STARK proof generation time given above (1.5-3s) for the same parameters as this? If so, that seems very weird. Why is go <2x faster than python for STARK generation but 4x faster for MIMC computation?

---

**sourabhniyogi** (2018-08-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Is the STARK proof generation time given above (1.5-3s) for the same parameters as this? If so, that seems very weird.

The *Forward MiMC* timings [1.85ms in C, 6.11ms in Go, 13.40ms in Python] are *just* the computations of `mimc(3, 2**LOGSTEPS, constants)` you have in [your proof generation](https://github.com/ethereum/research/blob/master/mimc_stark/mimc_stark.py#L49) [*just* step (2a) in the diagram] and [your verification](https://github.com/ethereum/research/blob/master/mimc_stark/test.py#L48) [step (v1) in the diagram], with the same parameters (same 8192 steps, same 64 constants, etc.) … just in different languages, with their various bigint libraries.  More cores doesn’t speed up Forward MiMC or Reverse MiMC, of course.

If you replace step (2a)'s Forward MiMC in Go [here](https://github.com/wolkdb/deepblockchains/blob/5ca08626adb3e12841620448408847d98cf80f2d/stark/proof.go#L246) with Reverse MiMC then the STARK proof generation will take ~272.69ms (278.8ms-6.11ms) longer [1.42s will become 1.69s]., because (2a) is on the longest path.

If you replace step (2a)'s Forward MiMC in Python [here](https://github.com/ethereum/research/blob/master/mimc_stark/mimc_stark.py#L49) with Reverse MiMC then the STARK proof generation will take ~1278ms (1,291.4ms-13.40ms) longer [that is, 3.78s becomes 5.05s].

Does that make sense?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Why is go <2x faster than python for STARK generation but 4x faster for MIMC computation?

For MiMC computation, the idiosyncrasies bigInt implementations (with memory setup/…) in each language obviously dominate, because that’s pretty much the only thing going on.  For STARK generation, the computations of the longest path use bigInt everywhere in the pipeline, but because you can parallelize almost all the steps in the pipeline, there is no heuristic like “its X times faster when you use L language” – what the level of improvements ends up at will depend on the structure of the pipeline and the amount of resources allocated to it.

Succinct prototyping in Python (because it handles bigInts and vectors so well) and putting things into production in a C library with a Go/Rust/… wrappers is the sane thing to do for VDFs + STARKs.

---

**daira** (2018-11-23):

You probably don’t want to use Reverse MiMC; it’s very slow. Instead use MiMC in Feistel mode, so that decryption is as fast as encryption.

---

**vbuterin** (2018-11-24):

The goal here is to be slow in the forward direction as that’s the direction the VDF is computed, and fast in the backward direction for proving/verification. So symmetric execution time is *not* desired.

---

**jgm** (2019-02-12):

Worth noting that the overall size of the proof generated by this code can be shrunk significantly by changing the Merkle root to root + *n* levels of branches and generating the proofs up to the highest branch than down to the root each time.

I couldn’t find a name for “root + *n* levels of branches” so called it a Merkle pollard.  Details are at https://medium.com/@jgm.orinoco/understanding-merkle-pollards-1547fc7efaa (skip to the section “Merkle pollards” to avoid the part explaining what Merkle trees are).

---

**vbuterin** (2019-02-12):

The MIMC stark code already does some Merkle proof compression via a separate compression algorithm that detects duplicate hashes and replaces them with a symbol. That said, I’m sure it’s suboptimal and there’s better ways to do the same thing, especially since any top levels of the tree that are fully covered by merkle branches can be left out entirely. I feel like optimal Merkle proof batching is a problem that someone somewhere has already come up with a neat clever algorithm for… something like “start with all the nodes for all branches, including both the branch and the sisters, and then repeatedly detect and remove any nodes for which both children are either in the proof or have been already been removed due to being calculable”.

---

**jgm** (2019-02-12):

Some sort of “proof tree”, if my mental image of the resulting structure is correct.  Interesting idea but not sure how much of a saving it would be over a simple pollard, which wouldn’t require additional pointers to link the common branches of proofs together.  Might have a play to see if there are additional space savings to be made.

---

**vbuterin** (2019-02-13):

I made a quick implementation: https://github.com/ethereum/research/blob/7db6b87cf8642a8671dd9890909586912a0929c9/mimc_stark/merkle_tree.py#L37

It seems to have reduced the size of the STARK proofs by nearly 20%, relative to what was already a pretty decent compression mechanism.

---

**tawarien** (2019-02-13):

Some years ago I developed an algorithm for the merkle tree traversal problem which asks the question which nodes to store of a merkle tree between generating authentication paths for leaf(i) & leaf(i+1) and which nodes to recalculate on demand. The goal is to have a good/optimal trade-off between required memory and required recomputation and it should be configurable. This is used for signature generation in merkle signature schemes. One component repeatedly used is the so called TreeHash algorithm which allows to calculate a node from its leaf requiring O(N) hashing and O(log(N)) memory (excluding the leafs (these are calculated in all merkle signature schemes instead of stored)). Where N is the number of leafs. Its a straight forward algorithm and probably used a lot outside of merkle signatures schemes as well. I think that by cleverly ordering the Nodes of your output this algorithm could be adapted to reduce the memory footprint and increase the performance of the verify process by recalculating the root from the proofs, proofing all proofs at once instead of calculating all the missing nodes and then proof each leaf individually. If I find time I will do an implementation of it

---

**denett** (2019-02-23):

First compliments on the three-part Stark explainer, great work.

I finally came around downloading the python code to look at its inner workings and I think I found a weak spot.

At every stage of the recursion you sample the rows that are checked based on the merkle root of the values of the column. Because we sample only 40 rows, we can get away with quite some changes in the column without getting caught. For example, if we change 10% of the numbers in the column and do 40 samples, we have a chance of 1.4% of not getting caught. We can easily try multiple variants of the column to beat the odds.

When we start with a high degree polynomial and have 10 levels of recursion, it is possible to change all points in such a way that they are all on the same low degree polynomial once we reach the final check.

To make this attack harder we could sample the rows of all levels based on the last merkle root. In that case we have a chance in the order of 10^{-19} which is much better. Turning it into an interactive proof via the blockchain is also possible, but might be less practical in some cases.

To avoid this attack altogether and also make the proof smaller, we should follow the sampled points from the base layer all the way to the final polynomial. So instead of sampling just one value on the column per check, we should sample the 3 sibling values as well, to use in the next recursion step. Skipping the second lookup per merkle tree can reduce the total size of the proof significantly.

By following these “point-traces” all the way, we make sure they have not been tampered with. You could still try to tamper with the sibling points, but this is not useful without knowing the column that will be chosen next.

---

**jgm** (2019-02-25):

[@vbuterin](/u/vbuterin) thanks for the code; finally had a chance to look at it and think about how it compares with pollarding.

Given that the chance of removing any given hash is related to the ratio of proofs to data values (plus level in the tree, of course) it’s no surprise the more proofs there are the better the overall reduction.  At relatively low levels (1:256, or 64:16384 as was actually tested) there is little difference and depending on the encoding method for the data it can be less efficient than pollarding (as the empty placeholders still take up some space).  But stepping this up to higher ratios brings in higher efficiencies, for example at 1:32 (512:16384) it is about 30% more efficient than pollarding (which is itself 60% more efficient than simple proofs).  A nice increase for many real-world cases.

An interesting difference is that both generation and verification of proofs require all of the individual proofs to be present; with the former this maximises the gain and with the latter it guarantees all values are in place to enable verification.  This makes pollarding potentially better for interactive proofs where the pollard can be sent once and subsequent proofs can refer to it.

The ultimate solution would be to have a progressive interactive version of your system where both sides remember the proofs that have been sent to date and so over time proofs sent can be more and more efficient as they require fewer new hashes to verify.  Probably not something that would be a common requirement, however (and it comes with its own trade-offs).

If you don’t mind I’d like to write up the solution (thinking of calling it “spare tree proofs” unless I can come up with something catchier) as a companion piece to the one I wrote on pollarding.


*(8 more replies not shown)*
