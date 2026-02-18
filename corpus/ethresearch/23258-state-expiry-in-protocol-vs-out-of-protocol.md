---
source: ethresearch
topic_id: 23258
title: "State Expiry: In-protocol vs. Out-of-protocol"
author: weiihann
date: "2025-10-17"
category: Execution Layer Research
tags: [stateless, data-availability, execution]
url: https://ethresear.ch/t/state-expiry-in-protocol-vs-out-of-protocol/23258
views: 484
likes: 10
posts_count: 9
---

# State Expiry: In-protocol vs. Out-of-protocol

# State Expiry: In-protocol vs. Out-of-protocol

*State growth* remains the primary performance and decentralization bottleneck. It drives longer node syncs, degrading block execution performance and increasing storage requirements. This is different from history growth (old blocks/receipts), which EIP-4444 lets clients prune. [Recent empirical analysis](https://ethereum-magicians.org/t/not-all-state-is-equal/25508) of state access patterns show state usage is highly skewed—most txs hits a small subset of hot state, so removing cold state can help to reduce node burden significantly.

**State expiry** primarily aims to slow down state growth (or even keep it at a constant). It proposes **removing cold state** from the active set and requiring **resurrection proofs** when it’s accessed again. So far, two blockers have delayed us from shipping state expiry:

1. User experience: how users retrieve proofs for resurrection.
2. Cheap, robust labeling of expired state objects.

As we move toward real-time proving and a stateless world, it’s unclear exactly how state expiry should fit. Therefore, this article does two things:

- Maps who actually needs state and how state expiry helps across today’s and plausible future roadmap.
- Compares in-protocol vs out-of-protocol state expiry with concrete trade-offs.

## Who holds the state?

### Today (2025)

*TL;DR: Most nodes have to hold the state.*

1. Validators: Build, execute and validate blocks against the active state. Practical operation still assumes full state.
2. Builders: Out-of-protocol. A few entities build the majority of blocks (see concentration in Who wins block building auctions?). They maintain state to simulate and build blocks.
3. RPC nodes: Typically run full nodes. Some may use follower patterns (e.g., Besu’s fleet mode) where lighter nodes retrieve state deltas from a trusted full node.

**If we ship in-protocol state expiry now:** everyone benefits from it—smaller active state for execution, faster sync, lower state read/write latency, and less risk when increasing gas limits.

### Long Term (ePBS + stateless)

*TL;DR: Only builders must hold state while others can be stateless.*

Assume enshrined PBS ([EIP-7732](https://eips.ethereum.org/EIPS/eip-7732)) and censorship-resistance mechanisms (e.g., [FOCIL](https://eips.ethereum.org/EIPS/eip-7805)), plus statelessness with either (a) Verkle/Binary trie witnesses in blocks or (b) block execution ZK proofs:

1. Proposers/Attesters — Verify via witnesses or proofs. No need for global state. Ideally validity-only partial statelessness (VOPS) to keep the public mempool healthy.
2. Builders: Requires state to build blocks. With FOCIL (without witness-carrying txs), builders are expected to have access to the full state.
3. Provers: Need state access to retrieve witnesses used in proof generation.
4. RPC nodes: Trend toward partial statelessness (local-node-favoring) where each node only stores state that it cares about, but still ideally VOPS.

In this world, state expiry primarily benefits builders, who bear most of the cost of state growth. Without expiry, builders must provision increasingly heavy hardware, further *increasing* builder centralization.

If provers are different from builders, then they can be stateless. But stateless provers still need to retrieve state witnesses from nodes that hold the full state, so state expiry also improves costs and efficiency in a real-time proving world.

## In or Out?

### In-protocol State Expiry

“In-protocol” means expiry rules live in **consensus**. State objects carry minimal metadata which gets updated on state access (read, write, or both). If an object is expired at access time, it must be **resurrected** (typically via a tx) with attached witnesses. One example is [EIP-7736](https://eips.ethereum.org/EIPS/eip-7736) (leaf-level expiry on Verkle/Binary trie).

#### Why it’s good

**1. Clear responsibility boundary**

If your state is expired, *you* are responsible for finding and supply the proof. No ambiguous “who hosts my old state?” problem.

**2. Keeps local building possible**

In a stateless world, a smaller active state keeps local builders viable and pushes back on builder concentration. However, it’s undeniable that in the current status quo, a few builders produce most of Ethereum’s blocks.

**3. Benefits remaining stateful nodes**

In a world with stateless attesters, syncing the full state is challenging if not impossible if most participants are stateless. Therefore, we should still expect some nodes will still hold the full state and serve it altruistically (i.e. snap sync). An in-protocol expiry rule would reduce their burden. However, this reliance on altruism can be mitigated by a decentralized state network such as the [Portal Network](https://ethereum.org/developers/docs/networking-layer/portal-network/#why-do-we-need-portal-network), which preserves and can serve state without depending on altruistic stateful nodes. Though Portal itself is an altruistic system.

**4. Predictable UX surface**

Wallets can target a *single* expiry rule, not a patchwork of builder policies.

#### Why it’s hard

**1. Resurrection UX**

Wallets need robust flows for **multi-object resurrection** (e.g., batch proofs) to avoid multiple hops for state resurrection. The more granular the scheme (slot-level vs account-level), the tougher the UX.

**2. Who hosts expired state?**

State expiry doesn’t make the state objects disappear forever. We still need *state serving infra*—ideally decentralized. Reliance on trusted proof providers may be tolerable in the short term only if the scheme truly prunes state that’s useless to ~99.99% of users. The tradeoff, however, is that less cold state tends to be pruned.

**3. Complexity & DoS surfaces**

Expiry metadata must be stored, which adds storage overhead. The finer-grained the expiry scheme, the higher this overhead. Resurrection complexity also depends on the scheme: for example, resurrection in a [multi-tree expiry approach](https://hackmd.io/@vbuterin/state_size_management#Two-trees) is more complex than a leaf-level design such as [EIP-7736](https://eips.ethereum.org/EIPS/eip-7736). Users also incur additional costs to resurrect expired state.

### Out-of-protocol State Expiry

Out-of-protocol means no consensus change. Nodes can adopt a socially coordinated expiry policies (e.g. onchain or offchain registries). Nodes may drop state and expect users to bring their own proofs—*but the chain does not force it.*

#### Why it’s good

**1. Reduce Ethereum protocol complexity**

Builders can flexibly determine expiry rules and iterate quickly. Policies can be coordinated socially or via onchain configuration. This could be easier than shipping a fork.

**2. Faster iteration & reversibility**

Builders can test with different pruning schemes more creatively. If a policy backfires, rollback is immediate and local. Bad expiry settings degrade that builders’ service quality (e.g. missed MEV, higher latency) rather than creating global consensus risk or chain-wide DoS surfaces.

**3. Ecosystem compostability**

Creates clear demand for decentralized state networks and commercial witness services. Both can compete on latency, coverage, and price without protocol coupling. Out-of-protocol fees for supplying valid witnesses can be trialed as sidecar markets.

**4. Transitioning into in-protocol**

Real world usage may inform eventual in-protocol expiry (if ever needed). It’s also easier than doing in-protocol from day one.

**5. Uniform access layer (when DA is strong)**

If a fast, permissionless state network exists, out-of-protocol is compelling. Any stateless or partial stateless node can fetch witnesses on demand. Nodes get most expiry benefits without a fork, and wallets use one simple, proof-centric access path.

#### Why it’s hard

**1. Inconsistent UX and data availability**

Builders that don’t hold specific state require users to provide witnesses. This mirrors the in-protocol UX burden but **without guarantees** that any builder still has your state. If policies live in social consensus, app tooling must track multiple rules which further complicates UX.

**2. Who hosts expired state?**

Same problem as in-protocol state expiry. However, in the case of in-protocol, ownership is clearly defined (i.e. your state is your responsibility). For out-of-protocol, it’s not so clear so chances of data that is forever lost are higher.

**3. Censorship vector**

If “we don’t hold your state” is an acceptable policy, external pressure can weaponize it to exclude specific contracts, effectively turning it into a censorship attack.

**4. Builders + FOCIL nuance**

If txs in inclusion list don’t carry witnesses, builders effectively need access to the full state, so the incentives for out-of-protocol expiry drops. Builders can adopt a hot-cold state segregation if it’s proven that performance is better.

If txs in inclusion list do carry witnesses, builders can be partial stateless, but this becomes another in-protocol rule which worsen user experience because now all txs have to carry witnesses (a.k.a. strong statelessness).

**5. Syncing the state**

When operators prune out-of-protocol, state availability is non-uniform across peers. Syncing the full state may be harder or even impossible.

### Challenges with State Resurrection

In general, any form of state expiry (in or out) has to deal with resurrection. Here are some of the challenges:

#### Resurrection Hopping

Imagine you want to send 1 ETH and some DAI to a long-dormant account. First, the account lookup reveals the account is expired, so the transaction fails. You fetch a proof and resurrect the account. Next, the DAI transfer touches the token’s storage, which are also expired. You must fetch additional proofs and resurrect those slots. This back-and-forth interaction is the *“resurrection hopping”* problem.

This is worse with **in-protocol** expiry because each resurrection typically requires submitting a transaction. The more expired objects a transaction touches, the more hops and fees. **Out-of-protocol** faces the same discovery/fetch loop, but the hops are **off-chain** (no extra transactions), but still adding extra latency.

**Possible mitigations**

1. Pre-simulate the transaction against a full-state oracle to enumerate all accounts and storage slots that must be resurrected before submitting the user transaction.
2. Reduce granularity of expiry (e.g., account- or contract-level vs slot-level) to remove the number of distinct objects that need resurrection.
3. Batch resurrection: support a single bundled proof that resurrects multiple accounts/slots atomically, with explicit byte caps to control DoS risk. Blobs can keep txs cheap, but because they are transient, the resurrection payload must be stored elsewhere permanently and made available to everyone.

#### Where to get the state?

1. RPC providers
Third-party infra (commercial or public) that serves the state with proofs.

Pros

Widely available today
2. Can offer service-level agreements (SLAs) that guarantee data availability
3. Naturally incentivized to retain full state in order to “sell” access to expired state
4. Cons

Trust & censorship risk: RPC providers can choose to or be compelled to censor certain state, denying state resurrection
5. Users pay to retrieve the state (in addition to resurrection txs for in-protocol state expiry)
6. Client-hosted providers
EL client teams can host static files/snapshots for expired state over a defined expiry period—similar to the era files for block data. These files are refreshed when the canonical chain enters a new expired period. Erigon and Reth use similar snapshot mechanisms in their state sync architectures.

Pros

Greater community trust and transparency
7. State files and response format can be coordinated to minimize resurrection latency
8. Cons

Additional infrastructure and maintenance burden on EL client teams
9. It’s still a matter of trusting that the teams hold all of the expired state. If the state is not available, users have to fallback on RPC providers or find it somewhere else.
10. Altruistic snap sync peers
Rely on peers that serve state chunks (snap sync) to assemble the needed accounts/slots for proofs. This builds on an assumption that there are still nodes with the full state that will serve snap requests altruistically even with state expiry.

Pros

Already works today
11. Avoids reliance on a specific trusted provider
12. Cons

Assumption may fail as more nodes prune expired state. That is, newly created nodes can no longer do snap sync.
13. Resurrection UX degrades as the number of full state peers decreases. In the worst case, users must fall back to trusted providers
14. Decentralized state network
Permissionless network that stores the full state and can serves state with proof. One such example is the state network from the Portal network.

Pros

Censorship-resistant
15. Built-in replication reduces the risk of state going missing
16. Cons

No production-grade deployments as of today
17. Participation is largely altruistic without incentives, which can limit reliability under load
18. Incentivize nodes to hold subset of state via rainbow staking
Treat state serving as a light service within rainbow staking’s “unbundled roles” (heavy vs light). Operators commit to storing subsets of state and serving verifiable witnesses, while delegators allocate weight to these operators.

Pros

Decentralized
19. Aligns incentives: persistent, protocol-native rewards for keeping state available, reducing reliance on altruism
20. Cons

Current still in research phase and requires concrete designs for operator selection and reward accounting

Option 5 is the best long-term approach, but it will take time to implement. Option 2 is more realistic in the near term.

####

### What’s Next?

If we value independent builders and predictable UX, in-protocol state expiry remains the safer long-term anchor. In today’s world, state expiry clearly helps. But the UX burden and the risk of irretrievable data make immediate enshrinement unlikely.

Near term, we should **experiment out-of-protocol**. Treat out-of-protocol as prototypes to solve the same problems without consensus risk, while surfacing practical issues (e.g., state availability) and iterating on solutions. If out-of-protocol expiry proves reliable and user-friendly, we can consider **enshrining it** later—**only if** it’s truly needed.

## Closing

Shipping state expiry sooner delivers immediate wins—smaller active state, faster syncs, safer gas headroom. In a stateless future, most of those gains accrue to builders, provers, and a few stateful providers—the very places where centralization pressure concentrates. Starting with out-of-protocol expiry captures the wins quickly, exposes risks (witness availability, DoS, UX), and lets us iterate without consensus risks.

Above all, state-serving infrastructure is essential. As we move toward statelessness and state expiry, the network needs public, reliable, permissionless ways to retrieve state and witnesses consistently.

**Bottom line**: the network must not allow for permanent loss of state.

## Further Reading

- Possible futures of the Ethereum protocol, part 5: The Purge
- How to Raise the Gas Limit, Part 1: State Growth
- EIP-7732: Enshrined Proposer-Builder Separation
- Not All State is Equal
- A Protocol Design View on Statelessness
- A local-node-favoring delta to the scaling roadmap

## Acknowledgements

Special thanks to Guillaume, Carlos and Ignacio for reviewing this article.

## Replies

**Julian** (2025-10-20):

Hey Han! Thanks for the insightful post! I fully agree we should go for out-of-protocol state expiry first and use learnings from that to consider in-protocol state expiry.

In this post you suggest that using in-protocol state expiry leads to better coordination on who holds what state than out-of-protocol state expiry. This point is not completely clear to me in a world where attesters are stateless. Today clients are written primarily for validators and Ethereum assumes a majority of validators are honest and therefore store the state as clients prescribe. Builders, however, are not assumed to be honest and are free to change the client code to a different state expiry rule. Nothing stops them from doing so, even if an in-protocol state expiry rule exists, which I also argue in the [Protocol Design view on Statelessness post](https://ethresear.ch/t/a-protocol-design-view-on-statelessness/22060).

If attesters are stateless, the goal of state expiry is to grow state as much as possible without burdening builders too much with state storage and lookups. My intuition is that we are still quite far from that problem since optimistic solutions like holding frequently used state in memory may be possible as well although I know little about that so would be curious if you agree ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14) . Since the state expiry rule is designed for builders in the long term, it should be one that they are happy with / incentivized to follow. If the community agrees on a reasonable state expiry rule and state growth rate jointly, I think builders will likely follow the rule since optimizing state storage is probably not worth the R&D costs. Also curious whether that assumption holds!

Finally, FOCIL forces builders to behave honestly by including all txs seen in the mempool. If there is a state expiry rule, we can adjust the FOCIL specs such that it forces builders to behave honeslty according to the state expiry rule. That may mean that users have to provide witnesses for state that the builder is not required to have. However, I think the first principles approach is to think about who holds the state and the state growth rate without considering FOCIL to prevent designing the state “experience” with too much path dependency from FOCIL.

---

**rjl493456442** (2025-10-20):

We’ve recently made several breakthroughs that allow us to **meaningfully compress the archive node size**. In theory, we could reduce the full historical data, from genesis to the latest block, to around **5 - 6 TB** (though the exact number for mainnet is still being evaluated).

Moreover, **state histories are stored externally in append-only files**, separated from the live state. This design allows us to **scale storage easily** as historical data grows. I’m optimistic that **the growth in historical demand will never outpace the decline in storage costs**.

All the engineering improvements unlock the potential that the normal nodes with full history can act as the state provider, with the ability to provide the expired states along with the proof.

We can design some incentive protocols with onchain payment plugged. These nodes can advertise themselves as the state provider via DiscV5 with topics registered and let “customers“ find them easily.

All in all, building a state provider network should be a solution if there is a huge demand for resurrecting the expired states.

---

**MicahZoltu** (2025-10-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/rjl493456442/48/21219_2.png) rjl493456442:

> I’m optimistic that the growth in historical demand will never outpace the decline in storage costs.

Full nodes are already too big for end-users to run their own RPC servers.  We don’t just need to halt growth or “match moores law”, we need to *decrease* the current state size.  Ideally, we should strive to get RPC server disk requirements down to ~10GB, which I believe is theoretically possible with some effort.  This is small enough that most laptops/desktops could fit it without much worry, and even some mobile devices could store it.

---

**weiihann** (2025-10-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Ideally, we should strive to get RPC server disk requirements down to ~10GB, which I believe is theoretically possible with some effort.

If the target audience is RPC providers, this is mostly a horizontal scaling problem. You can run one full node and many smaller “follower” nodes that trust the full node. [Besu’s Fleet Mode](https://community.linea.build/t/besu-linea-fleet-mode-rpc-specific-node/9831) already demonstrates this.

If we’re targeting independent users, the ~10 GB goal becomes realistic in a post–ZKEVM or post-Verkle/binary-trie world. But we don’t have to wait for that: in principle, a light client could store a partial state and keep it updated via snap sync.

---

**MicahZoltu** (2025-10-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/weiihann/48/20091_2.png) weiihann:

> If the target audience is RPC providers, this is mostly a horizontal scaling problem.

I don’t care at all about centralized service providers.  You can safely assume anything I say is unrelated to them unless I explicitly state otherwise.  ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=14)

![](https://ethresear.ch/user_avatar/ethresear.ch/weiihann/48/20091_2.png) weiihann:

> If we’re targeting independent users, the ~10 GB goal becomes realistic in a post–ZKEVM or post-Verkle/binary-trie world.

I do think that to make 10GB trustless clients requires some protocol changes, like in-consensus state-diffs for each block transmitted over the P2P layer and stateless block validation, but I do not believe it requires ZKEVM (very far away) and I don’t *think* it requires tree changes.

A client would mark parts of state that it wants to retain, and it would use the state-diffs with each block to maintain those records, but it would not store the full state tree.  We need blocks with witnesses so users can validate incoming blocks locally without having to store everything that might be read by any block.

![](https://ethresear.ch/user_avatar/ethresear.ch/weiihann/48/20091_2.png) weiihann:

> But we don’t have to wait for that: in principle, a light client could store a partial state and keep it updated via snap sync.

This would be a trusted solution if I understand the proposal correctly.  You are essentially trusting that whoever you are syncing with is giving you correct data, but you have no way to validate it.

---

**weiihann** (2025-10-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> This would be a trusted solution if I understand the proposal correctly. You are essentially trusting that whoever you are syncing with is giving you correct data, but you have no way to validate it.

It’s a trust-minimized (not fully trustless) process. Starting from a weak-subjectivity checkpoint, a light client verifies the head beacon block header each slot via the sync committee aggregate signature. From that update it reads the execution payload’s `stateRoot`, then can uses snap sync to rebuild partial state with range proofs for verification. Repeating this on new headers lets you keep an up-to-date and verified partial state for the keys you care about—though you’re not validating state transitions and snap sync doesn’t tell you which keys changed, so you have to repeat the process.

---

**weiihann** (2025-10-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> My intuition is that we are still quite far from that problem since optimistic solutions like holding frequently used state in memory

I agree—for now, big machines can keep a huge chunk of the trie in RAM, and that makes state access fast. Take geth as an example. Currently, the trie size in geth is around 250GB, which can definitely be fitted into a big RAM.

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> Builders, however, are not assumed to be honest and are free to change the client code to a different state expiry rule.

True, you can’t force builders to store any specific state, especially the rational ones where removing huge chunks of state helps making block building faster. But I doubt that’s the case for independent block builders. Most independent builders stick close to upstream clients and won’t bother with making custom optimizations. A simple example from today: you *could* modify an EL client to stop sending some p2p messages (like new block announcements) to save bandwidth or CPU. In theory, that’s a “rational” tweak. In practice, almost nobody does it—because the client doesn’t expose that toggle. Same idea here: if clients ship a sensible expiry rule and proof format by default, most independent builders will follow it rather than maintain a one-off fork.

---

**saidonnet** (2025-10-24):

please check what ive accomplished on this subject, im new to the platform so i cant create new topics , i tried replying to you with full document but it was deleted , im dead serious, check the work on github saidonnet repo : revival-precompile-research

