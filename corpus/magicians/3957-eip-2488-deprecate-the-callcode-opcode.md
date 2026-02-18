---
source: magicians
topic_id: 3957
title: "EIP-2488: Deprecate the CALLCODE opcode"
author: axic
date: "2020-01-24"
category: EIPs > EIPs core
tags: [opcodes, eip-2488]
url: https://ethereum-magicians.org/t/eip-2488-deprecate-the-callcode-opcode/3957
views: 2673
likes: 1
posts_count: 4
---

# EIP-2488: Deprecate the CALLCODE opcode

Discussion topic for [Add deprecate CALLCODE EIP by axic · Pull Request #2488 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/2488)

EIP: [EIP-2488: Deprecate the CALLCODE opcode](https://eips.ethereum.org/EIPS/eip-2488)

## Replies

**MicahZoltu** (2020-08-28):

If we can’t find any *real* usage of the CALLCODE opcode, I would rather just have that opcode be treated as an undefined opcode so we can re-use it in the future, rather than defining it to have certain behavior.  From the EIP it sounds like you have plans to research this further, so I think the results of that research will help inform whether we should do as this EIP suggests, or just free up that opcode and pretend it never existed.

---

**axic** (2020-08-28):

It was definitely used in some experiments, that’s how DELEGATECALL emerged. I am still torn which is easier: a) having a stub implementation as proposed on EIP-2488, or b) having the current implementation.

But you are correct, more research is needed before concluding on a final proposal.

---

**xrchz** (2025-12-14):

I would love to see CALLCODE deprecated, and have a slight preference for Micah’s suggestion (vs the current EIP). But either way is fine - just want to stop having to think about its semantics in EVM implementations and specifications.

