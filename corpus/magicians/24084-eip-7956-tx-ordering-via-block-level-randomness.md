---
source: magicians
topic_id: 24084
title: "EIP-7956: Tx Ordering via Block-Level Randomness"
author: aryaethn
date: "2025-05-07"
category: EIPs > EIPs core
tags: [core-eips, mev]
url: https://ethereum-magicians.org/t/eip-7956-tx-ordering-via-block-level-randomness/24084
views: 319
likes: 4
posts_count: 11
---

# EIP-7956: Tx Ordering via Block-Level Randomness

# EIP-7956: Tx Ordering via Block-Level Randomness

## Update

The EIP is renamed: “EIP-7956: Tx Ordering via Block-Level Randomness.”

## Update

`R` is now using [EIP-7998](https://eipsinsight.com/eips/eip-7998). The below description of the EIP is old and some changes have been made to the merged EIP. Please refer to https://eipsinsight.com/eips/eip-7956 or [EIPs/EIPS/eip-7956.md at master · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7956.md) for the most updated version.

Thank you.

## Simple Summary

Fix the execution order of transactions in every Ethereum block to an objective yet unpredictable key `H(tx) ⊕ R`, thereby removing **reorder‑based** MEV (e.g., sandwich and generalized front‑running).  Randomness `R` is sourced from the beacon chain; builders may still curate a profitable subset of the mempool, but once selected they **must** execute transactions in canonical order.  Deterministic tie‑breaking, explicit bundle mechanics, robust randomness analysis, and practical grinding limits are specified.

## Abstract

Proposers and builders can currently permute pending transactions arbitrarily, enabling reorder‑driven MEV.  This EIP introduces a consensus rule that sorts all transactions inside a block by XOR‑ing each transaction hash with fresh slot randomness.  The randomness is unknown until the slot starts, so the order is deterministic once known but unpredictable beforehand.  The mechanism **significantly reduces reorder‑based MEV**; latency‑driven back‑running, censorship, and other classes of MEV remain and should be mitigated through complementary techniques (encrypted mempools, reputation, PBS marketplaces, etc.).

## Motivation

Unrestricted ordering is the key enabler of sandwich and classic front‑running attacks.  Deterministic ordering collapses these vectors to latency racing and information asymmetry.  Clear candidate‑set and bundle semantics preserve fee markets while removing the need for trusted sequencers.  Academic work ([Qian et al., 2024](https://arxiv.org/pdf/2411.03327)) shows deterministic ordering drives sandwich profits toward zero.

## Specification

### Slot Randomness R

> Consensus‑layer prerequisite — Companion EIP “EL‑VRF‑exposure” is needed to add the RANDAO’s per‑slot VRF output to the execution layer.

```plaintext
randao_mix_slot     : bytes32
vrf_output_proposer : bytes32
R = (randao_mix_slot XOR vrf_output_proposer)[0:16]  # low 128 bits
```

Execution payloads include `randomness: bytes16` that **MUST** equal `R`; execution clients verify via EIP‑4788.

### Builder Flow

1. Candidate‑set selection – Builders MAY choose any subset of the mempool based on priority fees, side agreements, or policy.  Transactions not chosen are ignored.
2. Canonical sorting – Sort the chosen set by primary key H(tx) ⊕ R ascending, then secondary key H(tx) ascending, in case of collision on the primary key.
3. Gas‑limit packing – Append items in order until adding the next would exceed the block gas limit.
4. Bundles (optional cross‑address atomicity)

- Definition – A bundle is a user‑signed list of fully‑signed transactions.  Each child_tx_rlp is the canonical signed RLP encoding, including signature fields (v, r, s).  The bundle begins with a fee‑payment transaction that covers gas and builder tip for the entire bundle.
- Hashing / sort key – Treat the bundle as a virtual transaction with key H(concat(child_tx_rlps)), where:

child_tx_rlps[i] MUST be the exact bytes that will later appear in the block body for that transaction, i.e. the canonical RLP of the fully‑signed transaction per EIP‑2718 / EIP‑155 rules (for typed transactions the leading type byte and length prefix are included).
- Implementations MUST NOT strip or normalise the signature fields (v,r,s); those 65 bytes are hashed as‑is so every participant derives an identical bundle key.
- The concatenation order is the author‑declared execution order of the child transactions.

**Gas accounting** – Bundle gas is the **sum of the `gasLimit` fields** of all child transactions.  Builders use that sum when evaluating step 3.

**Fit‑or‑skip rule** – If the bundle (fee‑payment + children) would exceed the remaining gas limit, the bundle is skipped atomically.

1. Fee dynamics – Priority fees influence membership in the candidate set (step 1) but never override the canonical order once a tx or bundle is selected.

### Consensus Rule

A block is **invalid** if the executed list deviates from the canonical order derived from its `randomness` and the included transactions/bundles.  Verification is objective; fork‑choice remains unchanged.

## Security Analysis

### Randomness Bias & RANDAO Manipulation

- Single‑validator bias – A block proposer can influence only its own VRF output; XOR with the slot‑level RANDAO limits unilateral bias to 1‑in‑2¹²⁸.
- Coalition bias – Multiple consecutive‑slot proposers could attempt to influence RANDAO by withholding signatures, but the protocol already slashes equivocation and missed attestations.  The cost rises exponentially with coalition size, and the added VRF entropy further randomizes R.
- Forkable bias – Re‑org attempts longer than depth 1 must overcome the usual consensus finality thresholds.  Because R is embedded in the execution payload, any fork conflicts are objectively detectable by all nodes.

Conclusion: Collusion attacks are economically unattractive; the mixed entropy from RANDAO and VRF provides strong unpredictability guarantees.

### Hash Grinding

New signatures are required only when `calldata` changes, but attacks must begin **after** `R` is known (≤ 12 s).  Propagation delays and inclusion fees sharply limit profitable grinding to high‑value trades.

### Tie Collisions

Secondary key `H(tx)` guarantees total order; collision probability (`2^{-256}`) is negligible.

### Bundle Gas Consistency

Explicit summation rule ensures every client computes identical gas usage for bundles, preventing divergent validation.

### Residual MEV Vectors

- Back‑running & latency – Persist.
- Builder discretion – Builders may censor or selectively include transactions while forming the candidate set; exactly like the current status of Ethereum.

## Performance

Sorting ≤ 1 500 transactions remains `O(n log n)` (< 1 ms), on today’s hardware.

## Deployment

`txOrderingVersion = 1` flag + `ORDERING_TRANSITION_EPOCHS` window activate the rule.

### Backwards Compatibility

- Old nodes —  Execution clients that ignore the new fields will treat version‑1 blocks as malformed and fork away.  The short transition window gives operators time to upgrade.
- Light clients —  No additional work; they track headers chosen by upgraded full nodes.

## Replies

**4rdii** (2025-05-10):

In a system where validators select transactions but their ordering within a block is randomized to reduce MEV-driven front-running, how would your EIP address front-running strategies that operate across blocks or involve multiple transactions? For instance, consider a front-runner who identifies a victim’s high-value transaction (e.g., a large DeFi swap) in the mempool and proposes their own transaction one block earlier to manipulate the market state (e.g., inflating a token price before the victim’s swap).

Alternatively, what if the front-runner submits multiple redundant transactions (e.g., several swap transactions with slightly different parameters from different accounts) to increase the probability of a favorable random order within the victim’s block?

---

**4rdii** (2025-05-10):

Your EIP’s introduction of random transaction ordering could lead to non-deterministic outcomes, where the same set of transactions produces different blockchain states depending on their randomly assigned order. A critical example is in a lending protocol (e.g., Aave-like), where a price oracle update (Tx1) lowers the ETH/USD price from $2,000 to $1,500, making a borrower’s loan undercollateralized (1 ETH collateral = $1,500, debt = $1,600, ratio = 93.75%), and a liquidator’s transaction (Tx2) attempts to repay the debt and seize collateral. If Tx2 executes before Tx1 due to random ordering, the liquidation fails because the old price ($2,000) keeps the loan healthy (ratio = 125%). How does your proposal address the risks of such non-deterministic outcomes for DeFi protocols?

---

**aryaethn** (2025-05-10):

Hi,

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/4rdii/48/15223_2.png) 4rdiii:

> In a system where validators select transactions but their ordering within a block is randomized to reduce MEV-driven front-running, how would your EIP address front-running strategies that operate across blocks or involve multiple transactions? For instance, consider a front-runner who identifies a victim’s high-value transaction (e.g., a large DeFi swap) in the mempool and proposes their own transaction one block earlier to manipulate the market state (e.g., inflating a token price before the victim’s swap).

As for your first question:

1. The attacker cannot make sure that he can have his transaction a block earlier than the victim’s transaction, unless he is the block builder.
2. Even if he can have his transaction one block earlier, his transaction can be easily back-run by other MEV extractors, since now his transaction is already in the block and every transaction will be in the next block. So, his transaction will have little to no benefit to front-run the victim, as he becomes the victim, himself.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/4rdii/48/15223_2.png) 4rdiii:

> Alternatively, what if the front-runner submits multiple redundant transactions (e.g., several swap transactions with slightly different parameters from different accounts) to increase the probability of a favorable random order within the victim’s block?

As for your second question:

The probability of getting a transaction before the victim’s *k* transactions is *k/(k+1)*. If the attacker does craft transaction to be reverted, then he will fall for his own trap of making many transactions before the victim, and he will probably get back-run. Hence, I assume that he crafts the transactions to be reverted in case one is done.

In this case, the attacker must send base-fee and high priority-fee with each attacking transaction, to make sure they are included in the chain. This can lower their profitability significantly.

This means that the deterrent is economic, not cryptographic. The *deterministic* wins are removed, and what remains is **costly lottery.**

---

**aryaethn** (2025-05-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/4rdii/48/15223_2.png) 4rdiii:

> How does your proposal address the risks of such non-deterministic outcomes for DeFi protocols?

1. This can already happen if the validator/builder does not force some specific (e.g. oracle) transactions to be the first transaction of the block.
2. As proposed, the transaction submitter can easily bundle the transactions and sign them together, so the order in the bundle persists.
3. Most modern lending markets (Aave v3, Compound v3) pull the price inside the liquidation call, meaning the liquidation’s success never depends on a prior oracle-update transaction.
4. If projects want an even stronger guardrail, a lightweight application-level invariant can be added, to delay liquidation 1 block, or call the price within the same transaction of liquidation like those mentioned above.

---

**akasheruton** (2025-05-23):

One aspect that could be interesting to explore further is how this EIP handles scenarios requiring explicit execution dependencies *within the same block*, particularly when transactions might originate from different actors. For example, ensuring an oracle price update transaction is definitely executed *before* another transaction that consumes that price in a DeFi operation, all within the same block. While the EIP mentions bundles for atomicity, these are typically user-signed lists from a single originator.

A potential augmentation could be to introduce optional **execution tiers**.

- Users could specify a tier (e.g., Tier 0, Tier 1, Tier 2…) for their transaction, perhaps via a small field in the transaction data. Regular transactions could default to Tier 0.
- The block construction logic would first sort transactions by tier (Tier 0 executes first, then Tier 1, etc.).
- Within each tier, the EIP’s proposed canonical sorting mechanism (H(tx) ⊕ R primary key, H(tx) secondary) would be applied.

**Benefits of such a tiered approach could include:**

1. Explicit Dependency Management: Provides a protocol-level way for transactions from different origins to ensure a sequence (e.g., OracleCo’s price update in Tier 0, Alice’s DEX trade based on that oracle in Tier 1, Bob’s lending platform adjustment also in Tier 1).
2. Preservation of EIP’s MEV Reduction: Within each tier, the randomness-based sorting still protects against reordering attacks among transactions that don’t have a strict dependency or are in the same dependency group.
3. Clarity: Makes the intended execution flow more explicit for critical dependent transactions.

**Potential Considerations:**

- Added Complexity: This would introduce a new transaction field and require builders to perform a multi-stage sorting process (sort by tier, then sort by key within each tier).
- Tier Dynamics: It might lead to discussions around optimal tier usage, potential competition or new (albeit more constrained) MEV strategies related to accessing specific tiers if they become highly valued.

This isn’t to detract from the core proposal, which is strong for generalized MEV reduction. Rather, it’s a thought on how to layer explicit, user-defined sequencing for critical dependent operations on top of the randomized ordering foundation for the general case.

Great work on this EIP – it’s a valuable direction for mitigating a significant MEV vector! Curious to hear your thoughts on handling such explicit inter-transaction dependencies.

---

**siftman** (2025-05-24):

Hey, how does your deterministic transaction ordering deal with tricky cases like transaction dependencies or chain reorgs? What’s the plan to make sure nobody can game the system by exploiting predictable patterns from the block-level randomness?

---

**aryaethn** (2025-05-24):

Hi,

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/akasheruton/48/15318_2.png) akasheruton:

> One aspect that could be interesting to explore further is how this EIP handles scenarios requiring explicit execution dependencies within the same block, particularly when transactions might originate from different actors. For example, ensuring an oracle price update transaction is definitely executed before another transaction that consumes that price in a DeFi operation, all within the same block.

Firstly, I have to say that I have addressed this issue in another question:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aryaethn/48/15324_2.png) aryaethn:

> This can already happen if the validator/builder does not force some specific (e.g. oracle) transactions to be the first transaction of the block.
> As proposed, the transaction submitter can easily bundle the transactions and sign them together, so the order in the bundle persists.
> Most modern lending markets (Aave v3, Compound v3) pull the price inside the liquidation call, meaning the liquidation’s success never depends on a prior oracle-update transaction.
> If projects want an even stronger guardrail, a lightweight application-level invariant can be added, to delay liquidation 1 block, or call the price within the same transaction of liquidation like those mentioned above.

Also, adding Tiers to the system have multiple negative impacts. Firstly, it brings economic overhead without compensating gain to the system, since the answer above fully addresses the issue. Users must provide Tier-specific fees (or tips) to get included in the Tier they want, which brings complexity and war to the system. Secondly, it brings network overhead for the clients to do multiple steps of confirmation on each Tier’s ordering.

Last but most important, proposing Tiers to the system removes the entire purpose of this proposal of reducing MEV attacks. Here is an example:

- User A has a large swap on ETH-USDT pool with Tier-1.
- Malicious User M creates a front-running transaction with Tier-0.
- Malicious User M creates a back-running transaction with Tier-2.
- Malicious User M now has performed an easy sandwich attack to User A’s transaction.

I hope this answers your concerns.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/akasheruton/48/15318_2.png) akasheruton:

> Great work on this EIP – it’s a valuable direction for mitigating a significant MEV vector

Thanks ![:raised_hand_with_fingers_splayed:](https://ethereum-magicians.org/images/emoji/twitter/raised_hand_with_fingers_splayed.png?v=12)

---

**aryaethn** (2025-05-24):

Hi,

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/7ea924/48.png) siftman:

> Hey, how does your deterministic transaction ordering deal with tricky cases like transaction dependencies or chain reorgs?

In the following quote you can find the answer regarding this issue you raised.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aryaethn/48/15324_2.png) aryaethn:

> This can already happen if the validator/builder does not force some specific (e.g. oracle) transactions to be the first transaction of the block.
> As proposed, the transaction submitter can easily bundle the transactions and sign them together, so the order in the bundle persists.
> Most modern lending markets (Aave v3, Compound v3) pull the price inside the liquidation call, meaning the liquidation’s success never depends on a prior oracle-update transaction.
> If projects want an even stronger guardrail, a lightweight application-level invariant can be added, to delay liquidation 1 block, or call the price within the same transaction of liquidation like those mentioned above.

And for your next question:

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/7ea924/48.png) siftman:

> What’s the plan to make sure nobody can game the system by exploiting predictable patterns from the block-level randomness?

The answer is here:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aryaethn/48/15324_2.png) aryaethn:

> This means that the deterrent is economic, not cryptographic. The deterministic wins are removed, and what remains is costly lottery.

---

**dopaminix** (2025-08-20):

Hi,

Given that a malicious block builder could be the attacker themselves, thereby nullifying the defenses of propagation delay and priority fees against hash grinding, how does the proposal’s security model, particularly the unpredictability of the `R` value, serve as a sufficient deterrent? Does this specific scenario impact the conclusion that such attacks are “economically unattractive”?

---

**aryaethn** (2025-08-20):

Hi [@dopaminix](/u/dopaminix) .

If I correctly understand your question, I think I already addressed this within the EIP. Although this EIP reduces MEV bots who only see the  mempool, the builders can still try to grind the hash of their own transactions (if lucky enough). Also, they can choose not to include some transactions, as they already can in the current style of the Ethereum consensus.

I don’t claim I remove or reduce all kinds of MEV attacks by this EIP. My claim is that MEV bots who only see the mempool and have no other active malicious act in building the blocks are reduced or at least much harder to attack.

If my claim is not very clear in the EIP, or I have stated a sentence that claims otherwise, please tell me to update it to make it more clear. Thanks.

