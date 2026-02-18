---
source: magicians
topic_id: 8765
title: "ERC-4883: Composable SVG NFT"
author: AlexPartyPanda
date: "2022-03-31"
category: ERCs
tags: [nft, token, graphics]
url: https://ethereum-magicians.org/t/erc-4883-composable-svg-nft/8765
views: 4902
likes: 24
posts_count: 19
---

# ERC-4883: Composable SVG NFT

## EIP-4883 Composable SVG NFT

Discussion for [EIP-4883](https://github.com/ethereum/EIPs/pull/4888/files)

NFT has public render function returning SVG body that can be composed.

SVG specification Rendering model: [SVG 1.1 specification section 3](https://w3.org/TR/SVG11/render.html)

### Implementations

Implementations of composable SVGs:

- Fancy Loogies
- Loogie Tank
- Party Panda

#### BuidlGuidl BTF - Composable SVG NFTs demo

Fancy Loogies & Loogie Tanks

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/6/6db725828a0eafc90146ed534cef7fe34cae5f6a.jpeg)](https://www.youtube.com/watch?v=mnErFJwujSg)

#### Loogie Tank


      ![](https://opensea.io/favicon.ico?favicon.beaabd5c.ico)

      [opensea.io](https://opensea.io/item/optimism/0x37e2c6400214ae49339f2befab1abf3dd39b2b74/24)



    ![](https://opensea.io/item/optimism/0x37e2c6400214ae49339f2befab1abf3dd39b2b74/24/opengraph-image?ts=29450589)

###

## Replies

**abcoathup** (2022-04-01):

## Rights

I added that the caller of render must have rights to use the SVG body in a composed SVG.

## Relationships

I haven’t specified how this must be done, so any relationship can be used.

When [@AlexPartyPanda](/u/alexpartypanda) and I first started playing with adding accessories to pfps we had a token holder owning both the pfp and the accessory and creating a link between the two.

FancyLoogies introduced us to that the pfp could be the token holder of the accessory and that a linkage could be setup on transfer.

Need to find wording to describe the two tokens, composer and composee feel a bit clumsy.

---

**SamWilsn** (2022-04-06):

If I am a contract that’s composing together multiple SVGs, I’ll probably know the position and z-index of where I want to put my child SVGs. What scenarios do you envision where the child SVG knows what z-index to render at, but the composer does not?

---

Have you considered using the `link` tag instead of concatenating SVGs on-chain? Would have to more formally describe the URI format, but as a really rough example:

```xml



```

---

**SamWilsn** (2022-04-06):

Two more non-formatting related questions:

Should the optional methods revert if they aren’t supported? Would they be better placed in a separate optional interface?

What units are width and height in?

---

**abcoathup** (2022-04-07):

Great questions [@SamWilsn](/u/samwilsn)  ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)

Need to agree if zindex, width and height are required in the EIP or if a render function is sufficient.

A test was adding Party Pandas and Nouns glasses to a Loogie Tank using only a render function.  Need to dig in if sizing would help here, as currently the elements go out of the tank.

![Party Pandas in a Loogie Tank](https://openseauserdata.com/files/7e01e7e0e19ba84725358fc9a7612e6f.svg)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> What scenarios do you envision where the child SVG knows what z-index to render at, but the composer does not?

In PartyPanda there is permissionless linking, a token holder can add a child SVG NFT that is either a background or an accessory by transferring ownership of the child to the composable NFT.

Though this could be implemented in the child SVG NFT to provide a zindex as part of the transfer, so then it wouldn’t need to be part of the standard.



      [github.com](https://github.com/TeamPartyPanda/party-panda-nft/blob/main/src/ERC721PayableMintableComposableSVG.sol#L167)





####



```sol


1. ) external returns (bytes4) {
2. uint256 tokenId = Bytes.toUint256(idData);
3.
4. if (!_exists(tokenId)) revert NonexistentToken();
5. if (ownerOf[tokenId] != from) revert NotTokenOwner();
6.
7. IERC4883 composableToken = IERC4883(msg.sender);
8. if (!composableToken.supportsInterface(type(IERC4883).interfaceId))
9. revert NotComposableToken();
10.
11. if (composableToken.zIndex()  zIndex) {
19. if (composables[tokenId].foreground.tokenAddress != address(0))
20. revert ForegroundAlreadyAdded();
21. composables[tokenId].foreground = Token(


```










![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Have you considered using the link tag instead of concatenating SVGs on-chain? Would have to more formally describe the URI format, but as a really rough example:

I hadn’t considered using a `link` tag.

Concatenating SVGs on-chain works today, it allows for the child SVG to change based on state, and when combined with the parent holding the child, enforces ownership.

I assume a new URI format would require a huge effort to get adoption, compared with the output of concatenated SVGs working with current browsers. (See the SVG from OpenSea with composable SVGs)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Should the optional methods revert if they aren’t supported? Would they be better placed in a separate optional interface?

The optional methods should be in optional interfaces.

Still need to agree if zindex and size are required in the EIP.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> What units are width and height in?

“For SVG-specific properties, the length unit identifier is optional. If a unit is not provided, the length value represents a distance in the current user coordinate system.”

https://www.w3.org/TR/SVG11/types.html#DataTypeLength

---

**SamWilsn** (2022-04-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> A test was adding Party Pandas and Nouns glasses to a Loogie Tank using only a render function. Need to dig in if sizing would help here, as currently the elements go out of the tank.

Ah! That makes total sense. Otherwise the composer would have to parse the SVG to get the total size. Probably a good example to put in the EIP’s Rationale section!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> Though this could be implemented in the child SVG NFT to provide a zindex as part of the transfer, so then it wouldn’t need to be part of the standard.

Oh, I didn’t mean to imply that there wouldn’t be a z-index in the composer. Just that you’d probably have `setBackground(address, uint256)` and `addAttachment(address, uint256)` in the composer, and those would know what z-index to use, instead of the child only being usable at a single z-index.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> I assume a new URI format would require a huge effort to get adoption, compared with the output of concatenated SVGs working with current browsers. (See the SVG from OpenSea with composable SVGs)

I think this step could be implemented by preprocessing the SVG, and while it would increase the amount of work done off-chain, I think it might be worth while to reduce the amount of work on-chain. For example, this would be super useful to any NFT that currently base64 encodes data on the fly.

That said, I’d be happy with concatenation as well. Just wanted to throw the suggestion out there.

---

**qzhodl** (2022-04-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> I hadn’t considered using a link tag.
>
>
> Concatenating SVGs on-chain works today, it allows for the child SVG to change based on state, and when combined with the parent holding the child, enforces ownership.

Concatenated SVG on-chain will work when the image size is small, and when the pfp image size is big (the image may have more details), the cost of uploading metadata will be very high ([cyberbroker](https://opensea.io/collection/cyberbrokers) used nearly 100 ETH to upload their metadata). Also, the read gas could be very high and may exceed the gas limit.

As [@SamWilsn](/u/samwilsn) said, “link” tag could help by reducing the on-chain image size, but as [@abcoathup](/u/abcoathup) said, opensea compatibility is an issue right now. The SVG image with the image link could not be rendered properly by opensea, it shows an empty image when I tested it on rinkeby (https://testnets.opensea.io/assets/0x618d06a965917794c9df3e5f875ce3a63c6fe250/1)

it seems that there is no perfect tech solution for composable NFT

---

**qzhodl** (2022-05-26):

SVG format has great composability, and it can combine multiple PNG images into an SVG image by smart contracts in a very efficient way. It will release all artists’ creativity by enabling PNG image composability.

The format will be like this:

```auto




```

But the PNG files will consume a lot of storage, so we can either upload them to Ethereum by consuming a lot of gas or use a programmable storage L2  to store the PNG and assemble them according to the state of L1’s NFT.

We have a super cool [demo](https://github.com/iteyelmp/Web3Robot) here and use [Web3Q](https://web3q.io/home.w3q/) as the programmable storage L2 layer.

---

**wighawag** (2022-09-08):

Really cool EIP. Thanks for writing it and building such cool projects!

Just reading it and got a few comments

### A) The EIP should focus on the technical specification only

> If the caller of the render function composes an SVG NFT they must have rights to use the SVG body in a composable SVG.  The token holder could optionally hold both the SVG and rendered SVG NFTs or the token holder could hold the SVG NFT, and the SVG NFT could hold the rendered SVG NFT.

This should not be specified in my opinion and I strongly feel about this, the EIP should focus on the technical spec.

### B) viewbox information

I see that the rendered svg omits the SVG tag so it can be composed more easily, unfortunately it removes an important aspect of many SVG: the viewbox on which they were designed for.

As such we should somehow add that back in the returned data.

---

**abcoathup** (2022-09-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> This should not be specified in my opinion and I strongly feel about this, the EIP should focus on the technical spec.

I’d be ok with removing text around ensuring that users have appropriate rights before composing from the EIP.  Legal rights to use will be on a project basis.

Providing potential options for linking NFTs could be useful, but also don’t have to be in the EIP.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> I see that the rendered svg omits the SVG tag so it can be composed more easily, unfortunately it removes an important aspect of many SVG: the viewbox on which they were designed for.
> As such we should somehow add that back in the returned data.

An early draft of the EIP included dimensions and a z-index.  We stripped this back to just the `renderByTokenId` function.

What do you think is the minimum information required for [viewBox - SVG: Scalable Vector Graphics | MDN](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/viewBox) in the EIP? Could this be optional?

---

**anthonygraignic** (2022-09-27):

Thanks for this much needed & cool EIP !

I had a technical question about the SVG spec version considered. Should the `renderTokenById` function only support SVG 1.1 or SVG 2 (currently still in Candidate Recommendation) is OK ?

Concerning the `viewBox`, I made a few tests with a composable SVG marker. And after grabbing some random SVGs on the internet, it appears that wrapping the content in an `<svg viewBox="0 0 X X">` (if not already present) was mandatory to control the final rendering.

This can be done either by the composed SVG NFT or by the composable SVG NFT.

Which raise 2 questions for me:

- What do I want to return in the renderTokenById and control the rendering (to allow full composition with svg elements and taking the risk of being cropped or restrict it) ? And also should it be the same as tokenURI ?
- Who should handle it ?

Both are outside of this EIP for me and I like the simple yet very efficient `renderTokenById(uint256 id)`.

I think a recommandation guide would help heading in the same direction.

Also maybe later, an additional function returning an ENUM or an identifier, could specify the rendering, allowed composition uses and maybe pricing (a new kind of royalties/fees for using this composable NFT) ?

---

**abcoathup** (2022-09-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> This should not be specified in my opinion and I strongly feel about this, the EIP should focus on the technical spec.

I have removed the rights requirement from the EIP: [EIP-4883: remove rights requirement by abcoathup · Pull Request #5726 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5726)

---

**abcoathup** (2022-09-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/anthonygraignic/48/3868_2.png) anthonygraignic:

> I had a technical question about the SVG spec version considered. Should the renderTokenById function only support SVG 1.1 or SVG 2 (currently still in Candidate Recommendation) is OK ?

Do you know if SVG 2 draft is backwards compatible with SVG 1.1?  I see references to compatibility but nothing specified at a high level.

https://svgwg.org/svg2-draft/single-page.html#intro-RelationshipToPrevious

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/anthonygraignic/48/3868_2.png) anthonygraignic:

> What do I want to return in the renderTokenById and control the rendering (to allow full composition with svg elements and taking the risk of being cropped or restrict it) ? And also should it be the same as tokenURI ?

We have been returning an SVG group element, with accessories, background and pfp all using the same coordinates (viewBox) for Party Panda 2.0/Merge Bears.  Essentially not including the `<svg>` element.

So `tokenURI` includes the `svg` element whilst `renderTokenById` is just grouped elements.



      [github.com](https://github.com/TeamPartyPanda/party-panda-2.0/blob/a37781dfed4400549c3a6d8d32df1b7732ea63c0/src/ERC4883Composer.sol#L169)





####



```sol


1. }
2.
3. return accessories;
4. }
5.
6. function renderTokenById(uint256 tokenId) public view virtual override returns (string memory) {
7. if (!_exists(tokenId)) {
8. revert NonexistentToken();
9. }
10.
11. return string.concat(_generateBackground(tokenId), _generateSVGBody(tokenId), _generateAccessories(tokenId));
12. }
13.
14. function addAccessory(uint256 tokenId, address accessoryTokenAddress, uint256 accessoryTokenId) public {
15. address tokenOwner = ownerOf(tokenId);
16. if (tokenOwner != msg.sender) {
17. revert NotTokenOwner();
18. }
19.
20. // check for maximum accessories
21. uint256 accessoryCount = composables[tokenId].accessories.length;


```












      [github.com](https://github.com/TeamPartyPanda/party-panda-2.0/blob/a37781dfed4400549c3a6d8d32df1b7732ea63c0/src/PartyPanda2.sol#L92)





####



```sol


1. _generateAccessories(tokenId),
2. ""
3. );
4.
5. return svg;
6. }
7.
8. function _generateSVGBody(uint256 tokenId) internal view virtual override returns (string memory) {
9. string memory colourValue = _generateColour(tokenId);
10.
11. return string.concat(
12. '' "Party Panda 2.0 is Copyright 2022 by Alex Party Panda https://github.com/AlexPartyPanda"
15. '' ''
18. ' '
19. ' '
20. ' ' ""
21. ''


```










It was suggested by one of the editors that we standardize `viewBox="0 0 500 500"`.  An early draft of the EIP had sizing but we removed to keep the EIP as simple as possible.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/anthonygraignic/48/3868_2.png) anthonygraignic:

> Who should handle it ?

I think the composer should handle any scaling/transforms, as it is their responsibility to compose the SVGs as they require.

I played with translate and scale on a Merge Bear.  I used the `renderTokenById` function from a [Loogie Bow](https://optimistic.etherscan.io/address/0x7a6d1925cdaf97295d0e401c3450e32f8c39c817#readContract) and an [OE40](https://optimistic.etherscan.io/address/0x5763f564e0b5d8233da0accf2585f2dbef0f0dfa#readContract) and manually added to a Merge Bear in https://www.svgviewer.dev/ and adjusted the translate and scale so that it fit.

Example manual SVG with Merge Bear, Crown, Bow and OE40:



      [gist.github.com](https://gist.github.com/abcoathup/573782a5a7ada73a7bc988c896fb1e1f)





####



##### MergeBearWithAccessories.svg



```



      Merge Bear










```

   This file has been truncated. [show original](https://gist.github.com/abcoathup/573782a5a7ada73a7bc988c896fb1e1f)










Looking at this example, ERC4883 composers could optionally accept translate and scale so that the end user could craft the SVG as desired.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/anthonygraignic/48/3868_2.png) anthonygraignic:

> I think a recommandation guide would help heading in the same direction.

Agree.  We are still very early, as we work out how to compose, especially across different ERC4883 projects.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/anthonygraignic/48/3868_2.png) anthonygraignic:

> Also maybe later, an additional function returning an ENUM or an identifier, could specify the rendering, allowed composition uses and maybe pricing (a new kind of royalties/fees for using this composable NFT) ?

I removed the rights requirement from the EIP as suggested by [@wighawag](/u/wighawag)

I would like to see a license that allows an ERC4883 to be composed by it’s holder as long as not used in hate speech.  (something along the lines of [The Can’t Be Evil NFT Licenses - a16z crypto](https://a16zcrypto.com/introducing-nft-licenses/)

---

**anthonygraignic** (2022-09-29):

"abcoathup:

> Do you know if SVG 2 draft is backwards compatible with SVG 1.1? I see references to compatibility but nothing specified at a high level.
> Scalable Vector Graphics (SVG) 2

It’s not fully backwards compatible but is “builds upon SVG 1.1 Second Edition”.

So it won’t be a problem for most SVG elements but there still is a few breaking changes [SVG 2 breaking changes · w3c/svgwg Wiki · GitHub](https://github.com/w3c/svgwg/wiki/SVG-2-breaking-changes)

(You can also see the new features here [SVG 2 new features · w3c/svgwg Wiki · GitHub](https://github.com/w3c/svgwg/wiki/SVG-2-new-features) for a more readable version of Appendix K)

My concern was raised by the `<use>` element [<use> - SVG: Scalable Vector Graphics | MDN](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/use) and its older `xlink:href` with the associated namespace `xlink:` that might not be supported at some point by browsers. But is still heavily used…

In addition, the status of this W3C standard is very unclear to me as there was no significant progress/interest since 2018, but still the browsers implemented it (["svg use: href" | Can I use... Support tables for HTML5, CSS3, etc](https://caniuse.com/?search=svg%20use%3A%20href))

So again, composer responsibility ?

 "abcoathup:

> I would like to see a license that allows an ERC4883 to be composed by it’s holder as long as not used in hate speech. (something along the lines of The Can’t Be Evil NFT Licenses - a16z crypto

Me too ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

And thanks for all the details/explanations !

---

**abcoathup** (2022-09-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/anthonygraignic/48/3868_2.png) anthonygraignic:

> So again, composer responsibility ?

I am not sure it would be worth adding the SVG version to the EIP. as there is some backwards compatibility.  If a composer attempts to compose with an incompatible SVG then the user can undo any composing/linking.

---

**anthonygraignic** (2022-09-30):

Yes totally, adding it would create a limitation. So it shouldn’t be added to the EIP ![:ok_hand:](https://ethereum-magicians.org/images/emoji/twitter/ok_hand.png?v=12)

---

**MidnightLightning** (2023-05-20):

I just learned of this draft EIP, and wanted to add in another example “in the wild” that I helped develop:

The MoonCatRescue project allows anyone to design a new Accessory for MoonCats, and any MoonCat token-holders can purchase Accessories from [the Boutique](https://boutique.mooncat.community/). There is an on-chain rendering contract at `0x91CF36c92fEb5c11D3F5fe3e8b9e212f7472Ec14` that outputs layered SVGs of the MoonCat, wearing the Accessories their owner chose to be active at that time. The MoonCats themselves are SVG-style illustrations (using `<polygon>` shapes), while the Accessories are PNG-style data, which are embedded into the SVG as data URLs (like how [@qzhodl](/u/qzhodl) gave as an example).

Accessories themselves are defined in the contract at `0x8d33303023723dE93b213da4EB53bE890e747C63`, which has the PNG-style image data (an IDAT chunk) stored separately from the dimensions and position data (there are four different MoonCat poses, so each Accessory has up to four different offset positions, to indicate how it should be positioned on each of the four poses). I went into more details about how that contract works in [this Reddit post](https://www.reddit.com/r/MoonCatRescue/comments/pl5nxw/mooncat_accessories_image_storage_and_access_on/).

I think having a common way to name the composition/data information for assets like these would be a great addition to the space! Though I think each asset that’s intended to be an Accessory built onto some sort of base thing would need multiple position definitions (for how to position it on multiple base types of things), or would need to have the asset have its origin put at a specific spot on its artwork, and declare what “type” it is (e.g. all “neckwear” assets have their origin be where the center of the neck should be, and its “width” define how wide the neck is. That would be enough information for any sort of character to position the asset correctly, and scale it to fit their “neck”).

---

**abcoathup** (2023-09-18):

List of deployed ERC4883 contracts

https://dune.com/queries/3031318/5038726

---

**abcoathup** (2025-02-20):

I removed the ERC-165 requirement for compatibility with earlier SVG NFTs.

