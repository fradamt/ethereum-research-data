---
source: magicians
topic_id: 27416
title: "Potential Risk: Missing Relay Blacklisting in mev‑boost Can Waste Slots"
author: 0x_WeakSheep
date: "2026-01-11"
category: EIPs > EIPs informational
tags: [mev]
url: https://ethereum-magicians.org/t/potential-risk-missing-relay-blacklisting-in-mev-boost-can-waste-slots/27416
views: 18
likes: 0
posts_count: 1
---

# Potential Risk: Missing Relay Blacklisting in mev‑boost Can Waste Slots

# Potential Risk: Missing Relay Blacklisting in mev-boost Can Waste Slots

## TL;DR

mev-boost currently keeps only the top bid from `getHeader` and requests the payload from its relays with a fixed timeout. If those relays never deliver, validators wait ~4s and then fall back to the local execution client. There is no automatic penalty/blacklist for relays that repeatedly withhold payloads.

## Context

- getHeader stores the single highest-value bid and the set of relays that supplied it.
- getPayload fans out to those relays with --request-timeout-getpayload=4000ms.
- If no relay returns a payload, mev-boost returns HTTP 502 and the validator falls back to the local execution client.

Code references:

- fan-out logic: server/get_payload.go:152-334
- 502 response: server/service.go:419-429

## Risk

- No blacklisting: relays that repeatedly advertise high bids but never deliver are not deprioritized or disabled.
- Slot time waste: validators wait ~4 seconds for the timeout and then revert, making the builder flow for that slot effectively useless and reducing rewards.
- DoS/griefing vector: an attacker can run a relay that always posts top bids but never delivers payloads, wasting time across many validators, especially when relay lists overlap.



      [github.com/flashbots/mev-boost](https://github.com/flashbots/mev-boost/issues/882)












####



        opened 11:15AM - 05 Jan 26 UTC



        [![](https://avatars.githubusercontent.com/u/222537660?v=4)
          0xWeakSheep](https://github.com/0xWeakSheep)










# Potential Risk from Missing Relay Blacklisting Mechanism

## Problem Context

[…]()Currently, during `getHeader` mev-boost only keeps the **highest-value** builder bid and records the set of relays that supplied it. During `getPayload` it fans out payload requests to all relays with a default timeout of `--request-timeout-getpayload=4000ms`. If none of the relays deliver the payload, mev-boost responds to the beacon node with HTTP 502 (core handling in `server/service.go:419-429`), forcing the validator to fall back to the local execution client. The fan-out logic is in `server/get_payload.go:152-334`.

## Risk Description

- **No blacklisting**: Even if a relay repeatedly advertises high-value bids but refuses to deliver during `getPayload`, mev-boost never disables it automatically and will continue to select its bids in later slots.
- **Slot time waste**: When the winning relay withholds until timeout, the validator burns ~4 seconds waiting and still has to fall back to the local execution client, making that slot’s builder flow useless and reducing rewards.
- **DoS vector**: An attacker can run a relay that always posts top bids yet never hands over payloads, causing many validators to waste several slots, especially when operators share similar relay lists.

## Suggested Directions

1. Introduce penalties or blacklisting, e.g., disable or deprioritize a relay after it withholds/times out a given number of times.
2. Persist failure counters on top of existing health checks/metrics so external monitoring or CLI tools can warn operators automatically.
3. Consider keeping a secondary bid (second-highest) from `getHeader` to fall back to when all winning relays fail, reducing slot waste.

These improvements would mitigate the impact of malicious or unstable relays on validator rewards and shrink the 4-second delay + MEV loss caused by a single faulty relay.












## Possible Directions

1. Add penalties or blacklisting (e.g., disable/deprioritize relays after N timeouts or withheld payloads).
2. Persist failure counters on top of existing health checks/metrics so operators can be warned automatically.
3. Consider keeping a secondary bid (second-highest) from getHeader to fall back to if all winning relays fail.

## Questions for Discussion

- Is there appetite for relay-level penalty/blacklist logic inside mev-boost itself, or should this stay in external tooling?
- Would retaining a fallback bid introduce new security or incentive concerns?
- Are there existing proposals or implementations that address this in a standardized way?
