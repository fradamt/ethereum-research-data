---
source: magicians
topic_id: 2429
title: Automatic Authentication Signature
author: wighawag
date: "2019-01-15"
category: Web > Wallets
tags: [wallet, authentication]
url: https://ethereum-magicians.org/t/automatic-authentication-signature/2429
views: 5904
likes: 22
posts_count: 29
---

# Automatic Authentication Signature

Hi,

I’d like to discuss here the proposal about “Automatic Authentication Signature”, that I explain [here](https://medium.com/@wighawag/automatic-authentication-signatures-for-web3-dcbcbc64d6b5)

The idea behind authentication signature is to allow a back-end (verifier) to authenticate users via their web3 wallet signing capability. This is currently implemented crudely by some dapps with static messages that user need to confirm and ensure they are not signing a message pertaining to another application.

Ideally though the back-end should generate some random message every time and request a signature from the wallet. Theoretically this should not need user confirmation as the sole purpose is to verify that the wallet is indeed in control of the private key associated with the exposed address.

Indeed, it is assumed that a web3 wallet exposing a specific address has the corresponding private key. The signature required for authentication is only necessary because a dishonest user could simply expose an address as part of the web3 API for which it does not possess the private key.

Currently though because wallets require user confirmation popup for every signature request, the user experience is less than ideal: User would get asked to sign a message they can’t meaningfully verify (all the data being used for the sole purpose of back-end authentication).

We thus need to come up with an  **automatic authentication signature standard that would allow web3 wallets to recognize such specific signature requests and perform them without requiring user confirmation.**

This could take the form of a special signature format that wallet would recognise and would not be used in other contexts. I did not come up with a specific scheme yet but this could take the form of a specific envelope type for [EIP712](https://github.com/ethereum/EIPs/pull/712).

To avoid signature replay and  prevent a malicious application to generate such authentication signatures, the message needs to include random data that only the verifiers knows (not unlike a CSRF token).

As [@PhABC](/u/phabc) rightly point out in his reply to the article, such scheme implies that applications would be then able to generate signature at will unless wallet rate-limit such requests. He then raised the concern that ECDSA might not be adequately secure for such heavy use.

While I am not sure it is the case, I replied that apart from rate-limiting we can come up with alternative mechanism that involve generating private key scoped for each application/session …

See the [post](https://medium.com/@wighawag/automatic-authentication-signatures-for-web3-dcbcbc64d6b5) and associated replies for more details :

If you are involved in building wallet and web3 browser, I would love your feedback

[@danfinlay](/u/danfinlay) [@pete](/u/pete) [@iiwok](/u/iiwok)

Thanks

## Replies

**pedrouid** (2019-02-20):

I’m glad that Discourse notified me of this thread as I was about to write a new one.

I think this a great use-case where automated signing is harmless and improves the Web3 UX significantly for both users and developers.

I discussed this with a few people at ETH Denver (@rouven [@jamesyoung](/u/jamesyoung) [@michaelsena](/u/michaelsena) [@oed](/u/oed)) and I’m planning to introduce this to the WalletConnect protocol sooner than later. However I want WalletConnect to embrace as many standards as possible working together with other Web3 providers like Metamask to reduce the duplication of efforts.

My proposal is that Wallets should provide this authentication signature every time they expose new accounts as part of the JSON-RPC spec either as an updated `eth_accounts` or part of the new scope of `wallet_` prefixed methods.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rmeissner/48/643_2.png)
    [Add `wallet_` methods to improve dapp to wallet interaction](https://ethereum-magicians.org/t/add-wallet-methods-to-improve-dapp-to-wallet-interaction/1848) [Wallets](/c/wallets/17)



> Wallets are the most important interaction point between dapps and the Ethereum chain. Currently the most important wallet methods ( eth_sendTransaction ,  eth_sign  and  eth_signTypedData ) are part of the general api specification. For most wallets it does not make sense to provide implementations for all  eth_  methods. Therefore it would make sense to introduce a new prefix  wallet_  (this was already introduced with EIP 747: wallet_watchAsset).
> This will provide the possibility to support …

Whenever a Dapp requests access to the User’s accounts, the Wallet should sign a standard authentication message that Dapps could verify themselves. I think this standard shouldn’t be that extensive and ideally we could start pushing for adoption asap.

PS - Can we move this thread to the Wallet Ring? Feels more appropriate to discuss with those participants

---

**wighawag** (2019-02-20):

Hi [@pedrouid](/u/pedrouid)

Glad you like the idea.

When you say that wallet should automatically sign upon accounts request, how do you envision the possibility for server to inject the random data (to ensure nobody has requested the same signature before) ?

The idea I had was to make a generic signature request that can be call anytime but do not require user approval.

---

**pedrouid** (2019-02-20):

I followed up on my proposal on the `wallet_` scope proposal as I feel this should be part of it. In short I think it should be part of the JSON RPC response whenever the Dapp request access the accounts that user exposes to the Dapp



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png)
    [Add `wallet_` methods to improve dapp to wallet interaction](https://ethereum-magicians.org/t/add-wallet-methods-to-improve-dapp-to-wallet-interaction/1848/38) [Wallets](/c/web/wallets/17)



> Hey guys, I was going to start a new thread but after replying to this existing thread on Automatic Authentication Signature. I realised this should be part of the wallet_ methods.
> https://ethereum-magicians.org/t/automatic-authentication-signature/2429/2
> As you can read on the other thread, the proposal describes including a standard authentication signature that would be automatically signed by the Wallet to verify the account ownership on the Dapp side. Perhaps this could be part of either w…

---

**wighawag** (2019-02-20):

I suggest we continue the discussion here (i moved the thread to the wallet ring) as the other thread is too generic and has already seen some unrelated discussion.

I do not mean to say that the proposal should not be part of the wallet_ RPC methods though.

As for replying to your comments there :

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png)[Add `wallet_` methods to improve dapp to wallet interaction](https://ethereum-magicians.org/t/add-wallet-methods-to-improve-dapp-to-wallet-interaction/1848/38)

> This message doesn’t even require EIP-712 in my opinion, since it’s not meant to be read by the user. Something as simple as doing a personal_sign for a fixed message I own this account that return a JSON RPC response as follows.
>
>
>
> ```auto
> {
>   "id": 1,
>   "jsonrpc": "2.0",
>   "result": [
>     {
>       "address": "0x9b7b2B4f7a391b6F14A81221AE0920A9735B67Fb",
>       "signature": "0x30755ed65396facf86c53e6217c52b4daebe72aa4941d89635409de4c9c7f9466d4e9aaec7977f05e923889b33c0d0dd27d7226b6e6f56ce737465c5cfd04be400"
>     {
>   ]
> }
> ```

Using EIP712 might indeed not be desired.

As for a fixed message to be signed everytime, I think this is not a good security practice. Every dapp would then be able to get the signature for every other dapp unless we separate them via origins. I think it is important to let the dapp inject a random payload as a signature challenge.

That is why I was asking how you envision the possibility to add the required random data when using eth_accounts or other such methods.

This could simply be an extra parameters to the eth_accounts, etc but I do not see the issue in being simply a separate method.

---

**pedrouid** (2019-02-20):

That’s fine with me. Can you just expand on why you think it’s important for the dapp to inject a random payload as a signature challenge?

IMO the more predictable these signatures are the better. Reduces the attack surface and makes it more interoperable. If I’m able as a Dapp developer to have the Wallet automatically sign any message, I can move funds from a smart contract based wallet for example.

---

**wighawag** (2019-02-20):

I am not talking of allowing any message. As mentioned in the blog post, these messages signature request need to be identifiable form other and this should not allow the dapp to request message signature that could be valid in other context.

We could simply request a prefix that should not be used outside of authentication signature request.

like :

`Authentication Signature challenge: dkashfjdshfjdshfjhsafghsagfgasdfdsdsafdshgfjhjgjkjh`

Alternatively we could come up with something similar to how personal_sign use a prefix not usable in ethereum transaction.

The reason to add a random payload is simply to prevent an application to get the fixed signature and use to sign in another application.

If no random payload are used, the wallet would basically give the right to identify as the wallet address forever to any application.

---

**pedrouid** (2019-02-20):

I see that makes sense. This actually would play nicely with the WalletConnect SDK as the signatures would be tightly coupled to each session uuid.

```auto
Authentication Signature challenge: cbaff650-8d35-4106-8c28-394615d62e2c
```

Do you think it would make sense to use uuid’s as part of the standard or do you see any advantages to allow completely arbitrary data to be provided instead?

---

**wighawag** (2019-02-21):

The original idea was that the standard (at least in its generic version (not tied to a session creation)) should allow arbitrary data. This way it can be used for every kind of request without requiring the verifying end point to keep track of a session.

The standard should thus allow to sign any message following this format :

`Automatic Signature <payload>`

Maybe it could be exposed this way :

`wallet_autoSign(data)`

This would not remove the ability to use it this way for a session :

`Automatic Signature challenge: cbaff650-8d35-4106-8c28-394615d62e2c`

To summarize, I can’t see any reason for restricting the payload.

---

**pedrouid** (2019-02-21):

Fair enough, that makes sense. It makes no difference to restrict the challenge payload.

However I would not expose an autoSign method but would instead make it a parameter when requiring accounts using the `wallet_accounts` method.

Request

```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "wallet_accounts",
  "params": ["cbaff650-8d35-4106-8c28-394615d62e2c"]
}
```

Response

```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "result": [
    {
      "address": "0x9b7b2B4f7a391b6F14A81221AE0920A9735B67Fb",
      "signature": "0x30755ed65396facf86c53e6217c52b4daebe72aa4941d89635409de4c9c7f9466d4e9aaec7977f05e923889b33c0d0dd27d7226b6e6f56ce737465c5cfd04be400"
    {
  ]
}
```

---

**wighawag** (2019-02-21):

hmm, I guess you want this to be tied to account request to avoid yet another back and forth for wallet connect protocol, right ?

Is wallet_accounts the equivalent of `eth_requestAccounts` (https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1102.md)  or is `wallet_accounts` to be called **after** the user enabled access via `eth_requestAccounts` ?

If it is the former, I see the benefit in proving ownership in one call, instead of having to do it with another call.

If it is not, I would say such ownership proof should be added to `eth_requestAccounts` instead.

I would still advocate for another variant, that can be used any time after the wallet authorized the application via `eth_requestAccounts`

This is what I wanted to propose  as  `autoSign` so application can continuously request data to be signed by the wallet without requiring user input.  This can be used to communicate to a verifying endpoint without requiring sessions for example.

So we would have

```auto
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "wallet_accounts",
  "params": ["cbaff650-8d35-4106-8c28-394615d62e2c"]
}
```

OR if  `wallet_accounts` is to be called after user authorized access, we should do that there instead with :

```auto
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "eth_requestAccounts",
  "params": ["cbaff650-8d35-4106-8c28-394615d62e2c"]
}
```

And on top of that we would also have :

```auto
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "wallet_autoSign",
  "params": ["", "

"]
}
```

---

**pedrouid** (2019-05-14):

What’s the latest status on this proposal, should we make a PR to start a Draft EIP as well?

---

**wighawag** (2019-05-14):

It depends if we want to include the logic in 1102 itself ? In that case, we could help push forward 1102 with that proposal included.

At the same time, if you are interested to move to a “wallet_” namespace I’d be happy to move that forward too / instead.

I would also introduce “wallet_autoSign” as a separate proposal.

---

**pedrouid** (2019-05-14):

Yes, I would signal to make `wallet_autoSign` proposal first.

---

**wighawag** (2019-05-15):

Hey [@pedrouid](/u/pedrouid) I created a first draft here : https://github.com/wighawag/EIPs/blob/automatic_signatures/EIPS/eip-automatic-signatures.md

Let me know what you think, and I ll create a pull request with an specific number.

I’ll add you as a author too if you do not mind.

---

**danfinlay** (2019-06-14):

There are really two different motivations here, from what I can tell, and they aren’t entirely compatible:

1. The ability for apps to get signatures at-will.
2. The ability to reduce the number of sign-in prompts.

The first one is addressed neatly in [EIP 1775](https://github.com/Bunjin/EIPs/blob/master/EIPS/eip-1775.md), including accounting for using an app-isolated key, so that this key is only good for that app’s own session persistence, etc, and so no user interaction is needed, and the ECDSA concerns are largely mitigated.

The second one is the more WalletConnect like login moment, and it makes sense to want to integrate a signature into revealing accounts, because really people are getting too many confirmations, we should just ask them for what we need to do up front, and let them get on with their days.

Rather than this very small incremental approach, where we’re definitely going to be continuously adding new methods repeatedly to the provider, I’d like an extensible sign-in pattern that we can add permissions to as needed (maybe an extension of the `.enable()` method… could easily take an `options` object…).

I’m currently working on a proposal to this end, but first maybe I’ll put out a feeler for how people think this should look, maybe in a fresh topic.

---

**wighawag** (2019-06-14):

Hi [@danfinlay](/u/danfinlay) thanks for the feedback,

Yes, there are indeed 2 different motivations

motivation 2) has already been proposed here separately on EIP-1102 (which is not yet final) see [EIP-1102: Opt-in provider access](https://ethereum-magicians.org/t/eip-1102-opt-in-provider-access/414/58) and it is the most urgent motivation in my opinion: Apps are currently asking user to sign a message manually which is very ugly user experience. Worse, to alleviate slightly the problem some apps use a static friendly message, making them vulnerable to replay attacks.

adding it as an optional argument to `enable` or `requestAccounts` as mentioned in the comment, make it backward compatible so nothing is blocking wallet to support it today.

But note, that this is not only for WalletConnect like login. Metamask would definitely benefit from this too.

As for motivation 1) I don’t think we need to chose between 1775 and this. We can have both. I have given my opinion on the current 1775 draft [here](https://ethereum-magicians.org/t/eip-erc-app-keys-application-specific-wallet-accounts/2742/34) and from what I understood, it force separate apps into their own account, which can pose problem for apps that want to be bridged.

Edit: one thing to note is that if motivation 1) is fulfilled, it automatically fulfil motivation 2) as far as account authentication is concerned but I still favor having it in `enable` first as this is priority and could reduce back and forth fro solution like wallet connect

---

**wighawag** (2019-08-01):

I submited a Pull Request for that proposal, see here : https://github.com/ethereum/EIPs/pull/2224

---

**sscovil** (2025-05-11):

Hey everyone, I know this is a very old thread, but I wanted to revive the topic of automatic authentication signatures and see if there is any interested in re-opening PR 2224.

Here is why:

I’m the lead developer of EVMAuth, a groundbreaking contract based on the ERC-1155 token standard. EVMAuth provides a robust mechanism for EMV-based *authorization* that could eliminate entire categories of tech debt from just about any Web3 application.

In order for EVMAuth to reach it’s full potential, there needs to be a simple way to *authenticate* users. Right now, we recommend EIP-712 message signing, which I believe is the standard…but this requires end users to take manual action, and it’s not a great user experience.

If an app developer simply wants to confirm that an end user owns the wallet address they claim to own, for authorization via EVMAuth, it would be much better to have an automatic way of doing so. We just need a standardized way of doing that, built directly into digital wallets.

---

**mikem** (2025-05-14):

I would support it, I don’t know if there’s a good reason it died off but it looks like no? There have been some similar ideas discussed since this was first brought up but I don’t see any that inherently supersede this (but that does not mean there aren’t any).

---

**wighawag** (2025-05-14):

Hey [@sscovil](/u/sscovil), thanks for bringing this up and reviving this thread. I am happy to help move that forward too.

As discussed earlier in this thread there are 2 non-mutually exclusive proposals that we could push forward

A) EIP-1102 backward compatible extension (adding a challenge string to `eth_requestAccounts`)

B) Generic Automatic Signatures (PR-2224)

A) is simple and backward compatible. should be easier to get accepted. It does not offer the full feature set of B) but for authentication might be enough. Interested to know what you think here.

B) is more powerful and actually with B you don’t need A) anymore, but there are still open questions that I mentioned in the [PR](https://github.com/ethereum/EIPs/pull/2224)

- Is it secure to let applications sign at will (even if the message is prepended by “Automatic Signature”) ?
- Or should we do such signing using a non-hardened derived key ?
- If so could EIP-1102’s eth_requestAccounts be used to provide the parameter to derive from (could be one based on the origin of the document) ?
- Should we rate-limit the requests ?

Also if we explore B) we could also explore further proposals that I discussed in the past.

- 3 Proposals For Making Web3 A Better Experience
- Automatic Authentication Signatures For Web3  (different scheme than proposed here, using domain)


*(8 more replies not shown)*
