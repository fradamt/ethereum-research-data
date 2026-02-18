---
source: ethresearch
topic_id: 13210
title: Creating a basic SHA256 hasher in Circom
author: htctw0adi5x9
date: "2022-08-01"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/creating-a-basic-sha256-hasher-in-circom/13210
views: 1365
likes: 0
posts_count: 1
---

# Creating a basic SHA256 hasher in Circom

I want to create a SHA256 hasher in Circom so I can validate that a person knows the pre-image of a SHA256 hash without revealing the pre-image. This is my current code but it doesn’t work:

```auto
include "/node_modules/circomlib/circuits/sha256/sha256.circom"

template SHAHasher(nBits) {
  signal input bits[nBits];
  signal output newHash[256];

  component shaHash = Sha256(nBits);

  for (var i=0; i<nBits; i++) {
    shaHash.in[i] <== bits[i];
  }

  for (var i=0; i<256; i++) {
    newHash[i] <== shaHash.out[i];
  }
}
```
