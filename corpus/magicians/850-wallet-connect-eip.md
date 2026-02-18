---
source: magicians
topic_id: 850
title: (Wallet) Connect EIP
author: ligi
date: "2018-07-23"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/wallet-connect-eip/850
views: 11531
likes: 22
posts_count: 15
---

# (Wallet) Connect EIP

In the context of https://discuss.walletconnect.org/t/qr-code-data-format/14 - I am thinking about a (Wallet) Connect EIP and would love to gather some Ideas/Feedback.

The EIP will be based on [831](https://eips.ethereum.org/EIPS/eip-831).

As the [ERC-831](https://eips.ethereum.org/EIPS/eip-831) prefix I would suggest “connect”

- walletconnect is a bit too long imho - the longer the QR code gets the harder it gets to scan.
- wc would also be an idea - but it has a bit of a shitty () connotation   (maybe we ignore this as it is mostly seen by computers and not humans)
- connect is a bit broader - and not as opinionated - could be used for other use-cases in the future also

to encode the shared key I would suggest using base64 - which is easy to parse and saves some bytes compared to the hex encoding (also for making the QR code easier to scan) We should be open to updates from symetric to asymetric here also. Especially when these URLs are not only used for QR-Codes but also for Intents (think connecting a native Android dapp to a Wallet on the same device)

So I would suggest the following URL format:

“ethereum” “:”  “connect-” sessionID  “@” version “?” parameters

as parameters (taken from the current state of the art):

dappName

bridgeURL

symKey

Feedback/Ideas welcome!

## Replies

**pedrouid** (2018-07-23):

Maybe “wc” prefix isn’t so bad since it will be mostly viewed by devices and not humans, saving a few characters for displaying the QR code

Also agree that base64 should be used instead of the current hex encoding for the shared key

Regarding symmetric and asymmetric keys, I still think that at least for mobile-to-desktop is best to keep it symmetric but maybe it isn’t secure enough for mobile-to-mobile. However we need to balance user experience with security because WalletConnect is first and foremost a UX improvement to current implementations

Perhaps we should also save a few characters on the parameter names:

- dapp
- bridge
- key

---

**ligi** (2018-07-23):

Sounds great! Totally happy with shortening to dapp and bridge. With key I lean to keeping symKey to be able to distinguish later on when asymetric keys might be used. Also thinking about it a bit more: why would asymetric crypto here lead to worse UX in this case? I think this could be done without the user even noticing here …

---

**ligi** (2018-07-24):

As a follow-up from here: https://discuss.walletconnect.org/t/ideas-for-decentralizing-the-bridge-server/15/4 :

We really should care for changes in the transport layer. In the end I think PSS and/or whisper might an ideal fit here. When using these protocols IMHO we do not even need to add the keys to the URLs then as these protocols care for the encryption. Maybe we do not even need a session-id - but just generate an private  per session and use the public key as the session-id.

kindly inviting [@jarradhope](/u/jarradhope) as I know he is very interested in it: https://twitter.com/jarradhope/status/1021489103186092032

EDIT: this way we could also get really easy to scan QR-Codes:

[![Selection_097](https://ethereum-magicians.org/uploads/default/original/1X/90213183ecfebdc1d31869c53caa16f1d9b2155d.png)Selection_097405×401 8.03 KB](https://ethereum-magicians.org/uploads/default/90213183ecfebdc1d31869c53caa16f1d9b2155d)

this is the QR-code for:

ethereum:wc-0x381e247bef0ebc21b6611786c665dd5514dcc31f@2?name=tester&pss

---

**ligi** (2018-07-25):

Idea - why don’t we use the very same scheme already today? So instead of the current sessionId we use the public key/address of the session’s private key. So the url would currently look like:

ethereum:wc-0x381e247bef0ebc21b6611786c665dd5514dcc31f@1?name=tester&[bridge=bridge.mydapp.org](http://bridge=bridge.mydapp.org)

and as soon as PSS or whisper gets usable the URL just changes to:

ethereum:wc-0x381e247bef0ebc21b6611786c665dd5514dcc31f@2?name=tester&pss

or

ethereum:wc-0x381e247bef0ebc21b6611786c665dd5514dcc31f@2?name=tester&whisper

---

**dpyro** (2018-07-27):

Why not use checksummed addresses?

Should there be support for ENS-style addresses?

Also `string@` patterns seems to be used for user information in URI examples I’ve already seen such as username/password or email name. I could see it being used to pass an account name or private key in a connect URI. Why not use something like `&v=2` instead?

---

**ligi** (2018-07-28):

> Why not use checksummed addresses?

You mean ERC-55? QR codes already do error correction - not yet sure how it would help

> Should there be support for ENS-style addresses?

why - these addresses would only live for the session - not sure why they should support ENS

> Also string@ patterns seems to be used for user information in URI examples I’ve already seen such as username/password or email name. I could see it being used to pass an account name or private key in a connect URI. Why not use something like &v=2 instead?

I do not see the advantage yet - can you elaborate? I like @version as e.g. @2 is shorter than v=2 ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12) Also the version should always be there - the private key might not be.

---

**pedrouid** (2018-08-15):

I’ve created an EIP for this

https://github.com/ethereum/EIPs/issues/1328

[@ligi](/u/ligi) would love your review on it!

---

**pedrouid** (2019-01-29):

[@ligi](/u/ligi) I have created a PR for updating this EIP to match the changes we discussed on the WalletConnect forum



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/1728/files)














####


      `master` ← `pedrouid:patch-2`




          opened 05:10PM - 29 Jan 19 UTC



          [![](https://avatars.githubusercontent.com/u/10136079?v=4)
            pedrouid](https://github.com/pedrouid)



          [+10
            -11](https://github.com/ethereum/EIPs/pull/1728/files)







**Updating EIP-1328 WalletConnect Standard URI Format**

Changes being reviewe[…](https://github.com/ethereum/EIPs/pull/1728)d on linked discussion thread before merging and tech spec still in progress












Still updating the technical specification on the WalletConnect documentation to describe all details of the new protocol version v1.0.0-beta

I will ping on this thread by the end of the day

---

**pedrouid** (2019-01-30):

Here is the first draft of the WalletConnect v1.0.0-beta tech spec, still needs polishing but it should provide a clear enough picture


      [github.com](https://github.com/WalletConnect/walletconnect-docs/blob/v1.0.0-beta/tech-spec.md)




####

```md
# Technical Specification

## Introduction

WalletConnect is an open protocol for connecting Dapps to Wallets. The motivation behind it came from the lack of user-friendly solutions for user to use Wallets without browser extensions. In order to solve this it was designed to not require any software or hardware requirements from the user to connect a Wallet to a Dapp. The design is mostly tailored to mobile wallets but it could definitely support desktop wallets as well. The protocol relies that both the Dapp and the Wallet use the WalletConnect Client SDK and connect to a Bridge server that will relay the communications. The communication is initiated with a standard URI format that contains the topic of the connection request, a symmetric key used to decrypt the payload and the bridge server url.

## Core Architecture

The architecture consists essentially on a websocket server (Bridge) between two peers (Dapp and Wallet) that use the Client SDK.

### Requesting Connection

The initiator is the first peer that requests the connection (Dapp) by posting an encrypted payload using one-time topic used for handshake only with the connection request details to the Bridge Server and using the WalletConnect Standard URI format ([EIP-1328](https://eips.ethereum.org/EIPS/eip-1328)) passes the required parameters to establish the connection: (handshake) topic, bridge (url) and (symmetric) key.

```javascript
// Syntax

request       = "wc" ":" topic [ "@" version ][ "?" parameters ]
topic         = STRING
version       = 1*DIGIT
```

  This file has been truncated. [show original](https://github.com/WalletConnect/walletconnect-docs/blob/v1.0.0-beta/tech-spec.md)

---

**SamWilsn** (2022-05-13):

Let me prefix this (as I often do) by saying I don’t know anything about WebDev. That said, would it make sense to also support `web+wc:` as a scheme? That would be compatible with [Navigator.registerProtocolHandler](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/registerProtocolHandler).

---

**ligi** (2022-05-14):

As I think the wallet should not be in the browser context but outside the current solution is more to my liking. But no extreme strong opinion - if you can come up with a real use-case that is possible after switching to it (“also support” is not as easy I think as you can only use one URL nicely)

---

**SamWilsn** (2022-05-14):

The [Sequence](https://sequence.app/) wallet is probably the only use case I know of at the moment, and even they have a browser extension. In addition to `web+`, `ext+` could also work well with WebExtension’s [protocol_handlers](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/protocol_handlers).

---

**ligi** (2022-05-14):

That both sounds like “wallet in the context of the browser” to me. And I also think we should rather walk away from browser extensions rather than going more in that direction. But just my 2WEI.

---

**SamWilsn** (2022-05-14):

I don’t disagree about migrating away from extension/web wallets, but they do exist today, and having one library/platform that works for all wallet styles makes it easier for users to switch to the less popular options (like external program wallets.)

