---
source: magicians
topic_id: 650
title: "ERC-681: Representing various transactions as URLs"
author: jpitts
date: "2018-07-05"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/erc-681-representing-various-transactions-as-urls/650
views: 6670
likes: 7
posts_count: 11
---

# ERC-681: Representing various transactions as URLs

This is a very useful proposal by [@nagydani](/u/nagydani)  that should be getting more attention now that UX (and what I would call “developer UX”) is such a high priority in the community.

**Simple Summary**

A standard way of representing various transactions, especially payment requests in Ethers and ERC #20 tokens as URLs.

**Abstract**

URLs embedded in QR-codes, hyperlinks in web-pages, emails or chat messages provide for robust cross-application signaling between very loosely coupled applications. A standardized URL format for payment requests allows for instant invocation of the user’s preferred wallet application (even if it is a webapp or a swarm đapp), with the correct parameterization of the payment transaction only to be confirmed by the (authenticated) user.


      [github.com](https://github.com/nagydani/EIPs/blob/master/EIPS/eip-681.md)




####

```md
## Preamble

    EIP: 681
    Title: URL Format for Transaction Requests
    Author: Daniel A. Nagy
    Type: Standard Track
    Category: ERC
    Status: Draft
    Created: 2017-08-01
    Requires: 20, 137, 831

## Simple Summary
A standard way of representing various transactions, especially payment requests in Ethers and ERC #20 tokens as URLs.

## Abstract
URLs embedded in QR-codes, hyperlinks in web-pages, emails or chat messages provide for robust cross-application signaling between very loosely coupled applications. A standardized URL format for payment requests allows for instant invocation of the user's preferred wallet application (even if it is a webapp or a swarm đapp), with the correct parameterization of the payment transaction only to be confirmed by the (authenticated) user.

## Motivation
The convenience of representing payment requests by standard URLs has been a major factor in the wide adoption of Bitcoin. Bringing a similarly convenient mechanism to Ethereum would speed up its acceptance as a payment platform among end-users. In particular, URLs embedded in broadcast Intents are the preferred way of launching applications on the Android operating system and work across practically all applications. Desktop web browsers have a standardized way of defining protocol handlers for URLs with specific protocol specifications. Other desktop applications typically launch the web browser upon encountering a URL. Thus, payment request URLs could be delivered through a very broad, ever growing selection of channels.

```

  This file has been truncated. [show original](https://github.com/nagydani/EIPs/blob/master/EIPS/eip-681.md)

## Replies

**pedrouid** (2018-07-05):

Totally agree, we are working on implementing this as part of the WalletConnect standard. However I think this is a great start for doing transaction requests but I find that there is still more information needed to clearly provide human-readable machine-veriable transaction requests similar to Aragon’s Radspec as suggested by @avsa on the thread for EIP-1138

---

**jpitts** (2018-07-05):

Referencing these here:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/1138)












####



        opened 03:43AM - 07 Jun 18 UTC



          closed 06:13AM - 19 Dec 21 UTC



        [![](https://avatars.githubusercontent.com/u/2774008?v=4)
          coinfork](https://github.com/coinfork)





          stale







```
---
eip: 1138
title: Human-Readable Transaction Requests
author: Witek R[…]()adomski <witek@enjin.com>
type: Standards Track
category: ERC
status: WIP
created: 2018-06-06
discussions-to: https://github.com/ethereum/EIPs/issues/1138
requires: 681, 831
---
```

## Simple Summary

A standard format for providing additional human-readable data to smart contract functions using Ethereum function call URIs, as specified in ERC-681.

## Abstract

Including standard metadata in Transaction Request URIs will allow wallets to describe the proposed transaction to the end user in a more human-readable format, and also including the function parameter names that correspond to the passed arguments.

By implementing this ERC, a wallet will be able to display:
- The function name
- A table of parameter names, values (argument names) and their respective types
- Context, summary, and description text about the actual transaction
- An image representing the transaction or affected tokens

## Motivation

While the [URL Format for Transaction Requests](https://eips.ethereum.org/EIPS/eip-681) supports creating ETH transactions with minimum required data, not enough information is available in both the URI and blockchain to explain what parameters are being passed to the function.

As more wallets and dapps adopt the [ERC-681 standard]((https://eips.ethereum.org/EIPS/eip-681)), we need a way for all this software to inform the end-user about the transactions being created. One of the greatest frustrations (and attack vectors) with existing methods and wallets is the difficulty in understanding transaction data. Software supporting these URI standards should be able to clearly tell an end-user about precisely what is being signed.

Applications like [WalletConnect](https://github.com/WalletConnect/) and [Enjin Wallet](https://enjinwallet.io/) are used in conjunction with dapps to provide notifications of transaction requests in a friendly user-interface.

## Specification

### Syntax

Function call URIs follow the ERC-681 protocol, with the following change:

```
key    = "value" / "gas" / "gasLimit" / "gasPrice" / "param" / "context" / "summary" / "description" / "action" / "image" / TYPE
```

### Semantics

`param` are supplied as strings denoting each function parameter name. They must be in the exact same order and number as in the function signature.

`context` denotes the source or context of transaction being performed. For example, this might be the name of the Dapp. (Supports Argument Injection)

`summary` is the title of the transaction, for example "Transfer 5 tokens". (Supports Argument Injection)

`description` is the longer text description of the transaction being requested, for example "This will transfer $(_value)[18]$ ENJ tokens to $(_to)$". (Supports Argument Injection)

`action` is intended to customize the action button that proceeds to sign and broadcast the transaction. Examples of action text would be "Approve", "Transfer" or "Mint".

`image` is the HTTP/HTTPS URL of an image or icon that represents the transaction.

### Argument Injection

Any arguments passed to the contract can be replaced into the `context`, `summary`, and `description` fields by client software. This would help in showing end-users that the expected values are being passed to the function. To inject a function argument into the text, use the opening and closing pairs: `$(` and `)$` , for example `$(ARGUMENT_NAME)$`.

An optional helper can be included in this syntax to display numeric values (such as a token's value) with their appropriate decimal places. To do this, square brackets containing the number of decimal places between 0 and 18 can be included before the ending $ character: `$(ARGUMENT_NAME)[18]$`. All other variables can be parsed and displayed automatically by client software by simply looking at the parameter type defined in the ABI.

### Security Considerations

Wallet apps should offer an option to view the details of the function call.

This view should clearly display:
- The function name
- Each parameter's name
- Each parameter's argument value
- Each parameter's type

If the wallet is capable of interpreting the contract address (for example, a known ERC-20 or ERC-721 token), it could display more information about the transaction. For example, if the wallet is able to resolve the name, icon, decimals, and symbol of a non-fungible token, it should do so and display these depending on the specific transaction's context.

### Example

```
ethereum:0xF629cBd94d3791C9250152BD8dfBDF380E2a3B9c/transfer&address=0x1111111111111111111111111111111111111111&uint256=1880000000000000000&param=_to&param=_value&context=Game%20Marketplace&summary=Transfer%205%20tokens&description=This%20will%20transfer%20%24%28_value%29%24%20ENJ%20tokens%20to%20%24%28_to%29%24&action=Send&image=https%3A%2F%2Fenjincoin.io%2Fimages%2Findex%2Fenjin-coin-logo.png
```

## References
ERC-681, https://eips.ethereum.org/EIPS/eip-681
ERC-831, https://eips.ethereum.org/EIPS/eip-831
ERC-67, https://github.com/ethereum/EIPs/issues/67

## Implementation

- [Enjin Coin](https://enjincoin.io) ([github](https://github.com/enjin))

## Copyright
Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).














      [github.com](https://github.com/aragon/radspec)




  ![image](https://opengraph.githubassets.com/9c5e21ae116b614ffd324d682831019b/aragon/radspec)



###



🤘 Radspec is a safe interpreter for Ethereum's NatSpec

---

**mikro2nd** (2018-07-05):

Agree that this is an important step in improving UX. I do have one (faint) concern:

> chain_id is optional and contains the decimal chain ID, such that transactions on various test- and private networks can be requested. If no chain_id is present, the client’s current network setting remains effective.

Would it not be better to mandate that the default chain be the mainnet rather than something dependent on the client’s current settings. By relying on the client settings you’re introducing a vector for introducing debugging hassles:

##### A Play In One Act

```auto

Dev: What chain_id did you use?
User: ?
Dev: Did the URL contain a chain_id?
User : I don't think there was one...

Dev: OK, which blockchain was your client using at the time?
User: I've no idea. I think it may have been some test network.

```

…you get the idea, I hope!

Whereas, if the default is mandated to be the mainnet, there’s just one less (fertile) source for confusion when it comes to debugging.

Hope this makes some technical sense, but I confess I’m not well qualified to judge that – I’m just coming at it from a perspective of decades of debugging… ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=15)

---

**MicahZoltu** (2018-07-05):

There is not a single chain that can be considered canonical.  When a contentious fork occurs, there will be two “main” chains and it is up to users, exchanges, wallets, etc. to decide which one is “main”.  People have argued in the past (and I have supported) that the chain ID should change with *every* fork, thus defaulting is also not really reasonable.  Your client follows some chain, someone else’s client follows another chain, both clients call the chain they follow “main”, neither chain uses the same chain ID from before the fork.

---

**nagydani** (2018-07-05):

It has been debated a bit, and to be honest I do not remember why it was decided this way, but I guess that it had something to do with being able to test URL’s without a network id on testnets as well as being able to transition to a different chain ID after some contentious hardfork.

---

**mikro2nd** (2018-07-06):

I’ll stand by my conviction that the existence of a hidden variable is a dangerous source of confusion that will result in misery for many people in time to come, and I strongly urge a reconsideration while the EIP is still in draft and amenable to change/improvement.

Perhaps a better solution than I first suggested is simply to make the `chain` element of the URL mandatory rather than “optional with a hidden default”.

---

**ligi** (2018-07-30):

AFAIR the chain_id was made optional to provide some backward compatibility to ERC-67 - when making it mandatory would always break compatibility.

Also I do not really see the reason to make it mandatory - it is easy - if the parameter is not there -> then the value is 1. I dont’t see users knowing/remembering about chain_id’s in URLs as a valid case - they just will not know or remember - no matter if there is always a number or not. But just my 2cents.

---

**php4fan** (2022-06-19):

Why is there no explanation whatsoever in the specification about the `pay-` prefix??

The formal grammar specification says the url starts with `ethereum:` followed by an optional `pay-`, that is, either `ethereum:0x.....` or `ethereum:pay-0x.....`, but says nothing about when the `pay-` prefix is allowed or required. Does it make no difference whatsoever? If so it should be specified, because it’s quite counterintuitive that there would be a prefix that you can arbitrarily include or leave out and it makes no difference at all.

Intuition suggests that maybe the p`pay-` prefix should be present when the transaction has a non-zero value, but (a) that’s entirely me speculating, it’s not stated anywhere, and (b) there are examples with non-zero value and with no `pay-` prefix.

---

**zhangzhongnan928** (2025-07-31):

![:credit_card:](https://ethereum-magicians.org/images/emoji/twitter/credit_card.png?v=15) Making `ethereum:` URIs Actually Work: Proposal for ABI Discovery via ERC-5169 / 7738

---

We’re working on crypto-native NFC payment flows—think “Apple Pay for crypto.”

The ideal UX looks like this:

> Merchant enters amount
> User taps their phone on the NFC device
> Phone opens wallet with a pre-filled transaction
> User taps “Confirm” → done

To achieve this, we want to encode `ethereum:` payment URIs (EIP-681) into NFC tags.

###  The Problem

While native token transfers work fine using `?value=...`, **smart contract calls break** across nearly all major wallets (MetaMask, Rainbow, Trust, Coinbase Wallet, etc).

Example URI:

```auto
ethereum:0xABC123/transfer?address=0xDEF456&uint256=1.23
```

This silently fails or gets ignored. Why?

---

###  Root Cause

1. No ABI context — Wallets don’t know how to encode calldata without knowing parameter types.
2. No standard ABI discovery — There’s no canonical way for a wallet to fetch a contract’s ABI.
3. Wallet safety concerns — Guessing types is dangerous, so most wallets opt to ignore.

---

###  Proposed Solution: ABI Discovery via scriptURI

We propose using [ERC-5169](https://eips.ethereum.org/EIPS/eip-5169) or [ERC-7738](https://github.com/ethereum/EIPs/pull/7738) to let contracts expose ABI metadata to wallets.

#### Example:

```solidity
function scriptURI(bytes4 selector) external view returns (string memory);
```

Wallets could:

- Query scriptURI() on the contract
- Fetch the ABI from the returned URI
- Parse the URI params using that ABI
- Construct a valid data field and submit the transaction

This restores the original vision of EIP-681—linking wallets, NFC devices, QR codes, and POS terminals in a seamless, standardized way.

---

###  Sample Flow

1. NFC tag encodes:

```auto
ethereum:0xABC123/transfer?address=0xDEF456&uint256=1.23
```
2. Wallet calls:

```solidity
scriptURI("0xa9059cbb")
```
3. URI returns JSON:

```json
{
  "name": "transfer",
  "inputs": [
    { "name": "to", "type": "address" },
    { "name": "value", "type": "uint256" }
  ]
}
```
4. Wallet builds calldata, user confirms, done.

---

###  Why this matters

If we want crypto to reach real-world adoption (cafés, transit, vending machines), we **must**:

- Make URI-triggered smart contract interactions reliable
- Avoid requiring dApps or custom flows
- Empower POS hardware with standards-compliant, low-cost NFC/QR workflows

---

###  Call to Action

We’re calling on:

- Wallet developers
- ERC-681 / URI standards contributors
- Smart token and TokenScript builders
- Mobile UX & NFC ecosystem folks

Let’s collaborate on a lightweight, secure, standardized ABI-discovery flow so that `ethereum:` URIs can actually fulfill their promise.

Thoughts, feedback, or interest in prototyping with us? We’d love to hear from you.

---

**PushHandle** (2025-12-10):

+1 I would like to participate in your “Call to Action”. I’ve spoken with several ERC-681 developers in the last few weeks/months. Most feel like they are building independently despite the increased interest and potential for broader app adoption. Is activity happening somewhere else? If not, happy to help set up and share a working session.

