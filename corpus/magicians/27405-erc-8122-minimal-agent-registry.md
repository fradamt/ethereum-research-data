---
source: magicians
topic_id: 27405
title: "ERC-8122: Minimal Agent Registry"
author: nxt3d
date: "2026-01-09"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8122-minimal-agent-registry/27405
views: 78
likes: 2
posts_count: 1
---

# ERC-8122: Minimal Agent Registry

I’m proposing **ERC-8122: Minimal Agent Registry**, a lightweight, deployable onchain registry for **discovering AI agents**.

It combines:

- ERC-6909 (gas-efficient registry/token design)
- ERC-8048 (fully onchain key/value agent metadata)
- ERC-7930 (globally unique registry identifier)
- Optional ERC-8049 (contract-level registry metadata)

Spec draft: [https://github.com/nxt3d/ERCs/blob/agent-registry/ERCS/erc-agent-registry.md](https://github.com/ethereum/ERCs/pull/1463)

## Motivation

Existing approaches like ERC-8004 define an ERC-721-based agent registry intended to be a singleton (one per chain). Many use cases instead need custom registry deployments, such as curated collections, specialized domains, or fixed-supply registries.

## Key Points

- Global agent identifier: agentRegistry (ERC-7930 address) + agentId.
Display: :
- Single-owner model with ownerOf(agentId); transfers require amount == 1.
- Agent metadata stored onchain via ERC-8048; recommended keys include name, description, endpoint_type,
endpoint, agent_account.
- Registries MAY implement ERC-8049, for contract level metadata.
