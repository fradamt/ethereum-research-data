---
source: magicians
topic_id: 1292
title: Notes fom the wallet workshop at web3 UX unconference in Berlin
author: ligi
date: "2018-09-10"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/notes-fom-the-wallet-workshop-at-web3-ux-unconference-in-berlin/1292
views: 2263
likes: 14
posts_count: 9
---

# Notes fom the wallet workshop at web3 UX unconference in Berlin

We just had a workshop in the context of the [web3 UX unconference](http://discuss.conflux.network/t/web3-ux-unconf-september-10th-berlin-blockchain-week-full-node-berlin/114) in Berlin which happened as part of the Berlin BlockChain week.

The following projects participated:

Projects:

- daily
- zCash
- Gnossis Safe
- ENS
- BlockParty
- imToken
- Parity Fether
- WallETH

First we where talking about fiat conversion because this is important for onboarding new users and a good starting point. Often this is called fiat conversion - but we agreed that “fiat” is actually a bad term as it is mainly used in the crypto space but not a word that is familiar to most average users. We really need a *crypto glossary* and agree on a common terminology. Perhaps even surveys/research which terms best represent the concept for average people.

- a ban in certain countries can make the problem of onboarding users with crypto even worse (e.g. india or china)

legal implications can often be bypassed by small projects and small amounts
- imToken will spilt into 2 apps to deal with the regulations problem

[localEthereum](https://localethereum.com) can address the problem but is a silo and centralized single point of failure and can also be blocked by governments
we can onboard users at meetups by giving them crypto there or trading for government money

- we can also do “pre meetups” before BlockChain meetups - start e.g. 30min before the meetup to hand out crypto to users

it is also possible to charge for events and use this to onboard users with cryto then
we can make onboarding parties dedicated to onboard users with crypto
DAILY does a $10 drop to all venezueleans (which is nice but unfortunately does not scale to solve the problem globally)
the time it takes to get crypto is a big pain point (e.g. registration at coinbase)
KYC is another problem and might even be a blocker some times (parity was talking about how [PICOPS](https://picops.parity.io) was shut down because of GDPR
selling of cards (e.g. [ethercards](https://ether.cards)) can also be an option - users know this pattern from buying amazon or google play cards at stores - but has these problems at the moment:

- expensive currently (can get cheaper with more volume)
- another problem is that you need to trust the vendor (we might get technical solutions for this  - and one was named in the workshop - AFAIR color card - but when googling for it nothing came up - when the one dropping this info could give us a link that would be awesome - AFAIR it was makoto)
- currently ethercards is using mnemonic words to transfer the private keys. This is not ideal UX wise as users have to enter them. (EIP-1001 could help here in the future)

[wyre](https://www.sendwyre.com) was named as a solution and imToken is going to implement support

[bisq](https://bisq.network) is a decentralized solution based on TOR
selling hardware wallets (e.g. [opendime](https://opendime.com)) preloaded with crypto can be an option

Then we where talking about standards. There was discussion what standards actually are. First we where talking about standards in the sense of how wallets currently do and name things.

- displaying addresses:

addresses are long and ugly - often addressed by putting 3 dots in the middle - e.g. imToken displays 6 digits then 3 dots then again 6 digits. This is OK in overview and lists - but in some security relevant cases there should be the option to display all digits as brute forcing can be a problem if there are too few digits displayed
- if you display the full address you can use different shades/colors for the digits that are usually replaced by the 3 dots to improve UX (done by gnosis safe)
- often addresses are accompanied by identicons (e.g. blockies) - unfortunately blockies do not look that nice - for some cases the upcoming ethereum avatar standard can be an option - we also hope that nicer looking alternatives to blockies like flameID will be usable in the future.
- converting addresses to color sequences is also a nice option to make them easily recognizable for users - one project was doing this by directly converting the hex from the addresses to hex color code sequences.

displaying values:

- three dots or a tilde can indicate that the value is not precise (there as some disagreement which is the better option - 3 dots are more know to users but take more space than a tilde)
- clicking on it shuld reveal the precise value
- really hard to know where to cut of and how many digits to display users
- the units wei szabo finney should not be exposed to users too many terms will just confuse users - so this list is a really bad example - we need to find other ways to honor these humans

Then we where talking of standards more in the EIP sense of standards. Unfortunately even quite old standards - e.g. 681 still have low adoption - which is leading to a [lot of frustration](https://github.com/ethereum/EIPs/pull/681#issuecomment-417770108).

This part of the discussion was even leading to 2 action items (YAY):

- create a matrix where users can see what wallets support which standard (I will plant that seed but could use help than to fill gaps and add wallets)
- create a view on standards/EIPs as these are too many currently - so we need a site where you easily find e.g. all standards for wallets or all standards for contracts (perhaps this could be done on https://eips.ethereum.org cc @Arachnid )

Lastly we where talking about how to store and exchange keys. There are 2 main methods currently:

- JSON

advantage is that it has password protection
- unfortunately in v3 it is not possible to export this to a mnemonic in a compatible way (see the discussion here)
- you can use it with other tools/services like keepass

Mnemonic

- advantage is that it is possible to memorize (store/transport in your head)
- widely used
- you can write them down securely and fireproof on steel
- disadvantage: unprotected

raw keys

- just don’t

Big thanks to all participants, the organizers of the unconference and alejandro for facilitating this workshop!

## Replies

**divraj** (2018-09-11):

http://www.beelinereader.com/ was the color coding tool referenced as example for color coding addresses.

---

**oz1127** (2018-09-13):

This is great! Didn’t know the existence of this workshop. I am organizing [ledgerz.org](http://ledgerz.org) blockchain developers community in Berlin. If you are interested to do a version of this workshop in collaboration, I would be happy to contribute on organizing! I could help with the space and facilities, we could do an announcement on [meetup.com/ledgerz](http://meetup.com/ledgerz) for inviting people. Let’s contact!

---

**ligi** (2018-09-16):

[@divraj](/u/divraj) thanks for the link - do you by some chance have some deep link with more information? Somehow this site is not really filled with information about this …

[@oz1127](/u/oz1127) we should sure make this again! Thanks for the offer.

---

**p0s** (2018-09-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> This part of the discussion was even leading to 2 action items (YAY):
>
>
> create a matrix where users can see what wallets support which standard (I will plant that seed but could use help than to fill gaps and add wallets)
> create a view on standards/EIPs as these are too many currently - so we need a site where you easily find e.g. all standards for wallets or all standards for contracts (perhaps this could be done on https://eips.ethereum.org  cc @Arachnid )

I can help with the Matrix part. Let me know whether you started already! [@ligi](/u/ligi)

---

**ligi** (2018-09-18):

I struggled a bit with how it should look like - but I will start now with the data first. Just created the organisation ethereum-wallets to get distance from a specific implementation. Want to use it also for some android library that can resolve wallets depending on requirements.

Could use help with which fields should be added and then a PR for imToken ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

---

**p0s** (2018-09-19):

I’m still not too good with github. So please me know if I need to change anything directly in github!

---

**ligi** (2018-09-19):

Looks good so far - thanks!

---

**ligi** (2018-09-24):

I found a better link for the coloring of addresses: https://github.com/ethereum/EIPs/issues/928#issuecomment-389536771 - found it again after a new post there. The beeline link does not give too much information - this was the link I was searching in the first place - but it was buried in another topic …

