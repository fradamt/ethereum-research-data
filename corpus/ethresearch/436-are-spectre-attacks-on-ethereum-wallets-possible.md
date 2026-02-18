---
source: ethresearch
topic_id: 436
title: Are Spectre Attacks on Ethereum Wallets possible?
author: kladkogex
date: "2018-01-04"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/are-spectre-attacks-on-ethereum-wallets-possible/436
views: 2865
likes: 5
posts_count: 7
---

# Are Spectre Attacks on Ethereum Wallets possible?

A number of side-channel attacks on Intel and ARM processors have been released this week by [Paul Kocher](https://en.wikipedia.org/wiki/Paul_Kocher) and collaborators. These attacks exploit processor features such as speculative execution to let un-privileged processes read kernel memory, essentially breaking the entire security model of the operating system.

https://spectreattack.com/spectre.pdf

> As a  proof-of-concept,   JavaScript  code  was  written that,  when  run  in  the  Google  Chrome  browser,  allows JavaScript  to  read  private  memory  from  the  process in  which  it  runs.

Interesting to understand how will this apply to Ethereum wallets, specically Browser-base wallets … A question is whether Metamask and Mist are vulnerable to attackers stealing private keys … Note that the poc code reads the private memory of the browser process, but from reading the rest of the paper it seems that the entire memory space is vulnerable …

## Replies

**vbuterin** (2018-01-05):

Eek ![:frowning:](https://ethresear.ch/images/emoji/facebook_messenger/frowning.png?v=9)

Probably; it seems to me that the only way to defeat attacks that can access the entire memory is to either come up with some scifi scheme to avoid using memory entirely (ie. somehow implement a Turing-complete language directly using file system operations and use that to sign; no idea if this is possible) or use a secure hardware device. Though people with more domain knowledge than me can probably come up with something better.

---

**nootropicat** (2018-01-06):

Yes, but that can be mitigated by running every tab in a separate process with no shared sensitive memory. Until all browsers implement that remember to run web wallets in a completely separate browser instance.

Which in case of metamask on chrome unfortunately means a separate browser profile.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Probably; it seems to me that the only way to defeat attacks that can access the entire memory is to either come up with some scifi scheme to avoid using memory entirely

Moving signing to a non-mapped gpu memory should be enough. Unless gpus are also vulnerable to spectre…

---

**tymat** (2018-01-14):

How do you go from private key storage to GPU and keyboard (passphrase) to GPU without touching the CPU/RAM?

---

**nootropicat** (2018-01-15):

It’s ok to touch cpu as long as keys are in registers only and never leave them (eg. during a context switch), meltdown can only read ring0 memory. This would require a kernel module.

In principle it would allow running with a fully encrypted memory (code+data) as long as the key is safely put it during the boot process.

Somewhat related, enterprise gpus support direct io, like in [this project](https://github.com/enfiskutensykkel/ssd-gpu-dma). It’s called gpudirect for nvidia and directgma for amd.

---

**Etherbuddy** (2018-01-21):

The possibility of an attack makes cold storage solutions even more important.

---

**vbuterin** (2018-03-05):

This is also why partial slashing is important ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

