---
source: magicians
topic_id: 23040
title: "EIP-7899: On-Chain Function Return Type Encoding for Solidity Functions"
author: genkifs
date: "2025-03-03"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7899-on-chain-function-return-type-encoding-for-solidity-functions/23040
views: 216
likes: 22
posts_count: 21
---

# EIP-7899: On-Chain Function Return Type Encoding for Solidity Functions

Discussion topic for EIP-7899

- 2025-03-01: On-Chain Function Return Type Encoding for Solidity Functions, commit 26603fc

#### External Reviews

None as of 2025-03-03.

#### Outstanding Issues

None as of 2025-03-03.

## Replies

**SanLeo461** (2025-03-03):

I’m interested in the why the decision was made to limit the encoding to use `bytes32`, when more complex types such as `bytes`  in solidity could be used? This would allow infinite function size, and could even increase efficiency for small functions in many cases.

Another thought, for this to see a decent amount of adoption, ideally the tokenization process would be handled by the compiler, to avoid having to manually do or re-do this whenever writing/editing a function.

---

**genkifs** (2025-03-03):

1/ Your points are valid, and a bytes approach could be correct.  I also have a possible version using Bytes (see base of this message).

I went for bytes32 in the EIP because this is the most common size in the EVM and receiving a guaranteed fixed size definition seemed better for standardization and compatibility.

Bytes will always append 2x32bytes (0x20 and the bytestream length) to the start of any information returned, which seemed less efficient for small return types.

I’m flexible on this point.  I’d like to hear opinions from the community supporting either option.

---

2/ Yes, an optional parameter when compiling would be very useful and certainly help with standardization while also reducing the possibility of implementation error, but it would also slightly increase the bytecode size of the contract so I wouldn’t enforce it.

---

```
/**
 * @notice Encodes an array of uint8[] tokens into a bytes array.
 * @param tokens Array of uint8 tokens.
 * @return result The encoded bytes stream.
 */
function encodeStream(uint8[] memory tokens) internal pure returns (bytes memory result) {
    result = new bytes(tokens.length);
    for (uint256 i = 0; i < tokens.length; i++) {
        result[i] = bytes1(tokens[i]);
    }
}

/**
 * @notice Decodes an encoded bytes stream into an array of tokens.
 * @param encoded The bytes token stream.
 * @return tokens An array of tokens.
 */
function decode(bytes memory encoded) internal pure returns (uint8[] memory) {
    uint8[] memory tokens = new uint8[](encoded.length);
    for (uint256 i = 0; i < encoded.length; i++) {
        tokens[i] = uint8(encoded[i]);
    }
    return tokens;
}
```

---

**genkifs** (2025-03-04):

Ok, some quick tests.  Comparing gas cost using bytes instead of bytes32

Construction +312276

Storage +1232

Recall +874

So bytes are less gas efficient even for small numbers of return types.  But maybe the small addition cost of moving to Bytes is worthwhile for both future proofing and clarity of code.

Code below was tested quickly in Remix.

```
'''solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// construction 516913 gas
contract test{

     // 3633 gas
    mapping (bytes4 => bytes) public funcReturn;

    // "0x00000000","0x"
    // 29271 gas
    //  "0x00000000","0x0000000000000000000000000000000000000000000000000000000000000001"
    // 77814 gas
    // "0x00000005","0x05"
    // 52371 gas
    // "0x00000009","0x04050704"
    // 52413 gas
    // "0x00000018","0x000000000000000000000000000000000000000000000000000000000000001056"
    // 103583 gas
    function addBytes(bytes4 _index, bytes memory _in ) public  {
        funcReturn[_index] = _in;
    }
}

// construction 204637 gas
contract test2{

    //2759 gas
    mapping (bytes4 => bytes32) public funcReturn;

    // "0x00000001","0x0000000000000000000000000000000000000000000000000000000000000001"
    // 51139 gas
    function addBytes(bytes4 _index, bytes32 _in ) public  {
        funcReturn[_index] = _in;
    }
}
```

---

**wjmelements** (2025-03-05):

I have never not once wanted or needed this. The solidity 4byte abi is already clear enough about parameters and return types.

---

**genkifs** (2025-03-05):

The solidity 4byte abi is clear about parameters, but not about return types.  I’ll give you an example.

Let’s call the function “0x2fbebd38” [*“foo(uint256)”*] on a proxy contract.

I know I need to send a *uint* payload.

What is the shape of the data I am expecting back?

---

**wjmelements** (2025-03-05):

The 4byte ABI does include return type. It’s true though that the selector collides with other methods that would return different data. But if you’re using an interface you assume it conforms to the protocol. The level of trust depends on circumstance.

If users are supplying accounts that may or may not comply with a desired interface, you have to handle non-compliance with our without strict typing. An example of this is that USDT transfer returns null instead of 1 (but has the same selector). UniswapV1 reverts if the return value isn’t 1, while UniswapV2 simply disregards the output data unless it’s 0.

The problem is not solved by adding type assertions into the return data. Noncompliance is always possible. Even if solidity had always had this, it is possible to program without solc. The problem is also not solved by putting return types in the selector, though that’s a good idea and would have prevented accidental nonconformance like USDT.

---

**genkifs** (2025-03-05):

> if you’re using an interface you assume it conforms to the protocol.

From an on-chain perspective the protocol only defines the input for the interface.  The output is not defined at all.  It is not currently possible for a contract to assume anything.

> If users are supplying accounts that may or may not comply with a desired interface, you have to handle non-compliance with our without strict typing.

This EIP is about giving a contract the *optional* ability to supply the strict typing of the return

> Noncompliance is always possible.

Agreed.  But the option to provide compliance information using on-chain methods in a standardised way is useful.

> The problem is not solved by adding type assertions into the return data.

This is not what is being proposed.  Type definitions are being added to a separate function that can be optionally called.

> The problem is also not solved by putting return types in the selector

This is not what is being proposed.  This EIP does not change existing ABI definitions.  It is a separate function called in an optionally implemented interface.

> It’s true though that the selector collides with other methods that would return different data.

This is not what is being proposed.  This EIP does not attempt to address the (rare but possible) problem of duplicate signatures.

---

To clarify, EIP-7899 does not modify Solidity’s ABI encoding or change how selectors are derived. Instead, it introduces an optional metadata function that allows contracts to expose return type information in a standardized way.

This enables safer and more predictable interactions, reducing the likelihood of runtime errors when dealing with unknown or mutable contracts.

Standardization does not enforce strict typing, but offers an additional tool for developers who want to ensure compatibility of return types without resorting to off-chain methods.

---

**wjmelements** (2025-03-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/genkifs/48/7593_2.png) genkifs:

> From an on-chain perspective the protocol only defines the input for the interface. The output is not defined at all. It is not currently possible for a contract to assume anything.

We disagree on the meaning of “can assume”. I will now address both. For mine, everyone can assume the return type, even without your change; UniswapV1 can and does assume, sometimes incorrectly, that the token parameter implements ERC20. For yours, nobody can assume the return type, even with your change; I can write a contract in assembly that implements `funcReturn` and returns lies about the return data of other functions. The presense of `funcReturn` is irrelevant in either case; the ability to assume is unchanged for both meanings.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/genkifs/48/7593_2.png) genkifs:

> This EIP does not attempt to address the (rare but possible) problem of duplicate signatures.

Yes it does. You are trying to distinguish `transfer(address,uint256) returns (uint256)` from `transfer(address,uint256) returns (void)`. These ABI both have the same selector, which is a real problem.

---

**SanLeo461** (2025-03-05):

The only realistic usecase I can think of for this is for building a programmatic interface for contracts without traditional contract verification, this could be in the case where the program is using a weird/unsupported compiler, or raw bytecode, or in situations where getting that data is not viable for some reason.

But even then, it would only be provided on an “best case” / “as-is” basis, and would have no actual guarantee of correctness or safety, unlike contract verification.

---

**genkifs** (2025-03-05):

> UniswapV1 can and does assume, sometimes incorrectly, that the token parameter implements ERC20.

Ok lets use ERC20. From an on-chain point of view a contract can get `keccak256("balanceOf(address)") = "0x70a08231"` and so we know the function needs to called with a bytes20.  Off chain we can look up the agreed standard (if it exists), but *on-chain* the calling contract doesn’t know that it will receive back a uint256.

In this EIP no off chain information is needed.  For this example a contract would use ERC165 to check that `"funcReturn(bytes4)"` exists in the calling contract, then it would call `funcReturn("0x70a08231")` and receive the answer `"0x2F"` (padded with 0’s if we choose 32bytes over a bytes array).

For a standardized interface like ERC20 this doesn’t add much value, but for an arbitrary contract, being able to advise **on-chain** what the shape of the returning information will be is useful.

> I can write a contract in assembly that implements funcReturn and returns lies about the return data of other functions.  The presense of funcReturn is irrelevant in either case; the ability to assume is unchanged for both meanings.

True.  This EIP is about providing information to on chain contracts about the shape of the return data, not providing trust in the result.

> You are trying to distinguish transfer(address,uint256) returns (uint256) from transfer(address,uint256) returns (void) . These ABI both have the same selector.

No.  It’s not that both these ABI have the same selector.  It’s that neither `returns (uint256)` nor `returns (void)` enter into the ABI definition.  Only function name and input type(s) `keccak256("transfer(address,uint256)")` are defined by the ABI.

Return type is not part of the ABI, hence the need for this EIP

---

**wjmelements** (2025-03-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/genkifs/48/7593_2.png) genkifs:

> It’s that neither returns (uint256) nor returns (void) enter into the ABI definition

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/genkifs/48/7593_2.png) genkifs:

> Return type is not part of the ABI

This is incorrect. They are defined in the ABI. In solidity 4byte ABI it is the `outputs` field. Example

```auto
"outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}]
```

As aforementioned I think it would be beneficial for the return type to be part of the selector for future method-hash ABIs because it would catch return type programming errors like USDT transfer.

---

**genkifs** (2025-03-05):

Yes, one use case is to enable bytecode analysis without requiring source code access.

This is particularly useful in the case where the code being called is encrypted/obfuscated/unverified but the interface for the returned result needs to be known in advance.

The concept is not new.  **REST APIs** return JSON or XML with predefined field structures.  This is just the EVM equivalent of that documentation, on-chain.

Contract verification is more rigorous, testing step by step logic at every stage of computation.  This EIP is much simpler.  Just generating on-chain documentation for how the the output should be received.

---

**genkifs** (2025-03-05):

Ok.  Can you compile these following two contracts to bytecode, submit the transaction, then, using only solidity and the on-chain data, extract the bytes32 and address return types.

```
contract A{
    function foo() public returns (bytes32) {

    }
}
contract B{
    function foo() public returns (address) {

    }
}
```

If it’s easy to do and doesn’t cost much gas, then we can let this EIP die.

---

**wjmelements** (2025-03-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/genkifs/48/7593_2.png) genkifs:

> Ok. Can you compile these following two contracts to bytecode, submit the transaction, then, using only solidity and the on-chain data, extract the bytes32 and address return types.

Which brings us full circle:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> I have never not once wanted or needed this. The solidity 4byte abi is already clear enough about parameters and return types.

---

**genkifs** (2025-03-05):

The on-chain 4byte abi function signature does *not* contain return type information.

**Proof:**  The function signature (e.g.  “0x2fbebd38”) does not change if return type is modified.

There is no circularity (yet).  I asked if it is possible to efficiently extract the return type of a function only from on-chain contract data.  You seem confident it can be done.

- If you have a technical, on-chain solution that makes EIP 7899 redundant then please give details.  A rough outline would be sufficient.
- If you have other improvements to EIP 7899 then please give details.

---

**wjmelements** (2025-03-06):

You don’t know the precise meaning of the words you are using. This post will seek to educate you, after which you can reread my posts with clarity. My position should then be clear, that

1. This is not a problem that needs solving
2. Nobody can solve this problem
3. Your ERC does not solve the problem

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/genkifs/48/7593_2.png) genkifs:

> You seem confident it can be done.

ABI does not refer to the selector. It refers to the entire `Application Binary Interface`, which includes the encoding and decoding of the binary inputs and outputs.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/genkifs/48/7593_2.png) genkifs:

> The on-chain 4byte abi function signature

In the solidity 4byte ABI, this is called the selector.

---

**genkifs** (2025-03-06):

Thanks for you time and effort.  Your confusions and misunderstandings are helping me to increase the clarity of the EIP.   To provide precise meaning I will quote from the soliditylang documentation.

[Function Selector](https://docs.soliditylang.org/en/latest/abi-spec.html#function-selector)

> The first four bytes of the call data for a function call specifies the function to be called.   The return type of a function is not part of this signature. The JSON description of the ABI however contains both inputs and outputs.

This documentation implies

- The on-chain binary data does not encode the outputs.
- The off-chain human readable description of the ABI does contain output information, but it is inaccessible to on-chain contracts.
- Neither inputs nor outputs are decoded by the ABI.

To address your position

*1. This is not a problem that needs solving*

It may not be a problem **you** need solving.  I need to solve this problem.

*2. Nobody can solve this problem*

*3. Your ERC does not solve the problem*

EIP-7899 solves this problem for me.  It may also solve it for someone else, either now or in the future.  In my opinion it much better to get a community review of the proposal rather than create a maverick implementation.

While I have your attention.  Do you have any opinion on the following:-

### Token Definitions

- 0x01: bool
- 0x02: address
- 0x0C: complex numbers
- 0x10–0x2F: uint8 … uint256 (each increment means +8 bits)
- 0x30–0x4F: int8 … int256
- 0x50–0x6F: bytes1 … bytes32
- 0xB0: bytes (dynamic)
- 0xB1: string
- 0xE0: dynamic array marker; a dynamic array is encoded as [0xE0, elementType]
- 0xE1: fixed array marker; a fixed array is encoded as [0xE1, length, elementType]
- 0xF0: tuple start, 0xF1: tuple end

---

**genkifs** (2025-03-06):

Following your feedback I’ve moved from bytes32 to bytes.  Less efficient in terms of gas but more readable and no limit on return type complexity.

---

**wjmelements** (2025-03-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/genkifs/48/7593_2.png) genkifs:

> The on-chain binary data does not encode the outputs.

No, it definitely does. Perhaps your confusion is with the meaning of encoding and decoding.

You probably mean that the selector does not itself *specify* or *define* the output types. I pointed this out several times with the example of USDT, but you ironically said your proposal was not addressing this situation here:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/genkifs/48/7593_2.png) genkifs:

> It’s true though that the selector collides with other methods that would return different data.

This is not what is being proposed. This EIP does not attempt to address the (rare but possible) problem of duplicate signatures.

I am glad I brought this to your attention.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/genkifs/48/7593_2.png) genkifs:

> The off-chain human readable description of the ABI does contain output information, but it is inaccessible to on-chain contracts

It’s accessible to users of the interface at their compile-time, which is what is necessary to decode.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/genkifs/48/7593_2.png) genkifs:

> Neither inputs nor outputs are decoded by the ABI.

This is factually incorrect, unless you mean the interface itself doesn’t literally do the coding; it only defines the encoding and decoding. The meaning and types of the binary are well-defined by the binary interface. Perhaps the words you don’t know are encoding and decoding. Hard to know, but we aren’t speaking the same language.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/genkifs/48/7593_2.png) genkifs:

> I need to solve this problem.

I doubt it, but I suppose anyone can invent problems for themself. Academics do it all of the time.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/genkifs/48/7593_2.png) genkifs:

> EIP-7899

It’s not an EIP. It’s an ERC. You are still trying to merge it into the wrong repository even after I pointed this out to you [on Github](https://github.com/ethereum/EIPs/pull/9433#issuecomment-2699989798).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/genkifs/48/7593_2.png) genkifs:

> EIP-7899 solves this problem for me.

Probably not. It can’t when a contract doesn’t implement your method. It can’t when a contract implements the method incorrectly or maliciously. If you assume these things you might as well assume that it implements the desired interface correctly in the first place. As I said previously:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> If users are supplying accounts that may or may not comply with a desired interface, you have to handle non-compliance with our without strict typing

The ability to opt into this doesn’t change anything in the security or application modeling. It does create chaos if a subsequent ERC decides to use it to facilitate arbitrary return types. A better way to return arbitrary data would be to return the encoded type with the arbitrarily-typed data. I don’t think there are many use cases for this on-chain.

> Contracts don’t have to check off-chain sources to understand return data.

Contracts are not doing this.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/genkifs/48/7593_2.png) genkifs:

> Do you have any opinion

Your 1-byte type definitions are good. I don’t like that composite types can be arbitrarily long, but so can Solidity types.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/genkifs/48/7593_2.png) genkifs:

> 0x0C: complex numbers

Does solidity have a complex number type?

---

**genkifs** (2025-03-06):

> No, it definitely does.

Not according to the official documentation.  There the output definition exists only in the JSON description of the ABI, not in the bytecode.

If you want to prove once and for all that you are correct, please compile an example contract and demonstrate how to recover the return types from the bytecode.

> [the JSON is] accessible to users of the interface at their compile-time.

Not in all cases.  We cannot decode future contracts that are yet to be designed.

> Perhaps the words you don’t know are encoding and decoding.

The input types are encoded with a keccak256 hash and a truncation.  There is no way to decode that one way mapping.

The output types are only defined in the off-chain JSON file and are neither automatically encoded nor decoded.

> It’s not an EIP. It’s an ERC.

I am indifferent.  For the moment we will follow [SamWilsn’s naming decision](https://github.com/ethereum/EIPs/pull/9433/commits/121060c2b9bcf9acb1ddb2730924c991aabba4d4)

> It can’t when a contract doesn’t implement your method.

Correct.  This would be an optional standard,  If ERC165 isn’t followed then the return types will not even be queried.

> It can’t when a contract implements the method incorrectly or maliciously.

Agreed.  Automated complier integration would be a nice way to reduce this risk. But not essential for the EIP.

> A better way to return arbitrary data would be to return the encoded type with the arbitrarily-typed data.

Not ideal.  For example, that doesn’t stop a uint256 being mistaken for an address.  It also makes adoption compulsory where as my proposal is optional.

> Your 1-byte type definitions are good.

Great.  That’s the real meat of the proposal that I would like the community to accept/discuss.

> I don’t like that composite types can be arbitrarily long, but so can Solidity types.

Me neither, it stops everything fitting nicely into an efficient bytes32 storage space.  It is what it is.  I’ve swapped to a bytes array because if an edge case exists, someone is bound to hit it at some point.

> Does solidity have a complex number type?

There is a [stagnant EIP](https://eips.ethereum.org/EIPS/eip-5850).  I’m taking the liberty of reserving a placeholder for them.

