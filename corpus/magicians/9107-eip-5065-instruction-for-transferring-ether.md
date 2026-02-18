---
source: magicians
topic_id: 9107
title: EIP-5065 Instruction for transferring ether
author: maxsam4
date: "2022-05-01"
category: EIPs
tags: [evm, opcodes, core-eips]
url: https://ethereum-magicians.org/t/eip-5065-instruction-for-transferring-ether/9107
views: 4465
likes: 21
posts_count: 15
---

# EIP-5065 Instruction for transferring ether

## Abstract

Add a new instruction that transfers ether to a destination address without handing over the flow of execution to it. It should work similarly to how `SELFDESTRUCT` transfers ether to the destination without making a call to it.

## Motivation

From an architectural point of view, execution flow should never be handed over to an untrusted contract. Ethereum currently does not have any ideal way to transfer ether without transferring the flow of execution. People have come up with reentrancy guards and similar solutions to prevent some types of attacks but it’s not an ideal solution. The only way to transfer ether from smart contracts without triggering a call is to create a dummy contract, send the precise amount of ether to it and then call `SELFDESTRUCT` from it.

## Specification

Introduce a new instruction, `AIRDROP` that transfers ether to the destination without making a call to it.

### Stack input

address: the account to send ether to.

value: value in wei to send to the account.

### Gas

The total gas cost should be the sum of a static cost + address_access_cost + value_to_empty_account_cost.

- Static cost: 6700
- Dynamic cost:

address_access_cost: If the target is not in accessed_addresses, charge COLD_ACCOUNT_ACCESS_COST gas, and add the address to accessed_addresses. Otherwise, charge WARM_STORAGE_READ_COST gas. Currently, COLD_ACCOUNT_ACCESS_COST is 2600 while WARM_STORAGE_READ_COST is 100.
- value_to_empty_account_cost: If value is not 0 and the address given points to an empty account, then value_to_empty_account_cost is the account creation gas cost which currently is 25000. An account is empty if its balance is 0, its nonce is 0 and it has no code.

## Rationale

This behavior is already possible by deploying a new contract that does `SELFDESTRUCT` but it is prohibitively expensive. In most scenarios, the contract author only wants to transfer ether rather than transferring control of the execution. ERC20 can be used as a case study for this where most users transfer funds without a post-transfer hook.

This instruction allows contracts to safely pass ether to an untrusted address without worrying about reentrancy or other malicious things an untrusted contract can do on.

The static gas cost is derived by subtracting the gas stipend (2300) from the positive_value_cost of `CALL` opcode which is currently set to 9000.

## Backwards Compatibility

No known issues as this is a new instruction that does not affect any old instructions and does not break any valid assumptions since it make not anything impossible possible.

## Test Cases

TODO

## Security Considerations

No known security risks.

## Discussion points

- Gas costs - I would like them to be lower
- Should we allow EOA to transfer ether without triggering a call - Consensus is leaning towards NO. It adds an additional risk of locking mistakenly sent ether while there is no demand for the feature.
- Instruction name alternatives - REMIT/PAY/DISBURSE/GIFT/FORCESEND/BESTOW

## FAQ

Q) Why not just repurpose `SELFDESTRUCT`? It is already being planned to be used as just a force transfer.

A) `SELFDESTRUCT` transfers all of your ether. We need a way to transfer a specific amount. Also, the repurposing of `SELFDESTRUCT` might take a while longer to get into prod.

Q) Doesn’t this break the contracts that depend on the stipend?

A) Those contracts were already broken as bypassing stipend is already possible. Additionally, I do not think there are any practical contracts that get “broken” because of this. Sending money to a gnosis wallet, for example, does not break it even if you don’t end up executing its fallback function.

Q) What about the additional risk of locking ether mistakenly?

A) I agree that it does add some risk there but it’s negligible IMO. The existing contracts will work in the same old way. ERC20s have allowed and normalized forced transfers and it is a well-understood concept that I do not expect new devs to be mistakenly locking ether using this feature too often. This proposal does not recommend for EOAs to have this ability to reduce the risk of lock funds. Furthermore, tooling can warn users if a transaction force transfers ether to a contract that usually doesn’t accept ether. Considering everything, the benefits of this proposal outweigh the cons considerably IMO.

Q) Why not propose to remove stipends completely if you think they are broken?

A) Because that’s likely to have backward compatibility issues. If I was designing ETH from scratch, I would have advised against stipends but at this point, it might be too late to remove them. Well, too late to remove them without an thorough onchain analysis, at least.

Q) Why not adjust the gas given in a stipend?

A) That does not resolve the concern and promotes a bad habit of depending on gas costs. On one side, we recommend devs to not depend on gas costs and on the other, we give them a fixed gas cost to do stuff in certain scenarios. Very bad mixed messaging IMO.

## Replies

**chiro-hiro** (2022-05-01):

How does this backward compatible with older internal transfer?

---

**maxsam4** (2022-05-01):

> How does this backward compatible with older internal transfer?

It does not affect older transfers. This adds a new way to transfer ether using a new opcode.

---

**chiro-hiro** (2022-05-01):

I think, the proposal could be better if it emits some sort of event to the outside just like the behaviour of LOG1…LOG4. So, we could track the internal transaction much more easier.

---

**maxsam4** (2022-05-01):

I think that should be a different EIP that depends on this EIP.

I personally don’t think there should be an event. For tracing, it can be shown as a call with 0 gas in trace logs or a new type. Not sure how selfdestruct value transfer is shown right now.

---

**QEDK** (2022-05-01):

No good reason for that imho, if implemented, I feel it should semantically be similar to how an EOA sends ether to another EOA or a contract with an empty `receive()` (without any calldata).

---

**joeysantoro** (2022-05-01):

This is absolutely essential from a security perspective. The only alternative would be making native ETH ERC-20 compliant.

---

**tjayrush** (2022-05-01):

I think this is a great idea. I would not call it AIRDROP though. That word is way too loaded with meaning already. I get the idea of the word, but perhaps something a bit less loaded: REMIT?

The Cambridge Dictionary says:

### remit <verb>

formal

to send money to someone

**Example:** He worked in a different city and remitted half his monthly wage back to his family.

---

**maxsam4** (2022-05-01):

> I would not call it AIRDROP though

It is used as a placeholder and is one of the open-ended questions in the proposal. I would be fine if it actually got finalized as sort of an easter egg though.

> REMIT

I like it but it solidifies the view that ether is money. That might not be a good thing to do.

---

**dmfxyz** (2022-05-01):

I support this; but, would the receiving contract need to be marked as payable in any way, or is it ignored as with self destruct?

EDIT: I see the empty account notes now.

---

**0age** (2022-05-02):

How about `FORCE_SEND` or something that makes it explicit that the recipient has no say in the matter of whether or not to accept the payment?

Personally, I’d advocate that this *not* be something that EOAs can do; there aren’t nearly as many use-cases where it’s required (or a forwarding contract could easily be employed where it is needed — especially since the recipient can’t check the caller / origin anyway), and having it simply be an opcode with similar semantics to `SELFDESTRUCT` is much more straightforward.

One important backwards-compatibility concern is that many contracts are not designed with Ether recoverability in mind; hopefully most contract authors understand at this stage that the ether balance of a non-payable contract can still be modified via `SELFDESTRUCT` or as the coinbase recipient, but there’s a common understanding that users will not interact with contracts via those methods unless they *really* know what they’re doing or are acting maliciously. I could see this leading to more instances of Ether accidentally finding its way into unrecoverable situations.

Agreed that a feature like this is sorely needed, though — I wonder if there’s a way to pair it with a `BLOCK_FORCE_SEND` mechanic? (Though in that event the proposed name here is sub-optimal!)

---

**maxsam4** (2022-05-02):

> How about FORCE_SEND or something that makes it explicit that the recipient has no say in the matter of whether or not to accept the payment?

I don’t have strong opinions about the name but I prefer just SEND/REMIT. Send is overloaded in Solidity so maybe REMIT is better. Force is implicit, as it’s usually the case with transferring anything. Other names in my mind - PAY, DISBURSE, BESTOW.

> Personally, I’d advocate that this not be something that EOAs can do;

Agreed. I don’t see much of a use-case for EOAs to do this but there definitely are additional risks.

> I could see this leading to more instances of Ether accidentally finding its way into unrecoverable situations.

Potentially, yes. However, since this opcode can only be used by new contracts, I don’t think there should be any issue. ERC20 tokens, for example, are worse in terms of ease of sending mistakenly and recovering. People/devs are now sufficiently aware of asset recovery IMO.

> I wonder if there’s a way to pair it with a BLOCK_FORCE_SEND mechanic?

I think that will partially defeat the purpose. Not recommended until we make SELFDESTRUCT and block reward also follow it.

---

**charles-cooper** (2022-05-03):

Probably the mnemonic for this instruction should be `TRANSFER`. It’s semantics are clear, it matches ERC20 transfer, and there is no existing opcode named `TRANSFER`. What high-level languages call it is a different matter.

---

**firnprotocol** (2022-11-13):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/c0e974/48.png) maxsam4:

> Q) Doesn’t this break the contracts that depend on the stipend?
> A) Those contracts were already broken as bypassing stipend is already possible. Additionally, I do not think there are any practical contracts that get “broken” because of this. Sending money to a gnosis wallet, for example, does not break it even if you don’t end up executing its fallback function.

another good name could be `PAY`, which was proposed by [another EIP draft](https://ethereum-magicians.org/t/eip-5920-pay-opcode/11717).

---

**wjmelements** (2022-11-30):

Adding to the naming discussion:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0age/48/1052_2.png) 0age:

> How about FORCE_SEND or something that makes it explicit that the recipient has no say in the matter of whether or not to accept the payment?

There are at least two existing ways to non-consensually send ether to a contract. It is foolish to assume that a contract’s balance cannot increase without your permission. So I don’t like the wording of `FORCE`, as we don’t use such terminology to signal non-consent in the other contexts.

I like `TRANSFER`, `SEND`, and `PAY`, which convey the meaning and are distinct from the `CALL` opcodes.

