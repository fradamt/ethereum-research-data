---
source: ethresearch
topic_id: 7703
title: Residue Numeral Systems for ZK-STARKs
author: Levalicious
date: "2020-07-18"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/residue-numeral-systems-for-zk-starks/7703
views: 1246
likes: 1
posts_count: 3
---

# Residue Numeral Systems for ZK-STARKs

Hello!

I’ve been recently tinkering with the beginnings of a STARK VM and one of the things I’ve been considering is using Residue Numeral Systems to represent the numbers for it. RNS allows you to take an integer, represent it as a set of remainders modulo a set of moduli, letting you do cool things like carryless multiplication, addition, and subtraction, all over the field bounded by the product of the moduli.

However, the disadvantage of the system is that non-arithmetic operations like shifts and binary ops are very expensive. I’m currently doing them by converting to a ‘normal’ u256 and then converting back, although I have some ideas to implement with base extension that should improve efficiency.

I’m hoping to use RNS for my implementation, as I’ve already been getting decent performance benefits from it, but I’m not sure if the fact that it is over a field specified by the product of coprime moduli instead of a prime or binary field will have a security impact.

Any advice on things to watch out for while working on this?

## Replies

**Recmo** (2020-07-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/levalicious/48/2296_2.png) Levalicious:

> field specified by the product of coprime moduli

That would not be a field, but a ring. The main difference being that there are numbers other than zero that don’t have an inverse (specifically the multiples of any of the RNS moduli). Not being able to invert would be something to watch out for. Another thing would be the existence of any necessary roots of unity.

---

**Levalicious** (2020-07-24):

True, but division algorithms that eliminate those other non-invertible numbers are quite trivial to implement, at the expense of some computational cost. The simplest one is to just convert to a standard uint 256 and apply a modular inversion modulo the product of the primes, although many more efficient methods exist.

