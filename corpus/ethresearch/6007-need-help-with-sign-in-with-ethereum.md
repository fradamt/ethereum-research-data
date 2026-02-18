---
source: ethresearch
topic_id: 6007
title: Need help with "Sign in with Ethereum"
author: bvl
date: "2019-08-20"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/need-help-with-sign-in-with-ethereum/6007
views: 3406
likes: 6
posts_count: 17
---

# Need help with "Sign in with Ethereum"

Hi community,

was fascinated by the the “Sign in with Ethereum” [@vbuterin](/u/vbuterin) listed as an idea what should be built on top of Ethereum in this Twitter thread: https://twitter.com/VitalikButerin/status/1123136930177118209. I would like to start working on that. Is there any additional material or research how that should look like? Noticed that dAuth tries to do something similar but it doesn’t seem like it’s entirely what was intended based on the comments.

## Replies

**NicoDeva** (2019-08-21):

Usual authentication with Ethereum is done by signing with the private key, which in turn requires direct access to the private key. This is quite secure but inconvenient, since you need to have a web3 wallet holding your private key in every app in which you’d want to identify using Ethereum identity.

The [DAuth proposal](https://github.com/ethereum/eips/issues/1115) wanted to improve that by having a server do the authentication for you. A user could choose to set up its own server (otherwise, it would be a centralized authentication) and register that address in a smart contract (so that client app knows who to contact for id. But the auth server has to keep an unencrypted version of the private key. Client app sends a random encrypted string to the auth server, that decrypts it and sends it back, upon which client is happy and convinced. So unless you run your own server, you entrust your private key to a third party. Additionally that means that you can’t use this identity for payments (you wouldn’t trust your funds to be on that address).

Instead of a server signing a message, we’d want the client to sign a message. But the client doesn’t want to keep his private key (too long). So what if the secret is actually derived from the password, for example a hash salted with the public key: Hash256(password | pubkey). Now instead of proving ownership of a complex private key, Alice can identify herself by proving ownership of a key simple enough to remember.  However then it becomes easy to brute force. Authentication servers don’t allow trying for millions of solutions per second, here all the information to brute force is available on-chain. If it’s easy enough to remember, it’s easy enough to brute force.

Hope it helps you to start brainstorming.

---

**bvl** (2019-08-21):

Thanks [@NicoDeva](/u/nicodeva) for your input, some pubkey scheme is probably the most elegant for this.

Are there any examples of current dApps that would benefit and only need an Ethereum SSO, that don’t need the payment functionality that a private key + wallet enables? Trying to figure out whether this would actually be useful.

---

**bvl** (2019-08-21):

Here’s the initial idea how this login could be achieved in a way where nothing is leaked on-chain while the Ethereum Single Sign-On service (ethSSO) can still verify credentials without storing any private key info to a central repository.

The biggest leap is letting ethSSO store and read data from IPFS with their pub / priv key. However, I don’t see this as a problem since people would anyways be willing to write their ENS/ETH addr + password combination to ethSSO if they ever used the service. It would be still better than directly writing that info to the original website’s web form.

Here’s the flow in quick steps:

Register:

1. User opens ethSSO and web3 wallet login is required. They input their password to the register form.
2. The password is encrypted with the public key of ethSSO and an IPFS key is returned.
3. The msg.sender - IPFS key pair is stored to the contract with a web3 wallet confirmation.

Login:

1. User puts their ENS addr and password to the login form.
2. After ENS addr → ETH addr transformation the IPFS key is fetched from the contract with the ETH addr.
3. ethSSO decrypts the contents behind IPFS key with their private key and a password is returned.
4. ethSSO compares the passwords and returns either OK or FAIL to the original website.

Here’s a diagram describing that a bit more visually:

[![47](https://ethresear.ch/uploads/default/optimized/2X/6/62ea44707f25c637ec5801b05d6588b801373eab_2_690x458.png)471598×1062 34.5 KB](https://ethresear.ch/uploads/default/62ea44707f25c637ec5801b05d6588b801373eab)

---

**NicoDeva** (2019-08-22):

- Passwords are never transmitted in clear but hashed
- Smart contract accessing a private key means everybody can read the private key
- Some entity keeping the private keep means a central entity, so it’s not decentralized (unless it’s yourself, ofc)

---

**virgil** (2019-08-22):

I suggest starting from EAuth, available [here](https://github.com/pelith/discourse-eauth) with a [live example](https://discourse.pelith.com/).

There are a few changes I’d want to make before deploying something like EAuth on ethresear.ch to protect against name collisions with the current github usernames:

So if you have ownership of address `0xf00`, it should do a reverse-lookup to see if there’s any ENS name associated with it. If so, it uses the ENS name and appends the “.eth” (because github usernames aren’t allowed contain a dot). If there is no ENS name associated, then it gives the username of `0xf00` as a string (this works because github usernames are at most 39 characters, whereas `0xf00` will always be exactly 42 characters). In summary, the user isn’t able to specify their own username except through ENS.

The reasoning for this change is that if can currently create namespace collisions between the Github names and the self-inputted names from EAuth.

---

**bvl** (2019-08-22):

1. The password here is encrypted off-chain with the public key of ethSSO. After that it’s stored in encrypted form behind the IPFS url / key
2. Smart contract is not accessing the private key here, only the IPFS url / key that contains the password in encrypted form
3. If you want to login to a service without a wallet and are willing to login with a password, you are already putting your trust in that ethSSO service performing the login and not sharing your password. The plus side is that there’s no central repo of failure as the password are stored in ipfs in encrypted form.

---

**vbuterin** (2019-08-22):

I’m inclined to say that requiring users to have ethereum wallets in browsers they use to login is okay. Metamask and Opera exist; most users are going to access things from a laptop and a phone, and there aren’t any theoretical difficulties with having the same ethereum account on both (if it’s practically too difficult to have the same account on both, one could set up a meta-account which represents the idea that account A OR B could approve on their behalf). And if a server *is* used somehow to cover the cases where a user doesn’t have a wallet on some computer, that mechanism should be completely optional.

The main long-term issue with EAuth is that it expects ECDSA wallets, and does not support smart contract wallets. I’d suggest contracts having a (constant) function `verifySignature(msg, sig)` that verifies message/signature pairs and outputs `True` if the signature is valid and `False` if it is not. This way we get future-proof general-purpose abstraction.

As far as benefits to why web services would care about supporting sign-in-with-ethereum, I can see a few:

- Let users “control their own identity”
- Scan ETH and other tokens held inside the account (or other metrics eg. Slock’s proposal of historical txfees paid) and use those balances as an anti-sybil mechanism
- In the longer term, more security, as smart contract wallets could implement more advanced multisig-based account recovery setups that could outcompete centralized providers’ offerings.

---

**bvl** (2019-08-22):

I posted an initial password based solution for users that might not have a wallet in hand but might need a way to access a certain site with limited functionality, mainly excluding anything that requires private key signing.

Does that miss the point of ”Sign in with Ethereum” [@vbuterin](/u/vbuterin)?

If an ens address + password is not what we are looking for here due to lower security, then I don’t understand why not use wallet only in the first place. Similar to what you said, I see this as an optional convention.

It’s the same with facebook and other services: you might login with a password but do financial transactions only with your bank account / credit card.

---

**Ping** (2019-08-23):

Soon Eauth will support contract wallet login with [EIP1271](https://github.com/ethereum/EIPs/blob/e92c13b3bafafa081d0b9df04c3006626b3928cb/EIPS/eip-1271.md) interface.

Here’s an early beta demo:

https://eauth-beta.pelith.com

And a reference wallet implementation:

[https://github.com/artistic709/solidity_contracts/blob/035f8f18fc50d683df899b6c98fa269167d58d81/personalwalletfactory.sol](https://github.com/artistic709/solidity_contracts/blob/master/personalwalletfactory.sol)

Yeah, it’s exciting to have ‘self-sovereign’, ‘arbitrary curve’, ‘social recovery’ Identities thanks to blockchain.

But I think there are some drawbacks we have to consider: Supporting contract wallet makes Eauth ‘not pure’ since ecrecover is a pure function but isValidSignature() is a view function depends on Ethereum’s state.

Currently, the demo refers Rinkeby’s state, so you can’t login with a contract on Mainnet.

[![image](https://ethresear.ch/uploads/default/original/2X/1/17d6c43e07590d6263b87b6bab718ac7d8498c2e.jpeg)image286×399 93.2 KB](https://ethresear.ch/uploads/default/17d6c43e07590d6263b87b6bab718ac7d8498c2e)

---

**vbuterin** (2019-08-24):

> Supporting contract wallet makes Eauth ‘not pure’ since ecrecover is a pure function but isValidSignature() is a view function depends on Ethereum’s state.

What’s wrong with that? In the long run you’d *want* most users’ verification functions to be not pure, because that’s how you can do key revocation etc etc.

---

**austingriffith** (2019-08-27):

We are working on a one-line js implementation to let developers easily bring in web3 for signing, verifying, and bottom-up identity. We also hope to provide end-users with optionality around web3 providers similar to web3connect that even includes generating a burner key pair in localstorage.

I think the trick will be a system that can provide attestations between ephemeral (session) key pairs and colder wallets. Still just getting started, but the initial article and screencast is here:

https://medium.com/@austin_48503/kirby-32491315c5

The bottom line is making something that is incredibly easy for developers to implement in their applications, a straightforward interface for users, and the ability for signers to control their own attestations.

---

**bvl** (2019-08-28):

I believe we have now 4 different thoughts and implementations on this. [@vbuterin](/u/vbuterin) is there an existing spec / EIP that’s simple enough to be implemented and possibly adopted by the broader community?

So far it’s a bit unclear what’s the best course of action with this. Just like Uniswap was based on the simple x * y = k formula, is there a similar one for this?

---

**vbuterin** (2019-08-29):

I feel like the identity layer is the wrong place to resolve the “connect cold wallet to hot key” problem. The right layer to resolve that problem is smart contract wallets. If you have an `isValidSignature(msg, sig)` view-function, then it can verify against a different key than the key that has the ability to do whatever it wants to the account. This way smart contract wallets can also allow hot keys to do other low-risk things, like withdrawing small amounts of ETH to pay fees.

---

**vbuterin** (2019-08-29):

If I were designing the thing myself, I would do it as follows. For existing EOAs, just use message verification similar to EAuth (Virgil’s link: https://discourse.pelith.com/) to sign in with the account. For contract accounts, check that the account the user is trying to sign in with has a (public, view) `verifySignature(bytes32 msg, bytes signature) -> bool` method, and use that method to verify a signature to sign in with that account. Everything else can be done wallet-side, including setting up ephemeral keys etc etc.

The goal is that the standard itself should be maximally simple so that it can be maximally future-proof, and it’s the job of wallet developers to deal with user-side security/convenience tradeoffs.

---

**jvluso** (2019-08-29):

It should probably use `isValidSignature` as per EIP1271. That’s what I’m planning to do for [ethereum-oauth](https://github.com/Recoblix/ethereum-oauth).

---

**vbuterin** (2019-08-31):

Sounds good. I do like `data` being bytes instead of bytes32, it allows for higher-level standards forcing the data to be structured in some way that allows the smart contract wallet to require different levels of security for different actions (eg. a whitelist of websites for which you can sign with a lower-security hotkey, or alternativey a list that requires *higher* security).

