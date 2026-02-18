---
source: magicians
topic_id: 2422
title: Standardize URL Format for Web3 Browsers
author: brunobar79
date: "2019-01-14"
category: Working Groups > Mobile Ring
tags: [web3-browser, mobile, deep-linking]
url: https://ethereum-magicians.org/t/standardize-url-format-for-web3-browsers/2422
views: 6088
likes: 13
posts_count: 14
---

# Standardize URL Format for Web3 Browsers

Hello everyone!

During the weekend I wrote an initial EIP draft attempting to standardize the URL structure to link into a web3 browser (like Status, TrustWallet, Coinbase Wallet, imToken, MetaMask. etc…).

I’ve seen dApps detecting mobile browsers and asking you to download X browser and sometimes using deferred deeplinking (which is great) but I feel like we’re gonna get into a lot of vendor specific url schemes soon and that sucks.

In order to make the experience more seamless, dApps should still be able to recommend a specific mobile web3 browser via deferred deeplinking but by having a standard url format, if the user already has a web3 browser installed that implements this standard, it will be automatically linked to it.

Additional context: I’ve tried to keep this compatible with EIP-831 using `ethereum:` and the `dapp` prefix, which is making the urls a somehow ugly  or complex.

For ex. in order to link here:  https://peepeth.com/brunobar79?utm_source=twitter

the url would look like this: `ethereum:dapp-https/peepeth.com/brunobar79?chain_id=1&utm_source=twitter`

There’s a couple of problems with that:

1. Mobile wallets that don’t have a browser and registered the ethereum: scheme might be chosen by the OS to handle those links and they won’t be able to do anything with it.
2. ENS conflicts as pointed by @ligi here

In my opinion I think it would be much better if we just agree on the `dapp://` protocol and we shouldn’t have to deal with any of those issues I’ve mentioned before, so let’s discuss what’s the best solution!

Here’s the draft: https://github.com/brunobar79/EIPs/blob/master/url-format-web3-browsers.md

Tagging some people  to get feedback and primarily to discuss the viability of choosing the `dapp://` url scheme.

[@drwasho](/u/drwasho) [@pedrouid](/u/pedrouid) [@pete](/u/pete) [@mandrigin](/u/mandrigin)  [@DmitryBespalov](/u/dmitrybespalov)

If you guys know anyone else that should be involved please ping them!

Thanks!

## Replies

**ligi** (2019-01-15):

Thanks for the initiative! Really like this. Just fear we will have a hen and egg problem here. A bit like you hinted in #1 - that said in this case I do not see #2 as a problem as this one will always have a prefix then - when the whole thing has a prefix we do not run into the collision with ens.

So I would fully support this EIP - just fear we might run into adoption problems as for the hen and egg situation. Would be really happy about ideas on how to mitigate this. On android we might be able to work with fallback urls (then pointing to a neutral app that offers apps that fulfill this standard - e.g. with information from: https://github.com/ethereum-wallets/ethereum-wallet-list

But I do not really know how this can work on desktop or iOS. Perhaps a library that spits out different links depending on the platform.

---

**brunobar79** (2019-01-15):

[@ligi](/u/ligi) Thanks for the input!

#1 is a tough one and  AFAIK there’s nothing you can do on iOS. As you can see [in the docs](https://developer.apple.com/library/archive/documentation/iPhone/Conceptual/iPhoneOSProgrammingGuide/Inter-AppCommunication/Inter-AppComm) it says:

*" **Note:**  If more than one third-party app registers to handle the same URL scheme, there is currently no process for determining which app will be given that scheme."*

Regarding #2 If the ENS name gets a prefix it shouldn’t be a problem but `dapp-*.eth` is still a valid ENS name (as well as `pay-*.eth`)  and ERC-681 doesn’t specify a prefix yet.

On a separate note, What are your thoughts on using `dapp://` for this specific purpose?

---

**mandrigin** (2019-01-17):

yeah, I’m not sure that two apps with the same prefix will pass Apple Review as well. if you look at the browsers, each one of these registers it’s own prefix: `opera-http`, `opera-https`, `chrome-http`, `chrome-https`.

so, maybe we can come up with something like `status-dapp:`, `metamask-dapp:`, etc for iOS specifically?

---

**brunobar79** (2019-01-17):

[@mandrigin](/u/mandrigin) I don’t think having more than one protocol a problem with Apple (I’ve done it before)

Regarding having one prefix it per browser it’s exactly what I’m trying to avoid: vendor specific prefixes.

And it would be great if we have the same one also for both iOS and Android.

---

**mandrigin** (2019-01-17):

Yeah, but unpredictably opening *a* wallet isn’t a great idea and iOS has no mechanics on how to choose this. Unless that is fixed (maybe iOS 13?) I would prefer to just make a JS lib that multiplexes a deeplink into many vendor-specific ones and try to promote it to DApps users.

---

**brunobar79** (2019-01-17):

> unpredictably opening  a  wallet isn’t a great idea

That’s what’s already happening with the `ethereum:` url scheme,   And you’re right. Even U-port that’s not a wallet is opening links like that.

Also, that’s one of the reasons why I propose to register `dapp://` instead so we’re not randomly falling into any wallet but only those who have a browser included and implemented this

---

**ligi** (2019-01-18):

I think using “dapp://” is a good idea.

Btw just triggered registration of ethereum schema for IANA here; https://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml - there is bitcoin and bitcoin cash registered but no ethereum - needs to be changed. When dapp:// gets some usage we can also get this registered there.

That was also why I was looking at this site - wanted to check if dapp:// is already used.

---

**brunobar79** (2019-01-18):

[@ligi](/u/ligi) good call and great to know that the `dapp` uri scheme is “formally” available.

I’ve updated the EIP draft to use `dapp:` instead: https://github.com/ethereum/EIPs/pull/1710

---

**pedrouid** (2019-01-19):

What about making this URI format compatible with ERC-831?


      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-831)




###

Ethereum Improvement Proposals (EIPs) describe standards for the Ethereum platform, including core protocol specifications, client APIs, and contract standards.








Suggestion 1:

```auto
request       = "ethereum" ":" [ "dapp" ]  [ "@" chainId ][ "?" parameters ]
chainId       = 1*DIGIT
parameters    = parameter *( "&" parameter )
parameter     = key "=" value
key           = "url"
value         = STRING
```

Suggestion 2:

```auto
request       = "ethereum" ":" [ "dapp-" ] dappName [ "@" chainId ][ "?" parameters ]
dappName      = STRING
chainId       = 1*DIGIT
parameters    = parameter *( "&" parameter )
parameter     = key "=" value
key           = "url"
value         = STRING
```

---

**pedrouid** (2019-01-19):

However no matter if the schema is `dapp:` or `ethereum:`, there is still the issue with iOS where the user has two apps that subscribe/register/listen to the schema and iOS will pick the “last modified” (aka last updated).

In order to prevent this the Dapp would have to change the schema to target a specific wallet / web3 browser. Example: replacing the previous schema with the specific app schema

---

**brunobar79** (2019-01-19):

[@pedrouid](/u/pedrouid) Thanks for sharing your opinion! The first draft I made was compatible with  EIP-831 and very similar to what you proposed. The reason I think it’s better to have a different url scheme is because lots of wallets and ethereum related apps that don’t have a browser already registered the `ethereum` protocol, so if a user has let say a multi-coin wallet (BTC, ETH, etc.)  and a web3 browser, it could end up getting opened in the wallet app that doesn’t have a browser and that’s not great.

Regarding your second comment, dApps can do that already since most mobile web3 browser already have their own scheme: Status has `status-im`, Trust Wallet has `trust`, etc.

Ideally dApps would be browser agnostic and their only requirement would be to use a web3 browser, which is what I’m trying to promote through this EIP.

In the scenario where a user has two or more web3 browsers installed, the link will still be open by an app that can handle it correctly, (which again, it might not be the case if we go with an ERC-831 compatible scheme)

---

**pedrouid** (2019-01-19):

This makes sense, we’ve found the same issue with WalletConnect and discussed to make a similar change on the ERC-1328 to use a specific WalletConnect schema such as `wc:`

---

**DmitryBespalov** (2019-01-24):

Hi everyone!

TL;DR: for the Web3 browsers, the `dapp://` or other scheme that would be used only by browsers is preferrable to the more generic `ethereum://`. Maybe, the `ethbrowser://`, `web3://` or similar would be a better scheme name.

> note: due to me being a new user on this website, I can’t link to more than 2 sites in the post.

I was thinking what are the different options available to link into native apps on iOS and here are my two cents.

Generally, there are 2 ways to link into an app in iOS: using a custom URL (search for “ios Defining a custom url scheme for your app”) or using a [universal link](https://developer.apple.com/ios/universal-links/) (https scheme). On Android, the deep linking has a similar [mechanism](https://developer.android.com/training/app-links/deep-linking).

The universal link is a preferred way that Apple recommends.

How this works is that app vendor puts a JSON file on a server and registers the server’s url with Apple. In that file, app developer puts mapping from URL paths to specific apps. So if peepeth would build their own app, they could put the association JSON file on the peepeth-dot-com and then all the URL links associated with their domain (for specific paths mentioned in the JSON file) will open in the peepeth app, if it’s installed, or in Safari as a fallback.

Another option, the custom URL, is not as user-friendly as a universal link, but it also allows to directly open an app, if it is installed, provided that the custom URL’s scheme is unique across all apps installed on the device.

Here we have the problem that many already mentioned - if multiple apps register with the same custom URL scheme, then it is undefined which app will open.

From user’s point of view, if the link is directing to a dapp, then it should open in a compatible browser. Now, if it is a universal link, then the app developer decides which mobile app to associate to open the link. If it is a “common” custom URL scheme, and there is only one app that is defined for that scheme, then the link will open there.

To me, there is a problem with using the same custom URL scheme (ethereum://) for all kinds of applications. As was mentioned, Uport app opening a dapp website is a no-go. As a workaround, we could agree on several kinds of dapps that would have mobile clients, for example, browser, wallet, identity, game, what-not (will  look like `ethereum-browser://`, `ethereum-wallet://`, `ethereum-dapp://`, `ethereum-game://`). Then, the URL scheme would address not the protocol, but the kind of an app. That doesn’t solve problem when there are more than one app of the same kind, though, because the custom URL scheme is supposed to lead to a specific app, not to a selection of compatible apps, as it happens when you are trying to open a PDF file and then you can select to open it in … .

Either way, there is no possibility for a user to set a preference in which app to open this or that kind of link, moreover, most of the users won’t care about the technical details.

So, for the Web3 browsers, it totally makes sense to have a separate scheme, and there is no way at the moment on iOS to set a user preference which app to use when opening a deep link.

