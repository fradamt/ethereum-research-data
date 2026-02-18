---
source: magicians
topic_id: 8746
title: EIP-4955 Non-Fungible Token Metadata Namespaces Extension
author: 0xnacho
date: "2022-03-29"
category: EIPs
tags: [nft, erc-721, standards-adoption]
url: https://ethereum-magicians.org/t/eip-4955-non-fungible-token-metadata-namespaces-extension/8746
views: 2804
likes: 2
posts_count: 7
---

# EIP-4955 Non-Fungible Token Metadata Namespaces Extension

Hi folks! how are you?

I have written this [EIP-4955](https://github.com/ethereum/EIPs/pull/4955)

I propose an extension to the non-fungible tokens metadata schema to cover the needs that multiple projects have for using custom properties. This will help different projects integrate NFTs

Let me know what you think. I’d like community feedback regarding the best way to set this up for NFT projects.

## Replies

**SamWilsn** (2022-04-05):

I think coming up with a standard for this is probably a good idea, especially if projects are already doing something like it.

That said, I think using the marketplace/app name as a key in the metadata is a really really bad idea. I’d much prefer to see something like [Media Types](https://www.rfc-editor.org/rfc/rfc2046.html) be used as the keys. Maybe something like:

```json
{
    attachments: [
        {
            "id": "model",
            "type": "model/gltf+json",
            "uri": "..."
        },
        {
            "id": "model",
            "type": "model/stl",
            "uri": "..."
        },
        {
            "id": "preview",
            "type": "image/png",
            "uri": "..."
        },
        {
            "id": "preview",
            "type": "image/jpeg",
            "uri": "..."
        },
    ]
}
```

The attachment ids could be standardized in the EIP itself, and projects could choose whichever one matches what they need. In the above example, both `preview` attachments would have the same content, just in a different format.

---

**0xnacho** (2022-04-06):

Thanks for the reply [@SamWilsn](/u/samwilsn)

I agree that company names are not the best takeaway for this, but let me explain why I came up with namespaces:

- Armatures
Every metaverse uses its own armature. There is a standard for humanoids but it is not being used for every metaverse and not all the metaverses use humanoids. For example, Decentraland has a different esthetic than Cryptovoxels and TheSandbox. It means that every metaverse will need a different model and they may have the same extension (GLB, GLTF)

[![Screen Shot 2022-04-06 at 14.24.42](https://ethereum-magicians.org/uploads/default/original/2X/4/4c0c9d1fda4579e97225499d5d1a9c1fd5fda962.jpeg)Screen Shot 2022-04-06 at 14.24.42982×506 52.2 KB](https://ethereum-magicians.org/uploads/default/4c0c9d1fda4579e97225499d5d1a9c1fd5fda962)

- Metadata (Representations Files)

Every metaverse uses its own metadata representation files to make it work inside the engine depending on its game needs.

[This](https://peer.decentraland.org/lambdas/collections/wearables?wearableId=urn:decentraland:matic:collections-v2:0x55a2dd4dadbf0771226fe84c1adf79001b564db7:0) is how a wearable looks like in Decentraland in terms of the config file:

```auto
"data": {
  "replaces": [],
  "hides": [],
  "tags": [],
  "category": "upper_body",
  "representations": [
    {
      "bodyShapes": [
        "urn:decentraland:off-chain:base-avatars:BaseMale"
      ],
      "mainFile": "male/Look6_Tshirt_A.glb",
      "contents": [
        {
          "key": "male/Look6_Tshirt_A.glb",
          "url": "https://peer-ec2.decentraland.org/content/contents/QmX3yMhmx4AvGmyF3CM5ycSQB4F99zXh9rL5GvdxTTcoCR"
        }
      ],
      "overrideHides": [],
      "overrideReplaces": []
    },
    {
      "bodyShapes": [
        "urn:decentraland:off-chain:base-avatars:BaseFemale"
      ],
      "mainFile": "female/Look6_Tshirt_B (1).glb",
      "contents": [
        {
          "key": "female/Look6_Tshirt_B (1).glb",
          "url": "https://peer-ec2.decentraland.org/content/contents/QmcgddP4L8CEKfpJ4cSZhswKownnYnpwEP4eYgTxmFdav8"
        }
      ],
      "overrideHides": [],
      "overrideReplaces": []
    }
  ]
},
"image": "https://peer-ec2.decentraland.org/content/contents/QmPnzQZWAMP4Grnq6phVteLzHeNxdmbRhKuFKqhHyVMqrK",
"thumbnail": "https://peer-ec2.decentraland.org/content/contents/QmcnBFjhyFShGo9gWk2ETbMRDudiX7yjn282djYCAjoMuL",
"metrics": {
  "triangles": 3400,
  "materials": 2,
  "textures": 2,
  "meshes": 2,
  "bodies": 2,
  "entities": 1
}
```

`replaces`, `overrides`, `hides`, and different body shapes representation for the same asset are needed for Decentraland in order to render the 3D asset correctly.

Maybe we can use the `id` from your proposal like `"id": "model;decentraland"`; `"id":"model;cryptovoxels"`, etc and have the `glb`, `gltf`, and `json` types but I think that the `namespaces` approach allow custom key values which are more permissive.

---

**SamWilsn** (2022-04-06):

So first, this is an excellent post, and should go in the rationale section of the EIP!

---

That makes total sense! However, I’m still not a huge fan… I’d like to avoid a situation where another voxel-style game (hypothetically Boxocrypto) comes along, and uses some keys from the `"cryptovoxels"` namespace to bootstrap, and the rest from their `"boxocrypto"` namespace. Since these are all private companies, no one will be policing their implementations ![:rofl:](https://ethereum-magicians.org/images/emoji/twitter/rofl.png?v=12)

How about adding an optional `"tags"` array or dictionary, and making it customary to allow users to choose between assets matching `"id"` and `"type"`? So in the game example, you could have a `voxel` tag (or `“style”: “voxel”), and the game would display a dropdown to choose between them when importing?

---

Is the config file stored off- or on-chain? Can it work with different model files? It could be worthwhile to reach out to these vendors and make an informal working group of sorts to see what would work for everyone.

That said, if the config file *can* work with other assets, maybe something like:

```json
{
    "id": "config",
    "type": "application/vnd.decentraland+json",
    "uri": "..."
}
```

---

In any case, editors are not curators, so if you’re happy to use vendor names as namespaces, go for it!

---

**0xnacho** (2022-04-13):

Sorry for the delay on this Sam, I appreciate the ideas and time you are investing here.

The config file can be stored off- or on-chain but I imagine it mostly off-chain being resolved by a URI set as the token URI `tokenURI(tokenId)`.

I get your point of using having it inside `type` or `style` and I like the idea, however, thinking in terms of how this will work from the URI resolution, you will end up having a lot of different entries with the same `id`/`type` which will make hard for the metaverse to parse it and get the right models/files:

```auto
{
    "id": "model",
    "type": "model/gltf+json",
    "style": "metaverse1;newMetaverse2",
    "uri": "..."
},
{
    "id": "model",
    "type": "model/gltf+json",
    "style": "decentraland",
    "uri": "..."
},
{
    "id": "model",
    "type": "model/gltf+json",
    "style": "thesandbox;cryptovoxels",
    "uri": "..."
},
{
    "id": "config",
    "type": "application/vnd.metaverse1+json",
    "uri": "..."
},
{
    "id": "config",
    "type": "application/vnd.decentraland+json",
    "uri": "..."
}
```

If you are metaverse1, you will need to look for **all** of the entries and keep the ones that match you. If we use `vendors` or `namespaces` you will do `namespaces.metaverse1.model` and that’s all. It is easier and more performant rather than looking blindly through all the entries.

Am I misunderstanding something from your proposal?

---

**SamWilsn** (2022-04-14):

I think you have the gist of my suggestion, except that the `"style"` value should be human readable, and that the vendors would let their *users* choose any entry matching the `"type"` they support.

---

**kennedybaird** (2022-12-13):

I support it as it stands, I think that the concern about using company names is moot due to assets being easily replicated.

Using namespaces directly connecting to specific platforms would be the most user-friendly approach, encouraging metadata to remain layman readable as well.

Thanks for this EIP [@0xnacho](/u/0xnacho) - I think it has great usecases

