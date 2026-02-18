---
source: magicians
topic_id: 17541
title: On decoding raw calldata, without the ABI or signature resolution
author: Jon-Becker
date: "2023-12-20"
category: Magicians > Primordial Soup
tags: [evm, decoding, calldata]
url: https://ethereum-magicians.org/t/on-decoding-raw-calldata-without-the-abi-or-signature-resolution/17541
views: 786
likes: 5
posts_count: 6
---

# On decoding raw calldata, without the ABI or signature resolution

This will serve as discussion for my article: [“On Decoding Raw EVM Calldata”](https://jbecker.dev/research/decoding-raw-calldata)

Feedback is appreciated, and helps me improve!

*Note: It’s probable that this method is not 100% accurate, and can be iterated on and improved. If you notice any edge cases or bugs that I’m missing, please let me know by [opening an issue or PR](https://heimdall.rs/).*

## Replies

**wjmelements** (2023-12-21):

I think you still need signature resolution. Otherwise you don’t know the types and the decoding would be ambiguous. There are also collisions in the 4byte prefix so you really need the ABI json.

---

**Jon-Becker** (2023-12-21):

[@wjmelements](/u/wjmelements)

Decoding various types is ambiguous, such as `bool` and `uint<N>`. However, this is not a blocker for decoding readable types from

the raw calldata, and this article outlines how we can remove some of the ambiguity when decoding raw calldata.

For my purposes, i’ve found that this method of calldata decoding is extremely accurate, and can handle decoding dynamic types (and even nested dynamic types) with ease.

Heimdall does support decoding with signature resolution, but falls back to this method if no signature is found.

So you are partially correct, yes there is some ambiguity but no, you don’t *need* signature resolution or ABI to obtain a decoded view of the calldata ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**wjmelements** (2023-12-21):

Ok here is a concrete example for the ambiguous types. Suppose the 4byte calldata parameter-array is `[3, 0x40, 1, 0]`. Is this `(3, [0])` or is it `(3, 64, 1, 0)`?

---

**Jon-Becker** (2023-12-21):

You are correct, this is an example of an ambiguous type. This method, and heimdall, will assume it is (3, [0]).

This does not prevent us from decoding the calldata, however. This paper does not present this method as a perfect solution — this is the closest we can get **without** the ABI / signature.

---

**wjmelements** (2023-12-21):

This is the right decision and should be correct almost all of the time. I suspect your code will be useful for block explorers when the contract is unverified. I will recommend it to Etherscan.

