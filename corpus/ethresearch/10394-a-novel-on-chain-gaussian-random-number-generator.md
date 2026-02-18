---
source: ethresearch
topic_id: 10394
title: A novel on-chain Gaussian random number generator
author: maxareo
date: "2021-08-22"
category: Uncategorized
tags: [random-number-generator]
url: https://ethresear.ch/t/a-novel-on-chain-gaussian-random-number-generator/10394
views: 3758
likes: 3
posts_count: 14
---

# A novel on-chain Gaussian random number generator

## Abstract

Currently, randomness, be it on-chain or off-chain, is only uniform. Gaussian randomness is made available by simply counting 1’s in the binary representation of a hashed value calculated by the `keccak256` hashing algorithm. It is simple, costs little gas, and can open up many possibilities in gaming and DeFi.

## Motivation

DApps may desire to generate some numbers more frequently than the others, but currently, the randomness produced by `keccak256` hashing algorithm is uniform in the domain `[0, 2**256-1]`. That is limiting what is possible with Solidity and blockchains. This on-chain Gaussian RNG can satisfy such needs.

## Specification

The algorithm relies on the count of 1’s in the binary representation of a hashed value produced by the `keccak256` hashing algorithm. By Lyapunov Central Limit Theorem, this count after proper transformations, has a Gaussian distribution. The theoretical basis, condition and proofs as well as Solidity implementation and practical issues can be found [here](https://github.com/simontianx/OnChainRNG/tree/main/GaussianRNG).

## Backwards Compatibility

This is a brand new algorithm and there is no backwards compatibility issue. Actually, it is already with Solidity and it got a chance to come to light.

## Replies

**adompeldorius** (2021-08-23):

You could also apply the [quantile function](https://en.wikipedia.org/wiki/Quantile_function) of a probability distribution to the uniformly distributed value in order to get a variable with the specified distribution.

---

**maxareo** (2021-08-23):

Inverse CDF is a common tool in generating random numbers, however, it would be challenging to express it and apply it on-chain cheaply.

---

**adompeldorius** (2021-08-24):

I see. Do you have gas estimates? It could be interesting to compare the gas usage of this method to other methods such as the [Ziggurat](https://en.m.wikipedia.org/wiki/Ziggurat_algorithm) algorithm. I have a feeling that the Ziggurat could perhaps be more efficient, especially if many samples are computed, since each sample could consume just a small part of the hashed value, so you would need fewer hashings.

---

**maxareo** (2021-08-24):

Feel free to run the smart contract in the repo.

Many algorithms that are working in the traditional setup do not necessarily work in Solidity or on a blockchain. I do not think Ziggurat algorithm or alike can be implemented in Solidity at this point, when floating numbers are not even supported yet.

The algorithm I am proposing does not run with floating numbers or sophisticated mathematical calculations, instead simple counting is sufficient to generate Gaussian randomness.

Given the limitations imposed by Solidity and blockchain, this is a non-trivial step forward.

---

**adompeldorius** (2021-08-24):

I don’t think floating point calculations are actually needed for the Ziggurat if you use the same scaling trick as in your algorithm.

I agree that your solution is simple, but I’m not quite convinced that it is more gas efficient than the Ziggurat, although I might be wrong. One drawback of Ziggurat is the need for a lookup table, which could perhaps outweigh the gas savings on computations.

The advantage of using an algorithm like Ziggurat however, is that it could be used for more distributions, while it is harder to see how your algorithm generalises. If the Ziggurat turned out to also be more gas efficient, it would be a win win.

I’m not trying to nullify your work, just trying to give some constructive feedback and possible alternatives.

---

**maxareo** (2021-08-24):

Unfortunately, the Gaussian pdf is not available to do any rejection sampling including Ziggurat in the first place. It would be great if someone can make it available on-chain, and that can definitely open up new possibilities.

When tens of token standards are designed for very specific needs, the idea of finding any generalization seems unrealistic if not impossible at all.

---

**adompeldorius** (2021-08-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxareo/48/7553_2.png) maxareo:

> Unfortunately, the Gaussian pdf is not available to do any rejection sampling including Ziggurat in the first place.

Yeah, I see. You would need to find a way to approximate the pdf using integer arithmetic, which would be tricky, but perhaps not impossible. The devil lies in the details.

---

**maxareo** (2021-09-04):

Talking about generalization, this method can do well in generating RNGs for a few discrete distributions such as Bernoulli, Binomial, Negative Binomial, Poisson with a small parameter, and Geometric distributions. Continuous distributions are not possible to be generated with this methodology. Gaussian distribution, however, happens to be a special case since it can be approximated by discrete distributions.

---

**Aurelien-Pelissier** (2022-03-01):

That’s actually a very cheap way to generate normally distributed random numbers. With the only limitation that the discretization will be limited to 256 values. (since uint256 have 256 bits). If you want to have more, you can “sum” several gaussians.

---

**Aurelien-Pelissier** (2022-03-01):

https://coinsbench.com/arbitrarily-distributed-on-chain-random-numbers-9a3f54656fd

You can also check that article, who explain how to generate different distributions with any variance, mean, etc.

---

**maxareo** (2022-03-01):

Nice article. Great work in expanding the use cases of on-chain Gaussian randoness. The next step would be to build an DApp with these random numbers.

---

**bowaggoner** (2022-03-04):

Agree, this is nice. Adding some challenges in the random number space.

(a) An annoying fact is that one can’t easily use bits to generate a precisely uniform random integer in Uniform{1…n}, unless n is a power of two. The standard approach is rejection sampling, but that could be wasteful. Is there a better way, e.g. something more like arithmetic coding?

(b) One innovation would be to get several random numbers out of a single 256-bit hash, depending on how much accuracy is needed. Of course you can extract e.g. eight Uniform{0…31} variables just by looking at the bits in chunks of 32 at a time. More interesting, you can get an unspecified number of exponential random variables. One exponential distribution is X=0 w.prob. 1/2, X=1 w.prob. 1/4, …, X=k w.prob. 1/2^{k+1}. In this case, every run of bits in the hash gives you another independent exponential variable equal to the length of the run minus one. For example, the hash 10001101111... gives the sequence of iid exponential variables 0,2,1,0,3.... Discard the last one though.

(I’m assuming the bitwise operations to extract these are cheaper than just getting fresh randomness, but maybe that’s wrong?)

(c) Another important use of randomness is to shuffle a list. Fisher-Yates shuffles a list of length n using draws from Uniform{1…n}, Uniform{1…n-1}, …, Uniform{1,2}. This looks optimal to me, since it’s equivalent to drawing a number uniformly from 1 to n!, the number of possible shuffles. Is there a more efficient way to implement it than generating all of these random numbers separately?

---

**maxareo** (2022-04-08):

[@adompeldorius](/u/adompeldorius) [@bowaggoner](/u/bowaggoner) [@Aurelien-Pelissier](/u/aurelien-pelissier)

There is a potential application of this RNG in a EIP [here](https://ethereum-magicians.org/t/eip-quantum-nft-standard/8852?u=maxareo).

In a nut shell, Gaussian randomness, differing from uniform randomness, can provide a unique central tendency which could find interesting applications in this Quantum NFT Standard. Check it out and feel free to leave comments.

