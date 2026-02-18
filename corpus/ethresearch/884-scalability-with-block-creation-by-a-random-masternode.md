---
source: ethresearch
topic_id: 884
title: Scalability with block creation by a random Masternode
author: Etherbuddy
date: "2018-01-24"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/scalability-with-block-creation-by-a-random-masternode/884
views: 5593
likes: 8
posts_count: 4
---

# Scalability with block creation by a random Masternode

Hello,

These days I’m studying DPOS more closely, and it’s a very scalable protocol. It can manage thousands of transactions per second.

Under DPOS, 1 node, chosen among elected witnesses, is building the next block.

For example, with the Bitshares client, block creation is showing up swiftly every few seconds. EOS will do the same in a few months.

Personally, I think the election of witnesses may create flaws, and additionally it leads to centralization, since this is nearly always the same nodes who build blocks.

An alternative would be to choose a random masternode to build the next block.

In a network of a few hundreds or thousands masternodes, choosing one random masternode would deliver the same scalability without the need of any election.

Every other masternodes would check the block produced.

If the chosen masternode fails to deliver the next block, he would receive no fee, and if he builds a bad block, he would get a penalty.

On its website, Bitshares explains : http://docs.bitshares.org/bitshares/dpos.html :

> Reasons to not randomly select representatives from all users
>
>
> High probability they are not online.
> Attackers would gain control proportional to their stake, without any peer review.

But if only masternodes which are online are allowed to build blocks, and if each block is checked by other masternodes, these objections are no more relevant.

So why not considering this simple solution ?

Letting a random masternode build the next block.

It could deliver a very good scalability.

And it would be pretty safe, since it’s close to the successful POS protocol of NXT, which uses a deterministic algorithm to select a random shareholder to generate the next block.

## Replies

**vbuterin** (2018-01-24):

This will give no scalability improvements whatsoever. The effort of creating a block and the effort of verifying a block are exactly the same, and it’s the effort of verifying the blocks that’s really the bottleneck.

EOS’s scalability is NOT because of DPOS or anything similar; its claimed scalability comes entirely from the fact that it requires each node to have a much higher computational capacity, making it impossible for anyone but large businesses to run full nodes. We could do that too, but won’t because it’s contrary to the goals of decentralization.

Asterisk: it’s actually a totally reasonable strategy… inside of a Plasma chain. Hence why there’s https://github.com/ethereum/plasma, https://github.com/ethereum-plasma and several other projects.

---

**kladkogex** (2018-01-25):

My understanding from reading the EOS whitepaper was that they are running a small number of super powerful nodes - 21 nodes as I recall …  As Vitalik mentioned, the nodes need to be super powerful, because they have an algorithm to parallelize to a certain degree smartcontract validation. Essentially messages that go to separate smartcontracts can be processed in parallel to some degree.   My understanding is they did not demonstrate this parallelization algorithm yet, so the current incarnation of their chain does not actually run so fast.

My understanding is another problem they will have is storage, all these messages will need to be stored, so the servers will also need to have lots of storage capacity.

Imho a DPOS network is essentially a permissioned network,  because becoming a node is super hard.  Yes, you could theoretically have a campaign for people to elect your node, but it is almost like becoming a US president - anyone can become a candidate but then passing elections is superhard.   It seems to me that EOS is really pushing the boundary,  if the entire world runs on 21 nodes controlled by some people, then what kind of a decentralized network is that.

A funny thing is, if they really run 21 nodes, than almost for sure at some point someone will hack all these 21 nodes at once, so the entire network can essentially be decimated …

---

**vbuterin** (2018-01-25):

> As Vitalik mentioned, the nodes need to be super powerful, because they have an algorithm to parallelize to a certain degree smartcontract validation

It’s worth noting that [Easy parallelizability · Issue #648 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/648) can provide this for Ethereum as it exists, and the stateless client scalability proposal also implicitly accomplishes this.

