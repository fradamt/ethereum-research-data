---
source: magicians
topic_id: 16220
title: RollCall #1 - In-Person At Devconnect Instanbul
author: adietrichs
date: "2023-10-23"
category: Protocol Calls & happenings
tags: [rollcall, rip, devconnect]
url: https://ethereum-magicians.org/t/rollcall-1-in-person-at-devconnect-instanbul/16220
views: 1638
likes: 10
posts_count: 5
---

# RollCall #1 - In-Person At Devconnect Instanbul

As discussed during the [inaugural RollCall #0](https://github.com/ethereum/pm/issues/885), [@CarlBeek](/u/carlbeek), [@yoavw](/u/yoavw), and I are organizing an in-person session in Istanbul as part of Devconnect. The session will be held on Wednesday, November 15, during the second day of the [L2DAYS](https://l2days.xyz/) event organized by L2BEAT and Scroll.

**To attend, please ensure you have a ticket for L2DAYS. If you have issues, please reach out to Carl or Ansgar via the `#rollcall` channel in the [Eth R&D discord](https://discord.com/invite/qGpsxSA).**

## Schedule

- 10:00-10:30 Introduction
- 10:30-11:45 Meta: RollCall & RIP

RIP process
- Registry (precompile addresses, opcodes, tx types, EOF versions, etc.)
- Relationship with L1
- Different standards needs for zk vs. optimistic RUs

**11:45-12:45** EVM Equivalence

- Perspectives on future EVM evolution
- Pick&choose RIPs vs standardized L2EVM
- EVM 2.0: state expiry, tx parallelization, etc.
- Progressive precompiles

**12:45-13:30** Lunch Break
**13:30-15:00** Breakout 1

- secp256r1 Precompile
- Ethereum Object Format (EOF)
- Standardized bridges

**15:00-15:30** Coffee Break
**15:30-17:00** Breakout 2

- ERC-4337: account abstraction
- Verkle and alternative state commitment schemes
- Multidimensional fee markets for L2

**17:00-18:00** Results & Conclusion

If you have additional topics you would like to discuss, please leave a comment below. In addition, there will be room for impromptu discussions during the breakout sessions.

We are aware that not everyone will be able to attend the event in person. We are exploring options for remote attendance and/or recordings.

## Replies

**krlosmata** (2023-10-24):

Maybe it is worth to discuss the following EIP: [EIP-2935: Save historical block hashes in state](https://eips.ethereum.org/EIPS/eip-2935)

which enables saving the historical blockhashes in the state.

- we are actually doing that in L2 (allowing more than 256 historical blocks retrieval)
- this is very convenient for L2 since with a single L1 blockHash you can access all historical L1 data from L2

---

**CarlBeek** (2023-10-24):

Interesting, out of interest, is there that much demand/usage for historical data from within L2?

Are you proposing putting the data only in the L2 block-header? I think a standardized format for extending the L2 block-header could be super helpful.

In terms of the above schedule, this would be a good candidate to have a mini break-out session on if others are interested.

---

**krlosmata** (2023-10-24):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/df788c/48.png) CarlBeek:

> Interesting, out of interest, is there that much demand/usage for historical data from within L2?

Not right now, but I expect it to be useful in a near future for L2 to pass historical data from L1 to L2 with a single blockhash. One application could be some sort of bridging where instead of using a tree of deposits, we can use the Ethereum state tree itself.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/df788c/48.png) CarlBeek:

> Are you proposing putting the data only in the L2 block-header? I think a standardized format for extending the L2 block-header could be super helpful.

I like the idea to standardize L2 block-headers and add the L1 blockhash there (Although I think it is not easy since every rollup moves L1 data into L2 in different ways)

The purpose of adding historical blockhashes is that you can use many old L1 blockhashes in L2 and at the end you just need to proof that those blockhashes are included in the last L1 blockhash. Therefore, there is no need in L2 to know about all previous L1 blockhashes, just the last one.

Also (depending on L2 BLOCKHASH opcode) being able to retrieve all previous blockhashes, not just the last 256

---

**CarlBeek** (2023-11-04):

Due to the inability of many community members to attend Devconnect Istanbul in person and the desire not to put undue pressure on others to attend who many not feel safe doing so, we have decided not to host RollCall #1 at DevConnect. We explored the idea of remote participation, but were not happy with any of the proposed solutions. While we appreciate this may be a major disappointment to many of you (I know is it for me), we feel it is unwise to try launch a standards effort when many participants will be unable to attend.

## How we will be proceeding:

We will be canceling the in-person RollCall #1 - Devconnect Istanbul, but many of the people who planned to attend will still be in Istanbul, so informal meet-ups are highly encouraged. In particular, it’d be great to still have discussions and make progress on some of the specific topics listed above and more generally on how RIPs can be governed and run. We can then formulate these as more concrete written proposals for wider community discussion here on EthMagicians, and in upcoming RollCalls. Both myself and [@adietrichs](/u/adietrichs) will around and would love to chat so please reach out to either of us.

