---
source: ethresearch
topic_id: 9318
title: EVM optimistic rollup using Truebit
author: vbuterin
date: "2021-05-01"
category: Layer 2
tags: []
url: https://ethresear.ch/t/evm-optimistic-rollup-using-truebit/9318
views: 47234
likes: 29
posts_count: 14
---

# EVM optimistic rollup using Truebit

The interactive verification protocol Truebit [recently launched](https://truebit.substack.com/p/truebit-early-access). This post will assume that something like Truebit exists as a black box giving delayed results to queries of the form “run some code and return the output”, and show how to build an EVM optimistic rollup on top of it.

Truebit accepts code in WebAssembly. There are many Ethereum clients written in many languages, and many of them have compilation paths to WASM (eg. [go](https://www.sitepen.com/blog/compiling-go-to-webassembly), [Java](https://blog.dmitryalexandrov.net/webassembly-for-java-developers/), [Rust](https://developer.mozilla.org/en-US/docs/WebAssembly/Rust_to_wasm)). The first step would be to create a “stateless” version of a client. This is actually easy: replace the database lookups with lookups to a table that is provided as an input. The resulting “client” would implement a pure function: `process_block(state_lookup_table, block) -> post_state_root`. We assume that this can be compiled to WASM code.

The second step is to build the actual chain module. There is one challenge here: a blockchain is *not* stateless. When a fraud proving process is started against some block N in an optimistic rollup chain, there is an implicit assumption that the state committed to by the pre-state root of block N is available (ie. common knowledge). For this reason, if someone sees that an optimistic rollup chain contains invalid blocks, they should challenge the *first* invalid block. But Truebit by itself is an interactive computation system for pure functions. We get around this by simply moving a couple of easy steps of the interactive verification process outside of the Truebit call.

Here is a basic protocol description:

- The contract stores a chain of block hashes and state roots: List[Tuple[block_hash, state_root]]
- A sequencer (we leave it to the implementer to decide who is a valid sequencer; there may be multiple sequencers) can add a new block; they call a function add_block(expected_pre_state: bytes32, block: bytes, post_state: bytes32) which requires the expected_pre_state to be the head state root and then adds ((block, post_state)) to the chain.
- To challenge a state root, some challenger calls challenge(index: int, lookup_table: bytes, block: bytes). This:

Checks that the hash of the block matches the saved hash
- Starts a Truebit call to process_block
- Computes and saves the Merkle root of the lookup table.

Once the challenge has begun, anyone can challenge the challenger by proving that their lookup table is wrong: they can provide a Merkle branch rooted in the pre-state of that block showing a value at some position in the tree, and a Merkle branch rooted in the lookup table root showing that same value. If the two branches conflict, the challenge is cancelled and the challenger’s deposit is slashed.
Once the truebit call returns the `post_state_root` (the mechanics of Truebit itself ensure that this can only happen after at least one waiting period), it’s assumed that if there existed a valid challenge to the lookup table someone would have made the challenge, and so the remaining logic proceeds under the assumption that the Truebit result was correct.

- If the result is not the previously-saved post_state_root, and the result is not ERROR: LOOKUP_TABLE_MISSING_NEEDED_VALUE, the challenge is successful, the original submitter is slashed, and the next few submitters, instead of publishing blocks, will be tasked with publishing corrected state roots to replace the incorrect state root and all subsequent state roots. A variable index_of_next_state_root_to_replace is used to keep track of this process.
- If the result is one of those two values, the challenger is slashed.

Note: if you make an invalid block, *or* you challenge a block with an untrusted pre-state, you are vulnerable to getting slashed. So it’s important for sequencers to add blocks only on top of a fully valid chain, and for challengers to only challenge the *first* invalid block (so its pre-state is still guaranteed to be what you think it is).

**Reminder 2021.05.03: ethresear.ch is a special-purpose scientific forum, and is not a general discussion venue for (especially non-technical) issues about crypto projects, *even if* those issues are important. Please stay on topic.**

## Replies

**Mister-Meeseeks** (2021-05-03):

Practically speaking, I think it’s worth considering possible exploits in the presence of adversarial miners. With Optimistic rollups, there may potentially be billions of dollars on the line from controlling the timing to a single `publish()` call. The current Mev Flashbots frontrunner debacle has proven that the miners are more than happy to abuse their position, and manipulate blocks in shady ways to engage in financial shenanigans.

I’m sure others with more familiarity with optimistic rollups can dig deeper into the details, and establish formal bounds under specific conditions of adversarial miners. But one point that’s potentially concerning to me is:

> it’s assumed that if there existed a valid challenge to the lookup table someone would have made the challenge

Assuming a single period is a few blocks, then it’s more than possible for an adversarial miner to censor the validity challenge. The largest pool, Ethermine, makes up 27% of the hash power, and therefore can expect to fully control a three-block sequence one out 50 times. A Flashbots like pool may potentially allow for multiple mining pools to coordinate as a cartel.

Yeah, the fraudster is still at high risk of getting slashed. But particularly during periods of high market volatility, the penalties for getting slashed may be small relative to the rewards to manipulating the chain. There’s no real way for the fraud penalties to dynamically scale with the size of the Defi markets, so in many cases getting caught for fraud may simply be a cost of doing business in terms of miner-orchestrated market manipulation.

Just my two cents. I’m sure someone with more familiarity with rollup technology can give more precise  estimates on these threats and options to minimize them. My simple point is, based on the past six months, don’t assume that mining or transaction sequencing is a disinterested arms-length process that can be counted on behaving in an honest or deterministic way.

---

**vbuterin** (2021-05-03):

> Assuming a single period is a few blocks

This assumption is wrong. The typical challenge period for protocols like this is one week.

(In the [Truebit whitepaper](https://people.cs.uchicago.edu/~teutsch/papers/truebit.pdf) it says [page 24] that the challenge period can be set by whoever calls the function to start a task. If so, it’s up to the creator of this EVM rollup to set the challenge period responsibly)

---

**Option-Panda** (2021-05-06):

[@vbuterin](/u/vbuterin)  Truebit is based on WebAssembly to scale the computational power of contracts, on an web application level, with constraints. An adversarial miner might also infect the system’s ideal working based on economic return/cost. Gaming a system with economics will always be exploited by smart scientists. However, it is also an inherent low-efficiency economic incentive mechanism Truebit must implement.

What’s more, real-world applications usually require large amount of data storage, which Truebit doesn’t deal with.

Cartesi( [cartesi.io](http://cartesi.io)) might be a much more solid solution over Truebit. It doesn’t require an incentive layer and it supports offchain data storage representation onchain.

---

**denett** (2021-05-06):

If the challenge period is one week and you are not allowed to build on top of a block with an invalid post state, does this mean the chain halts for a week?

Would it be possible to add a block on top of an a block with an invalid post state by also posting the correct pre-state. If it turns out you used an invalid pre-state you will also be slashed, but at least the chain can go on.

---

**kladkogex** (2021-05-07):

Last time I reviewed Truebit there were a number of security flaws, especially related to frontrunning

May be they fixed them now.

---

**v01-d** (2021-05-08):

Maybe if they still existed, if they ever existed, maybe you’d point them out…

Let’s BUIDL

---

**codebei** (2021-05-14):

[@vbuterin](/u/vbuterin) are you aware of any team working on actually building this?

---

**vbuterin** (2021-05-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> If the challenge period is one week and you are not allowed to build on top of a block with an invalid post state, does this mean the chain halts for a week?

Nope! The chain should just allow you to build on top of a block that’s not the current head. Then you enforce a “fork choice rule” of “start at the root, if a block has multiple children, choose the earliest-submitted valid child, and keep going until you get to the head”.

---

**TiTi_Protocol** (2021-05-31):

Will truebit be the best practices?

---

**kladkogex** (2021-05-31):

As I remember front running was the unsolved problem in Truebit.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> To challenge a state root, some challenger calls challenge(index: int, lookup_table: bytes, block: bytes). This:

As described it is subject to front running (attacker can simply do nothing and wait for an honest verifier to submit the challenge.

If a commit-reveal scheme is used, the front-runner can front-run the commit, and then recompute the root.   Addressing front-running in Truebit is in general hard.

---

**karl** (2021-10-11):

An implementation using roughly this approach!

https://github.com/geohot/cannon ![:grin:](https://ethresear.ch/images/emoji/facebook_messenger/grin.png?v=9)

Get ready! Cuz’ it’s coming! ([reference](https://youtu.be/pq7ICQzyH5k?t=20))

---

**0xMax34** (2022-01-25):

Any update? or is there anyone Truebit is working with (*dogecoin*) that you could share? or not share ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=10) I  mean hint! Thank you for the hard work. I want to see truebit used everywhere

---

**jesuscrypto33** (2022-07-22):

Hey ![:wave:](https://ethresear.ch/images/emoji/facebook_messenger/wave.png?v=12) all

Is there any update about truebit + ethereum?

Do you believe that after Ethereum upgrades, will truebit start gaining more adoption?

Is there any new developments going on?

Thanks ![:pray:](https://ethresear.ch/images/emoji/facebook_messenger/pray.png?v=12)

