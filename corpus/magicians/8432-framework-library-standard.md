---
source: magicians
topic_id: 8432
title: Framework Library Standard
author: vigilance
date: "2022-02-26"
category: Magicians > Tooling
tags: []
url: https://ethereum-magicians.org/t/framework-library-standard/8432
views: 1484
likes: 0
posts_count: 1
---

# Framework Library Standard

---

|  |  |
| --- | --- |
| eip |  |
| title | Framework Library Standard |
| author | Tyler R. Drury vigilstudios.td@gmail.com (www.twitter.com/StudiosVigil) |
| discussions-to |  |
| status | Idea |
| type | Standards Track |
| category | ERC |
| created | 2022-02-26 |
| requires (*optional) | EIP-165 |

---

## Table of Contents

- Abstract
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

## Abstract

**Frameworks** are libraries which only encapsulate the **internal** or **private** constants of the **framework** and the functions associated

with some standard interface implementation, to be executed on an arbitrary address which **may** provide support for standard run-time interface detection.

**Framework** functions **must** either accept an address as their first argument or otherwise implicitly operates on the calling contract context or both,

then executes transactions on the external contract’s address as defined by a some standard interface.

All ERC standard interfaces could natively support an accompanying **framework**

in order to allow for the implementation of a standardized approach to external contract calls.

Additionally, such a fundamental abstraction, if proven useful, could have a convenient, native keyword (like library, interface or contract) added to future compiler versions,

so as to make the process of declaring, writing or using **frameworks** more convenient, intuitive and explicit,

along with providing compiler enforced behavior on **frameworks** as specified by this proposal.

---

## Motivation

Currently, there are two primary methods for executing external calls on contracts.

The **first** approach:

Use low level operations to execute functions on the contract address,

such as **.call**, **.staticall** and **.delegatecall**.

While this approach grants immense flexability, there is usually a high barrier of entry to new developers unfamiliar with such operations

since it also requires repeated calls to low level functions such as to **abi.encode** or **abi.encodeWithSignature**,

often preceeded by executing some introspection function to ensure the contract supports the desired function.

As with all low level coding, this ultimately becomes cumbersome quickly and leads to unnecessary code bloat and code repetition, especially in circumstances where

functions which do not accept arguments (such as getter/read-only functions) can precompute their encoded function signature and cached after calling **abi.encodeWithSignature**,

since they accept no arguments, the encoded function signature is guaranteed to remain the same indefinitely,

thus making repeated calls to the same function needlessly call **abi.encodeWithSignature** each time the function is executed,

causing unnecessary gas consumption on repeated calls.

The **second** approach:

Declare a contract or interface, then cast the target external contract address to the appropriate type.

This instance can then execute the functions of that interface or contract, however there is no guarentee the casted address

is in fact a contract of the desired type or supports the intended functions.

This can lead to issues, such as attempting to execute code on a wallet address, instead of a contract address.

Additionally, the concept of instantiating an Interface (while currently supported by the EVM), is not intuitive from the perspective of those with back ground in similar languages.

Interfaces should only declare the external ABI of a contract, to be explicitly overridden in derived contracts and should not be instansiatable,

as is commonplace with almost all other languages which implement such an abstraction and is ubiquitous with how the concept of interfaces are generally perceived

as being a means to declare a related set of functions to be overridden by the implementer of an interface.

This interpretation is further supported by a related construct to interfaces, the Abstract Base Contract (or **ABC**).

In Soliditiy, while **ABC**s can **not** be instansiated/deployed, interfaces can, contrary to standard coding practices in other languages.

As such **frameworks** are a convenient abstraction which unifies both approaches,

while also adding flexibility, reusability and composibility while also reducing complexity

by providing a standardized approach where the end-user is not concerned about the underlying low-level implementation,

since **frameworks** facilitate the exact same calls to an external contract as if it were a fully realized instance of an interface.

---

## Terms

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

|  |  |
| --- | --- |
| function | A named collection of opcodes which can be executed by a smart contract which may accept a list of arguments. |
| interface | defines a collection of related external functions a smart contract supports. |
| library | Similar to Contracts but generally contains functions which other contracts utilize, intended for reusability. Unlike Contracts, Libraries do not have their own storage and thus cannot have state variables, nor can they inherit nor be inherited from. |
| framework | library with functions which either exclusively accept an address as its first argument or implicitly operate on the calling contract context or both then executes functions on the external contract’s address which may support a standard interface |

---

## Specification

Leveraging the native language level mechanics of libraries, **frameworks** allow adding utility for various interfaces natively to generic addresses,

allowing convenient access to interface functions as if a raw address were an instance of the interface without casting it to an instance of that interface,

while offering the potential for built-in support for run-time interface introspection as well.

Since a **framework** is merely a library which accepts as its first argument a contract’s address,

An arbitrary number of **frameworks** **may** be attached to the native address type with the `using framework... for address;` statement within an implementing contract.

If a **framework** function instead does not accept an address as its first argument,

it **must** implicitly operate on the calling contract context,

which the associated function **should** be accessed via dot (.) notation through the **framework** name

without relying on a **using** statement.

```auto
contract ERC20Token is iERC20
{
    using frameworkERC173 for address;
    using frameworkERC20 for address;

    address _target;

    constructor(address target){
        _target = target;
    }
    function example()external
    {
        //call to .owner() automatically performs ERC-165's `supportsInterface` check for ERC-173 on target before attempting execution
        //reverting state if the address is either target is not a contract or does not support the desired interface
        require(address(this) == _target.owner(), "this contract does not own target contract");
        //
        _target.renounceOwnership();
        _target = address(0);
    }
    ///caller approves this contract to transfer `swappedTokenAmount`
    function targetTokenApprove(
        uint256 swappedTokenAmount
    )external
    {
        approve(msg.sender, swapTokenAmount);
    }
    /// @dev swap this ERC20 token for target's ERC20 token
    function swap(
        uint256 thisTokenAmount
    )external
    {
        require(_target.owner() != address(0), "Target contract is null");
        require(_target.owner() == address(this), "This contract does not own target");
        //
        // todo: get price feed for token pair from oracle to verify price of exchange is at fair market value
        uint256 swapTokenAmount = poolPriceRouter.getConversionrate(symbol(), _target.symbol(), thisTokenAmount);
        //
        require(_target.balanceOf(address(this) >= swapTokenAmount);
        require(allowance(msg.sender, address(this)) >= thisTokenAmount);
        //this contract transfers `thisTokenAmount` from this contract to caller performing the swap
        transferFrom(msg.sender, address(this), thisTokenAmount);
        //if approved, this contract transfers `swapTokenAmount` from msg.sender to this contract
        //reverts if address is not a contract or does not support ERC-20
        _target.transfer(msg.sender, swapTokenAmount);
    }
}
```

---

## Benefits

By leveraging the using statement (where *…* could be any EIP standard as necessary):

```auto
using framework... for address;`
```

a **framework**’s implementation can be attached to an arbitrary address

while the nature of libraries preserving the calling context of the executing contract and is guaranteed to perform

all appropriate introspection to ensure the address supports such execution, otherwise state is reverted and the transaction fails with no side-effects.

Additionally, this technique provides the benefit of reducing the executing contract’s bytecode,

leading to vast gains in terms of allowable contract functionality,

as enforced by the bytecode size of 24kb in the Spurious Dragon hard fork.

This approach also reduces or eliminates the need (and associated gas fees) of both:

- casting and instansiating an address as an interface/contract instance
- having to call abi.encodeWithSignature repeatedly when executing multiple low-level calls to interface functions which do not accept any arguments

since the **framework**’s implementation would be attached to the address data type at compile time.

This technique also allows for significantly less complex and straightforward contract code,

since the framework allows an arbitrary external address to be used within another contract as if the **framework**’s target address were a fully instansiated contract.

With the above example, the `swap` function only occupies 4 lines of code, is simple to read, understand or modify.

Explicitly casting the address to a contract or interface type, not only requires extra operations but is made unnecessary

with the more convenient syntax of the using statement:

```auto
using framework... for address;
```

approach of **frameworks** in this proposal and is much more concise.

Where as, if the approach of explicitly using low-level **.call** methods were used, the `swap` function would be almost twice as bloated,

thus consume more gas while also requiring additional calls to check if the address is a contract, multiple calls to abi.encodeWithSignature and explicit calls to ERC-165 before

other type checking operations occur for the desired interface.

Not only is the framework approach much more versatile and succinct than either of these alternative approaches,

this techniques also leaves an almost negligible byte-code foot print for each call.

---

## Implementation

Currently **frameworks** **must** be implemented as libraries,

with internal or private function which **should** accept a contract address as their first argument or implicitly operate on the calling contract context or both.

An example **framework** for ERC-165 might look similar this example:

```auto
// SPDX-License-Identifier: Apache-2.0

pragma solidity >=0.6.4  (www.twitter.com/StudiosVigil) - copyright 5/4/2021, All Rights Reserved
///
library frameworkERC165
{
    using logicConstraints for bool;
    using addressConstraints for address;
    using Address for address;

    bytes4 internal constant _INTERFACE_ID = type(iERC165).interfaceId;
    string internal constant SUPPORTS_INTERFACE_STUB = 'supportsInterface(bytes4)';
    ///
    ///read-only interface
    ///
    ///does target support ERC-165
    function supportsInterface(
        address target
    )internal view returns(
        bool ret
    ){
        target.requireNotNull();
        target.isContract().requireTrue(
            "ERC-165: target is not contract"
        );
        // ERC-165 requires supportInterface calls to consume no more than 60,000 gas
        (bool result, bytes memory data) = target.staticcall{gas: 60000}(
            abi.encodeWithSignature(
                SUPPORTS_INTERFACE_STUB,
                _INTERFACE_ID
            )
        );
        result.requireTrue('call failed');

        (ret) = abi.decode(data, (bool));
    }
    ///does target support ERC-165 AND the interface specified by interfaceId
    function supportsInterface(
        address target,
        bytes4 interfaceId
    )internal view returns(
        bool ret
    ){
        supportsInterface(target).requireTrue(
            "ERC-165: not supported"
        );

        (bool result, bytes memory data) = target.staticcall{gas: 60000}(
            abi.encodeWithSignature(
                SUPPORTS_INTERFACE_STUB,
                interfaceId
            )
        );
        result.requireTrue(
            '"ERC-165: external call failed'
        );

        (ret) = abi.decode(data, (bool));
    }
    function requireSupportsInterface(
        address target
    )internal view
    {
        supportsInterface(target).requireTrue(
            "ERC-165: interface not supported"
        );
    }
    function requireSupportsInterface(
        address target,
        bytes4 interfaceId
    )internal view
    {
        supportsInterface(
            target,
            interfaceId
        ).requireTrue(
            "ERC-165: interface not supported"
        );
    }
    function requireNotSupportsInterface(
        address target
    )internal view
    {
        supportsInterface(target).requireFalse(
            "ERC-165: target supports interface"
        );
    }
    function requireNotSupportsInterface(
        address target,
        bytes4 interfaceId
    )internal view
    {
        supportsInterface(
            target,
            interfaceId
        ).requireFalse(
            "target supports interface"
        );
    }
}
```

Additionally, it may be convenient in future EIPs, should this technique show large adoption,

to include a `framework` keyword in future compiler versions,

to abstract much of these idioms into compiler-defined and enforced behavior,

so as to differentiate between the use and purpose of traditional libraries such that **frameworks**:

- Must support only private variables for that specific framework.
- Functions must only be either internal or private.
- Functions must accept an address as its first argument or implicitly operate on the calling contract context or both.

---

## Rationale

Abstracting the concept of executing low-level operations on external contracts into

a single cohesive coding standard (or even built-in primitive type) would greatly enhance not only development of smart contracts but

also easy the barrier of entry to new comers who do not yet fully grasp the more subtle low-level operations of the EVM,

while allowing the the power and flexibility such techniques provide without the need for intimate knowledge of such semantics.

With **frameworks**, new developers only needs to be familiar with how libraries operate in order to take advantage of this powerful proposal.

---

## Security Considerations

The only obvious concerns are those common to executing external functions of contracts which can’t be trusted,

such as the underlying EIP the **framework** is built on or selector clashing concerns, as is the case with any approach to implementing external contract calls.

In this regard, a malicious contract could define a function which matches a specific **framework** selector to an interface function,

providing a malicious implementation which has nothing to do with the intended operation.

These concern can be alleviated by:

- Ensuring the Context contract and the Target contract are never the same address.
- Ensuring view/pure getter framework function calls use .staticcall to ensure state immutability in both Context and Target
do not modify the executing call context.
- Ensuring care is taken that mutable function should only modify the Target contract being called and not the calling Context,
since the intention of framework functions is to operate on the Target contract,
which should never modify the calling Context contract.
- Ensure all modifications to the calling Context state occur entirely with itself and never as the result of a framework call to a target.
- .delegatecall must never be used to implement framework functions since,
any potential malicious code should only affect the executing target contract (not the Context contract),
so long as the Context contract implements a ReentrancyGuard (or a similar technique),
this should prevent any potential of the target contract attempting to call back into the Context contract maliciously.

---

## References

- EIP-165: Standard Interface Detection
- EIP-897: Delegate Proxy
- EIP-1967: Proxy Storage Slots
- EIP-1613: Gas Station Network

---

## Copyright

Copyright and related rights waived via CC0.

---

## Citation

Tyler R. Drury, “EIP-TBD: **Framework Library Standard** [DRAFT]”,

Ethereum Improvement Proposals, no TBD, February 2022. [Online serial].
