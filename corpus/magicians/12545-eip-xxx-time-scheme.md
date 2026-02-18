---
source: magicians
topic_id: 12545
title: EIP-XXX Time Scheme
author: xinbenlv
date: "2023-01-12"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-xxx-time-scheme/12545
views: 631
likes: 0
posts_count: 1
---

# EIP-XXX Time Scheme

Motivation: many of the recent EIPs and development require a specification of what time scheme is being used. For example, in Voting, a snapshot of voting weight will only be meaningful if there is a sense of time-point. Also, for time-delay or recurring payment, it’s important to align between Smart Contract and its callers what time scheme they are used. The most often used are `blocknum` and `timestamp` which is made available in EVM. But we can leave to future extension for other type of time scheme.

# EIP-XXX Time Scheme

## Specification

```auto
enum TimeSchemeOption {
  blocknum = 0;
  timestamp = 1;
};

interface ERCTimeScheme {
  function defaultTimeScheme() external pure returns(TimeSchemeOption);
}
```

## Ref Impl

```auto
contract Foo is ERCTimeScheme, ERC1202, ERC5805, ERC5732 {
    function defaultTimeScheme() external pure returns(TimeSchemeOption) {
      return TimeSchemeOption.blocknum;
   }
}
```

This help ensuring whenever a time is being used, the scheme is acquirable and shall be consistent across different functions.

Complying contracts of [EIP-1202](https://eips.ethereum.org/EIPS/eip-1202) probably need to align with the same sense of time too. The [ERC-5007: Time NFT, ERC-721 Time Extension](https://eips.ethereum.org/EIPS/eip-5007) however choose to use int64 for unix stamp.
