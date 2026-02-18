---
source: magicians
topic_id: 2219
title: "Article: The EVM Is Fundamentally Unsafe"
author: lrettig
date: "2018-12-15"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/article-the-evm-is-fundamentally-unsafe/2219
views: 4068
likes: 15
posts_count: 22
---

# Article: The EVM Is Fundamentally Unsafe

Emily Pillmore, an engineer at Kadena, just published [this article](https://medium.com/kadena-io/the-evm-is-fundamentally-unsafe-ba486cb17f1f) about the differences between EVM/Solidity and Kadena’s VM/its interpreted smart contract language, Pact, which makes some very different design decisions than ours. I’ll leave deeper technical analysis to the experts and folks such as [@gregc](/u/gregc)/[@gcolvin](/u/gcolvin) who know far more about VM design than I, but a few high-level thoughts:

- Many of the issues highlighted in the article are in the process of being fixed. E.g., to a large extent, I believe “dispatch” and lack of native-multisig support are addressed by CREATE2 and account abstraction, and the lack of a trusted “standard library” and ability to inline libraries will be addressed by Ewasm.
- Kadena has taken a fundamentally different design direction with Pact than we have with EVM/Solidity, exemplified by the question of Turing-completeness. The Ethereum ethos seems to be, “we make everything possible, so the onus is on the smart contract developer to write safe code,” whereas the ethos with Pact seems to be, “we make the most dangerous things impossible in the first place.” This inspired my Disney World vs. Burning Man analogy. Obviously, there is no single right or wrong choice here: a different set of considerations has led to a different set of design decisions. I think we’d both gain a lot by having more dialog on this topic!
- Among Ewasm, shards, and sidechains, I wonder if it wouldn’t be possible to have different state execution environments in “greater Ethereum” that allow developers to opt into one or the other mindset, for different applications with different sets of security considerations.

## Replies

**gcolvin** (2018-12-15):

Thanks for the pointer, Lane.  She is of course right that there is a lot not to like about the EVM.  Still…

There was some other project with a non-Turing complete functional VM I saw, but not this one.  And of course if you give up Turing-completeness you make many programs, and problems, difficult to code.  Not impossible–you just have to use multiple contracts to pull it off.

I have no idea why she thinks interpreters can be as fast as compilers, pointing at SQL and Javascript.  Oracle’s SQL has been compiled for nearly 20 years now in order to get better performance, and eWasm grew out of compiled Javascript.  And human-readable bytecode?  It already needs to balance compact encoding, efficient decoding, and rapid execution.

Precompiles amount to a small standard library of crypto routines, and already are a burden on client development.  The JVM’s library was big from the start, providing support for an internet-enabled, multi-threaded, object-oriented, garbage-collected, dynamic programming environment with a full Posix file system and many other Posix system calls.  This is not what I would want for the blockchain.  I want libraries of code on the blockchain itself.

But her idea of a “proper” VM is close to the JVM, and mine is only a layer or so more abstract than eWasm.  And neither EVM, eWasm, or Pact is the VM I would design for a blockchain, but it’s too late now.  There’s an old saying in Texas politics, “Ya dance with the one that brought ya.”

---

**lrettig** (2018-12-15):

> if you give up Turing-completeness you make many programs, and problems, difficult to code. Not impossible–you just have to use multiple contracts to pull it off.

I’d be very curious to see an example or two if any are front of mind! This would help me better understand the tradeoff.

> neither EVM, eWasm, or Pact is the VM I would design for a blockchain, but it’s too late now

Out of curiosity, what would it look like? What are the main, high-level differences?

Thanks Greg!

---

**gcolvin** (2018-12-15):

If you don’t have loops you can’t have programs that don’t terminate.

I’d like something similar to eWasm, so far as being just machine operations, not a whole environment, but more abstract.  For instance, only vector operations, and those up to indefinite powers of two.  So close to the SIMD hardware and CPU registers at small powers, but limited by gas rather than arbitrary machine boundaries at large powers.

---

**lrettig** (2018-12-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> If you don’t have loops you can’t have programs that don’t terminate

Even without loops in the VM, to some degree you could still emulate this behavior at the language level, in the compiler, by unrolling loops, couldn’t you?

---

**AlexeyAkhunov** (2018-12-15):

The article might have some good point, but it reads as quite biased and unstructured. Why does she need to repeat “EVM does not have dispatch” so many times, without even once explaining that she actually means by “dispatch”. I assume by lack of dispatch she means that there is a single entry point into a contract, and the functions are simply an abstraction that exist on the level higher than EVM. In this way, EVM contracts are like executables in Unix - when you call them, you specify the input via command line and stdin. Contrast it will shared libraries, which come with host of advantages (referencing objects by name), but also with issues to resolve (name mangling to avoid collision, namespaces, dependency hell, etc.).

I do not believe that EVM creators did not know about dispatch and other things, they chose not to implement these features in order to ship within the time the budget would have allowed it.

---

**mcdee** (2018-12-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Even without loops in the VM, to some degree you could still emulate this behavior at the language level, in the compiler, by unrolling loops, couldn’t you?

Not if you don’t know the number of iterations in the loop, for example if you are looping over an array where the number of items in the array are unknown before runtime.

---

**lrettig** (2018-12-15):

Thanks, this makes sense. Dynamic loops, dynamic jumps. Got it. Are there other big examples of things you cannot do without Turing-completeness?

---

**virgil** (2018-12-16):

I didn’t pay a lot of attention in computing theory class but I recall that you’re also limited in recursion based on conditions.  I think it’s isomorphic to the loop constraint.

If it helps, I think the current philosophy on this issue is to always have Completeness at the base layer and if you want to prove fancy safety properties you will do that at a turing-incomplete high-level language before compiling to eWASM.

---

**gcolvin** (2018-12-17):

You handle loops by unrolling them to the maximum number of iterations required, then running only as much of the unrolled code as needed.  So instead of

```auto
max = 5;
if (n > max)
   revert();
while (i < n)
   f(i);
```

you do the obviously cleaner and safer

```auto
switch(i) {
case (4):
   f(i)
case (3):
   f(i)
case (2):
   f(i)
case (1):
   f(i)
case (0):
   f(i)
   break;
default:
   revert();
}
```

(Uncompiled C code off the  top of my head, pre-coffee.)

You convert recursion to iteration with an explicit stack, and unroll the iteration.  I’m not awake enough to write the code.  So I think all you actually need is some sort of conditional branch to emulate a limited one-tape Turing machine.

I’ve made [these](https://medium.com/@gregcolvin/there-is-a-lot-not-to-like-about-the-evm-some-of-which-im-working-to-fix-but-i-mostly-don-t-1ca43a31e235)  [comments](https://medium.com/@gregcolvin/ps-i-dont-know-what-to-make-of-the-argument-that-a-compiled-language-will-be-more-performant-ccb4f16c72) on the original.

---

**expede** (2018-12-17):

> you make many programs, and problems, difficult to code.

I actually disagree. It depends on how restricted of a Turing subset you’re using, but I assume here only limiting to an execution environment that guarantees totality. This is highly desirable with smart contracts anyway.

From the denotational side, many kinds of loops are total (ie: convergence doesn’t require Turing completion). to use more functional language maps, folds, and filters all fit into this paradigm. Further, we could get accurate gas measurements before actually running the program, they’re much much easier to test, write proofs for, and so on. Because Turing-complete languages encompass all incomplete ones, we can restrict ourselves within languages that we already use. In fact, I’d bet that a very high percentage of production Ethereum smart contracts are either already in this subset (because of the weaker guarantee / incentive from the gas limit), or could be improved by restriction to this subset.

I *STRONGLY* agree with the authors of Pact; if I had to design a smart contract execution environment, I would absolutely restrict it to a total subset with strong semantics. I’ve put a fair amount of thought into this previously. I realize that this is the opposite of Greg’s view (*Hi Greg* ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=12)![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)), and am *more than happy* to discuss the reasons for this (at length… as a PLT geek, this is one of my favourite topics to rant about ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=12))

Aside: At a previous company, I wrote a declarative DSL (constraint solver, &c) for financial smart contracts that had a bunch of these guarantees. Totality, static gas analysis, highly optimizable, easily composition / reuse, and correct-by-construction. Turing completion is great in general, but not the be-all-and-end-all.

> you could still emulate this behavior at the language level, in the compiler, by unrolling loops, couldn’t you?

Yup! But you don’t even need to unroll the loop, per se. Just need a richer grammar for the VM, and most programs will compile to that target normally, only rejecting divergent programs at compile time (via syntactic analysis).

---

**expede** (2018-12-17):

I had someone ping me asking what “convergence” is. The short answer is loopor recursion that are limited to a finite number of steps / will actually return an answer. Of course this is unsolvable *in general* (Halting Problem), but we can solve it for known subsets, both with language constructs or by analyzing a program syntactically (ex. looking at the AST for known forms).

```auto
// Divergent
while (true) { ... } // No way to end the loop (without an explicit `break`)
const diverge = f => f(f(f), f(f)); // Calls itself forever
const backForth = (x) => backForth(x % 2 === 0 ? x + 1 : x - 1); // Never reduces problem size

// Convergent
finiteList.map(x => x + 1); // Limited by number of elements in the finite list
for (x = 0 ; x  {
  if ( n === 1 ) {
    return 1; // Base case
  } else {
    return n * factorial( n - 1 ); // Next step operates on the smaller problem `n - 1`
  }
}
```

---

**charles-cooper** (2018-12-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/expede/48/4738_2.png) expede:

> I STRONGLY agree with the authors of Pact; if I had to design a smart contract execution environment, I would absolutely restrict it to a total subset with strong semantics. I’ve put a fair amount of thought into this previously. I realize that this is the opposite of Greg’s view ( Hi Greg ), and am more than happy to discuss the reasons for this (at length… as a PLT geek, this is one of my favourite topics to rant about )
>
>
> Aside: At a previous company, I wrote a declarative DSL (constraint solver, &c) for financial smart contracts that had a bunch of these guarantees. Totality, static gas analysis, highly optimizable, easily composition / reuse, and correct-by-construction. Turing completion is great in general, but not the be-all-and-end-all.

Sounds interesting! Care to expand? ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**gcolvin** (2018-12-18):

So far as designing *safe languages* I mostly agree, [@expede](/u/expede).  For *virtual machines*, not so much.  I want VMs to be an easily-implemented abstraction of typical real machines, and leave decisions about what kinds of languages to implement on them to others.   (My example was more tongue-in-cheek than it might have appeared, and checking the [docs](https://pact-language.readthedocs.io/en/latest/pact-reference.html#control-flow) I see that Pact eventually relented and put those [harmful](https://pact-language.readthedocs.io/en/latest/pact-reference.html#if-considered-harmful) conditionals in.)

---

**Arachnid** (2018-12-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/expede/48/4738_2.png) expede:

> Further, we could get accurate gas measurements before actually running the program

I really don’t see this as a compelling reason: We can do gas estimation in reasonable time right now just by running the code. It’s possible to write a program that is difficult  to estimate, but we’re not in an adversarial environment where we have to get accurate estimates for uncooperative programs.

---

**AlexeyAkhunov** (2018-12-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> I really don’t see this as a compelling reason: We can do gas estimation in reasonable time right now just by running the code. It’s possible to write a program that is difficult to estimate, but we’re not in an adversarial environment where we have to get accurate estimates for uncooperative programs.

I suspect it is compelling if you are trying to compile the code to binary and do not want to inject metering (with “if (gas > gaslimit) then throw OutOfGasException” all over the place), and just estimate it, for performance reasons (in context of eWASM research, for example)

---

**Arachnid** (2018-12-18):

Fair enough, but even most turing subsets would require dynamic gas costing, unless you just want to always charge users the maximum.

---

**samlavery** (2018-12-18):

This is pure marketing nonsense. I’m angry at the clickbait title, and couldn’t finish the article after the 4th totally absurd claim presented.  It’s not breaking news that bitcoin transactions are less complex, since bitcoin only does one thing(sends bitcoins).  If bitcoin does 1 thing, pact does 2 things, the evm does both and more, when do I care about the first two?

---

**trustfarm-dev** (2018-12-20):

[gist.github.com](https://gist.github.com/trustfarm-dev/cbbc9aa1ab76983cb7dbaa329097c1c3)




####

##### (ENG) Ethereum-gas-fee-autochange.txt

```
(ENG) Ethereum-gas-fee-autochange.txt

Ethereum Contract GasFee Autochange Idea. review on recent DDOS attacks.

From the beginning ethereum has object to be a world computer and smart contract coin platform.
Recent days of DDOS attacks, ETHEREUM normal node (geth , parity) has over consumed 16GB of Runtime memory and sometimes stuck over 10s minutes, or finally, Out of Memory error occurs and down.

It's not suitable for lite IoT systems, it needs less consume of run-time memory, not by sw footprint.
If operate nodes, that's possible to lite client which connect remote full nodes.
```

This file has been truncated. [show original](https://gist.github.com/trustfarm-dev/cbbc9aa1ab76983cb7dbaa329097c1c3)

##### (KOR) Ethereum-gas-fee-자동변경.txt

```
Gas비 자동변경에 대한 아이디어.

애시 당초 ETHEREUM 을 보면, computer 와 smart contract 이 동작할수있는 코인 플랫폼이었다.

최근 DDOS 를 보았을때, ETHEREUM 노드가 잡아먹는 런타임 메모리가 16GB 가 넘어가고, 노드가 몇 10분을 헤메다, 뻣거나 이렇게 되었다.

lite 한 IoT 시스템에 올리기에는 소프트 사이즈가 문제가 아닌, 런타임 메모리 사용때문에 현실적으로 불가한 상황이다.

굳이 한다고 해도, 원격지 서버 노드에 접속해서 클라이언트 기능만 넣을수있지, Full node 는 힘든 상황이다.

```

This file has been truncated. [show original](https://gist.github.com/trustfarm-dev/cbbc9aa1ab76983cb7dbaa329097c1c3)








Gas fee autochange idea will help for solve current EVM Gas problem.

And,

[@gcolvin](/u/gcolvin) [@lrettig](/u/lrettig)

I think script language is good solution for a verifying the contract source.

But, in view of normal people, even though script is opened, but Can’t verify and can’t understand well.

And, More large computation resources, for executing contract. it is not much better than current EVM bytecode.

So, I am researching, source code contained binary

1. at least bytecode itself can be verified by given sourcecode.
2. make compiler also indicated in bytecode.
3. for strong performance and adaption on lite IoT devices, use real cpu architecture based bytecode (e.g RISC-V or OpenRisc)

---

**lrettig** (2018-12-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/trustfarm-dev/48/1320_2.png) trustfarm-dev:

> for strong performance and adaption on lite IoT devices, use real cpu architecture based bytecode (e.g RISC-V or OpenRisc)

This is precisely what Wasm (WebAssembly) is [designed for](https://github.com/WebAssembly/design/blob/master/HighLevelGoals.md). I did see another project recently that was building a (deterministic?) virtual machine based on RISC-V but the name slips my mind.

---

**trustfarm-dev** (2018-12-20):

Webassembly also very heavy, because it runs on top of browser stack (eg. webkit).

And it’s resemble low level instructions. But is run on high level sw abstacted layers.

Just looks like low level, but it’s on top of very high level abstacted sw layers.

And it is scripts.

My project idea is here. https://forum.tao.foundation/topic/23/tao-architecture-conference-presentation

PPT files direct download link is here.

[Tao tokenizeit ppt](https://trustcoinmining.com/bbs/download.php?bo_table=notice&wr_id=19&no=0&sst=wr_datetime&sod=desc&sop=and&page=299260)

[![Screenshot_20181221-003729](https://ethereum-magicians.org/uploads/default/optimized/2X/d/de3f654353b85e4fcc3079d2e15cab09ff79f073_2_281x500.png)Screenshot_20181221-0037291080×1920 300 KB](https://ethereum-magicians.org/uploads/default/de3f654353b85e4fcc3079d2e15cab09ff79f073)

[![Screenshot_20181221-003746](https://ethereum-magicians.org/uploads/default/optimized/2X/4/41d3492845b2c363d9ad060a54ccd42a68a4b33a_2_281x500.png)Screenshot_20181221-0037461080×1920 328 KB](https://ethereum-magicians.org/uploads/default/41d3492845b2c363d9ad060a54ccd42a68a4b33a)


*(1 more replies not shown)*
