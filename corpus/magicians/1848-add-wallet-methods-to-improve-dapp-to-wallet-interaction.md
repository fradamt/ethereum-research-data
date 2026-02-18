---
source: magicians
topic_id: 1848
title: Add `wallet_` methods to improve dapp to wallet interaction
author: rmeissner
date: "2018-11-08"
category: Web > Wallets
tags: [wallet, ux]
url: https://ethereum-magicians.org/t/add-wallet-methods-to-improve-dapp-to-wallet-interaction/1848
views: 6172
likes: 33
posts_count: 38
---

# Add `wallet_` methods to improve dapp to wallet interaction

Wallets are the most important interaction point between dapps and the Ethereum chain. Currently the most important wallet methods ( `eth_sendTransaction` ,  `eth_sign`  and  `eth_signTypedData` ) are part of the general api specification. For most wallets it does not make sense to provide implementations for all  `eth_`  methods. Therefore it would make sense to introduce a new prefix  `wallet_`  (this was already introduced with [EIP 747: wallet_watchAsset](https://ethereum-magicians.org/t/eip-747-eth-watchtoken/1048)).

This will provide the possibility to support new types of wallets. While the current methods are focused on wallets based on externally owned accounts, more and more wallets start to make use of smart contracts. Interacting with smart contract based wallets is different to the interaction with EOA based wallets. The biggest difference is that smart contract based wallets cannot generate ECDSA signatures. Also smart contract based wallets provide the possibility for a lot of extended functionality.

There is an early version of an EIP (https://github.com/rmeissner/EIPs/blob/rmeissner-wallet-rpc/EIPS/eip-xxx.md) and I would love to move this forward.

The idea is to provide a standard that can be used by any sdk building ontop of an EthereumProvider. This interface could also be used for communication between mobile wallets and mobile apps. And it should be able to provide a base that can be extended for future wallet specific improvements.

(e.g. this would make it possible that dapps build there own EthereumProvider and browser wallets just inject the a WalletProvider that handles the `wallet_` rpc calls)

## Replies

**ligi** (2018-11-09):

Hey - thanks for the initiative - really like it.

Just having  a problem with one detail: wallet_getActiveWallet

I really do not like the idea of having the state of an active-account - would rather like to see that the account has to be passed as parameter to eth_sign, eth_signTypedData, …

---

**rmeissner** (2018-11-09):

My idea was that `wallet_getActiveWallet` just indicates which wallet is selected by default (if you don’t specify anything for `sign` or `signTypedData`)

Also a lot of dapps use `coinbase` to get the currently selected account from MetaMask and this would be a more explicit way of querying that.

But I think it makes sense to allow specifying an account for `sign` and `signTypedData`.

---

**ligi** (2018-11-09):

I think you should be forced to specify the account for signing. Really do not like the idea of an active account. And with the recent changes from metamask the coinbase thing should also not work anymore - correct?

---

**pcowgill** (2018-11-09):

I think this would be a great change, [@rmeissner](/u/rmeissner). [@ligi](/u/ligi) I agree - I think storing an active/default wallet should be the dapp’s responsibility.

---

**rmeissner** (2018-11-09):

In this case would you add something like `wallet_getWallets` to allow the dapp to query all addresses with their wallet types.

If the wallet (e.g. MetaMask) now manages multiple addresses and the dapp requests a signature from address2, should the user be allowed to change this?

[@ligi](/u/ligi) even with EIP-1102 the coinbase approach should work **after** the user approved the dapp.

A lot of wallet still have a selected account which is used for certain actions (e.g. sendTransactions). Should this be somehow explicitly exposed? What should a dapp display as the account if it sees that the user has multiple?

EDIT: After some thinking you could also say: If the wallet doesn’t want that the dapp can select between different address it should only return a single address (this is actually what we do for the safe extension right now). So if a wallet provider returns a list of addresses the dapp should be able to freely choose (this is what [@ligi](/u/ligi) and [@pcowgill](/u/pcowgill) were suggesting if I understood correctly)

---

**androolloyd** (2018-11-09):

I purpose a new method

`wallet_validNotaries` - effectively a way to return an array of valid accounts that can sign messages on behalf of the contract (meta txns, other types of messages, etc)

---

**androolloyd** (2018-11-09):

this is one of my original design approaches, the wallet could define default exposed identities to the dApp or service/ecommerce

---

**digitaldonkey** (2018-11-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcowgill/48/822_2.png) pcowgill:

> I think this would be a great change, @rmeissner. @ligi I agree - I think storing an active/default wallet should be the dapp’s responsibility.

Shouldn’t that be the responsibility of the Wallet?

Why encourage Dapp devs to chose from an Array of adresses. Wouldn’t it be better to expose only one address and let the Wallet user decide which one? So that you don’t need to share multiple addresses if it’s not required.

---

**digitaldonkey** (2018-11-15):

Second question to improve my understanding:

You can use provider-engine to combine Wallet/signing functions and other Web3 functions.

So the wallet just needs to provide the functions it supports. Is there something wrong with that approach?

---

**rmeissner** (2018-11-16):

That was the initial idea. After thinking some more, I am actually not sure what would be use cases where a dapp needs to know that a provider manages multiple wallets (e.g. why should a dapp know that I have multiple metamask accounts)

For your second question this is exactly the idea. Currently wallets and providers are kind of the same. So meta mask is proving an ethereum provider for all possible request (that includes nonce caching, filter abstracting and what endpoint is being used). By defining the wallet interface it should be possible that wallets just inject the wallet subprovider and each dapp uses the provider-engine to build a provider for their needs.

---

**pedrouid** (2018-11-24):

I like this idea! There might be less scenarios where a user might want to manage multiple accounts in the same Dapp but there is definitely a lot room to be played there. Plus this is already possible with hardware wallets, I think it would be great to provide this for other implementations like Metamask and WalletConnect.

The great thing about standards is that we won’t have to ask developers to consult our proprietary APIs and they can just assume these features are available for all wallets and build Dapps accordingly.

---

**ligi** (2018-11-25):

clef has a very similar API - see e.g. https://github.com/ethereum/go-ethereum/pull/18079/files#diff-d93f8d0c622b04c41f4723de960a1b20

Perhaps these efforts can be joined?

---

**holiman** (2018-11-26):

Here are the ‘official docs’ of the current WIP api for Clef: https://github.com/ethereum/go-ethereum/tree/master/cmd/clef . It’s subject to change, particularly around the signing, since I hope that we can get `signedTypedData` in there – the challenge is around that how to build the user flow, so the user knows what he/she is signing.

I also dislike statefullness in the actual wallet rpc endpoint (so `wallet_getActiveWallet`). Also, `clef` is written to have as little external dependencies and communications as possible, so there are no `sendXX` methods whatsoever, all you can do is request to have something signed, and you get back a result.

---

**ligi** (2018-11-28):

Adding one more discussion point to this. The networkId is also state currently that I would love to see vanish.

some context: https://discuss.walletconnect.org/t/networkid-in-the-protocol/42

---

**rmeissner** (2018-11-28):

I was thinking alot about that state topic recently and the walletconnect topic made me think of the following.

The rpc calls `wallet_` should not assume any state. In wallet connect you open a session an the state is part of the session, but that is something that would be a level above the rpc calls (at least in my opinion).

So if we assume an a dapp that wants to interact with a wallet. Then there could be a WalletSDK which allows the selection of the prefered wallet (or if only 1 wallet is exposed just default to that). And any signing/sending of transactions would make use of that wallet.

This would make it easy for dapp developer do implement interaction with the wallets, but would also manage the state on the dapp site.

Another question would be if something like the session should be part of the rpc methods.

---

**pedrouid** (2018-11-30):

I agree, that makes a lot of sense and I think it’s very much inline with the discussions around web3 providers. The state should be separate between a wallet and a session, that may live in a web3 provider or any equivalent wallet sdk as [@rmeissner](/u/rmeissner) was describing.

The JSON RPC methods should be used to gain access to more/new data to feed this state. This could fix one of the annoying ux flows that request users to change network/chain when a Dapp could simply just proceed and handle the chain selection on their side. Something that already happens with offline and hardware wallets.

The question is should this be a fixed design or should it be flexible that would Dapps to choose their preferred pattern. We need standarization but also to be cautious to not make them to opinionated. Preferably we can design two or more branches of standards that follow well defined design choices so that increase interoperability without removing options.

Example:

- Standards that favor Stateless Dapps (where Wallets control active account, chain, etc)
- Standards that favor Stateful Dapps (where Dapps can control state only requesting more information for Wallets)

Either way, there is room to branch out multiple standards to solve many of these. I was about to suggest that a better user flow to solve the chain switching would be to introduce a rpc method `wallet_changeChain`

PS - I’m trying to use the term chain instead of the network because of the EIP-155 prevents chainID conflict while networkID doesn’t

---

**ligi** (2018-12-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> Here are the ‘official docs’ of the current WIP api for Clef: https://github.com/ethereum/go-ethereum/tree/master/cmd/clef

just FYI - account_version seems to be missing in the the docs

---

**ligi** (2018-12-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rmeissner/48/643_2.png) rmeissner:

> The rpc calls wallet_ should not assume any state. In wallet connect you open a session an the state is part of the session, but that is something that would be a level above the rpc calls (at least in my opinion).
>
>
> So if we assume an a dapp that wants to interact with a wallet. Then there could be a WalletSDK which allows the selection of the prefered wallet (or if only 1 wallet is exposed just default to that). And any signing/sending of transactions would make use of that wallet.
>
>
> This would make it easy for dapp developer do implement interaction with the wallets, but would also manage the state on the dapp site.

I think it should be exactly as you described - this is what I had in mind when asking for removing the state in the protocol

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rmeissner/48/643_2.png) rmeissner:

> Another question would be if something like the session should be part of the rpc methods.

I do not see a reason to.

so I would see the following alterations to your EIP:

**wallet_getActiveWallet** would be removed and replaced with something wallet_requestAccounts

which can return one or more accounts - it can also return different accounts in subsequent calls. On the wallet side the user would be asked which accounts should be exposed to the dapp (at this point in time)

**wallet_sendTransaction**

would get an extra parameter chainId

from the account side sendTransaction and eth_sign are already stateless as the account/from is passed in the call already

---

**pedrouid** (2018-12-03):

I know it’s easier to add new methods then altering existing ones but I think these methods `wallet_requestAccounts` and `wallet_sendTransaction` feel duplicated.

Currently `eth_accounts` would serve the same purpose as `wallet_requestAccounts` and we already call it multiple times with Metamask to detect account switching. This would also be possible to support with WalletConnect easily.

Also `wallet_sendTransaction` includes an incremental change to `eth_sendTransaction` thus I would suggest a coordination of efforts with major clients and major wallets to simply update the existing `eth_sendTransaction` to include the chainId as second parameter

**BEFORE**

```auto
{
  "id":1,
  "jsonrpc": "2.0",
  "method": "eth_sendTransaction",
  "params": [txn]
}
```

**AFTER**

```auto
{
  "id":1,
  "jsonrpc": "2.0",
  "method": "eth_sendTransaction",
  "params": [txn, chainId]
}
```

---

**ligi** (2018-12-04):

yes if feels a bit duplicated - and usually I am preaching for DRY - but in this case I see it a bit different.

The difference between eth_accounts and wallet_requestAccounts is that eth_account returns all accounts and I see wallet_requestAccounts as the possibility to incrementally expose accounts to a dapp (user chooses which accounts are exposed to a dapp). As far as I understand eth_accounts it is always returning all accounts from a client.

with eth_sendTransaction the problem is a bit more complex. The main problem is that there is no real versioning of the JSON RPC interface. So adding a parameter is really messy. Also I think a wallet should not really send the transaction - this is responsibility of the dApp. The wallet should just sign the transaction and return the signature. Think e.g. about offline signing use cases.

So long story short - I would still signal for adding these methods to the wallet_ namespace and keep the eth_ methods untouched. There can be a translation layer in between that translates eth_sendTransaction to wallet_signTransaction for the migration phase.

Also as a learning from the past we should really add versioning - so I signal the need for wallet_rpcversion - returning a semver string which in the first iteration could be  “1.0.0”


*(17 more replies not shown)*
