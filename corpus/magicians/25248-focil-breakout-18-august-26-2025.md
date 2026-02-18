---
source: magicians
topic_id: 25248
title: FOCIL Breakout #18, August 26, 2025
author: system
date: "2025-08-26"
category: Protocol Calls & happenings
tags: [breakout, focil]
url: https://ethereum-magicians.org/t/focil-breakout-18-august-26-2025/25248
views: 70
likes: 7
posts_count: 3
---

# FOCIL Breakout #18, August 26, 2025

### Agenda

- FOCIL rebase
- FOCIL testing
- FOCIL development updates

**Meeting Time:** Tuesday, August 26, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1701)

## Replies

**jihoonsong** (2025-08-28):

FOCIL breakout hasn’t had a break since it started 8 months ago. We are continue working on rebasing onto Fulu, testing and adding metrics.

### Rebase onto Fulu

[Justin](https://x.com/JustinTraglia) has [rebased the CL spec onto Fulu](https://github.com/ethereum/consensus-specs/pull/4502). The CL spec will remain on top of Fulu and there will be a long-standing PR that rebases FOCIL onto Gloas. The latter will be updated regularly to stay ready for getting SFI’d.

Client implementations will rebase onto Gloas without ePBS implementation to minimize boilerplate code and remain as a feature fork. Specifically, our Kurtosis configs will set Gloas at epoch 0 and eip7805 fork at epoch 1.

### Testing

[Jihoon](https://x.com/jih2nn) will publish a testing document that lays out test cases such as their inputs, outputs and coverage. In discussions with the Protocol Security and STEEL teams, we believe this will be invaluable.

### Implementation Updates

- Geth has been updated to align with the revised Engine APIs spec.
- Lodestar has rebased onto Fulu and is implementing the updated CL, Engine APIs and Beacon  APIs specs. Further testing and interop with the updated Geth will follow.
- Teku has rebased onto Fulu and will be working on the updated specs.
- Reth has been working on rebasing onto Fulu and the updated specs.
- Besu has been focusing on the 60M gas limit.
- Nethermind has been focusing on BALs.

### FOCIL Metrics

- Katya shared an article on FOCIL beacon metrics. Please have a look and share your thoughts!

### Links

- Rebase FOCIL onto Fulu
- FOCIL beacon metrics

---

**jihoonsong** (2025-08-28):

### Recording

- YouTube
- X Stream

### Summary

- X Thread
- Full Summary

