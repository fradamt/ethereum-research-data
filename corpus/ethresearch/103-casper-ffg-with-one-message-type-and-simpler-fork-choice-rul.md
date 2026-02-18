---
source: ethresearch
topic_id: 103
title: Casper FFG with one message type, and simpler fork choice rule
author: vbuterin_old
date: "2017-09-29"
category: Proof-of-Stake > Casper Basics
tags: []
url: https://ethresear.ch/t/casper-ffg-with-one-message-type-and-simpler-fork-choice-rule/103
views: 16403
likes: 17
posts_count: 50
---

# Casper FFG with one message type, and simpler fork choice rule

As it turns out, we can reduce the number of message types in Casper the Friendly Finality Gadget from two (prepares and commits) to just one (“votes”), increasing the algorithm’s simplicity to something which is arguably no longer *that* much more complex than, say, Nakamoto PoW.

A vote has three parameters:

- Epoch number
- Checkpoint hash
- Epoch source (MUST BE less than epoch number)

The two slashing conditions are as follows, using the notation (e1, h1, s1) or one prepare and (e2, h2, s2) for the second prepare. If a validator sends two prepares that satisfy either of these, they can lose their deposit.

- NO_DBL_VOTE: e1 = e2
- NO_SURROUND: e1 > e2 > s2 > s1

Alternatively, this can be expressed as one three-clause condition (thanks Virgil for the suggestion!):

```auto
def is_slashable(vote1, vote2):
    if vote1.epoch > vote2.epoch:
        return vote1.source  vote2.source
    else:
        return True
```

NO_DBL_VOTE can be expressed in English as “don’t contradict yourself within the same round”, and NO_SURROUND can be expressed as a prohibition against forgetting. That is, if you first vote (e1, s1), then later (e2, s2) (the epoch counter being an implicit clock, so we can assume e2 > e1), then it really should be the case that s2 >= s1, as otherwise you’re pretending not to know about s1, which you’ve already proven earlier that you know about).

We define a checkpoint as “justified” as follows:

- The genesis is justified.
- If a chain has accepted votes from 2/3 of validators for some checkpoint C that all use as a source the same ancestor C’, and C’ is justified, then C is justified

Note that in an actual implementation, the Casper smart contract only needs to keep track of votes within its own chain; this check can be done on the hash of C, and if that passes then the epoch source uniquely identifies C’; this is why we no longer need (and in fact never needed) to specify the source hash.

We define a checkpoint as “finalized” as follows:

- The genesis is finalized.
- If a checkpoint (i) is justified, (ii) has a direct child C’ that is justified, and (iii) the votes justifying C’ use C as a source, then C is finalized.

Here’s the safety proof:

Suppose that two conflicting checkpoints C1 and C2 are finalized, and suppose e2 > e1 without loss of generality (if e2 = e1, then there is trivially an intersection of 1/3 of validators who voted for C2 and C1, which can be slashed with NO_DBL_VOTE). Consider the *justification chain* (ie. the chain of justified epochs along the chain from GENESIS to e2),  e2, e2’, e2’’, e2’’’ … e2*, e2** … GENESIS, where e2** is the first item in the chain that is <= e1 and e2* the epoch justified with e2** as its source. Note that e2* >= e1+1 by definition. There are two cases:

- e2** = e1. Then, 1/3 get slashed with NO_DBL_VOTE
- e2* = e1+1. Then, 1/3 get slashed with NO_DBL_VOTE
- e2**  e1+1. so there are 2/3 votes for (e2* > e1+1, e2** < e1). There are also 2/3 votes for (e1+1, e1). Hence, 1/3 are slashed by NO_SURROUND

Plausible liveness proof (can finalize new blocks assuming 2/3 compliant validators who do not use a non-justified checkpoint as an epoch source):

Let M1 be the highest justified epoch, and M2 be the highest epoch that anyone has prepared on. By the assumption, no one has made any prepares with epoch source higher than M1. Hence, 2/3 votes with epoch M3 > M2 and epoch source = M1 do not violate NO_DBL_VOTE or NO_SURROUND. Then another 2/3 votes on epoch M3 + 1 can finalize epoch M3.

We can also introduce a *correct by construction fork choice rule*: always choose the longest chain on top of the highest-epoch-number justified checkpoint. This is correct by construction because it follows along the logic of the liveness proof, which precisely states that attempting to finalize new checkpoints on top of the highest-epoch-number justified checkpoint is how new checkpoints can always be successfully finalized.

Note that a situation where C1 is finalized and C2, a non-descendant of C1 with a higher epoch number, is justified is impossible, and this can be proven with the same argument as the above safety proof. Hence, if we accept a 2/3 honest majority assumption, simply accepting the highest-epoch-number justified checkpoint actually works. If we do not accept such an assumption, then the simplest correction is to refuse to revert finalized blocks (note that this is time-dependent in that it will lead to permanent divergence if 1/3 equivocation does happen, but this is unavoidable).

## Replies

**nate** (2017-09-30):

Hey, this is super cool!

So if I were to try to summarize the difference between this and the previous version of the FFG, would it be fair to say: votes on some future epoch, if they use this (justified) epoch as the source, finalize this epoch?

Question about a condition for finality - one is that the checkpoint has a *direct* child C’ that is justified. What is a “direct” child? It seems like this should mean some descendant, and not that C’ has to be the very-next epoch after C (and then we lose interwoven consensus), but want to make sure I’m understanding “direct” properly.

Also, is there a small typo in the plausible liveness proof?

> Then another 2/3 votes on epoch M3 + 1 can finalize epoch N.

It seems like 2/3 votes on M3 + 1 would finalize M3 (since M3 has 2/3 votes and is thus justified) - and I’m not sure I see epoch N anywhere else ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

(As a side note, ![:heart_eyes:](https://ethresear.ch/images/emoji/facebook_messenger/heart_eyes.png?v=12) for the CBC fork choice rule.)

How does this change safety under dynamic validator sets? The same tactic of having the old/new validator sets “handshake” (finalize some epoch together) seems like it would work still. So now the old validators justify some epoch N w/ 2/3 votes (where the validator set changes starts in this epoch), then the old + new both justify some future epoch N1 (with N as source, to finalize N), and then the validator set rotation takes place after this?

---

**vbuterin_old** (2017-09-30):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/n/e95f7d/48.png) nate:

> So if I were to try to summarize the difference between this and the previous version of the FFG, would it be fair to say: votes on some future epoch, if they use this (justified) epoch as the source, finalize this epoch?

I think the best way to summarize the difference is roughly: new-style votes in epoch N are simultaneously prepares for epoch N and commits for epoch N-1.

> What is a “direct” child

It means that it has to be the very next epoch.

> How does this change safety under dynamic validator sets?

Same rules should apply. Dynasty counter increments when a checkpoint is finalized, and “2/3 votes” means “some set of validators which is both a superset of some 2/3 of the current dynasty and a superset of some 2/3 of the previous dynasty”.

---

**nate** (2017-09-30):

Cool - thanks for the info.

> It means that it has to be the very next epoch.

Ah, got it. So we can still have “interwoven” consensus - but for finality, we need two justified epochs in a row (with the votes on the second using first as source). There isn’t this in-a-row requirement for justified checkpoints, though (what I missed b4 ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) ).

---

**drcode** (2017-10-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> NO_DBL_VOTE: e1 = s1

Was this supposed to be `e1 = e2`? (Sorry if I’m missing some subtelty)

---

**vbuterin_old** (2017-10-01):

> Was this supposed to be e1 = e2? (Sorry if I’m missing some subtelty)

Yep! Fixed.

---

**cosurgi** (2017-10-02):

The sentence “Alternatively, this can be expressed as one three-clause condition” strictly speaking is false. This is because this three-clause condition will not catch a situation in which:

e2 <= s2

It only catches that ( (e1 > e2) and (s2 > s1) ) or ( (e2 > e1) and (s1 > s2) ) or (e1==e2)

but it completely ignores the relation between e2 and s2 in e1 > e2 > s2 > s1.

E.g. a situation in which e2==s2, and does not check whether e2<s2

---

**vbuterin_old** (2017-10-03):

Ah sorry, it should be implied that for a valid vote, e > s. I’ll clarify that.

---

**yhirai** (2017-10-05):

> e2** = e1-1. Then, 1/3 get slashed with NO_DBL_VOTE

Why is this?  C1 is at e1, and the child of C1 is at e1 + 1.  Is there anything at e1 - 1?

Also, we don’t know if e2** is finalized.

---

**yhirai** (2017-10-05):

How is this kind of fork prevented?

[![image](https://ethresear.ch/uploads/default/optimized/1X/82bf7e7bac6726c87ca6d9030f9d754d1f539feb_2_690x408.jpg)maybe_fork.jpg1557×921 241 KB](https://ethresear.ch/uploads/default/82bf7e7bac6726c87ca6d9030f9d754d1f539feb)

---

**asdf_deprecated** (2017-10-05):

At least 1/3 of validators are violating the NO_SURROUND condition - the GENESIS-to-C2 votes surround C1-to-C1+1

---

**yhirai** (2017-10-05):

I’m getting the game now.  It seems, if I vote on C1’ based on C1, I cannot extend any other branch over that epoch.  That’s the hidden commit.

---

**asdf_deprecated** (2017-10-06):

I might be misunderstanding something, but I think it’s possible for conflicting blocks to be finalized without punishment if the two forks have the following votes (all from 2/3 of validators):

- {sourceEpoch: 0, epoch: 1, hash: left1}
- {sourceEpoch: 1, epoch: 3, hash: left3}
- {sourceEpoch: 0, epoch: 2, hash: right2}
- {sourceEpoch: 2, epoch: 4, hash: right4}

`left` hashes are for one fork, `right` hashes for the other. Epoch 1 will have `left1` finalized, and Epoch 2 will have `right2` finalized, but `right2` doesn’t build off of `left1`.

`NO_DBL_VOTE` is satisfied because each epoch has a unique hash. `NO_SURROUND` is also satisfied - the votes for epochs 2, 3, and 4 can’t be surrounded because there’s no other votes with a larger `epoch - sourceEpoch` value, and the `{sourceEpoch: 0, epoch: 1}` vote isn’t surrounded because there’s no vote with `sourceEpoch < 0`.

**Why doesn’t the safety proof work?**

> Suppose that two conflicting checkpoints C1 and C2 are finalized, and suppose e2 > e1 without loss of generality… Consider the justification chain (ie. the chain of justified epochs along the chain from GENESIS to e2), e2, e2’, e2’’, e2’’’ … e2*, e2** … GENESIS, where e2** is the first item in the chain that is = e1 by definition. There are two cases:
>
>
> e2** = e1-1. Then, 1/3 get slashed with NO_DBL_VOTE
> e2* = e1. Then, 1/3 get slashed with NO_DBL_VOTE
> e2**  e1. so there are 2/3 votes for (e2* > e1, e2** < e1-1). There are also 2/3 votes for (e1, e1-1). Hence, 1/3 are slashed by NO_SURROUND

In this case, `e2 = 2` and `e1 = 1`, so `e2** = 0` and `e2* = e2 = 2`. `e2** = e1 - 1 = 0`, but `NO_DBL_VOTE` isn’t violated because the votes with `sourceEpoch = 0` target different epochs.

---

**asdf_deprecated** (2017-10-06):

Maybe the `NO_SURROUND` condition could be extended to treat chains of votes as single votes. Then the chain of votes from Epoch 0 to Epoch 4 (hash `right4`) would surround the vote from Epoch 1 to Epoch 3 (hash `left3`). Validators who voted for both `1 -> 3` and `2 -> 4` would be slashed, but the `0 -> 2` voters wouldn’t be (it’s not their fault).

**Safety**

Suppose there are 2 conflicting finalized checkpoints at epochs `e1` and `e2`, with `e2 > e1`. In the chain of checkpoints from genesis to `e2`, there must be a highest checkpoint with epoch `e2** < e1`, and its immediate successor with epoch `e2* >= e1`.

- e2* = e1: violates NO_DBL_VOTE
- e2* > e1: e1 is finalized by definition, and e2* is finalized because it is an ancestor of the finalized epoch e2. That means 2/3 of validators voted for a successor of e1 - call it (e1)+. There’s 2/3 votes e1 -> (e1)+, and there’s also a chain of 2/3 votes from e2** to (e2*)+ (a successor of e2*). Now there’s 3 possibilities:

(e2*)+ > (e1)+: the chain of votes from e2** -> (e2*)+ surrounds e1 -> (e1)+
- (e2*)+ = (e1)+: NO_DBL_VOTE is violated
- (e2*)+  (e1)+ surrounds the vote e2* -> (e2*)+, because in this case e2* > e1 and (e2*)+

**Plausible liveness**

As far as I can tell, Vitalik’s proof works without modification. `M1 -> M3` is a single vote, not a chain of votes, so the stricter `NO_SURROUND` condition shouldn’t cause problems.

**Open questions**

- If Chain A has a sequence of votes surrounding a vote in Chain B, how can Chain B’s validators confirm this without downloading all of Chain A?

My guess: if Chain B’s validators are “reasonable” and don’t skip a large number of epochs, they’ll only have to download a few blocks of Chain A before finding a slashing condition violation. For example, if every epoch in Chain B is justified, B’s validators need to download a max of 3 epochs from A to find a chain that surrounds B’s votes.

---

**vbuterin_old** (2017-10-06):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/a/848f3c/48.png) asdf_deprecated:

> I might be misunderstanding something, but I think it’s possible for conflicting blocks to be finalized without punishment if the two forks have the following votes (all from 2/3 of validators):
>
>
> {sourceEpoch: 0, epoch: 1, hash: left1}
> {sourceEpoch: 1, epoch: 3, hash: left3}
> {sourceEpoch: 0, epoch: 2, hash: right2}
> {sourceEpoch: 2, epoch: 4, hash: right4}

You are correct that nobody gets slashed here. But where this example is incorrect is that, except for the hash of epoch 0, **nothing was finalized**. Finalization requires 2/3 votes between two *consecutive* epochs.

---

**vbuterin_old** (2017-10-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/yhirai/48/153_2.png) yhirai:

> How is this kind of fork prevented?

The arrow from genesis to C2 and the arrow from C1 to its child conflict due to NO_SURROUND.

> Why is this? C1 is at e1, and the child of C1 is at e1 + 1. Is there anything at e1 - 1?

Ah, I think I wrote the original post wrong. Fixed now.

---

**asdf_deprecated** (2017-10-06):

You’re right, I got confused by “direct child” ![:frowning:](https://ethresear.ch/images/emoji/facebook_messenger/frowning.png?v=9)

The proof makes a lot more sense to me now:

- If two finalized chains conflict, one of them must be shorter (or no-double-vote is already violated)
- The shorter chain will have 2 consecutive justified epochs that conflict with the longer chain’s
- The longer chain either needs to “jump over” those, violating the surround condition, or collide with them, violating no-double-vote
- The finalized & next justified epochs must be consecutive, or else the longer chain could hop in between them and no one would get slashed

---

**yhirai** (2017-10-06):

Here is a safety proof in Isabelle/HOL https://github.com/pirapira/pos/blob/master/CasperOneMessage.thy#L424

---

**virgil** (2017-10-09):

Subject: Casper FFG with one message type.  Keep source hash?

There are currently two designs for the “Vote” message in Casper.  They are:

[![40](https://ethresear.ch/uploads/default/original/1X/dbd0d11b27a1df948eb47c198a3e9201d29aa4f4.png)40476×322 49.9 KB](https://ethresear.ch/uploads/default/dbd0d11b27a1df948eb47c198a3e9201d29aa4f4)

My understanding of the benefit of the Vote message with only three parts (the lower one) is simply that, “it uses less space”.  Space efficiency is good, so in principle, ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=14) .

However, given that the checkpoint-tree is an [Arborescent](https://en.wikipedia.org/wiki/Arborescence_(graph_theory)) tree, we could simplify this even further by simplying specifying the source and target checkpoint hashes.  Validators can then compute the length (epoch/checkpoint depth) of the source and target checkpoints on the fly, and cache any results.

I mentioned this to Vitalik, and his response was roughly: “Keeping tracking of depths of the source and target of every supermajority link, for every validator, is too high a memory burden for detecting slashing condition violations.”  This makes a lot of intuitive sense.  But with a mind for greater efficiency, my question becomes:

*How necessary is it that every validator immediately know when a slashing condition has been violated (before the evidence transaction)?  Because if a validator merely needs to update when it learns slashing condition evidence—then we can further reduce the size of the vote message to simply the two hashs (or alternatively, the epoch-depth of the source checkpoint, and the hash of the target checkpoint).*

---

**vbuterin_old** (2017-10-09):

Branch A does not know what the hashes are in branch B (and vice versa), and it would be very technically complex to introduce a data structure by which branch A learns these values. Hence, given a vote in branch A and a vote in branch B, if all you have are the hashes, and not the epoch depths, then you have no way to tell whether or not NO_SURROUND has been violated.

Enforcement of NO_SURROUND and NO_DBL_PREPARE both depend *crucially* on having the epoch depths very easily accessible. So I don’t see the direction of removing those values from the votes as being fruitful in the slightest - in fact, for efficiency purposes, it’s *keeping the epoch depths but removing the source hash* which is optimal.

---

**yhirai** (2017-11-16):

In the dynamic validator setting, when can the validator set change?

Currently, I’m verifying a version where validator sets can change between a finalized block and its finalizing child.


*(29 more replies not shown)*
