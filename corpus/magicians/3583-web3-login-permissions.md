---
source: magicians
topic_id: 3583
title: Web3 Login Permissions
author: danfinlay
date: "2019-08-26"
category: Web > Wallets
tags: [wallet, security, usability]
url: https://ethereum-magicians.org/t/web3-login-permissions/3583
views: 13616
likes: 38
posts_count: 31
---

# Web3 Login Permissions

Hi all, at MetaMask we’ve been working on a new feature proposal for web3 wallets, aimed at  increasing usability while maintaining coherent security. You can read about our motivations in more detail [in this blog post](https://medium.com/p/c55b3d73563f/).

The proposal below is a syndication of [this EIP branch](https://github.com/danfinlay/EIPs/blob/WalletPermissions/EIPS/eip-PermissionsSystem.md) submitted as [this EIP issue](https://github.com/ethereum/EIPs/issues/2255).

---

## eip: TBD
title: Wallet Permissions System
author: Dan Finlay (), Erik Marks ()
discussions-to: TBD
status: Work in progress (WIP)
type: Standard Track
category: Interface
created: 2019-08-22
requires: 1474

[![permission%20system](https://ethereum-magicians.org/uploads/default/optimized/2X/f/f7b2f29144e062e330125526167bc3fa359cd7aa_2_690x237.png)permission%20system2826×973 239 KB](https://ethereum-magicians.org/uploads/default/f7b2f29144e062e330125526167bc3fa359cd7aa)

## Simple Summary

A proposed standard interface for restricting and permitting access to security-sensitive methods within a restricted web3 context like a website or “dapp”.

## Abstract

Web3 JavaScript wallet browsers may implement `wallet_getPermissions` and `wallet_requestPermissions`. This provides a standard interface for requesting permissions and checking a domain’s current permissions status.

## Motivation

Web3 Wallets are built around the responsibility of mediating the interactions between untrusted applications and a user’s keys on their computer, getting appropriate consent from the user.

Today web3 browsers like MetaMask always prompt on a per-action basis. This provides security at the cost of substantial user friction. We believe that a single permissions request can achieve the same level of security with vastly improved UX.

The pattern of permissions requests is common around the web, from login with Facebook, Twitter, Github, and even Apple, making it a very familiar pattern.

![facebook permissions](https://proxy.duckduckgo.com/iu/?u=https%3A%2F%2Fi.stack.imgur.com%2FG7dRV.png&f=1)

[![log in with apple](https://ethereum-magicians.org/uploads/default/optimized/2X/e/e0d20c0faec92acec3e591c957612fd482d9d01a_2_527x499.jpeg)log in with apple584×554 53.1 KB](https://ethereum-magicians.org/uploads/default/e0d20c0faec92acec3e591c957612fd482d9d01a)

Many web3 applications today begin their sessions with a series of repetitive requests:

- Reveal your wallet address to this site.
- Switch to a preferred network.
- Sign a cryptographic challenge.
- Grant a token allowance to our contract.
- Send a transaction to our contract.

Many of these (and possibly all), and many more (like decryption), could be generalized into a set of human-readable permissions prompts on the original sign-in screen, and additional permissions could be requested only as needed.

On the user’s end, each of these permissions could be individually rejected (unchecked), or even *attenuated*, or adjusted to meet the user’s terms (for example, a sign-in request could have a user-added expiration date, and a token allowance could be adjusted by the user when it is requested), making the web3 login a sort of user-revisable terms of use.

## Specification

This proposal adds two new methods to a wallet’s web3 provider API:

- wallet_getPermissions
- wallet_requestPermissions

The `wallet_getPermissions` method is used for getting an array of current permissions (empty by default), while the `wallet_requestPermissions` method is used for an application to request additional permissions.

These two methods are used to restrict a few hypothetical “restricted methods”. The first such method we would suggest should be included as part of the standard is `eth_accounts`.

In this framework, the permission for a user to reveal their accounts would look like this:

```javascript
const response = await provider.send({
  method: 'wallet_requestPermissions',
  params: [{
    'eth_accounts': {},
  }]
})
```

If this request was rejected, it would throw an error with a `code` value equal to `4001`, per [EIP 1193 errors](https://eips.ethereum.org/EIPS/eip-1193), which the MetaMask team has canonized in a module [eth-json-rpc-errors](https://github.com/metamask/eth-json-rpc-errors).

If the request is accepted by the user, then subsequent requests to `eth_accounts` will succeed, and return an accounts array as usual.

A call to `wallet_getPermissions` will then return a permissions schema object that describes the current permission.

```javascript
const response = await provider.send({
  method: 'wallet_getPermissions'
})
```

Would return a value something like this:

```auto
[
  {
    parentCapability: 'eth_accounts',
    caveats: [
      {
        type: 'filterResponse',
        value: ["0x0c54fccd2e384b4bb6f2e405bf5cbc15a017aafb"]
      }
    ]
  }
]
```

The term `parentCapability` comes from the [ocap-ld spec](https://w3c-ccg.github.io/ocap-ld/), which these permissions objects are based on.

You can see above how internally the user-selected account is transformed into a [caveat](https://github.com/MetaMask/json-rpc-capabilities-middleware/blob/master/src/%40types/ocap-ld.d.ts#L28-L33), which is a restriction on the response values, in this case ensuring the page can only be notified of approved accounts. This also means this permissions system is forward-extensible to support logging into a page with multiple accounts.

## Rationale

While the current model of getting user consent on a per-action basis has high security, there are huge usability gains to be had bo getting more general user consent which can cover broad categories of usage, which can be expressed in a more human-readable way. This pattern has a variety of benefits to offer different functions within a web3 wallet.

The `eth_sendTransaction` method itself could be a restricted method (requested by default with the `provider.enable()` method), and the user could at sign-in time decide whether they wanted to require confirmations, approve all transactions, or only approve transactions to a certain contract, or up to a certain token limit, for example. By restricting this method by default, wallets could prevent sites from spamming the user with popups.

If `eth_call` were a restricted method, then random websites would not be able to drain a user’s subscription to a hosted provider, making it easier to protect services like Infura against DDoS attacks.

On-chain actions could be represented as a permission under this model, for example, the permission to send an allowance-setting transaction to a specific token address is virtually equialent to the approval of that transaction, except the site could choose to only invoke the transaction when it was needed. This could allow a standard interface for applications to request permissions which may require different actions depending on different types of accounts (hot wallets, hardware wallets, cold wallets, contract accounts).

The `requestPermissions` method could be expanded to include other options related to the requested permissions, for example, sites could request accounts with specific abilities. For example, a website like an exchange that requires `signTypedData_v3` (which is not supported by some hardware wallets), might want to specify that requirement, maybe like this:

```javascript
provider.send({
  method: 'requestPermissions',
  params: [
    {
      'eth_accounts': {
        requiredMethods: ['signTypedData_v3']
      }
    }
  ]
})
```

That type of API will also be up for discussion on [The MetaMask repository](https://github.com/MetaMask/metamask-extension/issues/6994).

This would allow the wallet to limit the user’s options to valid ones, and allows dapps to ensure selected accounts are compatible with their service, while preserving the user’s privacy regarding how they are storing their keys.

## Implementation

We have [a branch of MetaMask available now](https://github.com/MetaMask/metamask-extension/tree/LoginPerSite) which adds these methods via an [rpc-engine](https://github.com/MetaMask/json-rpc-engine) middleware called [json-rpc-capabilities-middleware](https://github.com/MetaMask/json-rpc-capabilities-middleware) (or often `RpcCap` internally, for short).

The latest build of this branch of MetaMask can be downloaded from [the draft pull request](https://github.com/MetaMask/metamask-extension/pull/7004) (look for the latest post by `@MetaMaskBot`). A guide to adding a custom build of MetaMask to Chrome can be found [here](https://github.com/MetaMask/metamask-extension/blob/develop/docs/add-to-chrome.md).

This branch of MetaMask can be used with [this sample site](https://metamask.github.io/permissions-adventure/) ([source](https://github.com/metamask/permissions-adventure)), which uses a couple sample permissions for demonstration purposes:

- readYourProfile: We have bundled this build with an imaginary concept of a local “profile”, a simple POJO. Eventually this could be extended to instead expose the user’s 3box profile.
- writeToYourProfile: This permission allows the requesting app to freely update/edit the user’s profile.
- sendEther: A permission allowing the sending of transactions.

![sample dapp](https://ethereum-magicians.org/uploads/default/original/2X/5/551dc8c72f5e0eec097c7ff38f666dc6585dfe4a.gif)

It is notable that this branch is the first version of MetaMask that allows you to be connected to each site with a different account, which persists on that site, along with any other permissions granted to the site.

You can get more detailed API and type information [on the RpcCap repository’s readme](https://github.com/MetaMask/json-rpc-capabilities-middleware#rpc-methods).

New hypothetical and proposed permissions can be easily added to [the restrictedMethods hash in the MetaMask permissions controller](https://github.com/MetaMask/metamask-extension/blob/774d931cb9f16a8f2df8c6deee1dd553b40d5ad5/app/scripts/controllers/permissions.js#L187).

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## Replies

**danfinlay** (2019-08-26):

[@wighawag](/u/wighawag) [@pedrouid](/u/pedrouid) [@boris](/u/boris) [@beltran](/u/beltran) [@Ethernian](/u/ethernian) [@ligi](/u/ligi) [@izqui](/u/izqui)

---

**boris** (2019-08-26):

This is great, thanks Dan.

Can we pull out the types of permissions and put them in a repo so we can agree and evolve them, as well as define vendor / dapp specific permissions?

Are these what OAuth2 calls “scopes”?

I think we can get to some Web3 wide permissions, and then enable per dapp / wallet custom ones.

Pinging [@expede](/u/expede) as she plans out our identity work.

---

**danfinlay** (2019-08-26):

> Can we pull out the types of permissions and put them in a repo so we can agree and evolve them, as well as define vendor / dapp specific permissions?

That’s a great idea! Starting a repo here, hopefully we can grow it into something nice.

https://github.com/MetaMask/wallet-permissions-spec

> Are these what OAuth2 calls “scopes”?

These permissions *are* basically equivalent to [OAuth2 Scopes](https://oauth.net/2/scope/).

However, the language of “scope” seems to suggest that a permission has some broad implications, like the `github:repo:write` scope, which includes a variety of permissions bundled under one label.

Taking inspiration from object capabilities, we’re calling them permissions here because we aspire to make the individual items coherent enough that they can result in informed consent when a brief description is read by the user.

---

**Ethernian** (2019-08-26):

I am unsure whether I like the permission idea in general and the permission “send the transaction on your behalf” in particular. Users may be so careless giving permissions… I have a bad feeling re-implementing the usual permission paradigm once more.

The way how are you solving the trade-off  “UX vs Security” by trading UX for Security is much different how I see it. I need more time to think about it. I’ll write then.

BTW, thank you for mentioning me.

---

**danfinlay** (2019-08-27):

> I am unsure whether I like the permission idea in general and the permission “send the transaction on your behalf” in particular. Users may be so careless giving permissions… I have a bad feeling re-implementing the usual permission paradigm once more.

I agree there are scary permissions we could add, and sending transactions is among the top, and so I’m not actually including any transaction sending permission as part of this proposal. That said, I will still defend the possibility of that permission, because I think it’s an important point.

Even today’s “prompt on every transaction” model relies on users mostly trusting the sites they visit, as [most transactions are of unknown types](https://medium.com/metamask/metamask-metrics-fbec0e2ceaa7), and are hard for wallets to represent to users.

For that reason, I think a properly designed permissions system will do a few things to improve the situation:

- Wallets should make dangerous permissions look dangerous. This isn’t an excuse to get users to click blindly. This is a time to rebuild the user’s sense of responsibility.
- Wallets should expose permissions that are meaningful to users. A token allowance is meaningful, but a hex blob is not. If we can identify the terms that convey the true risk a user is taking, I believe we can allow the risks a user takes to be much more comprehensible to them, which allows them to participate in informed consent. We cannot stop users from being reckless, but we can empower them to be careful with fewer steps.
- Wallets should allow users to attenuate permissions (add caveats), or reduce their impact when possible. An app may request a login, but the user may say “Just for the next 30 minutes”.

I imagine you might be thinking about [your Dapplet proposal](https://ethereum-magicians.org/t/dapplets-rethinking-dapp-architecture-for-better-adoption-and-security/2799) as an alternative security measure, but I think it actually could work better together: While we want to render transactions more coherently, there is *a hard question* about who you would trust to design your transaction approvals, so why not make “permission to render confirmations” a permission?

In Dapplets, you suggest a registry, and that the registry could have auditors, and I would suggest that this has [moved the goal post](https://en.m.wikipedia.org/wiki/Moving_the_goalposts), and now the concern is “who are the auditors?”. Rather than prescribe an imperfect solution, we could also just ask the user if they trust a given source for information.

I wish I could keep users safe by restricting functionality, but ultimately users will do extreme things to use applications if it isn’t easy. They’ll just trust the site to make a wallet for them, and they’ll fund it, or paste in a seed phrase. Rather than refuse to implement potentially dangerous APIs, I think it’s important for wallet developers to ask *what APIs allow users to take the risks they want to make*, as coherently as possible?

---

**rekmarks** (2019-08-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> Users may be so careless giving permissions… I have a bad feeling re-implementing the usual permission paradigm once more.
> …
> The way how are you solving the trade-off “UX vs Security” by trading UX for Security is much different how I see it.

I want to add that we do not believe that we are “trading UX for security” in this framework. As we state in the proposal:

> We believe that a single permissions request can achieve the same level of security with vastly improved UX.

Speaking for myself, regarding security, when we adopt this framework, the following statement will remain true:

> Dapps cannot take any action on the user’s behalf without the user’s explicit permission

I maintain that we can implement this framework such that the following is also true:

> The user is extremely unlikely to grant permissions that enable dapps to take actions counter to the user’s intentions

I believe we can accomplish this by:

1. Disallowing “unlimited” permissions for sensitive methods such as eth_sendTransaction

For instance, enforcing some kind of user-specified spending or usage limit.
2. Letting the user maintain existing behavior, with confirmations for every transaction, however small.

Perhaps we even maintain existing behavior for eth_sendTransaction by default.
3. Ensuring that permissions are human-readable through rigorous user research.

To accomplish this, our design team is deeply involved in determining how we present this feature to users.

---

**pedrouid** (2019-08-27):

I love everything about this! This aligns very well with what we wanted to do with “Automatic Authentication Signature” proposal and also with “WalletConnect Session Permissions”.

This design is even better which would be compatible with any web3/ethereum provider ![:raised_hands:](https://ethereum-magicians.org/images/emoji/twitter/raised_hands.png?v=9)

Pinging [@androolloyd](/u/androolloyd) who’s been asking me for ages to do something like this as part of Web3Connect ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=9)

---

**wighawag** (2019-08-27):

Thanks [@danfinlay](/u/danfinlay) for the mention,

Great proposal! I like its simplicity and extensibility

I share [@Ethernian](/u/ethernian)’s concerns though about making it easy for an application to get the ability to send tx at will without further thoughts on this. Even if this is only a potential permission.

While I actually think it make sense to let application send tx at will, we need to differentiate between fully decentralised application, whose front-end code cannot be changed (ipfs hash) and the one that can be updated at will or as a result of being attacked (DNS / ENS based)

**The proposal need to spec out exactly what/who these permissions are given to.**

In several of my post here and on my blog (https://medium.com/@wighawag), I mentioned about the document’s origin and how not all are created equal, how an ENS name should only be used a convenience (to point to an ipfs hash) and not as the canonical origin, etc…

Ideally such origin should always be the content itself. ipfs and swarm provide this mechanism and an ENS/ DNS name should simply be used as a redirection mechanism : they should not be used as origins themselves.

Obviously in the current context, we can’t entirely block such website. But we could forbid giving certain permission to them.

**a permission to send any kind of tx could indeed be given safely to a website hosted on IPFS (but without any mixed content (similar to how browser deal with http content in a website served over https)**

The content of the website could have been audited / reviewed / formally verified and I see no reason to limit their capabilities if users agree too. That’s exactly what i have been pushing for quite some time now : https://medium.com/@wighawag/3-proposals-for-making-web3-a-better-experience-974f97765700

And your proposal is a lot better than recording such permission on the smart contract themselves (as I was proposing)

On the other hand, such permission should not be given if the origin is a DNS domain pointing to a backend url without hash. Similary this permission should not be given to an ENS name, instead it should be given to the ipfs hash the ENS name points to (this way if the ENS name owner change the content, the user are protected)

Alternatively, if this could be possible, the web3 browser could generate an hash of the content and linked content to create the origin itself. DNS would then be simply used as a redirection mechanism.

But this would not work for any application that request data dynamically from non-hashed based data source.

Regarding the “eth_accounts” request, as I proposed in 1102 proposal, Giving permissions to eth_accounts should return a signed request so that the application can be sure the wallet is indeed in possession of the private key without having to make yet another request.

---

**Ethernian** (2019-08-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> I’m not actually including any transaction sending permission as part of this proposal. That said, I will still defend the possibility of that permission, because I think it’s an important point.

If we will put reasonable constraints on permissions, that could be ok.

Although I would put possible UseCases in focus (like gas payments) to check the applicability of the permission paradigm to it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> Wallets should make dangerous permissions look dangerous …

I am not sure, wallet will be able to identify “dangerous permissions” in generic manner because the value of the permitted transaction may be external to the blockchain (like a transfer of a real-world asset).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> I imagine you might be thinking about your Dapplet proposal as an alternative security measure, but I think it actually could work better together:

I am thinking about a convergence of both, not opposition. More details will follow.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rekmarks/48/1626_2.png) rekmarks:

> Dapps cannot take any action on the user’s behalf without the user’s explicit permission

This is exact that I am concerning about and not able understand currently: If some transaction get signed because of some permission is active, than for the transaction itself the user confirmation is implicit (implied) and not the explicit one. Right?

I see the security risk increasing here (because this implication may be correct or not) and do not understand how you don’t.

One more concern:

This protocol assumes bidirectional communication changing its direction many times.

For high security wallets like AirGap utilizing two separate uni-directional channels (Camera + Display) it will not be easy to implement it,

---

**loredanacirstea** (2019-08-27):

I see a difference in:

**1) Method permissions**

- Each method must have a unique identifier - in our case, this is the method name.

**2) Method argument type check and validation**

- Each argument type should be defined in the global scope and must have a unique identifier, so they can be reused across methods, with a custom label (instantiation name). Then, validation rules can also be reused in wallets, web3 libs etc. And custom type UIs can also be reused.

## Example

**1) `eth_sendTransaction` permission:**

```javascript
{
  method: 'wallet_requestPermissions',
  params: [{
    method: 'eth_sendTransaction',
  }]
}
```

**2) `eth_sendTransaction` permission + argument validation:**

First, `eth_sendTransaction` has the following interface:

```javascript
{
    type: 'function',
    label: 'eth_sendTransaction',
    inputs: [
        {
            type: 'address',
            label: 'from'
        },
        {
            type: 'address',
            label: 'to'
        },
        {
            type: 'bytes',
            label: 'data'
        },
    ],
    optionalInputs: [
        {
            type: 'uint256',
            label: 'gas'
        },
        {
            type: 'uint256',
            label: 'gasPrice'
        },
        {
            type: 'uint256',
            label: 'value'
        },
        {
            type: 'uint256',
            label: 'nonce'
        }
    ],
    outputs: [
        {
            type: 'bytes32',
            label: 'transactionHash'
        },
    ]
}

```

If we have standardized interface types, we can have automatic type validation rules & UI components for each method argument on the Wallet UI.

So, the JSON-RPC method can look something like this:

(no need to define types, because they are known by both web3 lib & wallet)

```javascript
{
  method: 'wallet_requestPermissions',
  params: [{
    method: 'eth_sendTransaction',
    params: [
        {
            name: 'from',
            required: true,
            customizable: true,
            selection: ['0x0001'],
        },
        {
            name: 'to',
            required: true,
            customizable: false,
            selection: ['0x0003', '0x0004'],
        },
        {
            name: 'gas',
            required: true,
            customizable: false,
            selection: [0, 2000000],
        },
        {
            name: 'gasPrice',
            required: true,
            customizable: true,
            selection: [1, 5],
        },
        {
            name: 'value',
            required: true,
            customizable: true,
            selection: [0, 100000000000],
        },
        {
            name: 'data',
            required: true,
            customizable: false,
        },
        {
            name: 'nonce',  // can be used for expiration of permissions
            required: false,
            customizable: true,
            selection: [5, 10],
        },
    ]
  }]
}
```

**Where:**

- name: argument name inside the method
- required: true if without it, the entire permission fails.
- customizable: the user can change type validation rules (increase a range, select another account etc.)
- selection: the argument value range / selection list (depends on each type; the wallet will show the appropriate UI for the type)

**Note:**

Permissions on `data` (e.g. how many tokens to approve, etc.) are tricky right now. If the above general mechanism (or similar) will be considered, I have some ideas about how to tackle the `data` problem in a general way, if people are interested.

## Conclusion

I am suggesting:

- general permissions + argument validation based on types for any web3 method; not just on handpicked ones
- a dApp should expose all web3 methods that it will use (calls & transactions)
- the wallet should be able to show the user all the web3 methods that the dApp uses/has used (it can be in the Advanced section, because this can be overwhelming); transparency + the above Infura DDoS example

Very good topic.

---

**danfinlay** (2019-08-27):

> The proposal need to spec out exactly what/who these permissions are given to.

Excellent point, I am surprised I didn’t include this.

Initially, as MetaMask can connect to normal DNS websites, I would use the [same origin](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) identifier, which should include a prefix of the protocol (i.e. `https://dapps.metamask.io`, `ens://danfinlay.eth`, or `ipfs://IPFSHASH`).

I do agree that we could use this opportunity to push developers towards more decentralized protocols, so at MetaMask we are improving the origin detection of our IPFS resolution.

That said, I think loading over an eth address or ENS name would be a powerful tool, because it allows the creation of on-chain update logic.

I can even see the possible benefits of locking permissions to the hash of a page, so that any page update requires a re-authentication. That’s a big usability tradeoff, but has some pretty great security benefits.

> Alternatively, if this could be possible, the web3 browser could generate an hash of the content and linked content to create the origin itself. DNS would then be simply used as a redirection mechanism.
> But this would not work for any application that request data dynamically from non-hashed based data source.

Agreed, I’m not sure it’s even possible for us to dynamically check the hash of a page that is loaded, we’ll have to check that out. Some of these goals are very ideal, but may be less practical in the short term, where we’re still building largely on web 2.0 infrastructure.

> Regarding the “eth_accounts” request, as I proposed in 1102 proposal, Giving permissions to eth_accounts should return a signed request so that the application can be sure the wallet is indeed in possession of the private key without having to make yet another request.

I don’t think all applications require cryptographic proof of key holding, nor do all accounts have a single key that controls them (contract accounts would be unable to sign in under this model!). We’re currently working on a proposal to integrate your `Automatic Authentication Signature` proposal into an additional, optional permission that a dapp could request at its discretion, for when it truly needs to verify a key’s possession.

---

**danfinlay** (2019-08-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> I would put possible UseCases in focus (like gas payments) to check the applicability of the permission paradigm to it.

Could you expand on this example use case?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> I am not sure, wallet will be able to identify “dangerous permissions” in generic manner because the value of the permitted transaction may be external to the blockchain (like a transfer of a real-world asset).

I don’t think we need to do it generically: Some permissions (like `sendTransaction`) are clearly security critical, and probably far too open-ended for most normal usage, and so it should be rendered with an extreme warning. Only if the requested permission is constrained to an extent that we can coherently render it should we laxen our warning. For example, an allowance of a known asset type.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> If some transaction get signed because of some permission is active, than for the transaction itself the user confirmation is implicit (implied) and not the explicit one. Right?
> I see the security risk increasing here (because this implication may be correct or not) and do not understand how you don’t.

Just to re-ground the discussion, this proposal at large is not presenting any “freely send transactions” permission, so it might be best to separate that into a future hypothetical discussion, so we don’t throw out this entire platform just because it could be extended in a dangerous way.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> One more concern:
> This protocol assumes bidirectional communication changing its direction many times.
> For high security wallets like AirGap utilizing two separate uni-directional channels (Camera + Display) it will not be easy to implement it,

This is fair. Signing in with different types of wallets will have different features, so Dapps may need to do some feature detection, and some dapps may only be able to work in some contexts. If an application requires streaming communication (for decryption, for example), it might mean that either it requires a web3 browser or that the wallet phone stays on during the connection.

I think this is an important consideration, and maybe we should add a permissions-feature-detecting API also, so Dapps could ask what permissions are even available. Or maybe feature-detection could be implicit, wherein a response to `wallet_requestPermissions` returns only approved (and available) permissions, which also improves user privacy by never exposing a list of available APIs.

---

**Ethernian** (2019-08-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> I would put possible UseCases in focus (like gas payments) to check the applicability of the permission paradigm to it.

Could you expand on this example use case?

Sorry for using uncommon terms.

I used “gas payments” for per-Tx micro payments for tool and infrastructure usage made in protocol tokens or other non-ETH assets. It could be a per Tx micro payment for using MetaMask, WalletConnect etc. These properties are:

- micro payments, maybe paychannel or other meta Tx.
- related to main Tx

I can imagine a permission for this Use Case. But note, that this permission is use case specific and not generic.

---

**danfinlay** (2019-08-27):

Hi [@loredanacirstea](/u/loredanacirstea), thanks for reading!

I like the idea of strongly-typing the method parameters, but am unclear by what API the wallet would make these available. Maybe that belongs in an additional method? Or should the `inputs` be returned as part of the `wallet_getPermissions` response?

I think the `required`, `customizable` parameters are excellent ideas, and is similar to a use case [suggested just yesterday](https://ethereum-magicians.org/t/eip-2250-gas-price-range/3585/2) by [@tomhschmidt](/u/tomhschmidt).

The `selection` parameter could be encoded as a type of `caveat`, which I think gives us a more open-ended model for defining the constraints on a permission.

One difference in your proposed examples and mine are the use of an array vs an object for defining the requested permissions. My reasoning had been that if permissions have unique names, then no array (or `label` key) is needed, we can iterate unique keys. Is there a particular benefit you see to submitting the requested permissions as an array?

---

**danfinlay** (2019-08-27):

One method that would benefit from a permissions system like this would be encryption/decryption, like [@topealabi](/u/topealabi) proposed with [EIP 1024](https://ethereum-magicians.org/t/eip-1024-cross-client-encrypt-decrypt/505).

At the time, [I had some concerns about how to securely expose such a method](https://ethereum-magicians.org/t/the-ux-of-eip-1024-encrypt-decrypt/1243), but I think this permissions framework gives us a pretty prescriptive path for adding such a method.

---

**danfinlay** (2019-08-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> On the other hand, such permission should not be given if the origin is a DNS domain pointing to a backend url without hash. Similary this permission should not be given to an ENS name, instead it should be given to the ipfs hash the ENS name points to (this way if the ENS name owner change the content, the user are protected)

Maybe this could be a login option:

```auto
- Log me out after X minutes.
- Log me out if this site is updated.
```

---

**loredanacirstea** (2019-08-28):

[@danfinlay](/u/danfinlay),

> I like the idea of strongly-typing the method parameters, but am unclear by what API the wallet would make these available. Maybe that belongs in an additional method? Or should the inputs be returned as part of the wallet_getPermissions response?

These types should not be controlled by an implementation, but agreed on as a standard and kept in a globally available scope. Libraries for transforming them into language-specific types can be built. I suggest using such a system.

For the purpose of defining immutable types that are **reused** across standards, I started [dType](https://github.com/pipeos-one/dType).

> The selection parameter could be encoded as a type of caveat, which I think gives us a more open-ended model for defining the constraints on a permission.

I don’t have anything against this.

> One difference in your proposed examples and mine are the use of an array vs an object for defining the requested permissions.

An object with keys is good, for the reasons that you mention.

---

**wighawag** (2019-08-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> I can even see the possible benefits of locking permissions to the hash of a page, so that any page update requires a re-authentication. That’s a big usability tradeoff, but has some pretty great security benefits.

That’s exactly where I think this should go. Giving permissions (at least the dangerous one like eth_sendTransaction) to anything else could come with a BIG warning to the users but I actually believe we should not even let such applications request it. This is too much risk for the users and too much responsibility for the application owner.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> Maybe this could be a login option:
>
>
>
> ```auto
> - Log me out after X minutes.
> - Log me out if this site is updated.
> ```

if this was the default and any different permission requests was acompagnied with a big warning, this could be an option. At the same time, it is easy to imagine users starting to accept such permission request blindly.

I think as stated aboive some permissions should simply never be allowed on origin that do not encode the full content.

Also if the result of a change was simply being logged out, the user might think they have been logged out for other reason (time based for example). As such we will still need to differentiate between the 2 so users are aware that the content change and that they might be better off waiting before trusting the new content.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> I don’t think all applications require cryptographic proof of key holding, nor do all accounts have a single key that controls them (contract accounts would be unable to sign in under this model!). We’re currently working on a proposal to integrate your Automatic Authentication Signature proposal into an additional, optional permission that a dapp could request at its discretion, for when it truly needs to verify a key’s possession.

Ok, having automatic signature as a permission would work but I still feel that giving the application access to the ethereum address without proving key ownership is potentially misleading.

Obviously for application that only display content associated to an address, there is no need to verify the address is indeed own by that wallet. But at the same time, what would be the risk to let application know that the wallet own the private key by giving out a signed message ?

Actually thinking about it, maybe it is privacy ? Like if wallet allow any user to display themselves as any address, they could potentially be able to see their data without necessarely giving out their address. But I guess some statistical analysis would reveal it in the end (how much time they spend on a specific address?)

Any other reasons ?

---

**danfinlay** (2019-08-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> But at the same time, what would be the risk to let application know that the wallet own the private key by giving out a signed message ?
>
>
> Actually thinking about it, maybe it is privacy ? Like if wallet allow any user to display themselves as any address, they could potentially be able to see their data without necessarely giving out their address. But I guess some statistical analysis would reveal it in the end (how much time they spend on a specific address?)
>
>
> Any other reasons ?

1. Supporting contract accounts, which may not have a single signer empowered to represent them.
2. Support viewing pages in “read-only” mode, maybe viewing from the “perspective” of a cold wallet, with an offline signer.
3. Privacy, plausible deniability, that all makes sense to me.

I don’t think it makes sense to require a feature that is not required for all use cases, and since some use cases cannot provide signatures, I would not want to make them a requirement, especially when adding the feature as an extra permission is so trivially easy.

I would instead ask, is there a good reason that *all accounts must sign* when connecting to an application?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/loredanacirstea/48/2202_2.png) loredanacirstea:

> These types should not be controlled by an implementation, but agreed on as a standard and kept in a globally available scope. Libraries for transforming them into language-specific types can be built. I suggest using such a system.
>
>
> For the purpose of defining immutable types that are reused across standards, I started dType.

Maybe we could encode the ethereum provider as a `dType`. I’ll look closer at that soon!

---

**wighawag** (2019-08-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> I don’t think it makes sense to require a feature that is not required for all use cases, and since some use cases cannot provide signatures, I would not want to make them a requirement, especially when adding the feature as an extra permission is so trivially easy.
>
>
> I would instead ask, is there a good reason that all accounts must sign when connecting to an application?

You are right! I now agree that the best way is to make auto signature (or maybe simply a single signature challenge) another permission for those that need it


*(10 more replies not shown)*
