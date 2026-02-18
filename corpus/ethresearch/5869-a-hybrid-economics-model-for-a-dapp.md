---
source: ethresearch
topic_id: 5869
title: A hybrid economics model for a Dapp
author: kladkogex
date: "2019-07-25"
category: Economics
tags: []
url: https://ethresear.ch/t/a-hybrid-economics-model-for-a-dapp/5869
views: 2231
likes: 4
posts_count: 5
---

# A hybrid economics model for a Dapp

TLDR; Today’s Dapps (think decentralized Uber) are not successful with consumers, because not enough consumes have ETH or ERC-20 tokens. We introduce a hybrid model, which starts with fiat and issues loyalty tokens on each transaction.  Once loyalty tokens become established, they can be used in lieu of fiat. The system then enables a smooth slow transition from 100% fiat to 100% crypto.

Lets take an example of a decentralized Uber (DUber).  A DUber based on ETH will fail with today consumers, since majority of them do not have ETH tokens.

To remedy this, a DUber token is established, which works as follows

- you mint two tokens on every transaction, awarding one token to the driver and one to the passenger.
- the passenger pays to the driver in fiat, but if the passenger has tokens, they can be used to get discount X off the fiat price. For instance, each DUBER token can equate to 0.1% discount, up to discount_limit = 20%
- discounting  is assumed collectively by all drivers, meaning that all fiat money goes to the common account. A particular driver will get the same payment per trip nomatter whether a particular passenger used the discount or not.
- Once DUBER tokens establish market fiat value, passengers will be able to pay per trip directly in DUBER tokens.
- What you get then, is an hybrid ecosystem where some passengers pay in fiat and some in DUBER. The key is then to slowly increase discount_limit up to 100% percent ( this may take, say, 20 years).
- The advantage of the model is that it enables a smooth over-many-years transition from fiat to crypto.

## Replies

**bgits** (2019-07-25):

If the economic value of the DUBER is a discount on rides why then is a DUBER minted for the driver, what value would the driver have from a discount on rides?

Have you considered using the same minting approach without discounting and having the platform fee (normally the 20% of the drivers fee going to Uber) go to a pool? How the funds in the pool would be disbursed is decided by the collective DUBER holders. Using the minting model described above the largest stakeholders in the network would be the most active drivers and riders and the value of the token would be derived from it’s proportional claim on the assets in the pool, which could be used for network improvements or a return of funds to stakeholders as a loyalty dividend.

---

**Futurizt** (2019-07-28):

The problem with Dapp today starts way earlier than having or not having a coin. It starts with a seed phrase. The motivation of going through a seed phrase hell for getting some dubious tokens is dubious at best in a view of any regular consumer.

---

**kladkogex** (2019-08-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/bgits/48/3550_2.png) bgits:

> If the economic value of the DUBER is a discount on rides why then is a DUBER minted for the driver, what value would the driver have from a discount on rides?

I think the driver can simply sell the tokens on the market.

![](https://ethresear.ch/user_avatar/ethresear.ch/bgits/48/3550_2.png) bgits:

> Have you considered using the same minting approach without discounting and having the platform fee (normally the 20% of the drivers fee going to Uber) go to a pool?

I am generally not in favor of the platform fees because then DUber will lose its attractiveness against Uber, which is its feeless nature …

---

**PaulRBerg** (2019-08-07):

We definitely need more ideas for bridging fiat money with dapps, while also preserving decentralisation, however I have a few concerns around the model described here.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Lets take an example of a decentralized Uber (DUber). A DUber based on ETH will fail with today consumers, since majority of them do not have ETH tokens.

I argue that Uber, or taxi apps in particular, are a hard beast to tame due to their offline nature. One of the important roles that Uber plays is that of a scapegoat. Governments, taxi alliances and drivers need to have someone to complain to, hence every so often we see clickbaity titles like [Uber Settles Driver’s Lawsuit for $20 Million](https://www.nytimes.com/2019/03/12/technology/uber-drivers-lawsuit-settle.html).

Even more so, if the said dapp gets any significant traction, it’s likely that the common web2 distribution channels like the App Store would outright ban the listing of DUber - or even proceed to ban any intermediary web3 wallet that allows access to it.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> you mint two tokens on every transaction, awarding one token to the driver and one to the passenger.

This seems to add unnecessary overhead to something as basic as getting a ride. Yes, the tokens could be associated with airline reward points, but in the latter we’re talking big money. If I spend $1000 to get around the globe in a day, sure thing, I’d love to stack some points so I get my 5th trip for free.

Not the same thing can be said about DUber though. The mental overhead of dealing with some token that gets me a little discount may not be worth it.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Once DUBER tokens establish market fiat value, passengers will be able to pay per trip directly in DUBER tokens.

Does this scale from an ecosystem-wide perspective? Users may not fancy dealing with DUber, DLyft, DAirbnb etc.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> The advantage of the model is that it enables a smooth over-many-years transition from fiat to crypto.

Ultimately, token-less models may be easier to handle in the long-term. [The Gas Station Network, which launched a few days ago](https://twitter.com/ramonrecuero/status/1158738112505237504) seems to be a good solution for dapp onboarding.

