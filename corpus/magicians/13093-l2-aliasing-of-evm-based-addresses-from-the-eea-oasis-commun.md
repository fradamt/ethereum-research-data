---
source: magicians
topic_id: 13093
title: L2 Aliasing of EVM based Addresses from the EEA-OASIS Community Projects L2 Standards Working Group
author: highlander
date: "2023-02-28"
category: EIPs
tags: [layer-2, address-space]
url: https://ethereum-magicians.org/t/l2-aliasing-of-evm-based-addresses-from-the-eea-oasis-community-projects-l2-standards-working-group/13093
views: 1969
likes: 0
posts_count: 3
---

# L2 Aliasing of EVM based Addresses from the EEA-OASIS Community Projects L2 Standards Working Group

# 1 Introduction

The [L2 WG](https://github.com/eea-oasis/L2) is an open-source initiative with a scope to

- Identify and document the most relevant use cases and business requirements for Layer 2 and other Blockchain Scalability solutions for EVM-compatible public blockchains
- Define a technical standard with identification and differentiation of classes of scalability solutions as required that meet both ecosystem and enterprise requirements, with a particular focus on interoperability between Layer 2 solutions for EVM compatible public blockchains
- For EVM-compatible public blockchains, identify, document, and devise solution approaches for Layer 2 Blockchain scalability solution-specific challenges such as MEV, block (gas) limits, TVL concentration, etc.
- Identify and document characteristics of Layer 2 Blockchain environments for EVM-compatible public blockchains that will be key in addressing mainstream and enterprise adoption.

The work is an [EEA Community Project](https://entethalliance.org/eeacommunityprojects/), which is managed by [OASIS](https://oasis-open-projects.org/).

The L2 Standards WG has just released a first draft of a [L2 Aliasing of EVM based Addresses specification](https://github.com/eea-oasis/L2/blob/main/workitems/EVM-based-L2-address-aliasing/evm-based-l2-address-aliasing-v1.0-psd01.md). The WG is intending to release this specification also as an EIP. As part of the EIP process, this post is to start a discussion on this topic.

## 1.1 Overview

The ability to deterministically derive addresses of a digital asset or an externally owned account (EOA) in EVM-based execution frameworks for L1s, L2s, and Sidechains based on an origin chain of an asset or EOA, known as address aliasing, simplifies interoperability between EVM based L1s, L2s, and Sidechains because:

- It allows messages from chain A (source chain) to unambiguously address asset A (smart contract) or EOA on chain Y (target chain), if asset A or EOA exists on Chain X and on Chain Y.
- It allows a user to deterministically verify the source chain of a message, and, if required, directly verify the origin chain of asset A or EOA and its state on its origin chain utilizing a canonical token list of the (message) source chain.

Note, that address-aliasing between non-EVM and EVM-based L1s, L2s, and Sidechains, and between non-EVM-based L1s, L2s, and Sidechains is out of the scope of this document.

The EIP is now in [DRAFT status](https://eips.ethereum.org/EIPS/eip-6735).

Please, review and comment!

## Replies

**SamWilsn** (2023-06-27):

There are a few other EIPs that describe addresses plus which chain they belong to. Have you considered them, and if so, what benefits does this proposal bring over those standards?

---

**highlander** (2023-07-31):

[@SamWilsn](/u/samwilsn) Apologies for the very liing delay. I presume you refer to EIP-3770 (chain specific addresses). The suggested approach generalizes 3770 and extends approaches used in practice. Hence, the proposal.

EIP-4337 (Account Abstraction) is not really relevant as the address aliasing is meant to be used in bridge messages. Similar arguments apply EIP-2678 and EIP-4834.

If there are others that I missed, please, advise.

