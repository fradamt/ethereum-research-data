---
source: ethresearch
topic_id: 11588
title: Leveraging SNARK proof aggregation to achieve large scale PBFT-based consensus
author: jieyilong
date: "2021-12-25"
category: zk-s[nt]arks
tags: [zk-roll-up, layer-2]
url: https://ethresear.ch/t/leveraging-snark-proof-aggregation-to-achieve-large-scale-pbft-based-consensus/11588
views: 3603
likes: 9
posts_count: 9
---

# Leveraging SNARK proof aggregation to achieve large scale PBFT-based consensus

PBFT-based consensus protocols provide some good properties such as fast finality over chain-based protocols (e.g. Bitcoin, Cardano Ouroboros), but they typically don’t scale well with the number of nodes participating in the consensus. This is because PBFT-based protocols require all-to-all votings to reach consensus (unless probabilistic tricks like Algorand-style committee sampling is in use). Even with latest proposals like HotStuff which avoids the complexity in view changes, each consensus decision still requires O(N^2) voting messages flowing through the network, where N is the number of nodes. Imagine a system with 100k nodes, in each of the consensus voting phases, every node has to receive and process 100k voting messages from other nodes. This could overwhelm the network, and thus limit the number of participants in PBFT-based protocols. This makes PBFT-based protocols less decentralized compared to chain-based protocols.

To address this bottleneck, we propose to leverage SNARK proof aggregation to reduce the amount of voting messages. Recently, [@vbuterin](/u/vbuterin) wrote a [nice introduction](https://vitalik.ca/general/2021/11/05/halo.html) to SNARK proof aggregation/merging.

The basic idea is to use SNARK aggregation in a way similar to signature aggregation, so that an aggregated SNARK can compactly encode which nodes have voted for a block. For simplicity, let us assume the network has a fixed number of N nodes. Assume a new block has just been proposed, and the i^{th} node n_i wants to vote for the block. It does the following:

- First generate a SNARK proof \pi_i representing his yes vote (basically it just needs to create a SNARK proof \pi_i for his signature \sigma = sign_{sk}(h), where h is the hash of the new block).
- Broadcast the SNARK proof \pi_i, and an index vector v_i to all its neighbors. The index vector is an N dimensional boolean vector that encodes which nodes have provided SNARK proofs for their yes votes. Initially, v_i = (0,0, ..., 1..,0), i.e., all but the i^{th} element are zeros, since only node n_i has provided the proof for its yes vote.

Meanwhile, Node n_i keeps aggregating the proof and index vector and then broadcast them out to all neighbors:

- Upon receiving (\pi_j, v_j) from its neighbor n_j, it first verifies the validity of the proof verify(\pi_j, v_j) == true. If so, it updates its local proof and index vector by \pi_i = Aggregate(\pi_i, v_i, \pi_j, v_j), v_i = v_i OR v_j. Here OR is the element-wise boolean “or” operator. The node stops doing aggregation when the number of "1"s in v_i is over a certain threshold, e.g. \frac{2}{3}N.
- Node n_i maintains a local timer. Whenever the timer is triggered (e.g. once every 100ms), node n_i broadcasts out the latest \pi_i and v_i. Note that in the first few rounds, most of the elements of v_i are zero, so data compress can be applied to effectively reduce the message size.

The readers might wonder why we don’t just use signature aggregation. The issue there is that signature aggregation typically requires v_i and v_j to be disjoint, i.e., the same element (e.g. the k^{th} element) cannot be 1 in both vectors. SNARK aggregation overcomes this restriction.

It can be shown that in a gossip network with relatively good connectivity, only O(logN) broadcasting rounds are required for the above voting process to converge (similar to how a gossiped message can propagated through the network in O(logN) time). Moreover, since a gossip network has O(N) number of edges, the total number of voting messages is O(NlogN), which scales much better as N grows. The above process also has good tolerance to Byzantine nodes, since Byzantine nodes cannot forge fake proofs.

Is this a viable approach? Feedback and comments are appreciated!

## Replies

**levs57** (2021-12-26):

Important point is that you will need to make these snarks uniform in some way, i.e. you will have “level k” proof, which attests that there exist a pair of proofs of level k-1. This level structure can be made to have logarithmic size.

I think it definitely should work, question is can not you do better with just signature aggregation and keeping “small” vectors (say, if there is signature which corresponds to the voters A, B, and another to the voters B, C, then you aggregate them to the signature A+2B+C). Of course it is a tradeoff, because instead of a boolean vector you juggle a bit more information, but it could be possible that this is more efficient.

---

**SebastianElvis** (2021-12-27):

There is a paper https://eprint.iacr.org/2021/005.pdf exploring a similar approach to reduce the communication complexity of DKG. When the gossip network is well-formed, the communication complexity can indeed be reduced to O(n \log{n}). The downside, as indicated by your analysis and the paper’s analysis, is the round complexity of O(\log{n}). A specialised data structure that is aggregatable and SNARK-free (more efficient)  is also of interest.

---

**Pratyush** (2021-12-27):

A similar idea is explored in this work, but for a different problem (BA, instead of BFT): [Cryptology ePrint Archive: Report 2020/130 - Breaking the $O(\sqrt n)$-Bit Barrier: Byzantine Agreement with Polylog Bits Per Party](https://eprint.iacr.org/2020/130)

Note that generation and verification for SNARK proofs is much slower than for signatures, so this would require a few optimizations before it becomes efficient enough for practice

---

**jieyilong** (2022-01-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/levs57/48/7254_2.png) levs57:

> Important point is that you will need to make these snarks uniform in some way, i.e. you will have “level k” proof, which attests that there exist a pair of proofs of level k-1. This level structure can be made to have logarithmic size.

Thanks for the suggestion! By “levels” do you mean to make a tree-like network for SNARK proof aggregation? Or “level k proof” simply means the SNARK proof generated in the k-th round of gossip?

![](https://ethresear.ch/user_avatar/ethresear.ch/levs57/48/7254_2.png) levs57:

> I think it definitely should work, question is can not you do better with just signature aggregation and keeping “small” vectors (say, if there is signature which corresponds to the voters A, B, and another to the voters B, C, then you aggregate them to the signature A+2B+C). Of course it is a tradeoff, because instead of a boolean vector you juggle a bit more information, but it could be possible that this is more efficient.

Yeah very good points! We actually [explored the signature aggregation route](https://arxiv.org/ftp/arxiv/papers/1911/1911.04698.pdf) a while back. One potential issue is that an adversary may make a signature with large “coefficients”, which could potentially increase the message sizes. For example, with signature A+B and B+C on hand, the adversary can make an aggregated signature like A + (n+1) B + n C where n is a large number. This increases the size of the “coefficient” vector and thus the communication overhead. In comparison, the SNARK approach requires the coefficients to be either 0 or 1, and hence eliminates the issue.

---

**vbuterin** (2022-01-05):

Do we have concrete numbers on how long it takes to SNARK-prove a signature? It feels like it’s the constant factors that will ultimately decide whether a scheme like this is viable or not!

---

**Pratyush** (2022-01-05):

For a SNARK-friendly curve (e.g., Jubjub/Bandersnatch over BLS12-381), and using a SNARK-friendly hash function, signature verification can be less than 10k R1CS constraints, and probably even smaller for PLONK-like constraint systems. That’s provable in less than half a second on Groth16, and probably even quicker on accumulation-based systems like Halo2. (Single-threaded; multi-threading could reduce this to even ~50ms?)

---

**vbuterin** (2022-01-05):

Right, but it feels like here we’re trying to aggregate dozens or hundreds of signatures. I guess you can aim on the lower end of that, and compensate by having more aggregation levels.

How many milliseconds do you expect it would take to aggregate two proofs into one?

---

**levs57** (2022-01-10):

> By “levels” do you mean to make a tree-like network for SNARK proof aggregation?

I mean that you will have a circuit #k, which validates the following predicate “there exist two zk-snarks of level #k-1 with some boolean vectors v_1, v_2, which are correct, and the resulting vector is max(v_1, v_2)”. I think you can not create a snark which refers to *itself*.

