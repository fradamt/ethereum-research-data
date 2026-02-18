---
source: ethresearch
topic_id: 1058
title: Fork-free sharding
author: JustinDrake
date: "2018-02-12"
category: Sharding
tags: []
url: https://ethresear.ch/t/fork-free-sharding/1058
views: 5879
likes: 3
posts_count: 12
---

# Fork-free sharding

**TLDR**: This post describes a possible “end game” for sharding. Assuming the existence of data availability proofs we can design a non-trivial sharding scheme that is “fork-free”, i.e. where every collation header added to the MVC has exactly one child. Fork-free sharding enjoys fantastic properties by construction:

1. Optimal head fetching
2. Optimal asynchronous (or synchronous) cross-shard communication
3. Security and finality elevated to that of the main shard

**Background on consensus**

As I see it there are three fundamental local impediments to global consensus. Each impediment manifests itself at a physics level and at a networking level:

1. Ordering: What comes first? In physics, time is relative and there is no absolute clock. In networking, routing speeds are unpredictable because topologies are inhomogeneous and transports are unreliable.
2. Availability: What can be seen? In physics, the speed of light is finite and we have black holes. In networking, communication has latency and partitions happen.
3. Validity: What is real? In physics, we have Heisenberg’s uncertainty and other quantum effects. In networking, software and hardware stacks are inhomogeneous and buggy.

In distributed consensus the traditional approach to overcoming local impediments to consensus is fork-choice rules. In a quantum-like fashion, we accept simultaneous candidate realities to co-exist as parallel forks, and global consensus emerges/collapses from fork-choice rules and local “observation”. Unfortunately following fork-choice rules comes at a cost:

1. Evaluation cost: Evaluating forks for availability may require downloading lots of data, and evaluating forks for validity may require executing many transactions. With fork-choice rules, evaluation costs are technically unbounded in paralellism, and this is a vector for DoS attacks (at least until we have quantum computers and quantum networking). Evaluation costs in a fork-free setting are bounded in the classical computing setting.
2. Forking risk: There is opportunity cost following one fork versus another, i.e. a risk in choosing the wrong fork. For example, PoW mining on a wrong fork is wasting electricity. With a single chain you are always on the right chain, so opportunity costs as a miner/validator/executor goes away.
3. Impedance to security, speed and finality: Having the possibility to follow the wrong fork dilutes security of consensus, wastes proposals that don’t advance state, and/or impedes finality.

In the current sharding scheme we have to pay the price of fork-choice rules *twice*: once for the main shard, and once within the VMC. (When we separate ordering from execution, we may actually have *three* nested levels of fork-choice rules. One providing ordering to the VMC, another providing availability, and yet another providing validity.)

Below we give a sharding scheme where ordering, availability and validity is guaranteed by construction by the VMC from the collation headers, i.e. there is no fork-choice rule within the VMC.

**Construction**

The VMC already provides ordering. That is, given two collation headers added to the VMC, we know which was added first. For validity, we know of several ways to have valid-by-construction collations:

1. Put a SNARK/STARK in the collation header which proves that the collation root corresponds to a valid state transition, and have the VMC’s addHeader method check the proof.
2. Use log shards where any (hashable) blob of data can be parsed as a bounded list of logs (and/or transactions where garbage/invalid transactions are no-ops) and push state execution to a second-layer protocol, or to the application layer.

For data availability—and this is today’s key missing ingredient—we assume the existence of succinct and efficiently computable/verifiable proofs which the VMC checks.

**Discussion**

With the VMC gating collation headers to guarantee ordering, availability and validity of collation bodies, the logic for head fetching collapses to just “get the last collation header from the VMC”. Cross-shard communication is significantly easier because there is no re-org risk, as least not from the point of view of the VMC. The main thing that needs to be provided is replay protection in case the main shard reorgs, and this is provided by construction with stateless client witnesses.

The security of collation bodies elevates to the security of collation headers in the VMC. In particular, we have tight coupling, i.e. breaking a single shard means breaking the VMC, which means breaking the main shard. The time-to-finality of child shards also matches that of the main shard. So in a setup where the main shard has full Casper PoS with finality in minutes, child shards also enjoy finality in minutes.

As a side note for choosing the log shard approach vs the SNARK/STARK approach for validity, notice that the SNARK/STARK approaches is much stricter by disallowing “shard forks” below the VMC level. The state execution rules are frozen in the VMC until it is updated/replaced/forked, which requires intervention in the main shard. When execution is decoupled from availability (e.g. the log shard approach) forking a shard’s execution rules can be done independently at the shard level.

## Replies

**vbuterin** (2018-02-13):

Nice! I just happened to write a post expressing similar ideas, with a more concrete construction, at the same time: [A model for stage 4 "tightly coupled" sharding plus full Casper](https://ethresear.ch/t/a-model-for-stage-4-tightly-coupled-sharding-plus-full-casper/1065)

I’m actually not too worried about data availability proofs, at least in the short term, because we can just use an honest majority substitute in the short term. In my model, the fork choice rule for the main chain is driven largely by collations, and collations are implicitly endorsements of the chain, so if you are considering building on some chain, you could simply verify the availability of the last, say, 100 collations that have been built on the chain, and trust everything before then. In the long term, I agree better data availability checking constructions would massively improve the scheme and possibly let it scale super-quadratically.

---

**nate** (2018-02-22):

Some existing projects (e.g. Tendermint, Cosmos) have taken the fork-free method to the extreme - and even on the root shard (or, only shard) they don’t allow forks and require finality on a block before it’s added to the chain (essentially, a prepare and commit per block).

That being said, I think it’s worth pointing are that there are some real benefits to allowing forking. For example, if we allow forking, and also consider blocks as votes, then we can have O(1) messages per finalized block. The tradeoff here is that though there’s significantly higher latency to finality, on the order of the number of validators, the protocol can reasonably support more validators (in the extreme no-fork case, O(n) messages are needed before advancing to the next block).

It seems most reasonable we’ll end up somewhere in the middle on the root shard - where both votes are votes *and* blocks are votes, and so we have a reasonable time to finality while also supporting a larger number of validators.

That being said, as the shards that exist in this scheme all delegate their forkchoice to the root shard/VMC, I don’t think we can actually take advantage of the above benefits of having forking, which make it seem like there aren’t many, if any, disadvantages to going fork-free, in this model ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=9)

---

**nate** (2018-02-22):

That being said, it’s also worth noting that we can get some of the benefits of this proposed scheme while still allowing forking (with the exception of optimal head fetching, obviously).

For optimal synchronous cross-shard communication, for example, we can simply enforce “atomicity of cross-shard blocks” before finality is reached. Essentially, if a merge block is in the fork choice of one shard it’s merged with, then it must be in the forkchoice of the other shard it’s merged with. Note that does require an ordering between shards that have a block “merge mined” between them.

Current CBC Casper sharding goes a bit farther and organizes the shards in a binary tree, where blocks can be merged between any two shards that are connected in the tree. Though this has problems of its own, if we add SNARKs/STARKs, you can imagine that when we can get security and finality on the shards that is equivalent to the main shard - when we get finality on a root shard block that merges with chains beneath it.

This is obviously a very different model - but I thought it was worth pointing out that going fork-free isn’t the only way of getting these benefits ![:fork_and_knife:](https://ethresear.ch/images/emoji/facebook_messenger/fork_and_knife.png?v=9)

---

**vbuterin** (2018-02-23):

Whether or not an algo is fork-free or not is a bit of a red herring, because it all depends on whether or not clients listen to partial confirmations. For example, in PBFT, you can have a client with a rule like “if piece of data X has 10 more prepares than any conflicting piece of data, then I will show it as partially confirmed”; this then makes PBFT forkful. In Casper FFG, you can have a client that refuses to show any blocks until they are finalized, and this makes Casper FFG fork-free. In an important philosophical sense, *any consensus algorithm where you can make intelligent guesses about what data will be finalized before finality technically happens is forkful*; it’s just a question of whether or not clients show the forkfulness. And you can probably prove that the only non-fully-synchronous consensus algo that doesn’t have that property is a dictator.

Now that we have that established, the next step is to point out that a chain-based data structure is really convenient, for a few reasons:

1. It allows us to merge different stages of confirmation for different pieces of data - for example, in Casper FFG, a vote for epoch N corresponds to a PBFT prepare for epoch N and a PBFT commit for epoch N-1. This double-duty reduces concrete finality latency by ~17% with no tradeoffs (as an average transaction needs to wait for 2.5 instead of 3 messaging rounds to finalize). In PoW, block N is an Mth confirmation for block N-M, for all M <= N; if this massive multi-duty function of blocks did not exist, every new PoW would have to separately mention what value it’s voting for in every previous height.
2. It allows us to merge the concept of leader election rounds (PBFT “views”) and transaction sequencing rounds (PBFT “sequence numbers”).
3. It allows us to merge proposals and prepare/commit messages, reducing overhead further.

I actually believe that a truly optimal version of Casper FFG could reduce finality latency by ~20% further with no tradeoffs except for algorithmic complexity, by taking full advantage of the fact that a reference to a block is also a reference to all of its ancestors. Casper CBC should be able to make this optimization and achieve total optimality in even its current form.

---

**kladkogex** (2018-02-23):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/n/e95f7d/48.png) nate:

> Some existing projects (e.g. Tendermint, Cosmos) have taken the fork-free method to the extreme -

I think that Tendermint whitepaper proves things under assumption of a reliable and synchronous network.

Real life networks are not reliable - packets get lost and misrouted.  I have a strong suspicion that one can show that because Tendermint does not allow forks it can get totally stuck in a real network. In particular,  TenderMint requires a node to receive 2/3 of pre-commits to commit. If some of the the pre-commits for some nodes are lost,  it seems that once can get into a situation where a minority of nodes will commit, and the rest of the nodes will proceed to the next round, which effectively will create a fork, but since Tenfermint does not allow forks the system will  get totally stuck!

I think only truly asyncronous consensus protocols can be forkless.   And the reason why asynchronous protocols can be forkless is because for fully asynchronous consensus protocols an unreliable network can be made effectively 100% reliable by retransmissions.  Node A sending a message to node B can retransmit if it does not receive a confirmation, where the retransmisison period can exponentially increase with time.

To my knowledge there is no real-life crypto currency based on Tendermint, and when Cosmos network is released,  it may well be that the system will get totally stuck because it is based on an assumption of a synchronous  and reliable network - this may be a very embarrassing moment for these guys!

---

**MaxC** (2018-02-28):

Fork-free sharding does sound like it would be simpler. It is how I’ve also been thinking about sharding.

**Pros:** Fork-free sharding makes doing data availability proofs simpler, and eliminates the need to do cross-chain forkful reverts, which might involve lots of roll-backs on other shards.

**Cons**: I guess the difficulty is in ensuring enough checks and balances are in place to make sure that finality can be given after every block, whilst still ensuring validity, availability etc.

---

**MaxC** (2018-02-28):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Real life networks are not reliable - packets get lost and misrouted.  I have a strong suspicion that one can show that because Tendermint does not allow forks it can get totally stuck in a real network. In particular,  TenderMint requires a node to receive 2/3 of pre-commits to commit. If some of the the pre-commits for some nodes are lost,  it seems that once can get into a situation where a minority of nodes will commit, and the rest of the nodes will proceed to the next round, which effectively will create a fork, but since Tenfermint does not allow forks the system will  get totally stuck!

In the real world why would the stuck nodes not just re-request messages from those they haven’t heard from? Is this really a big problem?

---

**kladkogex** (2018-03-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> In the real world why would the stuck nodes not just re-request messages from those they haven’t heard from? Is this really a big problem?

Well, Tendermint does not re-request messages …

> At the end of the P recommit step each node makes a decision. If the node had received more than 2/3 of precommits for a particular block, then the node enters the  Commit step. Otherwise it continues onto the Propose step of the next round. Even if a node hadn’t yet received the block precommitted by the network,
> it enters the Commit step.

A problem with Tendermint is that it is not a mathematically proven thing, there are no proofs in the whitepaper and it is known that Tendermint was getting stuck in its first iteration,  they seem to fix it, but it is not clear whether more ways for it to get stuck exist or not. They say it is based on a 1988 paper



      [groups.csail.mit.edu](https://groups.csail.mit.edu/tds/papers/Lynch/jacm88.pdf)



    https://groups.csail.mit.edu/tds/papers/Lynch/jacm88.pdf

###



3.04 MB










which assumes a synchronous network, meaning that there is a fixed latency bound for all communications.

---

**vbuterin** (2018-03-01):

I believe the 1988 paper assumes partial synchrony, so there is a latency bound, but if latency exceeds the bound that only temporarily prevents liveness, without risking safety.

Casper FFG operates under a similar model.

---

**kladkogex** (2018-03-01):

Below is an interesting discussion of partial synchrony in the HoneyBadgerBFT paper

Almost all modern BFT protocols rely on timing assumptions

(such as partial or weak synchrony) to guarantee liveness. Purely

asynchronous BFT protocols have received considerably less attention in recent years. Consider the following argument, which, if it held, would justify this narrowed focus:

Weak synchrony assumptions are unavoidable, since in any

network that violates these assumptions, even asynchronous

protocols would provide unacceptable performance.

In this section, we present two counterarguments that refute

the premise above. First, we illustrate the theoretical separation

between the asynchronous and weakly synchronous network models.

Specifically we construct an adversarial network scheduler that

violates PBFT’s weak synchrony assumption (and indeed causes it

to fail) but under which any purely asynchronous protocol (such

as HoneyBadgerBFT) makes good progress. Second, we make a

practical observation: even when their assumptions are met, weakly synchronous protocols are slow to recover from a network partition once it heals, whereas asynchronous protocols make progress as soon as messages are delivered

Specifically we construct an adversarial network scheduler that

violates PBFT’s weak synchrony assumption (and indeed causes it

to fail) but under which any purely asynchronous protocol (such

as HoneyBadgerBFT) makes good progress. Second, we make a

practical observation: even when their assumptions are met, weakly synchronous protocols are slow to recover from a network partition once it heals, whereas asynchronous protocols make progress as soon as messages are delivered

The intuition behind our scheduler is simple. First, we assume

that a single node has crashed. Then, the network delays messages whenever a correct node is the leader, preventing progress and causing the next node in round-robin order to become the new leader. When the crashed node is the next up to become the leader, the scheduler immediately heals the network partition and delivers messages very rapidly among the honest nodes; however, since the leader has crashed, no progress is made here either.

This attack violates the weak synchrony assumption because it

must delay messages for longer and longer each cycle, since PBFT widens its timeout interval after each failed leader election.

On the other hand, it provides larger and larger periods of synchrony as well.

However, since these periods of synchrony occur at inconvenient

times, PBFT is unable to make use of them. Looking ahead, HoneyBadgerBFT, and indeed any asynchronous protocol, would be able to make progress during these opportunistic periods of synchrony. To confirm our analysis, we implemented this malicious scheduler as a proxy that intercepted and delayed all view change messages to the new leader, and tested it against a 1200 line Python implementation of PBFT. The results and message logs we observed were consistent with the above analysis; our replicas became stuck in a loop requesting view changes that never succeeded.

---

**kladkogex** (2018-03-01):

I am not claiming to be a super expert in this, but imho it is a question whether a proof under a  weak synchrony assumption is equivalent to a proof that a system will never get totally stuck in a real network …

