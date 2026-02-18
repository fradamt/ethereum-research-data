---
source: magicians
topic_id: 22975
title: Portal Implementers Call #46
author: system
date: "2025-02-24"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/portal-implementers-call-46/22975
views: 41
likes: 0
posts_count: 2
---

# Portal Implementers Call #46

## Meeting Info

- Feb 17, 16:30 UTC
- Duration: 30 minutes
- Meet link: shared in EthR&D#portal-dev
- Recap: Portal Network Implementers Call Notes - HackMD (updated after each call)

## Agenda

- Team updates
- Review deployment plan for Ephemeral headers

[GitHub Issue](https://github.com/ethereum/pm/issues/1300)

## Replies

**Chloe** (2025-03-24):

### 1. General update

- Update on Berlin summit by Piper

Working on multiple talks for the summit

Portal implementer call schedule for the next 2 weeks

- March 3rd: Client team attendance uncertain; Confirmation of the call will be posted on the ethereum/pm github issue
- March 10th: No call expected due to the Berlin in-person event

### 2. Team update

- Update on Shisui by Grapepapa on EthR&D Discord

Ephemeral headers: Implemented the spec changes, incl. SSZ union removal, None removal in BlockHeaderWithProof, and add validation for post-Capella proof
- trace_offer API: Work in progress
- Geth integration: No updates this week
- Berlin event: All team members have their visa ready

Update on [Trin](https://github.com/ethereum/trin) and [Glados](https://github.com/ethereum/glados) by [Jason Carver](https://github.com/carver), [Milos](https://github.com/morph-dev) and [Nick](https://github.com/njgheorghita)

- Trusted block root: Now embedded instead of requiring command-line input
- Database migration

Added progress tracking to display stats during the migration
- Decided not to migrate post-merge headers with proofs, but still keep the post-merge block & receipts

Beacon network: Added a pruning task to remove outdated light client bootstrap data
Glados

- Now able to track database entries for every transfer failure, even if the audit succeeds
- Working on the state audits for block 21 million, expected to have a PR soon

Add e2hs file format proposal

- Proposed a new file format to be used in the History Network for storing pre & post-merge history data
- Feedback from the Nimbus team is needed to understand why receipts were excl. and whether should be incl. directly or stored separately
- Further discussions will take place in Berlin to gather feedback and finalize decisions on this format

Update on [Ultralight](https://github.com/ethereumjs/ultralight/tree/master) by [acolytec3](https://github.com/acolytec3)

- SSZ container discrepancy: Found and fixed a mismatch between the implementation and the spec for post-merge pre-Capella headers; Now passed all related portal spec tests
- Hive tests

Aim to rerun the hive tests to verfiy the fix works
- Noticed that some gossip tests for pre-merge blocks are failing, pending further investigation

Ephemeral headers

- PR is ~25% complete, with fundamental work completed, incl. storing and advertising headers via the ping extension
- Work remains on handling gossip and responses for content retrieval

Update on [Samba](https://github.com/meldsun0/samba) by [Meld](https://github.com/meldsun0)

- Hive tests: Passed 50+ tests related to the offer input, while some still failing
- Recursive lookup: Work on implementing and finalizing the necessary endpoints
- Additional endpoints: Implemented endpoints needed for testing the offer endpoint, including local content and history store
- Besu integration: Planning to start research and integration in the coming weeks

### 3. Review ephemeral headers deployment plan

- Deployment target for this week

Aim to remove SSZ union and enforce proofs for pre-merge headers

Client readiness

- On the call, Trin and Ultralight are ready to deploy the change
- Pending coordination with Fluffy and Shisui

Next steps

- Confirm readiness from Fluffy and Shisui on discord
- Team will move forward if the majority of the network is ready, even if some clients are temporarily offline

