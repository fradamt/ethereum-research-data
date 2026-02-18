---
source: magicians
topic_id: 1639
title: "Update on ERC902: Validated Token"
author: expede
date: "2018-10-21"
category: EIPs
tags: [erc-1066, validation, erc-902]
url: https://ethereum-magicians.org/t/update-on-erc902-validated-token/1639
views: 3274
likes: 2
posts_count: 2
---

# Update on ERC902: Validated Token

Hi everyone ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=15)

This is a bit of an oldie by EIP standards, but I was in there bringing the formatting of [ERC902](https://eips.ethereum.org/EIPS/eip-902) up to date, and figured that it couldn’t hurt to open this one up for discussion on Ethereum Magicians. This has the added bonus of this providing a `discussions-to` ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=15)

In summary, ERC902: Token Validation is a standard for sharable, *chainable*, [erc-1066](/tag/erc-1066) compatible, on-chain token validation. It has applications for security tokens (ex. [erc-1400](/tag/erc-1400)), NFTs, “restricted” ERC20s, shared or maintainable whitelists, the full decentralization of control behaviour to a clear on-chain process, and so on.

*Comments and feedback are very welcome,* especially as we begin to consider moving this closer to `LAST_CALL`.


      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-902)





###










# Interface

```solidity
interface TokenValidator {
    function check(
        address _token,
        address _subject
    ) public returns(byte statusCode)

    function check(
        address _token,
        address _from,
        address _to,
        uint256 _amount
    ) public returns (byte statusCode)
}
```

# Architecture

## Isolated

```auto
        +--------+
        │ Caller |
        +--------+
           │  ↑
check(...) │  │ statusCode
           ↓  │
      +-----------+
      | Validator |
      +-----------+
```

Here `Caller` may be a token, another `Validator`, an exchange (directly checking), or a user verifying that they will be authorized to perform some action.

## Stacked

(With example ERC1066 status codes for flavour)

```auto
        +-------+
        │ Token |
        +-------+
           │  ↑
check(...) │  │ 0x11
           ↓  │          check(...)
      +------------+   ------------->   +------------+
      | ValidatorA |                    | ValidatorC |
      +------------+   <-------------   +------------+
           │  ↑             0x21             │  ↑
check(...) │  │ 0x11              check(...) │  │ 0x31
           ↓  │                              ↓  │
      +------------+                    +------------+
      | ValidatorB |                    | ValidatorD |
      +------------+                    +------------+
```

# Example Diagram

[![](https://ethereum-magicians.org/uploads/default/optimized/1X/69a3613bdcd9dac53e46428e1ba276a7fa78e7df_2_690x422.jpeg)1562×956 139 KB](https://ethereum-magicians.org/uploads/default/69a3613bdcd9dac53e46428e1ba276a7fa78e7df)

## Replies

**fulldecent** (2019-09-05):

This includes a dependency on status codes. Please list that as a dependency.

