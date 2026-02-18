---
source: magicians
topic_id: 10715
title: A way to verify NFT authenticity given an author/artist public key
author: jsousa10
date: "2022-09-07"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/a-way-to-verify-nft-authenticity-given-an-author-artist-public-key/10715
views: 537
likes: 0
posts_count: 1
---

# A way to verify NFT authenticity given an author/artist public key

Question to community: should this idea be promoted to draft?

---

## eip:
title: Authentic NFT
author: João Sousa ()
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2020-08-25
requires (*optional): <EIP number(s)>

## Simple Summary

A standardized way to associate non-fungible tokens (NFTs) with digital assets, in a way that the NFT/asset pair can’t be replicated. Assets are digitally sign by authors/artists. Given an author/artist public key, the authenticity of a NFT can be verified.

## Abstract

NFTs are identified by a contract address and by a tokenId. This pair is unique. We call this pair the NFT id. NFT ids are known in advance, before creating the NFTs.

Following this standard, before creating NFT_1, author/artist Alice includes NFT_1 id in the digital asset asset_1, and digitally signs it using her private key, detaching the signature file signature_1. NFT_1 is associated with asset_1, but also with signature_1, through the NFT_1 metadata. NFT_1 is created.

Alice announces her new content/masterpiece NFT_1 by publishing asset_1. She also publishes her public key.

Author/artist Mallory creates NFT_2 with the same metadata of NFT_1. NFT_2 becomes associated with asset_1, and also with signature_1.

Before creating NFT_3, author/artist Mallory creates asset_3 by modifying asset_1 in order replace NFT_1 id by NFT_3 id. NFT_3 is associated with asset_3, and with signature_1, through the NFT_3 metadata. NFT_3 is created.

Before creating NFT_4, author/artist Mallory creates asset_4 by modifying asset_1 in order replace NFT_1 id by NFT_4 id. Given that Mallory has no access to Alice private key, which is necessary to sign, Mallory digitally signs asset_4 with his own private key, detaching the signature file signature_4. NFT_4 is associated with asset_4, and with signature_4, through the NFT_4 metadata. NFT_4 is created.

Mallory announces Alice’s new content/masterpieces NFT_2 and NFT_3 by publishing asset_2 and asset_3 and Alice’s public key.

Mallory announces Alice’s new content/masterpiece NFT_4 by publishing asset_4 and he also publishes his own public key as being Alice’s public key.

Victor uses trusted sources to obtain public keys. He gets Alice’s true key from these sources. Not the one published by Mallory.

Given Alice’s true public key, Victor verifies the authenticity of the four NFTs created:

- asset_1 contains NFT_1 id, and signature_1 is a valid signature of asset_1 made by Alice. Therefore, NFT_1 is an Alice’s authentic NFT.
- asset_2 does not contains NFT_2 id (NFT ids are unique). Therefore NFT_2 is not an Alice’s authentic NFT.
- asset_3 contains NFT_3 id. But signature_1 is not a valid signature of asset_3 made by Alice. Therefore NFT_3 is not an Alice’s authentic NFT.
- asset_4 contains NFT_4 id. But signature_4 is not a valid signature of asset_4 made by Alice. Therefore NFT_4 is not an Alice’s authentic NFT.

Given Alice’s public key, following this standard, all replicas of Alice NFTs created by Mallory are spotted as non authentic.

## Motivation

NFTs are identified by a contract address and a tokenID, the NFT id. NFTs can be associated with a digital asset through a tokenURI. Nothing prevents several NFTs to be associated to the same digital asset. All they need is to use the same tokenURI. This contributes to the proliferation of large numbers of NFTs associated with the assets of famous or new NFTs. Distinguishing a particular NFT becomes a really difficult task which contributes to lower the confidence in the NFTs ecosystem.

The goal of this standard is to stop the possibility of creating more than one NFT associated to the same digital asset. This is accomplished by including the NFT id in the associated asset and having the asset being digitally signed by its author/artist. Given the author/artist public key the authenticity of his/her NFTs can be verified.

Digital content authors/artists can resort to existing NFT creation services, in order to create the NFTs associated with the digital assets they created. The services have their own contracts for creating NFTs. Under this setup, the NFTs that authors/artists create are identified by a contract address and a tokenID that have nothing to do with the authors/artists themselves. They are related to the services that the authors/artists used to create their NFTs. Although there is nothing wrong with this mechanism, it moves the identification of the authorship of the NFT from the asset authors/artists to the services used to create the NFTs. In the world of painting, this would be the same as identifying a Picasso painting not by the painting itself and the Picasso signature, but by the canvas supplier Picasso used, and the canvas serial number of the canvas that that supplier sold to Picasso.

In this standard author/artist Alice resorts to an existing NFT creation service, in order to create authentic NFT_1 associated with digital asset asset_1, she created (the service supplies the NFT id it will use, so that Alice can include it in asset_1). NFT_1 is created. Alice announces her new asset possibly by using a copy of asset_1. Victor grabs NFT_1 id from asset_1 copy. Victor gets asset_1 and signature_1 from NFT_1 metadata. Victor gets Alice’s public key from trusted sources. Victor verifies NFT_1 authenticity by checking:

1. that the NFT_1 contract address and tokenID match the ones in asset_1;
2. that signature_1 is a valid Alice signature of asset_1.

If this two conditions are met, NFT_1 is an Alice’s authentic NFT.

Note that authenticity of an NFT is always verified against an author/artist public key. An authentic NFT is always authentic regarding one author/artist and non authentic regarding all the others.

In this standard the identification of a NFT associated with a digital asset is shifted from the NFT contract address and the NFT tokenID, to the asset itself, and the asset author/artist identification, through the author/artist public key. Returning again the world of painting, this is similar to identifying a painting by the painting itself and the painter’s signature, which is the common way. No paintings are identified by canvas supplier and canvas serial number.

This standard solves the problem of the proliferation of huge numbers of replicas of famous or new NFTs that are flooding the NTFs ecosystem. Digital content authors/artists interested in creating NFTs associated with their artworks, will benefit from this standard as the creation of NFT replicas of their exact assets are easily spotted as non authentic. Ultimately the NFTs ecosystem will benefit too.

This standard considers the image associated with an NFT only a graphical representation of the digital asset. This image is typically used by applications to show the NFT. By doing this separation it allows the digital asset to be a digital content of any format. It is not limited to images. It can be for example a pdf document or a text plain file, like this one, among all other existing formats. This allows the NFTs to be adopted as a mechanism for publishing scientific papers, source code or standards, for example.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

Compliant Authentic NFTs must implement ERC721Metadata interface and must extend the ERC721 Metadata JSON Schema with all the fields in the following JSON Schema:

```json
{
    "image": "A string with an URI pointing to a resource, with mime type image/*, representing the asset this NFT is associated to.",
    "media_file": "A string with an URI pointing to a resource, with any mime type. This resource is the asset associated with this NFT.",
    "authentic_nft": {
	"version": "A string with the authentic NFT schema version used in this NFT.",
	"digital_signature_type": "A string with the signature type used to sign the image and the media file.",
        "image_signature": "A string with an URI pointing to a resource, with mime type text/plain. This resource is the image signature made by the author/artist.",
        "media_file_signature": "A string with an URI pointing to a resource, with mime type text/plain. This resource is the media file signature made by the author/artist."
    }
}
```

Resources pointed by the “image” and “media_file” fields, of the above JSON Schema, of compliant Authentic NFTs must include the following three fields in their content:

ANFT-Blockchain-Identifier:

ANFT-Contract-Address:

ANFT-Token-Identifier:

The field “ANFT-Blockchain-Identifier:” must be followed by a blockchain identifier. No spaces after the “:” are allowed. In case of the Ethereum blockchain the identifier is “ethereum”.

The field “ANFT-Contract-Address:” must be followed by a contract address. No spaces after the “:” are allowed.

The field “ANFT-Token-Identifier:” must be followed by a tokenId number. No spaces after the “:” are allowed.

In case of resource formats that support metadata, the inclusion of this three fields must be done in the metadata. The metadata “Comment” field is recommended. Optionally they can also be included in the media content itself, in a human-readable way.

In case of resource formats that do not support metadata, the inclusion of this three fields must be done explicitly, in plain text.

## Rationale

This standard exclusively relies on NFT metadata information and on information in the associated image and media file. Nothing is required regarding smart contracts, which contributes to be a light easily implemented standard.

Besides the image that represents the asset associated to the NFT a media file is added as being the asset itself. This separation allows the creation of NFTs associated with all the variety of existing media files. In case of an image asset, the image cab be a low resolution preview version of the asset in the media file. The media file will contain the full resolution image that constitutes the NFT asset.

The prefix “ANFT”, in the ANFT fields, is the Authentic Non-Fungible Token acronym.

The image associated with the NFT is considered an authentic content just like the media file. For this reason both the image and the media file must have the three ANFT fields, and both of them must be signed by the authors/artist. For this reason both signatures are included in the NFT metadata.

The ANFT fields must be included in the resources either in the metadata or explicitly in plain text to allow for automated verification of authenticity.

The version field is included in the NFT metadata allowing the accommodation of future requirements is subsequent versions of this standard. This document refers to version “1.0”.

The signature type is included in the NFT metadata to allow the usage of different types of signatures schemas, ranging from the wallet signature, to OpenPGP or the schemas used in a variety of citizen cards, for example, those from European countries. A natural choice would be to consider the wallet signature type only. However, wallet signatures do not support mechanisms such as revocation certificates which are useful when managing identities of authors/artists.

The “ANFT-Blockchain-Identifier:” was included to allow this standard to be implemented in other blockchais without the necessity of copy/adapt it. Just like ethereum standards using RFC 2119 without the need to copy/adapt it.

## Backwards Compatibility

Not applicable.

## Test Cases

Not applicable.

Test cases for an implementation are mandatory for EIPs that are affecting consensus changes.  If the test suite is too large to reasonably be included inline, then consider adding it as one or more files in `../assets/eip-####/`.

## Reference Implementation

To be added.

## Security Considerations

Following this standard NFT authenticity verification resembles to obtaining true authors/artists public keys from trusted sources. If Mallory is able to forge

Alice’s public key then he can replicate all Alice’s NFT and the replicas will be considered Mallory’s authentic NFTs. This is a consequence on identity theft. And the identity theft avoidance is outside the scope of this standard.

## Copyright

Copyright and related rights waived via CC0.
