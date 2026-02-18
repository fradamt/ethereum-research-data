---
source: magicians
topic_id: 3652
title: "EIP-2274: Multiple address spaces for Precompiled contracts"
author: AntoineRondelet
date: "2019-09-12"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-2274-multiple-address-spaces-for-precompiled-contracts/3652
views: 1306
likes: 0
posts_count: 3
---

# EIP-2274: Multiple address spaces for Precompiled contracts

Hi everyone,

I just wrote this draft EIP to have different addressing schemes to define precompiled contracts



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/2274)














####


      `master` ← `AntoineRondelet:precompiled-versioning`




          opened 11:02AM - 12 Sep 19 UTC



          [![](https://avatars.githubusercontent.com/u/17513145?v=4)
            AntoineRondelet](https://github.com/AntoineRondelet)



          [+72
            -0](https://github.com/ethereum/EIPs/pull/2274/files)













Happy to discuss it and have any feedback!

## Replies

**shemnon** (2019-09-20):

First, I don’t think there is any requirement technical or specification wise that all precompiled contracts exist in a consecutive space.  The chain operator could just as easily add a precompiled contract at 0x42 instead of 0xE.

As an alternative what if instead the precompile range from 0x0 to 0xffff was assigned to precompile operators?  Much like port assignments are for TCP.  Mainnet would get 0x0000 to 0x00ff and a private use space would be reserved at 0xff00 to 0xffff much like unicode.  There are some mainnet uses such as 0xdead for ENS, where they could just be given the 0xdea0-0xdeaf range during the initial assignments.

I think this is no less disruptive than making sure the vmID space is properly used and has the advantage of not requiring a new opcode (with associated required toolchain support in solidity and vyper).

---

**AntoineRondelet** (2019-09-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> First, I don’t think there is any requirement technical or specification wise that all precompiled contracts exist in a consecutive space. The chain operator could just as easily add a precompiled contract at 0x42 instead of 0xE.

That’s right, I am not aware of any requirement for that. Nevertheless, I think that following current patterns on address allocation for precompiled contracts (hence declare them using consecutive addresses) makes sense. It is easier to reason about and improves dev experience IMHO. I think it is a bad pattern to randomly allocate addresses to newly created precompiled as it would pollute the address space (even though it is extremely big) with these “special addresses” that should not be associated with an EoA and newly deployed contracts.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> As an alternative what if instead the precompile range from 0x0 to 0xffff was assigned to precompile operators? Much like port assignments are for TCP. Mainnet would get 0x0000 to 0x00ff and a private use space would be reserved at 0xff00 to 0xffff much like unicode.

Yes, this would also make sense. I think this has already been discussed on this platform, and this approach is also described in the EIP proposed above. I preferred to have a “2 dimensional address space” for the precompiled as I think it is a nice way to solve the problem since it does not impose any bound on the number of precompiled contracts one can define, and paves the way for a sustainable and elegant way (IMO of course) of enabling forks to modify the execution environment. The drawback of this approach, however, is - as you pointed out - that we need to add an opcode… I agree that the less code we write, the better, so I definitely agree that this is annoying (OTOH working with ranges of allocated addresses is trivial to implement). This EIP was built on top of EIP1109 however. Thus, the reason why we may want to add the opcode PRECOMPILEDCALL is to save gas when calling precompiled contracts. So assuming we want to add this new opcode, I thought we could add an extra arg to it to support custom precompiled execution.

