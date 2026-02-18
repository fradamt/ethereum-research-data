---
source: magicians
topic_id: 3756
title: "EIP-2348: Validated EVM Contracts"
author: shemnon
date: "2019-11-04"
category: EIPs
tags: [evm, evm-evolution, validation, eip-2348]
url: https://ethereum-magicians.org/t/eip-2348-validated-evm-contracts/3756
views: 2562
likes: 2
posts_count: 14
---

# EIP-2348: Validated EVM Contracts

Discussion topic for



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/2348)














####


      `master` ← `shemnon:validated`




          opened 04:00PM - 04 Nov 19 UTC



          [![](https://avatars.githubusercontent.com/u/38109?v=4)
            shemnon](https://github.com/shemnon)



          [+273
            -0](https://github.com/ethereum/EIPs/pull/2348/files)







A set of contract markers and validation rules relating to those markers is prop[…](https://github.com/ethereum/EIPs/pull/2348)osed. These
validation rules enable forwards compatible evolution of EVM contracts and provide some assurances
to Ethereum clients allowing them to disable some runtime verification steps by moving these
validations to the deployment phase.












A set of contract markers and validation rules relating to those markers is proposed. These

validation rules enable forwards compatible evolution of EVM contracts and provide some assurances

to Ethereum clients allowing them to disable some runtime verification steps by moving these

validations to the deployment phase.

## Replies

**MrChico** (2019-11-08):

What confuses me about this EIP is that you seem to suggest having the two versioning schemes, 1702 and 1707 used in tandem. Why are you doing this?

A simpler proposal would be to just say that this validation should apply to all accounts of (1702) version “1”, and not introduce any bytecode versioning header.

---

**shemnon** (2019-11-08):

The reason is backwards compatibility. If we suddenly turn on 1702 and require all code to be validated suddenly contracts that could be submitted the block prior now fail to deploy. And such bad opcodes comes from widely used option in solidity (some of which may even be the default, I’d have to research that).

That’s bad UX, we need to provide some sort of a means for a contract deployer to “opt in,” and in time the tooling will default to opting in and provide options to opt out. We could just do the header (using  `0xef`  as the version header) that required validation at deployment time. But the impression I got is that other core developers would want a flag to indicate that validation has been/could have been performed other than just the content of the contract.

So if we had to choose one it would be the 1707 variant. That preserves the ability of tooling to ease into the new requirements.

---

**MrChico** (2019-11-12):

I see. Another alternative (which seems preferable to me) would be to rely upon https://specs.that.world/44-vertxn/ and use another field of the transaction data to specify that such contracts are to be created.

I don’t think that versioning information has a place in the bytecode. Some people use bytecode to store data, and could inadvertently deploy contracts which matches the versioning header. https://medium.com/coinmonks/on-efficient-ethereum-storage-c76869591add

---

**MrChico** (2019-11-12):

Not that one necessarily want to support such crazy hacks, but it could indicate that putting the versioning header in the bytecode can have unintended consequences

---

**shemnon** (2019-11-12):

Adding another data field in the transaction has a very high level of resistance to overcome, all of the client tooling would need to change to support it.

As for people using bytecode to store data, that is exactly the problem that this EIP is aiming to solve.  Without clear deliniation about what is code and what is data we can’t make reasonable conclusions about the contract code.  Just because some contracts started abusing the contract data should not preclude us from using the field as intended and to curb that abuse.

And I feel that the bytecode is a very good place for the versioning information.  The JVM, CIL, WebAssembly, and LLVM bitcode all use items like magic numbers for headers, in stream metadata, and explicit versioning in their data files.  This is in line with how modern VMs operate

---

**shemnon** (2020-01-09):

Looping back on this after a long Christmas break.

One concern on All Core Devs was that jump validation could cause a DOS attach based on memory use during validation from a large (8Mib) contract.  There are two situations: one where the contract is loaded into an account and when executed from a transaction.  For account contracts the size has been limited since Spurious Dragon to 24Kib, so the memory bloat is limited to a reasonable size.  For a TX the limit is the intrinsic size cost of a transaction.  at 4 gas per zero byte the size is brought up to no more than 2.4Mib and for a non-trival contract the limit is 16 gas per byte would be less than 611KiB.  Using a compact bitset the memory growth is 76KiB in non-pathological cases and 306KiB in pathological cases.  For account based contracts the increase memory needed is 3Kib.  As noted in the EiP there is sample code in Besu to do this analysis in one pass and one I believe would be one flip in Go (the APIs don’t match up the same) - https://github.com/ethereum/EIPs/pull/2348#issuecomment-555116068.

---

**shemnon** (2020-01-09):

Another concern is the interaction between validated and legacy EVM.  There are two orthogonal concerns that create four situations.  First is does the chain support validating code and the second is does the code expect to be validated.

The first case is what we have today, neither the chain nor the compiled code expects to be validated.  This is the status quo.

Next let’s consider if the chain expects to validate contracts and all code is treated the same.  In this case a lot of contracts that previously were deployable will no longer be deployable because of metadata such as the swarm hash of the code that was appended to the bytecode in a code section that will never be executed.  Because it’s not following the conventions marking non-executable code the contract is rejected.  This is bad, it would require all users to do a co-ordinated toolchain update of their build and deployment systems.  This is orders of magnitude larger and has more existential risk than an ordinary fork.  Consider that there are PDP-4 and Windows XP systems still in operation providing critical infrastructure to many businesses.

To maintain community compatibility we need to provide, at least for a little time, a way to still deploy non-validated EVM.  The question is then how to mark when EVM code should be validated.  One alternative is to introduce a new opcode to create validated contracts.  This would keep the versioning information out of the stream of code.  Considering that there are proposals to fundamentally redefine opcodes, such as redefining the number of stack items consumed by CALL series operations.  Keeping the versioning information out of the stream of operations could make detecting EVM opcodes targeting this proposal could lead to execution confusion.  Broadening our view we need to consider that EVM is becoming an ecosystem to it’s own.  Multiple hyperledger projects support EVM based contract execution.  Relying on an ethereum only way to identify the versioning would then result in these clients adopting different mechanisms to identify different versions of EVM code.  Based on this concern I feel in-stream versioning is superior and will result in less ecosystem confusion.

Consider also that almost all other VM systems use a magic number header byte.  Java has 0xCAFEBABE, wasm has ‘\0asm’, and even LLVM, the state of the art, uses [‘llvm’](https://releases.llvm.org/1.3/docs/BytecodeFormat.html#signature) at the start of it’s bytecode.  Hence a ‘\0evm’ or '\xefevm` (0xef65766d) would align with current best practices. If a contract wants to be subject to validation (and gain access to future byte codes) it can compile itself as validated and use the header bytes.  Older EVM code can be oblivious to this requirement.

So for the case of the blockchain that wants EVM code that is validated gating the new features off of a header validation byte would provide a means for old and new code to be added and executed simultaneously.  For users who do not update their toolchain they will operate as normal.

There is on last case, for a blockchain that does not want to or know how to validate code, when presented EVM code that claims to be validatable.  What happens then?  And what if the code expects new semantics such as different stack counts for CALL and DELEGATECALL?  Ideally we would not want such contracts to execute unless the blockchain supports those semantics.  out of stream versioning does nothing in these cases when the evm code becomes separated from it’s versioning information.  The two proposed headers for validated code would, in current implementations, fail to execute because the first operation would either be 0x00 which is STOP or 0xef which is an invalid opcode.

There is also the issue of code claiming to be validated code when it was deployed prior to fork validation.  This is where account versioning provides it’s value.  For account code the validated opcodes would require both the header and the account version, as already mentioned in the EIP.

So to summarize: pre-fork/v0 is fine.  post-fork/v0 would execute just as pre-fork with opcodes that don’t require validation.  Post fork/v1 would allow the version header, would run execution, and would unlock new opcodes in the validated contracts.  Pre-fork/v1 should not exist and would be a consensus failure if a v1 account existed prior to account versioning.  EVM code with the header would only execute in post-fork/v1 accounts or post-fork transactions (when executed out of the transaction).

---

**shemnon** (2020-01-09):

With the headers people can still continue to use code as data (even though it is a bad idea) by either (a) not using the EVM header bytes as the first 4 bytes of their data, which can be tricky if storing user data or (b) prefixing their data with the header byte and immediately going to the BEGINDATA opcode, then adding their data.

---

**holiman** (2020-01-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> One concern on All Core Devs was that jump validation could cause a DOS attach based on memory use during validation from a large (8Mib) contract

I think you misunderstood me on that call. I was talking about a `CREATE` call, within a tx. The `CREATE` passed along a 1-meg memory segment containing mainly jumpdests. After the create failed, it flipped a byte in memory, and called `CREATE` again, over and over.

So does this thing validate initcode or not?

---

**shemnon** (2020-01-10):

In this case I would expect the max code size check to run first and the create would fail because the code is > 24Kib.  So it wold be an implementation detail, would it be worth noting in the EIP that code validation should be one of the last validations, after easier checks like balance and code size?

---

**holiman** (2020-01-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> In this case I would expect the max code size check to run first and the create would fail because the code is > 24Kib.

I must be realy lousy at explaining myself… There’s a misunderstanding here, I think it’s one of these two:

1. You maybe think I am talking about the code that the initcode (CREATE-call) returns, the code-to-be-deployed. I am not, I’m talking about the execution of initcode.
2. You may think there’s a limit on the initcode? There is not, the initcode is arbitrary length, so the caller expands memory to e.g. 1 Mb once, and is then free to use that for CREATE ops arbitrary many times, at no extra cost-per-byte.

So, my concern/question is basically if there’s any situation where we have to do on-the-fly validation of `initcode`.

---

**shemnon** (2020-01-15):

Regardless of how it gets in I’m thinking we do want to provide some size limitations.  There are other ecosystem uses of EVM that may be depending on the size limitations that are not subject to mainnet paths.

What I’m thinking is adding in that the code segment be subject to the contract code size limit introduced in Spurious Dragon (EIP170).  By code segment I mean all data from the start to the BEGINDATA opcode must be less than 24KiB for mainnet, and whatever contract size limits other chains define.  This still allows for large amounts of data (zksnarks and such) to be crammed into the transacitons, they just wouldn’t be in code.

What I would need to gather data on is how the large TXes currently do this, and it could have a gas impact as well but again they would need to opt into validation.

---

**shemnon** (2020-01-21):

I’ve added some updates to the EIP in the PR [here](https://github.com/ethereum/EIPs/pull/2348/commits/04266aa5dc349eb9a7b0ead150dabcce1abd9c32).

Two main changes:

- Add a contract code size limit check to the ‘code segment’
- Settle on '0xefevm' as the header bytes ([0xef, 0x65, 0x76, 0x6d]) and PC=4 start

I would like to discuss this at the next All Core Devs call (#79).

