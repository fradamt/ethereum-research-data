---
source: magicians
topic_id: 16536
title: "ERC-7555: Single Sign-on for Account Discovery"
author: greg
date: "2023-11-10"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7555-single-sign-on-for-account-discovery/16536
views: 3277
likes: 6
posts_count: 5
---

# ERC-7555: Single Sign-on for Account Discovery

This proposal establishes a standardized interface and functionality for applications to discover user addresses that may not be readily available from an EOA. Specifically discovering addresses and smart accounts that may have been deployed or configured using a signing key that is not the standard Ethereum secp256k1 curve. The objective is to ensure uniformity of address retrieval across applications, and domains.

https://github.com/ethereum/ERCs/pull/99

Note: This EIP has an accompanying EIP [Embedded Accounts as Smart Modules](https://ethereum-magicians.org/t/erc-xxxx-embedded-accounts-as-smart-modules/16537), that extends the functionality of this one.

## Replies

**mac** (2023-11-11):

Webauthn (you call it passkey) does not force you to create anything – creating a public keypair (per origin) is just the tip of the iceberg, it can do so much more (prf, largeBlob, payment).

If you’re going to try to convince us to let centralized providers like walletconnect bring SSO to webwallets,  why aren’t they building it on the web standard FedCM?

It’s already in:

chromium

firefox nightly

Positive signal from webkit

It survived the google-dreaded mozilla review, now offering a privacy preserving /login endpoint, and preventing RPs from enumerating user accounts.

It also makes it dumb-easy for RPs to implement, using credentials.get()

![:point_down:](https://ethereum-magicians.org/images/emoji/twitter/point_down.png?v=12)



      [github.com](https://github.com/fedidcg/FedCM/blob/main/explainer.md)





####



```md
# Federated Credential Management (FedCM)
**Last Update:** Mar 08, 2022

## Introduction

Over the last decade, identity federation has played a central role in raising
the bar for authentication on the web, in terms of ease-of-use (e.g.
password-less single sign-in), security (e.g. improved resistance to phishing
and credential stuffing attacks) and trustworthiness compared to per-site
usernames and passwords. In identity federation, a **RP (relying party)** relies
on an **IDP (identity provider)** to provide the user an account without
requiring a new username and password.

Unfortunately, the mechanisms that identity federation was designed on (iframes,
redirects and cookies) are being abused to track users across the web. A user
agent isn’t able to differentiate between identity federation and tracking, the
mitigations for the various types of abuse make identity federation more
difficult.

The Federated Credential Management API provides a use case specific abstraction
```

  This file has been truncated. [show original](https://github.com/fedidcg/FedCM/blob/main/explainer.md)










We can do better here … ![:fairy:](https://ethereum-magicians.org/images/emoji/twitter/fairy.png?v=12)

---

**greg** (2023-11-11):

[@mac](/u/mac)

Thanks for flagging this!

First things first. FedCM looks reaaaally good, and should be discussed in a wider context! Happy to facilitate!

I want to make sure we’re using the same definitions, so let me articulate how I’ve described things, hopefully I haven’t missed something ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

> Webauthn (you call it passkey)

Webauthn is specification for a browser based API for public key crpyto. You can *almost* related it to EIP-1193, in the same sense how does a browser communicate with a wallet. To be even more concrete, an iOS app deployed through the native app store **does not** use webauthn when using passkeys, it will instead use the native `ASAuthorization APIs`. When I say passkey, I’m referring to the curve p256.

The main reason I’m explicit about that differentiation is because this EIP in my opinion shouldn’t care *how* a key is generated, nor what type it is (theoretically you could be generating BLS keys for a user).

> convince us to let centralized providers like walletconnect bring SSO

So I actually would prefer people not use them! Let me articulate how. The provider side logic needed to *discover* and *respond* back to an application should be stateless. Meaning you shouldn’t need an centralized server what so ever to do anything for you, a website with an IPFS hash is sufficient.

(fwii @ ChainSafe we’re working on this demo should have it at somepoint early next week)

Let’s imagine web3modal, it now hows a text box that says “enter url”, that url can be **anything**, native ios/android app deep linking, a website, localhost, it doesn’t matter. In this case, I will say its [sso.gregthegreek.com](http://sso.gregthegreek.com) (doesn’t exist), my personal website. On this website, I have implemented:

- Passkey (via Webauthn)
- Web3modal (for injected browser wallets, like metamask)
- Native Ledger support
On this website, I can select any of the above options to determine a public address that I want to use for the app I was previously on. Once I’ve selected a “login” option, the website automatically knows how to “discover” if that public key has an associated smart contract wallet, perhaps via create2. Per ERC-7555 I would respond with all that information.

As you can see, this ERC allows support of any signing algo. It also isn’t opinionated on what tech to use. The redirect in my example above using web3modal (walletconnect) you can completely skip that! You can just have a list of url’s and call `window.location.redirect(url)` and never even show any third parties!

This ERC extends the possibility of decentralizing 4337 wallet creation, and utilization which is currently heavily gated by APIs. The same way running a dappnode at home, and setting that as a custom RPC decentralizes you away from centralized RPC providers.

I hope that helps explain things a bit better, I love criticism, so lets keep finding holes.

I think using FedCM would probably need to be an effort discussed within the 4337 community more widely.

---

**dror** (2023-11-11):

I have a problem with the basic assumption of this ERC:

It assumes that for every signing key (public key over some curve), there exists a single smart contact account address.

It attempts to copy the same basic trait from EOA accounts, where the account address is derived from the public key.

However, this completely ignores the major feature of smart accounts, which is the ability to *change* the keys: once created, an account can change its keys.

Another major feature of smart accounts is that the account is defined by much more than the signing key.

Even if the account is modular, the address of the account is defined by the actual initial deployed modules, which again, defines much more than the signature method.

The bottom line is that the signing key is just one of many parameters needed to define the account address, and I strongly recommend NOT relying on it at all as a unique identifier.

---

**greg** (2023-11-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dror/48/2438_2.png) dror:

> Another major feature of smart accounts is that the account is defined by much more than the signing key.

Everything you mention makes sense and I believe is well covered in this ERC.

> It attempts to copy the same basic trait from EOA accounts, where the account address is derived from the public key.

Not exactly, it’s up to the 4337 provider to determine *how* to find the smart contract wallet. A single credential can have *many* SCWs, and a 4337 provider should display all known wallets it has access to.

> The bottom line is that the signing key is just one of many parameters needed to define the account address, and I strongly recommend NOT relying on it at all as a unique identifier.

As I brought up before, I don’t think that we’re explicitly saying a 4337 provider has to use a signing key as the unique parameter. The ERC explicitly doesn’t care about what a provider does to recover the SCW address, there could be a multitude of varying parameters on how to recover it. For example:

A provider could have google-auth, and uses a database to keep track of deployments, they can also track ownership changes and maintain a clean history for the end-user. In this example, on-redirect, the user is prompted via google auth, they do a lookup in the db, then return the SCW address and signing key. Furthermore, imagine the signing key was a passkey, in this example the end user never even needs to be prompted for their passkey. Now this might not be an ideal or good practice for handling it, but its 100% possible and articulates how non opinionated this ERC is.

