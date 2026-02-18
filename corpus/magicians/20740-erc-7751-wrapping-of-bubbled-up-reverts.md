---
source: magicians
topic_id: 20740
title: "ERC-7751: Wrapping of Bubbled Up Reverts"
author: marktoda
date: "2024-08-07"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7751-wrapping-of-bubbled-up-reverts/20740
views: 539
likes: 10
posts_count: 20
---

# ERC-7751: Wrapping of Bubbled Up Reverts

Discussion for [Add ERC 7751: Wrapping of bubbled up reverts by gretzke · Pull Request #578 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/578)

## Replies

**fallenderl** (2024-08-14):

very cool & sufficient gas trade offs for improved UX! i feel it needs be emphasised that following this at usual entry point contracts like SCA, routers etc is important to not lose the stack trace.

---

**Amxx** (2024-09-02):

I’d like to propose a profound change to the ERC.

**Motivation**

Currently the ERC relies on thwo things to detect and precess wrapped custom errors:

- Being able to detect the custom error (human readable) name from its “selector” (and argument format)
- Being able to identify the relevant custom errors by looking at a prefix in the custom error name

Saying that the first step is resolved by the presence of the ABI is big oversimplification. In practice it doesn’t work that well.

- If the contract is not verified, you don’t have an ABI to check. In particular, some networks may not have an obvious verification workflow.
- If the contract is a proxy, you need to know which ABI to look for. Simple ERC-1167 clones are usually well suported, but other proxy pattern are not that easy to work with. In particular, when dealing with a diamond proxy (ERC-1538 / ERC-2535), it is not obvious how to know which facet was used and get the correct ABI from the facet’s verified source code
- Last bu not least, when If a contract just “bubbles” the custom error without using this wrapper syntax, the ABI used to decode the wrapper will be hidden in the trace.

User calls contract A
- Contract A calls Contract B
- Contract B calls Contract C
- Contract C revert with some custom error
- Contract B catches the error, and wrap it in a Wrapping custom error
- Contract A gets the wrapped error from B, and bubble’s it without any wrapping

Here, You have A that throws a wrapped custom error that you cannot decode unless you know that it comes from B.

The big strenght of `require(boolean, string)` is that it emits a standardized format `Error(string)` that everyone should be able to decode without having to know any ABI. If that gets bubbled from contract to contract, you may lose the information about who triggered it (you need a trace for that) but you don’t lose the ability to decode the reason (and display it to users).

I think this EIP should target the same thing. A wrapped custom error should be (at least partly) decodable without any information about the ABI of the contract that triggered it.

**Specification**

When a contract performs a (static)-call, and when that operation fails with some `bytes` encoding the reason (that can be a custom error, a panic, a revert reason, …), then the contract that received that error can emit the following custom error

```solidity
error WrappedError(address target, bytes4 selector, bytes reason, bytes details);
```

With

- target: the address that was called, and that returned an error
- selector: the first 4 bytes of the call that reverted. If the call was an eth transfer without any data, put bytes4(0) here
- reason: The error message that was received
- params: an optional buffer that contains details about the operation that fails. It should correspond to a custom error declared on the contract that emits the WrappedError,

it should be formated using a 4 bytes selector, similar to how function data and custom errors are encoded
- it should be possible to decode it using the ABI of the contract that wrapped the error.

The benefit of this approach is that without the ABI, the only thing you miss is the ability to decode the optional `params`. You still have full ability to determine that “this function on this contract failled, and this is what we got”.

Note that this allows to rebuild revert traces from nested `WrappedError` without having to decode the `params`.

**Example and pseudocode**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {IERC20} from "@openzeppelin/contracts/interfaces/IERC20.sol";

interface IERC7751 {
    error WrappedError(address target, bytes4 selector, bytes reason, bytes details);
}

contract Vault {
    error WithdrawError(address to, uint256 amount);

    function withdraw(IERC20 token, address to, uint256 amount) external {
        // logic
        try token.transfer(to, amount) {} catch (bytes memory error) {
            revert IERC7751.WrappedError(address(token), token.transfer.selector, error, abi.encodeWithSignature("WithdrawError(address,uint256)", to, amount));

            //NOTE: if solidity was to add support for https://github.com/ethereum/solidity/pull/14974, we could do
            //revert IERC7751.WrappedError(address(token), token.transfer.selector, error, abi.encodeError(WithdrawError, to, amount));
        }
    }
}
contract Router {
    function withdraw(IERC20 token, Vault vault, uint256 amount) external {
        // logic
        try vault.withdraw(token, msg.sender, amount) {} catch (bytes memory error) {
            revert IERC7751.WrappedError(address(vault), vault.withdraw.selector, error, new bytes(0));
        }
    }
}
```

For decoding a custom error that was received (by calling contract `context`), one can do

```javascript
const {ethers} = require('ethers');

function* indentEach(indent, lines) {
    for (const line of lines) {
        if (Array.isArray(line)) {
            yield* indentEach(indent + 1, line);
        } else {
            const padding = '    '.repeat(indent);
            yield* line.split('\n').map(subline => (subline === '' ? '' : padding + subline));
        }
    }
}

function formatLines(...lines) {
    return [...indentEach(0, lines)].join('\n') + '\n';
}

function tryDecode(fragment, data) {
    const error = ethers.ErrorFragment.from(fragment);
    const interface = ethers.Interface.from([ error ]);
    try {
        return interface.decodeErrorResult(error, data);
    } catch {
        return undefined;
    }
}

function parseError(error, context) {
    if (details = tryDecode('Error(string)', error))
    {
        const [ reason ] = details;
        return [
            '[ Revert with reason ]',
            `- reason: ${reason}`,
        ];
    }
    else if (details = tryDecode('WrappedError(address,bytes4,bytes,bytes)', error))
    {
        const [ target, selector, reason, params ] = details;
        const withParams = ethers.getBytes(params).length > 0;
        return [
            '[ Wrapped Error ]',
            `- calling function ${selector} on contract ${target}`,
            `- with underlying error:`,
            parseError(reason, target),
            withParams && `- and params:`,
            withParams && parseError(params, context),
        ].filter(Boolean);
    }
    else
    {
        return [
            '[ Unknown error ]',
            `- raw data: "${error}"`,
            `- try decoding it using ABI at ${context}`,
        ];
    }
}

const IERC7751 = ethers.Interface.from([ 'error WrappedError(address,bytes4,bytes,bytes)' ]);
const StringInterface = ethers.Interface.from([ 'error Error(string)' ]);
const ParamsInterface = ethers.Interface.from([ 'error SomeParams(uint256, uint256)' ]);
const error = IERC7751.encodeErrorResult(
    'WrappedError',
    [
        '0x33da045DC129a97807FCb13bf30baa2Fb2DcC29F',
        '0x321f2612',
        IERC7751.encodeErrorResult(
            'WrappedError',
            [
                '0xd6B94a1b01c0e79AF91178A8eF0dcc0F7B191708',
                '0xa9059cbb',
                StringInterface.encodeErrorResult(
                    'Error',
                    [
                        'big badaboom'
                    ]
                ),
                '0x'
            ]
        ),
        ParamsInterface.encodeErrorResult(
            'SomeParams',
            [
                17,
                42
            ]
        )
    ]
);
console.log(formatLines(parseError(error, '0x239F4A46A9b348A4DE4008ba2DaC4b8be26daDba')));
```

That returns

```auto
    [ Wrapped Error ]
    - calling function 0x321f2612 on contract 0x33da045DC129a97807FCb13bf30baa2Fb2DcC29F
    - with underlying error:
        [ Wrapped Error ]
        - calling function 0xa9059cbb on contract 0xd6B94a1b01c0e79AF91178A8eF0dcc0F7B191708
        - with underlying error:
            [ Revert with reason ]
            - reason: big badaboom
    - and params:
        [ Unknown error ]
        - raw data: "0xe55cbd440000000000000000000000000000000000000000000000000000000000000011000000000000000000000000000000000000000000000000000000000000002a"
        - try decoding it using ABI at 0x239F4A46A9b348A4DE4008ba2DaC4b8be26daDba
```

---

**frangio** (2024-09-02):

Ideally, the address of the contract that produces the error and the calldata it was processing should be retrievable from the execution layer without smart contract code.

Currently one could look at the execution trace to try to do that, but unreliably heuristics are needed to differentiate original errors from errors that are bubbled up.

In that sense, I do think this ERC gets right the fact that the smart contract needs to explicitly mark an error as bubbled. But it would be better if we could omit the address and the calldata (or function arguments), since those should technically be retrievable in some other way.

There’s also the issue that traces are too heavyweight. We would need nodes to provide error data in receipts.

---

**ernestognw** (2024-09-02):

Overall I agree with [@Amxx](/u/amxx) motivations for changing the EIP. However, it’s not clear to me how the new proposal fixes the error bubbling for proxies (e.g. ERC-1167 clones, ERC1967 proxies), for those cases the ABI is still hidden one execution context deeper than expected.

Some off-chain tooling I’ve worked with checks whether the contract has a non-zero address at the ERC1967 implementation slot and then it retrieves the implementation ABI (if available) but it’s not 100% reliable. For example, one can purposely deploy a proxy pointing to another proxy just to obfuscate the lower level information.

I tend to agree with [@frangio](/u/frangio) that the address of the smart contract (in general, the execution context trace) should be provided by other mechanisms, but, many wallets don’t have access to execution traces when they show an error in a UI as they only check for the gas estimation to determine whether the transaction reverts or not. That makes me think that it’s just easier to add the `address` to the `WrappedError` [@Amxx](/u/amxx) is proposing.

---

**Amxx** (2024-09-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ernestognw/48/7916_2.png) ernestognw:

> I tend to agree with @frangio that the address of the smart contract (in general, the execution context trace) should be provided by other mechanisms

I thinbk we all agree that should be available. But the fact is, it is not available today.

Changing the client to include more information is a long and tedious process. The goal of this ERC is to propose a solution that is available right now, in the app/user space, without any client modifications.

---

**SamWilsn** (2024-09-29):

You should probably mention in the security considerations section that contracts may lie/incorrectly report the called contract, and that the information isn’t guarantee to be correct.

---

**0age** (2024-09-30):

So the key tradeoffs here as far as I see them:

- we want to be able to “bubble up” the original revert as that’s still the primary indicator of what went wrong, and clearly identifying what contract that original revert was tripped by is important
- we want to keep expressiveness on the top-level contract that contextualizes the error
- we want to be able to handle nested reverts
- we don’t want an unknown interface or non-compliant revert to completely brick the visibility of the error
- we don’t want wallet support to be a blocker to the standard’s usefulness

So what I’d propose to address this tradeoff space is something like this:

```solidity
struct RevertPayload {
    address target;
    bytes data;
}

error NestedRevert(RevertPayload[] revertChain);
```

(Note that this struct could optionally include `selector` or `details` like the `WrappedError` suggested by [@Amxx](/u/amxx), though I suspect they might not be necessary and especially `selector` might not be applicable in all cases e.g. single-function contracts or fallbacks.)

Then, the way you’d use it would be something like:

- Contract A calls contract B
- Contract B calls contract C
- Contract C reverts, returns a standard custom error
- Contract B sees the revert, and builds a length-two RevertPayload[] array where:

the first element has {target: Contract_B, data: Contract_B_Custom_Error(...)} and
- the second element has {target: Contract_C, data: Contract_C_Custom_Error(...)}

Contract B uses that array as the argument for throwing `NestedRevert`
Contract A sees the `NestedRevert`, and builds a length-three `RevertPayload[]` array where:

- the first element has {target: Contract_A, data: Contract_A_Custom_Error(...)},
- the second element has {target: Contract_B, data: Contract_B_Custom_Error(...)}, and
- the third element has {target: Contract_C, data: Contract_C_Custom_Error(...)}

What I like about this approach is that:

- the contract bubbling up the revert can add whatever context it wants to the error
- arbitrary levels of nesting still work
- if one of the contracts in the chain doesn’t know about this standard, you still keep the context from the higher-level reverts (especially if it’s the original revert, in which case it “just works”

Thoughts?

---

**hensha256** (2024-09-30):

[@0age](/u/0age) doesnt that mean that each level of the stack, the contract that receives a revert has to:

- check the custom error has NestedRevert selector
- decode the array of structs
- create a new array of length+1
- iterate through filling it up again
- wrap it in a NestedRevert selector

And at every step it has to assume that the data inside NestedRevert was badly formed. And then if up a level theres another contract, it has to follow this whole process again?

It feels like a very complex and gas-expensive revert process? or am i misunderstanding something?

---

**Amxx** (2024-10-01):

While I think [@0age](/u/0age) does make sens (I’d add a selector but that is beside the point) … I share [@hensha256](/u/hensha256)’s concerns about the complexity of the re-nesting operation. Its not just about gas cost of execution, but also about deployment size.

I think we should try to implement a compliant contract to see what it looks like to decode and re-encode the array.

---

**0age** (2024-10-01):

OK, here’s a working example that’s decently optimized:

```solidity
    /// @dev performs a call and returns the result on success; on a revert, looks for a `NestedRevert` custom error and
    ///      inserts address(this) and the supplied error data as the first element before passing along the revert; if
    ///      `NestedRevert` is not detected, it creates a new `NestedRevert` with 2 elements where the first element is
    ///      address(this) and errorData and the second element is target and the revert data returned by the target.
    ///      Do note that this code still needs to be cleaned up quite a bit from here and is missing all but most basic
    ///      tests; it also does not hold up very well to adversarial conditions (e.g. a target that gives fake NestedRevert
    ///      data back in its custom error) — though it's important to remember that untrusted targets can already grief on
    ///      revert visibility by consuming all available gas, by "revert-bombing" with huge revert messages, or even just
    ///      by returning misformatted revert data in general.
    function _lowLevelCallWithNestedRevertPassing(
        address target,
        bytes memory data,
        bytes memory errorData
    ) internal returns (bytes memory result) {
        assembly {
            // Clear scratch space.
            mstore(0, 0)

            // Perform the call and write first 4 bytes of returndata to last 4 bytes of scratch space
            if iszero(call(gas(), target, 0, add(data, 0x20), mload(data), 0x1c, 0x24)) {
                // Compare with 0xcd33d02d (NestedRevert.selector)
                if and(eq(mload(0), 0xcd33d02d), and(gt(returndatasize(), 0x43), eq(mload(0x20), 0x20))) {
                    // Read existing array length from returndata
                    returndatacopy(0, 0x24, 0x20)
                    let existingArrayLength := mload(0)
                    let newArrayLength := add(existingArrayLength, 1)

                    // Calculate size of new element
                    let errorDataLength := mload(errorData)
                    let newElementSize := add(0x80, mul(0x20, div(add(errorDataLength, 31), 32)))

                    // Calculate total size of new NestedRevert structure
                    let newStructSize := add(returndatasize(), newElementSize)

                    // Allocate memory for the new NestedRevert structure
                    let newNestedRevert := mload(0x40)
                    mstore(0x40, add(newNestedRevert, newStructSize))

                    // Copy selector and array offset
                    mstore(newNestedRevert, 0xcd33d02d)
                    mstore(add(newNestedRevert, 0x20), 0x20)

                    // Update array length
                    mstore(add(newNestedRevert, 0x40), newArrayLength)

                    // Calculate first element offset (relative to start of data)
                    let firstElementOffset := shl(5, newArrayLength)
                    mstore(add(newNestedRevert, 0x60), firstElementOffset)

                    // Copy existing offsets and adjust them
                    let offsetsStart := add(newNestedRevert, 0x80)
                    returndatacopy(offsetsStart, 0x44, shl(5, existingArrayLength))
                    for { let i := 0 } lt(i, existingArrayLength) { i := add(i, 1) } {
                        let offsetPos := add(offsetsStart, mul(i, 0x20))
                        mstore(offsetPos, add(mload(offsetPos), newElementSize))
                    }

                    // Add new element (address(this) and errorData)
                    let newElementStart := add(add(0x60, newNestedRevert), firstElementOffset)
                    mstore(newElementStart, address())
                    mstore(add(newElementStart, 0x20), 0x40)  // Offset to errorData within the element
                    mstore(add(newElementStart, 0x40), errorDataLength)

                    // Copy errorData
                    let errorDataStart := add(errorData, 0x20)
                    for { let i := 0 } lt(i, errorDataLength) { i := add(i, 0x20) } {
                        mstore(add(add(newElementStart, 0x60), i), mload(add(errorDataStart, i)))
                    }

                    // Copy existing RevertPayload elements
                    let existingDataStart := add(0x44, mul(existingArrayLength, 0x20))
                    let existingDataSize := sub(returndatasize(), existingDataStart)
                    returndatacopy(
                        add(add(newElementStart, 0x60), mul(0x20, div(add(errorDataLength, 31), 32))),
                        existingDataStart,
                        existingDataSize
                    )

                    // Revert with new NestedRevert structure
                    revert(add(0x1c, newNestedRevert), newStructSize)
                }

                // If no `NestedRevert` detected from the target, generate a new NestedRevert encoding
                let nestedRevertErrorPayload := mload(0x40)
                mstore(nestedRevertErrorPayload, 0xcd33d02d)  // NestedRevert selector
                mstore(add(nestedRevertErrorPayload, 0x20), 0x20)  // Offset to start of dynamic array
                mstore(add(nestedRevertErrorPayload, 0x40), 2)  // length of revertChain array (2 elements)

                // Offset to first element (fixed)
                mstore(add(nestedRevertErrorPayload, 0x60), 0x40)

                // Calculate offset to second element (dynamic)
                let errorDataLength := mload(errorData)
                let firstElementSize := add(0x60, mul(0x20, div(add(errorDataLength, 31), 32)))
                let secondElementOffset := add(0x40, firstElementSize)
                mstore(add(nestedRevertErrorPayload, 0x80), secondElementOffset)

                // First element: address(this) and errorData
                mstore(add(nestedRevertErrorPayload, 0xa0), address())
                mstore(add(nestedRevertErrorPayload, 0xc0), 0x40)  // offset to errorData
                mstore(add(nestedRevertErrorPayload, 0xe0), errorDataLength)  // length of errorData
                for { let i := 0 } lt(i, errorDataLength) { i := add(i, 0x20) } {
                    mstore(add(add(nestedRevertErrorPayload, 0x100), i), mload(add(add(errorData, 0x20), i)))
                }

                // Second element: target and full returndata
                let secondElementStart := add(nestedRevertErrorPayload, add(0xa0, firstElementSize))
                mstore(secondElementStart, target)
                mstore(add(secondElementStart, 0x20), 0x40)  // offset to returndata
                mstore(add(secondElementStart, 0x40), returndatasize())
                returndatacopy(add(secondElementStart, 0x60), 0, returndatasize())

                // Calculate new payload length
                let newLength := add(
                    add(0xa0, firstElementSize),
                    add(0x60, mul(0x20, div(add(returndatasize(), 31), 32)))
                )

                // Update free memory pointer
                mstore(0x40, add(nestedRevertErrorPayload, newLength))

                // Revert with new payload
                revert(add(0x1c, nestedRevertErrorPayload), add(4, newLength))
            }

            // Allocate memory and copy over the result
            result := mload(0x40)
            mstore(0x40, add(result, and(add(add(returndatasize(), 0x20), 0x1f), not(0x1f))))
            mstore(result, returndatasize())
            returndatacopy(add(result, 0x20), 0, returndatasize())
        }
    }
```

---

**0age** (2024-10-01):

just tried this with a `NestedRevert` with 3 reverts in the chain (so it’s adding a fourth) and total execution cost of the tx was 4694 gas; so overhead is actually pretty manageable from what I can tell!

If you took a more adversarial approach where you were suspicious of what the target was giving you (e.g. add an explicit tryDecode + verify step) it would definitely get pricier.

---

**0age** (2024-10-01):

also checked the size; this clocks in at 608 bytes of runtime code (encourage anyone to check my math on any of the above!)

---

**gretzke** (2024-10-02):

another benefit with [@0age](/u/0age)’s approach is that you also get the address of the contract throwing the top most error

---

**gretzke** (2024-10-03):

Updated ERC based on feedback from [@Amxx](/u/amxx) and [@SamWilsn](/u/samwilsn)

https://github.com/ethereum/ERCs/pull/665

---

**Amxx** (2024-10-04):

Well, this confirms it can be done, and its not necessarily an expensive operation.

But I’m not sure that addresses the “complexity” concerns. Holy shit that is a lot of assembly !

---

**Amxx** (2024-10-04):

For the record, here is a solidity version, that most likelly is way more expensive because of all the memory copies involved:

```auto
import { Bytes } from "./Bytes.sol";

interface IERC7751 {
    struct RevertPayload {
        address target;
        bytes data;
    }

    error NestedRevert(RevertPayload[] revertChain);
}

interface IRevert {
    function revertEndpoint(string calldata reason) external;
}

contract RevertWithString is IRevert {
    function revertEndpoint(string calldata reason) external pure {
        revert(reason);
    }
}

contract RevertWithERC7751 is IRevert {
    function revertEndpoint(string calldata reason) external view {
        IERC7751.RevertPayload[] memory revertChain;
        revertChain = new IERC7751.RevertPayload[](1);
        revertChain[0] = IERC7751.RevertPayload({ target: address(this), data: bytes(reason) });
        revert IERC7751.NestedRevert(revertChain);
    }
}

contract ERC7751 {
        function revertNested1(address target, string calldata args) public {
        try IRevert(target).revertEndpoint(args) {
            // happy path, out of scope here
        } catch (bytes memory reason) {
            if (bytes4(reason) == 0xcd33d02d) {
                IERC7751.RevertPayload[] memory oldRevertChain = abi.decode(Bytes.slice(reason, 4), (IERC7751.RevertPayload[]));
                IERC7751.RevertPayload[] memory revertChain = new IERC7751.RevertPayload[](oldRevertChain.length + 1);
                for (uint256 i = 0; i < oldRevertChain.length; ++i) revertChain[i] = oldRevertChain[i];
                revertChain[oldRevertChain.length] = IERC7751.RevertPayload({ target: address(this), data: "" });
                revert IERC7751.NestedRevert(revertChain);
            } else {
                IERC7751.RevertPayload[] memory revertChain = new IERC7751.RevertPayload[](2);
                revertChain[0] = IERC7751.RevertPayload({ target: target, data: reason });
                revertChain[1] = IERC7751.RevertPayload({ target: address(this), data: "" });
                revert IERC7751.NestedRevert(revertChain);
            }
        }
    }
}
```

---

**gretzke** (2024-10-07):

I implemented the updated ERC spec in Uniswap v4 here:



      [github.com](https://github.com/Uniswap/v4-core/blob/6526044abffee244cbf7e8ee66c04c8182ad34f0/src/libraries/CustomRevert.sol#L81-L109)





####



```sol


1. /// @notice bubble up the revert message returned by a call and revert with a wrapped ERC-7751 error
2. function bubbleUpAndRevertWith(address target, bytes4 functionSelector, bytes4 additionalContext) internal pure {
3. bytes4 wrappedErrorSelector = WrappedError.selector;
4. assembly ("memory-safe") {
5. let size := returndatasize()
6. // Ensure the size of the revert data is a multiple of 32 bytes
7. let encodedDataSize := mul(div(add(size, 31), 32), 32)
8.
9. let fmp := mload(0x40)
10.
11. // Encode wrapped error selector, address, function selector, offset, additional context, size, revert reason
12. mstore(fmp, wrappedErrorSelector)
13. mstore(add(fmp, 0x04), target)
14. mstore(add(fmp, 0x24), functionSelector)
15. // offset revert reason
16. mstore(add(fmp, 0x44), 0x80)
17. // offset additional context
18. mstore(add(fmp, 0x64), add(0xa0, encodedDataSize))
19. // size revert reason
20. mstore(add(fmp, 0x84), size)


```

  This file has been truncated. [show original](https://github.com/Uniswap/v4-core/blob/6526044abffee244cbf7e8ee66c04c8182ad34f0/src/libraries/CustomRevert.sol#L81-L109)










It’s called when a hook call fails for example:



      [github.com](https://github.com/Uniswap/v4-core/blob/6526044abffee244cbf7e8ee66c04c8182ad34f0/src/libraries/Hooks.sol#L136)





####



```sol


1. }
2.
3. /// @notice performs a hook call using the given calldata on the given hook that doesnt return a delta
4. /// @return result The complete data returned by the hook
5. function callHook(IHooks self, bytes memory data) internal returns (bytes memory result) {
6. bool success;
7. assembly ("memory-safe") {
8. success := call(gas(), self, 0, add(data, 0x20), mload(data), 0, 0)
9. }
10. // Revert with FailedHookCall, containing any error message to bubble up
11. if (!success) CustomRevert.bubbleUpAndRevertWith(address(self), bytes4(data), HookCallFailed.selector);
12.
13. // The call was successful, fetch the returned data
14. assembly ("memory-safe") {
15. // allocate result byte array from the free memory pointer
16. result := mload(0x40)
17. // store new free memory pointer at the end of the array padded to 32 bytes
18. mstore(0x40, add(result, and(add(returndatasize(), 0x3f), not(0x1f))))
19. // store length in memory
20. mstore(result, returndatasize())
21. // copy return data to result


```










Are there any additional concerns with the specification?

---

**danylonepritvoreniy** (2024-12-01):

How does the ERC-7751 proposal balance the trade-off between adding context to nested reverts and minimizing gas costs, especially in complex execution chains involving proxies or diamond patterns?

---

**gretzke** (2024-12-02):

I don’t see where proxies or diamond pattern contracts add a significant overhead compared to a normal contract as this would generally only affect reverting calls, not delegate calls.

Additionally I would argue that contracts don’t have to revert using 7751 wrapped errors if they don’t need to add any additional context compared to a plain bubbled up revert. The ability for nested reverts allows us to add additional data to the revert while preserving wrapped reverts that happened further down the execution chain without overwriting them.

