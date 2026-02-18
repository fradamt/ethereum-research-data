---
source: magicians
topic_id: 7014
title: "EIP-3855: PUSH0 instruction"
author: axic
date: "2021-09-06"
category: EIPs > EIPs core
tags: [evm, opcodes, shanghai-candidate]
url: https://ethereum-magicians.org/t/eip-3855-push0-instruction/7014
views: 32909
likes: 15
posts_count: 21
---

# EIP-3855: PUSH0 instruction

This is the discussion topic for



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-3855)





###



Introduce a new instruction which pushes the constant value 0 onto the stack

## Replies

**Arachnid** (2021-09-06):

Thank you for putting this forward! I was thinking about the need for a push0 instruction just the other day. Based on your stats, the impact of it is even larger than I expected!

Out of curiosity, did you collect stats on any other small numbers, such as 1, 2, and 32?

---

**axic** (2021-09-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> Out of curiosity, did you collect stats on any other small numbers, such as 1, 2, and 32?

We haven’t, but we could do that. Would take a couple of days though.

Instead of a special “PUSH 1”, I think something like `INC`/`DEC` would be a more interesting instruction, as that has multiple uses, especially around loops and rounding. I think 2 and 32 may be more common, though Solidity does rounding using both 31 and 32, which can also be optimised to a combination of shits.

---

**axic** (2021-09-07):

In the EIP we reason for this opcode:

> 0x5f means it is in a “contiguous” space with the rest of the PUSH implementations and potentially could share the implementation.

If this argument is not strong enough, then `0x5c` seems like a good alternative choice.

---

**Arachnid** (2021-09-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> Instead of a special “PUSH 1”, I think something like INC/DEC would be a more interesting instruction

So we can do `PUSH0 INC` instead of `PUSH1 1`? ![:laughing:](https://ethereum-magicians.org/images/emoji/twitter/laughing.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> I think 2 and 32 may be more common, though Solidity does rounding using both 31 and 32, which can also be optimised to a combination of shits.

A combination of whatnow?

---

**axic** (2021-09-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> axic:
>
>
> Instead of a special “PUSH 1”, I think something like INC/DEC would be a more interesting instruction

So we can do `PUSH0 INC` instead of `PUSH1 1`? ![:laughing:](https://ethereum-magicians.org/images/emoji/twitter/laughing.png?v=12)

Yes, isn’t that so much nicer?! ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

In fairness my hunch is that the constant 1 is mostly used for loops, in the form of `PUSH1 1 ADD`, so instead of that `INC` seems better. That is if we are willing to go into the direction of CISC. (`PUSH0` is still inspired by the constant 0 register in RISC machines.)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> axic:
>
>
> I think 2 and 32 may be more common, though Solidity does rounding using both 31 and 32, which can also be optimised to a combination of shits.

A combination of whatnow?

EVM hardcore mode ![:grimacing:](https://ethereum-magicians.org/images/emoji/twitter/grimacing.png?v=12)

Discounting the typo, I meant “combination of shifts and other bitwise instructions”.

---

**ricmoo** (2021-09-08):

Love the idea, but maybe we should use a different mnemonic, like IPUSH0 (for immediate) so that if we add others, we have room to grow? ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=10)

---

**hugo-dc** (2021-09-08):

I have posted the results here: https://gist.github.com/hugo-dc/1ca4682d60098282d7e499bdd0b01fca

Includes analysis of:

- Occurrences of PUSHn opcodes pushing the values 1, 2, 8, 31, and 32.
- Occurrences of pushing the specific values 1, 2, 8, 31, and 32, by any of the PUSH opcodes.
- A comparison between PUSH1 for the specific values 1, 2, 8, 31, and 32 vs any other values.

---

**axic** (2021-09-13):

My hunch is that the majority of cases using the constant 1 are for-loops. And likely a large number of the uses of the constant 32 is for such loops too, which operate on word sizes. (Though a significant number of occurrences should be for memory operations.)

And for these use cases I think this is a better direction to go:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> In fairness my hunch is that the constant 1 is mostly used for loops, in the form of PUSH1 1 ADD, so instead of that INC seems better. That is if we are willing to go into the direction of CISC. (PUSH0 is still inspired by the constant 0 register in RISC machines.)

---

**dankrad** (2021-09-17):

My intuition is that saving a 1 byte is a very marginal improvement and needs a pretty strong justification for actually reserving an opcode for it (which are after all limited)?

---

**axic** (2021-09-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dankrad/48/2962_2.png) dankrad:

> My intuition is that saving a 1 byte is a very marginal improvement

It is not *only* about saving 1 byte. The main motivation is runtime cost and avoiding that contracts use weird optimisations because they have no better option, and that optimisation limiting us in introducing other features.

Please read the motivation in the EIP and if it is fails to present convincing points, then we need to improve it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dankrad/48/2962_2.png) dankrad:

> and needs a pretty strong justification for actually reserving an opcode for it (which are after all limited)?

They are not limited, one can have extension bytes and two-byte opcodes, but even if someone mentally limits it to one byte, then we still have over 100 of them left.

Technically speaking all the `PUSHn` opcodes are not one byte opcodes ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**gcolvin** (2021-09-22):

These stats are taken from a [histogram](https://gist.github.com/gcolvin/ab8993d79d583076f3c6bc072e7ba0c6) of several thousand blocks at the end of last year’s chain.  One-byte pushes account for almost half of the pushes and over 10% of the instructions.  So from [@hugo-dc](/u/hugo-dc)’s numbers about 4% of instructions are `PUSH1 0`, and about 6% are a push of 1, 2, or 32.

| OP | Count | % |
| --- | --- | --- |
| All PUSH | 78,137,163 | 22.94% |
| PUSH1 | 37,886,773 | 11.12% |

---

**ekpyron** (2022-02-03):

FYI - this would save us some headache for solidity code generation - for once, in some situations we have to create stack balance between branches (we sometimes choose an awkward `codesize` for doing so…), and apart from that we constantly have to seek balance between keeping zeroes on stack or repushing them, both of which would be made easier, simpler and cleaner using a PUSH0. I’ve even had a draft for an optimizer step once that analysed which code paths are only executed prior to any external call and replaced zeroes with `returndatasize` in those paths - and considered something similar with `callvalue` for non-payable functions after their callvalue check - all of which is extremely awkward and it’d be nice to be able to drop crazy ideas like that with this EIP. Not that it’s crucial for us, but definitely a nice-to-have.

---

**wjmelements** (2022-02-09):

All PUSH, DUP, and SWAP operations should cost `base` gas. It’s weird that they don’t.

---

**axic** (2022-02-09):

We have some benchmarks about them, and it is not as clear cut. We do plan to share these with some recommendations, but I do not think this strictly is related to this EIP.

---

**poojaranjan** (2022-04-08):

PEEPanEIP-3855: PUSH0 instruction with [@axic](/u/axic) [@chfast](/u/chfast) [@hugo-dc](/u/hugo-dc)

  [![image](https://i.ytimg.com/vi/AIuJg6pkJxs/hqdefault.jpg)](https://www.youtube.com/watch?v=AIuJg6pkJxs)

---

**wjmelements** (2022-04-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> We have some benchmarks about them, and it is not as clear cut. We do plan to share these with some recommendations, but I do not think this strictly is related to this EIP.

It’s related to the motivation, because people are only using those opcodes instead of PUSH0 because they are cheaper.

---

**SKYBITDev3** (2023-09-07):

`PUSH0` has been enabled by default in Solidity since 0.8.20, but most blockchains still haven’t implemented it, causling “invalid opcode” error if developers use the latest compiler. So we’re stuck with using an older version.

The best we can do for the moment to work with the latest Solidity compiler is to set `evmVersion` to the previous version:

```auto
  solidity: {
    compilers: [
      {
        version: `0.8.21`,
        settings: {
          optimizer: {
            enabled: true,
            runs: 15000
          },
          evmVersion: `paris`
        }
      },
    ],
  },
```

Polygon announced just days ago that they’ve just implemented `PUSH0` on their zkEVM blockchain. I’ve tested the testnet and it works. zkEVM mainnet will work in 4 days. We need the many other blockchains to do so too.

---

**SKYBITDev3** (2023-09-18):

Hardhat v2.17.3 was released last week and reverted the default evmVersion back to `paris`.

They should have made such a change in a better way. I created an issue about it: [Automatic downgrade of default EVM version may not be welcome · Issue #4391 · NomicFoundation/hardhat · GitHub](https://github.com/NomicFoundation/hardhat/issues/4391)

I think it’s now best just to explicity set `evmVersion` in hardhat.config.js:

- evmVersion: 'shanghai' if it works on the blockchains you currently use
- evmVersion: 'paris' if you get the invalid opcode error

---

**radek** (2023-12-15):

Crafting the byte-exact CREATE3 factory I wonder whether there is any adoption dashboard of PUSH0 among chains?

---

**radek** (2023-12-15):

Do you plan any follow up on the stats? (incl. the new PUSH0)

It would be great to also see the stats of PUSH1 01 ADD combo wrt mentioned INC.

