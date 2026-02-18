---
source: magicians
topic_id: 1167
title: "EIP-1355: Ethash 1a"
author: chfast
date: "2018-08-27"
category: EIPs
tags: [mining]
url: https://ethereum-magicians.org/t/eip-1355-ethash-1a/1167
views: 4773
likes: 3
posts_count: 6
---

# EIP-1355: Ethash 1a

https://github.com/ethereum/EIPs/pull/1355

## Replies

**atlanticcrypto** (2018-08-30):

Does anyone have information on the BM1790 to know what its logic actually looks like? Is there a way to figure out if this device is programmable? I have one, currently ripped to shreds on a table. I am willing to destroy this thing to provide any information needed to the community. Fire, water, earth…plasma torches…whatever you need.

---

**salanki** (2018-08-31):

[@chfast](/u/chfast) what are the odds we can get this into Constantinople now that the issuance reduction is decided? Even if it turns out that the ASICs are programmable, it would be a good way to show miners that the devs are committed to decentralization. The end goal should be a more robust POW change like ProgPow.

---

**timolson** (2019-01-21):

This does next-to-nothing to stop ASIC’s. It is easily ECO’d.  Monero tried something similar by adding an XOR to their “v1” anti-ASIC tweak, but if you look at the hashrate of coins which stayed with this variant of CryptoNight, it is clear that all the Monero ASICs continued to work after such a change. Ethereum has plenty of value, and current ASIC manufacturers could have an ECO’d chip with your new FNV constant faster than you can get this proposal through committee.

---

**chfast** (2019-01-21):

What is ECO?

…

---

**timolson** (2019-05-31):

[en.m.wikipedia.org](https://en.m.wikipedia.org/wiki/Engineering_change_order)




###

Engineering change orders (ECO) are used for changes in components, assemblies, or documents such as processes and work instructions.  They may also be used for changes in specifications. Lastly, it can be "a modification that will have an effect on a manufactured product or manufacturing process."
 ECOs are also called an "engineering change note", engineering change notice (ECN), or just an engineering change (EC).
 In a typical system development cycle, the specification or the implementation...

