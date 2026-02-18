---
source: magicians
topic_id: 15313
title: Metamask fork for using SIM as hardware wallet
author: Evonne
date: "2023-08-01"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/metamask-fork-for-using-sim-as-hardware-wallet/15313
views: 533
likes: 7
posts_count: 5
---

# Metamask fork for using SIM as hardware wallet

Hi Magicians,

Wallet keys should be stored in a hardware wallet, but hardware wallets are difficult to use, especially with mobile devices.  So, we came up with a solution to use the SIM card as the hardware wallet.

**PoC**

An overlay SIM card with a custom Java SIMGap applet as the hardware wallet, it stores the keys and signs transactions.

An APP (MetaMask fork) as the user interface to show it can be integrated and work with existing software.

See the video demo at the bottom.

**Details**

As mentioned, the APP is forked from MetaMask to show how existing software can work with the SIMGap hardware wallet with only minor changes.  The APP does not store or access keys, it obtains user input for the transaction and sends the transaction details to the SIMGap hardware, the wallet keys are stored in the SIMGap and the SIMGap wallet does the signing.

APP used in video: [GitHub - TaisysTeam/metamask-mobile](https://github.com/TaisysTeam/metamask-mobile)

**Demo Video**

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/3/3323a36ede04f1a8d38e95e204e590dbdd882802.jpeg)](https://www.youtube.com/watch?v=96V-Ctx5o5k)

[@Aaron](/u/aaron) [@rekmarks](/u/rekmarks)

## Replies

**Mani-T** (2023-08-01):

SIM cards have limited memory and processing capabilities compared to dedicated hardware wallets. This limitation might affect the number of keys that can be stored and the efficiency of cryptographic operations.

---

**Evonne** (2023-08-02):

Yes, the limits of the SIM would probably be more restricting compared to dedicated hardware wallets, but it comes with the benefits of being less costly, easier to carry and use (in the mobile phone environment), etc.

---

**Kapu** (2023-08-05):

If we were to use SIM for hardware wallet, for sure higher end chip capability had to be considered and many options are in place. No worries.

---

**Mani-T** (2023-08-07):

Thank you for your answer.

