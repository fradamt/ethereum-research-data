---
source: magicians
topic_id: 5969
title: "EIP-3361: eth_signMessage"
author: pedrouid
date: "2021-04-12"
category: EIPs
tags: [wallet]
url: https://ethereum-magicians.org/t/eip-3361-eth-signmessage/5969
views: 4725
likes: 11
posts_count: 15
---

# EIP-3361: eth_signMessage

This proposal aims to reduce the fragmentation of both decentralizated applications and wallets regarding JSON-RPC methods to request message signatures. Also aims to incentivize implementers to move away from legacy methods that may have inherited broken implementations.

https://github.com/ethereum/EIPs/pull/3361

## Replies

**pedrouid** (2021-04-12):

This is quite a simple one and I think that the fact that EIP-1474 is not finalized yet gives us the opportunity to clean up some history with breaking changes.

unprefixed and/or prefixed eth_sign can still exist and so can exist personal_sign

However this proposal would create a new method name for the prefixed eth_sign which can be part of EIP-1474 standard and all dapps/wallets can move towards using the same

Essentially eth_signMessage becomes the standard when EIP-1474 is finalized and we can slowly deprecate the other ones

cc [@danfinlay](/u/danfinlay) [@rekmarks](/u/rekmarks)

---

**trevoraron** (2021-09-24):

I like it! Working with both `eth_sign` and `personal_sign` (where the former doesn’t include the prefix, and the latter does) has been pretty confusing and folks keep mixing up which is which. `eth_signMessage` seems to make much more sense

---

**azf20** (2021-11-29):

This makes a lot of sense to me. [@pedrouid](/u/pedrouid) I saw the EIP was closed as JSON-RPC specifications are moving out of the EIPs repository - is there an ongoing discussion about this somewhere else?

---

**pedrouid** (2021-11-29):

Unfortunately not ![:sweat:](https://ethereum-magicians.org/images/emoji/twitter/sweat.png?v=10) It’s something that I feel it should urgently addressed but just needs to be pushed to production

---

**timbeiko** (2022-01-19):

FWIW, the JSON RPC specs now live here: [execution-apis/src/eth at main · ethereum/execution-apis · GitHub](https://github.com/ethereum/execution-apis/tree/main/src/eth)

Suggest opening an issue/PR with the specification, and potentially adding support in at least 1 client if possible. From there, it can [be brought up on AllCoreDevs](https://github.com/ethereum/pm#agendas) to standardize across clients.

---

**q9f** (2022-01-25):

So to recap the status quo:

- we have eth_sign (unspecified, signing whatever data you put in)
- we have personal_sign (attempt to be more specific, signs only messages with a vaguely defined prefix)
- we have EIP-191 that tries to define signature prefix types (and can be retroactively applied to personal_sign)
- we have EIP-712 eth_signTypedData which currently exists in 4 different implementations
- we have EIP-1474 that tries to be more strict about defining eth_sign

Also, there is now the EIP-4361 movement, building their stack on top of the assumptions available in EIP-191.

I know where you are coming from with EIP-3361; however, if you are implementing Ethereum libraries, you would at some point need to support all of the above for compatibility reasons. So, to play devil’s advocate here, providing support for `eth_signMessage` just adds to the list of functions that you need to support for compatibility between libraries.

Not saying that I disagree. Something like `eth_signMessage` is probably the way we should have done it in the first place.

---

**pedrouid** (2022-01-25):

[@q9f](/u/q9f) definitely agree with your assessment but keep in mind the following:

- EIP-1474 is no longer the reference API which is now hosted at GitHub - ethereum/execution-apis: Collection of JSON-RPC APIs provided by Ethereum execution engines
- Execution APIs specifies a prefixed eth_sign which should be the correct spec
- MetaMask has so much adoption that their unprefixed eth_sign and prefixed personal_sign are more common than prefixed eth_sign as per the spec
- MetaMask in multiple times said that they won’t support prefixed eth_sign to not break compatibility (with projects older than 2018)
- eth_signMessage is essentially a renaming or alias for the prefixed eth_sign
- Ethereum libraries can simply default to eth_signMessage and replace the method name for personal_sign with re-ordered params

I feel like this proposal is actually very easy to grow adoption since the API is very similar and all it attempts to do is rename a JSON-RPC method name with the same parameters

The goal is reduce fragmentation in backwards-compatible approach… plus defaults are very powerful. Ethereum libraries could easily ship a major version that defaults to eth_signMessage once we coordinated adoption across all major wallets to add this simple alias

I understand that is a huge under taking but it’s a little bit ridiculous that we are building more and more features on top of personal_sign (like EIP-4361 Sign-in with Ethereum) and it’s not even part of the spec neither follows the same order of parameters as other signing methods

---

**danfinlay** (2022-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png) pedrouid:

> MetaMask in multiple times said that they won’t support prefixed eth_sign to not break compatibility (with projects older than 2018)

There are newer Ðapps that also are using it, like SushiSwap. That’s the thing about live methods and breaking them: when they’re live, people will use them if they solve a real problem, and breaking them creates problems. But that’s beside the point of the proposal.

I don’t see harm in adding a new alias. We might want to add a new eth_sign(legacy) alias at the same time too, so there can be an unambiguous name for that behvavior for wallets that want to implement it, and we could relegate all this mixed behavior out of main docs. Maybe eth_signRaw.

---

**sbacha** (2022-02-07):

> There are newer Ðapps that also are using it, like SushiSwap.

Sushiswap is using this method because Metamask does not offer a way to programmatically change RPC configuration for default networks. Asking the user to manually configure the RPC connection would render the solution useless. Here is a sort-of write up taken from internal issue tickets detailing the implementation - [The Mythical Web3 Developer Experience | Primitives](https://sambacha.github.io/primitives/2021/12/20/Web3-Technical-Debt-Creep.html)

---

**pedrouid** (2022-02-07):

Could you confirm that you would be able to support the same feature if MetaMask and WalletConnect supported eth_signTransaction?

Instead of using eth_sign where the user blindly signs a transaction as a blob of data you would prompt the users with the same popup as eth_sendTransaction but it would returned a signed serialized transaction that the dapp could send to specific RPC endpoint using the eth_sendRawTransaction

From my own research [@danfinlay](/u/danfinlay) I found the most common use-case of unprefixed signing (through eth_sign) is to replicate eth_signTransaction capability.

This is why I propose that unprefixed signing is removed completely in replacement to eth_signTransaction and eth_signMessage to provide human-readable approvals rather than signing raw data

PS - my own research consisted on tweeting and DMing projects that use eth_sign and asked them why they needed to use that API

---

**sbacha** (2022-02-15):

> Instead of using eth_sign where the user blindly signs a transaction as a blob of data you would prompt the users with the same popup as eth_sendTransaction but it would returned a signed serialized transaction that the dapp could send to specific RPC endpoint using the eth_sendRawTransaction

This is the entirety of our use case, yes. There is no other way to do that in a sane manner.

Walletlink (Now coinbase wallet) has just depreciated eth_sign as well.

let me know what you would like to do for testing, thanks

---

**sbacha** (2022-02-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sbacha/48/4661_2.png) sbacha:

> This is the entirety of our use case, yes. There is no other way to do that in a sane manner.
>
>
> Walletlink (Now coinbase wallet) has just depreciated eth_sign as well.
>
>
> let me know what you would like to do for testing, thanks

Let me make a clarification: while the suggested function of eth_sendTransaction returning a signed serialized transaction for eth_sendRawTransaction to use, there is still the need to be able to configure RPC provider of ANY chain_id.

This is needed for EIP4337, Account Abstraction

---

**sbacha** (2022-02-19):

Just an additional piece of evidence of in the wild usage by a modern dapp as well:

```ts
    } else if (e.code === METAMASK_SIGNATURE_ERROR_CODE) {
      // We tried to sign order the nice way.
      // That works fine for regular MM addresses. Does not work for Hardware wallets, though.
      // See https://github.com/MetaMask/metamask-extension/issues/10240#issuecomment-810552020
      // So, when that specific error occurs, we know this is a problem with MM + HW.
      // Then, we fallback to ETHSIGN.
      return _signPayload(payload, signFn, signer, 'eth_sign')
    } else if (V4_ERROR_MSG_REGEX.test(e.message)) {
      // Failed with `v4`, and the wallet does not set the proper error code
      return _signPayload(payload, signFn, signer, 'v3')
    } else if (V3_ERROR_MSG_REGEX.test(e.message)) {
      // Failed with `v3`, and the wallet does not set the proper error code
      return _signPayload(payload, signFn, signer, 'eth_sign')
    } else {
      // Some other error signing. Let it bubble up.
      console.error(e)
      throw e
    }
  }
```

> source, gnosis/cowswap

It is being used as a fallback mechanism due to users being unable to sign eip712 tx with a hw wallet and mm

---

**dror** (2022-03-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sbacha/48/4661_2.png) sbacha:

> This is needed for EIP4337, Account Abstraction

Alas, I don’t see how EIP-4337 can benefit from eth_signTransaction: the set of transaction parameters used by EIP-4337 differ from standard transaction.

