---
source: magicians
topic_id: 5453
title: "Weak statelessness and/or state expiry: coming soon"
author: vbuterin
date: "2021-03-02"
category: Working Groups > Ethereum 1.x Ring
tags: []
url: https://ethereum-magicians.org/t/weak-statelessness-and-or-state-expiry-coming-soon/5453
views: 2597
likes: 6
posts_count: 2
---

# Weak statelessness and/or state expiry: coming soon

One of the next major challenges for the Ethereum base layer is that of dealing with the growing state size: currently around 100 GB including tree nodes and growing by around 50 GB per year. The growing state is making it increasingly harder to sync the ethereum chain and to participate as a validator, and risks increasing network centralization if the state grows, especially if the gas limit is increased further.

There are two main techniques being proposed for how to deal with this problem for the short term:

- State expiry: remove state that has not been recently accessed from the state (think: accessed in the last year), and require witnesses to revive expired state. This would reduce the state that everyone needs to store to a flat ~20-50 GB.
- Weak statelessness: only require block proposers to store state, and allow all other nodes to verify blocks statelessly.

There is also the longer-term option of **full statelessness**, which can be viewed as either one of the above ideas taken to the extreme (it’s either state expiry with a time-to-expiry of zero, or weak statelessness but where block proposers too don’t have to store any state), but it’s more challenging so arguably not worth spending too much time to consider in the short term.

There are many challenges with both state expiry and weak statelessness (eg. see [my recent doc](https://hackmd.io/@HWeNw8hNRimMm2m2GH56Cw/state_size_management)), though in both cases we have recently seen significant improvements that greatly mitigate these challenges.

In the case of **state expiry**, the key challenges are:

- How to actually structure the state so that unused pieces of it expire (do we store “stubs” in the tree, do we move it to a separate tree, or something else entirely?). Do we do it at account-level granularity or storage-slot-level granularity? (I favor storage-slot-level granularity)
- How to expire state, particularly do we expire continuously vs in discrete epochs (eg. an epoch could be 1 year long). “ReGenesis” is a name that is often used to describe the second strategy.
- How to handle resurrection conflicts.  Resurrection conflicts are an important concept. Suppose some account or storage slot gets created at some address/position. That account or storage slot is then expired. Then, that account or storage slot gets refilled again at that same position. Finally, someone attempts to recover the original object that got expired. How do we resolve the conflict between the expired-and-recovered state and the newly created state? See this section of my doc for more details.

In the case of **weak statelessness**, the key challenges are:

- Gas repricings to bound the maximum size of a witness (EIP 2929 solves most of this; but we still need to add a cost to access each chunk of contract code once we introduce code Merklization)
- Witness sizes: the extra data needed to prove the validity of a block to a client without the state, even with repricings, is ~4 MB, which is still a little bit too large to safely broadcast through the network every 13 seconds.
- Transaction broadcasting in the mempool: how would transactions be broadcasted and verified if clients can’t directly access the state to verify that the nonce is correct and the transaction has enough ETH to pay its fee?

Fortunately, there has recently been a lot of headway made on both approaches, and some recent developments seem to address most people’s concerns:

- Some techniques for how a ReGenesis-like epoch-based expiry scheme can be adapted to minimize resurrection conflicts
- Piper Merriam’s work on transaction gossip networks that add witnesses to be stateless-client-friendly, and his work on distributed state storage and on-demand availability
- Verkle trees, which can reduce worst-case witness sizes from ~4 MB to ~800 kB (this is definitely small enough, because existing worst-case blocks that are full of calldata are already 12.5M / 16 ~= 780 kB and we have to handle those anyway). See slides, doc, code.

### From theory to practice

Both solutions are well underway in development, and it feels like around now is the time to switch gear from seeing these ideas as research problems to seeing them as concrete paths of which at least one (and perhaps eventually both) need to be implemented into Ethereum.

One challenge is prioritization: if we have to do one of the two first, which one is more important? Dankrad has a [case for weak statelessness](https://notes.ethereum.org/WUUUXBKWQXORxpFMlLWy-w); it would be interesting to also see the case for state expiry (I don’t know of a doc which makes that case, but perhaps there should be!).

A second challenge is getting the ecosystem ready for the costs of the transition. Some example challenges include:

- Weak statelessness will require replacing binary trees with verkle trees, which break all existing Merkle branch verifiers (whether in client code or in smart contract code)
- Verkle trees would require changing client sync protocols.
- We will need to add a per-chunk gas cost (eg. 500 gas for every 32-byte chunk of code accessed), which will render some applications more expensive than they are today.
- The state expiry scheme would require contracts to redesign themselves to efficiently use new state (the idea is that the schemes currently available for solving resurrection conflicts involve a concept of “old state regions” and “new state regions” where creating an object in an old state region requires submitting proofs that grow over time while creating an object in a new state region does not, and so eg. token contracts would require new versions and architectures to handle this well, though they would continue to work but with reduced convenience and higher gas costs if they are not upgraded)
- Dapps that depend on history accesses would need to switch to some extra-protocol/L2 mechanism (TheGraph?) to access things older than 1 year.

### Benefits

Dealing with the above issues is a significant amount of effort. But there are important rewards on the other side that make this worthwhile:

- Increasing the number of people who can run an ethereum node, helping to keep Ethereum decentralized and reducing “Infura dependency risk”
- Enabling stateless ethereum validation, greatly reducing the costs of staking: potentially, nodes could even selectively validate ethereum application data, eg. only if they are attesting to that block. This brings us closer to the dream of safeguarding the ability to stake using easily-accessible consumer hardware (even phones!) for the long term
- Increasing the gas limit: reducing state size for clients allows us to safely push the gas limit significantly higher, lowering transaction costs for users. A reduced state size means that more of the state can be in memory, reducing the cost of each individual state access, further opening the way for safe gas limit increases.
- Giving application developers confidence that after this, the protocol economics can be solidified and changed much less in the future, because the main remaining economic misalignment in the protocol (state that a user pays for once needing to be stored forever) would be gone.

I hope that we can have more discussion on these topics to get started on making the necessary preparations to fix our state problems and pave the way for higher L1 efficiency and scalability soon!

## Replies

**setunapo** (2023-02-24):

We did many investigations on StateExpiry, including your posts of the Epoch based state expiry solution.

I learnt a lot and I believe there is tons of work need to be done to support it, since it is really a huge project, which will impact the ecosystem a lot.

Recently, we raised a much practical proposal to support StateExpiry on BNB Smart Chain, detail can be found: [BEPs/BEP206.md at bep205_state_expiry · setunapo/BEPs · GitHub](https://github.com/setunapo/BEPs/blob/bep205_state_expiry/BEP206.md)

The main idea is to keep the AccountTrie, while only expire the StorageTrie. It may not a comprehensive solution, but it would have less impact on ecosystem, meanwhile help mitigate the storage pressure.

Could you help check and give some advice on this proposal?

