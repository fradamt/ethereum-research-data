---
source: magicians
topic_id: 13973
title: Draft EIP：Can be claimed NFT
author: naqunmiemie
date: "2023-04-25"
category: EIPs
tags: [nft, token]
url: https://ethereum-magicians.org/t/draft-eip-can-be-claimed-nft/13973
views: 418
likes: 0
posts_count: 5
---

# Draft EIP：Can be claimed NFT

A problem was recently discovered when I use ERC3525.

Currently, NFT often encapsulates some assets. When we purchase the NFT, we may expect to purchase the assets enclosed in the NFT. However, when ERC721 is transferred, the input parameter is only tokenId, and the assets may be transferred at purchase.

## Replies

**naqunmiemie** (2023-04-25):

I expect to add a hash.

```auto
function transferFrom(address _from,address _to,uint256 _tokenId，bytes calldata hash) external;

```

Developer need to override `getHashById`.

```auto
function getHashById（uint256 _tokenId） public

```

When a transaction occurs，need to claim `hash`.

---

**naqunmiemie** (2023-04-25):

I do not intend to inherit ERC721, because it is not safe.

---

**tbergmueller** (2023-04-27):

Interesting, what you propose is also something we encountered over the last months. I think what you want to solve is prettty much the problem we outline in the [first two problem paragraphs in our upcoming EIP](https://github.com/authenticvision/ethereum-eips/blob/assetBoundNFT/EIPS/eip_draft_asset_bound_non-fungible_tokens.md#the-problem) here?

Note we are finalizing currently the EIP “Asset-bound NFT”, pull-request is expected tomorrow or over the weekend. A new thread will be opened in this forum of course. However, you can already see the complete EIP (including reference implementation) in our [fork of the ethereum-eip repo](https://github.com/authenticvision/ethereum-eips/blob/assetBoundNFT/EIPS/eip_draft_asset_bound_non-fungible_tokens.md)

In a nutshell:

We identify assets by an `anchor`, which uniquely identifies the asset and corresponds to your `hash`. Our EIP may be a overkill for your use-case, since proofing control over the asset can be used to authorize transfers, but the key idea with mapping anchors (representing the asset) corresponds exactly to what you are proposing.

How does that relate to your idea:

However, in your case, it seems you want to hash the asset (assuming with asset you mean the metadata typically provided via tokenURI?), to represent it. I’d recommend NOT to do this, as you limit the application of your EIP to “frozen” assets, and do not allow “evolvable NFTs” (refer e.g. Otherdeeds) or not even a simple “reveal”. By equipping an asset with an identifier (`anchor`), you remain the flexibility and still have a way to verify it is the same asset. But the asset itself can evolve.

As a side-note; we spun the idea of calling the “asset identifier” an “anchor” for almost 6 months, and it works surprisingly well, as you can say “We anchor the token to the asset”.  That’s an analogy all people understand, while the concept of having a hash or ID seems to be rather hard to digest for artists, investors, users, …, so simply all, that do not write smart-contracts of their own ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

---

**naqunmiemie** (2023-04-27):

Thank you for your reply. English is not my native language, so I spent more time reading your code implementation reference.

Hope your EIP becomes ERC soon !

I think my solution assets are variable:

For example, I define an NFT that allows users to create an ether coin for each one they destroy, so when the developer implements `getHashById`, the hash will be related to the number of eth in that tokenId.

The core difference between my idea and yours:

Your EIP relies on a trust  oracle for transactions.  I expect my EIP to rely on trusted front-end pages for transactions.This is the basic process I imagined for buying NFT on dex：

T1:I opened the page and found a NFT encapsulated with 10eth on dex. The browser cached the tokenHash at this time

T2:The seller secretly transferred 5 eth for this NFT.

T3:The buyer clicks to buy and the browser automatically fills in the T1’tokenHash because the page is not refreshed.And then the contract transaction fail.

In this case the user is not exposed to tokenHash.

