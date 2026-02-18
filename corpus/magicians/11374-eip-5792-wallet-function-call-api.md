---
source: magicians
topic_id: 11374
title: EIP-5792 - Wallet Function Call API
author: moodysalem
date: "2022-10-18"
category: EIPs > EIPs interfaces
tags: []
url: https://ethereum-magicians.org/t/eip-5792-wallet-function-call-api/11374
views: 8318
likes: 43
posts_count: 64
---

# EIP-5792 - Wallet Function Call API

Thread to discuss [EIP-5792](https://eips.ethereum.org/EIPS/eip-5792)

## Replies

**moodysalem** (2022-10-18):

Re [@SamWilsn](/u/samwilsn):

> I don’t like this design. It doesn’t force interoperability between wallets. A bundle created with WalletA may or may not be usable with WalletB. I would suggest either:

I might be misunderstanding the comment, but I don’t think interoperability between wallets of a specific bundle identifier is a specific goal of this (that is, if you have both Rainbow and Metamask with the same EOA imported, you should not expect dapps to have consistent transaction UX between connections of the two). It is assumed that each wallet will have its own address that has its own namespaced bundle identifiers

---

**SamWilsn** (2022-10-18):

Nope, you’re understanding it correctly. If I have an EOA today, I can freely switch between wallet applications with no drawbacks. As a user, I can’t support a standard that restricts that freedom (though as an EIP Editor, I can’t stop the proposal.)

Is it that difficult to standardize bundle identifiers?

---

**moodysalem** (2022-10-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> As a user, I can’t support a standard that restricts that freedom

I agree that users should have mobility of their EOA between wallets. Both wallets should be able to import previous transaction history based on just the account.

For dapp interfaces, e.g. Uniswap interface, this EIP should have no impact on the transaction history UX as long as you don’t connect to a different wallet with the same address while a transaction is still pending. It seems like an edge case for a user to switch wallets for the same EOA while an interaction is pending.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Is it that difficult to standardize bundle identifiers?

It would not work for the dapp to specify the identifier for the bundle, because that could only be stored in the connected wallet, and would not sync between apps.

You could use the hash of the message bundle, but when switching from wallet app A to wallet app B, wallet app B won’t know the preimage of the bundle and cannot query it from anywhere (i.e. it cannot query it from a JSON RPC as it can do with a transaction hash).

---

**SamWilsn** (2022-10-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/moodysalem/48/4982_2.png) moodysalem:

> It seems like an edge case for a user to switch apps for the same EOA while an interaction is pending.

I use a different mobile wallet from my browser wallet. I don’t think it’s that inconceivable.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/moodysalem/48/4982_2.png) moodysalem:

> It would not work for the dapp to specify the identifier for the bundle, because that could only be stored in the connected wallet, and would not sync between apps.

Could it not be embedded in the bundle itself?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/moodysalem/48/4982_2.png) moodysalem:

> You could use the hash of the message bundle, but when switching from wallet app A to wallet app B, wallet app B won’t know the preimage of the bundle and cannot query it from anywhere (i.e. it cannot query it from a JSON RPC as it can do with a transaction hash).

Hm, and I guess the bundle might not have a `tx.origin` of the EOA itself (say for 4337 style bundles.) We are defining a new standard here, so we *could* make a new RPC endpoint on clients that deals with transaction bundles, if you’re interested in going that route.

---

**moodysalem** (2022-10-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I use a different mobile wallet from my browser wallet. I don’t think it’s that inconceivable.

In this case you’re using two different browsers, so the dapp doesn’t remember your transaction across the two contexts anyway–it’s stored in the `window.localStorage` for Uniswap interface, which isn’t synchronized across devices.

> Could it not be embedded in the bundle itself?

Yes, you can put the dapp-selected identifier in the bundle, but that bundle + ID is not synced to other wallets, so other wallets won’t know what function calls that dapp-selected bundle identifier corresponds to when queried about bundle status.

> Hm, and I guess the bundle might not have a tx.origin of the EOA itself (say for 4337 style bundles.) We are defining a new standard here, so we could make a new RPC endpoint on clients that deals with transaction bundles, if you’re interested in going that route.

I think this is purely a wallet JSON RPC method; it requires no P2P networking and no information about the state of the network. It’s just giving the dapps a better way to communicate with wallets about bundles of function calls that actually represent an action (e.g. approve and swap) rather than individual transactions.

---

**sbacha** (2022-11-01):

why no GraphQL support?

---

**rmeissner** (2022-11-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Is it that difficult to standardize bundle identifiers?

I would also add that the fact that smart contract wallets would handle differently to eoa based wallets might make this even harder.

for example for an eoa a bundle of multiple calls might result in multiple transactions, but for most smart contract based wallets that would only be 1 transaction. But for most smart contract based wallets the tx hash is calculated differently (e.g. the Safe uses a EIP-712 based hash). All of this makes it harder to create a standard for the bundle identifier.

Harder doesn’t mean impossible, but I don’t think it is necessary for this EIP and could be handled in a follow up EIP to this one.

---

**rmeissner** (2022-11-01):

Just as a general reference:

There has been a similar proposal with discussion that can be found [here](https://ethereum-magicians.org/t/add-wallet-methods-to-improve-dapp-to-wallet-interaction/1848)

---

**rmeissner** (2022-11-01):

Also could you elaborate why “function call” was used for the rpc name? For me “call” implies a non-state-changing operation, which is kind of confusing for this rpc.

---

**moodysalem** (2022-11-03):

Open to name suggestions, just gave it the best name I could think of that wasn’t overloaded (message is too ambiguous, bundles sounds like flashbots and needs qualifiers) but I think `call` is not usually meant as `staticcall` in most contexts.

Separately, I’m slightly concerned with the additional ‘optional’ qualifier in the current specification, perhaps that should be handled at the smart contract level. And anything more complex also, e.g. a dependency graph of function calls, should be expressed in the function that is called.

---

**rmeissner** (2022-11-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/moodysalem/48/4982_2.png) moodysalem:

> but I think call is not usually meant as staticcall in most contexts.

Agree that this is the semantic on contract/evm level. My comment was more related to RPC level (e.g. `eth_call` vs `eth_sendTransaction`). I mean in the end it is just a name … so not the most important thing :P.

The only thing that for me in the name is important (and already is the case) is the `wallet_` namespace ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

Personally I think there are 2 important points to push this EIP forward:

1. Get the right people involved

- Wallet developers (e.g. add MM, Rainbow and Argent)
- SDK developers (e.g. WalletConnect, Ethers, Web3js and co)
- Some dapp developers (i.e. CowSwap and 1Inch are quite cooperative)

1. Align on the return type

- As mentioned before, I don’t think all the details have to be listed here, but I think it makes sense to have a plan how to move this forward. There will be many devs asking the same questions as @SamWilsn.
- I think a uri schema based id would make sense. E.g. safe:tx: or evm:tx:. This way it is easy to extend this (can be defined in separate EIPs) and could even be backwards compatible.

---

**zemse** (2022-11-14):

What is the best way to know whether the connected wallet supports batching? I assume it will need a try-catch based on the following text in the EIP.

> Three new JSON-RPC methods are added. Dapps may begin using these methods immediately, falling back
> to eth_sendTransaction and eth_getTransactionReceipt when they are not available.

Knowing in advance whether a wallet supports batching can enable the frontend to show different UI. E.g. if batching not supported, Uniswap’s frontend shows both “Approve” and “Swap” buttons, but if wallet supports batching, just a “Swap” button can be shown.

What should be the behaviour of `wallet_sendFunctionCallBundle` with empty calls array? Would it fail or provide an id? (For check if RPC method is supported by wallet).

---

**rmeissner** (2022-11-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zemse/48/2748_2.png) zemse:

> Knowing in advance whether a wallet supports batching can enable the frontend to show different UI

I agree. It probably makes sense to have a separate rpc to get wallet capabilities. This could also be used for other rpc methods (e.g. related to signing; does a wallet support eip-712, etc.).

Should this be part of this eip or would it make sense to create a separate one for that?

---

**moodysalem** (2022-11-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rmeissner/48/643_2.png) rmeissner:

> Should this be part of this eip or would it make sense to create a separate one for that?

I would vote separate as it needs to support this and other RPCs, but also shouldn’t be specific to wallets. Could just be a generic JSON RPC introspection endpoint, maybe returning an [OpenRPC](https://open-rpc.org/) compliant response. I’ve also had cases where I was curious whether a particular RPC endpoint supported an RPC (e.g. `eth_getProof` support is not well documented)

But until such an endpoint exists, I think it’s a good carrot for adoption for dapps to just call `eth_sendTransaction` multiple times in its error handler. If dapps have to support different flows depending on wallet implementation, you still end up with the complex branching in the (single digit number of) dapps that support batch transactions for account abstracted wallets today. However this might break existing wallets if one call is required by a subsequent call, as the second `eth_sendTransaction` may be expected to fail without accounting for the first.

---

**moodysalem** (2022-11-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zemse/48/2748_2.png) zemse:

> What should be the behaviour of wallet_sendFunctionCallBundle with empty calls array? Would it fail or provide an id? (For check if RPC method is supported by wallet).

`calls` has a `minItems` of 1, implying that this should revert as a request validation error.

---

**SamWilsn** (2022-11-16):

I’d really like to see an option to specify the atomicity level of a bundle.

For example:

- "atomicity": "none" → Stop on first failed operation. Operations successfully executed so far MUST NOT be reverted.
- "atomicity": "loose" → If any operations fail, none of the operations should happen (they should either revert or not appear on-chain.) This could be implemented for EOAs with flashbots. May lose atomicity in the face of reorgs.
- "atomicity": "strict" → If any operations fail, all operations MUST either revert or never appear on-chain. Must remain atomic in the face of reorgs.

If the wallet is unable to satisfy the requirements, it should fail the RPC request with a well known error.

---

**dror** (2022-11-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> "atomicity": "strict" → If any operations fail, operations MUST revert

This mode is possible when working with contract wallets, but not with EOA.

For this API to be usable, it should have broad support for different wallets.

Also, a helper library (e.g. a wrapper provider) should be provided to provide this API on top of existing wallet API.

This provides both a reference implementation, and also an easy way for apps to work with providers whether they support the new API or not.

---

**SamWilsn** (2022-11-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dror/48/2438_2.png) dror:

> This mode is possible when working with contract wallets, but not with EOA.

Exactly. Wallets that don’t support a particular atomicity level should fail the RPC request.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dror/48/2438_2.png) dror:

> For this API to be usable, it should have broad support for different wallets.

While I don’t disagree with you, I think for this API to actually get used in dapps, it needs to offer more than what you can do with plain JSON-RPC batching. I don’t think “indicating to users that a batch of operations is logically a single chunk” is enough for dapps to write custom code for it.

Pretty sure `"atomicity": "strict"` is already supported in smart contract wallets today though, so it would be nice to expose to dapps in a consistent way. It’s possible to add support for this to EOAs as well, so if something like that ever happens, they’ll be able to implement this too.

---

**yoavw** (2022-11-16):

I second [@SamWilsn](/u/samwilsn) on `"atomicity"`.  It makes sense for the dapp to specify whether it’s a nice-to-have batching for saving gas (so `none`), frontrunning/sandwiching protection (that would be `loose`), or an actual security reason (`strict`).

Most contract wallets, whether 4337 or not, as well as wallets using an EIP 3074 invoker, can support all three (and in practice they’ll always provide `strict` because they’ll batch everything to a single transaction).

EOAs would return an error if `strict`, use Flashbots (or any other trusted mev-boost building service) for `loose`, and normal mempool transactions for `none`.

Dapps should only use `strict` when there’s a real reason, since some wallets won’t support it.

As for communicating the identifier when switching wallet (or using a 3rd party explorer to look at the bundle), I wonder if it would make sense to encode it on-chain in the 1st transaction of there’s more than one.  One byte of calldata may be enough.  Contract wallets will always use one transaction, so no need to encode anything.  If `from` is an EOA, then we can assume consecutive nonces and therefore we only need to know the number of transactions in the bundle.  A uint8 appended to calldata of the first transaction should be enough for all practical purposes.

The 2nd wallet will then decode the 1st transaction, parse the redundant byte, and check for the next N-1 transactions (either on-chain or in mempool).

The caveat (aside from paying gas for the additional calldata byte) is that the 2nd wallet can only parse it if it knows the call’s signature so that it can identify the appended byte as a non-parameter.

I’m not sure it’s worth the hassle, and adding an on-chain component (however small).  Just seems like an easy way to identify bundles across wallets.

---

**moodysalem** (2022-11-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Dapps should only use strict when there’s a real reason, since some wallets won’t support it.

My concern with the `atomicity` feature is that dapps will build things with this API that only work for the `strict` level of atomicity, which is bad for users of wallets that do not support it, i.e. the majority of Ethereum users today

And anything that is `strict` can probably be made into `none` by just architecting the contract differently–I can’t think of a counterexample to this point. So there’s no reason to actually require `strict`.

`strict` is also a bit funky when the combined calls require more than block gas limit and must be sent as multiple transactions. Maybe there should be an additional specification that the request should reject if the wallet cannot make all the calls in a single block, or maybe we want to support that use case of many calls that must be made in separate blocks


*(43 more replies not shown)*
