---
source: magicians
topic_id: 12689
title: "EIP-6372: Contract Clock"
author: Amxx
date: "2023-01-25"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-6372-contract-clock/12689
views: 1955
likes: 4
posts_count: 2
---

# EIP-6372: Contract Clock

Following the work on EIP-5805, we decided to spin off the clock part as its own EIP



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/6372)














####


      `master` ← `Amxx:clock`




          opened 12:42PM - 25 Jan 23 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/2/25ecfec94e89e81e1553723f9a30aef27c4e1627.jpeg)
            Amxx](https://github.com/Amxx)



          [+92
            -0](https://github.com/ethereum/EIPs/pull/6372/files)







Following discussion on EIP-5805, we decided to spin of clock part of the interf[…](https://github.com/ethereum/EIPs/pull/6372)ace as its own EIP.

EIP-5805 will add a dependency on this once merged.

## Replies

**sbacha** (2023-06-29):

Hey [@Amxx](/u/amxx) I have a few questions/suggestions if you dont mind:

Why state that it must be “not decreasing” — why not say monotonically increasing?

Their does not seem to be support for sub second precision, which is actually available in Quorum.

I have seen contracts that actually use different time standards than the normal civilian UTC

I have seen use cases for having timestamps in WAD



      [github.com](https://github.com/IPOR-Labs/ipor-protocol/blob/main/contracts/libraries/Constants.sol)





####



```sol
// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.16;

library Constants {
    uint256 public constant MAX_VALUE =
        115792089237316195423570985008687907853269984665640564039457584007913129639935;

    uint256 public constant D18 = 1e18;
    uint256 public constant D21 = 1e21;
    int256 public constant D18_INT = 1e18;
    uint256 public constant D36 = 1e36;
    uint256 public constant D54 = 1e54;

    uint256 public constant YEAR_IN_SECONDS = 365 days;
    uint256 public constant WAD_YEAR_IN_SECONDS = D18 * YEAR_IN_SECONDS;
    int256 public constant WAD_YEAR_IN_SECONDS_INT = int256(WAD_YEAR_IN_SECONDS);
    uint256 public constant WAD_P2_YEAR_IN_SECONDS = D18 * D18 * YEAR_IN_SECONDS;
    int256 public constant WAD_P2_YEAR_IN_SECONDS_INT = int256(WAD_P2_YEAR_IN_SECONDS);

    uint256 public constant MAX_CHUNK_SIZE = 50;
```

  This file has been truncated. [show original](https://github.com/IPOR-Labs/ipor-protocol/blob/main/contracts/libraries/Constants.sol)










I also have a proposal still in draft for a different timestamp unit

Finally, [GitHub - bokkypoobah/BokkyPooBahsDateTimeLibrary: Gas-Efficient Solidity DateTime Library](https://github.com/bokkypoobah/BokkyPooBahsDateTimeLibrary) is the Gold standard in terms of date and time libraries out there. Its been rigorously tested and audited. Its based off of the US Naval Observatory specifications and fwiw NTP is directly dependent upon them for accuracy etc.

If your available to talk on telegram my username is @sambacha

