---
source: magicians
topic_id: 6853
title: Scriptable ERC721
author: wuminzhe
date: "2021-08-13"
category: Magicians > Primordial Soup
tags: [erc-721]
url: https://ethereum-magicians.org/t/scriptable-erc721/6853
views: 572
likes: 0
posts_count: 1
---

# Scriptable ERC721

I don’t know if there is already a similar work in progress, if so please let me know.

The current erc721 is static. I think erc721 can be dynamic. This can be done by supporting script.

1. the creator writes the script, so the creator can control how NFT behaves.
2. once the NFT is minted, the script can’t be modified.
3. some parameters in the script can be modified by the NFT owner.
4. multiple script type support, such as p5js, raphael, etc.

Below is an example of how to extend the ERC721:

```auto
interface ERC721Scriptable {
	event ParamsUpdated(uint256 indexed tokenId, string oldParamsURI, string newParamsURI);
	function scriptType() external view returns (string);
	function scriptURI(uint256 tokenId) external view returns (string);
	// hash result of params, protect params from being modified
	function paramsHash(uint256 tokenId) external view returns (bytes32);
	function paramsURI(uint256 tokenId) external view returns (string);
	function updateParamsURI(uint256 tokenId, string paramsURI) external;
}
```

A p5js script example

```auto
function setup() {
  createCanvas(400, 400);
  background(200/*{bgcolor}*/);

  ellipse(200, 200, 80/*{ellipse1}*/, 80/*{ellipse2}*/);
  text('world'/*{title}*/, 10, 30);
}
```

The params example of the above script

```auto
{
	"bgcolor": 100,
	"ellipse1": 60,
	"ellipse2": 60,
	"title": "hello world"
}
```
