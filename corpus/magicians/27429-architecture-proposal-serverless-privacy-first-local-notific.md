---
source: magicians
topic_id: 27429
title: "Architecture Proposal: Serverless, Privacy-First Local Notifications for dApps"
author: nicosampler
date: "2026-01-13"
category: Web
tags: [dapp, notifications]
url: https://ethereum-magicians.org/t/architecture-proposal-serverless-privacy-first-local-notifications-for-dapps/27429
views: 36
likes: 0
posts_count: 1
---

# Architecture Proposal: Serverless, Privacy-First Local Notifications for dApps

### Abstract

This post proposes an architectural pattern for implementing dApp notifications that run entirely client-side using **Service Workers (PWAs)** and direct **contract calls**. This approach removes the need for centralized backends or third-party messaging protocols for basic event monitoring (e.g., when a loan is at risk about 20% for being liquidated), offering a privacy-first, self-sovereign user experience.

### Motivation

Currently, if a dApp wants to notify a user about an on-chain event, developers typically choose between:

1. Centralized Web2 Infrastructure: Using a backend to index events and sending alerts via Email/Telegram/Discord.

- Flaw: Requires users to doxx themselves (email/Telegram account) and trust a centralized server with their address and activity metadata.

1. Decentralized Protocols: Excellent for messaging, but often introduce friction (separate onboarding) or dependency on external relayers.
2. No Notifications: Leaving the user to manually refresh the page (current status quo for many DeFi frontends).

**The Missing Piece:**

We lack a standard for **Client-Side Autonomous Notifications**.

By this, I mean a mechanism where the **dApp frontend itself** (running in the user’s browser) acts as the monitoring agent. Instead of a server sending a message *to* the user, the user’s browser actively checks the blockchain state in the background and triggers a system alert locally when a condition is met (e.g., when a loan is close to liquidation).

### Proposed Architecture

The solution leverages the **Progressive Web App (PWA)** standard and **Service Workers** to create a background process that acts as a “personal node watcher.”

#### Core Components:

1. Passive vs. Active Monitoring: The system is flexible. The dApp can automatically track connected wallets (Active) or allow users to manually input addresses to watch in a “read-only” mode (Passive).
2. Service Worker (The Engine): A script running in the background, independent of the main UI thread. It remains active to execute periodic polling and triggers the native system notifications when a specific condition is met.
3. Direct Contract Calls: The Service Worker performs direct read calls to the blockchain to check specific contract states against user-defined thresholds.
4. System Notification API: Triggers a native device notification (Desktop/iOS/Android) when a condition is met.

#### Workflow:

1. User opens dApp → Enables monitoring for an address.
2. User closes the tab.
3. Service Worker wakes up periodically (lifecycle managed by browser).
4. Worker reads data directly from the protocol contracts.
5. Logic check: if (hf < 20%) sendNotification("Risk Warning").

### Benefits

- Privacy-First: No email, no Telegram ID, no server logs. The RPC provider is the only entity that sees the read request.
- Zero Infrastructure Cost: The dApp team does not need to maintain a notification server or indexer.
- Frictionless: Users don’t need to sign transactions or connect a wallet, just paste an address.

### Open Discussion: The Adoption Gap & Unknown Unknowns

This architecture aligns perfectly with the Web3 ethos: it is trustless, permissionless, and privacy-preserving. However, despite the technology (Service Workers) having existed for years, almost no major dApp implements native client-side notifications today.

**I would love to start a discussion on two main points:**

1. The “Why”: Why hasn’t this pattern been widely adopted yet?

- Is it simply a matter of prioritization?
- Are the inconsistencies in browser background task handling (specifically on iOS) considered too high of a barrier for production apps?
- Or is there a deeper technical limitation I am overlooking?

1. Blind Spots: As I refine this architecture, what potential blockers or security risks am I missing?

- I am looking for feedback from anyone who has attempted similar “background worker” implementations in Web3 to understand where this approach might fail in a real-world, high-stakes environment.

### Proof of Concept

I have been conducting experimental tests with protocols I personally use, implementing this architecture to monitor my own positions. So far, the implementation has worked as expected, successfully triggering background notifications without the need for a persistent open tab.
