---
source: ethresearch
topic_id: 15231
title: An idea about how to use zk-vms with the Edge Computing Achitectures in Ethereum
author: Wanseob-Lim
date: "2023-04-07"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/an-idea-about-how-to-use-zk-vms-with-the-edge-computing-achitectures-in-ethereum/15231
views: 1915
likes: 12
posts_count: 8
---

# An idea about how to use zk-vms with the Edge Computing Achitectures in Ethereum

[@CPerezz](/u/cperezz) [@oskarth](/u/oskarth), Violet, and Chiro had a presentation at the zk residency group for about the future verifiable computation researches, and mentioned that *“WASM does not have a gas model, so the computation is unbounded.”*

So I’m just bringing up an idea here about how to use the gas model in the verifiable computational schemes.

This is a slide that I’m using that why we should contribute to the Ethereum scaling

[![Untitled drawing](https://ethresear.ch/uploads/default/optimized/2X/6/6a6de9196c5fb7ba954e29c3a96444494bba12b7_2_690x130.png)Untitled drawing1493×282 101 KB](https://ethresear.ch/uploads/default/6a6de9196c5fb7ba954e29c3a96444494bba12b7)

So one of the future scaling is something like the end-clients compute somthing on their devices and submiting a proof instead of letting other execution layer nodes to run all the computations.

In this scenario, we can have an Edge Computing Interface such as

```auto
execution(
	function,
	input vars,
	state refs,
	proof
) -> output vars: {\[key\]: value}
```

Then, the execution layer nodes updates the state by the `output vars`, and we can make the gas cost just depends on the length of the output vars.

Just a quick idea sharing ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

## Replies

**longfin** (2023-04-18):

Recently, I became a fan of a similar idea. ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=12) it seems that Ethereum can operate purely as a data availability and state verification layer and can maximize parallelism.

here’re my concernings about that idea. (although I’m not familiar with zk yet, so it may be wrong ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=12)).

1. Even if the prover runs on WASM, the verifier still needs to be runnable on the EVM, and its complexity & efficiency might be affected by the program’s kinds.
2. Since we need the previous state for the computation, computation on the edges might be more complex. this may be a slightly different context than where DAs normally provide data availability for verification.

p.s. personally, I’m also interested in projects that use a general-purpose ISA like [risc0](https://www.risczero.com/)

---

**fewwwww** (2023-04-18):

It seems to me that what you are proposing is essentially a zk rollup with decentralized sequencer/validator?

I think the advancement of research and development in this area requires mainly

- Need a zkWASM/zkRISC0 rollup, and gain user adoption
- The current zkEVM rollup to find a suitable “consensus” algorithm and zk network mechanism
- Lower hardware requirements to run an effective prover

---

**bsanchez1998** (2023-04-18):

Using zk-VMS with edge computing architectures in Ethereum to enable end-clients to compute on their devices and submit proofs instead of having execution layer nodes run all the computations is what I think the end state of Ethereum will end up becoming. By having an Edge Computing Interface and making the gas cost dependent on the length of the output variables, you could address the challenge of unbounded computation in WASM.

Do you think integrating this approach into existing smart contract systems could pose challenges or is there a work around? I want to envision developers adapting their smart contracts to work with this Edge Computing Interface but wonder if they need to rewrite their contracts, or could there be a seamless transition?

---

**Wanseob-Lim** (2023-04-19):

FYI, this is also a cross-posted article across the [zkresear.ch forum](https://zkresear.ch/t/an-idea-about-how-to-use-zk-vms-with-the-edge-computing-achitectures-in-ethereum-cross-posted/113)

---

[@longfin](/u/longfin)

> Since we need the previous state for the computation, computation on the edges might be more complex

I agree on this, the most challenging part will be the parallelization of the executions. If we assume there exists a bundler or a sequencer, the batch of the edge computing transactions should have an additional constraints that

“All the execution outputs does not affect each other’s state references.”

Just a quick idea here is that we can express the state reference in the form of polynomial commitment and then add a constraint that all the polynomials does not vanish on the given execution outputs data.

Or, it would be really fun if we can make an homomorphic relationship between \Delta(\text{state ref}) and \Delta(\text{output}) to execute many transactions in parallel.

[@fewwwww](/u/fewwwww)

> the advancement of research and development in this area

Thx for your opinion! This requires a very efficient IVC (incrementally verifiable computation) most of all IMO. And this idea is not only applied for the rollups. When we have a very efficient IVC and prosper dev toolings and other, I think we can consider to put some changes in the Ethereum execution layer supporting this protocol.

[@bsanchez1998](/u/bsanchez1998)

> Do you think integrating this approach into existing smart contract systems could pose challenges or is there a work around?

I guess it’ll take a very long time to get to that stage. Let’s see what happens in the IVC researches for now ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**longfin** (2023-04-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/wanseob-lim/48/5020_2.png) Wanseob-Lim:

> “All the execution outputs does not affect each other’s state references.”

Interesting point. when I shared my thought and concern with my colleagues, they also addressed that as it might be a sort of partitioning problem. ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/wanseob-lim/48/5020_2.png) Wanseob-Lim:

> Or, it would be really fun if we can make an homomorphic relationship between Δ(state ref) and Δ(output) to execute many transactions in parallel.

Agree. but it might be harder than expected if some transactions want to produce unpredictable (even still deterministic) state delta. is there an effective approach for that scenario? or, just is there something I missed in understanding? (especially, I’m not sure that I’ve a complete understanding of “homomorphic relationship” ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=12) )

---

**Wanseob-Lim** (2023-04-21):

I don’t think that we have enough researches about how the state delta will affect its post state delta, but it definitely looks a really interesting topic!

---

**bsanchez1998** (2023-04-21):

I completely agree! I look forward to reading about it.

