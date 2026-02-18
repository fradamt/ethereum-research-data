---
source: magicians
topic_id: 4025
title: "\"Rich transactions\" via EVM bytecode execution from externally owned accounts"
author: Arachnid
date: "2020-02-24"
category: Uncategorized
tags: [evm, rich-transactions]
url: https://ethereum-magicians.org/t/rich-transactions-via-evm-bytecode-execution-from-externally-owned-accounts/4025
views: 5418
likes: 21
posts_count: 47
---

# "Rich transactions" via EVM bytecode execution from externally owned accounts

I’ve written up an EIP draft proposing a way for externally owned accounts to execute per-transaction bytecode, [here](https://github.com/Arachnid/EIPs/blob/richtx/EIPS/EIP-draft-rich-transactions.md). Feedback appreciated!

## Replies

**fubuloubu** (2020-02-24):

So, `SELFDESTRUCT` could be run multiple times for a given EOA?

---

**MicahZoltu** (2020-02-24):

While not critical, it may be *valuable* to mention how DELEGATECALL works.  It should be obvious to everyone, but I generally like how you explicitly called out most opcodes even when they should have been obvious.

---

**Recmo** (2020-02-24):

Can you add a line or two on the gas cost of the `SELFDESTRUCT` opcode? The gas refund would be inappropriate (frankly dangerous), since there is no matching `CREATE`.

---

**MicahZoltu** (2020-02-24):

What is the motivation for this?

> A call to the precompile address from a contract has no special effect and is equivalent to a call to a nonexistent precompile or an empty address.

From the cheap seats, it seems like it would be easier (implementation wise) to have a contract calling the precompile behave the same as an EOA calling the precompile, where it essentially is a delegate call to the code supplied in the CALLDATA.  This way clients don’t have to switch on caller.

---

**MicahZoltu** (2020-02-24):

> Any value sent in the transaction is transferred to the precompile address before execution, and is thus inaccessible.

This seems like it would be prone to error (foot gun).  Why not just have any value sent be a no-op?  How does `DELEGATECALL` work with value currently?

---

**Recmo** (2020-02-24):

> A new reserved address is specified at x , in the range used for precompiles. When a transaction is sent to this address from an externally owned account, the payload of the transaction is treated as EVM bytecode, and executed with the signer of the transaction as the current account.

Wouldn’t it be cleaner to have this as new kind of signed transaction message instead of as a somewhat odd precompile? It would add functionality at a place where we don’t usually do it, but it feels more natural.

---

**Recmo** (2020-02-24):

This breaks security assumptions in things like `transferAndCall`

---

**MicahZoltu** (2020-02-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recmo/48/2516_2.png) Recmo:

> Wouldn’t it be cleaner to have this as new kind of signed transaction message

Almost certainly, but no one so far has been willing to put the time into drafting a transaction versioning EIP, which requires a pretty strong understanding of the P2P protocol and has an impact on many layers of the system (all of which currently make assumptions about there being exactly one transaction format).

If you have the time, you should *definitely* talk to [@AlexeyAkhunov](/u/alexeyakhunov) about his ideas for transaction versioning system, and additional transaction types.  Solving this problem would open the doors to all sorts of goodness including this, the ability to have transactions which bundle multiple other transactions, the ability to have the gas payer be different from the signer, etc.

---

**MicahZoltu** (2020-02-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recmo/48/2516_2.png) Recmo:

> This breaks security assumptions in things like transferAndCall

Can you provide a bit of detail on the pattern and why it is broken by this?  `isHuman` checks definitely break, but I think the consensus of the dev community is that `isHuman` checks are *already* broken and they shouldn’t be used in the first place.

---

**Arachnid** (2020-02-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> So, SELFDESTRUCT could be run multiple times for a given EOA?

Yes. It can already be run multiple times on a contract account, thanks to CREATE2.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> While not critical, it may be valuable to mention how DELEGATECALL works. It should be obvious to everyone, but I generally like how you explicitly called out most opcodes even when they should have been obvious.

Done!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recmo/48/2516_2.png) Recmo:

> Can you add a line or two on the gas cost of the SELFDESTRUCT opcode? The gas refund would be inappropriate (frankly dangerous), since there is no matching CREATE .

Done!

Would it be simpler for implementers if I specified that `SELFDESTRUCT` reverts, instead?

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> From the cheap seats, it seems like it would be easier (implementation wise) to have a contract calling the precompile behave the same as an EOA calling the precompile, where it essentially is a delegate call to the code supplied in the CALLDATA. This way clients don’t have to switch on caller.

Recmo points out why this would be dangerous. It allows you to force any contract that is willing to make arbitrary calls for you (presently relatively harmless in many situations) to execute arbitrary bytecode in its context. Even if the contract only calls a specified function at an address you provide, we’d have to vet the meaning of every 4-byte function signature as EVM bytecode to be sure they’re safe!

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> This seems like it would be prone to error (foot gun). Why not just have any value sent be a no-op? How does DELEGATECALL work with value currently?

`DELEGATECALL` doesn’t have a value parameter. I specified it this way because that’s how `CALL`s with value to all other accounts behave, and I wanted to avoid adding more special cases.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recmo/48/2516_2.png) Recmo:

> Wouldn’t it be cleaner to have this as new kind of signed transaction message instead of as a somewhat odd precompile? It would add functionality at a place where we don’t usually do it, but it feels more natural.

I was wondering about that too. One option, for instance, would be to allow transactions with 21-byte `to` fields, where the first byte is interpreted as a call type. We’d define one new call type, which effectively `DELEGATECALL`s the target address instead of `CALL`ing it.

There are pros and cons. It would reduce some of the special-casing required in this proposal, but you’d still have to special case some things, such as `SELFDESTRUCT`. It would reduce transaction size for commonly executed operations, but make doing ad-hoc operations harder.

It would also likely confuse a lot of tools that rely on being able to parse transaction objects, which is more concerning to me.

---

**PhABC** (2020-02-24):

> SLOAD  and  SSTORE  operate on the storage of the EOA. As a result, an EOA can have data in storage, that persists between transactions.

What’s the rationale for this? I can think of some fun use cases, but wondering what you were thinking of. Also, what kind of can of worms can this open?

---

**Arachnid** (2020-02-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/phabc/48/81_2.png) PhABC:

> What’s the rationale for this? I can think of some fun use cases, but wondering what you were thinking of. Also, what kind of can of worms can this open?

It seemed like prohibiting would be adding unnecessary special-cases.

---

**sergio_lerner** (2020-02-24):

What happens if a contract called by the EOA then calls back the EOA. Will the code sent in the transaction data field still be there or will the code be empty  (as in a contract initialization) ?

---

**mudgen** (2020-02-24):

This seems like it would be very useful. [@Arachnid](/u/arachnid) are you providing the implementation of this?

---

**Arachnid** (2020-02-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sergio_lerner/48/1759_2.png) sergio_lerner:

> What happens if a contract called by the EOA then calls back the EOA. Will the code sent in the transaction data field still be there or will the code be empty (as in a contract initialization) ?

The EOA doesn’t have code; I tried to make that clear by specifying what `EXTCODE*` etc return - I’m open to suggestions on how to clarify further.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mudgen/48/1027_2.png) mudgen:

> This seems like it would be very useful. @Arachnid are you providing the implementation of this?

I’m not certain I’ll have time to. If there’s interest in including this in a fork, I can probably put together a geth implementation, though.

---

**sinamahmoodi** (2020-02-24):

I wonder if this opens a new attack vector against users, or negatively affect UX because the code is sent every time and there’s no immutable code deployed which can be checked/audited by everyone. Do I have to read the code every time I use a wallet website? Why not go the extra mile of assuming EoAs can have code (still different from contracts in that they can sign txes)?

---

**Recmo** (2020-02-24):

> […] SLOAD SSTORE
> It seemed like prohibiting would be adding unnecessary special-cases.

Leaving it in requires the special treatment of `SELFDESTRUCT` and maintaining state for EOA accounts. Additionally, state on EOA may complicate future state rent proposals. I’d consider these also special-cases. So something inelegant will happen either way.

It’s worth considering a proposal where `SLOAD`, `SSTORE` and `SELFDESTRUCT` become `INVALID/DONTUSE`. I don’t think this necessarily more complicated than the current proposal. (In fact, I’d argue that it’s simpler)

So let’s think about what the potential usescase of EOA state could be, to see if there is a good reason to keep it.

First, State would only be used to communicate between two EOA transactions. Inside a single tx it can just use memory.

- This can be useful if there are multiple signers with no other means to communicate, but if you share a private key and nonce counter, we can assume you already have an offchain communication channel.
- It can also be useful when some data is not available at the time of signing, but will be when a previous transaction finishes. I.e. a transaction does something, and a second transaction that depends on the outcome. But the whole point of this proposal is that we can merge those kinds of transactions into one.

I’m struggling to come up with a usecase for state in EOA accounts, and think it would be cleaner to not have it.

Also note that if we mark those opcodes `INVALID/DONTUSE`, then we can always add EOA state in a separate future proposal in a backwards compatible manner.

Finally, someone who needs EOA in a one-of case can deploy a contract that only listens to the EOA address and stores state on its behalf.

---

**Recmo** (2020-02-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> Wouldn’t it be cleaner to have this as new kind of signed transaction message instead of as a somewhat odd precompile? It would add functionality at a place where we don’t usually do it, but it feels more natural.

I was wondering about that too. One option, for instance, would be to allow transactions with 21-byte `to` fields, where the first byte is interpreted as a call type. We’d define one new call type, which effectively `DELEGATECALL` s the target address instead of `CALL` ing it.

Actually, I think the current precompile address is a very good solution. Currently we have (AFAIK) two transaction types:

- Contract calls, where to contains the contract to call and ether, gas and calldata is provided. (Plain EOA ETH transfers are a special case of this).
- Contract deployments, where to is the special flag value 0x00 and calldata contains a constructor, to be executed in the context of the newly created account, and returns the code that should be stored there.

What we want is similar to the second, except calldata is now executed in the context of the EOA account, and we don’t store any code at the end.

So there’s already a precedent for using flag-values in `to`. It seems natural to add one more.

My questions stems from the observation that this new transaction type is so powerful that it can replace the other two (first one would become a `CALL`, the second a `CREATE`). And when you implement them this way, you no longer need a `to` field in the transaction, so you couldpropse a new transaction message that does not include a `to` field and implements this proposal, which can then replace all existing transaction types.

This is a drastic change in the tx format though, and before this proposal it didn’t occur to me that it could also be done using a precompile-address + flag value. This is a great insight that allows ‘rich transactions’ to be implemented separately from a transaction format refactor!

---

**shemnon** (2020-02-24):

How does this differ from a contract creation transaction that doesn’t return a contract?  Init code still gets called and the empty account does not get generated.

This is a pattern I already used in the Ethereum Reference Tests - https://github.com/ethereum/tests/blob/develop/src/GeneralStateTestsFiller/stSStoreTest/sstore_gasLeftFiller.json#L75

---

**Arachnid** (2020-02-24):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/f04885/48.png) sinamahmoodi:

> I wonder if this opens a new attack vector against users, or negatively affect UX because the code is sent every time and there’s no immutable code deployed which can be checked/audited by everyone. Do I have to read the code every time I use a wallet website? Why not go the extra mile of assuming EoAs can have code (still different from contracts in that they can sign txes)?

RE immutability: The code is preserved in the transaction payload, which can be read and analyzed like any other.

I’d recommend that if this were adopted, wallets flag transactions to the target address with a warning message; it’d also be worth writing up a spec for a new RPC endpoint that wallets can support which accepts, say, a list of operations, and leaves it to the wallet to compose the bytecode. That way, the wallet can provide the user with a useful list of operations instead of an opaque blob to sign.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recmo/48/2516_2.png) Recmo:

> Leaving it in requires the special treatment of SELFDESTRUCT and maintaining state for EOA accounts.

No, `SELFDESTRUCT` requires special-casing either way; without storage you still need to make sure it doesn’t zero out the nonce.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recmo/48/2516_2.png) Recmo:

> Additionally, state on EOA may complicate future state rent proposals. I’d consider these also special-cases. So something inelegant will happen either way.

True, but I don’t believe any of those are mature enough to say whether they’re an issue or not.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recmo/48/2516_2.png) Recmo:

> It’s worth considering a proposal where SLOAD , SSTORE and SELFDESTRUCT become INVALID/DONTUSE . I don’t think this necessarily more complicated than the current proposal. (In fact, I’d argue that it’s simpler)

I’m onboard with the idea of prohibiting `SELFDESTRUCT`, though I’d like to hear from implementers which option is simplest. I still don’t think there’s a compelling reason to prohibit storage access.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recmo/48/2516_2.png) Recmo:

> I’m struggling to come up with a usecase for state in EOA accounts, and think it would be cleaner to not have it.

I really don’t think “we can’t think of a use-case right now” is a good reason to create a new special-case to prohibit something; we should prohibit something only if it’s reasonably likely to introduce complication to clients, or have security implications.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recmo/48/2516_2.png) Recmo:

> So there’s already a precedent for using flag-values in to . It seems natural to add one more.

In that event, should we specify instead that the `to` field should be a single byte, similar to contract creation, rather than a 20-byte address?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> How does this differ from a contract creation transaction that doesn’t return a contract? Init code still gets called and the empty account does not get generated.

Unlike that, this executes in the context of the EOA, which allows it to make use of resources owned by the EOA. A contract-creation TX is unable to operate on resources owned by its creator.


*(26 more replies not shown)*
