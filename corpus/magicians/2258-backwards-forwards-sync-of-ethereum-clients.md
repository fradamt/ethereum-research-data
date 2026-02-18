---
source: magicians
topic_id: 2258
title: Backwards-Forwards sync of Ethereum clients
author: AlexeyAkhunov
date: "2018-12-20"
category: Working Groups > Ethereum 1.x Ring
tags: []
url: https://ethereum-magicians.org/t/backwards-forwards-sync-of-ethereum-clients/2258
views: 2584
likes: 3
posts_count: 1
---

# Backwards-Forwards sync of Ethereum clients

This is another rough brain-dump of the idea I have sort of presented in the AllCoreDev gitter channel, but did not structure it yet.

A few things led to this idea: discussion of [EIP-161](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-161.md), and specifically, the Addendum, which described an exceptional handling of some special case. That special case arouse out of a consensus bug after Spurious Dragon hard-fork, and raised a question on how do we stop EVM rule set from growing more and more complicated, and clients needing to support all historical rules and special cases. For example, if we drop storage clearing refunds after introduction of State Rent, why should all the Ethereum clients (old and new) still code up all the refund rules?

Meanwhile, [Trinity team was thinking about implementing Parity’s warp sync](https://github.com/ethereum/py-evm/issues/1593), and analysing trade-offs between trust and performance. I suggested a hybrid sync model (which I definitely plan to implement in Turbo-Geth), very roughly described [here](https://github.com/ledgerwatch/eth_state/blob/master/sync/Hybrid_Sync.pdf).

And, thirdly, if anyone has [seen](https://slideslive.com/38911907/turbogeth-optimising-ethereum-clients) or [read](https://github.com/AlexeyAkhunov/papers/blob/master/TurboGeth-Devcon4.pdf) my Devcon4 presentation, you can notice on slides 8 and 9 I am talking about reverse diffs for the sake of better prune-ability. Now I think the reverse diffs have another application - backwards syncing.

Imagine that you synced the snapshot of current state using Hybrid sync (or fast-sync, or warp-sync). Now, if you want to reconstruct entire or part of the history, you would need to start from some earlier snapshot, or from genesis. Then, you would download the blocks of transactions starting from that earlier point, and apply transactions, advancing the state. Each time you advance the state to the next block, you verify state root against the one contained in the block header. For that, **your client needs to support all historical EVM rules** that were in force during the time from that earlier point.

Now imagine that instead, you are requesting reverse diffs (deltas), that would describe state changes taking the state of your current latest snapshot to 1 block before that. Once you received them, you compute the state 1 block before, and compare the root with the one in the block header. If it matches, you record those diffs in the database. Turbo-Geth can do it already (I call it state rewinding), but other clients can implement it too. And that goes on until you reconstructed the desired range of history of state. Crucially, this process **does not require the knowledge of any EVM rules**! Therefore, the client is free not to implement any historical rules just for the process of syncing.

Why it is called Backwards-Forwards sync? After you have received the current snapshot, and potentially launched Backwards sync of history, you also start Forwards sync, as clients usually do, catching up with, and then following the tip of the chain. This **only requires the knowledge of the current EVM rules**, and, for some time after a hard-fork, the knowledge of rules prior to the latest hard-fork.

Few days ago, we tried to transmit Turbo-Geth’s current pre-synced database (311Gb) over BitTorrent, for the sake of opening up data analysis, for some eWASM research, and then, perhaps, for State Rent. It kind of works, but it requires having this snapshot extracted and seeded for days, while the tip of the chain goes ahead. So such solution to data dissemination is not sustainable, in my opinion. But backwards-forwards sync could work - and it can be implemented in Turbo-Geth without any re-architecture. Therefore, I will make one of the priorities for Turbo-Geth development

**EDIT**: Addition - while clients implementing Backwards-Forwards sync would not need to have all historical EVM rules in the consensus critical code, they can still provide a utility program that can go through historical state database and re-trace (re-execute) any transactions. Here you would need to know all historical rules, but this code is not consensus critical!
