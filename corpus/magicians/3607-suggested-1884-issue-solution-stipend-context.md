---
source: magicians
topic_id: 3607
title: Suggested 1884 issue solution (stipend context)
author: tkstanczak
date: "2019-08-30"
category: EIPs > EIPs core
tags: [evm, core-eips, core-devs]
url: https://ethereum-magicians.org/t/suggested-1884-issue-solution-stipend-context/3607
views: 1202
likes: 0
posts_count: 1
---

# Suggested 1884 issue solution (stipend context)

EIP-1884

Solution 1) (stipend fix only)

The idea is to use the fact that when calling with a non-zero value, 9000 gas is used instead of 700.

Moreover this 9000 is calculated as a cost of the caller and callee account balance updates (two state updates).

Since these accounts will be cached by the clients, an attacker would have to keep calling a different predeployed contract each time to take advantage of the discounts proposed below in a loop and (in order to cause clients to load and update non-cached accounts). Attacker would have to pay 9000 for each call and significant amount of gas for each of the target contract deployments before the attack and additional gas for storing the target contract addresses in the calling contract storage before executing an attack. In such scenario, the attack should be prohibitively expensive.

(in such attack we get 9000 (non-zero value call) - 700 (standard call cost) gas for free to minimize the impact of the proposed stipend discount.

Let us introduce a short (2-byte) STIPEND_USE counter on EVM state (state at the current EVM call).

Let us introduce a boolean STIPEND_AVAILABLE variable on EVM state (for better performance of gas updates).

At the beginning of any call set STIPEND_AVAILABLE to true when TRANSFER_VALUE > 0 && CALL_DEPTH > 0.

STIPEND_USE starts at 0

each time GAS_USED is increased

if (STIPEND_AVAILABLE) increase the STIPEND_USE by the same amount

then if STIPEND_USE >= 2300 SET STIPEND_AVAILABLE to false

if (!STIPEND_AVAILABLE) do nothing

Now set price of SLOAD to:

800 if NOT(STIPEND_AVAILABLE)

200 otherwise

Now set price of BALANCE to:

700 if NOT(STIPEND_AVAILABLE)

400 otherwise

Now set price of EXTCODEHASH to:

700 if NOT(STIPEND_AVAILABLE)

400 otherwise

The client memory cost is ~3 bytes per call depth

The client performance cost is a ulong to short cast + short addition + short comparison when STIPEND_USE is below 2300, then one boolean check for each gas update

Maintenance cost - amortized since we can use this solution for any repricing in the future, additional logic in GAS_USED updates.
