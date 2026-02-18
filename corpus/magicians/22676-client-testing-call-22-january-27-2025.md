---
source: magicians
topic_id: 22676
title: Client testing call #22, January 27, 2025
author: danceratopz
date: "2025-01-27"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/client-testing-call-22-january-27-2025/22676
views: 85
likes: 3
posts_count: 1
---

# Client testing call #22, January 27, 2025

# Interop Testing Call (Jan 27, 2025)

#### Meeting Summary: Devnet 5, Devnet 6, and Related Updates

### Pectra Devnet 5

- Devnet-5 is finalizing successfully again after addressing key issues.

Dashboard link

**Client Updates**:

- Erigon: Fix implemented, resolving key issues and enabling finalization.
- Lodestar: Syncing is functional but block import issues persist (only 6 blobs present in blocks with more than 6).
- Prysm: Issue under investigation, early stages of debugging.
- Lighthouse: Debugging ongoing; no update yet.
- Geth: Issue appears resolved, pending verification.
- Grandine: Node resynced, debugging continues, and it is now proposing blocks.
- Besu: Block processing issue identified, tracing and debugging underway.

Hive issues remain a blocker for Devnet-5 and need resolution before progressing to Devnet-6.
**Decision**: Continue with Devnet-5 until fixes are in place, then transition to Devnet-6.

### Pectra Devnet 6

- Spec: @ethpandaops/pectra-devnet-6
- Timeline: Tentative release this week, dependent on client readiness and passing Hive tests.
- Consensus specifications are finalized.
- Execution spec test release this week, all PRs in place.
- Plan:

Add Devnet-6 to Hive for clients already passing Devnet-5.
- Clients that pass devnet-6 hive can then join devnet-6.
- Enable MEV from the start of Devnet-6 (Bloxroute ready for testing).

**Next steps**: Ensure all clients address outstanding issues to meet the timeline.

### PeerDAS

- Updates to configuration values shared in the PeerDAS channel.
- Interop testing underway, progressing well.
- Lighthouse team close to PeerDAS devnet readiness, working on improvements and testing stability using Kurtosis on Kubernetes.

### EOF

- Preliminary testnet spec shared: EOF Testnet Plan.
- Initial fuzzing with Geth, Besu, and REVM shows no errors in overnight run—indicating readiness for Osaka Devnet.
- Decision: Launch EOF devnet next week following Pectra spec finalization.

### Hive Updates

- ethpandaops have added a github action for hive, which executes all clients in parallel, resulting in a 6x speedup and at lower cost.
- Hive integration for testing Devnet-6 is a priority, as it remains a critical tool for identifying client issues.

### Key Links Shared in the Call

- Fork Monitor
- Node Monitor GitHub Repo
- Hive Testing Workflow

### Next Steps

- Continue debugging and fixing outstanding issues in Devnet-5.
- Transition to Devnet-6 as soon as Hive tests are passed.
- Plan EOF devnet launch for next week.
- Ongoing PeerDAS and Kurtosis testing to ensure stability over time.

Thanks for the notes [@poojaranjan](/u/poojaranjan)!
