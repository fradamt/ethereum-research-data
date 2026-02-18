---
source: magicians
topic_id: 24346
title: Relaxing the prover hardware requirements for the next few years
author: dankrad
date: "2025-05-26"
category: Magicians
tags: []
url: https://ethereum-magicians.org/t/relaxing-the-prover-hardware-requirements-for-the-next-few-years/24346
views: 1493
likes: 41
posts_count: 13
---

# Relaxing the prover hardware requirements for the next few years

# Real-time proving has arrived

Last week, Succinct announced that they had achieved real time proving:

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/5/5d29b1952c7a99a8ecf65ddda7e96759fed62229_2_350x500.png)image732×1045 329 KB](https://ethereum-magicians.org/uploads/default/5d29b1952c7a99a8ecf65ddda7e96759fed62229)

We should see this as an amazing success, and as the time the big bet Ethereum made on ZK is paying off.

Can we scale the L1 as much as we want now? Is anything possible? For good reasons, we started discussing the limits: [Formalizing decentralization goals in the context of larger L1 gaslimits and 2020s-era tech](https://ethereum-magicians.org/t/formalizing-decentralization-goals-in-the-context-of-larger-l1-gaslimits-and-2020s-era-tech/23942) – in short: Even in a world where most nodes can relax and only verify data availability and execution proofs, we want to make sure that the production of these don’t become singular choke points for the network and so we must keep some limits on how powerful we allow them to be. A good guideline is that if some people are still able to run them from home, it becomes hard to maintain a global ban.

There is one type of node that can’t really be distributed: A stateful node that remains able to follow the state and compute updated state roots (for example RPC, but also as part of the proving pipeline).

Proving is a bit more interesting, because in principle it is highly parallelizable not just across a single machine but across globally distributed networks, even with limited bandwidth; think of just splitting a block into many miniblocks to prove them. However, there are calls to apply our limits directly to provers:

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/6/6e766c05d35c9bd3db2dc580d43dd5aacbd0e01d_2_690x373.png)image738×400 109 KB](https://ethereum-magicians.org/uploads/default/6e766c05d35c9bd3db2dc580d43dd5aacbd0e01d)

I think while these are good goals for the Ethereum network to have, we should “suspend” the strict decentralization limits for proving for the next few years. Provers have improved by many orders of magnitude over the last few years, with proving overhead improving from the trillions to just around a million today. We can expect several more orders of magnitude over the next few years (with [@vbuterin](/u/vbuterin) believing it will ultimately be only a single digit overhead – almost a one million times improvement from today to go). This may take some years to materialize (and might ultimately depend on new types of hardware specialized in proving), but I suggest we should not repeat the mistake from the last few years: Let’s “suspend” the rules and be less strict about L1 provers for five years.

## Why it’s ok to be more relaxed about proving

There are several good reasons why proving can be more relaxed than other parts of the stack:

### 1. Unlike other parts of the stack, scaling back does solve proving

One of the reasons we were always extremely careful about scaling the L1 was that there was “no going back” – yes you can lower the gas limit again, but the large state size and its downsides remain. However, there is no such “ratchet effect” for proving. If we scale to 3 gigagas, and a global regulatory attack on provers happens, we can go back to today’s gas limit, and even though the state has grown, this does not really affect proving (except for slightly larger state witnesses, but logarithmic growth is manageable in practice). The provers are not a very effective choke point.

In fact, we could design our consensus so that it locks in transactions before proving – the only thing the attack could do would be slowing down, a graceful degradation.

### 2. Proving can be ultra-parallelized

Should the vision of “single-digit overhead proving” not materialize, there are still other ways to make sure that we won’t have prover chokepoints. At the cost of stlightly increased latency, we can distribute proving across tens, hundreds or even thousands of machines. While it would not be a strict “one out of n” honesty assumption on these, it would still be an honest minority assumption.

## Let’s not repeat our previous mistakes

Proving at scale is a huge win for Ethereum. It’s an industry that was bootstrapped both by many community investments and the rollup-centric roadmap. Not using these powers now that we have them would be our biggest mistake yet.

While we would probably be in a better place if we had decided on a moderate scaling L1 roadmap of ca. 10x in 2021, we understandably did not go for it: At the time, 10x did not seems to be enough of a factor to matter, and it wasn’t clear how to continue from there. Yet, we are paying dearly for this, as Ethereum would have probably stayed much more competitive over the last few years had it continued to make strong investments in L1 engineering.

We should not repeat this mistake now by choking scaling again due to concerns about prover decentralization. Prover centralization, for all the points mentioned above, is different: (1) It probably won’t last, (2) it’s not permanent (we can scale back), and (3) if push comes to shove we can slightly increase latency and distribute them.

## Replies

**ihagopian** (2025-05-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dankrad/48/2962_2.png) dankrad:

> If we scale to 3 gigagas, and a global regulatory attack on provers happens, we can go back to today’s gas limit, and even though the state has grown, this does not really affect proving (except for slightly larger state witnesses, but logarithmic growth is manageable in practice). The provers are not a very effective choke point.

Regarding this, I’m thinking of two consequences:

1. The base fee will probably skyrocket, which would have a big impact on existing applications—potentially making many of them not viable anymore and affecting many users. I think it is worth considering this impact for the proposed fallback strategy.
2. If the network has a 3 gigagas throughput, the state size would have grown massively. To prove, you still need to run a full node (i.e. full state) and be able to access it fast enough to generate the witness for proving.

Regarding the latter, maybe you’re thinking that the computational resources are the dominant factor compared to running a distributed system that can store and access the full state fast enough? (Clarif: I’m assuming the ban also cover builders)

---

**dankrad** (2025-05-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ihagopian/48/8788_2.png) ihagopian:

> The base fee will probably skyrocket, which would have a big impact on existing applications—potentially making many of them not viable anymore and affecting many users. I think it is worth considering this impact for the proposed fallback strategy.

Yes, in the case of such an attack, usage of Ethereum L1 would have to be reduced massively and be more restricted to the high value use cases that actually require the high level of censorship resistance it provides.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ihagopian/48/8788_2.png) ihagopian:

> If the network has a 3 gigagas throughput, the state size would have grown massively. To prove, you still need to run a full node (i.e. full state) and be able to access it fast enough to generate the witness for proving.

This is why I would still apply the stricter limits to stateful nodes (probably even much lower than the suggested $100k/10 kW limits and more around “beefy home computer with some extra SSDs”). Realistically this is still very possible and the main limit here is going to be bandwidth.

---

**RostyslavBortman** (2025-05-27):

If we go down this path, the permanent growth of state for full nodes could become so massive that we risk replicating Solana’s current problem - where only centralized RPC providers can realistically operate. This undermines the very decentralization Ethereum is trying to preserve. Relaxing prover decentralization may be fine short-term, but relaxing node requirements risks long-term centralization.

> a market structure dominated by a few RPC providers is one that will face strong pressure to deplatform or censor users

In saying that, I do want us to find a way to use Ethereum real time proving which was achieved recently as soon as possible.

---

**soispoke** (2025-05-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dankrad/48/2962_2.png) dankrad:

> Yes, in the case of such an attack, usage of Ethereum L1 would have to be reduced massively and be more restricted to the high value use cases that actually require the high level of censorship resistance it provides.

I don’t think it’s acceptable to have a threat that could render a large portion of users (including businesses and institutions built on Ethereum) unable to use the chain because they’re priced out in the event of a regulatory attack on provers. What would the priced out users do then? (h/t [@ihagopian](/u/ihagopian))

That would mean a network where censorship resistance is only guaranteed for the wealthiest N% of users so it doesn’t really work.

---

**dankrad** (2025-05-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/soispoke/48/13615_2.png) soispoke:

> I don’t think it’s acceptable to have a threat that could render a large portion of users (including businesses and institutions built on Ethereum) unable to use the chain because they’re priced out in the event of a regulatory attack on provers. What would the priced out users do then? (h/t @ihagopian)

You are arguing that since there is a risk that they might be priced out, we should never offer it at all. That seems crazy to me.

In the case where this attack happens, the user previously on L1 will have to move to L2s. This has some downsides:

- The users lose atomic composability with L1, which is presumably the main reason they were there
- Ethereum loses the network effects of having central liquidity

However, if the provers fail, they get the same benefits they would get now without scaling the L1.

---

**gballet** (2025-05-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ihagopian/48/8788_2.png) ihagopian:

> To prove, you still need to run a full node (i.e. full state) and be able to access it fast enough to generate the witness for proving.

not only that, but we also have to assume that the number of actors with the whole state will have greatly decreased by then, since most users would simply run a stateless validator.

---

**soispoke** (2025-05-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dankrad/48/2962_2.png) dankrad:

> You are arguing that since there is a risk that they might be priced out, we should never offer it at all. That seems crazy to me.

Ah no that’s not what I was arguing. I think we should offer it, I was just arguing for defining a reasonable prover budget so we minimize the chances of a regulatory ban shutting down *all* provers. This way we minimize the chances of users ever getting priced out in the first place.

I also don’t have super restrictive limits in mind, but if we can temporarily reduce chances of catastrophic events by defining some requirements that would still allow us to get a ton more scaling compared to today, I think there is value in doing that.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/netdev/48/14375_2.png) netdev:

> A large portion of users have already been priced out of Ethereum L1 for many years

Right, but (1) I don’t remember people being very happy about it, and (2) it’s one thing to be priced out, it’s another to suddenly have to shut down services provided on L1 due to a sudden change in regulation.

---

**netdev** (2025-05-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/soispoke/48/13615_2.png) soispoke:

> I don’t think it’s acceptable to have a threat that could render a large portion of users (including businesses and institutions built on Ethereum) unable to use the chain because they’re priced out in the event of a regulatory attack on provers. What would the priced out users do then? (h/t @ihagopian)

A large portion of users have already been priced out of Ethereum L1 for many years

---

**lex-node** (2025-05-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dankrad/48/2962_2.png) dankrad:

> a global regulatory attack on provers

this is the first time that I, a lawyer, am hearing of fears of regulatory attacks on provers…any particular reason for this fear or links to related discussions I can take a look at? I don’t normally think of proving as a high regulatory-risk activity. . .

---

**dankrad** (2025-05-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lex-node/48/14286_2.png) lex-node:

> this is the first time that I, a lawyer, am hearing of fears of regulatory attacks on provers…any particular reason for this fear or links to related discussions I can take a look at? I don’t normally think of proving as a high regulatory-risk activity. . .

This is less about law as it is and more about “what potentially could be”. The idea is that if there is any single chokepoint (e.g. 1 or a handful of provers worldwide) then this would be the easiest way to attack Ethereum, by preventing the prover from proving blocks that include some transactions. One way would be through regulations.

---

**lex-node** (2025-05-27):

makes sense, thanks ser

---

**tim-clancy.eth** (2025-05-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dankrad/48/2962_2.png) dankrad:

> For good reasons, we started discussing the limits: Formalizing decentralization goals in the context of larger L1 gaslimits and 2020s-era tech (https://ethereum-magicians.org/t/formalizing-decentralization-goals-in-the-context-of-larger-l1-gaslimits-and-2020s-era-tech/23942)

I am glad that we are already thinking of what limits are reasonable and formally defining them; being rigorous about requirements for solo stakers (`https://hackmd.io/DsDcxDAVShSSLLwHWdfynQ?view`) (local and non-local block building) is long overdue.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dankrad/48/2962_2.png) dankrad:

> I think while these are good goals for the Ethereum network to have, we should “suspend” the strict decentralization limits for proving for the next few years.

Which of [@vbuterin](/u/vbuterin)’s suggested requirements are you proposing suspending?

1. We still need to demonstrate real-time proving of the worst-case block anyways. If it’s much worse than the average case this seems like a good motivation to do some repricing.
2. We also need to formally verify anyways.
3. This seems to be the only limit to consider.
4. Whatever the gas limit ends up being will also heavily impact the limit.

I’ll add a requirement of my own. It goes without saying that the prover must be fully Free Software (`https://www.gnu.org/philosophy/free-sw.en.html#fs-definition`) as well; i.e. the SP1 CUDA prover is currently distributed as an unlicensed binary. It would not be tolerable for Ethereum to rely at its core upon something closed source.

So it all boils down to the kW. This specific mostly-realtime demo was 160x4090s for that under ~100kW figure. Even though we only need a single honest, parallelizable prover I don’t want to go nuts with this. I don’t have enough faith that if we start at 1MW we won’t decide to 10x throughput instead of making proving 10x cheaper the next time proving undergoes a 10x in performance.

