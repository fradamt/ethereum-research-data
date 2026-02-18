---
source: magicians
topic_id: 15699
title: A new opcode for decoding varint
author: esaulpaugh
date: "2023-09-06"
category: EIPs > EIPs interfaces
tags: [abi]
url: https://ethereum-magicians.org/t/a-new-opcode-for-decoding-varint/15699
views: 503
likes: 2
posts_count: 1
---

# A new opcode for decoding varint

In support of a space-efficient ABIv3, how about a new opcode for decoding variable-length-encoded integers? In protocol buffers (protobufs) there is a format called varint.

Varints are similar to length-prefix encoding except they use a continuation bit in each byte to tell the decoder when to stop. This format has very good space efficiency properties and that entails potential gas savings.

This encoding would not be used for the in-memory format but would be used by externally-owned accounts and optimistic rollups when writing calldata to EVM storage.

An AI program AlphaDev was recently able to reduce the length of the varint decoding algorithm from 31 instructions to 27 instructions on x86. Assuming a vaguely similar number of instructions in EVM code, this is acceptable for Layer-2 contracts but is too much for contracts on mainnet. This is especially true with the current lack of simple subroutines.

A more space-efficient calldata format using varints could also enable optimistic rollups to standardize rather than rely on bespoke per-contract calldata hacks.

One issue is that varints are by specification limited to 64-bit integer values (encoded as 10 bytes). It should be trivial to extend the format to account for 256-bit values, or some other format could be used for the larger ABI types.


      ![](https://ethereum-magicians.org/uploads/default/original/2X/3/38bccea72c2de74578b686a4a2f997fe4c35fa1a.png)

      [protobuf.dev](https://protobuf.dev/programming-guides/encoding/)





###



Explains how Protocol Buffers encodes data to files or to the wire.










https://doi.org/10.1038/s41586-023-06004-9
