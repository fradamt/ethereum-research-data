---
source: ethresearch
topic_id: 20313
title: L2 sequencer proving on weak hardware; parallelization and decentralization
author: rezahsnz
date: "2024-08-20"
category: Layer 2 > ZK Rollup
tags: []
url: https://ethresear.ch/t/l2-sequencer-proving-on-weak-hardware-parallelization-and-decentralization/20313
views: 461
likes: 4
posts_count: 4
---

# L2 sequencer proving on weak hardware; parallelization and decentralization

[Linea’s sequencer](https://ethresear.ch/t/vortex-building-a-prover-for-the-zk-evm/14427) proves a 30m gassed block of transactions in 5 minutes. Here’s its setup:

> On a 96 cores machine with 384 GB of RAM (hpc6a.48xlarge on AWS)
> In 5 minutes (only including the inner-proof)

So is it possible to reduce the proving time and, at the same time, obtain decentralization guarantees? We have an idea.

### Overview

Almost all of the L2 sequencers are closed-source, intellectual property, and thus protected behind centralized setups. To cram that much power into an entity requires a great deal of justification today. To decentralize the flow, on the other hand, one has to accept certain amounts of delay and noise usually found in decentralized compute networks.

#### zkVMs, recursion, and Risc0’s approach

Any zkVM toolset puts a certain upper bound on the maximum number of cycles(roughly speaking 1 cycle equals 1 operation) it can prove in one go. This is usually done for efficiency reasons. For [Risc0](https://github.com/risc0), a RISC-V general zkVM, it is 2^24 ~ 16.78m cycles. With recursion, proving infinitely sized programs are made possible. So the solution is to divide a large program into individual sub-programs(called segment in Risc0 jargon) and have them proved one by one and aggregate the proofs into a final proof as if the whole program was proved in one go. For example, consider proving a 1b cycles program. With 16.78M maximum segment size limit, one ends up proving 60 segments. The upper bound for segment size limit is not the end of story however and one can customize it into a well-known range of [2^13 - 2^24]. Each segment limit size needs specific memory requirements shown on Table 1:

[![Screenshot from 2024-07-18 14-37-34](https://ethresear.ch/uploads/default/optimized/3X/b/7/b790b7f5fb18cec94d0e621383844425862ba9fb_2_690x387.png)Screenshot from 2024-07-18 14-37-341366×768 32.9 KB](https://ethresear.ch/uploads/default/b790b7f5fb18cec94d0e621383844425862ba9fb)

Extrapolating Table 1’s values, we get 50m cycles for a program that needs 384gb of memory, in order to be proved in Risc0. Recall that Linea’s prover uses 384gb of memory to generate proofs. This is a naive 1-1 translation, but we can treat it as baseline for further testing. So, with this assumption, should one write Linea’s sequencer logic in Risc0, she would end up with a program that is 50m cycles long. Doubling cycles to ~90m, to account for aggregation won’t hurt here.

#### Segmentation, parallel proving, and decentralization

Recursion is a powerful idea in zkVM proving. With recursion once can get to prove seemingly large programs very quickly assuming she has a prove-ready network of machines. Table 2 shows a segmented prove session for a 90m cycles program on a pretty weak machine(8+ years old, Intel core i7 5500U(2C 4T), 16gb memory):

[![Screenshot from 2024-07-18 14-47-06](https://ethresear.ch/uploads/default/optimized/3X/0/9/091af39f1eb4b3465f1de18222eed6c4d1051edb_2_690x235.png)Screenshot from 2024-07-18 14-47-061288×439 64.4 KB](https://ethresear.ch/uploads/default/091af39f1eb4b3465f1de18222eed6c4d1051edb)

As you can see, different segment size limits result in varied proving regimes. In Table 2, two columns are colored in green, 2^18 and 2^19. Consulting Table 1, we would get 2gb and 4gb of required memory to prove them respectively. These columns are sweet spots for any zkVM proving network whose nodes are presumably weak. Focusing on the 2^19 segment size limit, to prove a 90m cycles program, one would need at least 168 nodes in order to prove the program in 4 minutes and 9 seconds. But 168 nodes is a faulty assumption. In reality, if a p2p network is to undertake the proving job, it needs to have redundancy values of 1:4 and above. The redundancy accounts for noise that is a feature of any p2p network. With 1:4 redundant nodes, 1 in every 5 nodes is assumed to be honest and the rest are time wasters. So, a 1:4 redundant p2p network needs at least of 840 nodes to get the job done.

Assuming that the proving network is p2p, one can expect to obtain decentralized guarantees en route.

### Conclusion

Here we introduced an imaginary setup to decentralize and improve L2 sequencer proving times. If the claim turns out to be legit, we would expect to improve the overall proving time for any zkVM application area. In addition, the setup provides decentralization guarantees as a side effect. While everything looks nice, we, at [Wholesum network](https://github.com/WholesumNet) would like to put this setup to test and see if it works in action. If successful, a p2p verifiable compute network of 10,000 weak nodes can handle up to 10 Linea like L2s.

A somewhat more expanded version of this post is also available [here](https://github.com/WholesumNet/docs/blob/779942cf6f650d24fcedf2d8da5a6dd2033a9fee/parallelization/parallelized-proving/report.pdf).

We appreciate your feedback.

## Replies

**rezahsnz** (2024-08-27):

I asked the Polygon team on the stats of the sequencer prover machinery, and got the following reply:

Google T2D VM, 60 cores CPU, 240GB memory

Performance: 580 gas/sec/vCPU

The stats are not confirmed by the team though and so please allow some error.

Extrapolating the performance for a 30M gas scenario like the one with the Linea sequencer, and we get:

30,000,000 / (60 * 580) / 2.56 = ~`5 mins and 28` secs of proving.

(Linea enjoys 384GB of memory + 96 cores CPU, so we better adjust the time and divide by 2.56(384 / 240 + 96 / 60))

---

**rezahsnz** (2024-09-10):

A rough sketch of the pipeline:

[![pipeline](https://ethresear.ch/uploads/default/optimized/3X/9/c/9c2d8fce4c69ada9ea9a6941d2867daf24804692_2_312x500.jpeg)pipeline1920×3074 150 KB](https://ethresear.ch/uploads/default/9c2d8fce4c69ada9ea9a6941d2867daf24804692)

---

**rezahsnz** (2024-12-04):

Some updates on our upcoming proving test:

On [zeth](https://github.com/risc0/zeth)(verifiable reth by Risc0 team):

With **po2=20**(**8gb** memory required to prove a segment) it takes **2663** segments(total cycles **~2.8b**) to verifiably produce a single eth block.

with **po2=19**(**4gb** memory required to prove a segment) it takes **5942** segments(total cycles **~3.1b**) to verifiably produce a single eth block.

So, with **po2=19**, and to obtain the final stark, we need **1 prove round** followed by **13 join rounds**. Given ~30k prover nodes, 1:4 redundancy, each powered by modern PC(e.g. with Intel core i5 1240p, 32gb memory, performance mode on ubuntu 2024),  it would be possible to produce the block + the stark proof in 200-300 seconds assuming 0 storage latency.

How?

Proving each segment takes ~60 seconds and joining two proofs take ~11 seconds. We have `one prove round(60s) + 13 join rounds(11s): (1 * 60s) + (13 * 11s) = 203s`.

Since decentralized storage is involved, there is a great amount of latency. Blobs are max 500kb in size. Before proving starts, clients need to do `1 batch upload of segments` . Each segment prove operation involves `1 download(segment) + 1 upload(proof)` on the prover side and `1 download(proof)` on the client side. Each join involves `2 downloads(proofs) + 1 upload(proof)` on the prover side and `2 uploads(proof) + 1 download(proof)` on the client side. More data on how decentralized storage affects the proving time will be provided later.

