---
source: ethresearch
topic_id: 7504
title: Expanding instruction set of Distaff VM
author: bobbinth
date: "2020-06-03"
category: zk-s[nt]arks
tags: [library]
url: https://ethresear.ch/t/expanding-instruction-set-of-distaff-vm/7504
views: 4136
likes: 20
posts_count: 15
---

# Expanding instruction set of Distaff VM

I’ve just released a new version of [Distaff VM](https://github.com/GuildOfWeavers/distaff). In this update I focused on adding many useful instructions - so, now Distaff is almost a fully-functional VM.

The current instruction set is described [here](https://github.com/GuildOfWeavers/distaff#instruction-set) in detail, but here are the highlights:

1. Added hashing operation. This operation computes a single round of Rescue hash function. Executing this operation 10 times in a row is equivalent to computing a full Rescue hash (at ~120-bit security level). You can hash up to four 128-bit elements at a time (or about 512 bits total).
2. Implemented support for secret inputs. A program can now consume an unlimited number of secret inputs. This is done via two input tapes (these are creatively named tape A and tape B). You can push values from both tapes onto the stack with a single instruction. Since each value is an element in a 128-bit field, you can move up to 256 bits onto the stack in a single operation.
3. Added a bunch of stack manipulation operations and a few conditional selection operations. These make it possible to write simple conditional logic. Also, completed the set of arithmetic operations. Specifically, added INV instruction to compute multiplicative inverses (so, now you can do divisions).

Using these new instructions you can write many useful programs. Specifically, writing a program which can anonymously prove membership in a Merkle tree is pretty simple (I have an example of such a program [here](https://github.com/GuildOfWeavers/distaff/blob/a20c3777e570d07eb98f8d6eab891afd21f8cfbd/src/examples/merkle.rs#L40)). This means that Distaff VM can be now be used to support Semaphore-like protocols (as well as many other things).

### Impact on performance

As expected, adding new instructions to the VM slowed down proving time. But the impact was not as significant as I expected. Overall, proving time increased by about 25%. However, the performance is still pretty impressive. For example, the VM can generate proofs for computing over 200 Rescue hashes / sec (on a single core).

Below are some rough benchmarks for running a program which verifies Merkle proofs for trees of various depths (run on Intel Core i5-7300U @ 2.60GHz, single thread):

| Tree depth | Operation count | Execution Time | Verification time | Proof size |
| --- | --- | --- | --- | --- |
| 16 | 29 | 180 ms | 2 ms | 73 KB |
| 32 | 210 | 300 ms | 2 ms | 85 KB |
| 64 | 211 | 600 ms | 3 ms | 95 K B |

These proofs were done at 120-bit security level and optimized for proving time. But, if you are willing to accept 100-bit security level and spend a bit more time on proof generation, proof sizes can be reduced quite a bit. For example, for a tree of depth 32, if we increase proving time to ~1 second, the proof size can be reduced to under 50 KB.

### What is missing

There are a few important things that are still missing from Distaff VM:

1. Equality and comparison instructions (less than, greater than etc.). I have a pretty good idea of how to implement these. Equality is easy and can be done in a single operation. Comparison is pretty easy as well, although it will require many operations. So, value comparisons will be one of the most expensive operations on the VM.
2. Random access memory. I have a pretty good idea of how to do this as well - though it will probably slow down the rest of the VM by 20% - 25%.
3. Ability to produce large number of outputs (currently, number of outputs is limited to 8). Not sure about the bet way to do this yet.

If you can think of anything else that could be added to the VM to make it more useful - let me know. I’m always looking for feedback and suggestions.

## Replies

**bobbinth** (2020-06-09):

I’ve just released a minor update to the VM. This update has new instructions which enable value comparisons. Specifically:

- EQ instruction can be used to check if two values are equal.
- CMP instruction can be used to check if one value is greater than or less than another value.
- BINACC instruction can be used to check if a value can be encoded with a given number of bits.

I have a detailed description of how value comparisons work in the VM [here](https://github.com/GuildOfWeavers/distaff#value-comparison-in-distaff-vm), but in the nutshell:

- EQ instruction is simple - it takes just one VM cycle to check value equality.
- CMP and BINACC instructions are more complex, and you need to use them in “mini-programs” to check inequality or binary decomposition.

The length of these mini-programs depends on the size of the values to be checked. For example, checking inequality between two unconstrained field elements takes about 145 cycles. But if you know that both values are at most 32 bits, it would take about 45 cycles to figure out whether one value is bigger or smaller than the other.

For comparison, hashing values takes just 10 cycles. This makes value comparisons the most expensive operations in the VM. Fortunately, the effect of these new instructions on the rest of VM is negligible. You pay the price only if you use these instructions.

To illustrate how these new instructions can be used, I’ve put together a simple [program](https://github.com/GuildOfWeavers/distaff/blob/3fcde498ee27de6ff517fcf574f91518e220c80b/src/examples/range.rs) which consumes a list of secret inputs and counts how many of these inputs can be encoded in 63 bits. When executed on Intel Core i5-7300U @ 2.60GHz (single thread), performance looks like so:

| Range-checks | Operation count | Execution time | Proof size |
| --- | --- | --- | --- |
| 10 | 210 | 300 ms | 81 KB |
| 100 | 213 | 2 sec | 118 KB |
| 900 | 216 | 16 sec | 159 KB |

This is just one example, and more sophisticated programs can be constructed with these instructions to accomplish many useful tasks. For example, summing up leaves of a Merkle tree in zero-knowledge while ensuring that there are no overflows or underflows.

Also in this release, I’ve added `ASSERT` instruction. This instruction fails if the top of the stack is not `1`. It can be used even now to make writing programs with conditional logic simpler. But in the future release it will enable more sophisticated programs with complex branching.

---

**xz-cn** (2020-06-19):

Awesome work!! Love to check it out. Can you give us some typical use cases for this VM? Thank you!

---

**bobbinth** (2020-06-19):

Thank you! Being a nearly general-purpose VM, the number of potential use-cases is huge, but here is how I think about it:

In general we can think of 2 different types of use cases: (1) when programs are public, and (2) when programs are private. You can also have a hybrid when parts of a program are public and other parts are private, but I’d lump these together with private programs.

For **public programs**, I can think of the following broad categories of use cases:

First, The VM could be a part of a larger protocol where someone executes a known program against their secret inputs to prove that they know something or that their secret inputs comply with some requirements. For example, you can have programs which:

1. Anonymously prove membership in Merkle tree;
2. Prove that a sum of leaves of a Merkle tree is equal to (or greater than, or less then) than some publicly known value;
3. Prove that some set of values is within a given range.

A few concrete examples:

1. Let’s say I have committed to 2 Merkle trees: one contains all my assets, and the other one contains all my liabilities. Using the VM, I can prove that the sum of my assets is greater than the sum of my liabilities by at least x, without revealing anything else about my assets or my liabilities.
2. Let’s say I have a commitment to my personal information which includes my date of birth. Using the VM, I can prove that I’m older than x but younger than y, without revealing my age.
3. Let’s say there a Merkle tree which commits to a set of people who can vote on some issue. Using the VM, I can anonymously prove that I’m in the set and cast a unique vote which cannot be linked to my identity.

I think all of these can be accomplished using other techniques, but the advantage of using the VM is that you can mix and match these (and many other) use cases, and you don’t really need to know anything about how ZK proofs work to do that.

Going beyond these, the VM could be a foundation for an L2 scaling solution. For example, your programs could be programs that describe state transitions for accounts on the blockchain, and you could aggregate these programs and run them all on the VM to generate a single succinct proof of all transitions.

For **private programs**, I think the primary use case would be privacy-preserving smart contracts. This is basically when only a small group of users knows the actual code behind a contract. Any one of them can execute the contract locally, and then submit the proof of execution to the blockchain. The blockchain can verify that the contract was executed correctly, and update its state accordingly. But what exactly was executed or what the new state is, would not be publicly known.

I do want to say that the VM is still very early in its development, and not everything described above is currently practical. For example, because proof sizes are in dozens of KB, privacy-preserving smart contracts are not going to be practical until there is a way to efficiently aggregate many proofs into a single succinct proof.

---

**bobbinth** (2020-06-22):

I’ve just released the next update of Distaff VM (v0.4). The biggest improvement in this update is the [Distaff Assembly](https://github.com/GuildOfWeavers/distaff/blob/a33fb4c56af2b3fb4fc91117a5b3de74e484b000/docs/assembly.md) language  which makes writing programs for the VM much much simpler. Some benefits of Distaff assembly are:

1. Simple, text-based representation.
2. Many new useful instructions. For example, there are now instruction for less than, greater than, and hash operations. You can also now compute a root of a Merkle path with a single instruction.
3. The language supports conditional execution natively. That is, you can now use normal if/else statements.

The last point is pretty significant. Up until now, conditional branches were very difficult to do in the VM. But now, you can write a program like this:

```auto
read
read
dup.2
gt.128
if.true
  add
else
  mul
endif
rc.64
```

The above program does the following:

1. Reads 2 values from the secret inputs tape
2. If the second values is greater than the first, adds them; otherwise multiplies them.
3. If the result of the previous operation is less than 2^{64}, outputs 1; otherwise, outputs 0.

The way branching is handled is described in some detail [here](https://github.com/GuildOfWeavers/distaff/blob/a33fb4c56af2b3fb4fc91117a5b3de74e484b000/docs/assembly.md#iftrue-else-endif-expression) and [here](https://github.com/GuildOfWeavers/distaff/tree/master/docs#program-hash). It is largely based on the MAST approach I described in the very [first post](https://ethresear.ch/t/a-sketch-for-a-stark-based-vm/7048) about Distaff VM. It has some limitations, which I hope to eliminate in the future.

Overall, there are only 2 limitations left which separate Distaff from a general-purpose VM:

1. There is still no RAM - though, I have a pretty good idea of how to implement it. This will also enable unlimited number of public inputs and outputs.
2. The VM is not Turing-complete - i.e. there are no loops, and there are limits to conditional logic. This would be a bit tougher to address - but I think it is possible to get very close to Turing-completeness (including support for un-bounded loops).

---

**gakonst** (2020-06-22):

This is great, thank you for the work on this.

Do you have any ideas (beyond the ones described in the original post) about future constraints optimizations when branching, to avoid exponential blowup of the program size on each if/else?

---

**bobbinth** (2020-06-22):

Thank you!

Exponential blowup around branching is actually not too difficult to avoid. I know of at least 2 potential ways to do that - though, each comes with its own pluses and minuses. Loops are much more tricky. So, at this point I’m trying to pick a methodology which would allow me to do both: (1) remove limitations around conditional branching, and (2) implement flexible looping structures.

---

**xz-cn** (2020-06-24):

Nice to see more interesting staff coming ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=14)

I guess later we are gonna need a compiler to compile regular programs e.g. in Python/Javascript into the VM assembly!

---

**AlexeyAkhunov** (2020-07-02):

Great and inspiring work, thank you!

I am trying to understand how `CMP` works. In the documentation it says that it removes 7 items from the stack, performs binary comparison and puts 7 results on the stack. There is an explanation, but I do not quite follow, because it also uses the concept of input tapes, and I do not see where the tapes are coming into play. And why 7?

---

**bobbinth** (2020-07-02):

Thank you!

First, as an aside, `CMP` is a low-level instruction and it is one of the most complex instructions in the VM. You probably won’t ever have to use it directly as there are [higher-level instructions](https://github.com/GuildOfWeavers/distaff/blob/592d82308e84a2987185cbb6e429bcc5ce229174/docs/assembly.md#comparison-instructions) which use `CMP`  internally to fulfill common use cases (i.e. greater-than and less-than comparisons).

But to explain how it works: at the high-level, to compare two numbers, we do the following:

1. Take their binary representation,
2. Starting with high-order bits, we compare these binary representations bit by bit,
3. As soon as we find a bit in one value which is greater than the corresponding bit of another value, we mark that value as the greater value.

`CMP` instruction performs this single bit comparison and also takes care of some other bookkeeping to enforce all necessary constraints. So, we need to invoke it as many times as there are bits in the values we want to compare. For example, if we want to compare two field elements, we need to invoke it 128 times (since all values in the VM are in a 128-bit prime field).

It might be simplest to understand all the mechanics on a concrete example. Let’s say we want to compare values 3 and 5, and let’s, for simplicity, represent each value using 5 bits: `00011` for 3, and `00101` for 5. To perform the comparision, we’ll need to arrange top 10 values of the stack in a special way, and then execute `CMP` operation 5 times. If we do that, here’s how the execution trace of the top 10 stack registers will look like:

| Step | s0 | s1 | s2 | s3 | s4 | s5 | s6 | s7 | s8 | s9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 5 |
| 1 | 8 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 3 | 5 |
| 2 | 4 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 3 | 5 |
| 3 | 2 | 0 | 1 | 1 | 0 | 1 | 4 | 0 | 3 | 5 |
| 4 | 1 | 1 | 0 | 0 | 0 | 1 | 4 | 2 | 3 | 5 |
| 5 | 1/2 | 1 | 1 | 0 | 0 | 1 | 5 | 3 | 3 | 5 |

To explain what’s going on here:

1. s_0 ... s_9 are the registers of the stack with s_0 being the top of the stack
2. Step 0 is just the initial state of the computation. Before we start executing CMP instructions, we need to position values on the stack as shown in the first row. That is, top of the stack should be set to 2^{n-1} (in our case n = 5). Then we should have 7 zeros. And finally, at the bottom of the stack, we should put the values we want to compare.
3. After the stack has been arranged as described above, we execute CMP instruction 5 times. The instruction affects the top 8 stack slots. So, in effect, you could say that it pops 8 values from the stack, does some computations with them, and pushes 8 values back onto the stack (in the docs I say 7 because one register is currently “hidden” in the VM). Each execution of CMP instruction does the following:
a. Divides the value in s_0 by 2. For step 5, I put 1/2 because 1/2 in a 128-bit field is a large number, and I didn’t want to bloat the table.
b. Reads the next bit of each value we are comparing into s_1 and s_2. This is where the tapes come in: binary representations of 3 and 5 are provided via secret inputs, and each execution of CMP instruction reads values from the input tapes and moves them into registers s_1 and s_2.
c. Register s_3 contains a flag which flips from 1 to 0 as soon as we know what the result of comparison is.
d. Registers s_4 and s_5 contain the result of the comparison. If by the time we execute all 5 CMP instructions, s_4 = 1, then the first value is greater than the second. If s_5 = 1, then the first value is less than the second. In our case, s_5 = 1 at step 5, which means that indeed 3 < 5.
e. Registers s_6 and s_7 contain accumulated values of the binary representation read so far. Specifically: s_{6,n + 1} = s_{6,n} + s_{0,n} \cdot s_{2,n+1} and s_{7,n + 1} = s_{7,n} + s_{0,n} \cdot s_{1,n+1}
4. After we execute CMP instruction 5 times, the state of the stack will be as shown in the step 5 of the table - but we are not done yet. We can discard top 4 values of the stack (they are no longer needed) and we need to make sure that s_6 = s_9 and s_7 = s_8 (otherwise, the values read from the input tapes could have been different from the values we are trying to compare). Once this is done, we are left with the results in registers s_4 and s_5 and can use them in further computations.

I know this is a lot of complexity - so, if anything is unclear, will be happy to provide more info.

And to say it again: complexity of the above process is one of the reasons for creating higher-level assembly instructions which abstract all of this complexity away. So, regular users of the VM would never need to use `CMP` instruction directly.

One other note: semantics of `CMP` instruction may change in the future (there might be more efficient ways to implement it) but the semantics of the higher-level assembly instructions will remain the same.

---

**AlexeyAkhunov** (2020-07-02):

Thank you for very detailed explanation. I did expect that level of complexity. In fact, I came to look at Distaff VM precisely because I was curious about how you implemented comparisons. Was just walking and thinking today about proofs of correct modifications of various data structures, and course, almost immediately came “face to face” with the problem of comparisons. It occurred to me that it would be far from trivial with the finite field arithmetics. I thought about looking at tinyRAM inside the libStark code, but then I remember about your Distaff VM, and this is where a looked.

---

**AlexeyAkhunov** (2020-07-03):

I also wonder whether there is a total order on the field elements that is cheaper to verify than “less than” and “greater than”, but can be used for the purpose of sorting and searching?

---

**AlexeyAkhunov** (2020-07-03):

Unless we start constructing sort and searching around cyclic groups and not around totally ordered sets ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

---

**bobbinth** (2020-07-03):

Without having thought too much about it, it seems like it would be difficult to order elements of a finite field without doing some sort of binary decomposition. But there might be more clever ways of doing decompositions which could be more efficient.

---

**AlexeyAkhunov** (2020-07-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/bobbinth/48/2389_2.png) bobbinth:

> Without having thought too much about it, it seems like it would be difficult to order elements of a finite field without doing some sort of binary decomposition

Thank you! I have realised that I have been trying to answer the wrong question ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) I will need to start researching completely different data structures that are based on cyclic groups rather than on the totally ordered sets. This can lead us somewhere interesting

