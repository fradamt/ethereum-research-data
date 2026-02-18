---
source: magicians
topic_id: 20174
title: All Core Devs - Consensus (ACDC) #134, May 30 2024
author: abcoathup
date: "2024-05-31"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-134-may-30-2024/20174
views: 1291
likes: 0
posts_count: 2
---

# All Core Devs - Consensus (ACDC) #134, May 30 2024

### Agenda

[Consensus-layer Call 134 · Issue #1050 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1050)

Moderator: [@ralexstokes](/u/ralexstokes)

### Summary

Recap by [@ralexstokes](/u/ralexstokes):

This call was packed with various discussions around scoping the upcoming Pectra hard fork.

- Began with a recap of devnet-0, which generally went really well!
- Next, covered a variety of updates, extensions or modifications to the existing EIP set
- Then turned to a new EIP (number 7688) to consider inclusion reflecting learnings from devnet-0
- Touched on early PeerDAS devnet alongside devnet-0, which also went very well given how early the implementations are
- Spent the rest of the call discussing fork scoping for Pectra

Check out the call for the full color
- Many teams/contributors expressed a variety of options
- Rough consensus formed around the importance of PeerDAS
- To reflect an intent to include PeerDAS in Pectra, while derisking feature sets and timelines, client teams agreed to build PeerDAS as part of the Electra fork with a separate activation epoch

If PeerDAS R&D goes well, this activation epoch can simply be the Pectra fork epoch
- If client teams discover difficulties with PeerDAS after implementation over the coming months, we have the option to set the PeerDAS activation epoch after the Pectra epoch (including possibly setting it so far in the future we would be able to schedule for a future hard fork)

Otherwise, we agreed to keep the existing Pectra scope as is

We didn’t quite have time to finish the discussion around EIP-7688 (stable container SSZ upgrade), which we will cover on the next call!

*From Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1246280395591385098)*

### Recording

  [![image](https://img.youtube.com/vi/Lrk99mKiWaU/maxresdefault.jpg)](https://www.youtube.com/watch?v=Lrk99mKiWaU&t=286s)

### Transcript

https://github.com/ethereum/pm/blob/master/AllCoreDevs-CL-Meetings/Call_134.md

### Additional info

Notes by [@Christine_dkim](/u/christine_dkim): [Crypto & Blockchain Research Reports | Galaxy](https://www.galaxy.com/insights/research/ethereum-all-core-developers-consensus-call-134/)

## Replies
