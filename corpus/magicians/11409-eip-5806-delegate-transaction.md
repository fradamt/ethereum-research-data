---
source: magicians
topic_id: 11409
title: EIP-5806 Delegate transaction
author: Amxx
date: "2022-10-20"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-5806-delegate-transaction/11409
views: 5416
likes: 7
posts_count: 34
---

# EIP-5806 Delegate transaction

[Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5806)





###



Adds a new transaction type that allows a EOAs to execute arbitrary code through delegation

## Replies

**Amxx** (2022-10-22):

One of the point I think should be discussed is the “amount” part of the transaction.

Since this transaction is going to delegate call, the amount should not be sent to anyone, and should remain on the sender/signer’s account. The delegate call mechanism cause the code that the is being executed to has access to the entire balance of the account.

Consequently, the amount doesn’t correspond to an actual transfer, and I believe it should not be part of the transaction parameters.

On the other hand, that means that the code being called through the delegate will always have msg.value equal to 0. Is that acceptable?

---

**k06a** (2023-03-03):

Amazing concept, would be awesome to have it together with EIP-3074

---

**optimalbrew** (2023-03-03):

I think of contract storage as being tied to a specific contract. For instance, when “upgrading” contract code using `create2` pattern the new code has to work with existing storage layout. So I am struggling to understand how arbitrary calls to different contracts via `delegatecall`  will work? Sorry if this is a silly question.

---

**Amxx** (2023-03-03):

I’m sorry I don’t understand.

---

**optimalbrew** (2023-03-03):

Only contracts have storage, not EOAs. That storage is managed by the contract’s bytecode. You propose to create storage under the EOA - without any code to manage that storage. I am thinking about issues that arise when using `delegatecall`, such as *storage collisions* or the “*constructor caveat*” mentioned here [Proxy Upgrade Pattern - OpenZeppelin Docs](https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies)  . How can you avoid such issues when your EOA’s storage is completely at the mercy of external contracts you delegatecall?

---

**sbacha** (2023-04-02):

Is this spec final? Interested in testing this

---

**k06a** (2023-05-27):

I returned to say idea is such a great, I will try contribute.

---

**smartprogrammer** (2023-08-03):

I would suggest to disallow storage on the EOA level. We can just halt execution if the bytecode being executed is trying to store something on the EOA account. This way only calls that don’t involve this mechanism will be allowed to be included in blocks (or mempool)

---

**Jlm** (2023-08-08):

Salut Hadrien,

The proposal is interersting. Yet, I’m confused about the `delegatecall` process originating from the EOA. When you use `delegatecall` , the `msg.sender` remains unchanged, which is similar to direct smart contract call without employing `delegatecall` . The distinction appears to be that the state of the smart contract would reside in the EOA’s storage. Is this the desired outcome?

I’ve identified two issues with this approach:

1.Security Concern: We often rely on eth_getCode and the fact that the storage of an EOA is ‘0x’ to ascertain if an account is an EOA. Without this distinction, it would be indistinguishable from any arbitrary smart contract. It is also the case for explorers.

2.Storage Collisions: Given that EOAs interact with various contracts, there’s a risk that variables stored in the EOA’s storage could be inadvertently overwritten, rendering the storage unreliable.

What is your opinion about having another type of call that preserves the msg.sender as in a delegate call, but uses the “implementation” contract storage such as in a ‘staticcall’?

---

**high_byte** (2024-01-18):

> The signature_y_parity, signature_r, signature_s elements of this transaction represent a secp256k1 signature over keccak256(0x02 || rlp([chain_id, nonce, max_priority_fee_per_gas, max_fee_per_gas, gas_limit, destination, data, access_list])) .

I see the `amount` field is missing, but otherwise is identical to eip-1559.

however, this eip suggests the signature should use type 2, same in eip 1559 but also without the amount. not only this is not compatible with deserialization, it might open the door for replayability of transactions simply by changing the envelope type from/to this new TX_TYPE.

even if there is no way to RLP encode such ambiguous transactions, it is ambiguous to developers and bugs could arise. (eg. trying to decode `data` bytes as integer `amount`)

to ensure there is no option to replay it should use the new TX_TYPE.

(perhaps for convenience it might be worth including the `amount` and enforcing it to be zero on validation, but unless someone explicitly states a good usecase for this I am not for it by default)

besides that I will just strengthen others points - the storage must not be touched. as mentioned I think the same `staticcall` checks should be performed, but instead of the `isStatic` flag it should check if `address(this).code` is empty.

---

**wjmelements** (2024-01-18):

EIP 3074 is more friendly for Coincidence of Wants schemes than EIP 5806. AuthCall lets you batch intents from different users in the same transaction, whereas EIP 5806 does not.

---

**Amxx** (2024-01-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/high_byte/48/11480_2.png) high_byte:

> I see the amount field is missing, but otherwise is identical to eip-1559.
> however, this eip suggests the signature should use type 2, same in eip 1559 but also without the amount. not only this is not compatible with deserialization, it might open the door for replayability of transactions simply by changing the envelope type from/to this new TX_TYPE.

You are right, the signature should not use 0x02 but the new transaction type (TBD)

This has been fixed.

---

**Amxx** (2024-01-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> EIP 3074 is more friendly for Coincidence of Wants schemes than EIP 5806. AuthCall lets you batch intents from different users in the same transaction, whereas EIP 5806 does not.

EIP-5806 lets you use create2. It allows you to replace transactions. Also there is less margin on how the signature is used (depending on the contract you use an Auth signature could possibly lead to different executions depending on parameter that are not signed), making simulation of the outcome safer when signing an EIP-5806 transaction compared to a 3074 authorisation …

The two EIP are very different approaches, with different forces and weaknesses. They just don’t do the same thing. It would be like comparing a toaster and an oven … sure they both heat-up things, but they have different usecases.

---

**Amxx** (2024-02-01):

I’m realising that setting state under an EOA could cause issues if code is then placed at that EOA’s address (using one of the EIP for transition to AA).

So it would make sens to disable any operation that has lasting effect on the account state (namely `sstore`). On the other hand, I don’t see any issue with allowing `tstore` and `log` to be executed during a delegate-transaction. Can anyone think of any issue with these opcodes (or other beside sstore and selfdestruct).

---

**StanislavBreadless** (2024-02-18):

During CREATE2 opcode the nonce of the account is incremented too as per the execution specs: https://github.com/ethereum/execution-specs/blob/4d953035fb0cceda7cf21d71b2ab7a9a6f4632f0/src/ethereum/shanghai/vm/instructions/system.py#L109 (this function will be called by the `create2`), so probably CREATE2 should be added as a forbidden opcode also.

I think it is also worth strictly specifying the behavior when “forbidden” opcodes are executed. For instance, in the context of EIP4337 if an account executes a “forbidden” opcode during validation, the transaction *should* be rejected. However, not rejecting such txs is just a matter of security for the bundler & so, in the end, such txs may be included nonetheless if the bundler has some personal agreements with the account.

In the case of this proposal, if either of the SSTORE/CREATE/CREATE2 is executed with `this` as EOA, this might break invariants of the protocol and so such situations should never happen. One option would be to reject such txs (i.e. consider those as invalid on the protocol level), but it might also appear as a bit of a DDoS vector (a tx might spend 15M gas and only after that do a forbidden tx, making sure that the builder’s work was all in vain).

So throwing an exception (reverting the context) sounds like a much more appealing approach. This way if the user is malicious, they will pay the fees to the miner nonetheless.

---

**Amxx** (2024-02-18):

Interresting. I did not realized `CREATE2` modified the account’s nonce. Since the nonce is not part of the address derivation, I did not think updating it was necessary.

I’m considering forbiding all the opcodes that change the nonce, so `CREATE`, `CREATE2` and `SELFDESTRUCT`/`DEACTIVATE`.

As for the error, I think it should revert (just like if you call any of these through a `STATICCALL`)

---

**Amxx** (2024-02-18):

An alternative would be to allow `CREATE2`, but say that if its executed by an EOA in the context of an EIP-5806 transaction, then the nonce should not be incremented.

---

**joeblogg801** (2024-02-18):

In certain contracts, you may encounter the following code snippet:

`require(msg.sender == tx.origin, "no contracts");`

This code serves the purpose of preventing calls to the contract from within another contract. If this EIP is implemented, it will render the assumption upon which these contracts relied invalid.

Perhaps it’s worth adding this to security considerations and explaining why the change is acceptable.

---

**Amxx** (2024-02-19):

[EIP-3074 does include a warning for that](https://eips.ethereum.org/EIPS/eip-3074#allowing-txorigin-as-signer). I beleive the same logic applies to this EIP, so maybe we should add a similar warning in EIP-5806.

---

**StanislavBreadless** (2024-02-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> An alternative would be to allow CREATE2, but say that if its executed by an EOA in the context of an EIP-5806 transaction, then the nonce should not be incremented.

Obviously, choices like that are opinionated, but IMHO the fewer edge cases we have on the execution layer, the better. I am unsure of any good use cases for EOA’s CREATE2…


*(13 more replies not shown)*
