---
source: magicians
topic_id: 10052
title: EIP-5313 Light Contract Ownership
author: fulldecent
date: "2022-07-22"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-5313-light-contract-ownership/10052
views: 2461
likes: 10
posts_count: 10
---

# EIP-5313 Light Contract Ownership

Latest draft: [Create eip-xxx.md by fulldecent · Pull Request #5313 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5313/checks)

## Replies

**SamWilsn** (2022-07-22):

I think you’re in the running for the fastest speedrun of the EIP process ![:rofl:](https://ethereum-magicians.org/images/emoji/twitter/rofl.png?v=12)

---

Serious question though, why not an `isOwner(address)` function? Compatibility with existing implementations?

---

**MicahZoltu** (2022-07-23):

While I agree that `isOwner(address)` would be better, `owner()` is currently a defacto standard within the ecosystem.  Perhaps someone can create another EIP for `isOwner(address) returns (bool)` and `owners() returns (address[])`?  Though, `owners()` perhaps should be paged?

---

**frangio** (2022-07-23):

IMO “ownership” should be only used when it’s a single account. Any kind of “shared ownership” is a more complex arrangement that can’t be described by a list of owners. For example: is it 1-of-N or N-of-M, is there any hierarchy, etc.

---

**MicahZoltu** (2022-07-24):

Yeah, a fair argument here would be that single owner should always be the case, and if you want a more complex multi-owner relationship that should be encapsulated into a separate contract that then is the single owner of the contract in question.  I think I can get behind this argument generally and support only having single owner contracts.

---

**fulldecent** (2022-07-25):

Long-term and big-picture, there is a good argument to use a new and versatile `isAuthorizedAccount(address account)`. And then after broad adoption, standardize it.

But this EIP is specifically so that you can inherit the minimum functionality needed to make your contract compatible with OpenSea or whatever else you need. I don’t control OpenSea and can’t make them design to other interfaces. But I have recently implemented this draft EIP-5313 (`ownerOf() returns (address)`) and it successfully worked to validate a collection on OpenSea.

---

**k06a** (2022-07-26):

In case of complex ownership, owner should be address of contract implementing custom ownership logic ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**fulldecent** (2022-08-02):

Thank you all for the feedback!

This EIP seems to be in a good state. Requesting to move to Last Call status at [Promote EIP-5313 to last call by fulldecent · Pull Request #5389 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5389)

---

**MicahZoltu** (2022-08-03):

I wonder if there is value in defining a return value of `0` as special (meaning the contract is unknowned)?  While one can infer this, it may be nice to standardize that `0` is the standard way to express unknowned so people don’t use other values like `0xdead` and whatnot.

---

Is there value in having a well defined event that is fired whenever ownership changes?  This may be more appropriate for a separate EIP (that perhaps depends on this one), but it does seem like a valuable thing to standardize.

---

**fulldecent** (2022-08-03):

An event is defined in EIP-173. The motivation in EIP-5313 (DRAFT) for not using the event is that it is not the minimal requirement.

---

I do not know of anybody that has implemented EIP-5313 (DRAFT) that would make use of a zero return value. Specifically, OpenSea is today using EIP-5313 (DRAFT) for logins and it does not make special use of a zero return value. For this reason, specification of the meaning for a zero return value would not be minimal and therefore it is not in 5313 (DRAFT)

