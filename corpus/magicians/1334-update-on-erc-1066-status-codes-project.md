---
source: magicians
topic_id: 1334
title: Update on ERC-1066 Status Codes project
author: expede
date: "2018-09-13"
category: EIPs
tags: [erc-1066]
url: https://ethereum-magicians.org/t/update-on-erc-1066-status-codes-project/1334
views: 1529
likes: 1
posts_count: 1
---

# Update on ERC-1066 Status Codes project

Okay! I’m back out of deep freeze. Just thought that it would be helpful to bring everyone up to date with the effort on ERC1066, especially since a lot has happened since Berlin!

(Feedback appreciated on format. I’m not totally certain that this is the correct place to post updates versus just in [the intro thread](https://ethereum-magicians.org/t/erc-1066-ethereum-status-codes-esc/283))

# Focused Effort

[@boris](/u/boris) and I got some breathing room to [focus on ESCs through the Consensys Tachyon Accelerator](https://techcrunch.com/2018/09/07/consensys-details-the-first-cohort-of-companies-to-enter-its-new-accelerator-tachyon/) open source track. We also have committed effort from Robot Overlord (which is also me ![:stuck_out_tongue_winking_eye:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue_winking_eye.png?v=15)) through at least the end of the year. The current team is three: [@expede](/u/expede) & @jenncoop focused on tech, and [@boris](/u/boris) on community.

[![](https://ethereum-magicians.org/uploads/default/optimized/1X/bdbd66abc249c8d186738278ae7cc0c7a760f45d_2_552x500.jpeg)720×652 90.8 KB](https://ethereum-magicians.org/uploads/default/bdbd66abc249c8d186738278ae7cc0c7a760f45d)

# In the Wild

[ERC1400 — Security Tokens](https://ethereum-magicians.org/t/erc-1400-security-token-standard/1314) uses ESCs as part of the standard. We’re going to be chatting with them about possibly integrating their use cases (on an abstraction of it) directly into the standard.

# Use Case Research

Protocols are essentially abstractions over common use cases. We’re doing a *bunch* of R&D around filling in the currently empty ranges in appropriate, flexible, reusable ways. If anyone wants to send us their use case, and especially contract architectures, we’d love to get that into the standard and make contracts more clearer and more interoperable.

# Translations

This is a very compelling use case of ESCs, and part of the original vision. The architecture and interfaces *may* be worth splitting out into a derivative standard, just to keep the core ERC-1066 focused. *It’s still a design goal of the core ESC project*, and the helper libs will almost certainly include translations support.

# Tool Integration

We’re talking to a bunch of wallets, frameworks, libs, and profilers to see if there’s a fit. Also to collect use cases from those projects’ goals ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=15)

# More Places to Talk!

- ESC Channel on the SPADE Discord
- Community calls starting up again… soon
