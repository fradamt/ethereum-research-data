---
source: magicians
topic_id: 6394
title: "On-chain Interactivity of NFTs: Making NFTs metaverse-compatible with Meta-actions"
author: dievardump
date: "2021-06-04"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/on-chain-interactivity-of-nfts-making-nfts-metaverse-compatible-with-meta-actions/6394
views: 1841
likes: 3
posts_count: 11
---

# On-chain Interactivity of NFTs: Making NFTs metaverse-compatible with Meta-actions

# On-chain Interactivity of NFTs: Making NFTs metaverse-compatible with Meta-actions

Opening a discussion about the best way we could find to make NFTs metaverse-compatible, and even more than just that, finding a way for NFTs to actually expose to consuming platform that they have an on-chain API available.

Quick Example: being able to tend to your cat needs directly in Cryptovoxels.

## Problem

Today if I create the next super NFT everyone wants, there is a big chance that I would like for it to be importable in current and future VR worlds and Metaverse.

However, more than just being able to import it, I will want users to be able to interact with this NFT.

As an example, this week a project allowing people to purchase a Bonsai NFT came out, and people have been thinking “however it would be nice to be able to tend to the bonsai. Water it. Cut it.”

But today, those actions, if they were possible on the website of the NFT creator, would have to be specifically coded for this specific NFTs to be able to work in Metaverse. Because there is right now no API that allows NFT creators to expose the existence of actions to the consuming platforms.

## Start of a solution

In Web3 and solidity programming, we have something similar: We need an ABI to be able to interact with a contract. Without the ABI, we can not know what are function names, nor what parameters we have to pass.

What if we were finding a way to do the same things for NFTs?

What if in the NFT JSON metadata - or somewhere on-chain, we had a field that actually tells consuming platforms:

“Hey there are actions possible on this NFT, you can even integrate it directly in your metaverse” with a list of actions and definite parameters:

Example:

```auto
{
	"name": "Bonsai #1",
	"description": "The super Bonsai",
	"image": "ipfs://ipfs/Qx...",
	"low_poly": "ipfs://ipfs/Qx...",
	"contract": "0xdeadbeef...",
	"meta_actions": [{
		"name": "Water Bonsai",
		"functionSignature": "waterBonsai(uint256)",
		"inputs": ["tokenId"],
		"user_type": "owner"
	},{
		"name": "Trim Bonsai",
		"functionSignature": "trimBonsai(uint256)",
		"inputs": ["tokenId"],
		"user_type": "owner"
	},{
		"name": "Compliment Bonsai",
		"functionSignature": "complimentBonsai(uint256)",
		"inputs": ["tokenId"],
		"user_type": "guest"
	}]
}
```

`inputs` would be a definite list of keywords that consuming platforms would know. (I can think of contract, tokenId, recipient, amount, …) that would be “self explanatory”

`user_type` would also be a deinite list of keywords that would mostly expose if this action is disponible to anyone or just owner

 → this is an example, it’s not the proposed form of it, I’m opening a discussion with ideas here

Something in this direction would actually allow all Metaverse, when someone loads a Bonsai in their world, to display “possible actions” that the owner can actually do *directly in the metaverse, without having to go away*

I haven’t seen this presented somewhere and can’t find any EIP for this but I think this is the next big step we will have to make for interoperability of NFTs.

Is this something worked on, and if not, what are you thinking about this?

## Replies

**dievardump** (2021-06-05):

When I say Metadata it can also be at contract level:

An extension to ERC721 and ERC1155 that allows to define an “NFT ABI” per token id:

Consuming platforms would see if the contract of the NFT supports this NFT Abi functionality, and if yes, query it to get the ABI / abiURI.

Something like:

```auto
if (await contract.supportsInterface(ERC_NFTABI_INTERFACE)) {
  const nftAbiURI = await contract.nftAbiURI(tokenId);
  const nftABI = await fetch(nftAbiURI).then(res => res.json());
  // now with nftABI the platform knows
  // what interactions are possible on the NFT
  // and can offer users to make those interactions
  // directly in their own interface
}
```

---

**wighawag** (2021-06-06):

if we are talking about on-chain action, the abi of the nft contract itself should be sufficient, no ?

solidity already include the ipfs hash of the source in the bytecode and [sourcify](https://sourcify.dev/) is building a db out of it on ipfs

This seems to already handle all you mention here. Or am I missing something ?

---

**dievardump** (2021-06-06):

Well the abi of the contract is sufficient for the world to know the functions, but how does it know that there are some specific functions that are “actions” available on an NFT?

For example you have an ERC1155 with several tokenIds.

Token ID 1 is a Sword

Token ID 2 is a Tree

Token ID 3 is a Cat

Let’s say all those can be imported and shown in Decentraland.

And in the contract, there is actually a function to Water the tree, so it doesn’t die.

Today if we want Decentraland to show, in their own interface a “Water” action, someone has to code specifically for this (contract, tokenId=2) a custom mapping so it is possible to show this “Water” action for this tree when you click on it.

However, if the NFT itself, could declare “these are the actions anyone can do on me”, then there is no custom mapping needed. The world can just read the interface for this ID, and show the actions that are possible.

Because all actions are not possible on all tokens, not to all people (guest vs owner) and probably the contract might also have function that have nothing to do with actions on the NFTs

Does that make sense?

The idea is more to allow any NFT, that are completely world agnostic, to be able to be fully used & interacted with, in all different worlds.

---

**wighawag** (2021-06-06):

It make sense, got it.

I guess a description field would also be useful. and an icon too, could be optional though.

But how do you think the various metaverse clients would handle this in generic fashion ?

I can see it working via text as this is universal (but we also need to consider languages, etc…). Similarly an icon should work in a generic fashion. This is already great, but not sure we can go much further without hitting some compatibility issues.

To take the watering example, we can imagine in the best case scenario that in the client in question, it would display a watering animation when the action is executed, but that assume specific knowledge of the “meta action” and thus specific integration which then mean that the generic standard was not needed for that instance.

We could maybe imagine a more complete mapping, with an animation associated with it, but this is where we are potentially hitting compatibility issue as different metaverse has different rendering strategies, etc…

I guess we do not need to go that far though and text+icon will already be great, just thinking aloud ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**wighawag** (2021-06-06):

Also regarding, metadata vs solitidy abi and natspec,

it could well be that instead of defining these meta_actions in the metadata it could be part of the natspec.

---

**dievardump** (2021-06-06):

> I guess we do not need to go that far though and text+icon will already be great, just thinking aloud

Yes I was thinking more “easy” first (an action name, signature, maybe “permission” & contract, and description and icons are sure needed you are right), before see what people need. I guess it can already be nice to just be able to interact with your “outsider NFT” without having to always go out of your VR world.

I thought of natspec, but I was thinking it can become a very very long comment if you have to define it for each possible IDs

When at contract level (I would say it’s prefered, like a function `getNFInterface(tokenId) returns (string)` )  or metadata, you would only have to update the “nft interface” to reflect it.

Also maybe the standard would evolve to allow action about this tokenId on different contract (for example if you have one contract that holds the Tokens, and a bunch of separate contracts that actually compose your game features. Then you can define “water” on the “TendToTheTree” contract, and “pet” on the “TenToTheCat” contract, etc… etc… and when you add features to your game, again you can just update the interface for this tokenId with a tx / with a metadata update, instead of redeploying a whole contract with natspecs updated

This way with a simple interface (one function call on the contract to get the interface) you can expose a complicated system to the worlds!

(pardon my schematization skill…)

[Capture d’écran de 2021-06-06 17-02-46|650x499](/uploads/short-url/wzkL1xs7vqwHFZe92uDeNxoncWV.png)

---

**Shymaa-Arafat** (2021-06-06):

1-ur overall topic reminded me of VR a, ie when(if) a country made NFTs for it’s monuments they should also make it include any use of it (the real piece) in VR.

.

2-However, ur example is not clear for me. I understand a game/movie creator would like to make NFTs for his characters how does he draws them, a cat starring in a cartoon for example, but not the moves?! This could vary according to the current movie. Unless u mean if he didn’t NFT every possible moving position of his cat, another game could copy the same cat moving it differently for example???

.

3-In fact that’s an issue I don’t understand how does NFT handle it?

How the cryptographic hash is calculated???

From ur cat example if a competitor put something in the cat hair, will he get away with it as the cryptographic hash will be different???

-Draw a temporary erasable color on an antique???

.

4-My last repeated Q about the Beeple pic, does the hash/copyright include all the hashes of the small pics?and how that is done?in a Merkle like for example?where can I find these details???

---

**dievardump** (2021-06-06):

Hello [@Shymaa-Arafat](/u/shymaa-arafat) , I think you answered to the wrong thread and misunderstood the goal of this one. There is nothing about hash nor drawing/moving things.

The thread you have been participating to until now is this one => [EIP-3340: NFT Editions Standard Extension - #4 by Shymaa-Arafat](https://ethereum-magicians.org/t/eip-3340-nft-editions-standard-extension/6044/4) where you have been talking about hash and asking question Beeple’s work.

---

**Shymaa-Arafat** (2021-06-06):

1-I talked & asked about NFTs in 3 or 4 threads not just the one u mentioned

.

2-If u don’t work in the cryptographic details of NFTs, u can answer the part about ur cat example. Am I getting it right u r talking about an animation cat drawing?

-Not exactly related to ur topic, but u do mean one like the mentioned & complained about in this article right?


      ![](https://static.files.bbci.co.uk/bbcdotcom/web/20251210-151139-37baf2dfdd-web-2.36.1-1/favicon-32x32.png)

      [bbc.com](https://www.bbc.com/news/technology-57273904)



    ![](https://ethereum-magicians.org/uploads/default/optimized/2X/b/b2368e867071940cdcd5af4ad04c9eeb9abf67b2_2_690x388.png)

###



Trying to own a virtual feline proves to be an exhausting and expensive process.

---

**Hectorzh** (2022-07-07):

There is nothing related to the hash.

Your NFT contract is there on the chain stating the NFT is yours. You cannot do anything with the NFT. If you download the cat picture of the NFT, it is a picture and not the NFT though you get the same picture and can draw on it.

