---
source: magicians
topic_id: 7147
title: EIP-2981 Extension - ERC2981Receiver | Token Identification At Payment
author: dievardump
date: "2021-09-27"
category: EIPs
tags: [nft, royalties]
url: https://ethereum-magicians.org/t/eip-2981-extension-erc2981receiver-token-identification-at-payment/7147
views: 1045
likes: 4
posts_count: 3
---

# EIP-2981 Extension - ERC2981Receiver | Token Identification At Payment

Hello everyone.

Wanted to start a discussion on an `ERC2981 Extension: ERC2981Receiver` - A callback that the recipient returned by `royaltyInfo()` could implement in order to allow cheaper collaborations, a better verification of the royalties payment and better accounting for creators.

The idea would be that `recipient`, when it’s a contract, could implement a callback called `onERC2981Received`, that would allow the caller to pass meta about the NFT sale (contract address, token id, paymentToken, paymentAmount) at the same time it sends the payment.

This to make the EIP a bit more solid and useful for creators than what it is already.

Current Draft: [Draft - EIP-2981 Extension - Token Identification At Payment · GitHub](https://gist.github.com/dievardump/f7b21f511f595a552becfb7a475eb133)

---

## Summary:

A standardized way to pass information (address registry, uint256 tokenId, address paymentToken, uint256 paymentValue) with the transfer of royalties payment when supporting EIP-2981.

## Abstract

This standard extends the [EIP-2981 specification](https://gist.github.com/dievardump/eip-2981.md) and add a callback `onERC2981Received(address, uint256, address, uint256)` on contracts *receiving royalties payments*, to allow for Marketplace contracts to pass critical information with the call made to pay royalties.

By adding the registry (NFT contract address), the token id, the payment token and the payment value, we allow cheaper management of multiple royalties recipients and easier tracking and accounting of royalties payment.

## Motivation

EIP-2981 has been designed to be the most easy to grasp and build on. However as we’ve seen during the discussions and since its finalization in the comments, something really needed is missing: multiple recipients.

For this, it has been said that this should be the role of a Splitter Contract to do the job when receiving payments.

However this has 2 bad sides:

1. being costly for creators, since the payment does not identify for which token it’s made for, creators would have to create one contract per collaboration.
More, some collaboration could involve the same people, but different payout allocations, forcing again another contract deployment (and therefore cost) from the creators.
2. being hard to do accounting on those royalties payment. Because there is actually nothing to identify these transfers as being payment for royalties, people could have a very hard time knowing, understanding and explaining why they received transfer (not everyone knows how to read etherscan, and being dependent on Etherscan API is the opposite of what our space searches to achieve).

…

---

See Draft to read more about the *why* this is needed.

I would love to be able to discuss about this with other builders. I have already poked a few of you about this and got nice feedback and would love to open the discussion with more people and maybe soon propose this draft as a start of EIP.

Any thoughts?

## Replies

**aug2uag** (2021-09-27):

Simon, what’s the intended implementation: is this a wrapper to existing tokens or will an NFT contract need to be deployed with integration to your splitting feature?

---

**dievardump** (2021-09-27):

This is not intended to be implemented by the NFT contract.

The callback is intended to be implement by the `royaltyRecipient` returned by `royaltyInfo(uint256 tokenId, uint256 value) returns (address royaltyRecipient, uint256 amount)`, if it is a contract.

This means this can actually be the NFT Contract, but it must not be it; it can be a random contract, or a splitter contract.

The introspection  and call to the callback is intended to be implemented by Marketplaces contracts at time they send royalties to `royaltyRecipient`, in order to identify the NFT and the payment tokens with the transfer.

