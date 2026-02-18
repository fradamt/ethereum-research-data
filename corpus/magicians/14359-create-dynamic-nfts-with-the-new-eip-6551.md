---
source: magicians
topic_id: 14359
title: Create dynamic NFTs with the new EIP-6551
author: lughino
date: "2023-05-19"
category: Magicians > Primordial Soup
tags: [nft, token, erc-721, erc-6551]
url: https://ethereum-magicians.org/t/create-dynamic-nfts-with-the-new-eip-6551/14359
views: 2140
likes: 7
posts_count: 11
---

# Create dynamic NFTs with the new EIP-6551

Following the good suggestion in [this thread](https://ethereum-magicians.org/t/erc-6551-non-fungible-token-bound-accounts/13030/112), I would like to create a project with NFTs that change dynamically based on the accessories owned by a bound account.

Reading the EIP-6551 proposal, I think it fits the use case well, even if it may not be highly relevant to the question itself.

An example of the use-case:

A user own an NFT which has an image attached to it. The user can buy different accessories (which are other NTFs). When an accessory is acquired and inside the bound account, the NFT should dynamically change with another image that contains the accessory (like a character that can wear several accessories, like hats, glasses, etc.)

What would be the way to implement this use case?

I’ve seen different ways but I could not really connect the dots and find a good way to implement this.

I would definitely prefer on-chains solutions as they would be more transparent and more efficient. Relying on personal servers off-chain could be perceived as an obstacle for some.

I would be happy to go with off-chain solutions if they are better, though.

Appreciate any feedback

## Replies

**abcoathup** (2023-05-19):

You could use [ERC-4883: Composable SVG NFT](https://eips.ethereum.org/EIPS/eip-4883) to compose NFTs with accessories.

Current NFTs implementing ERC4883 have the parent NFT as the holder of the accessory.




      [OpenSea](https://opensea.io/assets/optimism/0x37e2c6400214ae49339f2befab1abf3dd39b2b74/24)



    ![image](https://openseauserdata.com/files/7f3cd7d23dc762ba62aff4aab9136c4e.svg)

###



Loogie Tank

---

**MidnightLightning** (2023-05-20):

The MoonCatRescue project has an infrastructure that is doing something like that (which I helped develop). The MoonCatRescue project predates the ERC721 standard, but there is a wrapper contract at `0xc3f733ca98E0daD0386979Eb96fb1722A1A05E69` which wraps MoonCats into ERC721-compatible tokens (in-lore, those MoonCats are “acclimated” to life on the blockchain, and can participate in other ERC721-compatible projects). MoonCats that are acclimated then can visit [The Boutique](https://boutique.mooncat.community/) and buy additional accessories to wear.

The Boutique is powered by the contract at `0x8d33303023723dE93b213da4EB53bE890e747C63`, which is not ERC6551-compatible, but for paralleling your idea, fills that role. The Accessories contract is a custom contract, but it is possible to tell how many accessories a MoonCat owns by calling `balanceOf(uint256)`, and then use the `AccessoriesByMoonCat(uint256, uint256)` function to iterate through them (first argument is the MoonCat’s token ID, second argument is the zero-based index of their purchased Accessories). To tell what the Accessory itself looks like, the `accessoryImageData` and `accessoryInfo` functions give that (they’re stored on-chain as PNG-formatted pixel art).

So, putting all that together, there’s a contract at `0x91CF36c92fEb5c11D3F5fe3e8b9e212f7472Ec14` that is an example of what you’re aiming to do: That contract (`MoonCatAccessoryImages`) has an `accessorizedImageOf(uint256)` function that if you put in a MoonCat’s token ID (you can use “1289” to get my main avatar MoonCat) you get out an SVG that has several “layers” (`<g>` groups in the SVG code) to it. The base layer is the MoonCat itself, and then because my MoonCat is currently wearing three Accessories (a visor, a bowtie, and a vehicle), there’s three `<image href="data:image/png;base64...` embeds that are the PNG-formatted Accessories.

[![1289](https://ethereum-magicians.org/uploads/default/original/2X/2/2d91533f4720b633fcead65abfd20f684fe2af03.png)1289340×315 20.5 KB](https://ethereum-magicians.org/uploads/default/2d91533f4720b633fcead65abfd20f684fe2af03)

This is done on-chain in the contract by querying the Accessories contract for which Accessories are owned by that MoonCat, generating PNG data for each owned Accessory, creating a data-URL style tag for embedding each in an SVG and returning it. The code for that contract is posted [on Etherscan](https://etherscan.io/address/0x91CF36c92fEb5c11D3F5fe3e8b9e212f7472Ec14#code) if you want to peruse the Solidity behind it.

You could take this one step further and have the contract wrap that SVG in a JSON object that is the format expected for NFT marketplaces for the `tokenURI` output.

So, to accomplish “on-chain rendering of SVGs of an NFT and any Accessories they own, that change as they buy/activate others” you don’t *need* to use any standards, but if your “Accessories” are ERC721-style tokens in ERC6551 token-owned accounts, if your Accessories contract uses enumerable metadata (`tokenOfOwnerByIndex` or similar), you can use that to figure out which Accessories a given token owns pretty easily.

If you’re interested in learning more about how we accomplished storing the Accessory appearances themselves on-chain, I did a writeup on that [in a Reddit post](https://www.reddit.com/r/MoonCatRescue/comments/pl5nxw/mooncat_accessories_image_storage_and_access_on/).

---

**stoicdev0** (2023-05-31):

Have you seen [ERC-6220: Composable NFTs utilizing Equippable Parts](https://eips.ethereum.org/EIPS/eip-6220)?

It fits exactly what you are describing. You can define the equipping conditions and equip nested NFTs (it uses [ERC-6059: Parent-Governed Nestable Non-Fungible Tokens](https://eips.ethereum.org/EIPS/eip-6059) for nesting).

No need to change metadata, since it uses [ERC-5773: Context-Dependent Multi-Asset Tokens](https://eips.ethereum.org/EIPS/eip-5773), which lets you have multiple assets on the same NFT, you can have for instance a full view one and an equipped version.

This can work with any collection which implements the interfaces so it is really dynamic and forward compatible. The 3 mentioned ERCs are already on final status.

---

**lughino** (2023-05-31):

Hi all,

Thank you for all your suggestions, I’m definitely learning a lot!

[@abcoathup](/u/abcoathup) and [@MidnightLightning](/u/midnightlightning) unfortunately, it seems that your approach is based on SVG image composition. It doesn’t work in my use-case as the images should be real subjects, so ideally a PNG or similar.

Thanks [@stoicdev0](/u/stoicdev0) for the suggestion! This one seems to be the right direction.

Although, it is not clear to me how I can visualise the right NFT without changing the metadata?

Or is this something that wallets/platforms have to support? Like, is OpenSea supporting the ERC mentioned? So I can see the current NFT that reflects the accessories enabled?

Another question, can I use images like PNGs? The subjects are real so I have different images depending on the accessory enabled.

---

**stoicdev0** (2023-05-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lughino/48/9515_2.png) lughino:

> it is not clear to me how I can visualise the right NFT without changing the metadata?

You can add multiple images to your NFT, thanks to ERC-5773. You make the full render image the main one so it shows in marketplaces and others. Then you would configure the equipped version (which would be smaller and located at the right place) to be equippable into the parent at some specific slot, so only that one can be used.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lughino/48/9515_2.png) lughino:

> is this something that wallets/platforms have to support? Like, is OpenSea supporting the ERC mentioned? So I can see the current NFT that reflects the accessories enabled?

The ERC includes methods and events so you can compose the final image. We have an npm package with a working implementation and some utils to make the rendering easier. You can check the docs here: https://evm.rmrk.app/  it is open source.

About support, yes, we expect wallets and marketplaces to eventually support these ERCs for dynamic NFTs.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lughino/48/9515_2.png) lughino:

> Another question, can I use images like PNGs? The subjects are real so I have different images depending on the accessory enabled.

Yes, I have worked on collections using this ERC which are composed with PNGs. They can really be anything. A good example is audio, you could have a track NFT which is the parent, and send and equip different sounds to it.

---

**stoicdev0** (2023-05-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lughino/48/9515_2.png) lughino:

> The subjects are real so I have different images depending on the accessory enabled.

I just noticed this. With ERC-6220 you do not need to create images for each of the combinations. Just 2 versions of each asset, one for full render and one for when it is equipped. Following the protocol should produce the right output.

---

**lughino** (2023-05-31):

Thank you very much [@stoicdev0](/u/stoicdev0) for all the info.

I’m going to play with RMRK soon.

---

**MidnightLightning** (2023-06-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lughino/48/9515_2.png) lughino:

> it seems that your approach is based on SVG image composition. It doesn’t work in my use-case as the images should be real subjects, so ideally a PNG or similar.

My example is layering PNGs (the accessories). It uses SVG as an image language to build up the layers and compose the image (otherwise Solidity would need to do pixel-by-pixel comparison/logic). This means the output is an SVG made up of embedded PNGs; does your setup require the final composition be a PNG?

---

**tmoindustries** (2024-01-24):

Anyone found a simpler way to render dynamic nft image based on assets / collectibles in its TBA?

This is from May ‘23 and I suspect there may be better/simpler solutions now.

We set up a gif on IPFS that then adds metadata to the image and renders as a svg. It renders and serves fine but then OpenSea and Rarible etc are blocking the final image.

---

**abcoathup** (2024-01-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tmoindustries/48/7602_2.png) tmoindustries:

> Anyone found a simpler way to render dynamic nft image

EIP4883: [ERC-4883: Composable SVG NFT](https://eips.ethereum.org/EIPS/eip-4883)

Check out multiple ERC4883 projects floating in a Loogie tank:




      [OpenSea](https://opensea.io/assets/optimism/0x37e2c6400214ae49339f2befab1abf3dd39b2b74/24)



    ![image](https://openseauserdata.com/files/7f3cd7d23dc762ba62aff4aab9136c4e.svg)

###



Loogie Tank

