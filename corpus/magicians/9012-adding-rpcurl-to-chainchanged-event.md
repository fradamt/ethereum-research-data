---
source: magicians
topic_id: 9012
title: Adding rpcURL to `chainChanged` event
author: jamierumbelow
date: "2022-04-22"
category: Magicians > Primordial Soup
tags: [json-rpc]
url: https://ethereum-magicians.org/t/adding-rpcurl-to-chainchanged-event/9012
views: 905
likes: 2
posts_count: 1
---

# Adding rpcURL to `chainChanged` event

I’d like to discuss drafting a new EIP to extend the JavaScript provider API, adding the current RPC URL in use by the user’s wallet to the JavaScript provider.

### Context

I’m currently building a local staging environment for product-level manual and automated testing of dapp frontends.

One important piece of this environment is running tests on a forked version of mainnet, hosted internally for internal use.

[EIP-1193](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1193.md) defines a `chainChanged` event to be emitted when connecting to a new chain. This event is emitted with exactly one parameter, the `chainId` of the corresponding chain.

One limitation with the existing provider API is that there is currently no way for a frontend to detect which RPC URL is in use relative to some chainId. Frontends are expected to map chain IDs to appropriate RPC nodes by listing them explicitly, for example:

```auto
type ChainId = number;

type NodeURL = `https://${string}`;

const nodes: Record = {
    1: "https://eth-mainnet.alchemyapi.io/v2/[KEY]",
    137: "https://polygon-rpc.com",
    42161: "https://arb1.arbitrum.io/rpc",
    31337: "http://localhost:8000",
}
```

…and so on.

In some, but not all cases, `chainId` implicitly encodes information about what the URL might be. In particular, chain ID 31337 indicates this is a local network, and is likely to be hosted on `localhost`.

In all cases, however, there is no ability to deduce the RPC URL from the `chainId` directly (except in some cases in extremis, where, e.g. there is only one hosted node for some nascent network.)

There is therefore no connection between a *frontend* application (hereafter ‘Frontend’) and the node (hereafter ‘Node’) – and therefore, in some cases, chain – to which the user is connected via her wallet (hereafter ‘Wallet’).

### Problem

This independence of Node between Frontend and Wallet allows the user potentially to break Frontend by switching Wallet to a new Node connected to a different network but the same `chainId`.

For many production use-cases, this doesn’t cause a problem, since the state is synchronised via the EVM. Frontend talks to Alchemy, Wallet talks to Infura, and any state changes effected by Wallet get propagated through the network and read by Frontend A.

However, for local environments, this lack of RPC URL synchronisation between Frontend and Wallet means that when switching to a locally-hosted Node – hosted through, for instance, a call to `hardhat node --fork` – Wallet and Frontend can execute code in different, isolated environments.

Not only is breaking Frontend for reasons independent of Frontend’s code bad *per se*, but if a developer wishes to allow switching to new node URLs she needs to:

- add some scaffoldable network-switching UI to her application, and
- force the user to update the URL in two places, for both Frontend and Wallet.

This feels like an excellent opportunity to standardise a small piece of Frontend’s UI through a simple technical change.

### Potential Solution

An attractive solution might be to allow Wallet to emit the current RPC URL used when switching between networks.

Technically, this would involve changing the event signature of `chainChanged` defined in EIP-1193 to include the URL:

```typescript
Provider.on('chainChanged', listener: (chainId: string, rpcURL?: string) => void): Provider;
```

`rpcURL` is typed as `string | undefined` for two reasons:

- Backward-compatibility with existing the JS Provider API described in EIP-1193; a new function argument is an accretive change
- Offer a privacy off-ramp to Wallet, allowing the user to hide Node from Frontend’s execution environment if she wishes

Frontend can then parameterise the URL it uses to connect to Node, subscribe to `chainChanged` as before, and update the RPC URL when the wallet changes.

### Discussion Points

I’m not confident that this doesn’t introduce new attack vectors, nor that it will be useful beyond the sort of use case highlighted above.

But it strikes me as a small, backward-compatible change to the existing JS provider API that would improve the user experience and operations of testing environments like mine.

It would also allow further decoupling of frontends from centralised node providers such as Alchemy and Infura, allowing users to opt-out of sending their transactions through such providers and instead offer a standardised way for users to connect to their own hosted nodes, or some other preferred node provider.

(This might, inter alia, partially address the sorts of concerns around infrastructure centralisation made in the recent [Moxie Marlinspike](https://moxie.org/2022/01/07/web3-first-impressions.html) post.)
