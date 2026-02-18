---
source: magicians
topic_id: 285
title: "EIP-1065: Suggestion to add a logarithm opcode to the EVM"
author: fubuloubu
date: "2018-05-06"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-1065-suggestion-to-add-a-logarithm-opcode-to-the-evm/285
views: 1159
likes: 1
posts_count: 10
---

# EIP-1065: Suggestion to add a logarithm opcode to the EVM

I know this has probably been discussed before, but I think it might be worth implementing as an instruction in the EVM so that higher level languages can make use of it.

Issue here:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/1065)












####



        opened 07:53PM - 05 May 18 UTC



          closed 04:15AM - 20 Dec 21 UTC



        [![](https://avatars.githubusercontent.com/u/3859395?v=4)
          fubuloubu](https://github.com/fubuloubu)





          stale







Was curious what issues there would be with adding a integer logarithm opcode?
[…]()
I understand that logarithm opcodes for other processors are typically floating point instructions, but there has got to be a decent fixed-point operation that can be implemented in our 256-bit processor, that also minimizes information loss from the operation (especially when using change of bases to compute arbitrary logarithms), and is bounded by a constant time for a reasonable input.

I have a preliminary idea for such an algorithm [here](https://github.com/fubuloubu/evm-logarithm), but I am sure there are holes in such an approach that can be improved upon. My preliminary approach uses 256 loops at most, at costs about 160k gas. Hopefully that can be substantially reduced with an opcode.

A good minimal implementation would be able to implement at least a base 2 logarithm instruction that compiler writers could leverage via `log_a(b) = (DIV (B2LOG b 2) (B2LOG a 2))` either internally or through a psuedo opcode that implements that macro.

## Replies

**fulldecent** (2018-05-20):

I do not support this because the concept of real numbers (e.g. float, double) is not in the EVM.

---

**fubuloubu** (2018-05-20):

This would be an integer operation, approximated by an algorithm that was efficient for this narrow case, perhaps even as narrow as only allowing `log_2(x)` and `log_10(x)` for `x` in `[1, 2**256-1]`. Output would be `uint256` as well, so it would be rounded off or truncated to the nearest whole number.

Compiler Developers would then use logirithmic rules and identities to create more expansive use cases to capture the correct precision required for different operations on different types (fixed or integer) using these opcodes as a basis. These may be more complex operations, but they would be more useful and much cheaper if they had dedicated opcodes in EVM versus implementation as compiler macros or library calls.

---

**fulldecent** (2018-06-04):

Anyway, here is an implementation in Solidity:

```auto
pragma solidity ^0.4.23;

contract Math {
    function logarithm2(uint256 input) external pure returns(uint256 output) {
        uint256 value = input;
        if (value > 2^128) {
            value >>= 128;
            output += 128;
        }
        if (value > 2^64) {
            value >>= 64;
            output += 64;
        }
        if (value > 2^32) {
            value >>= 32;
            output += 32;
        }
        if (value > 2^16) {
            value >>= 16;
            output += 16;
        }
        if (value > 2^8) {
            value >>= 8;
            output += 8;
        }
        if (value > 2^4) {
            value >>= 4;
            output += 4;
        }
        if (value > 2^2) {
            value >>= 2;
            output += 2;
        }
        if (value > 2^1) {
            output += 1;
        }
    }
}
```

If this should become an opcode one day, I would expect many people to use the Solidity approach first so as to demonstrate the value.

---

**charles-cooper** (2019-02-22):

I agree that integer log2 is not that useful since the output range is [0,255] and it can be implemented easily as a library function. But I think that an opcode or precompile which calculates the log2 mantissa could be useful.

---

**charles-cooper** (2019-02-22):

The reason it would be useful is that you can implement pretty much all interesting floating point operations once you have the mantissa. cf. https://github.com/BANKEX/solidity-float-point-calculation/blob/master/contracts/FloatMath.sol, https://github.com/ethereum/vyper/issues/1266#issuecomment-465800310

---

**jochem-brouwer** (2019-02-22):

I disagree with adding this opcode to EVM. It is relatively cheap to verify the log of a number via the `EXP` opcode (with a hardcoded `e` constant and of course a precision). You can do these things off-chain and simply input the number into the transaction. The same applies to `SQRT`.

---

**fubuloubu** (2019-02-23):

To explain a very relevant potential use case, just think of everyone’s favorite mechanism du jour: bonding curves. These opcodes would both make the calculation of bonding curve math much easier, and that’s an example of something that is best calculatee on-chain, to allow dynamic repositioning of price targets (instead of forcing the client to calculate off-chain and validate them in the contract)

---

**jochem-brouwer** (2019-02-23):

I was thinking about my statement of “just plug in the solution off-chain” but then started to realize that this would mean you know the on-chain external “factors” which might influence the number you are trying to get the logarithm for. I must admit that this is indeed not doable in some practical use cases.

But we must also keep in mind that our opcode space is limited. I start to think this might be a good addition, together with some more mathematical handy functions like square roots or just a “root” function which takes two stack arguments: the number want to know the root of and the target root (e.g. cubic).

---

**fubuloubu** (2019-02-23):

Potentially. The best part about log2 and sqrt is that they are highly composable for other mathematical operations. Heck, [@charles-cooper](/u/charles-cooper) was showing me a trick to compute sqrt from log2 I think.

For example `log_b(a) = log_2(a) / log_2(b)` allows you to do the log of any possible base!

