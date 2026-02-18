---
source: ethresearch
topic_id: 3127
title: Can a user exit if they lose their proofs?
author: MihailoBjelic
date: "2018-08-29"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/can-a-user-exit-if-they-lose-their-proofs/3127
views: 1506
likes: 7
posts_count: 9
---

# Can a user exit if they lose their proofs?

Let’s say I’m a user of a Plasma chain (MVP or Cash, doesn’t matter) and my HDD dies. I’ve permanently lost my UTXOs/coins history/branches…

(How) can I exit?

## Replies

**kfichter** (2018-08-29):

So it depends on exactly what Plasma implementation you’re using. In Plasma MVP, lots of peers have the chain and can provide you with the missing information.

In Plasma Cash, things are a little harder. If you completely lose your coin history/branches and the operator isn’t behaving, you’re pretty much out of luck. Of course the “solution” here is to try to mitigate this as much as possible - backups and replication, and maybe even incentivized third parties who store the data on your behalf.

---

**fubuloubu** (2018-08-29):

Trying to build intuition on this.

Let’s assume the operator is not malicious, or the operator is a PoA chain that can provide the history of spent UTXOs (e.g. coin history).

You’re out of luck only due to losing the key for the UTXO that proves the final ownership for the exit, correct? All txns from 0 to N-1 are still available.

Does that mean if the owner of the UTXO prior to you knows that you lost your keys, they can exit unchallenged? Or can anyone challenge that?

---

**MihailoBjelic** (2018-08-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> In Plasma MVP, lots of peers have the chain and can provide you with the missing information.

I’m a bit confused now - does everyone need to store the whole blockchain in Plasma MVP or only to validate it? ![:no_mouth:](https://ethresear.ch/images/emoji/facebook_messenger/no_mouth.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> In Plasma Cash, things are a little harder.

Exactly as I thought. Thanks. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**kfichter** (2018-08-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> In Plasma MVP, lots of peers have the chain and can provide you with the missing information.

I’m a bit confused now - does everyone need to store the whole blockchain in Plasma MVP or only to validate it?

Technically only validate it and keep their own witness data. Efficient implementations will have full nodes store the entire blockchain so they can gossip information and decrease load on the operator.

---

**kfichter** (2018-08-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/fubuloubu/48/2424_2.png) fubuloubu:

> Does that mean if the owner of the UTXO prior to you knows that you lost your keys, they can exit unchallenged? Or can anyone challenge that?

Even if you lose your keys the operator will challenge the exit (assuming they’re not malicious). However, you’re still out of luck in that you can’t actually withdraw the funds without the private key.

---

**MihailoBjelic** (2018-08-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> Efficient implementations will have full nodes store the entire blockchain so they can gossip information and decrease load on the operator.

Can I get more info about this somewhere? How will these nodes be incentivized? I’m working on a solution where such “nodes” will always exist, they will be bonded and incentivized and they have to confirm that they have received the data (via Proof of Custody) before a main chain checkpoint can be created. I hope that can solve both the problem of lost proofs and the data availability problem…

---

**ldct** (2018-08-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> Technically only validate it and keep their own witness data. Efficient implementations will have full nodes store the entire blockchain so they can gossip information and decrease load on the operator.

If your threat model implies “I must personally be able to protect my money, without relying on anyone else’s incentives” don’t you need to keep around other people’s witness data as well? It seems to me that you need to prevent successful exits of spent TXOs whose child TXO has earlier (i.e. numerically lower) priority than yours.

---

**kfichter** (2018-08-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> If your threat model implies “I must personally be able to protect my money, without relying on anyone else’s incentives” don’t you need to keep around other people’s witness data as well?

Yes, definitely. In this case you would also probably run multiple nodes and regularly back up the chain somewhere else.

