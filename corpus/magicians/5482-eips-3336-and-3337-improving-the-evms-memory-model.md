---
source: magicians
topic_id: 5482
title: "EIPs 3336 and 3337: Improving the EVM's memory model"
author: Arachnid
date: "2021-03-06"
category: EIPs
tags: [evm, core-eips]
url: https://ethereum-magicians.org/t/eips-3336-and-3337-improving-the-evms-memory-model/5482
views: 4223
likes: 6
posts_count: 23
---

# EIPs 3336 and 3337: Improving the EVM's memory model

I’ve written up two EIP drafts, [3336](https://github.com/ethereum/EIPs/pull/3336/files) and [3337](https://github.com/ethereum/EIPs/pull/3337/files) that together permit a new efficient way to use EVM memory for storage of ephemeral data such as local variables, function arguments, and return values.

I believe that these changes represent a minimal overhead to implementers while making for a significant improvement for compiler writers and users. In short, if implemented we can say goodbye to “stack too deep” errors in Solidity, by making storing locals etc in memory instead of the EVM stack effective in cost and bytecode size terms.

Your feedback on the idea, and the details in the EIPs, is very much appreciated.

## Replies

**fubuloubu** (2021-03-06):

3337 link points to the wrong PR, it should point here:

https://github.com/ethereum/EIPs/pull/3337

---

**Arachnid** (2021-03-06):

Fixed, thank you.

(Extra nonsense to make discourse happy)

---

**gcolvin** (2021-03-09):

A SWAPFP opcode would be useful.  It would save one or two instructions per subroutine call, depending on whether you get the old FP onto the stack before or after setting up the new frame in memory.

---

**Arachnid** (2021-03-09):

I can see how it would potentially be handy - but I’m not sure it’s worth it to remove a couple of cheap stack manipulation opcodes per function call.

---

**gcolvin** (2021-03-10):

Probably so.  But it helps me the most when it saves two ops and makes intention clear.  This is the calling convention of first creating the new stack frame, leaving the new frame pointer already on the stack, then swapping it with the current frame pointer.  Which takes `GETFP  SWAP  SETFP` instead of just `SWAPFP`.

---

**Arachnid** (2021-03-10):

It occurs to me that if this is the common way to do it, we could just replace SETFP with SWAPFP. I’m not sure I understand how it’d be used, though - can you give an example function call prologue?

---

**gcolvin** (2021-03-10):

For my work right now I’m assuming I’ve constructed a new frame and its address is already on the stack before setting up the call.  So it’s this

```auto
SWAPFP
PUSH jump address
JUMPSUB
```

versus this

```auto
GETFP
SWAP
SETFP
PUSH jump address
JUMPSUB
```

---

**Arachnid** (2021-03-11):

How did you get the address of the new frame on the stack without first calling GETFP?

---

**gcolvin** (2021-03-11):

The new frame?  It never was in FP until after the SWAPFF.  Its address gets left on the stack by whatever code constructs the new frame, then swapped with current FP.

That is, `SWAPFP` is just the same as `GETFP  SWAP  SETFP`, but shorter, sweeter, and cheaper.

---

**Arachnid** (2021-03-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> The new frame? It never was in FP until after the SWAPFF. Its address gets left on the stack by whatever code constructs the new frame, then swapped with current FP.

But how did the code that constructs the new frame determine the new FP? It seems like it would have to already know what the old FP is for that.

---

**gcolvin** (2021-03-11):

No - it just needs to write to new memory relative to the current FP to construct the new frame.  The current FP can then be loaded and used to compute the new FP, but it gets consumed by the ADD.  Still - SWAPFP is a minor convenience, not a necessity.

So this

```auto
PUSH size of current frame
PUSH new frame data
MSTOREFP
... store more frame data
...
GETFP
PUSH size of current frame
ADD
SWAPFP
PUSH jump address
JUMPSUB
```

versus this

```auto
PUSH size of current frame
PUSH new frame data
MSTOREFP
... store more frame data
...
GETFP
PUSH size of current frame
ADD
GETFP
SWAP
SETFP
PUSH jump address
JUMPSUB
```

(Or - less likely - when frames are not allocated as a contiguous array, so the old FP was never needed.)

---

**ekpyron** (2021-03-12):

Just as a first comment: we did actually consider proposing something along these lines coming from the Solidity team as well at some point (actually both EIP 3336 and 3337 independently ;-)), so this is definitely interesting to us in general, although we did not find consensus about which change in this direction with which details would benefit us the most or not, but it’s great to discuss these!

Just for a small clarification in 3337: “An attempt to load data from a negative address should be treated identically to an invalid opcode, consuming all gas and reverting the current execution context.” - do you mean the address given as argument before adding the frame pointer or the sum after adding the frame pointer? I guess negative means 2’s complement negative on the 256-bit word? Anyways does this mean the client needs to do additional verification before the actual memory operation? To me this formulation does not seem entirely clear.

Apart from that, the main thing I’m currently wondering about is whether the gas costs for `MSTOREFP` and `MLOADFP` can reasonably be kept that low - my guess would be that they cannot and it would be interesting what we can realistically expect and especially how much cheaper these could be kept compared to manually adding the frame pointer to an address before a plain `MSTORE` or `MLOAD` (if there is little or no difference in the end, the EIP could be reduced to introducing a single general-purpose register that merely **can** be used as framepointer by convention).

---

**Arachnid** (2021-03-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> No - it just needs to write to new memory relative to the current FP to construct the new frame. The current FP can then be loaded and used to compute the new FP, but it gets consumed by the ADD.

But doesn’t it need to be loaded in order to store the old FP in memory for when the function returns? Or are you anticipating it would be stored on the stack instead?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ekpyron/48/2033_2.png) ekpyron:

> Just for a small clarification in 3337: “An attempt to load data from a negative address should be treated identically to an invalid opcode, consuming all gas and reverting the current execution context.” - do you mean the address given as argument before adding the frame pointer or the sum after adding the frame pointer? I guess negative means 2’s complement negative on the 256-bit word? Anyways does this mean the client needs to do additional verification before the actual memory operation? To me this formulation does not seem entirely clear.

The intent was for this to be a restriction on the sum of FP and the passed in value - since the FP is signed, the sum could be negative. But, it might be simpler just to say that the EVM should treat the result as an unsigned int.

[quote=“ekpyron, post:13, topic:5482”]

Apart from that, the main thing I’m currently wondering about is whether the gas costs for `MSTOREFP` and `MLOADFP` can reasonably be kept that low - my guess would be that they cannot and it would be interesting what we can realistically expect and especially how much cheaper these could be kept compared to manually adding the frame pointer to an address before a plain `MSTORE` or `MLOAD`[/quote]

The vast majority of the cost of the cheap opcodes is dispatch and gas accounting; an additional integer addition should not be enough to require increasing the gas cost of the operation.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ekpyron/48/2033_2.png) ekpyron:

> (if there is little or no difference in the end, the EIP could be reduced to introducing a single general-purpose register that merely can be used as framepointer by convention)

Can you elaborate on how this would work?

---

**gcolvin** (2021-03-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> But doesn’t it need to be loaded in order to store the old FP in memory for when the function returns? Or are you anticipating it would be stored on the stack instead?

I just meant the old FP needn’t be on the stack to create a new stack frame.  From your spec I thought the old FP would be need to be on the stack for the return – but I may have misunderstood.

---

**ekpyron** (2021-03-15):

> The vast majority of the cost of the cheap opcodes is dispatch and gas accounting; an additional integer addition should not be enough to require increasing the gas cost of the operation.

That’s why I was wondering about the exact phrasing of the restriction about the result being negative - last time I brought up something similar to EIP 3336 [@chfast](/u/chfast) mentioned (https://gitter.im/ethereum/solidity-dev?at=5d70d135b3e2fc5793583376) that the main problem in memory design is (besides gas accounting) the required validation, so I guess, if possible, it should be avoided to impose any additional restrictions (although client devs would probably be more qualified to say something about that than me). But just specifying `MLOADFP`/`MSTOREFP` to be equivalent to a regular unsigned addition and a regular `MLOAD`/`MSTORE` should also work, shouldn’t it? Also why exactly is the frame pointer signed and does it actually matter?

> Can you elaborate on how this would work?

Nothing fancy. I just meant that if it turns out that `MLOADFP` cannot be made cheaper than `GETFP ADD` on an offset plus a regular `MLOAD` (and similarly for storing), that *then* there would be little reason to introduce those two opcodes and what remains would be `SETFP` and `GETFP` - so then the frame pointer would just become a general purpose register and not specifically a framepointer. As for a bit more context: we did consider introducing memory frames without any new opcodes in solidity by storing the frame pointer itself in memory, but that requires an additional indirection on accesses, which makes things too expensive - so anything the EVM could provide to cheaply store a value would already help, i.e. even a single register without the special mstore and mload variants.

But yeah, that’s - at least to me - the main question: what would client devs estimate as costs for `MLOADFP` and `MSTOREFP`. If they can be kept cheap, then it’s of course better to have them than not having them.

---

**gcolvin** (2021-03-27):

> … why exactly is the frame pointer signed and does it actually matter?

You can build call stacks from lower addresses up or, traditionally, from higher addresses down.  In the latter case you need negative offsets from the frame pointer.

> … if it turns out that MLOADFP cannot be made cheaper than GETFP ADD on an offset plus a regular MLOAD (and similarly for storing)

The Geth interpreter would use a native 64-bit addition rather than a more expensive 256-bit addition, and the overhead of decoding the ADD would be saved.

---

**Alchemist33** (2021-03-30):

Sounds very interesting

---

**gcolvin** (2021-04-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> But doesn’t it need to be loaded in order to store the old FP in memory for when the function returns? Or are you anticipating it would be stored on the stack instead?

Aha.  Stack.  Sorry if I wasn’t clear.  So at the call site we have something like:

```auto
...              ; create frame, leave new FP on stack
SWAPFP           ; FP is new FP, old FP is now on stack
PUSH jump address
JUMPSUB
SETFP            ; restore old FP from stack
```

And at the return site we have

```auto
...              ; old FP must be on stack
RETURNSUB
```

An alternative convention might be to chain frames together with a link field.  Something like

```auto
...              ; create frame, leave new FP on stack
SWAPFP           ; FP is new FP, old FP is now on stack
PUSH 0
STOREFP          ; old FP is now at start of new frame
PUSH jump address
JUMPSUB
PUSH 0
LOADFP           ; retrieve old FP from current frame
SETFP            ; restore old FP
```

Then at the return site we just `RETURNSUB` with no need to have the old `FP` on the stack.

There are other ways to skin this cat, I haven’t thought through them all.

How to create the new frame is another question.  If the stack frames are growing contiguously in one direction it’s not hard.  In an example above I assumed it was growing towards higher addresses.

---

**gcolvin** (2021-04-01):

[@Arachnid](/u/arachnid) – I’ve scribbled a lot of speculative pseudo-code above.  What might better help this EIP-3337 is examples of how it can help improve on the existing Solidity calling conventions.

---

**gcolvin** (2021-04-02):

[@Arachnid](/u/arachnid) On 3336, I’m skeptical.  First, I think the quadratic cost function for memory means that most memory usage is going to be well within high-level cache – kilobytes, not megabytes – where the relevant boundary is the cache line, not the memory page, and a cache line is typically two EVM words.  So it seems like a lot of complexity and likely performance impact to handle a fairly small amount of memory.

A (not so radical) suggestion:  Allow memory to also grow from the top down.  That is, twos-complement, towards negative offsets.  Keep the same cost function.  Ideal for a stack of frames.  Also, twos complement, the frame stack could be aliased with memory via `MLOAD` and `MSTORE`.


*(2 more replies not shown)*
