---
source: ethresearch
topic_id: 23396
title: "The Future of State, Part 2: Beyond The Myth of Partial Statefulness & The Reality Of ZKEVMs"
author: CPerezz
date: "2025-11-03"
category: Execution Layer Research
tags: [stateless]
url: https://ethresear.ch/t/the-future-of-state-part-2-beyond-the-myth-of-partial-statefulness-the-reality-of-zkevms/23396
views: 603
likes: 12
posts_count: 6
---

# The Future of State, Part 2: Beyond The Myth of Partial Statefulness & The Reality Of ZKEVMs

# The Myth of Partial Statefulness: Why Ethereum’s Future May Force a Binary Choice

> We strongly recommend reading first the Part 1 of this series of articles. Even if a new type of client is not really interesting for you in particular, it will set the basis that showcase a lot of the problems tackled in this post.

Thanks to [@weiihann](/u/weiihann)  and [@gballet](/u/gballet)  for their feedback and endless reviews.

> We advise to readers that part 4.3.X can be skipped. But it showcases a bunch of issues and examples that are important to understand why Partial Statefulness & RPC-serving on this way might not be as good as it sounds.

## 1. Introduction — The Illusion of Middle Ground

Ethereum’s roadmap toward statelessness and ZK-based validation has inspired the idea of a [“partially stateful”](https://ethresear.ch/t/a-local-node-favoring-delta-to-the-scaling-roadmap/22368#p-54385-a-new-type-of-node-_partially-stateless-nodes_-4) node: one that stores and serves only a fraction of the global state while still contributing meaningfully to verification and data availability.

At first glance, this model promises a practical middle ground between the burden of full nodes and the fragility of fully stateless clients. Yet on closer inspection, the middle ground is largely illusory. Once state expiry and validity proofs dominate, the notion of sustainable partial statefulness collapses under the weight of execution semantics, data dependencies, and economic incentives.

The consequences extend far beyond performance. Ethereum’s security model relies on universal re-execution — the ability of any node to deterministically recompute state transitions. Once that ability is lost, state obtention from RPCs becomes an act of trust, not verification (as no proofs are served with such messages), and the decentralized execution layer begins to centralize in subtle but irreversible ways.

## 2. What Partial Statefulness Actually Means

Between the extremes of a fully stateful node and a stateless client lies a theoretically appealing compromise: partial statefulness, sometimes framed as partial statelessness.

In this model, a node retains and serves only the subset of Ethereum’s global state that is directly relevant to its own activity or the users it supports, discarding the rest.

This approach can be understood as an alternative path to the same goal as state expiry: reducing the burden of perpetual state growth. Whereas state expiry enforces data deletion protocol-wide, partial statefulness allows operators to specialize voluntarily — keeping only the data that matters to them.

It also offers an intuitive appeal from an application-centric perspective.

Consider USDC, the ERC-20 stablecoin. The USDC contract is among the most actively used on Ethereum mainnet, and the companies behind it, they already have machinery to provide state-related data mostly related to their contract..

For such an actor, maintaining an RPC server that stores and serves only the USDC-related portion of Ethereum’s state — balances, allowances, and event logs — would be highly efficient.

This arrangement provides three key benefits:

- Reduced operational cost. Limiting storage to a single contract’s data dramatically lowers hardware and indexing requirements.
- Localized availability. Users interacting with that contract can access data faster and more reliably, without relying on third-party RPC providers.
- Improved self-sufficiency under state expiry. If Ethereum eventually enforces in-protocol expiry — pruning old, inactive state — users or DApps that already hold the fragments they care about can revive that data far more easily.
Without such local holdings, users become vulnerable to revival monopolies. Imagine an account with a million dollars in tokens that remains untouched for five years and is thus pruned. When the owner returns, they must reconstruct the state from external providers — who may charge arbitrary fees for data restoration.

By contrast, partial state retention distributes this burden, aligning with the broader logic of state expiry — smaller global state, but more personalized persistence.

[![image](https://ethresear.ch/uploads/default/optimized/3X/f/a/fadc8bb01bb7ed53191e705a73636e815e0be865_2_690x317.png)image1528×704 19.2 KB](https://ethresear.ch/uploads/default/fadc8bb01bb7ed53191e705a73636e815e0be865)

This in turn reinforces the appeal of partial statefulness: the more users keep selective fragments, the easier it becomes to reason about and implement expiry, completing a virtuous cycle between selective storage and sustainable pruning.

Yet, as we will see, this is closer to an idealized scenario than a practical one. The coordination, consistency, and incentive mechanisms required to make such selective persistence reliable at scale are extraordinarily complex — turning what looks like a pragmatic optimization into, at least for now, a form of technological utopia rather than a realistic expectation.

## 3. From Full Nodes to Stateless Clients — The Structural Transition

In Ethereum’s early years, full nodes performed three tightly coupled functions:

Consensus verification — checking that every block’s execution followed protocol rules.

State availability — achieved primarily through sync state serving, where nodes provided state data to peers during fast or snap synchronization. This peer-to-peer mechanism was the backbone of Ethereum’s distributed data layer.

User-facing access — offered through RPC serving, a niche but essential interface enabling wallets, dApps, and explorers to query or broadcast transactions. Unlike sync state serving, RPC endpoints were rarely operated by individuals; they were and still are predominantly provided by companies and infrastructure services such as Infura, Alchemy, or exchange-operated nodes.

These three roles together formed a coherent ecosystem. To verify blocks, a node had to hold the full state; and by holding it, it naturally contributed to both the sync layer and (occasionally) the RPC layer. This alignment made Ethereum’s availability largely self-sustaining — a by-product of consensus itself.

The emergence of stateless validation and ZK-EVM proofs decouples these roles. A node can now verify correctness without holding any state at all. Once verification and storage are separated, maintaining full state becomes optional — and economically irrational unless compensated.

Partial statefulness appears to offer a compromise, but the illusion fades once we consider how Ethereum’s execution model actually works.

## 4. The Infeasibility of Partial Statefulness

### 4.1 The Missing Witness Range — Why Re-execution and Proof Serving Become Impossible

Ethereum’s consensus depends on every node’s ability to re-execute transactions deterministically, given the parent state root.

For this to hold, a node must be able to traverse the full authentication path of any account or storage slot — from the global state root down to the leaf node representing that value.

A partially stateful node (such as OOPSIE) intentionally retains only the leaves relevant to it — e.g., an account’s balance, nonce, or specific ERC-20 mappings — but discards most of the intermediate trie nodes that connect these leaves to the state root.

This absent segment is the missing witness range: the sequence of intermediate nodes between the leaf and the state root.

![missing_range](https://ethresear.ch/uploads/default/original/3X/6/0/6006b6d5528b474522c939005ef533f3d5579636.svg)

These nodes are crucial for two reasons:

#### Authentication and proof generation.

To produce or verify a Merkle proof of inclusion — whether for an RPC query, a light client request, or a snap-sync operation — a node must possess every node along this path.

Without it, the node cannot prove that its locally held data actually belongs to the canonical global state.

Consequently, partial nodes cannot serve authenticated RPCs, cannot participate in snap-sync for the segments they store, and cannot help others reconstruct state trustlessly.

The result is a network where only a few full providers (e.g., Infura, Alchemy, exchange nodes) retain the capacity to generate valid proofs.

Everyone else becomes a passive data holder, unable to attest to correctness — a quiet but absolute form of centralization.

#### State revival under expiry.

In state-expiry regimes (in-protocol or external), a user must prove that an expired account or storage slot previously existed and was part of the global state root at some block.

Doing so requires exactly the same authentication path.

If the user lacks the missing witness range, they cannot prove existence — even if they still hold their local data.

They must turn to centralized providers to obtain the missing nodes, effectively paying “revival rent” to data oligopolies.

This paradox defeats the purpose of partial statefulness.

A node may hold its own data, but it cannot authenticate it. It can serve state but not trustlessly; it can answer queries but not help anyone sync.

As a result, the network drifts toward a model where proofs, snapshots, and synchronization are monopolized by the few actors that preserve the full trie — the very centralization Ethereum sought to avoid.

[![image](https://ethresear.ch/uploads/default/optimized/3X/3/5/351b8de7b85e788f0ff6e66f5297a5fa02e94be5_2_518x500.png)image1228×1184 65.1 KB](https://ethresear.ch/uploads/default/351b8de7b85e788f0ff6e66f5297a5fa02e94be5)

### 4.2 The Economic Problem — No One Pays for Partial Knowledge

Historically, full nodes engaged in sync state serving as a by-product of consensus participation: to verify, they had to store; and by storing, they could serve & verify.

Stateless verification dissolves that link. Once nodes can validate without storage, there is no built-in reason to maintain state for others.

The peer-to-peer sync layer — the true backbone of availability — becomes an unpriced externality. Rational nodes prune aggressively, while only a few specialized actors retain complete snapshots.

This shift has practical and systemic consequences.

- Mundane operations we take for granted today — syncing a node from scratch, fetching a specific range of accounts or storage slots via snap-sync, or obtaining authenticated proofs for a particular contract — will no longer be broadly viable.
- The infrastructure that supports these everyday tasks will shrink to a handful of entities capable of serving authenticated data. In practice, that means RPC providers.
They will likely remain the only actors capable of sustaining full-state access, but this service will almost certainly be commercialized, not freely provided.
- As altruistic full-node operators disappear, the network’s capacity for permissionless synchronization and open access will erode, pushing Ethereum toward de-facto data centralization.
- If the data layer becomes centralized, those custodians gain the ability to collude — selectively throttling, censoring, or even excluding new builders and infrastructure providers from joining the network.
Control over state access becomes control over who can meaningfully participate.
- Furthermore, nodes that wish to reconstruct the full state independently will have no practical shortcut other than replaying blocks from genesis — performing a full sync.
Without broad state-serving peers, this process becomes prohibitively slow and resource-intensive, reinforcing dependence on centralized providers.

[![image](https://ethresear.ch/uploads/default/optimized/3X/5/8/5816ba0fcb7b34d655b3840cdbba5633ae8ebab0_2_685x500.png)image1510×1102 61.1 KB](https://ethresear.ch/uploads/default/5816ba0fcb7b34d655b3840cdbba5633ae8ebab0)

Furthermore, building incentivized state-serving markets is profoundly complex (ie. Portal Network, which took years to develop and did not include any incentive mechanism).

Private capital has little reason to fund such infrastructure when the simpler and more profitable path is to run proprietary RPC services.

Incentivized state availability requires cryptoeconomic coordination, micropayments(to pay minimal amounts for state-on-demand), and verifiable accounting for data served — a level of protocol-native integration that Ethereum has not yet achieved (And some might believe is unachievable).

Until that exists, the economic equilibrium remains clear: few will pay to serve state, and even fewer will do it altruistically.

### 4.3 The Fragmentation Problem — State as a Partially Divisible Graph

The challenge of state fragmentation is often overstated, yet it remains non-trivial.

When an operator chooses to maintain a partial state, it is typically because they know precisely what subset they need to fetch and maintain.

Given an account or contract address, one already possesses its code hash, which uniquely identifies the bytecode.

From that bytecode — or the associated ABI, when available — a node can reconstruct most of the depdancy layout, event schema, and function selectors relevant to that contract.

In many cases this is sufficient: the majority of interactions are self-contained, and delegate calls to arbitrary external contracts are relatively uncommon (though this is what 7702 does, so it’s about to become a lot more common).

Under these assumptions, a partial node can in principle isolate and maintain coherent fragments of the state, especially for contracts with stable, well-understood interfaces such as ERC-20 tokens or DEX pools.

However, this separability has limits. Cross-contract calls, upgradeable proxies, or composable protocols can introduce dependencies that are not statically inferable.

While not the most critical constraint, fragmentation still undermines the universality of re-execution: even if partial nodes remain functional within their domain, the system as a whole cannot guarantee deterministic replay across all subsets.

---

**The upcoming examples can be skiped. But they provide valuable insight on why these partial stateful RPC-serving nodes aren’t really useful in today’s use cases of Ethereum. Even for the basic users of the chain.**

---

### 4.3.1 An example: the never-ending chain of dependencies

It is tempting to say: “We only care about this one contract. Let’s just keep that.” But on Ethereum, even something as conceptually narrow as “just serve state for one ERC-20 token” very quickly drags in a long tail of other contracts, other storage, and other actors. Past a certain point, you are no longer “partially stateful.” You are just doing state, but informally and with worse guarantees.

Consider a seemingly simple goal: operate a partial node that “only” serves USDC-related state to users (balances, allowances, transfers), e.g. to act as an application-local RPC for that token.

At first glance this looks self-contained:

- You store USDC.balanceOf(address) for relevant addresses.
- You store allowance(holder, spender) for those addresses, so you can answer “can this wallet spend my USDC?”
- You store the USDC contract metadata and code hash.

So far, this looks perfectly compatible with partial statefulness. But now look at what users actually ask in practice, and what you would need to serve honestly (with correct answers instead of trust-me-bro state chunks without any MPT proofs):

### 4.3.2 DEX liquidity and pricing.

Users don’t just ask “what’s my USDC balance?” They ask “what is this USDC actually worth?” and “what will I get if I swap it?”.

To answer anything about price, you now need state from the AMM pools where USDC is paired: e.g. USDC/ETH pools, USDC/USDT pools, USDC/DAI pools.

Concretely, that means you now have to pull in:

- The pool contracts (e.g. specific Uniswap-style pair contracts or concentrated-liquidity pool contracts).
- The pool reserves / liquidity ranges / ticks.
- Fee parameters and accumulated fees per liquidity position.
Those are different contracts. They’re not part of USDC’s storage trie — they live in completely separate accounts, each with their own storage roots.

If you don’t store that, you cannot answer even very basic “is this price quote legit?” questions without deferring to some external source.

### 4.3.3 Routers and approvals.

Real users don’t transfer USDC directly; they route through DEX routers, aggregators, vaults.

To know if “this account can execute a swap using USDC right now,” you can’t just answer using `allowance(user, router)` from the USDC contract in isolation. You now also need:

- The router contract(s) themselves (which router are we talking about? Uniswap’s router? 1inch? CowSwap settlement contract?)

> and if the RPC/Dapp decides to select only a few, means that there will be a DEX centralization as well. It’s not just the chain that falls to this pitfall.

- The router’s logic about which pools it will touch,
- Potential intermediate hop tokens.

If USDC → WETH → some other token is the default path, you’re implicitly tracking WETH state too: balances, allowances, total supply, and possibly wrapped ETH accounting.

So “I only serve USDC state” silently becomes “I serve USDC, WETH, and all the router contracts and their assumptions about connectivity.”

And this pulls in yet another layer of external contract code and storage.

### 4.3.4 LP positions and vault wrappers.

Many users don’t even hold USDC directly in their externally owned account. They hold it inside something:

- In a Uniswap V3 position (which is itself an NFT that encodes a price range, tick spacing, and liquidity amount),
- In a lending protocol (USDC deposited as collateral, now represented as an aUSDC/cUSDC-style derivative balance),
- In a yield vault or auto-compounder contract.
To answer a very normal user question like “how much USDC do I really have?”, you now have to:
- Inspect their position manager NFT contract and read position state,
- Inspect lending pool accounting contracts to see how much claim they have on the underlying,
- Inspect vault share tokens and figure out the share→underlying exchange rate.

None of those live in the USDC contract. They’re not even structurally “children” of USDC in the trie. They are independent contracts with independent storage, each of which now becomes part of “your subset.”

### 4.3.5 Data authenticity.

Even if you say “fine, I won’t do prices, I’ll only tell you balances,” you still hit the witness problem.

To serve *provable* answers — i.e. to provide Merkle proofs that “this balance really is part of the canonical state” — you don’t just need the leaf for `USDC.balanceOf(user)`.

You need:

- The entire authentication path for that slot up to the global state root,
- Which means intermediate trie nodes for USDC’s account,
- Which themselves depend on the global account trie.
That already forces you outside of “just USDC,” because those intermediate trie nodes co-mingle structure from other accounts.

The dependency explosion happens even before we get to any DeFi composability.

> What looked like a neat, contract-scoped slice of state turns out not to be a slice at all. It’s a graph whose closure is “most of DeFi + witness paths.” The combinatorial dependency graph means that, in practice, trying to remain narrowly partial either makes you:
>
>
> useless (you can only answer trivial questions, and even then not with proofs), or
> de facto full-service (you’re now tracking a huge chunk of Ethereum’s economic state anyway).

This is why fragmentation, while not always the *first* blocker (the missing witness range is more fundamental), is still fatal at scale. Even a “tiny” vertical like “just USDC” tends to force you into everything else **if you want to be meaningful. Not just functional**.

## 5. The Incentive Paradox

Statelessness introduces an asymmetry: verification becomes trustless and cheap, while state availability remains costly and unrewarded.

This dismantles the feedback loop that once aligned incentives. Full nodes no longer gain utility from storage, and partial nodes cannot perform full verification.

The logical endpoint is a bifurcated system:

A small set of state-rich sync providers maintaining data continuity.

A large population of stateless proof consumers depending on those providers for access to historical or off-subset data.

Ironically, the more Ethereum optimizes for efficiency, the stronger its pull toward centralization. Efficiency removes redundancy; redundancy was what made the system resilient.

## 5.1 The technical part is fixable

The missing-witness problem described earlier — the inability of partial nodes to reconstruct the authentication path between their local storage and the global state root — is not a cryptographic dead end.

It is an architectural gap. Once we define a lightweight, standardized way to keep the upper levels of the state trie in sync, the gap closes.

[![image](https://ethresear.ch/uploads/default/optimized/3X/1/4/14616b7d4496a67e361563921888d3cca69fe81d_2_690x431.png)image1892×1184 246 KB](https://ethresear.ch/uploads/default/14616b7d4496a67e361563921888d3cca69fe81d)

### 5.1.1 Rebuilding the top of the trie — account commitments

Every Ethereum account leaf already commits to four fields:

```auto
nonce, balance, storageRoot, codeHash
```

encoded as an RLP tuple whose hash forms the account value in the Merkle-Patricia Trie:

```auto
accountHash = keccak256(RLP([nonce, balance, storageRoot, codeHash]))
```

If every node — even a partial one — kept **only this 32-byte hash per account**, it would have all the information needed to hash upward toward the global state root.

No balances, no code, no execution traces — just one 32-byte commitment per address.

At today’s scale:

- ≈ 300 million accounts
- × 32 bytes each
- ≈ 9.6 GB total

That dataset is small enough for a modest machine or even a Raspberry Pi-class device, yet complete enough to verify any account’s inclusion in the state root.

Nodes could store it as:

- a flat key-value table (address → accountHash), updated in place; or
- a lightweight Merkle accumulator, incrementally hashed upward as blocks arrive.

Either structure makes the node cryptographically aware of the global state without requiring it to re-execute transactions or retain contract storage it doesn’t care about.

### 5.1.2 Per-block sidecars — compact account-hash diffs

To keep this global account-hash table synchronized, each block would carry — or reference — a small **sidecar payload** broadcast through a pub-sub channel (similar in topology to Beacon-chain gossip).

The sidecar contains only:

1. The list of accounts touched by the block’s transactions old_accountHash = keccak256(RLP([nonce, balance, storageRoot, codeHash]))
2. For each, the updated new_accountHash = keccak256(RLP([nonce, balance, storageRoot, codeHash])).

Every partial node subscribed to this topic processes the sidecar as follows:

1. Replace the stored 32-byte hash for each changed account.
2. Re-hash incrementally — using cached untouched branches — to derive the new state root.
3. Verify that the computed root matches the one announced in the block header.

That’s all. The bandwidth overhead is minimal (typically comparable to, or less than, the block size itself) and the computation is trivial compared to full re-execution.

From then on, the node is **state-root–synchronized**: it can verify that its local partial data sits under a root consistent with the canonical chain.

[![image](https://ethresear.ch/uploads/default/optimized/3X/c/5/c5e8de273e0301c53b7e369422869cc20c7fa9f4_2_690x416.jpeg)image1656×1000 212 KB](https://ethresear.ch/uploads/default/c5e8de273e0301c53b7e369422869cc20c7fa9f4)

### 5.2 Proof-capable partial nodes and SnapSync contribution

Once a node maintains this up-to-date account-hash table, it gains full proof capability for the storage subtrees it actually holds.

For example, a node keeping the `USDC` contract’s storage can:

1. Produce a Merkle proof from a local slot (e.g. balanceOf(address)) to the contract’s storageRoot.
2. Use the globally tracked accountHash for USDC (which embeds its storageRoot) to connect that proof to the account layer.
3. Re-hash upward to the verified global state root derived from sidecar updates.

That’s enough to serve authenticated RPC responses and snap sync ranges for its subset of state — **no re-execution required**.

Collectively, such nodes would become *active contributors* to Ethereum’s data-availability layer:

- Each can serve verifiable state fragments to others.
- SnapSync no longer depends solely on a few full nodes.
- OOPSIE-style partial clients evolve from passive caches into distributed, proof-aware micro-providers.

This technical pathway doesn’t solve incentives — it only makes them easier to target.

Once partial nodes can serve authenticated state, Ethereum can design rewards around **sync-state serving** itself.

A light device at home could hold a few gigabytes of account-hash data, store one or two contract subtrees, and earn modest compensation for providing Snap Sync proofs — a realistic, energy-efficient role that broadens participation instead of narrowing it.

---

## 6. Conclusion — Ethereum’s Binary Future

Ethereum’s long-term architecture is converging on a binary outcome.

Either the protocol introduces **explicit incentives for sync-based state availability**, or it accepts a future in which a handful of persistent providers become the de facto custodians of the network’s data.

From a technical standpoint, we now know that *partial statefulness is not impossible*.

Through account-level commitments and per-block sidecars, it is possible for nodes to recompute the state root, prove correctness for their subsets, and even contribute authenticated data to snap sync.

In other words, the OOPSIE vision — partially stateful, proof-aware nodes that serve small fragments of state — can indeed exist as a coherent technical species within the Ethereum ecosystem.

But even if we solve the witness-range problem and make partial nodes cryptographically viable, we remain inside the same **economic vacuum**.

No mechanism today compensates anyone for holding or serving state.

Verification is rewarded implicitly through consensus participation; storage and sync serving are not.

This asymmetry is what slowly starves the network’s data layer.

Full nodes prune aggressively because there is no reason not to.

RPC operators consolidate because they can extract fees while others cannot.

And partial nodes, even if technically sound, will simply not appear in sufficient numbers without a reason to run them.

### 6.1 Incentivized snap sync as the Natural Focal Point

The good news is that, once the technical side is solved, the **incentive problem becomes far more tractable**.

If partial nodes can meaningfully participate in snap sync — serving authenticated subtrees and proofs — then *that* becomes the natural focal point for incentives.

Rather than paying for global storage or subsidizing full nodes indefinitely, Ethereum could instead reward **state-serving events**: the act of responding to SnapSync requests or supplying verifiable proofs of state to peers.

That changes the economics of participation.

It opens a path for *low-power, low-cost machines* — home devices, Raspberry Pi–class setups, or modest cloud instances — to run partial nodes profitably.

These nodes wouldn’t need to hold the entire global state or execute every transaction.

They would simply keep authenticated fragments and earn small, ongoing rewards for serving them.

The protocol’s data layer would shift from a system of altruistic giants to a swarm of incentivized micro-providers.

### 6.2 Who Provides the Sidecars?

One open question is *who actually generates and distributes* these per-block sidecars — the compact lists of account-hash diffs that allow partial nodes to update their state roots.

In principle, the responsibility could fall to **block proposers**, who already commit to the resulting state root in each block.

They are in the best position to assemble the set of changed account commitments and broadcast it through a pub-sub overlay, just as the beacon chain handles block attestations today.

Doing so could be coupled with a **market-based incentive**: nodes that serve or relay these sidecars (and can prove correct delivery) receive micropayments proportional to their contribution.

This aligns the cost of sidecar generation and dissemination with block production and network bandwidth, ensuring that the data layer remains economically grounded rather than purely altruistic.

### 6.3 The Fragility of Loss and the Need for Redundant Persistence

Even with a functioning incentive system, *state loss* remains a critical risk.

If certain fragments of the state — or their corresponding proofs — vanish due to inactivity or unavailability, those portions of Ethereum’s history effectively become opaque.

Contracts or accounts dependent on lost segments could no longer be proven to exist at a given root, and any mechanism relying on revival proofs (e.g., state expiry reactivation) would fail.

This underscores the importance of **redundant persistence**.

In a world of partial stateholders, the survival of any fragment should not depend on a single node.

Incentives must therefore not only reward serving but also *replication* — encouraging overlapping storage of the same subtrees across diverse participants.

A healthy network would display a natural redundancy gradient: popular or economically active contracts (like USDC or major DEX pools) replicated by thousands, obscure ones by a few.

### 6.4 Redefining Decentralization through Incentivized Diversity

That vision — *incentivized snap sync serving over total storage* — is what makes partial statefulness not just technically meaningful, but socially sustainable.

It redefines decentralization in practical terms: participation measured not by who can afford a datacenter, but by who can keep a small, verified piece of the state alive and responsive.

OOPSIE, in this light, is less a utopia than a prototype of alignment.

It exposes the gap between what is technically possible and what is economically rational — and in doing so, it points toward a future where Ethereum’s data layer could once again scale through *incentivized diversity*, not consolidation.

The challenge ahead is therefore not to invent new proofs, but to **reward persistence itself**.

Only when maintaining and serving state becomes an economically meaningful act — including the generation, relay, and redundancy of sidecar data — will Ethereum’s execution layer remain truly decentralized.

### 6.5 A final note on ZKEVM-statelessness.

> This is not a critique of ZK-EVMs — quite the opposite.

Their development marks one of the most significant technical leaps in Ethereum’s history.

But precisely because they make verification effortless, they expose and amplify a deeper structural problem: there is still no backplane for data persistence once nodes begin pruning state.

Without a coordinated mechanism for retaining or re-serving historical data, the network risks becoming verifiable yet empty — a chain whose proofs survive, but whose underlying state slowly disappears.

Solving this is not a detour from the ZK-EVM roadmap; it is a prerequisite for making its stateless future sustainable.

## Replies

**MicahZoltu** (2025-11-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/cperezz/48/9563_2.png) CPerezz:

> Mundane operations we take for granted today — syncing a node from scratch, fetching a specific range of accounts or storage slots via snap-sync, or obtaining authenticated proofs for a particular contract — will no longer be broadly viable.
> The infrastructure that supports these everyday tasks will shrink to a handful of entities capable of serving authenticated data. In practice, that means RPC providers.
> They will likely remain the only actors capable of sustaining full-state access, but this service will almost certainly be commercialized, not freely provided.
> As altruistic full-node operators disappear, the network’s capacity for permissionless synchronization and open access will erode, pushing Ethereum toward de-facto data centralization.
> If the data layer becomes centralized, those custodians gain the ability to collude — selectively throttling, censoring, or even excluding new builders and infrastructure providers from joining the network.
> Control over state access becomes control over who can meaningfully participate.
> Furthermore, nodes that wish to reconstruct the full state independently will have no practical shortcut other than replaying blocks from genesis — performing a full sync.
> Without broad state-serving peers, this process becomes prohibitively slow and resource-intensive, reinforcing dependence on centralized providers.

It also brings back the privacy problem, where lightclients are connecting their IP address and wallet address by asking centralized sync providers for their updated account data.  Can be somewhat mitigated by adding noise, but one could argue that lightclients today can already add “noise” to their eth_calls if they wanted (but they don’t).

---

**MicahZoltu** (2025-11-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/cperezz/48/9563_2.png) CPerezz:

> ### 6.2 Who Provides the Sidecars?
>
>
>
> One open question is who actually generates and distributes these per-block sidecars — the compact lists of account-hash diffs that allow partial nodes to update their state roots.
> In principle, the responsibility could fall to block proposers, who already commit to the resulting state root in each block.
>
>
> They are in the best position to assemble the set of changed account commitments and broadcast it through a pub-sub overlay, just as the beacon chain handles block attestations today.
>
>
> Doing so could be coupled with a market-based incentive: nodes that serve or relay these sidecars (and can prove correct delivery) receive micropayments proportional to their contribution.
> This aligns the cost of sidecar generation and dissemination with block production and network bandwidth, ensuring that the data layer remains economically grounded rather than purely altruistic.

I think the answer here is that this shouldn’t be a side-car, it should be part of the core protocol and a block is only valid if the “side car” is present on the network.  Block builders who want their blocks accepted **must** provide this data to the network at time of block publishing (just like they **must** provide block bodies).

---

**MicahZoltu** (2025-11-05):

General feedback:

I feel like we should try to move away from MPTs for proofs, because they are so big compared to other proofs.  Have you looked into things like Verkle trees to reduce proof sizes?

When sending assets to someone, you need *their* account details so you can know (for example) how much gas to provide (if the recipient is a contract wallet you’ll need more than 21,000).  I wonder if when someone shares their account with you via QR code, we could also fit their account proof in the QR code so the sender can properly construct the transaction without any third party involved?

---

**CPerezz** (2025-11-06):

I think that while I agree that privacy is a concern. Is even more concerning that we can simply not sync anymore or that full-state data becomes so scarce that centralization gets crazy.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Block builders who want their blocks accepted must provide this data to the network at time of block publishing (just like they must provide block bodies).

It’s mandatory for builders to provide it I’d agree on that. But I wouldn’t say it’s a must to recieve it/forward it. Basically, these sidecars can be quite big.  (MBs upwards). So you don’t want to propagate that across the entire network as it would significantly impact the overall bandwidth and latency of it.

Well. Verkle was the best option wrt. proof sizes. But it was killed when it was quasi-ready to be shipped. So we are back at the start line again..

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I wonder if when someone shares their account with you via QR code, we could also fit their account proof in the QR code so the sender can properly construct the transaction without any third party involved?

That we could do ofc. But should kinda be made as a standard. So we would probably need wallet-consensus most likely.

---

**MicahZoltu** (2025-11-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/cperezz/48/9563_2.png) CPerezz:

> It’s mandatory for builders to provide it I’d agree on that. But I wouldn’t say it’s a must to recieve it/forward it.

If it isn’t mandatory to propagate, then it isn’t mandatory to provide.  A given node in the network cannot trustlessly differentiate whether the person giving them a block is the original block builder or an intermediate peer gossiping the block.  If we try to enforce this, a builder can simply “gossip” their block to a single recipient (that they also operate) and then forward the block (without the sidecar) to the network.

I can appreciate that these “side cars” are big, but that is the price we pay for cranking up the gas limit to 11, and if we choose to continue to ignore the costs of high gas limits then *something* is going to break.  I would rather what breaks is the P2P network bandwidth, because that is visible to everyone (including core devs), rather than making it so fewer and fewer people can run trustless clients, which seems to be invisible to the core devs (despite many people telling them it is happening).

