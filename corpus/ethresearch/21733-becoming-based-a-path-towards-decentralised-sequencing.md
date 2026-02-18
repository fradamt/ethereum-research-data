---
source: ethresearch
topic_id: 21733
title: "Becoming Based: A Path towards Decentralised Sequencing"
author: kubimens
date: "2025-02-12"
category: Layer 2
tags: [preconfirmations, based-sequencing, sequencing]
url: https://ethresear.ch/t/becoming-based-a-path-towards-decentralised-sequencing/21733
views: 3376
likes: 48
posts_count: 14
---

# Becoming Based: A Path towards Decentralised Sequencing

*Co-authored by Lorenzo and [Kubi](https://x.com/kubimensah) from [Gattaca](https://x.com/gattacahq). Special thanks to [Justin](https://x.com/drakefjustin), [Drew](https://x.com/DrewVdW), [Jason](https://x.com/jasnoodle), [Ladi](https://x.com/ladislaus0x), [Connor](https://x.com/conormcmenamin9),  [Liam](https://x.com/liamihorne), [Sam B](https://x.com/sam_battenally), [Matthew](https://x.com/mteamisloading), [Lin](https://x.com/linoscope), [Brecht](https://x.com/Brechtpd), [Can](https://x.com/kisaguncan), [Thanh](https://x.com/hai_rise), [Kevin](https://x.com/lepsoe) and [Sam J](https://x.com/sjerniganIV) for their feedback and suggestions. Feedback is not necessarily an endorsement.*

**Prerequisite:** This article assumes familiarity with concepts such as: [based rollups](https://ethresear.ch/t/based-rollups-superpowers-from-l1-sequencing/15016), [preconfirmations](https://ethresear.ch/t/based-preconfirmations/17353) and [PBS](https://ethereum.org/en/roadmap/pbs/)

# Setting the Context

This article provides a practical roadmap for rollups currently operating a centralised sequencer at scale to progressively transition into *based* rollups.

To demonstrate how this transition can be achieved, the article first outlines a design for based sequencing, followed by an explanation of how parts of the design can be gradually adopted to enable the transition.

While several approaches have been proposed to leverage L1 proposers for sequencing services, such as free-for-all ([total anarchy](https://vitalik.eth.limo/general/2021/01/05/rollup.html)) and [vanilla based sequencing](https://ethresear.ch/t/vanilla-based-sequencing/19379), the design outlined in this article builds on an approach where L1 proposers delegate sequencing rights to  specialised 3rd parties called *gateways*. This concept was initially discussed in [“Based Preconfirmations”](https://ethresear.ch/t/based-preconfirmations/17353) and [“Vanilla Based Sequencing”](https://ethresear.ch/t/vanilla-based-sequencing/19379), and seeks to [avoid overloading validators](https://streameth.org/zuberlin/watch?session=666af08807f92b086c2c2e54).

The outlined design also incorporates ongoing [standardisation efforts](https://github.com/eth-fabric) around based preconfirmations and assumes the existence of an [open-source public-good “sidecar”](https://ethresear.ch/t/commit-boost-proposer-platform-to-safely-make-commitments/20107) that enables opt-in delegation. It further leverages existing low-latency Proposer-Builder Separation ([PBS](https://ethereum.org/en/roadmap/pbs/)) infrastructure for efficient L1 inclusion and settlement of batches. Together, these elements enable rollups to adopt based sequencing immediately, without the need for L1 protocol-level changes or hard forks.

Finally, some of the mechanics were inspired by collaborative efforts with teams such as [Taiko](https://taiko.xyz/), [Puffer UniFi](https://www.puffer.fi/unifi) , [Rise](https://www.riselabs.xyz/), [Spire](https://www.spire.dev/) and many others.

# TLDR

- Rollups can progressively decentralise and become based rollups by replacing their centralised sequencer with the most credibly neutral actors: the L1 validator set.
- This transition can occur in phases, enabling a gradual and robust path towards decentralisation.
- A practical first step would be to overlay preconfirmations - guarantees from the sequencer before an L2 block is published - on centralised sequencing. This can provide close to ping-latency UX and maintains forward-compatibility with permissionless based sequencing.
- By becoming based, rollups achieve stronger alignment with Ethereum. Moreover, by adopting a delegation model involving gateways in a competitive marketplace, they can also unlock significant performance improvements in throughput and processing speed.
- Mechanisms such as preconfirmations and pipelining block construction enable execution proofs on the order of tens of milliseconds.
- Rollups can adopt a pragmatic, incremental, three-phase approach to decentralisation, improving sequencer resilience and performance at each step. This is especially important for large-scale rollup operators managing ecosystems with substantial TVL and user bases, as it offers tangible incentives to adopt based sequencing while mitigating the risks of a major systemic overhaul.

# How this Article is structured

We begin with a Background discussion, examining the state of rollups and the challenges posed by centralised sequencers. Next, we highlight the Key Benefits of Based Sequencing, outlining how the Ethereum L1 proposer set can offer stronger resilience, composability, and economic security when sequencing rollups.

We then define Terminology to ensure clarity when discussing the key roles and mechanics of our proposed design. After that, we present a Based Sequencing Design Using Delegation, outlining the technical details and core mechanisms that form the foundation for a gradual adoption roadmap.

Finally, in Becoming Based, we provide a three-phase roadmap showing how rollup operators can progressively adopt parts of the proposed design to transition from a centralised sequencer model to fully permissionless based sequencing. After describing potential Risks, including centralisation concerns and UX variations, we conclude with Further Considerations, identifying areas that call for ongoing research and refinement.

# Background

Current state of rollups:

- Users currently enjoy an excellent UX, enabled by preconfirmations issued with low latency by centralised sequencers.
- By holding the exclusive right to sequence and batch transactions, centralised sequencers can give guarantees about the execution of these transactions.
- Rollups avoid the overhead of consensus mechanisms, unlocking a design space that can achieve exceptionally high levels of performance and throughput. Currently, most rollups rely on centralised sequencers that operate solely on a trust basis, raising concerns about censorship resistance and liveness. While some rollups include an “escape hatch” mechanism, it often comes at the cost of degraded user experience due to significant delays.

Why *Based* sequencing can improve rollups:

- Based sequencing enables Ethereum L1 proposers, the most decentralised and credibly neutral set of actors, to provide sequencing services for rollups. This enables shared sequencing across multiple rollups and, in turn, synchronous composability across the rollups and between the rollups and L1.
- Preconfirmations backed by economic guarantees can mitigate the delays caused by long L1 slot times. This ensures L2 users maintain an excellent UX while benefiting from enhanced economic security and mitigate risks such as liveness failures or regulatory challenges posed by centralised sequencers.

The importance of delegation:

- For based sequencing to fully leverage the L1 proposer set, all proposers, including solo stakers, must be able to opt in and participate. Inclusivity ensures equitable access to yield, which is critical for maintaining decentralisation of the L1 proposer set. In alignment with PBS and research such as APS, the research efforts around based sequencing have generally introduced a role referred to as a “Gateway.”
- Gateways, staked third-party entities providing specialised sequencing services, will be available to proposers lacking bandwidth and technical capacity to support high-throughput rollups. Gateways are held accountable through strict performance monitoring and are subject to slashing conditions, ensuring reliability and alignment with the network’s security guarantees. Nonetheless, delegating sequencing services to gateways introduces additional risks, which are discussed later in this article.

We strongly believe that, with a robust mechanism design, *based* sequencing should become the default choice for rollups. It leverages Ethereum’s economic security, reliability, and neutrality. Moreover, in based sequencing designs that adopt a delegation model and foster a competitive market among specialised gateways, rollups can achieve superior performance enabling them to meet the high-throughput demands users expect.

# Key Benefits of Based Sequencing

- High Performance with Decentralised Sequencing: Optimised block pipelining and efficient gossiping enable execution preconfirmations within just a few milliseconds. This level of performance has been demonstrated with pipelined sequencers, achieving 300,000 transactions per second, or approximately 6 gigagas per second on a consumer-grade laptop using a single core for sequencing.
- Enhanced Liveness and Resilience through Decentralisation: Sequencing becomes significantly more robust and fault-tolerant with multiple gateways, compared to reliance on a single centralised sequencer. The system can automatically recover from temporary liveness failures, ensuring continuous operation without the need for manual intervention.
- Retention of Control over MEV and Priority Fees: Rollup operators maintain full control over sequencing rules, MEV management, and fee attribution. This flexibility allows operators to fine-tune incentives and penalties to meet specific performance and economic goals.
- Alignment with Ethereum L1: Based sequencing leverages the Ethereum L1 proposer set as watchdogs to enhance security, ensure credible neutrality, and enable seamless composability with Ethereum L1.
- A Scalable Ecosystem of Rollups: Based sequencing provides a realistic and scalable path to synchronous composability with Ethereum L1, laying the foundation for a seamlessly interconnected ecosystem of rollups.

|  | Centralised Sequencing | Based Sequencing |
| --- | --- | --- |
| Performance | Excellent | Excellent - Gateways |
| Liveness | Single Point of Failure | Excellent - L1 proposers + Gateways |
| Economic Security | None | Excellent - Staked Proposers + Gateways |
| Real-time Censorship Resistance | Single Point of Failure | Excellent - L1 proposers |
| Composability | Limited | Excellent - Synchronous |

# Terminology

- Gateway: The entity responsible for issuing preconfirmations and sequencing the L2. Sophisticated L1 proposers may choose to operate their own gateways, while others can delegate sequencing responsibilities to third-party operators. For simplicity, we refer to all sequencing entities as gateways, with the understanding that proposers may self-delegate.
- Nodes: Non-sequencing follower nodes that track the tip of the chain by listening to sequenced transaction batches. These nodes are essential for tasks such as submitting fraud proofs, indexing, handling RPC calls, and supporting other off-chain services.
- Lookahead: A mapping from L1 slots to gateway identities, establishing the leader schedule for sequencers.
- Inbox Contract: An L1 contract where transaction batches from the L2 are posted.
- Frags: Fragments of a block that the leader shares with follower nodes before the block is fully constructed. This concept is similar to shreds in Solana and has been frequently discussed in Sequencing and Preconfirmations calls (eg #13).

## Confirmation Levels for a given L2 Transaction

We define **three levels of confirmation**:

1. Preconfirmed: The transaction is sequenced by a gateway, and an execution receipt is available to the user.
2. Included: The transaction is included in an L2 block.
3. Finalised: The L2 block containing the transaction has been batched and included in an L1 block.

**Note:** Even after being finalised, the L1 block may still be subject to reorgs, however reorging L2 blocks can be avoided by [chaining preconfirmations](https://ethresear.ch/t/avoiding-accidental-liveness-faults-for-based-preconfs/19888).

# Based sequencing design using delegation

The **lookahead** (as shown in the table below) serves as a leader schedule for sequencers, mapping L1 slot numbers to leader **gateways**. These gateways act as sequencers with exclusive rights to advance the L2 state during their assigned slots. Slot assignments are determined by L1 proposers who opt in to become sequencers, granting them sequencing rights during their respective L1 slot durations. If no L1 proposer has opted in for one or more slots, the sequencing rights for those slots are assigned to the next available proposer who has opted in.

| Gateway | L1 Slots |
| --- | --- |
| Gateway A | 100-102 |
| Gateway B | 103-105 |
| Gateway C | 106-108 |

Alternative methods for establishing a gateway schedule may also be considered. The assignment could take into account factors such as the proportional stake delegated to each gateway by L1 proposers to ensure fair representation across the proposer set. To further promote decentralisation and prevent monopolisation, a hard upper limit could be imposed on the number of consecutive slots a single gateway is allowed to sequence.

Finally, the inbox contract enforces this schedule by accepting transaction batches only from the designated gateway leader for each slot, as defined by the lookahead.

## Gateway and Node Connectivity

Gateways and nodes communicate via a fast, leader-aware peer-to-peer (p2p) gossip network, inspired by the Solana [Turbine](https://www.helius.dev/blog/turbine-block-propagation-on-solana) block propagation. This network plays a critical role in maintaining efficient and reliable communication and serves two primary purposes:

1. Inbound Gossip: Transactions are relayed from nodes to the current gateway leader for sequencing.
2. Outbound Gossip: The gateway leader distributes sequenced transaction batches back to nodes and the next leader in the lookahead schedule.

[![image](https://ethresear.ch/uploads/default/optimized/3X/2/2/220606b0249e52943c7ecddad7a8ea0cb66251cb_2_690x312.jpeg)image1896×860 98 KB](https://ethresear.ch/uploads/default/220606b0249e52943c7ecddad7a8ea0cb66251cb)

Users can send transactions directly to the current gateway leader or to any node, which then forwards transactions received via Inbound Gossip. The leader sequences these transactions and distributes the resulting frags via Outbound Gossip through the p2p network. It is important to note that these frags are signed (committed to) by the gateway leader. This streamlined block construction process allows nodes to begin rebuilding the current block immediately, rather than waiting for the entire block to be finalised, as is the case in Ethereum today.

```auto
struct Frag {
    // Block in which this frag will be included
    block_number: u64,
    // Index of this frag. Frags need to be applied sequentially by index
    seq: u64,
    // Whether this is the last frag in the sequence
    is_last: bool,
    // Ordered list of EIP-2718 encoded transactions
    txs: Transactions,
}
```

As peer nodes receive batches, they optimistically construct a local `TempBlock` and provide preconfirmations (execution receipts) to users. This is possible because nodes validate batches based on the current lookahead and the latest L2 block number posted on the L1, rejecting any batches not signed by the current leader.

[![](https://ethresear.ch/uploads/default/optimized/3X/2/9/2961a192d5384aa5516c33e8983d8bbeb0422546_2_413x500.png)907×1097 55.7 KB](https://ethresear.ch/uploads/default/2961a192d5384aa5516c33e8983d8bbeb0422546)

Nodes also monitor the sequencing performance and responsiveness of the gateway leader. If a node misses any sequential batches, it can request the missing data from other nodes within the p2p network.

[![image](https://ethresear.ch/uploads/default/optimized/3X/1/3/134a13b4335fee820f93a4943f1cfea4dacdb687_2_690x285.jpeg)image1695×701 84.7 KB](https://ethresear.ch/uploads/default/134a13b4335fee820f93a4943f1cfea4dacdb687)

New Nodes can join the network permissionlessly and independently reconstruct the gateway schedule by reading the lookahead data directly from the L1. This ensures that the network remains open and transparent, eliminating reliance on centralised RPC providers to issue preconfirmations. To support off-chain components such as wallets, indexers, and other services, nodes also expose a standard **JSON-RPC API**, enabling seamless integration and compatibility with existing infrastructure.

The size and frequency of frags can be adjusted by the rollup operator, balancing trade-offs between performance, hardware requirements and throughput. At the limit, where frags contain a single transaction and are streamed continuously, a user connected directly to the gateway leader can receive an execution preconfirmation within just a few milliseconds. This efficiency is achievable because L2s inherit security guarantees from the L1, removing the need for additional consensus overhead.

Periodically, the gateway leader broadcasts a **block seal**, consolidating a set of frags into a single L2 block, thereby advancing the tip of the chain.

```auto
struct Seal {
    // How many frags for this block were in this sequence
    total_frags: u64,
    // Header fields
    block_number: u64,
    gas_used: u64,
    gas_limit: u64,
    ...
}
```

To ensure a smooth transition between leaders, the current gateway also broadcasts an `EndOfSequence` message, signaling to the next gateway and nodes that sequencing rights can safely transfer. This approach minimises “dead times” when no sequencer is active, avoiding unnecessary reliance on L1 settlement during transitions.

```auto
struct EndOfSequence {
   // Last block sequenced
   block_number: u64,
   // Hash of last block
   block_hash: B256,
}
```

If the current gateway fails to broadcast the `EndOfSequence` message, the next gateway must fall back to waiting for the L1 to settle, preventing any risk of conflicting L2 transactions.

## L1 Settlement and Slashing

Even though the chain tip advances optimistically, each gateway is responsible for ensuring that batches of L2 blocks are settled on the L1 according to the schedule in the lookahead. Gateways and proposers must post collateral in the registry contract and are subject to slashing under certain conditions, including:

- Reneging on preconfirmations,
- Failing to settle batches on the L1,
- Missing assigned slots.

Notably, proposers may also face slashing penalties if the gateway they have delegated to is slashed. This creates a strong alignment of incentives between proposers and gateways, reinforcing the responsibility of proposers to monitor and carefully select the gateways. In return, proposers earn additional yield, which compensates for the risks associated with delegation.

The exact conditions for attribution and slashing fall outside the scope of this document but remain an important area for further specification.

## Fallback Mechanism

A liveness failure by a gateway results in a temporary “blackout,” during which users are unable to settle transactions, and the rollup is unable to progress. Failures in single centralised sequencers can result in hours-long disruptions, however a *based* rollup with multiple sequencers can recover within a few L1 slots.

In practice, a blackout caused by a faulty gateway would typically last only a short time, such as two L1 slots. The faulty gateway can be penalised by slashing its collateral and reducing its sequencing slots in future lookaheads. For instance, if `GatewayA` is the current leader as per the lookahead up to `Slot N`, but fails to post a Batch after the slot has passed, `GatewayA` can be slashed and temporarily excluded from the sequencing schedule.

This fallback mechanism ensures that even in the event of a gateway failure, the system remains resilient, minimising disruption and incentivising reliable performance from all gateways.

**Note:** Liveness failures can originate with either the gateway or the proposer, so we need a robust way to detect and penalise both scenarios. If the proposer is at fault, enforcing accountability may require an off-chain process, which conflicts with a truly trust-minimised approach. Designing a mechanism that can reliably attribute proposer-induced liveness failures, and penalise them, remains an open challenge.

## Proposers and Gateways

The ability to delegate sequencing responsibilities to third parties allows unsophisticated proposers, who may lack  bandwidth or the technical expertise required to run a gateway, to participate effectively. This delegation mechanism fosters a more equitable and inclusive market while introducing competitive pressure on gateway operators to provide higher-quality sequencing services.

Although similar in spirit to Proposer-Builder Separation (PBS), where validators delegate block-building to specialised third-party actors, *based* sequencing ensures that proposers retain control and oversight over their delegates. This is achieved through slashing  gateways for safety faults and proposers for liveness faults. If the liveness fault is not caused by the proposer, it is expected that proposers will seek compensation from gateways via off-chain mechanisms.

Proposers act as “watchdogs,” monitoring the performance of gateways by tracking key metrics and incentivising reliability and efficiency. This alignment of incentives ensures that delegation does not compromise the security or robustness of the system.

## Retention of Control over MEV and Priority Fees

Rollup operators retain full control over sequencing rules, priority fees, and MEV management. Gateways are required to operate in compliance with the rollup’s established policies. This is initially enforced by limiting participation to permissioned gateways until more robust mechanisms are available for fully permissionless participation.

Proposers earn a share of the fees as compensation for their indirect sequencing services and, in turn, allocate a portion of these fees to gateways based on their performance and reliability. This arrangement creates a virtuous cycle, incentivising gateways to deliver high-quality services while ensuring a fair distribution of rewards across the system.

The distribution of fees among proposers, gateways, and the rollup operator is determined at the discretion of the rollup operator, allowing flexibility to align with the rollup’s economic and operational goals.

# Becoming Based

Achieving fully permissionless, *based* sequencing is the ultimate goal. However, we recognise that rollups starting with centralised sequencers may adopt a gradual, 3-phase approach to decentralisation. This framework allows for a progressive transition to *based* sequencing while minimising risks and ensuring operational stability.

## Phase 1: Initial Deployment

In this phase, the leader-aware gossip protocol is deployed and integrated with a single gateway functioning as a centralised sequencer. This enables nodes to receive fast preconfirmations regardless of the L2 block time. A registry contract is introduced to lay the foundation for a sequencer set, initially comprising only one entity.

For added robustness, a fallback mechanism leveraging the existing rollup stack is also implemented.

## Phase 2: Additional Gateway Introduction

Gateways are progressively incorporated into the lookahead schedule. At this stage, gateways are still operated by the rollup operator and/or pre-approved third parties. The gossip network becomes fully operational, enabling transaction forwarding and the streaming of sequenced batches. While gateways operate under **SLA-like agreements** with the rollup operator, slashing mechanisms are not yet enabled.

## Phase 3: Permissionless Sequencing

Gateways can now permissionlessly join the sequencer set, and proposers are able to delegate sequencing responsibilities to gateways. Proposers are expected to monitor the performance and reliability of their delegates. At this stage, slashing mechanisms are activated to address safety and liveness faults.

However, several considerations, such as fault attribution and front-running prevention, must be addressed to ensure the system’s robustness before reaching this stage.

# Risks

- Centralisation Risk: If the majority of proposers delegate to a small number of gateways, it could result in an oligopolistic sequencing market. Nevertheless, as long as more than one active gateway exists, this model remains a significant improvement over the centralised status quo. Furthermore, gateways are staked actors subject to slashing conditions and are held accountable by L1 proposers, ensuring decentralised oversight.
- Inconsistent User Experience: A rotating set of distributed sequencers may introduce variability in user experience compared to a centralised sequencer. To mitigate this, a temporary whitelist of gateway operators under SLA-like agreements can be employed to provide more consistent performance during the transition phases.
- Dependency on Rollup Operator: During Phases 1 and 2, the sequencer set is not fully permissionless and remains reliant on the rollup operator. This “training wheels” approach is necessary to ensure stability but introduces some centralisation during the early stages.

# Further Considerations

Several topics require further discussion and detailed specification:

- The design and implementation of the registry contract.
- Collateral requirements for gateways and proposers.
- The definition of exact slashing conditions.

For Phase 3 (permissionless gateways), the following open questions remain:

- How to prevent front-running by malicious leaders.
- Determining fault attribution between proposers and gateways in cases of missed proposals.
- Establishing effective performance monitoring and addressing the fair exchange problem.

We are eager to work with protocol researchers, developers, rollup operators and other teams in the ecosystem to join in refining these open questions and shaping a secure, high-performance future for based sequencing. By collaborating on the outstanding design details and testing solutions in real-world settings, we can work together to build a more robust, permissionlessly sequenced rollup ecosystem.

## Replies

**MCarlomagno** (2025-02-13):

Thanks! Love the ideas, I’m just a bit skeptical about rollups reaching phase 3 considering they will leave significant MEV revenue to Gateways/Validators, do you Invision some mechanism in which they transition to phase 3 without losing revenue?

---

**thegaram33** (2025-02-13):

Great writeup! Just two notes.

![](https://ethresear.ch/user_avatar/ethresear.ch/kubimens/48/18593_2.png) kubimens:

> Economic Security  None  Excellent - Staked Proposers + Gateways

I don’t think “None” is accurate here, you could still require a bond/stake from the centralized sequencer and use it for equivocation protection. This way centralized sequencer preconfs would have some economic security (not just backed by reputation).

![](https://ethresear.ch/user_avatar/ethresear.ch/kubimens/48/18593_2.png) kubimens:

> Gateways can now permissionlessly join the sequencer set, and proposers are able to delegate sequencing responsibilities to gateways.

An important prerequisite of permissionless sequencing is that we have a mechanism to deal with *invalid batches*, i.e. batches that the rollup’s state transition function cannot interpret / execute. I think there are two main ways to deal with these:

1. Eliminate invalid batches: Make the STF infallible, i.e. it can process any data, even garbage (most likely resulting in a no-op, or an empty L2 block).
2. Revert invalid batches: Have a mechanism to identify and revert/ignore invalid batches. This can be a validity proof (essentially proof of invalidity), or some majority vote of staked participants.

---

**bertmiller** (2025-02-13):

Thanks for the post, interesting design!

Quick question about:

![](https://ethresear.ch/user_avatar/ethresear.ch/kubimens/48/18593_2.png) kubimens:

> High Performance with Decentralised Sequencing: Optimised block pipelining and efficient gossiping enable execution preconfirmations within just a few milliseconds. This level of performance has been demonstrated with pipelined sequencers , achieving 300,000 transactions per second, or approximately 6 gigagas per second on a consumer-grade laptop using a single core for sequencing.

Is this 6 gigagas per second only for sequencing? Or were you able to get full nodes to keep up a 6 gigagas per second too? Because I imagine the bottleneck isn’t going to be the sequencer.

---

**kubimens** (2025-02-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/mcarlomagno/48/18816_2.png) MCarlomagno:

> Thanks! Love the ideas, I’m just a bit skeptical about rollups reaching phase 3 considering they will leave significant MEV revenue to Gateways/Validators, do you Invision some mechanism in which they transition to phase 3 without losing revenue?

Yes, there are still many open design questions once rollups transition to Phase 3, including mechanisms for enforcing MEV and fee distribution policies!

---

**kubimens** (2025-02-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/thegaram33/48/13742_2.png) thegaram33:

> I don’t think “None” is accurate here, you could still require a bond/stake from the centralized sequencer and use it for equivocation protection. This way centralized sequencer preconfs would have some economic security (not just backed by reputation).

Good point!

![](https://ethresear.ch/user_avatar/ethresear.ch/thegaram33/48/13742_2.png) thegaram33:

> An important prerequisite of permissionless sequencing is that we have a mechanism to deal with invalid batches, i.e. batches that the rollup’s state transition function cannot interpret / execute. I think there are two main ways to deal with these:
>
>
> Eliminate invalid batches: Make the STF infallible, i.e. it can process any data, even garbage (most likely resulting in a no-op, or an empty L2 block).
> Revert invalid batches: Have a mechanism to identify and revert/ignore invalid batches. This can be a validity proof (essentially proof of invalidity), or some majority vote of staked participants.

Yes, 1 is similar to Taiko’s current design: if invalid transaction batches are posted to the inbox contract, they’re simply “skipped.”

---

**kubimens** (2025-02-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/bertmiller/48/10408_2.png) bertmiller:

> Is this 6 gigagas per second only for sequencing? Or were you able to get full nodes to keep up a 6 gigagas per second too? Because I imagine the bottleneck isn’t going to be the sequencer.

Yes, 6 gigagas per second here is for sequencing and root computation. We fully anticipate that sync and DA will become the bottleneck. This is where block pipelining and frag gossiping can help nodes keep up with the tip of the chain. Benchmarks coming soon!

---

**irfanshaik11** (2025-02-14):

Fantastic article, design, and implementation. Docs here are also super detailed: [based-op/based at main · gattaca-com/based-op · GitHub](https://github.com/gattaca-com/based-op/tree/main/based)

---

**evchip** (2025-02-16):

Great writeup! Something I’m unclear on:

![](https://ethresear.ch/user_avatar/ethresear.ch/kubimens/48/18593_2.png) kubimens:

> Rollup operators maintain full control over sequencing rules, MEV management, and fee attribution

How can rollup operators guarantee that gateways abide by these rules if the rules are not explicitly enforced in the L1 inbox contract? For instance, if a gateway decides to reorder transactions to extract MEV against the wishes of the rollup operator, where in the pipeline can this be detected?

---

**hyeonleee** (2025-02-17):

Thanks for this post—it really helped me understand the landscape of decentralized rollup environments. Could you provide an example scenario to illustrate this case further?

![](https://ethresear.ch/user_avatar/ethresear.ch/kubimens/48/18593_2.png) kubimens:

> Notably, proposers may also face slashing penalties if the gateway they have delegated to is slashed.

---

**otrsk** (2025-03-18):

I think it unfortunately can’t, fundamentally. This open area item seems to refer to a subset of this:

> How to prevent front-running by malicious leaders.

---

**kladkogex** (2025-04-09):

Well, I think this will make rollups as slow as the current mainnet - probably the finalization time will go to 30 sec.

So it is unusable from user perspective. If you look at Base and at Solana, the finalization time can be less than a second.

---

**otrsk** (2025-04-10):

Based rollups rely on preconfs for ux, not on mainnet block times, let alone finalisation. Btw current mainnet chain finalisation delay is more like 10 minutes.

---

**kladkogex** (2025-04-11):

Well, I respectfully disagree — I think users do care about security. But if you’re paying with this thing at a coffee shop, you can wait one second max. People pay and leave. The coffee shop owner won’t let you leave until it’s finalized.

You can already pay with Solana in one second.

Ethereum’s 13-second block time makes it noncompetitive with other blockchains — that’s why Ethereum has been dropping so much against BTC. These “Based rollups” seem like a theoretical construction destined to fail, because there doesn’t even appear to be an attempt to understand what users actually want.

I just wonder how many more unusable rollup types — and their corresponding hype tokens — the market will tolerate.  It just looks like ETH foundation has a random generator of hype ideas that go into hype tokens.

Weren’t ZK rollups supposed to be the magic bullet? They have zero usage. Maybe it’s better to focus on making them work, especially since there are zillions of tokens already tied to them.

