---
source: magicians
topic_id: 16683
title: "ERC-7562: Account Abstraction Validation Scope Rules"
author: dror
date: "2023-11-18"
category: ERCs
tags: [erc, account-abstraction]
url: https://ethereum-magicians.org/t/erc-7562-account-abstraction-validation-scope-rules/16683
views: 2771
likes: 9
posts_count: 25
---

# ERC-7562: Account Abstraction Validation Scope Rules

This is a discussion for ERC-7562 - [Add ERC: Account Abstraction Validation Scope Rules by drortirosh · Pull Request #105 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/105/files)

This is an extraction of the Account-Abstraction validation rules out of ERC-4337 itself

## Replies

**Hugo0** (2024-03-25):

Could I get some clarification on how that affects a userop that e.g. calls a contract that only releases funds after a certain block.timestamp? Does this check just get ignored during validation, but still gets run during execution? or does the userop just get dropped?

---

**dror** (2024-03-25):

The validation rules are not checked on-chain.

They are used by bundlers to protect against denial of service attacks: someone who submits a large # of UserOps that go into the mempool, but later fail validation, and thus just waste CPU of bundlers, without ever paying gas fees.

Also, the validation rules only apply to the **validation** phase. Since once validation is done, the account agreed to pay the gas fees.

The **execution** is free to do whatever it wants.

---

**frangio** (2024-06-27):

> If the entity (paymaster, factory) is staked, then it is also allowed:
>
> [STO-033] Read-only access to any storage in non-entity contract.

Can someone clarify for me: does this mean that the entity is allowed access, or that any contract is allowed access?

---

**matthiasgeihs** (2024-07-04):

Can someone clarify: Can a user perform an `ERC20.approve` during `validateUserOp`?

---

**matthiasgeihs** (2024-07-04):

And is eth-infinitism’s TokenPaymaster.sol compliant with ERC-7562?

In other words, does calling `ERC20.safeTransferFrom(token, userOp.sender, address(this), tokenAmount)` during `validatePaymasterUserOp` conflict with `ERC-7562`?

---

**dror** (2024-07-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> Can someone clarify for me: does this mean that the entity is allowed access, or that any contract is allowed access?

The validation checks are done by validation phase: factory , account (validateUserOp) and paymaster (validatePaymasterUserOp), by whatever inner call.

That means that a staked paymaster is allowed to call a contract that in turn performs any “read” operation in its storage (e.g. check whatever config, balance, proxy call to implementation, etc)

Care should be taken, though. This paymaster must carefuly verify that the external contract it uses can’t cause the paymaster itself to get throttled:

e.g.: If I use a token that uses a proxy  (e.g. USDC), at any point in time the owners of the token may change the proxy “implementation” pointer, and cause all pending payments to be rejected, and thus the paymaster gets throttled.

However, probably the damage to the token itself would be much larger, and thus a paymaster can safely assume that any implementation change will have all existing pending transfers valid.

Another, more subtle example: if a paymaster uses an oracle, and someone manages to make a large # of UserOps that “barely fit” the needed gas price just before the token’s price drops, it might cause all those UserOps to get reverted, and the paymaster gets throttled or even banned.

---

**dror** (2024-07-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matthiasgeihs/48/12741_2.png) matthiasgeihs:

> And is eth-infinitism’s TokenPaymaster.sol compliant with ERC-7562?
>
>
> In other words, does calling ERC20.safeTransferFrom(token, userOp.sender, address(this), tokenAmount) during validatePaymasterUserOp conflict with ERC-7562?

Yes, the paymaster is compliant, as long as it is staked.

A staked entity is allowed to access the account’s as well as its own “assocated storage”, and thus move balance from the account to itself.

(Note that it can’t move balance to another account, since its a storage not associated with the account (or paymaster). It can’t mint/burn either, since that would change the “totalSupply” of the token, which again, isn’t associated with a specific address)

---

**dror** (2024-07-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matthiasgeihs/48/12741_2.png) matthiasgeihs:

> Can someone clarify: Can a user perform an ERC20.approve during validateUserOp?

alas, no.

That requires modifying storage associated with another entity, that isn’t the account itself

---

**andysim3d** (2024-08-15):

A question of `test_rule[[STO-022]unstaked][paymaster][account_reference_storage_init_code][drop1]` - I take a look at EIPS/eip-7562#storage-rules but `STO-022` only mentioned Access to associated storage of the account in an external (non-entity) contract is allowed if there is an initcode and the factory contract is staked. not very sure why unstaked paymaster will cause a dropped UO in this scenario.

---

**emrah23** (2024-11-08):

Could I get some clarification on when `opsSeen` variable is incremented for both canonical mempool and alt-mempool. The definition is:

opsSeen: a per-entity counter tracking how many times a unique, valid UserOperation referencing this entity was received by the bundler. This includes UserOperations received via incoming RPC calls or through a P2P mempool protocol.

Does that mean if the paymaster is having some violation, such as storage, the UserOperation is considered invalid, and expected to be dropped by Bundler. But does that mean `opsSeen` for paymaster is not incremented?

---

**dror** (2024-11-20):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/e/898d66/48.png) emrah23:

> opsSeen: a per-entity counter tracking how many times a unique, valid UserOperation referencing this entity was received by the bundler.

The opsSeen is counted only for UserOperations that passes the first validation (when accepted over the rpc or p2p connection) and propagated to other nodes via the mempool.

If the UserOp is dropped in its initial validation (either on storage/opcode validation rule, or a “mere” revert), the opsSeen counters are unaffected.

The bundler protects itself using a connection quota mechanism.

The reputation rules (based on opsSeen/opsIncluded) kick in when the UserOperation fails when it is about to be included in a bundle. At this point, it already passed the above first validation and was propagated to all other bundlers on the p2p network (which means, many bundlers will try to include it in a bundle - and fail, since validation failures are not propagated in the mempool)

---

**colinlyguo** (2025-01-08):

A small question regarding the rule: **[AUTH-010]** A UserOperation may only contain a single [EIP-7702](https://eips.ethereum.org/EIPS/eip-7702) authorization tuple.

for userop, they cannot have an authorization tuple if I understand correctly. So does the rule mean the bundle transaction can only have one authorization tuple?

another question is about the rules of “The need for 2nd validation before submitting a block”, I think to perform ERC-7562 validation, it seems that getting the bundle transaction’s trace is unavoidable. Would this introduce expensive overhead of block proposer’s mempool?

---

**dror** (2025-01-15):

> for userop, they cannot have an authorization tuple if I understand correctly. So does the rule mean the bundle transaction can only have one authorization tuple?

A UserOperation can include an eip7702 tuple - the account itself can be an eip-7702 account (that is, and EOA that gets an account code)

A bundler that handles such UserOperations, can submit a bundle that  includes multiple authorization tuples, for all the UserOperations in the bundle that require it.

> The need for 2nd validation before submitting a block

Yes, a bundler is required to perform a 2nd validation against all UserOperations before creating a bundle, since from the time they were submitted until the current time, the account state might differ, and some UserOperations might be invalid.

Currently bundlers are not “block proposers”, but external entities that generate a bundle transaction out of UserOperations from the UserOperations mempool.

You can compare the work of such a bundler to a “searcher”, that submits a set of transactions to the block proposer, in order to collect MEV.

---

**colinlyguo** (2025-01-15):

Thanks for your reply, that helps me a lot. thus the `sequencer` is not required to validate during block building.

> A bundler that handles such UserOperations, can submit a bundle that includes multiple authorization tuples, for all the UserOperations in the bundle that require it.

(Updated after rethinking): I just want to make sure I understand this correctly: In this context, does this mean that the bundle transaction could potentially be an EIP-7702 transaction that includes the delegations necessary to support `UserOperations` where the `sender` is an EOA first-time delegate to code (or change delegation)? If so, would this potentially require a new RPC method (or methods) to be introduced for the bundler to collect and manage these authorizations?

---

**alex-forshtat-tbk** (2025-01-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/colinlyguo/48/13417_2.png) colinlyguo:

> Does this mean that the bundle transaction could potentially be an EIP-7702 transaction that includes the delegations necessary to support UserOperations where the sender is an EOA first-time delegate to code (or change delegation)?

Yes, it is expected that most bundle (`handleOps`) transactions will be EIP-7702 Type-4 transactions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/colinlyguo/48/13417_2.png) colinlyguo:

> Would this potentially require a new RPC method (or methods) to be introduced for the bundler to collect and manage these authorizations?

There is only a single new optional field, `authorizationTuple`, that is added to the existing `eth_sendUserOperation` API, there seems to be no need to create an entirely new API for that.

---

**colinlyguo** (2025-01-30):

Thanks for the reply, it makes sense and helps a lot.

---

**wminshew** (2025-02-07):

afaict the storage rules prohibit ~most smart accounts from being signers for other smart accounts; can someone help me understand what I might be missing? I feel like these must be expected to work in the endgame but I’m having trouble seeing it atm. Appreciate any help, thank you

---

**alex-forshtat-tbk** (2025-02-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wminshew/48/4658_2.png) wminshew:

> the storage rules prohibit ~most smart accounts from being signers for other smart accounts

Having accounts depend on each other as part of the UserOperation validation presents a serious challenge. The “signer” smart account is not an “entity” of the UserOperation, and the system has no ways to track or guarantee its behaviour.

Personally, I think it is technically possible to define a generic *“signer” staked entity* in a future revision of ERC-7562, and track this generic entity’s reputation based on a set of rules similar to the Paymaster-related rules, but so far there was no major use-case that would make this change urgent.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wminshew/48/4658_2.png) wminshew:

> I feel like these must be expected to work in the endgame but I’m having trouble seeing it atm.

It may be a strong requirement if multi-smart-account-multisigs become popular, but in many cases the “sender” smart account can also just store the keys of the “signer” smart contract in its own internal storage, use these credentials during the validation phase in accordance to ERC-7562 rules, and maybe even, during the execution phase, check with the “signer” contract that these keys are still valid.

---

**cejay** (2025-11-21):

```auto
**Associated storage:** a storage slot of any smart contract is considered to be “associated” with address `A` if:

The slot value was calculated as `keccak(A||x)+n`, where `x` is a `bytes32` value, and `n` is a value in the range 0..128
```

Is it possible to add one more rule:

“The slot value starts with A.”

For example, A: 0x1111111111111111111111111111111111111111.

Then any slot value starts with 0x1111111111111111111111111111111111111111 is considered **associated storage**, for example:

- 0x1111111111111111111111111111111111111111aaaaaaaaaaaaaaaaaaaaaaaa
- 0x1111111111111111111111111111111111111111bbbbbbbbbbbbbbbbbbbbbbbb

This would greatly increase the flexibility of slot usage **without reducing security**.

---

**wminshew** (2025-12-05):

from the L2 interop working group:

[![image](https://ethereum-magicians.org/uploads/default/optimized/3X/b/1/b1f69f9fc57b1976fbe4ba9f0fa820865d6a6cd6_2_690x315.png)image1016×464 97.8 KB](https://ethereum-magicians.org/uploads/default/b1f69f9fc57b1976fbe4ba9f0fa820865d6a6cd6)

would you confirm that arbitrary storage access is safe / storage limitations disappear w 7701? This feels at odds with the abstract of 7562 as I currently understand it ([ERC-7562: Account Abstraction Validation Scope Rules](https://eips.ethereum.org/EIPS/eip-7562#abstract))


*(4 more replies not shown)*
