---
source: magicians
topic_id: 11886
title: Almost self-destructing SELFDESTRUCT → DEACTIVATE
author: axic
date: "2022-11-25"
category: EIPs > EIPs core
tags: [evm, opcodes]
url: https://ethereum-magicians.org/t/almost-self-destructing-selfdestruct-deactivate/11886
views: 4995
likes: 16
posts_count: 29
---

# Almost self-destructing SELFDESTRUCT → DEACTIVATE

TLDR: The selfdestruct↔revive pattern stays working, but instead of deleting accounts, we use a special value in the `nonce` field to distinguish *deactivated* accounts.



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-6046)





###



Change SELFDESTRUCT to not delete storage keys and use a special value in the account nonce to signal deactivation










From the motivation of [EIP-4758](https://eips.ethereum.org/EIPS/eip-4758):

> The SELFDESTRUCT opcode requires large changes to the state of an account, in particular removing all code and storage. This will not be possible in the future with Verkle trees: Each account will be stored in many different account keys, which will not be obviously connected to the root account.

EIP-4758 proposes to:

> The SELFDESTRUCT opcode is renamed to SENDALL, and now only immediately moves all ETH in the account to the target; it no longer destroys code or storage or alters the nonce
> All refunds related to SELFDESTRUCT are removed

Concerns have been voiced that a number of contracts depend on a selfdestruct↔revive pattern, which would be broken by this change.

Here’s an alternative slightly-hackish idea. Haven’t investigated its merits too much, but wanted to float it.

Since [EIP-2681](https://eips.ethereum.org/EIPS/eip-2681) it is ensured that the `account.nonce` field can never exceed `2^64-1`. We can use this to our advantage.

1. SELFDESTRUCT continues to behave almost the same as today, but instead of removing the account, it will leave most properties of the account intact, with the exception of two:

- transfer all value and set balance to 0,
- set nonce to 2^64.

1. Modify account execution (triggered both via external transactions or CALL*), such that execution fails if the nonce equals 2^64.

- Note that the account can still receive non-executable value transfers (such as coinbase transactions).
- Another option would be to just behave like an account without code upon execution, i.e. return success and no data.

1. Modify CREATE2 such that it allows account creation if the nonce equals 2^64.
2. Rename the SELFDESTRUCT instruction to DEACTIVATE, since the semantics of “account re-creation” are changed: the old storage items will remain, and newly deployed code must be aware of this.

This option I think would accomplish the goal of removing unbounded tree changes, while not breaking existing contracts. Account/storage waste would remain, but that remains in-place with EIP-4758 too. Additionally, for deactivated accounts, the codehash and other inspectable properties would remain the same, just as with EIP-4758.

P.S. ~~Doesn’t the `nonce` of an account-with-code start at `1` and not `0`? If it does, could also use `0` as the magic value.~~ Contracts deployed before [EIP-161](https://eips.ethereum.org/EIPS/eip-161) behave differently.

P.P.S. If we want external observability of *deactivated* accounts, perhaps an [EXTNONCE opcode](https://ethereum-magicians.org/t/eip-4672-nonce-opcode/8171) would be useful.

## Replies

**MicahZoltu** (2022-11-26):

> set nonce to 2^64

It seems like this would break the implied invariant that EIP-2681 created which is that nonce can *always* fit into a 64-bit variable.  While I recognize that the specification didn’t say this explicitly, it was mentioned in the rationale and backward compatibility:

> Most clients already consider the nonce field to be 64-bit, such as go-ethereum.

> go-ethereum already has this restriction partially in place (state.Account.Nonce and types.txdata.AccountNonce it as a 64-bit number).

To hold 2^64, we would need a 65 bit or larger value type.

Alternatively, we could just further constrain valid nonces to `2^63` and use `2^64-1` for this new purpose.

---

**axic** (2022-11-26):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> It seems like this would break the implied invariant that EIP-2681 created which is that nonce can always fit into a 64-bit variable.

Yes, that was a goal.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> To hold 2^64, we would need a 65 bit or larger value type.
>
>
> Alternatively, we could just further constrain valid nonces to 2^63 and use 2^64-1 for this new purpose.

We discussed that it could be restricted to `2^64-2` or anything lower. None of these values are realistically reachable, so we are safe to do so.

---

**axic** (2022-11-26):

Drafted a more clear set of instructions here:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/6046)














####


      `master` ← `ipsilon:deactivate`




          opened 12:27PM - 26 Nov 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/0/0500df04ffb122fbd3f40611712c7aebb1bf3b8d.png)
            axic](https://github.com/axic)



          [+67
            -0](https://github.com/ethereum/EIPs/pull/6046/files)













This mentions the new limit of nonce.

Should also consider to clarify the various edge cases of selfdestruct, when does the transfer takes place, when does the deletion/update takes place, etc. The gas cost could also be looked at, and potentially increased.

---

**petertdavies** (2022-11-28):

I think the complexity with setting nonces to the special value of 2^64-1 and adding special behaviour if the nonce is 2^64-1 can be avoided by:

- Removing EIP-161 state clearing behaviour.
- Having DEACTIVATE set code to empty and nonce to 0.

We have to remove EIP-161 state clearing to do this because `DEACTIVATE` will create empty accounts, which will get cleared (along with their storage) by EIP-161, undermining the point of this EIP.

The one downside of this is that empty accounts have their own special semantics (for most purposes they are treated as if they don’t exist), but at least those semantics are already implemented by clients rather than the new special semantics added by this EIP.

---

**wjmelements** (2022-11-28):

I am a fan of this approach. It addresses the concerns of the people building the new trie by removing the requirement that storage is cleared, a behavior not needed by those of us using the create2 upgrade pattern.

I also like that this approach can make selfdestruct cheap enough to execute it and revert it during the transaction rather than deferring to the end.

One other matter for this approach to consider is how EXTCODECOPY and EXTCODEHASH should work. Some are using EXTCODEHASH to detect if a contract is empty or if an account is a contract. I like that this seems to distinguish a self-destructed contract from an EOA.

---

**dankrad** (2022-11-28):

It’s an interesting idea, but this introduces another pitfall: Unlike the old behaviour, storage does not get cleared.

I guess this could be an option if all the examples we can find do not depend on storage being cleared.

BTW, could it be another option to replace the code with a magic value, that marks it as being destroyed? I guess that could be a slightly more natural way of doing it. (We can use the EOF magic bytes to make sure that no code with the magic can be deployed by another means)

---

**vbuterin** (2022-11-28):

The big issue I see with this category of approaches is that it takes away a really nice invariant that we get if we neuter `SELFDESTRUCT` completely: that if an account has code X, it will always have code X. This has lots of nice use cases in terms of giving users and accounts the ability to trust that a particular contract will work in a certain way. One specific example is that it makes it easy for ERC-4337 wallets to be able to trust libraries (otherwise, someone could make an account that depends on a library, and then `SELFDESTRUCT` that library to require recalculating an unlimited number of pending ops).

The approaches that involve making `SELFDESTRUCT` only work during the same transaction the contract was created don’t have this problem to nearly the same extent.

---

**axic** (2022-11-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dankrad/48/2962_2.png) dankrad:

> It’s an interesting idea, but this introduces another pitfall: Unlike the old behaviour, storage does not get cleared.

This is listed in the backwards compatibility section of the EIP. Various ideas were discussed to work around this, with causing even more storage use, for example: hash storage keys one more time with the special nonce (in this case a range would need to be allocated), to avoid collisions. This also would make accessing old ones after revival impossible.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dankrad/48/2962_2.png) dankrad:

> BTW, could it be another option to replace the code with a magic value, that marks it as being destroyed? I guess that could be a slightly more natural way of doing it. (We can use the EOF magic bytes to make sure that no code with the magic can be deployed by another means)

I proposed this ~2 years ago on the R&D discord, but the argument against it was that it wouldn’t be as optimal in Verkel trees.

---

**wjmelements** (2022-11-30):

\

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> This has lots of nice use cases in terms of giving users and accounts the ability to trust that a particular contract will work in a certain way

This property was surrendered via `DELEGATECALL` proxies. I presume you wish to keep those, but the behavior of a contract *can* change significantly without changing its code.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> it makes it easy for ERC-4337 wallets to be able to trust libraries

Nobody can trust EVM code without reading it. The same off-chain processes that check for `DELEGATECALL` upgradeability would need to check for `SELFDESTRUCT`. Neutering `SELFDESTRUCT` doesn’t change this.

---

**MicahZoltu** (2022-12-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> This property was surrendered via DELEGATECALL proxies. I presume you wish to keep those, but the behavior of a contract can change significantly without changing its code.

I believe the word “trust” here is being used a bit differently than normal.  In this case, it means that things like tooling, consensus, etc. can rely on the set of bytes written to the code at an address not changing.

---

**xinbenlv** (2022-12-01):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> this case, it means that things like tooling, consensus, etc. can rely on the set of bytes written to the code at an address not changing.

[@wjmelements](/u/wjmelements)  's comment about DELEGATECALL seems to me still hold true in these examples. could you [@MicahZoltu](/u/micahzoltu) could you ellaborate more examples about in what scenarios such tooling, consensus will survive the ability to change behavior without change code enabled by DELEGATECALL.To me behavior immutability is broken by DELEGATECALL regardless of whether SELFDESTRUCT exist.

---

**MicahZoltu** (2022-12-01):

Yes, *behavior* immutability is entirely within the control of the contract author.  Even without delegate call this would still largely be true (just harder).  When we say “the code cannot change” we mean that it *literally* cannot change, not that its behavior is not dynamic.  When your building your tree structure of state, for example, you may be able to do some optimizations if you *know* that a particular bit of data cannot/will not change.

I have been out of the verkle tree loop for a while, but I believe whether this assertion can be made has a notable impact on that as well.

---

**xinbenlv** (2022-12-01):

That makes sense, well explained, thank you [@MicahZoltu](/u/micahzoltu)

---

**SamWilsn** (2022-12-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> the old storage items will remain, and newly deployed code must be aware of this

This is a *very* subtle change. How do we convince ourselves that this is safe for existing contracts?

---

**yoavw** (2022-12-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> This is a very subtle change. How do we convince ourselves that this is safe for existing contracts?

You’re right - we can’t. In fact it’s likely that it isn’t ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

For example, consider a multisig like Safe, that has signers and modules, with the following flow:

1. The Safe is initialized with {signer1}.
2. Signer1 adds {signer2,signer3}.
3. A selfdestructing module gets added.  A module can selfdestruct the Safe because Safe supports delegatecall’ing a module.
4. The Safe gets reinitialized with {signer1}.

Before this EIP, the result is that only signer1 is a valid signer.  After this EIP, {signer2,signer3} are also valid signers.

Besides, it opens up interesting new ways to rugpull/backdoor.  E.g. deploy a token, mint yourself a large balance, selfdestruct, redeploy.  Now `totalSupply` is reset, everything looks good, but in fact you still have the large balance (possibly higher than the totalSupply).  Some backdoors would be almost impossible to detect, if delegating to a library that gets selfdestructed and replaced.

---

**axic** (2022-12-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> For example, consider a multisig like Safe, that has signers and modules, with the following flow:
>
>
> The Safe is initialized with {signer1}.
> Signer1 adds {signer2,signer3}.
> A selfdestructing module gets added. A module can selfdestruct the Safe because Safe supports delegatecall’ing a module.
> The Safe gets reinitialized with {signer1}.
>
>
> Before this EIP, the result is that only signer1 is a valid signer. After this EIP, {signer2,signer3} are also valid signers.

This example is not correct, because the safe initialisation not only sets an array of signers, but also the count. See [this code](https://github.com/safe-global/safe-contracts/blob/main/contracts/base/OwnerManager.sol#L22-L44).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Besides, it opens up interesting new ways to rugpull/backdoor. E.g. deploy a token, mint yourself a large balance, selfdestruct, redeploy. Now totalSupply is reset, everything looks good, but in fact you still have the large balance (possibly higher than the totalSupply). Some backdoors would be almost impossible to detect, if delegating to a library that gets selfdestructed and replaced.

This is a more realistic example, unlike the safe above. I personally would not trust any contract which selfdestructs, nor do I trust proxy contracts much. That being said, it is already possible to hide intent in various ways.

Besides, there are some other potential options in making the old storage slots shadowed (inaccessible entirely) with hashing the keys with a revival-nonce. Not that I am fond of that approach.

---

**yoavw** (2022-12-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> This example is not correct, because the safe initialisation not only sets an array of signers, but also the count. See this code.

Hmmm, I believe it is correct because the count is not checked when the signer is used.  Neither in [isOwner](https://github.com/safe-global/safe-contracts/blob/main/contracts/base/OwnerManager.sol#L130-L132), nor in [checkNSignatures](https://github.com/safe-global/safe-contracts/blob/c36bcab46578a442862d043e12a83fec41143dec/contracts/GnosisSafe.sol#L301).

During signatures check, I think the default flow for a normal signature would reach `currentOwner = ecrecover(dataHash, v, r, s)` in [line 299](https://github.com/safe-global/safe-contracts/blob/c36bcab46578a442862d043e12a83fec41143dec/contracts/GnosisSafe.sol#LL299C17-L299C60), so `currentOwner` will be set to the left-over signer (despite the count).  And then it will pass the `require(currentOwner > lastOwner && owners[currentOwner] != address(0) && currentOwner != SENTINEL_OWNERS, "GS026");` in [line 301](https://github.com/safe-global/safe-contracts/blob/c36bcab46578a442862d043e12a83fec41143dec/contracts/GnosisSafe.sol#L301) because `owners[currentOwner]` has been set before the DEACTIVATE happened.  Therefore the signature will be counted towards `requiredSignatures`.

If `requiredSignatures` is set to 3, and there were 3 signers before DEACTIVATE, who are no longer valid signers in the current safe, they’ll be able to pass the signature check without any of the valid signers participating.

The count is only used during [getOwners()](https://github.com/safe-global/safe-contracts/blob/c36bcab46578a442862d043e12a83fec41143dec/contracts/base/OwnerManager.sol) which is never called on-chain. This makes the problem worse, because the “shadow owners” remain hidden when `getOwners()` is checked in the UI.

Am I missing some check that would prevent this?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> I personally would not trust any contract which selfdestructs, nor do I trust proxy contracts much. That being said, it is already possible to hide intent in various ways.

I’m with you on that.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> Besides, there are some other potential options in making the old storage slots shadowed (inaccessible entirely) with hashing the keys with a revival-nonce. Not that I am fond of that approach.

Yes, I was also considering the option of hashing it in the compiler, so that slots are not reused.  But this requires an opcode for accessing the nonce, and also not resetting the nonce to 0 on revival, but to a random number.  I actually think this would be a good addition to the compiler (if we add the EXTNONCE opcode - maybe that’s another good use case for [EIP-4672](https://ethereum-magicians.org/t/eip-4672-nonce-opcode/8171)).  It would also prevent similar issues with proxies.  What would be the downside of that approach?

To clarify, I don’t mean using EXTNONCE every time a mapping is accessed.  The nonce may change when creating additional contracts.  I mean saving it as `immutable` during construction, so when a contract is “revived” it’ll have a different storage base.  And maybe instead of hashing it, we would add it, so that it also affects simple variables and arrays, not just mappings.

---

**jwasinger** (2022-12-08):

The wording of the EIP implies that setting the nonce to `2^64-1` happens immediately upon calling `DEACTIVATE`.  In my opinion, this should be moved to happen at the end of the transaction similarly to how `SELFDESTRUCT` works.

---

**axic** (2022-12-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> axic:
>
>
> This example is not correct, because the safe initialisation not only sets an array of signers, but also the count. See this code.

Hmmm, I believe it is correct because the count is not checked when the signer is used. Neither in [isOwner](https://github.com/safe-global/safe-contracts/blob/main/contracts/base/OwnerManager.sol#L130-L132), nor in [checkNSignatures](https://github.com/safe-global/safe-contracts/blob/c36bcab46578a442862d043e12a83fec41143dec/contracts/GnosisSafe.sol#L301).

During signatures check, I think the default flow for a normal signature would reach `currentOwner = ecrecover(dataHash, v, r, s)` in [line 299](https://github.com/safe-global/safe-contracts/blob/c36bcab46578a442862d043e12a83fec41143dec/contracts/GnosisSafe.sol#LL299C17-L299C60), so `currentOwner` will be set to the left-over signer (despite the count). And then it will pass the `require(currentOwner > lastOwner && owners[currentOwner] != address(0) && currentOwner != SENTINEL_OWNERS, "GS026");` in [line 301](https://github.com/safe-global/safe-contracts/blob/c36bcab46578a442862d043e12a83fec41143dec/contracts/GnosisSafe.sol#L301) because `owners[currentOwner]` has been set before the DEACTIVATE happened. Therefore the signature will be counted towards `requiredSignatures`.

If `requiredSignatures` is set to 3, and there were 3 signers before DEACTIVATE, who are no longer valid signers in the current safe, they’ll be able to pass the signature check without any of the valid signers participating.

The count is only used during [getOwners()](https://github.com/safe-global/safe-contracts/blob/c36bcab46578a442862d043e12a83fec41143dec/contracts/base/OwnerManager.sol) which is never called on-chain. This makes the problem worse, because the “shadow owners” remain hidden when `getOwners()` is checked in the UI.

Am I missing some check that would prevent this?

The safe uses a “sentinel” field to trail the owner array. See `SENTINEL_OWNERS` [here](https://github.com/safe-global/safe-contracts/blob/c36bcab46578a442862d043e12a83fec41143dec/contracts/GnosisSafe.sol#L301) and [here](https://github.com/safe-global/safe-contracts/blob/main/contracts/base/OwnerManager.sol#L41).

---

**axic** (2022-12-08):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/j/57b2e6/48.png) jwasinger:

> The wording of the EIP implies that setting the nonce to 2^64-1 happens immediately upon calling DEACTIVATE. In my opinion, this should be moved to happen at the end of the transaction similarly to how SELFDESTRUCT works.

Good catch! I wonder however if it would make sense changing the behaviour to this, i.e. currently selfdestructed contracts can be called *after* they are selfdestructed as long as we didn’t exit the transaction frame.


*(8 more replies not shown)*
