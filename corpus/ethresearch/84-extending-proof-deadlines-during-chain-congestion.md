---
source: ethresearch
topic_id: 84
title: Extending proof deadlines during chain congestion
author: RoboTeddy
date: "2017-09-10"
category: Layer 2 > State channels
tags: []
url: https://ethresear.ch/t/extending-proof-deadlines-during-chain-congestion/84
views: 3773
likes: 8
posts_count: 25
---

# Extending proof deadlines during chain congestion

## Problem:

State channels, truebit, etc have deadlines for receiving final updates and fraud proofs. An attacker can participate in many of these state channels, commit mass fraud, and then congest the main chain (e.g. by attacking lots of state channels at the same time, or just spamming transactions). Fees could become very high, and attackees could miss the deadline.

## Possible solution:

Allow a deadline to be extended by a transaction claiming that there are many valid fraud proofs waiting to be processed. The claim carries a security deposit as well as the root of a merkle tree of the supposed transactions containing fraud proofs. The contract managing the deadline could sample from the list of claimed fraud proofs, and then interactively request & verify the actual fraud proofs. If the claimer fails to provide an actual fraud-proof-containing transaction, then the original fraud deadline is maintained and the claim’s security deposit is destroyed.

This “proof of proofs” process doesn’t require too many transactions, so they could include high fees that cut through congestion. Sufficiently-verified claims could both extend the deadline and deliver a reward to make up for the work, transaction fees, and time-value of the security deposit. The reward could be funded by state channel tx fees.

Could an attacker endlessly extend the deadline by committing fraud against themselves in order to generate valid proof-of-proofs? We could make it expensive:

1. After the deadline has been extended, the protocol could continue to demand submission of all the fraud proofs that the claimer committed to. If the claimer fails to submit any of them, their security deposit could be revoked.
2. It could be the case that each processed fraud proof results in the destruction of an associated security deposit (separate from the deposit in the claim). The claim could include a deposit size for each fraud proof it attests to, and selections for verification could be weighted by the size of the security deposit. Prior to actually extending the deadline, interactive verification could continue until some threshold amount of coin has been provably destroyed.

(This approach wouldn’t help against e.g. a network DDoS that takes down a sufficient number of nodes)

## Replies

**nate** (2017-09-10):

Another solution to the problem is having a gas oracle on-chain that is aware of congestion.

Essentially, we can use block.blockhash, as well as an RLP encoded block header, to prove to a smart contract the amount of gas used in previous blocks (as well as their gas limit, as well as a bunch of other interesting information).

This means we can say: “if the oracle is not aware of how congested things are, let’s assume it was because it’s to congested for it to become aware.” The benefit of this is that we don’t have to send any transactions when the network is congested. The tradeoff is that the oracle has to be constantly fed otherwise.

[Eric Tu](https://github.com/tueric) and I wrote a POC for a hack-a-thon over the summer. Most of the code is in a state of disrepair (both of our schools started back up ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) ), but you can find the essentials bits here:


      [gist.github.com](https://gist.github.com/naterush/fa2182f18e0ef86a285ee205753cd3c7)




####

##### GasOracle.sol

```
pragma solidity ^0.4.8;

// RLP library moved below for readability

contract GasOracle {
  using RLP for RLP.RLPItem;
  using RLP for RLP.Iterator;
  using RLP for bytes;

  mapping (uint => BlockHeader) blocks;
```

This file has been truncated. [show original](https://gist.github.com/naterush/fa2182f18e0ef86a285ee205753cd3c7)








We’ve been calling this “elastic timelocks.” Hopefully will be able to work more on this soon, but feel free to use our code as is (no warranty, though ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) ).

---

**MicahZoltu** (2017-09-10):

The immediate problem I see with the congestion Oracle (as you have described and I understand) is that a miner can choose to always mine the Oracle, even when normally it wouldn’t pick the Oracle transactions based on their gas price.

We have to remember that gas prices are a bribery system, and bribes are not guarantees.  Any system that makes any assumptions about which transactions will get mined and which won’t can be gamed by miners who don’t simply do “highest gas price first” for picking transactions.  We already see this today where it is not uncommon for a miner to fill its block with transactions that are not optimal in terms of gas pricing.

---

**nate** (2017-09-10):

Thanks for the feedback ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=9)

I should clarify - the congestion oracle does not rely on assumptions about which transactions miners choose to include (at least in the way I think you are saying); otherwise, we would have exactly the issue you describe, where miners could attack it super easily.

Instead, users prove to the oracle the congestion of recent blocks, by providing a block header from a recent block, confirming it is a recent block, then parsing the RLP to get the gasLimit and the gasUsed. (Note: the oracle I linked is just the bare-bones parsing bit of what is necessary to make it legit.)

If, as you describe, miners choose to always mine the Oracle, then the oracle will know if the network is congested; if miners choose to not mine the oracle (or there are no tx to the oracle), we assume it’s due to network congestion and stretch timelocks accordingly. The benefit here is that we don’t have to submit any (high fee) transactions during a congested period.

Miners could choose to censor all transactions to oracle as a sort of nuisance attack, but, in this case, we have much bigger worries; they would just choose to censor all challenges going to the state channels in the first place.

There is another, different issue with miners influencing the oracle though; they can simulate chain congestion at almost no cost (small cost is the increased risk of uncled blocks). Essentially, they can insert a bunch of fake transactions into their own blocks, convincing the oracle that the network is congested (and thus making the elastic timelocks strech when they really shouldn’t). This is probably a more reasonable and effective nusiance attack than the one described above, as it does not require a 51% majority to occur.

This can be mitigated to some degree with fee burning, but that’s a protocol level change ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**jgm** (2017-09-10):

I’m a little confused at the premise here.  Whatever the gas price of transactions in the pool a state channel recipient can always pay more in an attempt to have their transaction mined.

As long as the gas cost of closing a channel is low (which is an assumption, yes, but within the control of the contract developer) the cost to each channel recipient of the single transaction to close the channel should be small compared to the cost to an attacker to flood the network with delaying transactions.

Using a block gas limit of 6.7 million and a channel close cost of 200K as an example, the attacker would need to pay over 30x the amount of Ether that the channel recipient would be willing to pay *per block* to stop them from closing the channel.  If best practice is for channels to be closed 1 day before their expiry we’re talking about a total disparity of something like 100,000x.  It doesn’t strike me that this is a realistic concern.

That said, it would be interesting to consider if some of the meta information  (e.g. average time between blocks for last 100 blocks) from the chain could be made available to contracts.  Might hit consensus problems so perhaps would need to run a bit behind the current state but could be useful nonetheles.

---

**RoboTeddy** (2017-09-10):

Let’s take those constants (cost of 200k; gas limit 6.7m; window of 1 day; ~3k blocks/day). It’s thus impossible to prove fraud in more than 100,000 state channels in a single day. If the attacker is participating in 1 million state channels and commits fraud in all of them (who might do this? perhaps a payment channel hub), then victims will have to bid against each other for block space. The 100,000 attackees with the most at stake will make it in; 900,000 of them will not (to the attacker’s benefit).

---

**nate** (2017-09-11):

As [@RoboTeddy](/u/roboteddy) describes, the issue is more so that there is a limited amount of block space – so that even if everyone paid the highest fee they possibly could, not everyone would be able to get their challenge in on-time. As Robo says, think a single payment channel hub (or a few who are conspiring) committing fraud on all channels at once. This is something that the gas oracle could be useful in dealing with.

Also, with a single line added to the RLP blockheader parsing code linked above, the oracle linked above could be adapted to get information like “average time between blocks for last 100 blocks.” Pretty much any information that can be recovered from the block header (which is a lot) can be parsed by an oracle of this type (within the past 256 blocks, though there are ways around this).

---

**jgm** (2017-09-13):

“if the attacker is participating in 1 million state channels” seems like a bit of a jump.  If we take payment channels as an example: they generally have a set reason for existence (e.g. ongoing payments to a single target entity, e.g. ISP or utility company) or are set up to feed through a hub.  In the former case an average user might have 10 such channels open so you would need 100,000 people working together to cause the problem.  In the latter case there would be a significant minimum deposit to make the channel worthwhile so the attacker would need to find tens or hundreds of millions of dollars to attempt to mount an attack.

Separately, the mere activity of creating such a large number of state channels in the timeframe required to be able to mount an attack would cause an inadvertent version of the attack you are suggesting, which would raise enough flags to at least make channel recipients (hubs or otherwise) very aware of the issue and able to adjust accordingly.

---

**nate** (2017-09-13):

I’m no expert on state channels, but what stops the hub itself from attacking and settling all channels w/ some old state? In this case, it seems like there would be no need to coordinate among that many users.

Also, I’m not sure I follow the second part of the argument; not all state channels will be created, used, then settled immediately. As a user, in some cases, it makes more sense to keep payment channels open, as to be able to transact without having to place another deposit. In this case, the state channel creation deposits could happen over some longer time period, where block congestion is less of an issue.

---

**RoboTeddy** (2017-09-13):

Also see:


      [github.com/raiden-network/raiden](https://github.com/raiden-network/raiden/issues/383)











####



        opened 04:37PM - 08 Feb 17 UTC



        [![konradkonrad](https://avatars3.githubusercontent.com/u/3705643?v=4)
          konradkonrad](https://github.com/konradkonrad)






Problem Definition
Currently we have a fixed block number "settlement_timeout" (ST) that needs to pass after close was called in the Channel....

    Component / Smart Contracts
    Flag / Security
    State / In discussion

---

**jgm** (2017-09-13):

The reason that a hub would not settle with an old state is that promises provide monotonically increasing values, so settling with an older promise would rob the hub of funds.

Regarding the second argument: it is in all parties’ interests that the payment channel remain open as long as possible.  Payment channels might have a fixed duration (e.g. 4 weeks) or a fixed end date (e.g. 1st October).  In the former case it would be very expensive to create the required number of channels with a suitable end date, and in the latter case it would be obvious to the channel recipient what was going on well in advance of it becoming an isssue.

---

**vbuterin_old** (2017-09-15):

I don’t see why ethereum channels should ever have a preset end date. I think that this is a holdover from bitcoin land where the timelock approach has that inherent limitation; but in ethereum channels should generally last indefinitely until deliberately closed.

> “if the attacker is participating in 1 million state channels” seems like a bit of a jump. If we take payment channels as an example: they generally have a set reason for existence (e.g. ongoing payments to a single target entity, e.g. ISP or utility company) or are set up to feed through a hub. In the former case an average user might have 10 such channels open so you would need 100,000 people working together to cause the problem

I think we are assuming that channel systems will end up having at least a few centralized hubs. Companies like Coinbase, for example, could easily have 1 million connections that they are participating in; same with other large wallet providers.

---

**jgm** (2017-09-15):

> I don’t see why ethereum channels should ever have a preset end date. I think that this is a holdover from bitcoin land where the timelock approach has that inherent limitation; but in ethereum channels should generally last indefinitely until deliberately closed.

The traditional reason is to give the sender in the channel some surety that they can retrieve their funds if the recipient is being un-cooperative.  Yes there are other ways of achieving this, but having a hard-coded end time is both simple and cheap.  A secondary issue is that any funds in the channel are unavailable to either party until the channel is closed, so having a channel with an indeterminate end time gives no surety to either party as to when they may be paid/refunded.  Again, there are ways to alter the payment channel such that you can retrieve funds whilst the channel is open but not without significant requirements on the parties (i.e. having to monitor the chain and be aware of its state at all times).

> I think we are assuming that channel systems will end up having at least a few centralized hubs. Companies like Coinbase, for example, could easily have 1 million connections that they are participating in; same with other large wallet providers.

True, but unless these million connections were all under control of the same entity they couldn’t be used as part of a coordinated attack.

---

**vbuterin_old** (2017-09-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> True, but unless these million connections were all under control of the same entity they couldn’t be used as part of a coordinated attack.

But the whole point is that they *are*. These one million connections would all be with Coinbase.

---

**nate** (2017-09-16):

If the recipient is being uncooperative, the sender can just try and settle the channel with some old state; if the recipient does not challenge this, the sender gets all of their money back (+ some). If the recipient does challenge this, the channel will settle, and the sender will get all of their money back.

As the sender could post an old state anyways (not even when they are trying to force the channel to settle, just when they are trying to steal), the recipient of the channel necessarily must be monitoring the channel otherwise, so nothing really has to change.

---

**ZacMitton** (2017-09-28):

> in ethereum channels should generally last indefinitely until deliberately closed.

Generally yes, but Don’t we still need timeouts *after* a cheque has been presented? There still seems to be the need for a definite time a user has to prove a cheque is outdated before parties can withdraw.

For availability - I see it as 2 separate issues:

1)The network has too much traffic overall, and

2)Ethereum is being attacked (from shanghai with love)

The first It’s not a problem because the sheer expense of of this for *any meaningful* period of time is too expensive. Even for a fast timelock of 1 hr lets run the numbers. ~1.7 billion gas would have to be getting used for computation to fill this hour. Presenting my cheque may cost 50,000 gas. Thats 1/33000th of the total network in this hour. Even if the network is spending a million dollars an hour on ethereum transactions (maybe reached for 2 minutes during BAT ICO) It would only cost me 30$ to get my important Tx to the front of the line.

The second problem is, I believe, a growing pain that Ethereum can solve over time by properly calibrating gas prices and improving the networking layer. If that network can be DOSed like this, it will need an upgrade. Lets just think about how much value we hold in channels as Ethereum matures.

For Truebit however the problem is significantly exacerbated by the verification game, each step of which, requires a safe timeout period. This might be up to ~10-100 periods.

[@nate](/u/nate)’s solution does help. I think a more valuable focus first is engineering the network layer of these systems. Because availability of Ethereum as-a-whole is already far better then a single user’s internet connection. Any design for state-channels / Truebit *must* incentivize a side network to hold cheques and “poke” them in on behalf of users who lose signal.

---

**RoboTeddy** (2017-09-29):

[@ZacMitton](/u/zacmitton) per [@vbuterin](/u/vbuterin)’s post, we could expect to see huge sudden demand for chain space if a payment hub tried to cheat a ton of people at once. The fees for all that congestion would be paid by the victims or their advocates, not the attacker.

To make matters worse, the chain space available for this mass of fraud proofs could be further reduced if the attacker bribes selfish miners:

An attacker who stands to gain from censoring a fraud proof can create a smart contract that will automatically distribute a reward to miners iff that fraud proof is not committed to the chain during the challenge period. The reward received by each miner could be proportional to the number of blocks they discovered during the challenge period. (This could be done for each fraud proof). This kind of bribe-induced censorship could be a problem generally, but it’s particularly problematic in the presence of chain congestion and when the censorship only need be maintained during a limited window. If a bribe fails, the attacker gets his bribe money back (losing only its time value).

If half of mining power behaved selfishly, then there would be half the amount of chain space left over for the glut of fraud proofs. Half as many people would make it out safely. Ouch! (Under more typical circumstances, half of miners selfishly participating in the censorship of a transaction wouldn’t do much – it would merely double its expected confirmation time).

---

**nate** (2017-09-29):

> Generally yes, but Don’t we still need timeouts after a cheque has been presented?

Sure, there still have to be finite (maybe dynamic) timeouts for the challenge period - but otherwise, they are not necessary (no need for channels to timeout unless closed).

I’m not sure I follow your argument about network congestion. The case we have to consider isn’t just natural network congestion (this is still an issue), but rather the situation described above: a hub (e.g. Coinbase) fraudulently begins settlement of all it’s open channels at once, and there simply isn’t enough space over the next hour for all challenges to occur.

In this case, while certain wealthy (and willing - e.g. they have large state channel deposits that stand to be lost) users could pay to get into the limited space to challenge, some users would necessarily lose money. This is the case we have to worry about (and is the case that a system like the gas oracle described above can mitigate).

---

**ZacMitton** (2017-09-29):

Fair enough. I just think it’s premature to focus on this when the real problem is that I’ve yet to see a practical state channel with said “network” to play watchdog on itself (so no reasonable security at all at this point).

Agree it’s worth conceptualizing the issues with a system transacting for millions of people,  but let’s not overengineer the next/first generation of these channels. I believe google’s rule-of-thumb, is to engineer for 10x the current usage demands. In blockchain maybe we should engineer for 100x given the high speed of advancement, but the above problems mostly emerge in the 1000x and 100000x scenarios.

---

**yahgwai** (2018-02-15):

In response to [@RoboTeddy](/u/roboteddy) initial post. It seems that the problem is that the attacker has something to gain by stopping a victim from reaching the chain. Could the channel be designed such that it was actually more expensive, ie would cost the attacker more than they could ever possibly gain from fraud, to stop an attacker reaching the chain?

For two party channels, at the point of opening a channel both participants make additional deposits - lets call them “closing deposits”.  These closing deposits would be forfeit by both participants in the case that only one participant made it to the chain - this could happen for a number of reasons. If these deposits were greater in value than the sum of the deposits made by the participants for purpose of exchange, then both parties would lose more by preventing one another from reaching the chain.

In the case of payment channels it is easy to compare the value of a closing deposit with the sum of the exchange deposits. In state channels this comparison cannot be made directly, and the value of an end state is likely subjective so participants would need to agree on high enough closing deposits before opening the channel. I’m not sure how this would work for truebit, perhaps by declaring all verifiers up front?

---

**vbuterin** (2018-02-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/yahgwai/48/759_2.png) yahgwai:

> Could the channel be designed such that it was actually more expensive, ie would cost the attacker more than they could ever possibly gain from fraud, to stop an attacker reaching the chain.

No, because there are combination attacks. Even if system A had an invariant that said “an attack that prevents challenges has a cost of at least X, and the possible gain is X, so there’s no incentive to attack”, and system B had an invariant that said “an attack that prevents challenges has a cost of at least Y, and the possible gain is Y, so there’s no incentive to attack”, because congestion attacks congest the entire chain, you can pay max(X, Y) cost to get X + Y revenue from the attack.


*(4 more replies not shown)*
