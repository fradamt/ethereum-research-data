---
source: magicians
topic_id: 20481
title: All Core Devs - Consensus (ACDC) #137, July 11 2024
author: abcoathup
date: "2024-07-06"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-137-july-11-2024/20481
views: 570
likes: 0
posts_count: 2
---

# All Core Devs - Consensus (ACDC) #137, July 11 2024

### Agenda

[Consensus-layer Call 137 · Issue #1096 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1096)

Moderator: [@ralexstokes](/u/ralexstokes)

### Summary

**ACDC #137 recap**  by [@ralexstokes](/u/ralexstokes) *(from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1261006075818414263))*

Shorter call today!

We began with Pectra:

- CL clients are generally ready for pectra-devnet-1
- CL clients working well with static test vectors
- Given a few EL clients are ready, we should launch pectra-devnet-1 as soon as possible, aiming for sometime next week

Then, turned to PeerDAS:

- peerdas-devnet-1 launched but surfaced a number of client bugs which are being resolved
- Expect a peerdas-devnet-2 soon as client teams continue to iterate on scaling blob bandwidth
- I gave an update on the work to uncouple the blob max and target values between the consensus and execution layers

After reviewing the syncing semantics, it appears the check for the blob maximum on the EL is redundant and we can safely drop that check and have it done solely at the CL
- We also want the same uncoupling treatment for the blob target so this value will be driven by the CL but needs to be included in the EL block header for the security of client sync
- Expect updates to this PR on the CL and an EIP for the 4844 changes soon™!

Wrapped the call with an update on some work to expand the fork choice testing

- Presentation from TXRX research here: FC compliance test suite on ACDC - Google Präsentationen
- This work introduces tooling to expand the scope of the fork choice test suite for static coverage in clients
- Uses a constraint-driven programming language to generate interesting test cases which extend the static test corpus CL clients use for conformance testing
- CTA: CL teams please take a look and incorporate into your client for enhanced coverage

See you next time!

### Recording

  [![image](https://img.youtube.com/vi/IXgfhk_bFwA/maxresdefault.jpg)](https://www.youtube.com/watch?v=IXgfhk_bFwA&t=160s)

### Transcript

[To be added]

### Additional info

Notes by [@Christine_dkim](/u/christine_dkim): [Crypto & Blockchain Research Reports | Galaxy](https://www.galaxy.com/insights/research/ethereum-all-core-developers-consensus-call-137-writeup/)

## Replies
