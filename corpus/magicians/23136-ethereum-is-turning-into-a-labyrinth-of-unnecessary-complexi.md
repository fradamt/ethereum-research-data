---
source: magicians
topic_id: 23136
title: Ethereum is turning into a labyrinth of unnecessary complexity with EOF - Let's reconsider EOF
author: pcaversaccio
date: "2025-03-13"
category: EIPs
tags: [eof]
url: https://ethereum-magicians.org/t/ethereum-is-turning-into-a-labyrinth-of-unnecessary-complexity-with-eof-lets-reconsider-eof/23136
views: 3448
likes: 160
posts_count: 69
---

# Ethereum is turning into a labyrinth of unnecessary complexity with EOF - Let's reconsider EOF

[EOF](https://eips.ethereum.org/EIPS/eip-7692) is extremely complex. It introduces two new contract creation semantics ([EOFCREATE](https://eips.ethereum.org/EIPS/eip-7620) and [TXCREATE](https://eips.ethereum.org/EIPS/eip-7698)), removes and adds over a dozen opcodes. Furthermore, the purported benefits don’t require EOF, they could be implemented in the current EVM in much less invasive ways. Let’s explore these:

- Reducing compiler complexity:

EIP-663 opcodes allow access deeper in the data stack. This is useful, but not a requirement for modern compilers – all modern compilers know how to implement stack/register spilling. This is a shortcoming of solc, not of the underlying VM. (As an example, Vyper does not have stack-too-deep as a result of compiler and language design.)

Improving bytecode size due to `JUMPDEST` removal:

- We could just remove JUMPDESTs.

Makes it easier to upgrade the EVM, e.g. adding or removing opcodes:

- We can add validation rules to the existing EVM. Bytecodes of contracts can be analysed at creation, and we can disallow deploying contracts with specific opcodes - or change semantics thereof - if they are deployed after a given fork_blocknum.

Allows for opcodes with immediates:

- Again, we don’t need to change semantics of existing contracts. Rather, validate and apply updated semantics to newly created contracts.

Remove gas introspection:

- You can just add the EIP-7069 (CALL2, etc) opcodes, which don’t access gas.
- Validate that code does not include the GAS opcode.
- Because of the 63/64ths rule, contract behaviour depends on gasleft anyways (subcalls can OOG without the outer contract OOG).

Remove code introspection:

- You can add validation rules to legacy EVM to remove the relevant opcodes. New creation opcodes would need to be introduced, but it wouldn’t need to be shipped at the same time as all these other changes.

Remove dynamic jumps:

- This can also be addressed simply by updating pricing and providing a carveout for PUSH2 JUMP(I) in the gas schedule.

Subroutines:

- There are existing, less invasive proposals to the EVM which include subroutines and give preference to static jumps.

Address space expansion:

- Can change semantics of existing opcodes (like BALANCE) to not zero the top 12 bytes of the address, again via contract versioning.

Remove `codesize` limits:

- We can just do that, since initcode is metered via EIP-3860.

ZK-friendliness

- EOF is purportedly more ZK-friendly. However, we have not seen arguments for why this is a hard requirement.

In other words, all the benefits of EOF can be introduced in more piecemeal, less invasive updates to the EVM.

Meanwhile, the complexities of EOF cannot be ignored:

- Legacy EVM needs to be maintained, probably indefinitely.
- Tooling needs to support EOF. This requires coordination and effort across many different teams.
- Risk of vulnerabilities due to complexity. For instance, send() and transfer() now allow reentrancy. This was not noticed until a month before Osaka was scheduled to be finalised, even though EOF has been in development for nearly 4 years.
- Related to that, EOF has been a moving target: EOF is looking to get shipped even though parts of the spec keep changing, making it difficult for compiler and app devs to review the entire package.
- Work to target the new format for compilers and app devs.
- EVM contracts get much more complicated due to headers. An empty contract is now at least 15 bytes.
- Bytecode size tradeoffs. For instance, subroutines cost several bytes just to declare, which penalises contracts with many, small subroutines.

---

**Update:** I have co-authored a new and longer EOF deep-dive: [EOF: When Complexity Outweighs Necessity](https://hackmd.io/@pcaversaccio/eof-when-complexity-outweighs-necessity). We break down its supposed benefits and argue they’re more “nice-to-haves” than essential upgrades. Instead of adding complexity, we highlight cleaner, less disruptive solutions that achieve the same goals. EOF’s objectives are solid—but there’s a smarter way to get there.

Please give it a read and let us know your thoughts in this thread.

## Replies

**shemnon** (2025-03-13):

I’ll spend the time to give a more detailed response later this week, but I would like to point out that all of these questions were already asked and answered as a part of ACD 192 9 months ago.  I do not see any new concerns raised here.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png)

      [All Core Devs - Execution (ACDE) #192, July 18 2024](https://ethereum-magicians.org/t/all-core-devs-execution-acde-192-july-18-2024/20565) [Protocol Calls & happenings](/c/protocol-calls/63)




> Agenda
> Execution Layer Meeting 192 · Issue #1098 · ethereum/pm · GitHub
> Moderator: @timbeiko
> Summary
>
>
> Recording
> https://www.youtube.com/live/kL58hvM0E68?t=308s
> Additional info
>
> Notes: Ethereum All Core Developers Execution Call #192 Writeup | Galaxy by @Christine_dkim
> EOF: Why I am against EOF in Pectra – MariusVanDerWijden by @MariusVanDerWijden
> RIP7212: Brief History and Current Situation of RIP-7212 by @ulerdogan

---

**xrchz** (2025-03-13):

Perhaps as a meta point there seems to be disagreement about whether major EVM changes are desirable in general (including in the notes from the call you mentioned). I would argue that a stable VM, on which people can invest in building up excellent tooling and apps with confidence, is much more valuable than the ability to evolve the VM to compete with other VMs, since this has the cost of scaring away investment in something that’s gonna potentially change in the future. (I’m speaking in part here as someone who becomes much more hesitant about my investments in the EVM, both as user and dev, when I see that stability of the VM isn’t being prioritised.)

---

**mitche50** (2025-03-13):

I just want to echo this sentiment - As someone who has been building on the EVM for a long time now, all of these changes adding in unnecessary complexity and changing assumptions is a huge turn off for developers building on the supposed “world computer”.

---

**bbjubjub** (2025-03-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> Makes it easier to upgrade the EVM, e.g. adding or removing opcodes:
>
>
> We can add validation rules to the existing EVM. Bytecodes of contracts can be analysed at creation, and we can disallow deploying contracts with specific opcodes - or change semantics thereof - if they are deployed after a given fork_blocknum.

IMHO tracking deployment height and applying different semantics to a contract on that basis has drawbacks. It means that if you have deployment transactions, they might produce different results if you cross the hardfork boundary. Although this is technically true already with gas schedule changes, this seems much more likely to cause issues. This is also true if you work in an Osaka environment and then switch networks. And we haven’t addressed contracts creating contracts which could also be messy. By contrast, versioning seems more elegant and allows explicit opt-in.

That does not mean that *all* of EOFv1 belongs as a bundle together. In fact it would be possible to introduce versioning on its own and nothing else, but there would be no incentive to upgrade. If we want a carrot, a good choice would be stack validation + relative jumps, which enable optimizations that could enable a gas discount. This pulls in roughly half of the EOF EIPs, which constitute a more minimal set and exclude some of the more problematic changes like gas inobservability. This may be inaccurate because I haven’t been following EOF closely, but the message is: versioning per se uniquely unlocks a more efficient EVM afaict.

---

**xrchz** (2025-03-13):

If something has to be included, I think I could get behind adding relative jumps (although not yet convinced they are really worth it).

I don’t believe stack validation needs changed semantics. It can be done already via analysis of status-quo EVM code. Is there reason to think otherwise?

I take this opportunity to call out another pattern I have observed in discussion of EOF so far: that proponents seem keen to equivocate between “EOF enables X” and “X requires EOF”, when these are not in fact logically equivalent statements. I hope readers of these discussions take heed that demonstrating “Y enables X” is much easier than proving that “X requires Y”, but it’s the latter that we need proven before biting the bullet on adopting Y (assuming X is highly desired).

Thanks for your point about versioning. On that point my previous comment about stability still feels relevant: I would rather not make plans (like versioning) that make major EVM upgrades easier, because I would rather not have major EVM upgrades and for the benefits of this to be appreciated.

---

**duncancmt** (2025-03-14):

As I stated [over here](https://ethereum-magicians.org/t/eip-7620-eof-contract-creation-instructions/18625/8) EOF creates new problems for application-layer developers like me. Seeing as it also doesn’t really ***solve*** any of the existing problems that I have, I would not adopt EOF. Also seeing as legacy EVM will need support for the foreseeable future, I’m not enthusiastic about EOF.

My 3 major gripes are:

1. TXCREATE’s functionality (or lack thereof) not supporting CREATE3-like patterns.
2. The insistance around lack of inspectability of bytecode (and how you can’t completely hide the bytecode if you have anything resembling CREATE2)
3. Gas rules (not allowing capped-gas *CALL, the 2300 gas rule, 63/64ths rule)

---

**bbjubjub** (2025-03-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xrchz/48/12202_2.png) xrchz:

> I don’t believe stack validation needs changed semantics. It can be done already via analysis of status-quo EVM code. Is there reason to think otherwise?

After thinking about it, I personally believe that it would be possible to do stack validation without pulling in EOF. It would involve analyzing “legacy” bytecode using a similar algorithm as EIP-5450. Specific sequences involving the PC opcode would be recognized as static relative jumps, (a bit like `aiupc` in RISC-V) and PUSH-JUMP as absolute. Then if validation fails, the contract would be marked as non-compliant, but still remain usable with backwards compatible semantics as before. If it is compliant, it would be marked as such and potentially benefit from gas discounts and a higher size limit. This would still require a hardfork, but would be much more transparent to the application layer.

There would need to be an EIP to flesh this out and give it a chance. I am willing to help write it if there is interest.

---

**Arvolear** (2025-03-16):

The question I always ask is who would use EOF if L2s dominate the market share?

With such a huge EVM update it’s not enough for Ethereum to just be a “North Star”. Existing L2 stacks have to upgrade as well or an official stack need to be provided and maintained by EF.

Honestly, there are three things that scare me the most:

1. Instantly added complexity to EVM.
2. Even wider divergence of L2s from L1.
3. Short term concentration on the app layer “fixes”, while not addressing scalability issues and not bringing new ideas to L1.

Also with the current rollup-centric roadmap Ethereum may well become a pure DA layer. So all these EVM shenanigans may not really worth the effort.

---

**chfast** (2025-03-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> We could just remove JUMPDESTs.

Are you going to properly propose this in form of EIP / spec update?

---

**ajsutton** (2025-03-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arvolear/48/11091_2.png) Arvolear:

> Existing L2 stacks have to upgrade as well or an official stack need to be provided and maintained by EF.

Every L1 hard fork needs to be adopted by L2s, which they consistently do. What makes you think L2s wouldn’t adopt this given the exceptionally strong demand for full Ethereum equivalence?

At least for OP Stack EOF support would be inherited from the L1 client implementations quite easily and I don’t see any reason it wouldn’t be supported.

---

**Arvolear** (2025-03-16):

Because this upgrade is so complex and consists of numerous new opcodes, it must be coordinated with the L2 teams.

- For opstack, it is not as simple as “merging upstream changes”.
- For ZK rollups, constraints generation spec, tracers, zkECs, etc, need to be updated.

For example, Linea still doesn’t support a simple push0 opcode.
- zkstack has its own Solidity compiler that will need to be updated as well.

I really want to believe that L2s would wish to implement EOF, but given their reluctance to ship much smaller changes, I have doubts about that.

---

**pdobacz** (2025-03-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/duncancmt/48/15676_2.png) duncancmt:

> TXCREATE’s functionality (or lack thereof) not supporting CREATE3-like patterns.

Can you elaborate on this one please? [TXCREATE as specced out in EIP-7873](https://eips.ethereum.org/EIPS/eip-7873) is designed to allow anyone to deploy a CREATE3-like EOF factory to a deterministic address on different chains. By CREATE3-like I’m assuming you mean one which doesn’t include the initcode hash in the address.

If EIP-7873 misses any deployment pattern, please let us know.

---

**duncancmt** (2025-03-17):

Ahh, I wrote that original comment before the changes to 7873 that removed the inithash from the address calculation. I did not re-read the EIP to pick up the changes. I think that as it exists right now, 7873 supports every usecase that I can think of ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

---

**bbjubjub** (2025-03-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xrchz/48/12202_2.png) xrchz:

> If something has to be included, I think I could get behind adding relative jumps (although not yet convinced they are really worth it).

IMHO static jumps on their own are not really worth it because they can be done with combos of PC PUSH ADD/SUB and JUMP(I).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xrchz/48/12202_2.png) xrchz:

> I don’t believe stack validation needs changed semantics. It can be done already via analysis of status-quo EVM code. Is there reason to think otherwise?

As far as I can tell this type of analysis can be done. Since we wouldn’t have dedicated jump and call instructions, we would have to “bless” certain opcode sequences as the official ways to do a relative jump or a subroutine call and statically track the stack that way. Then you would be able to add protocol-level flags to the contract accounts that pass validation, which is something that EOF wanted to avoid. Someone could also explicitly trigger validation of an existing contract, which isn’t possible with EOF.

It seems as though if we already specced stack validation for EOFv1, we can port it back to legacy EVM. Plus, it seems compilers most likely generate compliant bytecode already. I would love if compiler people and client devs could check me on this though.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xrchz/48/12202_2.png) xrchz:

> Thanks for your point about versioning. On that point my previous comment about stability still feels relevant: I would rather not make plans (like versioning) that make major EVM upgrades easier, because I would rather not have major EVM upgrades and for the benefits of this to be appreciated.

That is a very fair concern for sure. It also made me think that if Ethereum is aiming to eventually ossify, at some point there would be an ultimate EOF version and we would stop changing semantics. However, we would be left with a lot of overhead due to all the previous versions. If we can avoid than and still get most of the benefits that would be nice.

---

**shemnon** (2025-03-18):

A lot of these questions have been asked and answered in other forums.  But it’s great to get a centralized list.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> Reducing compiler complexity:
>
>
> EIP-663  opcodes allow access deeper in the data stack. This is useful, but not a requirement for modern compilers – all modern compilers know how to implement stack/register spilling. This is a shortcoming of solc, not of the underlying VM. (As an example, Vyper does not have stack-too-deep as a result of compiler and language design.)

Compilers indeed can solve the famous “stack too deep” problem with [register allocation](https://en.wikipedia.org/wiki/Register_allocation) but they cannot guarantee optimal solution. But even if they could, stack/register spilling is very cost ineffective without reliable access to cheap memory. The EVM’s non-linear gas cost for memory makes access to larger variable pools more expensive and fragile than a paged memory model like one in typical silicon processors.

With this in mind, solving this problem on the compiler level is just a trade-off, rather than a direct improvement. Efficient and safe upgrade to EVM’s stack management is important, EIP-663 achieves that and in order to do so safely, requires immediate arguments (see other points).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> Improving bytecode size due to JUMPDEST removal:
>
>
> We could just remove JUMPDESTs.

Removing JUMPDESTs will have very negative downstream impact. JUMPDEST addressed an inherent defect in dynamic jumps. Without JUMPDEST compilation via Intermediate Representations (IR) (e.g. LLVM) was infeasible.

There are also security implications related to preventing execution of data carried in the contract. Details should be better explained in a stand alone article.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> Makes it easier to upgrade the EVM, e.g. adding or removing opcodes:
>
>
> We can add validation rules to the existing EVM. Bytecodes of contracts can be analysed at creation, and we can disallow deploying contracts with specific opcodes - or change semantics thereof - if they are deployed after a given fork_blocknum.

This describes an approach that was tried and rejected in 2019 ([EIP-1702](https://eips.ethereum.org/EIPS/eip-1702)).  You need to know which rule set to follow not only when validating, but also when executing a contract, so information about the version must be stored alongside the code. [EIP-7702](https://eips.ethereum.org/EIPS/eip-7702) also greatly complicates account versioning for contract validation. This is why EOF opts for storing it inside bytecode container.

Secondly, to allow for validation we also would need to allow for data segments. We would need to mark code as being EOF, then mark where the code ends and the data starts. This is the essence of the EOF container, and falls naturally from first principles once the need for validation is established.

Finally, EOF aims for changing the version as little as possible, ideally never. New rule set at every fork would mean a lot of versions co-existing together in the state, which greatly complicates reasoning about overall execution rules, any future (EVM- or adjacent) upgrade must take into account all possible versions it affects, and EVM implementations must maintain multiple rule sets in parallel. These are the points that EOF is already being criticized for, while introducing only one additional version. Piecemeal changes would have a net grater complexity if not aggregated in an upgrade like EOF.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> Allows for opcodes with immediates:
>
>
> Again, we don’t need to change semantics of existing contracts. Rather, validate and apply updated semantics to newly created contracts.

EOF forbids deploying undefined opcodes, which allows to introduce new opcodes in the future without changing EOF version. The system where new opcodes require new validation rules at every fork would be more complicated (see previous point).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> Remove gas introspection:
>
>
> You can just add the EIP-7069  (CALL2, etc) opcodes, which don’t access gas.
> Validate that code does not include the GAS opcode.
> Because of the 63/64ths rule, contract behaviour depends on gasleft anyways (subcalls can OOG without the outer contract OOG).

This is exactly how EOF removes gas introspection.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> Remove code introspection:
>
>
> You can add validation rules to legacy EVM to remove the relevant opcodes. New creation opcodes would need to be introduced, but it wouldn’t need to be shipped at the same time as all these other changes.

This is exactly how EOF removes code introspection.

Devising and shipping an intermediate container format which **just** enables code introspection removal and then iterating on it to achieve other benefits of the structuring means more EVM versions co-existing together in the state (see previous point). At the same time, achieving **just** code non-introspection by itself would not warrant the effort or complexity required for the containerization.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> Remove dynamic jumps:
>
>
> This can also be addressed simply by updating pricing and providing a carveout for PUSH2 JUMP(I) in the gas schedule.

This proposal has zero benefit for static analysis, because this pattern exists today and static analysis tools already recognize it. Dynamic jumps are not banned and this is what the tooling struggles to analyze.

Furthermore, detecting this carveout would slow down VM implementations as they would need to take processor time to detect the pattern at every jump. Gas charged will go down but so will gas per second and transactions per second.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> Subroutines:
>
>
> There are existing, less invasive proposals to the EVM which include subroutines and give preference to static jumps.

If this refers to [EIP-2315](https://eips.ethereum.org/EIPS/eip-2315), that one was [rejected by ACD](https://github.com/ethereum/pm/issues/263) after [arguments](https://ethereum-magicians.org/t/eip-2315-simple-subroutines-for-the-evm-analysis/4229) were made it would not be adopted. The argument was that there wasn’t enough benefit and enough gas saving provided by it. EOF’s approach to subroutines (functions) have strong support from at least one compiler team.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> Address space expansion:
>
>
> Can change semantics of existing opcodes (like BALANCE) to not zero the top 12 bytes of the address, again via contract versioning.

Important consideration here is that we want to prevent breaking of already deployed contracts if/when an ASE proposal is introduced. There are operational contracts that depend on the trimming of the address argument. This is what derailed previous attempts at address space extension.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> Remove codesize limits:
>
>
> We can just do that, since initcode is metered via EIP-3860 .

[EIP-3860](https://eips.ethereum.org/EIPS/eip-3860) addressed a JUMPDEST analysis exploit that was best executed at initcode time, however there is no metering to loading contracts from state. JUMPDEST analysis still needs to be performed or cached. And this needs to be loaded from the cache or performed every time the contract is executed. Piecemeal changes to existing analysis rules would also require cached validations to be updated.

EOF code validation is performed only when the code is first introduced to the blockchain via the initcode transaction.  Hence any other interactions with EOF code (reading the contract from state, executing other contracts, factory contracts creating new contracts, etc) are performed without needing any further validation. Validation is asserted for the life of the bytecode.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> ZK-friendliness
>
>
> EOF is purportedly more ZK-friendly. However, we have not seen arguments for why this is a hard requirement.

We do not claim it is a hard requirement. But ZK-friendliness is an argument in favor of EOF. Initial implementations have shown a [2.5 to 3x speed improvement](https://x.com/SuccinctLabs/status/1853525841537552833) in the cost of ZK proving a contract transaction. Driving down the prices of ZK transaction is needed to achieve the “nickle” goal of Ethereum scaling.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> In other words, all the benefits of EOF can be introduced in more piecemeal, less invasive updates to the EVM.

Piecemeal improvements have a greater cost over the longer term of their implementation.  Multiple backwards incompatible changes will cause the clients to have to support multiple incompatible versions of the EVM. This is why EOF is batching proposed backwards incompatible changes in to as few steps as possible, ideally one.

Piecemeal changes also have a tendency to complicate each other when not properly coordinated. One previously considered alternative was to add contract versioning ([EIP-1702](https://eips.ethereum.org/EIPS/eip-1702)). The new EIP-7702 contract delegate feature in Pectra breaks any safety guarantees that this EIP would have provided, as the actual code the account contains could easily be updated, and now two different accounts need to be considered in the logic, increasing the number of ways a client optimizing this interaction could introduce unexpected bugs.

Packaging the changes in aggregate allows the net impact of all of the changes to be smaller and less invasive than if each change were to be introduced slowly. It also removes the need for intermediate states between each piecemeal change, where novel attacks could be launched.

Piecemeal would mean we need to maintain multiple non-compatible EVMs. Also the piecemeal approach has been proposed before and rejected by ACD/the community as not useful enough and problematic (EIP-2315, EIP-1702, EIP-615, for example).

It is much more rational for EOF to ship all breaking changes in only one backwards-incompatible step.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> Meanwhile, the complexities of EOF cannot be ignored:
>
>
> Legacy EVM needs to be maintained, probably indefinitely.

EOF is at its core a container format for the EVM, and is designed to be run within the same VM code. The same operation dispatch, contract calling code, storage access, memory handling, arithmetic, etc. et. al. is all handled by the same client code whether the contract is in an EOF container or is a legacy contract. EOF shares more with the legacy EVM than what differentiates it.

By “legacy EVM” in this context we should clarify that we are talking about 16 removed opcodes, making up for roughly 10% of current opcode count. Some of these opcodes share large portions of logic with their legacy counterparts (e.g. `EXT*CALL`, `EOFCREATE`), bringing that figure further down.

Also, the potential for a legacy → EOF bytecode migration still has not been definitely ruled out, albeit it is a daunting task best approached once EOF is in production.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> Tooling needs to support EOF. This requires coordination and effort across many different teams.

This is true for all changes to the EVM. Coordination is done via the bi-weekly [EOF implementers call](https://github.com/ethereum/pm/issues/1361) everyone is welcome to. Besides the EOF implementers and EIP authors, there are members of testing, compiler and tooling teams participating. Some teams have already shipped devnet-0 support in their tools.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> Risk of vulnerabilities due to complexity. For instance, send() and transfer() now allow reentrancy . This was not noticed until a month before Osaka was scheduled to be finalised, even though EOF has been in development for nearly 4 years.

Solidity’s current plan is to deprecate `send()` and `transfer()` for EOF contracts. Other means to prevent reentrancy are encouraged (`TSTORE/TLOAD`), especially so since relying on gas to block reentrancy is [subject to break unexpectedly on gas repricings](https://www.alchemy.com/overviews/reentrancy-attack-solidity#gas-limit), which is also one of the reasons gas introspection is removed in EOF in general.

Other developments like the [PAY opcode](https://eips.ethereum.org/EIPS/eip-5920) may impact that decision, but given the subtleties between the implementations Solidity may choose to expose it via a new API (such as `pay()`) while providing compiler warnings when mapping send and transfer to the PAY opcode, but this is a decision for the Solidity team.

Answering the notion that the issue remained unnoticed for nearly 4 years: the first [PR](https://github.com/ethereum/solidity/pull/15294) with initial EOF Solidity support was pushed on July 23rd 2024. This is a problem which is related to language implementation and how it deals with reentrancy issue. It was actually [noticed](https://github.com/ethereum/solidity/issues/15310) by the Solidity team soon after that PR opened and before the official release with **experimental** support for EOF.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> Related to that, EOF has been a moving target: EOF is looking to get shipped even though parts of the spec keep changing, making it difficult for compiler and app devs to review the entire package.

Specifications being updated prior to activation is the norm in Ethereum, not the exception. For instance, EIP-7702 which had a [change](https://github.com/ethereum/EIPs/pull/9248) merged one month before Holesky activation. EIP-2537’s spec was updated [after](https://github.com/ethereum/EIPs/commit/437d026460d5c6d4f6159533efde6926b72dd324) the testnet hard fork.  This EIP is even older than the main EOF specifications.

The changes to spec are driven mostly by feedback from ACD and the community, or they are immaterial clarifications and renamings. For context and point of reference: we are still months away from EOF going to testnet and intend to freeze breaking changes with devnet-1, months from the public testnet rather than weeks we have seen in other major features.

You can review [planned EOF devnet-1 changes](https://github.com/ipsilon/eof/issues/165), and also review the [EOF Testnet plan](https://notes.ethereum.org/@ipsilon/eof-testnets-plan).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> Work to target the new format for compilers and app devs.

Solidity has already updated their compiler to the [current devnet-0 spec](https://soliditylang.org/blog/2025/03/12/solidity-0.8.29-release-announcement/) and end users will not need to update the source code of their contracts unless they are depending on deprecated features, such as the current incarnation of `SELFDESTRUCT`.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> EVM contracts get much more complicated due to headers. An empty contract is now at least 15 bytes.

With EOF, contracts get much simpler thanks to separating data and code reliably, as well as replacing dynamic jumps with static ones and function calls. Contract size cannot be seen as a metric to compare complication (or complexity).

In all but the simplest contracts the number of bytes used in the header is offset before the function dispatch code or first function is complete.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> Bytecode size tradeoffs. For instance, subroutines cost several bytes just to declare, which penalises contracts with many, small subroutines.

From [experiments with a preliminary PoC that was largely unoptimized](https://notes.ethereum.org/@ipsilon/solidity_eof_poc) we did not see any bytecode regressions for widely used contracts. The tested contracts all demonstrated a reduction in bytecode size.

Small subroutines indeed may be inlined by compiler optimizations, which is already the case when targeting legacy EVM.

The current Solidity EOF implementation still have almost all optimizations steps disabled for EOF in assembly level. This means that this version’s 10% reduction in code size when using EOF should not be used to measure the final impact. We have experimental version with most important optimizations enabled which confirm code size and gas cost reduction for EOF. It’s going to be pushed to solidity repo soon. Also CPU time benchmarks confirm gains in execution speed of EOF compiled contracts.

---

**shemnon** (2025-03-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xrchz/48/12202_2.png) xrchz:

> Perhaps as a meta point there seems to be disagreement about whether major EVM changes are desirable in general (including in the notes from the call you mentioned). I would argue that a stable VM, on which people can invest in building up excellent tooling and apps with confidence, is much more valuable than the ability to evolve the VM to compete with other VMs, since this has the cost of scaring away investment in something that’s gonna potentially change in the future. (I’m speaking in part here as someone who becomes much more hesitant about my investments in the EVM, both as user and dev, when I see that stability of the VM isn’t being prioritised.)

This is a fully general argument that could be applied to any change in the protocol, not only EVM. Any change for the sake of scalability, security, usability, goes against “stability” of ossified protocol.

Ossifying the protocol at the wrong time presents more risk to the future of Ethereum than not ossifying at all.

---

**shemnon** (2025-03-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bbjubjub/48/13986_2.png) bbjubjub:

> That does not mean that all of EOFv1 belongs as a bundle together. In fact it would be possible to introduce versioning on its own and nothing else, but there would be no incentive to upgrade. If we want a carrot, a good choice would be stack validation + relative jumps, which enable optimizations that could enable a gas discount. This pulls in roughly half of the EOF EIPs, which constitute a more minimal set and exclude some of the more problematic changes like gas inobservability. This may be inaccurate because I haven’t been following EOF closely, but the message is: versioning per se uniquely unlocks a more efficient EVM afaict.

This is a more nuanced take on the “one step” argument than the prior arguments and it deserves consideration in a less adversarial environment (such as delaying no code introspection and no gas intospection to a hypothetical ‘EOFv2’).  However, we have seen problems in getting [any EVM change adopted of any size](https://www.rollup.codes/linea#opcodes), so there is no guarantee that breaking EOF into multiple parts would lead to the latter pieces being adopted.

---

**shemnon** (2025-03-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bbjubjub/48/13986_2.png) bbjubjub:

> xrchz:
>
>
> I don’t believe stack validation needs changed semantics. It can be done already via analysis of status-quo EVM code. Is there reason to think otherwise?

After thinking about it, I personally believe that it would be possible to do stack validation without pulling in EOF. It would involve analyzing “legacy” bytecode using a similar algorithm as EIP-5450. Specific sequences involving the PC opcode would be recognized as static relative jumps, (a bit like `aiupc` in RISC-V) and PUSH-JUMP as absolute. Then if validation fails, the contract would be marked as non-compliant, but still remain usable with backwards compatible semantics as before. If it is compliant, it would be marked as such and potentially benefit from gas discounts and a higher size limit. This would still require a hardfork, but would be much more transparent to the application layer.

There would need to be an EIP to flesh this out and give it a chance. I am willing to help write it if there is interest.

The space that needs to be carved out is to ensure that no “compiler bombs” are allowed.  While most contracts are well behaved the presence of a malicious contract can remove all the gains seen by compliant contracts.  The sad truth of Ethereum security is we always optimize for the worst case, because these will be posted to the network (such as the Shanghai attacks in 2016).

Also, the time spent to separate compliant from non-compliant contracts could be more than the time saved by applying the compiler optimizations.

---

**shemnon** (2025-03-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/duncancmt/48/15676_2.png) duncancmt:

> TXCREATE’s functionality (or lack thereof) not supporting CREATE3-like patterns.

[TXCREATE as specced out in EIP-7873](https://eips.ethereum.org/EIPS/eip-7873) is designed to allow anyone to deploy a CREATE3-like EOF factory to a deterministic address on different chains.  This is a core feature of the EOF devnet-1 plans and has been part of the mega spec for two years.  It was removed from Prague as a concession to the size of the fork and was always intended to ship at some point.  The current plan is to ship it with the Osaka specced EOF version.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/duncancmt/48/15676_2.png) duncancmt:

> The insistance around lack of inspectability of bytecode (and how you can’t completely hide the bytecode if you have anything resembling CREATE2)

Vitalik makes the [best arguments](https://ethereum-magicians.org/t/eof-proposal-ban-code-introspection-of-eof-accounts/12113) for banning code introspection.  It separates the representation of the contract from the consensus about its execution and outcome at the protocol level, allowing code to be transpiled to other formats, such as RISC-V.  Allowing the code to enter or leave system memory locks in one particular representation of the contract as part of consensus.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/duncancmt/48/15676_2.png) duncancmt:

> Gas rules (not allowing capped-gas *CALL, the 2300 gas rule, 63/64ths rule)

Relying on a fixed gas schedule has been a problem for a long time and [best practices](https://www.alchemy.com/overviews/reentrancy-attack-solidity#gas-limit) are to not rely on it.  EOF formalizes this recommendation in a way that allows future EVM repricings to have minimal impact on user code. There is a working group working on dramatic changes, including things like multi-dimensional pricing and code merkelization, which will have dramatic effects on the gas schedule as a whole.

---

**chfast** (2025-03-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arvolear/48/11091_2.png) Arvolear:

> Because this upgrade is so complex and consists of numerous new opcodes, it must be coordinated with the L2 teams.
>
>
> For opstack , it is not as simple as “merging upstream changes”.
> For ZK rollups, constraints generation spec, tracers, zkECs, etc, need to be updated.
>
> For example, Linea  still doesn’t support a simple push0 opcode.
> zkstack  has its own  Solidity compiler that will need to be updated as well.
>
>
>
>
> I really want to believe that L2s would wish to implement EOF, but given their reluctance to ship much smaller changes, I have doubts about that.

These are general criticisms of the rollup centric roadmap, not EOF in particular. If EOF were not proposed these would still be problems, in the same way they are stated.

Note that one engineer from Optimism said that if EOF ships on mainnet it will appear on the op-stack. This is because of OP’s architecture that relies on lightly modified L1 clients, they will get the bulk of the work for free. The parts of the EVM that EOF would modify are fairly separated from the pieces that are changed to accomodate the other parts of the OP stack such as the sequencer.


*(48 more replies not shown)*
