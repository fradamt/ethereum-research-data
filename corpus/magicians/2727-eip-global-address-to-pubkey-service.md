---
source: magicians
topic_id: 2727
title: "EIP: Global address to pubkey service"
author: Ethernian
date: "2019-02-22"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-global-address-to-pubkey-service/2727
views: 920
likes: 6
posts_count: 10
---

# EIP: Global address to pubkey service

Forked from [GraphQL interface to Ethereum node data - #9 by Arachnid](https://ethereum-magicians.org/t/graphql-interface-to-ethereum-node-data/2710/9) :

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png)[GraphQL interface to Ethereum node data](https://ethereum-magicians.org/t/graphql-interface-to-ethereum-node-data/2710/4)

> RFE: I would like to have an ability to get a public key for address (without intermediary explicit tx lookup and ecrecover call).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png)[GraphQL interface to Ethereum node data](https://ethereum-magicians.org/t/graphql-interface-to-ethereum-node-data/2710/7)

> Sure, that’s possible, but:
>
>
> It would require new index datastructures on disk.
> It wouldn’t work for transactions sent before the node was fast-synced without changes to the fast-sync protocol.
> It wouldn’t work for light nodes without changes to the LES protocol.

I need to know a public key for address to send a encrypted message to recipient. Currently I need to communicate in advance with the recipient to get a pubkey for address. For some use cases like “Stealth transactions”  it is discouraged.

As stated before by [@Arachnid](/u/arachnid), default implementation `address`=> `pubkey` by clients is not easy.

A simple workaround suitable for many cases could be a trivial contract with a mapping inside deployed at well known address.

Is there such contract `address`=> `pubkey` already deployed?

If not: may be we should do it?

## Replies

**Amxx** (2019-02-28):

We had the same discussion in our project and were considering writing such contract.

---

**Ethernian** (2019-03-02):

Great!

Please publish it before use to collect public feedback. May be there are more hidden UseCases.

I would glad to see it as a public service.

---

**Amxx** (2019-03-02):

Our approach is pretty simple for now [Code is here](https://hackmd.io/a6nXxkUdREOerTBKa2J-wg#)

If you have any better idea, I’ll be happy to discuss that… I’ll be at the hackathon in paris next week, maybe this could be a good project

---

**Ethernian** (2019-03-02):

Yeah! Thank you!

One objection for public discussion:

- I would let only account owner create/update their own records.

**Reason**: preventing unexpected hostile deletion/alternation of entries.

It will simplify the contract greatly because the setter logic can be implemented in the default function and getter can be default public accessor.

---

**Ethernian** (2019-03-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ssh/48/1648_2.png) ssh:

> would let me add accounts of mine which don’t have any eth

valid argument. Anyway it could be done in fallback function with pubkey as payload.

---

**Ethernian** (2019-03-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> I’ll be at the hackathon in paris next week, maybe this could be a good project

I’ll be both at Council and at hackathon. Would you have a talk before hackathon (at Council)?

---

**Amxx** (2019-03-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ssh/48/1648_2.png) ssh:

> would let me add accounts of mine which don’t have any eth.

That was exactly my idea. I beleive at some point most wallets won’t hold any assets (ether/tokens) and will only be used to sign orders that will be relayed (meta transaction) to multisig identity smart contracts. Therefore I think anyone capable of paying a transaction should be able to register a public key for another account (provided it’s done right → computing the address from the key)

In my opinion, the next step is to allow identity contracts’ owners to setup a key for their contract … which could be done in a number of (bad) ways … we have to find the right one !

---

**Ethernian** (2019-03-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> would let me add accounts of mine which don’t have any eth.

There is another aspect:

Is someone publish his public key, he commits himself to listen and receive encrypted messages.

Is someone commits my public key, I am not aware of it and thus I will not check it for messages sent to me.

The question is: is sending a encrypted message to address essentially the same use case as sending the payment (which requires no pre-confirmation from owner)?

---

**Amxx** (2019-03-02):

I guess that is one way of seeing it.

My stance on that was more like “if this account ever participated in a procole that require you to send an encrypted message to it, here is the public key, but that doesn’t imply the account owner will actively be looking for any message”

