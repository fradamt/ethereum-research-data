---
source: magicians
topic_id: 23607
title: All Core Devs - Consensus (ACDC) #156, May 1 2025
author: system
date: "2025-04-18"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-156-may-1-2025/23607
views: 267
likes: 6
posts_count: 5
---

# All Core Devs - Consensus (ACDC) #156, May 1 2025

All Core Devs - Consensus (ACDC) #156, May 1, 2025

- May 1, 2025, 14:00 UTC

# Agenda

- Pectra

pectra mainnet shadow fork
- blog post up to date with releases?
- reminder: https://github.com/ethereum/pm/blob/master/Pectra/pectra-mainnet-plan.md#client-team-coordinators

Fusaka

- peerdas-devnet-7 updates

Research, open questions

Facilitator emails (comma-separated): [stokes@ethereum.org](mailto:stokes@ethereum.org)

 **🤖 config**

- Duration in minutes : 90
- Recurring meeting : true
- Call series : ACDC
- Occurrence rate : bi-weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : true
- display zoom link in invite : false # Set to true to add the Zoom link to the Google Calendar invite description

[GitHub Issue](https://github.com/ethereum/pm/issues/1490)

## Replies

**abcoathup** (2025-04-19):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png)

      [All Core Devs - Consensus (ACDC) #156, May 1 2025](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-156-may-1-2025/23607/5) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDC #156 Summary
> Action items
>
> Pectra mainnet is imminent!
>
> See Pectra Mainnet Announcement | Ethereum Foundation Blog for timing and client release info.
>
>
>
> Summary
> Pectra
>
> We had a mainnet shadow fork that went well. Ran into some config issues similar to Holesky but no applicability to mainnet.
> As an aside, GnosisChain already forked to Pectra with no issues.
> Clients discussed some minor release updates; check the ethereum.org blog for the latest required software.
>
> Fusaka
>
> Next peerdas…

### AI Summary



    [![](https://ethereum-magicians.org/uploads/default/original/2X/5/5dac7cbbca817547901f15be798f33185e5453a6.png)547×494 200 KB](https://ethereum-magicians.org/uploads/default/5dac7cbbca817547901f15be798f33185e5453a6)

      [All Core Devs - Consensus (ACDC) #156, May 1 2025](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-156-may-1-2025/23607/3) [Protocol Calls & happenings](/c/protocol-calls/63)




> Meeting Summary:
> Meeting summary for All Core Devs - Consensus (ACDC) (05/01/2025)
> Quick recap
> The meeting covered discussions on the main Shadow Fork, including deposit problems and client issues, as well as updates on the upcoming Pectra Mainnet Fork and client releases. Plans for Devnet 7 were addressed, with suggestions to delay its launch until after Spectra updates and considerations for including validator custody. The team also discussed various technical aspects, including syncing iss…

### Recordings

  [![image](https://img.youtube.com/vi/NQhTiMFDZHQ/maxresdefault.jpg)](https://www.youtube.com/watch?v=NQhTiMFDZHQ&t=231s)



      [x.com](https://x.com/EthCatHerders/status/1917937871329349811)





####

[@](https://x.com/EthCatHerders/status/1917937871329349811)



  https://x.com/EthCatHerders/status/1917937871329349811










### Writeups

- Highlights of Ethereum’s All Core Devs Meeting (ACDC) #156 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Mainnet upgrades to Pectra May 7, Epoch 364032

---

**system** (2025-05-01):

### Meeting Summary:

**Meeting summary for All Core Devs - Consensus (ACDC) (05/01/2025)**

**Quick recap**

The meeting covered discussions on the main Shadow Fork, including deposit problems and client issues, as well as updates on the upcoming Pectra Mainnet Fork and client releases. Plans for Devnet 7 were addressed, with suggestions to delay its launch until after Spectra updates and considerations for including validator custody. The team also discussed various technical aspects, including syncing issues, PRs related to minimal spec execution payload, and the need for more review on consensus specs blob schedule PR.

**Next steps**

• Tim to update the blog post with either “version X or later” language or strike the old release and add the new one for Lighthouse and Prism clients.

• Saulius to provide contact information for Grandine client team for the instant response plan.

• Terence to release Prism 6.0.1 with bug fixes.

• Client teams to continue working on fixing syncing issues for Devnet 7.

• Barnabas and team to consider launching Devnet 7 to help with debugging, particularly for Lighthouse.

• Client teams to review the consensus specs Blob Schedule PR shared by Justin.

• All teams to focus on final preparations for the Petra mainnet upgrade.

 ** click to expand detailed summary**

**Summary**
**Shadow Fork and Pectra Mainnet Updates**
In the meeting, Stokes led the discussion about the main Shadow Fork, which went mostly fine with some deposit problems on some clients. Barnabas explained that the issues were due to the Shadow Fork config and could not happen on Mainnet. Notices Forked Petra, and everything went well. There was a discussion about the instant response plan and the need for updates on the main Shadow Fork. Sean announced the release of Lighthouse 7.0.1, which helps with state cache misses. Terrence mentioned that Prysm is making a release today, which is recommended on top of 6.0.0. There was also a discussion about the upcoming Pectra Mainnet Fork, with updates on the blog post and the need for clients to be ready. The conversation ended with a discussion about the readiness of relays and builders for the upcoming fork.
**Devnet 7 Launch and Syncing Issues**
In the meeting, Barnabas suggested delaying the launch of Devnet 7 until after the Spectra updates, allowing more people to focus on it. He also mentioned that the syncing issues were being worked on by multiple client teams. Sean from Lighthouse team expressed the need for Devnet 7 to work through debugging. Terrence raised a question about the Devnet 7 spec, to which Barnabas responded that they were considering including validator custody in it. Justin Traglia discussed a PR related to the minimal spec execution payload, and Barnabas mentioned a need for more eyes on the consensus specs blob schedule PR. The team agreed to provisionally plan for Devnet 7 with Beta 5 and the data column by root requests change. The conversation ended with no further topics to discuss.
AI-generated content may be inaccurate or misleading. Always check for accuracy.

### Recording Access:


      ![](https://us06st1.zoom.us/zoom.ico)

      [Zoom](https://ethereumfoundation.zoom.us/rec/share/ELMBvymd8jRj33NRaAL2a6UlOL_ZCfTpMlLAtfeHiJe2RTqgMaevl_pV8DiBq4h1.j2EYv8efFovsczj2?startTime=1746107252000&pwd=aLHMF1MWCNrxDb9EH2HesTi4XBQg_UZJ)



    ![](https://us06st1.zoom.us/static/6.3.49959/image/thumb.png)

###



Zoom is the leader in modern enterprise video communications, with an easy, reliable cloud platform for video and audio conferencing, chat, and webinars across mobile, desktop, and room systems. Zoom Rooms is the original software-based conference...










### Recording Access:

- Join Recording Session
- Download Transcript
- Download Chat

---

**system** (2025-05-01):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/live/NQhTiMFDZHQ?feature=share

---

**ralexstokes** (2025-05-01):

**ACDC #156 Summary**

**Action items**

- Pectra mainnet is imminent!

See Pectra Mainnet Announcement | Ethereum Foundation Blog for timing and client release info.

**Summary**

Pectra

- We had a mainnet shadow fork that went well. Ran into some config issues similar to Holesky but no applicability to mainnet.
- As an aside, GnosisChain already forked to Pectra with no issues.
- Clients discussed some minor release updates; check the ethereum.org blog for the latest required software.

Fusaka

- Next peerdas devnet will be peerdas-devnet-7, launching after Pectra once sync issues are fixed.

Sunnyside Labs is running an instance of peerdas-devnet-6 in the mean time.

Ideally we also include validator custody in `peerdas-devnet-7` along with other bug fixes, although we likely need more progress with implementation here before including in `peerdas-devnet-7`.
We discussed the exact specs for `peerdas-devnet-7` which are forthcoming.
Had a call out to review the BPO infra for upcoming peerdas devnets

- PTAL: Introduce blob schedule by GabrielAstieres · Pull Request #4277 · ethereum/consensus-specs · GitHub

