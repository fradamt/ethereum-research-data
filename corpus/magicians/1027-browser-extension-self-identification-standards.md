---
source: magicians
topic_id: 1027
title: Browser extension self identification standards?
author: yarrumretep
date: "2018-08-11"
category: Web > Wallets
tags: [wallet, browserextension]
url: https://ethereum-magicians.org/t/browser-extension-self-identification-standards/1027
views: 937
likes: 4
posts_count: 6
---

# Browser extension self identification standards?

Greetings Wallet Folk,

Both Trust Wallet and MetaMask inject providers that self identify with “isMetaMask” and “isTrust” fields - perhaps other do as well.  I’ve noticed some d’apps are developing if/then logic based on these fields to prompt the user to connect to the detected injected wallet (or trezor, ledger, etc).

Would it be appropriate for these injected providers to expose a generic interrogation api to determine ‘wallet name’ and ‘wallet icon url’ so as more wallets come online these d’apps need not maintain separate logic for each?

Maybe something like:

```auto
function getWalletName();
function getWalletIconUrl();
```

Best,

pete

## Replies

**MicahZoltu** (2018-08-12):

It is really terrible when dapps switch on isMetamask and similar.  That is like switching on isChrome or isFirefox when building a web page.

If users are doing this, we should figure out why and fix that, rather than make it easier for them to do it.

---

**yarrumretep** (2018-08-12):

Agreed, [@MicahZoltu](/u/micahzoltu)  - that is the intention of adding generalized identifiers.  From what I’m seeing the  d’apps are just switching on the is field in order to display a friendly menu of wallet connection options that includes the injected web3.  If the injected provider can self-identify in a general sense, then the d’app will not need to switch to provide this.

---

**yarrumretep** (2018-08-12):

One other additional interface that would be good to add is an api for the d’app to identify itself to the wallet - so the wallet can indicate the d’app with which it is working.

Something like:

```auto
setDappInfo(name: string, iconurl: string): void;
```

Wallets can then provide additional context for transaction signing or connection indication.

Is there a formal definition of the injected provider interface?  From what I can see today it comprises only:

```auto
send(payload: JsonRPCRequest): JSONRPCResponse;   // optional?? - some implementations just throw
sendAsync(request: JsonRPCRequest, cb: (e: Error, response: JsonRPCResponse) => void): void;
```

Perhaps we should formalize this interface somewhere (EIP? or just written up somewhere)?

-pete

---

**ligi** (2018-08-13):

I think this *could* make sense - kind of like a user agent string. But I agree with [@MicahZoltu](/u/micahzoltu) here that it should not really be used for switching. Perhaps it is better to not even expose it in the first place - otherwise people will switch on this information. But then things like isTrust, isMetamask are emerging - which is even worse.

What would *IMHO* really make sense is that wallets expose the features they support.  So dApps don’t switch on a particular wallet - but on a feature-set.

---

**yarrumretep** (2018-08-14):

The reason for these methods specifically is to discourage switching for the simple identification use-case - and yet to allow d’apps to provide users a sense of assurance that the d’app has connected with their wallet.  Without this, in order to provide an initial connection menu, the d’app would have to say “Would you like to connect with the *injected wallet*, Trezor or Ledger?”.  In that use case it’s useful to be able to say “Would you like to connect with *MetaMask*, Trezor or Ledger?”  Right now d’apps are switching on isMetaMask just to provide that indication (e.g. [totle.com](http://totle.com)).  We could certainly discourage switching on the name in the documentation / standard - but right now there is no other way to identify the wallet software that is injected.

I think the converse is also likely true - that the wallet might like to display a friendly name for the d’app that is sending a transaction or currently active/connected.   Hence the functions allowing the d’app to self-identify to the provider would be good.

