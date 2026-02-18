---
source: ethresearch
topic_id: 271
title: PoW in Casper FFG appears to be pointless
author: nootropicat
date: "2017-11-29"
category: Proof-of-Stake > Casper Basics
tags: []
url: https://ethresear.ch/t/pow-in-casper-ffg-appears-to-be-pointless/271
views: 2703
likes: 4
posts_count: 6
---

# PoW in Casper FFG appears to be pointless

My understanding from the paper:

- PoS validators determine the most valid chain at every 100th block
- validators vote on PoW blocks, they don’t generate their own
- tip after a most recent checkpoint is PoW based
- for PoW to exist there has to be a block reward

Therefore:

1.) Hostile PoW attack.

In the case of a hostile PoW attack, validators are likely to cooperate and ignore the hostile PoW chain to save the network. It only requires a relatively short period of time to bring the PoW difficulty down. After that, validators start to mine low-difficulty PoW blocks - these blocks are initially ignored by other nodes. Then they create a checkpoint, making it the most valid chain. The rest of the network forks to their chain.

2.) Profit-maximizing validators.

Validators have a strong incentive (PoW block rewards) to conspire and ignore external PoW even in the absence of an attack. Not a realistic concern due to being invested for the long-term.

In both cases ethereum functionally changes to one ‘megablock’ (divided into 100 blocks) per ~23 minutes.

What (1) means is that PoW is irrelevant to the security, what (2) means is that validators are (implicitly) assumed to not be “rational” but at least a bit friendly, which makes PoW pointless in itself.

---

**I propose a very simple alternative to PoW in FFG**. It’s not meant to be the ideal end solution, merely better than PoW while being very simple to implement. Global PoW waste is infuriating.

*I* - target PoS inflation (interest) per epoch, in percents, assuming infinite coins vote

*coins* - how many coins in total

*V_e* - ordered set (array) of active validators (accounts) for epoch *e*

*V_e.stake* - how many coins these validators have in total

*I_e* - effective inflation rate for epoch *e*

*F_e* - total gas fees for epoch *e*

(a) for every epoch *e* scale the interest rate according to the logistic function, ie:

*I_e* = *I* * sigmoid(*k* * *V_e.stake*/*coins*)

Where *k* is the scaling factor.

At every checkpoint that ends epoch *e*:

(b) Scale the deposit for all active validators:

for *v* in *V_e*: *v.stake* *= (1 + *I_e*)

(c) divide all fees from the epoch proportionally amongst all active validators according to their deposits:

for *v* in *V_e*: *v.stake* += *F_e* * *v.stake*/*V_e.stake*

Which allows a simple hash-based block generation algorithm:

Given most recent block *B*, its hash H(*B*), current unix timestamp *t* and target block time *z* (seconds), validator *i* generates a child block when:

H(*B* . *t*) % (*z**|*V_e*|) == *i*

The more valid short pseudo-PoW chain is simply the one with more blocks, or if equivalent, the one that was seen first by the node.

Intended effect of incentives:

1. No validator cabals under condition:
Due to the sigmoid scaling of a block reward in (a), existing validators happily include new validators, as long as profit from a higher interest rate is higher than loss due to fee sharing. That’s why the interest rate must be strictly monotonically increasing.
Finding the ideal scale factor k requires currently untestable assumptions about future proportion of voting coins and average fees during epoch.
With k = 3 sigmoid rises from 0.5 at 0 to 0.817 at 0.5 - or equivalently 1% and 1.63% for 2% rate in the limit - which seems reasonable as an initial value.
2. No stake grinding and similar concerns, as fees are distributed among all validators.
3. Strictly monotonically increasing interest rate creates hard to quantify positive social effects - as every staking newcomer is directly beneficial to all others. Constant interest rate - or even, worse, decreasing - makes every newcomer a loss, in addition to perverse incentives due to fees.

Possible problem:

Free riding by not generating individual blocks. It’s another consequence of the ‘profit-maximizing validators’  assumption which imo isn’t realistic. In any case, it’s a much milder outcome than possible PoW hijacking.

## Replies

**vbuterin** (2017-11-29):

> PoW in Casper FFG appears to be pointless

Yep, you get it! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

Or rather, the point of PoW in Casper FFG is that it can be easily reverted to as the primary source of consensus if the PoS breaks for whatever reason.

Hybrid PoS is intended primarily as a low-risk transition phase, giving most of the benefits of PoS with relatively little work, setting the stage for a more comprehensive full PoS implementation.

---

**nootropicat** (2017-11-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Or rather, the point of PoW in Casper FFG is that it can be easily reverted to as the primary source of consensus if the PoS breaks for whatever reason.

The only way to turn off PoS without a hard fork is to *ask* stakers to stop validating, yes? So PoW makes zero sense even in that case.

PoW is not a zero-cost conservative alternative - each day means ~100k tons of burned coal and a tremendous global opportunity cost due to used hardware and human time.

Please reconsider using some pseudo-pow solution in that light - just as a temporary solution before better PoS.

---

**Silur** (2017-11-29):

how about a VRF committe model proposed by micali, with PoW solutions as VRF seeds?

works well with the curent “verifier rotation” method and can be reverted easily with verifiers no longer accepting VRF proofs, and the network just waits for every new PoW as usual.

---

**vbuterin** (2017-12-01):

> The only way to turn off PoS without a hard fork is to ask stakers to stop validating, yes?

Wrong. You just ask client developers to run their clients with a “–follow-pow-chain” setting, which would instruct them to ignore PoS votes. Once everyone does that it doesn’t matter what stakers do.

> Please reconsider using some pseudo-pow solution in that light - just as a temporary solution before better PoS.

The problem is that any kind of pseudo-PoW solution would take a few months to a year longer to figure out, test, implement, and so that would very gravely detract from the goal of switching to hybrid PoS ASAP that would allow us to cut the tons of coal we’re burning by ~50-83%. We can do research on what “PoS done right” would look like in parallel.

---

**nootropicat** (2017-12-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Wrong. You just ask client developers to run their clients with a “–follow-pow-chain” setting, which would instruct them to ignore PoS votes. Once everyone does that it doesn’t matter what stakers do.

You described a hard fork. It doesn’t matter whether the consensus algorithm is hard coded in a compiled binary or configurable. In principle the entire consensus code could be supplied as an argument.

> The problem is that any kind of pseudo-PoW solution would take a few months to a year longer to figure out, test, implement, and so that would very gravely detract from the goal of switching to hybrid PoS ASAP that would allow us to cut the tons of coal we’re burning by ~50-83%. We can do research on what “PoS done right” would look like in parallel.

Ok, I see that your mind is set. I’m happy with any significant reduction.

However, why *only* 50-83%? Either FFG with PoW is fine which means only symbolic PoW rewards are required (like a 200x reduction!) or it has to be turned off via manual intervention, which can increase PoW rewards as well.

Miners also would have to switch their nodes to mine on the pure-PoW chain after all - it’s a full network-wide hard fork.

