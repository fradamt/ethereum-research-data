---
source: magicians
topic_id: 9911
title: "EIP-5218: NFT Rights Management"
author: iseriohn
date: "2022-07-12"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-5218-nft-rights-management/9911
views: 2673
likes: 1
posts_count: 3
---

# EIP-5218: NFT Rights Management

Hi, we’re drafting an EIP for managing NFT licenses. The standard provides basic functionality to create, transfer, and revoke licenses, and to determine the current licensing state of an NFT.

The EIP-721 standard defines an API to track and transfer ownership of an NFT. When an NFT is to represent some off-chain asset, however, we would need some legally effective mechanism to *tether* the on-chain asset (NFT) to the off-chain property. One important case of off-chain property is creative work such as an image or music file. Recently, most NFT projects involving creative works have used licenses to clarify what legal rights are granted to the NFT owner. But these licenses are almost always off-chain and the NFTs themselves do not indicate what licenses apply to them, leading to uncertainty about rights to use the work associated with the NFT. It is not a trivial task to avoid all the copyright vulnerabilities in NFTs, nor have existing EIPs addressed rights management of NFTs beyond the simple cases of direct ownership (see EIP-721) or rental (see EIP-4907).

This EIP attempts to provide a standard to facilitate rights management of NFTs in the world of Web3. In particular, ERC-5218 smart contracts allow all licenses to an NFT, including the *root license* issued to the NFT owner and *sublicenses* granted by a license holder, to be recorded and easily tracked with on-chain data. These licenses can consist of human-readable legal code, machine-readable summaries such as those written in CC REL, or both. An EIP-5218 smart contract points to a license by recording a URI, providing a reliable reference for users to learn what legal rights they are granted and for NFT creators and auditors to detect unauthorized infringing uses.

Check out [EIP-5218](https://eips.ethereum.org/EIPS/eip-5218) for more details. We’d love to hear your thoughts on this!

## Replies

**SamWilsn** (2022-07-22):

Seems somewhat related to: [EIPs/eip-5289.md at 03fa0a067a35eb2cc37245a79aa6f0987e670d5c · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/blob/03fa0a067a35eb2cc37245a79aa6f0987e670d5c/EIPS/eip-5289.md)

---

**iseriohn** (2022-07-25):

Thank you for the reference. At the time of drafting eip-5218, the eip-5289 hadn’t been proposed yet. A few differences as follows:

1. EIP-5289 provides a general “notary” service that records evidence of an off-chain legal document, while EIP-5218 is particularly designed to get NFT licensing right, and is compatible with EIP-721 so NFT licenses can transfer with NFTs.
2. There’s no on-chain linkage among documents signed via EIP-5289, nor between a legal document and an NFT, while EIP-5218 records the NFT license and potentially sublicenses to an NFT in a tree structure, which makes it easier for users to track what they are purchasing and what rights to an NFT have already been granted.
3. Again, EIP-5218 is NFT specific, the APIs and reference implementations are all devised under the context of NFTs. In addition, we also provide the IC3 NFT license as a reference for NFT licensing language.

Our reference implementation attempts to tether NFTs with licenses to the creative work and can work without EIP-5289. A scenario where the integration of EIP-5218 and EIP-5289 could be useful is when the transfer of an NFT transfers the copyright of the creative work, which requires explicit consent from the new owner. In this case, one can implement a smart contract for atomically (1) signing the legal contract via EIP-5289, and (2) transferring the NFT together with the copyright ownership via EIP-5218. Either both take place or both revert.

We can add this option in our EIP. What do you think?

