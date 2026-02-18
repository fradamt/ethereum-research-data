---
source: ethresearch
topic_id: 8052
title: Stark-based VDFs
author: khovratovich
date: "2020-09-30"
category: Cryptography
tags: []
url: https://ethresear.ch/t/stark-based-vdfs/8052
views: 2322
likes: 2
posts_count: 2
---

# Stark-based VDFs

This is a follow-up to [an earlier research post](https://ethresear.ch/t/hash-based-vdfs-mimc-and-starks/2337/6).

For Eth 2.0 we need a VDF F(x)=y so that

- there exists a succinct proof \pi(x,y) that can be found only for x,y as above.
- there exists a lower bound on the latency of F and \pi, which can be matched closely on existing hardware.

The current plan is to use an [RSA-based VDF](https://eprint.iacr.org/2018/623)  where F=g^{2^t}\bmod{N} is a sequence of t squarings modulo an RSA modulus N with unknown factorization. The proof \pi is constant size, and can be computed in O(t/\log t) time. In practice computing \pi can be parallelized to make its latency be negligible compared to the actual computation of y.

There is an STARK-based construction alternative to an [RSA-based VDF](https://eprint.iacr.org/2018/623).  It works as follows:

- The VDF function F is a MiMC-like construction whose iterations are represented as low-degree polynomials. Our round function is
(X,Y) \leftarrow ((X+Y)^{(p-1)/3},2Y);

where X,Y  are n>64-bit elements of some field F_p. Note that the doubling of Y is crucial; otherwise [precomputation attacks](https://en.wikipedia.org/wiki/Time/memory/data_tradeoff_attack#Hellman's_tradeoff_attack_on_block_ciphers_%5B1%5D) allow to invert a VDF with a little amortized cost.

- An alternative VeeDo by StarkWare doesalike

(X,Y) \leftarrow (X^{1/3},Y^{1/3})
- (X,Y) \leftarrow M\cdot (X,Y) +C_r,
where  M is a matrix and C_r are round constants.  It seems to be more expensive to compute with the same latency.

The proof is a STARK proof of correctness that y=F(x) where x and y are public inputs. The STARK prover benefits from the fact that F is invertible and has low degree (3) in the reverse direction, which makes the prover efficient.

The obvious benefit of STARK-based VDS is that its prover is post-quantum and does not need a trusted setup. However, the disadvantage is that the prover is  more expensive compared to the RSA prover, i.e. makes O(t\log^a t) operations compared to O(t/\log t) of the RSA one. As a result, the prover running time becomes the dominant term in a VDF run, and, given it is parallelizable, the VDF latency becomes more volatile and we may miss the second requirement to a good VDF.

We thus face the following questions:

1. Do we  have to extend the construction for bigger state/smaller field to further increase the precomputation protection ?
2. Is the resulting VDF fully post-quantum, i.e. is F secure as a post-quantum hash? Do precomputation attacks have quantum speed up beyond Grover’s  search algorithm with square-root complexity?
3. Should we consider a VDF proof as a part of the VDF output formally, work with only a single latency parameter and optimize it alone?
4. What would the minimal hardware that would make the prover latency close to the lower bound? Is it much bigger than that for RSA?

## Replies

**khovratovich** (2020-10-01):

Apparently the quantum complexity of function inversion has been investigated in [several](https://arxiv.org/abs/1911.09176) [works](https://eprint.iacr.org/2019/1093). Most recently [it turned out](https://arxiv.org/pdf/2006.05650.pdf) that the time T and memory S complexity of a quantum invertor  are lower bounded by inequation

ST+T^2 > N

which for S<\sqrt{N} equals Grover, and for bigger S we can only hope for N/S time (but no algorithm exists). Therefore the best quantum adversary on a 128-bit function is either 2^{64}-Grover or a 2^{n<64} time, 2^{128-n} space hypothetical attack.

