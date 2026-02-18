---
source: ethresearch
topic_id: 13841
title: Byzantine Fault Tolerant Bridges
author: seunlanlege
date: "2022-10-04"
category: Applications
tags: []
url: https://ethresear.ch/t/byzantine-fault-tolerant-bridges/13841
views: 2907
likes: 1
posts_count: 12
---

# Byzantine Fault Tolerant Bridges

This article is a response to [a reddit post](https://www.redditmedia.com/r/ethereum/comments/rwojtk/ama_we_are_the_efs_research_team_pt_7_07_january/hrngyk8/?depth=2&showmore=false&embed=true&showtitle=true&context=1&showmedia=false&theme=dark) made by [@vbuterin](/u/vbuterin) about the lack of byzantine fault tolerance in cross-chain (cross-domain) bridges.

In this article i explore all of the different byzantine states of Proof of stake blockchains and describe a bridging protocol that is resistant to all these states, enabling the first of its kind: *byzantine fault tolerant bridges*.

https://medium.com/@seunlanlege/591e8b2d196e

## Replies

**MicahZoltu** (2022-10-04):

The thing I find most useful when thinking about cross chain bridging is a combination of:

1. Figuring out how to deal with rule changes.  e.g., hard forks
2. Figuring out how to deal with rule changes where the old and the new rules are both popularly supported (e.g., 50:50 community split).

In these scenarios, how do you determine which of the two chains is the correct one to bridge to?  You can’t bridge to both, as that would result in 2x as much money on your external chain, and human consensus is the only way to figure out which of the two copies of the original chain is “correct”.  This is true even if your remote chain has a perfect light client and the forked chain has a concept of finality.

---

**seunlanlege** (2022-10-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Figuring out how to deal with rule changes.  e.g., hard forks

This is a good catch, I’d argue here that the fork that this light client-bridge continues to support is actually determined by the majority of the community members of the counterparty chain.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Figuring out how to deal with rule changes where the old and the new rules are both popularly supported (e.g., 50:50 community split).

Highly unlikely that we’d ever see an even split on hard forks, But if we ever did, one of the chains would have to change it’s `chain_id`, and the one that does will no longer be supported by the bridge.

---

**MicahZoltu** (2022-10-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/seunlanlege/48/9754_2.png) seunlanlege:

> Highly unlikely that we’d ever see an even split on hard forks, But if we ever did, one of the chains would have to change it’s chain_id, and the one that does will no longer be supported by the bridge.

The current process for changing chain ID is very much not credibly neutral.  Just because the chain ID changes doesn’t make that chain less legitimate.  In fact, I would weakly argue that the chain that changes its chain ID is the *more* legitimate chain.  Really, the chain ID should change every time the rules change, even if 100% of users move to the new ruleset.

---

**cangurel0** (2022-10-12):

while I’ve really enjoyed the post, I think there are 2 distinct types of attacks both vaguely referred to as 51% attack, which makes things a bit confusing for me.

> “51% attack on the source chain. This is a byzantine state which arises when the source chain finalizes two competing chains at the same height. This is devastating for light client-based bridges because these two competing chains are valid for our light client verification algorithm and can be used to double-spend incoming assets.”

If I understand correctly, the scenario is as follows; majority consensus wants to double spend some funds. To do so, they equivocate. They sign two *otherwise valid* blocks at the same height. In this case, it wouldn’t matter if I’m running a full or light node. All nodes who observe 2 conflicting finalized blocks would halt. Eventually the network will default to social consensus to determine which fork to follow. If this attack is combined with an eclipse attack, the eclipsed node can be tricked to continue following a malicious chain while everyone else halts. Again, it doesn’t matter if the eclipsed node is light or full.

(In PoS, this event will be slashable if consensus votes are globally known)

Here is the part where I think a different type of attack is described.

> “It’s important to note that light clients are vulnerable to this attack because they do not validate the state transition function of the blocks², where they would’ve detected the invalid transactions and immediately rejected the block. This is of course why they’re called light clients; instead, they rely on full nodes to gossip finalized headers.This vulnerability can be mitigated by having light clients that actively participate in the p2p swarm and can ask as many nodes of the latest finalized header in the chain.”

The attack mentioned refers to a case where consensus votes on a block that breaks validity rules. A typical example is a block that prints unlimited tokens. In this case, it’s true that full nodes will automatically reject the block. It’s however not true that light nodes can be protected against this attack just by connecting peers and asking for the latest header. This is because there would be no way to detect a malicious tx in the block body, just by checking the header.

Thus the described security model doesn’t protect the light client bridge against invalid state transitions.

---

**cangurel0** (2022-10-12):

> These fishermen have a simple task: their job is to watch the headers that get sent to our on-chain light clients and compare them with what is gossiped in the p2p swarm. So in the event of an eclipse attack, a fisherman stands to earn significant rewards by reporting these forged headers back to the source chain and claiming the associated slashing rewards for themselves

a question related to this. Are you referring to the slashing of consensus nodes here? ie. a mechanic defined at consensus level

---

**seunlanlege** (2022-10-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/cangurel0/48/10342_2.png) cangurel0:

> Here is the part where I think a different type of attack is described.
>
>
>
> “It’s important to note that light clients are vulnerable to this attack because they do not validate the state transition function of the blocks², where they would’ve detected the invalid transactions and immediately rejected the block. This is of course why they’re called light clients; instead, they rely on full nodes to gossip finalized headers.This vulnerability can be mitigated by having light clients that actively participate in the p2p swarm and can ask as many nodes of the latest finalized header in the chain.”

To clarify further:

In a 51% attack, byzantine nodes are trying to break global consensus (ie break the canonical chain for everyone in the network)

Whereas an eclipse attack is where byzantine nodes gossip headers of invalid blocks specifically to light clients who they know do not validate blocks.

![](https://ethresear.ch/user_avatar/ethresear.ch/cangurel0/48/10342_2.png) cangurel0:

> It’s however not true that light nodes can be protected against this attack just by connecting peers and asking for the latest header. This is because there would be no way to detect a malicious tx in the block body, just by checking the header.

Light nodes can mitigate eclipse attacks by observing the p2p swarm for forks, they might not have the block body but they’ll know when something’s wrong.

---

**seunlanlege** (2022-10-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/cangurel0/48/10342_2.png) cangurel0:

> a question related to this. Are you referring to the slashing of consensus nodes here? ie. a mechanic defined at consensus level

Yes this will make use of the consensus level slashing protocol

---

**cangurel0** (2022-10-12):

> Light nodes can mitigate eclipse attacks by observing the p2p swarm for forks, they might not have the block body but they’ll know when something’s wrong.

that’s true if consensus finalizes two blocks competing for the same height. both can be relayed to the light node, and upon detecting 2 conflicting headers, light node can halt.

this protection won’t work if consensus produces only 1 invalid block right? light node can’t receive a conflicting header from p2p in that case.

---

**seunlanlege** (2022-10-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/cangurel0/48/10342_2.png) cangurel0:

> this protection won’t work if consensus produces only 1 invalid block right? light node can’t receive a conflicting header from p2p in that case.

You’re correct, this mitigation is based on the assumption that only a subset of the nodes are Byzantine and there are honest nodes present in the p2p swarm

---

**cangurel0** (2022-10-12):

not sure I follow.

if the quorum finalizes an invalid block (assume 2/3 of consensus is malicious) how could honest nodes present in p2p help the light node detect that?

---

**seunlanlege** (2022-10-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/cangurel0/48/10342_2.png) cangurel0:

> if the quorum finalizes an invalid block (assume 2/3 of consensus is malicious) how could honest nodes present in p2p help the light node detect that?

Remember that this is an eclipse attack, So the malicious nodes are playing both sides. They appear as honest to full nodes to preserve their stake, and malicious to light nodes whom they send finalized invalid blocks.

If they start to broadcast the finalized invalid blocks in the p2p swarm they’ll be slashed by the honest nodes.

Should add that this assumes that your blockchain liveness is decoupled from safety, so honest nodes can produce blocks where they slash the malicious validators and rotate them out of the authority set without the network halting so they can resume finalizing (safety)

