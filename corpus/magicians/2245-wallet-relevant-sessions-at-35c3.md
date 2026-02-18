---
source: magicians
topic_id: 2245
title: Wallet relevant sessions at 35c3
author: ligi
date: "2018-12-18"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/wallet-relevant-sessions-at-35c3/2245
views: 1648
likes: 4
posts_count: 4
---

# Wallet relevant sessions at 35c3

Hey - hope to see some members of the wallet ring at 35c3! Here some sessions that might be interesting to wallet devs:

## Lecture: wallet.fail

### Hacking the most popular cryptocurrency hardware wallets

https://fahrplan.events.ccc.de/congress/2018/Fahrplan/events/9563.html

## Lecture: Wallet Security

### How (not) to protect private keys

https://fahrplan.events.ccc.de/congress/2018/Fahrplan/events/9492.html

## Lecture: A Blockchain Picture Book

### Blockchain origins and related buzzwords, described in pictures.

https://fahrplan.events.ccc.de/congress/2018/Fahrplan/events/9573.html

## Session: Ethereum Magicians gathering

https://events.ccc.de/congress/2018/wiki/index.php/Session:Ethereum_Magicians_gathering

## Replies

**ligi** (2018-12-21):

One more interesting session (yes keys on smart-cards will be a thing in 2019 - https://github.com/status-im/status-keycard):

https://fahrplan.events.ccc.de/congress/2018/Fahrplan/events/9346.html

cc [@bitgamma](/u/bitgamma)

---

**Tbaut** (2019-01-04):

Thanks for that, all the talk are viewable and downloadable here https://media.ccc.de/b/congress/2018

---

**esaulpaugh** (2019-01-04):

I have an idea about using iterated hashing to mitigate password-protected wallet owners’ vulnerability to coercion:

Time-Lock ASICs for Password-protected Wallets: https://github.com/esaulpaugh/scratchpaper/blob/master/Crypto-Time-Lock

Instead of memorizing your wallet password, memorize your wallet password’s seed and hash it repeatedly to generate the wallet password. Seed (i.e. master password) “Jeb!2064” might produce derived password “bdrvpUu8N8xN3s7xi22jM” after 80 billion iterations.

By the time the attacker knows you’ve given him a fake (master) password, many hours or days will have elapsed, making attacks expensive/risky.

