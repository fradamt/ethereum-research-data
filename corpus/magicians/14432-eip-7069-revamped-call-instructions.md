---
source: magicians
topic_id: 14432
title: "EIP-7069: Revamped CALL instructions"
author: axic
date: "2023-05-25"
category: EIPs > EIPs core
tags: [evm, opcodes]
url: https://ethereum-magicians.org/t/eip-7069-revamped-call-instructions/14432
views: 2997
likes: 5
posts_count: 16
---

# EIP-7069: Revamped CALL instructions

Discussion topic for



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7069)





###



Introduce CALL2, DELEGATECALL2 and STATICCALL2 with simplified semantics

## Replies

**Philogy** (2023-06-05):

Reading the EIP, it’s unclear how “failure” of a call is defined. I assume “failure” is when the call can’t be initiated due to the contract’s `balance < value` or there being insufficient remaining gas? Are there any other constellations that would constitute a “failure” pushing the status code `2` onto the stack? An exceptional revert in the call context would still be considered a “revert” and not a “failure”, right?

---

**axic** (2023-06-06):

`revert` is only returned if the callee uses the `REVERT` instruction. Should clarify it.

---

**axic** (2023-06-06):

Historical context: these reworked `CALL` instructions were discussed starting late December when certain unobservability properties were required from EOF. The basic specification was discussed in January and until now kept in the “EOF mega spec”:

https://notes.ethereum.org/@ipsilon/mega-eof-specification

Creating the EIP is the next step, especially as it is not strictly dependant on EOF.

---

**petertdavies** (2023-06-06):

> Note: Unlike CALL there is no extra charge for value bearing calls.

What is the justification for this?

Currently the cheapest way to change a value in a MPT is by modifying a storage key. This costs 5000 gas, leading to a theoretical limit 6000 MPT writes per block under current gas limits. Under this EIP, using the `CALL` opcode you can modify the balance of an account for only 2600 gas, raising the theoretical limit to 11538 MPT writes per block.

MPT writes are likely to be expensive. Each MPT write incurs multiple database writes (due to a trie node updates) compared to a singe database read for an MPT read. Charging the same for a read and a write seems questionable.

I agree with [@Philogy](/u/philogy) that non-malicious code overpays for value carrying calls in practice, but I’m concerned this might be DOS vector.

---

**Philogy** (2023-06-06):

So the “revert state” **does not** include e.g. `INVALID` (0xfe) and exceptional reverts due to e.g. missing jumpdest, insufficient stack args, out-of-bounds returndatacopy?

---

**gumb0** (2023-06-07):

Correct, all these cases result with status code 2 on stack.

---

**sbacha** (2023-06-10):

HELL YES FINALLY

> It is also useful to have these as new opcodes instead of modifying the exiting CALL series inside of EOF. This creates an “escape hatch” in case gas observability needs to be restored to EOF contracts. This is done by adding the GAS and original CALL series opcodes to the valid EOF opcode list.

---

**charles-cooper** (2023-08-10):

Because the proposed instructions remove the output buffer, I think this proposal needs to include a `RETURNDATALOAD` instruction to be complete.

Here’s why: to replicate current `CALL` semantics, you need to add extra instructions to copy from returndata into an output buffer (which, I think the best you could do is `returndatacopy output_buffer 0 (min returndatasize buf_size)` – the best implementation I have for `min` here is something like `push2<buf_size> returndatasize dup2 xor push2 <buf_size> returndatasize lt push2<buf_size> mul xor`). Currently, copying into memory is important because it improves the performance of ABI decoding.

Introducing `RETURNDATALOAD` allows for (efficient) ABI decoding directly from the returned data and would solve the above concerns because we can skip copying to memory, also allowing us to skip returndatasize checks on account of the OOB semantics of `RETURNDATACOPY`/`RETURNDATALOAD`.

---

**frangio** (2023-08-14):

This EIP is related to the project of removing gas observability. I want to raise that the ability to observe “out of gas” errors might be necessary, that it’s not really possible with the current instruction set, and that a solution to this problem might be a good fit for this EIP.

The issue is that whenever a contract has logic such as “try this call, and if it reverts do this other thing”, due to EIP-150 there is a chance that the transaction originator can force a contract to follow the “catch” path by triggering the subcall to run out of gas while providing enough gas for the rest of execution to continue (perhaps more so with the introduction of MIN_RETAINED_GAS?). An example where this pattern could be used is to call a getter and have a fallback value if the getter is not implemented. Ideally, the contract would be able to specify that if the subcall reverts out of gas it should not continue execution and should revert. With the revamped CALL instructions this is semi-possible, because through the status code you can distinguish explicit revert from out of gas failure. However, the out of gas error can be triggered in a more deeply nested call, and in this case the “failure” information is lost in the outer scopes.

My proposal is to encode in the status code whether the call or any nested subcall ran out of gas. This would allow detecting that the code is operating without sufficient gas available.

---

**gumb0** (2023-09-22):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/p/4bbf92/48.png) petertdavies:

> Note: Unlike CALL there is no extra charge for value bearing calls.

What is the justification for this?

We have added a charge for calls with value, thank you for bringing this up [Update EIP-7069: Add charge for value-bearing calls by gumb0 · Pull Request #7220 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/7220)

---

**pdobacz** (2024-03-05):

[@charles-cooper](/u/charles-cooper) [@ekpyron](/u/ekpyron) There’s a topic we’d like some feedback on.

The revamped calls change the stack return values from

0-failure, 1-success - for original CALLs

to:

0-success, 1-revert, 2-failure (and possibly more failure codes [c.f. this PR thread](https://github.com/ethereum/EIPs/pull/8287/files#r1513021952)

Note that success and failure are flipped. Would this be problematic? In particular (from [@shemnon](/u/shemnon) ):

> I have concerns about flipping the outputs of calls.  e.g. 1 is success vs 0 is success.  Specifically for how it will impact the low-level call functions - Units and Globally Available Variables — Solidity 0.8.26 documentation (call, delegatecall, staticcall) as well as inline assembly.  Have solidity and vyper chimed in on it on how they would handle it?  i.e. would there be compatibility for call and friends and a new variant that will only work when the EOF mode is flipped? and inline assembly would fail if compiled with the wrong mode?

---

**charles-cooper** (2024-03-05):

Flipping would not be problematic – in fact it’s a slight improvement because you can use JUMPI to the shared revert block instead of ISZERO … JUMPI.

---

**ryley-o** (2024-06-10):

I have concerns regarding preventing all external calls from being able specify less than 63/64 of the overarching transaction’s gas. EOF1 removes `CALL`, so the new `EXTCALL` is the only option available, but with regressed functionality.

I think there are many important use cases where giving the developer control of the gas available to an individual `EXTCALL` is important to avoid certain attack vectors. Examples include:

- executing arbitrary instructions on behalf of multiple users in a single transaction, e.g. account abstraction ERC-4337. The EIP defines a User Operation parameter callGasLimit, which the reference implementation in the EIP enforces on each call: account-abstraction/contracts/core/EntryPoint.sol at 04ee30e3130dc1145ad7032318cf841909a8bc71 · eth-infinitism/account-abstraction · GitHub

without enforcing on each call, there is likely an attack vector opened where a tx can use more gas than estimated when actually executed, and the following logic in ERC-4337 becomes invalid: “If the call reverted, the bundler MUST use the trace result to find the entity that reverted the call. This is the last entity that is CALL’ed by the EntryPoint prior to the revert.”

while not a preferred pattern, the widely used “safeSendETH” pattern, where a `GAS_STIPEND_NO_GRIEF` is tried before falling back to an expensive `SENDALL`, becomes impossible.

- see popular implementation in solady repo here: solady/src/utils/SafeTransferLib.sol at main · Vectorized/solady · GitHub

I think the reasons above are enough to consider updating revamped call instructions to include a configurable gas limit. Curious if I’m missing anything though!

---

**shemnon** (2024-06-12):

One of the important design considerations for EOF is that we really have only one window to remove features, which is the first release.  We don’t want to support multiple versions of base level EOF across the chain.  However adding in items that make a previously invalid contract valid is a “forwards compatible chainge” that won’t require maintaining multiple simultaneous EOF versions.

With that in mind, we decided to address gas observability in a way that we can fall back on.  We banned GAS and introduced new gas-agnostic call operations.  If we do determine that we truly need gas limiting calls we can restore the old calls like we were adding new opcodes, in a forwards compatible way.

One major issue we have had with EVM evoluton is when contracts hard-code in gas values.  This prevents safe transitions to a new gas schedule.  If contracts were not allowed to limit gas on calls then all contracts can still work with dramatic gas cost changes (like the SSTORE changes seen in Tangerine Whistle/EIP-150). However those schedule changes broke a number of contacts. This is the main motivation for removing gas observability: any gas schedule change can be addressed by end users simply sending more gas.  If the contract can limit the gas it won’t matter how much they send if the reserved amount is still below the new execution cost.

For the listed problems, contracts can continue to use Legacy EVM until a better replacement is implemented.  In the two cases listed I think there are better options than gas limited call operations.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ryley-o/48/9317_2.png) ryley-o:

> executing arbitrary instructions on behalf of multiple users in a single transaction, e.g. account abstraction ERC-4337.

The best solution would be protocol enshrined Account Abstraction, which can execute a signed UserOperation, which includes a gas limitation that comes from outside the contract.  There are other options that should be investigated first before restoring gas introspection, such as adding a new “spawn” operation or system contract that will create a new transaciton and it can be gifted gas from the parent caller.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ryley-o/48/9317_2.png) ryley-o:

> while not a preferred pattern, the widely used “safeSendETH” pattern, where a GAS_STIPEND_NO_GRIEF is tried before falling back to an expensive SENDALL, becomes impossible.

The PAY opcode would be a strictly superior answer to this pattern.  I expect we will see it in the first fork after verkle ships.

---

**ryley-o** (2024-06-12):

Thanks for the perspective here. Especially appreciate the point about this being the best chance to remove functionality.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> The best solution would be protocol enshrined Account Abstraction, which can execute a signed UserOperation, which includes a gas limitation that comes from outside the contract. There are other options that should be investigated first before restoring gas introspection, such as adding a new “spawn” operation or system contract that will create a new transaciton and it can be gifted gas from the parent caller.

I think it’s safe to say that we agree that *some* method of controlling gas for each UserOperation is required here, and that the initial EOF implementation won’t support that in Pectra, right? It does make sense that different protocol-level solutions may be preferred, so I understand that relying on legacy contracts in the interim may be ideal since this is the main chance to remove functionality.

… and yes, PAY is much more ideal!

