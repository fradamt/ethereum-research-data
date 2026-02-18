---
source: magicians
topic_id: 19716
title: "ERC-7695: Ownership Delegation and Context for ERC-721"
author: ducthotran2010
date: "2024-04-19"
category: ERCs
tags: [erc, nft, erc-721]
url: https://ethereum-magicians.org/t/erc-7695-ownership-delegation-and-context-for-erc-721/19716
views: 1118
likes: 6
posts_count: 3
---

# ERC-7695: Ownership Delegation and Context for ERC-721

Hi Magicians,

I’m from the Axie community, currently, we’re currently grappling with scalability issues and want to encourage financial dApps for Axies without changing ownership due to lots of infrastructure and rewarding systems built on top of the ERC721 Axie standard.

Therefore I would like to propose an extension for ERC-721 tokens to facilitate a broader range of dApps (involving renting, delegating actions, and collateral systems). This proposal is to enhance NFT ownership without transferring to any contracts to perform renting or delegating actions. Furthermore, these extensions aim to support the integration of ERC-721 tokens into collateral systems in different and complex contexts.

Please read more at [ERCs/ERCS/erc-7695.md at erc · ducthotran2010/ERCs · GitHub](https://github.com/ducthotran2010/ERCs/blob/erc/ERCS/erc-7695.md)

https://github.com/ethereum/ERCs/pull/391

## Replies

**nvnamsss** (2024-04-24):

This proposal has the potential to improve the quality of life. Based on the current interface specification, the asset owner has no permission to cancel the right of ownership?

---

**ducthotran2010** (2024-04-25):

If I understand correctly, you might wonder why the NFT owner does not have permission to cancel the delegation once his/her NFT is delegated to someone.

Technically if owners have permission to cancel delegations, it seems like an approval for operators to control NFTs for owners, which was already introduced in the ERC-721 standard before (via `approve` or `setApprovalForAll`).

The ownership delegation can help with the mechanism which temporarily *transfers* the ownership rights from owners to delegatees until the agreement expires. This will:

- Provide us with a solid commitment between owners and delegatees.
- And enable the development of other dApps that can leverage this type of commitment.

E.g. Collateral contracts cannot built on top of ERC-721 without forcing to lock tokens in the contracts because using `approval` method seems ineffective since the owner can revoke approval at any moment. These contracts may find the mechanism to be a useful alternative.

