---
source: magicians
topic_id: 11604
title: "EIP-6051: Private Key Encapsulation"
author: Weiji
date: "2022-11-04"
category: EIPs
tags: [wallet, private-key]
url: https://ethereum-magicians.org/t/eip-6051-private-key-encapsulation/11604
views: 4513
likes: 6
posts_count: 26
---

# EIP-6051: Private Key Encapsulation

edit: EIP address: [EIP-6051: Private Key Encapsulation](https://eips.ethereum.org/EIPS/eip-6051)

pull request closed: [Add EIP-6051: Private Key Encapsulation by weiji-cryptonatty · Pull Request #6051 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6051)

## Replies

**firnprotocol** (2022-11-11):

hi [@Weiji](/u/weiji), huge thanks for putting this together, and apologies for not responding sooner.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/weiji/48/7328_2.png) Weiji:

> so that it could be securely relocated to another dApp without providing the seed.

the main thing I want to clarify is: are you envisioning here that the “dapp” would be running a separate backend server on a remote machine? from what you’ve written above, it appears that way, but please correct me otherwise.

i think this question—i.e., is the “dapp” on a different machine, or not—led to a degree of confusion in the other thread. so let’s try to get that out of the way now.

if you *do* imagine the dapp to be on a separate machine, then could you go through a few examples where you’re imagining this’d happen? in my view, the far-more-common case is where the “dapp” is static javascript running solely in the user’s browser.

---

**alenhorvat** (2022-11-11):

Hi.

Exporting/moving private keys (even in an encrypted form) is not a good security practice as it opens an attack surface.

This doesn’t mean there’s no solution for it ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

What if, instead of designing a key transfer/encapsulation/… protocol, decentralised identifiers (DIDs) are introduced on the protocol level (not on the SC level)? (DID method on the SC level [GitHub - uport-project/ethr-did: Create ethr DIDs](https://github.com/uport-project/ethr-did))

DID is a unique random string that resolves to a DID Document. DID Document is a collection of public keys controlled by the DID owner. You can add, update, and remove your keys, and the protocol ensures that you can add keys if and only if you control the DID (prove you own one of the DID controlling keys).

This would mean that the core identifier in the protocol is no longer an ETH address but a DID. It is a substantial change, of course. Is anyone aware of whether the topic was already discussed elsewhere?

BR, Alen

---

**Weiji** (2022-11-11):

Hi [@firnprotocol](/u/firnprotocol) , actually I have some possible use cases in mind and mostly the dApp is *not* remote, but also probably not a browser extension. Let me iterate:

1, for messaging use. Certainly users may generate a completely new key pair not related to existing seed. However then users will have to manage this new key pair as well as to publish the public key somehow. Without going into each individual situation, let’s say there might be the case that users wish to generate a new key pair, and there might be the case that users wish to use existing key pair especially when its backup has already been taken care of. In such case, the “dApp” could be a standalone desktop application or mobile app.

2, hardware wallet → MPC case.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/weiji/48/7328_2.png) Weiji:

> We might want to export one of many private keys from a hardware wallet, and split it with MPC technology so that a 3rd party service could help us identify potential frauds or known bad addresses, enforce 2FA, etc., meanwhile we can initiate transactions from a mobile device with much better UX and without carrying a hardware wallet.

There might not be a strong demand, but I believe it is a valid use. Users still have complete control over the private key, but a 3rd party service can still provide lots of value-added service.

---

**Weiji** (2022-11-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alenhorvat/48/7718_2.png) alenhorvat:

> DID is a unique random string that resolves to a DID Document. DID Document is a collection of public keys controlled by the DID owner. You can add, update, and remove your keys, and the protocol ensures that you can add keys if and only if you control the DID (prove you own one of the DID controlling keys).

With regard to messaging & encryption, I think what you describe here might help with key discovery of [EIP-5630](https://ethereum-magicians.org/t/eip-5630-encryption-and-decryption/10761), related but out of scope there.

---

**alenhorvat** (2022-11-11):

Ok. I’ll check that thread and see if I can help.

---

**Weiji** (2022-11-18):

Thinking this through, it seems signature to the recipient public key is crucial for security, to ensure the ephemeral public key is indeed generated from a trusted party and has not been tampered with.

The key sender then can verify the signature before proceeding to encapsulating the private key.

---

**Weiji** (2022-11-18):

edit: see PR in the top (edited):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/weiji/48/7328_2.png) Weiji:

> pull request here: Added EIP-6051 for private key encapsulation by weiji-cryptonatty · Pull Request #6051 · ethereum/EIPs · GitHub

---

**Weiji** (2022-11-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/weiji/48/7328_2.png) Weiji:

> ```auto
> request({
>     method: 'eth_generateEphemeralKeyPair',
>     params: [version, signerPubKey],
> })
> ```

Specifically, an external service (such as a MPC service) could publish its signer public key(s) for sender to verify. Then the signature could be calculated separately, and then appended to the generated public key.

---

**Weiji** (2022-11-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/weiji/48/7328_2.png) Weiji:

> If signerPubKey is provided or recipient contains signature, the implementation MUST perform signature verification. Missing data or incorrect format etc. SHALL result in empty return and optional error logs.

If the signature to the recipient public key is not provided, sender implementation MAY choose to decline the request. Sender implementation MAY choose to trust only limited signer. In that case, the signer public key could be further signed by the trusted signer, and that signature is appended to signerPubKey. This is open for now and further specification is pending.

---

**Weiji** (2022-11-28):

Hi folks, I have created PR and updated the top post. Please continue to review and any feedback are welcome!

---

**Weiji** (2022-11-29):

Here is the sample code to generate the test vectors, provided here as EIPs repository does not allowed external links: [GitHub - Base-Labs/encapsulation-sample: sample application to demonstrate how to encapsulate private key according to eip-kem](https://github.com/Base-Labs/encapsulation-sample)

---

**Weiji** (2022-11-30):

Quoting my own review comment from the pull request:

> We might want to export one of many private keys from a hardware wallet, and split it with MPC technology so that a 3rd party service could help us identify potential frauds or known bad addresses, enforce 2FA, etc., meanwhile we can initiate transactions from a mobile device with much better UX and without carrying a hardware wallet.

Reviewing the motivation, however, it seems in this exact case we may have alternative request to R2 and R3, that is, each party P_i in a MPC setting may generate its own ephemeral key pair (r_i, R_i), and then Sender application may safely split `sk` into several pieces sk_i, then encapsulate each sk_i to R_i. This effectively replaces the usual Distributed Key Generation procedure in a typical MPC protocol.

To be fair, this may be added as an amendment to EIP-6051 or a separate EIP. We also need to survey MPC protocols to see if the above suggestions work in their security models.

---

**shadow** (2022-12-05):

This is amusing. I was thinking about ‘encapsulation’ security just earlier today.

The issue that I see / thought about–with this:

It doesn’t make sense this late in the game. Methods to enumerate private keys are essentially exposed–that is with the course of time and lots of GPU power. So a hypothetical encapsulation securing a private key essentially becomes use*less* but not unusable. Yes, a cryptographic shell or valence layer per se could work,

If you are going to create security for something like an Ethereum Private Key, then the security around that private key must be unlocked and built encapsulating the original stored data and part of the complete mechanism needed to unlock the key.

You can already bruteforce a private key (if you are lucky) so who cares about the “security” around it.

You just can’t effectively encapsulate something with the original door is outside of the capsule.

Its like locking a  ‘gym locker lock’ without putting the the lock loop the whole.

if that makes sense

---

**Weiji** (2022-12-05):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/5fc32e/48.png) shadow:

> Methods to enumerate private keys are essentially exposed–that is with the course of time and lots of GPU power.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/5fc32e/48.png) shadow:

> You can already bruteforce a private key (if you are lucky)

My friend, this seems a serious misunderstanding of cryptography, or at least of elliptic curve cryptography. You can *theoretically* enumerate every private key or crack one given its public key in a certain public key system, but *in practice (or computationally)* it needs at least billions of years even if you were given all the (classic) computers in the world.

---

**shadow** (2022-12-05):

As I said  in the post that you quoted me on…

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/5fc32e/48.png) shadow:

> with the course of time and lots of GPU power.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/5fc32e/48.png) shadow:

> (if you are lucky)

---

**Weiji** (2022-12-05):

[@shadow](/u/shadow) There is no luck in cryptography. Reading this page might give you some sense of “being lucky” (or unlucky): [Security level - Wikipedia](https://en.wikipedia.org/wiki/Security_level)

---

**shadow** (2022-12-05):

How is there no luck in cryptography. I think any random guess that provides a result that satisfies your original intention out of unfathomable chances is luck.

A successful brute force is 100% luck.

No this page did not provide me with a sense of “being lucky” towards anything.

If anything at all,  mechanism that encapsulates data that is supposed to be secret is just a short cut for an attacker to located *that key" or *any key*

a mechanism using functions, algos, hashes or whatever it is encapsulating that *private data* is nothing more than a short cut to key identification. Instead of searching through every possible key, just find a way to get through and then you have what you are looking for with certainty.

---

**Weiji** (2022-12-05):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/5fc32e/48.png) shadow:

> A successful brute force is 100% luck.

One may try that, but the chance of success is extremely low. Say, Alice has a key pair `(a, A)` under `secp256k1` curve, and Bob wants to guess or brute force the private key `a`. For each guess, Bob’s success rate is 1 in 2^256 (I should have used the group order of `secp256k1` but let’s keep this post simple). A not very accurate but close enough analog is, for Alice to randomly pick any ***atom*** in the ***known universe***, then Bob tries to guess which one is her pick. No matter how hard Bob tries for how long, his chance of hitting the right atom is still extremely low. Hope this analog impresses you.

An attacker will not simply guess, instead he will narrow down the guess range with various tricks but at the end, there is still a security level measuring how much guesswork must be done. Note that `secp256k1`’s security level is 128, and 2^128 is indeed a very very large number.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/5fc32e/48.png) shadow:

> a mechanism using functions, algos, hashes or whatever it is encapsulating that private data is nothing more than a short cut to key identification. Instead of searching through every possible key, just find a way to get through and then you have what you are looking for with certainty.

That’s the whole point of symmetric cipher (AES-128 etc.) here. The target security level of AES-128 is 128 (bits). The actual security level might be slightly smaller, but is still considered secure.

---

**shadow** (2022-12-06):

I hate that ‘atom’ analogy. There are far more atoms in existence than bitcoin possibilities.

---

**Weiji** (2022-12-06):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/5fc32e/48.png) shadow:

> There are far more atoms in existence than bitcoin possibilities.

I guessed that you had underestimated greatly about the count of possible secp256k1 key pairs. What I said earlier is not rocket science (yet) but maybe a bit out of common sense for those not familiar with cryptography. So let me explain in greater details.

Scientists estimate that there are about 10^78 ~ 10^82 atoms in the known universe. You may find this number in a lot of creditable places online. The choice is yours.

For the secp256k1 curve that bitcoin and Ethereum uses, the group order is:

`n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141`

There are totally `n-1` possible key pairs. It is safe to say we have about `2^256` when compared to another estimated number. `2^256 ~= 10^77`. So you see, it is a very close analog.

Again, there is no luck in cryptography. All security parameters have been fine tuned to a point far beyond luck (as winning a lottery), when even the tiny possibility of such is not acceptable.


*(5 more replies not shown)*
