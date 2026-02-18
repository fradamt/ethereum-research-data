---
source: magicians
topic_id: 4353
title: "EIP-2711: Separate gas payer from msg.sender"
author: MicahZoltu
date: "2020-06-11"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-2711-separate-gas-payer-from-msg-sender/4353
views: 7175
likes: 14
posts_count: 53
---

# EIP-2711: Separate gas payer from msg.sender

https://eips.ethereum.org/EIPS/eip-2711

## Simple Summary

Allow for a second transaction signer who pays for gas, which is separate from the transaction signer who represents the `msg.sender` of the transaction.

## Replies

**MicahZoltu** (2020-06-11):

The link is broken until EIP editors merge the draft PR.  In the meantime, you can see the draft PR at https://github.com/ethereum/EIPs/pull/2711/files?short_path=d153253#diff-d1532538998fb37b8d96e11a10e4ffd0

---

**juanfranblanco** (2020-06-11):

What is the suggested order of signers and what do they sign? Will the sender sign the rlp message as per now, excluding the gas elements and the gas payer sign the rlp of that message including the r,s,v? I guess if the nonce provider could be similar?

---

**Amxx** (2020-06-11):

the sender could sign the transaction, just like now, and the provider, if he accepts the gas parameters included by the sender, would sign the entier sender tx (including r,s,v)

That way provider doesn’t have to add anything more, and is already replay protected by the sender’s replay protection

EDIT: I think this is better then having the provider give the gas details (in particular gas limit). Otherwize, a provider could purpousfully put a very low max gas (21000 when the transaction needs much more) have the transaction revert, lose the gas but make the sender’s nonce increase.

Having the sender nonce increase that way can deny deploying a contract to a particular address… which can have bad consequences. It should be to the signer to determine how much gas he needs, and the provider accepts (or not) by signing.

EDIT2: just realized that this is dangerous, because removing the last signature would make the transaction being paid by the sender (bypass the relayer). The sender ends up paying for its transaction, which is not a major security risk, but is an issue nontheless

---

**juanfranblanco** (2020-06-11):

I think the sender (signer) should provide the amount gas required for the transaction, the gas payer can estimate the gas and validate that it matches the requirements for the transaction, and provide the gas. If the txn fails the sender will be charged anyway or if it needs to be replayed with a higher price, that will be something for both the gas payer and sender to agree. That might require some other type of messaging between both parties and / or smart contract.

---

**matt** (2020-06-11):

This is an EIP I’m excited about and I believe it is long overdue. Here are a few thoughts I currently have:

- I’m not sure I follow the reasoning behind an explicit ChainID element in the transaction. It is already encoded in the v element, so it seems like redundant information.
- By not having the signer sign the gas_price and gas_limit, it protects them from having their tx inadvertently included on-chain w/o a sponsor. The thing to be careful of here is avoiding relay systems where a relayer can set the gas_price arbitrarily high and then recover the cost from the signer. So that will necessitate more calldata to authorize a certain amount of gas at a particular price.
- In terms of nonces, it might be helpful to also add that having two nonce would increase validation overhead in the tx pool more than just having the signer’s nonce.
- It could be worth giving a nod to some proposals that would provide atomicity for relayer payments as I believe they are complementary to this EIP
- I want to throw in the hat “Sponsored Transactions” as the name for this new type of tx before meta-tx folks claim it as “Native Core Protocol Meta-Transaction™”.

---

**MicahZoltu** (2020-06-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> I’m not sure I follow the reasoning behind an explicit ChainID element in the transaction. It is already encoded in the v element, so it seems like redundant information.

Hmm, good point.  I have never been a fan of bit packing `v`, but as it stands you are right.  That means we’ll need to be a bit more specific on what is signed unfortunately.  I’ll update with that tomorrow.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> a relayer can set the gas_price arbitrarily high and then recover the cost from the signer

It is up to the sender and relayer to negotiate an appropriate fee.  Personally, I wouldn’t recommend `gasPrice * gasLimit * exchangeRate` in tokens for the exact reason you mentioned.  They can do this negotiation via calldata as you suggested which is probably reasonable.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> In terms of nonces, it might be helpful to also add that having two nonce would increase validation overhead in the tx pool more than just having the signer’s nonce.

I added some more text about the nonces a bit ago, do you think I should add more or is what is now there good?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> It could be worth giving a nod to some proposals that would provide atomicity for relayer payments as I believe they are complementary to this EIP

I’m not a fan of standards including a bunch of history and fluff.  I prefer the standard (EIP) to be written so that someone reading it 3 years from now can easily implement it and isn’t bogged down by a bunch of “the road that got us here”.  That being said, the rationale section may get value from including specific things that were *not done* if it is not intuitive why they weren’t chosen.  Do you have specific things you can think of that should be mentioned in the rationale?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> I want to throw in the hat “Sponsored Transactions” as the name for this new type of tx before meta-tx folks claim it as “Native Core Protocol Meta-Transaction™”.

Fine with me, though I’m not sure if/where that would fit into the EIP (technical standard)?  I’m fine with using that term in conversation at the least.

---

**Amxx** (2020-06-11):

Proposition:

- Keep the “internal” transaction similar to the current ones. They include gasLimit, gasPrice and signeture by the “signer” (msg.sender). This can be submitted and mined like currently
- Wrap them by adding an overloaded gasPrice and the signature of the “relayer”.

The relayer, if he has an insentive to do so, can wrap the transaction. If the signer doesn’t want to pay the gas, just set the gasPrice of the inner transaction to 0

→ the inner transaction can be mined for free (not likelly, but why not ?)

→ the relayer can add gas to have the transaction mined

If the transaction involves a repaying mechanism onchain, the repaying mechanism should protect the signer by considering a “maxgas” … just like current meta-tx repayement schemes.

Question is, how would that fit with EIP1559

---

**Amxx** (2020-06-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> I want to throw in the hat “Sponsored Transactions” as the name for this new type of tx before meta-tx folks claim it as “Native Core Protocol Meta-Transaction™”.

whether you like it or not, this EIP proposes something that is very similar to meta-tx, and which has already been proposed in all core devs by the “meta-transaction folks”. I dobt starting this kind of crusade right here, right now, is a smart move. If I had to chose I would trade in a name I don’t like for support that would bet this EIP into a hard fork / network upgrade.

---

**matt** (2020-06-11):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I added some more text about the nonces a bit ago, do you think I should add more or is what is now there good?

I’m looking at [this](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-2711.md) as the most updated link, let me know if this is wrong. Under the nonce rationale you’ve listed payload size and deadlock as the problems with requiring a sponsor’s nonce, but I feel like increased cost of validation is biggest concern. I’m not sure if you intended it that to fall under deadlock, but I think it is slightly different and worth mentioning.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> That being said, the rationale section may get value from including specific things that were not done if it is not intuitive why they weren’t chosen. Do you have specific things you can think of that should be mentioned in the rationale?

I agree with you, we should avoid giving a history lesson within the EIP. However, I believe that it is worth mentioning that this EIP by itself does not solve the relayer payment problem. For that we really need something like [rich transactions](https://github.com/Arachnid/EIPs/blob/f6a2640f48026fc06b485dc6eaf04074a7927aef/EIPS/EIP-draft-rich-transactions.md) or [batched transactions](https://ethereum-magicians.org/t/eip-native-batched-transactions/4337). I wrote about this need more [here](https://ethresear.ch/t/native-meta-transaction-proposal-roundup/7525).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> Proposition:
>
>
> Keep the “internal” transaction similar to the current ones. They include gasLimit, gasPrice and signeture by the “signer” (msg.sender). This can be submitted and mined like currently
> Wrap them by adding an overloaded gasPrice and the signature of the “relayer”.

What do you see as the advantage of this method? At first I was thinking maybe we don’t need to change the tx structure, but if you don’t and introduce some sort of precompile for the relayer to send to then you’re going to link together the signer and sponsor’s nonce - which I think is a problem.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> If I had to chose I would trade in a name I don’t like for support that would bet this EIP into a hard fork / network upgrade.

I agree, I don’t want to get hung up on a name it means no support. However, I think being precise in naming is valuable - especially in a technical field. The people I’ve spoken to 1:1 regarding this find it is a more suitable name and appreciate that it is not overloaded with other meanings. Sponsored transactions clearly explain what this EIP is proposing. There is nothing “meta” about the transaction format here, everything is explicit and defined in the protocol.  For those reasons, I think it is an appropriate title for this EIP.

---

**Amxx** (2020-06-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> What do you see as the advantage of this method? At first I was thinking maybe we don’t need to change the tx structure, but if you don’t and introduce some sort of precompile for the relayer to send to then you’re going to link together the signer and sponsor’s nonce - which I think is a problem.

I might be wrong, but I imagine that enhancing transaction but appending additional data is preferable to reworking the structure (just like EIP155 does) as it simplifies the client implementation: “is there additional data ? keep the tx I’ve built and just add some check/update with whatever is left”

I really don’t see the point of having a relayer nonce.

→ The internal tx is protected against replay, so the signature for the sponsored transaction (and thus the sponsored transaction) also is.

→ You can sponsor many transaction by many signers without introducing strong ordering between them (better for at scale relaying).

→ If some transaction is sponsored by many people, if one of the version is mined, the other are automatically invalid, and relayer don’t have to support “out of sync” nounces.

Do you see any situation where a relayer nounce would be handy ?

---

**matt** (2020-06-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> I really don’t see the point of having a relayer nonce.

Sorry, I misread your post and thought that by wrapped tx you meant also wrapping with the sponsor’s nonce. But I realize now that you said only the overloaded `gas_price` and additional signature would be included.

In that case, I agree with you that appending data is probably preferable to reworking the structure. That seems like the advantage here. However, I’m not sure how much this actually matters in practice. Also, I don’t think the signer is has any more protected. Having a `gas_limit` is not helpful unless `gas_price` is bounded as well.

---

**Amxx** (2020-06-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> Having a gas_limit is not helpful unless gas_price is bounded as well.

I have to disagrea on that. gaslimit is not just about cost, it’s about controlling the execution context, which the signer should define.

A simple example: given its address, and its current nonce, the signer knows what we will the address of the contract he will deploy. This can be helpfull, particularly to recover funds that where send to a contract deployed on another network (I can find you references where that really happens).

Now the signer wants to deploy a contract, so I sign the transaction with the data, and asks for relaying. If the relayer is able to set the gas limit, he can attack by putting a low value (21000), a high gas price, having his transaction mined, reverted because gaslimit is to low.

Boom, he lost some gas but he also increased the signer nounce, preventing from deploying a contract to this address forever.

Also, if a signer wants to send multiple transaction with sequential nonce, and if a relayer uses the same trick to have the first tx revert, the subsequent transaction might have unexpected, potentially dangerous, behaviour.

Again, it’s the signer who is doing the action, so he is the one knowing how much gas is needed, and he is the one whose account is affected if the gas limit is reached. relayer have many way of protecting themselves (either through off chain repaying agreements or using repaying contracts with try/catch protection)

---

**pipermerriam** (2020-06-11):

I’m of the opinion that `gas_limit` and `gas_price` should both be under the control of the *sender*.

For `gas_limit`, the transaction sender is the one with the most context about how much gas the transaction needs to execute.  Roughly the same logic can be applied to `gas_price`.

For `gas_price`, having it settable by the *gas-payer* probably makes this un-usable for meta transactions since the it would allow the *gas-payer* to use unreasonably high gas prices with no consequence in cases where the transaction repays the *gas-payer*.

From the *gas-payer* perspective, if the signer uses either a `gas_limit` or a `gas_price` that they are not comfortable with, they have the choice to simply not sign the transaction.  If these values are left under the control of the *gas-payer* then the sender must sign a transaction without being able to have full knowledge about what they are signing.  And since this is a protocol level thing, I don’t think that we can assume that the sender and relayer will be able to *negotiate* in all situations.

---

**Amxx** (2020-06-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pipermerriam/48/65_2.png) pipermerriam:

> For gas_price , having it settable by the gas-payer probably makes this un-usable for meta transactions since the it would allow the gas-payer to use unreasonably high gas prices with no consequence in cases where the transaction repays the gas-payer .

current meta transaction already have a fix for that. They repay `gasUsed * min(gasPrice, maxGasPrice)` where maxGasPrice is provided by the sender to the repaying contract

---

**pipermerriam** (2020-06-11):

Regarding nonces:

The nonce in eth1.x gives us some DOS protection, ensuring that we can invalidate transactions with too high or low a nonce.  I believe that multiple nonces do not provide any additional value, and in-fact, make transaction validation more complex and expensive.

Assuming there is no argument with the above, then we only need one nonce.  Our choices seem to be:

1. sender nonce
2. gas-payer nonce
3. some-other nonce

Option 3 of having some other nonce that is not the sender or gas payer does not seem to makes sense.

Option 2 of **only** having the gas-payer nonce looks problematic.  One use case is signing multiple transaction with increasing nonce values which are guaranteed to be executed in nonce order.  Using gas-payer nonce would remove the ability of the sender to do this since they would be subject to the gas-payer potentially re-ordering their transactions.

Which leaves Option 1: Just include a single nonce, from the *sender* account.

---

**pipermerriam** (2020-06-11):

Interesting.  So the issue of *griefing* via using arbitrarily high gas prices is easily addressed for the meta-transaction use case at the EVM level.

I’m still concerned about this value being outside of the control of the sender.  In the extreme case, the sender has no relationship with the gas payer.  IIRC the status token sale set limits on the gas prices allowed for transactions which purchased tokens.  I’m not advocating for this design pattern, but such a situation would allow the relayer to cause the sender’s transaction to fail in a way that was outside of the control of the sender.

I’m curious to hear what the argument is for the gas-payer needing to be in control of gas price.  Since they have the discretion to sign or not-sign transactions, it seems to make the most sense to leave it in the hands of the sender, and assume that in cases where the gas-payer is sensitive to the exact gas price, then this would need to be handled outside of the protocol.

For example, if the sender trusts gas payer but needs protection against volitile gas prices, the sender can sign multiple messages with different gas prices and the relayer chooses the appropriate one to sign and send.

---

**MicahZoltu** (2020-06-12):

I imagine the `SENDER` as “the party that defines what they want to do” and the `GAS_PAYER` as “the party who gets the transaction included on-chain”.  This separation of concerns is what drove me to put both gasLimit and gasPrice into the `GAS_PAYER`'s control rather than the `SENDER`'s control.

I am imagining `GAS_PAYER` being used for far more than just the traditional meta-transactions of today.  One example would be a private relayer where one member of a business (say, an accountant or someone wanting to make a purchase) may submit a transaction to their company’s Transaction Submission Department (TSD) and the TSD would deal with all of the complexity of ensuring inclusion.  The person who signed the transaction indicating what they wanted to do doesn’t have the tools/knowledge to properly do gas estimates, gas pricing, replace by fee, escalation, etc.  They just know that they want to send 10 ETH to address X or call contract method Y on contract Z.

The fact that someone can maliciously bump the `SENDER` nonce is certainly something worth considering, and *may* be enough to convince me to move the `gasLimit` back to the `SENDER`'s control.  I’m pretty firm at the moment on `gasPrice` being controlled by the `GAS_PAYER` though as pricing may be done at a different time than `SENDER` signing.  Again, using the company example above, the `SENDER` may sign the transaction and then it goes through some test suite, is then verified by several different humans, before finally being handed off to the TSD (`GAS_PAYER`) who picks a reasonable `gasPrice` at that time.

**TL;DR**: I think the traditional untrusted-meta-transaction problem *can* be solved with `gasPrice` under `GAS_PAYER` control at layer 2, and by having `gasPrice` under `GAS_PAYER` control I think creates opportunities for other uses of this type of transaction.

---

**MicahZoltu** (2020-06-12):

I have moved `gasLimit` into `SENDER` control.  Compelling argument to me came from [@Amxx](/u/amxx) in  [EIP-2711: Separate gas payer from msg.sender](https://ethereum-magicians.org/t/eip-2711-separate-gas-payer-from-msg-sender/4353/13)

---

**MicahZoltu** (2020-06-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> I might be wrong, but I imagine that enhancing transaction but appending additional data is preferable to reworking the structure (just like EIP155 does) as it simplifies the client implementation: “is there additional data ? keep the tx I’ve built and just add some check/update with whatever is left”

I think the “right” thing to do would be to create a new transaction payload type, perhaps with a sentinel value up front to make it easily identifiable, that supports versioning of the transaction and adding transaction types over time.  For example, we could do `rlp([TransactionType, [...]])` where `TransactionType` is a number identifying the type of transaction that is included and the `[...]` is the actual signed transaction.  Need to think more on whether such a transaction can lead to conflicts with existing transactions or if it is possible to uniquely identify them easily or not, but that would let us add new transaction types without having to do bit packing like EIP-155 did, or having to worry about “how do I tell what type of transaction it is” as this one is going to end up doing.

I *think* the above is generally safe because the 2nd item in the tuple is a list, which is RLP encoded different from other things.  Also, we could say that the high bit of the `TransactionType` is always set to 1, which will never be a valid nonce for legacy transactions to make it even easier to identify legacy transactions early on.

---

**epheph** (2020-06-12):

Should an EIP-2711 transaction cost more than the standard base transaction cost of 21000? The raw TX will is larger, more signature verification, and more nonce/account state updates.

It seems tx.origin would be the “sender” and not the “gasPayer” ? Will there be an opcode for gasPayer address?


*(32 more replies not shown)*
