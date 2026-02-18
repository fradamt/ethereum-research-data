---
source: ethresearch
topic_id: 1055
title: What are the expected computational requirements to join a validator pool?
author: jamesray1
date: "2018-02-12"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/what-are-the-expected-computational-requirements-to-join-a-validator-pool/1055
views: 3147
likes: 4
posts_count: 13
---

# What are the expected computational requirements to join a validator pool?

At the moment it isn’t feasible for my computer to mine, as it is a Streacom FC8 which can’t physically fit GPUs. Additionally, with the transition to PoS, it isn’t feasible to buy a mining rig, as it’s unlikely to get a payback. What I want to know is whether my existing computer (as well as most modern desktop computers) would be able to join a validator pool with PoS?

My computer’s specs are:

[![Screenshot from 2018-02-12 12-23-37](https://ethresear.ch/uploads/default/original/1X/f52e8bbbcd48af0d8a9008009fa2f29173e97493.png)Screenshot from 2018-02-12 12-23-37456×444 28.1 KB](https://ethresear.ch/uploads/default/f52e8bbbcd48af0d8a9008009fa2f29173e97493)

## Replies

**vbuterin** (2018-02-12):

If you can run a full node you’ll be fine.

---

**jamesray1** (2018-02-12):

The problem is that I don’t think I can run a full node, at least, Mist 0.8.9 didn’t work for me; the disk got too full, and I had issues trying to put the data on an external HDD. But I realise that running a full node is a requirement for being a miner or a validator, although maybe not for stateless clients.

---

**jamesray1** (2018-02-12):

I managed to run geth on the external hard drive with `james@james-Streacom:~$ geth --datadir /media/james/"Seagate Expansion Drive"`. If I have further issues I’ll post them on Github in the Geth repo.

---

**vbuterin** (2018-02-12):

Try Parity with an SSD.

---

**jamesray1** (2018-02-12):

Running Parity doesn’t slow the internet down so that I can’t really use the computer (indeed there is barely a noticeable difference in speed), whereas with Geth it’s too slow to browse with it running.

---

**kladkogex** (2018-02-12):

If you have $300,000 for a deposit, then arguably a new server price is peanuts! ![:rofl:](https://ethresear.ch/images/emoji/facebook_messenger/rofl.png?v=9)![:rofl:](https://ethresear.ch/images/emoji/facebook_messenger/rofl.png?v=9)![:rofl:](https://ethresear.ch/images/emoji/facebook_messenger/rofl.png?v=9)

---

**jamesray1** (2018-02-13):

I was thinking more of validator pools.

---

**nootropicat** (2018-02-14):

What do you mean $300k? Something changed regarding the minimum stake?

---

**jamesray1** (2018-02-15):

I don’t know what the latest document is which suggests what the staking size might be, but I don’t think it has been set in stone. Perhaps [@vladzamfir](/u/vladzamfir), [@vbuterin](/u/vbuterin), [@nate](/u/nate), [@djrtwo](/u/djrtwo) or someone else can clarify.

---

**kladkogex** (2018-02-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/nootropicat/48/258_2.png) nootropicat:

> What do you mean $300k? Something changed regarding the minimum stake?

If you dig this message board you will find a mention  of 1000 ETH.

Which is $876K I believe as of today.

Which illustrates the problem with deposits -  you want the validators to be executed by independent security professionals, but whats you may end up with is a highly centralized system owned by miners. Miners have lots of money and lots of incentives to control validators as well as lots of technical knowledge to run validators.   In the current system, what is pretty much guaranteed to happen is large miners are going to buy up validators and then they control everything.

It may be that one should have a hybrid system, where there is a reasonable deposit (say $10K), but then you need both to deposit money and get enough community stake votes to become a validator. So it is delegated stake + deposits.

---

**toliuyi** (2018-03-25):

1000 ETH is really a big fortune. Is that possible to make a contract to be a validator? Then small investor could invest a share on that casper mining pool contract.

---

**kladkogex** (2018-03-26):

Yes - [it is possible as described here](https://ethresear.ch/t/decentralized-casper-validator-proposal/1430/3).

100 security researchers can deposit 15ETH to create a “Decentralized Validator”

