---
source: magicians
topic_id: 4550
title: "EIP-2677: Limit size of initcode"
author: axic
date: "2020-08-28"
category: EIPs
tags: [evm, core-eips]
url: https://ethereum-magicians.org/t/eip-2677-limit-size-of-initcode/4550
views: 3705
likes: 0
posts_count: 10
---

# EIP-2677: Limit size of initcode

Discussion topic for

https://eips.ethereum.org/EIPS/eip-2677

This was suggested during the discussion of EIP-2315: [EIP-2315 "Simple Subroutines for the EVM" - Analysis - #35 by chfast](https://ethereum-magicians.org/t/eip-2315-simple-subroutines-for-the-evm-analysis/4229/35)

> Enforce a maximum size limit ( max_initcode_size ) for  initcode . If the size of  initcode  exceeds  max_initcode_size , then contract creation fails with an out of gas error.
>
>
> Since EIP-170 was implemented, there has been a size limit of  24576  ( 0x6000 ) on contract code. We propose to also limit the size of executable code to  2x  the above limit, i.e.  49152  ( 0xc000 ).
>
>
> This also leads to two nice properties:
>
>
> instruction offset in code fits 16-bit value,
> code size fits 16-bit value.

## Replies

**esaulpaugh** (2020-08-29):

Is the rationale that this will reduce the worst-case resource consumption of `initcode`, enabling a price reduction? Or is it that `initcode` is priced too low already and this change will bring resource consumption in line with the current price?

---

**axic** (2020-09-06):

Ensuring a limit for init code makes analysis of it easier. While the lack of this limit may not be a problem currently, it makes the introduction of new EVM features harder. A good example is EIP-2315.

---

**esaulpaugh** (2020-09-07):

hmm, current stack width is 256 bits, but I guess the new return stack will be slimmer, only operating on program counters and not data

---

**MrChico** (2021-03-18):

If the cost of the jumpdest analysis scales linearly with the codesize, wouldn’t it make more sense to charge per initcode byte, instead of just imposing a hard cap?

Currently we charge 6 gas per 32 bytes for the keccak cost of CREATE2, maybe this can be added to CREATE as well? Possible wtih an increase in the per byte cost to make jumpdest analysis attacks unfeasible.

---

**chriseth** (2021-04-06):

Can you please provide an explanation in the EIP document that tells why the same effects cannot be achieved by charging a cost per byte, as @McChico proposes? I would find such a mechanism much more natural. Of course, it has to be partly charged per execution instead of per deployment, but isn’t that where we want to go anyway?

---

**holiman** (2021-04-16):

Sorry,I missed this. Yes, I totally agree that that mecanism would work to, and arguably be even *better*, since it would be more accurate.

My reason for proposing a hardcap is simply that I think it’s a more minimal change with less chances of leading to consensus errors.

If we didn’t already have a hard-cap on deployed-code size, then I would not have suggested this (otherwise quite hacky) solution.

---

**shemnon** (2021-04-30):

Would it be possible to limit executable code to `0xc000` or lower instead of the entire initdata being capped at 48k?  Allowing data to exist beyond the execution cap?  i.e. the PC will not jump past `0xc000` (or `0x6000` to match deployed contract sizes) but the initcode can CODECOPY well past the execution limit, for example to CREATE or CREATE2 multiple contracts based on call args.

The reason I ask is I’ve seen some contracts that will deploy a notable amount of “satellite” contracts and would benefit from atomic deployment. It doesn’t take many contracts before you are at the 24k limit for a factory contract and have to move into initcode for deployments.

---

**holiman** (2021-05-06):

Myeah maybe. Although, now that it’s definitely not slated for london, we have some more time on our hands. I might run a chain analysis to see what the largest (successful) execution ever was

---

**axic** (2021-09-07):

A new proposal has been pushed which introduces both a hard cap and a charge:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png)
    [EIP-3860: Limit and meter initcode](https://ethereum-magicians.org/t/eip-3860-limit-and-meter-initcode/7018) [Core EIPs](/c/eips/core-eips/35)



> This is the discussion topic for

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrchico/48/1427_2.png) MrChico:

> If the cost of the jumpdest analysis scales linearly with the codesize, wouldn’t it make more sense to charge per initcode byte, instead of just imposing a hard cap?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chriseth/48/2111_2.png) chriseth:

> Can you please provide an explanation in the EIP document that tells why the same effects cannot be achieved by charging a cost per byte, as @McChico proposes?

The answer to this can be found in the rationale of the new proposal. In short, having a hard cap helps in crafting worst case scenarios to measure the cost against.

