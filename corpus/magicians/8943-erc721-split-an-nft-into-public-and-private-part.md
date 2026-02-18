---
source: magicians
topic_id: 8943
title: "ERC721: Split an NFT into public and private part"
author: mukas
date: "2022-04-16"
category: ERCs
tags: [nft, token, erc721]
url: https://ethereum-magicians.org/t/erc721-split-an-nft-into-public-and-private-part/8943
views: 1051
likes: 3
posts_count: 4
---

# ERC721: Split an NFT into public and private part

First I will explain what it consists of and then I will give a practical example

### Motivation

Today it is normal to hear people wondering why they want an NFT if anyone can see it, listen to it, copy it, etc. Clearly, the people saying this sort of thing don’t have a good understanding of the underlying technology.

To refute this kind of thinking and also to give NFTs more exclusivity, I present this idea.

### What does it consist of

It consists of dividing the NFT into two parts, the public part, which is the one that everyone can see, share, etc. (although it still has a single owner, that is, the typical NFT) and the private or hidden part, which can only be viewed when interacting with the owner address.

### Use cases

A book, the public part would be the cover and if you want a few pages and the rest of the book is in the private part.

As for the world of music, you can apply it to songs, showing a few seconds of test or discs showing one or two test songs.

Even in the world of cinema, the party publishes a trailer and the private the movie…

These are just a few use cases that came to mind quickly, but I’m sure you can think of many others

### Conclusion

What is intended to achieve with this is to have a greater incentive when purchasing an NFT.

I hope you have found it interesting and do not forget to share your opinions, I will read them all.

### Practical example

This is a simple way to do it, I hope you help me to get bugs and improve it

```auto
// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0  bytes32) private _hashes;

    constructor() ERC721("Bitcoin Whitepaper","BTC-W") {}

    function tokenURI(uint256 tokenId) public view virtual override returns (string memory)

    {
        require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token");
        if(_hashes[tokenId] == keccak256(abi.encodePacked(msg.sender,tokenId))){
            return "https://ipfs.io/ipfs/QmT1RYrfvUhGB8j52fPrmFHExYG43Y6g1gNSaeEAU8ikjJ?filename=nft-private.json";
        }else{
            return "https://ipfs.io/ipfs/QmeXX2dcauN7HrHpbbeMiDtjUpYxFWKKWCpVrZbFrMzBjv?filename=nft-public.json";
        }
    }

    function mintNFT(address to) public

    {
        token_count += 1;
        _mint(to, token_count);
        _hashes[token_count] = keccak256(abi.encodePacked(msg.sender,token_count));
    }

}
```

## Replies

**pasevin** (2022-04-21):

I think this is a simple missing link in NFTs right now.

Can you hint on how are you going to solve the “privatization” part?

I assume the content will have to be encoded and only decoded with the owners signature?

I’m really curious! Good luck, I will follow your progress!

---

**mukas** (2022-04-23):

I’m glad you’re interested!

I just updated the post with a simple example to get feedback and improve it.

Greetings

---

**DAYvid** (2022-07-15):

I really like this idea!

Great in real life examples. Core value is clear, too.

I’m also surprised at how simple the implementation is. Very nice work.

