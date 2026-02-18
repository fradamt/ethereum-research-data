---
source: magicians
topic_id: 14330
title: "SHADOW: A Scheme-Handler Discovery Option for Wallets"
author: SamWilsn
date: "2023-05-17"
category: EIPs
tags: [wallet]
url: https://ethereum-magicians.org/t/shadow-a-scheme-handler-discovery-option-for-wallets/14330
views: 1654
likes: 3
posts_count: 6
---

# SHADOW: A Scheme-Handler Discovery Option for Wallets

This proposal (affectionately known as SHADOW) is an alternative to EIP-1193 for wallet discovery in web browsers that requires no special permissions. Web pages intending to open a connection to a wallet inject an `iframe` tag pointing at a well-known scheme. Communication between the page and the wallet uses the `postMessage` API.

## Replies

**SamWilsn** (2023-05-17):

The proposal pull request: [Add EIP: Scheme-Handler Discovery Option for Wallets by SamWilsn · Pull Request #7039 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/7039)

---

**SamWilsn** (2023-05-17):

Some WebExtensions to show a proof of concept: [GitHub - SamWilsn/wallet-demo](https://github.com/SamWilsn/wallet-demo)

These show an extension replying to a `postMessage` using an `iframe` and protocol handler in both Chrome and Firefox.

---

**SamWilsn** (2025-03-03):

Could be useful for future standards: [Local Peer-to-Peer API](https://wicg.github.io/local-peer-to-peer/)

---

**sbacha** (2025-03-08):

Was there any issues in your PoC regarding connectivity?

---

**SamWilsn** (2025-03-18):

This proposal (SHADOW) doesn’t rely on any networking, but still requires the wallet to register a scheme handler. That’s annoying for mobile/hardware wallets.

With WebRTC (or possibly this local peer-to-peer API), you get better options.

