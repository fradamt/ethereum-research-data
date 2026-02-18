---
source: magicians
topic_id: 4202
title: "EIP 2604: Conditional EXTBALANCE Repricing"
author: wjmelements
date: "2020-04-17"
category: EIPs
tags: [evm, opcodes, gas, eip-2604]
url: https://ethereum-magicians.org/t/eip-2604-conditional-extbalance-repricing/4202
views: 1061
likes: 2
posts_count: 6
---

# EIP 2604: Conditional EXTBALANCE Repricing

Rename BALANCE to EXTBALANCE and reduce its cost to 10 if it queries the current account.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/2604)














####


      `master` ← `wjmelements:extbalance`




          opened 04:04AM - 17 Apr 20 UTC



          [![](https://avatars.githubusercontent.com/u/799573?v=4)
            wjmelements](https://github.com/wjmelements)



          [+35
            -0](https://github.com/ethereum/EIPs/pull/2604/files)







This suggests renaming of BALANCE to EXTBALANCE and repricing it.

## Replies

**wjmelements** (2020-04-17):

It would be nice if we could reduce all trie-based opcode gas when the state is cached, as we do in 1380.

---

**fubuloubu** (2020-04-18):

This might have been a good approach to take before Istanbul, but Istanbul enables [EIP-1884](https://eips.ethereum.org/EIPS/eip-1884), which adds the `SELFBALANCE` opcode, doing exactly as you describe. Probably does not make sense to do both at this point.

---

**jochem-brouwer** (2020-04-24):

Pre-Istanbul contracts get penalized, because these use `BALANCE` on themselves and do not use `SELFBALANCE` while what these semantically do is exactly the same. Thus changing `BALANCE` gas for all addresses, but introducing `SELFBALANCE` per the Istanbul EIP is not reasonable for me.

I support this EIP.

It also makes sense to rename `BALANCE` to `EXTBALANCE`: look at `EXTCODESIZE` vs `CODESIZE`. However, this does not apply to `SELFBALANCE`, but changing that to `BALANCE` would be confusing.

---

**fubuloubu** (2020-04-24):

I’m not making a value judgement of this proposal, more just stating that we already have `SELFBALANCE`, it seems unlikely to have the EVM design basically recant that choice, and do it the “correct” way, which might involve a bunch of additional checks that could affect the cost reduction that EIP-1884 provides

---

**axic** (2020-04-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> It also makes sense to rename BALANCE to EXTBALANCE : look at EXTCODESIZE vs CODESIZE .

Renaming opcodes, includes this one, is also proposed by [EIP-1803: Rename opcodes for clarity](https://ethereum-magicians.org/t/eip-1803-rename-opcodes-for-clarity/3345) (Correction: it seems this particular renaming didn’t made it into the forum/EIP, but was discussed on Gitter post-Istanbul)

However as discussed during past ACD calls, this is not part of hard forks, just adopted by tooling.

