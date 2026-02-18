---
source: ethresearch
topic_id: 6937
title: "Surrogeth: Tricking frontrunners into being transaction relayers"
author: lsankar4033
date: "2020-02-13"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/surrogeth-tricking-frontrunners-into-being-transaction-relayers/6937
views: 4673
likes: 8
posts_count: 3
---

# Surrogeth: Tricking frontrunners into being transaction relayers

## Background

There are two use-cases for relayer networks that have been getting attention recently:

1. meta-transactions to ease user onboarding (i.e. not require owning Eth)
2. mixers because the withdraw address may not have Eth to pay for gas

Existing relayer network solutions attempt to create relayer networks from scratch ([tornado](https://github.com/tornadocash/relayer) and [GSN](https://gsn.openzeppelin.com/)). The small number of initial relayers in these networks means that they’re doomed to have oligopoly pricing until some point in the future where there’s a massive number of relayers in each of them.

Fortunately, there’s an actor who’s already doing relayer-type activity on Ethereum for cheap: smart contract frontrunners. As has been [documented elsewhere](https://arxiv.org/abs/1904.05234), these actors scan the mempool for transactions that are profitable to run and ‘frontrun’ them indiscriminately, frequently with a very low profit margin.

I present here [surrogeth](https://github.com/lsankar4033/surrogeth), a  system for tricking frontrunners into running transactions.

## Experimenting with Frontrunners

To convince myself that frontrunners do in fact pick up profitable transactions profitably and to get an idea of what their ‘minimum’ profit was, I ran a quick experiment.

I loaded a contract with Eth and exposed a single method that would release some of that Eth as a reward to `msg.sender` if it was called with a signature of `(reward_released, incrementing_nonce)` by a key that I control ([Source code](https://github.com/lsankar4033/lemonade/blob/a02a748ad13ec3cdb167cf7fa3e9bbc40e564d5a/contracts/contracts/Lemonade.sol#L12)). I then attempted to transact (and get frontrun) with this contract. Sure enough, a [number](https://etherscan.io/tx/0x4c76fbee84232214de28bd8de76324b8d5796d3c8cf56b05a341dd92c432a19f) [of](https://etherscan.io/tx/0x7ac58deb397df36b650b59f5ed46cbd11fc7c5793e7145385e1dd816c292809e) [my](https://etherscan.io/tx/0x59acbba5e30b80d91c6fc4db614ad21c8f47276289082e61fb478e14dd3f251a) transactions were frontrun.

Although this is far from statistically significant and all of this frontrunning happened to be done by a single frontrunner, the minimum profit the frontrunner took on my transactions was ~0.00177 Eth, which is an order of magnitude smaller than [a representative fee on tornado.cash](https://etherscan.io/tx/0x3af72b131bb6ea590c29231629e5d8d547b0b7f950c15b29c6e652c206c2465d).

## High-level design

The following diagram shows the entire system:

Mempool

Mempool

Registry Contract

Registry Contract

Forwarder Contract

Forwarder Contract

Forwarder Contract->Registry Contract

7

Application Contract

Application Contract

Forwarder Contract->Application Contract

6

Client

Client

Client->Registry Contract

1

Broadcaster

Broadcaster

Client->Broadcaster

2

Broadcaster->Mempool

3

Frontrunner

Frontrunner

Frontrunner->Mempool

4

Frontrunner->Forwarder Contract

5

Numbered interactions:

1. Client checks registry contract for URIs of broadcasters and appropriate fees
2. Client sends signed data to broadcaster’s URI
3. Broadcaster broadcasts transaction to Forwarder Contract to the network
4. Frontrunner payload it can profit from in the mempool
5. Frontrunner frontruns transaction to Forwarder Contract
6. Forwarder Contract calls Application Contract. Application Contract sends relayer fee back to Forwarder, which then refunds msg.sender
7. Forwarder Contract logs successful relay + fee in Registry Contract

## Mechanism explanation

Broadcasters are necessary to get the client’s signed data to the mempool because the application user may not have any Eth to pay for gas. Because broadcasters are effectively offering their txes up to frontrunners, they need to run as efficiently as frontrunners (likely because they are). Otherwise they have no incentive to advertise their URI in the registry contract.

With even a few capable frontrunners advertising their addresses in the registry, signed data will now be broadcast to the entire frontrunner network. Note that this mechanism assumes that frontrunners will want the edge of seeing profitable txes first so much that they’re willing to potentially be frontrun. This seems to be the case intuitively, but is worth validating.

One way to think about how this system functions is that we’re restructuring apps that need txes relayed to operate on some piece of signed data from the user:

- in mixers, this is the ZKP proving the deposit
- in meta-transactions, this is signed data demonstrating that the user wants to take an action

When these signed pieces of data hit the mempool, they’re free money for whoever is willing to bite.

## Next steps

I decided to post this before surrogeth is live so I feel a bit more pressure to finish the remaining pieces:

- deploy the contract and publish the address
- documentation, documentation, documentation

---

If you’re interested in using gasless transactions or want to build an alternative, low-fee UI for tornado.cash, let me know! I’ll be at EthDenver and hope to kick the tires on this thing.

Frontrunners can permissionlessly list themselves in the registry, but feel free to get in touch if you want to list yourself and need help ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

Finally, if you have any other ideas for how we can use frontrunners to our advantage, please let me know. I suspect they could fit into the layer 1.5 picture somehow, but haven’t quite figured out how yet.

[tg discussion link](https://t.me/joinchat/HdJ0wBc1xi52GtOMtayyAg)

(thanks to [@barryWhiteHat](/u/barrywhitehat) and [@weijiekoh](/u/weijiekoh) for conversations that led to this)

## Replies

**Pertsev** (2020-02-23):

Case 1. Someone sends a tx to all registered broadcasters. They will process and distribute the tx simultaneously, so one of them will be rejected by the smart contract and charged by the network.

Case 2. Someone implements a contract that gives the reward while a broadcaster simulates a tx, but rejects for the actual tx.

Is there any protection from those attacks?

---

**lsankar4033** (2020-02-26):

It’s on the broadcasters to choose which txes they want to re-broadcast. I’d expect broadcasters to eventually be able to tell (by looking at contract bytecode) whether or not there are conditionals based on block values (i.e. block ts or hash) and decide to reject those that are ‘un-simulatable’

