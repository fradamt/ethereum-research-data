---
source: magicians
topic_id: 13091
title: Canonical Token List Standard from the EEA-OASIS Community Projects L2 Standards Working Group
author: highlander
date: "2023-02-28"
category: EIPs
tags: [governance]
url: https://ethereum-magicians.org/t/canonical-token-list-standard-from-the-eea-oasis-community-projects-l2-standards-working-group/13091
views: 1491
likes: 0
posts_count: 1
---

# Canonical Token List Standard from the EEA-OASIS Community Projects L2 Standards Working Group

# 1 Introduction

The [L2 WG](https://github.com/eea-oasis/L2) is an open-source initiative with a scope to

- Identify and document the most relevant use cases and business requirements for Layer 2 and other Blockchain Scalability solutions for EVM-compatible public blockchains
- Define a technical standard with identification and differentiation of classes of scalability solutions as required that meet both ecosystem and enterprise requirements, with a particular focus on interoperability between Layer 2 solutions for EVM compatible public blockchains
- For EVM-compatible public blockchains, identify, document, and devise solution approaches for Layer 2 Blockchain scalability solution-specific challenges such as MEV, block (gas) limits, TVL concentration, etc.
- Identify and document characteristics of Layer 2 Blockchain environments for EVM-compatible public blockchains that will be key in addressing mainstream and enterprise adoption.

The work is an [EEA Community Project](https://entethalliance.org/eeacommunityprojects/), which is managed by [OASIS](https://oasis-open-projects.org/).

The L2 Standards WG has just released a first draft of a [Canonical Token List specification](https://github.com/eea-oasis/L2/blob/main/workitems/tokenlist/l2-token-list-v1.0-psd01.md). The WG is intending to release this specification also as an EIP. As part of the EIP process, this post is to start a discussion on this topic.

## 1.1 Overview

There is a significant challenge around the definition and listing of tokens on Layer 1 (L1), Layer 2 (L2), and Sidechain systems. Note that for simplicity, this document we will collectively refer to L1, L2 and Sidechain systems as chains below since the challenge described below is valid across all such systems:

- Consensus on the “canonical” token on chain B that corresponds to some token on chain A. When one wants to bridge token X from chain A to chain B, one must create some new representation of the token on chain B. It is worth noting that this problem is not limited to L2s – every chain connected via bridges must deal with the same issue.

Related to the above challenge is the standardization around lists of bridges and their routes across different chains. This will be addressed in a separate document.

Note that both of these issues are fundamental problems for the current multi-chain world.

Therefore, the goal of this document is to help token users to operationalize and disambiguate the usage of a token in their systems.

Also, note that a standard for defining tokens is beyond the scope of this document.
