---
source: magicians
topic_id: 1243
title: "The UX of EIP 1024: Encrypt/Decrypt"
author: danfinlay
date: "2018-09-04"
category: Web > Wallets
tags: [wallet, ux]
url: https://ethereum-magicians.org/t/the-ux-of-eip-1024-encrypt-decrypt/1243
views: 2739
likes: 4
posts_count: 6
---

# The UX of EIP 1024: Encrypt/Decrypt

EIP 1024 is starting to settle down and finalize, and so we just about have a solid technical foundation on which to build encryption and decryption into web3 browsers.

You can read the technical aspects of the proposal here:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/topealabi/48/212_2.png)
    [EIP-1024: Cross-client Encrypt/Decrypt](https://ethereum-magicians.org/t/eip-1024-cross-client-encrypt-decrypt/505) [EIPs](/c/eips/5)



> eip: 1024
> title: Add web3.eth.encrypt and web3.eth.decrypt functions
> author: Tope Alabi
> status: Draft
> type: Interface Track
> created: 2018-05-14
>
>
>
>
> Abstract
> This EIP proposes a cross-client method for requesting encryption/decryption. This method will include a version parameter, so that different encryption methods can be added under the same name. Nacl is a cryptographically complete and well audited library that works well for this by implementers are free to choos…

In this thread I’d like to open the discussion to issues related to the user experience of encryption and decryption in web3 browsers.

A few questions I have, with my current opinions stated after them:

1. Should users be prompted before their encryption public key is exposed to the dapp via web3.eth.getEncryptionPublicKey?

I think especially with improved “explicit sign in” that this could be unnecessary, and associated keys could be revealed with a single “sign in” request.
2. Should we prompt users to encrypt?

This probably isn’t necessary, since encryption doesn’t require their private key material at all, could be performed without a web3 browser.
3. Eventually if/when we add a “sign and encrypt” method, we can prompt the user in one place there.
4. Should we prompt users to decrypt and download a file?

I don’t think this is necessary, since it does not expose the decrypted data to anyone but the user’s own hard disk.
5. Should we return decrypted data to the requesting Ðapp?

This is the behavior that I think would require a prompt and user authorization.
6. For the sake of keeping decryption-heavy dapps practical and usable, we probably want to introduce a batch requestPersistentUsageOfDecryptionKeyForAccount( account ) method.

The Dapp should provide a user a way of revoking this decryption method if it can be extended.

Thoughts?

[@topealabi](/u/topealabi) [@cjeria](/u/cjeria) [@chrislundkvist](/u/chrislundkvist)

## Replies

**danfinlay** (2018-09-05):

[@andytudhope](/u/andytudhope) [@beltran](/u/beltran) [@alexvandesande](/u/alexvandesande)

---

**perpetualescap3** (2018-09-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> Should we prompt users to decrypt and download a file?

I wonder if client implementations would always be able to guarantee the downloaded file wouldn’t / couldn’t be intercepted?

---

**godfreyhobbs** (2018-09-26):

Dan these are a great set of questions.  Here is a demo we have created.

https://drive.google.com/file/d/14iY8ea_I6GC6oEyUXfTuF8xGUc6OSSFK/view

---

**wighawag** (2018-10-15):

Hi [@danfinlay](/u/danfinlay)

I am just jumping in with my 3 proposals in context (explained [here](https://medium.com/@wighawag/3-proposals-for-making-web3-a-better-experience-974f97765700))

On that note I posted a new topic on UX ring to bring discussion on these proposals, see  [here](https://ethereum-magicians.org/t/3-proposals-for-making-web3-a-better-experience/1586)

One thing I did not mention and that you touch upon here is “encryption and the use of public key”.

So as to answer your point :

**1. Should users be prompted before their encryption public key?**

We could either

1. consider the public key as “already public” in the context of the wallet, or
2. we provide an api for encryption that do not reveal the public key.

In regard to 1), this is not too far fetched for most web3 browser as it is expected of the user to sign messages or transactions at some point. If not, are we going to explain to them that their public key will be public after their first transactions?

I think unless, the user is knowledgeable of what is happening, it would scare most user and most would simply accept such warning.

At the same time, 2) allow us to simply bypass the need for revealing the public key.

**2. Should we prompt users to encrypt?**

As you mentioned, this would be unnecessary if they have access to the public key

**4. Should we return decrypted data to the requesting Ðapp?**

As you understood from the [article](https://medium.com/@wighawag/3-proposals-for-making-web3-a-better-experience-974f97765700) if the application encode the origin(s) allowed to decrypt the web3 browser could check the origin of the document attempting to decrypt and make sure they match before revealing the decrypted data.

This would also allow to safeguard from other application asking to decrypt data without the web3 browser having context to explain to the user where that data came from.

---

**Recmo** (2019-01-29):

Hi! I have a need to implement new signature algorithms and made a proposal for extensible cryptography in wallets. It can also be used to implement encryption.

Please see the proposal here: [Extensible crypto for wallets](https://ethereum-magicians.org/t/extensible-crypto-for-wallets/2546)

It’s stil draft. In particular it is not specified how the user confirmation would work. My original use case is for signing, but I’d like it to be general enough to solve all future needs for cryptography, including what EIP2¹⁰: Encrypt/Decrypt covers. My hope is to make it so good that it can be merged with EIP1024 into one proposal that covers all our wallet crypto needs.

