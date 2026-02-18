---
source: ethresearch
topic_id: 3290
title: Casper FFG slashing condition unclarities
author: leafcutterant
date: "2018-09-09"
category: Proof-of-Stake > Casper Basics
tags: []
url: https://ethresear.ch/t/casper-ffg-slashing-condition-unclarities/3290
views: 3235
likes: 13
posts_count: 18
---

# Casper FFG slashing condition unclarities

First of all, I’m not sure if this post fits here; let me know if not.

Certain thing are unclear to me with regards to either of the Casper FFG slashing conditions.

**Condition I:**

> “…a validator must not publish two distinct votes for the same target height.”

So this is not about whether *two conflicting chains* are being validated by the same validator, only that she mustn’t validate *two blocks* of the same height, on any fork.

If I’m not mistaken, this lets a validator keep validating on two conflicting forks if she validates every  2k ^{th}  block on fork *A* and every  (2k+1)^{th}  on fork *B*. (If Condition II applies cross-fork, then modify it to  4k and  4k+2 .) Isn’t that a problem?

**Condition II:**

> …a validator must not vote within the span of its other votes.

A validator can split their stake into two smaller stakes, and pose as two separate entities. Sure, this halves her weight in one voting round, but she will still have a say, and twice as much stake colluding can get around this commandment.

1. It seems trivial, so why is this not a problem?
2. However, this does seem to lessen the effect of byzantine behavior. Why’s the span only one block? Why not increase it to 2/5/n blocks?

## Replies

**vbuterin** (2018-09-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/leafcutterant/48/3309_2.png) leafcutterant:

> If I’m not mistaken, this lets a validator keep validating on two conflicting forks if she validates every 2k^{th} block on fork A and every (2k+1)^{th} on fork B . (If Condition II applies cross-fork, then modify it to 4k and 4k+2 .) Isn’t that a problem?

No, this is not a problem. It’s supposed to be okay to flip-flop. In fact, FLP impossibility means that there’s no way to make a consensus algorithm that does *not* have the possibility of flip-flopping forever without coming to consensus. It’s only not okay to flip-flop away from something that has already been finalized (in effect, this is what the slashing conditions do).

> A validator can split their stake into two smaller stakes, and pose as two separate entities. Sure, this halves her weight in one voting round, but she will still have a say, and twice as much stake colluding can get around this commandment.

If an attacker does that, there’s no way the attacker will be able to get to 2/3 of total deposits, so it’s not usable as an attack vector.

---

**MihailoBjelic** (2018-09-10):

I think [@vbuterin](/u/vbuterin)’s answer said enough.

![](https://ethresear.ch/user_avatar/ethresear.ch/leafcutterant/48/3309_2.png) leafcutterant:

> However, this does seem to lessen the effect of byzantine behavior. Why’s the span only one block? Why not increase it to 2/5/n blocks?

I’m wondering what did you mean by this, can you please elaborate?

---

**leafcutterant** (2018-09-10):

Thank you for your answers.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> No, this is not a problem. It’s supposed to be okay to flip-flop. In fact, FLP impossibility means that there’s no way to make a consensus algorithm that does not have the possibility of flip-flopping forever without coming to consensus. It’s only not okay to flip-flop away from something that has already been finalized (in effect, this is what the slashing conditions do).

But couldn’t – and shouldn’t – flip-flopping be punished? E.g. if you serve proof to fork *A* that a validator consistently flip-flopped, she would get slashed on fork *A*, and vice versa on fork *B*. Flip-flopping looks like an alternative to equivocation (kind of maximizes profit and minimized loss while voting on conflicting histories), making it more difficult to arrive at consensus.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> If an attacker does that, there’s no way the attacker will be able to get to 2/3 of total deposits

Could you expand on the reason for this? And couldn’t they sabotage finalization just by having a cumulative 1/3 of the stake?

---

**leafcutterant** (2018-09-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> I’m wondering what did you mean by this, can you please elaborate?

Sure. If I understand Condition II correctly, a validator’s opportunities for byzantine bahavior are reduced to half by requiring that she mustn’t cast two consecutive votes (e.g. on block height n and  n+k, where k start with 1 and increments by 1). She will still be able to vote on n and n+2k). Coulldn’t we further reduce such a possibility by increasing this span (so going with  n+3k,  n+5k, …  n+m*k) without reducing security relevantly?

---

**dlubarov** (2018-09-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/leafcutterant/48/3309_2.png) leafcutterant:

> Why’s the span only one block? Why not increase it to 2/5/n blocks?

It sounds like the second rule isn’t really making sense to you intuitively? Not sure if this helps, but I would think of a vote from `s` to `t` as a conditional vote: “I vote to justify `t`, but only if `s` is already justified”. If the same voter previously voted to justify a conflicting block `r`, but `r` is older than `s`, that doesn’t matter (in terms of safety) because if `s` is justified, `r` must not have been finalized. (If `s` was justified AND `r` was finalized, we can show that at least 1/3 of voters broke the rules by voting `r -> r'` within the span of `q -> s` for some `q`.) So legal flip-flopping is harmless (and sometimes necessary); there’s no need to discourage it.

If it’s unintuitive, you could look at a BFT algorithm like Tendermint’s which is nearly equivalent, but described in different terms. They would say that when a voter votes to finalize (aka commit) a block, the voter becomes locked on that block. They can’t legally vote for anything else unless some conflicting block becomes justified (aka precommitted), at which point everyone on a conflicting fork can safely unlock, knowing that their fork must have failed at finalization since the other fork obtained a 2/3 vote.

---

**MihailoBjelic** (2018-09-10):

I’m still having a hard time understanding, sorry…

Here’s the link to the Casper FFG paper: https://arxiv.org/pdf/1710.09437.pdf, you can find the Condition II on top of page 4 and it’s fairly simple - one is not allowed to make “nested” votes (Vote 1 source < Vote 2 source < Vote 2 target < Vote 1 source). You can choose any k (2k, 3k, … , nk) to symbolize the height difference between any of these four checkpoints, the same rule applies.

---

**leafcutterant** (2018-09-10):

[@dlubarov](/u/dlubarov), then I believe I had an even greater misunderstanding: it was my impression that Condition II applies to *voting on all blocks*, not *voting on checkpoints*.

I think I understand it now, but could you give a situation where legal flip-flopping is necessary?

---

**leafcutterant** (2018-09-10):

[@MihailoBjelic](/u/mihailobjelic), thank you, it’s clearer now after I realized that it’s for checkpoints, not all blocks. Am I correct to assume that Condition II, in humanspeak means this? “A validator mustn’t pick a vote source that is lower in height than the source of her previous vote.”

---

**MihailoBjelic** (2018-09-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/leafcutterant/48/3309_2.png) leafcutterant:

> Condition II applies to voting on all blocks , not voting on checkpoints

Yes, it’s voting on checkpoints. Also, you should be aware that Casper FFG and sharding recently got merged and that changes things a bit, but that’s another topic.

![](https://ethresear.ch/user_avatar/ethresear.ch/leafcutterant/48/3309_2.png) leafcutterant:

> could you give a situation where legal flip-flopping is necessary?

[This video](https://youtu.be/uQ3IqLDf-oo?t=33m24s) should make “flip-flopping” clear for anyone (watch 10-20 mins from the point I’ve set it on). Ethereum is a distributed system, and network partitions will probably (or I should say definitely ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)) happen. During such periods, validators will not be aware of the global state (they’ll be aware of their partition only) and some of them will vote on the “wrong” chain (the chain that will get rejected once the partitions merge). The point is that you have to allow them to chose the “right side” (the wining chain) once they become aware of it.

---

**dlubarov** (2018-09-10):

Let’s say we have this checkpoint structure

```
  ,-b--c
 /
a
 \
  `-d--e
```

and `a` is justified. Say when it’s time to vote for `a -> b` or `a -> d`, and we get a 50/50 split. If nobody changed branches, we’d get another 50/50 split next time between `a -> c` and `a -> e`, and same for any future children. So some voters need to legally flip-flop in order for one branch to reach quorum (2/3 votes).

---

**MihailoBjelic** (2018-09-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/leafcutterant/48/3309_2.png) leafcutterant:

> Am I correct to assume that Condition II, in humanspeak means this? “A validator mustn’t pick a vote source that is lower in height than the source of her previous vote.”

Not quite. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14) I think the easiest way to understand this rule is to think of it as the “nested votes prohibition”, where a “nested vote” is a vote which can completely “fit in” the previous one, i.e. V1 source < V2 source < V2 target < V1 target. This figure from the FFG paper should help, too:

[![ffg](https://ethresear.ch/uploads/default/original/2X/a/ac27a0ea5eb46e30c6d67bc2ca8abe3ccd89a21d.png)ffg483×458 24 KB](https://ethresear.ch/uploads/default/ac27a0ea5eb46e30c6d67bc2ca8abe3ccd89a21d)

Can you see how vote a2-a3 can completely “fit in” the vote b2-b3? We don’t want to allow that, the figure shows why. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

As everything, it becomes incredibly simple once you understand it. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

---

**leafcutterant** (2018-09-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> network partitions will probably (or I should say definitely ) happen. During such periods, validators will not be aware of the global state (they’ll be aware of their partition only) and some of them will vote on the “wrong” chain (the chain that will get rejected once the partitions merge).

Yeah, that is clear to me.

Let’s say there is partition A and B, and a validator votes on A (because she only sees A). Then she realizes that there’s a partition B and the majority stake votes for B. She catches up by voting on B. That is understandably honest. But once she “commits” (not as in commit as a vote) to partition B, she could go back to partition A and vote there again (perhaps contributing to a super-majority link which doesn’t trigger the nested voting violation). So she voted A-B-A, and there is proof of that.

Why isn’t this undesirable/punished?

Doesn’t this contribute to the survival of network partitions? (If needed, we can assume an adversary who deliberately creates network partitions.) Why do we want to maintain her voting ability on both partitions after this?

---

**leafcutterant** (2018-09-12):

Right, thanks – now I get what the nested vote means ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Does this rule prohibit nested votes by a validator only on two different forks, or on the same fork as well?

---

**MihailoBjelic** (2018-09-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/leafcutterant/48/3309_2.png) leafcutterant:

> Let’s say there is partition A and B, and a validator votes on A (because she only sees A). Then she realizes that there’s a partition B and the majority stake votes for B. She catches up by voting on B. That is understandably honest. But once she “commits” (not as in commit as a vote) to partition B, she could go back to partition A and vote there again (perhaps contributing to a super-majority link which doesn’t trigger the nested voting violation). So she voted A-B-A, and there is proof of that.

This might not be clear enough because there are two possible scenarios here, so I’ll try to address both:

1. The validator first voted on A (vote1), then on B (vote 2), and then again on A (vote 3), but the votes 2 and 3 are not the same height, i.e. h(vote2) < h(vote3)

In this situation the validator will not be slashed (she might get a small “bleeding” penalty as described in the video I shared above), but she will not earn any reward for the vote 3, because it’s not on the winning fork (the winning fork is A and the checkpoint will be finalized on it), so the validator has no incentive to behave this way.

1. The same as no.1, but the votes 2 and 3 are the same height, i.e. h(vote2) = h(vote3)

The validator will get slashed, because this violates Condition I.

---

**leafcutterant** (2018-09-13):

Thank you! No, I was trying to interpret “nested voting” in these two different ways (pardon my *rudimentary* graphics):

[![nested](https://ethresear.ch/uploads/default/original/2X/9/98c5b561fac5dd8c9b75f2f5af2aab506ddf2d18.png)nested455×313 22.4 KB](https://ethresear.ch/uploads/default/98c5b561fac5dd8c9b75f2f5af2aab506ddf2d18)

…and find out which if the action on the left gets slashed as well. The right one obviously does.

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> but she will not earn any reward for the vote 3, because it’s not on the winning fork

Why is that? Do we assume that the winning fork’s coins will be worthless? Or is it because no rewards are paid without finalizing the epoch?

---

**djrtwo** (2018-09-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/leafcutterant/48/3309_2.png) leafcutterant:

> But couldn’t – and shouldn’t – flip-flopping be punished?

This is not punished via slashing conditions but is disincentivized via missed rewards and even a slow bleed of your deposit.

---

**MihailoBjelic** (2018-09-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/leafcutterant/48/3309_2.png) leafcutterant:

> I was trying to interpret “nested voting” in these two different ways (pardon my rudimentary graphics):
>
>
> nested455×313 22.4 KB
>
>
> …and find out which if the action on the left gets slashed as well. The right one obviously does.

The validator is slashed in both cases if I’m not mistaken, maybe [@djrtwo](/u/djrtwo) can confirm. There is no reason/explanation for a validator to vote in a way illustrated on the left.

![](https://ethresear.ch/user_avatar/ethresear.ch/leafcutterant/48/3309_2.png) leafcutterant:

> Why is that? Do we assume that the winning fork’s coins will be worthless? Or is it because no rewards are paid without finalizing the epoch?

Neither. When I say “it’s not on the winning fork” I mean “she will not get a reward because she voted for a checkpoint that will not get 2/3 votes, so no reward”.

Hope this helped. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

P.S. You can also skim through [this article](https://medium.com/coinmonks/a-simplified-look-at-ethereums-casper-4fa9461b245), it’s nice. ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=14)

P.P.S. [@dlubarov](/u/dlubarov) noticed that Condition II is stricter then necessary, and [proposed a nice tweak to fix it](https://ethresear.ch/t/casper-ffg-leniency-tweak/2286) (it passed [@vbuterin](/u/vbuterin)’s QC ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)).

