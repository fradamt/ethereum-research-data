---
source: magicians
topic_id: 22591
title: Client testing call #21, January 20, 2025
author: parithosh
date: "2025-01-20"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/client-testing-call-21-january-20-2025/22591
views: 140
likes: 2
posts_count: 1
---

# Client testing call #21, January 20, 2025

**Pectra:**

**Client updates:**

**Nethermind:**

- Progress is on track; requires updates for blob base fee, baseFeeUpdateFraction, and EIP-7702.
- Changes are straightforward and expected to be completed within a few days.
- Encountering some test failures on Hive, particularly with the consume engine. The team is investigating.

**Erigon**

- Work in progress; several Hive tests are failing.
- The team is addressing the issues and expects resolution in a few days.

**Besu**

- All tests failing due to a missing genesis file for block fee, which has been merged recently.
- Execution spec tests are still in progress.
- Hive tests will soon specify the base fee, requiring updates from all clients.

**Reth**

- Awaiting EIP-7702 changes and plans to check the base fee update change on the main branch.
- Question on timeline:
- Pari: Timeline details will be shared by Tim in the coming weeks. Fork expected around the 3rd week of February, providing sufficient time for releases.

**Other Updates**

- Pectra-devnet-5 remains available for clients.
- Image updates can be requested from Rafael or Pari.
- MEV workflow now works on all CLs except Nimbus and Prysm
- Work continues on Flashbot builder.
- Holesky launch date is undecided but will allow ample discussion time.

**EIP-7702 Discussion (Delegation Introspection)**

- Julian: Overview of proposed changes discussed in the last ACD call. Changes received positive reviews, aiming for a temperature check on implementation ease.
- Open PRs: PR 9248, PR 9250
- Updates indicate willingness to implement from Besu, Nethermind, Reth, and Erigon. PRs will be merged in after comments are resolved.

**Next Steps:**

- Move forward with Pectra devnet 6 or a shadowfork, incorporating a new genesis file and validator set increase to 50,000–100,000.
- Mario will release updates with EIP-7702 changes and fixes. Expect an EELS/EEST release this week.

**PeerDAS**

- Manu (Prysm): Rebase completed; focus shifts to Lighthouse and others in the coming days.
- Local interop expected in a few weeks, followed by a PeerDAS devnet.

**EOF Update**

- Fuzzing is ongoing but not comprehensive; clients are at varying implementation stages.
- Plans remain unchanged, targeting late Q1 to early Q2 for a devnet.

**Additional Notes**

- Marek highlighted test issues on Hive for nethermind; Mario to investigate.
- Mario reassured all required tests are in the Cancun folder and will be in release 1.3 before the next ACD call.
