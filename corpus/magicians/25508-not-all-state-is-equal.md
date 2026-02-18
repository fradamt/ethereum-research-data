---
source: magicians
topic_id: 25508
title: Not All State is Equal
author: weiihann
date: "2025-09-18"
category: Uncategorized
tags: [stateless, state-expiry, stateless-clients]
url: https://ethereum-magicians.org/t/not-all-state-is-equal/25508
views: 634
likes: 11
posts_count: 3
---

# Not All State is Equal

# Not All State is Equal

Ethereum’s state is uneven: a few contracts hold most storage, while most accounts are short-lived—sometimes only a single block. Studying state access patterns shows what stays hot and what goes cold. If we optimize for real-world usage, we can make the execution layer go faster.

## Analysis

This study analyzes state usage by account type, bytecode usage, deployer and factory patterns, code size, and slot activity. It covers **all blocks** from **genesis** through the **pre-Pectra block 22,431,083** (May 2025).

### EOAs vs. Contracts — which one stays active longer?

> Activity span = block distance from first to last access (reads and writes) of a particular state.
> 0 activity span = a state was accessed only in a single block.

> Assume 1 block = 12s.

|  | Contracts | EOAs |
| --- | --- | --- |
| Total accounts | 50,119,846 | 243,161,178 |
| Median activity span (blocks) | 0 | 22,317 (~3.1 days) |
| P75 activity span (blocks) | 966,579 (~4.5 months) | 1,274,601  (~5.8 months) |
| P95 activity span (blocks) | 4,857,691 (~1.85 years) | 6,800,324 (~2.59 years) |
| Zero activity span share | 55.17% | 4.50% |

![](https://notes.ethereum.org/_uploads/Hy6fkHdoll.png)

*Figure 1: Over half of contracts never see activity, while majority of the active contracts last less than one year.*

![](https://notes.ethereum.org/_uploads/Bk6VySuoex.png)

*Figure 2: Most EOAs are active for under a year, with a minority persisting multiple years.*

1. EOAs clearly outlast contracts.
EOAs have a non-zero median span (~3.1 days), while the median contract span is zero. The right tail for EOAs is heavier at every quantile (q75, q95), indicating a larger long-lived cohort.
2. Most contracts are ephemeral by design or intent.
About 55% of contracts are zero-span. Likely drivers include:

Factory spam & mass-mint templates (e.g., token clones, pair contracts that never see follow-ups).
3. MEV / utility deployments that are created for a single transaction.
4. Self-destruct patterns (especially pre-EIP-6780), where creation and destruction happen within the same block/tx.
5. “Short-lived EOAs” are common too.
The median EOA is active for only ~3.1 days from first to last observation, and 75% end within ~6 months. This could include one-off claimers/minters, exchange deposit addresses and bot wallets.
6. Long-lived contracts exist—but are atypical.
Contracts with multi-year spans tend to be standards-driven or infrastructural: token contracts (ERC-20/721), registries, routers, multisig/proxy admin contracts, and other core primitives. Many application teams rotate addresses on upgrades, which fragments activity across newer deployments and shortens the measured span at each address.

### How diverse are the contracts?

1 contract ≠ 1 unique application. In fact, many of the contracts reuse existing bytecodes or are deployed using the same template (with factories). We can analyze the contracts based on different categories:

- Template vs. Unique Bytecodes
- By Deployer Address
- By Factory Address
- By Code Size
- Stateful (With slots) vs. Stateless (Without slots)

#### Template vs. Unique Bytecodes

> Template = Bytecode hash deployed by more than one contract address.
> Unique = Bytecode hash deployed exactly once.

|  | Bytecode Count | Contract Count | Avg. Median Activity Span (blocks) |
| --- | --- | --- | --- |
| Template | 150,587 | 48,663,814 | 468,852 (~2.1 months) |
| Unique | 1,456,032 | 1,456,032 | 905,439 (~4.1 months) |
| Total | 1,606,619 | 50,119,846 |  |

![](https://notes.ethereum.org/_uploads/S10mmE2cgg.png)

*Figure 3: The majority of bytecodes are unique.*

![](https://notes.ethereum.org/_uploads/SJxIem4n5el.png)

*Figure 4: Nearly all contracts are deployed from template bytecodes, with unique ones forming only a small share.*

![](https://notes.ethereum.org/_uploads/r1pqXN2cxe.png)

*Figure 5: 50% of template bytecodes are used by at most 2 contracts, while 99% are used by at most 728 contracts.*

![](https://hackmd.io/_uploads/SJdamI49lg.png)

*Figure 6 (Lorenz Curve): Contract deployments are extremely concentrated, with a Gini coefficient near 0.99.*

![](https://notes.ethereum.org/_uploads/SkHzXNhcge.png)

*Figure 7: Unique contracts hold about two-thirds of all storage slots despite being a small share of deployments.*

What the data shows:

- Extreme contract concentration: ~150k template bytecodes account for 97% of all contracts. The top 1 code hash alone covers 14.4% of contracts; top 10 cover 51%; top 100 cover 81.8%. This is heavy long-tail template reuse rather than a wide diversity of implementations.
- Slots are not where the clones are: Despite being only 2.9% of contracts, unique bytecodes hold ~875.2M storage slots vs ~429.1M for templates—~67% of state resides in one-off implementations.

The median activity span for unique contracts (~4.1 months) is **almost 2×** that of templates (~2.1 months). This aligns with intuition: many templates are minimal proxies/clones, token factories, or ephemeral deployments (spam/memecoins, MEV scaffolding, pre-EIP-6780 self-destruct patterns) that are short-lived or never used beyond creation.

Unique contracts being more state-heavy likely reflects complex systems (DEXs, staking, bridges, rollup infrastructure) that manage larger, persistent data. On the flipside, the huge template share of contracts explains the long tail of zero-activity-span deployments seen – many clones never meaningfully execute after creation.

#### By Deployer Address

> Single = Deployer which only deploys one contract.
> Multiple = Deployer which deploys more than one contract.

|  | Deployer Count | Total Contracts | Avg. Slots per Contract | Avg. Median Activity Span (blocks) |
| --- | --- | --- | --- | --- |
| Single | 4,793,357 | 4,793,357 | 30.65 | 197,134 (~0.9 months) |
| Multiple | 850,064 | 45,326,489 | 193.28 | 687,037 (~3.1 months) |
| Total | 5,643,421 | 50,119,846 |  |  |

![](https://notes.ethereum.org/_uploads/SyyNIE39gx.png)

*Figure 8: Most deployers only create one contract, while a minority deploy many.*

![](https://notes.ethereum.org/_uploads/ryHNIVn5ee.png)

*Figure 9: A small group of high-volume deployers account for over 90% of all contracts.*

![](https://hackmd.io/_uploads/BkDlFuNqle.png)

*Figure 10: 50% of the deployers deploy only 1 contract, while 99% deploys at most 14 contracts.*

![](https://hackmd.io/_uploads/rJneK_Vcxl.png)

*Figure 11 (Lorenz Curve): Contract creation is highly concentrated, with a Gini coefficient of 0.884 showing most contracts come from a small minority of deployers.*

What the data shows:

- A small cohort does almost all the deploying — The top 500 deployers alone are responsible for 57.4% of all contracts; the single largest deployer accounts for 3.15%.
- Active deployers produce more long-lasting, slots-heavier contracts on average. Contracts from “multiple” deployers live ~3.5× longer (687k vs 197k blocks) and use ~6× more slots per contract (193 vs 31 slots). This pattern fits teams/services that maintain products on-chain (and they are successful), versus one-off experiments.
- But the very top volume deployers skew ephemeral. Among the top-10 by volume, contracts have extremely short activity spans (hundreds of blocks on average) and minimal storage—consistent with mass-produced clones, factory spam, and MEV scaffolding. In other words: within the “multiple” group, there’s a split between builders (durable, stateful deployments) and sprayers (high-volume, short-lived deployments).

Contract deployments are highly concentrated. Most durable, state-heavy contracts come from repeat deployers, while the highest-volume deployers flood the chain with short-lived ones.

For the multiple contracts deployers, it could also be that they made a mistake, so they had to redeploy the contracts.

#### By Factory Address

> Non-Factory = Created directly by an EOA (no intermediary contract).
> Factory – Individual = Created by a contract which produced exactly one child.
> Factory – Multi = Created by a contract that produced more than one child.

|  | Count | Total Contracts | Avg. Slots per Contract | Avg. Median Activity Span (blocks) |
| --- | --- | --- | --- | --- |
| Non-Factory | 808,188 | 5,470,844 | 313.14 | 768,567 (~3.6 months) |
| Individual | 66,900 | 66,900 | 196.58 | 431,153 (~2 months) |
| Multi | 32,929 | 44,582,102 | 177.58 | 510,060 (~2.36 months) |
| Total | 908,017 | 50,119,846 |  |  |

![](https://notes.ethereum.org/_uploads/S1gYL8E29ge.png)

*Figure 12: The vast majority of addresses are non-factories, with only a small share creating multiple contracts.*

![](https://notes.ethereum.org/_uploads/H1aIIEhqgl.png)

*Figure 13: Nearly 90% of contracts are deployed by multi-contract factories, while direct non-factory deployments form just ~11%.*

![](https://hackmd.io/_uploads/SySRZ8V5gl.png)

*Figure 14: 50% of the factories deploy at most 5 contracts and 99% of the factories deploy at most 4978 contracts.*

![](https://hackmd.io/_uploads/SJefMUNqex.png)

*Figure 15 (Lorenz Curve): Deployment is extremely unequal across factories, with a Gini coefficient of 0.993.*

What the data shows:

- Most contracts are factory-minted clones. ~89.1% of all contracts come from multi-contract factories (32,929 addresses), while only 10.9% are deployed without factories. Yet non-factory contracts are, on average, heavier (≈313 storage slots/contract) and stay active longer (median activity span ≈ 769k blocks) than factory children (≈178–197 slots/contract; 431–510k-block medians).
- Concentration is extreme. The top 5 factories account for ~43% of all deployments and the top 100 for ~89%. Half of factories deploy ≤5 contracts and 99% deploy ≤4,978 contracts.

**Factories scale cheap, lightweight code.** Lower slots per contract and shorter median activity spans in the *Individual* and *Multi* factory groups are consistent with proxy patterns, token/pair spam, airdrop mints, and MEV/scaffolding contracts—easy to mass-produce, often short-lived, and many never accrue meaningful slots.

**Non-factory deployments skew toward infra.** More storage and longer spans suggest bespoke systems (governance, vaults, routers, bridges, rollup infra) deployed directly by EOAs/multisigs and kept active over time.

**“Individual factory” ≠ durable.** Factories that produced exactly one child show shorter spans and less slots than non-factory deployments. Many look like bootstrap or vanity uses of a factory rather than long-running applications.

#### By Code Size

> Age = Latest block (22431083) - the block where the state was first seen.

| Size Category | Contract Count | Zero Activity Span (%) | Non-Zero Median Activity Span (blocks) | Non-Zero P99 Activity Span (blocks) | Median Age (blocks) |
| --- | --- | --- | --- | --- | --- |
| Tiny (<1KiB) | 44,298,982 | 57.9 | 2,192,443 (~10 months) | 8,958,543 (~3 years) | 6,318,754 (~2.4 years) |
| Small (1-5KiB) | 4,333,667 | 41.4 | 205,882 (~28 days) | 11,690,310 (~4 years) | 11,044,783 (~4.2 years) |
| Medium (5-10KiB) | 592,936 | 23.4 | 58,613 (~8 days) | 11,417,402 (~4 years) | 7,283,986 (~2.8 years) |
| Large (10-20KiB) | 794,012 | 8.6 | 8,302 (~1 day) | 10,871,423 (~4 years) | 5,297,655 (~2 years) |
| Very Large (20-24KiB) | 100,249 | 11.1 | 273,516 (~1 month) | 11,276,444 (~4 years) | 5,973,078 (~2.3 years) |

![](https://hackmd.io/_uploads/Hkeyz_Bcle.png)

*Figure 16: Tiny contracts dominate in number, though most of them never see activity beyond a single block.*

![](https://hackmd.io/_uploads/HJN1z_Sqxx.png)

*Figure 17: Tiny and Very Large contracts tend to persist longer than medium-sized ones.*

What the data shows:

- Tiny dominates, but it’s two different worlds. Tiny contracts account for ~88% of all contracts, but over half are zero-span (57.9%), consistent with mass-minted clones and stubs. Yet among those that do see activity, Tiny has the longest median span of any group (~2.19M blocks ≈ 10 months), revealing a second sub-population of long-lived usage.
- Activity span vs. size is not monotonic—it’s U-shaped. Conditioning on non-zero activity, the median span drops from Tiny → Small → Medium → Large (shortest, ~8.3k blocks ≈ 1 day), then rebounds for Very Large (~273k blocks ≈ 1 month). So “bigger code operate longer” is false as the middle sizes churn the fastest.
- Every size category has a long-lived tail. P99 spans cluster between ~10–11.7M blocks (~3–4 years) across all sizes, meaning a small fraction of contracts in every bucket persist for years.

Tiny contracts are typically packed with proxies and factory clones. Most are cheap, disposable and never used. However, the ones the matter and are actually useful operates much longer, hence the long spans among the non-zero cohort. Another possibility is that they are gateway contracts used for upgrades.

Small/Medium/Large contracts concentrate bespoke, hype-cycle contracts (tokens/NFT mints/farms, one-off app logic). Teams also rotate addresses on upgrades, so activity spans fragment.

Very Large contracts often signal complex systems. They are rarer and more long-lived than mid-sizes but not uniformly successful—some heavy deployments never get adopted.

#### Stateful vs. Stateless Contracts

> Stateful = Contracts with at least 1 storage slot
> Stateless = Contracts with 0 storage slot

| Type | Total Contracts | Zero Lifespan (%) | Median Non-Zero Activity Span (blocks) |
| --- | --- | --- | --- |
| Stateful | 23,127,186 | 50.8 | 105,112 (~14.6 days) |
| Stateless | 26,992,660 | 58.91 | 3,185,332 (~1.2 years) |

![](https://notes.ethereum.org/_uploads/HJ9DTVnqll.png)

*Figure 18: A slight majority of contracts are stateless, while stateful ones make up ~46%.*

![](https://hackmd.io/_uploads/SkEvo3Sqll.png)

*Figure 19: Stateless contracts tend to persist much longer than stateful ones when they are active.*

What the data shows:

- Most contracts are stateless. 53.9% never touch storage; 46.1% do.
- Zero-activity is more common for stateless contracts. 58.9% vs. 50.8% for stateful.
- Stateless contracts operate longer. Their median non-zero span is ~30× longer than stateful (1.2 years vs. 14.6 days).

Why this likely happens

- Stateless = cheap and durable utilities. Many are simple forwarders, proxies, or helpers. They are easy to deploy in bulk (so many end up with zero span), but the useful ones can run for years because they don’t hold data and never need migrations.
- Stateful = upgraded or replaced. Tokens, pools, vaults, and apps that store data are more likely to be upgraded or swapped for newer versions. That splits activity across new addresses and shortens the span at each old address.

### How actively used are storage slots?

![](https://hackmd.io/_uploads/rypm9YS5gl.png)

*Figure 20: Most storage slots are written once and never used again, with over 60% falling into zero activity span.*

![](https://hackmd.io/_uploads/r1FsHjB5le.png)

*Figure 21 (Lorenz Curve): Storage usage is extremely skewed, with a Gini coefficient of 0.973.*

What the data shows:

- More than half of the storage slots are ephemeral (63.3%). These slots never get accessed after setting.
- Concentration is extreme. A single contract holds ~6% of the total slots (see XEN Crypto); the top 1000 contracts hold ~51% of all slots.

Zero-activity slots are common for one-time flags, airdrop claims, initialization records, abandoned balance, or data in contracts that were quickly replaced.

A small set of large systems carry most of Ethereum’s live storage slots. That’s why a tiny fraction of contracts dominate total slots.

One caveat is that proxy patterns usually split logic and storage. The logic contract often appears stateless and long-lived, while the storage contract holds state and may be rotated. Looking only at addresses (not projects) will show shorter spans for stateful proxies.

Some slots labeled “zero activity” may still be read off-chain (via RPC calls). Those reads don’t appear on-chain.

## Open Ideas

### State Expiry

Most state goes cold quickly. A pragmatic direction is **periodic pruning of inactive state** with a **resurrection scheme**:

- Window: A 12–18 month activity window fits the distribution: the median non-zero spans for many state land well under a year, while long-lived state are above it.
- Benefits: Keeps hot state small, slow down state growth, reduces disk I/O, reduces storage size and improves block processing time

As a starter, let’s consider how much storage space we can save by **removing zero activity span accounts and storage slots**. We measured this on Geth’s flat snapshot (key-value “state” table), comparing the original snapshot to one where those keys are removed (the node was synced to block 22,431,083):

|  | Original Size (GiB) | Zero Activity Span Size (GiB) | After Deletion (GiB) | Savings |
| --- | --- | --- | --- | --- |
| Accounts | 13.48 | 2.58 | 10.90 | 19.14% |
| Slots | 94.12 | 57.62 | 36.50 | 61.22% |
| Total | 107.60 | 60.20 | 47.40 | 55.95% |

On the snapshot alone, removing zero-span state would **cut storage space by ~56%**—a strong signal that state expiry could materially shrink the hot state set.

### Cheaper deployment for bytecodes that already exist

Duplicate code wastes gas on deployment even though clients typically deduplicate bytecode on disk by code hash. A few workable variants:

1. Local duplicate discount (same block/epoch): If bytecode codehash appears twice in the same block (or short epoch), the second deployment pays a reduced code-deposit.

Pros

Can be easily verified in a block based on the orderings of contract deployments
2. Immediate gas cost savings for factories, and AA wallets
3. Limits spam impact since the discount only applies in-block
4. Cons

Unfairness: who should pay the full amount?
5. Complexity on EL clients implementation
6. Global “codehash registry”: A system contract storing mappings of codehash → exists in its storage. All contract deployments first check if bytecode already exists.

Pros:

Gas savings for AA wallets, proxies, and factory contracts.
7. Possible mechanism of delegating to a contract if bytecode already exists
8. Cons:

Incentivizes spammy clones
9. Adds DoS surface to the registry–needs careful pricing so the discount doesn’t get abused by spammers
10. Bytecode hashes may become a problem for state growth as the storage trie size grows
11. ZKEVMs have to prove the existence of the code hashes
12. Single contract per library: Instead of having duplicates for the same library, add a new opcode LIBCREATE which deploys a “library contract” where only the code hash is used. This might be useful to deduplicate libraries, but only if further analysis shows that these libraries are indeed taking up a huge share of the contracts.

### Progressive per-address storage pricing

Today, a handful of contracts dominate global storage. We might want prices that reflect *marginal* burden.

**Progressive per-address storage pricing**: Base `SSTORE` cost plus a **tiered surcharge** as the `slot_count(address)` crosses thresholds (requires an in-protocol slot counter, as in EIP-2027-style metadata). Keeps costs predictable (tiers), yet nudges very large contracts to internalize state externalization costs.

**Pros:**

- Ties cost to actual storage growth at an address.
- Tiers make costs easier to plan than per-slot repricing.
- Encourages better storage design where “unlimited slots” is not abused.

**Cons:**

- Needs slot-count metadata and rules; adds complexity.
- Harder gas estimation when a tx crosses a tier mid-tx.
- May push devs to split state across many contracts (more calls, more surface, worse UX).
- Useful contracts tend to have many slots, and we are punishing them for being active

### Temporary Storage Model

Many slots are written once and never touched again. Give developers a cheaper, contract-readable place for short-lived data that can be dropped deterministically.

How it works (high level):

- Per-account temporary storage root: add tempStorageRoot to each contract account for temporary data
- Global period buckets: all writes go into the current period (e.g. 6-12 months)
- Deterministic expiry: once a period is over, its data is logically zero for reads, whether or not it’s been physically pruned by EL clients
- Pricing: Make current SSTORE more expensive and storing data in the temporary storage cheaper than SSTORE

**Pros:**

- Aligns cost to intended lifetime
- Simple mental model: “use temporary storage for data you’re okay to lose after ~N months”
- Orthogonal to (and compatible with) future state-expiry work

**Cons:**

- Accounts migration are required due to new account field
- Tooling risks if developers rely on values past storage reset
- Gas schedule needs careful tuning to avoid abuse
- SSTORE in deployed contracts has a higher gas cost, may be unfair

### Performance Improvements for EL clients

Some ideas on how EL clients may utilize these information to improve their performances:

- Hot/cold state segregation in storage engines: Keep recently touched accounts/slots in “hot” storage engine, then batch-compact and snapshot the cold ones less frequently to reduce write amplification.
- Slot-count–driven commits: Prioritize database commits for trie paths of mega-contracts that hold outsized shares of slots. This targets the worst offenders first.
- Cache frequently seen code hashes and check for existence: For contract creations, skip re-persisting duplicate bytecode, reducing write amplification and compaction pressure.

## Closing

Ethereum’s problem isn’t just state growth—there isn’t a way to handle stale state.

Most accounts are short-lived. Factories and template clones dominate deployments, but unique contracts hold most storage. A small set of contracts owns the large bulk of slots, and many slots are written once and never touched again. If we can find breakthroughs in tackling these problems without breaking composability, Ethereum can scale faster.

Not all state is equal—perhaps the protocol shouldn’t treat it as if it were.

## Acknowledgements

Special thanks to the ethPandaOps team for their amazing [Xatu](https://github.com/ethpandaops/xatu) infrastructure.

Also thanks to Guillaume, Carlos, Matan and Ignacio for reviewing this article.

## Next Steps

- Intensity analysis: Pair span with activity intensity to distinguish “quiet long-lived” from “short but intense” state. Gas spent should also be considered.
- Group by labels: Analysis with labels (e.g. tokens, routers, vaults, bridges, factories, proxies) to further solidify the reasonings.
- Post EIP-6780 self destructs: Investigate how many contracts were supposed to self-destruct and removed from the state trie but couldn’t because of EIP6780.
- Empty balance contracts: Check how many contracts are created, HODL for years, and then are emptied. If they aren’t going to be used, perhaps we could delete them and nobody cares.
- Libraries: Check how many of the contracts are deployed using libraries.
- Distribution of factory/non-factory contracts according to unique/template division.
- Identify clusters based on different attributes (e.g. deployers, factories, code hash, categories) and how much storage space they represent in the EL clients.

## Appendix

[Link](https://github.com/weiihann/ethereum-state-analysis) to the analysis code repository.

## Replies

**misilva73** (2025-09-22):

Brilliant analysis, [@weiihann](/u/weiihann)!

The temporary storage model is an interesting design. Maybe to understand its impact, I am wondering if we could gather some info on RPC reads of “zero activity” slots. As you pointed out, even they are touched on-chain, there could still be users accessing them through RPC calls. This type of use-cases would not be able to leverage the temporary storage model, right?

---

**weiihann** (2025-09-22):

I think it’s practically impossible to obtain the data for offchain reads, even if we work with the RPC providers to get those data. For example, I could run an RPC node myself and read the state that I want.

Regarding the temporary storage model, it depends on what it’s used for. For example, if I want some data to be persisted onchain forever, then use permanent storage. If there’s some data that I’d like to persist for let’s say maximum 6 months or 1 year and I do not care that it’s gone after that, then use the temporary storage.

Regarding why people would use temporary storage, the obvious incentive is that it’d be cheaper. But whether people would actually use it (i.e. if there’s some data that can be stored temporarily onchain and not permanent), we have to do more investigations.

