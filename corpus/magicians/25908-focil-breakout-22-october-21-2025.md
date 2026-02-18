---
source: magicians
topic_id: 25908
title: FOCIL Breakout #22, October 21, 2025
author: system
date: "2025-10-21"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/focil-breakout-22-october-21-2025/25908
views: 52
likes: 0
posts_count: 5
---

# FOCIL Breakout #22, October 21, 2025

### Agenda

- Development updates

**Meeting Time:** Tuesday, October 21, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1774)

## Replies

**system** (2025-10-21):

### Meeting Summary:

The team discussed development updates, focusing on client development, metrics, and testing. Jihoon shared progress on unit tests for inclusion-laced store and issues with Geth interoperability. Pelle reported on metrics cleanup and execution test checklist development. Mehdi provided an update on Teku, explaining their decision to stay on top of Folu and wait for PBS stabilization before rebasing. The team also discussed discrepancies in metrics tracking between consensus layer and execution layer, with Pelle clarifying the differences in tracking methods.

**Click to expand detailed summary**

The team discussed development updates, focusing on client development, metrics, and testing. Jihoon shared progress on unit tests for inclusion-laced store and issues with Geth interoperability. Pelle reported on metrics cleanup and execution test checklist development. Mehdi provided an update on Teku, explaining their decision to stay on top of Folu and wait for PBS stabilization before rebasing. The team also discussed discrepancies in metrics tracking between consensus layer and execution layer, with Pelle clarifying the differences in tracking methods.

### Next Steps:

- Jihoon to fix the bug in the Geth image for interop between Geth and Wrath.
- Jihoon to add more test cases and implement corresponding tests for inclusion-laced store.
- Pelle to complete the remaining 3 EL metrics in Reth.
- Pelle to continue working on execution tests based on the checklist.
- Mehdi/Teku team to wait for a stable version of ePBS before rebasing on GlowEyes.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: h+0$f%Mg)
- Download Chat (Passcode: h+0$f%Mg)

---

**system** (2025-10-21):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=7tEXtPTMpPM

---

**jihoonsong** (2025-10-23):

FOCIL now has test checklists for the CL and the EL.

### Implementation Updates

- Teku has rebased onto no-op Gloas and reverted to Fulu as we discussed last time.
- Lodestar has no update.

### Testing

- Jihoon has added unit tests for InclusionListStore and test cases for the CL.
- Pelle has been working on test cases for the EL.

### FOCIL Metrics

- Pelle has cleaned up and added remaining the EL metrics in Reth.

### Links

- FOCIL test cases for the CL
- FOCIL test cases for the EL

---

**jihoonsong** (2025-10-23):

### Recording

- YouTube
- X Stream

### Summary

- X Thread
- Full Summary

