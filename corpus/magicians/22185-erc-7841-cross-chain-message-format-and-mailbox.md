---
source: magicians
topic_id: 22185
title: "ERC-7841: Cross-chain Message Format and Mailbox"
author: ellie
date: "2024-12-12"
category: ERCs
tags: [erc, rollups, cross-chain]
url: https://ethereum-magicians.org/t/erc-7841-cross-chain-message-format-and-mailbox/22185
views: 527
likes: 7
posts_count: 3
---

# ERC-7841: Cross-chain Message Format and Mailbox

This ERC proposes a mailbox API and message format for sending and receiving data between L2s. It is intentionally designed to be general, providing a foundational standard for building application-specific messaging protocols.  This ERC is analogous to the Internet Protocol; it focuses on a format for sending and receiving messages, but leaves everything else up to higher-level protocols.

This ERC has similar motivations as [ERC-7786](https://ethereum-magicians.org/t/erc-7786-cross-chain-messaging-gateway/21374). Both standards offer general cross-chain interfaces, but differ in how messages are represented and stored on chain.  It may make sense to combine this ERC with ERC-7786 or vice versa.

[ERC PR](https://github.com/ethereum/ERCs/pull/766)

## Replies

**kalmanL** (2025-01-16):

Hey I have a question regarding sessionId. As I understand the purpose of this is to allow the singing of txs on multiple chains in parallel ( before the txs are submitted), and the different txs can trigger the interop on multiple chains.

Would it not be easier to add some other access management scheme, e.g. add an ExecutionAddress/EntryPoint that can trigger the interop txs? The only problem then would be paying for gas, but that is simpler and can also be solved

---

**philippecamacho** (2025-01-20):

Hey! Thank you for your question.

You are right regarding the *sessionId* value. Its purpose it to enable contracts deployed on different chains to coordinate by fetching the right messages from the Mailbox.

> Would it not be easier to add some other access management scheme, e.g. add an ExecutionAddress/EntryPoint that can trigger the interop txs? The only problem then would be paying for gas, but that is simpler and can also be solved

This standard aims at capturing communication protocols where application contracts proactively fetch information from the *Mailbox*. We call this communication model *PULL* (the application pulls from the Mailbox). What you are proposing makes all the sense, yet it corresponds to the *PUSH* model where the *Mailbox* calls a function on the destination chain contract. This communication model is the most common in practice and there are already a number of standards for it, such as [ERC 7786](https://ethereum-magicians.org/t/erc-7786-cross-chain-messaging-gateway/21374).

