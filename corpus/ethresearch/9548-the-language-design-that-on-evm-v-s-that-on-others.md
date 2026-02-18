---
source: ethresearch
topic_id: 9548
title: The language design, that on EVM v.s. that on Others
author: ghasshee
date: "2021-05-18"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/the-language-design-that-on-evm-v-s-that-on-others/9548
views: 6797
likes: 7
posts_count: 26
---

# The language design, that on EVM v.s. that on Others

I am analyzing a compiler which was called Bamboo Compiler.

For me, the design was something unreadable and it was an incomplete model as an escrow language.

Now, I clean up and aliasing the former work and I put it on my github as `pen` compiler project.



      [github.com](https://github.com/ghasshee/pen)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/5/8/58df6a9b07a7bd08186365e00488e471a0ddae7e_2_690x344.png)



###



A compiler into EVM code










## Loops and Program Graph

Bamboo does not have loops in the language design, claiming that we do not need loops because we have gas limit in the execution.

I think this is not the word of those who create a User Friendly Language.

The dijkstra’s Guarded Command Language(GCL) is a way of defining formal method and solving this kind of problems. GCL is translated into Program Graphs easily.

It is compiler that transform loops into a safe finite sequences of opcodes.

This might allow us to use `loops` in the language design.

## Functional OOP

Unlike Bamboo, I would like the approach of Functional OOP language design which is developped by B.C. Pierce and so on around 90’s, which is the original model of Objective Caml.

I heard that Bamboo cannot fill the gap between escrow language which @pirapira pursued and the EVM design which is quite similar to OOP design.

I would like to see and borrow ideas from a lot of projects now going , e.g. michelson in Tezos.

I found Bamboo compiler lacks some of EVM opcodes like `CALLCODE` which I believe caused the parity bug. I do not know now, how to avoid this operation called from some sender, and in the design of Functional OOP. The first thing is to do the whole design of FOOP on EVM roughly.

## Stack Verification

Recently, a team on tezos language developped a formal way to anlayze the language in order to grasp if  the language terminates as intended.

This is done by applying Refinement Type to the Stack. Refinement Type can have a “predicate” on every Type. We can have every subset of every type as a set with applying the predicate.

Thus, type checking on the type of stack contents is exactly formal vericafition of the program.

( However, this type checking sometimes does not terminate if it has second-order logic. )

The implementation depends on SMT solver for the computation of the logical part.

I would like to try this on EVM.

## TODO

- make Guarded Command Langauge for EVM
- define Functional OOP
- add stack verification

I would like to know much more about language designs.

If anyone know about them or interested in them, feel free to let me know !

## Replies

**ghasshee** (2021-06-06):

There are bunches of unneeded definitions / corrupted designing in Bamboo

- Interface Types do nothing / have no meanings in Bamboo.
- Multiple Returning do nothing in Bamboo…
- Void Type and Empty List has the same Role in Bamboo.
- Bamboo’s case is not case pattern match.
- Sentence was Just a Statement
- append_label has a different role from appending labels
- duplication of functions which does the totally same role
- Bamboo has two different names for functions, cases and functions.
- The term interface has multiple meanings in Bamboo Compiler

The design of Bamboo seems fully unreadable and full of useless designs.

An ordinal type theorist would not write codes in such a way.

Pen is going to be a much simplified and sophisticated version.

And let’s try to make typed functional programming languages on evm.

---

**ghasshee** (2021-06-08):

The Bamboo Compiler turned out to be a useless compiler in terms of formal verification.

The guard code 'reentrance` in Bamboo does nothing in creating contracts.

Unlike, type checking in a single computer which has a single user, EVM has bunches of users who use the function. Thus outside checking process does not guarantee the safety. Rather, we must have the guard condition inside the contracts.

I have remembered someone pointed out the uselessness.

It’s just a compiler.

There is no formality on it.

Thus, that means pen also has no formalities in terms of contract safety checking.

We have to make them from the bottom.

---

**ghasshee** (2021-06-30):

Besides,

as just a compiler,

it does have a fatal bug.

setup_seed function in codegen.ml lacks SLOAD just after PUSHing a location of array (a seed) and thus says

“if some array is not initialized, then overwrite Program Counter to 1.”

“if some array is initialized, then abort this work.”

This is a fatal bug.

And I warn NOT TO USE bamboo at all. (maybe you know well)

It’s fully useless because it’s designed lacking the ability of designing formality at all.

If tests are done correctly, this must be avoided, and all the source code looks like this.

I concluded bamboo is an insane compiler as its unreadability indicates.

---

**ghasshee** (2021-06-30):

Pen compiler is planned to have “Internal Type checker” .

This is a new type of type checking.

External Type Check is a statically type checking as done on a program run by a single computer before its code generation. Thus, the generated machine code does not have type checking process at all.

Internal Type Check is a type checking run dynamically but statically embedded in the compiled code, which means any computer in the world who runs the program must run the type checker. This is a decentralized Type Checker.

( @pirapira 's fatal mistake was the confusion between External Type Check and Internal Type Check. )

With Linear Type Checking or, Quantitative Type Theory (a practical Dependent Linear Type Theory introduced in 2016-2018) ,

we can determine how many times each function has to be used.

Pen compiler is planned to integrate Linear Type System with the Internal Type Checking first.

---

**ghasshee** (2021-08-25):

Now pen compiler has primitive lambda calculus and let-in syntax.

It’s the starting point of functional style language and modern static type checker.

Check, review, and criticize!

---

**ghasshee** (2021-10-26):

Recursive Function is now supported in Pen Compiler !

It’s great step from imperative programming language into functional programming language !

( I have not run the code on any EVM yet.  I Just made the compiler itself. )

( Linear Type checking is not yet supported.

Now we are going to the phase of development of the formality as written in https://bentnib.org/quantitative-type-theory.pdf  and TaPL (Pierce 2000) )

---

**ghasshee** (2022-03-09):

EVM decompiler, yes it’s decompiler! , is now available in pen repository!

It’s at the alpha version!

You can compile it after installing Haskell;

```auto
git clone https://www.github.com/ghasshee/pen
cd pen/disasm
make
cat ../count.hex | ./Disasm
```

This is going to be used to develop pen compiler in the purpose of analyzing Solidity’s bytecode directly.

The architecture of pen is not solidated yet;

in a ‘Contract Oriented’ Langauge, a contract can call itself recursively,

which was @pirapira’s attempt, while solidity seems to have chosen the other way; contracts cannot call itself recursively.

---

**wangtsiao** (2022-04-19):

Awesome! Solute to your ambition.

Recently, i am reading the book TaPL, thinking about whether i can contribute to smart contract language!

After searching, i saw your amazing work, thank you for your efforts, and then I will study the design of the **pen compiler** and try to make contribute!

So, if you can, if you have the time, could you please write an introductory document for new developers of **pen compiler**. I think documentation will greatly help the development of the pen compiler.

---

**ghasshee** (2022-11-19):

Today I fixed the bug that I could not find for around a year.

So now, we can deploy a simple counter contract (count.pen) that can work on EVM.

Please follow the README.md at



      [github.com](https://github.com/ghasshee/pen)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/c/6/c64784ed5f2ec4379b53087e7a8b779e9d33aa67_2_690x344.png)



###



A compiler into EVM code










to deploy the counter contract on EVM.

---

**ghasshee** (2022-11-19):

The decompiler also works much better now than it was.

We can decompile EVM bytecode into Guarded-Command-Like Langauge (GCLL) with DEVM.

Please see this great book [Formal Methods | SpringerLink](https://link.springer.com/book/10.1007/978-3-030-05156-3)

if you want to know much about Dijkstra’s [Guarded Command Language - Wikipedia](https://ja.wikipedia.org/wiki/Guarded_Command_Language)

---

**ghasshee** (2022-11-19):

Currently, we have two clear goals.

The first one is to develop DEVM into a tool which handles Program Graph and do formal things on “Linear Algebra over Semiring Lattice” : refer e.g.

- Principles of Program Analysis | SpringerLink
- https://ems.press/books/standalone/172

The second one is to clean up the pen compiler which is really untidy still now.

It derives from bad, unreadable, and bug-friendly former project.

I, rather, would like to reduce dependencies in order to develop codes formally.

So, removing libraries such as `menhir` might be a good short term developing path.

We need to completely handle in much more sophisticated codes in modern functional programming styles such as  [MPRI 2-4](https://xavierleroy.org/mpri/2-4/) .

The road map is still long, I feel!

---

**ghasshee** (2022-11-30):

Another goal is to implement the Pen compiler from Scratch with Continuation Passing Style (CPS) transformation in Haskell.

CPS transforms Lambda Calculus into Procedural Languages like Dijkstra’s Guarded Command language in a very good manner.

I would like to derive “Contract-Oriented Language” which @pirapira started.

I might start another compiler which has the “Recursive Contract Construction”.

Another problem is that @pirapira mixed the term tree and their type.

It might lead to a bad arch when we would like to appreciate “functional pearls”.

Separating terms and types also enables us to insert a new Intermediate language between Pen lang and EVM opcodes quite easily.

To organize the architecture of the language, I started to think we must apply CPS into it.

The answer type of the continuation is the very contract type.

In @pirapira 's setting Methods `return a then becomes contract A(_)` ,

In our setting, this may be `(Term -> A) -> A` which is CPS.

Continuation is a monad `Cont A`.

In order to accomplish formality on typing, we must employ monad to wrapping the side effects.

What monad is it ? The answer is the continuation monad. We would like to build an Abstract Syntax Tree which is Functional Programming friendly style.

e.g.  if we write this in pen lang;

```auto
if cond
  then return a becomes contract A(x)
  else return b becomes contract A(y)
```

This is typable

we would like to make a AST as

```auto
TmIF
  + cond
  + TmRET(a) ; Storage[_] := x
  + TmRET(b) ; Storage[_] := y
```

And the whole body is typable using Monad Type Class.

Obviously, this code have effects and we must wrap the effect into the Cont Monad using CPS transformation.

```auto
toCPS (TmABS x ty t)  k   = toCPS t $ \m -> k (TmABS x ty m)
toCPS (TmAPP t s)    k   = toCPS t $ \m -> toCPS s $ \n -> k (TmAPP m n)
toCPS (TmIF b t s)   k   = toCPS t $ \m -> toCPS s $ \n -> k (TmIF b m n)
toCPS (TmRET a eff) k = toCPS a (k . eff)
```

with this definition of CPS;

```auto
toCPS (TmIF(cond,TmRET(a);S[_]:=x, TmRET(b); S[_] := y))
```

is converted into something like this;

```auto
return a ; S[_] := x ; return b ; S[_] := y ; if cond jump
```

which is reverse order of GCLL IR.

Haskell is a very nice language which is quite simple to write codes.

Using `Tree Comonad` , there is nothing but visibility in few lines, ( please see the source code of `DEVM` ).

---

**ghasshee** (2022-12-06):

The Language we want to create is “Functional” Term (`term`)  ; i.e. there is no distinction between statements (`stmt`) and Expressions (`expr`), whereas low level formal languages such as dijkstra’s Guarded Command language is consists of `stmt` and `expr`, which is called Guarded Command Like Langauge (`GCLL`) in our development.

To begin with the language design, we should organize the name space well.

The Highest Level Language is represented by Monadic terms `term` wrapped by monad `m`.

The Second High Level Language is represented by CPS terms `kont` .

The Mid Level Language is represented by GCLL’s `stmt` and `expr` .

The Lowest Language is represented by Assembler `asm` or EVM opcodes `[opcode]` .

The compilation is like;

```auto
src --parse-> m term --(typecheck)-> m term --CPS->  kont --(CPS App)-> GCLL(stmt) ---> [opcode]
```

One purpose of the type-check phase is to embed dynamical type-checking system as a monad, as mentioned earlier on this thread. The other purpose is the statically checking which is described in TaPL (Types and Programming Languages). We postpone type-checking construction phase until we construct the rest.

In our settings, monadic term  `m t` is intuitively defined as "adding `GCLL` effects to the `term` `t` ".

So monad `m` can be either adding dynamical type checking code or adding the continuation of the contract, which proves that the combination of monad and cps is much better design enabling what we want to do.

---

**ghasshee** (2023-01-23):

Flush

In DEVM decompiler, we used Red-Black Tree to represent AST; Red tree represents a subtree that returns expression and Black tree a subtree that does not returns expression but makes effects.

In PEN compiler, we would like to do in the similar way,

Black node in the AST is effect; e.g. Storage Assignment, Send transaction, … e.t.c.

Storage assignment does not occur until it reaches the end of method.

It means storage assignment in the middle of a method is replaced with a variable assignment in EVM memory. and when all what should be done are done, the variable is flushed to the corresponding Storage Address.

e.g.

```auto
counter : u256

method foo() {
    counter := counter + 1 ;
    let a = 100 ;
    counter := a;
    return 0
}
```

is actually

```auto
counter : u256

method foo() {
    counter := (\c ->
       let c' := c + 1;
       let a := 100 ;
       let c'' := a ;
       c'' ) counter  ;
    return 0
}
```

Here, `counter` is the only storage variable.

and its assignment is done only once just before it returns 0.

---

**ghasshee** (2023-02-07):

The design is described here and sometimes it is updated;



      [github.com](https://github.com/ghasshee/pen/blob/4eaeb8eafbb9def9d5fd4e646a25d71118595824/hs/Design.txt)





####



```txt
{--

      |
    Parse
      |
      v
  +--------------+
  | Decls & Term |
  +------+-------+
         |
    +----+----+
    |         |
 Verify    Transpile
    |         |
    |         v
    |    +-------------+
    |    |  Term only  |
    |    +------+------+
    |           |
    |         Type Check
```

  This file has been truncated. [show original](https://github.com/ghasshee/pen/blob/4eaeb8eafbb9def9d5fd4e646a25d71118595824/hs/Design.txt)










We are referring `vc` function at the Chapter 7 of Winskel’s Book (The formal semantics of Programming Langauges) as the design of the formal verification process which is going to be translated into SMT language http://smtlib.cs.uiowa.edu; i.e. we are going to depend on Z3 solver for the verification process.

This is the current development process.

We are going to completely abandon the OCaml src code which derives from pirapira’s bamboo.

Currently, Haskell-Written pen compiler’s code looks like this;

```auto
contract counter {

    counter : u256  ;
    unusedvar : u256 ;

    method inc : () :=              { counter >= 0 }
        let counter = counter + 1 ; { counter > 0  }
        counter

    method get : u256 :=            { counter >= 0 }
        counter                     { counter > 0  }

    method reset : () :=            { counter >= 0 }
        let x = 0;
        let id x = x;
        let counter = id x ;        { counter = 0  }
        if x != 0 then 0 else counter

}
```

which is located here; [pen/count.pen at 4eaeb8eafbb9def9d5fd4e646a25d71118595824 · ghasshee/pen · GitHub](https://github.com/ghasshee/pen/blob/4eaeb8eafbb9def9d5fd4e646a25d71118595824/hs/count.pen)

---

**ghasshee** (2023-03-11):

The current development is concentrating on the procedure that transforms AST into program graph.

Once it is established we can have a lot of good analytics which is derived from simple linear algebra.

Program Graph might be then considered as a “weighted pushdown automata”.

“Weighted automata” is equivalent to linear algebra over semi-ring (or rig).

see https://perso.telecom-paristech.fr/jsaka/ENSG/MPRI/Files/Lectures/FLAT-cplt-190123.pdf for the introduction to weighted automata.

---

**ghasshee** (2023-03-11):

“send” / “transfer” functions

For " The DAO " avoidance,

all contracts “COULD” control the balance as they know who send what amount to them.

i.e. all pen contracts could have the table whose entries were the sender and whose values were  amounts.

So, why not have a table inside each contract compiled by pen compiler ?

Then, in the language, the “send” function and “transfer” function is distinct.

“send” function sends some amount to a contract,

“transfer” function just change the table which is inside the contract.

i.e. “transfer” function does not send any value out of the contract to accounts outside.

Internally,

“send(A, B, amount)” function checks whether the amount is less than the table value of account B if the sender A is a contract.

“transfer(A, B, amount) " function first checks amount is less than the value of A in the table, then reduce the value of A by the amount, and then gain the table value of B by the amount.”

---

**ghasshee** (2023-06-06):

[![program_graph_and_matrix](https://ethresear.ch/uploads/default/optimized/2X/7/79858e80a399a1cf117579d9d5aa1b85ab98c040_2_690x397.png)program_graph_and_matrix3588×2065 361 KB](https://ethresear.ch/uploads/default/79858e80a399a1cf117579d9d5aa1b85ab98c040)

Now we are supporting Primitive Matrix Representation of Program Graph.

If we find the fixpoint in taking star-operation against the matrix, we will know all the program behavior.

We are not supporting all the language feature, but small subset.

However it seems a good first step towards a “Nice” compiler.

References :

- Formal Methods / An Apetizer : Formal Methods: An Appetizer | Springer Nature Link (formerly SpringerLink)
- Handbook of Automata Theory : Handbook of Automata Theory: Volumes I (Theoretical Foundations) and II (Automata in Mathematics and Selected Applications)

(The latter one is an introduction to matrix representation over Non Commutative Semiring, i.e. Automata. See chapter 1.)

Besides to the above references, if we want to find the fixpoint, we should remove ambiguity of system configuration; i.e. stack or memory (or storage) states. To achieve this, primitive automaton is not a framework enough to represent properly, removing the ambiguity. The more proper system is “Pushdown Automata” which is described in chapter 7 of Handbook of Weighted Automata. [Algebraic Systems and Pushdown Automata | Springer Nature Link (formerly SpringerLink)](https://link.springer.com/chapter/10.1007/978-3-642-01492-5_7).

---

**ghasshee** (2023-06-13):

**Banning Send (Transfer) function put other than at the last of Program Graph**

EVM is a machine which handles “money” transitions from account to account.

As described above, in pen compiler, money transition in a single contract that handles many people’s balance should not use “send” function in the internal money transitions, rather use “transfer” function which only rewrites balance table in the storage.

When running a contract, “send”/“transfer” can be a finalization of the contract running.

A contract should be made between one account and another account, and therefore, the finalization of money between them can be one time at the last in an event.

Suppose there is a program graph which is compiled to from Pen compiler’s source code;

O is some opcodes and M stands for a memory state change and C is a condition, and

S(or T) is a send function (or a transition function). The representation matrix (block matrix; i.e. O, M, C, and S is a block made of a small matrix) of the graph should be like this;

Here, M* is the star operation of M, as in the context of regular expression.

```auto
\ 1  2  3  4
1    O
2    M* C
3          S
4
```

In this graph, after we run S operation, there is no loop; i.e. M*.  ( Each of rows and columns represents a node number, and Node 1 is the initial node, and Node 4 is the last or termination node . )

We could impose the constraint to the compiler, such that S(or T) must be in the last part of the program graph without the loss of usability of a contract.

This constraint also catches an error in compiling classical condition check order problem as in TheDAO source code. (Another way of avoiding TheDAO was described above; by separation of send/transfer and by managing balance tables).

We might take the constraint as that we cannot write a contract that sends 100 $ to randomly selected 100 people, i.e.;

```auto
contract Foo() {
  method send100people100dollars(){
     for account in [1..100]
         send 100 to Addr[account];
  }
}
```

But this can be avoided, setting proper analysis of for loop;i.e. each loop in a for loop accompanied by a state change. And in a context of representation matrices of Pushdown Automata rather than those of Automata, the one-loop is not a loop in the larger block matrix.

Thus, we should construct “proper” for-loop or functionals in the compiler, such that its corresponding part in the analysis of program graph, representation matrix is not a loop, by making matrix much larger taking the primitive matrix as block elements of the larger matrix.

---

**ghasshee** (2023-10-03):

**Synthetic Way and Analytic Way**

The most of us, including other formal verification project researchers, are relying on the “[analytic](https://en.wikipedia.org/wiki/Static_program_analysis)” way of program verification. That is, program first, verification later. However, using such way means we write a program in a certain language and after that we verify the program satisfying the specification we want; the programming language has no restriction about their programs that can occur with respect to the specification. On the other hand, in using “[synthetic](https://en.wikipedia.org/wiki/Program_synthesis)” languages such as Coq, we specify the specification precisely and first. Thanking that there is Generalization of [Curry-Howard Correspondence](https://en.wikipedia.org/wiki/Curry%E2%80%93Howard_correspondence#General_formulation), program can be generated if and only if we proved that the program specification is right.

Here we saw two opposite ways of program verification, analytic v.s. synthetic.

I would not mention which is better because the both ways have each weak points.

e.g. synthetic way always can have trivial program. (Even if we write specifications  S_1, ... S_n , and if we forget to add a specification  S_{n+1}  which we need, we can always have the trivial synthetic program.  And, the proving technique in synthetic language such as Coq is sometimes much harder than formal verification of program analysis using approximation. )

**Guard Condition**

Concerning Pen Compiler, currently we have defined Syntax Tree, its Program Graph, and the representation matrix, that is, we have been developing the analytic side.

Particularly, concerning Program Graph, we did not decide how to handle loops in the graph.

One of the analytic way of loop verification is “invariant analyisis” which is studied in the theory of Hoare Logic. However, invariant analysis needs that we have to specify what the invariant is and it might be difficult to find it in cases. Then how to handle loops? For the question, we would like to apply synthetic way to pen compiler. It’s called “guard condition”.

Guard condition asserts that the loop branch condition has inductive data structure and each time we reach the condition, we have to shrink the structure, and it must shrink to just a “point structure”, breaking the loop.

For example, Coq compiler uses the guard condition in order that it assures that programs in Coq stops, and it is statically analyzed.

Many compilers, such as solidity, use Integer, but we might not need it.

Rather, we have Natural Numbers( , positive numbers, and integers as in Coq style).

Negative numbers can be represented by natural numbers in double-entry bookkeeping.

We might not need integers in formal ways.

We sometimes say loop branch condition is “noetherian” if it satisfies the guard condition, since the condition sequence is descending and has the end, as descending sequences in algebraic geometry is noetherian if it has the end point named from a great mathematician “Emmy Noether”.

**Formal Opcodes**

In such assumptions, we cannot use EVM’s  `ADD` Opcode directory in adding two numbers since `ADD` works exactly as defined in EVM.

We have inductive data structures and we have to embed them into EVM. Since embedded EVM code works and it is called in EVM, static checking does not mean even if we check the code carefully in compile time. So, in embedding data structure, we have to define Formal Addition `FADD` to be addition with boundary condition check, `FMUL` to be multiplication with boundary condition check, and so on. Of course, the gas prices of the Formal Opcodes should be cheap.


*(5 more replies not shown)*
