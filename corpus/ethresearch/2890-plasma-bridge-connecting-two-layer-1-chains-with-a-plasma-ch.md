---
source: ethresearch
topic_id: 2890
title: Plasma Bridge -- connecting two Layer-1 chains with a plasma chain
author: akomba
date: "2018-08-11"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-bridge-connecting-two-layer-1-chains-with-a-plasma-chain/2890
views: 3390
likes: 2
posts_count: 3
---

# Plasma Bridge -- connecting two Layer-1 chains with a plasma chain

# Plasma Bridge

## Connecting Two Layer 1 Blockchains With a Plasma Chain

While working on the [Peace Relay](https://twitter.com/akombalabs/status/1008241906109710337?s=19) project, we came up with the idea of developing a plasma chain that could be attached to more than one public chain. For example we can deploy a plasma chain that is connected to both Ethereum and Ethereum Classic.

### What Is Plasma?

[Plasma](http://www.learnplasma.org/) is not a specific implementation. Rather,  *it*  is a  *set of guidelines*  or a  *protocol*  that makes it possible to deploy a layer 2 chain that is connected to a layer 1 chain.

Plasma is commonly used as an application specific sidechain. Its main purpose is to provide scalability for that application.

### Why Connect Two Layer 1 Chains?

Interoperability between chains is good for the ecosystem. The ability to move value between chains is useful and desired by the users. Among other things, it provides liquidity and interoperability.

### Why Use Plasma For Connecting The Chains?

There are several interoperability solutions (“meta chains”) in development. Many of these requires the user to trust the provider of the service. Others try to implement their own trustless protocols.

Plasma’s major benefit is that it provides a very secure solution to move assets between the layer 1 chain and the plasma chain. It deals with and provides solution for the security and accountability issues. It is as trustless as required.

In essence, plasma solves the problem of connecting two layer 1 chains. Using it for cross-chain transactions seems to be a good fit.

### Implementation

In a normal plasma chain, there is a smart contract deployed on Ethereum. This contract is used to move funds in and out of the plasma chain. This contract is the “owner” of the plasma chain.

#### Example: Moving Funds In and Out

Alice can send 1 ETH to the plasma contract on the main net. This ETH gets locked in the contract, and a corresponding ETHX gets created on the plasma chain. Now this ETHX can be moved in the plasma chain, much faster and cheaper than on the main net.

Alice can send the ETHX to Bob. Bob then can decide to redeem the ETHX. During the withdrawal process the ETHX will be destroyed, and the original ETH will be released to Bob on the main net.

#### Using Two Chains

The proposed implementation uses the exact same mechanism, but it will connect the same plasma chain to two main chains. Let’s use Ethereum and Ethereum Classic as an example.

An anchor contract will be deployed on both chains. Through ethereum, Alice can move ETH into the plasma chain as ETHX. On the other side, Bob moves his ETC in as ETCX.

In the plasma chain  **both ETHX and ETCX are native tokens** . They can be transferred to any address within the plasma chain. Atomic swaps can be easily performed.

#### Withdrawing from a Meta Plasma Chain

ETHX can only be withdrawn to Etherum, and ETCX can only be withdrawn to Ethereum Classic.

### When One Of The Chains Goes Down

The Plasma Chain should be able to operate while – for example – Ethereum Classic is down. In that case ETCX withdrawals would not be possible, but potentially the ETCX already in Plasma should still be transferable.

We say “potentially” because we have yet to build a complete model for this scenario. It is not out of the question that the plasma chain will have to record its state with all layer 1 networks.

In that case validators will refuse any transactions that touches the asset of the “down” chain.

### More Than Two Chains?

If we can implement the idea for two layer 1 chains, then it is possible to implement it for N chains. It is not known at this time whether this is feasible, or even desirable.

### What’s Next?

At Akomba Labs, we’re working on a proof-of-concept implementation that we hope to present at Devcon4 in Prague. Stay tuned!

*Thank you for*  [Virgil Griffith](https://medium.com/@virgilgr) *,*  [Dave Appleton](https://medium.com/@Dave_Appleton) *,*  [Ying Tong Lai](https://medium.com/@yingtong_905)  *and*  [Chip Wilcox](https://medium.com/@audioclectic)  *for the help.*

*Andras Kristof*

(Article on medium: https://medium.com/akomba/plasma-bridge-48122c554e38)

## Replies

**loiluu** (2018-08-11):

Very nice to see that you guys are working on this idea. We have thought about this idea before, but not sure how to cleanly implement it in practice. A few concerns, not sure if you have thought about them.

1. Would the validator have to deposit on both ETH and ETC? If so, how much is the deposit for each chain? The capital requirement would then increase if we increase the number of chains.
2. Should we have separate validators each representing a corresponding root chain? If not, the cost to commit the plasma chain increases linearly to the number of root chains. If so, how do the validators communicate and run the Plasma chain?
3. If the validator is malicious towards ETC users only, how does that affect ETHX users?

Happy to discuss these questions here.

---

**akomba** (2018-08-11):

Hi [@loiluu](/u/loiluu). Thanks for your encouraging words ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) Some of the questions that you raised can’t be answered yet – I’ll address the rest below:

> Would the validator have to deposit on both ETH and ETC?

Unlikely. The validator will have to commit to one of the chains, and deposit one token to the respective smart contract. This is a common pattern in the design (so that a validator or other actor will have to interact with only one of the L1 chains). This is to keep the architecture simple. We do recognize that it can create some unique situations. We will deal with those in the specs that we are writing now.

> Should we have separate validators each representing a corresponding root chain?

We believe we can get away with only one kind of validator. How exactly it will work is yet to be determined. Some of the earlier designs required that a validator could only validate a transaction if it has stakes for the token that is being transacted. However, this can get complicated really quickly, and we would like to keep it simple.

Long story short, we believe that it is possible to have only one kind of validator, regardless of the number of L1 chains.

> If the validator is malicious towards ETC users only, how does that affect ETHX users?

It shouldn’t affect ETHX users. It shouldn’t affect ETHX users even if the ETC L1 chain becomes unreachable. It is even possible that in that case the plasma chain can keep the ETCX tokens transferable. (Albeit unlikely).

I will share the more detailed paper as soon as I am done with it. Please let me know if you would like to collaborate on this – it would be awesome ![:sunny:](https://ethresear.ch/images/emoji/facebook_messenger/sunny.png?v=12)

