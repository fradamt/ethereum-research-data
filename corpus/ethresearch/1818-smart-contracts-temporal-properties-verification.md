---
source: ethresearch
topic_id: 1818
title: Smart contracts temporal properties verification
author: unboxedtype
date: "2018-04-24"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/smart-contracts-temporal-properties-verification/1818
views: 3440
likes: 6
posts_count: 5
---

# Smart contracts temporal properties verification

Hello, researchers!

I am investigating ways of verifying temporal properties of smart contracts using Linear Temporal Logic.

Putting it simple, besides checking that a smart contract never violates some property P

(variables never overflow, balance is always positive, etc so called safety properties), I would like to

ensure that it behaves as expected over its lifetime: if event B fires, it must be the case, that,

before that, event A has fired; if event A fires then after some time, event B will fire; and so on.

As far as I know, most approaches concerning smart contract correctness are focused solely on safety

properties, while liveness properties stay out of reach for most modern tools/attempts.

My aim is to research this subject in several directions. Questions to be answered are:

1. To what extent Linear Temporal Logic (in its classic form) can be a good fit for specifying useful properties of smart contracts? We have to do several specification attempts before the answer will emerge.
2. Do we need to extend LTL with modality of the past? While doing some toy examples, I found,
that sometimes I need to express dependency between the current event and past events instead of
traditional “event A leads to event B” future-oriented style. I would like to make specification language as convenient as possible for a business user.
3. For bounded systems, temporal property can be model-checked. For unbounded systems, temporal model checking is undecidable; for that reason, I would like to build a reasoning framework inside Coq proof assistant to be able to deduce properties using logical inference.

The research work is in its infancy, however, I made a prototype of the framework in Coq, and specified

one toy contract example.

What I would like to do is to specify some non-trivial contracts. There are many contracts source code

available online, but this is useless unless someone can answer questions regarding on how the contract

**should** behave over time (having only the source code, you always have to guess about its **intended** behavior)

For that reason, I need someone who can play a role of an expert on contract’s behavior under study.

This person can be someone who wants to check his contract for correctness, or more deeply understand

its properties.

Feel free to contact me if interested in *any form* of research collaboration. We can discuss things.

Thanks!

P.S. For direct messaging, this site has “Messages” facility, look inside the profile.

## Replies

**yhirai** (2018-04-24):

LTL with an “until” operator can specify some interesting properties https://arxiv.org/pdf/1802.06038.pdf (Definition 3.3).

Modality of the past is sometimes convenient (if player A has cheated, it can be punished).  Or, in Casper contract, other branches are also important (if player A contradicts what it said on another branch).

Regarding Coq, the thrid author of the above paper is somebody to contact.

You might be interested in modeling

- Plasma Cash or
- Plasma MVP

They define rather involved games, so a rigorous analysis is welcome.  I modeled [Plasma MVP a bit in Coq](https://github.com/pirapira/practice/blob/master/simple_plasma/SimplePlasma.v), but it’s currently halted.

---

**unboxedtype** (2018-04-25):

Hello, mr. Hirai!

> Modality of the past is sometimes convenient (if player A has cheated, it can be punished). Or, in Casper contract, other branches are also important (if player A contradicts what it said on another branch).

Regarding of reasoning about different Casper branches, it might be the case that CTL logic will suite it even more naturally, but its just a guess.

What I found about past modality is that sometimes I need to specify something like:

“It is always the case that if this event happens then it must have been preceded by that other event”.

Maybe it is expressible with some combination of Until/Weak until/Eventually operators, but I doubt it will feel natural to do so for an end-user.

> Regarding Coq, the third author of the above paper is somebody to contact.

Thanks, I will consider the option of contacting that person!

> They define rather involved games, so a rigorous analysis is welcome.

Yeah. Those foundational smart contracts are made of even more difficult algorithms than some “average” smart contract, while I see my “target audience” as of more typical business smart contracts, and those I would like to address in my research.

---

**hyeonleee** (2018-05-07):

Hi unboxedtype

As I can’t find direct message ficility, I write reply on here.

Like you, I found the fact that most existing approaches are focused on safety properties.

So I’m really interested in proving Linvness property in smart contract and to proove these kinds of properties,

LTL is general logics to use.

But I’m novice in this subject and started thesedays.

In the while, I found your post and like a lot as I found the person who is finding something like me

Do you have progress in this research?

---

**unboxedtype** (2018-05-14):

Hello, hyeonleee!

My current observations are as follows:

Some systems are complex, and still they can be specified using some simple specifications. Think of a compiler. It can be very complex inside (different layers of optimization, etc) yet most of the time we want to check a rather simple thing: a behavior of high level program is preserved by the low-level output of the compiler.

Take another example: some distributed mutual exclusion or leader election algorithm. It can be very complex inside, nevertheless there are several canonical properties we would like to check for that kind of beasts (safety, progress, starvation-freedom etc) that are easily expressed in LTL logic.

On the other hand, we have systems that look not so complex, and yet it is very difficult to formally specify them.

Take a text editor as an example. Its purpose is simple, but it is stuffed with user-level options, and it makes specification hard.

Formal methods are of little value if your specification becomes so complex that only few experts can read

and understand them: you just moved your trust from complex code to the complex specs, and this is no good.

Specs must be considerably easier to understand to be useful.

So, I am trying to find that class of smart contracts which are easy to specify but have complex implementations.

The second thing I am thinking of is: how can we debug specifications? Are there any tools that can help ensure in its correctness. I am aware of synthesis techniques using SAT/SMT engines (see Rosetta tool).

That is all for now.

