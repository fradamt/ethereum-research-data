---
source: magicians
topic_id: 25200
title: EIP-7732 Breakout Room Call #22, August 29, 2025
author: system
date: "2025-08-21"
category: Protocol Calls & happenings
tags: [breakout, epbs]
url: https://ethereum-magicians.org/t/eip-7732-breakout-room-call-22-august-29-2025/25200
views: 50
likes: 2
posts_count: 4
---

# EIP-7732 Breakout Room Call #22, August 29, 2025

### Agenda

1. Payload Post-State Availability in the EVM (EIP-4788 Implications Post-ePBS): Discuss EVM access to beacon state roots post-ePBS, which introduces separate consensus and execution state transitions. EIP-4788 exposes the parent beacon block root (containing a state_root, pre-payload), enabling proofs of pre-payload states (e.g., validator not slashed) but not post-payload states (e.g., consolidation requests processed in payload). Evaluate options:

a. Leave as-is, using state.state_roots for post-payload access (grandparent payload, sufficient for most cases).
2. b. New EIP exposing execution payload envelope root (like EIP-4788, for post-payload proofs).
3. c. Add pre_state_root to beacon block (similar functionality to a).
4. Handling Beacon Block Body Fields Moved to Execution

Description: Decide on fields shifted from CL to EL (e.g., blob_kzg_commitments, execution_requests) Options:

(a) Remove entirely (changes generalized indices; backward compatibility concerns, but no known breakage;
5. (b) Stub as empty, assert in STF (preserves indices, adds tech debt).
6. If removing, consider dropping unused deposits and eth1data (post-Pectra).
7. PR Reviews and Spec Updates

Description: Review open PRs:

PR-4525: Rename execution payload header to bid. link
8. PR-4527: Remove inclusion proof/signed header from Gloas data column. link
9. Rebase block access list on Gloas spec (add to ExecutionPayload).
10. Consider ePBS rebase on EIP-7688 for SSZ consistency.
11. Discuss Potential Impact on Builder API: ePBS MEV Relays Design - HackMD
12. Discuss Process and Timing for Advancing  Spec: epbs-devnet-0 spec

**Meeting Time:** Friday, August 29, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1696)

## Replies

**system** (2025-08-29):

YouTube recording available: https://youtu.be/KYj9iBdT2ew

---

**system** (2025-08-29):

### Meeting Summary:

No summary available. Could not retrieve summary.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: U.0gM#?P)
- Download Chat (Passcode: U.0gM#?P)

---

**system** (2025-08-30):

### Meeting Summary:

No summary available. Could not retrieve summary.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: U.0gM#?P)
- Download Chat (Passcode: U.0gM#?P)

