---
source: magicians
topic_id: 23371
title: History Expiry Breakout | April 8th 2025
author: system
date: "2025-04-03"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/history-expiry-breakout-april-8th-2025/23371
views: 91
likes: 1
posts_count: 2
---

# History Expiry Breakout | April 8th 2025

# History Expiry Breakout - April 8th 2025

- April 8, 2025, 14:00 UTC
- Duration in minutes : 60 minutes
- Zoom link will be posted in Eth R&D#history-expiry prior to the call

# Agenda

- eth/69 protocol finalization
- review meta-EIP
- Update EIP-7801: Update 7801 to accomodate era1 file format storage and serving by smartprogrammer93 · Pull Request #9331 · ethereum/EIPs · GitHub  - Update to 7801 related to era file formats

[GitHub Issue](https://github.com/ethereum/pm/issues/1427)

## Replies

**pipermerriam** (2025-04-08):

History Expiry Breakout Call Notes

`eth/69` should be updated as follows:  Agreement on the call from Besu, Geth, Nethermind, and Reth.

- Status message should be updated to include earliestBlock and latestBlock.  This is to allow clients to more efficiently avoid connecting to clients that do not have useful block data.
- New “announcement” style message added to protocol that includes earliestBlock and latestBlock.  This message should be sent once per epoch.  It was agreed that this announcement style message was preferable to a request/response to avoid polling patterns in client implementations.

The justification for `earliestBlock` addition is so that clients can communicate the beginning of the history range they can serve from locally available data.

The justification for `latestBlock` is from multiple reasons.

1. To allow full sync clients to communicate the status of their sync
2. To provide a signaling mechanism that indicates participation in the protocol.

A modification to 7801 to change the storage ranges to align with Era file ranges was highlighted: [Update EIP-7801: Update 7801 to accomodate era1 file format storage and serving by smartprogrammer93 · Pull Request #9331 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9331)

Piper (me) requested feedback on the History Expiry Meta EIP: [Add EIP: History Expiry Meta by pipermerriam · Pull Request #9572 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9572/files)

