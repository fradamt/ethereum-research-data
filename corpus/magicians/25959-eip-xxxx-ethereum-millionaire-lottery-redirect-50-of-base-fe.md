---
source: magicians
topic_id: 25959
title: "[EIP-XXXX] Ethereum Millionaire Lottery — Redirect 50% of base fee to a perpetual jackpot"
author: su007-eth
date: "2025-10-25"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/eip-xxxx-ethereum-millionaire-lottery-redirect-50-of-base-fee-to-a-perpetual-jackpot/25959
views: 114
likes: 1
posts_count: 5
---

# [EIP-XXXX] Ethereum Millionaire Lottery — Redirect 50% of base fee to a perpetual jackpot

# EIP: Ethereum Millionaire Lottery — Redirect 50% of base fee to a perpetual jackpot (author: wutaner.eth)

## EIP: Ethereum Millionaire Lottery

### Summary

This proposal introduces a minimal, protocol-level lottery mechanism that redirects 50% of EIP-1559 base fees into a perpetual jackpot pool.

Each address that pays at least a threshold τ of base fees during a round becomes eligible for one ticket.

When the jackpot pool reaches 100 ETH, one random address wins up to 100 ETH using delayed beacon-chain randomness (EIP-4788).

### Key Details

- 50% base fee burned, 50% into jackpot pool.
- One address = one ticket (≥ τ base fee).
- Jackpot triggers at pool ≥ 100 ETH.
- Randomness from beacon RANDAO (K = 128 slots delay).
- Payout = min(100 ETH, N × τ) ensures fairness & liveness.
- τ auto-adjusts between rounds to track participation.
- No tokens, no teams, no external oracles — fully native.

### Motivation

EIP-1559 burns ETH but provides no social feedback.

This EIP keeps Ethereum deflationary *and* adds a perpetual, decentralized wealth-effect engine:

> “Half burns the rich, half blesses the brave.”

### Security

- Randomness manipulation prevented via 128-slot RANDAO delay.
- Bots can’t profit: EV per ticket ≤ τ.
- Memory usage bounded (delete accumulator after qualification).
- Fully compatible with EIP-1559 and existing fee markets.

### Author

**wutaner.eth** — [@wutaner](https://twitter.com/wutaner)

### Discussions

Ethereum Magicians thread:

![:backhand_index_pointing_right:](https://ethereum-magicians.org/images/emoji/twitter/backhand_index_pointing_right.png?v=15) https://ethereum-magicians.org/t/eip-ethereum-millionaire-lottery/XXXX

### License

CC0-1.0

## Replies

**su007-eth** (2025-10-25):

---

## file: eip-millions-lottery.md
eip: TBD
title: Ethereum Millionaire Lottery
description: Redirect 50% of EIP-1559 base fee to a perpetual jackpot with one-address-one-ticket eligibility and delayed beacon randomness.
author: wutaner.eth (@wutaner)
discussions-to:
status: Draft
type: Standards Track
category: Core
created: 2025-10-25
requires: 1559, 4788

## Abstract

This EIP redirects **50%** of the EIP-1559 base fee to a **perpetual jackpot pool**, awarding **one random address up to 100 ETH** per round using delayed beacon-chain randomness.

An address becomes eligible for **one ticket** once its cumulative base fee paid reaches a per-round threshold **τ**.

The payout applies a fuse rule **P = min(J, N·τ)** to ensure liveness and eliminate positive-EV Sybil attacks.

No tokens, no oracles — pure Ethereum math.

---

## Motivation

EIP-1559 burns the base fee, improving ETH’s monetary policy but providing no social feedback.

Redirecting half of this burn to a jackpot introduces a **continuous, fair, and permissionless wealth effect**, rewarding on-chain activity while maintaining deflationary pressure.

> “Half burns the rich, half blesses the brave.”

---

## Specification

### Constants and Parameters

| Symbol | Meaning | Default |
| --- | --- | --- |
| J | Jackpot cap | 100 ETH |
| τ | Threshold per address | 0.001 ETH (auto-adjusted) |
| K | Randomness delay | 128 slots |
| P | Actual payout | min(J, N·τ) |
| N | Qualified addresses | dynamic |

### Base-Fee Allocation

Each transaction’s base fee:

- 50% → burned
- 50% → jackpot pool

### Eligibility (One Address, One Ticket)

An address is **qualified** if its cumulative base fee paid in the round ≥ τ.

Each qualified address = 1 ticket.

τ is fixed at the start of each round.

### Trigger and Payout

When the jackpot pool ≥ J:

1. Snapshot the qualified addresses (publish Merkle root).
2. Delay K = 128 beacon slots (≈25 min).
3. Use beacon-chain RANDAO randomness via EIP-4788.
4. Winner index = hash(seed || round_id) mod N.
5. Payout = min(J, N·τ) ETH to the winner.
6. If P = tau && !qualified[sender(tx)]:
      qualified[sender(tx)] = true
      N += 1
      delete acc[sender(tx)]
  if phase == ACCUMULATING && pool >= J:
    snapshot_root = merkleRoot(sorted(qualified.keys()))
    snapshot_slot = current_beacon_slot()
    phase = SNAPSHOT

on_beacon_slot_tick():
  if phase == SNAPSHOT && current_beacon_slot() >= snapshot_slot + K_SLOTS:
    seed = beaconRandao(current_beacon_slot())
    idx = hash(seed || round_id) mod N
    winner = address_at_index(idx)
    payout = min(J, N * tau)
    transfer_from_pool(winner, payout)
    reset_round()  // carry over (J - payout)
```

---

## Security Considerations

- Randomness manipulation: mitigated by 128-slot delay.
- Sybil botting: per-ticket EV ≤ τ → unprofitable.
- DoS/memory: delete accumulators once qualified.
- Reorgs: no higher risk than standard finality assumptions.

---

## Backwards Compatibility

No transaction format changes.

Base-fee allocation is modified to redirect half into jackpot accounting.

Fully compatible with EIP-1559 semantics.

---

## Example Scenarios

| Scenario | N | τ | Payout | Comment |
| --- | --- | --- | --- | --- |
| Low activity | 12,000 | 0.005 | 60 ETH | Partial payout, 40 ETH rolls over |
| Normal | 120,000 | 0.001 | 100 ETH | Full jackpot |
| Bot attempt | 10,000 bots, τ=0.001 | 100,000 total | EV ≤ cost | No profit |

---

## Copyright

CC0-1.0 — Public Domain

---

**Rexjaden** (2025-10-27):

i do really like the concept,security could be an issue,some form of AI monitoring would be a good addition with correct implementation

---

**wjmelements** (2025-10-27):

The burn is not only monetary policy. It is the only way that unstaked ETH accrues value. Halving the protocol revenue halves the intrinsic value of ETH.

Even if we wanted a marketing budget, it should not be spent paying EOAs randomly. Users are not necessarily EOAs, and even if they were they would not necessarily want to transact just for a chance to win. But if this did attract new usage, the actual gas would still be the same; those gamblers would be outbidding others, resulting in a higher base fee. There would be no way to opt out; everyone would be forced to pay higher fees to benefit those degenerates.

Your scheme is also a sybil vector because you limit to one ticket per account. It would be simpler to grant every EOA a chance proportionate to their fees. Your ticketing system only encourages users to sybil.

---

**su007-eth** (2025-10-28):

Thanks for the thoughtful feedback — really appreciate it!

Let me clarify a few things, because I think there’s a misunderstanding of the mechanism’s intent and math.

![:one:](https://ethereum-magicians.org/images/emoji/twitter/one.png?v=12) **We’re not removing the burn.**

The proposal still burns 50% of the base fee — enough to preserve ETH’s scarcity narrative.

The other 50% is just *repurposed* for social feedback. EIP-1559 optimized monetary policy, but it didn’t create any positive reinforcement loop for participation.

“Half burns the rich, half blesses the brave” means half goes to scarcity, half to activity.

![:two:](https://ethereum-magicians.org/images/emoji/twitter/two.png?v=12) **It doesn’t raise gas fees.**

The base fee is still market-driven. The jackpot pool is funded by *existing* base-fee flow — not an external budget, and not an additive cost.

Nobody pays extra; the only change is where the already-collected ETH goes (part burn, part jackpot).

![:three:](https://ethereum-magicians.org/images/emoji/twitter/three.png?v=12) **Sybil resistance is built-in.**

This is where our design differs: each address gets *one* ticket once it pays ≥ τ in base fees.

If someone tries to farm tickets with many accounts, they must pay m × τ to get m tickets.

But the expected value per ticket ≤ τ (since payout ≤ N·τ).

That means there’s no positive EV — only cost and variance.

A “weighted by fees” approach would actually *increase* Sybil profitability, since spending more gas directly increases win odds.

So, it’s not about gambling; it’s about creating a perpetual, fair, zero-EV participation reward loop — a social layer complementing the monetary one.

Appreciate your challenge — it’s exactly the kind of discussion this EIP needs ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)

