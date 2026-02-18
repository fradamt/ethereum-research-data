---
source: magicians
topic_id: 7216
title: ERC-2350 - Semantic contracts
author: Daniella
date: "2021-10-06"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-2350-semantic-contracts/7216
views: 845
likes: 1
posts_count: 2
---

# ERC-2350 - Semantic contracts

# Simple Summary

Store relevant infos on contract, in hexadecimal or hash to IPFS/other network file, instead of relying on individual data provided by different blockchain explorers.

# Motivation

Tokens already stores the most basic useful information: name, symbol, decimals. This data is used by APIs, services and blockchain explorers. But other information (site url, email, blog, social networks) depends to be updated on individual blockchain explorers. It gives more work to contract developers, instead of just focus on development. It also makes discrepancy between different services with contrasting infos which can mislead users.

# Abstract

Info are hexadecimal fields. If they are big, refer to a hash of external file, instead. All assets a token refers (such as icon), are hosted in Swarm, IPFS or other network.

- Type (contract, app, game, function)
- Category (different categories according to type)
- Icon
- Description
- Banner/cover
- Email (can add more than one, referring to a single file with emails)
- Blog (can refer to multiple places: hugo, Medium, Steemit - also in a single file if more than one)
- Social networks
- Developer (if contains fields or more than one, store in a file)
- Git repo
- Whitepaper

All data need to be in JSON format. Also, files such as a git repo can have the same file/folder linked into multiple locations (same file in IPFS, Swarm, SSB, etc).

# Specification

Its still a draft. If you’re technically skilled, please tell your thoughts to update this.

# Challenges

Exchanges and other services need to support new token standards otherwise only ERC20; or, this ERC can be just a compatible extension.

## Replies

**Daniella** (2021-10-19):

This proposal on GitHub: [ERC-2350 Semantic contracts (ERC extension - draft) · Issue #2350 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/2350)

