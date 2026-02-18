---
source: ethresearch
topic_id: 16324
title: Solidity Function Types conversion
author: maniou-T
date: "2023-08-10"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/solidity-function-types-conversion/16324
views: 878
likes: 2
posts_count: 3
---

# Solidity Function Types conversion

In docs-soliditylang-org-en-v0.8.21.pdf, p65

A function type A is implicitly convertible to a function type B if and only if their parameter types are identical, their return types are identical, their internal/external property is identical and 1. the state mutability of A is more restrictive than the state mutability of B.

In particular:

• pure functions can be converted to view and non-payable functions

• view functions can be converted to non-payable functions

2. payable functions can be converted to non-payable functions

No other conversions between function types are possible.

The rule about payable and non-payable might be a little confusing, but in essence, if a function is payable, this means that it also accepts a payment of zero Ether, so it also is non-payable. On the other hand, a non-payable function will reject Ether sent to it, so non-payable functions cannot be converted to payable functions. To clarify, 3.rejecting ether is more restrictive than not rejecting ether. This means you can override a payable function with a non-payable but not the other way around.

Above statement 1,2,3 contradict each other.

## Replies

**zetsuboii** (2023-08-12):

You can think of a non-payable function as a payable function that requires `msg.value` to be 0. A non-payable function like this:

```auto
function myFunction() external {}
```

is (kind of) compiled to this

```auto
function myFunction() external payable {
  assert(msg.value == 0);
}
```

So in essence, a non-payable function is more restrictive than the payable one. And that’s why you can use a payable function where a non-payable function is required.

---

**maniou-T** (2023-08-14):

Thanks, it’ s very clear.Your code example neatly demonstrates the idea, showing how a non-payable function is more restrictive.

