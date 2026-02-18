---
source: magicians
topic_id: 13846
title: "EIP: math checking"
author: RenanSouza2
date: "2023-04-17"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/eip-math-checking/13846
views: 1740
likes: 2
posts_count: 6
---

# EIP: math checking

Hey everyone, this is a different proposal for math checking at EVM level

https://github.com/ethereum/EIPs/pull/6888

## Replies

**matt** (2023-04-17):

> It was an openzeppelin library and then incorporated in solidity’s default behavior. Bringing this to EVM level can combine both gas efficiency and safety.

Just wanted to say that I think this is exactly the type of thing that shouldn’t go into the protocol. The aims of the EVM are to maximally simple and extensible. This EIP proposes making the EVM more complex in a way that can already be achieved with user code.

---

**RenanSouza2** (2023-04-17):

Thank for taking your time to review this EIP,

It already is possible to do this but has to be operation by operation so you end up adding a lot of extra code to keep the code safe

With this implementation one could check the flags once per block code or one time in the whole execution. The times that would be suggest to check the flag is when the code switchs between using signed and unsigned numbers.

And there were other proposals that didn’t had to be in evm but greatly bennefit of this low level, like push0.

Let me know what you think ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) and thanks again

---

**hiddenintheworld** (2023-04-17):

I agree, the problem is that a lot of people still have not understand why EVM is designed this way.

---

**gcolvin** (2023-04-26):

I’d like to see something like this.  I don’t know if this is best design, but like that it carefully defines the meaning of the flags for all operations.

I’m sorry I don,t haven’t time to dig deeper, but will note that:

- UERR and SERR are not the usual names, as the conditions are not always errors. CARRY and OVERFLOW are the typical names.
- These are well defined only for addition and subtraction – CPUs vary in how they behave with other operations.  I don’t know how well your definitions map to the usual conventions.
- Depending on the underlying libraries it may or may not be efficient to compute the flags for all operations.  I don’t know how efficiently your definitions can be computed.
- It might be more a more efficient EVM convention to add two jump instructions conditional on each flag.

A good discussion of how the flags work is here: [The CARRY flag and OVERFLOW flag in binary arithmetic](http://teaching.idallen.com/dat2343/11w/notes/040_overflow.txt)

The Wikipedia entries are OK too, starting here: [Status register](https://en.wikipedia.org/wiki/Status_register).

---

**RenanSouza2** (2023-04-27):

Thank you so much for your inputs, I`ve adopted the names and the new jump instructions.

About the hardware definitions, it makes sense for hardware to behave like that, I would still like to include in some way every arithmetic instruction.

I`m thinking ways to measure the added load to the instuctions as in many cases listed here it would require 2 opearions by instruction.

I`m working in my own execution client implementation but as it is not yet in production neither ready the measurements would’t mean much.

