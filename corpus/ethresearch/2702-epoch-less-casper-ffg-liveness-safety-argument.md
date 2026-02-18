---
source: ethresearch
topic_id: 2702
title: Epoch-less Casper FFG liveness/safety argument
author: vbuterin
date: "2018-07-25"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/epoch-less-casper-ffg-liveness-safety-argument/2702
views: 7108
likes: 8
posts_count: 21
---

# Epoch-less Casper FFG liveness/safety argument

**Status: draft, pending verification.**

**Recommended pre-reading: the original Casper FFG paper: [[1710.09437] Casper the Friendly Finality Gadget](https://arxiv.org/abs/1710.09437)**

Suppose that we extend Casper FFG as follows.

- Time is broken up into “slots” (periods of d seconds, eg. d=8).
- The validator set is split up ahead of time into N equal-sized slices, which are repeated (eg. slice 3 of the validator set is called to send messages during slots 3, N+3, 2N+3…).
- During each slot, a single validator can propose a block, and the slice of validators corresponding to that slot can vote for it.
- A vote votes both for a block (its “target”) and for that block’s N-1 nearest ancestors (ie. N blocks in total).
- A block is justified if 2/3 of the validator set votes for it (in any of the N slices that include or follow its slot). Note that any block can be justified, not just epoch-transition blocks. The chain keeps track internally of what the “last justified block” is, and votes use this as their “source”. Note also that a chain only accepts votes if their source is the source specified in the chain, which itself is guaranteed to be an ancestor of the head of the chain.
- If a sequence of N+1 blocks that are all part of the same chain is justified, then the earliest block in the sequence is finalized.
- The two slashing conditions are:

A validator cannot make two distinct votes in the same slot
- A validator cannot make two votes (s1, t1), (s2, t2), where slot(s1) < slot(s2) < slot(t2) < slot(t1), where slot(x) is the “slot number of x” function.

We prove safety as follows. Suppose that two conflicting blocks `b1`, `b2`, with `[slot(b1) ... slot(b1) + 2N)` being the span of slots in which `b1` is finalized. Suppose without loss of generality that `slot(b2) > slot(b1)`. Then, there exists some sequence of slots `j[0] < j[1] < ... < j[n]` representing the justification chain, where `j[0]` is the last justified checkpoint that is also part of the same chain as `b1` (ie. `j[1]` is the first one that is **not**), and `j[n] = slot(b2)`. For each `j[i]`, 2/3 of validators made votes whose slot numbers for the target are in `[j[i] ... j[i] + N)` and for the source are `<= j[i-1]`. We know such a sequence exists because we know `j[n]` is justified and justifying any checkpoint requires some previous justified checkpoint. Let `j[i]` be the highest slot in the sequence where `j[i] < slot(b1)`. We consider three cases:

[![EpochlessFFG](https://ethresear.ch/uploads/default/original/2X/3/32cbf8e09146d4f1f7d94dc2da4ae7becd80bc89.png)EpochlessFFG641×470 11.4 KB](https://ethresear.ch/uploads/default/32cbf8e09146d4f1f7d94dc2da4ae7becd80bc89)

**Case 1:** If `[j[i+1] ... j[i+1] + N)` is fully inside `[slot(b1) ... slot(b1) + 2N)`, then there would be 2/3 of validators voting for something in the `b2` chain intersecting 2/3 of validators voting for something in the b1 chain, implying at least 1/3 violated (1).

**Case 2:** If `j[i+1] >= slot(b1) + 2N`, then 2/3 of validators would have made a vote with a span surrounding `(slot(b1), slot(b1) + 2n)` and 2/3 of validators a vote with a span *within* that same range, meaning at least 1/3 violated (2).

**Case 3:** Now consider the case where `slot(b1) + N < j[i+1] < slot(b1) + 2N`, so `[j[i+1] ... j[i+1] + N)` is partially inside and partially outside `[slot(b1) ... slot(b1) + 2N)`. There are now two subsets of validators: a set v1, which made votes surrounding the span `(slot(b1), slot(b1) + 2n)` and a set v2, which made votes inside of this span. The combined size of v1 and v2 is 2/3, meaning at least 1/3 of them also participated in the `b1` chain. These validators therefore violated conditions (1) or (2), or some combination of both.

Plausible liveness can be proven much more easily. Suppose that `h1` is the highest justified checkpoint. Then, no honest validator made a block with a source higher than `h1`. Suppose `h2` is the highest slot number used up to this point. Then, 2/3 of validators can justify `h2 + N`, using `h1` as a source, and then proceed to fill the span `[h2 + N ... h2 + 3N)`.

## Replies

**djrtwo** (2018-07-25):

I’m a bit confused about how “source” works in this context. Are votes with a different implied “source” congruent? Because the last justified epoch can update potentially every slot, the votes for a Block M, as they arrive during slot M and future slots, could be different for each subsequent slot.

EDIT:

For clarity:

Votes for `Block M` are for `Block M` and its N-1 nearest ancestors. `Block M - (N - 1)` becomes justified due to the implicit votes pushing it over the 2/3 threshold. It is now the “last justified block”.

1. Is the “source” for these Block M votes now Block M - (N - 1) or is the still the previous last justified epoch?
2. Now votes for Block M + 1 come in. These potentially have a different “source” than the Block M votes (depending on the answer to question 1), but they certainly have different “source” than votes from slot M-1. Many of the implied ancestor votes from Block M + 1 are for blocks that were explicitly or implicitly voted for in previous slots with different “sources”. The spec seems to imply that these votes with different sources are congruent and can be summed. True?

EDIT2:

I think it makes sense if we add these two conditions:

1. When explicit votes for Block M come in, the implicit and explicit votes are applied from oldest to youngest ancestor.
2. The initial votes for a Block M at Slot M set and dictate the “source” for all future implied votes for Block M.

(1) will ensure that younger blocks get the latest possible source epoch and (2) gets rid of my above concerns by enforcing a standard “source” for future votes on the same block.

---

**vbuterin** (2018-07-25):

I suppose I am allowing source epochs to be different, though there is an implied weaker requirement that the source checkpoints must all be part of the same chain. So if there are votes from 2/3 of validators in the span right after `b2` justifying `b2`, what we know is that there exists some prior justified checkpoint with height `s[n-1]`, and the spans of all of the votes for `b2` include `(s[n-1], s(b2))`.

---

**naterush** (2018-07-25):

> Suppose that two conflicting blocks b1, b2, with [s(b1) … s(b1) + 2N) being the span of slots in which b1 is finalized.

Couldn’t `b1` be finalized in the span `[s(b1) ... s(b1) + 5/3N)`? Not sure if affects the proof, but it seems like we both don’t need the last 1/3 of validators to finalize `b1`, and also want to minimize the number of slots used to minimize overlap w/ `b2`.

> Then, there exists some sequence of slots s[0]  Let s[i] be the highest slot in the sequence where s[i] < s(b2)

Same line of questioning as above - is `s[i]` the slot during which the parent block of `b2` was made?

---

Haven’t gotten through the safety proof b/c of the above questions, but is correct that rotating which validators are in a specific slice doesn’t change it? It seems like there might be issues if they are rotated too quickly (e.g. it seems like latency would increase if validators were rotated before all `N` slots), but reshuffling at the end of every `N` slots seems fine.

Btw, yay for being able to parameterize [overhead per decision](https://twitter.com/VladZamfir/status/942278180408381440) in FFG ::))

---

**vbuterin** (2018-07-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/naterush/48/4241_2.png) naterush:

> Couldn’t b1 be finalized in the span [s(b1) ... s(b1) + 5/3N) ? Not sure if affects the proof, but it seems like we both don’t need the last 1/3 of validators to finalize b1 , and also want to minimize the number of slots used to minimize overlap w/ b2 .

Sure; in the happy case, if you get 2/3 votes by s(b1) + 5/3N you can just shortcut and say then that the block is finalized.

![](https://ethresear.ch/user_avatar/ethresear.ch/naterush/48/4241_2.png) naterush:

> “The justification chain that led to b2 being finalized” sounds like the sequence of justified N+1 blocks in the same chain that all become justified, and thus finalize the first block (which is b2 ). However, given that s[n] = s(b2) , this doesn’t make sense. Is this sequence of slots s[0] < s[1] < ... < s[n] the slots that made the blocks from b2 all the way back to the b2 's most-recent common ancestor with b1 ?

Aah, perhaps I should have written `s[n-1] = s(b2)`. To answer precisely, it’s a chain of span numbers of justified blocks, with the property that for each `s[i]`, 2/3 of validators voted with targets between `s[i]` and `s[i] + N`, and sources <= `s[i-1]`.

---

**vbuterin** (2018-07-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/naterush/48/4241_2.png) naterush:

> but reshuffling at the end of every N slots seems fine.

Reshuffling could break the proof theoretically. On average, since the span `[kN + N/2, k(N+1) + N/2]` contains two independently sampled halves, it would only contain 75% of the validator set, and a randomly selected 2/3 of it would only contain ~55.5%. Hence, one could double-finalize with only 1/9 equivocating (and possibly even zero equivocating if the attacker can choose well which nodes to attack with). Without reshuffling, we maintain the hard property that any sequence of N slots actually contains all the nodes.

Hence at this point I’d favor either only reshuffling at dynasty boundaries, or finding a way to reshuffle a small amount per epoch.

---

**kladkogex** (2018-07-26):

As an example, if the total network has 1/4 bad guys

then probability that a 100-node slot contains more than 1/3 bad guys is  0.02759456413 using binomial calculator

https://stattrek.com/online-calculator/binomial.aspx

If a single slot contains more than 1/3 bad guys , how bad it is? these bad slots in the example above will repeat every 50 slots

In other word, what is the assumption made by the proof above? Is the assumption “the overall network has less 1/3 of bad guys” or “every slot has less than 1/3 bad guys?”

---

**vbuterin** (2018-07-26):

I think that you can prove a very strong safety claim (“the chain never reverts”) if you have every slice having less than 1/2 bad guys, and the network latency sufficiently low. If some slices have >1/2 bad guys, then the chain may sometimes revert a few blocks, though as long as the chain as a whole has <1/2 bad guys, it should still keep progressing.

Edit: though it probably won’t “finalize” if there are >1/3 bad guys.

---

**naterush** (2018-07-26):

Thanks! Spent some more time on the safety proof with [@djrtwo](/u/djrtwo) - have a couple more questions ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=12)

> Then, there exists some sequence of slots s[0]  Let s[i] be the highest slot in the sequence where s[i]  If s[i+1] is fully in the span [s(b1) … s(b1) + N]

When you refer to some slot `s[i+1]` being fully in this span it’s because a slot in the sequence can be understood as the range from that slot to the slot `N` in the future, right?

Aka: `s[i+1]` is a range of `N` slots. In case 1, the range is entirely in `[s(b1) ... s(b1) + 2N)`. In case 2, the range starts above ` s(b1) + 2N`. In case 3, the range is starts in `[s(b1) ... s(b1) + 2N)` and ends above it.

---

**vbuterin** (2018-07-26):

Added all the fixes, thanks!

---

**naterush** (2018-07-26):

Thanks for the changes! One or two more residual nitpicks ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=12)

> where j[0] is the first justified checkpoint that is not part of the same chain as b1

Shouldn’t it be "most recent justified block that *is* part of the same chain as `b1`?

> Case 1: If [s[i+1] … s[i+1] + N)

There are some residual `s`’s that should be `j`’s in cases 1-3.

---

**vbuterin** (2018-07-26):

Fixed again ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

---

**naterush** (2018-07-28):

It seems fairly simple to extend this algorithm to be live in partial synchrony - unless I’m missing something.

One simple approach is: if a newly added block does not finalize any previous blocks in its chain, increase the length of the timeout `d` by some constant. As soon as any new block is finalized, set `d` back to its base value.

Another possible approach (that is closer to the [Exponential epoch backoff](https://ethresear.ch/t/exponential-epoch-backoff/1152)) would be doubling `d` at the end of a period of `N` blocks in which nothing new has been finalized, and setting `d` back to its base value when something is finalized.

In the case of no finality, both strategies will continue to increase the timeout until it is greater than network latency, in which case blocks can again be finalized.

---

**vbuterin** (2018-07-28):

In general, any “safe under asynchony, live under synchrony” consensus algorithm can be trivially converted into a “live under partial synchrony” algorithm. The most general-purpose strategy is simple: replace all references to time with a reference to sqrt(t - t0). The amount of real time that it takes to increment one unit of sqrt time increases without limit, so the network latency measured in sqrt time will eventually drop below any specific threshold.

I think the challenge is though that we want slot intervals to line up across branches, which any kind of “reset the interval growth upon dynasty changes” would preclude. Unless we’re ok with relaxing the criterion to “we want slot intervals to line up across branches within a dynasty”. We’re already ok with reshuffling across dynasties so maybe it could be fine…

---

**NicLin** (2018-08-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Case 3: Now consider the case where slot(b2) + N  A vote votes both for a block and for its N-1 nearest ancestors (ie. N blocks in total) as targets.

I’m a little confused by this. Does this mean vote target is a sequence of N blocks instead of just one block?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> For each j[i] , 2/3 of validators made votes with targets in [j[i] ... j[i] + N) and sources  Hence at this point I’d favor either only reshuffling at dynasty boundaries, or finding a way to reshuffle a small amount per epoch.

How’s the dynasty boundary defined in this design?

---

**vbuterin** (2018-08-02):

Fixed, thanks!

See [Beacon chain Casper mini-spec](https://ethresear.ch/t/beacon-chain-casper-ffg-rpj-mini-spec/2760) for a possible description of how dynasties could change.

---

**naterush** (2018-08-17):

It seems like these proofs can be extended to remove the in-protocol (safety) fault tolerance threshold for non-validator nodes. In this modified version, nodes detect safety in the following way:

- Nodes choose a fault tolerance threshold 0 < t < 1. They consider a block justified_t if at least 1/2 + t/2 of the validator set votes for it (in any of the N slots that include or follow its slot).
- If there are N + 1 justified_t blocks in a row, the first block in this sequence is considered finalized with fault tolerance t.

Note that 1/2 refers to half of the weight of the entire validator set. 0 < t as otherwise safety could be detected on two chains, each with 1/2 of the validator set.

The safety proof follows a similar structure to the original proof (just replacing 2/3 with 1/2 + t/2), so we just consider each case:

**Case 1:** If  `[j[i+1] ... j[i+1] + N)`  is fully inside  `[slot(b1) ... slot(b1) + 2N)` , then there would be 1/2 + t/2 of validators voting for something in the  `b2`  chain intersecting 1/2 + t/2 of validators voting for something in the b1 chain, implying at least 1/2 + t/2 + 1/2 + t/2 -1 = t violated (1).

**Case 2:** If  `j[i+1] >= slot(b1) + 2N` , then 1/2 + t/2 of validators would have made a vote with a span surrounding  `(slot(b1), slot(b1) + 2n)`  and 1/2 + t/2 of validators a vote with a span *within* that same range, meaning at least t violated (2).

**Case 3:**  Now consider the case where  `slot(b1) + N < j[i+1] < slot(b1) + 2N` , so  `[j[i+1] ... j[i+1] + N)`  is partially inside and partially outside  `[slot(b1) ... slot(b1) + 2N)` . There are now two subsets of validators: a set v1, which made votes surrounding the span  `(slot(b1), slot(b1) + 2n)` and a set v2, which made votes inside of this span. The combined size of v1 and v2 is 1/2 + t/2, meaning at least t of them also participated in the  `b1`  chain. These validators therefore violated conditions (1) or (2), or some combination of both.

---

The above changes seem to make the plausible liveness proof more complicated (as expected). Nodes who choose t > 1/3 may have t - \epsilon equivocate, and as 1 - t - \epsilon < 2/3 < 1/2 + t/2, it may be impossible for a large enough quorum to form to finalize any more blocks. However, for nodes that run at t \leq 1/3, the proof should remain the same.

Furthermore, I think this scheme changes the forkchoice that nodes should run. Namely, starting from the highest justified block may not make sense, as different nodes have different opinions on what is justified. This seems fixable by having nodes start their forkchoice from their last finalized block, but again this might complicate the plausible liveness proof…

Finally, I’m not sure how this interacts with how the current approach has the chain store the `last_justified_slot` and only include attestations that attest to this. This approach seems to make it impossible to remove the fault tolerance threshold for validators (as we need them all to see the same `last_justified_slot`)…

---

As an interesting side note, this forkchoice and the above safety oracle (N + 1 justified blocks in a row) seem to fit fine into the CBC Casper framework. That is - I think the “mini-fault tolerance crisis” was a property just of the class of estimators we were considering, rather than CBC as a whole ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**vbuterin** (2018-08-17):

The problem is that it doesn’t matter what a client thinks is justified, because the slashing conditions only care about what the *protocol* thinks is justified, which is 2/3. You could imagine a protocol where validators need to link to multiple justified checkpoints, one for each fault tolerance level, but I haven’t yet found a way to do this that doesn’t lead to undesirable edge cases.

---

**vbuterin** (2018-08-17):

I’ll elaborate on one edge case here. Suppose that a vote must refer to two justified checkpoints, one at the 4/5 level and one at the 3/5 level. Suppose that the status quo looks like this, where the number in each circle is the percentage that voted for that checkpoint:

![image](https://ethresear.ch/uploads/default/original/3X/a/0/a0d878c96118076161a45f6b4de9c27ff03a108e.svg)

The winning branch is clearly the rightmost one, the last 4/5-justified checkpoint is yellow, the last 3/5-justified checkpoint is blue, and green is 3/5-finalized. But now, suppose a new 4/5-justified checkpoint gets created as follows:

![image](https://ethresear.ch/uploads/default/original/3X/e/8/e85ac5a0714f3acef428b357aee61953a1832d76.svg)

Now, the orange checkpoint is 4/5-justified and has a higher epoch, so by a fork choice rule that says “highest-finality highest-justified-epoch checkpoints win”, the fork choice would switch to it, nullifying the 3/5-finality of the green block.

---

**naterush** (2018-08-26):

Interesting. It seems like we might want our forkchoice to have the property that it returns the same block(s) no matter the fault tolerance threshold of the node running it. Latest-message-driven GHOST in CBC has this property even if nodes run the forkchoice starting from their last finalized block (which is something dependent on their fault tolerance threshold), as the forkchoice will always select *all blocks* that have *any* amount of fault tolerance.

I don’t totally understand your example. Why are nodes necessarily using a “highest-finality highest-justified-epoch checkpoints win” forkchoice? It seems like there might be a variant of the forkchoice that has the above property - which seems like enough to me, but maybe I’m missing something…

---

**vbuterin** (2018-08-26):

> Why are nodes necessarily using a “highest-finality highest-justified-epoch checkpoints win” forkchoice?

Because if they don’t do that then that’s far enough from the original algo that it’s probably best not to call it FFG ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

Though I guess names don’t matter, optimal algorithms do; in this case there’s still the efficiency issue: what slashing conditions do you add to ensure that validators are not violating the protocol in ways that break finality, and how do you efficiently validate them?

