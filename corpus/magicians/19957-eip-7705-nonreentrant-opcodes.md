---
source: magicians
topic_id: 19957
title: "EIP-7705: nonreentrant opcodes"
author: charles-cooper
date: "2024-05-09"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7705-nonreentrant-opcodes/19957
views: 1445
likes: 5
posts_count: 17
---

# EIP-7705: nonreentrant opcodes

discussion for [EIP for reentrancy protection opcodes by charles-cooper · Pull Request #8543 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8543)

## Replies

**xinbenlv** (2024-05-09):

Yet to be convinced the benefit outweigh the cost and increased complication to have a EVM opcode level support to avoid reentry.

---

**charles-cooper** (2024-05-09):

Then please, give me another way to prevent it.

EIP-7609 and EIP-5920 were both dropped from inclusion for Pectra. I am starting to think core devs don’t want to help users prevent reentrancy.

---

**xinbenlv** (2024-05-09):

I am not a core dev.

I just happen to believe that if reentry avoidance shall be done at the level of smart contract, and shall be done by carefully structure state change. I think [@Amxx](/u/amxx) or [@frangio](/u/frangio) shared similar views, both are not core dev either.

---

**charles-cooper** (2024-05-09):

That’s fine, but not everybody thinks like that. Structuring your contract like that is more difficult to get right (as evidenced by this rather impressive list of reentrancy attacks: [GitHub - pcaversaccio/reentrancy-attacks: A chronological and (hopefully) complete list of reentrancy attacks to date.](https://github.com/pcaversaccio/reentrancy-attacks)). It’s harder to audit, and harder to maintain (make changes without introducing bugs).

Let me put it another way, if the EVM came with reentrancy protection to begin with, would you still think that developers should use CEI? Would you want to throw out the opcode in the name of simplicity and tell developers “just use CEI”?

By the way, this EIP is completely unnecessary if the cost of transient storage can come down, as I proposed in EIP-7609. I think EIP-7609 is a much more elegant solution and it also addresses the deeper problem (which is that transient storage is overpriced). But it was not included in Petra without any feedback or discussion, so I want to propose an alternative method to prevent reentrancy.

---

**xinbenlv** (2024-05-09):

Thank you for sharing the context.

I agree with you that Reentry is a huge security problem to solve, and;

I agree with you that EIP-7609 is more preferable, which is more general and elegant compare to this proposal. I will be curious to learn more about rationale that EIP-7609 was not prioritized. Let me do more digging and come back.

---

**pcaversaccio** (2024-05-09):

I do support this proposal. One may argue that reentrancy is a feature and not a bug (e.g. for applications like flash loans or DeFi/DEX aggregators like 1inch), but the real facts are clear: reentrancy attacks are among the top 3 attack vectors in the smart contract protocol space. As a reminder, a reentrancy attack almost destroyed Ethereum in 2016. In fact, the last 8 years have shown us that we have not become any smarter when it comes to securing reentrancy attacks. On the contrary, reentrancy can happen in a very hidden ways nowadays due to the increased complexity of protocols and requires a very deep understanding of the context which 90% of developers probably don’t have. We should add guard rails that compilers can reuse to create safer bytecode. Thus, I personally believe that the EVM should strongly incentivise the development of *secure* applications, as its (=EVM) success ultimately depends on the use of opcodes in the real world. Let’s build a VM suited not only for the 5% top developers but also for the remaining 95%.

---

**wjmelements** (2024-05-09):

Re-entrancy was a big reason for TSTORE/TLOAD. Those opcodes are overpriced. If you can do a study that demonstrates their execution cost is too large relative to other opcodes that would be productive.

---

**charles-cooper** (2024-05-09):

I already did it. It’s the first comment in the discussion for EIP-7609: [EIP-7609 reduce transient storage pricing - #2 by charles-cooper](https://ethereum-magicians.org/t/eip-7609-reduce-transient-storage-pricing/18435/2)

---

**wjmelements** (2024-05-09):

Cool. I’m more supportive of a gas reduction than new opcodes.

Be sure to measure revert cost too.

---

**radek** (2024-05-13):

I agree with [@pcaversaccio](/u/pcaversaccio) that reentrancy needs to be addressed.

IMO ideally within the dispatcher phase (or earlier).

I do not like the following reasoning and creating new opcodes due to the lack of fluidity of the standardization process.

> But it (EIP7609) was not included in Petra without any feedback or discussion, so I want to propose an alternative method to prevent reentrancy.

Anyway, if this EIP is further favored I guess 1 opcode design should be preferable. I would rather call that `REENTRANCY_GUARD` for clarity. With 1 immediate byte:

- 0 → removes guard flag
- 1 → sets guard flag
- 128 → pushes to stack the guard flag of the contract’s address on the stack 1

Reading the flag to stack is for cases, when initiating contract wants to check the other contract is callable (as the revert does not indicate the reentrancy reason).

---

**wjmelements** (2024-05-14):

Immediate parameters are generally frowned upon. They require new EVM versions (eg EOF) because of backwards compatibility with jump validity. So additional opcodes and stack parameters are better.

I don’t think being able to detect if another contract is blocking re-entrancy is that useful. I’ve never wanted to do that. It seems useful to hackers though.

---

**radek** (2024-05-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> They require new EVM versions (eg EOF) because of backwards compatibility with jump validity.

Strange, as PUSHx literally have immediate parameter.

> So additional opcodes and stack parameters are better.

It would be ideal if consensus on architectural principles was written somewhere.

Eg.:

- Preference of the least amount of opcodes (as can be understood from some EIP discussions)
- Preference of the least amount of extra implemented precompiles (ref. a recent EIP by Vitalik)
- Preference of onchain code reusal (strangely does not seem to be wrt CALL cost)
- …

*Apologies for OT, but EIP-7609 TSTORE/TLOAD approach would be a clear winner if there was a strong consensus on the principle of least amount of opcodes.*

---

**wjmelements** (2024-05-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/radek/48/16714_2.png) radek:

> Strange, as PUSHx literally have immediate parameter.

It will not be available for legacy EVM, only EOF.

---

**wjmelements** (2024-05-15):

[@radek](/u/radek) I was mistaken about what you were referring to. PUSHx are the only immediate-instructions allowed in legacy EVM. EOF will add more but new versions will be required for each one. The basic reason is that jumpdest validity must not change for existing contracts.

I thought you were referring to eip-663.



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-663)





###



Introduce additional instructions for manipulating the stack which allow accessing the stack at higher depths

---

**radek** (2024-05-15):

> I was mistaken about what you were referring to. PUSHx are the only immediate-instructions allowed in legacy EVM.

I appreciate that you corrected your statement. This is a great  example of the Ethereum community culture. Thanks.

Is there any reference to the architectural principles I mentioned?

That would help further discussions…

> The basic reason is that jumpdest validity must not change for existing contracts.

If I understand that correctly the concern is that the immediate parameter could  have the 0x5B byte (JUMPDEST opcode) in itself.

---

**wjmelements** (2024-05-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/radek/48/16714_2.png) radek:

> If I understand that correctly the concern is that the immediate parameter could have the 0x5B byte (JUMPDEST opcode) in itself.

That’s right. It has mattered for some of the contracts I’ve written but it’s a non-issue for most contracts out there.

