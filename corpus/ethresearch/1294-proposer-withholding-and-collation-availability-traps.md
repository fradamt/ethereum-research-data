---
source: ethresearch
topic_id: 1294
title: Proposer withholding and collation availability traps
author: JustinDrake
date: "2018-03-03"
category: Sharding
tags: [proposal-commitment, proofs-of-custody]
url: https://ethresear.ch/t/proposer-withholding-and-collation-availability-traps/1294
views: 5024
likes: 2
posts_count: 15
---

# Proposer withholding and collation availability traps

In the context of proposer-validator separation [@vbuterin](/u/vbuterin) exposed a [proposer withholding attack](https://ethresear.ch/t/proposal-confirmation-separation-a-bug-and-a-fix/1261). In an attempt to solve proposer withholding, a [proposal commitment mechanism](https://ethresear.ch/t/alternative-fix-for-proposer-withholding-attack/1268) was suggested to prevent validators from stealing collation bodies, thereby encouraging proposers to safely share their collation bodies.

By itself the commitment scheme is not sufficient because validators are incentivised to maintain “credit scores” for proposers, i.e. evaluate the likeliness of proposers not withholding their collation bodies. In this post we augment the commitment scheme with a challenge scheme to address the credit score issue.

**Construction**

We require every proposal to contain the root r of a “fine-grain” Merklelisation of the corresponding collation body. (Let B be the collation body. We partition B into 32 byte chunks B[0], ..., B[n-1] and build r by Merklelising the chunks B[i].)

We now give proposers the right to challenge validators of their own proposals. That is, a proposer can issue a transaction to the VMC challenging the validator to disclose some chunk B[i] for one of his validated proposals. The challenge passes if the validator responds (within one epoch, say) with a Merkle path from B[i] to r. The challenge fails otherwise.

If the challenge fails the validator is slashed, and half the validator’s deposit is given to the proposer.

**Discussion**

The above challenge scheme is a way to enforce validators to only include proposals to the VMC for which the corresponding collation body is available to them, thereby nullifying credit scoring. Indeed, whenever a validator includes a proposal to the VMC without downloading the collation body from the proposer this is an opportunity for the proposer to set a trap by partially withholding the collation body. Even a single 32 byte chunk withheld by the proposer is enough to slash the validator and earn the proposer a large financial return.

## Replies

**vbuterin** (2018-03-04):

What does the full protocol look like? Something like this?

1. Proposers propose headers.
2. Validator co-signs a header with the highest fee.
3. Proposer maybe publishes the body.
4. If the proposer publishes, the validator confirms. If the proposer does not publish, then the validator does not confirm, because otherwise the proposer could challenge the validator and the validator would be unable to respond, leading to a lost deposit.

If the validator does not confirm, do they still get the fee? If yes, then there seems to be no incentive to make oneself vulnerable by confirming, and if not, then validators still have an incentive to engage in credit scoring.

I suppose one approach would be that if a validator does not confirm, they get the fee but not the base reward?

---

**JustinDrake** (2018-03-04):

What I had in mind:

1. Proposers propose headers to the validator.
2. The validator commits to all headers he has seen (or at least the highest paying proposal per proposer).
3. Upon receiving the commitment, rational proposers disclose their collation body to the validator.
4. The validator co-signs and publishes to the VMC the highest paying proposal for which the collation body is available.

The fee F, the subsidy S and the total transaction fees T get paid iff the proposal published to the VMC wins.

> if not, then validators still have an incentive to engage in credit scoring

The validator does *not* get the fee and should *still not* engage in credit scoring. Imagine a “bluffing” proposer constructs a high credit score over several months with a validator by behaving perfectly. Once the credit score is high enough (say, 99%) the validator stops downloading the full collation body. At that point the proposer challenges and the validator gets slashed. In other words, the credit score needs to continuously be at 100%, i.e. credit scoring is ineffective.

---

**vbuterin** (2018-03-04):

> Once the credit score is high enough (say, 99%) the validator stops downloading the full collation body.

Aah, I think I know where I got things wrong. What I was thinking is, at the proposal selection stage the validator chooses proposers that have higher credit scores, because they are more likely to get paid. But with your approach, the validator can commit to an unlimited number of headers, so they would just take in every proposal. Makes sense.

---

**vbuterin** (2018-03-04):

We can extend the trap mechanism further: the proposer can steal not just from the validator, but from any of their next N descendants. This incentivizes a certain minimum windback value.

---

**skilesare** (2018-03-04):

What are the long term cartel implications?  If you slash me for not downloading and I have a 99% score, can I then exclude all of your proposals in the future?  Can cartels arise that, wink* check all the collations *wink.

Maybe external challengers keep them in line?

---

**MaxC** (2018-03-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> for

Is this solution saying: validators are responsible for data availability (losing stake if a collation is not available), but proposers are responsible for validity (losing the reward and their fee). And we leave the actual checking of data availability and validity to the network itself. Doing this, we can ensure the block-chain grows because the validators will not want to lose their fee in the event of unavailable data.

In that  be the case, why does a validator need to merkalise commitments: would it not be sufficient just to punish validators if the network finds that a collation body is unavailable - after a vote say which takes place every time a block is added?

**Edit:** Ah, I see - because there is no global vote on availability for efficiency reasons, when adding a block only the block proposer checks to see if data is available. If that be the case, that’s a very nice intertwining of incentives, and might mean one doesn’t even need data availability proofs.

I guess the scheme could  only break down if we assume a dishonest majority of validators, working in concert with a malicious proposer.

Or in the bribing attacker model, an attacker could flip the inceptive structure back round again, by creating a smart contract that promises money to the first validator if he gets slashed. Then a 51% stalling attack could theoretically be possible, but is still v. unlikely.

---

**JustinDrake** (2018-03-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/skilesare/48/336_2.png) skilesare:

> What are the long term cartel implications?  If you slash me for not downloading and I have a 99% score, can I then exclude all of your proposals in the future?

I don’t expect cartels to have any real impact:

- Validators should assume all proposers to be on the lookout for bad validator behaviour.
- Revenue from proposals is dwarfed by revenue from successful challenges. If the minimum deposit to become a validator is 1000 ETH then a proposer will earn a lump sum of 500 ETH for a successful challenge. So a single successful challenge is probably more than a lifetime of earnings for the typical proposer.
- If a proposer feels like his identity is tainted he can cash out and return to the proposing game with a fresh identity.

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> because there is no global vote on availability for efficiency reasons

That’s right.

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> that’s a very nice intertwining of incentives, and might mean one doesn’t even need data availability proofs.

Indeed it’s an unusual “coopetition” dynamic that I expect will significantly strengthen availability ![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=12) :

- Validators and proposers “collaborate” on collation formation
- Validators and proposers “compete” on collation availability

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> in the bribing attacker model, an attacker could flip the inceptive structure back round again, by creating a smart contract that promises money to the first validator if he gets slashed. Then a 51% stalling attack could theoretically be possible, but is still v. unlikely.

The good news here is that we can quantify the cost of a stalling attack. If the minimum deposit to become a validator is 1000 ETH then the cost of stalling is 500 ETH per period.

---

**MaxC** (2018-03-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> The good news here is that we can quantify the cost of a stalling attack. If the minimum deposit to become a validator is 1000 ETH then the cost of stalling is 500 ETH per period.

Is that not the budget an attacker needs, rather than the cost? Since if an attacker is viewing this as a repeated game rather than a one-off , he will not mind losing out 500 Eth by fooling a validator.

But yeah, similar to Bitcoin where an attacker needs a budget of 6 blocks to subvert consensus.

---

**JustinDrake** (2018-03-04):

> Is that not the budget an attacker needs, rather than the cost? Since if an attacker is viewing this as a repeated game rather than a one-off , he will not mind losing out 500 Eth by fooling a validator.

Change the game slightly to allow anyone to be a challenger (not just the proposer). Then validators can challenge themselves to receive the 500 ETH challenger reward in addition to the 1000 ETH slashing insurance from the attacker. That costs the attacker 1000 ETH per period, and validators make a profit of 500 ETH per slashing.

---

**MaxC** (2018-03-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Change the game slightly to allow anyone to be a challenger (not just the proposer). Then validators can challenge themselves to receive the 500 ETH challenger reward in addition to the 1000 ETH slashing insurance from the attacker. That costs the attacker 1000 ETH per period, and validators make a profit of 500 ETH per slashing.

That seems much stronger.  Difficult to see this scheme being attacked. The only way I could see it is if the proposer bribed the validator to withhold the data they have. I don’t see that as being very likely because once an attacker has paid him, the validator can do what he likes with the data… unless the proposer gave the validator 99% of the data but could use the 1%  to slash the validator’s balance.

---

**nate** (2018-03-09):

> The challenge passes if the validator responds (within one epoch, say) with a Merkle path from
> B[i] to r.

Based on a brief conversation today, it may make sense to extend the valid response time to be as long as it can reasonably be.

The logic here is that if the response period is short (and punishments are high), it’s very easy for miners (or validators, in full PoS) to censor the response txs unless they receive a payment from the validator who was challenged. A shorter response period makes this censorship attack easier, and higher punishments make it more profitable (assuming validators pay up to the amount they were going to be slashed).

Even though the security assumptions of phase 1 include an honest majority assumption, we don’t seem to lose anything by extending the response period to as long as it can reasonably be (unless I’m missing something) - so it seems like a reasonable thing to do.

---

**vbuterin** (2018-03-10):

Agree; I was thinking the period should be something like 2 months or longer; the same as the Casper withdrawal period.

---

**nate** (2018-03-12):

One thing I’m not totally clear on is what other validators should actually do in the case of an outstanding challenge - especially with long challenge times.

Let’s say there is some collation (farther back than the windback) that has an outstanding challenge. If we require future validators to download this collation with to check it’s availability, this sounds like it would introduce a fair bit of extra overhead (+ possible DoS vector), especially if a challenge can be outstanding for 2 months. If we don’t require validators to download this, then it seems we can end up with a sharded chain with unavailable collations.

It’s possible this isn’t a concern, with the current security assumptions; if the collation wasn’t available, then the validators who checked that collation’s availability in their windback wouldn’t have built on top of it…

---

**vbuterin** (2018-03-12):

My understanding is that validators can be made only responsible for the availability of the 25 collations that are immediate ancestors of their own (plus of course their own collation itself); so they can simply store this data until the challenge period runs out.

