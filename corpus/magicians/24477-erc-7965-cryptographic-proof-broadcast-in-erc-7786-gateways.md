---
source: magicians
topic_id: 24477
title: "ERC-7965: Cryptographic Proof Broadcast in ERC-7786 Gateways"
author: ernestognw
date: "2025-06-06"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7965-cryptographic-proof-broadcast-in-erc-7786-gateways/24477
views: 151
likes: 3
posts_count: 1
---

# ERC-7965: Cryptographic Proof Broadcast in ERC-7786 Gateways

## Summary

ERC-7965 extends [ERC-7786](https://ethereum-magicians.org/t/erc-7786-cross-chain-messaging-gateway/21374) to enable **trustless cross-chain messaging using storage proofs** instead of external validators. Messages are stored on source chains and verified on destination chains using cryptographic proofs of the source chain’s state.

## Key Design Choices

The standard defines three ERC-7786 attributes:

- route((address,bytes,uint256)[]) - Verification path with proofs and versions
- storageProof(bytes) - Proof that message exists in source state
- targetBlock(uint256) - Block number where message was stored

We use empty string `""` as receiver address to indicate **broadcast messages** (available to any contract on destination).



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1072)














####


      `master` ← `ernestognw:feat/storage-proof-broadcasting-gateways`




          opened 05:36PM - 06 Jun 25 UTC



          [![](https://avatars.githubusercontent.com/u/33379285?v=4)
            ernestognw](https://github.com/ernestognw)



          [+238
            -0](https://github.com/ethereum/ERCs/pull/1072/files)







Extends ERC-7786 cross-chain messaging with cryptographic proof-based verificati[…](https://github.com/ethereum/ERCs/pull/1072)on and granular broadcasting semantics. It enables trustless message verification using blockchain consensus mechanisms rather than external validators or multisigs.

The specification defines three ERC-7786 attributes: `route()` for multi-hop verification paths, `inclusionProof()` for cryptographic evidence of message commitment, and optional `targetBlock()` for finality validation.

Broadcasting leverages ERC-7930 addresses to enable targeted message distribution: empty address components broadcast to all addresses on specific chains, empty chain references broadcast to all chains of a type, and fully zeroed addresses enable universal broadcasting.
