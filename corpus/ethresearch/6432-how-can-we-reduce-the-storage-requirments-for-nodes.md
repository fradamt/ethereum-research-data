---
source: ethresearch
topic_id: 6432
title: How can we reduce the storage requirments for nodes?
author: lithp
date: "2019-11-08"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/how-can-we-reduce-the-storage-requirments-for-nodes/6432
views: 2402
likes: 8
posts_count: 4
---

# How can we reduce the storage requirments for nodes?

As it becomes more burdensome to run nodes fewer people will decide to. This has a couple negative effects:

- Security is reduced as more people trust providers such as Infura
- Developing novel eth applications is made harder, as developers are stuck with the interface Infura provides.
- The incentives to write and run a non-conforming client (such as one which threw away historical chain data after it had verified the correct chain) become greater, which would threaten the health of the network.

Ethereum relies on the charity of people who run nodes; by allowing the disk requirements to increase we’re rewarding that charity by asking for ever larger donations!

I’ve listed some options below but I’m sure I’ve missed something, are there more/better ideas?

1. Stateless clients. This is the most thorough solution. It users were responsible for maintaining their own state then using ethereum would become harder (you definitely don’t want to lose that state!), but running a node would become much easier. Nodes only need to sync the chain data.
2. SeF proposes using authenticated fountain codes to reduce node storage requirements. Essentially, after verifying the full chain each node would drop 9/10ths of it (or whatever ratio you like). They do this in such a way that a newly bootstrapping node only needs to talk to ~10 nodes in order to download the full chain. Even halving the storage requirement would be useful! And doing so would mean a node joining the network would need to sync against existing nodes.
3. Chain pruning is much simpler than SeF but I think a little more dangerous, it opens up the possibility that new full-syncing nodes can’t find some parts of the chain.
4. Some kind of incentivization scheme.
5. Storing the state in swarm. It worries me because any system which concentrates responsibility for storing each part of the chain into a small part of a DHT means an attacker only needs to DOS one part of the DHT to prevent new nodes from joining the network.
6. State Rent. This work seems to have been deferred in favor of stateless clients?
7. I think there was a proposal for a zero knowledge proof? A proof that a given block has some total difficulty would allow nodes to join without downloading any chain data with similar security properties to how fast sync works now. I’m skeptical this is possible but it would be great!

## Replies

**Mikerah** (2019-11-08):

Another potential way to reduce storage requirements would be to use another blockchain as a data availability layer such as ETH2.0 Phase 1 shards, LazyLedger, or any other blockchain with very cheap (relatively speaking) storage costs. The main drawback is the increase overhead in doing cross-chain communication. But, I suspect there might still be gains despite this extra overhead.

---

**jm9k** (2019-11-28):

Substantial improvements are needed in this area, and there are some very promising directions listed, but the quickest interim solution you can make is probably a form a chain pruning.

If you offer full node operators an option to prune off a percentage of the full chain, then more may be willing to continue operating them on a charity basis rather than shutting them down.

Bitcoin’s pruning model is to set a chain size limit, then prune old blocks until you are under the limit. A safer approach would be to keep the most recent X blocks, then randomly prune old blocks until under the limit. This would give a more even distribution of available blocks similar to SeF, but much less sophisticated.

In the long term, incentivization schemes really need to be developed. IMO, the requirement of altruistic individuals to host the chain has always been a hole in the protocols.

---

**pinkiebell** (2019-12-19):

It doesn’t help the past, but I just proposed [1](https://ethereum-magicians.org/t/rfc-eip-2442-logqueryn-opcodes/3867) and that is one of many small things that can help in the future.

