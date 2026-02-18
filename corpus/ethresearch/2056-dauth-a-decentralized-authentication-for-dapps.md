---
source: ethresearch
topic_id: 2056
title: DAuth - A decentralized authentication for DApps
author: madhavanmalolan
date: "2018-05-23"
category: Applications
tags: []
url: https://ethresear.ch/t/dauth-a-decentralized-authentication-for-dapps/2056
views: 3985
likes: 0
posts_count: 3
---

# DAuth - A decentralized authentication for DApps

# Introduction

DAuth is a replacement to OAuth based authentication systems like “Login with Facebook”, “Sign in with Google”.

# Motivation

I was building a DApp, and realized there is no way for the user to deterministically say which ethereum address she owns without using MetaMask or other Web3 providers and are instantaneous.

Let us take the example of CryptoKitties. Though making any transaction like selling/buying should need MetaMask - just viewing my kitties should be possible on any device that may or may not have Web3, using a simple username password.

# Solution

I created a simple protocol describing the exchange of messages, in a way similar to OAuth. This uses an authentication server that can be self hosted by the user. The identities and the authentication flow is determined by a smart contract.

All logins are instantaneous and free of transaction costs.

# More information

## GitHub

https://github.com/madhavanmalolan/dauth

## Whitepaper

[dauth.pdf](https://github.com/madhavanmalolan/dauth/blob/master/dauth.pdf)

# Demo

https://dauth.co

# Disclaimer

I am relatively new to designing decentralized systems, I would love to hear your feedback on this ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Looking forward to help the community at [ERC 1115](https://github.com/ethereum/eips/issues/1115)

## Replies

**kowalski** (2018-05-24):

It’s not clear to me why you need to generate additional private/public key pairs. Ethereum address is defined by its private key. You can use it to sign a message using `web3`:

```javascript
import ethUtils from 'ethereumjs-util';

const msg = ethUtil.bufferToHex(Buffer.from(data, 'utf8'));
const signed = await asyncCall(web3.personal.sign, msg, account);
```

where `account` is the public address you what to prove you own.

On the receiving side you can verify the signature using:

```javascript
import { recoverPersonalSignature } from 'eth-sig-util';
import { bufferToHex } from 'ethereumjs-util';
import { toLower } from 'lodash';

function checkSignedData({ sign, data, account }) {
  const msg = bufferToHex(new Buffer(data, 'utf8'));
  const params = { data: msg, sig: sign };
  let pub;
  try {
    pub = recoverPersonalSignature(params);
  } catch (e) {
    return false;
  }
  return toLower(pub) === toLower(account);
}
```

---

**madhavanmalolan** (2018-05-24):

I generate an additional pair of keys for the following reasons

- A user may not always have Web3 installed on the browser they are using with their account unlocked. Consider the example of signing in into your CryptoKitties account from your friend’s machine. If you do not have the same account imported on the device you are using, you are pretty much locked out of your own account.
- Using independent keys are also to ensure that identification is decoupled from the payments workflow. I do not expect every layman to set up their own HTTP server to handle the login requests. Decoupling the keys allows one to trust someone else with the identification private keys if need be, at the same time be totally sure that their ETHs are perfectly safe no matter what. Should the Server that hosts their private key be compromised, they can always change the keys and register with a new server or set one up themselves.

