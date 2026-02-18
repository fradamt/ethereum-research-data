---
source: magicians
topic_id: 27617
title: "EIP-8141: Frame Transaction"
author: matt
date: "2026-01-29"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-8141-frame-transaction/27617
views: 385
likes: 30
posts_count: 32
---

# EIP-8141: Frame Transaction

Add a new transaction whose validity and gas payment can be defined abstractly. Instead of relying solely on a single ECDSA signature, accounts may freely define and interpret their signature scheme using any cryptographic system.


      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-8141)



    ![](https://eips.ethereum.org/assets/images/eip-og-image.png)

###



Add frame abstraction for transaction validation, execution, and gas payment

## Replies

**thegaram33** (2026-01-29):

This looks great!

What happens if there are multiple `VERIFY` frames that return `APPROVE(0x1)` or `APPROVE(0x2)`? Does that invalidate the transaction, or the first/last will pay for gas?

---

**fjl** (2026-01-29):

As per Behavior section, if a frame exits with 2, 3, or 4, and the corresponding variable (`sender_approved`, `payer_approved`) is already set to true, the frame reverts. So only the first approval counts. Redundant/conflicting approvals do not invalidate the transaction.

---

**thegaram33** (2026-01-29):

Makes sense. So it is possible that some frames revert, while the rest do not.

Is there a way to implement “atomic multicall” functionality with this then? I.e. given multiple `SENDER` frames, either all of them succeed or all revert?

---

**fjl** (2026-01-29):

~~There is no feature for introspecting the status code of other frames in the transaction.~~ Edit: actually, we do have that, using TXPARAMLOAD (0x15).

You can also check for a revert by inspecting the effects of the frame. But performing multiple SENDER frames is equivalent to a single SENDER frame that batches the calls.

It should not be possible to make the entire transaction invalid after some SENDER frames have already been processed. So the only way this could be done is by adding a preamble to each SENDER frame that asserts whether the previous frame reverted, and make the current frame also revert in that case.

---

**Helkomine** (2026-01-29):

> The payload is defined as the RLP serialization of the following:
>
>
> [chain_id, nonce, sender, frames, max_priority_fee_per_gas, max_fee_per_gas, max_fee_per_blob_gas, blob_versioned_hashes] frames = [[mode, target, gas_limit, data], …]

I think there’s no need for multiple call frames at the protocol level, because the atomicity of these frames isn’t organized efficiently enough. For comparison, [UniversalRouter](https://docs.uniswap.org/contracts/universal-router/overview) allows nested call frames of arbitrary depth, as well as the ability to isolate unrelated calls or bind them in various ways. A more reasonable approach would be to have a maximum of 3 call frames. One is for `DEFAULT`, one for `VERIFY`, and the other for `SENDER` the execution of data in the `SENDER` will be determined by the contract.

> The EIP-7702 authorization list heavily relies on ECDSA cryptography to determine the authority of accounts to delegate code. While delegations could be used in other manners later, it does not satisfy the PQ goals of the frame transaction.

Why are we willing to complicate the protocol by introducing new transaction formats and a lot of code when a simpler approach would be to periodically add new signature schemes/delete old signature schemes for the authorizarion_tuple?

> TXPARAM* opcodes

I like this idea because it allows access to nonce, hopefully it will be implemented soon.

---

**shemnon** (2026-01-29):

Before I dive in completely, is there any reason the DeFi use case wasn’t listed in the examples? Frame 0 verify, Frame 1 approve, Frame 2 swap? I wonder if focusing examples on the PQ motivation undersells the immediate use case that the community has been asking to get for years.

---

**matt** (2026-01-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> Before I dive in completely, is there any reason the DeFi use case wasn’t listed in the examples? Frame 0 verify, Frame 1 approve, Frame 2 swap?

Mostly because defi use cases can be realized today with several mechanisms: smart accounts, 4337, 7702. There are also endless alternative proposals to achieve what you outlined.

The motivation for 8141 is about solving the protocol’s ECDSA problem in accounts. Obviously this has high overlap with AA and UX, and we should keep it in mind, we do primarily want to offer a robust and flexible platform to begin migrating accounts to. Give that there there will be further improvements to PQ crypto systems over time, AA is the perfect mechanism to realize PQ resilience.

---

**matt** (2026-01-29):

Thanks for your questions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/helkomine/48/15936_2.png) Helkomine:

> I think there’s no need for multiple call frames at the protocol level, because the atomicity of these frames isn’t organized efficiently enough.

It’s important to understand the rationale for frames in the first place, which can do a better job expressing the EIP. Frames are required to support introspection *by the protocol*. It’s not about supporting multiple calls at the EVM layer. It’s about allowing end users to flexibly define the way their transactions should be handled. The protocol can in turn, use the modes we’re introducing to reason about the transaction and safely bound the resources needed to validate and propagate abstract transactions over p2p.

You can see in the examples, there are actually several types of use cases for this and they don’t always require three frames. We could potentially come up with the top N use cases and design the tx with those specific ones in mind, but IMO it goes against the philosophy of the protocol: expose powerful primitives for there users of the protocol to innovate on top of.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/helkomine/48/15936_2.png) Helkomine:

> Why are we willing to complicate the protocol by introducing new transaction formats and a lot of code when a simpler approach would be to periodically add new signature schemes/delete old signature schemes for the authorizarion_tuple?

Migrating EOA accounts away from ECDSA entirely **requires** a new transaction type. Today there are several potential PQ crypto systems that could be used to secure an Ethereum account, but none of them are such clear front runners that we would feel confident enshrining directly into the protocol. Not to mention, entire body of work that AA comprises of, focuses solely on making the validation phase of the transaction user-definable. It’s really the perfect combination. There are several nice things that native AA gives us beyond PQ, including reducing the number of intermediaries required to relay a transaction.

---

**Helkomine** (2026-01-30):

> It’s important to understand the rationale for frames in the first place, which can do a better job expressing the EIP. Frames are required to support introspection by the protocol. It’s not about supporting multiple calls at the EVM layer. It’s about allowing end users to flexibly define the way their transactions should be handled. The protocol can in turn, use the modes we’re introducing to reason about the transaction and safely bound the resources needed to validate and propagate abstract transactions over p2p.
>
>
> You can see in the examples, there are actually several types of use cases for this and they don’t always require three frames. We could potentially come up with the top N use cases and design the tx with those specific ones in mind, but IMO it goes against the philosophy of the protocol: expose powerful primitives for there users of the protocol to innovate on top of.

The examples you provided, and many others, are entirely achievable using command-oriented architectures like Uniswap’s UniversalRouter, at least functionally. For example, the following call frame: `{VERIFY, PAY_GAS, {DO_SOMETHING}, POST_EXEC}` where `{}` denotes execution frames in the command-line contract and the above calls are defined by the contract. The creative possibilities on these contracts are almost limitless. Your solution allows for the setup of multiple call frames with the sender being `ENTRY_POINT (0xaa)` (essentially a specific address authorized to perform checks), but a different sponsor protocol might use a different authorized contract to achieve the same effect. If your goal is to reduce reliance on ECDSA, then you don’t need to do anything - the new ERCs and signature schemes will address this issue in due course. Therefore, I don’t see any clear benefit from this proposal other than the additional burden it creates on the network. I prefer more sustainable long-term solutions (reducing the cost of the opcode ([EIP-7904](https://eips.ethereum.org/EIPS/eip-7904)), adding new signature schemes, lock EOA ([EIP-7851](https://eips.ethereum.org/EIPS/eip-7851)), …) They are more in line with the AA route but still maintain simplicity for the network.

> Migrating EOA accounts away from ECDSA entirely requires a new transaction type. Today there are several potential PQ crypto systems that could be used to secure an Ethereum account, but none of them are such clear front runners that we would feel confident enshrining directly into the protocol. Not to mention, entire body of work that AA comprises of, focuses solely on making the validation phase of the transaction user-definable. It’s really the perfect combination. There are several nice things that native AA gives us beyond PQ, including reducing the number of intermediaries required to relay a transaction.

What I mean is we don’t need to choose exactly one rigid scheme, but just change the scheme periodically, which is perfectly feasible because authorization_tuple is just an integrated part of EOA, so there won’t be many backward compatibility issues if we make changes. However, you’re right, we should discuss this in a separate proposal.

---

**matt** (2026-01-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/helkomine/48/15936_2.png) Helkomine:

> I don’t see any clear benefit from this proposal other than the additional burden it creates on the network.

To move away from ECDSA, we either 1) need a tx type with a predfined set of whitelisted (PQ) cryptographic algos 2) need to allow smart accounts to originate transactions. Obviously 2) is far more compatible with the Ethereum philosophy of giving users powerful primitives.

The UniversalRouter cannot address this without similar protocol changes, because it is a user-level construct. We don’t have any mechanism to allow it to originate a tx, at the protocol. ERC-4337 has attempted to be a user-level implementation of AA, similar to as your propose, but while looking into integration into geth, it always ended up kludgy combining the two layers.

---

**Helkomine** (2026-01-30):

> We don’t have any mechanism to allow it to originate a tx, at the protocol. ERC-4337 has attempted to be a user-level implementation of AA, similar to as your propose, but while looking into integration into geth, it always ended up kludgy combining the two layers.

Your solution focuses on addressing issues related to the originator, which I believe is a minor issue that we can solve using a minor solution. Because most contracts execute logic based on `msg.sender`, with only a small number performing `tx.origin` checks, code observation, or signature requests, these issues are neatly resolved by a single opcode statement that both disguises `ORIGIN` and eliminates code observation, let’s call it `SETORIGIN`. This opcode will thoroughly address the first two issues; regarding the third, fortunately, we have EIP-7702 which allows EOA to perform `SETORIGIN` and simultaneously use their signatures. In short, I agree that the barriers posed by initator-based censorship affect AA’s development, but the solutions to them don’t have to be as massive as this.

---

**matt** (2026-01-30):

It’s not about the value of `ORIGIN`, it’s about origination. It’s about sending a transaction. Today to pay the block builder to include a transaction there is only 1 pathway: via EOA. The frame transaction adds a second pathway: via code. To do this, it requires something like `APPROVE` to tell the builder that the gas costs can be deducted from the account and the reset of the processing can continue. The UniversalRouter cannot pay for the gas in the transactions because there is no way to signal to the client who will pay what. `SETORIGIN` doesn’t fix that.

We have already attempted a simpler proposal than EIP-8141 when we proposed EIP-2938. It was simpler and allowed you very arbitrarily define the smart contract system (UniversalRouter, etc) to determine the validity, `PAYGAS`, and execute calls. But it failed due to the lack of protocol-level introspection. It was complicated to build a p2p tx pool ruleset around it.

The frame transaction is a direct response to this. I understand that it may seem that we are skipping over simpler solutions, but I don’t think that’s the case. We have thought deeply for a long time about this and it isn’t so simple.

Please feel welcome to fully sketch out your idea, I can review it. It needs to be comparable though and allow users to define arbitrary validation functions that determine if a user transaction can pay gas and be included on-chain.

---

**Helkomine** (2026-01-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> It’s not about the value of ORIGIN, it’s about origination. It’s about sending a transaction. Today to pay the block builder to include a transaction there is only 1 pathway: via EOA. The frame transaction adds a second pathway: via code.

The only benefit of your proposed solution is perhaps limiting censorship from the sponsor’s side. In a typical `AA` transaction, a sponsor receives the user’s transaction package and analyzes it, which could expose front-running attack vectors… .  But I think this is a common problem across the entire protocol because block builders can also censor them. Your framework transaction offers limited benefits by allowing gas payments via code, which only reduces one layer of censorship from the bundler. Aside from this benefit, there is no significant difference between an `EOA` paying gas and receiving payment in ETH/ERC20 versus paying gas via code. If we propose solutions without reconsidering the core problem that creates the barrier (censorship via `ORIGIN`), we will cause solutions that negatively impact the network.

---

**matt** (2026-01-31):

The frame transaction allows sponsorship by code or by signature from a paymaster. It allows an arbitrary definition of who pays when.

Builders will not be able to censor frame transactions when combined with FOCIL, which is the expected partner headliner for Hegota. Together, they provide native censorship resistant account abstraction. This is not possible without both.

---

**nlordell** (2026-02-02):

One thing that wasn’t clear to me from the EIP is that `APPROVE` opcode includes a memory `offset` and `length` for specifying some return data, but it does not really specify what is done with this data. AFAICT there is no `TXPARAM*` way to access the return data from previous frames (like you can currently access `status`).

Is this intended? If so, what is the purpose of allowing `APPROVE` to also return data and not just a scope?

---

**matt** (2026-02-02):

Good question. We can try to clarify more in the EIP. The idea is that APPROVE is supposed to allow contracts to “approve” of a call type in nested call frames, but unroll it to the surface using the standard “return” behavior. At the top level, the return data is just the return data of the transaction. It isn’t used by the system, it’s up to developers to use it how they see fit. In the inner call frames, there might be info that needs to be propagated back to the wallet, just like RETURN.

APPROVE is really just about giving devs the natural ability to unroll approve decisions deeper in the call stack by using the existing return code convention and extending it with other codes beyond 0 and 1.

---

**nlordell** (2026-02-02):

I think I understand: the frame `target` can `CALL` another contract which halts execution with `APPROVE` (instead of `RETURN`), and the calling `target` contract can propagate the approval scope to the transaction so-to-speak (so that it observes the frame transaction rules).

If I understood correctly, does that mean that `CALL` can push more than a 0 or 1 to the stack (it can push 2, 3, or 4 for the different approval scopes) — which would deserve a mention in the backwards compatibility section IMO? It would be nice to elaborate on this a bit in the EIP.

---

**ruhil6789** (2026-02-03):

This aligns with what I have been thinking and researching regarding post-quantum signatures—an era in which the digital signature schemes we rely on today, such as RSA and ECDSA, may no longer provide sufficient security.

---

**frangio** (2026-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> We can try to clarify more in the EIP. The idea is that APPROVE is supposed to allow contracts to “approve” of a call type in nested call frames, but unroll it to the surface using the standard “return” behavior.

I don’t see this in the spec.

Do outer calls have to invoke APPROVE or is the approval status somehow automatically propagated by RETURN?

By the way, this EIP seems to be overloading the term “frame” which I believe was already in use for the nested execution contexts created by the CALL opcode. Have you considered other names? Or perhaps a qualified name such as “transaction frame”?

---

**thegaram33** (2026-02-04):

> The frame.data of VERIFY frames is elided from the signature hash […] the input data to the sponsor is intentionally left malleable.

Is the expectation here that data in `VERIFY` frames will only contain a signature and nothing else? Otherwise this malleability seems quite risky.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fjl/48/5846_2.png) fjl:

> performing multiple SENDER frames is equivalent to a single SENDER frame that batches the calls.

Given that frame transactions do not aim to solve batching (that can be done in the smart account logic), what is the point of allowing multiple `SENDER` frames?

If there is no point, it could also be considered to make the sender and payment verification fields of the top-level transaction. Otherwise this list of frames (with the corresponding list of receipts, and list of nested lists of logs) will require lots of changes in tooling, RPC, etc. (Point originally raised by [@tynes](/u/tynes)).

> Frame transactions introduce new denial-of-service vectors

If node operators and builders implement custom policies (e.g. only accept up to a certain verification gas), that raises censorship concerns.

I’m particularly concerned about the case where a user creates a smart account with a particular post-quantum signature scheme, then later builders decide to drop support for this scheme. The user might have a hard time updating their account. (Maybe FOCIL on L1 and enforced transactions on L2 can solve this.)


*(11 more replies not shown)*
