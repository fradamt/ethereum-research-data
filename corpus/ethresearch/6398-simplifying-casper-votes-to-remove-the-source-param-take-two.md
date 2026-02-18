---
source: ethresearch
topic_id: 6398
title: Simplifying Casper votes to remove the “source” param (take two)
author: jacob-eliosoff
date: "2019-11-01"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/simplifying-casper-votes-to-remove-the-source-param-take-two/6398
views: 1668
likes: 0
posts_count: 3
---

# Simplifying Casper votes to remove the “source” param (take two)

I wanted to sketch a possible tweak to Casper FFG, related to my [post last year](https://ethresear.ch/t/should-we-simplify-casper-votes-to-remove-the-source-param/3549) about the possibility of removing the “source” param from the votes (“attestations”) validators cast.  (See also four old Twitter threads: [Casper walkthrough](https://twitter.com/JaEsf/status/1041485169776058369), [Casper in one tweet](https://twitter.com/JaEsf/status/1039031211660783616), [earlier walkthrough](https://twitter.com/JaEsf/status/1037960095412486144), [@danrobinson](/u/danrobinson) [clarifying](https://twitter.com/danrobinson/status/1037703192748990464).)  I was spurred to revisit the topic by [@djrtwo](/u/djrtwo)’s talk at Devcon Osaka, where the definition of finalization seemed messy to me.

The main motivations for this work are simplicity/clarity, especially of finalization, and robustness under network lag.  See the final section below for six potential benefits.

If there’s a better forum for discussing this stuff, please point me at it!  I’m also happy to chat…

### Sketch of proposal

1. As a validator, you’re always casting two types of votes: the block B you’re “voting for”, and the earlier block F you’re “voting-to-finalize”.
2. Time is broken down into 6-second slots.  In each slot, you can update your B and/or F, or (by default) leave either or both unchanged from the previous slot.
3. You can only vote-to-finalize a block F in slot s if:
a) block_height(F) ≥ block_height(F’), your previous vote-to-finalize; and
b) F received 2/3 of the votes in some slot sF 1/3 of votes in slot sF were for blocks other than F.
- c): at some slot s’ (sF 1/3 of votes were for blocks that aren’t ancestors of B.

### Definition of finalization

A block F is **finalized** as of some slot s, if 2/3 of votes-to-finalize in s are for F or descendants of F.

### Safety and liveness

I believe safety and liveness follow from the rules and definition above.  I can try to sketch proofs if anyone’s interested…

### Why do it this way?

Some possible advantages over existing FFG (as I understand it!): (see also the related list in [last year’s post](https://ethresear.ch/t/should-we-simplify-casper-votes-to-remove-the-source-param/3549))

1. The definition of finalization above is simpler than the definition I understood from @djrtwo’s talk, with its “k=1, k=2, k=3” cases.
2. Having each validator keep track of two things - the B it’s voting for, and the F it’s voting-to-finalize - is to me more intuitive than FFG’s “source” and “checkpoint edge”.
3. Time (slot number) and block height are distinguished.  You can vote repeatedly for the same block (at the same height) in successive slots: by default your B and F stay unchanged from slot to slot.  (It might make sense to require votes to refer to the previous vote - a “votechain”! - to prevent validators from filling in skipped votes later.)
4. A block can be finalized many slots after it was justified (got 2/3 of votes), whereas I believe in regular FFG it must be finalized the immediate block after.  This could be useful, eg, in situations where a laggy network means validators are having trouble updating their votes every 6 seconds.
5. The slashing rules above are tighter than FFG’s: FFG slashes more cases than are required to guarantee safety and liveness.  (See also the @JustinDrake and @dlubarov notes in the post linked above.)
6. Each validator’s “vote-to-finalize” blocks increase monotonically in height: you’re prohibited from linking your current vote to an arbitrarily old justified block.  This might simplify some things.

## Replies

**vbuterin** (2019-11-05):

> whereas I believe in regular FFG it must be finalized the immediate block after.

It must be finalized the immediate *epoch* after, so 6 minutes.

> b): >1/3 of votes in slot sF were for blocks other than F.

This slashing condition seems risky, because it means that if you make a vote before you see >1/3 such votes, but later on other people make such votes, then you can get slashed even though you did nothing wrong from your own point of view.

---

**jacob-eliosoff** (2019-11-05):

> It must be finalized the immediate  epoch  after, so 6 minutes.

Oh yeah, good point.  Anyway there might be some situation where that next-epoch requirement is annoying (though honestly none leap to mind?)

> b): >1/3 of votes in slot sF were for blocks  other  than F.

This slashing condition seems risky, because it means that if you make a vote before you see >1/3 such votes, but later on other people make such votes, then you can get slashed even though you did nothing wrong from your own point of view.

No, rule b) is so you get slashed if, in slot s, you **vote-to-finalize** a block F that, in slot sF, received <2/3 of **votes**.  That is, you must wait till you see F got 2/3 of votes before voting-to-finalize F.  The people who voted for the non-F 1/3 in slot sF don’t get slashed!

