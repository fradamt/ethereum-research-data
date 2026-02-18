---
source: magicians
topic_id: 9142
title: "EIP: wallet_switchActiveRpcProvider"
author: sbacha
date: "2022-05-03"
category: EIPs
tags: [wallet, json-rpc]
url: https://ethereum-magicians.org/t/eip-wallet-switchactiverpcprovider/9142
views: 2575
likes: 16
posts_count: 14
---

# EIP: wallet_switchActiveRpcProvider

# wallet_switchNetworkRpcProvider

> draft spec github repo link

Critiques, contributions, and requests are openly welcomed. If you would like to contribute to the specification just open a PR on github!

## Abstract

The `wallet_switchNetworkRpcProvider` RPC method allows Ethereum applications (“dapps”) to request

that the wallet switches its active RPC Provider backend if the wallet has a concept thereof.

The caller MUST specify a chain ID. The caller MUST specify a valid URL for the RPC Endpoint

The wallet application **may not** arbitrarily refuse or accept the request. A status code of `200`

is returned if the active RPC was successfully switched, A status code of `[TODO]` otherwise.

> Important cautions for implementers of this method are included in the
> Security Considerations section.

## Motivation

The purpose `wallet_switchNetworkRpcProvider` is to provide dapps with a way of requesting to switch

the wallet’s active chain’s RPC Provider, which they would otherwise have to ask the user to do manually.

- Account Abstraction via private mempool (EIP4339)
- Fallback provider for RPC Connectivity issues (at the Server side) (Example: Infura Service
Outage)
- Failover provider for RPC Connectivity issues (as the Client side) (Example: Smartphone
connectivity issues)
- Providing Transaction Privacy via RPC Provider endpoint (e.g. Flashbots, OpenMEV, EdenNetwork,
etc)
- Accessing custom RPC Methods supported by the custom RPC Endpoint’s Provider

### Existing EIP Specifications do not service this end

`updatedEthereumChain` specifies that the “…Wallet should default the `rpcUrl` to **any existing

endpoints matching a chainId known previously to the wallet**, otherwise it will use the provided

rpcUrl as a fallback.”

`wallet_switchNetworkRpcProvider` intentionally and explicitly is purely concerned with switching

the active RPC endpoints, regardless of any other metadata associated therewith.

## Rationale

All dapps require the user to interact with one or more Ethereum chains in order to function. Some

wallets only supports interacting with one chain at a time. We call this the wallet’s “active

chain”.

The Wallet’s “active chain” has an “active RPC Provider”

`wallet_switchNetworkRpcProvider` enables dapps to request that the wallet switches its active RPC

connection provider to whichever one is required by the dapp.

This enables UX improvements for both dapps and wallets as discussed in the motivation section.

The method accepts am object parameter to allow for future extensibility at virtually no cost to

implementers and consumers.[^4]

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”,

“RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in

[RFC-2119](https://www.ietf.org/rfc/rfc2119.txt).

Since JSON-RPC utilizes JSON, it has the same type system (described in

[RFC 4627](http://www.ietf.org/rfc/rfc4627.txt)). JSON can represent four primitive types (Strings,

Numbers, Booleans, and Null) and two structured types (Objects and Arrays). The term “Primitive” in

this specification references any of those four primitive JSON types. The term “Structured”

references either of the structured JSON types. Whenever this document refers to any JSON type, the

first letter is always capitalized: Object, Array, String, Number, Boolean, Null. True and False are

also capitalized.

All member names exchanged between the Client and the Server that are considered for matching of any

kind should be considered to be case-sensitive. The terms function, method, and procedure can be

assumed to be interchangeable.

The Client is defined as the origin of Request objects and the handler of Response objects. The

Server is defined as the origin of Response objects and the handler of Request objects.

### wallet_switchNetworkRpcProvider

The method accepts an object parameter with defined fields ^parameters The method

returns `null` if the wallet switched its active chain, and an error otherwise.

The method presupposes that the wallet has a concept of a single “active chain”. The active chain is

defined as the chain that the wallet is forwarding RPC requests to.

1. Terminology: Wallets are defined as ‘Clients’ as defined in the Specification section Dapps are
defined as ‘Servers’ as defined in the Specification section
2. Wallets MUST switch to the requested RPC URL if the existing ChainID is known to the wallet.

- A dialog box requesting a user to add this to their ‘address book’/etc is recommended to be
shown.

1. Wallets MUST NOT reject the switch to the new RPC Provider URL if the ChainID is known to the
wallet for no non-error reasoning.
2. If a field does not meet the requirements of this specification, the wallet MUST reject the
request.
3. The wallet application MUST NOT arbitrarily refuse the request.

### Connectivity

The Provider is said to be “connected” when it can service RPC requests to at least one chain.

The Provider is said to be “disconnected” when it cannot service RPC requests to any chain at all.

To service an RPC request, the Provider must successfully submit the request to the remote location, and receive a response. In other words, if the Provider is unable to communicate with its Client, for example due to network issues, the Provider is disconnected.

#### Parameters

> .NOTE - WORK IN PROGRESS SECTION

| Parameter | Description | Required | Values | Error Code | Error Message |  |
| --- | --- | --- | --- | --- | --- | --- |
| chainId | specify the integer ID of the chain as a hexadecimal string, per EIP 695 | TRUE | 1-4503599627370476 | -32701 | Result: eth_ChainId Result: Transport Connection Result: Malformed Input | eth_chainId |
| rpcUrl | The RPC endpoint URL to target. | TRUE | ^$|[1][a-zA-Z_\$0-9]*$ | -32300 | rpcUrl URL ADDRESS format is invalid. |  |
| rpcMethod | The RPC method to request. | FALSE |  |  |  |  |
| setDefault | OPTIONAL | FALSE |  |  |  |  |
| setConfig | OPTIONAL | FALSE |  |  |  |  |
| flushPendingTransactions | Rebroadcast all non-confirmed transactions, in order of oldest to newest, to the new rpc connection | TRUE |  |  |  |  |
| version |  | FALSE | [0-9]+\.[0-9]+\.[0-9]+ |  |  |  |

- chainId

REQUIRED

- MUST specify the integer ID of the chain as a hexadecimal string, per the
eth_chainId Ethereum RPC method.
- The chain ID MUST be known to the wallet.
- The wallet is REQUIRED be able to switch to the specified chain and service RPC requests to
it. It can not reject the request based on exclusivity of pairing providers with networks.
- This exclusivity means wallets MUST allow users to be able to configure ANY ChainID with
an RPC Provider of their choice.

`rpcUrl`

- REQUIRED
- can’t have user@password in RPC url

`flushPending`:

- REQUIRED

`setDefault`:

- OPTIONAL
- optional field for dapp’s to automatically switch when logged into

#### Parameters

`wallet_switchNetworkRpcProvider` accepts an object parameter, specified by the following TypeScript

interface:

```typescript
interface SwitchEthereumChainParameter {
  rpcUrl:  // required
  chainId: string; // required
  flushPending: boolean // required
  setDefault: boolean; // optional
}
```

#### Returns

The method **MUST** return `null` if the request was successful, and an error otherwise.

If the wallet does not have a concept of an active RPC Provider, the wallet **MUST** reject the

request.

If an RPC method defined in a finalized EIP is not supported, it **SHOULD** be rejected with a 4200 error per the Provider Errors section below, or an appropriate error per the RPC method’s specification.

### Examples

These examples use JSON-RPC, but the method could be implemented using other RPC protocols.

To switch to Mainnet:

```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "wallet_switchNetworkRpcProvider",
  "params": [
    {
      "chainId": "0x1",
      "rpcUrl": "https://"
    }
  ]
}
```

To switch to the Goerli test chain:

```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "wallet_switchNetworkRpcProvider",
  "params": [
    {
      "chainId": "0x5",
      "rpcUrl": "https://"
    }
  ]
}
```

## Backwards Compatibility

*Tenative*: Will Examine more thoroughly

Does not introduce backwards incompatibilities with existing `wallet_` methods or EIP specifications

## Security Considerations

For wallets with a concept of an active chain, switching the active chain has significant

implications for pending RPC requests and the user’s experience. This is relevant with the parameter

of `flushPendingTxs`. If the active RPC Provider switches the new endpoint *could* be behind the default RPC

endpoint’s ‘latest’ block.

In light of this, the wallet should:

- Display a confirmation whenever a wallet_switchNetworkRpcProvider is received, clearly
identifying the requester and the chain that will be switched to.
- The confirmation used in EIP-1102 may serve as a point of reference.
- When switching the active RPC Provider, MUST NOT cancel and/or rebroadcast any pending RPC requests and/or
chain-specific user confirmations unless flushPendingTransactions is TRUE.
- Wallet’s could provide a syncing modal until the transactions are confirmed if flushPendingTransactions is FALSE

1. a-zA-Z_\$ ↩︎

## Replies

**jamierumbelow** (2022-05-03):

Eager to help push this if possible.

It feels like a natural companion to my [Adding rpcURL to `chainChanged` event](https://ethereum-magicians.org/t/adding-rpcurl-to-chainchanged-event/9012), which allows wallet → frontend RPC provider synchronisation. This EIP offers synchronisation in the other direction.

---

**matthewlilley** (2022-05-04):

Likewise, this would make the UX a lot better for Sushi users.

---

**sbacha** (2022-05-05):

Very interesting! We actually have a draft spec of a new Web3 Provider called an ‘ablative provider’. It similarly provided wallet → frontend sync!

> …It would also allow further decoupling of frontends from centralised node providers such as Alchemy and Infura, allowing users to opt-out of sending their transactions through such providers and instead offer a standardised way for users to connect to their own hosted nodes, or some other preferred node provider.

Exactly. I think it’s actually weird that all of these issues really boil down to the fact that wallets immediately broadcast a signed transaction. I understand why they would implement that behavior, though it seems like an easy option to provide users.

Would love to chat more if you are so inclined, I think defining a new web3 provider may be warranted, especially with how state is handled currently.

- Deterministic, finite states & caching #85
Deterministic, finite states & caching · wevm/wagmi · Discussion #85 · GitHub
- Discussion: Provider will fail if the backend network changes except for “any” #866
Discussion: Provider will fail if the backend network changes except for "any" · Issue #866 · ethers-io/ethers.js · GitHub

An example use case is mentioned here

[bug] Account hook rpc not update on chain switch]([[bug] Account hook rpc not update on chain switch · Issue #365 · wevm/wagmi · GitHub](https://github.com/tmm/wagmi/issues/365#))#365

> Ultimately my goal here is to use the default WalletConnect modal/UI when connecting on mobile screens, but on desktop the modal is replaced by a custom QR code display (similar to how Shields did their mint). Aside from rpc in both, an alternative option could be a custom connector with its own id that is meant for the QR code override (so that this is the connector that is cached/restored). Let me know if you have any ideas/suggestions for a better approach!

---

**jamierumbelow** (2022-05-10):

> Would love to chat more if you are so inclined, I think defining a new web3 provider may be warranted, especially with how state is handled currently.

It’s definitely worth exploring a new provider – if only for inspiration – but I think there’s still plenty of low-hanging fruit to pick before we need to make such drastic changes. (For one thing, getting dapps to opt-in to a non-backwardly-compatible provider API is going to take time and effort.)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sbacha/48/4661_2.png) sbacha:

> Wallets MUST NOT reject the switch to the new RPC Provider URL if the ChainID is known to the
> wallet for no non-error reasoning.

Does the wallet need to know the `chainID` in order to support the RPC URL? One benefit to raising the status of the RPC URL to first-class, as in this proposal, is to detach the `chainID` entirely and allow it to vary independently (as it does in practice.)

I’d suggest instead:

> Wallets MAY display a warning if the chainID is not known to the wallet. Wallets MUST NOT reject the switch to the new RPC Provider URL if the chainId is not known.

---

**ligi** (2022-05-10):

Thanks for the proposal - but it feels wrong to me. I think it would be cleaner that wallets stop proxying the RPC for the dapps - but only sign with the keys they have access to (also going more to the unix philosophy of " Do One Thing and Do It Well"). Then the dApp directly talks to the RPC they want. So also instead of using `eth_sendTransaction` they use `eth_signTransaction` + `eth_sendRawTransaction`

So this proposal feels like trying to work around an issue that should not exist in the first place and introduce complexity this way.

Also open questions in this area:

- what is if no RPC is used but light clients (really hope after the merge they finally get used)
- should it only change in context of the dapp that was requesting or globally? If globally I see some scenarios that could be exploited. Unfortunately currently there is a lot of trust in these RPC providers. E.g. changing the RPC for chainID 1 and then the RPC provider could fake ENS resolutions to their own addresses …

---

**sbacha** (2022-05-10):

I 100% agree, the whole idea of browser extensions, etc, is terrible UX.

The unix philosophy is in its own merits a worthwhile aspiration, however even unix has abandoned that approach. Look at Metamask snaps, the exact opposite is happening with Wallets.

The real issue is primarily the fact that wallets immediately broadcast transactions that are signed. I understand the reasoning behind this but that is really the issue here. Users have no control in how there transaction is broadcasted,  and that sort of meta data to me at least is worrisome from a privacy standpoint and a censorship standpoint.

The point of a malicious endpoint being used is sort of mute. Metamask for example does an out of band verification using etherscans API to cross check the RPCs reported responses.

Additionally, this method would enable a failover safe guard for when current RPC provider is having issues, etc, in a potentially automated manner.

Very interesting point wrt to light clients. Lets go a step further and go to thin clients, basically an RPC assisted light client ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**ligi** (2022-05-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sbacha/48/4661_2.png) sbacha:

> The real issue is primarily the fact that wallets immediately broadcast transactions that are signed.

this needs to be addressed. Wallets should only broadcast transactions that are issued with `eth_sendTransaction` but never transactions with `eth_signTransaction` - I would consider it a (possibly dangerous) bug otherwise. Maybe we should find a way to put wallets on a pillory that misbehave here. I just recently heard from [@pedrouid](/u/pedrouid) in a call that some wallets misbehave here - and was really shocked - was also a problem for a new feature we do for the [pretix eth payment provider](https://github.com/esPass/pretix-eth-payment-plugin) currently. IMHO we should try fix the problem of wallets misbehaving instead of working around it.

---

**hboon** (2022-05-11):

[@sbacha](/u/sbacha) `wallet_switchNetworkRpcProvider` seems to overlap a lot with [wallet_switchEthereumChain](https://eips.ethereum.org/EIPS/eip-3326) and [wallet_addEthereumChain](https://eips.ethereum.org/EIPS/eip-3085) which is already implemented and used by some wallets and dapps

Is it possible to use `wallet_addEthereumChain` and/or `wallet_switchEthereumChain` instead? If not, why not?

---

**izayl** (2022-05-12):

[@hboon](/u/hboon) you can check the [Motivation](https://ethereum-magicians.org/t/eip-wallet-switchactiverpcprovider/9142#motivation-3) section

`wallet_switchEthereumChain`  and [wallet_addEthereumChain](https://eips.ethereum.org/EIPS/eip-3085) resolve make dapp can add/switch chain automaticly, but can not resolve the single-point failure, e.g. Infura provider

there are more scene can use this rpc, like:

1. with defi dapp, give user a option to use flashbot as provider to send transaction for protect
2. for test purpose, temporary toggle to forked network to debug transactions

and more.

---

**jamierumbelow** (2022-05-12):

Thank you for an important contribution to this discussion. I thought I’d respond to the point about light clients in particular; I’ll leave it to others to make the more general case for this method.

I’m also excited about the potential shift post-merge toward light clients. However, a large number of users will, for legacy reasons, continue to use wallets that depend upon RPC nodes. Further, the wallet interface is often used as conduit for `evm_call`s to `view` functions.

A method such as the one suggested here – especially in concert with [my ancillary proposal](https://ethereum-magicians.org/t/adding-rpcurl-to-chainchanged-event/9012) – will enable us to further detach the wallet, RPC node, and interface from one another. Right now, due to ambiguities in the spec, they are far too complected; the wallet/RPC state is shared across the three components implicitly rather than explicitly. Adopting these proposals will help wallets become more independent, not less.

---

**sbacha** (2022-06-08):

Just providing an update:

There is now this additional EIP that has been proposed which is very relevant:

https://github.com/ethereum/EIPs/pull/5139

and a somewhat related EIP proposal:

https://github.com/ethereum/EIPs/pull/5094

I have created issues that will be resolved before submission, including:

https://github.com/manifoldfinance/wallet_switchNetworkRpcProvider/issues/14

https://github.com/manifoldfinance/wallet_switchNetworkRpcProvider/issues/15

Additionally, I will rework the EIP proposal to be less verbose. Any feedback is most welcomed and I appreciate all the comments so far!

---

**sbacha** (2022-07-27):

so only `eth_sendTransaction` should broadcast immediately? `eth_signTransaction` should not, correct?

---

**ligi** (2022-08-03):

yes - correct

eth_signTransaction should not broadcast at all - just sign

