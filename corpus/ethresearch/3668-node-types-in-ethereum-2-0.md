---
source: ethresearch
topic_id: 3668
title: Node types in Ethereum 2.0
author: MihailoBjelic
date: "2018-10-02"
category: Sharding
tags: []
url: https://ethresear.ch/t/node-types-in-ethereum-2-0/3668
views: 6511
likes: 21
posts_count: 19
---

# Node types in Ethereum 2.0

From the [Sharding FAQ](https://github.com/ethereum/wiki/wiki/Sharding-FAQs#what-might-a-basic-design-of-a-sharded-blockchain-look-like):

"Note that there are now several ‘levels’ of nodes that can exist in such a system:

- Super-full node  - fully downloads every collation of every shard, as well as the main chain, fully verifying everything.
- Top-level node  - processes all main chain blocks, giving them “light client” access to all shards.
- Single-shard node  - acts as a top-level node, but also fully downloads and verifies every collation on some specific shard that it cares more about.
- Light node  - downloads and verifies the block headers of main chain blocks only; does not process any collation headers or transactions unless it needs to read some specific entry in the state of some specific shard, in which case it downloads the Merkle branch to the most recent collation header for that shard and from there downloads the Merkle proof of the desired value in the state."

I have a few questions in the context of Eth 2.0:

1. Why do these super-full nodes have to verify all transactions (the main chain + all the shards), it will take a LOT of resources and I don’t see the point? Storing everything makes sense (it ensures data availability of all the data), but it will also require a lot of disk space and bandwidth?
2. I don’t get what/why these top-level nodes do?
3. The single-shard nodes get periodically reshuffled. How do they “hand over” the data to the next elected node?
4. So light clients only download the main chain headers?

Is this all maybe outdated (things have changed/will change now when we merged Casper and sharding)?

Thanks!

## Replies

**meyer9** (2018-10-03):

1. These aren’t nodes that have to be run. These are just the possible nodes that can be run. In the case of having a super-full node, some staking pools might want to do that so they don’t have to resync to a different shard each cycle for each validator.
2. They only validate the beacon chain, so they only have access to headers of shards and do not actually validate shard transactions or process shard blocks.
3. They generate collations and add them to the shard chain. That’s like asking how do Bitcoin miners hand off data to the next Bitcoin miner.
4. Yes.

---

**jannikluhn** (2018-10-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> The single-shard nodes get periodically reshuffled.

Not necessarily, only validators are being shuffled, “normal” single-shard nodes (e.g. from users who are interacting with some contract on that shard) can stay on one shard permanently.

---

**MihailoBjelic** (2018-10-04):

Thanks [@meyer9](/u/meyer9) and [@jannikluhn](/u/jannikluhn). ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/meyer9/48/1941_2.png) meyer9:

> These aren’t nodes that have to be run. These are just the possible nodes that can be run. In the case of having a super-full node, some staking pools might want to do that so they don’t have to resync to a different shard each cycle for each validator.

If we don’t have these super-full nodes, how can we guarantee the data availability of the entire system (what if e.g. a single shard gets corrupted or attacked and we don’t have its data anymore)?

![](https://ethresear.ch/user_avatar/ethresear.ch/meyer9/48/1941_2.png) meyer9:

> They only validate the beacon chain, so they only have access to headers of shards and do not actually validate shard transactions or process shard blocks.

What’s the point/reason for having nodes that do only this? I was thinking that every single validator needs to do this (validate the beacon chain and keep track of all the shards’ headers) anyway, I though of it as some default, base level function?

![](https://ethresear.ch/user_avatar/ethresear.ch/meyer9/48/1941_2.png) meyer9:

> They generate collations and add them to the shard chain. That’s like asking how do Bitcoin miners hand off data to the next Bitcoin miner

I believe this comparison makes no sense. If I got it right, “single-shard nodes” are referred to as operators in [this presentation](https://www.youtube.com/watch?v=J4rylD6w2S4) by [@JustinDrake](/u/justindrake), and it’s clearly stated that they are being reshuffled e.g. once per week (Bitcon miners/nodes are not being reshuffled). That said, it’s clear that, when the new group of validators is selected, the old operators (single-shard nodes) should “hand over” all the shard data (the whole chain) to the new operators (they don’t have this data, they only have that shard’s headers). Now when I think about t, the problem is even deeper than I originally thought, I might start a new topic on it.

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> Not necessarily, only validators are being shuffled, “normal” single-shard nodes (e.g. from users who are interacting with some contract on that shard) can stay on one shard permanently.

Can you please share where did you get the information that only validators are being reshuffled? That would completely change the model and introduce completely new challenges/concerns (I can go into more details if this is confirmed). And of course, we can have permanent single-shard nodes run by users, but those are irrelevant for the analysis (not mandatory/guaranteed + not staked → can not be relied on).

---

**vbuterin** (2018-10-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> If we don’t have these super-full nodes, how can we guarantee the data availability of the entire system (what if e.g. a single shard gets corrupted or attacked and we don’t have its data anymore)?

Because of shuffling, there’s a strong probabilistic guarantee that a single shard can’t get attacked or corrupted without basically an attacker having close to 50% of the entire validator set, and if/when we add fraud proofs and data availability proofs, the entire network will be able to reject bad blocks without checking all of the data.

> Can you please share where did you get the information that only validators are being reshuffled?

From me ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

Any node that is *not* a validator is a node that is simply being run for its own user’s benefit, so that node can of course listen to and download or not download and check or not check whatever it wants. So the protocol has no ability to compel these other nodes to go on any specific shard, and no reason to.

---

**MihailoBjelic** (2018-10-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> From me

Oh, than I’ll consider that information pretty reliable! ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=12) So that means that Sharding FAQs and the Justin’s presentation (or at least their parts) are deprecated?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Any node that is not a validator is a node that is simply being run for its own user’s benefit, so that node can of course listen to and download or not download and check or not check whatever it wants. So the protocol has no ability to compel these other nodes to go on any specific shard, and no reason to.

I think mentioning these user-run nodes just brings confusion, they’re irrelevant because they (as you and I both said) offer no guarantees on anything at all, they are **unbonded** and **might** or **might not** validate and/or keep any shard’s data (or arbitrary portions of it). Validators must not rely on these nodes at any moment, they need nodes that are **bonded** and **will/must** validate every shard collation and keep all the shard’s data (the whole, up-to-date shard chain). How many of these nodes will we have per shard? If it’s one, there are several concerns, if it’s more than one, there are several other concerns (again, I can go into more details if I have this answer). ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) If these things are still not fully specified, it’s understandable, of course.

---

**drcode1** (2018-10-05):

One detail to keep in mind is that the “light clients” for sharding will likely also have the responsibility of uploading data to full nodes, not something that you’d typically think of as a light client duty. To quote Vitalik et al’s recent light client spec, which I assume uses the same data availability mechanism as eth 2.0: “Each share and valid Merkle proof that is received by the light client is gossiped to all the full nodes that the light client is connected to if the full nodes do not have them”

> I think mentioning these user-run nodes just brings confusion

I’m no expert on the game theory here, I’ll just point out that 100% of bittorrent nodes are unbonded and have no duty to serve up data or validate: Default behavior of software (plus a few altruists) can lead to a powerful mechanism with meaningful effects on a distributed software system.

---

**MihailoBjelic** (2018-10-05):

Thanks [@drcode1](/u/drcode1)! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/drcode1/48/707_2.png) drcode1:

> I’ll just point out that 100% of bittorrent nodes are unbonded and have no duty to serve up data or validate

Exactly, and BitTorrent is the perfect example of an unreliable distributed network (everyone experienced unavailable torrent links). The same goes for IPFS, that’s why Filecoin is being built (you need **bonded** people that **have to** keep the data if you want to offer guarantees on that data being available, and even then the problem is far from trivial). And that is exactly why I consider these user/altruist-run nodes should not be relied upon at all, i.e. they shouldn’t even be considered when discussing safety and guarantees of the system.

That said, I would still really like to know:

a) are we going to have bonded single-shard nodes (nodes that have to download and keep all the data of a single shard),

b) are we definitely not going to reshuffle them,

c) are they the same thing/entity as proposers (they propose blocks/collations and validators vote on them),

d) how many of them will we have per shard?

I’ve just watched an awesome presentation on Ethereum networking by Peter Szilagyi and Felix Lange, and [here](https://youtu.be/qJA6J0mP73w?t=3841) you can see that the plan at the time was for collators to constantly switch shards (it it’s unclear whether or not collators are the same as proposers/single-shard nodes, though  ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)).

---

**daniel** (2018-10-11):

Very good questions! I’ve been wondering about exactly this topic for quite some time now and I would like to offer some answers that are purely my opinion and intuition for now:

a) Yes! I don’t see another way to guarantee long-term data availability

b) Depends. As of now, I don’t think it would be required to reshuffle them in practice, but I feel like for guaranteeing provable liveness, reshuffling might be necessary. Otherwise a bribing attacker might be able to entirely stall a shard by never proposing any collation to vote on.

c) Yes! I think the highest synergy effect (and therefore efficiency) could be achieved by combining the responsibilities of long-term state storage + execution of transactions + proposing of collations into the same role.

d) That’s an interesting and open question. If we don’t “assign” or “shuffle” (let’s call them) *executors*, then we have no control over this anyway and it’s up to economic incentives to achieve a reasonable distribution over all shards. If we do assign them, I have not thought about reasonable numbers yet.

---

**MihailoBjelic** (2018-10-11):

Thanks for the comments [@daniel](/u/daniel)! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

I agree with most of the things you wrote.

From the research standpoint, d) (number of single-shard nodes per shard) is particularly interesting. If we have one, it’s a SPOF of every shard ![:see_no_evil:](https://ethresear.ch/images/emoji/facebook_messenger/see_no_evil.png?v=9); if we have more, a very interesting problem of syncing and coordination is introduced (if this is not solved properly, we can actually end up with “multiple SPOFs” per shard, i.e. any of these nodes can permanently halt the shard ![:see_no_evil:](https://ethresear.ch/images/emoji/facebook_messenger/see_no_evil.png?v=9)![:see_no_evil:](https://ethresear.ch/images/emoji/facebook_messenger/see_no_evil.png?v=9)). Polkadot, for example, has multiple “collators” (their version of single-shard nodes) per “parachain” (their  version of sidechains, quite similar to Eth shards); I’ve discussed this problem with them and they still don’t have the solution (it’s still an open problem).

And yes, in my previous post I forgot to put: e) are we having these super-full nodes (nodes that store every collation of every shard)? ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**daniel** (2018-10-13):

d) Definitely more than 1. Since validators don’t verify the computational results of executing a transaction, every shard needs at least one executor who was not the proposer, so incorrect results can be challenged. Two is still very low speaking in terms of fault tolerance, however a reasonable number depends a lot on the incentive mechanism given to executors for joining a shard (if we allow them to) or for becoming an executor in the first place (if we assign executors in the protocol as we do with validators). I would be very happy to hear any ideas and thoughts on this ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

d.2) I don’t think we would end up with multiple SPOF in this construct. My suggestion would be to require (or incentivize) every executor in shard X to keep up to date with the entire state in shard X. They will be able to acquire the current state the same way full nodes currently do in Ethereum 1.0. Executors are generally implicitly incentivized to

1. Keep the entire state available for themselves in order to not restrict themselves from which transactions they can execute
2. Freely share the state in order to enable users (which we assume most will be light clients) to send transactions, which is required to give them something to execute in the first place

e) I guess we will have them, but they are not required or incentivized by the network / protocol itself. Requiring supernodes for the network to function kind of defeats the whole purpose of sharding and poses a great centralization risk. However, some project like [etherscan.io](http://etherscan.io) might be interested in running a supernode for external motivations.

---

**jrhea** (2018-10-25):

I faced a similar problem in a project i worked on called Arithmetica where we were developing a prototype to create a distributed platform for computational math and physics. We used libP2P pubsub to create topics that workers could subscribe to and participate in the solution. We needed a way to assign work to workers without much chatter and no rework.  We landed on an emergent/leaderless approach that required very little chatter between nodes to stay in sync.  A similar technique could help single shard nodes on the same shard coordinate what work to take and schedule when to sync.  I attached a draft write-up of the algorithm…if u are interested:

[work scheduling algorithm.pdf](https://ethresear.ch/uploads/default/original/2X/c/c8293129ba59094438dbd2ecdce79fe5ddac3ab6.pdf) (73.8 KB)

---

**LeapM** (2018-10-25):

I understandings:

1. Before phase 2 (state execution) is completed, less than 1/3 of shard proposers and shard attesters  are reelected very cycle, 2/3 of original shard validators set are reminded in the same shard. It helps data availability
2. proof of custody, after shard validators leave the current shard, he may still keep the shard data for later challenging, not mandatory, but he may do it.
3. big stake pools most likely have all shard data
4. Once phase2 completed, executors may always stay in this same shard, it helps data availability.

---

**MihailoBjelic** (2018-11-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/daniel/48/146_2.png) daniel:

> d) Definitely more than 1. Since validators don’t verify the computational results of executing a transaction, every shard needs at least one executor who was not the proposer, so incorrect results can be challenged.

I’m not sure if other shard nodes should challenge incorrect collations, I thought the validators should simply reject them (not in this first phase, though, now they only verify their existence/data blobs).

![](https://ethresear.ch/user_avatar/ethresear.ch/daniel/48/146_2.png) daniel:

> My suggestion would be to require (or incentivize) every executor in shard X to keep up to date with the entire state in shard X.

I agree, but this then requires some “syncing model”, i.e. consensus algorithm between these nodes. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/daniel/48/146_2.png) daniel:

> e) I guess we will have them, but they are not required or incentivized by the network / protocol itself. Requiring supernodes for the network to function kind of defeats the whole purpose of sharding and poses a great centralization risk.

Agree with this, too, but then how can we ensure data availability of the whole system (every shard)?

---

**MihailoBjelic** (2018-11-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/jrhea/48/1406_2.png) jrhea:

> I faced a similar problem in a project i worked on called Arithmetica where we were developing a prototype to create a distributed platform for computational math and physics.

I know it’s unrelated to this discussion, but I’ve checked the website and it looks interesting. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) Can you briefly describe differences/advantages over “old-school” grid computing projects like SETI? Just curious, you don’t have to bother if you’re busy/lazy… ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/jrhea/48/1406_2.png) jrhea:

> We used libP2P pubsub to create topics that workers could subscribe to and participate in the solution.

Nice. I believe even Ethereum 2.0 will be using Libp2p PubSub, and I’m pretty convinced that that’s the best solution.

![](https://ethresear.ch/user_avatar/ethresear.ch/jrhea/48/1406_2.png) jrhea:

> We landed on an emergent/leaderless approach that required very little chatter between nodes to stay in sync. A similar technique could help single shard nodes on the same shard coordinate what work to take and schedule when to sync. I attached a draft write-up of the algorithm…if u are interested:

Thank you for sharing this. ![:blush:](https://ethresear.ch/images/emoji/facebook_messenger/blush.png?v=12) The model is very simple, and simple solutions are always the best (when they do the job).

To me it looks like it really does the job for work scheduling, but I’m not sure about the data syncing… I guess every node needs to keep an eye on the scheduler and as soon as e.g. Peer 3 finishes the work assigned to them in the Epoch 2, all other nodes should pull the “fresh” data from Peer 3? In this case, I think we need to have some sort of confirmations form other nodes that they have indeed downloaded the data, which practically means we need a consensus algorithm (maybe it even needs to be BFT, I’m not sure). ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) Maybe I’m missing something?

---

**jrhea** (2018-11-04):

> Can you briefly describe differences/advantages over “old-school” grid computing projects like SETI?

I’d be happy to. I’ll keep it brief, but if you want more info I have a longer winded explanation. Projects like SETI, Folding@home, Asteroids@home, etc all use BOINC. BOINC can be frustrating to install and non trivial to create new problems. It is also what I like to call centralized command and control. So it is essentially a single point of failure. Arithmetica is emergent/leaderless and runs in a browser so it is easy to onboard.

> Thank you for sharing this.  The model is very simple, and simple solutions are always the best (when they do the job).

My pleasure and very well said

> I’m not sure about the data syncing

Glad you pointed that out bc I never got around to writing that down formally. I should probably do that ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

> guess every node needs to keep an eye on the scheduler and as soon as e.g. Peer 3 finishes the work assigned to them in the Epoch 2, all other nodes should pull the “fresh” data from Peer 3?

This is essentially correct. I just wanted to clarify a couple of things. Since there is no leader, the scheduler is an emergent property of all the nodes - they all know what to do. If one node loses connectivity, or stops producing work, then the other nodes notice it and weave the extra work into their queue.

All the nodes know when Peer 3 is done bc it broadcasts a small message to the room to inform other peers that Peer 3’s Epoch 2 work is complete and also provides an ipfs content hash so the other peers know where to find it.

Nodes can confirm that they have all synced up correctly by periodically comparing the content hash of their data every N epochs.

This gives us several tunable parameters to play with:

- num work items per epoch
- num of epochs required before nodes verify they are all in sync
- some other’s I can’t think of at the moment

Tunable parameters are nice bc it could allow us simulate a variety of network conditions (topologies, latencies, bandwidth issues) and use that as feed forward information so the network optimize performance, or adapt to pathological conditions.

I’d love to hear your (or anyone’s) thoughts on possiblity adapting the methodology to help with ETH 2.0/Serenity. I have worked with [@mhchia](/u/mhchia) from the foundation on some of the P2P stuff, but would like to get more involved.

---

**MihailoBjelic** (2018-11-04):

Thanks for the explanation, it’s definitely an interesting project! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/jrhea/48/1406_2.png) jrhea:

> Since there is no leader, the scheduler is an emergent property of all the nodes - they all know what to do

I’ve figured this out, that’s great. But how is the work scheduled, i.e. who creates/updates the index?

![](https://ethresear.ch/user_avatar/ethresear.ch/jrhea/48/1406_2.png) jrhea:

> If one node loses connectivity, or stops producing work, then the other nodes notice it and weave the extra work into their queue.

I’ve checked the document again and I guess the redistribution of work in the case of Eth 2.0 should be done instantly, because blocks (collations) form a blockchain and you cannot enter the missing blocks at a latter point in time.

![](https://ethresear.ch/user_avatar/ethresear.ch/jrhea/48/1406_2.png) jrhea:

> All the nodes know when Peer 3 is done bc it broadcasts a small message to the room to inform other peers that Peer 3’s Epoch 2 work is complete and also provides an ipfs content hash so the other peers know where to find it.

The message is fine, but I guess shard nodes should directly send the data (blocks) to their peers (no need for IPFS).

![](https://ethresear.ch/user_avatar/ethresear.ch/jrhea/48/1406_2.png) jrhea:

> Nodes can confirm that they have all synced up correctly by periodically comparing the content hash of their data every N epochs.

I’m speaking off the top of my head, but I guess in Eth 2.0 they only need to make sure that everyone are on the same height. I might easily be wrong, have to think about that…

![](https://ethresear.ch/user_avatar/ethresear.ch/jrhea/48/1406_2.png) jrhea:

> Tunable parameters are nice bc it could allow us simulate a variety of network conditions (topologies, latencies, bandwidth issues) and use that as feed forward information so the network optimize performance, or adapt to pathological conditions.

I completely agree.

![](https://ethresear.ch/user_avatar/ethresear.ch/jrhea/48/1406_2.png) jrhea:

> I’d love to hear your (or anyone’s) thoughts on possiblity adapting the methodology to help with ETH 2.0/Serenity.

I’ve shared a few thoughts above and I think your model really could be a nice starting point for shard nodes coordination. It’s also important to note that I’m still not familiar with every aspect/detail of the Eth 2.0 design. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**jrhea** (2018-11-05):

> Thanks for the explanation, it’s definitely an interesting project!

Thanks man… great to hear that. ![:cowboy_hat_face:](https://ethresear.ch/images/emoji/facebook_messenger/cowboy_hat_face.png?v=12)

> I’ve figured this out, that’s great. But how is the work scheduled, i.e. who creates/updates the index?

Are you asking how new work is added to the queue? If so, work can be added in two ways:

1. By virtue of the problem definition. For example, many number theory problems essentially iterate over the integers.
2. Work can also by added by subscribing to s.c. events.

> I’ve checked the document again and I guess the redistribution of work in the case of Eth 2.0 should be done instantly, because blocks (collations) form a blockchain and you cannot enter the missing blocks at a latter point in time.

In the case of Arithmetica, I had to assume that peers would be unreliable. In the case of Eth 2.0, I think we can probably work under a different assumption without too much of a problem, but that is just my gut reaction.

> The message is fine, but I guess shard nodes should directly send the data (blocks) to their peers (no need for IPFS).

I agree. In fact, the original version sent the data directly to the peers without the ipfs intermediary. Ipfs was essentially added as a hack bc we didn’t have any type of incentivized storage.

> I’ve shared a few thoughts above and I think your model really could be a nice starting point for shard nodes coordination. It’s also important to note that I’m still not familiar with every aspect/detail of the Eth 2.0 design.

Perhaps we could get [@vbuterin](/u/vbuterin) or [@pipermerriam](/u/pipermerriam) to weigh in. Also, I think the spec is only 60% complete so perhaps we could help define this part. I’d be happy to work with you and others on it.

---

**MihailoBjelic** (2018-11-05):

Thanks for the answers. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Of course, I’m more than willing to help in any way I can. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) I’m working on a scalability solution for Ethereum that has a lot in common with Eth 2.0/sharding, so I believe my whole team can and will contribute. We’re even considering starting another Eth 2.0 client/beacon chain implementation (or join one of the existing teams) in parallel with our work, I guess that would be the best way to contribute to the ecosystem (we would also help with research during the process, of course).

