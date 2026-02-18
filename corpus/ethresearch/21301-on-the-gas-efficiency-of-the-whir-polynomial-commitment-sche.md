---
source: ethresearch
topic_id: 21301
title: On the gas efficiency of the WHIR polynomial commitment scheme
author: Pierre
date: "2024-12-19"
category: Cryptography
tags: []
url: https://ethresear.ch/t/on-the-gas-efficiency-of-the-whir-polynomial-commitment-scheme/21301
views: 843
likes: 13
posts_count: 5
---

# On the gas efficiency of the WHIR polynomial commitment scheme

# On the gas efficiency of the WHIR polynomial commitment scheme

Joint post with [@WizardOfMenlo](/u/wizardofmenlo)

*TLDR; We developed an [open-sourced and MIT licensed](https://github.com/privacy-scaling-explorations/sol-whir) prototype EVM verifier for the [WHIR](https://eprint.iacr.org/2024/1586) polynomial commitment scheme (PCS). For a multivariate polynomial of 22 variables and 100 bits of security, verification costs are 1.9m gas. With a more aggressive parameter setting, we reach even lower costs, below the 1.5m gas mark. This makes WHIR a serious post-quantum PCS candidate for teams using or looking to leverage STARKs in production.*

### WHIR

WHIR is a multilinear PCS requiring only a transparent setup and guaranteeing post-quantum security, while achieving high verification speeds. We wanted to estimate how high verification speed would translate in terms of gas usage, when verifying WHIR proofs on the EVM. To this end, we developed a prototype WHIR verifier and benchmarked it at various parameters levels.

Our prototype implementation supports various settings, with a folding factor of at most 4 - this is an implementation idiosyncrasy stemming from gas optimizations and can be easily modified. While we present results for a specific set of parameters, our verifier is [open-sourced and MIT-licensed](https://github.com/privacy-scaling-explorations/sol-whir), letting anyone test it with different configuration requirements.

### Gas saving strategies

WHIR is equipped with a variety of parameters and lets users choose how much work the prover should carry out in the benefit of the verifier. We quickly review here four important ones:

1. The chosen code rate \rho will impact the argument size and hence verifier time, at the expense of prover time. In concrete terms, with WHIR, the number of queries (i.e. requests for evaluations of a polynomial) a verifier makes tends to 0 as \rho approaches 0. This means that each saved query translates into saved gas costs.
2. The folding factor k determines the number of rounds between the prover and verifier. A higher k means fewer rounds, but additional prover work.
3. The amount of proof of work grinding[1] lets the verifier decrease the number of authentication paths it will demand from the prover. Higher grinding levels translates into reducing both calldata and verifier execution costs.
4. We can also tune WHIR’s security parameter \lambda directly. In practice, this means that higher \lambda values will result in increased verifier queries and gas costs.

Independently from WHIR, one final technique we can leverage is masking. It allows to save calldata by masking the output of the last bytes of the merkle tree hash function[[2]](#footnote-51861-2). For the sake of completeness, we included an implementation of this verifier working with a (naive) version of this industry-standard technique. We recall that masking is specifically beneficial when achieving \lambda \le 128, as to get to a \lambda security level, we need our hash function digest size to be at most 2*\lambda.

### Results

In this work, we show how the WHIR verifier performs with different starting rates \rho, folding factors k, and \lambda bits of security, for randomly sampled polynomials of 16, 20 and 22 variables and instantiated with the capacity bound conjecture. We will plot how each of those parameters impact gas costs relative to the chosen level of pow grinding and show how to reach low gas costs when using WHIR.

We chose our experiment parameters to be in line with what we consider to be useful levels of practicality and security. Our gas results are obtained from computing an average transaction gas cost using [foundry](https://github.com/foundry-rs/foundry) forge and anvil at version 0.2.0 - [commit e10ab3d](https://github.com/foundry-rs/foundry/commit/e10ab3d7010b2cbe2b76030d6638c49a3cec696d).

#### Setting \rho

We start with adjusting for the code rate and plot the impact of the chosen rate on the verifier’s gas usage. We can see the impact of choosing the correct starting code rate \rho is quite large. For 20 variables and pow grinding at 30 bits, we can cut gas costs in half when going from \rho=2^{-1} to \rho=2^{-6}. Hence, for the rest of our experiment, we set a code rate \rho=2^{-6}. Also, we omitted for the sake of clarity results for polynomials with 22 variables. We will now start to plot results for it as well.

[![whir-rho](https://ethresear.ch/uploads/default/original/3X/f/b/fb704007ff8c87ccc06e7e8f8e919a7d365e3976.png)whir-rho600×400 6.61 KB](https://ethresear.ch/uploads/default/fb704007ff8c87ccc06e7e8f8e919a7d365e3976)

#### Setting k

Our next parameter of interest will be the folding factor k. In the case where we have a polynomial composed of 22 variables and pow grinding set to 30 bits, we end up with a x1.75 increase in gas costs when using a lower folding factor k=2 instead of k=4. Hence, we will now set k=4.

[![whir-k](https://ethresear.ch/uploads/default/original/3X/4/c/4c1f40db6915930afdebfe34dfcc1abba9663536.png)whir-k600×400 12.6 KB](https://ethresear.ch/uploads/default/4c1f40db6915930afdebfe34dfcc1abba9663536)

#### Setting \lambda

Next, we tune our \lambda parameter to a more aggressive level of security. We plot how setting \lambda=80 further decreases our gas costs. Clearly, removing 20 bits of security results in large additional savings. In the case of 22 variables and 30 bits of grinding, each removed bit of security translates into more than 10k of saved gas.

[![whir-lambda](https://ethresear.ch/uploads/default/original/3X/4/8/4820aea1dc4d7ae430efd9dc49dec64d59cac127.png)whir-lambda600×400 7.62 KB](https://ethresear.ch/uploads/default/4820aea1dc4d7ae430efd9dc49dec64d59cac127)

#### Masking

Finally, we apply a naive masking strategy for our calldata. Since we set \lambda = 80, we mask commitments to 160 bits - [a similar level to what starkware runs (or has been running) its verifier](https://github.com/starkware-libs/starkex-contracts/blob/aecf37f2278b2df233edd13b686d0aa9462ada02/evm-verifier/solidity/contracts/MerkleVerifier.sol#L7). Combined with \rho=6, k=4, we get to our final and rather competitive gas costs for our WHIR verifier:

- For 16 variables, our naive implementation of this strategy saves us an average additional 25k gas. We end with an average total gas cost of 1091720 gas, just above the 1m mark.
- In the case where our multivariate  polynomials are of size 20 and 22, we can save an additional ~35k gas. We end up with average total gas costs of respectively 1388230 and 1493552 gas, below the 1.5m gas mark.

For comparison, verifying groth16 and fflonk proofs costs around 300k gas today. However, WHIR is transparent and post-quantum. Such gas costs illustrate why we think WHIR is a pretty good option when not only compared to protocols with similar assumptions like FRI, but also to trusted setup based ones.

### Future directions

First, we developed a *prototype* verifier. We are confident that additional optimizations lie ahead. One of the low hanging fruit being that there still are parts of our code that would benefit from assembly re-writes.

For 22 variables, with \lambda=80, \rho=1/2^6, k=4, 30 bits of grinding and masking, our average gas cost is almost 1.5m gas. However, we expect a total optimized gas cost averaging around 1.2m-1.3m gas. Indeed, our current (average) costs breakdown consists into roughly: 700k gas for calldata, 250k gas for merkle proving, 80k gas for computing STIR challenges, 65k gas for the sumcheck iterations, 60k gas for fiat shamir utilities (pop from transcript, pow checking, ..) and 25k gas for various uni/multivariate evaluations. Hence, we estimate remaining glue code (paid in memory expansions, overheads from using abstractions, ..) to take around 300k - 250k gas, which an assembly rewrite would help reduce.

Also, our implementation of masking has been somewhat naive, as it simply consisted into zeroing the last 12 bytes of our  merkle decommitments. We would be happy to integrate an [improved version](https://github.com/privacy-scaling-explorations/sol-whir/issues/5) of this masking strategy to not pay anything for masked values. On a related front, we carried out a bespoke multi merkle proof assembly implementation hailing from [Recmo’s initial solidity version](https://gist.github.com/Recmo/0dbbaa26c051bea517cd3a8f1de3560a). Multi-merkle proofs make up for ~20% of gas costs of the verifier. We would be happy to see further algorithmic improvements here as we suspect our version to be far from perfect.

Finally, WHIR isn’t limited to a particular field. We would be curious to see how those numbers fare in the context of different, smaller fields. In particular, we expect our field operations to bear less gas costs compared to when working with the BN254 scalar field.

### Acknowledgements

Thanks to [@alxkzmn](/u/alxkzmn) for helping with the merkle and pow modules in an early version of this work.

1. For a primer on grinding, see section 3.11.3 of the ethSTARK paper. ↩︎
2. Gas savings obtained from this approach might be subject to change in the future, see EIP 7623. ↩︎

## Replies

**alinush** (2024-12-19):

Very exciting!

Which conjecture are the verification gas numbers for?

[![Screenshot 2024-12-19 at 8.24.13 AM](https://ethresear.ch/uploads/default/optimized/3X/b/e/be8b5b16d27e822dc95cc7901d9f16fb2a1a7fd1_2_690x147.png)Screenshot 2024-12-19 at 8.24.13 AM2192×468 139 KB](https://ethresear.ch/uploads/default/be8b5b16d27e822dc95cc7901d9f16fb2a1a7fd1)

---

**Pierre** (2024-12-20):

Thanks!

Good question, I will edit the post with this info. Those numbers are obtained using the \textit{Capacity Bound} conjecture.

---

**alinush** (2024-12-20):

I see. My (limited) understanding is that the capacity bound is a theoretical optimum that is not achieved for Reed-Solomon?

---

**WizardOfMenlo** (2024-12-20):

Yes, currently we know that Reed-Solomon codes have proximity gaps and list-decoding up to the Johnson bound. There is some reason to believe that in fact RS codes are list-decodable up to capacity (for example, we know that random puncturing of RS codes are decodable up to capacity), and we suspect that they also have proximity gaps up to capacity, but proving it is a hard and exciting open question.

It is called capacity bound because we know that for distances larger than that the list-size actually grows exponentially (and so we can’t really hope to have good list-decoding). See arxiv org 2304.09445 for some background.

