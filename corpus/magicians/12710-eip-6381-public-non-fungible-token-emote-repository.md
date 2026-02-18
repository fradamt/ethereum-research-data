---
source: magicians
topic_id: 12710
title: "EIP-6381: Public Non-Fungible Token Emote Repository"
author: ThunderDeliverer
date: "2023-01-26"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-6381-public-non-fungible-token-emote-repository/12710
views: 3507
likes: 20
posts_count: 32
---

# EIP-6381: Public Non-Fungible Token Emote Repository

---

## eip: 6381
title: Public Non-Fungible Token Emote Repository
description: React to any Non-Fungible Tokens using Unicode emojis.
author: , , ,
discussions-to:
status: Last Call
last-call-deadline: 2023-05-02
type: Standards Track
category: ERC
created: 2023-01-22
requires: 165

## Abstract

The Public Non-Fungible Token Emote Repository standard provides an enhanced interactive utility for [ERC-721](https://eips.ethereum.org/EIPS/eip-721) and [ERC-1155](https://eips.ethereum.org/EIPS/eip-1155) by allowing NFTs to be emoted at.

This proposal introduces the ability to react to NFTs using Unicode standardized emoji in a public non-gated repository smart contract that is accessible at the same address in all of the networks.

## Motivation

With NFTs being a widespread form of tokens in the Ethereum ecosystem and being used for a variety of use cases, it is time to standardize additional utility for them. Having the ability for anyone to interact with an NFT introduces an interactive aspect to owning an NFT and unlocks feedback-based NFT mechanics.

This ERC introduces new utilities for [ERC-721](https://eips.ethereum.org/EIPS/eip-721) based tokens in the following areas:

- Interactivity
- Feedback based evolution
- Valuation

### Interactivity

The ability to emote on an NFT introduces the aspect of interactivity to owning an NFT. This can either reflect the admiration for the emoter (person emoting to an NFT) or can be a result of a certain action performed by the token’s owner. Accumulating emotes on a token can increase its uniqueness and/or value.

### Feedback based evolution

Standardized on-chain reactions to NFTs allow for feedback based evolution.

Current solutions are either proprietary or off-chain and therefore subject to manipulation and distrust. Having the ability to track the interaction on-chain allows for trust and objective evaluation of a given token. Designing the tokens to evolve when certain emote thresholds are met incentivizes interaction with the token collection.

### Valuation

Current NFT market heavily relies on previous values the token has been sold for, the lowest price of the listed token and the scarcity data provided by the marketplace. There is no real time indication of admiration or desirability of a specific token. Having the ability for users to emote to the tokens adds the possibility of potential buyers and sellers gauging the value of the token based on the impressions the token has collected.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

```solidity
/// @title ERC-6381 Emotable Extension for Non-Fungible Tokens
/// @dev See https://eips.ethereum.org/EIPS/eip-6381
/// @dev Note: the ERC-165 identifier for this interface is 0x08eb97a6.

pragma solidity ^0.8.16;

interface IERC6381 /*is IERC165*/ {
    /**
     * @notice Used to notify listeners that the token with the specified ID has been emoted to or that the reaction has been revoked.
     * @dev The event MUST only be emitted if the state of the emote is changed.
     * @param emoter Address of the account that emoted or revoked the reaction to the token
     * @param collection Address of the collection smart contract containing the token being emoted to or having the reaction revoked
     * @param tokenId ID of the token
     * @param emoji Unicode identifier of the emoji
     * @param on Boolean value signifying whether the token was emoted to (`true`) or if the reaction has been revoked (`false`)
     */
    event Emoted(
        address indexed emoter,
        address indexed collection,
        uint256 indexed tokenId,
        bytes4 emoji,
        bool on
    );

    /**
     * @notice Used to get the number of emotes for a specific emoji on a token.
     * @param collection Address of the collection containing the token being checked for emoji count
     * @param tokenId ID of the token to check for emoji count
     * @param emoji Unicode identifier of the emoji
     * @return Number of emotes with the emoji on the token
     */
    function emoteCountOf(
        address collection,
        uint256 tokenId,
        bytes4 emoji
    ) external view returns (uint256);

    /**
     * @notice Used to get the information on whether the specified address has used a specific emoji on a specific
     *  token.
     * @param emoter Address of the account we are checking for a reaction to a token
     * @param collection Address of the collection smart contract containing the token being checked for emoji reaction
     * @param tokenId ID of the token being checked for emoji reaction
     * @param emoji The ASCII emoji code being checked for reaction
     * @return A boolean value indicating whether the `emoter` has used the `emoji` on the token (`true`) or not
     *  (`false`)
     */
    function hasEmoterUsedEmote(
        address emoter,
        address collection,
        uint256 tokenId,
        bytes4 emoji
    ) external view returns (bool);

    /**
     * @notice Used to emote or undo an emote on a token.
     * @dev Does nothing if attempting to set a pre-existent state.
     * @dev MUST emit the `Emoted` event is the state of the emote is changed.
     * @param collection Address of the collection containing the token being checked for emoji count
     * @param tokenId ID of the token being emoted
     * @param emoji Unicode identifier of the emoji
     * @param state Boolean value signifying whether to emote (`true`) or undo (`false`) emote
     */
    function emote(
        address collection,
        uint256 tokenId,
        bytes4 emoji,
        bool state
    ) external;
}
```

### Pre-determined address of the Emotable repository

The address of the Emotable repository smart contract is designed to resemble the function it serves. It starts with `0x311073` which is the abstract representation of `EMOTE`. The address is:

```auto
0x311073569e12f7770719497cd3b3aa2db0a0c3d9
```

## Rationale

Designing the proposal, we considered the following questions:

1. Does the proposal support custom emotes or only the Unicode specified ones?
The proposal only accepts the Unicode identifier which is a bytes4 value. This means that while we encourage implementers to add the reactions using standardized emojis, the values not covered by the Unicode standard can be used for custom emotes. The only drawback being that the interface displaying the reactions will have to know what kind of image to render and such additions will probably be limited to the interface or marketplace in which they were made.
2. Should the proposal use emojis to relay the impressions of NFTs or some other method?
The impressions could have been done using user-supplied strings or numeric values, yet we decided to use emojis since they are a well established mean of relaying impressions and emotions.
3. Should the proposal establish an emotable extension or a common-good repository?
Initially we set out to create an emotable extension to be used with any ERC-721 compilant tokens. However, we realized that the proposal would be more useful if it was a common-good repository of emotable tokens. This way, the tokens that can be reacted to are not only the new ones but also the old ones that have been around since before the proposal.
In line with this decision, we decided to calculate a deterministic address for the repository smart contract. This way, the repository can be used by any NFT collection without the need to search for the address on the given chain.

## Backwards Compatibility

The Emote repository standard is fully compatible with [ERC-721](https://eips.ethereum.org/EIPS/eip-721) and with the robust tooling available for implementations of ERC-721 as well as with the existing ERC-721 infrastructure.

## Test Cases

Tests are included in [emotableRepository.ts](https://github.com/ethereum/EIPs/tree/master/assets/eip-6381/test/emotableRepository.ts).

To run them in terminal, you can use the following commands:

```auto
cd ../assets/eip-6381
npm install
npx hardhat test
```

## Reference Implementation

See [EmotableRepository.sol](https://github.com/ethereum/EIPs/tree/master/assets/eip-6381/contracts/EmotableRepository.sol).

## Security Considerations

The same security considerations as with [ERC-721](https://eips.ethereum.org/EIPS/eip-721) apply: hidden logic may be present in any of the functions, including burn, add asset, accept asset, and more.

Caution is advised when dealing with non-audited contracts.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**toledoroy** (2023-01-30):

What do you think about maybe holding arbitrary data about token on a separate contract?

Just a simple contract that holds mapping, e.g.  [account][contract][tokenId]=>emoji

I think that since smart contracts are supposed to function like micro services, it might make more sense to create a contract as a public service for that.

This could potentially allow you to add emojis or any other arbitrary data about any NFT, even for  immutable contracts that were already deployed.

---

**stoicdev0** (2023-01-30):

Hey [@toledoroy](/u/toledoroy), thanks for participating!

Internally, we actually created 2 versions, an extension (the one we’re presenting) and a stand alone which can track emojis for any contract.

We don’t see it as valuable to create an EIP for the second case, since you don’t really need an interface, ideally you would need a single contract deployed which tracks them all. Hard to achieve.

---

**SamWilsn** (2023-02-15):

Apologies if I’ve mentioned this before, but what if you track reactions as [ERC-5114](https://eips.ethereum.org/EIPS/eip-5114) badges? Note that these soulbound badges aren’t removable, which would be different from your current proposal.

---

**stoicdev0** (2023-02-20):

That’s just too different honestly. Besides not being removable, you may have thousands of reactions using the same emoji on a token, which can be tracked by a simple counter in this proposal. With the badges approach it would be too expensive to do this.

---

**SamWilsn** (2023-02-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> Besides not being removable

What if I suggest allowing burning badges to [@MicahZoltu](/u/micahzoltu)? It’s a small amount of mutability, in exchange for use cases like these.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> can be tracked by a simple counter in this proposal.

If the emoji are tracked as a simple counter, how do you control who can remove one? Couldn’t anyone remove the reaction I added?

---

**ThunderDeliverer** (2023-02-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> If the emoji are tracked as a simple counter, how do you control who can remove one? Couldn’t anyone remove the reaction I added?

We use two simple mappings to track the emotes given by the address and the number of emotes the token has received: [EIPs/assets/eip-6381/contracts/Emotable.sol at 2bdcdb61baf8ba6210096c06f0e265d8622d4d7f · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/blob/2bdcdb61baf8ba6210096c06f0e265d8622d4d7f/assets/eip-6381/contracts/Emotable.sol#L8)

This ensures that the emoter can emote and undo emote and that the change is reflected on the token.

---

**SamWilsn** (2023-02-21):

That seems roughly equivalent to what you’d need to do to keep track of badges. You could use `keccak256(abi.encode(msg.sender, tokenId, emoji))` as the badge’s `tokenId`.

---

**SamWilsn** (2023-02-21):

Here’s an untested implementation:

```plaintext
// SPDX-License-Identifier: CC0-1.0

pragma solidity ^0.8.17;

interface IERC5114 {
	event Mint(uint256 indexed badgeId, address indexed nftAddress, uint256 indexed nftTokenId);

	function ownerOf(uint256 badgeId) external view returns (address nftAddress, uint256 nftTokenId);

	function collectionUri() external pure returns (string memory collectionUri);

	function badgeUri(uint256 badgeId) external view returns (string memory badgeUri);

	function metadataFormat() external pure returns (string memory format);
}

contract Reactions is IERC5114 {
    event Reacted(
        address indexed emoter,
        address indexed nftAddress,
        uint256 indexed nftTokenId,
        bytes4 emoji,
        bool enabled
    );

    struct Reaction {
        address operator;
        address nftAddress;
        uint256 nftTokenId;
        bytes4 codepoint;
        bool enabled;
    }

    mapping (uint256 => Reaction) private _reactions;

    //      (nftAddress =>         (nftTokenId =>        (codepoint => count  )))
    mapping (address    => mapping (uint256    => mapping(bytes4    => uint256))) private _counts;

    /*
     * IERC5114 Implementation
     */
    string constant public metadataFormat = "TODO";
    string constant public collectionUri = "TODO";

    function ownerOf(uint256 badgeId) external view returns (address nftAddress, uint256 nftTokenId) {
        Reaction storage reaction = _reactions[badgeId];
        require(address(0) != reaction.operator);
        return (reaction.nftAddress, reaction.nftTokenId);
    }

    function badgeUri(uint256 badgeId) external view returns (string memory) {
        require(address(0) != _reactions[badgeId].operator);
        return "TODO";
    }

    /*
     * IToggleable Implementation
     */
    function isEnabled(uint256 badgeId) external view returns (bool) {
        Reaction storage reaction = _reactions[badgeId];
        require(address(0) != reaction.operator);
        return reaction.enabled;
    }

    /*
     * Reactions Implementation
     */

    function id(
        address operator,
        address nftAddress,
        uint256 nftTokenId,
        bytes4 codepoint
    ) public pure returns (uint256) {
        return uint256(keccak256(abi.encode(operator, nftAddress, nftTokenId, codepoint)));
    }

    function react(
        address nftAddress,
        uint256 nftTokenId,
        bytes4 codepoint,
        bool enabled
    ) external returns (uint256) {
        uint256 badgeId = id(msg.sender, nftAddress, nftTokenId, codepoint);
        Reaction storage reaction = _reactions[badgeId];

        if (reaction.enabled == enabled) {
            return badgeId;
        }

        if (address(0) == reaction.operator) {
            reaction.operator = msg.sender;
            reaction.nftAddress = nftAddress;
            reaction.nftTokenId = nftTokenId;
            reaction.codepoint = codepoint;

            emit Mint(badgeId, nftAddress, nftTokenId);
        }

        if (enabled) {
            _counts[nftAddress][nftTokenId][codepoint] += 1;
        } else {
            _counts[nftAddress][nftTokenId][codepoint] -= 1;
        }

        reaction.enabled = enabled;
        emit Reacted(
            msg.sender,
            nftAddress,
            nftTokenId,
            codepoint,
            enabled
        );

        return badgeId;
    }

    function reactionCountOf(
        address nftAddress,
        uint256 nftTokenId,
        bytes4 codepoint
    ) public view returns (uint256) {
        return _counts[nftAddress][nftTokenId][codepoint];
    }
}
```

---

**MicahZoltu** (2023-02-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> What if I suggest allowing burning badges to @MicahZoltu? It’s a small amount of mutability, in exchange for use cases like these.

Any mutability (including burning) makes it so you can not aggressively cache badges, which was a design goal of 5114.  That being said, one could create another EIP for mutable badges where the owner can burn them.  This EIP could share essentially the same interface as 5114, so anyone supporting one would likely support the other as well.  I think there is value in calling those two types of badges different things however, which is why I think they should be different EIPs (with different numbers and titles).

---

**stoicdev0** (2023-02-21):

There are so many differences:

1. They are meant to be non removable, confirmed by the author.
2. Badges are sent to any contract, which can be a nice feature, but our proposal is meant to be an extension, so badges are tracked within the contract itself.
3. We don’t need collectionUri nor metadataFormat. For badgeUri we could force it to return the id of the emoji I guess, but it feels really hacky IMO.
4. There’s no way to get the count of reactions for a specific emoji on a token. It is reasonable in general since an indexer could take care of this. But it is important on our EIP since we intend implementations to vary the behavior based on this. e.g:

- An NFT of a plant returns a dying plant image unless it has a certain number of  reactions. This plays really well with ERC-5773.
- An NFT of a person returns a blushed version after it gets 100  emojis. Goes also well with 5773.
- An NFT can be transferable only after receiving 10  reactions, playing nice with ERC-6454

Finally, when building extensions of `ERC721`, we’ve found contract size to be a huge limitation. You hit the 24kb limit easily when you stack many together. So we try to keep them as minimal as possible. I understand your purpose with this and it’s really valuable, but in this case forcing it into use a somehow related one would be harmful for us.

---

**SamWilsn** (2023-02-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> They are meant to be non removable, confirmed by the author.

Very true. The [example](https://ethereum-magicians.org/t/eip-6381-emotable-extension-for-non-fungible-tokens/12710/9) I posted uses non-removable badges. I’d be very open to making a burnable badge standard if necessary.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> Badges are sent to any contract, which can be a nice feature, but our proposal is meant to be an extension, so badges are tracked within the contract itself.

What benefits come with putting the reactions in the same contract?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> We don’t need collectionUri nor metadataFormat. For badgeUri we could force it to return the id of the emoji I guess, but it feels really hacky IMO.

Assuming someone made a generic badge viewing dapp, or wallets build in native support for badges, then the reactions/emoji badges would just show up (and `collectionUri` could have a nice description of what a reaction is for.) `metadataFormat` is just an implementation detail.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> There’s no way to get the count of reactions for a specific emoji on a token.

See `reactionCountOf` from my earlier example.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> An NFT of a plant returns a dying plant image unless it has a certain number of  reactions. This plays really well with ERC-5773.
> An NFT of a person returns a blushed version after it gets 100  emojis. Goes also well with 5773.

Ha, I love it! That’ll be quite fun. I think you could still implement this by querying the badge contract in your `tokenURI`?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> Finally, when building extensions of ERC721, we’ve found contract size to be a huge limitation.

Isn’t this a great argument against your point 2? If the reactions/emoji live in their own contract, there’s no code size increase to the ERC-721 contract.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> I understand your purpose with this and it’s really valuable, but in this case forcing it into use a somehow related one would be harmful for us.

It seems like such a close fit to me, but it’s totally fine if you don’t agree!

---

**stoicdev0** (2023-02-21):

Thanks again, I really enjoy this discussions ![:grin:](https://ethereum-magicians.org/images/emoji/twitter/grin.png?v=12)

> What benefits come with putting the reactions in the same contract?

I don’t have to keep track of an external contract where emojis would be stored. My main problem with tracking them in an external contract is that there could actually be many! Each marketplace might have their own for instance, so I’d have to either choose or aggregate, which feels less usable.

> Assuming someone made a generic badge viewing dapp, or wallets build in native support for badges, then the reactions/emoji badges would just show up (and collectionUri could have a nice description of what a reaction is for.) metadataFormat is just an implementation detail.

It still feels forced and extra unneeded effort IMO. Emojis are powerful, widely used and can be achieved with as little as what we’re proposing.

> See reactionCountOf from my earlier example.

The thing is, that’s not part of the 5114’s interface, and we do need it to be there if we want to use it as intended.  It would be a show stopper.

> Isn’t this a great argument against your point 2? If the reactions/emoji live in their own contract, there’s no code size increase to the ERC-721 contract.

It is ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12) I realized as I was writing it. But weighing pros and cons we find local storage better for this use case, mostly for the reason pointed in the answer about benefits.

---

**SamWilsn** (2023-02-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> I don’t have to keep track of an external contract where emojis would be stored. My main problem with tracking them in an external contract is that there could actually be many! Each marketplace might have their own for instance, so I’d have to either choose or aggregate, which feels less usable.

That’s a great point ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12) What if the standard includes [the deployment transaction](https://yamenmerhi.medium.com/nicks-method-ethereum-keyless-execution-168a6659479c) so there can be exactly one emoji contract at a well-known address?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> SamWilsn:
>
>
> See reactionCountOf from my earlier example.

The thing is, that’s not part of the 5114’s interface, and we do need it to be there if we want to use it as intended. It would be a show stopper.

For sure! I’m more suggesting we define `IEmotable` as:

```solidity
interface IEmotable is IERC5114 { ... }
```

Or in other words, add whatever extra methods/events you need on top of `IERC5114`.

---

**MicahZoltu** (2023-02-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> That’s a great point  What if the standard includes the deployment transaction  so there can be exactly one emoji contract at a well-known address?

I would use something like [GitHub - Zoltu/deterministic-deployment-proxy: An Ethereum proxy contract that can be used for deploying contracts to a deterministic address on any chain.](https://github.com/Zoltu/deterministic-deployment-proxy) personally, which is a simplification around keyless execution.  I agree with this general idea though.  Have a single “reaction registry” (this would be standardized) that allows anyone to react to any token (5114 or 721 or other, anything with the form `(address, id)`).  This means you don’t need to build tokens with support for reactions built-in, it can be added on to any existing token.  For example, people could react to CryptoKitties or Bored Apes once the standard is finished.

---

**stoicdev0** (2023-02-22):

We will review your suggestions [@SamWilsn](/u/samwilsn) and [@MicahZoltu](/u/micahzoltu), they look promising.

Thanks!

---

**stoicdev0** (2023-02-27):

We decided to switch for the recommended approach of a single contract with a predictable address across all chains. ![:partying_face:](https://ethereum-magicians.org/images/emoji/twitter/partying_face.png?v=12)  but not reusing 5114. We’ll need a few days to adapt, will keep you posted.

Thanks!

---

**ThunderDeliverer** (2023-04-04):

Thank you once again for the constructive comments [@SamWilsn](/u/samwilsn) and [@MicahZoltu](/u/micahzoltu)!

We have now published the updated version of the EIP that aims to standardise a [Public Non-Fungible Token Emote Repository](https://eips.ethereum.org/EIPS/eip-6381) that is deployed to a pre-determined address (while the updated proposal is already published, we are still calculating the desired address, so I’ll post it here as soon as we have it along with the list of test networks we deployed the repository to).

---

**SamWilsn** (2023-04-04):

Couple further questions:

- It’ll be expensive to emote on mainnet. Is there any way we can emote on a cheaper chain for an NFT on mainnet? Is that even worthwhile?
- How does this handle emoji built from several codepoints, like ? That one is at least two pieces ( and 🏿.)

I think it’s looking great so far!

---

**ThunderDeliverer** (2023-04-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> It’ll be expensive to emote on mainnet. Is there any way we can emote on a cheaper chain for an NFT on mainnet? Is that even worthwhile?

It isn’t that expensive (and any reaction that is not the first reaction with a given emoji costs less than the first one), but we designed the repository in a way that it can be deployed to any EVM compatible chain at the same address.

I just ran the gas profiler and these are the results:

```auto
·------------------------------------------------------------------------------------|---------------------------|-------------|-----------------------------·
|                                Solc version: 0.8.18                                ·  Optimizer enabled: true  ·  Runs: 200  ·  Block limit: 30000000 gas  │
·····················································································|···························|·············|······························
|  Methods                                                                           ·               50 gwei/gas               ·       1865.56 usd/eth       │
················································|····································|·············|·············|·············|···············|··············
|  Contract                                     ·  Method                            ·  Min        ·  Max        ·  Avg        ·  # calls      ·  usd (avg)  │
················································|····································|·············|·············|·············|···············|··············
|  RMRKEmoteTrackerMock                         ·  emote                             ·      24874  ·      70211  ·      57994  ·           17  ·       5.41  │
················································|····································|·············|·············|·············|···············|··············
```

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> How does this handle emoji built from several codepoints, like ? That one is at least two pieces ( and 🏿.)

It doesn’t intend to. There could be an extension to support it, but currently only the base emojis are supported. We see this as beneficial if you are using the emotes to drive the evolution of the token. Having to only process one emoji (thumbs up) and not 5 emojis (variations of thumbs up) maintains the simplicity of using the repository.

---

**ThunderDeliverer** (2023-04-07):

We are happy to announce that the initial implementation of the Emote Repository is now live on Görli, Sepolia, Mumbai and MoonbaseAlpha test networks @ **0x311073569e12F7770719497CD3B3Aa2dB0a0C3D9**.


*(11 more replies not shown)*
