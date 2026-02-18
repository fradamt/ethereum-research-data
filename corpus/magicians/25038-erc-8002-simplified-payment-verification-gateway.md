---
source: magicians
topic_id: 25038
title: "ERC-8002: Simplified Payment Verification Gateway"
author: Arvolear
date: "2025-08-07"
category: ERCs
tags: [bitcoin]
url: https://ethereum-magicians.org/t/erc-8002-simplified-payment-verification-gateway/25038
views: 582
likes: 8
posts_count: 4
---

# ERC-8002: Simplified Payment Verification Gateway

Hey Magicians! We’ve just finished drafting the ERC to bring Bitcoin’s SPV node concept to Ethereum, paving the road to a trustless and native issuance of BTC. Would love to hear your feedback!

Please do check out the [Wrapless](https://arxiv.org/pdf/2507.06064) research paper as well. It describes one of the use cases of this ERC through the usage of *native* BTC as a lending collateral.

---

## Abstract

Introduce a singleton contract for on-chain verification of transactions that happened on Bitcoin. The contract is available at “0xTODO”, acting as a trustless Simplified Payment Verification (SPV) gateway where anyone can submit Bitcoin block headers. The gateway maintains the mainchain of blocks and allows the existence of Bitcoin transactions to be verified via Merkle proofs.

## Motivation

Ethereum’s long-term mission has always been to revolutionize the financial world through decentralization, trustlessness, and programmable value enabled by smart contracts. Many great use cases have been discovered so far, including the renaissance of Decentralized Finance (DeFi), emergence of Real-World Assets (RWA), and rise of privacy-preserving protocols.

However, one gem has been unreachable to date – Bitcoin. Due to its extremely constrained programmability, one can only hold and transfer bitcoins in a trustless manner. This EIP tries to expand its capabilities by laying a solid foundation for bitcoins to be also used in various EVM-based DeFi protocols, unlocking a whole new trillion-dollar market.

The singleton SPV gateway contract defined in this proposal acts as a trustless one-way bridge between Bitcoin and Ethereum, already enabling use cases such as using *native* BTC as a lending collateral for stablecoin loans. Moreover, with the recent breakthroughs in the BitVM technology, the full-fledged, ownerless two-way bridge may soon become a reality, powering the permissionless and wrapless issuance of BTC on Ethereum.

## Specification

Check out the full specification on GitHub:



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1155)














####


      `master` ← `Hrom131:master`




          opened 01:05PM - 07 Aug 25 UTC



          [![](https://avatars.githubusercontent.com/u/44612825?v=4)
            Hrom131](https://github.com/Hrom131)



          [+1231
            -0](https://github.com/ethereum/ERCs/pull/1155/files)







Hey, a quick one here. Would love to hear your feedback!












The full reference implementation is available [here](https://github.com/distributed-lab/spv-gateway).

## Replies

**Tobi** (2025-08-20):

Sounds nice. But couldn’t just anyone write such a trustless contract on ethereum? Is an ERC needed?

---

**Arvolear** (2025-09-01):

That’s true. But how would anyone know of its existence and be sure that it is secure? Such singletons are a boon and a bane for an ERC. Also, the standardized spec allows these contracts to be deployed across multiple chains & to the same address.

---

**Arvolear** (2025-09-06):

UPD: The reference implementation is now ready and is available [here](https://github.com/distributed-lab/spv-gateway).

