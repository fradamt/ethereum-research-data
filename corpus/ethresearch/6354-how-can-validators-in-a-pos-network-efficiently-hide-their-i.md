---
source: ethresearch
topic_id: 6354
title: How can validators in a PoS network efficiently hide their IP addresses
author: mc8864
date: "2019-10-18"
category: Privacy
tags: []
url: https://ethresear.ch/t/how-can-validators-in-a-pos-network-efficiently-hide-their-ip-addresses/6354
views: 3194
likes: 9
posts_count: 6
---

# How can validators in a PoS network efficiently hide their IP addresses

Is it possible for validators in a PoS network to hide their IP addresses without causing issues?

## Replies

**Mikerah** (2019-10-18):

There has been some work done on this in the past. Namely, [this proposal by the Pegasys R&D team](https://ethresear.ch/t/anonymity-a-zkp-to-remove-the-mapping-ip-address-wallets-public-key-of-a-validator/6049/2) and [this proposal by me to use Dandelion++](https://github.com/ethresearch/p2p/issues/11). There are other proposals in [this no longer used github repo](https://github.com/ethresearch/p2p) (see the issues for the proposals).

I am currently working on anonymity networking for PoS networks. I’ll try to have some more thoughts and criteria posted on here in the next month.

---

**kladkogex** (2019-10-18):

You can pretty much use any anonymizer VPN

---

**Mikerah** (2019-10-18):

No you can’t. PoS validators are sensitive to both latency and bandwidth. If such a validator uses any VPN, they are making themselves susceptible to slashing.

---

**mc8864** (2019-10-21):

Thanks for your reply Mikerah! I think indeed both Pegasys’s proposal or your twist of Dandelion++ make associating IP addresses with public keys difficult. But since the set of all IP addresses is still exposed/public, in an extreme case the government can simply take out all the validators using their public IP information. What measures do you think might address this issue?

---

**Mikerah** (2019-10-21):

This is still an open question! Potential solutions include using onion/garlic routing or mix nets.

