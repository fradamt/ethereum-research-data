---
source: magicians
topic_id: 22245
title: "ERC-7846: Wallet Connection API"
author: conner
date: "2024-12-17"
category: ERCs
tags: [erc, wallet]
url: https://ethereum-magicians.org/t/erc-7846-wallet-connection-api/22245
views: 725
likes: 21
posts_count: 14
---

# ERC-7846: Wallet Connection API

This proposal defines a new RPC for wallet connection with an emphasis on extensibility. Builds on the notion of optional “capabilities” defined in [ERC-5792](https://eips.ethereum.org/EIPS/eip-5792#wallet_getcapabilities) to add new functionality modularly. This proposal defines one capability to reduce separate interactions for connection and authentication, but otherwise seeks to leave capability definitions open-ended.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/779)














####


      `master` ← `ilikesymmetry:wallet-connection-api`




          opened 03:02AM - 17 Dec 24 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/2/2ed9c3a2fb5b1da29c4ebdb1a6bae789ea99f161.jpeg)
            ilikesymmetry](https://github.com/ilikesymmetry)



          [+233
            -0](https://github.com/ethereum/ERCs/pull/779/files)







This proposal defines a new RPC for wallet connection with an emphasis on extens[…](https://github.com/ethereum/ERCs/pull/779)ibility. Builds on the notion of optional “capabilities” defined in [ERC-5792](https://eips.ethereum.org/EIPS/eip-5792#wallet_getcapabilities) to add new functionality modularly. This proposal defines one capability to reduce separate interactions for connection and authentication, but otherwise seeks to leave capability definitions open-ended.

## Replies

**conner** (2024-12-17):

In this initial draft, I wanted to design without consideration for the status quo set by `eth_requestAccounts`. **Most notably, this thought experiment converged on only returning a singular `account` object instead of an array of them.**

This intuition derives from building many apps in practice and noticing how seldom the batch return is used. Slimming down to a single account by default simplifies how we can leverage results from capabilities and if we want to enable multi-account discovery or connection, that seems feasible to add as its own capability down the line. Especially because the super majority of apps are designed for single-account use cases, multi-account seems to be more aligned as a capability on principle. Definitely expect others to push back on this and am looking forward to finding the optimal DevX here :).

---

**Kames** (2024-12-18):

Overall I really like this approach, especially because it creates space for other authentication methods, besides Sign-In With Ethereum (SIWE), to be adopted in the Ethereum ecosystem.

Personally I want to see 2 other authentication methods explored more deeply.

- Verifiable Presentations using the W3C Decentralized Identifier and Verifiable Credential specifications.
- Zero-Knowledge Proofs using a protocol like Semaphore

Verifiable Presentations would enable more rich/complex user data requests, whether it’s self-attested data like shipping/address information or credentials issued from an organization.

Zero-Knowledge Proof based authentication would allow applications to unlock resources (data and compute) without users having to reveal their full identity to the application.

For example an application might request a proof from that I belong to X group of people (e.x. DAO or unique human protocol) without requiring me to reveal who I am in relation that group.

This can be achieved by presenting a proof, created via the [Semaphore protocol](https://semaphore.pse.dev/), that I belong to a particular group or groups, which than grants me access to privileged offchain resources.

As Vitalik recently pointed out in his “[What I would love to see in a wallet](https://vitalik.eth.limo/general/2024/12/03/wallets.html)” article it’s time for wallets to evolve from only managing private keys, to also acting as personal data hubs.

> Wallets need to become not just software to store onchain access permissions, but also software to store your private data . This is something that the non-crypto world is increasingly recognizing as well, eg. see Tim Berners-Lee’s recent work in personal data stores. All of the problems that we need to solve around robustly guaranteeing control of access permissions, we also need to solve around robustly guaranteeing accessibility and non-leakage of data.

I think Verifiable Credentials/Presentations and Zero-Knowledge Proofs, in relation to wallet authentication, are the perfect medium for advancing that mission, while also being relatively low-stakes.

---

**Kames** (2024-12-19):

[@conner](/u/conner) one thing that is still unclear to me is how applications use the `wallet_getCapabilities` if the intention is to combine the `connect` and `authenticate` requesst into a single call?

If the application doesn’t have an established connection with the wallet, how can they request the capabilities to know what authentication methods is available to them?

---

**jxom** (2024-12-19):

Forwarding GitHub comments:

**Multiple Connections**

Speaking on behalf of the larger Wagmi consumers, I would really appreciate if this supported multiple Accounts.

While the point of “By constraining the account return to a single address, this ERC simplifies developer experience while still supporting richer capability results.” is made, I don’t really see how supporting multiple accounts with their capabilities really degrades developer experience as 99% of the time applications will be using developer tooling that abstracts over these JSON-RPC methods (ie. Wagmi Connectors, etc).

Even if no developer tooling existed, I still don’t think DX would be degraded as applications could just use the first item in the array anyway, and ignore the others (this was Wagmi behavior pre-v1). In fact, user experience would be moreso degraded as users would have to

their current account, and then connect their other account" to achieve previous behavior.

I think capabilities per-account also makes sense, because you wouldn’t really be able to specify fine-grained capabilities (per-account) in the request anyway, so it would always be Should this just be an array of supported chains? Consumers can use `wallet_getCapabilities` to extract capabilities from a Wallet.implied that it is batched across all accounts (for example, a SIWE signature for each account).

**supportedChainsAndCapabilities**

Should the response of `wallet_connect` just return an array of `chains` instead of chains and capabilities (`supportedChainsAndCapabilities`)?

I wonder if it makes sense to omit the assumption that a Wallet “should” be connected to obtain it’s capabilities in ERC-5792 while it’s still in review because this limits the capabilities we can pass to `wallet_connect` if we don’t even know what capabilities the wallet supports (this is Kames’ point).

---

**conner** (2024-12-19):

Thanks for the extension idea! I would normally bucket ideas like this into adding new capabilities, but this flavor of privacy may imply not returning the account address entirely.

Pragmatically, all subsequent wallet RPCs require having access to the wallets address (e.g. signing & transacting). I think the “prove I’m in X group” may be better fit for a paradigm outside of connection if the intent is to maintain privacy of the account address. I’ve noticed a growing pattern  of needing the wallet to sign things in absence of a standard connect flow and this may be a better fit for that. For example wallet_proveMembership could just not require pre-existing connection and would return a address-concealing proof.

---

**conner** (2024-12-19):

Good call out. In talking with [@jxom](/u/jxom) we think we may have to just rely on try/catch here and fallback to eth_requestAccounts. Being the initial request in most cases, we may just need to require a hard upgrade to wallets/apps to get this support.

---

**Kames** (2024-12-19):

I think you’re right in saying that a `wallet_proveMembership` request would make sense for the specific example I provided, but I shared those examples more with the intention of highlighting the fact this ERC appears to be opening the door for a “Wallet 0Auth Standard”.

> Current standards like eth_requestAccounts and personal_sign lack extensibility and require separate interactions for connection and authentication. This results in added complexity for both users and developers. A unified and extensible RPC can enhance user experience, simplify development, and prepare for increasing sophistication in wallet interactions.

IMHO would be a missed opportunity to not have this ERC become the defacto “Wallet 0Auth” experience that supports read/write permission scopes in the form of verifiable credentials and zero-knowledge proofs during wallet authentication.

It’s possible I am barking up the wrong tree though, and it doesn’t make sense to think about a Wallet 0Auth type experience in relation to ERC-7846, in which case I am happy to drop the issue… but based on the stated motivations, it does seem like it’s the right one?

---

**conner** (2024-12-20):

I align with the intuition of this being an onchain-native form of OAuth. Ideally we can make one standard that is sufficiently modular to extend into the future without being overly general and lose clear utility. The only thing that comes to mind if concealing addresses is desirable is for the return address to be optional, but require capabilities to explicitly define if they do not wish to have an address return. This may mean such capabilities will not be able to combine with other capabilities that require an address return. Curious if you have any tangible recommendaations to alter the current interface or if this would suffice?

---

**conner** (2024-12-20):

After thinking it over, I am aligned with accepting a multi-account return! I think improving the path to backwards compatibility to `eth_requestAccounts` is also important for practically getting this adopted.

As for returning `chains` instead of also nesting the capabilities, I’m open to removing this interdependency.

I would note that 5792 explicitly mentions the [privacy risks](https://eips.ethereum.org/EIPS/eip-5792#privacy-considerations) of sharing capabilities pre-connection:

> This method SHOULD return an error if the user has not already authorized a connection between the application and the requested address.

I’m not sure if declaring chain support on its own is entirely useful if it can be inferred from the capabilities return. I’m leaning on removing the chain props from both params and result for brevity and we can decide to add it back in later if others find it vital. My intention with including capabilities in the result by default was to remove the need to request it in isolation as every app should fetch capabilities to know what functionality they have to work with.

---

**greg** (2024-12-30):

I really like what’s trying to be done here; as [@Kames](/u/kames) mentioned, it opens the door for many other forms of authentication.

There is a UX issue that gets exposed by bundling, which, IIRC, is actually why it hasn’t been bundled before.

Not every user has the ability to sign a message at time of `connect,` specifically those:

- Who are using a hardware wallet
- Safe accounts that require multiple signatures to sign a message

It’s valuable from a product perspective to ensure you don’t churn out users early, and as a user, you should be able to view the app from the state of your wallet, even if you don’t sign-in. More concretely, if I want to see that running rates of my NFTs on opensea, I shouldn’t have to sign-in to see my portfolio. The caveats:

- You’re displaying sensitive data
- You’re about to perform an action

I’d worry that this gets abused pretty quickly and becomes the de facto way of connecting to an app which basically.

Wondering if it would make sense to have a boolean to dictate if a capability is required. Might make more sense to actually bake this into 5792, but you could do something like:

```auto
type WalletConnectResult = {
  accounts: {
    address: `0x${string}`; // connected account address
    required: Record;
    capabilities: Record; // results of this connection request's connection capabilities
  }[]
}
```

---

**pedrouid** (2025-01-08):

While I understand the motivation for creating EVM-specific standards for Wallets… there is nothing new or extra that ERC-7846 provides that isn’t already covered by CAIP-222



      [Chain Agnostic Improvement Proposals](https://chainagnostic.org/CAIPs/caip-222)





###



Chain Agnostic Improvement Proposals (CAIPs) describe standards for blockchain projects that are not specific to a single chain.










Why restrict such an important pattern like “Connect + Sign” to only EVM wallets?

---

**glitch-txs** (2025-01-09):

Seconding Pedro here, I think the agnostic approach will give, even for EVM only, a more flexible way to support different methods. Nowadays, most wallets and a lot of dapps are multichain. If, adopting an agnostic approach (that will reduce the workload for developers), doesn’t impact the DevEx or UX of the implementation, I think it would be a good idea to integrate it to this EIP.

EDIT: I mixed the CAIPs, I think this could be more aligned with CAIP-300



      [github.com/ChainAgnostic/CAIPs](https://github.com/ChainAgnostic/CAIPs/pull/300)














####


      `ChainAgnostic:main` ← `lukaisailovic:main`




          opened 10:47AM - 28 Jun 24 UTC



          [![lukaisailovic](https://avatars.githubusercontent.com/u/23192278?v=4)
            lukaisailovic](https://github.com/lukaisailovic)



          [+192
            -0](https://github.com/ChainAgnostic/CAIPs/pull/300/files)







This CAIP defines a JSON-RPC method to request a batch of RPC methods to be reso[…](https://github.com/ChainAgnostic/CAIPs/pull/300)lved when connecting a wallet in a single roundtrip.












Additionally, I would also like to request to add **support for transaction requests** and not only authentication methods. This could simplify even more the user flow when interacting with some dapps.

---

**johanneskares** (2025-07-21):

I’d suggest to make it optional for wallets to have the address be part of the signed message.

E.g. this would be a valid response.

```auto
website[dot]com wants you to sign in with your Ethereum account.

Sign in with Ethereum

URI: uri[dot]com
Version: 1
Chain ID: 8453
Nonce: 3c8777590866fd36b2f92f6839406817
Issued At: 2025-07-21T14:45:22.944Z
```

Base Account (former Coinbase Smart Wallet) still faces the issue, that you need 2 passkey authorizations for signup. One for creating the passkey (derives the address) and one for signing the SIWE message (includes the address). If the wallet is not forced to return the address as part of the message, it could do both steps in one.

