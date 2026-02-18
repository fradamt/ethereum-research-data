---
source: magicians
topic_id: 8588
title: "EIP4906: ERC-721/ERC-1155 Metadata Update Extension"
author: 0xanders
date: "2022-03-13"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip4906-erc-721-erc-1155-metadata-update-extension/8588
views: 4660
likes: 9
posts_count: 10
---

# EIP4906: ERC-721/ERC-1155 Metadata Update Extension

---

## eip: 4906
title: ERC-721/ERC-1155 Metadata Update Extension
description: Standard interface extension for ERC-721/ERC-115 metadata update
author: Anders ()
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2022-03-13
requires: 721 or 1155

## Abstract

This specification defines standard metadata update event of ERC-721and ERC-1155. The proposal depends on and extends the existing ERC-721 and ERC-1155.

## Motivation

Many ERC-721 and ERC-1155 contracts emit their custom event when metadata changed.It is easy to update metadata of one NFT by specific event, but it is difficult for third-party platforms such as NFT marketplace to update metadata of many NFTs based on custom events.

Having a standard `MetadataUpdate` event will make it easy for third-party platforms to timely update metadata of  many NFTs.

## Specification

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

The **metadata update extension** is OPTIONAL for ERC-721/ERC-1155 contracts.

```solidity
/// @title ERC-721/ERC-1155 Metadata Update Extension
interface IERC4906MetadataUpdate  {
    /// @dev This event emits when the metadata of a token is changed.
    /// So that the third-party platforms such as NFT market could
    /// timely update the images and related attributes of the NFT
    event MetadataUpdate(uint256 indexed _tokenId);
}
```

The `MetadataUpdate` event MUST be emitted when the metadata of a token is changed.

## Rationale

Different NFTs have different metadata, and metadata generally has multiple fields. `bytes data` could be used to represents the modified value of metadata.  It is difficult for third-party platforms to identify various types of `bytes data`, so there is only one parameter `uint256 indexed _tokenId` in `MetadataUpdate` event.

After capturing the `MetadataUpdate` event, a third party can update the metadata with information returned from the `tokenURI(uint256 _tokenId)` of ERC721 or `uri(uint256 _tokenId)` of ERC1155.

## Backwards Compatibility

No issues.

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## Replies

**pizzarob** (2022-03-19):

Hi. I think this makes a lot of sense. I would however suggest that the event accept a range of consecutive token IDs. See ERC2309. My rationale is that you can tell a platform to update and entire collection of metadata using one event rather than one at a time. Emitting a single event for a collection of 10,000 NFTs is not financially reasonable.

---

**aram** (2022-03-19):

I agree with this. There must be a way to signal that a range or whole collection is updated.

---

**niftynathangang** (2022-06-01):

I would like to propose the following two updates:

1. Make the token id a range of consecutive ids, as already suggested in this thread.
2. Many dynamic NFTs are time-based, so a way to instruct a marketplace whether or not to repeat the metadata query and the repeating details would be handy.

```auto
event MetadataUpdate(uint256 beginTokenId, uint256 endTokenId, uint256 repeatInterval)
```

For updates of a single token id, set beginTokenId and endTokenId to the same value.

A repeat interval of 0 means ‘do not repeat, this is a one-time update only’.  Otherwise, the repeat interval would be specified in seconds.

Additionally, is there any reason to limit this to ERC-721 tokens?  I feel like this can be applicable to ERC-1155 tokens as well.

Thoughts?

---

**niftynathangang** (2022-06-01):

Draft PR for review, if you think these suggestions are reasonable.

https://github.com/ethereum/EIPs/pull/5125

---

**Christophe** (2022-07-04):

I’m the author of another draft EIP that is also about metadata “updates” but with different scope & motivation. Check [EIP-5185: NFT Updatable Metadata Extension](https://eips.ethereum.org/EIPS/eip-5185)

EIP4906 proposal makes senses to help 3rd parties keep track of metadata URI, maybe the events should be named  `MetadataURIUpdate` and `BatchMetadataURIUpdate` to better differentiate with updates taking place inside the metadata themselves such as eip-5185 is about.

---

**0xG** (2022-07-19):

How about

```auto
interface IERCMetadataUpdate {
  event MetadataUpdate(uint256[] tokenIds);
  event MetadataUpdateRange(uint256 start, uint256 end);
}
```

would work with both ERC721 and 1155.

Passing an empty array could mean update all. Alternatively another method could be used to define ranges.

---

**sullof** (2022-08-26):

[@0xanders](/u/0xanders) Sorry, I just realized that you talk about general updates.

We need more something like [@Christophe](/u/christophe) proposal.

I will delete my comments, to avoid generating confusion. But, I agree with Christophe that `MetadataURIUpdate` would be definitely better.

---

**PaulRBerg** (2023-05-26):

Hey! I was reading the ERC and got confused by this:

> Not emitting MetadataUpdate event is RECOMMENDED when the tokenURI changes but the JSON metadata does not.

Could you guys provide an example for when the `tokenURI` changes but not the JSON metadata?

I thought that it is impossible to change the `tokenURI` without altering the metadata.

---

**sullof** (2023-05-26):

You may put your JSON files on S3 and later create a CloudFront distribution and associate it to your own domain. In this case the metadata are not changing, just the tokenURI.

