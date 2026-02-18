---
source: magicians
topic_id: 24746
title: "EIP-7987: Transaction Gas Limit Cap at 2^24 (EIP-7825)"
author: Nerolation
date: "2025-07-06"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7987-transaction-gas-limit-cap-at-2-24-eip-7825/24746
views: 1129
likes: 35
posts_count: 29
---

# EIP-7987: Transaction Gas Limit Cap at 2^24 (EIP-7825)

Discussion topic for [EIP-7987](https://github.com/ethereum/EIPs/pull/9984#pullrequestreview-2991679894)

#### Update Log

- 2025-07-06: initial draft
- 2025-07-07: Withdrawn in favor of EIP-7825 including the changes: https://github.com/ethereum/EIPs/pull/9986

#### External Reviews

None as of 2025-07-06

#### Outstanding Issues

None as of 2025-07-06

## Replies

**bbjubjub** (2025-07-06):

consider the following scenario: the gas limit is 45M, and there are three 16.7M transactions in the mempool and nothing else that pays the base fee. Then the block builder can only include two of those and we lose almost 33% of the block. That’s an unlikely edge case, but that’s a peculiarity of this cap compared to 30M or 15M. What we could do though is agree that the block gas limit should be n*2**24 so that we can guarantee that the block builder can include at least n transactions if the mempool has at least n.

The concerns expressed in the [EIP-7825 thread](https://ethereum-magicians.org/t/eip-7825-transaction-gas-limit-cap/21848) of course still apply to this EIP, as much if not more so.

(also the github link is to the wrong EIP)

---

**Nerolation** (2025-07-07):

This isn’t how the fee market works, and what you’re describing is block packing (in-)efficiency. If the only transactions that can make it in are two 16.7M gas ones, then either the basefee is high and those senders are willing to burn a lot of ETH. With the exponential pricing from EIP-1559 in place, it definitely is a edge case.

Also, gas must be paid for: it’s **not** enough to just set a high gas limit but use little gas. So this kind of spamming “attack” isn’t actually an attack, the cost is simply too high.

---

**wjmelements** (2025-07-08):

The best motivation here is parallelization. Singular transactions are purely sequential. While unbatching transactions doesn’t improve the worst case, it can improve the best case.

> A fixed cap reduces the risk of DoS attacks caused by excessively high-gas transactions.

I’m not convinced of this. Gas is fungible. If a malicious user is outbidding everyone else with one transaction, they can also outbid with two transactions at the same price. Can you elaborate what you mean?

> By capping individual transactions, the validation of blocks becomes more predictable and uniform.

If fewer transactions are more burdensome than more transactions, that just means that the base transaction gas (21000) should be recalibrated. It is possible that the gas advantage of batching is too large, if the transaction overhead (nonce, signature, value) isn’t properly calibrated.

I don’t think this is the correct solution to facilitate parallelization. I can DoS your parallelization by creating a bunch of transactions reading and modifying the same slot. In the same block, this would be worse than a singular transaction. Perhaps a better solution would consider this possibility. I know you’ve also been doing work on the block access list proposals. Perhaps hot slots should cost more, not less. An alternative solution might be for the block producer to specify the before and after values per transaction, which would allow the contentious transactions to be validated in parallel.

---

**Nerolation** (2025-07-08):

Yeah agree, it’s mostly about enabling parallelization, assuming we eventually have the tools for parallel validation.

On DoS risks, I’m more worried about unknown unknowns, e.g., quadratic attacks where some resource doesn’t scale linearly. If an attacker fills a block with max calldata or `SLOAD`s, splitting into 2–3 txs only adds ~21k gas each, so the mitigation is weak. This is true and I wouldn’t even call it a mitigation for such attacks at all.

With block-level access lists, we might want to revisit pricing, possibly deprecate warm access discounts or add caps on storage.

Declaring touched accounts/slots could lead to block bloat if a tx intentionally hits random addresses or storage. You’d get to a worst-case block larger than the worst-case calldata block if you don’t reprice storage at the same time.

I explored some sizing impacts here:


      ![image](https://hackmd.io/favicon.png)

      [HackMD](https://hackmd.io/@Nerolation/r1-wG1rCyg)



    ![image](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###



One of the hot topic of the recently (re-)ignited push towards scaling the L1, in particular, the execution layer, are block-level access lists (BALs).

---

**sbacha** (2025-07-09):

[github.com](https://github.com/mds1/convex-shutdown-simulation)




  ![image](https://opengraph.githubassets.com/0ddb0ac5d753cfae2474c62864aee9cc/mds1/convex-shutdown-simulation)



###



Simulates a call to Convex Finance's system shutdown method, which uses about 16M gas










Some projects do have use cases for transactions exceeding this limit, for example “Emergency Shutdown” (re: global settlement and the ilk). Convex has `systemShutdown` that exceeds 16M in one, giant, transaction.

---

**Nerolation** (2025-07-10):

Thanks for this resource. Reaching out to matt with more questions.

Do you know more such examples?

---

**sbacha** (2025-07-16):

How old do you want?

---

**wminshew** (2025-07-16):

if we set the txn gas limit cap ~at the current block limit and then keep it fixed as the block size expands, we don’t have to ship something that isn’t backwards compatible (but hopefully get the ~same long term benefits?). Just an idea I wanted to throw out there, anyway

---

**Nerolation** (2025-07-17):

That’s true but it also means intentionally choosing to allow a few large transactions at the cost of limiting scaling potential that many others could benefit from.

Backward compatibility is, of course, very important. Changes like the one being proposed must be made carefully, with full consideration of the trade-offs and the parties affected.

Still, after weighing everything, I’ve come to the conclusion that the change is worth it.

---

**duncancmt** (2025-07-24):

Why not set this limit to the “conventional” limit of 30M? If we’re already seeing broken dApps as a result of the low ~16M limit, why not enforce the “old” limit that dApp developers built into their smart contracts.

I bang this drum a lot, but not making backwards-incompatible/breaking changes is a major sin for L1 developers. The EVM ecosystem has an active and vibrant developer base precisely because Ethereum is a stable platform for immutable smart contracts. Breaking things (even if it appears inconsequential) is a violation of that trust and squanders the goodwill that has been built up.

---

**sbacha** (2025-07-26):

Another example, however this won’t be the case going forward for Eigenlayer:

> take one of Renzo’s EigenPods. This pod has 1775 validators, representing 56,800 ETH in TVL. When Renzo wants to checkpoint their validators to process validator exits/accrued beacon chain rewards, this requires 24 transactions and ~99 million total gas spent.

source: https://hackmd.io/uijo9RSnSMOmejK1aKH0vw?view

---

**Nerolation** (2025-07-29):

Hey [@duncancmt](/u/duncancmt), it’s a completely valid concern and one we took seriously throughout the discussion.

Ultimately, it’s always a trade-off. Even a 30M cap would’ve already introduced backwards incompatibilities for certain users. Now that the block gas limit has sat at 36M for quite some time and we’re now at 45M, a 16.7M cap means we’re drawing a line in the sand, not because we want to break things, but because many believe it’s necessary to enable more meaningful scaling and parallelization in the long run while keeping the chain safe. It’s worth the cost.

That said, you’re absolutely right that trust and platform stability are core to Ethereum’s success. The decision was made after weeks of open discussion and broad agreement that this cap is needed.

---

**duncancmt** (2025-07-29):

I hear you regarding the open discussion, but please keep in mind that application teams (e.g. me) don’t follow the EIP process at every step. Unfortunately, my top priority is developing an application and keeping it running, not participating in the EIP/ACD process. So “weeks” (in this case ~3 weeks, from what I can tell from the timestamp on this thread an on the GitHub PR) is really ***REALLY*** not enough time to solicit feedback and assess impact on the EVM ecosystem.

I’m not saying that a cap isn’t needed. Clearly it is. What I’m saying is that setting the cap to ~16.8M is a bad idea and breaks stuff.

> It’s worth the cost.

Hot take: it’s worth the cost because you’re not the one paying it.

---

**Nerolation** (2025-07-29):

I see your points, and overall, I agree, backward compatibility is important, and usually app developers should be able to trust that Ethereum won’t change that fundamentally that their apps break.

That said, backward compatibility isn’t a binary issue. If the goal is *zero* disruption and we’re willing to get *zero* gains, then sticking with 45m or 36m makes sense.

I agree that 30m offers a better trade-off between gains and compatibility concerns than 36m, but 16.67m pushes that trade-off even further in the right direction.

Ultimately, many app developers have been calling for greater scalability, which is why this discussion was reopened in the first place. Large transactions are becoming a real bottleneck, and reducing the transaction gas limit is one very effective way to address it.

---

**duncancmt** (2025-07-29):

If the goal of this EIP is to force application developers to produce transactions with lower gas limits, then I can say wholeheartedly that I oppose this EIP and that it is a bad idea. Furthermore, I’m not seeing these “gains” that you describe. What is the scalability/load impact of a single 30M transaction vs a pair of 15M transactions back-to-back? What about the single-transaction gas limit hampers scalability in a way that the block gas limit does not? Perhaps my vision is limited by my place in the ecosystem.

> usually app developers should be able to trust that Ethereum won’t change

There is no “usually” about it. Either Ethereum changes (somewhat frequently, I might add) in ways that break dApps, and consequently dApp developers cannot trust the platform upon which they build. Or Ethereum prioritizes backwards compatibility and that trust is retained. I don’t want Ethereum to end up in a state where every audit report contains a finding of “Non-upgradeable contracts may be broken in unpredictable ways by a future hardfork” whenever there’s immutability.

> backward compatibility isn’t a binary issue

Ahh, but it ***is***. Either a change breaks existing dApps or it does not. If the limit were set to 30M (before the recent increases) then it would emphatically be a nonbreaking change. Likewise, if we were to set it to 45M now, it would be nonbreaking. With the limit set as it is, this is a breaking change. Breaking changes on a platform that demands immutability is not acceptable. Doubly so when it has already been demonstrated upthread that this change breaks a security-critical function for a large (high-TVL) DeFi protocol.

---

**wminshew** (2025-07-29):

> many believe it’s necessary to enable more meaningful scaling and parallelization in the long run while keeping the chain safe. It’s worth the cost.

I am seeing plenty of people talk about future gas block limits of 100+m, so setting the txn cap at 30m (or 36m) seems like it accomplishes the same goal in the long-term without breaking *anything* in the short term.

What data or analysis can you provide on the scalability improvements of a txn cap at 30m vs 16.7m once the block gas limit is at 300+m and the L1 runs on zkevm? Otherwise if this is some short term measure, it’s absolutely not worth breaking app developer trust, esp given the alternative scaling options at hand

---

**Nerolation** (2025-07-30):

There’re 3 points here: parallelism, zk proving, quadratic attacks.

If you have perfect parallelism, then comparing worst-case block sizes depends solely on the number of cores available. Today, the worst-case block can consist of either one large transaction or many small ones that effectively do the same thing, because transactions are executed sequentially. So, having one core available for transaction execution is effectively the same as having two.

With parallel transaction validation, this is no longer the case. Having two cores can give you a 2x. It becomes clear that some form of parallel EVM is inevitable if we want to go beyond 100m. In the worst case, you could leverage 5–6 cores (100/16.76) instead of just 2–3 (100/36), effectively doubling worst-case processing throughput.

However, it’s more difficult to enable parallelism *within* a single transaction, so large transactions can’t simply be broken down into smaller chunks. This is the same challenge faced by zk-provers.

So, both valuable scaling strategies, parallelism and zk proving, benefit from a lower per-block gas cap. This directly conflicts with the desire for backward compatibility from dapp developers.

Re, robustness of the protocol, transactions consuming extensive gas have been the source of a bunch of issues in the past. Quadratic attacks are real and become increasingly dangerous with increasing gas limits. Many parts of the protocol benefit from preventing txs from excessive gas usage (e.g. public mempools and inclusion lists).

I fully understand that tension, and I’m not saying your point is wrong. It’s a trade-off.

---

**duncancmt** (2025-07-30):

If the goal here is to improve worst-case parallelism (and consequently avoid DoS attacks on validators/zk provers), then this EIP does not help. Assuming that state contention is the limit for parallelism, a transaction with 30M gas limit can be broken into 2 ~15M gas-limit transactions that have storage/account read/write behavior that requires sequential composability. Only reducing the block gas limit or adding some additional state contention validity rules (like Solana does) would help with that.

Re: quadratic attacks: clearly the present 30M transaction gas limit does not pose a DoS threat to the L1 from quadratic attacks. I am not suggesting to increase the transaction gas limit beyond its present value. EIP-7825 is a good idea and is necessary. I am arguing that the ~16.8M limit is too low from an ecosystem perspective ***AND MOST IMPORTANTLY*** setting the limit below 30M is a breaking change, which is a major sin and should be avoided.

---

Now speaking specifically about the challenges that the ~16.8M have on my corner of the ecosystem: to put it simply, it causes an exponential increase in the complexity of the problem of exchange of tokenized value. And I do mean *literally exponential*. I represent [0x](https://0x.org), a leading EVM DEX aggregation platform. We recently ported our DEX aggregation technology to Solana. Solana prioritizes throughput and parallelism over developer experience. The problem of DEX aggregation in an ecosystem that constrains state contention is NP-hard. This increase in complexity makes it more difficult for new entrants to the ecosystem to operate searcher/solver/aggregator stacks (which all require the ability to efficiently solve value flow/exchange problems). Additionally, the desire/requirement for “big” transactions that contend for more state than is allowed in-protocol causes developers to seek out-of-protocol solutions. This causes more flow through private mempools/builders (Jito) to achieve multi-transaction atomicity, compromising decentralization. Tying this back directly to the present EIP: on L2s where gas is cheap, 0x’s APIs routinely return transactions that exceed the proposed cap. This will cause users (or 0x API) to seek multi-transaction atomicity through Ethereum block builder networks or the adoption of more complex, costly routing/MEV technology. If gas throughput is the primary desire, to the detriment of decentralization, then Ethereum would not offer enough differentiated value compared to other L1s. Solana would be the superior choice.

Additionally, a ~16.8M transaction gas limit makes it difficult to deploy “big” contracts. 0x’s router contracts are quite large, pushing the 24KiB Spurious Dragon limit. Deploying a full complement of router contracts *already* exceeds the proposed limit. See transaction `0xadc4e06a7a4c9442c14d1cf90c384d175e7e39f49f713924461c368253cb2697`. Of course, this can be broken up into multiple transactions, with attendant increase in orchestration complexity, but now you’re giving up on atomicity. But more importantly, if we were to adopt an enhanced version of EIP-7907, it would constrain deployed contract bytecode sizes. Monad L1 testnet has already demonstrated that very large contracts (128Kib) are possible/practical, and this limit curtails that kind of innovation/enhancement.

---

**TL;DR:** a ~16.8M gas limit is a breaking change, which should be avoided as to not squander developer goodwill, create a reputation for Ethereum as an unstable platform upon which to build, and to avoid breaking existing dApps. This EIP has second-order ecosystem-wide impacts on application competition that are not fully explored in the discourse around this EIP. We already have examples of broken dApps and degraded developer experience, which should on its own be sufficient reason not to adopt this change. But on top of that, we do not know what we do not know about ecosystem impact.

***This EIP should not be adopted as is.***

---

**Nerolation** (2025-07-31):

You don’t require sequential execution because Ethereum might adopt full parallelism in the future. EIP-7928, for example, is a candidate for Glamsterdam. With such changes, worst-case blocks would just be the least parallelizable ones  (those with few big transactions).

Quadratic attacks are already a concern today: think `modexp`, large contract code sizes, or the point evaluation precompile, just to name some recent examples that caused problems. These and other constraints have blocked Ethereum from raising the gas limit. Often, it’s the behavior of a tiny fraction of users, like 0.0001%, that prevents scaling for the remaining 99.9%. Transactions over 16.8M gas are typically XEN, ENS batch buys, or spam attacks (= address poisoning attacks) and similar.

While contracts like XEN have long been a scaling pain, a per-tx gas limit directly helps mitigate these issues. It’s not perfect, but it’s a meaningful step. And like many changes, just like te modexp repricing too, it’s a trade-off. It’s not backward-compatible, but necessary if we take L1 scaling seriously.

On contract code: with 5M gas, you can already deploy a 24 KiB contract. So even with a 16M gas limit, you’re not currently able to make use of all of it. There’s ongoing discussion about increasing the code size limit, but this introduces concerns about cache bloat. Some form of code chunking may be required before lifting the 24 KiB cap.

---

**vbuterin** (2025-07-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/duncancmt/48/15676_2.png) duncancmt:

> Assuming that state contention is the limit for parallelism, a transaction with 30M gas limit can be broken into 2 ~15M gas-limit transactions that have storage/account read/write behavior that requires sequential composability. Only reducing the block gas limit or adding some additional state contention validity rules (like Solana does) would help with that.

The way ZK-EVMs generally work today is that they chunk at the transaction boundary: a monolithic prover proves each transaction (or, if they are small, batch of transactions), and then you aggregate those proofs into a single proof. And so within this architecture, the size of a transaction determines the degree to which you can parallelize. The theoretical minimum latency bound on SNARK-proving a block is something like: `tx_gas_limit + recursion_cost * log(number_of_txs)`. And so if we want safe shorter slot times, pushing down the max tx gas limit cap is one of the key variables for doing that.

Distributed proving also adds pressure to decrease the max tx gas limit because the whole point is that you have a prover that’s very large in aggregate but where each individual piece is smaller, and so single very large transactions are precisely the case where it would break.

I have suggested multiple times to ZK-EVM developers to chunk at the EVM step boundary instead of the transaction boundary to be able to better process multiple transactions. As far as I know almost all of them have not done it. The reason why is that it is *much* more complex to chunk within a transaction: you have to carry over all kinds of internal state (callstack, memory, refunds, TSTORE…) from one proof to the other. There’s massive dev effort and room for bugs there.

The way that this EIP can improve *execution* parallelism is in combination with block-level access lists, particularly the version where you require the post-state of each transaction to be included. Any node verifying such a block becomes able to run all transactions in parallel, even if they have cross-dependencies, and verify that each intermediate access list is correct in parallel.

The reason why this EIP improves worst-cases around quadratic execution bugs, is that (I’m pretty sure without exception) all of the quadratic execution bugs we have seen involve interactions within a transaction (eg. depth-N call stack followed by N transactions) and not between transactions. Between transactions there is no shared state (except the Ethereum state itself), and so much less surface area for quadratic execution bugs.

> AND MOST IMPORTANTLY setting the limit below 30M is a breaking change, which is a major sin and should be avoided.

**I really hope that we do not adopt “breaking changes are a major sin and should be avoided” as our philosophy. “Breaking changes should be done very carefully, the carefulness in proportion to how many things they break” is better**. If we treat breaking changes as a sin, then we end up suffering an eternal ongoing penalty for the sake of avoiding a one-time pain, and the amount of backwards-compatibility cruft that we suffer will keep stacking up over time.

We have made breaking changes before, with very positive results. The most famous one was  increasing the gas costs of storage IO opcodes in order to improve DoS resistance. The first few rounds of this (40 → 200 → 700) were security-critical. The [last round of this](https://eips.ethereum.org/EIPS/eip-2929) was arguably not security-critical, we could have arguably survived SLOAD at 700, but:

1. It was ok at lower gas limits but it would have made gaslimit increases to the level we see today unsafe.
2. It would have made statelessness unviable.

An even stronger example was the [SELFDESTRUCT nerf](https://hackmd.io/@vbuterin/selfdestruct) (recently, [SELFDESTRUCT became only usable to destroy a contract created within the same transaction](https://eips.ethereum.org/EIPS/eip-6780)). The goal of the SELFDESTRUCT nerf was to establish a new invariant: there is a hard O(1) bound on how many state changes can happen within a single transaction. This in turn made client development significantly easier, because clients would be able to have a simple one-layer caching mechanism for the state, instead of a complicated structure that could handle giant contracts being SELFDESTRUCTED, then that operation being reverted, then calls going into that contract, etc.

These changes were good for Ethereum. As a general principle, **having more hardline invariants that bound what can happen within a transaction, or a block, is a very good thing in hard-to-predict ways**. It makes future client optimizations possible. It makes client code simpler, which increases safety, improves client diversity and reduces development costs for teams. It prevents classes of safety issues that we did not know existed.

A key goal that many people have expressed for this year is scaling the L1. But scaling the L1 is risky, to safety and decentralization. One very good strategy for meeting both goals at the same time is to increase the L1 gaslimit and at the same time establish more and stronger invariants that cut off problematic worst-case scenarios.

I expect that the amount of disruption that proposals like (i) multidimensional gas, (ii) per-code-chunk witness pricing, (iii) serious gas repricings for ZK-EVM safety will be greater than that caused by reducing the tx gas limit, and so we need to be prepared for some applications that are unusually resource-intensive along some margin to need to rewrite parts of their logic regardless.

In fact, I would argue that as the ecosystem matures, the cost of making any breaking change rises every year, and so by constraining the per-tx load *now*, we would actually *reduce* total pain, because we get more leeway to do these future repricings (which will happen at a time when the ecosystem is even more mature and entrenched) through increasing limits rather than decreasing them.


*(8 more replies not shown)*
