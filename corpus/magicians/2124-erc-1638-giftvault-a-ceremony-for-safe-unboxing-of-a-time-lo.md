---
source: magicians
topic_id: 2124
title: "ERC-1638: GiftVault -- a ceremony for safe unboxing of a time-locked multisig smart contract holding gifts"
author: ontofractal
date: "2018-12-04"
category: EIPs
tags: [multisigs]
url: https://ethereum-magicians.org/t/erc-1638-giftvault-a-ceremony-for-safe-unboxing-of-a-time-locked-multisig-smart-contract-holding-gifts/2124
views: 711
likes: 3
posts_count: 1
---

# ERC-1638: GiftVault -- a ceremony for safe unboxing of a time-locked multisig smart contract holding gifts

Hi everyone!

I’ve submitted [an EIP](https://github.com/ethereum/EIPs/pull/1638) to propose a new kind of mostly* safe gifting experience for assets on the Ethereum blockchain.

**Summary**

GiftVault smart contract standard and ceremony are designed to provide superior gifting/unboxing experience that doesn’t impose undue operation security burdens and assures peace of mind for participants.

**Abstract**

This standard provides basic functionality to create, transfer, and recover assets packaged as gifts on the Ethereum blockchain. GiftVault is designed to be compatible with multiple third-party wallets.

**Gifter and gift recepient perform a guided ceremony** to protect the gift both from malicious actors and inadvertent loss.

User experience of any gift-related product is paramount. As as result GiftVault specs include both smart contract interface specification and UX/UI specs for wallets and apps.

GiftVault design embraces redundancy to minimize loss of assets which leads to increased complexity. UX/UI trials are required before finalization of standard.

Gifts are a powerful viral user acquisition channel and as a result wallets are incentivized to implement the GiftVault standard and maintain the notification infrastructure.

**Next steps**

This is a first draft. Next iterations require extensive testing by wallet developers and users.

Your feedback, discussion, and criticism are appreciated.

Thank you
