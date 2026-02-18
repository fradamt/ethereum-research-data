---
source: magicians
topic_id: 7305
title: Extension of ERC-721 standard which requires signature from recipient prior to transfer
author: mechanikalk
date: "2021-10-21"
category: Magicians > Primordial Soup
tags: [nft, erc-721]
url: https://ethereum-magicians.org/t/extension-of-erc-721-standard-which-requires-signature-from-recipient-prior-to-transfer/7305
views: 877
likes: 0
posts_count: 3
---

# Extension of ERC-721 standard which requires signature from recipient prior to transfer

Traditionally NFTs are only thought of as assets and not representations of contracts or potentially liabilities.  There are several potential use cases where commercial contracts could be created wherein one or more of the parties in the commercial contract would be identified via NFT ownership.  Moreover, that ownership would potentially carry with it both assets as well as commitments and liabilities.

Unfortunately, this means that to transfer such an NFT the recipient will need to explicitly sign a message that accepts that NFT into their wallet and states that the owner takes on the both the benefits and obligations carried forth with the NFT.

Are there any NFT standards that currently exist or that are in draft form that restrict the transfer of an NFT by requiring the receiving address to sign a message stating the intent to receive the NFT and take on both the benefits and liabilities associated?

A further extension of this could require the receiving address to have undergone some form of KYC which may be represented by an NFT held in that address. Are there any NFTs that currently exist or are in draft form that require the receiving address to have a KYC type NFT prior to being able to transfer a NFT to that address?

## Replies

**poma** (2021-10-21):

If my address owns something of negative value why don’t I just discard the address?

---

**mechanikalk** (2021-10-28):

It could hold a contract that has both benefits as well as liabilities.  For example the deed to a house has benefits, but depending on where it is located it can also have a liability, eg property tax.

