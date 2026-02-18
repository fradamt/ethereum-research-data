---
source: magicians
topic_id: 23822
title: Interop Testing #34 | April 28 2025
author: system
date: "2025-04-24"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/interop-testing-34-april-28-2025/23822
views: 339
likes: 3
posts_count: 2
---

# Interop Testing #34 | April 28 2025

# Interop Testing #34 | April 28 2025

- April 28, 2025, 14:00 UTC

# Agenda

- Pectra Testing

New EL test release: Release Vltava (v4.3.0) · ethereum/execution-spec-tests · GitHub

Contains invalid deposit contract log layout tests

Potentially a new release this week

PeerDAS Testing
EOF Testing:

- Discuss and decide on EOF Fusaka Options

Others:

- https://github.com/ethereum/consensus-specs/pull/4291

 **🤖 config**

- Duration in minutes : 60
- Recurring meeting : true
- Call series : interop testing
- Occurrence rate : weekly
- Already a Zoom meeting ID : false
- Already on Ethereum Calendar : true # Set to true if this meeting is already on the Ethereum public calendar (will not create calendar event)
- Need YouTube stream links : true # Set to false if you don’t want YouTube stream links created
- display zoom link in invite : false # Set to true to add the Zoom link to the Google Calendar invite description

[GitHub Issue](https://github.com/ethereum/pm/issues/1520)

**YouTube Stream Links:**

- Stream 1 (Apr 28, 2025): https://youtube.com/watch?v=GcA-sVRSCHc

## Replies

**abcoathup** (2025-04-28):

### EOF removed from Fusaka upgrade (Declined for Inclusion)

*[Reasoning by [@timbeiko](/u/timbeiko) copied from [Update EIP-7607: Remove EOF from Fusaka by timbeiko · Pull Request #9703 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9703#issue-3025759055)]*

**
Reasoning**

On [“ACDT” 34](https://github.com/ethereum/pm/issues/1499), a decision was made to remove EOF from Fusaka.

The process here was highly unusual. I encourage people to listen to the [full discussion](https://www.youtube.com/watch?v=M3DWaWbIB3s). Here are the reasons why I think this is the correct outcome, despite several client teams expressing support for EOF:

1. Risks to Fusaka timelines: all client teams, ELs included, seem to agree that shipping PeerDAS ASAP is Ethereum’s most important priority. While this wasn’t a major topic of discussion on the call, it’s worth acknowledging that debating variants of the EOF spec at this point affects our ability to ship. As we move towards Fusaka devnets, and coupling EL & CL changes, keeping EOF would increasingly become the default path. While there are ways to mitigate this risk, such as the modular EOF devnets proposed by the EIPs’ champions, it is nevertheless a risk, and one we should only take if we feel the payoff is significant. Points (2) and (3) below make me question this.
2. Technical uncertainty about impact: while there seemed to be broad support on the call towards the Option D variant, midway through, some participants realized that they did not understand the implications of this variant. Reasoning about the implications of an EIP’s semantic change should ideally happen much earlier in the process. Had another EIP with similar levels of open questions been proposed on today’s call, ACD would have rejected it without hesitation.
3. Process considerations: last but not least, I think the entire EOF inclusion debate has shown failures in ACD’s prioritization process. While core devs originally agreed to ship EOF (many times), at each occasion, many prominent community members raised objections to it. While, individually considered, it didn’t seem like any of these concerns warranted EOF’s removal, zooming out, it’s clear that ACD’s feedback loops failed at addressing these concerns.

Given the above, and the intention to [reconfigure AllCoreDevs](https://ethereum-magicians.org/t/reconfiguring-allcoredevs/23370) for Glamsterdam, it seems right to remove EOF from Fusaka while leaving the door for its champions to present a case for it in Glamsterdam, where hopefully the process begins by assessing what the highest impact changes for Ethereum as a whole are.

My apologies to everyone who has sunk more time into this than they should have because of the process failures. I hope we can learn from this to improve how we plan upgrades going forward ![:folded_hands:](https://ethereum-magicians.org/images/emoji/twitter/folded_hands.png?v=15)

### Summary

*[Summary by [@poojaranjan](/u/poojaranjan) copied from [Interop Testing #34 | April 28 2025 · Issue #1499 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1499#issuecomment-2836061807)]*

- Mainnet Shadow Fork in progress; EF Testing prepping a new BLS-heavy test release.
- PeerDAS Devnet 6 deprecated; Devnet 7 coming this week.
- Consensus spec update PR (#4291) proposed to align EL and CL minimal specs.
- EOF Discussion: After strong debate, EOF removed from Fusaka upgrade.
- Option D explored (limited introspection), but community support was split.
- Focus shifted back to PeerDAS + scaling improvements for Fusaka.
- App dev feedback emphasized — stronger app-dev engagement required for future EVM upgrades.
- Future EOF considerations deferred to Glamsterdam cycle.

### Notes & chat log


      ![](https://hackmd.io/favicon.png)

      [HackMD](https://hackmd.io/@poojaranjan/InteropTestingNotes#Interop-Testing-Call-34-%E2%80%93-April-28-2025)



    ![](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###



Progress is on track; requires updates for blob base fee, baseFeeUpdateFraction, and EIP-7702.










### Recordings

  [![image](https://img.youtube.com/vi/M3DWaWbIB3s/maxresdefault.jpg)](https://www.youtube.com/watch?v=M3DWaWbIB3s&t=53s)



      [x.com](https://x.com/EthCatHerders/status/1916854796692390082)





####

[@](https://x.com/EthCatHerders/status/1916854796692390082)



  https://x.com/EthCatHerders/status/1916854796692390082










### Additional info

- EIP-7607: Hardfork Meta - Fusaka
- Declined for Inclusion defined in EIP-7723: Network Upgrade Inclusion Stages
- Ipsilon team:

EOF Fusaka Options
- EOF - Solidity library compatibility (initial) report

