---
source: magicians
topic_id: 16152
title: "EIP-7539: ERC Extensions"
author: joeysantoro
date: "2023-10-18"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-7539-erc-extensions/16152
views: 821
likes: 1
posts_count: 8
---

# EIP-7539: ERC Extensions

---

## eip: 7539
title: ERC Extensions
description: Establishes Naming Conventions, Metadata, and Procedures for ERC Extensions
author: Joey Santoro ()
discussions-to:
status: Draft
type: Standards Track
category: Meta
created: 2023-10-18
requires: 1

## Abstract

This EIP Establishes a framework for ERC Extensions, or ERCs which directly extend or override the functionality of a prior ERC.

This standard includes a standardized definition for an ERC Extension. It includes a naming convention for the Title EIP header field, adds an optional `extensions` EIP header field for referencing downstream ERC extensions, and extablishes procedures for specifying overridden functionality.

## Motivation

Ethereum application development uses a contract oriented programming paradigm which is similar to Object Oriented Programming (OOP). Because of this, many smart contract systems and high level languages have object like behavior with the possibility for overriden functionality.

ERC Standards also behave in a similar way, with logical extensions flowing from the necessity to standardize specific use cases on top of higher level standards. (e.g. ERC-2612 extends ERC712) and ERC-4626 extending ERC-20).

There should be a framework for handling these extension cases both retroactively and in the future to improve ERC accessibility.

## Specification

### Definitions

Usage of the term Extension below is shorthand for an ERC Extension.

An Extension is any ERC which has all of the following properties:

- inheritance
- interface compatibility
- logically consistent

#### Inheritance

An Extension MUST require the implementation of at least one existing ERC.

It MUST add additional functionality or specificity.

An Extension MAY NOT define new functions or add functions to the extended interface. If an Extension does not define any new functions, it MUST specify  functionality for a limited use case of the extended ERC.

#### Interface Compatibility

An Extension MUST be fully compatible at the function interface level. I.e. all functions in the extended interface MUST implement the exact same function signature and selector.

An Extension MAY NOT have the same parameter names or state mutability.

#### Logically Consistent

An Extension MUST maintain the core logical functionality of the extended ERC. This MAY include some non-compliance at the implementation level specification, as long as the overriden behavior is fully specified.

Specifically, mutable functions MUST remain mutable and immutable functions MUST remain immutable. I.e. the state mutability between `payable` and `non-payable` MAY interchange and the state mutablity between `view` and `pure` MAY interchange.

### Extension Naming

An Extension SHOULD include the ERC number of the extended ERC in the title (e.g. Non-transferrable ERC-721). If not in the title, the description MUST include the ERC number of the extended ERC.

### Extensions EIP Header

Once an Extension becomes Final, the extended ERC MUST be edited to include the extension in a new header field called `extensions`.

E.g. ERC-4626 extends ERC-20, therefore ERC-20 must be edited to add: `extensions: 4626`

### Extension Specification

Any breaking changes or non-compliance at the implementation level MUST be fully specified and justified in the `Rationale`. An explicit `ERC-XXX Breaking Changes` sub-heading must be included in the `Specification` section for every extended ERC which has breaking changes. Omission of the Breaking Changes subheading MUST mean there are no breaking changes at the implementation specification level.

All breaking changes MUST be compliant with the properties of an Extension.

EIPs published before EIP-7539 MAY be edited to comply with some or all of EIP-7539.

## Rationale

This EIP was designed to provide a minimal framework for future Extensions without adding too much boilerplate. All features are designed to improve the utility and accessibility of Extensions and the ERCs they extend.

### Extensions Header

The header allows historical ERCs to reference future extensions cleanly. The `extensions` header allows for forward navigation and the existing `requires` header allows for backward navigation of ERC heirarchies.

### Breaking Changes

Extensions may require certain breaking changes at the implementation, however those should be constrained to a well defined set of possible changes. Functions changing their mutability should not happen, and interfaces should remain fully compatible.

All breaking changes should be clearly specified in their own section with respect to each extended ERC for maximum legibility.

### Derivative EIP numbers

Each EIP should still have a canonical number following the EIP process. If instead derivative naming such as ERC-20b was used, EIPs become harder to place in a chronological context, Extensions which extend multiple ERCs become difficult to name, and many parts of the existing EIP process become unweildy or change significantly.

Instead, requiring the extended ERC to be named in the title or description allows for sufficient colloquial discussions to tie the Extension to the extended ERC.

## Backwards Compatibility

This EIP is fully backward compatible with all EIPs.

It does not require editing historical ERCs, but does open the possibility of doing so in part or full.

## Security Considerations

N/A

## Copyright

Copyright and related rights waived via CC0.

## Replies

**SamWilsn** (2023-10-27):

I don’t think we can do the `extensions: XXXX` header. That would require modifying already finalized EIPs. We *could* do an `extends: 20` header, but that’s basically a more specific version of the `requires` header.

---

**SamWilsn** (2023-10-27):

I am concerned about how much technical knowledge would be required of Editors to correctly judge the requirements in your proposal. We don’t want to place too much of a burden on Editors who might not be intimately familiar with Solidity and its nuances (like yours truly!)

For example:

> An Extension MUST be fully compatible at the function interface level.

Is this something that can be enforced with a tool when pull requesting into the repository? If not, I don’t think we can expect Editors to reliably judge this.

> Any breaking changes or non-compliance at the implementation level MUST be fully specified and justified in the Rationale.

This is probably fine, as long as doable solely by reading the base and the extension EIPs.

---

**joeysantoro** (2023-10-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I don’t think we can do the extensions: XXXX header. That would require modifying already finalized EIPs. We could do an extends: 20 header, but that’s basically a more specific version of the requires header.

the `extensions:` header is the main reason to do this EIP as it allows forward and backward traversal of EIP hierarchies. In my opinion this is a strong candidate for a rule-based edit of final EIPs as it does not impact the content of the EIP at all and can even be done automatically with the right tooling.

I still think the EIP is useful without `extensions:` but not nearly as useful.

`extends` doesn’t really add anything as you point out.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I am concerned about how much technical knowledge would be required of Editors to correctly judge the requirements in your proposal. We don’t want to place too much of a burden on Editors who might not be intimately familiar with Solidity and its nuances (like yours truly!)

The amount of technical knowledge is limited exclusively to the understanding of how the abi is encoded into  function signature and selector. It isn’t a specific issue to Solidity but rather the abi encoding at the evm level. I just happen to write Solidity as my preferred high level language.

Point taken that editors shouldn’t necessarily be required to know this.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Is this something that can be enforced with a tool when pull requesting into the repository? If not, I don’t think we can expect Editors to reliably judge this.

If we came up with an interface specification that we also enforced for ERCs this could be easily done automatically with the right tooling development. I can potentially PoC a tool if this is a deal-breaker for this EIP. There were some cool ideas around specifying ERC interfaces in a language-agnostic yaml format which could be worth revisiting.

---

**frangio** (2023-10-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joeysantoro/48/5147_2.png) joeysantoro:

> the extensions: header is the main reason to do this EIP as it allows forward and backward traversal of EIP hierarchies.

This seems like a UI/UX consideration that doesn’t need to be reflected in the data model. An `extends` field could also be used to implement navigation both ways.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joeysantoro/48/5147_2.png) joeysantoro:

> extends doesn’t really add anything as you point out.

Any EIP that is simply mentioned in the text has to be added in `requires`, so that field does not represent extended EIPs, and an `extends` field would have that specific meaning so it does add something IMO.

---

**SamWilsn** (2023-10-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joeysantoro/48/5147_2.png) joeysantoro:

> the extensions: header is the main reason to do this EIP as it allows forward and backward traversal of EIP hierarchies.

We can (probably) set up our site builder to enable forward and backward traversal regardless of where the header lives. The same information is encoded either way, but the `extends` header doesn’t require modifying a final EIP.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joeysantoro/48/5147_2.png) joeysantoro:

> extends doesn’t really add anything as you point out.

Like I said, it’s the same information in `extensions` or `extends`. The only difference for between those two and `requires` is that an “extension” is a more strict subset of `requires` (every extension requires its parent, but not every `requires` is an extension.)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joeysantoro/48/5147_2.png) joeysantoro:

> If we came up with an interface specification that we also enforced for ERCs this could be easily done automatically with the right tooling development.

If it can be automated, I’m much less opposed to this idea. Could be something like a NatSpec comment of the form `@custom:erc-extends proposal identifier`, like:

```solidity
/// @custom:erc-extends ERC-4400 IEIP721Consumable
interface Foo {
}
```

[eipw](https://github.com/ethereum/eipw) already has a whole JSON Schema validator in it, so why not add the entire solidity compiler and friends ![:rofl:](https://ethereum-magicians.org/images/emoji/twitter/rofl.png?v=12)

---

**SamWilsn** (2023-10-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joeysantoro/48/5147_2.png) joeysantoro:

> yaml

No‍‍‍‍‍‍‍‍‍‍‍‍.

---

**joeysantoro** (2023-10-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> We can (probably) set up our site builder to enable forward and backward traversal regardless of where the header lives. The same information is encoded either way, but the extends header doesn’t require modifying a final EIP.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> This seems like a UI/UX consideration that doesn’t need to be reflected in the data model. An extends field could also be used to implement navigation both ways.

If this is the case then `extends:` works and is fine with me, the important part is the site linking not the actual EIP

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> eipw already has a whole JSON Schema validator in it, so why not add the entire solidity compiler and friends

Will take a look and see if there is a straightforward way to do it

