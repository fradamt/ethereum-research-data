---
source: magicians
topic_id: 5985
title: "Request for Feedback: Standardizing Location Metadata and Other Metadata in ERC-721 Tokens"
author: RicardoChacon
date: "2021-04-13"
category: ERCs
tags: [nft, token, metadata, feedback-wanted]
url: https://ethereum-magicians.org/t/request-for-feedback-standardizing-location-metadata-and-other-metadata-in-erc-721-tokens/5985
views: 3497
likes: 12
posts_count: 15
---

# Request for Feedback: Standardizing Location Metadata and Other Metadata in ERC-721 Tokens

Token Metadata can be incredibly meaningful, how do we make sure everyone is able to make use of it?

With the increasing popularity of NFTs and use of ERC-721 tokens as well as the adoption of the Ethereum Blockchain for a variety of use cases, we are presented with a unique opportunity to learn an incredible amount of the token movements and use cases through its metadata. This is not the only benefit we have, we can start thinking about composability as well since development can be sped up and optimized if Smart Contracts and Tokens use previously defined compatible standards. With this idea in mind we can set up the building blocks for a myriad of complex scenarios moving forward.

However, metadata is optional and as such, millions of tokens could be addressing similar use cases (with similar metadata) but not become immediately apparent. In order to easily and cost-efficiently draw meaningful conclusions from this metadata, I would argue that it is in the best interest of the community to standardize how certain pieces of metadata are structured in the tokens. For example: I want to include location metadata to a token in the following format:

[![Screen Shot 2021-04-12 at 2.47.13 PM](https://ethereum-magicians.org/uploads/default/optimized/2X/9/9693609784528a5413f98c1d08867df5be495559_2_334x500.png)Screen Shot 2021-04-12 at 2.47.13 PM1152×1722 198 KB](https://ethereum-magicians.org/uploads/default/9693609784528a5413f98c1d08867df5be495559)

Note: this is what the ERC-721 token Metadata JSON would look like after adding the location metadata in the particular proposed format.

The idea is to turn this into an EIP and set a precedent for future Metadata Standards, this way anyone adding metadata to their ERC-721 tokens has access to robust guidelines which they can follow in order to make their use cases tidier and benefit the community as a whole. As part of the Blockchain division at EY (Ernst & Young), we’re working on products and services promoting transparency across business partners, traceability for tokenized assets, and trust in technology by showing token information in a way that is responsive to the metadata associated with that token. We’re looking for input from the community to determine what information is most important to help make this EIP happen so we can collaborate and build together solutions that would positively impact developers and help towards the widespread adoption of Ethereum and Blockchain as a technology.

## Replies

**cryppadotta** (2021-04-14):

One thing you might find helpful is to re-use existing schema archives and tooling from web development generally. For example [JSON Schema](https://www.schemastore.org/json/) has a library of schemas as well as schema dot org, which has thoughtful schemas on things such as a Place or even a [LocalBusiness](https://schema.org/LocalBusiness).

---

**greg7mdp** (2021-04-18):

What about reusing the existing standard [Extensible Metadata Platform - Wikipedia](https://en.wikipedia.org/wiki/Extensible_Metadata_Platform) ?

---

**RicardoChacon** (2021-04-20):

I’ll look into it. I guess the only thing that comes to mind as of right now is that XMP at the end of the day is implemented through embedding XML in the media file. However, since this EIP looks for a standardization of the ERC-721 Token Metadata (a JSON), it wouldn’t be practical to use XMP. That being said, I’ll dive into it and see if there’s any way in which we could reuse anything from it. Cheers!

---

**anett** (2021-04-26):

Hi Ricardo,

Have you seen [EIP-2477](https://eips.ethereum.org/EIPS/eip-2477) about Token Metadata Integrity ? This EIP may solve similar issues that your proposed new standard would solve.

I’m organising Working Group around improving the ERC721 Standard and creating new improved standard. There is a lot to improve on the ERC721 and I believe together we can create new community standard that would be better than the old ERC721. Feel free to chime in [Improving NFT standard](https://ethereum-magicians.org/t/improving-nft-standard/6012)

---

**dievardump** (2021-05-02):

We have been integrating using JSON-LD and https://schema.org/VisualArtwork for our artists artworks.

This coupled to some [DID](https://www.w3.org/TR/did-core/)  can go very very far and give a lot of information.

What is great is that Schema dot Org have very extensive list of Schema for all kinds of data, and it is possible to describe almost everything needed.

---

**anthonygraignic** (2021-05-02):

Hi,

After looking at the metadata spec of ERC721, ERC1155 and what big platforms do, I think too that Metadata Standards are needed.

But as NFT represents a wide range of things from gaming to art (or attendance proof) and as this is a fast growing and changing market, the task seems really complicated !

So I ended up finding the ERC721 metadata minimal requirements a good approach at this time allowing you to add your metadata scheme on top (and the ERC1155 going too far even in i18n).

As [@dievardump](/u/dievardump) said, we found the schema dot org a good place for mature data scheme (even if the naming is weird sometimes ![:roll_eyes:](https://ethereum-magicians.org/images/emoji/twitter/roll_eyes.png?v=9)) and the DID approach really good for combining schemes (still in DRAFT)

https://www.w3.org/TR/did-core/#production-0

“@context”: [

“https ://www.w3.org/2018/credentials/v1”,

“https ://w3id.org/security/bbs/v1”,]

So if we want to do an EIP about extending metadata, I think we should keep it simple and just standardize the schema definitions used, so computers can get the schema definition, parse and validate it correctly something like the DID’s `@context: []`. Totally up for it !

---

**fulldecent** (2021-05-06):

# Comment on this EIP

Please double check the JSON schema, it is not having the effect you intend. You can test here with a valid and an invalid example. https://www.jsonschemavalidator.net

# How to do what you want to do

ERC-721 (and more tokens) admits the ability to connect any JSON object, and provides a brief, option schema. Of course, in the wild much more metadata is used.

The correct™ way to add more structured metadata to ERC-721 is to use an existing data schema defined at [Full schema hierarchy - Schema.org](https://schema.org/docs/full.html). (Please click “expand all” and then use your browser to search that page.) You can directly implement those into your application.

# This EIP should be abandoned

The creation of a new location standard, which is incompatible with the well-established [Schema.org](http://Schema.org) location standard, and gluing it into ERC-721 does not add any value in the matter of the semantic web (i.e. the original “web 3.0”). Furthermore, if this EIP will be in-scope for the EIP project, it could easily be argued that EVERY JSON Schema should be added a new EIP.

1,700 metadata schemas × 50 token standards = why are we doing this?

In the interest of Do not Repeat Yourself, I recommend this EIP be abandoned as out-of-scope for the Ethereum project.

Or, at a very minimum, it should be replaced to say only “EIP-XXXX, if an ERC-721 token uses the metadata extension and the referenced JSON file includes a “location” property then that property shall conform to the XXXXXXX schema as published on [Schema.org](http://Schema.org).”

---

**dievardump** (2021-05-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> The correct™ way to add more structured metadata to ERC-721 is to use an existing data schema defined at Schema.org - Schema.org .

Hi ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) could you elaborate on this? Where do you take this statement from?

The only mentions of JSON Schema in [EIP-721](https://eips.ethereum.org/EIPS/eip-721) that I found do not clarify the fact that all and any structured metadata are to follow an existing [Schema.org](http://Schema.org) schema if it exists.

And although I would like it to be true, I would like to see it stated somewhere clearly, but I can’t find it.

---

**fulldecent** (2021-05-07):

[Schema.org](http://Schema.org) is a standard only in a *de facto* sense. This means I might convince you and everybody that it is a standard if I can convince you that most everybody else is already using it.

Let’s try.

- The French government recognizes schema.org as the first notable initiative compared to their own data organization initiatives, https://schema.data.gouv.fr
- Google integrates structured data in its web crawlers. In their structured data documentation, “Most Search structured data uses schema.org vocabulary” Intro to How Structured Data Markup Works | Google Search Central  |  Documentation  |  Google for Developers.
- So does Bing (and by extension Duckduckgo), Bing Webmaster Tools - Help Documentation.
- The US government website on open data references schema.org as something to consider mapping to, Home | resources.data.gov.
- The US Federal Emergency Management Agency, in discussing data sharing with hospitals regarding COVID-19, recognized schema.org as a “standardized format” for metadata.
- schema.org is the 1813th most popular website on Earth. I have not checked the ones before it, but this is pretty good for something that does not have an end-user product. Screen Shot 2021-05-07 at 09.08.472648×1960 537 KB

These are just the first few examples I have found from looking at the backlinks to [schema.org](http://schema.org) from government sources (plus what I already know about Google’s crawler). There are 7,400 remaining government references. And 200 million other non-government references.

---

I don’t have much more to say about notoriety. But in terms of the quality of that project… it is quite thorough.

---

**deshicollector** (2021-05-09):

Living ‘NFT’: A Token with variable (meta)Data structure

I am a PM developing a Game

User wants his Token to have properties of change ( Eg. As age changes by time)

Is there a protocol to support this Use case?

---

**anett** (2021-05-10):

[Async Art](https://async.art/) is using similar concept - the artwork changes based on the set properties (changes by time). Unfortunately they have no live technical documentation where you can find how their programmable art works. They are definitely using ERC721 and some custom extension built on the top of it.

---

**jamesmorgan** (2021-05-20):

Hi all,

I think it would be great to push for wider standardisation of JSON metadata for NFTs, lots of various bespoke offerings atm and we should all try and converge on some baseline standards IMO.

Some of the [schema.org](http://schema.org) ones I have been looking at are:

- VisualArtwork - Schema.org Type
- CreativeWork - Schema.org Type
- ArtGallery - Schema.org Type

This is mainly as I have been looking at NFTs for art and creativity use cases but I am sure there are others which can be repurposed.

I generally favour using these more well established ones from [Schema.org](http://Schema.org) if possible and not to re-invent something just for NFTs. Maybe any new EIPs can simple reference [schema.org](http://schema.org) version as a baseline? I am also not sure how wide any [schema.org](http://schema.org) schemas are used but they do a great job of listing out lots of options.

---

**RicardoChacon** (2021-06-18):

Hi all and thanks for the feedback collected thus far. We’ve taken it all into consideration and made some major changes to incorporate [Schema.org](http://Schema.org) and provide a more streamlined way of extending the metadata with this principle in mind. The changes are up in the same PR [Added new EIP Draft for ERC-721 location metadata by RicardoChacon · Pull Request #3551 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/3551) and we look forward to receiving any further comments or suggestions

---

**anett** (2021-08-13):

Hey [@RicardoChacon](/u/ricardochacon), can you please elaborate on why you would like to include location metadata to a token? Why physical location for token matters? It make sense for projects like [foam](https://foam.space/) but I’m sure they are using other solution (I haven’t looked into technical details).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ricardochacon/48/3758_2.png) RicardoChacon:

> I want to include location metadata to a token in the following format:

I do agree that we need to collaborate on better standard and not use ERC721 anymore as it has more flaws than strength honestly.

We should look into better definition of metadata and how to display and access token metadata. The [EIP-1047](https://github.com/ethereum/EIPs/pull/1028) was supposed to define metadata but it fell off to the darkness.

I hosted NFT Metadata twitter spaces a few weeks ago where we discussed this problem into more details, [notes](https://hackmd.io/@Bnkhqf0tSbi1lX2Xc-WXYQ/ByxXJK-JK). The main takeaway from this session: NFT platforms should collaborate together on unification of metadata, metadata formats so users will see their NFTs across different platforms.

