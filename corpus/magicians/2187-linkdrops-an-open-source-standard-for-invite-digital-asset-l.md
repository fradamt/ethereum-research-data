---
source: magicians
topic_id: 2187
title: "Linkdrops: An open-source standard for invite & digital asset links on Ethereum (EIP 1077 + EIP1167)"
author: Kisgus
date: "2018-12-11"
category: Web > User Experience
tags: []
url: https://ethereum-magicians.org/t/linkdrops-an-open-source-standard-for-invite-digital-asset-links-on-ethereum-eip-1077-eip1167/2187
views: 1373
likes: 0
posts_count: 1
---

# Linkdrops: An open-source standard for invite & digital asset links on Ethereum (EIP 1077 + EIP1167)

### How does it work?

NB: As a new user I can only submit one picture + 2 links, for full references, including gas optimizations, links to repos and graphical step-to-step flows, please see this post: https://medium.com/@Gfriiis/linkdrops-an-open-source-standard-for-invite-digital-asset-links-on-ethereum-29f34b3fa5ec

#### Core Assumptions

- Bob is a new user without ETH, wallet or any prior crypto knowledge
- Alice has an EIP 1077 identity contract and a spare ERC721 Robot
- Alice share the invite link with Bob over a secure channel e.g Whatsapp
- There is an incentive in place (on a user, dapp or relay level) to pay gas

[![](https://ethereum-magicians.org/uploads/default/optimized/2X/a/a8e69bb27117c5474150ba0406276c51198ef765_2_498x500.png)757×759 12.3 KB](https://ethereum-magicians.org/uploads/default/a8e69bb27117c5474150ba0406276c51198ef765)

1. Bob is a new user without ETH, wallet or any prior crypto knowledge
2. Alice shares an invite link to Bob
3. Link includes a transit private key and a signature
4. Bob is directed to a webpage
5. Bob generates his own private key stored in the browser
6. Bob uses transit private key to sign Bob’s address
7. Bob’s browser sends his two signatures to the relayer
8. Relayer calls Alice’s identity contract
9. Alice’s identity contract creates an identity contract for Bob and sends a Robot
10. Bob is now onboarded to Ethereum and owns a robot that he can play with!

### Modular implementation of linkdrops

Based on rich iterations, the implementation of the Universal Login SDK Alex van de Sande & Marek has undergone updates towards a modular architecture since Devcon 4. Below is the current draft of a simple modular version of Invite Scheme without generating an identity contract for receiver:

The main function of the module is  ***transferTokensByLink*** *,*  which:

- Verifies 2 signatures (sender’s and receiver’s signatures)
- Checks that link wasn’t used before (by storing transitPubKey in storage)
- Transfers tokens from sender’s identity contract to receiver address

Sender’s signature verification can be done using  ***owner.canExecute***

And for transferring tokens, we can use  ***owner.moduleExecute***  *—*

Any feedback on how we can improve approve, highly appreciated!

### React Native Starter Implementation

As we are actively working to implement linkdrops including invite link functionality into different mobile applications, we have developed this Universal Login React Native. Feedback highly appreciated ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

#### Requirements

- NodeJS v10.12.0
- Yarn 1.10.1

This starter has been tested only on OS X.

#### Dependencies

This starter uses  `react-native-navigation`  (v1) for navigation.

`rn-nodeify`  package allows to use node core modules.

Native libs for secure and fast crypto:

- react-native-secure-randombytes
- react-native-fast-crypto

### Reducing Gas cost via Proxy delegation

In search of reducing the gas we decided research or proposed EIPs tackling this problem, with inspiration from best practices, such as Gnosis Safe, Tenzorum, Argent (https://www.argent.xyz/) and feedback from Pet3rpan from the #MetaCartel. Mikhail has proposed to reduce gas cost using proxy delegation.

#### Gasless implementation (without Universal Login integration)

FInally the newest enhancement in this regard is below gassless webdapp prototype, which can be considered an enhancement to the #burner wallet by Austin Griffith. We hope to a demo of the wallet soon and learn about you feedback.

###  Cryptoxmas.xyz  a charity NFT reference implementation of linkdrops (without Universal Login integration)

#### Cryptoxmas.xyz: Send Christmas NFT cards & support Venezuelans in need

Finally we have now found an application for the greater good, utilizing the linkdrop standard, the receiver only needs to click the link, and does not need to have an Ethereum wallet in advance. Excepts gas fees, every funds are sent to the Giveth Campaign Escrow contract.
