---
source: ethresearch
topic_id: 9186
title: Introducing Scroll, a new layer2 solution
author: silverpoker
date: "2021-04-14"
category: Layer 2
tags: []
url: https://ethresear.ch/t/introducing-scroll-a-new-layer2-solution/9186
views: 9098
likes: 20
posts_count: 8
---

# Introducing Scroll, a new layer2 solution

Hi all,

I’m Ye Zhang, a Ph.D. student at NYU. We’re building a new layer2 system on Etherum based on Rollup. Here is a draft introduction:

https://scroll-finance.medium.com/scroll-a-layer-2-ecosystem-based-on-zk-rollup-186ff0d764c

Three main differences from other Rollup projects:

(1) We are considering combining two different zero-knowledge proof systems for both on-chain and off-chain efficiency. If the recursive proof system is efficient enough, we will also consider that.

(2) We use commitment (UTXO) as the middle layer for interaction between different layer2 ASIC circuits. So ASIC circuits can interact and combine arbitrarily. It’s similar to Zexe. We will eventually move to recursive proof for the CPU circuit if it’s feasible enough in the future.

(3) We want to use a new incentive mechanism for layer2 mining and let “miners” be volunteers to generate proofs for us. It’s a little similar to snarker in Mina. The mechanism is still working under progress thus we didn’t provide many details in the article. We think it can eliminate the problem of MEV by separating batching and proving.

We are still at a very early stage for development and hope to get more feedback from the Ethereum community. Also, we are hiring, if anyone is interested in joining, pls email us (hr@scroll.finance). Some are still open problems for all L2. If you are interested in doing research or solving some problems or collaborating or giving suggestions, we can also talk and build a better layer2 together. Email me at  [silverpoker1998@gmail.com](mailto:silverpoker1998@gmail.com).

## Replies

**vbuterin** (2021-04-15):

Interesting!

How does this compare to the Aztec zk-zk rollup’s vision? Are there any large technical differences between what they are doing and your approach?

---

**silverpoker** (2021-04-18):

Hi, Thanks for your interest!

It’s true that this framework can easily support privacy due to the underlying two-layer zero-knowledge proof system (like Aztec does in zk-zk rollup). However, we don’t focus on privacy for now. We focus more on the practical efficiency to support more dedicated DeFi circuits and their interactions on layer2.

So, one difference behind this is that we use two different zkp systems for **efficiency** instead of privacy.

Most rollup only supports Transfer and Swap circuits using Merkle Tree. It’s hard to support more complicated DeFi and larger applications. It takes a fairly long time to generate a snark proof for large-sized computation. However, there are indeed many prover-efficient protocols with longer proof size or longer verification time. For example, zk-stark, spartan, and many GKR-based protocols are efficient for prover but not as succinct as snark for the verifier. We want an efficient off-chain prover and efficient verifier to reduce the on-chain gas cost. So we combine two different zkp systems to support large circuits in the future. This is also pretty much similar to Mina’s/Zcash’s cross-chain bridge to Etherum ---- the Pickle system or Halo2 can support recursive proof but the verification is costy on EVM, we need another “wrapping” layer for the verification.

Another technical difference is that we propose a new interaction model through the commitment scheme.

We think it’s still hard to support general zkEVM at this point and each DeFi circuit still needs to be written manually for efficiency. The problem for circuit auditing might be solved in the future by a stronger compiler with math proof (i.e., Leo compiler supports verification for zkp circuits, see [Leo paper](https://docs.zkproof.org/pages/standards/accepted-workshop4/proposal-leo.pdf)). However, such separated circuits are hard to interact like smart contracts usually does. One way to allow general interaction is importing different DeFi ASIC circuits and generate one proof for all in one shot. However, this might bring more problems with the increasing size of the composed circuit. We give a more clear way to model interactions between those circuits. It’s like a hybrid version of the account based model and UTXO model where you generate proofs for separate parts and link them together in the end.

The last thing is that we want to enable layer2 mining where everyone can still join to generate the proof. This looks easy but needs a careful incentive mechanism design to avoid the situation where the fastest miner always wins.

---

**silverpoker** (2021-04-18):

All those ideas are very open for discussion and expect more feedbacks from the Ethereum community.

Our specific roadmap is that:

(1) Test the layer2 mining model with one zkp layer (i.e. zksync or loopring).

(2) Add more DeFi circuits and test for the best interaction model (i.e. nft, lending and other protocols)

(3) Move to the new layered proving system with the best efficiency (i.e. halo+plonk)

We will make some adjustments depending on concrete performance of zkEVM. We believe recursive proof+VM with the solidity support will be the winning solution in the future. But even with VM, the exploration of DeFi ASIC circuits will be useful as builtins or sub gadgets. We are looking forward to more discussion of all those details. Email me at yezhang@scroll.finance or [silverpoker1998gmail.com](http://silverpoker1998gmail.com) ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**ileuthwehfoi** (2021-10-13):

In regards to point (3), can you elaborate on the economic incentives of this system? I can see the appeal, which is to separate the sequencer to eliminate MEV. But it seems to me that the most profitable response is for block producers to also run a miner and prioritize including their own proofs. Unless there is a way to prevent this, the end result is equivalent to a full sequencer.

Another thing that would be interesting to see is some modeling around the miner ecosystem. It seems to me that if the mempool is sufficiently small such that a single miner can handle all pending txs, then it can drive all competing miners out of business by reducing it’s own margin for a prolonged period of time. On the other hand, if there is enough volume for two or more miners, the most efficient miner will prioritize transactions in order of price per unit of computation, ignoring the actions of other miners. To prevent wasted work, the less efficient miner would carve out the most profitable transactions and begin with transactions it knows will not be included by the first miner. But the result is that the likelihood of inclusion could actually be reduced if it is on the border between the two miner’s “territories”.

Lastly, this might be off topic, so feel free to ignore it or dm me your thoughts instead of replying, but do you have any thoughts on validiums vs monolithic zk-blockchains like Mina? It seems to me that the Mina snarker + block producer is equivalent to the Scroll miner and batcher. Assuming Mina eventually adds a data availability solution, the only difference would be that Scroll pays an extra cost of committing the block hash to L1, making it strictly better than all validiums, all else being equal.

---

**silverpoker** (2021-10-14):

Hi, thanks for your interest!

We have another article describing this mechanism. The high-level idea is that we will reward the “miners”  who help us generate the proof with our token. We hope to open a different proving market — having a strong proving network is valuable, you can enable public verifiability for general off-chain computation. This can also incentives the external community to build better and better hardware accelerators to make proving faster. (See the second goal in our new [overview](https://hackmd.io/@yezhang/S1sJ2cEWY))

Yeah, it’s true that the only way to eliminate MEV relies on sequencer… For now, we are still using a centralized sequencer with proof generation outsourced to “miners”. We are still halfway to achieve full decentralization and plan to decentralize the sequencer at some point (i.e. use auction or some other methods). The point is that “miners” in our system can’t order transactions to profit. This can naturally be separated into two different parties: “sequencer community” and “miner community”.

As for the miner ecosystem, we will avoid the “Fastest prover always win” problem. In our mechanism, we only require miners to generate proof within a time window `T`. Then we will select the qualified miner using a random beacon – So you don’t have to be the fastest, and even you are fast, you won’t take all the reward.

I feel there are more and more similarities between us and Mina, but we still position ourselves as a layer 2 relying on the security of Ethereum. I think one day, we can bring EVM-compatibility to other non-EVM-compatible chains like Mina and Aleo as far as they can verify our proofs. There are some other differences, I will dm you the latest write-up about our mechanism design and some of my thoughts.

---

**silverpoker** (2021-10-14):

To the readers of this thread, we changed a lot during the past 6 months. The write-up is out of date now ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) We make huge and marked modifications to our roadmap and technology. See a new brief overview [here](https://hackmd.io/@yezhang/S1sJ2cEWY).

We will reuse the idea of proof outsourcing and the hierarchical proving system. However, a more important focus is contributing to the zkEVM community. See the recent thread [here](https://ethresear.ch/t/the-intuition-and-summary-of-zkevm/10877). zkEVM can provide a better developer experience than individual ASIC circuits mentioned in this article.

DM me or email yezhang@scroll.tech if you are interested in us.

---

**yyb9882** (2023-01-17):

I am a current Ph.D student in China. My major interest includes multiparty computation and zero-knowledge proof. I have read some paper about zero-knowledge and it is really interesting to apply zero-knowledge proof on the Ethereum. Recently, I focus on your research on proving the correctness of execution of EVM (zkEVM). I think this is the most interesting topic in Scroll.

