---
source: magicians
topic_id: 22917
title: All Core Devs - Consensus (ACDC) #151, February 20, 2025
author: system
date: "2025-02-19"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-151-february-20-2025/22917
views: 226
likes: 2
posts_count: 2
---

# All Core Devs - Consensus (ACDC) #151, February 20, 2025

# Consensus-layer Call 151

#### Agenda

[Consensus-layer Call 151 · Issue #1280 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1280) moderated by [@ralexstokes](/u/ralexstokes)

**
Agenda**

[prev: call 150](https://github.com/ethereum/pm/issues/1265)

Meeting Date/Time: [Thursday 2025/2/20 at 14:00 UTC](https://savvytime.com/converter/utc/feb-20-2025/2pm)

Meeting Duration: 1.5 hours

[stream](https://youtube.com/live/RMXhEnc4PZk?feature=share)

1. Electra

devnet-6 open questions?

attestation aggregation under EIP-7549
2. testnet readiness
3. PeerDAS / Blob scaling

peerdas-devnet-4
4. Bump up Fulu blob count
5. Migration of proof computation to transaction sender, vs beacon node

Offloading Proof Computation from Beacon Nodes to Transaction Sender - HackMD
6. BPO forks
7. Research, spec, etc.

Max blobs and hardware requirements update
8. Open discussion/Closing remarks

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png)

      [All Core Devs - Consensus (ACDC) #151, February 20, 2025](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-151-february-20-2025/22917/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDC #151 summary
> Action Items
>
> Pectra Holesky fork at epoch 115968 (Feb. 24, 21:55 UTC)
>
> Update any infrastructure and be prepared to monitor the hard fork!
> Pectra Testnet Announcement | Ethereum Foundation Blog
>
>
> Review attestation performance on the upcoming mainnet shadowfork and on Holesky (following discussion of EIP-7549 impact)
> Last call for EIPs recommending minimum hardware requirements and the associated “max blobs” flag
>
> Add EIP: Hardware and Bandwidth Recommendations for Validator…

#### Recording

  [![image](https://i.ytimg.com/vi/RMXhEnc4PZk/hqdefault.jpg)](https://www.youtube.com/watch?v=RMXhEnc4PZk&t=230s)

#### Writeups

- Crypto & Blockchain Research Reports | Galaxy by @Christine_dkim

#### Additional info

- Testnets:

Pectra-devnet-6
- Ephemery testnet
- Pectra Testnet Announcement | Ethereum Foundation Blog

Last call for [Pectra Retrospective](https://ethereum-magicians.org/t/pectra-retrospective/22637)

## Replies

**ralexstokes** (2025-02-22):

**ACDC #151 summary**

**Action Items**

- Pectra Holesky fork at epoch 115968 (Feb. 24, 21:55 UTC)

Update any infrastructure and be prepared to monitor the hard fork!
- Pectra Testnet Announcement | Ethereum Foundation Blog

Review attestation performance on the upcoming mainnet shadowfork and on Holesky (following discussion of EIP-7549 impact)
Last call for EIPs recommending minimum hardware requirements and the associated “max blobs” flag

- Add EIP: Hardware and Bandwidth Recommendations for Validators and Full Nodes by kevaundray · Pull Request #9270 · ethereum/EIPs · GitHub
- Add EIP: Max blob flag for local builders by kevaundray · Pull Request #9296 · ethereum/EIPs · GitHub

**Summary**

- Pectra

devnet-6 is stable and looking good!
- Still working on Pectra-compatible MEV builder

some final bugs with execution requests, investigation is ongoing

Pectra system contracts are live on Holesky, Sepolia, and Mainnet

- Check the respective EIPs for system contract addresses

We discussed attestation aggregation algorithms clients use and updates required in Pectra following EIP-7549

- Prysm found an issue with suboptimal packing
- Teku suggested their approach by normalizing the new attestation type to the existing attestation type where clients have long-standing and battle-tested algorithms to handle

PeerDAS / blob scaling

- peerdas-devnet-4 is underway; some notable issues:

ELs should be able to disable EOF so that PeerDAS can be tested in isolation
- Migration of proof computation from the CL to the EL

Needs an update to the network wrapper for blob transactions
- Spec update: Update EIP-7594: include cell proofs in network wrapper of blob txs by fradamt · Pull Request #9378 · ethereum/EIPs · GitHub
- More info: Offloading Proof Computation from Beacon Nodes to Transaction Sender - HackMD
- We discussed this change a bit on this call, but ultimately decided to move to next weeks’ ACDE for EL input.

Announcement of `peerdas-devnet-5`: https://peerdas-devnet-5.ethpandaops.io/
`jimmygchen` assembled a PeerDAS readiness checklist to know when we are in a place to move ahead with the PeerDAS feature in Fusaka; please take a look!

- pm/Fusaka/peerdas-readiness.md at master · ethereum/pm · GitHub

Discussion around how to scale blob counts in Fusaka

- The current spec parameter is much lower than the theoretical maximum.
- We agreed to commit to pushing the development as far as we can while keeping networks stable.
- We may desire to ship PeerDAS to mainnet at a lower blob count to derisk the new mechanism, but then will want some way to scale to the expected maximum (and ideally without a formal new hard fork, as this implies a lot of boilerplate in CL clients)
- Mark brought up the proposal of BPO forks (Blob-Parameter-Only (BPO) forks) to navigate the rollout

For example: ship PeerDAS at half the theoretical max, and also have the infrastructure in clients to programmatically increase the blob count without a new named fork

Dankrad suggested a smart contract implementation maintained by client devs that would provide the blob parameters to scale up without a new hard fork. Another idea suggested is to put the blob parameters under control of validators like the gas limit today.
Keeping all of these options in mind, we agreed to see how PeerDAS R&D goes where we will wait for more data from PeerDAS devnet performance to see what the exact scaling strategy will be.

Updates on minimum hardware requirements

- PR to set minimum hardware requirements: Add EIP: Hardware and Bandwidth Recommendations for Validators and Full Nodes by kevaundray · Pull Request #9270 · ethereum/EIPs · GitHub
- PR to describe a “max blobs” flag for local block builders to customize their build process: Add EIP: Max blob flag for local builders by kevaundray · Pull Request #9296 · ethereum/EIPs · GitHub
- We discussed the interplay between this “max blobs” flag and the getBlobs mechanism, where the flag could not apply if blobs are already present in the mempool (and can be fetched with getBlobs).
- We also touched on the consideration of validator profitability in light of the suggested minimum hardware requirements

There was quite a bit of nuance here, so check the call for the full discussion.
- As a summary, there are ideas around improving the economics of staking in the future which could change the sustainability of full nodes and/or validators. It is possible that these macro-level improvements could change the extent to which the protocol subsidizes hardware costs today and that would have direct impact to the minimum hardware requirements to participate rationally.
- We agreed that we should not let staking economics artificially constrain hardware requirements (e.g. having low in-protocol rewards imply hardware specs that get in the way of scaling the L1), and that we will keep revisiting this question given all of the uncertainty around the future of staking.

