---
source: magicians
topic_id: 10932
title: Discussion - Can Ethereum be a linked data web?
author: JessicaC
date: "2022-09-19"
category: Magicians > Primordial Soup
tags: [nft, metadata, sbt, semantic]
url: https://ethereum-magicians.org/t/discussion-can-ethereum-be-a-linked-data-web/10932
views: 1766
likes: 10
posts_count: 9
---

# Discussion - Can Ethereum be a linked data web?

After the long awaited merge shipped on 15 Sept 2022, the stage is set for further scalability, security, and sustainability. Now we can start to think of building something novel if the txs are 100x cheaper.

The SBTs proposed by the paper Decentralized Society: Finding Web3’s Soul is inspiring. To build something centred around the Ethereum Identity Ecosystem, the way to prove something about your account, or you can call it wallets or souls, is really important. There are some early movers already building in this field, like POAPs to prove the attendance.

**What if we can go one step beyond them by making the proof of something NFTs public goods?**

The current NFT standard writes only the tokenID, name and URI in metadata. The URI usually points to somewhere on a centralized server like AWS. Although the data is open, the machine reading of the data causes high friction. The friction is even worse if we try to build something that requires more intelligence. Not to mention the centralized storage is in the contract to data sovereignty. The numerous tokens become meaningless once the server is down.

A more decentralized way to issue the SBTs is that we write the meaning directly in the metadata. The open availability makes the reading of the meaning independent of any servers. And if we want to make it easier for the developers, we can write the meaning in some structure format, or even in some standard format like using RDF.

For example, if the SBT represents someone who is a member of a DAO. When you read the on-chain data, you only know the account is holding an SBT, that’s all. But if we add the meaning in an RDF format, the machine can easily know the account is a member of a DAO. And this is a directed graph link, linking the account and the DAO.

Consider each account is a data source that holds many SBTs, each SBT describes the relationship meaning in standard format and pointing to another data source.  Ethereum is now a linked data web!

With more and more people creating their data in the format, the data web has increasing returns to all that can be easily shared and reused across community boundaries.

## Replies

**Pandapip1** (2022-09-20):

This is already possible with `data:` URIs.

---

**DonMartin3z** (2022-09-21):

Please. Contact me . i got a deep project that will soon be posted in here , it 's all about ethereum’s future and the SBT’s interface / objective. [Zaeondao@gmail.com](mailto:Zaeondao@gmail.com)

---

**JessicaC** (2022-09-25):

The URI is the way to identify the resources stored else where like AWS. The semantic NFTs will create a chain native data layer that is easy to query, to share and reuse with lower friction.

---

**TimDaub** (2022-09-27):

I’ve been working actively on this idea since 2016 when we proposed an IP rights management on blockchains with COALA IP: [GitHub - COALAIP/specs: COALA IP is a blockchain-ready, community-driven protocol for intellectual property licensing.](https://github.com/COALAIP/specs). Way more recently, with https://neume.network we’re building a socially scalable data extraction crawler geared towards derivative data published on Ethereum. The biggest challenge we currently face is that many in the space consider block tag “latest” as the de-facto manifestation of a blockchain object: But honestly, working more closely on the use case, what seems to be most important is the idempotency of calls and block tag “latest” doesn’t allow it.

So I’ve been actively trying to influence identity groups to add a block tag descriptor to identity formats - I see them as precursors to properly linked data. Here are two examples where I’ve yet to succeed having influence and adding idempotency:

CAIP-19: [CAIP-19: Add block number tag in query by qizhou · Pull Request #125 · ChainAgnostic/CAIPs · GitHub](https://github.com/ChainAgnostic/CAIPs/pull/125)

EIP-4804: [EIP-4804: Web3 URL to EVM Call Message Translation - #27 by TimDaub](https://ethereum-magicians.org/t/eip-4804-web3-url-to-evm-call-message-translation/8300/27)

---

**gbdt** (2022-10-12):

The idea is practical. The current metadata lacks standards, resulting in fragmented data. We need pre-defined data models for metadata.

I’m not sure it’s a good idea to put metadata on-chain. Possibly we can put RDF on-chain? or RDF attached to the metadata on IPFS?

Ceramic and Textile teams are working on IPFS in this similar area.

[Ceramic ComposeDB](https://composedb.js.org)

[Textilt TableLand](https://tableland.xyz/)

---

**MidnightLightning** (2024-01-15):

I’ve been musing on this topic recently, and now that ERC4804 is accepted in the Standards Track, there’s some possibilities for standardizing there (though with a note that a few errors were found in ERC4804 post-approval, and [EIP6860](https://eips.ethereum.org/EIPS/eip-6860) is in-progress to clarify and replace ERC4804).

In RDF’s “Subject, Predicate, Object” data structure, each needs a URI to define them. To define “The DAI balance of Address X” we can present:

- Subject: web3://0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 (or web3://vitalik.eth)
- Predicate: web3://0x6B175474E89094C44Da98b954EedeAC495271d0F/balanceOf
- Object: uint fetched from blockchain execution

This works well for annotations that have an EVM Address as the Subject, and any “view” function of a smart contract. However, what if we wanted to talk about a specific NFT (ERC721)? The EIP6860 standard indicates that what comes after the contract address in the path must be a contract function. So I believe `web3://0xc3f733ca98E0daD0386979Eb96fb1722A1A05E69/1289` would not be a valid way to refer to MoonCat #1289. However, EIP6860 only reserves two query parameters (`returns` and `returnTypes`) as important to that standard, so a URI like `web3://0xc3f733ca98E0daD0386979Eb96fb1722A1A05E69?tokenId=1289` would be allowed by that standard.

However, the RDF standard gives a slight preference toward using [fragment identifiers](https://www.w3.org/TR/rdf11-concepts/#section-fragID) in the URI. So `web3://0xc3f733ca98E0daD0386979Eb96fb1722A1A05E69#1289` would be a way to refer to MoonCat #1289.

Fragment identifiers could also be used for tokens with non-integer identifiers. Since the MoonCat tokens predate the ERC721 standard, they use raw hex identifiers in their original contract. So, `web3://0x60cd862c9C687A9dE49aecdC3A99b74A4fc54aB6#0x004e3952fa` works as a URI for MoonCat #1289 too.

Thus, would the following make sense as JSON-LD data for a Linked Data representation of token metadata?

```json
{
  "@context": {
    "mcr": "web3://0x60cd862c9C687A9dE49aecdC3A99b74A4fc54aB6#",
    "mctraits": "web3://0x9330BbfBa0C8FdAf0D93717E4405a410a6103cC2/traitsOf#",
    "mccolors": "web3://0x2fd7E0c38243eA15700F45cfc38A7a7f66df1deC/colorsOf"
  },
  "@id": "mcr:0x004e3952fa",
  "mctraits:catId": "0x004e3952fa",
  "mctraits:pose": "pouncing",
  "mctraits:rescueYear": 2017,
  "mctraits:expression": "smiling",
  "mctraits:facing": "right",
  "mctraits:genesis": false,
  "mctraits:pale": false,
  "mctraits:pattern": "tortie",
  "mccolors": "57,82,250,0,7,51,0,13,102,0,30,230,102,122,255,153,234,255,230,200,0,255,242,153"
}
```

---

**MidnightLightning** (2024-01-16):

I jumped straight to JSON-LD as an idea, since that meshes well with the existing NFT implementations that represent a token’s metadata in JSON-format (either directly as an output of the `tokenURI` call, or what gets returned when the URI is queried). Opensea has tried to establish themselves as the owners of [that standard](https://docs.opensea.io/docs/metadata-standards), though it’s not an official EIP (so ERC721-compliant tokens don’t *have* to adhere to it).

If contracts used JSON-LD to self-identify the linkages they have authority over, I think the key missing piece would be an overall ontology. The overall ontology would need to define “a smart contract” (and allow linking them to other RDF ontologies, like the Person or Organization that created/owns them. This could be a subclass of a [Creative Work](https://schema.org/CreativeWork)), and represent the EIPs that define smart contract interfaces (EIPs can use URIs in the form of `https://eips.ethereum.org/EIPS/eip-20` to represent them, but need separate RDF-formatted ontologies that structure the requirements like “an ERC20 smart contract may have a `name` and `symbol` property”). Since those overall definitions would not be project-specific, they could be worked on collectively, and be a good starting point for getting semantic crawlers able to parse information about blockchains?

---

**MidnightLightning** (2024-06-24):

Delving further into the idea of JSON-LD, and hit a snag. One of the key tenants of having data be in JSON-LD format is the `@context` property can be used to annotate an existing vanilla JSON blob to give it JSON-LD functionality. The benefit of that is any tool that only knows JSON instead of JSON-LD can simply ignore the `@context` property and continue as normal.

The issue arises from the fact that the [JSON format for Solidity smart contracts](https://docs.soliditylang.org/en/latest/abi-spec.html#json) has a top-level `type` property (which can be `function`, `event`, `constructor`, `receive`, or `error`) which is a true “type” classification for the object, but the items that are in `inputs` and `outputs` properties also have a `type` property, and those properties indicate what format the data they process are, not what they themselves are (`type=inputArgument` or `type=outputProperty`). The way that JSON-LD `@context` is handled, you cannot alias sub-properties separately than top-level properties. So the following is invalid:

```json
{
  "@context": {
    "type": "@type",
    "inputs.type": "https://example.com/#inputArgumentType"
    "outputs.type": "https://example.com/#outputArgumentType"
  }
}
```

There [was a proposal](https://github.com/w3c/json-ld-syntax/issues/7) to create a `@values` context property to define the types of lists/containers, but that’s not been actually merged into the JSON-LD format. If it were, something like this might work, but at the moment no parsers manage this:

```json
{
  "@context": {
    "type": "@type",
    "inputs": {
      "@container": "@list",
      "@values": {
        "type": "https://example.com/#inputArgumentType"
      }
    }
  }
}
```

The only way I see to get all three properties named “type” to have three different interpretations, is to have an individual `@context` block for every single `input` and `output` sub-element. An automated process could convert a plain JSON ABI to have all those `@context` elements, but it would no longer be a feasible process to do by hand.

