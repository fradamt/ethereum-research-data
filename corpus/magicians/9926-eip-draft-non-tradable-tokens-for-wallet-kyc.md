---
source: magicians
topic_id: 9926
title: "EIP Draft: Non-Tradable Tokens for wallet KYC"
author: Doubleweb3
date: "2022-07-13"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-draft-non-tradable-tokens-for-wallet-kyc/9926
views: 792
likes: 0
posts_count: 4
---

# EIP Draft: Non-Tradable Tokens for wallet KYC

Non-Tradable Tokens for wallet KYC (Blue Check)

- EIP Draft is available here
- Reference implementation

**Abstract**

Blue Check is a unique, non-tradable, non-transferable token representing a wallet owned by someone who has gone through a standard KYC process. This KYC token standard protects owners’ privacy and fulfills regulation requirements. This proposal also includes a revoke mechanism in case the verified wallet is compromised. All Blue Check tokens are unique; one person can only generate one token using their personal information. Those tokens do not have a monetary value and only serve as proof that this wallet passed a specific KYC process.

**Motivation**

In some countries, KYC is required for Defi, NFT trading, and exchange withdrawal. By providing a standard interface for non-tradable KYC tokens, we allow more applications to offer their services without violating laws in certain countries. The KYC tokens also need to be able to protect privacy while revealing the minimum required personal information of the account owners.

**Specification**

The KYC system comprises three main parts:

- The Blue Check (Soulbound Token for KYC)
- The OKEY (A transferrable token for revoking the Blue Check)
- The Control Hub

The Blue Check is a unique, non-tradable, non-transferable token bound with an address. The Blue Check contains the following information

- hash of first name, last name, date of birth, id number (personal hash)
- nationality

Each Blue Check will pair with an OKEY; this is a transferrable token. OKEY is minted together with Blue Check. Users should store their OKEY in a safe address immediately after receiving it. Burning the OKEY will revoke the Blue Check status.

The Control Hub is a smart contract that controls both the minting and revoking Blue Check.

Minting a Blue Check is a three-step process:

- Users need to connect their wallets to an authorized KYC solution provider.
- Users submit their KYC applications to the solution provider with an anti-fraud process.
- The solution provider confirms the document’s authenticity and generates the personal hash to mint both Blue Check and OKEY for users.

## Replies

**michelangelo** (2023-01-17):

I know a company that is doing that with Polygon - check out https://togggle.io/

---

**numtel** (2023-01-31):

I have a very similar interface on [coinpassport.net](http://coinpassport.net). I’m not familiar enough with Gitcoin Passport to make specific recommendations but I feel like it should be discussed in a standard like this.

---

**Alex-Klasma** (2023-02-03):

How does the “KYC solution provider” respond to requests for user’s data? Say I want to know who “blue check” Ethereum address **0xabc…** is, what is the process for doing that?

How does the application know what countries users are from, is some parts of the blue check public? Assuming some parts are private, how is this data secured?

It always seems like there are endless hacks for KYC data, and this could put users at extreme risk levels if their data is hacked. Oh, that guy who lives down the street holds $5,000,000 of Ethereum in his Blue Check address? *>>> $5 wrench attack!*

Seems like an extremely dangerous proposal without this critical info and security.

