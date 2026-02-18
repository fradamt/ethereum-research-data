---
source: magicians
topic_id: 2045
title: "EIP-1581: Non-wallet usage of keys derived from BIP-32 trees"
author: andytudhope
date: "2018-11-28"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-1581-non-wallet-usage-of-keys-derived-from-bip-32-trees/2045
views: 863
likes: 4
posts_count: 1
---

# EIP-1581: Non-wallet usage of keys derived from BIP-32 trees

After the initial discussion [here](https://ethereum-magicians.org/t/non-wallet-usage-of-keys-derived-from-bip-32-trees/1817/2) with [@ligi](/u/ligi) providing some good feedback, non-wallet usage of keys derived from BIP-32 trees has been formalised into an EIP! ![:tada:](https://ethereum-magicians.org/images/emoji/twitter/tada.png?v=9)


      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-1581)




###

Details on Ethereum Improvement Proposal 1581 (EIP-1581): Non-wallet usage of keys derived from BIP-32 trees








Applications interacting with the blockchain often make use of additional, non-blockchain technologies to perform the task they are designed for. For privacy and security sensitive mechanisms, sets of keys are needed. Reusing keys used for wallets can prove to be insecure, while keeping completely independent keys make backup and migration of the full set of credentials more complex. Defining a separate (from BIP44 compliant wallets) derivation branch allows combining the security of independent keys with the convenience of having a single piece of information which needs to be backup or migrated.

We’ll be using this at Status for our Keycard (a java card that stores your keys separately from your device - which almost always already an adversarial environment), and as a means of ensuring that whisper keys and account keys are decoupled so that it is easier to handle the need for multiple identities/accounts/means of managing keys.

Any and all comments and feedback are appreciated! ![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=9)
