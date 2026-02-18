---
source: magicians
topic_id: 24612
title: "ERC-7978: Non Fungible Account Tokens"
author: mikelxc
date: "2025-06-20"
category: ERCs
tags: [erc, nft, wallet]
url: https://ethereum-magicians.org/t/erc-7978-non-fungible-account-tokens/24612
views: 212
likes: 1
posts_count: 3
---

# ERC-7978: Non Fungible Account Tokens

Hi everyone,

Smart-contract wallets (ERC-4337 / 7579) are gaining adoption, but today they remain invisible to the NFT ecosystem: you can’t list a wallet on OpenSea, you can’t hand it to someone in a single transfer, and NFTs themselves still behave like static receipts rather than real containers of value.

**My take:** let’s fuse the two worlds.

A **Non-Fungible Account Token (NFAT)** is an ERC-721 whose metadata *hard-codes* the address of an ERC-7579 wallet. Because the wallet’s validator accepts signatures only from the current NFT holder, transferring the token instantly transfers full control of the smart account — balances, DeFi positions, game items, history, everything.

Key points of the draft spec (link ![:point_right:](https://ethereum-magicians.org/images/emoji/twitter/point_right.png?v=12) *[ERC-7978](https://github.com/ethereum/ERCs/pull/1101)*):

- Factory + Validator pattern – one transaction mints the NFT and deploys (or references) any audited 7579 wallet (Kernel, Nexus, Safe-7579, etc.).
- No registry, no indirection – the wallet address lives right in tokenURI, so explorers and marketplaces need zero extra calls.
- Self-transfer lock & module reset – prevents accidental black-holing and ensures the new owner starts with a clean wallet.
- Backward-friendly – legacy NFTs can be wrapped; existing 6551 projects can keep their TBA registry and still offer a tradable NFAT overlay.

Looking forward to your thoughts!

## Replies

**SamWilsn** (2025-07-15):

How does this compare to [ERC-6551](https://eips.ethereum.org/EIPS/eip-6551)?

---

**mikelxc** (2025-07-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> How does this compare to ERC-6551

**ERC-6551**: NFT ↔ account binding stored in a **registry contract**; NFT metadata unchanged.

**NFAT**: NFT metadata **directly names the wallet address**; validator enforces “current NFT holder == wallet signer”; wallet is tradable anywhere ERC-721 is supported.

The philosophy is to make the wallet address part of the NFT’s identity; use a minimal validator so the NFT *is* the key. Instead of relying on a central registry coordinates the mapping and NFT point to an account;

