---
source: magicians
topic_id: 27216
title: FOCIL Breakout #26, January 13, 2026
author: system
date: "2025-12-18"
category: Protocol Calls & happenings
tags: [breakout, focil]
url: https://ethereum-magicians.org/t/focil-breakout-26-january-13-2026/27216
views: 42
likes: 2
posts_count: 5
---

# FOCIL Breakout #26, January 13, 2026

### Agenda

- Development updates
- and more

**Meeting Time:** Tuesday, January 13, 2026 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1848)

## Replies

**system** (2026-01-13):

### Meeting Summary:

The meeting began with technical difficulties regarding YouTube live streaming and casual conversation among participants. The team discussed various technical issues and updates related to the FOCI Breakout 26 session, including proposals for HEGOTA and the readiness of the HECO test, while also addressing remote participation possibilities. The group reviewed pending PR submissions and discussed preparations for the next Glamsterdam event, including timeline considerations for the Hagota headliner process and various implementation options.

**Click to expand detailed summary**

The meeting began with a brief delay as participants waited for additional attendees. Jihoon announced they would start once more people joined, but after a few minutes, they decided to begin the meeting with the current participants. The group engaged in casual conversation, including jokes and banter, before formally starting the meeting. Jihoon mentioned they were experiencing technical difficulties with YouTube live streaming and would resolve the issue.

The team discussed technical issues with live streaming meetings, particularly regarding YouTube streaming capabilities. Pooja clarified that while the EF team has automated some processes for uploading recordings to YouTube, breakout room meetings may not be streamed unless explicitly requested. The team agreed to test YouTube livestreaming during the current meeting and rely on the automated upload infrastructure for future breakout calls.

The meeting focused on updates and discussions related to the FOCI Breakout 26 session, including the proposal for HEGOTA and the readiness of the HECO test. Jihoon shared updates on changes to the CL spec and mentioned that further updates would be shared as needed. Matthew inquired about the possibility of participating remotely in the Hagoda interop, to which Jihoon responded that details about livestreaming or remote participation were not yet available.

The team discussed the possibility of remote participation in an upcoming meeting, with Justin confirming that while ad-hoc remote attendance is feasible, it can be challenging due to audio quality issues. Matthew expressed his inability to attend in person but confirmed that his team would be represented. The conversation then shifted to a PR that is pending FOCIL becoming a headliner for Hagota, with Jihoon explaining that the implementation currently relies on Flu due to the lack of a working ePBS implementation, noting that many of the previously built clients are now non-functional.

The team discussed the timeline for the Hagota headliner process, which is expected to be completed by late February. They debated whether to base interop on Flulu or Glamsterdam, with Matthew expressing concerns about the tight timeline if they choose Flulu. Jihoon noted that while CL clients don’t need to rush interop, EL clients like Besu might prefer to build everything from scratch once a working PBS client is available in mid-March or April.

The team discussed preparations for the next Glamsterdam event and reviewed a PR submission by Jihoon, which involved refactoring the withdrawal processing function and aligning the fork-choice function with the full spec. Jihoon provided a summary of the changes, which were deemed minor and non-essential. The group agreed to continue discussions in their next breakout call in two weeks.

### Next Steps:

- Jihoon: Write a proposer for headliner candidates for Hagota
- Jihoon: Share any future changes made to the FOCIL spec with the team so people can update their prototypes
- Jihoon: Update the PR based on the latest Gloas spec once the Gloas spec is frozen
- Justin: Bring a microphone to the Hagota interop and advocate for Matthew’s team if needed
- Matthew’s team: Find a second person interested in FOCIL to represent at the Hagota interop
- Team members: Review the PR  to ensure it makes sense

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 0L^K!#8e)
- Download Chat (Passcode: 0L^K!#8e)
- Download Audio (Passcode: 0L^K!#8e)

---

**system** (2026-01-13):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=Go7H43hjx-k

---

**jihoonsong** (2026-01-14):

Wishing you a happy and FOCIL new year!

### FOCIL for Hegotá

- During the holidays, we published FOCIL Readiness for Hegotá.

### Implementation Updates

- The FOCIL CL spec has updated to reflect recent refactors to the CL spec.

Q: When do we rebase onto Gloas?

A: The spec on top of Gloas is pretty much ready. The first ePBS devnet is expected around mid March so we can rebase onto Gloas after that. There is no need to rush since we still have plenty of time before Gloas ships.

### Links

- FOCIL Readiness for Hegotá
- Reflect recent changes into EIP-7805 spec

---

**jihoonsong** (2026-01-14):

### Recording

- YouTube

### Summary

- X Thread
- Full Summary

