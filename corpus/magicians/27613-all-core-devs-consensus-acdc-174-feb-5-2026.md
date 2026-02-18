---
source: magicians
topic_id: 27613
title: All Core Devs - Consensus (ACDC) #174, Feb 5, 2026
author: system
date: "2026-01-28"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-174-feb-5-2026/27613
views: 30
likes: 2
posts_count: 6
---

# All Core Devs - Consensus (ACDC) #174, Feb 5, 2026

### Agenda

- Interfork

Cell-level deltas

Glam

- epbs-devnet-0

Hegotá

- Headliner discussion and finalization

FOCIL

**Meeting Time:** Thursday, February 05, 2026 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1907)

## Replies

**abcoathup** (2026-01-28):

## Call details

### Video, transcript & chatlog

- All Core Devs Consensus #174 - Forkcast - [Forkcast] by EF Protocol Support

### News coverage

- [Ethereal news] edited by @abcoathup
- [ACD After Hours] by @Christine_dkim
- [Etherworld] by @yashkamalchaturvedi

### Resources

- Glamsterdam Upgrade - Forkcast
- Hegotá Upgrade - Forkcast

---

**system** (2026-02-05):

### Meeting Summary:

The meeting began with live streaming and agenda setting, followed by updates on various projects including Interfork, ePBS, and DevNet progress, along with discussions about headliner proposals and level delta topics. The team reviewed implementation progress of sellable deltas and discussed upcoming DevNet Zero launch, while also addressing bug fixes and testing requirements for various clients including Lighthouse, Prysm, and Nimbus. The conversation ended with discussions about EGOTA proposals, including FOCIL as a CL headliner candidate, and the team agreed to make the final headliner selection at the next ACDC meeting after giving participants time to review the proposals.

**Click to expand detailed summary**

The meeting began with Mario streaming the session live on YouTube and Twitter, with Pooja assisting in the setup. Stokes then welcomed everyone and outlined the agenda, which included updates on Interfork, ePBS with Glamsterdam, and DevNet progress. The team discussed headliner proposals, noting that the deadline for submissions had passed, and they were now in the phase of discussing these proposals for Hagota. Marco was set to provide an update on level delta topics, which were sequenced between Fusaka and Glamsterdam.

The team discussed the implementation progress of sellable deltas, a backwards-compatible optimization that allows peers to exchange bitmaps and only exchange missing cells. Marco provided updates from various client teams, noting that Lighthouse, Prysm, and Nimbus are close to completion, with testing ongoing in BlobDevNet. The team agreed to deploy this feature progressively, starting with controlled validators, and Barnabas suggested enabling it by default once thoroughly tested. They also briefly touched on the upcoming DevNet Zero, with a new specs release published and a target launch in the next 1-3 weeks.

The team discussed updates on the Bob KZG commitments and Lodestar targeting the end of the month. Potuz highlighted a serious bug caught by Lido researchers regarding deposits and encouraged other clients to review the current PR. The group also discussed the complexity of implementing ForkChoice in Glamsterdam, with Potuz urging caution in handling invalid branches. Stokes mentioned the need for testing infrastructure for ForkChoice, particularly for optimistic sync and removing branches. The team agreed to target DevNet 0 for the separation of payload and block, with self-building but separate broadcasting. Raúl shared a new tool for simulating the separation and mentioned plans to add BALs and deadline analysis based on network activity.

The team discussed a tool for analyzing beacon blocks and execution payloads, noting variations in compression rates due to Snappy’s compression table. Raúl explained these fluctuations were negligible and confirmed the tool’s utility for analyzing deadlines and variable PTC. The meeting then shifted to EGOTA, where Spoke officially proposed FOCIL as a CL headliner candidate, highlighting its benefits for censorship resistance and transaction inclusion guarantees. The team debated the merits of FOCIL, with some expressing concerns about its effectiveness compared to other designs, but agreed it could serve as a foundation for future developments. They also discussed the need for further economic modeling to understand its benefits fully.

The meeting focused on two main proposals: Leo’s proposal for a partial two-dimensional peer-to-peer extension and the FOCIL proposal for H-star. While there was broad consensus in favor of FOCIL, Ansgar suggested taking an extra two weeks to ensure complete confidence in the decision. The group agreed to make the headliner selection for Hagota on the CL side at the next ACDC meeting, giving participants time to review Leo’s proposal and provide feedback.

### Next Steps:

- Marco: Share the markdown document with useful links about cell-level deltas
- Marco: Add interested parties to the Telegram working group for cell-level deltas upon request
- All CL client teams: Target Alpha 2 specs release for ePBS DevNet Zero implementation
- All CL client teams: Aim to have DevNet Zero live by end of month
- All CL client teams: Review and provide feedback on the deposits bug fix PR  in Discord
- stokes: Take a look at ForkChoice testing infrastructure after the call
- stokes: Review the deposits bug PR  after the call
- All CL client teams: Review Leo’s proposal for partial reconstruction and 2D PeerDAS and provide feedback in the post or contact Leo directly
- All participants: Prepare to make the Hagota headliner selection on next ACDC call
- All CL client teams: Conduct final review and confirm confidence in FOCIL selection before next ACDC call

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 8d&g8tn?)
- Download Chat (Passcode: 8d&g8tn?)
- Download Audio (Passcode: 8d&g8tn?)

---

**system** (2026-02-05):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=K0E15WZYufc

---

**system** (2026-02-05):

### Meeting Summary:

The meeting began with live streaming and agenda setting, followed by updates on various projects including Interfork, ePBS, and DevNet progress, along with discussions about headliner proposals and level delta topics. The team reviewed implementation progress of sellable deltas and discussed upcoming DevNet Zero launch, while also addressing bug fixes and testing requirements for various clients including Lighthouse, Prysm, and Nimbus. The conversation ended with discussions about EGOTA proposals, including FOCIL as a CL headliner candidate, and the team agreed to make the final headliner selection at the next ACDC meeting after giving participants time to review the proposals.

**Click to expand detailed summary**

The meeting began with Mario streaming the session live on YouTube and Twitter, with Pooja assisting in the setup. Stokes then welcomed everyone and outlined the agenda, which included updates on Interfork, ePBS with Glamsterdam, and DevNet progress. The team discussed headliner proposals, noting that the deadline for submissions had passed, and they were now in the phase of discussing these proposals for Hagota. Marco was set to provide an update on level delta topics, which were sequenced between Fusaka and Glamsterdam.

The team discussed the implementation progress of sellable deltas, a backwards-compatible optimization that allows peers to exchange bitmaps and only exchange missing cells. Marco provided updates from various client teams, noting that Lighthouse, Prysm, and Nimbus are close to completion, with testing ongoing in BlobDevNet. The team agreed to deploy this feature progressively, starting with controlled validators, and Barnabas suggested enabling it by default once thoroughly tested. They also briefly touched on the upcoming DevNet Zero, with a new specs release published and a target launch in the next 1-3 weeks.

The team discussed updates on the Bob KZG commitments and Lodestar targeting the end of the month. Potuz highlighted a serious bug caught by Lido researchers regarding deposits and encouraged other clients to review the current PR. The group also discussed the complexity of implementing ForkChoice in Glamsterdam, with Potuz urging caution in handling invalid branches. Stokes mentioned the need for testing infrastructure for ForkChoice, particularly for optimistic sync and removing branches. The team agreed to target DevNet 0 for the separation of payload and block, with self-building but separate broadcasting. Raúl shared a new tool for simulating the separation and mentioned plans to add BALs and deadline analysis based on network activity.

The team discussed a tool for analyzing beacon blocks and execution payloads, noting variations in compression rates due to Snappy’s compression table. Raúl explained these fluctuations were negligible and confirmed the tool’s utility for analyzing deadlines and variable PTC. The meeting then shifted to EGOTA, where Spoke officially proposed FOCIL as a CL headliner candidate, highlighting its benefits for censorship resistance and transaction inclusion guarantees. The team debated the merits of FOCIL, with some expressing concerns about its effectiveness compared to other designs, but agreed it could serve as a foundation for future developments. They also discussed the need for further economic modeling to understand its benefits fully.

The meeting focused on two main proposals: Leo’s proposal for a partial two-dimensional peer-to-peer extension and the FOCIL proposal for H-star. While there was broad consensus in favor of FOCIL, Ansgar suggested taking an extra two weeks to ensure complete confidence in the decision. The group agreed to make the headliner selection for Hagota on the CL side at the next ACDC meeting, giving participants time to review Leo’s proposal and provide feedback.

### Next Steps:

- Marco: Share the markdown document with useful links about cell-level deltas
- Marco: Add interested parties to the Telegram working group for cell-level deltas upon request
- All CL client teams: Target Alpha 2 specs release for ePBS DevNet Zero implementation
- All CL client teams: Aim to have DevNet Zero live by end of month
- All CL client teams: Review and provide feedback on the deposits bug fix PR  in Discord
- stokes: Take a look at ForkChoice testing infrastructure after the call
- stokes: Review the deposits bug PR  after the call
- All CL client teams: Review Leo’s proposal for partial reconstruction and 2D PeerDAS and provide feedback in the post or contact Leo directly
- All participants: Prepare to make the Hagota headliner selection on next ACDC call
- All CL client teams: Conduct final review and confirm confidence in FOCIL selection before next ACDC call

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 8d&g8tn?)
- Download Chat (Passcode: 8d&g8tn?)
- Download Audio (Passcode: 8d&g8tn?)

---

**system** (2026-02-05):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=K0E15WZYufc

