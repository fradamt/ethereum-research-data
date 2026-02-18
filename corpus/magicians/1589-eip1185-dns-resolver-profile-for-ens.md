---
source: magicians
topic_id: 1589
title: "EIP1185: DNS resolver profile for ENS"
author: mcdee
date: "2018-10-15"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip1185-dns-resolver-profile-for-ens/1589
views: 3520
likes: 3
posts_count: 3
---

# EIP1185: DNS resolver profile for ENS

I’ve created EIP 1185 which describes an ENS resolver profile for ENS.  This allows DNS resolvers to obtain information about ENS, and is used in EthDNS to resolve DNS records in Ethereum transparently.  Comments welcome.

Link to the EIP: https://github.com/ethereum/EIPs/edit/master/EIPS/eip-137.md

Explanation of EthDNS: https://medium.com/@jgm.orinoco/ethdns-an-ethereum-backend-for-the-domain-name-system-d52dabd904b3

## Replies

**sbacha** (2022-09-07):

Hello, is there any interest in reviving this proposed EIP? Am very interested in it!

---

**xinbenlv** (2024-12-25):

Hi Jim,

Thank you for this important ERC.

It took me a while to get to review this. Here is a few comments from my early feedback

## Editorial Suggestions

- Consider adding in the specification the ERC-165 (supportsInterface), which you already using in ref-impl
- Consider making setZonehash/zonehash optional interfaces in the requirement
- In Security Consideration, consider mentioning the importance of authorised(node) and its implication if done wrong.
- Since CoreDNS ENS Plugin supports these implementation, have you considered mentioning the CoreDNS ENS plugin and its reading side of code in GoLang?

## Technical discussions

- How do you envision  the DNS TTL being set and handled? Could you ellaborate it in the ref-impl section
- Have you considered specific way to supply DNSSEC keys when it has more implications?

