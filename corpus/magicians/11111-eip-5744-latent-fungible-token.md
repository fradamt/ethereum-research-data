---
source: magicians
topic_id: 11111
title: "EIP-5744: Latent Fungible Token"
author: mds1
date: "2022-09-29"
category: EIPs
tags: [token]
url: https://ethereum-magicians.org/t/eip-5744-latent-fungible-token/11111
views: 2699
likes: 0
posts_count: 5
---

# EIP-5744: Latent Fungible Token

This thread is to discuss EIP-5744: Latent Fungible Token. The proposal can be found here: [Add EIP-5744: Latent Fungible Tokens by mds1 · Pull Request #5744 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5744)

## Replies

**SamWilsn** (2022-11-18):

Some small non-formatting related comments:

- Perhaps matureBalanceOf instead of balanceOfMatured? I think that has slightly better grammar.
- Have you looked at EIP-1132?
- Creating and returning an entire array of MintMetadata might be gas intensive. Would a length function plus a get-at-index function be better?
- I’m not a huge fan of calling the metadata “mints”. To borrow some terminology from established finance, maybe you could go with a VestingCliff or something similar?

---

**SamWilsn** (2022-11-25):

So I think I completely misunderstood the point of this EIP. The idea isn’t to prevent the transfer of some EIP-20 token for X amount of time, but rather to conceptually separate “immature tokens” from “mature tokens” where “mature tokens” have some utility that the “immature tokens” don’t?

If my new understanding is correct, perhaps this is better suited as an [EIP-1155](https://eips.ethereum.org/EIPS/eip-1155) family of tokens, where the fungible tokens are tracked at id `0x0`, and each mint is a 1-of-1 token with its own metadata and transfer rules?

---

**SamWilsn** (2022-12-16):

We’re trying a new process where we get a volunteer peer reviewer to read through your proposal and post any feedback here. Your peer reviewer is [@enehizy](/u/enehizy)!

If any of this EIP’s authors would like to participate in the volunteer peer review process, [shoot me a message](https://ethereum-magicians.org/new-message?username=SamWilsn&title=Peer+Review+Volunteer)!

---

[@enehizy](/u/enehizy) please take a look through [EIP-5744](https://eips.ethereum.org/EIPS/eip-5744) and comment here with any feedback or questions. Thanks!

---

**sullof** (2023-07-04):

For compatibility with ERC20, I would expect that `balanceOf` returns the balance of all the tokens that are matured, i.e., that can be transferred. So, it would make more sense to have an `unmaturedBalanceOf` function to returns the full balance of the user, without causing issues to any actor who attempts to make a transfer based on `balanceOf``.

