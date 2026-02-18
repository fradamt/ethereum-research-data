---
source: magicians
topic_id: 904
title: Default Accounts for dApps
author: ligi
date: "2018-07-31"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/default-accounts-for-dapps/904
views: 2788
likes: 1
posts_count: 10
---

# Default Accounts for dApps

cross posting from here https://discuss.walletconnect.org/t/default-accounts-for-dapps/46

I think it would be great if the wallet-connect protocol (or perhaps the web3 provider) could support users with correlating a dApp to accounts. I think it is good digital hygiene to use different dApps with different keys - especially as there is still a lot of privacy infrastructure missing on ethereum or it is just still to expensive to use.

But UX wise this can be hard - 2 ideas to help here:

when the dApp is querying for the account

- add ability give a hint what account was used last
- save what account was used last with a certain dApp on the wallet side. I think for this we would need something like a dApp-id as the name might not be stable enough over time

## Replies

**boris** (2018-07-31):

By “account” I am assuming you mean Ethereum address. I use login / identity / wallet. An Ethereum address can represent all three, and mostly does today.

Some wallets might generate a new address per login per dapp.

On the user side, email address and one time login link for length of session is the most usable way to access. No passwords. Up to user to generate multiple emails for multiple dapp identity.

For malicious dapps this can still allow for correlation, but makes pure on chain correlation harder.

I think we need some consistent flow diagrams to help talk about this.

---

**ligi** (2018-07-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> By “account” I am assuming you mean Ethereum address.

no - not really

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> I use login / identity / wallet. An Ethereum address can represent all three, and mostly does today.

OK - perhaps we need to define these terms to get some shared context - for me this would be:

- account: keypair with possible metadata (name)
- wallet: contains account(s)
- address: identifier of account derived from the public key
- login: using an account to access something
- identity: don’t want to define this term - don’t even like to use it …-)

---

**boris** (2018-07-31):

This is going to take me some time and I’m traveling. We definitely don’t agree on all terminology ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

Thank you for the account / address disambiguation — I have struggled with that in the past.

Additionally there is the concept of a dapp account — which MAY use an account to login or MAY use a completely separate kind of login.

There is more than one kind of login to both dapps and wallet *apps*. eg every time I open The Status wallet & Chat app I need to enter a password. That is a login (perhaps native app login to differ from dapp login).

Every time I open Trust Wallet on iOS I need to enter TouchID. That is technically an authentication — my “login” of the wallet app is cached and tied to my mobile device.

Let’s move this to the wiki for these different words and a glossary / definitions.

---

**ligi** (2018-07-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Every time I open Trust Wallet on iOS I need to enter TouchID. That is technically an authentication

I disagree here - TouchID/Fingerprints are no authentication as you leave your fingerprint everywhere. Fingerprints should only be used as id/user_identifier/login_name not as authentification - you should watch some talks by starbug on this topic …

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Let’s move this to the wiki for these different words and a glossary / definitions.

very goo idea!

---

**boris** (2018-07-31):

This is not an argument about biometrics, it’s an example of a class of authentication (not login) that exists today.

The Status app asking for a password login every single time I open it on my device is a stupid pattern on mobile too ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

I think the current Web3 provider conflating account/address/login/wallet/identity is the worst ever — but it’s a pattern that exists today!

On to the wiki! ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

---

**ligi** (2018-07-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> This is not an argument about biometrics, it’s an example of a class of authentication (not login) that exists today.

I think it is not really a form of authenication - and after reading up on [Authentication - Wikipedia](https://en.wikipedia.org/wiki/Authentication) - I think identification is the right word for it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> The Status app asking for a password login every single time I open it on my device is a stupid pattern on mobile too

yea - this is really an ugly antipattern - really hope [@jarradhope](/u/jarradhope) and his team fix this at some point. Would prevent me from really using the app more than just for testing things. But there is WallETH that does not have this antipattern *SCNR* ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> I think the current Web3 provider conflating account/address/login/wallet/identity is the worst ever — but it’s a pattern that exists today!

yea unfortunately ![:cry:](https://ethereum-magicians.org/images/emoji/twitter/cry.png?v=12) cruel world - hope we can fix this mess at some point …

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> On to the wiki!

YAY!

---

**tjayrush** (2018-08-01):

This may be relevant: https://www.youtube.com/watch?v=qF2lhJzngto. It’s Alex van de Sande talking about what I think are very related ideas.

---

**boris** (2018-08-02):

Yes. Here’s that thread [ERC-1077 and ERC-1078: The magic of executable signed messages to login and do actions](https://ethereum-magicians.org/t/erc-1077-and-erc-1078-the-magic-of-executable-signed-messages-to-login-and-do-actions/351)

Anyway — step one is to have a common set of terms and some common user flows.

---

**beltran** (2018-08-03):

hey [@ligi](/u/ligi) and everyone else ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) we are also discussing those things in here

http://discuss.conflux.network/t/patterns-login/92?u=beltran

Naming and content is definitively one big area to tackle

