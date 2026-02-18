---
source: magicians
topic_id: 22816
title: Client testing call #24, February 10, 2025
author: parithosh
date: "2025-02-10"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/client-testing-call-24-february-10-2025/22816
views: 83
likes: 1
posts_count: 1
---

# Client testing call #24, February 10, 2025

## Key Decisions & Next Steps

- Going ahead with testnet Pectra forks:
Announcement in ACD channel; client teams should prepare for releases. Dates can be found here.
- Tx Pool Tests:
Testing team is currently working on them.
- PeerDAS:
PeerDAS-devnet-4 is now live, planning for future devnets has started.
- EOF Testing:
Kurtosis-based testing now works, EEST is going to be used to trigger bugs at the start.
- ePBS & IL Testing:
Proceed with standalone domain testing before considering mainnet inclusion. Kurtosis integration is complete.

## Devnet 6 Updates

### Devnet 6

- ~95% participation rate, stable devnet with no large unknown issues
- MEV relay of flashbots still has a validation issue, that’s being fixed soon.
- Lighthouse noticed a kzg verification edge case that they are trying to triage.
- Prysm fixed a cache issue last week.
- Kurtosis is updated; most clients are passing all the Hive tests.

## Testnet Pectra fork

- All clients present confirmed going ahead with the testnet release. The other clients will chime in on discord.

## PeerDAS

- PeerDAS Devnet 4 is live and stable so far.
- Out-of-memory bug in Prysm; PeerDAS test scheduled for tomorrow.
- Full focus after Pectra completion. Hence the planning of devnet-5 has already stared.
- Peerdas devnet 5 spec
- Note: The breakout room has been moved to be weekly instead of once every two weeks.

## EOF Testing

- Kurtosis integration is complete, 3 client devnets can now be locally spun up
- EEST is being used to trigger bugs in the local devnet, some changes are required and will be discussed with the testing team.

## ePBS & Inclusion List (IL) Testing

- Standalone domain testing for IL & ePBS is ongoing.
