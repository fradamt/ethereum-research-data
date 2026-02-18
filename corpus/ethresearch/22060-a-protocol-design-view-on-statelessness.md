---
source: ethresearch
topic_id: 22060
title: A Protocol Design View on Statelessness
author: Julian
date: "2025-04-01"
category: Proof-of-Stake > Economics
tags: [stateless]
url: https://ethresear.ch/t/a-protocol-design-view-on-statelessness/22060
views: 962
likes: 14
posts_count: 7
---

# A Protocol Design View on Statelessness

*Thanks to [Guillaume Ballet](https://x.com/gballet), [Ignacio Hagopian](https://x.com/ignaciohagopian), [CPerezz](https://x.com/CPerezz19), [Barnabé Monnot](https://x.com/barnabemonnot), [Caspar Schwarz-Schilling](https://x.com/casparschwa), [Thomas Thiery](https://x.com/soispoke), [Kev](https://x.com/kevaundray), [Dankrad Feist](https://x.com/dankrad), [Justin Drake](https://x.com/drakefjustin), and [Ng Wei Han](https://x.com/ngweihan_eth).*

State in Ethereum is the data that contains all account balances, account nonces, contract bytecode, and contract storage. As new accounts and contracts are added to Ethereum and existing contracts write more storage, the state grows. A crucial role that validators perform is attesting: issuing votes indicating whether a block is valid and should be finalized. A large state size is problematic because attesters cannot be expected to store too much data, and state access becomes more computationally expensive. The current Ethereum protocol needs attesters to store the state because, without it, attesters cannot independently perform their core duty: verify whether a block is valid.

The community wants Ethereum to be used more, so the state will grow. Yet, it does not want the burden that state growth puts on attesters, as higher attester hardware requirements degrade the quality of the network. [Statelessness](https://stateless.fyi/) is the proposed solution space to allow the state to grow while ensuring attesters do not need overly expensive hardware. Various solutions within the statelessness design space have been discussed.

Much effort has been spent removing the need for attesters to store the (full) state. However, relatively less mindshare has gone to who should hold the state instead. The purpose of this post is to explore who should hold the state instead of attesters.

[![paradigm_state](https://ethresear.ch/uploads/default/optimized/3X/8/f/8f791e659e81d96f2a2161ee36c2a85a34e5d90a_2_690x384.png)paradigm_state2738×1524 321 KB](https://ethresear.ch/uploads/default/8f791e659e81d96f2a2161ee36c2a85a34e5d90a)

Figure 1: Overview of state size per contract type and accounts. Taken from [this Paradigm post](https://www.paradigm.xyz/2024/03/how-to-raise-the-gas-limit-1) that has a clickable version of this figure.

**Full Statelessness** is a line of work that removes the need for the attester to store the state. Instead, attesters store minimal state information, namely the post-state root of the previous block, and receive a witness along with the new block. The witness contains:

1. The raw state necessary to execute a transaction from the block. For example, if a transaction sends 1 ETH from account A to account B, the required raw state to execute the transaction is the account balance and nonce of account A.
2. Proof that the raw state provided is correct. Proof that the account balance and nonce of account A provided above correspond to the canonical chain. Attesters check this proof against the post-state root of the previous block they had stored.

**[Two variants of full statelessness exist](https://hackmd.io/@vbuterin/state_size_management#Stateless-clients):** In a **weak stateless protocol**, the block producer is expected to provide the witness to the attesters, and therefore, it should have access to the full state. In a **strong stateless protocol**, the user must give the witness to the block producer. The block producer aggregates witnesses and sends them to the attesters. The user should have access to part of the state relevant to their transaction and their witness.

**Partial Statelessness** is a different line of work that allows network participants to store part of the state instead of its entirety. The core principle is that the state is partitioned into two sets. One *active* set is stored by all network participants and functions like the state does today. Another *inactive* set does not have to be stored by the block producer or attesters. If a user wants to access state from the inactive set, they need to provide a witness to resurrect that piece of state. The inactive set could consist of low-value or unused state. Storm and Georgios’ [post](https://www.paradigm.xyz/2024/03/how-to-raise-the-gas-limit-1) estimates that at least 7.4% of Ethereum’s state is no longer actively used. However, if Ethereum adopts partial statelessness, it would not mean only 7.4% of the state is part of the inactive set. Instead, the community needs to set the percentage of the state that must be part of the active set and determine state growth gas costs from there. Therefore, the inactive set could be far greater than 7.4% of the entire state.

**The core idea of the statelessness solution space is to optimally choose who is responsible for providing a witness to attesters, such that Ethereum can maximize state growth while keeping hardware requirements for network participants reasonable.** A key difference between partial and full statelessness is that the block producer and the attesters store the same state information in partial statelessness. In contrast, the block producer is expected to store the state in weak statelessness, but the attesters do not. In strong statelessness, neither the block producer nor the attester is expected to store the state. However, partial and full statelessness are not mutually exclusive (even if the terminology might suggest so). In Figure 2, we provide an overview of the possible combinations of solutions.

[![stateless](https://ethresear.ch/uploads/default/optimized/3X/3/a/3ac5d31d93742cfbe4c8f30b5670ca3f9bff5d33_2_690x244.png)stateless930×330 40.4 KB](https://ethresear.ch/uploads/default/3ac5d31d93742cfbe4c8f30b5670ca3f9bff5d33)

Figure 2: Overview of statelessness solution space. Blue headers correspond to full statelessness. The red header corresponds to partial statelessness. The purple header is a combination of full and partial statelessness, where block producers are partially stateless and attesters are fully stateless. Even though no witness is propagated over the network in a stateful protocol, we say attesters provide the witness necessary to convince themselves the state is part of the state tree in order to highlight that statelessness is about choosing who should provide a witness for a piece of state.

This post explores statelessness and state expiry from a high-level protocol design perspective. We aim to provide researchers and developers working on statelessness with insights on the following research questions:

1. Assuming a weak stateless protocol, is it necessary to implement partial statelessness in protocol?
 tldr: Block producers may determine their own state expiry rule, regardless of what state expiry rule the protocol sets.
2. What is the fundamental difference between weak and strong statelessness?
 tldr: Honest block producer behavior is defined differently in both settings; however, the parts of the state that rational block producers store may be similar.
3. Does state growth still constrain the gas limit in a weak stateless protocol?
 tldr: Protocol designers must jointly choose the gas limit and the state-providing architecture that best suits Ethereum. More state growth may lead to a worse state provider architecture.

This post is agnostic to how weak statelessness is implemented, so the results hold regardless of whether Ethereum uses a [Verkle Tree](https://stateless.fyi/trees/vkt-tree.html), a [Binary Tree](https://stateless.fyi/trees/binary-tree.html), or a zkEVM. We focus on the role of attesters and block producers and treat them as potentially separate entities, building on the [rainbow staking](https://ethresear.ch/t/unbundling-staking-towards-rainbow-staking/18683) framework.

## Out-of-protocol Partial Statelessness

Partial statelessness uses a *state expiry rule* to divide the state into two mutually exclusive and collectively exhaustive subsets. One set, the *active* set, contains state that may be accessed frequently by users and is stored by all attesters and block producers. The other set is referred to as the *inactive* set, for example, because state in this set may be accessed only sporadically. Attesters and block producers are not required to store the inactive set.

The state expiry rules that have been most explored partition the state into two subsets based roughly on the date the piece of state was last accessed. For example, a state expiry rule, as discussed in this [talk by Han](https://youtu.be/6j-7ZY2ITw8?si=MhxyIE9fmwAk6fb9), could say: if a piece of state has not been accessed in 6 months, move the piece of state from the active to the inactive set. In practice, this would mean attesters and block producers may remove that piece of state from their storage; a user wishing to access this piece of state now must provide a witness to resurrect that piece of state from the inactive to the active set. For context, [the state expiry rule Vitalik proposed](https://ethresear.ch/t/resurrection-conflict-minimized-state-bounding-take-2/8739) roughly states: move the active set to the inactive set every so many months; users must provide a witness to resurrect state from the inactive set to the active set.

[Ress](https://www.paradigm.xyz/2025/03/stateless-reth-nodes), stateless Reth, allows an execution client to run while only storing part of the state. Ress is an out-of-protocol partial stateless solution for attesters. It does not state what state the block producer is expected to store. Ress partitions the state such that the witness size is small and the part of the state that attesters must store is small. It assigns the contract bytecode to the active set and the rest of the state to the inactive set. This approach differs from the time-based approach in that the choice for partial statelessness is practically motivated to keep the witness size small. However, it is still expected that almost every transaction must provide a witness, unlike in the time-based approaches mentioned above.

State expiry rules aim to maximize the expected value of the difference between the active state to the network and the costs incurred by state churn, while keeping the maximum active state size under a certain threshold. State churn is the process of moving state between the active and inactive sets. In other words, the state expiry rule can be interpreted as the objective function of a knapsack problem, where the maximum active state size is the constraint*.

The protocol determines a state expiry rule that all attesters should adhere to. If attesters were to have a different state expiry rule, some attesters might require a witness for interaction with a piece of state, while others do not. Suppose there is no global state expiry rule, but attesters use their own expiry rules, then a block producer providing a block without a witness may split the attestations, leading to network instability. Attesters can always store more state than the state expiry rule prescribes, but should never store less.

Interestingly, block producers do not need to adhere to this state expiry rule. A block producer could prune a part of its state tree, for example, the infrequently accessed state, and make the following statement: “Transactions for which I have the state are included in the block; any transaction that touches state I do not have must provide a witness.” Figure 3 provides an example of how a block producer could do so. Consider a block producer who wishes to store accounts 1 and 2 but not 3 and 4. To include a transaction touching only account 1, the block producer must store the witness, consisting of account 2 and intermediate node B. If someone else touches account 3 in a different block, our block producer needs to update its witness with the new value of B.

[![root](https://ethresear.ch/uploads/default/original/3X/5/6/569a19f60cc68e26d39542dd9304a10cb9fff34c.png)root560×370 10.4 KB](https://ethresear.ch/uploads/default/569a19f60cc68e26d39542dd9304a10cb9fff34c)

Figure 3: State Tree Example. Consider a block producer who wants to include a transaction that interacts with account 1 (green). The block producer must provide a witness (orange) consisting of account 2 and intermediate node B. It does not have to store accounts 3 and 4.

We may not expect a block producer to prune part of their state tree since attesters with far worse hardware store the entire state as well. Indeed, if the protocol is designed such that block producers can always reasonably store all state, it may be unlikely they will prune their state tree. However, this post aims to highlight the possibility for protocol designers to lean on block producers pruning their local view of the state tree themselves. Even if attesters are stateless, implementing a state expiry rule could increase state growth since block producers are not expected to store all state. What is possible if we are not held back by the state-size block producers must hold? The question the community needs to pose itself is not why block producers would prune their state given the current state growth trends, but whether it would be beneficial to grow the state to a size larger than the protocol can expect a single block producer to store.

**We conclude that block producers may determine state expiry rules locally, regardless of what state expiry rule the protocol sets.** State expiry rules then do not maximize the value of the active state to the network, but the value of the active state to the block producer. Therefore, if attesters are stateless, a state expiry rule does not have to be a protocol rule. Setting a global state expiry rule, even if attesters are stateless, may still benefit the community in two ways. First, it could allow for more state growth, as the state block producers hold is smaller in size, so state growth is less constrained. Secondly, a global rule would help improve user experience as all block producers exhibit similar behavior. This rule could be stored in a smart contract instead of the protocol specifications. For starters, the rule should probably state that the smart contract it is in must not be pruned ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=14).

## Weak vs. Strong Statelessness

In both weak and strong stateless protocols, the attesters do not store the state but use witnesses to verify the correctness of the provided state instead. In weak statelessness, the block producer is expected to store the state and deliver the witness, whereas in strong statelessness, the user is expected to do so.

In the previous section, we argued that block producers may decide what state to store regardless of the protocol’s expectations of them. This immediately brings us to the core of the argument of this section: weak and strong statelessness may not be fundamentally different. If Ethereum adopts a weak stateless protocol, block producers may not store the entire state and require witnesses for interaction with some parts of the state. If Ethereum adopts a strong stateless protocol, block producers may store part of the state to supply users with witnesses for interaction with certain parts of the state. Regardless of whether Ethereum adopts weak or strong statelessness, in principle, block producers may store the same state information.

In a strong stateless protocol, the user still needs to access the state to decide whether to send a transaction (e.g., what is the price Uniswap quotes?) and to create a witness for its transaction. In principle, the user could store the state themselves, but this is impractical as the user must update its witness frequently, as explored in [this impossibility result](https://a16zcrypto.com/posts/article/on-the-impossibility-of-stateless-blockchains/) by Christ and Bonneau. Instead, the user may get this state from a state provider. The state provider may also be called the proof-serving node, as in [Srinivasan et al. (2021)](https://eprint.iacr.org/2021/599.pdf). The proof-serving node could be the wallet, the application, or anyone else. The block producer could also be the state provider. **Weak statelessness can be seen as a special case of strong statelessness in which the block producer is expected to be the proof-serving node for the user.**

Understanding the difference between weak and strong statelessness is important, even if they are very similar because it helps to define what honest block producer behavior may look like. Defining honest block producer behavior is essential as the protocol could employ numerous tools to force dishonest block producers to behave more like honest block producers. Examples of these tools include [MEV-Burn](https://ethresear.ch/t/mev-burn-a-simple-design/15590) and [FOCIL](https://ethresear.ch/t/fork-choice-enforced-inclusion-lists-focil-a-simple-committee-based-inclusion-list-proposal/19870). If the community decides the block producer must be the proof-serving node, then FOCIL could force-include transactions without providing a witness. If the community chooses otherwise, then FOCIL could only force-include transactions if they come with a witness. Importantly, for every future protocol, it must first be defined what honest block producer behavior is and then what the functionality of these tools is.

## State Growth post-Statelessness

Currently, state growth is constrained by the state size attesters can reasonably be expected to hold. If attesters are stateless, this constraint disappears. Perhaps the state size is still bounded by the state block producers can be expected to hold? However, if block producers do not fulfill the proof-serving node role, perhaps this is not a constraint either. What constraints does state growth still put on the gas limit in a stateless Ethereum protocol?

Perhaps we want to ensure archive nodes, nodes that presumably would store the entire state even if Ethereum were stateless, can keep up with the tip of the chain. Perhaps, we want to ensure there is sufficient redundancy and accessibility in the proof-serving node architecture to provide users the guarantee that their state can always easily be accessed for free. Note however, that these constraints are very different from the constraints state growth currently faces. Today, state growth is constrained by the attesters’ abilities, which is core to the protocol functioning. In the future, the constraints are formed by the user experience guarantees Ethereum wants to provide, which is a different trade-off.

**As protocol designers, we must jointly decide on the maximum state growth per unit of time and the proof-serving node architecture that best fulfills Ethereum’s needs. If allowing large state growth is the goal, the proof-serving node architecture must be robust. If it is more critical to ensure strong and freely accessible state storage via block producers and networks like [Portal](https://ethportal.net/), it may be necessary to temper state growth.**

To make this decision, the protocol design community needs to better understand the requirements for a proof-serving node architecture. I think it may be interesting to explore a proof-serving node architecture in which no single entity holds the entire state, but applications are responsible for the state relevant to their application, and perhaps wallets are responsible for the state relevant to their users. This system emulates the essential idea of [state rent](https://github.com/ethereum/EIPs/issues/35): applications and users increasing the state should not be able to pay once for a perpetual cost. In this system, the cost of storing state would be on the application or user who grows the state.

## Replies

**keyneom** (2025-04-02):

Thank you for writing this. It helped push me to finally at least write *something* about an idea I’ve had for a while. I’d love to get your perspective on it: [Enshrined Native L2s and Stateless Block Building](https://ethresear.ch/t/enshrined-native-l2s-and-stateless-block-building/22079)

Also, you mention that

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> Interestingly, block producers do not need to adhere to this state expiry rule. A block producer could prune a part of its state tree, for example, the infrequently accessed state, and make the following statement: “Transactions for which I have the state are included in the block; any transaction that touches state I do not have must provide a witness.”

I think FOCIL restricts this as a feasible strategy to some extent, no? So much so that I’d doubt it occurs in practice.

---

**Julian** (2025-04-03):

Thanks for your comment! I’d have to check out your article.

![](https://ethresear.ch/user_avatar/ethresear.ch/keyneom/48/19968_2.png) keyneom:

> I think FOCIL restricts this as a feasible strategy to some extent, no? So much so that I’d doubt it occurs in practice.

FOCIL is a tool that the Ethereum protocol can use to force block producers to behave more like “honest” block producers.

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> Understanding the difference between weak and strong statelessness is important, even if they are very similar because it helps to define what honest block producer behavior may look like. Defining honest block producer behavior is essential as the protocol could employ numerous tools to force dishonest block producers to behave more like honest block producers. Examples of these tools include MEV-Burn and FOCIL. If the community decides the block producer must be the proof-serving node, then FOCIL could force-include transactions without providing a witness. If the community chooses otherwise, then FOCIL could only force-include transactions if they come with a witness. Importantly, for every future protocol, it must first be defined what honest block producer behavior is and then what the functionality of these tools is.

FOCIL should never hurt an honest block producer. If the community decides that honest block producers are not expected to store the state, FOCIL should facilitate that such that it can be a feasible strategy for block producers to state.

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> “Transactions for which I have the state are included in the block; any transaction that touches state I do not have must provide a witness.”

The question is what the protocol should expect from honest block producers.

---

**kladkogex** (2025-04-09):

The current size of the state is tiny compared to the modern storage compatibilities. It is hard to store the blocks and the historic state, but the current state is peanuts ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

So I am not sure, what problem is being solved here? Reading state from disk is fast, if needed you trivially parallelize the database like LevelDB by key to make it as fast as needed. So the problem does not exist, at least in my experience.

If you read locally, you wont need to re-verify Merkle proofs, and it is just way simpler.

---

**kladkogex** (2025-04-09):

The current size of the state is tiny compared to modern storage capabilities. While storing blocks and historical state can be challenging, the current state is negligible ![:blush:](https://ethresear.ch/images/emoji/facebook_messenger/blush.png?v=12)

So I’m not sure what problem is being solved here. Reading state from disk is fast, and if needed, you can easily parallelize the database—like LevelDB—by key to achieve whatever performance you want. In my experience, this problem doesn’t really exist.

If you’re reading locally, there’s no need to re-verify Merkle proofs, which makes things much simpler and faster.

This is a classic solution in a search of a problem IMHO.  Has any user or block producer ever asked for statelesness ? It is a basic rule for any project that you do things that users ask for.

---

**Julian** (2025-04-09):

In Ethereum, the state growth is set such that the current state size is indeed not problematic. Growing the state, however, is expensive, precisely because we need to keep the total state size small. Users want to grow the state because it means that they can interact and create applications more cheaply. I motivate the problem in this post, and it has been described in many other works like [this canonical work](https://dankradfeist.de/ethereum/2021/02/14/why-stateless.html) by Dankrad.

Your reasoning that the current state size is not so big that state size management is not a problem misses the fact that the state size is small by design, and allowing it to grow bigger would benefit users. That is, you are taking the wrong counterfactual. With statelessness, the state size would be vastly bigger. Users clearly want to be able to interact with and create new applications for lower fees.

Finally, your premise that the state size is negligible doesn’t completely hold. The current state size is around 250GiB and is expected to be between 400 and 600 GiB in 5 years (without statelessness) ([source](https://www.paradigm.xyz/2024/03/how-to-raise-the-gas-limit-1)). A goal of Ethereum is to allow as many people to participate in the protocol as possible, which is clearly easier to satisfy if there were no entry requirement of let’s say 500 GiB of storage in 5 years (without statelessness), but virtually zero storage requirements instead. Allowing potentially even smart-watch clients to join ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**kladkogex** (2025-04-11):

Hey Julian,

I beg to disagree. If you ask me to grow the state cheaply I will just shard the state database into multiple cloud VMs. It is trivial. I can bet with you Julian that I can reach ANY performance benchmark with this.

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> I motivate the problem in this post, and it has been described in many other works like this canonical work by Dankrad

Things usually become canonical Julian after many years.  Canonical are the works of Einstein on general relativity.  This is just a post from Dankrad.

I find it so funny that ETH foundation developed this  “speak”,  it is totally against freedom of science.  People on top like Vitalik need to think hard about this.

