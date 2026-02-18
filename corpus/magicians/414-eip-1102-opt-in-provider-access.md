---
source: magicians
topic_id: 414
title: "EIP-1102: Opt-in provider access"
author: bitpshr
date: "2018-05-18"
category: EIPs
tags: [provider-ring]
url: https://ethereum-magicians.org/t/eip-1102-opt-in-provider-access/414
views: 17382
likes: 69
posts_count: 67
---

# EIP-1102: Opt-in provider access

Hi everyone. My name is Paul Bouchon and I recently joined the MetaMask team.

MetaMask and most other tools that provide access to Ethereum-enabled environments do so automatically and without user consent. This exposes users of such environments to fingerprinting attacks since untrusted websites can check for a provider object and reliably identify Ethereum-enabled clients.

This proposal outlines a new dapp initialization strategy in which websites request access to an Ethereum provider API instead of relying on its preexistence in a given environment. Feedback welcome and encouraged!

[Proposal draft](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1102.md)

cc [@danfinlay](/u/danfinlay) [@ricburton](/u/ricburton)

*Related to [Web3 Providers for the Future](https://ethereum-magicians.org/t/web3-providers-for-the-future/380)*

## Replies

**danfinlay** (2018-05-19):

Since [@bitpshr](/u/bitpshr) didn’t introduce himself, I’ll just briefly share that he’s one of the newest members of the MetaMask team, has been doing some great work on it, and has begun driving our privacy-centric opt-in provider effort with this spec!

MetaMask hopes to develop its future behavior based on this proposal, so please consider it seriously!

cc [@andytudhope](/u/andytudhope)

---

**bitpshr** (2018-05-19):

Ah! “About me” sentence added, thanks [@danfinlay](/u/danfinlay).

---

**boris** (2018-05-19):

Welcome! Great work [@bitpshr](/u/bitpshr)!

These are all desktop web-centric examples – does some of this differ in a mobile webview context? (I don’t think it does for embedded webviews, and “native” clients would be … totally different, potentially, but I thought I’d ask).

This concerns web3 only – do you think guidance / best practices on showing different addresses for different apps or other “auto address creation / switching” should be included in this proposal, or handled elsewhere?

Because without address switching, we’re still doing 100% correlation of activities between dapps on accounts.

---

**andytudhope** (2018-05-19):

Thanks [@bitpshr](/u/bitpshr) - have shared with the Status team.

I’m not sure there is a big difference for us currently, as we use embedded webviews when navigating to DApps - we just care that those DApps can easily identify which provider is being used and use that for some UI info/education.

I think “auto address creation / switching" should be handled elsewhere, and think it ties more into what [@alexvandesande](/u/alexvandesande) was saying about smooth logins: https://github.com/ethereum/EIPs/pull/1078

---

**bitpshr** (2018-05-19):

Thanks [@boris](/u/boris), and great question about web vs. other platforms. This proposal intentionally omits platform-specific details like messaging protocols, and instead chooses only to detail a high-level strategy that can be applied agnostically of platform or available APIs. For example, a web3 environment built on a mobile platform without a DOM wouldn’t use `postMessage` but should still follow the strategy outlined in this proposal to provide the same parameterized, user-approved web3 access. I updated the proposal to explicitly state that it’s intended to be applied across platforms and that any code is example code.

[@andytudhope](/u/andytudhope) thanks for the feedback. I agree that address creation / switching and anything beyond user-approved web3 access is important but outside the scope of this specific proposal. This proposal is meant to serve a single purpose: to provide user-approved, parameterized web3 access in web3-enabled environments. With this proposal in place, other features can be built on top of it, such as requesting specific account types, accounts with specific balances, etc.

---

**cfly** (2018-05-19):

Thanks for posting this, [@bitpshr](/u/bitpshr).

This proposal, as-is, assumes that there is only one wallet listening on the window. If opt-in web3 access indeed becomes the new standard, then there must be a way for the dapp to specify which wallet the request is intended for.

Otherwise, you could get multiple wallets prompting sign-in.

Have you considered adding an identifier to the request, which would specify the intended wallet?

Example:

`window.postMessage({ type: 'WEB3_API_REQUEST', id: 'METAMASK' });`

A discovery request type, which would send out a command to see which wallets, if any, are listening on the window, may be beneficial in some cases as well.

---

**bitpshr** (2018-05-20):

Interesting thought [@cfly](/u/cfly). While I think it’s slightly contrived to think that multiple wallets would be listening on a given page in a given environment, I do think this case should be gracefully handled. For example, it’s possible that a dapp browser could support the WebExtensions API and a user could have MetaMask installed. In this case (albeit slightly unrealistic) both the dapp browser environment and MetaMask would respond to a request for the web3 API.

Proposal updated, good catch!

As for a discovery API, I’m not sure we could provide this in a way that doesn’t still leave users susceptible to fingerprinting.

---

**danfinlay** (2018-05-20):

If there were a discovery API, this proposal would lose some of its privacy benefits.

That said, this proposal is open-ended, and a client-preference parameter could easily be added later.

If multiple wallets were listening at once in the meantime, I think it’s nice that the user would get total control of which one they used to provide accounts with, already mitigating the “multiple colliding web3 extensions” problem.

---

**cfly** (2018-05-20):

Good point about the discovery API. In my mind, the API would only disclose whether or not a user has a wallet type installed, but that’s enough to be a cause for concern. However, the discovery API idea was just an afterthought.

Mainly, I am trying to avoid 2+ sign-in windows popping up in a world of multiple web3-enabled browser extensions.

Example:

A dapp wants to add a `Login with MetaMask` as well as a `Login with WalletB` button.

The issue is resolved as long as a wallet *can* filter out requests using an `id`.

Thanks for amending the proposal, [@bitpshr](/u/bitpshr)!

I’m wondering if it’d be worthwhile to pass the `id` back in the wallet’s response message as well. That way, if two requests are sent out, you know which wallet is responding. This could be excluded if you want dapps to rely on the injected provider to know who they’re talking to (e.g. `web3.currentProvider.isMetaMask`).

---

**bitpshr** (2018-05-20):

[@cfly](/u/cfly) I added the `id` property to the response, I think it makes sense given the use cases discussed. Thanks again for identifying the multiple-wallet case!

---

**wighawag** (2018-05-21):

I like the proposal,

Thinking about it, could the request ask for a specific network too ?

```
window.postMessage({ type: 'WEB3_API_REQUEST', id: 'METAMASK', networkId: 4 });
```

---

**danfinlay** (2018-05-21):

Yes, this proposal is deliberately forward-extensible, with an eye for requesting networks, and all kinds of specificity.

---

**MicahZoltu** (2018-05-25):

Another privacy enabling feature that would be cool would be that when the dapp asks the provider for the user’s address, the provider returns a randomly generated 20-byte number.  The provider remembers this for the session and returns the same one each time.  Anytime the dapp makes a request of the provider, the provider will search and replace that 20-byte number with the user’s actual address before submitting to the blockchain or returning a result to the dapp.

This would allow users to use dapps without giving up their actual address to the dapp.

---

**wighawag** (2018-05-30):

sounds like a good idea, but in practice, the address will be detectable through transaction/message being signed.

Also if the provider replace the number with the actual address for every web3 call, you would just need a contract with a public method that return the msg.sender to get back the actual address. If it does not replace the number, then you forbid the dapp to actually get info about that address.

---

**MicahZoltu** (2018-05-30):

Hmm, good point that a dapp could get around this by creating a contract that returns the address encrypted, and the website has the decryption key.  Then MetaMask wouldn’t know it needs to swap anything out, and thus return the address to the dapp.

---

**bitpshr** (2018-05-31):

After more discussion on the EIP [pull request](https://github.com/ethereum/EIPs/pull/1102) and valid points by [@MicahZoltu](/u/micahzoltu) and [@Arachnid](/u/arachnid), this proposal shifted from defining an abstract platform-agnostic protocol to defining a concrete DOM-specific protocol for user-approved web3 access. All dapp browsers that currently expose web3 also expose a DOM, so it makes sense to make an immediately-actionable EIP to standardize existing DOM-specific implementations using uniform APIs.

---

**jeluard** (2018-06-22):

[@bitpshr](/u/bitpshr) Have you considered extending this pattern to host specifics API?

I guess it could be as simple as requesting using a different `type`.

e.g. for status: access to whisper key, contacts, …

---

**xinbenlv** (2018-07-04):

Good idea for proposing 1102.

1. Agree that having an approval process will greatly help with privacy and, i believe it helps security in the long run. Since attacker can easily find out account balances and token holdings by simply having  account address, if the web application use the account address together with many other information available at the time of loading web app on browser, it will make it much easier for attacker to collect large amount of accounts and scan to find accounts valuable and vulnerable to exploit.
2. Since this adds a handshake, have you considered adding API versioning information exchange at the time? In that we can allow future development to make use of it.

Again, kudos for proposing it.

[@xinbenlv](/u/xinbenlv)

---

**serso** (2018-08-09):

Why reinventing the wheel and not using existing Permissions API?

See, for example: https://developer.mozilla.org/en-US/docs/Web/API/Permissions_API/Using_the_Permissions_API

---

**bitpshr** (2018-08-09):

Hi [@serso](/u/serso). While the experimental Permissions API initially seemed promising for the purposes of opt-in provider access, key limitations made it less than ideal for this specific use case.

The current Permissions API doesn’t offer the ability to define custom permissions and was only intended to provide a better API to request native browser permissions like “geolocation” or “notification”. Requesting a non-standard permission - like “ethereum” - throws an Error. While dapp browsers could override the `permissions.query` method to explicitly handle a non-standard “ethereum” permission request, malicious sites could then initiate this non-standard request and know they’re in a dapp browser if no Error is thrown as expected. For example:

The following non-standard permission request will immediately throw:

```auto
navigator.permissions.query({ name: 'ethereum' });
// TypeError: The provided value ethereum is not a valid PermissionName.
```

If dapp browsers override `permissions.query` to handle “ethereum” requests, it will not immediately throw:

```auto
const originalQuery = navigator.permissions.query;
navigator.permissions.query = (query) => {
	if (query.name === 'ethereum') {
		// Handle provider request...
    } else {
		return originalQuery.apply(navigator.permissions, arguments);
    }
};
navigator.permissions.query({ name: 'ethereum' });
// undefined
```

Because the Permissions API is meant only for predefined permissions and doesn’t (yet) allow for dynamically-defined permissions in a given context, any support at all for a non-standard “ethereum” permission would allow malicious websites to fingerprint and track Ethereum users. The Permissions API also displays a default browser confirmation dialog and doesn’t allow custom confirmation UIs; this limits the type of information that can be presented to the user, but this issue is less important.

Thanks for your comment, let me know if you have any other ideas around this. I agree that the Permissions API would be great to leverage if it was safely usable for non-standard permission types. We’ll continue to monitor it closely for EIP-1102 applicability.


*(46 more replies not shown)*
