---
source: magicians
topic_id: 24605
title: Scaling the L1 to Gigagas with Real-Time Proving
author: ks_kulk
date: "2025-06-19"
category: Magicians
tags: []
url: https://ethereum-magicians.org/t/scaling-the-l1-to-gigagas-with-real-time-proving/24605
views: 1601
likes: 11
posts_count: 7
---

# Scaling the L1 to Gigagas with Real-Time Proving

*Real-time proving will let Ethereum reduce execution bottlenecks, pump the gas, and scale the L1. Prover networks, which are two-sided marketplaces that coordinate ZK provers and requesters, will ensure Ethereum can scale by giving block builders access to the most competitive provers, implementing proposer-prover separation via a “zk-boost” relay.*

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/2/22327fa598f7b83d4a9de85436b25b5294a72891_2_690x245.png)image3113×1107 222 KB](https://ethereum-magicians.org/uploads/default/22327fa598f7b83d4a9de85436b25b5294a72891)

*Figure 1:* The zk-boost relay, along with decentralized prover networks, can enable proposer-prover separation and scale the L1.

[The achievement of real-time Ethereum proving](https://blog.succinct.xyz/sp1-hypercube/) has expanded the avenues for Ethereum to scale the L1 by massively increasing the gas limit. Questions remain: how should Ethereum best make use of this technological breakthrough, and on what time scale?

We propose that **decentralized prover networks, which are two-sided marketplaces for ZK proof generation, can act as core infrastructure for Ethereum** by allowing block builders to access a specialized set of actors (provers) who competitively and reliably generate proofs. Note that decentralized prover networks, which create a competitive marketplace for proof generation, are distinct from distributed proving, which splits up proving of a single workload among several actors.

Such a market structure is not without precedent in Ethereum: proposer-builder separation, implemented via [mev-boost](https://github.com/flashbots/mev-boost), induced specialization in block building. This gave a path to an endgame where [block production is still centralized, but block validation is trustless and highly decentralized](https://vitalik.eth.limo/general/2021/12/06/endgame.html?utm_source=chatgpt.com).

Similarly, we can build a “zk-boost” middleware for Ethereum that lets builders submit proofs to the block’s proposer and allows validators to verify these proofs, implementing proposer-prover separation (Figure 1). This lets builders access prover networks via the relay; builders are incentivized to do so because prover networks surface the most competitive set of provers. Instead of directly enshrining proving in the protocol, this gives a path for Ethereum to outsource its proofs and make use of real-time proving in the short run and scale to gigagas.

In this post, we’ll cover the state of the L1, the current challenges with scaling, what real-time proving achieves, and how it can be integrated into Ethereum in the short-term via proposer-prover separation.

## The State of the L1

Ethereum today relies on redundant re-execution of transactions by a committee of validators who come to consensus on each 12 second slot. There is a robust block construction economy that allows validators to receive and verify blocks. The process of including a block into Ethereum works as follows:

1. A block builder, who is typically a sophisticated actor outside the Ethereum protocol, constructs a block from transactions in the public mempool and private order flow and submits them to the block’s proposer .
2. The proposer forwards the block to attesters, who are the other validators in the committee. The attesters gossip it to each other, re-execute the transactions in the block to check for validity, and vote that the block and its data were valid.
3. If a majority of attestations are received in time, the block is included. If not, the block is ignored or reorged.

This process creates a hard ceiling on scalability: every validator in the attestation committee must individually re-execute the entire block within a few seconds before casting a vote. Even if a few validators have fast hardware, the slowest honest node defines the system’s throughput; increasing the nodes’ hardware requirements comes with making tradeoffs on the decentralization and verifiability of the network. This makes it difficult to raise the gas limit while maintaining a large, distributed validator set. In nearly 4 years, the gas limit has only been raised once, [from 30 million to 36 million in February 2025](https://www.coindesk.com/markets/2025/02/04/ethereum-raises-gas-limits-for-first-time-since-2021-boosting-eth-appeal?utm_source=chatgpt.com).

Raising the gas limit, which increases the maximum size of each block, is also challenging for other reasons:

1. State growth: Larger blocks mean more accounts and more contract storage; in short, state growth. This puts a burden on full nodes, who need to store the entire history of the state, and slows their sync time. However, modern consumer hardware means that Ethereum can sustain current levels of state growth for many years, with a comfortable buffer before it becomes a bottleneck. Even if state grows faster due to increased gas limits, proposed solutions including pruning historical data and Verkle trees mean that state growth is not the bottleneck.
2. Reading the chain: Increasing the size of blocks also means that full nodes have a harder time reading the chain in a trustless way without relying on intermediaries. In response, a local-node-favoring delta to the scaling roadmap can be added to make it easy to run partially stateless nodes that keep a portion of the state.

With these workarounds, there is a path to making rapid use of ZK proving technology to eliminate the re-execution of transactions by each validator. Instead of re-execution, validators can simply verify ZK proofs that are submitted by the proposer of the block. Today, Ethereum conflates execution with validation. But [asymmetries between execution and validation are scaling opportunities](https://ethresear.ch/t/decoupling-throughput-from-local-building/22004). Motivated by advances in ZK proving, the Overton window on raising the gas limit has expanded and recent proposals have suggested [exponentially increasing the gas limit 100x over 4 years](https://eips.ethereum.org/EIPS/eip-7938).

## Tackling the Scaling Bottleneck

ZK proofs present a significant scaling opportunity for Ethereum. The key enabling technology is a general purpose [zero-knowledge virtual machine (zkVM)](https://docs.succinct.xyz/docs/sp1/introduction), which can prove the execution of arbitrary code, including execution of Ethereum blocks. With zkVMs, attesters in the validator committee don’t need to re-execute the transactions in the block at all. They can [statically verify](https://eips.ethereum.org/EIPS/eip-7886) the block, which involves simple checks, without executing transactions. The job of proving the execution of transactions in the block can be then outsourced to a prover, who runs the execution of the transactions inside a zkVM. Because proof verification requires constant time, attesters can quickly verify the proof (in milliseconds) on commodity hardware or even on cheap hardware like Raspberry Pis.

### The Need for Real-Time Proving

Real-time proving is the ability to generate a ZK proof of execution of an Ethereum block in less than 12 seconds (a single slot time). Because of the serial nature of the chain, proving in real-time is necessary to scale the number of transactions in a block. Real-time proving [was a sci-fi problem](https://x.com/drakefjustin/status/1925138107508130105) and considered to be years away, but exponential advances in proof systems and performance engineering have made it a reality. Succinct [recently achieved](https://blog.succinct.xyz/sp1-hypercube/) real-time proving on a cluster of ~160 GPUs, with a path to reducing this number and the time required for proving even further. In a world with real-time proving, block construction would work as follows:

1. A block builder submits a block’s contents to the block’s proposer . This builder is also responsible for force including a ZK proof of execution to the attesters in the next slot.
2. The proposer forwards the block to attesters , the other validators in the committee. The attesters gossip it to each other and statically verify the block without re-execution, checking signatures and transaction fees.
3. The builder submits a proof to the next slot’s proposer .
4. Attesters in the next slot verify this proof, and the block is included.

The responsibility of proving the execution of the block is assigned to the block’s builder via delayed execution. This solves an incentive problem: if the responsibility is offloaded, say, to the block’s proposer, the builder may construct so-called “prover killers” that are very expensive to prove.

### Implications

Since attesters don’t need to re-execute the block, merely verify the proof, Ethereum can massively increase its gas limit. This presents an unprecedented scaling opportunity for Ethereum, **one that wasn’t available before the advent of zkVMs** .

Proof generation with zkVMs is inherently parallelizable and therefore benefits from the ubiquitous availability of GPUs and experiences complementarities with the worldwide AI buildout. Even if we 100x the gas limit, ZK proving latency will not be significantly impacted because we can chunk up a block into subblocks which are [proven in parallel and then aggregated into one proof at the end](https://x.com/pumatheuma/status/1925231968117277066). This makes using real-time proving a viable solution for scaling Ethereum.

## Proposer-Prover Separation

If Ethereum is to integrate real-time proving into its scaling roadmap, how should it source its proofs? There are several options:

1. Ethereum contracts an individual prover to do all of its proof generation. This is a centralized, “software as a service” model.
2. Ethereum requires proving infrastructure to be cheap and energy-efficient enough to support real-time proving at home, and enshrines “heavy nodes” that do this proving in-protocol.
3. Ethereum makes use of decentralized prover networks that can surface a competitive, reliable set of provers with free market competition and scales by outsourcing proofs and implementing proposer-prover separation.

Proving has a [1 of N trust assumption](https://vitalik.eth.limo/general/2020/08/20/trust.html) (meaning that you only need one honest prover to be active for a valid proof to be generated). Even so, it is clear that having only a single prover (or small collection of provers) be available to prove blocks would lead to an uncomfortable degree of centralization for Ethereum. These provers can be [subject to global bans](https://ethereum-magicians.org/t/relaxing-the-prover-hardware-requirements-for-the-next-few-years/24346/12) that prevent them from proving blocks that include some transactions. The software as a service model, therefore, is doomed.

Home proving makes it possible for anyone to be a prover. Suggestions to wait to scale the L1 until [ZK proving becomes energy efficient enough to prove at home](https://x.com/VitalikButerin/status/1925050155922862526) (~10 kW) are motivated by making it easy for anyone to run a prover at home. However, baking this into the protocol immediately is untenable and would [require Ethereum to not use the newly acquired power](https://ethereum-magicians.org/t/relaxing-the-prover-hardware-requirements-for-the-next-few-years/24346) that is real-time proving for a while.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/d/d9995f07dff9f5158cfb7f2ca154392edb91abd1_2_474x500.png)image1063×1121 37.5 KB](https://ethereum-magicians.org/uploads/default/d9995f07dff9f5158cfb7f2ca154392edb91abd1)

*Figure 2:* Builders can use prover networks to source proofs from the most competitive provers.

As a third option, we can [relax the proving requirements for the next few years](https://ethereum-magicians.org/t/relaxing-the-prover-hardware-requirements-for-the-next-few-years/24346) and rely on prover networks or marketplaces that surface provers who can generate proofs for Ethereum. Decentralized prover networks make it possible for block builders to access, in a permissionless fashion, the most competitive set of provers worldwide. Importantly, prover networks make use of spare GPU capacity that is already available worldwide without imposing energy and hardware constraints on the protocol’s participants. This spare capacity might be a lot more cost effective than any particular home proving setup. Accelerated hardware setups can contribute to prover networks as well. Because prover networks surface the most competitive provers, builders are incentivized to use then. Since ZK proofs are self-verifying and massively parallelizable, builders can easily outsource their workloads to provers.

Recent work on [incentivizing anonymous participation](https://ethresear.ch/t/on-incentivizing-anonymous-participation/22469) and on [procurement auctions that incentivize multiple parties to provide services](https://pdf.succinct.xyz/) suggests that Ethereum can use prover networks to find a sufficiently decentralized, efficient set of provers that can be used to scale the L1 rapidly.

### ZK-Boost: Implementing Proposer-Prover Separation

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/7/78577aa06731d8fc5981823f0dbc9c01f2a12c2e_2_690x190.png)image2352×648 92.6 KB](https://ethereum-magicians.org/uploads/default/78577aa06731d8fc5981823f0dbc9c01f2a12c2e)

*Figure 4:* A proposed zk-boost architecture.

To implement proposer-prover separation, we can build a “zk-boost” relay that acts as middleware, coordianting builders, provers, and validators. A `zk_getExecutionProof` endpoint allows builders to request proofs from prover networks (or prove locally in case they choose to do so) and an `eth_verifyProof` endpoint allows validators to verify proofs.

After the designated builder requests a proof via the relay, the prover network can run a competitive procurement process for the proof of each block. By implementing proposer-prover separation, the zk-boost relay makes it possible for builders to contract the best provers and for Ethereum validators to verify proofs.

### Comparison: mev-boost and PBS

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/5/50abe0b15202d0d4b020287e7a2e4c6353ef4cd5_2_690x245.png)image3113×1107 286 KB](https://ethereum-magicians.org/uploads/default/50abe0b15202d0d4b020287e7a2e4c6353ef4cd5)

*Figure 3:* The mev-boost relay outsources block building to specialized builders. Diagram adapted from [here](https://ethresear.ch/t/mev-boost-merge-ready-flashbots-architecture/11177).

Relying on markets that outsource Ethereum’s needs to sophisticated third parties is not without precedent. Ethereum’s growth over the last several years has given us examples of specialization leading to positive-sum dynamics. Consider mev-boost, which implements proposer-builder separation (PBS). By introducing a middleware layer that allows proposers to outsource block building to sophisticated third parties, mev-boost created a marketplace for block building. This allowed builders to optimize block contents, while validators retained the roles of final block selection and attestation.

By opting into this middleware, proposers are able to access professional market participants. Because decentralization in this market is a means, not an end goal, it’s [ok to centralize block building](https://ethereum.org/en/roadmap/pbs/). If there is going to be centralization due to economies of scale, we want to isolate it to certain parts of the stack. In the PBS endgame design, proposing blocks and verifying their correctness remains decentralized and trustless.

Similarly, proving will also face a degree of specialization in the short run. Provers have higher hardware requirements than builders and compete on performance. However, they don’t extract MEV. Therefore, we can expect the prover market to be more decentralized than the builder market. Since we only need one prover to submit a proof, relying on prover networks is ok.

### Further Considerations

- Proof liveness: every block just needs a single proof to be generated for the chain to progress. In this sense, the censorship of proofs is less pressing of a problem than censorship of a block’s contents. However, an adversary can bribe all provers to not submit a proof. To solve this, prover networks can require bonds and fallbacks that make it very expensive to censor the proof.
- Interactions between proving and MEV: block builders prefer waiting until the last second to submit their blocks to have as much of an information advantage as possible. How do we avoid giving an edge to faster provers running on specialized hardware?
- Interactions with native tokens: Builders currently pay proposers in ETH. How do the economics of block building change with the native tokens of prover networks?

***Note**: This post is by [Succinct](https://blog.succinct.xyz/). The snarkification of Ethereum entails many open questions. The purpose of this post is to spark discussion around new infrastructure (prover networks) that Ethereum can use on its way to integrating ZK proofs.*

***Acknowledgments:** We’d like to thank [Mike Neuder](https://michaelneuder.github.io/), [Dankrad Feist](https://dankradfeist.de/), and [Artem Kotelskiy](https://artofkot.xyz/) for valuable feedback on this post. Feedback is not necessarily an endorsement.*

## Replies

**asotie** (2025-06-20):

This is *insanely exciting*—real-time proving is no longer sci-fi! ![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=12) The zk-boost relay + decentralized prover networks = a practical path to *Gigagas Ethereum*. The parallels to mev-boost make so much sense, and the proposer-prover separation model is a brilliant way to preserve decentralization while tapping into global GPU liquidity. L1 scaling is finally entering its ZK-powered era. Let’s gooo! ![:man_mage:](https://ethereum-magicians.org/images/emoji/twitter/man_mage.png?v=12)![:zap:](https://ethereum-magicians.org/images/emoji/twitter/zap.png?v=12)![:test_tube:](https://ethereum-magicians.org/images/emoji/twitter/test_tube.png?v=12) #ZK #Ethereum [scaling](/tag/scaling)

---

**neoreign** (2025-06-21):

Finally seeing Real time proving becoming reality at this speed and at this time is extremely impressive, to be very honest, this is a praise worthy work.

---

**mrabino1** (2025-07-05):

a.) respect ! great wok…

b.) question… if succinct was able to use ~150 GPUs to have ~99% of blocks with RTP… will having 1500 GPUs provide almost certainty to RTP?  The reason for the question lies with actual L1 implementation timeframes.  While the tech is more than impressive, I am curious what the timeframe would be to getting a test net together for this.

c.) would ETH (as a bond to ensure liveliness) be a viable asset?

thx.

---

**ks_kulk** (2025-07-05):

> if succinct was able to use ~150 GPUs to have ~99% of blocks with RTP… will having 1500 GPUs provide almost certainty to RTP?

Although scaling up GPUs can help, the main bottleneck is serial computation that needs to be done to generate work for the GPUs in the “executor”. Several efforts to reduce this bottleneck are currently under way.

---

**mrabino1** (2025-07-07):

Interesting ! Thank you. I would assume that once that coordination effort is largely resolved, the scale would be mostly linear. However, I also have to assume the larger the # of transactions in a block, the more “state collisions” there would be. I can imagine the overhead on this with a continuous river of transactional flow. Would love to learn more and help. Scaling the L1 and successfully navigating from an execution layer to a verification layer is paramount.

---

**daniel-ivanco** (2025-07-30):

As far as I know, only an Nvidia GPU was used for this. Have there been any successful tests using non-Western hardware too?

