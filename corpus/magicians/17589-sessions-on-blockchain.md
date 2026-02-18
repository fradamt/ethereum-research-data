---
source: magicians
topic_id: 17589
title: Sessions On Blockchain
author: CryptoCoinism
date: "2023-12-22"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/sessions-on-blockchain/17589
views: 917
likes: 1
posts_count: 5
---

# Sessions On Blockchain

Hi everyone, I am new here, I have an idea for Ethereum blockchain and happy to share it with you so tell me your opinion about that.

**Sessions is a solution for the security of digital currency wallets (crypto wallets):**

In the world of cryptocurrency, security is considered the most important part of this technology because it is developing and expanding day by day and the general public is entering this market.

It has happened many times that people’s digital currency wallets have been hacked. Or the stress of connecting the wallet to a site through signature and also importing wallet recovery words (keywords) in wallet providers platforms such as Zerion Wallet, Tai Ho, Aim Token, etc. It causes dissatisfaction among users.

To solve this problem, we present a workaround here. In short, in this method, we deal with sessions (meetings) similar to what happens in Web 2. But with a difference that these sessions do not need to spend resources for permanent session validation and are validated when needed. Below is a complete description of this method.

At the beginning of the creation stage in the network, each wallet receives key phrases of the wallet, and then a session must be created to use the wallet. These sessions need to be displayed on the network so that in addition to better management of the wallet, we will be informed when unwanted sessions are created by hackers.

How to create a session using Timestamp:

To create disposable hashes, we need another expression that is combined with wallet keywords and creates a hash, so that when we need to import the wallet into a wallet server, it can be indirectly validated and connected to the network.

Here the random words that are supposed to be combined with the keywords and create another phrase with the help of the Timestamp function.

like this :

Seed Phrases + Timestamp = a

a=“aa”

Timestamp shows the date and time this session was created. As a result, we will not have two sessions with the same value.

for example :

“09072023175340” => 07/09/2023 , 17:53:40

Then we hash this expression “A” and store it in the network.

Whenever there is a need to import a wallet in a wallet server, we can use this created session. Just enter the generated hash to be verified.

Other people do not have access to this hash. Also, the keywords of the wallet are no longer visible.

We can use a password along with this output hash, which creates more security.

When the hash is entered and used in a wallet server, this created session starts working.

Sessions can be managed. That is, we can set limits for transactions and the amount of transfer of assets.

One of the other advantages of these sessions is that we can temporarily give access to the wallet to trusted friends or acquaintances without disclosing the key words of the wallet.

If needed, we can invalidate the session. Or stop the session for a short time. Be aware of unauthorized access.

---

**Implementation**

When a wallet is created, it receives its seed phrase. To use the wallet, a session must be created. These sessions must be visible on the network so that users can track their wallets and be alerted to unauthorized sessions created by hackers.

**Problem**

There have been many cases of cryptocurrency wallets being hacked. In addition, the process of connecting a wallet to a website through signing and importing the wallet’s recovery phrase (seed phrase) can be stressful and inconvenient for users.

**Solution**

We propose a solution to this problem using sessions, similar to what is used in web 2.0. However, our sessions do not require constant validation, and are only validated when needed.

**Implementation**

When a wallet is created, it receives its seed phrase. To use the wallet, a session must be created. These sessions must be visible on the network so that users can track their wallets and be alerted to unauthorized sessions created by hackers.

**Benefits**

This solution offers several benefits over the current state of the art:

Increased security: Sessions are a more secure way to connect wallets to websites than signing and importing the seed phrase.

Improved user experience: Sessions make it easier and more convenient for users to connect their wallets to websites.

Increased transparency: Sessions are visible on the network, which allows users to track their wallets and be alerted to unauthorized activity.

**Conclusion**

We believe that sessions are a promising solution for improving the security of cryptocurrency wallets. They offer a number of benefits over the current state of the art, and can help to protect users’ digital assets.

## Replies

**CryptoCoinism** (2023-12-22):

Sorry if my english is not good ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)

---

**lukaisailovic** (2024-11-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cryptocoinism/48/11185_2.png) CryptoCoinism:

> the process of connecting a wallet to a website through signing and importing the wallet’s recovery phrase (seed phrase) can be stressful and inconvenient for users.

How is this the case? I don’t import my seed phrase on random websites

---

**Nikita** (2024-11-13):

Potential Challenges:

1. Session Management Overhead: Implementing session revocation or expiration on-chain might introduce complexities, especially given Ethereum’s current gas costs. Managing these sessions efficiently without burdening users with extra fees could be tricky.
2. Scalability Concerns: If every session needs to be recorded on-chain, this could lead to bloating the state, potentially affecting network performance. You might need to explore L2 solutions or off-chain storage to mitigate this.
3. User Education: While this solution is technically solid, non-technical users may struggle to understand the concept of sessions, revocations, and session management. A good UI/UX will be essential to make this intuitive.

---

**undefined** (2025-04-14):

It sounds very ineffiecient, leaky and in general not desirable to require an on-chain tx for each session. You say they need to be displayed on the network but shoudn’t it be sufficient that the relevant parties have this information?

Some of what you are solving for sounds similar to Certificate Transparency in TLS PKI (which are indeed intentionally public)?

