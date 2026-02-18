---
source: magicians
topic_id: 5391
title: ERC-2770 Meta-Transactions Forwarder Contract
author: alex-forshtat-tbk
date: "2021-02-21"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/erc-2770-meta-transactions-forwarder-contract/5391
views: 2545
likes: 0
posts_count: 2
---

# ERC-2770 Meta-Transactions Forwarder Contract

Starting a discussions topic for ERC-2770

## Replies

**Amxx** (2021-02-22):

Note: I’ll be using [this implementation](https://github.com/opengsn/gsn/blob/master/packages/contracts/src/forwarder/Forwarder.sol) as a reference for my discussion.

I really don’t understand the whole point of preparing the EIP712 structure for extra content. This increases the complexity of the contract, and amount of data that has to be passed (domain separator) … which has a gas cost.

Adding support for typesHashes is not a security issue, but it doesn’t bring anything to the table since the additional fields are disregarded. Line 63 doesn’t change its behavior depending on the presence of suffixData.

Why pay the price of verifying it is signed properly and then not use it ?

If the idea is that the interface is future proof, so that future implemntation could use the same interface in a way that make use of this data, I honestly think you are going in the wrong direction.

My personal opinion is that there should be only ONE common (singleton) forwarder, at the same address on all networks, for this to even hope to be successful. Having multiple forwarder that should all be whitelisted by all apps causes governance issues, and will never happen. Also, if you state that the forwarder is going to be changed, people will just wait for it to be final before adopting it. Why should I make my contract compatible with the current forwarder if its going to be deprecated anyway ?

I’d personally drop this extra-data & multiple typeHashes nonsense in favor of features that would actually improve the forwarder to a point where it meets most usecase and can be envisionned as somehow futur-proof. Out of order execution of meta-tx is IMO one of such features.

If I remeber correctly, [@wighawag](/u/wighawag) proposed a mechanism where the the 256bits nonce was separated into two 128bits integer, one being a “sub-nonce” identifier, and the other one being the value for this subnonce. Keeping le leftmost 128bits to 0 would replicate the current behavior, and setting these leftmost 128bits to any value would allow to create independent timelines where meta-tx can be ordered independently of the main (and of any other) timeline. [This is how it could look like](https://github.com/Amxx/openzeppelin-contracts/blob/feature/OutOfOrderForwarder/contracts/metatx/OutOfOrderForwarder.sol)

