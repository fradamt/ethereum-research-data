---
source: magicians
topic_id: 12407
title: "EIP #?: add precompile for Blake2s/Blake3"
author: laudiacay
date: "2023-01-03"
category: EIPs
tags: [opcodes, precompile]
url: https://ethereum-magicians.org/t/eip-add-precompile-for-blake2s-blake3/12407
views: 1890
likes: 8
posts_count: 5
---

# EIP #?: add precompile for Blake2s/Blake3

I’m interested in adding a precompile that adds support for Blake3/Blake2s, similar to [this issue](https://github.com/ethereum/EIPs/issues/152) discussing adding Blake2b.

I left a [comment](https://github.com/ethereum/EIPs/issues/152#issuecomment-1183674205) there saying I’m willing to implement this this if people would be willing to help me get the PR merged (this is my first EIP and will be my first geth PR). Opening this up as a space to discuss.

My team [forked](https://github.com/banyancomputer/blake3-sol) and benchmarked an existing solidity implementation. Image attached, it basically costs $60 to hash something. This is not great! I’m checking out a decompiled version of it, but I’m not super hopeful about the gains that hand-optimizing this is going to get me.

[![image](https://ethereum-magicians.org/uploads/default/original/2X/2/22a2815aa745f9a36a2cbcafa19b33a0183b95f6.png)image1016×342 13.4 KB](https://ethereum-magicians.org/uploads/default/22a2815aa745f9a36a2cbcafa19b33a0183b95f6)

[Blake3](https://en.wikipedia.org/wiki/BLAKE_(hash_function)#BLAKE3) is a merkle-tree-based hash function with cool features like being super-parallelizable, updateable on the fly, indefinitely extensible for KDF’ing, and (my favorite) allows for verified streaming and log(n) verification of randomly selected chunks from files. My team was originally hoping to use it to build an Ethereum-based decentralized incentive layer for IPFS pinning (we are no longer building this), but I can imagine plenty of other fun optimizations of things like optimistic L2s and data availability that could be enabled with this. Blake2s is also necessary to do Wireguard handshakes… if for some reason you are attempting to do that on-chain, you’d need it.

Zooko has a [comment](https://github.com/ethereum/EIPs/issues/152#issuecomment-1183824411) detailing the changes between the existing [opcode](https://eips.ethereum.org/EIPS/eip-152) at `0x09`- basically, it’s the same code, with four constants changed, and the word size of the function is halved. See the relevant RFC [here](https://www.rfc-editor.org/rfc/rfc7693).

As far as gas fees, the `0x09` Blake2b F function precompile is charged as `Each operation will cost GFROUND * rounds gas, where GFROUND = 1`. Blake2b is usually run with 12 rounds, whereas Blake2s is usually run with 10, so most calls would take 10 gas. The input size difference is accounted for with CALL gas computations. On modern 64-bit architectures, assuming a negligible amount of weird packing and unpacking the 32-bit words into 64-bit words, I think it’ll be appropriate to go with the same gas pricing for this precompile as with `0x09`.

I propose that this precompile go at contract `0x0a`, which will be compatible with anything that *doesn’t* assume there’s nothing at that address.

I think the only work left to do is to write this up as an EIP, do a PR (**where should that go?**), and validate my assumptions above about gas costs.

## Replies

**prestwich** (2023-01-04):

As one of the people who initially pushed for EIP-152 and helped write it, I think a post-mortem is long overdue. I may write a full one for a blog sometime, but here’s the condensed version:

Fundamentally EIP-152 failed for 2 reasons

1. Politicization of the proposal led to a weird technical design.
Implementing the F function instead of the hashfunction was political nonsense. It should never have been done. It led to a bad result for everyone.
2. Envisioned use cases were not validated before inclusion
The authors had specific goals in mind, but we did not have any evidence that users wanted what we (the authors) wanted. And given the extra expense imposed by the f-function design, we could not realize our goals anyway. So we failed to launch any products into a market that (as time has shown) probably didn’t want those products anyway.

I think that EIP-152 is a strong candidate for deletion. Rather than updating it, we should deprecate, evaluate past usage, and deactivate in some post-Shanghai fork. It can be used as a safe & uncontroversial testflight for deprecating and removing EVM features.

If we want to add more hash functions to the EVM, we piloted an [extensible hash precompile](https://github.com/celo-org/celo-proposals/blob/master/CIPs/cip-0020.md). However, it hasn’t seen much adoption either last I checked.

---

**laudiacay** (2023-01-26):

I actually like your proposal quite a bit, and agree that supporting them individually is subpar (with individual function families and the way it’s currently being done with the blakes in practice/in this proposal… if this continues, it could blow up to people wanting 10 precompiles… yuck)

An extensible hash precompile that properly does blake3 merkle validation without 2^n precompile CALLs would be incredible for building verifiable networking and certain DA primitives and more. Could also get poseidon in here pretty easily.

Can you think of anyone else who might be interested in supporting this? I wonder if Filecoin Saturn folks might be into it…

---

**dhl** (2024-10-14):

[@prestwich](/u/prestwich) thank you so much for the multi-year work you and others have put in to make EIP-152 possible.

The low usage of BLAKE2f is likely due to how hard it is to use BLAKE2b, even with the EIP. EIP-152 solves the performance problem by off-loading the most expensive part of BLAKE2b hashing to native implementation, but the lack of correct and complete implementation of BLAKE2b made BLAKE2b inaccessible to all but the most determined developers.

I really hope BLAKE2f doesn’t get deleted. I’ve just released [blake2b-solidity](https://github.com/dhl/blake2b-solidity/) to make using BLAKE2b a bit more accessible to Solidity developers. It’s still a work-in-progress, but it is a complete implementation where I strive for correctness and feature completeness (all extensions except tree hashing is implemented).

I can’t help but feel a bit envious of the Solana folks for being able to just import a Rust crate and have available at their disposal all sorts of interesting cryptographic primitives, including BLAKE2b and BLAKE3. I’ve been wondering what would it take to take this sort of extensibility to the EVM.

---

**rexbarq** (2025-04-02):

I noticed that your implementation runs at 114% of keccak. Is below 100% possible with a better precompile? I would want this for my protocol.

