---
source: ethresearch
topic_id: 12481
title: Yet another decentralized zkRollup L2 design
author: dantaik
date: "2022-04-23"
category: Layer 2
tags: []
url: https://ethresear.ch/t/yet-another-decentralized-zkrollup-l2-design/12481
views: 2843
likes: 3
posts_count: 4
---

# Yet another decentralized zkRollup L2 design

Over the last few months, we (the taiko team) have been working on the design of a general-purpose zkRollup layer 2 that will be decentralized from day 1. We hope to share it with the Ethereum community to collect feedbacks. Our design is still in its early draft stage but we believe it can be improved easily to adopt EIP-4844. Here is the link to our doc:

https://taikocha.in

All feedback are welcomed. Thank you. dan@taikocha.in.

## Replies

**MicahZoltu** (2022-04-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/dantaik/48/18607_2.png) dantaik:

> https://taikochain.github.io/l2design/

Link doesn’t work.

50 characters to bypass forum requirements.

---

**dantaik** (2022-04-23):

Thank you for reporting the link issue. It’s now fixed.

---

**MicahZoltu** (2022-04-23):

General feedback: I’m not a fan of using a zkEVM as I think the benefits don’t outweigh the costs.  For a simple example, IIUC a VM with backward jumps (loops) is significantly harder to generate proofs for than a VM that simply doesn’t have any backward jumps.  Also, EVM is 256-bits which I have heard is problematic for ZK provers (something about 224 bits being a better fit?).  Further, a lot of lessons have been learned in developing the EVM and if you ask any of the core developers who work on it they can list off a bunch of things they would change if they didn’t have to worry about supporting already deployed contracts, like the completely removal of `SELFDESTRUCT`, weird gas accounting subtleties (EIP-2730), support for smaller width storage slots, removal tx.origin, etc.

All in all, I think any L2 project would be far better served at *least* using a strict subset of the EVM, and potentially better off using a derivative of it or something entirely new.  The problem with “entirely new” of course is that you need to build a new compiler and toolchain, which I do understand is a pretty big undertaking.  By doing a subset or a derivative, you may be able to still use most of the Ethereum toolchain.

