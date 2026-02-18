---
source: magicians
topic_id: 14076
title: "EIP-6963: Multi Injected Provider Discovery"
author: pedrouid
date: "2023-05-01"
category: EIPs > EIPs interfaces
tags: [provider-ring]
url: https://ethereum-magicians.org/t/eip-6963-multi-injected-provider-discovery/14076
views: 5830
likes: 15
posts_count: 30
---

# EIP-6963: Multi Injected Provider Discovery

Introducing a new pattern to discover multiple injected providers using window events to announce EIP-1193 providers in a two-communication standard between Ethereum libraries and Wallet peoviders.

**NOTE:** This EIP replaces the existing [EIP5749](https://eips.ethereum.org/EIPS/eip-5749)

## Replies

**pedrouid** (2023-05-01):

**What changes from EIP-5749?**

- EIP-6963 uses an event-based approach to discover multiple providers
- EIP-6963 does not extend EIP-1193 with info but instead exposes it in parallel
- EIP-6963 includes a local unique identifier and a global unique identifier for each provider
- EIP-6963 does not include provider description to stay agnostic to localization
- EIP-6963 supports any URI encoded image for icons (data, ipfs, http, etc)

---

**SamWilsn** (2023-05-01):

Inspired by a discussion on the [AllWalletDevs](https://allwallet.dev) discord:

Is it possible for a dapp to access `window.evmproviders` before all wallets have had a chance to modify the array? If so, should this proposal also specify an event dapps can subscribe to? Something like:

```javascript
// In the dapp:
window.addEventListener("evmprovider", () => ...);
```

```javascript
// In the wallet's content script:
modifyEvmProviders();
window.dispatchEvent(new Event("evmprovider", ...));
```

---

**pedrouid** (2023-05-11):

I’ve updated the EIP-6963 spec to use an event-based approach now ![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=15)

[![Screenshot 2023-05-11 at 16.28.00](https://ethereum-magicians.org/uploads/default/optimized/2X/c/ce4aa7bde0e339a1b42199c9efc367efea382305_2_361x500.png)Screenshot 2023-05-11 at 16.28.001680×2324 432 KB](https://ethereum-magicians.org/uploads/default/ce4aa7bde0e339a1b42199c9efc367efea382305)

---

**pedrouid** (2023-05-14):

Reverted the “postMessage” back to “dispatchEvent” approach

Please read last comment on Github for context

https://github.com/ethereum/EIPs/pull/6963#issuecomment-1546846953

---

**SamWilsn** (2023-05-15):

Is `name` in `EIP6963ProviderInfo` ever translated into other languages, or is it always in the native language of the wallet?

---

**SamWilsn** (2023-05-15):

So you’re using events because they can pass arbitrary JavaScript objects instead of `postMessage` which can only pass transferable objects?

I feel pretty strongly that we should use `postMessage`, perhaps transferring a [MessagePort](https://developer.mozilla.org/en-US/docs/Web/API/MessagePort) to handle further communication.

I understand that this is a departure from how [EIP-1193](https://eips.ethereum.org/EIPS/eip-1193) works (which requires a `request` *method*), but using `postMessage` really does open up a *lot* of options for wallet design, some of which don’t even need special permissions to run.

You can implement an EIP-1193 compatible provider on top of a `MessageChannel` like so:

```typescript
class PortProvider implements ethers.Eip1193Provider {
    private port: MessagePort;

    constructor(port: MessagePort) {
        this.port = port;
    }

    public request(request: Request): Promise {
        return new Promise((res, rej) => {
            const channel = new MessageChannel();
            channel.port1.onmessage = (evt) => res(evt.data);
            channel.port1.onmessageerror = (evt) => rej(evt.data);
            this.port.postMessage(request, "*", [channel.port2]);
        });
    }
}
```

For the rest of the example, you can take a look at Wallet-Test-Framework’s [dapp](https://github.com/wallet-test-framework/framework/blob/1c841497c536349743bd1d0492c1701a69674e4c/client/src/index.ts#L17C41-L35) and [fake chain](https://github.com/wallet-test-framework/framework/blob/1c841497c536349743bd1d0492c1701a69674e4c/client/src/worker_chain.ts) halves.

---

**rekmarks** (2023-05-17):

Speaking for MetaMask, we’re more amenable to this proposal and are reviewing it internally. Thanks [@pedrouid](/u/pedrouid) for driving, and to everyone who contributed!

On the `postMessage` vs. `dispatchEvent` discussion, we believe that `dispatchEvent` is a good solution for the specific problem this EIP aims to solve, i.e. `window.ethereum` clobbering. We also agree that there’s a need for a more generic messaging protocol, however:

1. This EIP does not seem like the right place for it.
2. If we’re talking browser extensions, such a protocol should use the externally_connectable permission, which recently became possible after the Chrome team fixed this bug originally filed by @MicahZoltu.

---

**pedrouid** (2023-05-17):

I agree with [@rekmarks](/u/rekmarks) feedback that the need for a more generalized communication protocol is important but this EIP is not the place for this as it only focuses on EIP-1193 provider discovery which `dispatchEvent` suffices

That being said a protocol with `externally_connectable` is on my radar and that would be part of a bigger scope of work which would address both provider discovery and interface

---

**SamWilsn** (2023-05-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rekmarks/48/1626_2.png) rekmarks:

> such a protocol should use the externally_connectable permission

Unfortunately `externally_connectable` isn’t universally supported yet: [1319168 - Implement externally_connectable from a website](https://bugzilla.mozilla.org/show_bug.cgi?id=1319168)

---

**rekmarks** (2023-05-17):

To the extent that we should concern ourselves with a browser that has less than 3% global market share, fair enough. Regardless, it shouldn’t be difficult to create a `postMessage`-based version of a protocol written for `externally_connectable`. Come to think of it, the standard should probably consist of a transport-agnostic message protocol with extensions for specific transports.

---

**SamWilsn** (2023-05-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rekmarks/48/1626_2.png) rekmarks:

> has less than 3% global market share

![:hot_pepper:](https://ethereum-magicians.org/images/emoji/twitter/hot_pepper.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rekmarks/48/1626_2.png) rekmarks:

> the standard should probably consist of a transport-agnostic message protocol with extensions for specific transports

Yeah, extracting some bits of EIP-1193 into their own EIP might be worthwhile.

---

**SamWilsn** (2023-05-17):

I know there are some significant drawbacks to this option, but I wanted to get a formal write-up of using scheme handlers for wallet discovery up just so we can discuss it more broadly.

Here’s the proposal pull request: [Add EIP: Scheme-Handler Discovery Option for Wallets](https://github.com/ethereum/EIPs/pull/7039/files)

And its discussion thread: [SHADOW: A Scheme-Handler Discovery Option for Wallets](https://ethereum-magicians.org/t/shadow-a-scheme-handler-discovery-option-for-wallets/14330)

tl;dr use `registerProtocolHandler` and `<iframe src="web+evm://">` to connect to wallets over `postMessage`.

---

**sk1122** (2023-05-18):

I am curious, why are we not using `window.evmproviders`, coupled with a great frontend library, [EIP5749](https://eips.ethereum.org/EIPS/eip-5749) can be a better solution

What are the possible drawbacks of EIP5749 over EIP6963?

---

**pedrouid** (2023-05-19):

EIP-6963 was created from a group that was pushing for adoption of EIP-5749

The main issue is that using a global window object can be manipulated and overwritten by different scripts

EIP-5749 also used a map instead of an array which caused issues with conflicting providers or even an attacker could replace another provider

EIP-6963 also introduces the concept of two identifiers (one local and one global) to ensure uniqueness of providers

EIP-6963 is the successor to EIP-5749 and shares the same authors

---

**sk1122** (2023-05-19):

Understood, Its a great alternative way for EIP-5749

I have been implementing a wallet standard for EVM chains which is based on the [Wallet standard](https://github.com/wallet-standard/wallet-standard)

I myself was working on this problem, previously I was trying to solve this by assigning each wallet their own “namespace” in the browser, something like `window.wallets.metamask` and `window.wallets.backpack`, but then quickly realised it will not be adopted by wallets as it requires a lot of work and also that anybody can update the data from window

Will integrate this in ethereum wallet adapter, how is the adoption like, any wallets integrating currently?

---

**SamWilsn** (2023-05-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png) pedrouid:

> The main issue is that using a global window object can be manipulated and overwritten by different scripts

The current proposal is also vulnerable to manipulation:

```javascript
const foo = window.dispatchEvent;
window.dispatchEvent = function() {
    console.log("here");
    return foo.apply(this, arguments);
};
```

---

**pedrouid** (2023-05-22):

True… an attacker can override or proxy the payloads for `dispatchEvent`

But it’s better to take that risk than breaking compatibility with EIP-1193

My take is that we only get one take to break compatibility with EIP-1193 and if we are going to do it then the best candidate is CAIP-25

It’s a massive task to update all wallets and libraries to support an alternative provider interface (like EIP-1193) so this EIP-6963 is only tackling provider discovery

---

**kdenhartog** (2023-05-22):

[@pedrouid](/u/pedrouid) can you expand a bit further on why you think we only get one opportunity to break compatibility? Internet protocols have never followed that approach. Look at iterations on some of the following examples.

- HTTP v1.0 / v1.1/ v1.2 / v2.0
- TLS v1.0 / v1.1 / v1.2 / v1.3
- SSL v1 / v2 / v3
- OAuth v1 / v2.0 / v2.1
- SAML v1.0 / v1.1 / v2.0

In every one of those cases there’s multiple iterations that occurred at various points of success with various degrees of adoption. I’m not following your line of reasoning that we only get one take to break compatibility. Similarly, isn’t the reason this is so contentious is because we are already breaking compatibility of the discovery mechanism portion of the protocol? Given the protocol encompasses more than just how messages are passed (`window.ethereum` → Event messaging) and what the interface looks like (EIP-1193 → CAIP-25) such as what failure states occur, what RPC methods are supported, what happens if we need to support multiple interfaces, etc can you expand more on why you believe keeping EIP-1193 is necessary versus adding CAIP-25 interface now?

> True… an attacker can override or proxy the payloads for dispatchEvent

Uh that seems like a showstopper to me. A malicious third party iframe such as an advertisement on a DApp being able to MITM the message in order to modify the `to` address in a swap seems rather dangerous doesn’t it?

---

**SamWilsn** (2023-05-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> True… an attacker can override or proxy the payloads for dispatchEvent

Uh that seems like a showstopper to me. A malicious third party iframe such as an advertisement on a DApp being able to MITM the message in order to modify the `to` address in a swap seems rather dangerous doesn’t it?

If an iframe is capable of modifying the window object in the way I described, we’re already screwed because the ethereum object lives on the window as well.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> can you expand a bit further on why you think we only get one opportunity to break compatibility?

I can’t speak for [@pedrouid](/u/pedrouid), but breaking changes are painful, and we should make them judiciously.

---

**glitch-txs** (2023-05-25):

> I am curious, why are we not using window.evmproviders , coupled with a great frontend library, EIP5749 can be a better solution

Adding to what Pedro said, the initial idea of using events was to make sure no wallet was left behind since there [might be a delay](https://groups.google.com/a/chromium.org/g/chromium-extensions/c/ib-hi7hPdW8/m/34mFf8rrGQAJ?pli=1) until the injection happens. This is currently managed by individual wallet events or a setTimeout (which isn’t ideal).

I also agree that evmproviders seems more fragile and easier to break. Regarding the iframe security concern, I think we could add an advise on the security considerations section about sandboxing any iframe used in the website. At least on the dapp side the issue will persist whether we use events, window.ethereum, postMessage or anything that’s attached to the window object.

If I’m not mistaken, sandboxing the iframe, as long as the `allow-same-origin` flag is not there, will prevent the iframe from overwriting the window object.


*(9 more replies not shown)*
