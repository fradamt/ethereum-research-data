---
source: ethresearch
topic_id: 4632
title: Command-line tools for ethereum
author: alexpanter
date: "2018-12-19"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/command-line-tools-for-ethereum/4632
views: 1483
likes: 0
posts_count: 3
---

# Command-line tools for ethereum

Looking at [Home | ethereum.org](https://www.ethereum.org/#cancel)

E.g. the command

> listProposal(42)

It seems that you guys don’t have a lot of experience with using terminals.

I am sorry to put it so bluntly, but terminals are all about SPEED.

We use terminals because they are MUCH faster than GUI interfaces.

So, in my humble opinion, the command SHOULD be:

> list proposal 42

- it is faster to write, contains no annoying upper cases, and is more intuitive
(list could be a function, proposal an argument, and 42 another argument)

Please consider this,

thanks.

Cheers for all your hard work!

## Replies

**flygoing** (2018-12-19):

The Geth console is a javascript REPL. `listProposal(42)` is calling a javascript function, so changing this to `list proposal 42` wouldn’t make much sense. On top of that, semantically it doesn’t make sense to separate list and proposal, because the function is named listProposal. It’s not a program `list` with a sub-routine `proposal`.

---

**alexpanter** (2018-12-19):

geez, why does everything have to be javascript these days - what a horrible language…

alright, yeah then I see why this design choice was made. Thanks!

