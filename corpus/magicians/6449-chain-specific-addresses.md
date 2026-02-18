---
source: magicians
topic_id: 6449
title: Chain-specific addresses
author: lukasschor
date: "2021-06-09"
category: Web > Wallets
tags: [wallet, chain-id]
url: https://ethereum-magicians.org/t/chain-specific-addresses/6449
views: 12596
likes: 58
posts_count: 32
---

# Chain-specific addresses

Hey all. This post is inspired by [this tweet](https://twitter.com/SchorLukas/status/1395325291887833090?s=20) I made a few weeks ago. I was trying to navigate the different EIPs / CAIPs but haven’t found them to be quite satisfactory. Or at least I don’t quite see how one of these standards is able to solve the problems we are facing with bringing Gnosis Safe as a smart contract wallet onto different networks. Therefore I was just aiming to propose a minimally viable solution for chain-specific addresses that would provide optimal UX. I am aware that I might have missed quite a few compatibility aspects etc. and that my proposed solution is not viable, so happy to receive feedback or pointers of any kind.

## Simple Summary

A standard for encoding the network into blockchain address URIs

## Abstract

A standard to be adapted by wallets and dApps to ensure addresses on EVM-based networks remain deterministic.

## Motivation

The need for this EIP emerges from the increasing adoption of non-Ethereum networks that use the Ethereum Virtual Machine. In this context, addresses are not deterministic anymore, as the same address may refer to an EOA on-chain X or a smart contract on-chain Y.

This will eventually lead to Ethereum users losing funds due to human error. For example, users sending funds to a smart contract wallet address that was not deployed on the chain the user actually did the transfer on.

This is not just a hypothetical problem, but users are actually already losing significant funds.

[![CleanShot 2021-06-10 at 08.47.36@2x](https://ethereum-magicians.org/uploads/default/optimized/2X/5/5c618c16095db17087520e5728fd88098a7cbc0b_2_345x94.png)CleanShot 2021-06-10 at 08.47.36@2x978×268 15.9 KB](https://ethereum-magicians.org/uploads/default/5c618c16095db17087520e5728fd88098a7cbc0b) [![CleanShot 2021-06-10 at 08.49.13@2x](https://ethereum-magicians.org/uploads/default/optimized/2X/2/2eb30d4386192954e88f4580df29e47bb9cbbcce_2_345x70.png)CleanShot 2021-06-10 at 08.49.13@2x968×198 10.3 KB](https://ethereum-magicians.org/uploads/default/2eb30d4386192954e88f4580df29e47bb9cbbcce) [![CleanShot 2021-06-10 at 08.48.55@2x](https://ethereum-magicians.org/uploads/default/optimized/2X/6/669c5fd7ad351a0377cd0518c3cde6d2fd5aeba4_2_345x70.png)CleanShot 2021-06-10 at 08.48.55@2x974×198 12.4 KB](https://ethereum-magicians.org/uploads/default/669c5fd7ad351a0377cd0518c3cde6d2fd5aeba4) [![CleanShot 2021-06-10 at 08.48.41@2x](https://ethereum-magicians.org/uploads/default/optimized/2X/6/6b949146efadf26488b9ffb9c05b0395e40b7fc1_2_345x48.png)CleanShot 2021-06-10 at 08.48.41@2x972×136 6.52 KB](https://ethereum-magicians.org/uploads/default/6b949146efadf26488b9ffb9c05b0395e40b7fc1) [![CleanShot 2021-06-10 at 08.48.16@2x](https://ethereum-magicians.org/uploads/default/optimized/2X/8/850fc13c0508536a76829a688cfaa46555825837_2_345x46.png)CleanShot 2021-06-10 at 08.48.16@2x964×130 7.34 KB](https://ethereum-magicians.org/uploads/default/850fc13c0508536a76829a688cfaa46555825837) [![CleanShot 2021-06-10 at 08.47.53@2x](https://ethereum-magicians.org/uploads/default/optimized/2X/0/0465273d49841de63346ce92cb1a08abb9f55fd3_2_345x100.png)CleanShot 2021-06-10 at 08.47.53@2x826×240 5.23 KB](https://ethereum-magicians.org/uploads/default/0465273d49841de63346ce92cb1a08abb9f55fd3)

Besides these security issues, there are also quite a few UX reasons why chain-specific addresses should become the default:

- When a user sends someone an address they don’t want to have to explain what networks their wallet supports and where they can receive assets
- Moving funds from one network to another may result in additional costs or delays. So with more chains emerging and finding adoption, a user would want to specify the network anyways most of the times
- Transaction sender also don’t want to have to ask a recipient what their preferred network is. Or risking sending on a network that then causes inconvenience to the recipient

## Specification

### Syntax

Chain-specific addresses are constructed as follows:

```
Chain-specific address = "network" ":" address”
network = STRING
address = STRING
```

### Semantics

`network` is mandatory and MUST be a valid short name from [GitHub - ethereum-lists/chains: provides metadata for chains](https://github.com/ethereum-lists/chains)

`address` is mandatory and MUST be a EIP-55 compatible hexadecimal address

### Examples

```
eth:0x89205a3a3b2a69de6dbf7f01ed13b2108b2c43e7

matic:0x8e23ee67d1332ad560396262c48ffbb01f93d052
```

## Rationale

I think the above-proposed solution would be the most user-friendly and easiest to coordinate the community around. Especially the human-readable nature of the network shortnames has some nice properties. Because they would mean that even if some users might not yet be used to this new address format and would remove the network identifier in favor of the traditional address format, they still understand that they should only do transactions on the network mentioned. This might not be the case with some of the alternatives below.

### Alternative 1: ChainID instead of shortname

It would be possible to use the EIP-155 compatible chainIDs instead of the shortname

`I.e. 0x...abcd@1 instead of eth:0x…abcd`

Using the chainID would be technically the preferred option, as this would eliminate the dependency on the ethereum-lists repository. It would also allow for better compatibility with existing standards such as EIP-681. Basically, this would mean defining a new minimal standard as a sub-standard to EIP-681 only defining the chainID postfix.

However, the shortname is easier to understand and harder to confuse with other networks due to its human-readable nature.

### Alternative 2: Chain agnostic solution

The Chain Agnostic Improvement Proposals CAIP-2/CAIP-10 try to establish network identifiers that are also inclusive of non-EVM based networks. The problem is that different chain ecosystems have established their own standards for network identifiers similar to EIP-155, such as BIP122 for Bitcoin-chains, LIP9 for Lysk-chains. CAIP2 aims to solve this by referencing those standards in the chainID in order to deterministically define a given network. Potentially CAIP-2 could be utilized to establish chain-specific addresses beyond EVM-based networks. However, this would necessarily lead to a degradation in UX. As the addresses would have to look something like this in order to be compliant with CAIP-2

```
Ethereum mainnet
0xab16a96d359ec26a11e2c2b3d8f8b8942d5bfcdb@eip155:1

Bitcoin mainnet
128Lkh3S7CkDTBZ8W7BbpsN3YYizJMp8p6@bip122:000000000019d6689c085ae165831e93
```

This address format does not seem very user-friendly and will therefore likely be quite controversial. Therefore I argue that an EVM-focused solution is preferred as it is easier to coordinate community around the standard and shows better user experience properties.

### Alternative 3: Use prefix to define network

EIP-831 and other standards define an “ethereum:” schema as part of the URI format and an optional prefix as a use-case definition.

`request                 = "ethereum" ":" [ prefix "-" ] payload`

It might be possible to leverage this prefix for network indicators.

**3a) Using shortname**

`ethereum:matic-0xCecF54a1A0D3c5eFE58102E2751654Ff301d9b63`

**3b) Using chainID**

`ethereum:137-0xCecF54a1A0D3c5eFE58102E2751654Ff301d9b63`

This would mean using a network identifier as a prefix essentially works the same way as the     `pay-` prefix but specific to a given network.

This would allow for future expansion of the standard into a more chain-agnostic standard, where “ethereum:” as an indicator for EVM-based (EIP-155 compatible) chains can be replaced with for example “bitcoin:" allowing to also refer to specific networks in other blockchain ecosystems. However, having Ethereum mentioned in the address, even for EVM sidechains etc. might be misleading.

## Other considerations

### Practical implementation

I think it would be very important for the entire community to come together and adopt chain-specific addresses as a default. In order to make the transition for users as smooth as possible, this would probably have to be a two-step process:

**Step #1**

Dapps and wallets accept chain-specific addresses as input across the board and are just generally able to deal with chain-specific addresses

**Step #2**

Dapps and wallets start displaying all addresses as chain-specific addresses, so users would also copy the chain-specific address and use them to communicate a given address. At this point, most dapps and wallets hopefully already implemented step 1 and the transition would be smooth for users.

## Backwards compatibility

### Compatibility with EIP-831


      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-831)





###



A way of creating Ethereum URIs for various use-cases.










tbd

### Compatibility with EIP-681



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-681.md)





####

  [master](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-681.md)



```md
---
eip: 681
category: ERC
status: Moved
---

This file was moved to https://github.com/ethereum/ercs/blob/master/ERCS/erc-681.md
```










tbd

### Compatibility with ERC-67



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/67)












####



        opened 01:12PM - 17 Feb 16 UTC



          closed 12:46PM - 16 Feb 18 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/1X/52ff44d2b1f56b5a8ccc2fc0b0be8eeca7b69f0b.jpg)
          alexvandesande](https://github.com/alexvandesande)










This proposal is inspired by [BIP 21](https://github.com/bitcoin/bips/blob/maste[…]()r/bip-0021.mediawiki) and could apply to [IBAN address format](https://github.com/ethereum/wiki/wiki/ICAP:-Inter-exchange-Client-Address-Protocol) but can be extended to other proposed addresses formats. Imagine these scenarios:
- An exchange or a instant converter like shape shift wants to create a single ethereum address for payments that will be converted into credit in their internal system or output bitcoin to an address
- A store wants to show a QR code to a client that will pop up a payment for exactly 12.34 ethers, which contains metadata on the product being bought
- A betting site wants to provide a link that the user can click on his site and it will open a default ethereum wallet and and execute a specific contract with given parameters
- A dapp in Mist wants so simply ask the user to sign a transaction with a specific abi in a single call

In all these scenarios, the provider wants to set up internally a transaction, with a recipient, an associated number of ethers (or none) and optional byte code, all without requiring any fuss from the end user that is expected simply to choose a sender and authorise the transaction.

Currently implementations for this are wonky: shape shift creates tons of temporary addresses and uses an internal system to check which one correspond to which metadata, there isn't any standard way for stores that want payment in ether to put specific metadata about price on the call and any app implementing contracts will have to use different solutions depending on the client they are targeting.

I propose adding, beyond address, also optional byte code and value to any proposed address standard. Of course this would make the link longer, but it should not be something visible to the user, instead it should be shown as a visual code (QR or otherwise), a link or some other way to pass the information.

If properly implemented in all wallets, this should make execution of contracts directly from wallets much simpler as the wallet client only needs to put the byte code by reading the qr code.

If we follow the bitcoin standard, the result would be:

```
 ethereum:<address>[?value=<value>][?gas=<suggestedGas>][?data=<bytecode>]
```

Other data could be added, but ideally the client should take them from elsewhere in the blockchain, so instead of having a `label` or a `message` to be displayed to the users, these should be read from an identity system or metadata on the transaction itself.
#### Example:

Clicking this link would open a transaction that would try to send _5 unicorns_ to address _deadbeef_. The user would then simply to approve, based on each wallet UI.

```
 ethereum:0x89205A3A3b2A69De6Dbf7f01ED13B2108B2c43e7?gas=100000&data=0xa9059cbb00000000000000000000000000000000000000000000000000000000deadbeef0000000000000000000000000000000000000000000000000000000000000005
```
### Without byte code

Alternatively, the byte code could be generated by the client and the request would be in plain text:

```
 ethereum:<address>[?value=<value>][?gas=<suggestedGas>][?function=nameOfFunction(param)]
```
#### Example:

This is the same function as above, to send 5 unicorns from he sender to _deadbeef_, but now with a more readable function, which the client converts to byte code.

```
 ethereum:0x89205A3A3b2A69De6Dbf7f01ED13B2108B2c43e7?gas=100000&function=transfer(address 0xdeadbeef, uint 5)
```












tbd

### Compatibility with CAIP-2



      [github.com/ChainAgnostic/CAIPs](https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-2.md)





####

  [main](https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-2.md)



```md
---
caip: 2
title: Blockchain ID Specification
author: Simon Warta (@webmaster128), ligi , Pedro Gomes (@pedrouid), Antoine Herzog (@antoineherzog)
discussions-to: https://github.com/ChainAgnostic/CAIPs/pull/1, https://github.com/UCRegistry/registry/pull/13, https://ethereum-magicians.org/t/caip-2-blockchain-references/3612,
status: Final
type: Standard
created: 2019-12-05
updated: 2021-08-25
---

## Simple Summary

CAIP-2 defines a way to identify a blockchain (e.g. Ethereum Mainnet, Görli, Bitcoin, Cosmos Hub) in a human-readable, developer-friendly and transaction-friendly way.

## Abstract

Often you need to reference a blockchain, for example when you want to state where some asset or smart contract is located. In Ethereum the [EIP155](https://eips.ethereum.org/EIPS/eip-155) chain ID is used most of the time. But with an Ethereum chain ID you cannot reference e.g. a Bitcoin or Cosmos chain.

## Motivation
```

  This file has been truncated. [show original](https://github.com/ChainAgnostic/CAIPs/blob/main/CAIPs/caip-2.md)










tbd

## Replies

**kladkogex** (2021-06-09):

Nice

We will be happy to adopt it at SKALE - we have many chains.

---

**pedrouid** (2021-06-10):

This is definitely an important problem which is why CAIPs have been tackling it as early as 2019

account = address + chainId

Addresses are not contextual enough without a corresponding chainId

However calling a chain “ethereum” or “eth” is too contentious and it will result in a race to capture names plus it will rely on some form of registry

Using EIP-155 chainId have both the advantage of reducing conflicts (communities won’t care so much about integers) and EIP-155 can be queried from the chain directly both off-chain (JSON-RPC) or on-chain (OPCODE)

CAIP-2 chainId’s require that chain identifiers have a reference that is queryable from a blockchain node and each namespace has its own query method.

chainId = namespace + reference

utf8_format = namespace + “:” + reference

example = eip155:1

After developing our CAIP-2 chainId’s specification it was very easy to simply add them to addresses to make them into CAIP-10 account identifiers

We prioritized user familiarity so we decided to make them as suffixes rather than prefixes and used “@“ as separator to resemble emails:

account = address + chainId

utf8_format = address + “@“ + chainId

example = 0xab16a96d359ec26a11e2c2b3d8f8b8942d5bfcdb@eip155:1

CAIP-10 has even been added to the DID linked data vocabulary as “blockchainAccountId”

However some blockchain projects have made some criticisms regarding the order of identifiers in the string

specific @ general : middle

And suggestions were made to include the chainId as prefix instead with the same separator as CAIP-2

general : middle : specific

This could be added to CAIPs as a new account identifier standard to avoid breaking compatibility of existing CAIP-10 integrations

For example: WalletConnect 2.0 protocol, Ceramic chain and Starname service

Important to note that these identifiers are all intended to be machine verifiable and human readable BUT there are other proposals to make more efficient identifiers but less human readable

[@oed](/u/oed) and [@danfinlay](/u/danfinlay) are proposing a multi-format encoding for chain agnostic account identifiers that would reduce the length of identifiers but also would be less recognizable to users accustomed to current addresses

Personally I think there is utility for both CAIP-10 and another more efficient CAIP encoding

I would welcome anyone interested in these discussions to join the CAIP discord (https://discord.gg/3EZWMGPu6g) or the CAIP github ([GitHub - ChainAgnostic/CAIPs: Chain Agnostic Improvement Proposals](https://github.com/ChainAgnostic/CAIPs))

---

**lukasschor** (2021-06-10):

Very valid points! And thanks for elaborating on the thought process behind the existing CAIPs.

I would be interested in what you think of the alternative 3b above specifically. As, while not showing the best UX properties, would be more in line with the concerns you pointed out:

- Having a scheme that uses an identifier ordering from general → middle → specific
- Using chainID to prevent the race for shortnames and as it’s easier to implement

Maybe I’m missing something, but I think it would be interesting to leverage the existing structure defined in EIP-831 and also adopted in EIP-681 where “ethereum:” basically serves the same purpose as “@eip155” in CAIP2/CAIP10, but just more human-readable.

---

**pedrouid** (2021-06-10):

Honestly I’ve been in the past a big proponent of EIP-681 and WalletConnect URI (EIP-1328) shares the same URI format as specified EIP-831

I’ve been contemplating this new CAIP format (namespaces:reference:address) as it’s easier to parse and still easy to read in my opinion. A simple Javascript example:

```javascript
const chain = "eip155:1"
const address = "0xab16a96d359ec26a11e2c2b3d8f8b8942d5bfcdb"
const account = `${chain}:${address}`

const [namespace, reference, address] = account.split(":")
```

It would also make it easy to identify between identifiers by validating the presence of the address

```javascript
function isAccount(id: string) {
   const [namespace, reference, address] = account.split(":")
   return typeof address !== 'undefined'
}
```

Additionally prefixing makes it easier to iterate through different accounts on different chains:

```javascript
const accounts = [
"eip155:1:0xab16a96d359ec26a11e2c2b3d8f8b8942d5bfcdb",
"cosmos:cosmoshub-4:cosmos1t2uflqwqe0fsj0shcfkrvpukewcw40yjj6hdc0",
"polkadot:b0a8d493285c2df73290dfb7e61f870f:HyKp64KyiRn9grkiqobx66MXSjdWYJ1HCMwgYyxTpHxLjq5"
]

// filter ethereum mainnet accounts
accounts.filter(account => account.startsWith("eip155:1")

// filter eip155 compatible accounts
accounts.filter(account => account.startsWith("eip155")
```

---

**John-Status** (2021-06-10):

Hi [@lukasschor](/u/lukasschor) I’ve been thinking about a related issue for some time, see these two comments for some earlier thoughts on this topic:



    ![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/j/0ea827/48.png)
    [Increasing address size from 20 to 32 bytes](https://ethereum-magicians.org/t/increasing-address-size-from-20-to-32-bytes/5485/19) [Ethereum 1.x Ring](/c/working-groups/ethereum-1-x-ring/33)



> Proposal: any new address schema should support encoding multiple shard and L2 rollup chain IDs in a single address
> The shard and L2 rollup chain IDs that are encoded in the address would represent the destination chains into which the address owner is happy to receive tokens e.g. If an address includes the IDs for say the Ethereum L1, Optimism L2 and ZKSync L2 chains, this would signal that the owner of the address is happy for tokens sent to this address to be sent on the Ethereum L1, Optimism…



    ![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/j/0ea827/48.png)
    [EIP-3220 crosschain id specification](https://ethereum-magicians.org/t/eip-3220-crosschain-id-specification/5446/4) [EIPs](/c/eips/5)



> @weijia31415  I think it’s very important that any enhancement of Ethereum’s address format includes the ability to encode multiple chain IDs, not just a single chain ID that is possible with EIP-1191.  I’d like to experiment to see if it’s possible to devise a scheme that uses EIP-55 style case encoding to encode multiple Chain IDs into today’s Ethereum address format.  This would be incompatible with also encoding an EIP-55 checksum into an address, but as we move towards a multi-chain world t…

I see the ability to attach *multiple* chain-IDs to an ethereum address as an important requirement.

However since writing these posts my thinking has shifted a bit and I now think that adding chain-ids to Ethereum addresses (either via extending the address format or via backwards compatible letter case encoding) is not the best approach.

Encoding chain-ids into Ethereum addresses has a fundamental problem in that once Alice shares her address with Bob, and Bob saves Alice’s address into his address book, it is very unlikely that Bob will ever update the copy of Alice’s address that he has saved in his address book.  However the wallet that Alice is using is supporting more and more L2s as time goes on, however Bob will remain unaware that Alice is happy to receive funds to the L2s that Alice’s wallet only recently started supporting because the version of Alice’s address that is saved in Bob’s address book only contains the chain ID’s that Alice’s wallet supported at the time the address was shared.  Even worse, say Alice switches to a different wallet that doesn’t support some of the L2s that Alice’s wallet previously supported at the time Alice shared her address with Bob (or alternatively Alice’s wallet stops supporting an L2 that it previously supported).  Now next time Bob sends funds to Alice, there is a good chance that Bob’s wallet will send funds to Alice on a chain she can’t address.

I think the solution to this problem is that instead of trying to encode chain-IDs into ethereum addresses, we should use resolver services (e.g. an ENS like service) to check on which chains (chain-IDs) the owner of any given ethereum address is happy for funds to be sent to at any given time.  By using a resolver service for this, the chainIDs associated with an ethereum address could be updated by the address owner’s wallet at any time.

An even better solution might be to use an identify service to further abstract this, I had a brief conversation about this with the [iden3.io](http://iden3.io) folks last week.

Happy to hop on a call to discuss, the Ethereum wallet community needs to align around a solution to this problem (how to determine which chains an owner of an Ethereum address is using)

---

**SCBuergel** (2021-06-10):

One concern for me is privacy. I don’t like that I am automatically using the same address across chains, like “Oh sht, did I just accidentally use my savings account for this game on xDAI which is linked to my name?!”

This would be a deeper change to the protocol so probably not going to happen but could be done by adding the chainID to the pubkey before hashing so e.g. `A = B96..255(KEC(chain_id, ECDSAPUBKEY(p)))`

---

**danfinlay** (2021-06-10):

Some properties I’d love to see a widespread standard have:

- a prefix that self-identifies the address format itself
- addresses on different networks or ledgers should be distinct even if the identifier (public key, contract address, etc) controlling that actor is the same.
- The identity of the ledger or network that this account belongs to must be embedded in the address.
- efficient to parse

intended for usage in high-cost computing environments
- making it efficient to find the segment you’re looking for (minimize per-character checks)

could be length-prefixing

use consistent/dense encoding formats

- it’s wasteful to encode base16 as base64

include version prefix to allow forward extensibility

- like in ipld, so that a parser can start by enforcing conditional variants and allowing forward-extensibility

compact in size

- should be small to store and convey, will often be in a QR code, for example.

defined concretely, with binary encoding (CAIP-10 is ambiguous, as it’s defined just in text)

- ipld allows variable encoding
- Since hex is a subset of ascii, if you get a utf-8 string with hex in it, you don’t even know if it’s hex or ascii.
- multibase is a way to render binary data in an unambiguous way, could be an option for representing a binary spec we define.

a checksum for verifying integrity

- Should be fast and cheap to compute
- Maybe could be left to the transport environment (the way a QR does), but EIP-55 seemed to add value.

endian consistency

- I probably prefer most-significant digit first, because it invites the eye to recognize the most important info first, but consistency is probably more important than direction.

---

**oed** (2021-06-10):

Created a quick draft based on conversations with [@pedrouid](/u/pedrouid) [@danfinlay](/u/danfinlay) Kumavis, and insights from observing the multibase / IPLD communities.


      ![](https://ethereum-magicians.org/uploads/default/original/2X/0/0e059a8feebbdf6b4348f5049c9408cfc998331c.png)

      [HackMD](https://hackmd.io/uwG4YAOlQkSV7RW5IVch3g?view)



    ![](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###










I think this addresses all of Dans points above!

Spec tl;dr:

# Multi-Chain Account ID

```js
mcai ::=

```

Example for `0xde30da39c46104798bb5aa3fe8b9e0e1f348163f` on mainnet: `zUJWDxUnc8pZCfUtVKcAsRgxijaVqHyuMgeKKF`.

Edit:

The above spec has not been adopted as CAIP-50: https://github.com/ChainAgnostic/CAIPs/pull/50

---

**bohendo** (2021-06-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png) pedrouid:

> However calling a chain “ethereum” or “eth” is too contentious and it will result in a race to capture names plus it will rely on some form of registry
>
>
> Using EIP-155 chainId have both the advantage of reducing conflicts (communities won’t care so much about integers) and EIP-155 can be queried from the chain directly both off-chain (JSON-RPC) or on-chain (OPCODE)

I doubt that identifying chains w short strings will be very contentious. Squatters on DNS/ENS names have something to gain financially by staking out common names bc they can be resold for a profit but some brand new chain trying to use eg “polkadot” as their short identifier is bad for them (everyone will think it refers to the more popular polkadot chain & not the new one) and it’s bad for the community so no devs would want to add support for a confusing id to their project.

That said, we might be able to avoid this problem entirely: there is an organic & decentralized collision-avoidance problem being solved already w ticker symbols that we might be able to piggy-back off of. As far as I can tell, every chain must have a native currency in which security fees are paid and this native currency could be usable as part of the identifier. It avoids a *new* registry that maps short strings to chains & instead uses mappings that are human-readable and which everyone is already familiar with eg ETH->Ethereum, ETC->Ethereum Classic, DOT->Polkadot, etc, etc. We’ll probably want to add a chainId somehow to accommodate testnets, maybe as a suffix to the mainnet ticker or as an intermediate field? Eg some addresses could be:

Bitcoin: BTC:128Lkh3S7CkDTBZ8W7BbpsN3YYizJMp8p6

Ethereum mainnet: ETH:0xab16a96d359ec26a11e2c2b3d8f8b8942d5bfcdb

Ethereum rinkeby: ETH-4:0xab16a96d359ec26a11e2c2b3d8f8b8942d5bfcdb

Polygon: MATIC:0xCecF54a1A0D3c5eFE58102E2751654Ff301d9b63

I kind of like using eg “ETH-4” for testnets bc it’s not a “real” ticker symbol which indicates that it’s a network which doesn’t store “real” value. Being able to clearly distinguish between value-storing networks from test networks at a glance would be really nice IMO.

Having an intermediate (and optional?) field specifying the chain id could work too eg “ETH:4:0xab16a96d359ec26a11e2c2b3d8f8b8942d5bfcdb” but then it’s not immediately clear which addresses can hold real value & which are only interesting for developers/alpha-testers, which isn’t strictly necessary so whatev.

This pattern of using ticker symbols probably falls apart when it comes to L2 networks tho since many charge security fees in the native currency of the L1… Optimistic Ethereum as an example charges security fees in ETH iiuc so might be confused w mainnet unless we require a chainId to always be present which is probably what we’d want anyway.

---

**pedrouid** (2021-06-15):

Well ticker symbols are not really decentralized nor organic. They are enforced by centralized exchanges.

The BTC vs BCH was not an organic debate but a blind coordination of centralized exchanges to pick a side.

The migration from DAI to SAI ticker was also a coordination by the Maker Foundation to ensure a smooth transition with cooperation of centralized exchanges.

I’m not saying that tickers are a bad idea since they are practical and easily understandable for end-users. But they are also not controlled by a transparent nor democratic process.

EIP155 chainId integers are however more transparent. They are exposed by the blockchain nodes and we have seen collusions being resolved very democratically under the biggest EVM-compatible Github registry repo ([GitHub - ethereum-lists/chains: provides metadata for networkIDs and chainIDs](https://github.com/ethereum-lists/chains)). It’s a very simple dispute where the chain with the older genesis gets to keep the chainId and the other must update it.

Example of an EIP155 dispute: [ChainID 101 conflict · Issue #25 · ethereum-lists/chains · GitHub](https://github.com/ethereum-lists/chains/issues/25)

If most parties feel that EIP155 is not a great prefix perhaps we could introduce an alias like EVM and apply the proposed schema above with `namespace:chainId:address`

Ethereum mainnet: EVM:1:0xab16a96d359ec26a11e2c2b3d8f8b8942d5bfcdb

Ethereum rinkeby: EVM:4:0xab16a96d359ec26a11e2c2b3d8f8b8942d5bfcdb

Polygon mainnet: EVM:137:0xab16a96d359ec26a11e2c2b3d8f8b8942d5bfcdb

Optimism mainnet: EVM:10:0xab16a96d359ec26a11e2c2b3d8f8b8942d5bfcdb

I’m still a strong proponent of the EIP155 chainId integers because these were crucial for WalletConnect since inception to allow maximum interoperability with little to no governance required.

These standards should favor the least human intervention to be successful and that IMO means to have the simplest registry to maintain and verify

---

**lukasschor** (2021-06-16):

I like using the alias “evm:137:…” as an indicator or the namespace. It seems more human-readable and I just see myself having more success explaining to people what the Ethereum Virtual Machine is and why their addresses start with evm, than if I would have to introduce EIPs to people. Users really don’t care where and how these chainIDs are defined.

I also like it from a “marketing” perspective, giving more visibility to the term EVM and therefore showing that “Ethereum” in its wider interpretation is the foundation.

---

**pedrouid** (2021-06-16):

TBH after discussing with multiple projects that currently use CAIPs in production I don’t see any possibility for us to break CAIP-10 spec at all

That being said I also wouldn’t want to see a new spec duplicating the same efforts as CAIP-10 unless it brings significant improvements like CAIP-50

We could however introduce to specification some form of aliases or short names for CAIP-2 namespaces

bip122 → btc

eip155 → evm

cosmos → cosm

polkadot → dot

This could help make namespaces themselves more compact.

PS - this would still introduce breaking changes to existing projects that require deterministic identifiers

---

**lukasschor** (2021-06-16):

I don’t think it should be a hard requirement to not break CAIP-10. Obviously, it would be nice, but after all, it’s a standard that is in “DRAFT” stage with still low adoption. So I would argue that projects implementing a standard like this without making sure it will eventually have broad backing by the ecosystem should be aware of the risks of the standard changing or a competing standard being adopted over it. That’s why we should now really make sure that the entire ecosystem is included in the discussion so that eventually we can settle on a standard that actually gets adopted widely.

Sadly this topic might at some point even turn into a political / ideological discussion. As the ideal solution for projects with a more “EVM-centric” mentality might look different than people that think truly “multichain”. And we don’t want to end up having both, an EIP and a CAIP, eventually solving the same problem and worst-case even be non-compatible. So I would just be careful having e.g. the compatibility with non-final CAIPs be a hard requirement because this will remove flexibility in finding common ground / compromises on these bigger concerns.

---

**pedrouid** (2021-06-16):

Could we open an issue on Github CAIPs to make these proposed changes more formally?



      [github.com](https://github.com/ChainAgnostic/CAIPs)




  ![image](https://opengraph.githubassets.com/edbc7adc6170962e23268ca3563f0bb8/ChainAgnostic/CAIPs)



###



Chain Agnostic Improvement Proposals










That way we could gather consensus around these decisions and present arguments properly

---

**bohendo** (2021-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png) pedrouid:

> Well ticker symbols are not really decentralized nor organic. They are enforced by centralized exchanges.

Multiple centralized exchanges deciding on ticker symbols is still decentralized decision making, there’s no central-centralized-exchange that has any power to coerce the others either way.

That said, I don’t have a strong preference for ticker symbols & EVM:chainId:address is actually my favorite proposal so far… pending chainId conflicts for which I think first-come-first-served is a perfectly clear & fair rule to coordinate around.

EIP155 is a killer solution for those in the know… but it’ll prob be alien & unfamiliar for most end users whereas the `EVM` prefix is more well known & also provides useful info regarding the chain’s capabilities which is a nice bonus

---

**pedrouid** (2021-06-28):

I’ve aggregated what I think were some of the most important points touched on this thread and also on different threads on Twitter under a single issue on CAIPs

I would like to invite anyone who has strong opinions over the proposed formats for multi-chain account identifiers to share their feedback below



      [github.com/ChainAgnostic/CAIPs](https://github.com/ChainAgnostic/CAIPs/issues/51)












####



        opened 03:14PM - 23 Jun 21 UTC



          closed 04:57PM - 10 Feb 22 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/f/f066c21f9a2231bd2cb4eb4ff77d3a4670d39599.png)
          pedrouid](https://github.com/pedrouid)










CAIP-10 has received a lot of feedback within the last year including some criti[…]()cisms over its structure. Many Twitter and Discord threads have been written about what would constitute an ideal multi-chain account identifier from which it has also generated new CAIP proposals (#50).

A lot of feedback has also been generated recently in an Ethereum Magicians thread: https://ethereum-magicians.org/t/chain-specific-addresses/6449

Additionally some polls were also created on Twitter:
Poll 1 - https://twitter.com/SchorLukas/status/1404831686714613769
Poll 2 - https://twitter.com/pedrouid/status/1404869512512606218

From my perspective there is essentially a division between 3 main identifiers:
```
A - "0xab16a96d359ec26a11e2c2b3d8f8b8942d5bfcdb@eip155:1" (current CAIP-10)
B - "evm:1:0xab16a96d359ec26a11e2c2b3d8f8b8942d5bfcdb" (updated CAIP-10)
C - "zUJWDxUnc5gJJSWFzxyKkmLp1dgyxiPYT3BrT4" (proposed CAIP-50)
```

From both polls and also from the Ethereum Magicians thread, the majority supports the identifier with format B.

This would mean that it would require the following changes:
1. change of endianness of CAIP-10 and using the same separator as CAIP-2
```
specific@generic:middle → generic:middle:specific
```
2. update CAIP-2 namespaces to shorter and more recognizable names
```
bip122 → btc
eip155 → evm
cosmos → cosm
polkadot → dot
```

I propose that we make these changes to respective CAIP standards which are in DRAFT status with two separate PRs for each change and follow up with discussions for each.












Most importantly please share the use-cases you are tackling with your proposed formats to better understand what it’s being optimized for

---

**lukasschor** (2021-08-22):

Here’s a suggestion of using shortnames from ethereum-lists as aliases for the CAIP-3 blockchain IDs. This would create a human-readable standard for chain specific addresses that can be resolved to CAIP-10 account identifiers for better developer-handling. Would love to hear your feedback. CC [@oed](/u/oed) [@danfinlay](/u/danfinlay) [@itamarl](/u/itamarl)



      [docs.google.com](https://docs.google.com/document/d/1Mu_o9bdyteaZd468BNdTKtrUj2QjzTfEdOFmJPyGOOs/edit?usp=sharing)



    https://docs.google.com/document/d/1Mu_o9bdyteaZd468BNdTKtrUj2QjzTfEdOFmJPyGOOs/edit?usp=sharing

###

--- eip:  title: Chain-specific addresses Author: Lukas, Pedro, Ligi discussions-to: https://ethereum-magicians.org/t/chain-specific-addresses status: Draft type: Standard category: Interface created: 2021-08-16 --- Simple Summary A standard for...

---

**pedrouid** (2021-08-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lukasschor/48/1468_2.png) lukasschor:

> EIP: Chain-specific addresses - Google Docs

This looks great ![:ok_hand:](https://ethereum-magicians.org/images/emoji/twitter/ok_hand.png?v=12) we should move it to Github and point the “discussions-to” url to this thread

---

**lukasschor** (2021-08-28):

Started an EIP draft: [EIP for chain-specific addresses by lukasschor · Pull Request #3770 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/3770)

[@pedrouid](/u/pedrouid) [@ligi](/u/ligi)

---

**SamWilsn** (2022-04-05):

I’m late to the party, but I’d love to see [EIP-3770](https://eips.ethereum.org/EIPS/eip-3770) move to review then final!

Two *tiny* recommendations:

- drop the 0x prefix since it doesn’t really convey any useful information; and
- move the table of prefixes into the EIP itself.


*(11 more replies not shown)*
