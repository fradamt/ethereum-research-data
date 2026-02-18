---
source: ethresearch
topic_id: 338
title: Formal Language / Category Theory
author: ghasshee
date: "2017-12-18"
category: Meta-innovation
tags: []
url: https://ethresear.ch/t/formal-language-category-theory/338
views: 5620
likes: 4
posts_count: 21
---

# Formal Language / Category Theory

I am afraid that such a powerless man could make a topic on this research page and it can be really harmful for those who are really specially talented because this particular instance of the topic may be getting ordinarily talented, non revolutional and usually very slowly developing.

But from 2014, when Vitalik said about POS and already published white paper, Dr Gavin published yellow paper and Mr Jeffery developed useful go client and user-interface, and so many… , I was eager to learn Haskell, OCaml and Category Theory;

- minimal OCaml may be developed with reading ‘Types and Programming Languages’
- It is just entrance of functional programming.
- SKI combinators are Turing Complete ( I think it can make another kind of VM )
- I am not clear about the possibility of Axiomatic Semantics with Ethereum State Chain.

There are a lot of things to do, for the purpose of this topic, and just I wanted to try to clarify.

I do not know even it is suitable for this community. There are a lot of other communities. And Blockchain enables them. But I just thought that open discussion might not cause a bad future anywhere.

Ethereum is open low level infrastructure such that I am afraid this topic is really mixing higher level and lower level in a bad manner.

## Replies

**yhirai** (2017-12-18):

https://github.com/MaiaVictor/ is pursuing some ideas.  He’s trying to unify dapp programming and Ethereum contract programming with a single sweep.

---

**ghasshee** (2017-12-18):

Wow, really nice crazy person.

The reduction optimization is the main topic for SKI combinator (or λ-calculus) and I thought the process needs much calculation as finding prime numbers. For that, he refers;

- http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.90.2386&rep=rep1&type=pdf

This is one really interesting topic.

And there might be another approach of just building axiomatic semantics on current opcodes.

This could have much reality.

---

**Silur** (2017-12-18):

with ewasm we try to use a restricted subset of webassembly to eliminate/limit all non-deterministic behaviour, thus making formal verification easier.


      [github.com](https://github.com/WebAssembly/design/blob/master/Nondeterminism.md)




####

```md
# Nondeterminism in WebAssembly

WebAssembly is a [portable](Portability.md) [sandboxed](Security.md) platform
with limited, local, nondeterminism.

  * *Limited*: nondeterministic execution can only occur in a small number of
    well-defined cases (described below) and, in those cases, the implementation
    may select from a limited set of possible behaviors.
  * *Local*: when nondeterministic execution occurs, the effect is local,
    there is no "spooky action at a distance".

The [rationale](Rationale.md) document details why WebAssembly is designed as
detailed in this document.

The following is a list of the places where the WebAssembly specification
currently admits nondeterminism:

 * New features will be added to WebAssembly, which means different implementations
   will have different support for each feature. This can be detected with
   `has_feature`, but is still a source of differences between executions.
```

  This file has been truncated. [show original](https://github.com/WebAssembly/design/blob/master/Nondeterminism.md)








Eyecandy: You currently can write wasm with S-expressions, lispers gather!

---

**ghasshee** (2017-12-18):

> With shared memory, the result of load operators is nondeterministic

This might be helpful for evm.

> Discussions about NaN

It seems that we could put it outside discussion of evm language because evm may not have floating numbers, doesn’t it?

Their approach seems to be really along ‘axiomatic semantics’, which determines PRECONDITION and POSTCONDITION of variables and requests programs to terminate.

Really nice approach I think.

And I had confused that

‘axiomatic semantics’ and ‘dependent type’ were related each other in some region.

But now it seems that they are completely independent concepts.

This means, if we have the system which has the unique type such as lisp, we can develop ‘axiomatic semantics’ on it, and vice versa.

---

**ghasshee** (2017-12-18):

Axiomatic semantics is the form like this;

> PRECONDITION program POSTCONDITION

Ethereum has state which is changing even when we are writing a contract.

So, we have to handle 2 points of state over time.

1st point is an assumption with a set of variables called pre-PRECONDITION which is used when we start writing a contract.

2nd point is real-PRECONDITION which with check-precondition-function we verify that the deployed contract with real-PRECONDITION has the same effect with that with the pre-PRECONDITION. (If check-precondition-function returned false, the contract is designed to refund suitably and then self-destruct. )

so it is like;

> pre-PRECONDITION real-PRECONDITION contract POSTCONDITION

and ethereum real-PRECONDITION that I assume is not stable as it were seen in the incident of library bugs.

( It might be false to say it is PRECONDITION but the Genesis Block be. )

In ethereum PRECONDITION is really changing with mining blocks.

Then we should set the definition a bit more formally.

evm-PRECONDITION consists of 3 components, PRECONTRACTS, pre-PRECONDITION, and real-PRECONDITION. And we also have ordinary PRECONDITION.

A (*)-PRECONDITION is a small set of variables of evm state trie which is required for a contract.

Each contract made by the formal language has a ‘checkPrecondition’ function and every time the contract is called it is designed to return error and refund all back to suitable accounts if real-PRECONDITION is changed.

Without PRECONTRACT, the ‘contract’ part can have the side effect such as calling another contract. Such side-effects all must be situated in evm-PRECONDITION,so I added PRECONTRACTS as a part of evm-PRECONDITION.

In this way, just I think even #EIP156 might not be needed if we have this kind of formal language which will take the role at a higher level. (I never say that lower level safety is not a must.)

> PRECONTRACTS pre-PRECONDITION real-PRECONDITION PRECONDITION contract POSTCONDITION

PRECONTRACTS might be designed to exclude infinite loops of contract call.

( or include in some ordinary way like described in #EIP771 )

---

**ghasshee** (2017-12-21):

For the introduction of Aximatic Semantics,

I found Hoare’s paper, maybe it is too famous and seems very nice.

http://sunnyday.mit.edu/16.355/Hoare-CACM-69.pdf

---

**ghasshee** (2018-03-11):

I am afraid I would suggest This should be in the;

#ReadingList

http://ts.data61.csiro.au/publications/csiro_full_text/Amani_BSB_18.pdf

---

**yhirai** (2018-03-12):

This is the standard textbook for programming language semantics (operational, axiomatic, denotational) https://mitpress.mit.edu/books/formal-semantics-programming-languages

---

**ghasshee** (2018-05-03):

I have just found Type Theory Tips :



      [github.com](https://github.com/jozefg/learn-tt)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/e/d/ed11304c3fb6ed447c45e7f705c372a445fa987d_2_690x344.png)



###



A collection of resources for learning type theory and type theory adjacent fields.










Also I would like to put the link of Spivak’s

Temporal Type Theory

which handles ‘time’ in a beautiful way.

https://arxiv.org/pdf/1710.10258.pdf

---

**yhirai** (2018-05-04):

In that paper, time is real numbers.  What happens when we replace reals with a partial order showing, say, “for this block’s validity, that block’s validity is necessary”?

---

**ghasshee** (2018-05-04):

Ah you mentioning a partial order which is not total.

Ah, I did not see that. It’s a good point!

---

**ghasshee** (2018-05-04):

Your question sounded like ‘Is there a polymorphism from Tree A to List A which will do a breadth first search (which is determined by timestamps), where A denotes for a total ordered number ?’

And I am not sure but there might be a kind of manager who is selected based on RANDAO, so locally ( I mean in some small time,) the POS sharding system can be regarded as a centralized system.

This might be wrong.

---

**ghasshee** (2018-05-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/yhirai/48/153_2.png)
    [Smart contracts temporal properties verification](https://ethresear.ch/t/smart-contracts-temporal-properties-verification/1818/2)



> LTL with an “until” operator can specify some interesting properties https://arxiv.org/pdf/1802.06038.pdf (Definition 3.3).
> Modality of the past is sometimes convenient (if player A has cheated, it can be punished).  Or, in Casper contract, other branches are also important (if player A contradicts what it said on another branch).
> Regarding Coq, the thrid author of the above paper is somebody to contact.
> You might be interested in modeling
>
>
> Plasma Cash or
> Plasma MVP
>
> They define rather invo…

---

**ghasshee** (2018-06-06):

NATURAL ROUGH SKETCH

contract guaranteed programming language

A formal contract must not be a game of the language by which it is written.

So, formal language on evm MUST have an abstract interface which define The Formal Language, i.e. the behavior,  and in case it did an unexpected behavior which happens outside the formal language, i.e.  lower level bug, it allows to be double-checked.

In this sense, " CODE is LAW " would be achieved in a higher (formal) programming language which is human readable and highly structured more than machine codes.

how to do that ?

Simply every time when ‘ether’ of the contract moves, the original source code written by formal language is checked. The checking process will consume much more gas than that without guarantee. Formal way will cost literally.

---

**ghasshee** (2019-10-23):

Here, I call ‘Gas’ for the ether in a contract.

# Gas System

c.f. #Type System

# Against  The Parity Contract Bug

The proof that Gas was accessible from what person and what person is needed.

---

**ghasshee** (2019-12-22):

State Transition Function:

For some state transition function f and for substate S_i,

```auto
if ( S_i+1 == S_i ) then
it means stable state .
else
the state is changing.
```

This is the method of analyzing the syntax trees or lexers of a compiler in context of automaton.

In order to apply this method to blockchain programming,

we assert that function application always need the block height .

1. first lap the block state by monad and separate the purely functional part and the non-pure part.
2. the abstract contract language is functional.
3. the syntax is like this

```auto
t ::=
   | x                      (variable)
   | λb.λx.t                (abstraction)
   | t b t                  (application)
   | b                      (block height)

b ::=
   | n                      (natural number)
```

# Evaluation

For instance let’s see the contract code execution like

```auto
assert sender_balance == 150;
let (return_address_of_Alice, success) = send_100_ether_to_Alice 10000 sender_balance in
send_100_to_Bob 9000 return_address_of_Alice
```

and this pseudo snippet should fail.

It means evaluation of (t n (t m t)) should fail if m>n.

# Typing / Gas

Typing Rules or Gas Rules on this syntax can decide that the program can execute or returns error. (ToDo)

---

**ghasshee** (2019-12-22):

Note: One way to develop State Transition Functions is doing with Reference Types in Classical Type Theory;

```auto
the_previous_state = ref (Alice, 100ether);
new_state := send_10ether_to_Bob !the_previous_state
```

and whose typing is ;

```auto
the_previous_state : Ref (Address * Ether)
new_state : Ref (Address * Ether)
```

But we need the block height to apply function;

```auto
the_previous_state : Ref (BlockHeight * Address * Ether)
new_state : Ref (BlockHeight * Address * Ether)
```

and purification of the theory and its typing rules in the ToDo.

---

**ghasshee** (2020-01-07):

Against TheDAO Contract Leak,

the blockchain functional programming languages have another primitive constants

```auto
t ::=  ...
    | send_once latest t t t            (send once)
    | send_nth latest t t t t           (send at most n times)
    | v                          (value)

b ::= ...
    | latest                     (latest block)

v ::=
    | n                          (natural number)
    | wei                        (wei)
    | addr                       (address)
```

The evaluation rules of `send_once` are primitively defined such that it cannot be sent from the same sender to the same receiver with the assertion before the sending opcode like in the ordinal modified way.

The details of the evaluation / type (gas) rules to be later.

---

**ghasshee** (2020-01-10):

https://sdk.dfinity.org

Functional programmer @nomeata who has plenty of the knowledge of functional programming has released a programming language on a blockchain in last November. The website says it is a lanuguage internally like OCaml but its syntax is like javascript.

I did not see the src code, but it might be helpful when you consider blockchain programming languages.

---

**ghasshee** (2020-05-30):

Hi, I started the zulip page for the research page of formal language.


      ![](https://ethresear.ch/uploads/default/original/3X/4/3/43a768a6bc041934e87b530a83c1e74e49fbabad.svg)

      [Zulip](https://formal-blockchain.zulipchat.com/login/)



    ![](https://ethresear.ch/uploads/default/original/3X/c/5/c59dfc39716e44a2e2ea7524a4d9b8d20da18c0e.png)

###










It is the prereseach-level (undergraduate level) of research group,

interested in HoTT, ∞-groupoids, Types and Programming Languages.

Feel free to join!

