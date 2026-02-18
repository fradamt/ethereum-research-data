---
source: ethresearch
topic_id: 8592
title: Complete revamp of the "Stateless Ethereum" roadmap
author: pipermerriam
date: "2021-01-28"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/complete-revamp-of-the-stateless-ethereum-roadmap/8592
views: 5559
likes: 10
posts_count: 7
---

# Complete revamp of the "Stateless Ethereum" roadmap

The “goal” of “Stateless Ethereum” is to modify the protocol such that we can have stateless clients which do not store the *state* and instead, use witnesses to execute and verify new blocks.

The current “Stateless Ethereum” roadmap can be loosely summarized as:

1. Use binary trie and code merklization to reduce witness sizes.
2. Modify the core protocol such that block witnesses are created and gossiped
3. Stateless clients use block witnesses for stateless block execution.

I am going to make a case that this roadmap is fundamentally flawed and that we’re unlikely to deliver on our goal of having clients that do stateless block execution.

### Useless stateless clients

If we accomplished the above, a client could be built that executes blocks in a stateless manner.  The problem is, that client would be capable of doing very little else.

- Without the state it would not be able to participate in transaction gossip since transaction validation depends on having access to the state to check nonces and account balances.
- Without the state it would not be able to serve some of the most important JSON-RPC endpoints (eth_call, eth_getBalance, eth_estimateGas)
- Without the state the client couldn’t be part of the DevP2P eth network as it would not be able to serve GetNodeData requests.

Our roadmap gets us the ability to do stateless block execution, but none of the clients are going to build out that functionality because the client would be useless.

### Training the monkey instead of building the pedestal

> Tackle the monkey first. Don’t use up all your resources on the… | by Astro Teller | X, the moonshot factory

It is my assertion that we’re not working on the right problems.  We know that we can reduce witnesses to a manageable size.  Producing block level witnesses and gossiping them isn’t a fully solved problem but we have ideas for how to go about solving it and the problem space is well understood.  These are not the hard problems.

The hard problems are:

- Stateless clients need to be able to expose and serve the JSON-RPC API.
- Stateless clients need to be able to participate in transaction gossip even when they don’t have any of the state.

### Stateless clients and Full nodes are going to be fundamentally different

The other major change in thinking I think we need to make is that we should not expect existing clients to be the first ones to adopt stateless block execution.  The architecture of a stateless client is going to be fundamentally different from existing full node architecture.  Because they won’t have the state they will be required to use these different mechanisms for serving JSON-RPC requests and doing transaction gossip (and likely other things as well).  Current client development teams already are taxed to their limits simply building and maintaining their clients.

It is my assertion that we should expect the first stateless clients to be greenfield projects that operate only in the stateless paradigm.  Thus, we should not expect the majority of the work to be done by existing client development teams, but rather by newly formed teams who are specifically focused on delivering this new type of client.

### What about witness sizes…

This isn’t to say that we shouldn’t do the binary trie conversion or code merklization.  We still need to do these.  They are going to be necessary.  Luckily they are already underway.  We need to continue to support the people working on these efforts, but the research part should be largely done, and the implementation part is going to rest primarily on the existing mainnet client teams.

### What about witness production…

Without consumers of witnesses, witness production is a useless activity.  Without stateless clients, we are going to have no consumers of witnesses.  Focusing on witness production before we have a reasonable handle on the clients that will consume them is doing things in the wrong order.  We need to focus on the clients

### How can a stateless client do stateless block execution if they don’t have witnesses

They can’t, but this doesn’t actually matter.  If we build the functionality for stateless clients to gossip transactions, serve JSON-RPC, etc, then they don’t actually **need** to execute blocks in order to be useful.  Once we have a solid handle on filling out all of the other functionality needed to make stateless clients useful, we’ve built everything needed to create really nice ultra light clients.

Stateless block execution is simply an extra layer of verification and security that can be enabled/added once witnesses are being produced and made available.

### How does chain history come into play

It technically is orthogonal, but we should do it anyways.  It will be useful to all types of clients and there’s little reason not to build it if we have the resources to do so.

### Additional reading and information

A three part blog post I wrote on how we solve these additional problems.

- The winding road to functional light clients - part 1
- The winding road to functional light clients - part 2
- The winding road to functional light clients - part 3

A talk that I gave on the same subject: https://www.youtube.com/watch?v=MZxqRs_tLNs

## Summary

- We keep going with the binary trie conversion and code merklization
- We need new networks to serve on demand state and on demand chain history
- We need new gossip mechanics to allow stateless transaction gossip.
- We need new client teams that are dedicated to build stateless clients since we should not expect current client teams to do this.

This will require multiple independent teams working concurrently on these problems.  I’m already working to secure funding.  It’s very likely that ESP may play a roll in this as well providing grants.

## Questions and Critical Feedback

What questions do you have.

Do you see something you think I got wrong, or something I missed?

## Replies

**dankrad** (2021-01-28):

I think this post misses a bit the “why” of stateless Ethereum. Stateless exists because we can get cheap consensus nodes. I can instantly spin up a node on my laptop, even if it doesn’t have a fancy SSD. An Eth2 validator after the merge, potentially running on a lowly Raspberry Pi, can hop on the Eth1 shard, validate one block, and forget about it for 100 blocks, and then validate another block. This is why statelessness matters.

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> Without the state it would not be able to participate in transaction gossip since transaction validation depends on having access to the state to check nonces and account balances.

Wouldn’t any stateless proposal include adding witnesses to gossiped transactions? Stateless clients should absolutely be able to participate in gossiping.

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> Stateless clients need to be able to expose and serve the JSON-RPC API.

It is obvious that a stateless node can’t answer questions about the state. That was never the goal. A stateless node exists to maintain consensus, and nodes that answer questions about the state will still exist in order to, for example, save JSON-RPC data.

---

**pipermerriam** (2021-01-28):

Yes, transaction gossip can be solved with witnesses.  There’s complexity to be figured out for how witnesses get updated.

Yes, a stateless client without JSON-RPC is useful to maintain consensus.

Here are my reasons whyI believe the expanded roadmap is still the right way forward (and why the current minimal roadmap isn’t likely to succeed)

### 1. The ETH DevP2P network isn’t well suited for stateless clients

A stateless node will not be able to be part of the `ETH` DevP2P network.  The network places the implicit requirement that all nodes hold all history and all state.  Without this data, the node won’t be able to respond to most requests from peers and will be dropped as a useless peer.

Modifications would need to be made to the `ETH` DevP2P protocol such that:

- Nodes don’t have to hold the chain history
- Nodes don’t have to hold the state
- Nodes can participate in transaction gossip without having the state.

I don’t think current mainnet client developers are going to put forth the effort to tackle these problems.  They have other priorities and the work to make these changes isn’t simple.

### 2. Better clients should be part of our goal

Current clients are heavy and hard to run.  It is my opinion that we should be investing effort into addressing this.  It makes natural sense to combine efforts and both build out the infrastructure we need for stateless clients which **also** gives us the infrastructure needed to make extremely lightweight clients.

### 3. Consensus only stateless clients are not compelling

If we just try to stick to the current roadmap and build consensus only clients I don’t think we are likely to succeed.  We need significant ongoing buy in from client developers and I don’t think that will happen.  They have other priorities.  The stateless clients we can build with the current roadmap can do very little, and are only useful in the eth2 context.

I’m not saying that this path cannot be done.  I’m simply saying that it is a lot of work towards a goal that isn’t interesting outside of the eth2 context and it requires buy in from a group that has other priorities.  I’m not interested in leading that effort.  I don’t think it will succeed and it has external dependencies that are outside of my control which can cause it to fail simply by inaction.

---

**dankrad** (2021-01-28):

I think the points about prioritization are very fair. As far as I understand, what your suggestion ultimately comes down to is this:

> We need new client teams that are dedicated to build stateless clients since we should not expect current client teams to do this.

I’m very skeptical about this. The idea of statelessness should be that ultimately, *most* people don’t need to keep the state. That’s how we could potentially increase the gas limit (because DOS attacks due to state growth cease to be a problem and Eth2 validators will not have to follow all blocks, reducing their bandwidth) and allow several execution shards on Eth2 (because validators don’t have to follow all execution shards, which would be the case if they’re stateful).

So unless the clients reduce their target customers and only want to be useful to state serving/block proposing, they will have to provide a stateless mode.

---

**pipermerriam** (2021-01-28):

I completely agree with you that current clients should move this direction.  I think they will, eventually…

I haven’t seen anything that convinces me that they’ll prioritize it anytime soon.  I want to do this **now** and I see a way to do it.  I don’t see existing client developers putting the significant resources towards this.  They have other pressing matters that take up all of their capacity.

My expectation is that once it’s built, and there are lightweight clients and stateless clients that expose the same external functionality, market forces naturally pull existing clients in the same direction.  Some will remain heavy, focused instead on serving use cases that need the full state.  Some will lighten themselves, by adopting the new protocols that allow them to drop ancient history, cold state, or all of the state.

---

**pipermerriam** (2021-01-28):

A perfect way to prove me wrong would be for some representative sample of the mainnet client developers to drop in and express their plans to commit to focusing on this issue.  I have made assertions about what I expect them to prioritize (or not prioritize) but I don’t and can’t speak for them.

---

**pipermerriam** (2021-02-03):

I’ve updated my document here to reflect my latest thoughts: https://notes.ethereum.org/mSOAdx_XT02MEqrt0f2CPA

