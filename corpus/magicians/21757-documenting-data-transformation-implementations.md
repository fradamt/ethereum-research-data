---
source: magicians
topic_id: 21757
title: Documenting data-transformation implementations
author: MidnightLightning
date: "2024-11-18"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/documenting-data-transformation-implementations/21757
views: 65
likes: 1
posts_count: 3
---

# Documenting data-transformation implementations

Within solidity smart contracts, I’ve seen a few repetitions of different data-formatting algorithms like base64 encoding/decoding, JSON, and SVG. Rather than having smart contracts re-implement this logic over and over, I think it would be helpful to document any smart contracts that already exist as standalone Library implementations for any other contract to use (and smart contracts that have some algorithm’s logic baked in that would be good candidates for someone to refactor into a standalone library), so starting here with the few I know of:

## Standalone Libraries

- AVL tree (self-balancing binary search tree): Grove 0xD07cE4329B27Eb8896c51458468d98a0e4C0394C

## Examples

- SVG: MoonCatSVGs 0xB39C61fe6281324A23e079464f7E697F8Ba6968f
- PNG (cyclic redundancy check (CRC) checksums): MoonCatAccessoryImages 0x91CF36c92fEb5c11D3F5fe3e8b9e212f7472Ec14
- Base64: MoonCatAccessoryImages 0x91CF36c92fEb5c11D3F5fe3e8b9e212f7472Ec14

---

What others exist out there? A key algorithm that I’ve been thinking about trying to implement in Solidity is the DEFLATE ([RFC-1951](https://www.rfc-editor.org/rfc/rfc1951.html)) decoder/decompression algorithm. This would allow data to be saved into a contract’s memory compressed, and then allow view functions to still be able to parse it. Does that exist anywhere out there on-chain already?

## Replies

**MidnightLightning** (2024-12-28):

The Moonbirds project created an `AssetStorageManager` contract at `0xEDe24B4988cb64cC07fB72fF8AE71Bd8bB031b70`, which includes in its source code an `InflateLib.sol` library that is a solidity implementation of inflating a DEFLATE-compressed stream, and is annotated as Apache-2.0 licensed.

https://etherscan.io/address/0xEDe24B4988cb64cC07fB72fF8AE71Bd8bB031b70#code#F3#L1

There is a standalone version deployed to `0x8d69408205dEc1F1Eb5A2250C8638017Ef6069b6` that has a single `inflate` function that accepts a tuple (uncompressed size, followed by the compressed data).

---

**MidnightLightning** (2025-01-01):

**Merkle Tree:** [Murky](https://github.com/dmfxyz/murky/tree/main) project has standalone implementations of “full” and “complete” binary tree Merkle tree parsing. Unsure if these have been deployed to any blockchains as standalone libraries.

