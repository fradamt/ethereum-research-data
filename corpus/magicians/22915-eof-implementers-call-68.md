---
source: magicians
topic_id: 22915
title: EOF Implementers Call #68
author: system
date: "2025-02-19"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eof-implementers-call-68/22915
views: 74
likes: 4
posts_count: 3
---

# EOF Implementers Call #68

# EOF Implementers Call #68

- Date and time in UTC in format March 05, 2025, 15:00 UTC with link to savvytime.com or timeanddate.com. E.g. Mar 05, 2025, 15:00 UTC
- Duration: 60
- Zoom: Launch Meeting - Zoom
- Other optional resources

# Agenda

- Testing Update
- Client and Compiler Update
- Osaka Testnets Plan - HackMD
- EOF-devnet-1 changes

Omnibus PR - Update EIP-3540: Move to Review by shemnon · Pull Request #9446 · ethereum/EIPs · GitHub

EOF-devnet-2 changes

- PAY Opcode
- Add Metadata Section EIP-7834
- EXTCODEADDRESS EIP-7780 / EOFCODETYPE EIP-7761

Other comments and resources

[GitHub Issue](https://github.com/ethereum/pm/issues/1312)

## Replies

**shemnon** (2025-03-05):

Agenda for tomorrows call:

- Testing Update
- Client and Compiler Update
- Osaka Testnets Plan - HackMD
- EOF-devnet-1 changes

Creator Contract from EIP-7873 - how feature-rich should it be? And specifically, should it include a flag to include CALLER in the final_salt for non-frontrunnable deploys?
- Omnibus PR - Update EIP-3540: Move to Review by shemnon · Pull Request #9446 · ethereum/EIPs · GitHub
- commit to final hash.  0xff or not?

EOF-devnet-2 changes

- PAY Opcode (@wjmelements - if you want to present your slides)
- Add Metadata Section EIP-7834
- EXTCODEADDRESS EIP-7780 / EOFCODETYPE EIP-7761

---

**shemnon** (2025-03-05):

Meeting Notes

Client and compilers - no updates

Testing - there is a “final” devnet 0 test suite - pleas test and report back

Devnet 1 - ’

- hash : 0xff || sender || salt

0xff guarantees no rlp collisions, that was EIP-1014 motivation.  Retain it for consistency.
- creator contract - add optional sender to salt

without it, the contracts can be front runnable, wherever it matters (such as using tx.origin in initcode).
- Could we use two selectors?  One that is sender safe and one that is sender unsafe?
- Start with simplest version.  Initcode hash, plus a called salt, plus arguments for initcode. don’t include sender.
- ERCs can deploy the safer ones and tooling can ensure deployment.
- We need to communicate with dev tool to see how it would impact their use case. (Foundary, hardhat, etc.)
- Frangio is still nervous.  We need to have a flag for the caller.

Pay Opcode

- slides presented by wjelemts.
- No consensus one way or another

Metadata section

- Can metadata section be excluded from initcode hash as a part of TXCREATE initcode?  Uniswap drops metadata because it impacts addresses.
- Metadata has been solved on etherscan for a while (frangio).  There are concerns about frontrunnig that may have been solved.

