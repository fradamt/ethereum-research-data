---
source: magicians
topic_id: 9819
title: "IDEA : a new standard for 360° NFTs - equirectangular format"
author: Natural_Warp
date: "2022-07-01"
category: EIPs
tags: [nft, equirectangular, "360"]
url: https://ethereum-magicians.org/t/idea-a-new-standard-for-360-nfts-equirectangular-format/9819
views: 969
likes: 2
posts_count: 4
---

# IDEA : a new standard for 360° NFTs - equirectangular format

The main idea is to create a standard which enables the use of 360° images / 360° photos :

- to be rendered across marketplace platforms in a panorama viewer / 360 photo viewer format
- to be used interoperable as a volumetric portal sphere in virtual reality games
- to be uploaded and tokenized as such interoperable / compatible 360NFT

2 main problems :

- a huge amount of platforms ( for NFT creation / collection ) are not ready to display a photosphere.
- many 3D / VR spaces do have the ability to show volumetric 360° spheres but there is no agreed standard to recognize whether a .jpg NFT contains the “equirectangular” metadata or not.

An experimental solution for now was the agreement between KnownOrigin, Somnium Space VR and Natural Warp where a JSON freetext ( simple to add / simple to read ) was added to recognize the format.

The result of this collab is that since March 2021 artists can upload 360° artworks ( 2:1 ratio .jpgs with the equirectangular metadata / exif tags ) on the Knownorigin platform and that collectors with such NFT in their wallets can use it in Somnium Space directly as a 3D asset.

Here you can see the result of this collaboration :

[![360-NFT-gallery-up](https://ethereum-magicians.org/uploads/default/optimized/2X/0/07f9eaf3378e9cb49ad5b73629c6275e708cb1a9_2_690x388.jpeg)360-NFT-gallery-up1920×1080 184 KB](https://ethereum-magicians.org/uploads/default/07f9eaf3378e9cb49ad5b73629c6275e708cb1a9)

The WEB VR venue showcasing these 360NFTs : [Somnium Space WEB - Parcel #752](https://somniumspace.com/parcel/752)

The 360NFT collection at KnownOrigin : [KnownOrigin](https://knownorigin.io/natural-warp)

Since this is an advice seeking thread and this is basically where we’re at - any help of EIP wizards would be greatly appreciated ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=15)

## Replies

**Natural_Warp** (2022-07-08):

So it looks like the ball finally started rolling.

Apparently Superrare and Transientlabs managed to launch an artist with 360 photography.



      [twitter.com](https://twitter.com/tylekki/status/1545139051384160259)





####

[@tylekki](https://twitter.com/tylekki/status/1545139051384160259)

  WE ARE LIVE!!!  @SuperRare

The first 360 Virtual Reality NFT.
Thanks to @TransientLabs

I’m beyond excited to present LOMA BLANCA from my genesis series VERTIGO

For the full screen immersive interactive experience and to view in VR. ⬇️

https://t.co/FiMlVwEAXZ

  https://twitter.com/tylekki/status/1545139051384160259










but the JSON isn’t in sync with the #360NFTs created on KnownOrigin so they are interoperable with SomniumSpace VR.

Hence the obvious need for an EIP standard on 360 NFT creation so they can be fully utilized in VR spaces.

---

**Natural_Warp** (2022-07-08):

[twitter.com](https://twitter.com/Natural_Warp/status/1545321850485481474)





####

[@](https://twitter.com/Natural_Warp/status/1545321850485481474)

  @SuperRare @TransientLabs @tylekki Hi @SuperRare awesome to see you added the 360° functionality on your platform

But it is not the first

March 6th 2021 we released the first true #360NFT minted on @KnownOrigin_io with utility in @SomniumSpace #VR

Let's get this in 360 format in sync !
https://t.co/pzEMQy5S2P

  https://twitter.com/Natural_Warp/status/1545321850485481474

---

**stoicdev0** (2023-03-06):

You might be interested in taking a look into [ERC-5773](https://eips.ethereum.org/EIPS/eip-5773). It’s an extension to 721 which adds the capability to NFTs of having multiple assets. So you can have a simple image representing the sphere for marketplaces, and add other assets with the actual sphere (or anything else). Depending on where it’s being showed it can load different assets.

It also gives you forward compatibility since you can later add new assets to the same NFTs, say with a newer version or to make it compatible with another software or metaverse.

