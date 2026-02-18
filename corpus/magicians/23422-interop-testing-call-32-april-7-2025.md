---
source: magicians
topic_id: 23422
title: Interop Testing Call #32 – April 7, 2025
author: poojaranjan
date: "2025-04-07"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/interop-testing-call-32-april-7-2025/23422
views: 134
likes: 1
posts_count: 1
---

# Interop Testing Call #32 – April 7, 2025

**Facilitator:** Parithosh Jayanthi

### Next Steps

- Pari to follow up with Nimbus on attestation packing fix.
- Daniel to provide update on Besu teams validators running into hardware bottlenecks.
- DevOps to:

Prepare and execute a round of mainnet shadow fork testing.

**DevOps** to update `eth-clients` metadata for the fork date.
**Testing teams** to continue running tests and raise issues as needed.
**Problabs** will publish Blob analysis results.
**Danno** to submit PR for EIP editors’ review by tomorrow.

- Update and finalize test plan.
- Add more clients to EOF Devnet 1.
- Plan Devnet 2 (including opcodes).

Parithosh and team will begin internal planning for Fusaka Devnet post-EOF.
Parithosh will prepare for livestreaming of future testing calls.

## Pectra – Hoodi

- Pari: Validator tests are complete; all intended features have been covered and the network looks stable.
- Pari: Noted an orphan block on Sepolia (by Teku); believed to be a one-off, and Teku is investigating.
- Sam: Continuing to analyze attestation performance.
- Terence (Prysm team):

Prysm updated attestation handling – changes merged.
- No bugs reported; focus currently on proposer logic, not full network analysis.

**pk910**: Cross-withdrawal address consolidation is still pending, but other teams have tested and confirmed it’s feasible.
**Pari**: Will wait to see if **Nimbus** corrects attestation packing.
**Nico**: No notable changes in the last 7 days.
**Daniel**:

- Tested 25k validators on one Lighthouse node.

## Specs & MEV Testing

- Mario Vega: Specs testing ongoing. Test suites being re-reviewed and executed against all clients. No major issues found yet.
- MEV testing is active – consistent stream of MEV blocks being observed.
- Partition tool has been used to gather client-side fixes, collected from clients’ retrospective reviews.
- Pawan: Diff fuzzer has been running all EF test cases for a week – no crashes so far.
- Terence: Mainnet fork date update required in upstream specs.
- nflaig: Confirmed that update is likely only needed at:
eth-clients/mainnet/config.yaml
- Pari: DevOps team will handle the update in the repo.

## PeerDAS

- Pari shared link: PeerDAS Devnet 6
- Barnabas Busa:

Devnet 6 setup in progress with Kurtosis.
- Lighthouse and Grandine clients integrated.
- Geth team aware of issues; fix pending.

**Marius**: Code is fixed but slow; better hardware may help.
**Pari**: PR submitted by Barnabas to Kurtosis. All spam tools expected to work.
**Problabs** is analyzing mainnet blob usage; report to be published in coming days.
**Marius**: Geth does not yet support **RPC v2** – patch expected tomorrow.
**Barnabas**: Asked for clarification – whether the fix relates to a v1 wrapper. Parithosh confirmed it.

## EOF (EVM Object Format)

- Danno:

Working to roll out specs for EOF.
- Test plan (including EEST) will be updated.
- EVM 1 is already running EEST.
- Having 3 clients running will be nice to have – aiming for more.

ETA for **EOF Devnet 1** aligns with Pectra fork timeline.
**EOF Devnet 2** will include Opcode changes.
**Pari** asked if PeerDAS EL version is easy to rebase.

- Marius + Roman: Confirmed rebasing is straightforward.

After EOF Devnet 1 is stable, **Fusaka Devnet** planning will start (Interop, June).
**Pari** shared: [EOF Devnet 1](https://notes.ethereum.org/@ethpandaops/eof-devnet-1)
Livestreaming:

- Danno: Shared concerns but agreed livestreaming will be needed eventually.
- Async fallback: Use Party Lounge when needed.
