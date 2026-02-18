---
source: ethresearch
topic_id: 10507
title: Cross-rollup NFT wrapper and migration ideas
author: vbuterin
date: "2021-09-06"
category: Sharding
tags: []
url: https://ethresear.ch/t/cross-rollup-nft-wrapper-and-migration-ideas/10507
views: 73108
likes: 101
posts_count: 60
---

# Cross-rollup NFT wrapper and migration ideas

The NFT ecosystem is growing rapidly, and it’s a significant part of the Ethereum chain’s gas consumption. The youth and relative lack of entrenchment of the ecosystem, as well as the greater need to avoid high fees due to the non-financial nature of a large part of the NFT sector, makes it a prime target for moving to layer 2. However, this opens the question of *how* a move to layer 2 could happen.

One simple proposal is to socially coordinate a move to a single rollup platform (eg. Arbitrum, as it’s available for general contract deployment today), but this has some important downsides:

- All existing major EVM-capable rollup platforms have backdoors, centralized sequencing or other training wheels, and it’s risky to commit an entire ecosystem to a single rollup while there is uncertainty about how the rollup will graduate beyond such features
- The NFT ecosystem may well grow too big for one single rollup to handle safely
- No part of the NFT ecosystem, or even the entire NFT ecosystem, is a closed-off world; they will need to interoperate with other parts of the Ethereum ecosystem

This document is a proposal for how to make NFTs cross-rollup friendly, allowing NFTs to move to the entire *layer 2 ecosystem*.

## Proposed solution 1

NFTs would begin by being registered in one rollup (or the base chain). An NFT could hop between other rollups (or the base chain) by creating a **wrapper NFT**.

The process for wrapping is as follows:

1. On rollup A, send the NFT (we’ll call it X) to a wrapper manager contract, specifying (i) a destination rollup and (ii) an initial owner. The lockbox contract saves a record in storage, assigning X a new serial number R, and saving the destination rollup (we’ll call it B) and the initial owner on the destination rollup (we’ll call this account O1)
2. On rollup B, anyone can create a wrapper NFT using the wrapper manager contract on rollup B. Creating a wrapper NFT requires specifying the source rollup and the serial number. Creating a “valid” wrapper NFT of X can only be done by the specified owner and by claiming (R, A) as the serial number and source rollup. Note that it is possible to create an invalid wrapper NFT that points to nothing; rollup B does not know what is valid and invalid. The wrapper manager contract stores (serial number, source rollup, initial owner) tuples and prevents multiple NFTs from being created with the same tuple.
3. To withdraw the NFT from the lockbox, the current owner of wrapped-X on rollup B must send it back to the wrapper manager, which issues a receipt saying “the NFT with serial number R, source rollup A, and initial owner O1, was just unwrapped, with desired new owner O2”.
4. The lockbox contract can hand X to O2 when it receives a proof that such a receipt on rollup B was made, and checks the serial number, source rollup and initial owner against its own stored information and verifies that it passes.

[![nft_issuance_p1](https://ethresear.ch/uploads/default/optimized/2X/7/7df0890b9ded9693eb844824acbe79cc1b1fa7fc_2_673x500.png)nft_issuance_p1879×653 23 KB](https://ethresear.ch/uploads/default/7df0890b9ded9693eb844824acbe79cc1b1fa7fc)

[![nft_issuance_p2](https://ethresear.ch/uploads/default/optimized/2X/1/1ecba82eaec4515fe33e976e1087621a7ab76c58_2_673x416.png)nft_issuance_p2881×544 19.9 KB](https://ethresear.ch/uploads/default/1ecba82eaec4515fe33e976e1087621a7ab76c58)

Note that the withdrawal will have a time delay, because a time delay of ~1 week is required for optimistic rollup state roots to finalize so that receipts can be verified. The only way to do multiple hops more quickly, so far, would be to do multiple layers of wrapping.

For a user to verify that a wrapped X is legitimate, they would need to verify the state on rollup B *and* the receipt on rollup A themselves.

## Extension: add cross-rollup transfers

On rollup B, the owner of wrapped-X can send it to the wrapper manager with an instruction to issue a different receipt: “the NFT with serial number R, source rollup A, and initial owner O1, was just moved to rollup C, with desired new owner O2”.

On rollup C, once again anyone can make a wrapped-X object by specifying the original source rollup (this is rollup A in this example), serial number and initial owner, and this wrapped-X on rollup C can be freely traded. However, once this happens, actually withdrawing X would now require publishing the entire chain of receipts (in this case just two) of cross-rollup transfers.

[![nft_extension_p1](https://ethresear.ch/uploads/default/optimized/2X/f/f8eeff44b6e125fdbd45ed335c8fe86855fa00c5_2_690x377.png)nft_extension_p11321×722 37.6 KB](https://ethresear.ch/uploads/default/f8eeff44b6e125fdbd45ed335c8fe86855fa00c5)

[![nft_extension_p2](https://ethresear.ch/uploads/default/optimized/2X/2/23f769ba8a54c7d9af1f97df9cc3c1f023ad187d_2_690x419.png)nft_extension_p21321×804 45.4 KB](https://ethresear.ch/uploads/default/23f769ba8a54c7d9af1f97df9cc3c1f023ad187d)

Note for the simplicity, “withdrawal” is no longer a cross-rollup operation; instead, withdrawal is done by doing a cross-rollup operation to create wrapped-X *on rollup A* (the same rollup as X), and then finally unwrapping X in a separate single-step operation.

What is effectively happening is that when the NFT is moved from rollup to rollup, the chain of transfers leaves behind a chain of receipts, and every single receipt in that chain of receipts is mirrored to rollup A and processed in order at some point in the future when the state roots on the other rollups finalize (this can be space-optimized in the short term via Kate commitments, and in the long term an entire chain of receipts can be proven via ZK-SNARKs).

For a user to verify that a wrapped X is genuine, they would need to verify the entire chain of receipts on all rollups reflecting the cross-rollup transfers (or at least, the chain of receipts since the last receipt that was already mirrored onto rollup A).

## Extension 2: gas-optimized issuing on base chain

All NFTs can be issued in such a way that they are “owned” by the lockbox contract on the Ethereum base chain. To make this gas-efficient, the lockbox contract would get the functionality to generate a whole set of serial numbers and transfer them to a rollup. Effectively, all NFTs are pre-created, but with no “meaning” yet assigned to any of them (think: there are 2**256 not-yet-differentiated “stem cell” NFTs), and they are transferred to rollups in batches.

The process of “issuance” now becomes a process of assigning meaning. This can be done simply by passing along a “meaning hash” through receipts in the same way that owners are passed through: if an NFT has no meaning (it’s a “stem cell”), the owner can assign a meaning to it, turning it into a “differentiated” NFT. The base chain only learns the meaning of an NFT once it verifies the chain of receipts up until the point where the meaning was assigned (realistically, receipt verification would have to be ZK-SNARKed to make this viable).

This allows all NFTs to be “rooted” in the base chain, instead of a rollup. This is useful to deal with the scenario where a rollup breaks or otherwise becomes non-viable, and applications need to permanently migrate to other domains.

**Reminder: ethresear.ch is a special-purpose scientific forum, and is not a general discussion venue for (especially non-technical) issues about crypto projects, *even if* those issues are important. Please stay on topic.**

## Replies

**zhew2013** (2021-09-06):

This is a very smart and timely post. The only issue I have with this is, as the price of NFT fluctuates wildly within days or even hours, I doubt there would hardly be anyone willing to put up with the ~1 week withdraw delay.

Is there any realistic way to have near instant withdraw (people can withdraw within minutes instead of days)? I think in 99% of all cases, people will just use one single layer 2, plus the Eth base layer. Is there a good design that can make NFT trading gas efficient within the context of one single rollup + Eth base layer? I am pretty sure cross-rollup transfer will be followed on once there is a good single rollup people are using.

Also I am pretty new to L2 stuff so if my question is obvious or my understanding is wrong, please forgive me. Would really appreciate your response, Vitalik [@vbuterin](/u/vbuterin) !

---

**vbuterin** (2021-09-06):

In the design in Extension 1, you could just make a wrapper of the NFT on rollup A instantly, and immediately put it up for auction. It would take a week until the receipt from rollup B propagates and the wrapper becomes withdrawable, but in the meantime anyone running the correct software would be able to automatically see that the wrapped NFT is valid and would be willing to buy it.

> Is there a good design that can make NFT trading gas efficient within the context of one single rollup + Eth base layer?

You could just take the design I describes verbatim, but put the base layer in place of one of the rollups. The gas costs would be higher, but users could just make a wrapper of the NFT in the rollup and generally trade it inside of there.

---

**zhew2013** (2021-09-06):

Thanks for the quick response [@vbuterin](/u/vbuterin) !

So in the case of issuing NFT in ETH base layer (I doubt how many people would issue NFT in rollups), there would be one time gas fee of transferring/wrapping ETH to/on roll up. And then trading is not expensive because it is on roll up. Is that correct?

To me it looks like how Uniswap uses Arbitrum. There is a one time fee on depositing/withdrawing in and out of L2, but then trading is cheap.

Please correct me if I am wrong. Thanks again [@vbuterin](/u/vbuterin) !

---

**vbuterin** (2021-09-07):

RIght. But why wouldn’t people issue NFTs on rollups? If it’s cheaper to do the creation step inside a rollup, surely you might as well just do it there. If that rollup ever becomes untrustworthy, then you just recognize the wrapper in a different rollup as being the real one.

---

**zhew2013** (2021-09-07):

Good point. I think the real issue is to get NFT issuer convinced to use rollups then. Onboarding them project by project. Maybe over time the herd will all come.

I am very interested in taking on this one. The remaining issue is if all this work will become useless once ETH 2.0 sharding is alive? People might just trade on eth base layer, or even after sharding the rollups solution will be significantly cheaper to trade NFTs?

Thanks [@vbuterin](/u/vbuterin) !

---

**vbuterin** (2021-09-07):

> The remaining issue is if all this work will become useless once ETH 2.0 sharding is alive?

It will not become useless for a long time. The current proposed implementation of sharding is just data sharding, meaning that you would not be able to have txs “directly” on the shards; rather, the shards would just be data space so that rollups could have much higher scalability.

---

**zhew2013** (2021-09-07):

Thanks [@vbuterin](/u/vbuterin) !!! ![:grinning:](https://ethresear.ch/images/emoji/facebook_messenger/grinning.png?v=9)

---

**vanhen** (2021-09-08):

Interesting thread. Many important trade offs to consider.

---

**7LVLS** (2021-09-08):

Vitalik, is it safe to say that what you have outlined here would be similar to the approach of the Cross-Chain Interoperability Protocol (CCIP) being developed by Chainlink Labs to tackle these problems?

---

**ChinmayPatel** (2021-09-08):

Why just rollups? The same “wrapper” can be used for multi-chain approach as well. Theoretically, an NFT specific parachain can connect with ETH for the exact same reason using the same framework.

---

**rjramesh** (2021-09-08):

What do you think about


      ![](https://ethresear.ch/uploads/default/original/3X/7/0/708f207bd240819d9fb354677a5152880b23d51e.png)

      [immutable.com](https://www.immutable.com/)



    ![](https://ethresear.ch/uploads/default/optimized/3X/4/e/4e2b77d042c50cc7371efc8f7f773b73da6edaa9_2_690x362.jpeg)

###



Maximize your game's growth, engagement, and revenue with Immutable's next generation infrastructure.










# THE FIRST LAYER 2 FOR NFTS ON ETHEREUM

Zero gas fees, instant trades and scalability for games, applications, marketplaces, without compromise.

---

**coinfreak** (2021-09-08):

So eth can’t handle defi, “let’s take that to l2”

Then eth can’t handle dog tokens. “They dont belong here”

Then “eth should be for the metaverse”, but wait. Eth can’t handle that either. “Time for nft’s to move to l2’s”

Defi didn’t move to l2’s. It moved to other l1’s

Shitcoins didn’t move to l2’s. They moved to other l1’s

Why would nft’s go to other l2’s? Noone likes the centralized l2’s. They are expensive and not convenient. Bsc is more convenient and less centralized than the l2’s and so is avax, sol, and the rest.

How about we increase the gas limit?

---

**driferia** (2021-09-08):

People like to actively trade and issue NFTs (much more so than ERC-20), and interactions with NFTs cost more gas. There is a huge incentive expand the market by issuing directly on L2 while fully preserving the security and data availability aspects of Ethereum, then wrapping L1 “legacy” NFTs into L2.

---

**vbuterin** (2021-09-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/chinmaypatel/48/7143_2.png) ChinmayPatel:

> Why just rollups? The same “wrapper” can be used for multi-chain approach as well. Theoretically, an NFT specific parachain can connect with ETH for the exact same reason using the same framework.

The difference between rollups and the multi chain world is that while a proof of rollup state can be 100% reliable, a bridge to another chain always has a risk of breaking in extreme scenarios: what if the bridge itself is unreliable, or there is a 51% attack and the community forks to recover but the bridge doesn’t capture that, etc etc. So you can absolutely do the same thing, but I do think that there will always be security uncertainties with multi-chain that don’t exist in a rollup ecosystem.

> l2’s? Noone likes the centralized l2’s

The centralized training wheels on the L2s are a temporary measure, because this is new tech with high risk of software bugs. All the L2s I know have a clear roadmap toward removing them.

---

**coinfreak** (2021-09-08):

You won’t get those 100k tps and instant finality with an arduino running from your home. Rollups will always be very expensive, inconvenient, easy-to-censor, datacenter chains. So yes, highly centralized

---

**Mintable** (2021-09-08):

[@vbuterin](/u/vbuterin) This seems nice to reduce gas costs, but for user experience its really taxing. NFTs are traditionally much more easier to grasp than something as complicated as DeFi and as such, more users using NFTs are brand new to blockchain and not experienced.

Asking a user to submit multiple transactions, to jump from one layer to rollup, and from one state to another will be much more complicated and confusing. Having a user try to verify an NFT is legit (say an official cryptokitty) when its on a L2 and was used on Rollup B and then on Rollup C - would be basically impossible for a newer user.

Having one marketplace on rollup B and one marketplace on rollup A and C would be another issue all together.

Depositing funds on a rollup would be a final issue - total gas costs to the user is probably higher in this situation (correct?) since they need to:

1. Deposit into rollup - mainnet gas costs
or 1a. deposit eth into rollup to make a purchase/transfer
2. Move the NFT from one rollup to another because wallet X only support Rollup A and not rollup B, or marketplace Y only uses Rollup C.
3. Move back on mainnet

Opposed to currently, where a user can just submit one transaction to buy an NFT on mainnet, effectively saving them money instead of using a layer 2.

So the problem here is:

1. Over-complication for a generalized user (not an experienced blockchain user)
2. Higher gas costs for the end user - which reduces their desire to actually use it opposed to mainnet
3. User experience where metamask only supports Rollup A, trust wallet only supports Rollup B and C, and rainbow supports all three. (or marketplaces, viewing dapps, rarity tools, etc). Fragmentation within the ecosystem basically.

Instead - I believe there should be one, dedicated NFT rollup, not rollup a b or c, but one dedicated NFT rollup on Ethereum. So that apps, marketplaces, wallets can know exactly which is the official and which has 99% of the NFTs on it.

I think we need to consider the withdrawal and deposit of funds and NFTs quite hard - because if I have to submit 1 transaction to deposit ETH, then trade an NFT and submit multiple free transactions, then submit a second transaction to withdrawal my ETH, I’m looking at paying more in gas costs in some scenarios - depending on however many of X transactions I submitted. If I submitted only 1 tx to buy a single NFT or sell, then I’m negative in terms of savings and have spent more.

These don’t even address the waiting period of a week for settlement, which is another issue all together and really not acceptable for an average user who just bought a $50 jpeg to be used in a game/redeemed for access to a page.

Thoughts?

---

**ChinmayPatel** (2021-09-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The difference between rollups and the multi chain world is that while a proof of rollup state can be 100% reliable, a bridge to another chain always has a risk of breaking in extreme scenarios: what if the bridge itself is unreliable, or there is a 51% attack and the community forks to recover but the bridge doesn’t capture that, etc etc. So you can absolutely do the same thing, but I do think that there will always be security uncertainties with multi-chain that don’t exist in a rollup ecosystem.

Agreed. The assumption was to have a reliable bridge.

---

**coinfreak** (2021-09-08):

Well said! NFT’s were all about onboarding new users

People seem happy (ok, not happy) to pay the fees, but this is far too complicated

---

**weijia31415** (2021-09-08):

There are challenges of crossNTF for L2 on crosschain security and decentralization. Recently, there has been a big increase in attacks on crosschain bridges.

Since a crosschain bridge is a holistic system that connects a source chain with a target chain, the attacks on the crosschain integrity can be on source chain, target chain, or the bridge connecting them.  The crosschain security has not been mentioned much and recent crosschain attacks have caught crypto communities attention.

To ensure the crosschain bridges are secure, besides securing source and target chain smart contracts, there should also be a shaking and slashing mechanism to safeguard crosschain assets.

Because the value of NFT are subjective and hard to define, the staking and slashing model might need to re-evaluated.

---

**sidhujag** (2021-09-08):

You can define your own data availability and consensus policies on L2, wallet/UX/usability can be improved but that is an iteration once the infrastructure is built out. For example a VRF based selection mechanism with a POS L2 rollup would allow for seperations of concerns where NFT’s can exist for certain applications (for example a sports theme’d NFT marketplace). Apply this idea to be able to jump across individual L2’s which wallet’s can adopt and likely it will cut down on L1 settlement times and skip L1 altogether for the most part.


*(39 more replies not shown)*
