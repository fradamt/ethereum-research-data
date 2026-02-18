---
source: magicians
topic_id: 8574
title: Create a new opcode for muldiv
author: moodysalem
date: "2022-03-11"
category: EIPs
tags: [evm, opcodes]
url: https://ethereum-magicians.org/t/create-a-new-opcode-for-muldiv/8574
views: 2643
likes: 6
posts_count: 11
---

# Create a new opcode for muldiv

In Uniswap V3, we make heavy use of a [FullMath#mulDiv](https://github.com/Uniswap/v3-core/blob/ed88be38ab2032d82bf10ac6f8d03aa631889d48/contracts/libraries/FullMath.sol#L14-L106), which allows you to multiply two numbers `x` and `y` then divide by a third number `d`, when `x * y > type(uint256).max` but `x * y / d <= type(uint256).max`

This function is extremely useful to smart contract developers working with fixed point math. Hari ([@_hrkrshnn](https://twitter.com/_hrkrshnn)) suggested that we write an EIP to add a muldiv opcode.

Is there any reason this shouldn’t be built into the EVM? Should it be a precompile since the result can overflow?

## Replies

**lukasz-glen** (2022-03-12):

What about signed `int256`?

---

**chfast** (2022-03-14):

So this suppose to work like `MULMOD` except it should return quotient instead of remainder? You also need to specify what happens when divisor is zero and when quotient is bigger than `type(uint256).max`.

But fundamentally, I don’t see technical reasons not to have it if useful. The division algorithm in `MULMOD` and other instructions computes both quotient and remainder in general case.

---

**hrkrshnn** (2022-03-14):

Yes. It should be the quotient for from the `mulmod` algorithm. If the quotient is bigger, I was thinking maybe it should truncate to `256` bits. Just `and(2**256 - 1, 512-bit-quotient)`. The zero divisor case can be the same as that for `mulmod`.

---

**moodysalem** (2022-03-14):

Maybe this is obvious, but how do you detect the calculation overflowed if it just returns the lower 256 bits on overflow?

---

**BoringCrypto** (2022-03-16):

This would indeed be very useful. I use this ALL THE TIME!

---

**chfast** (2022-03-16):

Truncating to 256-bit is straight-forward from implementation perspective. But this probably should be checked with formal verification. IIRC returning 0 for division by 0 causes some troubles in verification.

To be clear, this very much make sense as an EIP draft. Someone should start writing it.

---

**PaulRBerg** (2022-04-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boringcrypto/48/3164_2.png) BoringCrypto:

> This would indeed be very useful. I use this ALL THE TIME!

Seconded. A native `muldiv` opcode would allow me to do away with my [monster implementation](https://github.com/paulrberg/prb-math/blob/426aa3d0e1d2d5f26a3118d130ccc1b7a3d0cf4a/contracts/PRBMath.sol#L394-L478) in PRBMath.

And I guess a precompile would be faster than any implementation available today?

---

**moodysalem** (2022-04-18):

[@hrkrshnn](/u/hrkrshnn) et al started an EIP here! [MULDIV instruction by hrkrshnn · Pull Request #5000 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5000)

---

**moodysalem** (2022-06-02):

[@hrkrshnn](/u/hrkrshnn) Why did you opt for special casing `z = 0` instead of returning two stack items, from the EIP?

> Returning two stack items, higher and lower order bits

---

**axic** (2022-07-13):

Yup! It was merged today: [EIP-5000: MULDIV instruction](https://ethereum-magicians.org/t/eip-5000-muldiv-instruction/9930)

