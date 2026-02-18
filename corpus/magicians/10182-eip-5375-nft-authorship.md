---
source: magicians
topic_id: 10182
title: EIP-5375 - NFT Authorship
author: samuelemarro
date: "2022-07-30"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-5375-nft-authorship/10182
views: 2626
likes: 5
posts_count: 8
---

# EIP-5375 - NFT Authorship

This is the discussion thread for EIP-5375, an EIP that provides a standardized JSON field for author information, in addition to Author Consent Proofs (ACPs), which prove that an address agreed to be named as the author.

[Link to the PR](https://github.com/ethereum/EIPs/pull/5375)

## Replies

**SamWilsn** (2022-08-09):

It might be useful to add [EIP-165](https://eips.ethereum.org/EIPS/eip-165) support to this EIP.

---

**samuelemarro** (2022-08-09):

~~Definitely, give us a couple days and we’ll add it!~~

Edit: Luca and I have discussed it and we believe that EIP-165 is not necessary, mostly due to two reasons:

- The EIP-165 identifier is computed using contract function signatures, but EIP-5375 does not add any functions;
- Requiring modifications to supportsInterface() would mean that all existing contracts would need to be updated.

---

**samuelemarro** (2022-08-16):

Moving from Draft to Review!

You can find the new PR [here](https://github.com/ethereum/EIPs/pull/5465).

---

**purplehat** (2022-09-13):

If I am understanding correctly the currently proposed standard, `authorInfo` assumes that the entire set of tokens within a given ERC-721-conforming contract all have the same author, which often isn’t the case.

I’d suggest that `authorInfo` be something that is `tokenId`-keyed, in the same way that token URI is.

That is, that the EIP be updated to use `authorInfo(uint256 _tokenId)` instead of a shared `authorInfo`.

---

**samuelemarro** (2022-09-13):

`authorInfo` is not a method of the contract, it’s a field in the JSON document pointed by `tokenURI`/`uri`, which both take the `_tokenId` parameter. In this way, it’s possible to provide id-specific author info.

---

**purplehat** (2022-09-13):

AH–that makes much more sense to me, my misunderstanding there.

One additional thing to clarify, am I understanding correctly that the `consentInfo` field entirely is optional for conformance here (e.g. it can be left out of `authorInfo`)?

---

**samuelemarro** (2022-09-13):

That’s correct, the rationale is that if you only want to provide a claim of who the author is (without any proof), you can do it.

The downside is that you can basically claim anything about who the author is, but the upside is that from a UX POV, you can support EIP-5375 without forcing all users to sign EIP-712 messages. While less secure, this simplifies adoption, since NFT platforms can make ACPs optional.

In my opinion, I think ACPs will end up being like the blue checkmark on Twitter: pretty irrelevant for most people, but extremely important for “celebrities” to distinguish themselves from scammers.

Obviously, a platform can also force all users to sign ACPs, for maximum security.

