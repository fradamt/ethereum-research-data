---
source: magicians
topic_id: 3347
title: "EIP-2069: Recommendation for using YAML ABI in specifications"
author: axic
date: "2019-06-02"
category: EIPs > EIPs informational
tags: []
url: https://ethereum-magicians.org/t/eip-2069-recommendation-for-using-yaml-abi-in-specifications/3347
views: 3225
likes: 12
posts_count: 12
---

# EIP-2069: Recommendation for using YAML ABI in specifications

Discussion URL for

https://github.com/ethereum/EIPs/pull/2069

## Replies

**tjayrush** (2019-06-03):

I find this a very interesting idea.

It would be excellent if I could scrape the EIP repo and easily parsed standards. I build tools that benefit immeasurably from the standards. I could support them all (or any portion I wish) if the process was more easily automated.

Why not even go further and automate the process to scrape the EIP repo looking for these finalized standards and lay them down into some immutable file store? Finalized EIPs are supposed to never change. We should store them (in machine readable format) at a hash and add the hash to the repo.

---

**fubuloubu** (2019-06-07):

Isn’t YAML a superset of JSON? Couldn’t we just *do* this?

---

**axic** (2019-06-09):

The EIP/ERC explains this and the motivation. YAML is a superset, but if we use the JSON-compatible features, then we get the benefit of in-line comments, perhaps more readable structure and that the YAML spec can be converted to the JSON undrestood by tools.

---

**fubuloubu** (2019-06-09):

Hmm, this seems to be of primary benefit to situations where the json is not automatically generated, but human managed or created. Things like test cases and external interfaces come to mind. Perhaps extending this spec to cover some of the common test case formats would be of value? This spec could also be used when testing tools that work with ABIs in test cases for those tools.

---

**esaulpaugh** (2019-06-10):

Here are some of my ABI test cases, based on the [ethers.js](https://github.com/ethers-io/ethers.js)/[tests](https://github.com/ethers-io/ethers.js/tree/master/tests)/[tests](https://github.com/ethers-io/ethers.js/tree/master/tests/tests)/ **contract-interface-abi2.json.gz** test case format (minus the solidity-specific properties): https://github.com/esaulpaugh/headlong/blob/master/src/test/resources/tests/headlong/tests/abi_tests.json

---

**axic** (2019-06-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> Hmm, this seems to be of primary benefit to situations where the json is not automatically generated, but human managed or created.

The whole point of the proposal is to move on from Solidity interfaces to defining interfaces as YAML. This would reduce the dependency on Solidity.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> Things like test cases and external interfaces come to mind. Perhaps extending this spec to cover some of the common test case formats would be of value? This spec could also be used when testing tools that work with ABIs in test cases for those tools.

I guess it could be, but I’m not sure.

---

**fubuloubu** (2019-06-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> The whole point of the proposal is to move on from Solidity interfaces to defining interfaces as YAML. This would reduce the dependency on Solidity.

I didn’t make that connection before, although it is spelled out plainly. This is definitely a benefit, but not necessarily solving all the problems other languages have with the current way ERC specifications are made.

For example, many people lately have been defining ERCs with the heavy use of dynamic arrays arguments, a feature Vyper doesn’t currently support (but we are working on it). My hope would be that people would define single-size arguments in their interfaces, but people make use of more advanced features like this pretty pervasively. And even more generally, the use of mixedCamelCase in defining the names of everything has forced us to adopt that style over the more Pythonic snake_case style that Python linting tools expect.

Not that we should (or can) remove these choices that derived originally from the use of the Solidity language in defining many early ERCs, but there are many more subtle decisions made which cannot be resolved by creating a more generic specification format, although I do welcome the intent behind doing that.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> Things like test cases and external interfaces come to mind. Perhaps extending this spec to cover some of the common test case formats would be of value? This spec could also be used when testing tools that work with ABIs in test cases for those tools.

I guess it could be, but I’m not sure.

Another thing that comes to mind is the EIP190/1123 ethPM packaging format, which leverages JSON, and people will occasionally use to define packages manually for testing purposes, etc.

---

**axic** (2019-06-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> This is definitely a benefit, but not necessarily solving all the problems other languages have with the current way ERC specifications are made.
>
>
> For example, many people lately have been defining ERCs with the heavy use of dynamic arrays arguments, a feature Vyper doesn’t currently support (but we are working on it).

Actually on that note the other benefit would be that only features included in the Contract ABI can be specified and Solidity specific features cannot. However, dynamic arrays are “part of the Contract ABI” as long as we consider the spec in the Solidity documentation the canonical one. Unless this one is merged [Create contract ABI encoding draft by axic · Pull Request #1605 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/1605) (we’ve actually discussed and hope to finalise and merge it next week)

---

**fubuloubu** (2019-06-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> Unless this one is merged https://github.com/ethereum/EIPs/pull/1605  (we’ve actually discussed and hope to finalise and merge it next week)

That one should definitely be merged. Perhaps the Solidity examples in that spec could be JSON/YAML ones instead?

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> Actually on that note the other benefit would be that only features included in the Contract ABI can be specified and Solidity specific features cannot.

I agree this is a very good reason why this proposal will help improve the formulation of ERCs.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> However, dynamic arrays are “part of the Contract ABI” as long as we consider the spec in the Solidity documentation the canonical one.

As they should be. I wasn’t advocating for changing that part of the ABI spec, more thinking it would be good guidance for the construction of ERCs not to use dynamic arrays by default. It complicates the implementation’s handling of the ERC, and uses a newer feature that IIRC is only available with ABIEncoderV2 in Solidity.

---

**axic** (2019-06-13):

Change the format slightly to support “interface” names:

```auto
# The transfer function. Takes the recipient address
# as an input and returns a boolean signaling the result.
ERC20:
- name: transfer
  type: function
  stateMutability: nonpayable
  inputs:
  - name: recipient
    type: address
  - name: amount
    type: uint256
  outputs:
  - name: ''
    type: bool
- name: balance
  type: function

ERC2020:
- name: transfer
  type: function
- name: balance
  type: function
```

Also created a dumb Javascript tool to convert that into a Solidity interface: https://github.com/axic/yamabi

It translates the above to:

```auto
interface ERC20 {
  function transfer(address recipient, uint256 amount)  returns (bool);
  function balance();
}

interface ERC2020 {
  function transfer();
  function balance();
}
```

---

**metaver5o** (2023-03-13):

OMG this is soo underrated!

please VOTE UP! #YAMLFTW

