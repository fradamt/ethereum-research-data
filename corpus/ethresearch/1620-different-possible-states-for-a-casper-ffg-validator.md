---
source: ethresearch
topic_id: 1620
title: Different possible states for a Casper FFG validator
author: jacob-eliosoff
date: "2018-04-05"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/different-possible-states-for-a-casper-ffg-validator/1620
views: 1700
likes: 6
posts_count: 13
---

# Different possible states for a Casper FFG validator

Is this a reasonable breakdown of possible validator states (in Casper FFG):

1. In the validator set (for this epoch), and actively voting each round (ie, on each block)
2. In the validator set, but currently not voting, eg, lost connection (and therefore supposed to gradually lose “voting weight”?  But i don’t see this in the code below)
3. Not in the validator set: “logged out”, but hasn’t yet withdrawn deposit so can still log back in (how?) & resume voting
4. Not in the validator set: already withdrew deposit, can no longer rejoin

About #3, I couldn’t make out how to “log back in” in https://github.com/ethereum/casper/blob/master/casper/contracts/simple_casper.v.py.  There’s a logout(), but no login() - the comment for logout() says “Log in or log out from the validator set”…

## Replies

**vbuterin** (2018-04-06):

> But i don’t see this in the code below

Offline validators “leak” deposits through the `deposit_scale_factor` going down.

> Not in the validator set: “logged out”, but hasn’t yet withdrawn deposit so can still log back in (how?) & resume voting

There’s no ability to “log back in” right now.

---

**jacob-eliosoff** (2018-04-06):

Got it, thanks.

```
# Reward if finalized at least in the last two epochs
```

Possibly stupid question: does this mean it’s possible for a validator to only be voting once per two epochs (ie, voting on one block per 200 blocks?), and still avoid getting inactivity-leak penalized?  (Though the block it voted on would need to get enough other votes as well, that it gets finalized?)

---

**vbuterin** (2018-04-06):

No. Notice that the last finalized epoch is two blocks ago only if every epoch is justified, as it normally takes two epochs to finalize. Some degree of leaking starts after even a single epoch fails to justify.

---

**jacob-eliosoff** (2018-04-06):

OK, so no skipping epochs allowed, fair enough.  But looking ahead to pure-PoS (let’s say FFG) world, and supposing epochs are still 100 blocks, does my validator need to vote on one (finalized) block per epoch - that is, one per 100 blocks total?  Or if I vote on say 90/100, am I getting penalized for the 10 I skipped.

---

**vbuterin** (2018-04-07):

> Or if I vote on say 90/100, am I getting penalized for the 10 I skipped.

You’re always penalized for epochs you skip, but if the rest of the voters are functioning normally then a penalty will only have about the same size as one reward, so you get rewarded on net if you’re online more than 50% of the time.

---

**jacob-eliosoff** (2018-04-07):

I think what’s confusing me is, finalization happens once per epoch, right?  So in a pure-PoS world, are there:

a) 100 blocks per epoch (“[Every 100th block](https://medium.com/@VitalikButerin/minimal-slashing-conditions-20f0b500fc6c) could be a kind of checkpoint”…), with validators only voting (directly) on one of them?  Or,

b) 1 block per epoch - validators vote on every single block?

I was assuming a), which seems to mean a validator only technically need to be online once per 100 blocks.  But maybe I was confused and it’s b), in which case every single block you neglect to vote on costs you a little.

---

**jacob-eliosoff** (2018-04-07):

Again, apologies if these are dumb questions, if there’s a source I can read to inform myself, just point me at it!

---

**beneficial02** (2018-04-07):

Though it is hybrid PoW/PoS, according to [Karl’s slide(slide 56~, 103~)](https://docs.google.com/presentation/d/16zJtDZHWDeNtFQpASxFrTuRa5Io3yGpXrZZ0GubMeUM/mobilepresent?slide=id.g29703948a2_0_2075), it seems validators vote only once per epoch(once per 100 blocks). But I’m noob for casper so please correct me if I’m wrong.

---

**jacob-eliosoff** (2018-04-07):

I’d still love to hear an authoritative answer to my 100-vs-1 question but meanwhile - hadn’t seen Karl’s slides, thanks!

---

**liangcc** (2018-04-08):

a) 100 blocks per epoch. that 100 is parameterizable, you can use some other numbers too, say, 50.

see implementation guide for more https://github.com/ethereum/casper/blob/master/IMPLEMENTATION.md

---

**jacob-eliosoff** (2018-04-08):

So then again, coming back to my original question: if there are 100 blocks per epoch, only one of which is directly finalized, is it true that a validator only needs to vote on 1 block per 100 (ie, be online ~1% of the time) in order to avoid inactivity-leak penalization?

---

**vbuterin** (2018-04-09):

If consistently coming online and voting once every 15 minutes counts as being online 1% of the time, then sure, a validator only needs to be online 1% of the time.

