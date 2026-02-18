---
source: magicians
topic_id: 4049
title: Dapplets/SOWA - Secured Open Wallet Architecture
author: Ethernian
date: "2020-02-27"
category: Web > Wallets
tags: [wallet, dapplets]
url: https://ethereum-magicians.org/t/dapplets-sowa-secured-open-wallet-architecture/4049
views: 1183
likes: 1
posts_count: 1
---

# Dapplets/SOWA - Secured Open Wallet Architecture

Hello All the Magicians,

A long time ago I published a thread and a medium article

[Dapplets: Rethinking Dapp Architecture for better adoption and security](https://ethereum-magicians.org/t/dapplets-rethinking-dapp-architecture-for-better-adoption-and-security/2799).

While we are mostly focused on the Dapplets project, we have decided to split-off the Wallet related part of it into the separate project *S.O.W.A. - Secured Open Wallet Architecture*.

**Articles:**

[Part 1: Introducing S.O.W.A. – Secured Open Wallet Architecture](https://medium.com/@Ethernian/part-1-introducing-s-o-w-a-secured-open-wallet-architecture-a89fb74bf794?source=friends_link&sk=30f8b2d23bd2cd27ecd6eb6a5e4a329c)

[Part 2: Implementing S.O.W.A. – Secured Open Wallet Architecture](https://medium.com/@Ethernian/part-2-implementing-s-o-w-a-secured-open-wallet-architecture-3787c76bd438?source=friends_link&sk=7705c47cbf5383f7e14a075b1dd39db1)

**What is it about?**

> S.O.W.A. — is a general chain agnostic standard for scripts running in the Wallet’s sandbox and describing both the confirmation View and the Action execution plan.

**What is the advantage?**

1. Interoperability between Wallets.
2. WYSIWYS Views.
3. Suitable for a wide range of hardware and security requirements.
4. Modular and extensible architecture.
5. Transaction batching (User confirms one Action starting many transactions).
6. Allows gas payments for infrastructure providers like Wallets, Bridges and Relays
7. Easy to audit; explicit specifications and audit status.

We have started work on S.O.W.A. because we need the standard for our Dapplets project and believe it would be useful for many other projects too.

Our work is still in progress, but we hope to start a discussion between Wallets and DApp developers to create new standards for better UX and interoperability.

**Acknowledgements**

A lot of thanks to [@danfinlay](/u/danfinlay), [@JamesZaki](/u/jameszaki) and [@ligi](/u/ligi) for their support and feedback!
