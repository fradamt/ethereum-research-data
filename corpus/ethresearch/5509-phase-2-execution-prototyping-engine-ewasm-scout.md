---
source: ethresearch
topic_id: 5509
title: Phase 2 execution prototyping engine (Ewasm Scout)
author: axic
date: "2019-05-25"
category: Sharded Execution
tags: []
url: https://ethresear.ch/t/phase-2-execution-prototyping-engine-ewasm-scout/5509
views: 6356
likes: 6
posts_count: 7
---

# Phase 2 execution prototyping engine (Ewasm Scout)

This post is introducing a phase 2 prototyping effort, but lets first discuss some background.

---

Phase 2 proposals:

- Casey: Phase One and Done: eth2 as a data availability engine
- Vitalik: A layer-1-minimizing phase 2 state execution proposal

The actual spec is here: Phase 2 Proposal 1
- Slides summarising the proposal

Vitalik: [Proposed further simplifications/abstraction for phase 2](https://ethresear.ch/t/proposed-further-simplifications-abstraction-for-phase-2/5445)

Vitalik: [Phase 2 Proposal 2](https://notes.ethereum.org/s/Bkoaj4xpN)

Matt Garnett: [Ethereum Execution Environment](https://hackmd.io/s/BkGWnignE)

Goals:

1. Create a (black boxed) execution prototyping engine
2. Create some example contracts (“execution scripts”)
3. Ask other teams to create useful scripts
4. By having actual real world use cases in scripts, we can benchmark the design and identify bottlenecks

Since Phase 2 Proposal 2 seems to offer a stateless execution model a lot of processing is shifting into the scripts. Instead of whiteboarding these proposals, the main goal here is to provide a simple environment where scripts can be developed,  tested and iterated on. This would also allow iterating on the Phase 2 proposal.

### Phase 2 Proposal 2 Questions

#### Where to do execution script validation?

New code is proposed via `NewExecutionScript` in the beacon block and is placed into the beacon state.

1. Should validation occur on the beacon chain?
2. Should validation occur on the shard chain? If so, should it happen once and the code be marked in valid if it failed?

#### How to track execution time (aka “gas metering”)?

There’s no limit to execution time in the current design.

### Phase 2 Proposal 2 EEI

[In this proposal](https://notes.ethereum.org/s/Bkoaj4xpN) execution is simplified to basically a “stateless execution”:

```auto
post_state, deposits = execute_code(exec_code, [pre_state, block.data]))
```

In the simplest form, the script needs to:

- retrieve the pre_state
- return the post_state
- return a list of deposits
- potentially access other parts of the shard state, shard block and beacon state

#### Core EEI proposal

Basic concepts about “the EEI” can be found in the [ewasm design repo](https://github.com/ewasm/design).

- eth2::loadPreStateRoot(memoryOffset: u32ptr)

The current pre_state_root (256-bit value) is loaded from the memory offset pointed at

`eth2::blockDataSize() -> u32`

- Returns the size of the block.data

`eth2::blockDataCopy(memoryOffset: u32ptr, offset: u32, length: u32)`

- Copies length bytes from block.data + offset to the memory offset

`eth2::savePostStateRoot(memoryOffset: u32ptr)`

- The post_state_root (256-bit value) is set to the content of the memory offset pointed at

`eth2::pushNewDeposit(memoryOffset: u32ptr, length: u32)`

- This expects a Deposit data structure to be stored at the memory offset (SSZ serialised?). It will be appended to the deposit list.

*Note*: the `state_root` above is currently a 256-bit value, but it would be possible to extend this to support RSA accumulators for example.

`eth2::` here refers to the namespace these functions are in.

Execution of the script starts with executing the `main()` function.

**Question:** Should the modified state also be returned (not just the state root)?

**Question:** What other data from the shard state, shard block or beacon block should be made available to the scripts?

#### Extensions

The following features will be recurring among different execution scripts. It would make sense providing a single implementation of these for two reasons:

- to save space
- to speed up execution

A good option here is to make them system libraries, which can be implemented natively by clients if they choose to do so.

Candidates:

1. Bignums (see https://github.com/ewasm/design/issues/189)
2. SSZ
3. BLS utilities
4. Hashing
5. ?

### Phase 2 prototyping

Considering the above a rough prototyping tool was created: https://github.com/ewasm/scout

Please check out the README, even if it quite sparse.

To get some excitement going, here is an actually working execution script source code:

```auto
extern crate ewasm_api;

use ewasm_api::*;

#[cfg(not(test))]
#[no_mangle]
pub extern "C" fn main() {
    let pre_state = eth2::load_pre_state();

    assert!(eth2::block_data_size() == 0);

    // No updates were made to the state
    let post_state = pre_state;

    eth2::save_post_state(post_state)
}
```

The next goal is to write a more complex script. The “deposit manager” (aka [in-shard ETH transfer](https://notes.ethereum.org/s/Bkoaj4xpN#Implementing-in-shard-ETH-transfers)) seems like the obvious choice.

## Replies

**matt** (2019-05-25):

> Should the modified state also be returned (not just the state root)?

I don’t think the modified state is necessary for shard nodes since it will be the relayers’ responsibility to i) package transactions with their merkle proofs and ii) to store whatever state is necessary to perform future state transitions / provide merkle proofs. Therefore in the relayer runtime there should be a way for retrieving and saving the modified state, but not in a shard node.

As for the implementation, I’m not sure which is preferable: the beacon chain contract explicitly returning the modified state and the shard node discarding it or making use of the [context object](https://ethresear.ch/t/eth-execution-environment-proposal/5507) I proposed.

> What other data from the shard state, shard block or beacon block should be made available to the scripts?

From Vitalik’s [optimistic receipt root](https://ethresear.ch/t/fast-cross-shard-transfers-via-optimistic-receipt-roots/5337) design, `expected_roots` would be another important data struct to provide to execution environments.

> A good option here is to make them [extensions] system libraries, which can be implemented natively by clients if they choose to do so.

I definitely agree with providing a single implementation of these, but I would argue that it would be better to provide them as another execution scripts – aka wasm precompiles. I believe this is a more favorable approach because it minimizes the overhead for clients even more and allows upgrades and new scripts to be added without hard forks. Obviously performance is crucial for these extensions, so if we can’t securely compile them to native code from wasm they may have to just be implemented in the client.

---

**axic** (2019-05-25):

Thanks for the response!

![](https://ethresear.ch/user_avatar/ethresear.ch/matt/48/4560_2.png) matt:

> Therefore in the relayer runtime there should be a way for retrieving and saving the modified state, but not in a shard node.

Exactly. And the script needs a way to expose the modified state. The shard node can ignore it. I may need to explore one implementation as part of writing the “deposit manager”.

![](https://ethresear.ch/user_avatar/ethresear.ch/matt/48/4560_2.png) matt:

> I definitely agree with providing a single implementation of these, but I would argue that it would be better to provide them as another execution scripts – aka wasm precompiles.

Please have a look at the “[system libraries](https://github.com/ewasm/design/issues?q=is%3Aissue+is%3Aopen+label%3A%22system+libraries%2Fcontracts%22)” tag on the Ewasm design repo. We use the term quite liberally. In short, the idea would be to specify a standard interface for the ones I’ve suggested and provide a wasm implementation of them. They can be dynamically linked or the node can decide to natively implement (some of) them and link against those.

The speed and overheads are yet to be discovered and real decisions cannot be made without benchmarking. For the time being likely whatever is easier for the given case will be done and we can iterate on that.

---

**vbuterin** (2019-05-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/axic/48/1578_2.png) axic:

> Should validation occur on the beacon chain?
> Should validation occur on the shard chain? If so, should it happen once and the code be marked in valid if it failed?

I think it has to be done in the beacon chain. The reason is that there’s no good place to mark it failed if the validation occurs in the shard chain; shard chains don’t have the ability to directly write to beacon chain state, so you would have to separately mark it failed in every shard, which is even less efficient than just doing it in the beacon chain.

> There’s no limit to execution time in the current design.

I was assuming by default some fixed gas limit; if desired it could also be a beacon chain state variable that can get voted up or down over time.

> Core EEI proposal

Question: why make the first three an EEI instead of just passing them as arguments to the function? Or is it lower complexity to do it this way?

> Question: Should the modified state also be returned (not just the state root)?

The consensus layer doesn’t recognize any concept of “state beyond the state root”; from the consensus layer’s point of view, the state root *is* the state. So, no.

> Question: What other data from the shard state, shard block or beacon block should be made available to the scripts?

Maybe shard ID? In general, any needed info can be Merkle proven from the shard state so we can afford to be fairly minimal here.

> Extensions

Are we really giving up on the idea of linear-pass-compiling callable WASM contracts stored on the beacon chain to get any needed efficiencies? To me that sounds like a really tragic thing if we end up going that way; we’d end up imposing a lot of load on all the different clients asking them to keep adding new implementations of different crypto primitives.

In the short term, I think bignums are ok because of their universality, BLS is ok because we are using it for plenty of things already, and same with SHA256, but everything else is much harder to justify. I don’t see a need to have a protocol-level SSZ library; SSZ is not computationally intensive, and we could just implement the library in WASM code and make it be a callable beacon chain contract.

> From Vitalik’s optimistic receipt root  design, expected_roots would be another important data struct to provide to execution environments.

Optimistic receipt roots are theoretically implementable entirely as a higher level concept; basically you would have a light client of some other shards inside each shard. Though I suppose if we want to ensure it keeps being funded we could enshrine it…

---

**axic** (2019-05-25):

The goal with the current prototype is to get started on writing execution scripts and only write the bare minimum client code needed for that. The “helloworld” example is fairly useless, but I’m working on a proper example now, which actually takes in a state root, the actual state, some new data and returns the new root. It doesn’t yet make use of merkle proofs.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I think it has to be done in the beacon chain.

In that case basically I would suggest to extend your “Proposal 2” where it has `verify_wasm` to also state it not only verifies Wasm validity, but that the code satisfies the Phase 2 scripting requirements (aka uses the correct EEI, etc.).

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I was assuming by default some fixed gas limit; if desired it could also be a beacon chain state variable that can get voted up or down over time.

The variable sounds nice, but we can start with a fixed limit. What would be an appropriate limit (thinking EVM terms in references). How much time is there to spent execution time on?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Question: why make the first three an EEI instead of just passing them as arguments to the function? Or is it lower complexity to do it this way?

It is mostly a decision to help prototyping. It is easy to change/extend them without breaking every example script. Keep in mind though that all these fields are larger than 64-bit and hence must be passed via memory. In some cases, like browsers, it still may be problematic preloading the memory from the executor’s side. It is not a problem outside of browsers.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Are we really giving up on the idea of linear-pass-compiling callable WASM contracts stored on the beacon chain to get any needed efficiencies?

I don’t think we’re giving up on it.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> we’d end up imposing a lot of load on all the different clients asking them to keep adding new implementations of different crypto primitives.

Extension might be the wrong term, but explained that part a bit further in the [response to Matt](https://ethresear.ch/t/phase-2-execution-prototyping-engine-ewasm-scout/5509/3).

Having these libraries still allows static linking them with the execution scripts *and then* compiling them to native code. The main benefit in this case is the saving on space and reusing code.

In the current state of prototyping actually all of what I’ve mentioned is just compiled to Wasm as part of the execution script. There’s no split needed right now.

---

**vbuterin** (2019-05-25):

Got it, I didn’t understand the nuance that some of the decisions were shortcuts for prototyping and aren’t meant to necessarily reflect considered opinions about eventual optimums; that seems like a very pragmatic thing to do for the time being.

> In that case basically I would suggest to extend your “Proposal 2” where it has verify_wasm to also state it not only verifies Wasm validity, but that the code satisfies the Phase 2 scripting requirements (aka uses the correct EEI, etc.).

Got it, will do.

![](https://ethresear.ch/user_avatar/ethresear.ch/axic/48/1578_2.png) axic:

> The variable sounds nice, but we can start with a fixed limit. What would be an appropriate limit (thinking EVM terms in references). How much time is there to spent execution time on?

Maybe 100ms average case? Keep in mind these blocks are coming every 3 seconds, so that comes out to roughly the same CPU percentage per shard as the current eth1 chain. Though I’d be ok increasing it more particularly if eg. that ends up not being sufficient to verify a single STARK.

---

**axic** (2019-05-29):

[@vbuterin](/u/vbuterin) in the “in-shard ETH transfer” section `processDeposit` doesn’t return the deposits, but `process_block` below that expects it.

Can you extend the “spec” to clarify that part?

I assume `deposit_data` is what needs to be returned. Also `MyDeposit` has a `deposit` field but `processDeposit` expects `deposit_data`.

