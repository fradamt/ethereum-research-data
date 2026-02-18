---
source: magicians
topic_id: 8687
title: "EIP-4931: Generic Token Upgrade Standard"
author: john-peterson
date: "2022-03-22"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-4931-generic-token-upgrade-standard/8687
views: 2067
likes: 1
posts_count: 3
---

# EIP-4931: Generic Token Upgrade Standard

Token contract upgrades typically require each asset holder to exchange their old tokens for new ones using a bespoke interface provided by the developers. EIP-4931 allows for the implementation of a standard API for ERC20 token upgrades. This standard specifies an interface that supports the conversion of tokens from one contract (called the “source token”) to those from another (called the “destination token”), as well as several helper methods to provide basic information about the token upgrade. There is also an extension optionally available to provide downgrade functionality. Upgrade contract standardization will allow centralized and decentralized exchanges to conduct token upgrades more efficiently while reducing security risks and enabling a frictionless user experience for anyone holding an ERC20 asset during an upgrade.

The proposal - [EIP-4931](https://github.com/ethereum/EIPs/pull/4931)

[EIP-4931 - Generic Token Upgrade Standard Reference Implementation](https://github.com/coinbase/eip-token-upgrade)

## Replies

**SamWilsn** (2022-04-05):

Would `previous` and `next` be better descriptions for the contracts (instead of `source` and `destination`)?

Since `ratio()` returns a tuple, it somewhat limits the conversion rate, and I think its purpose is served by `computeUpgrade` and `computeDowngrade`. I think it could be removed?

---

**cygnusv** (2022-04-13):

> Would previous and next be better descriptions for the contracts (instead of source and destination)?

Perhaps, we went with `source` and `destination` because they were more immediate terms for us at that moment, but there may be other alternatives, e.g., previous/next, original/updated, etc. I guess this may be fairly subjective.

> Since ratio() returns a tuple, it somewhat limits the conversion rate, and I think its purpose is served by computeUpgrade and computeDowngrade. I think it could be removed?

The purpose of `ratio()` is informational (that is, being able to clearly state from the contract that this upgrade is, say, a 3-to-2 conversion), but `ratio()` is not meant to be used directly, as there are many pitfalls for users of the contract that can be solved if the amount that wants to be converted is tried first via `computeUpgrade` and `computeDowngrade`.

