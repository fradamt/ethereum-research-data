---
source: magicians
topic_id: 17232
title: "ERC-7573: Conditional-upon-Transfer-Decryption for Delivery-Versus-Payment"
author: cfries
date: "2023-12-11"
category: ERCs
tags: [dvp]
url: https://ethereum-magicians.org/t/erc-7573-conditional-upon-transfer-decryption-for-delivery-versus-payment/17232
views: 2965
likes: 19
posts_count: 26
---

# ERC-7573: Conditional-upon-Transfer-Decryption for Delivery-Versus-Payment

# ERC-7573: Conditional-upon-Transfer-Decryption - A Proposal for a Lean and Functional Delivery versus Payment

## Abstract

The interfaces model the functional transaction scheme to establish a secure delivery-versus-payment across two blockchains, where a) no intermediary is required and b) the operator of the payment chain/payment system has a small overhead and does not need to store state.

The main idea comes with two requirements: First, the payment chain operator hosts a stateless decryption service that allows decrypting messages with his secret key. Second, a “Payment Contract” is deployed on the payment chain that implements a function

```solidity
function transferAndDecrypt(uint id, address from, address to, keyEncryptedSuccess, string keyEncryptedFailure) external;
```

that processes the (trigger-based) payment and emits the decrypted key depending on the success or failure of the transaction. The respective key can then trigger an associated transaction, e.g. claiming delivery by the buyer or re-claiming the locked asset by the seller.

## Motivation

Within the domain of financial transactions and distributed ledger technology (DLT), the Hash-Linked Contract (HLC) concept has been recognized as valuable and has been thoroughly investigated.

The concept may help to solve the challenge of delivery-versus-payment (DvP), especially in cases where the asset chain and payment system (which may be a chain, too) are separated. The proposed solutions are based on an API-based interaction mechanism which bridges the communication between a so-called Asset Chain and a corresponding Payment System or require complex and problematic time-locks (\cite{BancaItalia}). We believe that an even more lightweight interaction across both systems is possible, especially when the payment system is also based on a DLT infrastructure.

## Specificaiton

### Methods

#### Smart Contract on the Asset Chain

```solidity
interface IDeliveryWithKey {
    event AssetTransferIncepted(address initiator, uint id);
    event AssetTransferConfirmed(address confirmer, uint id);
    event AssetClaimed(uint id, string key);
    event AssetReclaimed(uint id, string key);

    function inceptTransfer(uint id, int amount, address from, string keyEncryptedSeller) external;
    function confirmTransfer(uint id, int amount, address to, string keyEncryptedBuyer) external;
    function transferWithKey(uint id, string key) external;
}
```

#### Smart Contract on the Payment Chain

```solidity
interface IPaymentAndDecrypt {
    event PaymentTransferIncepted(address initiator, uint id, int amount);
    event TransferKeyRequested(uint id, string encryptedKey);
    event TransferKeyReleased(uint id, bool success, string key);

    function inceptTransfer(uint id, int amount, address from, string keyEncryptedSuccess, string keyEncryptedFailure) external;
    function transferAndDecrypt(uint id, address from, address to, keyEncryptedSuccess, string keyEncryptedFailure) external;
    function cancelAndDecrypt(uint id, address from, address to, keyEncryptedSuccess, string keyEncryptedFailure) external;
}
```

## Rationale

The rationale is described in the following sequence diagram.

### Sequence diagram of delivery versus payment

[![DvP-Seq-Diag](https://ethereum-magicians.org/uploads/default/optimized/2X/c/c4514ebe180739600e19cb136fcb307868ff3618_2_314x500.jpeg)DvP-Seq-Diag1920×3057 248 KB](https://ethereum-magicians.org/uploads/default/c4514ebe180739600e19cb136fcb307868ff3618)

## Original Concept

[A Proposal for a Lean and Functional Delivery versus Payment across two Blockchains](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4628811)

## Replies

**Mani-T** (2023-12-11):

If it indeed manages to address the challenge of delivery-versus-payment, particularly in situations where the asset chain and payment system operate as separate entities, then this would be a truly significant proposal.

---

**cfries** (2023-12-11):

[@pekola](/u/pekola) I have the following questions on the current interface specification:

- Should the parameter id be a string rather than an uint to allow for more flexible usage? Id could then be a json specifiying which decryption orcale to use, etc.
- Some function have redundant specification of “to/from” as these fields have already been specified when initiating with id. Should we require to have these redundant parameters specified?

---

**pekola** (2023-12-12):

Hello [@cfries](/u/cfries) - I would rather suggest a first weak linkage to ERC-6123.

We could extend the IDeliveryWithKey by the functions inceptTrade, cofirmTrade in which the trading parties agree on the trade terms. Based on the transactionSpecs which are agreed a hash gets generated. This will be used in the function pattern vor DvP. Therefore “id” is fine (transactionSpecs = tradedata, paymentamount, etc. are agreed before).

---

**cfries** (2023-12-13):

So id is generated by another function call (that is not part of the interface)? Otherwise they have to ensure that they do not use an existing id. Is it is required that id is identical on both chains, right?

---

**pekola** (2023-12-13):

Yes - I would prefer: Trading Parties agree on terms (incept/confirm), for those terms a unique id is generated which gets processed via DvP-Pattern. Asset Contract keeps track on the states within Dvp-Process. Gonna be a nice design.

---

**cfries** (2023-12-15):

OK. But the point of making id a `string` instead of an `int` maybe remains. I believe an `int` is too narrow. The id could by a UUID.

---

**moinlars** (2024-06-19):

Really interesting proposal ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) The idea that both buyer and seller don’t need to store the secret (as compared to a HTLC protocol for example) seems to be a valuable feature.

I’ve got some questions:

I was wondering if all calls are really necessary. Given that buyer and seller agree on a trade by exchanging E(B) and E(S). Wouldn’t it be enough for the seller to upload E(B) and E(S) to the asset contract (and locking the asset tokens) and for the buyer to store E(B) and E(S) to the payment contract once the buyer has observed that the tokens have been locked in the asset contract? If the buyer fails to call the payment contract with E(B) and E(S), the payment contract could allow to cancel the trade if and only if the combination of E(B) and E(S) is not present.

The functions `transferAndDecrypt` and `cancelAndDecrypt` require E(B) and E(S) as parameters. However, they should already be stored inside the smart contract using the ID as a reference. What’s the reason for providing them again? The diagram shows that `to` is also needed. But that also could be referenced using the ID. Same applies to `from` and `to` as mentioned in the interface.

---

**moinlars** (2024-06-20):

I think it could be as easy as the following:

1. Buyer creates E(S) and seller creates E(B) after agreeing on a trade and they exchange the encrypted documents
2. Buyer calls inceptTransfer on the payment contract with E(S) and E(B)
3. Seller observes that the transfer on the payment contract has been incepted correctly and calls inceptTransfer on the asset contract also using E(B) and E(S)
4. Success case: Buyer observes that the transfer on the asset contract has been incepted correctly and calls transferAndDecrypt on the payment contract. Failure case: If the buyer fails to call transferAndDecrypt on the payment contract, the seller can call cancelAndDecrypt on the payment contract.
5. Upon the revealing of S or B by the payment operator, buyer or seller call transferWithKey on the asset contract.

Upsides:

- This would reduce smart contract calls and thus gas costs for the participants
- I think it’s easier to understand because the buyer who holds cash on the payment chain mainly operates the payment contract and the seller who holds the asset on the asset chain mainly operates the asset contract

Am I missing something?

---

**ivica** (2024-06-20):

I like this proposal too. It is useful for the cases where no entity with trusted entity is in place to manage the trigger and cancellation keys off-chain. In the case of Bank of Italy implementation in the context of ECB exploratory work, I would argue that if you trust Eurosystem to manage the RTGS accounts, then you can also put the trust into managing the trigger and cancellation keys. However, not in all situations you can have someone like a central bank offering the service and in this cases I believe this proposal might be useful.

At the first glance, as a fan of symmetry, I am asking myself why you introduced two different interfaces? Isn’t it possible to unify in the sense that it doesn’t make a difference which side initiates the transfer? Also with payments, in the and it is asset vs asset, so why differentiation between asset chain and payment chain?

Moreover, could we avoid encrypt/decrypt and work with hashes only? Could be more resource-efficient?

---

**moinlars** (2024-06-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivica/48/12670_2.png) ivica:

> At the first glance, as a fan of symmetry, I am asking myself why you introduced two different interfaces? Isn’t it possible to unify in the sense that it doesn’t make a difference which side initiates the transfer? Also with payments, in the and it is asset vs asset, so why differentiation between asset chain and payment chain?

[@ivica](/u/ivica) I agree, it doesn’t matter if the centrally managed side contains the cash asset or some other asset - comparable to the HTLC protocol.

However, from my understanding (as with HTLC) the order of transactions matters. Also, there is really just a single contract “that matters”. That is the hash link contract on the asset chain. The payment contract is just an interoperability mechanism between the payment operator and the participants of the trade used for retrieving the decrypted secrets.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivica/48/12670_2.png) ivica:

> Moreover, could we avoid encrypt/decrypt and work with hashes only? Could be more resource-efficient?

The encryption of the pre image is necessary so that it remains private to the respective other party, if we assume that the we use a public ledger for the payment contract.

---

**cfries** (2024-06-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/moinlars/48/10847_2.png) moinlars:

> ivica:
>
>
> Moreover, could we avoid encrypt/decrypt and work with hashes only? Could be more resource-efficient?

The encryption of the pre image is necessary so that it remains private to the respective other party, if we assume that the we use a public ledger for the payment contract.

One can replace the on-chain encrypted key with a hash and avoid on-chain encryption. This reduces computational complexity on chain. It is described in our paper: You replace the encrypted key E(K) with a hash H(K) of the decrypted key K. However, this requires that the decryption-oracle provides an additional stateless function that maps E(K) to H(K) without exposing K. The decryption oracle can do this via E(K) → K → H(K). This function could be provided off-chain and it is still stateless.

- Advantage: just a hashing on-chain.
- Disadvantage: additional (but still stateless) API required.

---

**ivica** (2024-06-20):

[@cfries](/u/cfries) what’s also not clear to me yet: are Asset Contract and Payment Contract on the same DLT or on two different DLTs? As far as I understand the seq. diagram, the Payment Operator would need to call the smart contract (blockchain transaction), right?

If there is a separate ledger that Payment Operator is providing, then compared to BdI HLC solution it would be shifting the key storage to DLT instead of having it in the Payment System (so basically the complexity is not removed, but just shifted). If it would be on the same ledger, then the PaymentOperator would have to go into dependency with potentially many market DLTs, which introduces additional integration efforts (additional complexity).

---

**pekola** (2024-07-02):

Hi - Each of the two contracts reside on a separate blockchain - using just one DLT this pattern is not needed. According to the sequence diagram the “payment operator” has two roles:

1. To decrypt an encrypted secret (independent of known the transaction details)
2. To store the decrypted secret in the Payment Contract “releaseKey”

The PaymentOperator does not need to provide an own Blockchain.  He does not even has anything to do with the DLT on whicht the PaymentContract is deployed.

As depicted in the Diagram the PaymentContract is processing the payment on its own (could be directly onchain as depicted or by using an offchain-payment-adapter).

The “PaymentOperator” just serves as a transaction-agnostic “Decryption oracle”. And the nice thing about storing decrypted keys on the payment chain is that, the PaymentOperator does not need to store or hold anything offchain. The functionality he provides is completely stateless.

But to make this even more clear - we could rename the PaymentOperator a bit more general to “DecryptionOracle” to see that it is completely independent regarding the Payment Transaction itself.

With the result that this protocol requires a very minimalistic oracle service functionality - which we found very charming ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**cfries** (2024-07-02):

Maybe I like to add here that we changed the names of the contract in the updated version of the paper. The earliest version of the paper was talking about Asset and Payment, but the contracts are `LockingContract` (the contract that locks a token on chain A) and `DecryptionContract` (the contract that decrypts the key required for unlocking upon a successful transfer on chain B). The asymmetry is somewhat natural since it is just two steps. Note that a locking on the second chain is not required.

See [ERC-7573: Conditional-upon-Transfer-Decryption for DvP](https://eips.ethereum.org/EIPS/eip-7573#specification)

The words “asset” and “payment” are just illustrative. The two tokens should stand for anything (XvY = DvP, PvD, PvP, DvD).

---

**moinlars** (2024-12-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cfries/48/8032_2.png) cfries:

> It is described in our paper: You replace the encrypted key E(K) with a hash H(K) of the decrypted key K.

Okay, yes. We can avoid the encryption / decryption operation on chain, but we still need it off-chain.

---

**Julius278** (2025-01-16):

Hi all,

whats not quite clear to me is the DecryptionOracle - verify - Part.

How does the Oracle get to know the address of the DecryptionContract?

Is the Oracle stateful and stores all deployed DecryptionContracts (probably by intercepting TransferIncepted event)?

And what if I accidentally (or on purpose) deploy and incept two separate DecryptionContracts with the same E(S) and E(B)? In a test you may choose the same key twice.

Maybe generate the “id” within the contracts constructor and add the “id” to the oracles verify request?

Best regards,

Julius

---

**cfries** (2025-01-20):

Hi Julius.

This is a good question. We added a more lengthy description of the interaction between the contract and the oracle in the white paper at https://ssrn.com/abstract=4628811

The oracle should be 100 % stateless (except for owning a private key for descryption and (if necessary) the chain it is being “attached”.

There we propose an XML schema for the key K ( K = S | B ). The key should contain the address of the contract as well as some random part ensuring uniqueness.

When the oracle get the verify(E(K)) message it decrypts the E(K) to a K and returns the address of the contract, but not the K itself. Thus the counterparties can verify that the keys are associated with the right contract.

When the oracle gets the decrypt(EK)) message (called or observed) it decrypts the E(K) to a K, checks that the adress of the contract that called or emitted the message agrees with the address in the K and then (and only then) calls back that specific contract.

This ensures that b) a given key cannot be decrypted though other contracts, and, a) that the two counterparties can verify that the key will be decrypted by the appropriate payment contract.

Does this make sense?

Best

Christian

---

**Julius278** (2025-01-23):

Hey Christian,

okay, sounds good.

So the whole XML is the key and will be encrypted containing a secret, some unique stuff and the DecryptionContract?

And I guess the oracles verify endpoint should be extended by the hashedKey:

verify( E(K), H(K) ) returns DecryptionContract address

Cause the easiest way of encryption in Solidity is hashing, you could store the hashedKey ( H(K) ) in the contract and when K is used to release the locked asset, it is hashed on chain and checked against the already stored hashedKey.

In this case, the oracle could verify that the hash ( H(K) ) is correct which is needed to release funds and returns the DecryptionContract address.

Best regards

Julius

---

**Julius278** (2025-02-20):

Hey all,

In this discussion the initial interfaces use uint type for transfer id.

The interfaces in the ERC repo currently use bytes32. It’s probably cause - as Peter in December 2023 said - a generated unique id should be used and the easiest way in Solidity is probably a hash (keccak256) which produces a bytes32.

But that one can be easily transformed into a uint256.

It’s also more readable from an end users perspective for frontends. (Conversion off chain also shouldn’t be a problem but I would prefer to see the exact value that is used for the transaction.)

Best regards

Julius

---

**Julius278** (2025-02-21):

Oh and to somehow couple ERC-7573 and ERC-6123, it would also be easier to use int256 as transactionID type cause the ISDC.afterTransfer also uses uint256 as its transactionID so you could take advantage of this pattern.


*(5 more replies not shown)*
