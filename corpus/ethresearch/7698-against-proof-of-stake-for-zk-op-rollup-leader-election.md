---
source: ethresearch
topic_id: 7698
title: Against proof of stake for [zk/op]rollup leader election
author: barryWhiteHat
date: "2020-07-17"
category: Layer 2
tags: [rollup]
url: https://ethresear.ch/t/against-proof-of-stake-for-zk-op-rollup-leader-election/7698
views: 9276
likes: 19
posts_count: 14
---

# Against proof of stake for [zk/op]rollup leader election

## Intro

The adoption of layer 2 scaling solutions could represent the centralization of control over assets stored within them.

[zk/optimistic]Rollup promises to offers 1000’s of transactions per second on ethereum. However this comes at removing the miners as the groups involved in transaction ordering AND the group who 51% are able to censor transactions. This power is vested in a coordinator. A coordinator is basically selected as a single entity who has a monopoly on block creation for a given epoch.

The selections of coordinator is a difficult open problem. A few solutions have been proposed

1. Centralized coordinator
2. MEV/ burn auction
3. Proof of stake

Here we describe several attacks against proof of stake coordinator selection on layer 2 and recommend alternative approaches.

## Hardfork to recover from failure modes

On layer 1 POS works well. Huge amounts of capital is placed and used to ensure that data is available. If the system enters a failure mode (a DOS attack or data availability attack) then there can be a protocol level hardfork to remove the deposit from the attacker.

On layer 2 this is very different. It seems very unlikely to be able to coordinate a hardfork in order to slash a misbehaving coordinator of some layer 2 system. Removal of this tool fundamentally limits the ability of POS to be able to respond from attacks.

## DOS attack

If someone with a lot of stake wants to shut down or slow down layer2 system. They can begin staking their tokens and mint only empty blocks. The cost of for them is

1. The opportunity cost on their tokens
2. The reduction in the value of their stake that this attack has.

There are also several ways for users to profit from this attack

1. Charge a high fee in order to process transactions
2. Charge a high fee in order to allow users to withdraw
3. Lock up a bunch of the supply of certain tokens causing the markets to go crazy, for example if you locked up 50% of DAI you could profit if the price of eth fluctuated.
4. Take a short position on the token that is used for staking. Stake -> DOS -> Price Crashes -> Profit.

On layer 1 this is less of a problem because we can always do a protocol level hardfork in order to remove the stake. But on layer 2 it seems like there is no way to punish people for using this attack.

## Fake DOS attack

If a dos attack is happening. Stakers will have a opportunity to not participate in the dos attack and get more rewards. This could push the price of the token higher during a dos attack as more stakers look to increase their stake in order to get more rewards.

An attacker can use this as follows

1. Buy a bunch of token X
2. Start dos attack using some of your token X
3. The market goes up as stakers rush to increase their stake
4. Attacker sells their token X for profit
5. Attacker ends their DOS attack value of token X goes down.
6. Attacker buys token for lower price (Optional)

Repeating this attack an attacker can

1. Discourage other stakers from joining during a dos attack
2. Can start to increase their stake by repeating this attack causing the market to fluctuate.

## Slashing attack

Most of these systems have a slashing condition where stakers get slashes if they don’t create a block by time X. The attacker who is also a miner. Refusing to include transactions from other coordinators. They also refuse to build upon blocks containing their transactions trying to uncle them and slash the victim.

Using a relatively small % of the mining power the attacker can significantly increase the chances of another staker getting slashed.

NOTE: There are also network level dos attacks that an attacker can use to prevent the propagation of valid blocks , prevent the staker from producing their blocks in time.

## Coordinator takeover

The ability to slash or buy most of the staking tokens in circulation can lead to coordinator take over. Where they can create almost all the blocks and use this power to impose massive withdraw fees on users wishing to leave. This reduces to almost 0 the value of their tokens.

## Conclustion

The limitations here are based upon

1. The inability to hardfork the token gives no way to recover from failure modes like we can on layer 1.
2. Its possible that attackers with a small % of active stake holders can harm the network as a whole. They can materially reduce the through put of the system by creating empty blocks.

Solutions like [MEV Auction: Auctioning transaction ordering rights as a solution to Miner Extractable Value](https://ethresear.ch/t/mev-auction-auctioning-transaction-ordering-rights-as-a-solution-to-miner-extractable-value/6788/9) and [Spam resistant block creator selection via burn auction](https://ethresear.ch/t/spam-resistant-block-creator-selection-via-burn-auction/5851) also need more analysis before we can start to recommend what to use for rollup leader election.

## Replies

**GriffGreen** (2020-07-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> On layer 2 this is very different. It seems very unlikely to be able to coordinate a hardfork in order to slash a misbehaving coordinator of some layer 2 system. Removal of this tool fundamentally limits the ability of POS to be able to respond from attacks.

Slashing can still be done without a hard fork, as long as the Staking is done on L1 and the Staking contract has a time lock and a strategy to apply slashing (could be just a subjective Staking Coordinators’ vote, Kleros or Aragon Court judgement, or an automated strategy).

What am I missing?

---

**adlerjohn** (2020-07-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/griffgreen/48/1128_2.png) GriffGreen:

> could be just a subjective Staking Coordinators’ vote, Kleros or Aragon Court judgement, or an automated strategy

Then the security of the L2 degenerates to this governance mechanism and the PoS becomes redundant.

---

**edmundedgar** (2020-07-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/griffgreen/48/1128_2.png) GriffGreen:

> barryWhiteHat:
>
>
> On layer 2 this is very different. It seems very unlikely to be able to coordinate a hardfork in order to slash a misbehaving coordinator of some layer 2 system. Removal of this tool fundamentally limits the ability of POS to be able to respond from attacks.

Slashing can still be done without a hard fork, as long as the Staking is done on L1 and the Staking contract has a time lock and a strategy to apply slashing (could be just a subjective Staking Coordinators’ vote, Kleros or Aragon Court judgement, or an automated strategy).

What am I missing?

So the difference is that with a protocol-level fork, the “true” fork can win even if the attacker marshals more funds than the defender, because people will just ignore the bad ledger and use the good one. Governance systems like Augur that work on top of L1 have this subjective security property with respect to their own token, REP, but resort to an objective measure when it comes to all the “hard” assets they manage that they can’t fork. In Augur’s case, they fork Augur into two, but all the ETH and DAI locked in existing markets will go to the version of Augur that had more REP moved into it. So you can break Augur enough to steal the ETH and DAI by controlling more REP than the other side, and moving them into the “lying” fork. Augur tries to disincentivize attacks like this by using fees to regulate the amount of “hard” assets it controls compared to the value of REP, but this is probably not really enforceable even for them, and it wouldn’t be practical here.

Note that you *could* have subjective security for a governed rollup with respect to the governed rollup’s governance token (if it had one), *and any assets issued inside the rollup*. So if I issue a token on the rollup’s ledger, the governance of the rollup could get broken, the rollup ledger copied by another operator, and my token now exists in both ledgers. Since the “honest” ledger is more useful, we can reasonably hope the users and the value will migrate to that, regardless of the governance breakage.

I think you can take this to another level and say that since we have to take the security hit for governance anyhow and preserve the possibility of forking to secure it (albeit we couldn’t totally secure the “hard assets”) ***we may as well build in a general-purpose oracle***, so that the same trust anchor used to manage who should be operating the rollup can also tell you (via an escalation game), “what is the value of 1 ETH in USD” or “Who won the 2024 presidential election”. Making complex, interrelated contracts work properly in the event of a governance fork is something that’s quite practically tricky to do on the current L1 - [I’ve tried](https://medium.com/@edmundedgar/what-happens-when-you-try-to-fork-an-ethereum-token-863e3defcf7) - but should be very simple and clean if you’re just copying a rollup ledger.

---

**gluk64** (2020-07-28):

A simple solution to all the problems raised in the case of zkRollup: disable slashing, instead provide an option of mass-migration, enforceable on L1 via a priority queue. It can be considered an L2 equivalent of a hard-fork.

---

**adlerjohn** (2020-07-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/gluk64/48/11557_2.png) gluk64:

> instead provide an option of mass-migration, enforceable on L1 via a priority queue

That’s called [Plasma MVP](https://ethresear.ch/t/minimal-viable-plasma/426).

---

**gluk64** (2020-07-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> That’s called Plasma MVP .

No, no, no, not a mass exit ![:stuck_out_tongue_closed_eyes:](https://ethresear.ch/images/emoji/facebook_messenger/stuck_out_tongue_closed_eyes.png?v=12)

A mass migration! That’s why I said it is only an option for zkRollup (not optimistic rollups).

The way it works: the pissed off users organize and form a new zkRollup validator group. Then they submit a single proof of mass exit to the old zkRollup smart contract, which will transfer the total amount of tokens owned by these users to the smart contract of the new zkRollup.

---

**gluk64** (2020-07-28):

A mass migration does not need to happen within a fixed temporal frame – it can be done anytime. Hence no mass exit problem.

---

**adlerjohn** (2020-07-28):

Ah I see.

You can do the same in an optimistic rollup though, with the same guarantees that the optimistic rollup would provide. The way it works: the pissed off users organize and form a new optimistic rollup chain. Then they submit a single block of mass exit to the old optimistic rollup smart contract, which will transfer the total amount of tokens owned by these users to the smart contract of the new optimistic rollup after a timeout and no fraud proofs.

(Note: anything you can do with validity proofs can be done with fraud proofs + synchrony assumption.)

---

**gluk64** (2020-07-28):

With optimistic rollup you will have to publish the witness data (addresses and signatures) for every single pissed-off user. Assuming millions of accounts in the rollup, this remains a huge DoS vector.

---

**adlerjohn** (2020-07-28):

You can eliminate the overhead of witness data using aggregate signatures (making optimistic rollup take up less blockspace than zk rollups!). Beyond signatures, using a validity proof doesn’t let you post less data on-chain.

---

**barryWhiteHat** (2020-07-28):

There is no incentive for proof of stake selected coordinator to allow these annoyed users to mass migrate. In fact it harms them to let these users leave. So they would either charge a huge fee or just not process them at all.

I image we would have to go on chain to force the exit. This would be heavily dependent on the gas market which would mean that users with less funds would not be able to afford to migrate.

Both cause users to be stuck in zkrollup with a coordinator whose incentives are not aligned with their interests.

---

**kladkogex** (2020-08-13):

Great topic.  IMHO when someone tries to fix things, one almost immediately arrives at a blockchain.

Like in this example. The best remedy is to decentralize the operator.  Then a rollup turns into a slave blockchain that pull transactions from the master.

---

**thor314** (2020-08-17):

This may not be the attitude of the community, but I would recommend substituting master-slave with leader-follower terminology for inclusiveness reasons ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=14)

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Like in this example. The best remedy is to decentralize the operator. Then a rollup turns into a slave blockchain that pull transactions from the master.

