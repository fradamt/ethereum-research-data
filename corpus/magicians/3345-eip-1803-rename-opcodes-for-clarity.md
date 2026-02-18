---
source: magicians
topic_id: 3345
title: "EIP-1803: Rename opcodes for clarity"
author: axic
date: "2019-06-02"
category: EIPs
tags: [opcodes, devx]
url: https://ethereum-magicians.org/t/eip-1803-rename-opcodes-for-clarity/3345
views: 4034
likes: 4
posts_count: 8
---

# EIP-1803: Rename opcodes for clarity

Discussion topic for


      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-1803)




###

Ethereum Improvement Proposals (EIPs) describe standards for the Ethereum platform, including core protocol specifications, client APIs, and contract standards.

## Replies

**axic** (2019-06-02):

A comment about changing the title: https://github.com/ethereum/EIPs/pull/1803/#issuecomment-488119162

---

**ekpyron** (2019-06-19):

It might be worth considering to rename `NOT` to `BITNOT` (and maybe all other bitwise operations as well).

---

**axic** (2019-06-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ekpyron/48/2033_2.png) ekpyron:

> It might be worth considering to rename NOT to BITNOT (and maybe all other bitwise operations as well).

How about `NEG` for bitwise negation?

---

**axic** (2019-09-19):

[@ekpyron](/u/ekpyron) [@chriseth](/u/chriseth)  what do you think about this?

---

**axic** (2019-11-27):

Within the Solidity team today we’ve discussed a couple of new additions:

- ADDRESS -> SELFADDRESS (in line with SELFBALANCE)
- ORIGIN -> TXORIGIN
- CODESIZE -> SELFCODESIZE (as above)
- CODECOPY -> SELFCODECOPY (as above)
- GASPRICE -> TXGASPRICE
- DIFFICULTY -> BLOCKDIFFICULTY
- TIMESTAMP -> BLOCKTIMESTAMP

---

**MicahZoltu** (2020-07-29):

I just learned about this, what needs to happen to get this moved to final?  Given that it is just a naming thing, it feels like there is little coordination needed and if everyone agrees we can just move to final, update the yellow paper, and be done.  Am I missing something that makes this particularly challenging to get through?

---

**axic** (2020-10-21):

There is more discussion to be found at https://github.com/ethereum/solidity/issues/7966

