---
source: ethresearch
topic_id: 5032
title: Shamir secret sharing implementation in a non-custodial mobile Ethereum wallet
author: arnavvohra
date: "2019-02-21"
category: UI/UX
tags: []
url: https://ethresear.ch/t/shamir-secret-sharing-implementation-in-a-non-custodial-mobile-ethereum-wallet/5032
views: 4580
likes: 8
posts_count: 7
---

# Shamir secret sharing implementation in a non-custodial mobile Ethereum wallet

Me and the whole Coinsafe team have been working on a Shamir secret sharing implementation in a non-custodial mobile wallet. Our implementation allows you to recover your 12 word mnemonic phrase using your trusted devices essentially making it safe for everyone to hold private keys of their cryptocurrencies instead of trusting custodial services. I’m excited to announce that we are live in testnet beta for both Android and iOS.

Over the past couple of months we tried to tackle all the attack vectors in integrating secret sharing in a mobile wallet and make it simple to use for a non-technical user.

Some key achievements of our technical architecture :

1. Applying secret sharing at the mnemonic level instead of private key level in order to support multiple cryptocurrencies. This is not possible with a smart contract based recovery approach as in such approaches a user’s funds are held in a smart contract which means there can only be support for ETH & ERC20 tokens.
2. Successfully handling the case of ‘trusted devices collusion’ which ensures that your funds remain secure even if all your trusted devices collude. We handled this problem by ensuring that :
a. You first encrypt your mnemonic using a symmetric key to get an encrypted text. This symmetric key is mapped with your email address hash and is safely stored in Coinsafe’s database.
b. You apply secret sharing on this encrypted text to generate shares that are to be shared with your trusted devices/friends.
M (original mnemonic) +X (symmetric key) → M’ (encrypted text)
M’ (Encrypted text) -> Secret sharing -> S1, S2, S3, S4, S5 (Secrets)
This means that even if your trusted devices/friends collude, they would only get an encrypted text and in order to gain access to your original mnemonic, they would need to hack your email as well to gain access to the decrypting symmetric key. The probability of both of them happening together is substantially low. Full details in our first blog post.
3. Making sure only you know your trusted devices - this is essential as we don’t want Coinsafe or any other third party to have the ability to send recovery request to your trusted devices on your behalf.
This is accomplished because our architecture only needs to know the hash of your trusted device wallet public keys. Full details in our second blog post.
4. Using a wallet public, private key pair for secure communication between you and your trusted devices while ‘setting up key recovery’ and ‘recovering forgotten key’. This public, private key pair is derived from the user’s mnemonic phrase but is not tied to any cryptocurrency. It’s just used to do encrypted communication between the user and their trusted devices.

Feedback we are looking for :

- UI/UX improvement in our implementation of secret sharing in the app with the goal of allowing even our Moms to secure her funds by selecting friends/devices she trusts.
- Possible security issues with our architecture, if any.
- Collaborations/partnerships we can do to reach to a wider user base. This can be collaborations with other software/hardware wallet companies, institutions or high networth individuals who are looking to safeguard the private keys of their crypto etc.

**Relevant Links :**

[Coinsafe Twitter](https://twitter.com/coinsafeapp)

[Coinsafe Website](https://getcoinsafe.app/)

App Beta versions :

[Android](https://play.google.com/store/apps/details?id=app.getcoinsafe.android)

[iOS](https://testflight.apple.com/join/WNoEZnby)

## Replies

**arne9131** (2019-02-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/arnavvohra/48/1429_2.png) arnavvohra:

> Successfully handling the case of ‘trusted devices collusion’ which ensures that your funds remain secure even if all your trusted devices collude. We handled this problem by ensuring that :
> a. You first encrypt your mnemonic using a symmetric key to get an encrypted text . This symmetric key is mapped with your email address hash and is safely stored in Coinsafe’s database.
> b. You apply secret sharing on this encrypted text to generate shares that are to be shared with your trusted devices/friends.
> M (original mnemonic) +X (symmetric key) → M’ (encrypted text)
> M’ (Encrypted text) -> Secret sharing -> S1, S2, S3, S4, S5 (Secrets)
> This means that even if your trusted devices/friends collude, they would only get an encrypted text and in order to gain access to your original mnemonic, they would need to hack your email as well to gain access to the decrypting symmetric key. The probability of both of them happening together is substantially low.

In case the trusted devices collude. The encrypted text is as strong as the “password” used to encrypt it. Hacker can easily brute force the “password” space and decrypt it.

What you can do is, generate a random number x and hash the password x times. This random number can be securely stored on Coinsafe servers. This increases the “password” space for the attacker to brute force.

How does the recovering forgotten key mechanism work?

---

**arnavvohra** (2019-02-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/arne9131/48/3176_2.png) arne9131:

> In case the trusted devices collude. The encrypted text is as strong as the “password” used to encrypt it. Hacker can easily brute force the “password” space and decrypt it.
>
>
> What you can do is, generate a random number x and hash the password x times. This random number can be securely stored on Coinsafe servers. This increases the “password” space for the attacker to brute force.

Good question. The ‘password’ or the symmetric key is as difficult to brute force (if not more) than a private key.

A signature is calculated first using your wallet private key and sent to Coinsafe’s database. This signature is the symmetric key (X).

Pseudo-code for the above step looks like :

var salt = SHA 256 hash (private key);

const X = calculateSymmetricKey (salt, walletPrivateKey);

X obtained above looks like : MFEwDQYJYIZIAWUDBAIDBQAEQMTWsMfOhZWvjcPdwoucjvKqYbiTitQzb7qJk72s4//lt6/O+n/3J4+CaNcJUfDpHoY3q5AhLVUahPkb4RB3lgY=

---

**arnavvohra** (2019-02-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/arne9131/48/3176_2.png) arne9131:

> How does the recovering forgotten key mechanism work?

The following is how you would go about recovering your mnemonic:

1. Click on ‘Recover’ in the app.
2. Verify OTP sent to your email.
3. Send recovery request to trusted devices.
4. If required number of trusted devices accept your request, your recovery is complete!

Our [first blog post](https://medium.com/coinsafeapp/introducing-coinsafe-never-lose-your-bitcoins-ever-cbf69bce9099) goes in-depth into explaining this.

If you want a visual on our recovery process then watch [this video](https://twitter.com/CoinsafeApp/status/1080116080897605632).

---

**lambotango** (2019-02-21):

Interesting stuff. I’ve personally been wanting such a solution for my crypto holdings & I think [@vbuterin](/u/vbuterin) also had expressed his interest in the same : [Dark crystal slides from devcon (secret sharding utility ontop of SSB)](https://ethresear.ch/t/dark-crystal-slides-from-devcon-secret-sharding-utility-ontop-of-ssb/4074/2).

My question is what if multiple trusted devices lose access to the secrets, I wouldn’t be able to recover my mnemonic in that case?

---

**arnavvohra** (2019-02-21):

Yes, you wouldn’t be able to recover your mnemonic in such a case. Although, we are taking special measures to ensure something like this doesn’t happen. This includes:

1. Allow users to see the status of their trusted devices.
2. Send a notification to the trusted devices which asks them to open Coinsafe app and prove they have the secret with them (would only need to click some buttons on the trusted devices end).
3. Send periodic notification to the user (once a week or so) to open the Coinsafe app to check status of his/her trusted devices and change a trusted device in-case of inactivity.

There is no such thing as 100% security but we think these measures greatly enhance the security of a user’s shares.

---

**jettblu** (2022-11-17):

A few notes on your threshold scheme.

1. The model is heavily dependent on the availability of the encryption key (stored in your DB).
2. The model makes it less secure for Coinsafe (or another hosting company) to be a shareholder. Since Coinsafe has the privileged position of holding the decryption key, collusion or compromise at Coinsafe has more weight than collusion or compromise of other shareholders. Consider the case where Coinsafe gets K-1 shares. Coinsafe would now have access to both the cipher text and the decryption key.
3. Updating the number of shareholders would be a challenge. Legacy shares can always be copied and used to recover the original ciphertext. Have you considered whether a new encryption key would be used when updating the number of shareholders (dealing new shares)?

Overall, nice work. More thought is needed to develop better self custody schemes and I’m glad Coinsafe is working on a solution.

Finally, I included point #2 as you may want to consider adding third party shareholders for convenience and Coinsafe would be a natural canidate.

