---
source: magicians
topic_id: 1170
title: Building a taxonomy of smart contract errors
author: Arachnid
date: "2018-08-28"
category: Magicians > Primordial Soup
tags: [dx, errors]
url: https://ethereum-magicians.org/t/building-a-taxonomy-of-smart-contract-errors/1170
views: 1781
likes: 10
posts_count: 8
---

# Building a taxonomy of smart contract errors

Our goal: To develop a comprehensive error taxonomy for Ethereum smart contracts. A taxonomy helps categorise types of error, and ensure that different applications report the same kind of error the same way.

Using error codes in place of descriptive messages has several other advantages:

- Reduces the gas cost of deploying contracts.
- Permits internationalization of error messages.
- Permits automated handling of expected error types

The need for a proper error taxonomy was recognized during several audits as well as working on the development of ENS smart contracts.

We propose to break errors up into a two-level taxonomy of error types. At the top level are major types: Basic reasons that something may fail, such as invalid input or invalid state. Under each major type are minor types: specific cases of the major type.

Major type and minor type numbers each range from 1 to 255, enabling each to be packed in a single byte, if necessary.

The minor type is then optionally followed by an application-specific error code, in the range 0-65536.

In text form, a fully qualified error is represented in the form “E.x.y.z”, where x is the major type, y is the minor type, and z is the app-specific error code.

We’d value your input - please propose changes and additions to the taxonomy, and we’ll adjust it to suit.

# Taxonomy

This is a work in progress - please help us expand and curate this list.

## 1: Invalid Input

Errors that occur purely due to the format or contents of the input data belong here.

### 1.1: Value too small

Examples:

- Trying to set a price below a limit.
- Supplying a timestamp that is before the current time.

### 1.2: Value too large

Examples:

- Trying to set a value above a limit.
- Supplying a timestamp that is more than a year in the future.

### 1.3: Value mismatch

Examples:

- Supplying a different number of elements in two matched array inputs.
- Mixing element types in a homogenous array.

### 1.4: Invalid syntax

Examples:

- Including invalid characters in a string

### 1.5: Feature not supported

Examples:

- Specifying an enum value that is not implemented.

### 1.255: Other

## 2: Invalid State

Errors that occur due to the current state of the contract, or due to a combination of input and state.

### 2.1: Input caused overflow/underflow

Examples:

- Trying to issue or transfer more tokens than can be represented.

### 2.2: Data not found

Examples:

- Attempting to reference a mapping entry that is unset.

### 2.3: Value too small

Examples:

- Attempting to transfer more tokens than are in an account.
- Attempting to call transferFrom from an account that has insufficient (or no) allowance.

### 2.4: Value too large

Examples:

- Attempting a transfer that would exceed an account’s limit

### 2.5: Value must be nonzero

Examples:

- Attempting to specify an address of 0.
- Attempting to set a limit to 0.

### 2.6 Value must be zero

Examples:

- Attempting to set a token allowance from one nonzero value to another.

### 2.7: No code at address

Examples:

- Supplying an external account when a contract is expected.
- Supplying a nonexistent account address.

### 2.8: Interface not implemented

Examples:

- Supplying the address of a contract that does not implement a required interface.

### 2.9: Feature Disabled

Examples:

- Trying to vote after a voting period has ended.

### 2.10: Action Already Completed

Examples:

- Trying to reveal a bid that has already been revealed.

### 2.255: Other

## 3: Unauthorised

### 3.1: Unauthorised caller

Examples:

- Calling an ‘owner only’ contract with an account other than the owner.

### 3.2: Unauthorised signer

Examples:

- Submitting a signed message with an unrecognised signer.

### 3.3: Insufficient authorisations

Examples:

- Submitting a request to a multisig with too few signatures.

### 3.255: Other

## 4: Internal Error

### 4.1: Internal Error

## Replies

**cwhinfrey** (2018-08-28):

Couple ideas:

1. Feature disabled - An error code under “Invalid State” for when a function is not available or is guaranteed to fail with the current state or “phase” of the contract (e.g. calling bid() before bidding is opened, calling vote() after the voting period has ended.)
2. Action has already been completed - An error code under “Invalid State” for when an action that should only be performed once is attempted again. (e.g. revealVote() is called for a vote that has already been revealed)
Are these too specific?

---

**izqui** (2018-08-28):

I really like this. We have been hesitant to introduce revert reasons because of how expensive having error strings in the contract code is.

I wonder if the address of the contract where the error originates should be included in the returned error data as well, so the error would be “E.x.y.z.addr”. In the case of Solidity, if a contract makes a call that reverts, the parent context will revert with the same data. This would make it hard to identify in which contract the error originated, so the application-specific error would be hard to properly detect.

---

**Arachnid** (2018-08-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cwhinfrey/48/8002_2.png) cwhinfrey:

> Feature disabled - An error code under “Invalid State” for when a function is not available or is guaranteed to fail with the current state or “phase” of the contract (e.g. calling bid() before bidding is opened, calling vote() after the voting period has ended.)
> Action has already been completed - An error code under “Invalid State” for when an action that should only be performed once is attempted again. (e.g. revealVote() is called for a vote that has already been revealed)

Good ideas, I’ll add these.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/izqui/48/224_2.png) izqui:

> I wonder if the address of the contract where the error originates should be included in the returned error data as well, so the error would be “E.x.y.z.addr”. In the case of Solidity, if a contract makes a call that reverts, the parent context will revert with the same data. This would make it hard to identify in which contract the error originated, so the application-specific error would be hard to properly detect.

In theory this ought to be discernable using transaction traces, although it’s difficult to do so in practice. Adding it to the revert reason would be very high overhead, however - you’d need code for string concatenation and hex encoding in each contract!

I really, really wish Solidity had added revert ABIs, instead of hardcoding a string-based ‘reason’.

---

**izqui** (2018-08-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> I really, really wish Solidity had added revert ABIs, instead of hardcoding a string-based ‘reason’.

Would it be problematic to just cast an ABI encoded payload for the error as a string so no hardcoded strings need to be added to contracts at all? You can then have an error parser client side that can read those and return a proper string.



      [gist.github.com](https://gist.github.com/izqui/2ffece981bfa1fec74e07164a81e21b2)





####



##### error.sol



```
contract Error {
    function x() {
        revert(error(1, 1, 2567));
    }

    function error(uint8 x, uint8 y, uint16 z) internal view returns (string) {
        return string(abi.encodePacked(x, y, z, address(this)));
    }
}
```

---

**beltran** (2018-08-29):

fantastic.

are those errors to be thrown by the Smart contract (burden on the solidity developer) at runtime or the EVM (or maybe even the compiler in some cases, even though I understand these are mainly runtime errors) ?

maybe separating by these categories further clarifies who has to do what with these errors?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> Supplying a timestamp that is more than a year in the future.

on the topic of out of bounds for example I would leave it to the Solidity developer to signal that a timestamp is too far into the future, rather than hardcoding this limit somewhere.

I can see a use for long term inputs…like bets that happen in the next 5 years

---

**Arachnid** (2018-08-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/izqui/48/224_2.png) izqui:

> Would it be problematic to just cast an ABI encoded payload for the error as a string so no hardcoded strings need to be added to contracts at all? You can then have an error parser client side that can read those and return a proper string.

Not problematic, but a bit weird - Solidity itself is ABI encoding an error string and 4 byte identifier, and we’d be nesting another ABI encoding inside that. It’d be better to be able to return custom ABIs from solidity instead.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/beltran/48/192_2.png) beltran:

> are those errors to be thrown by the Smart contract (burden on the solidity developer) at runtime or the EVM (or maybe even the compiler in some cases, even though I understand these are mainly runtime errors) ?

These errors are up to smart contract developers to return.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/beltran/48/192_2.png) beltran:

> on the topic of out of bounds for example I would leave it to the Solidity developer to signal that a timestamp is too far into the future, rather than hardcoding this limit somewhere.

That was just an example of a case where a contract author might choose to return an error.

---

**shrugs** (2018-08-30):

I had written up a bunch of general error cases when making https://vmexceptionwhileprocessingtransactionrevert.com/ so the content of that website might be helpful here.

