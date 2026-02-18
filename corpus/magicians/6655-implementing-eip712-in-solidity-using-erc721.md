---
source: magicians
topic_id: 6655
title: Implementing EIP712 in Solidity using ERC721
author: jmb-42
date: "2021-07-14"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/implementing-eip712-in-solidity-using-erc721/6655
views: 1410
likes: 0
posts_count: 1
---

# Implementing EIP712 in Solidity using ERC721

## Overview

I think an ERC721 NFT contract may serve as a public registry for typed, structured signable data that aims to be the implementation of EIP712. I call it the reversible-hash-registry. I wrote an initial implementation of the contract [EIP712.sol](https://github.com/jmb-42/reversible-hash-registry/blob/main/contracts/EIP712.sol).

## Safe Signatures

EIP712 is a standard for signing typed, structured data that allows wallet software to derive the target of an ECDSA signature, giving certainty that the message being signed is not a malicious digest, e.g. the hash of a transaction that steals all of the user’s funds. Currently, there is no Solidity implementation for generalized EIP712.

On a related note, there exists a registry contract that serves as a mapping from contract method names to function selectors [here](https://etherscan.io/address/0x44691b39d1a75dc4e0a0346cbb15e310e6ed1e86). I discovered this contract via the MetaMask docs. It is my understanding that this registry improves UX by allowing wallet software and block explorers to present users with actual method names, rather than illegible 4 bytes function selectors. This is the inspiration for the idea.

## A Natural Marriage

The `keccak256` function is not reversible, but EIP712 defines a piecewise function that is. This piecewise function depends on two key on-chain and off-chain data structures:

1. A Solidity struct
2. A JSON object

ERC721 NFTs are a natural fit for this standard, because they offer the ability to reference off-chain metadata via a smart contract, giving us 2. Then it remains to generalize 1., within the context of ERC721. It’s also quite interesting that the numbers of these standards are permutations of one another, but that’s just a happy accident I think.

## The Specific Solution

The idea for the NFT contract is hopefully simple:

1. the tokenId of each NFT is the hash of a signature type
2. the ownerOf of each NFT is a smart contract that implements the solidity struct and the hash function for that specific type
3. metadata of each NFT references the JSON object for user facing wallet software

Under this scheme, wallets can compute the hash of instances of the type by referencing the metadata of the typehash NFT. Further, smart contracts can reference the `ownerOf` a typehash NFT to compute the hash of an instance on-chain, eg for a `transferWithPermit` call. So we have routes for both usecases, on-chain and off-chain.

## Challenges

- EIP712 specifies an EIP712Domain, which differs for each contract. This implementation possibly needs to adapt to be able to compute the hash for any arbitrary domain from within any calling contract, to generalize/centralize the logic.
- Metadata is not immutable, therefore the off-chain hash function may not be secure

if the solidity implementations are robust enough, we may not need the JSON object, because wallet software can make an rpc call to the NFT contract to compute the hash of any instance

The flow of using this registry can be refined a lot more, as it’s not exactly clear how to use this from an external developer’s standpoint imo (in either off-chain or on-chain software)

I may not have communicated this idea well enough, but I hope the general idea is clear. I’m hoping that the community can help me to refine this idea, especially as I think it would be incredibly useful for EIP-3074, because contracts implementing `AUTH`/`AUTHCALL` will rely on ECDSA signature recovery, and this hash registry could improve UX enough that it accelerates the development, utility, and convenience of smart contract wallets.
