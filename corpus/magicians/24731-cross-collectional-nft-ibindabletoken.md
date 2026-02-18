---
source: magicians
topic_id: 24731
title: "Cross-collectional NFT: IBindableToken"
author: sebasky-eth
date: "2025-07-04"
category: Magicians > Primordial Soup
tags: [nft, token, erc-721]
url: https://ethereum-magicians.org/t/cross-collectional-nft-ibindabletoken/24731
views: 82
likes: 0
posts_count: 2
---

# Cross-collectional NFT: IBindableToken

I created **[A]** token-agnostic minimal interface, **[B]** IERC721, **[C]** Specific implementation for multi-collectional tokens.

Core idea is based on *binding*. If token is bound to collection: it become tradable there. If not: untradable.

Binding strategies depends on implementation. It could be:

mint-burn-mint

unlock-lock-unlock

transfer to owner - transfer to collection - transfer to owner.

In my working code: mint for current smaller collection; unlock for core. But smaller always can do something else (that core code allowed).

[A] **IBindableToken**: [content-finance-contracts/src/token/common/bindable/IBindableToken.sol at master · sebasky-eth/content-finance-contracts · GitHub](https://github.com/sebasky-eth/content-finance-contracts/blob/master/src/token/common/bindable/IBindableToken.sol)

It’s just face for dApps. Informs about potential binds for users. If token is bindable, dApps could list what kind of collections will come with specific token. Very important for exchanges.

[B] **IERC721Bindable**: [content-finance-contracts/src/token/common/bindable/IBindableToken.sol at master · sebasky-eth/content-finance-contracts · GitHub](https://github.com/sebasky-eth/content-finance-contracts/blob/master/src/token/common/bindable/IBindableToken.sol)

It’s also face, but extended for IERC721.

*effectiveOwnerOf(uint256 tokenId)* gives information about ownership in entire cross-collection.

*isBound(uint256 tokenId)* points to binding status for token

[C] **Multipaired group**: core collection has all tokens, smaller ones act like groups. Token can belong only to two collections: core or its specific group.

It’s highly utilized for gas:

1. All collections are deployed by CREATE3 factory, so verification of binding mechanism is cheap. Core has salt 0. Smaller ones: bytes32(groupId).
2. Core collection must has in tokenId information about group: [tokenIdInGroup][groupId].
3. There a lot more to optimize, but not in my collection, because it was released before core. So it act independently from it. However, if core is released, smaller ones don’t need to store ownership data

Core: **IERC721MultipairedBinder** ([content-finance-contracts/src/token/erc721/IERC721MultipairedBinder.sol at master · sebasky-eth/content-finance-contracts · GitHub](https://github.com/sebasky-eth/content-finance-contracts/blob/master/src/token/erc721/IERC721MultipairedBinder.sol))

Smaller: **IERC721PairedBinder** ([content-finance-contracts/src/token/erc721/IERC721PairedBinder.sol at master · sebasky-eth/content-finance-contracts · GitHub](https://github.com/sebasky-eth/content-finance-contracts/blob/master/src/token/erc721/IERC721PairedBinder.sol))

**For indexers:**

*IERC721PairedBinder* (smaller) emit:

*MultiGroupRegistered(IBindableMultiGroup indexed core, uint256 indexed groupIdInCore)*

That to points to its core.

*IERC721MultipairedBinder* (bigger) emits:

*BinderFactory(address factory)*

For verification of PairedBinders.

*GroupMetadata(uint256 offsetInGroupId, uint256 bitWidthInGroupId, uint256 offsetInTokenId, uint256 bitWidthInTokenId)*

For fast mapping: tokenId in core ↔ tokenId in specific group

**Deployed Implementation of smaller collection: ERC721PairedBinderPrelaunched**

([content-finance-contracts/src/token/erc721/open-zeppelin-extensions/ERC721PairedBinderPrelaunched.sol at master · sebasky-eth/content-finance-contracts · GitHub](https://github.com/sebasky-eth/content-finance-contracts/blob/master/src/token/erc721/open-zeppelin-extensions/ERC721PairedBinderPrelaunched.sol))

For *IERC165* interface I went to: *IBindableToken*, *IERC721Bindable*, *IERC721PairedBinder*

However IERC721Bindable was overkill. I think *IBindableToken*, *IERC721PairedBinder* was enough.

**Binding works by:**

Owner call *bind* → contract call *unbindFor* in other (limitation is to one maximum bind).

Owner call *unbind* → contract call *bindFor* in other.

Owner send token to collection → contract call *unbindFor*, *bindFor* depending on *to*.

**How prerelease work?**

Unbinding is blocked from core until it was done at last once.

Every transfer call low-level call IERC721MultipairedBinder.mirroredTransferFrom.

**There are also more possible systems**

SoloBinders: *IDirectedBinder* ([content-finance-contracts/src/token/common/bindable/IDirectedBinder.sol at master · sebasky-eth/content-finance-contracts · GitHub](https://github.com/sebasky-eth/content-finance-contracts/blob/master/src/token/common/bindable/IDirectedBinder.sol))

Does not need core. Owner select new target for binding in active binder. Or call target collection with previous binder.

You could use *IERC721CoreBinder* ([content-finance-contracts/src/token/erc721/IERC721CoreBinder.sol at master · sebasky-eth/content-finance-contracts · GitHub](https://github.com/sebasky-eth/content-finance-contracts/blob/master/src/token/erc721/IERC721CoreBinder.sol)) for custom centralized system. *IERC721MultipairedBinder*, which I focus on, has strong limitations: 2 collections max for specific token.

## Replies

**sebasky-eth** (2025-07-06):

[![bindable token music nft](https://ethereum-magicians.org/uploads/default/optimized/2X/6/65e43cbe0069cc3da78f708b87cabf92fd22d273_2_690x431.png)bindable token music nft1920×1200 79.9 KB](https://ethereum-magicians.org/uploads/default/65e43cbe0069cc3da78f708b87cabf92fd22d273)

Diagram showing how MultipairedBinder looks like in example of Discography - Albums

