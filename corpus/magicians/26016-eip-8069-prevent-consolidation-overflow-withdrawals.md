---
source: magicians
topic_id: 26016
title: "EIP-8069: Prevent consolidation overflow withdrawals"
author: aelowsson
date: "2025-10-30"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-8069-prevent-consolidation-overflow-withdrawals/26016
views: 73
likes: 2
posts_count: 2
---

# EIP-8069: Prevent consolidation overflow withdrawals

Discussion topic for EIP-0000; PR

#### Description

Limit a source validator’s movable balance by the target validator’s available room, accounting for already-reserved incoming consolidations.

### Abstract

This EIP modifies EIP-7251 by limiting the balance a source validator can consolidate into a target validator. The transferable amount is capped by the target validator’s available room, defined as `MAX_EFFECTIVE_BALANCE_ELECTRA` minus its current effective balance and any other incoming consolidations already reserved in the queue. This prevents consolidation overflow withdrawals which side-step the intended churn budgets. Incoming consolidations are tracked by adding a `reserved_balance` field to the `BeaconState`.

## Replies

**aelowsson** (2025-11-02):

Superseded by [EIP-8071](https://ethereum-magicians.org/t/eip-8071-prevent-using-consolidations-as-withdrawals/26037).

