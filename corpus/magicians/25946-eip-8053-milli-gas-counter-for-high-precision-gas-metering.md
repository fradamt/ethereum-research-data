---
source: magicians
topic_id: 25946
title: "EIP-8053: Milli-gas Counter for High-precision Gas Metering"
author: misilva73
date: "2025-10-24"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-8053-milli-gas-counter-for-high-precision-gas-metering/25946
views: 51
likes: 0
posts_count: 2
---

# EIP-8053: Milli-gas Counter for High-precision Gas Metering

Discussion topic for EIP-8053; [PR](https://github.com/ethereum/EIPs/pull/10563)

#### Abstract

This proposal introduces the `milli-gas` counter as the EVM’s internal gas accounting. Gas costs are defined in `milli_gas` and internal EVM gas accounting is entirely carried out in `milli_gas`. At the end of transaction execution,`milli_gas` is rounded up to `gas`. Gas limits and transaction fees are still computed and verified using the current `gas_used` counter. This new counter enables a more precise accounting of cheap compute without impacting UX.

## Replies

**duncancmt** (2026-01-04):

it seems to me that the EIP as currently published conflates whether the `GAS` opcode ought to report the higher-level divide-by-1000-round-up gas concept or the lower-level milli-gas concept. as a consequence, the following statements are confusing:

> At the same time, after the transaction is executed, evm.milli_gas_left is rounded up to evm.milli_gas_used = ceil(evm.milli_gas_used / 1000).

seems like this should state `evm.milli_gas_used = ceil(evm.milli_gas_used / 1000) * 1000`

> The GAS opcode reports the available gas in milli-gas units.

> *CALL opcodes receive the amount of gas to send to the sub context to execute in gas

latter two, when read literally, suggest that the common idiom of `GAS` => `CALL` results in forwarding 1000x (obviously not realizable, for several reasons) the gas available in the current context.

---

for myself, as a dApp programmer, I recommend keeping the semantics for `*CALL` as written in the text of the EIP, but modifying the semantics of `GAS` such that it reports `floor(milli_gas_left / 1000)`, to preserve *rough* compatibility with existing dApps as much as possible. this hides the details of milli-gas implementation from the VM to a significant degree. with this modification, I can sincerely endorse this EIP as a Good Idea™

as a footnote, I also recommend that the EIP-150 all-but-one-64th rule be applied to *gas* and not to milli-gas before the amount of gas forwarded is converted to milli-gas inside the newly-created context. this seems like the obvious way to do it given the text of the EIP, but it seems to me that it ought to be explicitly stated for the avoidance of any doubt.

