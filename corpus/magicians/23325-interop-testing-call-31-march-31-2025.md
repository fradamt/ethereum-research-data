---
source: magicians
topic_id: 23325
title: Interop Testing Call #31 – March 31, 2025
author: poojaranjan
date: "2025-03-31"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/interop-testing-call-31-march-31-2025/23325
views: 117
likes: 0
posts_count: 1
---

# Interop Testing Call #31 – March 31, 2025

**Facilitated by:** Parithosh Jayanthi

## Next Steps

- Lucas is working on block reward and effectiveness analysis; results to be shared once available.
- Mario will prepare more EEST tests and a potential release.
- Tim Beiko & Stokes will collect async input and coordinate the decision on the Pectra mainnet fork block date.
- Parithosh will create a tracking page for EOF Devnet 1, potentially combining testing EOF with PeerDAS Devnet 6.

## Hooodi Testnet

- Pectra fork occurred last Wednesday.
- Testing details:

PK910: EL-triggered exit seems fine.
- Partial withdrawals yet to be tested.
- Some pending in deposit queue – to be followed up.
- Initial testing with 7702 completed.

## Attestation Issues

- Pari: No major outages so far, but attestations not behaving as expected. Discord thread
- Enrico: Haven’t looked very closely, but essentially clients lack optimal attestation packing algorithms. It was a big problem on testnet but not on mainnet.

Teku still has a naive version; updates planned.
- A bug affecting attestation propagation fixed in latest Teku release.

**Pari**:  Most of the issues were on scaling up.
**Enrico**: Teku running very big number of attestation and takes close to 3sec to publish. If running 5k validator, it should not be a problem.
**nflaig**: Double checked the metrics. Only timely target attestations get rewarded. Many don’t make it to the next block.
**Saulius**: Some clients not packing blocks efficiently; could be identified by comparing client behavior across the same slot.

- Currently no exact data; proposing a joint client comparison effort.

**Pari**: Confirmed the lack of current metrics.
**Nico**: Acknowledged the difficulty but noted that some patterns might be visible through existing data.
**Nico**: Mentioned that Lucas is conducting an analysis on block rewards and other metrics, and more data should be available soon.
**Saulius**: Proposed a joint effort to test and compare client performance for the *same slot*, which could yield clearer insights.
**Nico**: Not entirely convinced it’s critical to compare within the same slot but agreed it might be ideal.
**Pari**: Suggested checking with the Vouch team, who may already have relevant data.

**Next step**: Parithosh will check with Vouch team, they might have helpful data.

### Effectiveness Concerns & Performance Metrics

- nflaig: If this goes live on mainnet as-is, users will likely complain about reduced effectiveness—even if it’s not a critical network risk.
- Parithosh: Agreed, users are accustomed to high performance and will notice the drop.
- nflaig: Users already complain when effectiveness drops from 99.9% to 99.7%.
- Marius: Asked for current effectiveness metrics.
- Parithosh: Head rate is fluctuating between ~75% and 88%, while it should ideally be around 92%.
- Marius: That’s a significant drop.
- Parithosh: It definitely needs to be fixed before mainnet. It’s an optimization issue, not a bug.
- Marius: A 17–4% drop is major—why wasn’t this caught earlier? Could it be related to the change from 256 to 8 aggregates per block?
- Parithosh: it’s an optimization issue, not a pure bug. Issues like this require a public network to surface; they may not appear in smaller-scale testing environments.
- nflaig: Lodestar runs 5k keys per node – may perform better on mainnet.

## Client-Specific Updates

- Parithosh mentioned that Potuz shared a Fork choice issue that is fixed in Prysm.
- Pawan: The issue was related to epoch processing in Lighthouse. It performed balance updates twice during a single pass, which caused the problem. Most clients are now aware of the issue, and it has been fixed.Lighthouse fix PR
- Pawan: Working on improved fuzzing to detect similar issues earlier.
- Mario: Some RLP tests were ran locally, EIP-7702 tests passed across all clients; planning a test release next week.

### Pectra Mainnet Block Discussion

- Tim Beiko: Asked how the group should approach selecting the Pectra fork block.
- Barnabas Busa: Suggested deferring the discussion to Thursday’s ACD call.
- Parithosh: Proposed doing a temperature check in the meantime.
- Stokes: Supported a temp check, noting uncertainty among CL teams given recent updates.
- Pawan: Expressed low confidence at the moment.
- Nixo: Highlighted that confirming April 30 on April 3 would break the 30-day notice commitment.
- Pawan: Requested a few more days to complete fuzzer runs.
- Stokes: Asked if teams are comfortable with April 30 “vibes-wise.”
- Stokes: Requested if specs could be released earlier than Wednesday.
- Justin Traglia: Confirmed specs could be released sooner.
- Som (Erigon): No objections to April 30 but suggested May 5–6 as a backup if the decision is made Thursday.

**Next step**: Tim and Alex will collect more decision data points from async chat.

## PandaOps & Coordination Tools

- Hive dashboard for tracking.
- PandaOps bot available in interop Discord channel.
- Dedicated Discord channels for:

Pectra
- EOF
- PeerDAS

Client teams feel free to tag PandaOps as needed.

## PeerDAS Updates

- Will is helping with coordination and devnet spec updates.
- Current status:

Geth PeerDAS implementation still under test.
- n/m implementation is there, yet to tested. Bug in Prysm has been fixed.
- Waiting on clients to havegetblob v2 support.

Will be discussed in upcoming **PeerDAS testing call**.

## EOF (EVM Object Format)

- Danno:

Devnet 0 running.
- Erigon added fuzzing.
- EOF Devnet 1 will follow after Pectra mainnet release.
- Working on devnet release and EIP updates.
- Will ping Discord once specs are finalized.

**Pari**:

- Suggests combining EOF Devnet 1 and PeerDAS Devnet 6.

**Next step**: Parithosh Will create a devnet tracking page.

(If anything is missed, please add [here](https://hackmd.io/@poojaranjan/InteropTestingNotes#Interop-Testing-Call-31-%E2%80%93-March-31-2025)).
