---
source: magicians
topic_id: 1955
title: ABI Specification Working Group
author: fubuloubu
date: "2018-11-20"
category: Working Groups
tags: [interfaces, abi]
url: https://ethereum-magicians.org/t/abi-specification-working-group/1955
views: 918
likes: 7
posts_count: 5
---

# ABI Specification Working Group

Hey all!

We started the ETH ABI Working Group, which is aiming to standardize the ABI Interface Specification for Compilers, Web3 libraries, and other tools. If you are in one of these groups that consumes the ABI specification, please let me know so I can add you to this working group.

We also aim to create a standard test suite for ABI encoding/decoding that all of these groups can use to supplement their testing suite (and eventually merge all core featureset tests!).

Organization: https://github.com/ethabi

## Replies

**Ethernian** (2018-11-21):

I have gathered a small and focused task force for whisper specification.

It could be part of this group, imho.

---

**fubuloubu** (2018-11-21):

Perhaps we could share approaches, but I think being focused is a strength. Contract ABI and Whisper don’t strictly affect each other.

---

**Ethernian** (2018-11-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> Contract ABI and Whisper don’t strictly affect each other.

for sure not. It it is ABI specification group only.

---

**xinbenlv** (2022-11-11):

Hi from 2022,

Here is one other latest case demonstrating it’s good for having an ABI representation in EIP spec



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/5805#discussion_r1020490378)














#### Review by
         -


      `master` ← `Amxx:vote_with_delegation`







LGTM!. While I reserve my opinion on this particular point but respect this is a[…](https://github.com/ethereum/EIPs/pull/5805)uthor's discretion at the technical choice made in this proposal.

That said, this different understanding about ERC20's `approval` whether they mean to be `payable` or `nonpayable` or _unspecified_ seem to hard to be represented in Solidity, and hence a good point to use ABI actually

