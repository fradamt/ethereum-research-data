---
source: magicians
topic_id: 9938
title: "ERC-5247: Executable Proposal Standard"
author: xinbenlv
date: "2022-07-14"
category: EIPs
tags: [erc, governance, dao]
url: https://ethereum-magicians.org/t/erc-5247-executable-proposal-standard/9938
views: 2163
likes: 1
posts_count: 3
---

# ERC-5247: Executable Proposal Standard

Propose a standard for executable proposal.

https://github.com/ethereum/EIPs/pull/5247

## Replies

**numtel** (2022-08-25):

Interesting proposal. I implemented a multi-transaction proposal election system a few months ago for my democratic.capital website in the following contract:



      [github.com](https://github.com/numtel/democratic-capital/blob/master/contracts/ElectionBase.sol)





####



```sol
// SPDX-License-Identifier: MIT
pragma solidity 0.8.13;

import "./AddressSet.sol";
using AddressSet for AddressSet.Set;
import "./VoteSet.sol";
using VoteSet for VoteSet.Data;
import "./BytesLib.sol";
using BytesLib for bytes;

import "./ChildBase.sol";

abstract contract ElectionBase is ChildBase {
  mapping(address => VoteSet.Data) elections;
  mapping(address => bytes[]) invokeData;
  AddressSet.Set proposals;
  bytes[] public allowedInvokePrefixes;

  struct ProposalDetails {
    address key;
```

  This file has been truncated. [show original](https://github.com/numtel/democratic-capital/blob/master/contracts/ElectionBase.sol)










One of the key features that I added was to allow proposals to interact with contracts deployed from factories within the same proposal by implementing an address rewriter. I’m not saying it’s a perfect implementation but it seems very useful when allowing multiple transactions in a proposal.



      [github.com](https://github.com/numtel/democratic-capital/blob/master/contracts/InvokeRewriter.sol)





####



```sol
// SPDX-License-Identifier: MIT
pragma solidity 0.8.13;
import "./IVerifiedGroupFactory.sol";

import "./BytesLib.sol";
using BytesLib for bytes;

contract InvokeRewriter {
  function rewrite(bytes memory data, IVerifiedGroupFactory origin, address group, uint startChildCount) external view returns(address, bytes memory) {
    for(uint i = 0; i < data.length - 20; i++) {
      uint point = addrIndex(uint8(data[i]));
      if(point != 255 &&
         data[i] == data[i+1] &&
         data[i] == data[i+2] &&
         data[i] == data[i+3] &&
         data[i] == data[i+4] &&
         data[i] == data[i+5] &&
         data[i] == data[i+6] &&
         data[i] == data[i+7] &&
         data[i] == data[i+8] &&
```

  This file has been truncated. [show original](https://github.com/numtel/democratic-capital/blob/master/contracts/InvokeRewriter.sol)










See my documentation for an example use case of these contracts:

democratic.capital/docs/create-proposal.html

---

**xinbenlv** (2022-09-06):

Thank you for the suggestion. Let me take a look

