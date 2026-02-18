---
source: magicians
topic_id: 14692
title: "EIP-7182: Interface Naming Conventions"
author: pcaversaccio
date: "2023-06-15"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/eip-7182-interface-naming-conventions/14692
views: 595
likes: 1
posts_count: 5
---

# EIP-7182: Interface Naming Conventions

Discussion thread for my EIP-7182 proposal [here](https://github.com/ethereum/EIPs/pull/7182).

## Motivation

The vast majority of interface definitions today are based on Solidity-based naming conventions such as `camelCase` for function names or `PascalCase` for events and custom errors. This has been an opinionated decision that is not compatible with other languages such as Vyper or Cairo that use a `snek_case` convention. Unfortunately, this approach leads to inconsistent naming within such codebases, where functions, events, or custom errors that must adhere to interface definitions are written in `camelCase`, while all other functions, events, or custom errors use a `snek_case` approach. This EIP attempts to standardise the naming convention on which the `keccak256`-based signatures of functions, events, custom errors, and other identifiers are calculated. The implementation of the naming convention can be implemented directly by the compilers, allowing each language to maintain its naming convention scheme generically.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

1. Every single word of an interface function, event or custom error definition, or anything else contained in an interface definition and used as an identifier, MUST be capitalised and concatenated with an underscore _ before conversion. Examples:

- transferFrom → TRANSFER_FROM
- balanceOf → BALANCE_OF
- safeBatchTransferFrom → SAFE_BATCH_TRANSFER_FROM

1. Using the standardised name, all non-alphanumeric characters excluding the underscore _ MUST be removed from the name. Examples:

- $TRANSFER_FROM → TRANSFER_FROM
- BA{L}ANCE_OF → BALANCE_OF
- SAFE_BA\TCH_TRAN!SFER_FROM → SAFE_BATCH_TRANSFER_FROM

1. The alphanumeric name string is keccak256 hashed and converted to an integer type accordingly. Examples:

- TRANSFER_FROM → int(keccak(text="TRANSFER_FROM").hex(), 16) = 94395173975023775779662060048629656272561824698643396274474837925292473410016
- BALANCE_OF → int(keccak(text="BALANCE_OF").hex(), 16) = 80708256028020625538388752345478945032378179923394270514785770355663480356011
- SAFE_BATCH_TRANSFER_FROM → int(keccak(text="SAFE_BATCH_TRANSFER_FROM").hex(), 16) = 255983261274881569444563352188479556572877507257597428201081558335645686969

1. The following naming conventions MUST be supported:

- camelCase
- flatcase
- MACRO_CASE
- PascalCase
- snake_case

> kebab-case and COBOL-CASE are not supported due to general language compatibility reasons.

1. Eventually, the naming convention is selected based on the following algorithm, where hashed MUST be the result of step 3 and non_alphanumeric_name MUST be the result of step 2:

```python
MAX_UINT256 = 2**256 - 1  # Maximum value that a `keccak256` hash can reach.
INTERVAL = MAX_UINT256 / 5  # We support 5 different naming conventions.

if hashed > (MAX_UINT256 - INTERVAL):
    return camelcase(non_alphanumeric_name)
elif hashed > (MAX_UINT256 - 2 * INTERVAL):
    return flatcase(non_alphanumeric_name)
elif hashed > (MAX_UINT256 - 3 * INTERVAL):
    return macrocase(non_alphanumeric_name)
elif hashed > (MAX_UINT256 - 4 * INTERVAL):
    return pascalcase(non_alphanumeric_name)
else:
    return snakecase(non_alphanumeric_name)
```

Theoretically, it is possible that ERCs are proposed that are optimised for a particular naming convention based on this approach with forged names. The EIP editors MUST ensure that the names are reasonable enough to justify such reverse engineering of the implied naming convention.

## Rationale

Based on the above specification, we can achieve two goals:

- Each language can continue to use its naming convention consistently, while compilers can implement the conversion beneath the surface.
- The most common naming conventions are supported, covering Solidity, Vyper, Huff, Fe, or Cairo, making it future-proof.

## Replies

**radek** (2023-06-19):

Can you elaborate impact on Solidity’s 4 bytes selectors? There is already an ecosystem surrounding those - bytes4 DBs, HW wallets supports, …

---

**pcaversaccio** (2023-06-19):

They are not impacted at all to the extent that all the function signatures up until the day this EIP is final are calculated based on the *old* method. This EIP “just” standardises on *what input* the selectors are calculated. So let me make an example. Let’s assume someone makes a new ERC with a function called `safeBatchTransferFrom`. What Solidity would need to do is first calculate the canonical name (based on my EIP) which would be `safe_batch_transfer_from`. Thereafter, Solidity would calculate the function selector as usual, e.g. `bytes4(keccak256(bytes("safe_batch_transfer_from"))) = 0xab556ee4`.

---

**radek** (2023-06-29):

Thx for the example. Seams clear in this straight one. How would that be after the EIP final’s date when having multiple inheritance with one Base class from before this EIP and other Base class from after this EIP?

---

**pcaversaccio** (2023-06-29):

Good question but this is, IMO, an implementation question to be solved on the compiler side and not part of the ERC definition as other languages don’t allow for instance for inheritance (see e.g. Vyper). Generally speaking, for instance, in Vyper you could add an additional `kwarg` `is_eip7182` to the function or event for differentiation. In Solidity, we could maybe annotate the behaviour for functions using NatSpec or add an additional contract/function member via `{}`, e.g. `C{isEIP7182: true}.fn(...)` or `fn{isEIP7182: true}(...)`.

