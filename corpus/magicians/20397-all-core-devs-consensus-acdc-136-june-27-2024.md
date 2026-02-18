---
source: magicians
topic_id: 20397
title: All Core Devs - Consensus (ACDC) #136, June 27 2024
author: abcoathup
date: "2024-06-27"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-136-june-27-2024/20397
views: 701
likes: 1
posts_count: 2
---

# All Core Devs - Consensus (ACDC) #136, June 27 2024

### Agenda

[Consensus-layer Call 136 · Issue #1084 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1084)

Moderator: [@ralexstokes](/u/ralexstokes)

### Summary

By [@ralexstokes](/u/ralexstokes) *(from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1256053147085049898))*

- Started with a presentation of some research into private sharing of node information for client diversity purposes
- Then, a discussion of some work from Peter to support stateless validation across multiple execution clients (even before Verkle!). There was a lot of nuance here around the implications and various appetites for support so check the call for the full color. If you’d like to follow up take a look at this proposal
- Pectra was next: implementation for devnet-1 is proceeding well with some CL clients ready to go. EL clients are not far behind which puts us at a devnet-1 launch in the coming weeks.
- Mikhail does have a PR to iterate on Pectra EIP-6110 following discussions for devnet-0, please take a look here
- Next, PeerDAS: the PeerDAS devnet-1 testnet has launched and is proceeding well. There are some minor bugs but clients are fixing to line up the next iteration of PeerDAS
- We also covered a new proposal by Dankrad to migrate the blob base fee calculation into the CL; this complements the proposal to migrate the implementation of the max blob count from where it is today (both CL and EL) to just to the CL. See this comment for links to both proposals
- And last, we had an update around progress on SSZ in clients supporting the inclusion of EIP-7688 in Pectra which allows for the construction of forward-compatible consensus data structures (with respect to serialization)
- Some clients have implemented the necessary features and some have not completed it yet; so we decided to defer the inclusion question to a later call to give client teams time to digest the changes and assess the complexity of implementation weighed against the benefit this feature provides.

### Recording

  [![image](https://img.youtube.com/vi/T-w5dzte36c/maxresdefault.jpg)](https://www.youtube.com/watch?v=T-w5dzte36c&t=95s)

### Transcript

[To be added]

### Additional info

Notes by [@Christine_dkim](/u/christine_dkim): [Crypto & Blockchain Research Reports | Galaxy](https://www.galaxy.com/insights/research/ethereum-all-core-developers-consensus-call-136/)

## Replies
