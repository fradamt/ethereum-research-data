---
source: ethresearch
topic_id: 14752
title: "Probably outdated, but: EIP-170 24KB max. leading to Expensive On-Chain Data Blobs masqueraded as compiled EVM bytecode"
author: zdanl
date: "2023-02-04"
category: EVM
tags: []
url: https://ethresear.ch/t/probably-outdated-but-eip-170-24kb-max-leading-to-expensive-on-chain-data-blobs-masqueraded-as-compiled-evm-bytecode/14752
views: 1108
likes: 0
posts_count: 2
---

# Probably outdated, but: EIP-170 24KB max. leading to Expensive On-Chain Data Blobs masqueraded as compiled EVM bytecode

Hi! I’m new to Ethereum intrinsics, and would like to benchmark / PoC out of sheer interest, its capability - no matter how right or wrong, or disincentived that currently is - as a Decentralized Globally Distributed, reputable, Database or Encrypted Record hosts. Bluntly, I was reading about the Deployment mechanism of “Compiled EVM Smartcontracts” sent to an empty recipient address / or 0x00.

Questioning, without reading Code yet but some Documentation and Proposals, how a Compiled Binary Blob qualifies as a Compiled Smartcontract, whether ELF header like segmentation was already done, and noonetheless - in the end, if i am willing to pay the enourmos gas fees for production-scale use of that interface, I would probably win in letting an AES blob look like whatever the “Validator?” expects.

Is this… possible in theory and practice, and which thoughts/comments does it raise, disregarding Gwei->Eth payments?

Happy to hear any recommendations for the current closest Blockchain equivalent of a Redis Cluster, too.

Dan

## Replies

**zdanl** (2023-02-05):

I wanted to mention this American Fuzzy Loop AFL quote, in case you want to make compiled smart contracts more verifiable:

`Internal filesystem checksums also pose a challenge. The fuzzer will change things in the image, but those values won't be reflected in the checksums. One possibility would be to comment out the checksum-verification code in the filesystem, though that could lead to introducing other bugs. It also means that the test-case images may no longer work on a stock kernel. A better idea is to calculate the correct checksums and modify the image before it gets mounted. Figuring out how and where to do that can take a fair amount of work, however.`


      ![](https://ethresear.ch/uploads/default/original/2X/d/dd728d0ae9981d5a3babd5e54310b5a3816e6641.png)

      [LWN.net](https://lwn.net/Articles/685182/)





###



Fuzz testing (or fuzzing) is an increasingly popular technique to find security and other bugs [...]










Dan

