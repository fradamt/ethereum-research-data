---
source: magicians
topic_id: 5834
title: "ERC-3448: MetaProxy Factory"
author: pinkiebell
date: "2021-03-29"
category: EIPs
tags: [erc, metadata]
url: https://ethereum-magicians.org/t/erc-3448-metaproxy-factory/5834
views: 3206
likes: 1
posts_count: 7
---

# ERC-3448: MetaProxy Factory

![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=10) Let’s start the discussion around: [[ERC] MetaProxy Factory Standard by pinkiebell · Pull Request #3448 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/3448)

Reference Implementation: https://github.com/pinkiebell/MetaProxy

## Replies

**Amxx** (2021-03-29):

Personnal opinion: the tests are really not helping understanding the use of metadata.

I believe it’d be much clearer if the “factory” and the “implementation” were clearly separated.

My intuition tells me that the proxy points to the SimpleMock implementation, because I don’t see any other contract defined, but I believe an the first 20 bytes of the `_metaProxyFromXXX` should be the address of the implementation (and whatever is after that should be the metadata).

Restricting your tests to a self replicating contract is not helping beginners.

---

**pinkiebell** (2021-03-29):

Thanks for the feedback. I think the confusion stems from the fact that I use the name `factory` and in the reference implementation the `SimpleMock ` inherits the `_metaProxyFromXXX` functionaliy and thus, create a copy of itself (the SimpleMock).

Basically, developers inherit/copy the functionality and use them as they see fit. i.e any contract that implements that exposes their own factory function.

I actually thought about making a universal Factory that could be called from other contracts but refrained from the idea because the EIP should really just specify the bytecode.

But I’m interested to hear opinions about this. If something like a factory is wanted by developers I might just specify this one too. This could be deployed on the same address on mainnet and testnet networks.

---

**pinkiebell** (2021-11-29):

I changed the structure a bit and also implemented suggestions from [@Amxx](/u/amxx) .

Bumping the status to `Review` ![:ok_hand:](https://ethereum-magicians.org/images/emoji/twitter/ok_hand.png?v=10)

---

**pinkiebell** (2021-12-07):

The changes got merged and this EIP is now officially open for review: [EIP-3448: MetaProxy Standard](https://eips.ethereum.org/EIPS/eip-3448)

---

**pinkiebell** (2022-01-11):

Moved to last call (2022-01-25).

Let me know if someone knows a good way to reach the Etherscan developer team.

For reference, here is one contract that makes use of EIP-3448: https://etherscan.io/address/0xfd7eea107df33d9322c05b8956aed4a5697595b8#code

---

**Pfed-prog** (2024-06-11):

A question on SO: EIP-3448 really need the metadata length or is it optional?

My answer:

> It may seem odd to store the length of the metadata at the end, as ABI encoding typically stores length before the data begins, but in this case, it makes it easy for the implementation contract to parse the extra metadata with the following code from earlier.

`let posOfMetadataSize := sub(calldatasize(), 32)`

The assembly code illustrates how to easily parse the metadata.

It is not a security issue necessarily, it is a matter of convenience and a community enforced practice.

Without the standard one might expect to obtain the length at the beginning and not the end or not expect it at all.

Can the answer be better?

