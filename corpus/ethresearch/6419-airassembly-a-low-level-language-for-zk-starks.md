---
source: ethresearch
topic_id: 6419
title: "AirAssembly: a low-level language for zk-STARKs"
author: bobbinth
date: "2019-11-07"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/airassembly-a-low-level-language-for-zk-starks/6419
views: 8396
likes: 10
posts_count: 7
---

# AirAssembly: a low-level language for zk-STARKs

One of the goals I have for [AirScript](https://ethresear.ch/t/airscript-v0-5-now-with-loops) is to make the language fully composable and enable writing modular “gadgets”. But as I’ve been thinking of how to accomplish this, I realized that AirScript is not the right level for where code composition should happen. There are just too many high-level constructs (and more are on the way) which makes code composition non-trivial.

Enter AirAssembly, which is a low-level language for encoding Algebraic Intermediate Representation (AIR) of computations. The goal of the language is to provide a minimum number of constructs required to fully express AIR for an arbitrary computation, and to make code composition much much simpler.

Unlike AirScript, AirAssembly is intended to be a compilation target for higher-level languages (of which AirScript will be one, but maybe other languages will emerge over time). I’m also hoping that AirAssembly could become a common language understood by various STARK libraries. So, the model could be something like this:

[![image](https://ethresear.ch/uploads/default/optimized/2X/a/a5eedc914d812508dab9d72b4bdea813fb36bc17_2_690x284.png)image1389×573 13.6 KB](https://ethresear.ch/uploads/default/a5eedc914d812508dab9d72b4bdea813fb36bc17)

I’ve just published the first draft of [AirAssembly specifications](https://github.com/GuildOfWeavers/AirScript/blob/master/AirAssembly.md), and would love to get feedback/comments from people working with or interested in STARKs.

Also, here is the obligatory MiMC example written in AirAssembly:

```auto
(module
    (field prime 340282366920938463463374607393113505793)
    (const 3)
    (static
        (cycle 42 43 170 2209 16426 78087 279978 823517))
    (transition
        (span 1) (result vector 1)
        (add
            (exp (load.trace 0) (load.const 0))
            (load.static 0)))
    (evaluation
        (span 2) (result vector 1)
        (sub
            (load.trace 1)
            (add
                (exp (load.trace 0) (load.const 0))
                (load.static 0))))
    (export mimc128 (steps 256))
    (export mimc256 (steps 1024)))
```

## Replies

**AlexeyAkhunov** (2019-11-07):

I really like the idea, especially if it means interoperability

---

**bobbinth** (2019-12-06):

I’ve just released a JavaScript compiler/runtime for AirAssembly. The specs have changed a little as well since my last post.

The library is located here: https://github.com/GuildOfWeavers/AirAssembly

And the updated specs are here: https://github.com/GuildOfWeavers/AirAssembly/tree/master/specs

Here is a simple example of how the library can be used to generate an execution trace table and constraint evaluation table for a MiMC computation:

```auto
import { compile, instantiate } from '@guildofweavers/air-assembly';

const source = `
(module
    (field prime 4194304001)
    (const
        (scalar 3))
    (static
        (cycle (prng sha256 0x4d694d43 64)))
    (transition
        (span 1) (result vector 1)
        (add
            (exp (load.trace 0) (load.const 0))
            (get (load.static 0) 0)))
    (evaluation
        (span 2) (result vector 1)
        (sub
            (load.trace 1)
            (add
                (exp (load.trace 0) (load.const 0))
                (get (load.static 0) 0))))
    (export main (init seed) (steps 32)))`;

// instantiate AirModule object
const schema = compile(Buffer.from(source));
const air = instantiate(schema);

// generate execution trace table
const prover = air.createProver();
const trace = prover.generateExecutionTrace([3n]);

// generate constraint evaluation table
const tracePolys = air.field.interpolateRoots(prover.executionDomain, trace);
const constraintEvaluations = prover.evaluateTransitionConstraints(tracePolys);
```

A more sophisticated example of AirAssembly for Poseidon hash function can be found [here](https://github.com/GuildOfWeavers/AirAssembly/blob/9d1058ad1b3c92f75c045dc579c8a7750ef97c24/examples/poseidon.ts).

Next, I’m planning to integrate the runtime into [genSTARK](https://github.com/GuildOfWeavers/genSTARK).

One thing AirAssembly doesn’t yet support is “long-range” constraints. I’d love to add support for these as I think that opens up some interesting use cases. If anyone has any thoughts about long-range constraints (or any other aspect of AirAssembly), would love to hear them.

---

**bobbinth** (2019-12-18):

I’ve just released a new version of AirAssembly (v0.2). Notable changes include:

1. A single AirAssembly module can now contain AIR for many computations. This will enable “library” modules which will export different types of computations (e.g. hash functions, signature verification etc.).
2. It is now possible to define module-level functions to encapsulate common algebraic expressions. This makes code much more compact.
3. AirAssembly specs now include initial support for “long-range” constraints - thought, the compiler/runtime doesn’t handle them yet.

Here is how AirAssembly module for MiMC computation looks like now:

```auto
(module
    (field prime 4194304001)
    (const $alpha scalar 3)
    (function $mimcRound
        (result vector 1)
        (param $state vector 1) (param $roundKey scalar)
        (add
            (exp (load.param $state) (load.const $alpha))
            (load.param $roundKey)))
    (export mimc
        (registers 1) (constraints 1) (steps 1024)
        (static
            (cycle (prng sha256 0x4d694d43 64)))
        (init
            (param $seed vector 1)
            (load.param $seed))
        (transition
            (call $mimcRound (load.trace 0) (get (load.static 0) 0)))
        (evaluation
            (sub
                (load.trace 1)
                (call $mimcRound (load.trace 0) (get (load.static 0) 0))))))
```

genSTARK has also been updated to work with AirAssembly back-end, though, the changes haven’t been merged to the master yet (if anyone is curious, they are in [this PR](https://github.com/GuildOfWeavers/genSTARK/pull/25)).

As always, any thoughts/feedback is welcome.

---

**bobbinth** (2020-01-22):

I’ve just released a new version of [AirScript](https://github.com/GuildOfWeavers/AirScript) (v0.6) and [genSTARK](https://github.com/GuildOfWeavers/genSTARK) library (v0.7). The biggest thing is that now AirScript gets compiled into an [AirAssembly](https://github.com/GuildOfWeavers/AirAssembly) module, and then genSTARK creates a STARK from this AirAssembly module.

In fact, genSTARK can now instantiate STARKs from either AirScript or AirAssembly source code. This will help with making AirScript modular/composable - which is what I’m planning to do next.

Other notable change is that now AirScript supports naming of input and readonly registers. So, for example, a MiMC STARK in AirScript can be written like this:

```auto
define MiMC over prime field (2^128 - 9 * 2^32 + 1) {
    const alpha: 3;

    // define cyclic readonly register
    static round_constant: cycle [42, 43, 170, 2209, 16426, 78087, 279978, 823517];

    // require a single secret input
    secret input start_value: element[1];

    // transition function definition
    transition 1 register {
        for each (start_value) {
            init { yield start_value; }
            for steps [1..8192] {
                yield $r0^3 + round_constant;
            }
        }
    }

    // transition constraint definition
    enforce 1 constraint {
        for all steps {
            enforce transition($r) = $n;
        }
    }
}
```

More sophisticated examples (hash functions, Merkle proofs) can be found [here](https://github.com/GuildOfWeavers/genSTARK/tree/master/examples/poseidon) and [here](https://github.com/GuildOfWeavers/genSTARK/tree/master/examples/rescue).

---

**porobov** (2020-01-23):

Wow! This is amazing! SNARKs to the masses))

I tried Zokrates recently. Could you please show an example similar their [tutorial](https://zokrates.github.io/sha256example.html)? That would be really  helpful.

---

**bobbinth** (2020-01-23):

Thanks! I have some examples [here](https://github.com/GuildOfWeavers/genSTARK/tree/master/examples) but nothing like a full-blown tutorial yet.

One of the reasons for this is that the language is still evolving quite a bit and the tutorial would get obsolete pretty quickly. I think the things will stabilize after the next iteration, and I do have a tutorial on my TODO list after that ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

