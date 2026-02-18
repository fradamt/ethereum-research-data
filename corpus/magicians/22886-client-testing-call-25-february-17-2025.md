---
source: magicians
topic_id: 22886
title: Client testing call #25, February 17, 2025
author: abcoathup
date: "2025-02-18"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/client-testing-call-25-february-17-2025/22886
views: 52
likes: 0
posts_count: 1
---

# Client testing call #25, February 17, 2025

# Testing call on 17/Feb/2025:

Notes by [@marioevz](/u/marioevz) *(Copied from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1341065731885760662))*

### MEV on Pectra Devnet-6 status:

- MEV-boost is currently running, but there are issues with withdrawal and consolidation requests. Ryan from Flashbots is currently working on this.
- Reth builder (rbuilder) is working but it’s currently not including execution requests
- Pk910 offered to send more deposit/withdrawal/consolidation request transactions to the devnet if either team needs them for testing.

### Mainnet shadow-fork

- Currently underway with all client releases, expected to be completed in 1-2 days.

### Client updates on Pectra

#### Erigon

- Released a version based on Erigon 2, that is compatible with Pectra.
- No official release for Erigon 3 yet because they want to support their internal CL implementation (kaplin), which has encountered some issues.
- An official Erigon 3 release may be available in a day or two.
- Erigon encountered issues with Kurtosis pectra tests on Devnet-6 that weren’t present on Devnet-5.
- pk910 is investigating the cause: It could be two lengthy tests in Assertor that take 30 hours to run, and work is needed to stabilize these tests.
- Erigon also tried to include Assertor directly in the CI and suggested introducing an option to split these lengthy tests into a separate test suite. #### Nethermind
- Released a new version
- All hive tests passed. #### Besu
- Released a version last week
- All hive tests passed without any known issues. #### Teku
- There’s an impact on attestation aggregation: Prior to pectra there were 128 attestations in a block, now we have 8 attestations aggregated.
- Optimizations are necessary to include attestations correctly in the block, but this is not part of the current release.
- Potentially there will be another release before mainnet. #### Prysm
- Confirmed that they have the attestation bug as well.
- They plan to release at least one more version or possibly two before the mainnet.
- They also have a few more features that missed the cut for the Devnet release which should be included in the following releases. #### Grandine
- Release is now available.
- Testing looks good so far. #### Lodestar
- Released version 1.27.
- A couple of cleanup stuff remaining, but nothing urgent.

### Sepolia and Holešky System Contract Deployments for EIP-2935

- Mario from EEST will try to make the deployments.
- Will reach out to lightclient if he encounters any issues.

### Peerdas:

- Devnet is still stable.
- We are experiencing issues with sync tests due to the pinned Geth version used. A plan is being developed in the peerdas-testing chat.
- There’s a potential Peerdas update that may require involvement from the Eth R&D team. EL teams were asked attend the Peerdas breakout call tomorrow:
- Potential new transaction type that includes KZG commitments.
- Discussion currently ongoing here: ⁠allcoredevs⁠

### EOF

- Devnet-0 launched last week:
- Geth RPC node was offline due to an outdated Geth node, which brought down the explorer but nothing major.
- Nethermind deployed fixes to issues they encountered.
- Node 1 in Reth stopped, while Node 2 didn’t fork, possibly due to a misconfiguration, but more investigation is required.
- The execute remote command is being used, which may cause some flakiness in the test execution due to the nature of sending test transactions, which can be improved, but overall Danno mentions this is an useful tool.
- Overall, there were no unexpected problems.

### New Eth R&D Discord Bot for Devnet Monitoring

- The new bot, EthR&D, is taking over some of the EthPandaOps work.
- Can be found on Discord at ⁠pectra-devnet-alerts.
- It pings clients if there are any issues in Devnets:
- Displays the client that is hitting the issue, the node, the type of issue, the SSH command to log in, and more.
- Triggers if the head of the chain isn’t advancing, or the finalized epoch isn’t advancing, sync failures, etc.

### New Hive UI from EthPandaOps

- The new Hive UI is available at https://hive.ethpandaops.io/pectra-devnet-6/.
- Thanks to @skylenet from the EthPandaOps team, who has been working on this for the past month.
