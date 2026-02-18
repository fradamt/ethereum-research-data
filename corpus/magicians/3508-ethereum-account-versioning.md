---
source: magicians
topic_id: 3508
title: Ethereum account versioning
author: axic
date: "2019-07-27"
category: EIPs > EIPs core
tags: [accounts, versioning]
url: https://ethereum-magicians.org/t/ethereum-account-versioning/3508
views: 4189
likes: 5
posts_count: 14
---

# Ethereum account versioning

In the past few months account versioning was a topic of importance due to EIP-615 requiring it. Additionally it could wall off other changes (such as gas changes) to minimize protocol update effects on existing contracts.

There have been a number of proposals for account versioning: [EIP-1702](http://eips.ethereum.org/EIPS/eip-1702), [EIP-1707](https://github.com/ethereum/EIPs/pull/1707), [EIP-1891](https://github.com/ethereum/EIPs/pull/1891) as well two auxiliary EIPs [EIP-2138](https://github.com/ethereum/EIPs/pull/2138) and [EIP-2139](https://github.com/ethereum/EIPs/pull/2139). All of these proposals were made by [@sorpaas](/u/sorpaas).

EIP-1702 was the most reviewed option.

Some of discussion took place on [EVM instruction set versioning](https://ethereum-magicians.org/t/evm-instruction-set-versioning/2286), [EIP-1702: Generalized Account Versioning Scheme · Issue #2 · sorpaas/EIPs · GitHub](https://github.com/sorpaas/EIPs/issues/2) and [EIP-1891: Contract-based Account Versioning · Issue #6 · sorpaas/EIPs · GitHub](https://github.com/sorpaas/EIPs/issues/6), but mostly it was discussed on the AllCoreDevs gitter channel.

Created this topic here to have a single place to discuss versioning, because tracking all these places became a burden, at least to me.

## Replies

**axic** (2019-07-27):

My personal opinion is that account versioning is useful, but it has to be used with great care.

I do see a use case

- to distinguish between EVM and other bytecode (such as Wasm) or
- to have different EVM versions when new opcodes are introduced

However locking gas changes into new versions is a double edged sword. On the outset it seems to lock gas changes to new contracts without affecting old ones, but having accounts of different versions interact with each other can easily complicate matters a lot.

Two more issues regarding gas changes locked behind versioning:

- a reduction of costs cannot be utilised by existing contracts, prompting users to redeploy them, which contributes to state bloat
- an increase of costs would not affect existing contracts, minimising the intended effect, potentially giving very limited results (one example is repricing SLOAD as per EIP-1884 to reflect the actual workload)

---

**shemnon** (2019-07-28):

One case where I see account versioning as a “must do” is when backwards incompatible changes are being introduced.  I would almost suggest this is the only time a new account version should be considered for introduction.

I see a few places where this would be warranted under the “versioning required” standard

- introduction of new contract validation rules.
- prohibition of previously allowed opcodes or constructs

such as dynamic jump or dynamic jump from a non-fixed stack value
- such as invalid opcodes, like you might find in data sections.

introduction of a new bytecode, such as eWASM

However we may want to consider “horse trading” version upgrades, such as ones that significantly reduce prices on one set of operations at the cost of raising other sets of operations, such as cheaper precompiles for extremely expensive memory operations.  I’m not providing any specific suggestions but am putting it out there as a tool that is available.

---

**AntoineRondelet** (2019-09-03):

I can see in EIP-1702 that no account versioning is scheduled for the precompiled contracts.

See Section `Precompiled Contract and Externally-owned Address` of [EIP-1702: Generalized Account Versioning Scheme](https://eips.ethereum.org/EIPS/eip-1702)

> Precompiled contracts and externally-owned addresses do not have version

Why such a decision has been taken?

I see several benefits to have version numbers for the precompiled contracts.

1. It could allow forks of Ethereum to define their set of precompiled without interfering with the addressing scheme used on the main chain (and without needing to allocate/reserve a range of addresses of precompiled for “forks’ custom precompiled” which IMHO does not provide an elegant solution). That way, the precompiled version would always be 0 on the main chain, while it could be set to be =/= 0 on forks so that the same address can be used to call a different/custom precompiled. This makes it easier for forks of Ethereum to define their precompiled and makes it trivial to keep a forked client in sync with the parent project.
2. I also see a benefit of using precompiled versioning on main chain as it could be used to introduce newer versions of the precompiled, and could thus be used to provide backward compatibility. Eg: We could define a new snark/pairing friendly curve on Ethereum and introduce the corresponding precompiled contracts as an upgraded version of the current bn256 precompiled. We know that the bn256 package used on Ethereum was initially claiming to provide 128 bits of security. However, recent work (Kim–Barbulescu variant of the Number Field Sieve to compute discrete logarithms in finite fields | ellipticnews) suggest this is not the case anymore. For this reason, it would make sense to either replace the bn precompiled by precompiled for another curve (BLS12-381?) but this would break backward compatibility (I think it’s a good thing actually), or we could add a new version for the point addition, scalar multiplication and pairing check precompiled such that arithmetic is done over the new curve. As the set of precompiled grows (blake2b has just been introduced which is great) and as new cryptographic primitives and curves are added I think we should think about the event in which new attacks on these are published which could affect the security promises - or even worst - break some of these. For this reason, supporting versioning would make sense I think.

Hopefully this makes sense, and please let me know if I missed something!

[EDIT] I proposed an EIP to address some of the matters mentioned above. A thread is dedicated to discuss it here: [EIP-2274: Multiple address spaces for Precompiled contracts](https://ethereum-magicians.org/t/eip-2274-multiple-addresses-range-for-precompiled-contracts/3652) happy to discuss this further ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**AntoineRondelet** (2019-09-11):

Further to the comment above, I’d be keen to understand better some of the design choices made in EIP1702. [@sorpaas](/u/sorpaas), did I understand correctly that you didn’t plan to support precompiled versionning in EIP1702? If so, would you mind exposing the reason behind this choice? Thanks in advance for your help ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**sorpaas** (2019-09-13):

I was writing the spec under the assumption that all contracts having a global view of precompiled contracts, and adding new precompiles or changing existing precompiles is basically an irregular state change. That’s why in 1702 they don’t have versions.

I do see your argument. I’m fine either way. If we make precompiles have versions, then it’s basically treating them as EVM internal implementations that do not query state at all. However, there’s a small inconsistency in that you can call precompiles directly from a transaction, and it indeed has side effect because the gas costs are different.

---

**AntoineRondelet** (2019-09-17):

I see, thanks very much for your input.

As precompiled contracts extend the instruction set of the EVM, I wanted to enable different “libraries of precompiled contracts”. Those defined on mainnet and those which can be defined by forks. To that end, I wrote EIP-2274 that extends EIP-1109 (that I stumbled upon a few days ago) while following the idea mentioned in my comment above. It may be a way to stick to the EIP as you wrote it while having different set of precompiled contracts.

I’m not sure, though, I fully understood what you meant by:

> However, there’s a small inconsistency in that you can call precompiles directly from a transaction, and it indeed has side effect because the gas costs are different.

If you call a precompiled from a deployed contract, you’ll pay the gas cost of CALL and of the precompiled. However, if you call the precompiled directly via a tx you should only pay only the gas cost of the precompiled contract (in both case you’d also pay for the base tx fee of 21k gas or so). Is that correct and is that what you were referring to as the “side effect”? If so, why is this problematic?

---

**sorpaas** (2019-10-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/antoinerondelet/48/2210_2.png) AntoineRondelet:

> However, if you call the precompiled directly via a tx you should only pay only the gas cost of the precompiled contract (in both case you’d also pay for the base tx fee of 21k gas or so).

Yeah, and I consider that to be a side effect of precompiled. When doing a tx directly, the address or contract we’re calling can be said to be on the “global view”. If any effect of the precompiles (the return value, additional gas cost) is visible, then precompiles can be said to be on the global view.

---

**tjayrush** (2019-11-23):

Can some change the topic of this pos to “Account Versioning”? It’s confusing to those of us who are interested in Accounting. Thanks.

---

**axic** (2019-11-23):

Oh, I have just noticed the typo (“Accounting”), haha.

---

**sorpaas** (2020-02-15):

[@axic](/u/axic) The title is still not yet fixed.

---

**jpitts** (2020-02-15):

It might be Discourse software does not allow [@axic](/u/axic) to change it after submitting the topic. I went ahead and updated the title.

---

**axic** (2021-04-28):

It was not mentioned in this topic, but a related discussion took place here:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png)
    [EIP-2348: Validated EVM Contracts](https://ethereum-magicians.org/t/eip-2348-validated-evm-contracts/3756) [EIPs](/c/eips/5)



> Discussion topic for
>
>
> A set of contract markers and validation rules relating to those markers is proposed. These
> validation rules enable forwards compatible evolution of EVM contracts and provide some assurances
> to Ethereum clients allowing them to disable some runtime verification steps by moving these
> validations to the deployment phase.

And speaking of validation, [EIP-615](https://eips.ethereum.org/EIPS/eip-615) also proposed code validation.

---

**axic** (2021-06-09):

Another proposal introducing a variant of code versioning is discussed here:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png)
    [EVM Object Format (EOF)](https://ethereum-magicians.org/t/evm-object-format-eof/5727) [EIPs](/c/eips/5)



> Last week I have shared a document on the Eth R&D discord explaining some background on why some EVM changes are hard and motivation for improving the situation:
>
> It also suggests a container format for EVM, which would enable further improvements, such as removing jumpdests, moving to static jumps, etc. While the document does not aim to provide a final, implementable solution, it is a good one for discussions.

