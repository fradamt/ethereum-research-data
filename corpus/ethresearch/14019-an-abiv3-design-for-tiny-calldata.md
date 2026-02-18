---
source: ethresearch
topic_id: 14019
title: An ABIv3 design for tiny calldata
author: esaulpaugh
date: "2022-10-25"
category: Layer 2
tags: []
url: https://ethresear.ch/t/an-abiv3-design-for-tiny-calldata/14019
views: 2213
likes: 0
posts_count: 6
---

# An ABIv3 design for tiny calldata

It is my understanding that calldata length has become a bottleneck for Layer 2 scaling. I have recently begun to collaborate with some people on a possible version 3 of the ABI specification which could help with this.

In v3, a call to `foo(bool[12])` would encode as `047f` for `[ false, false, false, false, false, true, true, true, true, true, true, true ]`.

In the header byte, the first three bits are the encoding version identifier, `000`. The next five bits are the function identifier `00100`, in this case, 4. If the function ID is 31 or greater, all five bits are set and the RLP encoding of the function ID is appended to the header byte.

Next is `7f` which is the RLP encoding of the integer which represents the values in the bool array, where each element is represented by a bit. Notice that in this case the first five bools are `false` which makes the integer `000001111111` or 127 i.e. `0x7f`.

Boolean arrays are a special case. Everything else is much more normal. Values are straightforwardly encoded as RLP strings, except for arrays and tuples which are encoded as RLP lists.

An example call to `foo((string,bool,bool,int72)[2],uint8)` (given function ID 27) is `1bcac44180010ac44201800181ff`.

I would like to know if this would be acceptable for use in Layer 2 and elsewhere. The full implementation in Java is here: [GitHub - esaulpaugh/abiv3: ABIv3 proof of concept for Ethereum](https://github.com/esaulpaugh/abiv3) and I am considering beginning a python implementation.

## Replies

**MicahZoltu** (2022-10-26):

I believe most L2s already do some amount of manual compression for their calldata, but the problem is just that the sheer volume of information required to be committed on-chain is massive given the cost per byte.  No amount of changes to Solidity are likely to alleviate this problem.

---

**esaulpaugh** (2022-10-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> the sheer volume of information required to be committed on-chain

Is it not correct that the throughput of current L2s is roughly (inversely) proportional to the average length of a calldata? ABIv2 is inherently space-inefficient, and while compression algorithms can help significantly, I think the widespread use of manual calldata hacks shows that it is not sufficient. And I am not aware of any proposal that would make calldata on L1 so inexpensive per byte that compression and calldata hacks are no longer worth the effort.

In fact I think that calldata hacks are here to stay, which is why they should be automated and generalized to apply to any function signature. Hence ABIv3.

---

**MicahZoltu** (2022-10-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/esaulpaugh/48/4998_2.png) esaulpaugh:

> ABIv2 is inherently space-inefficient, and while compression algorithms can help significantly, I think the widespread use of manual calldata hacks shows that it is not sufficient.

I *think* most L2s just pass in a byte array, then they extract data out of that inside their function.  Changing the Solidity ABI to be more space efficient wouldn’t change anything for such L2s because they already are just sending a byte array that is mostly opaque to Solidity.

This isn’t to say that there wouldn’t be any value in making changes to the ABI to be more space efficient, just that I don’t think it will have a meaningful impact on L2s.  Its biggest impact would be on novice Ethereum developers who are not gas golfing.

FYI: You will probably have better luck getting feedback on Solidity changes over at https://forum.soliditylang.org/

---

**esaulpaugh** (2022-10-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Changing the Solidity ABI to be more space efficient wouldn’t change anything for such L2s

I must stress that (my personal conception of) ABIv3 is not intended to serve the status quo or make the currently most popular contracts more popular or profitable. It is my opinion that if Ethereum scales, current contract designs will be a negligible fraction of all contracts.

I think that gas golfing is a harmful barrier to entry which saps Ethereum of scarce developer resources. It’s all well and good if someone enjoys that, but having bespoke per-contract hacks be mandatory for reasonable performance is just shooting the network in the foot long-term. Especially if the hacks negatively affect adoption, composability, understandability, and potentially security.

You are right about the solidity forum, though. I should see what they think about changing the defaults.

---

**esaulpaugh** (2023-02-09):

I’ve written a first-draft spec for such an ABIv3 based on certain assumptions:

1. Ethereum will scale and the overwhelming majority of contract execution will occur on Layer-2 in and among contracts which do not exist today.
2. De facto, there is no calldata standardization on Layer 2 currently. It is not possible to achieve compatibility with existing L2 contracts in general because L2 contracts generally do not conform to any standard.
3. Layer-2 computation costs will be inconsequential compared to costs proportional to calldata length (such as cryptographic verification).
4. If a proposed standard’s calldata is significantly more expensive than custom hacked calldata, that standard will fail to achieve widespread adoption.



      [github.com](https://github.com/esaulpaugh/abiv3/blob/0c6626c97b6a2f432c94e311315cfb81091d9a04/SPEC.md)





####



```md
## Assumptions

### The following assumptions drive this iteration of the design:

1. Ethereum will scale and the overwhelming majority of contract execution will occur on Layer-2 in and among contracts which do not exist today.
2. De facto, there is no calldata standardization on Layer 2 currently. It is not possible to achieve compatibility with existing L2 contracts in general because L2 contracts generally do not conform to any standard.
3. Layer-2 computation costs will be inconsequential compared to costs proportional to calldata length (such as cryptographic verification).
4. If a proposed standard's calldata is significantly more expensive than custom hacked calldata, that standard will fail to achieve widespread adoption.

## Resources

ABIv2 spec: https://solidity.readthedocs.io/en/latest/abi-spec.html

RLP spec: https://github.com/ethereum/wiki/wiki/RLP

## Encoding

### Byte zero:

```

  This file has been truncated. [show original](https://github.com/esaulpaugh/abiv3/blob/0c6626c97b6a2f432c94e311315cfb81091d9a04/SPEC.md)

