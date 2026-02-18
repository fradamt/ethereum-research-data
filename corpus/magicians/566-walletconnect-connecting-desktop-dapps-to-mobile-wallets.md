---
source: magicians
topic_id: 566
title: WalletConnect - Connecting desktop Dapps to mobile Wallets
author: pedrouid
date: "2018-06-18"
category: Web > User Experience
tags: []
url: https://ethereum-magicians.org/t/walletconnect-connecting-desktop-dapps-to-mobile-wallets/566
views: 3942
likes: 3
posts_count: 7
---

# WalletConnect - Connecting desktop Dapps to mobile Wallets

Hi everyone

If you haven’t heard of WalletConnect it’s an open-source project that enables desktop Dapps to interact with mobile Wallets. Richard [presented it](https://www.youtube.com/watch?v=94-z6-JQXek) on Web3 UXUnconf

The user flow is pretty simple, the user scans a QR code to initiate a session which then allows the Dapp to retrieve the user’s accounts. From there, the user can use the Dapp freely on desktop and once there is any messages or transactions to be signed, they are pushed to your phone as a notification and the user can view and signed them securely.

Video Demo: https://twitter.com/ricburton/status/978509303500984320

This UX removes the requirement to install a browser extension and opens up a whole world of Dapps to all mobile wallets available on iOS and Android. It also provides the ability for the user to manage their assets with one wallet without being tidied to one desktop or having to move their seed phrase from one application to another.

I wanted to open this topic to engage with anyone who wants to contribute to this project and add their inputs to the discussions as we develop new standards or features to this protocol.


      ![image](https://github.githubassets.com/favicons/favicon.svg)

      [GitHub](https://github.com/WalletConnect)



    ![image](https://avatars.githubusercontent.com/u/37784886?s=280&v=4)

###



Open protocol connecting Wallets to Dapps. WalletConnect has 111 repositories available. Follow their code on GitHub.










Looking forward to hear your opinions and suggestions!

## Replies

**MicahZoltu** (2018-06-19):

How does it compare to Parity’s mobile hardware wallet?

---

**pedrouid** (2018-06-19):

Parity Signer involves a lot more QR code scanning so technically there is not message relaying through any sort of infrastructure

While Parity’s implementation you have to scan QR code both from desktop and mobile with WalletConnect’s implementation you only scan the QR code once and all of the comunications are relayed through a Bridge server. The information is never accessible by the Bridge as the session is initiated between the desktop and the mobile with a QR code that shares a ephemeral key for encrypting all messages

These messages are very simple and do not share any critical data that could expose the wallet but secure it from being tampered with, here is the technical walkthrough of the WalletConnect implementation:

Creating a session:

1. Desktop pings Bridge to create a session ID
2. Desktop generates ephemeral shared Key
3. Desktop shares session ID, bridge URL and shared Key with Mobile using a QR code
4. Mobile scans the QR code and obtains the session data

*** immediatelly after scanning the QR code ***

Getting Accounts:

1. Mobile is prompted to initiate the session and share wallet Accounts
2. Mobile encrypts Accounts with shared Key and sends it to the bridge URL using the session ID
3. Desktop listens to session ID change and fetches encrypted Accounts
4. Desktop decrypts Accounts with shared Key

*** at this points the user can freely use the Dapp without worrying about the Mobile wallet until it needs to sign something ***

Transaction Request:

1. Desktop encrypts a transaction request with shared Key
2. Desktop sends encrypted transaction request to the Bridge using the session ID
3. Bridge notifies the mobile Wallet of the transaction request by push notification
4. Mobile fetches transaction request and decrypts with shared Key
5. Mobile displays transaction request to the User to be signed
6. Mobile shares the status of transaction request (reject or approved with tx hash)

PS - I missed one part of the infrastructure for clarity of the explanation. The Mobile wallet shares with the bridge a device ID when initiating the session. This device ID is used to trigger a push notification on the Push server (managed by the Wallet developer)

---

**fubuloubu** (2018-06-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png) pedrouid:

> Mobile is prompted to initiate the session and share wallet Accounts
> Mobile encrypts Accounts with shared Key and sends it to the bridge URL using the session ID
> Desktop listens to session ID change and fetches encrypted Accounts
> Desktop decrypts Accounts with shared Key

So, the desktop receives a copy of the encrypted key, therefore it is transporting this encrypted key over a secure pipe? Is the desktop supposed to destroy this key after the session?

---

**pedrouid** (2018-06-19):

There is only shared Key that is being used for encryption between the Desktop and the Mobile.

This key is generated on the Desktop and is shared with the Mobile using the QR code when initiating the session

The session management/lifetime is however a great question.

There are several determining factors in this matter that we have discussed so far:

1. Should the session lifetime be controlled by the Mobile wallet or fixed by the WalletConnect standard/library?
2. How long should we allow the Desktop dapp to expose this shared key? Specially regarding browsers local storage which is vulnerable and exposing this shared key could open vulnerabilities for phishing and spam.
2.1 Would a Dapp smart contract registry prevent phishing from having this shared key expose?
2.2 Could a User control the authorization from its Mobile wallet without requiring a session lifetime?
2.3 Should we scan the QR code every time the user initiates the session without persisting the session?

Currently the Bridge is persisting the session ID for 24 hours (totally arbitrary decision) but this session ID is useless if the shared Key discarded by the Desktop (example when refreshing a web page without persisting with local storage)

---

**fubuloubu** (2018-06-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png) pedrouid:

> Should the session lifetime be controlled by the Mobile wallet or fixed by the WalletConnect standard/library?

I think a 24 hour window is probably fine, but either client using the bridge should be allowed to close it. This way, you could program something in like proximity via bluetooth or wifi where both clients will actively close the bridge when it leaves the coverage area. A laptop might also close if the screen is shut, or even on demand if the user requests it in the mobile wallet (temporary login on a new device)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png) pedrouid:

> How long should we allow the Desktop dapp to expose this shared key? Specially regarding browsers local storage which is vulnerable and exposing this shared key could open vulnerabilities for phishing and spam.

Both devices can be vulnerable in a multitude of ways. Mobile apps have better guarantees because they’re sandboxed, I hope eventually key management is handled in a similar way for laptops/desktops.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png) pedrouid:

> Would a Dapp smart contract registry prevent phishing from having this shared key expose?

That’s one way. Or could just use ENS subdomain for the application’s IP address. No expert here, but [@alexvandesande](/u/alexvandesande) had something along these lines he presented at the UX unconf (although I think identity contracts are a harder sell then application contracts)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png) pedrouid:

> Could a User control the authorization from its Mobile wallet without requiring a session lifetime?

Close the bridge?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png) pedrouid:

> Should we scan the QR code every time the user initiates the session without persisting the session?

Define “intiating a session”? If that you mean “log into the device”, then that’s not too bad for UX. If you mean every time you load a webpage, that sounds bad.

---

**pedrouid** (2018-07-16):

Created a new discourse for WalletConnect to get into more detail for all components of the standard

https://discuss.walletconnect.org/

