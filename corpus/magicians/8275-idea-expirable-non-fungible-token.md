---
source: magicians
topic_id: 8275
title: "Idea: Expirable Non-Fungible Token"
author: Jeffxz
date: "2022-02-12"
category: Magicians > Primordial Soup
tags: [nft, token]
url: https://ethereum-magicians.org/t/idea-expirable-non-fungible-token/8275
views: 1949
likes: 0
posts_count: 7
---

# Idea: Expirable Non-Fungible Token

## Simple Summary

This is an idea for Expirable NFTs, which extends ERC-721.

It is called Expirable Non-Fungible Token (ENFT) to provide potential NFT lending use cases.

## Abstract

The [ERC-721](https://eips.ethereum.org/EIPS/eip-721) is mainly used for transferring digital or physical assets and transfer interface does not have any expiration date.

Meanwhile, there are some potential possibility of lending NFT such as digital book as NFT which a digital library could lend to person for a certain period. A NFT owner might lend his/her collection to other party momentarily. Or even 1 year real estate rental.

With ENFT then when the expiration date is due the NFT temporary ownership will be revoked and the original owner will re-own the digital or physical assets.

The ENFT does not consider combining lending condition contract (usually happens in physical world) at this moment but it can be expanded in the future with combine support of lending contract.

## Summary

The ENFT can be considered as extention of [ERC-721](https://eips.ethereum.org/EIPS/eip-721) which adding expiration date to support a temporarily ownersip will be expired in future date.

## Replies

**poria-cat** (2022-02-13):

[unlock protocol](https://unlock-protocol.com/)  works on it

---

**Jeffxz** (2022-02-13):

Thanks!

Any ideas about if [unlock protocol](https://unlock-protocol.com/) started draft an EIP standard extention about it?

I was trying to propose a standard extention if no one is already working on it.

---

**poria-cat** (2022-02-14):

They did’t write EIP, so feel free to do it.

---

**AriaNaraghi** (2022-07-13):

Have you written an EIP for it? I really support this Idea. We can work on it together if you want.

---

**edison0xyz** (2022-07-13):

This has been resolved in [EIP-4907: Rental NFT, ERC-721 User And Expires Extension](https://eips.ethereum.org/EIPS/eip-4907). It has expiration added into it.

---

**AriaNaraghi** (2022-07-16):

Thanks for the information. I appreciate it.

