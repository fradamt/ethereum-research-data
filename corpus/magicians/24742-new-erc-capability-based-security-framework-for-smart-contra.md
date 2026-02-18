---
source: magicians
topic_id: 24742
title: "New ERC: Capability-Based Security Framework For Smart Contracts"
author: FeurJak
date: "2025-07-05"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/new-erc-capability-based-security-framework-for-smart-contracts/24742
views: 54
likes: 0
posts_count: 1
---

# New ERC: Capability-Based Security Framework For Smart Contracts

I’ve drafted my first ERC proposal which introduces a general framework for adopting a policy-driven & capabilty-based security model for smart-contracts that enforces zero-trust principles & accommodates local-first architecture.

There is a lack of well established security-frameworks for protocols that does not depend strongly on traditional access-control-lists & owner-based permissions. As we know these security-models suffer from the ambient authority problem & confused deputy vulnerabilities.

Zero-knowledge protocols are also pushing for a local-first architecture (e.g. Aztec PXE service, Miden Edge-Node) which works well with capability-based authorisation strategies to safeguard accounts or apps from malicious actors without sacrificing privacy (i.e. represent a capability as a cryptographic note).

The draft is rather long so I won’t post it here but will share the link:

https://github.com/FeurJak/ERCs/blob/c48f81329459a864405979a7fb361c2207de317e/ERCS/erc-7965.md

Appreciate for any critiques & feedbacks !
