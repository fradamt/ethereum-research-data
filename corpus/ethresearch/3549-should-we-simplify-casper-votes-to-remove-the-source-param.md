---
source: ethresearch
topic_id: 3549
title: Should we simplify Casper votes to remove the "source" param?
author: jacob-eliosoff
date: "2018-09-25"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/should-we-simplify-casper-votes-to-remove-the-source-param/3549
views: 2685
likes: 12
posts_count: 17
---

# Should we simplify Casper votes to remove the "source" param?

Casper FFG votes are (essentially) of the form `vote(target, source)`, where `target` is the checkpoint you’re voting for and `source` is a justified ancestor of `target`.  `source` is handy for the safety proof.  However, `source` isn’t *necessary* to ensure safety, and I argue removing it - so votes were just of the form `vote(target)` - would be a net win.  Curious to hear what others think.

Main arguments I see for **removing** `source`:

1. It’s confusing.  “Each validator votes for one branch at each height” is intuitive; “Each validator votes for one branch at each height, linking to a block at an earlier height” is not.  Eg, this confused Matthew Green (and me).
2. It’s not necessary.  As I argued in a recent post, safety can be ensured without source.  This also results in a simpler definition of a finalization vote (a boolean finalize=true flag included with votes, rather than an explicit reference to the immediate parent checkpoint), and a simpler slashing condition than the “no-spanning rule” - a “no-reneging rule”: “If you vote to finalize A, you can’t vote for conflicting B, unless 2/3 of voters (not including you) voted for ancestor B’ of B at height between A and B.”
3. As @dlubarov (in June) and @JustinDrake (this month) have argued, the no-spanning rule for source is needlessly strict: it slashes more cases than needed to ensure safety.  Eg, it slashes spanning votes even if (as Daniel noted) the spanned vote wasn’t a finalization vote, or (as I noted) if none of the four checkpoints conflict.  Slashing more cases than necessary is gratuitous and confusing.  Both Daniel and Justin proposed ways the no-spanning rule can be amended to be “tight” (not slash unnecessarily) without removing source, but removing it is another, arguably more parsimonious solution to consider.
4. Making voters specify source pointlessly opens the door to bizarre cases.  Why let a voter specify a source 100 checkpoints old, if there are 99 more recent justified ones?  Why allow the case where 2/3-ε vote for (t, s) and ε vote for (t, s’s parent), resulting in a failed vote for (t, s) rather than what is intuitively a successful 2/3 vote for t?  source should really always be “the most recent ancestor of target that I know to be justified”; letting voters choose any other source just creates opportunities for confusion and unnecessarily failed votes.

(EDIT: Another silly case we enable by making voters specify source, courtesy of @danrobinson: votes with unjustified sources.  There is really no point to allowing these…)

Main arguments I see for **keeping** `source`:

1. Casper FFG works fine with source.  Why tinker with it now?
2. My proposed no-reneging slashing condition that doesn’t rely on source is more complicated to enforce, since “vote v2 spans v1” is easier to check than “vote v2’s target has no justified ancestor at height >v1”.  (See discussion in my post.)  So, I see this as a question of whether clearer, more parsimonious voting is worth the price of somewhat more elaborate slashing mechanics.
3. At least one person (@MihailoBjelic) finds vote(target, source) easier to understand than vote(target).  If most of you agree, then we should certainly keep it!

We all want Casper deployed, so now is not the time for cute new features or experimental variants.  But I do think we should consider *simplifications* if they result in greater clarity and cleaner code (and if they work!).  Eg: either removing source (as I advocate), or at least tightening up the no-spanning rule (as Justin and, I think, Daniel advocate).

## Replies

**dlubarov** (2018-09-26):

Are you thinking votes would be stored on-chain? I’m not sure if the plan is on-chain or gossip voting. (Or maybe some hybrid, like gossip voting with threshold signatures included on-chain to show the results?)

If votes are off-chain though, I think source parameters are the easiest way to handle slashing. Like say a validator votes `a`, then switches to `b`, a higher-depth checkpoint on a different branch. If `b` has a justified ancestor whose height is at least `h(a)`, then the vote is legit, but if not, we need a way to either ignore the vote or slash the validator.

But without source params, it seems tough to prove that a validator switched branches illegally. Even if most validators don’t see any justified ancestor, it’s possible that the justification votes just haven’t propagated yet.

---

**jacob-eliosoff** (2018-09-26):

I wasn’t thinking to change how votes are stored, though I may be missing a motivation for doing so.  I agree that removing `source` makes slashing more complex: this is one of the main tradeoffs.  The approach I proposed in my [Medium post](https://medium.com/@jacob.eliosoff/a-simplified-look-at-ethereums-casper-4fa9461b245) was, the slasher gives two votes A and B she claims violated no-reneging, and the slashee has n months to counter with a justified ancestor of B.  There may be other ways to handle it, but the big picture is: removing `source` makes voting simpler, slashing more complicated (but, I argue, still safe).

---

**vbuterin** (2018-09-26):

You need the source to be part of the vote to enforce the no-surround condition, even the more relaxed version.

---

**jacob-eliosoff** (2018-09-26):

Well, I’m arguing for scrapping the no-surround condition (I called it the no-spanning rule) in favor of what I call the no-reneging rule.  More details in my [Medium post](https://medium.com/coinmonks/a-simplified-look-at-ethereums-casper-4fa9461b245).

---

**dlubarov** (2018-09-26):

Ah, I missed that bit about the interactive slashing protocol. Makes sense now.

I think the interactive protocol would be pretty nontrivial once we add some incentives and limits. Probably not worth the tradeoff IMO.

---

**dlubarov** (2018-09-26):

Re your first point about confusion, I think it comes down to whether most readers want to understand the slashing protocol or not. If not, Casper could be explained in terms of voters becoming “locked” and “unlocked” (like the Tendermint paper); source parameters could be considered an implementation detail for the yellow paper.

---

**dahliamalkhi** (2018-09-26):

since no-reneging (or equivalently, Tendermint’s lock/unlock) are sufficient for safety, and since no one would want to risk slashing and actually cast a “spanning” vote, it indeed appears somewhat redundant.

many recent systems (e.g., Byzcoin, Concord, Hot-Stuff, Dfinty) have clever ways to aggregate votes. A voter can then piggyback a “quorum-certificate” that proves that she received 2/3 votes that justifies her vote.

---

**jacob-eliosoff** (2018-09-26):

I’m not familiar with all those systems, but it’s certainly true that no-reneging has a clear predecessor in Tendermint’s lock/unlock rules, especially “Unlock-on-Polka”.

The main difference I see is in Casper you lock on a *branch,* not a block.  So blocks can keep getting added w/o finalization, as no blocks at each height get a 2/3 vote (“polka”), or one does get 2/3 (“unlocking” validators locked on other branches) but fails to get the subsequent 2/3 finalization (“commit”); until eventually some branch finally does.

---

**vbuterin** (2018-09-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/jacob-eliosoff/48/4185_2.png) jacob-eliosoff:

> Well, I’m arguing for scrapping the no-surround condition (I called it the no-spanning rule) in favor of what I call the no-reneging rule. More details in my Medium post

Your no-reneging rule basically says that if you make a finalization vote on P, you can’t vote for any Q with a higher slot number than P that’s not a descendant of P unless an ancestor of Q is itself justified at a point after P. But then how would you track whether or not an ancestor of Q is justified? Answer: by having a variable keep track of when it was last justified. What would the slashing condition be? Two votes v1, v2 are invalid if slot(v2) > slot(v1) but it’s not the case that last_justified(v2) > last_justified(v1), ie. source(v2) < source(v1) < slot(v1) < slot(v2).

So you’ve basically reinvented a different way of describing the no-spanning rule.

---

**jacob-eliosoff** (2018-09-26):

Yes, kind of.  But as described above, there are some differences:

1. As @dlubarov and @JustinDrake argued, the current no-spanning rule slashes cases that their tightened versions (or the no-reneging rule) don’t: eg, if the spanned vote is not a finalization vote, or if the two votes’ targets don’t conflict.
2. The difference between what Justin proposed and what I’m proposing comes down to who keeps track of your last-justified variable.  I’m proposing that the protocol (the slasher, I suppose) should track it, rather than the voter specifying it:

> Making voters specify  source  pointlessly opens the door to bizarre cases. Why let a voter specify a source 100 checkpoints old, if there are 99 more recent justified ones? Why allow the case where 2/3-ε vote for (t, s) and ε vote for (t, s’s parent), resulting in a failed vote for (t, s) rather than what is intuitively a successful 2/3 vote for t?  source  should really always be “the most recent ancestor of  target  that I know to be justified”; letting voters choose any other source just creates opportunities for confusion and unnecessarily failed votes.
>
> (EDIT: Another silly case we enable by making voters specify  source , courtesy of @danrobinson: votes with unjustified  source s. There is really no point to allowing these…)

It’s a bit like the difference between BASIC making you specify your line number and other languages tracking it themselves.  Or explicit type declaration vs implicit type inference,

---

**vbuterin** (2018-09-26):

So basically the slashing condition verifier would have to check Merkle branches pointing to the source in the state tree whose root hash is specified by the vote to figure out what the source is?

Yeah, sure, you can do that. I suppose my aesthetics tell me that it’s much simpler on net to have the source be explicit rather than have to be figured out in such a relatively complicated way.

---

**jacob-eliosoff** (2018-09-26):

It seems no harder than checking which blocks are finalized, and I’m sure a lot of people/code are going to need to do that.

---

**dahliamalkhi** (2018-09-26):

[@vbuterin](/u/vbuterin) seems like the verifier needs to check that there are 2/3 votes on the source anyway, even if the voter specifies it, correct? so why not simply check if the vote is justified?

that said, as I pointed out before, it may be more efficient for the vote itself to carry constant size information to demonstrate it is justified.

---

**MihailoBjelic** (2018-09-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Yeah, sure, you can do that. I suppose my aesthetics tell me that it’s much simpler on net to have the source be explicit rather than have to be figured out in such a relatively complicated way.

I generally agree with this. Also, as [@jacob-eliosoff](/u/jacob-eliosoff) already noted, “source-target” votes make slashing conditions easier to grok for me (it might be only because I originally learned them like that, though).

Speaking off the top of my head, I think it would be nice if we could keep “source-target” votes, but tighten the second condition (there’s definitely no need to slash votes that can do no harm)… However, if that would cause new delays, rewriting a lot of code/specs, maybe we shouldn’t change anything for now (at the end of the day, it would be unacceptable if the conditions are tighter, i.e. less strict than necessary, and this is opposite).

---

**jacob-eliosoff** (2018-09-26):

Note that keeping `source` but tightening up the no-spanning/no-surround condition is pretty much [@JustinDrake](/u/justindrake)’s [proposal](https://ethresear.ch/t/a-tight-and-intuitive-casper-slashing-condition/3359).

---

**MihailoBjelic** (2018-09-27):

Not completely, he eliminated Condition I and [@dlubarov](/u/dlubarov) pointed that that could be an issue, but I agree it’s generally close to what I proposed, and it might be a step in the right direction (at least IMHO).

