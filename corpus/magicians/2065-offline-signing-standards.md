---
source: magicians
topic_id: 2065
title: Offline Signing Standards
author: pedrouid
date: "2018-11-29"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/offline-signing-standards/2065
views: 1848
likes: 5
posts_count: 20
---

# Offline Signing Standards

Following the discussion at Devcon that involved initially me, [@ligi](/u/ligi), [@p0s](/u/p0s), [@ricburton](/u/ricburton) and @airgap we were looking to create a standard for Offline Signing currently supported by Walleth, Parity Signer, imToken Wallet and AirGap.

In order to achieve this there are 3 interactions that require URI standards for displaying QR Codes that can communicate between the online and offline device:

1. Expose Accounts
2. Request Transaction
3. Broadcast Transaction

Main considerations to have when drafting these 3 new URIs are that they should clearly identity the chains that they are targeting (using chainID), potentially drafting a blockchain agnostic standard and also including message signing support would be beneficial.

Currently there is a Ethereum standard for formatting URIs - EIP 831 - which would be useful for this use-case but it needs to account for other blockchains compatibility to allow Wallets to support non-EVM based blockchains that might have this Offline Signing functionality.

## Replies

**pedrouid** (2018-11-29):

I think that a good first step could be to find a solution to make the standard EIP 831 - URI Format for Ethereum to be blockchain agnostic.


      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-831)




###

Ethereum Improvement Proposals (EIPs) describe standards for the Ethereum platform, including core protocol specifications, client APIs, and contract standards.








Alternatively we could draft a new standard for URI Format for all Blockchains

---

**maciej** (2019-03-05):

Hey! I’m not in Paris, so I’ll just pitch in here.

I intend to post a standard proposal for offline wallets using QR codes that will be used by Parity Signer, which will also be extensible to non-Ethereum networks.

I’d strongly advise *against* using the URI. Couple reasons:

1. There is absolutely no reason why this format needs to be human readable. Nobody can scan a QR code with their eyes, you need an app to scan the QR, and if you’re already using an app, you can have the app decode the format used.
2. QR codes are very sensitive to the amount of data you want to show on them, with bigger loads producing higher resolution images that are problematic to scan with cheap cameras paired with low power CPUs. You want the format to be as concise as possible, especially since transactions on ethereum are variable length and can be large.
3. Given 1 and 2 - Ethereum already has a concise format for representing transactions: RLP. It’s well documented and libraries for handling it exist in plenty of languages, so there is no need to re-invent the wheel here.
4. RLP also guarantees that what we hash and sign will be exactly the same thing that will be then broadcast to the network. There is no ambiguity or room for error that could arise if we were to construct the RLP on the side of the signer form an intermediate format.
5. ERC-681 is hardly suitable for this task (it would require custom parameters to be attached, which could lead to implementation differences). ERC-831 is generic and could be adopted, but at this point we again have to invent a format that duplicates what RLP is already doing.

---

**maciej** (2019-03-12):

First draft: https://github.com/maciejhirsz/uos

---

**ligi** (2019-03-12):

the issue with nod using an URI is that the user needs to be in the correct app/state to scan. By using an uri - the user can use a generic scanning app to initiate the process. So I strongly signal that using an URI for at least step 1 is considered.

---

**maciej** (2019-03-12):

You then have to have an option to paste the URI into your signer app somehow, which means that either:

1. The device that you are storing private keys on is online, or:
2. It’s offline, but for some reason you have another app for scanning QR codes next to it.

Also ERC-681 lacks the address with which you want to sign the tx, you’d have to pick that in the signer app, which is a UX hurdle, or add it as a custom parameter. Just the fact that chunks of the URI are optional and parameters can be custom goes against the “Unambiguous” part of the design - the whole signing is only valid if both apps produce the exact same RLP out of whatever flies over the QR.

---

**ligi** (2019-03-12):

not proposing to use erc-681 here - but something custom to this use case building on 831. Or even something completely custom (with a different/shorter prefix) so more bytes can be shoved off the QR code. Perhaps with a really short scheme like wc for walletconnect …

---

**maciej** (2019-03-12):

Yeah, my thinking always goes the same route. The requirements pretty much demand a custom solution, so if we are going to engineer one, why not do one that is actually designed for this use case specifically and address all the issues (QR code resolution constraint and size limits).

I’ll look at the walletconnect, but as far as I can tell it is a very different use case, where you are also more likely to use a new phone.

I’m really pushing for the small QR codes, because my current test device for development is a samsung galaxy s4 mini, which is comparable in price to a ledger, and scanning QR codes with that thing is a pain ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=9). I reckon if people are to build dedicated hardware for this (and some are planning to do something very similar already), they are not going to put 12-megapixel iPhone X cameras on it.

---

**ligi** (2019-03-12):

I totally love the push for small QR codes! This is often overlooked and then produces problems in real world use cases - totally on your side with this.

Still think leveraging URIs could be of benefit as it adds context of what this QR code represents and e.g. allows the use of 3rd party scanners.

WalletConnect was just an example of a short schema (wc) in order to save bytes.

So perhaps we can use ot: (offline transactions)

the initial qr-code could look like “ot:address@chain”

we can drop the 0x for address and make the chain hex to save bytes.

OK we still would have this 37.5% overhead - but I think this is OK as I think the added context is worth it.

---

**maciej** (2019-03-12):

Alphanumeric QR codes have only [44 possible values](https://www.thonky.com/qr-code-tutorial/alphanumeric-table), there is no `@` sign or lower-case lettering. For a proper URI you have to use Binary encoded UTF-8, so hex is always 100% overhead, not 37.5%.

---

**ligi** (2019-03-12):

Ah right - no @ - you are correct - but we can replace this with e.g. $ or even leave it out if we assume the address is always 40nybbles

---

**maciej** (2019-03-12):

Or you could go with Binary UTF-8 and use base64 or base58, both of which have (slightly) smaller overhead. Whichever you do though, at this point you have something so custom I don’t really see an advantage in using URI-compatible format over just prefixing things with raw bytes.

---

**ligi** (2019-03-12):

intent-filters do not work on raw bytes

---

**maciej** (2019-03-12):

Ah, right, I see. So you could say slide into the default camera mode, scan the QR code and have it just open the signer app. We could use short a URI prefix and then keep everything else binary with base64/58/whatever.

I’d like to know if anyone has done any UX research if that’s something people are likely to do. I haven’t seen any users complain about it to us with the signer (which is using the non-URI JSON payload atm).

---

**ligi** (2019-03-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/maciej/48/917_2.png) maciej:

> We could use short a URI prefix and then keep everything else binary with base64/58/whatever.

that sounds great - but as I said on twitter I think Base58 is a bad choice here:

https://twitter.com/mr_ligi/status/1105567368108015621

---

**maciej** (2019-03-12):

Ye, I’ve seen that. AFAIK `data:` URIs are using base64, so I don’t see why we would run into issues there, but I don’t know what intent-filters do or don’t let you do.

---

**ligi** (2019-03-12):

yea - but data URI’s are URIs  - so there is no problem there.

With intent-filters I can match e.g. on a scheme - basically on parts of an URI. But I cannot inspect binary blobs or json. You cannot have custom code there - just matchers which are quite limited

---

**maciej** (2019-03-12):

I know, I’m just saying that if base64 is legal in `data` scheme, it should be legal in a custom scheme for intent-filters, unless iOS/Android are being weird about it ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=9).

---

**ligi** (2019-03-12):

no - base64 is legal there - I do not really care much of what’s behind the scheme - I mainly feel strongly we should have a scheme so I can match it with some intent filter ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

---

**maciej** (2019-03-12):

Ok, so two ideas I have now.

1. Use alphanumeric QR code and base-x with 44-40 character set (that’s ~0-3% overhead).
2. Use a normal scheme URI with base64 encoding, but only when executing URLs from other apps as an extra feature, not in QR codes (that I think would make it applicable to AirGap model).

