---
source: magicians
topic_id: 3941
title: EIP-2315 Simple Subroutines for the EVM
author: gcolvin
date: "2020-01-22"
category: EIPs > EIPs core
tags: [evm, opcodes, core-eips, shanghai-candidate, eip-2315]
url: https://ethereum-magicians.org/t/eip-2315-simple-subroutines-for-the-evm/3941
views: 70083
likes: 43
posts_count: 141
---

# EIP-2315 Simple Subroutines for the EVM

## Abstract

This proposal provides a *complete*, *efficient*, *safe* and *static* control-flow facility.

It introduces two new opcodes to support calling and returning from subroutines:

- RJUMPSUB relative_offset – relative jump to subroutine
- RETURNSUB – return to PC after most recent RJUMPSUB.

It depends on the two new opcodes proposed by EIP-4200 to support static jumps:

- RJUMP relative_offset — relative jump to PC + relative_offset
- RJUMPI relative_offset — conditional relative jump

It deprecates `JUMP` and `JUMPI`, allowing valid code to support streaming, one-pass, and other near-linear compilers.

In concert with EIP-3540 and EIP-3670 it ensures, at initialization time, that valid code will not execute invalid instructions or jump to invalid locations, will not underflow stack, will maintain consistent numbers of inputs and outputs for subroutines, and will have bounded stack height in the absence of recursion.

This is among the simplest possible proposals that meets these requirements.


      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-2315)





###



Two opcodes for efficient, safe, and static subroutines.










> September 9, 2022:  The world keeps turning, and this proposal evolves with it.  We can now have immediate data, relative jumps, and no more JUMP, JUMPI or JUMPDEST.  So this draft removes BEGINSUB and returns to the original design of just two new opcodes, but with immediate data.  It retains the validity constraints and algorithm adapted from EIP-615.  Which means we can at long last write one-pass compilers.

## Replies

**lithp** (2020-01-22):

I’m probably just being slow but I don’t understand why this should be adopted, and the provided rationale doesn’t clear anything up for me. If it’s already possible to implement subroutines then as inelegant as the current situation might be why introduce a native subroutine mechanism? It can be implemented more efficiently, letting contracts have a lower gas cost? It makes static analysis on the resulting contracts easier? It unlocks other future changes with cool benefits?

---

**gcolvin** (2020-01-22):

Yes, lower gas costs.  And yes, easier static analysis - you can know that the code is a subroutine call or return, rather than try to work it out by pattern matching Solidity or other conventions.

---

**gcolvin** (2020-02-02):

Pulling over from AllCoreDevs.

Tomasz Kajetan Stańczak [@tkstanczak](/u/tkstanczak) 06:22

[@gcolvin](/u/gcolvin) would be good to have a test for nested JUMPSUB and a JUMPSUB nested in a CALL invoked from inside the subtoutine

---

**gcolvin** (2020-02-02):

[@tkstanczak](/u/tkstanczak) [@holiman](/u/holiman)  Here are a couple more test cases, probably wrong as I hurry to get out in the sun.

```auto
offset step op        stack
0      0    PUSH1 3   []
1      1    JUMPSUB   [3]
2      8    STOP      []
3      2    JUMPDEST  []
4      3    PUSH1 7   []
5      4    JUMPSUB   [7]
6      7    RETURNSUB []
7      5    JUMPDEST  []
8      6    RETURNSUB []
```

Program should `STOP` with an empty stack after 8 steps.

```auto
offset step op        stack
0      0    PUSH1 3   []
1      1    JUMPSUB   [3]
2      2    JUMPDEST  []
3      3    RETURNSUB []
1      4    JUMPSUB   []
```

Program should `STOP` with an empty stack after 4 steps, due to virtual zero at end of code.

---

**tkstanczak** (2020-02-02):

I think the second one will cause InvalidJumpDestination exception (which is a good test case too).

---

**tkstanczak** (2020-02-02):

```
offset step op        stack
0      0    PUSH1 3   []
1      1    JUMPSUB   [2]
2      2    JUMPDEST  []
3      3    RETURNSUB []
4      4    STOP   []
```

---

**gcolvin** (2020-02-02):

The idea here is to demand nothing, but simply provide a mechanism.  For this EIP such demands will need to be made by other tools.

---

**gcolvin** (2020-02-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tkstanczak/48/2667_2.png) tkstanczak:

> offset step op stack
> 0 0 PUSH1 3
> 1 1 JUMPSUB [2]
> 2 2 JUMPDEST
> 3 3 RETURNSUB
> 4 4 STOP

`PUSH1 2` I assume.  The second time this hits `RETURNSUB` it will pop the `codesize` left on the call stack and jump to the implicit 0 past the end of the code (at offset 5) and stop.  It will never get to the `STOP` at offset 4.

---

**gcolvin** (2020-02-14):

```auto
contract fun {
    function multiply(uint x, uint y) returns (uint) {
        return x * y;
    }
    function test() returns (uint) {
        return multiply(2,3);
    }
}

Solidity:
   MULTIPLY:
      0x0
      dup2
      dup4
      mul
      swap1
      pop
      swap3
      swap2
      pop
      pop
      jump
   TEST:
      0x0
      RTN
      0x2
      0x3
      MULTIPLY
      jump
   RTN:
      swap1
      pop
      swap1
      jump

Comparable EIP-2315 or EIP-615:
   MULTIPLY:
       mul
       returnsub
   TEST:
       0x2
       0x3
       MULTIPLY
       jumpsub
       returnsub
```

---

**lialan** (2020-02-17):

Pros:

- Less gas consumption
- much easier for static analysis
- better readability: concise and clear syntax
- easier to maintain
- less error prone
- no hard fork needed

Cons:

- nothing.This is how a machine should work.

---

**gcolvin** (2020-02-17):

Optimized code from the latest solc does a better job with the multiply() function, which is a leaf.  Non-leaf functions remain costly to get out of, as shown by adding a layer to the test.

```auto
contract fun {
    function multiply(uint x, uint y) public returns (uint) {
        return x * y;
    }
    function test_mul(uint x, uint y) public returns (uint) {
        return multiply(x,y);
    }
    function test(uint x, uint y) public returns (uint) {
        return test_mul(2,3);
    }
}
```

Here is what solc can do now with just `jump`:

```auto
1  MULTIPLY:
5     mul
3     swap1
8     jump
=
17 gas

1  TEST_MUL:
5     0x00
5     RTN
5     dup4
5     dup4
5     MULTIPLY
8     jump
=
34 gas

1  RTN:
3     swap4
3     swap3
2     pop
2     pop
2     pop
8     jump
=
21 gas (twice)

   TEST:
5     0x00
5     RTN
5     0x02
5     0x03
5     TEST_MUL
5     jump
=
30 gas

123 gas TOTAL
```

But with `jumpsub` and `returnsub` only a third as much gas is needed.

```auto
1  MULTIPLY:
5     mul
3     returnsub
=
9 gas

1  TEST_MUL:
3     MULTIPLY
5     jumpsub
3     returnsub
=
12 gas

1  TEST:
3     0x02
3     0x03
3     TEST_MUL
5     jumpsub
3     returnsub
=
18 gas

39 gas TOTAL
```

---

**lialan** (2020-02-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> contract fun { function multiply(uint x, uint y) public returns (uint) { return x * y; } function test_mul(uint x, uint y) public returns (uint) { return multiply(x,y); } function test(uint x, uint y) public returns (uint) { return test_mul(2,3); } }

Surprised to see the optimizer doing such a bad job. But yeah this test case shows exactly how the subroutine features would benefit sophisticated situations like this.

---

**gcolvin** (2020-02-24):

I haven’t tried to hand-optimize the Solidity output, but I don’t think that it could do much better.  It’s intrinsically difficult to handle subroutines without instructions for the purpose, as the history of CPU development pretty clearly shows.

I’m not sure what’s sophisticated here – just two function calls and one multiplication.

---

**lialan** (2020-02-25):

Some diggings: On Remix it is using Solidity compiler’s legacy optimizer, which cannot handle functions with calls to other functions, hence the non-optimized TEST_MUL function.

---

**gcolvin** (2020-02-25):

Hi [@lialan](/u/lialan) The output above is from the latest solc.

---

**axic** (2020-02-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> And yes, easier static analysis - you can know that the code is a subroutine call or return, rather than try to work it out by pattern matching Solidity or other conventions.

Is static analysis **that** much easier if all the subroutine offsets are still dynamic (e.g. not an immediate on `JUMPSUB`)?

---

**gcolvin** (2020-02-26):

Better to say, *some kinds* of static analysis, [@axic](/u/axic), as I’ve heard complaints about the problem of deciphering subroutines in EVM code, and the EIP gives a good example.  Other kinds analysis don’t care.

---

**axic** (2020-02-28):

The reason none of this optimised is that all functions are marked `public`. That means all of them need to made available externally. In a more realistic example, most of those would not be marked `public` and then they become inlined or better optimised.

---

**gcolvin** (2020-02-28):

[@axic](/u/axic)  Thanks, I’ll try that.  The public case is still relevant, but I also want to see what the limits are.

---

**gcolvin** (2020-03-01):

[@axic](/u/axic), [@lialan](/u/lialan), [@holiman](/u/holiman). [@karalabe](/u/karalabe).  This program should be more optimizable. test() must be public or else the optimizer tries to eliminate everything.

```auto
pragma solidity >0.6.2;
contract fun {
    function test(uint x, uint y) pure public returns (uint) {
        return test_mul(x, y);
    }
    function test_mul(uint x, uint y) pure private returns (uint) {
        return multiply(x, y);
    }
    function multiply(uint x, uint y) pure private returns (uint) {
        return x * y;
    }
}
```

Compiling with `solc --asm --optimize fun.sol` gives this.  I don’t fully understand what it is doing.

```auto
   TEST:
      0x00
      OUT
      dup4
      dup4
      MULTIPLY
      jump
   OUT:
      swap4
      swap3
      pop
      pop
      pop
      jump
   MULTIPLY:
      0x00
      dup2
      dup4
      mul
      OUT
      jump
```

Code generation with JUMPSUB should also optimize away test_mul.

```auto
  TEST:
     MULTIPLY
     jumpsub
     returnsub

  MULTIPLY:
     mul
     returnsub
```

I think in both cases the multiply() function could be inlined, but then there would be no test.


*(120 more replies not shown)*
