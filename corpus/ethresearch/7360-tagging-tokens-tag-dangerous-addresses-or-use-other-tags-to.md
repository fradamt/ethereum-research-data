---
source: ethresearch
topic_id: 7360
title: Tagging Tokens - Tag dangerous addresses or use other tags to signal other situations
author: RandomDecryptor
date: "2020-05-05"
category: Applications
tags: []
url: https://ethresear.ch/t/tagging-tokens-tag-dangerous-addresses-or-use-other-tags-to-signal-other-situations/7360
views: 2107
likes: 0
posts_count: 3
---

# Tagging Tokens - Tag dangerous addresses or use other tags to signal other situations

## Summary

Tagging tokens provide a simple way, using compatibility with ERC-20 tokens, to tag certain ethereum addresses.

This allows users of the ethereum network to tag addresses with the tagging tokens they want.

## Tagging Tokens

With all the scams appearing related to cryptocurrencies is more important than ever to for users to know if they are interacting with safe addresses or not.

Tagging tokens will allow users to signal certain addresses as dangerous or trusted, using simple compatibility with ERC-20 tokens.

Many other possible tags could also exist to signal exchange addresses, known scams, invalid / abandoned contracts, trusted contracts, etc.

Tags (tagging tokens) are a subset of ERC-20 tokens, following the same interface, but with the following restrictions:

- One address A can only tag another address B with a certain tag once;
- One address can be tagged with many different tags;
- The tag tokens are not transferable, that is, operations that would allow a user to transfer a token after receiving it are blocked (transfer, transferFrom and approve);
- Only the user that does a tagging can remove it, that is, if address A has tagged address B previously, only address A can remove its tagging from address B.
- The total supply of the token (that corresponds to the Tag) is increased by 1 for each tagging;
- The total supply of the token is reduced by 1 for each removal of a tagging;

Will also be possible for users to create their own Tags, so they or other people can use.

Users can also send simple messages to each other using tagging tokens, but not the best purpose for it.

## Economics

To avoid spam and specially to avoid revenge tagging, each tagging will have a certain cost (**TAG-COST**).

For example, if a user Alice is tricked into sending Ether into address of user Bob, for something that Bob never delivers, Alice can tag that Bob’s address with the SCAMMER Tag.

Bob could be tempted to reciprocate and tag also Alice address. That would cost *TAG-COST* for Alice and also *TAG-COST* for Bob.

But, if Bob had tricked more users, say 1000 users that would also tag his address with the SCAMMER tag, to reciprocate he would have to pay 1000 x *TAG-COST*. So a big expense for him and not feasible in most cases, while not costing almost anything for an individual user.

At this stage, we are thinking of setting the TAG-COST as 0.005 Eth (US $1, at the time this document was written), a reasonable number for an individual user, but for a scammer like Bob, the cost would rise very fast. As you can confirm on the following figure:

[![Figure_1_Cost_Of_Tagging](https://ethresear.ch/uploads/default/original/2X/9/956a4c8556c3cb99d1cd8e57db987bc587a2d94e.png)Figure_1_Cost_Of_Tagging640×480 17.4 KB](https://ethresear.ch/uploads/default/956a4c8556c3cb99d1cd8e57db987bc587a2d94e)

The cost, while minimal, will also avoid people spamming the Ethereum network, if they don’t really need this.

## Implementation

The current test implementations (on [Tagged](https://www.tag.gd/test) and [TaggdNg](https://www.tag.gd/test2), with a more modern interface), allows users to support all these functions already.

They include also the possibility for users that **create** a Tag (tagging token) to receive a commission from other users that use that tag for their taggings.

## Future possibilities

In the future, through information gathered from the tagged addresses, we hope to help improve access to the Ethereum network, helping signaling dangerous or scammer addresses (or simply malfunctioning contracts), so users avoid sending Ethereum (or other tokens) to those addresses, with the help of the Ethereum community.

## Replies

**owocki** (2020-05-10):

Have you seen this? This project is already active and in use by metamask https://github.com/MetaMask/eth-phishing-detect

Slightly diff architecture and approach tho

---

**RandomDecryptor** (2020-05-10):

Good tip owocki!

A little different from my objective here, as I want it to be available directly on the blockchain first, so any wallets and users can check it.

I think [etherscan.io](http://etherscan.io), also has something more similar to my idea with the possibility to associate any tag to an address on their site, but sadly only on their site, not on the blockchain.

