---
source: magicians
topic_id: 19893
title: "EIP-7701: Native Account Abstraction"
author: alex-forshtat-tbk
date: "2024-05-03"
category: EIPs > EIPs core
tags: [account-abstraction, eof, evm-object-format]
url: https://ethereum-magicians.org/t/eip-7701-native-account-abstraction/19893
views: 2401
likes: 26
posts_count: 20
---

# EIP-7701: Native Account Abstraction

One of the issues that arises from enshrining an [ERC-4337: Account Abstraction Using Alt Mempool](https://ethereum-magicians.org/t/erc-4337-account-abstraction-via-entry-point-contract-specification/7160) design in Ethereum is its reliance on Solidity method signatures and ABI-encoding that is not a native part of the EVM.

This EIP solves these issues by introducing a new transaction type as well as a family of AA-specific opcodes: `ACCEPTROLE`, `TXPARAMLOAD`, `TXPARAMSIZE`, and `TXPARAMCOPY`.



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7701)





###



Native Account Abstraction protocol, relying on a new transaction type and a family of opcodes

## Replies

**shemnon** (2024-06-26):

A bit late reviewing this, but it’s been because EOF v1 has been solidifying.  With that in mind I have some comments and suggestions with the EOF portions of the PR.

- Remove target_section_pc_offset and require all sections to start at PC=0 within the code section

My reasoning for this relates to the code validaiton within EOF, it’s only intended to start with a single entry point at zero. If code can enter at multiple entry points significant portions of stack validation need to be reconsidered, and that feels like too much for this EIP, in addition to needing a separate skill set to evaluate.

- Reconsider specifying ssz encoding of data

Clients are not yet mandated to implement, but more importantly robust solidity libraries handling SSZ do not exist yet, and the efficiency of SSZ in the EVM is an open question.  This is an issue that may be overcome in time, but I don’t think Native AA is the correct place to find out. Right now the Solidity ABI is much better ingrained in the ecosystem and will result in less friction when it comes to adoption.

The following 2 suggestions are to allow Native AA to use the EOF features without embedding the AA aspects into the EOF spec, and provide a generic reusable facility for other uses.

- Consider 4 bytes for entrypoint_role, and assign names based on ABI selectors

Expanding this to 4 bytes makes arbitrary mappings a bit less arbitrary, and preserves two future design spaces: multiple possible signatures for entry point actions, and secondarily possibly expanding it to a general case “selector” mode that EOF can deploy, where solidity can dispense with the occasionally large switching logic for function dispatch.  This also helps decouple AA logic from the EVM.

- Consider adding a “flags” field in entrypoints_section entries.

Some drafts of various AA proposals have imposed more restrictions on the kinds of operations that a function may perform, such as prohibiting all block info access in sender validation calls.  An extra flags field will provide signaling into the EVM so that EOF can perform that validation as part of EOF validation. This further decouples AA logic from the EVM otherwise specific validations would be tied to specific types which would then require EVM updates when new or different validations are requested.

---

**alex-forshtat-tbk** (2024-10-09):

Thank you for your review! Sorry on my part for a late response. We have made significant progress implementing RIP-7560 and, hopefully, it will have some production use by the time EOF is merged and EIP-7701 becomes our main focus.

I have made changes to EIP-7701, mostly implementing your suggestions.

You can see the PR with the recent changes here:

https://github.com/ethereum/EIPs/pull/8941

However, I do have a couple of questions about them:

1. You have mentioned the “selector” mode for EOF.
Is this something that is currently on a roadmap for EOF? I could not find this feature described anywhere, and native AA could greatly benefit from using a standard EVM-level dispatch.
I assume EIP-7701 would have little chance of getting accepted with its own dispatch logic when there are plans to introduce a system-wide solution. Do you think it makes sense for us to propose a general EVM “selector”, for instance, as a separate EIP that is a prerequisite to EIP-7701?
2. Regarding the flags field for entrypoints_section entries, would we have to define the full set of possible flags as part of this EIP? Currently, I am not sure I know what are the flags we may need in the future, so I assumed we would need a new EIP for each new flag, right?
3. Regarding the ABI encoding for the data necessary during the transaction validation, one alternative we discussed and are still considering is creating one or a small number of “transaction getter” opcodes that would provide the missing EIP-7701 transaction fields. Would you consider such a direction to be more or less consistent with the direction of the EOF?

---

**shemnon** (2024-10-10):

1. Selector mode.  I haven’t published any of my ideas for post EOF right now to keep focus on 1.0.  I have a talk at devcon where I will disuss some of my ideas.  It would be a general EVM selector.  It would basically switch out what the entry code section is.
If the section is present…

- Input data less than 4 bytes enters at section zero
- if there is an entry in the table matching the first 4 bytes of input data, that index + 1 is the entry section
- If non match, section zero is the entry
- the table must be sorted, so you can do a binary search.
- 4 byte selectors are meant to match solidity function selectors.

1. I’m not sure if we need flags.  There are bytes we can use in the type section if needed.  A new EIP for each flag.
2. I would prefer system contracts (precompiles) to peek data out from the transaciton.  Opcode space is getting crowded with opcodes that sometimes lose meaning in rollups and other applications such as off-chain compute.

---

**frangio** (2024-10-19):

I’d like to better understand the main goal of this proposal. Is it to:

1. have account validation and execution code sections be inaccessible from within the EVM,
2. dispatch AA methods in-protocol (direct jump into code section) rather than with EVM code, or
3. avoid enshrining Solidity ABI encoding in the protocol?

The last point is the one that the EIP highlights the most in Motivation but it actually seems secondary.

Separately, is SSZ easy/efficient to decode in EVM?

---

**shemnon** (2024-10-21):

I think there are two related proposals.

1. The 7701 proposal proposes a means where the native AA entry points would be inaccessible unless explicitly exposed.
2. The other proposal is to enshrine 4 byte function dispatch into the EVM, which is typical of all solidity compiled contracts.

These two proposals occupy a lot of the same design space, which is why I am trying to get them combined.  Unless the AA entrypoints need to have the option of being inaccessible I see a lot of value in making them look, act, and smell like regular solidity function calls.

There is a lot of backwards compatibility gained when using non-EOF Smart Contract Account Wallets by keeping the functionality accessible via a standard call (in addition to enshrined calls).  The question is whether we want to enable AA accounts to fail when not being used with enshrined abstraction.

---

**frangio** (2024-10-22):

My question was mainly about the current EIP-7701 proposal. I wanted to make sure I understood the main problems this EIP is addressing. I think that can also help to understand if it makes sense to combine those two proposals. At least from the current text in the EIP it seems like avoiding Solidity ABI encoding is a main goal.

I hadn’t read the previous discussion until now.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> Reconsider specifying ssz encoding of data
>
>
> Clients are not yet mandated to implement, but more importantly robust solidity libraries handling SSZ do not exist yet, and the efficiency of SSZ in the EVM is an open question. This is an issue that may be overcome in time, but I don’t think Native AA is the correct place to find out. Right now the Solidity ABI is much better ingrained in the ecosystem and will result in less friction when it comes to adoption.

I see we brought up a similar point, though I think I’m more open to considering SSZ. Even though Solidity ABI is in widespread use, it’s very inefficient in terms of space, so a replacement at some point or in some cases could be good.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> Selector mode

I’m not a fan of enshrining this in the EVM. I’m not at all convinced that 4-byte selectors are the best ABI design. There’s been concrete proposals that go in other directions, for example using smaller selectors to optimize calldata use for common methods. With RJUMPV it might make sense to use sequential selectors since they’re so easy to dispatch.

---

**frangio** (2024-10-22):

I’ve been looking at the potential efficiency of SSZ in EVM. I think the main source of inefficiency is that SSZ is little-endian and needs conversion to big-endian in EVM. I think the rest can be done efficiently, but endianness may be a dealbreaker.

---

**alex-forshtat-tbk** (2024-10-29):

Our project’s high level goal is to enable full account abstraction, which includes abstracted validation, in the least opinionated way while maintaining DoS resistance.

The minimum requirement to achieve that is to separate the validation and execution steps. We also want to leave some freedom to build practical AA protocols on top of EIP-7701 by applying their choice of rules on the validation code to maintain DoS resistance.

EIP-7701 can be used for permissionless AA protocols like ERC-4337, which is our main goal.

However, it can be used to enable different models as well, both centralized and decentralized. For instance, it could also be used by permissioned intent-solvers that don’t apply any restrictions, but do sponsor gas for their users and handle DoS mitigation at their centralized RPC service.

So, I would not describe the main goal of EIP-7701 as a simple in-protocol dispatch mechanism to replace solidity functions.

It is a mechanism to define and assign protocol-level **roles** to contracts. These roles are taken by contracts who implement the appropriate methods, and calls to these methods and their effects have special meaning to the protocol.

We also define a pair of such roles: “account” and “paymaster”.

For example, a contract becomes an **account** if it has a validation code section.

The validation code section of an account:

1. cannot be called or accessed externally within the EVM, but only as part of an EIP-7701 transaction type validation (it is “called” and executed by a protocol)
2. a transaction with a revert in the validation section call cannot be included in the block
3. a successful call to the validation code means the transaction is in fact valid (and the account can be charged for its gas)

These rules can be attached to Solidity functions by name, which is what we did in RIP-7560.

However, this required a number of compromises and using EOF code sections with some AA dispatching seemed to be more suitable for Ethereum post-EOF.

Regarding the SSZ encoding, it has now been removed.

The data needed by the validation section will probably be provided as an ABI encoding, but this part is not final and we do not have any strong feelings about it.

The options we have discussed as a mechanism to deliver the transaction information are:

1. Provided as a calldata with either ABI encoding or any other more efficient encoding
2. An opcode or a set of opcodes to do the same (similar to ORIGIN, GASPRICE, etc.)
3. A precompile contract that returns the details of the current EIP-7701 transaction

Each of these options has its pros and cons and any feedback is appreciated.

---

**frangio** (2024-10-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alex-forshtat-tbk/48/1453_2.png) alex-forshtat-tbk:

> The options we have discussed as a mechanism to deliver the transaction information are:

A fourth option is to use a combination of stack elements and calldata. In particular, single-word values would be provided to the entry point directly on the stack, and variable-length values provided in calldata. For sender validation, there are three variable-length values that would be concatenated in calldata, so you would need to include some extra information on the stack like the offset and length of each one, or just the two offsets where one ends and another starts.

This removes the need to do ABI encoding or decoding.

---

**frangio** (2024-11-02):

More thoughts on the fourth option. While using the stack for inputs seems feasible (to me at least), using the stack for outputs seems incompatible with the `RETURN` opcode.

---

**frangio** (2025-04-12):

What is the best place to get updates on this effort?

---

**j1729labs** (2025-04-13):

[quote=“alex-forshtat-tbk, post:1, topic:19893, full:true”]

Great to see continued exploration toward native AA. One key advantage of extending the EOF format is that it aligns better with long-term EVM evolution goals and avoids Solidity/ABI coupling. Curious to hear thoughts on how this proposal balances compatibility with existing tooling while moving toward a more minimal native AA interface.

---

**vbuterin** (2025-04-13):

EIP-7701 itself just got updated quite a bit in the past week:



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7701)





###



Native Account Abstraction protocol, relying on EOF code sections, new transaction type and a family of opcodes










Significant simplifications.

---

**alex-forshtat-tbk** (2025-04-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> What is the best place to get updates on this effort?

Hello [@frangio](/u/frangio), you are right, this thread should be the place to get updates.

Here is a short summary of the changes we’ve made to the EIP-7701 recently and a short rationale for the change:

1. Complete removal of any reliance on ABI encoding, for both inputs and outputs of all frames.

Previously, we suggested exposing the ABI encoding of transaction parameters directly as “calldata”, but this approach has some downsides. Most importantly, it makes the ABI encoding itself a part of the EVM specification, which was never the case.

1. Introduction of the TXPARAM* opcodes

We still need to provide these transaction parameters to the validation frames, which we now suggest doing via `TXPARAM*` opcodes, which behave similarly to `CALLDATA*` opcodes. As we need to provide 23 parameters and we probably don’t want to introduce 23 new opcodes, we chose to have `TXPARAM*` opcodes accept the parameter index as an “immediate argument”.

These opcodes are currently limited to the validation frames and are not available during the execution.

1. Made the time range validity parameters part of the transaction payload

Previously, we had the validation frames return the `validAfter` and `validUntil` parameters. This was a pattern introduced in [ERC-4337](https://eips.ethereum.org/EIPS/eip-4337) intended to support the “session keys” use-case in AA contracts that have no access to the `TIMESTAMP` opcode due to [ERC-7562](https://eips.ethereum.org/EIPS/eip-7562) rules.

For now, it seems like having these parameters be a part of the transaction payload is beneficial, and even that the use of the `TIMESTAMP` opcode may be acceptable in validation frames in certain scenarios.

1. Removed the explicit Paymaster “postOp context”

As there is now an [EIP-1153](https://eips.ethereum.org/EIPS/eip-1153) transient storage, returning the “context” from the paymaster validation frame is no longer necessary to access this data in the “postOp frame”.

Together, these two changes mean that it is enough for the validation frame to return without reverting to be considered valid.

1. Added the Non-EOF Proxy Contract Support

Previously, the “lookup” for the code section with a specified role happened directly for the contract at the address specified as Sender, Deployer, or Paymaster. Now, this role lookup can be satisfied by any contract that runs in its context via a `(EXT)DELEGATECALL` opcode.

This change makes the concept of “roles” both backward- and forward-compatible for upgradeable contracts. This should also work out of the box with EIP-7702.

This list is not exhaustive, but I think it covers the biggest changes we have made. I appreciate any feedback and questions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/j1729labs/48/14839_2.png) j1729labs:

> Curious to hear thoughts on how this proposal balances compatibility with existing tooling while moving toward a more minimal native AA interface.

Of course, there is a need to make certain updates to the existing tooling around Account Abstraction. Specifically, the Solidity compiler will need to implement a couple of new features to support EIP-7701, as well as any tool that relies on transaction tracing in any way. But for regular users, as well as developers of Smart Accounts and Paymasters, changes that are required are supposed to be minimal.

---

**dror** (2025-04-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alex-forshtat-tbk/48/1453_2.png) alex-forshtat-tbk:

> This change makes the concept of “roles” both backward- and forward-compatible for upgradeable contracts

Specifically, this means that any existing upgradeable account (either ERC-4337 accounts, Safe accounts or any other account using a DELEGATECALL-based proxy) can upgrade to an EIP-7701 native AA account.

---

**frangio** (2025-04-15):

Thanks for the summary!

> The TXPARAM* opcode family provides the Account Abstraction contracts with access to this data.
>
>
> These values are not made accessible to the transactions’ execution or to legacy transaction types. This limitation prevents the TXPARAM* opcode family from becoming a new source of a globally observable state

Isn’t this argument weakened given that the data can be “leaked” into the execution frame through transient storage?

> 0x12
> accessList hash
> 32
>
>
> 0x13
> authorizationList hash
> 32

Are these hashes already available or do they need to be computed when requested?

What would be the gas cost of the `TXPARAM*` opcodes?

It’s interesting that the `*Data` parameters are available via `TXPARAM*` but also passed as calldata to each frame, so it seems like they wouldn’t be needed.

---

**alex-forshtat-tbk** (2025-04-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> Isn’t this argument weakened given that the data can be “leaked” into the execution frame through transient storage?

Yes, it can, however some “leaked” transaction data is probably, at least to a certain degree, inevitable with the current approach to Account Abstraction. It is not inherent to the `TXPARAM*` opcodes.

However, this “leaked” global state only affects Sender and Paymaster smart contracts that actively choose to workaround the limitations we put on `TXPARAM*` opcodes, by storing these opcodes’ data in transient storage during validation and knowingly reading this transient state during execution. This “leaked” data cannot be “accidentally” used by a third-party contract the way `tx.origin` can be used anywhere and cause issues.

I think this distinction justifies putting the limits on the new opcodes, but I am open to making these opcodes unrestricted as well.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> Are these hashes already available or do they need to be computed when requested?

Right, I don’t think they are currently computed, but I assume the cost of calculating this hash can be covered by the transaction stipend. As a more complex alternative, accessing these two may cost some extra gas for the first time they are accessed or something like that.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> What would be the gas cost of the TXPARAM* opcodes?

Right, this is missing from the EIP. Do you see a reason these opcodes should have a gas cost different from the `CALLDATA*` opcodes? If not, I think I will just add this pricing to the EIP for now.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> It’s interesting that the *Data parameters are available via TXPARAM* but also passed as calldata to each frame, so it seems like they wouldn’t be needed.

Right, I think we don’t need to pass the `*Data` parameters as `calldata` in the validation frames any more, so we can totally avoid this duplication. However for the execution frame we can still do it because it is simple enough and because `TXPARAM*` opcodes are not available there, at least currently. What do you think?

---

**alex-forshtat-tbk** (2025-05-09):

Hello everyone!

With the recent ACD decision to remove EOF from Fusaka (more details here: [Update EIP-7607: Remove EOF from Fusaka by timbeiko · Pull Request #9703 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9703)), we made some necessary changes to EIP-7701 to decouple these proposals.

The previous version of EIP-7701 has made EOF containers and code sections a requirement, however most of the Native Account Abstraction design has remained unaffected by its removal.

Here is the list of major changes made in the last update ([Update EIP-7701: Removing dependency on EOF (#21) by forshtat · Pull Request #9734 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9734)):

1. Introduction of the ACCEPTROLE opcode

In the previous version, the invoked smart contracts immediately “knew” what is the “role” of the current call by having the EVM call into entirely different sections of their bytecode.

Successfully returning from these code sections indicated the contracts’ approval of the proposed “role” (i.e. `Paymaster`, `Account`, etc).

In a new version, we remove any dependency on AA-specific code sections. Instead, the new `ACCEPTROLE` opcode is introduced and the invoked contract has to use it to explicitly accept the proposed “role”.

In order to find out which “role” is currently executing, the contract must use the `TXPARAMLOAD` opcode with an argument `current_frame_role`.

The addition of the `ACCEPTROLE` opcode eliminated the need for the EVM to provide any kind of function dispatch mechanism, so this is potentially a major simplification of the overall architecture.

1. Removal of any proposed modifications to the EOF code container

Regardless of the future of [EIP-3540](https://eips.ethereum.org/EIPS/eip-3540), the combination of the `ACCEPTROLE` opcode and the `TXPARAMLOAD` opcode removes the need to make the EOF container explicitly aware of Account Abstraction.

Any future modifications of the EVM, or even its potential replacement, will be able to use EIP-7701 transactions using these opcodes or their corresponding system calls.

1. Clearly define the limitations applied to the TXPARAM* opcodes

Previously the rules of which parameters are available in which frame were not formally defined. The default behaviour was also not clearly stated.

This is now addressed with the introduction of the “allowed `txparam_id`” table.

---

To elaborate a bit further, this is how we expect these opcodes to be used in real-world contracts:

On a bytecode level, the first thing that the `Factory`, `Paymaster` or `Account` contracts do is perform a `TXPARAMLOAD(current_frame_role)`, and use the result to dispatch the code to the appropriate function.

In Solidity this dispatching may be a part of Solidity language specification, as an `@annotation`, a keyword modifier like `payable`, or a special function name like `receive` and `fallback`.

For the function marked this way the `return` keyword is compiled into a `ACCEPTROLE(current_frame_role)` sequence instead of the `RETURN` opcode to accept the role.

So in terms of how the contracts’ source code will probably look in the future, the EIP-7701 transaction still performs multiple call frames like before - just not using EOF code sections for it.

For example, this is what a Paymaster contract could look like:

```solidity

contract EIP7701Paymaster {

	@PaymasterValidation
	function validateTransaction() external {
        // perform validation
        return;
    }

	@PaymasterPostOp
	function postOp() external {
        // perform the post-op action
        return;
    }

}

```

In conclusion, we believe that the last two changes represent a significant improvement and simplification over the original proposal, moving EIP-7701 closer to its final form and to being proposed for inclusion in upcoming hard-forks.

All feedback is highly appreciated.

---

**frangio** (2025-09-12):

If you’re still interested in using immediates for the opcodes defined in this EIP, you can do so without EOF using the same recipe I’m applying to EIP-663 in this PR:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/10298)














####


      `master` ← `frangio:663-sans-eof`




          opened 01:05AM - 07 Sep 25 UTC



          [![](https://avatars.githubusercontent.com/u/481465?v=4)
            frangio](https://github.com/frangio)



          [+113
            -39](https://github.com/ethereum/EIPs/pull/10298/files)













See the section “Disallowed immediate range” under Rationale for the explanation.

For this EIP it’s even simpler because `txparam_id` can only be one of very few values. As long as none of those are 0x5B or 0x60 to 0x7F, the new instruction is backwards compatible.

