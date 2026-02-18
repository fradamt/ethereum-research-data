---
source: magicians
topic_id: 6697
title: Adding ABI to hardware wallet to decode DeFi transactions
author: Lixin
date: "2021-07-20"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/adding-abi-to-hardware-wallet-to-decode-defi-transactions/6697
views: 611
likes: 2
posts_count: 4
---

# Adding ABI to hardware wallet to decode DeFi transactions

Hi Magicians,

Here is a new demo of our hardware wallet Keystone - https://twitter.com/KeystoneWallet/status/1415316932954255362

Basically we put a big pack of ABIs (thanks to Sourcify’s work) into microSD card and insert the card into the device. Then the device will be able to use the ABI to decode complex DeFi transactions.

What even cooler is that we allow user to customize his own ABI into the microSD card.

This will enable the user to fully verify a DeFi transaction on his hardware wallet.

Please let me know if you have any comments about this.

## Replies

**tyevlag** (2021-07-20):

The video looks very cool, but it doesn’t seem to be particularly friendly to ordinary users?

---

**Lixin** (2021-07-20):

Good point.

Right now the plan is:

For average users, we will embed top DeFi projects’ (30-50 projects) ABI with our firmware. So they just need to upgrade and that’s it.

For power users, we will put those ~60k ABIs into a zip pack. Power users can download it, unzip, put it in microSD and insert it into our hardware wallet (user can put their own ABI into it too). The UX is cumbersome but it can theoretically cover all Defi projects.

For average users, we can do one more step to close more attack surfaces-

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/3/34ef36331dbffde8ec604fe8164e3999485d5764_2_500x500.jpeg)image1200×1200 213 KB](https://ethereum-magicians.org/uploads/default/34ef36331dbffde8ec604fe8164e3999485d5764)

---

**tyevlag** (2021-07-20):

It’s really great. It can let users know what they are doing to a certain extent ![:grinning_face_with_smiling_eyes:](https://ethereum-magicians.org/images/emoji/twitter/grinning_face_with_smiling_eyes.png?v=9)

