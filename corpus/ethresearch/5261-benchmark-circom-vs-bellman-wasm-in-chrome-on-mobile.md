---
source: ethresearch
topic_id: 5261
title: "Benchmark: Circom vs Bellman (wasm) in Chrome on Mobile"
author: poma
date: "2019-04-04"
category: zk-s[nt]arks
tags: [benchmark]
url: https://ethresear.ch/t/benchmark-circom-vs-bellman-wasm-in-chrome-on-mobile/5261
views: 4726
likes: 14
posts_count: 9
---

# Benchmark: Circom vs Bellman (wasm) in Chrome on Mobile

I was experimenting with snark proof generation inside a browser for mobile phones and made a benchmark: I’ve tested a simple circuit (5 rounds of pedersen commitment) written on Circom and ported to browser using browserify, and the same circuit written on Bellman and compiled to WebAssembly; I also compared them to their native counterparts.

```nohighlight
MacBook Core-i7 @ 2.6Ghz
circom (node.js):        53685ms
circom (chrome):         53266ms
circom (websnark):       1408ms
bellman (webassembly):   1151ms
bellman (rust, 1 core):  235ms
bellman (rust, 8 cores): 85ms

iPhone XS
bellman (webassembly):   1126ms
```

As we can see Bellman compiled to wasm is already 50x faster and still has a room for more than 10x improvement as WebAssembly execution speed should be pretty close to native speeds when everything is done right. The full support for wasm compilation was recently merged into Matter labs fork of Bellman, and it was uploaded to [crates.io](http://crates.io) and can now be incuded as `bellman_ce`, you can see [wasm-bellman](https://github.com/poma/wasm-bellman) test repo for example usage. On modern phones the execution speeds are similar to laptop speeds, so in the current state wasm compilation seems to be good enough for many simple snark proofs on mobile.

The main bottleneck is that when compiled to wasm Bellman is single threaded like Circom. If we take advantage of multiple CPU cores (most modern phones have 8), we can speed this up significantly. WebAssembly in Chrome already supports multiple threads with shared memory as experimental feature, so we are waiting when the rust compiler will support it (alternatively it can be done via importing WebWorker api). Additionally, the browser profiler [[1]](https://i.imgur.com/MsBltFz.png), [[2]](https://i.imgur.com/bDXZ2Ce.png) shows that most CPU time is spent in __multi3 that is called from mul_assign followed by internals of mul_assign itself, so maybe there are some inefficiencies in int64 multiplication implementation on wasm. When compiled to native mobile app, Bellman can already take advantage of all the cores and calculate proofs even faster than in browser. [@shamatar](/u/shamatar) from Matter labs did a few tests on that and got some impressive results.

We currently work on Circom -> Bellman export so that we can combine the ease of use of Circom language and performance and portability of Bellman. The goal is to make a toolchain that allows you to write snarks in Circom and get super fast .wasm + js bindings as compilation result, hiding the complexity of Bellman under the hood.

### Benchmark details

The circuit verifies that a hash corresponds to a private 256 bit preimage after taking 5 rounds of pedersen commitment. Resulting circuits on Circom and Bellman have similar number of constraints:

```nohighlight
3459 bellman
3540 circom
```

Circom has a little bit more partially because it calculates hash in 256 bit field compared to 254 bit in Bellman, but the difference is negligible.

The tests were done on a 5 year old laptop with 2.6GHz Core i7 CPU, and an iPhone XS.

Circom source: https://github.com/poma/circom-pedersen-benchmark

Native Bellman source: https://github.com/poma/bellman_pedersen

WebAssembly Bellman source: https://github.com/poma/wasm-bellman

In this last repo you can see an example of how to build your snark that will work within a browser.

See also: [@kobigurk benchmark and demo of Bellman in wasm](https://community.zkproof.org/t/zksnarks-in-webassembly-running-demo-and-discussion/30)

*update:* added websnark benchmark for the same circuit

## Replies

**lebed2045** (2019-04-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/poma/48/674_2.png) poma:

> room for more than 10x improvement

amazing achievement!

What’s the nature of “room for more than 10x improvement” you mentioned above?

What’s the memory consumption on these benchmarks?

---

**poma** (2019-04-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/lebed2045/48/2342_2.png) lebed2045:

> What’s the nature of “room for more than 10x improvement” you mentioned above?

Since WebAssembly generates the proof in 1151ms and native code in 85ms. There is no reason for them to be significantly different, we just need to find inefficiencies and fix them if possible (see 3rd paragraph in op).

I don’t know how to properly measure memory consumption, but during the proof Chrome tab eats 180Mb memory, I think most of it is allocated for browser related stuff and not for prover itself.

update: on memory snapshots wasm code appears to be taking around 50Mb.

---

**shamatar** (2019-04-04):

My impression is that native full-width u64 x u64 -> u128 is polyfilled with using multiple (need to check the assembly) half-width i64 x i64 -> i64 instructions in WASM. Naively one would expect 4 times slowdown just due to number of instructions required, which is close to single-thread native benchmark.

---

**jbaylina** (2019-04-16):

For reference in this post, we released websnark: https://github.com/iden3/websnark

This is a by hand written webassembly library. It uses web workers to parallelize.

The margins of improvement I’m aware of:

1.- May be there is a more optimal web assembly implementation.  It would be good to have some advice from the developers of the compiler of webassembly to native machine code.

2.- Multiescalar is done by windowing, but the windows are calculated on demand.  If the windows were precalculated, this could go faster at the cost of bigger proving key or some setup time in the application. It would also consume more memory.   (I plan to do this because I think it’s worthy for small circuits).

3.- Use some (not available yet) webassembly feratures, like native parallelization or wasm64.

---

**poma** (2019-04-16):

Nice! I’ll try to run the same test on websnark and see how it compares to bellmans wasm. So far it also doesn’t use threads and wasm64 (not sure about this one) so the comparison should be “fair”.

update: wait, so websnark doesn’t have native parallelization, but it still uses all the cores through webworkers right?

---

**jbaylina** (2019-04-19):

Yes, it creates webWorkers and run a webAssembly module on each. The effect is that it uses all the cores to compute the proof.

---

**poma** (2019-04-26):

[@jbaylina](/u/jbaylina) I’ve tested the same circuit on websnark and proof time is 1408ms. It’s a bit slower than single threaded wasm generated from Bellman, but still 35x faster than snarkjs.

---

**jbaylina** (2020-08-05):

For reference, it would be good to check the new snarkjs@0.3 It contains many improvements.

Also, I don’t know if this times includes witness computation.  If so, new circom@0.5 generates webassembly that should also run much faster,

