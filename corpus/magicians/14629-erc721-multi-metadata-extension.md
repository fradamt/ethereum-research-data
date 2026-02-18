---
source: magicians
topic_id: 14629
title: ERC721 Multi-Metadata Extension
author: 0xG
date: "2023-06-09"
category: ERCs
tags: [nft]
url: https://ethereum-magicians.org/t/erc721-multi-metadata-extension/14629
views: 2734
likes: 4
posts_count: 13
---

# ERC721 Multi-Metadata Extension

This EIP proposes an extension to the ERC721 standards to support multiple metadata URIs per token via a new tokenURIs method that returns the pinned metadata index and a list of metadata URIs.

It introduces a new interface, IERC721MultiMetadata, which provides methods for accessing the metadata URIs associated with a token, including a pinned URI index and a list of all metadata URIs. The extension is designed to be backward compatible with existing ERC721Metadata implementations.

## Motivation

The current ERC-721 standard allows for a single metadata URI per token with the ERC721Metadata implementation. However, there are use cases where multiple metadata URIs are desirable. Some example use cases are listed below:

- A token represents a collection of (cycling) assets with individual metadata
- An on-chain history of revisions to token metadata
- Appending metadata with different aspect ratios so that it can be displayed properly on all screens
- Dynamic and evolving metadata
- Collaborative and multi-artist tokens

This extension enables such use cases by introducing the concept of multi-metadata support.

The primary reason for having a multi-metadata standard in addition to the existing ERC721Metadata standard is that dapps and marketplaces don’t have a mechanism to infer and display all the token URIs. Giving a standard way for marketplaces to offer collectors a way to pin/unpin one of the metadata choices also enables quick and easy adoption of this functionality.

For details see https://github.com/ethereum/EIPs/pull/7160/files

## Replies

**mpeyfuss** (2023-07-27):

We’ve officially entered the Draft stage as the EIP has been merged into the EIP repo!

Would appreciate any feedback on the EIP prior to moving to the Review stage. We think this EIP makes a lot of sense, has interesting use cases, and is backwards compatible.

For context, here is the interface and link to the EIP is below.

```auto
/// @title EIP-721 Multi-Metdata Extension
/// @dev The ERC-165 identifier for this interface is 0x06e1bc5b.
interface IERC7160 {

  /// @dev This event emits when a token uri is pinned and is
  ///  useful for indexing purposes.
  event TokenUriPinned(uint256 indexed tokenId, uint256 indexed index);

  /// @dev This event emits when a token uri is unpinned and is
  ///  useful for indexing purposes.
  event TokenUriUnpinned(uint256 indexed tokenId);

  /// @notice Get all token uris associated with a particular token
  /// @dev If a token uri is pinned, the index returned SHOULD be the index in the string array
  /// @dev This call MUST revert if the token does not exist
  /// @param tokenId The identifier for the nft
  /// @return index An unisgned integer that specifies which uri is pinned for a token (or the default uri if unpinned)
  /// @return uris A string array of all uris associated with a token
  /// @return pinned A boolean showing if the token has pinned metadata or not
  function tokenURIs(uint256 tokenId) external view returns (uint256 index, string[] memory uris, bool pinned);

  /// @notice Pin a specific token uri for a particular token
  /// @dev This call MUST revert if the token does not exist
  /// @dev This call MUST emit a `TokenUriPinned` event
  /// @dev This call MAY emit a `MetadataUpdate` event from ERC-4096
  /// @param tokenId The identifier of the nft
  /// @param index The index in the string array returned from the `tokenURIs` function that should be pinned for the token
  function pinTokenURI(uint256 tokenId, uint256 index) external;

  /// @notice Unpin metadata for a particular token
  /// @dev This call MUST revert if the token does not exist
  /// @dev This call MUST emit a `TokenUriUnpinned` event
  /// @dev This call MAY emit a `MetadataUpdate` event from ERC-4096
  /// @dev It is up to the developer to define what this function does and is intentionally left open-ended
  /// @param tokenId The identifier of the nft
  function unpinTokenURI(uint256 tokenId) external;

  /// @notice Check on-chain if a token id has a pinned uri or not
  /// @dev This call MUST revert if the token does not exist
  /// @dev Useful for on-chain mechanics that don't require the tokenURIs themselves
  /// @param tokenId The identifier of the nft
  /// @return pinned A bool specifying if a token has metadata pinned or not
  function hasPinnedTokenURI(uint256 tokenId) external view returns (bool pinned);
}
```

You can find the full EIP [here](https://eips.ethereum.org/EIPS/eip-7160).

---

**Robinnnnn** (2023-07-27):

thank you for putting this together!

question: do you think multimedia assets could be encoded within a single URI? looking at the use cases, it seems like 1) multiple assets to cycle through, 2) revisions, 3) multi-aspect ratios, etc. could follow a new `tokenURI` standard that references a list of objects or a list of URIs. of course this flavor of standardization (and adoption) would be more offchain but remove the need for a new ERC-721 standard.

---

**0xG** (2023-07-28):

Hi [@Robinnnnn](/u/robinnnnn), that’s a good point. Technically an update to the standard that allows nested token uris would work too I guess – you’d have to keep it shallow i.e. allow only one level of nesting. It might work for on-chain metadata as well.

However the pinning story for off-chain metadata might be tricky since I suppose that the pinned index would be another field in the metadata and changing that for off-chain metadata is impossible – the main metadata file would always have to be on-chain. Probably not a big deal.

Thanks a lot for the suggestion – this is the kind of feedback we are looking for. Let’s see what marketplaces think about it.

---

**mpeyfuss** (2023-07-28):

[@Robinnnnn](/u/robinnnnn) thanks for the feedback! To piggyback off [@0xG](/u/0xg), I think the on-chain mechanics are important here. I don’t think off-chain metadata specs are as flexible and are typically not controllable by the collector. Part of this EIP is adding to what on-chain ownership enables.

Also, this EIP does not get rid of the ERC-721 Metadata extension and rather is meant to work side-by-side. So it is a non-breaking extension and doesn’t require marketplaces to make updates, unless they want to enable the functionality for collectors.

Hope that gives you more insight into the thinking behind this! If you have any other thoughts, please don’t hesitate to share!

---

**rickmanelius** (2023-07-28):

## Overall

- I love the spirit of this and think it’s directionally correct/useful.
- NFTs have barely scratch the surface of exploring metadata (we are in the 1995-1999 of HTML)
- This could be one of a handful of ways to solve/empower developers.

## Concerns/Feedback

- We might be hard-pressed to expand on metadata fields variety and standards when we are woefully lacking right now. Some NFTs are still barely 4-5 fields (name, description, image, and attributes).
- Markets / SC templates are missing many of these sane defaults (notably copyright).
- As an earlier commenter Robinnnnn mentioned, this could be resolved by moving the index into the top level tokenURI object. They could be either a flat array OR (better yet) key value pairs.
- Keys/Labels could help add specific functionality (a copyright key, a localization key, etc)
- Example use case. While the EIP touches on changelog, it might be instructive to build out a literal set of examples to showcase and work through this. Such an explicit example might serve as a template/pattern without enforcing it as a “standard”. A benefit might be helping make the call of keys/labels or recognizing they are superfluous.

I shared a bunch of links w/Marco on Twitter. A few that might be meaningful.

- Let’s Talk About a Schema org for NFTs
- Coypright Metadata Structure proposal

---

**mpeyfuss** (2023-07-29):

Hey [@rickmanelius](/u/rickmanelius) thanks for the feedback!

I definitely agree that licensing is a huge issue in the NFT space and adding it to the metadata is at least the first step in the right direction. However, this EIP is not geared towards a new metadata schema standard and is open to all schemas out there at the moment.

We’ve made this open ended on purpose so that people could use it as they want. It’s always fun seeing how people would use something like this. The goal of this proposal is really to extend what is possible with ownership, through code, such as displaying a different aspect ratio piece depending on the frame you have at home.

I’m happy to expand on the examples in the proposal but feel that specifying a new JSON metadata schema is out of the scope of this proposal.

With all that said, I’ve commented on your PR and hope to keep the licensing conversation going over there ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**mpeyfuss** (2023-08-11):

Hello all! We’ve made a few updates to the EIP and I’ve updated my previous message with the new interface. The goal was to simplify and get just the core logic needed to allow for innovation on top of this. Please let us know if you have any other feedback! Otherwise, we plan to put this into the Review stage early next week.

---

**rickmanelius** (2023-08-21):

Hi [@mpeyfuss](/u/mpeyfuss)! Adding clarity to my previous post. Agreed that ERC-7160 should not propose/dictate a schema standard! That’s a heavy lift in itself, and it shouldn’t bog down this EIP.

Rather, I was more interested whether `uris` would return and array vs mapping. If an NFT had >10 entries in this array to meet the use cases you suggested (revisions, media with different aspect ratios, changelogs, etc), it’ll be important to index, sort them.

That said, the counter argument to my approach would be an asset having multiple items of the same type. If an asset had 50 changelog entries, a mapping with a single key would be useless. And it would enforce the changelog to be a single file vs an array of similar files.

So I agree the most flexible approach is to keep it as an array, but my focus for both devs and end-users becomes how to structure the individual changelog entries so we can index by type, sort by blockheight, etc.

---

**ThunderDeliverer** (2023-09-01):

Hi, maybe I’m missing something, but this proposal seems to tackle the same issue as ERC-5773.



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5773)





###



An interface for Multi-Asset tokens with context dependent asset type output controlled by owner's preference.










Could you help me understand how the two compare?

---

**YuriNondual** (2023-09-01):

Hey [@0xG](/u/0xg), it looks like the goal behind this is similar to our ERC-5773



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5773)





###



An interface for Multi-Asset tokens with context dependent asset type output controlled by owner's preference.










You might want to have a look, because we have been building it (together with 4 other complimentary ERCs) for more than 12 month, including real world testing (We have an NFT marketplace that uses this and other of our standards singular.app), and we had plenty of time to think of different edge cases. Let us know if you still think that your one is needed, but otherwise, I don’t think there’s a need to re-invent the wheel ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**0xG** (2023-09-02):

Hey [@YuriNondual](/u/yurinondual) and [@ThunderDeliverer](/u/thunderdeliverer) thanks for chiming in and sharing your work – it seems that  we are fundamentally aiming for a similar functionality.

Here are my two cents about 5773:

1. It is proposing two features that in my opinion should be distinct EIPs (composability ftw):

- Multi-assets
- The propose-accept mechanic

Both [@mpeyfuss](/u/mpeyfuss) and I like the propose-accept mechanic (see https://twitter.com/0x0000G/status/1677374480283492352) but I feel that this is a distinct feature and should be a separate EIP as it could be used for the current ERC721 standard too.

The goal of EIP-7160 is only to provide a way to return multiple URIs in order to support multi-metadata tokens. Propose-accept is out of scope/topic and adds a lot to the API surface.

1. In 5773 you can query the contract to get a list of IDs with getActiveAssets and then you will have to make n RPC calls to get all the URIs. With EIP-7160 you get all the URIs at once, then you can schedule off-chain indexing/caching however you want.

Internal representation of the metadata and how it is stored is not a concern of ours and similarly to ERC721’s tokenURI it is on the developer to come up with those internal details.

---

In short, I like small scoped APIs and that’s why I prefer to solve a single problem with 7160. Getting all the URIs with a single RPC call is something that marketplaces will find it easier to implement.

Regardless of mine or your preference, we share a common “problem” that is with multi-assets/metadata marketplaces will have to switch to a one-to-many model (currently one-to-one) and this is a major challenge.

I talked with an engineer in the protocols team at OpenSea and that was their feedback too. They shared the EIP internally and they want to see use cases in order to get interested (they are open to consider when the EIP gets traction).

---

**sullof** (2024-02-12):

I think the EIP should specify what is supposed to happen when the standard tokenURI is called since it may be:

- the first uri in the uris’ list
- the last in the list
- the pinned one, if any
- some other criteria

Another point is how can I pick one of the uris without knowing what they represents?

Two uris can bring two different aspects of the NFT, let’s say, its collectible data and its properties in a game. It may have sense to think how to give users a criteria for a choice.

If we expect that any NFT in the collections will have 2 uris, like anyone else, i.e., the number of uris is not specific of a specific tokenID, then we can name any position in the uri’s array.

Not sure which can be the best way to set a dictionary, still it would be very helpful.

One way I can think is to define a multi-chain registry of all the supported names, so that the listeners knows what they can expect, and the implementer can pick some from there or suggest new ones. It goes a bit off this EIP but having many uris without having a way to preentively know what they are for is not very helpful.

