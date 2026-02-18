---
source: ethresearch
topic_id: 11651
title: Multidimensional EIP 1559
author: vbuterin
date: "2022-01-05"
category: Economics
tags: []
url: https://ethresear.ch/t/multidimensional-eip-1559/11651
views: 47593
likes: 76
posts_count: 20
---

# Multidimensional EIP 1559

Many resources in the EVM have the property that they have very different limits for **burst capacity** (how much capacity we could handle for one or a few blocks) and **sustained capacity** (how much capacity we would be comfortable having for a long time). Examples include:

- EVM usage: blocks occasionally taking 2s to process may be okay, but every block taking that long would make it extremely difficult to keep a node synced
- Block data: clients have enough bandwidth to process 2 MB blocks when they come, but not enough disk space to store them
- Witness data: same concern as data - clients have enough bandwidth to process medium-big witnesses, but not enough disk space to store them
- State size filling: there’s basically no limit to how much it’s okay to let state increase in a single block (if state blows up from 45 GB to 46 GB in one block but further state growth goes back to normal, who will notice?) as long as the witnesses can handle it, but we can’t have rapid state growth in every block

The scheme we have today, where all resources are combined together into a single multidimensional resource (“gas”), does a poor job at handling these differences. For example, on average transaction data plus calldata consumes ~3% of the gas in a block. Hence, a worst-case block contains ~67x (including the 2x slack from EIP 1559) more data than an average-case block. Witness size is similar: average-case witnesses are a few hundred kB, but worst case witnesses even with [Verkle gas reforms](https://notes.ethereum.org/@vbuterin/verkle_tree_eip) would be a few megabytes in size, a 10-20x increase.

Shoehorning all resources into a single virtual resource (gas) forces the worst case / average case ratio to be based on usage, leading to very suboptimal gas costs when the usage-based ratio and the ratio of the burst and sustained limits that we know clients can handle are very misaligned.

### This post proposes an alternative solution to this problem: multidimensional EIP 1559.

Suppose that there are n resources, each with a *burst limit* b_i and a *sustained target* s_i (we require b_i >> s_i). We want the quantity of resource i in any single block to never exceed b_i, and for long-run average consumption of resource i to equal s_i.

The solution is simple: we maintain a separate EIP 1559 targeting scheme for each resource! We maintain a vector of basefees f_1 ... f_n, where f_i is the basefee for one unit of resource i. We have a hard rule that each block cannot consume more than b_i units of resource i. f_i is adjusted by a targeting rule (we’ll use exponential adjustment since we know now that it [has better properties](https://ethresear.ch/t/make-eip-1559-more-like-an-amm-curve/9082)): f_{i,new} = f_{i,old} * exp(k * \frac{u_i - s_i}{s_i}).

To make this work in an Ethereum context, where there is only one resource (gas) that gets passed from parent calls to child calls, we still charge everything in gas.

- Option 1 (easier but less pure): we keep gas costs of execution fixed, and we keep the current EIP 1559; let f_1 be the basefee. The gas prices of all “special” resources (calldata, storage use…) become \frac{f_i}{f_1}. Blocks have both the current gas limit and the limit b_1 ... b_n on each resource. Priority fee works in the same way as today.
- Option 2 (harder but more pure): the gas basefee is fixed to 1 wei (or if we want, 1 gwei). The gas price of using each resource (of which execution is one) becomes f_i. There is no block gas limit; there are only the limits b_1 ... b_n on each resource. In this model, “gas” and “ETH” become truly synonymous. Priority fee works by specifying a percentage; priority fees paid to the block producer equal base fees times that percentage (an even more advanced approach would be to specify a vector of n priority fees, one per resource).

### Multidimensional pricing and knapsack problem objections

The main historical objection to multidimensional pricing models has been that they impose a difficult optimization problem on block builders: block builders would not be able to simply accept transactions in high-to-low order of fee-per-gas, they would have to balance between different dimensions and solve a [multidimensional knapsack problem](https://en.wikipedia.org/wiki/List_of_knapsack_problems#Multiple_constraints). This would create room for proprietary optimized miners that do significantly better than stock algorithms, leading to centralization.

This problem is much weaker than before in two key ways:

1. Miner extractable value (MEV) already creates opportunities for optimized miners, so “the ship has sailed” on stock algorithms being optimal in a meaningful way. Proposer/builder separation (PBS) addresses this problem, firewalling the economies of scale of block production away from the consensus layer.
2. EIP 1559 means that any resource hitting a limit is an edge case and not an average case, so naive algorithms will underperform only in a few exceptional blocks.

To see why (2) is the case, we need to note one very important fact: **in multidimensional EIP 1559, the “slack” parameter (\frac{maximum}{target}) for each resource can be much higher than 2x**. This is because the 2x slack parameter of today creates a burst/sustained gap that stacks on top of the burst/sustained gap that comes from unpredictable usage, whereas in multidimensional EIP 1559, the slack parameter represents the *entire* burst/sustained gap. For example, we could target calldata usage to ~256 kB (~8x more than today), have an 8x slack parameter (\frac{b_i}{s_i}) on top of that, and still have comparable burst limits to today. If witness gas costs are unchanged, we could bound witness size to another ~2 MB and have a slack parameter for witness size of ~6x. A survey of 240 recent blocks suggests that only 1 of those blocks would have hit the limit under a calldata slack parameter of even 4x!

This shows a nice side effect of multidimensional EIP 1559: it would make the boundary case of priority fee auctions much more rare, and clear sudden burst of transactions more quickly.

### What resources could be multidimensionally priced?

We can start with the basics:

- EVM execution
- Tx calldata
- Witness data
- Storage size growth

When sharding is added, shard data can also be added to this list. This would already give us a lot of gains in being able to support more scalability while mitigating risks from burst usage.

In the longer term, we could even make the pricing much more fine-grained:

- Split witness by read vs write
- Split witness by branch vs chunk
- Separately price each individual precompile
- Calls
- Each individual opcode

The main value of this is that it would add another layer of DoS protection: if each opcode is only allocated eg. 100 ms of max expected execution time, then if an attacker discovers a 10x slowdown in one opcode or precompile, they can only add 900 ms expected execution time to the block. This is in contrast to today, where they can fill the entire block with that opcode or precompile, so a 10x slowdown in *any* single opcode or precompile could allow the attacker to create blocks that cannot be processed in time for a single slot.

## Replies

**OisinKyne** (2022-01-05):

I think this would be a reasonable suggestion although I imagine it would be a significant engineering undertaking.

Would it be compatible with a non-linear basefee escalation model? I can’t find the exact piece I remember seeing (I don’t think I’m thinking of [your post along the same lines](https://ethresear.ch/t/make-eip-1559-more-like-an-amm-curve/90820)), that proposed that fixed 12.5% steps up and 12.5% steps down, although effective, were not optimal, and that an algorithm that could take dynamic steps up and down could handle a burst and return to its normal load faster. My napkin math suggests the basefee can currently rise at most 80% in a minute (1.125^5 \approx 1.8...) and takes as long to come back down.

My question is whether dynamism in the escalator algorithm(s) would be incompatible with having many distinct escalation algorithms.

If I had to guess, I would assume many distinct escalator algorithms, both static and dynamic are feasible in theory, but I’m not confident it wouldn’t make the equilibria too unpredictable, and whether we could cause unintended consequences to the stability of the system from different dynamic systems all conflicting with one another in a manner that might end up hurting the smooth inclusion instead of facilitating it. e.g. a spike in one resource triggering a larger spike in another resource through follow on effects.

---

**karl** (2022-01-05):

At a high level I really want this as I think it could lead to significantly lower transaction fees because devs can optimize much more precisely for resource usage. Also it would allow us to do things like increase the EVM execution capacity while still targeting fixed state growth.

My main concern I have is around EVM backwards compatibility. I think `Option 1` is much more realistic from this perspective. That said, I would love some really thorough analysis on backwards compatible similar to what we’ve been doing with address space extension. If we have to break some backwards compatibility for ASE maybe we consider slipping something like this in too?

Anyway, thank you for proposing this! Definitely an underrated topic & design space!!!

---

**vbuterin** (2022-01-05):

Yeah, this is fully compatible with dynamic escalation. That said, the greater slack parameter here arguably makes dynamic escalation less necessary, because eg. if the update parameter is 1/8 and the slack is 8x, then applying the formulas as-is mean that the basefee of each resource can increase by 1.875x per slot in conditions of high congestion.

> My main concern I have is around EVM backwards compatibility. I think Option 1 is much more realistic from this perspective

I feel like the backwards compatibility breakage from even option 2 is much less than the breakage from ASE. All that option 2 does is it re-adjusts the gas costs of everything, so you can no longer do hardcoded gas costs anywhere in a contract. Which seems like… where we want devs to go anyway?

That said, I agree that option 1 is a less risky change, because only a few operations (calldata, shard data, witness data use, storage size expansion) would be dynamic.

---

**Pratyush** (2022-01-05):

> block builders would not be able to simply accept transactions in high-to-low order of fee-per-gas, they would have to balance between different dimensions and solve a multidimensional knapsack problem.

I wonder if using scheduling algorithms like https://www2.eecs.berkeley.edu/Pubs/TechRpts/2010/EECS-2010-55.pdf would be interesting here. Would have to adapt these to account for adversarial behaviour, but might be a worthwhile thing to look into.

---

**Oraliks** (2022-01-05):

What if we can create automatically empty block to the chain before they are filled

---

**domothy** (2022-01-05):

How do per-transaction limits play into this?

Gas as an abstraction of resources makes it very straightforward for a user to say “I am willing to use up to 200,000 gas at a maximum of 100 gwei on this transaction with max priority fee of 2 gwei”, it’s very straightforward for every node to acknowledge that the user does have the funds necessary to pay for 200k gas × 100 gwei, and it’s very straightforward for the block producer to look at the mempool and say “This transaction is going to get me up to 200,000 gas × 2 gwei in priority fees”

With multidimensional EIP1559, would it be the job of the user to lay out ahead of time how much they’re willing to spend on each resource? For each of the resources, you would need: A max base fee, max priority fee, and a max usage limit. If every single opcode gets its own pricing, this would make for sizable transaction headers and additional checks.

Or do we scrap this “transaction gas limit” concept altogether in favor of a simple max total fee, i.e. “I am willing to spend up to 0.05 ETH in fees on this transaction”? This feels simpler for UX but terrible for nodes and producers to figure out which transactions can and can’t be included given the non-deterministic nature of resource usage and all the limits involved. Can’t exactly fail and revert the transaction at run time either, given that the same transaction could potentially be included in a later block with lower base fees.

Personally I’m okay with a separate pricing for calldata (and later on shard data) for the sake of more efficient pricing for rollups, but the rest seems like a lot of added complexity of granular pricing for little benefit; in the long run all I see the base layer doing is offering as much data as it can to rollups and the little execution happening there would be proof checking, which can be optimized in other ways (e.g. snark friendly opcodes if not a straight up snarkified base layer)

---

**vbuterin** (2022-01-05):

In option 1, the UX would look very similar to today. The gas costs of storage opcodes, calldata, etc, would be variable, but uncertainty in that would be handled through the tx gaslimit and not the max-basefee. In option 2, *everything* would be handled through the tx gaslimit, which de-facto *would* become a parameter saying “I am willing to pay a maximum of X”.

The complexity in multidimensionality going *too* high is definitely a good reason to stick to ~4 dimensions and not try to go beyond that.

---

**barnabe** (2022-01-06):

We’ve written a paper about dynamic adjustment schemes to the basefee controller, [Transaction fees on a honeymoon](https://arxiv.org/abs/2110.04753), maybe this is what you are referring to? But I agree with [@vbuterin](/u/vbuterin) 's comment that it gets less necessary as the slack becomes greater: it “speeds up” the dynamic system in a sense, instead of spreading over a few blocks a high demand signal, it more fully captures it via direct inclusion

---

**Michael2Crypt** (2022-01-07):

On the long term, the right fee for a simple token transfer is a few cents.

Because it means some wallets will offer the fee for watching an ad.

It means ordinary people will be able to transfer tokens for free, just watching an ad.

At this point, many influencers will create their fan tokens and give them away to their followers for free, knowing that they will be able to transfer them easily.

It will just develop the microeconomy around each influencer creating a token.

At this point crypto will really reach billion of people.

---

**MicahZoltu** (2022-01-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/michael2crypt/48/8077_2.png) Michael2Crypt:

> On the long term, the right fee for a simple token transfer is a few cents.

Fees aren’t “maximum a certain demographic of user is willing to bear”.  They are “minimum possible to incentivize people not using Ethereum when it can’t handle more users”.  If Ethereum had infinite space for stuff and there were no attack vectors, everything would be free.

The fees are dynamically adjusted such that the set of users willing to pay the most for inclusion (which is a proxy for those with the highest demand for inclusion) get included up to the threshold of “we can’t handle anymore users at the moment”.

---

**quickBlocks** (2022-01-09):

“up to the threshold of ‘we can’t handle anymore…’” is a perfect way of saying it. Someone should make a meme…

---

**yoavw** (2022-01-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Each individual opcode

Seems a bit too granular, and might introduce attack vectors on existing contracts. If the price of each opcode is controlled individually, it becomes much cheaper to manipulate it through selective spamming. Certain functions could become uncallable due to an existing gas limit, or even block gas limit.

If I understand correctly, it might also introduce a new censorship vector:  If gas price of individual opcodes becomes unpredictable, a short-lived targeted spam could cause specific mempool transactions to revert on chain (out of gas).

- Alice wants to call Contract.func(), simulates it and sends an appropriate gas limit.
- Eve watches the mempool for these transactions.
- Every time Alice sends the transaction, Eve frontruns it with a spam call which temporarily increases the cost of an opcode which Contract.func() uses extensively.
- Alice’s transaction reverts and is no longer in mempool, so Eve doesn’t need to keep spending ETH until Alice retries.
- Each retry costs Alice ETH until she runs out and stops sending.

Might also have an effect on EIP 4337 batching, since it introduces a new inter-dependency between orthogonal transactions (no shared state involved). Two orthogonal transactions extensively use the same opcode, each pushing the cost of the opcode and making the other one revert. If one succeeds, the other one reverts.

---

**imkharn** (2022-01-10):

The cost of an opcode would probably be or need to be fixed from the start of block execution to the end of block execution and known in advance based on the state at last published block. Additionally it could have a max percent increase per block. The attacker would then need to block victims transaction for enough blocks to get it to revert if ran. Victims could counter by having a higher gas limit.

There exist ways to fix issues that pop up, but I also had the same intuition about unknown unknown attack vectors. It might be one of those features that no matter how well researched, some issue will make it into production and cause a scene.

My method of achieving the goal would be to redefine each opcode to cost a fixed number of units of computation, storage, etc… For example, one opcode might cost 4 units of storage and 2 units of computation. Then the gas per store and compute etc would change predictably be known exactly in advance. For example, any user/wallet could know for sure that until the end of the current hour the cost per storage will be 3 gas, and the cost per compute will be 1 gas, and that next hour they know for sure all hour it will be 4 gas per storage and 1 gas per compute, but hour after next is unknown and can only be predicted. The changes would be locked in advance preventing various sorts of manipulation and unpredictability in exchange for being less reactive.

---

**yoavw** (2022-01-10):

You’re right that capping the max percent increase per block would make the attack harder to perform.  Short term predictability can protect mempool transactions, as long as they pay enough priority fee to be included within the next hour or so.

But your intuition regarding unknown unknowns is correct.  My concern is that it introduces a new way for transactions to affect the outcome of orthogonal transactions.  I think currently transactions are cross-dependent only if they access a shared storage slot, or call a shared contract that can be self-destructed.  Orthogonal transactions can only delay each other by competing on fees, but can’t change the outcome or prevent inclusion indefinitely.

The per-opcode gas prices are essentially global mutable variables, indirectly accessed by all transactions.  It may be introducing a way for orthogonal transactions to mess with each others, and will be hard to determine if we mitigate all of them.

In fact, even the less granular suggestions might introduce such vectors, but I’m not sure about the details.  It’s something we’ll have to research and see whether these changes could be detected by transactions - which means they could be used as global variables.

---

**wanderingbort** (2022-01-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The gas costs of storage opcodes, calldata, etc, would be variable, but uncertainty in that would be handled through the tx gaslimit and not the max-basefee.

There is already *too much* uncertainty in gas consumption and it is the cause of a great deal of end-user pain. The infrastructure for estimating gas, padding it, and the cost of it being wrong **to the end-user** is already too high.

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavw/48/6142_2.png) yoavw:

> My concern is that it introduces a new way for transactions to affect the outcome of orthogonal transactions.

This is my primary concern and cannot be understated in my opinion. While block limits can be made to not penalize an end-user with an out-of-gas error, the per-transaction limits cannot without opening up the network to exploit.

The longer your transaction is in the mempool the more likely it becomes that a malicious actor could drive up your transactions gas cost and exceed your per-transaction limit. This will disincentivize any use of the network that is okay trading time for lower gas fees and in an extreme case will probably push more traffic into MEV pools that maintain confidentiality as any time in the mempool is treacherous.

---

**ThomasdenH** (2022-01-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/wanderingbort/48/8327_2.png) wanderingbort:

> This is my primary concern and cannot be understated in my opinion. While block limits can be made to not penalize an end-user with an out-of-gas error, the per-transaction limits cannot without opening up the network to exploit.

What do you mean? Won’t a transaction just specify limits for every resource? For most resources this would just be the value as it is known beforehand so it wouldn’t be too tricky. A block proposer can determine in advance whether the transaction will fit in the block. What kind of exploit were you thinking of?

![](https://ethresear.ch/user_avatar/ethresear.ch/wanderingbort/48/8327_2.png) wanderingbort:

> The longer your transaction is in the mempool the more likely it becomes that a malicious actor could drive up your transactions gas cost […]

They can only do this without exceeding the maximum specified basefee. The user can opt to specify a tight maximum. My guess would be that it becomes easier to have a transaction pass since one expensive resource won’t necessarily be prohibitively so. But that is really just a guess.

---

**vbuterin** (2022-02-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/wanderingbort/48/8327_2.png) wanderingbort:

> There is already too much uncertainty in gas consumption and it is the cause of a great deal of end-user pain. The infrastructure for estimating gas, padding it, and the cost of it being wrong to the end-user is already too high.

![](https://ethresear.ch/user_avatar/ethresear.ch/thomasdenh/48/3760_2.png) ThomasdenH:

> What do you mean? Won’t a transaction just specify limits for every resource? For most resources this would just be the value as it is known beforehand so it wouldn’t be too tricky. A block proposer can determine in advance whether the transaction will fit in the block. What kind of exploit were you thinking of?

I was thinking that each transaction could specify both (i) a total gaslimit, and (ii) a limit for each f_i. So if you know the max gas your transaction is consuming, you won’t have a risk of OOG’ing: if the f_i values are wrong, then the transaction just won’t make it on chain.

---

**MicahZoltu** (2022-02-18):

Currently, the gas limit varies only if the code path taken changes.  For code with a single well defined code path, you have an exact gas limit.  Dapps can also calculate the worst case code path for a given execution environment off-chain and specify it when submitting the transaction.

I think introducing a new way for the gas required for a transaction to vary that is a function of current usage patterns of Ethereum is likely to introduce a lot of new complexity into dapp development.  If instead we vary the price of different opcodes, this mostly falls into existing paradigms that dapp developers and wallets already have to deal with.

One thing that I think would be almost required though is tooling for figuring out how much of each type of resource is consumed in a given execution.  Right now all tooling will tell you how much gas was used, but we would need all of this tooling to be updated to tell you how much of each *type* of gas was used so that max fee estimation can be done correctly.

---

**MisheruNeldon** (2022-03-19):

12.7 approximately basically and more sigma 11*11 121

