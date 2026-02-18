---
source: magicians
topic_id: 16274
title: Verkle proof verification precompile
author: gballet
date: "2023-10-26"
category: EIPs > EIPs core
tags: [prague-candidate]
url: https://ethereum-magicians.org/t/verkle-proof-verification-precompile/16274
views: 1895
likes: 3
posts_count: 2
---

# Verkle proof verification precompile

Introducing a new Ethereum Improvement Proposal (EIP) titled **“Verkle proof verification precompile”** . The proposal is currently in the **Draft** stage and falls under the **Core** category.

# TLDR

The EIP proposes the addition of a precompiled contract to provide up-to-date state proof verification capabilities to smart contracts in a stateless Ethereum context. This is aimed at keeping proving systems up-to-date without having to develop and deploy new proving libraries each time another proof format must be supported.

# How does it work?

A precompiled contract is added at address `0x21`, wrapping the stateless ethereum proof verification function. The precompile requires 4 inputs, tightly encoded: `version` , `proof_data_location` , `proof_data_size` , and `state_root` . If `version` is `0` , then the proof is expected to follow the SSZ format described in [the verge](https://github.com/ethereum/consensus-specs/pull/3230) proposal in the consensus spec. The precompile returns `1` if it was able to verify the proof, and `0` otherwise.

Full EIP text: https://github.com/ethereum/EIPs/pull/7926

## Replies

**protolambda** (2023-11-23):

EIP suggestion: move the version-byte from being a calldata argument to just being part of the memory range that is specified, so that the byte-prefix becomes a standard part of the opaque data that contracts pass around when proving state.

Edit: and if it’s truly a precompile, it should not have access to memory of the caller, and should probably just take only calldata.

I’d be interested in adding MPT verification code to this too. Verifying a branch is relatively easy, given the large amount of existing MPT code in the EL client code-bases. Whereas onchain MPT verification is considered quite risky.

The OP-Stack uses an onchain MPT contract on L1 for L2 withdrawals, and this contract is only really considered acceptable because of the audits, lindy effect and 7 day window for responses in case of verification bugs. This contract is very inefficient also; we have investigated optimizations, but those come with code-complexity risks. Even simple things like encoding the MPT nibbles differently are an ugly and very involved solidity/yul operation. Replacing this with a precompile call would be a great improvement.

With MPT support contracts can seemlessly move over from MPT state-verification to verkle state-verification also.

And a simple state-verification precompile in general can be incredibly valuable for cross-ethereum-chain messaging: if every chain supports the MPT/verkle verification of contract-storage, then inbox/outbox cross-chain messaging systems become a lot less risky to implement, and thus improve overall ethereum ecosystem security.

