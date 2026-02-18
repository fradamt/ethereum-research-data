---
source: ethresearch
topic_id: 8121
title: "Increasing ETH’s Gas Limit: What we can safely do today"
author: eleni
date: "2020-10-16"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/increasing-eth-s-gas-limit-what-we-can-safely-do-today/8121
views: 5294
likes: 6
posts_count: 8
---

# Increasing ETH’s Gas Limit: What we can safely do today

By Professor Aleksander Kuzmanovic & Eleni Steinman @ bloXroute Labs

*At bloXroute we have spoken to many in the community about safely increasing the gas limit and have created this post to encapsulate those conversations and continue the discourse.*

Note: We were limited in the number of included hyperlinks and used additional spaces to trick the system.

**How do we know the gas limit can be increased safely?**

In July, the total gas used on the Ethereum blockchain reached a new all-time high after Ethereum miners voted to increase the block gas limit by 25% (from 10,000,000 to 12,500,000). While our data implies that the recent gas limit increase is modest, and that a much higher gas limit can be deployed, we argue that (1) incremental gas limit upgrades are necessary to allow sufficient time to assess the effects of modest upgrades and (2) yet in absence of negative side effects, such modest gas increases can be conducted more frequently.

Through our close work with many of the mining pools, we can further see that the network is healthy and can handle a higher volume of TPS then we are currently seeing as bloXroute operates at the networking layer. There was no statistically significant increase in the uncle rate after the gas limit was increased by 25%. This is also true after the 25% increase in September 2019 (which occurred in conjunction with bloXroute going live).

[![](https://ethresear.ch/uploads/default/optimized/2X/5/5d1a4222f9313a2418ad8893b240a4c6f31331c8_2_624x180.png)1050×303 98.3 KB](https://ethresear.ch/uploads/default/5d1a4222f9313a2418ad8893b240a4c6f31331c8)

Data from [Etherscan.io](http://Etherscan.io)

When two different miners mine two different blocks at roughly the same time, these competing blocks cause a fork in the blockchain. Once a new block is mined on top of one of them, those blocks become the longer chain and the other block is discarded and will only be referenced as an “uncle”. When forks occur, we measure the delta between the two blocks. We break those forks into 50 ms segments, which indicates how long it takes for miners to hear of a new block.

Image: //imgur .com/a/G1z8mnd

We can see that almost 20% of miners move to mine the next block within 100 ms (0.1 sec) after a new block is mined, and it takes about 0.6 sec for half of the miners to start mining the next block. Lastly, almost all (90%) of the hashpower is already working on the next block within 1.5 sec.

This should quiet the fears of those concerned that increasing the gas limit will break Ethereum as we’re not seeing a significant difference in uncle rates and propagation times before and after the gas limit increase when such networking optimizations are implemented. The key is to minimize such risk that increasing the gas limit will break Ethereum by taking incremental steps, like we have seen this past year, to increase the gas limit.

**How bloXroute optimizing the network?**

Blockchains today are at a similar place where the Web was 20 years ago — in its infancy and with the scalability problem unsolved. In a similar way Akamai solved the problem for the Web, by propagating data more quickly across the Internet, so does bloXroute today, by providing a technology breakthrough to propagate data throughout the blockchain P2P network.

In particular, bloXroute deploys a blockchain distribution network (BDN) that helps all blockchain nodes propagate transactions and blocks quicker and more efficiently. Both Akamai’s and our architectures actively push (propagate) content across the Internet, and cache (store) content on its servers in order to serve users better, i.e., with a larger throughput and a smaller latency.

It is such network optimization that allows for a higher gas limit and we expect to see further improvements in the future, both from bloXroute and other actors.

**Arguments against increasing the gas limit**

Some in the community have proposed concerns about increasing the block gas limit at all. Below we address such concerns.

1. Larger blocks increase the time to sync a new node

The time to sync a new node will keep increasing even without any changes to the block size. Hence, this problem needs to be addressed independently. bloXroute’s BDN provides a viable solution: instead of downloading data via a potentially low-bandwidth distant peer in a p2p network, a new node can download data from a nearby BDN at a high rate. While a node can be bottlenecked either by network or by processing transactions, bloXroute’s experience (corroborated by our clients and partners) is that a bloXroute-supported node syncs much faster than a “regular” node. Hence, the networking bottleneck is more dominant in practice. There are no centralization concerns with this approach, because a user can always independently verify that the content downloaded from the BDN is valid.

1. Increased block computation time will prevent older, slower nodes from staying in sync and will increase sync time for new nodes

Another concern being voiced is that increasing the gas limit won’t allow full nodes to process new blocks fast enough to keep up with the rate of new blocks arriving, and they will be effectively thrown off the network.

However, a full node running on a commodity PC can usually process a block within 0.5–1 second. Since new blocks arrive every 13 seconds, on average, we have a 10–25x multiplier before this becomes an issue at the current hardware. Given that hardware also improves over time (as an example, Samsung’s SSD EVO improved by 5x since 2017). I don’t see this ever becoming an issue, but it is definitely not an issue now.

1. Increased gas limit will increase DOS vulnerability (See Broken Metre: Attacking Resource Metering in EVM @ https:// arxiv .org /pdf /1909.07220.pdf)

The key source behind the above DoS attacks is an inconsistency in the pricing of some instructions, which lead to DoS attacks in the form of low-throughput contracts. As such, this issue is orthogonal to the gas limit, and the solution lies elsewhere, i.e., in appropriately adjusting the gas cost for given instructions. Short- and long-term solutions to this problem are outlined in Broken Metre report.

Additionally, Vitalik recently created a new EIP to mitigate DoS attacks in EIP 2929 of which “a secondary benefit of this EIP is that it also performs most of the work needed to make stateless witness sizes (https:// ethereum-magicians .org/t/protocol-changes-to-bound-witness-size/3885) in Ethereum acceptable” (https:// eips.ethereum .org/EIPS/eip-2929). In discussions with Vitalik over the past 2 years ( lastly at Stanford’s SBC2020), he had been consistent to argue that gradually increasing the gas limit is viable and that stateless clients are more than practical at this point.

1. Increased gas limit may increase chain and state size growth

A concern for all layer 1 chains is how quickly the size of the blockchain is growing (chain growth), or the chain state (the number of active accounts and all their data.), called the State Size Growth. Before a full node can join the Ethereum network, it must sync the entire history of the blockchain; the longer that history is, the more data there is to store, the more time it takes to sync and the higher the cost to store the data. There may arise other implications from state size growth such as memory utilization or client performance, but these issues should be addressed as they reveal themselves.

Many argue that increasing the gas limit would affect the chain-size growth — larger blocks mean the amount of data that needs to be stored grows faster and the problem is exacerbated.

However data shows that increasing the gas limit does not translate to higher chain growth. On September 1, 2019, the Ethereum miners increased the gas limit significantly — by 25% — from 8M gas to 10M. You would expect to see a jump in the rate of state size growth — but we don’t. (Source: https: //blockchair .com/)

How can that be? Because more gas doesn’t necessarily mean more data is stored on-chain. Gas can be used to transfer wealth, computations, loading of data, etc. Storing data is just one of the things gas is used for. If that extra gas is used by DeFi smart contracts which use a lot of gas to compute trading pairs prices, for example, it won’t affect the state size growth.

Similarly, it has been demonstrated (see https: //medium .com/@akhounov/is-ethereum-state-growing-faster-now-and-ethereum-state-analytics-project-97777ab47af) that the state growth does not always correlate with the gas limit.

1. Increased reliance on bloXroute is a move towards centralization

bloXroute’s BDN does not replace the Ethereum p2p network, but rather improves it. The p2p communication is still necessary because in certain scenarios it still can provide a faster path, and in all scenarios it can be used to verify the correctness of bloXroute’s BDN. Another related question is whether everyone needs to connect directly to bloXroute in order for it to provide benefits. The answer is no. bloXroute is already connected to many miners and clients. Hence, even those who are not directly connected to bloXroute’s BDN, are pretty close to it, because their immediate peers are very likely directly connected to bloXroute. Lastly, by design, bloXroute introduces open-source backup-nodes, idle nodes which can be operated by any interested party or stake holder wishing to ensure fast block propagation, e.g., miners, validators, and pools. If bloXroute maliciously rejects a transaction, said transactions would be broadcasted to all the gateways by the backup network. Furthermore, if bloXroute were to provide inconsistent updates or suffer from a system-wide failure, it would be replaced by backup-nodes for any amount of time necessary to find a remedy or a replacement.

1. Blocks could become much larger than they are now (perhaps 10x) even if the gas limit does not change, if rollups start generating much more calldata. These larger blocks might increase propagation time and uncle rate. Increasing the gas limit on top of this could make the problem worse.

If blocks could become much larger than they are now (perhaps 10x) even if the gas limit does not change, due to rollups, then increasing the gas limit is not the key source of the “large block” problem. Rollups are an order-of-magnitude bigger problem. Yet this means that we have to find a solution to handling blocks that are 10x larger than they are now. bloXroute is such a solution, today. Only network cashing, deployed by bloXroute, reduces the effective block size by at least 50x.

## Replies

**technocrypto** (2020-10-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/eleni/48/5643_2.png) eleni:

> However, a full node running on a commodity PC can usually process a block within 0.5–1 second. Since new blocks arrive every 13 seconds, on average, we have a 10–25x multiplier before this becomes an issue at the current hardware. Given that hardware also improves over time (as an example, Samsung’s SSD EVO improved by 5x since 2017). I don’t see this ever becoming an issue, but it is definitely not an issue now.

This is a deep misunderstanding of when “the issue” arises.  That same multiplier tells you how much faster than realtime a block can sync *even if using a BDN*.  It has very intentionally been targetted to this range, and use of a BDN cannot make lower multipliers acceptable.  Projects like Turbogeth which change the multiplier independently of the gas limit are the only way to make higher gas limits practical to sync on commodity hardware in reasonable time periods, and even they have clear technical limits.

---

**eleni** (2020-10-19):

Hi! I think there is a misunderstanding here. The 10-25x multiplier before syncing becomes an issue is a problem irrespective of the BDN - we don’t effect the multiplier at all (either lower or higher).

---

**technocrypto** (2020-10-19):

That was exactly the point I was making.  Since this multiplier is the limit on scaling, adding a BDN to Ethereum doesn’t help with scaling.  It may slightly improve sync times, if they are in fact peer bandwidth limited.  But it doesn’t let us raise gas limits.

---

**uri-bloXroute** (2020-10-20):

First - I have nothing but appreciation for he Turbo Geth team (and specifically to Alexey  who adds a lot of value to the ACD calls). The performance improvements are much needed, and I expect for more and more actors to rely on Turbo Geth more heavily.

That said, the gas limit was not set for these validate/sync multiplier back in Dec 2017.

At the time, the gas limit was increased to 8M and the multiplier was more like ~x5 on a $500 PC (and I think Turbo Geth was still in beta).

A lot had changed in these 3 years, both because of the excellent dev work, and because the definition of a commodity PC had changed: you can get a much stronger PC for $500 today, improving the multiplier substantially.

To an extent, the reason we point out the networking bottleneck is because the SW is now good enough not to be the bottleneck. There’s plenty to improve, but we emphasize it is now safe to increase the capacity substantially, without reaching neither the SW, HW nor networking bottlenecks.

---

**technocrypto** (2020-10-20):

It’s definitely true that the ratio on a $500 USD pc wasn’t the target when ssds were more expensive (I’d say it was more like a $1000 USD pc that the multiplier was aimed at for a while).  But as someone who just synced the full blockchain on an $800 USD PC with 4 cores/8 threads, 32GB of RAM, and a fast NVMe SSD, I can tell you that thing was chugging and it still took almost two days.  With ETH1 nodes becoming the performance bottleneck in the beacon chain I am not at all eager to decrease the multiplier right now.  If people start switching over to Turbo Geth in production and it gives us more headroom, then I think there is more openness to changing the gas limit.  But right now on standard Geth there is definitely not room to increase it “substantially”.

---

**uri-bloXroute** (2020-10-20):

I would like to offer an alternative perspective:

syncing the entire chain on a $800 PC in under 2 days is stupidly *fast*, and increasing it is an inconvenience. Limiting the chain’s capacity, on the other hand, throws out users, prevent valid use-cases, and bleeds momentum to competing projects.

The latter is crucial - because momentum (tooling, ecosystem, network effect) is the most important moat ETH got over its competitors.

Ethereum is an invaluable infrastructure - it’s ok if you can connect immediately but it takes a few days to run your own infrastructure.

As per the implications on the beacon chain - I am *very* much against stalling ETH1 in any way for the sake of ETH2 (despite my support for ETH2!).

ETH2 is the major let’s-change-everything gambit, and it’s worth doing. But nobody knows if, when or how it will turn out (see Vitalik’s latest rollup-centric ETH1.5), and ETH1 should be improved and enhanced in iterative steps to the best of our efforts

---

**technocrypto** (2020-10-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/uri-bloxroute/48/9412_2.png) uri-bloXroute:

> But nobody knows if, when or how it will turn out (see Vitalik’s latest rollup-centric ETH1.5)

Look, I see that you’re new to these forums.  I’d suggest you poke around a bit.  The question of *if* ETH2 will turn out isn’t really something anyone here is worried about.  We’re definitely going to keep tweaking right until it does, because Ethereans are obsessed with optimisation and scalability.  But ETH2 isn’t a gambit, it’s a grind that we continuously and inevitably progress towards, taking the time that’s necessary to maximise properties like reliability, decentralization, security, efficiency, and theoretical rigour. Instead of just throwing things at the wall and seeing what sticks.

Second, nobody is “stalling” ETH1 for ETH2.  Turbo Geth, rollups, and other ETH1 improvements are proceeding in full parallel with ETH2.  Meanwhile ETH2 phase 0 is going to offer an enormous bump in light client security to ETH1, and an even more enormous bump to throughput in Phase 1. So it’s synergy we’re talking about, not tradeoffs.

There is a direct link between the gas limit we set and the social consensus we maintain about what sort of computer is required to sync the chain.  We have already made a thoughtful decision to permit *more* gas throughput in the ETH1 chain than chains like Bitcoin, which maintain a social consensus of targetting even smaller, cheaper machines.  But we are not interested in moving further towards the social consensus of networks like EOS where [much larger, more expensive machines are required to sync the chain](https://twitter.com/ercwl/status/1206930560838451201).  Technologies like Turbo Geth let us change the gas limit without changing the social consensus.  At literally any level someone could argue that *just* a little increase in gas limit won’t move the average node requirements much.  But we’re not looking to move the node requirements upward at all.  And hopefully we will move them downward as sharding arrives, and as disk i/o capabilities continue to improve.

Ever since Ethereum launched people have been breathlessly warning that if we don’t scale *right now* some type of “momentum” will be lost to “competitors”.  But those worries have always looked pretty silly [in the rear view mirror](https://twitter.com/cburniske/status/942402912952770560).  There are no wolves at the door.  Just like there weren’t last year, or the year before that, or the year before that.  People are using Ethereum far more than other chains *today*, and as someone who actually runs an ETH1 node in my home, I’d say we’re still on the upper end of the performance requirements we want.  Lots of people will sync a node if it they can do it in a couple days, but won’t if it takes over a week.  Those are just facts.  Personally, I’d like to see it reliably under 24 hours, and I think that Turbo Geth is going to give us that.  And whatever it gives us more, that can go into the gas limit.

But fundamentally this is a *social* question, which is why you’re being met with *social* rebuffing.  We don’t *want* to change our social consensus toward higher end hardware.  We *like* being in this sweet spot where serious enthusiasts can do it on home internet connections, and we might even want to *lower* the financial load for those enthusiasts.

Right now the CPU and SSD markets are doing exactly that, and we see that as a good thing.  That’s why we’re more excited about Turbo Geth and rollups than BDNs. It’s nothing personal.  I know for certain that if I started trying to argue with the Bitcoin community that they should raise their social consensus on hardware requirements to be more like Ethereum, they wouldn’t be interested in that either.  We’ve chosen our beds.  People know what to expect.  I built my $800 USD machine to run a node for years to come, and I’m counting on the community to keep that possible.  Being able to do that makes blockchain communities better.  Moving outside of the expected range [is considered a bug](https://github.com/prysmaticlabs/prysm/issues/7585).

