---
source: magicians
topic_id: 20284
title: All Core Devs - Consensus (ACDC) #135, June 13 2024
author: abcoathup
date: "2024-06-13"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-135-june-13-2024/20284
views: 811
likes: 0
posts_count: 2
---

# All Core Devs - Consensus (ACDC) #135, June 13 2024

### Agenda

[Consensus-layer Call 135 · Issue #1069 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1069)

Moderator: [@ralexstokes](/u/ralexstokes)

### Summary

ACDC 135 summary by [@ralexstokes](/u/ralexstokes):

We began with some announcements:

- Migration of the Kurtosis ethereum-package, see details here: Consensus-layer Call 135 · Issue #1069 · ethereum/pm and be sure to upgrade your infra!
- Request to review Add EIP: Network Upgrade Inclusion Stages by timbeiko · Pull Request #8662 · ethereum/EIPs to add more refinement to different senses of “CFI” in core dev governance

Then discussed Electra `devnet-1` from the CL side:

- Agreed to merge this PR into the devnet-1 specs, which refactors the attestation layout following EIP-7549 and has implications for the SSZ merkelization of this type
- Client teams agreed to target v1.5.0-alpha.3 of the consensus specs for devnet-1 . Be on the look out for release soon™!
- Wrapped this segment with some rough timelines on devnet-1 readiness, most clients seemed to think a couple weeks after the specs release is all that would be needed to get an implementation ready, which means we can keep Pectra moving along

And then moved to PeerDAS work:

- Started by calling out this PR to move PeerDAS to formal inclusion in Pectra to reflect client intent, even if PeerDAS is developed separately from the “core” Pectra set.
- Next discussed how to proceed on PeerDAS development given that we want to work in parallel to the other Pectra work; PeerDAS implementer’s agreed on the PeerDAS breakout call #1 to implement PeerDAS on top of Deneb for the time being, to minimize thrash with Pectra changes as the core EIP set is still in the process of stabilizing. The intent is to rebase PeerDAS on top of the Pectra changes once it is clearer that the other Pectra EIPs have stabilized, ideally over the next few Pectra devnets.

We then turned to raising the blob count in Pectra:

- The intent is to raise the blob count to provide an increase in Ethereum’s data throughput in the upcoming hard fork.
- However, there are a few complications:

Preliminary analysis shows turbulence at the current blob count.
- PeerDAS handles blob data differently than today’s EIP-4844 mechanism, which unlocks further scale but makes it hard to compare the blob count today to a blob count under Pectra.

In light of these facts, there are a variety of opinions on how to raise the blob count in Pectra; including: increasing the blob count even without PeerDAS, increasing the blob count with PeerDAS, or simply deploying PeerDAS and leaving the blob count alone. Analysis of the future Pectra devnets should give us more confidence in the right approach — check the call for the full nuance here.
We also covered a proposal to uncouple the blob count, which currently is set independently on the EL and CL (yet has to match); there is an [initial PR here](https://github.com/ethereum/consensus-specs/pull/3800) that has the CL drive the blob count but discussion on the call raised a few more questions to do this safely. We also discussed how to handle the change in the blob base fee when the blob count changes. In short, expect some possible changes in how blob accounting is carried out in Pectra.

We concluded with a [great update](https://github.com/ethereum/pm/issues/1069#issuecomment-2162556692) on the SSZ-ification of the protocol (expect to see a devnet by the next CL call), and a call-out to determine the name of the “F-star” for the next CL fork to accompany Osaka on the EL.

*From Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1250966401888555109)*

### Recording

  [![image](https://img.youtube.com/vi/LpY1JQHl9EY/maxresdefault.jpg)](https://www.youtube.com/watch?v=LpY1JQHl9EY&t=290s)

### Transcript

[To be added]

### Additional info

Notes by [@Christine_dkim](/u/christine_dkim): [Crypto & Blockchain Research Reports | Galaxy](https://www.galaxy.com/insights/research/ethereum-all-core-developers-consensus-call-135/)

F-star name discussion: [F-star name for Consensus Layer upgrade after Electra](https://ethereum-magicians.org/t/f-star-name-for-consensus-layer-upgrade-after-electra/20285)

## Replies
