---
source: magicians
topic_id: 3177
title: Finality gadget for Ethereum1x Working Group
author: AlexeyAkhunov
date: "2019-04-23"
category: Working Groups > Ethereum 1.x Ring
tags: [eth1x, finality]
url: https://ethereum-magicians.org/t/finality-gadget-for-ethereum1x-working-group/3177
views: 8792
likes: 67
posts_count: 54
---

# Finality gadget for Ethereum1x Working Group

This is to discuss the idea of launching this working group, and also for people who are interested in working on this to check in.

Note that the group has not formed yet, but I expect it to happen fairly soon.

Now the videos are up, here is my short kick-off [presentation](https://youtu.be/HaT-BIzWSew?t=24502)

And here are the slides: https://drive.google.com/file/d/16KLZKAutK79NxMh8L7B6hpNKuoOaAPZT/view

## Replies

**fubuloubu** (2019-04-23):

Very cool! I think this would go a long way towards demonstrating the power and robustness of the PoS mechanism.

It may or may not be obvious, but it seems this comes in two stages:

1. Beacon chain does sufficiently well finalizing “ETH 1x data” for a given amount of time (how much time? 3 mos? 6 mos?)
2. Beacon chain’s block finalizations are integrated somehow into consensus of ETH 1x chain (hard or soft fork? maybe in the mining software to reduce uncles? can we revert/reduce the effects if it doesn’t work?)

I think it’s important here to gradually incorporate this mechanism over time as it proves itself to work. We have to de-risk this combination enough in practice that it doesn’t get abused when vulnerabilities are discovered that we didn’t know about (“when” not “if”)

Also, is step 1. needed to process deposits?

---

Edit: I guess I’m saying I would like to be involved haha

---

**terence** (2019-04-23):

I’d love to be involved. A little back ground for myself, I’ve been working and researching ETH2 just over a year. Here’s something I’m looking to implement in my spare time: https://github.com/ethereum/eth2.0-specs/tree/dev/specs/light_client (Besides working on beacon chain ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=9) )

---

**poemm** (2019-04-23):

First a summary, then feedback.

A summary in my own words: Originally, it was proposed that a PoS-based gadget would finalize the PoW chain. In June 2018, this plan was abandoned in favor of Eth2. In December 2018, it was [proposed](https://ethresear.ch/t/using-the-beacon-chain-to-pos-finalize-the-ethereum-1-0-chain/4521) to salvage the original finality gadget plans – Eth2 clients must be aware of recent Eth1 block hashes to decide on Eth1 to Eth2 validator deposits, but deciding on validator deposits may be interpreted as Casper votes, which may finalize the Eth1 chain. For this to work, Eth1 clients would have to change their fork-choice rule to monitor the beacon chain, perhaps as an [Eth2 light client](https://ethereum-magicians.org/t/eth2-in-eth1-light-clients/2880), so that they can honor the finalization of blocks.

Feedback: I believe that an earlier plan was to replace PoW with full PoS, not just finality. Of course, finalization alone brings great value and should be considered alone. But perhaps it would be wise to also consider further steps to replace PoW with PoS. This would solve the ASIC miner centralization problem, and allow reducing block rewards significantly.

---

**boris** (2019-04-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poemm/48/1340_2.png) poemm:

> Feedback: I believe that an earlier plan was to replace PoW with full PoS, not just finality. Of course, finalization alone brings great value and should be considered alone. But perhaps it would be wise to also consider further steps to replace PoW with PoS. This would solve the ASIC miner centralization problem, and allow reducing block rewards significantly.

This is a way to make use of the ETH2 beacon chain on ETH1. The plan for ETH2 is still full PoS.

---

**poemm** (2019-04-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> This is a way to make use of the ETH2 beacon chain on ETH1. The plan for ETH2 is still full PoS.

I proposed that we also consider full PoS on Eth1.

---

**AlexeyAkhunov** (2019-04-23):

Thanks to people who already checked in and started the discussion. To make it more interesting, I would like someone to answer the first open questions (by studying the beacon chain specification and confirming or refuting my own answers) that I mentioned in the presentation:

1. Is it possible for Beacon Chain block proposers to never agree on the eth1 block (i.e. to never produce at least 513 out of 1024 “votes”)? My answer is YES
2. Do Beacon Chain block proposers have an incentive to never agree on the eth1 block? My answer is YES

Change my mind ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**terence** (2019-04-23):

1.) Yes

2.) Yes, but I was under the impression by doing so beacon chain won’t reach finality and the proposers and validators will lose out on reward and even more $$ when quadratic leaks kick in.

I raised a concern a while back about there’s an incentive for proposer to stall on eth1 deposit: https://github.com/ethereum/eth2.0-specs/issues/539

then it was addressed here: https://github.com/ethereum/eth2.0-specs/pull/758

---

**poemm** (2019-04-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> Is it possible for Beacon Chain block proposers to never agree on the eth1 block (i.e. to never produce at least 513 out of 1024 “votes”)? My answer is YES
> Do Beacon Chain block proposers have an incentive to never agree on the eth1 block? My answer is YES

1. It is unclear what “agree on the eth1 block” means. If you consider that a vote on a block is also a vote on all earlier blocks, then a random sample from a population which includes a 2/3rds honest majority (which Eth2 assumes) will “agree” on at least the genesis block with high probability.
2. Sure, as you explained in your linked talk, beacon chain block proposers may have incentive to prevent new validators. Your and @terence 's proposed economic incentives are a reasonable solution to this problem.

---

**fubuloubu** (2019-04-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> Is it possible for Beacon Chain block proposers to never agree on the eth1 block (i.e. to never produce at least 513 out of 1024 “votes”)? My answer is YES
> Do Beacon Chain block proposers have an incentive to never agree on the eth1 block? My answer is YES

Spot on. There must be some built-in incentive to ensure this bridge connection is strongly maintained in both directions (ETH 1->2 deposits, and ETH 2->1 finality). It’s essentially a bit of an oracle problem unless we graft an ETH 1 light client into the ETH 2 protocol (which will not be sustainable long-term), and a ETH 2 light client into the ETH 1 protocol. I’m more in favor of a “lighter” approach in this regard, perhaps something like the bonding for ETH 2 Validators is “temporary” (i.e. set from ETH 1 deposit contract, but not used to run what will later be the ETH 2 “main net”), and have that feed back as an extension to miners to have reduced uncle rates or something else beneficial without grafting it to the ETH 1 protocol directly.

---

**terence** (2019-04-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> There must be some built-in incentive to ensure this bridge connection is strongly maintained in both directions

Do you think the current beacon chain spec has this built-in incentive in place?

---

**fubuloubu** (2019-04-24):

I’m not sure it’s the proper place. It’s a little bit higher level than that (the “why”, not the “how” the spec provides us). I think it seems complete enough, basically we can place the ETH 1 light client code in the beacon chain and process deposits directly in the protocol. [@AlexeyAkhunov](/u/alexeyakhunov) is right though there may be a dis-incentive for ETH 2 Validators to process them, but it works at a small scale by optimistically assuming Validators won’t try to cheat. I think working through the incentive model a bit may definitely be called for.

---

**AlexeyAkhunov** (2019-04-24):

Thanks everyone who joined the initial warm-up discussion. Now to the mechanics of the group formation. I do not create working groups for living, but my intuition and experience from other WGs in Ethereum 1x so far tell me that for a WG to be active and successful, it needs a leader who properly dedicates time to the work (ideally full-time, but at least 50% time I would say), and then perhaps some more dedicated people.

To preempt the questions about funding, I would say that if we found a suitable leader (not necessarily an expert in beacon chain) initially, and perhaps some more people to help out, a decent funding would be provided.

Other working groups would participate in work reviews (we will be regularly talking to each other and review each other’s work, as it is necessary to come up with consistent roadmaps), and if a group becomes inactive, we should fold the group (with funding going away obviously), and allow a new group to form.

If you want, please DM me (or post here if you are comfortable with it), how much of your time you would dedicate to the group (provided that this time will be paid), and how confident you are about becoming the leader.

---

**djrtwo** (2019-04-26):

Hi! Just wanted to let y’all know I’m glad to be involved with this working group but cannot take the “lead” at the moment. I am very pro this initiative, so excited to see it get some momentum ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**MadeofTin** (2019-04-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> Spot on. There must be some built-in incentive to ensure this bridge connection is strongly maintained in both directions (ETH 1->2 deposits, and ETH 2->1 finality). It’s essentially a bit of an oracle problem unless we graft an ETH 1 light client into the ETH 2 protocol (which will not be sustainable long-term), and a ETH 2 light client into the ETH 1 protocol.

I am going to ask the dumb question. Why does there need to be a bridge with separate tokens? Can’t miners receive a block reward and proposers receive a finalizing reward all using the same ETH?

I went back and rewatched the presentation and can see the beacon chain is happening separately to the PoW. It makes sense that the validators have their mechanism for reaching consensus between themselves outside of the main chain. It also makes sense if more is happening on the beacon chain (i.e., full proof of stake) that value is exchanged throughout those blocks. But, in the case where the beacon chain’s sole purpose is to finalize the main chain, can’t we reduce complexity under that assumption? Things like balances would not need to change. This simplification may also be an answer to Alexey’s proposed problem of encouraging agreement on an Eth1.X block if proposers are unable to get paid until they do so.

---

**fubuloubu** (2019-04-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/madeoftin/48/1969_2.png) MadeofTin:

> I am going to ask the dumb question. Why does there need to be a bridge with separate tokens? Can’t miners receive a block reward and proposers receive a finalizing reward all using the same ETH?

Because we’re dealing with two separate chains. There are ways to mix the two together more deeply than what a bridge mechanism usually implies, since we may be able to make protocol changes at later stages, but we can’t change the fact that they’re two separate chains with two separate (but interrelated!) tokens.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/madeoftin/48/1969_2.png) MadeofTin:

> But, in the case where the beacon chain’s sole purpose is to finalize the main chain, can’t we reduce complexity under that assumption? Things like balances would not need to change. This simplification may also be an answer to Alexey’s proposed problem of encouraging agreement on an Eth1.X block if proposers are unable to get paid until they do so.

There’s a fundamental question here of what the Beacon chain *should* do when we make this upgrade. Shall it live forever in this role, and later Phases end up with their own testnets as the ETH 2.0 roadmap moves forward? Is this the first “release” of the ETH 2.0 chain, that will be there forever and ever?

By integrating things too closely too early, we might bind our hands to future upgrades, which is something I don’t think we should do. I think we should identify the requirements and constraints we have, as well as the minimum goals we seek to achieve with this project.

---

**cyberbono3** (2019-04-29):

Hi. I am excited to contribute to this project part time.

---

**ralexstokes** (2019-04-30):

[@AlexeyAkhunov](/u/alexeyakhunov) i’m keen to lead the efforts here… i’m involved w/ eth2.0 and have enjoyed seeing this idea develop. been looking for a way to help out w/ eth1.x and this seems like a good point to jump in ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) i’ll message you directly to discuss further

---

**AlexeyAkhunov** (2019-04-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png) ralexstokes:

> i’ll message you directly to discuss further

Please do, and thank you for checking in!

---

**lrettig** (2019-05-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> we can’t change the fact that they’re two separate chains with two separate (but interrelated!) tokens

Depends how you define “different tokens.” If they can be moved bidirectionally, and further, the two chains have similar security guarantees, then in practice they should be fungible and function like a single logical token.

---

**fubuloubu** (2019-05-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> If they can be moved bidirectionally

We should discuss this as a requirement. My current understanding is that the bridge might only work uni-directionally, but there are benefits to allowing a bi-directional bridge.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> further, the two chains have similar security guarantees

I’m not sure how this follows, but I suppose in the hybrid case where both are securing each other, this might be true.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Depends how you define “different tokens”… they should be fungible and function like a single logical token.

The crux of this being true depends on the bridge mechanism and issuance. I would say they are only “fungible” if 1 ETH = 1 bETH (sorry, but we need something to call the ETH 2.0 token). This probably means that there shouldn’t be any issuance on the Beacon chain until we decide the mechanism can support hybrid operation, and then we split the issuance between mining rewards and validator rewards. But, if we do that, it means there is no economic incentive to become a validator on the beacon chain (there’s probably social incentives). I think in practice, we have to have some economic incentive, but this should be artificially limited to our level of trust of the hybrid model.

It’s unfortunately much more complicated than “1 ETH = 1 bETH”. The closer we tie these tokens together, the more we have to legitimize our decision and ensure the issuance is moved from a legitimate source. If we create more issuance out of no where, that’s a problem.

The alternative is to just create a separate chain and supply of tokens, but have an in-protocol exchange mechanism that derives the price. This would be a much more fluid mechanism, and we wouldn’t have to be held to “1 ETH = 1 bETH”. This probably has its own complications as well. Think of it as a continuous ICO model where all the ETH is refundable at any time (like a DAICO).


*(33 more replies not shown)*
