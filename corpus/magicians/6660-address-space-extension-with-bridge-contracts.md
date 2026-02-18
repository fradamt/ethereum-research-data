---
source: magicians
topic_id: 6660
title: Address Space Extension with bridge contracts
author: axic
date: "2021-07-15"
category: Working Groups > Ethereum 1.x Ring
tags: [address-space]
url: https://ethereum-magicians.org/t/address-space-extension-with-bridge-contracts/6660
views: 1081
likes: 0
posts_count: 2
---

# Address Space Extension with bridge contracts

This is an alternative proposal building on top of the [Address Space Extension with Translation Map](https://notes.ethereum.org/@ipsilon/address-space-extension-exploration) idea. See [this for open questions](https://notes.ethereum.org/@ipsilon/address-space-extension-issues).

One of the major issues identified is the inability to distinguish short (legacy) addresses from compressed addresses, and the resulting complexity of automatic translation.

In order to avoid this problem, we introduce a special contract type, called bridge contract, which announces itself being capable of interacting with the new address space, but is actually placed in the legacy address space (and has a short address).  Other contracts in the legacy space can not interact with the new address space.

For the complete text see [ASE with bridge-contracts - HackMD](https://notes.ethereum.org/@axic/ase-bridge-contracts)

## Replies

**dogeprotocol** (2023-12-02):

Hi, FunctionTypes in Ethereum currently use 20+4 bytes where 4 bytes is for function identifier in an external contract (for example). So it is only possible to use 28 bytes instead of 32 bytes for the address, otherwise FunctionTypes will break.

Any solution around this?

