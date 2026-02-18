---
source: ethresearch
topic_id: 1746
title: Plasma Mass Withdrawal vs Simple Withdrawal
author: gongbully
date: "2018-04-16"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-mass-withdrawal-vs-simple-withdrawal/1746
views: 1622
likes: 3
posts_count: 10
---

# Plasma Mass Withdrawal vs Simple Withdrawal

In a byzantine situation, why should individual go through mass withdrawal rather than simple?

In a individual’s point of view, simple withdrawal seems to be fast and simple withdrawal is not banned in a byzantine situation too.

Then why should one choose mass withdrawal? I know fee can be relately low, but I can not think of other factors

than fee.

## Replies

**vbuterin** (2018-04-16):

I actually don’t think mass withdrawals are necessary, especially in a plasma cash setup. Each user could just wait until either their account specifically gets attacked or they actually need to move their funds and only do a plasma withdrawal then.

---

**gongbully** (2018-04-16):

Thanks vitalik for your perfect answer!

---

**MihailoBjelic** (2018-08-26):

I guess it is the only economical way to exit small value UTXOs (smaller than the main chain exiting fee).

---

**gakonst** (2018-08-26):

But Mass Exits/Withdrawals are actually a security requirement in any non-NFT Plasma Design similar to Plasma Cash, e.g Plasma MVP. Otherwise, a malicious operator can create a huge UTXO, exit that, and if the number of UTXOs that need to be exited is big enough, rootchain blocks will not have the capacity to fit them all, before the malicious exit from the operator goes through.

---

**MihailoBjelic** (2018-08-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> a malicious operator can create a huge UTXO, exit that, and if the number of UTXOs that need to be exited is big enough, rootchain blocks will not have the capacity to fit them all, before the malicious exit from the operator goes through

How can this happen? AFAIK, time ordering of UTXOs when exiting is still a part of the Plasma MVP design? If a malicious operator creates a huge invalid UTXO, users should immediately spot it, stop transacting on that chain and start submitting exits. The huge invalid UTXO will be the last in the exit queue, so the contract will be emptied out before that exit is processed? The same will happen even if he creates the UTXO, withholds the block and try to exit (users will start exiting because they can not trust the operator who withholds blocks).

---

**gakonst** (2018-08-26):

> The huge invalid UTXO will be the last in the exit queue, so the contract will be emptied out before that exit is processed?

Napkin math ahead:

Operator submits exit. Each block can handle 9 million gas. Let’s say that a new block gets mined every 15 seconds. There are 40320 blocks per week. Let’s also consider that the exit period is a week. Each exit let’s say costs 100k gas.

40.320 * 9.000.000 / 100.000 = 3.628.800 UTXO exits that can fit in that period, which is the maximum we can handle with the above things in mind

I’d imagine that having 3.6 million UTXOs being exited for a large plasma chain to be reasonable. Also consider that you do not have only exit transactions in the above said gas capacity, you may have any other challenge related tx’s with respect to the plasma contract in question, let alone any other on-chain gas costly ones. So yes, I do believe that in non-NFT Plasma designs are much necessary

---

**MihailoBjelic** (2018-08-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> Napkin math ahead

I don’t see the point of this whole calculation if, as I’ve pointed out, UTXOs are exited in the order in which they were created?

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> a malicious operator can create a huge UTXO

Maybe you wanted to say “a malicious operator can create a huge number of UTXOs”? But then again, all those UTXOs will be at the end of the queue…

I think what your’re pointing out is a valid concern, but the same thing will happen with such a large number of UTXOs to exit even when those malicious UTXOs don’t exist, they don’t affect this problem in any way?

---

**gakonst** (2018-08-26):

An exit can be finalized T time after it was submitted, but the priority is being set by the outputs (or inputs in the More Viable Plasma Design) of the UTXO included in the exit, not by the time that the exit itself is submitted.

A malicious operator can create 1 UTXO that gives them a huge amount of PETH (or even the whole amount of PETH in the plasma chain/contract), and exit that. At that point all users must rush and exit their UTXOs, otherwise if they cannot fit an exit before the finalization of the operator’s exit (7 days later) they’ll lose their ETH that was locked in the plasma contract.

---

**MihailoBjelic** (2018-08-26):

Oh, now I get you. And you totally have a point.

Actually, that could be a big issue now that I think about it. Imagine a situation where a big Plasma chain (definitely millions of UTXOs) gets corrupted and users are starting to exit, while at the same time the main chain is clogged by some new CryptoKitties and a few big ICOs. ![:radioactive:](https://ethresear.ch/images/emoji/facebook_messenger/radioactive.png?v=9)![:skull_and_crossbones:](https://ethresear.ch/images/emoji/facebook_messenger/skull_and_crossbones.png?v=9)![:scream_cat:](https://ethresear.ch/images/emoji/facebook_messenger/scream_cat.png?v=9) That 3.6M possible exits will go down to thousands…

