---
source: magicians
topic_id: 20391
title: Open Graph for Onchain Actions
author: kkonrad
date: "2024-06-26"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/open-graph-for-onchain-actions/20391
views: 483
likes: 6
posts_count: 4
---

# Open Graph for Onchain Actions

# Open Graph for Onchain Actions

Let’s work on a standard that enables EVM transactions to be previewed, signed and sent as URLs.  The idea is to be able to suggest transaction through links, QR codes, buttons, widgets and websites. This allows users to perform blockchain transactions without the need to go to another app or webpage. This would expose onchain action to the entire surface of the web. The basic idea is to do what OG did for social previews but for onchain actions.

> “The Open Graph protocol enables any web page to become a rich object in a social graph. For instance, this is used on Facebook to allow any web page to have the same functionality as any other object on Facebook.”

Any onchain action can be shared as a rich link (URL). An additional benefit is that some context aware apps such as in-wallet browsers can display additional features. For example, on a website, a swap button could trigger a transaction preview without going to a swap app.

The fallback is a simple frontend for a given action and that action only. Therefore, a user without a context aware app will be directed to that frontend to make their transaction the traditional way.

Solana has recently launched pretty much this. See the full specification [here](https://solana.com/docs/advanced/actions)

Prior art also includes [Farcaster frames](https://docs.farcaster.xyz/reference/frames/spec), which unfortunately only work with Warpcast. There is a need to agree on a standard so that we can avoid yet more fragmentation.

Next Steps:

1. hear your initial thoughts
2. start working with partners: wallets, wallet connection kits, apps.

FAQ

- What about safety and drainer links? Clients (e.g. wallets) should simulate transactions and give appropriate warnings if they cannot. Additionally, a maintained registry of non-malicious actions should exist.
- Why are we doing this? hugo0 and kkonrad have been working on a standard for a single use case URL-encoded transaction format, Peanut Protocol (sending tokens via links / QR codes) and this is a logical next step.
- What’s next? Let’s have a kick off call?

## Replies

**MidnightLightning** (2024-07-31):

I think having a potential/proposed transaction be share-able as a standardized data blob is great, including one that can be done as a QR code. Having a URL be the carrier of the data I think is good, but having it be a “rich web link” adds a layer of complexity on it that I’m not sure is helpful. In order for an Open Graph preview to work, the thing being linked to needs to have a URL that resolves to an HTML object, with special parameters in the HEAD tag. For a  basic “Alice meets Bob IRL and proposes a trade with him”, Alice would either need to have her own website, or need to use a centralized service to host her partial/proposed transaction.

An option that doesn’t require any hosting provider is Data URIs. By having the “link” that is given be structured as `data:application/json;charset=UTF-8,{"hello":"world"}`, the data can be in the URL itself.

But with the goal being to specify information about what a transaction would be, we already have a way to encode a transaction’s data: the transaction payload itself. When a wallet is asked to “sign a transaction”, they get given a raw hex version of the transaction to be signed, and then the wallet software parses that into a nice preview for the user to decide whether they want to sign it or not. The raw hex value of a transaction could be represented in a QR code (one of the “modes” a QR code can present data as is binary data). But a QR code of that nature a generic QR-code-scanning app wouldn’t know what to do with (would just be binary data).

Bitcoin has [BIP0021](https://bips.xyz/21) which defines `bitcoin:` as a URI scheme for requesting a payment in Bitcoin. On the Ethereum side, [ERC67](https://eips.ethereum.org/EIPS/eip-67) was proposed, but withdrawn, replaced by [ERC681](https://eips.ethereum.org/EIPS/eip-681). A benefit of having the request be “a URI” is that custom schemes like `ethereum:` can be registered by mobile apps, so a generic QR-code scanner knows which application(s) are able to hand that request off to directly (rather than needing to have a web browser handle the HTTP request for a “rich web link” and then try to take further action from there).

---

**kkonrad** (2024-09-06):

Thanks for pointing out the difficulties.

Regarding the first problem of Alice having to have her own website: I think it’s OK to have a number of providers with mirrors. Initially, these could just rely on a whitelist and later could be decentralised with some kind of attestation mechanism to weed out ones that resolve the link wrongly.

data: is a great suggestion but does not have the gracefull fallback of an http link.

The URI also has the problem that it’s to obscure and would require adoption from browsers (good luck). Regarding registering by mobile apps, thanks to universal linking, we can do so with HTTPS links which have the added benefit of graceful fallbacks to a website (that can e.g. prompt a user to install an app or just use a webapp).

OKX implemented it [this way](https://www.okx.com/learn/okx-multi-chain-blinks). They did so the [same way](https://medium.com/dialect-labs/introducing-the-blinks-client-sdk-8bf0e3474349) as Solana Blinks.

I think it’s best to watch the OKX+Dialect implementation and if it gets traction think about a more robust, permissionless and open source iteration.

---

**MidnightLightning** (2024-10-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kkonrad/48/10952_2.png) kkonrad:

> I think it’s OK to have a number of providers with mirrors.
>
>
> …
>
>
> thanks to universal linking, we can do so with HTTPS links which have the added benefit of graceful fallbacks to a website

I think these two ideas are at odds with each other? If this hypothetical platform focuses on “decentralized”, the top option comes to fruition (lots of web applications, with different web domains, each being a “block explorer” for “Onchain Action intentions”). But then the way that mobile app HTTPS linking works is an application needs to register which individual HTTPS web domains it wants to provide a hook for. If there are a few dozen viewer tools, wallet software would need to register hooks to all of them. And if they are decentralized (some new ones popping up frequently, and some existing ones fading away), the wallet apps would need to be frequently updating their HTTPS link list.

Some of the viewer tools for these “Onchain Action intentions” might become the more-popular tools to use, and many wallets could just focus on those, but then you’re no longer “decentralized”; you’ve got a bottleneck at a handful of hosts, where if their website is down, the whole system stalls (as is evidenced by Metamask using a specific RPC provider by default, and when that provider has an outage, it is noticed by the whole system as most users don’t change their default Metamask RPC).

I think a solution like what you’re proposing could work (as Blinks examples show they are being used), but it seems it could only grow as a centralized solution. That’s not necessarily a bad thing, but it should be labeled as such, so users know to assess it with the security questions appropriate for a centralized service, rather than a decentralized protocol.

