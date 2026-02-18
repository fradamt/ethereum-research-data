---
source: ethresearch
topic_id: 22236
title: A pragmatic path towards Validity-Only Partial Statelessness (VOPS)
author: soispoke
date: "2025-04-29"
category: Execution Layer Research
tags: [stateless]
url: https://ethresear.ch/t/a-pragmatic-path-towards-validity-only-partial-statelessness-vops/22236
views: 1247
likes: 18
posts_count: 15
---

# A pragmatic path towards Validity-Only Partial Statelessness (VOPS)

[![ChatGPT Image Apr 22, 2025, 11_26_48 AM](https://ethresear.ch/uploads/default/optimized/3X/7/8/7812ac088ae07c6faaafc7ee1162930a1bd79b6a_2_333x500.jpeg)ChatGPT Image Apr 22, 2025, 11_26_48 AM1024×1536 148 KB](https://ethresear.ch/uploads/default/7812ac088ae07c6faaafc7ee1162930a1bd79b6a)

*Thanks to [Julian Ma](https://x.com/_julianma), [Ignacio Hagopian](https://x.com/ignaciohagopian), [Carlos Perez](https://x.com/CPerezz19), [Guillaume Ballet](https://x.com/gballet), [Justin Drake](https://x.com/drakefjustin), [Francesco D’Amato](https://x.com/fradamt) and [Caspar Schwarz‑Schilling](https://x.com/casparschwa) and for ideas, discussions, feedback, and contributions to the proposal.*

# Introduction

Ethereum has long pursued the goal of [stateless validation](https://stateless.fyi/): enabling participants to verify blocks without needing to store the entire state of the chain. Statelessness aims to reduce hardware requirements, promote greater decentralization among verifier nodes, and unlock scalability by allowing larger blocks to be constructed and validated without requiring all nodes to replicate the full state.

One leading proposal toward this vision is [weak statelessness](https://ethereum.org/en/roadmap/statelessness/), where only block producers retain the full state and other nodes validate blocks using small state proofs. While attractive for its simplicity and efficiency, weak statelessness raises a critical challenge: **How can Ethereum preserve its censorship resistance (CR) properties in a world where most nodes cannot independently validate transactions?**

In this post, we explore why weak statelessness, on its own, undermines Ethereum’s censorship resistance guarantees, and propose a pragmatic solution: **Validity-Only Partial Statelessness (VOPS)**. By requiring nodes to store just enough account data to validate pending transactions, **VOPS** offers a **25x storage reduction** while preserving Ethereum’s censorship resistance.

> We argue that:
>
>
> Weak statelessness alone cannot guarantee strong censorship resistance.
> Future designs must revisit strong statelessness, and address practical questions, such as who generates these proofs, what types of proofs are most efficient, and how bandwidth and proving costs impact node requirements.
> In the meantime, Validity-Only Partial Statelessness (VOPS) offers a simple and effective bridge: reducing local storage by 25x while preserving a functional, censorship-resistant public mempool.
> AA-VOPS extends VOPS to support full native account abstraction, offering a path toward strong statelessness by minimizing witness overhead through local caching and incremental updates.

# The why

We’ll start by explaining why weak statelessness (i.e., only relying on block producers to hold the state) doesn’t work well if we want to give strong censorship resistance guarantees for all transactions through mechanisms like [FOCIL](https://eips.ethereum.org/EIPS/eip-7805). Before diving deeper, here’s a quick recap of the main ingredients required for FOCIL to work in a stateful world. We’ll show how FOCIL’s current design relies on the assumption that the mempool can retain valid transactions while pruning out invalid ones:

- Users send transactions that, if valid (i.e., passing nonce and balance checks), are broadcast across nodes and remain pending in the public mempool.
Note: In this post, we use the term “node” to refer mempool maintainers via their execution layer client.
- Includers: Each slot, 16 includers observe the pending mempool transactions, add them to inclusion lists (ILs), and broadcast these ILs across the CL P2P network.
- Block producers must include the union of valid transactions from all ILs in their blocks. An IL transaction can only be excluded from the block if it is invalid or if the block is full (i.e., conditional property).
- Attesters verify whether all IL transactions are included in the block. If they are, the attesters vote for the block. Otherwise, they assess whether the block is full or whether the missing transactions were valid, in order to determine if the exclusions were justified or if the block was censoring.

Now, imagine the protocol only expects ***block producers*** to hold the state. This would mean that ***users***, ***nodes*** maintaining a mempool, ***includers***, and ***attesters*** are unable to determine if transactions are valid against the `preStateRoot` on their own. Indeed, they would lack access to the complete, up-to-date state information necessary for critical validation checks, including confirming that the sender has sufficient `balance` and that the transaction’s `nonce` is correct. *Note that any smart contract conditions or state-dependent logic (for example, the current state of a Uniswap pool) are already provided by dApps today to help **users** avoid reverts.*

So, in a weak statelessness world:

- Everything actually works out for attesters: they don’t need to store anything at all since block producers generate block-level witnesses. These witnesses can take the form of aggregated Merkle/Verkle proofs (e.g., IPA multiproofs) or even SNARKs (more on this in a section later on), which show that all state accesses made by transactions included in the block are valid against preStateRoot. In other words, they prove that the provided data for the block execution exists in the previous block state root. Importantly, block producers must also attach witnesses for any IL transactions they exclude (either using witnesses submitted alongside the ILs or by reconstructing them), so that attesters can re-execute the block and verify whether each omission was justified.
- For nodes maintaining the mempool and includers, there is a fundamental problem if we want them to be stateless. When transactions are sent to the public mempool by users, nodes have no way of knowing if these transactions are valid against the preStateRoot as they can’t perform the usual nonce and balance checks to determine whether they should rebroadcast transactions or prune them from their local mempool:

 This can be exploited to flood the mempool and ILs with invalid transactions, effectively negating the benefits of FOCIL and enabling the censorship of transactions that would have otherwise benefited from being included in ILs.
- The absence of nonce and balance checks as a first line of defense creates a new DoS vector: it allows anyone to submit invalid transactions to the mempool or ILs, degrading the quality of the mempool and making it harder for valid transactions to surface. This creates the same kind of disruption that would occur if includers were adversarial and filled ILs with garbage. The key difference is that today, only validators (with 32 ETH) can be includers, whereas without basic filtering, any participant can degrade mempool quality and interfere with inclusion list effectiveness—lowering the barrier to attack and weakening censorship resistance in practice.

# Wat do?

In the following section, we explore potential options to overcome the challenges presented by the weak statelessness approach.

## Option 1: Strong statelessness

One seemingly straightforward approach is to require that user transactions be bundled with complete state accesses against the `preStateRoot` (e.g., Merkle or Verkle proofs), often referred to as strong statelessness. We could even relax the strict definition of strong statelessness by requiring each previous ***block producer*** to attach state witnesses to every transaction, so that ***nodes*** can fetch them on demand. This would, in theory, enable any ***node***, including ***includers*** and ***attesters*** to independently verify that a transaction’s state accesses are consistent with the `preStateRoot` without needing access to the full, current state. Such a mechanism is useful for managing the mempool effectively: instead of excluding and including transactions every slot, ***nodes*** can retain transactions that remain unaffected by subsequent blocks and prune those whose nonce or balance has changed.

But in practice, it would require a real-time delivery channel between nodes and the current block producer, introducing strong trust assumptions and a new censorship vector: a block producer could delay or selectively withhold transaction-level proofs to keep targeted transactions out of every mempool and inclusion list, quietly excluding them while still producing an apparently valid block. Moreover, for new transactions, relying solely on the previous block’s state is insufficient. Users need access to updated, real-time state witnesses that include both the accounts and storage slots actually touched by the transaction, as well as any additional parts of the state trie required to reconstruct the path to those entries—due to how the trie structure interlinks state. Not only does continuously fetching these proofs increase bandwidth usage and latency—degrading UX—but it also raises a crucial question: who should serve as [proof-serving nodes](https://ethresear.ch/t/a-protocol-design-view-on-statelessness/22060)? Wallets? dApps? The Portal network? Supernodes (i.e., validators staking `2048 ETH`)? All of the above?

Although strong statelessness may be the endgame if we want attester and includer nodes to be completely stateless and run on smart watches, further research is essential to answer this question and determine which actors are best suited to perform this duty by evaluating the costs and hardware requirements needed to **(1)** store the full state and **(2)** generate and broadcast the witnesses and proofs associated with user transactions. Note that this approach only requires a one-out-of-N honesty assumption—in theory, a single honest actor capable of generating valid proofs is sufficient. However, in practice, relying on only one or very few actors could lead to issues such as rent extraction (e.g., commitment attacks, censorship, and monopoly pricing).

## Option 2: Validity-Only Partial Statelessness

A pragmatic, short‑term approach is to rely on partial statelessness and store only the minimal data needed to verify transaction validity. Under VOPS, each node maintains just four fields per EOA—`address` (20 B), `nonce` (8 B), `balance` (12 B), and a one‑bit `codeFlag`—instead of the full state.

When a transaction arrives, the node checks `codeFlag`:

- codeFlag = 0 (pure EOA, no delegation designator — meaning the account cannot delegate execution to custom code):

Verify signature, nonce, balance vs. fees, and gas limits.
- Allow multiple in‑flight transactions per address.

`codeFlag = 1` (any address capable of running code using a 23‑byte [EIP‑7702](https://eips.ethereum.org/EIPS/eip-7702) delegation designator):

- Enforce at most one pending transaction per address.
- Prevents nonce/balance conflicts as delegated code can alter state unpredictably.

On each new block, the node updates its table with all modified quadruplets, prunes any transactions rendered invalid by stale nonces or insufficient balances, drops all but the highest‑priority pending transaction whenever an account’s `codeFlag` flips from **0** to **1**, and promotes any queued EOA transactions whose nonces now match when the flag flips back from **1** to **0**.

Because each account entry is only `20 + 8 + 12 + 0.125 ≈ 40.125 bytes`, maintaining [~241 million accounts](https://stateless.fyi/development/mainnet-analysis/tree-shape.html#accounts-and-code-length-stats) requires:

241\,\text{million} \times 40.125\,\text{bytes} \approx 8.4\,\text{GiB}

That’s more than a **25×** reduction compared to today’s `~233 GiB` full‐state size (h/t Guillaume), yet still lets VOPS nodes maintain the mempool effectively. Note that the `8.4 GiB` figure is uncompressed, so it’s a pessimistic estimate of the storage savings VOPS could deliver.

### VOPS for Verkle

To make the VOPS idea concrete, we’ll start by anchoring the proposal in a **[Verkle](https://eips.ethereum.org/EIPS/eip-6800) setting**.

**Block Header Fields**

| Field | Purpose |
| --- | --- |
| preStateRoot | State root before executing the block. |
| postStateRoot | State root after execution. |
| Block-level witness (IPA multiproof, in the block body) | Proves that every state element read during execution is valid against the preStateRoot. |
| transactions | Full list of transactions. |

Let’s recap who does what in that scenario:

- Users broadcast transactions to the public mempool. Under VOPS, partial‑stateless nodes keep only four fields per account—address, nonce, balance, and codeFlag—just enough to decide whether each pending transaction should stay or be pruned.
- Includers: Each slot, 16 includers observe the pending mempool transactions, add them to inclusion lists (ILs), and broadcast these ILs across the CL P2P network. If the includer also maintains a mempool—as is the case today—no additional checks are needed before including transactions in ILs, since validity checks against the preStateRoot (e.g., nonce, balance, and codeFlag) are performed as part of mempool maintenance. However, if in the future includers are separated into a standalone role (e.g., light “smart-watch” includers), they will need to independently perform transaction validity checks before including transactions in ILs.
- Block producers hold the full Ethereum state. They must include the union of all valid transactions from all ILs in their proposed blocks. An IL transaction can only be excluded if it is invalid or if the block is full (i.e., the conditional property is satisfied).
 In a VOPS for Verkle world, block producers are responsible for generating and committing the following:

A block-level witness (e.g., an IPA multiproof over a Verkle tree): This proves that the provided data for the block execution exists in the previous block state root.
- Post-state root: After executing all transactions, the block producer computes and commits the resulting postStateRoot in the block header. This serves as the output of execution and must be verified by attesters. This is already what block producers do today, and wouldn’t be a new requirement in a VOPS world.

***Attesters*** verify the block by performing the following steps:

1. Verify the block-level witness: Confirm that all the provided state (proven via the IPA multiproof) are valid against the preStateRoot.
2. Re-execute the block locally: Using the provided transactions, attesters independently re-execute the block starting from the pre-state (reconstructed from the witness) to recompute the postStateRoot.
3. Check the postStateRoot: Ensure that the locally recomputed postStateRoot matches the one committed in the block.
4. Validate IL conditions

- Included IL transactions

During local re-execution from the reconstructed pre-state, all state changes corresponding to IL transactions present in the block can be observed.

**Excluded IL transactions**

- After executing all included transactions in the block, attempt to execute each excluded IL transaction:

If the transaction would fail nonce or balance checks, or if the block was full, the exclusion is justified.
- Otherwise, the block producer is censoring and the block should not receive a vote.

If all checks pass—validity of state access, correctness of execution, and satisfaction of IL conditions—**attesters vote for the block**. By re-executing blocks in **step 2** and simultaneously updating their local quadruplet tables in **step 3**, VOPS nodes keep their partial state perfectly in sync without ever storing the full Verkle tree.

### VOPS for zkVMs

Building on the Verkle flavour of VOPS, we can replace block‑level state proofs and local re‑execution with a zero-knowledge Virtual Machine (**zkVM)**. Each block would come with a **SNARK** that lets every verifier check the whole transition—and all IL conditions—by running a single, millisecond‑scale verification.

- What block producers must prove:

State validity: Every key/value read by transactions is proven against the preStateRoot.
- Execution correctness: Executing the ordered transactions over that reconstructed pre-state yields the committed postStateRoot.
- Diff correctness: Applying the correct full state diff to preStateRoot yields postStateRoot, and the diff matches the one embedded in the header.

**Block Header Fields**

| Field | Purpose |
| --- | --- |
| preStateRoot | State root before execution |
| postStateRoot | State root after execution |
| stateDiff | Merkle root of the complete list of every modified account leaf and storage slot |
| execProof | SNARK binding transactions + stateDiff to the transition preStateRoot → postStateRoot |

> Two notes:
>
>
> Under VOPS and AA‑VOPS, nodes rely on receiving the full stateDiff per block to patch their local state. EIP-7928 Block-Level Access Lists (BALs) would provide exactly this: a verifiable, enforced publication of all modified accounts, storage keys, balances, and nonces.
> IL compliance is checked locally by VOPS nodes using their updated quadruplet tables and the received stateDiff—no extra proof obligation here (see AA-VOPS for where per-account proof ties into inclusion-list rules).

**Block-by-block routine for VOPS nodes**

1. Verify execProof. Confirms  state validity,  execution correctness, and  diff correctness.
2. Extract quadruplets. From the verified full stateDiff, pull out each modified account’s (address, nonce, balance, codeFlag) and update the local table.
3. Enforce IL rules. Using the refreshed quadruplet table, re-check inclusion-list conditions locally. IL enforcement can be done out-of-the-proof using local checks with the stored VOPS-quadruplet fields.
4. Prune the mempool. Drop any pending transaction invalidated by the new quadruplet values.

**Resource profile**

| Aspect | Node | Block producer |
| --- | --- | --- |
| Disk | ≈ 8.4 GiB for the quadruplet table (≈ 25× smaller than full MPT state) | Unchanged |
| Bandwidth | stateDiff adds only a few tens of KB—negligible vs. current block limits | Almost unchanged, but a bit more upload bandwidth for witnesses |
| CPU | One fast SNARK verification per block (milliseconds on a laptop) | Heavy proving workload—still a lot costlier (multiple GPUs) than building Merkle/Verkle witnesses, though improving quickly |
| Proof size | Constant-size, verifiers always download the same few hundred bytes | Constant-size, ideally aiming for 128-256 KiB per proof |

**Bottom line.**

With ≈ 8.4 GiB of local state, unchanged mempool rules, and a single succinct proof per block, zkVM VOPS preserves Ethereum’s censorship-resistance while keeping verifier hardware requirements within consumer-grade limits.

### VOPS Syncing

Let’s start with an important note. In today’s [Verkle](https://eips.ethereum.org/EIPS/eip-6800) and [Binary tree](https://eips.ethereum.org/EIPS/eip-7864) proposals, accounts and storage slots are interleaved, unlike the Merkle Patricia Tree where accounts form a distinct subtrie. A VOPS node cannot reliably tell accounts apart from storage slots, and cannot simply download a snapshot to rebuild its local account table. Most isolated slots (>80%) can be filtered, but attackers could create fake account-like slots to slow down syncing. Syncing from genesis does not solve this, since current witness formats do not indicate whether a value is an account or a storage slot. Solving this would require richer witness formats, such as those proposed for block-level access lists, or small changes to the tree structure.

Today, the account trie represents roughly `1/6` of the total state size. Assuming a snap sync approach, downloading just the account trie would make syncing about five to six times faster compared to downloading the full state, accounting for the healing phase. The healing phase would still take the same time as today, and much of the downloaded data would eventually be discarded, but syncing could happen from any full node, just like today.

Bootstrapping a VOPS node requires **only accounts state** (no storage tries or code blobs) along with the usual block headers:

1. Header download and verification

Fetch and verify block headers from genesis (or a trusted checkpoint) to the latest head.
2. Block-by-Block Updates
 For each new block:

Retrieve:

Verkle-tree: header + IPA multiproof + full transaction list
3. zkVM: header + SNARK execProof + compact stateDiff sidecar
4. Verify & Extract:

Verkle-tree: check the multiproof, extract all touched account entries, then re-execute every transaction in order against that reconstructed pre-state. Record each changed (address, nonce, balance, codeFlag).
5. zkVM: verify the SNARK (state reads, execution, and IL rules) and parse the stateDiffsidecar list of updated quadruplets.
6. Apply: update the local table with each modified account entry.
7. Mempool Pruning

Upon each table update, drop any pending transaction whose sender now has a stale nonce, insufficient balance, or a codeFlag flip from 0→1 (retaining only the highest-priority pending tx for that address).
8. After processing all blocks to the head, the table is fully current and the mempool enforces valid-only admission/pruning exactly as in live operation.

## VOPS and Native Account Abstraction (AA‑VOPS)

**Native Account Abstraction (AA, see [EIP-7701](https://eips.ethereum.org/EIPS/eip-7701))** introduces a major paradigm shift: accounts are no longer simple objects with fixed validation rules, but programmable entities that can run arbitrary code. This flexibility breaks the assumption that checking just the `nonce`, `balance`, and `codeFlag` is enough to validate a transaction. As a result, VOPS needs an upgrade: **AA-VOPS**.

AA-VOPS extends VOPS to support native AA while keeping nodes lightweight, by avoiding full global state replication. Instead of requiring every node to track every account, each node only tracks the accounts it actively cares about (for its own EOAs or ones it interacts with), maintaining a small local cache that is updated incrementally over time.

While native AA unlocks powerful new capabilities, it also forces the ecosystem closer to strong statelessness designs, where transactions must carry explicit witnesses. As we extend VOPS to support AA-VOPS, we should carefully weigh whether the benefits of full native AA justify this added complexity, or if sticking to a simpler VOPS model better preserves decentralization and efficiency.

### AA-VOPS vs Strong Statelessness

**Strong statelessness** expects users to attach a full state witness to every transaction, covering all touched accounts and storage slots.

In contrast, **AA-VOPS** allows nodes to maintain up-to-date proofs only for specific accounts tied to their own EOAs. These proofs stay valid across multiple blocks unless the account changes and are refreshed using lightweight `stateDiffs` included with each block.

This avoids bulky witnesses on every transaction, keeping bandwidth and storage requirements minimal while preserving censorship-resistance and transaction validity.

### How AA-VOPS Work

**Local Cache and Witness Maintenance**

A node (or a wallet or dApp backend acting on its behalf) keeps:

- Its own account leaf: nonce, balance, storageRoot, and codeHash.
- Any extra storage slots required by the account’s AA logic.
- A Merkle or Verkle path witness authenticating these fields against a recent stateRoot.

The witness remains valid until a later block modifies any of the covered fields.

**Bootstrapping the witness:**

- The node obtains the initial leaf and path once, using eth_getProof from any full node or RPC provider (in Reth, you can now get all the witnesses with a single RPC call).

**Incremental updates:**

Every block provides

1. A compact, full stateDiff (as in VOPS-with-zkVM).
2. An IL commitment (e.g., an aggregate of the 16 IL signatures). This commitment allows attesters to verify that the block producer committed to all ILs they observed locally.
3. A block-level proof (e.g., a SNARK) binding the transactions, the stateDiff, and the IL compliance rules together.

When a block arrives, the node:

1. Verifies the block-level proof, which ensures:

The stateDiff correctly encodes the transition from preStateRoot to postStateRoot.
2. All included transactions are executed correctly.
3. Each transaction in the IL set was either included or validly excluded (because the block was full or the transaction became invalid after prior execution).
4. Patches its witness if needed:
 The VOPS node (or a wallet/dapp tracking its own EOAs) checks if any of its accounts appear in the stateDiff.

If present, it updates the cached leaf and recomputes affected Merkle/Verkle paths.
5. If absent, the cached witness remains valid against the new stateRoot.

If a node stays online and processes every block, it never needs another archive query after bootstrapping. If it falls behind, it can replay missing diffs or reseed its witness via `eth_getProof`.

### Transaction Packaging

When submitting a transaction:

- For EOAs and EIP-7702 accounts, no additional witness is needed. The minimal account fields are locally available.
- For EIP-7701 smart accounts, a succinct single-account validity proof (e.g., a SNARK) is attached, showing both inclusion of the account leaf and correct VALIDATE logic execution.

### Future AA compatibility

If future AA standards allow `VALIDATE` to read outside the account, the sender can widen the attached witness to cover those additional storage slots. The model extends naturally.

**Mempool Admission**

A receiving node verifies the witness or proof against the referenced `stateRoot`, using its cached `stateDiffs` to check for updates:

- If the diffs show the account has not changed, the transaction is accepted.
- If the diffs indicate the account has changed, the witness is stale and the node requests an updated proof.

In practice, nodes could also maintain a sliding window of recent stateDiffs—e.g., the last ~N blocks—to allow for transaction validation without re-querying.

### Why AA-VOPS is Compelling

- No global replication:
 Each node stores only a few kilobytes, not 8 GiB (VOPS) or ~233 GiB (full state). Block producers and RPC providers still need the full state.
- AA compatibility:
 Works with EIP-7701 today and can adapt if validation logic later reads external storage.
- On-demand bootstrapping:
 To track a new EOA, a node fetches a single eth_getProof once and keeps it fresh with diffs.

### Trade-offs

1. Higher P2P bandwidth:
 Every transaction carries its own witness or succinct proof, growing average transaction size (~736 bytes for Verkle, ~1024 bytes for binary trees).
2. User-side proving or fetching:
 Nodes must keep proofs current by tracking diffs or querying a full node, which is prone to centralization vectors.
3. Dependency on full nodes for bootstrapping:
 Unlike VOPS, AA-VOPS depends on full nodes or RPC providers to initially fetch account proofs. If missing diffs, nodes must reseed via eth_getProof, potentially introducing centralization risks if few providers dominate.

## Conclusion and takeaways

**Validity‑Only Partial Statelessness** (**VOPS**) reduces local storage requirements for nodes to roughly 8.4 GiB uncompressed—just the `(address, nonce, balance, codeFlag)` quadruplets—while preserving Ethereum’s censorship‑resistance properties. This approach leverages the asymmetry between account and storage-slot growth: as long as storage continues to dominate new state entries, the savings remain substantial; should account creation ever outpace storage growth, the relative advantage would diminish accordingly.

There are two main advantages to VOPS in its original version: The first is a witness-free mempool: because every node stores each EOA’s `(address, nonce, balance, codeFlag)` quadruplet, the mempool never needs per-transaction Merkle or Verkle proofs. Block-level proofs (for example, SNARKs in a zkEVM) still guarantee full correctness while adding only a few hundred bytes to each block’s propagation. The second is truly peer-to-peer syncing: since every node maintains that minimal state for all EOAs, you can bootstrap or restore from any peer without needing additional proofs or individual account data, eliminating reliance on full or archive nodes.

But supporting native AA pushes us toward a different set of trade-offs. AA-VOPS cuts local storage to just a few kilobytes by attaching a small, up-to-date proof to each transaction, but the downside is higher P2P payloads and occasional calls to a full node or dedicated service whenever you start tracking a new account, bootstrap a node, or come back online after being offline. As proving technology and SNARKs continues to improve, AA-VOPS could become the long-term, future-proof route to full statelessness. The original VOPS, by contrast, stands out as a pragmatic short-term solution, preserving seamless UX by avoiding transaction-level witnesses.

## Replies

**morph-dev** (2025-04-30):

I want to propose alternative approach, in a context of Weak statelessness.

What if transactions would come with a regular Merkle Proof on a Verkle/Binary trie (not aggregated one, i.e. IPA multiproof). Wouldn’t the **nodes** and **Includers** be able to maintain that proof across blocks solely based on block’s execution witness?

Instead of keeping them separately, we can optimize storage and computation by keeping partial Verkle trie locally (partial only enough to cover all accounts associated with transaction in their mempool). Every transaction that enters mempool would have enough data to expand partial view.

If we assume that **nodes** are going to store X recent blocks (relatively small number) and their execution witness, then transaction that are sent by **Users** could be lagging few blocks behind head of the chain, and **nodes** would still be able to updated their proofs. That mean that **Users** could obtain these proofs from sources that don’t have to be as *fast*, e.g. Portal Network.

This could be explored in the context of Strong statelessness, but my intuition tells me that Verkle proofs would be too big for this to be practical. However, that might not be the problem for Unified Binary Trie.

---

**pipermerriam** (2025-05-01):

I believe that Portal is well positioned to provide solutions and options for a few things in this proposal.  Our state network plans are roughly as follows.

Current stage implements a full archival model that serves the Ethereum state in the format of individual trie nodes.  This model will be available up to the latest finalized block.  This stage should be complete before the end of this year.

Once the first stage is live we will begin on the second stage which stores the state at the head of the chain.  This model uses a “flat” access model allowing direct lookup of leaf data with an O(1) lookup cost.  The in progress spec for this model can be found [here](https://github.com/ethereum/portal-network-specs/pull/389)

With both of these live, the Portal state network should be capable of doing the following things.

- Supporting initial sync of the compressed state for VOPS nodes.
- Bootstrapping witnesses for AA-VOPS nodes.
- Removing dependencies of full nodes for eth_getProof. Any place where eth_getProof is used, it should be viable to use Portal state network at the cost of higher latency.

We are currently already building towards a model in our state network that is based on pushing out state diffs at each block.  There seems to be a lot of overlap in the proving primitives that are needed for this VOPS design and what Portal needs for state network.  We are also very pro-verkle as the unified trie design benefits Portal greatly.

---

**soispoke** (2025-05-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/morph-dev/48/14323_2.png) morph-dev:

> What if transactions would come with a regular Merkle Proof on a Verkle/Binary trie (not aggregated one, i.e. IPA multiproof). Wouldn’t the nodes and Includers be able to maintain that proof across blocks solely based on block’s execution witness?

If transactions come with merkle or verkle/binary proofs, this isn’t weak statelessness anymore, but yes nodes and includers would be able to maintain the mempool in that case. What you describe is really close to the AA-VOPS design suggested in the post.

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> With both of these live, the Portal state network should be capable of doing the following things.
>
>
> Supporting initial sync of the compressed state for VOPS nodes.
> Bootstrapping witnesses for AA-VOPS nodes.
> Removing dependencies of full nodes for eth_getProof. Any place where eth_getProof is used, it should be viable to use Portal state network at the cost of higher latency.

This is great! I think having an actual practical solution for VOPS nodes to access state via Portal, including fresh/head of the chain state is what’s needed in case we go towards AA-VOPS for sure.

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> We are currently already building towards a model in our state network that is based on pushing out state diffs at each block.

I’m guessing [Block-level Access Lists](https://github.com/ethereum/EIPs/pull/9580) would help/simplify things on this particular point?

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> Removing dependencies of full nodes for eth_getProof. Any place where eth_getProof is used, it should be viable to use Portal state network at the cost of higher latency.

Agreed. Even if Portal has slightly higher latency than full-node RPCs, just having a decentralized fallback could make a real difference especially if you can default to Portal automatically if/when needed.

---

**yoavw** (2025-05-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/soispoke/48/12076_2.png) soispoke:

> Local Cache and Witness Maintenance
>
>
> A node (or a wallet or dApp backend acting on its behalf) keeps:
>
>
> Its own account leaf: nonce, balance, storageRoot, and codeHash.
> Any extra storage slots required by the account’s AA logic.
> A Merkle or Verkle path witness authenticating these fields against a recent stateRoot.
>
>
> The witness remains valid until a later block modifies any of the covered fields.

The validation data for an account may include `codeHash`, `storageRoot` and storage slots for more contracts, if they’re accessed during the account’s validation. For example, modular accounts (ERC-6900 and ERC-7579) may access a number of validation modules.

In addition, if a paymaster contract pays for the gas, then the transaction’s validity also depends on the code and storage of that paymaster.

Caching should be quite effective here.  My understanding is that a light node would typically serve a single user or a small number of users sending transactions.  The validation data of an account seldom changes (e.g. key rotation).  The node would seldom have to refresh its proof.

The exception to this is paymasters, as they’re used by a large number of users and their balance keeps changing.  If the nodes’ users frequently use a certain paymaster, the node may end up getting new proofs for it frequently.  In the most common case this will be just the balance, but in some cases it’ll also involve storage changes (e.g. user uses TokenPaymaster to pay with USDC, so the USDC contract’s `storageRoot` becomes a dependency.  The user’s USDC balance slot may not change frequently but the proof will change every block because others transact with USDC.

To reduce latency in that case, would it make sense for the node to maintain a list of frequently accessed contracts (e.g. TokenPaymaster+USDC) and keep refreshing their state from Portal network?

![](https://ethresear.ch/user_avatar/ethresear.ch/soispoke/48/12076_2.png) soispoke:

> Agreed. Even if Portal has slightly higher latency than full-node RPCs, just having a decentralized fallback could make a real difference especially if you can default to Portal automatically if/when needed.

I think it’s important to use Portal, at least as fallback to reduce dependency on full nodes.  Ideally the node should preemptively refresh the state of the accounts it frequently uses (frequently used user accounts and their dependencies, frequently used paymasters and their dependencies).

[@pipermerriam](/u/pipermerriam) how much latency does it add?  And since we know which contracts the light node uses most frequently, would it make sense to preemptively refresh them, or will it put too much burden on Portal?

---

**sina** (2025-05-13):

Very interesting proposal! I’ve been struggling to square how scaling L1 execution can be compatible with FOCIL and similar anti-censorship gadgets that rely on a broad attestor set, and this is a very interesting angle for a solution. ![:grin:](https://ethresear.ch/images/emoji/facebook_messenger/grin.png?v=12)

One way I’m understanding this, feel free to correct me, is that we’re effectively decomposing the L1 state into two types:

1. “account state”, which we expect “everyone” (nodes) to be able to effectively download/verify/index due to its necessary dissemination for effective CR gadgets
2. “full state”, which we don’t expect as wide of access (~block producers only)

I’m concerned there’s a lot of hidden complexity around maintaining two such state types- potentially different metering, bandwidth constraints, and limits will be required. Thinking adversarially, I could imagine a world where an insidious block producer bloats the total size of the “account state” or the size of the block-to-block diffs to purposely deteriorate the ability of nodes to keep up. To avoid this I believe you’d need to effectively meter “account state” separately, considering things like a total size limit, state rent, a diff size limit per block, or similar. While you get the benefit of “one global state” in some senses, the protocol will have to effectively manage two separate resources.

I’m curious about the benefits we get for this complexity compared to the status quo of having an execution layer with a “full state” metered to be downloaded, executed, and indexed by all nodes instead of just builders (eg. philosophically ~what we have now) which acts as the backstop layer for CR, and then have the “rolled-up” flavors of state sitting on top as explicitly separate-but-connected domains (philosophically ~what enshrined L2s would be)?

Most relevant to this post, keeping a small-node-friendly-fullstate-layer grants simpler protocol management of distinct state resources (similar to the current L1 vs L2 dynamic we see today) as well as more accessible block building (don’t need to be a prover). The main advantage I see to the VOPs design is that we can scope down the small-node-friendly-state to focus only on what’s needed to validate transactions rather than arbitrary state types as we see today, potentially resulting in more accurate metering if we can effectively design around attack and griefing vectors. I’m curious though to hear about other angles that I may not be considering.

---

**soispoke** (2025-05-13):

Thanks for your feedback and comments!

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavw/48/6142_2.png) yoavw:

> To reduce latency in that case, would it make sense for the node to maintain a list of frequently accessed contracts (e.g. TokenPaymaster+USDC) and keep refreshing their state from Portal network?

The paymaster case is definitely one I didn’t have in mind. After our discussion and thinking more about your comments, I’m still quite concerned about nodes having to rely on external services to keep their proofs up-to-date. I agree Portal can be an option in theory, but we would need a lot more certainty about the viability of this option (e.g., the latency) to make sure we don’t end up having all nodes just fetching from centralized providers. We might also need to start thinking about alternatives to Portal anyways, for example we could ask all nodes that stake 2048 ETH to be stateful and provide state, or wallets and dApps to be responsible for providing state to their users.

![](https://ethresear.ch/user_avatar/ethresear.ch/sina/48/11475_2.png) sina:

> Very interesting proposal! I’ve been struggling to square how scaling L1 execution can be compatible with FOCIL and similar anti-censorship gadgets that rely on a broad attestor set, and this is a very interesting angle for a solution.

Thanks!

![](https://ethresear.ch/user_avatar/ethresear.ch/sina/48/11475_2.png) sina:

> Thinking adversarially, I could imagine a world where an insidious block producer bloats the total size of the “account state” or the size of the block-to-block diffs to purposely deteriorate the ability of nodes to keep up.

I think this definitely need to be kept in mind, but I don’t think it’s necessarily a concern. Imagine a case in which a block producer bloats the block-to-block diff: If attesters are not able to download the diff they wouldn’t actually vote for the block (assuming we make it a fork choice enforced condition), which would ultimately hurt the block producer.

![](https://ethresear.ch/user_avatar/ethresear.ch/sina/48/11475_2.png) sina:

> the protocol will have to effectively manage two separate resources.

I think that’s right, but it’s the case with any statelessness proposal right? You have to have some stateful nodes (e.g., block producers), in order for some other light stateless nodes (e.g., attesters, includers) to be a possibility. VOPS is just one instantiation of this, proposing that light nodes should still hold the state that’s necessary for maintaining a healthy mempool.

![](https://ethresear.ch/user_avatar/ethresear.ch/sina/48/11475_2.png) sina:

> I’m curious about the benefits we get for this complexity compared to the status quo of having an execution layer with a “full state” metered to be downloaded, executed, and indexed by all nodes instead of just builders

Imposing all nodes to be stateful like today might just not be possible if we both (1) want to increase the gas limit and (2) ensure some nodes can participate in attesting and in CR without needing high hardward requirements.

![](https://ethresear.ch/user_avatar/ethresear.ch/sina/48/11475_2.png) sina:

> The main advantage I see to the VOPs design is that we can scope down the small-node-friendly-state to focus only on what’s needed to validate transactions rather than arbitrary state types as we see today, potentially resulting in more accurate metering if we can effectively design around attack and griefing vectors.

Yeah that’s the main advantage I see as well ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**pipermerriam** (2025-05-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavw/48/6142_2.png) yoavw:

> @pipermerriam how much latency does it add? And since we know which contracts the light node uses most frequently, would it make sense to preemptively refresh them, or will it put too much burden on Portal?

Latency for accessing a single account can be projected as

- A: time to navigate the network to find the nodes that store the account
- B: time to retrieve the account

For A, clever clients should be able to do this in well under 500ms.  There’s lots of shortcuts and optimizations for DHT navigation so this number should be able to be reduced under 200ms if the client is willing tot do some work to cache a larger view of the network.

For B, account data is small so another few hundred milliseconds.

I think it’s probably reasonable to have average cases be less than 1s for random access lookups, and probably less than 500ms for things that are regularly accessed.

As for things like pre-emptive refreshing of a frequently accessed account, I expect this should be fine.  There’s also probably a few different routes to doing this by either fetching the data regularly… or by keeping it up-to-date yourself with block level state diffs being gossiped around the network.

---

**sina** (2025-05-14):

Appreciate the reply [@soispoke](/u/soispoke) ![:grin:](https://ethresear.ch/images/emoji/facebook_messenger/grin.png?v=12)![:pray:](https://ethresear.ch/images/emoji/facebook_messenger/pray.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/soispoke/48/12076_2.png) soispoke:

> sina:
>
>
> Thinking adversarially, I could imagine a world where an insidious block producer bloats the total size of the “account state” or the size of the block-to-block diffs to purposely deteriorate the ability of nodes to keep up.

I think this definitely need to be kept in mind, but I don’t think it’s necessarily a concern. Imagine a case in which a block producer bloats the block-to-block diff: If attesters are not able to download the diff they wouldn’t actually vote for the block (assuming we make it a fork choice enforced condition), which would ultimately hurt the block producer.

It sounds like we’re in agreement here that the protocol will have to consider such edge cases that effectively make account-state and full-state different resources with unique limits and metering. I’m a bit more worried about the “hidden complexity” that comes with this though, as I put it in my original reply. I’ll try to illustrate some more angles here.

![](https://ethresear.ch/user_avatar/ethresear.ch/soispoke/48/12076_2.png) soispoke:

> sina:
>
>
> the protocol will have to effectively manage two separate resources.

I think that’s right, but it’s the case with any statelessness proposal right?

At risk of going a bit off-topic to poke at statelessness more generally, do you have any concerns around the protocol having resources that functionally behave differently and are metered/limited differently but have a unified interface leading to patterns forming on top that poorly abstract over the unique features of the resources anyway?

For example, would an application or usecase decide it wants to use account balances/nonces as a type of pseudo-storage because of the “stronger properties” it affords (more widely accessible/indexed)? I can imagine a similar dynamic that goes the other way too-- certain state that should otherwise be considered account state ends up in some form in the non-account-state to arbitrage any gain that falls out of the different metering, degrading the original intent behind the design.

To me the ideal way to design around this is to decide which resources make sense for the protocol to expose and then simply expose them as purely as possible with expressive interfaces, letting the ecosystem adjust to the unique metering of different resources in a more “natural” way. Zooming back in to VOPs, this means being able to cleanly express whether the “state” I’m targetting is all-nodes or super-nodes-only state, and knowing how I’m charged/metered for it without thinking of more complex extraprotocol patterns meant to hack/arbitrage the design.

I’m not saying that it’d be impossible to design a robust system that achieves the properties we want, but my worry is that by relying on misdirection-via-unified-interface to try to make both resources feel like one, we’ll just end up with hacky meta-interfaces to the unique resources that mirror what we should’ve done in the first place.

![](https://ethresear.ch/user_avatar/ethresear.ch/soispoke/48/12076_2.png) soispoke:

> sina:
>
>
> I’m curious about the benefits we get for this complexity compared to the status quo of having an execution layer with a “full state” metered to be downloaded, executed, and indexed by all nodes instead of just builders

Imposing all nodes to be stateful like today might just not be possible if we both (1) want to increase the gas limit and (2) ensure some nodes can participate in attesting and in CR without needing high hardward requirements.

The reason I highlight the status quo is because I think when you compare it through a VOPs-ish lens it actually achieves pretty desirable properties while maintaining pure and expressive interfaces to the underlying resources. Depending on how specific scaling the L1 is to mean “more synchronously accessible L1 state”, the status quo via L2s effectively gives us more state that is opt-in by large builders and accessible asynchronously.

I’m sure there are more angles and smarter framings than I’m identifying, which I’d love to better understand; here’s a snapshot of my current perspective:

| Facet | VOPs | Status Quo L1 + L2 |
| --- | --- | --- |
| Metered-to-be-widely-downloaded state | Account state, only what’s needed to maintain a healthy mempool | L1 state, everything needed to progress L1 |
| Larger, cheaper, but sparsely downloaded state | The rest of the L1 state, needed to progress L1 | L2 state-- customizable on top of the pure resources the protocol offers, opt-in, not required for progressing L1 |
| Purity of interfaces to resources | TBD but probably low based on our above agreement on unique metering required for account state despite the unified interface | Highly pure, though things like limits, metering, rent, etc. will evolve and could always be better |
| Concentrates block building | Yes for the L1 (requires proving and state that is explicitly metered to be large) | No for the L1, yes for L2s (which are opt-in) |
| Interop between “small” and “large” state | Synchronous, it’s all just L1 state | Async is easy (cross-L2 calls), sync is TBD; relies on playing out rollup-verify opcodes and similar frontier research |
| Compatibility with the broader statelessness research direction | Medium-high (open questions but designed with statelessness from the ground up) | Low-medium (not designed with statelessness in mind but more battle-hardened patterns) |

---

**yoavw** (2025-05-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> For A, clever clients should be able to do this in well under 500ms.

The problem is that account validation may depend on multiple contracts.  E.g. modular accounts (ERC-6900, ERC-7579) typically access a few.  When refreshing the cache, the client already knows the dependencies and can fetch them in parallel unless a dependency has changed.  But on first access they’ll have to be fetched sequentially, leading to high latency.

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> For B, account data is small so another few hundred milliseconds.

I hope portal can fetch the required subset of the account’s state rather than the entire account data.  It’s not always small.  For example if the wallet uses the USDC TokenPaymaster to pay for the gas, then the node needs the user’s USDC balance (small data) but the entire USDC contract’s state is quite big.  Does portal’s state network operate at the account level, or the slot level?

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> As for things like pre-emptive refreshing of a frequently accessed account, I expect this should be fine.

Considering the above (e.g. modular accounts accessing a number of contracts during validation), pre-emptive refreshing may be required.

---

**pipermerriam** (2025-05-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavw/48/6142_2.png) yoavw:

> Does portal’s state network operate at the account level, or the slot level?

Slot level.  Everything in portal is designed for granular low level access patterns.

---

**MicahZoltu** (2025-06-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/soispoke/48/12076_2.png) soispoke:

> Users send transactions that, if valid (i.e., passing nonce and balance checks), are broadcast across nodes and remain pending in the public mempool.
> Note: In this post, we use the term “node” to refer mempool maintainers via their execution layer client.

I think this is an incorrect definition of a user, or we need to define a new type of user that is far more common than the one defined here.  What is described here is a Bitcoin user at best, though even on Bitcoin people need ways to check their balances.

In Ethereum, people are interacting with contracts and those contracts have state, and reading that state is very frequently a soft requirement for interacting with the protocol and often a hard requirement.  In order to meaningfully generate a transaction, a user needs the ability to read current state/balances from one or more contracts in order to correctly construct a transaction which they then publish.

Unless I’m missing something (I’ll admit, I didn’t read whole post in great detail), this post seems to start the thinking/discussion from after the point where the user has already constructed a valid transaction and it describes how that whole flow would work end-to-end.  Unfortunately, none of this is useful if users cannot actually construct valid transactions in the first place!

The core issue (IMO) when it comes to state is that end-users (as a group) need access to a significant portion of state in order to interact with Ethereum in meaningful ways.  This is an assertion that I don’t believe we can remove.  There may be solutions (and I think there are) that allow us to reduce the set of state that a user needs to store for *their* interactions, and reduce the size on disk of that state.  There are also more theoretical solutions that would allow users to interact with state held by third parties without those third parties being aware of what state is being accessed (FHE with noise or erasure coding or something).

Any discussion that involves talking about how to mitigate state growth must address this core issue in order for the solution to be useful for mitigating the real harms caused by state growth.

---

**soispoke** (2025-06-23):

Thanks for your feedback!

I think you’re referring to a problem that’s different than what VOPS aims to solve.

VOPS gives a solution to avoid having witnesses attached to all transactions in a stateless world while retaining the CR properties we get from maintaining a healthy public mempool.

You’re asking what state end users should store in order to craft valid transactions in the first place especially for transactions more complex than simple transfers (for which tracking the nonce and balance fields of your own accounts might suffice). One answer could be that users should store the state related to the contracts they care about /are interacting with (e.g., a given Uniswap pool).

But then the more difficult question becomes: where and how should they obtain that state in the first place? I agree we don’t have good answers for that yet. I think ideally it could be a combination of users storing the state themselves, but also maybe dApps, wallets, “supernodes” (e.g., that are staking 2048 ETH), a decentralized Portal like network…

Let’s say we asked users to be the ones having to store the state they care about, would you see a big issue with that?

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> There are also more theoretical solutions that would allow users to interact with state held by third parties without those third parties being aware of what state is being accessed (FHE with noise or erasure coding or something).

I’m not really aware of these solutions, they definitely seem interesting but a bit far from being efficient/practical. Still if you have some references would love to look into it more.

---

**MicahZoltu** (2025-06-23):

Ah, I see.  What you are proposing here is a mechanism that allows a person to prove that their transaction is valid (and thus eligible for mempool inclusion) without the recipient needing to hold all of the state necessary to execute that transaction?

---

**soispoke** (2025-06-24):

No, here is a mechanism that specifies what state nodes maintaining a mempool, FOCIL includers, and attesters should store to guarantee CR is preserved without having to attach transaction-level witnesses. Like you said this isn’t really about end users, more about what nodes with protocol duties should do.

Instead of asking users to generate witnesses every time to prove that their transaction is valid (and should be kept in the mempool), you ask nodes to store the minimal state necessary to determine whether a txn is valid or not.

- If users only want to do transfers, all they need to store is the balance, nonce, codeflag fields associated with their accounts.
- If they want to interact with contracts, then they need to store the state associated with these contracts to construct these transactions.
- If they want to do send native AA txns (e.g., 7701) and benefit from the CR FOCIL provides, they will probably need to only store state and generate witnesses for any state they access during the validation phase (they witnesses still wouldn’t have to include VOPS fields so they would be more lighweight)

