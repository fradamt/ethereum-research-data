---
source: ethresearch
topic_id: 18760
title: "RFC: Fixing Ethereum UX with user-centric asset model & ERC versioning"
author: peersky
date: "2024-02-22"
category: Applications
tags: [account-abstraction]
url: https://ethresear.ch/t/rfc-fixing-ethereum-ux-with-user-centric-asset-model-erc-versioning/18760
views: 1553
likes: 1
posts_count: 3
---

# RFC: Fixing Ethereum UX with user-centric asset model & ERC versioning

### Abstract

Taking a look back on 90s and beyond to pull a parallels between current state of Ethereum and bare-metal programming in Assembly and C back in a day, as well as today in embedded world.

The goal of this is to take the learnings and solve some problems we are seeing in Application layer security, such as highly complex vulnerability management procedures, difficulties to pre-arrange effective emergency response automations, and not least - very high level of stagnation caused by ERC standards track which just doest not allows easily to keep dApps and contracts with the progress we need there.

Referring to the fact that Ethereum Virtual Machine its still only a Machine, Im trying to reason that in traditional programming and computer architecture many security issues of what we see today on application-layer on Ethereum smart contracts are effectively solved and we can learn from there “how”.

My analogy is based on following illustration:

> Think of an IoT enabled house. If there is an asset behind the door, which is controlled trough WiFi by chip in a computer, and we can declare, that the one who is able to open the doors is owning an asset. If we also understood section above that any peripheral is just an interface that can be accessed by calling right address on address bus, then we can map this equation out to the fact that from CPU standpoint, an asset ownership is equal to ability to set or unset a byte in some registry on some address of IO bus.

Based on this I’m making conclusions that

a) Assets are not interfaces

b) Secure architecture requires split between asset storage and asset driving interfaces

c) Current asset model is not user centric and is causing not just stagnation and poor ux, but also centralisation risks

d) The model of EVM seems correct for me, it can be competitive with what Move has to offer, but it must build a wrapper to abstract us away from “bare-evm-programming”.

e) ERC versioning is something we need to consider

## Full article

https://peersky.xyz/blog/fixing-ethereum-ux/

## RFC

This is request for comments. Im am looking for community feedback to incorporate this further.

## Replies

**Zergity** (2024-02-23):

Great analysis and analogy.

I have a similar thought for a while: [[RFC] Contract-Led Storage-Rent Roadmap](https://ethresear.ch/t/rfc-contract-led-storage-rent-roadmap/18642)

Your idea of “Asset Storage” fit right into my “Storage Manager” model, I would call it “Storage Abstraction” after this.

[![image](https://ethresear.ch/uploads/default/optimized/2X/b/bb9256010a5e92848d746e43d5fd041ff5335ede_2_690x172.png)image2577×644 159 KB](https://ethresear.ch/uploads/default/bb9256010a5e92848d746e43d5fd041ff5335ede)

In Storage Abstraction, data/asset logic and permission can be designed and managed by Storage/Asset Dev. (E.g. an asset with move semantic is possible and useful for a lot of token contract).

Applications don’t have to worry about Storage Abstraction implementation, they just have to pick and use the best one for their logic.

---

**peersky** (2024-03-03):

Indeed interesting. The similarity is that there is need for memory storage that is (i) dedicated on user owned domain (ii) deterministically linked to one unique application that has access to mutate it.

I would like to point out that in my research puts user is in the center of owning memory access, giving user ultimate custody over asset belonging to one. That implies another requirement (iii) user able to issue and revoke permit to mutate such asset.

In order to implement (iii) the call to an asset *must* be routed trough user-centric access layer. On other hand it creates application-centric risks that must be mitigated in (ii), one way to mitigate that would be to ensure that user-centric access layer is known to be secure and supported system by the application.

I could see way to implement this as follows:

- Factory: Issues Smart wallets that act as user-centric access layer that has direct-memory access functionality
- Wallet: Deployed by factory it is limited in ability to upgrade/mutate own logic and can be hence trusted by apps which can trust the Factory.
- App: Can implement asset/abstract storage on wallets that are listed on trusted factories.

