---
source: ethresearch
topic_id: 19411
title: Enabling light node to verify a field element from its column in peer das
author: Athos
date: "2024-04-29"
category: Sharding
tags: [data-availability]
url: https://ethresear.ch/t/enabling-light-node-to-verify-a-field-element-from-its-column-in-peer-das/19411
views: 1728
likes: 0
posts_count: 1
---

# Enabling light node to verify a field element from its column in peer das

When we finally implements 2D PeerDAS, blob data will be formatted into a data matrix, where each element (aka cell) of the matrix is an array of field elements, with 64 field elements in each array. Peers are required to sample this matrix, with the minimum sampling unit being a cell.

For nodes with limited resources, such as light nodes, we may allow them to perform sampling in the following manner:

1. Light node requests:

- Column index
- Blob index
- Field element index within the cell

1. The requested peer’s response:

- The value of the field element
- The KZG commitment of the cell polynomial
- The proof of the field element in the cell polynomial
- The KZG proof of the cell in the blob

The light node performs verification on the aforementioned content.

For a KZG multiproof, we have the following:

 Proof_{cell}={\frac {f(\alpha)-I(\alpha)}{z(\alpha)}}G_1

The polynomial I(x), which represents the cell polynomial, is obtained by interpolating the field elements within the cell based on their indices within the blob, where I(\alpha)G_1 represents the KZG commitment of the cell polynomial

For a specific field element within the cell, its proof format is as follows

 Proof_{ele}=\frac {I(\alpha)-val_{ele}} {x_{ele}-\alpha}G_1

These two proofs are related through I(\alpha)G_1, which allows us to verify a specific field element within the blob without obtaining the complete cell data.
