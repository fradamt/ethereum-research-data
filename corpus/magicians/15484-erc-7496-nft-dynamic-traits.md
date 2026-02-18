---
source: magicians
topic_id: 15484
title: "ERC-7496: NFT Dynamic Traits"
author: ryanio
date: "2023-08-18"
category: ERCs
tags: [erc, nft]
url: https://ethereum-magicians.org/t/erc-7496-nft-dynamic-traits/15484
views: 4627
likes: 18
posts_count: 26
---

# ERC-7496: NFT Dynamic Traits

Discussion thread for [ERC-7496: NFT Dynamic Traits](https://eips.ethereum.org/EIPS/eip-7496).

> This specification introduces a new interface that extends ERC-721 and ERC-1155 that defines methods for setting and getting dynamic onchain traits associated with non-fungible tokens. These dynamic traits can be used to represent properties, characteristics, redeemable entitlements, or other attributes that can change over time. By defining these traits onchain, they can be used and modified by other onchain contracts.

## Replies

**fedepo** (2023-08-19):

This is extremely interesting and a much needed upgrade to the existing metadata model!

If I understand correctly this would applies to traits *only*. One possible expansion would be to allow the smartcontract to also generate `name`, `image`, `description`, `animation_url` and `external_url`. These fields are typically present in the metadata of NFTs and some projects would benefit a lot from generate them directly on-chain. (still mixing them with less “delicate” traits that could still be served from off-chain through the old school metadata uri).

As an example, at [Fabrica](https://www.fabrica.land) our NFTs point to a metadata that is dynamically generated on our servers ([example](https://metadata.fabrica.land/ethereum/0x5cbeb7a0df7ed85d82a472fd56d81ed550f3ea95/3775392155688387140)). This is flexible but highly centralized, and some of the data we (will) include in the metadata is actually available on chain, so it should be served directly from there in a non decentralized fashion. Another good example is ENS.

---

**ryanio** (2023-08-19):

Thanks that’s great to hear!

This standard is general enough that it could be used like that, returning information at keys like `bytes32("name")`, `bytes32("description")`. We could think about defining a basic set in this ERC under a nesting like `metadata.name`, `metadata.description`, or create a separate EIP that requires this one that focuses on defining them (can require that anything under `metadata` is used as a top level metadata key and display type should be hidden). There is a strong focus on “traits” because they can influence the NFT’s value and specific ones may have to be checked during order fulfillment.

---

**Mouradif** (2023-08-20):

Nice! This is going to prove essential for creating a Zone to validate trait-based offers on SeaPort.

---

**ryanio** (2023-08-21):

Yes! We have started defining a spec for that [here](https://github.com/ProjectOpenSea/SIPs/blob/main/SIPS/sip-15.md).

---

**wwhchung** (2023-09-06):

Question:

Couldn’t we accomplish the same by using existing EIP for token metadata update (ERC-4906) on the metadata side?

Example pseudo code:

`

contract MyERC721 is ERC721 {

…

mapping(uint256 => boolean) redemptionMap;

function tokenURI(uint tokenId) {

return string(abi.encodePacked(‘data:application/json;utf8,{“name”:“Token”,“attributes”:[{“trait_type”:“Redeemed”,“value”:"’, boolToString(redemptionMap[tokenId]),'"}]));

}

function redeem(tokenId) {

… check ownership

require(redemptionMap[tokenId] == false);

redemptionMap[tokenId] = true;

}

}

`

Granted, I can see the value of retrieving trains on chain for secondary enforcement.

However, if that were the goal, I would propose an EIP that also addresses general NFT modifiability so it can handle other aspects as well.

So, for example, an EIP that allows for the identification of a ‘lastModifyDate’ instead.

---

**wwhchung** (2023-09-06):

Note that I bring up secondary enforcement as a secondary aspect because you’re going to run into similar issues for any modifiable NFT or any NFT’s that also have ownership rights attached (e.g. EIP6551)

---

**nickjuntilla** (2023-09-09):

Does this seem over-engineered to anyone else?

Are all of these getters required?

```auto
    /* Getters */
    function getTraitValue(bytes32 traitKey, uint256 tokenId) external view returns (bytes32);
    function getTraitValues(bytes32 traitKey, uint256[] calldata tokenIds) external view returns (bytes32[] memory);
    function getTraitKeys() external view returns (bytes32[] memory);
    function getTotalTraitKeys() external view returns (uint256);
    function getTraitKeyAt(uint256 index) external view returns (bytes32);
    function getTraitLabelsURI() external view returns (string memory);
```

This seems like a prohibitive amount of code to add for something that (could) ony be only one key and value.

Also why do we have trait keys, full trait keys, and trait labels? Are these all not the same thing? Then the trait keys are indexed so they have yet another way to call them. Why are there so many ways to address the trait names? This seems every confusing.

And then what is a trait URI? Is this meant to just describe the label again? If this is meant to store offchain data about keys, why is this necessary if the point of this to store data onchain?

My main criticism is why are there so many ways to tell us how the how to translate trait names into human readable form? Is that not the least most important thing? Isn’t what matters, just that there is in fact a unique key for each trait (which is accomplished by having an index in the trait key array) and then if we have any kind of human readable label the contract operator should be able to easily find a unique human readable label within bytes32 that should be a sufficient enough clue to properly label the key in a user interface.

Thanks for helping me to understand.

---

**ryanio** (2023-09-11):

[@wwhchung](/u/wwhchung) tokenURI is not guaranteed to be readable onchain, this EIP focuses on providing certain metadata traits onchain so contracts that need to verify the trait values (marketplaces, redemption contracts, onchain games, etc.) can query, use, and update them in a predictable manner.

---

**ryanio** (2023-09-11):

[@nickjuntilla](/u/nickjuntilla) yes the interface is quite broad and am open to suggestions to keep it as narrow as possible. I can explain the purpose of each of the methods:

- getTraitValue - for querying one trait at a time
- getTraitValues - for querying traits for multiple tokenIds at a time
- getTraitKeys - to identify all the trait keys available for the contract
- getTotalTraitKeys - in case there are more keys than what getTraitKeys can return in memory, you can use this to get all the trait keys with getTraitKeyAt
- getTraitKeyAt - see above
- getTraitLabelsURI - because we store trait keys as bytes32 for gas efficiency, this is provided to support longer trait labels than 32 ascii chars, as well as complex metadata use cases (see the trait labels spec in the document for what can be specified)

so yes it is a lot together, i would like to have fewer, but also want to make sure we can support as much discoverability as possible for trait keys/values for onchain contracts.

---

**wwhchung** (2023-09-11):

That’s what I was alluding to (ie the benefit would be on chain checking).

I still think there are immense benefits decoupling this from the nft itself (ie not on the same contract).

---

**ryanio** (2023-09-11):

[@wwhchung](/u/wwhchung) I just left a reply here on our approach here: [ERC-7498: NFT Redeemables - #8 by ryanio](https://ethereum-magicians.org/t/erc-7498-nft-redeemables/15485/8) ideally we don’t want an NFT contract, a dynamic traits contract, and a redeemable contract PER NFT contract as accessing 3 contracts would be very expensive for one operation, so we designed a registry that can be used with all these features together for already-deployed NFTs OR devs can build these features into the token contract itself.

---

**nickjuntilla** (2023-09-13):

The spec says:

“Contracts implementing this EIP MUST include the events, getters, and setters as defined below”

I think getTraitLabelsURI should be optional. OpenSea was originally and still able to infer trait value types by the values that exist. I think it’s also reasonable for a platform to infer use the labels if the TraitKey is English. If the contract author knows they are using a hash for the key then they can provide the label URI. This means less work for the most common use case which is just having short label names and a few simple values. Why make everyone do more work (and deploy more code) for the less common use case? I think we should strive to make sure only what is necessary is on chain and make offchain do more work. The values and distinguishing labels are onchain and that’s what matters right.

Providing the trait labels json also may make this more brittle. If for instance you want to add a trait, which I don’t see a method for that here then you would also have to update your trait label URI. People may want to add traits.

What event is triggered if someone wants to add a trait? Is there then an event for updating the trait URI?

By the way I am all for this and think it is sorely needed.

---

**ryanio** (2023-09-13):

[@nickjuntilla](/u/nickjuntilla) Thanks for your feedback, we would like to collaborate on this proposal to make it ideal across the ecosystem.

I think I’d be okay with making traitLabelsURI optional if the 32 chars of the traitKey is sufficient, although the trait labels schema can contain more functionality if you take a look at the spec (displayType, addresses that can edit the acceptable values to provide a UI for users to update traits themselves if they are allowed to). However I think it’s challenging to start having different interfaceID requirements in the same EIP, the EIP should ideally still have just one interfaceID. We could specify if the traitLabelsURI returns no data or blank string, then the ascii value of the traitKey should be used as the label.

> What event is triggered if someone wants to add a trait? Is there then an event for updating the trait URI?

yes there are events for these in the spec, `TraitUpdated` and `TraitLabelsURIUpdated`.

---

**nickjuntilla** (2023-09-14):

Thanks I see the TraitLabelURIUpdated now.

Just to confirm, if someone adds a trait then a traitUpdated event will fire should fire that has the new trait in the event right? That is even if the trait has not previously existed software watching this event should see the new update with the new trait and accept that there is now a new trait right?

When you are saying the “interface” for the EIP I think there is some confusion because the interface for the smart contract is not really the json schema for the labels. That a convenience file to help display data. The actual interface for the smart contract are the getters and setters. So the getters and setters for the smart contract are the source of truth. So if the json schema does not align with the actual keys returned from getTraitKeys then getTraitKeys wins. So the json schema is actually redundant and a point of weakness because it could get out of alignment with the actual data in the smart contract. This is why I believe it should be optional.

For instance you talk about a list of addresses that are allowed to edit traits being in the json schema, but that is actually irrelevant if it is not reflected in the smart contract. So therefore it is up to developers to always insure that the information is in 2 places. Many errors and confusion can happen if these things get out of sync. In fact if it’s really useful to have multiple editors for traits then that data should probably be return from a getEditors getter instead. I suspect though that most people will only have one administration account that can edit traits, which is another reason why requiring a traitLabelsURI just seems like an extra way mistakes can be introduced. I’m not against traitLabelsURI. I see the benefit, but I also see how it can go wrong if it gets out of sync and some people might not wish to use it.

Also I had another question. Is fullTraitKey in the json schema necessary if traitLabel is supplied?

---

**nickjuntilla** (2023-09-14):

Also I second [@fedepo](/u/fedepo) for expanding this to include other on-chain metadata, possible in a new EIP, but it seems a shame to have not standard to include other root metadata properties and it accounts for project reveal phases, changing images, and many common use cases already across the ecosystem.

---

**xinbenlv** (2023-09-21):

This is interesting. Love the idea, [@ryanio](/u/ryanio) . We would like to invite you to share the proposal  on [GitHub - ercref/AllERCDevs: Meeting Repository for AllERCDevs](https://github.com/ercref/AllERCDevs). It rotates between 2 timezone and run biweekly, a place for ERC authors and dApp builders to meet/learn/give feedback/advocate for standardization.

---

**ryanio** (2023-09-22):

> Just to confirm, if someone adds a trait then a traitUpdated event will fire should fire that has the new trait in the event right? That is even if the trait has not previously existed software watching this event should see the new update with the new trait and accept that there is now a new trait right?

Correct

> When you are saying the “interface” for the EIP I think there is some confusion because the interface for the smart contract is not really the json schema for the labels. That a convenience file to help display data. The actual interface for the smart contract are the getters and setters. So the getters and setters for the smart contract are the source of truth. So if the json schema does not align with the actual keys returned from getTraitKeys then getTraitKeys wins. So the json schema is actually redundant and a point of weakness because it could get out of alignment with the actual data in the smart contract. This is why I believe it should be optional.

I am okay with making traitLabelsURI optional. I will still require that the getter be present to simplify the interfaceId instead of having multiple versions, but the method can return a blank string to mean just to use the ASCII value of the traitKey. Yes it is up to the developers to ensure the trait labels URI stays in sync. If it is out of sync, preference should be given to the contract values.

> In fact if it’s really useful to have multiple editors for traits then that data should probably be return from a getEditors getter instead.

I like that idea, but hesitate to add more getters to the interface. Will think about it.

> Also I had another question. Is fullTraitKey in the json schema necessary if traitLabel is supplied?

It is optional if the traitKey is the fullTraitKey. The purpose of fullTraitKey is to get the full raw trait key including its nesting. I am considering removing the nesting aspect to simplify this area. Do you think the trait key nesting would be valuable to have, or an extra feature that just adds complication? In today’s metadata world we don’t really have a concept of nesting metadata.

> Also I second @fedepo for expanding this to include other on-chain metadata, possible in a new EIP, but it seems a shame to have not standard to include other root metadata properties and it accounts for project reveal phases, changing images, and many common use cases already across the ecosystem.

We can include in a EIP that inherits this one. To me it isn’t necessary to return root metadata properties since they are largely not used on chain and doesn’t affect the value of the NFT. I do see the value in other contracts using the values though in some e.g. gaming contexts. I explained similar reasoning in my reply [here](https://ethereum-magicians.org/t/erc-7496-nft-dynamic-traits/15484/3).

---

**ryanio** (2023-09-22):

Thanks! I just submit the google form on your website to offer to present at the Oct 3 meeting.

---

**nickjuntilla** (2023-09-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ryanio/48/10290_2.png) ryanio:

> I am okay with making traitLabelsURI optional.

I feel like that is a decent compromise.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ryanio/48/10290_2.png) ryanio:

> I am considering removing the nesting aspect to simplify this area. Do you think the trait key nesting would be valuable to have, or an extra feature that just adds complication?

I understand what the intent is now, but I worry that this is probably the most confusing part of an otherwise very straightforward specification. It may be optimizing for a very small edge case and trying to solve a problem that doesn’t currently exist. I’ve looked at hundreds of NFT metadata files and rarely seen one with so many traits that they could be better served by nesting. It could also lead to encouraging some poor data hygiene like nesting when it isn’t necessary. If someone were to naively map these values into a nosql database with deep nesting they would be difficult to query. People could still add dot syntax to their projects and create their own custom UI if they have NFTs with some extravagant amount of traits. Then to keep the updating optimization in place for indexers using traitKeyPattern the event syntax could be changed to `*`, `prefix*`, or `keyName` where people would be free to use a prefix if they wanted. Most people would probably still use a single key or all. A comma separated list would be nice, but that would have the character limit. This could also get weird if someone is adding a new trait. If someone adds 5 new traits, but you don’t have the full keyNames. You would need to query the blockchain to figure out what they are, same as with the dot notation. You could say bulk update can only be used with existing keys. Then it would have to be clear that new keys could only be added one at a time. We want to be able to reconstruct everything from events right?

All of this makes me wonder why there is no bulk trait setter methods if we have bulk update events? Why not for many tokens:

`function setTraitsBulk(bytes32 traitKey, uint256[] tokenIds, bytes32 value) external;`

and for all many traits on a token

`function setTraitsToken(bytes32[] traitKeys, uint256 tokenId, bytes32 value) external;`

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ryanio/48/10290_2.png) ryanio:

> To me it isn’t necessary to return root metadata properties since they are largely not used on chain and doesn’t affect the value of the NFT

Having the possibility to have the name on-chain for instance opens the door for better fully on-chain dapp experiences as well as documentation. Not having a plan for letting people put data on-chain is what got us into this situation. It would make it more granular and efficient as well if for instance someone is just updating the image on nothing else. I think the best pattern would just be to override root level properties with traits of the same name. A name trait would be the name property. Description would be description. I think this would probably be expected behavior by most people.

---

**ryanio** (2023-10-12):

Some recent updates to the spec:

- Based on feedback, we simplified the getters/setters to a much more concise list of just 3 getters and 1 setter
- Removed the uri param in the TraitMetadataURIUpdated event since an onchain uri may get long and expensive to emit. The event simply lets offchain indexers know to go fetch the latest from getTraitMetadataURI()
- Simplified the JSON schema and added more functionality

Added dataType and valueMappings
- Added a validateOnSale property for marketplaces to know what values to guard orders on

Please take a look at these latest round of changes and let us know other things to consider.


*(5 more replies not shown)*
