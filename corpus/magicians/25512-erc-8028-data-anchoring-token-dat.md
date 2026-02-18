---
source: magicians
topic_id: 25512
title: "ERC-8028: Data Anchoring Token (DAT)"
author: HenryRoo
date: "2025-09-18"
category: ERCs
tags: [erc, token, data, sft, ai]
url: https://ethereum-magicians.org/t/erc-8028-data-anchoring-token-dat/25512
views: 565
likes: 18
posts_count: 16
---

# ERC-8028: Data Anchoring Token (DAT)

## Data Anchoring Tokens (DAT): Usage-Metered Revenue Distribution for AI Assets

The Data Anchoring Token (DAT) standard represents a paradigm shift in tokenizing AI assets by unifying three essential properties into a single token structure: ownership certificates, usage rights, and value share. Unlike general-purpose NFTs or fungible tokens, DAT is purpose-built for the dynamic, evolving world of decentralized AI through its class-based architecture, value-based metering system, and on-chain verifiability.

## Token Architecture

**Semi-Fungible Token Structure**

[![](https://ethereum-magicians.org/uploads/default/optimized/3X/0/6/06e6b27627b095adee6e15f191ba17a3ed4e6732_2_690x385.jpeg)1496×836 80.6 KB](https://ethereum-magicians.org/uploads/default/06e6b27627b095adee6e15f191ba17a3ed4e6732)

Each DAT is a comprehensive primitive carrying multiple integrated components:

**Core Identity**

- id (uint256) - Unique token identifier for each specific AI asset
- name (string) - Human-readable token name
- description (string) - Detailed token description
- class (uint256) - Asset category classification (Dataset: 0x01, Model: 0x02, Agent: 0x03, etc.)

**Asset Provenance**

- url (string) - Privacy data location on decentralized storage
- hash (string) - SHA256 hash of raw content for integrity verification
- owner (address) - Token owner’s wallet address
- timestamp (uint256) - Creation timestamp on blockchain

**Economic Properties**

- value (uint256) - Dual-purpose metric representing both data quality and service credit
- quota (uint256) - Optional usage limit; data becomes inaccessible when exhausted
- shareRatio (uint256) - Revenue entitlement in basis points (e.g., 500 = 5%)
expireAt (uint256) - Optional expiration timestamp for time-bound licenses

**Access Control & Verification**

- permissions (Permission struct) - Wallet address and public key mapping for data access control, typically requiring staking to prevent fraud
- proof (Proof struct) - Authenticity verification containing token ID, quality score, file URL, and proof URL from TEE/ZK/OP verification
- verified (boolean) - Verification status flag

**Usage Tracking**

- metrics (mapping) - Records AI process interactions with account addresses and usage type/count for inference, training, or RAG queries Usage Tracking

## VALUE Semantics: Dual-Function Economic Model

### 1. Service Usage Credits

The `value` field represents service credit. Each DAT has an initial value, which is usually evaluated by the validator node of the corresponding iDAO based on the quality, uniqueness, and relevance of the data. This creates a quality gate: users cannot upload data that is completely irrelevant to the iDAO or is of low quality, which would result in a very small initial value of DAT.

**Value Consumption Model:**

- Charged per AI process invocation (training/inference)
- Deducted for dataset/model usage
- Can be recharged through AI processes
- Recorded on-chain for complete traceability

**Example**: A DAT with `CLASS = 0x03` (Agent) and `value = 1000` enables 1000 model invocations or equivalent compute resources.

### 2. Fractional Ownership & Revenue Distribution

For dataset and model DATs, value also represents fractional ownership stakes, enabling automatic revenue distribution:

- Model usage by other agents triggers proportional income splits
- Dataset contributors earn shares when data is used for training
- Rewards settle automatically to token holders without manual claims

**Revenue Calculation Example:**

> Model DAT #1234 total supply: 10,000 shares
>
>
> Your DAT holding: value = 500
>
>
> Monthly model earnings: 10,000 DAT
>
>
> Your revenue share: (500 / 10,000) × 10,000 = 500 DAT

## System Architecture & Lifecycle

[![Picture#2](https://ethereum-magicians.org/uploads/default/optimized/3X/1/c/1c1d28f3ffc2e7286566ce1debfe81cfe4ca2595_2_690x373.jpeg)Picture#21920×1040 119 KB](https://ethereum-magicians.org/uploads/default/1c1d28f3ffc2e7286566ce1debfe81cfe4ca2595)

### Phase 1: Asset Class Creation

> createClass(
> 1,                                              // classId
> “Medical Dataset”,                              // name
> “Open-source disease classification dataset”,   // description
> “ipfs://metadata/med-dataset-class”            // URI
> )

### Phase 2: DAT Minting & Asset Binding

> mintDAT(
> user1,          // recipient
> 1,              // classId: Medical Dataset
> 1000 * 1e6,     // value: 1000 (6 decimals)
> 0,              // expireAt: never expires
> 500             // shareRatio: 5% (in basis points)
> )

**Multi-User Ownership:** Mint multiple DATs within the same class to distribute fractional ownership across contributors.

### Phase 3: Usage-Based Value Transfer

> transferValue(
> user1TokenId,
> agentTreasuryTokenId,
> 100 * 1e6  // 100 units of value
> )

Enables pay-as-you-use models where agent invocations deduct value from user DATs to treasury contracts.

### Phase 4: Automated Revenue Settlement

When AI agents generate revenue from serving requests:

> agent.payToDATHolders(classId, 10 USDC);

The contract calculates each DAT holder’s `shareRatio` and distributes revenue proportionally without requiring individual claims.

### Phase 5: Expiration Enforcement (Optional)

> require(block.timestamp  function approveForClass(uint256 classId, address operator, bool approved) external;
> function isApprovedForClass(uint256 classId, address operator) public view returns (bool);

**Purpose:** Delegate control to platforms, automation contracts, or managed execution systems without requiring individual token approvals.

## Production Use Cases

**1. Decentralized inference markets:** Usage-based pricing for LLM/vision model APIs with automatic revenue splits to model trainers, data contributors, and compute providers

**2. Federated learning coordination:** Revenue distribution across dataset providers proportional to training contribution

**3. Agent-to-agent transactions:** Autonomous agents purchasing inference quota with programmatic access control

**4. Composable AI pipelines:** Chain multiple model classes (preprocessing → inference → post-processing) with usage tracking across the full stack

---

## Smart Contract Implementation

The DAT contract provides a comprehensive implementation with the following:

### Key Contract Functions

**Class Management:**

- createClass(classId, name, description, dataURI) - Create new asset category (owner only)
- classURI(classId) - Returns metadata URI for a class
- contractURI() - Returns contract-level metadata

**Token Operations:**

- mintDAT(to, classId, value, expireAt, shareRatio) - Create new DAT (owner only, returns tokenId)
- transferValue(fromTokenId, toTokenId, value) - Move value between same-class tokens
- approveForClass(classId, operator, approved) - Delegate class-level control
- isApprovedForClass(classId, operator) - Check approval status

**Query Functions:**

- valueOf(tokenId) - Get token’s current value
- classOf(tokenId) - Get token’s class
- shareOf(tokenId) - Get token’s revenue share ratio
- tokenSupplyInClass(classId) - Get total tokens minted in a class
- classCount() - Approximation of total classes

---

## Links

- LazAI Network Documentation
- GitHub ERC-8028 PR
- DAT Litepaper

## Replies

**HenryRoo** (2025-10-06):

**LazAI** is gearing up to launch its **Alpha Mainnet**, and as part of this milestone, we’re enhancing the Data Anchoring Token (DAT) to unlock the full potential of **ERC-8028**.

**You can dive into this article:**


      ![image](https://lazai.network/favicon.ico)

      [LazAI](https://lazai.network/blog/data-anchoring-token-dat-and-erc-8028-an-ai-native-asset-standard-for-ethereums-dai-era)



    ![image](https://cdn.prod.website-files.com/681bb4714316ae7f9cd23e99/69318f33faf581b8c80f32a9_Deliverables%5D20251202_LazAI_%20DAT%20Banner%20for%20article_v1.3.png)

###



DAT - Data Anchoring Token (ERC-8028) sets a new AI-native asset standard for Ethereum’s dAI era, turning AI data, models and agents into programmable on-chain assets.










**To explore:** The Data Anchoring Token (DAT) standard (ERC-8028) is transforming AI models and datasets into first-class, programmable assets on Ethereum. By embedding features like ownership rights, usage quotas, and revenue-sharing mechanisms directly into the token, DAT lays the foundation for a true “dAI” economy. This breakthrough enables agents to settle value trustlessly and verify provenance on-chain, pushing us beyond the “illusion of decentralized AI” toward a future where Ethereum serves as the settlement layer for autonomous machine-driven economies

---

**hash** (2025-10-31):

Hi. Could you provide concrete examples of what value represents for each “asset class” (dataset/model/agent)?

Also is the primary intended user a **B2B** platform (e.g., HuggingFace tokenizing its models for other platforms) or a C2C marketplace (e.g., an individual selling access to their custom-trained “My-Art-Style” LoRA model)?

---

**HenryRoo** (2025-11-04):

Hello [@hash](/u/hash). Thanks for asking, good question tho, lemme elaborate.

`value` is a **quota** whose **unit is defined per Class** (described in the `policyURI`, with precision via `unitDecimals`). The Class policy sets *what one unit means* and *how many decimals it has*.

So, to your example: if the Class policy says **1 unit = 1 image**, then `value = 100` means **you can read 100 images. The actual unit depends on the Class settings (e.g., images, API requests, tokens, minutes, etc.).

**Who is it for?** Both.

- B2B: e.g., a hosting platform issues DATs for its models/datasets, and any integrator can consume them with transparent on-chain usage accounting and deterministic revenue settlement.
- C2C: e.g., an individual artist sells access to a custom LoRA model; value could be 1,000 inference calls or 50k output tokens, and revenue is distributed by shareRatio.

---

**anaye1997** (2025-11-22):

I have two questions

- Can multiple underlying model versions map to the same DAT class (or it’s 1 to 1 relationship)?
- What determines the ‘value’ deducted per call — gas, oracle price, or a contract-set schedule?

---

**HenryRoo** (2025-11-24):

Hi [@anaye1997](/u/anaye1997), thanks for the questions! Here’s how we see it:

**1. Can multiple underlying model versions map to the same DAT class (or it’s 1 to 1 relationship)?**

In the nutshell - Yes. A DAT Class is the boundary for accounting and provenance (`classId`, `metadataURI`, `integrityHash`, `policyURI`).

- If versions are materially different (new weights/architecture/licensing/evals), we recommend a separate Class per version so quotas, usage accounting, and revenue distribution stay cleanly separated. (but its up to your model)
- If changes are minor, you can keep a single Class and update metadata (optionally adding proofs/attestations).

**Rule of thumb:** the moment you need separate quotas/settlement/provenance, create a separate Class.

**2) What determines the ‘value’ deducted per call — gas, oracle price, or a contract-set schedule?**

**Value** is a **quota**, and the deduction rules are defined by the **Class policy** (`policyURI`, precision via `unitDecimals`). Gas is **not** tied to quota by default. You can:

- Set a static rule (“1 inference = 1 unit”),
- Use metrics (output tokens / seconds / steps),
- Make it dynamic via an oracle/adapter (e.g., deduct more for higher complexity).

In our intended profile, the deduction per call is the **inference weight**: the `amount` passed to `recordUsage(tokenId, metricType, amount)` reflects a workload-based metric (e.g., a·input_tokens + b·output_tokens + c·latency + d·model_tier) defined in the Class `policyURI`. This keeps quota tied to **actual compute**, not gas.

- Hard-quota mode (recommended): recordUsage decrements value by amount (and prevents underflow).
- Soft-quota mode: the contract emits an event only; limits/policy are enforced off-chain.

---

**0x_WeakSheep** (2025-11-26):

### How is “value” and “unit” accurately determined?

- The proposal mentions that each DAT token has a value whose unit is defined by the Class Policy (such as images, API requests, tokens, minutes, etc.). However, how exactly is the “value” measured and calculated across different use cases?How can units be standardized across various applications?How is the  How do different asset classes (e.g., datasets, models, inference) balance their “value”?

### 2. Is the fee deduction mechanism fair and scalable?

The fee deduction is based on workload or inference calls, but does this approach face **scalability or fairness issues**? For example:

- Can more complex workloads lead to disproportionate fees?
- If using oracles or adapters for dynamic deductions, how can transparency and fairness be ensured?

---

**HenryRoo** (2025-12-02):

Hi [@0x_WeakSheep](/u/0x_weaksheep) thanks for asking. I tried to make it clear. So following your questions

### 1.How is “value” and “unit” accurately determined?

Making it simple:

- value = quota: how many times/how many units the resource can be used.
- unit = the quota unit, defined by the Class (in policyURI), precision set by unitDecimals.
- Examples:

Dataset: images / records / MB / requests.
- Model: inference weight (e.g., input tokens + output tokens + seconds).
- Agent: steps / tasks / minutes.

In **hard-quota**, `recordUsage(...)` decrements the quota; in **soft-quota**, it only emits an event and limits are enforced off-chain.

**Simple example:** if the Class policy says “1 unit = 1 image,” then `value = 100` = you can read **100 images**.

---

### 2. Is the fee deduction mechanism fair and scalable?

It depends what you mean by “fair.” Everyone has their own idea of fairness, but the **principle** is simple: we deduct based on real workload (inference weight), not gas. The coefficients and rules live in the **`policyURI`** they’re visible, versioned, and you can set **caps** (max per call/minute). That’s pretty fair and transparent, right?

On **scalability**, accounting is just a single **`recordUsage`** event, and payouts are done via **index + `claim`** cheap and predictable on-chain.

If you need dynamic deductions, you can plug in an oracle/adapter, but the source and version must be declared in the policy; if something breaks, we fall back to a static schedule. That covers most cases but if you see a hole or a better way, tell me and I’ll happily dig into it lol.

---

**fulldecent** (2025-12-04):

Hi Henry, thank you for sharing.

I see your note on the marketing page:

> LazAI empowers developers to create value-aligned, personalized AI agents

From that main motivation, I don’t see why that requires anything more than an existing value token.

---

If there are obvious other types of things that need to be tracked, and if you think there are lots of other projects that have the same problem, I would recommend to put this at the very beginning of your proposal.

---

**HenryRoo** (2025-12-09):

Got it, [@fulldecent](/u/fulldecent) thanks for calling that out. A simple value token handles price and ownership, but our use cases consistently need a bit more so usage and payouts don’t fall back to off-chain spreadsheets. The short version is that AI assets create value when they are used, not just when they exist, so we standardize a tiny set of primitives around that.

- On-chain usage metering, who consumed how much, not just who owns it
- Quota semantics, transferable and partially spendable value with optional expiry
- Deterministic revenue split, class-level settlement index plus claim for multi-party payouts
- Provenance binding, integrityHash and metadataURI to tie usage and fees to a specific version
- Policy-defined units, images or requests or tokens or seconds or inference weight, auditable in policyURI

We will add this on top shortly, thanks for suggestion!

---

**zero** (2025-12-12):

After reviewing 8024, I want to highlight an architectural observation that may help frame some long-term design choices.DAT is clearly modeling a rights-based, semi-fungible asset. The core semantics—class identity, integrityHash, metadataURI, quota/usage rules—place it much closer to a logical entitlement framework than a conventional fungible token standard.

This raises an important question: should the “rights semantics” and the “value/transfer semantics” continue to live in the same layer, or would a layered separation provide clearer abstraction boundaries, better composability, and more flexibility for future extensions?

---

**vitali_grabovski** (2025-12-12):

hello [@HenryRoo](/u/henryroo),

very interesting ERC. I’ll add more comments on the matter later, but first a few technical ones:

- why does this condition Both tokens non-expired (expireAt == 0 || now <= expireAt) treat the current time as not expired? When the current time is equal to the expiration time, it should already be considered expired. I suggest using now < expireAt instead.
- each link to the referenced ERCs is broken (for example, erc-1155 link: https://github.com/Thirumurugan7/ERCs/blob/erc-proposal-for-DAT/ERCS/eip-1155.md

---

**aina** (2025-12-14):

ERC-8028 is indeed an excellent proposal — I really like the direction it takes.

If it truly exhibits fungibility, then composing it with [ERC-8086: Privacy Token](https://ethereum-magicians.org/t/erc-8086-privacy-token/26623) would make it straightforward to address privacy concerns in this area, especially from a cryptographic and protocol-level perspective.

---

**ten-io-meta** (2025-12-14):

Hi Vladimir,

thanks for sharing this.

I’ve had a chance to skim the ERC-8028 (DAT) draft and part of the discussion here. Overall, the proposal feels well thought out and quite honest about the problem it’s trying to address.

Treating “value” as a class-defined usage quota, rather than as an abstract economic value, makes a lot of sense for AI assets like datasets, models, and agents, where value is really created at execution time. I also think keeping unit semantics and deduction rules at the Class policy level is a reasonable tradeoff versus trying to standardize everything globally.

I’ll keep following the discussion and will chime in if any point feels worth debating.

Best regards,

TEN

---

**devender-startengine** (2025-12-23):

What I Like

1. The dual-purpose value field is clever - Using it for both quality scoring and usage credits creates a natural quality gate. Low-quality data = low value = limited utility. Elegant.
2. Class-based architecture scales well - Separating asset categories (Dataset/Model/Agent) with class-level approvals (approveForClass) is cleaner than per-token permissions for marketplace use cases.
3. Built-in revenue distribution - The shareRatio + automatic settlement removes a lot of off-chain coordination. This is the right abstraction for contributor compensation.

Questions / Potential Gaps

1. Gas costs for on-chain usage tracking
The metrics mapping records every inference/training call on-chain. At scale (thousands of calls/day), this could get expensive. Have you considered:

- Batched merkle root commits?
- L2/rollup-specific optimizations (you’re on Metis)?
- Threshold-based recording (only log every Nth call)?

1. Value vs Quota relationship unclear
Both seem to limit usage. When does quota apply vs value depletion? Could these be unified?
2. Verification enforcement
The proof struct references TEE/ZK verification, but how is this enforced on-chain? Is there an oracle/verifier contract, or is verified set by a trusted party?
3. Expiration + fractional ownership
What happens to revenue share rights when a DAT expires? Does the holder lose their shareRatio claim, or just usage rights?
4. ERC-165 interface detection
Consider adding supportsInterface() so wallets/marketplaces can detect DAT tokens programmatically.

Potential Synergy: ERC-1450

I’m working on ERC-1450 (RTA-Controlled Security Token) - we’re solving a similar “controlled asset” problem but for SEC-regulated securities. Interesting parallels:

| Aspect | ERC-8028 | ERC-1450 |
| --- | --- | --- |
| Asset type | AI data/models | Securities |
| Class system | Asset categories | Regulation types (Reg CF, Reg D, etc.) |
| Controller | Validators/iDAO | Registered Transfer Agent |
| Usage tracking | Inference calls | Transfer requests |
| Revenue | Auto-split to holders | Fees + dividends |
| Verification | TEE/ZK proofs | Off-chain KYC/AML |

Both standards deal with “assets that need gatekeeping before transfer/use” - yours for AI quality/authenticity, ours for regulatory compliance.

If you have a few minutes, I’d appreciate your thoughts on our approach:

- Discussion: ERC-1450: RTA-Controlled Security Token Standard
- PR: Update ERC-1450: Move to Draft by devender-startengine · Pull Request #1335 · ethereum/ERCs · GitHub
- Reference Implementation: GitHub - StartEngine/erc1450-reference

Happy to continue the conversation and cross-reference if there are patterns that could benefit both standards.

Best,

Devender

---

**Ankita.eth** (2025-12-23):

Hi, [@HenryRoo](/u/henryroo)

After reading through the spec and discussion, I think ERC-8028 is framing the problem in the right way. Most confusion I’ve seen comes from assuming “value” means price or economic worth, when in reality it’s a **class-defined usage quota** with settlement semantics layered on top.

That distinction matters, and once it’s internalized, a lot of the design choices start to make sense.

A few observations and questions from a systems perspective:

**1. Rights vs. value semantics (layering question)**

I agree with the observation that DAT is closer to a rights/entitlement primitive than a conventional value token. Today, rights (quota, expiry, policy) and settlement (shareRatio, payouts) live in the same abstraction. That’s not wrong, but it does hard-couple two concerns.

Long term, it may be worth clarifying whether:

- DAT is intended to remain the minimal rights + accounting layer, with pricing and monetization living above it, or
- DAT is explicitly the economic primitive for AI assets.

Even a short “non-goal” section could help future implementers avoid overloading the base standard.

**2. Usage accounting at scale**

The hard-quota path (`recordUsage` decrementing value) is clean, but at inference-scale volumes this will almost certainly push usage tracking off L1.

You already hint at this with soft-quota mode and adapters, but it might be useful to explicitly frame:

- on-chain usage = settlement anchor, not full telemetry
- off-chain aggregation (batching, Merkle roots, rollups) as the expected production path

That sets expectations correctly and avoids people reading the spec as “every inference call must hit L1”.

**3. Value vs. quota semantics**

Conceptually, `value` already *is* the quota. The separate `quota` field feels redundant unless it’s meant to enforce a hard cap independent of spendable value.

If there’s a concrete scenario where both are required, a short example would help. Otherwise, unifying them could simplify the mental model and reduce implementation variance.

**4. Verification and trust boundaries**

The `proof` / `verified` mechanism is powerful, but the trust model deserves one explicit paragraph:

- Who is allowed to set verified?
- Is verification final or versioned?
- What guarantees does a consumer actually get from a verified DAT?

This isn’t about making verification “fully trustless” — just about making the trust boundary obvious and auditable.

**5. Expiry vs. revenue rights**

One subtle but important edge case: when a DAT expires, does it lose only *usage rights* or also *revenue participation*?

My assumption is “usage expires, settlement rights persist”, but stating this explicitly would prevent downstream surprises.

Overall, I think ERC-8028 is doing something important: it acknowledges that AI assets derive value from **use**, not existence, and it encodes that directly into the token model instead of pushing it into off-chain contracts and spreadsheets.

