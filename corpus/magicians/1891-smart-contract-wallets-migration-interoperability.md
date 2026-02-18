---
source: magicians
topic_id: 1891
title: Smart Contract Wallets 👉 Migration / Interoperability
author: c-o-l-o-r
date: "2018-11-13"
category: Web > Wallets
tags: [wallet, dx]
url: https://ethereum-magicians.org/t/smart-contract-wallets-migration-interoperability/1891
views: 1007
likes: 0
posts_count: 3
---

# Smart Contract Wallets 👉 Migration / Interoperability

I have been thinking a lot about what the future of wallets look like and how we streamline the on-boarding of new users and I’ve come up with a few thoughts. I would like to start a dialogue with everyone and see how others in the space see the future. I also feel like there is a lot of fragmented and duplicate work is going on right now and it would be great to consolidate our efforts a bit.

I believe smart contract wallets will eventually account for the majority of wallets in use. I think Universal Login is a great example of how we’ll use smart contract wallets in the future. I foresee smart contract wallets becoming what we know today as our bank account and it will be ubiquitous with storing money.

We’re a long way from that and I think there are a couple core issues that need to be overcome to reach this.

First off, on-boarding needs to be easy. It is unrealistic to get new users into dapps and expect them to signup for the dapp and a wallet at this time. The dapp should be able to create a contract wallet for their user and store an ephemeral key on their device. Once the user decides its time to upgrade to a real wallet, that contract should either be able to plug directly into a real wallet interface *or* it should be able to be migrated to a more fully featured contract like Gnosis Safe.

All wallet contracts should implement a core set of features. Every dapp on the planet should be able to interact with any smart contract wallet, regardless of what extra modules / feature are included. In this same vein, smart contract wallets should be mobile. If one day the wallet provider I use does something I don’t like, I should be able to pack up my contract and move everything over to a different provider with little friction. I imagine it like being able to move all your money / personal info / history from one bank to another at the press of a button.

In order to address the issues I’ve raised, it seems like there are two avenues we can take: migrations & interoperability. I’d argue we need both.

Interoperability (between dapps and wallet UIs) is the ideal route to take, because it doesn’t rely on issuing a new contract wallet. However, I think that if this is the only route we explore we will end up in a corner by ourselves with a bunch of modules. I believe that also setting a standard for migrating between contract wallets early will avoid this and allow development to continue and improve the experience without restrictions.

This was a bit of a brain dump, I look forward to hearing what some others in this space are thinking! Please direct me to any existing EIPs or discussions that may be relevant.

## Replies

**c-o-l-o-r** (2018-11-13):

Can you elaborate on the actor/asset model? And who is publishing this article?

---

**bumblefudge** (2025-02-20):

heh, did this get pulled out of another thread or something? I can’t see what Antoine Herzog post this is responding to ![:see_no_evil:](https://ethereum-magicians.org/images/emoji/twitter/see_no_evil.png?v=12)

