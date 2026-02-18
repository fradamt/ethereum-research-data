---
source: magicians
topic_id: 15144
title: "EIP-7377: Migration Transaction"
author: matt
date: "2023-07-22"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7377-migration-transaction/15144
views: 5854
likes: 66
posts_count: 52
---

# EIP-7377: Migration Transaction

Discussion for the Migration Transaction EIP. This EIP proposes a new transaction type that allows EOAs to submit a one-time upgrade to a smart contract.

> Introduce a new EIP-2718 transaction type with the format 0x04 || rlp([chainId, nonce, maxFeePerGas, maxPriorityFeePerGas, gasLimit, codePtr, storageTuples, data, value, accessList, yParity, r, s]) which sets the sending account’s code field in the state trie to the code value at codePtr and applies the storage tuples to the sender’s storage trie.

## Replies

**ch4r10t33r** (2023-07-26):

Interesting proposal.

I have a question though. Once upgraded, what happens the private key that controls the EOA?

---

**kyrers** (2023-07-26):

As far as I can understand, this seems like a good approach.

I do have some doubts related to `codeAddr`: Is this address supposed to be known and supplied by users? Or generally, do you expect wallet providers to facilitate this migration?

Also, just to make sure I understand, a custom contract address would be valid? So more advanced users could, for instance, implement a personalized version.

---

**matt** (2023-07-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ch4r10t33r/48/10109_2.png) ch4r10t33r:

> Once upgraded, what happens the private key that controls the EOA?

Per EIP-3607, the account can no longer originate transactions so the key is not useful to the core protocol. ERCs that use simple cryptographic checks, like `permit`, may still be able to use the private key to control some of the accounts funds.

> I do have some doubts related to codeAddr: Is this address supposed to be known and supplied by users? Or generally, do you expect wallet providers to facilitate this migration?

This address is supplied by the originator of the transaction, but I assume that wallet companies will deploy the code they want their users to use (likely a proxy account) and when the tx is sent, the `codeAddr` will be the address associate with the wallet and the storage element will define the owner of the contract wallet.

Any address is valid for `codeAddr` as long as it has code deployed, so it is completely customizable.

---

**Emilijus** (2023-07-26):

Why do the `chainId`, `maxFeePerGas`, `maxPriorityFeePerGas` and `value` fields have the `int256` type instead of `uint256`?

---

**david** (2023-07-26):

The EIP states “Allowing cheaper storage in this instance acts as a reward to users who migrate their EOAs to smart contract wallets.”

I’m not sure the actual discount (tried to look it up, but couldn’t find the formula for pricing deploy transactions, even in the yellow paper). But does this not simply incentivize deploying smart contracts using this transaction instead of a standard deployment transaction?

---

**ch4r10t33r** (2023-07-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> Any address is valid for codeAddr as long as it has code deployed, so it is completely customizable.

Isn’t this risky? Can’t this lead to other attack vectors? Shouldn’t there be some kind of check to ensure the code at codeAddr adhere to certain basic rules for a wallet?

---

**david** (2023-07-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> Per EIP-3607, the account can no longer originate transactions so the key is not useful to the core protocol. ERCs that use simple cryptographic checks, like permit, may still be able to use the private key to control some of the accounts funds.

This is a security risk worth noting in the EIP.

Users may assume that once their account is “upgraded”, that the private key is “deactivated”.

If a user’s private key is compromised, the key can’t be used to send a transaction, but can be used to steal any asset that supports meta-txs (USDC, Dai) or other assets via meta-tx protocols (CowSwap) if previously approved.

---

**rmeissner** (2023-07-26):

This can be extended to cross-chain considerations. As on chains where this eip is not available or the migration was not executed the ownership is fundamentally different (in the context of the Safe contracts we generally call this “state drift”)

---

**rmeissner** (2023-07-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> ERCs that use simple cryptographic checks, like permit, may still be able to use the private key to control some of the accounts funds.

Should the eip contain an adjustment for `ecrecover` to prevent this?

---

**ryanschneider** (2023-07-26):

Is there a timing attack vector of some sort where I convince you to send a tx to an EOA but then convert the EOA to a contract by colluding w/ a block producer to put my migration transaction before yours?  I feel like the fact that the “type” of an address is no longer immutable should be mentioned in the security considerations.

---

**david** (2023-07-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rmeissner/48/643_2.png) rmeissner:

> Should the eip contain an adjustment for ecrecover to prevent this?

Changing the behavior of basic cryptographic primitives seems like a reeally bad idea…

---

**rmeissner** (2023-07-26):

I generally agree. My question is more if it would be necessary to keep a “secure setup”.

---

**frangio** (2023-07-26):

Forcing the use of a code pointer seems odd given that this cloning behavior can be easily implemented with init code, but not the other way around. Are there other drawbacks of using init code like normal creation transactions?

---

**matt** (2023-07-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/david/48/3827_2.png) david:

> I’m not sure the actual discount (tried to look it up, but couldn’t find the formula for pricing deploy transactions, even in the yellow paper). But does this not simply incentivize deploying smart contracts using this transaction instead of a standard deployment transaction?

So the discount comes in during the intrinsic gas calculation. Instead of 20k for each storage element set, it is 15k. I haven’t looked closely into reasonable numbers yet, but the intuition is that this operation can only be done one time per address. Since there is not inherent value in deploying gobs of contracts with just junk storage, it is probably okay to give a small one time discount.

This isn’t a requirement for the EIP by any means. The final version may offer no discount if we find it too problematic.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ch4r10t33r/48/10109_2.png) ch4r10t33r:

> Shouldn’t there be some kind of check to ensure the code at codeAddr adhere to certain basic rules for a wallet?

It’s always up to the user and their wallet to sign safe messages they understand. The same could be said about the data field of normal transactions: “isn’t it risky, shouldn’t there be certain basic rules the data should adhere to?”. And the answer is also the same: no, the decision is with the user and their wallet.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/david/48/3827_2.png) david:

> If a user’s private key is compromised, the key can’t be used to send a transaction, but can be used to steal any asset that supports meta-txs (USDC, Dai) or other assets via meta-tx protocols (CowSwap) if previously approved.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rmeissner/48/643_2.png) rmeissner:

> This can be extended to cross-chain considerations. As on chains where this eip is not available or the migration was not executed the ownership is fundamentally different (in the context of the Safe contracts we generally call this “state drift”)

Good points, I will add them to the security considerations.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rmeissner/48/643_2.png) rmeissner:

> Should the eip contain an adjustment for ecrecover to prevent this?

Possibly? I am curious what you, other wallet devs, and core devs think. I think it would probably be a separate EIP in general, but we may bundle the two together. I have generally been for adding a check in `ecrecover` to see if the recovered account has code deployed and fail if it does as it neutralizes this issue. Not sure if there are unforeseen effects downstream.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> Forcing the use of a code pointer seems odd given that this cloning behavior can be easily implemented with init code, but not the other way around. Are there other drawbacks of using init code like normal creation transactions?

A reason for doing this is I believe it is forward compatible with other ideas (such as EOF) and minimizes the transaction’s foot print. Without this `codeAddr` concept, we’ll have 10s-100s of copies of a short EVM program to bootstrap a proxy contract into the address. It can probably be done rather cheaply, but given the concerns around EOF this seems reasonable.

Not a hard requirement though if the core devs find it unpalatable.

---

**ch4r10t33r** (2023-07-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> It’s always up to the user and their wallet to sign safe messages they understand. The same could be said about the data field of normal transactions: “isn’t it risky, shouldn’t there be certain basic rules the data should adhere to?”. And the answer is also the same: no, the decision is with the user and their wallet.

I hear you. However, unlike the data field of a regular transaction. The user wouldn’t understand the code at a particular address. There is no easy means to interpret the code as well, is there?

---

**StanislavBreadless** (2023-07-26):

If I understand the gas pricing correctly (i.e. the deployment cost does not depend on the size of the contract), I think this EIP will become the de-facto standard of deploying copies of contracts.

So basically instead of using things like minimal proxies (which actually involve additional costs for users for relaying the calldata via `delegatecall`s), the users will generate an EOA, send funds to it. Migrate it to a contract that in its initializer will send funds back to the initial deployer.

Not a bad thing per se, but an interesting implication.

---

**ryanschneider** (2023-07-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stanislavbreadless/48/5336_2.png) StanislavBreadless:

> Not a bad thing per se, but an interesting implication.

Hmm, any idea yet how an “ideal client” will actually implement this EIP?  If they can actually just point to the code of the existing contract then ya this approach being cheaper feels fine, but if the code actually does need to be copied then it does seem like the gas cost should reflect that.

---

**yoavw** (2023-07-27):

Neat and minimalist design ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

Setting the code to reference an existing one in the database is a good optimization.

Clarification question:

I understand that after setting the code, the account is called with `data` and `value`.  Is the transaction atomic?  I.e. if this call reverts, will it revert the entire transaction and keep the account codeless?  I think it should, as it allows sanity checks and prevents user mistakes that might result in loss of the account.

A couple of thoughts about design trade offs:

Transaction type vs. an opcode that combines `AUTH`+`AUTHUSURP`, i.e. a `SETEOACODE` opcode:

- Transaction type is easier to reason about, and for wallets to identify and treat with extreme care.
- However, gas abstraction becomes harder.  The EOA must have eth to pay for its migration.
- With an opcode, any gas abstraction system could sponsor the migration.  E.g. the 4337 EntryPoint singleton could trigger the migration, so a paymaster could pay for it.
- Common use case: user gets USDC to an EOA, has no eth, wants to use TokenPaymaster.
- The downside with the opcode approach is that it’s now just a signed message.

Setting storage slots vs. calling an `account.init()`

- When setting storage slots, deployment is a bit complicated (having to calculate storage slots for mappings and dynamic arrays).
- Harder to verify the deployment later (no information about mapping assignment, e.g. a Safe where there’s no way to know for sure who the signers are, or what modules are installed - only to verify known ones).
- The slots could be set by an init() call when the account is called with data after setting the code.
- What’s the rationale for offering the storage tuples list method?

tx.origin hashing - nice way to placate these projects, but should we?

- tx.origin “protection” has been proven problematic many times in the past.
- It is one of the two biggest obstacles to AA adoption (the 2nd one being lack of EIP-1271 support).
- AA might never become a 1st class citizen if we don’t let contract accounts be tx.origin.
- While it’s a bit out-of-scope for this EIP, maybe we should keep tx.origin=account in this transaction, if only as a statement for the future.

One-time migration

- Seems like the right choice.  Otherwise the account remains exposed to the old key forever.
- We’re finally getting rid of homomorphic contracts by removing SELFDESTRUCT.  It wouldn’t be great to add them back through multiple-migrations of EOAs.

Cheap storage

- Encouraging migration is awesome, but is there a risk that it would become a cheap way to deploy and initialize non-AA contracts?
- Projects might start deploying instances of their contracts by converting EOAs if it’s cheaper.
- Not a huge deal but these contracts will be opaque to users due to the storage assignment (no way to associate slots with mappings, so a token contract might have an arbitrary balance for some unknown address).
- Can we somehow discourage that without losing the benefit of cheap storage for AA migration?

Security consideration:

As [@rmeissner](/u/rmeissner) noted, the problem isn’t just `permit` but also other chains (including future chains that don’t even exist at the time of migration).  The EOA’s original key remains important after switching to AA.  Since there is no way to mitigate this risk, I’d add these recommendations to AA wallet devs:

1. Do not use this as the default path when creating new accounts.  By default, deploy the account using a normal CREATE2 unless the user explicitly asks to keep an existing EOA address.  This pertains to the next billion users, who currently don’t have an EOA.
2. If a user chooses to take the EOA migration path, explain the implications clearly: the EOA key remains in effect on other chains so it should still be treated accordingly after migration.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> Possibly? I am curious what you, other wallet devs, and core devs think. I think it would probably be a separate EIP in general, but we may bundle the two together. I have generally been for adding a check in ecrecover to see if the recovered account has code deployed and fail if it does as it neutralizes this issue. Not sure if there are unforeseen effects downstream.

Would be great if we could do this, but doesn’t it change the pricing model for ecrecover?  It adds an additional `EXTCODEHASH` to a cold account (2600 gas).  If ecrecover become more expensive, it could in theory break existing contracts.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ryanschneider/48/945_2.png) ryanschneider:

> Is there a timing attack vector of some sort where I convince you to send a tx to an EOA but then convert the EOA to a contract by colluding w/ a block producer to put my migration transaction before yours? I feel like the fact that the “type” of an address is no longer immutable should be mentioned in the security considerations.

While the timing attack is possible, I think it’ll be hard to exploit it in any meaningful way.  The victim’s wallet would see that it’s sending to an EOA, and cap gas at 21000.  The deployed contract wouldn’t be able to do anything so it’ll just cause a fairly cheap revert.

---

**matt** (2023-07-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stanislavbreadless/48/5336_2.png) StanislavBreadless:

> If I understand the gas pricing correctly (i.e. the deployment cost does not depend on the size of the contract), I think this EIP will become the de-facto standard of deploying copies of contracts.

If core devs are okay with this format for deploying contacts, I think it should also be available in the EVM. Either way, this is not a trustworthy way to deploy a multi-tenant contract (e.g. a defi protocol), because they can’t prove they don’t also own the private key for the account.

Might be able to skirt around that though by constructing a creating a synthetic signature (a sig constructed arbitrarily where the private key isn’t know, but you can then derive the address for a one-time transaction).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ryanschneider/48/945_2.png) ryanschneider:

> Hmm, any idea yet how an “ideal client” will actually implement this EIP? If they can actually just point to the code of the existing contract then ya this approach being cheaper feels fine, but if the code actually does need to be copied then it does seem like the gas cost should reflect that.

Geth reads and writes code from disk using the [hash as the key](https://github.com/ethereum/go-ethereum/blob/2274a03e339f213361453590b54917bbfd0a0c31/core/rawdb/accessors_state.go#L82-L87). I assume most clients do it this way. So to implement this, you would just load the target address from disk and set the EOA’s code hash to the same code hash as the target.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> if this call reverts, will it revert the entire transaction and keep the account codeless?

This is a good question, the spec isn’t clear on this. I agree it should be kept codeless upon revert.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Transaction type is easier to reason about, and for wallets to identify and treat with extreme care.

In both cases you have a EIP-2718 type byte as prefix. So the wallet identify equally easily both 3074 and 7377 messages.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> However, gas abstraction becomes harder. The EOA must have eth to pay for its migration.
> With an opcode, any gas abstraction system could sponsor the migration. E.g. the 4337 EntryPoint singleton could trigger the migration, so a paymaster could pay for it.
> Common use case: user gets USDC to an EOA, has no eth, wants to use TokenPaymaster.
> The downside with the opcode approach is that it’s now just a signed message.

Fully agree abstraction becomes harder. I prefer to have an opcode, but one complaint [@vbuterin](/u/vbuterin) had in the past is he didn’t want to further enshrine ECDSA in the EVM. Now I disagree with that - but still, EIP-7377 comes more to address that perspective.

For better or worse, EIP-7377 is simpler to reason about than EIP-5003 and that may be what we need.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> What’s the rationale for offering the storage tuples list method?

The motivation is to minimize the cost to the user to migrate. Running initcode does cost gas. We could optimize it more, but allowing the user to apply the entire migration and begin using it normally in the same transaction (w/o additional setup) is neat. It’s not a feature I feel strongly about though, if it needs to go and we rely on the first call - sure. But the fact it is harder to verify deployments later is simply a sign of immaturity in our tooling. The storage locations are deterministic. It would not be hard to making it clearer both in the safe contract and using external tools to know that slot X1, X2, … etc. represent the owners of the wallet.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> tx.origin hashing - nice way to placate these projects, but should we?

Migrating EOAs is extremely useful even in just an ERC-4337 world with this tx.origin fix. I worry that doing to much with the EIP will cause it to fail. But I am open to removing it.

The [dedaub audit](https://dedaub.com/blog/eip-3074-impact) was fairly clear: there are a lot of contracts using this check, but none were found to be vulnerable to exploit if the invariant broke. So yes, it is something to consider.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Encouraging migration is awesome, but is there a risk that it would become a cheap way to deploy and initialize non-AA contracts?

I will think about this. I didn’t consider this a viable path for protocols to deploy projects due to danger that the private key for the deployed account may be known (and could therefore use permit). But yes this has been raised several times and so we’ll need a better answer.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Would be great if we could do this, but doesn’t it change the pricing model for ecrecover? It adds an additional EXTCODEHASH to a cold account (2600 gas). If ecrecover become more expensive, it could in theory break existing contracts.

Yes this is a consideration. But for a long time devs have known to not rely on specific costs of EVM operations, so I will be surprised if many things were to break.

–

Thanks for the feedback [@yoavw](/u/yoavw) !

---

**chendatony31** (2023-07-27):

When an EOA wallet is upgraded to a AA, some contracts (maybe some defi protocols) may refuse the contract address to interact with, I think it may cause some problems, for example, the user can’t withdraw assets from these protocols. ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12)


*(31 more replies not shown)*
