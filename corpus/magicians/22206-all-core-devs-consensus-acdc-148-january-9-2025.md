---
source: magicians
topic_id: 22206
title: All Core Devs - Consensus (ACDC) #148, January 9, 2025
author: abcoathup
date: "2024-12-14"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-148-january-9-2025/22206
views: 415
likes: 6
posts_count: 3
---

# All Core Devs - Consensus (ACDC) #148, January 9, 2025

#### Agenda

[Consensus-layer Call 148 · Issue #1218 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1218) moderated by [@ralexstokes](/u/ralexstokes)

**
Agenda summary**

by [@nixo](/u/nixo) *(Copied from [Twitter](https://x.com/nixorokish/status/1877096007621546147))*

##### Pectra testing

![:play_button:](https://ethereum-magicians.org/images/emoji/twitter/play_button.png?v=15) Builder specs v0.5.0 for Pectra released ![:tada:](https://ethereum-magicians.org/images/emoji/twitter/tada.png?v=15)

![:play_button:](https://ethereum-magicians.org/images/emoji/twitter/play_button.png?v=15) devnet-5 (live soon™) may be the last devnet. A devnet-6 is possible, but if 5 is smooth, could see testnets (Sepolia & Holešky) by… Feb?

*relevant: testing, consensus & execution teams*

##### Post-Pectra

PeerDAS & EOF are scheduled for inclusion in Fusaka (the next fork) - they’ll go over any updates

The name for the fork post Fusaka is being chosen (vote here: [G-star name for Consensus Layer upgrade after Fusaka](https://ethereum-magicians.org/t/g-star-name-for-consensus-layer-upgrade-after-fusaka/22357)) - prolly’ll be chosen this week

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png)

      [All Core Devs - Consensus (ACDC) #148, January 9, 2025](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-148-january-9-2025/22206/3) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDC #148 summary
> Action Items
>
> Continue implementation/polish for pectra-devnet-5. Be on the lookout for devnet launch in the next week or two!
>
> Summary
> Shorter call today that mainly focused on pectra-devnet-5 logistics.
>
> Touched on a few open questions/PRs for devnet-5 specs. Open items have been addressed.
> Touched on client implementation progress. Various stages of readiness, but all CL clients are very close to being ready for devnet-5 launch.
> Going to check-in with EL clients on next …

#### Recording

  [![image](https://img.youtube.com/vi/4LbNL_hp2Ho/maxresdefault.jpg)](https://www.youtube.com/watch?v=4LbNL_hp2Ho&t=219s)

#### Additional Info

- Gloas chosen as G-star name for Consensus Layer upgrade after Fusaka
- Reminder: standardized validator hardware requirements:
- Crypto & Blockchain Research Reports | Galaxy by @Christine_dkim
- https://etherworld.co/2025/01/09/highlights-of-ethereums-all-core-devs-consenus-meeting-148/ by @yashkamalchaturvedi

## Replies

**yashkamalchaturvedi** (2025-01-09):

Call Notes:  [Highlights of Ethereum's All Core Devs Meeting #148](https://etherworld.co/2025/01/09/highlights-of-ethereums-all-core-devs-consenus-meeting-148/)

---

**ralexstokes** (2025-01-10):

**ACDC #148 summary**

**Action Items**

- Continue implementation/polish for pectra-devnet-5. Be on the lookout for devnet launch in the next week or two!

**Summary**

Shorter call today that mainly focused on `pectra-devnet-5` logistics.

- Touched on a few open questions/PRs for devnet-5 specs. Open items have been addressed.
- Touched on client implementation progress. Various stages of readiness, but all CL clients are very close to being ready for devnet-5 launch.
- Going to check-in with EL clients on next ACDE, but expect to launch devnet-5 in the next week or two.
- Assuming devnet-5 has no issues, we should be on track to start discussing dates for forking testnets Sepolia and Holesky to Pectra in the next few weeks.
- Had a request for last call on a networking PR to add IPv6 support to ENR records. PR here has been merged.
- Had another request to provide feedback on a minimal set of node requirements to facilitate community coordination and help with protocol R&D. Document here: Hardware Requirements - HackMD
- Closed out the call with a discussion of a poll to help find a star for the “G-fork” after Fusaka. Community favorite is Gloas.

