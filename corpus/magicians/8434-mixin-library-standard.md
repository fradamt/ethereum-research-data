---
source: magicians
topic_id: 8434
title: Mixin Library Standard
author: vigilance
date: "2022-02-26"
category: Magicians > Tooling
tags: []
url: https://ethereum-magicians.org/t/mixin-library-standard/8434
views: 2049
likes: 0
posts_count: 1
---

# Mixin Library Standard

---

|  |  |
| --- | --- |
| eip |  |
| title | Mixin Library Standard |
| author | Tyler R. Drury vigilstudios.td@gmail.com (www.twitter.com/StudiosVigil) |
| discussions-to |  |
| status | Idea |
| type | Standards Track |
| category | ERC |
| created | 2022-02-26 |
| requires (*optional) | EIP-165 |

---

# Table of Contents

- Summary
- Motivation
- Terms
- Specification
- Benefits
- Implementation
- Rationale
- Security Considerations
- References
- Copyright

- Citation

---

## Summary

This proposal allows for a standardized approach when implementing the common eternal/external storage slot pattern in libraries and contracts.

**Mixins** are libraries that are atomic units which are composable with other **mixins** and encapsulate the internal state

variables and associated logic of a single, concrete, concept,

providing internal constants and internal or private functions,

which may be (typically) be associated with some structured data storage.

**Mixin** libraries support **internal** functions to be called by an implementing contract and **private** constants, functions or modifiers for internal use.

**Mixins** result in a library’s bytecode being inlined to all call sites within the callin Context contract which,

by the transitive property of inheriting the inlined byte-code, effectively makes the Context ‘inherit’ the internal data structure and logic provided by the **mixin**,

without the additional overhead associated with external library calls.

It is convenient to reuse and compose various **mixins**, since they load unique storage slots specific within the Context of an individual implementing contract,

and since they are atomic structures with all necessary operations provided for that data type,

functionality of contracts can not only be simplified by breaking them down into atomic components,

but also allows for greater flexibility and reusibity, since multiple differing contracts can implement the same **Mixin**,

or a single contract can utilize any number of additional storage slots while reusing the same library code.

For example, the ERC-20 token and EIP-1753 License standard both implement a name function which returns a string,

a single **Mixin** can be declared which loads a contract’s storage slot with the desired structure and provides

the appropriate getters and setters for the data as necessary.

This technique allows both ERC-20 and EIP-1753 implementations to utilize the exact same code in both contracts,

without the unnecessary duplication of code by developers (although during compilation, the inlined internal functions will be injected into the contract directly at all call sites),

while each individual contract manages its own unique storage slot.

Another example would be the ERC-721 and ERC-1155 metadata uri functions.

Both contracts could easily adopt the same **Mixin** providing functionality,

while also expanding on that functionality as required by each unique contract,

usually by implementing multiple other related Mixins as desired.

This technique also provides the distinct advantage that the **Mixin**’s storage utilized by the implementing Context contract is not contained within

the contract itself (but rather is stored in an external, constant storage slot location, for each unique contract),

thus dramatically reducing contract code size to be effectively only that of the compiled contract’s functions,

by eliminating local internal contract storage within a contract.

This approach effectively allows an unlimited amount of data storage within a single contract,

irrespective of contract bytecode size limit imposed by the Spurious Dragon hard fork, without actually violating it,

since none of the storage space is contained within the contract, none of the data contributes to the implementing contract’s bytecode size,

similar to how public libraries reduce code size by internally delegating calls to a separately deployed, public library.

This effectively reduces all contracts to only the size of their function’s bytecode,

allowing for larger, more robust contracts, while also being incredibly small and gas efficient,

with minimal overhead, while also making the implementing contracts much more easy to read and manage.

---

## Motivation

Currently, the Spurious Dragon hard fork enforces a maximum contract bytecode size of ~24kb.

This limit effectively means that contracts significantly larger or more complex than a standard ERC-20 token

hit this limit quickly during development.

This has lead to several interesting approaches to address the size limit, such as **Proxies** and **Diamonds**.

This proposal is based on EIP-2535 standard, providing a much more detailed standard for `diamond storage` specifically,

for implementations of such a storage technique for general purpose use, beyond just **Diamonds** or **Proxies**.

When it comes to the need to reuse contract code and data contracts often inherit from other contracts, however,

this technique causes the inherited code to be directly injected into the derived contract,

meaning the larger a contract is, the larger its children’s bytecode will also be also.

**Mixins** are libraries and thus, can not be instanstiated/deployed or inherited from, instead they define atomic operations on specific data structures,

which can be called by an implementing contract context.

These structures and their functions can then be used in a contract (being inlined directly in the contracts),

providing the data and functionality to the implementing contract as if it directly contained the data and functions,

while minimally affecting overall bytecode size, providing the same functionality as inheritance but,

with far higher benefits of both more complex and more efficient contracts,

due to the reduced bytecode size since no data and minimal code exists within the deployed smart contract itself.

---

## Specification

Since a **Mixin** is an **internal** library which operates on its own storage slot(s) by default,

often **Mixins** don’t require a `using ... for bytes32;` statement in their implementing contracts,

since all operations are executed directly through the **Mixin**, implementing contracts access functions through the **Mixin** directly as defined by the library.

Alternatively, if a **Mixin** supports using non-default storage slots,

due to the nature of libraries the libraries functionality can be attached to a storage slot with a `using ... for bytes32;` statement is the implementing contract.

An arbitrary number of **Mixins** may be implemented by any contract through its library functions,

so care must be taken to avoid clashing of function selectors.

Conversely a single contract may only implement a single version of any one **Mixin** for a specific storage slot,

since multiple calls to the same **Mixin**’s storage slot from within the same contract map to the same place in storage.

---

## Terms

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

|  |  |
| --- | --- |
| bytecode | The compiled EVM compatible binary representing a smart contract’s executable code to deployed on the blockchain at the contract’s address. |
| struct | A single data type representing a collection of other related data types. |
| library | Similar to Contracts but generally contains functions which other contracts utilize, intended for reusability. Unlike Contracts, Libraries do not have their own storage and thus cannot have state variables, nor can they inherit nor be inherited from. |
| mixin | A Library which generally accepts a storage slot as the first argument, which provides functionality for accessing and manipulating a structured data at a storage slot location. |
| storage slot | A unique bytes32 identifier for a storage location within a contract |

---

## Benefits

By leveraging the `using ... for bytes32` statement, a **mixin**’s implementation can be attached to an arbitrary storage slot,

allowing for great reuse and flexibility.

By moving variable storage out of the contract and into external storage slots,

this technique provides the benefit of reducing the executing contract’s bytecode,

leading to vast gains in terms of allowable contract functionality, as enforced in the Spurious Dragon hard fork.

This technique also allows for much more simple and straightforward contract code which is highly versatile.

---

## Implementation

**Mixins** **must** be libraries which adhere to the following axioms:

- All constants must either be private or internal
- All functions must either be declared as either internal or private
- Must declare or operate on at least one unique storage slot identifier, represented as a bytes32 hash
- At least one pure function (either private or internal) which loads a data structure from the location of a unique storage slot,
to be accessed or manipulated as defined by its interface by an implementing contract.
- May declare one or more data structures and associated operations for accessing or mutating that structured data
- May declare modifiers for use with its other functions

A trivial example **Mixin** implementation for the ERC-173 Contract Ownership Standard:

```auto
// SPDX-License-Identifier: Apache-2.0

pragma solidity >=0.6.4  (www.twitter.com/StudiosVigil) - copyright 2/4/2021, All Rights Reserved
///
library mixinERC173
{
    using addressConstraints for address;
    using eventsERC173 for address;

    struct ERC173Storage {
        address owner;
    }

    bytes32 internal constant STORAGE_SLOT = keccak256("ERC-173.mixin.storage");

    function storageERC173(
        bytes32 slot
    )internal pure returns(
        ERC173Storage storage ret
    ){
        bytes32 position = slot;

        assembly {
            ret_slot := position
        }
    }
    ///
    ///read-only interface
    ///
    function owner(
        bytes32 slot
    )internal view returns(
        address
    ){
        return storageERC173(slot).owner;
    }

    function requireOwner(
        bytes32 slot,
        address sender
    )internal view
    {
        address O = owner(slot);

        O.requireNotNull(
            "owner can not be NULL"
        );
        O.requireEqual(
            sender
            "caller not owner"
        );
    }
    ///
    ///mutable interface
    ///
    function transferOwnership(
        bytes32 slot,
        address newOwner
    )internal
    {
        addres owner O = owner(slot);

        O.requireNotEqual(newOwner);
        O.emitTransferOwnership(newOwner);

        storageERC173(slot).owner = newOwner;
    }
    function renounceOwnership(
        bytes32 slot
    )internal
    {
        transferOwnership(
            slot,
            addressLogic.NULL
        );
    }
}
```

Additionally, it may be convenient in future EIPs, should this technique show large adoption,

to include a `mixin` keyword in future compiler versions,

to abstract these axioms into compiler-defined and enforced behavior, in order to eliminate human error and

so as to differentiate between the use and purpose of traditional libraries in contrast to external storage **Mixins**, such that:

- Constants should only be private or internal, to prevent deploying a public library.
- Functions should only be private or internal,
so as to allow for the inlining of the internal code for loading the storage structure from the specific storage slot,
within the context of the implementing contract (this technique does not work properly with public library functions).
- At least one data structure may be defined along with an associated, default storage slot,
which the compiler could generate in future versions by default based on the name of the Mixin library which could be accessible using standard EVM type() introspection.
- Code for loading a data structure from a storage slot (which is trivial assembly similar to a compiler generated default constructor)
could easily be automatically generated by the complier in future version,
along with the corresponding automatically generated storage slot identifier,
similar to how contracts may have auto-generated default constructors, if one is not explicitly declared.

---

## Rationale

With the byte-code limit for the Spurious Dragon hard-fork of 24Kb is incredibly limiting,

utilizing external storage slots in a standardized manner via **mixins** is not only convenient but incredibly powerful and flexible,

allowing for more complex contracts without imposing massive restrictions on contract size.

This proposal also allows for the distinction between internal library code which defines the **mixin**’s functionality on a specific type or storage slot

and the implementing contract which should utilize the **mixin**’s functionality while also being

responsible for managing state logic associated with external callers of a public interface,

providing a clean distinction between these two approaches and what constructs have responsibility for what functionality.

Additionally having a single, reusable **Mixin** library allows for greater flexibility as a developer by easily allowing code reuse

in multiple contracts which implement the same structures or logic without having to duplicate code or the associated bytecode bloat of declaring contract variables.

---

## Security Considerations

There are no immediate security concerns regarding **Mixins** (since they are abstractions for atomic data structures)

beyond any concerns specific to a particular standard implementation however,

as this technique further develops there is a possibility this proposal may have unforeseen security issues.

Since each individual **Mixin** (with a unique storage slot) loads its data structure within the Context of an implementing contract,

multiple contracts which implement the same **Mixin** do not conflict, conversely,

accessing the same **Mixin** internally from a derived Context contract will load the same storage as if called from the base contract.

Similar to the Black Diamond pattern in languages which support multiple inheritance,

if a single contract that inherits from multiple various base contracts but which also happen to implement the same **Mixin** utilizing the same storage slot

the potential exists for conflict and unintentionally overwrite storage intended for use by the other **Mixin**.

Since the contracts don’t have the variables declared locally, the compiler will most likely not generate any warning that multiple contracts

are modifying the same storage location.

The simple solution to this concern is to just use a unique storage slot for each derived implementation when it is unavoidable

to have a contract inherit from two or more contracts which implement the same **Mixin**.

Another concern is that there may be storage conflicts between Proxies and their implementations if the layout of a storage slot is updated or slot locations between the two differ.

There are currently no other major issues regarding the use of **Mixins**.

---

## References

- ERC-165: Interface Support
- EIP-897 Delegate Proxy
- EIP-2470: Singleton Factory
- EIP-2535: Diamonds
- EIP-1613: Gas Station Network

---

## Copyright

Copyright and related rights waived via CC0.

---

## Citation

Tyler R. Drury, “EIP-XXX: **Mixin Library Standard** [DRAFT]”,

Ethereum Improvement Proposals, no XXX, February 2022. [Online serial].
