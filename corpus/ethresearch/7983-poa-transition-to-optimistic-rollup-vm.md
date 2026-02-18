---
source: ethresearch
topic_id: 7983
title: POA transition to optimistic rollup VM
author: barryWhiteHat
date: "2020-09-16"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/poa-transition-to-optimistic-rollup-vm/7983
views: 4825
likes: 13
posts_count: 9
---

# POA transition to optimistic rollup VM

## Intro

We have a desperate need to scale ethereum. The state of smart contract scaling is not as advanced as we would like it to be. As such a lot of projects are leaning towards deploying upon Proof of authority (POA) networks.

These (POA) networks do NOT provide censorship resistance, finality or security of the funds they hold. A super majority of the validators (Authority) can steal these funds, censor transactions or revert finality. However some projects are desperate to scale so these concessions in the short term make sense.

Virtual machine optimistic rollups is an optimistic rollup that contains a fraud proof for every EVM operation. They allow anyone to deploy any ethereum smart contract. So that any observer can proof a fraud and revert. These systems improve upon POA by providing much stronger guarantees.

Here we propose deploying a POA network as a short term solution which will transition to optimistic rollup in stages. We hope to find an Authority (multiple projects) that has high reputation for the short term and then once optimistic rollups are ready replace the authority with them.

## Phase 1: Setup

First we setup a POA chain with our high reputation projects. Each token that wants to use this chain deploys its own token bridge contract. This is registered on the POA side who treat balance made here as POA chain deposits.

## Phase 2: Optimistic rollups join

When optimistic rollups are ready to join they can update token bridges with their fraud proofs. This is opt in for the projects who now can choose when to use optimistic rollups.

Once we enter phase 2 an optimistic token bridge is not secure. A super majority of the Authority can still make data un-available and steal from the token bridges.

## Phase 3: Authorities are replaced with optimistic rollups

In this stage we replace some of the Authorities with optimistic rollups. This means that if an Authorities makes an illegal state transition its attestation can be undone.

If a super majority of Authorities migrate to optimistic rollup then we can roll back illegal state transitions.

## Phase 4: Decentralize transaction ordering

Finally we need to provide some decentralized way to order transactions. We can use something like [MEV Auction: Auctioning transaction ordering rights as a solution to Miner Extractable Value](https://ethresear.ch/t/mev-auction-auctioning-transaction-ordering-rights-as-a-solution-to-miner-extractable-value/6788/9) or [Spam resistant block creator selection via burn auction](https://ethresear.ch/t/spam-resistant-block-creator-selection-via-burn-auction/5851) where the burn is donated to ethereum public goods funding using quadratic funding or similar.

## Conclusion

One big advantage here is that we will have multiple optimistic rollups proving validity. So if one of them is broken the system is still secure. Its like an M of N multisig. M need to have a critical security bug before we are in trouble.

Having optimistic rollups build on the same chain makes sense to make tooling the same and help them learn and improve each others work. It removes the need for every token to be on the same optimistic rollup in order to benefit from network effect. So instead of having one optimistic rollup winner now we can have many.

## Clarification

To be clear this is not a recommendation that anyone deploy on proof of authority (or proof of stake) side chains. They are intrinsically flawed. If you have no option but to do this you should deploy on one that has a clear path and commitment towards adding fraud proofs.

If you deploy to a proof of authority network. You run the risk of the chain prevent your users from exiting with high fees when you try and upgrade to another solution. There is intrinsic locking here that is very concerning.  See [here](https://ethresear.ch/t/against-proof-of-stake-for-zk-op-rollup-leader-election/7698) fro more information.

## Replies

**igorbarinov** (2020-09-16):

> These (POA) networks do NOT provide censorship resistance, finality or security of the funds they hold.

Hi Barry,

Are you familiar with [Dunning–Kruger](https://en.wikipedia.org/wiki/Dunning%E2%80%93Kruger_effect) effect? It is a well-known effect in psychology when one’s lack of knowledge of how something works leads to overestimating abilities, in this case how to actually break stuff, censor stuff, or steal stuff. If it’s me who is under such effect please show how to implement any of those attacks on any POA networks widely used in prod and we will try to fix them by upgrading their protocols.

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> A super majority of the validators (Authority) can steal these funds, censor transactions or revert finality.

Do you mean `censor transactions`

or `censor transactions via censoring blocks of other validators`?

In the POA model, 100% of validators should agree on censoring transactions (which is [unanimity](https://english.stackexchange.com/questions/238760/word-for-100-majority) and not [supermajority](https://en.wikipedia.org/wiki/Supermajority#Common_supermajorities)) or they should start to censor other validators’ blocks.

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> A super majority of the validators (Authority) can steal these funds, censor transactions or revert finality.

Could you please show the attack on how to revert finality? We actually need it on Kovan to revert some transactions to remove PWASM support from two years ago. We can organize a supermajority of validators for this attack.

Here is one tx which created the first PWASM contract on Kovan https://kovan.etherscan.io/tx/0x5adeea1aeebb8911ed989a692de65b59083d517c566c9d41b3b18825830ae0cc

> can steal these funds

Please provide a more detailed attack vector how validators can steal funds of users.

Also, we invite you as a validator on Kovan or Sokol where you can show this attack

> These systems improve upon POA by providing much stronger guarantees.

Do you have any proofs of stronger guarantees of the observers model vs consensus model?

> Each token that wants to use this chain deploys its own token bridge contract.

It’s overhead. OmniBridge multi-token extension for the Arbitrary Message Bridge between Ethereum and such chain is the simplest way to transfer tokens to another chain https://docs.tokenbridge.net/eth-xdai-amb-bridge/multi-token-extension

With Optimistic TokenBridge there is no need for validators of the bridge to exit to Mainnet which is a better solution  [Optimistic bridge between Mainnet and a POS chain](https://ethresear.ch/t/optimistic-bridge-between-mainnet-and-a-pos-chain/7965)

> When optimistic rollups are ready to join they can update token bridges with their fraud proofs. This is opt in for the projects who now can choose when to use optimistic rollups.

there is no need to use optimistic rollups when there is an optimistic bridge. It doesn’t add security or reduce expenses but adds a complexity of the operation

> They are intrinsically flawed.

The COOP model (which is used in POA) with `one head is one vote` is one of the oldest ways of solving coordination problems in societies.

> You run the risk of the chain prevent your users from exiting with high fees when you try and upgrade to another solution

one can always deploy their own bridge and not use the abovementioned bridges by respectful validators, one can use Optimistic TokenBridge and not rely on the abovementioned bridges by token project [Optimistic bridge between Mainnet and a POS chain](https://ethresear.ch/t/optimistic-bridge-between-mainnet-and-a-pos-chain/7965)

---

**barryWhiteHat** (2020-09-16):

> Do you mean censor transactions
> or censor transactions via censoring blocks of other validators ?
> In the POA model, 100% of validators should agree on censoring transactions (which is unanimity and not supermajority) or they should start to censor other validators’ blocks.

Both. if you have n validators and m of them need to agree to censor a transaction then m is the number of validators needed to censor a transaction and n - m is the number of validators need to collaberate in order to censor blocks. So you have this difficult trade off when you make it harder to censor transactions you make it easier to censor blocks.

> Do you have any proofs of stronger guarantees of the observers model vs consensus model?

I am talking about optimistic rollup.

> The COOP model (which is used in POA) with one head is one vote is one of the oldest ways of solving coordination problems in societies.

I think that this is intrinsically flawed. Its like saying lets everyone vote for what the state of this system is after processing these x transactions and no one vote for yourself okay.

> Please provide a more detailed attack vector how validators can steal funds of users.

Super majority of validator sign a new state where they have all the funds. They then go to the bridge and withdraw their funds. If the bridge does not let them do it then a super majority of whoever controls the bridge can steal funds from users.

---

**rstormsf** (2020-09-16):

Could you please demonstrate it by running a Kovan’s validator node, please?

---

**vbuterin** (2020-09-18):

So the goal is to basically design a network that starts off as a fully PoA sidechain where the authorities can withdraw whatever they want, but then transitions over to having proper security guarantees over time by adding optimistic rollup features? (I agree with [@barryWhiteHat](/u/barrywhitehat)’s stance that PoA does not have the security guarantees that the broad Ethereum community expects and should be viewed as a stopgap solution only)

Seems reasonable; my main concern is just that the actual optimistic rollup projects that are out there (Optimism, Fuel, Arbitrum…) are getting close to launch so not sure how much we benefit by trying to spin up yet another new system in the meantime.

(I know that at least Optimism is starting with a single sequencer, so even if its fraud proof checking code has heightened risk at the beginning as any full-EVM OR must be, that risk is greatly tempered by a de-facto PoA security model…)

---

**igorbarinov** (2020-09-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> Both. if you have n validators and m of them need to agree to censor a transaction then m is the number of validators needed to censor a transaction and n - m is the number of validators need to collaberate in order to censor blocks. So you have this difficult trade off when you make it harder to censor transactions you make it easier to censor blocks.

In theorycraft setting, it’s a valid point. Although, that censorship attack is not practical by validators for valid exits. We didn’t see PoA network with censorship on consensus level used in wild.

Meanwhile, we are working on several tools for transaction prioritization for QoS based on the sender, receiver, function signature.

Here is an example of a `TxPriority` contract [posdao-contracts/contracts/TxPriority.sol at 49e2c37e43296f06ee25795ceeb9acc16b8c64c8 · poanetwork/posdao-contracts · GitHub](https://github.com/poanetwork/posdao-contracts/blob/49e2c37e43296f06ee25795ceeb9acc16b8c64c8/contracts/TxPriority.sol)

```auto
which defines three types of rules:

* Transaction targets (destinations) sorted by descending of weight.
* Whitelist of top priority senders.
* Additional Min Gas Price filter for certain targets.
```

We propose it on a non-consensus level where validators can apply or can not apply such rules for essential/ malicious destinations.

> I am talking about optimistic rollup.

offtopic question: which properties of optimistic rollup are missing in a sidechain with PoS consensus and optimistic exit without validators?

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> If the bridge does not let them do it then a super majority of whoever controls the bridge can steal funds from users.

in the design of our optimistic bridge, the bridge can be stopped by a social recovery mechanism managed by the community with a wide distribution of keys like 5 of 9. Such a social recovery mechanism is protecting trillions of dollars in value in the wild, e.g. root zone of DNS domain is 13 authorities with n of m signature [Root Servers](https://www.iana.org/domains/root/servers)

not speaking of billions locked in DeFi projects all over Ethereum.

---

**barryWhiteHat** (2020-09-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> So the goal is to basically design a network that starts off as a fully PoA sidechain where the authorities can withdraw whatever they want, but then transitions over to having proper security guarantees over time by adding optimistic rollup features?

Yes. Some projects could even delay withdraw ability until after the fraud proofs have validated historic state.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Seems reasonable; my main concern is just that the actual optimistic rollup projects that are out there (Optimism, Fuel, Arbitrum…) are getting close to launch so not sure how much we benefit by trying to spin up yet another new system in the meantime.

I would have loved to have had this idea in January ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) I have listed reasons why its may be still worth it below.

#### Reasons for

1. Uncertainty about the delivery time + uncertainty about maturity / security in the short term.
2. People needing to launching stuff right now. The upgrade path from side chain to optimistic rollup tends to include a withdraw fee which can be adjusted by side chain governance so am not crazy about launching on another side chain.
3. People reluctant to launch on a brand new system that has not been battle tested.
4. Having a rollup with two different fraud proofs on the same rollup will force push optimistic rollup VM teams to standardize on the data availability format EVM and some other stuff which would be helpful but also possibly slow things down.
5. Optimistic rollup VMs could be a naturally monopoly forming so structuring things in a way that there can be more than one “winner” seems like a good idea.
6. Allowing different tokens to have different withdraw bridges with different time outs and dependent upon different fraud proofs makes sense.
7. Would mean there is more than one implementation of coordinator “node” which could help security.

---

**adowson** (2020-09-19):

Hi Barry,

This is an extremely interesting proposal which I think is a fantastic short term plan.

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> ## Phase 1: Setup
>
>
>
> First we set up a PoA chain with our high reputation projects. Each token that wants to use this chain deploys its own token bridge contract. This is registered on the PoA side who treat balance made here as PoA chain deposits.

It seems strange that we would not consider using the xDai rather than spinning up an entirely separate PoA chain, xDai has been in production for over 2 years now which has a tonne of tooling available (TheGraph, Nethermind, OpenEthereum…), wallet support, a solid developer following, well battle-tested, a great set of validators and many projects migrating over there frequently.

If we decided to set up a new PoA chain it would throw away a lot of the infrastructure and support which is already available with xDai, granted it’s is far from perfect however it fits perfectly with the proposal outlined here.

igorbarinov has already outlined a proposal for as an interim solution to [increase the number of bridge validators from 5 to 9](https://forum.poa.network/t/increase-number-of-participants-in-the-xdai-bridge-management-multsigs/3773) (far from ideal) but the team has also proposed an [optimistic bridge between mainnet and a POS chain](https://ethresear.ch/t/optimistic-bridge-between-mainnet-and-a-pos-chain/7965/6) which again, is harmonious with this proposal.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> my main concern is just that the actual optimistic rollup projects that are out there (Optimism, Fuel, Arbitrum…) are getting close to launch so not sure how much we benefit by trying to spin up yet another new system in the meantime.

I completely agree with what [@vbuterin](/u/vbuterin) has said here, optimistic rollup projects are close to being done so deploying an entirely separate PoA chain instead of using xDai will just delay what we all are aiming to achieve which is the quickest / best solution to scale Ethereum. We have the PoA expertise of igorbarinov and the POA / xDai team and the wealth of knowledge from the EF to make this a reality, we have seen over the past few weeks we simply can’t afford to wait and we need a solution now.

I’m sure between igorbarinov and ourselves we can reach some sort of consensus on this, the xDai team have already publicly stated several times about being a staging network for ETH2 / rollups. If we can find some harmony here, it seems like a great fit.

I think the guys over at Gnosis (recently migrated to xDai) have summed this up nicely:

> We’re looking forward to this collaboration [with xDai] bolstering the perfect staging environment for Ethereum, due to its migration capabilities, token economics, and low transaction costs. Because Gnosis is long on the Ethereum ecosystem, we believe it’s important to invest in infrastructure that will keep bringing users and developers to our ecosystem.

I would be interested to hear [@barryWhiteHat](/u/barrywhitehat), [@vbuterin](/u/vbuterin) and igorbarinov’s thoughts to see how we could make this collaboration a reality.

---

**kaiynne** (2020-09-21):

Agreed this would have been an excellent idea in January had we suspected things could get this extreme, but I honestly think that we are now so close to launch for implementations of ORU that resources would be far better spent on shaking down those testnets and ensuring the mainnet transition is as smooth as possible. This is where we have been putting the Synthetix resources and I think it is about to pay off ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

