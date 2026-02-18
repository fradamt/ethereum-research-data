---
source: magicians
topic_id: 14065
title: "Draft: ERC-6889: Expiring EIP-20 Approvals"
author: z.ftm
date: "2023-04-30"
category: ERCs
tags: [erc, token]
url: https://ethereum-magicians.org/t/draft-erc-6889-expiring-eip-20-approvals/14065
views: 530
likes: 0
posts_count: 1
---

# Draft: ERC-6889: Expiring EIP-20 Approvals

Hey everyone, I am drafting an extension to EIP-20, which would allow for expiring ERC20 approvals.

This is my first time creating an EIP, so I would appreciate any review. The following is [this document](https://github.com/Pokesi/EIPs/blob/master/EIPS/eip-6889.md).

## Abstract

I propose to extend the EIP-20 standard with a time-restricted approval system. The owner of a FT (fungible token) would approve spending of their tokens using the `approve()` function, which would be modified to accept an expiry parameter. The approved tokens would be transferrable by the approvee until the time specified in the `approve()` call.

## Motivation

EIP-20 tokens have risen massively in popularity over the years, with most having a real-world, dollar, value. For this reason, EIP-20 tokens have become a big target for malicious actors, and EIP-20’s approval specifications allow for many attack vectors. The main attack vector for malicious actors is smart contract vulnerabilities, which regards smart-contracts capable of using user tokens can being used to steal those tokens by attackers [e.g. SushiSwap RouterProcessor2](https://www.theblock.co/post/225473/sushiswap-hack).

The change I propose is: instead of being infinietly approved, token approvals have a set timestamp/block number at which the spender cannot spend the tokens.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

Expiring EIP-20 **MUST** implement the `IERC6889` interface:

```solidity
// SPDX-License-Identifier: CC0-1.0

pragma solidity ^0.8.18;

/**
 * @dev EIP-20 Token standard, optional approval expiry extension
 * ERC20 token that when approved, cannot be spent after a certain timestamp.
 * This is to protect users of ERC20 tokens against approval-related smart contract
 * vulnerabilites.
 * This extension ensures long-term security of ERC20 tokens, while allowing spending
 * and not requiring revoke transactions.
 *
 * A default interval value should be set in the implementation of this interface
 * so legacy approve(address, uint256) calls can still be used with an expiry of
 * a developer-defined expiry interval. `allowance()` should also be modified to return
 * 0 when an approval has expired.
 */

interface IERC6889 {
    /**
     * @dev Emmited when a timed approval occurs
     */

    event Approval(address indexed _owner, address indexed _spender, uint256 _value, uint256 _expiry);

    /**
     * @dev Returns the expiry of approval from `_owner` to `_spender`
     */
    function expiry(address _owner, address _spender) external view returns (uint256 expiry);

    /**
     * @dev Approve usage of `_value` tokens to `_spender` until `_expiry`
     *
     * Requirements:
     *  - _value is less than or equal to the senders value
     *  - _expiry is greater than or equal to the current block.timestamp
     *
     * Emits an `Approval()` event
     */
    function approve(address _spender, uint256 _value, uint256 _expiry) external returns (bool success);
}
```

## Rationale

### Approve

When approving, a user needs to specify the spender, the amount of tokens, and the expiry time. After the expiry timestamp, the spender’s access to the tokens is revoked.

## Backwards compatiability

This standard is compatiable with EIP-20.

## Test cases

…

## Reference implementation

…

## Security considerations

…

## Copyright

Copyright and related rights waived via CC0.
