---
source: magicians
topic_id: 7752
title: Standardizing marketplace "view" of an NFT while allowing for user-defined "view"
author: tim-cotten
date: "2021-12-12"
category: Magicians > Primordial Soup
tags: [nft, erc-721, 3d-model]
url: https://ethereum-magicians.org/t/standardizing-marketplace-view-of-an-nft-while-allowing-for-user-defined-view/7752
views: 706
likes: 1
posts_count: 1
---

# Standardizing marketplace "view" of an NFT while allowing for user-defined "view"

Example Use Case: NFTs based on 3D Models

Benefit: Standardize the way marketplaces present the NFT (scene, lighting, orientation, camera) while allowing the user to provide their own presentation view definition.

Example:

A player in a popular MMO has an NFT representing their +10 Sword of Fire that has a translucent edge. They also have the ability to show it on their in-game character at a chosen orientation with the backlighting that shows it off (in their eyes) in the best way to other players.

However, when they move it onto a marketplace for an auction sale, the sword might be up against several other swords from the same game. Rather than have them all be in willy nilly orientations the NFT creator instead declared that all swords of this class have a default “view” so that they can be easily compared/contrasted visually.

This would make item preview windows in marketplaces be able to enforce consistency between iterations of similar objects.

In my case, I’m working on a fun Christmas project for jewels, and I want to give users the ability to assign their own custom JSON metadata to represent *their* proposed view (and also allow this to be rendered on my website) while also keeping a consistent system default view for sales/comparisons.

That way a blue diamond looks blue by default regardless of the user’s chosen lighting.

I envision this to be an interface similar to ERC721Metadata that exposes two functions: “canonical” and “custom”; each, like ERC721Metadata, pointing to a URI with a JSON file. The “canonical” will NOT be updateable, but custom will have a method to update it by the NFT owner.

The JSON file format is not fleshed out yet; it’d be good to discuss scene definition (for 3D), or background images/CSS effects (for 2D).
