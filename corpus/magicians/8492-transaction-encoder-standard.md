---
source: magicians
topic_id: 8492
title: Transaction Encoder Standard
author: vigilance
date: "2022-03-02"
category: EIPs
tags: [smart-contracts]
url: https://ethereum-magicians.org/t/transaction-encoder-standard/8492
views: 1844
likes: 0
posts_count: 1
---

# Transaction Encoder Standard

---

|  |  |
| --- | --- |
| eip |  |
| title | Transaction Encoder Standard |
| author | Tyler R. Drury vigilstudios.td@gmail.com |
| discussions-to |  |
| status | Idea |
| type | Standards Track |
| category | ERC |
| created | 2022-03-02 |
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

This proposal allows for a standardized approach to writing libraries and smart contracts which encode transactions for executing low-level external calls on **EIP** compliant contracts.

**Encoders** **must** be either:

- libraries which encapsulate the internal or private constants for encoding transactions.
- contracts which provide public or external functions for encoding transactions to some associated standard EIP interface implementation.

Libraries and smart contracts compliant with this proposal exclusively support only **pure** functions which return ABI encoded bytes payloads of the arguments passed to them,

which can be used for calls to *contracts*, **proxies**, **diamonds**, **gas station network relay**, **multisig wallets** or other *delegatecall*/proxy based primitives, which do not provide a static ABI.

---

## Motivation

When executing transactions using *.call*, *.staticcall*, or *.delegatecall* on an external address, it is necessary to first *abi.encode*

the function and its arguments into a binary payload, which can then be executed directly on the *contract*, used for forwarding transactions via **EIP-1613: Gas Station Network**,

or used with the built-in *fallback()* of a proxy or diamond, when calling a function not explicitly defined within a *contract* external ABI.

Since gas consumption and byte-code size are two critical factors to consider when developing smart contracts,

it is important to utilize/optimize the contracts being used, not only to reduce associated costs with deploying or executing smart *contract* functions,

but to also allow for greater flexibility when it comes to creating singular contracts with high degrees of functionality/usability/versatility.

Additionally, since there is no high-level, internal mechanism built into the EVM or compiler to provide smart contracts with such functionality (aside from the low-level *abi.encode* functions),

when working with smart contracts in a capacity external to the native blockchain, such as using **web3** or **ether.js** JavaScript libraries in the context of a web browser.

It is incredibly cumbersome and tedious to have to write custom JavaScript code (which is insecure and dynamic by its very nature, the exact opposite of when blockchain developers expect),

just to be able to encode a binary payload using such a JavaScript library to be used for low-level calls to a smart *contract* deployed on the blockchain,

especially in the case of **proxies** or **diamonds**, which do not define any ABI what so ever but can still execute them via the *fallback()* method.

The simple solution to this, as outlined in this proposal, is to have dedicated **encoder** contracts deployed on the blockchain which provide such functionality

in a secure manner.

Developers only need to instantiate the **encoder** *contract* from a blockchain address, which provides its static ABI,

as opposed to writing custom JavaScript code for each occasion ABI encoding functionality is required,

which as stated previously is both insecure and dynamic due to the very nature of the JavaScript virtual machine.

Since calling **pure** and **view** functions on a *contract* externally from the blockchain (such as with a JavaScript API) does not consume gas,

not only does this technique provide a concise manner by which to implement **ABI encoders** but also provides a cheap way to guarantee

the binary payload is correctly encoded for a given external transaction on any ERC/EIP compliant *contract*,

while also providing the smallest gas cost possible (most commonly less than 30,000 gas) when using **ABI Encoder** contracts on-chain.

**Encoder** contracts have specific utility when implemented with Framework Library Standard compliant libraries,

further leading to reduced byte-code size, gas consumption and increased performance,

by avoiding having to make multiple, unnecessary, calls to *abi.encode* functions and/or repeatedly instantiating and deallocating the temporary strings used to represent the function’s stub.

---

## Terms

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

|  |  |
| --- | --- |
| ABI | Application Binary Interface. |
| library | specified with the library keyword, similar to contracts but generally contains functions which other contracts utilize, intended for reusability. Unlike Contracts, Libraries do not have their own storage and thus cannot have state variables, nor can they inherit nor be inherited from. |
| encoded transaction | An EVM compatible binary payload which can be sent to a smart contract address to execute a transaction. |
| encoder | Either a library smart contract which specializes in encoding transactions, returning EVM compatible binary encoded payloads. |

---

## Specification

Any **EIP** standard **could** have an associated **ABI Encoder** with the same function names and argument lists as specified in the source material.

---

**Encoders** **must**:

- declare all constants as internal or private.
- declare all functions with the pure modifier.
- declare all functions with the same name and argument list as the associated transaction being encoded.
- declare all non-constructor functions as returning a single variable of type bytes memory.
- either:

if the transaction to encode accepts arguments, the function make a single call abi.encodeWithSignature, returning the encoded arguments passed to it using a function name which matches the name of the transaction to encode.
- if the transaction to encode is either a getter and other function which does not accept arguments, returns a constant value.

---

**Encoders** **must not**:

- declare or access storage slots.
- declare structs or enums.
- modify storage in any way.
- emit events.
- declare modifiers.

---

**Encoders** **may**:

- support EIP-165 or other runtime interface introspection standard, such as EIP-1820.
- if a contract, inherit from other encoder contracts compliant with this standard.
- make calls to encoder libraries or external contracts which are compliant with this standard.
- be implemented either as:

a library which must have either all internal or all public functions.
- a contract which must have either external or public functions.

have an associated *interface* or framework (which complies with Frameworks Library Standard).

---

## Benefits

The primary benefit of **encoders** is this technique provides a convenient way to create gas efficient, on-chain binary encoded transactions

which can be used to interact with **contracts**, **proxies**, **diamonds**, **GSN relays**, **multisig wallets**, **payable tokens** and more.

Another benefit of this technique being it allows for minimizing byte-code when making external,

calls to any *contract* which accepts arbitrary binary payloads either at a low-level on-chain or at a high-level off-chain,

since deployed **encoders** bytecode is external to which ever *contract* utilizes it,

while also allowing for developing significantly less complex and more straight forward *contract* code,

since both **encoder** libraries and **encoder** contracts allow easy,

compossible use with many other smart contracts wishing to make arbitrary external *contract* calls.

---

## Implementation

A trivial example of an ABI **Encoder** library for the **ERC-173** standard might look similar to this example:

```auto
// SPDX-License-Identifier: Apache-2.0

pragma solidity >=0.6.4  (www.twitter.com/StudiosVigil) - copyright 30/8/2021, All Rights Reserved
///
library abiEncoderERC173
{
    bytes internal constant SIG_OWNER = abi.encodeWithSignature('owner()');
    bytes internal constant SIG_RENOUNCE_OWNERSHIP = abi.encodeWithSignature('renounceOwnership()');

    string internal constant STUB_TRANSFER_OWNERSHIP = 'transferOwnership(address)';

    function transferOwnership(
        address newOwner
    )internal pure returns(
        bytes memory
    ){
        return abi.encodeWithSignature(
            STUB_TRANSFER_OWNERSHIP,
            newOwner
        );
    }
}
```

The associated interface **may** look similar to this:

```auto
// SPDX-License-Identifier: Apache-2.0

pragma solidity >=0.6.4  (www.twitter.com/StudiosVigil) - copyright 30/8/2021, All Rights Reserved
///
interface iEncoderERC173
{
    function owner(
    )external pure returns(
        bytes memory
    );

    function renounceOwnership(
    )external pure returns(
        bytes memory
    );

    function transferOwnership(
        address newOwner
    )external pure returns(
        bytes memory
    );
}
```

Then a *contract* implementing this interface and utilizing the library might look similar to this:

```auto
// SPDX-License-Identifier: Apache-2.0

pragma solidity >=0.6.4  (www.twitter.com/StudiosVigil) - copyright 30/8/2021, All Rights Reserved
///
abstract contract EncoderERC173ABC is iEncoderERC173
{
    constructor(
    )internal
    {
    }

    function owner(
    )public pure override returns(
        bytes memory
    ){
        return abiEncoderERC173.SIG_OWNER;
    }

    function renounceOwnership(
    )public pure override returns(
        bytes memory
    ){
        return abiEncoderERC173.SIG_RENOUNCE_OWNERSHIP;
    }

    function transferOwnership(
        address newOwner
    )public pure override returns(
        bytes memory
    ){
        return abiEncoderERC173.transferOwnership(
            newOwner
        );
    }
}
```

The **encoder** in this example **should not** to be deployed as is, since a concrete *contract* **should** at least implement **ERC-165** (or implement some other runtime interface introspection specification such as **EIP-1820**) and also derive from this abstract base *contract*,

or other contracts to provide additional functionality as necessary, including other **encoders** (which **may** also derive from/support multiple other **EIP** standard interfaces).

An example of a fully realized and deployable **ABI Encoder** *contract* for the **EIP-173 standard** might look like this:

```auto
// SPDX-License-Identifier: Apache-2.0

pragma solidity >=0.6.4  (www.twitter.com/StudiosVigil) - copyright 30/8/2021, All Rights Reserved
///
contract EncoderERC173Ownership is ERC165,
    EncoderERC173ABC
{
    constructor(
    )public
        ERC165()
        EncoderERC173ABC()
    {
        _registerInterface(type(iEncoderERC173).interfaceId);
    }
}
```

---

## Rationale

External calls to **contracts**, **proxies**, **diamonds**, **GSN relays**, **multisig wallets**, **payable tokens** or other similar construct in solidity which accept arbitrary binary encoded payloads for executing *contract* functions

(either natively or via an external API), is both time consuming and tedious for developers and can be the source of subtle bugs (ie, if the string used for the function stub contains a typo, which will not be reported by the compiler, making them difficult to track down).

Offering a fast, cheap, reusable and immutable means by which to accurately and trustlessly ABI encode EVM compatible binary payloads for **EIP** standard compliant contracts as outlined in this proposal,

serves to address a major issue developers face when dealing with the complex nature of interacting with contracts on-chain on a low-level,

or interacting with proxy primitives (which don’t provide an external ABI) from a high level, off-chain context such as a console or JavaScript browser.

By providing a standardized means by which to develop ABI **encoder**s,

this burden on developers is greatly alleviated, while also providing the smallest possible byte-code and gas cost for consuming an **EIP** compliant *contract*’s services

for use both on and off chain.

---

## Security Considerations

Since this standard guarantees contracts which implement this proposal only have constant data members and *pure** methods (which never modify the blockchain or access storage),

there are no immediately obvious security concerns outside potential selector collision.

Here it is important to realize that an **encoder** and the specific **EIP** it is derived from would share the same interface ID,

since currently only the function name and arguments are considered when abi encoding a transaction,

without any regard for the return type of the data.

If, for example, an ERC-165 *supportsInterface* call on an ERC-20 token with: *type(iEncoderERC20).interfaceId*

the result would return true, while also returning true if calling *supportsInterface* on an ERC-20 Encoder passing it: *type(iEncoderERC20).interfaceId*,

despite this not being the indented effect considering they are different interfaces,

which share function name and argument types but differ in return types and modifiers.

This, however is not a security concern for this standard to address,

since that is specifically an implementation detail of the EVM compiler and constitutes a separate proposal in its own right.

It is also important to acknowledge this technique does not guarantee,

nor prevent, any security issues or flaws present in the underlying **EIP** that the corresponding ABI **encoder** is based on,

since there is no validation done on the arguments being encoded,

such things are the responsibility of the executing logic *contract*, not the **encoder** to address.

For example, using an ABI **Encoder** to call an ERC-20 token method with known security concerns (eg. such as *approve*)

on a **proxy** does nothing to circumvent or alleviate any underlying security concerns regarding the very well known double spend attack when revoking a pre-approved amount.

Similarly, an ABI **encoder** smart *contract* simply encodes a transaction, returning the binary payload for executing the desired method on an external *contract*.

It is thus the responsibility of *contract* developers and administrators to ensure that the underlying *contract*’s implementation security concerns are addressed in regards to that specific proposal.

---

## References

- EIP-165: Interface Support
- EIP-1822: Universal Upgradeable Proxy Standard (UUPS)
- EIP-2535: Diamonds
- EIP-2470: Singleton Factory
- EIP-1613: Gas Station Network
- EIP-1363: Payable Token

---

## Copyright

Copyright and related rights waived via CC0.

---

## Citation

Tyler R. Drury, “EIP-TBD: **Transaction Encoder Standard** [DRAFT]”,

Ethereum Improvement Proposals, no TBD, March 2022. [Online serial].
