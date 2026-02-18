---
source: magicians
topic_id: 20445
title: "EIP-7733: Deactivate EIP-158"
author: gballet
date: "2024-07-02"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7733-deactivate-eip-158/20445
views: 528
likes: 3
posts_count: 2
---

# EIP-7733: Deactivate EIP-158

After EIP-6780, the `SELFDESTRUCT` instruction was neutered, so that contracts could no longer be deleted. Contract deletions can still occur, however, via EIP-158. While EIP-7702 this can not happen, this latter EIP introduces the possibility for an empty EoA to have state. This is causing some issues when interfacing with verkle, for which state deletion is not possible.

EIP-158 was meant as a temporary measure to combat the “Shanghai attacks”. Now that this is attack has been mitigated by other means, it can be deactivated.

Note: The deactivation should happen in Prague, for alternative methods to EIP-7612 to be valid. If EIP-7612 is accepted, then nothing opposes its inclusion in Osaka instead.

PR URL: [Add EIP: Deactivate EIP-158 by gballet · Pull Request #8712 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8712/files)

## Replies

**RenanSouza2** (2024-07-03):

it is not correct that a contract can be deleted by this because at the deploy, it’s nonce is set to 1

eip 158 requires the nonce to be zero

