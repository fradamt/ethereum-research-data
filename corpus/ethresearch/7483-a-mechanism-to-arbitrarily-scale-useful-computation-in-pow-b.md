---
source: ethresearch
topic_id: 7483
title: A mechanism to arbitrarily scale useful computation in PoW blockchains
author: sourav1547
date: "2020-05-30"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/a-mechanism-to-arbitrarily-scale-useful-computation-in-pow-blockchains/7483
views: 1337
likes: 6
posts_count: 9
---

# A mechanism to arbitrarily scale useful computation in PoW blockchains

TLDR: We have worked out a paper that shows trivial increase in block validation has leads to unfairness to miners with slow processing power. Also, it proposes a new mechanism to allow arbitrary computation in PoW blockchains. The core idea is to delay the validation of

transaction by up to \zeta blocks to get block validation step off the critical path of PoW.

Abstract:

Proof-of-Work~(PoW) based blockchains typically allocate only a tiny fraction (e.g., less than 1% for Ethereum) of the average interarrival time~(mathbb{I} ) between blocks for validating transactions. A trivial increase in validation time~( \tau ) introduces the popularly known Verifier’s Dilemma, and as we demonstrate, causes more forking and increases unfairness. Large \tau also reduces the tolerance for safety against a Byzantine adversary. Solutions that offload validation to a set of non-chain nodes (a.k.a. off-chain approaches) suffer from trust issues that are non-trivial to resolve.

In this paper, we present Tuxedo, the first on-chain protocol to theoretically scale \tau/\mathbb{I} \approx 1 in PoW blockchains. The key innovation in Tuxedo is to separate the consensus on the ordering of transactions from their execution. We achieve this by allowing miners to delay validation of transactions in a block by up to \zeta blocks, where \zeta is a system parameter. We perform security analysis of Tuxedo considering all possible adversarial strategies in a synchronous network with end-to-end delay \Delta and demonstrate that Tuxedo achieves security equivalent to known results for longest chain PoW Nakamoto consensus. Additionally, we also suggest a principled approach for practical choices of parameter \zeta as per the application requirement. Our prototype implementation of Tuxedo atop Ethereum demonstrates that it can scale \tau without suffering the harmful effects of naive scaling in existing blockchains.

Paper link: https://arxiv.org/abs/2005.11791

## Replies

**SebastianElvis** (2020-05-30):

This paper looks cool! Indeed this can somewhat solve the Miner’s Dilemma. I have two questions regarding the Tuxedo protocol.

1. Tuxedo assumes synchronous network, i.e., messages are delivered to all honest miners within a known time bound \Delta. Is this assumption too strong for permissionless blockchains? Also, why should Tuxedo rely on this assumption? I guess the reason is that, all honest miners should have the complete knowledge on all pending transactions, am I right?
2. What if there is a block that has a valid PoW solution but includes some invalid transactions? Although miners may not have such incentive (as this renders his work in vein), this will make the fork starting from that invalid block invalid. If transaction verification is delayed, then this might happen after several new blocks appended to that invalid block. I cannot find any discussion on this issue. If there is, could you please point me to that section?

---

**sourav1547** (2020-05-30):

[@SebastianElvis](/u/sebastianelvis)

1. Every permissionless blockchain that uses PoW based Nakamoto consensus requires known bounded delay assumption for safety conditions to hold. To see why consider the following example, let k be the confirmation rule of a Nakamoto consensus based blockchain. For example, Bitcoin users typically use k=6. Then for any given k, if the network delay is not known a priori, no finite k will suffice. This is because an adversary can partition the honest miners into two subsets and delay messages across these subsets till both subset of miners mine at least k blocks. According to our k-block confirmation rule, both blocks should be committed. However, as we all know, when the adversary allows messages across these subsets, after k or more blocks has been mined by each of them, one of the chains (the shorter among the both) will be discarded violating our safety guarantees.
 NOTES:
a) More generally, consensus protocol tolerating more than 1/3rd Byzantine nodes is impossible in a network with unknown delay. See https://decentralizedthoughts.github.io/2019-06-25-on-the-impossibility-of-byzantine-agreement-for-n-equals-3f-in-partial-synchrony/ for more detailed and easily accessible explanation of the impossibility result.
b) Typical Nakamoto style consensus tolerates up to 1/2 Byzantine adversary; hence they can not provide safety in a network with unknown delay.
2. The goal of any consensus algorithm is too make sure that honest nodes agree on a sequence of instructions. How these sequences of instructions are treated at the application layer (say transaction validity) is a concern at the higher layer of the protocol.  For example, even Ethereum can include some variants of invalid transactions, for example, transactions that do not pay enough gas for its execution are also invalid. Currently, all miners in Ethereum treat such transactions as NoOps (No operation). The crucial thing to understand is that as long as all honest miners identically treat invalid transactions, there won’t be any fork among honest miners.
 I agree that there that in Tuxedo, malicious miners can include junk transactions in a block. This is indeed an excellent point. Such issues can be mitigated using incentive mechanisms such as fee collection. We talk about fee collection in section IV.C of the paper.

---

**SebastianElvis** (2020-05-30):

Thanks for your detailed reply.

> Every permissionless blockchain that uses PoW based Nakamoto consensus requires known bounded delay assumption for safety conditions to hold. To see why consider the following example, let kk be the confirmation rule of a Nakamoto consensus based blockchain.

I don’t think so. With sufficient confirmation blocks, PoW-based consensus can achieve both safety and liveness in asynchronous networks with overwhelming probability. See this paper https://eprint.iacr.org/2016/454.pdf. Nakamoto consensus does not need to rely on synchronous networks. The reason of assuming synchronous networks is to simply security proofs. I believe Tuxedo can be proven secure in asynchronous networks the same way, although complicated and tedious.

> For example, Bitcoin users typically use k=6k=6 . Then for any given kk , if the network delay is not known a priori, no finite kk will suffice. This is because an adversary can partition the honest miners into two subsets and delay messages across these subsets till both subset of miners mine at least kk blocks. According to our kk -block confirmation rule, both blocks should be committed. However, as we all know, when the adversary allows messages across these subsets, after kk or more blocks has been mined by each of them, one of the chains (the shorter among the both) will be discarded violating our safety guarantees.

To launch such an attack, 1) the adversary should control an overwhelming portion of mining power, and 2) the adversary should prevent these two subset of miners from communicating with each other. As long as 2) does not hold, miners will know both forks and only accept the longer one, according to the longest chain rule.

> NOTES:
> a) More generally, consensus protocol tolerating more than 1/3rd Byzantine nodes is impossible in a network with unknown delay. See Byzantine Agreement is impossible for $n \leq 3 f$ under partial synchrony for more detailed and easily accessible explanation of the impossibility result.

True, this is the FLP impossibility. Nakamoto consensus works around FLP by two mesaures. First, Nakamoto consensus only provides probabilistic guarantee. Second, Nakamoto consensus is not live in asynchronous networks, but can be safe with overwhelming probability by having sufficient confirmation blocks.

> b) Typical Nakamoto style consensus tolerates up to 1/2 Byzantine adversary; hence they can not provide safety in a network with unknown delay.

I’m not sure if the “1/2 fault tolerance” results in the broken safety in asynchronous networks. Is there any paper proving this causality?

> The goal of any consensus algorithm is too make sure that honest nodes agree on a sequence of instructions. How these sequences of instructions are treated at the application layer (say transaction validity) is a concern at the higher layer of the protocol. For example, even Ethereum can include some variants of invalid transactions, for example, transactions that do not pay enough gas for its execution are also invalid. Currently, all miners in Ethereum treat such transactions as  NoOps  (No operation). The crucial thing to understand is that as long as all honest miners identically treat invalid transactions, there won’t be any fork among honest miners.
>
>
> I agree that there that in Tuxedo, malicious miners can include junk transactions in a block. This is indeed an excellent point. Such issues can be mitigated using incentive mechanisms such as fee collection. We talk about fee collection in section IV.C of the paper.

Indeed, both the `NoOps` approach and the fee mechanism seem to be feasible.

However, in this way, being included no longer means being valid. Then lightweight clients might have some problems. For example, a lightweight client may confirm that a transaction is included in a specific block (by communicating with other nodes), but cannot verify whether this transaction is valid.

---

**sourav1547** (2020-05-30):

> I don’t think so. With sufficient confirmation blocks, PoW-based consensus can achieve both safety and liveness in asynchronous networks with overwhelming probability. See this paper https://eprint.iacr.org/2016/454.pdf. Nakamoto consensus does not need to rely on synchronous networks. The reason of assuming synchronous networks is to simply security proofs. I believe Tuxedo can be proven secure in asynchronous networks the same way, although complicated and tedious.

The paper you mentioned does the proof in the same network model as Tuxedo. This network model is more commonly referred as the **synchronous** network.

> To launch such an attack, 1) the adversary should control an overwhelming portion of mining power, and 2) the adversary should prevent these two subset of miners from communicating with each other. As long as 2) does not hold, miners will know both forks and only accept the longer one, according to the longest chain rule.

Adversary only needs to satisfy 2), and he can do so in a **partially synchronous** network without violating any assumptions.

> True, this is the FLP impossibility. Nakamoto consensus works around FLP by two mesaures. First, Nakamoto consensus only provides probabilistic guarantee. Second, Nakamoto consensus is not live in asynchronous networks, but can be safe with overwhelming probability by having sufficient confirmation blocks.

What I refer is different from FLP impossibility. In brief, FLP says that deterministic consensus algorithm has infinite executions in **asynchronous** network. Again, this is different from partial synchronous network you mentioned in your first reply.

> I’m not sure if the “1/2 fault tolerance” results in the broken safety in asynchronous networks. Is there any paper proving this causality?

In the example I described we can break safety of Nakamoto consensus with probability 1 in a partially-**synchronous** or **asynchronous** network.

> Indeed, both the NoOps approach and the fee mechanism seem to be feasible.
> However, in this way, being included no longer means being valid. Then lightweight clients might have some problems. For example, a lightweight client may confirm that a transaction is included in a specific block (by communicating with other nodes), but cannot verify whether this transaction is valid.

Application layer validity would require additional mechanism. Similar to Ethereum, inclusion of a transaction does not imply that it is valid. One has to check the status in the transaction receipt. In Tuxedo, clients should take a similar approach. They should wait for the miners to compute the receipt first before accepting a transaction. Yes, this do introduces additional delay for computationally intensive transactions.

In section V of the paper, we do extend Tuxedo to include transactions that gets executed immediately and hence has same latency as standard PoW based blockchain.

---

**HAOYUatHZ** (2020-05-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/sebastianelvis/48/7342_2.png) SebastianElvis:

> I don’t think so. With sufficient confirmation blocks, PoW-based consensus can achieve both safety and liveness in asynchronous networks with overwhelming probability. See this paper https://eprint.iacr.org/2016/454.pdf. Nakamoto consensus does not need to rely on synchronous networks. The reason of assuming synchronous networks is to simply security proofs. I believe Tuxedo can be proven secure in asynchronous networks the same way, although complicated and tedious.

[Miller and LaViola also formalise Bitcoin in a Sync. model.](https://socrates1024.s3.amazonaws.com/consensus.pdf?spm=a2c65.11461447.0.0.4c15478eANvEh5&file=consensus.pdf).

I agree with you that:

![](https://ethresear.ch/user_avatar/ethresear.ch/sebastianelvis/48/7342_2.png) SebastianElvis:

> Nakamoto consensus works around FLP by two mesaures. First, Nakamoto consensus only provides probabilistic guarantee. Second, Nakamoto consensus is not live in asynchronous networks, but can be safe with overwhelming probability by having sufficient confirmation blocks.

But not sure whether Miller and LaViola do so just for simpler proof. They also admit that their model may be able to be extended to partial sync.

---

**SebastianElvis** (2020-05-31):

Thanks for correcting me. This paper is pretty clear to me now. Great work!

---

**HAOYUatHZ** (2020-05-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/sourav1547/48/4273_2.png) sourav1547:

> The paper you mentioned does the proof in the same network model as Tuxedo. This network model is more commonly referred as the synchronous network.

I find that you are right. It actually depends on the definitions.

https://eprint.iacr.org/2016/454.pdf analyses nakamoto consensus under “asynchronous

networks with ∆-bounded delays”,   which is “more commonly referred as the  **synchronous**  network.”

“fully asynchronous setting, where an adversary can arbitrarily delay messages” is instead, more commonly referred as the **asynchronous** network.

---

**adlerjohn** (2020-05-31):

Reviewer number: 1.

There are a number of incorrect claims in your paper. At a high level, as has been said over and over, consensus is not the bottleneck for blockchains today. An improved consensus protocol will not result in additional transaction throughput. The bottleneck for both Bitcoin and Ethereum is very much IBD and state growth, none of which are affected by delaying transaction execution.

Now, onto specifics. Non-exhaustively:

1. In Section IV-C:

> Recall  that  every  transaction  in  TUXEDO specifies  the maximum  amount  of  computation  resources  needed  for  its execution. Based on this specification, fees of every transaction in i^{th} block, B_i is collected in the same block. These fees are paid  using  the  native  token  of  TUXEDO, token1 (similar  to Ether  in  Ethereum).  Once  the  transaction  gets  executed,  any leftover  fees  i.e.,  fees  of  unused  computational  resources  are refunded  in B_i+ζ where  the  state  after  the  execution  of $B_i$’s transactions is reported.

This gas model doesn’t work simultaneously with delayed execution. The block producer can’t know how much gas a transaction will use unless they execute it immediately, which not only requires immediate execution, it requires immediate execution against the latest state (in other words, all previous blocks must also be executed prior to being able to mine a new block). Since this applies to all potential consensus nodes, all consensus nodes must validate all blocks immediately. Delayed execution doesn’t affect non-consensus nodes, so no nodes in the system can benefit from delayed execution.

The obvious "well, then we just don’t refund unused gas retort brings us to:

1. Imagine the following scenario. Alice has X ETH in her account. She sends 2 transactions: the first empties her account, the second posts a bunch of data on-chain as calldata (which would cost  He ought to find it more profitable to play by the rules, such rules that favour him with more new coins than everyone else combined, than to undermine the system and the validity of his own wealth.

Reviewer recommendation: reject.

