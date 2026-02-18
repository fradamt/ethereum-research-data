---
source: ethresearch
topic_id: 19593
title: Derivatives Market for Implementing Based Sequencing
author: 0xTariz
date: "2024-05-20"
category: Economics
tags: [preconfirmations, based-sequencing]
url: https://ethresear.ch/t/derivatives-market-for-implementing-based-sequencing/19593
views: 4681
likes: 18
posts_count: 7
---

# Derivatives Market for Implementing Based Sequencing

Authors: [Tariz](https://x.com/Hyunxukee) ([Radius](https://x.com/radius_xyz))

[![8qmb0g](https://ethresear.ch/uploads/default/optimized/3X/1/0/1082a792a892a3e09ad171507d684219426b59dc_2_690x388.jpeg)8qmb0g700×394 69.6 KB](https://ethresear.ch/uploads/default/1082a792a892a3e09ad171507d684219426b59dc)

*Special thanks to [Nathan](https://x.com/NathanYJLee) from [Factomind](https://x.com/factomind) for his valuable advice on the design of the derivatives market.*

# TL;DR

This article introduces a derivatives market designed to implement based sequencing for fast finality in rollups. The proposed market aims to align incentives between Ethereum and rollups, mitigate operational risks associated with rollups, and promote voluntary participation and fair competition among rollups, proposers, and builders.

The unique design allows rollups to act as preconf providers, offering users fast preconfirmation while minimizing censorship, sandwich attacks, and frontrunning risks.

> For the full proposal, please refer to the complete blog post. This summary covers only the key design aspects.

# Motivation

If rollups, acting as preconf providers, pay proposers to pre-purchase the block building rights for specific slots, they can deterministically promise settlement to users by owning the Ethereum block. This mechanism allows rollups to achieve fast preconfirmation through self-sequencing. However, the difficulty in predicting future block prices introduces operational risks for rollups. To offset these operational risks and create a fair market that encourages active participation from traders, I propose a series of derivatives.

> This idea is connected to the implementation of delegated preconf mentioned in @JustinDrake based preconfirmation.

# Forward Contract

The process of a rollup purchasing the block building rights for a specific slot from a proposer can be likened to a forward contract in financial markets. To understand the operational risks a rollup might face in this transaction, let’s consider a basic scenario involving a 32-slot lookahead for the proposer and a slot auction.

1. At t = 1, the rollup participates in a slot auction to purchase a forward contract with the proposer for a specific slot.
2. From t = 2 onwards, after securing the slot, the rollup sequences its users’ transactions, providing preconfirmation to users and generating revenue from the block.
3. At t = 3, the rollup requests the execution of the forward contract, compressing its transactions into an Ethereum block and submitting them to the proposer.
4. At t = 4, the proposer fulfills the contract by signing the received block and proposing it on Ethereum.

**Operational Risks for Rollups**

1. Excessive Payment Risk: Rollups may find it challenging to accurately predict block value, leading to overpayment for block space. This occurs because they have to participate in slot auctions and purchase the entire space even if they only need a portion for settlement.
2. Revenue Uncertainty: Rollups cannot reliably predict their future revenue. If transaction costs exceed revenue, they may face potential financial risks.
3. Increased Labor Costs: To ensure stable operations, rollups must now engage in activities such as predicting Ethereum block values, competing with builders, and accurately forecasting revenues, which were previously unnecessary.

# Derivative Market

To mitigate the operational risks faced by rollups, we propose a derivatives market involving specialized participants, builders. This market includes two key derivatives: a forward contract between the builder and the proposer, and a swap contract between the rollup and the builder.

1. At t = 1, the builder participates in a slot auction and enters into a forward contract with the proposer for the block building right.
2. At t = 2, the rollup and the builder enter into a swap contract. This contract obligates the builder to include the rollup’s transactions in the block.
3. At t = 3, utilizing the block building right secured through the swap contract, the builder constructs the rollup block up until t = 4, thereby generating revenue.
4. At t = 4, the rollup demands contract fulfillment according to the obligations stipulated in the swap contract:

The rollup requires the builder to include its transactions in the Ethereum block secured through the forward contract.
5. To maximize revenue, the builder places the rollup’s transactions at the bottom of the Ethereum block and its own transactions at the top, forming a complete block.
6. At t = 5, the builder delivers the Ethereum block to the proposer, who then proposes it on Ethereum, fulfilling the forward contract.

**Motivation for Participation**

- Rollup: Rollups participate to provide deterministic preconfirmation to users regarding their inclusion in Ethereum, while mitigating the operational risks associated with purchasing block space. Preconfirmed transactions are guaranteed inclusion in the Ethereum block, avoiding the risk of spending more than their revenue on block space. This eliminates the need for unnecessary labor in price prediction and auction participation.
- Builder: Builders participate to reduce the risk of overpayment from slot auctions. The secured Ethereum block space, along with the rollup block, offers dual revenue streams, diversifying and reducing the risk of loss.
- Proposer: Proposers participate to receive compensation for rollup preconfirmation. Builders consider the revenue generated from rollup blocks when bidding in slot auctions, aligning proposer incentives with rollup settlement.

# Additional Design

To effectively implement these financial products, it is crucial to create an environment where all participants can compete fairly and engage actively. This involves three key additional design elements.

**Conditional Swap Contract**

Rollups may be hesitant to participate if they are required to allocate all potential revenue opportunities to builders through a swap contract. To encourage rollup participation, a conditional swap contract is proposed.

In this arrangement, if the builder generates profits from the rollup’s block building that exceed the fixed costs paid in the forward contract with the proposer, the rollup is allowed to stop providing the remaining block space to the builder. The rollup can then use the remaining block space to either build independently or auction it to builders for additional revenue.

This approach preserves the builder’s incentive to participate while protecting the rollup’s opportunity to generate revenue.

**Competitive Proposer Market**

Settlement is essential for rollups to inherit Ethereum’s security. When rollups are compelled to purchase blocks, proposers/builders gain significant pricing power, potentially leading to an uneven playing field that undermines market fairness and efficiency.

To reduce the pricing power of any single builder, multiple builders should be encouraged to participate in swap transactions, fostering competition among them. This requires expanding the forward contract market to include multiple proposers with block building rights for different slots.

Such a structure ensures that the variable value of the rollup’s block aligns more closely with the fixed cost of acquiring Ethereum block space. This is analogous to achieving a ‘par value’ of zero for swap contracts in a competitive market, maintaining reasonable costs for rollups. The lookahead necessary to achieve this par value requires further discussion.

**Syndicated Rollup Strategy: Derivatives for All Rollups**

Builders may be unwilling to engage with rollups that have relatively low block value, potentially marginalizing app-specific rollups in the market.

The Syndicated Rollup Strategy groups multiple rollups into a syndicate, enhancing their market participation. Cross-rollup arbitrage has the potential to increase the value of each block. Builders receive the block building rights for the rollups in the group, and the rollups require the builder to include all group transactions in the Ethereum block.

# Building Blocks in Rollups

This section describes how builders secure rollup block building rights through swap contracts, focusing on censorship resistance and fast preconfirmation for user-centric rollups.

**Censorship Resistance**

In a structure similar to Proposer-Builder Separation (PBS), rollups that enter into swap contracts receive blocks from builders and execute them. However, this setup may expose users to censorship, sandwich attacks, and frontrunning by builders. Rollups can address these issues by integrating Radius’s [sequencing engine](https://docs.theradius.xyz/testnet/curie-testnet/encrypted-mempool).

- Encrypted Mempool (using delay encryption): Users’ transactions are encrypted until the promise of inclusion in the rollup block is issued.
- Decryption and Execution: Once inclusion is confirmed, transactions are decrypted and executed by the rollup, providing preconfirmation similar to standard transactions.
- Economic Order Guarantees: By assigning an order to the inclusion promises, the economic guarantees ensure that transactions cannot be reordered after decryption, minimizing the risk of frontrunning and sandwich attacks.

**Fast Preconfirmation**

Rollups can achieve fast preconfirmation by designating the preconf provider as their sequencer and implementing self-sequencing. Block space is divided into two segments: Top-of-Block (ToB) and Bottom-of-Block (BoB).

[![스크린샷 2024-05-07 오후 12.44.26](https://ethresear.ch/uploads/default/optimized/3X/d/2/d23430465b0f7160e93904427eba688aef1fff2f_2_690x366.png)스크린샷 2024-05-07 오후 12.44.261262×670 37.9 KB](https://ethresear.ch/uploads/default/d23430465b0f7160e93904427eba688aef1fff2f)

- Top-of-Block (ToB): This space is allocated to the builder under the swap contract. The builder creates a backrunning bundle based on the rollup’s previous block state and submits it to the rollup’s sequencer.
- Bottom-of-Block (BoB): This space is reserved for end-user transactions. The rollup sequences these transactions and provides preconfirmation.
 Using Radius’s sequencing engine in BoB protects users’ transactions from censorship by the sequencer and harmful MEV by the builder, as the builder cannot see the user’s transactions when creating the ToB.

**Syndicated Rollup Strategy**

In a syndicated rollup strategy, a group of rollups entering into swap contracts with a builder allocates ToB space to the builder. The builder submits a cross-rollup bundle to be included in the ToB.

[![스크린샷 2024-05-10 오전 11.09.13 (1)](https://ethresear.ch/uploads/default/optimized/3X/c/4/c4dcc9cf943b6b8894cbabc1360b8aa91e92b141_2_690x432.png)스크린샷 2024-05-10 오전 11.09.13 (1)894×561 83.1 KB](https://ethresear.ch/uploads/default/c4dcc9cf943b6b8894cbabc1360b8aa91e92b141)

A [Shared Sequencing Engine](https://docs.theradius.xyz/testnet/portico-testnet/multi-rollup-sequencing) aims to ensures smooth contract execution between rollups and builders. It will verifies that the builder submitting the bundle is a party to the swap contract and is designed to ensure that all rollups in the group fulfill the contract by including the builder’s submitted bundles in ToB.

Rollups can choose the shared sequencing engine for BoB sequencing. This allows the selected sequencer to act as a shared preconf provider, supporting atomic inclusion for end-users across multiple rollups.

# Conclusion

I am enthusiastic about the future of a rollup-centric Ethereum and am dedicated to exploring designs that benefit rollup users. A derivatives market that incentivizes voluntary participation of Ethereum for rollup settlements can significantly contribute to the effective implementation of based sequencing. My future research related to the derivatives market includes the following areas:

- Exploring the technical requirements necessary for market implementation.
- Updating the design to accommodate rollups utilizing blobspace.
- Proposing additional designs that can contribute to Ethereum’s decentralization, potentially considering the separation of beacon proposers and execution proposers as suggested in @mikeneuder Execution Ticket and @barnabe APS-Burn.

Beyond the derivatives market, I am exploring various methods for implementing based sequencing. I look forward to contributing to this field through diverse feedback and collaboration within the community.

## Replies

**yusufxzy** (2024-05-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/0xtariz/48/16327_2.png) 0xTariz:

> auction

Very interesting! Curious to know more about the nature of the auction design. Is it an English auction or a type of sealed bid auction?

I assume ToB and BoB will have two separate auctions?

How would the cost of encryption/decryption of user transactions be managed? Would it be offloaded to any participant? Or are these costs low enough not to be a concern?

---

**dpl0a** (2024-05-20):

Well, this is exactly what manifold and 20squares have been doing since the end of last year.

(Can’t include links yet, replace the "dot"s below)

- blog dot 20squares dot xyz/mev-io-initial-announcement/
- forums dot manifoldfinance dot com/t/mev-protocol-update-nov-30-2023/532
- forums dot manifoldfinance dot com/t/mev-evolution-manifold-finance-introduces-xga-after-dissolution-of-meveth-collaboration/560

We already have built an L2 that handles this and we’re live on mainnet.

---

**0xTariz** (2024-05-22):

Thank you for your question ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

The method of auction requires further discussion. I am considering both options—each will be chosen according to the purpose of the auction. For example, the builder’s slot auction is about obtaining block building rights from the proposer, and since it’s not a block auction (because the revenue a builder can generate from the block is not clear), an English Auction might create too much competition.

ToB and BoB will indeed be conducted separately.

Encryption is performed by the user, while decryption is handled by the sequencer. There are two options for the encryption method: SKDE and PVDE.

The cost for encryption and decryption with SKDE is not a concern as it is sufficiently low. PVDE, on the other hand, might incur some costs as it requires users to generate a zkp related to encryption, but it offers trustlessness in return. The cost for decryption is minimized by distributing the load.

Fees for decryption operations are passed on to the sequencer through transaction fees or rewards.

---

**0xTariz** (2024-05-22):

That’s very interesting! I’ll take a look as well ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

Could you please let me know if there are any major differences?

---

**FabrizioRomanoGenove** (2024-05-23):

Yes, our system is a bit simpler. The reason for this is that we wanted to assess one problem at the time.

In your model, you seem to be much more focused on the rollup side of things. In our design, there are three actors involved:

1. A proposer, which wants to sell part of the block beforehand as a forward contract;
2. A ToB builder, as in ‘someone taking part to usual mev-auctions today’;
3. A BoB builder, as in 'someone willing to reserve blockspace beforehand, be it an intent provider, a rollup willing to reserve blockspace for preconfs or whatnot;
4. A relay, which is no more no less than what it is today in mev-boost land.

We designed our system with the purpose of staying compatible with mev-boost. The reason for this is that the whole mev landscape is **highly** political and pushing any change to the current status quo will encounter a high adoption barrier. So we tried to change as little as possible and to upset as few actors as possible.

In our model, a validator that decides to use the mechanism will listen to a particular relay **exclusively**[^1]. This relay does two things:

- It auctions away the ToB blockspace, atm fixed at 25M gas max, as in traditional mev-boost.
- It fills the last 5M (BoB) as futures.
The relay has some unbundling/merging logic to be able to merge the ToB and BoB; From the PoV of the proposer, nothing changes: Besides the exclusivity requirement as above, proposer will just run mev-boost and won’t have to change a thing.

The BoB is auctioned away on a dedicated L2. Every time a validator using the mechanism gets elected as proposer, we’ll know up to 2 epochs in advance. This means that we can open up an auction for the BoB blockspace up to 64 slots in advance. This auction is run via a dedicated smart contract, and quite literally tokenizes BoB: At each auction, 50 tokens representing 100k gas for a given slot are sold.

The reason for this is that we want the forward contracts to be tradable. Buyers can:

- Use the forward contract by burning the tokens and submitting their bundles, which need to use an amount of gas that is less than 100k*number of tokens burned.
- Transferring the tokens to someone else.

The dedicated relay receives the BoB bundles, verifies that requirements are met (e.g. that gas doesn’t exceed the allowed maximum), and merges them with the ToB. The merging logic is not super easy as we need to check for a few things such as potentially duplicated transactions.

For what I can see, this system just implements the forward contract logic whereas you’re also taking care of what’s happening at the interface between a rollup willing to buy block space and the block space provider, which if I understand correctly you call builder. In this respect, I think there may be avenues of collaboration between what we’re doing and what you propose.

[^1]: This is a HUGE limitation and we’re aware of that. We have already a solution to make our system relay agnostic, and we’re working hard to implement it. I hope I’ll be able to say more about it sooner than later!

---

**meridian** (2024-06-12):

Thanks [@FabrizioRomanoGenove](/u/fabrizioromanogenove) for this reply

