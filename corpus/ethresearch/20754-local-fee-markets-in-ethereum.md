---
source: ethresearch
topic_id: 20754
title: Local Fee Markets in Ethereum
author: keyneom
date: "2024-10-24"
category: Economics
tags: [fee-market]
url: https://ethresear.ch/t/local-fee-markets-in-ethereum/20754
views: 720
likes: 5
posts_count: 15
---

# Local Fee Markets in Ethereum

### Proposal for Implementing Local Fee Markets in Ethereum

**Objective**: Introduce a local fee market mechanism to manage network congestion and ensure fair fee distribution, applying dynamic fee multipliers based on high-demand storage locations while maintaining accurate and predictable fee estimates.

### Current Mechanism

Ethereum currently uses the EIP-1559 model for transaction fees, where the base fee is dynamically adjusted based on network demand to target an optimal gas usage per block. Wallets estimate transaction costs using the base fee and gas limit.

### Proposed Enhancement

**Over-Target Adjustment**:

1. Identify High-Demand Addresses: When a block exceeds the target gas usage, track accounts whose storage writes consume more than 1/16th of the total gas used in that block. It could be 1%, 50%, or any desired percentage instead of 1/16th but this impacts how many accounts end up needing to be tracked across blocks so adds to memory requirements.
2. Calculate Fee Multiplier: Determine a fee multiplier for these high-demand addresses based on their “excess” gas usage.

**Fee Multiplier Application**:

1. Transaction Simulation with eth_estimateGas: Simulate transactions using eth_estimateGas to determine which storage locations and addresses are accessed.
2. Return Additional Data: Modify eth_estimateGas to return a list of touched addresses and storage locations during the simulation.
3. Apply Multiplier: Apply any existing fee multiplier to the base fee for transactions that interact with currently identified high-demand addresses.
4. Reducing Multiplier: If a given block’s gas usage falls below the target gas then the multiplier is removed and everything returns to normal. If the account no longer consumes more than the 1/16th threshold amount the multiplier reduces by an equal amount it would have increased by if it had surpassed the threshold until it is back at the regular base fee.

### Multiplier Compounding

The fee multiplier can compound across blocks:

- Incremental Multiplier: If an account remains over the target usage in subsequent blocks, the multiplier increases further.
- Cumulative Effect: The multiplier builds over time, applying an increasingly higher cost to transactions involving persistent high-demand addresses.

### Example Process

1. Block N Analysis:

Total gas used: 20 million units. (this is above target gas so a contention multiplier will be applied)
2. Account A’s storage writes: 3.2 million units
3. Threshold: 1.25 million units
4. Excess usage: 2 million units (10% over threshold)
5. Multiplier Calculation:

Initial Multiplier: 1.10x (since we are 10% over threshold, but this multiplier could be modified depending on how much we want fees to increase faster for hot spots than other locations).
6. If Account A exceeds the threshold again in Block N+1, the new multiplier increases:

New excess percentage: 10%.
7. Compounded Multiplier: 1.10x (previous) * 1.10x (current excess) = 1.21x.
8. Fee Estimate for Block N+2:

Base fee for Block N+2: 100 gwei.
9. Effective fee for transactions involving Account A: 100 gwei * 1.21 = 121 gwei.

### Benefits

- Predictability: Users can rely on accurate fee estimates without requiring extensive transaction simulations.
- Fair Access: The fee increases are localized to high-demand storage locations, allowing other users to access the network at lower costs.
- Transparency: Users are informed about potential high-cost interactions, maintaining transparency in fee calculations.

### Implementation Steps

1. Modify eth_estimateGas: Enhance the function to return additional data indicating touched storage locations and addresses.
2. Track High-Demand Addresses: Maintain a list of addresses that exceeded the 1/16th gas usage threshold from the previous block.
3. Wallet Integration:

Update wallet software to use the additional data from eth_estimateGas for fee estimation.
4. Implement logic to apply the fee multiplier when high-demand addresses are detected.
5. Ensure compounding of multipliers if the same addresses continue to exceed thresholds in subsequent blocks.

### Weaknesses

- Fee increases are not entirely localized
- Might be complex enough that we want to switch to providing touched addresses with the transaction up front to better support parallelization.
- Unclear how impactful this would be to keeping fees lower on L1 for p2p payments or other use cases that some people feel L1 shouldn’t be used for.
- From a historical perspective, I haven’t looked at how often a smart contract is getting touched that it would surpass the 1/16th (or w/e we decided on) gas trigger for the multiplier to take effect.
- Popular apps on mainnet are probably opposed to getting charged more for being popular (another reason to spin-off as an alt-L1 or L2?)
- Probably a pain to implement anyways

### Conclusion

This proposal seeks to enhance network fairness by dynamically adjusting fees based on actual resource consumption, maintaining predictable transaction costs for users. By applying these targeted fee adjustments, Ethereum can manage localized congestion effectively without requiring significant changes to the existing fee estimation processes. While there are some downsides to this approach I think it could be a reasonable step-wise approach to avoiding noisy neighbor problems on Ethereum improving its position as an app platform.

Feedback and further refinement are welcome.

## Replies

**MicahZoltu** (2024-10-25):

Why do you believe that a contract that is infrequently used should be cheaper than one that is frequently used?

How do you prevent people from just bloating state by spreading out activity across many accounts or many contracts in order to reduce gas costs?

---

**kosunghun317** (2024-10-25):

Wouldn’t this approach simply increase transaction costs for several popular coins without offering meaningful performance improvement?

---

**keyneom** (2024-10-25):

I don’t. In the regular scenario, price is the same for everyone. It’s only when a hotspot is identified where everyone wants to access it at once that access becomes more costly for them. I could flip the question and ask why everyone has to pay more to do a simple Eth transfer just because a bunch of people are trying to claim an airdrop? Why do we all have to pay for their degeneracy ![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=12)? This speeds up price discovery and leads me to a point that I forgot to mention but that a comment on Twitter reminded me to bring up.

The system as currently described is a bit volatile. As soon as we hit target gas all prices return to normal. This was intentional on my part mostly because it still has the function of spreading out demand over time. But fees to access the in demand state can go from very high to much lower very quickly and then have to “rediscover” the price for access to that state again. While this is simpler in my opinion, you could also make it so that the multiplier stays in place and only moves up or down depending on whether gas used is above or below the threshold regardless of where overall gas used is to target gas until the multiplier returns to the regular base fee. It might be the better approach.

Returning to the point of your post. When one part of a system absorbs all resources it starts preventing other portions of the system from functioning properly. As an example, let’s say an airdrop is very popular and viewed as extremely valuable so much so that base fee starts hitting into the hundreds or the thousands. Oracles (especially those that are just getting started) realize they don’t actually have the funds to post updated prices for a number of coins. Defi markets that are relying on those price feeds are out of date and start getting manipulated or liquidations occur that shouldn’t have. If I’m building an app on a system, I want to be sure that there are enough resources available to keep all parts of the system running at all times without letting one part of it freeze up everything else to the point that something it itself relies on no longer works (in the happy case that reduces demand for the contentious state but in the unhappy path it could actually increase demand for the contentious state). So as I originally mentioned, in order for Ethereum L1 to function as an effective app platform it needs some degree of parallel processing that allows other systems to continue functioning even when one part of it has extreme demand. Pretty much all operating systems for computers work this way now to ensure important parts of the system are not resource starved. Credible neutrality hampers us from doing so in as direct a manner on the world computer but ideally we still get some parallelism capabilities. Ethereum is an app platform, when an app platform is designed in such a way that one app interferes with the ability of other apps to function (make fees, etc) it is poorly designed.

E.g. if dynamo DB on AWS had been designed in such a way that any app built on it could disrupt the ability of the other apps to function they never would have attracted people to build on it. It never would have scaled. I’d prefer people can build on Ethereum with confidence, hence the proposal.

This brings me to my next point. This type of design can actually be beneficial for data center chains (i.e. L2s) because you can split state across multiple data partitions and high contention on one part of state doesn’t end up receiving all of the load. When you pair this with things like optimistic parallelism on execution instead of a single threaded approach I think you can get almost all the benefits of full parallelism (allow for higher target gas).

---

**keyneom** (2024-10-25):

I touched on this in my reply above but let me know if you have follow up questions.

---

**MicahZoltu** (2024-10-26):

Interesting line of thinking, and notably more convincing than I expected.  There is still the issue of people designing their code to be spread out over a large surface area to avoid getting hit by spike in demand pricing.  I’m not sure how you could implement this in a way that isn’t gameable.

---

**keyneom** (2024-10-26):

I think there are natural limits to how much they can spread out their code and still have it be functional. Luckily for us I believe a good balance is at the account level, so any writes to the storage of an account at a specific address probably does a decent job of giving us the benefits we are looking for.

---

**MicahZoltu** (2024-10-26):

It would not be hard to “shard” some token across many different addresses.  You can have a single proxy entrypoint that doesn’t have any storage reads/writes in it that handles routing so your total cost is just an additional call (not much more than an upgradable proxy or similar), yet your contract reads/writes would be spread out over hundreds or thousands of addresses.

---

**keyneom** (2024-10-26):

That’s fair, I’m not positive it’d always be feasible but perhaps. If we wanted to catch more scenarios we could include the entry contract as well. People could then try to shard outside of the chain though in a UI or otherwise.

One way to counteract this would be to just take the difference between the base fee and the multiplier and just have those go to the app developer. Then they have a natural incentive to keep things in a shingle contract. This does run into a bit of the problem of having an incentive to write less gas efficient contracts but it’d be at the expense of end users only under heavy usage conditions so that might be enough of a deterrent to keep them from giving the average user under normal use a less ideal experience. I think it might strike a reasonable balance though it might overly incentivize launching airdrops with odd properties that encourage contention instead of avoiding it.

In any case, I don’t think sharding state to avoid the additional fees has really seen much adoption on Solana (and it kind of helps solve the tech hot spot issues for us if they do) even though we might not get the full benefits of avoiding a run up of fees for everyone else. To some extent I think it’s impossible to guarantee contracts aren’t actually all part of one big master application (some might call that application Ethereum). But I think you could still socially discourage that kind of approach. There might be other heuristics we could use but I think most fall apart at the point when you start adding a bunch of offchain logic. I don’t think I really see that (extensive contract sharding) as being too likely to occur though.

---

**MicahZoltu** (2024-10-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/keyneom/48/19968_2.png) keyneom:

> we could include the entry contract as well

People will just create proxy factories that can trustlessly pump out shards as needed.

![](https://ethresear.ch/user_avatar/ethresear.ch/keyneom/48/19968_2.png) keyneom:

> just have those go to the app developer

The app developer could be a contract account that just kicks the fees back to the users.

The underlying problem here is that we *really* don’t want any incentives to increase state bloat (number of items stored, number of contracts, number of accounts, etc.).  Even the smallest incentive to increase state can lead to very rapid state expansion.  Every incentive should push people towards *fewer* contracts (smaller state), not more.

---

**keyneom** (2024-10-26):

I dunno, like I said I think there are natural limits to how much I can do this in practice. If I have to call into 16 different contracts to read the size of the liquidity pool, are the potential gas savings under contention really worth the ongoing x additional costs to just be able to calculate how much a swap is moving the market? The other option I see is fragmented liquidity but we already know that’s not ideal. I think most of the time you’d benefit just doing things the simple way. Are there a lot of scenarios you imagine being functional and not incurring higher median gas through a sharded approach?

---

**MicahZoltu** (2024-10-27):

Never underestimate the ability for incentives to be gamed.  With little thought, I can imagine ways to shard a token contract so (the simplest and most common type of contract on Ethereum), and I could easily shard an airdrop claim or “staking” scheme in ways that would cost very little gas overhead (a single proxy contract at most, and even that could be abstracted away with some effort).  Once you create incentives, people will spend a *lot* more thought than just the couple minutes I have to figure out ways to shard more complex contracts like swapping protocols.

We shouldn’t be thinking about specific attacks, but rather what sorts of behaviors we are incentivizing.  Future people will think much harder than we will about this than we will in hypotheticals.  In this case, we would be incentivizing people to spread load out across a larger address space in order to get lower costs, and that is the concern that I have.  Can the concept be retained without incentivizing spreading out load across a larger address space?

---

**abdouecon** (2024-11-12):

Hi all,

I’m sharing on this research platform some of my research on the economics of local fee markets https:/\papers.ssrn.com/sol3/papers.cfm?abstract_id=4985253

and the earlier talk that accompanies it: https:/\www.youtube.com/watch?v=UD_7Crtxy-k

Comments welcome

---

**keyneom** (2024-11-12):

Assuming the paper covers the same thing the video did it looks like an interesting approach to fair ordering of transactions. I watched the video at double speed so I might have misunderstood some parts of it. It sounded like base fee doesn’t actually change for anyone, just that we are determining an ordering rule that enables txs to be included even when they are not paying as much. I’m assuming the thought process here is that we have some kind of ILs that are restricting the validator’s freedom to include transactions that might be more profitable for them. Is that correct?

---

**keyneom** (2024-11-12):

You could probably split the multiplier fee between being burnt and going to the address. I think that gives reasonable incentives. In the normal case you keep gas costs as low as possible. In the case that you are seeing high traffic to your contract you are somewhat rewarded for building something of interest to the network. Obviously that can be returned to users but if it is only half of the multiplier fee then you still have an effective multiplier with its own fee market and devs have incentives to avoid irrationally sharding their logic since they can keep a portion of what is retuned to them.

