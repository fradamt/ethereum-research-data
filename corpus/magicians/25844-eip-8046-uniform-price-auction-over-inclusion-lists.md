---
source: magicians
topic_id: 25844
title: "EIP-8046: Uniform price auction over inclusion lists"
author: aelowsson
date: "2025-10-16"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-8046-uniform-price-auction-over-inclusion-lists/25844
views: 200
likes: 2
posts_count: 8
---

# EIP-8046: Uniform price auction over inclusion lists

Discussion topic for [EIP-8046](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-8046.md); [PR](https://github.com/ethereum/EIPs/pull/10554); [Web](https://eips.ethereum.org/EIPS/eip-8046).

#### Description

Ensure IL transactions that offer a higher ranking fee than competing transactions are included in the block. Burn the marginal ranking fee.

#### Relevant resources

- First research post on UPIL design (ranking transactions based on fee).
- FOCIL research post, EIP and homepage.
- AUCIL research post.

*Thanks to Francesco D’Amato for feedback.*

### Abstract

This EIP proposes a uniform price auction over inclusion lists (UPIL), which ranks transactions by their offered ranking fee per gas. When the block is full, no transaction is allowed to displace an inclusion-list (IL) transaction that passes regular inclusion criteria and offers a higher ranking fee per gas. All included transactions pay a uniform inclusion price, equal to the highest ranking fee offered by any valid IL transaction excluded from the block, and this fee is burned. UPIL achieves strong censorship resistance by not allowing builders to circumvent propagated ILs when the block is full. This is particularly valuable for time-sensitive transactions and promotes fairness while preventing cheap block-stuffing under a multidimensional fee market. UPIL is specified to run on top of FOCIL (EIP-7805), but can be deployed on top of any IL mechanism.

## Replies

**bubbaready** (2025-11-27):

this could be used to stop MEV attacks?

---

**aelowsson** (2025-11-27):

It does not prevent MEV.

---

**dnstaked** (2025-11-27):

Does FOCIL/FOCILR take OFAC into consideration?

---

**box** (2025-12-03):

Thanks for the proposal — FOCILR feels like a meaningful evolution of FOCIL, especially for maintaining censorship-resistant inclusion guarantees under multi-resource congestion.

What I particularly appreciate is the combination of:

- Explicit ranking_fee_per_gas → expresses inclusion urgency directly
- Uniform marginal ranking fee → removes value extraction incentives for block stuffing
- Ordered IL enforcement → strengthens the credible commitment in congested conditions

To help the ecosystem align around adopting this, I believe two areas could use more elaboration:

![:one:](https://ethereum-magicians.org/images/emoji/twitter/one.png?v=12) **Tooling / UX implications**

Wallets, explorers, and simulation tools need clear guidance to prevent confusing situations where users overpay ranking fees or fail inclusion despite high gas settings. A recommended “ranking fee bidding” strategy or baseline heuristics would be very useful.

![:two:](https://ethereum-magicians.org/images/emoji/twitter/two.png?v=12) **Builder / includer implementation paths**

As FOCILR introduces new ordering constraints, having more detail on how block builders should efficiently incorporate ranked IL during block construction can help avoid accidental centralization pressure.

If the EIP includes these operational considerations (or links to reference implementations), it would be easier for client teams and infra providers to commit to rolling this into their roadmaps — and the proposal’s benefits to censorship-resistance would be much clearer to the broader community.

Overall, I support the direction and would love to see more concrete benchmarks and UX guidelines as next steps.

---

**Xiawpohr** (2026-01-06):

I like the idea of upholding censorship resistance under inclusion lists (ILs). However, I have several questions from a transactor’s perspective.

Transactors may find it difficult to evaluate how much to pay for censorship resistance, and the distinction between `max_ranking_fee_per_gas` and `max_priority_fee_per_gas` could be confusing. From a transactor’s standpoint, I understand:

- max_ranking_fee_per_gas is meant to overcome censorship, increasing the probability that my transaction won’t be excluded from the current block.
- max_prioriry_fee_per_gas is meant to incentivize builders to include or order my transaction, increasing the probability of inclusion in the current block.
- Practically speaking, both fees serve nearly the same purpose for transactors, which creates confusion and poor user experience.

Following this logic, consider how transactors will behave when blocks are full. Since transactors want their transactions included quickly with minimal fees, they have two options. The first is to raise `max_priority_fee_per_gas`. However, because blocks must reserve space for ILs, the available block space shrinks, forcing transactors to increase priority fees more than they would have before this EIP. The second option is to raise `max_ranking_fee_per_gas` above 12.5% of the current base fee. When all transactors adopt this strategy and at least one of inclusion list committee members select transactions based on the highest ranking fees, a [chicken game](https://en.wikipedia.org/wiki/Chicken_(game)) emerges. Transactors continually bid up ranking fees until they reach their maximum affordable level. Censorship costs escalate so dramatically that builders have no choice but to include nearly all IL transactions. Yet since transactions in ILs need to pay neither ranking fee nor priority fee, most transactors will clearly opt for this second option. Consequently, the mechanism is distorted into serving only the wealthiest transactors, making ILs a privilege for giant whales.

In my view, a [pay-as-you-bid auction using only priority fees](https://eips.ethereum.org/EIPS/eip-8046#pay-as-you-bid-auction-using-only-priority-fee) would be better to avoid that situation, since priority fee represents a direct expense for transactors. This approach requires no new transaction format and avoids confusing terminology.

However, I don’t see the necessity of `priority_fee_shift_per_gas`. Since builders have last-look when constructing blocks and can decide whether to include transactions, why should they help transactors get selected into ILs only to include them anyway?

---

**hirako2000** (2026-01-06):

> since transactions in ILs need to pay neither ranking fee nor priority fee

My reading of the FOCILR (EIP-8046) specification is that a transaction **must pay its pre-committed** `max_ranking_fee_per_gas` **if it is included via the Inclusion List**. This fee is part of the `inclusion_fee_per_gas` (base fee + marginal ranking fee) that is **burned**.

If this understanding is correct, that IL transactions do incur a real, burned fee. How would that change the predicted bidding dynamics and the ‘whale privilege’ scenario you’ve raised? It seems this would shift the analysis from fee avoidance to the economics of a uniform-price auction..

---

**Xiawpohr** (2026-01-07):

According to the proposal specification, `inclusion_fee_per_gas = base_fee + marginal_ranking_fee`, where `marginal_ranking_fee = max(ranking_fee | IL transactions excluded from the block)`.

Consider four transactions (A, B, C, D) in the inclusion list with `max_ranking_fee_per_gas` values of (2, 1, 4, 3) respectively, ordered as C > D > A > B. If the builder includes only transactions C and D, the marginal ranking fee is determined by the highest excluded transaction which is 2(A’s fee) in this case, and all transactions in the block pay the same inclusion fee. Notably, transaction C pays a marginal ranking fee of 2 rather than its bid of 4. If the builder includes all IL transactions, no transactions are excluded, so the marginal ranking fee is 0. This marginal ranking fee functions as a censorship cost for the builder, incentivizing them to include all IL transactions to minimize this cost.

From a transactor’s perspective, there’s no need to pay a priority fee if our transactions are in the inclusion list. This creates a competition to secure IL space, with transactors bidding up ranking fees competitively. The censorship cost becomes so high that builders are forced to include all IL transactions, driving the marginal ranking fee toward zero. As expected, whales dominate this competition for IL slots.

I believe only using priority fees to rank transactions within the inclusion list could mitigate this problem. This approach would prevent transactors from bidding up priority fees without constraints.

