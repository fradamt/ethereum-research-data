---
source: magicians
topic_id: 19826
title: "ERC-7699: ERC20 Transfer reference extension"
author: radek
date: "2024-04-26"
category: ERCs
tags: [erc, erc-20, erc20]
url: https://ethereum-magicians.org/t/erc-7699-erc20-transfer-reference-extension/19826
views: 1499
likes: 9
posts_count: 19
---

# ERC-7699: ERC20 Transfer reference extension

ERC:

- ERCs/ERCS/erc-7699.md at master · ethereum/ERCs · GitHub
- ERC-7699: ERC-20 Transfer Reference Extension

ERC pull request: [Add ERC: ERC-20 Transfer Reference Extension by radeksvarz · Pull Request #399 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/399/files)

> Beware, some details below were amended based on the further discussion. See the latest pull request and merged file.

A minimal standard interface for ERC20 tokens allowing users to include a unique identifier (payment reference) for each transaction to help distinguish and associate payments with orders and invoices.

Requires: EIP-20, EIP-165

# Abstract

The ERC20 token standard has become the most widely used token standard on the Ethereum network. However, it does not provide a built-in mechanism for including a payment reference (message) in token transfers. This proposal extends the existing ERC20 token standard by adding minimal methods to include a payment reference in token transfers and transferFrom operations. The addition of a payment reference can help users, merchants, and service providers to associate and reconcile individual transactions with specific orders or invoices.

# Motivation

The primary motivation for this proposal is to improve the functionality of the ERC20 token standard by providing a mechanism for including a payment reference in token transfers, similar to the traditional finance systems where payment references are commonly used to associate and reconcile transactions with specific orders, invoices or other financial records.

Currently, users and merchants who want to include a payment reference in their transactions must rely on off chain external systems or custom payment proxy implementations. In traditional finance systems, payment references are often included in wire transfers and other types of electronic payments, making it easy for users and merchants to manage and reconcile their transactions.

By extending the existing ERC20 token standard with payment reference capabilities, this proposal will help bridge the gap between traditional finance systems and the world of decentralized finance, providing a more seamless experience for users, merchants, and service providers alike.

# Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

Any contract complying with EIP-20 when extended with this ERC, MUST implement the following interface:

```auto
// The EIP-165 identifier of this interface is 0xxxxxxx - to be updated once ERC number is assigned

interface IERCXXXX {

function transfer(address to, uint256 amount, bytes calldata paymentReference) external returns (bool);

function transferFrom(address from, address to, uint256 amount, bytes calldata paymentReference) external returns (bool);

event Transfer(address indexed from, address indexed to, uint256 amount, bytes indexed paymentReference);

}
```

These `transfer` and `transferFrom` functions MUST emit `Transfer` event with paymentReference parameter.

`paymentReference` parameter MAY be empty - example: `emit Transfer(From, To, amount, "");`

`paymentReference` parameter is not limited in length by design, users are motivated to keep it short by calldata and log data gas costs.

Transfers of 0 amount MUST be treated as normal transfers and fire the `Transfer` event.

# Rationale

## Parameter name

The choice to name the added parameter paymentReference was made to align with traditional banking terminology, where payment references are widely used to associate and reconcile transactions with specific orders, invoices or other financial records.

The paymentReference parameter name also helps to clearly communicate the purpose of the parameter and its role in facilitating the association and reconciliation of transactions. By adopting terminology that is well-established in the financial industry, the proposal aims to foster a greater understanding and adoption of the extended ERC20 token standard.

# Backwards Compatibility

This extension is fully backwards compatible with the existing ERC20 token standard. The new functions can be used alongside the existing transfer and transferFrom functions. Existing upgradable ERC20 tokens can be upgraded to include the new functionality without impact on the storage layout; new ERC20 tokens can choose to implement the payment reference features based on their specific needs.

ERC20 requires its `Transfer(address indexed _from, address indexed _to, uint256 _value) ` event to be emitted during transfers, thus there will be duplicitous data logged (from, to, amount) in two events.

# Security Considerations

Payment reference privacy: Including payment references in token transfers may expose sensitive information about the transaction or the parties involved. Implementers and users SHOULD carefully consider the privacy implications and ensure that payment references do not reveal sensitive information. To mitigate this risk, implementers can consider using encryption or other privacy-enhancing techniques to protect payment reference data.

Manipulation of payment references: Malicious actors might attempt to manipulate payment references to mislead users, merchants, or service providers. This can lead to:

1. Legal risks: The beneficiary may face legal and compliance risks if the attacker uses illicit funds, potentially impersonating or flagging the beneficiary of involvement in money laundering or other illicit activities.
2. Disputes and refunds: The user might discover they didn’t make the payment, request a refund or raise a dispute, causing additional administrative work for the beneficiary.

To mitigate this risk, implementers can consider using methods to identify proper sender and to generate unique and verifiable related payment references.

## Replies

**radek** (2024-04-27):

This ERC was discussed during the BeerFi Prague chaindev meetup. There were 2 points for consideration:

A. paymentReference type - initially bytes32 was considered in order to motivate users to either use short references (as is common in TradFi) or rather use Keccak 256 hash of the reference content. Conclusion was that we should rather keep the options open as one use case examples could be to pass a signed reference, where the token contract checks the signature and potentially refuses the transfer if invalid.

B. The emitted Transfer event contains both - the reference data and also the from, to, amount data. That is duplicate to ERC-20 Transfer event. In fact 2 events are fired:

B1)

1. ERC7699.Transfer(from, to, amount, paymentReference)
2. ERC20.Transfer(form, to, amount)

There could be the option to rather emit:

B2)

1. ERC7699.PaymentReference(paymentReference)
2. ERC20.Transfer(form, to, amount)

However for that case the offchain indexing / wallets / BackEnds would need to listen to and aggregate information from both events.

We would like to have the sound discussion on this.

---

**radek** (2024-05-01):

The 3rd option was mentioned:

B3)

ERC7699.Transfer(from, to, amount, paymentReference) MUST be emitted also in the case the ERC20.transfer(to, amount) op is done. In that case paymentReference is to be emitted empty ( “” ).

By that the indexers, wallets, etc. can rely solely on this event for contracts compliant with this ERC.

---

**ashhanai** (2024-05-15):

In the paymentReference type discussion (A), you mention that a receiver can refuse the transfer based on the reference. That is a very nice use case, but you would have to define a set of callbacks where the receiver would be able to perform such checks similarly to [ERC-1363](https://eips.ethereum.org/EIPS/eip-1363). Extending this ERC with them and supporting the mentioned use case is a good idea.

I wouldn’t necessarily make it mandatory and check if a contract receiver implements it, like in the “safe” transfers in other token standards, but rather keep it optional. By doing that, tokens implementing this ERC would be backward compatible with existing protocols and, at the same time, give projects that rely on the `paymentReference` the option to perform the checks.

Unlike other token standards, this ERC also emits the `paymentReference` in its events. I like option 3, where even ERC-20 transfer functions would emit ERC-7699 events so that indexers interested in reference could rely only on those events. In the same way, ERC-20 transfer functions will call the callbacks if the receiver implements it.

Even though I understand why you named the value `paymentReference`, I think it’s not a good idea to mix another term for transfer. Rather, be consistent with the rest of the token standards and use `data`, or keep it simple and use `reference` or `transferReference` if you need to be explicit.

---

**radek** (2024-05-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ashhanai/48/5885_2.png) ashhanai:

> In the paymentReference type discussion (A), you mention that a receiver can refuse the transfer based on the reference. That is a very nice use case, but you would have to define a set of callbacks where the receiver would be able to perform such checks similarly to ERC-1363. Extending this ERC with them and supporting the mentioned use case is a good idea.
>
>
> I wouldn’t necessarily make it mandatory and check if a contract receiver implements it, like in the “safe” transfers in other token standards, but rather keep it optional. By doing that, tokens implementing this ERC would be backward compatible with existing protocols and, at the same time, give projects that rely on the paymentReference the option to perform the checks.

This was mentioned as the example use case for the potential extension by either the extra implementation of the transfer function as a general mechanism (no callbacks needed), or by extra callbacks.

Such extensions are NOT in scope of this ERC as I assume there are many other cases how to use payment reference within tx call.

---

**radek** (2024-05-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ashhanai/48/5885_2.png) ashhanai:

> Unlike other token standards, this ERC also emits the paymentReference in its events. I like option 3, where even ERC-20 transfer functions would emit ERC-7699 events so that indexers interested in reference could rely only on those events.

I have the same opinion, and would like to see the feedback from indexers on this.

---

**radek** (2024-05-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ashhanai/48/5885_2.png) ashhanai:

> Even though I understand why you named the value paymentReference, I think it’s not a good idea to mix another term for transfer. Rather, be consistent with the rest of the token standards and use data, or keep it simple and use reference or transferReference if you need to be explicit.

Good point to align on the consistent naming.

With reference to standards:

- SWIFT: field 70 “Remittance Information” is commonly used for such content (e.g " PAYMENT FOR INVOICE 998877"). There is also field 72 “Sender to receiver information”. MT103 - Wikipedia
- ISO 20022 (for SEPA): PAIN.001 has field called RmtInf (Remittance Information)
- Ethereum ETH xfer: ‘data’ field - Metamask labels that Hex data and one must change settings to use that (not available for ERC20 transfers): How to add a memo to a transaction | MetaMask Help Center 🦊♥️

I am not in favor of calling the parameter `data` as `data` is commonly used for execution instructions content and not a reference (descriptive) content.

---

**radek** (2024-05-24):

[@ashhanai](/u/ashhanai) I get your point now - key objection is to use word “payment”.

I agree that to use transfer reference is more consistent and shorter:

`ERC-7699: ERC20 Transfer reference extension`

```auto
function transfer(address to, uint256 amount, bytes calldata reference) external returns (bool);

function transferFrom(address from, address to, uint256 amount, bytes calldata reference) external returns (bool);

event Transfer(address indexed from, address indexed to, uint256 amount, bytes indexed reference);
```

I will update the ERC, if there is no objection to this.

---

**radek** (2024-09-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/radek/48/16714_2.png) radek:

> B. The emitted Transfer event contains both - the reference data and also the from, to, amount data. That is duplicate to ERC-20 Transfer event. In fact 2 events are fired:
>
>
> B1)
>
>
> ERC7699.Transfer(from, to, amount, paymentReference)
> ERC20.Transfer(form, to, amount)
>
>
> There could be the option to rather emit:
>
>
> B2)
>
>
> ERC7699.PaymentReference(paymentReference)
> ERC20.Transfer(form, to, amount)
>
>
> However for that case the offchain indexing / wallets / BackEnds would need to listen to and aggregate information from both events.
>
>
> B3)
>
>
> ERC7699.Transfer(from, to, amount, paymentReference) MUST be emitted also in the case the ERC20.transfer(to, amount) op is done. In that case paymentReference is to be emitted empty ( “” ).
> By that the indexers, wallets, etc. can rely solely on this event for contracts compliant with this ERC.

B1 and B3 options violate DRY principle.

Thus amended B2 option is favoured:

1. ERC7699.Reference(transferReference)
2. ERC20.Transfer(form, to, amount)

With a strict requirement that the ERC20.Transfer event MUST be fired immediately after the Reference event.

Researching the process for user application:

1. listen to eth_getLogs filtering by ERC20 contract address, Reference event signature and Reference → gets the tx hash and logIndex of the reference
2. retrieve tx logs by tx hash using getTransactionReceipt
3. find log where topic 0 to be ERC20.Transfer event signature && logIndex > reference_logIndex

Now it can be assumed the emitted Transfer is corresponding to the emitted Reference

We might add `keccak(from, to, value)` to Reference event ( `ERC7699.Reference(bytes indexed transferReference, bytes32 transferEventHash)`) in order to have the option to crosscheck the association with the Transfer event. This is yet to be discussed. [@ashhanai](/u/ashhanai) ?

---

**radek** (2024-09-27):

For the cases where the reference extension is added via pattern of “wrapper over base token”, the Transfer event might not be fired immediately after the Reference event. Therefore it is better to not limit search on reference_logIndex + 1.

Keccak(from, to, value) as a pointer does not help in cases the Transfer log is different due to the imposed fees within the ERC20.transfer(). ERC20 standard does not declare whether the logged amount MUST be the net transferred amount, or the amount including the fees (e.g. Safemoon token).

---

**radek** (2024-09-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ashhanai/48/5885_2.png) ashhanai:

> Even though I understand why you named the value paymentReference, I think it’s not a good idea to mix another term for transfer. Rather, be consistent with the rest of the token standards and use data, or keep it simple and use reference or transferReference if you need to be explicit.

`reference` is the Solidity keyword. Adjusting the term to `transferReference`.

---

**radek** (2024-10-15):

[@abcoathup](/u/abcoathup) I added the section ## Privacy Considerations (reflecting the Web3Privacy Now initiative). The commit does not pass through the checks.

Is there a way to have such chapter within standards?

---

**abcoathup** (2024-10-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/radek/48/16714_2.png) radek:

> Is there a way to have such chapter within standards?

Sounds like a question for [@SamWilsn](/u/samwilsn)

---

**SamWilsn** (2024-10-16):

Make it a subsection under security.

---

**radek** (2024-10-16):

Thx, fixed. I also fixed the license issue. All checks passed, can be merged now.

---

**radek** (2024-10-22):

[@SamWilsn](/u/samwilsn) [@abcoathup](/u/abcoathup) I fixed everything, can you please merge?

---

**abcoathup** (2024-10-22):

You need an ERC editor for that (which I am not).

There is an office hours next week: [EIP Editing Office Hour Meeting 46 · Issue #363 · ethcatherders/EIPIP · GitHub](https://github.com/ethcatherders/EIPIP/issues/363)

---

**mostarz93** (2025-03-13):

Whats the update here fellas? Any momentum to get this thing towards being a standard?

---

**radek** (2025-03-14):

We have this implemented for the Czech stablecoin (yet to be released).

I would appreciate to have the call with someone from the major stablecoins. E.g. Circle devs.

Any help is welcome.

[@mostarz93](/u/mostarz93) Curious, what is your use case?

