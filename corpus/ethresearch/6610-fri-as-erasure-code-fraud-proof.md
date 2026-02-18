---
source: ethresearch
topic_id: 6610
title: FRI as erasure code fraud proof
author: vbuterin
date: "2019-12-10"
category: Sharding
tags: [fraud-proofs]
url: https://ethresear.ch/t/fri-as-erasure-code-fraud-proof/6610
views: 7797
likes: 6
posts_count: 25
---

# FRI as erasure code fraud proof

*Special thanks to Eli Ben-Sasson for discussions*

One lower-tech alternative to [using STARKs to prove](https://ethresear.ch/t/stark-proving-low-degree-ness-of-a-data-availability-root-some-analysis/6214) the correctness of a Merkle root is based around the underlying technology behind STARKs: FRI (see [here](https://vitalik.ca/general/2017/11/22/starks_part_2.html) for a technical intro).

To give a quick recap, the problem statement is that you have a Merkle root of 4n leaves (we’ll use the number 4 for illustrative purposes; it could be any constant), which claim to represent a degree < n polynomial evaluated at 4n points. The goal is to prove that a very large fraction of the points (eg. > 90%) actually are evaluations of the same polynomial.

For example, if n = 2, then one *completely valid* evaluation set would be [10, 11, 12, 13, 14, 15, 16, 17] (representing y = x + 10). An *almost valid* evaluation set might be [55, 57, 59, -888, 63, 65, 67, 69] (representing y = 2x + 55 except at one point), and an *invalid* evaluation set might be [80, 90, 100, 110, 4, 5, 6, 7].

[![rooot](https://ethresear.ch/uploads/default/optimized/2X/d/d8b0704339dc34a6e62d15821f914d20a6613506_2_690x418.png)rooot742×450 14.6 KB](https://ethresear.ch/uploads/default/d8b0704339dc34a6e62d15821f914d20a6613506)

FRI proves that an evaluation set is completely valid or almost valid by doing random sampling: it involves committing to a degree \frac{n}{4} polynomial, checking the evaluations at a few dozen points to prove that in a certain sense the degree \frac{n}{4} polynomial represents the same function (read [the intro](https://vitalik.ca/general/2017/11/22/starks_part_2.html) to understand this in detail), and then repeating until you get to a very low-degree polynomial that you can check directly. The possibility of admitting *almost* validity (only 80-99% of points are correct) arises because it’s very easy for a random check to miss any specific single point that might contain a mistake.

Now, suppose that we have a Merkle root that represents (maybe with a few mistakes) some polynomial p(x), and we want to determine an evaluation at some position, *without the possibility of a mistake*. It turns out that we can do this, but it’s more expensive than a simple Merkle branch. We need to use a “subtract-and-divide” trick: to prove that p(z) = a, we commit to a Merkle root of a set of evaluations of *another* polynomial, q(x) = \frac{p(x) - a}{x - z}, and then make a set of queries (ie. provide a randomly selected set of Merkle branches) to the original set of evaluations and the new set to prove that they match (or almost-match), and then do a FRI proof on the new set to prove that it’s a polynomial.

The trick here is that if p(z) is *not* a, then p(x) - a is not zero at z, and so x - z is not a factor of p(x) - a, so the result would be an expression with a quotient, and not a polynomial.

[![rooot2](https://ethresear.ch/uploads/default/optimized/2X/a/a60ac7917567f8d3c7dcdf55479bbe52942fb55c_2_690x157.png)rooot21981×451 31.4 KB](https://ethresear.ch/uploads/default/a60ac7917567f8d3c7dcdf55479bbe52942fb55c)

Notice how even if we are trying to obtain the evaluation at the position where the original data is incorrect, the correct evaluation leads to a well-formed q(x) and the original incorrect evaluation leads to a poorly-formed q(x). In this case, since p(x) is only a degree-1 polynomial, q(x) will be a deg-0 polynomial, or a constant; in other cases q(x) will generally have a degree 1 less than p(x).

Evaluating *at* the position x=z is more difficult since simple pointwise evaluation gives you \frac{0}{0}, but we can just ignore this and put any value as almost-correct evaluations will generally still pass FRI.

One approach would be to use this technique as our evaluation proving scheme directly instead of Merkle proofs. But the problem here is that FRI proofs are big (~20 kB for big inputs) and take linear time to produce. So what we will do instead is use FRI as a *fraud proof*.

### FRI as fraud proof

Suppose, as in the data availability check setting, that an honest node attempting to make a fraud proof has > \frac{1}{4} of some data D that is an erasure-code extension of some underlying data D^{*} (ie. it’s a deg < |D^{*}| polynomial where the first quarter of the evaluations are D^{*} and the rest can be used to recover D^{*} if parts of D^{*} are missing). The node uses the > \frac{1}{4} of D that it has to recover the rest of D, and realizes that the Merkle root of the provided D and the Merkle root of the reconstruction do not match, ie. the D provided has errors. The challenge is: can the node prove that this is the case without providing the entire > \frac{1}{4} of D in its possession?

We solve this as follows. When performing data availability checks, we require *clients* to do one extra step. In addition to randomly sampling k Merkle branches (eg. k = 80), they also ask for the middle level of the tree (ie. the level where there are \sqrt{|D|} nodes where each node is itself a sub-root of \sqrt{|D|} data). This ensures that for any blocks that clients accept, this data is available.

If a checker node downloads > \frac{1}{4} of D (from the responses rebroadcasted by clients making samples), and its finds that the Merkle root of the reconstructed D does not match the original Merkle root, then this implies that there is some position where the original data gives an incorrect value. The checker node downloads the middle layer of the tree (guaranteed to be available because clients asked for it before accepting the block), and finds one sub-root in this layer which differs from the sub-root of the data that they reconstructed; at least one such discrepancy is guaranteed to exist.

[![rooot3](https://ethresear.ch/uploads/default/optimized/2X/1/15db707fd15ee12d94d500afc8e0630656b98d4a_2_690x222.png)rooot31442×464 27.9 KB](https://ethresear.ch/uploads/default/15db707fd15ee12d94d500afc8e0630656b98d4a)

Let x_1 ... x_n be the set of positions inside this faulty sub-root, and y_1 ... y_n be the “correct” evaluations that the checker node computes. The checker node computes an *interpolant* I(x), which is the deg < n polynomial that evaluates to y_i at x_i for every x_i in this set. This can be computed using Lagrange interpolation, though if we are clever we can specify the coordinates in the tree such that any subtree is a multiplicative subgroup shifted by a coordinate so that we can compute the interpolant using an [FFT](https://vitalik.ca/general/2019/05/12/fft.html) (the explicit construction for this would be for the positions to be powers of a generator \omega sorted by the exponent in binary form with bits reversed, so [1, \omega^4, \omega^2, \omega^6, \omega, \omega^5, \omega^3, \omega^7] if |D| = 8).

Let p(x) be the polynomial that D almost-represents. We will prove that ((x_1, y_1) .. (x_n, y_n) \in p(x) by committing to q(x) = \frac{p(x) - I(x)}{(x - x_1) * ... * (x - x_n)}, and then proving two claims: (i) q(x) matches p(x) at some randomly selected points, and (ii) q(x) is a polynomial (or almost-polynomial). The fraud proof then consists of the set of evaluations ((x_1, y_1) .. (x_n, y_n), sets of probabilistic checks to prove the two claims, along with a Merkle path to the *incorrect* root in D(x); verifying the proof would involve verifying the checks, and then verifying that the *reconstructed* root of ((x_1, y_1) .. (x_n, y_n) and the *provided* root inside of D do not match.

One important and subtle nuance here is that for the q(x) vs p(x) check to be sound, we need to randomly sample positions from D, but the checker only has at least \frac{1}{4} of D, and so will generally not be able to successfully provide p(x) responses for the challenges in the proving process. There are two solutions here.

First, the checker node can masquerade as a client and ask the network for samples; the attacker publishing D would have to provide the desired values in D to convince the “client” that the block is available.

Second, we can require the checker to have a larger fraction of D, eg. at least \frac{1}{2}, and then prove a probabilistic claim: q(x) matches p(x) on at least 40% of the sampled claims. Making this proof would require hundreds of queries for statistical soundness reasons, but the proof is already \sqrt{|D|} sized so this would not make it *that* much bigger; also, a Bayesian verification scheme can be used that automatically terminates earlier if a checker successfully answers more queries, which would happen in the usual case where they have much more than 50% of the data. A valid D would not match an invalid q(x) on more than 25% of positions, so a malicious checker would not be able to generate a fraud proof for valid data.

### FAQ

- Why make I(x) from a \sqrt{|D|} sized set of evaluations, why not check a single point? Answer: because we are not guaranteed to have the attacker’s provided value at any specific single point, but by checking the middle leaves we are guaranteed to have the attacker provide a hash of the set of values within each \sqrt{|D|} sized range, so we can prove against that. Also note that concretely in the eth2 implementation, “chunk roots” already are these sub-roots.
- Why is this better than the 2D erasure code scheme? Because the number of checks clients need to make is smaller, and the complexity is more encapsulated; fraud proof generation and verification is complex but it is a self-contained pure function, and otherwise the data is just a simple single-dimensional Merkle root. Also it is more compatible with upgrading to STARK-based Merkle roots in the future.

## Replies

**dankrad** (2019-12-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Second, we can require the checker to have a larger fraction of DD , eg. at least 12\frac{1}{2} , and then prove a probabilistic claim: q(x)q(x) matches p(x)p(x) on at least 40% of the sampled claims.

This has another security implication though, which is that despite initially choosing a Reed-Solomon code with a stopping ratio of 0.25, clients will have to assume that it is actually 0.5, to make sure that the fraud proof can always be constructed. I think at least in this specific instance, it makes the code efficiency as bad as the 2D code.

Here is a try to estimate how many queries we would need: Since we know the fraud prover has only about half the data, we are sending them n queries and allowing to pass on n/2, meaning that we have to compute the probability that they could provide n/2 of the data given the assumption that 40% of it is correct. The distribution of incorrect evaluations would be a B(n, p=0.4) binomial distribution, which we can roughly approximate with a normal distripution N(0.4n, \sigma=\sqrt{n \cdot p \cdot (1-p)}. We want to make the probability, if less than 0.4 of the data is correct, that they can provide n/2 evaluations, very small, say with security parameter 2^{-80}; that’s about 10\sigma in the normal distribution, so we need 10\sqrt{n \cdot p \cdot (1-p)}=0.1n or \sqrt n = 100 \sqrt{p (1-p)}, so ca. 2400 evaluations, does that sound right?

---

**vbuterin** (2019-12-10):

So here is another solution that could be much more favorable statistically. The prover commits to the entire set of indices in D that they know, and then the proof is done by randomly selecting only from that set. Both the p(x) vs q(x) equivalence check *and* the FRI check on q(x) would be restricted to samples from that set.

---

**dankrad** (2019-12-10):

Ah yes, that would lower the number of samples required. However, the rate efficiency problem would remain.

What controls the lower bound of the number of places that the fraud prover has to prove? It seems to me that anything >25\% would do, is that correct? So he could claim to have 30% of the data, and then use a evaluations to show that at least 25% (i.e. 83% of the 30%) of it is the same as the original D. That should be enough and lower the stopping rate to 30%. You can then arbitrarily push this as close to 25% as you like, at the cost of a few more evaluations.

Seems like this should actually work …

---

**dankrad** (2019-12-11):

Ah, one problem that I did not consider in the last post is that the fraud prover is faced with two difficulties:

- They may only be able to download some fraction of the data, because the prover did not upload all data
- Only some of the downloaded data may be on a low-degree polynomial, as the FRI commitment does not prove 100%

I’ll try to work through the numbers with that in mind, as I did not consider the second part of this above.

Setting security at \lambda = 2^{-80}: Let’s say the prover has to commit to the data with rate r=0.25 and with a FRI that proves f=90\% of the commited evaluations in D are on that polynomial. (This needs -\log(\lambda)/\log(f) \approx 526 FRI tests)

Let’s say the fraud prover wants to use the same rate f'=90\% for their fraud proof. That means they will need to have r/f' evaluations of the polynomial, which means they actually need r/(f'f) total data, as some of the data they download might not be on the polynomial. This means at this rate, the stopping rate would be r/(f'f) \approx 31\%.

If we instead set f=f'=80\% (approximately halving the proof sizes), the stopping rate will be approximately 39\%.

Both are a bit better than the 2D scheme.

Two more interesting problems I noticed:

1. How does the fraud prover effectively commit to a subset of the data, that is at the same time efficient to query. One possibility is to commit to a boolean vector using a Merkle tree. If we assume the fraud prover has 1/3 of the data, it will on average need three queries into that boolean vector per test to find an available piece of data, so that might add quite a bit to the proof. It would be interesting if instead, there is a way to commit to a map D \rightarrow D', where D' is the data available to the fraud prover, which is provably random.
2. A second interesting problem is given an oversampled polynomial interpolation with some errors, how to find the correct polynomial that interpolates most points in the sample. I would guess in the case of complex polynomials this could be done using FFT as it should still give an approximation despite the noise, but there is not really a notion of approximation in \mathbb{F}_p. It’s probably a solved problem but I would be interested in how it’s actually done.

---

**vbuterin** (2019-12-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> How does the fraud prover effectively commit to a subset of the data, that is at the same time efficient to query. One possibility is to commit to a boolean vector using a Merkle tree.

Ah, I was just thinking of a list of indices. Or would that be attackable because a prover could create a list that has a lot of duplicates and do mischief that way?

If we want to do a boolean vector, then one chunk in the vector would represent 256 data pieces, so if you hit a 0 you could just query sequentially until you find a 1. To deal with contiguous chunks of D being missing, you could use our index shuffling function to shuffle [1 ... |D|] and put the bits in that order.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> A second interesting problem is given an oversampled polynomial interpolation with some errors, how to find the correct polynomial that interpolates most points in the sample.

The algorithm I know about is the [Berlekamp-Welch algorithm](https://en.wikipedia.org/wiki/Berlekamp%E2%80%93Welch_algorithm) (the [article used to have](https://en.wikipedia.org/w/index.php?title=Berlekamp%E2%80%93Welch_algorithm&oldid=766993640#Example) a nice graphical example that I added ~7 years ago, but someone else edited the article and made it look like the usual run-of-the-mill terrible wikipedia math article again… ![:cry:](https://ethresear.ch/images/emoji/facebook_messenger/cry.png?v=12)). But this algorithm is O(n^3) so it would be fairly complex to run in practice. I know that [you can have an FFT-based algo](https://ethresear.ch/t/reed-solomon-erasure-code-recovery-in-n-log-2-n-time-with-ffts/3039) to correct for *known omissions*, but that’s a much easier problem…

---

**dankrad** (2019-12-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Ah, I was just thinking of a list of indices. Or would that be attackable because a prover could create a list that has a lot of duplicates and do mischief that way?

That is my intuition. As a minimum, you would probably have to prove that it is monotone or something like that, which sounds difficult.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The algorithm I know about is the Berlekamp-Welch algorithm (the article used to have a nice graphical example that I added ~7 years ago, but someone else edited the article and made it look like the usual run-of-the-mill terrible wikipedia math article again… ). But this algorithm is O(n3)O(n^3) so it would be fairly complex to run in practice. I know that you can have an FFT-based algo to correct for known omissions , but that’s a much easier problem…

It’s great that there is an algorithm, but it’s very likely that O(n^3) will be too slow to solve our problem. Especially since we have to generate fraud proofs quickly, and we have large amounts of data. Sounds like an additional research problem required to be solved to use FRIs in this way.

---

**denett** (2019-12-11):

I don’t think it is necessary for the clients to ask for the full middle level of the merkle tree.

The middle level could also be expanded using Reed-Solomon and the clients could sample this expansion as well.

When this sampling is combined with the other sampling, this will cost only one extra hash per sample.

The checker needs to reconstruct the middle level and checks to see if the upper part of the merkle tree is correct.

If it is correct, the checker could build a proof showing that a sub-branch is incorrect as you described.

Otherwise the checker can construct a proof that the upper part is not correct. The upper part is of the same size as a sub-branch so the proof will be of similar size.

Because the sampling of a middle level is relatively cheap, we can choose to expand and sample every level. Then we only need to proof a subbranch with two nodes.

---

**vbuterin** (2019-12-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> The middle level could also be expanded using Reed-Solomon and the clients could sample this expansion as well.

This is true. Taking this approach to the extreme you basically get [coded Merkle trees](https://arxiv.org/abs/1910.01247). It’s a reasonable approach, though I personally feel like the difference between 40 * log(n) and sqrt(n) is small enough that the gains are not worth the complexity. Particularly note that if you’re willing to have fraud proofs be bigger than the sampling size (which is a good tradeoff as fraud proofs are going to be rare) then you can sample a layer slightly above the middle layer, eg. get n^{0.4} sized sampling and n^{0.6} sized fraud proofs.

For eg. 32 MB (2^{20} chunks), 40 samples would be 40 * log_2(2^{20} \div 40) = 587 chunks, whereas the sqrt layer would be 1024 chunks, and a n^{0.4} layer would be 256 chunks.

---

**denett** (2019-12-11):

If the block creator just fills the expansion with random data, it will be impossible to find enough (>25%) points and the checker cannot build a fraud proof. Or am I missing something?

As an alternative, the clients could do the FRI sampling them self. When done in a certain way (as I tried to explain [here](https://ethresear.ch/t/stark-proving-low-degree-ness-of-a-data-availability-root-some-analysis/6214/6)), it is guaranteed that the values that are sampled are on the same polynomial.

---

**dankrad** (2019-12-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> If the block creator just fills the expansion with random data, it will be impossible to find enough (>25%) points and the checker cannot build a fraud proof. Or am I missing something?

I think this construction actually needs two FRIs, one to show that the original erasure coding is “almost correct”, and then potentially one for a fraud proof. If they do this, they will not be able to create the original FRI, which requires a high percentage of the points to be on a low degree polynomial.

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> As an alternative, the clients could do the FRI sampling them self. When done in a certain way (as I tried to explain here), it is guaranteed that the values that are sampled are on the same polynomial.

Aha, now this is a very interesting idea! Sorry I missed it the first time. So if we do this, we have to do a little bit of extra work when downloading an element by also downloading the FRI path. However, we can probably do this very intelligently by “injecting” those elements required into the Merkle tree. For example, f(z) and f(-z) could be sibling leaves, so getting f(-z) comes at no extra cost. Then if w^2=-z^2, we would make those f(w) and f(-w) a sibling of the node that contains (f(z), f(-z), and at this level mix in the values f(z^2) and f(-z^2).

The Merkle tree would be twice as deep, but it would come with relatively cheap full authentication of the elements lying on a low degree polynomial. Very cool!

Since this scheme would have no difference between coding rate and stopping rate, it may well be the most efficient at the moment (apart from the STARK one, which might not be feasible at this point after all).

---

**dankrad** (2019-12-17):

It seems from some discussions I had that you cannot put all FRI layers into one Merkle tree, as each layer needs to be computed (Fiat-Shamir) from the previous layer.

However, I still quite like the idea of combining data availability checks with spot checks on the FRI layers. It will not save us from having to do FRI for fraud proofs when parts of the data are just not available. But it does improve the construction because we need to accommodate for a smaller buffer to construct that fraud proof, as we don’t need to consider that some of the downloaded data may be incorrect. For example, for a FRI rate of 0.8 and an erasure code rate of 0.25, the original construction would get a stopping rate of 0.25/0.8^2 \approx 0.39, whereas by doing spot checks with data availability checks we get to 0.25/0.8 \approx 0.31.

---

**denett** (2019-12-18):

Yes, we still need extra merkle branches for the FRI, but the described method is quite efficient, because the column merkle branch and the next row merkle branch can be combined.

I expect the size of the samples to increase by a factor of 5 or 6 compared to just sampling a single merkle branch.

---

**dankrad** (2019-12-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> One approach would be to use this technique as our evaluation proving scheme directly instead of Merkle proofs. But the problem here is that FRI proofs are big (~20 kB for big inputs) and take linear time to produce. So what we will do instead is use FRI as a fraud proof .

For the record I would want to correct this: I think this approach need a FRI *both* for the initial proof of closeness *and* as a fraud proof. Otherwise, the producer can just commit to a totally random D and nobody would have a chance to make a valid FRI fraud proof out of it (at least not a short one).

I also have a feeling that the FRI proofs we are talking about are going to be much bigger: My estimate (worst case) is that a polynomial would need 2^{27} evaluations (at rate 0.25), which means a Merkle tree of depth 26. So that means each FRI spot check needs 2\cdot 25 field elements plus 27 \cdot 26 /2 = 351 hashes for Merkle proofs. That’s already around 13 kb for one spot check, and to get to 80\% correctness you using my naïve estimate you would need -128 \frac{\log2}{\log 0.8} \approx 400 evaluations (does someone know the correct way to approximate this?)

So it would appear that this FRI is already 5 MB in size. Am I wildly off here?

---

**denett** (2019-12-19):

My estimate for a FRI without special optimizations: A block of  32MB = 2^{20} chunks of 32 bytes, expanded is 2^{22} chunks. A merkle branch for 4 chunks is 20 hashes plus 4 values.

To get the first row is 24 chunks, to get the column and the next row is 22 chunks. So for one spot check we need 24+22+..+4 = 154 chunks. A light client doing 40 spot checks needs to download 192.5kb plus 64kb(for the middle layer) which is 0.78% of the 32MB.

Instead of doing a new FRI for the fraud proof, would it not be sufficient to proof that a subset of \sqrt{|D|} nodes that do not match the merkle tree, actually do match the FRI used for the sampling?

For that we only need the full FRI layer of \sqrt{|D|} size. Because the FRI roots are known we already know all the columns that are chosen during the FRI. So to verify the fraud proof, the \sqrt{|D|} values can be combined using the first column to \sqrt{|D|}/4 values in the next layer. We can continue doing this until we have a single value that can be checked at the committed FRI layer.

So if we let the light-clients download an extra 64kb for the FRI layer, the fraud proof can be around 64kb as well.

**EDIT:** This fraud proof does not work, because it will be easy to build a fake fraud proof.

---

**dankrad** (2019-12-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> A block of 32MB = 2202^{20} chunks of 32 bytes, expanded is 2222^{22} chunks. A merkle branch for 4 chunks is 20 hashes plus 4 values.
> To get the first row is 24 chunks, to get the column and the next row is 22 chunks. So for one spot check we need 24+22+…+4=15424+22+…+4 = 154 chunks. A light client doing 40 spot checks needs to download 192.5kb plus 64kb(for the middle layer) which is 0.78% of the 32MB.

Need to also consider the worst case which is 2^{26} chunks.

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> EDIT: This fraud proof does not work, because it will be easy to build a fake fraud proof.

Can you say why that is? Because it seems like an elegant idea.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> So it would appear that this FRI is already 5 MB in size. Am I wildly off here?

It seems that this is in the right ballpark. So that would make it impractical for fraud proofs. The main problem is that we want to do a FRI at a very high correctness rate, which is expensive. If we instead lower this rate to only 50\% correct, then our proof will be several times smaller. However, we will need to lower the rate to 0.125 then (because we need to make sure that the fraud prover has twice as many correct elements as needed in order to create the FRI; in addition, he needs twice as many since half of them could be incorrect, so at a rate 0.125 the stopping rate would be 0.5).

Then we would need about -128 \frac{\log 2}{\log 0.5} = 128 evaluations, bringing us to ca. 1.6 MB proof size (or 1 MB at security 80 bits).

However, we bought this at the expense of having a stopping rate that’s q=4r (r being the coding rate). For r=0.125 that’s actually worse that the 2D scheme (which would achieve a stopping rate of ca \sqrt r \approx 0.35). Also the fraud proofs in the 2D scheme would only be 370 kb and thus smaller.

---

**denett** (2019-12-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Need to also consider the worst case which is 2^{26} chunks.

Why is the worst case 2^{26}?

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Can you say why that is? Because it seems like an elegant idea.

FRI is based on the premise that for two lines to intersect at a randomly chosen point, you got either very lucky or the two lines are the same. This does not hold if the point is known in advance. That is why we need Fiat-Shamir at every level of the FRI.

We could still use the trick to roll up the \sqrt{|D|} sized subset to a single value in the fraud proof, but then it needs to be a new FRI where the first column is chosen based on the merkle root of this subset.

Then we use this new FRI to show that more than 25% of the total merkle branches are on the same polynomial as the subset.

If the checker collected 50% of the samples, he can commit using a merkle tree to the 50% of the samples that are missing. So when during the FRI sampling a missing branch is selected, this can be proven via a merkle branch. The resulting FRI has a expansion rate of 2, so for 80 bits of security we will need 80 FRI samples. This means the total proof will be around 450kB. Increasing the original expansion rate will off course decrease this size significantly.

---

**denett** (2019-12-22):

I was wondering, why is it necessary for the light-clients to get 80 bits security on the data availability sampling? Isn’t that a false sense of security, because the bigger risk seems to be that you are one of the few clients that get served the correct samples.

Besides, the main strength of the data availability sampling seems to be that it is impossible to convince a large part of the validators that unavailable data is available. So an unavailable block will never be finalized.

---

**vbuterin** (2019-12-22):

I think 30 bits of security on data availability sampling should be fine.

---

**dankrad** (2019-12-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> I was wondering, why is it necessary for the light-clients to get 80 bits security on the data availability sampling?

I think for the sampling, much lower security is ok. But for the correctness of encoding, I would go for 128 bits if possible (to be consistent with the rest of the protocol) or 100 as a compromise (assuming that FRIs are a billion times harder to compute than simple things like hashes). I’m very critical of anything that’s only 80 bits security.

---

**dlubarov** (2019-12-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> FRI is based on the premise that for two lines to intersect at a randomly chosen point, you got either very lucky or the two lines are the same. This does not hold if the point is known in advance. That is why we need Fiat-Shamir at every level of the FRI.

Are you sure that’s needed? If we do Fiat-Shamir only on f^{(0)}, then throughout the commit phase the prover can predict where an interpolated polynomial will be evaluated, but they can’t predict which chunk of 2^η points will be interpolated. So it doesn’t seem obvious to me that soundness would break down. Wouldn’t each invalid “coset reduction” (from 2^η points in f^{(i)} to a point in f^{(i + 1)}) still have a certain probability of being detected?


*(4 more replies not shown)*
