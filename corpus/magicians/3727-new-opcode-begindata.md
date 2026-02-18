---
source: magicians
topic_id: 3727
title: "New opcode: BEGINDATA"
author: MrChico
date: "2019-10-28"
category: EIPs
tags: [opcodes, eth1x]
url: https://ethereum-magicians.org/t/new-opcode-begindata/3727
views: 3204
likes: 4
posts_count: 9
---

# New opcode: BEGINDATA

This is for discussing EIP BEGINDATA opcode as proposed here: https://github.com/ethereum/EIPs/pull/2327, and as previously as part of [@gcolvin](/u/gcolvin) 's static jumps and subroutines proposal. While being a fairly small change on its own, I think it serves as an important prerequisite for proposals like EIP-1702 or EIP-615.

## Replies

**chriseth** (2021-03-02):

Another use-case of BEGINDATA that has not been mentioned in the EIP document:

Layer two solutions like Optimism that check arbitrary code for conformity to a certain pattern (only pure opcodes, etc) have to jump through various hoops to avoid the failure of such a checking mechanism on data. If the EVM guaranteed that a certain part of the code is never executed through an opcode like BEGINDATA, arbitrary data could be included.

For those who argue that data has no place in code, I would like to list the following features Solidity currently uses to store data in code:

- constructor arguments
- large constants
- metadata hash
- compiler version
- deployed code (could be considered code)
- other contracts to be created via “new”

---

**gcolvin** (2021-03-05):

Good proposal, [@MrChico](/u/mrchico), I’m sorry it has been lying fallow so long.  My only concern here is backwards-compatibility.  The proposal states:

> The proposal will not change any existing contracts unless their current behaviour relies upon the usage of unused opcodes.

How does it break such contracts?

Does it matter?

If it does matter what can we do about it?

---

**MrChico** (2021-03-05):

My point here is simply to notice that the introduction of this opcode *can* change the semantics of existing code, if they

a) contain the BEGINDATA opcode outside pushdata and

b) there are codepaths that run through code located *after* the BEGINDATA opcode.

Such a contract would no longer be able to execute those codepaths.

I am not aware of any examples, nor can think of any reasonable use case for this.

Unless some prominent examples are discovered, I would argue that it does not matter. For every semantic change it is possible to create a contract that is broken by it.

---

**gcolvin** (2021-03-07):

I may be confused here, but if existing code branches around a BEGINDATA opcode without ever executing it then it is still valid code, but will not be valid afterwords.

---

**holiman** (2021-03-08):

I’ll take some words from the EIP

> It is here introduced in its own right in order to exclude data from the JUMPDEST analysis of contracts, making it impossible to jump to data.

What does impossible mean…? Impossible for whom? Impossible, as in, more difficult for the compiler to  mistakenly jump to “data” ?

> This makes it easier for static analysis tools to analyse contracts, allows disassemblers, chain explorers and debuggers to not display data as a mess of INVALID opcodes

It makes it a bit easier to know that a segment of strange code is intended to be used as data. To me that seems like yes, it’s an improvement, but a pretty marginal one, no?

> and may even provide a marginal improvement in performance.

I  suspect it would be the opposite. Right now, the jumpdest analysis only need to check if an op is `PUSH1 <= op <= PUSH32 ` (two ifs) and otherwise move on to the next op. With this change, we’d introduce one more branch condition for each byte of code, to also check if the op is `BEGINDATA`.

> I am not aware of any examples, nor can think of any reasonable use case for this.
> Unless some prominent examples are discovered, I would argue that it does not matter.

I think there may be, but I’m also inclined to think they’re just old experiments. I did investigate that pretty thorougly back when we wanted to prevent jumping out of subroutines, where the same problem arose regarding `BEGINSUB`. There are a few quirky contracts that jumps across data-portions to deliver data. I’ll see if I can dig up that old analysis.

---

**holiman** (2021-03-08):

Would be neat if `BEGINDATA` could instead be declared as the first op, maybe like `CODEEND xxyy`. Then it wouldn’t impact jumpdest analysis at all.

But I guess that’s another can of worms.

---

**chriseth** (2021-03-09):

[@holiman](/u/holiman) in my opinion, the main (and maybe only) use-case is for on-chain analysis of code like the one done by optimism: For the sake of performance, their on-chain verifier directly executes raw EVM code instead of interpreting it. Optimism contracts whose execution is verified on chain cannot contain opcodes like ‘sstore’. Instead, such opcodes need to be translated into a call to the “manager contract” who then checks the relevant proofs submitted to it. Similar changes need to be done to regular `call` opcodes. Before the contract is executed for sake of verification, it is analyzed that it conforms to these conditions, i.e. they contain no sstore and instead they contain calls to the manager that also have to be of a certain form (for example, they have to revert if the manager reverted).

If a contract contains data (for example for constructor arguments or large constants), data can of course violate these conditions if it is read as code. Currently, it cannot be reliably and cheaply detected on-chain whether or not a certain piece of code (which is in fact data) is reachable or not.

With the introduction of `begindata` (or a similar mechanism) that makes the EVM enforces that certain code cannot be reached, such analysis can be done much more easily on chain.

I don’t care how this is implemented. We can also do it by introducing a new opcode `codeend` that consumes a single stack item and reverts if it is not preceded by a push opcode. Then we probably would not even have the problem of analyzing if any contract in the past has ever used the `begindata` opcode.

Maybe [@axic](/u/axic) would like to chime in who has made similar suggests recently. This `codeeend` opcode could also be used in a forwards-compatible manner and provide more structure to bytecode. We could only use it for specifying the code size for now, make it consume two stack slots where the first has to be zero for now and the second specifies the code length.

---

**wjmelements** (2021-04-02):

Static analysis tools will need to be careful because `0xb6` can still appear after `PUSH`.

Answering the EIP’s motiviation, I don’t think Ethereum should analyze new contracts for validity because it would increase the computational cost of `CREATE` operations.

