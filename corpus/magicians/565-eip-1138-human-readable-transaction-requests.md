---
source: magicians
topic_id: 565
title: "EIP-1138: Human-Readable Transaction Requests"
author: pedrouid
date: "2018-06-18"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-1138-human-readable-transaction-requests/565
views: 1641
likes: 8
posts_count: 9
---

# EIP-1138: Human-Readable Transaction Requests

I wanted to bring up here the discussion for Human-Readable Transaction Requests that Witek Radomski proposed



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












On WalletConnect we have a method to relay a transaction request from the desktop Dapp to the mobile Wallet but currently this simply provides a raw transaction that the Wallet needs to parse in order to display to the user what’s being requested to be signed

With this EIP it would enable not only to share this information between the Dapp and the Wallet to display to the user but also to generate a raw transaction to be signed and broadcasted.

## Replies

**pedrouid** (2018-06-18):

This proposal includes parameters for sharing a summary, a description and an icon in the transaction request to display information that may not be available on the wallet. However this still needs to be machine verifiable otherwise it opens up vulnerabilities for phishing

---

**alexvandesande** (2018-06-18):

> ethereum:makerdai.eth/transfer&address=notascammer.eth&uint256=100000e18¶m=_to¶m=_value&description=Buys a cute innocent little kitten. Pay no attention to the DAI transfer call, I swear all this does is buy a super cute kitten!

I think this is the wrong approach. We should not trust the app to describe to us what the transactions does. Instead, we should rely on a [Radspec](https://github.com/aragon/radspec) description of the contract functions which is provided by either the contract itself or given by the client/wallet.

---

**pedrouid** (2018-06-18):

Amazing, exactly what I was looking for allowing the description to be verifiable ![:raised_hands:](https://ethereum-magicians.org/images/emoji/twitter/raised_hands.png?v=9) I’ve commented on the github issue for this EIP

---

**MicahZoltu** (2018-06-19):

[@pedrouid](/u/pedrouid) I recommend checking out https://github.com/ethereum/EIPs/issues/719.  It is in dire need of a champion, I drafted up the issue hoping someone would get excited enough about it to take it to the finish line but no such luck so far.  If you are really interested in informed signing requests, that is where I recommend you start.

---

**pedrouid** (2018-06-19):

Thanks for sharing this [@MicahZoltu](/u/micahzoltu)! There is definitely a lot of candidates for tackling machine-verifiable human-readable transaction requests. So far we have the 681, 831, 719, 1138 and also radspec

I think the key aspects that will make or break from all of these is the one that is able to tick the following:

1. Fully machine verifiable
2. Can be easily read as single sentence
3. Doesn’t focus solely on token transfers (thus covering all smart contract functions)
4. Could also be used interchangeably between normal transactions & smart contract calls
(ideally even for signing messages)

And optionally I think it could even be designed in a way that it can be easily used between different protocols like the 681, 831 and 1138 have the uri format starting with `ethereum:`

---

**fubuloubu** (2018-06-19):

Of course don’t be specific to ETH/Token transfers, but I think some sort of common flag that denotes “transfers or handles valuable assets” like tokens but also ownership and such would be useful to call out. I sort of see three different levels of risk in a function: 1) no state changes, 2) internal state changes, or 3) transfers or handles valuable assets internally or through an external call

A change in UX feedback such as a different color or something would be very handy I think.

---

**pedrouid** (2018-06-19):

That’s a great point [@fubuloubu](/u/fubuloubu), however Ethereum smart contracts could be anything, how would you distinguish the level 2 from 3? Technically they both constitute internal state changes and it’s the Dapp developer who will be determining this level of risk when requesting the transaction.

Thus how could we make this distinction machine verifiable?

---

**fubuloubu** (2018-06-19):

Well, you can’t. Humans ascribe value to whatever trinkets make sense to them. That isn’t really machine validateable.

I would suggest it becomes part of the discipline of writing into Natspec-style comments.

EDIT: I mean, you could probably try all the functions and tell the human that the function executed wrong but the state change is final, and then judge the degree of violence the human perpetuates against the machine, but that probably isn’t a scalable method for measuring value.

