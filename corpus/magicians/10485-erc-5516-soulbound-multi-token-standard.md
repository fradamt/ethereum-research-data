---
source: magicians
topic_id: 10485
title: "ERC-5516: Soulbound, Multi Token Standard"
author: LucasGrasso
date: "2022-08-22"
category: ERCs
tags: [nft, erc1155, erc5516]
url: https://ethereum-magicians.org/t/erc-5516-soulbound-multi-token-standard/10485
views: 2996
likes: 7
posts_count: 8
---

# ERC-5516: Soulbound, Multi Token Standard

# ERC5516

Co-Authored with: [@MatiArazi](/u/matiarazi)

---

This is the discussion thread for [EIP-5516](https://eips.ethereum.org/EIPS/eip-5516) (Currently in Draft):

This EIP proposes a standard interface for non-fungible double signature Soulbound multi-tokens. Previous account-bound token standards face the issue of users losing their account keys or having them rotated, thereby losing their tokens in the process. This EIP provides a solution to this issue that allows for the recycling of SBTs.

This EIP was inspired by the main characteristics of the [EIP-1155](https://eips.ethereum.org/EIPS/eip-1155) token and by articles in which benefits and potential use cases of Soulbound/Accountbound Tokens (SBTs) were presented. This design also allows for batch token transfers, saving on transaction costs. Trading of multiple tokens can be built on top of this standard and it removes the need to approve individual token contracts separately. It is also easy to describe and mix multiple fungible or non-fungible token types in a single contract.

EDIT (23/01/26):

After giving some thought to this EIP, and given that [Update ERC-5516: Move to Draft by LucasGrasso · Pull Request #1372 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1372) is merged, this are the changes applied to the interface:

- Remove compatibility with EIP-1155 due to major breaking changes.
- Remove double signature functionality to allow for cheaper obtainance of tokens.
- Overhauling of the interface so to minimalize it while mantaining the original goal of this EIP.
- Re-implementation of the standard.

## Replies

**MatiArazi** (2022-08-30):

It was great working with you [@lucasgrasso](/u/lucasgrasso) on this one, feedback is appreciated!

---

**LucasGrasso** (2022-08-30):

An honor to work with you [@MatiArazi](/u/matiarazi).

---

**DonMartin3z** (2022-09-03):

I am refering this thread in my work of implementation and use cases for SBT. I would like to share the concept before post the thread.

---

**MatiArazi** (2022-09-13):

Thank you!

Any doubts comment here

---

**ndajiya** (2022-12-08):

How does a lost account(lost key) recycle a SBT?

---

**LucasGrasso** (2022-12-08):

[@ndajiya](/u/ndajiya)

The token, being compliant to the ERC-1155 Standard, has the feature of it being able to be trabsferred to multiple accounts. Taking this into consideration, you could send the SBT to a multi-sig contract, or if you can prove that you own both the lost account and your new account, the issuer may re-transfer the token. Despite this, the standard does not provide a methodology to recover the SBTs, it just gives these recommendations.

---

**LucasGrasso** (2025-11-26):

I’ve been wanting to resume working on this EIP and after revising I thought it would be a good idea to minimize the interface whilst keeping the main idea intact. I would appreciate if you could check the [draft PR](https://github.com/ethereum/ERCs/pull/1372) and give your opinions

- Remove compatibility with EIP-1155 due to major breaking changes.
- Remove double signature functionality to allow for cheaper obtainance of tokens.
- Overhauling of the interface so to minimalize it while mantaining the original goal of this EIP.
- Re-implementation of the standard.

Im also unfamiliar with the process of updating the EIP, so would appreciate guidance on that.

