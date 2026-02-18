---
source: magicians
topic_id: 17242
title: ERC-4337 meets zk-SNARKs with IoTeX
author: GiupiDeLuca
date: "2023-12-11"
category: ERCs
tags: [erc, wallet]
url: https://ethereum-magicians.org/t/erc-4337-meets-zk-snarks-with-iotex/17242
views: 1241
likes: 6
posts_count: 4
---

# ERC-4337 meets zk-SNARKs with IoTeX

ioPay (built by the IoTeX team) has just launched Account Abstraction, making ioPay the largest, battle-tested multi-chain AA wallet on the market. This article will focus on the importance of Account Abstraction (ERC4337), and how IoTeX has leveraged ERC4337 to build a zkSNARKS-based wallet.

### An AA refresher

Account Abstraction, as defined by ERC-4337, “allows users to use smart contract wallets containing arbitrary verification logic instead of EOAs as their primary account.” ERC-4337 introduces many user experience benefits, most notably enabling people to use Smart Contracts as their primary accounts.

ERC-4337 runs on top of the blockchain and does not require any changes to the blockchain itself.

### loTeX Modular Infra for DePIN

IoTeX is a full-stack blockchain based infrastructure (fully compatible with Ethereum ecosystem and tools) essential for applications that require custom proofs derived from off-chain data (like “proofs of physical work” in DePIN). DePIN is a new category in the web3 space, and it stands for Decentralized Physical Infrastructure Networks. DePIN applications facilitate token rewards to incentivize communities to run and maintain certain infrastructures.

Leveraging zk-SNARK proof technology, IoTeX has built an account abstraction wallet that can be authorized by password. Earning itself a grant from the Ethereum Foundation back in September, 2023. Specifically, the grant awarded was for [ERC-4337 and IoTeX’s work in employing Zero-knowledge Account Abstraction Wallets.](https://www.erc4337.io/?ref=iotex.io)

zk-SNARK (Zero-Knowledge Succinct Non-Interactive Argument of Knowledge) is a cryptographic proof system that enables one party to prove to another party that a statement is true without revealing any additional information beyond the validity of the statement itself. The term zk-SNARK is sometimes colloquially used to refer to any zero-knowledge proof system, but strictly speaking, zk-SNARK refers to a particular type of zero-knowledge proof system that has a succinct proof size and does not require interaction between the prover and verifier.

[![AA Details](https://ethereum-magicians.org/uploads/default/optimized/2X/9/9ad3685c70ebbf1ab755d57bd6a705e408009a48_2_690x379.jpeg)AA Details1686×928 93.8 KB](https://ethereum-magicians.org/uploads/default/9ad3685c70ebbf1ab755d57bd6a705e408009a48)

If you would like to test out the IoTeX’s MVP which earned zero-knowledge account abstraction grant you can do so at the following link: [https://zk-wallet-demo.iotex.io](https://zk-wallet-demo.iotex.io/?fbclid=IwAR304uZ5HsT3Hidy50F4YQ0FqAb_kstu-0ixJt4VgetysNZeTAOJwCjhaQU&ref=iotex.io).

### ioPay Implementation of Account Abstraction

ioPay has always had a deep focus on security and user experience. Both of which have been enhanced by the implementation of account abstraction. IoPay currently offers Gmail AA login support. In the near future ioPay plans to implement other methods of AA authentication. In building this feature into ioPay, the team leveraged P256 to authenticate wallet transactions and email based DKIM protocol to recover user accounts. DKIM( DomainKeys Identified Mail ) is an email authentication method that uses a digital signature to let the receiver of an email know that the message was sent and authorized by the owner of a domain. Once the receiver determines that an email is signed with a valid DKIM signature, it can be confirmed that the email’s content has not been modified. So we can verify DKIM signature users on-chain contracts and recover users ioPay accounts. P256 uses the secp256r1 elliptical curve, a widely accepted cryptographic standard that can be applied on EVM to create secure authentication and signing for transactions/smart contracts. Most of the modern devices and applications rely on the “secp256r1” elliptic curve. For example:

1. Apple’s Secure Enclave: There is a separate “Trusted Execution Environment” in Apple hardware which can sign arbitrary messages and can only be accessed by biometric identification.
2. Webauthn: Web Authentication (WebAuthn) is a web standard published by the World Wide Web Consortium (W3C). WebAuthn aims to standardize an interface for authenticating users to web-based applications and services using public-key cryptography. It is being used by almost all of the modern web browsers.
3. Android Keystore: Android Keystore is an API that manages the private keys and signing methods. The private keys are not processed while using Keystore as the applications’ signing method. Also, it can be done in the “Trusted Execution Environment” in the microchip.
4. Passkeys: Passkeys is utilizing FIDO Alliance and W3C standards. It replaces passwords with cryptographic key-pairs which is also can be used for the elliptic curve cryptography.Because IoTeX network already supports pre-compiled contracts that perform signature verifications in the “secp256r1” elliptic curve. It made sense to base ioPay AA wallet’s verification logic based on Apple’s Secure Enclave and Android Keystore with a constant gas cost. Leveraging the device’s secure enclave/keystore and biometric identification, we can achieve highly secure AA wallets.To encourage usage of these new AA wallets, for a limited time, IoTeX supplies 2 IOTX per day to pay for gas fees for user’s who leverage the ioPay AA wallet. If ioPay users own the MachineFi NFT they can receive 10 IOTX per day for gas fees as an extra level of utility for our MachineFi NFT holders.

## Replies

**iChristwin** (2023-12-15):

This is an interesting implementation. IoPay’s strategy to become the go-to wallet for interacting with DePINs through EIP-4337 is brilliant.

DePINs are poised to bring Web3 to the real world, connecting physical infrastructure like energy grids and transportation networks to the blockchain. This opens up a whole new realm of possibilities for ownership, management, and monetization while potentially attracting a new generation of web3 users.

However, the current web3 UX can be daunting for newcomers who not have the technical knowledge or comfort level to navigate traditional wallets. Having a wallet that shield users from the intricacies of web3, would greatly ease the entry of these new users into web3, and IoPay is positioned to be just that wallet.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/4/498b64df6194133aa670ef6b2f0696ea22bcbd95_2_690x388.jpeg)image1600×900 103 KB](https://ethereum-magicians.org/uploads/default/498b64df6194133aa670ef6b2f0696ea22bcbd95)

In short, ioPay’s strategic combination of DePINs and powerful ZKP technology behind EIP-4337 is just brilliant positioning. This innovative use of zk-SNARKs demonstrates its commitment to delivering a secure, scalable, and user-centric Web3 experience and I’m definitely keeping an eye on their progress!

---

**GiupiDeLuca** (2023-12-15):

Thanks for joining the convo [@iChristwin](/u/ichristwin) - I agree! I think 4337 become incredibly valuable in DePIN projects, where the end UX needs to abstract away native web3 complexities, as you said, like gas fees in various tokens, tx signing, etc…

I would love to see more engagement on this topic especially in the DePIN community!

---

**andrew_dropwireless** (2023-12-16):

Enhancing usability is pivotal for the widespread adoption of Web3. Even among tech-savvy communities, mastering the intricacies of cryptocurrency transactions can be quite challenging. In this context, our shared advertising use case, encompassing physical devices, media contents, and cryptocurrencies, stands out as a promising experimental platform for introducing IoTeX’s Account Abstraction (AA) to individuals accustomed to the Web2 landscape. AA possesses the potential to be a revolutionary force, significantly enhancing the accessibility of Web3 applications for the general public. Once again, commendations to the IoTeX team for their unwavering commitment and persistence in transforming complex DePIN use cases into reality. We stand united in this endeavor, placing our trust in IoTeX to lead the way in advancing Web3 perspectives.

