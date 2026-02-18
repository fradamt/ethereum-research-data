---
source: magicians
topic_id: 19047
title: "EIP-7645: Alias ORIGIN to SENDER"
author: cyrus
date: "2024-03-04"
category: EIPs > EIPs core
tags: [opcodes, account-abstraction, security]
url: https://ethereum-magicians.org/t/eip-7645-alias-origin-to-sender/19047
views: 1590
likes: 2
posts_count: 6
---

# EIP-7645: Alias ORIGIN to SENDER

Hello Ethereum Magicians.

A simple standalone EIP (7645) has been created for aliasing ORIGIN to SENDER which cleans up origin tech debt, closes security holes and lays the groundwork for account abstraction. If AA is going to happen, ORIGIN must be dealt with one way or the other. The choice is between solving it cleanly, universally and finally as proposed herein or leaving it as-is + working around it within the “winning” AA proposal, whatever it becomes. We look forward to hearing your thoughts.

Some discussion in the Eth R&D Discord #future-eoas channel [here](https://discord.com/channels/595666850260713488/718596092828057631/1210690513750073394).

PR [here](https://github.com/ethereum/EIPs/pull/8283).

## Abstract

This EIP proposes aliasing the ORIGIN opcode to the SENDER opcode within the Ethereum Virtual Machine (EVM). The purpose of this change is to move Ethereum closer to enabling account abstraction by harmonizing the treatment of externally owned accounts (EOAs) and smart contracts and to address the security concerns associated with the use of ORIGIN that have and will continue to surface in all or most account abstraction proposals.

## Motivation

The ORIGIN opcode in Ethereum returns the address of the account that started the transaction chain, differing from the SENDER (or CALLER) opcode, which returns the address of the direct caller. The use of ORIGIN has been discouraged and deemed deprecated since mid-2016 due to the security problems it introduces, such as susceptibility to phishing attacks and other vulnerabilities where the distinction between the original sender and the immediate sender can be exploited.

For instance, if an ERC-4337 bundler has tokens or other authority in a smart contract determined by ORIGIN, any of the transactions it bundles can hijack this authority since ORIGIN remains the bundler address throughout each child transaction.

More apropos in the current context of EVM evolution, the differentiation between the ORIGIN and SENDER opcodes presents a challenge for all account abstraction efforts, such as those outlined in EIP-7377 and EIP-3074, because any move towards account abstraction must address the ORIGIN opcode’s role, either by modifying or completely bypassing it. Without addressing this, the ORIGIN opcode stands as a barrier to the evolution of Ethereum’s account model towards greater flexibility and functionality.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

This EIP proposes the alteration of the behavior of the ORIGIN opcode within the Ethereum Virtual Machine (EVM). Currently, the ORIGIN opcode returns the address of the original transaction initiator. Under this EIP, the ORIGIN opcode would, instead, return the same value as the SENDER opcode, which is the address of the immediate sender of the message or transaction.

Definition Change: The ORIGIN opcode (0x32) MUST, in all contexts of execution, return the same value as that returned by the SENDER (also known as CALLER) opcode (0x33).

EVM Implementation: All Ethereum clients MUST implement the following change to the EVM: Whenever the ORIGIN opcode is called, the value to be pushed onto the stack is the current call’s sender address, as if the SENDER opcode was executed instead.

Transaction Validation: Transactions MUST be validated as before, with no changes to the transaction structure or processing logic beyond the EVM opcode behavior specified above.

Compatibility: Smart contracts relying on the ORIGIN opcode for obtaining the transaction initiator’s address MUST be reviewed to ensure they function correctly under the new definition and worked-around or avoided if this EIP introduces breaking changes.

Implementers are encouraged to provide feedback on this specification and report any potential issues encountered during the implementation or testing phases.

## Rationale

The rationale behind aliasing ORIGIN to SENDER is to:

Facilitate Account Abstraction: Elegantly nullify a universal barrier to account abstraction, enabling more flexible and powerful account models in Ethereum.

Enhance Security: Eliminate the security vulnerabilities associated with differentiating between the original transaction initiator and the immediate caller.

Clean up tech debt and simplify the EVM Model: Reduce the complexity of the EVM’s transaction and execution model by removing an outdated and deprecated feature, making future changes easier and safer.

## Backwards Compatibility

This change is not fully backwards compatible. Contracts relying on the distinction between ORIGIN and SENDER for logic or security will be affected. However, given the longstanding discouragement of ORIGIN’s use, the minimal impact of the change, the widespread desire for a future account abstraction solution in the EVM, and the reality that any AA solution will ultimately have to deal with ORIGIN one way or the other, this incompatibility is considered a necessary step forward for Ethereum’s development.

No backward compatibility issues found.

## Test Cases

For each CALL, STATICCALL, DELEGATECALL, CALLCODE:

Direct - Ensure that, at the target smart contract, ORIGIN and SENDER produce the same value. (For simple no-hop EOA-to-EOA/SCA transactions, this is already the case today.)

Multi-hop - Ensure that, at each frame in a multi-hop transaction, ORIGIN and SENDER produce the same value.

## Security Considerations

By aliasing ORIGIN to SENDER, the specific security vulnerabilities associated with the ORIGIN opcode are addressed and eliminated. Outside the scope of this EIP, it may be wise to ban all use of ORIGIN to eliminate further misunderstanding or misuse. This can be done via tooling changes outside the EVM or, inside the EVM, reverting smart contract deployments that use ORIGIN.

For existing misuse of ORIGIN affected negatively by this aliasing to SENDER (of yet a clear example has yet to be identified), it may be necessary to educate users to avoid this problematic legacy code.

## Replies

**0xTraub** (2024-03-04):

While I agree that we need a better way to distinguish AA transactions, at present because bytecode isn’t stored until the end of a constructor call, `require(msg.sender == tx.origin)` is the only way to be certain that the address interacting with a contract is an EOA. Can you elaborate on how the solidity compiler/developers should handle this going forward, since a `require(msg.sender.code.length == 0)` check can be easily bypassed?

Also, what do you suggest for backwards compatibility since there’s a lot of contracts right now implementing this `tx.origin == msg.sender` check which would immediately be nullified?

---

**cyrus** (2024-03-05):

[@yoavw](/u/yoavw) from 7377 discussion:

> tx.origin hashing - nice way to placate these projects, but should we?
>
>
> tx.origin “protection” has been proven problematic many times in the past.
> It is one of the two biggest obstacles to AA adoption (the 2nd one being lack of EIP-1271 support).
> AA might never become a 1st class citizen if we don’t let contract accounts be tx.origin.

The situation is:

- We can’t get first-class AA without addressing tx.origin
- We can’t address tx.origin (either in 7645 or in the AA solution itself) without breaking stuff
- The stuff we would “break” is already “broken”, having been advised against since mid-2016

Quoting [@MicahZoltu](/u/micahzoltu) from the #future-eoas Discord channel:

> This pattern is flagged by every auditor out there, and plastered all over docs, tutorials, etc. None the less, people do stupid things when they are allowed, even when you tell them not to.

[@yoavw](/u/yoavw) again from the 7377 discussion

> [require(tx.origin == msg.sender)] often doesn’t achieve its goal. Some projects added this check as a knee-jerk reaction to flashloans when they came out. But a miner (or now block builder) could always perform the same attack by bundling transactions to bring liquidity, perform the attack, and pull the liquidity out.

How to let contract developers *reliably* know if they’re dealing with a smart contract or, more to the point, simply avoid problems if caller *is* a smart contract is outside the scope of this EIP.

So the question is: “are we going to let advised-against, misuse of tx.origin to stop us from eliminating this tech debt and moving Ethereum forward with AA?”

I understand people saying “we shouldn’t be opinionated about what opcodes someone use if they are available.” My response to that would be that we are opinionated that developer shouldn’t use gas prices for critical logic, right? But via Murphy’s law, they probably have. That hasn’t stopped us from adjusting gas prices when necessary. How is fixing tx.origin any different?

Back to this EIP: shouldn’t we fix tx.origin simply, elegantly and finally in this manner now rather than spaghetti-coding around it later and forever? I’d almost rather abandon AA altogether than do the latter, but I might be in a minority on that.

---

**0xTraub** (2024-03-05):

spaghetti at the wall idea here, but what if we introduce a new opcode which returns the top level contract interacted with, maybe something like `ENTRYPOINT`. If it’s an EOA transfer it just returns the zero address. Then you could check that the value of the opcode was the known entrypoint contract for 4337 and perform more specific checks based on that. This might allow devs to implement an additional check where maybe something like

```auto
if (msg.sender != tx.origin) require(tx.entrypoint == ENTRYPOINT_CONTRACT);
```

[This idea has been discussed slightly here but needs more work first](https://ethereum-magicians.org/t/globally-available-tx-opcodes-in-solidity/13471)

---

**SamWilsn** (2024-03-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xtraub/48/7553_2.png) 0xTraub:

> require(msg.sender == tx.origin) is the only way to be certain that the address interacting with a contract is an EOA

You can also require a signed message (verified with `ecrecover`.) I would warn against trying to detect EOAs generally though.

---

**Vectorized** (2024-12-10):

Not in favor of this EIP.

`tx.origin` is super useful when initializing the owner for a contract deployed via a create2 factory.

Otherwise, developers will need to hardcode deployer addresses into their implementations. This is infeasible for open source contracts intended to be deployed by anyone.

Mining deterministic addresses for implementations with variable constructor arguments is extremely cumbersome. There is no available ready made tooling for it today.

