---
source: magicians
topic_id: 18218
title: EL triggered validator Pause
author: g11in
date: "2024-01-19"
category: EIPs > EIPs core
tags: [consensus-layer]
url: https://ethereum-magicians.org/t/el-triggered-validator-pause/18218
views: 767
likes: 7
posts_count: 5
---

# EL triggered validator Pause

EIP 7002 ([EIP-7002: Execution layer triggerable exits](https://eips.ethereum.org/EIPS/eip-7002)) introduces a mechanism for allowing withdrawal addresses to trigger exits and potentially partial withdrawals with maxEB ([EIP-7251: Increase the MAX_EFFECTIVE_BALANCE](https://eips.ethereum.org/EIPS/eip-7251))

Another important thing for staking UX could be an ability to PAUSE a validator (previously discussed/raised by [@MicahZoltu](/u/micahzoltu) on github or other discussion forums). Various kind of Pause UX can be build upon:

1. Pause validator for a specific time after which it goes active automatically
2. Pause validator and wait for re-activation trigger again via withdrawal credentials

While 2. is more flexible, 1. seems to be better as the fees for pausing for a particular period can be estimated/charged and burned (for maintaining the validator in `BeaconState`) and also relatively easier to implement.

This would allow stakers to take a break in their operations (for whatever reasons) without going through exits and potentially preventing churn which can cause a bloat in state and unnecessary operational complications.

For maintaining the PoS security, the pause and (automatic or manual) resume will need to be go through activation/exit queues.

## Replies

**nflaig** (2024-01-19):

what time frames is this targeting? feels like this is only worth if you wanna pause operations for multiple weeks / months

---

**g11in** (2024-01-19):

yes ideal timeframe is `weeks` but we can allow whatever timeframe a staker wants to choose as long as he is willing to pay Beacon Chain timeframe based appropriate `rent` (which EL will BURN as some baseFee) for keeping his/her/their validator around.

---

**ensi321** (2024-01-19):

It will need to coordinate with EIP-6914 to distinguish between withdrawn validator and paused validator, which both are seen as inactive in the current protocol.

I like 2. Resume/pause will be very similar to the Activate/withdraw mechanism.

---

**g11in** (2024-01-19):

yes thats correct, 6914 would have to ignore these indices for reallocation.

