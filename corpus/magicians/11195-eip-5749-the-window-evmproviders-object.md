---
source: magicians
topic_id: 11195
title: "EIP-5749: The 'window.evmproviders' object"
author: kvhnuke
date: "2022-10-05"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-5749-the-window-evmproviders-object/11195
views: 7568
likes: 18
posts_count: 64
---

# EIP-5749: The 'window.evmproviders' object

## Abstract

A Javascript Ethereum Provider interface injection that will allow for the interoperability of multiple browser wallets at the same time. Replacing `window.ethereum` with `window.evmproviders` is a simple solution that will provide multiple benefits including: improving user experience, encouraging innovation in the space, removing race conditions and a ‘winner-takes-most’ environment, and lowering barriers to user adoption.

## Motivation

At present, `window.ethereum` is the prevailing method by which Ethereum-compatible applications interact with injected wallets. This originated with Mist Wallet in 2015 to interact with other applications. With the proliferation of both applications and wallets, `window.ethereum` has unintended negative consequences:

- window.ethereum only permits one wallet to be injected at a time, resulting in a race condition between two or more wallets. This creates an inconsistent connection behavior that makes having and using more than one browser wallet unpredictable and impractical. The current solution is for wallets to inject their own namespaces, but this is not feasible as every application would need to be made aware of any wallet that might be used.
- The aforementioned race condition means users are disincentivized to experiment with new wallets. This creates a ‘winner-takes-most’ wallet market across EVM chains which forces application developers to optimize for a particular wallet experience.
- The ‘winner-takes-most’ wallet environment that results from the window.ethereum standard hinders innovation because it creates a barrier to adoption. New entrants into the space have difficulty gaining traction against legacy players because users can have no more than one injected wallet. With new entrants crowded out, legacy wallet providers are put under little pressure to innovate.
- Wallets continue to be the most fundamental tool for interacting with blockchains. A homogeneous wallet experience in Ethereum and EVM chains risks stunting UX improvement across the ecosystem and will allow other ecosystems that are more encouraging of competition and innovation to move ahead.
- Some wallets that currently use window.ethereum as of August, 2022. Currently a user will have inconsistent behavior if they use multiple of these wallets in a single browser.

Metamask
- Coinbase wallet
- Enkrypt
- Trust wallet
- Rainbow ..etc

Replacing `window.ethereum` with `window.evmproviders` will allow solutions such as web3modal and web3onboard to only display all injected wallets the user has installed. This will simpify the UX and remove race conditions between wallet providers in case multiple wallets are installed. Over time, as `window.evmproviders` supplants the current standard and removes barriers to choice, we can hope to see a wallet landscape more reflective of user preference.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

### window.evmproviders={}

```typescript
interface ProviderInfo {
	name: string
	icon:  `data:image/svg+xml;base64,${string}`
	description: string
}
interface ProviderWithInfo extends EIP1193Provider {
	info: ProviderInfo
}
interface EVMProvidersType {
	[key: string]: ProviderWithInfo;
}
interface  Window {
	evmproviders: EVMProvidersType
}
```

```javascript
/**
 * @typedef {Object} ProviderInfo
 * @property {string} name
 * @property {string} icon - format: `data:image/svg+xml;base64,${string}`
 * @property {number} description
 */

/**
 * @typedef {EIP1193Provider} ProviderWithInfo
 * @property {ProviderInfo} info
 */

/**
 * @typedef {Object.} EVMProvidersType
 */

/**
 * @typedef {Object} Window
 * @property {EVMProvidersType} evmproviders
 */

```

Type `EIP1193Provider` is well documented at EIP-1193

```auto
interface ProviderInfo

name: Name of the Wallet
icon: base64 encoded svg image
description: Description for your wallet
```

```auto
interface EVMProvidersType
key is RECOMMENDED to be the name of the extension
```

By adopting an object for EIP-1193 compliant providers we can have multiple different ethereum/evm compatible wallets coexists in the same browser. This will prevent race conditions and inconsistent behaviors.

## Rationale

By introducing `ProviderInfo` type web onboarding libraries such as

Web3Modal

Web3React

Web3Onboard

can easily grab the necessary information to populate their popup window to choose the wallet.

The name `evmproviders` was chosen in order to be inclusive of other evm-compliant chains.

**data:image/svg+xml;** svg data uri was chosen since it is easier to be modified if the application requires for example different size for the image.

## Backwards Compatibility

This EIP doesn’t require supplanting `window.ethereum`, so it doesn’t directly break existing applications. However, the recommended behavior of eventually supplanting `window.ethereum` would break existing applications that rely on it.

## Reference Implementation

### Injection

```typescript
const provider: ProviderWithInfo = [your wallet]
window.evmproviders = window.evmproviders || {};
window.evmproviders[name] = provider
```

### Retrieving all EVM providers

```typescript
const allproviders = Object.values(window.evmproviders)
```

## Security Considerations

The security considerations of EIP-1193 apply for this EIP.

The use of SVG images introduces a cross-site scripting risk as they can include JavaScript code. Applications and libraries must render SVG images using the `<img>` tag to make sure no JS executions can happen.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**kvhnuke** (2022-10-05):

EIP PR link [Add EIP-5749: Deprecate 'window.ethereum' by kvhnuke · Pull Request #5749 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5749)

---

**MicahZoltu** (2022-10-06):

If we are going to deprecate `window.ethereum`, I would rather replace it with a better mechanism for dapp <=> browser communication than go through all of that effort only to replace it with an equally bad (but differently named) solution.

---

**0xwagmiwarrior** (2022-10-06):

I’m a big fan of any solution that can help fix the browser extension “race”. It’s a poor user experience to be forced to choose between a single browser wallet or managing multiple browser / browser profiles. Would love to see how if this implementation can fix that issue and leave room for user adoption and experimentation of many browser wallet solutions

---

**kvhnuke** (2022-10-06):

is there any specific ideas you have? because no matter what kind of communication we come up with, we have to open up a channel to the browser wallet. This needs to be a specific variable, this EIP addresses the injection part not the communication part. In the future once we have a better solution than EIP-1193 we can replace each provider to follow that standard but we can assume those providers will still be part of evmproviders={} object

At the same time, EIP-1193 (current communication standard) was implemented in 2018, to this day there are websites that doesn’t follow that standard. Changing the whole communication model is not as easy as it sounds.

Current problem has existed for years, we need a simple enough solution we can implement easily.

This eip only requires two lines of code to implement, every browser wallet already has rest of the functionality

```auto
window.evmproviders = window.evmproviders || {};
window.evmproviders[name] = provider
```

---

**MicahZoltu** (2022-10-07):

[@SamWilsn](/u/samwilsn) has a concept using scheme handlers, which lets us use the browser’s built-in scheme handler selection system for user choice of wallets.  It also supports both in-browser wallets, desktop wallets, and (in theory) mobile wallets via QR codes.

I had another idea using `window.postMessage`, which I believe can be handled by a browser plugin or iframe host without the broadcasting page being aware of what handlers exist.

The general idea is that the browser extensions shouldn’t be injecting code into every page, there should be a well defined mechanism for the application to probe for wallets and (ideally) a mechanism for the user to choose their wallet without the page knowing that any of the other wallets even exist (or choose no wallet so the page is unaware of them all).

---

**SamWilsn** (2022-10-07):

You can see a *really* early sketch of the idea here: [GitHub - SamWilsn/wallet-demo](https://github.com/SamWilsn/wallet-demo)

The general idea is that every wallet registers a protocol handler for a well-known scheme (maybe `eth://`, `evm://`, or even `wc://`). The dapp encodes connection information into the rest of the URI. I was thinking a WebRTC data channel, but I’m far from an expert on web technology. When you open a URI with that scheme (say in a hidden `<iframe>`), the browser asks the user which wallet they want to use.

The advantages over injecting a script are that this requires no special privileges and works with wallets running in web sites, extensions, and external programs.

---

**kvhnuke** (2022-10-07):

[@MicahZoltu](/u/micahzoltu)

I believe your main concern is when the injection happens. Yes, I’m also not a fan of injecting to every page.

I did look into [@SamWilsn](/u/samwilsn) code. Basically, it makes the dapp responsible for what browser wallets currently inject. `window.postMessage` is how the currently injected code communicates with the extension background script. Based on Sam’s sketch, instead of letting the extension inject it, it becomes part of the dapp itself and dapp devs are responsible for adding the iframe communication model. Yes, this could be simplified, and turned into a library that they can easily add. However, to re-emphasize the original goal of this EIP, suggested solutions still don’t solve the multi-wallet problem.

Here is why?

A quick test on `registerProtocolHandler` on chrome, made me realize you cant have multiple handlers for same scheme. Meaning, each wallet still needs to register its own scheme, and all schemes must start with `web+` as browsers dont  allow arbitrary schemes. [Navigator.registerProtocolHandler() - Web APIs | MDN](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/registerProtocolHandler#permitted_schemes)

If we let browser wallets pick their own scheme, let’s say `web+enkrypt` and `web+metamask`, there is still no way for a dapp to know which wallets are installed, and the dapp devs need to add a growing number of iframes to support all possible schemes. Which brings us back to square one. The main reason for EIP-5749 is to have a way for multiple browser wallets to coexist and for dapps to easily figure out which wallets are available.

Even if we go with [@MicahZoltu](/u/micahzoltu) idea of another extension to keep track of handlers. Then we again have to maintain another whole extension, that needs to keep track of all new browser wallets as they come into existence.

I do like [@SamWilsn](/u/samwilsn)’s idea of switching communication to webrtc (MV3 introduced a whole set of new issues to webrtc but I’m sure those will be solved in the near future). However, since this EIP is not about communication channels, I think we have to address that in a different EIP.

[@MicahZoltu](/u/micahzoltu) I also would like to say that, it is possible for a user to want to use multiple browser extension wallets at the same time. For example, `eth_accounts` can return all approved accounts over multiple different wallets. If we limit users to using just one wallet at a time, then we are back to square one.  However, to address your concern of always injecting into every page, maybe in a different EIP we can put together a library that dapps can integrate, which sends out a `window.postMessage`, that extension wallets can listen to and prompt the user to ask whether that extension needs to be injected to this site. If the user agrees, then it could be part of `window.evmproviders={}`. Also, `evmproviders` object would be `undefined` if none of the wallets accepted. This will prevent random websites from knowing what wallets the user has installed.

---

**SamWilsn** (2022-10-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> Based on Sam’s sketch, instead of letting the extension inject it, it becomes part of the dapp itself and dapp devs are responsible for adding the iframe communication model.

I think we’ve settled on having the dapp listen over WebRTC (so it’s uniform for web extensions and external programs.)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> However, to re-emphasize the original goal of this EIP, suggested solutions still don’t solve the multi-wallet problem.

When I was testing, firefox displays a selector to change between handlers for each link. Apparently Chrome has it buried in the settings…

---

**kvhnuke** (2022-10-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> When I was testing, firefox displays a selector to change between handlers for each link. Apparently Chrome has it buried in the settings…

yea even with that kind of selection, it wont let you select multiple wallets, and who knows when chrome and safari will add even the selection box ![:frowning:](https://ethereum-magicians.org/images/emoji/twitter/frowning.png?v=12)

I dont think safari even supports `registerProtocolHandler`

---

**MicahZoltu** (2022-10-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> I believe your main concern is when the injection happens.

My concerns:

- Wallets should not inject into every page.
- Non-extension wallets should mostly share a protocol with extension wallets.
- Code injection isn’t an appropriate way for wallets to communicate with dapps.
- Many other things related to wallets that are out of scope of this discussion.

If you want to see a prototype I built a while ago you can check out [GitHub - Zoltu/ethereum-browser-sdk: An SDK for communicating between Ethereum dapps and Ethereum enabled browsers via events.](https://github.com/Zoltu/ethereum-browser-sdk).  It may have some bit rot, and I think I only really tested it extensively back in the day on Firefox, but at one point it was fully functional and you could actually use it.  I even created a backward compatibility extension that injects into the page so existing dapps could work with it.  It supports multiple simultaneous wallets with no injection into the page.  It works either as a browser extension or an iframe host (e.g., wallet hosts the dapp inside an iframe).  It uses `window.postMessage` to communicate, which both a hosting iframe and an extension can see, and the dapp/site is completely blind to what wallets are installed/registered until the wallet reveals itself (dapp is the first mover in the handshake).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> A quick test on registerProtocolHandler on chrome, made me realize you cant have multiple handlers for same scheme.

This is unfortunate.  I have only used scheme registration in Firefox where you *can* register multiple handlers with the same scheme and you get a selector dialog.  ![:cry:](https://ethereum-magicians.org/images/emoji/twitter/cry.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> I also would like to say that, it is possible for a user to want to use multiple browser extension wallets at the same time.

This is possible with the `window.postMessage` mechanism.  When the dapp broadcasts its message expressing interest in using a wallet, any number of wallets that are listening in on this well defined channel can respond and the application can establish communication with all of them, or prompt the user to select one.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> to address your concern of always injecting into every page, maybe in a different EIP we can put together a library that dapps can integrate, which sends out a window.postMessage, that extension wallets can listen to and prompt the user to ask whether that extension needs to be injected to this site.

There is no need for injection.  All communication can happen over `window.postMessage`.

---

**kvhnuke** (2022-10-09):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> My concerns:
>
>
> Wallets should not inject into every page.
> Non-extension wallets should mostly share a protocol with extension wallets.
> Code injection isn’t an appropriate way for wallets to communicate with dapps.
> Many other things related to wallets that are out of scope of this discussion.

- Yea this is something I definitely agree with you, wallets shouldn’t inject to every page, but unfortunately 6+ years of always injecting to window has led lot of dapps to expect it to be there. Ive seen many dapps simply fail if there is no ethereum object. Thats why even on this EIP I mentioned to deprecate it, and not completely take it away.
- Im not exactly clear on this, are you referring to wallet connections such as “walletconnect” as non-extension wallets? if so aren’t they already sharing the eip 1193 as a communication protocol?
- I agree with you on not injecting every page, however, Im not sure why you think code injection in general bad practice? Lot of major extensions use the injection to achieve their desired behavior. This is why even MV3 supports this behavior.

I looked into your repo, it was impressive. Here are my concerns.

Iframe communication can work and you proved it is possible, Since the change is for dapps to implement, this change is not feasibly over a short term. We have to clearly define the protocol, message communication channels. A complicated and time consuming process. At that point we should completely switch to webrtc per [@SamWilsn](/u/samwilsn) suggestion. At the same time Im unclear on why this is better than injection as the injected script also uses `postMessage` for communication and this is the standard we’ve been using for the past 6+ years. Only difference I see here is who injects the code. per your suggestion dapps needs to add the iframe code vs currently extension it self add the injected code.

Also, in your example, dapp is wrapped in an iframe. Not sure whether this was intentional, in real life we cant ask users to load the dapps in an iframe. This will lead to bad UI/UX. If it is the other way around, similar to Sam’s code what will be the `src` of the iframe? is it an extension url or is it a code remotely hosted. Basically, there will be lot of CORS and CSP issues, also how can we trust the validity of the remote frame?

Imo, letting the extension it self inject the code is better overall, since there are only few extensions compared to hundreds of thousands of dapps out there. It is easier to extend the feature set, and issue updates over time.

---

**MicahZoltu** (2022-10-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> Ive seen many dapps simply fail if there is no ethereum object. Thats why even on this EIP I mentioned to deprecate it, and not completely take it away.

We can very easily create an adapter extension that either a standalone extension (or wallet extensions in “legacy mode”) auto-inject into every page.  This would allow us to have a smooth transition away from this behavior without breaking the world.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> Im not exactly clear on this, are you referring to wallet connections such as “walletconnect” as non-extension wallets? if so aren’t they already sharing the eip 1193 as a communication protocol?

Yeah, WalletConnect I think would classify.  I don’t know much about the protocol they speak under the hood, and maybe there already is a standard for this.  I was just listing the things I think should be kept in mind when we are talking about wallet <=> dapp communication protocols.  ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> I agree with you on not injecting every page, however, Im not sure why you think code injection in general bad practice? Lot of major extensions use the injection to achieve their desired behavior. This is why even MV3 supports this behavior.

The page is sandboxed away from extensions for a good reason.  When an extension “naively” injects into the page using content scripts the JS that executes has its own JS environment that is sandboxed away from the page while it shares a DOM with the page.  This ensures that the page and the extension injected script don’t clobber each other e.g., by both touching the global namespace.  MetaMask (and others) have hacked around this sandboxing by injecting a script tag into the page which is then executed in the page’s JS environment rather than the sandboxed one.

I *suspect* that one day this “bug” will be fixed, as sandboxes shouldn’t have backdoors in them.  That being said, I am under the impression that the browser standardization people don’t consider this a serious security concern so it may not be fixed anytime soon.

One important distinction is that an `iframe` host cannot inject code into its child.  This means it is impossible to run a dapp inside an iframe, which I believe is why tools like Gnosis have to custom integrate every dapp they support rather than just throwing any old dapp into an `iframe`.

Another important distinction is that there is a well established, documented, and supported mechanism for having pages talk to extensions and that is via `window.postMessage`.  Injecting a script that adds a global variable to the page’s JS environment is non-trivial, introduces complexities/risks with sharing an execution environment, and isn’t well documented at all (I suspect because it is basically a hack).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> Since the change is for dapps to implement, this change is not feasibly over a short term.

An adapter extension can be written (and in fact it has been in that repository) and can be trivially integrated into existing wallets like MM and MV3.  There is no need for dapps to move first here, we can have extensions move first and then incentivize new dapps to build using the new approach and eventually legacy dapps to update to the new approach.  The adapter extension (or wallet in legacy mode) would just inject `window.ethereum` into the page as normal and any calls to those methods would just get wrapped up into a `window.postMessage` call to communicate with the extension(s) via the new protocol.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> per your suggestion dapps needs to add the iframe code vs currently extension it self add the injected code.

This is incorrect, no iframe is necessary (that is just a new way to build a wallet that you can’t do with injection).  A new dapp would just do `window.postMessage({ method: 'eth_blockNumber' })` (+ an envelope for the communication protocol) instead of `window.ethereum.request({ method: 'eth_blockNumber' })`.  An existing dapp would get an adapter injected into their page that just converts `window.ethereum.request` into `window.postMessage` calls.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> in your example, dapp is wrapped in an iframe. Not sure whether this was intentional, in real life we cant ask users to load the dapps in an iframe.

This is an example of a new type of wallet that **can** exist if we switch to using `window.postMessage` butt **cannot** exist with the current injection mechanism.  This is a very powerful type of wallet because it can be IPFS hosted and you don’t need to have custom browser extensions yet (because it is statically hosted) you can trust it.  In fact, if you have IPFS already then this model is significantly lower trust then the current model of extension based wallets.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> Imo, letting the extension it self inject the code is better overall, since there are only few extensions compared to hundreds of thousands of dapps out there. It is easier to extend the feature set, and issue updates over time.

I think you have misunderstood what I am proposing here, but hopefully the above answers/comments have cleared things up.  Let me know if you still feel this way after reviewing this response!

---

**kvhnuke** (2022-10-20):

Sorry I was away for devcon and another conference, finally got some time to respond

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> The page is sandboxed away from extensions for a good reason. When an extension “naively” injects into the page using content scripts the JS that executes has its own JS environment that is sandboxed away from the page while it shares a DOM with the page. This ensures that the page and the extension injected script don’t clobber each other e.g., by both touching the global namespace. MetaMask (and others) have hacked around this sandboxing by injecting a script tag into the page which is then executed in the page’s JS environment rather than the sandboxed one.
>
>
> I suspect that one day this “bug” will be fixed, as sandboxes shouldn’t have backdoors in them. That being said, I am under the impression that the browser standardization people don’t consider this a serious security concern so it may not be fixed anytime soon.
>
>
> One important distinction is that an iframe host cannot inject code into its child. This means it is impossible to run a dapp inside an iframe, which I believe is why tools like Gnosis have to custom integrate every dapp they support rather than just throwing any old dapp into an iframe.
>
>
> Another important distinction is that there is a well established, documented, and supported mechanism for having pages talk to extensions and that is via window.postMessage. Injecting a script that adds a global variable to the page’s JS environment is non-trivial, introduces complexities/risks with sharing an execution environment, and isn’t well documented at all (I suspect because it is basically a hack).

I see your concern, since current approach seems like a hack due to the fact that we are injecting the script into DOM. However, this isnt the case with new MV3 they actually made it a feature. I believe  since it is more useful in real world now. Enkrypt did intergrate this, however we are waiting for couple more chrome release before adding it to our main codebase.  [Fix: 🔧 immediately inject code by kvhnuke · Pull Request #89 · enkryptcom/enKrypt · GitHub](https://github.com/enkryptcom/enKrypt/pull/89/files#diff-1a7598a9963dd7992cf764a44d758da77562890a57d3d672d970afe0cbc08cb4R44)

basically, with MV3 you can execute a script in “MAIN” world and this will prevent the current way of injecting scripts. I personally tested it and it works as it should. I believe, this legitimize and make it more of standard to execute a script in the DOM. Since this exists now I dont think it will no longer can be considered as a hack or a bug. Not only that, they also added `injectImmediately: true` which forces the browser to execute the script immediately before executing any other scripts. This actually fixes a current bug, where the dapp scripts load first and it cant detect `window.ethereum` since the extension is lagging.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> We can very easily create an adapter extension

It is easy to create an adapter extension however, getting users to install it and getting devs to maintain it will be the tough part. Overall user experience will not be good. If we decide to make it part of for example MM or Enkrypt then we are back to square one where we still inject to `window.ethereum` and needs to fight over the implementation. Which also means, the extensions that dont want to follow will still inject and override `window.ethereum` to be a EIP 1193 provider.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> This is incorrect, no iframe is necessary (that is just a new way to build a wallet that you can’t do with injection). A new dapp would just do window.postMessage({ method: 'eth_blockNumber' }) (+ an envelope for the communication protocol) instead of window.ethereum.request({ method: 'eth_blockNumber' }). An existing dapp would get an adapter injected into their page that just converts window.ethereum.request into window.postMessage calls.

I dont believe it will be easy as this, now we have to define how to respond to these requests since for example which extension is responsible for responding to `eth_blockNumber` (since all extensions will receive the same request). If we decide to add an extra parameter, then we have to clearly define things such as, name/id who maintains this list, how can dapps know which extensions installed. Also, in the case of being backwards compatible, which extension will get all the requests…etc It seems like communication layer will be a big change that requires both extension devs, dapps, and onboarding libs to work together.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> This is an example of a new type of wallet that can exist if we switch to using window.postMessage butt cannot exist with the current injection mechanism. This is a very powerful type of wallet because it can be IPFS hosted and you don’t need to have custom browser extensions yet (because it is statically hosted) you can trust it. In fact, if you have IPFS already then this model is significantly lower trust then the current model of extension based wallets.

Ah I see! since this is a whole another topic I’ll skip this for now.

Overall, I do understand some of the benefits of what you are proposing however, It is hard to justify the problems of current approach specially since the scriptExecution is now becoming a standard. Change to the whole communication model will be extremely hard, time consuming and not necessary if the benefits cant justify the change. May be in the future, we can move away from `window.postMessage` completely and use something like WEBRTC, However, this will be a major change that can take years. Whole purpose of this EIP is to fix an issue that millions of users facing today, and I do believe the simplest solution will be the best solution.

---

**MicahZoltu** (2022-10-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> since this is a whole another topic I’ll skip this for now.

I don’t agree this is a different topic because this is, IMO, one of the strongest arguments against using injection for wallet communication.

The current injection mechanism doesn’t allow us to create purely web based wallets, and this results in situations like Gnosis Safe’s wallet being unable to work with arbitrary dapps and people having to install wallets into their browser and give those wallets full access to every webpage they view (pending https://bugs.chromium.org/p/chromium/issues/detail?id=679238 getting fixed).  `iframe` based wallets require zero permissions and can be IPFS hosted which gives us strong decentralization in the distribution of the wallet rather than relying on Chorme/Firefox/Safari extension stores (which have been known to randomly shutdown/block wallets in the past).

The changes to manifest v3 you mentioned are compelling in suggesting this isn’t “just a hack” as I previously expressed, though I would like to hear if Firefox is going to implement that or not as they have been pushing back on Chrome’s machinations for manifest v3 due to Chrome seemingly having forgotten to put its user’s first.  However, I don’t think injection being not-a-hack is enough to convince me that we should continue down the injection road.  I would want to see a viable path away from extension wallets to iframe wallets, which I think is very important.

---

**kvhnuke** (2022-10-28):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> The current injection mechanism doesn’t allow us to create purely web based wallets, and this results in situations like Gnosis Safe’s wallet being unable to work with arbitrary dapps and people having to install wallets into their browser and give those wallets full access to every webpage they view (pending 679238 - chromium - An open-source project to help move the web forward. - Monorail  getting fixed). iframe based wallets require zero permissions and can be IPFS hosted which gives us strong decentralization in the distribution of the wallet rather than relying on Chorme/Firefox/Safari extension stores (which have been known to randomly shutdown/block wallets in the past).

you should look into `walletconnect` they are doing something similar to what you are referring, basically their relays acts as the middleware to create a communication channel between 2 websites. With that for example uniswap user can communicate with a myetherwallet user, only problem with this is having to switch between tabs as you have to sign txs on MEW (this feature is not implemented on MEW im just referring to it as an example). However, I still believe this is a whole another communication model, we cannot simply expect all dapps to host themselves inside an iframe. Gnosis problem is actually not a problem, it is feature that they implemented to be secure and they follow a different wallet model, and libraries such as `walletconnect` can enable more features they need. This EIP is specifically addressing extension wallets and the current injection model, which is used by over 15 million users out there, and how we can solve a major problem by changing few lines of code.

Regarding your ipfs comment, afaik current extension wallets work fine with ipfs so Im not sure why we need iframes.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> iframe based wallets require zero permissions and can be IPFS hosted which gives us strong decentralization in the distribution of the wallet rather than relying on Chorme/Firefox/Safari extension stores (which have been known to randomly shutdown/block wallets in the past).

At the same time, lets say one of the extension wallets gets shutdown by the respective store, user will still lose access to that wallet whether it is an iframe wallet or not.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> The changes to manifest v3 you mentioned are compelling in suggesting this isn’t “just a hack” as I previously expressed, though I would like to hear if Firefox is going to implement that or not as they have been pushing back on Chrome’s machinations for manifest v3 due to Chrome seemingly having forgotten to put its user’s first. However, I don’t think injection being not-a-hack is enough to convince me that we should continue down the injection road. I would want to see a viable path away from extension wallets to iframe wallets, which I think is very important.

Firefox already implemented it even on MV2 [scripting.executeScript() - Mozilla | MDN](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/scripting/executeScript)

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> don’t think injection being not-a-hack is enough to convince me that we should continue down the injection road. I would want to see a viable path away from extension wallets to iframe wallets,

Please dont think Im trying to discourage your view or opinion, I do believe iframe wallets can work as another type of wallet. If you want it to be the main type of wallet, it is a major change that involves dapp devs, wallet devs, well documented communication layer, and ton of time. Unfortunately, current market is too big to make such a big change immediately.

---

**MicahZoltu** (2022-11-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> you should look into walletconnect they are doing something similar to what you are referring, basically their relays acts as the middleware to create a communication channel between 2 websites.

WalletConnect requires a centralized (and hence censorable and privacy violating) relay in the middle.  I hear they are working on trying to figure out a way to connect without a relay, but at the moment this solution is going in the opposite direction of censorship resistance, unpermissioned, trust minimization, and privacy preservation.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> we cannot simply expect all dapps to host themselves inside an iframe

Dapps would not host themselves in iframes, the *user* would choose to load a dapp within their wallet’s iframe.  Dapps would be hosted normally (ideally IPFS, but via whatever means they currently do).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> Gnosis problem is actually not a problem, it is feature that they implemented to be secure and they follow a different wallet model

Having spoken with Gnosis on this issue, they do it this way because it is the only viable option, not because they want to.  They either need to author an extension (which greatly complicates things when users want to sign a transaction with an extension wallet), or they need every supported app to have a custom integration, or they need to centralize by using WalletConnect.  These aren’t great options, and in their view the custom integration route was the preferred of the options, not because it is good but because it is better than the others.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> how we can solve a major problem by changing few lines of code.

I think this is where we disagree.  While I agree that this is a small change, it is none the less a breaking change.  If we are going to go through the process of introducing a breaking change, a deprecation cycle, and end of life policy we should use that opportunity to fix more than the “smallest possible thing”.  The cost of any breaking change is *extremely* high and we should spend it making large changes that solves multiple problems rather than just using it to fix one tiny little thing.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> Regarding your ipfs comment, afaik current extension wallets work fine with ipfs so Im not sure why we need iframes.

Extension wallets work fine with IPFS hosted dapps.

IPFS hosted web wallets do not work at all with current extension wallets (that use injection).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> At the same time, lets say one of the extension wallets gets shutdown by the respective store, user will still lose access to that wallet whether it is an iframe wallet or not.

It seems like you still may be misunderstanding my proposal.  The wallet is just a website like `ipfs://<cid>` or (if you don’t care about security) `https://whatever`.  There is nothing hosted on any store, and if you use IPFS there is nothing even hosted on a central server that can be taken down.  As long as the IPFS network is functional and *someone somewhere* is pinning or using the wallet (thus keeping the cache warm), it will be available to everyone.  The wallet has an `iframe` inside of it that loads the dapp in question.  This could be loaded via some sort of dapp browser, or it may allow the user to just enter any website into an internal address bar and load it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> Firefox already implemented it even on MV2 scripting.executeScript() - Mozilla | MDN

Ah, nice!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> it is a major change that involves dapp devs, wallet devs, well documented communication layer, and ton of time

See above, I suspect you still may not be understanding the model I’m proposing.  While long term it would require changes from both wallets and dapps (just as your proposal would), there are intermediate solutions that allow us to create a transition path that doesn’t require getting everyone to do everything at once.

---

I just want to highlight that my primary argument at this point is that any breaking change (such as what you and I are both proposing) should including fixing as much as possible because breaking changes are extremely expensive to get adopted (I think we agree on this point).  Your proposal is to make the smallest breaking change possible, while I am advocating that if we are going to eat that cost we should fix as much as possible and not waste the effort on a relatively small change.

---

**kvhnuke** (2022-11-09):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> WalletConnect requires a centralized (and hence censorable and privacy violating) relay in the middle. I hear they are working on trying to figure out a way to connect without a relay, but at the moment this solution is going in the opposite direction of censorship resistance, unpermissioned, trust minimization, and privacy preservation.

Yea I think their main way of decentralizing is by letting anyone becomes a relay, and the relay is open-source as well. but yea I agree, it does introduce a level of centralization.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Dapps would not host themselves in iframes, the user would choose to load a dapp within their wallet’s iframe. Dapps would be hosted normally (ideally IPFS, but via whatever means they currently do).

Going back to iframe wallet comment, currently in order to do that it doesn’t require a whole new EIP  afaik you can simply call `parent.ethereum` (I know you are not a fan of this) from the iframe so dapps can simply do something like `const provider = window.ethereum || parent.ethereum` and current functionality will be there. Parent window only need to implement the provider interface as a global variable. You achieved a similar functionality in your code as well. However, Iframes have whole another set of problems, starting from ton of vulnerabilities to all the UX/UI issues this is why lot of other projects gave up on it. I remember there was another project who tried to integrate dapps into their wallet interface however, dapps UI doesnt scale properly as no one is expecting it to be inside an iframe also responsiveness goes out the door as soon as you put a website inside an iframe. Security issues are whole another conversation. Due to potential phishing, lot of website also use a header so you cant embed it inside an iframe. Due to all this, I dont think iframe wallet will be a good approach.

That said, I am not against rest of your proposal of using `window.postMessage` directly instead of injecting. However, my argument is that we already use it behind the scenes with injected wallets. Your approach `client->postMessage->wallet` but the postMessage communication layer needs to be rewritten to handle the issues I mentioned on one of my previous comments.

Current approach `client->dedicated variable->postMessage->wallet` This way lets you communicate and make use of existing code base without major changes.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Having spoken with Gnosis on this issue, they do it this way because it is the only viable option, not because they want to.

I honestly dont believe best approach for Gnosis to try and host every dapp inside and iframe, it will vastly reduce the user experience and they will run into ton of security issues.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> They either need to author an extension (which greatly complicates things when users want to sign a transaction with an extension wallet), or they need every supported app to have a custom integration, or they need to centralize by using WalletConnect.

Not sure why it would complicates things when the user wants to sign a transaction? with a proper support to multi wallet standard, they can simply add `window.evmprovider.gnosis` variable and handle the communication however they want. Also, we all need to understand, at the end of the day there will be 100s of different wallet types. If you open any of the wallet onboarding libraries (web3onboard, web3modal, web3react) they all have different integrations for wallets. We will never have just one standard that every wallet will follow. Because of this, if you are a wallet provider part of the deal is going after dapps and adding custom integrations and thats unfortunately what lot of wallets including Enkrypt needs to do since there is no proper way of letting dapps know which wallets are available.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I think this is where we disagree. While I agree that this is a small change, it is none the less a breaking change. If we are going to go through the process of introducing a breaking change, a deprecation cycle, and end of life policy we should use that opportunity to fix more than the “smallest possible thing”. The cost of any breaking change is extremely high and we should spend it making large changes that solves multiple problems rather than just using it to fix one tiny little thing.

Breaking changes are not binary, you have to take into consideration how much work you are expecting the world to do in order to support your change. More popular you are even changing one line of code across every place it is used could be next to impossible. This is why we are stuck with internet protocols that were invented in 3-4 decades ago. Changes proposed by this EIP is easier to adopt than the changes you are proposing. At the same time, your proposed changes doesnt provide any significant advantages. We can come up with an extremely complex model that could be applied to every blockchain out there, however it doesn’t mean people will adopt it and we will still have issues around `window.ethereum` for the foreseeable future.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> IPFS hosted web wallets do not work at all with current extension wallets (that use injection).

I am consfused about this, wdym by “IPFS hosted web wallets” also I am not sure whether wallet could be fully decentralized. Blockchain data is not in ipfs so the wallet needs to connect to a centralized node at some point to get the data and broadcast tx.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> it will be available to everyone. The wallet has an iframe inside of it that loads the dapp in question. This could be loaded via some sort of dapp browser, or it may allow the user to just enter any website into an internal address bar and load it.

I dont think this could be done with current technology, how is the wallet getting blockchain data? it still needs to interact with a node. Only way this could work without a node, if the user willing to manually set the gasprices, nonce and willing to take the signed tx and broadcast it somewhere else or user needs to have a node running or access to rpc address. This is a very specific use case and not sure how many users are technical enough to even achieve this.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Your proposal is to make the smallest breaking change possible, while I am advocating that if we are going to eat that cost we should fix as much as possible and not waste the effort on a relatively small change.

Yea but like I mentioned before all breaking changes are not the same, if we can make a change that can solve a problem with least amount of work I believe that will get adopted rather than a massive change. Otherwise users will be the ones who’ll suffer forever. Also dont forget the fact that, each new line of code can introduce a vulnerability that we didn’t think about, injection method has been battle tested for 7+ years.

I think best cause of action for your proposal is to make it an EIP and have a separate discussion around it. I will be more than happy to participate and give you my thoughts around the extra communication layer we need, I can also make Enkrypt team implement it if it is satisfactory. There is no reason for a wallet to only support one standard.

---

**MicahZoltu** (2022-11-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> Breaking changes are not binary, you have to take into consideration how much work you are expecting the world to do in order to support your change. More popular you are even changing one line of code across every place it is used could be next to impossible. This is why we are stuck with internet protocols that were invented in 3-4 decades ago. Changes proposed by this EIP is easier to adopt than the changes you are proposing. At the same time, your proposed changes doesnt provide any significant advantages. We can come up with an extremely complex model that could be applied to every blockchain out there, however it doesn’t mean people will adopt it and we will still have issues around window.ethereum for the foreseeable future.

Putting this first (out of order from your message) since I think the rest of the discussion is largely not relevant as long as we disagree on this point.

While you are correct that a tiny change is easier to get adopted than a large one, I think this is lost in the noise to the overall cost of an ecosystem wide breaking change.  If we assign arbitrary units, getting the entire ecosystem to adopt *any* breaking change (e.g., epsilon sized) is say 1000 units of effort and a one line change is +1 units of effort and a big change like switching to `window.postMessage` is +10 units of work.  Yes, it is 10x harder, but it is still insignificant compared to the cost of doing *any* change.

Your mentioning of decades old protocols I feel helps my argument here because it exemplifies just how amazingly hard it is to do *any* change.  IPv6 is arguably one of the smallest possible breaking changes to a core internet protocol, just changing the size of a number essentially, yet it has taken ~25 years to get adopted and it *still* hasn’t supplanted IPv4.  I really think we need to get this right rather than doing the smallest thing possible because it may take us years to get broad adoption of *anything*, and that thing should be provide the maximum utility as we may not get another chance to do a breaking change (the more Ethereum grows, the harder it will be).

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> Yea I think their main way of decentralizing is by letting anyone becomes a relay, and the relay is open-source as well. but yea I agree, it does introduce a level of centralization.

Due to firewalls, this generally doesn’t work because users don’t run servers that can accept incoming HTTP connections.  I have heard that there is a way to get two devices on the same internal network communicating (thus potentially avoiding NAT issues), but I’m not sure how realistic this is.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> Iframes have whole another set of problems, starting from ton of vulnerabilities to all the UX/UI issues this is why lot of other projects gave up on it. I remember there was another project who tried to integrate dapps into their wallet interface however, dapps UI doesnt scale properly as no one is expecting it to be inside an iframe also responsiveness goes out the door as soon as you put a website inside an iframe. Security issues are whole another conversation. Due to potential phishing, lot of website also use a header so you cant embed it inside an iframe. Due to all this, I dont think iframe wallet will be a good approach.

I would like more details on the downsides to iframe wallets you see.  I have implemented one, and Gnosis has implemented one, and I haven’t run into any of the problems you mentioned here.  The *only* problem we have both run into is the fact that dapps require an injected provider and so don’t work by default (you need an extension to do the injecting, or you need the dapp to support another mechanism of connecting to the host wallet).

What are the fishing vectors you see here?

What are the security vulnerabilities?

What are the performance problems?

For the UI issues I think perhaps you are imagining a visual iframe with the host all around it and it has its own scrollbars and whatnot?  I’m envisioning something more like the host page just has a little toolbar on the top or bottom, or perhaps a floating tab on one of the sides but the app’s iframe is basically the entire window.  In the one I wrote, it was a floating header bar that could be collapsed down to just a tab that you could click to bring it back, but the dapp got essentially 100% of the viewport to itself.  Gnosis does have left and top bars, and I haven’t noticed any problems with it but perhaps I just haven’t used enough dapps to run into trouble?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> lot of website also use a header so you cant embed it inside an iframe

This one is quite unfortunate, and frustrates me quite a bit.  I don’t think dapps should be doing this (I am not convinced it offers meaningful protection for a dapp), but you are correct that some do it none the less.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> Your approach client->postMessage->wallet but the postMessage communication layer needs to be rewritten to handle the issues I mentioned on one of my previous comments.

I’m not sure which comment you are referring to specifically, but I believe I have already replied and mentioned that these things were already solved in my prototype SDK?  I would be happy to discuss more, but I feel like it is out of scope of this specific discussion beyond just saying that it is a very solvable problem and one I believe is in fact already solved in my prototype (so not just theoretically solvable).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> they can simply add window.evmprovider.gnosis variable and handle the communication however they want

They literally cannot do this.  This is exactly the problem I’m trying to describe.  An iframe host cannot inject into or mutate the hosted iframe.  This is a core browser security/sandbox thing that is very unlikely to go away.  They cannot provide *any* variables to the dapp they have in an iframe.  The only way they can communicate with the iframe dapp is via `window.postMessage`.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> I am consfused about this, wdym by “IPFS hosted web wallets” also I am not sure whether wallet could be fully decentralized.

Meaning iframe host wallets like Gnosis, which can be hosted on IPFS (unlike a browser extension, which cannot be).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> Blockchain data is not in ipfs so the wallet needs to connect to a centralized node at some point to get the data and broadcast tx.

Users should be running their own node or using an embedded light client, but that is a separate problem that I am advocating for elsewhere.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kvhnuke/48/7370_2.png) kvhnuke:

> I dont think this could be done with current technology, how is the wallet getting blockchain data? it still needs to interact with a node. Only way this could work without a node, if the user willing to manually set the gasprices, nonce and willing to take the signed tx and broadcast it somewhere else or user needs to have a node running or access to rpc address. This is a very specific use case and not sure how many users are technical enough to even achieve this.

The iframe host wallet behaves the same as an extension wallet.  It would allow the user to set a JSON-RPC provider, or it would have an embedded light client, or it would provide a centralized RPC for the user.

---

**kvhnuke** (2022-11-10):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> While you are correct that a tiny change is easier to get adopted than a large one, I think this is lost in the noise to the overall cost of an ecosystem wide breaking change. If we assign arbitrary units, getting the entire ecosystem to adopt any breaking change (e.g., epsilon sized) is say 1000 units of effort and a one line change is +1 units of effort and a big change like switching to window.postMessage is +10 units of work. Yes, it is 10x harder, but it is still insignificant compared to the cost of doing any change.

I can get behind this if the extra work you are proposing can add additional advantages. We shouldn’t do extra work if the extra work can be boiled down to few lines. What you are proposing is only applicable to a very specific use case where 99.9% of the the current Ethereum users are not technical enough to handle [running nodes (either full/light), I understand the fact this proper decentralization however not good user experience].

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> IPv6 is arguably one of the smallest possible breaking changes to a core internet protocol, just changing the size of a number essentially, yet it has taken ~25 years to get adopted and it still hasn’t supplanted IPv4.

I definitely do not agree with this, IPv6 is one of the biggest major changes internet protocol is going through. It might look simple but definitely not simple, they even had to abandon IPv5.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Due to firewalls, this generally doesn’t work because users don’t run servers that can accept incoming HTTP connections. I have heard that there is a way to get two devices on the same internal network communicating (thus potentially avoiding NAT issues), but I’m not sure how realistic this is.

Firewalls blocking is not something we can fix with any standards. Firewalls can prevent users from visiting any site or running any node including Ethereum and even ipfs.

**Iframe issue?**

A simple google search on “Iframe vulnerabilities” will give you everything you need from clickjacking to phishing.

`X-Frame-Options` is a recomended header for you to follow for best security practices in web, thus preventing your site being embeded inside other sites. You should also check “why X-Frame-Options”.

At the same time, based on my understanding you do believe having scrollbars in a frame is ok. However, if you talk with any UI/UX person they will highly disagree with you.

So yea iframes have ton of issues and since this is EIP is not about that I wouldn’t get into those.

Like I mentioned before, I dont believe advocating for iframe wallets is the best way to propose your idea. I do believe the technical side of things that you achieved with your way, however it is hard to justify the extra work that goes into it. If you’d like iframes wallets to work then the easiest way would be asking web3onboarding libraries to change one line of code to something like this

`const provider = parent.ethereum || window.ethereum` or based on this EIP `const providers = parent.evmproviders || window.evmproviders`. This will let the iframe talk to the host frame.

Again, if you make your idea into EIP I would be more than happy to contribute

---

**jmcho** (2022-11-23):

Hey [@kvhnuke](/u/kvhnuke), I’m from the Coinbase Wallet team. What’s the status on this EIP? We’re very supportive of this idea and would be happy to support.


*(43 more replies not shown)*
