---
source: magicians
topic_id: 7698
title: ERC-721; safeTransferFrom function, Modification idea
author: serCorp
date: "2021-12-06"
category: ERCs
tags: [nft, token, erc-721]
url: https://ethereum-magicians.org/t/erc-721-safetransferfrom-function-modification-idea/7698
views: 949
likes: 0
posts_count: 1
---

# ERC-721; safeTransferFrom function, Modification idea

Hi all,

Concerning the ERC721.sol safeTransferFrom function, I propose to move the code line and invert the require by the call to transferFrom:

**Current code:**

function safeTransferFrom(address from, address to, uint256 tokenId, bytes memory _data) public {

transferFrom(from, to, tokenId);

require(_checkOnERC721Received(from, to, tokenId, *data), “ERC721: transfer to non ERC721Receiver implementer”);

}*

**I propose:**

function safeTransferFrom(address from, address to, uint256 tokenId, bytes memory _data) public {

require(_checkOnERC721Received(from, to, tokenId, *data), “ERC721: transfer to non ERC721Receiver implementer”);

transferFrom(from, to, tokenId);***

}

In my point of view, the require must be always before the call to any function that should be called if the require is confirmed.

Thanks!

Sergio
