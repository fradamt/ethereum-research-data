---
source: magicians
topic_id: 2742
title: "EIP ERC App Keys: application specific wallet accounts"
author: Bunjin
date: "2019-02-26"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-erc-app-keys-application-specific-wallet-accounts/2742
views: 12968
likes: 43
posts_count: 39
---

# EIP ERC App Keys: application specific wallet accounts

Hi everyone,

Our research at MetaMask has lead us to propose the following EIP and we would very much appreciate if the community gave us feedback such that we can come to an agreement on a standard that would be appropriate both for wallets and applications developers to guarantee cross-compatibility.

https://github.com/ethereum/EIPs/pull/1775

**Simple Summary:**

Among others cryptographic applications, scalability and privacy solutions for ethereum blockchain require that an user performs a significant amount of signing operations. It may also require her to watch some state and be ready to sign data automatically (e.g. sign a state or contest a withdraw). The way wallets currently implement accounts poses several obstacles to the development of a complete web3.0 experience both in terms of UX, security and privacy.

This proposal describes a standard and api for a new type of wallet accounts that are derived specifically for a each given application. We propose to call them  `app keys` . They allow to isolate the accounts used for each application, thus increasing privacy. They also allow to give more control to the applications developpers over account management and signing delegation. For these app keys, wallets can have a more permissive level of security (e.g. not requesting user’s confirmation) while keeping main accounts secure. Finally wallets can also implement a different behavior such as allowing to sign transactions without broadcasting them.

This new accounts type can allow to significantly improve UX and permit new designs for applications of the crypto permissionned web.

**Abstract:**

In a wallet, an user often holds most of her funds in her main accounts. These accounts require a significant level of security and should not be delegated in any way, this significantly impacts the design of cryptographic applications if a user has to manually confirm every action. Also often an user uses the same accounts across apps, which is a privacy and potentially also a security issue.

We introduce here a new account type, app keys, which permits signing delegation and accounts isolation across applications for privacy and security.

In this EIP, we provide a proposal how to uniquely identify and authenticate each application, how to derive the accounts along an Hierachical Deterministic (HD) path restricted for the domain and we finally define an API for applications to derive and use these app keys. This ERC aims at finding a standard that will fit the needs of wallets and application developers while also allowing app keys to be used across wallets and yield the same accounts for the user for each application.

**Elements to discuss:**

The motivation of this ERC is to get feedback about the following points:

- Applications Hierarchical Deterministic Path
- The use of personas
- Applications unique identifiers (uid) and applications authentication
- Uid slicing for HD path
- Application Customisable sub path
- Api methods

Thanks, looking forward to discuss this with the community!

Vincent

## Replies

**jpitts** (2019-02-26):

Cross-referencing to a recent post by someone who was pointing out that we should value privacy more ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png)
    [Meta: we should value privacy more](https://ethereum-magicians.org/t/meta-we-should-value-privacy-more/2475) [Primordial Soup](/c/primordial-soup/9)



> Right now, Ethereum privacy is quite lacking. There are two reasons why. First, all of your activity is by default done through a single account, so it is all linkable on-chain. Second, and more insidiously, even if you have multiple accounts that you split your activity between (ideally, the default would be to use a different account for each application), the fact that you need to transfer ETH between accounts to pay for gas on all of them is itself a privacy leak.
> This is a situation that c…

---

**danfinlay** (2019-02-26):

A couple other points I’d like to highlight:

- Eventually this proposal could be extended to support other cryptographic curves, facilitating alternative cryptography like zk-STARKs.
- While this proposal generates a path for key generation per domain, a delegation system could allow groups of distinct domains to coordinate securely.
- To revoke these keys the client will need to keep track of the revoked keys, and skip them when generating keys in the future. This is an important requirement of any wallet implementing this standard (personal side-chains, anyone?).

---

**wighawag** (2019-02-27):

This is a great proposal!

This should allow for so much nicer user interface.

I have been thinking along these lines for quite some time and I ll here shamlessly plug my related proposals as I think they bring a different perspective that might be helpful to be aware of:

1. 3 Proposals For Making Web3 A Better Experience

There is 3 proposals in there. The two on signature are similar to appkey in intent but use the main account (no isolation) and is restricted to EIP712 signature in its current form. it allows them to be used without modification, except for an extra domain Seperator field in EIP712.

The one on encryption could be applied to app keys.

In that article, it is also mentioned the idea of smart contract domain approval by users. This would allow users to stay in control of which domain has the right to act on behalf of the users on each smart contract following the standard. For app keys I guess this can be done via address. Any plan to standardise such in this proposal?

1. Automatic Authentication Signature

This one (modified in this direction by [@pedrouid](/u/pedrouid)) could also be used for app keys to let `wallet.appkey.enable` return an authenticated account by passing a challenge to the request, instead of having the application to do a signature request on top.

As for general comments, I ll have a closer read later, but few things jumped to mind :

the option to use app keys per content hash is I think very important for fully decentralised app where even the app creator and ENS name owner should be considered malicious. Relying on the ENS is prone to vulnerability as you mentioned. ENS should be used for discoverability not as the basis for security. As such app key should ideally be using the contentHash for the domain, when such is used.

Having said that I think it could also be an option to have app keys for ENS names to allow application to update without having to scare their users with another enable popup or share data with earlier version easily. This should be clearly indicated to the user though as a warning when accepting such ENS name based app keys.

Similarly: App keys should work with DNS names. I am not sure I understand the rational behind refusing them. Is it really not possible to come with a normalization scheme similar to ENS ?

Looking forward to play with such proposal!

---

**Bunjin** (2019-02-27):

Hi Ronan, @widhawag, good to get your feedback!

I’ll take the time to review the links and your post in details, but for now I had a quick comment about your last part:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> Similarly: App keys should work with DNS names. I am not sure I understand the rational behind refusing them. Is it really not possible to come with a normalization scheme similar to ENS ?

Agreed that we should find a way to support non ENS names (both for generality and to remove the requirement to register an ENS domain). DNS names are indeed a good candidate and should be fairly easy to support.

Looking forward to discuss this more.

---

**BradleyC** (2019-02-27):

Something like this is definitely needed. I’d like to engage with it more but initial reaction - *it seems like the system should be designed to accommodate all DNS names*. I also wonder how long it will be safe to trust the domain model - if there is a valuable payload it may become worthwhile to attempt to access wallets from forged domains.

Perhaps we can accept any app regardless of domain by requiring apps to use their own public / private keypair. Then the user proactively trusts the app (identified by keypair and not a hash of the name) similar to adding a public key to ssh `authorized_keys`.

**Edit: an alternative to generating new accounts per app could be to leverage existing TLS certificates, since most web hosts (whether VPS or AWS style providers) have secure mechanisms built in to store secure signed data.

---

**cartercarlson** (2019-02-27):

I definitely agree that the EIP should offer support for all DNS names (assuming support for ENS), and with DNS names you could uniquely identify addresses just like ENS.  Overall, I know there’s a different process to make a subdomain tied to a unique address on DNS than on ENS.

Short term focus on DNS support could slow down overall progress on this EIP.  With other teams working on integrating DNS services with Ethereum addresses, DNS implementation may be out of the scope of this EIP.

If this EIP focuses solely on ENS app accounts, other EIPs should come out to improve DNS standards of Ethereum address creation. As soon as that happens, it should be easy adding a feature for DNS support.

---

**light** (2019-02-27):

> They allow to isolate the accounts used for each application, thus increasing privacy.

It could be worth enumerating on the use-cases where these app keys could increase privacy, and to document how a user can take advantage of this feature to protect privacy.

For example if all a user is doing with these keys is signing messages, I can see it being relatively easy for a wallet to keep them isolated and thus prevent correlation between the keys. But if a user begins transacting with these keys, and funding them from their main account(s) then it becomes trivial through blockchain analysis to correlate the keys and provide a confidence score that they are owned by the same user.

---

**boris** (2019-02-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/light/48/838_2.png) light:

> But if a user begins transacting with these keys, and funding them from their main account(s) then it becomes trivial through blockchain analysis to correlate the keys and provide a confidence score that they are owned by the same user.

Yes, thank you for raising this. Anything that doesn’t solve this is no better than what we have now.

---

**Bunjin** (2019-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/light/48/838_2.png) light:

> It could be worth enumerating on the use-cases where these app keys could increase privacy, and to document how a user can take advantage of this feature to protect privacy.

Agreed.

So indeed if all an application needs to do with its keys is to sign messages and it does not require funding, then this EIP allows for privacy through the use of distinct keys for each application with a simple deterministic standard compatible across wallets.

However if these application keys require funding, indeed there can be trail and the use of app keys would not fully solve the privacy problem there indeed.

A few comments however about this:

- Mixers or anonymous ways of funding an ethereum address (ring signatures) along with this proposal would guarantee privacy
- Even if privacy is not solved fully without this anonymous funding method, we still need a way to easily create and restore different accounts/addresses for each application

And importantly, this EIP is not only about privacy, it’s also about delegation. So even in the case where your application require funding and that we have no way to obfuscate the funding trail, I really think that there is a lot to benefit from using this standard to derive accounts specific for the application for which I can delegate signing and to use these only for a single application.

Current situation where accounts are used for several different applications and for transacting is both a privacy and a security concern but also very painful to manage if you are going to have to remember which account you are using for each specific application, and there is no standard for this to be managed in a compatible way across wallets.

So even if this is not the end of the story for the privacy problem when you need to fund the app accounts, this EIP is a potential prerequisit since any private funding method will require seperate accounts and it also brings other benefits such as delegation and UX improvements.

---

**Bunjin** (2019-03-03):

Added support for DNS names, using the ENS hashing scheme and authenticated by the wallet through the loading of the DNS webpage.

This can create some ambiguity when using ENS names that point to an DNS url. Thus adding an option in the .enable() that allows to specify which of the 2 the app would like to use for the app keys derivation path.

[@wighawag](/u/wighawag), I’m still reviewing your links and comments, but your comments suggested me to add the following to the appkeys.enable method:

- .enable() now returns the app’s root account extended public key. This should allow for the app to derive all non hardened child public keys.
If enable() options also include a challenge string the wallet will sign it with the app’s root account and will return the signature.
This should allow the applications to safely authenticate the users by verifying that they indeed own the private key of the public keys they are claiming to own.

Here is the commit that includes most of these changes:

https://github.com/ethereum/EIPs/pull/1775/commits/d69b5d101639ff01a9ec1e2ce50116e331020c5f

Thanks again everyone for all the comments!

---

**danfinlay** (2019-03-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bunjin/48/1580_2.png) Bunjin:

> .enable() now returns the app’s root account extended public key. This should allow for the app to derive all non hardened child public keys.

We should find a way to support this behavior without breaking the current API for other sites, possibly by adding a new option to the enable call.

---

**danfinlay** (2019-03-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Anything that doesn’t solve this is no better than what we have now.

It isn’t *much* better for privacy, but some sites use signatures only to authenticate, and for them it is infinitely better for privacy.

Also like Bunjin wrote, this is a prerequisite to other anonymization strategies like mixers.

---

**boris** (2019-03-03):

I’m totally in favour of the steps here (insofar as I understand them!) – I was quoting a very specific point that [@light](/u/light) made. If out of the box all the keys can be correlated – then this is a step *backwards*.

Theoretically today I can have multiple addresses and do my own app / key management. Was it Cipher Browser that generated like 10 addresses for you but you couldn’t label them or do anything other than switch between them?

The same as having multiple email addresses where it’s all my own opsec to keep them from not being correlated.

So perhaps this is better in the form of a question [@danfinlay](/u/danfinlay) : given this method, how much can an external actor correlate? Can they trivially (just using the chain, not IP address or browser fingerprinting) correlate my fluffy-puppies address with my hardcore-metal address?

---

**Bunjin** (2019-03-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> We should find a way to support this behavior without breaking the current API for other sites, possibly by adding a new option to the enable call.

No worries there, for now it’s appkeys.enable(), a separate method than the EIP1102 .enable().

Not sure if we should merge them or not.

---

**danfinlay** (2019-03-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> given this method, how much can an external actor correlate? Can they trivially (just using the chain, not IP address or browser fingerprinting) correlate my fluffy-puppies address with my hardcore-metal address?

The app key is not correlated at all by default (it is generated from a hardened HD derivation path), but could be correlated by whatever means the account was funded.

So it’s privacy until funding, or continued privacy if the funding source can be obfuscated.

There would theoretically be an XPub key capable of proving the correlation of an account and all of its app keys, but this proposal does not include any method for sharing that XPub at this time.

---

**boris** (2019-03-07):

Great. Funding correlation of multiple accounts is already where we’re at, so this is at least as good as that. Thanks!

---

**danfinlay** (2019-03-09):

Oh I did partly misspeak about the possibility of sharing an Xpub on this path, but the point you took away is the same. Vincent will clarify soon.

---

**Bunjin** (2019-03-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> about the possibility of sharing an Xpub on this path

App Keys of each application are isolated one from another across applications because we harden the derivation path for each application keys.

So even if you had the root extended public key (coming from the mnemonic), you would not be able to compute the child public keys of any application’s keys.

However, once at the application level, since the application sub path is not constrained, an application can choose to use non hardened indexes and would thus be able to compute the extended public keys (and thus addresses) of all this app’s accounts from the application’s root public key.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Funding correlation of multiple accounts is already where we’re at, so this is at least as good as that.

Indeed and I’ll try to explain why this proposal allows to be in a better state than currently in terms of privacy.

It will allow to make using a new account for each application a default. So instead of having accounts used for several applications you will have separated accounts by default. If you don’t need funding then that’s fully private.

If you need funding there is indeed a potential correlation by following the funding trail. Even in that case, it’s already better than the status quo and for several reasons:

1. Following the funding trail does not give you certainty that these accounts belong to the same person, only some probability.
2. If you use a mixer to fund the app account then it would obfuscate this trail. And with our proposal you have a proper way to create and manage a large amount of applications specific accounts.

---

**Bunjin** (2019-03-11):

ETHcc video where I introduce this work.

---

**gravityblast** (2019-03-12):

hey [@Bunjin](/u/bunjin), great proposal! We’ve been thinking about something similar to this in Status for a long time, getting the derivation path from ENS names, and I like this solution!  we would love to contribute to this and implement it when it’s finalized.

I also think this can work on top of [eip-1581](https://eips.ethereum.org/EIPS/eip-1581), what do you think?

I saw this in the proposal this:

> EIP 1581: Non-wallet usage of keys derived from BIP-32 trees also discussed here proposes a scheme that relies on a list of indexes where application should register (similar to SLIP0044 list for instance).

But EIP-1581  only defines a standard way to derive non-wallet keys, without requiring apps to be registered. Only the key_type should be, so in this case the key type can be `apps` / `dapps`, and the the sub paths what you already proposed, which I like especially in the way we can get the derivation path from a ENS name.

So if we have both we can have general non-wallet keys not based on app/domains, and apps keys based on specific apps/dapps.

What do you think?


*(18 more replies not shown)*
