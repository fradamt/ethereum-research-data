---
source: magicians
topic_id: 1568
title: ERC721 metadata doesn't fit our data model
author: TimDaub
date: "2018-10-11"
category: Magicians > Primordial Soup
tags: [erc-721, metadata]
url: https://ethereum-magicians.org/t/erc721-metadata-doesnt-fit-our-data-model/1568
views: 3652
likes: 3
posts_count: 5
---

# ERC721 metadata doesn't fit our data model

Hi there Ethereum Magicians,

My name is Tim Daubenschütz and I’m one of the co-authors of the COALA IP

specification (https://github.com/COALAIP/specs). I’m currently working with a

client that wants to put film rights on the Ethereum blockchain and thought of

using ERC721 to tokenize the rights and COALA IP for modeling a right’s

metadata. I did some research into ERC721 and found out that there

is an optional metadata extension that specifies `name`, `symbol` and

`tokenURI`. That’s great, I thought, but when I looked more closely into the

specification I noticed that `tokenURI` expects a very specific JSON schema of

the form:

```auto
{
    "title": "Asset Metadata",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Identifies the asset to which this NFT represents",
        },
        "description": {
            "type": "string",
            "description": "Describes the asset to which this NFT represents",
        },
        "image": {
            "type": "string",
            "description": "A URI pointing to a resource with mime type image/* representing the asset to which this NFT represents. Consider making any images at a width between 320 and 1080 pixels and aspect ratio between 1.91:1 and 4:5 inclusive.",
        }
    }
}
```

As we’ll see later, this JSON schema will lead to problems defining a COALA IP

right as an ERC721 `tokenURI`. But first, let’s introduce COALA IP.

COALA IP is a blockchain-ready licensing protocol for intellectual property.

It’s based on the LinkedContentCoalition’s Right Reference

Model, a model that existing IP

standards are drafted upon (e.g. DDEX for music, PLUS for stock photos).

At COALA IP’s core are data models that can be used to model an ontology using

JSON-LD. There are data models for an entity creating a work (the Party entity),

the work itself (Creation and Manifestation entity) as well as an entity for

representing copyright and licensing rights (the Right entity). These models

are then linked to build an ontology using JSON-LD (and IPLD - a minor detail).

A specialty of COALA IP is that it maps the LCC’s “RightAssignment” entity -

which represents a transfer of copyright or licensing rights from one Party to

another - to blockchain transfers. The idea behind it is to make as many

blockchains compatible with COALA IP as possible as they only need

to have the following features:

- Need to allow for an entity to be stored on the substrate (I’m saying
substrate because it can include tech like IPFS)
- Need to allow an entity to be transferred natively.

So when I first heard of ERC721 I got excited, especially because it

would mean that we can tokenize COALA IP Rights as ERC721 tokens and transfer

them between wallets seamlessly. However, a COALA IP Right looks like this:

```auto
{
    "@context": "http://coalaip.schema/",
    "@type": "Right",
    "@id": "",
    "usages": "all|copy|play|stream|...",
    "territory": "",
    "context": "inflight|inpublic|commercialuse...",
    "exclusive": true|false,
    "numberOfUses": "1, 2, 3, ...",
    "share": "1, 2, 3, ..., 100",
    "validFrom": {
        "@type": "Date",
        "@value": "2016-01-01"
    },
    "validTo": {
        "@type": "Date",
        "@value": "2017-01-01"
    },
    "source": "",
    "license": ""
}
```

My initial excitement deflated once I saw the JSON schema that ERC721

optionally recommends. It’s totally incompatible.

How can we reconcile this? A few ideas I had so far are:

### 1. Change COALA IP to make it fit ERC721

Hardly possible. We can try to squeeze COALA IP information into name,

description and image, but that will ultimately only confuse wallet end users.

A COALA IP’s right’s essence is that the license is linked as a PDF and that

certain crucial values like `share`, `exclusive`, etc. are contained in the

data model. Making COALA IP fit ERC721 would erase most of COALA IP’s positive

properties and only add a half-baked tokenized right into users’ wallets.

### 2. Define name, description and image, but also define COALA IP Right’s properties

Probably the easiest solution out there. Instead of changing anything in COALA IP and ERC721, I’ll just add more metadata to the JSON schema. In fact, [some websites like Opensea.io have gone ahead already and support additional properties in the tokenURI](https://docs.opensea.io/docs/2-adding-metadata). The problem with this is the challenge for wallet developers. Will they care about COALA IP properties enough to implement them separately? Likely not.

### 3. Write an EIP that supports a COALA IP Right as JSON schema

More difficult than 1. and 2… To create an EIP one needs to gather use cases,

reference implementations, etc. In the end it’s also highly unlikely that an

EIP solely for the purpose of tokenizing IP rights is gonna stand out enough

for wallet developers to implement it.

### 4. Write a standard to allow arbitrary data to be included into an ERC721 tokenURI (e.g. using JSON-LD)

Definitely the most difficult thing to do. Not only is some of the tech

controversial (e.g. JSON-LD), it’s also unclear to me if wallet developers

would adopt such a way more complicated standard.

### So now what?

After all of these thoughts, I’m now here, looking for the council of the

Ethereum Magicians. What do you think is the best option to go with? Is there

options that I missed? Specifically, what do you think of options 3. and 4., and

do you think they’re viable.

Additionally: Are you an ERC721 implementer and have encountered the issues

described in this post? If so, I’d like to hear from you. After all, we’re

calling these things non-fungible tokens, but so far they can hardly be more

than in-game items. There are so many more use cases to be explored!

Best,

Tim

## Replies

**RiganoESQ** (2018-10-12):

wow, literally about to release this in the coming days.  EIP tokenization of IP for public benefit, ref implementation and all … been working on it for about 1 year, i went w/ 3 … its more of an R&D IP DAO situation, but no reason it couldn’t be applicable to movie rights.  does not require new wallets, etc.

im a tech IP lawyer based in NYC ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**dekz** (2018-10-12):

The metadata described in ERC721 is an optional extension. What resides at the destination of tokenURI is totally out of scope for the core standard.

You would not be “out of spec” by choosing to implement any additional metadata stored in the tokenURI location. People may want to use JSON or csvs or what have you.

> The URI may point to a JSON file that conforms to the “ERC721 Metadata JSON Schema”.

Emphasis on the **may** and the lack of **must**. There’s no way we can define a off-chain metadata schema that will solve all use cases. The EIP can only attempt to define a standard for on-chain interfaces and behaviour. TokenURI is an extremely loose guarantee which can change at any time and is non binding.

The community can decide on what this should look like outside of the blockchain interface for an ERC721.

Consider moving some of that metadata up into the ERC721 token itself, ERC721 defines the basic interface for a interoperable token, you can extend it and add any data on-chain.

The example from OpenSeas is bad, `level`, `weapon_power` should all be on-chain attributes otherwise the value of the asset can be changed by who ever has control of the destination of tokenURI. TokenURI cannot be resolved and read on-chain so it has no on-chain interop capability.

---

**RiganoESQ** (2018-10-16):

Educational purposes only, not legal advice.

(1) If its a movie script, why is on-chain interop capability necessary? check out EIP 1046, by team https://www.rareart.io/ and zeppelin personnel.  it takes the ERC 721 metadata to ERC20.  This is the draft EIP I’ve been working on: https://github.com/RiganoESQ/EIPs/blob/patch-2/EIPS/eip-1048.md , basically defines new metadata structure for licensing intellectual property on a blockchain - using 1046 as a baseline and it leverages the COALA IP schema.

I think this is something the community should work towards given that we can for the first time ever make IP (worth trillions of dollars, legacy system is non-fungible) fungible.

(2) As an immediate solution, consider the following: leverage 1046, create an ERC20 w/ the following Metadata

{

“title”: “Asset Metadata”,

“type”: “object”,

“properties”: {

“name”: {

“type”: “string”,

“description”: “Movie Title”,

},

“description”: {

“type”: “string”,

“description”: “[SWARM/IPFS link to all intellectual property assets, all rights reserved]”,

},

“image”: {

“type”: “string”,

“description”: “[a PDF of the actual human readable license]”,

}

The metadata license agreement should be part of the IP token issuance documentation, thereby enabling the initial set of buyers (from the issuer) to click a check box (standard for token sales) agreeing to the license terms (binding). On the secondary market, transacting in this ERC20 token is consent to the legal agreement in the metadata, thereby enabling IP transactions to occur between two parties using the Ethereum blockchain for enforcement as opposed to lawyers, admins and courts. This is similar to markets trading contracts for commodities. Parts of EULAs are deemed unenforceable when the language is unreasonable.  If this is a standard market licensing agreement, w/o extreme language I’d like to this its ok.

Regarding making more binding for tx on the secondary market, is it possible that every transaction broadcast on the ethereum blockchain must incorporate the hash of the actual license as part of the signature, thereby explicitly binding the signer to the contract every time the token is traded? So get the hash on the signature level as opposed to metadata?

(3) Also, the fact that the minter can change tokenURI can be to your advantage in that you can upload new intellectual property to the SWARM/IPFS database, thereby giving the token holders more solid rights, as opposed to having to speculate that the new trademark or derivative work is not part of this IP package.

thoughts?

---

**Jodokk** (2019-11-24):

We’re  looking for someone to help us at MXRTOW ([Tribesofwar.com](http://Tribesofwar.com)) with licensing for a ERC721 character series.

Do you offer those types of legal services?

