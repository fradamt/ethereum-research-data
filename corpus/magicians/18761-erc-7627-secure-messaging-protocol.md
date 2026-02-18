---
source: magicians
topic_id: 18761
title: "ERC-7627: Secure Messaging Protocol"
author: bizliaoyuan
date: "2024-02-18"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7627-secure-messaging-protocol/18761
views: 1482
likes: 6
posts_count: 7
---

# ERC-7627: Secure Messaging Protocol

[github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/268)














####


      `master` ← `chenly:erc-chat`




          opened 06:56PM - 18 Feb 24 UTC



          [![](https://avatars.githubusercontent.com/u/13716?v=4)
            chenly](https://github.com/chenly)



          [+143
            -0](https://github.com/ethereum/ERCs/pull/268/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/ERCs/pull/268)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.












## Abstract

This proposal implements the capability to securely exchange encrypted messages on-chain. Users can register their public keys and encryption algorithms by registration and subsequently send encrypted messages to other users using their addresses. The interface also includes enumerations for public key algorithms and a structure for user information to support various encryption algorithms and user information management.

## Objectives

1. Provide a standardized interface for implementing messaging systems in smart contracts, including user registration and message sending functionalities.
2. Enhance flexibility and scalability for messaging systems by defining enumerations for public key algorithms and a structure for user information.
3. Define events for tracking message sending to enhance the observability and auditability of the contract.
4. Using a custom sessionId allows messages to be organized into a conversation.

## Replies

**SamWilsn** (2024-07-23):

A few non-editorial related comments:

- I raised a similar idea for an on-chain key registry in Pretty good privacy (PGP / GPG) on-chain keyserver. Happy to see someone else exploring the same space!
- Using an enumeration for key types might limit the future expandability of the standard. What if a new algorithm comes along?
- It might be a good idea to allow users to store one public key per algorithm, instead of just one per user, and further, you might want to allow users to store separate signing/encryption keys for validation vs. encryption.

---

**0xTraub** (2024-07-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> It might be a good idea to allow users to store one public key per algorithm, instead of just one per user,

I agree, which also means the `function sendMessage()` and `event MessageSent` will probably need to specify which algorithm the message was encrypted with (or at least the associated public key) so that the recipient can properly decrypt it. This may also make it easier for indexers and clients to process incoming messages if it’s a lot and to switch which one is used if vulnerabilities or other issues are found.

---

**bizliaoyuan** (2024-08-29):

As you mentioned, having a wallet store only one public key is not a good design. I modified the implementation to allow users to set multiple public keys and specify expiration times.

---

**sewing848** (2025-06-15):

Hello. I came across this EIP only recently, after working on a decentralized messaging system for general use on EVM compatible blockchains. My somewhat different approach was already integrated into a working application, so I have submitted a version of that in [another ERC](https://ethereum-magicians.org/t/erc-stateless-encrypted-communication-standard/24554).

I tend to agree with what others have posted here - that the protocol is somewhat restrictive. But that might well be a feature, not a bug, in some specific application. I am curious to know whether you, or anyone else, has used the approach described here in an actual app - whether in development or production. Do you have any information on this?

Also - there is one part of the design that I don’t fully understand the rationale for, which is using a custom session ID to allow messages to be organized into a conversation.

You stated in the ERC that “The use of session IDs in message transactions allows multiple messages to be grouped under specific conversations. This feature is crucial for organizing and managing discussions within a dApp, providing users with a coherent and structured messaging experience.”

However, the simpler approach is to treat events sent between a pair of addresses as a single conversation within any app that is sending data through the `sendMessage()` function and reading data from the `MessageSent` event. I would be interested in understanding why you made this design choice, since the necessity of a session ID is not immediately obvious to me.

Scott

---

**bizliaoyuan** (2025-11-28):

Hi Scott, thanks for raising these points — I appreciate the thoughtful questions.

I’ve been following the recent discussions in the ecosystem about encrypted messaging, including [Vitalik’s latest comments](https://x.com/VitalikButerin/status/1993803663026860125) highlighting the importance of permissionless identities and metadata-minimized communication. In light of that, I’d like to clarify why ERC-7627 takes the shape it does.

### 1. On whether this approach is used in actual applications

Yes. The interface came out of several dApp integrations where developers needed a very small, chain-native primitive for encrypted messaging. These projects were experimenting with account-abstraction wallets, multi-party coordination, and private in-app communication channels.

The goal was never to build a full protocol like Signal/Session/SimpleX, but rather a **minimal envelope** that dApps can compose with.

---

### 2. Why a sessionId is included, and why (from, to) is not enough

You’re right that for the simplest case — one linear conversation between two addresses — `sessionId` is not strictly necessary.

However, in practice many real applications require **multiple concurrent contexts** between the same two parties. Examples include:

- parallel threads (e.g. “support”, “trading”, “governance”)
- contract-originated messages that belong to different logical flows
- group or multi-device messaging
- integrations where each conversation has its own ephemeral key state

Modern E2EE systems (including Session/SimpleX, as noted by VB) separate conversations into explicit sessions or queues for exactly these reasons: it improves state isolation, reduces metadata leakage, and helps clients operate statelessly.

Ethereum frontends reconstruct everything from logs, so having an explicit session identifier gives applications a **deterministic, portable, and indexable** way to organize threads — without dictating how they must implement their cryptographic or routing logic.

Importantly, apps that prefer the simple model can still derive:

```auto
sessionId = keccak256(abi.encodePacked(from, to))
```

So nothing becomes harder, but more sophisticated applications gain the structure they need.

---

### 3. Design philosophy

The ERC intentionally stays minimal:

- no ratchets
- no routing rules
- no inbox semantics
- no device-sync requirements

Those belong to higher-level protocols.

The aim here is only to provide a small, interoperable foundation that dApps can build on top of.

---

**0xTraub** (2025-12-15):

Im on board with a `sessionId` as a form of metadata but what if session id is too restrictive. If the goal is for frontends to be able to organize and display based on this information why stop at a session Id? Why not just make it `Metadata` and specify the format as `JSON` or `YAML`? That would allow a lot more flexibility on the frontend. You could also encrypt that as well. The spec already specifies session ID as a string type so switching to a bytes type wouldn’t be a dramatic change either.

