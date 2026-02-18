---
source: magicians
topic_id: 3569
title: "Discussion: ENS Login"
author: cwhinfrey
date: "2019-08-21"
category: Magicians > Primordial Soup
tags: [ens]
url: https://ethereum-magicians.org/t/discussion-ens-login/3569
views: 5068
likes: 12
posts_count: 8
---

# Discussion: ENS Login

At the Meta Cartel Demo Day ETH Magicians ENS discussion we presented an idea for an open standard for logging in with ENS. I’d like to open up the discussion here for further discussion. The idea was inspired by Universal Logins and Web3Connect.

**Description:**

ENS allows users to [store data in a key value store](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-634.md) associated with a given ENS name. To allow for a wallet agnostic login widget (example below), users can add urls to web3 providers in their ENS name’s key value store under keys such as “provider-mainnet”. In the widget users can enter their ENS name and click “log in”. The widget can then look up the appropriate provider URL in the ENS contract and then download the provider from that URL. The provider can then be passed to the dapp which will then instantiate web3 (or other alternatives) with the provider. (e.g. `var web3 = Web3(provider)`). As [@danfinlay](/u/danfinlay) suggested [here](https://twitter.com/danfinlay/status/1163583938440208384), a user could register different providers for each network. It was also suggested by [@cmeisl](/u/cmeisl) that users could register different providers to be used on desktop vs mobile.

We plan to build a PoC (with [@shane](/u/shane), [@amxx](/u/amxx), and [@dobrokhvalov](/u/dobrokhvalov)) for our ETHBerlin hack and then write up a draft of the standard but wanted to open up the discussion for ideas, suggestions, and concerns from the rest of the ETH Magicians community in the meantime.

[![ENS%20Login](https://ethereum-magicians.org/uploads/default/optimized/2X/b/ba6661277d652445e062d54b2255fdc89e4532ed_2_690x427.png)ENS%20Login919×570 34.3 KB](https://ethereum-magicians.org/uploads/default/ba6661277d652445e062d54b2255fdc89e4532ed)

## Replies

**Kisgus** (2019-08-27):

Great stuff. Is it possible to already play with the ETH Berlin prototype you guys build?

---

**danfinlay** (2019-08-29):

I guess this requires making your preferred provider type public. That’s probably not a very big privacy/security issue, but is probably worth making clear on whatever interfaces are provided to help users declare their preferred client.

---

**Dobrokhvalov** (2019-09-17):

Hey guys, we’re working on a demo with iframes sandboxing wallet providers described here - https://gist.github.com/Dobrokhvalov/3e5294cdbd2c28ed175477a3aacb9987

Will share soon. Is anyone else working on a demo or something?

And I’ve recently stumbled on a relevant work, Kirby - https://blog.joincivil.com/kirby-and-the-birth-of-wall-apps-bd6ce396e229. Might be useful to check it out.

---

**makoto** (2019-10-15):

Hello. We had a small get together and here is the summary.

# ENS Login meetup in Osaka

## Participants

- Makoto
- Chris
- Hadrien

## Topics

- Hardian and Chris worked on drafting EIP = snapshot of the spec. Will link it once the atual EIP is raise.
- Experimental integration into ENS manager
- Added instructions on how to integrate

---

**Amxx** (2019-10-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/makoto/48/153_2.png) makoto:

> Experimental integration into ENS manager
> Added instructions on how to integrate

Since then I started a “login with ethereum” react object.

- Code is here
- Example of (very simple) use is here

---

**fubuloubu** (2020-02-21):

Was just reading the latest version of [ERC-2525](https://github.com/ethereum/EIPs/pull/2525). A couple thoughts:

- Ensure either some measure of privacy about the user’s choice of which client they use, or a robustness to the paths of their choice such that the choice could not be faked by a malicious dapp in order to target them and their cryptocurrency. I’m not quite sure how one would go about doing this, but it is important if this preference were to live on-chain that there is guards against such malicious behavior on the user side.
- Internationalization choices might be nice to consider as a part of this standard. See ERC-1444 for inspiration or integration: EIP-1444: Localized Messaging with Signal-to-Text
- Not sure if this is the right place, but it seems related to the idea I’ve been considering with ERC for "Execute as". The basic idea of having a set of handlers that the user chooses for how their web3 connection should be handled (and how transactions are submitted, etc.) would integrate nicely here. Instead of maintaining a bunch of dapp-specific or wallet-specific functionality, this could serve as a common standard for translation of multi-party, smart-contract based accounts to the front-end user. If it makes sense, please consider that with this proposal.

---

**vilafan** (2022-06-01):

The basic idea is that you might want to use your Ethereum address as an identifier in the same way that you can use an email address, phone number, or some other identifier to log in to various applications. Here you can hire [resume writers in australia](https://www.au-resumesplanet.com/) to manage your thesis task easily. This would allow other applications to automatically verify that you are who you say you are, without requiring any central authority or third-party authentication service.

