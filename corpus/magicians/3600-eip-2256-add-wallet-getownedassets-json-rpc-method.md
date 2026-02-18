---
source: magicians
topic_id: 3600
title: "EIP-2256: Add wallet_getOwnedAssets JSON-RPC method"
author: loredanacirstea
date: "2019-08-29"
category: EIPs
tags: [wallet, eip, json-rpc]
url: https://ethereum-magicians.org/t/eip-2256-add-wallet-getownedassets-json-rpc-method/3600
views: 7004
likes: 28
posts_count: 20
---

# EIP-2256: Add wallet_getOwnedAssets JSON-RPC method

EIP-2256: [EIP-2256: wallet_getOwnedAssets JSON-RPC Method](https://eips.ethereum.org/EIPS/eip-2256)

tl;dr

This is a proposal targeting wallet API standardization: a new JSON-RPC method `wallet_getOwnedTokens`, for retrieving a selection of owned tokens by an Ethereum address, with the owner’s permission.

There are financial dApps that require a list of owned tokens from a user, for various purposes - calculating taxes, selecting customized payment options, etc. Each of these dApps are now forced to keep a list of popular tokens (smart contract addresses, ABIs) and retrieve the user’s data from the blockchain, for each token. This leads to effort duplication and nonoptimal UX where the user is presented with either more or less token options than the user would like - various airdrops, incomplete list of tokens kept by the dApp.

This proposal was already requested [here](https://github.com/ethereum/EIPs/pull/2253#issuecomment-525410506).

## Replies

**loredanacirstea** (2019-08-29):

[@pedrouid](/u/pedrouid), [@ligi](/u/ligi), [@danfinlay](/u/danfinlay), [@lefterisjp](/u/lefterisjp)

---

**ligi** (2019-08-29):

Thanks for the initiative! I think the chainId should also be part of this EIP as users can own tokens on different chains. This might also help us on the path to ETH 2.0. I suggest a chainId field in the response and perhaps also one (optional) in the request to filter for specific chainID(s)

---

**loredanacirstea** (2019-08-29):

Good idea. I added the `chainId` in [132a1e9](https://github.com/ethereum/EIPs/commit/132a1e958976f5409e9abdf6404e7a24aeed01fe).

---

**LefterisJP** (2019-08-29):

Hey Loredana thank you for the initiative! You know I really want this to be standardized ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

Only comment I got is that we perhaps don’t need the optional fields of symbol, name and icon since the first two would be part of the token contract/abi anyway and the icon would be handled by the dapp and would most probably use something like https://github.com/atomiclabs/cryptocurrency-icons

If you really want them then we could go for more of the optional attributes like the decimals e.t.c.

---

**fulldecent** (2019-08-29):

I don’t like this. Tokens are at the application layer and JSON is at the node layer. The node does not know about tokens and it shouldn’t.

Every time a new token standard is proposed (which is monthly) they will want it to be supported by all the wallets. This is too much tight-coupling of systems.

Additionally, I will spam the system by making one million new tokens and airdropping all addresses. The name of the token will be:

> Buy Su Squares at https://tenthousandsu.com

Every person that opens any wallet supporting this proposed approach will have to present these one million spam messages to the human.

The countermeasure to that is of course is a blacklist. Blacklists don’t work. So the end result is exactly the current best practice we have today, whitelisting.

---

**ligi** (2019-08-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> I don’t like this. Tokens are at the application layer and JSON is at the node layer.

[@fulldecent](/u/fulldecent): this is wrong - JSON is not only used at the node layer. E.g. also with things like clef.

---

**rekmarks** (2019-08-29):

I don’t see how your suggested spam attack is any more powerful if this proposal were adopted.

In the MetaMask case, we would - in my assessment - implement this without causing any additional Ethereum node queries. Our wallet already maintains lists of owned tokens and would simply return that.

---

**rekmarks** (2019-08-29):

I think this proposal argues its own case, and all I want is more feedback from dapp devs as to the data they want/need on the response objects.

Re: [@LefterisJP](/u/lefterisjp)’s comment, I’m agnostic about e.g. `name`, `symbol`, and `icon` being optional. I don’t believe they should be required, but other than that, why not?

---

**danfinlay** (2019-08-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> Every time a new token standard is proposed (which is monthly) they will want it to be supported by all the wallets. This is too much tight-coupling of systems.
>
>
> Additionally, I will spam the system by making one million new tokens and airdropping all addresses.

I think this kind of spam attack can be mitigated at the wallet layer, using a token whitelist, which is what MetaMask does today. Just because there is a `getOwnedTokens` method does not mean the wallet needs to scan the blockchain for all tokens.

For similar concerns, at MetaMask we proposed, implemented, and comply with [EIP 747](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-747.md), a method that allows dapps to explicitly ask to list individual tokens in a user’s wallet. We only detect some major known tokens, and we do not autodetect all known tokens, precisely to avoid spammy airdrops.

I would expect `getOwnedTokens` to only return the tokens that a user’s wallet is already tracking, and to not invoke additional scanning of the blockchain.

EIP 747 also is forward-extensible for defining types of assets (it is `wallet_watchAsset`, not `watchToken`), and proposes a schema for defining the asset type.

```auto
provider.send({
  method: 'wallet_getOwnedAssets',
  params: [{
	types: ['ERC20', 'ERC721']
  }]
})
```

Maybe this proposal could also be changed to `wallet_getOwnedAssets`, and allow a `params` object that can specify the types of assets that the app is interested in.

---

**rekmarks** (2019-08-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> ```auto
> provider.send({
>   method: 'wallet_getOwnedAssets',
>   params: [{
>     types: ['ERC20', 'ERC721']
>   }]
> })
> ```

Nice, then the wallet can return an error like (if `ERC721` is not supported):

```auto
{
  code: 4xxx,
  message: 'Asset type not supported',
  data: [ 'ERC721' ]
}
```

---

**ligi** (2019-08-30):

wondering if we should open an upgrade path for chains not covered by EIP155 and change the field to a string and do something like the interchain-registry is doing: https://github.com/interchain-registry/interchain-registry/pull/13

Unfortunately there is no standard to point to yet - but I like the idea of this upgrade path.

---

**loredanacirstea** (2019-08-30):

As [@danfinlay](/u/danfinlay) & [@rekmarks](/u/rekmarks) already said, this proposal targets data already existing on the user’s wallet.

[@danfinlay](/u/danfinlay):

> Maybe this proposal could also be changed to wallet_getOwnedAssets, and allow a params object that can specify the types of assets that the app is interested in.

I agree with `wallet_getOwnedAssets` (it is more general). I will add the type as a parameter. Don’t you think `interface` is more descriptive?

The asset data type should be the same in both EIP-747 & this one. So, what is the reason for using `{ type, options }` instead of `{ type, address, symbol, decimals [, image] }`?

[@rekmarks](/u/rekmarks):

> Nice, then the wallet can return an error like (if  ERC721  is not supported):

I would just return `[]` instead of an error, to avoid error catches that are not related to the user rejecting the request. What do you say? The purpose of the error for `wallet_watchAsset` indeed makes sense.

---

**loredanacirstea** (2019-08-30):

[@ligi](/u/ligi)

I agree on the chainId as string. At least something like EthPM has - [EIP-1123](https://eips.ethereum.org/EIPS/eip-1123) with example [here](https://github.com/ethpm/ethpm-spec/blob/master/examples/wallet/1.0.0-pretty.json#L102).

But yes, probably after such a standard would be final.

---

**danfinlay** (2019-09-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/loredanacirstea/48/2202_2.png) loredanacirstea:

> Don’t you think interface is more descriptive?

It is slightly more descriptive, but EIP-747 is already using `type`, so I’m torn between descriptiveness and consistency.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/loredanacirstea/48/2202_2.png) loredanacirstea:

> So, what is the reason for using { type, options } instead of { type, address, symbol, decimals [, image] } ?

For the sake of forward-extensibility. ERC-20 and ERC721 may have all of those parameters in common, but a `subscription` might have very different features, for example. For this reason, we isolated all of the interface-specific parameters into an interface-dependent `options` object.

---

**loredanacirstea** (2019-09-03):

[@danfinlay](/u/danfinlay),

Based on the discussions up to this point, I made some changes to the PR: [cb6dbea](https://github.com/ethereum/EIPs/pull/2256/commits/cb6dbea8a50b7e34a9730c809c1cac3b584111cd), to be more aligned with EIP-747:

- rename wallet_getOwnedTokens to wallet_getOwnedAssets
- use options in the response field
- use asset instead of token where generalization is needed
- replace interface with type
- add types as a filter field
- add decimals as an optional field in options

If you think this is good enough to be merged as a Draft, please signal this on the PR.

---

**loredanacirstea** (2019-09-06):

This EIP has been merged as a Draft and can now be found at https://eips.ethereum.org/EIPS/eip-2256

The current request proposal, with the optional filter arguments looks like this:

```json
{
  "id":1,
  "jsonrpc": "2.0",
  "method": "wallet_getOwnedAssets",
  "params": [
    "0x3333333333333333333333333333333333333333",
    {
      "chainId": 1,
      "limit": 10,
      "types": ["ERC20"],
      "justification": "Select up to 10 frequently used tokens and we will tell you what services accepted them as payment."
    }
  ]
}
```

[@danfinlay](/u/danfinlay),  regarding the first type of permissions (ongoing) from https://github.com/ethereum/EIPs/pull/2256#issuecomment-527683267:

I imagine an ongoing permission can work with `wallet_getOwnedAssets`:

1. dApp requests ongoing access to all assets and user agrees.
2. dApp requests ongoing access to all ERC20 & ERC721 assets and user agrees.
3. dApp requests ongoing access to all ERC20 & ERC721 assets and user only wants to grant access for some assets. In this case, the wallet needs to remember what assets were chosen. Indeed, a bit more work for the wallet.

---

**danfinlay** (2019-09-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/loredanacirstea/48/2202_2.png) loredanacirstea:

> I imagine an ongoing permission can work with wallet_getOwnedAssets :
>
>
> dApp requests ongoing access to all assets and user agrees.
> dApp requests ongoing access to all ERC20 & ERC721 assets and user agrees.
> dApp requests ongoing access to all ERC20 & ERC721 assets and user only wants to grant access for some assets. In this case, the wallet needs to remember what assets were chosen. Indeed, a bit more work for the wallet.

I think this API is a little clearer if we distinguish two methods, one for ongoing usage, and one that initiates a specific selection.

It might help me imagine how you’re proposing these are compatible by giving hypothetical code for how the extended permission would be granted.

For example, today under the current [wallet permissions proposal](https://github.com/danfinlay/EIPs/blob/WalletPermissions/EIPS/eip-PermissionsSystem.md), any method that hasn’t been granted permission using `requestPermission` would get an unauthorized `4001` error. Would you suggest that some methods, like this, might instead trigger confirmations on each request instead?

I think I slightly prefer them being separate methods, for the sake of a simpler implementation for the wallet, but I understand that an ideal interface should dictate implementation, not the other way around.

Item 3: I think making more-specific attenuations is always a good feature, and wallets could always add this enhancement as they are able to, so it doesn’t need to block the proposal.

---

**VanijaDev** (2022-04-21):

Hello devs,

What’s the status of this issue? Any update?

I tired **wallet_getOwnedAssets** method added to Ethereum EIP - [https://ethereum-magicians.org/t/eip-2256-add-wallet-getownedassets-json-rpc-method/3600/](https://github.com/MetaMask/metamask-extension/issues/url) But I can’t manage get it working through MetaMask. I get error - **MetaMask - RPC Error: The method “wallet_getOwnedAssets” does not exist / is not available**

[![Screenshot 2022-04-21 at 14.24.32](https://ethereum-magicians.org/uploads/default/optimized/2X/b/b619575e22c3ded4449a21ee1b0a0fc9c168497c_2_690x53.png)Screenshot 2022-04-21 at 14.24.323824×296 109 KB](https://ethereum-magicians.org/uploads/default/b619575e22c3ded4449a21ee1b0a0fc9c168497c)

---

**Ardziv** (2022-12-14):

Hi, i am facing the same issue - when trying to use the “**wallet_getOwnedAssets**” I still see it does not exists inside “window.ethereum.requests” API. Can anyone at Metamask team give us a realistic implementation deadline for this long awaited feature?

also what are the other work arounds for now? how do dapp developpers manage to check if a Token is already in the “watchlist” of a user’s wallet? and if it is not then triggering the “**wallet_watchAsset**” methods?

any help would be greatly appreciated thanks.

