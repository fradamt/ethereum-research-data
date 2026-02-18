---
source: ethresearch
topic_id: 6138
title: Ethereum 2 address format
author: jgm
date: "2019-09-15"
category: Sharding
tags: []
url: https://ethresear.ch/t/ethereum-2-address-format/6138
views: 2828
likes: 5
posts_count: 4
---

# Ethereum 2 address format

Has there been any thought given to the format for Ethereum 2 addresses?  Obviously we can stick with the current format, but do we want to do anything different?  Explicit checksums/error detection?  A different encoding system such as https://github.com/bitcoin/bips/blob/33e6283a68ad4573d7418152350f93e39dc7e2cd/bip-0173.mediawiki ?

## Replies

**delbonis** (2019-09-15):

I’m a big a fan of the bech32 address encoding given the very nice error detection properties it has.  Another underappreciated benefit is case insensitivity, which is helpful from a usability standpoint when reading addresses out loud or typing them in manually from another device.  Could also look into sneaking a few extra bits of useful information in the address like if the address is a user or contract account, and that would be pretty opaque to users since it’s hidden inside the BCH code.  Perhaps using a human-readable prefix of `eth`.

Downsides of this of course is that wallets and user applications would have to be rewritten to support the new address format, but since things are being rewritten for eth2 anyways the situation might not actually be as mixed as it is for bitcoin segwit addresses currently.

---

**jgm** (2019-09-16):

Not sure that adding in the type of contract would be workable, as it’s not information that will always be to-hand (and the lines will be blurred a fair bit with account abstraction).

Would definitely need a suitable prefix if bech32 was used; `eth` seems to be the obvious one (and gives us immediate non-hex characters so we can differentiate between hex and this format).

---

**p_m** (2020-12-09):

Bump. I think this needs to be discussed soon (phase1 is close).

SHA256 seems to be the choice for v2 nowadays. So, the format is different already.

Should bech32 be applied? How long should the addr be?

