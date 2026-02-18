---
source: magicians
topic_id: 26601
title: FOCIL Breakout #24, December 2, 2025
author: system
date: "2025-11-17"
category: Protocol Calls & happenings
tags: [breakout, focil]
url: https://ethereum-magicians.org/t/focil-breakout-24-december-2-2025/26601
views: 64
likes: 1
posts_count: 3
---

# FOCIL Breakout #24, December 2, 2025

### Agenda

- Development updates
- FOCIL in Heka/Bogota

**Meeting Time:** Tuesday, December 02, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1811)

## Replies

**jihoonsong** (2025-12-04):

How can FOCIL realize “credible commitment” to Heka/Bogotá?

### Implementation Updates

- Reth has implemented all EL metrics and rebased onto the master branch.
- Erigon has implemented an EL FOCIL prototype and interop with a pair of Reth and Lodestar is working. A CL prototype in Erigon about 70% complete.

### FOCIL for Heka/Bogotá

- FOCIL was DFI’d from Glamsterdam on the condition of a credible commitment to Heka/Bogotá. The last ACD call ended with an open question: should FOCIL be CFI’d or SFI’d for Heka/Bogotá?
- People in the breakout call supported credibly committing FOCIL to Heka/Bogotá, but opinions diverged on execution. Two main views emerged among others:

The ACD outcome is to make a final decision on CFI’ing or SFI’ing FOCIL for Heka/Bogotá at the ACDC on the 11th. We should follow the ACD process.
- FOCIL should go through the headliner process for Heka/Bogotá, which hasn’t started yet. We will be able to find a way to respect the “credible commitment” decision during that process.

People also pointed out that we need a better pipelining process if we want a faster fork cadence. The earlier we decide on the fork scope, the more comfortable client teams are committing resources to features and the more likely we are to streamline development and testing. Sometimes great ideas come late, but a faster fork cadence reduces inclusion delay.

A concern was raised that it’s a bit early to SFI FOCIL as a more urgent issue could come up later. In the same vein, some argued that FOCIL should go through the headliner process to avoid a situation where FOCIL is SFI’d and then un-SFI’d, which could hurt the credibility of Ethereum’s governance process. The idea is to have the headliner process of 1–2 months that informs the community that the headliner process for Heka/Bogotá is ongoing and invites them to voice their opinions.

However, several counterarguments were made. The broad community is already aware of it and the process has been changed too many times during the past 6 months while FOCIL inclusion has been discussed. Introducing another process is not a solution that adds legitimacy and the credible commitment decision from the last ACD call should be respected.

Given that FOCIL is in a different position from others, a suggestion was made to create a document that lays out the estimated timeline for FOCIL implementation and testing, which could facilitate the headliner process. Client devs estimated it would take around a month to rebase FOCIL onto ePBS once they have a working ePBS implementation, as they already have mature implementations on Fulu. [Nixo](https://x.com/nixorokish) and [Jihoon](https://x.com/jih2nn) will reach out to EthPandaOps to outline that document.

### Links

- FOCIL EL prototype in Erigon

---

**jihoonsong** (2025-12-04):

### Recording

- YouTube
- X Stream

### Summary

- X Thread
- Full Summary

