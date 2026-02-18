---
source: ethresearch
topic_id: 5831
title: Ethereum cross-chain DEX
author: tom2459
date: "2019-07-17"
category: Decentralized exchanges
tags: []
url: https://ethresear.ch/t/ethereum-cross-chain-dex/5831
views: 1942
likes: 0
posts_count: 1
---

# Ethereum cross-chain DEX

**TLDR** : I want to build a cross-chain DEX on Ethereum. What do you guys think?

Cross-chain DEXs are difficult to build due to the varying consensus algorithms and security requirements of each blockchain. Blockchains can’t communicate with other blockchains and for a cross-chain DEX to be feasible, both transactions need to reach irreversible state at the same time.

I suggest a minimal architecture allowing cryptocurrencies to be exchanged without funds going through any third party by utilizing a light-weight system of collaterals smart contracts.

By requiring the market maker, the Maker, to lock collaterals in a smart contract, the second trader whose role is to create a limit order, the Taker, can fulfill the order securely (sending payments first) without risk of payment reversal or double-spending.

Collaterals are secured by oracles. Trades happen on-chain without requiring extra protocol support for them resulting in compatibility with most blockchains. As there is no third party receiving payments on traders’ behalf, there’s no trading fees for traders. There are transaction fees for running the collaterals smart contracts.

The minimal architecture is ideal for low latency, high volume trades. To use the exchange, both traders will need ETH for smart contract fees and the tokens they are exchanging. The Maker will need ETH for collaterals. This DEX is good for decentralized OTC trading and if multiple of these DEXs are set up, can be used as alternatives to large centralized exchanges.
