---
source: magicians
topic_id: 10754
title: "EIP-5625: NFT Metadata JSON Schema dStorage Extension"
author: gavfu
date: "2022-09-08"
category: EIPs
tags: [nft, metadata, storage, decentralization, dstorage]
url: https://ethereum-magicians.org/t/eip-5625-nft-metadata-json-schema-dstorage-extension/10754
views: 3011
likes: 5
posts_count: 8
---

# EIP-5625: NFT Metadata JSON Schema dStorage Extension

Add a **dStorage** property to non-fungible tokens (NFTs) metadata JSON schema to provide decentralized storage information of NFT assets.

## Abstract

This standard is an extension to NFT metadata JSON schema defined by **EIP-721** and **EIP-1155**. As a complement, it provides additional information about how the NFT asset is stored in a decentralized storage system, if applicable.

## Motivation

As high valuable crypto property, NFT assets intrinsically demand guaranteed storage to assure their **immutability**, **reliability** and **durability**. NFT ownership is tracked by **ERC721** or **ERC1155** smart contracts, hence persisted in blockchain, which is not a problem. But how about the mime type assets that NFT tokens actually represent? Ideally, they should also be stored in some reliable and verifiable decentralized storage system which is designed to store larger amounts of data than the blockchain itself. As an effort to promote **decentralized storage** adoption in NFT world, we propose to add additional **dStorage** information into NFT metadata JSON schema.

As a refresher, let’s review existing NFT metadata JSON schema standards. **EIP-721** defines a standard contract method `tokenURI` to return a given NFT’s metadata JSON file, conforming to the *ERC721 Metadata JSON Schema*, which defines three properties: `name`, `description` and `image`.

Similarly, **EIP-1155** also defines a standard contract method `uri` to return NFT metadata JSON files conforming to the *ERC-1155 Metadata JSON Schema*, which defines properties like `name`, `decimals`, `description`, `image`, `properties`, `localization`, etc.

Besides, as the world’s largest NFT marketplace nowadays, OpenSea defines their own *Metadata Standards*, including a few more properties like `image_data`, `external_url`, `attributes`, `background_color`, `animation_url`, `youtube_url`, etc. This standard is de facto respected and followed by other NFT marketplaces like LooksRare.

Apparently, none of these standards conveys storage information about the mime type asset that NFT token actually represents. This proposal is an effort to fill the missing part.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

In addition to the existing properties, the Metadata JSON file returned by **ERC721** and **ERC1155** smart contracts (via `tokenURI` and `uri` methods, respectively), should OPTIONALLY contains one more `dStorage` property.

For **ERC721** smart contracts, the Metadata JSON file schema is:

```json
{
    "title": "Asset Metadata",
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
        "dStorage": {
            "type": "object",
            "required": ["platform", "description", "persistence_mechanism", "challenge_mechanism", "consensus", "dstorage_note"],
            "properties": {
                "platform": {
                    "type": "string",
                    "description": "dStorage platform name like Swarm, Arweave, Filecoin, Crust, etc"
                },
                "description": {
                    "type": "string",
                    "description": "A brief description of the dStorage platform"
                },
                "persistence_mechanism": {
                    "type": "string",
                    "description": "Persistence mechanism or incentive structure of the dStorage platform, like 'blockchain-based', 'contract-based', etc"
                },
                "challenge_mechanism": {
                    "type": "string",
                    "description": "Challenge mechanism of the dStorage platform, like Arweave's proof-of-access, etc"
                },
                "consensus": {
                    "type": "string",
                    "description": "Consensus mechanism of the dStorage platform, like PoW, PoS, etc"
                },
                "dstorage_note": {
                    "type": "string",
                    "description": "A note to prove the storage of the NFT asset on the dStorage platform, like a Filecoin deal id, a Crust place_storage_order transaction hash, etc"
                }
            }
        }
    }
}
```

For **ERC1155** smart contracts, the Metadata JSON file schema is:

```json
{
    "title": "Token Metadata",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Identifies the asset to which this token represents",
        },
        "decimals": {
            "type": "integer",
            "description": "The number of decimal places that the token amount should display - e.g. 18, means to divide the token amount by 1000000000000000000 to get its user representation."
        },
        "description": {
            "type": "string",
            "description": "Describes the asset to which this token represents"
        },
        "image": {
            "type": "string",
            "description": "A URI pointing to a resource with mime type image/* representing the asset to which this token represents. Consider making any images at a width between 320 and 1080 pixels and aspect ratio between 1.91:1 and 4:5 inclusive."
        },
        "properties": {
            "type": "object",
            "description": "Arbitrary properties. Values may be strings, numbers, object or arrays.",
        },
        "localization": {
            "type": "object",
            "required": ["uri", "default", "locales"],
            "properties": {
                "uri": {
                    "type": "string",
                    "description": "The URI pattern to fetch localized data from. This URI should contain the substring `{locale}` which will be replaced with the appropriate locale value before sending the request."
                },
                "default": {
                    "type": "string",
                    "description": "The locale of the default data within the base JSON"
                },
                "locales": {
                    "type": "array",
                    "description": "The list of locales for which data is available. These locales should conform to those defined in the Unicode Common Locale Data Repository (http://cldr.unicode.org/)."
                }
            }
        },
        "dStorage": {
            "type": "object",
            "required": ["platform", "description", "persistence_mechanism", "challenge_mechanism", "consensus", "dstorage_note"],
            "properties": {
                "platform": {
                    "type": "string",
                    "description": "dStorage platform name like Swarm, Arweave, Filecoin, Crust, etc"
                },
                "description": {
                    "type": "string",
                    "description": "A brief description of the dStorage platform"
                },
                "persistence_mechanism": {
                    "type": "string",
                    "description": "Persistence mechanism or incentive structure of the dStorage platform, like 'blockchain-based', 'contract-based', etc"
                },
                "challenge_mechanism": {
                    "type": "string",
                    "description": "Challenge mechanism of the dStorage platform, like Arweave's proof-of-access, etc"
                },
                "consensus": {
                    "type": "string",
                    "description": "Consensus mechanism of the dStorage platform, like PoW, PoS, etc"
                },
                "dstorage_note": {
                    "type": "string",
                    "description": "A note to prove the storage of the NFT asset on the dStorage platform, like a Filecoin deal id, a Crust place_storage_order transaction hash, etc"
                }
            }
        }
    }
}
```

An example of an **ERC721** NFT asset Metadata JSON file follows. The `dStorage` property contains information about how the NFT asset is stored on Crust Network, which can be verified on [IPFS SCAN](https://ipfs-scan.io?cid=QmVvigK7jfLyHcDjnNYr2mAReFW9FCFWf41UNB9tbK8rWw).

```json
{
	"name": "LAND (13, -86)",
	"description": "A LAND is a digital piece of real estate in The Sandbox metaverse that players can buy to build experiences on top of",
	"image": "ipfs://QmVvigK7jfLyHcDjnNYr2mAReFW9FCFWf41UNB9tbK8rWw",
	"dStorage": {
		"platform": "Crust",
		"description": "Crust Network, the Incentive Layer of IPFS",
		"persistence_mechanism": "contract-based",
		"challenge_mechanism": "mpow",
		"consensus": "gpos",
		"dstorage_note": "0x466ab180124de1718d30cd2e018e7fe013a07c4860674110ccd13e97eb31ae16"
	}
}
```

## Rationale

### Choice between Interface and JSON Schema Extension

A smart contract interface like `NFTdStorageMetadata` would require extra implementation, which is detrimental to the standard adoption, especially for NFT projects that already have their NFT smart contracts finalized and deployed. By contrast, an optional JSON schema extension is noninvasive, and more easily to be adopted.

# Backwards Compatibility

This EIP is backward compatible with EIP-721 and EIP-1155.

## Security Considerations

There are no security considerations related directly to the implementation of this standard.

## Copyright

Copyright and related rights waived via [CC0](https://eips.ethereum.org/LICENSE).

## Replies

**pangwa** (2022-09-09):

Nice proposal to adapt [ethereum dencentralized storage](https://ethereum.org/en/developers/docs/storage/) to the nft metadata!

---

**gavfu** (2022-09-10):

Right, [Ethereum Decentralized Storage](https://ethereum.org/en/developers/docs/storage/) is indeed an inspiration for this EIP proposal.

Let me elaborate a bit more why a simple `ipfs://xxx` or `arweave://xxx` URL is not enough to attest to *Decentralized Storage*.

Firstly, I would point out a fact that: **IPFS does not have built-in incentive mechanism, hence strictly speaking, IPFS storage does not mean Decentralized Storage.** Say, if an NFT asset is stored on some IPFS nodes operated by a single company or organization, that asset will be inaccessible or even lost, if these IPFS nodes are shutdown. This is why we need some IPFS incentive protocols like Crust and Filecoin.

Secondly, even if the NFT asset is stored on some Decentralized Storage platforms like Arweave, Filecoin or Crust, we still need some information to verify the storage. This is what `dstorage_note` comes for. It could be an Arweave tx, Filecoin deal id, Crust place_storage_order tx, pinning job id of some *IPFS pinning service* like Pinata, etc. NFT marketplace could display `dstorage_note` on NFT asset page as some value certificate for potential buys.

---

**gavfu** (2023-01-28):

BTW, this EIP is already supported by some Web3 storage products like W3Bucket. Here are some links for reference:

DAPP: [Cloud3.cc](https://cloud3.cc/#/buckets)

Documentation: [Cloud3 Documentation](https://docs.cloud3.cc/w3bucket/nftmetadata)

Also as a real example, metadata URI of token 1000010 (https://opensea.io/assets/ethereum/0x587ad7a26c5acae69d683fe923fd3f5b0700f3ef/1000010) is: https://ipfs.io/ipfs/QmaErntVy9NUZBvZFRxvyrrvjFVSxvPkhoZ2z4h4dmjrVB

```json
{
  "name": "W3BKT (10 GB, syc6x3, 0)",
  "image": "ipfs://QmSt7vra39Jk22kQxFACU89oSy6Txwwneu28YjR9pGjP47",
  "dStorage": {
    "platform": "Crust",
    "consensus": "gpos",
    "description": "Crust Network, the Incentive Layer of IPFS",
    "dstorage_note": "0x74aba8278c5da98d3fb9651d7fb1c795bdc79181572f862225083ebecb8a025b",
    "challenge_mechanism": "mpow",
    "persistence_mechanism": "contract-based"
  },
  "attributes": [
    {
      "value": "Crust",
      "trait_type": "dStorage Platform"
    },
    {
      "value": "1",
      "trait_type": "Edition"
    },
    {
      "value": "10",
      "trait_type": "Capacity (GB)"
    }
  ],
  "description": "This is a W3Bucket NFT (W3BKT). You are guaranteed with decentralized, immutable and timeless IPFS storage by Cloud3.",
  "external_url": "https://ipfs-scan.io?cid=QmSt7vra39Jk22kQxFACU89oSy6Txwwneu28YjR9pGjP47",
  "file_history": "ipns://k51qzi5uqu5dhhamqzf86gsb2hiltegehn35m77f6g6m4zntueopt30psyc6x3"
}
```

---

**tmoindustries** (2023-05-10):

Could this support JSON-LD as well? [@gavfu](/u/gavfu)

---

**tmoindustries** (2023-05-28):

Any update on this?  We have IRL use case.

---

**gavfu** (2023-07-06):

Thanks for the suggestion. Technically, we could. But the ‘dStorage’ property aims to be an extension to the existing EIP-721 and EIP-1155 NFT metadata JSON schema, which itself does not support JSON-LD at the first place.

Using JSON-LD in the ‘dStorage’ extension would introduce unnecessary complexity, and require more effort for crypto wallets or NFT marketplaces to parse the ‘dStorage’ property.

Based on that, I still prefer plain JSON to ease the adoption of this extension.

---

**yoheinishikubo** (2023-07-06):

Although I haven’t seen this thread, I did post a metadata-extension proposal including JSON-LD.

“Including” means any data can be added with its schema in the proposal definition.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoheinishikubo/48/9939_2.png)
    [EIP-7280: NFT Metadata Extension like JSON-LD](https://ethereum-magicians.org/t/eip-7280-nft-metadata-extension-like-json-ld/14935) [Tokens](/c/tokens/18)



> I am now working with an airline company to mint NFTs as proofs of carbon-offset flights and trying to expand the project to all companies in the industry.
> In terms of the nature of blockchains, we would like to have a long-living and flexible standard for semantic data structure with metadata of NFTs to be used from computers.
> On the other hand, I think the basic concept for metadata of NFT should be free.
> I found this agenda is like the relationship among HTML and JSON-LD.
> So, I designed a…

