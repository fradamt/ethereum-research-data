---
source: magicians
topic_id: 4229
title: EIP-2315 "Simple Subroutines for the EVM" - Analysis
author: chfast
date: "2020-04-29"
category: EIPs
tags: [evm, opcodes, eip-2315]
url: https://ethereum-magicians.org/t/eip-2315-simple-subroutines-for-the-evm-analysis/4229
views: 6092
likes: 8
posts_count: 58
---

# EIP-2315 "Simple Subroutines for the EVM" - Analysis

*by Pawel Bylica [@chfast](/u/chfast), Andrei Maiboroda [@gumb0](/u/gumb0), and Alex Beregszaszi [@axic](/u/axic).*

This is a short analysis of certain properties of [EIP-2315: Simple Subroutines for the EVM](https://eips.ethereum.org/EIPS/eip-2315) ([version as of 2020-04-16](https://github.com/ethereum/EIPs/blob/fcab0ca9d905ba7baace204fdfd4ab8e4ea76128/EIPS/eip-2315.md)).

We have focused on both usability from compilers point of view and the effect on EVM implementations.

First we discuss two problems, followed by two relevant remarks, which could benefit from the solutions to the problems.

## Fallthrough to next subroutine

### Problem

During instruction-by-instruction execution when `BEGINSUB` is encountered the execution continues (`BEGINSUB` works as no-op). I.e. execution falls through from one subroutine to the next one.

```auto
PUSH 0
CALLDATALOAD
PUSH 32
CALLDATALOAD
JUMPSUB $sub1
PUSH 0
SSTORE

BEGINSUB $sub1
ADD

BEGINSUB $sub2
PUSH 1
ADD
RETURNSUB
```

This feature is not very useful for code generators (Solidity, EVM LLVM) therefore it will not be used. But an EVM implementation has to support it. And this behavior requires additional testing.

This is especially problematic when translating EVM to more structured representation (e.g. LLVM IR). Here we will represent the above example with C-like pseudo-code (as a substitute for LLVM IR functions):

```auto
void entry(char* calldata)
{
    int depth = 0;

    Stack stack;
    stack.push(uint256(calldata[0]));
    stack.push(uint256(calldata[32]));

    // Call the subroutine with bumped depth.
    sub1(&stack, depth + 1);

    sstore(0, stack.pop());
}

void sub1(Stack* stack, int depth)
{
    if (depth == 1023)
        abort();

    uint256 a = stack.pop();
    uint256 b = stack.pop();
    uint256 result = a + b;
    stack.push(result);

    // Because the sub1 does not end with RETURNSUB
    // or any other terminating instruction
    // the next subroutine must be called at the end
    // to emulate subroutine fallthrough behavior.
    // Depth is not bumped though because this is not `JUMPSUB`.
    // Therefore, we can run out of system call stack space.
    sub2(stack, depth);
}

void sub2(Stack* stack, int depth)
{
    if (depth == 1023)
        abort();

    uint256 a = stack.pop();
    uint256 result = a + 1;
    stack.push(result);
}
```

### Solution

Change the specification in a way that `BEGINSUB` can only be reached via `JUMPSUB`. Specifically:

1. Execution of BEGINSUB causes exception (OOG: all gas consumed) and terminates execution. This way BEGINSUB behaves like INVALID (aka 0xfe) and it should never be executed in a well-formed EVM program.
2. JUMPSUB sets the pc to location + 1 (As opposed to location in the current spec).
3. In the edge case when BEGINSUB is the last instruction in code and this subroutine is jumped-to, the implementations should execute STOP. This is consistent with the other similar case of returning from a subroutine jumped-to from the JUMPSUB being the last instruction in code.

## JUMPs across subroutines

### Problem

The EIP intentionally does not modify the semantics of `JUMP`/`JUMPI`s. They are still only restricted to targeting `JUMPDEST`s. It is allowed to jump from any point in one subroutine to any `JUMPDEST`-marked point in another subroutine.

Current EIP properly specifies what would happen in each of these cases, but this feature is not practically useful (code generators are unlikely to use it). And it creates a family of edge cases which are needed to be properly covered with tests.

It seems very impractical to translate such EVM program to C / LLVM IR. The only partial support may be possible by using [setjmp / longjmp](https://en.wikipedia.org/wiki/Setjmp.h). Because of the complexity of such translation C examples are not provided in this section.

1. Example: JUMP to the middle of subroutine

```auto
JUMP $middle

BEGINSUB
DUP1
JUMPDEST $middle
RETURNSUB # Causes exception as return_stack is empty.
```

1. Example: JUMP between subroutines

```auto
JUMPSUB $sub1

BEGINSUB $sub1
JUMP $middle
RETURNSUB

BEGINSUB $sub2
NOT
JUMPDEST $middle
RETURNSUB  # Returns to the "main" code after JUMPSUB.
```

### Solution

1. Use BEGINSUB as strict subroutine boundaries.
1.1. There exists a “main” subroutine starting at PC 0 without BEGINSUB. See Main (subroutine) section.
1.2. Every BEGINSUB opcode position in the code marks the beginning of a new subroutine and the ending of the “previous” subroutine.
1.3. This implies that there’s no code outside of subroutines (all the code is either in explicit subroutines or in the implicit “main” subroutine)
2. When collecting valid JUMPDEST locations (must be done before execution) assign them to subroutines. Instead of having flat list as before, we get 2-level collection grouped by subroutines.
3. During execution keep information which subroutine is currently being executed.
4. During execution when validating a jump target only consider JUMPDESTs from the list of the current subroutine.

#### Example

```auto
00 PUSH 0
02 CALLDATALOAD
03 PUSH 32
05 JUMPDEST
06 CALLDATALOAD
07 JUMPSUB $sub1
08 JUMPDEST
09 PUSH 0
0a SSTORE

0b BEGINSUB $sub1
0c JUMPDEST
0d ADD
0e JUMPDEST
0f RETURNSUB

10 BEGINSUB $sub2
11 PUSH 1
13 ADD
14 JUMPDEST
15 RETURNSUB
```

- Before:
JUMPDESTs: (05, 08, 0c, 0e, 14)
- After:

"main" @ 00: (05, 08)
- "sub1" @ 0b: (0c, 0e)
- "sub2" @ 0f: (14)

### Benefits

1. When checking if a jump destination is valid search is performed on a smaller collection (limited to current subroutine scope only).
2. JUMPDEST analysis (collecting valid jump destinations) can be performed lazily per subroutine. Optimized EVM implementation may perform advanced code analysis and/or translation beyond collecting JUMPDEST offsets.
3. May help with code merklization.
With properly isolated subroutines it is possible to collect a list of subroutines used in a given transaction and it is easy to include in a witness those only. The other two options currently which exist for merklization: a) partition by JUMPDESTs; b) chunk code by even-sized parts, which needs offsets in case of splitting through a PUSH opcode.
With the original EIP, it seems the gains of merklization-by-subroutine is restricted or even diminished by the ability to jump around.
4. Having subroutine-level “pure” control flow (no magic jumps between subroutines) helps performing static analysis.
5. Limits complexity of test cases.
In the original EIP, test cases composed of multiple steps are required. Examples of two-step test cases: (jump cross subroutine, RETURNSUB reached causing exception), (jump cross subroutine, RETURNSUB returns successfully). Test cases composed of 3+ steps may be also needed.
This is not required in the version with restricted jumps because it is only needed to check if execution terminates with exception on “jump cross subroutine”.

### Potential issues caused by the change

1. Jumps across subroutines allow implementing tail subroutine calls.

This is not very elegant. There are two distinct kinds of jumping targets: JUMPDEST and BEGINSUB. However this encourages to also use JUMPs to perform a kind of subroutine call.
2. Suggestion: If tail subroutine calls are desired, let’s introduce a TAILJUMPSUB instruction.
3. This restriction can potentially break existing contracts. E.g.

```auto
JUMP $skip      # Not allowed as $skip JUMPDEST belongs to other subroutine.
BEGINSUB        # Previously invalid instruction, but never executed.
JUMPDEST $skip
```

Suggestion: analyze existing contracts whether this would cause an issue (e.g. search for the BEGINSUB opcode used in existing contracts)

### Remark: example implementation of JUMPDEST analysis

Prior to this EIP, evmone stores `JUMPDEST`'s code offset in an array. They are already ordered so binary search is used to validate a jump destination.

After the change we can still keep `JUMPDEST`s as an array. For subroutines we additionally have to collect ranges of `JUMPDEST`s - it is enough to keep 2 pointers: to the begin/end `JUMPDEST`'s entry in the array. To validate a jump destination do binary search of the current subroutine `JUMPDEST`'s range.

## Main (subroutine)

This section introduces the concept of “main” subroutine as a result of the EIP-2315 “Subroutines” with our two proposed changes.

Execution of an EVM bytecode starts at PC=0 (the “first” byte). We propose that code segment starting as PC=0 and ending just before first `BEGINSUB` (or end-of-code) is now called the “main” subroutine. The following restrictions apply to the “main” subroutine":

1. The return_stack remains empty (i.e. is not populated with the “main” subroutine’s caller return address).
2. Therefore, RETURNSUB is invalid inside “main” subroutine.
3. Since the “main” subroutine does not start with a BEGINSUB, it cannot be called from any other subroutine (including “main” subroutine itself).
4. The “main” subroutine defines the scope for JUMP/JUMPDEST validity - jumps within “main” subroutine are valid as in any other subroutine.

### Comparison with POSIX

We can now compare an EVM bytecode to a "POSIX binary":

```auto
// alias STOP = RETURN(0, 0);

// An example subroutine.
int doSomething() {
  if (random() & 1)
    return 1;  // => RETURNSUB
  else
    exit(0);   // => STOP
}

// The C language main function.
int main() {
  if (doSomething())
      exit(1)  // => RETURN(0, 1)

  // This is not be allowed in EVM, as RETURNSUB is invalid in "main" subroutine.
  return 0;    // => RETURNSUB
}

// The POSIX start fuction - entry point invoked by the operating system.
void start() {
  int ret = main();
  exit(ret);
}
```

Since most current EVM programs start with what resembles "main" above (because they have to ability to "exit" by reaching the end), we don't want to consider and introduce "start" into EVM.

### Benefits

We believe this rather small semantical distinction of “main” subroutine provides a cohesive and structured design, and will prove beneficial in the future.

One potential use case could be in "account abstraction" (AA), where instead of paying with supplied gas or Ether token, there needs to exist some other mean to pay the "miner". It is wished this would exists via executing code, which pays the miner.

Making this possible with main:

1. Disallow JUMP/JUMPI in main
2. The miner has to be paid before the first JUMPSUB
3. Restrict the number of instructions allowed (and terminate if exceeded)

This could seriously reduce the complexity miners would be need to face when evaluating such AA-enabled transactions.

## “BEGINDATA”

A lot of EVM programs contain data. The most prevalent example is constructor bytecode containing the runtime bytecode at the very end. Unfortunately without structure, currently the “data” has to be also analyzed for `JUMPDEST`s.

Some proposals were made to alleviate this by introducing a `BEGINDATA` opcode (see [EIP-615](https://eips.ethereum.org/EIPS/eip-615) and [EIP-2327](https://eips.ethereum.org/EIPS/eip-2327)).

We however think the above changes could also be used to provide an alternative to `BEGINDATA` by placing a unreferenced `BEGINSUB` prior to the data.

**Downside**: this looks like an abuse of `BEGINSUB`, but so far the authors have not found any problem with it.

```auto
# The "main" subroutine: the contract constructor.
COPYCODE($data+1, S)
RETURN(0, S)

# The unreferenced subroutine with data.
BEGINSUB $data
...
```

## Replies

**holiman** (2020-04-29):

Some quick notes/questions, I’ll probably have more when I’ve digested it a bit further.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> Fallthrough to next subroutine

This one is pretty simple, and I agree. Implementation-wise, it can be done either as you describe it or something else, but it’s not a big change.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> ## JUMPs across subroutines
>
>
>
>
> ### Problem
>
>
>
> The EIP intentionally does not modify the semantics of JUMP / JUMPI s. They are still only restricted to targeting JUMPDEST s. It is allowed to jump from any point in one subroutine to any JUMPDEST -marked point in another subroutine.

I agree this is unfortunate.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> ### Benefits
>
>
>
> When checking if a jump destination is valid search is performed on a smaller collection (limited to current subroutine scope only).

This is not necessarily true. Geth does a one-pass analysis, and the lookup is O(1) on the bitmap. If we have N different (small) analysis:es for each contract, it will probably actually be slower.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> JUMPDEST analysis (collecting valid jump destinations) can be performed lazily per subroutine. Optimized EVM implementation may perform advanced code analysis and/or translation beyond collecting JUMPDEST offsets.

It can be done lazily even now. Not until an actual jump is there any need to do the analysis (geth does this, AFAIR). In theory, the analysis could stop after going past the desired jump location, and continue later if needed.

I agree with the other benefits, and the concept in general.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> This restriction can potentially break existing contracts. E.g.

Oh, that’s a bit nasty, nice catch!

---

**gcolvin** (2020-04-29):

This generally seems OK, though I’m very short on time to analyze it.  My general concern with imposing any structural restrictions was to not slide down a slippery slope towards EIP-615. And I did have in mind EVM code as a target for compilers more than the reverse - so my model was more existing CPUs and optimizing compilers.

---

**AlexeyAkhunov** (2020-04-29):

Good effort analysing this!

The most concerning piece that I learnt from this analysis is the cross-subroutine jumps. I think if we do not introduce structural restrictions on the legacy `JUMP`/`JUMPI`, it will be very messy situation. But, as [@gcolvin](/u/gcolvin) noted, introducing these restriction is a “slippery slope” towards EIP-615. I hope it will prompt former opponents of EIP-615 reconsider the hypothesis that spitting it into pieces would make thing simpler.

---

**lialan** (2020-04-29):

Good observations about tail calls.

The tail calls is definitely a benefit to the performance, but I think it is a good-to-have feature for compilers. If the code is compiled by a compiler then it is structured code, and EIP2315 can only guarantee compiler-generated cases. Should compilers optimize tail calls? sure in this case. Will it change the call structure? sure, yes, that is what tail calls intended to do anyway. But users should not feel encouraged to use such technique to circumvent the checks, as compiler generated code is not intended to be read by humans.

---

**lialan** (2020-04-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> This restriction can potentially break existing contracts.

To guarantee safety, it is best to have versioning on contract codes, or checks inside EVM. Should we do that?

---

**axic** (2020-04-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lialan/48/2494_2.png) lialan:

> To guarantee safety, it is best to have versioning on contract codes, or checks inside EVM. Should we do that?

I would much rather analyze the chain first, and if there is no major breaking contract, then announce this decision (so that people deploy vulnerable contracts by their own decisions) and launch it without versioning.

---

**lialan** (2020-04-29):

True. But I think this is more of a one time solution.

But I still think that there will be backward-incompatible add-ons in the future, which will make versioning inevitable. So it is good to start thinking how versioning can be implemented.

edit: forgot to cc: [@axic](/u/axic)

---

**tkstanczak** (2020-04-29):

Great thing [@axic](/u/axic), [@chfast](/u/chfast), [@gumb0](/u/gumb0).

As for the main subrotuine - actually Nethermind has a separation of the top level call and subcalls already. I was planning to refactor that but now it will make me think twice.

As for the jump dest analysis - currently is has barely any performance impact because of caching and single O(1) pass. It may be relevant for stateless clients but agree with Martin that taking into account how simple and optimized current implementations are any additional splitting would probably make it slower.

---

**tkstanczak** (2020-04-29):

I would not introduce the discussion of BEGINDATA into this EIP and maybe discuss it in a separate one? As Greg mentioned - we do not want to go into a scope creep scenario.

---

**axic** (2020-04-29):

There is no suggestion to include the `BEGINDATA` opcode, but as a result of the restrictions, an unreferenced `BEGINSUB` can be used for storing “data”. At least it’s better than the current situation: Solidity inserts `INVALID` to avoid code flowing into the data, but EVMs still need to crunch through it looking for `JUMPDEST`s.

---

**axic** (2020-04-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lialan/48/2494_2.png) lialan:

> True. But I think this is more of a one time solution.
>
>
> But I still think that there will be backward-incompatible add-ons in the future, which will make versioning inevitable. So it is good to start thinking how versioning can be implemented.

Sure, versioning can be useful. There were some concerns that versioning complicates any future repricings, so if it is possible to avoid/postpone it, maybe we should take that option.

---

**holiman** (2020-04-30):

1.2. Every BEGINSUB position starts new subroutine ending the “current” one.

Does this mean that `ENDSUB` is not requried between subroutines? SO that a valid program might be:

```auto
PUSH2 1024
JUMPSUB
BEGINSUB,BEGINSUB,BEGINSUB,BEGINSUB,BEGINSUB,BEGINSUB,BEGINSUB,BEGINSUB....
```

That is, `N` tiny subroutines, up to around 24K of them (on a normal contract, way higher if it’s initcode being executed)?

I think the code above would make a 2-level jumpdest mapping croak. Using a bitmap for jumpdest analysis was the way to save the day, when someone executed a one-megabyte large slice of initcode filled with jumpdests.

With this new propose approach, we’re back at having to either

- Maintain a map[PC]->bitmap of subroutines, or
- Maintain a bitmap of A of “beginsub/or/not”, in addition to the map B of “data/or/code”. Then we could, at JUMP X, first do the regular check of X against B, and afterwards, go to bitmap A and scan backwards (or forwards) all the way from X to current PC, to verify that there are no bits set on the way there (abort early if we hit a bit set: indicating a subroutine boundary).

It sounds like it might be attackable, but maybe there’s some better algorithm. I suspect this comes at a cost, though

---

**chriseth** (2020-04-30):

I like this proposal a lot! I hope the cross-sub-jump analysis can be done efficiently, because I think disallowing “crossing returnsubs” makes testing much easier, as suggested by the authors. Returning from a sub will be a syntactic instead of a semantic action.

One edge case that would have to be covered by a test: Jumping to a beginsub that is directly followed by a beginsub, which could be implemented differently than flowing into a beginsub.

I’m pretty sure the Solidity compiler never generated code that jumped over non-code. Anything that is not code is at the end of the bytecode.

---

**holiman** (2020-04-30):

I think these two things are confusing, taken together:

> Every BEGINSUB position starts new subroutine ending the “current” one.

(this implies, to me, that there’s some form of “implicit returnsub” on a `BEGINSUB`?)

and

> Execution of BEGINSUB causes exception

Your example program:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> 0b BEGINSUB $sub1
> 0c JUMPDEST
> 0d ADD
> 0e JUMPDEST
> 0f BEGINSUB $sub2
> 10 PUSH 1
> 12 ADD
> 13 JUMPDEST
> 14 RETURNSUB

What would happen after `0e`, doesn’t it suddenly walk into a new subroutine and crash?

If there is *not* an implicit returnsub, shouldn’t you put `RETURNSUB` at e.g `0f` in the example?

---

**axic** (2020-04-30):

Update: comment again before reading the entire message ![:man_facepalming:](https://ethereum-magicians.org/images/emoji/twitter/man_facepalming.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> (this implies, to me, that there’s some form of “implicit returnsub” on a BEGINSUB ?)

There is a statement in “Fallthrough to next subroutine”, but I agree the “spec” part of “JUMPs across subroutine” not clear:

> Execution of  BEGINSUB  causes exception (OOG: all gas consumed) and terminates execution.

---

**gcolvin** (2020-05-01):

I’m still worried about making subroutines syntactic.   The intent was pure mechanism at the level of EVM assembly - retaining current control flow operations and adding a Forth-style return stack.  At first I only had JUMPSUBs to any JUMPDST.  It was trying to write some example code that way inspired BEGINSUB - it seemed the minimum necessary structure.

For an interpreter this doesn’t present much trouble, but I can see how  it would cause problems for LLVM and similar tools.  So I’d ask, without time to analyze, for the minimal structure needed for the purpose.

And I suspect extended dup and swap could help.

---

**chfast** (2020-05-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> This is not necessarily true. Geth does a one-pass analysis, and the lookup is O(1) on the bitmap. If we have N different (small) analysis:es for each contract, it will probably actually be slower.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> It can be done lazily even now. Not until an actual jump is there any need to do the analysis (geth does this, AFAIR). In theory, the analysis could stop after going past the desired jump location, and continue later if needed.

Lazy `JUMPDEST` analysis is indeed possible currently and problematic in the same time — it is rather complex to implement and easily defeatable by worst cases. In nature it may help in average workloads so I never was keen to implement it and check it in practice. I regret a bit I mentioned it in this context at all. However, having subroutines strictly partitioning code opens up new (at least theoretical) strategies.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> This restriction can potentially break existing contracts. E.g.

Oh, that’s a bit nasty, nice catch!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lialan/48/2494_2.png) lialan:

> To guarantee safety, it is best to have versioning on contract codes, or checks inside EVM. Should we do that?

Originally I was wrong. We are able to perform static analysis of all EVM code deployed and check if `BEGINSUB` instruction is present there. We actually should extend this and collect information about “usage” of all unassigned opcodes. Should be helpful for some future EIPs.

But in case `BEGINSUB` is present, it would be very difficult to check there exist a possible jump over it.

Requiring code versioning is definitely not something we want to use here.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> My general concern with imposing any structural restrictions was to not slide down a slippery slope towards EIP-615.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> I think if we do not introduce structural restrictions on the legacy JUMP / JUMPI , it will be very messy situation. But, as @gcolvin noted, introducing these restriction is a “slippery slope” towards EIP-615.

I actually was not considering EIP-615 at all. [@gcolvin](/u/gcolvin) proposed the MVP of subroutines what was good decision on its own and also good discussion starting point. We propose two additional “restrictions” which (in our opinions) provide some additional benefits to this feature. But it stays within EVM Look&Feel:

- it is backward compatible with existing contracts (one issue remains here),
- no code version is needed,
- no code validation is needed at deploy time,
- all execution aborts happen only when you execute malformed piece of code.

I think it is good to stay within this boundaries.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> I think the code above would make a 2-level jumpdest mapping croak. Using a bitmap for jumpdest analysis was the way to save the day, when someone executed a one-megabyte large slice of initcode filled with jumpdests.
>
>
> With this new propose approach, we’re back at having to either
>
>
> Maintain a map[PC]->bitmap of subroutines, or
> Maintain a bitmap of A of “beginsub/or/not”, in addition to the map B of “data/or/code”. Then we could, at JUMP X , first do the regular check of X against B , and afterwards, go to bitmap A and scan backwards (or forwards) all the way from X to current PC , to verify that there are no bits set on the way there (abort early if we hit a bit set: indicating a subroutine boundary).
>
>
> It sounds like it might be attackable, but maybe there’s some better algorithm. I suspect this comes at a cost, though

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tkstanczak/48/2667_2.png) tkstanczak:

> As for the jump dest analysis - currently is has barely any performance impact because of caching and single O(1) pass. It may be relevant for stateless clients but agree with Martin that taking into account how simple and optimized current implementations are any additional splitting would probably make it slower.

I must to agree here. How to perform jumpdest/subroutine analysis and how later store this information is problem on its own. And looks it will get much harder with the proposed change. I think we at least need to inspect that further and propose a recommended implementation. I would prefer to discuss that on a side as there is a lot to say about this problem.

Some quick ideas though:

1. You can store the information in a byte array of the size of the code. We need 1 bit for “is it a JUMPDEST”, 1 bit for “is it a BEGINSUB”, and we have 6 bits left to encode (using variadic length encoding) the length of a subroutine. This has 8x larger memory footprint than bitset used in geth.
2. To bound worst cases we can limit the max code size to the 2x the max deplyable code size (this will affect the input size for CREATE, CREATE2 and “create” transactions). EIP-1985 comes to mind.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> I think these two things are confusing, taken together:
>
>
>
> Every BEGINSUB position starts new subroutine ending the “current” one.

(this implies, to me, that there’s some form of “implicit returnsub” on a `BEGINSUB` ?)

and

> Execution of BEGINSUB causes exception

The first sentence is about analysis, not execution. I changed it to:

> Every BEGINSUB opcode position in the code marks the beginning of a new subroutine and the ending of the “previous” subroutine.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> 0b BEGINSUB $sub1
> 0c JUMPDEST
> 0d ADD
> 0e JUMPDEST
> 0f BEGINSUB $sub2
> 10 PUSH 1
> 12 ADD
> 13 JUMPDEST
> 14 RETURNSUB
> What would happen after 0e , doesn’t it suddenly walk into a new subroutine and crash?
> If there is not an implicit returnsub, shouldn’t you put RETURNSUB at e.g 0f in the example?

It would crash only if “no subroutine fallthrough” is applied. But I put the missing `RETURNSUB` in the example not to be distracted by this.

---

**AlexeyAkhunov** (2020-05-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> it is backward compatible with existing contracts (one issue remains here),
> no code version is needed,
> no code validation is needed at deploy time,
> all execution aborts happen only when you execute malformed piece of code.
>
>
> I think it is good to stay within this boundaries.

Yes, when you put it like this, I agree

---

**gcolvin** (2020-05-01):

I really am coming to prefer the approach of subroutines as pure mechanism.  Just new control-flow operators, with no syntax and no changes to any other operators.

[Unlimited SWAP and DUP instructions](https://eips.ethereum.org/EIPS/eip-663) would probably be useful in this programming model.

Can the imposition of further syntax and invariants – for things like validation, merklization, and clean compilation – be handled with custom smart contracts and init code?

---

**holiman** (2020-05-03):

I have an variant of the proposal.

- A subroutine may only start at PCs divisable by 32: 0, 32, 64` etc.
- The BEGINSUB, if executed at some other position, causes error.
- If a BEGINSUB is at PC % 32 == 0, then we say that a new subroutine starts there.

With these changes, the following effects happen:

- We keep the old code/data bitmap. Size codelen / 8. (A)
- We create one more bitmap during jumpdest-analysis. Bit 0 represents PC=0, bit 1 represents PC=32. If a new subroutine starts there, we place a 1 in the bitmap. (B). Size of B is codelen/ 32 /8

Now, whenever we need to check if a `JUMP` is valid, we do

- Check A as before,
- Check LOC is JUMPDEST as before,
- Seek through B from PC to LOC. This seek operation effectively covers 32 bytes per check. On a 64-bit platform, large large jumps can be checked with 64 bits at a time, effectively covering 32*64 bytes of code per check.  A jump across 1MB gigantic subroutine can be performed with ~490 checks.

This means that compilers will have to be smart about allocating the subroutines, and use some padding here and there, and maybe inline small stuff instead of subroutining it.

For code merklization, that might be a good thing too, since it puts a floor on the size of a code chunk.

Furthermore:

- this decreases the chance of causing backward compatibility problems: any non-32 BEGINSUB op is still ‘just an invalid opcode’, and the only case that would cause problems would be

A jump across a data-section, where a BEGINSUB is at PC %32 ==0.

PS: The choice of `32` is pretty arbitrary.


*(37 more replies not shown)*
