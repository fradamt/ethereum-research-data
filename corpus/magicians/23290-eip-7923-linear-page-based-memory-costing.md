---
source: magicians
topic_id: 23290
title: "EIP-7923: Linear, Page-Based Memory Costing"
author: charles-cooper
date: "2025-03-27"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7923-linear-page-based-memory-costing/23290
views: 599
likes: 18
posts_count: 32
---

# EIP-7923: Linear, Page-Based Memory Costing

discussions-to for: [Add EIP: Linear, Page-Based Memory Costing by charles-cooper · Pull Request #9556 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9556/files)

adding the EIP link, now that it has been merged: [EIP-7923: Linear, Page-Based Memory Costing](https://eips.ethereum.org/EIPS/eip-7923)

## Replies

**sbacha** (2025-03-28):

Isn’t this advocating for removing the 63/64 rule?

---

**charles-cooper** (2025-03-28):

Bit off topic, but yes, I think that should be removed as well.

---

**charles-cooper** (2025-03-28):

Since memory access gets substantially more expensive after around 32MB, I considered several variants:

1. Thrash costing only, global memory limit is implied by gas limit (currently in the EIP)
2. No thrash costing, limit per message call. This has the disadvantage that the global limit has to be inferred from the call stack limits
3. No thrash costing, global memory limit. This has the disadvantage that the global memory limit may need to be kept small permanently, since CPU cache grows very slowly over time.
4. Thrash costing AND global memory limit. This has the disadvantage that developers may come up with valid use cases for using much more memory and be blocked by EVM limitations, but on the other hand, it can help nodes reason about DoS vectors invariant of gas limit (see EIP-7686: Linear EVM memory limits - #5 by qizhou).

I think all of these fall in the realm of ‘acceptable’ solutions. I personally prefer 1, 4 or 3, in that order.

---

**jhb10c** (2025-03-28):

63/64 rule is still necessary if for page-based memory since this does not limit the memory of child calls. Is there an alternative mechanism that should be done. Limiting maximum memory size on a transactions level based on gas limit?

---

**charles-cooper** (2025-04-04):

I think one of the motivations for this EIP actually is that the memory limit is invariant wrt the state of the call stack, so you don’t need to think about how allocation patterns across the call stack can affect memory usage. In this EIP, there is an implied limit of memory usage based on the gas limit, which in the current iteration of the draft, would be `gas_limit * 4096 / 109`, where `4096` is the number of bytes per page, and `109` is the cost to allocate a page.

---

**charles-cooper** (2025-04-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/charles-cooper/48/1308_2.png) charles-cooper:

> Thrash costing AND global memory limit. This has the disadvantage that developers may come up with valid use cases for using much more memory and be blocked by EVM limitations, but on the other hand, it can help nodes reason about DoS vectors invariant of gas limit (see EIP-7686: Linear EVM memory limits - #5 by qizhou).

I’ve added this transaction global limit in the latest commit: [Add EIP: Linear, Page-Based Memory Costing by charles-cooper · Pull Request #9556 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9556/commits/a124e275a9430fd108ba1356ff5c7ebc97461b1c)

---

**benaadams** (2025-04-11):

Do you benchmarks also include clearing costs; as memory will have to be zeroed to not leak data between transactions

---

**charles-cooper** (2025-04-11):

Yes – that’s included in the 100 gas cost to allocate+zero a page.

---

**gcolvin** (2025-08-13):

I’ll happily support this over the current model.

Nonetheless, I think the page-based model and thrash-charging are overkill, which leave things difficult to reason about for no actual benefit.  I would like to see more empirical evidence that they are necessary and that they work –  I’d rather not have to maintain an LRU in the client, which may or may not match the hardware well enough to help.  L3 caches are getting so large and pre-fetch algorithms so good that I’d actually be surprised to see much thrashing by programs using 64MB, even if code was malicious.

So I would be happier with the much simpler model of just charging for how much memory an allocation uses beyond the current “high water mark.”  Unix (brk and sbrk) imposed that limitation on memory  allocators for a long time, and it mitigates against attacks that touch randomly scattered memory.

---

**frangio** (2025-08-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> just charging for how much memory an allocation uses beyond the current “high water mark.”

Isn’t this what the EVM currently does?

---

**gcolvin** (2025-08-31):

Yes, it does charge by change in high water mark, but with a ridiculously complicated formula.

---

**gcolvin** (2025-09-26):

I’ve studied this some more, and my thinking hasn’t changed much.  I would support it over the current model, but would prefer something simpler.

In the EIP you report these (among other) times on an unknown, but fairly old CPU:

- Time to randomly read a byte from a 2MB range: 1.8ns
- Time to randomly read a byte from a 32MB range: 7ns
- Time to randomly read a byte from a 4GB range: 40ns

There is a big gap around  32MB, so we really need to have timings for the wider range of CPUs that will be running on the network in order to judge the minimum cache size to avoid thrashing.  *I propose to set the maximum allocation below the minimum thrashing range.*

If we really want to charge warm reads less than cold reads then LRU eviction from the set of warm reads is a DoS surface.  Me and Nick Johnson went over this years ago and decided the best policy was random eviction, which couldn’t be DoSed.  But with the maximum allocation set to avoid thrashing all pages will be in cache.  *I propose to charge the same for warm and cold page access.*

---

**Ankita.eth** (2025-09-30):

This EIP feels like a strong step forward compared to the current quadratic memory model. Moving to a linear, page-based costing makes gas usage:

- More predictable for developers
- Closer to real hardware behavior
- Easier for compilers to optimize memory without sudden cost spikes

A few thoughts/suggestions:

- Keeping MSIZE unchanged is good for backward compatibility, but maybe consider a new opcode for “actual allocated pages” to help newer compilers.
- The THRASH_PAGE_COST idea is interesting — more benchmarks on worst-case thrashing (e.g., >512 pages) would be useful to see stability under stress.
- The 64MB memory cap makes sense for DoS protection, but it might be better as a configurable parameter for future flexibility.

Overall, this proposal improves predictability, developer experience, and scalability while keeping safety in mind. I’m supportive of this direction.

---

**charles-cooper** (2025-10-09):

Why is LRU eviction a DOS surface?

---

**gcolvin** (2025-10-24):

If you have a cache with predictable behavior you can attack the behavior.  In this case I think you could hit the chain with series of transactions that cause the LRU item to actually be a very bad choice.

---

**yoavw** (2025-10-27):

This EIP seems to have an issue similar to what I described in [EIP-7971: Hard limit and cost reduction for transient storage allocation - #2 by yoavw](https://ethereum-magicians.org/t/eip-7971-hard-limit-and-cost-reduction-for-transient-storage-allocation/24542/2)

The EIP defines `MAXIMUM_MEMORY_SIZE = 64 * 1024 * 1024 and` says “A transaction-global memory limit is imposed. If the number of pages allocated in a transaction exceeds MAXIMUM_MEMORY_SIZE // PAGE_SIZE (i.e., 16384), an exceptional halt should be raised.”

In transactions that include calls from different users (e.g. EIP-7702 batching relayer, ERC-4337 bundler, intent solver, crosschain bridges), the first call could maliciously allocate `64MB-ε`, and move the solidity memory pointer back to its original position so it cannot be detected by other calls.  This will cause an exceptional halt in other calls.

There’s no GAS-like opcode to check the current memory allocation, and no CALL param to limit the amount of memory a call may use.  Therefore no way for calls to defend themselves.

For any transaction-wide “shared budget”, we need an opcode and a way to limit the resource use per CALL.

Can we avoid this altogether, and just use gas pricing to mitigate DoS instead of introducing new shared budgets?

---

**charles-cooper** (2025-10-28):

I don’t really see the problem. You can also cause downstream calls or subcalls to halt by denying them gas (by using it all up first).

I don’t think gas pricing mitigates DOS, as explained in the EIP. Further, using gas in this way controls two dimensions of DOS prevention – compute and memory – when it should just be used to cost compute. The cost of memory behaves more like a step function, where it does not cost any resources, until you hit OOM, at which point the program crashes. I think crashing due to OOM is a fundamental feature of machines that should be reflected to the user through the VM, and is already a familiar programming model to most programmers.

---

**yoavw** (2025-10-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/charles-cooper/48/1308_2.png) charles-cooper:

> I don’t really see the problem. You can also cause downstream calls or subcalls to halt by denying them gas (by using it all up first).

Gas is indeed a shared budget as well, but EVM provides a way to control the allocation (`*CALL` opcodes let the caller limit the call’s consumption), and a way to check the current call’s budget (the `GAS` opcode).  Protocols like ERC-4337 as well as intents and other interop protocols use this to isolate calls from one another, and also to protect the calls from incorrect execution by the transaction sender (typically a relayer).

Take a look at ERC-4337 for example - see the EntryPoint singleton contract.  Bundlers pick UserOps from the AA mempool and submit them via `EntryPoint.handleOps()`.  EntryPoint ensures that each UserOp gets exactly the gas limit it asked for.  One UserOp’s execution cannot interfere with another’s.  A bundler can’t cause a UserOp execution to revert unexpectedly.  If it doesn’t give a UserOp the requested gas, the entire bundle transaction reverts at the bundler’s expense, and another bundler will pick the UserOps from the mempool and execute them correctly.

If we add another shared budget such as `MAXIMUM_MEMORY_SIZE` and don’t also add a way to control and measure it (a `*CALL` arg and an opcode like `GAS`), the EntryPoint contract won’t be able to prevent one UserOp from interfering with others by exhausting memory.  Furthermore, a UserOp may grief bundlers in the mempool by causing the entire bundle to revert at the bundler’s expense.

Similar situations will occur in intent protocols and in swap protocols that involve an offchain orderbook.  A malicious user may include a token that exhausts the shared budget, causing a complex swap to fail for all the users involved (in the swap case) or for a the intent solver to fail fulfillment at its own expense.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/charles-cooper/48/1308_2.png) charles-cooper:

> I don’t think gas pricing mitigates DOS, as explained in the EIP. Further, using gas in this way controls two dimensions of DOS prevention – compute and memory – when it should just be used to cost compute. The cost of memory behaves more like a step function, where it does not cost any resources, until you hit OOM, at which point the program crashes. I think crashing due to OOM is a fundamental feature of machines that should be reflected to the user through the VM, and is already a familiar programming model to most programmers.

Resource measurement could prevent DoS - if measured correctly, but I agree with you that it requires multiple dimensions. Different EVM chains may even need to reprice different dimensions.  Compute, memory, storage, ZK proving costs (e.g. KECCAK is extremely expensive to prove but gas doesn’t reflect it), blob-space cost, etc.  I’m also familiar with how memory cost behaves, and it gets even more complicated with cache eviction strategies.  OOM is an extreme case, but even transactions that just break memory locality patterns have an adverse effect on performance, especially as we try to improve EVM parallelization.

However, I don’t think we should solve it by introducing shared budgets and hard limits.  They add complexity and introduce DoS vectors against other components, such as the examples above.  The solution is to measure different resources correctly and not try to flatten them to a single `gas` value.  There’s already a proposal for multidimensional gas which would enable that.

I share your desire to make memory cost more linear (the quadratic pricing is an imperfect attempt to solve the same problem).  Your proposal comes from a necessity - we currently have one number and we need to somehow flatten the complexity into it.  But like other proposals that tried to tackle the many-resources-one-number problem, it introduces other issues. We need to bite the bullet and adopt multidimensional gas to solve the root of the problem.

---

**qizhou** (2025-11-06):

For the cost of thrashing, I have completed extensive experiments on a modern machine and different memory sizes.

Machine: AMD 5950x, 16 cores, 32 threads, 128 MB ECC memory

MLOAD Random Access Patterns:

- Random Page Access, i.e., [random_page_idx*4096, random_page_idx*4096+32)
- Random Cross-Page Access, i.e., [random_page_idx*4096+4096-16, random_page_idx+4096+16)
- Random Cross-Page Access (Unaligned), i.e., [random_page_idx*4096+4096-15, random_page_idx+4096+17), which aims to simulate the worst case of MLOAD random access.

The access time (ns/acc) is summarized as follows:

| Memory Size | Random Page Access | Random Cross-Page Access | Random Cross-Page Access (Unaligned) |
| --- | --- | --- | --- |
| 2.5MB | 3.58ns/acc | 3.78ns/acc | 5.41ns/acc |
| 256MB | 4.73ns/acc | 5.49ns/acc | 7.13ns/acc |
| 4GB | 5.49ns/acc | 7.53ns/acc | 9.07ns/acc |

Note that:

- All experiments pin the process to a single core to stabilize the results
- For 256MB and 4GB, the dTLB cache miss rate is >95% (via perf stat -e dTLB-loads,dTLB-load-misses), while for 2.5MB, the dTLB cache miss rate is ~0%
- Page fault cost is ~500ns/fault
- Script to reproduce: research/evm/tlb_thrash_evm.sh at main · qizhou/research · GitHub

---

**gcolvin** (2025-11-06):

In the EIP Charles reports these numbers on an older machine:

- Time to randomly read a byte from a 2MB range: 1.8ns
- Time to randomly read a byte from a 32MB range: 7ns
- Time to randomly read a byte from a 4GB range: 40ns

I put all of it in charts below.  Plotted on a linear graph it seems there is maybe a thrash point somewhere below 32 MB.  But plotted on a log-log graph they are all straight-line power laws with no obvious knee.  It would be worth running the experiments with more data points to better explore the smaller memory sizes.  I suspect we may be looking at the effects of on-chip caching – at 4GB the newer machine isn’t thrashing main memory at all. Instead we might be seeing a smoother increase in timings as data falls from L1 to L3 cache.  Or, given that an AMD 5950x has only 64MB of L3 per core, it is hitting main mem, but the caching is doing a good job.

[![image](https://ethereum-magicians.org/uploads/default/optimized/3X/8/9/896016b64ad14cc16e2b7d313dd855becc2039f1_2_532x500.png)image1610×1512 65.4 KB](https://ethereum-magicians.org/uploads/default/896016b64ad14cc16e2b7d313dd855becc2039f1)

[![image](https://ethereum-magicians.org/uploads/default/optimized/3X/d/4/d484ad8ca601677e973410132c4038407a2d3ab7_2_532x500.png)image1610×1512 54.7 KB](https://ethereum-magicians.org/uploads/default/d484ad8ca601677e973410132c4038407a2d3ab7)


*(11 more replies not shown)*
