---
source: magicians
topic_id: 10044
title: EVM Equivalence (EIP-6269) and Ethereum Stack Compatibility Definition
author: pcaversaccio
date: "2022-07-22"
category: EIPs
tags: [evm]
url: https://ethereum-magicians.org/t/evm-equivalence-eip-6269-and-ethereum-stack-compatibility-definition/10044
views: 2996
likes: 15
posts_count: 10
---

# EVM Equivalence (EIP-6269) and Ethereum Stack Compatibility Definition

In light of the recent zkEVM announcements of various projects and the ongoing discussion & confusion on how **EVM Equivalence** is defined, I propose to create an informational EIP that defines properly **EVM Equivalence** and **Ethereum Stack Compatibility**.

This discussion thread is intended to collect the community’s opinions that will be used to draft an initial EIP.

I will start with my (maybe controversial) opinion on how to define **EVM Equivalence** and **Ethereum Stack Compatibility**:

- EVM Equivalence is complete compliance with the Ethereum yellow paper. Period.
- Ethereum Stack Compatibility = EVM Equivalence + JSON-RPC Compatibility + Node Architecture Compatibility + Design Pattern Compatibility
- Design Pattern Compatibility = Consensus/Execution Client Separation + (… what else should we put here?)

Now it’s your turn - please share your thoughts on my idea about creating an information EIP as well as your thoughts on defining EVM Equivalence and / or Ethereum Stack Compatibility.

### Update 1 (10 January 2023)

I have drafted a first *meta* EIP that defines the term **Full EVM Equivalence**: [Add EIP-6269: Full EVM Equivalence](https://github.com/ethereum/EIPs/pull/6269). This thread however covers still the additional topic with respect to **Ethereum Stack Compatibility** or **Full Ethereum Equivalence**. My aim is still to draft an additional *meta* EIP on **Full Ethereum Equivalence**.

## Replies

**sergio_lerner** (2022-07-28):

I find 2 issues with this definition:

- The yellow paper is not updated at the same time of Ethereum hard-fork activations, so Ethereum can become non EVM-equivalent for some time.
- Even if we define EVM-equivalence in relation with the EIPs that are activated, EVM-equivalent blockchains may activate Ethereum EIPs later than Ethereum, which makes them suddenly non-equivalent.

I prefer EVM-equivalence to be a property of the evolution of a blockchain: it is EVM equivalent if it follows all activated EIPs of Ethereum, even if this is delayed.

---

**sergio_lerner** (2022-07-28):

Most smart contract blockchains are EVM-Stack equivalent and EVM-equivalent with the exception of exact opcode gas costs. I don’t need exact gas costs to consider a blockchain or rollup Ethereum compatible.

Therefore EVM-equivalence definition is not useful.

---

**frangio** (2022-07-28):

Whether equal gas costs are required for EVM equivalence is an important thing to clarify. Defining it as “compliance with yellow paper” or even “compliance with activated EIPs” seems to imply that gas costs should be the same. I think we should explicitly exclude gas costs from the basic definition of “EVM equivalence”, and when desired make it explicit such as “EVM equivalence down to gas costs” or so.

If we’re being truly precise, the cost of an operation is a part of its semantics. The behavior of a contract can definitely change with different opcode pricing, and we’ve seen this happen on Ethereum itself with hard forks. However, that same precedent shows that Ethereum itself doesn’t consider pricing a “core” part of EVM semantics. We should expect smart contract developers to know by now to design their contracts in a way that their semantics are independent of pricing, although I don’t know if we can say that this is always feasible.

Moreover, if we want to truly explore the scalability design space we have to consider that some chains will have entirely different cost models, and this has to be reflected in opcode pricing. For example, there is no reason to think a zkEVM should be priced the same as e.g. geth, given that it runs on a completely different “substrate”.

---

**pcaversaccio** (2022-07-29):

Just as an example (a test contract) where “We should expect smart contract developers to know by now to design their contracts in a way that their semantics are independent of pricing” does not hold: [seaport/ExcessReturnDataRecipient.sol](https://github.com/ProjectOpenSea/seaport/blob/main/contracts/test/ExcessReturnDataRecipient.sol). If memory expansion costs change (even though it hasn’t changed since the release of the Yellow Paper) there will be a problem.

Generally, with the release of Huff language and further low-level initiatives, I feel that the smart contract semantics will be dependent to a certain extent at least on the specific pricing (whether this is good or not is another question). So if we take the EVM running on Ethereum as the benchmark and the semantics can depend on the pricing, we should probably include the gas costs into the definition of **EVM Equivalence**.

For the scalability design space, where gas costs are not the same by design, we could define it as **EVM Adherence**.

---

**gcolvin** (2022-09-05):

Gas costs *have* to be able to change, as if they are too far off they are become an attack vector.  And whether they are an attack vector depends, as [@frangio](/u/frangio) puts it, on the “substrate”.  Some systems systems might not need gas at all.

---

**david** (2022-12-27):

Right now, the most popular classification of different types of zkEVMs is probably Vitalik’s August blog post:

https://vitalik.ca/general/2022/08/04/zkevm.html

Perhaps an EIP could enshrine this 4-tier classification system with additional technical defintions?

---

**pcaversaccio** (2023-01-07):

I have drafted a first meta EIP that defines the term “Full EVM Equivalence”: [Add EIP-6269: Full EVM Equivalence](https://github.com/ethereum/EIPs/pull/6269).

---

**protolambda** (2023-01-07):

Feedback on the EIP draft:

Do you intent to capture the meaning of the whole EL, or just the EVM? From this magicians post I see you also mention “Ethereum Stack compatibility”, but the EIP completely ignores that.

The Ethereum Execution Layer as defined in the execution specs encompasses *more* than just the EVM. It includes the EVM as one of its main features.

The **transaction-types** are not strictly part of the EVM. In go-ethereum for example the transaction-types are abstracted into a generic `Message` before being [applied](https://github.com/ethereum/go-ethereum/blob/2189773093b2fe6d161b6477589f964470ff5bce/core/state_transition.go#L185) to the EVM, and no tx-typing can be introspected by the EVM.

Yet, the equivalence of **tx-encoding** and **signing** with L1 mainnet is still a requirement for a significant part of existing ethereum tooling to work out of the box on alternative networks, something some ZK rollups that claim EVM-equivalence don’t support. This is worth highlighting in the EIP.

Another part that’s not technically “EVM” but definitely part of the EL specs is the **state-trie-format**: L1 uses an account model backed by a Merkle-Patricia-Trie. Is this part of EVM equivalence? Probably not, but by just pointing at the EL specs it appears as if it is. And many ZK-rollups choose an alternative ZK-friendly state format anyway. And mainnet L1 may change it in the next few years to Verkle trees.

And although event-logs are part of the EVM, **tx-receipts** are not; they are part of the EL storage format and only referenced in the block-header. Are these included in EVM equivalence?

And then comes the **execution-layer RPC APIs**, which are an expectation around the EL and specified too: [GitHub - ethereum/execution-apis: Collection of APIs provided by Ethereum execution layer clients](https://github.com/ethereum/execution-apis/) Are these part of EVM equivalence? I would say no, but also worth calling out, as again *A LOT* of tooling depends on these, and this includes EVM-traces!

I would define “EVM equivalence” as conformance to the processing of a single abstracted transaction onto an abstracted accounts-state and conforming to *all* mainnet L1 EVM features: EVM-context (memory, callstack, stack, gas, etc.), instructions and precompiles.

And a mention of the origin of the term “EVM equivalence” would be appropriate: it’s was not the ZK-EVMs who first popularized the meaning. Optimism has posted about the difference with “EVM compatibility” and “EVM equivalence” as early as in Sept 17 2021: [The Future of Optimistic Ethereum | by Optimism | Optimism PBC Blog | Medium](https://medium.com/ethereum-optimism/the-future-of-optimistic-ethereum-7f22d987331) and described it as “By precisely enforcing the [Ethereum Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf)” (which at the time of the post was more of a canonical source for EVM spec, this was pre-Merge and pre-EL-specs readiness). And Optimism then introduced it in more detail on Oct 26 2021: [Introducing EVM Equivalence. Or, Ethereum All the Way Down: How We… | by Optimism | Optimism PBC Blog | Medium](https://medium.com/ethereum-optimism/introducing-evm-equivalence-5c2021deb306) and followed up with an upgrade end 2021 dedicated to these described changes.

L2 users expect tx-typing & state format & receipts & RPCs to also be there, so I support the definition of something like “Ethereum Stack Compatibility”, although it definitely needs more detail. Does this include consensus part of the stack with proof-of-stake? That too has formatted blocks, state, APIs, etc.

And FWIW, Optimism is nearing its launch of Bedrock, which will go far beyond EVM-equivalance to fully include all of these non-EVM Ethereum features, by using the Engine API and almost using Geth as-is, with the exception of minor additions to function as a rollup at all (deposit-tx type, payment for L1-data usage, and ability to reproduce exact blocks from inputs only with engine API). And with multi-client support planned as well (already have an Erigon prototype). By using this API and Geth and other clients with so few modifications, you could maybe even call it “ethereum stack equivalence” instead of just “ethereum stack compatibility” ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

---

**pcaversaccio** (2023-01-09):

[@protolambda](/u/protolambda) appreciate your extended feedback. Let me try to address your points separately:

> Do you intent to capture the meaning of the whole EL, or just the EVM? From this magicians post I see you also mention “Ethereum Stack compatibility”, but the EIP completely ignores that.

The short answer is yes. The long answer is this: I’ve been watching these (marketing) battles between you guys at Optimism and other projects like Polygon zkEVM for some time now, and I’m convinced that someone impartial (in this case me) should write an EIP on how **Full EVM Equivalence** and possibly **Full Ethereum Equivalence** is defined. When I started this discussion 6 months ago, I thought I would put both terms in one EIP, but after careful thought, I decided to split these two topics into two EIPs for simplicity. I now started with the first EIP on **Full EVM Equivalence**. So having this discussion in one thread is more of a legacy issue, but I don’t see any problems with addressing it here. **Edit:** I updated the description of this thread to reflect the concern accordingly.

> Yet, the equivalence of tx-encoding and signing with L1 mainnet is still a requirement for a significant part of existing ethereum tooling to work out of the box on alternative networks, something some ZK rollups that claim EVM-equivalence don’t support. This is worth highlighting in the EIP.
>
>
> Another part that’s not technically “EVM” but definitely part of the EL specs is the state-trie-format: L1 uses an account model backed by a Merkle-Patricia-Trie. Is this part of EVM equivalence? Probably not, but by just pointing at the EL specs it appears as if it is. And many ZK-rollups choose an alternative ZK-friendly state format anyway. And mainnet L1 may change it in the next few years to Verkle trees.
>
>
> And although event-logs are part of the EVM, tx-receipts are not; they are part of the EL storage format and only referenced in the block-header. Are these included in EVM equivalence?
>
>
> And then comes the execution-layer RPC APIs, which are an expectation around the EL and specified too: GitHub - ethereum/execution-apis: Collection of APIs provided by Ethereum execution layer clients Are these part of EVM equivalence? I would say no, but also worth calling out, as again A LOT of tooling depends on these, and this includes EVM-traces!
>
>
> I would define “EVM equivalence” as conformance to the processing of a single abstracted transaction onto an abstracted accounts-state and conforming to all mainnet L1 EVM features: EVM-context (memory, callstack, stack, gas, etc.), instructions and precompiles.

Those are all very valid points and worth discussing. So here is some background: What I understand is that the [Ethereum Execution Client Specifications](https://github.com/ethereum/execution-specs) is a superset of the [Ethereum Yellow Paper](https://github.com/ethereum/yellowpaper/blob/1016c0603062b76388e3c3c19786cd5f9ca9ac61/paper.pdf). In my first draft version of the EIP I was **only** referring to the Ethereum Yellow Paper. Because how I see it is that **Full EVM Equivalence** is the **complete** compliance with the latest version of the Ethereum Yellow Paper. Full stop. However, as [@matt](/u/matt) pointed out [here](https://github.com/ethereum/EIPs/pull/6269#issuecomment-1373819342), the Yellow Paper is considered a deprecated source and I should please refer to the [execution-specs](https://github.com/ethereum/execution-specs) repository for the latest definitions of the EVM. That’s why [@Pandapip1](/u/pandapip1) changed the reference to the [execution-specs](https://github.com/ethereum/execution-specs) in this commit [da87c92](https://github.com/ethereum/EIPs/pull/6269/commits/da87c922b6ccfcb5033e23fe29c946e0ac1f994f). I believe the discussion points to the question what reference is the single source of truth. IMHO it’s the latest version of the Ethereum Yellow Paper, and if this is located in the [execution-specs](https://github.com/ethereum/execution-specs) repository, we have to link it of course. Now the natural problem arises what does the repository cover more than the Ethereum Yellow Paper (you correctly mentioned the examples of **transaction-types** or the **state-trie-format** and there are even further specs that could be included there as well) and what do we need to exclude? I feel that this approach will lead to never-ending circles of discussion. I feel more that we should agree on the fact whether the [Ethereum Execution Client Specifications](https://github.com/ethereum/execution-specs) should be considered as the new **complete** reference for the EVM (even though this goes beyond the original definition of the EVM we know from the Yellow Paper). I strongly support this notion since the EIP is written in a completely backward-compatible way where I define the change of the single source of truth at the Bellatrix hard fork date.

> And a mention of the origin of the term “EVM equivalence” would be appropriate: it’s was not the ZK-EVMs who first popularized the meaning. Optimism has posted about the difference with “EVM compatibility” and “EVM equivalence” as early as in Sept 17 2021: The Future of Optimistic Ethereum | by Optimism | Optimism PBC Blog | Medium and described it as “By precisely enforcing the Ethereum Yellow Paper” (which at the time of the post was more of a canonical source for EVM spec, this was pre-Merge and pre-EL-specs readiness). And Optimism then introduced it in more detail on Oct 26 2021: Introducing EVM Equivalence. Or, Ethereum All the Way Down: How We… | by Optimism | Optimism PBC Blog | Medium and followed up with an upgrade end 2021 dedicated to these described changes.

While I understand your motivation, I don’t think an EIP is a place to name-drop a project (that’s why I didn’t mention specific projects in the draft EIP). It is always a matter of debate as to what the exact origin is. I would like to keep this EIP unbiased and therefore do not support such an addendum.

> L2 users expect tx-typing & state format & receipts & RPCs to also be there, so I support the definition of something like “Ethereum Stack Compatibility”, although it definitely needs more detail. Does this include consensus part of the stack with proof-of-stake? That too has formatted blocks, state, APIs, etc.

IMHO **Full Ethereum Equivalence** involves definitely the consensus part. But for this part, I haven’t drafted the EIP yet, but I keep you posted on this.

