---
source: magicians
topic_id: 588
title: "ERC-1169: Multi-Class Fungible Tokens"
author: achon22
date: "2018-06-22"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/erc-1169-multi-class-fungible-tokens/588
views: 1060
likes: 2
posts_count: 6
---

# ERC-1169: Multi-Class Fungible Tokens

This standard allows for the implementation of a standard API for multi-class fungible tokens (henceforth referred to as “MCFTs”) within smart contracts. This standard provides basic functionality to track and transfer ownership of MCFTs.

## Replies

**Ethernian** (2018-06-22):

would you provide more info or link?

thanx!

---

**achon22** (2018-06-22):

Sure, here’s the link to the EIP pull request I made:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/1178)














####


      `master` ← `albertchon:master`




          opened 06:09PM - 22 Jun 18 UTC



          [![](https://avatars.githubusercontent.com/u/20461629?v=4)
            albertchon](https://github.com/albertchon)



          [+148
            -0](https://github.com/ethereum/EIPs/pull/1178/files)













Here’s the proposal: [EIPs/EIPS/eip-1178.md at 1ba1372f8911f12d040b638d1ae1d337738fd77f · albertchon/EIPs · GitHub](https://github.com/achon22/EIPs/blob/1ba1372f8911f12d040b638d1ae1d337738fd77f/EIPS/eip-1178.md)

---

**Ethernian** (2018-06-22):

Why would you like to implement the Multiclass Use Case like *“preferred/common/restricted shares of a company”* in one MCFT instead to use a set of independent separate tokens using existing token standards?

---

**achon22** (2018-06-24):

[@Ethernian](/u/ethernian) Great question.

If one were to use separate tokens to model the different classes, external calls would have to be made. For non-trivial dapps that require maintenance of state in internal variables of the contract, this would result in having to write many getter/setter methods which is cumbersome and expensive to call.

E.g. imagine modeling the conversion of restricted stock in a company to common stock. It would be much easier to write the logic for this if the tokens for these classes were in the same contract.

---

**Ethernian** (2018-06-24):

> conversion of restricted stock in a company to common stock

would you please desdribe typical conversion rules?

- Who should be eligible to set conversion rules?
- Who should be eligible to execute conversion of customer’s stock at some time?
- Is it always "all shares in the class "conversion or it may be applied to selected subset of the class owner?

what about exchanges?

- What token interface should an exchange adopt? Is it similar to existing token interface like transfer/allowance or they must implement more aspects?
- What UI iterface and MCFT token description (ticker) should exchange provide to the customers? Is it different from existing one?

