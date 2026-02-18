---
source: magicians
topic_id: 22805
title: Forcing a block’s transaction ordering by gas usage volume
author: OlegJakushkin
date: "2025-02-09"
category: EIPs > EIPs core
tags: [mev]
url: https://ethereum-magicians.org/t/forcing-a-block-s-transaction-ordering-by-gas-usage-volume/22805
views: 292
likes: 0
posts_count: 6
---

# Forcing a block’s transaction ordering by gas usage volume

## Forcing Block Transaction Ordering by Gas Usage Volume

### 1. Introduction

This discussion explores a proposal to **enforce a canonical transaction ordering** in Ethereum blocks based on each transaction’s “volume”—defined, for example, as `gasUsed * gasPrice`. By stripping block producers of the freedom to reorder transactions arbitrarily, the aim is to reduce certain kinds of Maximal Extractable Value (MEV), particularly front-running and sandwich attacks. We also consider broader implications, including changes to incentive structures, potential shifts in MEV strategies, and how aggregator (“bundler”) contracts might evolve.

---

## 2. Core Idea

### 2.1 Proposal

- Consensus Rule
Modify Ethereum’s consensus layer so that every block must sort its transactions in ascending order of a “volume” metric. A possible metric is
   V(tx) = gasUsed * gasPrice
(In an EIP-1559 environment, “gasPrice” may include baseFee + tip, but the exact formula can be refined.)
- Block Validity
Under this rule, a block is valid only if for each transaction tx_i that appears before tx_j,
   V(tx_i) <= V(tx_j).
Any tie in V(tx_i) could be broken by a deterministic fallback (e.g., transaction hash then nonce).
- Rationale
Because block producers cannot reorder transactions to exploit private ordering benefits, many front-running and sandwiching attacks become more difficult or impossible to execute. Over time, the ecosystem might see widespread use of aggregator (“mega-tx”) contracts, each internally bundling multiple user transactions with a predictable sub-ordering that is verifiable on-chain.

---

## 3. Critical Analysis

1. MEV-Boost and Proposer-Builder Separation (PBS) Still Relevant

Even if the protocol enforces a fixed transaction order, proposers or builders still decide which transactions to include. Reordering is only part of MEV; the ability to include or exclude transactions remains a vector for censorship-based or content-based MEV. Also there is always someplace to compete for inclusion into the block tail and, thus, MEV, it just costs much more to be included.
2. Partial, Not Complete, MEV Elimination

Many forms of MEV rely on timing (e.g., liquidations) or selective inclusion/exclusion. Forced ordering mitigates reorder-based strategies (like sandwiching) but does not address MEV arising from transaction content or block-level censorship.
3. Centralization & Complexity Risks

Major aggregator (“bundler”) contracts could dominate, effectively becoming gatekeepers for entire blocks.
4. Implementing forced ordering at the consensus level is a major protocol shift, requiring a hard fork, client updates, and broad ecosystem support.
5. Market Dynamics & Fee Market Interactions

Under EIP-1559, users pay a baseFee (burned) plus a tip. Forcing strict ascending volume might distort fee signals: a user could deliberately lower or raise gas usage to manipulate ordering position.
6. This could lead to gaming the system with artificially constructed transactions (“spam race”).
7. Incentive Compatibility

Blocks that do not follow the mandated ordering are invalid. This high penalty ensures compliance but fundamentally changes how block producers assemble transactions.
8. It also partly shifts block-building complexity from an off-chain builder ecosystem to on-chain logic and aggregator smart contracts.

---

## 4. Proposed EIP Draft

**EIP**: *TBD*

**Title**: *Forced Transaction Ordering by Gas Usage*

**Author**: Oleg Iakushkin ([@OlegJakushkin](/u/olegjakushkin) / 0x614c2916F5BD3ea04DE1E5714Bf814A81f53C71F) , You dear reader

**Status**: *Draft*

**Type**: Standards Track — Core

**Created**: *TBD*

### 4.1 Abstract

This EIP proposes an Ethereum consensus rule requiring that transactions in each block appear in ascending order of a defined “volume” metric (e.g., `gasUsed * gasPrice`). By removing the block producer’s freedom to reorder transactions, a significant portion of reorder-based MEV may be reduced or eliminated.

### 4.2 Motivation

Reorder-based MEV, especially front-running and sandwiching, continues to create harmful user experiences and economic inefficiency. A strict, protocol-level ordering aims to diminish such attacks by preventing block producers from tailoring the transaction sequence for personal gain.

### 4.3 Specification

1. Volume Definition
   V(tx) = gasUsed * gasPrice
(Future EIPs may refine this to incorporate EIP-1559 baseFee, tips, or other dynamic fields.)
2. Ordering Rule
A block is valid only if for every pair tx_i, tx_j with i < j,     V(tx_i) <= V(tx_j).
3. Tie-Breaking
In the case of identical volume values, an agreed fallback (transaction hash in ascending order, then ascending transaction nonce) ensures deterministic ordering.
4. Implementation

Validation: Ethereum clients reject blocks with out-of-order transaction volume.
5. Block Assembly: Validators must incorporate sorting by volume into their block construction process.

### 4.4 Rationale

- Determinism: Directly addresses reorder discretion at the block producer level.
- Tie-Breaking: Minimizes cross-client discrepancies.
- Extendability: The definition of volume can adapt to protocol changes.

### 4.5 Backwards Compatibility

- Hard Fork: Non-upgraded clients will diverge from the chain, making this a breaking change.
- Block Production: Existing block-building workflows must be modified to sort transactions by volume before block finalization.

### 4.6 Test Cases

1. Ascending Check: Blocks must list transactions strictly from lowest to highest volume.
2. Tie Cases: Confirm consistent fallback ordering across multiple clients.
3. Edge Cases: Blocks with a single large aggregator transaction or many minimal-volume transactions.

### 4.7 Security Considerations

- Limited MEV Reduction: Only addresses reorder-driven MEV, not censorship or timing-based MEV.
- Gaming Volume: Users might inflate or deflate gas usage or manipulate tips to secure favorable positions.
- Aggregator Centralization: Large bundling contracts may dominate, potentially introducing new forms of gatekeeping or censorship.

### 4.8 References

- MEV Research (Flashbots)
- Proposer-Builder Separation (PBS)
- SUAVE (Flashbots)

---

## 5. Why Aren’t Large “Bundling Contracts” Dominant Already?

Despite their theoretical value in mitigating reorder-based attacks, “mega-transactions” (aggregator contracts containing multiple user trades) remain relatively niche:

1. Gas Overhead & Block Limit

Bundling many trades into a single transaction can be costly. Such mega-txs risk hitting block gas limits or incurring high fees.
2. User Trust & Complexity

Users must trust aggregator operators to handle transactions fairly. A malicious aggregator can reorder or censor sub-txs internally.
3. Competition from MEV Infrastructure

MEV-boost, private relays, and specialized searchers currently form a robust system for sophisticated transaction inclusion strategies. Bundlers must compete on fees or tips to displace these methods.
4. Weak Adoption Incentives

A single aggregator transaction might not always deliver higher total fees to block builders. Builders usually prefer individually high-fee transactions unless a bundler pays a large aggregate tip.
5. Coordination Hurdles

For aggregator-based ordering to significantly reduce reordering attacks, a critical mass of users and dApps must adopt it, which has yet to happen.

---

## 6. Predicted Outcomes

1. Reduced Builder Discretion

By sorting transactions by volume, a major lever of reorder-based MEV is reduced. However, block builders and proposers can still pick which transactions to include, preserving some forms of MEV.
2. Aggregator (Mega-Tx) Surge

Large bundling contracts with on-chain verifiable order might grow in importance. If these aggregators become trusted, they could fill entire blocks with minimal reorder risk—albeit at the cost of centralization.
3. Possible “Spam Race”

Users might craft micro-volume or artificially manipulated transactions to exploit the forced ordering. This could bloat the mempool or create new front-running tactics around gas usage.
4. Shift in MEV Tactics

Although reorder-based MEV could decline, new methods involving content-based inclusion, censorship, or timing might become more prevalent.
5. Alignment with PBS

Proposer-Builder Separation remains relevant because it decentralizes block building; forced ordering primarily addresses how included transactions are sequenced, not who selects them.

---

## 7. Conclusion

Enforcing a strict block-level ordering by transaction “volume” may curb certain reorder-driven MEV attacks, enhancing fairness for many users. However, it introduces significant protocol changes, opens potential for volume manipulation, and could spur aggregator centralization. While this approach might make some forms of MEV more transparent, it will not eliminate MEV altogether—censorship, timing, and inclusion-based strategies can still thrive.

Before any mainnet adoption, robust debate, simulation, and potentially trial deployments on testnets or rollups are essential. The Ethereum community must weigh whether the reduction in reorder-based MEV justifies the complexity, potential for new vectors of gaming, and the protocol-level upheaval required by a forced ordering rule.

**Feedback, additional ideas, and critiques are encouraged!**

## Replies

**Nerolation** (2025-02-10):

Wouldn’t this lead to a situation in which searchers/builders would have to potentially “waste” gas in order to sandwich a user by trying to have one transaction where `gasUsed * gasPrice` is higher than the victim transaction and one that is lower. This would just be a shift in gaming-strategy that wastes more gas.

Furthermore, you only know the gas_used after execution, making block building more difficult because you’d always have to insert transactions somewhere and then execute all transactions from there again to make sure no other transaction got invalidated. For sure solvable but additional complexity.

---

**OlegJakushkin** (2025-02-10):

On the first point, yes, in a way: one can imagine a sizeable first tx(s) from bundler(s) (say 1-3) with super small space left for MEVed txs from the Builder (if he got lucky) and there Builder will use all possible means to gain some value; thus MEV can become prohibitively costly.

I agree with the second point - reruns on resorting will bring additional complexity.

[@Nerolation](/u/nerolation) Would you consider the first or second point as a dealbreaker, or would you say they can be worth the risk?

---

**Nerolation** (2025-02-10):

I think both points are problematic but the gamification the even bigger problem. Currently, 1inch enforces some gas_price limit on chain that causes solvers to put many SLOADs into transactions just to consume more gas thus making their transaction more lucrative to builders. Those are now the transactions with the highest SLOAD usage. So, while a limit to protect users might sound smart, there are bad externalities such as solvers now waisting gas which contributes to higher prices for users as well as stressing certain opcodes, in this case SLOAD.

Another issue I see is it being incompatible with [delayed execution](https://ethresear.ch/t/delayed-execution-and-skipped-transactions/21677) because we would want to allow validators to attest to a block before doing the execution. This would only work if we order by tx.gas*gas_price, which makes no sense.

---

**OlegJakushkin** (2025-02-10):

Any bundler(s) TX with honest txs inside will have a considerable potential of getting into the block. Yet yes, as it pays to win, such cases may occur. Are their stats on that issue public so we can see what may be expected?

On the second point - thank you, I see - `gasUsed *gasPrice` will indeed require doing the execution and kill `Delayed Execution`. Is there an EIP of Delayed Execution for me to reference?

---

**Nerolation** (2025-02-10):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/o/a88e57/48.png) OlegJakushkin:

> Is there an EIP of Delayed Execution for me to reference?

Not yet but soon. I’m happy to ping you again and forward it to you as we’re putting it out.

Regarding some public stats… not really, unfortunately. I just remember stumbling across it during some analysis on block-level warming.

However, this is an example tx:


      ![image](https://dashboard.tenderly.co/favicon.ico)

      [dashboard.tenderly.co](https://dashboard.tenderly.co/tx/mainnet/0x9eac0ada21d56e2e2adf8a36661baa5668b29e79424044b05447096b67d4c94d)



    ![image](https://dashboard.tenderly.co/Assets/twitter_card_image.png)

###



Tenderly is a full-stack infrastructure for the entire dapp lifecycle, offering the only node RPC with built-in development environments and tools. Sign up now!










And here is some additional info on that:

https://snapshot.org/#/s:1inch.eth/proposal/0x16de4fba8ea4839bd41e4f6917bd09b07283b1428398339983f8768ea6e4e5d0



      [github.com](https://github.com/1inch/limit-order-settlement/blob/master/contracts/Settlement.sol#L31)





####



```sol


1. function _postInteraction(
2. IOrderMixin.Order calldata order,
3. bytes calldata extension,
4. bytes32 orderHash,
5. address taker,
6. uint256 makingAmount,
7. uint256 takingAmount,
8. uint256 remainingMakingAmount,
9. bytes calldata extraData
10. ) internal virtual override {
11. if (!_isPriorityFeeValid()) revert InvalidPriorityFee();
12. super._postInteraction(order, extension, orderHash, taker, makingAmount, takingAmount, remainingMakingAmount, extraData);
13. }
14.
15. /**
16. * @dev Validates priority fee according to the spec
17. * https://snapshot.org/#/1inch.eth/proposal/0xa040c60050147a0f67042ae024673e92e813b5d2c0f748abf70ddfa1ed107cbe
18. * For blocks with baseFee 104.1 gwei – priorityFee is capped at 65% of the block’s baseFee.
21. */


```

