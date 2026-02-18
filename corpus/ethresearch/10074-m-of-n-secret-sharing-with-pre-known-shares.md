---
source: ethresearch
topic_id: 10074
title: M-of-N secret sharing with pre-known shares
author: vbuterin
date: "2021-07-12"
category: Cryptography
tags: []
url: https://ethresear.ch/t/m-of-n-secret-sharing-with-pre-known-shares/10074
views: 5486
likes: 13
posts_count: 11
---

# M-of-N secret sharing with pre-known shares

Suppose that you want to generate a secret s, where s can be recovered by bringing together M of N secret-shares, where *all N secret shares are pre-known*. Two use cases of this are:

- A brainwallet where the N shares are answers to N security questions, and you want the funds to be recoverable with only answers to M security questions (security questions suck individually, but if you combine eg. 20 of them you can get quite a lot of entropy)
- A social recovery design where you want to use threshold decryption instead of smart contract wallets because you are trying to recover access to private data and not cryptocurrency, and you want your recovery partners to be able to use keys that they already have (to reduce risk that they will lose those keys)

Plain old M-of-N secret sharing does not work for either of these use cases, because it only allows M shares to be pre-chosen; the remaining N-M shares must be generated from the original M using a deterministic algorithm, and look like random data (in the brainwallet case, making them unsuitable as answers to security questions, and in the social recovery case, requiring users to use special software to store them, instead of making them derived from an existing HD wallet).

So here is what we do instead. We make a *N-of-(2N-M)* threshold scheme, generating the N-M excess shares from the original N. We then *publish all N-M excess shares on the blockchain*. If desired, in the social recovery case one could instead simply give every participant a copy of all excess shares. This has the effect that the excess shares become effectively public information: there is negligible risk that they will get lost, but also any attacker will have them. As a result, only M of the non-published N shares are needed to combine with the N-M excess shares and uncover the data - hence, we have an M-of-N scheme, which is exactly what we want.

### Edit 2021.07.18: alternative mechanism for the social recovery use case

In the social recovery use case, we want to make the setup procedure as simple as possible, because users are lazy and if setup is difficult they will inevitably choose insecurely small recovery partner sets. This means distributed key generation (DKG) needed to generate secret shares in a decentralized way is likely a bad idea, because it requires 2 rounds of communication (which implies either extra blockchain transactions or everyone being online at the same time *and* having a synchronous communication channel).

Instead, we can take advantage of the fact that the account holder themselves has their private key. They can simply ask each recovery partner for their public key (eg. via `pk = G * hash(ecdsa_sign(msk, nonce))` where `msk` is the recovery partner’s main secret key), and then publish a single transaction on-chain containing `nonce` and `encrypt(share_i, pk_i)` for each `i` (where `share_i` is the i’th share of the key and `pk_i` is the public key of the i’th participant).

If we are careful about not reusing nonces and thus not reusing keys (eg. setting `nonce = hash(secret, maddr_1 ... maddr_n)` ,where `secret` is the value being put into recovery and `maddr_i` is the address of the i’th recovery partner, should be sufficient), a very simple bare-bones Diffie-Hellman encryption can be used. This means that only a single transaction, with `32 * (n+1)` bytes of calldata, is sufficient to save the recovery info.

## Replies

**kelvin** (2021-07-12):

This is very interesting! I guess in a social recovery design, the N participants would append some public salt to their private keys and then hash it to generate the N pre-known shares?

Otherwise they will be unwilling to give their shares away to let the N - M excess shares be computed, and also they would have to reveal M keys to recover the secret.

Also, what types of private data do you think people would like to distribute this way?

---

**SebastianElvis** (2021-07-14):

This looks like a threshold version of identity-based encryption (IBE).

In IBE, given an arbitrary public key pk (e.g., an email), a key distribution centre can generate a secret key sk such that f(sk) = pk and V(sk, pk) = 1.

Here, given n arbitrary inputs s_1, \dots, s_n and parameter m, one can output a secret s such that f(S) = s and V(S, s) = 1, where S is a set of any m inputs.

Perhaps combining techniques in threshold crypto and IBE can do?

---

**vbuterin** (2021-07-18):

> append some public salt to their private keys and then hash it to generate the N pre-known shares

Realistically, they would use `hash(ecdsa_sign(key, salt))` as a hash function to generate subkeys, because the `ecdsa_sign` method is exposed in the web3 API and has a standardized deterministic output (whereas “output the key” is *not* exposed in the web3 API). But that’s an implementation detail; the effect is the same.

> Also, what types of private data do you think people would like to distribute this way?

I was just thinking encryption keys for “Ethereum email” and decentralized messaging apps like Status to start off. Another natural use case is of course private keys for other blockchains.

---

**kelvin** (2021-07-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> In the social recovery use case, we want to make the setup procedure as simple as possible, because users are lazy and if setup is difficult they will inevitably choose insecurely small recovery partner sets. This means distributed key generation (DKG) needed to generate secret shares in a decentralized way is likely a bad idea, because it requires 2 rounds of communication (which implies either extra blockchain transactions or everyone being online at the same time and having a synchronous communication channel).
>
>
> Instead, we can take advantage of the fact that the account holder themselves has their private key. They can simply ask each recovery partner for their public key (eg. via pk = G * hash(ecdsa_sign(msk, nonce)) where msk is the recovery partner’s main secret key), and then publish a single transaction on-chain containing nonce and encrypt(share_i, pk_i) for each i (where share_i is the i’th share of the key and pk_i is the public key of the i’th participant).

I think that is a *significant* improvement, as having everyone in a synchronous communication channel seems nearly impossible. However, I’m afraid some users will not even be willing to wait for all N people to reply with a public key. They may also dislike having to ask each of these people to sign a special message.

We know users are lazy, so can we go further and have a procedure in which a user could just list N addresses of his friends and get it done already?

Here is my proposal. It requires that all N addresses have sent transactions already, so that we can recover each public key `pk_i` from them using some external service, of course validating that they indeed correspond to the addresses. Then we can simply publish `encrypt(share_i, pk_i)` for each i.

Do you think that works?

---

**vbuterin** (2021-07-24):

> Do you think that works?

The problem with that is that it requires the recovery partner’s primary tx sending key to be the decryption key. Metamask, Status and most other wallets don’t expose the sending key for any function except signing transactions and messages.

---

**kelvin** (2021-07-25):

> The problem with that is that it requires the recovery partner’s primary tx sending key to be the decryption key. Metamask, Status and most other wallets don’t expose the sending key for any function except signing transactions and messages.

MetaMask has recently added support to decryption [here](https://docs.metamask.io/guide/rpc-api.html#other-rpc-methods), but it requires users to generate a special “encryption public key”, so it is more similar to your idea.

Digging a little more it seems that the *secp256k1* is not very well-suited to assymetric encryption. If this is so then my idea really doesn’t work.

Not only that, but maybe we *should have* to ask users before sending them a secret share? Otherwise I’m pretty sure many people would randomly decide to add **you** as a recovery partner. It would be like the dog tokens, but this time you would get people begging you to help them recover their wallets!

---

**vbuterin** (2021-07-25):

> Not only that, but maybe we should have to ask users before sending them a secret share?

Yeah I think that’s reasonable. Of course, there may well be ways to send people secret shares regardless once they publish some kind of L2 public key for any purpose, but it shouldn’t be default/easy to do such a thing.

---

**peg** (2021-08-09):

I am wondering if there are ways one could minimise what metadata is exposed in the messages published on chain, whilst still making life easy for the recovery partners.

Given such a message, anybody can see: that it is a social recovery message, who published it, the number of shares (unless we obfuscate that by padding them with extra ones - but that would be expensive), and when it was published.

Could there be some way to obfuscate the ‘what’ by making these messages difficult to distinguish from other types of on-chain message?

Or maybe would it make sense to obfuscate the ‘who’ by publishing it from a one-time account. But then we need a way for the recovery partners to find it, without requiring them to know some additional information - as that is what we are trying to avoid.  They might need to attempt to decrypt a whole load of messages to search for their encrypted share.  There is a trade-off between the computational effort that adds, and the additional security this would offer.

---

**debuggor** (2022-09-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Instead, we can take advantage of the fact that the account holder themselves has their private key. They can simply ask each recovery partner for their public key (eg. via pk = G * hash(ecdsa_sign(msk, nonce)) where msk is the recovery partner’s main secret key), and then publish a single transaction on-chain containing nonce and encrypt(share_i, pk_i) for each i (where share_i is the i’th share of the key and pk_i is the public key of the i’th participant).

It can also be handled in this way,  ECDH,

**alicePubKey * bobPrivKey = bobPubKey * alicePrivKey = secret**,

key_i = hash(secret_i),  encrypt(share_i,  key_i)

During initialization, no action is required from the partner.

---

**jhsotoca** (2024-02-06):

Just for completeness, this cryptographic technique appeared in 2007-2010, in a series of works by Daza et al., see for instance  documents 2008/502  and  2007/127 on the IACR ePrint repository

