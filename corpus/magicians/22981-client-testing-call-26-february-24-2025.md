---
source: magicians
topic_id: 22981
title: Client testing call #26, February 24, 2025
author: abcoathup
date: "2025-02-24"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/client-testing-call-26-february-24-2025/22981
views: 53
likes: 0
posts_count: 1
---

# Client testing call #26, February 24, 2025

## Testing Call 24/Feb/2025

Notes by [@marioevz](/u/marioevz) *(Copied from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1343604407891398717))*

### MEV:

- Flashbots identified an issue and are working on a fix, aiming for Holesky.
- Prysm and Nimbus are progressing on SSZ & Builder API : ⁠Builder workflow with SSZ⁠
- MEV Tests are using local devnets using kurtosis.

### Pectra Mainnet Shadow Fork

- No progress: Clients could not be synced due to infrastructure issues.
- There was an issue getting mainnet data to the nodes.
- Rafael started working on a fix.
- Expected to be resolved today or tomorrow.

### Client updates on Pectra

#### Erigon, Geth, Teku

- No updates.

#### Nethermind

- Marek: still everything good.

#### Besu

- Daniel: still everything good with the release.

#### Reth

- Roman: Local nodes updated, no major issues.

#### Prysm

- James: Looking to merge https://github.com/prysmaticlabs/prysm/pull/14896, which is one of the attestation related items. The solution is still being reviewed.

#### Grandine

- Saulius: A few small fixes, might wait for a few days for a release, but nothing major.

#### Lighthouse

- Pawan: Lighthouse is still on 7.0.0-beta.0 for holesky.

#### Lodestar

- Potential hot-fix for an issue caught during gnosis testing, which is also relevant for holesky.
- Issue was not caught by local testing.
- Issue related to compounding of a validator that is being loaded from DB, and only happens during proposals.
- fix: ensure new withdrawalCredentials in switchToCompoundingValidator() by twoeths · Pull Request #7478 · ChainSafe/lodestar · GitHub
- Nethermind team could share the details regarding the test case that triggers the issue.

### PeerDAS

- Rafael: Devnet-5, same spec as Devnet-4 and is basically a relaunch, which fixed the client versions issues that caused the problem in Devnet-4.
- Devnet 5 Tooling: PeerDAS Dashboard

### EOF

- Danno: Devnet-0 is a success
- 3+ clients in sync in the Devnet-0.
- Reth fell out for a bit but caught up afterwards.
- Devnet-1 will contain all EIP changes, and will be longer lived than Devnet-0 to allow public access to deploy and test EOF contracts.
- Evmone will have a proof-of-concept for TXCREATE over the next couple of weeks, which will allow EEST to fill tests and make fixes.
- Rafael: Suggested having a hive dashboard for the status of the clients passing EOF tests.
- Requires an EOF EEST release. Mario will work on this.
