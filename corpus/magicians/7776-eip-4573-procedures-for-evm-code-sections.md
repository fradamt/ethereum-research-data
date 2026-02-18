---
source: magicians
topic_id: 7776
title: "EIP-4573: Procedures for EVM Code Sections"
author: gcolvin
date: "2021-12-16"
category: EIPs > EIPs core
tags: [evm, opcodes, core-eips]
url: https://ethereum-magicians.org/t/eip-4573-procedures-for-evm-code-sections/7776
views: 2544
likes: 0
posts_count: 6
---

# EIP-4573: Procedures for EVM Code Sections

Currently, Ethereum bytecode has no syntactic structure, and *subroutines* have no defined interfaces.

We propose to add *procedures* – delimited blocks of code that can be entered only by calling into them via defined interfaces.

Also, the EVM currently has no automatic management of memory for *procedures*.  So we also propose to automatically reserve call frames on an in-memory stack.

Constraints on the use of *procedures* must be validated at contract initialization time to maintain the safety properties of EIP-3779: Valid programs will not halt with an exception unless they run out of gas or recursively overflow stack.

## Replies

**gumb0** (2022-01-25):

What is the motivation to have multiple sections with multiple entry points in each one as opposed to

- multiple sections each one with a single entry point
- or a single code section with multiple entry points?

---

**gcolvin** (2022-01-26):

The motivation is just to allow for the encapsulation of related sets of procedures into independent code sections.  External tools could then combine these sections like libraries for different contracts.

The encapsulation allows for all of the procedures in a section to share optimized subroutines that will not be accessible to other code sections.  (And if we don’t allow for multiple entry points we can wind up with people using flags to do the job with a single one anyway.)

---

**gumb0** (2022-01-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> The encapsulation allows for all of the procedures in a section to share optimized subroutines that will not be accessible to other code sections.

How will they be not accessible? Isn’t `CALLPROC` allowing to call any entry point of any section?

---

**gcolvin** (2022-01-26):

Subroutines are accessed via RJUMPSUB, which is always limited to the current code section.  And only those procedures called out in an Entry Point section can be called from a different code section.

I’ll note that the procedure concept stands on its own, and I could propose these opcodes independently if we don’t find them useful as entry points.

---

**gcolvin** (2022-01-30):

I’ve taken my own suggestion, [@gumb0](/u/gumb0)  and narrowed this EIP down to just specifying procedures.

