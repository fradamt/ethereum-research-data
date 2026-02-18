---
source: magicians
topic_id: 17157
title: "ERC-7572: Contract-level metadata via `contractURI()`"
author: ryanio
date: "2023-12-08"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7572-contract-level-metadata-via-contracturi/17157
views: 3474
likes: 9
posts_count: 21
---

# ERC-7572: Contract-level metadata via `contractURI()`

[Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7572)





###



Specifying and updating contract-level metadata










> This specification standardizes contractURI() to return contract-level metadata. This is useful for dapps and offchain indexers to show rich information about a contract, such as its name, description and image, without specifying it manually or individually for each dapp.

```solidity
interface IERC7572 {
  function contractURI() external view returns (string memory);

  event ContractURIUpdated();
}
```

## Replies

**0xCLARITY** (2024-01-03):

Should “featured image” be part of the payload as well?

I feel like OpenSea has three possible images that could be powered by contract-level metadata:

- Banner Image (banner_image)
- Collection Image (image)
- Featured Image (???)

[![os-banner-image](https://ethereum-magicians.org/uploads/default/optimized/2X/e/ee9d3d1647de8034464334f5687aabf2c6b67068_2_690x282.jpeg)os-banner-image1920×787 125 KB](https://ethereum-magicians.org/uploads/default/ee9d3d1647de8034464334f5687aabf2c6b67068)

[![os-featured-image](https://ethereum-magicians.org/uploads/default/optimized/2X/e/e193d97fe48db49ea893a02d931e544f9b0bdcf2_2_690x302.jpeg)os-featured-image1920×843 171 KB](https://ethereum-magicians.org/uploads/default/e193d97fe48db49ea893a02d931e544f9b0bdcf2)

---

**ryanio** (2024-01-03):

nice suggestion, i think it is a good idea can call it `featured_image`. however it might be hard to define just one aspect ratio for all types of websites and apps. square (1:1) would likely be the most practical?

---

**0xCLARITY** (2024-01-03):

Yeah, I think 1:1 would be the most practical.

Potentially you could have a nested JSON structure with different URLs for different aspect ratios??? But that seems unnecessarily convoluted.

---

**ryanio** (2024-01-03):

agreed keeping it 1:1 would be more simple for people to adopt and use. [added](https://github.com/ethereum/ERCs/pull/150/commits/2316cfe7722eb241ab6a47a2932cb4a2efac91ae)! thanks again for the suggestion.

edit: reconsidering omitting a suggested aspect ratio: [ERC-7572: Contract-level metadata via `contractURI()` - #14 by ryanio](https://ethereum-magicians.org/t/erc-7572-contract-level-metadata-via-contracturi/17157/14)

---

**robpolak** (2024-01-04):

Strong +1 on Adding Banner / Collection images, this is something we typically have to fetch from marketplaces that store this off-chain.

---

**ryanio** (2024-01-04):

yes, banner and collection images are present ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) images defined are now: `image`, `banner`, and `featured_image`

---

**SamWilsn** (2024-01-09):

Should there be a way for off-chain indexers to determine if `ContractURIUpdated` will be emitted? Could use [ERC-165](https://eips.ethereum.org/EIPS/eip-165) or maybe something in the metadata itself?

---

**ryanio** (2024-01-09):

Thanks for reviewing the ERC! I’m not sure if it’s necessary since offchain indexers will watch to see if `ContractURIUpdated` is emitted from any contract, the contract doesn’t necessarily have to implement ERC-165 to be added to some kind of “watch list”. I’m not opposed to adding it but don’t see much benefit. What do others think?

---

**SamWilsn** (2024-01-09):

Contracts that implement `contractURI()` today obviously don’t implement `IERC7572` and won’t return true from their `supportsInterface()` implementation.

An indexer can therefore use `supportsInterface()` to determine if they need to use an “low-efficiency” cache invalidation implementation (eg. polling), or a higher-efficiency one (watching for `ContractURIUpdated`.)

You’re suggesting indexers use the low-efficiency method for all contracts, until they receive the event, and then switching to event watching? Wouldn’t that mean indexers waste resources for contracts that never get a URI update?

---

**ryanio** (2024-01-09):

Our chain watchers are designed to get and filter logs based on event topic, so we just watch for any logs that come in with the topic0 for `ContractURIUpdated()`. We don’t have to further scope by contract address. This is easy and doesn’t require any use of `supportsInterface()`, which is why I didn’t see a need to implement it, but if other watcher systems would benefit from this then I’m not opposed to adding, it’s just not something we would use so didn’t see an immediate need for it. And as you suggest, contracts that have already been deployed won’t have the supportsInterface so it wouldn’t be a foolproof method for detecting if a contract supports the event anyhow. Thanks for continuing the discussion!

---

**SamWilsn** (2024-01-23):

I had assumed you have a list of contracts that you need to watch, some of which emit `ContractURIUpdated` when the URI changes. I guess that’s incorrect, but since you explicitly call out backwards compatibility in your proposal, I still this this is worth discussing.

Imagine the following scenario:

Someone like OpenSea who has to support a wide range of contracts.

Some of those contracts would’ve existed before ERC-7572, and some will have come after.

For contracts predating ERC-7572, the only way to detect a changed contract URI is to poll the contract periodically.

Contracts supporting ERC-7572 will emit an event when their contract URI changes.

Now, if this OpenSea-like platform wants to actually cut their server bill, they’ll want to reduce the amount of useless `eth_call`s they have to do polling for new URIs. As far as I can see it, the only way (without receiving an event) to determine if a contract requires polling or supports events is with `supportsInterface`.

---

I think just adding 165 to `requires` and a note that implementations SHOULD return true from `supportsInterface` with the correct id would be sufficient.

---

**Mani-T** (2024-01-23):

Good idea. Dapps can easily integrate this ERC, streamlining the process of displaying rich contract information.

---

**ryanio** (2024-02-05):

I think I will remove the 1:1 aspect ratio suggestion, since we cannot propose a format that makes everyone happy, and also feels weird to suggest a aspect ratio just for one of the image fields. I think dapps can just process the image however they’d like to fit into their design.

---

**xinbenlv** (2024-02-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Contracts that implement contractURI() today obviously don’t implement IERC7572 and won’t return true from their supportsInterface() implementation.

[@SamWilsn](/u/samwilsn)

That happens to every “adoption then standardization” behaviors, including ERC-20. I think it’s fine. Retroactively how to identify if a contract support certain behavior we can come up with more ideas.

---

**xinbenlv** (2024-02-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ryanio/48/10290_2.png) ryanio:

> I think I will remove the 1:1 aspect ratio suggestion, since we cannot propose a format that makes everyone happy, and also feels weird to suggest a aspect ratio just for one of the image fields. I think dapps can just process the image however they’d like to fit into their design.

Ryan, as a standard I think it’s ok to suggest a aspect ratio, as long as we don’t decline other aspect ratios.

Uses “SHOULD” for strong recommendation

```md
Image aspect ratio SHOULD be 1:1
```

means it’s *highly recommended* (but not required) for the NFT issuer to set aspect ratio to 1:1.

it means reader of NFT metadata should assume marjority of image of aspect ratio tobe 1:1 but expect exceptions.

---

Or use “MAY” for enablement

```md
Image aspect ratio MAY be 1:1
```

means it’s ok for the NFT issuer to set aspect ratio to 1:1.

it would be assumed to be supported by reader of the metadata, such as NFT marketplace, dApps or Wallet.

---

**peersky** (2024-09-10):

I think this standard proposal is over opinionated yet very actual and needed.

industry does need standard way of interfacing and defining URIs, yet these do not need to have any schemas pre-defined, that could be encapsulated in separate, follow-up ERC.

I suggest removing schemas from specification

These are not needed, for example, contract name in EC712 is already defined on blockchain level, hence schema defining `name` field is opinionated and can be implemented as separate standard.

My proposed changes are here: [Update ERC-7572: Remove Schema assumptions, Add updated URI information to the event by peersky · Pull Request #630 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/630)

---

**ryanio** (2024-09-10):

The “name” is provided for this reason described in the ERC:

> If the underlying contract provides any methods that conflict with the contractURI schema such as name() or symbol() , the metadata returned by contractURI() is RECOMMENDED to take precedence. This enables contract creators to update their contract details with an event that notifies of the update.

Also, the reason ContractURIUpdated() doesn’t have parameters is that 1. it is cheaper and 2. it may be outdated from prior events, so the latest value can just be queried from the contract when seeing the event.

I am confused why you feel there is no need for a schemas definition, then how is the contractURI response standardized?

---

**peersky** (2024-09-10):

I suggest standartising the interface of having `contractURI()` available first.  perhaps adding ERC165 as dept.

It can have wide generic use within smart contracts itself (i.e. contracts distribution could collect multiuple URIs and return them as an array etc).

Later, you can always add on top of that extra layer of schemas per specific needs.

Going this path would allow to avoid increasing fragmentation in ethereum standards.

Merging my PR enables to propose it as dependency for [ERC-4824: Common Interfaces for DAOs](https://eips.ethereum.org/EIPS/eip-4824) instead of having them having a separate `daoURI` there which only creates fragmentation as there is no principle difference between a DAO smart contract returning it’s URI and a generic contract returning it’s URI.

Also perhaps it’s worth of adding address for the described contract to the return of `contractURI`, allowing to support their case with registrator

---

**pash7ka** (2025-12-09):

Currently ERC says

> ## Backwards Compatibility
>
>
>
> As a new ERC, no backwards compatibility issues are present.

Since OpenSea uses same function name for their Metadata, i think it would be helpfull to understand if the proposed json is compatible with their requirements.

---

**ryanio** (2025-12-11):

yes it’s compatible / the same

