---
source: magicians
topic_id: 9077
title: "EIP-5185: NFT Updatable Metadata Extension"
author: Christophe
date: "2022-04-28"
category: EIPs
tags: [nft, erc-721, erc1155, metadata, json]
url: https://ethereum-magicians.org/t/eip-5185-nft-updatable-metadata-extension/9077
views: 4360
likes: 8
posts_count: 15
---

# EIP-5185: NFT Updatable Metadata Extension

---

## eip:
title: NFT Updatable Metadata Extension
description: An interface extension for ERC-721/ERC-1155 controlled metadata updates
author: Christophe Le Bars (@clbrge)
status: Draft
type: Standards Track
category: ERC
requires: 721, 1155

## Abstract

This specification defines a standard way to allow controlled NFTs’ metadata updates along predefined formulas. Updates of the original metadata are restricted and defined by a set of recipes and the sequence and results of these recipes are deterministic and fully verifiable with on-chain metadata updates event. The proposal depends on and extends the EIP-721 and EIP-1155.

## Motivation

Storing voluminous NFT metadata on-chain is often neither practical nor cost-efficient.

Storing NFT metadata off-chain on distributed file systems like IPFS can answer some needs of verifiable correlation and permanence between an NFT tokenId and its metadata but updates come at the cost of being all or nothing (aka changing the `tokenURI`). Bespoke solutions can be easily developed for a specific NFT smart contract but a common specification is necessary for NFT marketplaces and third parties tools to understand and verify these metadata updates.

This ERC allows the original JSON metadata to be modified step by step along a set of predefined JSON transformation formulas. Depending on NFT use-cases, the transformation formulas can be more or less restrictive.

As examples, an NFT representing a house could only allow append-only updates to the list of successive owners, and a game using NFT characters could let some attributes change from time to time (e.g. health, experience, level, etc) while some other would be guaranteed to never change (e.g. physicals traits etc).

This standard extension is compatible with NFTs bridged between Ethereum and L2 networks and allows efficient caching solutions.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY” and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

The **metadata updates extension** is OPTIONAL for EIP-721 and EIP-1155 contracts.

```solidity
/// @title ERC-721/ERC-1155 Updatable Metadata Extension
interface IERC5185UpdatableMetadata {
    /// @notice A distinct Uniform Resource Identifier (URI) for a set of updates
    /// @dev This event emits an URI (defined in RFC 3986) of a set of metadata updates.
    /// The URI should point to a JSON file that conforms to the "NFT Metadata Updates JSON Schema"
    /// Third-party platforms such as NFT marketplace can deterministically calculate the latest
    /// metadata for all tokens using these events by applying them in sequence for each token.
    event MetadataUpdates(string URI);
}
```

The original metadata SHOULD conform to the “ERC-5185 Updatable Metadata JSON Schema” which is a compatible extension of the “ERC-721 Metadata JSON Schema” defined in ERC-721.

“ERC-5185 Updatable Metadata JSON Schema” :

```json
{
    "title": "Asset Updatable Metadata",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Identifies the asset to which this NFT represents"
        },
        "description": {
            "type": "string",
            "description": "Describes the asset to which this NFT represents"
        },
        "image": {
            "type": "string",
            "description": "A URI pointing to a resource with mime type image/* representing the asset to which this NFT represents. Consider making any images at a width between 320 and 1080 pixels and aspect ratio between 1.91:1 and 4:5 inclusive."
        },
        "updatable": {
            "type": "object",
            "required": ["engine", "recipes"],
            "properties": {
                "engine": {
                    "type": "string",
                    "description": "Non ambiguous transformation method/language (with version) to process updates along recipes defined below"
                },
                "schema": {
                    "type": "object",
                    "description": "if present, a JSON Schema that all sequential post transformation updated metadata need to conform. If a transformed JSON does not conform, the update should be considered voided."
                },
                "recipes": {
                    "type": "object",
                    "description": "A catalog of all possibles recipes identified by their keys",
                    "patternProperties": {
                        ".*": {
                            "type": "object",
                            "description": "The key of this object is used to select which recipe to apply for each update",
                            "required": ["eval"],
                            "properties": {
                                "eval": {
                                    "type": "string",
                                    "description": "The evaluation formula to transform the last JSON metadata using the engine above (can take arguments)"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
```

“NFT Metadata Updates JSON Schema” :

```json
{
    "title": "Metadata Updates JSON Schema",
    "type": "object",
    "properties": {
        "updates": {
            "type": "array",
            "description": "A list of updates to apply sequentially to calculate updated metadata",
            "items": { "$ref": "#/$defs/update" },
            "$defs": {
                "update": {
                    "type": "object",
                    "required": ["tokenId", "recipeKey"],
                    "properties": {
                        "tokenId": {
                            "type": "string",
                            "description": "The tokenId for which the update recipe should apply"
                         },
                        "recipeKey": {
                            "type": "string",
                            "description": "recipeKey to use to get the JSON transformation expression in current metadata"
                        },
                        "args": {
                            "type": "string",
                            "description": "arguments to pass to the JSON transformation"
                        }
                    }
                 }
            }
        }
    }
}
```

### Engines

Only one engine is currently defined in this extension proposal.

If the engine in the original metadata is “jsonata@1.8.*”, updated metadata is calculated starting from original metadata and applying each update sequentially (all updates which are present in all the URIs emitted by the event `MetadataUpdates` for which tokenId matches).

For each step, the next metadata is obtained by the javascript calculation (or compatible jsonata implementation in other language) :

```js
const nextMetadata = jsonata(evalString).evaluate(previousMetadata, args)
```

With `evalString` is found with `recipeKey` in the original metadata recipes list.

If the key is not present in the original metadata list, `previousMetadata` is kept as the valid updated metadata.

If the evaluation throws any errors, `previousMetadata` is kept as the valid updated metadata.

If a validation Schema JSON has been defined and the result JSON `nextMetadata` does not conform, that update is not valid and `previousMetadata` is kept as the valid updated metadata.

## Rationale

There have been numerous interesting uses of EIP-721 and EIP-1155 smart contracts that associate for each token essential and significant metadata. While some projects (e.g. EtherOrcs) have experimented successfully to manage these metadata on-chain, that experimental solution will always be limited by the cost and speed of generating and storing JSON on-chain. Symmetrically, while storing the JSON metadata at URI endpoint controlled by traditional servers permit limitless updates the the metadata for each NFT, it is somehow defeating in many uses cases, the whole purpose of using a trustless blockchain to manage NFT: indeed users may want or demand more permanence and immutability from the metadata associated with their NFT.

Most use cases have chosen intermediate solutions like IPFS or arweave to provide some permanence or partial/full immutability of metadata. This is a good solution when an NFT represents a static asset whose characteristics are by nature permanent and immutable (like in the art world) but less so with other use cases like gaming or NFT representing a deed or title. Distinguishable assets in a game often should be allowed to evolve and change over time in a controlled way and titles need to record real life changes.

The advantages of this standard is precisely to allow these types of controlled transformations over time of each NFT metadata by applying sequential transformations starting with the original metadata and using formulas themselves defined in the original metadata.

The original metadata for a given NFT is always defined as the JSON pointed by the result of `tokenURI` for EIP-721 and function `uri` for EIP-1155.

The on-chain log trace of updates guarantee that anyone can recalculate and verify independently the current updated metadata starting from the original metadata. The fact that the calculation is deterministic allows easy caching of intermediate transformations and the efficient processing of new updates using these caches.

The number of updates defined by each event is to be determined by the smart contract logic and use case, but it can easily scale to thousands or millions of updates per event. The function(s) that should emit `MetadataUpdates` and the frequency of these on-chain updates is left at the discretion of this standard implementation.

The proposal is extremely gas efficient, since gas costs are only proportional to the frequency of committing changes. Many changes for many tokens can be batched in one transaction for the cost of only one `emit`.

## Reference Implementation

### Transformation engines

We have been experimenting with this generic Metadata update proposal using the JSONata transformation language.

Here is a very simple example of a NFT metadata for an imaginary ‘little monster’ game :

```json
{
    "name": "Monster 1",
    "description": "Little monsters you can play with.",
    "attributes": [
      { "trait_type": "Level", "value": 0 },
      { "trait_type": "Stamina", "value": 100 }
    ],
    "updatable": {
      "engine": "jsonata@1.8.*",
      "recipes": {
        "levelUp": {
          "eval": "$ ~> | attributes[trait_type='Level'] | {'value': value + 1} |"
        },
        "updateDescription": {
          "eval": "$ ~> | $ | {'description': $newDescription} |"
        }
      }
    }
}
```

This updatable metadata can only be updated to increment by one the trait attribute “Level”.

An example JSON updates metadata would be :

```json
{
    "updates": [
      {"tokenId":"1","action":"levelUp"},
      {"tokenId":"2","action":"levelUp"},
      {"tokenId":"1","action":"updateDescription","args":{"newDescription":"Now I'm a big monster"}},
      {"tokenId":"1","action":"levelUp"},
      {"tokenId":"3","action":"levelUp"}
    ]
}
```

## Security Considerations

A malicious recipe in the original metadata might be constructed as a DDoS vector for third parties marketplaces and tools that calculate NFT updated JSON metadata. They are encouraged to properly encapsulate software in charge of these calculations and put limits for the engine updates processing.

Smart contracts should be careful and conscious of using this extension and still allow the metadata URI to be updated in some contexts (by not having the same URI returned by `tokenURI` or `uri` for a given tokenId over time). They need to take into account if previous changes could have been already broadcasted for that NFT by the contract, if these changes are compatible with the new “original metadata” and what semantic they decide to associate by combining these two kinds of “updates”.

## Backwards Compatibility

The proposal is fully compatible with both EIP-721 and EIP-1155. Third-party applications that don’t support this EIP will still be able to use the original metadata for each NFT.

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## Replies

**BCTSAG** (2022-05-03):

Excellent initiative

---

**Christophe** (2022-06-27):

Draft EIP PR has been opened. The text has been updated to last version.

---

**TimDaub** (2022-07-04):

This seens like a duplicate effort to me as there is one such proposal already in review: [EIP-4906: ERC-721 Metadata Update Extension](https://eips.ethereum.org/EIPS/eip-4906) Or am I missing something. You don’t mention 4906 in your document, so I assume you’re unaware.

---

**Christophe** (2022-07-04):

This new draft is quite different in motivation and principles so it’s not a duplicate. But you are right I should I have mentioned eip 4906 here because of the name conflict. Thanks for bringing that up.

So one problem I see between the 2 proposals is the similar name for their events though we are signaling two very different kinds of “update”.

Other than that the two EIPs be could both agreed and work together since their answer different needs.

I will submit my comments on EIP-4906 in a bit…

---

**mv1986** (2022-07-11):

Hi Christophe,

I am trying get my head around a couple of technical things when it comes to equipping an NFT with either updatable metadata or attachable SBTs. What first comes to my mind is whether there is an important difference for someone who wants to judge the value of an NFT unknown to that person? With “value” I am not only referring to monetary value, but also reputation, credibility, etc., anything that can be captured and described as a category in JSON format.

Isn’t your EIP-5185 essentially what Vitalik describes as SBTs? Or is there a fundamental difference from a user’s / issuer’s / holder’s perspective between updatable meta data extension and the term SBT?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/christophe/48/6498_2.png) Christophe:

> but less so with other use cases like gaming or NFT representing a deed or title. Distinguishable assets in a game often should be allowed to evolve and change over time in a controlled way and titles need to record real life changes.

Let’s assume people sign up on a sports prediction market platform. They can then choose either one competition (basketball) or certain competitions (several sports) and compete with their predictions against others. The platform provides clear rules (which oracle to choose, scoring, prize for 1st, 2nd, 3rd, punishments etc.) upfront. Wouldn’t that be a classical case for your EIP-5185 along with RFC-2119? Is there another standard that you are aware of that would be more or equally appropriate for such a use case? If it turns out that the oracle failed at pulling the correct result for whatever reason, how would a future update then be realized? Could a consensus rule by all participants of a certain competition be tied into the contract in order to overwrite wrongly attached metadata, like agreeing to an alternative URI for a certain object?

Hope my questions make sense here. Just diving into all the token standards that are popping up left, right and center and would like to understand what would be the way to go about for the scenario I described.

All the best,

MV

---

**Christophe** (2022-07-11):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/779978/48.png) mv1986:

> I am trying get my head around a couple of technical things when it comes to equipping an NFT with either updatable metadata or attachable SBTs. What first comes to my mind is whether there is an important difference for someone who wants to judge the value of an NFT unknown to that person? With “value” I am not only referring to monetary value, but also reputation, credibility, etc., anything that can be captured and described as a category in JSON format.

Thanks for these interesting questions and observations. I also believe that we only have started to dig in how much off-chain JSON storage can be useful in many scenarios.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/779978/48.png) mv1986:

> Isn’t your EIP-5185 essentially what Vitalik describes as SBTs? Or is there a fundamental difference from a user’s / issuer’s / holder’s perspective between updatable meta data extension and the term SBT?

EIP-5185 is targeting “classic” NFT not SBT because fundamentally an updatable NFT is not less transferable than an NFT. What the ERC is *only* solving from issuer and holder perspective is the possibility to have a mix of metadata impermanent and permanent.

Now maybe the same principles could be useful for SBT (and it’s not in the current scope of EIP-5185) if you imagine that some updates would only apply to some wallet(s)/soul and/or that a transfer would “reset” or “revert” updates if the token move to a new wallet(s)/soul.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/779978/48.png) mv1986:

> Let’s assume people sign up on a sports prediction market platform. They can then choose either one competition (basketball) or certain competitions (several sports) and compete with their predictions against others. The platform provides clear rules (which oracle to choose, scoring, prize for 1st, 2nd, 3rd, punishments etc.) upfront. Wouldn’t that be a classical case for your EIP-5185 along with RFC-2119? Is there another standard that you are aware of that would be more or equally appropriate for such a use case? If it turns out that the oracle failed at pulling the correct result for whatever reason, how would a future update then be realized? Could a consensus rule by all participants of a certain competition be tied into the contract in order to overwrite wrongly attached metadata, like agreeing to an alternative URI for a certain object?
>
>
> Hope my questions make sense here. Just diving into all the token standards that are popping up left, right and center and would like to understand what would be the way to go about for the scenario I described.

May be a use case but your question is centered on the who/how the update is decided. EIP-5185 is totally neutral on the mechanism to provide the update event so it all depends on who has the right to

do it in the NFT smart contract. In the game example I’m citing in the proposal, it’s probably reserved to the owner of the smart contract (that is to say the game master). A NFT smart contract *could* indeed implement functions where updates are committed only when a consensus is reached by N participants or other consensus for overwriting.

Cheers

---

**sullof** (2022-08-26):

In Mobland/ByteCity we are working on the same problem. We tried initially to define how an NFT can be updated — what you call recipies — and it was not sustainable because there are too many things that you may need to change in a game. We ended up with a different approach, where the type of update is left to the game and the metadata show the history of the change.

Look at this example

```auto
{
   "name": "Monster 1",
   "description": "Little monsters you can play with.",
   "attributes": [
    {
      "trait_type": "Level",
      "value": 2,
      "history": [
        {
          "value": 0,
          "changedAt": 1661553285
        },
        {
          "value": 1,
          "changedAt": 1561855532
        }
      ]
    },
    {
      "trait_type": "Stamina",
      "value": 100
    },
    {
      "trait_type": "Skill",
      "value": 56,
      "history": []
    }
  ]
}
```

There are 3 traits, Level, Skill and Stamina.

Level and Skill are updatable, and Level has actually been updated 2 times.

The advantage here is that it stays compatible with third parties, like OpenSea, while adds all the information needed to know how it changed.

The decision of using the timestamp, instead of the block number (which would be more precise) is for convenience.

---

**Christophe** (2022-11-10):

Sorry for long delay in answering this. Your implementation is interesting but I see 2 problems. First the updates are not trustless (one can verify the history maybe but actual changes AFAIK are full overwrite). Unless server side, it’s costly to overwrite multiple times so many URI.

---

**sullof** (2023-01-07):

You are right about the trust issue and also about the frequency of the updates, but if you are building a game, you must have a way to manage those changes. Putting them in a database, served by a specific API, solves the issue. It is not ideal, I totally agree.

---

**sprice** (2023-05-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/christophe/48/6498_2.png) Christophe:

> This is a good solution when an NFT represents a static asset whose characteristics are by nature permanent and immutable (like in the art world)

Paintings in the world of art are by necessity mutable. They must be or else they would decay and disappear. We trust institutions to periodically restore them.

Here’s the use case I’m exploring

> As the creator of an NFT project, I want to transfer ownership to a trusted multi-sig which will act as the project steward over decades, centuries, and millennia. I understand that numerous things could happen over this time. The metadata files (json, images) may need to be exactly copied to a new location and the baseURI may need to be updated. .png, or .jpeg files may become unusable and the image files may need to be converted and the metadata updated. I want to know that all changes are recorded on-chain and are easy to inspect and verify so that the integrity of the project remains sound.

This EIP solves a number of use cases. Am I correct in understanding it solves the one outlined here or is this for a different EIP to solve?

---

**Christophe** (2023-05-21):

This EIP might indeed cater to your use-cases, but a few conditions should be considered:

The EIP does not explicitly specify the location of the updates URI. This could potentially reside on a server, IPFS, or any other future supported protocols. As a result, both the initial metadata and subsequent updates aren’t strictly on-chain; rather, they may depend on your architectural choices and could reside on semi-permanent storage solutions like IPFS.

If the multi-signature steward has the autonomy to alter any metadata at will, this EIP may not be entirely appropriate. The primary advantage of this EIP lies in its ability to provide distinct update rights per attribute. If this function isn’t necessary in your scenario, then the benefits of this EIP may be significantly diminished.

---

**sprice** (2023-05-22):

A reframe of the problem I’m wanting to solve is this:

> As a collector I want to inspect the metadata of an NFT and see both the canonical URI of the image and a sha256 hash of the image. I can download the image and check that the hash is correct. I can also see that there is a hash of the metadata itself. In the future .png files are not usable and all the files are migrated to a new format. After the update, I can inspect the data within the metadata including the sha256 hash of the new image, I can view information about how the conversion was done. I can use the available information that may be both in the state of the contract or within the off-chain json metadata and I can verify that the update kept the integrity of the nft and no funny business happened.

Will this EIP help me achieve this?

---

**Christophe** (2023-05-25):

Since you don’t know in advance what type of conversion will happen, you could have in metadata something like that

```auto
{
  "name": "Work ABC",
  "description": "a description of work ABC, this will never change.",
  "image": "the last image ipfs uri"
  "attributes": [
   { "trait_type": "hash",   "value": "" }
   { "trait_type": "generationMethod",  "value": "" }
   ],
   "updatable": {
     "engine": "jsonata@1.8.*",
     "recipes": {
       "hash": {
         "eval": "$ ~> | attributes[trait_type='hash'] | {'value': $newhash} |"
       },
       "generationMethod": {
         "eval": "$ ~> | attributes[trait_type='generationMethod'] | {'value': $cmdline} |"
       },
     }
   }
```

You can guarantee then that the only modification to take place are the one for migration. and it’s easy to check that hash are correct…

---

**nickjuntilla** (2024-12-15):

You’ve mentioned ERC-1155 in this but updating the token URI has already been part of ERC-1155

```auto
 /**
        @dev MUST emit when the URI is updated for a token ID.
        URIs are defined in RFC 3986.
        The URI MUST point to a JSON file that conforms to the "ERC-1155 Metadata URI JSON Schema".
    */
    event URI(string _value, uint256 indexed _id);
```

This already seems like an elegant solution and one that most people are using. Trying to pre-define how the data will change seems restrictive to me.

If you are just trying to add functionality to the dated ERC-721 standard then my suggestion would be to simply add the exact same URI event. That seems to be the industry standard. Many people create the URI from on-chain data so even though it says URI often times it is cobbled together from the contract. A one-liner for ERC-721s to add the missing event seems like the most elegant solution to me. Let me know how I’m wrong.

Thanks

EDIT: After reviewing eip-4906 I really like it. It seems to fix exactly what is missing from ERC-721 and only that since ERC-1155 already has this. Anyway just my 2 cents.

