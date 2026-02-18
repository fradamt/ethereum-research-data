---
source: magicians
topic_id: 7368
title: "EIP-4399: Supplant DIFFICULTY opcode with RANDOM"
author: mkalinin
date: "2021-10-30"
category: EIPs > EIPs core
tags: [eth1-eth2-merge]
url: https://ethereum-magicians.org/t/eip-4399-supplant-difficulty-opcode-with-random/7368
views: 34999
likes: 33
posts_count: 59
---

# EIP-4399: Supplant DIFFICULTY opcode with RANDOM

This is the discussion topic for EIP-4399: Supplant DIFFICULTY opcode with RANDOM.

This EIP proposes to supplant the `DIFFICULTY` opcode with the `RANDOM` opcode within the upgrade to PoS (a.k.a. the Merge)



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/4399)














####


      `master` ← `mkalinin:eip-4398`




          opened 06:45AM - 30 Oct 21 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/9/9a2c4f5dd7f75e3c0780f1fac63f71aa851a38ae.png)
            mkalinin](https://github.com/mkalinin)



          [+110
            -0](https://github.com/ethereum/EIPs/pull/4399/files)







A proposal to supplant the `DIFFICULTY` opcode with the `RANDOM` opcode during t[…](https://github.com/ethereum/EIPs/pull/4399)he upgrade to PoS (a.k.a. the Merge):
- enshrine the output of the beacon chain randomness beacon into the block header structure by supplanting the value of the deprecated `mixHash` field
- make the instruction with the number of the `DIFFICULTY` opcode return the value of the `mixHash` field
- rename the `mixHash` field and the `DIFFICULTY` opcode to `random` field and `RANDOM` opcode respectively

## Replies

**shemnon** (2021-11-08):

I think strong consideration should be given to adding a new `RANDOM` opcode instead of replacing the `DIFFICULTY` opcode.  When writing solidity contracts that use the difficulty and random field it would make it easier to audit when code may depend on the semantics of one over the other.

---

**mkalinin** (2021-11-08):

The changes introduced by this EIP are applied beginning with `TRANSITION_POS_BLOCK` (the first PoS block in the network). Beginning with `TRANSITION_POS_BLOCK`, the `DIFFICULTY` opcode will start to return `0` as per the deprecation of the `difficulty` field introduced by [EIP-3675](https://eips.ethereum.org/EIPS/eip-3675). The idea of preserving the `DIFFICULTY` instruction number for the new `RANDOM` opcode is in removing backwards incompatible change introduced by EIP-3675 with respect to existing smart contracts. Existing smart contracts will be able to use the EVM instruction with the same number as a source of randomness outputs disregarding the Merge has happened or not. Although, they will have to take in account the change in the size and the nature of these outputs post-Merge as it’s stated in the EIP.

---

**PatrickAlphaC** (2021-11-08):

This improvement seems like it will lead developers down a disingenuous path. As I understand it, the current method of randomness in ETH 2 is RANDAO (correct me if I’m wrong).

This would mean:

1. We are baking an application built on top of ETH into ETH itself (seems incorrect)
2. We are leaking a potential security vulnerability to developers. One hack of the DAO and every application using this randomness is potentially corrupted.
3. Additionally, we’ve seem hacks perivously of people using block.difficulty so changing the name I’m not sure makes sense on ETH 1 either. See a previous hack. Obviously, something like this is not even in consideration for ETH 1, since it would give the miners too much power.

Imagine someone being able to hack every single randomness-based application on ETH, lotteries, raffles, etc in a single go. Like a defi protocal hack times infinity. We are talking billions of dollars here.

Seems like a small change, but I think the naming convention would be drastically misleading, and a massive threat to the entire system.

This is my current understanding, but maybe I’m missing something.

---

**mkalinin** (2021-11-09):

The mechanism of accumulating randomness in the beacon chain is inspired by the RANDAO, there is no DAO that is used to obtain randomness seeds. The detailed explanation of how does it work in the beacon chain is [here](https://github.com/ethereum/annotated-spec/blob/master/phase0/beacon-chain.md#aside-randao-seeds-and-committee-generation). The power of each validator with respect to the randao computation is significantly limited on the beacon chain.

[Security Considerations](https://eips.ethereum.org/EIPS/eip-4399#security-considerations) section of the EIP states that the randomness output that is exposed by the `RANDOM` opcode becomes known to network participants when the parent block gets published, application developers MUST take this into consideration. In that regard the new opcode doesn’t differ much from the `DIFFICULTY` as `block.difficulty` is known to the miner of the block in advance and should there be an incentive the `difficulty` value could easily be shared or even sold.

---

**alexroan** (2021-11-09):

Since `DIFFICULTY` will not return anything meaningful in POS (there is no block difficulty in POS), contracts that use `block.difficulty` will break after the merge. Therefore, the `DIFFICULTY` opcode *has* to be changed to return something.

So the question becomes, “What do we replace it with?”. The EIP states that:

> Given prior analysis on the usage of DIFFICULTY, the value returned by the opcode mixed with other values is a common pattern used by smart contracts to obtain randomness.

In other words, given that pseudo-randomness generation is the most common use of `block.difficulty` in contracts, and pseudo-randomness is generated as part of the beacon chain, changing `DIFFICULTY` to return the `RANDOM` value is reasonable for backwards compatibility.

Furthermore, under “Security Considerations”, it states:

> The RANDOM opcode in the PoS network should be considered as a source of randomness output of a higher strength than the output provided by either the BLOCKHASH or the DIFFICULTY opcode in the PoW network.
>
>
> However, the randomness output returned by the RANDOM opcode is revealed to the network within the parent block.

So if anything, it’s slightly improving the pseudo-randomness generated in contracts using `block.difficulty`. However, it’s still not a true source of randomness in much the same way as `block.difficulty` is not.

---

**PatrickAlphaC** (2021-11-12):

Thanks for the context Alex, and thanks for the info [@mkalinin](/u/mkalinin).

It sounds like `PRANDOM` would be a better opcode then since this is a pseudo-randomness method. I think having the opcode be purely `RANDOM` would be incredibly dangerous.

I’ve seen enough hacks from projects thinking that the difficulty is a secure method of randomness, and I’d rather not bake a bad practice into Ethereum.

Ideally, we choose a different name entirely.

---

**mkalinin** (2021-11-15):

I don’t think that adding a `P` prefix to the name of this opcode changes anything. Careful implementer like you are would read and grok all the implications before using a thing. Others would rely on `DIFFICULTY` and `BLOCKHASH` as a source of randomness (thinking that they are strong enough) despite of warnings made here and there. Additionally, is there a system that uses true randomness? It seems like pseudo randomness is used in most of the cases.

---

**PatrickAlphaC** (2021-11-16):

“Careful implementer like you”

I don’t think we should be implementing conventions that make things more complicated. Developer experience is death by 1,000 cuts, and this is one of those things that could be easily avoided.

“Oh wait, the `RANDOM` opcode isn’t actually random?”

I’d really rather us not introduce concepts that are confusing.

And yes, there are systems that use True randomness like [Chainlink VRF](https://docs.chain.link/docs/chainlink-vrf/).

---

**mkalinin** (2021-11-17):

VRF is pseudo-random by its definition. In the beacon chain what is called `randao_reveal` is basically the output of VRF. And the output that is proposed to be exposed in the EVM is a mix of VRF outputs of different oracles for millions of slots starting from genesis.

There are two weaknesses. 1) validator may skip its reveal by refusing to propose a block and reduce the strength of the output by a bit 2) privacy issue, `randao_reveal` hence accumulated randomness output becomes known to the validator in a slight advance. These two weaknesses are presented in Chainlink VRF as well.

There is no issue with respect to the pseudo-random nature of the output. And I don’t understand how `P` prefix or any other prefixes would emphasise the existing weaknesses. They should be written in the spec and learned by developers who is going to use it.

---

**PatrickAlphaC** (2021-11-17):

> They should be written in the spec and learned by developers who is going to use it.

I think we will just disagree on that point and see what others think. To me, it seems naming something that we know to be misleading is counterproductive.

As per your two points against Chainlink VRF, this may be true in the current implementation, but new versions are being worked on, including [threshold signatures](https://blog.chain.link/threshold-signatures-in-chainlink/) which will remove these weaknesses, and other similar devices could also be created that are better versions of randomness for smart contracts than those built into the ETH system.

---

**haltman-at** (2021-12-03):

So, I’m wondering what disassemblers and debugging tools should report on seeing this opcode.  This isn’t the first time an opcode has been renamed, but it’s the first time it’s been renamed to something with such a different meaning.  It’s like, are these tools now going to have to be aware of what hardfork a given contract was written for…?

---

**poojaranjan** (2022-01-14):

An overview of the proposal by [@mkalinin](/u/mkalinin)

[EIP-4399: Supplant DIFFICULTY opcode with RANDOM](https://youtu.be/wwfOqmCbPNU)

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/0/01cf54a9a73f51f87ec98ac4c524e343d2f91177.jpeg)](https://www.youtube.com/watch?v=wwfOqmCbPNU)

---

**haltman-at** (2022-01-21):

Oh, here’s a possibility: What if a duplicate opcode were added?  That could solve the tooling issue.

Suppose that 0x44 is changed from returning difficulty to returning random, but also, 0x49 were added which would have exactly the same function.  Then we could have 0x49 be called `RANDOM`, while 0x44 would continue to be called `DIFFICULTY` (even though it would actually also return random), and post-merge compilers would make a point to use 0x49 for random.

I’d like to propose this as a solution to the problem.

---

**a2468834** (2022-01-25):

I agree with the idea that adding another opcode `RANDOM` rather removing/replacing `DIFFICULTY`.

(Keeping compiler/opcode set backward compatible is important!)

However according to EIP-3675, after “the merge” phase, the block field `difficulty` should return a constant value `0`. So, I believe that letting only `RANDOM` returns (pseudo-) random numbers could be more suitable.

---

**mkalinin** (2022-02-17):

There is an RFC to reconsider the opcode name and probably use anything else than `RANDOM`:

Beacon chain RANDAO mixes are much less biasable than `difficulty` and `blockHash` values in PoW network. But they are still biasable up to a limited extent which is expanded in the [Security Considerations](https://eips.ethereum.org/EIPS/eip-4399#security-considerations) section of the EIP.

One of nice to have things limiting biasability is to have a `RANDOM(n)` instruction, where `n` is a *slot* number, which returns a RANDAO mix produced in a specified slot disregarding whether this slot is empty or not (if empty, RANDAO mix from latest non-empty slot is returned). It prevents an attack where proposer/builder pushes back transaction that rolls the dice until a mix with desired outcome is met. Security properties of return value of this instruction may be hardened up by returning a recent VDF result.

So, we might want `RANDOM` instruction to have *a parameter* in the future and this is where the `RANDOM` name proposed in EIP-4399 may become a source of confusion.

Options:

1. Keep DIFFICULTY -> RANDOM renaming, and name the future opcode if that need be SECURE_RANDOM(n) or RANDOM2(n) (the latter is a sort of a joke as it looks terrible). Or any reserve any other name for the future – we have a plenty of time for this
2. Rename DIFFICULTY -> ?, we need to define ? in the next few days. RANDOM stays reserved for the future
3. Keep DIFFICULTY to reflect how difficult it is to pick up a name

---

**MicahZoltu** (2022-02-17):

I recommend something like `BARELY_RANDOM`, `RANDOMISH`, `SORTA_RANDOM`, etc. for the colloquial rename of `DIFFICULTY`.  The reason for this is because it is nearly impossible to securely use this opcode as a source of randomness in any real-world setting, and that should be made very clear to any developer.  If we introduce `RANDOM(n)` in the future like [@mkalinin](/u/mkalinin) suggests, then we can have something that *can* be secure if used appropriately (especially when combined with VDFs).

---

**yperbasis** (2022-02-17):

`WEAK_RANDOM` perhaps?

---

**MicahZoltu** (2022-02-17):

This is certainly better than `RANDOM`, but I do worry that it is used too frequently in computer science to just mean “pseudo-random” which these days means “pretty good random, but not as good as radioactive decay”.  In this case what we have is *far far far* worse than that.

---

**axic** (2022-02-17):

Why not just keep it as `DIFFICULTY` and call it a day?

---

**MicahZoltu** (2022-02-17):

I think keeping `DIFFICULTY` is a reasonable option, though I do worry that people will colloquially name it `RANDOM` if we don’t give them an alternative.


*(38 more replies not shown)*
