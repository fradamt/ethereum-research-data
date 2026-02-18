---
source: magicians
topic_id: 4355
title: "EIP-2718: Typed Transaction Envelope"
author: MicahZoltu
date: "2020-06-13"
category: EIPs > EIPs core
tags: [transactions]
url: https://ethereum-magicians.org/t/eip-2718-typed-transaction-envelope/4355
views: 69177
likes: 34
posts_count: 76
---

# EIP-2718: Typed Transaction Envelope

Discussion thread for [EIP-2718: Typed Transaction Envelope](https://eips.ethereum.org/EIPS/eip-2718).

# Description

Defines a new transation type that is an envelope for future transaction types.

`rlp([TransactionType, [...])` will be a valid transaction where `TransactionType` is a number identifying the format of the transaction and `[...]` is the transaction, whose definition is defined in future EIPs. The first new transaction will be just a wrapped legacy transaction with the format `rlp([0, [nonce, gasPrice, gasLimit, to, value, data, senderV, senderR, senderS]])`.

## Replies

**MicahZoltu** (2020-06-13):

## 0x32: ORIGIN: tx.origin

Smart contract developers have been told for a long time to avoid using the `ORIGIN` opcode and static analysis tools tend to warn when it is used.  Most uses of it are people attempting to author contracts that disallow contract callers, which goes against the ethos of Ethereum (IMO) and goes against the idea that contracts can own and manage money.  Contracts that disallow contract callers discourage the usage of smart wallets, which tend to have enhanced security features for end users thus preventing their usage decreases end-user security.

With the introduction of multiple types of transactions, it is possible that the definition of `ORIGIN` may change over time, or differ between transaction types.  EIP-2711 for example will likely assert that `ORIGIN` is the `GAS_PAYER`, rather than the `SENDER`.  One can imagine a multisig transaction type where multiple signatures control the operation of a single account, or rich transactions where an account with a private key can have a contract gating its operations.  In these cases, what `ORIGIN` means may vary slightly, and currently the EVM doesn’t have insight into the type of transaction.

## Potential Solution

Change opcode `0x32` to be `TRANSACTION_DATA`, where the first 32 bits are the transaction type, and the remaining 224 bits are defined per `TransactionType`.  For `TransactionType` `0` (wrapped legacy transactions), this would be backward compatible since currently `TRANSACTION_DATA` would be an address, which has 96 leading `0` bits.  For `TransactionType` `1` (EIP-2177), the value would be something like `0x000000010000000000000000cafebabecafebabecafebabecafebabecafebabecafebabe` where the first 32-bits is the `TransactionType` (`1` in this case) and the remaining 224 bytes would be an Ethereum address representing `GAS_PAYER`.  This would allow the EVM to both identify what type of transaction is running, and also have a small amount of transaction-type specific data available to it.  Some transaction types may have no data, in which case it would just be 32 high bits containing the transaction type and the rest of the bits would be `0`.

### Backward Compatibility

This does potentially have a backward compatibility issue with existing contracts that reference `tx.origin`, but since the high bits are the transaction type we don’t have to worry about collisions with actual addresses for anything other than legacy transactions, which would retain the old semantics of `ORIGIN` means transaction signer.

For new type transactions, they’ll just fail *all* comparisons of `tx.origin` and any Ethereum address.  There is *potential* that there are contracts which store `tx.origin` of some original caller and then require the same `tx.origin` later.  If a non-0 type transaction was used for the first and a 0 type transaction was used for follow-ups this won’t match.  Also, if you do something like an EIP 7211 transaction you may end up with different `GAS_PAYER`s and would not match.

Personally, I have lobbied long and hard against contracts that use `tx.origin` for basically anything, so I don’t have a problem finally breaking people who have failed repeatedly to heed the warnings.  Also, such contracts **CAN** just tell their users to only use legacy type transactions and they will continue to work, so it isn’t like we would be sticking people’s funds in a way that was unpreventable for existing contracts.

---

**matt** (2020-06-14):

I have a few thoughts on how the existing (legacy) transaction format should be handled in this EIP.

**1. Should the protocol continue to support the legacy transaction format?**

I believe the answer is yes, but with some caveats. There are many existing tools that have been built for this format and it is unreasonable to deprecate it without a warning far in advance. However, I don’t think that the legacy tx format should be supported at the *protocol* level (devp2p). Hard forks are inherently not backwards compatible, so there isn’t an advantage of continuing to support them at that layer. The only caveat is that the `0` tx type must continue to follow the legacy hashing format (e.g. the tx hashed as it is now, without the tx type) so existing signing tools don’t need to be updated. By completely removing the legacy tx format, txs can be decoded without relying on a “high bit” since a client will never expect the first element in a tx to be anything other than a tx type identifier. We can lean on the clients’ RPC endpoints for support in this transition. For example, all endpoints can continue operating as they do today and accept legacy txs as input, then transform them into a typed tx or filter out non-legacy txs for outputs, then strip them of their tx type. An optional flag can be added to the endpoints to denote whether the requester would prefer to send / receive transactions encoded in the typed format or legacy format. This will allow backwards compatible to be maintained with existing tools.

**2. Should the legacy transaction format ever be deprecated?**

Since the protocol no longer recognizes the legacy transaction format, I don’t see any reason to not put an end-of-life date on it a few hard forks in advance. This will give teams enough time to update their systems to support the new tx format, at which point the tx hash logic can be updated for `0` typed txs to follow the standard procedure.

**3. Should transactions be in a two element “envelope” structure?**

I argue no. Because I don’t believe there is a need to continue supporting the legacy format, there is no advantage of the envelope structure versus a flat structure. When decoding, clients will *always* expect the first element to be the tx type. The flat structure will be simpler to reason about and will save a few superfluous bytes denoting the length of the enveloped list.

---

**MicahZoltu** (2020-06-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> However, I don’t think that the legacy tx format should be supported at the protocol level (devp2p). Hard forks are inherently not backwards compatible, so there isn’t an advantage of continuing to support them at that layer. The only caveat is that the 0 tx type must continue to follow the legacy hashing format (e.g. the tx hashed as it is now, without the tx type) so existing signing tools don’t need to be updated.

I originally was somewhat against this, but in the process of writing up a response I have talked myself into aligning with you on the matter.  The clients’ JSON-RPC (or other) interface can still accept and return legacy style transactions and update at their leisure or create a new endpoint for returning legacy style transactions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> Since the protocol no longer recognizes the legacy transaction format, I don’t see any reason to not put an end-of-life date on it a few hard forks in advance. This will give teams enough time to update their systems to support the new tx format, at which point the tx hash logic can be updated for 0 typed txs to follow the standard procedure.

An end-of-life policy would be per client I think.  I don’t believe there is any need for cross-client consensus beyond what you have proposed in (1), which would end-of-life it for dev2p2 at `FORK_BLOCK_NUMBER`.  I certainly would support and lobby for individual clients setting up an EOL policy for the JSON-RPC though (outside of the EIP/hardfork process).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> I argue no. Because I don’t believe there is a need to continue supporting the legacy format, there is no advantage of the envelope structure versus a flat structure. When decoding, clients will always expect the first element to be the tx type. The flat structure will be simpler to reason about and will save a few superfluous bytes denoting the length of the enveloped list.

Right now we can decode a transaction with no context other than a byte array.  It even has a weak form of consistency from RLP such that you can be reasonably confident whether or not you have a 9 item RLP encoded thing by just seeing if it decodes without a buffer overrun/underun.  You can further validate that you have a transaction by verifying the signature.  *In theory*, someone may create a transaction type in the future that has an 8 item payload (say, `TransactionType=5`) and whose signature is the last 3 items of the payload and signs the full transaction (including the `TransactionType`).  At such a time, if someone were to give you a byte array you would not be able to tell whether it was a legacy transaction with nonce 5 or a type 5 transaction.

While this may be a bit of an edge case that is *unlikely* to ever be hit, I dislike having one more foot-gun that future Ethereum developers have to worry about and keep in the back of their heads.  It is that accumulation of gotchas that, over time, builds up to the point where someone forgets a gotcha and we have problems.  Personally, I would rather spend the extra byte per transaction and avoid the gotcha than have it looming over us forever.

---

[@pipermerriam](/u/pipermerriam) over in Discord had a good suggestion (IMO) for this EIP which is to make the second item just be a byte array, rather than an RLP list.  This would allow future transactions to be encoded using a different encoding format such as ssz or even something custom.  I prefer that over the current proposal of forcing the second item being an RLP encoded list.

---

**MicahZoltu** (2020-06-15):

I just merged a set of changes to this EIP.  The highlights are that I have taken [@pipermerriam](/u/pipermerriam)’s suggestion about having the second parameter be an opaque value, with `TransactionType=0` being an `rlp` encoded legacy transaction, and taking [@matt](/u/matt)’s suggestion that we should not support legacy transactions over devp2p and instead only support new type transactions.

Both changes combine to make it so that tooling doesn’t need to change aside from clients because clients can simply wrap legacy transactions in `TransactionType=0` transactions with almost no hassle.  In theory, we don’t even need to add an JSON-RPC endpoint or make any JSON-RPC endpoints at or before `FORK_BLOCK_NUMBER`, that can be done more “lazily” by individual clients over time (though, a standard for among clients would be hugely valuable).

---

**pipermerriam** (2020-06-15):

I am *interested* in exploring the solution space for how we can deprecate the old format in a more universal way.  I like that we have mechanisms through which we can still *support* the old format, but I think we’d benefit from a strategy that let us *eventually* migrate all tooling to the new format.

In the legacy format, the transaction hash is defined as `keccak(legacy_9_item_rlp_transaction)` and the signature is `sign(first_6_items_of_legacy_txn)`.  I would propose that we add a *new* version of the old transaction which:

1. includes the TransactionType as part of the signature.
2. computes the hash as  `keccak(rlp([TransactionType, ]))

This give us both a *legacy* version of the current transaction format **and** a modernized version, allowing us to differentiate between transactions that are still being created using *old* tooling and ones using the new modern approach.

My thought is that we can leverage this to add a “fee bomb” into the protocol.  The exact mechanism is up for debate, but I would propose:

1. have the bomb slowly ramp up transaction fees for legacy transactions

start small and ramp up to something like 2-10x multiplier on the fees.
2. have be bomb kick in in a 12-24 month timeframe.

The rational for ramping up the transaction fees for legacy transactions is that it provides a financial incentive to get off the tooling that is still using the old format.  This incentive should work for both users and developers since users will not want to pay higher fees and developers of transaction signing infrastructure should be sensitive to the needs of their users.

The benefits I see from being able to fully leave behind the legacy format are:

1. reduced complexity for client and tooling developers (no need to special case the old format).
2. reduced complexity for future protocol changes (no extra special rules for if TransactionType == 0)

I’m curious to hear what other people think about this.

---

**pipermerriam** (2020-06-15):

I think the spec is missing a section on how transaction hash should be computed.  It seems like for the legacy `TransactionType` we are unable to change, but we might benefit from having a defined standard for new types assuming we can come up with a scheme that we expect to be forwards compatible.  I would suggest:

1. The TransactionType must be included in the fields that are signed.
2. The hash must be computed from the full transaction payload `keccak(rlp([TransactionType, [, …]]))

These rules would only apply to all *new* transaction types, with the legacy type being stuck with the legacy rules for signing and hashing (see my previous post on adding a second type here that follows the new convention).

---

**MicahZoltu** (2020-06-16):

[@pipermerriam](/u/pipermerriam) Why a fee bomb instead of just a well defined EOL schedule?  Even with a fee bomb, we would still need an EOL schedule  in order to stop supporting legacy transactions, and it is unclear to me what value the fee bomb adds if an EOL schedule is still necessary.

Is the fear that people will procrastinate upgrading their tooling and then be upset in 1-2 years when all of a sudden it stops working?

---

**MicahZoltu** (2020-06-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pipermerriam/48/65_2.png) pipermerriam:

> The TransactionType must be included in the fields that are signed.
> The hash must be computed from the full transaction payload `keccak(rlp([TransactionType, [, …]]))

I’m a little hesitant to make any assertions about what **MUST** be included in a transaction’s signature, mainly because I am hesitant to make assertions in this document about what it even means to “sign” something.  I would like to leave the system as flexible as possible for future transaction types so that things we haven’t thought of today are possible, and the best way I think to achieve that is to put as few requirements on the transaction as possible.

I generally think it is a good idea for transaction types to sign the `TransactionType`, as it removes the possibility of various types of replay attacks, but maybe some future transaction types are specifically designed to enable certain classes of replay (e.g., sign a transaction that can be submitted as either type 5 or type 6 or both).

---

**pipermerriam** (2020-06-16):

I’m good changing the signing language to **SHOULD**.  The idea that we don’t know what future transaction types will look like, how they will be signed, etc, makes enough sense to me.

---

**MicahZoltu** (2020-06-16):

I added a **SHOULD** for signing `TransactionType`.

---



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/2730)














####


      `master` ← `MicahZoltu:patch-3`




          opened 03:49AM - 16 Jun 20 UTC



          [![](https://avatars.githubusercontent.com/u/886059?v=4)
            MicahZoltu](https://github.com/MicahZoltu)



          [+6
            -0](https://github.com/ethereum/EIPs/pull/2730/files)













I have added some text about what ORIGIN and CALLER mean going forward.  For `TransactionType` `0` they are fully backward compatible and the change is invisible to contracts.  However, for all other transaction types, the value of both `ORIGIN` and `CALLER` will have a transaction-dependent meaning.  For `ORIGIN`, I feel like the risks are pretty low.  However, I am concerned that for `CALLER` the risks in this change are a bit more significant.

Do people think that we are OK to redefine `CALLER` for future transaction types?  We could allow its contents to be determined per transaction type, but require that it always be an address (never some other data) so that existing contracts won’t choke on receiving a non-address `CALLER`.

---

**matt** (2020-06-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pipermerriam/48/65_2.png) pipermerriam:

> My thought is that we can leverage this to add a “fee bomb” into the protocol.

I’m not strongly for or against a fee bomb. I do believe a fee bomb will unduly increase the complexity. Depending on EIP-1559, there could be a major change to the transaction format in the near future anyways. Their solution is to slowly scales down the fraction of the block dedicated to legacy transactions.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Do people think that we are OK to redefine CALLER for future transaction types? We could allow its contents to be determined per transaction type, but require that it always be an address (never some other data) so that existing contracts won’t choke on receiving a non-address CALLER .

I don’t think it is okay to redefine `ORIGIN` or `CALLER` in this way.

1. There are no other opcodes which pack multiple return values into a single word
2. We’d need to analyze every contract and determine if modifying the high 32-bits would break anything.

I believe a new opcode for `TransactionType` would be preferable. However, we should be cautious of allowing contracts to access such information. Are there compelling use cases for this? We can always add it later via a new EIP.

If we’re going to colloquially rename opcodes, I believe renaming `ORIGIN` to `GASPAYER` would make more sense. As new transaction types are proposed we can decide if there is value in adding a type-dependent data opcode.

---

**MicahZoltu** (2020-06-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> If we’re going to colloquially rename opcodes, I believe renaming ORIGIN to GASPAYER would make more sense. As new transaction types are proposed we can decide if there is value in adding a type-dependent data opcode.

The problem is that in the context of the generalized concept of typed transactions (not sponsored transactions specifically), we cannot assert what `ORIGIN` or `CALLER` means globally.  Each transaction type will need to define what those opcodes return and for some it may not be comparable to what legacy transactions return for those opcodes.  While for EIP 2711 it *may* not break things too badly if we jam the gas payer into `ORIGIN` and the `SENDER` into caller, I am not confident that the same will be true for all future transaction types.  If we want the freedom to create new transaction types going forward, then I think we need to solve the problem of `ORIGIN`/`CALLER`.

One option that is a bit of a middle ground is that we could assert that `ORIGIN` and `CALLER` must always be an address, but we cease asserting what those addresses represent.  If we were to go that route then I think we should add a new opcode for Transaction Type so that contracts can figure out what those two addresses represent.

Alternatively, we could assert that all transaction types must have a `CALLER` that represents “the address that will be considered to have called the contract”.  This constrains what we can do with transactions (what would a 2 of 2 multisig contract set for `CALLER`?), but maybe it is a reasonable constraint?

The last option is to assert that `ORIGIN == <CALLER of first frame>`, and `CALLER` is always an address and each Transaction Type would define what that address is.  I think this is the most backward compatible solution, but it means we’ll have to create a new opcode for `TRANSACTION_DATA` and `TRANSACTION_TYPE` (or we could bit pack them if we want to try to save opcodes).

---

**matt** (2020-06-16):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> If we want the freedom to create new transaction types going forward, then I think we need to solve the problem of ORIGIN / CALLER .

I don’t think think we need to boil the ocean in this EIP. I can’t come up with any use cases where `CALLER` wouldn’t refer to the address of the entity making a call. If there are, we should could address them. However, I don’t see a benefit in altering a widely used opcode to support potential transaction types.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> While for EIP 2711 it may not break things too badly if we jam the gas payer into ORIGIN and the SENDER into caller, I am not confident that the same will be true for all future transaction types.

`ORIGIN` is a bit of a special case since AFAIK it hasn’t been used for anything terribly productive on mainnet. To be safe and less contentious, we might as well just introduce `GASPAYER` since all transactions will be paid by someone. `CALLER` is widely used and any transaction type which significantly alters the meaning of it will be certainly be met with resistance.

My intuition is that we should minimize the observability of different transaction types from within the EVM. For example, what if a transaction was introduced which paid a portion of the fees to a developer fund and to boycott it, some contracts would not allow transactions of that type? I believe all transactions should be treated equally once they enter the EVM. What use cases can you imagine if contracts can treat transactions unequally?

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Alternatively, we could assert that all transaction types must have a CALLER that represents “the address that will be considered to have called the contract”.

I think this is more than reasonable and, in fact, is already the implicit assertion made by contract developers.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> what would a 2 of 2 multisig contract set for CALLER ?

Is there a reason why it wouldn’t set `CALLER` to the address of the multisig?

---

**matt** (2020-06-17):

Also, I spent some time messing around with different RLP encodings of the typed transaction format. The envelope format was much easier to implement, so I’m happy to say I was wrong about it. For a typical transaction, the flat structure was 4 bytes shorter than the envelope structure. I didn’t get a chance finish the `lazy` transaction, but lazy decoding isn’t standard RLP anyways and [@MicahZoltu](/u/micahzoltu) pointed out earlier – it adds complexity without much savings.

I’ve posted my code [here](https://gist.github.com/lightclient/798d723c530a5938b5db9745fdfc7b5d) if anyone is interested.

---

**MicahZoltu** (2020-06-17):

After sleeping on it and reading the feedback from [@matt](/u/matt) I have removed the ORIGIN and CALLER stuff.  I added a note in the rationale saying that ORIGIN and CALLER should be the same for the first frame of the transaction for all transaction types, and that if future transaction types want to include additional data they will need a new opcode.

I am mildly convinced that allowing differentiation by transaction type may lead to some bad things like contracts not working for people who utilize certain types of transactions, but in that case I’m not sure how to best deal with sponsored transactions.  I’ll continue the discussion on that over in [EIP-2711: Separate gas payer from msg.sender](https://ethereum-magicians.org/t/eip-2711-separate-gas-payer-from-msg-sender/4353)

---

**tjayrush** (2020-06-17):

Not sure I’m knowledgable enough to comment on this EIP’s worth, but I noticed a few small issue with wording:

In the rationale section, under “Opaque second item rather than an array” section you say,

`By having the second item of the array just be opaque bytes, rather than a list, we can support different encoding formats for the transaction payload in the future, such as SSZ or a fixed-width format.`

In the backward compatibility section you say:

`...noting that the second element is a list rather than a value.`

Did you mean that the second item is bytes?

And in the Security Considerations section you say:

`...the second item as a value when it is encoded as an array`

Probably a result of the change to bytes after the initial writing of the spec.

Thought I’d point that out as it’s a bit confusing…

---

**MicahZoltu** (2020-06-18):

[@tjayrush](/u/tjayrush) Both of those were mistakes due to a change from earlier version.  Both have been fixed!

---

**AFDudley** (2020-06-24):

Sorry if I missed this in the docs, does each transaction type get its own mempool?

---

**matt** (2020-06-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/afdudley/48/1396_2.png) AFDudley:

> does each transaction type get its own mempool?

It’s not clear what you mean by “get its own mempool”. If you mean the mempool may need to maintain a list of transactions of a certain type to perform additional checks (e.g. that their total gas is less than the allow 1559 limits or that their `valid_until` block hasn’t lapsed), then I suppose the answer is yes. Whether or not these checks are performed in parallel seems like an implementation concern.

---

**MicahZoltu** (2020-06-26):

That is “out of scope” of this EIP, but for the currently on-deck 2718 transaction types, 1559 is the only one that would need its own mempool.  The rest would share one with legacy transactions.


*(55 more replies not shown)*
