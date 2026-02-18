---
source: magicians
topic_id: 21612
title: "EIP-XXXX: Scaled Signature Scheme for Off-Chain Signature Distinction"
author: ethmag
date: "2024-11-07"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-xxxx-scaled-signature-scheme-for-off-chain-signature-distinction/21612
views: 100
likes: 5
posts_count: 5
---

# EIP-XXXX: Scaled Signature Scheme for Off-Chain Signature Distinction

Note: Have not created PR yet, as it is advised to get recommendations.

Abstract:

This EIP proposes a new signature method, eth_safeSign, which introduces a scaling factor applied to the private key during the signing process. By modifying the signature in a way that cryptographically distinguishes off-chain signatures from on-chain signatures, this method aims to mitigate phishing attacks where users are tricked into signing malicious messages. This allows decentralized applications (dApps) to verify the signer by retrieving the original public key from the scaled signature, enhancing the security of off-chain authentication and verification processes.

Outstanding issue:

Let me know if you would like to have full details formulated in PR.

## Replies

**0xwitty** (2024-11-07):

How does this scaled signature method impact the usability of dApps, especially in terms of user experience and performance when verifying off-chain signatures?

---

**frangio** (2024-11-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethmag/48/13467_2.png) ethmag:

> this method aims to mitigate phishing attacks where users are tricked into signing malicious messages

I think this is already addressed by ERC-191 and EIP-712, at least to the same extent that this proposal would. That is to say, phishing is not at all a solved problem, but the signature schemes don’t seem to be the problem.

---

**ethmag** (2024-11-07):

Point operations to recover original public address is super cheap and dApps will be as performant.

Today users are reluctant to interact with dApps that ask to sign a simple sign-in message, because of phishing concerns. Scaled signatures would increase confidence of a user in interacting with dApps that often ask for signatures for off-chain purposes.

---

**ethmag** (2024-11-07):

Existing signature schemes are great. But scaled signatures would allow separation of concerns between off-chain and on-chain signatures. Most importantly, a user will be able to distinguish whether a signed message would have on-chain consequences without being extra vigilant.

