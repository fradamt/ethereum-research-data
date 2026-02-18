---
source: magicians
topic_id: 21885
title: "ERC-7845: Universal Orchestrator RPC"
author: IAmKio
date: "2024-11-29"
category: ERCs
tags: [orchestrator, solver]
url: https://ethereum-magicians.org/t/erc-7845-universal-orchestrator-rpc/21885
views: 123
likes: 2
posts_count: 5
---

# ERC-7845: Universal Orchestrator RPC

Hi everyone ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=15)

Currently there’s no real standard for talking to Orchestrators. The ERC i’m looking for feedback for is an attempt to try and define a **minimum standard of a request** from an app / dapp / service etc (that is looking for solution(s) to a problem(s)) to an Orchestrator.

The request being made to Solver Service is incorporated inside the [Ethereum JSON-RPC API](https://ethereum.org/en/developers/docs/apis/json-rpc/) specification for wider compatibility and adoption.

Below is an excerpt from the [HackMD document](https://hackmd.io/@IAmKio/HJjb6N5Wke).

## Abstract

> “Hey Google, swap my SHIB for Pillar”

> “Alexa, how much USDC can i buy with what’s in my wallet?”

> “Siri, send 10 OP to Vitalik and 5 PEPE to Deimantas”

The Minimal Orchestrator RPC aims to standardise the **minimum shape and requirements** of a **request for a solution** ***from*** an arbitrary system managing an Ethereum wallet ***to***, ultimately, an Orchestrator.

An arbitrary system could be a website, app, a server program etc - anything that manages an Ethereum wallet that **[speaks Ethereum JSON-RPC](https://ethereum.org/en/developers/docs/apis/json-rpc/)** and is looking to request solutions from an Orchestrator.

[![ERC_ Minimal Orchestrater RPC - Frame 1](https://ethereum-magicians.org/uploads/default/optimized/2X/1/14660905db1784a374228f1b1701bc2577ced60c_2_690x209.jpeg)ERC_ Minimal Orchestrater RPC - Frame 13626×1103 150 KB](https://ethereum-magicians.org/uploads/default/14660905db1784a374228f1b1701bc2577ced60c)

## Motivation

Data model standards can be written in any shape. A system will often expose their external interface but require that the request to the aforementioned interface is modelled in a way that the service understands. This creates a huge level of inconsistency and in turn makes Orchestrator interoperability more difficult.

Orchestrators will become more widespread and numerous over time. This is especially true with the advent of Artificial Intelligence (AI) driven systems and the continued advancement of Human Computer Interaction (HCI) devices, especially those that are voice controlled.

Standardising the request object that an Orchestrator can understand from a wallet will drive adoption and make decentralised app development easier for developers that don’t know how to make on-chain transactions or have the required technical understanding of block building systems.

[![swimlanes-c8c4fd0971c329903472d948e5282c30](https://ethereum-magicians.org/uploads/default/optimized/2X/5/587043b89dd6cb373948b7d592f484ce3fd677f2_2_690x357.png)swimlanes-c8c4fd0971c329903472d948e5282c302600×1346 108 KB](https://ethereum-magicians.org/uploads/default/587043b89dd6cb373948b7d592f484ce3fd677f2)

---

Todo:

- DONE: More JSON-RPC API examples: as many scenarios as possible should be covered
- DONE: Solver Service response examples: needs to be able to support a user interface as much as possible whilst providing the necessary transactions to allow the solution to be executed on-chain
- Specifcation review: Are the key word interpretations (RFC 2119 and RFC 8174) correct?
- DONE: Security considerations: how to handle this

This has been reviewed internally by a few people but now opening up for wider review before opening a PR in the EIPs repository.

Any feedback / suggestions / comments would be appreciated ![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=15)

Thanks in advance! ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=15)

https://hackmd.io/@IAmKio/HJjb6N5Wke

## Replies

**0xsimka** (2024-12-01):

What are the main challenges or trade-offs in designing a minimal solver service RPC interface that ensures both standardization and extensibility across different solver implementations, while avoiding fragmentation in the ecosystem?

---

**IAmKio** (2024-12-01):

The whole point of the Minimal Solver Service RPC *is* to ensure some level of standardisation and extensibility. Standardisation so that we all speak the same language when it comes to asking for a solution, and extensibility is catered for by ensuring that this is a minimal specification, to allow for future changes or use cases. Because this is proposing a minimal standard, there is going to be some fragmentation going forward but at least the basics should be standardised.

It’s worth noting that this ERC doesn’t care how the solver implementation is - just how one would ask for a solution from a solver service.

---

**IAmKio** (2025-01-11):

Just worth noting that Minimal Solver RPC has now been renamed to Minimal Orchestrator RPC after technical feedback.

---

**IAmKio** (2025-05-04):

Updated: This has been reviewed - the name has changed to Universal Orchestrator RPC

