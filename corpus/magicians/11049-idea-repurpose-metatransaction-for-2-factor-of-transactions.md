---
source: magicians
topic_id: 11049
title: "Idea: repurpose metatransaction for 2-factor of transactions, and a possible added benefit of dis-intermediate ERC20.approvals"
author: hellwolf
date: "2022-09-26"
category: Magicians > Primordial Soup
tags: [token]
url: https://ethereum-magicians.org/t/idea-repurpose-metatransaction-for-2-factor-of-transactions-and-a-possible-added-benefit-of-dis-intermediate-erc20-approvals/11049
views: 456
likes: 1
posts_count: 1
---

# Idea: repurpose metatransaction for 2-factor of transactions, and a possible added benefit of dis-intermediate ERC20.approvals

# Background

In current convention,

> Meta Transactions are transactions who’s data is created and signed off-chain by one person and executed by another person who pays the gas fees.

It was generally created for no-gas-token UX experiences. Regardless of its actual adoption, the efforts have yielded lots of development and tooling for it. The purpose of this discussion thread is to propose a alternative use of the meta transaction technique but for an entirely different purpose, namely 2-factor transactions and a possible benefit of dis-intermediate ERC20.approvals

# Short Description

A meta transaction could be re-purposed to: a transaction intention signed off-chain by one person and executed by **the same person** via a contract related to a trust intermediate who could have the opportunity to offer the person security advice before it would through.

In order to make it actually work for security purpose, the capability of making transactions via the token contract directly must be turned off (although likely as an opt-in per each account of the token); hence making the two token transactions 2-factor.

Here is an example:

- Bob opt-in the 2-factor token transaction feature, and designate a hypothetical trustedtxs.eth as the sole approver of his token transactions (known as security advisor).
- Bob signs a ERC20.transfer intention and forwards it to “https://trustedtxs.eth” (e.g. a ipfs/swarm hosted site for temper proof).
- Bob is prompted to review his supposed transaction intention at https://trustedtxs.eth. TrustedTxs provides security advises to Bob by analyzing the transaction intention.
- Bob broadcasts the transaction on https://trustedtxs.eth through a known trustedtx on-chain contract (part of the opt-in onchain record) with its own gas tokens.
- Bob concludes his transaction.

# Implications

- The role of security advisors could be introduced to token users with little or now decentralization compromises.

should a security advisor go rogue, it should still not have the capability of damaging the user, a user in this situation should have a independently but equally secure channel for opting-out from it, so that his transactions could resume.

It does raise some UX friction, but 2-factor in general does.
We need a wallet independent and open-standard approach. You may argue why we cannot simply let metamask do the “security advisories”? Because they don’t, otherwise there will be less incentive for creating this discussion thread.
Because of the long-term relationships established between *security advisor* and token users, token user may further delegate some responsibilities to the *security advisor*, e.g.:

- For ERC20 approvals, with additional token logic extensions, a “security advisor” could turn off token approvals for token users in one transaction, should the approved contract found a severe security issue.

Thanks,

---

Disclaimer: I am from [Superfluid protocol](https://github.com/superfluid-finance/protocol-monorepo/), a protocol that adds super powers to token standards, called Super Token, a ERC20-compatible with features including new semantics to ERC20 tokens including 1to1 flows, and 1toN mass distributions; token-native batch call supports; etc. I’m interested in this topic since I am not very happy with the status quo of the ERC20 security model, and I’d like to us to improve it through the EIP process and eventually also get it integrated to Super Token standards.
