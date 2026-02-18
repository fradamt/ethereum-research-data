---
source: magicians
topic_id: 23589
title: "EIP-7934: Add bytesize limit to blocks"
author: Giulio2002
date: "2025-04-17"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7934-add-bytesize-limit-to-blocks/23589
views: 636
likes: 8
posts_count: 18
---

# EIP-7934: Add bytesize limit to blocks

This proposal introduces a protocol-level cap on the maximum RLP-encoded execution block size to 10 megabytes (MB), which includes a margin of 512 KB to account for beacon block sizes.

## Motivation

Currently, Ethereum does not enforce a strict upper limit on the encoded size of blocks. This lack of constraint can result in:

1. Network Instability: Extremely large blocks slow down propagation and increase the risk of temporary forks and reorgs.
2. DoS Risks: Malicious actors could generate exceptionally large blocks to disrupt network performance.

Additionally, blocks exceeding 10 MB are not propagated by the consensus layer’s (CL) gossip protocol, potentially causing network fragmentation or denial-of-service (DoS) conditions.

By imposing a protocol-level limit on the RLP-encoded block size, Ethereum can ensure enhanced resilience against targeted attacks on block validation times. Adding an additional margin of 512 KB explicitly accommodates beacon block sizes, ensuring compatibility across network components.

## Replies

**wjmelements** (2025-04-18):

I’m generally opposed to separate caps for separate resources as it complicates block building. We already have gas metering to constrain resource usage on every dimension. Large blocks with little execution aren’t especially worse than small ones with lots of execution; they both tax the network in different ways. The block gas limit already sets a size cap on blocks, and it can be increased without a hard fork. Your proposal would require a hard fork for future increases, which could give Ethereum the same ossification problem Bitcoin has right now. We will never know for sure if the last hard fork was the last ever.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/giulio2002/48/11035_2.png) Giulio2002:

> blocks exceeding 10 MB are not propagated by the consensus layer’s (CL) gossip protocol, potentially causing network fragmentation or denial-of-service (DoS) conditions.

Why don’t you fix this problem instead?

---

**SirSpudlington** (2025-04-18):

Looking at [Etherscan](https://etherscan.io/chart/blocksize) the highest block size ever was about 300 KiB, would there really need to be a 10MB limit? It seems like gas is already a soft-limit by itself and I don’t know whether a hard limit would be practical.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/giulio2002/48/11035_2.png) Giulio2002:

> DoS Risks: Malicious actors could generate exceptionally large blocks to disrupt network performance.

How would this be possible? With current calldata costs the upper bound to a blocks size is ~6MiB AFAIK. Either a malicious actor would have to include valid transactions from others, which is not malicious, or spend a significant amount of ETH to pay for these large transactions.

---

**siladu** (2025-05-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> Your proposal would require a hard fork for future increases

I like the protection this proposal provides, but agree that it’s not ideal to tie the CL gossip constraint to EL consensus. I don’t know how frequently the gossip limit may change but with this we will need an EL hard fork whenever it does.

---

**aryaethn** (2025-05-18):

As others already noted, the gas limit on each block already puts a cap on the amount of data could be stored in a block.

Also, with [EIP-7623](https://eips.ethereum.org/EIPS/eip-7703) already taking place on the Ethereum mainnet, it will be very costly and infeasible to upload large amounts of data without proper execution transaction.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/giulio2002/48/11035_2.png) Giulio2002:

> This proposal introduces a protocol-level cap on the maximum RLP-encoded execution block size to 10 megabytes (MB)

I believe this cap on the amount of data, i.e. 10MB, is unnecessary, and does not actually solve any problem.

And as [@wjmelements](/u/wjmelements) said:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> The block gas limit already sets a size cap on blocks, and it can be increased without a hard fork. Your proposal would require a hard fork for future increases, which could give Ethereum the same ossification problem Bitcoin has right now.

A hard fork is required for each update on the data store cap, which is a huge problem.

---

**aelowsson** (2025-05-18):

How about tying the cap to the gas limit instead? A 36M gas limit could impose a 3.6MB cap (1/10) or 1.8MB cap (1/20) for example. As the gas limit is adjusted, the cap changes with it. This would be like a multidimensional fee market, but with an upper bound on one of the resources as a proportion of all available gas.

Or do you consider the cap rather as a security measure that should be kept fixed as the gas limit increases?

---

**wjmelements** (2025-05-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aelowsson/48/14632_2.png) aelowsson:

> How about tying the cap to the gas limit instead?

This is the essence of the current behavior. You don’t need to make it more complicated.

---

**arnetheduck** (2025-06-10):

There is some prior discussion on this topic here: [Decoupling gas price from payload size · Issue #4064 · ethereum/consensus-specs · GitHub](https://github.com/ethereum/consensus-specs/issues/4064) - it highlights several options - in particular, it highlights that we can negotiate a max gas cap dynamically via an API extension which solves this problem without introducing arbitrary guesses about CL vs EL block size needs.

---

**Giulio2002** (2025-06-10):

We still have a devp2p limit. anyway, this cannot fit into consensus so it does not solve the underlying issue

---

**arnetheduck** (2025-06-10):

Since the devp2p protocol is not gossiping any more, merely responding to requests, there’s no real need for a (tight) limit there (specially since the protocol is only used for syncing, ie at a time when there’s little else useful going on). The bigger problem is typically the gossip mechanism that has an amplification factor (on the CL side), which is why it stands to reason that it remains the main source of truth for any block-based limits.

---

**Giulio2002** (2025-06-10):

you need to sync with DevP2P. that is quite a huge usecase because you cannot run nodes with blocks too big

---

**Giulio2002** (2025-06-10):

actually, it is even worse if it is accepted by gossip and rejected during sync because there is no going back in that case.

---

**rjl493456442** (2025-06-17):

We should consider modifying the EIP slightly to allow including withdrawals without a size limitation.

In theory, the consensus layer can specify an arbitrary number of withdrawals to include, and the execution layer **MUST** include all of them.

---

**aelowsson** (2025-07-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aelowsson/48/14632_2.png) aelowsson:

> How about tying the cap to the gas limit instead? A 36M gas limit could impose a 3.6MB cap (1/10) or 1.8MB cap (1/20) for example. As the gas limit is adjusted, the cap changes with it. This would be like a multidimensional fee market, but with an upper bound on one of the resources as a proportion of all available gas.
>
>
> Or do you consider the cap rather as a security measure that should be kept fixed as the gas limit increases?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> This is the essence of the current behavior. You don’t need to make it more complicated.

It is *not* the current behavior to bound resource consumption along any dimension in the block. A cap tied to the gas limit is a very simple way to unlock most of the scaling gains of a multidimensional fee market, simply by imposing a maximum constraint on the critical resource (data). The invariance where the data relative to compute remains fixed as the gas limit varies seems like a rather natural choice.

For reference, there is currently a [proposal](https://ethresear.ch/t/a-practical-proposal-for-multidimensional-gas-metering/22668) that relies on similar upper bounds on resource consumption. This proposal also changes the base fee as any resource pushes against that bound, but it is not at this point clear that a singular base fee is desirable. Therefore, a simple cap on payload size tied to the gas limit could be the right short-term approach for scaling Ethereum L1 (implying here discounts for beacon block size).

---

**wjmelements** (2025-07-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aelowsson/48/14632_2.png) aelowsson:

> very simple way to unlock most of the scaling gains of a multidimensional fee market

It’s not a market if there’s no pricing. If the limited, contended resources are not priced differently than the abundant plentiful ones, then we won’t get the benefits, but we will get the complexity.

---

**aelowsson** (2025-07-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> It’s not a market if there’s no pricing. If the limited, contended resources are not priced differently than the abundant plentiful ones, then we won’t get the benefits, but we will get the complexity.

I am in favor of implementing a multidimensional fee market. This is however a complex endeavor. A benefit of a multidimensional fee market from a scaling perspective is the hard limits it imposes on individual resources consumed by a single block. Such hard limits would allow us to trim the slack and tighten timelines, unlocking scaling gains in terms of higher gas limits and shorter slot times. We can however impose such hard limits even without/before specifically designing a multidimensional fee market. There is no strong economical reason to provide slack for a block consisting only of, e.g., calldata, and we can therefore cap, e.g., the amount of bytes per gas in a block, set such that, e.g., 99.9% or 99.99% of current blocks still would pass these limits.

The best critique I can come up with against tighter caps on byte size is that builders have an incentive to only build blocks that can pass any potential caps anyway, seeing that they want their blocks included. There are still good reasons to make the limits of the protocol explicit. It makes it much easier to reason about the protocol when the limits are enforced instead of implied. We could then be more comfortable in raising the gas limit or shortening the slot time. Explicit limits also serve a purpose when the builder cannot control the byte size of a block. A good example is [FOCIL with transaction hashes](https://meetfocil.eth.limo/focil-but-with-transaction-hashes/). In such a design, includers could force up the byte size by including hashes to big txs, and a cap on the byte size would need to be explicit to protect builders.

---

**wjmelements** (2025-07-08):

> builders have an incentive to only build blocks that can pass any potential caps anyway

All right, next I am going to try explain to you why market prices are good. I think that is what you are missing.

Suppose you are a user and your transaction is not included. Today you could just raise the gas price. How much should you raise it to? You just check the base fee.

I remember how things were before EIP-1559. If you wanted to get your transaction included, you would have to have a good view of the mempool. Most users subscribed to a service like EthGasStation, which provided an API providing estimated gas prices. But due to MEV and private orderflow, predicting the upcoming block is much more difficult now, and you are proposing to increase this complexity.

If tx flow is disproportionately loading against a constraint, eg size, builders are able to reprice this internally, choosing transactions that pay higher priority fees to win this resource. However this scenario is invisible to the users. In order to know how much they have to pay to get their transaction included, they would have to process all pending tx flow (of which they can only see the public mempool), performing the NP-complete task of block building, to determine which of the multidimensional constraints they are in contention with. Only by simulating all orderflow is this possible. Only then, in this example, they might discover that while the base fee is 10 gwei, the priority fee for calldata is currently 200 gwei.

For another example, consider if instead of a separate blob gas price, blobs and transactions had one gas price. Depending on the price of regular gas, blobs might be entirely priced out of existence, or might outbid other resources. So you would propose a separate blob gas limit. The blob gas price would still not be able to go below the base fee. If you wanted to get a blob in quickly, you would have to know about all of the pending transactions that are currently trying to insert blobs. Many of these are private orderflow, so you would have to subscribe to some Titan Builder API to get a complete picture.

So by taking this shortcut, the core developers are offloading the burden of creating a multidimensional fee market onto builders. However, it is not only the sellers of blockspace that are affected. The purchasers also have to do this calculation. And though we have saved the core developers a few weeks of development time, we have granted a complete monopoly on transaction fees to Titan Builder. Every wallet would have to ask them what priority fee is needed for their particular transaction to be included quickly. We cannot expect each transaction to analyze the entire mempool along every dimension you might want to constrain.

This problem is not solved by additional blockspace. For any amount of blockspace there is a supply and a demand. The current intersection of these should be at a visible price. If only the seller can compute the price, they have a huge advantage over the buyer. Prices provide transparency to otherwise complex economic calculations.

---

**aelowsson** (2025-07-08):

That’s a very nice overview. As stated, I am very much in favor of a multidimensional fee market, so you are preaching to the choir on the merits of it. But I think you captured it very nicely, so I am still thankful for the answer. I am not suggesting changes that would have a price impact on transactions (i.e., priority fees). The purpose is to limit rare outliers that may even only happen artificially. There should be no effect on priority fees, and certainly no effect that comes close to the variation that happens naturally as a function of fluctuations in transaction demand.

The context of my initial suggestion is delayed execution/ePBS, which opens up for vastly more compute each block and shorter slot times. All of this in the absence of a multidimensional fee market, which may not be realistic for Glamsterdam. We must in this context decide how we wish to approach the size of the execution block. If we wish to ensure that the largest possible execution blocks must safely be able to propagate, it is possible (depending on specific choices made) that we will have to limit gas throughput by shifting the payload deadline. We may as an alternative instead facilitate higher throughput by imposing certain limits on the payload, touching only (potentially “artificial”) outliers. The conversation I am interested in is if such limits should be enforced implicitly or explicitly.

